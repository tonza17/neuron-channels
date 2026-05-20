"""Trial helpers for the t0080 Bed B v2 MOBO task.

Helpers ``_bar_arrival_times``, ``_rates_with_ar2_noise``, ``_gaba_prob_for_direction``,
``_rates_to_events``, ``_count_spikes``, ``BASE_ACH_PROB``, ``RATE_DT_MS``, ``BAR_SIGMA_MS``,
``CELL_PREF_DEG``, ``PREF_GABA_PROB``, ``NULL_GABA_PROB`` are COPIED verbatim from
``tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`` (lines 52-232) per
the project's cross-task code-reuse rule (these are private helpers in t0024, not entry
points of the registered ``de_rosenroll_2026_dsgc`` library asset).

``_setup_synapses_parametric`` is forked from t0076 unchanged. AIS sections are
not in ``cell.all_dends`` (they live in ``cell.ais_proximal`` / ``cell.ais_distal``)
so the placer's candidate set automatically excludes the AIS — no synapses are
ever placed on the AIS.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C24
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.ar2_noise import (
    generate_ar2_batch,
)
from tasks.t0113_t0106_seed2247_replicate.code import (
    bootstrap as _bootstrap,  # noqa: F401
)
from tasks.t0113_t0106_seed2247_replicate.code.build_cell_ais import (
    DSGCCellWithAIS,
)
from tasks.t0113_t0106_seed2247_replicate.code.constants_electrophys import (
    ACH_EREV_MV,
    ACH_TAU1_MS,
    ACH_TAU2_MS,
    GABA_EREV_MV,
    GABA_TAU1_MS,
    GABA_TAU2_MS,
)
from tasks.t0113_t0106_seed2247_replicate.code.parametric_placer import (
    PlacedSynapse,
    place_synapses,
)

# ---- BEGIN COPIED FROM t0024 run_tuning_curve.py lines 52-95 ----

RATE_DT_MS: float = 1.0
BAR_SIGMA_MS: float = 30.0
BASE_ACH_PROB: float = 0.5
PREF_GABA_PROB: float = 0.05
NULL_GABA_PROB: float = 0.80
CELL_PREF_DEG: float = 0.0


def _gaba_prob_for_direction(direction_deg: float) -> float:
    """Sigmoid between PREF_GABA_PROB and NULL_GABA_PROB based on angle-from-pref."""
    d = abs((direction_deg - CELL_PREF_DEG + 180.0) % 360.0 - 180.0)
    sigmoid_val: float = float(1.0 - 0.98 / (1.0 + np.exp((d - 91.0) / 25.0)))
    return PREF_GABA_PROB + (NULL_GABA_PROB - PREF_GABA_PROB) * sigmoid_val


def _bar_arrival_times(
    syn_xy: NDArray[np.float64],
    origin_xy: tuple[float, float],
    direction_deg: float,
) -> NDArray[np.float64]:
    """Time (ms) at which the moving bar intersects each synapse."""
    theta = np.radians(direction_deg)
    ux, uy = float(np.cos(theta)), float(np.sin(theta))
    dx = syn_xy[:, 0] - origin_xy[0]
    dy = syn_xy[:, 1] - origin_xy[1]
    proj = dx * ux + dy * uy
    return C24.BAR_START_TIME_MS + (proj - C24.BAR_X_START_UM) / C24.BAR_VELOCITY_UM_PER_MS


def _rates_with_ar2_noise(
    *,
    n_syn: int,
    n_bins: int,
    rate_dt_ms: float,
    arrival_times_ms: NDArray[np.float64],
    rho: float,
    seed: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Per-synapse (n_syn, n_bins) rate traces for ACh and GABA."""
    t_ms = np.arange(n_bins, dtype=np.float64) * rate_dt_ms
    traces = generate_ar2_batch(
        n_samples=n_bins,
        n_streams=n_syn,
        phi=C24.AR2_PHI,
        rho=rho,
        seed=seed,
        innov_scale=C24.AR2_INNOV_SCALE,
    )
    env = np.exp(-0.5 * ((t_ms[None, :] - arrival_times_ms[:, None]) / BAR_SIGMA_MS) ** 2)
    base = C24.AR2_BASE_RATE_HZ * env
    ach = np.clip(base * (1.0 + traces[:, :, 0]), a_min=0.0, a_max=None)
    gaba = np.clip(base * (1.0 + traces[:, :, 1]), a_min=0.0, a_max=None)
    return ach, gaba


