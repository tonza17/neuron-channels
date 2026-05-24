"""Helpers for dumping NEURON pt3d, building MorphologyParams, and applying the NEURON DLL bypass.

Copied / adapted (per the cross-task code-reuse rule):

* NEURON DLL bypass (~10 lines): from
  `tasks/t0115_seed9354_no_autostop/code/build_top50_morphologies.py` lines 42-59.
* `Pt3dPoint`, `SectionDump`, `_collect_pt3d`, `_pt3d_euclidean_length`, `_section_area`,
  `_dump_one_section`, `_parent_name`: from
  `tasks/t0092_diagnose_morphology_generator_silence/code/structural_dump.py`.
* `_section_midpoint_xy_strict`: adapted from
  `tasks/t0091_morphology_extended_nsga2_v1/code/trial_helpers.py` lines 160-178 with the silent
  `(0.0, 0.0)` fallback replaced by a `RuntimeError` so degenerate sections are caught as audit
  failures rather than masked.
* `_params_from_14d`: from `build_top50_morphologies.py` lines 100-116.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)

# ---------------------------------------------------------------------------
# NEURON DLL bypass (must be applied before any generate_fixed_morphology call).
# ---------------------------------------------------------------------------


def _noop_ensure_dll_loaded(*, h: Any) -> None:  # noqa: ARG001
    return None


def install_neuron_dll_bypass() -> None:
    """Monkey-patch `ensure_t80_dll_loaded` on both t0080 and t0090 generator modules.

    This skips compilation of the t0024 + t0080 MOD libraries when only geometry is needed.
    Idempotent: safe to call multiple times.
    """
    from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code import (
        apply_params as _t80_apply_params,
    )
    from tasks.t0090_morphology_generator_diversity_test.code import (
        generator as _t90_generator,
    )

    _t80_apply_params.ensure_t80_dll_loaded = _noop_ensure_dll_loaded
    _t90_generator.ensure_t80_dll_loaded = _noop_ensure_dll_loaded


# ---------------------------------------------------------------------------
# pt3d collection helpers (copied from t0092 structural_dump.py).
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Pt3dPoint:
    x: float
    y: float
    z: float
    diam: float


@dataclass(frozen=True, slots=True)
class SectionDump:
    """Per-section dump combining Python-frame endpoints with NEURON pt3d.

    Extends the t0092 SectionDump with three audit-specific fields:
    `python_start_xy`, `python_end_xy` (from MorphologyResult.section_endpoints_xy), and
    `midpoint_xy_neuron` (from the strict `_section_midpoint_xy` helper).
    """

    name: str
    name_stripped: str  # name with the "_t90" NEURON suffix removed
    parent_name: str | None  # NEURON parent section name (with "_t90" suffix)
    parent_name_stripped: str | None
    section_kind: str  # one of: soma, primary, non_terminal, terminal, ais_proximal, ais_distal
    sec_l_neuron: float
    nseg: int
    diam: float
    area_um2: float
    pt3d: list[Pt3dPoint]
    pt3d_euclidean_length_um: float
    python_start_xy: tuple[float, float] | None
    python_end_xy: tuple[float, float] | None
    midpoint_xy_neuron: tuple[float, float] | None
    midpoint_error_reason: str | None  # None if midpoint was computed cleanly


@dataclass(frozen=True, slots=True)
class CellDump:
    """Per-cell dump used by run_checks.py to evaluate Check 1, Check 2, Check 3."""

    cell_id: str
    source_task: str
    seed: int
    generation: int
    individual_idx: int
    stratum_tag: str
    asymmetry_params: dict[str, float]
    origin_xy: tuple[float, float]
    soma_pt3d_xy_min: tuple[float, float]
    soma_pt3d_xy_max: tuple[float, float]
    soma_frame_offset_um: float
    n_sections: int
    n_primary: int
    n_non_primary_dends: int
    n_dendrites: int
    sections: list[SectionDump]
    connectivity: dict[str, str]  # child -> parent (NEURON-suffix-stripped)


def _collect_pt3d(*, h: Any, sec: Any) -> list[Pt3dPoint]:
    sec.push()
    try:
        n = int(h.n3d())
        out: list[Pt3dPoint] = []
        for i in range(n):
            out.append(
                Pt3dPoint(
                    x=float(h.x3d(i)),
                    y=float(h.y3d(i)),
                    z=float(h.z3d(i)),
                    diam=float(h.diam3d(i)),
                )
            )
        return out
    finally:
        h.pop_section()


def _pt3d_euclidean_length(*, pt3d: list[Pt3dPoint]) -> float:
    if len(pt3d) < 2:
        return 0.0
    total: float = 0.0
    for i in range(1, len(pt3d)):
        dx = pt3d[i].x - pt3d[i - 1].x
        dy = pt3d[i].y - pt3d[i - 1].y
        dz = pt3d[i].z - pt3d[i - 1].z
        total += math.sqrt(dx * dx + dy * dy + dz * dz)
    return float(total)


def _section_area(*, sec: Any) -> float:
    total: float = 0.0
    for seg in sec:
        total += float(seg.area())
    return float(total)


def _strip_t90_suffix(*, name: str) -> str:
    """Remove the "_t90" suffix appended by the t0090 generator's NEURON sections."""
    suffix: str = "_t90"
    if name.endswith(suffix):
        return name[: -len(suffix)]
    return name


