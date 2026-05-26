"""68-d joint evaluator for the t0129 NSGA-II run.

t0129 forks the t0126 evaluator with three behavioural changes:

* SIGNED antipodal DSI replaces vector-sum DSI:
  ``DSI = (R_PD - R_ND) / (R_PD + R_ND)`` in range ``[-1, 1]``. Reversed
  preference (R_ND > R_PD) becomes a detectable negative value rather
  than collapsing to a non-negative magnitude. F vector becomes
  ``[-dsi_signed, +atp_per_spike_molecules]`` (DSI still maximised).
* Real per-direction firing rates: ``pd_rate_hz`` and ``nd_rate_hz``
  exposed as named scalar fields on ``CellEvalResult``, both computed
  from actual per-direction spike counts. No placeholder values.
* Per-cell parameter dump: ``_append_cell_params`` writes one JSONL row
  per evaluated cell to a path captured at
  ``BedBV3MorphProblem.__init__`` time (pickled into workers). Replaces
  the env-var-driven ``_append_cell_trace`` that silently dropped data
  when workers did not inherit the env var.

MI_count_bits remains computed and stored on ``CellEvalResult`` as a
TRACKED DIAGNOSTIC (free since t0123 added the estimator). It does NOT
enter the F vector.
"""

from __future__ import annotations

