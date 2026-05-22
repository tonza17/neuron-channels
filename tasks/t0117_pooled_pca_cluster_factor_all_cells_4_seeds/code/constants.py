"""Constants for t0117 pooled PCA + cluster + factor analysis (no DSI/PD filter)."""

from __future__ import annotations

from pathlib import Path

# Dead constants retained from t0116 for documentation; t0117 does NOT apply any cohort filter.
DSI_THRESHOLD: float = 0.7
PD_THRESHOLD_HZ: float = 10.0

DEDUP_DECIMALS: int = 6

N_ELECTROPHYS_DIMS: int = 54
N_MORPHOLOGY_DIMS: int = 14
N_TOTAL_DIMS: int = 68

K_SWEEP: tuple[int, ...] = (3, 4, 5, 6, 7)
KMEANS_RANDOM_STATE: int = 42
N_INIT_KMEANS: int = 10

KAISER_FACTOR_CAP: int = 10
VARIANCE_RETENTION_TARGET: float = 0.80
JOINT_FACTOR_R_THRESHOLD: float = 0.30

CHART_DPI: int = 150
RANDOM_SEED: int = 42

GEN0_GENERATION_INDEX: int = 1
EXPECTED_GEN0_PER_SEED: int = 96
MAX_MORPH_SEED: int = 2**31 - 1
N_REPRESENTATIVES_PER_CLUSTER: int = 15

ANSWER_SPEC_VERSION: str = "2"

# Four NSGA-II pool sources to combine: (source_task, seed, predictions_path_relative_to_repo).
SOURCES: tuple[tuple[str, int, Path], ...] = (
    (
        "t0106_long_pdnd_nsga2_300gen",
        44,
        Path(
            "tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/"
            "nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz"
        ),
    ),
    (
        "t0112_t0106_seed77_replicate",
        77,
        Path(
            "tasks/t0112_t0106_seed77_replicate/assets/predictions/"
            "t0112-bedb-morph-nsga2-seed77/files/all_evaluations_seed77.json.gz"
        ),
    ),
    (
        "t0114_seed7755_no_autostop",
        7755,
        Path(
            "tasks/t0114_seed7755_no_autostop/assets/predictions/"
            "t0114-bedb-morph-nsga2-seed7755/files/predictions.jsonl.gz"
        ),
    ),
    (
        "t0115_seed9354_no_autostop",
        9354,
        Path(
            "tasks/t0115_seed9354_no_autostop/assets/predictions/"
            "t0115-bedb-morph-nsga2-seed9354/files/predictions.jsonl.gz"
        ),
    ),
)

# 54 electrophys parameter names (identical to t0106 / t0108 ParamIndex order).
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

# 14 morphology parameter names (matching t0090 / t0108 layout).
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

# Tab10 colours assigned to the four seeds (in SOURCES order).
SEED_COLORS: tuple[str, str, str, str] = (
    "#1f77b4",  # tab10[0] — t0106 seed 44
    "#ff7f0e",  # tab10[1] — t0112 seed 77
    "#2ca02c",  # tab10[2] — t0114 seed 7755
    "#d62728",  # tab10[3] — t0115 seed 9354
)
