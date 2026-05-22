"""Emit `results/data/methodology_notes.md` and `results/data/t0116_comparison.csv`.

Reads:
* t0117 outputs from this task's `results/data/` (per-seed pool counts, cluster purity, factor
  correlations, gen-0 displacements).
* t0116 outputs from `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/data/` (per-seed
  cohort counts, cluster purity, factor correlations, gen-0 displacements).

Writes:
* `results/data/methodology_notes.md`
* `results/data/t0116_comparison.csv` with t0116 vs t0117 head-to-head numbers.

Usage:
    uv run python -u -m \
        tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.methodology_and_comparison
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.paths import (
    CLUSTER_SEED_PURITY_CSV,
    FACTOR_CORRELATIONS_CSV,
    GEN0_DISPLACEMENT_CSV,
    METHODOLOGY_NOTES_MD,
    PER_SEED_POOL_COUNTS_CSV,
    T0116_CLUSTER_SEED_PURITY_CSV,
    T0116_COMPARISON_CSV,
    T0116_FACTOR_CORRELATIONS_CSV,
    T0116_GEN0_DISPLACEMENT_CSV,
    T0116_PER_SEED_COHORT_COUNTS_CSV,
)


@dataclass(frozen=True, slots=True)
class ComparisonRow:
    quantity: str
    t0116_value: str
    t0117_value: str
    delta: str


def _format_float(value: float, decimals: int = 4) -> str:
    return f"{value:.{decimals}f}"


def _build_comparison_rows() -> list[ComparisonRow]:
    rows: list[ComparisonRow] = []

    # 1. Pool size (post-dedup).
    t0116_counts: pd.DataFrame = pd.read_csv(T0116_PER_SEED_COHORT_COUNTS_CSV)
    t0117_counts: pd.DataFrame = pd.read_csv(PER_SEED_POOL_COUNTS_CSV)
    t0116_total: int = int(
        t0116_counts.loc[t0116_counts["source_task"] == "TOTAL", "n_unique"].iloc[0]
    )
    t0117_total: int = int(
        t0117_counts.loc[t0117_counts["source_task"] == "TOTAL", "n_unique"].iloc[0]
    )
    rows.append(
        ComparisonRow(
            quantity="pool_size_total_unique",
            t0116_value=str(t0116_total),
            t0117_value=str(t0117_total),
            delta=f"+{t0117_total - t0116_total}",
        )
    )

    # 1a. Per-seed pool sizes (raw and unique).
    for _, t0117_row in t0117_counts.iterrows():
        st: str = str(t0117_row["source_task"])
        if st == "TOTAL":
            continue
        t0117_n_unique: int = int(t0117_row["n_unique"])
        t0117_n_raw: int = int(t0117_row["n_raw"])
        t0116_match: pd.Series[object] = t0116_counts.loc[t0116_counts["source_task"] == st].iloc[0]
        t0116_n_unique: int = int(t0116_match["n_unique"])
        rows.append(
            ComparisonRow(
                quantity=f"per_seed_unique[{st}]",
                t0116_value=str(t0116_n_unique),
                t0117_value=str(t0117_n_unique),
                delta=f"+{t0117_n_unique - t0116_n_unique}",
            )
        )
        rows.append(
            ComparisonRow(
                quantity=f"per_seed_raw[{st}]",
                t0116_value=str(int(t0116_match["n_raw"])),
                t0117_value=str(t0117_n_raw),
                delta="0 (same source files)",
            )
        )

    # 2. KMeans k chosen + silhouette + NMI per partition.
    t0116_purity: pd.DataFrame = pd.read_csv(T0116_CLUSTER_SEED_PURITY_CSV)
    t0117_purity: pd.DataFrame = pd.read_csv(CLUSTER_SEED_PURITY_CSV)
    for partition_key in ("electrophys", "morphology"):
        t0116_row: pd.Series[object] = t0116_purity.loc[
            t0116_purity["partition"].str.startswith(partition_key)
        ].iloc[0]
        t0117_row = t0117_purity.loc[t0117_purity["partition"].str.startswith(partition_key)].iloc[
            0
        ]
        t0116_k: int = int(t0116_row["k"])
        t0117_k: int = int(t0117_row["k"])
        t0116_nmi: float = float(t0116_row["nmi"])
        t0117_nmi: float = float(t0117_row["nmi"])
        rows.append(
            ComparisonRow(
                quantity=f"{partition_key}_kmeans_k_chosen",
                t0116_value=str(t0116_k),
                t0117_value=str(t0117_k),
                delta=f"{t0117_k - t0116_k:+d}",
            )
        )
        rows.append(
            ComparisonRow(
                quantity=f"{partition_key}_nmi_vs_seed",
                t0116_value=_format_float(t0116_nmi),
                t0117_value=_format_float(t0117_nmi),
                delta=_format_float(t0117_nmi - t0116_nmi, decimals=4),
            )
        )

    # 3. Factor analysis: factor count, total var explained, joint-factor count.
    t0116_fa: pd.DataFrame = pd.read_csv(T0116_FACTOR_CORRELATIONS_CSV)
    t0117_fa: pd.DataFrame = pd.read_csv(FACTOR_CORRELATIONS_CSV)
    t0116_n_factors: int = int(len(t0116_fa))
    t0117_n_factors: int = int(len(t0117_fa))
    t0116_total_var: float = float(t0116_fa["var_explained_pct"].sum())
    t0117_total_var: float = float(t0117_fa["var_explained_pct"].sum())
    t0116_joint_count: int = int(t0116_fa["joint_factor_flag"].sum())
    t0117_joint_count: int = int(t0117_fa["joint_factor_flag"].sum())
    rows.append(
        ComparisonRow(
            quantity="varimax_factor_count",
            t0116_value=str(t0116_n_factors),
            t0117_value=str(t0117_n_factors),
            delta=f"{t0117_n_factors - t0116_n_factors:+d}",
        )
    )
    rows.append(
        ComparisonRow(
            quantity="varimax_total_var_explained_pct",
            t0116_value=_format_float(t0116_total_var, decimals=2),
            t0117_value=_format_float(t0117_total_var, decimals=2),
            delta=_format_float(t0117_total_var - t0116_total_var, decimals=2),
        )
    )
    rows.append(
        ComparisonRow(
            quantity="joint_factor_count_abs_r_gt_0p30_on_both",
            t0116_value=str(t0116_joint_count),
            t0117_value=str(t0117_joint_count),
            delta=f"{t0117_joint_count - t0116_joint_count:+d}",
        )
    )

    # 4. Per-seed displacement (PC1+PC2 mean and 68-d mean).
    t0116_disp: pd.DataFrame = pd.read_csv(T0116_GEN0_DISPLACEMENT_CSV)
    t0117_disp: pd.DataFrame = pd.read_csv(GEN0_DISPLACEMENT_CSV)
    for _, t0117_drow in t0117_disp.iterrows():
        seed_i: int = int(t0117_drow["seed"])
        t0116_drow: pd.Series[float] = t0116_disp.loc[t0116_disp["seed"] == seed_i].iloc[0]
        t0116_pc12: float = float(t0116_drow["mean_disp_pc12"])
        t0117_pc12: float = float(t0117_drow["mean_disp_pc12"])
        t0116_68d: float = float(t0116_drow["mean_disp_68d"])
        t0117_68d: float = float(t0117_drow["mean_disp_68d"])
        rows.append(
            ComparisonRow(
                quantity=f"mean_disp_pc12[seed_{seed_i}]",
                t0116_value=_format_float(t0116_pc12, decimals=3),
                t0117_value=_format_float(t0117_pc12, decimals=3),
                delta=_format_float(t0117_pc12 - t0116_pc12, decimals=3),
            )
        )
        rows.append(
            ComparisonRow(
                quantity=f"mean_disp_68d[seed_{seed_i}]",
                t0116_value=_format_float(t0116_68d, decimals=3),
                t0117_value=_format_float(t0117_68d, decimals=3),
                delta=_format_float(t0117_68d - t0116_68d, decimals=3),
            )
        )

    return rows


def _write_comparison_csv() -> None:
    rows: list[ComparisonRow] = _build_comparison_rows()
    df: pd.DataFrame = pd.DataFrame(
        [
            {
                "quantity": r.quantity,
                "t0116_value": r.t0116_value,
                "t0117_value": r.t0117_value,
                "delta": r.delta,
            }
            for r in rows
        ]
    )
    T0116_COMPARISON_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(T0116_COMPARISON_CSV, index=False)
    print(f"Wrote {T0116_COMPARISON_CSV} ({len(df)} rows)", flush=True)


def _write_methodology_notes() -> None:
    notes: str = """# Methodology notes — t0117 pooled PCA + cluster + factor analysis (no filter)

