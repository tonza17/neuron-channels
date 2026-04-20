"""Fetch CrossRef metadata for the synaptic-integration shortlist and emit compact JSON."""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SHORTLIST: list[tuple[str, str, int]] = [
    ("10.1038/346565a0", "Lester1990", 1),
    ("10.1073/pnas.80.9.2799", "KochPoggio1983", 2),
    ("10.1038/nature02116", "WehrZador2003", 3),
    ("10.1016/s0959-4388(03)00075-8", "HausserMel2003", 4),
    ("10.1038/nature00931", "EulerDetwilerDenk2002", 5),
]


@dataclass(frozen=True, slots=True)
class MetadataRecord:
    doi: str
    citation_key: str
    theme: int
    payload: dict[str, Any]


def fetch_crossref(*, doi: str) -> dict[str, Any]:
    url: str = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(
        url=url,
        headers={"User-Agent": "neuron-channels-research/1.0 (mailto:a.nikolaev@sheffield.ac.uk)"},
    )
    with urllib.request.urlopen(url=req, timeout=20) as response:
        raw: bytes = response.read()
    result: dict[str, Any] = json.loads(raw)["message"]
    return result


def main() -> None:
    out_path: Path = Path(
        "tasks/t0018_literature_survey_synaptic_integration/plan/crossref_metadata.json",
    )
    records: list[dict[str, Any]] = []
    for doi, ckey, theme in SHORTLIST:
        try:
            payload: dict[str, Any] = fetch_crossref(doi=doi)
            records.append(
                {
                    "doi": doi,
                    "citation_key": ckey,
                    "theme": theme,
                    "status": "ok",
                    "payload": payload,
                }
            )
            print(f"OK   {doi}", flush=True)
        except (urllib.error.URLError, json.JSONDecodeError) as exc:
            records.append(
                {
                    "doi": doi,
                    "citation_key": ckey,
                    "theme": theme,
                    "status": "error",
                    "error": str(exc),
                }
            )
            print(f"FAIL {doi}: {exc}", file=sys.stderr, flush=True)
        time.sleep(0.3)
    out_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
