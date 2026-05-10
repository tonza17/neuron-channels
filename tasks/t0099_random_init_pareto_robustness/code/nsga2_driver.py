"""t0099 per-seed NSGA-II driver — random-init joint 68-d run.

Adapted from t0091's `nsga2_driver`. Differences:

* Per-seed cost cap of $1.00 (was $4.00 in t0091).
* `sampling` is a (96, 68) numpy matrix produced by ``random_init.py`` from
  Latin Hypercube Sampling — no anchor warm-start.
* Per-seed file naming: `pareto_front_seed{s}.json`,
  `all_evaluations_seed{s}.json`, `hv_trajectory_seed{s}.json`,
  `nsga2_checkpoint_seed{s}.json`.
* Pymoo `seed=<task_seed>` is passed to `minimize` so the inner GA RNG also
  varies across runs (not just the initial sample).
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
    from pymoo.parallelization.starmap import (
        StarmapParallelization,
    )
except ImportError:  # pragma: no cover
    from pymoo.core.problem import StarmapParallelization  # type: ignore[no-redef]
from pymoo.indicators.hv import HV
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize
from pymoo.termination.collection import TerminationCollection
from pymoo.termination.max_gen import MaximumGenerationTermination

from tasks.t0099_random_init_pareto_robustness.code.constants import (
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
    T0099_HARD_BUDGET_PER_SEED_USD,
)
from tasks.t0099_random_init_pareto_robustness.code.cost_watchdog import (
    make_watchdog_from_machine_log,
)
from tasks.t0099_random_init_pareto_robustness.code.evaluator import (
    BedBV3MorphProblem,
)
from tasks.t0099_random_init_pareto_robustness.code.hv_plateau_watchdog import (
    HVPlateauTermination,
)
from tasks.t0099_random_init_pareto_robustness.code.paths import (
    ALGORITHM_CONFIG_JSON,
    EVALUATION_SEEDS_JSON,
    MACHINE_LOG_JSON,
    all_evaluations_json,
    budget_overrun_md,
    checkpoint_json,
    ensure_directories,
    hv_trajectory_json,
    init_pop_json,
    pareto_front_json,
)

_HOURLY_RATE_USD: float = 0.30  # patched at runtime by cost_watchdog.patch_t99_loop_rate


@dataclass(slots=True)
class _DriverState:
    seed: int
    started_at: datetime
    instance_started_at: datetime
    cost_watchdog: Any
    all_evaluations: list[dict[str, object]]
    hv_trajectory: list[dict[str, object]]
    pop_snapshots: list[dict[str, object]]


class CostWatchdogTermination(Termination):
    """Termination triggered when the cost watchdog trips."""

    def __init__(self, *, watchdog: Any, seed: int) -> None:
        super().__init__()
        self._watchdog = watchdog
        self._seed = seed

    def _update(self, algorithm: object) -> float:  # type: ignore[override]
        if self._watchdog.trip_if_over_cap(intervention_md_path=budget_overrun_md(seed=self._seed)):
            print(f"[cost_watchdog seed={self._seed}] tripped — terminating NSGA-II")
            return 1.0
        return 0.0


def _compute_hv(F_neg: NDArray[np.float64]) -> float:
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
    hv_trajectory_json(seed=state.seed).write_text(
        json.dumps({"trajectory": state.hv_trajectory}, indent=2),
        encoding="utf-8",
    )
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
    all_evaluations_json(seed=state.seed).write_text(
        json.dumps({"evaluations": state.all_evaluations}, indent=2),
        encoding="utf-8",
    )
    state.pop_snapshots.append(
        {
            "generation": int(generation),
            "X": [[float(v) for v in row] for row in population_X],
            "F": [[float(v) for v in row] for row in population_F],
        }
    )
    checkpoint_json(seed=state.seed).write_text(
        json.dumps({"generations": state.pop_snapshots}, indent=2),
        encoding="utf-8",
    )
    print(
        f"[seed {state.seed} gen {generation}] HV={hv:.4f}  pop_size={len(population_X)}  "
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


def _load_init_matrix(*, seed: int) -> NDArray[np.float64]:
    payload = json.loads(init_pop_json(seed=seed).read_text(encoding="utf-8"))
    matrix = np.array(payload["matrix"], dtype=np.float64)
    assert matrix.shape == (POP_SIZE, 68), f"init pop shape {matrix.shape} != (96, 68)"
    return matrix


def _eval_seeds() -> list[int]:
    """Deterministic evaluation seeds (kept identical to t0091 for parity)."""
    ss = np.random.SeedSequence(42)
    seeds = [int(s.generate_state(1)[0]) for s in ss.spawn(N_EVAL_SEEDS)]
    EVALUATION_SEEDS_JSON.write_text(
        json.dumps({"seeds": seeds, "method": "np.random.SeedSequence(42).spawn(5)"}, indent=2),
        encoding="utf-8",
    )
    return seeds


def _save_algorithm_config(*, eval_seeds: list[int], task_seeds: list[int]) -> None:
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
        "task_seeds": task_seeds,
        "ref_point_hv": list(REF_POINT_HV),
        "hv_utopia": [HV_UTOPIA_DSI, HV_UTOPIA_PD_RATE_HZ, HV_UTOPIA_ROBUSTNESS],
        "hard_budget_per_seed_usd": T0099_HARD_BUDGET_PER_SEED_USD,
        "sampling_method": "pymoo.operators.sampling.lhs.LatinHypercubeSampling",
    }
    ALGORITHM_CONFIG_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")


def run_nsga2_for_seed(*, task_seed: int) -> dict[str, object]:
    """Run NSGA-II for a single random-init task seed."""
    ensure_directories()
    eval_seeds = _eval_seeds()
    init_matrix = _load_init_matrix(seed=task_seed)

    instance_started_at = datetime.now(UTC)
    cost_watchdog = make_watchdog_from_machine_log(
        machine_log_path=MACHINE_LOG_JSON,
        instance_started_at=instance_started_at,
        hard_budget_usd=T0099_HARD_BUDGET_PER_SEED_USD,
    )
    rate = cost_watchdog.hourly_rate_usd
    global _HOURLY_RATE_USD
    _HOURLY_RATE_USD = rate

    state = _DriverState(
        seed=task_seed,
        started_at=instance_started_at,
        instance_started_at=instance_started_at,
        cost_watchdog=cost_watchdog,
        all_evaluations=[],
        hv_trajectory=[],
        pop_snapshots=[],
    )

    n_workers: int = min(60, max(1, (cpu_count() or 4) - 4))
    print(f"[nsga2_driver seed={task_seed}] using {n_workers} parallel workers")
    pool = Pool(processes=n_workers)
    runner = StarmapParallelization(pool.starmap)
    problem = BedBV3MorphProblem(eval_seeds=eval_seeds, elementwise_runner=runner)

    algorithm = NSGA2(
        pop_size=POP_SIZE,
        sampling=init_matrix,
        crossover=SBX(eta=SBX_ETA, prob=SBX_PROB),
        mutation=PM(eta=PM_ETA, prob=PM_PROB),
        eliminate_duplicates=True,
    )

    termination = TerminationCollection(
        MaximumGenerationTermination(n_max_gen=N_GEN),
        HVPlateauTermination(seed=task_seed),
        CostWatchdogTermination(watchdog=cost_watchdog, seed=task_seed),
    )

    callback = _GenerationCallback(state=state, rate_usd_per_hour=rate)

    print(
        f"[nsga2_driver seed={task_seed}] starting: pop={POP_SIZE} max_gen={N_GEN} "
        f"hard_cap=${T0099_HARD_BUDGET_PER_SEED_USD:.2f} rate=${rate:.4f}/hr"
    )
    t_start = time.time()
    res = minimize(
        problem,
        algorithm,
        termination,
        seed=task_seed,
        verbose=True,
        callback=callback,
        save_history=False,
    )
    elapsed = time.time() - t_start

    if res is not None and res.X is not None and res.F is not None:
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
        out_path = pareto_front_json(seed=task_seed)
        n_cells = len(cells_out)
        out_path.write_text(
            json.dumps(
                {"seed": task_seed, "n_total": n_cells, "cells": cells_out},
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"[nsga2_driver seed={task_seed}] wrote {out_path} with {n_cells} Pareto cells")

    final_cost = cost_watchdog.current_cost_usd()
    pool.close()
    pool.terminate()
    print(
        f"[nsga2_driver seed={task_seed}] FINISHED in {elapsed:.0f}s ({elapsed / 60:.1f} min); "
        f"final cost=${final_cost:.4f}; tripped={cost_watchdog.tripped}"
    )

    return {
        "seed": task_seed,
        "n_pareto": int(len(res.X)) if res is not None and res.X is not None else 0,
        "elapsed_s": float(elapsed),
        "final_cost_usd": float(final_cost),
        "watchdog_tripped": bool(cost_watchdog.tripped),
        "n_generations_completed": len(state.hv_trajectory),
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="t0099 NSGA-II driver (one seed)")
    parser.add_argument("--seed", type=int, required=True, help="Task RNG seed")
    parser.add_argument(
        "--save-algorithm-config",
        action="store_true",
        help="Write algorithm_config.json (do this once across the 3-seed run)",
    )
    parser.add_argument(
        "--task-seeds",
        type=int,
        nargs="+",
        default=None,
        help="Task seeds for the algorithm_config (defaults to T0099_SEEDS)",
    )
    args = parser.parse_args()
    if args.save_algorithm_config:
        from tasks.t0099_random_init_pareto_robustness.code.constants import T0099_SEEDS

        eval_seeds = _eval_seeds()
        task_seeds = args.task_seeds if args.task_seeds is not None else list(T0099_SEEDS)
        _save_algorithm_config(eval_seeds=eval_seeds, task_seeds=task_seeds)
    summary = run_nsga2_for_seed(task_seed=int(args.seed))
    print("[nsga2_driver] summary:", json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
