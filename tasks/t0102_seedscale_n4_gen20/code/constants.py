"""t0102 task-local constants — wraps the 68-d hyperparameter set from
``constants_morphology`` and adds the 2-seed schedule plus the per-seed cost cap.

Per t0102 plan REQ-3/REQ-6:

* ``T0102_SEEDS = (44, 55)`` — two RNG seeds for independent random-init runs.
* ``T0102_HARD_BUDGET_PER_SEED_USD`` — $4.00 per seed.
* ``T0102_TASK_BUDGET_TOTAL_USD`` — $8.00 task-local hard cap.

Inherits all 68-d bounds and NSGA-II hyperparameters from t0099's design via
``constants_morphology``, including the overridden ``N_EVAL_SEEDS = 4`` and
``N_GEN = 20``. No anchor warm-start; the NSGA-II driver uses pure LHS
initialisation via ``random_init.py``.
"""

from __future__ import annotations

from tasks.t0102_seedscale_n4_gen20.code.constants_morphology import (
    ANCHOR_NAMES,
    HV_PLATEAU_MIN_HV_HISTORY,
    HV_PLATEAU_REL_THRESHOLD,
    HV_PLATEAU_WINDOW,
    HV_UTOPIA_DSI,
    HV_UTOPIA_PD_RATE_HZ,
    HV_UTOPIA_ROBUSTNESS,
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

# t0102-specific run schedule.
T0102_SEEDS: tuple[int, ...] = (44, 55)
T0102_HARD_BUDGET_PER_SEED_USD: float = 4.00
T0102_TASK_BUDGET_TOTAL_USD: float = 8.00

assert len(T0102_SEEDS) == 2, f"expected 2 seeds, got {len(T0102_SEEDS)}"
assert T0102_HARD_BUDGET_PER_SEED_USD > 0
assert sum([T0102_HARD_BUDGET_PER_SEED_USD] * len(T0102_SEEDS)) <= T0102_TASK_BUDGET_TOTAL_USD

__all__ = [
    "ANCHOR_NAMES",
    "HV_PLATEAU_MIN_HV_HISTORY",
    "HV_PLATEAU_REL_THRESHOLD",
    "HV_PLATEAU_WINDOW",
    "HV_UTOPIA_DSI",
    "HV_UTOPIA_PD_RATE_HZ",
    "HV_UTOPIA_ROBUSTNESS",
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
    "T0102_HARD_BUDGET_PER_SEED_USD",
    "T0102_SEEDS",
    "T0102_TASK_BUDGET_TOTAL_USD",
    "UPPER_BOUNDS_68",
    "WORST_CASE_DSI",
    "WORST_CASE_PD_RATE_HZ",
    "WORST_CASE_ROBUSTNESS",
]
