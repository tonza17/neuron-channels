"""Centralised path constants for t0121.

Resolves the repository root from the file location so the constants are
robust to invocation CWD. All input paths point at upstream task folders
(read-only); all output paths point at t0121's own ``results/`` and
``assets/`` subdirectories.
"""

from __future__ import annotations

from pathlib import Path

_THIS_FILE: Path = Path(__file__).resolve()
TASK_ROOT: Path = _THIS_FILE.parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

# ---------------------------------------------------------------------------
# Source-task evaluation dumps (read-only inputs)
# ---------------------------------------------------------------------------

# t0106 stores its evaluations as a registered predictions asset.
T0106_EVALS: Path = (
    REPO_ROOT
    / "tasks"
    / "t0106_long_pdnd_nsga2_300gen"
    / "assets"
    / "predictions"
    / "nsga2-seed44-bedb-morph-2dir-300gen"
    / "files"
    / "all_evaluations_seed44.json.gz"
)
T0106_HV: Path = (
    REPO_ROOT
    / "tasks"
    / "t0106_long_pdnd_nsga2_300gen"
    / "results"
    / "data"
    / "hv_trajectory_seed44.json"
)
T0106_PARETO: Path = (
    REPO_ROOT
    / "tasks"
    / "t0106_long_pdnd_nsga2_300gen"
    / "results"
    / "data"
    / "pareto_front_seed44.json"
)

# t0112 evaluations live under results/data/ (gzipped).
T0112_EVALS: Path = (
    REPO_ROOT
    / "tasks"
    / "t0112_t0106_seed77_replicate"
    / "results"
    / "data"
    / "all_evaluations_seed77.json.gz"
)
T0112_HV: Path = (
    REPO_ROOT
    / "tasks"
    / "t0112_t0106_seed77_replicate"
    / "results"
    / "data"
    / "hv_trajectory_seed77.json"
)
T0112_PARETO: Path = (
    REPO_ROOT
    / "tasks"
    / "t0112_t0106_seed77_replicate"
    / "results"
    / "data"
    / "pareto_front_seed77.json"
)

# t0113 stores its evaluations as a registered predictions asset.
T0113_EVALS: Path = (
    REPO_ROOT
    / "tasks"
    / "t0113_t0106_seed2247_replicate"
    / "assets"
    / "predictions"
    / "t0113-bedb-morph-nsga2-seed2247"
    / "files"
    / "all_evaluations_seed2247.json.gz"
)
T0113_HV: Path = (
    REPO_ROOT
    / "tasks"
    / "t0113_t0106_seed2247_replicate"
    / "results"
    / "data"
    / "hv_trajectory_seed2247.json"
)
T0113_PARETO: Path = (
    REPO_ROOT
    / "tasks"
    / "t0113_t0106_seed2247_replicate"
    / "results"
    / "data"
    / "pareto_front_seed2247.json"
)

# t0114 evaluations live under results/data/ (plain JSON).
T0114_EVALS: Path = (
    REPO_ROOT
    / "tasks"
    / "t0114_seed7755_no_autostop"
    / "results"
    / "data"
    / "all_evaluations_seed7755.json"
)
T0114_HV: Path = (
    REPO_ROOT
    / "tasks"
    / "t0114_seed7755_no_autostop"
    / "results"
    / "data"
    / "hv_trajectory_seed7755.json"
)
T0114_PARETO: Path = (
    REPO_ROOT
    / "tasks"
    / "t0114_seed7755_no_autostop"
    / "results"
    / "data"
    / "pareto_front_seed7755.json"
)

# t0115 evaluations live under results/data/ (plain JSON).
T0115_EVALS: Path = (
    REPO_ROOT
    / "tasks"
    / "t0115_seed9354_no_autostop"
    / "results"
    / "data"
    / "all_evaluations_seed9354.json"
)
T0115_HV: Path = (
    REPO_ROOT
    / "tasks"
    / "t0115_seed9354_no_autostop"
    / "results"
    / "data"
    / "hv_trajectory_seed9354.json"
)
T0115_PARETO: Path = (
    REPO_ROOT
    / "tasks"
    / "t0115_seed9354_no_autostop"
    / "results"
    / "data"
    / "pareto_front_seed9354.json"
)

# ---------------------------------------------------------------------------
# Output paths (t0121 writes only inside its own task folder)
# ---------------------------------------------------------------------------

OUT_RESULTS_DIR: Path = TASK_ROOT / "results"
OUT_DATA_DIR: Path = OUT_RESULTS_DIR / "data"
OUT_IMAGES_DIR: Path = OUT_RESULTS_DIR / "images"

CSV_PER_SEED: Path = OUT_DATA_DIR / "per_seed_substrate_rate_5seed.csv"
CSV_CONVENTION_DRIFT: Path = OUT_DATA_DIR / "convention_drift_5seed.csv"
CSV_STATS: Path = OUT_DATA_DIR / "substrate_stats_5seed.csv"
CSV_CONVERGENCE: Path = OUT_DATA_DIR / "per_seed_convergence_5seed.csv"
CSV_LITERATURE: Path = OUT_DATA_DIR / "literature_comparison_5seed.csv"
PARQUET_POOLED: Path = OUT_DATA_DIR / "pooled_legit_jointpass_cells.parquet"

CHART_ACCEPTANCE_BAR: Path = OUT_IMAGES_DIR / "per_seed_acceptance_bar.png"
CHART_HV_OVERLAY: Path = OUT_IMAGES_DIR / "hv_trajectory_5seed_overlay.png"
CHART_DSI_PD_SCATTER: Path = OUT_IMAGES_DIR / "dsi_pd_scatter_5seed_pooled.png"

ANSWER_ASSET_DIR: Path = TASK_ROOT / "assets" / "answer" / "substrate-rate-5seed-canonical"
ANSWER_DETAILS_JSON: Path = ANSWER_ASSET_DIR / "details.json"
ANSWER_SHORT_MD: Path = ANSWER_ASSET_DIR / "short_answer.md"
ANSWER_FULL_MD: Path = ANSWER_ASSET_DIR / "full_answer.md"
