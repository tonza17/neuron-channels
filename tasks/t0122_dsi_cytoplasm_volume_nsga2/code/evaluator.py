"""68-d joint evaluator for the t0091 NSGA-II run (REQ-2, REQ-8, REQ-18).

Per-cell evaluation: split 68-d -> (54-d electrophys, 14-d morphology), build
or reuse a worker-cached cell via the t0092 patched generator (REQ-1), apply
the electrophys vector, run 16 directions x 5 seeds.

Objectives (minimised by pymoo, so we negate where positive is good):
* f0: -DSI vector-sum
* f1: -PD firing rate (Hz)
* f2: -robustness (inverse CV of DSI across seeds)

Worker cache key: (54-d electrophys hash, 14-d morphology hash). On morphology
hash change we rebuild the cell via `generator_wrapper.build_cell`. On
electrophys-only change we reuse the cached cell and re-run
`apply_parameter_vector`.
"""

from __future__ import annotations

import json
import os
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any

import numpy as np
from numpy.typing import NDArray
from pymoo.core.problem import ElementwiseProblem

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
    MorphologyResult,
)
from tasks.t0122_dsi_cytoplasm_volume_nsga2.code import (
    bootstrap as _bootstrap,  # noqa: F401
)
from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.constants_electrophys import (
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
from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.constants_morphology import (
    LOWER_BOUNDS_68,
    N_DIRECTIONS,
    N_EVAL_SEEDS,
    UPPER_BOUNDS_68,
    WORST_CASE_CYTOPLASM_VOLUME_UM3,
    WORST_CASE_DSI,
    WORST_CASE_PD_RATE_HZ,
    WORST_CASE_ROBUSTNESS,
)
from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.cytoplasm_volume import (
    compute_cytoplasm_volume_um3,
)
from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.generator_wrapper import (
    _LIVE_CELLS,
    build_cell,
    hash_morphology_vector,
    morphology_params_from_vector,
    split_68d_vector,
)
from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.trial_helpers import (
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


@dataclass(frozen=True, slots=True)
class CellEvalResult:
    dsi_vector_sum: float
    pd_rate_hz: float
    robustness: float
    n_trials: int
    n_errors: int
    elapsed_s: float
    is_unstable: bool
    peak_vm_mv: float
    # t0122 REQ-10: per-cell cytoplasm volume (sum of pi r^2 L over
    # soma + all dendrites + AIS). Units: um^3. Computed once per cell
    # immediately after _ensure_worker_cell builds the cell. Enters
    # NSGA-II selection as the SECOND objective via
    # ``BedBV3MorphProblem._evaluate`` with ``out["F"] = [-dsi,
    # +cytoplasm_volume_um3]`` (NOT negated because minimised).
    cytoplasm_volume_um3: float


# DSI silence guard threshold (S-0102-01, REQ-3).
# Retained for back-compat and for ``smoke_gate._check_3``; the actual
# guard inside ``_summarise_trials`` is now driven by
# ``SILENCE_PD_SPIKES_THRESHOLD`` -- t0122 REQ-11 tightened the threshold
# from ``total_mean_spikes < 10`` to ``pd_spikes_sum < 3``.
SILENCE_SPIKE_COUNT_THRESHOLD: int = 10


# t0122 REQ-10/REQ-19: per-cell side-channel JSONL trace.
# ``_evaluate`` writes one JSON line per cell to the trace path defined
# by the ``T0122_CELL_TRACE_JSONL`` env var. This is the load-bearing
# resume channel for downstream PD-rate / robustness / peak_vm recovery
# (the F vector only carries DSI + cytoplasm volume, so PD-rate is not
# otherwise available to the post-run pareto / asset builders). The
# trace is opened in append mode with a process-local lock to avoid
# interleaved partial writes across the multiprocessing Pool workers
# (each worker process has its own file handle and lock).
_CELL_TRACE_LOCK: Lock = Lock()


def _cell_trace_path() -> Path | None:
    p = os.environ.get("T0122_CELL_TRACE_JSONL", "").strip()
    if p == "":
        return None
    return Path(p)


# Forward declaration; the actual ``_append_cell_trace`` lives below
# ``CellEvalResult`` because it references that type.

# t0122 REQ-11: tightened silence guard.
# Cytoplasm-volume minimisation pushes the optimiser toward tiny cells
# with low total spike counts -- exactly the silence-corner regime where
# the t0102 DSI = 1.0 artifact appeared. Replacing the
# ``total_mean_spikes < 10`` threshold with ``sum(pd_spikes) < 3`` (i.e.
# total PD spikes across the N_EVAL_SEEDS=3 PD trials below 3, meaning
# fewer than 1 spike on average per PD trial) is the minimum-risk patch
# that hardens the guard for the new objective vector.
SILENCE_PD_SPIKES_THRESHOLD: int = 3


# Worker-process global cache (REQ-18).
_WORKER_CELL: MorphologyResult | None = None
_WORKER_BUNDLE: SynapseBundle | None = None
_WORKER_MORPH_HASH: int | None = None
_WORKER_ELECTROPHYS_HASH: int | None = None


def _ensure_worker_cell(*, morph_params: MorphologyParams, morph_hash: int) -> MorphologyResult:
    """Build or reuse the worker cell for the given morphology vector."""
    global _WORKER_CELL, _WORKER_MORPH_HASH, _WORKER_BUNDLE, _WORKER_ELECTROPHYS_HASH
    if _WORKER_CELL is not None and morph_hash == _WORKER_MORPH_HASH:
        return _WORKER_CELL
    # Rebuild — reset bundle / electrophys cache.
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
) -> TrialResult:
    h = cell.h
    try:
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
                eval_seed_index=eval_seed_index,
                spike_count=0,
                peak_mv=float("nan"),
                error="non_finite_voltage",
            )
        spikes = _count_spikes(v_arr, AP_THRESHOLD_MV)
        peak = float(v_arr.max()) if v_arr.size > 0 else float("nan")
        return TrialResult(
            direction_deg=direction_deg,
            seed=seed,
            eval_seed_index=eval_seed_index,
            spike_count=spikes,
            peak_mv=peak,
            error=None,
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


def _vector_sum_dsi(*, spike_counts_per_dir: dict[float, list[int]]) -> float:
    """Vector-sum DSI: |sum_dir(spikes_dir * unit_vec(dir))| / sum_dir(spikes_dir).

    Result is bounded in [0, 1]. Returns 0 if no direction has any spikes.
    """
    if len(spike_counts_per_dir) == 0:
        return 0.0
    total_x = 0.0
    total_y = 0.0
    total_spikes_f = 0.0
    for direction_deg, counts in spike_counts_per_dir.items():
        if len(counts) == 0:
            continue
        mean_count = float(np.mean(counts))
        rad = np.deg2rad(direction_deg)
        # PD = 0 deg = +x axis.
        total_x += mean_count * np.cos(rad)
        total_y += mean_count * np.sin(rad)
        total_spikes_f += mean_count
    if total_spikes_f <= 1e-12:
        return 0.0
    return float(np.hypot(total_x, total_y) / total_spikes_f)


def _summarise_trials(
    *,
    results: list[TrialResult],
    n_seeds: int,
    cytoplasm_volume_um3: float = WORST_CASE_CYTOPLASM_VOLUME_UM3,
) -> CellEvalResult:
    spike_counts_per_dir: dict[float, list[int]] = {}
    pd_seed_dsis: list[float] = []
    n_errors = 0
    peak_vm_mv: float = float("-inf")
    is_unstable = False
    pd_spikes: list[int] = []
    # Index by eval_seed_index (0..N_EVAL_SEEDS-1) to compute per-seed DSI.
    seed_to_dir_counts: dict[int, dict[float, int]] = {}
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

    if n_errors >= len(results) // 2 or len(spike_counts_per_dir) == 0:
        return CellEvalResult(
            dsi_vector_sum=WORST_CASE_DSI,
            pd_rate_hz=WORST_CASE_PD_RATE_HZ,
            robustness=WORST_CASE_ROBUSTNESS,
            n_trials=len(results),
            n_errors=n_errors,
            elapsed_s=0.0,
            is_unstable=True,
            peak_vm_mv=peak_vm_mv if peak_vm_mv != float("-inf") else float("nan"),
            cytoplasm_volume_um3=cytoplasm_volume_um3,
        )

    # t0122 REQ-11: tightened silence guard. Replaces the t0102/t0115
    # ``total_mean_spikes < 10`` threshold with ``sum(pd_spikes) < 3``,
    # i.e. fewer than 3 total PD spikes across the N_EVAL_SEEDS=3 PD
    # trials. Cytoplasm-volume minimisation pushes the optimiser toward
    # tiny cells that may spike below the t0115 threshold but still ride
    # the DSI = 1.0 silence-corner artifact; the new threshold is hard
    # to spoof because PD = 0 deg should be the highest-firing direction
    # for any genuinely directional cell.
    pd_spikes_sum: int = int(sum(pd_spikes)) if len(pd_spikes) > 0 else 0
    if pd_spikes_sum < SILENCE_PD_SPIKES_THRESHOLD:
        dsi_vector_sum = 0.0
    else:
        dsi_vector_sum = _vector_sum_dsi(spike_counts_per_dir=spike_counts_per_dir)
    pd_rate_hz = float(np.mean(pd_spikes)) / (TSTOP_MS / 1000.0) if pd_spikes else 0.0

    # Per-seed DSI for robustness: vector-sum DSI computed per seed.
    for _seed, dir_counts in seed_to_dir_counts.items():
        if len(dir_counts) < 2:
            continue
        per_seed_dsi = _vector_sum_dsi(spike_counts_per_dir={k: [v] for k, v in dir_counts.items()})
        pd_seed_dsis.append(per_seed_dsi)

    if len(pd_seed_dsis) >= 2:
        mean_dsi = float(np.mean(pd_seed_dsis))
        std_dsi = float(np.std(pd_seed_dsis))
        if mean_dsi <= 1e-6:
            robustness = WORST_CASE_ROBUSTNESS
        else:
            cv = std_dsi / mean_dsi
            robustness = float(1.0 / (1.0 + cv))  # bounded in (0, 1]
    else:
        robustness = WORST_CASE_ROBUSTNESS

    return CellEvalResult(
        dsi_vector_sum=dsi_vector_sum,
        pd_rate_hz=pd_rate_hz,
        robustness=robustness,
        n_trials=len(results),
        n_errors=n_errors,
        elapsed_s=0.0,
        is_unstable=is_unstable,
        peak_vm_mv=peak_vm_mv,
        cytoplasm_volume_um3=cytoplasm_volume_um3,
    )


def evaluate_68d_vector(
    *,
    vector_68d: NDArray[np.float64],
    eval_seeds: list[int] | None = None,
    n_directions: int = N_DIRECTIONS,
) -> CellEvalResult:
    """Evaluate one 68-d vector. SINGLE-WORKER, SEQUENTIAL — caller parallelises by cell."""
    t0 = time.time()
    electrophys_54d, morph_14d = split_68d_vector(vector_68d=vector_68d)
    morph_hash = hash_morphology_vector(vector=morph_14d)
    electrophys_hash = hash(electrophys_54d.tobytes())
    morph_params = morphology_params_from_vector(morph_vector_14d=morph_14d)
    electrophys_params = ParameterVector(values=electrophys_54d)
    placer_seed = SEED_BASE + (electrophys_hash & 0xFFFF)

    try:
        cell = _ensure_worker_cell(morph_params=morph_params, morph_hash=morph_hash)
        # t0122 REQ-10: compute per-cell cytoplasm volume immediately
        # after the cell is built (pure geometry; no NEURON simulation
        # step needed). Passed through to ``_summarise_trials`` so the
        # second F-axis lives on ``CellEvalResult.cytoplasm_volume_um3``.
        cytoplasm_volume_um3 = compute_cytoplasm_volume_um3(cell=cell)
        bundle = _ensure_synapse_bundle(
            cell=cell,
            electrophys_params=electrophys_params,
            placer_seed=placer_seed,
            electrophys_hash=electrophys_hash,
        )
    except (RuntimeError, ValueError, AssertionError, ArithmeticError):
        elapsed = time.time() - t0
        return CellEvalResult(
            dsi_vector_sum=WORST_CASE_DSI,
            pd_rate_hz=WORST_CASE_PD_RATE_HZ,
            robustness=WORST_CASE_ROBUSTNESS,
            n_trials=0,
            n_errors=1,
            elapsed_s=elapsed,
            is_unstable=True,
            peak_vm_mv=float("nan"),
            cytoplasm_volume_um3=WORST_CASE_CYTOPLASM_VOLUME_UM3,
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
                )
            )

    summary = _summarise_trials(
        results=results,
        n_seeds=len(eval_seeds),
        cytoplasm_volume_um3=cytoplasm_volume_um3,
    )
    return CellEvalResult(
        dsi_vector_sum=summary.dsi_vector_sum,
        pd_rate_hz=summary.pd_rate_hz,
        robustness=summary.robustness,
        n_trials=summary.n_trials,
        n_errors=summary.n_errors,
        elapsed_s=time.time() - t0,
        is_unstable=summary.is_unstable,
        peak_vm_mv=summary.peak_vm_mv,
        cytoplasm_volume_um3=summary.cytoplasm_volume_um3,
    )


