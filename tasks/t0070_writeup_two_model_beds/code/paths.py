"""Path constants for the two-model-bed writeup task.

All file paths produced or consumed by this task are centralised here per the project
Python style guide. This module is import-side-effect-free; directory creation is the
caller's responsibility (`IMAGES_DIR.mkdir(parents=True, exist_ok=True)` is invoked by
the plotting scripts at runtime).
"""

from pathlib import Path
from typing import Final

TASK_ROOT: Final[Path] = Path(__file__).resolve().parent.parent

CODE_DIR: Final[Path] = TASK_ROOT / "code"
RESULTS_DIR: Final[Path] = TASK_ROOT / "results"
IMAGES_DIR: Final[Path] = RESULTS_DIR / "images"

BED_A_MORPH_PNG: Final[Path] = IMAGES_DIR / "bed_a_morphology.png"
BED_B_MORPH_PNG: Final[Path] = IMAGES_DIR / "bed_b_morphology.png"
BED_A_SYNDIAG_PNG: Final[Path] = IMAGES_DIR / "bed_a_synaptic_diagram.png"
BED_B_SYNDIAG_PNG: Final[Path] = IMAGES_DIR / "bed_b_synaptic_diagram.png"

RESULTS_DETAILED_MD: Final[Path] = RESULTS_DIR / "results_detailed.md"
RESULTS_SUMMARY_MD: Final[Path] = RESULTS_DIR / "results_summary.md"
