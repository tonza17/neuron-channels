"""Centralized path constants for t0074 channel tuning-width sweep on Bed A."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0074_channel_tuning_width_bed_a"

CODE_DIR: Path = TASK_ROOT / "code"
MODS_DIR: Path = CODE_DIR / "mods"
BUILD_DIR: Path = CODE_DIR / "build"
T74_NRNMECH_DLL: Path = BUILD_DIR / "nrnmech.dll"
FORKED_HOC: Path = CODE_DIR / "dsgc_model_t74.hoc"
RUN_NRNIVMODL_CMD: Path = CODE_DIR / "run_nrnivmodl.cmd"

RESULTS_DIR: Path = TASK_ROOT / "results"
DATA_DIR: Path = RESULTS_DIR / "data"
TUNING_CURVES_DIR: Path = DATA_DIR / "tuning_curves"
IMAGES_DIR: Path = RESULTS_DIR / "images"

PER_TRIAL_FULL_CSV: Path = DATA_DIR / "per_trial_full.csv"
PER_TRIAL_PASSIVE_CSV: Path = DATA_DIR / "per_trial_passive.csv"
TUNING_CURVES_CSV: Path = DATA_DIR / "tuning_curves.csv"

METRICS_SUMMARY_CSV: Path = RESULTS_DIR / "metrics_summary.csv"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
REGRESSION_GATE_JSON: Path = RESULTS_DIR / "regression_gate.json"

# Path to the t0004 cosine target tuning curve.
T0004_TARGET_CSV: Path = (
    REPO_ROOT
    / "tasks"
    / "t0004_generate_target_tuning_curve"
    / "assets"
    / "dataset"
    / "target-tuning-curve"
    / "files"
    / "curve_mean.csv"
)

ASSETS_DIR: Path = TASK_ROOT / "assets"
LIBRARY_ID: str = "dsgc_active_channel_pack"
LIBRARY_DIR: Path = ASSETS_DIR / "library" / LIBRARY_ID
LIBRARY_DETAILS_JSON: Path = LIBRARY_DIR / "details.json"
LIBRARY_DESCRIPTION_MD: Path = LIBRARY_DIR / "description.md"
