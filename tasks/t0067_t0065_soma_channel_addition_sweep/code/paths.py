"""Path constants for t0067 channel-density sweep."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0067_t0065_soma_channel_addition_sweep"

DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"

CODE_DIR: Path = TASK_ROOT / "code"
T67_NRNMECH_DLL: Path = CODE_DIR / "build" / "nrnmech.dll"

PER_TRIAL_METRICS_JSON: Path = DATA_DIR / "per_trial_metrics.json"
DSI_BY_CONDITION_JSON: Path = DATA_DIR / "dsi_by_condition.json"

METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
COSTS_JSON: Path = RESULTS_DIR / "costs.json"
REMOTE_MACHINES_JSON: Path = RESULTS_DIR / "remote_machines_used.json"

FIRING_RATE_PNG: Path = IMAGES_DIR / "firing_rate_vs_density.png"
DSI_PNG: Path = IMAGES_DIR / "dsi_vs_density.png"
HEATMAP_PNG: Path = IMAGES_DIR / "spike_count_heatmap.png"
