"""Centralised paths for t0125 cluster + factor analysis on t0123 MI/ATP NSGA-II output."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[3]

TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0125_t0123_cluster_factor_mi_atp"

CODE_DIR: Path = TASK_ROOT / "code"
DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
ASSETS_DIR: Path = TASK_ROOT / "assets"
ANSWERS_DIR: Path = ASSETS_DIR / "answer"

# Source predictions file (relative to REPO_ROOT).
T0123_PREDICTIONS_REL_PATH: Path = Path(
    "tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/"
    "nsga2-mi-atp-per-spike-bedb-morph/files/predictions.jsonl.gz"
)

# Persistent intermediate data.
T0123_CELLS_PARQUET: Path = DATA_DIR / "t0125_cells.parquet"
T0123_SPIKING_CELLS_PARQUET: Path = DATA_DIR / "t0125_spiking_cells.parquet"
T0123_GEN0_PARQUET: Path = DATA_DIR / "t0125_gen0.parquet"
T0123_STANDARDISER_NPZ: Path = DATA_DIR / "t0125_standardiser.npz"
PCA_MODELS_PKL: Path = DATA_DIR / "pca_models.pkl"

# Per-step results data tables.
POOL_COUNTS_CSV: Path = RESULTS_DATA_DIR / "pool_counts.csv"
GROUP_THRESHOLDS_JSON: Path = RESULTS_DATA_DIR / "group_thresholds.json"
GEN0_DISPLACEMENT_CSV: Path = RESULTS_DATA_DIR / "gen0_displacement.csv"
ELECTROPHYS_CLUSTERS_CSV: Path = RESULTS_DATA_DIR / "electrophys_clusters.csv"
MORPHOLOGY_CLUSTERS_CSV: Path = RESULTS_DATA_DIR / "morphology_clusters.csv"
FACTOR_CORRELATIONS_CSV: Path = RESULTS_DATA_DIR / "factor_correlations.csv"
FACTOR_LOADINGS_CSV: Path = RESULTS_DATA_DIR / "factor_loadings.csv"
CLUSTER_GROUP_PURITY_CSV: Path = RESULTS_DATA_DIR / "cluster_group_purity.csv"
GROUP_COMPARISON_CSV: Path = RESULTS_DATA_DIR / "group_comparison.csv"
CORNER_PARAM_MEANS_CSV: Path = RESULTS_DATA_DIR / "corner_param_means.csv"
ATP_COMPARTMENT_SHARES_CSV: Path = RESULTS_DATA_DIR / "atp_compartment_shares.csv"
METHODOLOGY_NOTES_MD: Path = RESULTS_DATA_DIR / "methodology_notes.md"

# Chart paths.
PCA_COMBINED_COLOR_MI_PNG: Path = RESULTS_IMAGES_DIR / "pca_combined_color_mi.png"
PCA_COMBINED_COLOR_ATP_PNG: Path = RESULTS_IMAGES_DIR / "pca_combined_color_atp.png"
PCA_COMBINED_COLOR_CORNER_PNG: Path = RESULTS_IMAGES_DIR / "pca_combined_color_corner.png"
PCA_WITH_GEN0_OVERLAY_PNG: Path = RESULTS_IMAGES_DIR / "pca_with_gen0_overlay.png"
ELECTROPHYS_SILHOUETTE_PNG: Path = RESULTS_IMAGES_DIR / "electrophys_silhouette.png"
MORPHOLOGY_SILHOUETTE_PNG: Path = RESULTS_IMAGES_DIR / "morphology_silhouette.png"
FACTOR_LOADINGS_HEATMAP_PNG: Path = RESULTS_IMAGES_DIR / "factor_loadings_heatmap.png"
CLIFFS_DELTA_MI_PNG: Path = RESULTS_IMAGES_DIR / "cliffs_delta_high_vs_low_mi.png"
CLIFFS_DELTA_ATP_PNG: Path = RESULTS_IMAGES_DIR / "cliffs_delta_high_vs_low_atp.png"
CORNER_PARAM_HEATMAP_PNG: Path = RESULTS_IMAGES_DIR / "corner_param_heatmap.png"
ATP_SHARE_TERNARY_PNG: Path = RESULTS_IMAGES_DIR / "atp_share_ternary.png"
ATP_SHARE_VIOLINS_PNG: Path = RESULTS_IMAGES_DIR / "atp_share_violins.png"


def electrophys_cluster_morphs_png(*, cluster_id: int) -> Path:
    """Per-cluster morphology grid PNG path for the electrophys partition."""
    return RESULTS_IMAGES_DIR / f"electrophys_cluster_{cluster_id}_morphs.png"


def morphology_cluster_representatives_csv(*, cluster_id: int) -> Path:
    """Per-cluster representative table CSV path for the morphology partition."""
    return RESULTS_DATA_DIR / f"morphology_cluster_{cluster_id}_representatives.csv"
