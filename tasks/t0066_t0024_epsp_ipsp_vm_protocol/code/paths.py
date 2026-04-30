"""Path constants for t0066 (de Rosenroll EPSP/IPSP/FULL protocol)."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0066_t0024_epsp_ipsp_vm_protocol"

DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"

VOLTAGE_TRACES_CSV: Path = DATA_DIR / "voltage_traces.csv"
PER_TRIAL_METRICS_JSON: Path = DATA_DIR / "per_trial_metrics.json"

METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
COSTS_JSON: Path = RESULTS_DIR / "costs.json"
REMOTE_MACHINES_JSON: Path = RESULTS_DIR / "remote_machines_used.json"

VM_FULL_PNG: Path = IMAGES_DIR / "vm_full_pd_vs_nd.png"
EPSP_PNG: Path = IMAGES_DIR / "epsp_pd_vs_nd.png"
IPSP_PNG: Path = IMAGES_DIR / "ipsp_pd_vs_nd.png"
THREE_MODE_PD_PNG: Path = IMAGES_DIR / "three_mode_pd_overlay.png"
THREE_MODE_ND_PNG: Path = IMAGES_DIR / "three_mode_nd_overlay.png"
COMPARISON_T0065_T0066_PNG: Path = IMAGES_DIR / "comparison_t0065_vs_t0066_ipsp.png"

T0065_VOLTAGE_TRACES_CSV: Path = (
    REPO_ROOT / "tasks" / "t0065_t0020_epsp_ipsp_vm_protocol" / "data" / "voltage_traces.csv"
)
