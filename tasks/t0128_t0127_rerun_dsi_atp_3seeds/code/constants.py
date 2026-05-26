"""t0128 task-local constants -- 60-generation completion mandate replication
of t0124's 68-d Bed B + 14-d morphology NSGA-II substrate (DSI maximised,
ATP-per-spike minimised). Two behavioural deltas from t0124:

* Fresh GA seed drawn via ``secrets.randbelow(10000)`` (rejecting multiples
  of 100/500/1000, values below 100, prior-lineage seeds
  {77, 441, 1524, 2247, 7755, 9354}, AND t0124's seed 6650). Drawn ONCE at
  plan-edit time. ``T0128_SEEDS = (2608, 8276, 9986)`` -- explicitly distinct from
  t0124's 6650 to break the single-LHS-ancestry confound.
* 60-generation completion mandate. ``OperatorStopTermination`` is REMOVED
  from the live ``TerminationCollection`` in ``nsga2_driver.py``. The only
  legitimate termination triggers are ``MaximumGenerationTermination`` at
  gen 60 and ``CostWatchdogTermination`` at $5 per-instance / $6 task.

All other constants (POP_SIZE=96, N_EVAL_SEEDS=3, N_DIRECTIONS=2,
COST_CAP_USD=6.0, _POOL_RESTART_EVERY=10, HV_PLATEAU_AUTO_STOP=False,
SILENCE_PD_SPIKES_THRESHOLD=3, WORST_CASE_DSI=-1.0) are inherited verbatim
from t0124. The non-negotiable project policy constants
``_POOL_RESTART_EVERY = 10`` (memory: ``feedback_nsga2_pool_restart_every_10.md``)
and ``HV_PLATEAU_AUTO_STOP = False`` (memory:
``feedback_disable_hv_plateau_autostop.md``) are surfaced here as named
module-level constants so the smoke gate and a downstream grep both pick
them up directly from ``constants.py``.

Back-compat aliases for t0104/t0106/t0114/t0115/t0122/t0124 budget symbol
names are preserved so the forked ``cost_watchdog`` and ``nsga2_driver``
modules pick up the $6 task cap without further code changes.
"""

from __future__ import annotations

from tasks.t0128_t0127_rerun_dsi_atp_3seeds.code.constants_morphology import (
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

# t0128-specific run schedule (3 fresh non-lineage seeds, sequential on
# one EPYC). Seeds drawn via ``secrets.randbelow(10000)`` at task creation
# (2026-05-26), rejecting (a) multiples of 100/500/1000, (b) zero, and
# (c) any prior-lineage seed in {77, 441, 1524, 2247, 6650, 7755, 8929,
# 9354}. The 3 values below were the first 3 valid draws of that procedure.
T0128_SEEDS: tuple[int, ...] = (2608, 8276, 9986)
T0124_SEED_EXCLUDED: int = 6650  # documented exclusion (t0124's seed)
T0126_SEED_EXCLUDED: int = 8929  # documented exclusion (t0126's seed)

# Hard cost cap: $4.00, dictated by current Vast.ai credit ($4.81 verified
# 2026-05-26). Realistic 3-seed spend is ~$3.42 ($0.19/hr * 6 h * 3) so this
# cap leaves ~$0.58 of headroom. If a seed is slow the watchdog trips before
# the credit runs out, yielding partial results rather than a 0-credit halt.
COST_CAP_USD: float = 4.0
T0128_HARD_BUDGET_USD: float = COST_CAP_USD
T0128_PER_INSTANCE_WATCHDOG_USD: float = 3.5

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
T0104_SEEDS: tuple[int, ...] = T0128_SEEDS
T0104_HARD_BUDGET_PER_SEED_USD: float = T0128_HARD_BUDGET_USD
T0104_TASK_BUDGET_TOTAL_USD: float = T0128_HARD_BUDGET_USD
T0106_SEEDS: tuple[int, ...] = T0128_SEEDS
T0106_HARD_BUDGET_USD: float = T0128_HARD_BUDGET_USD
T0106_PER_INSTANCE_WATCHDOG_USD: float = T0128_PER_INSTANCE_WATCHDOG_USD
T0114_SEEDS: tuple[int, ...] = T0128_SEEDS
T0114_HARD_BUDGET_USD: float = T0128_HARD_BUDGET_USD
T0114_PER_INSTANCE_WATCHDOG_USD: float = T0128_PER_INSTANCE_WATCHDOG_USD
T0115_SEEDS: tuple[int, ...] = T0128_SEEDS
T0115_HARD_BUDGET_USD: float = T0128_HARD_BUDGET_USD
T0115_PER_INSTANCE_WATCHDOG_USD: float = T0128_PER_INSTANCE_WATCHDOG_USD
T0122_SEEDS: tuple[int, ...] = T0128_SEEDS
T0122_HARD_BUDGET_USD: float = T0128_HARD_BUDGET_USD
T0122_PER_INSTANCE_WATCHDOG_USD: float = T0128_PER_INSTANCE_WATCHDOG_USD

assert len(T0128_SEEDS) == 3, f"expected 3 seeds, got {len(T0128_SEEDS)}"
_LINEAGE_EXCLUDED: set[int] = {77, 441, 1524, 2247, 6650, 7755, 8929, 9354}
for _s in T0128_SEEDS:
    assert _s not in _LINEAGE_EXCLUDED, (
        f"T0128 seed {_s} collides with prior lineage seed; must be fresh"
    )
    assert _s % 100 != 0 and _s % 500 != 0 and _s % 1000 != 0, (
        f"T0128 seed {_s} is a round number; must be non-round"
    )
    assert _s > 0, f"T0128 seed {_s} must be positive"
assert len(set(T0128_SEEDS)) == len(T0128_SEEDS), "T0128_SEEDS must be unique"
assert T0128_HARD_BUDGET_USD > 0
assert T0128_PER_INSTANCE_WATCHDOG_USD <= T0128_HARD_BUDGET_USD
assert _POOL_RESTART_EVERY == 10, "10-gen rule: _POOL_RESTART_EVERY must be 10"
assert HV_PLATEAU_AUTO_STOP is False, "auto-stop disabled per project policy"
assert N_GEN_MAX == 60, f"N_GEN_MAX must be 60, got {N_GEN_MAX}"
assert N_DIRECTIONS == 2, f"N_DIRECTIONS must be 2, got {N_DIRECTIONS}"
assert POP_SIZE == 96, f"POP_SIZE must be 96, got {POP_SIZE}"
assert N_EVAL_SEEDS == 3, f"N_EVAL_SEEDS must be 3, got {N_EVAL_SEEDS}"
assert COST_CAP_USD == 4.0, f"COST_CAP_USD must be 4.0, got {COST_CAP_USD}"

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
    "T0124_SEED_EXCLUDED",
    "T0128_HARD_BUDGET_USD",
    "T0128_PER_INSTANCE_WATCHDOG_USD",
    "T0128_SEEDS",
    "UPPER_BOUNDS_68",
    "WORST_CASE_ATP_PER_SPIKE",
    "WORST_CASE_DSI",
    "WORST_CASE_MI_BITS",
    "WORST_CASE_PD_RATE_HZ",
    "WORST_CASE_ROBUSTNESS",
    "_POOL_RESTART_EVERY",
]
