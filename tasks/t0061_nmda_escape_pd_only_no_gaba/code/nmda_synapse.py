"""NMDA-only synapse builder for t0061.

Each E location gets ONE NMDA_MgBlock POINT_PROCESS plus a NetStim + NetCon. No AMPA Exp2Syn,
no GABA tonic — fully replaces t0059's EiPair with an NMDA-only construct.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.placement import Location

NMDA_TAU1_MS: float = 5.0
NMDA_TAU2_MS: float = 80.0
NMDA_REVERSAL_MV: float = 0.0


@dataclass(slots=True)
class NmdaPair:
    """One NMDA-only synapse instance.

    Carries both the POINT_PROCESS handle (for setting parameters and recording) and the
    NetStim + NetCon driving it (for setting per-trial start time and weight).
    """

    location: Location
    nmda: Any  # h.NMDA_MgBlock instance
    netstim: Any  # h.NetStim
    netcon: Any  # h.NetCon


def build_nmda_pairs(
    *,
    h: Any,
    locations: list[Location],
    sections: list[Any],
    soma_origin_um: tuple[float, float, float],
) -> list[NmdaPair]:
    """Construct one NMDA-only synapse per Location."""
    _ = soma_origin_um  # not used here; signature parallels t0059 build_ei_pairs
    pairs: list[NmdaPair] = []
    for loc in locations:
        section = sections[loc.section_index]
        seg = section(loc.section_x)
        nmda = h.NMDA_MgBlock(seg)
        nmda.tau1 = NMDA_TAU1_MS
        nmda.tau2 = NMDA_TAU2_MS
        nmda.e = NMDA_REVERSAL_MV
        nmda.Voff = 0  # voltage-dependent (Mg block on)
        netstim = h.NetStim()
        netstim.number = 1
        netstim.start = 100.0  # placeholder; overwritten per trial
        netstim.noise = 0.0
        netcon = h.NetCon(netstim, nmda)
        netcon.weight[0] = 0.0  # placeholder; overwritten per trial
        netcon.delay = 0.0
        pairs.append(
            NmdaPair(location=loc, nmda=nmda, netstim=netstim, netcon=netcon),
        )
    return pairs


def schedule_nmda_onsets(
    *,
    pairs: list[NmdaPair],
    angle_deg: float,
    velocity_um_per_ms: float,
    base_offset_ms: float,
    gnmda_ns: float,
) -> list[float]:
    """Per-trial scheduling of NetStim onsets and NMDA NetCon weights.

    Each location's onset is the bar-arrival time at that synapse's coordinate. Returns the
    per-pair onset times for diagnostic purposes.
    """
    import math

    weight_us: float = gnmda_ns * 1e-3
    onsets: list[float] = []
    theta_rad: float = math.radians(angle_deg)
    cos_t: float = math.cos(theta_rad)
    sin_t: float = math.sin(theta_rad)
    for pair in pairs:
        x: float = pair.location.x_um
        y: float = pair.location.y_um
        onset: float = (x * cos_t + y * sin_t) / velocity_um_per_ms + base_offset_ms
        pair.netstim.start = onset
        pair.netcon.weight[0] = weight_us
        onsets.append(onset)
    return onsets
