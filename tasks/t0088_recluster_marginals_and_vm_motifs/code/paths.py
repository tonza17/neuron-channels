"""Centralised path constants for task t0088_recluster_marginals_and_vm_motifs."""

from __future__ import annotations

from pathlib import Path

_THIS_FILE: Path = Path(__file__).resolve()
TASK_ROOT: Path = _THIS_FILE.parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

# Inputs from upstream completed tasks.
T0083_ALL_EVALUATIONS_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0083_bedb_v3_extend_nsga2_gen8plus"
    / "results"
    / "data"
    / "all_evaluations.json"
)
T0086_CELL_CLASSIFICATION_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0086_robustness_cluster_bio_comparison"
    / "results"
    / "data"
    / "cell_classification.json"
)

# Output directories.
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"

# Output JSONs.
RECLUSTER_ASSIGNMENTS_JSON: Path = RESULTS_DATA_DIR / "recluster_assignments.json"
RECLUSTER_CENTROIDS_JSON: Path = RESULTS_DATA_DIR / "recluster_centroids.json"
RECLUSTER_BIOLOGICAL_SCORECARD_JSON: Path = RESULTS_DATA_DIR / "recluster_biological_scorecard.json"
BIOLOGICAL_PRIORS_JSON: Path = RESULTS_DATA_DIR / "biological_priors.json"
REPRESENTATIVE_CELLS_JSON: Path = RESULTS_DATA_DIR / "representative_cells.json"
MECHANISM_DISTINCTNESS_JSON: Path = RESULTS_DATA_DIR / "mechanism_distinctness.json"

# Output PNGs (Phase A clustering visualisations).
CLUSTER_UMAP_PNG: Path = RESULTS_IMAGES_DIR / "cluster_umap.png"
CLUSTER_PCA_PNG: Path = RESULTS_IMAGES_DIR / "cluster_pca.png"
CLUSTER_SILHOUETTE_PNG: Path = RESULTS_IMAGES_DIR / "cluster_silhouette.png"
CLUSTER_DENDROGRAM_PNG: Path = RESULTS_IMAGES_DIR / "cluster_dendrogram.png"
BIOLOGICAL_HEATMAP_PNG: Path = RESULTS_IMAGES_DIR / "biological_plausibility_heatmap.png"

# Top-level results files.
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
COSTS_JSON: Path = RESULTS_DIR / "costs.json"
REMOTE_MACHINES_JSON: Path = RESULTS_DIR / "remote_machines_used.json"

# Answer asset folder.
ANSWER_DIR: Path = TASK_ROOT / "assets" / "answer" / "are-cluster-motifs-mechanistically-distinct"


def ensure_directories() -> None:
    """Create all output directories (idempotent)."""
    for d in (RESULTS_DATA_DIR, RESULTS_IMAGES_DIR, ANSWER_DIR):
        d.mkdir(parents=True, exist_ok=True)
