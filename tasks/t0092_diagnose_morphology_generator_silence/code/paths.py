"""Centralised filesystem paths for t0092 diagnose-morphology-generator-silence task."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

DATA_DIR: Path = TASK_ROOT / "data"
STRUCTURAL_COMPARISON_JSON: Path = DATA_DIR / "structural_comparison.json"
SYNAPSE_COMPARISON_JSON: Path = DATA_DIR / "synapse_comparison.json"
VM_TRACE_PROCEDURAL_NPY: Path = DATA_DIR / "vm_trace_procedural.npy"
VM_TRACE_HANDCODED_NPY: Path = DATA_DIR / "vm_trace_handcoded.npy"
VM_TRACE_FIXED_NPY: Path = DATA_DIR / "vm_trace_procedural_fixed.npy"
ROOT_CAUSE_ANALYSIS_JSON: Path = DATA_DIR / "root_cause_analysis.json"
POST_FIX_VERIFICATION_JSON: Path = DATA_DIR / "post_fix_verification.json"

RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"
VM_TRACE_COMPARISON_PNG: Path = IMAGES_DIR / "vm_trace_comparison.png"
POST_FIX_POLAR_TUNING_PNG: Path = IMAGES_DIR / "post_fix_polar_tuning.png"
RESULTS_METRICS_JSON: Path = RESULTS_DIR / "metrics.json"

ASSETS_DIR: Path = TASK_ROOT / "assets"
ASSETS_LIBRARY_DIR: Path = ASSETS_DIR / "library"
ASSETS_ANSWER_DIR: Path = ASSETS_DIR / "answer"

# Cross-task input paths -- read-only references to upstream task outputs.
T0090_DIFFERENT_DIR: Path = (
    REPO_ROOT
    / "tasks"
    / "t0090_morphology_generator_diversity_test"
    / "data"
    / "different_morphologies"
)


def ensure_directories() -> None:
    """Create every output directory the task writes to."""
    for directory in (
        DATA_DIR,
        RESULTS_DIR,
        IMAGES_DIR,
        ASSETS_DIR,
        ASSETS_LIBRARY_DIR,
        ASSETS_ANSWER_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)
