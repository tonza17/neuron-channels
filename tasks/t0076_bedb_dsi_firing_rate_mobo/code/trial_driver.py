"""Trial driver: 25-d ParameterVector -> (DSI, PD firing rate Hz).

The driver runs N_DIRECTIONS x N_SEEDS trials per cell evaluation. Each trial
applies the parameter vector to a (worker-cached) Bed B cell, builds the
parametric synapse bundle, queues the per-direction events, and runs ``h.run()``
under a try/except that returns the worst-case score on any RuntimeError per
plan.md Risk #4.

The single-process variant is used for the local Windows smoke test; the
multi-process variant uses ProcessPoolExecutor with ``max_workers``-1 cores.
"""

from __future__ import annotations

import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from os import cpu_count

import numpy as np
from numpy.typing import NDArray

from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C24
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import (
    DSGCCell,
    build_dsgc_cell,
)
from tasks.t0076_bedb_dsi_firing_rate_mobo.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0076_bedb_dsi_firing_rate_mobo.code.constants import (
    AP_THRESHOLD_MV,
    CELSIUS_DEG_C,
    DT_MS,
    ND_DIRECTION_DEG,
    PD_DIRECTION_DEG,
    RHO_CORRELATED,
    SEED_BASE,
    STEPS_PER_MS,
    TSTOP_MS,
    V_INIT_MV,
    WORST_CASE_DSI,
    WORST_CASE_RATE_HZ,
    ParameterVector,
)
from tasks.t0076_bedb_dsi_firing_rate_mobo.code.trial_helpers import (
    BASE_ACH_PROB,
    RATE_DT_MS,
    SynapseBundle,
    _bar_arrival_times,
    _count_spikes,
    _gaba_prob_for_direction,
    _rates_to_events,
    _rates_with_ar2_noise,
    setup_synapses_parametric,
)


@dataclass(frozen=True, slots=True)
class TrialResult:
    direction_deg: float
    seed: int
    spike_count: int
    peak_mv: float
    error: str | None


@dataclass(frozen=True, slots=True)
class EvalResult:
    dsi: float
    pd_rate_hz: float
    n_trials: int
    n_errors: int
    elapsed_s: float


# Worker process state: each worker keeps a cached cell and bundle so we don't
# rebuild morphology per trial.
_WORKER_CELL: DSGCCell | None = None
_WORKER_BUNDLE: SynapseBundle | None = None
_WORKER_PARAMS_HASH: int | None = None


def _worker_get_cell() -> DSGCCell:
    global _WORKER_CELL
    if _WORKER_CELL is None:
        _WORKER_CELL = build_dsgc_cell()
    return _WORKER_CELL


def _hash_param_vector(values: NDArray[np.float64]) -> int:
    return hash(values.tobytes())


def _worker_prepare(
    *, params: ParameterVector, placer_seed: int
) -> tuple[
    DSGCCell,
    SynapseBundle,
]:
    """Prepare cell + bundle in the worker; reuse if same params already applied."""
    global _WORKER_BUNDLE, _WORKER_PARAMS_HASH
    cell = _worker_get_cell()
    h = _hash_param_vector(params.values)
    if _WORKER_BUNDLE is None or h != _WORKER_PARAMS_HASH:
        apply_parameter_vector(cell=cell, params=params)
        _WORKER_BUNDLE = setup_synapses_parametric(
            cell=cell,
            n_ach=params.n_ach,
            n_gaba=params.n_gaba,
            rho_0_ach=params.rho0_ach,
            lambda_ach_um=params.lambda_ach_um,
            rho_0_gaba=params.rho0_gaba,
            lambda_gaba_um=params.lambda_gaba_um,
            w_ach_us=params.w_ach_us,
            w_gaba_us=params.w_gaba_us,
            placer_seed=placer_seed,
        )
        _WORKER_PARAMS_HASH = h
    return cell, _WORKER_BUNDLE


