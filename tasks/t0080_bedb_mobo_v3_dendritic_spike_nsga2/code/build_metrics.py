"""Build ``results/metrics.json`` in the explicit multi-variant format.

Reads the Pareto front and writes one variant per Pareto cell plus a
``pareto_best_joint`` variant pointing at the cell closest to the bio-grounded
target (DSI=0.4, PD-rate=10 Hz).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.paths import (
    PARETO_FRONT_JSON,
    RESULTS_DIR,
)

T0080_PASS_DSI: float = 0.4
T0080_PASS_PD_HZ: float = 10.0


def _build_variant(*, cell: dict[str, Any], variant_id: str, label: str) -> dict[str, Any]:
    return {
        "variant_id": variant_id,
        "label": label,
        "dimensions": {
            "cell_index": cell.get("cell_index"),
            "generation": cell.get("generation"),
            "is_feasible": cell.get("is_feasible"),
            "is_unstable": cell.get("is_unstable"),
        },
        "metrics": {
            "direction_selectivity_index": cell.get("dsi"),
            "pd_firing_rate_hz": cell.get("pd_rate_hz"),
            "peak_vm_mv": cell.get("peak_vm_mv"),
            "tuning_curve_hwhm_deg": None,
            "tuning_curve_reliability": None,
            "tuning_curve_rmse": None,
        },
    }


def main() -> int:
    if not PARETO_FRONT_JSON.exists():
        print(f"[metrics] missing {PARETO_FRONT_JSON}; nothing to build")
        return 1
    data = json.loads(PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    cells: list[dict[str, Any]] = data.get("cells", [])
    if len(cells) == 0:
        print("[metrics] empty pareto front; writing minimal metrics.json")
    target = np.array([T0080_PASS_DSI, T0080_PASS_PD_HZ], dtype=np.float64)
    closest_cell: dict[str, Any] | None = None
    closest_dist: float = float("inf")
    variants: list[dict[str, Any]] = []
    for c in cells:
        ci = c.get("cell_index", 0)
        v = _build_variant(
            cell=c,
            variant_id=f"pareto_cell_{ci:04d}",
            label=f"Pareto cell {ci} (gen {c.get('generation')})",
        )
        variants.append(v)
        dist = float(np.linalg.norm(np.array([c["dsi"], c["pd_rate_hz"]]) - target))
        if dist < closest_dist:
            closest_dist = dist
            closest_cell = c
    if closest_cell is not None:
        variants.append(
            _build_variant(
                cell=closest_cell,
                variant_id="pareto_best_joint",
                label=(
                    f"Closest to joint target (DSI={T0080_PASS_DSI}, "
                    f"PD={T0080_PASS_PD_HZ}Hz); distance={closest_dist:.3f}"
                ),
            )
        )
    payload = {
        "spec_version": "2",
        "task_id": "t0080_bedb_mobo_v3_dendritic_spike_nsga2",
        "format": "explicit",
        "n_total_cells": data.get("n_total", 0),
        "n_pareto_cells": len(cells),
        "joint_target": {"dsi": T0080_PASS_DSI, "pd_rate_hz": T0080_PASS_PD_HZ},
        "variants": variants,
    }
    out_path: Path = RESULTS_DIR / "metrics.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[metrics] wrote {out_path} with {len(variants)} variants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
