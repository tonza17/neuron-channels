"""Local lightweight verificator for the three answer assets produced by t0116.

The repo lacks a `verify_answer_asset` script, so this module checks the answer spec rules
manually: structural fields in `details.json`, presence of mandatory section headings in the
canonical short answer / full answer documents, the 2-5-sentence rule on the short answer's
`## Answer` block, and folder/slug consistency. Intended as a one-shot local check; not committed
output beyond stdout.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ANSWER_BASE: Path = (
    Path(__file__).resolve().parents[3]
    / "tasks"
    / "t0116_pooled_pca_cluster_factor_dsi07_pd10"
    / "assets"
    / "answer"
)

REQUIRED_DETAILS_FIELDS: tuple[str, ...] = (
    "spec_version",
    "answer_id",
    "question",
    "short_title",
    "short_answer_path",
    "full_answer_path",
    "categories",
    "answer_methods",
    "source_paper_ids",
    "source_urls",
    "source_task_ids",
    "confidence",
    "created_by_task",
    "date_created",
)

REQUIRED_SHORT_SECTIONS: tuple[str, ...] = ("## Question", "## Answer", "## Sources")
REQUIRED_FULL_SECTIONS: tuple[str, ...] = (
    "## Question",
    "## Short Answer",
    "## Research Process",
    "## Evidence from Papers",
    "## Evidence from Internet Sources",
    "## Evidence from Code or Experiments",
    "## Synthesis",
    "## Limitations",
    "## Sources",
)


def _count_sentences(text: str) -> int:
    # Strip code fences and inline code, then count terminating punctuation.
    cleaned: str = re.sub(r"`[^`]+`", "", text)
    cleaned = re.sub(r"```.*?```", "", cleaned, flags=re.DOTALL)
    sentences: list[str] = [s for s in re.split(r"[.!?]+\s+", cleaned.strip()) if s.strip() != ""]
    return len(sentences)


def _check_one(slug: str) -> list[str]:
    errors: list[str] = []
    folder: Path = ANSWER_BASE / slug
    details_path: Path = folder / "details.json"
    short_path: Path = folder / "short_answer.md"
    full_path: Path = folder / "full_answer.md"

    if not details_path.exists():
        errors.append(f"{slug}: details.json missing")
        return errors

    try:
        details: dict[str, object] = json.loads(details_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{slug}: details.json invalid JSON: {exc}")
        return errors

    for field in REQUIRED_DETAILS_FIELDS:
        if field not in details:
            errors.append(f"{slug}: details.json missing required field '{field}'")

    if details.get("answer_id") != slug:
        errors.append(f"{slug}: answer_id={details.get('answer_id')!r} does not match folder slug")

    confidence: object = details.get("confidence")
    if confidence not in {"high", "medium", "low"}:
        errors.append(f"{slug}: confidence={confidence!r} invalid")

    has_evidence: bool = any(
        len(details.get(k, [])) > 0  # type: ignore[arg-type]
        for k in ("source_paper_ids", "source_urls", "source_task_ids")
    )
    if not has_evidence:
        errors.append(f"{slug}: no evidence references in details.json (AA-E014)")

    if not short_path.exists():
        errors.append(f"{slug}: short_answer.md missing")
    else:
        body: str = short_path.read_text(encoding="utf-8")
        for sec in REQUIRED_SHORT_SECTIONS:
            if sec not in body:
                errors.append(f"{slug}: short_answer.md missing section {sec!r} (AA-E011)")
        # 2-5 sentence check on the ## Answer block.
        m = re.search(r"## Answer\n(.*?)(?:\n## |\Z)", body, flags=re.DOTALL)
        if m is not None:
            n_sentences: int = _count_sentences(m.group(1))
            if not (2 <= n_sentences <= 5):
                errors.append(
                    f"{slug}: ## Answer has {n_sentences} sentences (must be 2-5, AA-E013)"
                )

    if not full_path.exists():
        errors.append(f"{slug}: full_answer.md missing")
    else:
        body = full_path.read_text(encoding="utf-8")
        for sec in REQUIRED_FULL_SECTIONS:
            if sec not in body:
                errors.append(f"{slug}: full_answer.md missing section {sec!r} (AA-E012)")

    return errors


def main() -> None:
    if not ANSWER_BASE.exists():
        print(f"ERROR: answer folder {ANSWER_BASE} not found")
        raise SystemExit(2)
    slugs: list[str] = sorted(p.name for p in ANSWER_BASE.iterdir() if p.is_dir())
    print(f"Checking {len(slugs)} answer asset slugs:")
    for slug in slugs:
        print(f"  - {slug}")
    all_errors: list[str] = []
    for slug in slugs:
        errs: list[str] = _check_one(slug=slug)
        if not errs:
            print(f"\n{slug}: OK")
        else:
            print(f"\n{slug}: {len(errs)} errors")
            all_errors.extend(errs)
            for e in errs:
                print(f"  - {e}")
    if all_errors:
        print(f"\nTotal errors: {len(all_errors)}")
        raise SystemExit(1)
    print("\nAll answer assets pass local verification.")


if __name__ == "__main__":
    main()
