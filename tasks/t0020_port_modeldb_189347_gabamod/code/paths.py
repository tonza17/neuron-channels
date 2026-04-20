"""Centralized path constants for the t0020 gabaMOD-swap port."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0020_port_modeldb_189347_gabamod"
LIBRARY_ID: str = "modeldb_189347_dsgc_gabamod"

# Asset folders.
LIBRARY_ASSET_DIR: Path = TASK_ROOT / "assets" / "library" / LIBRARY_ID
LIBRARY_DETAILS_JSON: Path = LIBRARY_ASSET_DIR / "details.json"
LIBRARY_DESCRIPTION_MD: Path = LIBRARY_ASSET_DIR / "description.md"

# Task data outputs.
DATA_DIR: Path = TASK_ROOT / "data"
TUNING_CURVES_CSV: Path = DATA_DIR / "tuning_curves.csv"

# Task results outputs.
RESULTS_DIR: Path = TASK_ROOT / "results"
SCORE_REPORT_JSON: Path = RESULTS_DIR / "score_report.json"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
IMAGES_DIR: Path = RESULTS_DIR / "images"
PD_VS_ND_PNG: Path = IMAGES_DIR / "pd_vs_nd_firing_rate.png"

# Code paths (for reference).
CODE_DIR: Path = TASK_ROOT / "code"
CONSTANTS_PY: Path = CODE_DIR / "constants.py"
PATHS_PY: Path = CODE_DIR / "paths.py"
RUN_GABAMOD_SWEEP_PY: Path = CODE_DIR / "run_gabamod_sweep.py"
SCORE_ENVELOPE_PY: Path = CODE_DIR / "score_envelope.py"
PLOT_PD_VS_ND_PY: Path = CODE_DIR / "plot_pd_vs_nd.py"
