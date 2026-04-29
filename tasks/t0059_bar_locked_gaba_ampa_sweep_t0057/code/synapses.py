"""Co-located E + I synapse pairs with bar-arrival-locked tonic GABA windows.

Adapted from ``tasks/t0057_tonic_gaba_sweep_t0053/code/synapses.py``. Two surgical changes per the
t0059 plan:

1. **Per-synapse bar-arrival-locked window (REQ-1).** The constant ``T_ON_MS`` / ``T_OFF_MS``
   writes in t0057's ``schedule_ei_onsets`` are replaced by ``pair.gaba_syn.t_on = onset_ms`` and
   ``pair.gaba_syn.t_off = onset_ms + WINDOW_MS``, where ``onset_ms`` is the same per-pair
   bar-arrival time used by the AMPA NetStim and ``WINDOW_MS = 200.0`` ms is fixed (REQ-1).

2. **Public ``gampa_ns`` parameter (REQ-7).** The previously hard-coded ``AMPA_PEAK_NS`` is
   replaced by a public ``gampa_ns: float`` parameter on ``schedule_ei_onsets``. The AMPA NetCon
   weight becomes ``pair.ampa_netcon.weight[0] = gampa_ns * 1e-3``.

The spatial centripetal-gating predicate ``i_synapse_fires`` is bit-identical to t0053 / t0057.
Silent (non-firing) I synapses still receive ``g = 0``, ``t_on = 0``, ``t_off = 0`` so subsequent
``schedule_ei_onsets`` calls always start from a clean state.

Pre-condition for ``build_ei_pairs``: ``h.gaba_tonic`` must be registered (call
``neuron_bootstrap.ensure_gaba_tonic_compiled()`` before invoking this function).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants import (
    AMPA_E_MV,
    AMPA_TAU1_MS,
    AMPA_TAU2_MS,
    BASE_OFFSET_MS,
    GABA_E_MV,
    GABA_RAMP_MS,
    WINDOW_MS,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.placement import Location


@dataclass(frozen=True, slots=True)
class EiPair:
    """One co-located AMPA Exp2Syn + tonic GABA pair.

    The ``ampa_netcon.weight[0]`` carries the AMPA per-event conductance in microsiemens (set by
    ``schedule_ei_onsets`` to ``gampa_ns * 1e-3``). The GABA branch uses no NetStim or NetCon:
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

    The rule (bit-for-bit identical to t0053 / t0057) is:

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
    ``h.NetStim(number=1, noise=0)`` via an ``h.NetCon`` whose ``weight[0]`` is set per trial by
    ``schedule_ei_onsets`` (was hard-coded at AMPA_PEAK_NS * 1e-3 in t0057). GABA is driven by
    direct attribute writes to the tonic point process; no NetStim or NetCon is used for the
    GABA branch.
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
        ampa_netcon.weight[0] = 0.0  # set per trial by schedule_ei_onsets

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
    gampa_ns: float,
    gaba_base_ns: float,
) -> ScheduleResult:
    """Set per-pair AMPA NetStim.start times and per-pair tonic GABA window/conductance.

    For each pair: AMPA always fires once at the bar-arrival time at the synapse's projected
    position on the bar's normal. GABA's tonic window is opened only when the spatial
    centripetal-gating rule ``cos(radians(angle_deg - degrees(theta_centrifugal_rad))) < 0`` is
    True. When fired, the GABA tonic conductance is ``gaba_base_ns * 1e-3`` (microsiemens) over
    a per-synapse window ``[t_on_i, t_on_i + WINDOW_MS]`` where ``t_on_i = onset_ms`` is the
    same bar-arrival time used by the AMPA NetStim. When silent, ``g`` is 0 and the window edges
    are collapsed to 0.

    The AMPA NetCon weight is ``gampa_ns * 1e-3`` (microsiemens) for every pair (REQ-7).

    Returns a :class:`ScheduleResult` carrying the per-pair onset times and the per-pair fire
    mask.
    """
    onset_times_ms: list[float] = []
    i_fired_mask: list[bool] = []
    ampa_weight_us: float = gampa_ns * 1e-3
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
            pair.gaba_syn.t_on = onset_ms
            pair.gaba_syn.t_off = onset_ms + WINDOW_MS
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
