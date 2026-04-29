"""Centralized path constants for t0061 (NMDA-only PD diagnostic)."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
CODE_DIR: Path = TASK_ROOT / "code"
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"

MOD_DIR: Path = CODE_DIR / "mod"
MOD_SOURCE: Path = MOD_DIR / "NMDA_MgBlock.mod"
NRNMECH_DLL: Path = MOD_DIR / "nrnmech.dll"
RUN_NRNIVMODL_CMD: Path = CODE_DIR / "run_nrnivmodl.cmd"

VOLTAGE_TRACES_CSV: Path = RESULTS_DIR / "voltage_traces_pd_only.csv"
SUMMARY_CSV: Path = RESULTS_DIR / "summary_pd_only.csv"
WALLCLOCK_JSON: Path = RESULTS_DIR / "wallclock.json"
PLACEMENT_JSON: Path = RESULTS_DIR / "placement_seed0.json"

VOLTAGE_GRID_PNG: Path = IMAGES_DIR / "voltage_response_grid.png"
VOLTAGE_OVERLAY_PNG: Path = IMAGES_DIR / "voltage_response_overlay.png"
