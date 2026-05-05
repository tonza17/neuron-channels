"""Centralised path constants for task t0084_t0081_cell_767_vm_trace_deepdive."""

from __future__ import annotations

from pathlib import Path

_THIS_FILE: Path = Path(__file__).resolve()
TASK_ROOT: Path = _THIS_FILE.parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

ALL_EVALUATIONS_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0081_bedb_v3_warmstart_nsga2"
    / "results"
    / "data"
    / "all_evaluations.json"
)

RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
COSTS_JSON: Path = RESULTS_DIR / "costs.json"
REMOTE_MACHINES_JSON: Path = RESULTS_DIR / "remote_machines_used.json"

ANSWER_DIR: Path = (
    TASK_ROOT / "assets" / "answer" / "cell-767-dendritic-spike-mechanism-attribution"
)


def ensure_directories() -> None:
    """Create all output directories (idempotent)."""
    for d in (RESULTS_DATA_DIR, RESULTS_IMAGES_DIR, ANSWER_DIR):
        d.mkdir(parents=True, exist_ok=True)
