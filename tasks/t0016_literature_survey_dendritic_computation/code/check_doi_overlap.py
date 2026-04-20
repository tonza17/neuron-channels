"""Verify no DOI in this task's paper assets collides with the t0002 corpus.

Run:
    uv run python -m tasks.t0016_literature_survey_dendritic_computation.code.check_doi_overlap
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[3]

T0002_PAPER_DIR: Path = (
    REPO_ROOT / "tasks" / "t0002_literature_survey_dsgc_compartmental_models" / "assets" / "paper"
)
T0016_PAPER_DIR: Path = (
    REPO_ROOT / "tasks" / "t0016_literature_survey_dendritic_computation" / "assets" / "paper"
)


def _collect_dois(paper_dir: Path) -> set[str]:
    """Collect non-null DOIs from every `details.json` under paper_dir."""
    dois: set[str] = set()
    if not paper_dir.is_dir():
        return dois
    for details_path in paper_dir.glob("*/details.json"):
        with details_path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        doi = data.get("doi")
        if isinstance(doi, str) and doi.strip() != "":
            dois.add(doi.strip().lower())
    return dois


def main() -> int:
    """Compare DOIs and exit non-zero if any overlap exists."""
    t0002_dois: set[str] = _collect_dois(paper_dir=T0002_PAPER_DIR)
    t0016_dois: set[str] = _collect_dois(paper_dir=T0016_PAPER_DIR)
    print(f"t0002 DOIs: {len(t0002_dois)}")
    print(f"t0016 DOIs: {len(t0016_dois)}")
    overlap: set[str] = t0002_dois & t0016_dois
    if len(overlap) > 0:
        print("OVERLAP DETECTED:")
        for doi in sorted(overlap):
            print(f"  - {doi}")
        return 1
    print("No DOI overlap with t0002 corpus.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
