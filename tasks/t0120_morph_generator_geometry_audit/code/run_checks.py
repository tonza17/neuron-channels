"""Step 7: run the 3 coordinate-consistency checks per cell (REQ-4, REQ-5, REQ-6, REQ-7, REQ-9).

Reads `results/data/section_endpoints_dump.json` and computes per-cell pass/fail booleans:

* **Check 1** (primary stem origin): for every primary dendrite section,
  `python_start_xy ≈ origin_xy` within `CHECK_ABS_TOL`.
* **Check 2** (parent/child match): for every non-primary dendrite section,
  `python_start_xy ≈ parent.python_end_xy` within `CHECK_ABS_TOL`.
* **Check 3** (synapse pt3d frame): for every dendrite section, `midpoint_xy_neuron` lies on
  the line from `python_start_xy` to `python_end_xy` (cross-product zero within tolerance) AND
  the midpoint is in the same coordinate frame as `origin_xy` (i.e. midpoint - origin distance
  is small enough that no `soma_offset`-magnitude shift could have occurred). Degenerate
  sections (`midpoint_error_reason is not None`) count as failures.

Writes `results/data/coordinate_consistency_checks.csv`.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any

import pandas as pd

from tasks.t0120_morph_generator_geometry_audit.code.constants import (
    CELL_ID_COL,
    CHECK1_PRIMARY_START_COL,
    CHECK2_PARENT_CHILD_COL,
    CHECK3_SYNAPSE_FRAME_COL,
    CHECK_ABS_TOL,
    GENERATION_COL,
    INDIVIDUAL_IDX_COL,
    SEED_COL,
    SOURCE_TASK_COL,
    STRATUM_TAG_COL,
)
from tasks.t0120_morph_generator_geometry_audit.code.paths import (
    COORDINATE_CONSISTENCY_CHECKS_CSV,
    SECTION_ENDPOINTS_DUMP_JSON,
)

# Coarse upper bound on midpoint -> origin distance in the post-asymmetry frame for any dendrite
# section. The t0090 generator field elongation runs 1-3 over ~150 um per side, so the maximum
# expected dendrite-tip distance from the soma is ~3 * 150 = 450 um. We add generous slack to
# catch only frame-magnitude shifts (e.g. an unintended `+soma_offset` of up to 150 um on top of
# the dendrite-tip distance). Anything beyond `MAX_MIDPOINT_FROM_ORIGIN_UM` flags a frame error.
MAX_MIDPOINT_FROM_ORIGIN_UM: float = 1000.0

# Lateral-deviation threshold in um for Check 3 sub-check 3a (midpoint on line through start,
# end). This is the *physical* mismatch we care about: a sub-um lateral error is float-arithmetic
# noise, anything above ~1 um would indicate a real geometry frame mismatch. The actual
# audit-relevant question is whether a `soma_offset_pd_um` shift (tens to ~150 um) leaked into
# the dendrite midpoint pt3d -- which would surface as a *huge* lateral deviation, not a tens-of-
# nm one. We set the threshold at 0.1 um (100 nm) which is two orders of magnitude above the
# observed float-arithmetic noise floor (~10 nm on 200 um segments) and three orders below the
# smallest plausible frame-shift signature.
MIDPOINT_LATERAL_TOL_UM: float = 0.1


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Per-cell check outcomes plus max-error diagnostics."""

    check1_primary_start: bool
    check2_parent_child: bool
    check3_synapse_frame: bool
    n_primary_stems: int
    n_non_primary_sections: int
    n_dendrite_sections: int
    max_check1_error_um: float
    max_check2_error_um: float
    max_check3_lateral_error_um: float
    max_check3_origin_distance_um: float
    check3_n_degenerate_sections: int


def _xy_close(*, a: tuple[float, float], b: tuple[float, float]) -> bool:
    return math.isclose(a[0], b[0], abs_tol=CHECK_ABS_TOL) and math.isclose(
        a[1], b[1], abs_tol=CHECK_ABS_TOL
    )


def _xy_distance(*, a: tuple[float, float], b: tuple[float, float]) -> float:
    return float(math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))


