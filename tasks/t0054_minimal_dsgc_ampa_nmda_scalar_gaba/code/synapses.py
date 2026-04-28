"""Co-located E + I synapse pairs with position-gated event scheduling and scalar gabaMOD.

Adapted from ``tasks/t0052_minimal_dsgc_scalar_gaba/code/synapses.py`` (the ``EiPair``,
``build_ei_pairs``, ``schedule_ei_onsets`` machinery) and extended with a co-located NMDA
``Exp2Syn`` driven by a SECOND ``NetCon`` attached to the SAME shared ``NetStim`` per pair.

NMDA mechanism: voltage-independent ``Exp2Syn`` with ``tau1 = NMDA_TAU1_MS = 5 ms``,
``tau2 = NMDA_TAU2_MS = 80 ms``, ``e = NMDA_E_MV = 0 mV``. No Mg block, no ``n`` exponent —
``i = g * (v - e)``. Built on the same ``seg`` as the AMPA ``Exp2Syn`` (co-located), so the
two share both the spatial location and the ``NetStim`` event source.

Per the t0054 plan: ``NetStim.number = 1``, no E-I offset, no PD/ND branching — every pair
shares the same scalar ``gaba_mod_theta`` weight, and AMPA + NMDA share the same scheduled
event start time.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.constants import (
    AMPA_E_MV,
    AMPA_PEAK_NS,
    AMPA_TAU1_MS,
    AMPA_TAU2_MS,
    BASE_OFFSET_MS,
    GABA_BASE_NS,
    GABA_E_MV,
    GABA_TAU1_MS,
    GABA_TAU2_MS,
    NMDA_E_MV,
    NMDA_TAU1_MS,
    NMDA_TAU2_MS,
    THETA_ND_DEG,
)
from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.placement import Location


@dataclass(frozen=True, slots=True)
class EiPair:
    """One co-located AMPA + NMDA + GABA synapse triplet, with NetStim drivers and NetCons.

    The ``ampa_netcon`` / ``nmda_netcon`` / ``gaba_netcon`` ``weight[0]`` carry the per-event
    conductance in microsiemens. The base AMPA weight is fixed at ``AMPA_PEAK_NS * 1e-3``
    (i.e., 0.5 nS = 0.0005 uS); the base NMDA weight is per-trial scaled by ``gnmda_ns * 1e-3``
    (the gNMDA outer sweep parameter); the base GABA weight is per-trial scaled by
    ``gaba_mod_theta`` (see :func:`schedule_ei_onsets`).

    AMPA and NMDA share a single ``ampa_netstim`` ``NetStim`` instance — there is no separate
    NMDA NetStim. This guarantees AMPA and NMDA fire at byte-identical times.
    """

    pair_index: int
    section_index: int
    section_x: float
    x_um: float
    y_um: float
    ampa_syn: Any
    nmda_syn: Any
    gaba_syn: Any
    ampa_netstim: Any
    gaba_netstim: Any
    ampa_netcon: Any
    nmda_netcon: Any
    gaba_netcon: Any


def gaba_mod(*, theta_deg: float, theta_pd_deg: float = 0.0) -> float:
    """Return the scalar gabaMOD multiplier for bar direction ``theta_deg``.

    Defined so that ``gaba_mod(theta_pd) == 0.33`` (preferred direction; weak inhibition) and
    ``gaba_mod(theta_pd + 180) == 0.99`` (null direction; strong inhibition):

        ``gaba_mod(theta) = 0.33 + 0.66 * (1 - cos(theta - theta_pd)) / 2``

    NOTE: The plan text labels the subtracted angle ``theta_ND``, but with ``theta_ND = 180`` the
    formula evaluates to 0.99 at ``theta = 0`` and 0.33 at ``theta = 180`` — the opposite of REQ-7
    ("PD weight = 0.33 x base, ND weight = 0.99 x base"). The endpoint values in REQ-7 and the
    sanity-check ratio ``gNULL/gPD ~= 3`` are the canonical specification, so the formula here
    uses ``theta - theta_pd`` (with the default PD = 0 deg).

    The unused ``THETA_ND_DEG`` constant (= 180.0 deg) is preserved as documentation only; it is
    not used in the formula because PD is the canonical reference angle.
    """
    _ = THETA_ND_DEG  # documentation marker; not used in the formula.
    delta_rad: float = math.radians(theta_deg - theta_pd_deg)
    return 0.33 + 0.66 * (1.0 - math.cos(delta_rad)) / 2.0


def build_ei_pairs(
    *,
    h: Any,
    locations: list[Location],
    sections: list[Any],
) -> list[EiPair]:
    """Construct one AMPA + NMDA + GABA Exp2Syn triplet per ``Location``.

    Each E location hosts a co-located AMPA and NMDA ``Exp2Syn`` on the SAME ``seg``; both are
    driven by the same single-event ``NetStim`` (``ampa_netstim``) via two separate ``NetCon``
    instances. The GABA ``Exp2Syn`` shares the same segment but has its own ``NetStim`` (for
    consistency with t0052; the t0054 spec only requires AMPA and NMDA to share, not GABA).

    The NMDA NetCon's ``weight[0]`` is left at 0.0 here; per-trial values (``gnmda_ns * 1e-3``)
    are written by :func:`schedule_ei_onsets`. Setting ``gnmda_ns = 0.0`` yields a wired-but-inert
    NMDA mechanism, which is exactly the design needed to satisfy the gNMDA = 0 regression gate.
    """
    pairs: list[EiPair] = []
    for pair_index, location in enumerate(locations):
        sec: Any = sections[location.section_index]
        seg = sec(location.section_x)

        ampa_syn: Any = h.Exp2Syn(seg)
        ampa_syn.tau1 = AMPA_TAU1_MS
        ampa_syn.tau2 = AMPA_TAU2_MS
        ampa_syn.e = AMPA_E_MV

        nmda_syn: Any = h.Exp2Syn(seg)
        nmda_syn.tau1 = NMDA_TAU1_MS
        nmda_syn.tau2 = NMDA_TAU2_MS
        nmda_syn.e = NMDA_E_MV

        gaba_syn: Any = h.Exp2Syn(seg)
        gaba_syn.tau1 = GABA_TAU1_MS
        gaba_syn.tau2 = GABA_TAU2_MS
        gaba_syn.e = GABA_E_MV

        ampa_netstim: Any = h.NetStim()
        ampa_netstim.number = 1
        ampa_netstim.noise = 0.0
        ampa_netstim.interval = 1.0  # required by NEURON even for single events
        ampa_netstim.start = 0.0

        gaba_netstim: Any = h.NetStim()
        gaba_netstim.number = 1
        gaba_netstim.noise = 0.0
        gaba_netstim.interval = 1.0
        gaba_netstim.start = 0.0

        ampa_netcon: Any = h.NetCon(ampa_netstim, ampa_syn)
        ampa_netcon.delay = 0.0
        ampa_netcon.weight[0] = AMPA_PEAK_NS * 1e-3  # nS -> uS

        # Second NetCon attached to the SAME ampa_netstim. No second NetStim per the t0054 spec.
        nmda_netcon: Any = h.NetCon(ampa_netstim, nmda_syn)
        nmda_netcon.delay = 0.0
        nmda_netcon.weight[0] = 0.0  # set per-trial in schedule_ei_onsets

        gaba_netcon: Any = h.NetCon(gaba_netstim, gaba_syn)
        gaba_netcon.delay = 0.0
        gaba_netcon.weight[0] = GABA_BASE_NS * 1e-3  # nS -> uS, scaled per trial

        pairs.append(
            EiPair(
                pair_index=pair_index,
                section_index=location.section_index,
                section_x=location.section_x,
                x_um=location.x_um,
                y_um=location.y_um,
                ampa_syn=ampa_syn,
                nmda_syn=nmda_syn,
                gaba_syn=gaba_syn,
                ampa_netstim=ampa_netstim,
                gaba_netstim=gaba_netstim,
                ampa_netcon=ampa_netcon,
                nmda_netcon=nmda_netcon,
                gaba_netcon=gaba_netcon,
            ),
        )
    return pairs


def _onset_time_ms(
    *,
    pair: EiPair,
    angle_deg: float,
    velocity_um_per_ms: float,
) -> float:
    """Return ``t_bar = (x cos theta + y sin theta) / velocity + base_offset``."""
    theta_rad: float = math.radians(angle_deg)
    raw_t: float = (
        pair.x_um * math.cos(theta_rad) + pair.y_um * math.sin(theta_rad)
    ) / velocity_um_per_ms
    return max(raw_t, 0.0) + BASE_OFFSET_MS


def schedule_ei_onsets(
    *,
    pairs: list[EiPair],
    angle_deg: float,
    velocity_um_per_ms: float,
    gaba_mod_theta: float,
    gnmda_ns: float,
) -> list[float]:
    """Set per-pair NetStim.start times and refresh NetCon weights for this trial.

    Returns the list of per-pair onset times in ms (in order) so the caller can persist them
    for the activation-time histogram.

    The ``gnmda_ns`` parameter is the per-trial peak NMDA conductance in nS; it is converted to
    microsiemens and written to every ``nmda_netcon.weight[0]``. Setting ``gnmda_ns = 0.0``
    leaves the NMDA mechanism wired but inert (zero current at any voltage).
    """
    onset_times_ms: list[float] = []
    ampa_weight_us: float = AMPA_PEAK_NS * 1e-3
    nmda_weight_us: float = gnmda_ns * 1e-3
    gaba_weight_us: float = GABA_BASE_NS * gaba_mod_theta * 1e-3
    for pair in pairs:
        onset_ms: float = _onset_time_ms(
            pair=pair,
            angle_deg=angle_deg,
            velocity_um_per_ms=velocity_um_per_ms,
        )
        # AMPA NetStim drives both AMPA and NMDA NetCons (same start time).
        pair.ampa_netstim.start = onset_ms
        pair.gaba_netstim.start = onset_ms
        pair.ampa_netcon.weight[0] = ampa_weight_us
        pair.nmda_netcon.weight[0] = nmda_weight_us
        pair.gaba_netcon.weight[0] = gaba_weight_us
        onset_times_ms.append(onset_ms)
    return onset_times_ms
