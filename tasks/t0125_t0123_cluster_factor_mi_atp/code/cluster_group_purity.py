"""Cluster-vs-quartile-group purity.

Four (partition, reference) pairs on the SPIKING cohort:
  * (electrophys_cluster, MI_quartile_group)
  * (electrophys_cluster, ATP_quartile_group)
  * (morphology_cluster, MI_quartile_group)
  * (morphology_cluster, ATP_quartile_group)

Each reference assigns each cell to {high, mid, low} based on the q1/q3 thresholds.

Outputs:
    results/data/cluster_group_purity.csv
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy.stats import chi2_contingency
from sklearn.metrics import normalized_mutual_info_score

from tasks.t0125_t0123_cluster_factor_mi_atp.code.load_t0123_cells import (
    ATP_PER_SPIKE_COLUMN,
    CELL_INDEX_COLUMN,
    MI_COLUMN,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.paths import (
    CLUSTER_GROUP_PURITY_CSV,
    ELECTROPHYS_CLUSTERS_CSV,
    GROUP_THRESHOLDS_JSON,
    MORPHOLOGY_CLUSTERS_CSV,
    T0123_SPIKING_CELLS_PARQUET,
)

CLUSTER_ID_COLUMN: str = "cluster_id"
GROUP_HIGH: str = "high"
GROUP_MID: str = "mid"
GROUP_LOW: str = "low"


def _assign_quartile_group(
    *,
    values: NDArray[np.float64],
    q1: float,
    q3: float,
) -> NDArray[np.str_]:
    labels: list[str] = []
    for v in values.tolist():
        if v >= q3:
            labels.append(GROUP_HIGH)
        elif v <= q1:
            labels.append(GROUP_LOW)
        else:
            labels.append(GROUP_MID)
    return np.array(labels, dtype=str)


def _compute_pair(
    *,
    cluster_labels: NDArray[np.int_],
    reference_labels: NDArray[np.str_],
    partition_name: str,
    reference_name: str,
) -> dict[str, object]:
    nmi: float = float(normalized_mutual_info_score(reference_labels, cluster_labels))
    ct = pd.crosstab(pd.Series(reference_labels), pd.Series(cluster_labels))
    chi2_result = chi2_contingency(ct.to_numpy())
    p_value: float = float(chi2_result.pvalue)
    print(
        f"  {partition_name} vs {reference_name}: NMI={nmi:.4f}, chi2_p={p_value:.3e}, "
        f"n_cells={len(cluster_labels)}",
        flush=True,
    )
    return {
        "partition": partition_name,
        "reference": reference_name,
        "nmi": nmi,
        "chi2_p": p_value,
        "n_cells": int(len(cluster_labels)),
    }


def main() -> None:
    df_spiking: pd.DataFrame = pd.read_parquet(T0123_SPIKING_CELLS_PARQUET)
    elec_df: pd.DataFrame = pd.read_csv(ELECTROPHYS_CLUSTERS_CSV)
    morph_df: pd.DataFrame = pd.read_csv(MORPHOLOGY_CLUSTERS_CSV)
    thresholds: dict[str, float] = json.loads(GROUP_THRESHOLDS_JSON.read_text(encoding="utf-8"))

    # Restrict cluster tables to the spiking cohort.
    spiking_idx: set[int] = set(df_spiking[CELL_INDEX_COLUMN].astype(int).tolist())
    elec_spiking: pd.DataFrame = elec_df[elec_df[CELL_INDEX_COLUMN].isin(spiking_idx)].copy()
    morph_spiking: pd.DataFrame = morph_df[morph_df[CELL_INDEX_COLUMN].isin(spiking_idx)].copy()

    # Merge cluster columns onto df_spiking ordering by cell_index.
    df_with_e = df_spiking.merge(
        elec_spiking[[CELL_INDEX_COLUMN, CLUSTER_ID_COLUMN]].rename(
            columns={CLUSTER_ID_COLUMN: "electrophys_cluster"}
        ),
        on=CELL_INDEX_COLUMN,
        how="left",
        validate="one_to_one",
    )
    df_with_em = df_with_e.merge(
        morph_spiking[[CELL_INDEX_COLUMN, CLUSTER_ID_COLUMN]].rename(
            columns={CLUSTER_ID_COLUMN: "morphology_cluster"}
        ),
        on=CELL_INDEX_COLUMN,
        how="left",
        validate="one_to_one",
    )
    assert df_with_em["electrophys_cluster"].notna().all()
    assert df_with_em["morphology_cluster"].notna().all()

    mi_vals: NDArray[np.float64] = df_with_em[MI_COLUMN].to_numpy(dtype=np.float64)
    atp_vals: NDArray[np.float64] = df_with_em[ATP_PER_SPIKE_COLUMN].to_numpy(dtype=np.float64)
    mi_groups: NDArray[np.str_] = _assign_quartile_group(
        values=mi_vals, q1=thresholds["mi_q1"], q3=thresholds["mi_q3"]
    )
    atp_groups: NDArray[np.str_] = _assign_quartile_group(
        values=atp_vals, q1=thresholds["atp_q1"], q3=thresholds["atp_q3"]
    )
    elec_clusters: NDArray[np.int_] = df_with_em["electrophys_cluster"].to_numpy(dtype=np.int_)
    morph_clusters: NDArray[np.int_] = df_with_em["morphology_cluster"].to_numpy(dtype=np.int_)

    rows: list[dict[str, object]] = [
        _compute_pair(
            cluster_labels=elec_clusters,
            reference_labels=mi_groups,
            partition_name="electrophys_cluster",
            reference_name="MI_quartile_group",
        ),
        _compute_pair(
            cluster_labels=elec_clusters,
            reference_labels=atp_groups,
            partition_name="electrophys_cluster",
            reference_name="ATP_quartile_group",
        ),
        _compute_pair(
            cluster_labels=morph_clusters,
            reference_labels=mi_groups,
            partition_name="morphology_cluster",
            reference_name="MI_quartile_group",
        ),
        _compute_pair(
            cluster_labels=morph_clusters,
            reference_labels=atp_groups,
            partition_name="morphology_cluster",
            reference_name="ATP_quartile_group",
        ),
    ]
    out_df: pd.DataFrame = pd.DataFrame(rows)
    CLUSTER_GROUP_PURITY_CSV.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(CLUSTER_GROUP_PURITY_CSV, index=False)
    print(f"\nWrote {CLUSTER_GROUP_PURITY_CSV}", flush=True)
    print(out_df.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
