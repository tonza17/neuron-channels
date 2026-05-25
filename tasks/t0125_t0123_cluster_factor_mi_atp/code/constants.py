"""Constants for t0125 cluster + factor analysis (t0123 single-seed MI/ATP NSGA-II)."""

from __future__ import annotations

DEDUP_DECIMALS: int = 6

N_ELECTROPHYS_DIMS: int = 54
N_MORPHOLOGY_DIMS: int = 14
N_TOTAL_DIMS: int = 68

K_SWEEP: tuple[int, ...] = (3, 4, 5, 6, 7)
KMEANS_RANDOM_STATE: int = 42
N_INIT_KMEANS: int = 10

KAISER_FACTOR_CAP: int = 10
JOINT_FACTOR_R_THRESHOLD: float = 0.30

CHART_DPI: int = 150
RANDOM_SEED: int = 42

MAX_MORPH_SEED: int = 2**31 - 1
N_REPRESENTATIVES_PER_CLUSTER: int = 15

# t0123 NSGA-II layout: pop_size = 96, 60 generations → 5760 cells; cell_index is 0-indexed.
T0123_POP_SIZE: int = 96
T0123_EXPECTED_RAW_CELLS: int = 5760
GEN0_GENERATION_INDEX: int = 1  # 1-indexed convention from t0117

# Spiking-cohort filter for the ATP-per-spike-stability analyses.
SPIKING_PD_RATE_HZ_THRESHOLD: float = 1.0

# Quartile group cuts.
MI_QUARTILE_TOP_QUANTILE: float = 0.75
MI_QUARTILE_BOTTOM_QUANTILE: float = 0.25
ATP_QUARTILE_TOP_QUANTILE: float = 0.75
ATP_QUARTILE_BOTTOM_QUANTILE: float = 0.25
MEDIAN_QUANTILE: float = 0.5

# Cliff's delta top-N for the ranked bar charts.
CLIFFS_DELTA_TOP_N: int = 20

ANSWER_SPEC_VERSION: str = "2"

# Corner labels (MI x ATP 2x2 corners) — used as categorical keys throughout.
CORNER_HIGH_MI_LOW_ATP: str = "high_mi_low_atp"
CORNER_HIGH_MI_HIGH_ATP: str = "high_mi_high_atp"
CORNER_LOW_MI_LOW_ATP: str = "low_mi_low_atp"
CORNER_LOW_MI_HIGH_ATP: str = "low_mi_high_atp"
CORNER_LABELS: tuple[str, str, str, str] = (
    CORNER_HIGH_MI_LOW_ATP,
    CORNER_HIGH_MI_HIGH_ATP,
    CORNER_LOW_MI_LOW_ATP,
    CORNER_LOW_MI_HIGH_ATP,
)

# Tab10 colours assigned to the four corners (in CORNER_LABELS order).
CORNER_COLORS: tuple[str, str, str, str] = (
    "#2ca02c",  # tab10[2] — Pareto-favoured (high MI, low ATP)
    "#ff7f0e",  # tab10[1]
    "#7f7f7f",  # tab10[7]
    "#d62728",  # tab10[3] — Pareto-dominated (low MI, high ATP)
)

# 54 electrophys parameter names (identical to t0108 / t0117 ParamIndex order).
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

# 14 morphology parameter names (matching t0090 / t0117 layout).
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
