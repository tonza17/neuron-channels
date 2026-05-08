"""Run a single PD bar trial and return the soma Vm trace.

Mirrors ``tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver.run_one_trial``
but exposes the full voltage vector so the diagnostic can save a per-cell .npy
trace and compute peak Vm, time-to-peak, EPSP area, and spike count.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    AP_THRESHOLD_MV,
    CELSIUS_DEG_C,
    DT_MS,
    RHO_CORRELATED,
    STEPS_PER_MS,
    TSTOP_MS,
    V_INIT_MV,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import (
    BASE_ACH_PROB,
    RATE_DT_MS,
    SynapseBundle,
    _bar_arrival_times,
    _count_spikes,
    _gaba_prob_for_direction,
    _rates_to_events,
    _rates_with_ar2_noise,
)


@dataclass(frozen=True, slots=True)
class TraceResult:
    direction_deg: float
    seed: int
    spike_count: int
    peak_mv: float
    time_to_peak_ms: float
    epsp_area_mv_ms: float
    v_trace: NDArray[np.float64]
    error: str | None


def _epsp_area_above(*, v: NDArray[np.float64], floor_mv: float, dt_ms: float) -> float:
    """Trapezoidal area under the trace above ``floor_mv``, in mV-ms."""
    excess = np.maximum(v - floor_mv, 0.0)
    return float(np.trapezoid(excess, dx=dt_ms))


def run_one_trial_with_trace(
    *,
    cell: Any,
    bundle: SynapseBundle,
    direction_deg: float,
    seed: int,
    epsp_floor_mv: float = -70.0,
) -> TraceResult:
    """Run one bar trial on ``cell`` and return its soma Vm trace plus stats."""
    h = cell.h
    try:
        n_ach = int(len(bundle.syns_ach))
        n_gaba = int(len(bundle.syns_gaba))
        n_bins = int(np.ceil(TSTOP_MS / RATE_DT_MS))

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

        v_arr: NDArray[np.float64] = np.array(v_vec.to_python(), dtype=np.float64)
        if not np.all(np.isfinite(v_arr)):
            return TraceResult(
                direction_deg=direction_deg,
                seed=seed,
                spike_count=0,
                peak_mv=float("nan"),
                time_to_peak_ms=float("nan"),
                epsp_area_mv_ms=float("nan"),
                v_trace=v_arr,
                error="non_finite_voltage",
            )

        spikes = int(_count_spikes(v_arr, AP_THRESHOLD_MV))
        peak = float(v_arr.max()) if v_arr.size > 0 else float("nan")
        argmax = int(np.argmax(v_arr)) if v_arr.size > 0 else 0
        time_to_peak = float(argmax) * float(DT_MS)
        area = _epsp_area_above(v=v_arr, floor_mv=epsp_floor_mv, dt_ms=float(DT_MS))
        return TraceResult(
            direction_deg=direction_deg,
            seed=seed,
            spike_count=spikes,
            peak_mv=peak,
            time_to_peak_ms=time_to_peak,
            epsp_area_mv_ms=area,
            v_trace=v_arr,
            error=None,
        )
    except (RuntimeError, ValueError, ArithmeticError) as exc:
        return TraceResult(
            direction_deg=direction_deg,
            seed=seed,
            spike_count=0,
            peak_mv=float("nan"),
            time_to_peak_ms=float("nan"),
            epsp_area_mv_ms=float("nan"),
            v_trace=np.zeros(0, dtype=np.float64),
            error=f"{type(exc).__name__}: {exc}",
        )
