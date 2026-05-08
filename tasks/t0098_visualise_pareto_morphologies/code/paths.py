"""Centralised Path constants for t0098_visualise_pareto_morphologies."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0098_visualise_pareto_morphologies"

T0091_DATA_DIR: Path = (
    REPO_ROOT / "tasks" / "t0091_morphology_extended_nsga2_v1" / "results" / "data"
)
PARETO_PATH: Path = T0091_DATA_DIR / "pareto_front.json"
ANCHOR_TRACKING_PATH: Path = T0091_DATA_DIR / "anchor_tracking.json"

OUT_IMAGES_DIR: Path = TASK_ROOT / "results" / "images"
GRID_PATH: Path = OUT_IMAGES_DIR / "morphology_grid_57cells.png"
DSI_BAR_PATH: Path = OUT_IMAGES_DIR / "pareto_dsi_bar.png"
PD_BAR_PATH: Path = OUT_IMAGES_DIR / "pareto_pd_bar.png"
SCATTER_PATH: Path = OUT_IMAGES_DIR / "pareto_dsi_vs_pd_scatter.png"
