"""Attach a two-subsegment AIS to the de Rosenroll 2026 Bed B cell.

Forked from ``tasks/t0069_t0067_ais_localised_channel_sweep/code/extend_with_ais.py``.
The single AIS section in t0069 is split here into two ``h.Section`` objects:

* ``ais_proximal_t80`` — proximal half-segment carrying HHst (basal Na+K stand-in
  for Nav1.1/Nav1.2; researcher decision: do NOT vendor a separate Nav1.2 MOD).
* ``ais_distal_t80`` — distal half-segment carrying HHst, ``nav16t80`` (Nav1.6),
  ``kv3t80``, ``kv7t80``. NaP, BK, SK, slow-AHP are explicitly EXCLUDED from
  both AIS subsegments per task description.

Topology: ``ais_proximal.connect(soma, 1.0, 0.0)`` then
``ais_distal.connect(ais_proximal, 1.0, 0.0)``.

Segment count uses NEURON's d_lambda rule:
``nseg = int((sec.L / (d_lambda * lambda_f(100, sec=sec))) / 2) * 2 + 1``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from tasks.t0113_t0106_seed2247_replicate.code.constants_electrophys import (
    AIS_D_LAMBDA,
    AIS_DEFAULT_DIAMETER_UM,
    AIS_DEFAULT_LENGTH_UM,
    AIS_LAMBDA_F_FREQ_HZ,
    AIS_PASSIVE_CM_UF_CM2,
    AIS_PASSIVE_ELEAK_MV,
    AIS_PASSIVE_GLEAK_S_CM2,
    AIS_PASSIVE_RA_OHM_CM,
    AIS_PROXIMAL_FRACTION,
)


@dataclass(slots=True)
class AISExtension:
    """Two-subsegment AIS sections appended to the deposited cell."""

    ais_proximal: Any
    ais_distal: Any


def _compute_nseg(*, h: Any, section: Any) -> int:
    """Compute nseg per d_lambda=0.1 rule at 100 Hz, rounded to nearest odd."""
    section.push()
    try:
        lam = float(h.lambda_f(AIS_LAMBDA_F_FREQ_HZ, sec=section))
    finally:
        h.pop_section()
    if lam <= 0.0 or math.isnan(lam):
        return 5
    raw = section.L / (AIS_D_LAMBDA * lam)
    return max(1, int(raw / 2.0) * 2 + 1)


def extend_with_ais(
    *,
    h: Any,
    soma: Any,
    total_length_um: float = AIS_DEFAULT_LENGTH_UM,
    diameter_um: float = AIS_DEFAULT_DIAMETER_UM,
) -> AISExtension:
    """Build proximal + distal AIS sections, attach to ``soma(1)``.

    HHst basal Na+K is inserted everywhere on the AIS (the proximal subsegment
    uses HHst as a Nav1.1/Nav1.2 stand-in per researcher decision). ``nav16t80``,
    ``kv3t80``, ``kv7t80`` are inserted on the DISTAL subsegment only. NaP, BK,
    SK, and slow-AHP are EXCLUDED from both subsegments.

    The actual conductance densities (per-segment ``gbar_*`` values) are written
    later by ``apply_parameter_vector``; this function only inserts the
    mechanisms and sets passive properties.
    """
    proximal_length = max(1.0, total_length_um * AIS_PROXIMAL_FRACTION)
    distal_length = max(1.0, total_length_um - proximal_length)

    ais_proximal = h.Section(name="ais_proximal_t80")
    ais_proximal.L = float(proximal_length)
    ais_proximal.diam = float(diameter_um)
    ais_proximal.Ra = float(AIS_PASSIVE_RA_OHM_CM)
    ais_proximal.cm = float(AIS_PASSIVE_CM_UF_CM2)
    ais_proximal.nseg = _compute_nseg(h=h, section=ais_proximal)
    # HHst gives basal Na+K (Nav1.1/Nav1.2 stand-in for the proximal subsegment).
    ais_proximal.insert("HHst")
    for seg in ais_proximal:
        seg.HHst.gleak = float(AIS_PASSIVE_GLEAK_S_CM2)
        seg.HHst.eleak = float(AIS_PASSIVE_ELEAK_MV)
    ais_proximal.connect(soma, 1.0, 0.0)

    ais_distal = h.Section(name="ais_distal_t80")
    ais_distal.L = float(distal_length)
    ais_distal.diam = float(diameter_um)
    ais_distal.Ra = float(AIS_PASSIVE_RA_OHM_CM)
    ais_distal.cm = float(AIS_PASSIVE_CM_UF_CM2)
    ais_distal.nseg = _compute_nseg(h=h, section=ais_distal)
    ais_distal.insert("HHst")
    for seg in ais_distal:
        seg.HHst.gleak = float(AIS_PASSIVE_GLEAK_S_CM2)
        seg.HHst.eleak = float(AIS_PASSIVE_ELEAK_MV)
    ais_distal.connect(ais_proximal, 1.0, 0.0)

    return AISExtension(ais_proximal=ais_proximal, ais_distal=ais_distal)


def update_ais_geometry(
    *,
    h: Any,
    extension: AISExtension,
    total_length_um: float,
    diameter_um: float,
) -> None:
    """Update AIS geometry on an existing extension before channel insertion.

    Called by ``apply_parameter_vector`` when the BO has sampled new AIS length
    and diameter values. Re-runs the d_lambda nseg rule on the updated geometry.
    """
    proximal_length = max(1.0, total_length_um * AIS_PROXIMAL_FRACTION)
    distal_length = max(1.0, total_length_um - proximal_length)
    extension.ais_proximal.L = float(proximal_length)
    extension.ais_proximal.diam = float(diameter_um)
    extension.ais_proximal.nseg = _compute_nseg(h=h, section=extension.ais_proximal)
    extension.ais_distal.L = float(distal_length)
    extension.ais_distal.diam = float(diameter_um)
    extension.ais_distal.nseg = _compute_nseg(h=h, section=extension.ais_distal)
