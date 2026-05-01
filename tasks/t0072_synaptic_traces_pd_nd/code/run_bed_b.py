"""Bed B (de Rosenroll 2026 DSGC port) PD + ND trial runner with per-synapse recording.

Records g_ACh and g_GABA (Exp2Syn _ref_g, in microsiemens) and the local membrane voltage
v at the synapse insertion point for every terminal-dendrite synapse pair. PD/ND swap is
implemented via the bar's direction angle (0 deg PD vs 180 deg ND).

The Exp2Syn _ref_g values returned here are in microsiemens (uS); the aggregate.py step
converts them to nanosiemens (nS) before computing I = g * (v - E).

Helpers ``_setup_synapses``, ``SynapseBundle``, ``_bar_arrival_times``,
``_rates_with_ar2_noise``, ``_gaba_prob_for_direction``, ``_rates_to_events``,
``_count_spikes``, ``BASE_ACH_PROB``, ``RATE_DT_MS``, ``BAR_SIGMA_MS``,
``CELL_PREF_DEG``, ``PREF_GABA_PROB``, ``NULL_GABA_PROB`` are COPIED verbatim from
``tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`` (lines 52-232) per
the project's cross-task code-reuse rule (these are private helpers in t0024, not entry
points of the registered ``de_rosenroll_2026_dsgc`` library asset).

The trial-runner pattern is adapted from
``tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py`` ``_run_one_trial``
(lines 205-298) with EPSP_PASSIVE / IPSP_PASSIVE mode logic stripped (FULL mode only).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C24
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.ar2_noise import (
    generate_ar2_batch,
)
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import (
    DSGCCell,
    build_dsgc_cell,
)
from tasks.t0072_synaptic_traces_pd_nd.code.constants import (
    DIRECTION_ND_DEG,
    DIRECTION_PD_DEG,
    E_ACH_BED_B_MV,
    E_GABA_BED_B_MV,
    E_REV_MV_KEY,
    G_TRACES_KEY,
    GABA_WEIGHT_SCALE,
    RECORD_DT_MS,
    RHO_CORRELATED,
    SEED,
    T_MS_KEY,
    TSTOP_MS,
    V_INIT_MV,
    V_LOCAL_TRACES_KEY,
    Direction,
    RecordedSynapseType,
)
from tasks.t0072_synaptic_traces_pd_nd.code.paths import (
    BED_B_ND_ACH_NPZ,
    BED_B_ND_GABA_NPZ,
    BED_B_PD_ACH_NPZ,
    BED_B_PD_GABA_NPZ,
    DATA_DIR,
)

# ---- BEGIN COPIED HELPERS (from t0024 run_tuning_curve.py L52-232) ----

# Release-kinetics parameters (not in plan, chosen to give a paper-like DSI).
RATE_DT_MS: float = 1.0  # binning for Poisson rate sampling
BAR_SIGMA_MS: float = 30.0  # width of the bar's temporal RF at each synapse
BASE_ACH_PROB: float = 0.5  # baseline ACh release probability
PREF_GABA_PROB: float = 0.05  # GABA release probability in preferred direction
NULL_GABA_PROB: float = 0.80  # GABA release probability in null direction
CELL_PREF_DEG: float = 0.0  # preferred direction (bar moving rightwards)


@dataclass(slots=True)
class SynapseBundle:
    """All NEURON objects that must be kept alive for the synapses to work."""

    syns_ach: list[Any]
    syns_gaba: list[Any]
    ncs_ach: list[Any]
    ncs_gaba: list[Any]
    netstims: list[Any]


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
    """Per-synapse (n_syn, n_bins) rate traces for ACh and GABA in Hz, clipped at 0."""
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


def _setup_synapses(*, cell: DSGCCell, gaba_weight_scale: float) -> SynapseBundle:
    """Create ACh + GABA Exp2Syn synapses on every terminal dendrite."""
    h = cell.h
    bundle = SynapseBundle(syns_ach=[], syns_gaba=[], ncs_ach=[], ncs_gaba=[], netstims=[])
    for dend in cell.terminal_dends:
        syn_e = h.Exp2Syn(0.5, sec=dend)
        syn_e.tau1 = C24.ACH_TAU1_MS
        syn_e.tau2 = C24.ACH_TAU2_MS
        syn_e.e = C24.ACH_EREV_MV

        syn_i = h.Exp2Syn(0.5, sec=dend)
        syn_i.tau1 = C24.GABA_TAU1_MS
        syn_i.tau2 = C24.GABA_TAU2_MS
        syn_i.e = C24.GABA_EREV_MV

        ns_e = h.NetStim()
        ns_e.number = 0
        ns_e.start = 1e9
        nc_e = h.NetCon(ns_e, syn_e)
        nc_e.weight[0] = C24.ACH_WEIGHT_US
        nc_e.delay = 0.0

        ns_i = h.NetStim()
        ns_i.number = 0
        ns_i.start = 1e9
        nc_i = h.NetCon(ns_i, syn_i)
        nc_i.weight[0] = C24.GABA_WEIGHT_US * gaba_weight_scale
        nc_i.delay = 0.0

        bundle.syns_ach.append(syn_e)
        bundle.syns_gaba.append(syn_i)
        bundle.ncs_ach.append(nc_e)
        bundle.ncs_gaba.append(nc_i)
        bundle.netstims.append(ns_e)
        bundle.netstims.append(ns_i)
    return bundle


# ---- END COPIED HELPERS ----


@dataclass(slots=True)
class BedBRecorders:
    """NEURON Vector handles for Bed B (Exp2Syn ACh + GABA per terminal)."""

    g_ach: list[Any]
    g_gaba: list[Any]
    v_local: list[Any]
    t_rec: Any
    n_terminals: int


def _attach_bed_b_recorders(*, h: Any, bundle: SynapseBundle) -> BedBRecorders:
    """Attach Vector.record handles for ACh g, GABA g, and per-synapse local v."""
    n_terminals: int = len(bundle.syns_ach)
    assert n_terminals == len(bundle.syns_gaba), (
        f"Bundle has mismatched ACh ({n_terminals}) and GABA "
        f"({len(bundle.syns_gaba)}) synapse counts"
    )
    g_ach: list[Any] = []
    g_gaba: list[Any] = []
    v_local: list[Any] = []
    for i in range(n_terminals):
        syn_ach: Any = bundle.syns_ach[i]
        syn_gaba: Any = bundle.syns_gaba[i]

        v_a: Any = h.Vector()
        v_a.record(syn_ach._ref_g, RECORD_DT_MS)
        g_ach.append(v_a)

        v_g: Any = h.Vector()
        v_g.record(syn_gaba._ref_g, RECORD_DT_MS)
        g_gaba.append(v_g)

        seg: Any = syn_ach.get_segment()
        v_v: Any = h.Vector()
        v_v.record(seg._ref_v, RECORD_DT_MS)
        v_local.append(v_v)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t, RECORD_DT_MS)
    return BedBRecorders(
        g_ach=g_ach,
        g_gaba=g_gaba,
        v_local=v_local,
        t_rec=t_rec,
        n_terminals=n_terminals,
    )


def _vectors_to_2d_array(*, vectors: list[Any]) -> np.ndarray:
    """Stack a list of NEURON Vectors into a (n_synapses, n_samples) numpy array."""
    assert len(vectors) > 0, "vector list is non-empty"
    arrays: list[np.ndarray] = [np.array(list(v), dtype=np.float64) for v in vectors]
    sizes: set[int] = {arr.size for arr in arrays}
    assert len(sizes) == 1, (
        f"Recorder vectors have inconsistent lengths: {sorted(sizes)}; recorder may "
        "have been attached after some traces started recording."
    )
    return np.stack(arrays, axis=0)


def _save_one_type(
    *,
    output_path: Path,
    g_vectors: list[Any],
    v_vectors: list[Any],
    t_rec: Any,
    e_rev_mv: float,
) -> None:
    """Stack vectors and save a compressed .npz."""
    g_traces: np.ndarray = _vectors_to_2d_array(vectors=g_vectors)
    v_local_traces: np.ndarray = _vectors_to_2d_array(vectors=v_vectors)
    t_ms: np.ndarray = np.array(list(t_rec), dtype=np.float64)
    assert g_traces.shape == v_local_traces.shape, (
        f"g_traces shape {g_traces.shape} != v_local_traces shape {v_local_traces.shape}"
    )
    assert g_traces.shape[1] == t_ms.size, (
        f"g_traces n_samples {g_traces.shape[1]} != t_ms size {t_ms.size}"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output_path,
        **{
            G_TRACES_KEY: g_traces.astype(np.float64),
            V_LOCAL_TRACES_KEY: v_local_traces.astype(np.float64),
            T_MS_KEY: t_ms.astype(np.float64),
            E_REV_MV_KEY: np.array(e_rev_mv, dtype=np.float64),
        },
    )
    print(
        f"  wrote {output_path.name}: g_traces={g_traces.shape}, "
        f"v_local_traces={v_local_traces.shape}, t_ms={t_ms.shape}, "
        f"e_rev={e_rev_mv} mV, size={output_path.stat().st_size} B"
    )


def _save_bed_b_direction(
    *,
    direction: Direction,
    recorders: BedBRecorders,
) -> None:
    """Save two .npz files (ACh, GABA) for one direction."""
    file_for_type: dict[RecordedSynapseType, Path] = {
        RecordedSynapseType.ACH: (
            BED_B_PD_ACH_NPZ if direction == Direction.PD else BED_B_ND_ACH_NPZ
        ),
        RecordedSynapseType.GABA: (
            BED_B_PD_GABA_NPZ if direction == Direction.PD else BED_B_ND_GABA_NPZ
        ),
    }
    g_for_type: dict[RecordedSynapseType, list[Any]] = {
        RecordedSynapseType.ACH: recorders.g_ach,
        RecordedSynapseType.GABA: recorders.g_gaba,
    }
    e_for_type: dict[RecordedSynapseType, float] = {
        RecordedSynapseType.ACH: E_ACH_BED_B_MV,
        RecordedSynapseType.GABA: E_GABA_BED_B_MV,
    }
    for syn_type in (RecordedSynapseType.ACH, RecordedSynapseType.GABA):
        _save_one_type(
            output_path=file_for_type[syn_type],
            g_vectors=g_for_type[syn_type],
            v_vectors=recorders.v_local,
            t_rec=recorders.t_rec,
            e_rev_mv=e_for_type[syn_type],
        )


def _run_bed_b_one_direction(
    *,
    cell: DSGCCell,
    bundle: SynapseBundle,
    direction: Direction,
    direction_deg: float,
) -> None:
    """Set up the bar, queue events, attach recorders, run one trial, save .npz files."""
    print(f"\n=== Bed B {direction.value.upper()} (direction_deg={direction_deg:.1f}) ===")
    h = cell.h

    n_syn: int = len(cell.terminal_dends)
    n_bins: int = int(np.ceil(C24.TSTOP_MS / RATE_DT_MS))

    arrival = _bar_arrival_times(
        syn_xy=cell.terminal_locs_xy,
        origin_xy=cell.origin_xy,
        direction_deg=direction_deg,
    )
    ach_rates, gaba_rates = _rates_with_ar2_noise(
        n_syn=n_syn,
        n_bins=n_bins,
        rate_dt_ms=RATE_DT_MS,
        arrival_times_ms=arrival,
        rho=RHO_CORRELATED,
        seed=SEED,
    )
    gaba_prob = _gaba_prob_for_direction(direction_deg)
    ach_probs = np.full(n_syn, BASE_ACH_PROB, dtype=np.float64)
    gaba_probs = np.full(n_syn, gaba_prob, dtype=np.float64)
    print(f"  n_syn={n_syn} n_bins={n_bins} gaba_prob={gaba_prob:.4f} ach_prob={BASE_ACH_PROB:.4f}")

    rng = np.random.default_rng(SEED + 1_000_003)
    ach_events = _rates_to_events(
        rates_hz=ach_rates,
        release_prob=ach_probs,
        rate_dt_ms=RATE_DT_MS,
        rng=rng,
    )
    gaba_events = _rates_to_events(
        rates_hz=gaba_rates,
        release_prob=gaba_probs,
        rate_dt_ms=RATE_DT_MS,
        rng=rng,
    )

    def _queue() -> None:
        for i, nc in enumerate(bundle.ncs_ach):
            for t in ach_events[i]:
                if t < C24.TSTOP_MS:
                    nc.event(t)
        for i, nc in enumerate(bundle.ncs_gaba):
            for t in gaba_events[i]:
                if t < C24.TSTOP_MS:
                    nc.event(t)

    fih = h.FInitializeHandler(_queue)
    recorders: BedBRecorders = _attach_bed_b_recorders(h=h, bundle=bundle)

    h.celsius = C24.CELSIUS_DEG_C
    h.dt = C24.DT_MS
    h.steps_per_ms = C24.STEPS_PER_MS
    h.v_init = V_INIT_MV
    h.tstop = TSTOP_MS
    h.finitialize(V_INIT_MV)
    _ = fih  # keep alive
    h.run()

    _save_bed_b_direction(direction=direction, recorders=recorders)


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Building Bed B cell (de Rosenroll 2026 port)...")
    cell: DSGCCell = build_dsgc_cell()
    n_terminals: int = len(cell.terminal_dends)
    print(f"Bed B cell ready: {n_terminals} terminal dendrites")

    bundle: SynapseBundle = _setup_synapses(cell=cell, gaba_weight_scale=GABA_WEIGHT_SCALE)
    print(
        f"Bed B synapses: {len(bundle.syns_ach)} ACh + "
        f"{len(bundle.syns_gaba)} GABA Exp2Syn instances"
    )

    _run_bed_b_one_direction(
        cell=cell,
        bundle=bundle,
        direction=Direction.PD,
        direction_deg=DIRECTION_PD_DEG,
    )
    _run_bed_b_one_direction(
        cell=cell,
        bundle=bundle,
        direction=Direction.ND,
        direction_deg=DIRECTION_ND_DEG,
    )
    print("\nBed B trials complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
