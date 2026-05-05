"""NSGA-II loop entry point for t0081, reusing t0080's harness with warm-start.

Builds the 96-cell warm-start array, wraps it in ``Population.new("X", arr)``,
and invokes ``nsga2_loop.run_nsga2_loop`` with custom sampling. Result paths
are redirected from t0080's ``results/`` to t0081's ``results/`` via
monkey-patching the t0080 module-level path constants before the loop runs.
"""

from __future__ import annotations

import argparse
import sys

import numpy as np
from numpy.typing import NDArray
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.population import Population
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize

# Import t0080's harness; we patch its path constants before running so all
# saves land in t0081's results dir.
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code import nsga2_loop as t80_loop
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    HARD_BUDGET_USD,
    HOURLY_RATE_USD,
    LHS_SEED,
    PM_ETA,
    POP_SIZE,
    SBX_ETA,
)
from tasks.t0081_bedb_v3_warmstart_nsga2.code.paths import (
    ALL_EVALUATIONS_JSON,
    BUDGET_OVERRUN_MD,
    HV_TRAJECTORY_JSON,
    INTERVENTION_DIR,
    PARETO_FRONT_JSON,
    RESULTS_DATA_DIR,
    ensure_directories,
)
from tasks.t0081_bedb_v3_warmstart_nsga2.code.warm_start import (
    N_TOTAL,
    assemble_warm_start_population,
)


def _redirect_t80_paths_to_t81() -> None:
    """Override t0080 module-level path constants so writes land in t0081/."""
    t80_loop.PARETO_FRONT_JSON = PARETO_FRONT_JSON
    t80_loop.RESULTS_DATA_DIR = RESULTS_DATA_DIR
    t80_loop.INTERVENTION_DIR = INTERVENTION_DIR
    t80_loop.BUDGET_OVERRUN_MD = BUDGET_OVERRUN_MD
    # The all_evaluations and hv_trajectory writers compute paths from
    # RESULTS_DATA_DIR at call time, so patching that constant suffices.
    _ = ALL_EVALUATIONS_JSON
    _ = HV_TRAJECTORY_JSON


def _run_warmstart_nsga2(
    *,
    pop_size: int,
    n_gen: int,
    seed: int,
    max_workers: int,
    hourly_rate_usd: float,
    hard_budget_usd: float,
) -> None:
    """Run NSGA-II with the 96-cell warm-started initial population."""
    ensure_directories()
    _redirect_t80_paths_to_t81()
    # Override hard budget cap (t0080 default is $2.00; t0081 spec is $3.00).
    t80_loop._HARD_BUDGET_USD = hard_budget_usd  # type: ignore[attr-defined]

    import time

    t80_loop._LOOP_START_TIME = time.time()  # type: ignore[attr-defined]
    t80_loop._HOURLY_RATE_USD = hourly_rate_usd  # type: ignore[attr-defined]
    t80_loop._ALL_EVALUATIONS = []  # type: ignore[attr-defined]

    problem = t80_loop.BedBV3Problem(max_workers=max_workers)
    warm_array: NDArray[np.float64] = assemble_warm_start_population(problem=problem)
    assert warm_array.shape[0] == pop_size, (
        f"warm-start size {warm_array.shape[0]} != pop_size {pop_size}"
    )
    initial_pop = Population.new("X", warm_array)
    algorithm = NSGA2(
        pop_size=pop_size,
        sampling=initial_pop,
        crossover=SBX(eta=SBX_ETA, prob=0.9),
        mutation=PM(eta=PM_ETA),
        eliminate_duplicates=True,
    )
    print(
        f"[t0081] starting NSGA-II: pop_size={pop_size} n_gen={n_gen} seed={seed} "
        f"max_workers={max_workers} hourly_rate=${hourly_rate_usd:.4f} "
        f"hard_budget=${hard_budget_usd:.2f} warm_start={warm_array.shape}",
        flush=True,
    )
    minimize(
        problem,
        algorithm,
        ("n_gen", n_gen),
        seed=seed,
        verbose=True,
        save_history=False,
    )
    t80_loop._save_all_evaluations(  # type: ignore[attr-defined]
        all_evaluations=t80_loop._ALL_EVALUATIONS  # type: ignore[attr-defined]
    )
    t80_loop._save_pareto_front(  # type: ignore[attr-defined]
        all_evaluations=t80_loop._ALL_EVALUATIONS  # type: ignore[attr-defined]
    )
    t80_loop._save_hv_trajectory(  # type: ignore[attr-defined]
        all_evaluations=t80_loop._ALL_EVALUATIONS  # type: ignore[attr-defined]
    )
    final_cost = t80_loop._elapsed_cost_usd()  # type: ignore[attr-defined]
    print(
        f"[t0081] done: {len(t80_loop._ALL_EVALUATIONS)} evaluations, "  # type: ignore[attr-defined]
        f"final cost ${final_cost:.4f} (cap ${hard_budget_usd:.2f})",
        flush=True,
    )


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pop-size", type=int, default=N_TOTAL)
    parser.add_argument("--n-gen", type=int, default=8)
    parser.add_argument("--seed", type=int, default=LHS_SEED)
    parser.add_argument("--max-workers", type=int, default=0)
    parser.add_argument("--hourly-rate-usd", type=float, default=HOURLY_RATE_USD)
    parser.add_argument("--hard-budget-usd", type=float, default=3.00)
    args = parser.parse_args()
    assert args.pop_size == POP_SIZE or args.pop_size == N_TOTAL, (
        f"pop_size must be {N_TOTAL} (the warm-start size); got {args.pop_size}"
    )
    _run_warmstart_nsga2(
        pop_size=args.pop_size,
        n_gen=args.n_gen,
        seed=args.seed,
        max_workers=args.max_workers,
        hourly_rate_usd=args.hourly_rate_usd,
        hard_budget_usd=args.hard_budget_usd,
    )
    _ = HARD_BUDGET_USD  # kept for symmetry with t0080 import surface
    return 0


if __name__ == "__main__":
    sys.exit(_main())
