"""t0104 task-local constants — wraps the 68-d hyperparameter set from
``constants_morphology`` and adds the 3-seed schedule plus the per-seed cost
cap.

Per t0104 plan REQ-6/REQ-9/REQ-11:

* ``T0104_SEEDS = (44, 55, 66)`` — three RNG seeds for independent
  random-init runs (44/55 inherited from t0102 for direct comparison; 66 is
  fresh).
* ``T0104_HARD_BUDGET_PER_SEED_USD`` — $4.00 per seed (inherits t0102's
  watchdog cap).
* ``T0104_TASK_BUDGET_TOTAL_USD`` — $12.00 task-local budget (3 x $4 + small
  idle margin under the $15 orchestrator cap).

``HV_UTOPIA_ROBUSTNESS`` is intentionally NOT re-exported here (REQ-6): the
robustness axis is dropped from NSGA-II selection in t0104, so any downstream
accidental reference to the robustness HV utopia fails fast at import time.
``WORST_CASE_ROBUSTNESS`` remains exported because
``CellEvalResult.robustness`` is still populated for predictions assets.

Inherits all 68-d bounds and NSGA-II hyperparameters from t0099's design via
``constants_morphology``, including the overridden ``N_EVAL_SEEDS = 4`` and
``N_GEN = 20``. No anchor warm-start; the NSGA-II driver uses pure LHS
initialisation via ``random_init.py``.
"""

from __future__ import annotations

from tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.constants_morphology import (
    ANCHOR_NAMES,
    HV_PLATEAU_MIN_HV_HISTORY,
    HV_PLATEAU_REL_THRESHOLD,
    HV_PLATEAU_WINDOW,
    HV_UTOPIA_DSI,
    HV_UTOPIA_PD_RATE_HZ,
    INT_PARAM_INDICES_68,
    LOWER_BOUNDS_68,
    MORPHOLOGY_LOWER_BOUNDS,
    MORPHOLOGY_UPPER_BOUNDS,
    N_ANCHORS,
    N_DIRECTIONS,
    N_EVAL_SEEDS,
    N_GEN,
    N_MORPH_PARAMS,
    N_PARAMS_54,
    N_PARAMS_68,
    PM_ETA,
    PM_PROB,
    POP_SIZE,
    REF_POINT_HV,
    SBX_ETA,
    SBX_PROB,
    UPPER_BOUNDS_68,
    WORST_CASE_DSI,
    WORST_CASE_PD_RATE_HZ,
    WORST_CASE_ROBUSTNESS,
)

# t0104-specific run schedule.
T0104_SEEDS: tuple[int, ...] = (44, 55, 66)
T0104_HARD_BUDGET_PER_SEED_USD: float = 4.00
T0104_TASK_BUDGET_TOTAL_USD: float = 12.00

assert len(T0104_SEEDS) == 3, f"expected 3 seeds, got {len(T0104_SEEDS)}"
assert T0104_HARD_BUDGET_PER_SEED_USD > 0
assert sum([T0104_HARD_BUDGET_PER_SEED_USD] * len(T0104_SEEDS)) <= T0104_TASK_BUDGET_TOTAL_USD

__all__ = [
    "ANCHOR_NAMES",
    "HV_PLATEAU_MIN_HV_HISTORY",
    "HV_PLATEAU_REL_THRESHOLD",
    "HV_PLATEAU_WINDOW",
    "HV_UTOPIA_DSI",
    "HV_UTOPIA_PD_RATE_HZ",
    "INT_PARAM_INDICES_68",
    "LOWER_BOUNDS_68",
    "MORPHOLOGY_LOWER_BOUNDS",
    "MORPHOLOGY_UPPER_BOUNDS",
    "N_ANCHORS",
    "N_DIRECTIONS",
    "N_EVAL_SEEDS",
    "N_GEN",
    "N_MORPH_PARAMS",
    "N_PARAMS_54",
    "N_PARAMS_68",
    "PM_ETA",
    "PM_PROB",
    "POP_SIZE",
    "REF_POINT_HV",
    "SBX_ETA",
    "SBX_PROB",
    "T0104_HARD_BUDGET_PER_SEED_USD",
    "T0104_SEEDS",
    "T0104_TASK_BUDGET_TOTAL_USD",
    "UPPER_BOUNDS_68",
    "WORST_CASE_DSI",
    "WORST_CASE_PD_RATE_HZ",
    "WORST_CASE_ROBUSTNESS",
]
