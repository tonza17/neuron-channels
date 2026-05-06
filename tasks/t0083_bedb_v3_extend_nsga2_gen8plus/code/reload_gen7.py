"""Rebuild t0081's gen-7 survivor pool from saved evaluation history (REQ-3).

Procedure:
1. Load the 768 ``CellEvaluation`` records from
   ``tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json``.
2. Filter to records with ``generation in {6, 7}`` (192 records).
3. Build a 192-individual ``Population`` with X/F/G keys; substitute worst-case
   sentinels (``WORST_CASE_DSI=-1.0``, ``WORST_CASE_RATE_HZ=0.0``) for cells
   marked ``is_unstable=True`` so F matches what NSGA-II actually saw.
4. Mark each individual ``evaluated={"F","G"}`` so pymoo's
   ``Evaluator.eval`` skips re-evaluation.
5. Run ``RankAndCrowding().do(problem, pop, n_survive=96, random_state=...)``
   with explicit seed (``LHS_SEED``) to deterministically recover the gen-7
   survivors NSGA-II selected at end-of-gen-7.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from pymoo.algorithms.moo.nsga2 import RankAndCrowding
from pymoo.core.population import Population

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    LHS_SEED,
    POP_SIZE,
    WORST_CASE_DSI,
    WORST_CASE_RATE_HZ,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.nsga2_loop import BedBV3Problem
from tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code import paths

GEN6_GEN7_GENS: frozenset[int] = frozenset({6, 7})
N_RELOADED_INDIVIDUALS: int = 192  # 96 per gen x 2 gens
N_GEN7_SURVIVORS: int = POP_SIZE  # 96


@dataclass(frozen=True, slots=True)
class ReloadedRecord:
    """One serialisable survivor record (used for diagnostic JSON output)."""

    cell_index: int
    generation: int
    params: list[float]
    f0: float
    f1: float
    g0: float
    is_unstable: bool


def _load_t0081_records(*, path: Path) -> list[dict[str, object]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    records = raw.get("evaluations", raw) if isinstance(raw, dict) else raw
    assert isinstance(records, list), "expected list of records"
    return records


def _filter_gen6_gen7(*, records: list[dict[str, object]]) -> list[dict[str, object]]:
    out = [r for r in records if int(r["generation"]) in GEN6_GEN7_GENS]
    assert len(out) == N_RELOADED_INDIVIDUALS, (
        f"expected {N_RELOADED_INDIVIDUALS} gen6+gen7 records, got {len(out)}"
    )
    return out


def _build_population_from_records(
    *,
    records: list[dict[str, object]],
) -> Population:
    n = len(records)
    n_var = len(records[0]["params"])  # type: ignore[arg-type]
    x_arr: NDArray[np.float64] = np.zeros((n, n_var), dtype=np.float64)
    f_arr: NDArray[np.float64] = np.zeros((n, 2), dtype=np.float64)
    g_arr: NDArray[np.float64] = np.zeros((n, 1), dtype=np.float64)
    for i, r in enumerate(records):
        x_arr[i, :] = np.asarray(r["params"], dtype=np.float64)
        is_unstable: bool = bool(r["is_unstable"])
        dsi_to_f: float = WORST_CASE_DSI if is_unstable else float(r["dsi"])
        pd_to_f: float = WORST_CASE_RATE_HZ if is_unstable else float(r["pd_rate_hz"])
        f_arr[i, 0] = -dsi_to_f
        f_arr[i, 1] = -pd_to_f
        g_arr[i, 0] = float(r["constraint_violation"])
    pop = Population.new("X", x_arr, "F", f_arr, "G", g_arr)
    for ind in pop:
        ind.evaluated.update(["F", "G"])
    return pop


def reload_t0081_gen7_survivors(
    *,
    problem: BedBV3Problem,
    seed: int,
) -> Population:
    """Return the 96-individual gen-7 survivor pool (X, F, G already evaluated).

    Deterministic given ``seed`` and the saved ``all_evaluations.json``.
    """
    records = _load_t0081_records(path=paths.T0081_ALL_EVALUATIONS_JSON)
    survivors_input = _filter_gen6_gen7(records=records)
    pop192 = _build_population_from_records(records=survivors_input)
    survival = RankAndCrowding()
    rng = np.random.default_rng(seed=seed)
    survivors = survival.do(
        problem,
        pop192,
        n_survive=N_GEN7_SURVIVORS,
        random_state=rng,
    )
    assert len(survivors) == N_GEN7_SURVIVORS, (
        f"survival did not return {N_GEN7_SURVIVORS} individuals, got {len(survivors)}"
    )
    for ind in survivors:
        ind.evaluated.update(["F", "G"])
    return survivors


def _records_for_dump(
    *,
    survivors: Population,
    survivor_records_input: list[dict[str, object]],
) -> list[ReloadedRecord]:
    """Map survivor X back to the input record cell_index for diagnostic output."""
    out: list[ReloadedRecord] = []
    by_params: dict[tuple[float, ...], dict[str, object]] = {
        tuple(float(v) for v in r["params"]): r  # type: ignore[arg-type]
        for r in survivor_records_input
    }
    for ind in survivors:
        x: NDArray[np.float64] = ind.X
        key = tuple(float(v) for v in x)
        rec = by_params.get(key)
        if rec is None:
            # Should not happen; record placeholder if it does.
            out.append(
                ReloadedRecord(
                    cell_index=-1,
                    generation=-1,
                    params=[float(v) for v in x],
                    f0=float(ind.F[0]),
                    f1=float(ind.F[1]),
                    g0=float(ind.G[0]),
                    is_unstable=False,
                ),
            )
            continue
        out.append(
            ReloadedRecord(
                cell_index=int(rec["cell_index"]),
                generation=int(rec["generation"]),
                params=[float(v) for v in x],
                f0=float(ind.F[0]),
                f1=float(ind.F[1]),
                g0=float(ind.G[0]),
                is_unstable=bool(rec["is_unstable"]),
            ),
        )
    return out


def _dump_survivors_json(
    *,
    survivors: Population,
    survivor_records_input: list[dict[str, object]],
    out_path: Path,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rrs = _records_for_dump(
        survivors=survivors,
        survivor_records_input=survivor_records_input,
    )
    payload = [
        {
            "cell_index": r.cell_index,
            "generation": r.generation,
            "params": r.params,
            "F": [r.f0, r.f1],
            "G": [r.g0],
            "is_unstable": r.is_unstable,
            "evaluated": ["F", "G"],
        }
        for r in rrs
    ]
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=LHS_SEED)
    parser.add_argument("--max-workers", type=int, default=1)
    args = parser.parse_args()
    paths.ensure_directories()
    problem = BedBV3Problem(max_workers=args.max_workers)
    survivors = reload_t0081_gen7_survivors(problem=problem, seed=args.seed)
    records = _load_t0081_records(path=paths.T0081_ALL_EVALUATIONS_JSON)
    gen67 = _filter_gen6_gen7(records=records)
    _dump_survivors_json(
        survivors=survivors,
        survivor_records_input=gen67,
        out_path=paths.RELOADED_GEN7_SURVIVORS_JSON,
    )
    print(
        f"[reload_gen7] reloaded {len(survivors)} gen-7 survivors from t0081 "
        f"({len(gen67)} input records); wrote {paths.RELOADED_GEN7_SURVIVORS_JSON}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(_main())
