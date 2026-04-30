"""Paths for t0064 (HH current-step diagnostic)."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"

VOLTAGE_TRACES_CSV: Path = RESULTS_DIR / "voltage_traces.csv"
SUMMARY_CSV: Path = RESULTS_DIR / "summary.csv"
WALLCLOCK_JSON: Path = RESULTS_DIR / "wallclock.json"

VOLTAGE_GRID_PNG: Path = IMAGES_DIR / "voltage_response_grid.png"
VOLTAGE_OVERLAY_PNG: Path = IMAGES_DIR / "voltage_response_overlay.png"
