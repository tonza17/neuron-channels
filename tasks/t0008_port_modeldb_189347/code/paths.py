"""Centralized path constants for the t0008 ModelDB 189347 port."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0008_port_modeldb_189347"
LIBRARY_ID: str = "modeldb_189347_dsgc"
HANSON_LIBRARY_ID: str = "hanson_2019_spatial_offset_dsgc"
ANSWER_ID: str = "dsgc-modeldb-port-reproduction-report"

# Asset folders.
LIBRARY_ASSET_DIR: Path = TASK_ROOT / "assets" / "library" / LIBRARY_ID
HANSON_LIBRARY_ASSET_DIR: Path = TASK_ROOT / "assets" / "library" / HANSON_LIBRARY_ID
ANSWER_ASSET_DIR: Path = TASK_ROOT / "assets" / "answer" / ANSWER_ID

LIBRARY_DETAILS_JSON: Path = LIBRARY_ASSET_DIR / "details.json"
LIBRARY_DESCRIPTION_MD: Path = LIBRARY_ASSET_DIR / "description.md"
HANSON_DETAILS_JSON: Path = HANSON_LIBRARY_ASSET_DIR / "details.json"
HANSON_DESCRIPTION_MD: Path = HANSON_LIBRARY_ASSET_DIR / "description.md"
ANSWER_DETAILS_JSON: Path = ANSWER_ASSET_DIR / "details.json"
ANSWER_SHORT_MD: Path = ANSWER_ASSET_DIR / "short_answer.md"
ANSWER_FULL_MD: Path = ANSWER_ASSET_DIR / "full_answer.md"

# ModelDB 189347 source archive (cloned as git repo under library asset).
MODELDB_SOURCES_DIR: Path = LIBRARY_ASSET_DIR / "sources"
MODELDB_MAIN_HOC: Path = MODELDB_SOURCES_DIR / "main.hoc"
MODELDB_RGCMODEL_HOC: Path = MODELDB_SOURCES_DIR / "RGCmodel.hoc"
MODELDB_GUI_FREE_HOC: Path = MODELDB_SOURCES_DIR / "dsgc_model.hoc"

# Hanson 2019 sources.
HANSON_SOURCES_DIR: Path = HANSON_LIBRARY_ASSET_DIR / "sources"

# Build directories (compiled MOD files, nrnmech.dll).
BUILD_DIR: Path = TASK_ROOT / "build"
MODELDB_BUILD_DIR: Path = BUILD_DIR / "modeldb_189347"
MODELDB_BUILD_LOG: Path = MODELDB_BUILD_DIR / "build_log.txt"
HANSON_BUILD_DIR: Path = BUILD_DIR / "hanson_2019"
HANSON_BUILD_LOG: Path = HANSON_BUILD_DIR / "build_log.txt"

# On Windows, nrnivmodl emits nrnmech.dll under <builddir>/nrnmech.dll
# (platform-dependent suffix). We discover the DLL via glob at runtime.
MODELDB_NRNMECH_GLOBS: list[str] = [
    "nrnmech.dll",
    "x86_64/.libs/libnrnmech.so",
    "x86_64/libnrnmech.so",
]

# Calibrated DSGC morphology from t0009.
CALIBRATED_SWC_PATH: Path = (
    REPO_ROOT
    / "tasks"
    / "t0009_calibrate_dendritic_diameters"
    / "assets"
    / "dataset"
    / "dsgc-baseline-morphology-calibrated"
    / "files"
    / "141009_Pair1DSGC_calibrated.CNG.swc"
)

# Task data outputs.
DATA_DIR: Path = TASK_ROOT / "data"
TUNING_CURVES_DIR: Path = DATA_DIR / "tuning_curves"
TUNING_CURVE_MODELDB_CSV: Path = TUNING_CURVES_DIR / "curve_modeldb_189347.csv"
TUNING_CURVE_HANSON_CSV: Path = TUNING_CURVES_DIR / "curve_hanson_2019.csv"
SMOKE_TEST_CSV: Path = DATA_DIR / "smoke_test_single_angle.csv"
MORPHOLOGY_SWAP_REPORT: Path = DATA_DIR / "morphology_swap_report.md"
SCORE_REPORT_JSON: Path = DATA_DIR / "score_report.json"
SCORE_REPORT_HANSON_JSON: Path = DATA_DIR / "score_report_hanson.json"
PHASE_B_SURVEY_CSV: Path = DATA_DIR / "phase_b_survey.csv"

# Task results.
RESULTS_DIR: Path = TASK_ROOT / "results"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
IMAGES_DIR: Path = RESULTS_DIR / "images"

# Code paths (for module_paths in details.json).
CODE_DIR: Path = TASK_ROOT / "code"
CONSTANTS_PY: Path = CODE_DIR / "constants.py"
PATHS_PY: Path = CODE_DIR / "paths.py"
BUILD_CELL_PY: Path = CODE_DIR / "build_cell.py"
RUN_TUNING_CURVE_PY: Path = CODE_DIR / "run_tuning_curve.py"
SCORE_ENVELOPE_PY: Path = CODE_DIR / "score_envelope.py"
REPORT_MORPHOLOGY_PY: Path = CODE_DIR / "report_morphology.py"
SWC_IO_PY: Path = CODE_DIR / "swc_io.py"
RUN_NRNIVMODL_CMD: Path = CODE_DIR / "run_nrnivmodl.cmd"
TEST_SMOKE_PY: Path = CODE_DIR / "test_smoke_single_angle.py"
TEST_SCORING_PY: Path = CODE_DIR / "test_scoring_pipeline.py"
