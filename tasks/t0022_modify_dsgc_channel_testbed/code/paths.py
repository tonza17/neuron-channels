"""Centralized path constants for the t0022 DSGC dendritic-computation port."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0022_modify_dsgc_channel_testbed"
LIBRARY_ID: str = "modeldb_189347_dsgc_dendritic"

# Asset folders.
LIBRARY_ASSET_DIR: Path = TASK_ROOT / "assets" / "library" / LIBRARY_ID
LIBRARY_DETAILS_JSON: Path = LIBRARY_ASSET_DIR / "details.json"
LIBRARY_DESCRIPTION_MD: Path = LIBRARY_ASSET_DIR / "description.md"

# ModelDB 189347 sources (reused from the t0008 library asset).
T0008_TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0008_port_modeldb_189347"
T0008_LIBRARY_ASSET_DIR: Path = T0008_TASK_ROOT / "assets" / "library" / "modeldb_189347_dsgc"
T0008_MODELDB_SOURCES_DIR: Path = T0008_LIBRARY_ASSET_DIR / "sources"

# Build directory for the freshly compiled nrnmech.dll against the
# bundled MOD files. We rebuild inside the t0022 task root so this
# worktree does not mutate the t0008 folder.
BUILD_DIR: Path = TASK_ROOT / "build"
MODELDB_BUILD_DIR: Path = BUILD_DIR / "modeldb_189347"
MODELDB_NRNMECH_DLL: Path = MODELDB_BUILD_DIR / "nrnmech.dll"
MODELDB_BUILD_LOG: Path = MODELDB_BUILD_DIR / "build_log.txt"

# Task data outputs.
DATA_DIR: Path = TASK_ROOT / "data"
TUNING_CURVES_DIR: Path = DATA_DIR / "tuning_curves"
TUNING_CURVE_DENDRITIC_CSV: Path = TUNING_CURVES_DIR / "curve_modeldb_189347_dendritic.csv"
SCORE_REPORT_JSON: Path = DATA_DIR / "score_report.json"

# Preflight / debugging output.
PREFLIGHT_DIR: Path = TASK_ROOT / "logs" / "preflight"
PREFLIGHT_ONSETS_JSON: Path = PREFLIGHT_DIR / "onsets.json"
PREFLIGHT_TRACE_CSV: Path = PREFLIGHT_DIR / "preflight_trace.csv"
PREFLIGHT_CURVE_CSV: Path = PREFLIGHT_DIR / "preflight_curve.csv"

# Task results.
RESULTS_DIR: Path = TASK_ROOT / "results"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
IMAGES_DIR: Path = RESULTS_DIR / "images"
TUNING_CURVE_PNG: Path = IMAGES_DIR / "tuning_curve_dendritic.png"

# Code paths (for module_paths in details.json).
CODE_DIR: Path = TASK_ROOT / "code"
CONSTANTS_PY: Path = CODE_DIR / "constants.py"
PATHS_PY: Path = CODE_DIR / "paths.py"
NEURON_BOOTSTRAP_PY: Path = CODE_DIR / "neuron_bootstrap.py"
RUN_TUNING_CURVE_PY: Path = CODE_DIR / "run_tuning_curve.py"
SCORE_ENVELOPE_PY: Path = CODE_DIR / "score_envelope.py"
CHANNEL_PARTITION_HOC: Path = CODE_DIR / "dsgc_channel_partition.hoc"

# HOC path-safe string (forward slashes on Windows).
T0008_SOURCES_HOC_SAFE: str = str(T0008_MODELDB_SOURCES_DIR).replace("\\", "/")
CHANNEL_PARTITION_HOC_SAFE: str = str(CHANNEL_PARTITION_HOC).replace("\\", "/")
