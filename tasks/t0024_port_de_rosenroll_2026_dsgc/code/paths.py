"""Centralized path constants for the t0024 de Rosenroll 2026 DSGC port."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0024_port_de_rosenroll_2026_dsgc"
LIBRARY_ID: str = "de_rosenroll_2026_dsgc"

# Asset folders.
LIBRARY_ASSET_DIR: Path = TASK_ROOT / "assets" / "library" / LIBRARY_ID
LIBRARY_SOURCES_DIR: Path = LIBRARY_ASSET_DIR / "sources"
LIBRARY_DETAILS_JSON: Path = LIBRARY_ASSET_DIR / "details.json"
LIBRARY_DESCRIPTION_MD: Path = LIBRARY_ASSET_DIR / "description.md"
LIBRARY_NRNIVMODL_CMD: Path = LIBRARY_ASSET_DIR / "run_nrnivmodl.cmd"

# Library source files.
RGCMODEL_HOC: Path = LIBRARY_SOURCES_DIR / "RGCmodelGD.hoc"
NRNMECH_DLL: Path = LIBRARY_SOURCES_DIR / "nrnmech.dll"

# Task data outputs.
DATA_DIR: Path = TASK_ROOT / "data"
TUNING_CURVE_8DIR_CORR_CSV: Path = DATA_DIR / "tuning_curves_8dir_correlated.csv"
TUNING_CURVE_8DIR_UNCORR_CSV: Path = DATA_DIR / "tuning_curves_8dir_uncorrelated.csv"
TUNING_CURVE_12ANG_CORR_CSV: Path = DATA_DIR / "tuning_curves_12ang_correlated.csv"
TUNING_CURVE_12ANG_UNCORR_CSV: Path = DATA_DIR / "tuning_curves_12ang_uncorrelated.csv"
TUNING_CURVE_8DIR_CORR_PREFLIGHT_CSV: Path = (
    DATA_DIR / "tuning_curves_8dir_correlated_preflight.csv"
)
SCORE_REPORT_JSON: Path = DATA_DIR / "score_report.json"

# Task results.
RESULTS_DIR: Path = TASK_ROOT / "results"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
IMAGES_DIR: Path = RESULTS_DIR / "images"
TUNING_CURVE_12ANG_PLOT_PNG: Path = IMAGES_DIR / "tuning_curve_12ang.png"
TUNING_CURVE_8DIR_PLOT_PNG: Path = IMAGES_DIR / "tuning_curve_8dir.png"

# Intervention / corrections.
INTERVENTION_DIR: Path = TASK_ROOT / "intervention"
PORT_FIDELITY_MISS_MD: Path = INTERVENTION_DIR / "port_fidelity_miss.md"
