"""t0129 task-local constants -- signed-DSI + real per-cell firing rates
reproduction of the t0126 NSGA-II protocol on one fresh seed (3517).

Behavioural deltas from t0126:

* Signed antipodal DSI replacing vector-sum DSI; field
  ``CellEvalResult.dsi_vector_sum -> dsi_signed`` (range [-1, 1]).
* Real per-cell firing rates ``pd_rate_hz`` and ``nd_rate_hz`` exposed
  as named scalar fields on ``CellEvalResult``.
* Per-cell parameter dump written to ``results/cell_params.jsonl``
  via a path captured at ``BedBV3MorphProblem.__init__`` (no env var).

Hard invariants preserved verbatim from t0126:

* ``POP_SIZE = 96``, ``N_EVAL_SEEDS = 3``, ``N_DIRECTIONS = 2``,
  ``N_GEN = 60``, ``_POOL_RESTART_EVERY = 10``,
  ``HV_PLATEAU_AUTO_STOP = False``, ``SILENCE_PD_SPIKES_THRESHOLD = 3``,
  ``WORST_CASE_DSI = -1.0``, ``TSTOP_MS = 1400``.
* ``OperatorStopTermination`` REMOVED from the live
  ``TerminationCollection`` in ``nsga2_driver.py``. Termination triggers:
  ``MaximumGenerationTermination(60)`` + ``CostWatchdogTermination``.

GA seed = 3517 (fresh; not in the lineage seed set
{441, 6650, 8929, 2608, 8276, 9986}).

The non-negotiable project policy constants ``_POOL_RESTART_EVERY = 10``
(memory: ``feedback_nsga2_pool_restart_every_10.md``) and
``HV_PLATEAU_AUTO_STOP = False`` (memory:
``feedback_disable_hv_plateau_autostop.md``) are surfaced here as named
module-level constants so the smoke gate and a downstream grep both pick
them up directly from ``constants.py``.

Back-compat aliases for t0104/t0106/t0114/t0115/t0122/t0124/t0126
budget symbol names are preserved so the forked ``cost_watchdog`` and
``nsga2_driver`` modules pick up the cap without further code changes.
"""

from __future__ import annotations

from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.constants_morphology import (
    ANCHOR_NAMES,
    HV_PLATEAU_MIN_HV_HISTORY,
    HV_PLATEAU_REL_THRESHOLD,
    HV_PLATEAU_WINDOW,
    HV_UTOPIA_ATP_PER_SPIKE,
    HV_UTOPIA_DSI,
    HV_UTOPIA_MI_BITS,
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
    WORST_CASE_ATP_PER_SPIKE,
    WORST_CASE_DSI,
    WORST_CASE_MI_BITS,
    WORST_CASE_PD_RATE_HZ,
    WORST_CASE_ROBUSTNESS,
)

# t0129-specific run schedule.
# Fresh GA seed: 3517. Lineage seeds excluded: {441, 6650, 8929, 2608,
# 8276, 9986}. Selection verified at plan-edit time 2026-05-26.
T0129_SEEDS: tuple[int, ...] = (3517,)
T0126_SEEDS: tuple[int, ...] = T0129_SEEDS  # back-compat alias

# Hard cost cap. t0129 widens to $8 (project per-task default) because
# the run is local-CPU only; the cap is purely defensive.
COST_CAP_USD: float = 8.0
T0129_HARD_BUDGET_USD: float = COST_CAP_USD
T0129_PER_INSTANCE_WATCHDOG_USD: float = 5.0

# Project policy constants surfaced for smoke-gate / grep visibility.
# The actual ``PerGenerationPoolRestart`` cadence and the
# ``TerminationCollection`` content live in ``nsga2_driver.py``.
_POOL_RESTART_EVERY: int = 10
HV_PLATEAU_AUTO_STOP: bool = False

# Task-description-mandated ceiling. Alias for ``constants_morphology.N_GEN``
# so grep on either name finds it.
N_GEN_MAX: int = N_GEN

