"""Path constants for t0068 Nav1.6+Kv3 co-expression rescue."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0068_t0067_nav16_kv3_coexpression_rescue"

DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"

T68_NRNMECH_DLL: Path = TASK_ROOT / "code" / "build" / "nrnmech.dll"

PER_TRIAL_METRICS_JSON: Path = DATA_DIR / "per_trial_metrics.json"
DSI_BY_CONDITION_JSON: Path = DATA_DIR / "dsi_by_condition.json"

METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
COSTS_JSON: Path = RESULTS_DIR / "costs.json"
REMOTE_MACHINES_JSON: Path = RESULTS_DIR / "remote_machines_used.json"

DSI_RESCUE_PNG: Path = IMAGES_DIR / "dsi_rescue_curve.png"
FIRING_RATE_RESCUE_PNG: Path = IMAGES_DIR / "firing_rate_rescue.png"
