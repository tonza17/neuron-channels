"""Compile the Typst source for the t0076 detailed writeup into PDF.

COPIED verbatim from ``tasks/t0072_synaptic_traces_pd_nd/code/render_pdf.py`` with
the ``paths`` import retargeted to
``tasks.t0076_bedb_dsi_firing_rate_mobo.code.paths``.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import typst

from tasks.t0076_bedb_dsi_firing_rate_mobo.code.paths import (
    PDF_OUTPUT_PATH,
    TYPST_SOURCE_PATH,
)

MIN_PDF_SIZE_BYTES: int = 50_000


@dataclass(frozen=True, slots=True)
class CompileResult:
    source_path: Path
    output_path: Path
    output_size_bytes: int


def compile_typst(*, source_path: Path, output_path: Path) -> CompileResult:
    assert source_path.exists(), f"typst source missing at {source_path}"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    typst.compile(str(source_path), output=str(output_path))
    assert output_path.exists(), f"typst.compile produced no PDF at {output_path}"
    size_bytes: int = output_path.stat().st_size
    return CompileResult(
        source_path=source_path,
        output_path=output_path,
        output_size_bytes=size_bytes,
    )


def main() -> int:
    result: CompileResult = compile_typst(
        source_path=TYPST_SOURCE_PATH,
        output_path=PDF_OUTPUT_PATH,
    )
    print(f"Compiled: {result.source_path}")
    print(f"Output:   {result.output_path}")
    print(f"Size:     {result.output_size_bytes} bytes")
    if result.output_size_bytes < MIN_PDF_SIZE_BYTES:
        print(
            f"WARNING: PDF is smaller than the {MIN_PDF_SIZE_BYTES}-byte threshold; "
            "verify equations and figures rendered correctly.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