import json
import multiprocessing as _mp
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from pymoo.core.problem import ElementwiseProblem

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
    MorphologyResult,
)
from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code import (
    bootstrap as _bootstrap,  # noqa: F401
)
from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.atp_per_spike import (
    AtpPerApResult,
    compute_atp_per_ap,
    compute_atp_per_spike,
    compute_compartment_breakdown,
    detect_ap_windows,
)
from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.constants_electrophys import (
    AP_THRESHOLD_MV,
    CELSIUS_DEG_C,
    DT_MS,
    PD_DIRECTION_DEG,
    RHO_CORRELATED,
    SEED_BASE,
    STABILITY_PEAK_VM_MAX_MV,
    STABILITY_PEAK_VM_MIN_MV,
    STEPS_PER_MS,
    TSTOP_MS,
    V_INIT_MV,
    ParameterVector,
)
from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.constants_morphology import (
    LOWER_BOUNDS_68,
    N_DIRECTIONS,
    N_EVAL_SEEDS,
    UPPER_BOUNDS_68,
    WORST_CASE_ATP_PER_SPIKE,
    WORST_CASE_DSI,
    WORST_CASE_MI_BITS,
    WORST_CASE_PD_RATE_HZ,
    WORST_CASE_ROBUSTNESS,
)
from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.generator_wrapper import (
    _LIVE_CELLS,
    build_cell,
    hash_morphology_vector,
    morphology_params_from_vector,
    split_68d_vector,
)
from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.mi_estimator import (
    compute_mi_count_bits,
)
from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.trial_helpers import (
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
    eval_seed_index: int  # which of the N_EVAL_SEEDS this trial belongs to
    spike_count: int
    peak_mv: float
    error: str | None
    atp_per_ap_results: tuple[AtpPerApResult, ...] = ()
    spike_times_ms: tuple[float, ...] = ()


@dataclass(frozen=True, slots=True)
class CellEvalResult:
    # Optimised diagnostics (MI inherited from t0123; not in F).
    mi_count_bits: float
    atp_per_spike_molecules: float
    # Per-AP mean and per-compartment breakdown for downstream analysis.
    atp_per_ap_molecules: float
    atp_per_ap_compartment_breakdown: dict[str, float]
    # Per-direction firing rates for downstream Niven plots / Pareto chart.
    firing_hz_per_dir: dict[str, float]
    # t0129: signed antipodal DSI in [-1, 1]. Replaces t0126 dsi_vector_sum.
    dsi_signed: float
    # Real per-direction firing rates from actual spike counts (t0129).
    pd_rate_hz: float
    nd_rate_hz: float
    robustness: float
    # Bookkeeping.
    n_trials: int
    n_errors: int
    elapsed_s: float
    is_unstable: bool
    peak_vm_mv: float
    silence_failed: bool


# DSI silence guard threshold (S-0102-01, REQ-3). Retained from t0122.
SILENCE_SPIKE_COUNT_THRESHOLD: int = 10

# t0122 -> t0123 inherits the tightened silence guard at pd_spikes_sum < 3.
SILENCE_PD_SPIKES_THRESHOLD: int = 3


# Worker-process global cache.
_WORKER_CELL: MorphologyResult | None = None
_WORKER_BUNDLE: SynapseBundle | None = None
_WORKER_MORPH_HASH: int | None = None
_WORKER_ELECTROPHYS_HASH: int | None = None


def _ensure_worker_cell(*, morph_params: MorphologyParams, morph_hash: int) -> MorphologyResult:
    """Build or reuse the worker cell for the given morphology vector."""
    global _WORKER_CELL, _WORKER_MORPH_HASH, _WORKER_BUNDLE, _WORKER_ELECTROPHYS_HASH
    if _WORKER_CELL is not None and morph_hash == _WORKER_MORPH_HASH:
        return _WORKER_CELL
    from neuron import h  # type: ignore[import-not-found]

    _WORKER_CELL = build_cell(h=h, morph_params=morph_params)
    _LIVE_CELLS.append(_WORKER_CELL)
    _WORKER_MORPH_HASH = morph_hash
    _WORKER_BUNDLE = None
    _WORKER_ELECTROPHYS_HASH = None
    return _WORKER_CELL


def _ensure_synapse_bundle(
    *,
    cell: MorphologyResult,
    electrophys_params: ParameterVector,
    placer_seed: int,
    electrophys_hash: int,
) -> SynapseBundle:
    """Apply electrophys + (re)build the synapse bundle if hash changed."""
    global _WORKER_BUNDLE, _WORKER_ELECTROPHYS_HASH
    if _WORKER_BUNDLE is not None and electrophys_hash == _WORKER_ELECTROPHYS_HASH:
        return _WORKER_BUNDLE
    apply_parameter_vector(cell=cell, params=electrophys_params)  # type: ignore[arg-type]
    _WORKER_BUNDLE = setup_synapses_parametric(
        cell=cell,  # type: ignore[arg-type]
        n_ach=electrophys_params.n_ach,
        n_gaba=electrophys_params.n_gaba,
        rho_0_ach=electrophys_params.rho0_ach,
        lambda_ach_um=electrophys_params.lambda_ach_um,
        rho_0_gaba=electrophys_params.rho0_gaba,
        lambda_gaba_um=electrophys_params.lambda_gaba_um,
        w_ach_us=electrophys_params.w_ach_us,
        w_gaba_us=electrophys_params.w_gaba_us,
        placer_seed=placer_seed,
        gnmda_dend=electrophys_params.gnmda_dend,
        mg_conc_mm=electrophys_params.mg_conc_mm,
        voff_nmda=electrophys_params.voff_nmda,
    )
    _WORKER_ELECTROPHYS_HASH = electrophys_hash
    return _WORKER_BUNDLE


def _run_one_trial(
    *,
    cell: MorphologyResult,
    bundle: SynapseBundle,
    direction_deg: float,
    seed: int,
    eval_seed_index: int = 0,
    record_ina_for_atp: bool = True,
) -> TrialResult:
    h = cell.h
    try:
        from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.recorder import (
            attach_ina_recorders_for_atp,
        )

        n_ach: int = len(bundle.syns_ach)
        n_gaba: int = len(bundle.syns_gaba)
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
        v_vec.record(cell.soma(0.5)._ref_v, DT_MS)
        t_vec = h.Vector()
        t_vec.record(h._ref_t, DT_MS)
        ina_recorders = None
        if record_ina_for_atp:
            ina_recorders = attach_ina_recorders_for_atp(h=h, cell=cell)
        h.celsius = CELSIUS_DEG_C
        h.dt = DT_MS
        h.steps_per_ms = STEPS_PER_MS
        h.v_init = V_INIT_MV
        h.tstop = TSTOP_MS
        h.finitialize(V_INIT_MV)
        _ = fih
        h.run()
        v_arr = np.array(v_vec.to_python(), dtype=np.float64)
        t_arr = np.array(t_vec.to_python(), dtype=np.float64)
        if not np.all(np.isfinite(v_arr)):
            return TrialResult(
                direction_deg=direction_deg,
                seed=seed,
                eval_seed_index=eval_seed_index,
                spike_count=0,
                peak_mv=float("nan"),
                error="non_finite_voltage",
            )
        spikes = _count_spikes(v_arr, AP_THRESHOLD_MV)
        peak = float(v_arr.max()) if v_arr.size > 0 else float("nan")
        # Detect AP windows from somatic Vm and (optionally) integrate
        # inward Na charge per AP per compartment for ATP.
        atp_per_ap_results: tuple[AtpPerApResult, ...] = ()
        spike_times_ms_tuple: tuple[float, ...] = ()
        if ina_recorders is not None:
            ap_windows = detect_ap_windows(t_ms=t_arr, v_soma_mv=v_arr)
            spike_times_ms_tuple = tuple(float(w.t_peak_ms) for w in ap_windows)
            ina_by_section: dict[str, list[tuple[NDArray[np.float64], float]]] = {
                "soma": [
                    (np.array(v.to_python(), dtype=np.float64), area)
                    for v, area in ina_recorders.soma_ina
                ],
                "ais": [
                    (np.array(v.to_python(), dtype=np.float64), area)
                    for v, area in ina_recorders.ais_ina
                ],
                "dendrites": [
                    (np.array(v.to_python(), dtype=np.float64), area)
                    for v, area in ina_recorders.dend_ina
                ],
            }
            results_list = compute_atp_per_ap(
                t_ms=t_arr,
                ina_by_section=ina_by_section,
                ap_windows=ap_windows,
            )
            atp_per_ap_results = tuple(results_list)
        return TrialResult(
            direction_deg=direction_deg,
            seed=seed,
            eval_seed_index=eval_seed_index,
            spike_count=spikes,
            peak_mv=peak,
            error=None,
            atp_per_ap_results=atp_per_ap_results,
            spike_times_ms=spike_times_ms_tuple,
        )
    except (RuntimeError, ValueError, ArithmeticError) as exc:
        return TrialResult(
            direction_deg=direction_deg,
            seed=seed,
            eval_seed_index=eval_seed_index,
            spike_count=0,
            peak_mv=float("nan"),
            error=f"{type(exc).__name__}: {exc}",
        )


def _signed_antipodal_dsi(*, spike_counts_per_dir: dict[float, list[int]]) -> float:
    """Signed antipodal DSI = (R_PD - R_ND) / (R_PD + R_ND), range [-1, 1].

    Assumes exactly two antipodal directions: PD at ``PD_DIRECTION_DEG``
    (= 0.0) and ND at ``PD_DIRECTION_DEG + 180.0``. Returns
    ``WORST_CASE_DSI = -1.0`` when the denominator is zero (silence
    sentinel reused; -1.0 sits at the lower bound of the signed range).
    """
    pd_dir: float = PD_DIRECTION_DEG
    nd_dir: float = (PD_DIRECTION_DEG + 180.0) % 360.0
    pd_counts: list[int] = spike_counts_per_dir.get(pd_dir, [])
    nd_counts: list[int] = spike_counts_per_dir.get(nd_dir, [])
    r_pd: float = float(np.mean(pd_counts)) if len(pd_counts) > 0 else 0.0
    r_nd: float = float(np.mean(nd_counts)) if len(nd_counts) > 0 else 0.0
    denom: float = r_pd + r_nd
    if denom <= 0.0:
        return WORST_CASE_DSI
    return (r_pd - r_nd) / denom


def _summarise_trials(
    *,
    results: list[TrialResult],
    n_seeds: int,
    n_directions: int,
) -> CellEvalResult:
    spike_counts_per_dir: dict[float, list[int]] = {}
    n_errors = 0
    peak_vm_mv: float = float("-inf")
    is_unstable = False
    pd_spikes: list[int] = []
    nd_spikes: list[int] = []
    seed_to_dir_counts: dict[int, dict[float, int]] = {}
    direction_labels_list: list[int] = []
    spike_counts_flat: list[int] = []
    all_atp_per_ap_results: list[AtpPerApResult] = []
    all_directions: list[float] = []
    nd_direction_deg: float = (PD_DIRECTION_DEG + 180.0) % 360.0
    for r in results:
        if r.error is not None:
            n_errors += 1
            continue
        if r.peak_mv == r.peak_mv:  # not NaN
            if r.peak_mv > peak_vm_mv:
                peak_vm_mv = r.peak_mv
            if r.peak_mv < STABILITY_PEAK_VM_MIN_MV or r.peak_mv > STABILITY_PEAK_VM_MAX_MV:
                is_unstable = True
        spike_counts_per_dir.setdefault(r.direction_deg, []).append(r.spike_count)
        seed_to_dir_counts.setdefault(r.eval_seed_index, {})[r.direction_deg] = r.spike_count
        if abs(r.direction_deg - PD_DIRECTION_DEG) < 1e-6:
            pd_spikes.append(r.spike_count)
        if abs(r.direction_deg - nd_direction_deg) < 1e-6:
            nd_spikes.append(r.spike_count)
        if r.direction_deg not in all_directions:
            all_directions.append(r.direction_deg)
        direction_labels_list.append(all_directions.index(r.direction_deg))
        spike_counts_flat.append(int(r.spike_count))
        all_atp_per_ap_results.extend(r.atp_per_ap_results)

    if n_errors >= len(results) // 2 or len(spike_counts_per_dir) == 0:
        return CellEvalResult(
            mi_count_bits=WORST_CASE_MI_BITS,
            atp_per_spike_molecules=WORST_CASE_ATP_PER_SPIKE,
            atp_per_ap_molecules=WORST_CASE_ATP_PER_SPIKE,
            atp_per_ap_compartment_breakdown={
                "soma": 0.0,
                "ais": 0.0,
                "dendrites_total": 0.0,
            },
            firing_hz_per_dir={},
            dsi_signed=WORST_CASE_DSI,
            pd_rate_hz=WORST_CASE_PD_RATE_HZ,
            nd_rate_hz=WORST_CASE_PD_RATE_HZ,
            robustness=WORST_CASE_ROBUSTNESS,
            n_trials=len(results),
            n_errors=n_errors,
            elapsed_s=0.0,
            is_unstable=True,
            peak_vm_mv=peak_vm_mv if peak_vm_mv != float("-inf") else float("nan"),
            silence_failed=True,
        )

    pd_spikes_sum: int = int(sum(pd_spikes)) if len(pd_spikes) > 0 else 0
    silence_failed = pd_spikes_sum < SILENCE_PD_SPIKES_THRESHOLD

    if silence_failed:
        # t0129: per task_description.md silence-guard recipe, DSI = -1.0
        # for cells with R_PD < 3 spikes. Uses WORST_CASE_DSI sentinel so
        # the NSGA-II non-dominated sort rejects them.
        dsi_signed = WORST_CASE_DSI
    else:
        dsi_signed = _signed_antipodal_dsi(spike_counts_per_dir=spike_counts_per_dir)
    pd_rate_hz = float(np.mean(pd_spikes)) / (TSTOP_MS / 1000.0) if pd_spikes else 0.0
    nd_rate_hz = float(np.mean(nd_spikes)) / (TSTOP_MS / 1000.0) if nd_spikes else 0.0

    # Per-seed DSI for robustness (kept as a diagnostic). Uses the same
    # signed antipodal helper, then aggregates by coefficient of variation
    # of the absolute signed values (sign-aware mean would not be
    # meaningful when a cell genuinely flips direction across seeds).
    pd_seed_dsis: list[float] = []
    for _seed, dir_counts in seed_to_dir_counts.items():
        if len(dir_counts) < 2:
            continue
        per_seed_dsi = _signed_antipodal_dsi(
            spike_counts_per_dir={k: [v] for k, v in dir_counts.items()},
        )
        pd_seed_dsis.append(per_seed_dsi)
    if len(pd_seed_dsis) >= 2:
        mean_abs_dsi = float(np.mean([abs(x) for x in pd_seed_dsis]))
        std_dsi = float(np.std(pd_seed_dsis))
        if mean_abs_dsi <= 1e-6:
            robustness = WORST_CASE_ROBUSTNESS
        else:
            cv = std_dsi / mean_abs_dsi
            robustness = float(1.0 / (1.0 + cv))
    else:
        robustness = WORST_CASE_ROBUSTNESS

    # Per-direction firing rates in Hz (mean spikes / 1.4 s).
    firing_hz_per_dir: dict[str, float] = {}
    for direction_deg, counts in spike_counts_per_dir.items():
        label = f"dir_{int(round(direction_deg))}"
        firing_hz_per_dir[label] = float(np.mean(counts)) / (TSTOP_MS / 1000.0)

    # Optimised objectives.
    if silence_failed:
        mi_count_bits = WORST_CASE_MI_BITS
        atp_per_spike_molecules = WORST_CASE_ATP_PER_SPIKE
        atp_per_ap_molecules = WORST_CASE_ATP_PER_SPIKE
        compartment_breakdown = {"soma": 0.0, "ais": 0.0, "dendrites_total": 0.0}
    else:
        mi_count_bits = compute_mi_count_bits(
            direction_labels=np.array(direction_labels_list, dtype=np.int_),
            spike_counts=np.array(spike_counts_flat, dtype=np.int_),
            n_bins=4,
        )
        atp_per_spike_molecules = compute_atp_per_spike(
            atp_per_ap_results=all_atp_per_ap_results,
        )
        if not np.isfinite(atp_per_spike_molecules):
            atp_per_spike_molecules = WORST_CASE_ATP_PER_SPIKE
            atp_per_ap_molecules = WORST_CASE_ATP_PER_SPIKE
            silence_failed = True
        else:
            atp_per_ap_molecules = atp_per_spike_molecules
        compartment_breakdown = compute_compartment_breakdown(
            atp_per_ap_results=all_atp_per_ap_results,
        )

    return CellEvalResult(
        mi_count_bits=mi_count_bits,
        atp_per_spike_molecules=atp_per_spike_molecules,
        atp_per_ap_molecules=atp_per_ap_molecules,
        atp_per_ap_compartment_breakdown=compartment_breakdown,
        firing_hz_per_dir=firing_hz_per_dir,
        dsi_signed=dsi_signed,
        pd_rate_hz=pd_rate_hz,
        nd_rate_hz=nd_rate_hz,
        robustness=robustness,
        n_trials=len(results),
        n_errors=n_errors,
        elapsed_s=0.0,
        is_unstable=is_unstable,
        peak_vm_mv=peak_vm_mv,
        silence_failed=silence_failed,
    )


def evaluate_68d_vector(
    *,
    vector_68d: NDArray[np.float64],
    eval_seeds: list[int] | None = None,
    n_directions: int = N_DIRECTIONS,
) -> CellEvalResult:
    """Evaluate one 68-d vector. SINGLE-WORKER, SEQUENTIAL -- caller parallelises by cell."""
    t0 = time.time()
    electrophys_54d, morph_14d = split_68d_vector(vector_68d=vector_68d)
    morph_hash = hash_morphology_vector(vector=morph_14d)
    electrophys_hash = hash(electrophys_54d.tobytes())
    morph_params = morphology_params_from_vector(morph_vector_14d=morph_14d)
    electrophys_params = ParameterVector(values=electrophys_54d)
    placer_seed = SEED_BASE + (electrophys_hash & 0xFFFF)

    try:
        cell = _ensure_worker_cell(morph_params=morph_params, morph_hash=morph_hash)
        bundle = _ensure_synapse_bundle(
            cell=cell,
            electrophys_params=electrophys_params,
            placer_seed=placer_seed,
            electrophys_hash=electrophys_hash,
        )
    except (RuntimeError, ValueError, AssertionError, ArithmeticError):
        elapsed = time.time() - t0
        return CellEvalResult(
            mi_count_bits=WORST_CASE_MI_BITS,
            atp_per_spike_molecules=WORST_CASE_ATP_PER_SPIKE,
            atp_per_ap_molecules=WORST_CASE_ATP_PER_SPIKE,
            atp_per_ap_compartment_breakdown={
                "soma": 0.0,
                "ais": 0.0,
                "dendrites_total": 0.0,
            },
            firing_hz_per_dir={},
            dsi_signed=WORST_CASE_DSI,
            pd_rate_hz=WORST_CASE_PD_RATE_HZ,
            nd_rate_hz=WORST_CASE_PD_RATE_HZ,
            robustness=WORST_CASE_ROBUSTNESS,
            n_trials=0,
            n_errors=1,
            elapsed_s=elapsed,
            is_unstable=True,
            peak_vm_mv=float("nan"),
            silence_failed=True,
        )

    if eval_seeds is None:
        ss = np.random.SeedSequence(42)
        eval_seeds = [int(x.generate_state(1)[0]) for x in ss.spawn(N_EVAL_SEEDS)]

    angles_deg: list[float] = [float(d) * (360.0 / n_directions) for d in range(n_directions)]
    results: list[TrialResult] = []
    for eval_seed_index, seed in enumerate(eval_seeds):
        for direction_deg in angles_deg:
            seed_int = int(seed) % (2**31 - 1) + int(direction_deg) * 13
            results.append(
                _run_one_trial(
                    cell=cell,
                    bundle=bundle,
                    direction_deg=direction_deg,
                    seed=seed_int,
                    eval_seed_index=eval_seed_index,
                    record_ina_for_atp=True,
                )
            )

    summary = _summarise_trials(
        results=results,
        n_seeds=len(eval_seeds),
        n_directions=n_directions,
    )
    return CellEvalResult(
        mi_count_bits=summary.mi_count_bits,
        atp_per_spike_molecules=summary.atp_per_spike_molecules,
        atp_per_ap_molecules=summary.atp_per_ap_molecules,
        atp_per_ap_compartment_breakdown=summary.atp_per_ap_compartment_breakdown,
        firing_hz_per_dir=summary.firing_hz_per_dir,
        dsi_signed=summary.dsi_signed,
        pd_rate_hz=summary.pd_rate_hz,
        nd_rate_hz=summary.nd_rate_hz,
        robustness=summary.robustness,
        n_trials=summary.n_trials,
        n_errors=summary.n_errors,
        elapsed_s=time.time() - t0,
        is_unstable=summary.is_unstable,
        peak_vm_mv=summary.peak_vm_mv,
        silence_failed=summary.silence_failed,
    )


def _worker_evaluate_vector(
    *, vector_68d: NDArray[np.float64], eval_seeds: list[int]
) -> CellEvalResult:
    try:
        return evaluate_68d_vector(vector_68d=vector_68d, eval_seeds=eval_seeds)
    except (RuntimeError, ValueError, AssertionError, ArithmeticError):
        return CellEvalResult(
            mi_count_bits=WORST_CASE_MI_BITS,
            atp_per_spike_molecules=WORST_CASE_ATP_PER_SPIKE,
            atp_per_ap_molecules=WORST_CASE_ATP_PER_SPIKE,
            atp_per_ap_compartment_breakdown={
                "soma": 0.0,
                "ais": 0.0,
                "dendrites_total": 0.0,
            },
            firing_hz_per_dir={},
            dsi_signed=WORST_CASE_DSI,
            pd_rate_hz=WORST_CASE_PD_RATE_HZ,
            nd_rate_hz=WORST_CASE_PD_RATE_HZ,
            robustness=WORST_CASE_ROBUSTNESS,
            n_trials=0,
            n_errors=1,
            elapsed_s=0.0,
            is_unstable=True,
            peak_vm_mv=float("nan"),
            silence_failed=True,
        )


def _append_cell_params(
    *,
    sink_path: Path,
    lock: Any,
    row: dict[str, Any],
) -> None:
    """Append one JSON line per cell to the t0129 cell_params sink.

    ``sink_path`` and ``lock`` are captured at problem-construction time
    and pickled into worker processes (no env var dependency). Failures
    are swallowed and logged; we never want a sink write to abort a
    NEURON simulation that already completed successfully.
    """
    try:
        sink_path.parent.mkdir(parents=True, exist_ok=True)
        line: str = json.dumps(row) + "\n"
        with lock, sink_path.open("a", encoding="utf-8") as f:
            f.write(line)
    except (OSError, RuntimeError):
        traceback.print_exc()


class BedBV3MorphProblem(ElementwiseProblem):
    """68-d joint problem for pymoo NSGA-II (t0129 signed-DSI + ATP)."""

    def __init__(
        self,
        *,
        eval_seeds: list[int],
        cell_params_path: Path,
        elementwise_runner: Any | None = None,
    ) -> None:
        kwargs: dict[str, Any] = {
            "n_var": 68,
            "n_obj": 2,
            "n_ieq_constr": 0,
            "xl": LOWER_BOUNDS_68,
            "xu": UPPER_BOUNDS_68,
        }
        if elementwise_runner is not None:
            kwargs["elementwise_runner"] = elementwise_runner
        super().__init__(**kwargs)
        self._eval_seeds = eval_seeds
        # t0129: cell_params sink captured at construction time. Use a
        # Manager().Lock() so it pickles into worker processes; falls
        # back to a local threading.Lock if a Manager cannot be spawned
        # (single-process smoke gate path).
        self._cell_params_path: Path = cell_params_path
        try:
            manager: Any = _mp.Manager()
            self._cell_params_lock: Any = manager.Lock()
        except (OSError, RuntimeError):
            from threading import Lock as _ThreadingLock

            self._cell_params_lock = _ThreadingLock()
        # Generation index, set externally by a NSGA-II callback before
        # each generation's _evaluate sweep. Default -1 covers Phase A.
        self._current_gen: int = -1
        # Cell-index counter resets per generation by the same callback.
        self._cell_idx_in_gen: int = 0

    def _evaluate(self, x: NDArray[np.float64], out: dict[str, Any], *args, **kwargs) -> None:
        vec = np.asarray(x, dtype=np.float64)
        try:
            result = evaluate_68d_vector(vector_68d=vec, eval_seeds=self._eval_seeds)
            # t0129 F vector: 2 objectives (signed DSI maximised so
            # negated; ATP_per_spike minimised so POSITIVE).
            out["F"] = np.array(
                [-result.dsi_signed, +result.atp_per_spike_molecules],
                dtype=np.float64,
            )
            row: dict[str, Any] = {
                "gen": int(self._current_gen),
                "cell_idx": int(self._cell_idx_in_gen),
                "param_vector": [float(v) for v in vec],
                "dsi_signed": float(result.dsi_signed),
                "atp_per_spike_molecules": float(result.atp_per_spike_molecules),
                "pd_rate_hz": float(result.pd_rate_hz),
                "nd_rate_hz": float(result.nd_rate_hz),
                "silence_failed": bool(result.silence_failed),
                "n_errors": int(result.n_errors),
            }
            _append_cell_params(
                sink_path=self._cell_params_path,
                lock=self._cell_params_lock,
                row=row,
            )
            self._cell_idx_in_gen += 1
        except Exception:  # noqa: BLE001
            traceback.print_exc()
            out["F"] = np.array(
                [-WORST_CASE_DSI, +WORST_CASE_ATP_PER_SPIKE],
                dtype=np.float64,
            )