def run_one_trial(
    *,
    cell: DSGCCell,
    bundle: SynapseBundle,
    direction_deg: float,
    seed: int,
) -> TrialResult:
    """Run one bar-sweep trial; return spike count + peak voltage.

    Catches RuntimeError from ``h.run()`` and returns the worst-case fallback.
    """
    h = cell.h
    try:
        n_ach: int = len(bundle.syns_ach)
        n_gaba: int = len(bundle.syns_gaba)
        n_bins = int(np.ceil(TSTOP_MS / RATE_DT_MS))

        # ACh + GABA arrival times use their respective synapse xy coords.
        arrival_ach = _bar_arrival_times(
            syn_xy=bundle.syn_xy_ach,
            origin_xy=cell.origin_xy,
            direction_deg=direction_deg,
        )
        arrival_gaba = _bar_arrival_times(
            syn_xy=bundle.syn_xy_gaba,
            origin_xy=cell.origin_xy,
            direction_deg=direction_deg,
        )

        ach_rates, _ = _rates_with_ar2_noise(
            n_syn=n_ach,
            n_bins=n_bins,
            rate_dt_ms=RATE_DT_MS,
            arrival_times_ms=arrival_ach,
            rho=RHO_CORRELATED,
            seed=seed,
        )
        _, gaba_rates = _rates_with_ar2_noise(
            n_syn=n_gaba,
            n_bins=n_bins,
            rate_dt_ms=RATE_DT_MS,
            arrival_times_ms=arrival_gaba,
            rho=RHO_CORRELATED,
            seed=seed + 7919,
        )

        gaba_prob = _gaba_prob_for_direction(direction_deg)
        ach_probs = np.full(n_ach, BASE_ACH_PROB, dtype=np.float64)
        gaba_probs = np.full(n_gaba, gaba_prob, dtype=np.float64)

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

        def _queue() -> None:
            for i, nc in enumerate(bundle.ncs_ach):
                for t in ach_events[i]:
                    if t < TSTOP_MS:
                        nc.event(t)
            for i, nc in enumerate(bundle.ncs_gaba):
                for t in gaba_events[i]:
                    if t < TSTOP_MS:
                        nc.event(t)

        fih = h.FInitializeHandler(_queue)
        v_vec = h.Vector()
        v_vec.record(cell.soma(0.5)._ref_v)

        h.celsius = CELSIUS_DEG_C
        h.dt = DT_MS
        h.steps_per_ms = STEPS_PER_MS
        h.v_init = V_INIT_MV
        h.tstop = TSTOP_MS
        h.finitialize(V_INIT_MV)
        _ = fih
        h.run()

        v_arr = np.array(v_vec.to_python(), dtype=np.float64)
        if not np.all(np.isfinite(v_arr)):
            return TrialResult(
                direction_deg=direction_deg,
                seed=seed,
                spike_count=0,
                peak_mv=float("nan"),
                error="non_finite_voltage",
            )
        spikes = _count_spikes(v_arr, AP_THRESHOLD_MV)
        peak = float(v_arr.max()) if v_arr.size > 0 else float("nan")
        return TrialResult(
            direction_deg=direction_deg,
            seed=seed,
            spike_count=spikes,
            peak_mv=peak,
            error=None,
        )
    except (RuntimeError, ValueError, ArithmeticError) as exc:
        return TrialResult(
            direction_deg=direction_deg,
            seed=seed,
            spike_count=0,
            peak_mv=float("nan"),
            error=f"{type(exc).__name__}: {exc}",
        )


# ---------------------------------------------------------------------------
# Worker entrypoint (top-level so it pickles cleanly).
# ---------------------------------------------------------------------------


def _worker_run_trial(
    *,
    params_values: NDArray[np.float64],
    direction_deg: float,
    seed: int,
    placer_seed: int,
) -> TrialResult:
    """Top-level pickleable function used by ProcessPoolExecutor."""
    try:
        params = ParameterVector(values=params_values)
        cell, bundle = _worker_prepare(params=params, placer_seed=placer_seed)
        return run_one_trial(
            cell=cell,
            bundle=bundle,
            direction_deg=direction_deg,
            seed=seed,
        )
    except (RuntimeError, ValueError, ArithmeticError, AssertionError):
        return TrialResult(
            direction_deg=direction_deg,
            seed=seed,
            spike_count=0,
            peak_mv=float("nan"),
            error=traceback.format_exc(limit=2),
        )


