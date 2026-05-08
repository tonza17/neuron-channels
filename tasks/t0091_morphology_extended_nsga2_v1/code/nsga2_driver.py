"""t0091 NSGA-II driver — joint 68-d run with HV-plateau + cost watchdog termination.

Mirrors t0080's `nsga2_loop.py` adapted for:
* 68-d problem (REQ-2)
* Pop 96 with warm-start sampling (REQ-3)
* SBX(eta=15, prob=0.9), PM(eta=20, prob=1/68), eliminate_duplicates=True (REQ-5)
* TerminationCollection: MaxGen(8) + HVPlateauTermination(2-gen window, 1% rel
  threshold, 4-gen min) + CostWatchdogTermination($4.00 hard cap) (REQ-6, REQ-7)
* Per-generation HV trajectory and all_evaluations dump (incremental writes).

The driver writes after every generation:
* `hv_trajectory.json`  — generation index + hypervolume
* `all_evaluations.json` — every cell evaluated so far
* `nsga2_checkpoint.json` — minimal pop snapshot for resume
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from multiprocessing import Pool, cpu_count
from typing import Any

import numpy as np
from numpy.typing import NDArray
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.callback import Callback
from pymoo.core.termination import Termination

try:
    # 0.6.x location
    from pymoo.parallelization.starmap import (
        StarmapParallelization,  # type: ignore[import-not-found]
    )
except ImportError:  # pragma: no cover
    from pymoo.core.problem import StarmapParallelization  # type: ignore[import-not-found]
from pymoo.indicators.hv import HV
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize
from pymoo.termination.collection import TerminationCollection
from pymoo.termination.max_gen import MaximumGenerationTermination

from tasks.t0091_morphology_extended_nsga2_v1.code.constants_t91 import (
    HV_UTOPIA_DSI,
    HV_UTOPIA_PD_RATE_HZ,
    HV_UTOPIA_ROBUSTNESS,
    N_EVAL_SEEDS,
    N_GEN,
    PM_ETA,
    PM_PROB,
    POP_SIZE,
    REF_POINT_HV,
    SBX_ETA,
    SBX_PROB,
    T0091_HARD_BUDGET_USD,
)
from tasks.t0091_morphology_extended_nsga2_v1.code.cost_watchdog import (
    make_watchdog_from_machine_log,
)
from tasks.t0091_morphology_extended_nsga2_v1.code.evaluator import (
    BedBV3MorphProblem,
)
from tasks.t0091_morphology_extended_nsga2_v1.code.hv_plateau_watchdog import (
    HVPlateauTermination,
)
from tasks.t0091_morphology_extended_nsga2_v1.code.paths import (
    ALGORITHM_CONFIG_JSON,
    ALL_EVALUATIONS_JSON,
    BUDGET_OVERRUN_MD,
    CHECKPOINT_JSON,
    EVALUATION_SEEDS_JSON,
    HV_TRAJECTORY_JSON,
    MACHINE_LOG_JSON,
    WARM_START_POPULATION_JSON,
    ensure_directories,
)

_HOURLY_RATE_USD: float = 0.30  # patched at runtime by cost_watchdog.patch_t91_loop_rate


@dataclass(slots=True)
class _DriverState:
    started_at: datetime
    instance_started_at: datetime
    cost_watchdog: Any
    all_evaluations: list[dict[str, object]]
    hv_trajectory: list[dict[str, object]]
    pop_snapshots: list[dict[str, object]]


class CostWatchdogTermination(Termination):
    """Termination triggered when the cost watchdog trips."""

    def __init__(self, *, watchdog: Any) -> None:
        super().__init__()
        self._watchdog = watchdog

    def _update(self, algorithm: object) -> float:  # type: ignore[override]
        if self._watchdog.trip_if_over_cap(intervention_md_path=BUDGET_OVERRUN_MD):
            print("[cost_watchdog] tripped — terminating NSGA-II")
            return 1.0
        return 0.0


def _objective_to_dsi_pd_robustness(F_neg: NDArray[np.float64]) -> NDArray[np.float64]:
    """Reverse the sign convention used inside the problem (we negated maximisations)."""
    return -F_neg


def _compute_hv(F_neg: NDArray[np.float64]) -> float:
    """HV in the (DSI, PD-rate, robustness) maximisation space, mapped to minimisation.

    pymoo HV indicator expects minimisation; our F is already minimisation-form
    (negated maximisations). Reference point is REF_POINT_HV = (0, 0, 0)
    (any solution worse than (-0, -0, -0) is excluded). Utopia is at
    (-DSI_max, -PD_max, -robustness_max).
    """
    ref_point = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    if F_neg.size == 0:
        return 0.0
    hv = HV(ref_point=ref_point)
    return float(hv.do(F_neg))


def _save_iteration(
    *,
    state: _DriverState,
    generation: int,
    population_X: NDArray[np.float64],
    population_F: NDArray[np.float64],
    rate_usd_per_hour: float,
) -> None:
    """Persist HV trajectory, all_evaluations, and pop snapshot to disk."""
    elapsed_s = (datetime.now(UTC) - state.instance_started_at).total_seconds()
    cost_so_far_usd = (elapsed_s / 3600.0) * rate_usd_per_hour
    hv = _compute_hv(F_neg=population_F)
    state.hv_trajectory.append(
        {
            "generation": int(generation),
            "hypervolume": float(hv),
            "cumulative_cost_usd": float(cost_so_far_usd),
            "elapsed_s": float(elapsed_s),
            "n_evaluations": int(len(state.all_evaluations)),
        }
    )
    HV_TRAJECTORY_JSON.write_text(
        json.dumps({"trajectory": state.hv_trajectory}, indent=2),
        encoding="utf-8",
    )
    # Append generation snapshot to all_evaluations.
    for x_row, f_row in zip(population_X, population_F, strict=True):
        state.all_evaluations.append(
            {
                "generation": int(generation),
                "vector_68d": [float(v) for v in x_row],
                "objective_F_minimised": [float(v) for v in f_row],
                "dsi_vector_sum": float(-f_row[0]),
                "pd_rate_hz": float(-f_row[1]),
                "robustness": float(-f_row[2]),
            }
        )
    ALL_EVALUATIONS_JSON.write_text(
        json.dumps({"evaluations": state.all_evaluations}, indent=2),
        encoding="utf-8",
    )
    # Pop snapshot for resume.
    state.pop_snapshots.append(
        {
            "generation": int(generation),
            "X": [[float(v) for v in row] for row in population_X],
            "F": [[float(v) for v in row] for row in population_F],
        }
    )
    CHECKPOINT_JSON.write_text(
        json.dumps({"generations": state.pop_snapshots}, indent=2),
        encoding="utf-8",
    )
    print(
        f"[gen {generation}] HV={hv:.4f}  pop_size={len(population_X)}  "
        f"cost_so_far=${cost_so_far_usd:.4f}  elapsed={elapsed_s:.0f}s"
    )


class _GenerationCallback(Callback):
    def __init__(self, *, state: _DriverState, rate_usd_per_hour: float) -> None:
        super().__init__()
        self._state = state
        self._rate = rate_usd_per_hour

    def notify(self, algorithm: Any) -> None:  # type: ignore[override]
        gen = algorithm.n_gen
        pop = algorithm.pop
        X = np.array([ind.X for ind in pop], dtype=np.float64)
        F = np.array([ind.F for ind in pop], dtype=np.float64)
        _save_iteration(
            state=self._state,
            generation=int(gen),
            population_X=X,
            population_F=F,
            rate_usd_per_hour=self._rate,
        )


def _load_warmstart_matrix() -> NDArray[np.float64]:
    payload = json.loads(WARM_START_POPULATION_JSON.read_text(encoding="utf-8"))
    matrix = np.array(payload["matrix"], dtype=np.float64)
    assert matrix.shape == (POP_SIZE, 68), f"warmstart shape {matrix.shape} != (96, 68)"
    return matrix


def _eval_seeds() -> list[int]:
    """Deterministic evaluation seeds (REQ-21)."""
    ss = np.random.SeedSequence(42)
    seeds = [int(s.generate_state(1)[0]) for s in ss.spawn(N_EVAL_SEEDS)]
    EVALUATION_SEEDS_JSON.write_text(
        json.dumps({"seeds": seeds, "method": "np.random.SeedSequence(42).spawn(5)"}, indent=2),
        encoding="utf-8",
    )
    return seeds


def _save_algorithm_config(*, eval_seeds: list[int]) -> None:
    out: dict[str, object] = {
        "pop_size": POP_SIZE,
        "n_gen_max": N_GEN,
        "sbx_eta": SBX_ETA,
        "sbx_prob": SBX_PROB,
        "pm_eta": PM_ETA,
        "pm_prob": PM_PROB,
        "eliminate_duplicates": True,
        "n_eval_seeds": N_EVAL_SEEDS,
        "eval_seeds": eval_seeds,
        "ref_point_hv": list(REF_POINT_HV),
        "hv_utopia": [HV_UTOPIA_DSI, HV_UTOPIA_PD_RATE_HZ, HV_UTOPIA_ROBUSTNESS],
        "hard_budget_usd": T0091_HARD_BUDGET_USD,
    }
    ALGORITHM_CONFIG_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")


def run_nsga2() -> dict[str, object]:
    ensure_directories()
    eval_seeds = _eval_seeds()
    _save_algorithm_config(eval_seeds=eval_seeds)
    warmstart = _load_warmstart_matrix()

    instance_started_at = datetime.now(UTC)
    cost_watchdog = make_watchdog_from_machine_log(
        machine_log_path=MACHINE_LOG_JSON,
        instance_started_at=instance_started_at,
        hard_budget_usd=T0091_HARD_BUDGET_USD,
    )
    rate = cost_watchdog.hourly_rate_usd
    global _HOURLY_RATE_USD
    _HOURLY_RATE_USD = rate

    state = _DriverState(
        started_at=instance_started_at,
        instance_started_at=instance_started_at,
        cost_watchdog=cost_watchdog,
        all_evaluations=[],
        hv_trajectory=[],
        pop_snapshots=[],
    )

    # Effective cores billed = 64 (per machine_log.json cpu_cores_effective_billed).
    # cpu_count() returns 128 logical (with HT) on this AMD EPYC instance, but
    # NEURON workloads do not benefit from HT; cap at 60 to leave headroom.
    n_workers: int = min(60, max(1, (cpu_count() or 4) - 4))
    print(f"[nsga2_driver] using {n_workers} parallel workers")
    pool = Pool(processes=n_workers)
    runner = StarmapParallelization(pool.starmap)
    problem = BedBV3MorphProblem(eval_seeds=eval_seeds, elementwise_runner=runner)

    algorithm = NSGA2(
        pop_size=POP_SIZE,
        sampling=warmstart,
        crossover=SBX(eta=SBX_ETA, prob=SBX_PROB),
        mutation=PM(eta=PM_ETA, prob=PM_PROB),
        eliminate_duplicates=True,
    )

    termination = TerminationCollection(
        MaximumGenerationTermination(n_max_gen=N_GEN),
        HVPlateauTermination(),
        CostWatchdogTermination(watchdog=cost_watchdog),
    )

    callback = _GenerationCallback(state=state, rate_usd_per_hour=rate)

    print(
        f"[nsga2_driver] starting NSGA-II: pop={POP_SIZE} max_gen={N_GEN} "
        f"hard_cap=${T0091_HARD_BUDGET_USD:.2f} rate=${rate:.4f}/hr"
    )
    t_start = time.time()
    res = minimize(
        problem,
        algorithm,
        termination,
        seed=42,
        verbose=True,
        callback=callback,
        save_history=False,
    )
    elapsed = time.time() - t_start

    # Final dump.
    if res is not None and res.X is not None and res.F is not None:
        # res.X / res.F are 2D arrays (one row per Pareto solution).
        from tasks.t0091_morphology_extended_nsga2_v1.code.paths import PARETO_FRONT_JSON

        cells_out: list[dict[str, object]] = []
        for i, (x_row, f_row) in enumerate(zip(res.X, res.F, strict=True)):
            cells_out.append(
                {
                    "cell_id": i,
                    "vector_68d": [float(v) for v in x_row],
                    "params": [float(v) for v in x_row[:54]],
                    "morphology_vector_14d": [float(v) for v in x_row[54:]],
                    "objective_F_minimised": [float(v) for v in f_row],
                    "dsi_vector_sum": float(-f_row[0]),
                    "pd_rate_hz": float(-f_row[1]),
                    "robustness": float(-f_row[2]),
                }
            )
        PARETO_FRONT_JSON.write_text(
            json.dumps({"n_total": len(cells_out), "cells": cells_out}, indent=2),
            encoding="utf-8",
        )
        print(f"[nsga2_driver] wrote {PARETO_FRONT_JSON} with {len(cells_out)} Pareto cells")

    final_cost = cost_watchdog.current_cost_usd()
    pool.close()
    pool.terminate()
    print(
        f"[nsga2_driver] FINISHED in {elapsed:.0f}s ({elapsed / 60:.1f} min); "
        f"final cost=${final_cost:.4f}; tripped={cost_watchdog.tripped}"
    )

    return {
        "n_pareto": int(len(res.X)) if res is not None and res.X is not None else 0,
        "elapsed_s": float(elapsed),
        "final_cost_usd": float(final_cost),
        "watchdog_tripped": bool(cost_watchdog.tripped),
        "n_generations_completed": len(state.hv_trajectory),
    }


if __name__ == "__main__":
    summary = run_nsga2()
    print("[nsga2_driver] summary:", json.dumps(summary, indent=2))
