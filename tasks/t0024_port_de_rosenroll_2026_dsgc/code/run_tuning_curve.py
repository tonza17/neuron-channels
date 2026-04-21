"""Moving-bar tuning-curve driver for the de Rosenroll 2026 DSGC port.

This script realises plan steps 10, 11, 12: it runs N trials per direction
(8-direction and 12-angle sweeps) for both correlated (rho=0.6) and
uncorrelated / AMB (rho=0.0, GABA weight x1.8) conditions, counts somatic
spikes, and writes four CSVs under ``data/``.

Model sketch (simplified port of upstream ``ei_balance.py``):

* 177 terminal dendrites each carry one ACh (Exp2Syn, E=0 mV) and one GABA
  (Exp2Syn, E=-60 mV) synapse.
* A moving bar passes at 1 um/ms across a rotated coordinate frame. For
  each direction the bar arrival time at each synapse is computed by
  projecting its (x, y) location onto the velocity axis.
* Per-synapse release rates are baseline * (1 + AR2 noise), gated to a
  window centred on bar arrival (Gaussian of width SIGMA_MS). Rates are
  clipped at 0 and converted to Poisson spike counts per bin (RATE_DT_MS).
* ACh vs GABA cross-channel correlation is controlled by the AR(2) rho
  parameter (see ``ar2_noise.generate_ar2_process``).
* GABA has a directional asymmetry: release probability follows a smooth
  sigmoid in direction (null_prob on the null side, pref_prob on pref side),
  simulating the SAC-to-DSGC asymmetric inhibition described in the paper.
* Spike times are injected into each NetCon via
  ``FInitializeHandler`` + ``NetCon.event``.
* Somatic voltage is recorded; spikes are counted by threshold crossing at
  AP_THRESHOLD_MV.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C
from tasks.t0024_port_de_rosenroll_2026_dsgc.code import paths as P
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.ar2_noise import (
    generate_ar2_batch,
)
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import (
    DSGCCell,
    build_dsgc_cell,
)

# Release-kinetics parameters (not in plan, chosen to give a paper-like DSI).
RATE_DT_MS: float = 1.0  # binning for Poisson rate sampling
BAR_SIGMA_MS: float = 30.0  # width of the bar's temporal RF at each synapse
BASE_ACH_PROB: float = 0.5  # baseline ACh release probability
PREF_GABA_PROB: float = 0.05  # GABA release probability in preferred direction
NULL_GABA_PROB: float = 0.80  # GABA release probability in null direction
CELL_PREF_DEG: float = 0.0  # preferred direction (bar moving rightwards)

# Output CSV columns.
CSV_COLUMNS: list[str] = ["trial", "direction_deg", "spike_count", "peak_mv"]


@dataclass(frozen=True, slots=True)
class TrialResult:
    trial: int
    direction_deg: float
    spike_count: int
    peak_mv: float


@dataclass(frozen=True, slots=True)
class SweepConfig:
    angles_deg: tuple[int, ...]
    correlated: bool
    n_trials: int
    output_csv_path: Any
    seed_base: int


def _gaba_prob_for_direction(direction_deg: float) -> float:
    """Sigmoid between PREF_GABA_PROB and NULL_GABA_PROB based on angle-from-pref.

    Matches upstream ``dir_sigmoids["prob"]`` when centred on 180 deg null.
    """
    # angle between direction and cell preferred, wrapped into [0, 180]
    d = abs((direction_deg - CELL_PREF_DEG + 180.0) % 360.0 - 180.0)
    # upstream: p + (n - p) * (1 - 0.98 / (1 + exp((d - 91) / 25)))
    sigmoid_val: float = float(1.0 - 0.98 / (1.0 + np.exp((d - 91.0) / 25.0)))
    return PREF_GABA_PROB + (NULL_GABA_PROB - PREF_GABA_PROB) * sigmoid_val


def _bar_arrival_times(
    syn_xy: NDArray[np.float64],
    origin_xy: tuple[float, float],
    direction_deg: float,
) -> NDArray[np.float64]:
    """Time (ms) at which the moving bar intersects each synapse.

    The bar's velocity axis is along ``direction_deg`` at 1 um/ms, starting
    at ``(BAR_X_START_UM, BAR_Y_START_UM)`` relative to the cell origin.
    """
    theta = np.radians(direction_deg)
    ux, uy = float(np.cos(theta)), float(np.sin(theta))  # unit velocity vector
    # Project synapse offset from origin onto the velocity axis.
    dx = syn_xy[:, 0] - origin_xy[0]
    dy = syn_xy[:, 1] - origin_xy[1]
    # Bar leading edge starts at BAR_X_START_UM along the axis.
    proj = dx * ux + dy * uy
    return C.BAR_START_TIME_MS + (proj - C.BAR_X_START_UM) / C.BAR_VELOCITY_UM_PER_MS


def _rates_with_ar2_noise(
    *,
    n_syn: int,
    n_bins: int,
    rate_dt_ms: float,
    arrival_times_ms: NDArray[np.float64],
    rho: float,
    seed: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Per-synapse (n_syn, n_bins) rate traces for ACh and GABA.

    Returns (ach_rates, gaba_rates) in Hz, clipped at 0.
    Each synapse gets its own AR(2) stream (correlated across channels
    via the shared innovation inside ``generate_ar2_process``).
    """
    t_ms = np.arange(n_bins, dtype=np.float64) * rate_dt_ms
    # Vectorised: (n_syn, n_bins, 2).
    traces = generate_ar2_batch(
        n_samples=n_bins,
        n_streams=n_syn,
        phi=C.AR2_PHI,
        rho=rho,
        seed=seed,
        innov_scale=C.AR2_INNOV_SCALE,
    )
    # Gaussian envelope centred on each synapse's bar-arrival time.
    env = np.exp(-0.5 * ((t_ms[None, :] - arrival_times_ms[:, None]) / BAR_SIGMA_MS) ** 2)
    base = C.AR2_BASE_RATE_HZ * env  # (n_syn, n_bins)
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
    """Convert (n_syn, n_bins) rates to per-synapse lists of event times (ms).

    Each bin draws Poisson(rate * dt/1000) counts; the release probability
    scales the expected count so downstream NetCons either fire or don't.
    """
    n_syn, n_bins = rates_hz.shape
    # Expected count per bin in seconds. Apply per-synapse release prob.
    lam = rates_hz * (rate_dt_ms / 1000.0) * release_prob[:, None]
    counts = rng.poisson(lam=lam)
    events: list[list[float]] = []
    for s in range(n_syn):
        syn_events: list[float] = []
        for b in range(n_bins):
            k = int(counts[s, b])
            if k == 0:
                continue
            # Jitter events uniformly within the bin.
            jitter = rng.uniform(0.0, rate_dt_ms, size=k)
            t0 = b * rate_dt_ms
            for j in jitter:
                syn_events.append(float(t0 + j))
        syn_events.sort()
        events.append(syn_events)
    return events