def _parent_name(*, h: Any, sec: Any) -> str | None:
    sec.push()
    try:
        sref = h.SectionRef(sec=sec)
        if not bool(sref.has_parent()):
            return None
        parent = sref.parent
        return str(parent.name())
    finally:
        h.pop_section()


def _section_midpoint_xy_strict(
    *,
    h: Any,
    section: Any,
) -> tuple[tuple[float, float] | None, str | None]:
    """Return the (x, y) of the section's midpoint pt3d, or (None, reason) on degeneracy.

    Adapted from `tasks/t0091_morphology_extended_nsga2_v1/code/trial_helpers.py`
    `_section_midpoint_xy`. The original silently returns (0.0, 0.0) on `n3d() == 0`,
    which would mask the very bug t0120 is auditing. This strict copy returns `(None, reason)`
    so callers can flag degenerate sections explicitly.
    """
    section.push()
    try:
        n_pts = int(h.n3d())
        if n_pts == 0:
            return None, "n3d() == 0 (no pt3d points emitted)"
        if n_pts % 2 == 1:
            mid: int = (n_pts - 1) // 2
            return (float(h.x3d(mid)), float(h.y3d(mid))), None
        a: int = n_pts // 2
        b: int = a - 1
        midpoint: tuple[float, float] = (
            (float(h.x3d(a)) + float(h.x3d(b))) / 2.0,
            (float(h.y3d(a)) + float(h.y3d(b))) / 2.0,
        )
        return midpoint, None
    finally:
        h.pop_section()


def _dump_one_section(
    *,
    h: Any,
    sec: Any,
    section_kind: str,
    python_start_xy: tuple[float, float] | None,
    python_end_xy: tuple[float, float] | None,
) -> SectionDump:
    pt3d: list[Pt3dPoint] = _collect_pt3d(h=h, sec=sec)
    midpoint, midpoint_err = _section_midpoint_xy_strict(h=h, section=sec)
    name: str = str(sec.name())
    parent_name_raw: str | None = _parent_name(h=h, sec=sec)
    return SectionDump(
        name=name,
        name_stripped=_strip_t90_suffix(name=name),
        parent_name=parent_name_raw,
        parent_name_stripped=(
            _strip_t90_suffix(name=parent_name_raw) if parent_name_raw is not None else None
        ),
        section_kind=section_kind,
        sec_l_neuron=float(sec.L),
        nseg=int(sec.nseg),
        diam=float(sec.diam),
        area_um2=_section_area(sec=sec),
        pt3d=pt3d,
        pt3d_euclidean_length_um=_pt3d_euclidean_length(pt3d=pt3d),
        python_start_xy=python_start_xy,
        python_end_xy=python_end_xy,
        midpoint_xy_neuron=midpoint,
        midpoint_error_reason=midpoint_err,
    )


# ---------------------------------------------------------------------------
# 14-d morphology vector -> MorphologyParams (copied from t0115).
# ---------------------------------------------------------------------------


def _params_from_14d(*, vec: tuple[float, ...]) -> MorphologyParams:
    return MorphologyParams(
        num_primary_branches=int(round(vec[0])),
        branch_prob_per_um=float(vec[1]),
        max_strahler_depth=int(round(vec[2])),
        mean_branching_angle_deg=float(vec[3]),
        rall_exponent=float(vec[4]),
        soma_offset_pd_um=float(vec[5]),
        field_elongation_pd=float(vec[6]),
        branch_density_gradient_pd=float(vec[7]),
        primary_branch_pd_concentration=float(vec[8]),
        mean_segment_length_um=float(vec[9]),
        soma_diameter_um=float(vec[10]),
        ais_length_um=float(vec[11]),
        morph_seed=int(round(vec[12])),
        branch_length_cv=float(vec[13]),
    )
