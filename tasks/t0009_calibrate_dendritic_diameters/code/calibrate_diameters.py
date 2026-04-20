"""Main calibration pipeline for the t0009 diameter-calibration task.

Reads the CNG-curated DSGC source SWC, computes Strahler orders, assigns
per-compartment radii from the Poleg-Polsky & Diamond 2016 bins harvested by
:mod:`harvest_poleg_polsky`, clamps to the task's radius floors, and writes
a calibrated SWC that preserves the source topology byte-for-byte (ids,
parents, xyz) while replacing every radius.

Usage::

    uv run python -u -m arf.scripts.utils.run_with_logs \
        --task-id t0009_calibrate_dendritic_diameters -- \
        python -m tasks.t0009_calibrate_dendritic_diameters.code.calibrate_diameters
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import fmean

from tasks.t0009_calibrate_dendritic_diameters.code.constants import (
    BIN_MID,
    BIN_PRIMARY,
    BIN_SOMA,
    BIN_TERMINAL,
    SOMA_RADIUS_FLOOR_UM,
    TERMINAL_RADIUS_FLOOR_UM,
    TYPE_DENDRITE,
    TYPE_SOMA,
)
from tasks.t0009_calibrate_dendritic_diameters.code.morphology import (
    MorphologyGraph,
    build_graph,
)
from tasks.t0009_calibrate_dendritic_diameters.code.paths import (
    CALIBRATED_SWC_PATH,
    CALIBRATION_RECORDS_JSON_PATH,
    POLEG_POLSKY_BINS_JSON_PATH,
    SOURCE_SWC_PATH,
)
from tasks.t0009_calibrate_dendritic_diameters.code.swc_io import (
    SwcCompartment,
    parse_swc_file,
    write_swc_file,
)

SOMA_ENDPOINT_ARTEFACT_UM: float = 1.0


@dataclass(frozen=True, slots=True)
class CalibrationRecord:
    compartment_id: int
    type_code: int
    strahler_order: int
    bin_label: str
    assigned_radius_um: float
    clamped: bool


@dataclass(frozen=True, slots=True)
class PolegPolskyBins:
    primary_radius_um: float
    mid_radius_um: float
    terminal_radius_um: float
    soma_raw_diameters_um: list[float]
    source_url: str
    source_sha256: str


@dataclass(frozen=True, slots=True)
class CalibrationSummary:
    n_total: int
    n_soma: int
    n_dendrite: int
    n_clamped_dendrites: int
    soma_radius_um: float
    primary_radius_um: float
    mid_radius_um: float
    terminal_radius_um: float
    max_strahler_order: int
    n_distinct_radii: int


def _load_bins(*, bins_path: Path) -> PolegPolskyBins:
    raw = json.loads(bins_path.read_text(encoding="utf-8"))
    return PolegPolskyBins(
        primary_radius_um=float(raw["primary_radius_um"]),
        mid_radius_um=float(raw["mid_radius_um"]),
        terminal_radius_um=float(raw["terminal_radius_um"]),
        soma_raw_diameters_um=[float(x) for x in raw["soma_raw_diameters_um"]],
        source_url=str(raw["source_url"]),
        source_sha256=str(raw["source_sha256"]),
    )


def _compute_soma_radius_um(*, bins: PolegPolskyBins) -> float:
    """Return the soma radius assigned to all soma rows.

    Reject the 0.878906 µm reconstruction-endpoint artefacts by requiring
    ``diameter > SOMA_ENDPOINT_ARTEFACT_UM`` (the 0.88 µm values in
    Poleg-Polsky's pt3dadd are contour endpoints that come in at the same
    artefact value; the five central values span 6-10 µm diameter).
    """

    central_diameters: list[float] = [
        d for d in bins.soma_raw_diameters_um if d > SOMA_ENDPOINT_ARTEFACT_UM
    ]
    if len(central_diameters) == 0:
        return SOMA_RADIUS_FLOOR_UM
    mean_diameter = fmean(central_diameters)
    raw_radius = mean_diameter / 2.0
    if raw_radius < SOMA_RADIUS_FLOOR_UM:
        return SOMA_RADIUS_FLOOR_UM
    return raw_radius


def _assign_dendritic_radius_um(
    *,
    strahler_order: int,
    max_order: int,
    bins: PolegPolskyBins,
) -> tuple[str, float]:
    if strahler_order == 1:
        return BIN_TERMINAL, bins.terminal_radius_um
    if strahler_order == max_order:
        return BIN_PRIMARY, bins.primary_radius_um
    return BIN_MID, bins.mid_radius_um


def calibrate(
    *,
    raw_compartments: list[SwcCompartment],
    bins: PolegPolskyBins,
) -> tuple[list[SwcCompartment], list[CalibrationRecord], CalibrationSummary]:
    graph: MorphologyGraph = build_graph(compartments=raw_compartments)
    soma_radius = _compute_soma_radius_um(bins=bins)
    calibrated: list[SwcCompartment] = []
    records: list[CalibrationRecord] = []
    n_clamped = 0
    for compartment in raw_compartments:
        if compartment.type_code == TYPE_SOMA:
            assigned_radius = soma_radius
            bin_label = BIN_SOMA
            clamped = soma_radius == SOMA_RADIUS_FLOOR_UM
            strahler = graph.strahler_by_id[compartment.compartment_id]
        elif compartment.type_code == TYPE_DENDRITE:
            strahler = graph.strahler_by_id[compartment.compartment_id]
            bin_label, raw_radius = _assign_dendritic_radius_um(
                strahler_order=strahler,
                max_order=graph.max_strahler_order,
                bins=bins,
            )
            if raw_radius < TERMINAL_RADIUS_FLOOR_UM:
                assigned_radius = TERMINAL_RADIUS_FLOOR_UM
                clamped = True
                n_clamped += 1
            else:
                assigned_radius = raw_radius
                clamped = False
        else:
            # Preserve radius for any non-soma, non-dendrite rows (should not
            # occur for the t0005 morphology, but fail safe).
            assigned_radius = compartment.radius
            bin_label = "other"
            clamped = False
            strahler = graph.strahler_by_id.get(compartment.compartment_id, 0)
        calibrated.append(
            SwcCompartment(
                compartment_id=compartment.compartment_id,
                type_code=compartment.type_code,
                x=compartment.x,
                y=compartment.y,
                z=compartment.z,
                radius=assigned_radius,
                parent_id=compartment.parent_id,
            )
        )
        records.append(
            CalibrationRecord(
                compartment_id=compartment.compartment_id,
                type_code=compartment.type_code,
                strahler_order=strahler,
                bin_label=bin_label,
                assigned_radius_um=assigned_radius,
                clamped=clamped,
            )
        )
    distinct_radii = {round(c.radius, 6) for c in calibrated}
    summary = CalibrationSummary(
        n_total=len(calibrated),
        n_soma=sum(1 for c in calibrated if c.type_code == TYPE_SOMA),
        n_dendrite=sum(1 for c in calibrated if c.type_code == TYPE_DENDRITE),
        n_clamped_dendrites=n_clamped,
        soma_radius_um=soma_radius,
        primary_radius_um=bins.primary_radius_um,
        mid_radius_um=bins.mid_radius_um,
        terminal_radius_um=max(bins.terminal_radius_um, TERMINAL_RADIUS_FLOOR_UM),
        max_strahler_order=graph.max_strahler_order,
        n_distinct_radii=len(distinct_radii),
    )
    return calibrated, records, summary


def _save_records(
    *,
    records: list[CalibrationRecord],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(r) for r in records]
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    raw_compartments = parse_swc_file(swc_path=SOURCE_SWC_PATH)
    print(f"Loaded {len(raw_compartments)} compartments from {SOURCE_SWC_PATH}")
    bins = _load_bins(bins_path=POLEG_POLSKY_BINS_JSON_PATH)
    print(
        f"Bins: primary={bins.primary_radius_um:.4f} um, "
        f"mid={bins.mid_radius_um:.4f} um, "
        f"terminal={bins.terminal_radius_um:.4f} um"
    )
    calibrated, records, summary = calibrate(
        raw_compartments=raw_compartments,
        bins=bins,
    )
    print(
        f"Calibrated: soma_radius={summary.soma_radius_um:.4f} um, "
        f"max_strahler_order={summary.max_strahler_order}, "
        f"n_clamped_dendrites={summary.n_clamped_dendrites}, "
        f"n_distinct_radii={summary.n_distinct_radii}"
    )
    header_comments = [
        "Diameter-calibrated SWC for dsgc-baseline-morphology-calibrated.",
        f"Source: {SOURCE_SWC_PATH.name} (t0005_download_dsgc_morphology).",
        "Diameter source: Poleg-Polsky & Diamond 2016 (doi 10.1016/j.neuron.2016.02.013).",
        f"Poleg-Polsky hoc sha256: {bins.source_sha256}.",
        "Calibration: per-Strahler-order three-bin partition "
        "(terminal=order 1, primary=max order, mid=intermediate).",
        f"Terminal radius floor: {TERMINAL_RADIUS_FLOOR_UM} um.",
        f"Soma radius floor: {SOMA_RADIUS_FLOOR_UM} um.",
        "Written by tasks.t0009_calibrate_dendritic_diameters.code.calibrate_diameters.",
    ]
    write_swc_file(
        compartments=calibrated,
        output_path=CALIBRATED_SWC_PATH,
        header_comments=header_comments,
    )
    print(f"Wrote {len(calibrated)} compartments to {CALIBRATED_SWC_PATH}")
    _save_records(records=records, output_path=CALIBRATION_RECORDS_JSON_PATH)
    print(f"Wrote {len(records)} calibration records to {CALIBRATION_RECORDS_JSON_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
