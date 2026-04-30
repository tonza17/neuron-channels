"""Path constants for t0065 EPSP/IPSP/FULL protocol on the deposited DSGC."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parents[1]

DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"

VOLTAGE_TRACES_CSV: Path = DATA_DIR / "voltage_traces.csv"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"

VM_FULL_PD_VS_ND_PNG: Path = IMAGES_DIR / "vm_full_pd_vs_nd.png"
EPSP_PD_VS_ND_PNG: Path = IMAGES_DIR / "epsp_pd_vs_nd.png"
IPSP_PD_VS_ND_PNG: Path = IMAGES_DIR / "ipsp_pd_vs_nd.png"
THREE_MODE_PD_OVERLAY_PNG: Path = IMAGES_DIR / "three_mode_pd_overlay.png"
THREE_MODE_ND_OVERLAY_PNG: Path = IMAGES_DIR / "three_mode_nd_overlay.png"