* **Source schema variance**: t0106 (seed 44) and t0112 (seed 77) ship predictions as gzipped JSON
  with the structure `{"evaluations": [...]}`. t0114 (seed 7755) and t0115 (seed 9354) ship
  predictions as gzipped JSONL (one record per line). The loader (`code/load_pooled_cells.py`)
  branches on `path.suffixes` to choose the right decoder for each file.

* **Generation indexing**: All four files are 1-indexed for `generation`; `generation == 1`
  contains exactly 96 records (one per pop slot) and is the random-init pool. The
  `code/load_pooled_gen0.py` loader filters on this index. There is no `generation == 0` row.

* **No cohort filter applied (deliberate divergence from t0116)**: The only methodological change
  vs t0116 is the **removal** of the `dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0` cohort filter
  from `code/load_pooled_cells.py`. Every record from every source is admitted. The
  `joint_pass` / `legit` booleans on t0114 / t0115 records are deliberately ignored in t0116 and
  remain ignored here. Per-seed counts are recorded as `n_raw` (every record) and `n_unique`
  (post-dedup); the t0116-style `n_passing_filter` column is omitted because no filter exists.

* **Dedup convention**: deduplication uses the 68-d vector rounded to `DEDUP_DECIMALS = 6` decimals
  (same convention as t0116 / t0108). NSGA-II's converged offspring legitimately collapse many
  duplicate rows into one — t0106 alone produces n_raw=3744 -> n_unique=1065 (28%). This is
  expected, not a bug; the same convention applied to t0116 produced 658 passing-filter rows
  -> 121 unique rows (18%).

