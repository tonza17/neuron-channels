"""Centralised paths for t0108."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[3]

TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0108_t0106_cluster_factor_dsi05_pd10"

CODE_DIR: Path = TASK_ROOT / "code"
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
ASSETS_DIR: Path = TASK_ROOT / "assets"
ANSWERS_DIR: Path = ASSETS_DIR / "answer"

T0106_EVALUATIONS_GZ: Path = (
    REPO_ROOT
    / "tasks"
    / "t0106_long_pdnd_nsga2_300gen"
    / "results"
    / "data"
    / "all_evaluations_seed44.json.gz"
)

FILTERED_CELLS_JSON: Path = RESULTS_DATA_DIR / "filtered_cells.json"
ELECTROPHYS_CLUSTERS_JSON: Path = RESULTS_DATA_DIR / "electrophys_clusters.json"
MORPHOLOGY_CLUSTERS_JSON: Path = RESULTS_DATA_DIR / "morphology_clusters.json"
FACTOR_ANALYSIS_JSON: Path = RESULTS_DATA_DIR / "factor_analysis.json"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"

PCA_ELECTROPHYS_BY_CLUSTER_PNG: Path = RESULTS_IMAGES_DIR / "pca_electrophys_by_cluster.png"
PCA_ELECTROPHYS_BY_DSI_PD_PNG: Path = RESULTS_IMAGES_DIR / "pca_electrophys_by_dsi_pd.png"
MORPH_OVERLAY_PNG: Path = RESULTS_IMAGES_DIR / "morph_overlay_by_electrophys_cluster.png"

PCA_MORPHOLOGY_BY_CLUSTER_PNG: Path = RESULTS_IMAGES_DIR / "pca_morphology_by_cluster.png"
PCA_MORPHOLOGY_BY_DSI_PD_PNG: Path = RESULTS_IMAGES_DIR / "pca_morphology_by_dsi_pd.png"
ELECTROPHYS_OVERLAY_PNG: Path = RESULTS_IMAGES_DIR / "electrophys_overlay_by_morphology_cluster.png"

FACTOR_LOADINGS_PNG: Path = RESULTS_IMAGES_DIR / "factor_loadings_heatmap.png"
FACTOR_CORRELATIONS_PNG: Path = RESULTS_IMAGES_DIR / "factor_correlations_dsi_pd.png"
