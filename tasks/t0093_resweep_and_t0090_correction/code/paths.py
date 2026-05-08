"""Centralised filesystem paths for t0093 patched-generator re-sweep + correction overlay."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

# ---------------------------------------------------------------------------
# t0093-local data outputs.
# ---------------------------------------------------------------------------

DATA_DIR: Path = TASK_ROOT / "data"
DATA_POST_FIX_VERIFICATION_JSON: Path = DATA_DIR / "post_fix_verification_summary.json"
DATA_PRE_POST_DELTA_JSON: Path = DATA_DIR / "pre_post_delta.json"
DATA_LIBRARY_SUPERSESSION_JSON: Path = DATA_DIR / "library_supersession_check.json"

# ---------------------------------------------------------------------------
# Results.
# ---------------------------------------------------------------------------

RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
RESULTS_METRICS_JSON: Path = RESULTS_DIR / "metrics.json"

POST_FIX_GRID_PNG: Path = RESULTS_IMAGES_DIR / "post_fix_morphology_grid.png"
PRE_VS_POST_BAR_PNG: Path = RESULTS_IMAGES_DIR / "pre_vs_post_spike_counts.png"
TRANSITION_FLOW_PNG: Path = RESULTS_IMAGES_DIR / "transition_flow.png"

# ---------------------------------------------------------------------------
# Corrections.
# ---------------------------------------------------------------------------

CORRECTIONS_DIR: Path = TASK_ROOT / "corrections"
CORRECTION_LIBRARY_JSON: Path = (
    CORRECTIONS_DIR / "library_procedural_dsgc_morphology_generator.json"
)

# ---------------------------------------------------------------------------
# Cross-task input paths -- read-only references to upstream task outputs.
# ---------------------------------------------------------------------------

T0090_TASK_DIR: Path = REPO_ROOT / "tasks" / "t0090_morphology_generator_diversity_test"
T0090_DIFFERENT_DIR: Path = T0090_TASK_DIR / "data" / "different_morphologies"
T0090_SIMILAR_DIR: Path = T0090_TASK_DIR / "data" / "similar_morphologies"
T0090_VERIFICATION_JSON: Path = T0090_TASK_DIR / "data" / "verification_summary.json"

T0083_PARETO_FRONT_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0083_bedb_v3_extend_nsga2_gen8plus"
    / "results"
    / "data"
    / "pareto_front.json"
)


def ensure_directories() -> None:
    """Create every output directory the task writes to."""
    for directory in (
        DATA_DIR,
        RESULTS_DIR,
        RESULTS_IMAGES_DIR,
        CORRECTIONS_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_directories()
    print("paths.py: directories ensured")
