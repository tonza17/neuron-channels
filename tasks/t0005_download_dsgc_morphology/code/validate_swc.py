"""Validate a CNG-curated SWC morphology file for DSGC modeling.

Primary check uses only the Python stdlib: parse the SWC line by line, build a
compartment tree, and confirm structural invariants required by compartmental
simulators (exactly one root, fully connected tree, non-negative radii, at
least one soma compartment, enough dendritic compartments to be usable).

Secondary check attempts to load the same SWC via ``neurom.load_morphology``
when ``neurom`` is importable. A missing ``neurom`` install is logged but does
not fail the validator, matching the plan's "nice-to-have" designation.

Prints ``VALID`` to stdout on success; exits non-zero with a human-readable
error on any structural violation.
"""

from __future__ import annotations

import argparse
import importlib
import sys
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


def _validate_structure(*, compartments: list[SwcCompartment]) -> None:
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


def _summarize(*, compartments: list[SwcCompartment]) -> SwcSummary:
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


def _try_neurom_secondary_check(*, swc_path: Path) -> str:
    try:
        neurom_module = importlib.import_module("neurom")
    except ImportError:
        return "neurom not installed; secondary check skipped"
    try:
        morphology = neurom_module.load_morphology(str(swc_path))
    except Exception as exc:  # noqa: BLE001 - any neurom error should be reported
        return f"neurom secondary check FAILED: {type(exc).__name__}: {exc}"
    section_count = len(list(morphology.sections))
    return f"neurom secondary check OK (sections={section_count})"


def validate(*, swc_path: Path) -> SwcSummary:
    compartments = parse_swc_file(swc_path=swc_path)
    _validate_structure(compartments=compartments)
    return _summarize(compartments=compartments)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a CNG-curated SWC morphology file. Exits 0 and prints "
            "VALID on success; non-zero with an error message on failure."
        )
    )
    parser.add_argument(
        "swc_path",
        type=Path,
        help="Path to the SWC file to validate",
    )
    args = parser.parse_args()
    swc_path: Path = args.swc_path
    if not swc_path.exists():
        print(f"ERROR: SWC file not found: {swc_path}", file=sys.stderr)
        return 2
    try:
        summary = validate(swc_path=swc_path)
    except (ValueError, AssertionError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(f"File: {swc_path}")
    print(f"Total compartments: {summary.total_compartments}")
    print(f"  Soma: {summary.soma_compartments}")
    print(f"  Dendrite: {summary.dendrite_compartments}")
    print(f"  Axon: {summary.axon_compartments}")
    print(f"  Other: {summary.other_compartments}")
    print(f"Branch points: {summary.branch_points}")
    print(f"Leaf points: {summary.leaf_points}")
    print(f"Total dendritic length: {summary.total_dendritic_length_um:.2f} um")
    neurom_status = _try_neurom_secondary_check(swc_path=swc_path)
    print(f"Secondary check: {neurom_status}")
    print("VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())
