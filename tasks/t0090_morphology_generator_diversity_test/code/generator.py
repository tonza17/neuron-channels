"""Procedural DSGC morphology generator.

Builds a NEURON-compatible cell from 14 morphology knobs. The result mirrors the
t0080 ``DSGCCellWithAIS`` interface so downstream code (``apply_parameter_vector``,
the trial driver) consumes it without modification.

Implementation notes:

* Topology is generated as a Python tree first (lightweight node objects) and
  the NEURON sections are materialised in a second pass. This separation keeps
  the asymmetry transforms (soma offset, field elongation, density gradient)
  off the NEURON side: they only mutate Python coordinates and length scaling
  before the sections are created.
* Branching uses ``rng.random()`` per attempted child placement; the
  probability of a daughter pair at any node is ``branch_prob_per_um *
  segment_length_um``. The recursion is bounded by ``max_strahler_depth``.
* Primary stems are placed in 2D from the soma using a von Mises distribution
  centred on the PD axis (``mu = 0`` rad), with concentration kappa =
  ``primary_branch_pd_concentration``. ``kappa = 0`` yields uniform.
* Daughter diameters obey Rall's generalised power law:
  ``d_parent**rall = d_d1**rall + d_d2**rall``. We currently emit binary
  branching (``num_daughters = 2``); the parent diameter is ``d_parent`` and
  daughters share an equal split: ``d_daughter = d_parent / 2**(1/rall)``.
* Every section's ``nseg`` is set by NEURON's d_lambda rule
  (``freq=100 Hz``, ``d_lambda=0.1``).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import (
    _ensure_neuron_on_path,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
    ensure_t80_dll_loaded,
)
from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    AIS_DEFAULT_DIAMETER_UM,
    AIS_PROXIMAL_FRACTION,
    CHILD_BASE_LOC,
    D_LAMBDA,
    DEFAULT_CM_UF_CM2,
    DEFAULT_DENDRITE_DIAMETER_UM,
    DEFAULT_RA_OHM_CM,
    DEFAULT_TIP_DIAMETER_UM,
    LAMBDA_F_FREQ_HZ,
    PARENT_TIP_LOC,
    StabilityKind,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
    MorphologyResult,
    MorphometricSummary,
)

# ---------------------------------------------------------------------------
# Process-level NEURON loader guard.
#
# Multiple calls to ``generate_morphology`` from the same process must not
# re-load the t0024 / t0080 mod libraries. Re-loading raises
# ``NEURON: The user defined name already exists: Exp2NMDA``.
# ---------------------------------------------------------------------------

_LOADED_H: Any | None = None


def _get_neuron_h() -> Any:
    """Return a process-singleton ``h`` with both t0024 and t0080 DLLs loaded.

    All loads are guarded so repeat calls are no-ops. NEURON raises
    ``user defined name already exists`` if the same MOD library is loaded twice
    in one process. We track which DLL paths we have already loaded.
    """
    global _LOADED_H
    if _LOADED_H is not None:
        return _LOADED_H

    _ensure_neuron_on_path()

    from neuron import h  # type: ignore[import-untyped]

    # Source stdrun. NEURON also complains about duplicate template definitions
    # when stdrun.hoc is loaded twice; we silently ignore the second load attempt.
    from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C24
    from tasks.t0024_port_de_rosenroll_2026_dsgc.code import paths as P24

    stdrun_path = str(
        __import__("pathlib").Path(C24.NEURONHOME_DEFAULT) / "lib" / "hoc" / "stdrun.hoc"
    ).replace("\\", "/")
    h.load_file(1, stdrun_path)

    # Load t0024 nrnmech.dll (HHst + cad + Exp2NMDA) once per process.
    t24_dll = str(P24.NRNMECH_DLL).replace("\\", "/")
    rc24 = h.nrn_load_dll(t24_dll)
    assert rc24 == 1.0, f"h.nrn_load_dll failed for t0024 DLL {t24_dll}"

    # Load t0080 nrnmech.dll (the 13 t80 channels) once per process.
    ensure_t80_dll_loaded(h=h)

    _LOADED_H = h
    return h


# ---------------------------------------------------------------------------
# Internal Python tree (lightweight; not NEURON-coupled).
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class _Node:
    """One section in the topology tree, before NEURON instantiation."""

    name: str
    parent: _Node | None
    depth: int
    length_um: float
    diameter_um: float
    angle_rad: float  # absolute angle of this segment from soma
    start_xy: tuple[float, float]
    end_xy: tuple[float, float]
    children: list[_Node] = field(default_factory=list)
    is_primary: bool = False


def _compute_nseg(*, h: Any, section: Any) -> int:
    """Compute nseg per d_lambda=0.1 rule at 100 Hz, rounded to nearest odd."""
    section.push()
    try:
        lam = float(h.lambda_f(LAMBDA_F_FREQ_HZ, sec=section))
    finally:
        h.pop_section()
    if lam <= 0.0 or math.isnan(lam):
        return 5
    raw = float(section.L) / (D_LAMBDA * lam)
    return max(1, int(raw / 2.0) * 2 + 1)


def _sample_primary_angles(
    *,
    n_branches: int,
    kappa: float,
    rng: np.random.Generator,
) -> NDArray[np.float64]:
    """Sample primary-stem angles around mu=0 (PD axis) via von Mises.

    kappa=0 is treated as uniform [-pi, pi). This is the numpy convention.
    """
    if kappa <= 0.0:
        out: NDArray[np.float64] = rng.uniform(-math.pi, math.pi, size=n_branches)
        return out
    samples: NDArray[np.float64] = rng.vonmises(mu=0.0, kappa=float(kappa), size=n_branches)
    return samples


def _segment_length_for(
    *,
    mean_um: float,
    cv: float,
    rng: np.random.Generator,
) -> float:
    """Sample a positive segment length from a truncated normal.

    Uses ``mean * (1 + cv * normal())`` clipped to [0.1*mean, 3*mean].
    """
    raw = float(mean_um * (1.0 + cv * float(rng.normal())))
    return float(np.clip(raw, 0.1 * mean_um, 3.0 * mean_um))


def _branching_angle_for(
    *,
    mean_deg: float,
    cv: float,
    rng: np.random.Generator,
) -> float:
    """Sample a branching half-angle in radians."""
    raw = float(mean_deg + rng.normal() * cv * 30.0)
    raw = float(np.clip(raw, 5.0, 175.0))
    return math.radians(raw / 2.0)


def _daughter_diameter(
    *,
    parent_diam_um: float,
    rall_exponent: float,
    n_daughters: int,
) -> float:
    """Apply Rall's generalised power law for an equal-split branch."""
    assert n_daughters >= 1
    if rall_exponent <= 0.0:
        return parent_diam_um
    return float(parent_diam_um / (n_daughters ** (1.0 / rall_exponent)))


