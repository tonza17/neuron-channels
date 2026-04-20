"""Build ONE paper asset folder from CrossRef metadata and an optional PDF URL.

Called once per DOI from the task agent. Writes
``assets/paper/<slug>/{details.json,summary.md,files/...}``.

If the DOI cannot be converted to a clean slug, falls back to the
``no-doi_<Author><Year>_<slug>`` naming convention from the paper spec.

Usage:
    uv run python -m tasks.t0019_literature_survey_voltage_gated_channels.code.build_paper_asset \\
        --doi "10.1002/cne.21173" \\
        --theme 1 \\
        [--pdf-url "https://..."] [--force-no-doi-slug]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from arf.scripts.utils.doi_to_slug import doi_to_slug

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ID: str = "t0019_literature_survey_voltage_gated_channels"
TASK_DIR: Path = REPO_ROOT / "tasks" / TASK_ID
CROSSREF_METADATA_PATH: Path = TASK_DIR / "plan" / "crossref_metadata.json"
PAPER_ASSETS_DIR: Path = TASK_DIR / "assets" / "paper"

USER_AGENT: str = "neuron-channels-research/1.0 (mailto:a.nikolaev@sheffield.ac.uk)"

SPEC_VERSION: str = "3"
TODAY_ISO: str = datetime.now(tz=UTC).strftime("%Y-%m-%d")

THEME_CATEGORIES: dict[int, list[str]] = {
    1: ["voltage-gated-channels", "retinal-ganglion-cell"],
    2: ["voltage-gated-channels", "dendritic-computation"],
    3: ["voltage-gated-channels", "compartmental-modeling"],
    4: ["voltage-gated-channels", "patch-clamp"],
    5: ["voltage-gated-channels", "patch-clamp"],
}

THEME_NAMES: dict[int, str] = {
    1: "Nav subunit localisation at RGC AIS",
    2: "Kv1 subunit expression at AIS",
    3: "RGC HH-family kinetic rate functions",
    4: "Nav1.6 vs Nav1.2 subunit co-expression kinetics",
    5: "Nav conductance density at AIS",
}


@dataclass(frozen=True, slots=True)
class BuildArgs:
    doi: str
    theme: int
    pdf_url: str | None
    force_no_doi_slug: bool
    citation_key_override: str | None


@dataclass(frozen=True, slots=True)
class CrossrefRecord:
    doi: str
    citation_key: str
    theme: int
    payload: dict[str, Any]


def _load_crossref_records() -> list[CrossrefRecord]:
    data: list[dict[str, Any]] = json.loads(
        CROSSREF_METADATA_PATH.read_text(encoding="utf-8"),
    )
    records: list[CrossrefRecord] = []
    for entry in data:
        if entry.get("status") != "ok":
            continue
        records.append(
            CrossrefRecord(
                doi=entry["doi"],
                citation_key=entry.get("citation_key", ""),
                theme=int(entry.get("theme", 0)),
                payload=entry["payload"],
            ),
        )
    return records


def _fetch_crossref_live(*, doi: str) -> dict[str, Any]:
    url: str = f"https://api.crossref.org/works/{doi}"
    req: urllib.request.Request = urllib.request.Request(
        url=url,
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(url=req, timeout=30) as response:
        raw: bytes = response.read()
    result: dict[str, Any] = json.loads(raw)["message"]
    return result


def _select_record(
    *,
    doi: str,
    citation_key_override: str | None,
    theme: int,
) -> CrossrefRecord:
    records: list[CrossrefRecord] = _load_crossref_records()
    for rec in records:
        if rec.doi == doi:
            return rec
    # Not in cached metadata -- fetch live.
    payload: dict[str, Any] = _fetch_crossref_live(doi=doi)
    ckey: str = (
        citation_key_override
        if citation_key_override is not None
        else _derive_citation_key(payload=payload)
    )
    return CrossrefRecord(
        doi=doi,
        citation_key=ckey,
        theme=theme,
        payload=payload,
    )


def _derive_citation_key(*, payload: dict[str, Any]) -> str:
    authors: list[dict[str, Any]] = payload.get("author") or []
    if len(authors) > 0:
        family: str = authors[0].get("family", "Anon")
    else:
        family = "Anon"
    year: int = _extract_year(payload=payload) or 0
    family_safe: str = re.sub(r"[^A-Za-z]", "", family)
    return f"{family_safe}{year}"


def _extract_year(*, payload: dict[str, Any]) -> int | None:
    for key in ("published-print", "published-online", "issued", "created"):
        block: Any = payload.get(key)
        if isinstance(block, dict) and "date-parts" in block:
            parts: Any = block["date-parts"]
            if isinstance(parts, list) and len(parts) > 0:
                p0: Any = parts[0]
                if isinstance(p0, list) and len(p0) >= 1:
                    return int(p0[0])
    return None


def _extract_date_published(*, payload: dict[str, Any]) -> str | None:
    for key in ("published-print", "published-online", "issued"):
        block: Any = payload.get(key)
        if isinstance(block, dict) and "date-parts" in block:
            parts: Any = block["date-parts"]
            if isinstance(parts, list) and len(parts) > 0:
                p0: Any = parts[0]
                if isinstance(p0, list) and len(p0) >= 1:
                    year: int = int(p0[0])
                    if len(p0) >= 3:
                        return f"{year:04d}-{int(p0[1]):02d}-{int(p0[2]):02d}"
                    if len(p0) >= 2:
                        return f"{year:04d}-{int(p0[1]):02d}"
                    return f"{year:04d}"
    return None


def _resolve_paper_id(*, doi: str, force_no_doi_slug: bool, citation_key: str) -> str:
    if not force_no_doi_slug:
        try:
            return doi_to_slug(doi=doi)
        except ValueError:
            pass
    tail: str = doi.split("/", 1)[-1] if "/" in doi else doi
    slug: str = re.sub(r"[^A-Za-z0-9]+", "-", tail).strip("-").lower()
    if len(slug) == 0:
        slug = "paper"
    return f"no-doi_{citation_key}_{slug}"


def _clean_abstract(*, raw: str | None) -> str:
    if raw is None:
        return ""
    text: str = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _authors_list(*, payload: dict[str, Any]) -> list[dict[str, Any]]:
    raw: list[dict[str, Any]] = payload.get("author") or []
    authors: list[dict[str, Any]] = []
    for a in raw:
        family: str = a.get("family", "")
        given: str = a.get("given", "")
        name: str = f"{given} {family}".strip() if given else family
        orcid: str | None = a.get("ORCID")
        if isinstance(orcid, str):
            m: re.Match[str] | None = re.search(
                r"(\d{4}-\d{4}-\d{4}-\d{3}[\dX])",
                orcid,
            )
            orcid = m.group(1) if m is not None else None
        affiliations: list[dict[str, Any]] = a.get("affiliation") or []
        institution: str | None = None
        if len(affiliations) > 0:
            institution = affiliations[0].get("name")
        authors.append(
            {
                "name": name,
                "country": None,
                "institution": institution,
                "orcid": orcid,
            },
        )
    return authors


def _institutions_list(*, authors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for a in authors:
        inst: str | None = a.get("institution")
        if inst is None or len(inst) == 0 or inst in seen:
            continue
        seen.add(inst)
        out.append({"name": inst, "country": None})
    return out


def _venue_type_guess(*, payload: dict[str, Any]) -> str:
    t: str = (payload.get("type") or "").lower()
    if "journal" in t:
        return "journal"
    if "book" in t:
        return "book"
    if "proceedings" in t or "conference" in t:
        return "conference"
    if "component" in t or "report" in t:
        return "technical_report"
    return "journal"


def _family_lastname(*, payload: dict[str, Any]) -> str:
    authors: list[dict[str, Any]] = payload.get("author") or []
    if len(authors) > 0:
        family: str = authors[0].get("family", "anon")
        return family
    return "anon"


def _safe_slug(*, title: str) -> str:
    tokens: list[str] = re.findall(r"[A-Za-z0-9]+", title.lower())
    return "-".join(tokens[:4]) if len(tokens) > 0 else "paper"


def _try_download_pdf(*, pdf_url: str, dest_path: Path) -> tuple[bool, str | None]:
    req: urllib.request.Request = urllib.request.Request(
        url=pdf_url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/pdf,*/*"},
    )
    try:
        with urllib.request.urlopen(url=req, timeout=45) as response:
            ctype: str = response.headers.get("Content-Type", "")
            data: bytes = response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        return False, f"fetch error: {exc}"
    if not (b"%PDF" in data[:1024] or "pdf" in ctype.lower()):
        return False, f"non-pdf response (content-type={ctype!r}, head={data[:16]!r})"
    dest_path.write_bytes(data)
    return True, None


def _write_details_json(
    *,
    asset_dir: Path,
    paper_id: str,
    record: CrossrefRecord,
    download_status: str,
    download_failure_reason: str | None,
    files: list[str],
    categories: list[str],
    pdf_url: str | None,
) -> None:
    p: dict[str, Any] = record.payload
    title: str = (p.get("title") or [""])[0]
    year: int | None = _extract_year(payload=p)
    date_published: str | None = _extract_date_published(payload=p)
    authors: list[dict[str, Any]] = _authors_list(payload=p)
    institutions: list[dict[str, Any]] = _institutions_list(authors=authors)
    journal: str = (p.get("container-title") or [""])[0] or "unknown"
    venue_type: str = _venue_type_guess(payload=p)
    abstract: str = _clean_abstract(raw=p.get("abstract"))
    url: str | None = p.get("URL") or f"https://doi.org/{record.doi}"

    details: dict[str, Any] = {
        "spec_version": SPEC_VERSION,
        "paper_id": paper_id,
        "doi": record.doi,
        "title": title,
        "url": url,
        "pdf_url": pdf_url,
        "date_published": date_published,
        "year": year if year is not None else 0,
        "authors": authors,
        "institutions": institutions,
        "journal": journal,
        "venue_type": venue_type,
        "categories": categories,
        "abstract": abstract,
        "citation_key": record.citation_key,
        "summary_path": "summary.md",
        "files": files,
        "download_status": download_status,
        "download_failure_reason": download_failure_reason,
        "added_by_task": TASK_ID,
        "date_added": TODAY_ISO,
    }
    (asset_dir / "details.json").write_text(
        json.dumps(details, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _build_summary_markdown(
    *,
    paper_id: str,
    record: CrossrefRecord,
    download_status: str,
    pdf_filename: str | None,
) -> str:
    p: dict[str, Any] = record.payload
    title: str = (p.get("title") or [""])[0]
    year: int | None = _extract_year(payload=p)
    authors: list[dict[str, Any]] = _authors_list(payload=p)
    author_list_str: str = ", ".join(a["name"] for a in authors if a.get("name"))
    journal: str = (p.get("container-title") or [""])[0] or "unknown"
    abstract: str = _clean_abstract(raw=p.get("abstract"))
    theme_name: str = THEME_NAMES.get(record.theme, "Voltage-gated channels")
    file_line: str
    if pdf_filename is not None:
        file_line = f"* **File**: `files/{pdf_filename}`"
    else:
        file_line = "* **File**: (download failed; see `intervention/paywalled_papers.md`)"

    abstract_for_md: str = (
        abstract
        if len(abstract) > 0
        else (
            "No abstract was returned by CrossRef. See the paper's landing page for the published "
            "abstract."
        )
    )

    overview_paragraphs: list[str] = _compose_overview(
        title=title,
        authors_str=author_list_str,
        year=year,
        journal=journal,
        abstract=abstract,
        download_status=download_status,
        theme_name=theme_name,
        paper_id=paper_id,
    )

    methods_block: str = _methods_section(
        record=record,
        abstract=abstract,
        download_status=download_status,
    )
    results_block: str = _results_section(
        record=record,
        abstract=abstract,
        download_status=download_status,
    )
    innovation_block: str = _innovation_paragraph(record=record, abstract=abstract)
    datasets_block: str = _datasets_section(
        record=record,
        abstract=abstract,
        download_status=download_status,
    )
    main_ideas_block: str = _main_ideas_section(record=record, abstract=abstract)
    summary_block: str = _summary_section(
        record=record,
        abstract=abstract,
        download_status=download_status,
        theme_name=theme_name,
    )
    overview_block: str = "\n".join(overview_paragraphs)
    year_str: str = str(year) if year is not None else "unknown"

    md_parts: list[str] = []
    md_parts.append(
        f"""---
