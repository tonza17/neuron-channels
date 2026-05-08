"""Phase A: side-by-side per-section structural dump (REQ-1).

Builds the procedural BedB-equivalent cell and the t0024 hand-coded Bed B cell
in the same NEURON process and writes ``data/structural_comparison.json`` with
per-section data plus per-cell totals. The leading-hypothesis test is the soma
surface area: a ratio greater than ~2.0x flags soma-area mismatch as the
primary candidate cause of t0090's all-cell silence.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from typing import Any

from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    LAMBDA_F_FREQ_HZ,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyResult,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.build_cells import (
    TwoCells,
    build_both_cells,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.constants import (
    SPEC_VERSION_STRUCTURAL,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.paths import (
    STRUCTURAL_COMPARISON_JSON,
    ensure_directories,
)


@dataclass(frozen=True, slots=True)
class Pt3dPoint:
    x: float
    y: float
    z: float
    diam: float


@dataclass(frozen=True, slots=True)
class SectionDump:
    name: str
    parent_name: str | None
    sec_l_neuron: float
    nseg: int
    diam: float
    area_um2: float
    pt3d: list[Pt3dPoint]
    pt3d_euclidean_length_um: float
    electrotonic_length_lambda: float
    intended_length_um: float | None  # what the builder intended (procedural only)


@dataclass(frozen=True, slots=True)
class CellDump:
    cell_kind: str  # "procedural_bedb" or "handcoded_bedb"
    n_sections: int
    soma: SectionDump
    primary_dends: list[SectionDump]
    non_terminal_dends: list[SectionDump]
    terminal_dends: list[SectionDump]
    ais_proximal: SectionDump
    ais_distal: SectionDump
    origin_xy: tuple[float, float]
    soma_area_um2: float
    total_dendritic_length_um: float
    soma_to_terminal_max_path_um: float
    soma_to_terminal_max_l_lambda: float


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


def _electrotonic_length(*, h: Any, sec: Any) -> float:
    """Return ``L / lambda_f(100 Hz)`` for a section.

    Uses the t0090 generator's ``_compute_nseg`` invocation pattern:
    ``h.lambda_f(100, sec=section)`` outside of a push/pop block.

    Returns NaN when ``sec.L`` is below ``1e-6`` um (which happens for the
    procedural soma when its pt3dadd sequence yields a degenerate cylinder —
    the very bug under diagnosis); calling ``lambda_f`` on such a section
    raises a NEURON ``division by zero`` HOC error.
    """
    if float(sec.L) < 1e-6:
        return float("nan")
    try:
        lam = float(h.lambda_f(LAMBDA_F_FREQ_HZ, sec=sec))
    except (RuntimeError, ValueError, ArithmeticError):
        return float("nan")
    if lam <= 0.0 or math.isnan(lam):
        return float("nan")
    return float(sec.L) / lam


def _section_area(*, sec: Any) -> float:
    """Return total surface area in um^2 by summing per-segment area()."""
    total: float = 0.0
    for seg in sec:
        total += float(seg.area())
    return float(total)


def _dump_one_section(
    *,
    h: Any,
    sec: Any,
    parent_name: str | None,
    intended_length_um: float | None,
) -> SectionDump:
    pt3d = _collect_pt3d(h=h, sec=sec)
    return SectionDump(
        name=str(sec.name()),
        parent_name=parent_name,
        sec_l_neuron=float(sec.L),
        nseg=int(sec.nseg),
        diam=float(sec.diam),
        area_um2=_section_area(sec=sec),
        pt3d=pt3d,
        pt3d_euclidean_length_um=_pt3d_euclidean_length(pt3d=pt3d),
        electrotonic_length_lambda=_electrotonic_length(h=h, sec=sec),
        intended_length_um=intended_length_um,
    )


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


def _dump_procedural_cell(*, h: Any, cell: MorphologyResult) -> CellDump:
    intended_lengths: dict[str, float] = {}
    for name, (sx, sy, ex, ey) in cell.section_endpoints_xy.items():
        intended_lengths[name] = float(math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2))

    soma_dump = _dump_one_section(
        h=h,
        sec=cell.soma,
        parent_name=None,
        intended_length_um=None,
    )
    primary_dumps = [
        _dump_one_section(
            h=h,
            sec=sec,
            parent_name=_parent_name(h=h, sec=sec),
            intended_length_um=intended_lengths.get(str(sec.name()).replace("_t90", "")),
        )
        for sec in cell.primary_dends
    ]
    non_terminal_dumps = [
        _dump_one_section(
            h=h,
            sec=sec,
            parent_name=_parent_name(h=h, sec=sec),
            intended_length_um=intended_lengths.get(str(sec.name()).replace("_t90", "")),
        )
        for sec in cell.non_terminal_dends
    ]
    terminal_dumps = [
        _dump_one_section(
            h=h,
            sec=sec,
            parent_name=_parent_name(h=h, sec=sec),
            intended_length_um=intended_lengths.get(str(sec.name()).replace("_t90", "")),
        )
        for sec in cell.terminal_dends
    ]
    ais_prox = _dump_one_section(
        h=h,
        sec=cell.ais_proximal,
        parent_name=_parent_name(h=h, sec=cell.ais_proximal),
        intended_length_um=None,
    )
    ais_dist = _dump_one_section(
        h=h,
        sec=cell.ais_distal,
        parent_name=_parent_name(h=h, sec=cell.ais_distal),
        intended_length_um=None,
    )
    total_dend_length = float(
        sum(d.sec_l_neuron for d in primary_dumps + non_terminal_dumps + terminal_dumps)
    )
    max_path, max_l_lambda = _max_path_to_terminal(
        h=h,
        soma=cell.soma,
        terminals=list(cell.terminal_dends),
    )
    n_total = 1 + len(cell.all_dends) + 2  # soma + dends + 2 AIS
    return CellDump(
        cell_kind="procedural_bedb",
        n_sections=n_total,
        soma=soma_dump,
        primary_dends=primary_dumps,
        non_terminal_dends=non_terminal_dumps,
        terminal_dends=terminal_dumps,
        ais_proximal=ais_prox,
        ais_distal=ais_dist,
        origin_xy=(float(cell.origin_xy[0]), float(cell.origin_xy[1])),
        soma_area_um2=soma_dump.area_um2,
        total_dendritic_length_um=total_dend_length,
        soma_to_terminal_max_path_um=max_path,
        soma_to_terminal_max_l_lambda=max_l_lambda,
    )


def _dump_handcoded_cell(*, h: Any, cell: Any) -> CellDump:
    soma_dump = _dump_one_section(
        h=h,
        sec=cell.soma,
        parent_name=None,
        intended_length_um=None,
    )
    primary_dumps = [
        _dump_one_section(
            h=h,
            sec=sec,
            parent_name=_parent_name(h=h, sec=sec),
            intended_length_um=None,
        )
        for sec in cell.primary_dends
    ]
    non_terminal_dumps = [
        _dump_one_section(
            h=h,
            sec=sec,
            parent_name=_parent_name(h=h, sec=sec),
            intended_length_um=None,
        )
        for sec in cell.non_terminal_dends
    ]
    terminal_dumps = [
        _dump_one_section(
            h=h,
            sec=sec,
            parent_name=_parent_name(h=h, sec=sec),
            intended_length_um=None,
        )
        for sec in cell.terminal_dends
    ]
    ais_prox = _dump_one_section(
        h=h,
        sec=cell.ais_proximal,
        parent_name=_parent_name(h=h, sec=cell.ais_proximal),
        intended_length_um=None,
    )
    ais_dist = _dump_one_section(
        h=h,
        sec=cell.ais_distal,
        parent_name=_parent_name(h=h, sec=cell.ais_distal),
        intended_length_um=None,
    )
    total_dend_length = float(
        sum(d.sec_l_neuron for d in primary_dumps + non_terminal_dumps + terminal_dumps)
    )
    max_path, max_l_lambda = _max_path_to_terminal(
        h=h,
        soma=cell.soma,
        terminals=list(cell.terminal_dends),
    )
    n_total = 1 + len(cell.all_dends) + 2
    return CellDump(
        cell_kind="handcoded_bedb",
        n_sections=n_total,
        soma=soma_dump,
        primary_dends=primary_dumps,
        non_terminal_dends=non_terminal_dumps,
        terminal_dends=terminal_dumps,
        ais_proximal=ais_prox,
        ais_distal=ais_dist,
        origin_xy=(float(cell.origin_xy[0]), float(cell.origin_xy[1])),
        soma_area_um2=soma_dump.area_um2,
        total_dendritic_length_um=total_dend_length,
        soma_to_terminal_max_path_um=max_path,
        soma_to_terminal_max_l_lambda=max_l_lambda,
    )


def _max_path_to_terminal(
    *,
    h: Any,
    soma: Any,
    terminals: list[Any],
) -> tuple[float, float]:
    """Return (max_path_um, max_l_lambda) from soma(0.5) to any terminal(0.5)."""
    if len(terminals) == 0:
        return (0.0, 0.0)
    h.distance(0, soma(0.5))
    max_path: float = 0.0
    max_l_lambda: float = 0.0
    for term in terminals:
        d_um = float(h.distance(term(0.5)))
        if d_um > max_path:
            max_path = d_um
        # Approximate L/lambda by walking the section's own L over its lambda;
        # the precise per-path electrotonic distance walk is expensive and the
        # approximation is good enough for the diagnostic.
        l_l = _electrotonic_length(h=h, sec=term)
        if not math.isnan(l_l) and l_l > max_l_lambda:
            max_l_lambda = l_l
    return (max_path, max_l_lambda)


def _serialise_section(*, sec: SectionDump) -> dict[str, Any]:
    out: dict[str, Any] = asdict(sec)
    return out


def _serialise_cell(*, cell: CellDump) -> dict[str, Any]:
    return {
        "cell_kind": cell.cell_kind,
        "n_sections": cell.n_sections,
        "soma": _serialise_section(sec=cell.soma),
        "primary_dends": [_serialise_section(sec=s) for s in cell.primary_dends],
        "non_terminal_dends": [_serialise_section(sec=s) for s in cell.non_terminal_dends],
        "terminal_dends": [_serialise_section(sec=s) for s in cell.terminal_dends],
        "ais_proximal": _serialise_section(sec=cell.ais_proximal),
        "ais_distal": _serialise_section(sec=cell.ais_distal),
        "origin_xy": list(cell.origin_xy),
        "soma_area_um2": cell.soma_area_um2,
        "total_dendritic_length_um": cell.total_dendritic_length_um,
        "soma_to_terminal_max_path_um": cell.soma_to_terminal_max_path_um,
        "soma_to_terminal_max_l_lambda": cell.soma_to_terminal_max_l_lambda,
    }


def run_structural_dump(*, two: TwoCells) -> dict[str, Any]:
    proc_dump = _dump_procedural_cell(h=two.h, cell=two.procedural_bedb)
    hand_dump = _dump_handcoded_cell(h=two.h, cell=two.handcoded_bedb)
    soma_ratio = (
        proc_dump.soma_area_um2 / hand_dump.soma_area_um2 if hand_dump.soma_area_um2 > 0 else None
    )
    return {
        "spec_version": SPEC_VERSION_STRUCTURAL,
        "procedural_bedb": _serialise_cell(cell=proc_dump),
        "handcoded_bedb": _serialise_cell(cell=hand_dump),
        "summary": {
            "procedural_soma_area_um2": proc_dump.soma_area_um2,
            "handcoded_soma_area_um2": hand_dump.soma_area_um2,
            "soma_area_ratio_proc_over_hand": soma_ratio,
            "procedural_n_sections": proc_dump.n_sections,
            "handcoded_n_sections": hand_dump.n_sections,
            "procedural_total_dendritic_length_um": proc_dump.total_dendritic_length_um,
            "handcoded_total_dendritic_length_um": hand_dump.total_dendritic_length_um,
        },
    }


def main() -> int:
    ensure_directories()
    two = build_both_cells()
    payload = run_structural_dump(two=two)
    STRUCTURAL_COMPARISON_JSON.write_text(json.dumps(payload, indent=2))
    summary = payload["summary"]
    print(f"procedural soma area: {summary['procedural_soma_area_um2']:.2f} um^2")
    print(f"handcoded  soma area: {summary['handcoded_soma_area_um2']:.2f} um^2")
    ratio = summary["soma_area_ratio_proc_over_hand"]
    print(f"soma area ratio (proc / hand): {ratio:.3f}" if ratio is not None else "ratio: N/A")
    print(f"wrote {STRUCTURAL_COMPARISON_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
