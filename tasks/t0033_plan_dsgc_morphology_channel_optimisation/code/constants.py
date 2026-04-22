"""Named constants for task t0033 planning-cost arithmetic.

All magic strings and numeric constants that feed into the cost model live
here. This keeps `ruff` happy on string-literal duplication and provides a
single source of truth for downstream scripts.
"""

from enum import StrEnum

# Region tags match `tasks/t0022_modify_dsgc_channel_testbed/code/dsgc_channel_partition.hoc`.
REGION_SOMA: str = "SOMA_CHANNELS"
REGION_DEND: str = "DEND_CHANNELS"
REGION_AIS_PROX: str = "AIS_PROXIMAL"
REGION_AIS_DIST: str = "AIS_DISTAL"
REGION_THIN_AXON: str = "THIN_AXON"

# Sub-dendrite tiers introduced by the t0024 port.
DEND_TIER_PRIMARY: str = "primary_dend"
DEND_TIER_NONTERMINAL: str = "nonterminal_dend"
DEND_TIER_TERMINAL: str = "terminal_dend"

# Canonical protocol per t0022.
N_ANGLES: int = 12
N_TRIALS_DETERMINISTIC: int = 8
N_TRIALS_STOCHASTIC: int = 10

# t0026 empirical anchors (seconds per angle-trial) — Source:
# tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/results_detailed.md
T0022_DETERMINISTIC_S_PER_ANGLE_TRIAL: float = 3.8
T0024_STOCHASTIC_S_PER_ANGLE_TRIAL: float = 12.0

# Under the full 12 angle x 10-trial canonical optimisation protocol.
SECONDS_PER_SIM_DETERMINISTIC: float = (
    T0022_DETERMINISTIC_S_PER_ANGLE_TRIAL * N_ANGLES * N_TRIALS_STOCHASTIC
)  # 456.0 s
SECONDS_PER_SIM_STOCHASTIC: float = (
    T0024_STOCHASTIC_S_PER_ANGLE_TRIAL * N_ANGLES * N_TRIALS_STOCHASTIC
)  # 1440.0 s

# Assumption: CoreNEURON speedup at RTX 3090 reference vs single-threaded CPU NEURON.
# Flagged in the answer-asset limitations section; not corpus-evidenced.
CORENEURON_REFERENCE_SPEEDUP: float = 5.0

# Assumption: NN-surrogate inference speedup over direct NEURON simulation.
# Flagged in limitations; sensitivity band covers 50x-500x.
SURROGATE_INFERENCE_SPEEDUP: float = 100.0

# Assumption: NN-surrogate training sample count (central).
# Poleg-Polsky 2026 mentions "tens of thousands of configurations" but does
# not break out training vs validation sample counts.
SURROGATE_TRAIN_SAMPLES_LOWER: int = 1000
SURROGATE_TRAIN_SAMPLES_CENTRAL: int = 5000
SURROGATE_TRAIN_SAMPLES_UPPER: int = 50000

# Many-core CPU parallelism assumption (Vast.ai standard 96-core node).
CPU_CORES_PER_NODE: int = 96

# Checkpointing overhead kicks in at the 2-hour cliff per
# arf/specifications/remote_machines_specification.md.
CHECKPOINT_CLIFF_HOURS: float = 2.0
CHECKPOINT_OVERHEAD_MULT: float = 1.05

# Parameter-count presets (plan commits).
N_FREE_PARAMS_TIGHT: int = 25
N_FREE_PARAMS_RICH: int = 45

# Sensitivity grid multipliers.
COST_MULTIPLIERS: tuple[float, ...] = (0.5, 1.0, 2.0)
SAMPLE_MULTIPLIERS: tuple[float, ...] = (0.5, 1.0, 2.0)

# Answer-asset confidence (plan commits to medium with caveats).
ANSWER_CONFIDENCE: str = "medium"

# Vast.ai pricing snapshot (date-stamped; not a live quote).
PRICING_SNAPSHOT_DATE: str = "2026-04-22"
PRICING_SOURCE_NOTE: str = "vast.ai historical market observation; not a live quote"


class SearchStrategy(StrEnum):
    """Gradient-free search strategies evaluated in the cost model."""

    GRID = "GRID"
    RANDOM = "RANDOM"
    CMA_ES = "CMA_ES"
    BAYESIAN = "BAYESIAN"
    SURROGATE_NN_GA = "SURROGATE_NN_GA"


class ComputeMode(StrEnum):
    """Compute-backend options priced by the Vast.ai cost model."""

    CORENEURON_GPU = "CORENEURON_GPU"
    SURROGATE_NN_GPU = "SURROGATE_NN_GPU"
    MANY_CORE_CPU = "MANY_CORE_CPU"


class Tier(StrEnum):
    """Vast.ai GPU tier labels compared in the plan."""

    RTX_3090 = "RTX 3090"
    RTX_4090 = "RTX 4090"
    A100_40GB = "A100 40GB"
    H100 = "H100"
    CPU_96 = "CPU-96"


# Column names for CSV outputs (eliminates magic strings in downstream code).
COL_STRATEGY: str = "strategy"
COL_COMPUTE_MODE: str = "compute_mode"
COL_TIER: str = "tier"
COL_N_DIMS: str = "n_dims"
COL_PARAMETERISATION: str = "parameterisation"
COL_N_SAMPLES_LOWER: str = "n_samples_lower"
COL_N_SAMPLES_CENTRAL: str = "n_samples_central"
COL_N_SAMPLES_UPPER: str = "n_samples_upper"
COL_ASSUMPTION: str = "assumption_text"
COL_SOURCE_CITATION: str = "source_citation"
COL_MODEL_VARIANT: str = "model_variant"
COL_N_ANGLES: str = "n_angles"
COL_N_TRIALS: str = "n_trials"
COL_S_PER_ANGLE_TRIAL: str = "seconds_per_angle_trial"
COL_TOTAL_SECONDS: str = "total_seconds"
COL_TOTAL_MINUTES: str = "total_minutes"
COL_PER_SIM_SECONDS: str = "per_sim_seconds"
COL_DOLLARS_PER_HOUR: str = "dollars_per_hour"
COL_SPEED_TIER_RATIO: str = "speed_tier_ratio"
COL_USD_TOTAL: str = "usd_total"
COL_WALL_HOURS: str = "wall_hours"
COL_EFFECTIVE_WALL_HOURS: str = "effective_wall_hours"
COL_COST_MULT: str = "cost_mult"
COL_SAMPLE_MULT: str = "sample_mult"
COL_USD_SENSITIVITY: str = "usd_scaled"
COL_TRAIN_USD: str = "train_usd"
COL_INFER_USD: str = "inference_usd"
COL_NOTES: str = "notes"

PARAM_TIGHT: str = "tight"
PARAM_RICH: str = "rich"
