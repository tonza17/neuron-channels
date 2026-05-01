from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent

RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"

TYPST_SOURCE_PATH: Path = RESULTS_DIR / "results_detailed.typ"
PDF_OUTPUT_PATH: Path = RESULTS_DIR / "results_detailed.pdf"
