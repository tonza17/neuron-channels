"""Path constants for the t0035 distal-dendrite diameter sweep task on the t0024 DSGC port.

All filesystem paths used by the sweep driver, metrics reducer, classifier, and plot scripts are
centralised here per the project Python style guide. Paths are anchored relative to this file so
that the task runs correctly regardless of the current working directory.
"""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0035_distal_dendrite_diameter_sweep_t0024"

RESULTS_DIR: Path = TASK_ROOT / "results"
DATA_DIR: Path = RESULTS_DIR / "data"
PER_DIAMETER_DIR: Path = DATA_DIR / "per_diameter"
IMAGES_DIR: Path = RESULTS_DIR / "images"

LOGS_DIR: Path = TASK_ROOT / "logs"
LOGS_PREFLIGHT_DIR: Path = LOGS_DIR / "preflight"

SWEEP_CSV: Path = DATA_DIR / "sweep_results.csv"
WALL_TIME_JSON: Path = DATA_DIR / "wall_time_by_diameter.json"
METRICS_PER_DIAMETER_CSV: Path = DATA_DIR / "metrics_per_diameter.csv"
DSI_BY_DIAMETER_CSV: Path = DATA_DIR / "dsi_by_diameter.csv"
METRICS_NOTES_JSON: Path = DATA_DIR / "metrics_notes.json"
CURVE_SHAPE_JSON: Path = DATA_DIR / "curve_shape.json"
SLOPE_CLASSIFICATION_JSON: Path = DATA_DIR / "slope_classification.json"
DISTAL_SECTIONS_JSON: Path = LOGS_PREFLIGHT_DIR / "distal_sections.json"

METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
DSI_VS_DIAMETER_PNG: Path = IMAGES_DIR / "dsi_vs_diameter.png"
VECTOR_SUM_DSI_VS_DIAMETER_PNG: Path = IMAGES_DIR / "vector_sum_dsi_vs_diameter.png"
POLAR_OVERLAY_PNG: Path = IMAGES_DIR / "polar_overlay.png"
PEAK_HZ_VS_DIAMETER_PNG: Path = IMAGES_DIR / "peak_hz_vs_diameter.png"


def per_diameter_curve_csv(*, multiplier: float) -> Path:
    """Return the canonical per-diameter tuning-curve CSV path for a given multiplier."""
    label: str = _multiplier_label(multiplier=multiplier)
    return PER_DIAMETER_DIR / f"tuning_curve_D{label}.csv"


def polar_png(*, multiplier: float) -> Path:
    """Return the per-diameter diagnostic polar plot path."""
    label: str = _multiplier_label(multiplier=multiplier)
    return IMAGES_DIR / f"polar_D{label}.png"


def _multiplier_label(*, multiplier: float) -> str:
    """Return a safe filename label for a float multiplier (e.g. 0.5 -> ``0p50``)."""
    formatted: str = f"{multiplier:.2f}"
    return formatted.replace(".", "p")