def _build_topology(
    *,
    params: MorphologyParams,
    rng: np.random.Generator,
) -> tuple[_Node, list[_Node]]:
    """Build the topology tree; return the soma node and the flat list of all dendrites."""
    soma_xy: tuple[float, float] = (0.0, 0.0)
    soma = _Node(
        name="soma",
        parent=None,
        depth=0,
        length_um=float(params.soma_diameter_um),
        diameter_um=float(params.soma_diameter_um),
        angle_rad=0.0,
        start_xy=soma_xy,
        end_xy=soma_xy,
    )

    primary_angles = _sample_primary_angles(
        n_branches=int(params.num_primary_branches),
        kappa=float(params.primary_branch_pd_concentration),
        rng=rng,
    )

    all_dends: list[_Node] = []
    for primary_idx, angle in enumerate(primary_angles):
        primary = _grow_branch(
            parent=soma,
            depth=1,
            angle_rad=float(angle),
            base_xy=soma_xy,
            base_diameter_um=DEFAULT_DENDRITE_DIAMETER_UM,
            primary_index=primary_idx,
            params=params,
            rng=rng,
            collected=all_dends,
        )
        primary.is_primary = True
        soma.children.append(primary)

    return soma, all_dends


def _grow_branch(
    *,
    parent: _Node,
    depth: int,
    angle_rad: float,
    base_xy: tuple[float, float],
    base_diameter_um: float,
    primary_index: int,
    params: MorphologyParams,
    rng: np.random.Generator,
    collected: list[_Node],
) -> _Node:
    """Recursively grow one dendritic branch from base_xy in angle_rad direction."""
    length_um = _segment_length_for(
        mean_um=float(params.mean_segment_length_um),
        cv=float(params.branch_length_cv),
        rng=rng,
    )
    end_xy = (
        base_xy[0] + length_um * math.cos(angle_rad),
        base_xy[1] + length_um * math.sin(angle_rad),
    )
    name = f"dend_p{primary_index}_d{depth}_n{len(collected)}"
    node = _Node(
        name=name,
        parent=parent,
        depth=depth,
        length_um=length_um,
        diameter_um=float(base_diameter_um),
        angle_rad=angle_rad,
        start_xy=base_xy,
        end_xy=end_xy,
    )
    collected.append(node)

    # Termination: depth bound or stochastic stop.
    if depth >= int(params.max_strahler_depth):
        return node

    # Probability of branching scales linearly with segment length (per micron).
    branch_prob = float(params.branch_prob_per_um) * length_um
    branch_prob = float(np.clip(branch_prob, 0.0, 1.0))

    # Density gradient: bias branching toward / away from the PD axis depending on
    # the sign of branch_density_gradient_pd. A value of 0 disables the bias.
    if abs(params.branch_density_gradient_pd) > 1e-12:
        # Project end_xy onto the PD axis (cos of angle from PD).
        pd_projection = math.cos(math.atan2(end_xy[1], end_xy[0]))
        branch_prob = float(
            np.clip(
                branch_prob * (1.0 + float(params.branch_density_gradient_pd) * pd_projection),
                0.0,
                1.0,
            )
        )

    if float(rng.random()) >= branch_prob:
        return node

    # Daughter pair.
    half_angle = _branching_angle_for(
        mean_deg=float(params.mean_branching_angle_deg),
        cv=float(params.branch_length_cv),
        rng=rng,
    )
    d_diam = _daughter_diameter(
        parent_diam_um=base_diameter_um,
        rall_exponent=float(params.rall_exponent),
        n_daughters=2,
    )
    d_diam = max(d_diam, DEFAULT_TIP_DIAMETER_UM)

    for sign in (-1.0, +1.0):
        child_angle = angle_rad + sign * half_angle
        child = _grow_branch(
            parent=node,
            depth=depth + 1,
            angle_rad=child_angle,
            base_xy=end_xy,
            base_diameter_um=d_diam,
            primary_index=primary_index,
            params=params,
            rng=rng,
            collected=collected,
        )
        node.children.append(child)

    return node