def _check_one_cell(*, cell: dict[str, Any]) -> CheckResult:
    origin_xy: tuple[float, float] = (
        float(cell["origin_xy"][0]),
        float(cell["origin_xy"][1]),
    )
    sections: list[dict[str, Any]] = cell["sections"]

    # Build name -> section dict to look up parents.
    section_by_stripped: dict[str, dict[str, Any]] = {s["name_stripped"]: s for s in sections}
    connectivity: dict[str, str] = cell["connectivity"]

    # Identify dendrite sections by kind.
    primary_secs: list[dict[str, Any]] = [s for s in sections if s["section_kind"] == "primary"]
    dendrite_secs: list[dict[str, Any]] = [
        s for s in sections if s["section_kind"] in {"primary", "non_terminal", "terminal"}
    ]
    non_primary_dends: list[dict[str, Any]] = [
        s for s in dendrite_secs if s["section_kind"] != "primary"
    ]

    n_primary: int = len(primary_secs)
    n_non_primary: int = len(non_primary_dends)
    n_dend: int = len(dendrite_secs)

    # -----------------------------------------------------------------------
    # Check 1: every primary stem's python_start_xy ≈ origin_xy.
    # -----------------------------------------------------------------------
    check1_pass: bool = True
    max_err_1: float = 0.0
    for sec in primary_secs:
        start_xy_raw: list[float] | None = sec["python_start_xy"]
        if start_xy_raw is None:
            check1_pass = False
            continue
        start_xy: tuple[float, float] = (float(start_xy_raw[0]), float(start_xy_raw[1]))
        err: float = _xy_distance(a=start_xy, b=origin_xy)
        if err > max_err_1:
            max_err_1 = err
        if not _xy_close(a=start_xy, b=origin_xy):
            check1_pass = False

    # -----------------------------------------------------------------------
    # Check 2: every non-primary section's python_start_xy ≈ parent.python_end_xy.
    # -----------------------------------------------------------------------
    check2_pass: bool = True
    max_err_2: float = 0.0
    for sec in non_primary_dends:
        child_start_raw: list[float] | None = sec["python_start_xy"]
        if child_start_raw is None:
            check2_pass = False
            continue
        child_start: tuple[float, float] = (float(child_start_raw[0]), float(child_start_raw[1]))
        parent_name_stripped: str | None = connectivity.get(sec["name_stripped"])
        if parent_name_stripped is None:
            # Non-primary dendrite missing a parent entry is itself a defect; flag.
            check2_pass = False
            continue
        parent_sec: dict[str, Any] | None = section_by_stripped.get(parent_name_stripped)
        if parent_sec is None:
            check2_pass = False
            continue
        parent_end_raw: list[float] | None = parent_sec["python_end_xy"]
        if parent_end_raw is None:
            check2_pass = False
            continue
        parent_end: tuple[float, float] = (float(parent_end_raw[0]), float(parent_end_raw[1]))
        err = _xy_distance(a=child_start, b=parent_end)
        if err > max_err_2:
            max_err_2 = err
        if not _xy_close(a=child_start, b=parent_end):
            check2_pass = False

    # -----------------------------------------------------------------------
    # Check 3: for every dendrite section, midpoint_xy_neuron lies on the Python line and
    # in the same frame as origin_xy.
    # -----------------------------------------------------------------------
    check3_pass: bool = True
    max_lateral: float = 0.0
    max_origin_dist: float = 0.0
    n_degenerate: int = 0
    for sec in dendrite_secs:
        mid_raw: list[float] | None = sec["midpoint_xy_neuron"]
        start_raw: list[float] | None = sec["python_start_xy"]
        end_raw: list[float] | None = sec["python_end_xy"]
        err_reason: str | None = sec["midpoint_error_reason"]
        if err_reason is not None or mid_raw is None:
            n_degenerate += 1
            check3_pass = False
            continue
        if start_raw is None or end_raw is None:
            check3_pass = False
            continue
        mid: tuple[float, float] = (float(mid_raw[0]), float(mid_raw[1]))
        start: tuple[float, float] = (float(start_raw[0]), float(start_raw[1]))
        end: tuple[float, float] = (float(end_raw[0]), float(end_raw[1]))
        # Sub-check 3a: lateral deviation in um from the line through start, end.
        # |cross(end - start, mid - start)| / |end - start| = perpendicular distance.
        cross_product: float = abs(
            (end[0] - start[0]) * (mid[1] - start[1]) - (end[1] - start[1]) * (mid[0] - start[0])
        )
        seg_len: float = _xy_distance(a=start, b=end)
        lateral_um: float = cross_product / max(seg_len, 1e-12)
        # Sub-check 3b: midpoint is in the same frame as origin_xy (coarse).
        dist_origin: float = _xy_distance(a=mid, b=origin_xy)
        max_lateral = max(max_lateral, lateral_um)
        max_origin_dist = max(max_origin_dist, dist_origin)
        if lateral_um > MIDPOINT_LATERAL_TOL_UM:
            check3_pass = False
        if dist_origin > MAX_MIDPOINT_FROM_ORIGIN_UM:
            check3_pass = False

    return CheckResult(
        check1_primary_start=check1_pass,
        check2_parent_child=check2_pass,
        check3_synapse_frame=check3_pass,
        n_primary_stems=n_primary,
        n_non_primary_sections=n_non_primary,
        n_dendrite_sections=n_dend,
        max_check1_error_um=max_err_1,
        max_check2_error_um=max_err_2,
        max_check3_lateral_error_um=max_lateral,
        max_check3_origin_distance_um=max_origin_dist,
        check3_n_degenerate_sections=n_degenerate,
    )