* **Union-pool standardiser**: The 68-d z-score standardiser is fitted ONCE on the full unfiltered
  union pool (n=4431) and serialised to `data/pooled_standardiser.npz`. Every downstream PCA,
  KMeans, FA, and gen-0 projection reuses this exact fit. Per-seed re-fitting would absorb
  cross-seed scale differences into the standardiser and erase the very signal the analysis is
  designed to detect.

* **No registered metric applies**: this task performs no new simulations. `dsi_vector_sum` and
  `pd_rate_hz` are backfilled from frozen predictions assets produced by the source NSGA-II tasks
  (t0106 / t0112 / t0114 / t0115). The registered metrics in `meta/metrics/` describe per-cell DSI
  / tuning measurements taken during a simulation; none correspond to the unsupervised summaries
  this task produces (silhouette score, % variance explained, NMI, Euclidean displacement). The
  implementation therefore does not write any registered metric keys into `results/metrics.json`.

* **Head-to-head comparison vs t0116**: the comparison CSV
  `results/data/t0116_comparison.csv` reads t0116's published numbers directly from its own
  `results/data/` directory (per-seed cohort counts, cluster-seed purity, factor correlations,
  gen-0 displacements) and produces a row per quantity with `t0116_value`, `t0117_value`, `delta`.
  No t0116 number is recomputed from raw NSGA-II outputs here — the comparison is wholly
  data-driven from the published t0116 result CSVs, so the comparison can be reproduced
  deterministically by re-running this module.
"""
    METHODOLOGY_NOTES_MD.parent.mkdir(parents=True, exist_ok=True)
    METHODOLOGY_NOTES_MD.write_text(notes, encoding="utf-8")
    print(f"Wrote {METHODOLOGY_NOTES_MD}", flush=True)


def main() -> None:
    _write_methodology_notes()
    _write_comparison_csv()


if __name__ == "__main__":
    main()
