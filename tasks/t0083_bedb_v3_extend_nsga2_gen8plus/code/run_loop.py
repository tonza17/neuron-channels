"""NSGA-II continuation entry point for t0083.

Reuses t0081's harness + t0080's underlying nsga2_loop substrate library:

* Pre-loads t0081's gen-7 final population (96 survivors) via
  ``reload_gen7.reload_t0081_gen7_survivors`` so pymoo skips re-evaluation.
* Pre-sets ``problem.eval_count = 768`` so the first true offspring evaluation
  lands at generation 8 (768 // POP_SIZE).
* Pre-loads t0080 module global ``_ALL_EVALUATIONS`` from t0081's saved
  ``all_evaluations.json`` so subsequent ``_save_*`` calls emit the union
  (768 t0081 cells + new t0083 cells).
* Combines ``MaximumGenerationTermination(10)`` and the HV-plateau watchdog
  via ``TerminationCollection`` (stop on either).
* Overrides the cost-cap to $5.00 (vs t0081's $3.00 vs t0080's $2.00).
"""

from __future__ import annotations

import argparse
import json
import sys
import time

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize
from pymoo.termination.collection import TerminationCollection
from pymoo.termination.max_gen import MaximumGenerationTermination

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code import nsga2_loop as t80_loop
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    HOURLY_RATE_USD,
    LHS_SEED,
    PM_ETA,
    POP_SIZE,
    SBX_ETA,
)
from tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code import paths, reload_gen7
from tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code.hv_plateau_watchdog import (
    HVPlateauTermination,
)

# t0083 specific parameters.
T0083_HARD_BUDGET_USD: float = 5.00
T0083_MAX_ADDITIONAL_GENERATIONS: int = 10
N_T0081_EVALUATIONS: int = 768  # 96 (POP_SIZE) * 8 generations from t0081


def _redirect_t80_paths_to_t83() -> None:
    """Override t0080 module-level path constants so writes land in t0083/."""
    t80_loop.PARETO_FRONT_JSON = paths.PARETO_FRONT_JSON
    t80_loop.RESULTS_DATA_DIR = paths.RESULTS_DATA_DIR
    t80_loop.INTERVENTION_DIR = paths.INTERVENTION_DIR
    t80_loop.BUDGET_OVERRUN_MD = paths.BUDGET_OVERRUN_MD


def _load_t0081_evaluations_into_module() -> int:
    """Pre-load t0081's all_evaluations.json into the t0080 module global.

    Returns the number of records loaded.
    """
    raw = json.loads(paths.T0081_ALL_EVALUATIONS_JSON.read_text(encoding="utf-8"))
    records = raw.get("evaluations", raw) if isinstance(raw, dict) else raw
    assert isinstance(records, list), "expected list of records"
    # Convert dicts back to CellEvaluation dataclasses so the existing
    # save helpers (which call asdict) work.
    cells = [
        t80_loop.CellEvaluation(
            cell_index=int(r["cell_index"]),
            generation=int(r["generation"]),
            params=[float(v) for v in r["params"]],
            dsi=float(r["dsi"]),
            pd_rate_hz=float(r["pd_rate_hz"]),
            is_unstable=bool(r["is_unstable"]),
            peak_vm_mv=float(r["peak_vm_mv"]),
            elapsed_s=float(r["elapsed_s"]),
            constraint_violation=float(r["constraint_violation"]),
            is_feasible=bool(r["is_feasible"]),
        )
        for r in records
    ]
    t80_loop._ALL_EVALUATIONS = cells  # type: ignore[attr-defined]
    return len(cells)


def _run_continuation_nsga2(
    *,
    pop_size: int,
    max_additional_gens: int,
    seed: int,
    max_workers: int,
    hourly_rate_usd: float,
    hard_budget_usd: float,
) -> None:
    paths.ensure_directories()
    _redirect_t80_paths_to_t83()
    # Override hard budget cap.
    t80_loop._HARD_BUDGET_USD = hard_budget_usd  # type: ignore[attr-defined]
    t80_loop._LOOP_START_TIME = time.time()  # type: ignore[attr-defined]
    t80_loop._HOURLY_RATE_USD = hourly_rate_usd  # type: ignore[attr-defined]

    # Pre-load t0081 evaluation history into the module global so saved
    # files contain the union (additive, not destructive).
    n_loaded = _load_t0081_evaluations_into_module()
    assert n_loaded == N_T0081_EVALUATIONS, (
        f"expected {N_T0081_EVALUATIONS} t0081 evaluations, loaded {n_loaded}"
    )
    print(
        f"[t0083] pre-loaded {n_loaded} t0081 evaluations into _ALL_EVALUATIONS",
        flush=True,
    )

    problem = t80_loop.BedBV3Problem(max_workers=max_workers)
    # Pre-set eval_count so first true offspring evaluation lands at gen 8.
    problem.eval_count = N_T0081_EVALUATIONS

    # Reload t0081 gen-7 survivors with X/F/G + evaluated marker so pymoo
    # skips re-evaluation on the resumed initial population.
    survivors = reload_gen7.reload_t0081_gen7_survivors(problem=problem, seed=seed)
    assert len(survivors) == pop_size, f"survivor pool size {len(survivors)} != pop_size {pop_size}"

    algorithm = NSGA2(
        pop_size=pop_size,
        sampling=survivors,
        crossover=SBX(eta=SBX_ETA, prob=0.9),
        mutation=PM(eta=PM_ETA),
        eliminate_duplicates=True,
    )
    termination = TerminationCollection(
        MaximumGenerationTermination(max_additional_gens),
        HVPlateauTermination(),
    )
    print(
        f"[t0083] starting continuation NSGA-II: pop_size={pop_size} "
        f"max_additional_gens={max_additional_gens} seed={seed} "
        f"max_workers={max_workers} hourly_rate=${hourly_rate_usd:.4f} "
        f"hard_budget=${hard_budget_usd:.2f}",
        flush=True,
    )
    minimize(
        problem,
        algorithm,
        termination,
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
    final_cost: float = t80_loop._elapsed_cost_usd()  # type: ignore[attr-defined]
    n_evals: int = len(t80_loop._ALL_EVALUATIONS)  # type: ignore[attr-defined]
    n_new = n_evals - N_T0081_EVALUATIONS
    print(
        f"[t0083] done: {n_evals} total evaluations ({N_T0081_EVALUATIONS} from t0081 + "
        f"{n_new} new); final cost ${final_cost:.4f} (cap ${hard_budget_usd:.2f})",
        flush=True,
    )


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pop-size", type=int, default=POP_SIZE)
    parser.add_argument("--max-gen", type=int, default=T0083_MAX_ADDITIONAL_GENERATIONS)
    parser.add_argument("--seed", type=int, default=LHS_SEED)
    parser.add_argument("--max-workers", type=int, default=0)
    parser.add_argument("--hourly-rate-usd", type=float, default=HOURLY_RATE_USD)
    parser.add_argument("--cost-cap", type=float, default=T0083_HARD_BUDGET_USD)
    args = parser.parse_args()
    _run_continuation_nsga2(
        pop_size=args.pop_size,
        max_additional_gens=args.max_gen,
        seed=args.seed,
        max_workers=args.max_workers,
        hourly_rate_usd=args.hourly_rate_usd,
        hard_budget_usd=args.cost_cap,
    )
    return 0


if __name__ == "__main__":
    sys.exit(_main())
