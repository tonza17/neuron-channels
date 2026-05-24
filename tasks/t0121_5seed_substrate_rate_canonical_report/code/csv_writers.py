"""CSV writers for t0121 result tables.

Five CSVs:
* ``per_seed_substrate_rate_5seed.csv`` -- per-seed acceptance recompute.
* ``convention_drift_5seed.csv`` -- legacy-vs-canonical reconciliation table.
* ``substrate_stats_5seed.csv`` -- 5-seed mean / SD / SE / both 95% CIs.
* ``per_seed_convergence_5seed.csv`` -- per-seed convergence-trajectory summary.
* ``literature_comparison_5seed.csv`` -- Hay / Druckmann / Mohacsi side-by-side table.

Plus one parquet:
* ``pooled_legit_jointpass_cells.parquet`` -- 675 pooled LEGIT cells.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd

from tasks.t0121_5seed_substrate_rate_canonical_report.code.constants import (
    DRUCKMANN_2007_RATE_PCT,
    EXPECTED_LEGIT_COUNT,
    HAY_2011_PERISOMATIC_RATE_PCT,
    HAY_2011_RATE_PCT,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.loaders import (
    cell_vector_key,
    is_legit_joint_pass,
    load_evaluations,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.paths import (
    CSV_CONVENTION_DRIFT,
    CSV_CONVERGENCE,
    CSV_LITERATURE,
    CSV_PER_SEED,
    CSV_STATS,
    PARQUET_POOLED,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.per_seed import (
    PerSeedSummary,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.seed_metadata import (
    ALL_SEED_KEYS,
    HV_AUTOSTOP_ENABLED,
    POOL_RESTART_CADENCE,
    PROTOCOL_DRIFT_NOTES,
    SEED_TASK_IDS,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.stats import (
    SubstrateStats,
)

# ---------------------------------------------------------------------------
# Per-seed substrate rate
# ---------------------------------------------------------------------------

_CSV_CANONICAL_CONVENTION: str = "unique_legit_jp_cells_per_total_evals"


def write_per_seed_substrate_rate(
    *,
    summaries: dict[str, PerSeedSummary],
) -> Path:
    fieldnames: list[str] = [
        "seed_label",
        "task_id",
        "task_seed",
        "n_total_evals",
        "n_legit_joint_pass_unique",
        "acceptance_rate_pct",
        "convention",
    ]
    CSV_PER_SEED.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PER_SEED.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for key in ALL_SEED_KEYS:
            s = summaries[key]
            writer.writerow(
                {
                    "seed_label": s.seed_key,
                    "task_id": s.task_id,
                    "task_seed": s.task_seed,
                    "n_total_evals": s.n_total_evals,
                    "n_legit_joint_pass_unique": s.n_legit_unique,
                    "acceptance_rate_pct": round(s.acceptance_rate_pct, 4),
                    "convention": _CSV_CANONICAL_CONVENTION,
                }
            )
    return CSV_PER_SEED


# ---------------------------------------------------------------------------
# Convention drift
# ---------------------------------------------------------------------------

# Legacy reported acceptance-percent per seed, taken from the historical
# CSVs published by the upstream tasks:
# * Seeds 44, 77, 2247, 7755: t0114 joint_pass_summary_4seeds.csv
#   (numerator = n_joint_pass_unique, silence-guard cells INCLUDED).
# * Seed 9354: t0115 substrate_rate_5seed.csv (LEGIT-only, canonical).
LEGACY_REPORTED_PCT: dict[str, float] = {
    "t0106_seed44": 3.6325,
    "t0112_seed77": 0.3472,
    "t0113_seed2247": 0.1488,
    "t0114_seed7755": 12.9536,
    "t0115_seed9354": 1.1932,
}

LEGACY_CONVENTION: dict[str, str] = {
    "t0106_seed44": "silence-guard-included (joint_pass_summary_4seeds.csv)",
    "t0112_seed77": "LEGIT-by-coincidence (no silence-guard cells in this seed)",
    "t0113_seed2247": "silence-guard-included (joint_pass_summary_4seeds.csv)",
    "t0114_seed7755": "silence-guard-included (joint_pass_summary_4seeds.csv)",
    "t0115_seed9354": "LEGIT-only (substrate_rate_5seed.csv; canonical)",
}

LEGACY_SOURCE_TASK: dict[str, str] = {
    "t0106_seed44": "t0114_seed7755_no_autostop",
    "t0112_seed77": "t0114_seed7755_no_autostop",
    "t0113_seed2247": "t0114_seed7755_no_autostop",
    "t0114_seed7755": "t0114_seed7755_no_autostop",
    "t0115_seed9354": "t0115_seed9354_no_autostop",
}


def write_convention_drift(
    *,
    summaries: dict[str, PerSeedSummary],
) -> Path:
    fieldnames: list[str] = [
        "seed",
        "task_id",
        "legacy_joint_pass_pct",
        "legacy_convention",
        "legacy_source_task",
        "canonical_legit_pct",
        "delta_pct",
        "protocol_notes",
    ]
    CSV_CONVENTION_DRIFT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_CONVENTION_DRIFT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for key in ALL_SEED_KEYS:
            s = summaries[key]
            legacy = LEGACY_REPORTED_PCT[key]
            canonical = s.acceptance_rate_pct
            writer.writerow(
                {
                    "seed": s.seed_key,
                    "task_id": s.task_id,
                    "legacy_joint_pass_pct": round(legacy, 4),
                    "legacy_convention": LEGACY_CONVENTION[key],
                    "legacy_source_task": LEGACY_SOURCE_TASK[key],
                    "canonical_legit_pct": round(canonical, 4),
                    "delta_pct": round(canonical - legacy, 4),
                    "protocol_notes": PROTOCOL_DRIFT_NOTES[key],
                }
            )
    return CSV_CONVENTION_DRIFT


# ---------------------------------------------------------------------------
# Substrate stats
# ---------------------------------------------------------------------------


def write_substrate_stats(*, stats: SubstrateStats) -> Path:
    """Write the 5-seed mean / SD / SE / both 95% CIs / n_above_hay table.

    Long form (one row per metric) keeps the CSV easy to grep and matches
    the verification-criterion schema in plan VC-5.
    """
    fieldnames: list[str] = [
        "metric",
        "value",
        "normal_approx_lo",
        "normal_approx_hi",
        "bootstrap_lo",
        "bootstrap_hi",
    ]
    CSV_STATS.parent.mkdir(parents=True, exist_ok=True)
    with CSV_STATS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # Mean row carries both CIs alongside the point estimate.
        writer.writerow(
            {
                "metric": "mean_pct",
                "value": round(stats.mean_pct, 4),
                "normal_approx_lo": round(stats.normal_approx_ci_lo_pct, 4),
                "normal_approx_hi": round(stats.normal_approx_ci_hi_pct, 4),
                "bootstrap_lo": round(stats.bootstrap_ci_lo_pct, 4),
                "bootstrap_hi": round(stats.bootstrap_ci_hi_pct, 4),
            }
        )
        writer.writerow(
            {
                "metric": "sample_sd_pct",
                "value": round(stats.sample_sd_pct, 4),
                "normal_approx_lo": "",
                "normal_approx_hi": "",
                "bootstrap_lo": "",
                "bootstrap_hi": "",
            }
        )
        writer.writerow(
            {
                "metric": "sample_se_pct",
                "value": round(stats.sample_se_pct, 4),
                "normal_approx_lo": "",
                "normal_approx_hi": "",
                "bootstrap_lo": "",
                "bootstrap_hi": "",
            }
        )
        writer.writerow(
            {
                "metric": "normal_approx_ci_lo_pct",
                "value": round(stats.normal_approx_ci_lo_pct, 4),
                "normal_approx_lo": "",
                "normal_approx_hi": "",
                "bootstrap_lo": "",
                "bootstrap_hi": "",
            }
        )
        writer.writerow(
            {
                "metric": "normal_approx_ci_hi_pct",
                "value": round(stats.normal_approx_ci_hi_pct, 4),
                "normal_approx_lo": "",
                "normal_approx_hi": "",
                "bootstrap_lo": "",
                "bootstrap_hi": "",
            }
        )
        writer.writerow(
            {
                "metric": "bootstrap_ci_lo_pct",
                "value": round(stats.bootstrap_ci_lo_pct, 4),
                "normal_approx_lo": "",
                "normal_approx_hi": "",
                "bootstrap_lo": "",
                "bootstrap_hi": "",
            }
        )
        writer.writerow(
            {
                "metric": "bootstrap_ci_hi_pct",
                "value": round(stats.bootstrap_ci_hi_pct, 4),
                "normal_approx_lo": "",
                "normal_approx_hi": "",
                "bootstrap_lo": "",
                "bootstrap_hi": "",
            }
        )
        writer.writerow(
            {
                "metric": "n_seeds_above_hay_envelope",
                "value": stats.n_seeds_above_hay_envelope,
                "normal_approx_lo": "",
                "normal_approx_hi": "",
                "bootstrap_lo": "",
                "bootstrap_hi": "",
            }
        )
    return CSV_STATS


# ---------------------------------------------------------------------------
# Per-seed convergence
# ---------------------------------------------------------------------------


def write_per_seed_convergence(
    *,
    summaries: dict[str, PerSeedSummary],
) -> Path:
    fieldnames: list[str] = [
        "seed",
        "task_id",
        "n_generations_completed",
        "n_total_evals",
        "final_hypervolume",
        "stop_trigger",
        "wall_clock_per_gen_s",
        "pool_restart_every",
        "hv_plateau_autostop",
        "protocol_drift_notes",
    ]
    CSV_CONVERGENCE.parent.mkdir(parents=True, exist_ok=True)
    with CSV_CONVERGENCE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for key in ALL_SEED_KEYS:
            s = summaries[key]
            wall_clock_field: object
            if s.wall_clock_per_gen_s is None:
                wall_clock_field = ""
            else:
                wall_clock_field = round(s.wall_clock_per_gen_s, 4)
            writer.writerow(
                {
                    "seed": s.seed_key,
                    "task_id": s.task_id,
                    "n_generations_completed": s.n_generations_completed,
                    "n_total_evals": s.n_total_evals,
                    "final_hypervolume": round(s.final_hypervolume, 4),
                    "stop_trigger": s.stop_trigger,
                    "wall_clock_per_gen_s": wall_clock_field,
                    "pool_restart_every": POOL_RESTART_CADENCE[key],
                    "hv_plateau_autostop": HV_AUTOSTOP_ENABLED[key],
                    "protocol_drift_notes": PROTOCOL_DRIFT_NOTES[key],
                }
            )
    return CSV_CONVERGENCE


# ---------------------------------------------------------------------------
# Literature comparison
# ---------------------------------------------------------------------------


def write_literature_comparison(*, stats: SubstrateStats) -> Path:
    """Write the side-by-side literature comparison table.

    ``None`` represents missing data (e.g., Mohacsi 2024 reports a gen band,
    not an acceptance rate). It is rendered as a blank CSV cell, never as
    0.0. The 5-seed mean row carries the normal-approx CI bounds inline.
    """
    fieldnames: list[str] = [
        "study",
        "rate_pct",
        "substrate_d",
        "notes",
        "cite_paper_id",
    ]
    CSV_LITERATURE.parent.mkdir(parents=True, exist_ok=True)

    def _opt(value: float | int | None) -> object:
        return "" if value is None else value

    rows: list[dict[str, object]] = [
        {
            "study": "Hay 2011 full envelope",
            "rate_pct": HAY_2011_RATE_PCT,
            "substrate_d": 22,
            "notes": (
                "~2000 accepted / 500K evaluations on L5b pyramidal cell; "
                "full perisomatic + back-propagating AP fits."
            ),
            "cite_paper_id": "10.1371_journal.pcbi.1002107",
        },
        {
            "study": "Hay 2011 perisomatic-only",
            "rate_pct": HAY_2011_PERISOMATIC_RATE_PCT,
            "substrate_d": 22,
            "notes": (
                "52 accepted / 500K evals; substrate-limited counterexample "
                "(perisomatic-only fit set)."
            ),
            "cite_paper_id": "10.1371_journal.pcbi.1002107",
        },
        {
            "study": "Druckmann 2007 baseline",
            "rate_pct": DRUCKMANN_2007_RATE_PCT,
            "substrate_d": 12,
            "notes": ("300 accepted / 300K evals on 12-d cortical interneuron substrate."),
            "cite_paper_id": "10.3389_neuro.01.1.1.001.2007",
        },
        {
            "study": "Mohacsi 2024 convergence band",
            "rate_pct": _opt(None),
            "substrate_d": _opt(None),
            "notes": (
                "NSGA-II asymptotes within 20-60 generations on 3-12 param "
                "problems; reports gen band, not an acceptance rate."
            ),
            "cite_paper_id": "10.1371_journal.pcbi.1012039",
        },
        {
            "study": "This work 5-seed mean (LEGIT canonical)",
            "rate_pct": round(stats.mean_pct, 4),
            "substrate_d": 68,
            "notes": (
                f"t0106/t0112/t0113/t0114/t0115 5-seed batch; normal-approx "
                f"95% CI = ({stats.normal_approx_ci_lo_pct:.2f}, "
                f"{stats.normal_approx_ci_hi_pct:.2f}); bootstrap "
                f"95% CI = ({stats.bootstrap_ci_lo_pct:.2f}, "
                f"{stats.bootstrap_ci_hi_pct:.2f})."
            ),
            "cite_paper_id": _opt(None),
        },
    ]
    with CSV_LITERATURE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return CSV_LITERATURE


# ---------------------------------------------------------------------------
# Pooled LEGIT joint-pass cells (parquet)
# ---------------------------------------------------------------------------

_POOLED_COLUMNS: list[str] = [
    "seed",
    "source_task_id",
    "generation",
    "dsi",
    "pd_rate_hz",
    "cell_id",
]


def build_pooled_legit_cells(
    *,
    eval_paths: dict[str, Path],
) -> pd.DataFrame:
    """Build the pooled LEGIT joint-pass cells DataFrame.

    Dedups per seed by the 68-d parameter vector (the canonical convention)
    and synthesises a stable per-seed cell index as ``cell_id``.
    """
    rows: list[dict[str, object]] = []
    for key in ALL_SEED_KEYS:
        evals = load_evaluations(path=eval_paths[key])
        seen_keys: set[tuple[float, ...]] = set()
        seq: int = 0
        for cell in evals:
            dsi = float(cell["dsi_vector_sum"])
            pd_rate = float(cell["pd_rate_hz"])
            if not is_legit_joint_pass(dsi=dsi, pd_rate_hz=pd_rate):
                continue
            vec_key = cell_vector_key(vector_68d=cell["vector_68d"])
            if vec_key in seen_keys:
                continue
            seen_keys.add(vec_key)
            rows.append(
                {
                    "seed": key,
                    "source_task_id": SEED_TASK_IDS[key],
                    "generation": int(cell["generation"]),
                    "dsi": dsi,
                    "pd_rate_hz": pd_rate,
                    "cell_id": f"{key}_{seq:04d}",
                }
            )
            seq += 1
    df: pd.DataFrame = pd.DataFrame(rows, columns=_POOLED_COLUMNS)
    df = df.astype(
        {
            "seed": pd.StringDtype(),
            "source_task_id": pd.StringDtype(),
            "generation": pd.Int64Dtype(),
            "dsi": np.dtype("float64"),
            "pd_rate_hz": np.dtype("float64"),
            "cell_id": pd.StringDtype(),
        }
    )
    return df


def write_pooled_legit_cells(*, df: pd.DataFrame) -> Path:
    """Write the pooled LEGIT joint-pass DataFrame to parquet.

    Asserts the row count equals the canonical sum
    ``sum(EXPECTED_LEGIT_COUNT.values()) = 675``.
    """
    expected_n: int = sum(EXPECTED_LEGIT_COUNT.values())
    assert len(df) == expected_n, f"pooled LEGIT row count is {expected_n}, got {len(df)}"
    PARQUET_POOLED.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(PARQUET_POOLED, index=False)
    return PARQUET_POOLED
