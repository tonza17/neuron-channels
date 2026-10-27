"""Step 12: decide from pre-declared triggers whether the dendritic-scaling arm must be run."""

import json
from typing import Any

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    TRIGGER_B_MIN_COLLAPSED_CELLS,
    ScalingArm,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    ARM_DECISION_JSON,
    CC_COLLAPSE_VERDICT_JSON,
    CHOSEN_BIAS_JSON,
    FITTED_SCALINGS_JSON,
)


def main() -> None:
    arm = str(ScalingArm.SOMA_AIS)
    fits: dict[str, Any] = json.loads(FITTED_SCALINGS_JSON.read_text(encoding="utf-8"))
    cc: dict[str, Any] = json.loads(CC_COLLAPSE_VERDICT_JSON.read_text(encoding="utf-8"))
    bias: dict[str, Any] = json.loads(CHOSEN_BIAS_JSON.read_text(encoding="utf-8"))
    failed_cells = [cid for cid, v in fits["cells"].items() if v["failed_sustained_reach"]]
    trig_a = bool(fits["any_failed_sustained_reach"])
    trig_b = int(cc["n_collapsed"]) < TRIGGER_B_MIN_COLLAPSED_CELLS
    trig_c = not bool(bias["trigger_c_satisfied"])
    out: dict[str, Any] = {
        "base_arm": arm,
        "trigger_a_part1_sustained_reach_failed": {
            "fired": trig_a,
            "rule": "max grid sustained ratio below 1.55 for any cell",
            "failed_cells": failed_cells,
            "max_grid_sustained_ratio_per_cell": {
                cid: v["max_grid_sustained_ratio"] for cid, v in fits["cells"].items()
            },
            "n_cells_within_tolerance_of_1.7": fits["n_cells_within_tolerance"],
        },
        "trigger_b_evoked_firing_not_collapsed": {
            "fired": trig_b,
            "rule": "base arm collapses +60 pA firing on fewer than 6 of 8 cells",
            "n_collapsed": cc["n_collapsed"],
            "n_uninformative": cc["n_uninformative"],
            "n_cells": cc["n_cells"],
        },
        "trigger_c_bias_phenotype_not_met": {
            "fired": trig_c,
            "rule": "rd1-like 4-10 Hz with ISI CV above 0.5 while WT-like stays below 1 Hz",
            "selection": bias["selection"],
            "applied_all_cells": bias["applied_all_cells"],
        },
        "triggered": bool(trig_a or trig_b or trig_c),
    }
    ARM_DECISION_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
