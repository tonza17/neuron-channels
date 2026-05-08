"""Programmatic confirmation that the corrections overlay routes library lookups
to the t0092 ``procedural_dsgc_morphology_generator_fix`` library.

In this branch ``aggregate_libraries.py`` is **not present**. Library record
lookups instead go through ``arf.scripts.common.artifacts.load_target_record``
combined with ``arf.scripts.common.corrections.resolve_target``, which honour
the `replace` action in the corrections overlay.

This script:

1. Builds the original target key
   ``(task=t0090, kind=library, id=procedural_dsgc_morphology_generator)``.
2. Discovers all corrections in the project, builds the index, and resolves the
   effective target key.
3. Asserts the effective key now points at
   ``(task=t0092, kind=library, id=procedural_dsgc_morphology_generator_fix)``.
4. Writes ``data/library_supersession_check.json`` with the evidence.

If ``arf.scripts.common.artifacts`` cannot be loaded for any reason, the script
falls back to reading the correction file directly + checking that t0092's
library ``details.json`` exists, and records the fallback path in ``evidence``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from tasks.t0093_resweep_and_t0090_correction.code.constants import (
    CORRECTING_TASK,
    CORRECTION_ID,
    REPLACEMENT_LIBRARY_ID,
    REPLACEMENT_TASK,
    TARGET_KIND_LIBRARY,
    TARGET_LIBRARY_ID,
    TARGET_TASK,
)
from tasks.t0093_resweep_and_t0090_correction.code.paths import (
    CORRECTION_LIBRARY_JSON,
    DATA_LIBRARY_SUPERSESSION_JSON,
    REPO_ROOT,
    ensure_directories,
)


def _try_resolve_via_artifacts() -> dict[str, Any] | None:
    """Attempt to resolve the effective target via artifacts + corrections modules.

    Returns the result dict on success, or None on failure (caller should fall
    back to the file-existence check path).
    """
    try:
        from arf.scripts.common.artifacts import TargetKey
        from arf.scripts.common.corrections import (
            build_correction_index,
            discover_corrections,
            resolve_target,
        )
    except Exception as exc:  # pragma: no cover - guard for harness drift
        print(f"library_supersession_check: failed to import artifacts/corrections: {exc!r}")
        return None

    original_key = TargetKey(
        task_id=TARGET_TASK,
        target_kind=TARGET_KIND_LIBRARY,
        target_id=TARGET_LIBRARY_ID,
    )
    correction_specs = discover_corrections()
    correction_index = build_correction_index(correction_specs=correction_specs)
    resolution = resolve_target(
        original_key=original_key,
        correction_index=correction_index,
    )

    if resolution.deleted:
        return {
            "aggregator_present": False,
            "evidence": (
                "library aggregator not present in branch — verified via "
                "arf.scripts.common.artifacts directly"
            ),
            "effective_task_id": None,
            "effective_library_id": None,
            "deleted": True,
            "correction_id": CORRECTION_ID,
            "method": "arf.scripts.common.corrections.resolve_target",
        }

    effective_task: str = resolution.effective_key.task_id
    effective_id: str = resolution.effective_key.target_id
    return {
        "aggregator_present": False,
        "evidence": (
            "library aggregator not present in branch — verified via "
            "arf.scripts.common.artifacts directly"
        ),
        "effective_task_id": effective_task,
        "effective_library_id": effective_id,
        "deleted": False,
        "correction_id": CORRECTION_ID,
        "method": "arf.scripts.common.corrections.resolve_target",
    }


def _fallback_check() -> dict[str, Any]:
    """Fallback: confirm the correction file exists and t0092's details.json exists."""
    correction_exists: bool = CORRECTION_LIBRARY_JSON.exists()
    replacement_details: Path = (
        REPO_ROOT
        / "tasks"
        / REPLACEMENT_TASK
        / "assets"
        / "library"
        / REPLACEMENT_LIBRARY_ID
        / "details.json"
    )
    replacement_exists: bool = replacement_details.exists()
    correction_payload: dict[str, Any] = {}
    if correction_exists:
        correction_payload = json.loads(CORRECTION_LIBRARY_JSON.read_text())

    effective_task = correction_payload.get("changes", {}).get("replacement_task")
    effective_id = correction_payload.get("changes", {}).get("replacement_id")

    return {
        "aggregator_present": False,
        "evidence": (
            "fallback: read correction file directly and verified t0092 library details.json exists"
        ),
        "effective_task_id": effective_task if replacement_exists else None,
        "effective_library_id": effective_id if replacement_exists else None,
        "correction_id": CORRECTION_ID,
        "method": "fallback_file_existence",
        "correction_file_exists": correction_exists,
        "replacement_details_exists": replacement_exists,
    }


def main() -> int:
    ensure_directories()
    payload = _try_resolve_via_artifacts()
    if payload is None:
        payload = _fallback_check()

    payload["correcting_task"] = CORRECTING_TASK
    payload["original_task_id"] = TARGET_TASK
    payload["original_library_id"] = TARGET_LIBRARY_ID

    DATA_LIBRARY_SUPERSESSION_JSON.write_text(json.dumps(payload, indent=2))

    if (
        payload.get("effective_task_id") == REPLACEMENT_TASK
        and payload.get("effective_library_id") == REPLACEMENT_LIBRARY_ID
    ):
        print("supersession verified")
        print(f"wrote {DATA_LIBRARY_SUPERSESSION_JSON}")
        return 0

    print(
        "supersession NOT verified: effective_task_id="
        f"{payload.get('effective_task_id')!r}, "
        f"effective_library_id={payload.get('effective_library_id')!r}",
    )
    print(f"wrote {DATA_LIBRARY_SUPERSESSION_JSON}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
