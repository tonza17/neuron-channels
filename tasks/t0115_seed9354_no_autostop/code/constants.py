"""t0115 task-local constants — wraps the 68-d hyperparameter set from
``constants_morphology`` and replaces the t0114 single-seed schedule with a
new GA seed (9354, drawn via ``secrets.randbelow(10000)``) while keeping the
$25 total cost cap.

Per t0115 plan REQ-2/REQ-3/REQ-6:

* ``T0115_SEEDS = (9354,)`` — single RNG seed (9354; random replicate of
  t0106 seed 44, t0112 seed 77, t0113 seed 2247, and t0114 seed 7755 to test
  substrate vs seed-specific joint-pass yield with HV-plateau auto-stop
  disabled).
* ``T0115_HARD_BUDGET_USD`` — $25.00 total task cost cap (value unchanged
  from t0114).
* ``T0115_PER_INSTANCE_WATCHDOG_USD`` — $20.00 per-instance watchdog cap
  (value unchanged from t0114; consumed by ``CostWatchdogTermination`` via
  ``make_watchdog_from_machine_log``).

``HV_UTOPIA_ROBUSTNESS`` is intentionally NOT re-exported here (inherited from
t0104): the robustness axis is dropped from NSGA-II selection in this lineage,
so any downstream accidental reference to the robustness HV utopia fails fast
at import time. ``WORST_CASE_ROBUSTNESS`` remains exported because
``CellEvalResult.robustness`` is still populated for predictions assets.

Inherits all 68-d bounds and NSGA-II hyperparameters from t0099's design via
``constants_morphology``, including the overridden ``N_EVAL_SEEDS = 3``,
``N_DIRECTIONS = 2``, and ``N_GEN = 300`` (t0114/t0115: matches t0106's
original ceiling; HV-plateau auto-stop disabled; budget cap and operator stop
are binding). No anchor warm-start; the NSGA-II driver uses pure LHS
initialisation via ``random_init.py``.
"""

from __future__ import annotations

from tasks.t0115_seed9354_no_autostop.code.constants_morphology import (
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

# t0115-specific run schedule.
T0115_SEEDS: tuple[int, ...] = (9354,)
T0115_HARD_BUDGET_USD: float = 25.00
T0115_PER_INSTANCE_WATCHDOG_USD: float = 20.00

# Backwards-compatible aliases for code paths that still reference the t0104
# / t0106 / t0113 / t0114 names (e.g., ``nsga2_driver`` defaults). The
# single-seed cost cap is the total task cap because there is only one seed.
T0104_SEEDS: tuple[int, ...] = T0115_SEEDS
T0104_HARD_BUDGET_PER_SEED_USD: float = T0115_HARD_BUDGET_USD
T0104_TASK_BUDGET_TOTAL_USD: float = T0115_HARD_BUDGET_USD
T0106_SEEDS: tuple[int, ...] = T0115_SEEDS
T0106_HARD_BUDGET_USD: float = T0115_HARD_BUDGET_USD
T0106_PER_INSTANCE_WATCHDOG_USD: float = T0115_PER_INSTANCE_WATCHDOG_USD
T0114_SEEDS: tuple[int, ...] = T0115_SEEDS
T0114_HARD_BUDGET_USD: float = T0115_HARD_BUDGET_USD
T0114_PER_INSTANCE_WATCHDOG_USD: float = T0115_PER_INSTANCE_WATCHDOG_USD

assert len(T0115_SEEDS) == 1, f"expected 1 seed, got {len(T0115_SEEDS)}"
assert T0115_HARD_BUDGET_USD > 0
assert T0115_PER_INSTANCE_WATCHDOG_USD <= T0115_HARD_BUDGET_USD

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
    "T0114_HARD_BUDGET_USD",
    "T0114_PER_INSTANCE_WATCHDOG_USD",
    "T0114_SEEDS",
    "T0115_HARD_BUDGET_USD",
    "T0115_PER_INSTANCE_WATCHDOG_USD",
    "T0115_SEEDS",
    "UPPER_BOUNDS_68",
    "WORST_CASE_DSI",
    "WORST_CASE_PD_RATE_HZ",
    "WORST_CASE_ROBUSTNESS",
]
