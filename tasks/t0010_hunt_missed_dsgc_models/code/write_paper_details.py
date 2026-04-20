"""Write details.json for the Poleg-Polsky 2026 paper asset.

Per paper spec v3, details.json is a mandatory structured metadata file per
paper asset. This writer emits UTF-8 JSON with stable key ordering matching
the spec example.
"""

from __future__ import annotations

import json
from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
ASSETS_PAPER_DIR: Path = TASK_ROOT / "assets" / "paper"


POLEGPOLSKY_DETAILS: dict[str, object] = {
    "spec_version": "3",
    "paper_id": "10.1038_s41467-026-70288-4",
    "doi": "10.1038/s41467-026-70288-4",
    "title": (
        "Machine learning discovers numerous new computational principles "
        "underlying direction selectivity in the retina"
    ),
    "url": "https://www.nature.com/articles/s41467-026-70288-4",
    "pdf_url": "https://www.nature.com/articles/s41467-026-70288-4.pdf",
    "date_published": "2026",
    "year": 2026,
    "authors": [
        {
            "name": "Alon Poleg-Polsky",
            "country": "US",
            "institution": ("University of Colorado Anschutz Medical Campus"),
            "orcid": "0000-0001-5947-0707",
        },
    ],
    "institutions": [
        {
            "name": "University of Colorado Anschutz Medical Campus",
            "country": "US",
        },
    ],
    "journal": "Nature Communications",
    "venue_type": "journal",
    "categories": [
        "compartmental-modeling",
        "direction-selectivity",
        "retinal-ganglion-cell",
        "synaptic-integration",
        "dendritic-computation",
    ],
    "abstract": (
        "Direction selectivity is a canonical example of neural computation "
        "in the retina, yet the full repertoire of biophysical mechanisms "
        "that can produce it remains unclear. Here, a machine learning "
        "pipeline explores an enormous space of compartmental models of a "
        "352-segment direction-selective ganglion cell (DSGC) receiving "
        "bipolar-cell inputs with varying spatial offsets, weights, "
        "kinetics, and dendritic biophysics. The search discovers multiple "
        "novel computational primitives that each produce robust direction "
        "selectivity, including velocity-dependent coincidence detection, "
        "distance-graded delay lines, and NMDA-mediated multiplicative "
        "gating. These primitives complement - rather than replace - the "
        "classical starburst-amacrine-cell-based inhibitory mechanism, "
        "suggesting the retinal DS circuit relies on a richer set of "
        "mechanisms than previously appreciated."
    ),
    "citation_key": "PolegPolsky2026",
    "summary_path": "summary.md",
    "files": [
        "files/polegpolsky_2026_ml-motion-primitives.pdf",
    ],
    "download_status": "success",
    "download_failure_reason": None,
    "added_by_task": "t0010_hunt_missed_dsgc_models",
    "date_added": "2026-04-20",
}


def main() -> None:
    target: Path = ASSETS_PAPER_DIR / "10.1038_s41467-026-70288-4" / "details.json"
    target.write_text(
        data=json.dumps(obj=POLEGPOLSKY_DETAILS, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("wrote:", target)


if __name__ == "__main__":
    main()
