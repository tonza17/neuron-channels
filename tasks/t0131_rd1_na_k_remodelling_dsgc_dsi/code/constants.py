"""Constants for t0131 (rd1-like Na/K remodelling of the DSGC model)."""

from enum import StrEnum

# ---- Simulation protocol (copied from t0129 constants_electrophys.py) ----
CELSIUS_DEG_C: float = 36.9
DT_MS: float = 0.1
STEPS_PER_MS: float = 10.0
TSTOP_MS: float = 1400.0
V_INIT_MV: float = -60.0
AP_THRESHOLD_MV: float = -10.0
PD_DIRECTION_DEG: float = 0.0
ND_DIRECTION_DEG: float = 180.0
RHO_CORRELATED: float = 0.6
SEED_BASE: int = 1000
STABILITY_PEAK_VM_MIN_MV: float = -80.0
STABILITY_PEAK_VM_MAX_MV: float = 60.0
N_PARAMS_54: int = 54
N_PARAMS_68: int = 68
N_MORPH_PARAMS: int = 14
N_EVAL_SEEDS: int = 3
N_DIRECTIONS_FULL: int = 8
EVAL_SEED_SS: int = 42

# Silence guard: PD spikes summed over seeds below this => low_count flag.
LOW_COUNT_PD_SPIKES: int = 3

# ---- Reference cells ----
RNG_SEED: int = 131
LEGIT_DSI_MIN: float = 0.5
LEGIT_DSI_CEILING: float = 0.9999
LEGIT_PD_RATE_MIN_HZ: float = 30.0
ALL_SEED_KEYS: list[str] = [
    "t0106_seed44",
    "t0112_seed77",
    "t0114_seed7755",
    "t0115_seed9354",
]
SEED_TASK_IDS: dict[str, str] = {
    "t0106_seed44": "t0106_long_pdnd_nsga2_300gen",
    "t0112_seed77": "t0112_t0106_seed77_replicate",
    "t0114_seed7755": "t0114_seed7755_no_autostop",
    "t0115_seed9354": "t0115_seed9354_no_autostop",
}
EXPECTED_STRATUM_COUNTS: dict[str, int] = {
    "t0114_seed7755": 484,
    "t0106_seed44": 121,
    "t0115_seed9354": 63,
    "t0112_seed77": 7,
}
EXPECTED_POOLED_ROWS: int = 675
STRATUM_DRAW_ORDER: list[str] = [
    "t0114_seed7755",
    "t0106_seed44",
    "t0115_seed9354",
    "t0112_seed77",
]
STRATUM_DRAW_COUNTS: dict[str, int] = {
    "t0114_seed7755": 3,
    "t0106_seed44": 2,
    "t0115_seed9354": 2,
    "t0112_seed77": 1,
}
N_HEATMAP_CELLS: int = 5
N_PANEL_D_CELLS: int = 3

# ---- Section / mechanism names ----
SOMA_SECTION: str = "soma_t90"
AIS_PROXIMAL_SECTION: str = "ais_proximal_t90"
AIS_DISTAL_SECTION: str = "ais_distal_t90"
NA_MECHANISMS: list[str] = ["nav16t80"]
NA_DENDRITIC_EXTRA: list[str] = ["napt80"]
K_MECHANISMS: list[str] = ["kdrt80", "kv3t80", "kv4t80"]
HHST: str = "HHst"
HHST_GNABAR: str = "gnabar_HHst"
HHST_GKBAR: str = "gkbar_HHst"
CURRENT_SUFFIXES_NA: list[str] = ["nav16t80", "napt80", "nart80"]
CURRENT_SUFFIXES_K: list[str] = ["kdrt80", "kv3t80", "kv4t80", "kv7t80", "bkt80", "skt80"]


class ScalingArm(StrEnum):
    SOMA_AIS = "soma_ais"
    SOMA_AIS_DENDRITE = "soma_ais_dendrite"