def _apply_asymmetry(*, soma: _Node, all_dends: list[_Node], params: MorphologyParams) -> None:
    """Apply the post-hoc asymmetry transforms to (start_xy, end_xy) coordinates."""
    soma_offset = float(params.soma_offset_pd_um)
    elong = float(params.field_elongation_pd)

    soma_new = (soma.start_xy[0] + soma_offset, soma.start_xy[1])
    soma.start_xy = soma_new
    soma.end_xy = soma_new

    for node in all_dends:
        # Soma offset shifts every section root and tip in PD (x).
        sx, sy = node.start_xy
        ex, ey = node.end_xy
        # Apply soma offset to entire tree (so primary-branch base sits at offset soma).
        sx += soma_offset
        ex += soma_offset
        # Apply PD-axis stretch.
        sx_dx = sx - soma_offset
        ex_dx = ex - soma_offset
        sx = soma_offset + elong * sx_dx
        ex = soma_offset + elong * ex_dx
        node.start_xy = (sx, sy)
        node.end_xy = (ex, ey)


def _materialise_neuron_sections(
    *,
    h: Any,
    soma_node: _Node,
    all_dend_nodes: list[_Node],
    params: MorphologyParams,
) -> tuple[
    Any,
    list[Any],
    list[Any],
    list[Any],
    list[Any],
    Any,
    Any,
    dict[str, str],
    dict[str, tuple[float, float, float, float]],
]:
    """Build NEURON sections for the soma, every dendrite node, and the AIS.

    Returns: ``(soma, all_dends, primary_dends, non_terminal_dends, terminal_dends,
    ais_proximal, ais_distal, connectivity, section_endpoints_xy)``.
    """
    # Soma.
    soma_sec = h.Section(name="soma_t90")
    soma_sec.L = float(params.soma_diameter_um)
    soma_sec.diam = float(params.soma_diameter_um)
    soma_sec.Ra = DEFAULT_RA_OHM_CM
    soma_sec.cm = DEFAULT_CM_UF_CM2
    soma_sec.nseg = _compute_nseg(h=h, section=soma_sec)

    # Add pt3dadd for the soma so h.n3d() works downstream. Soma is a single
    # spheroid: emit start and end at the same xy with the soma diameter.
    soma_sec.push()
    try:
        h.pt3dadd(
            float(soma_node.start_xy[0]),
            float(soma_node.start_xy[1]),
            0.0,
            float(soma_node.diameter_um),
        )
        h.pt3dadd(
            float(soma_node.end_xy[0]),
            float(soma_node.end_xy[1]),
            0.0,
            float(soma_node.diameter_um),
        )
    finally:
        h.pop_section()

    sections_by_node: dict[str, Any] = {soma_node.name: soma_sec}
    section_endpoints_xy: dict[str, tuple[float, float, float, float]] = {
        soma_node.name: (
            soma_node.start_xy[0],
            soma_node.start_xy[1],
            soma_node.end_xy[0],
            soma_node.end_xy[1],
        )
    }
    all_dend_secs: list[Any] = []
    primary_secs: list[Any] = []
    non_terminal_secs: list[Any] = []
    terminal_secs: list[Any] = []
    connectivity: dict[str, str] = {}

    for node in all_dend_nodes:
        sec = h.Section(name=f"{node.name}_t90")
        sec.L = float(node.length_um)
        sec.diam = float(node.diameter_um)
        sec.Ra = DEFAULT_RA_OHM_CM
        sec.cm = DEFAULT_CM_UF_CM2
        sec.nseg = _compute_nseg(h=h, section=sec)
        # Add pt3dadd for the start and end of this dendritic section.
        sec.push()
        try:
            h.pt3dadd(
                float(node.start_xy[0]),
                float(node.start_xy[1]),
                0.0,
                float(node.diameter_um),
            )
            h.pt3dadd(
                float(node.end_xy[0]),
                float(node.end_xy[1]),
                0.0,
                float(node.diameter_um),
            )
        finally:
            h.pop_section()
        sections_by_node[node.name] = sec
        all_dend_secs.append(sec)
        section_endpoints_xy[node.name] = (
            node.start_xy[0],
            node.start_xy[1],
            node.end_xy[0],
            node.end_xy[1],
        )

    # Connect dendrites into the topology.
    for node in all_dend_nodes:
        if node.parent is None:
            continue
        parent_sec = sections_by_node[node.parent.name]
        child_sec = sections_by_node[node.name]
        child_sec.connect(parent_sec, PARENT_TIP_LOC, CHILD_BASE_LOC)
        connectivity[node.name] = node.parent.name

    for node in all_dend_nodes:
        sec = sections_by_node[node.name]
        if node.is_primary:
            primary_secs.append(sec)
        if len(node.children) == 0:
            terminal_secs.append(sec)
        else:
            non_terminal_secs.append(sec)

    # AIS sections (two halves attached to soma(0); per t0080 idiom soma(1) but the
    # procedural soma is a single point so we use soma(1)=tip just like t0080).
    total_ais_length = float(params.ais_length_um)
    proximal_length = max(1.0, total_ais_length * AIS_PROXIMAL_FRACTION)
    distal_length = max(1.0, total_ais_length - proximal_length)

    ais_proximal = h.Section(name="ais_proximal_t90")
    ais_proximal.L = float(proximal_length)
    ais_proximal.diam = float(AIS_DEFAULT_DIAMETER_UM)
    ais_proximal.Ra = DEFAULT_RA_OHM_CM
    ais_proximal.cm = DEFAULT_CM_UF_CM2
    ais_proximal.nseg = _compute_nseg(h=h, section=ais_proximal)
    ais_proximal.connect(soma_sec, PARENT_TIP_LOC, CHILD_BASE_LOC)

    ais_distal = h.Section(name="ais_distal_t90")
    ais_distal.L = float(distal_length)
    ais_distal.diam = float(AIS_DEFAULT_DIAMETER_UM)
    ais_distal.Ra = DEFAULT_RA_OHM_CM
    ais_distal.cm = DEFAULT_CM_UF_CM2
    ais_distal.nseg = _compute_nseg(h=h, section=ais_distal)
    ais_distal.connect(ais_proximal, PARENT_TIP_LOC, CHILD_BASE_LOC)

    return (
        soma_sec,
        all_dend_secs,
        primary_secs,
        non_terminal_secs,
        terminal_secs,
        ais_proximal,
        ais_distal,
        connectivity,
        section_endpoints_xy,
    )


