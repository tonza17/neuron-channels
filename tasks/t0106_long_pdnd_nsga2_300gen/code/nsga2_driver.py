"""t0106 per-seed NSGA-II driver — long-run 2-direction 68-d random-init NSGA-II.

Adapted from t0104's `nsga2_driver`. t0106 differences:

* Single GA seed (44) at pop = 96, n_gen = 300 (hard cap, extendable via
  --n-gen-override). 2 directions (PD = 0, ND = 180), N_EVAL_SEEDS = 3.
* `OperatorStopTermination` polls ``intervention/stop.md`` each generation
  and triggers a clean halt at the next generation boundary (REQ-5).
* `_GenerationCallback` writes one JSONL line per gen to ``hv_trace.jsonl``
  with fields ``gen``, ``wall_clock_s``, ``hv``, ``n_cells_evaluated``
  (REQ-4), and dill-dumps the pymoo Algorithm to
  ``checkpoint_seed<s>_gen<NNNN>.pkl``.
* `PerGenerationPoolRestart` closes the multiprocessing.Pool every 25
  generations and recreates it, swapping ``problem.elementwise_runner`` to
  the fresh ``StarmapParallelization`` (REQ-6). This pattern is NEW in
  the lineage (not present in t0102 / t0104) and is load-bearing for
  300-gen NEURON memory mitigation.
* `HVPlateauTermination` is kept but with `MIN_HV_HISTORY = 60` (1-hour
  sliding window at ~60 s/gen) so it does not spuriously trigger on long
  runs.
* `CostWatchdogTermination` reads ``T0106_HARD_BUDGET_USD = 25.00`` as
  the per-instance cap.
"""

from __future__ import annotations

import json
import subprocess
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from multiprocessing import Pool, cpu_count
from pathlib import Path
from typing import Any

import dill
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

from tasks.t0106_long_pdnd_nsga2_300gen.code.constants import (
    HV_UTOPIA_DSI,
    HV_UTOPIA_PD_RATE_HZ,
    N_EVAL_SEEDS,
    N_GEN,
    PM_ETA,
    PM_PROB,
    POP_SIZE,
    REF_POINT_HV,
    SBX_ETA,
    SBX_PROB,
    T0106_HARD_BUDGET_USD,
)
from tasks.t0106_long_pdnd_nsga2_300gen.code.cost_watchdog import (
    make_watchdog_from_machine_log,
)
from tasks.t0106_long_pdnd_nsga2_300gen.code.evaluator import (
    BedBV3MorphProblem,
)
from tasks.t0106_long_pdnd_nsga2_300gen.code.hv_plateau_watchdog import (
    HVPlateauTermination,
)
from tasks.t0106_long_pdnd_nsga2_300gen.code.paths import (
    ALGORITHM_CONFIG_JSON,
    EVALUATION_SEEDS_JSON,
    MACHINE_LOG_JSON,
    all_evaluations_json,
    budget_overrun_md,
    checkpoint_dill,
    checkpoint_json,
    ensure_directories,
    hv_trace_jsonl,
    hv_trajectory_json,
    init_pop_json,
    pareto_front_json,
    stop_signal_md,
)

_HOURLY_RATE_USD: float = 0.30  # patched at runtime by cost_watchdog.patch_t99_loop_rate

# REQ-6: pool restart cadence (load-bearing for NEURON memory mitigation at 300 gens).
_POOL_RESTART_EVERY: int = 25

# REQ-8 (S-0102-08 partial fix): when True, the run_nsga2_for_seed finally
# block invokes `vastai destroy instance <id>` if the cost watchdog tripped.
# Default False so smoke gates and local runs do not destroy anything.
# Production path enables it via the --teardown-on-watchdog CLI flag.
TEARDOWN_ON_WATCHDOG: bool = False


