"""Per-simulation wall-time extrapolation from t0026 anchors.

Writes two CSVs:

* ``sim_wall_time.csv`` — baseline per-sim wall-time under the canonical
  12-angle x 10-trial protocol for the t0022 deterministic and t0024
  stochastic AR(2) models (2 rows).
* ``per_tier_wall_time.csv`` — scaled per-sim wall-time under each compute
  mode (CoreNEURON-GPU, surrogate-NN inference, many-core CPU) across 3-4
  representative GPU tiers plus the CPU fallback.

The ``arf.scripts.utils.vast_machines.GPU_SPEED_TIERS`` table is imported
directly — it is a framework constant.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass

from arf.scripts.utils.vast_machines import GPU_SPEED_TIERS
from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code import paths
from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code.constants import (
    COL_ASSUMPTION,
    COL_COMPUTE_MODE,
    COL_MODEL_VARIANT,
    COL_N_ANGLES,
    COL_N_TRIALS,
    COL_PER_SIM_SECONDS,
    COL_S_PER_ANGLE_TRIAL,
    COL_SPEED_TIER_RATIO,
    COL_TIER,
    COL_TOTAL_MINUTES,
    COL_TOTAL_SECONDS,
    CORENEURON_REFERENCE_SPEEDUP,
    CPU_CORES_PER_NODE,
    N_ANGLES,
    N_TRIALS_STOCHASTIC,
    SURROGATE_INFERENCE_SPEEDUP,
    T0022_DETERMINISTIC_S_PER_ANGLE_TRIAL,
    T0024_STOCHASTIC_S_PER_ANGLE_TRIAL,
    ComputeMode,
    Tier,
)


@dataclass(frozen=True, slots=True)
class SimWallTime:
    model_variant: str
    n_angles: int
    n_trials: int
    seconds_per_angle_trial: float
    total_seconds: float
    total_minutes: float


@dataclass(frozen=True, slots=True)
class PerTierWallTime:
    compute_mode: ComputeMode
    model_variant: str
    tier: Tier
    speed_tier_ratio: float
    per_sim_seconds: float
    assumption: str


BASELINE_SIMS: list[SimWallTime] = [
    SimWallTime(
        model_variant="t0022_deterministic",
        n_angles=N_ANGLES,
        n_trials=N_TRIALS_STOCHASTIC,
        seconds_per_angle_trial=T0022_DETERMINISTIC_S_PER_ANGLE_TRIAL,
        total_seconds=T0022_DETERMINISTIC_S_PER_ANGLE_TRIAL * N_ANGLES * N_TRIALS_STOCHASTIC,
        total_minutes=(T0022_DETERMINISTIC_S_PER_ANGLE_TRIAL * N_ANGLES * N_TRIALS_STOCHASTIC)
        / 60.0,
    ),
    SimWallTime(
        model_variant="t0024_stochastic_AR2_rho0.6",
        n_angles=N_ANGLES,
        n_trials=N_TRIALS_STOCHASTIC,
        seconds_per_angle_trial=T0024_STOCHASTIC_S_PER_ANGLE_TRIAL,
        total_seconds=T0024_STOCHASTIC_S_PER_ANGLE_TRIAL * N_ANGLES * N_TRIALS_STOCHASTIC,
        total_minutes=(T0024_STOCHASTIC_S_PER_ANGLE_TRIAL * N_ANGLES * N_TRIALS_STOCHASTIC) / 60.0,
    ),
]


def _tier_speed(tier: Tier) -> float:
    if tier is Tier.CPU_96:
        return 1.0  # not applicable; placeholder for column
    return GPU_SPEED_TIERS[tier.value]


def scale_by_gpu_tier(*, base_seconds: float, tier: Tier) -> float:
    """Scale CPU-reference per-sim wall-time by GPU speed-tier ratio.

    The reference tier is RTX 3090 (speed 1.0). CoreNEURON is assumed to
    deliver a literature-placeholder 5x speedup over single-threaded CPU
    NEURON at the reference tier. Higher tiers scale linearly.
    """
    ratio: float = _tier_speed(tier=tier)
    return base_seconds / (CORENEURON_REFERENCE_SPEEDUP * ratio)


def surrogate_inference_seconds(*, base_seconds: float) -> float:
    """Surrogate-NN inference is assumed 100x faster than a NEURON sim.

    GPU-tier independent within the sensitivity band; an RTX 3090 already
    trivialises the surrogate forward pass.
    """
    return base_seconds / SURROGATE_INFERENCE_SPEEDUP


def many_core_cpu_seconds(*, base_seconds: float) -> float:
    """Many-core Vast.ai CPU node divides the wall-time across cores."""
    return base_seconds / float(CPU_CORES_PER_NODE)


GPU_TIERS: list[Tier] = [Tier.RTX_3090, Tier.RTX_4090, Tier.A100_40GB, Tier.H100]


def build_per_tier_table() -> list[PerTierWallTime]:
    rows: list[PerTierWallTime] = []
    for sim in BASELINE_SIMS:
        # CoreNEURON-GPU rows across all four GPU tiers.
        for tier in GPU_TIERS:
            per_sim = scale_by_gpu_tier(base_seconds=sim.total_seconds, tier=tier)
            rows.append(
                PerTierWallTime(
                    compute_mode=ComputeMode.CORENEURON_GPU,
                    model_variant=sim.model_variant,
                    tier=tier,
                    speed_tier_ratio=_tier_speed(tier=tier),
                    per_sim_seconds=per_sim,
                    assumption=(
                        f"CoreNEURON reference 5x CPU->GPU at RTX 3090; linear scale by "
                        f"GPU_SPEED_TIERS[{tier.value}]={_tier_speed(tier=tier):.2f}"
                    ),
                )
            )
        # Surrogate-NN inference rows.
        for tier in GPU_TIERS:
            per_sim = surrogate_inference_seconds(base_seconds=sim.total_seconds)
            rows.append(
                PerTierWallTime(
                    compute_mode=ComputeMode.SURROGATE_NN_GPU,
                    model_variant=sim.model_variant,
                    tier=tier,
                    speed_tier_ratio=_tier_speed(tier=tier),
                    per_sim_seconds=per_sim,
                    assumption=(
                        "Surrogate inference 100x faster than NEURON; GPU tier "
                        "trivialises forward pass"
                    ),
                )
            )
        # Many-core CPU row.
        per_sim_cpu = many_core_cpu_seconds(base_seconds=sim.total_seconds)
        rows.append(
            PerTierWallTime(
                compute_mode=ComputeMode.MANY_CORE_CPU,
                model_variant=sim.model_variant,
                tier=Tier.CPU_96,
                speed_tier_ratio=1.0,
                per_sim_seconds=per_sim_cpu,
                assumption=f"Stock NEURON, {CPU_CORES_PER_NODE}-core Vast.ai CPU node",
            )
        )
    return rows


def _write_base_csv(sims: list[SimWallTime]) -> None:
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)
    with paths.WALL_TIME_BASE_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                COL_MODEL_VARIANT,
                COL_N_ANGLES,
                COL_N_TRIALS,
                COL_S_PER_ANGLE_TRIAL,
                COL_TOTAL_SECONDS,
                COL_TOTAL_MINUTES,
            ]
        )
        for sim in sims:
            writer.writerow(
                [
                    sim.model_variant,
                    sim.n_angles,
                    sim.n_trials,
                    f"{sim.seconds_per_angle_trial:.3f}",
                    f"{sim.total_seconds:.3f}",
                    f"{sim.total_minutes:.3f}",
                ]
            )


def _write_per_tier_csv(rows: list[PerTierWallTime]) -> None:
    with paths.WALL_TIME_PER_TIER_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                COL_COMPUTE_MODE,
                COL_MODEL_VARIANT,
                COL_TIER,
                COL_SPEED_TIER_RATIO,
                COL_PER_SIM_SECONDS,
                COL_ASSUMPTION,
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.compute_mode.value,
                    row.model_variant,
                    row.tier.value,
                    f"{row.speed_tier_ratio:.3f}",
                    f"{row.per_sim_seconds:.3f}",
                    row.assumption,
                ]
            )


def main() -> None:
    _write_base_csv(BASELINE_SIMS)
    rows = build_per_tier_table()
    _write_per_tier_csv(rows)
    print(f"Wrote {len(BASELINE_SIMS)} rows to {paths.WALL_TIME_BASE_CSV}")
    for sim in BASELINE_SIMS:
        print(
            f"  {sim.model_variant}: {sim.total_seconds:.1f} s "
            f"({sim.total_minutes:.1f} min) per sim"
        )
    print()
    print(f"Wrote {len(rows)} rows to {paths.WALL_TIME_PER_TIER_CSV}")
    for row in rows[:6]:
        print(
            f"  {row.compute_mode.value:<18} {row.model_variant:<30} "
            f"tier={row.tier.value:<10} per_sim={row.per_sim_seconds:.3f} s"
        )


if __name__ == "__main__":
    main()
