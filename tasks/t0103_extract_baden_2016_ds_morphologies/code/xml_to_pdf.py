"""Convert the NCBI PMC fulltext XML for Baden 2016 into a clean PDF.

The publisher PDF for Baden et al. 2016 (DOI 10.1038/nature16468) is paywalled
and the PMC/Europe PMC PDF endpoints either redirect to JS-protected pages or
report `Failed to retrieve PDF`. The full text is however available as PMC
fulltext XML (NCBI EFetch, db=pmc, id=4724341). This script transforms that
XML into a typeset PDF rendition that serves as the canonical paper file for
the paper asset.

Only structural text content (title, authors, affiliations, abstract,
hierarchical sections with paragraphs, methods, extended data text) is
preserved. Figures, tables, and references are omitted — readers needing the
visual figures should consult the publisher landing page recorded in
`details.json` `url`.

Usage:
    uv run python -u tasks/.../code/xml_to_pdf.py
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass

import typst

from tasks.t0103_extract_baden_2016_ds_morphologies.code.paths import (
    PAPER_PDF_PATH,
    PAPER_TYPST_PATH,
    PAPER_XML_PATH,
)


@dataclass(frozen=True, slots=True)
class Section:
    heading: str
    level: int
    paragraphs: list[str]


def _text_of(el: ET.Element) -> str:
    parts: list[str] = []
    if el.text is not None:
        parts.append(el.text)
    for c in el:
        parts.append(_text_of(c))
        if c.tail is not None:
            parts.append(c.tail)
    return "".join(parts)


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _find_first(el: ET.Element, name: str) -> ET.Element | None:
    for sub in el.iter():
        if sub.tag.endswith(name):
            return sub
    return None


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _walk_sections(el: ET.Element, level: int = 1) -> list[Section]:
    sections: list[Section] = []
    for sub in list(el):
        if _local(sub.tag) == "sec":
            heading_el = None
            for c in sub:
                if _local(c.tag) == "title":
                    heading_el = c
                    break
            heading = _clean(_text_of(heading_el)) if heading_el is not None else ""
            paragraphs: list[str] = []
            for c in sub:
                if _local(c.tag) == "p":
                    text = _clean(_text_of(c))
                    if len(text) > 0:
                        paragraphs.append(text)
            sections.append(Section(heading=heading, level=level, paragraphs=paragraphs))
            sections.extend(_walk_sections(el=sub, level=level + 1))
    return sections


def _escape_typst(text: str) -> str:
    replacements: list[tuple[str, str]] = [
        ("\\", "\\\\"),
        ("#", "\\#"),
        ("$", "\\$"),
        ("@", "\\@"),
        ("*", "\\*"),
        ("_", "\\_"),
        ("`", "\\`"),
        ("<", "\\<"),
        (">", "\\>"),
        ("=", "\\="),
        ("[", "\\["),
        ("]", "\\]"),
    ]
    out = text
    for old, new in replacements:
        out = out.replace(old, new)
    return out


def _extract_authors(root: ET.Element) -> list[str]:
    authors: list[str] = []
    for contrib in root.iter():
        if _local(contrib.tag) == "contrib":
            ctype = contrib.get("contrib-type", "")
            if ctype != "author":
                continue
            surname = None
            given = None
            for c in contrib.iter():
                if _local(c.tag) == "surname" and c.text is not None:
                    surname = c.text
                if _local(c.tag) == "given-names" and c.text is not None:
                    given = c.text
            if surname is not None:
                name = surname if given is None else f"{given} {surname}"
                authors.append(name)
    return authors


def _extract_abstract(root: ET.Element) -> str:
    abs_el = _find_first(el=root, name="abstract")
    if abs_el is None:
        return ""
    return _clean(_text_of(abs_el))


def _extract_title(root: ET.Element) -> str:
    title_el = _find_first(el=root, name="article-title")
    return _clean(_text_of(title_el)) if title_el is not None else ""


def _build_typst_source(
    *,
    title: str,
    authors: list[str],
    abstract: str,
    sections: list[Section],
) -> str:
    lines: list[str] = []
    lines.append('#set page(paper: "a4", margin: 2cm)')
    lines.append('#set text(font: "DejaVu Sans", size: 10pt)')
    lines.append("#set par(justify: true, leading: 0.65em)")
    lines.append("")
    lines.append(f'#align(center)[#text(size: 16pt, weight: "bold")[{_escape_typst(title)}]]')
    lines.append("")
    if len(authors) > 0:
        lines.append(
            '#align(center)[#text(size: 10pt, style: "italic")['
            f"{_escape_typst(', '.join(authors))}]]"
        )
        lines.append("")
    lines.append(
        "#align(center)[#text(size: 9pt)[Baden et al. 2016. "
        "Nature 529(7586):345-350. DOI: 10.1038/nature16468.]]"
    )
    lines.append("")
    lines.append("#line(length: 100%)")
    lines.append("")
    if len(abstract) > 0:
        lines.append("== Abstract")
        lines.append("")
        lines.append(_escape_typst(abstract))
        lines.append("")
    for sec in sections:
        if len(sec.heading) == 0 and len(sec.paragraphs) == 0:
            continue
        prefix = "=" * min(sec.level + 1, 6)
        if len(sec.heading) > 0:
            lines.append(f"{prefix} {_escape_typst(sec.heading)}")
            lines.append("")
        for p in sec.paragraphs:
            lines.append(_escape_typst(p))
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    tree = ET.parse(PAPER_XML_PATH)
    root = tree.getroot()

    title = _extract_title(root=root)
    authors = _extract_authors(root=root)
    abstract = _extract_abstract(root=root)
    body_el = _find_first(el=root, name="body")
    sections: list[Section] = []
    if body_el is not None:
        sections = _walk_sections(el=body_el, level=1)

    typst_source = _build_typst_source(
        title=title,
        authors=authors,
        abstract=abstract,
        sections=sections,
    )
    PAPER_TYPST_PATH.write_text(typst_source, encoding="utf-8")
    typst.compile(input=str(PAPER_TYPST_PATH), output=str(PAPER_PDF_PATH))
    pdf_bytes = PAPER_PDF_PATH.stat().st_size
    print(f"Wrote {PAPER_PDF_PATH} ({pdf_bytes} bytes)")
    print(f"Sections: {len(sections)}, authors: {len(authors)}")


if __name__ == "__main__":
    main()
