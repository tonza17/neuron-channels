"""Centralized path constants for t0010_hunt_missed_dsgc_models."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0010_hunt_missed_dsgc_models"

DATA_DIR: Path = TASK_ROOT / "data"
CANDIDATES_CSV: Path = DATA_DIR / "candidates.csv"
TUNING_CURVE_DIR: Path = DATA_DIR / "tuning_curves"

ASSETS_DIR: Path = TASK_ROOT / "assets"
ASSETS_LIBRARY_DIR: Path = ASSETS_DIR / "library"
