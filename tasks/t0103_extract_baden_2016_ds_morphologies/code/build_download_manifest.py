"""Build `data/download_manifest.json` from the files actually downloaded.

Records SHA-256, byte size, and source URL for every file under
`data/` and the paper PDF asset file. The script is idempotent — running
it again rewrites the manifest with the current file inventory.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from tasks.t0103_extract_baden_2016_ds_morphologies.code.paths import (
    DATA_DIR,
    DOWNLOAD_MANIFEST_PATH,
    PAPER_PDF_PATH,
    TASK_ROOT,
)

_PAPER_PDF_REL = "assets/paper/10.1038_nature16468/files/baden_2016_functional_diversity_rgc.pdf"

KNOWN_SOURCES: dict[str, str] = {
    "data/Baden_et_al_2016_visualization.zip": (
        "http://retinal-functomics.net/wp-content/uploads/2015/12/"
        "Baden_et_al_2016_visualization.zip"
    ),
    "data/visualization_code/plotOverview.m": ("extracted from Baden_et_al_2016_visualization.zip"),
    "data/visualization_code/plotStamp.m": ("extracted from Baden_et_al_2016_visualization.zip"),
    "data/visualization_code/shadedErrorBar.m": (
        "extracted from Baden_et_al_2016_visualization.zip"
    ),
    "data/baden_2016_fulltext.xml": (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=4724341"
        "&rettype=full&retmode=xml"
    ),
    "data/baden_2016_fulltext.txt": (
        "derived from data/baden_2016_fulltext.xml via xml.etree.ElementTree text extraction"
    ),
    "data/baden_2016_paper.typ": (
        "derived from data/baden_2016_fulltext.xml by code/xml_to_pdf.py"
    ),
    _PAPER_PDF_REL: (
        "derived from data/baden_2016_fulltext.xml by code/xml_to_pdf.py "
        "(publisher PDF at https://www.nature.com/articles/nature16468 is paywalled; "
        "PMC PDF endpoint is JS-protected)"
    ),
}


@dataclass(frozen=True, slots=True)
class ManifestEntry:
    path: str
    bytes: int
    sha256: str
    source: str


def _sha256_of(file_path: Path) -> str:
    h = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _iter_files() -> list[Path]:
    files: list[Path] = []
    if DATA_DIR.exists():
        for f in DATA_DIR.rglob("*"):
            if f.is_file():
                files.append(f)
    if PAPER_PDF_PATH.exists():
        files.append(PAPER_PDF_PATH)
    return files


def main() -> None:
    entries: list[ManifestEntry] = []
    files = _iter_files()
    for f in sorted(files):
        rel = f.relative_to(TASK_ROOT).as_posix()
        source = KNOWN_SOURCES.get(rel, "internal_generated")
        entries.append(
            ManifestEntry(
                path=rel,
                bytes=f.stat().st_size,
                sha256=_sha256_of(file_path=f),
                source=source,
            )
        )
    out: dict[str, object] = {
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "task_id": "t0103_extract_baden_2016_ds_morphologies",
        "note": (
            "Records every file in data/ plus the paper PDF asset file. "
            "The Dryad bundle files (BadenEtAl_RGCs_2016_v1.mat and the "
            "Dryad README PDF) are NOT in this manifest because the Dryad "
            "v2 API and download endpoints rejected unauthenticated CLI "
            "downloads. See intervention/dryad_download_blocked.json."
        ),
        "entries": [
            {
                "path": e.path,
                "bytes": e.bytes,
                "sha256": e.sha256,
                "source": e.source,
            }
            for e in entries
        ],
    }
    DOWNLOAD_MANIFEST_PATH.write_text(
        json.dumps(out, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {DOWNLOAD_MANIFEST_PATH} with {len(entries)} entries.")


if __name__ == "__main__":
    main()
