"""Centralized path constants for t0057 (tonic GABA + amplitude sweep on t0053 spatial DSGC).

Adapted from ``tasks/t0053_minimal_dsgc_spatial_gaba/code/paths.py`` with three additions for the
new ``gaba_tonic.mod`` build pipeline (``MOD_DIR``, ``RUN_NRNIVMODL_CMD``, ``NRNMECH_DLL``) and a
``T0053_PLACEMENT_JSON`` reference for the bit-identity placement test. All file paths used by
simulation drivers, analysis scripts, and figure renderers are defined here per the project Python
style guide.
"""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0057_tonic_gaba_sweep_t0053"
LIBRARY_ID: str = "minimal_dsgc_tonic_gaba_sweep"

# Code, results, images.
CODE_DIR: Path = TASK_ROOT / "code"
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"

# Library asset.
LIBRARY_ASSET_DIR: Path = TASK_ROOT / "assets" / "library" / LIBRARY_ID
LIBRARY_DETAILS_JSON: Path = LIBRARY_ASSET_DIR / "details.json"
LIBRARY_DESCRIPTION_MD: Path = LIBRARY_ASSET_DIR / "description.md"

# MOD build directory and outputs (mirror t0055 pattern).
MOD_DIR: Path = CODE_DIR / "mod"
MOD_SOURCE: Path = MOD_DIR / "GabaTonic.mod"
NRNMECH_DLL: Path = MOD_DIR / "nrnmech.dll"
RUN_NRNIVMODL_CMD: Path = CODE_DIR / "run_nrnivmodl.cmd"

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

# t0004 target tuning curve (used for tuning_curve_rmse).
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

# t0053 placement (bit-identity test reference).
T0053_PLACEMENT_JSON: Path = (
    REPO_ROOT / "tasks" / "t0053_minimal_dsgc_spatial_gaba" / "results" / "placement_seed0.json"
)

# NEURON install (validated by t0007).
NEURONHOME_DEFAULT: str = r"C:\Users\md1avn\nrn-8.2.7"

# Tuning-curve CSV outputs (one per mode; rows for all 5 GABA_BASE_NS values are appended into
# the same per-mode CSV with a `gaba_base_ns` column).
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

# Per-direction active fraction CSV (carried over from t0053; conductance-independent).
ACTIVE_FRACTION_CSV: Path = RESULTS_DIR / "active_fraction_per_direction.csv"

# Placement metadata.
PLACEMENT_JSON: Path = RESULTS_DIR / "placement_seed0.json"

# Metrics outputs.
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
DERIVED_QUANTITIES_JSON: Path = RESULTS_DIR / "derived_quantities.json"

# Wall-clock log.
WALLCLOCK_JSON: Path = RESULTS_DIR / "wallclock.json"

# Cross-conductance summary plots.
DSI_PRIMARY_VS_GABA_PNG: Path = IMAGES_DIR / "dsi_primary_vs_gaba.png"
DSI_VECTOR_SUM_VS_GABA_PNG: Path = IMAGES_DIR / "dsi_vector_sum_vs_gaba.png"
PEAK_HZ_VS_GABA_PNG: Path = IMAGES_DIR / "peak_hz_vs_gaba.png"
NULL_HZ_VS_GABA_PNG: Path = IMAGES_DIR / "null_hz_vs_gaba.png"
HWHM_VS_GABA_PNG: Path = IMAGES_DIR / "hwhm_vs_gaba.png"
RMSE_VS_GABA_PNG: Path = IMAGES_DIR / "rmse_vs_gaba.png"