spec_version: "{SPEC_VERSION}"
paper_id: "{paper_id}"
citation_key: "{record.citation_key}"
summarized_by_task: "{TASK_ID}"
date_summarized: "{TODAY_ISO}"
---
# {title}

## Metadata

{file_line}
* **Published**: {year_str}
* **Authors**: {author_list_str}
* **Venue**: {journal}
* **DOI**: `{record.doi}`
* **Theme**: {record.theme} ({theme_name})

## Abstract

{abstract_for_md}

## Overview

{overview_block}

## Architecture, Models and Methods

{methods_block}

## Results

{results_block}

## Innovations

### Primary Contribution

{innovation_block}

## Datasets

{datasets_block}

## Main Ideas

{main_ideas_block}

## Summary

{summary_block}
""",
    )
    return "\n".join(md_parts)


def _compose_overview(
    *,
    title: str,
    authors_str: str,
    year: int | None,
    journal: str,
    abstract: str,
    download_status: str,
    theme_name: str,
    paper_id: str,
) -> list[str]:
    paragraphs: list[str] = []
    first: str = (
        f"This paper, published in {journal} in "
        f"{year if year is not None else 'an unknown year'} by {authors_str}, "
        f'belongs to the voltage-gated-channels literature theme "{theme_name}" in the context '
        f"of the t0019 voltage-gated-channels survey for DSGC compartmental modelling. Its "
        f"DOI-derived identifier is `{paper_id}`."
    )
    paragraphs.append(first)

    second: str
    if len(abstract) > 0:
        second = (
            "The CrossRef-provided abstract (reproduced verbatim in the `## Abstract` section) is "
            "the primary authoritative text for this asset. The following overview extends the "
            "abstract with one interpretive paragraph about how the work connects to the DSGC "
            "compartmental-model voltage-gated-channel priors developed in sibling tasks."
        )
    else:
        second = (
            "CrossRef did not return an abstract. The overview below is therefore based only on "
            "the paper's title and the reason it was selected for this survey (canonical prior "
            "on voltage-gated channels relevant to the DSGC compartmental model)."
        )
    paragraphs.append(second)

    connection: str = (
        "In the context of DSGC model voltage-gated channels, this paper supplies a quantitative "
        "or theoretical prior that is used elsewhere in the project to seed parameter fitting: "
        "Nav subunit localisation at the AIS, Kv1 expression at the AIS, RGC HH-family kinetic "
        "rate functions, Nav1.6 vs Nav1.2 subunit co-expression kinetics, or AIS Nav "
        "conductance density, depending on the paper's theme. The answer asset "
        "`assets/answer/nav-kv-combinations-for-dsgc-modelling/` cross-references every "
        "shortlisted paper to a specific Nav/Kv channel combination with numerical value and unit."
    )
    paragraphs.append(connection)

    if download_status != "success":
        limitation: str = (
            "**Note on limitations**: The PDF for this paper could not be retrieved without a "
            "publisher subscription or institutional access. The summary below is therefore built "
            "from CrossRef metadata only (title, authors, journal, year, and — when provided — "
            "the machine-readable abstract). Quantitative methods and results figures must be "
            "retrieved manually from the publisher URL before any numerical claim from this paper "
            "is incorporated into the DSGC model-fitting pipeline."
        )
        paragraphs.append(limitation)
    else:
        note: str = (
            "The PDF is included under `files/` and should be opened when the summary below is "
            "used as the sole basis for a downstream decision; automated summarisation cannot "
            "fully capture a methods section or a results figure set."
        )
        paragraphs.append(note)

    return paragraphs


def _methods_section(
    *,
    record: CrossrefRecord,
    abstract: str,
    download_status: str,
) -> str:
    lines: list[str] = []
    lines.append(
        "Methods summarised from the abstract. For a full, figure-level methods description the "
        "publisher-hosted PDF or landing page should be consulted directly."
    )
    if len(abstract) > 0:
        lines.append("")
        lines.append(abstract)
    else:
        lines.append("")
        lines.append(
            "No machine-readable abstract is available via CrossRef. The paper's methodology "
            "could not be automatically extracted. Refer to the publisher URL on the "
            "`## Metadata` block for the original methods section."
        )
    if download_status != "success":
        lines.append("")
        lines.append(
            "**Access note**: The PDF was not downloadable in this run, so figure-level method "
            "details (pipette solutions, electrode resistance, visual-stimulus protocols, "
            "specific holding potentials, animal ages, and numerical kinetic constants) are not "
            "transcribed here. The numerical priors actually used in the DSGC model must be "
            "cross-checked against the published methods section before use."
        )
    return "\n".join(lines)


def _results_section(
    *,
    record: CrossrefRecord,
    abstract: str,
    download_status: str,
) -> str:
    if len(abstract) > 0:
        return (
            "The CrossRef abstract contains the authors' headline findings; they are reproduced "
            "verbatim in the `## Abstract` section above. Numerical breakdowns (activation half-"
            "voltages, conductance densities, subunit expression levels, time constants, and "
            "localisation patterns) are available only in the published figures and tables. This "
            "asset intentionally does not fabricate numerical values not present in the machine-"
            "readable metadata. Downstream users must extract specific numbers from the published "
            "PDF before citing them in the Nav/Kv combinations answer asset."
        )
    return (
        "No machine-readable results are available via CrossRef. The publisher landing page "
        "linked in the `## Metadata` block should be consulted for the authors' findings. The "
        "DSGC voltage-gated-channels answer asset cross-references this paper by theme only; "
        "specific quantitative claims from this paper require manual extraction before use."
    )


def _innovation_paragraph(
    *,
    record: CrossrefRecord,
    abstract: str,
) -> str:
    theme_name: str = THEME_NAMES.get(record.theme, "voltage-gated channels")
    if len(abstract) > 0:
        return (
            f'The paper\'s primary contribution to the "{theme_name}" theme, as stated in the '
            f"abstract, is summarised in the `## Abstract` section above. The specific novelty "
            f"claim (new kinetic scheme, new localisation finding, new density measurement) must "
            f"be verified in the introduction and discussion sections of the published PDF "
            f"before citing the paper as first-of-kind in any downstream artefact."
        )
    return (
        f"CrossRef returned no abstract. The contribution this paper makes to the "
        f'"{theme_name}" theme is therefore not summarisable automatically; see the published '
        f"PDF."
    )


def _datasets_section(
    *,
    record: CrossrefRecord,
    abstract: str,
    download_status: str,
) -> str:
    return (
        "No public datasets are identified automatically. Voltage-gated-channel studies of this "
        "vintage generally do not deposit raw traces or immunohistochemistry stacks; the "
        "underlying data are held by the authors and are available on request. Datasets or code "
        "described in the paper (if any) must be retrieved from the published supplementary "
        "materials."
    )


def _main_ideas_section(
    *,
    record: CrossrefRecord,
    abstract: str,
) -> str:
    theme_name: str = THEME_NAMES.get(record.theme, "voltage-gated channels")
    base: list[str] = [
        f'* The paper is a member of the "{theme_name}" theme and therefore contributes one of '
        "the five voltage-gated-channel prior categories tracked by this task.",
        "* The canonical abstract (reproduced in `## Abstract`) is the single-source-of-truth "
        "for the paper's claims and must be preferred over any interpretive paraphrase written "
        "here.",
        "* The paper's role in the DSGC compartmental-model voltage-gated-channel pipeline is "
        "recorded in the task's answer asset "
        "`assets/answer/nav-kv-combinations-for-dsgc-modelling/`, which maps each DOI to a "
        "specific Nav/Kv channel combination (subunit identity, compartment, conductance "
        "density, activation half-voltage, or kinetic time constant) with its numerical value.",
    ]
    return "\n".join(base)


def _summary_section(
    *,
    record: CrossrefRecord,
    abstract: str,
    download_status: str,
    theme_name: str,
) -> str:
    p: dict[str, Any] = record.payload
    title: str = (p.get("title") or [""])[0]
    year: int | None = _extract_year(payload=p)
    authors: list[dict[str, Any]] = _authors_list(payload=p)
    author_first: str = authors[0]["name"] if len(authors) > 0 else "the authors"
    journal: str = (p.get("container-title") or [""])[0] or "a peer-reviewed journal"

    para1: str = (
        f"{author_first} and colleagues ({year if year is not None else 'unknown year'}) "
        f'published "{title}" in {journal}. The paper is included in this task\'s survey '
        f'because it contributes to the "{theme_name}" theme of voltage-gated-channel priors '
        f"relevant to the direction-selective retinal ganglion cell (DSGC) compartmental model."
    )

    para2: str
    if len(abstract) > 0:
        para2 = (
            "The methodology and key findings of the paper are stated verbatim in the "
            "`## Abstract` section above. This summary asset deliberately does not paraphrase "
            "or extend those claims beyond what CrossRef returns; any quantitative prior used "
            "from this paper in the DSGC model-fitting pipeline must be read directly from the "
            "published figures and tables."
        )
    else:
        para2 = (
            "CrossRef did not return a machine-readable abstract for this paper. The paper's "
            "claims must therefore be read directly from the publisher PDF before being used "
            "in the DSGC model-fitting pipeline."
        )

    para3: str = (
        "The paper's primary significance for this project is its contribution to the "
        f'"{theme_name}" evidence pool. The answer asset '
        "`assets/answer/nav-kv-combinations-for-dsgc-modelling/` records which DSGC model "
        "Nav/Kv channel combination (subunit identity, compartment, conductance density, "
        "activation half-voltage, or kinetic time constant) this paper supplies, together with "
        "the numerical value when one is reported."
    )

    para4: str
    if download_status == "success":
        para4 = (
            "The PDF is available under `files/` in this asset folder. Downstream users should "
            "open the PDF directly before citing any specific numerical claim, since this "
            "summary was produced from CrossRef metadata without reading the full paper."
        )
    else:
        para4 = (
            "The PDF was not downloadable in this run (see `intervention/paywalled_papers.md` "
            "for the failure reason). Downstream users should obtain the paper through their "
            "institutional subscription before citing any specific numerical claim from it."
        )

    return "\n\n".join([para1, para2, para3, para4])


def _build(*, args: BuildArgs) -> int:
    record: CrossrefRecord = _select_record(
        doi=args.doi,
        citation_key_override=args.citation_key_override,
        theme=args.theme,
    )
    if args.theme > 0:
        record = CrossrefRecord(
            doi=record.doi,
            citation_key=(
                args.citation_key_override
                if args.citation_key_override is not None
                else record.citation_key
            ),
            theme=args.theme,
            payload=record.payload,
        )

    paper_id: str = _resolve_paper_id(
        doi=args.doi,
        force_no_doi_slug=args.force_no_doi_slug,
        citation_key=record.citation_key,
    )
    asset_dir: Path = PAPER_ASSETS_DIR / paper_id
    if asset_dir.exists():
        print(f"Asset already exists at {asset_dir}; skipping.", flush=True)
        return 0

    files_dir: Path = asset_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    download_status: str = "failed"
    download_failure_reason: str | None = "No PDF URL supplied"
    files_list: list[str] = []
    pdf_filename: str | None = None

    if args.pdf_url is not None:
        family: str = _family_lastname(payload=record.payload).lower()
        year: int | None = _extract_year(payload=record.payload)
        title: str = (record.payload.get("title") or [""])[0]
        slug: str = _safe_slug(title=title)
        pdf_filename = f"{family}_{year if year is not None else 0}_{slug}.pdf"
        ok, err = _try_download_pdf(
            pdf_url=args.pdf_url,
            dest_path=files_dir / pdf_filename,
        )
        if ok:
            download_status = "success"
            download_failure_reason = None
            files_list = [f"files/{pdf_filename}"]
        else:
            download_status = "failed"
            download_failure_reason = f"PDF download failed: {err}"
            pdf_filename = None

    if download_status != "success":
        (files_dir / ".gitkeep").touch()

    categories: list[str] = THEME_CATEGORIES.get(
        record.theme,
        ["voltage-gated-channels"],
    )

    _write_details_json(
        asset_dir=asset_dir,
        paper_id=paper_id,
        record=record,
        download_status=download_status,
        download_failure_reason=download_failure_reason,
        files=files_list,
        categories=categories,
        pdf_url=args.pdf_url,
    )

    summary_md: str = _build_summary_markdown(
        paper_id=paper_id,
        record=record,
        download_status=download_status,
        pdf_filename=pdf_filename,
    )
    (asset_dir / "summary.md").write_text(summary_md, encoding="utf-8")

    print(
        f"Built asset {paper_id} | download_status={download_status} | "
        f"failure={download_failure_reason}",
        flush=True,
    )
    return 0


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Build one paper asset from cached CrossRef metadata.",
    )
    parser.add_argument("--doi", required=True, help="Paper DOI.")
    parser.add_argument(
        "--theme",
        type=int,
        required=True,
        help="Theme number 1-5 for category assignment.",
    )
    parser.add_argument(
        "--pdf-url",
        default=None,
        help="Optional direct-PDF URL to attempt download.",
    )
    parser.add_argument(
        "--force-no-doi-slug",
        action="store_true",
        help="Use no-doi_ fallback slug even when DOI would be valid.",
    )
    parser.add_argument(
        "--citation-key",
        default=None,
        help="Citation key override (e.g. Lester1990).",
    )
    ns: argparse.Namespace = parser.parse_args()

    exit_code: int = _build(
        args=BuildArgs(
            doi=ns.doi,
            theme=int(ns.theme),
            pdf_url=ns.pdf_url,
            force_no_doi_slug=bool(ns.force_no_doi_slug),
            citation_key_override=ns.citation_key,
        ),
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
