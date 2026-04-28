"""Co-located E + I synapse pairs with the new tonic GABA mechanism.

Adapted from ``tasks/t0053_minimal_dsgc_spatial_gaba/code/synapses.py``. Differences from t0053:

* The GABA branch's ``h.Exp2Syn`` + ``h.NetStim`` + ``h.NetCon`` triplet is replaced by a single
  ``h.gaba_tonic(seg)`` POINT_PROCESS instance per pair (see ``code/mod/GabaTonic.mod``).
* ``EiPair`` no longer carries ``gaba_netstim`` / ``gaba_netcon`` fields.
* ``schedule_ei_onsets`` accepts a ``gaba_base_ns`` parameter (the swept value); for "fired"
  synapses it writes ``pair.gaba_syn.g = gaba_base_ns * 1e-3``, ``pair.gaba_syn.t_on = T_ON_MS``,
  ``pair.gaba_syn.t_off = T_OFF_MS``; for silent synapses it writes ``g = 0``,
  ``t_on = 0``, ``t_off = 0``. The spatial centripetal-gating predicate ``i_synapse_fires`` is
  carried over bit-for-bit from t0053.

The AMPA path (Exp2Syn + NetStim + NetCon) is unchanged and bit-identical to t0053. This is
verified by the AMPA_ONLY peak-Hz regression sentinel (REQ-14 / 0.667 Hz).

Pre-condition for ``build_ei_pairs``: ``h.gaba_tonic`` must be registered (call
``neuron_bootstrap.ensure_gaba_tonic_compiled()`` before invoking this function).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from tasks.t0057_tonic_gaba_sweep_t0053.code.constants import (
    AMPA_E_MV,
    AMPA_PEAK_NS,
    AMPA_TAU1_MS,
    AMPA_TAU2_MS,
    BASE_OFFSET_MS,
    GABA_E_MV,
    GABA_RAMP_MS,
    T_OFF_MS,
    T_ON_MS,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.placement import Location


@dataclass(frozen=True, slots=True)
class EiPair:
    """One co-located AMPA Exp2Syn + tonic GABA pair.

    The ``ampa_netcon.weight[0]`` carries the AMPA per-event conductance in microsiemens (fixed at
    ``AMPA_PEAK_NS * 1e-3``, i.e., 0.5 nS = 0.0005 uS). The GABA branch uses no NetStim or NetCon:
    the conductance is set by direct attribute write to ``gaba_syn.g`` (microsiemens) and
    ``gaba_syn.t_on`` / ``gaba_syn.t_off`` (ms) per trial in :func:`schedule_ei_onsets`.

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
    ampa_netcon: Any


@dataclass(frozen=True, slots=True)
class ScheduleResult:
    """Result of one ``schedule_ei_onsets`` call.

    ``onset_times_ms[i]`` is the bar-arrival time in ms for pair ``i`` (with the BASE_OFFSET_MS
    added). ``i_fired_mask[i]`` is True iff the spatial centripetal-gating rule fired pair ``i``'s
    GABA synapse for this stimulus direction; when False, the I synapse's tonic conductance is
    set to zero.
    """

    onset_times_ms: list[float]
    i_fired_mask: list[bool]


def i_synapse_fires(
    *,
    theta_stim_deg: float,
    theta_centrifugal_deg: float,
) -> bool:
    """Return True iff the I synapse fires under the centripetal-gating rule.

    The rule (bit-for-bit identical to t0053 ``synapses.py`` lines 76-91) is:

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
    """Construct one AMPA Exp2Syn + tonic gaba_tonic instance per ``Location``.

    Each pair's ``theta_centrifugal_rad`` is precomputed from its (x_um, y_um) and the soma
    origin's (x_soma, y_soma) using ``atan2(y - y_soma, x - x_soma)``. AMPA is driven by its own
    ``h.NetStim(number=1, noise=0)`` via an ``h.NetCon`` whose ``weight[0]`` carries the AMPA
    per-event conductance in microsiemens. GABA is driven by direct attribute writes to the
    tonic point process; no NetStim or NetCon is used for the GABA branch.
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

        gaba_syn: Any = h.gaba_tonic(seg)
        gaba_syn.e = GABA_E_MV
        gaba_syn.g = 0.0
        gaba_syn.t_on = 0.0
        gaba_syn.t_off = 0.0
        gaba_syn.ramp_ms = GABA_RAMP_MS

        ampa_netstim: Any = h.NetStim()
        ampa_netstim.number = 1
        ampa_netstim.noise = 0.0
        ampa_netstim.interval = 1.0  # required by NEURON even for single events
        ampa_netstim.start = 0.0

        ampa_netcon: Any = h.NetCon(ampa_netstim, ampa_syn)
        ampa_netcon.delay = 0.0
        ampa_netcon.weight[0] = AMPA_PEAK_NS * 1e-3  # nS -> uS

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
                ampa_netcon=ampa_netcon,
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
    gaba_base_ns: float,
) -> ScheduleResult:
    """Set per-pair AMPA NetStim.start times and per-pair tonic GABA window/conductance.

    For each pair: AMPA always fires once at the bar-arrival time at the synapse's projected
    position on the bar's normal. GABA's tonic window is opened only when the spatial
    centripetal-gating rule ``cos(radians(angle_deg - degrees(theta_centrifugal_rad))) < 0`` is
    True. When fired, the GABA tonic conductance is ``gaba_base_ns * 1e-3`` (microsiemens) over
    ``[T_ON_MS, T_OFF_MS]``; when silent, ``g`` is 0 and the window edges are collapsed to 0.

    Returns a :class:`ScheduleResult` carrying the per-pair onset times and the per-pair fire
    mask. The mask is downstream-consumed by the active-fraction CSV emitter and the
    activation-time histogram renderer.
    """
    onset_times_ms: list[float] = []
    i_fired_mask: list[bool] = []
    ampa_weight_us: float = AMPA_PEAK_NS * 1e-3
    gaba_full_g_us: float = gaba_base_ns * 1e-3
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
            pair.gaba_syn.g = gaba_full_g_us
            pair.gaba_syn.t_on = T_ON_MS
            pair.gaba_syn.t_off = T_OFF_MS
        else:
            pair.gaba_syn.g = 0.0
            pair.gaba_syn.t_on = 0.0
            pair.gaba_syn.t_off = 0.0

        onset_times_ms.append(onset_ms)
        i_fired_mask.append(fires)
    return ScheduleResult(
        onset_times_ms=onset_times_ms,
        i_fired_mask=i_fired_mask,
    )
