"""Centralised path constants for the t0076 Bed B MOBO task."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_THIS_FILE: Path = Path(__file__).resolve()
TASK_ROOT: Path = _THIS_FILE.parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

CODE_DIR: Path = TASK_ROOT / "code"
MODS_DIR: Path = CODE_DIR / "mods"

# Compiled MOD library: nrnivmodl on Linux drops the shared object in
# ``mods/x86_64/.libs/libnrnmech.so`` (Vast.ai), and on Windows the
# project convention (per t0067 / t0074) places it in ``code/build/nrnmech.dll``
# emitted by ``nrnivmodl.bat``.
LINUX_MOD_BUILD_SO: Path = MODS_DIR / "x86_64" / ".libs" / "libnrnmech.so"
LINUX_MOD_FALLBACK_SO: Path = MODS_DIR / "x86_64" / "libnrnmech.so"
WINDOWS_MOD_BUILD_DLL: Path = CODE_DIR / "build" / "nrnmech.dll"


def resolve_t76_mod_library() -> Path:
    """Return the first existing compiled MOD library for the current platform."""
    candidates: list[Path] = (
        [LINUX_MOD_BUILD_SO, LINUX_MOD_FALLBACK_SO]
        if sys.platform != "win32"
        else [WINDOWS_MOD_BUILD_DLL]
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "Compiled t0076 MOD library not found. Run nrnivmodl on the mods/ "
        f"folder. Tried: {', '.join(str(c) for c in candidates)}."
    )


# Data + results.
DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
IMAGES_DIR: Path = RESULTS_DIR / "images"

# Bayesian-optimisation state outputs.
TRIAL_HISTORY_PARQUET: Path = DATA_DIR / "trial_history.parquet"
HYPERVOLUME_TRAJECTORY_CSV: Path = DATA_DIR / "hypervolume_trajectory.csv"
PARETO_FRONT_JSON: Path = RESULTS_DATA_DIR / "pareto_front.json"
CHECKPOINT_DIR: Path = DATA_DIR / "checkpoints"

# Plots.
PARETO_FRONT_PNG: Path = IMAGES_DIR / "pareto_front.png"
HYPERVOLUME_PNG: Path = IMAGES_DIR / "hypervolume_trajectory.png"

# Typst writeup (consumed by render_pdf.py).
TYPST_SOURCE_PATH: Path = RESULTS_DIR / "results_detailed.typ"
PDF_OUTPUT_PATH: Path = RESULTS_DIR / "results_detailed.pdf"

# Intervention files.
INTERVENTION_DIR: Path = TASK_ROOT / "intervention"
BUDGET_OVERRUN_MD: Path = INTERVENTION_DIR / "budget_overrun.md"


def ensure_directories() -> None:
    """Create all output directories (idempotent)."""
    for d in (DATA_DIR, RESULTS_DIR, RESULTS_DATA_DIR, IMAGES_DIR, CHECKPOINT_DIR):
        d.mkdir(parents=True, exist_ok=True)


# Default NEURON installation prefix on the local Windows workstation. The remote
# Vast.ai instance uses the pip-installed wheel in the project venv so this
# constant has no effect on Linux.
WINDOWS_NEURONHOME_DEFAULT: str = r"C:\Users\md1avn\nrn-8.2.7"
if sys.platform == "win32":
    os.environ.setdefault("NEURONHOME", WINDOWS_NEURONHOME_DEFAULT)
