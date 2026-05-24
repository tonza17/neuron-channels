"""Build ``results/metrics.json`` for t0122 (REQ-22).

Uses the explicit multi-variant format. Reports the registered metric
``direction_selectivity_index`` with three variants per the plan
REQ-22:

* ``best_legit`` -- highest DSI among LEGIT cells (non-silence-failed,
  DSI in [0.5, 0.9999), PD-rate >= 30 Hz, volume <= 50000 um^3).
* ``overall_max`` -- highest DSI across all unique evaluated cells
  (includes the silence-corner ceiling cells at DSI = 1.0).
* ``dsi_eq_one_count`` -- count of cells whose DSI >= 0.9999, reported
  as the metric value (cells -- a coarse signal of how saturated the
  silence guard is).

Per the plan, ``cytoplasm_volume_um3`` is NOT a registered metric in
``meta/metrics/``, so the cytoplasm-volume axis is reported as part of
each variant's ``dimensions`` block (``min_cytoplasm_volume_um3``,
``mean_top10_cytoplasm_volume_um3``) but does not appear in the
``metrics`` block.

Registered metrics applicability check (per planning skill Phase 1
step 7): the project registers 4 metrics. ``direction_selectivity_index``
applies here. ``tuning_curve_*`` do NOT apply because this task uses
2-direction PD-vs-ND-only evaluation, not a full angular sweep.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.constants import T0122_SEEDS
from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.paths import (
    RESULTS_DATA_DIR,
    RESULTS_DIR,
    ensure_directories,
)

DSI_LEGIT_THRESHOLD: float = 0.5
PD_RATE_LEGIT_THRESHOLD_HZ: float = 30.0
DSI_SILENCE_CEILING: float = 0.9999
VOLUME_LEGIT_CEILING_UM3: float = 50000.0


def _load_all_evaluations(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"all_evaluations_seed{seed}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["evaluations"]


def _load_cuntz_summary(*, seed: int) -> dict[str, Any] | None:
    path = RESULTS_DATA_DIR / f"cuntz_top10_seed{seed}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _is_legit(*, cell: dict[str, Any]) -> bool:
    return (
        float(cell["dsi_vector_sum"]) >= DSI_LEGIT_THRESHOLD
        and float(cell["dsi_vector_sum"]) < DSI_SILENCE_CEILING
        and float(cell["pd_rate_hz"]) >= PD_RATE_LEGIT_THRESHOLD_HZ
        and float(cell["cytoplasm_volume_um3"]) <= VOLUME_LEGIT_CEILING_UM3
    )


def build_metrics_for_seed(*, seed: int) -> list[dict[str, Any]]:
    cells = _load_all_evaluations(seed=seed)
    cuntz = _load_cuntz_summary(seed=seed)
    n_cells = len(cells)
    legit = [c for c in cells if _is_legit(cell=c)]
    n_legit = len(legit)
    dsi_eq_one = [c for c in cells if float(c["dsi_vector_sum"]) >= DSI_SILENCE_CEILING]
    n_dsi_eq_one = len(dsi_eq_one)
    best_legit_dsi = max((float(c["dsi_vector_sum"]) for c in legit), default=0.0)
    overall_max_dsi = max((float(c["dsi_vector_sum"]) for c in cells), default=0.0)

    # Cytoplasm-volume axis dimensions: legit cells only.
    min_volume_legit = min(float(c["cytoplasm_volume_um3"]) for c in legit) if n_legit > 0 else None

    # Top-10 LEGIT by DSI for the mean-top10 metric dimension.
    top10_legit = sorted(
        legit,
        key=lambda c: (
            -float(c["dsi_vector_sum"]),
            float(c["cytoplasm_volume_um3"]),
        ),
    )[:10]
    mean_top10_legit_volume = (
        float(sum(c["cytoplasm_volume_um3"] for c in top10_legit) / len(top10_legit))
        if len(top10_legit) > 0
        else None
    )

    base_dims: dict[str, Any] = {
        "task_seed": int(seed),
        "init_method": "lhs_random",
        "n_obj": 2,
        "n_directions": 2,
        "dsi_metric": "ratio",
        "dsi_silence_guard_active": True,
        "silence_guard_threshold_pd_spikes": 3,
        "n_eval_seeds": 3,
        "n_generations_target": 60,
        "n_cells": int(n_cells),
        "n_legit": int(n_legit),
        "n_dsi_eq_one": int(n_dsi_eq_one),
        "pool_restart_every": 10,
        "hv_plateau_auto_stop_disabled": True,
        "min_legit_cytoplasm_volume_um3": min_volume_legit,
        "mean_top10_legit_cytoplasm_volume_um3": mean_top10_legit_volume,
        "cuntz_in_band_count": (cuntz["in_band_count"] if cuntz is not None else None),
        "cuntz_finite_count": (cuntz["finite_count"] if cuntz is not None else None),
    }

    variants: list[dict[str, Any]] = []
    variants.append(
        {
            "variant_id": f"t0122-seed{seed}-best-legit",
            "label": (
                f"t0122 NSGA-II seed {seed}: best legit DSI (highest non-silence-guard cell)"
            ),
            "dimensions": {**base_dims, "dsi_subvariant": "best_legit"},
            "metrics": {
                "direction_selectivity_index": float(best_legit_dsi),
            },
        }
    )
    variants.append(
        {
            "variant_id": f"t0122-seed{seed}-overall-max",
            "label": (
                f"t0122 NSGA-II seed {seed}: overall max DSI (silence-guard "
                f"saturated cells included)"
            ),
            "dimensions": {**base_dims, "dsi_subvariant": "overall_max"},
            "metrics": {
                "direction_selectivity_index": float(overall_max_dsi),
            },
        }
    )
    variants.append(
        {
            "variant_id": f"t0122-seed{seed}-dsi-eq-one",
            "label": (
                f"t0122 NSGA-II seed {seed}: silence-guard ceiling cell count (cells at DSI = 1.0)"
            ),
            "dimensions": {**base_dims, "dsi_subvariant": "dsi_eq_one_count"},
            "metrics": {
                # The metric value reports the saturation level: 1.0 if
                # any cells saturated, 0.0 otherwise. The actual count
                # lives in ``dimensions.n_dsi_eq_one``.
                "direction_selectivity_index": 1.0 if n_dsi_eq_one > 0 else 0.0,
            },
        }
    )
    return variants


def build_metrics() -> dict[str, Any]:
    variants: list[dict[str, Any]] = []
    for seed in T0122_SEEDS:
        variants.extend(build_metrics_for_seed(seed=int(seed)))
    return {"variants": variants}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=RESULTS_DIR / "metrics.json")
    args = parser.parse_args()
    ensure_directories()
    payload = build_metrics()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[metrics_builder] wrote {args.out} with {len(payload['variants'])} variants")


if __name__ == "__main__":
    main()
