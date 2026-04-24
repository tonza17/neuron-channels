"""One-shot helper to prepend ModelDB-189347 provenance to .hoc and .mod files.

Idempotent: if the marker already exists, the file is not modified again.
Operates on the verbatim ModelDB sources copied from t0008 into
``code/sources/`` and mirrors them into the library asset's ``sources/``.

This is a build helper, not part of the library's runtime API.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

PROVENANCE_MARKER: str = "PROVENANCE: ModelDB accession 189347"
PROVENANCE_HEADER_HOC: str = (
    "// PROVENANCE: ModelDB accession 189347\n"
    "// Commit SHA: 87d669dcef18e9966e29c88520ede78bc16d36ff\n"
    "// Authored: 2019-05-31 by tommorse\n"
    "// Source mirror: https://github.com/ModelDBRepository/189347\n"
    "// Verbatim copy in this task: tasks/"
    "t0046_reproduce_poleg_polsky_2016_exact/code/sources/\n"
    "// Library mirror: assets/library/modeldb_189347_dsgc_exact/sources/\n"
    "//\n"
)
PROVENANCE_HEADER_MOD: str = (
    "COMMENT\n"
    "PROVENANCE: ModelDB accession 189347\n"
    "Commit SHA: 87d669dcef18e9966e29c88520ede78bc16d36ff\n"
    "Authored: 2019-05-31 by tommorse\n"
    "Source mirror: https://github.com/ModelDBRepository/189347\n"
    "Verbatim copy in this task: tasks/"
    "t0046_reproduce_poleg_polsky_2016_exact/code/sources/\n"
    "Library mirror: assets/library/modeldb_189347_dsgc_exact/sources/\n"
    "ENDCOMMENT\n"
)

CODE_SOURCES: Path = Path(__file__).resolve().parent / "sources"
LIBRARY_SOURCES: Path = (
    Path(__file__).resolve().parent.parent
    / "assets"
    / "library"
    / "modeldb_189347_dsgc_exact"
    / "sources"
)

PROVENANCE_FILES: tuple[str, ...] = (
    "main.hoc",
    "RGCmodel.hoc",
    "mosinit.hoc",
    "HHst.mod",
    "bipolarNMDA.mod",
    "SAC2RGCinhib.mod",
    "SAC2RGCexc.mod",
    "SquareInput.mod",
    "spike.mod",
)

PASSTHROUGH_FILES: tuple[str, ...] = (
    "model.ses",
    "readme.html",
    "readme.docx",
)


def _strip_existing_marker(*, text: str) -> str:
    """Remove any earlier provenance header that used the wrong (//) syntax."""
    if "// PROVENANCE: ModelDB accession 189347" not in text:
        return text
    lines: list[str] = text.splitlines(keepends=True)
    out: list[str] = []
    skip: bool = True
    for line in lines:
        if skip and (line.startswith("//") or line.strip() == ""):
            continue
        skip = False
        out.append(line)
    return "".join(out)


def _prepend_provenance(*, file_path: Path) -> bool:
    raw_bytes: bytes = file_path.read_bytes()
    try:
        text: str = raw_bytes.decode(encoding="utf-8")
    except UnicodeDecodeError:
        # Some MOD files were authored with windows-1252 line endings.
        text = raw_bytes.decode(encoding="windows-1252")
    is_mod: bool = file_path.suffix.lower() == ".mod"
    expected_header: str = PROVENANCE_HEADER_MOD if is_mod else PROVENANCE_HEADER_HOC
    # If the file already starts with the right header, nothing to do.
    if text.startswith(expected_header):
        return False
    text = _strip_existing_marker(text=text)
    new_text: str = expected_header + text
    file_path.write_text(data=new_text, encoding="utf-8")
    return True


def main() -> int:
    LIBRARY_SOURCES.mkdir(parents=True, exist_ok=True)
    n_changed: int = 0
    for file_name in PROVENANCE_FILES:
        src_path: Path = CODE_SOURCES / file_name
        if not src_path.exists():
            print(f"[skip] {src_path} not present", flush=True)
            continue
        if _prepend_provenance(file_path=src_path):
            n_changed += 1
            print(f"[edit] {src_path}", flush=True)
        # Mirror into library asset sources.
        dst_path: Path = LIBRARY_SOURCES / file_name
        shutil.copyfile(src=src_path, dst=dst_path)
        print(f"[copy] {src_path} -> {dst_path}", flush=True)
    for file_name in PASSTHROUGH_FILES:
        src_path = CODE_SOURCES / file_name
        if not src_path.exists():
            print(f"[skip] {src_path} not present", flush=True)
            continue
        dst_path = LIBRARY_SOURCES / file_name
        shutil.copyfile(src=src_path, dst=dst_path)
        print(f"[copy] {src_path} -> {dst_path}", flush=True)
    print(f"\nChanged {n_changed} files; mirrored to {LIBRARY_SOURCES}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