@dataclass(slots=True)
class SynapseBundle:
    """All NEURON objects that must be kept alive for the synapses to work."""

    syns_ach: list[Any]
    syns_gaba: list[Any]
    ncs_ach: list[Any]
    ncs_gaba: list[Any]
    netstims: list[Any]  # strong refs so GC doesn't reap NetStim sources


def _setup_synapses(*, cell: DSGCCell, gaba_weight_scale: float) -> SynapseBundle:
    """Create ACh + GABA synapses on every terminal."""
    h = cell.h
    bundle = SynapseBundle(syns_ach=[], syns_gaba=[], ncs_ach=[], ncs_gaba=[], netstims=[])
    for dend in cell.terminal_dends:
        syn_e = h.Exp2Syn(0.5, sec=dend)
        syn_e.tau1 = C.ACH_TAU1_MS
        syn_e.tau2 = C.ACH_TAU2_MS
        syn_e.e = C.ACH_EREV_MV

        syn_i = h.Exp2Syn(0.5, sec=dend)
        syn_i.tau1 = C.GABA_TAU1_MS
        syn_i.tau2 = C.GABA_TAU2_MS
        syn_i.e = C.GABA_EREV_MV

        # Sources (NetStim.number=0 -> used only as a NetCon source that we
        # drive via nc.event(t)).
        ns_e = h.NetStim()
        ns_e.number = 0
        ns_e.start = 1e9
        nc_e = h.NetCon(ns_e, syn_e)
        nc_e.weight[0] = C.ACH_WEIGHT_US
        nc_e.delay = 0.0

        ns_i = h.NetStim()
        ns_i.number = 0
        ns_i.start = 1e9
        nc_i = h.NetCon(ns_i, syn_i)
        nc_i.weight[0] = C.GABA_WEIGHT_US * gaba_weight_scale
        nc_i.delay = 0.0

        bundle.syns_ach.append(syn_e)
        bundle.syns_gaba.append(syn_i)
        bundle.ncs_ach.append(nc_e)
        bundle.ncs_gaba.append(nc_i)
        bundle.netstims.append(ns_e)
        bundle.netstims.append(ns_i)
    return bundle


