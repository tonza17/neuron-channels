"""Path constants for the t0037 null-GABA reduction ladder sweep.

All filesystem paths used by the sweep driver, metrics reducer, classifier, and plot scripts are
centralised here per the project Python style guide. Paths are anchored relative to this file so
that the task runs correctly regardless of the current working directory.

Structural clone of ``tasks/t0036_rerun_t0030_halved_null_gaba/code/paths.py`` with chart and
per-sweep-point CSV names reparameterised for a GABA X-axis (nS) instead of a diameter multiplier.
"""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0037_null_gaba_reduction_ladder_t0022"

RESULTS_DIR: Path = TASK_ROOT / "results"
DATA_DIR: Path = RESULTS_DIR / "data"
PER_GABA_DIR: Path = DATA_DIR / "per_gaba"
IMAGES_DIR: Path = RESULTS_DIR / "images"

LOGS_DIR: Path = TASK_ROOT / "logs"
LOGS_PREFLIGHT_DIR: Path = LOGS_DIR / "preflight"

SWEEP_CSV: Path = DATA_DIR / "sweep_results.csv"
WALL_TIME_JSON: Path = DATA_DIR / "wall_time_by_gaba.json"
METRICS_PER_GABA_CSV: Path = DATA_DIR / "metrics_per_gaba.csv"
DSI_BY_GABA_CSV: Path = DATA_DIR / "dsi_by_gaba.csv"
METRICS_NOTES_JSON: Path = DATA_DIR / "metrics_notes.json"
CURVE_SHAPE_JSON: Path = DATA_DIR / "curve_shape.json"
DISTAL_SECTIONS_JSON: Path = LOGS_PREFLIGHT_DIR / "distal_sections.json"

METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
NULL_HZ_VS_GABA_PNG: Path = IMAGES_DIR / "null_hz_vs_gaba.png"
PRIMARY_DSI_VS_GABA_PNG: Path = IMAGES_DIR / "primary_dsi_vs_gaba.png"
VECTOR_SUM_DSI_VS_GABA_PNG: Path = IMAGES_DIR / "vector_sum_dsi_vs_gaba.png"
PEAK_HZ_VS_GABA_PNG: Path = IMAGES_DIR / "peak_hz_vs_gaba.png"
POLAR_OVERLAY_PNG: Path = IMAGES_DIR / "polar_overlay.png"


def per_gaba_curve_csv(*, gaba_null_ns: float) -> Path:
    """Return the canonical per-GABA tuning-curve CSV path for a given conductance value (nS)."""
    label: str = gaba_label(gaba_null_ns=gaba_null_ns)
    return PER_GABA_DIR / f"tuning_curve_G{label}.csv"


def gaba_label(*, gaba_null_ns: float) -> str:
    """Return a safe filename label for a float GABA value (e.g. 0.5 -> ``0p50``)."""
    formatted: str = f"{gaba_null_ns:.2f}"
    return formatted.replace(".", "p")
