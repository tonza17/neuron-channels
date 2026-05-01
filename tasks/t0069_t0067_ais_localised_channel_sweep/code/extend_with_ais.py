"""Extend the t0008 deposited cell with a virtual AIS + axon cable.

The deposited Poleg-Polsky cell (built via ``t0008.code.build_cell.build_dsgc``) has a soma
and dendrites but no axon initial segment. This module adds a 30 um AIS section + 1 mm
passive axon cable to the cell after construction. The new sections carry their own HHst
mechanism at biologically-realistic AIS / axon densities (per t0019 priors).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tasks.t0069_t0067_ais_localised_channel_sweep.code.constants import (
    AIS_DIAM_UM,
    AIS_GKBAR_S_CM2,
    AIS_GKMBAR_S_CM2,
    AIS_GNABAR_S_CM2,
    AIS_LENGTH_UM,
    AIS_NSEG,
    AXON_DIAM_UM,
    AXON_GKBAR_S_CM2,
    AXON_GKMBAR_S_CM2,
    AXON_GNABAR_S_CM2,
    AXON_LENGTH_UM,
    AXON_NSEG,
    PASSIVE_CM_UF_CM2,
    PASSIVE_ELEAK_MV,
    PASSIVE_GLEAK_S_CM2,
    PASSIVE_RA_OHM_CM,
)


@dataclass(frozen=True, slots=True)
class AISExtension:
    """AIS + axon sections appended to the deposited cell."""

    ais: Any
    axon: Any


def extend_with_ais(*, h: Any, soma: Any) -> AISExtension:
    """Create AIS + axon sections, attach to ``soma(1)``, insert HHst at AIS densities."""
    ais = h.Section(name="ais_t69")
    ais.L = float(AIS_LENGTH_UM)
    ais.diam = float(AIS_DIAM_UM)
    ais.nseg = int(AIS_NSEG)
    ais.Ra = float(PASSIVE_RA_OHM_CM)
    ais.cm = float(PASSIVE_CM_UF_CM2)
    ais.insert("HHst")
    for seg in ais:
        seg.HHst.gnabar = float(AIS_GNABAR_S_CM2)
        seg.HHst.gkbar = float(AIS_GKBAR_S_CM2)
        seg.HHst.gkmbar = float(AIS_GKMBAR_S_CM2)
        seg.HHst.gleak = float(PASSIVE_GLEAK_S_CM2)
        seg.HHst.eleak = float(PASSIVE_ELEAK_MV)
    ais.connect(soma, 1.0, 0.0)

    axon = h.Section(name="axon_t69")
    axon.L = float(AXON_LENGTH_UM)
    axon.diam = float(AXON_DIAM_UM)
    axon.nseg = int(AXON_NSEG)
    axon.Ra = float(PASSIVE_RA_OHM_CM)
    axon.cm = float(PASSIVE_CM_UF_CM2)
    axon.insert("HHst")
    for seg in axon:
        seg.HHst.gnabar = float(AXON_GNABAR_S_CM2)
        seg.HHst.gkbar = float(AXON_GKBAR_S_CM2)
        seg.HHst.gkmbar = float(AXON_GKMBAR_S_CM2)
        seg.HHst.gleak = float(PASSIVE_GLEAK_S_CM2)
        seg.HHst.eleak = float(PASSIVE_ELEAK_MV)
    axon.connect(ais, 1.0, 0.0)

    return AISExtension(ais=ais, axon=axon)
