"""Fetch Poleg-Polsky & Diamond 2016 ``RGCmodel.hoc`` and harvest per-section diameters.

Downloads the MIT-licensed Hanson-lab mirror of the ModelDB 189347 ``.hoc``
geometry, writes it to ``data/RGCmodel.hoc`` for hermetic re-runs, then
parses every ``pt3dadd(x, y, z, diam)`` call, classifies each ``dend[i]``
section as primary / mid / terminal using the ``connect`` topology in the
.hoc, filters diameter == 0 interpolation nodes, and writes a JSON bin
summary to ``data/poleg_polsky_bins.json``.

Usage::

    uv run python -u -m arf.scripts.utils.run_with_logs \
        --task-id t0009_calibrate_dendritic_diameters -- \
        python -m tasks.t0009_calibrate_dendritic_diameters.code.harvest_poleg_polsky
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from statistics import fmean

from tasks.t0009_calibrate_dendritic_diameters.code.paths import (
    POLEG_POLSKY_BINS_JSON_PATH,
    POLEG_POLSKY_HOC_PATH,
)

SOURCE_URL: str = (
    "https://raw.githubusercontent.com/"
    "geoffder/Spatial-Offset-DSGC-NEURON-Model/master/RGCmodel.hoc"
)
FETCH_TIMEOUT_SECONDS: float = 30.0

PT3DADD_REGEX: re.Pattern[str] = re.compile(
    r"pt3dadd\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)"
)
SECTION_OPEN_REGEX: re.Pattern[str] = re.compile(
    r"(?:^|[^A-Za-z_])(soma|dend\s*\[\s*(\d+)\s*\])\s*\{"
)
DIRECT_CONNECT_REGEX: re.Pattern[str] = re.compile(
    r"connect\s+dend\s*\[\s*(\d+)\s*\]\s*\(\s*[\d.]+\s*\)\s*,\s*"
    r"(soma|dend)(?:\s*\[\s*(\d+)\s*\])?\s*\(\s*[\d.]+\s*\)"
)
FOR_CONNECT_REGEX: re.Pattern[str] = re.compile(
    r"for\s+i\s*=\s*(\d+)\s*,\s*(\d+)\s+connect\s+dend\s*\[\s*i\s*\]\s*\(\s*[\d.]+\s*\)\s*,\s*"
    r"dend\s*\[\s*(i\s*-\s*\d+|i)\s*\]\s*\(\s*[\d.]+\s*\)"
)

SOMA_SECTION_KEY: str = "soma"


@dataclass(frozen=True, slots=True)
class HarvestResult:
    sha256: str
    n_pt3dadd_total: int
    n_pt3dadd_nonzero: int
    soma_raw_diameters_um: list[float]
    primary_radius_um: float
    mid_radius_um: float
    terminal_radius_um: float
    n_primary_sections: int
    n_mid_sections: int
    n_terminal_sections: int


def _fetch_hoc(*, url: str, timeout: float) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "glite-arf-t0009"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            return str(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        print(f"ERROR: failed to fetch {url}: {exc}", file=sys.stderr)
        raise


def _save_hoc(*, hoc_text: str, path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(hoc_text, encoding="utf-8")
    digest = hashlib.sha256(hoc_text.encode("utf-8")).hexdigest()
    return digest


def _parse_connect_edges(
    *,
    hoc_text: str,
) -> list[tuple[int, str, int | None]]:
    """Return ``(child_dend_index, parent_kind, parent_dend_index_or_None)``.

    Handles both direct ``connect dend[i](0), dend[j](1)`` lines and the
    ``for i = a, b connect dend[i](0), dend[i-k](1)`` loops used throughout
    ``RGCmodel.hoc``; for the loops the edges are expanded to one per ``i``.
    """

    edges: list[tuple[int, str, int | None]] = []
    for match in DIRECT_CONNECT_REGEX.finditer(hoc_text):
        child_idx = int(match.group(1))
        parent_kind = match.group(2)
        parent_idx_str = match.group(3)
        parent_idx = int(parent_idx_str) if parent_idx_str is not None else None
        edges.append((child_idx, parent_kind, parent_idx))
    for loop_match in FOR_CONNECT_REGEX.finditer(hoc_text):
        start = int(loop_match.group(1))
        stop_inclusive = int(loop_match.group(2))
        offset_expr = loop_match.group(3).replace(" ", "")
        if offset_expr == "i":
            offset = 0
        elif offset_expr.startswith("i-"):
            offset = int(offset_expr[2:])
        else:
            continue
        for i in range(start, stop_inclusive + 1):
            parent_idx_value = i - offset
            edges.append((i, "dend", parent_idx_value))
    return edges


def _classify_dendrite_sections(
    *,
    hoc_text: str,
    all_dend_indices: set[int],
) -> dict[int, str]:
    """Classify each ``dend[i]`` section as ``primary``, ``mid``, or ``terminal``.

    * ``primary`` = child of ``soma``.
    * ``terminal`` = no other dendrite is attached with it as parent.
    * ``mid`` = has at least one child dendrite but is not attached to soma.
    """

    edges = _parse_connect_edges(hoc_text=hoc_text)
    primary_indices: set[int] = set()
    parent_of: dict[int, tuple[str, int | None]] = {}
    has_child: set[int] = set()
    for child_idx, parent_kind, parent_idx in edges:
        parent_of[child_idx] = (parent_kind, parent_idx)
        if parent_kind == "soma":
            primary_indices.add(child_idx)
        elif parent_kind == "dend" and parent_idx is not None:
            has_child.add(parent_idx)
    classification: dict[int, str] = {}
    for idx in all_dend_indices:
        if idx in primary_indices:
            classification[idx] = "primary"
        elif idx not in has_child:
            classification[idx] = "terminal"
        else:
            classification[idx] = "mid"
    return classification


def _parse_pt3dadd_by_section(
    *,
    hoc_text: str,
) -> dict[str, list[float]]:
    """Return ``{section_key: [diam, diam, ...]}`` with diam > 0 only.

    ``section_key`` is ``"soma"`` or ``"dend_<i>"``. The current-section
    cursor is updated whenever a line opens a new section block via a
    ``soma {`` or ``dend[i] {`` pattern; ``pt3dadd`` calls between two
    cursor updates are attributed to the most recent cursor.
    """

    by_section: dict[str, list[float]] = {}
    current_key: str | None = None
    for raw_line in hoc_text.splitlines():
        line = raw_line.strip()
        if len(line) == 0 or line.startswith("//"):
            continue
        header_match = SECTION_OPEN_REGEX.search(line)
        if header_match is not None:
            section_token = header_match.group(1)
            if section_token.startswith("soma"):
                current_key = SOMA_SECTION_KEY
            else:
                idx_str = header_match.group(2)
                current_key = f"dend_{int(idx_str)}"
        for pt_match in PT3DADD_REGEX.finditer(line):
            diameter = float(pt_match.group(4))
            key = current_key if current_key is not None else "unknown"
            by_section.setdefault(key, []).append(diameter)
    return by_section


def _count_pt3dadd(*, by_section: dict[str, list[float]]) -> tuple[int, int]:
    total = 0
    nonzero = 0
    for diameters in by_section.values():
        for diameter in diameters:
            total += 1
            if diameter > 0.0:
                nonzero += 1
    return total, nonzero


def _compute_role_mean_radius_um(
    *,
    by_section: dict[str, list[float]],
    classification: dict[int, str],
    role: str,
) -> float:
    collected: list[float] = []
    for dend_idx, section_role in classification.items():
        if section_role != role:
            continue
        key = f"dend_{dend_idx}"
        for diameter in by_section.get(key, []):
            if diameter > 0.0:
                collected.append(diameter / 2.0)
    if len(collected) == 0:
        return 0.0
    return fmean(collected)


def harvest(*, url: str, hoc_path: Path, bins_path: Path) -> HarvestResult:
    if hoc_path.exists():
        hoc_text = hoc_path.read_text(encoding="utf-8")
        sha256 = hashlib.sha256(hoc_text.encode("utf-8")).hexdigest()
    else:
        hoc_text = _fetch_hoc(url=url, timeout=FETCH_TIMEOUT_SECONDS)
        sha256 = _save_hoc(hoc_text=hoc_text, path=hoc_path)
    by_section = _parse_pt3dadd_by_section(hoc_text=hoc_text)
    n_total, n_nonzero = _count_pt3dadd(by_section=by_section)
    all_dend_indices: set[int] = set()
    for key in by_section:
        if key.startswith("dend_"):
            all_dend_indices.add(int(key.split("_", 1)[1]))
    classification = _classify_dendrite_sections(
        hoc_text=hoc_text,
        all_dend_indices=all_dend_indices,
    )
    soma_diameters: list[float] = [
        diameter for diameter in by_section.get(SOMA_SECTION_KEY, []) if diameter > 0.0
    ]
    primary_radius = _compute_role_mean_radius_um(
        by_section=by_section,
        classification=classification,
        role="primary",
    )
    mid_radius = _compute_role_mean_radius_um(
        by_section=by_section,
        classification=classification,
        role="mid",
    )
    terminal_radius = _compute_role_mean_radius_um(
        by_section=by_section,
        classification=classification,
        role="terminal",
    )
    result = HarvestResult(
        sha256=sha256,
        n_pt3dadd_total=n_total,
        n_pt3dadd_nonzero=n_nonzero,
        soma_raw_diameters_um=soma_diameters,
        primary_radius_um=primary_radius,
        mid_radius_um=mid_radius,
        terminal_radius_um=terminal_radius,
        n_primary_sections=sum(1 for v in classification.values() if v == "primary"),
        n_mid_sections=sum(1 for v in classification.values() if v == "mid"),
        n_terminal_sections=sum(1 for v in classification.values() if v == "terminal"),
    )
    bins_path.parent.mkdir(parents=True, exist_ok=True)
    bins_path.write_text(
        json.dumps(
            {
                "source_url": url,
                "source_sha256": result.sha256,
                "n_pt3dadd_total": result.n_pt3dadd_total,
                "n_pt3dadd_nonzero": result.n_pt3dadd_nonzero,
                "soma_raw_diameters_um": result.soma_raw_diameters_um,
                "primary_radius_um": result.primary_radius_um,
                "mid_radius_um": result.mid_radius_um,
                "terminal_radius_um": result.terminal_radius_um,
                "n_primary_sections": result.n_primary_sections,
                "n_mid_sections": result.n_mid_sections,
                "n_terminal_sections": result.n_terminal_sections,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return result


def main() -> int:
    result = harvest(
        url=SOURCE_URL,
        hoc_path=POLEG_POLSKY_HOC_PATH,
        bins_path=POLEG_POLSKY_BINS_JSON_PATH,
    )
    print(f"Fetched {SOURCE_URL} sha256={result.sha256}")
    print(f"pt3dadd total={result.n_pt3dadd_total} nonzero={result.n_pt3dadd_nonzero}")
    print(f"soma raw diameters (um): {result.soma_raw_diameters_um}")
    print(
        f"primary radius={result.primary_radius_um:.4f} um (n_sections={result.n_primary_sections})"
    )
    print(f"mid     radius={result.mid_radius_um:.4f} um (n_sections={result.n_mid_sections})")
    print(
        f"terminal radius={result.terminal_radius_um:.4f} um "
        f"(n_sections={result.n_terminal_sections})"
    )
    if result.terminal_radius_um > 0:
        ratio = result.primary_radius_um / result.terminal_radius_um
        print(f"primary / terminal diameter ratio = {ratio:.2f}")
    print(f"bins JSON written to: {POLEG_POLSKY_BINS_JSON_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
