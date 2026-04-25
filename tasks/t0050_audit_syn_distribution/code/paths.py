"""Centralised path constants for t0050 (audit synapse spatial distribution).

Anchored to the task root via ``Path(__file__).resolve().parent.parent`` so the module works
whether invoked from the repo root or from inside the worktree. Pattern copied from t0049's
``code/paths.py``.
"""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent

TASK_ID: str = "t0050_audit_syn_distribution"
ANSWER_ID: str = "synapse-distribution-audit-deposited-vs-paper"

# Top-level task subdirectories.
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
ASSETS_DIR: Path = TASK_ROOT / "assets"
ASSETS_ANSWER_DIR: Path = ASSETS_DIR / "answer" / ANSWER_ID
LOGS_DIR: Path = TASK_ROOT / "logs"

# CSV outputs.
SYNAPSE_COORDINATES_CSV: Path = RESULTS_DIR / "synapse_coordinates.csv"
PER_CHANNEL_DENSITY_STATS_CSV: Path = RESULTS_DIR / "per_channel_density_stats.csv"

# Metrics JSON.
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"

# PNG outputs.
SYN_X_HIST_PNG: Path = RESULTS_IMAGES_DIR / "syn_x_hist_per_channel.png"
SYN_RADIAL_HIST_PNG: Path = RESULTS_IMAGES_DIR / "syn_radial_distance_per_channel.png"
SYN_COUNT_BAR_PNG: Path = RESULTS_IMAGES_DIR / "syn_count_pd_vs_nd_per_channel.png"

# Answer asset files.
ANSWER_DETAILS_JSON: Path = ASSETS_ANSWER_DIR / "details.json"
ANSWER_SHORT_MD: Path = ASSETS_ANSWER_DIR / "short_answer.md"
ANSWER_FULL_MD: Path = ASSETS_ANSWER_DIR / "full_answer.md"


# Ensure output dirs exist at module-load time. mkdir is idempotent.
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_ANSWER_DIR.mkdir(parents=True, exist_ok=True)
