"""Co-located AMPA Exp2Syn + NMDA_MgBlock synapse builder for t0062."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.placement import Location
from tasks.t0062_nmda_escape_with_ampa_priming.code.constants import (
    AMPA_REVERSAL_MV,
    AMPA_TAU1_MS,
    AMPA_TAU2_MS,
)


@dataclass(slots=True)
class AmpaNmdaPair:
    """Co-located AMPA Exp2Syn + NMDA_MgBlock at one dendritic Location.

    Both mechanisms are driven by a single shared NetStim via two NetCons (one per mechanism).
    """

    location: Location
    ampa: Any  # h.Exp2Syn
    nmda: Any  # h.NMDA_MgBlock
    netstim: Any  # h.NetStim
    ampa_netcon: Any  # h.NetCon (NetStim -> ampa)
    nmda_netcon: Any  # h.NetCon (NetStim -> nmda)


def build_ampa_nmda_pairs(
    *,
    h: Any,
    locations: list[Location],
    sections: list[Any],
) -> list[AmpaNmdaPair]:
    pairs: list[AmpaNmdaPair] = []
    for loc in locations:
        section = sections[loc.section_index]
        seg = section(loc.section_x)
        ampa = h.Exp2Syn(seg)
        ampa.tau1 = AMPA_TAU1_MS
        ampa.tau2 = AMPA_TAU2_MS
        ampa.e = AMPA_REVERSAL_MV
        nmda = h.NMDA_MgBlock(seg)
        nmda.Voff = 0  # voltage-dependent (Mg block on)
        netstim = h.NetStim()
        netstim.number = 1
        netstim.start = 100.0
        netstim.noise = 0.0
        ampa_netcon = h.NetCon(netstim, ampa)
        ampa_netcon.delay = 0.0
        ampa_netcon.weight[0] = 0.0
        nmda_netcon = h.NetCon(netstim, nmda)
        nmda_netcon.delay = 0.0
        nmda_netcon.weight[0] = 0.0
        pairs.append(
            AmpaNmdaPair(
                location=loc,
                ampa=ampa,
                nmda=nmda,
                netstim=netstim,
                ampa_netcon=ampa_netcon,
                nmda_netcon=nmda_netcon,
            ),
        )
    return pairs


def schedule_onsets(
    *,
    pairs: list[AmpaNmdaPair],
    angle_deg: float,
    velocity_um_per_ms: float,
    base_offset_ms: float,
    gampa_priming_ns: float,
    gnmda_ns: float,
) -> None:
    ampa_weight_us: float = gampa_priming_ns * 1e-3
    nmda_weight_us: float = gnmda_ns * 1e-3
    theta_rad: float = math.radians(angle_deg)
    cos_t: float = math.cos(theta_rad)
    sin_t: float = math.sin(theta_rad)
    for pair in pairs:
        x: float = pair.location.x_um
        y: float = pair.location.y_um
        onset: float = (x * cos_t + y * sin_t) / velocity_um_per_ms + base_offset_ms
        pair.netstim.start = onset
        pair.ampa_netcon.weight[0] = ampa_weight_us
        pair.nmda_netcon.weight[0] = nmda_weight_us
