"""Canonical path constants and CSV column name constants for tuning_curve_loss."""

from __future__ import annotations

from pathlib import Path

# Repo root: tasks/t0012_.../code/tuning_curve_loss/paths.py -> 4 parents up = repo root.
_THIS_FILE: Path = Path(__file__).resolve()
REPO_ROOT: Path = _THIS_FILE.parent.parent.parent.parent.parent

# Current task root.
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0012_tuning_curve_scoring_loss_library"

# Upstream t0004 target dataset.
TARGET_DATASET_DIR: Path = (
    REPO_ROOT
    / "tasks"
    / "t0004_generate_target_tuning_curve"
    / "assets"
    / "dataset"
    / "target-tuning-curve"
    / "files"
)
TARGET_MEAN_CSV: Path = TARGET_DATASET_DIR / "curve_mean.csv"
TARGET_TRIALS_CSV: Path = TARGET_DATASET_DIR / "curve_trials.csv"
TARGET_GENERATOR_PARAMS_JSON: Path = TARGET_DATASET_DIR / "generator_params.json"

# CSV column name constants.
# Canonical library schema (per task_description.md) uses trial_seed naming,
# but t0004 emits trial_index. Loader accepts either.
ANGLE_COLUMN: str = "angle_deg"
FIRING_RATE_COLUMN: str = "firing_rate_hz"
TRIAL_SEED_COLUMN: str = "trial_seed"

# t0004 mean-curve schema.
MEAN_RATE_COLUMN: str = "mean_rate_hz"
# t0004 trials-curve schema.
TRIAL_INDEX_COLUMN: str = "trial_index"
TRIAL_RATE_COLUMN: str = "rate_hz"

# Canonical trial schema per task_description.md.
TUNING_CURVE_CSV_COLUMNS: tuple[str, str, str] = (
    ANGLE_COLUMN,
    TRIAL_SEED_COLUMN,
    FIRING_RATE_COLUMN,
)
# Legacy two-column schema (t0004 curve_mean.csv).
MEAN_CURVE_CSV_COLUMNS: tuple[str, str] = (ANGLE_COLUMN, MEAN_RATE_COLUMN)

# Grid constants.
N_ANGLES: int = 12
ANGLE_STEP_DEG: float = 30.0
