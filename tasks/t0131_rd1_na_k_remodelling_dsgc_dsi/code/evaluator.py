"""Trial-level evaluator for the Bed B DSGC with optional s_Na/s_K scaling and tonic bias.

Adapted from t0129 ``evaluator.py`` (signed antipodal DSI protocol). Changes: pymoo / MI / ATP
removed; scale factors applied after ``apply_parameter_vector``; optional soma bias IClamp; DSI
rule moved to ``dsi_rules.py`` (None instead of the -1.0 sentinel); each trial is an independent
picklable job so batches are resumable and parallel; the cell is rebuilt (and the previous one
deleted) whenever (cell, scales, arm) changes; the synapse placer seed uses crc32 instead of the
process-randomised ``hash`` used in t0129.
"""

import time
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import SynapseBundle
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyResult,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.bias import (
    BiasSpec,
    attach_bias,
    detach_bias,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_factory import (
    build_scaled,
    dispose_all_cells,
    get_h,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    AP_THRESHOLD_MV,
    CELSIUS_DEG_C,
    DT_MS,
    EVAL_SEED_SS,
    N_EVAL_SEEDS,
    PULSE_CENTERS_MS,
    PULSE_SIGMA_MS,
    RHO_CORRELATED,
    STEPS_PER_MS,
    V_INIT_MV,
    ScalingArm,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.scaling import ChannelScales
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.trial_helpers_private import (
    BASE_ACH_PROB,
    RATE_DT_MS,
    bar_arrival_times,
    gaba_prob_for_direction,
    rates_to_events,
    rates_with_ar2_noise,
    rates_with_envelope,
)

MODE_BAR: str = "bar"
MODE_PULSE: str = "pulse"


@dataclass(frozen=True, slots=True)
class TrialJob:
    job_key: str
    cell_id: str
    vector_68d: list[float]
    s_na: float
    s_k: float
    arm: str
    bias: BiasSpec | None
    mode: str
    direction_deg: float
    seed_index: int
    seed: int
    exc_scale: float
    tstop_ms: float


@dataclass(frozen=True, slots=True)
class TrialOutcome:
    job_key: str
    spike_count: int
    spike_times_ms: list[float]
    peak_mv: float | None
    error: str | None
    elapsed_s: float


@dataclass(slots=True)
class WorkerState:
    cache_key: str | None
    cell: MorphologyResult | None
    bundle: SynapseBundle | None
    base_w_ach: list[float]
    base_w_nmda: list[float]


@dataclass(frozen=True, slots=True)
class EventLists:
    ach: list[list[float]]
    gaba: list[list[float]]


_STATE: WorkerState = WorkerState(
    cache_key=None, cell=None, bundle=None, base_w_ach=[], base_w_nmda=[]
)


def worker_init() -> None:
    get_h()


def eval_seeds() -> list[int]:
    ss = np.random.SeedSequence(EVAL_SEED_SS)
    return [int(x.generate_state(1)[0]) for x in ss.spawn(N_EVAL_SEEDS)]


def trial_seed(*, base_seed: int, direction_deg: float) -> int:
    return int(base_seed) % (2**31 - 1) + int(direction_deg) * 13


def reset_worker_state() -> None:
    global _STATE
    dispose_all_cells()
    _STATE = WorkerState(cache_key=None, cell=None, bundle=None, base_w_ach=[], base_w_nmda=[])


def _ensure_state(*, job: TrialJob) -> None:
    global _STATE
    key = f"{job.cell_id}|{job.s_na:.6f}|{job.s_k:.6f}|{job.arm}"
    if _STATE.cache_key == key and _STATE.bundle is not None:
        return
    reset_worker_state()
    built = build_scaled(
        vector_68d=job.vector_68d,
        scales=ChannelScales(s_na=job.s_na, s_k=job.s_k, arm=ScalingArm(job.arm)),
        with_synapses=True,
    )
    assert built.bundle is not None, "synapse bundle built"
    _STATE = WorkerState(
        cache_key=key,
        cell=built.cell,
        bundle=built.bundle,
        base_w_ach=[float(nc.weight[0]) for nc in built.bundle.ncs_ach],
        base_w_nmda=[float(nc.weight[0]) for nc in built.bundle.ncs_nmda],
    )


def spike_times_from_trace(
    *, t_ms: NDArray[np.float64], v_mv: NDArray[np.float64], threshold_mv: float
) -> list[float]:
    above = v_mv > threshold_mv
    idx = np.nonzero((~above[:-1]) & above[1:])[0]
    return [float(t_ms[i + 1]) for i in idx]


def pulse_envelope(*, n_bins: int, dt_ms: float) -> NDArray[np.float64]:
    t = np.arange(n_bins, dtype=np.float64) * dt_ms
    env = np.zeros(n_bins, dtype=np.float64)
    for c in PULSE_CENTERS_MS:
        env += np.exp(-0.5 * ((t - c) / PULSE_SIGMA_MS) ** 2)
    peak = float(env.max())
    assert peak > 0.0, "pulse envelope has positive peak"
    return env / peak


def _make_events(*, job: TrialJob, cell: MorphologyResult, bundle: SynapseBundle) -> EventLists:
    n_ach = len(bundle.syns_ach)
    n_gaba = len(bundle.syns_gaba)
    n_bins = int(np.ceil(job.tstop_ms / RATE_DT_MS))
    rng = np.random.default_rng(job.seed + 1_000_003)
    if job.mode == MODE_BAR:
        arr_ach = bar_arrival_times(
            syn_xy=bundle.syn_xy_ach, origin_xy=cell.origin_xy, direction_deg=job.direction_deg
        )
        arr_gaba = bar_arrival_times(
            syn_xy=bundle.syn_xy_gaba, origin_xy=cell.origin_xy, direction_deg=job.direction_deg
        )
        ach_rates, _ = rates_with_ar2_noise(
            n_syn=n_ach,
            n_bins=n_bins,
            rate_dt_ms=RATE_DT_MS,
            arrival_times_ms=arr_ach,
            rho=RHO_CORRELATED,
            seed=job.seed,
        )
        _, gaba_rates = rates_with_ar2_noise(
            n_syn=n_gaba,
            n_bins=n_bins,
            rate_dt_ms=RATE_DT_MS,
            arrival_times_ms=arr_gaba,
            rho=RHO_CORRELATED,
            seed=job.seed + 7919,
        )
        gaba_prob = gaba_prob_for_direction(direction_deg=job.direction_deg)
    else:
        env = pulse_envelope(n_bins=n_bins, dt_ms=RATE_DT_MS)
        ach_rates, _ = rates_with_envelope(
            n_syn=n_ach, n_bins=n_bins, envelope=env, rho=RHO_CORRELATED, seed=job.seed
        )
        gaba_rates = np.zeros((n_gaba, n_bins), dtype=np.float64)
        gaba_prob = 0.0
    ach_events = rates_to_events(
        rates_hz=ach_rates,
        release_prob=np.full(n_ach, BASE_ACH_PROB, dtype=np.float64),
        rate_dt_ms=RATE_DT_MS,
        rng=rng,
    )
    gaba_events = rates_to_events(
        rates_hz=gaba_rates,
        release_prob=np.full(n_gaba, gaba_prob, dtype=np.float64),
        rate_dt_ms=RATE_DT_MS,
        rng=rng,
    )
    return EventLists(ach=ach_events, gaba=gaba_events)


def run_trial_job(job: TrialJob) -> TrialOutcome:
    t0 = time.time()
    try:
        _ensure_state(job=job)
        h = get_h()
        cell = _STATE.cell
        bundle = _STATE.bundle
        assert cell is not None and bundle is not None, "worker state built"
        for nc, w in zip(bundle.ncs_ach, _STATE.base_w_ach, strict=True):
            nc.weight[0] = w * job.exc_scale
        for nc, w in zip(bundle.ncs_nmda, _STATE.base_w_nmda, strict=True):
            nc.weight[0] = w * job.exc_scale
        events = _make_events(job=job, cell=cell, bundle=bundle)

        def _queue() -> None:
            for i, nc in enumerate(bundle.ncs_ach):
                for t in events.ach[i]:
                    if t < job.tstop_ms:
                        nc.event(t)
            for i, nc in enumerate(bundle.ncs_gaba):
                for t in events.gaba[i]:
                    if t < job.tstop_ms:
                        nc.event(t)

        fih = h.FInitializeHandler(_queue)
        v_vec = h.Vector()
        v_vec.record(cell.soma(0.5)._ref_v, DT_MS)
        t_vec = h.Vector()
        t_vec.record(h._ref_t, DT_MS)
        handles = None
        if job.bias is not None:
            handles = attach_bias(
                h=h, soma=cell.soma, bias=job.bias, tstop_ms=job.tstop_ms, dt_ms=DT_MS
            )
        h.celsius = CELSIUS_DEG_C
        h.dt = DT_MS
        h.steps_per_ms = STEPS_PER_MS
        h.v_init = V_INIT_MV
        h.tstop = job.tstop_ms
        h.finitialize(V_INIT_MV)
        _ = fih
        h.run()
        if handles is not None:
            detach_bias(handles=handles)
        v_arr = np.array(v_vec.to_python(), dtype=np.float64)
        t_arr = np.array(t_vec.to_python(), dtype=np.float64)
        if not np.all(np.isfinite(v_arr)):
            return TrialOutcome(
                job_key=job.job_key,
                spike_count=0,
                spike_times_ms=[],
                peak_mv=None,
                error="non_finite_voltage",
                elapsed_s=time.time() - t0,
            )
        times = spike_times_from_trace(t_ms=t_arr, v_mv=v_arr, threshold_mv=AP_THRESHOLD_MV)
        return TrialOutcome(
            job_key=job.job_key,
            spike_count=len(times),
            spike_times_ms=times,
            peak_mv=float(v_arr.max()),
            error=None,
            elapsed_s=time.time() - t0,
        )
    except (RuntimeError, ValueError, ArithmeticError, AssertionError) as exc:
        reset_worker_state()
        return TrialOutcome(
            job_key=job.job_key,
            spike_count=0,
            spike_times_ms=[],
            peak_mv=None,
            error=f"{type(exc).__name__}: {exc}",
            elapsed_s=time.time() - t0,
        )
