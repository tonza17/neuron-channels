"""Constants for t0105 cluster + factor analysis."""

from __future__ import annotations

# Filter thresholds (REQ-1, REQ-3, REQ-11).
PRIMARY_DSI_THRESHOLD: float = 0.1
PRIMARY_PD_THRESHOLD: float = 2.0
STRICT_DSI_THRESHOLD: float = 0.2
STRICT_PD_THRESHOLD: float = 3.0

# Silenced-cell artifact filter (REQ-3).
SILENCE_DSI_THRESHOLD: float = 0.95
SILENCE_PD_THRESHOLD: float = 5.0

# Asymmetry classification (REQ-4).
ASYM_CLASS_THRESHOLD: float = 0.5
ASYM_THRESHOLD_SWEEP: tuple[float, ...] = (0.3, 0.5, 1.0)

# Vector layout (54 electrophys + 14 morphology).
N_ELECTROPHYS_DIMS: int = 54
N_MORPHOLOGY_DIMS: int = 14
N_TOTAL_DIMS: int = 68

# Morphology offsets inside the 68-d vector (used by the asym-score formula).
MORPH_OFFSET: int = N_ELECTROPHYS_DIMS
IDX_SOMA_OFFSET_PD_UM: int = MORPH_OFFSET + 5
IDX_FIELD_ELONGATION_PD: int = MORPH_OFFSET + 6
IDX_BRANCH_DENSITY_GRADIENT_PD: int = MORPH_OFFSET + 7
IDX_PRIMARY_BRANCH_PD_CONCENTRATION: int = MORPH_OFFSET + 8

# Asymmetry-score normalisation denominators (REQ-4).
ASYM_DENOM_SOMA_OFFSET: float = 150.0
ASYM_DENOM_FIELD_ELONGATION: float = 2.0
ASYM_FIELD_ELONGATION_BASELINE: float = 1.0
ASYM_DENOM_BRANCH_DENSITY_GRADIENT: float = 1.0
ASYM_DENOM_PRIMARY_BRANCH_PD_CONCENTRATION: float = 5.0

# 54 electrophys parameter names (PARAM_NAMES, derived from ParamIndex enum in t0104).
ELECTROPHYS_PARAM_NAMES: tuple[str, ...] = (
    "NAV16_SOMA_GBAR",
    "NAV16_PRIMARY_GBAR",
    "NAV16_MID_GBAR",
    "NAV16_TERMINAL_GBAR",
    "NAV16_AIS_GBAR",
    "KV3_SOMA_GBAR",
    "KV3_PRIMARY_GBAR",
    "KV3_MID_GBAR",
    "KV3_TERMINAL_GBAR",
    "KV3_AIS_GBAR",
    "NAP_SOMA_GBAR",
    "NAP_PRIMARY_GBAR",
    "NAP_MID_GBAR",
    "NAP_TERMINAL_GBAR",
    "NAP_AIS_GBAR",
    "BK_SOMA_GBAR",
    "BK_PRIMARY_GBAR",
    "BK_MID_GBAR",
    "BK_TERMINAL_GBAR",
    "BK_AIS_GBAR",
    "SK_SOMA_GBAR",
    "SK_PRIMARY_GBAR",
    "SK_MID_GBAR",
    "SK_TERMINAL_GBAR",
    "SK_AIS_GBAR",
    "KDR_GBAR",
    "KV4_GBAR",
    "NAR_GBAR",
    "IH_GBAR",
    "CAL_GBAR",
    "CAT_GBAR",
    "IM_GBAR",
    "SKAHP_GBAR_SOMA_AIS",
    "SKAHP_TAU_CA_MULTIPLIER",
    "RA_OHM_CM",
    "CM_UF_CM2",
    "GLEAK_S_CM2",
    "CAD_DEPTH_UM",
    "CAD_TAUR_MS",
    "N_ACH",
    "N_GABA",
    "RHO0_ACH",
    "LAMBDA_ACH_UM",
    "RHO0_GABA",
    "LAMBDA_GABA_UM",
    "W_ACH_US",
    "W_GABA_US",
    "AIS_LENGTH_UM",
    "AIS_DIAMETER_UM",
    "GNMDA_DEND",
    "MG_CONC_MM",
    "VOFF_NMDA",
    "NAV16_DEND_DISTAL",
    "NAP_DEND_DISTAL",
)
assert len(ELECTROPHYS_PARAM_NAMES) == N_ELECTROPHYS_DIMS

# 14 morphology parameter names (matching t0090.constants.PARAM_NAMES).
MORPHOLOGY_PARAM_NAMES: tuple[str, ...] = (
    "num_primary_branches",
    "branch_prob_per_um",
    "max_strahler_depth",
    "mean_branching_angle_deg",
    "rall_exponent",
    "soma_offset_pd_um",
    "field_elongation_pd",
    "branch_density_gradient_pd",
    "primary_branch_pd_concentration",
    "mean_segment_length_um",
    "soma_diameter_um",
    "ais_length_um",
    "morph_seed",
    "branch_length_cv",
)
assert len(MORPHOLOGY_PARAM_NAMES) == N_MORPHOLOGY_DIMS

ALL_PARAM_NAMES: tuple[str, ...] = ELECTROPHYS_PARAM_NAMES + MORPHOLOGY_PARAM_NAMES
assert len(ALL_PARAM_NAMES) == N_TOTAL_DIMS

# Source-task tags.
SOURCE_T0091: str = "t0091"
SOURCE_T0099: str = "t0099"
SOURCE_T0102: str = "t0102"
SOURCE_T0104: str = "t0104"
ALL_SOURCE_TASKS: tuple[str, ...] = (SOURCE_T0091, SOURCE_T0099, SOURCE_T0102, SOURCE_T0104)

# Lineages with pre-guard data that needs the post-hoc silenced-cell filter.
PRE_GUARD_SOURCE_TASKS: frozenset[str] = frozenset({SOURCE_T0091, SOURCE_T0099, SOURCE_T0102})

# Asymmetry classes.
CLASS_SYMMETRIC: str = "symmetric"
CLASS_ASYMMETRIC: str = "asymmetric"

# Analysis hyperparameters.
GALLERY_MAX_CELLS: int = 30
BOOTSTRAP_RESAMPLES: int = 200
KAISER_FACTOR_CAP: int = 10
CHART_DPI: int = 150
RANDOM_SEED: int = 42

# Dedup precision: round to 6 decimal places before signing.
DEDUP_DECIMALS: int = 6

# Registered metric keys (from meta/metrics/).
METRIC_DIRECTION_SELECTIVITY_INDEX: str = "direction_selectivity_index"
METRIC_TUNING_CURVE_HWHM_DEG: str = "tuning_curve_hwhm_deg"
METRIC_TUNING_CURVE_RELIABILITY: str = "tuning_curve_reliability"
METRIC_TUNING_CURVE_RMSE: str = "tuning_curve_rmse"

# Variant IDs for metrics.json (REQ-14).
VARIANT_PRIMARY_COHORT: str = "primary_cohort"
VARIANT_STRICT_COHORT: str = "strict_cohort"

# Spec versions used by output answer assets.
ANSWER_SPEC_VERSION: str = "2"