def _compute_morphometric_summary(
    *,
    all_dend_nodes: list[_Node],
    params: MorphologyParams,
) -> MorphometricSummary:
    """Compute six morphometric features from the Python tree (no NEURON access)."""
    if len(all_dend_nodes) == 0:
        return MorphometricSummary(
            total_dendritic_length_um=0.0,
            branch_count=0,
            max_strahler_depth=0,
            electrotonic_length_lambda=0.0,
            soma_displacement_um=float(abs(params.soma_offset_pd_um)),
            field_major_axis_length_um=0.0,
        )

    total_length = sum(node.length_um for node in all_dend_nodes)
    branch_count = sum(1 for node in all_dend_nodes if len(node.children) > 0)
    max_depth = max(node.depth for node in all_dend_nodes)

    # Electrotonic length (max path L/lambda from soma to terminal). Use the
    # canonical lambda = sqrt((d * Rm) / (4 * Ra)) approximation with default
    # Rm = 1 / 1.667e-4 ohm.cm^2 and Ra = 100 ohm.cm.
    rm_ohm_cm2 = 1.0 / 1.667e-4
    ra_ohm_cm = DEFAULT_RA_OHM_CM
    max_l_lambda = 0.0
    for node in all_dend_nodes:
        if len(node.children) > 0:
            continue
        # Walk from this leaf to the soma summing L/lambda.
        cum = 0.0
        cur: _Node | None = node
        while cur is not None and cur.parent is not None:
            d_cm = float(cur.diameter_um) * 1e-4
            l_cm = float(cur.length_um) * 1e-4
            lam_cm = math.sqrt(max(d_cm * rm_ohm_cm2 / (4.0 * ra_ohm_cm), 1e-12))
            cum += l_cm / lam_cm
            cur = cur.parent
        max_l_lambda = max(max_l_lambda, cum)

    soma_disp = float(abs(params.soma_offset_pd_um))

    # Field major-axis length: max - min PD-coordinate of all section endpoints.
    pd_coords: list[float] = []
    for node in all_dend_nodes:
        pd_coords.append(node.start_xy[0])
        pd_coords.append(node.end_xy[0])
    field_major = float(max(pd_coords) - min(pd_coords)) if len(pd_coords) > 0 else 0.0

    return MorphometricSummary(
        total_dendritic_length_um=float(total_length),
        branch_count=int(branch_count),
        max_strahler_depth=int(max_depth),
        electrotonic_length_lambda=float(max_l_lambda),
        soma_displacement_um=float(soma_disp),
        field_major_axis_length_um=float(field_major),
    )


