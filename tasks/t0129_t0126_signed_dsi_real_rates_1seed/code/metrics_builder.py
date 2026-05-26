"""Build ``results/metrics.json`` for t0123 (REQ-23).

Uses the explicit multi-variant format per
``arf/specifications/metrics_specification.md``. Reports the registered
metric ``direction_selectivity_index`` as a TRACKED DIAGNOSTIC (not an
optimised axis) in three of the four variants, alongside the ad-hoc
keys ``mi_count_bits``, ``atp_per_spike_molecules``, and
``mi_strong_bialek_bits_per_sec`` (the two optimised axes plus the
post-hoc bits/s rate).

Variant set:

* ``best_legit`` -- best Pareto-cell stats in the LEGIT cohort
  (DSI >= 0.5 AND PD-rate >= 30 Hz AND NOT silence-failed).
* ``overall_max_mi`` -- population-wide max ``mi_count_bits``.
* ``overall_min_atp`` -- population-wide min ``atp_per_spike_molecules``.
* ``top10_strong_bialek`` -- aggregate over the top-10 Pareto cells from
  the post-hoc Strong-Bialek rerun.

Registered-metric applicability (per planning skill Phase 1 step 7):

* ``direction_selectivity_index`` applies (tracked diagnostic).
* ``tuning_curve_*`` do NOT apply -- this task uses 4 antipodal
  directions only, not a full angular sweep with a target tuning curve.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.constants import T0129_SEEDS
from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.paths import (
    RESULTS_DATA_DIR,
    RESULTS_DIR,
    ensure_directories,
)

DSI_LEGIT_THRESHOLD: float = 0.5
PD_RATE_LEGIT_THRESHOLD_HZ: float = 30.0


def _load_cell_trace_jsonl(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"cell_trace_seed{seed}.jsonl"
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def _load_all_evaluations(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"all_evaluations_seed{seed}.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("evaluations", []))


def _load_strong_bialek_top10() -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / "post_hoc_strong_bialek_mi_top10.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("cells", []))


def _is_legit_diagnostic(*, row: dict[str, Any]) -> bool:
    dsi = float(row.get("dsi_vector_sum", 0.0))
    pd_rate = float(row.get("pd_rate_hz", 0.0))
    silence_failed = bool(row.get("silence_failed", False))
    return (
        dsi >= DSI_LEGIT_THRESHOLD and pd_rate >= PD_RATE_LEGIT_THRESHOLD_HZ and not silence_failed
    )


def _safe_float(value: Any) -> float | None:
    if isinstance(value, int | float) and (value == value) and value not in (float("inf"),):
        return float(value)
    return None


def build_metrics_for_seed(*, seed: int) -> list[dict[str, Any]]:
    trace_rows = _load_cell_trace_jsonl(seed=seed)
    eval_rows = _load_all_evaluations(seed=seed)
    sb_cells = _load_strong_bialek_top10()
    cells = trace_rows if len(trace_rows) > 0 else eval_rows
    n_cells = len(cells)
    legit_cells = [c for c in cells if _is_legit_diagnostic(row=c)]
    n_legit = len(legit_cells)

    def _best(rows: list[dict[str, Any]], key: str, *, reverse: bool) -> dict[str, Any] | None:
        candidates = [r for r in rows if isinstance(r.get(key), int | float) and (r[key] == r[key])]
        if len(candidates) == 0:
            return None
        candidates.sort(key=lambda r: float(r[key]), reverse=reverse)
        return candidates[0]

    best_legit_row = _best(legit_cells, "mi_count_bits", reverse=True)
    overall_max_mi_row = _best(cells, "mi_count_bits", reverse=True)
    overall_min_atp_row = _best(cells, "atp_per_spike_molecules", reverse=False)

    base_dims: dict[str, Any] = {
        "task_seed": int(seed),
        "init_method": "lhs_random",
        "n_obj": 2,
        "n_directions": 4,
        "dsi_metric": "vector_sum",
        "dsi_silence_guard_active": True,
        "silence_guard_threshold_pd_spikes": 3,
        "n_eval_seeds": 3,
        "n_generations_target": 60,
        "n_cells": int(n_cells),
        "n_legit": int(n_legit),
        "pool_restart_every": 10,
        "hv_plateau_auto_stop_disabled": True,
    }

    variants: list[dict[str, Any]] = []

    def _variant_from_row(
        *,
        row: dict[str, Any] | None,
        variant_id: str,
        label: str,
        dsi_subvariant: str,
    ) -> dict[str, Any]:
        metrics: dict[str, Any] = {
            "direction_selectivity_index": _safe_float(
                row.get("dsi_vector_sum") if row is not None else None,
            ),
            "mi_count_bits": _safe_float(
                row.get("mi_count_bits") if row is not None else None,
            ),
            "atp_per_spike_molecules": _safe_float(
                row.get("atp_per_spike_molecules") if row is not None else None,
            ),
        }
        return {
            "variant_id": variant_id,
            "label": label,
            "dimensions": {
                **base_dims,
                "dsi_subvariant": dsi_subvariant,
                "pd_rate_hz": _safe_float(row.get("pd_rate_hz") if row is not None else None),
            },
            "metrics": metrics,
        }

    variants.append(
        _variant_from_row(
            row=best_legit_row,
            variant_id=f"t0123-seed{seed}-best-legit",
            label=(f"t0123 NSGA-II seed {seed}: best LEGIT cell by mi_count_bits"),
            dsi_subvariant="best_legit",
        ),
    )
    variants.append(
        _variant_from_row(
            row=overall_max_mi_row,
            variant_id=f"t0123-seed{seed}-overall-max-mi",
            label=(f"t0123 NSGA-II seed {seed}: overall max mi_count_bits across all cells"),
            dsi_subvariant="overall_max_mi",
        ),
    )
    variants.append(
        _variant_from_row(
            row=overall_min_atp_row,
            variant_id=f"t0123-seed{seed}-overall-min-atp",
            label=(f"t0123 NSGA-II seed {seed}: overall min atp_per_spike_molecules"),
            dsi_subvariant="overall_min_atp",
        ),
    )

    # Top-10 Strong-Bialek variant: aggregate stats only (no per-cell DSI
    # because the post-hoc rerun does not recompute DSI).
    sb_bits = [_safe_float(c.get("bits_per_sec")) for c in sb_cells]
    sb_bits_clean = [x for x in sb_bits if x is not None]
    sb_metrics: dict[str, Any] = {
        "mi_strong_bialek_bits_per_sec": (
            float(max(sb_bits_clean)) if len(sb_bits_clean) > 0 else None
        ),
        "atp_per_spike_molecules": None,
        "niven_2007_above_below_count": None,
    }
    if len(sb_cells) > 0:
        atp_values = [_safe_float(c.get("atp_per_spike_molecules")) for c in sb_cells]
        atp_clean = [x for x in atp_values if x is not None]
        if len(atp_clean) > 0:
            sb_metrics["atp_per_spike_molecules"] = float(min(atp_clean))
    variants.append(
        {
            "variant_id": f"t0123-seed{seed}-top10-strong-bialek",
            "label": (
                f"t0123 NSGA-II seed {seed}: top-10 Pareto cells under "
                f"post-hoc Strong-Bialek 1998 direct method"
            ),
            "dimensions": {
                **base_dims,
                "dsi_subvariant": "top10_strong_bialek",
                "n_top_cells": len(sb_cells),
            },
            "metrics": sb_metrics,
        },
    )
    return variants


def build_metrics() -> dict[str, Any]:
    variants: list[dict[str, Any]] = []
    for seed in T0129_SEEDS:
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
