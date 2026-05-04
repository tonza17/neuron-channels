"""NSGA-II MOBO loop on the t0080 v3 substrate (REQ-6, REQ-8, REQ-13, REQ-17).

Replaces t0078's BoTorch qLogNEHVI with pymoo NSGA-II. Population batch
evaluation uses the t0078 NEURON-fresh-subprocess pattern verbatim (the trial
driver's ``ProcessPoolExecutor`` fans out per-cell evaluations to worker
subprocesses); pymoo is invoked WITHOUT ``StarmapParallelization`` to avoid
double-nesting (REQ-17).

Hard biological constraint: AIS-to-soma Nav ratio >= 5 (Werginz 2024;
REQ-8). Hard parameter lower bound: ``nav16_ais >= 0.25`` S/cm^2 (Kole 2008;
REQ-7) is enforced by the constants.py LOWER_BOUNDS array.

Cost watchdog: per-cell elapsed-time check against $2.00 hard cap (REQ-13,
REQ-19). On trip, writes ``intervention/budget_overrun.md`` and exits.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

# pymoo imports — pin >= 0.6.1.6 for the StarmapParallelization path fix.
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.indicators.hv import Hypervolume
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.lhs import LHS
from pymoo.optimize import minimize

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    ANGLES_8DIR_DEG,
    HARD_BUDGET_USD,
    HOURLY_RATE_USD,
    HV_UTOPIA_DSI,
    HV_UTOPIA_RATE_HZ,
    LHS_SEED,
    LOWER_BOUNDS,
    N_GENERATIONS,
    N_PARAMS,
    N_SEEDS,
    PM_ETA,
    POP_SIZE,
    REF_POINT_DSI,
    REF_POINT_RATE_HZ,
    SBX_ETA,
    SOFT_BUDGET_USD,
    UPPER_BOUNDS,
    WORST_CASE_DSI,
    WORST_CASE_RATE_HZ,
    ParameterVector,
    ParamIndex,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.paths import (
    BUDGET_OVERRUN_MD,
    INTERVENTION_DIR,
    PARETO_FRONT_JSON,
    RESULTS_DATA_DIR,
    ensure_directories,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import (
    EvalResult,
    evaluate_parameter_vector,
)


@dataclass(frozen=True, slots=True)
class CellEvaluation:
    cell_index: int
    generation: int
    params: list[float]
    dsi: float
    pd_rate_hz: float
    is_unstable: bool
    peak_vm_mv: float
    elapsed_s: float
    constraint_violation: float
    is_feasible: bool


# Module-level state for the cost watchdog.
_LOOP_START_TIME: float = 0.0
_HOURLY_RATE_USD: float = HOURLY_RATE_USD
_HARD_BUDGET_USD: float = HARD_BUDGET_USD
_BUDGET_TRIPPED: bool = False
_CELL_INDEX_GLOBAL: int = 0
_GENERATION_GLOBAL: int = 0
_ALL_EVALUATIONS: list[CellEvaluation] = []


def _elapsed_cost_usd() -> float:
    elapsed_s = time.time() - _LOOP_START_TIME
    return (elapsed_s / 3600.0) * _HOURLY_RATE_USD


def _trip_budget_overrun_if_needed() -> bool:
    """Return True if budget overrun was tripped (caller should halt)."""
    global _BUDGET_TRIPPED
    cost = _elapsed_cost_usd()
    if cost >= _HARD_BUDGET_USD and not _BUDGET_TRIPPED:
        _BUDGET_TRIPPED = True
        INTERVENTION_DIR.mkdir(parents=True, exist_ok=True)
        BUDGET_OVERRUN_MD.write_text(
            "# Budget Overrun\n\n"
            f"NSGA-II loop tripped the $2.00 hard cap at "
            f"cell {_CELL_INDEX_GLOBAL} / generation {_GENERATION_GLOBAL}.\n\n"
            f"- Elapsed cost (USD): {cost:.4f}\n"
            f"- Hourly rate (USD/hr): {_HOURLY_RATE_USD:.4f}\n"
            f"- Soft budget: ${SOFT_BUDGET_USD}\n"
            f"- Hard budget: ${HARD_BUDGET_USD}\n"
            f"- Hard cap tripped at: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n"
            "\nThe partial Pareto front is in results/data/pareto_front.json.\n",
            encoding="utf-8",
        )
    return _BUDGET_TRIPPED


class BedBV3Problem(Problem):
    """pymoo Problem subclass: 54-d MOBO with one inequality constraint.

    n_ieq_constr = 1 (REQ-8): AIS-to-soma Nav ratio >= 5
    encoded as ``g(x) = 5 - nav16_ais / nav16_soma <= 0``.
    """

    def __init__(self, *, max_workers: int) -> None:
        super().__init__(
            n_var=N_PARAMS,
            n_obj=2,
            n_ieq_constr=1,
            xl=LOWER_BOUNDS,
            xu=UPPER_BOUNDS,
            elementwise_evaluation=False,
        )
        self.max_workers: int = max_workers
        self.eval_count: int = 0

    def _evaluate(
        self,
        x: NDArray[np.float64],
        out: dict[str, NDArray[np.float64]],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        global _CELL_INDEX_GLOBAL, _GENERATION_GLOBAL
        n_individuals: int = x.shape[0]
        f: NDArray[np.float64] = np.zeros((n_individuals, 2), dtype=np.float64)
        g: NDArray[np.float64] = np.zeros((n_individuals, 1), dtype=np.float64)
        gen: int = self.eval_count // POP_SIZE
        for i in range(n_individuals):
            _CELL_INDEX_GLOBAL = self.eval_count + i
            _GENERATION_GLOBAL = gen
            if _trip_budget_overrun_if_needed():
                # Set to worst-case for remaining cells; minimization sense.
                f[i, 0] = -WORST_CASE_DSI
                f[i, 1] = -WORST_CASE_RATE_HZ
                # Constraint violation set to worst-case so cell is dominated.
                g[i, 0] = 100.0
                continue
            params = ParameterVector(values=x[i].copy())
            t0 = time.time()
            try:
                eval_res: EvalResult = evaluate_parameter_vector(
                    params=params,
                    angles_deg=ANGLES_8DIR_DEG,
                    n_seeds=N_SEEDS,
                    max_workers=self.max_workers,
                )
            except (RuntimeError, ValueError, ArithmeticError, AssertionError) as exc:
                print(f"[gen {gen} cell {i}] error: {exc}", flush=True)
                f[i, 0] = -WORST_CASE_DSI
                f[i, 1] = -WORST_CASE_RATE_HZ
                g[i, 0] = 100.0
                continue
            elapsed_s = time.time() - t0
            # Sign-flip for pymoo's minimisation convention.
            dsi_to_record = eval_res.dsi if not eval_res.is_unstable else WORST_CASE_DSI
            pd_rate_to_record = (
                eval_res.pd_rate_hz if not eval_res.is_unstable else WORST_CASE_RATE_HZ
            )
            f[i, 0] = -dsi_to_record
            f[i, 1] = -pd_rate_to_record
            # Constraint: AIS-to-soma Nav ratio >= 5 (REQ-8).
            nav16_ais: float = float(x[i, int(ParamIndex.NAV16_AIS_GBAR)])
            nav16_soma: float = float(x[i, int(ParamIndex.NAV16_SOMA_GBAR)])
            ratio = float("inf") if nav16_soma <= 0 else nav16_ais / nav16_soma
            g[i, 0] = 5.0 - ratio
            is_feasible: bool = bool(g[i, 0] <= 0.0)
            evaluation = CellEvaluation(
                cell_index=_CELL_INDEX_GLOBAL,
                generation=gen,
                params=[float(v) for v in x[i]],
                dsi=eval_res.dsi,
                pd_rate_hz=eval_res.pd_rate_hz,
                is_unstable=eval_res.is_unstable,
                peak_vm_mv=eval_res.peak_vm_mv,
                elapsed_s=elapsed_s,
                constraint_violation=float(g[i, 0]),
                is_feasible=is_feasible,
            )
            _ALL_EVALUATIONS.append(evaluation)
            cost = _elapsed_cost_usd()
            print(
                f"[gen {gen} cell {i}/{n_individuals}] "
                f"dsi={eval_res.dsi:.3f} pd={eval_res.pd_rate_hz:.2f}Hz "
                f"unstable={eval_res.is_unstable} "
                f"feasible={is_feasible} ratio={ratio:.2f} "
                f"elapsed={elapsed_s:.1f}s cost=${cost:.3f}",
                flush=True,
            )
        self.eval_count += n_individuals
        out["F"] = f
        out["G"] = g


def _compute_hypervolume(
    *,
    objectives: NDArray[np.float64],
    is_feasible: NDArray[np.bool_],
) -> float:
    """Compute hypervolume on the feasible front. objectives are minimised (-DSI, -PD)."""
    feasible_obj = objectives[is_feasible]
    if feasible_obj.shape[0] == 0:
        return 0.0
    # ref point in minimisation = -REF_POINT_DSI, -REF_POINT_RATE_HZ but we
    # want feasible points to have negative coordinates so they are below the
    # ref point (REF point above all points).
    ref_point = np.array([-REF_POINT_DSI, -REF_POINT_RATE_HZ], dtype=np.float64)
    # Replace any worst-case sentinels (e.g. dsi=-1) with ref point so they
    # do not contribute negative HV.
    valid = (feasible_obj[:, 0] <= 0.0) & (feasible_obj[:, 1] <= 0.0)
    feasible_obj = feasible_obj[valid]
    if feasible_obj.shape[0] == 0:
        return 0.0
    hv_indicator = Hypervolume(ref_point=ref_point)
    return float(hv_indicator.do(feasible_obj))


def _save_pareto_front(*, all_evaluations: list[CellEvaluation]) -> None:
    """Extract non-dominated feasible cells and write pareto_front.json."""
    feasible = [e for e in all_evaluations if e.is_feasible and not e.is_unstable]
    pareto: list[CellEvaluation] = []
    for cand in feasible:
        dominated = False
        for other in feasible:
            if other is cand:
                continue
            if (
                other.dsi >= cand.dsi
                and other.pd_rate_hz >= cand.pd_rate_hz
                and (other.dsi > cand.dsi or other.pd_rate_hz > cand.pd_rate_hz)
            ):
                dominated = True
                break
        if not dominated:
            pareto.append(cand)
    PARETO_FRONT_JSON.parent.mkdir(parents=True, exist_ok=True)
    PARETO_FRONT_JSON.write_text(
        json.dumps(
            {"cells": [asdict(c) for c in pareto], "n_total": len(all_evaluations)},
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        f"[pareto] {len(pareto)} non-dominated feasible cells out of {len(all_evaluations)} total",
        flush=True,
    )


def _save_all_evaluations(*, all_evaluations: list[CellEvaluation]) -> None:
    """Write the full per-cell evaluation log."""
    out_path: Path = RESULTS_DATA_DIR / "all_evaluations.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps([asdict(c) for c in all_evaluations], indent=2),
        encoding="utf-8",
    )


def _save_hv_trajectory(*, all_evaluations: list[CellEvaluation]) -> None:
    """Compute per-generation hypervolume against the t0076/t0078 utopia point."""
    if len(all_evaluations) == 0:
        return
    by_gen: dict[int, list[CellEvaluation]] = {}
    for e in all_evaluations:
        by_gen.setdefault(e.generation, []).append(e)
    trajectory: list[dict[str, Any]] = []
    cumulative: list[CellEvaluation] = []
    ref_point = np.array([-REF_POINT_DSI, -REF_POINT_RATE_HZ], dtype=np.float64)
    for gen in sorted(by_gen.keys()):
        cumulative.extend(by_gen[gen])
        feasible = [e for e in cumulative if e.is_feasible and not e.is_unstable]
        if len(feasible) == 0:
            hv = 0.0
        else:
            obj = np.array([[-e.dsi, -e.pd_rate_hz] for e in feasible], dtype=np.float64)
            valid = (obj[:, 0] <= 0.0) & (obj[:, 1] <= 0.0)
            obj_v = obj[valid]
            hv = 0.0 if obj_v.shape[0] == 0 else float(Hypervolume(ref_point=ref_point).do(obj_v))
        trajectory.append({"generation": gen, "n_evaluations": len(cumulative), "hypervolume": hv})
    out_path: Path = RESULTS_DATA_DIR / "hv_trajectory.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(
            {"utopia_point": [HV_UTOPIA_DSI, HV_UTOPIA_RATE_HZ], "trajectory": trajectory}, indent=2
        ),
        encoding="utf-8",
    )


def run_nsga2_loop(
    *,
    pop_size: int,
    n_gen: int,
    seed: int,
    max_workers: int,
    hourly_rate_usd: float,
) -> None:
    """Main entry-point for the NSGA-II loop."""
    global _LOOP_START_TIME, _HOURLY_RATE_USD, _ALL_EVALUATIONS
    ensure_directories()
    _LOOP_START_TIME = time.time()
    _HOURLY_RATE_USD = hourly_rate_usd
    _ALL_EVALUATIONS = []
    problem = BedBV3Problem(max_workers=max_workers)
    algorithm = NSGA2(
        pop_size=pop_size,
        sampling=LHS(),
        crossover=SBX(eta=SBX_ETA, prob=0.9),
        mutation=PM(eta=PM_ETA),
        eliminate_duplicates=True,
    )
    print(
        f"[nsga2] starting: pop_size={pop_size} n_gen={n_gen} seed={seed} "
        f"max_workers={max_workers} hourly_rate=${hourly_rate_usd:.4f}",
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
    _save_all_evaluations(all_evaluations=_ALL_EVALUATIONS)
    _save_pareto_front(all_evaluations=_ALL_EVALUATIONS)
    _save_hv_trajectory(all_evaluations=_ALL_EVALUATIONS)
    final_cost = _elapsed_cost_usd()
    print(
        f"[nsga2] done: {len(_ALL_EVALUATIONS)} evaluations, "
        f"final cost ${final_cost:.4f} (cap ${HARD_BUDGET_USD})",
        flush=True,
    )


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--smoke", action="store_true", help="Run a small smoke test (pop=4, gen=2)"
    )
    parser.add_argument("--pop-size", type=int, default=POP_SIZE)
    parser.add_argument("--n-gen", type=int, default=N_GENERATIONS)
    parser.add_argument("--seed", type=int, default=LHS_SEED)
    parser.add_argument(
        "--max-workers", type=int, default=0, help="0 -> cpu_count()-1 in the trial driver"
    )
    parser.add_argument("--hourly-rate-usd", type=float, default=HOURLY_RATE_USD)
    args = parser.parse_args()
    pop = 4 if args.smoke else args.pop_size
    gens = 2 if args.smoke else args.n_gen
    workers = args.max_workers
    if args.smoke and workers == 0:
        workers = 1  # sequential for debuggable smoke
    run_nsga2_loop(
        pop_size=pop,
        n_gen=gens,
        seed=args.seed,
        max_workers=workers,
        hourly_rate_usd=args.hourly_rate_usd,
    )
    return 0


if __name__ == "__main__":
    sys.exit(_main())
