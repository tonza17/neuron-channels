"""Repository-relative path constants used by the smoke tests.

Only the smoke tests consume these paths. The plotting functions accept arbitrary
``Path`` arguments; they do not import anything from this module.
"""

from __future__ import annotations

from pathlib import Path

# Repo root: tasks/t0011_.../code/tuning_curve_viz/paths.py -> 4 parents up = repo root.
_THIS_FILE: Path = Path(__file__).resolve()
REPO_ROOT: Path = _THIS_FILE.parent.parent.parent.parent.parent

# Current task root and asset folder (underscored to match Python package name).
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0011_response_visualization_library"
LIBRARY_ASSET_DIR: Path = TASK_ROOT / "assets" / "library" / "tuning_curve_viz"
LIBRARY_ASSET_FILES_DIR: Path = LIBRARY_ASSET_DIR / "files"

# Upstream t0004 target dataset.
T0004_TARGET_DATASET_DIR: Path = (
    REPO_ROOT
    / "tasks"
    / "t0004_generate_target_tuning_curve"
    / "assets"
    / "dataset"
    / "target-tuning-curve"
    / "files"
)
T0004_TARGET_MEAN_CSV: Path = T0004_TARGET_DATASET_DIR / "curve_mean.csv"
T0004_TARGET_TRIALS_CSV: Path = T0004_TARGET_DATASET_DIR / "curve_trials.csv"

# Upstream t0008 simulated curve.
T0008_SIMULATED_CURVE_CSV: Path = (
    REPO_ROOT
    / "tasks"
    / "t0008_port_modeldb_189347"
    / "data"
    / "tuning_curves"
    / "curve_modeldb_189347.csv"
)

# Smoke-test output PNG file names (emitted into LIBRARY_ASSET_FILES_DIR).
SMOKE_TARGET_CARTESIAN_PNG: Path = LIBRARY_ASSET_FILES_DIR / "target_cartesian.png"
SMOKE_TARGET_POLAR_PNG: Path = LIBRARY_ASSET_FILES_DIR / "target_polar.png"
SMOKE_T0008_CARTESIAN_PNG: Path = LIBRARY_ASSET_FILES_DIR / "t0008_cartesian.png"
SMOKE_T0008_POLAR_PNG: Path = LIBRARY_ASSET_FILES_DIR / "t0008_polar.png"
SMOKE_OVERLAY_PNG: Path = LIBRARY_ASSET_FILES_DIR / "overlay_target_vs_t0008.png"
SMOKE_RASTER_PSTH_0_PNG: Path = LIBRARY_ASSET_FILES_DIR / "raster_psth_0deg.png"
SMOKE_RASTER_PSTH_PREF_PNG: Path = LIBRARY_ASSET_FILES_DIR / "raster_psth_90deg.png"
