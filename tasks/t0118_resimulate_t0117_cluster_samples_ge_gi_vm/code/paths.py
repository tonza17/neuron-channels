"""Centralised filesystem paths for t0118.

All file paths used by the t0118 pipeline are defined here. Downstream modules import these
constants rather than constructing paths inline.
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# t0118 task root layout
# ---------------------------------------------------------------------------
T0118_TASK_DIR: Path = Path("tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm")
T0118_CODE_DIR: Path = T0118_TASK_DIR / "code"
RESULTS_DIR: Path = T0118_TASK_DIR / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"

# Trace storage layout: results/data/traces/<cluster_id>/<cell_key>/<mode>_<dir>.parquet.
TRACES_ROOT: Path = RESULTS_DATA_DIR / "traces"

# Output tables.
SELECTED_CELLS_CSV: Path = RESULTS_DATA_DIR / "selected_cells.csv"
PER_CELL_METRICS_CSV: Path = RESULTS_DATA_DIR / "per_cell_metrics.csv"
SIMULATION_FAILURES_CSV: Path = RESULTS_DATA_DIR / "simulation_failures.csv"
DSI_SANITY_CHECK_CSV: Path = RESULTS_DATA_DIR / "dsi_sanity_check.csv"

# Figures.
CLUSTER_TRACES_FIGURE_TEMPLATE: str = str(RESULTS_IMAGES_DIR / "cluster_{c}_traces.png")
CROSS_CLUSTER_FIGURE: Path = RESULTS_IMAGES_DIR / "cross_cluster_traces.png"

# ---------------------------------------------------------------------------
# Source data (read-only from t0117 dependency)
# ---------------------------------------------------------------------------
T0117_TASK_DIR: Path = Path("tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds")
T0117_ELECTROPHYS_CLUSTERS_CSV: Path = (
    T0117_TASK_DIR / "results" / "data" / "electrophys_clusters.csv"
)
T0117_POOLED_PARQUET: Path = T0117_TASK_DIR / "data" / "pooled_all_cells.parquet"

# ---------------------------------------------------------------------------
# NEURON DLL (gitignored; must be present in worktree before simulation).
# ---------------------------------------------------------------------------
T0080_DLL_WIN: Path = Path("tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/build/nrnmech.dll")
