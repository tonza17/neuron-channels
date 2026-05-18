"""Constants for t0108 cluster + factor analysis (strict cohort)."""

from __future__ import annotations

DSI_THRESHOLD: float = 0.5
PD_THRESHOLD_HZ: float = 10.0

DEDUP_DECIMALS: int = 6

N_ELECTROPHYS_DIMS: int = 54
N_MORPHOLOGY_DIMS: int = 14
N_TOTAL_DIMS: int = 68

K_SWEEP: tuple[int, ...] = (2, 3, 4)
KMEANS_RANDOM_STATE: int = 42
N_INIT_KMEANS: int = 10

KAISER_FACTOR_CAP: int = 10
VARIANCE_RETENTION_TARGET: float = 0.80
JOINT_FACTOR_R_THRESHOLD: float = 0.30

CHART_DPI: int = 150
RANDOM_SEED: int = 42

SOURCE_TASK: str = "t0106_long_pdnd_nsga2_300gen"
SOURCE_SEED: int = 44

VARIANT_STRICT_COHORT: str = "t0108_strict_cohort"

ANSWER_SPEC_VERSION: str = "2"

# 54 electrophys parameter names (identical to t0105 / t0104 ParamIndex order).
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

# 14 morphology parameter names (matching t0090 / t0105 layout).
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
