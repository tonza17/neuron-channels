"""t0112 task-local constants — wraps the 68-d hyperparameter set from
``constants_morphology`` and replaces the t0106 single-seed schedule with a
new GA seed plus the new $25 total cost cap.

Per t0112 plan REQ-2/REQ-8:

* ``T0112_SEEDS = (77,)`` — single RNG seed (77; replicate of t0106 seed 44
  to test substrate vs seed-specific joint-pass yield).
* ``T0112_HARD_BUDGET_USD`` — $25.00 total task cost cap.
* ``T0112_PER_INSTANCE_WATCHDOG_USD`` — $20.00 per-instance watchdog cap
  (consumed by ``CostWatchdogTermination`` via ``make_watchdog_from_machine_log``).

``HV_UTOPIA_ROBUSTNESS`` is intentionally NOT re-exported here (inherited from
t0104): the robustness axis is dropped from NSGA-II selection in this lineage,
so any downstream accidental reference to the robustness HV utopia fails fast
at import time. ``WORST_CASE_ROBUSTNESS`` remains exported because
``CellEvalResult.robustness`` is still populated for predictions assets.

Inherits all 68-d bounds and NSGA-II hyperparameters from t0099's design via
``constants_morphology``, including the overridden ``N_EVAL_SEEDS = 3``,
``N_DIRECTIONS = 2``, and ``N_GEN = 60`` (t0112 ceiling; HV-plateau primary).
No anchor warm-start; the NSGA-II driver uses pure LHS initialisation via
``random_init.py``.
"""

from __future__ import annotations

from tasks.t0112_t0106_seed77_replicate.code.constants_morphology import (
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

# t0112-specific run schedule.
T0112_SEEDS: tuple[int, ...] = (77,)
T0112_HARD_BUDGET_USD: float = 25.00
T0112_PER_INSTANCE_WATCHDOG_USD: float = 20.00

# Backwards-compatible aliases for code paths that still reference the t0104
# / t0106 names (e.g., ``nsga2_driver`` defaults). The single-seed cost cap
# is the total task cap because there is only one seed.
T0104_SEEDS: tuple[int, ...] = T0112_SEEDS
T0104_HARD_BUDGET_PER_SEED_USD: float = T0112_HARD_BUDGET_USD
T0104_TASK_BUDGET_TOTAL_USD: float = T0112_HARD_BUDGET_USD
T0106_SEEDS: tuple[int, ...] = T0112_SEEDS
T0106_HARD_BUDGET_USD: float = T0112_HARD_BUDGET_USD
T0106_PER_INSTANCE_WATCHDOG_USD: float = T0112_PER_INSTANCE_WATCHDOG_USD

assert len(T0112_SEEDS) == 1, f"expected 1 seed, got {len(T0112_SEEDS)}"
assert T0112_HARD_BUDGET_USD > 0
assert T0112_PER_INSTANCE_WATCHDOG_USD <= T0112_HARD_BUDGET_USD

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
    "T0106_HARD_BUDGET_USD",
    "T0106_PER_INSTANCE_WATCHDOG_USD",
    "T0106_SEEDS",
    "T0112_HARD_BUDGET_USD",
    "T0112_PER_INSTANCE_WATCHDOG_USD",
    "T0112_SEEDS",
    "UPPER_BOUNDS_68",
    "WORST_CASE_DSI",
    "WORST_CASE_PD_RATE_HZ",
    "WORST_CASE_ROBUSTNESS",
]
