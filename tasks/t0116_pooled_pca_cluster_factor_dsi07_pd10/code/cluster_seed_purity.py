"""Compute cluster-vs-seed purity for both KMeans partitions.

For each partition, report:
  (a) Normalised mutual information (NMI) between cluster_id and seed.
  (b) Chi-square contingency test (chi2, p_value, dof) on the cluster x seed crosstab.

Outputs:
    results/data/cluster_seed_purity.csv

Usage:
    uv run python -u -m tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.cluster_seed_purity
"""

from __future__ import annotations

import pandas as pd
from scipy.stats import chi2_contingency
from sklearn.metrics import normalized_mutual_info_score

from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.paths import (
    CLUSTER_SEED_PURITY_CSV,
    ELECTROPHYS_CLUSTERS_CSV,
    MORPHOLOGY_CLUSTERS_CSV,
)

CLUSTER_ID_COLUMN: str = "cluster_id"
SEED_COLUMN: str = "seed"


def _compute_partition_metrics(*, df: pd.DataFrame, label: str) -> dict[str, object]:
    seeds = df[SEED_COLUMN].astype(int).to_numpy()
    clusters = df[CLUSTER_ID_COLUMN].astype(int).to_numpy()
    nmi: float = float(normalized_mutual_info_score(seeds, clusters))
    crosstab: pd.DataFrame = pd.crosstab(df[SEED_COLUMN], df[CLUSTER_ID_COLUMN])
    chi2_result = chi2_contingency(crosstab.to_numpy())
    chi2_stat: float = float(chi2_result.statistic)
    p_value: float = float(chi2_result.pvalue)
    dof: int = int(chi2_result.dof)
    # Warn if any expected cell count < 5 (chi-square asymptotic invalid).
    n_low_expected: int = int((chi2_result.expected_freq < 5).sum())
    n_total_cells: int = int(chi2_result.expected_freq.size)
    print(
        f"{label}: NMI={nmi:.4f}, chi2={chi2_stat:.2f}, p={p_value:.3e}, dof={dof}, "
        f"low_expected={n_low_expected}/{n_total_cells}",
        flush=True,
    )
    return {
        "partition": label,
        "k": int(crosstab.shape[1]),
        "nmi": nmi,
        "chi2": chi2_stat,
        "p_value": p_value,
        "dof": dof,
        "n_expected_below_5": n_low_expected,
        "n_total_cells": n_total_cells,
    }


def main() -> None:
    elec_df: pd.DataFrame = pd.read_csv(ELECTROPHYS_CLUSTERS_CSV)
    morph_df: pd.DataFrame = pd.read_csv(MORPHOLOGY_CLUSTERS_CSV)

    rows: list[dict[str, object]] = []
    rows.append(
        _compute_partition_metrics(
            df=elec_df,
            label=f"electrophys_k={int(elec_df[CLUSTER_ID_COLUMN].nunique())}",
        )
    )
    rows.append(
        _compute_partition_metrics(
            df=morph_df,
            label=f"morphology_k={int(morph_df[CLUSTER_ID_COLUMN].nunique())}",
        )
    )
    out_df: pd.DataFrame = pd.DataFrame(rows)
    CLUSTER_SEED_PURITY_CSV.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(CLUSTER_SEED_PURITY_CSV, index=False)
    print(f"\nWrote {CLUSTER_SEED_PURITY_CSV}", flush=True)
    print(out_df.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
