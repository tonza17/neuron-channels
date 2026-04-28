"""Pure-Python NEURON cell builder for the t0054 minimal DSGC.

Reads the calibrated SWC from t0009, collapses the 19 soma rows into one ``soma`` section, builds
one ``dend[i]`` ``h.Section`` per non-soma compartment with ``pt3dadd`` from the parent and child
3D coords, attaches a synthetic ``axon_initial_segment`` to ``soma(1)``, and assigns the
project's standard channel/passive parameters.

Channels:

* ``hh`` only on ``soma`` and ``axon_initial_segment``.
* ``pas`` (with ``g_pas = 1/Rm``, ``e_pas = V_INIT_MV``) on every dendrite.

All sections receive ``Ra = RA_OHM_CM`` and ``cm = CM_UF_PER_CM2``.

This is the t0052 cell builder copied verbatim with the import-path rewrite to t0054 â€” no
mechanistic changes (the cell is independent of NMDA).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tasks.t0055_nmda_mg_block_dsi_recovery.code.constants import (
    AIS_DIAMETER_UM,
    AIS_EL_HH_MV,
    AIS_GKBAR_S_PER_CM2,
    AIS_GL_S_PER_CM2,
    AIS_GNABAR_S_PER_CM2,
    AIS_LENGTH_UM,
    CM_UF_PER_CM2,
    RA_OHM_CM,
    RM_OHM_CM2,
    V_INIT_MV,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.swc_io import (
    SWC_TYPE_SOMA,
    SwcCompartment,
    parse_swc_file,
    validate_structure,
)


@dataclass(frozen=True, slots=True)
class CellHandles:
    """Handles for the constructed NEURON cell.

    ``dendrites[i]`` corresponds to a non-soma compartment in the SWC; the matching entry in
    ``dendrite_xyz_um`` carries the (x, y, z, length_um) of that compartment in the morphology
    coordinate frame.
    """

    soma: Any
    axon_initial_segment: Any
    dendrites: list[Any] = field(default_factory=list)
    dendrite_xyz_um: list[tuple[float, float, float, float]] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class CellBuildSummary:
    n_dendrites: int
    total_dendritic_length_um: float
    soma_diameter_um: float
    soma_length_um: float


def _euclid_distance(a: SwcCompartment, b: SwcCompartment) -> float:
    dx: float = a.x - b.x
    dy: float = a.y - b.y
    dz: float = a.z - b.z
    return (dx * dx + dy * dy + dz * dz) ** 0.5


def build_dsgc_from_swc(*, swc_path: Path) -> CellHandles:
    """Build a NEURON cell from a calibrated SWC.

    Returns a :class:`CellHandles` carrying the soma section, the synthetic axon initial segment,
    the per-compartment dendrite section list, and the matching (x, y, z, length_um) coordinates.
    """
    from neuron import h  # noqa: PLC0415

    compartments: list[SwcCompartment] = parse_swc_file(swc_path=swc_path)
    validate_structure(compartments=compartments)

    by_id: dict[int, SwcCompartment] = {c.compartment_id: c for c in compartments}
    soma_compartments: list[SwcCompartment] = [
        c for c in compartments if c.type_code == SWC_TYPE_SOMA
    ]
    dendrite_compartments: list[SwcCompartment] = [
        c for c in compartments if c.type_code != SWC_TYPE_SOMA
    ]

    # ----------------------------------------------------------------
    # Soma: collapse the 19 SWC soma rows into one cylindrical section.
    # Length = sum of segment-to-segment Euclidean distances; diameter = 2 x mean radius.
    # ----------------------------------------------------------------
    soma_length_um: float = 0.0
    for compartment in soma_compartments:
        if compartment.parent_id == -1:
            continue
        parent = by_id[compartment.parent_id]
        if parent.type_code != SWC_TYPE_SOMA:
            continue
        soma_length_um += _euclid_distance(a=compartment, b=parent)
    if soma_length_um == 0.0:
        soma_length_um = 1.0
    mean_radius_um: float = sum(c.radius for c in soma_compartments) / float(len(soma_compartments))
    soma_diameter_um: float = 2.0 * mean_radius_um

    soma: Any = h.Section(name="soma")
    soma.L = soma_length_um
    soma.diam = soma_diameter_um
    soma.Ra = RA_OHM_CM
    soma.cm = CM_UF_PER_CM2
    soma.insert("hh")

    # ----------------------------------------------------------------
    # Axon initial segment (synthetic; SWC has no axon).
    # Connect to the soma's distal end (1.0).
    # ----------------------------------------------------------------
    ais: Any = h.Section(name="axon_initial_segment")
    ais.L = AIS_LENGTH_UM
    ais.diam = AIS_DIAMETER_UM
    ais.Ra = RA_OHM_CM
    ais.cm = CM_UF_PER_CM2
    ais.insert("hh")
    # Boost AIS gNa / lower gK so the synaptic depolarisation can trigger an action potential.
    # See the AIS comment block in code/constants.py for the rationale.
    ais.gnabar_hh = AIS_GNABAR_S_PER_CM2
    ais.gkbar_hh = AIS_GKBAR_S_PER_CM2
    ais.gl_hh = AIS_GL_S_PER_CM2
    ais.el_hh = AIS_EL_HH_MV
    ais.connect(soma(1.0), 0.0)

    # ----------------------------------------------------------------
    # Dendrites: one h.Section per non-soma compartment.
    # Use pt3dadd of (parent_xyz_radius) -> (this_xyz_radius) to give the section a length
    # equal to the parent->child Euclidean distance and the correct local diameter.
    # Connect each section to its parent at parent(1.0); soma rows act as a single proximal
    # connection point (we use soma(0.5) for any dendrite whose SWC parent is a soma row).
    # ----------------------------------------------------------------
    dendrites: list[Any] = []
    dendrite_xyz_um: list[tuple[float, float, float, float]] = []
    section_by_swc_id: dict[int, Any] = {}
    for swc_id in (c.compartment_id for c in soma_compartments):
        section_by_swc_id[swc_id] = soma

    soma_origin: SwcCompartment = soma_compartments[0]

    for index, compartment in enumerate(dendrite_compartments):
        sec: Any = h.Section(name=f"dend[{index}]")
        sec.Ra = RA_OHM_CM
        sec.cm = CM_UF_PER_CM2
        sec.insert("pas")

        parent: SwcCompartment = by_id[compartment.parent_id]
        # Choose a usable 3D parent point: if the SWC parent is a soma row we anchor the segment
        # at the soma origin so the geometry is correct relative to the collapsed soma.
        parent_xyz: tuple[float, float, float, float] = (
            (soma_origin.x, soma_origin.y, soma_origin.z, parent.radius)
            if parent.type_code == SWC_TYPE_SOMA
            else (parent.x, parent.y, parent.z, parent.radius)
        )
        h.pt3dclear(sec=sec)
        h.pt3dadd(parent_xyz[0], parent_xyz[1], parent_xyz[2], 2.0 * parent_xyz[3], sec=sec)
        h.pt3dadd(
            compartment.x,
            compartment.y,
            compartment.z,
            2.0 * compartment.radius,
            sec=sec,
        )

        # Connect to parent's distal end (1.0) â€” for soma parent this yields soma(1.0); we re-bind
        # to soma(0.5) for parent-is-soma so the dendrite emerges from the somatic centre.
        if parent.type_code == SWC_TYPE_SOMA:
            sec.connect(soma(0.5), 0.0)
        else:
            parent_section: Any = section_by_swc_id[compartment.parent_id]
            sec.connect(parent_section(1.0), 0.0)

        # Passive parameters (g_pas = 1/Rm in S/cm^2 -> NEURON expects g_pas in S/cm^2).
        for seg in sec:
            seg.pas.g = 1.0 / RM_OHM_CM2
            seg.pas.e = V_INIT_MV

        section_by_swc_id[compartment.compartment_id] = sec

        # Record midpoint in microns (compartment xyz) and segment length.
        dx: float = compartment.x - parent_xyz[0]
        dy: float = compartment.y - parent_xyz[1]
        dz: float = compartment.z - parent_xyz[2]
        length_um: float = (dx * dx + dy * dy + dz * dz) ** 0.5
        mid_x: float = 0.5 * (parent_xyz[0] + compartment.x)
        mid_y: float = 0.5 * (parent_xyz[1] + compartment.y)
        mid_z: float = 0.5 * (parent_xyz[2] + compartment.z)
        dendrite_xyz_um.append((mid_x, mid_y, mid_z, length_um))
        dendrites.append(sec)

    return CellHandles(
        soma=soma,
        axon_initial_segment=ais,
        dendrites=dendrites,
        dendrite_xyz_um=dendrite_xyz_um,
    )


def summarize_cell(*, cell: CellHandles) -> CellBuildSummary:
    """Return a short structural summary of the constructed cell."""
    total_length: float = sum(entry[3] for entry in cell.dendrite_xyz_um)
    soma: Any = cell.soma
    return CellBuildSummary(
        n_dendrites=len(cell.dendrites),
        total_dendritic_length_um=total_length,
        soma_diameter_um=float(soma.diam),
        soma_length_um=float(soma.L),
    )
