"""Centralized path constants for t0055 (Mg-block NMDA DSI recovery; minimal DSGC).

All file paths used by simulation drivers, analysis scripts, and figure renderers are defined here
per the project Python style guide. No code outside this module hardcodes paths.

This is the t0054 paths file with:

* TASK_ID and LIBRARY_ID rebound to t0055 / minimal_dsgc_mg_block_nmda.
* The placement and gNMDA=0 regression references rebound from t0052 to t0054
  (T0054_PLACEMENT_JSON, T0054_TUNING_CURVE_FULL_CSV).
* Three new constants for the NMDA_MgBlock MOD build (NMDA_MOD_DIR, NRNMECH_DLL,
  RUN_NRNIVMODL_CMD).
* One new sweep-summary PNG path (MG_BLOCK_G_V_PNG).
* One new validation-gate output JSON (MG_BLOCK_G_V_EMPIRICAL_JSON).
"""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0055_nmda_mg_block_dsi_recovery"
LIBRARY_ID: str = "minimal_dsgc_mg_block_nmda"

# Code, results, images.
CODE_DIR: Path = TASK_ROOT / "code"
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"

# Library asset.
LIBRARY_ASSET_DIR: Path = TASK_ROOT / "assets" / "library" / LIBRARY_ID
LIBRARY_DETAILS_JSON: Path = LIBRARY_ASSET_DIR / "details.json"
LIBRARY_DESCRIPTION_MD: Path = LIBRARY_ASSET_DIR / "description.md"

# MOD build directory and outputs.
NMDA_MOD_DIR: Path = CODE_DIR / "mod"
NMDA_MOD_SOURCE: Path = NMDA_MOD_DIR / "NMDA_MgBlock.mod"
NRNMECH_DLL: Path = NMDA_MOD_DIR / "nrnmech.dll"
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

# t0054 placement and gNMDA=0 tuning curve (used for placement-match and gNMDA=0 regression
# gates). Reference rebound from t0052 (used by t0054) to t0054 (used by t0055).
T0054_PLACEMENT_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0054_minimal_dsgc_ampa_nmda_scalar_gaba"
    / "results"
    / "placement_seed0.json"
)
T0054_TUNING_CURVE_FULL_CSV: Path = (
    REPO_ROOT
    / "tasks"
    / "t0054_minimal_dsgc_ampa_nmda_scalar_gaba"
    / "results"
    / "tuning_curve_full.csv"
)
T0054_DERIVED_QUANTITIES_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0054_minimal_dsgc_ampa_nmda_scalar_gaba"
    / "results"
    / "derived_quantities.json"
)

# NEURON install (validated by t0007).
NEURONHOME_DEFAULT: str = r"C:\Users\md1avn\nrn-8.2.7"

# Tuning-curve CSV outputs (one per mode; rows from all four gNMDA values are appended into
# the same per-mode CSV with a `gnmda_ns` column).
TUNING_CURVE_FULL_CSV: Path = RESULTS_DIR / "tuning_curve_full.csv"
TUNING_CURVE_E_ONLY_CSV: Path = RESULTS_DIR / "tuning_curve_e_only.csv"
TUNING_CURVE_GABA_ONLY_CSV: Path = RESULTS_DIR / "tuning_curve_gaba_only.csv"

# Spike times CSV.
SPIKE_TIMES_FULL_CSV: Path = RESULTS_DIR / "spike_times_full.csv"
SPIKE_TIMES_E_ONLY_CSV: Path = RESULTS_DIR / "spike_times_e_only.csv"
SPIKE_TIMES_GABA_ONLY_CSV: Path = RESULTS_DIR / "spike_times_gaba_only.csv"

# Voltage trace CSVs (long form).
VOLTAGE_TRACES_FULL_CSV: Path = RESULTS_DIR / "voltage_traces_full.csv"
VOLTAGE_TRACES_E_ONLY_CSV: Path = RESULTS_DIR / "voltage_traces_e_only.csv"
VOLTAGE_TRACES_GABA_ONLY_CSV: Path = RESULTS_DIR / "voltage_traces_gaba_only.csv"

# Activation times (synapse onset times) CSV; produced from FULL mode (mode-independent).
ACTIVATION_TIMES_CSV: Path = RESULTS_DIR / "activation_times.csv"

# Placement metadata.
PLACEMENT_JSON: Path = RESULTS_DIR / "placement_seed0.json"

# Metrics outputs.
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
DERIVED_QUANTITIES_JSON: Path = RESULTS_DIR / "derived_quantities.json"

# Wall-clock log written at end of full sweep.
WALLCLOCK_JSON: Path = RESULTS_DIR / "wallclock.json"

# Mg-block g(v) sanity-test empirical output (six (v_clamp_mv, peak_g) pairs from Step 13).
MG_BLOCK_G_V_EMPIRICAL_JSON: Path = RESULTS_DIR / "mg_block_g_v_empirical.json"

# Sweep-summary plots (one each, written by render_figures).
EPSP_DECAY_VS_GNMDA_PNG: Path = IMAGES_DIR / "epsp_decay_vs_gnmda.png"
PEAK_HZ_VS_GNMDA_PNG: Path = IMAGES_DIR / "peak_hz_vs_gnmda.png"
DSI_VS_GNMDA_PNG: Path = IMAGES_DIR / "dsi_vs_gnmda.png"
MG_BLOCK_G_V_PNG: Path = IMAGES_DIR / "mg_block_g_v_curve.png"
