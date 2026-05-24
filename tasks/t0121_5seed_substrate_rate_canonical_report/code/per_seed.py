"""Per-seed acceptance-rate recompute and convergence-trajectory summary.

For each seed key in ``ALL_SEED_KEYS``, this module loads the raw NSGA-II
evaluation dump and HV trajectory, applies the canonical LEGIT predicate,
dedups by the 68-d parameter vector, counts unique LEGIT joint-pass cells,
and packages the per-seed summary plus convergence metadata into a
``PerSeedSummary`` dataclass.

The per-seed counts and totals are asserted against the pinned canonical
anchors from t0115's ``substrate_rate_5seed.csv``; any drift halts the
pipeline with a clear AssertionError.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tasks.t0121_5seed_substrate_rate_canonical_report.code.constants import (
    EXPECTED_LEGIT_COUNT,
    EXPECTED_N_EVALS,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.loaders import (
    cell_vector_key,
    is_legit_joint_pass,
    load_evaluations,
    load_hv,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.seed_metadata import (
    ASSET_DECLARED_FINAL_HV,
    ASSET_DECLARED_N_GEN,
    ASSET_DECLARED_STOP_TRIGGER,
    SEED_TASK_IDS,
    SEED_TASK_SEED,
)


@dataclass(frozen=True, slots=True)
class PerSeedSummary:
    seed_key: str
    task_id: str
    task_seed: int
    n_total_evals: int
    n_legit_unique: int
    acceptance_rate_pct: float
    n_generations_completed: int
    final_hypervolume: float
    stop_trigger: str
    wall_clock_per_gen_s: float | None


def _wall_clock_per_gen(*, hv_trajectory: list[dict[str, object]]) -> float | None:
    """Average wall-clock seconds per generation from the HV trajectory.

    Returns ``None`` (not 0.0) when the trajectory has fewer than 2 records
    or when the ``elapsed_s`` field is missing. Per the project style guide,
    ``None`` means "no measurement available", never zero.
    """
    if len(hv_trajectory) < 2:
        return None
    first = hv_trajectory[0]
    last = hv_trajectory[-1]
    if "elapsed_s" not in first or "elapsed_s" not in last:
        return None
    first_s = float(first["elapsed_s"])  # type: ignore[arg-type]
    last_s = float(last["elapsed_s"])  # type: ignore[arg-type]
    first_gen = int(first["generation"])  # type: ignore[arg-type]
    last_gen = int(last["generation"])  # type: ignore[arg-type]
    n_intervals = last_gen - first_gen
    if n_intervals <= 0:
        return None
    return (last_s - first_s) / n_intervals


def summarize_seed(
    *,
    seed_key: str,
    eval_path: Path,
    hv_path: Path,
) -> PerSeedSummary:
    """Compute the per-seed acceptance summary for one seed key.

    Loads the evaluations and HV trajectory, applies the LEGIT predicate,
    dedups by 68-d vector, and asserts the canonical anchors. Raises
    ``AssertionError`` with a positive message if any anchor is violated.
    """
    evals = load_evaluations(path=eval_path)
    hv = load_hv(path=hv_path)

    legit_unique_keys: set[tuple[float, ...]] = set()
    for cell in evals:
        dsi = float(cell["dsi_vector_sum"])
        pd = float(cell["pd_rate_hz"])
        if is_legit_joint_pass(dsi=dsi, pd_rate_hz=pd):
            key = cell_vector_key(vector_68d=cell["vector_68d"])
            legit_unique_keys.add(key)

    n_total = len(evals)
    n_legit = len(legit_unique_keys)

    expected_total = EXPECTED_N_EVALS[seed_key]
    expected_legit = EXPECTED_LEGIT_COUNT[seed_key]
    assert n_total == expected_total, f"{seed_key} total evals is {expected_total}, got {n_total}"
    assert n_legit == expected_legit, (
        f"{seed_key} LEGIT unique count is {expected_legit}, got {n_legit}"
    )

    acceptance_pct = 100.0 * n_legit / n_total

    return PerSeedSummary(
        seed_key=seed_key,
        task_id=SEED_TASK_IDS[seed_key],
        task_seed=SEED_TASK_SEED[seed_key],
        n_total_evals=n_total,
        n_legit_unique=n_legit,
        acceptance_rate_pct=acceptance_pct,
        n_generations_completed=ASSET_DECLARED_N_GEN[seed_key],
        final_hypervolume=ASSET_DECLARED_FINAL_HV[seed_key],
        stop_trigger=ASSET_DECLARED_STOP_TRIGGER[seed_key],
        wall_clock_per_gen_s=_wall_clock_per_gen(hv_trajectory=hv),
    )
