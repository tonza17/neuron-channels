"""Centralized path constants for t0052 (minimal DSGC with scalar gabaMOD).

All file paths used by simulation drivers, analysis scripts, and figure renderers are defined here
per the project Python style guide. No code outside this module hardcodes paths.
"""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0052_minimal_dsgc_scalar_gaba"
LIBRARY_ID: str = "minimal_dsgc_scalar_gaba"

# Code, results, images.
CODE_DIR: Path = TASK_ROOT / "code"
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"

# Library asset.
LIBRARY_ASSET_DIR: Path = TASK_ROOT / "assets" / "library" / LIBRARY_ID
LIBRARY_DETAILS_JSON: Path = LIBRARY_ASSET_DIR / "details.json"
LIBRARY_DESCRIPTION_MD: Path = LIBRARY_ASSET_DIR / "description.md"

# Morphology source (t0009 calibrated SWC).
MORPHOLOGY_SWC_PATH: Path = (
    REPO_ROOT
    / "tasks"
    / "t0009_calibrate_dendritic_diameters"
    / "assets"
    / "dataset"
    / "dsgc-baseline-morphology-calibrated"
    / "files"
    / "141009_Pair1DSGC_calibrated.CNG.swc"
)

# Optional t0004 target tuning curve (used for tuning_curve_rmse if available).
TARGET_TUNING_CURVE_CSV: Path = (
    REPO_ROOT
    / "tasks"
    / "t0004_generate_target_tuning_curve"
    / "assets"
    / "dataset"
    / "target-tuning-curve"
    / "files"
    / "curve_mean.csv"
)
TARGET_TUNING_CURVE_TRIALS_CSV: Path = TARGET_TUNING_CURVE_CSV.parent / "curve_trials.csv"

# NEURON install (validated by t0007).
NEURONHOME_DEFAULT: str = r"C:\Users\md1avn\nrn-8.2.7"

# Tuning-curve CSV outputs (one per mode).
TUNING_CURVE_FULL_CSV: Path = RESULTS_DIR / "tuning_curve_full.csv"
TUNING_CURVE_AMPA_ONLY_CSV: Path = RESULTS_DIR / "tuning_curve_ampa_only.csv"
TUNING_CURVE_GABA_ONLY_CSV: Path = RESULTS_DIR / "tuning_curve_gaba_only.csv"

# Spike times CSV.
SPIKE_TIMES_FULL_CSV: Path = RESULTS_DIR / "spike_times_full.csv"
SPIKE_TIMES_AMPA_ONLY_CSV: Path = RESULTS_DIR / "spike_times_ampa_only.csv"
SPIKE_TIMES_GABA_ONLY_CSV: Path = RESULTS_DIR / "spike_times_gaba_only.csv"

# Voltage trace CSVs (long form).
VOLTAGE_TRACES_FULL_CSV: Path = RESULTS_DIR / "voltage_traces_full.csv"
VOLTAGE_TRACES_AMPA_ONLY_CSV: Path = RESULTS_DIR / "voltage_traces_ampa_only.csv"
VOLTAGE_TRACES_GABA_ONLY_CSV: Path = RESULTS_DIR / "voltage_traces_gaba_only.csv"

# Activation times (synapse onset times) CSV; produced from FULL mode (mode-independent).
ACTIVATION_TIMES_CSV: Path = RESULTS_DIR / "activation_times.csv"

# Placement metadata.
PLACEMENT_JSON: Path = RESULTS_DIR / "placement_seed0.json"

# Metrics outputs.
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
DERIVED_QUANTITIES_JSON: Path = RESULTS_DIR / "derived_quantities.json"
