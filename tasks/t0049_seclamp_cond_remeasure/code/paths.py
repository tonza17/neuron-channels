"""Centralised path constants for t0049 (SEClamp conductance re-measurement).

Anchored to the task root via ``Path(__file__).resolve().parent.parent`` so the module works
whether invoked from the repo root or from inside the worktree. Pattern copied from t0047's
``code/paths.py``.
"""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent

TASK_ID: str = "t0049_seclamp_cond_remeasure"
ANSWER_ID: str = "seclamp-conductance-remeasurement-fig3"

# Top-level task subdirectories.
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
ASSETS_DIR: Path = TASK_ROOT / "assets"
ASSETS_ANSWER_DIR: Path = ASSETS_DIR / "answer" / ANSWER_ID
LOGS_DIR: Path = TASK_ROOT / "logs"

# Per-CSV / per-JSON file locations.
SECLAMP_TRIALS_CSV: Path = RESULTS_DATA_DIR / "seclamp_trials.csv"
SECLAMP_COMPARISON_CSV: Path = RESULTS_DATA_DIR / "seclamp_comparison_table.csv"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"

# PNG outputs.
SECLAMP_PD_VS_ND_PNG: Path = RESULTS_IMAGES_DIR / "seclamp_conductance_pd_vs_nd.png"
SECLAMP_MODALITY_PNG: Path = (
    RESULTS_IMAGES_DIR / "seclamp_vs_per_syn_direct_modality_comparison.png"
)

# Answer asset files.
ANSWER_DETAILS_JSON: Path = ASSETS_ANSWER_DIR / "details.json"
ANSWER_SHORT_MD: Path = ASSETS_ANSWER_DIR / "short_answer.md"
ANSWER_FULL_MD: Path = ASSETS_ANSWER_DIR / "full_answer.md"


# Ensure output dirs exist at module-load time. mkdir is idempotent.
RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_ANSWER_DIR.mkdir(parents=True, exist_ok=True)