def _count_spikes(v_trace: NDArray[np.float64], threshold_mv: float) -> int:
    """Count rising threshold crossings in a voltage trace."""
    above = v_trace > threshold_mv
    return int(np.sum((~above[:-1]) & above[1:]))


def run_single_trial(
    *,
    cell: DSGCCell,
    ncs_ach: list[Any],
    ncs_gaba: list[Any],
    direction_deg: float,
    rho: float,
    seed: int,
) -> TrialResult:
    """Run one bar-sweep trial and return spike count + peak voltage."""
    h = cell.h
    n_syn = len(cell.terminal_dends)
    n_bins = int(np.ceil(C.TSTOP_MS / RATE_DT_MS))

    # Compute bar arrival times for this direction.
    arrival = _bar_arrival_times(
        syn_xy=cell.terminal_locs_xy,
        origin_xy=cell.origin_xy,
        direction_deg=direction_deg,
    )

    # Generate AR(2)-modulated rate traces per synapse.
    ach_rates, gaba_rates = _rates_with_ar2_noise(
        n_syn=n_syn,
        n_bins=n_bins,
        rate_dt_ms=RATE_DT_MS,
        arrival_times_ms=arrival,
        rho=rho,
        seed=seed,
    )

    # Directional release probabilities.
    gaba_prob = _gaba_prob_for_direction(direction_deg)
    ach_probs = np.full(n_syn, BASE_ACH_PROB, dtype=np.float64)
    gaba_probs = np.full(n_syn, gaba_prob, dtype=np.float64)

    # Convert rates to spike-time events.
    rng = np.random.default_rng(seed + 1_000_003)
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

    # Queue events via FInitializeHandler so they land in the event queue
    # after h.finitialize() clears it.
    def _queue() -> None:
        for i, nc in enumerate(ncs_ach):
            for t in ach_events[i]:
                if t < C.TSTOP_MS:
                    nc.event(t)
        for i, nc in enumerate(ncs_gaba):
            for t in gaba_events[i]:
                if t < C.TSTOP_MS:
                    nc.event(t)

    fih = h.FInitializeHandler(_queue)

    # Record soma.
    v_vec = h.Vector()
    v_vec.record(cell.soma(0.5)._ref_v)

    h.celsius = C.CELSIUS_DEG_C
    h.dt = C.DT_MS
    h.steps_per_ms = C.STEPS_PER_MS
    h.v_init = C.V_INIT_MV
    h.tstop = C.TSTOP_MS
    h.finitialize(C.V_INIT_MV)
    _ = fih  # keep alive
    h.run()

    v = np.array(v_vec.to_python(), dtype=np.float64)
    spikes = _count_spikes(v, C.AP_THRESHOLD_MV)
    peak = float(v.max()) if v.size else float("nan")
    return TrialResult(
        trial=seed,
        direction_deg=direction_deg,
        spike_count=spikes,
        peak_mv=peak,
    )


