"""t0122 task-local constants -- forks the t0115 single-seed 68-d NSGA-II
substrate with three deltas:

* New GA seed drawn via ``secrets.randbelow(10000)`` (avoiding round-ish
  numbers per the t0113/t0115 convention). Drawn ONCE at edit time.
* ``COST_CAP_USD = 6.0`` (REDUCED from t0115's $25 because the user's
  Vast.ai account balance is $7; $1 teardown buffer required).
  ``T0122_PER_INSTANCE_WATCHDOG_USD = 5.0`` (leaves $1 below the task cap).
* ``N_GEN_MAX = 60`` (alias re-export of ``constants_morphology.N_GEN``
  which is set to 60 in this task -- down from t0115's 300 -- per the
  task-description ``N_GEN_MAX = 60`` constraint and the project's
  auto-stop-disabled convention).

The non-negotiable project policy constants ``_POOL_RESTART_EVERY = 10``
(memory: ``feedback_nsga2_pool_restart_every_10.md``) and
``HV_PLATEAU_AUTO_STOP = False`` (memory:
``feedback_disable_hv_plateau_autostop.md``) are surfaced here as named
module-level constants so the smoke gate and a downstream grep both pick
them up directly from ``constants.py``. The ``HVPlateauTermination`` is
also NOT included in the live ``TerminationCollection`` in
``nsga2_driver.py``.

Back-compat aliases for t0104/t0106/t0114/t0115 budget symbol names are
preserved so the forked ``cost_watchdog`` and ``nsga2_driver`` modules
pick up the $6 task cap without further code changes.
"""

from __future__ import annotations

from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.constants_morphology import (
    ANCHOR_NAMES,
    HV_PLATEAU_MIN_HV_HISTORY,
    HV_PLATEAU_REL_THRESHOLD,
    HV_PLATEAU_WINDOW,
    HV_UTOPIA_DSI,
    HV_UTOPIA_PD_RATE_HZ,
    HV_UTOPIA_VOLUME_UM3,
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
    V_MAX_UM3,
    WORST_CASE_CYTOPLASM_VOLUME_UM3,
    WORST_CASE_DSI,
    WORST_CASE_PD_RATE_HZ,
    WORST_CASE_ROBUSTNESS,
)

# t0122-specific run schedule.
# GA seed drawn via ``secrets.randbelow(10000)`` (avoided round-ish
# numbers per the t0113/t0115 convention; drawn 2026-05-24).
T0122_SEEDS: tuple[int, ...] = (1524,)

# Hard cost cap per task_description.md ``Hard Constraints`` section.
# REDUCED from t0115's $25 because the Vast.ai account balance is $7
# ($1 buffer for teardown / unexpected costs).
COST_CAP_USD: float = 6.0
T0122_HARD_BUDGET_USD: float = COST_CAP_USD
T0122_PER_INSTANCE_WATCHDOG_USD: float = 5.0

# Project policy constants surfaced for smoke-gate / grep visibility.
# The actual ``PerGenerationPoolRestart`` cadence and the
# ``TerminationCollection`` content live in ``nsga2_driver.py``.
_POOL_RESTART_EVERY: int = 10
HV_PLATEAU_AUTO_STOP: bool = False

# Task-description-mandated ceiling. Alias for ``constants_morphology.N_GEN``
# so grep on either name finds it.
N_GEN_MAX: int = N_GEN

# Backwards-compatible aliases for code paths that still reference the
# t0104 / t0106 / t0113 / t0114 / t0115 symbol names (e.g.,
# ``nsga2_driver`` defaults, ``cost_watchdog`` constructors). The
# single-seed cost cap is the total task cap because there is only one
# seed.
T0104_SEEDS: tuple[int, ...] = T0122_SEEDS
T0104_HARD_BUDGET_PER_SEED_USD: float = T0122_HARD_BUDGET_USD
T0104_TASK_BUDGET_TOTAL_USD: float = T0122_HARD_BUDGET_USD
T0106_SEEDS: tuple[int, ...] = T0122_SEEDS
T0106_HARD_BUDGET_USD: float = T0122_HARD_BUDGET_USD
T0106_PER_INSTANCE_WATCHDOG_USD: float = T0122_PER_INSTANCE_WATCHDOG_USD
T0114_SEEDS: tuple[int, ...] = T0122_SEEDS
T0114_HARD_BUDGET_USD: float = T0122_HARD_BUDGET_USD
T0114_PER_INSTANCE_WATCHDOG_USD: float = T0122_PER_INSTANCE_WATCHDOG_USD
T0115_SEEDS: tuple[int, ...] = T0122_SEEDS
T0115_HARD_BUDGET_USD: float = T0122_HARD_BUDGET_USD
T0115_PER_INSTANCE_WATCHDOG_USD: float = T0122_PER_INSTANCE_WATCHDOG_USD

assert len(T0122_SEEDS) == 1, f"expected 1 seed, got {len(T0122_SEEDS)}"
assert T0122_HARD_BUDGET_USD > 0
assert T0122_PER_INSTANCE_WATCHDOG_USD <= T0122_HARD_BUDGET_USD
assert _POOL_RESTART_EVERY == 10, "10-gen rule: _POOL_RESTART_EVERY must be 10"
assert HV_PLATEAU_AUTO_STOP is False, "auto-stop disabled per project policy"
assert N_GEN_MAX == 60, f"N_GEN_MAX must be 60, got {N_GEN_MAX}"

__all__ = [
    "ANCHOR_NAMES",
    "COST_CAP_USD",
    "HV_PLATEAU_AUTO_STOP",
    "HV_PLATEAU_MIN_HV_HISTORY",
    "HV_PLATEAU_REL_THRESHOLD",
    "HV_PLATEAU_WINDOW",
    "HV_UTOPIA_DSI",
    "HV_UTOPIA_PD_RATE_HZ",
    "HV_UTOPIA_VOLUME_UM3",
    "INT_PARAM_INDICES_68",
    "LOWER_BOUNDS_68",
    "MORPHOLOGY_LOWER_BOUNDS",
    "MORPHOLOGY_UPPER_BOUNDS",
    "N_ANCHORS",
    "N_DIRECTIONS",
    "N_EVAL_SEEDS",
    "N_GEN",
    "N_GEN_MAX",
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
    "T0122_HARD_BUDGET_USD",
    "T0122_PER_INSTANCE_WATCHDOG_USD",
    "T0122_SEEDS",
    "UPPER_BOUNDS_68",
    "V_MAX_UM3",
    "WORST_CASE_CYTOPLASM_VOLUME_UM3",
    "WORST_CASE_DSI",
    "WORST_CASE_PD_RATE_HZ",
    "WORST_CASE_ROBUSTNESS",
    "_POOL_RESTART_EVERY",
]