class Condition(StrEnum):
    WT_LIKE = "wt_like"
    RD1_LIKE = "rd1_like"
    WT_LIKE_BIAS = "wt_like_with_bias"
    RD1_LIKE_BIAS = "rd1_like_with_bias"


# ---- Voltage clamp (panel C) ----
V_HOLD_MV: float = -65.0
V_STEP_DELTA_MV: float = 100.0
V_STEP_ABS_SENSITIVITY_MV: float = 40.0
CLAMP_HOLD_PRE_MS: float = 50.0
CLAMP_STEP_MS: float = 340.0
CLAMP_HOLD_POST_MS: float = 60.0
CLAMP_RS_MOHM: float = 0.001
CLAMP_DT_MS: float = 0.025
CLAMP_SUSTAINED_WINDOW_MS: float = 50.0
CLAMP_TRANSIENT_WINDOW_MS: float = 5.0
TARGET_SUSTAINED_RATIO: float = 1.7
TARGET_TRANSIENT_RATIO: float = 0.25
TRANSIENT_RATIO_SENSITIVITY: list[float] = [0.15, 0.35]
LOSS_SCALE_SUSTAINED: float = 0.1
LOSS_SCALE_TRANSIENT: float = 0.1
SUSTAINED_RATIO_TOLERANCE: float = 0.15
MAX_SUSTAINED_FAIL_THRESHOLD: float = 1.55
S_NA_GRID: list[float] = [0.25, 0.40, 0.55, 0.70, 0.85, 1.00]
S_K_GRID: list[float] = [1.0, 1.4, 1.8, 2.2, 2.6, 3.0]
MIN_TRANSIENT_ABS_NA: float = 0.2
CLAMP_REPORT_PRE_MS: float = 50.0
CLAMP_TARGET_ABS_NA_WT_SUSTAINED: float = 2.0

# ---- Current clamp (panel B) ----
CC_DELAY_MS: float = 100.0
CC_DUR_MS: float = 500.0
CC_TSTOP_MS: float = 700.0
CC_DT_MS: float = 0.025
CC_AMPLITUDES_PA: list[float] = [0.0, 20.0, 40.0, 60.0, 100.0, 200.0, 400.0, 800.0]
CC_TEST_AMP_PA: float = 60.0
CC_FIRST_WINDOW_MS: float = 100.0
CC_LAST_WINDOW_MS: float = 200.0
COLLAPSE_MAX_RD1_SPIKES: int = 1
COLLAPSE_MIN_DIFFERENCE: int = 3
WT_MIN_SPIKES_INFORMATIVE: int = 2
V_INIT_CLAMP_MV: float = -65.0

# ---- Spontaneous activity and bias ----
SPONT_DUR_MS: float = 2000.0
SPONT_SETTLE_MS: float = 200.0
SPONT_DT_MS: float = 0.1
SPONT_NOISE_SEEDS: list[int] = [11, 22, 33]
BIAS_GRID_PA: list[float] = [0.0, 5.0, 10.0, 15.0, 20.0, 30.0, 40.0, 50.0]
NOISE_GRID_PA: list[float] = [0.0, 5.0, 10.0]
BIAS_TUNING_N_CELLS: int = 3
BIAS_TARGET_RATE_HZ: float = 7.0
BIAS_MIN_ISI_CV: float = 0.5
TRIGGER_C_RATE_MIN_HZ: float = 4.0
TRIGGER_C_RATE_MAX_HZ: float = 10.0
TRIGGER_C_WT_MAX_HZ: float = 1.0
TRIGGER_B_MIN_COLLAPSED_CELLS: int = 6

# ---- DSI protocol ----
DSI_N_BOOTSTRAP: int = 10000
WILCOXON_ALPHA: float = 0.05
HEATMAP_DIRECTIONS_DEG: list[float] = [0.0, 180.0]
HEATMAP_N_SEEDS: int = 2
DSI_GATE_PD_TOLERANCE: float = 0.25
DSI_GATE_MIN_DSI: float = 0.3

