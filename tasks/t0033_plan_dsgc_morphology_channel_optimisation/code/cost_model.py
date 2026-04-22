"""Compute the (strategy x compute_mode x tier) USD cost envelope.

Consumes outputs from ``search_space.py``, ``wall_time.py``, and
``pricing.py`` and writes:

* ``cost_envelope.csv`` — one row per (strategy, compute_mode, tier,
  parameterisation) with USD total, wall-hours, and optional
  train/inference splits for the surrogate path.
* ``sensitivity_grid.csv`` — the 3x3 grid over cost_mult x sample_mult
  multipliers for every cell of the cost envelope.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from typing import Any

from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code import paths
from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code.constants import (
    CHECKPOINT_CLIFF_HOURS,
    CHECKPOINT_OVERHEAD_MULT,
    COL_COMPUTE_MODE,
    COL_COST_MULT,
    COL_DOLLARS_PER_HOUR,
    COL_EFFECTIVE_WALL_HOURS,
    COL_INFER_USD,
    COL_N_DIMS,
    COL_N_SAMPLES_CENTRAL,
    COL_NOTES,
    COL_PARAMETERISATION,
    COL_PER_SIM_SECONDS,
    COL_SAMPLE_MULT,
    COL_STRATEGY,
    COL_TIER,
    COL_TRAIN_USD,
    COL_USD_SENSITIVITY,
    COL_USD_TOTAL,
    COL_WALL_HOURS,
    CORENEURON_REFERENCE_SPEEDUP,
    COST_MULTIPLIERS,
    N_ANGLES,
    N_TRIALS_STOCHASTIC,
    SAMPLE_MULTIPLIERS,
    SECONDS_PER_SIM_DETERMINISTIC,
    SECONDS_PER_SIM_STOCHASTIC,
    SURROGATE_INFERENCE_SPEEDUP,
    SURROGATE_TRAIN_SAMPLES_CENTRAL,
    T0022_DETERMINISTIC_S_PER_ANGLE_TRIAL,
    ComputeMode,
    SearchStrategy,
    Tier,
)
from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code.pricing import (
    build_pricing_rows,
)
from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code.search_space import (
    build_table as build_search_space,
)
from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code.wall_time import (
    many_core_cpu_seconds,
    scale_by_gpu_tier,
    surrogate_inference_seconds,
)


@dataclass(frozen=True, slots=True)
class CostRow:
    strategy: SearchStrategy
    compute_mode: ComputeMode
    tier: Tier
    parameterisation: str
    n_dims: int
    n_samples_central: float
    per_sim_seconds: float
    wall_hours: float
    effective_wall_hours: float
    dollars_per_hour: float
    usd_total: float
    train_usd: float | None
    inference_usd: float | None
    notes: str


GPU_TIERS: list[Tier] = [Tier.RTX_4090, Tier.A100_40GB, Tier.H100]


def _lookup_price(*, tier: Tier, pricing: dict[str, float]) -> float:
    return pricing[tier.value]


def _per_sim_seconds(*, compute_mode: ComputeMode, tier: Tier, model_variant: str) -> float:
    base = (
        SECONDS_PER_SIM_DETERMINISTIC
        if model_variant == "t0022_deterministic"
        else SECONDS_PER_SIM_STOCHASTIC
    )
    match compute_mode:
        case ComputeMode.CORENEURON_GPU:
            return scale_by_gpu_tier(base_seconds=base, tier=tier)
        case ComputeMode.SURROGATE_NN_GPU:
            return surrogate_inference_seconds(base_seconds=base)
        case ComputeMode.MANY_CORE_CPU:
            return many_core_cpu_seconds(base_seconds=base)


def _effective_hours(wall_hours: float) -> float:
    if wall_hours > CHECKPOINT_CLIFF_HOURS:
        return wall_hours * CHECKPOINT_OVERHEAD_MULT
    return wall_hours


def _surrogate_train_usd(*, tier: Tier, pricing: dict[str, float]) -> float:
    """USD cost of burning ~5,000 NEURON-backed evals to train the surrogate.

    The surrogate training sample is evaluated on the t0022 deterministic
    path (cheaper per-sim) via CoreNEURON on the same GPU tier as the GA
    inference. Training dominates the USD budget of the surrogate pipeline.
    """
    train_per_sim = scale_by_gpu_tier(base_seconds=SECONDS_PER_SIM_DETERMINISTIC, tier=tier)
    total_seconds = float(SURROGATE_TRAIN_SAMPLES_CENTRAL) * train_per_sim
    hours = total_seconds / 3600.0
    effective = _effective_hours(hours)
    return effective * _lookup_price(tier=tier, pricing=pricing)


def _surrogate_infer_usd(*, n_samples: float, tier: Tier, pricing: dict[str, float]) -> float:
    """USD cost of GA evaluations on the trained surrogate.

    Each evaluation is ~surrogate inference time (t0022 base / 100). The
    GA itself does not burn further NEURON simulations — the ~13,500-eval
    count carried by ``n_samples`` for the surrogate strategy is the
    trained-surrogate invocation count.
    """
    per_eval_seconds = surrogate_inference_seconds(base_seconds=SECONDS_PER_SIM_DETERMINISTIC)
    # GA evaluations after training = n_samples - training samples.
    # Both ga_evals and training already included inside the budget; here we
    # count only the post-training GA inference cost.
    ga_evals = max(0.0, n_samples - float(SURROGATE_TRAIN_SAMPLES_CENTRAL))
    hours = ga_evals * per_eval_seconds / 3600.0
    effective = _effective_hours(hours)
    return effective * _lookup_price(tier=tier, pricing=pricing)


def _row_for_cell(
    *,
    strategy: SearchStrategy,
    compute_mode: ComputeMode,
    tier: Tier,
    parameterisation: str,
    n_dims: int,
    n_samples: float,
    pricing: dict[str, float],
) -> CostRow:
    # Use t0024 stochastic as the optimiser's default per-sim cost envelope.
    model_variant = "t0024_stochastic_AR2_rho0.6"
    per_sim_seconds = _per_sim_seconds(
        compute_mode=compute_mode, tier=tier, model_variant=model_variant
    )
    wall_hours = n_samples * per_sim_seconds / 3600.0
    effective = _effective_hours(wall_hours)
    price = _lookup_price(tier=tier, pricing=pricing)
    usd_total = effective * price

    train_usd: float | None = None
    inference_usd: float | None = None
    notes = ""
    if compute_mode is ComputeMode.SURROGATE_NN_GPU:
        train_usd = _surrogate_train_usd(tier=tier, pricing=pricing)
        inference_usd = _surrogate_infer_usd(n_samples=n_samples, tier=tier, pricing=pricing)
        usd_total = train_usd + inference_usd
        notes = (
            f"Surrogate pipeline: train_usd = CoreNEURON on {tier.value} x "
            f"{SURROGATE_TRAIN_SAMPLES_CENTRAL} deterministic sims; "
            f"inference_usd = GA on trained NN (100x speedup)."
        )
    elif compute_mode is ComputeMode.MANY_CORE_CPU:
        notes = "Stock CPU NEURON on 96-core Vast.ai node; speed-tier not applied."
    else:
        notes = (
            f"CoreNEURON GPU: base 5x speedup at RTX 3090, scaled by GPU_SPEED_TIERS."
            f" t0024 stochastic per-sim {SECONDS_PER_SIM_STOCHASTIC:.1f} s."
        )

    return CostRow(
        strategy=strategy,
        compute_mode=compute_mode,
        tier=tier,
        parameterisation=parameterisation,
        n_dims=n_dims,
        n_samples_central=n_samples,
        per_sim_seconds=per_sim_seconds,
        wall_hours=wall_hours,
        effective_wall_hours=effective,
        dollars_per_hour=price,
        usd_total=usd_total,
        train_usd=train_usd,
        inference_usd=inference_usd,
        notes=notes,
    )


def _load_pricing() -> dict[str, float]:
    return {row.tier: row.dollars_per_hour for row in build_pricing_rows()}


def build_cost_envelope() -> list[CostRow]:
    pricing = _load_pricing()
    search_rows = build_search_space()  # list of (parameterisation, SimulationBudget)
    envelope: list[CostRow] = []
    for parameterisation, budget in search_rows:
        # Skip grid for non-anchor strategies above 6 dims to avoid printing
        # astronomical numbers — but record one grid-anchor row per
        # parameterisation at each tier in the envelope to document the
        # infeasibility.
        for compute_mode in ComputeMode:
            for tier in GPU_TIERS:
                if compute_mode is ComputeMode.MANY_CORE_CPU:
                    # MANY_CORE_CPU ignores GPU tier; one row only.
                    if tier is not Tier.RTX_4090:
                        continue
                    envelope.append(
                        _row_for_cell(
                            strategy=budget.strategy,
                            compute_mode=compute_mode,
                            tier=Tier.CPU_96,
                            parameterisation=parameterisation,
                            n_dims=budget.n_dims,
                            n_samples=budget.n_samples_central,
                            pricing=pricing,
                        )
                    )
                else:
                    envelope.append(
                        _row_for_cell(
                            strategy=budget.strategy,
                            compute_mode=compute_mode,
                            tier=tier,
                            parameterisation=parameterisation,
                            n_dims=budget.n_dims,
                            n_samples=budget.n_samples_central,
                            pricing=pricing,
                        )
                    )
    return envelope


def _write_envelope(rows: list[CostRow]) -> None:
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)
    with paths.COST_ENVELOPE_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                COL_STRATEGY,
                COL_COMPUTE_MODE,
                COL_TIER,
                COL_PARAMETERISATION,
                COL_N_DIMS,
                COL_N_SAMPLES_CENTRAL,
                COL_PER_SIM_SECONDS,
                COL_WALL_HOURS,
                COL_EFFECTIVE_WALL_HOURS,
                COL_DOLLARS_PER_HOUR,
                COL_USD_TOTAL,
                COL_TRAIN_USD,
                COL_INFER_USD,
                COL_NOTES,
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.strategy.value,
                    row.compute_mode.value,
                    row.tier.value,
                    row.parameterisation,
                    row.n_dims,
                    f"{row.n_samples_central:.3e}",
                    f"{row.per_sim_seconds:.3f}",
                    f"{row.wall_hours:.3f}",
                    f"{row.effective_wall_hours:.3f}",
                    f"{row.dollars_per_hour:.3f}",
                    f"{row.usd_total:.2f}",
                    "" if row.train_usd is None else f"{row.train_usd:.2f}",
                    "" if row.inference_usd is None else f"{row.inference_usd:.2f}",
                    row.notes,
                ]
            )


def sensitivity_grid(*, envelope: list[CostRow]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in envelope:
        for cost_mult in COST_MULTIPLIERS:
            for sample_mult in SAMPLE_MULTIPLIERS:
                # Sample-multiplier scales wall-hours; cost-multiplier scales USD/hour.
                scaled_wall_hours = row.wall_hours * sample_mult
                scaled_effective = (
                    scaled_wall_hours * CHECKPOINT_OVERHEAD_MULT
                    if scaled_wall_hours > CHECKPOINT_CLIFF_HOURS
                    else scaled_wall_hours
                )
                if row.compute_mode is ComputeMode.SURROGATE_NN_GPU:
                    # Surrogate split: training cost is fixed; inference scales
                    # with sample_mult.
                    train = row.train_usd if row.train_usd is not None else 0.0
                    infer = row.inference_usd if row.inference_usd is not None else 0.0
                    scaled = cost_mult * (train + infer * sample_mult)
                else:
                    scaled = scaled_effective * row.dollars_per_hour * cost_mult
                rows.append(
                    {
                        COL_STRATEGY: row.strategy.value,
                        COL_COMPUTE_MODE: row.compute_mode.value,
                        COL_TIER: row.tier.value,
                        COL_PARAMETERISATION: row.parameterisation,
                        COL_COST_MULT: cost_mult,
                        COL_SAMPLE_MULT: sample_mult,
                        COL_USD_SENSITIVITY: round(scaled, 2),
                    }
                )
    return rows


def _write_sensitivity(rows: list[dict[str, Any]]) -> None:
    with paths.SENSITIVITY_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                COL_STRATEGY,
                COL_COMPUTE_MODE,
                COL_TIER,
                COL_PARAMETERISATION,
                COL_COST_MULT,
                COL_SAMPLE_MULT,
                COL_USD_SENSITIVITY,
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def _print_preview(envelope: list[CostRow]) -> None:
    """Print the central (1x, 1x) cost for each strategy at each tier for the tight param set."""

    print()
    print("=== Central-cell cost preview (tight parameterisation, stochastic t0024) ===")
    for row in envelope:
        if row.parameterisation != "tight":
            continue
        if row.strategy is SearchStrategy.GRID:
            continue  # skip astronomical numbers in preview
        tag = f"{row.compute_mode.value:<18} {row.tier.value:<12}"
        print(
            f"  {row.strategy.value:<18} {tag}  samples={row.n_samples_central:.2e}"
            f"  per_sim={row.per_sim_seconds:>10.3f} s"
            f"  wall_h={row.wall_hours:>8.2f}"
            f"  USD=${row.usd_total:>12,.2f}"
        )


def main() -> None:
    envelope = build_cost_envelope()
    _write_envelope(envelope)
    print(f"Wrote {len(envelope)} rows to {paths.COST_ENVELOPE_CSV}")

    sens_rows = sensitivity_grid(envelope=envelope)
    _write_sensitivity(sens_rows)
    print(f"Wrote {len(sens_rows)} rows to {paths.SENSITIVITY_CSV}")

    _print_preview(envelope)

    # Cheap sanity: 12 angles x 10 trials x 3.8 s = 456 s.
    expected_det = T0022_DETERMINISTIC_S_PER_ANGLE_TRIAL * N_ANGLES * N_TRIALS_STOCHASTIC
    assert abs(SECONDS_PER_SIM_DETERMINISTIC - expected_det) < 0.01, (
        f"deterministic per-sim mismatch: {SECONDS_PER_SIM_DETERMINISTIC} vs {expected_det}"
    )

    # Export a small JSON summary for downstream answer-asset writer.
    summary = {
        "coreneuron_reference_speedup": CORENEURON_REFERENCE_SPEEDUP,
        "surrogate_inference_speedup": SURROGATE_INFERENCE_SPEEDUP,
        "seconds_per_sim_deterministic": SECONDS_PER_SIM_DETERMINISTIC,
        "seconds_per_sim_stochastic": SECONDS_PER_SIM_STOCHASTIC,
        "pricing": _load_pricing(),
    }
    (paths.DATA_DIR / "cost_model_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