def _terminal_locs_xy(
    *,
    all_dend_nodes: list[_Node],
) -> NDArray[np.float64]:
    """Return (n_terminals, 2) array of terminal-section midpoints in xy."""
    coords: list[tuple[float, float]] = []
    for node in all_dend_nodes:
        if len(node.children) == 0:
            mid_x = 0.5 * (node.start_xy[0] + node.end_xy[0])
            mid_y = 0.5 * (node.start_xy[1] + node.end_xy[1])
            coords.append((mid_x, mid_y))
    if len(coords) == 0:
        out: NDArray[np.float64] = np.zeros((0, 2), dtype=np.float64)
        return out
    return np.array(coords, dtype=np.float64)


def generate_morphology(
    *,
    params: MorphologyParams,
    morph_seed: int | None = None,
) -> MorphologyResult:
    """Build a procedural DSGC cell from the 14 knobs.

    The ``morph_seed`` argument overrides ``params.morph_seed`` if provided.
    Determinism: same ``(params, morph_seed)`` produces byte-identical sections.
    """
    seed = int(morph_seed) if morph_seed is not None else int(params.morph_seed)
    rng = np.random.default_rng(seed)

    soma_node, all_dend_nodes = _build_topology(params=params, rng=rng)
    _apply_asymmetry(soma=soma_node, all_dends=all_dend_nodes, params=params)

    h = _get_neuron_h()

    (
        soma_sec,
        all_dend_secs,
        primary_secs,
        non_terminal_secs,
        terminal_secs,
        ais_proximal,
        ais_distal,
        connectivity,
        section_endpoints_xy,
    ) = _materialise_neuron_sections(
        h=h,
        soma_node=soma_node,
        all_dend_nodes=all_dend_nodes,
        params=params,
    )

    morphometric_summary = _compute_morphometric_summary(
        all_dend_nodes=all_dend_nodes,
        params=params,
    )
    terminal_locs = _terminal_locs_xy(all_dend_nodes=all_dend_nodes)

    return MorphologyResult(
        h=h,
        rgc=None,
        soma=soma_sec,
        all_dends=all_dend_secs,
        primary_dends=primary_secs,
        non_terminal_dends=non_terminal_secs,
        terminal_dends=terminal_secs,
        terminal_locs_xy=terminal_locs,
        origin_xy=(float(soma_node.end_xy[0]), float(soma_node.end_xy[1])),
        ais_proximal=ais_proximal,
        ais_distal=ais_distal,
        stability_flag=StabilityKind.STABLE,
        morphometric_summary=morphometric_summary,
        connectivity=connectivity,
        section_endpoints_xy=section_endpoints_xy,
    )
