"""Canonical constants for the t0026 V_rest sweep task.

Defines the exact eight-value sweep grid, the 12-angle direction protocol, the
trial counts for each model, and the CSV column names used by the tidy output.
Path constants for the task's `data/` and `results/images/` subdirectories are
also centralized here (per the project Python style guide).
"""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0026_vrest_sweep_tuning_curves_dsgc"

# Sweep grid (REQ-1). Exactly eight values, -90 to -20 mV in 10 mV steps.
V_REST_VALUES_MV: tuple[float, ...] = (
    -90.0,
    -80.0,
    -70.0,
    -60.0,
    -50.0,
    -40.0,
    -30.0,
    -20.0,
)

# 12-angle direction protocol (0, 30, 60, ..., 330 degrees).
ANGLES_DEG: tuple[int, ...] = tuple(range(0, 360, 30))

# Trial counts (REQ-3, REQ-4).
N_TRIALS_T0022: int = 1
N_TRIALS_T0024: int = 10

# t0024 stochastic parameters.
AR2_RHO_T0024: float = 0.6  # correlated condition

# CSV column names (tidy schema used by both models' sweep drivers).
CSV_COL_V_REST_MV: str = "v_rest_mv"
CSV_COL_TRIAL: str = "trial"
CSV_COL_DIRECTION_DEG: str = "direction_deg"
CSV_COL_SPIKE_COUNT: str = "spike_count"
CSV_COL_PEAK_MV: str = "peak_mv"
CSV_COL_FIRING_RATE_HZ: str = "firing_rate_hz"

CSV_COLUMNS: tuple[str, ...] = (
    CSV_COL_V_REST_MV,
    CSV_COL_TRIAL,
    CSV_COL_DIRECTION_DEG,
    CSV_COL_SPIKE_COUNT,
    CSV_COL_PEAK_MV,
    CSV_COL_FIRING_RATE_HZ,
)

# Data / results paths.
DATA_DIR: Path = TASK_ROOT / "data"
DATA_T0022_DIR: Path = DATA_DIR / "t0022"
DATA_T0024_DIR: Path = DATA_DIR / "t0024"

VREST_SWEEP_TIDY_CSV_NAME: str = "vrest_sweep_tidy.csv"
VREST_METRICS_CSV_NAME: str = "vrest_metrics.csv"
WALL_TIME_JSON_NAME: str = "wall_time_by_vrest.json"

VREST_TIDY_T0022: Path = DATA_T0022_DIR / VREST_SWEEP_TIDY_CSV_NAME
VREST_TIDY_T0024: Path = DATA_T0024_DIR / VREST_SWEEP_TIDY_CSV_NAME

VREST_METRICS_T0022: Path = DATA_T0022_DIR / VREST_METRICS_CSV_NAME
VREST_METRICS_T0024: Path = DATA_T0024_DIR / VREST_METRICS_CSV_NAME

WALL_TIME_T0022: Path = DATA_T0022_DIR / WALL_TIME_JSON_NAME
WALL_TIME_T0024: Path = DATA_T0024_DIR / WALL_TIME_JSON_NAME

RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"

# Assets.
ASSETS_DIR: Path = TASK_ROOT / "assets"
PREDICTIONS_DIR: Path = ASSETS_DIR / "predictions"

# Model labels used in asset directories and filenames.
MODEL_LABEL_T0022: str = "t0022"
MODEL_LABEL_T0024: str = "t0024"

# Spike-detection threshold reuse (match each model's constants).
# These are re-imported from the respective model constants inside the trial
# runners; kept here as documentation only.
