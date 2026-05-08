"""Centralised path constants for the t0091 joint 68-d NSGA-II task."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_THIS_FILE: Path = Path(__file__).resolve()
TASK_ROOT: Path = _THIS_FILE.parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

CODE_DIR: Path = TASK_ROOT / "code"
MODS_DIR: Path = CODE_DIR / "mods"

# Compiled MOD library paths. t0091 reuses the t0080 MOD library on Linux to
# avoid double-loading the same channel SUFFIXes (which raises
# "The user defined name already exists: bkt80" inside NEURON).
T0080_MODS_DIR: Path = (
    REPO_ROOT / "tasks" / "t0080_bedb_mobo_v3_dendritic_spike_nsga2" / "code" / "mods"
)
LINUX_MOD_BUILD_SO: Path = T0080_MODS_DIR / "x86_64" / ".libs" / "libnrnmech.so"
LINUX_MOD_FALLBACK_SO: Path = T0080_MODS_DIR / "x86_64" / "libnrnmech.so"
WINDOWS_MOD_BUILD_DLL: Path = (
    REPO_ROOT
    / "tasks"
    / "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
    / "code"
    / "build"
    / "nrnmech.dll"
)


def resolve_t91_mod_library() -> Path:
    """Return the t0080 compiled MOD library (shared SUFFIX namespace).

    t0091 reuses t0080's MOD library because t0090.generator's `_get_neuron_h`
    already loads it (via `ensure_t80_dll_loaded`). Loading the same SUFFIX
    twice raises a NEURON error; pointing t0091's apply_params at the same
    library file makes the load idempotent (NEURON dedupes by file handle).
    """
    candidates: list[Path] = (
        [LINUX_MOD_BUILD_SO, LINUX_MOD_FALLBACK_SO]
        if sys.platform != "win32"
        else [WINDOWS_MOD_BUILD_DLL]
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "Compiled t0080 MOD library not found. Run nrnivmodl on the t0080 mods/ "
        f"folder. Tried: {', '.join(str(c) for c in candidates)}."
    )


# Data + results.
DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
IMAGES_DIR: Path = RESULTS_DIR / "images"

# Predicted output paths.
PARETO_FRONT_JSON: Path = RESULTS_DATA_DIR / "pareto_front.json"
ALL_EVALUATIONS_JSON: Path = RESULTS_DATA_DIR / "all_evaluations.json"
HV_TRAJECTORY_JSON: Path = RESULTS_DATA_DIR / "hv_trajectory.json"
WARM_START_POPULATION_JSON: Path = RESULTS_DATA_DIR / "warm_start_population.json"
ANCHOR_DEFINITIONS_JSON: Path = RESULTS_DATA_DIR / "anchor_definitions.json"
ANCHOR_TRACKING_JSON: Path = RESULTS_DATA_DIR / "anchor_tracking.json"
BIOLOGICAL_PRIORS_68D_JSON: Path = RESULTS_DATA_DIR / "biological_priors_68d.json"
BIOLOGICAL_SCORECARD_68D_JSON: Path = RESULTS_DATA_DIR / "biological_scorecard_68d.json"
EVALUATION_SEEDS_JSON: Path = RESULTS_DATA_DIR / "evaluation_seeds.json"
EVALUATION_LATENCY_JSON: Path = RESULTS_DATA_DIR / "evaluation_latency.json"
LENGTH_DSI_CORRELATION_JSON: Path = RESULTS_DATA_DIR / "length_dsi_correlation.json"
ALGORITHM_CONFIG_JSON: Path = RESULTS_DATA_DIR / "algorithm_config.json"
CHECKPOINT_JSON: Path = RESULTS_DATA_DIR / "nsga2_checkpoint.json"

# Plots.
DSI_VS_LENGTH_PNG: Path = IMAGES_DIR / "dsi_vs_length.png"
ANCHOR_TRACKING_BAR_PNG: Path = IMAGES_DIR / "anchor_tracking_bar.png"
BIOLOGICAL_HEATMAP_PNG: Path = IMAGES_DIR / "biological_plausibility_heatmap_68d.png"
HV_TRAJECTORY_PNG: Path = IMAGES_DIR / "hv_trajectory.png"
PARETO_FRONT_PNG: Path = IMAGES_DIR / "pareto_front.png"

# Intervention files.
INTERVENTION_DIR: Path = TASK_ROOT / "intervention"
BUDGET_OVERRUN_MD: Path = INTERVENTION_DIR / "budget_overrun.md"
SMOKE_GATE_FAILURE_MD: Path = INTERVENTION_DIR / "smoke_gate_failure.md"

# Upstream data sources.
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
T0086_CELL_CLASSIFICATION_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0086_robustness_cluster_bio_comparison"
    / "results"
    / "data"
    / "cell_classification.json"
)
T0093_POST_FIX_VERIFICATION_SUMMARY_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0093_resweep_and_t0090_correction"
    / "data"
    / "post_fix_verification_summary.json"
)
MACHINE_LOG_JSON: Path = TASK_ROOT / "logs" / "steps" / "008_setup-machines" / "machine_log.json"


def ensure_directories() -> None:
    """Create all output directories (idempotent)."""
    for d in (DATA_DIR, RESULTS_DIR, RESULTS_DATA_DIR, IMAGES_DIR, INTERVENTION_DIR):
        d.mkdir(parents=True, exist_ok=True)


# Default NEURON installation prefix on the local Windows workstation.
WINDOWS_NEURONHOME_DEFAULT: str = r"C:\Users\md1avn\nrn-8.2.7"
if sys.platform == "win32":
    os.environ.setdefault("NEURONHOME", WINDOWS_NEURONHOME_DEFAULT)