def _rates_to_events(
    *,
    rates_hz: NDArray[np.float64],
    release_prob: NDArray[np.float64],
    rate_dt_ms: float,
    rng: np.random.Generator,
) -> list[list[float]]:
    """Convert (n_syn, n_bins) rates to per-synapse lists of event times (ms)."""
    n_syn, n_bins = rates_hz.shape
    lam = rates_hz * (rate_dt_ms / 1000.0) * release_prob[:, None]
    counts = rng.poisson(lam=lam)
    events: list[list[float]] = []
    for s in range(n_syn):
        syn_events: list[float] = []
        for b in range(n_bins):
            k = int(counts[s, b])
            if k == 0:
                continue
            jitter = rng.uniform(0.0, rate_dt_ms, size=k)
            t0 = b * rate_dt_ms
            for j in jitter:
                syn_events.append(float(t0 + j))
        syn_events.sort()
        events.append(syn_events)
    return events


def _count_spikes(v_trace: NDArray[np.float64], threshold_mv: float) -> int:
    """Count rising threshold crossings in a voltage trace."""
    above = v_trace > threshold_mv
    return int(np.sum((~above[:-1]) & above[1:]))


# ---- END COPIED FROM t0024 ----


@dataclass(slots=True)
class SynapseBundle:
    """All NEURON objects that must be kept alive for the synapses to work.

    v3 extension: ``syns_nmda`` and ``ncs_nmda`` co-located with each ACh
    placement (REQ-2, REQ-5; one Exp2NMDA per ACh contact, sharing the same
    NetStim driver).
    """

    syns_ach: list[Any]
    syns_gaba: list[Any]
    ncs_ach: list[Any]
    ncs_gaba: list[Any]
    netstims: list[Any]
    syn_xy_ach: NDArray[np.float64]
    syn_xy_gaba: NDArray[np.float64]
    syns_nmda: list[Any]
    ncs_nmda: list[Any]


def _section_midpoint_xy(*, h: Any, section: Any) -> tuple[float, float]:
    """Return the (x, y) of the section's midpoint pt3d."""
    section.push()
    try:
        n_pts = int(h.n3d())
        if n_pts == 0:
            # Degenerate section: fall back to (0, 0).
            return (0.0, 0.0)
        if n_pts % 2 == 1:
            mid = (n_pts - 1) // 2
            return float(h.x3d(mid)), float(h.y3d(mid))
        a = n_pts // 2
        b = a - 1
        return (
            (float(h.x3d(a)) + float(h.x3d(b))) / 2.0,
            (float(h.y3d(a)) + float(h.y3d(b))) / 2.0,
        )
    finally:
        h.pop_section()


def _instantiate_synapse(
    *,
    h: Any,
    placed: PlacedSynapse,
    tau1_ms: float,
    tau2_ms: float,
    erev_mv: float,
    weight_us: float,
) -> tuple[Any, Any, Any]:
    """Create one Exp2Syn at ``placed.position`` plus its NetStim-driven NetCon."""
    syn = h.Exp2Syn(placed.position, sec=placed.section)
    syn.tau1 = tau1_ms
    syn.tau2 = tau2_ms
    syn.e = erev_mv

    netstim = h.NetStim()
    netstim.number = 0
    netstim.start = 1e9

    nc = h.NetCon(netstim, syn)
    nc.weight[0] = weight_us
    nc.delay = 0.0
    return syn, netstim, nc


