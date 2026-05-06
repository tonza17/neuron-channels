"""Build metrics.json for t0083 from pareto_front.json + all_evaluations.json.

Only registers project metric keys (direction_selectivity_index +
tuning_curve_hwhm_deg + tuning_curve_reliability + tuning_curve_rmse). Tags
each Pareto cell with the ``joint_pass`` dimension when DSI >= 0.4 AND
PD >= 10 Hz. Adds one extra closest-to-joint variant if the closest-to-joint
cell is not already on the Pareto front.
"""

from __future__ import annotations

import json
import math
from typing import Any

from tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code import paths

ALLOWED_METRIC_KEYS: set[str] = {
    "direction_selectivity_index",
    "tuning_curve_hwhm_deg",
    "tuning_curve_reliability",
    "tuning_curve_rmse",
}


def _joint_distance(*, dsi: float, pd: float) -> float:
    return math.sqrt(max(0.0, 0.4 - dsi) ** 2 + max(0.0, 10.0 - pd) ** 2)


def _build_per_generation_summary(
    *,
    all_cells: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compact per-generation summary: feasible cell counts + joint-pass count."""
    by_gen: dict[int, list[dict[str, Any]]] = {}
    for c in all_cells:
        by_gen.setdefault(int(c["generation"]), []).append(c)
    out: list[dict[str, Any]] = []
    for gen in sorted(by_gen):
        records = by_gen[gen]
        feasible = [r for r in records if r.get("is_feasible") and not r.get("is_unstable")]
        joint = [r for r in feasible if float(r["dsi"]) >= 0.4 and float(r["pd_rate_hz"]) >= 10.0]
        out.append(
            {
                "generation": gen,
                "n_total": len(records),
                "n_feasible": len(feasible),
                "n_joint_pass": len(joint),
            },
        )
    return {"per_generation": out}


def main() -> None:
    paths.ensure_directories()
    pareto_raw = json.loads(paths.PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    pareto_cells = pareto_raw.get("cells", pareto_raw)
    all_raw = json.loads(paths.ALL_EVALUATIONS_JSON.read_text(encoding="utf-8"))
    all_cells = all_raw.get("evaluations", all_raw) if isinstance(all_raw, dict) else all_raw

    feasible = [c for c in all_cells if c.get("is_feasible") and not c.get("is_unstable")]
    feasible.sort(key=lambda c: _joint_distance(dsi=float(c["dsi"]), pd=float(c["pd_rate_hz"])))
    closest = feasible[0] if len(feasible) > 0 else pareto_cells[0]

    variants: list[dict[str, Any]] = []
    for c in pareto_cells:
        cidx: int = int(c["cell_index"])
        gen: int = int(c["generation"])
        joint_pass: bool = bool(float(c["dsi"]) >= 0.4 and float(c["pd_rate_hz"]) >= 10.0)
        variants.append(
            {
                "variant_id": f"pareto_cell_{cidx:04d}",
                "label": (
                    f"Pareto cell {cidx} (gen {gen})" + (" [JOINT PASS]" if joint_pass else "")
                ),
                "dimensions": {
                    "cell_index": cidx,
                    "generation": gen,
                    "is_feasible": True,
                    "is_unstable": False,
                    "joint_pass": joint_pass,
                    "pd_rate_hz": float(c["pd_rate_hz"]),
                },
                "metrics": {
                    "direction_selectivity_index": float(c["dsi"]),
                    "tuning_curve_hwhm_deg": None,
                    "tuning_curve_reliability": None,
                    "tuning_curve_rmse": None,
                },
            },
        )

    pareto_indices: set[int] = {int(c["cell_index"]) for c in pareto_cells}
    if int(closest["cell_index"]) not in pareto_indices:
        cidx = int(closest["cell_index"])
        gen = int(closest["generation"])
        variants.append(
            {
                "variant_id": f"closest_to_joint_cell_{cidx:04d}",
                "label": f"Closest-to-joint cell {cidx} (gen {gen})",
                "dimensions": {
                    "cell_index": cidx,
                    "generation": gen,
                    "is_feasible": True,
                    "is_unstable": False,
                    "joint_pass": False,
                    "pd_rate_hz": float(closest["pd_rate_hz"]),
                },
                "metrics": {
                    "direction_selectivity_index": float(closest["dsi"]),
                    "tuning_curve_hwhm_deg": None,
                    "tuning_curve_reliability": None,
                    "tuning_curve_rmse": None,
                },
            },
        )

    summary = _build_per_generation_summary(all_cells=all_cells)
    out: dict[str, Any] = {
        "variants": variants,
        "per_generation_summary": summary["per_generation"],
        "n_total_evaluations": len(all_cells),
        "n_pareto_cells": len(pareto_cells),
    }
    out_path = paths.RESULTS_DIR / "metrics.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    n_pass = sum(1 for v in variants if v["dimensions"].get("joint_pass"))
    print(f"[metrics] wrote {out_path} with {len(variants)} variants")
    print(f"[metrics] joint-pass variants: {n_pass}")


if __name__ == "__main__":
    main()