# ---- Panel D ----
PD_STRENGTHS: list[float] = [0.0, 5.0, 10.0, 20.0, 30.0, 50.0, 75.0, 100.0]
PD_N_SEEDS: int = 3
PULSE_CENTERS_MS: list[float] = [180.0, 430.0, 680.0]
PULSE_SIGMA_MS: float = 20.0
PULSE_TSTOP_MS: float = 1000.0
PULSE_N_REPS: int = 10
PSTH_BIN_MS: float = 10.0
PSTH_SMOOTH_SIGMA_MS: float = 20.0
BASELINE_WINDOWS_MS: list[list[float]] = [[0.0, 100.0], [900.0, 1000.0]]
SAT_PRED_RD1_MIN: float = 0.9
SAT_PRED_WT_MAX: float = 0.6
BASELINE_PRED_RD1: float = 0.35

# Toy-model anchor points read by eye from panel D (relative / output units).
TOY_U_GRID_MAX: float = 100.0
TOY_WT_ANCHORS_U_OUT: list[list[float]] = [[0.0, 0.0], [50.0, 10.0], [100.0, 15.0]]
TOY_RD1_ANCHORS_U_OUT: list[list[float]] = [[0.0, 10.0], [5.0, 23.0], [50.0, 23.0], [100.0, 23.0]]
TOY_BASELINE_RD1: float = 0.35
TOY_BASELINE_WT: float = 0.0
TOY_PEAK_HEIGHTS: list[float] = [0.9, 0.85, 0.8]
TOY_ANCHOR_TOLERANCE: float = 0.2

# ---- Parallelism ----
MAX_WORKERS: int = 7

# ---- Strings ----
COL_CELL_ID: str = "cell_id"

# ---- Added during implementation ----
CLAMP_TRANSIENT_START_MS: float = 0.5
CLAMP_BASELINE_WINDOW_MS: float = 10.0
CC_SETTLE_MS: float = 200.0
NA_CURRENT_ATTRS: list[str] = ["i_nav16t80", "i_napt80", "i_nart80"]
K_CURRENT_ATTRS: list[str] = ["i_kdrt80", "i_kv3t80", "i_kv4t80", "i_kv7t80", "i_bkt80", "i_skt80"]
HHST_INA_ATTR: str = "ina"
HHST_IK_ATTR: str = "ik"
NA_PER_MA_CM2_UM2: float = 1e-2

# ---- Reference-cell reproducibility screen (added after the Step 9/11 gates failed) ----
SCREEN_SPARE_CANDIDATES: int = 5
SCREEN_PD_TOLERANCE: float = 0.25
SCREEN_MIN_DSI: float = 0.3

# ---- Exploratory extensions (flagged as such in all outputs) ----
# The model's absolute current scale is ~100x the researcher's (sustained clamp current of
# hundreds of nA versus ~2 nA), so pA-range currents barely perturb it. The extended grids
# below are only used when the pre-declared grids fail the pre-declared criteria.
CC_AMPLITUDES_EXTENDED_PA: list[float] = [1000.0, 2000.0, 5000.0, 10000.0]
BIAS_GRID_EXTENDED_PA: list[float] = [100.0, 200.0, 400.0, 800.0, 1600.0, 3200.0, 6400.0]
NOISE_GRID_EXTENDED_PA: list[float] = [0.0, 100.0, 400.0, 1600.0]

# ---- Toy-model anchors, all read by eye from panel D (relative signal / output units) ----
TOY_U_REF: float = 100.0
TOY_DT_MS: float = 0.5
TOY_TSTOP_MS: float = 1000.0
TOY_MEAN_PEAK_TARGET: float = 0.88
TOY_RD1_MIN_BETWEEN_TARGET: float = 0.30
TOY_STATIC_U_SAT_CHECK: float = 20.0
SPONT_DT_RUN_MS: float = 0.05
