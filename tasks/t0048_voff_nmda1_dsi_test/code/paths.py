"""Centralised path constants for t0048.

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
ASSETS_ANSWER_DIR: Path = ASSETS_DIR / "answer" / "dsi-flatness-test-voltage-independent-nmda"
LOGS_DIR: Path = TASK_ROOT / "logs"

# Cross-task baseline data (read-only).
T0047_TASK_ROOT: Path = TASK_ROOT.parent / "t0047_validate_pp16_fig3_cond_noise"
T0047_GNMDA_TRIALS_CSV: Path = T0047_TASK_ROOT / "results" / "data" / "gnmda_sweep_trials.csv"

# This task's output files.
GNMDA_TRIALS_VOFF1_CSV: Path = RESULTS_DATA_DIR / "gnmda_sweep_trials_voff1.csv"
GNMDA_TRIALS_VOFF1_LIMIT_CSV: Path = RESULTS_DATA_DIR / "gnmda_sweep_trials_voff1_limit.csv"
DSI_BY_GNMDA_VOFF1_JSON: Path = RESULTS_DATA_DIR / "dsi_by_gnmda_voff1.json"
DSI_BY_GNMDA_VOFF0_FROM_T0047_JSON: Path = RESULTS_DATA_DIR / "dsi_by_gnmda_voff0_from_t0047.json"
VERDICT_VOFF1_JSON: Path = RESULTS_DATA_DIR / "verdict_voff1.json"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"

# PNG outputs.
DSI_OVERLAY_PNG: Path = RESULTS_IMAGES_DIR / "dsi_vs_gnmda_voff0_vs_voff1.png"
CONDUCTANCE_COMPARISON_PNG: Path = (
    RESULTS_IMAGES_DIR / "conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png"
)