def _row_for_cell(*, cell: dict[str, Any], result: CheckResult) -> dict[str, Any]:
    asym: dict[str, float] = cell["asymmetry_params"]
    origin_xy: list[float] = cell["origin_xy"]
    soma_min: list[float] = cell["soma_pt3d_xy_min"]
    soma_max: list[float] = cell["soma_pt3d_xy_max"]
    return {
        CELL_ID_COL: cell["cell_id"],
        SOURCE_TASK_COL: cell["source_task"],
        SEED_COL: int(cell["seed"]),
        GENERATION_COL: int(cell["generation"]),
        INDIVIDUAL_IDX_COL: int(cell["individual_idx"]),
        STRATUM_TAG_COL: cell["stratum_tag"],
        "soma_offset_pd_um": float(asym["soma_offset_pd_um"]),
        "field_elongation_pd": float(asym["field_elongation_pd"]),
        "branch_density_gradient_pd": float(asym["branch_density_gradient_pd"]),
        "primary_branch_pd_concentration": float(asym["primary_branch_pd_concentration"]),
        "soma_diameter_um": float(asym["soma_diameter_um"]),
        CHECK1_PRIMARY_START_COL: result.check1_primary_start,
        CHECK2_PARENT_CHILD_COL: result.check2_parent_child,
        CHECK3_SYNAPSE_FRAME_COL: result.check3_synapse_frame,
        "n_primary_stems": result.n_primary_stems,
        "n_non_primary_sections": result.n_non_primary_sections,
        "n_dendrite_sections": result.n_dendrite_sections,
        "max_check1_error_um": result.max_check1_error_um,
        "max_check2_error_um": result.max_check2_error_um,
        "max_check3_lateral_error_um": result.max_check3_lateral_error_um,
        "max_check3_origin_distance_um": result.max_check3_origin_distance_um,
        "check3_n_degenerate_sections": result.check3_n_degenerate_sections,
        "soma_origin_x": float(origin_xy[0]),
        "soma_origin_y": float(origin_xy[1]),
        "soma_pt3d_x_min": float(soma_min[0]),
        "soma_pt3d_x_max": float(soma_max[0]),
        "soma_pt3d_y_min": float(soma_min[1]),
        "soma_pt3d_y_max": float(soma_max[1]),
        "soma_frame_offset_um": float(cell["soma_frame_offset_um"]),
    }


def main() -> None:
    print(f"[checks] reading {SECTION_ENDPOINTS_DUMP_JSON}", flush=True)
    payload: list[dict[str, Any]] = json.loads(
        SECTION_ENDPOINTS_DUMP_JSON.read_text(encoding="utf-8")
    )
    print(f"[checks] loaded {len(payload)} cells", flush=True)

    rows: list[dict[str, Any]] = []
    for cell in payload:
        result: CheckResult = _check_one_cell(cell=cell)
        rows.append(_row_for_cell(cell=cell, result=result))
        expected_offset: float = abs(float(cell["asymmetry_params"]["soma_offset_pd_um"]))
        print(
            f"[checks] cell_id={cell['cell_id']} "
            f"check1={'pass' if result.check1_primary_start else 'FAIL'} "
            f"check2={'pass' if result.check2_parent_child else 'FAIL'} "
            f"check3={'pass' if result.check3_synapse_frame else 'FAIL'} "
            f"soma_frame_offset={float(cell['soma_frame_offset_um']):.3f} "
            f"(expected={expected_offset:.3f}) "
            f"n_degenerate={result.check3_n_degenerate_sections}",
            flush=True,
        )

    df: pd.DataFrame = pd.DataFrame(rows)
    df.to_csv(path_or_buf=COORDINATE_CONSISTENCY_CHECKS_CSV, index=False)
    print(f"[checks] wrote {COORDINATE_CONSISTENCY_CHECKS_CSV}", flush=True)

    n_check1: int = int(df[CHECK1_PRIMARY_START_COL].sum())
    n_check2: int = int(df[CHECK2_PARENT_CHILD_COL].sum())
    n_check3: int = int(df[CHECK3_SYNAPSE_FRAME_COL].sum())
    n_total: int = len(df)
    print(
        f"[checks] PASS counts: "
        f"check1={n_check1}/{n_total}, "
        f"check2={n_check2}/{n_total}, "
        f"check3={n_check3}/{n_total}",
        flush=True,
    )

    # Soma-frame consistency: expected offset == |soma_offset_pd_um|.
    diffs: pd.Series = (df["soma_frame_offset_um"] - df["soma_offset_pd_um"].abs()).abs()
    max_soma_frame_offset_residual: float = float(diffs.max())
    print(
        f"[checks] max |soma_frame_offset_um - |soma_offset_pd_um|| = "
        f"{max_soma_frame_offset_residual:.6f} um (should be ~ 0)",
        flush=True,
    )


if __name__ == "__main__":
    main()
