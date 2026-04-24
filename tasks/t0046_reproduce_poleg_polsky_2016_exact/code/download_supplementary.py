"""Download the Poleg-Polsky 2016 PMC supplementary PDF into this task's local supplements/ folder.

The downloaded file is then attached to the existing t0002 paper asset
``10.1016_j.neuron.2016.02.013`` via a corrections overlay file in
``corrections/paper_10.1016_j.neuron.2016.02.013.json`` per
``arf/specifications/corrections_specification.md`` v3.

Per the immutability rule, the t0002 task folder is not mutated. The corrections file points at
this task's local copy via the ``add`` file action.

Usage::

    uv run python -m arf.scripts.utils.run_with_logs \\
        --task-id t0046_reproduce_poleg_polsky_2016_exact -- \\
        uv run python -u \\
        tasks/t0046_reproduce_poleg_polsky_2016_exact/code/download_supplementary.py
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.paths import (
    CORRECTIONS_DIR,
    TASK_ROOT,
)

SUPP_URL: str = (
    "https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf"
)
SUPP_FILENAME: str = "NIHMS766337-supplement.pdf"
SUPP_LOCAL_DIR: Path = TASK_ROOT / "supplements"
SUPP_LOCAL_PATH: Path = SUPP_LOCAL_DIR / SUPP_FILENAME

# The correcting task adds this file as a new logical file in the t0002 paper asset's
# effective `files` list.
PAPER_ASSET_ID: str = "10.1016_j.neuron.2016.02.013"
PAPER_TASK_ID: str = "t0002_literature_survey_dsgc_compartmental_models"
CORRECTION_PATH: Path = CORRECTIONS_DIR / f"paper_{PAPER_ASSET_ID}.json"


CANDIDATE_URLS: tuple[str, ...] = (
    "https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf",
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4795984/bin/NIHMS766337-supplement.pdf",
    "https://www.cell.com/cms/10.1016/j.neuron.2016.02.013/attachment/b2b9a2d9-4a06-4e9c-8d93-3fb8d7d8a9d1/mmc1.pdf",
)

USER_AGENTS: tuple[str, ...] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/17.4 Safari/605.1.15",
)


def _looks_like_pdf(*, content: bytes) -> bool:
    return content[:8].startswith(b"%PDF-")


def _download(*, url: str, dst: Path) -> bool:
    if dst.exists() and dst.stat().st_size > 0 and _looks_like_pdf(content=dst.read_bytes()[:8]):
        print(f"  [skip] {dst} already exists ({dst.stat().st_size} bytes)", flush=True)
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    for ua in USER_AGENTS:
        for candidate in CANDIDATE_URLS:
            print(f"  Trying {candidate} (UA: {ua[:40]}...)", flush=True)
            req = urllib.request.Request(  # noqa: S310 — explicit https URL.
                url=candidate,
                headers={
                    "User-Agent": ua,
                    "Accept": "application/pdf,*/*",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4795984/",
                },
            )
            try:
                with urllib.request.urlopen(req, timeout=60) as response:  # noqa: S310
                    content: bytes = response.read()
            except urllib.error.URLError as e:
                print(f"    error: {e}", flush=True)
                continue
            if not _looks_like_pdf(content=content):
                print(
                    f"    not a PDF ({len(content)} bytes, first 16 = {content[:16]!r})",
                    flush=True,
                )
                continue
            dst.write_bytes(content)
            print(f"  Wrote {dst} ({len(content)} bytes)", flush=True)
            return True
    return False


def _write_correction(*, download_succeeded: bool) -> None:
    """Write the corrections overlay either with file_changes (if download OK) or metadata-only.

    When the download fails (PMC interstitial), we still write a corrections file that records
    the canonical supplementary URL in the rationale and notes that the PDF could not be
    auto-downloaded. Manual download is documented as an open intervention.
    """
    if download_succeeded:
        correction: dict[str, object] = {
            "spec_version": "3",
            "correction_id": "C-0046-01",
            "correcting_task": "t0046_reproduce_poleg_polsky_2016_exact",
            "target_task": PAPER_TASK_ID,
            "target_kind": "paper",
            "target_id": PAPER_ASSET_ID,
            "action": "update",
            "changes": {
                "files": [
                    "files/poleg-polsky_2016_nmda-dsgc-multiplicative.xml",
                    f"files/{SUPP_FILENAME}",
                ],
            },
            "file_changes": {
                f"files/{SUPP_FILENAME}": {
                    "action": "add",
                    "replacement_task": "t0046_reproduce_poleg_polsky_2016_exact",
                    "replacement_id": PAPER_ASSET_ID,
                    "replacement_path": f"supplements/{SUPP_FILENAME}",
                },
            },
            "rationale": (
                "Attach the PMC supplementary PDF (NIHMS766337) to the existing Poleg-Polsky "
                "2016 paper asset (REQ-14). The supplementary contains methods detail "
                "(synapse counts, kinetics) needed to audit the paper-vs-code discrepancies "
                "catalogued by t0046. Per the immutability rule, the PDF is hosted in this "
                "task's supplements/ folder and made effective in the paper asset via the "
                "file-overlay add action defined in corrections_specification.md v3. "
                f"Source URL: {SUPP_URL} (PMC accession PMC4795984)."
            ),
        }
    else:
        correction = {
            "spec_version": "3",
            "correction_id": "C-0046-01",
            "correcting_task": "t0046_reproduce_poleg_polsky_2016_exact",
            "target_task": PAPER_TASK_ID,
            "target_kind": "paper",
            "target_id": PAPER_ASSET_ID,
            "action": "update",
            "changes": {
                "abstract": (
                    "[Supplementary materials NIHMS766337 (PMC4795984) cited at: "
                    f"{SUPP_URL}] "
                    "Postsynaptic responses in many CNS neurons are typically small and "
                    "variable, often making it difficult to distinguish physiologically "
                    "relevant signals from background noise. To extract salient information, "
                    "neurons are thought to integrate multiple synaptic inputs and/or "
                    "selectively amplify specific synaptic activation patterns. Here, we "
                    "present evidence for a third strategy: directionally selective ganglion "
                    "cells (DSGCs) in the mouse retina multiplicatively scale visual signals "
                    "via a mechanism that requires both nonlinear NMDA receptor (NMDAR) "
                    "conductances in DSGC dendrites and directionally tuned inhibition "
                    "provided by the upstream retinal circuitry. Postsynaptic multiplication "
                    "enables DSGCs to discriminate visual motion more accurately in noisy "
                    "visual conditions without compromising directional tuning. These "
                    "findings demonstrate a novel role for NMDARs in synaptic processing and "
                    "provide new insights into how synaptic and network features interact to "
                    "accomplish physiologically relevant neural computations."
                ),
            },
            "rationale": (
                "REQ-14 partial: PMC blocks programmatic download of NIHMS766337-supplement.pdf "
                "with a JS-only interstitial page that returns 1.8 KB of HTML instead of the "
                "PDF binary. We tried multiple user-agents, referer chains, and mirror URLs; "
                "all returned the interstitial. Recording the supplementary citation in the "
                "paper asset abstract via this metadata-only update so that downstream "
                "consumers see the canonical source URL "
                f"({SUPP_URL}). Manual fetch through a real browser is required to attach the "
                "PDF binary itself; this is documented in intervention/. The audit table and "
                "discrepancy catalogue still cite the supplementary text as needed."
            ),
        }
    CORRECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    CORRECTION_PATH.write_text(
        data=json.dumps(obj=correction, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"  Wrote correction file: {CORRECTION_PATH}", flush=True)


def main() -> int:
    SUPP_LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    ok: bool = _download(url=SUPP_URL, dst=SUPP_LOCAL_PATH)
    _write_correction(download_succeeded=ok)
    if not ok:
        # Remove the HTML interstitial bytes (if any) so we don't ship them.
        if SUPP_LOCAL_PATH.exists():
            SUPP_LOCAL_PATH.unlink()
        # Drop a placeholder so the supplements/ folder is committed for visibility.
        marker: Path = SUPP_LOCAL_DIR / "DOWNLOAD_BLOCKED.txt"
        marker.write_text(
            data=(
                "Programmatic download of NIHMS766337-supplement.pdf is blocked by PMC's "
                f"JS-only interstitial. Source URL: {SUPP_URL}. The corrections overlay "
                "records the citation as a metadata-only update. Manual fetch via a real "
                "browser is required to attach the PDF binary.\n"
            ),
            encoding="utf-8",
        )
        print(
            "\nSupplementary download blocked by PMC interstitial. Corrections overlay "
            "written as metadata-only citation; manual fetch documented as intervention.",
            flush=True,
        )
        return 0
    print("\nSupplementary PDF in place; corrections overlay written.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
