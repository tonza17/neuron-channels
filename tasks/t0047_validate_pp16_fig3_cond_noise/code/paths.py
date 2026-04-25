"""Centralised path constants for t0047.

Anchored to the task root via ``Path(__file__).resolve().parent.parent`` so the
module works whether invoked from the repo root or from inside the worktree.
"""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent

# Top-level task subdirectories.
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
ASSETS_DIR: Path = TASK_ROOT / "assets"
ASSETS_ANSWER_DIR: Path = ASSETS_DIR / "answer" / "polegpolsky-2016-fig3-conductances-validation"
LOGS_DIR: Path = TASK_ROOT / "logs"

# Per-CSV / per-JSON file locations.
GNMDA_TRIALS_CSV: Path = RESULTS_DATA_DIR / "gnmda_sweep_trials.csv"
NOISE_TRIALS_CSV: Path = RESULTS_DATA_DIR / "noise_extension_trials.csv"
PSP_TRACES_CSV: Path = RESULTS_DATA_DIR / "psp_traces_fig3f_top.csv"
CONDUCTANCE_TABLE_CSV: Path = RESULTS_DATA_DIR / "conductance_comparison_table.csv"
DSI_BY_GNMDA_JSON: Path = RESULTS_DATA_DIR / "dsi_by_gnmda.json"
DSI_AUC_BY_COND_NOISE_JSON: Path = RESULTS_DATA_DIR / "dsi_auc_by_condition_noise.json"

METRICS_JSON: Path = RESULTS_DIR / "metrics.json"

# PNG outputs.
FIG3A_PNG: Path = RESULTS_IMAGES_DIR / "fig3a_nmda_conductance_pd_vs_nd.png"
FIG3B_PNG: Path = RESULTS_IMAGES_DIR / "fig3b_ampa_conductance_pd_vs_nd.png"
FIG3C_PNG: Path = RESULTS_IMAGES_DIR / "fig3c_gaba_conductance_pd_vs_nd.png"
FIG3F_TOP_PNG: Path = RESULTS_IMAGES_DIR / "fig3f_top_psp_traces.png"
FIG3F_BOTTOM_PNG: Path = RESULTS_IMAGES_DIR / "fig3f_bottom_dsi_vs_gnmda.png"
FIG6_PNG: Path = RESULTS_IMAGES_DIR / "fig6_dsi_vs_noise_per_condition.png"
FIG7_PNG: Path = RESULTS_IMAGES_DIR / "fig7_auc_vs_noise_per_condition.png"
