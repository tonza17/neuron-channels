"""Co-located E + I synapse pairs with position-gated event scheduling and scalar gabaMOD.

Adapted from ``tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/synapses.py``. Single change
vs t0054: the NMDA point process is now ``h.NMDA_MgBlock`` (custom POINT_PROCESS) instead of
``h.Exp2Syn`` (built-in voltage-independent). Same dual-exponential gating kinetics
(``tau1 = 5 ms``, ``tau2 = 80 ms``, ``e = 0 mV``) but multiplied by the Jahr-Stevens Boltzmann
Mg-block factor at every BREAKPOINT step:

    g_NMDA(v, t) = (B(t) - A(t)) / (1 + n * exp(-gama * local_v))

where ``local_v = v * (1 - Voff) + Vset * Voff``. With ``Voff = 0`` (default) the gating is
voltage-dependent (Mg block on); with ``Voff = 1`` ``local_v`` clamps to ``Vset = -60 mV``
(voltage-independent regime, kept available for future ablation but NOT exercised here).

AMPA mechanism is unchanged: ``h.Exp2Syn`` with ``tau1 = 0.5 ms``, ``tau2 = 2.5 ms``, ``e = 0 mV``,
peak ``0.5 nS``, driven by the same single ``ampa_netstim`` ``NetStim`` per pair via two separate
``NetCon`` instances (the second NetCon drives NMDA). This guarantees AMPA and NMDA fire at
byte-identical times — the property that makes the gNMDA = 0 regression bit-identical to t0054.

Per-trial NMDA NetCon weight (``gnmda_ns * 1e-3`` in microsiemens) is unchanged: with ``gnmda_ns
= 0`` the Mg-block factor multiplies a zero conductance, yielding exactly zero NMDA current at
any voltage.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from tasks.t0055_nmda_mg_block_dsi_recovery.code.constants import (
    AMPA_E_MV,
    AMPA_PEAK_NS,
    AMPA_TAU1_MS,
    AMPA_TAU2_MS,
    BASE_OFFSET_MS,
    GABA_BASE_NS,
    GABA_E_MV,
    GABA_TAU1_MS,
    GABA_TAU2_MS,
    MG_BLOCK_GAMMA,
    MG_BLOCK_N,
    MG_BLOCK_VOFF,
    MG_BLOCK_VSET_MV,
    NMDA_E_MV,
    NMDA_TAU1_MS,
    NMDA_TAU2_MS,
    THETA_ND_DEG,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.placement import Location


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

    The NMDA mechanism is now a custom ``h.NMDA_MgBlock`` POINT_PROCESS (see
    ``code/mod/NMDA_MgBlock.mod``) with the Jahr-Stevens Boltzmann Mg block. The dual-exponential
    gating + NetCon event handling is identical to ``Exp2Syn`` so the NetCon wiring below is
    unchanged from t0054.
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
    """Construct one AMPA + NMDA_MgBlock + GABA synapse triplet per ``Location``.

    Each E location hosts a co-located AMPA ``Exp2Syn`` and ``NMDA_MgBlock`` on the SAME ``seg``;
    both are driven by the same single-event ``NetStim`` (``ampa_netstim``) via two separate
    ``NetCon`` instances. The GABA ``Exp2Syn`` shares the same segment but has its own
    ``NetStim`` (for consistency with t0054).

    The NMDA NetCon's ``weight[0]`` is left at 0.0 here; per-trial values (``gnmda_ns * 1e-3``)
    are written by :func:`schedule_ei_onsets`. Setting ``gnmda_ns = 0.0`` yields a wired-but-inert
    NMDA mechanism, which is exactly the design needed to satisfy the gNMDA = 0 regression gate.

    Pre-condition: ``h.NMDA_MgBlock`` must be registered (call
    ``neuron_bootstrap.ensure_nmda_mg_block_compiled()`` before invoking this function).
    """
    pairs: list[EiPair] = []
    for pair_index, location in enumerate(locations):
        sec: Any = sections[location.section_index]
        seg = sec(location.section_x)

        ampa_syn: Any = h.Exp2Syn(seg)
        ampa_syn.tau1 = AMPA_TAU1_MS
        ampa_syn.tau2 = AMPA_TAU2_MS
        ampa_syn.e = AMPA_E_MV

        nmda_syn: Any = h.NMDA_MgBlock(seg)
        nmda_syn.tau1 = NMDA_TAU1_MS
        nmda_syn.tau2 = NMDA_TAU2_MS
        nmda_syn.e = NMDA_E_MV
        nmda_syn.n = MG_BLOCK_N
        nmda_syn.gama = MG_BLOCK_GAMMA
        nmda_syn.Voff = MG_BLOCK_VOFF
        nmda_syn.Vset = MG_BLOCK_VSET_MV

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
