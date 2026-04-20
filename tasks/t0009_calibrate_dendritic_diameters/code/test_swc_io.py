"""Topology-equality and calibration-floor tests for t0009.

Run::

    uv run pytest tasks/t0009_calibrate_dendritic_diameters/code/ -v
"""

from __future__ import annotations

from tasks.t0009_calibrate_dendritic_diameters.code.constants import (
    EXPECTED_BRANCH_POINTS,
    EXPECTED_COMPARTMENTS,
    EXPECTED_DENDRITIC_LENGTH_UM,
    EXPECTED_LEAVES,
    SOMA_RADIUS_FLOOR_UM,
    TERMINAL_RADIUS_FLOOR_UM,
    TYPE_DENDRITE,
    TYPE_SOMA,
)
from tasks.t0009_calibrate_dendritic_diameters.code.paths import (
    CALIBRATED_SWC_PATH,
    SOURCE_SWC_PATH,
)
from tasks.t0009_calibrate_dendritic_diameters.code.swc_io import (
    parse_swc_file,
    summarize,
)


def test_calibrated_compartment_count_matches() -> None:
    source = parse_swc_file(swc_path=SOURCE_SWC_PATH)
    calibrated = parse_swc_file(swc_path=CALIBRATED_SWC_PATH)
    assert len(source) == EXPECTED_COMPARTMENTS, (
        f"source has {len(source)} rows; expected {EXPECTED_COMPARTMENTS}"
    )
    assert len(calibrated) == len(source), (
        f"calibrated has {len(calibrated)} rows; expected {len(source)}"
    )


def test_calibrated_topology_unchanged() -> None:
    source = parse_swc_file(swc_path=SOURCE_SWC_PATH)
    calibrated = parse_swc_file(swc_path=CALIBRATED_SWC_PATH)
    for source_row, calibrated_row in zip(source, calibrated, strict=True):
        assert source_row.compartment_id == calibrated_row.compartment_id, (
            "compartment ids must be identical per row"
        )
        assert source_row.type_code == calibrated_row.type_code, (
            "type codes must be identical per row"
        )
        assert source_row.parent_id == calibrated_row.parent_id, (
            "parent ids must be identical per row"
        )


def test_calibrated_coordinates_unchanged() -> None:
    source = parse_swc_file(swc_path=SOURCE_SWC_PATH)
    calibrated = parse_swc_file(swc_path=CALIBRATED_SWC_PATH)
    for source_row, calibrated_row in zip(source, calibrated, strict=True):
        assert abs(source_row.x - calibrated_row.x) < 1e-9, "x coordinates match"
        assert abs(source_row.y - calibrated_row.y) < 1e-9, "y coordinates match"
        assert abs(source_row.z - calibrated_row.z) < 1e-9, "z coordinates match"


def test_calibrated_no_radius_below_floor() -> None:
    calibrated = parse_swc_file(swc_path=CALIBRATED_SWC_PATH)
    for row in calibrated:
        if row.type_code == TYPE_DENDRITE:
            assert row.radius >= TERMINAL_RADIUS_FLOOR_UM - 1e-9, (
                f"dendrite {row.compartment_id} radius {row.radius} below "
                f"{TERMINAL_RADIUS_FLOOR_UM} um floor"
            )
        elif row.type_code == TYPE_SOMA:
            assert row.radius >= SOMA_RADIUS_FLOOR_UM - 1e-9, (
                f"soma row {row.compartment_id} radius {row.radius} below "
                f"{SOMA_RADIUS_FLOOR_UM} um floor"
            )


def test_calibrated_has_at_least_three_distinct_radii() -> None:
    calibrated = parse_swc_file(swc_path=CALIBRATED_SWC_PATH)
    radii = {round(row.radius, 6) for row in calibrated}
    assert len(radii) >= 3, (
        f"calibrated SWC must have at least three distinct radii; got {len(radii)}: {radii}"
    )


def test_calibrated_summary_matches_source() -> None:
    source = parse_swc_file(swc_path=SOURCE_SWC_PATH)
    calibrated = parse_swc_file(swc_path=CALIBRATED_SWC_PATH)
    source_summary = summarize(compartments=source)
    calibrated_summary = summarize(compartments=calibrated)
    assert source_summary.branch_points == EXPECTED_BRANCH_POINTS, (
        f"source branch points {source_summary.branch_points} != {EXPECTED_BRANCH_POINTS}"
    )
    assert calibrated_summary.branch_points == EXPECTED_BRANCH_POINTS, (
        f"calibrated branch points {calibrated_summary.branch_points} != {EXPECTED_BRANCH_POINTS}"
    )
    assert source_summary.leaf_points == EXPECTED_LEAVES, (
        f"source leaves {source_summary.leaf_points} != {EXPECTED_LEAVES}"
    )
    assert calibrated_summary.leaf_points == EXPECTED_LEAVES, (
        f"calibrated leaves {calibrated_summary.leaf_points} != {EXPECTED_LEAVES}"
    )
    assert abs(source_summary.total_dendritic_length_um - EXPECTED_DENDRITIC_LENGTH_UM) < 1e-2, (
        f"source length {source_summary.total_dendritic_length_um:.4f} um "
        f"!= expected {EXPECTED_DENDRITIC_LENGTH_UM} um"
    )
    assert (
        abs(calibrated_summary.total_dendritic_length_um - EXPECTED_DENDRITIC_LENGTH_UM) < 1e-2
    ), (
        f"calibrated length {calibrated_summary.total_dendritic_length_um:.4f} um "
        f"!= expected {EXPECTED_DENDRITIC_LENGTH_UM} um"
    )
