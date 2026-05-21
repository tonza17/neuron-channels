"""Centralised paths for t0116 pooled PCA + cluster + factor analysis."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[3]

TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0116_pooled_pca_cluster_factor_dsi07_pd10"

CODE_DIR: Path = TASK_ROOT / "code"
DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
ASSETS_DIR: Path = TASK_ROOT / "assets"
ANSWERS_DIR: Path = ASSETS_DIR / "answer"

# Sources are listed in constants.SOURCES (absolute via REPO_ROOT at use site).

# Persistent intermediate data.
POOLED_SURVIVORS_PARQUET: Path = DATA_DIR / "pooled_survivors.parquet"
POOLED_GEN0_PARQUET: Path = DATA_DIR / "pooled_gen0.parquet"
POOLED_STANDARDISER_NPZ: Path = DATA_DIR / "pooled_standardiser.npz"
PCA_MODELS_PKL: Path = DATA_DIR / "pca_models.pkl"

# Per-step results data tables.
PER_SEED_COHORT_COUNTS_CSV: Path = RESULTS_DATA_DIR / "per_seed_cohort_counts.csv"
GEN0_DISPLACEMENT_CSV: Path = RESULTS_DATA_DIR / "gen0_displacement.csv"
ELECTROPHYS_CLUSTERS_CSV: Path = RESULTS_DATA_DIR / "electrophys_clusters.csv"
MORPHOLOGY_CLUSTERS_CSV: Path = RESULTS_DATA_DIR / "morphology_clusters.csv"
FACTOR_CORRELATIONS_CSV: Path = RESULTS_DATA_DIR / "factor_correlations.csv"
FACTOR_LOADINGS_CSV: Path = RESULTS_DATA_DIR / "factor_loadings.csv"
CLUSTER_SEED_PURITY_CSV: Path = RESULTS_DATA_DIR / "cluster_seed_purity.csv"
METHODOLOGY_NOTES_MD: Path = RESULTS_DATA_DIR / "methodology_notes.md"
SUMMARY_JSON: Path = RESULTS_DATA_DIR / "implementation_summary.json"

# Chart paths.
PCA_COMBINED_PNG: Path = RESULTS_IMAGES_DIR / "pca_combined.png"
PCA_WITH_GEN0_OVERLAY_PNG: Path = RESULTS_IMAGES_DIR / "pca_with_gen0_overlay.png"
ELECTROPHYS_SILHOUETTE_PNG: Path = RESULTS_IMAGES_DIR / "electrophys_silhouette.png"
MORPHOLOGY_SILHOUETTE_PNG: Path = RESULTS_IMAGES_DIR / "morphology_silhouette.png"
FACTOR_LOADINGS_HEATMAP_PNG: Path = RESULTS_IMAGES_DIR / "factor_loadings_heatmap.png"


def electrophys_cluster_morphs_png(*, cluster_id: int) -> Path:
    """Per-cluster morphology grid PNG path for the electrophys partition."""
    return RESULTS_IMAGES_DIR / f"electrophys_cluster_{cluster_id}_morphs.png"


def morphology_cluster_representatives_csv(*, cluster_id: int) -> Path:
    """Per-cluster representative table CSV path for the morphology partition."""
    return RESULTS_DATA_DIR / f"morphology_cluster_{cluster_id}_representatives.csv"