def setup_synapses_parametric(
    *,
    cell: DSGCCellWithAIS,
    n_ach: int,
    n_gaba: int,
    rho_0_ach: float,
    lambda_ach_um: float,
    rho_0_gaba: float,
    lambda_gaba_um: float,
    w_ach_us: float,
    w_gaba_us: float,
    placer_seed: int,
    gnmda_dend: float = 0.0,
    mg_conc_mm: float = 0.3,
    voff_nmda: float = 0.0,
) -> SynapseBundle:
    """Place N_ach + N_gaba synapses on the dendritic tree per the spatial rule."""
    h = cell.h

    placed_ach: list[PlacedSynapse] = place_synapses(
        h=h,
        soma=cell.soma,
        candidate_sections=cell.all_dends,
        n_target=n_ach,
        rho_0=rho_0_ach,
        lambda_um=lambda_ach_um,
        seed=placer_seed,
    )
    placed_gaba: list[PlacedSynapse] = place_synapses(
        h=h,
        soma=cell.soma,
        candidate_sections=cell.all_dends,
        n_target=n_gaba,
        rho_0=rho_0_gaba,
        lambda_um=lambda_gaba_um,
        seed=placer_seed + 1,
    )

    syns_ach: list[Any] = []
    syns_gaba: list[Any] = []
    ncs_ach: list[Any] = []
    ncs_gaba: list[Any] = []
    netstims: list[Any] = []
    syns_nmda: list[Any] = []
    ncs_nmda: list[Any] = []
    xy_ach: NDArray[np.float64] = np.zeros((n_ach, 2), dtype=np.float64)
    xy_gaba: NDArray[np.float64] = np.zeros((n_gaba, 2), dtype=np.float64)

    for i, placed in enumerate(placed_ach):
        syn, netstim, nc = _instantiate_synapse(
            h=h,
            placed=placed,
            tau1_ms=ACH_TAU1_MS,
            tau2_ms=ACH_TAU2_MS,
            erev_mv=ACH_EREV_MV,
            weight_us=w_ach_us,
        )
        syns_ach.append(syn)
        ncs_ach.append(nc)
        netstims.append(netstim)
        # v3: co-locate Exp2NMDA on the same section/position, share the same
        # NetStim, drive with NetCon weight = gnmda_dend (REQ-2, REQ-5).
        nmda = h.Exp2NMDA(placed.position, sec=placed.section)
        nmda.tau1 = 50.0
        nmda.tau2 = 2.0
        nmda.e = 0.0
        nmda.n = mg_conc_mm
        nmda.gama = 0.074
        nmda.Voff = voff_nmda
        nmda.Vset = -60.0
        nc_nmda = h.NetCon(netstim, nmda)
        nc_nmda.weight[0] = gnmda_dend
        nc_nmda.delay = 0.0
        syns_nmda.append(nmda)
        ncs_nmda.append(nc_nmda)
        x, y = _section_midpoint_xy(h=h, section=placed.section)
        xy_ach[i, 0] = x
        xy_ach[i, 1] = y

    for i, placed in enumerate(placed_gaba):
        syn, netstim, nc = _instantiate_synapse(
            h=h,
            placed=placed,
            tau1_ms=GABA_TAU1_MS,
            tau2_ms=GABA_TAU2_MS,
            erev_mv=GABA_EREV_MV,
            weight_us=w_gaba_us,
        )
        syns_gaba.append(syn)
        ncs_gaba.append(nc)
        netstims.append(netstim)
        x, y = _section_midpoint_xy(h=h, section=placed.section)
        xy_gaba[i, 0] = x
        xy_gaba[i, 1] = y

    return SynapseBundle(
        syns_ach=syns_ach,
        syns_gaba=syns_gaba,
        ncs_ach=ncs_ach,
        ncs_gaba=ncs_gaba,
        netstims=netstims,
        syn_xy_ach=xy_ach,
        syn_xy_gaba=xy_gaba,
        syns_nmda=syns_nmda,
        ncs_nmda=ncs_nmda,
    )