# Top-level pickleable for ProcessPoolExecutor.
def _worker_evaluate_vector(
    *, vector_68d: NDArray[np.float64], eval_seeds: list[int]
) -> CellEvalResult:
    try:
        return evaluate_68d_vector(vector_68d=vector_68d, eval_seeds=eval_seeds)
    except (RuntimeError, ValueError, AssertionError, ArithmeticError):
        return CellEvalResult(
            dsi_vector_sum=WORST_CASE_DSI,
            pd_rate_hz=WORST_CASE_PD_RATE_HZ,
            robustness=WORST_CASE_ROBUSTNESS,
            n_trials=0,
            n_errors=1,
            elapsed_s=0.0,
            is_unstable=True,
            peak_vm_mv=float("nan"),
            cytoplasm_volume_um3=WORST_CASE_CYTOPLASM_VOLUME_UM3,
        )


def _append_cell_trace(*, vector_68d: NDArray[np.float64], result: CellEvalResult) -> None:
    """Append one JSON line per cell to the side-channel trace file.

    No-op when ``T0122_CELL_TRACE_JSONL`` is unset (e.g., in unit tests
    and smoke gates). Tolerant of write errors -- the trace is a
    convenience channel; the cell evaluation has already returned via F.
    """
    path = _cell_trace_path()
    if path is None:
        return
    record = {
        "vector_68d": [float(v) for v in vector_68d],
        "dsi_vector_sum": float(result.dsi_vector_sum),
        "pd_rate_hz": float(result.pd_rate_hz),
        "robustness": float(result.robustness),
        "cytoplasm_volume_um3": float(result.cytoplasm_volume_um3),
        "n_trials": int(result.n_trials),
        "n_errors": int(result.n_errors),
        "is_unstable": bool(result.is_unstable),
        "peak_vm_mv": float(result.peak_vm_mv)
        if result.peak_vm_mv == result.peak_vm_mv  # not NaN
        else None,
        "elapsed_s": float(result.elapsed_s),
        "wall_clock_s": time.time(),
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record) + "\n"
        with _CELL_TRACE_LOCK, path.open("a", encoding="utf-8") as f:
            f.write(line)
    except (OSError, RuntimeError):
        pass