def _summarise_trials(*, results: list[TrialResult]) -> EvalResult:
    """Aggregate trial results into (DSI, PD firing rate, error count)."""
    pd_spikes: list[int] = []
    nd_spikes: list[int] = []
    n_errors = 0
    for r in results:
        if r.error is not None:
            n_errors += 1
            continue
        if abs(r.direction_deg - PD_DIRECTION_DEG) < 1e-6:
            pd_spikes.append(r.spike_count)
        elif abs(r.direction_deg - ND_DIRECTION_DEG) < 1e-6:
            nd_spikes.append(r.spike_count)

    if len(pd_spikes) == 0 or n_errors >= len(results) // 2:
        return EvalResult(
            dsi=WORST_CASE_DSI,
            pd_rate_hz=WORST_CASE_RATE_HZ,
            n_trials=len(results),
            n_errors=n_errors,
            elapsed_s=0.0,
        )

    pd_mean = float(np.mean(pd_spikes))
    nd_mean = float(np.mean(nd_spikes)) if len(nd_spikes) > 0 else 0.0
    denom = pd_mean + nd_mean
    dsi = 0.0 if denom <= 0.0 else float((pd_mean - nd_mean) / denom)
    pd_rate_hz = pd_mean / (TSTOP_MS / 1000.0)
    return EvalResult(
        dsi=dsi,
        pd_rate_hz=pd_rate_hz,
        n_trials=len(results),
        n_errors=n_errors,
        elapsed_s=0.0,
    )


def evaluate_parameter_vector(
    *,
    params: ParameterVector,
    angles_deg: tuple[int, ...],
    n_seeds: int,
    max_workers: int = 0,
) -> EvalResult:
    """Run angles_deg x n_seeds trials in parallel; aggregate to EvalResult.

    ``max_workers=0`` -> use ``cpu_count()-1`` worker processes.
    ``max_workers=1`` -> run sequentially in this process (for debugging).
    """
    placer_seed = SEED_BASE + (_hash_param_vector(params.values) & 0xFFFF)
    t0 = time.time()
    if max_workers == 1:
        # Sequential mode: keep cell + bundle in this process.
        results: list[TrialResult] = []
        cell, bundle = _worker_prepare(
            params=params,
            placer_seed=placer_seed,
        )
        for angle in angles_deg:
            for s in range(n_seeds):
                seed = SEED_BASE + s * 10_007 + int(angle) * 13
                results.append(
                    run_one_trial(
                        cell=cell,
                        bundle=bundle,
                        direction_deg=float(angle),
                        seed=seed,
                    )
                )
    else:
        if max_workers == 0:
            max_workers = max(1, (cpu_count() or 4) - 1)
        results = []
        with ProcessPoolExecutor(max_workers=max_workers) as ex:
            futures = []
            for angle in angles_deg:
                for s in range(n_seeds):
                    seed = SEED_BASE + s * 10_007 + int(angle) * 13
                    futures.append(
                        ex.submit(
                            _worker_run_trial,
                            params_values=params.values,
                            direction_deg=float(angle),
                            seed=seed,
                            placer_seed=placer_seed,
                        )
                    )
            for f in as_completed(futures):
                results.append(f.result())

    summary = _summarise_trials(results=results)
    return EvalResult(
        dsi=summary.dsi,
        pd_rate_hz=summary.pd_rate_hz,
        n_trials=summary.n_trials,
        n_errors=summary.n_errors,
        elapsed_s=time.time() - t0,
    )


# ---------------------------------------------------------------------------
# CLI for smoke tests.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-seeds", type=int, default=2)
    parser.add_argument("--n-directions", type=int, default=2)
    parser.add_argument("--max-workers", type=int, default=1)
    args = parser.parse_args()

    pv = ParameterVector.default()
    angles = tuple(range(0, 360, 360 // args.n_directions))[: args.n_directions]
    print(f"Running {len(angles)} dir x {args.n_seeds} seeds at workers={args.max_workers}")
    print(f"Default param vector: {pv.values}")

    res = evaluate_parameter_vector(
        params=pv,
        angles_deg=angles,
        n_seeds=args.n_seeds,
        max_workers=args.max_workers,
    )
    print(
        f"DSI={res.dsi:.3f}  PD_rate_hz={res.pd_rate_hz:.2f}  "
        f"n_trials={res.n_trials}  n_errors={res.n_errors}  elapsed={res.elapsed_s:.1f}s"
    )
    _ = C24
