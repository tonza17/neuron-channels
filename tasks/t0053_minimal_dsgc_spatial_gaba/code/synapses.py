"""Co-located E + I synapse pairs with position-gated event scheduling and spatial GABA gating.

Rewritten from t0052's ``synapses.py`` to implement the t0053 spatial centripetal-gating rule:
each I synapse fires only when the moving stimulus has a centripetal component, i.e.
``cos(radians(theta_stim - theta_centrifugal_i)) < 0``, where
``theta_centrifugal_i = atan2(y_i - y_soma, x_i - x_soma)`` is the synapse-to-soma centrifugal
direction (computed once at pair-construction time). When the gate fires, the I synapse delivers
the full GABA_BASE_NS = 2.0 nS amplitude. When the gate is silent, the synapse weight is set to
zero and the NetStim.start is pushed past TSTOP_MS as defence-in-depth.

E synapses fire once per trial regardless of direction (one event per pair when the bar's leading
edge crosses the synapse position).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from tasks.t0053_minimal_dsgc_spatial_gaba.code.constants import (
    AMPA_E_MV,
    AMPA_PEAK_NS,
    AMPA_TAU1_MS,
    AMPA_TAU2_MS,
    BASE_OFFSET_MS,
    GABA_BASE_NS,
    GABA_E_MV,
    GABA_TAU1_MS,
    GABA_TAU2_MS,
    TSTOP_MS,
)
from tasks.t0053_minimal_dsgc_spatial_gaba.code.placement import Location


@dataclass(frozen=True, slots=True)
class EiPair:
    """One co-located AMPA + GABA synapse pair, with NetStim drivers and NetCon weights.

    The ``ampa_netcon`` and ``gaba_netcon`` fields' ``weight[0]`` carry the unit conductance in
    microsiemens. AMPA is fixed at ``AMPA_PEAK_NS * 1e-3`` (i.e., 0.5 nS = 0.0005 uS); GABA is
    either ``GABA_BASE_NS * 1e-3`` (full 2 nS, when the spatial gate fires) or 0.0 (silent).

    ``theta_centrifugal_rad`` is the polar angle of the synapse position relative to the soma
    origin in the morphology xy-plane: ``atan2(y_um - y_soma, x_um - x_soma)``. It is set once at
    construction time and reused per trial.
    """

    pair_index: int
    section_index: int
    section_x: float
    x_um: float
    y_um: float
    theta_centrifugal_rad: float
    ampa_syn: Any
    gaba_syn: Any
    ampa_netstim: Any
    gaba_netstim: Any
    ampa_netcon: Any
    gaba_netcon: Any


@dataclass(frozen=True, slots=True)
class ScheduleResult:
    """Result of one ``schedule_ei_onsets`` call.

    ``onset_times_ms[i]`` is the bar-arrival time in ms for pair ``i`` (with the BASE_OFFSET_MS
    added). ``i_fired_mask[i]`` is True iff the spatial centripetal-gating rule fired pair ``i``'s
    GABA synapse for this stimulus direction; when False, the I synapse's NetCon weight is zero.
    """

    onset_times_ms: list[float]
    i_fired_mask: list[bool]


def i_synapse_fires(
    *,
    theta_stim_deg: float,
    theta_centrifugal_deg: float,
) -> bool:
    """Return True iff the I synapse fires under the centripetal-gating rule.

    The rule is:

        ``cos(radians(theta_stim - theta_centrifugal)) < 0``

    i.e. the bar direction has a centripetal projection onto the synapse's centrifugal axis.
    Strict inequality: at exactly perpendicular (cos == 0) the synapse does NOT fire.
    """
    delta_rad: float = math.radians(theta_stim_deg - theta_centrifugal_deg)
    return math.cos(delta_rad) < 0.0


def build_ei_pairs(
    *,
    h: Any,
    locations: list[Location],
    sections: list[Any],
    soma_origin_um: tuple[float, float, float],
) -> list[EiPair]:
    """Construct one AMPA + GABA Exp2Syn pair per ``Location`` from a pre-sampled placement list.

    Each pair's ``theta_centrifugal_rad`` is precomputed from its (x_um, y_um) and the soma
    origin's (x_soma, y_soma) using ``atan2(y - y_soma, x - x_soma)``. Each synapse is driven by
    its own ``h.NetStim(number=1, noise=0)`` via an ``h.NetCon`` whose ``weight[0]`` carries the
    per-event conductance in microsiemens.
    """
    soma_x_um: float = soma_origin_um[0]
    soma_y_um: float = soma_origin_um[1]

    pairs: list[EiPair] = []
    for pair_index, location in enumerate(locations):
        sec: Any = sections[location.section_index]
        seg = sec(location.section_x)

        ampa_syn: Any = h.Exp2Syn(seg)
        ampa_syn.tau1 = AMPA_TAU1_MS
        ampa_syn.tau2 = AMPA_TAU2_MS
        ampa_syn.e = AMPA_E_MV

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

        gaba_netcon: Any = h.NetCon(gaba_netstim, gaba_syn)
        gaba_netcon.delay = 0.0
        gaba_netcon.weight[0] = 0.0  # set per trial by schedule_ei_onsets

        theta_centrifugal_rad: float = math.atan2(
            location.y_um - soma_y_um,
            location.x_um - soma_x_um,
        )

        pairs.append(
            EiPair(
                pair_index=pair_index,
                section_index=location.section_index,
                section_x=location.section_x,
                x_um=location.x_um,
                y_um=location.y_um,
                theta_centrifugal_rad=theta_centrifugal_rad,
                ampa_syn=ampa_syn,
                gaba_syn=gaba_syn,
                ampa_netstim=ampa_netstim,
                gaba_netstim=gaba_netstim,
                ampa_netcon=ampa_netcon,
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
) -> ScheduleResult:
    """Set per-pair NetStim.start times and per-pair GABA weights for this trial.

    For each pair: AMPA always fires at the bar-arrival time at the synapse's projected position
    on the bar's normal. GABA fires only when the spatial centripetal-gating rule
    ``cos(radians(angle_deg - degrees(theta_centrifugal_rad))) < 0`` is True. When fired, the
    GABA NetCon weight is ``GABA_BASE_NS * 1e-3`` (full 2 nS); when silent, the weight is 0 and
    the NetStim.start is pushed past TSTOP_MS as defence-in-depth.

    Returns a :class:`ScheduleResult` carrying the per-pair onset times and the per-pair fire mask.
    """
    onset_times_ms: list[float] = []
    i_fired_mask: list[bool] = []
    ampa_weight_us: float = AMPA_PEAK_NS * 1e-3
    gaba_full_weight_us: float = GABA_BASE_NS * 1e-3
    for pair in pairs:
        onset_ms: float = _onset_time_ms(
            pair=pair,
            angle_deg=angle_deg,
            velocity_um_per_ms=velocity_um_per_ms,
        )
        pair.ampa_netstim.start = onset_ms
        pair.ampa_netcon.weight[0] = ampa_weight_us

        fires: bool = i_synapse_fires(
            theta_stim_deg=angle_deg,
            theta_centrifugal_deg=math.degrees(pair.theta_centrifugal_rad),
        )
        if fires:
            pair.gaba_netstim.start = onset_ms
            pair.gaba_netcon.weight[0] = gaba_full_weight_us
        else:
            pair.gaba_netstim.start = TSTOP_MS + 1.0
            pair.gaba_netcon.weight[0] = 0.0

        onset_times_ms.append(onset_ms)
        i_fired_mask.append(fires)
    return ScheduleResult(
        onset_times_ms=onset_times_ms,
        i_fired_mask=i_fired_mask,
    )
