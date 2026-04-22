"""Per-strategy expected simulation counts for the future DSGC joint optimiser.

Five search strategies are compared at two parameterisations (tight ~25 dims,
rich ~45 dims). Rules are grounded in:

* Grid: 10**n_dims. Infeasibility anchor; no corpus precedent for n_dims>5.
* Random baseline: generic Monte-Carlo convergence (~2000 samples central).
* CMA-ES: lambda = 4 + floor(3 * log(n_dims)); ~100 generations per Hansen.
* Bayesian optimisation: central 500 evaluations; falls over above ~30 dims.
* Surrogate-NN GA: Ezra-Tsur 2021 + Poleg-Polsky 2026 template
  — population 100-200, generations 20-45, multi-seed >=3,
  plus a ~5000-sample surrogate training overhead.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass

from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code import paths
from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code.constants import (
    COL_ASSUMPTION,
    COL_N_DIMS,
    COL_N_SAMPLES_CENTRAL,
    COL_N_SAMPLES_LOWER,
    COL_N_SAMPLES_UPPER,
    COL_PARAMETERISATION,
    COL_SOURCE_CITATION,
    COL_STRATEGY,
    N_FREE_PARAMS_RICH,
    N_FREE_PARAMS_TIGHT,
    PARAM_RICH,
    PARAM_TIGHT,
    SURROGATE_TRAIN_SAMPLES_CENTRAL,
    SURROGATE_TRAIN_SAMPLES_LOWER,
    SURROGATE_TRAIN_SAMPLES_UPPER,
    SearchStrategy,
)


@dataclass(frozen=True, slots=True)
class SimulationBudget:
    strategy: SearchStrategy
    n_dims: int
    n_samples_lower: float
    n_samples_central: float
    n_samples_upper: float
    assumption_text: str
    source_citation: str


def _grid_budget(*, n_dims: int) -> SimulationBudget:
    n = float(10) ** n_dims
    return SimulationBudget(
        strategy=SearchStrategy.GRID,
        n_dims=n_dims,
        n_samples_lower=n,
        n_samples_central=n,
        n_samples_upper=n,
        assumption_text="10**n_dims (infeasibility anchor)",
        source_citation="plan_assumption",
    )


def _random_budget(*, n_dims: int) -> SimulationBudget:
    return SimulationBudget(
        strategy=SearchStrategy.RANDOM,
        n_dims=n_dims,
        n_samples_lower=500.0,
        n_samples_central=2000.0,
        n_samples_upper=10000.0,
        assumption_text=(
            "Generic Monte-Carlo convergence; no corpus precedent for DSGC-specific "
            "random baselines"
        ),
        source_citation="plan_assumption",
    )


def _cma_es_budget(*, n_dims: int) -> SimulationBudget:
    # Hansen CMA-ES default: lambda = 4 + floor(3 * log(n_dims)); ~100 generations
    lambda_pop: int = 4 + math.floor(3.0 * math.log(n_dims))
    central: float = float(lambda_pop * 100)
    return SimulationBudget(
        strategy=SearchStrategy.CMA_ES,
        n_dims=n_dims,
        n_samples_lower=central * 0.5,
        n_samples_central=central,
        n_samples_upper=central * 2.0,
        assumption_text=(
            f"Hansen lambda=4+floor(3*log(n_dims))={lambda_pop}; 100 generations; "
            "no DSGC corpus precedent"
        ),
        source_citation="Hansen2006_assumption",
    )


def _bayesian_budget(*, n_dims: int) -> SimulationBudget:
    central: float = 500.0
    note: str = "Gaussian-process BO scales poorly above ~30 dims"
    if n_dims > 30:
        note += " — expect convergence failure; values are optimistic"
    return SimulationBudget(
        strategy=SearchStrategy.BAYESIAN,
        n_dims=n_dims,
        n_samples_lower=200.0,
        n_samples_central=central,
        n_samples_upper=1000.0,
        assumption_text=note,
        source_citation="plan_assumption_no_corpus_DSGC_precedent",
    )


def _surrogate_nn_ga_budget(*, n_dims: int) -> SimulationBudget:
    # Population 100-200, generations 20-45, multi-seed >=3, + surrogate training.
    # Training samples carried separately via SURROGATE_TRAIN_SAMPLES_*.
    ga_evaluations_lower: int = 100 * 20  # 2000
    ga_evaluations_central: int = 150 * 30 * 3  # 13,500
    ga_evaluations_upper: int = 200 * 45 * 3  # 27,000
    central: float = float(SURROGATE_TRAIN_SAMPLES_CENTRAL + ga_evaluations_central)
    lower: float = float(SURROGATE_TRAIN_SAMPLES_LOWER + ga_evaluations_lower)
    upper: float = float(SURROGATE_TRAIN_SAMPLES_UPPER + ga_evaluations_upper)
    return SimulationBudget(
        strategy=SearchStrategy.SURROGATE_NN_GA,
        n_dims=n_dims,
        n_samples_lower=lower,
        n_samples_central=central,
        n_samples_upper=upper,
        assumption_text=(
            "Surrogate training = 1,000/5,000/50,000 NEURON evals + GA evaluations"
            f" = (100x20) / (150x30x3) / (200x45x3) = {ga_evaluations_lower} /"
            f" {ga_evaluations_central} / {ga_evaluations_upper}. Post-surrogate "
            "evaluations are cheap and ignored here."
        ),
        source_citation="Ezra-Tsur2021,PolegPolsky2026",
    )


def expected_simulations(*, strategy: SearchStrategy, n_dims: int) -> SimulationBudget:
    match strategy:
        case SearchStrategy.GRID:
            return _grid_budget(n_dims=n_dims)
        case SearchStrategy.RANDOM:
            return _random_budget(n_dims=n_dims)
        case SearchStrategy.CMA_ES:
            return _cma_es_budget(n_dims=n_dims)
        case SearchStrategy.BAYESIAN:
            return _bayesian_budget(n_dims=n_dims)
        case SearchStrategy.SURROGATE_NN_GA:
            return _surrogate_nn_ga_budget(n_dims=n_dims)


def build_table() -> list[tuple[str, SimulationBudget]]:
    rows: list[tuple[str, SimulationBudget]] = []
    for label, n_dims in [(PARAM_TIGHT, N_FREE_PARAMS_TIGHT), (PARAM_RICH, N_FREE_PARAMS_RICH)]:
        for strategy in SearchStrategy:
            rows.append((label, expected_simulations(strategy=strategy, n_dims=n_dims)))
    return rows


def main() -> None:
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)
    rows = build_table()
    with paths.SEARCH_SPACE_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                COL_PARAMETERISATION,
                COL_STRATEGY,
                COL_N_DIMS,
                COL_N_SAMPLES_LOWER,
                COL_N_SAMPLES_CENTRAL,
                COL_N_SAMPLES_UPPER,
                COL_ASSUMPTION,
                COL_SOURCE_CITATION,
            ]
        )
        for label, budget in rows:
            writer.writerow(
                [
                    label,
                    budget.strategy.value,
                    budget.n_dims,
                    f"{budget.n_samples_lower:.3e}",
                    f"{budget.n_samples_central:.3e}",
                    f"{budget.n_samples_upper:.3e}",
                    budget.assumption_text,
                    budget.source_citation,
                ]
            )
    print(f"Wrote {len(rows)} rows to {paths.SEARCH_SPACE_CSV}")
    for label, budget in rows:
        print(
            f"  [{label:<5}] {budget.strategy.value:<18} n_dims={budget.n_dims:<3} "
            f"central={budget.n_samples_central:.3e}"
        )


if __name__ == "__main__":
    main()
