"""t0099 task-local constants — wraps the 68-d hyperparameter set from
``constants_morphology`` (mirror of t0091's ``constants_t91``) and adds the
3-seed schedule plus the per-seed cost cap.

Inherits the 68-d bounds and NSGA-II hyperparameters from t0091's design but
overrides:

* ``T0099_HARD_BUDGET_PER_SEED_USD`` — $1.00 per seed (was $4.00 in t0091).
* ``T0099_SEEDS`` — three RNG seeds for independent random-init runs.
* No anchor warm-start; the NSGA-II driver is parameterised by a sampling
  matrix produced by ``random_init.py`` instead.
"""

from __future__ import annotations

from tasks.t0099_random_init_pareto_robustness.code.constants_morphology import (
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

# t0099-specific run schedule.
T0099_SEEDS: tuple[int, ...] = (11, 22, 33)
T0099_HARD_BUDGET_PER_SEED_USD: float = 1.00
T0099_TASK_BUDGET_TOTAL_USD: float = 3.15

assert len(T0099_SEEDS) == 3, f"expected 3 seeds, got {len(T0099_SEEDS)}"
assert T0099_HARD_BUDGET_PER_SEED_USD > 0
assert sum([T0099_HARD_BUDGET_PER_SEED_USD] * len(T0099_SEEDS)) <= T0099_TASK_BUDGET_TOTAL_USD

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
    "T0099_HARD_BUDGET_PER_SEED_USD",
    "T0099_SEEDS",
    "T0099_TASK_BUDGET_TOTAL_USD",
    "UPPER_BOUNDS_68",
    "WORST_CASE_DSI",
    "WORST_CASE_PD_RATE_HZ",
    "WORST_CASE_ROBUSTNESS",
]
