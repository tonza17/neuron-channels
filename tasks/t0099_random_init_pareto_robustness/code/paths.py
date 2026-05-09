"""Centralised path constants for the t0099 random-init NSGA-II reproducibility task.

t0099 mirrors t0091's path layout but adds per-seed output filenames keyed on
the integer RNG seed (one of 11, 22, 33).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_THIS_FILE: Path = Path(__file__).resolve()
TASK_ROOT: Path = _THIS_FILE.parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

CODE_DIR: Path = TASK_ROOT / "code"

# t0099 reuses t0080's compiled MOD library (same SUFFIX namespace as t0091).
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


def resolve_t99_mod_library() -> Path:
    """Return the t0080 compiled MOD library (shared SUFFIX namespace)."""
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

# Cross-seed outputs.
ALGORITHM_CONFIG_JSON: Path = RESULTS_DATA_DIR / "algorithm_config.json"
EVALUATION_SEEDS_JSON: Path = RESULTS_DATA_DIR / "evaluation_seeds.json"
CROSS_SEED_SUMMARY_JSON: Path = RESULTS_DATA_DIR / "cross_seed_summary.json"
ANCHOR_DISTRIBUTION_TABLE_JSON: Path = RESULTS_DATA_DIR / "anchor_distribution_table.json"

# Intervention files.
INTERVENTION_DIR: Path = TASK_ROOT / "intervention"
BUDGET_OVERRUN_DIR: Path = INTERVENTION_DIR  # one MD per seed if it trips


def init_pop_json(*, seed: int) -> Path:
    return RESULTS_DATA_DIR / f"init_pop_seed{seed}.json"


def pareto_front_json(*, seed: int) -> Path:
    return RESULTS_DATA_DIR / f"pareto_front_seed{seed}.json"


def all_evaluations_json(*, seed: int) -> Path:
    return RESULTS_DATA_DIR / f"all_evaluations_seed{seed}.json"


def hv_trajectory_json(*, seed: int) -> Path:
    return RESULTS_DATA_DIR / f"hv_trajectory_seed{seed}.json"


def checkpoint_json(*, seed: int) -> Path:
    return RESULTS_DATA_DIR / f"nsga2_checkpoint_seed{seed}.json"


def anchor_tracking_json(*, seed: int) -> Path:
    return RESULTS_DATA_DIR / f"anchor_tracking_seed{seed}.json"


def biological_scorecard_json(*, seed: int) -> Path:
    return RESULTS_DATA_DIR / f"biological_scorecard_seed{seed}.json"


def biological_priors_json() -> Path:
    return RESULTS_DATA_DIR / "biological_priors_68d.json"


def budget_overrun_md(*, seed: int) -> Path:
    return INTERVENTION_DIR / f"budget_overrun_seed{seed}.md"


# Plots.
HV_TRAJECTORY_CROSS_SEED_PNG: Path = IMAGES_DIR / "hv_trajectory_cross_seed.png"
PARETO_OVERLAY_PNG: Path = IMAGES_DIR / "pareto_overlay_dsi_pdrate_robust.png"
ANCHOR_HEATMAP_PNG: Path = IMAGES_DIR / "anchor_distribution_heatmap.png"


# Upstream data references (read-only).
T0091_PARETO_FRONT_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0091_morphology_extended_nsga2_v1"
    / "results"
    / "data"
    / "pareto_front.json"
)
T0091_HV_TRAJECTORY_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0091_morphology_extended_nsga2_v1"
    / "results"
    / "data"
    / "hv_trajectory.json"
)
T0091_ANCHOR_DEFINITIONS_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0091_morphology_extended_nsga2_v1"
    / "results"
    / "data"
    / "anchor_definitions.json"
)
T0091_ANCHOR_TRACKING_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0091_morphology_extended_nsga2_v1"
    / "results"
    / "data"
    / "anchor_tracking.json"
)
T0091_BIOLOGICAL_SCORECARD_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0091_morphology_extended_nsga2_v1"
    / "results"
    / "data"
    / "biological_scorecard_68d.json"
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
