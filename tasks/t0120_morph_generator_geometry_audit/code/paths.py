"""Path constants for the t0120 morphology generator geometry audit."""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Repo / task roots
# ---------------------------------------------------------------------------

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0120_morph_generator_geometry_audit"
CODE_DIR: Path = TASK_ROOT / "code"
DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
ASSETS_DIR: Path = TASK_ROOT / "assets"
ANSWERS_DIR: Path = ASSETS_DIR / "answer"

# ---------------------------------------------------------------------------
# Source data (read-only, from upstream tasks)
# ---------------------------------------------------------------------------

POOLED_ALL_CELLS_PARQUET: Path = (
    REPO_ROOT
    / "tasks"
    / "t0117_pooled_pca_cluster_factor_all_cells_4_seeds"
    / "data"
    / "pooled_all_cells.parquet"
)

# Hand-curated list of worst-looking cells from inspection of t0115's
# top50_morphologies_seed9354.png. See README inside the CSV's header comment.
WORST_LOOKING_CELLS_CSV: Path = CODE_DIR / "worst_looking_cells.csv"

# ---------------------------------------------------------------------------
# Per-step output paths
# ---------------------------------------------------------------------------

SAMPLED_CELL_MANIFEST_CSV: Path = RESULTS_DATA_DIR / "sampled_cell_manifest.csv"
SECTION_ENDPOINTS_DUMP_JSON: Path = RESULTS_DATA_DIR / "section_endpoints_dump.json"
COORDINATE_CONSISTENCY_CHECKS_CSV: Path = RESULTS_DATA_DIR / "coordinate_consistency_checks.csv"
GEOMETRY_AUDIT_GALLERY_PNG: Path = RESULTS_IMAGES_DIR / "geometry_audit_gallery.png"

# ---------------------------------------------------------------------------
# Answer asset paths
# ---------------------------------------------------------------------------

ANSWER_ID: str = "morphology-generator-geometry-consistency"
ANSWER_DIR: Path = ANSWERS_DIR / ANSWER_ID
ANSWER_DETAILS_JSON: Path = ANSWER_DIR / "details.json"
ANSWER_SHORT_MD: Path = ANSWER_DIR / "short_answer.md"
ANSWER_FULL_MD: Path = ANSWER_DIR / "full_answer.md"


def ensure_directories() -> None:
    """Create all output directories if they do not exist."""
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    ANSWER_DIR.mkdir(parents=True, exist_ok=True)
