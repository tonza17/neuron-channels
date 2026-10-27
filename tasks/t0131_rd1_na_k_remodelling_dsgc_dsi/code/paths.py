"""Centralised path constants for t0131."""

from pathlib import Path

TASK_ID: str = "t0131_rd1_na_k_remodelling_dsgc_dsi"
_THIS_FILE: Path = Path(__file__).resolve()
CODE_DIR: Path = _THIS_FILE.parent
TASK_ROOT: Path = CODE_DIR.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent
TASKS_DIR: Path = REPO_ROOT / "tasks"

DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"
BUILD_DIR: Path = CODE_DIR / "build"
T0131_DLL: Path = BUILD_DIR / "nrnmech.dll"

# Mechanism libraries.
T0107_DLL: Path = TASKS_DIR / "t0107_t0106_polar_8dir_recheck" / "code" / "mods" / "nrnmech.dll"
T0024_DLL: Path = (
    TASKS_DIR
    / "t0024_port_de_rosenroll_2026_dsgc"
    / "assets"
    / "library"
    / "de_rosenroll_2026_dsgc"
    / "sources"
    / "nrnmech.dll"
)

# Reference-cell sources (t0121 parquet and the four evaluation dumps).
T0121_PARQUET: Path = (
    TASKS_DIR
    / "t0121_5seed_substrate_rate_canonical_report"
    / "results"
    / "data"
    / "pooled_legit_jointpass_cells.parquet"
)
EVAL_DUMP_PATHS: dict[str, Path] = {
    "t0106_seed44": TASKS_DIR
    / "t0106_long_pdnd_nsga2_300gen"
    / "results"
    / "data"
    / "all_evaluations_seed44.json.gz",
    "t0112_seed77": TASKS_DIR
    / "t0112_t0106_seed77_replicate"
    / "results"
    / "data"
    / "all_evaluations_seed77.json.gz",
    "t0114_seed7755": TASKS_DIR
    / "t0114_seed7755_no_autostop"
    / "results"
    / "data"
    / "all_evaluations_seed7755.json",
    "t0115_seed9354": TASKS_DIR
    / "t0115_seed9354_no_autostop"
    / "results"
    / "data"
    / "all_evaluations_seed9354.json",
}

# Data outputs.
REFERENCE_CELLS_JSONL: Path = DATA_DIR / "reference_cells.jsonl"
CLAMP_BASELINE_CSV: Path = DATA_DIR / "clamp_baseline.csv"
CLAMP_TRACES_NPZ: Path = DATA_DIR / "clamp_traces.npz"
CLAMP_SENSITIVITY_CSV: Path = DATA_DIR / "clamp_sensitivity_abs40.csv"
CLAMP_GRID_CSV: Path = DATA_DIR / "clamp_grid.csv"
FITTED_SCALINGS_JSON: Path = DATA_DIR / "fitted_scalings.json"
FIT_VERIFY_TRACES_NPZ: Path = DATA_DIR / "clamp_fit_verify_traces.npz"
CC_STEP_SUMMARY_CSV: Path = DATA_DIR / "cc_step_summary.csv"
FI_CURVES_CSV: Path = DATA_DIR / "fi_curves.csv"
CC_COLLAPSE_VERDICT_JSON: Path = DATA_DIR / "cc_collapse_verdict.json"
CC_TRACES_NPZ: Path = DATA_DIR / "cc_traces.npz"
BIAS_TUNING_CSV: Path = DATA_DIR / "bias_tuning.csv"
SPONTANEOUS_SUMMARY_CSV: Path = DATA_DIR / "spontaneous_summary.csv"
CHOSEN_BIAS_JSON: Path = DATA_DIR / "chosen_bias.json"
SPONTANEOUS_TRACES_NPZ: Path = DATA_DIR / "spontaneous_traces.npz"
DSI_RESULTS_CSV: Path = DATA_DIR / "dsi_results.csv"
DSI_TRIALS_JSONL: Path = DATA_DIR / "dsi_trials.jsonl"
CELL_PARAMS_JSONL: Path = DATA_DIR / "cell_params.jsonl"
DSI_STATS_JSON: Path = DATA_DIR / "dsi_stats.json"
DSI_HEATMAP_CSV: Path = DATA_DIR / "dsi_heatmap.csv"
DSI_HEATMAP_TRIALS_JSONL: Path = DATA_DIR / "dsi_heatmap_trials.jsonl"
ARM_DECISION_JSON: Path = DATA_DIR / "arm_decision.json"
TOY_PARAMS_JSON: Path = DATA_DIR / "toy_params.json"
TOY_ANCHOR_CHECK_JSON: Path = DATA_DIR / "toy_anchor_check.json"
PANEL_D_SWEEP_TRIALS_JSONL: Path = DATA_DIR / "panel_d_neuron_sweep_trials.jsonl"
PANEL_D_SWEEP_CSV: Path = DATA_DIR / "panel_d_neuron_sweep.csv"
PANEL_D_PULSE_TRIALS_JSONL: Path = DATA_DIR / "panel_d_neuron_pulse_trials.jsonl"
PANEL_D_PULSES_CSV: Path = DATA_DIR / "panel_d_neuron_pulses.csv"
PANEL_D_VERDICTS_JSON: Path = DATA_DIR / "panel_d_verdicts.json"
PANEL_D_PSTH_NPZ: Path = DATA_DIR / "panel_d_psth.npz"

# Results.
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
COSTS_JSON: Path = RESULTS_DIR / "costs.json"
REMOTE_MACHINES_JSON: Path = RESULTS_DIR / "remote_machines_used.json"
DATA_SUMMARY_JSON: Path = RESULTS_DIR / "data_summary.json"


def with_arm_suffix(*, path: Path, arm: str) -> Path:
    """Return ``path`` unchanged for the base arm, else with an ``_dendritic`` stem suffix."""
    if arm == "soma_ais":
        return path
    return path.with_name(f"{path.stem}_dendritic{path.suffix}")