# Backwards-compatible aliases for code paths that still reference the
# t0104 / t0106 / t0113 / t0114 / t0115 / t0122 symbol names (e.g.,
# ``nsga2_driver`` defaults, ``cost_watchdog`` constructors). The
# single-seed cost cap is the total task cap because there is only one
# seed.
T0104_SEEDS: tuple[int, ...] = T0129_SEEDS
T0104_HARD_BUDGET_PER_SEED_USD: float = T0129_HARD_BUDGET_USD
T0104_TASK_BUDGET_TOTAL_USD: float = T0129_HARD_BUDGET_USD
T0106_SEEDS: tuple[int, ...] = T0129_SEEDS
T0106_HARD_BUDGET_USD: float = T0129_HARD_BUDGET_USD
T0106_PER_INSTANCE_WATCHDOG_USD: float = T0129_PER_INSTANCE_WATCHDOG_USD
T0114_SEEDS: tuple[int, ...] = T0129_SEEDS
T0114_HARD_BUDGET_USD: float = T0129_HARD_BUDGET_USD
T0114_PER_INSTANCE_WATCHDOG_USD: float = T0129_PER_INSTANCE_WATCHDOG_USD
T0115_SEEDS: tuple[int, ...] = T0129_SEEDS
T0115_HARD_BUDGET_USD: float = T0129_HARD_BUDGET_USD
T0115_PER_INSTANCE_WATCHDOG_USD: float = T0129_PER_INSTANCE_WATCHDOG_USD
T0122_SEEDS: tuple[int, ...] = T0129_SEEDS
T0122_HARD_BUDGET_USD: float = T0129_HARD_BUDGET_USD
T0122_PER_INSTANCE_WATCHDOG_USD: float = T0129_PER_INSTANCE_WATCHDOG_USD

_T0129_LINEAGE_EXCLUDED: frozenset[int] = frozenset({441, 6650, 8929, 2608, 8276, 9986})

assert len(T0129_SEEDS) == 1, f"expected 1 seed, got {len(T0129_SEEDS)}"
assert T0129_SEEDS[0] == 3517, f"T0129_SEEDS[0] must be 3517, got {T0129_SEEDS[0]}"
assert T0129_SEEDS[0] not in _T0129_LINEAGE_EXCLUDED, (
    f"T0129_SEEDS[0]={T0129_SEEDS[0]} must not be in lineage {_T0129_LINEAGE_EXCLUDED}"
)
assert T0129_HARD_BUDGET_USD > 0
assert T0129_PER_INSTANCE_WATCHDOG_USD <= T0129_HARD_BUDGET_USD
assert _POOL_RESTART_EVERY == 10, "10-gen rule: _POOL_RESTART_EVERY must be 10"
assert HV_PLATEAU_AUTO_STOP is False, "auto-stop disabled per project policy"
assert N_GEN_MAX == 60, f"N_GEN_MAX must be 60, got {N_GEN_MAX}"
assert N_DIRECTIONS == 2, f"N_DIRECTIONS must be 2, got {N_DIRECTIONS}"
assert POP_SIZE == 96, f"POP_SIZE must be 96, got {POP_SIZE}"
assert N_EVAL_SEEDS == 3, f"N_EVAL_SEEDS must be 3, got {N_EVAL_SEEDS}"
assert COST_CAP_USD == 8.0, f"COST_CAP_USD must be 8.0, got {COST_CAP_USD}"

__all__ = [
    "ANCHOR_NAMES",
    "COST_CAP_USD",
    "HV_PLATEAU_AUTO_STOP",
    "HV_PLATEAU_MIN_HV_HISTORY",
    "HV_PLATEAU_REL_THRESHOLD",
    "HV_PLATEAU_WINDOW",
    "HV_UTOPIA_ATP_PER_SPIKE",
    "HV_UTOPIA_DSI",
    "HV_UTOPIA_MI_BITS",
    "HV_UTOPIA_PD_RATE_HZ",
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
    "T0126_SEEDS",
    "T0129_HARD_BUDGET_USD",
    "T0129_PER_INSTANCE_WATCHDOG_USD",
    "T0129_SEEDS",
    "UPPER_BOUNDS_68",
    "WORST_CASE_ATP_PER_SPIKE",
    "WORST_CASE_DSI",
    "WORST_CASE_MI_BITS",
    "WORST_CASE_PD_RATE_HZ",
    "WORST_CASE_ROBUSTNESS",
    "_POOL_RESTART_EVERY",
]