def run_sweep(
    cfg: SweepConfig,
    *,
    cell: DSGCCell,
    limit_per_angle: int | None = None,
) -> list[TrialResult]:
    """Run the full sweep; returns a flat list of TrialResult records."""
    rho = C.AR2_CROSS_CORR_RHO_CORRELATED if cfg.correlated else C.AR2_CROSS_CORR_RHO_UNCORRELATED
    gaba_scale = 1.0 if cfg.correlated else C.GABA_SCALE_UNCORRELATED

    # Setup synapses with the appropriate GABA weight.
    bundle = _setup_synapses(cell=cell, gaba_weight_scale=gaba_scale)
    ncs_ach = bundle.ncs_ach
    ncs_gaba = bundle.ncs_gaba

    n_trials = cfg.n_trials if limit_per_angle is None else min(cfg.n_trials, limit_per_angle)

    results: list[TrialResult] = []
    for angle in cfg.angles_deg:
        for trial in range(n_trials):
            seed = cfg.seed_base + trial * 10_007 + int(angle) * 13
            t0 = time.time()
            res = run_single_trial(
                cell=cell,
                ncs_ach=ncs_ach,
                ncs_gaba=ncs_gaba,
                direction_deg=float(angle),
                rho=rho,
                seed=seed,
            )
            dt = time.time() - t0
            results.append(res)
            print(
                f"  dir={angle:>3}  trial={trial:>2}  spikes={res.spike_count:>3}"
                f"  peak={res.peak_mv:+.1f}  [{dt:.2f}s]",
                flush=True,
            )
    return results


def _write_csv(path: Any, results: list[TrialResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)
        for r in results:
            writer.writerow([r.trial, r.direction_deg, r.spike_count, f"{r.peak_mv:.3f}"])


def _configs_for_mode(mode: str) -> list[SweepConfig]:
    """Build the list of SweepConfigs for the requested CLI mode."""
    if mode == "preflight":
        return [
            SweepConfig(
                angles_deg=C.ANGLES_8DIR_DEG,
                correlated=True,
                n_trials=C.N_TRIALS_PER_ANGLE,
                output_csv_path=P.TUNING_CURVE_8DIR_CORR_PREFLIGHT_CSV,
                seed_base=1000,
            ),
        ]
    if mode == "full":
        return [
            SweepConfig(
                angles_deg=C.ANGLES_8DIR_DEG,
                correlated=True,
                n_trials=C.N_TRIALS_PER_ANGLE,
                output_csv_path=P.TUNING_CURVE_8DIR_CORR_CSV,
                seed_base=1000,
            ),
            SweepConfig(
                angles_deg=C.ANGLES_8DIR_DEG,
                correlated=False,
                n_trials=C.N_TRIALS_PER_ANGLE,
                output_csv_path=P.TUNING_CURVE_8DIR_UNCORR_CSV,
                seed_base=2000,
            ),
            SweepConfig(
                angles_deg=C.ANGLES_12ANG_DEG,
                correlated=True,
                n_trials=C.N_TRIALS_PER_ANGLE,
                output_csv_path=P.TUNING_CURVE_12ANG_CORR_CSV,
                seed_base=3000,
            ),
            SweepConfig(
                angles_deg=C.ANGLES_12ANG_DEG,
                correlated=False,
                n_trials=C.N_TRIALS_PER_ANGLE,
                output_csv_path=P.TUNING_CURVE_12ANG_UNCORR_CSV,
                seed_base=4000,
            ),
        ]
    raise ValueError(f"Unknown mode: {mode}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        required=True,
        choices=["preflight", "full"],
        help="preflight: 3 trials 1 dir (correlated only); full: all 4 CSVs",
    )
    parser.add_argument(
        "--limit-per-angle",
        type=int,
        default=None,
        help="cap trials per angle (preflight sanity check); default = full N_TRIALS",
    )
    args = parser.parse_args(argv)

    cell = build_dsgc_cell()
    print(f"Cell loaded: {len(cell.terminal_dends)} terminals")

    cfgs = _configs_for_mode(args.mode)
    for cfg in cfgs:
        label = "correlated" if cfg.correlated else "uncorrelated"
        print(
            f"\n=== sweep: n_angles={len(cfg.angles_deg)} "
            f"n_trials/angle={cfg.n_trials} rho={label} ==="
        )
        results = run_sweep(cfg, cell=cell, limit_per_angle=args.limit_per_angle)
        _write_csv(cfg.output_csv_path, results)
        print(f"wrote {len(results)} rows -> {cfg.output_csv_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
