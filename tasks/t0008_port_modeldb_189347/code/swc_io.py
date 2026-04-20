"""Stdlib SWC reader + writer for the t0009 diameter-calibration pipeline.

Adapted from ``tasks/t0005_download_dsgc_morphology/code/validate_swc.py`` per
CLAUDE.md rule 3 (no cross-task imports — copy and adapt). The parser, type
codes, and summary utilities are preserved verbatim (minor rename to the
project-standard ``ROOT_PARENT_ID`` constant shared with ``constants``) and
extended with a writer (``write_swc_file``) and a children index builder
(``build_children_index``).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# SWC compartment type codes defined by the CNG standard.
SWC_TYPE_UNDEFINED: int = 0
SWC_TYPE_SOMA: int = 1
SWC_TYPE_AXON: int = 2
SWC_TYPE_BASAL_DENDRITE: int = 3
SWC_TYPE_APICAL_DENDRITE: int = 4

# Minimum number of dendritic compartments required for a meaningful DSGC
# reconstruction. Under this count the morphology is unlikely to represent a
# full dendritic arbor.
MIN_DENDRITE_COMPARTMENTS: int = 100

# Marker value used for the root compartment's parent id.
ROOT_PARENT_ID: int = -1


@dataclass(frozen=True, slots=True)
class SwcCompartment:
    compartment_id: int
    type_code: int
    x: float
    y: float
    z: float
    radius: float
    parent_id: int


@dataclass(frozen=True, slots=True)
class SwcSummary:
    total_compartments: int
    soma_compartments: int
    dendrite_compartments: int
    axon_compartments: int
    other_compartments: int
    branch_points: int
    leaf_points: int
    total_dendritic_length_um: float


def parse_swc_file(*, swc_path: Path) -> list[SwcCompartment]:
    assert swc_path.exists(), f"SWC file exists: {swc_path}"
    compartments: list[SwcCompartment] = []
    with swc_path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if len(line) == 0:
                continue
            if line.startswith("#"):
                continue
            fields = line.split()
            if len(fields) < 7:
                raise ValueError(
                    f"Malformed SWC row (expected 7 fields, got {len(fields)}): {line}"
                )
            compartment = SwcCompartment(
                compartment_id=int(fields[0]),
                type_code=int(fields[1]),
                x=float(fields[2]),
                y=float(fields[3]),
                z=float(fields[4]),
                radius=float(fields[5]),
                parent_id=int(fields[6]),
            )
            compartments.append(compartment)
    assert len(compartments) > 0, "SWC file contains at least one compartment"
    return compartments


def validate_structure(*, compartments: list[SwcCompartment]) -> None:
    ids: set[int] = {c.compartment_id for c in compartments}
    assert len(ids) == len(compartments), "all compartment ids are unique"
    roots = [c for c in compartments if c.parent_id == ROOT_PARENT_ID]
    if len(roots) != 1:
        raise ValueError(f"SWC must have exactly one root (parent == -1); found {len(roots)}")
    for compartment in compartments:
        if compartment.parent_id == ROOT_PARENT_ID:
            continue
        if compartment.parent_id not in ids:
            raise ValueError(
                f"Compartment {compartment.compartment_id} references missing "
                f"parent {compartment.parent_id}"
            )
    negative_radii = [c for c in compartments if c.radius < 0.0]
    if len(negative_radii) > 0:
        first = negative_radii[0]
        raise ValueError(
            f"{len(negative_radii)} compartment(s) have negative radius; "
            f"first is id={first.compartment_id} r={first.radius}"
        )
    soma_count = sum(1 for c in compartments if c.type_code == SWC_TYPE_SOMA)
    if soma_count == 0:
        raise ValueError("SWC must contain at least one soma compartment (type 1)")
    dendrite_count = sum(
        1
        for c in compartments
        if c.type_code in (SWC_TYPE_BASAL_DENDRITE, SWC_TYPE_APICAL_DENDRITE)
    )
    if dendrite_count < MIN_DENDRITE_COMPARTMENTS:
        raise ValueError(
            f"SWC has only {dendrite_count} dendritic compartments; "
            f"need at least {MIN_DENDRITE_COMPARTMENTS}"
        )


def summarize(*, compartments: list[SwcCompartment]) -> SwcSummary:
    by_id: dict[int, SwcCompartment] = {c.compartment_id: c for c in compartments}
    child_counts: dict[int, int] = {c.compartment_id: 0 for c in compartments}
    for compartment in compartments:
        if compartment.parent_id == ROOT_PARENT_ID:
            continue
        child_counts[compartment.parent_id] += 1
    branch_points: int = sum(1 for count in child_counts.values() if count >= 2)
    leaf_points: int = sum(1 for count in child_counts.values() if count == 0)
    soma: int = 0
    dendrite: int = 0
    axon: int = 0
    other: int = 0
    for compartment in compartments:
        if compartment.type_code == SWC_TYPE_SOMA:
            soma += 1
        elif compartment.type_code in (
            SWC_TYPE_BASAL_DENDRITE,
            SWC_TYPE_APICAL_DENDRITE,
        ):
            dendrite += 1
        elif compartment.type_code == SWC_TYPE_AXON:
            axon += 1
        else:
            other += 1
    total_length: float = 0.0
    for compartment in compartments:
        if compartment.parent_id == ROOT_PARENT_ID:
            continue
        if compartment.type_code not in (
            SWC_TYPE_BASAL_DENDRITE,
            SWC_TYPE_APICAL_DENDRITE,
        ):
            continue
        parent = by_id[compartment.parent_id]
        dx: float = compartment.x - parent.x
        dy: float = compartment.y - parent.y
        dz: float = compartment.z - parent.z
        total_length += (dx * dx + dy * dy + dz * dz) ** 0.5
    return SwcSummary(
        total_compartments=len(compartments),
        soma_compartments=soma,
        dendrite_compartments=dendrite,
        axon_compartments=axon,
        other_compartments=other,
        branch_points=branch_points,
        leaf_points=leaf_points,
        total_dendritic_length_um=total_length,
    )


def build_children_index(
    *,
    compartments: list[SwcCompartment],
) -> dict[int, list[int]]:
    """Return a mapping ``parent_id -> [child_id, ...]`` for tree walks.

    The root's parent slot (``ROOT_PARENT_ID``) is intentionally included so
    callers can look up root-level children without special-casing the root.
    """

    children: dict[int, list[int]] = {c.compartment_id: [] for c in compartments}
    children[ROOT_PARENT_ID] = []
    for compartment in compartments:
        children[compartment.parent_id].append(compartment.compartment_id)
    return children


def write_swc_file(
    *,
    compartments: list[SwcCompartment],
    output_path: Path,
    header_comments: list[str],
) -> None:
    """Write a CNG-compatible SWC file.

    Each data row is formatted as ``id type x y z radius parent`` with xyz
    and radius printed to six decimal places. Comment lines are prefixed with
    ``# `` and emitted before the data rows. UTF-8 encoding, LF line endings,
    final newline.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [f"# {comment}" for comment in header_comments]
    for compartment in compartments:
        row = (
            f"{compartment.compartment_id} "
            f"{compartment.type_code} "
            f"{compartment.x:.6f} "
            f"{compartment.y:.6f} "
            f"{compartment.z:.6f} "
            f"{compartment.radius:.6f} "
            f"{compartment.parent_id}"
        )
        lines.append(row)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
