"""Centralised filesystem paths for t0090 procedural morphology generator task."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

DATA_DIR: Path = TASK_ROOT / "data"
DATA_DIFFERENT_DIR: Path = DATA_DIR / "different_morphologies"
DATA_SIMILAR_DIR: Path = DATA_DIR / "similar_morphologies"
DATA_VERIFICATION_JSON: Path = DATA_DIR / "verification_summary.json"
DATA_BEDB_REPRO_JSON: Path = DATA_DIR / "bedb_reproducibility.json"
DATA_G1_AUDIT_JSON: Path = DATA_DIR / "g1_nav_ratio_audit.json"
DATA_G2_CALIB_JSON: Path = DATA_DIR / "g2_nmda_calibration.json"
DATA_G3_KNOCKOUT_JSON: Path = DATA_DIR / "g3_nap_knockout.json"
DATA_G3_TRACES_DIR: Path = DATA_DIR / "g3_traces"
DATA_MORPHOMETRIC_SUMMARY_JSON: Path = DATA_DIR / "morphometric_summary.json"

RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
RESULTS_METRICS_JSON: Path = RESULTS_DIR / "metrics.json"

ASSETS_DIR: Path = TASK_ROOT / "assets"
ASSETS_LIBRARY_DIR: Path = ASSETS_DIR / "library"
ASSETS_ANSWER_DIR: Path = ASSETS_DIR / "answer"

# Cross-task input paths -- read-only references to upstream task outputs.
T0083_PARETO_FRONT_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0083_bedb_v3_extend_nsga2_gen8plus"
    / "results"
    / "data"
    / "pareto_front.json"
)
T0083_ALL_EVALUATIONS_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0083_bedb_v3_extend_nsga2_gen8plus"
    / "results"
    / "data"
    / "all_evaluations.json"
)
T0088_RECLUSTER_CENTROIDS_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0088_recluster_marginals_and_vm_motifs"
    / "results"
    / "data"
    / "recluster_centroids.json"
)
T0088_REPRESENTATIVE_CELLS_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0088_recluster_marginals_and_vm_motifs"
    / "results"
    / "data"
    / "representative_cells.json"
)


def ensure_directories() -> None:
    """Create every output directory the task writes to."""
    for directory in (
        DATA_DIR,
        DATA_DIFFERENT_DIR,
        DATA_SIMILAR_DIR,
        DATA_G3_TRACES_DIR,
        RESULTS_DIR,
        RESULTS_IMAGES_DIR,
        ASSETS_DIR,
        ASSETS_LIBRARY_DIR,
        ASSETS_ANSWER_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)
