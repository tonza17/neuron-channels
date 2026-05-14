"""Centralised pathlib.Path constants for t0105 inputs and outputs."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[3]

TASK_ID: str = "t0105_cluster_factor_analysis_dsi_pd"
TASK_DIR: Path = REPO_ROOT / "tasks" / TASK_ID

CODE_DIR: Path = TASK_DIR / "code"

RESULTS_DIR: Path = TASK_DIR / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"

ASSETS_DIR: Path = TASK_DIR / "assets"
ANSWER_DIR: Path = ASSETS_DIR / "answer"

# Input data files (predecessor tasks).
T0091_EVAL_PATH: Path = (
    REPO_ROOT
    / "tasks"
    / "t0091_morphology_extended_nsga2_v1"
    / "results"
    / "data"
    / "all_evaluations.json"
)
T0099_DATA_DIR: Path = (
    REPO_ROOT / "tasks" / "t0099_random_init_pareto_robustness" / "results" / "data"
)
T0102_DATA_DIR: Path = REPO_ROOT / "tasks" / "t0102_seedscale_n4_gen20" / "results" / "data"
T0104_DATA_DIR: Path = (
    REPO_ROOT / "tasks" / "t0104_nsga2_2obj_dsi_pdrate_3seeds" / "results" / "data"
)

T0099_SEEDS: tuple[int, ...] = (11, 22, 33)
T0102_SEEDS: tuple[int, ...] = (44, 55)
T0104_SEEDS: tuple[int, ...] = (44, 55)


def t0099_seed_path(*, seed: int) -> Path:
    return T0099_DATA_DIR / f"all_evaluations_seed{seed}.json"


def t0102_seed_path(*, seed: int) -> Path:
    return T0102_DATA_DIR / f"all_evaluations_seed{seed}.json"


def t0104_seed_path(*, seed: int) -> Path:
    return T0104_DATA_DIR / f"all_evaluations_seed{seed}.json"


# Output JSON files (results/data).
SELECTED_CELLS_PRIMARY_PATH: Path = RESULTS_DATA_DIR / "selected_cells_primary.json"
SELECTED_CELLS_STRICT_PATH: Path = RESULTS_DATA_DIR / "selected_cells_strict.json"
SELECTION_COUNTS_PATH: Path = RESULTS_DATA_DIR / "selection_counts.json"
ASYM_SCORE_DISTRIBUTION_PATH: Path = RESULTS_DATA_DIR / "asym_score_distribution.json"
GALLERY_QUOTA_TABLE_PATH: Path = RESULTS_DATA_DIR / "gallery_quota_table.json"
PCA_RESULTS_PATH: Path = RESULTS_DATA_DIR / "pca_results.json"
PCA_MANNWHITNEY_PATH: Path = RESULTS_DATA_DIR / "pca_mannwhitney.json"
FACTOR_LOADINGS_PATH: Path = RESULTS_DATA_DIR / "factor_loadings.json"
FACTOR_SCORES_PATH: Path = RESULTS_DATA_DIR / "factor_scores.json"
FACTOR_CORRELATIONS_PATH: Path = RESULTS_DATA_DIR / "factor_correlations.json"
FACTOR_BOOTSTRAP_PATH: Path = RESULTS_DATA_DIR / "factor_bootstrap.json"

PCA_RESULTS_STRICT_PATH: Path = RESULTS_DATA_DIR / "pca_results_strict.json"
PCA_MANNWHITNEY_STRICT_PATH: Path = RESULTS_DATA_DIR / "pca_mannwhitney_strict.json"
FACTOR_LOADINGS_STRICT_PATH: Path = RESULTS_DATA_DIR / "factor_loadings_strict.json"
FACTOR_CORRELATIONS_STRICT_PATH: Path = RESULTS_DATA_DIR / "factor_correlations_strict.json"

METRICS_PATH: Path = RESULTS_DIR / "metrics.json"

# Output PNG files (results/images).
ASYM_HISTOGRAM_PATH: Path = RESULTS_IMAGES_DIR / "asym_score_histogram.png"
MORPHOLOGY_GALLERY_PATH: Path = RESULTS_IMAGES_DIR / "morphology_gallery.png"
PCA_PANELS_PATH: Path = RESULTS_IMAGES_DIR / "pca_electrophys_panels.png"
EIGENVALUE_SCREE_PATH: Path = RESULTS_IMAGES_DIR / "eigenvalue_scree.png"
FACTOR_LOADINGS_HEATMAP_PATH: Path = RESULTS_IMAGES_DIR / "factor_loadings.png"
FACTOR_CORRELATIONS_CHART_PATH: Path = RESULTS_IMAGES_DIR / "factor_correlations.png"
FACTOR_BOOTSTRAP_PATH_PNG: Path = RESULTS_IMAGES_DIR / "factor_loadings_bootstrap.png"

PCA_PANELS_STRICT_PATH: Path = RESULTS_IMAGES_DIR / "pca_electrophys_panels_strict.png"
FACTOR_LOADINGS_STRICT_PATH_PNG: Path = RESULTS_IMAGES_DIR / "factor_loadings_strict.png"
FACTOR_CORRELATIONS_STRICT_PATH_PNG: Path = RESULTS_IMAGES_DIR / "factor_correlations_strict.png"
