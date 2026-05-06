"""Centralised path constants for t0086.

Keeps all filesystem paths in one place (per project Python style guide).
"""

from pathlib import Path

TASK_DIR: Path = Path(__file__).resolve().parent.parent
RESULTS_DIR: Path = TASK_DIR / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
INTERVENTION_DIR: Path = TASK_DIR / "intervention"
LOGS_DIR: Path = TASK_DIR / "logs"
ASSETS_DIR: Path = TASK_DIR / "assets"
ANSWER_DIR: Path = ASSETS_DIR / "answer" / "cluster-biological-plausibility-attribution"

# Step 8 setup-machines log folder (canonical location for machine_log.json).
SETUP_MACHINES_LOG_DIR: Path = LOGS_DIR / "steps" / "008_setup-machines"
MACHINE_LOG_JSON: Path = SETUP_MACHINES_LOG_DIR / "machine_log.json"

# Output files for results step.
SELECTED_CELLS_JSON: Path = RESULTS_DATA_DIR / "selected_cells.json"
REPLICATION_SEEDS_JSON: Path = RESULTS_DATA_DIR / "replication_seeds.json"
REPLICATION_RESULTS_JSON: Path = RESULTS_DATA_DIR / "replication_results.json"
CELL_CLASSIFICATION_JSON: Path = RESULTS_DATA_DIR / "cell_classification.json"
CLUSTERING_RESULTS_JSON: Path = RESULTS_DATA_DIR / "clustering_results.json"
CLUSTER_CENTROIDS_JSON: Path = RESULTS_DATA_DIR / "cluster_centroids.json"
BIOLOGICAL_PRIORS_JSON: Path = RESULTS_DATA_DIR / "biological_priors.json"
BIOLOGICAL_SCORECARD_JSON: Path = RESULTS_DATA_DIR / "biological_scorecard.json"
COSTS_JSON: Path = RESULTS_DIR / "costs.json"
REMOTE_MACHINES_USED_JSON: Path = RESULTS_DIR / "remote_machines_used.json"
BUDGET_OVERRUN_MD: Path = INTERVENTION_DIR / "budget_overrun.md"

# Source dataset paths from dependency tasks.
T0081_ALL_EVALUATIONS_JSON: Path = (
    TASK_DIR.parent / "t0081_bedb_v3_warmstart_nsga2" / "results" / "data" / "all_evaluations.json"
)
T0083_ALL_EVALUATIONS_JSON: Path = (
    TASK_DIR.parent
    / "t0083_bedb_v3_extend_nsga2_gen8plus"
    / "results"
    / "data"
    / "all_evaluations.json"
)
T0083_PARETO_FRONT_JSON: Path = (
    TASK_DIR.parent
    / "t0083_bedb_v3_extend_nsga2_gen8plus"
    / "results"
    / "data"
    / "pareto_front.json"
)


def ensure_directories() -> None:
    """Create all output directories if they do not exist."""
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    INTERVENTION_DIR.mkdir(parents=True, exist_ok=True)
    ANSWER_DIR.mkdir(parents=True, exist_ok=True)
