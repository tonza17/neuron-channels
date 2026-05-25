"""Cytoplasm-volume computation for the t0122 NSGA-II objective.

Per the t0122 task description (Cuntz 2010 wiring-cost interpretation of
the Cajal cytoplasm-conservation principle), the per-cell cytoplasm
volume is the geometric sum over soma, all dendrites, and AIS sections
of ``pi * (sec.diam / 2.0)**2 * sec.L``. Units: um^3.

This is a pure geometric quantity computable from the live ``h.Section``
handles on ``MorphologyResult`` -- no NEURON simulation step is required.
The t0092 ``_patch_soma_geometry`` patch (which sets the soma length to
``params.soma_diameter_um`` and the soma diameter to
``BEDB_AREA_TARGET_UM2 / (pi * soma_diameter_um)``) is already in place
on every cell built by ``generate_fixed_morphology``, so the volume
formula is correct against the patched geometry.

Used by:

* ``evaluator.evaluate_68d_vector`` -- computes per-cell volume after
  ``_ensure_worker_cell`` builds the cell.
* ``evaluator.BedBV3MorphProblem._evaluate`` -- emits the volume in the
  positive direction (``out["F"] = [-dsi, +volume_um3]``) because
  volume is minimised directly, NOT negated.
* ``build_pareto_plots.py`` -- recomputes per-section breakdown for the
  top-N cells.
* ``build_predictions_assets.py`` -- writes ``cytoplasm_volume_um3`` to
  every per-cell row.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyResult,
)


@dataclass(frozen=True, slots=True)
class VolumeBreakdown:
    """Per-compartment cytoplasm volume in um^3."""

    soma_um3: float
    dendrites_um3: float
    ais_um3: float

    @property
    def total_um3(self) -> float:
        return self.soma_um3 + self.dendrites_um3 + self.ais_um3


def _section_volume_um3(*, length_um: float, diameter_um: float) -> float:
    """Cylinder volume in um^3 from length and diameter in um."""
    radius_um = diameter_um / 2.0
    return math.pi * radius_um * radius_um * length_um


def compute_cytoplasm_volume_um3(*, cell: MorphologyResult) -> float:
    """Sum the cytoplasm volume over soma + all dendrites + AIS sections.

    Returns total cell cytoplasm volume in um^3 as ``sum(pi * (sec.diam /
    2.0)**2 * sec.L for sec in [soma, *all_dends, ais_proximal,
    ais_distal])``.
    """
    sections = [cell.soma, *cell.all_dends, cell.ais_proximal, cell.ais_distal]
    total: float = 0.0
    for sec in sections:
        total += _section_volume_um3(length_um=float(sec.L), diameter_um=float(sec.diam))
    return total


def compute_per_section_volume_breakdown(*, cell: MorphologyResult) -> VolumeBreakdown:
    """Per-compartment breakdown of cytoplasm volume in um^3."""
    soma_um3 = _section_volume_um3(
        length_um=float(cell.soma.L),
        diameter_um=float(cell.soma.diam),
    )
    dendrites_um3 = 0.0
    for sec in cell.all_dends:
        dendrites_um3 += _section_volume_um3(
            length_um=float(sec.L),
            diameter_um=float(sec.diam),
        )
    ais_um3 = 0.0
    for sec in (cell.ais_proximal, cell.ais_distal):
        ais_um3 += _section_volume_um3(
            length_um=float(sec.L),
            diameter_um=float(sec.diam),
        )
    return VolumeBreakdown(
        soma_um3=soma_um3,
        dendrites_um3=dendrites_um3,
        ais_um3=ais_um3,
    )


__all__ = [
    "VolumeBreakdown",
    "compute_cytoplasm_volume_um3",
    "compute_per_section_volume_breakdown",
]
