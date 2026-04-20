"""Fetch CrossRef metadata for the patch-clamp shortlist and emit compact JSON."""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

SHORTLIST: list[tuple[str, str, int]] = [
    ("10.1038/nature00931", "Euler2002", 5),
    ("10.1016/0165-0270(94)00116-x", "Kyrozis1995", 1),
    ("10.3791/50400", "Huang2013", 1),
    ("10.1152/jn.1996.75.5.2129", "Velte1996", 3),
    ("10.1371/journal.pone.0019463", "PolegPolsky2011", 3),
    ("10.1016/j.neuroscience.2021.08.024", "To2022", 3),
    ("10.1126/sciadv.abb6642", "Werginz2020", 1),
    ("10.1016/j.neuron.2017.09.058", "Sethuramanujam2017b", 2),
    ("10.1016/j.neuron.2012.08.041", "RivlinEtzion2012", 4),
    ("10.1523/JNEUROSCI.0130-07.2007", "Margolis2007", 1),
    ("10.1113/jphysiol.2001.013009", "OBrien2002", 1),
    ("10.1016/j.neuron.2016.01.024", "Yonehara2016", 4),
    ("10.1523/JNEUROSCI.0933-15.2015", "Pei2015", 2),
    ("10.1113/jphysiol.2014.276543", "Stafford2014", 2),
    ("10.1523/JNEUROSCI.1241-13.2013", "Borghuis2013", 5),
    ("10.1111/ejn.14343", "Percival2019", 4),
    ("10.1371/journal.pone.0103822", "Grzywacz2014", 4),
    ("10.1109/TNS.2004.832706", "Litke2004", 4),
    ("10.1073/pnas.0907178107", "Pang2010", 2),
    ("10.1038/nn.3404", "Trenholm2013", 4),
]


@dataclass(frozen=True, slots=True)
class MetadataRecord:
    doi: str
    citation_key: str
    theme: int
    payload: dict


def fetch_crossref(*, doi: str) -> dict:
    url: str = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(
        url=url,
        headers={"User-Agent": "neuron-channels-research/1.0 (mailto:a.nikolaev@sheffield.ac.uk)"},
    )
    with urllib.request.urlopen(url=req, timeout=20) as response:
        raw: bytes = response.read()
    return json.loads(raw)["message"]


def main() -> None:
    out_path: Path = Path("tasks/t0017_literature_survey_patch_clamp/plan/crossref_metadata.json")
    records: list[dict] = []
    for doi, ckey, theme in SHORTLIST:
        try:
            payload: dict = fetch_crossref(doi=doi)
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
