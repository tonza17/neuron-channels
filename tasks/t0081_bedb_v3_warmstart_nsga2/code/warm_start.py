"""Assemble the 96-cell warm-start initial population for t0081 (REQ-3).

The t0080 ``BedBV3Problem`` declares ``xl=LOWER_BOUNDS, xu=UPPER_BOUNDS`` in
*natural* units (S/cm^2, ohm-cm, mM, etc.), so pymoo's sampling, crossover,
and mutation all operate directly in natural-unit space. This module
assembles the warm-start population in that same natural-unit space:

* 5 t0080 Pareto cells: ``cells[*].params`` from t0080's pareto_front.json
  are already in natural units, used verbatim.
* 17 t0078 Pareto cells: ``pareto_cells[*].params_natural`` are 49-d in
  natural units. Indices 0-48 map directly into t0080's first 49 dims
  (REQ-21 of t0080: preserve t0078 49-d ParamIndex layout). Indices 49-53
  (the 5 v3 dendritic-spike additions) are sampled per-cell from
  ``rng.uniform(LOWER_BOUNDS[i], UPPER_BOUNDS[i])`` with seed 42.
* 74 fresh LHS samples in 54-d, drawn from pymoo's ``LHS()`` sampler against
  the t0080 problem (which already has the natural-unit bounds).

Each row is clamped per-dim to ``[LOWER_BOUNDS[i], UPPER_BOUNDS[i]]`` before
output; this matters mainly for t0078 cells whose AIS Nav1.6 may be below
the Kole 2008 floor of 0.25 S/cm^2 and would be rejected by the t0080
constraint otherwise.

Total: 96 cells, written to ``results/data/warm_start_population.json``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from pymoo.operators.sampling.lhs import LHS

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    LOWER_BOUNDS,
    N_PARAMS,
    UPPER_BOUNDS,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.nsga2_loop import BedBV3Problem
from tasks.t0081_bedb_v3_warmstart_nsga2.code.paths import (
    T0078_PARETO_FRONT_JSON,
    T0080_PARETO_FRONT_JSON,
    WARM_START_POPULATION_JSON,
    ensure_directories,
)

N_T0080_CELLS: int = 5
N_T0078_CELLS: int = 17
N_LHS_FILL: int = 74
N_TOTAL: int = N_T0080_CELLS + N_T0078_CELLS + N_LHS_FILL  # 96
T0078_PARAMS_NATURAL_LEN: int = 49

T0078_PROJECT_SEED: int = 42
LHS_FILL_SEED: int = 43


def load_t0080_pareto() -> NDArray[np.float64]:
    """Return the (5, 54) natural-unit t0080 Pareto cell matrix."""
    raw = json.loads(T0080_PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    cells = raw["cells"]
    assert len(cells) == N_T0080_CELLS, (
        f"expected {N_T0080_CELLS} t0080 Pareto cells, got {len(cells)}"
    )
    out: NDArray[np.float64] = np.zeros((N_T0080_CELLS, N_PARAMS), dtype=np.float64)
    for i, cell in enumerate(cells):
        params = cell["params"]
        assert len(params) == N_PARAMS, (
            f"t0080 cell {i} has {len(params)} params, expected {N_PARAMS}"
        )
        out[i] = np.asarray(params, dtype=np.float64)
    return out


def load_and_project_t0078_pareto(*, rng_seed: int = T0078_PROJECT_SEED) -> NDArray[np.float64]:
    """Return the (17, 54) projection of t0078 Pareto cells into 54-d natural space.

    t0078's ``params_natural`` is 49-d in natural physical units, and t0080
    inherits the t0078 49-d ParamIndex layout for indices 0-48. We:
    * indices 0-48: copy the t0078 natural-unit values verbatim, then clamp
      to ``[LOWER_BOUNDS[i], UPPER_BOUNDS[i]]`` to enforce the t0080 Kole
      2008 AIS-Nav1.6 floor (0.25 S/cm^2) on cells that fall below it.
    * indices 49-53: sample uniformly within ``[LOWER_BOUNDS[i], UPPER_BOUNDS[i]]``
      using the seeded RNG.
    """
    raw = json.loads(T0078_PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    cells = raw["pareto_cells"]
    assert len(cells) == N_T0078_CELLS, (
        f"expected {N_T0078_CELLS} t0078 Pareto cells, got {len(cells)}"
    )
    rng = np.random.default_rng(seed=rng_seed)
    out: NDArray[np.float64] = np.zeros((N_T0078_CELLS, N_PARAMS), dtype=np.float64)
    for i, cell in enumerate(cells):
        natural = cell["params_natural"]
        assert len(natural) == T0078_PARAMS_NATURAL_LEN, (
            f"t0078 cell {i} has {len(natural)} params, expected {T0078_PARAMS_NATURAL_LEN}"
        )
        for j in range(T0078_PARAMS_NATURAL_LEN):
            lo = float(LOWER_BOUNDS[j])
            hi = float(UPPER_BOUNDS[j])
            out[i, j] = max(lo, min(hi, float(natural[j])))
        for j in range(T0078_PARAMS_NATURAL_LEN, N_PARAMS):
            lo = float(LOWER_BOUNDS[j])
            hi = float(UPPER_BOUNDS[j])
            out[i, j] = float(rng.uniform(lo, hi))
    return out


def generate_lhs_fill(
    *,
    n_samples: int = N_LHS_FILL,
    problem: BedBV3Problem,
    rng_seed: int = LHS_FILL_SEED,
) -> NDArray[np.float64]:
    """Return (n_samples, 54) LHS matrix in the t0080 problem's natural-unit space.

    pymoo's ``LHS()`` samples in ``[problem.xl, problem.xu]``, which for
    ``BedBV3Problem`` is the natural-unit ``[LOWER_BOUNDS, UPPER_BOUNDS]``.
    """
    sampler = LHS()
    arr = sampler(problem, n_samples, seed=rng_seed).get("X")
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (n_samples, N_PARAMS), f"LHS shape {arr.shape} != ({n_samples}, {N_PARAMS})"
    return arr.astype(np.float64)


def assemble_warm_start_population(*, problem: BedBV3Problem) -> NDArray[np.float64]:
    """Return the (96, 54) warm-start population matrix in natural-unit space."""
    t80 = load_t0080_pareto()
    t78 = load_and_project_t0078_pareto()
    lhs = generate_lhs_fill(n_samples=N_LHS_FILL, problem=problem)
    pop = np.concatenate([t80, t78, lhs], axis=0)
    assert pop.shape == (N_TOTAL, N_PARAMS), f"pop shape {pop.shape} != ({N_TOTAL}, {N_PARAMS})"
    # Final per-row, per-dim clamp to LOWER_BOUNDS / UPPER_BOUNDS so all
    # rows are valid pymoo samples.
    pop = np.maximum(pop, LOWER_BOUNDS[np.newaxis, :])
    pop = np.minimum(pop, UPPER_BOUNDS[np.newaxis, :])
    return pop


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=str,
        default=str(WARM_START_POPULATION_JSON),
        help="Output JSON path",
    )
    args = parser.parse_args()
    ensure_directories()
    problem = BedBV3Problem(max_workers=1)
    pop = assemble_warm_start_population(problem=problem)
    payload: dict[str, Any] = {
        "n_total": int(pop.shape[0]),
        "n_t0080": N_T0080_CELLS,
        "n_t0078": N_T0078_CELLS,
        "n_lhs": N_LHS_FILL,
        "n_params": N_PARAMS,
        "t0078_project_seed": T0078_PROJECT_SEED,
        "lhs_fill_seed": LHS_FILL_SEED,
        "population": pop.tolist(),
    }
    out_path: Path = (
        WARM_START_POPULATION_JSON
        if args.out == str(WARM_START_POPULATION_JSON)
        else Path(args.out)
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(
        f"[warm_start] wrote {pop.shape} population to {out_path} "
        f"(t0080={N_T0080_CELLS} + t0078={N_T0078_CELLS} + lhs={N_LHS_FILL} = {N_TOTAL})",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(_main())