class BedBV3MorphProblem(ElementwiseProblem):
    """68-d joint problem for pymoo NSGA-II (REQ-2)."""

    def __init__(
        self,
        *,
        eval_seeds: list[int],
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

    def _evaluate(self, x: NDArray[np.float64], out: dict[str, Any], *args, **kwargs) -> None:
        vec = np.asarray(x, dtype=np.float64)
        try:
            result = evaluate_68d_vector(vector_68d=vec, eval_seeds=self._eval_seeds)
            # t0122 REQ-10: 2 objectives (DSI maximised, cytoplasm
            # volume minimised). DSI is negated (pymoo minimises);
            # volume is NOT negated because it is the cost objective
            # already in the minimised direction. PD-rate is still
            # computed and stored on ``CellEvalResult`` for downstream
            # diagnostics / joint-pass filtering / predictions assets,
            # but does NOT enter the F vector.
            out["F"] = np.array(
                [-result.dsi_vector_sum, +result.cytoplasm_volume_um3],
                dtype=np.float64,
            )
            _append_cell_trace(vector_68d=vec, result=result)
        except Exception:  # noqa: BLE001
            traceback.print_exc()
            out["F"] = np.array(
                [-WORST_CASE_DSI, +WORST_CASE_CYTOPLASM_VOLUME_UM3],
                dtype=np.float64,
            )