def _teardown_vast_instance(*, instance_id: str) -> None:
    """Invoke `vastai destroy instance <id>` as a subprocess.

    Tolerant of missing `vastai` binary (e.g., on Windows local dev): logs
    the failure but does not raise.
    """
    try:
        result = subprocess.run(
            ["vastai", "destroy", "instance", instance_id],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        print(
            f"[nsga2_driver teardown] vastai destroy instance {instance_id} "
            f"exit={result.returncode} stdout={result.stdout.strip()} "
            f"stderr={result.stderr.strip()}"
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        print(
            f"[nsga2_driver teardown] WARNING: vastai destroy failed "
            f"({type(exc).__name__}: {exc}); instance {instance_id} may "
            f"still be billing — verify manually."
        )


@dataclass(slots=True)
class _DriverState:
    seed: int
    started_at: datetime
    instance_started_at: datetime
    cost_watchdog: Any
    all_evaluations: list[dict[str, object]]
    hv_trajectory: list[dict[str, object]]
    pop_snapshots: list[dict[str, object]]
    step_id: str
    start_wall_s: float


class OperatorStopTermination(Termination):
    """Poll ``intervention/stop.md`` each generation; trigger on file exists.

    REQ-5: the operator can drop ``stop.md`` into ``intervention/`` to halt
    NSGA-II cleanly at the next generation boundary. This is one of four
    terminations in the ``TerminationCollection`` and never races with the
    others.
    """

    def __init__(self, *, stop_path: Path) -> None:
        super().__init__()
        self._stop_path = stop_path

    def _update(self, algorithm: object) -> float:  # type: ignore[override]
        if self._stop_path.exists():
            print(
                f"[operator_stop] stop signal detected at {self._stop_path}; "
                f"terminating NSGA-II at next gen boundary"
            )
            return 1.0
        return 0.0


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
    # REQ-4: shrink HV reference point from 3 to 2 entries to match the
    # 2-column F matrix (DSI, PD-rate) returned by BedBV3MorphProblem with
    # n_obj=2.
    ref_point = np.array([0.0, 0.0], dtype=np.float64)
    if F_neg.size == 0:
        return 0.0
    hv = HV(ref_point=ref_point)
    return float(hv.do(F_neg))


def _append_hv_trace_line(
    *,
    state: _DriverState,
    generation: int,
    hv: float,
    n_cells_evaluated: int,
) -> None:
    """REQ-4: append one JSON line per generation to ``hv_trace.jsonl``.

    Schema (per ``task_description.md``):
    ``{gen, wall_clock_s, hv, n_cells_evaluated}``.
    """
    trace_path = hv_trace_jsonl(step_id=state.step_id)
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    line = {
        "gen": int(generation),
        "wall_clock_s": float(time.time() - state.start_wall_s),
        "hv": float(hv),
        "n_cells_evaluated": int(n_cells_evaluated),
    }
    with trace_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")


def _dill_checkpoint_algorithm(
    *,
    state: _DriverState,
    generation: int,
    algorithm: Any,
) -> None:
    """REQ-4: dill-dump the pymoo Algorithm object every gen for resume."""
    ckpt = checkpoint_dill(seed=state.seed, gen=generation, step_id=state.step_id)
    ckpt.parent.mkdir(parents=True, exist_ok=True)
    try:
        with ckpt.open("wb") as f:
            dill.dump(algorithm, f)
    except Exception as exc:  # noqa: BLE001
        # dill on Pool-backed algorithms can fail for unrelated reasons;
        # the trace + per-gen evaluations json are the primary recovery
        # channels, so we tolerate checkpoint failure.
        print(
            f"[nsga2_driver seed={state.seed} gen={generation}] WARNING: "
            f"dill checkpoint failed ({type(exc).__name__}: {exc}); "
            f"trace + evaluations still written"
        )


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
    # REQ-4: append one JSON line per generation to hv_trace.jsonl.
    _append_hv_trace_line(
        state=state,
        generation=generation,
        hv=hv,
        n_cells_evaluated=int(len(population_X)),
    )
    print(
        f"[seed {state.seed} gen {generation}] HV={hv:.4f}  pop_size={len(population_X)}  "
        f"cost_so_far=${cost_so_far_usd:.4f}  elapsed={elapsed_s:.0f}s"
    )


class _GenerationCallback(Callback):
    def __init__(
        self,
        *,
        state: _DriverState,
        rate_usd_per_hour: float,
        problem: BedBV3MorphProblem,
    ) -> None:
        super().__init__()
        self._state = state
        self._rate = rate_usd_per_hour
        self._problem = problem

    def notify(self, algorithm: Any) -> None:  # type: ignore[override]
        gen = int(algorithm.n_gen)
        pop = algorithm.pop
        X = np.array([ind.X for ind in pop], dtype=np.float64)
        F = np.array([ind.F for ind in pop], dtype=np.float64)
        _save_iteration(
            state=self._state,
            generation=gen,
            population_X=X,
            population_F=F,
            rate_usd_per_hour=self._rate,
        )
        # REQ-4: per-generation dill checkpoint after the JSONL trace line.
        _dill_checkpoint_algorithm(
            state=self._state,
            generation=gen,
            algorithm=algorithm,
        )


class PerGenerationPoolRestart(Callback):
    """REQ-6: close + recreate the multiprocessing.Pool every N generations.

    This is the load-bearing memory mitigation for 300-gen runs. NEURON
    accumulates memory in worker processes (cf. t0102 risk row); the t0102 /
    t0104 lineage runs a single Pool for the entire ``minimize()`` call,
    which is acceptable at ~20 gens but blows out at 300. This callback
    closes the current pool, terminates workers, recreates the pool, and
    swaps ``problem.elementwise_runner`` to a fresh
    ``StarmapParallelization`` so the next generation's evaluations route
    through the new pool.
    """

    def __init__(
        self,
        *,
        problem: BedBV3MorphProblem,
        pool_holder: dict[str, Any],
        n_workers: int,
        restart_every: int = _POOL_RESTART_EVERY,
    ) -> None:
        super().__init__()
        self._problem = problem
        self._pool_holder = pool_holder
        self._n_workers = n_workers
        self._restart_every = restart_every

    def notify(self, algorithm: Any) -> None:  # type: ignore[override]
        gen = int(algorithm.n_gen)
        if gen <= 0 or gen % self._restart_every != 0:
            return
        old_pool = self._pool_holder.get("pool")
        if old_pool is None:
            return
        print(
            f"[pool_restart gen={gen}] closing/recreating multiprocessing.Pool "
            f"({self._n_workers} workers) — REQ-6 memory mitigation"
        )
        try:
            old_pool.close()
            old_pool.terminate()
        except Exception as exc:  # noqa: BLE001
            print(
                f"[pool_restart gen={gen}] WARNING: old pool teardown failed "
                f"({type(exc).__name__}: {exc}); continuing with fresh pool"
            )
        new_pool = Pool(processes=self._n_workers)
        new_runner = StarmapParallelization(new_pool.starmap)
        self._pool_holder["pool"] = new_pool
        self._problem.elementwise_runner = new_runner
        print(
            f"[pool_restart gen={gen}] new Pool + runner installed; "
            f"resuming NSGA-II at gen {gen + 1}"
        )


class _CompositeCallback(Callback):
    """Chain multiple callbacks; notifies each in registration order."""

    def __init__(self, *, callbacks: list[Callback]) -> None:
        super().__init__()
        self._callbacks = callbacks

    def notify(self, algorithm: Any) -> None:  # type: ignore[override]
        for cb in self._callbacks:
            cb.notify(algorithm)


def _load_init_matrix(*, seed: int) -> NDArray[np.float64]:
    payload = json.loads(init_pop_json(seed=seed).read_text(encoding="utf-8"))
    matrix = np.array(payload["matrix"], dtype=np.float64)
    assert matrix.shape == (POP_SIZE, 68), f"init pop shape {matrix.shape} != (96, 68)"
    return matrix


def _eval_seeds() -> list[int]:
    """Deterministic evaluation seeds (kept identical to t0091 for parity)."""
    ss = np.random.SeedSequence(42)
    seeds = [int(s.generate_state(1)[0]) for s in ss.spawn(N_EVAL_SEEDS)]
    EVALUATION_SEEDS_JSON.parent.mkdir(parents=True, exist_ok=True)
    EVALUATION_SEEDS_JSON.write_text(
        json.dumps({"seeds": seeds, "method": "np.random.SeedSequence(42).spawn(3)"}, indent=2),
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
        # REQ-6: 2-entry hv_utopia (robustness dropped from selection).
        "hv_utopia": [HV_UTOPIA_DSI, HV_UTOPIA_PD_RATE_HZ],
        "hard_budget_usd": T0106_HARD_BUDGET_USD,
        "sampling_method": "pymoo.operators.sampling.lhs.LatinHypercubeSampling",
        "pool_restart_every": _POOL_RESTART_EVERY,
    }
    ALGORITHM_CONFIG_JSON.parent.mkdir(parents=True, exist_ok=True)
    ALGORITHM_CONFIG_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")


def _read_instance_id_from_machine_log() -> str | None:
    """Read the active Vast.ai instance ID from machine_log.json.

    Returns the most recently created instance's ``instance_id``, or None if
    the log is missing/empty.
    """
    if not MACHINE_LOG_JSON.exists():
        return None
    try:
        records = json.loads(MACHINE_LOG_JSON.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(records, list) or len(records) == 0:
        return None
    last = records[-1]
    if not isinstance(last, dict):
        return None
    instance_id = last.get("instance_id")
    if instance_id is None:
        return None
    return str(instance_id)


def run_nsga2_for_seed(
    *,
    task_seed: int,
    n_gen_override: int | None = None,
    step_id: str = "009_implementation",
) -> dict[str, object]:
    """Run NSGA-II for a single random-init task seed (t0106 long-run version).

    Adds operator-stop, hv_trace.jsonl, per-gen dill checkpoint, and the
    PerGenerationPoolRestart callback.
    """
    ensure_directories()
    eval_seeds = _eval_seeds()
    init_matrix = _load_init_matrix(seed=task_seed)

    instance_started_at = datetime.now(UTC)
    cost_watchdog = make_watchdog_from_machine_log(
        machine_log_path=MACHINE_LOG_JSON,
        instance_started_at=instance_started_at,
        hard_budget_usd=T0106_HARD_BUDGET_USD,
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
        step_id=step_id,
        start_wall_s=time.time(),
    )

    n_workers: int = min(60, max(1, (cpu_count() or 4) - 4))
    print(f"[nsga2_driver seed={task_seed}] using {n_workers} parallel workers")
    pool: Pool = Pool(processes=n_workers)
    pool_holder: dict[str, Any] = {"pool": pool}
    runner = StarmapParallelization(pool.starmap)
    problem = BedBV3MorphProblem(eval_seeds=eval_seeds, elementwise_runner=runner)

    algorithm = NSGA2(
        pop_size=POP_SIZE,
        sampling=init_matrix,
        crossover=SBX(eta=SBX_ETA, prob=SBX_PROB),
        mutation=PM(eta=PM_ETA, prob=PM_PROB),
        eliminate_duplicates=True,
    )

    n_gen_effective = int(n_gen_override) if n_gen_override is not None else N_GEN
    termination = TerminationCollection(
        MaximumGenerationTermination(n_max_gen=n_gen_effective),
        HVPlateauTermination(seed=task_seed),
        CostWatchdogTermination(watchdog=cost_watchdog, seed=task_seed),
        OperatorStopTermination(stop_path=stop_signal_md()),
    )

    gen_callback = _GenerationCallback(
        state=state,
        rate_usd_per_hour=rate,
        problem=problem,
    )
    pool_restart_callback = PerGenerationPoolRestart(
        problem=problem,
        pool_holder=pool_holder,
        n_workers=n_workers,
        restart_every=_POOL_RESTART_EVERY,
    )
    callback = _CompositeCallback(callbacks=[gen_callback, pool_restart_callback])

    print(
        f"[nsga2_driver seed={task_seed}] starting: pop={POP_SIZE} max_gen={n_gen_effective} "
        f"hard_cap=${T0106_HARD_BUDGET_USD:.2f} rate=${rate:.4f}/hr "
        f"pool_restart_every={_POOL_RESTART_EVERY}"
    )
    t_start = time.time()
    res: Any = None
    try:
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
    finally:
        elapsed_final = time.time() - t_start
        final_cost = cost_watchdog.current_cost_usd()
        try:
            current_pool = pool_holder.get("pool")
            if current_pool is not None:
                current_pool.close()
                current_pool.terminate()
        except Exception as exc:  # noqa: BLE001
            print(
                f"[nsga2_driver seed={task_seed}] WARNING: pool teardown "
                f"failed: {type(exc).__name__}: {exc}"
            )
        print(
            f"[nsga2_driver seed={task_seed}] FINISHED in "
            f"{elapsed_final:.0f}s ({elapsed_final / 60:.1f} min); "
            f"final cost=${final_cost:.4f}; tripped={cost_watchdog.tripped}"
        )
        if TEARDOWN_ON_WATCHDOG and cost_watchdog.tripped:
            instance_id = _read_instance_id_from_machine_log()
            if instance_id is not None:
                print(
                    f"[nsga2_driver seed={task_seed}] cost watchdog tripped; "
                    f"invoking Vast.ai teardown for instance {instance_id}"
                )
                _teardown_vast_instance(instance_id=instance_id)
            else:
                print(
                    f"[nsga2_driver seed={task_seed}] cost watchdog tripped "
                    f"but no instance_id found in machine_log.json; skipping "
                    f"vastai destroy"
                )

    elapsed = time.time() - t_start
    final_cost = cost_watchdog.current_cost_usd()
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

    parser = argparse.ArgumentParser(description="t0106 NSGA-II long-run driver (one seed)")
    parser.add_argument("--seed", type=int, required=True, help="Task RNG seed")
    parser.add_argument(
        "--pop",
        type=int,
        default=POP_SIZE,
        help=f"Population size (default {POP_SIZE}).",
    )
    parser.add_argument(
        "--n-gen",
        type=int,
        default=N_GEN,
        help=f"Maximum number of generations (default {N_GEN}).",
    )
    parser.add_argument(
        "--n-eval-seeds",
        type=int,
        default=N_EVAL_SEEDS,
        help=(
            f"Number of evaluation seeds (default {N_EVAL_SEEDS}). "
            f"Informational; the constant in constants_morphology drives the run."
        ),
    )
    parser.add_argument(
        "--n-directions",
        type=int,
        default=2,
        help="Number of angular directions (default 2 for t0106).",
    )
    parser.add_argument(
        "--obj-mode",
        type=str,
        default="ratio_dsi_pdrate",
        help="Objective mode label (informational; baked into evaluator).",
    )
    parser.add_argument(
        "--hv-trace-path",
        type=str,
        default=None,
        help=(
            "Override path for hv_trace.jsonl (default: "
            "logs/steps/009_implementation/hv_trace.jsonl)."
        ),
    )
    parser.add_argument(
        "--stop-signal",
        type=str,
        default=None,
        help=("Override path for operator-stop signal (default: intervention/stop.md)."),
    )
    parser.add_argument(
        "--checkpoint-dir",
        type=str,
        default=None,
        help=(
            "Override directory for dill checkpoints (default: "
            "logs/steps/009_implementation/checkpoints)."
        ),
    )
    parser.add_argument(
        "--save-algorithm-config",
        action="store_true",
        help="Write algorithm_config.json (do this once across the run)",
    )
    parser.add_argument(
        "--task-seeds",
        type=int,
        nargs="+",
        default=None,
        help="Task seeds for the algorithm_config (defaults to T0106_SEEDS)",
    )
    parser.add_argument(
        "--teardown-on-watchdog",
        action="store_true",
        help=(
            "When the cost watchdog trips, invoke ``vastai destroy "
            "instance <id>`` in the finally block to prevent post-NSGA-II "
            "idle billing. Default off so smoke gates and local runs do "
            "not destroy anything."
        ),
    )
    args = parser.parse_args()
    if args.teardown_on_watchdog:
        global TEARDOWN_ON_WATCHDOG
        TEARDOWN_ON_WATCHDOG = True
    if args.save_algorithm_config:
        from tasks.t0106_long_pdnd_nsga2_300gen.code.constants import T0106_SEEDS

        eval_seeds = _eval_seeds()
        task_seeds = args.task_seeds if args.task_seeds is not None else list(T0106_SEEDS)
        _save_algorithm_config(eval_seeds=eval_seeds, task_seeds=task_seeds)
    summary = run_nsga2_for_seed(
        task_seed=int(args.seed),
        n_gen_override=int(args.n_gen) if args.n_gen is not None else None,
    )
    print("[nsga2_driver] summary:", json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
