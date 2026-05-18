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

import time
import traceback
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray
from pymoo.core.problem import ElementwiseProblem

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
    MorphologyResult,
)
from tasks.t0107_t0106_polar_8dir_recheck.code import (
    bootstrap as _bootstrap,  # noqa: F401
)
from tasks.t0107_t0106_polar_8dir_recheck.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0107_t0106_polar_8dir_recheck.code.constants_electrophys import (
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
from tasks.t0107_t0106_polar_8dir_recheck.code.constants_morphology import (
    LOWER_BOUNDS_68,
    N_DIRECTIONS,
    N_EVAL_SEEDS,
    UPPER_BOUNDS_68,
    WORST_CASE_DSI,
    WORST_CASE_PD_RATE_HZ,
    WORST_CASE_ROBUSTNESS,
)
from tasks.t0107_t0106_polar_8dir_recheck.code.generator_wrapper import (
    _LIVE_CELLS,
    build_cell,
    hash_morphology_vector,
    morphology_params_from_vector,
    split_68d_vector,
)
from tasks.t0107_t0106_polar_8dir_recheck.code.trial_helpers import (
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
    # t0107 patch: per-direction mean firing rate (Hz) and angle order.
    # Length equals the n_directions argument passed to evaluate_68d_vector.
    # Mean is taken across the N_EVAL_SEEDS noise replicates.
    # Computed only when summarise_trials succeeds; otherwise empty.
    per_direction_rates_hz: tuple[float, ...] = ()
    per_direction_angles_deg: tuple[float, ...] = ()


# DSI silence guard threshold (S-0102-01, REQ-3).
# When the total mean spike count across the 16 directions is below this
# threshold, _summarise_trials forces dsi_vector_sum = 0.0 instead of calling
# _vector_sum_dsi. This eliminates the t0102 silence-corner artifact that put
# 27 cells at a spurious DSI = 1.0 by dividing by near-zero total_spikes_f.
SILENCE_SPIKE_COUNT_THRESHOLD: int = 10


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


def _summarise_trials(*, results: list[TrialResult], n_seeds: int) -> CellEvalResult:
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
            per_direction_rates_hz=(),
            per_direction_angles_deg=(),
        )

    # DSI silence guard (S-0102-01, REQ-3): force DSI = 0.0 when the cell's
    # total mean spike count across the 16 directions is below threshold.
    # This eliminates the t0102 silence-corner artifact. The guard runs ONLY
    # at the cell level; the per-seed _vector_sum_dsi call below remains raw
    # so robustness keeps its signal even for low-spike cells.
    total_mean_spikes: float = 0.0
    for _direction_deg, counts in spike_counts_per_dir.items():
        if len(counts) == 0:
            continue
        total_mean_spikes += float(np.mean(counts))
    if total_mean_spikes < SILENCE_SPIKE_COUNT_THRESHOLD:
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

    # t0107 patch: per-direction mean firing rate (Hz) ordered by ascending
    # angle. Mean is across the N_EVAL_SEEDS noise replicates per direction.
    sorted_angles: list[float] = sorted(spike_counts_per_dir.keys())
    per_direction_rates_hz: list[float] = [
        float(np.mean(spike_counts_per_dir[a])) / (TSTOP_MS / 1000.0) for a in sorted_angles
    ]

    return CellEvalResult(
        dsi_vector_sum=dsi_vector_sum,
        pd_rate_hz=pd_rate_hz,
        robustness=robustness,
        n_trials=len(results),
        n_errors=n_errors,
        elapsed_s=0.0,
        is_unstable=is_unstable,
        peak_vm_mv=peak_vm_mv,
        per_direction_rates_hz=tuple(per_direction_rates_hz),
        per_direction_angles_deg=tuple(sorted_angles),
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
            per_direction_rates_hz=(),
            per_direction_angles_deg=(),
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

    summary = _summarise_trials(results=results, n_seeds=len(eval_seeds))
    return CellEvalResult(
        dsi_vector_sum=summary.dsi_vector_sum,
        pd_rate_hz=summary.pd_rate_hz,
        robustness=summary.robustness,
        n_trials=summary.n_trials,
        n_errors=summary.n_errors,
        elapsed_s=time.time() - t0,
        is_unstable=summary.is_unstable,
        peak_vm_mv=summary.peak_vm_mv,
        per_direction_rates_hz=summary.per_direction_rates_hz,
        per_direction_angles_deg=summary.per_direction_angles_deg,
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
            per_direction_rates_hz=(),
            per_direction_angles_deg=(),
        )


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
            # Negate maximisation objectives for pymoo minimisation.
            # REQ-2: 2 objectives (DSI vector-sum + PD-rate); robustness is
            # still computed and stored on CellEvalResult for predictions
            # assets but does NOT enter NSGA-II selection.
            out["F"] = np.array(
                [-result.dsi_vector_sum, -result.pd_rate_hz],
                dtype=np.float64,
            )
        except Exception:  # noqa: BLE001
            traceback.print_exc()
            out["F"] = np.array(
                [-WORST_CASE_DSI, -WORST_CASE_PD_RATE_HZ],
                dtype=np.float64,
            )
