"""Build metrics.json for t0081 from pareto_front.json + all_evaluations.json.

Only registers project metric keys (direction_selectivity_index +
tuning_curve_hwhm_deg + tuning_curve_reliability + tuning_curve_rmse).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from tasks.t0081_bedb_v3_warmstart_nsga2.code import paths

ALLOWED_METRIC_KEYS: set[str] = {
    "direction_selectivity_index",
    "tuning_curve_hwhm_deg",
    "tuning_curve_reliability",
    "tuning_curve_rmse",
}


def main() -> None:
    paths.ensure_directories()
    pareto_raw = json.loads(paths.PARETO_FRONT_JSON.read_text())
    pareto_cells = pareto_raw.get("cells", pareto_raw)
    all_raw = json.loads(paths.ALL_EVALUATIONS_JSON.read_text())
    all_cells = all_raw.get("evaluations", all_raw) if isinstance(all_raw, dict) else all_raw

    def joint_distance(c: dict) -> float:
        dsi = c.get("dsi", 0.0)
        pd = c.get("pd_rate_hz", 0.0)
        return math.sqrt(max(0, 0.4 - dsi) ** 2 + max(0, 10.0 - pd) ** 2)

    feasible = [c for c in all_cells if c.get("is_feasible") and not c.get("is_unstable")]
    feasible.sort(key=joint_distance)
    closest = feasible[0] if feasible else pareto_cells[0]

    variants: list[dict] = []
    for c in pareto_cells:
        cidx = c["cell_index"]
        gen = c["generation"]
        joint_pass = bool(c["dsi"] >= 0.4 and c["pd_rate_hz"] >= 10.0)
        variants.append(
            {
                "variant_id": f"pareto_cell_{cidx:04d}",
                "label": f"Pareto cell {cidx} (gen {gen}){' [JOINT PASS]' if joint_pass else ''}",
                "dimensions": {
                    "cell_index": cidx,
                    "generation": gen,
                    "is_feasible": True,
                    "is_unstable": False,
                    "joint_pass": joint_pass,
                },
                "metrics": {
                    "direction_selectivity_index": c["dsi"],
                    "tuning_curve_hwhm_deg": None,
                    "tuning_curve_reliability": None,
                    "tuning_curve_rmse": None,
                },
            },
        )

    if closest["cell_index"] not in {c["cell_index"] for c in pareto_cells}:
        cidx = closest["cell_index"]
        gen = closest["generation"]
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
                },
                "metrics": {
                    "direction_selectivity_index": closest["dsi"],
                    "tuning_curve_hwhm_deg": None,
                    "tuning_curve_reliability": None,
                    "tuning_curve_rmse": None,
                },
            },
        )

    out: dict = {"variants": variants}
    out_path: Path = paths.RESULTS_DIR / "metrics.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"[metrics] wrote {out_path} with {len(variants)} variants")
    n_pass = sum(1 for v in variants if v["dimensions"].get("joint_pass"))
    print(f"[metrics] joint-pass variants: {n_pass}")


if __name__ == "__main__":
    main()
