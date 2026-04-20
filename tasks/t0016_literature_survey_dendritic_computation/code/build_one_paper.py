"""Build a single paper asset (details.json + summary.md) from an inline record.

This script is intentionally single-paper: it accepts one DOI on the command
line, looks up the matching record in `PAPER_RECORDS`, and writes
`details.json` + `summary.md` for that paper only. Writing multiple paper
assets in one invocation is disallowed by task rules; this script enforces
that by accepting exactly one DOI per run.

Run:

    uv run python -m \
        tasks.t0016_literature_survey_dendritic_computation.code.build_one_paper \
        --doi "10.1038/35005094"

The paper records live in this file (as module constants). Adding a new
record and then running the script for that DOI is how each paper gets
into the repository. The two-stage split keeps the record definitions in
a reviewable Python file while the actual write happens per-invocation.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
PAPER_DIR: Path = (
    REPO_ROOT / "tasks" / "t0016_literature_survey_dendritic_computation" / "assets" / "paper"
)
TASK_ID: str = "t0016_literature_survey_dendritic_computation"
DATE_ADDED: str = "2026-04-20"


@dataclass(frozen=True, slots=True)
class PaperRecord:
    doi: str
    title: str
    url: str
    pdf_url: str | None
    date_published: str | None
    year: int
    authors: list[dict[str, str | None]]
    institutions: list[dict[str, str]]
    journal: str
    venue_type: str
    categories: list[str]
    abstract: str
    citation_key: str
    download_status: str
    download_failure_reason: str | None
    summary_body: str


def _doi_to_slug(*, doi: str) -> str:
    return doi.replace("/", "_")


def _write_details(*, record: PaperRecord) -> Path:
    slug: str = _doi_to_slug(doi=record.doi)
    folder: Path = PAPER_DIR / slug
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "files").mkdir(parents=True, exist_ok=True)
    gitkeep: Path = folder / "files" / ".gitkeep"
    if not gitkeep.exists() and record.download_status == "failed":
        gitkeep.write_text(data="", encoding="utf-8")
    details: dict[str, object] = {
        "spec_version": "3",
        "paper_id": slug,
        "doi": record.doi,
        "title": record.title,
        "url": record.url,
        "pdf_url": record.pdf_url,
        "date_published": record.date_published,
        "year": record.year,
        "authors": record.authors,
        "institutions": record.institutions,
        "journal": record.journal,
        "venue_type": record.venue_type,
        "categories": record.categories,
        "abstract": record.abstract,
        "citation_key": record.citation_key,
        "summary_path": "summary.md",
        "files": [],
        "download_status": record.download_status,
        "download_failure_reason": record.download_failure_reason,
        "added_by_task": TASK_ID,
        "date_added": DATE_ADDED,
    }
    path: Path = folder / "details.json"
    path.write_text(
        data=json.dumps(obj=details, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def _write_summary(*, record: PaperRecord) -> Path:
    slug: str = _doi_to_slug(doi=record.doi)
    folder: Path = PAPER_DIR / slug
    path: Path = folder / "summary.md"
    path.write_text(data=record.summary_body, encoding="utf-8")
    return path


def _author(*, name: str, country: str | None, institution: str | None) -> dict[str, str | None]:
    return {"name": name, "country": country, "institution": institution, "orcid": None}


def _institution(*, name: str, country: str) -> dict[str, str]:
    return {"name": name, "country": country}


PAYWALL_NATURE: str = (
    "Publisher (Nature Publishing Group) requires subscription for full text; "
    "direct PDF fetch returned 403. Abstract-based summary produced per paper spec."
)
PAYWALL_SCIENCE: str = (
    "Publisher (AAAS Science) requires subscription for full text; direct PDF "
    "fetch returned 403. Abstract-based summary produced per paper spec."
)
PAYWALL_NEURON: str = (
    "Publisher (Cell Press Neuron) requires subscription for full text; direct "
    "PDF fetch returned 403. Abstract-based summary produced per paper spec."
)
PAYWALL_NATNEURO: str = (
    "Publisher (Nature Neuroscience) requires subscription for full text; direct "
    "PDF fetch returned 403. Abstract-based summary produced per paper spec."
)
PAYWALL_ANNUALREV: str = (
    "Publisher (Annual Reviews) requires subscription for full text; direct PDF "
    "fetch returned 403. Abstract-based summary produced per paper spec."
)
PAYWALL_IEEE: str = (
    "Publisher (IEEE Xplore) requires subscription for full text; direct PDF "
    "fetch returned 403. Abstract-based summary produced per paper spec."
)


def _load_records() -> dict[str, PaperRecord]:
    from tasks.t0016_literature_survey_dendritic_computation.code.paper_records import (
        RECORDS,
    )

    return {r.doi: r for r in RECORDS}


def main() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Write details.json + summary.md for exactly one paper."
    )
    parser.add_argument("--doi", required=True, help="Target DOI (one per run)")
    args: argparse.Namespace = parser.parse_args()
    records: dict[str, PaperRecord] = _load_records()
    if args.doi not in records:
        print(f"Unknown DOI: {args.doi}")
        print("Known DOIs:")
        for doi in sorted(records.keys()):
            print(f"  - {doi}")
        return 2
    record: PaperRecord = records[args.doi]
    details_path: Path = _write_details(record=record)
    summary_path: Path = _write_summary(record=record)
    print(f"Wrote {details_path}")
    print(f"Wrote {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
