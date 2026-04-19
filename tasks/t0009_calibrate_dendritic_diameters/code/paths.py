"""Centralized path constants for the t0009 diameter-calibration pipeline."""

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

DATASET_ID: str = "dsgc-baseline-morphology-calibrated"
SOURCE_DATASET_ID: str = "dsgc-baseline-morphology"
SOURCE_TASK_ID: str = "t0005_download_dsgc_morphology"

SOURCE_SWC_PATH: Path = (
    REPO_ROOT
    / "tasks"
    / SOURCE_TASK_ID
    / "assets"
    / "dataset"
    / SOURCE_DATASET_ID
    / "files"
    / "141009_Pair1DSGC.CNG.swc"
)

DATASET_ASSET_DIR: Path = TASK_ROOT / "assets" / "dataset" / DATASET_ID
FILES_DIR: Path = DATASET_ASSET_DIR / "files"
DETAILS_JSON_PATH: Path = DATASET_ASSET_DIR / "details.json"
DESCRIPTION_MD_PATH: Path = DATASET_ASSET_DIR / "description.md"
CALIBRATED_SWC_PATH: Path = FILES_DIR / "141009_Pair1DSGC_calibrated.CNG.swc"

POLEG_POLSKY_HOC_PATH: Path = TASK_ROOT / "data" / "RGCmodel.hoc"
POLEG_POLSKY_BINS_JSON_PATH: Path = TASK_ROOT / "data" / "poleg_polsky_bins.json"
CALIBRATION_RECORDS_JSON_PATH: Path = TASK_ROOT / "data" / "calibration_records.json"

RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"
METRICS_JSON_PATH: Path = RESULTS_DIR / "metrics.json"
MORPHOLOGY_METRICS_JSON_PATH: Path = RESULTS_DIR / "morphology_metrics.json"
PER_ORDER_RADII_CSV: Path = RESULTS_DIR / "per_order_radii.csv"
PER_BRANCH_AXIAL_CSV: Path = RESULTS_DIR / "per_branch_axial_resistance.csv"

RADIUS_DIST_PNG: Path = IMAGES_DIR / "radius_distribution_by_strahler_order.png"
AXIAL_RES_PNG: Path = IMAGES_DIR / "surface_area_by_strahler_order.png"
SOMA_PROFILE_PNG: Path = IMAGES_DIR / "radius_vs_path_distance.png"
