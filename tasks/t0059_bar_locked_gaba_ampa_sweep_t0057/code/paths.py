"""Centralized path constants for t0059 (bar-arrival-locked tonic GABA + AMPA sweep).

Adapted from ``tasks/t0057_tonic_gaba_sweep_t0053/code/paths.py``. Per-mode CSV constants are
renamed from ``ampa_only`` / ``gaba_only`` to ``epsp_passive`` / ``ipsp_passive`` per the
S-0055-01 measurement-protocol fix. ``ACTIVATION_TIMES_CSV`` is dropped (not produced by t0059).
``T0057_PLACEMENT_JSON`` references the parent task's seed-0 placement file for the bit-identity
test (REQ-16). The cross-grid heatmap output paths are added.
"""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0059_bar_locked_gaba_ampa_sweep_t0057"
LIBRARY_ID: str = "minimal_dsgc_bar_locked_gaba_ampa_sweep"

# Code, results, images.
CODE_DIR: Path = TASK_ROOT / "code"
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"

# Library asset.
LIBRARY_ASSET_DIR: Path = TASK_ROOT / "assets" / "library" / LIBRARY_ID
LIBRARY_DETAILS_JSON: Path = LIBRARY_ASSET_DIR / "details.json"
LIBRARY_DESCRIPTION_MD: Path = LIBRARY_ASSET_DIR / "description.md"

# MOD build directory and outputs (mirror t0057 pattern).
MOD_DIR: Path = CODE_DIR / "mod"
MOD_SOURCE: Path = MOD_DIR / "GabaTonic.mod"
NRNMECH_DLL: Path = MOD_DIR / "nrnmech.dll"
RUN_NRNIVMODL_CMD: Path = CODE_DIR / "run_nrnivmodl.cmd"

# Test data directory (for HH save-and-zero reference trace).
TEST_DATA_DIR: Path = CODE_DIR / "test_data"
HH_REFERENCE_TRACE_NPY: Path = TEST_DATA_DIR / "full_reference_trace.npy"

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

# t0057 placement (bit-identity test reference; t0057 itself matched t0053 / t0052).
T0057_PLACEMENT_JSON: Path = (
    REPO_ROOT / "tasks" / "t0057_tonic_gaba_sweep_t0053" / "results" / "placement_seed0.json"
)

# NEURON install (validated by t0007).
NEURONHOME_DEFAULT: str = r"C:\Users\md1avn\nrn-8.2.7"

# Tuning-curve CSV outputs (one per mode; rows for all 25 (gampa, gaba) cells are appended into
# the same per-mode CSV with leading ``gampa_ns`` / ``gaba_base_ns`` columns).
TUNING_CURVE_FULL_CSV: Path = RESULTS_DIR / "tuning_curve_full.csv"
TUNING_CURVE_EPSP_PASSIVE_CSV: Path = RESULTS_DIR / "tuning_curve_epsp_passive.csv"
TUNING_CURVE_IPSP_PASSIVE_CSV: Path = RESULTS_DIR / "tuning_curve_ipsp_passive.csv"

# Spike times CSV.
SPIKE_TIMES_FULL_CSV: Path = RESULTS_DIR / "spike_times_full.csv"
SPIKE_TIMES_EPSP_PASSIVE_CSV: Path = RESULTS_DIR / "spike_times_epsp_passive.csv"
SPIKE_TIMES_IPSP_PASSIVE_CSV: Path = RESULTS_DIR / "spike_times_ipsp_passive.csv"

# Voltage trace CSVs (long form).
VOLTAGE_TRACES_FULL_CSV: Path = RESULTS_DIR / "voltage_traces_full.csv"
VOLTAGE_TRACES_EPSP_PASSIVE_CSV: Path = RESULTS_DIR / "voltage_traces_epsp_passive.csv"
VOLTAGE_TRACES_IPSP_PASSIVE_CSV: Path = RESULTS_DIR / "voltage_traces_ipsp_passive.csv"

# Per-direction active fraction CSV (carried over from t0057; conductance-independent).
ACTIVE_FRACTION_CSV: Path = RESULTS_DIR / "active_fraction_per_direction.csv"

# Placement metadata.
PLACEMENT_JSON: Path = RESULTS_DIR / "placement_seed0.json"

# Metrics outputs.
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
DERIVED_QUANTITIES_JSON: Path = RESULTS_DIR / "derived_quantities.json"

# Wall-clock log.
WALLCLOCK_JSON: Path = RESULTS_DIR / "wallclock.json"

# Cross-grid summary heatmap PNGs.
HEATMAP_DSI_PRIMARY_PNG: Path = IMAGES_DIR / "heatmap_dsi_primary.png"
HEATMAP_DSI_VECTOR_SUM_PNG: Path = IMAGES_DIR / "heatmap_dsi_vector_sum.png"
HEATMAP_PEAK_HZ_PNG: Path = IMAGES_DIR / "heatmap_peak_hz.png"
HEATMAP_NULL_HZ_PNG: Path = IMAGES_DIR / "heatmap_null_hz.png"
HEATMAP_HWHM_PNG: Path = IMAGES_DIR / "heatmap_hwhm.png"
HEATMAP_RMSE_PNG: Path = IMAGES_DIR / "heatmap_rmse.png"

# Regime-boundary contour overlay.
REGIME_BOUNDARY_CONTOUR_PNG: Path = IMAGES_DIR / "regime_boundary_contour.png"
