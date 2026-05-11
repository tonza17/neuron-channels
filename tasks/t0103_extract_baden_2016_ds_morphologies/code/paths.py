"""Centralized path constants for t0103."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = TASK_ROOT / "data"
CODE_DIR: Path = TASK_ROOT / "code"
ASSETS_DIR: Path = TASK_ROOT / "assets"
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
INTERVENTION_DIR: Path = TASK_ROOT / "intervention"

VISUALIZATION_CODE_DIR: Path = DATA_DIR / "visualization_code"
DOWNLOAD_MANIFEST_PATH: Path = DATA_DIR / "download_manifest.json"
VISUALIZATION_ZIP_PATH: Path = DATA_DIR / "Baden_et_al_2016_visualization.zip"

# Source .mat (gitignored at the repo root because of size — ~426 MB).
BADEN_MAT_PATH: Path = DATA_DIR / "BadenEtAl_RGCs_2016_v1.mat"
BADEN_README_PDF_PATH: Path = DATA_DIR / "README_for_BadenEtAl_RGCs_2016_v1.pdf"

# Paper asset paths.
PAPER_ASSET_DIR: Path = ASSETS_DIR / "paper" / "10.1038_nature16468"
PAPER_DETAILS_PATH: Path = PAPER_ASSET_DIR / "details.json"
PAPER_SUMMARY_PATH: Path = PAPER_ASSET_DIR / "summary.md"
PAPER_PDF_PATH: Path = PAPER_ASSET_DIR / "files" / "baden_2016_functional_diversity_rgc.pdf"
PAPER_XML_PATH: Path = DATA_DIR / "baden_2016_fulltext.xml"
PAPER_TYPST_PATH: Path = DATA_DIR / "baden_2016_paper.typ"

# Dataset asset paths.
DATASET_ASSET_DIR: Path = ASSETS_DIR / "dataset" / "baden-2016-ds-cells"
DATASET_DETAILS_PATH: Path = DATASET_ASSET_DIR / "details.json"
DATASET_DESCRIPTION_PATH: Path = DATASET_ASSET_DIR / "description.md"
DATASET_FILES_DIR: Path = DATASET_ASSET_DIR / "files"
DATASET_OUT_PARQUET_PATH: Path = DATASET_FILES_DIR / "baden-2016-ds-cells.parquet"

# Code artefacts.
VISUALIZATION_NOTES_PATH: Path = CODE_DIR / "visualization_code_notes.md"
GROUP_COUNT_CHECK_PATH: Path = CODE_DIR / "group_count_check.json"
REQ_COMPLETION_PATH: Path = CODE_DIR / "REQ_COMPLETION.md"

# Result charts.
CELL_COUNTS_IPL_PNG_PATH: Path = RESULTS_IMAGES_DIR / "cell_counts_and_ipl.png"
REPRESENTATIVE_TRACES_PNG_PATH: Path = RESULTS_IMAGES_DIR / "representative_traces.png"
