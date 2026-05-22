"""Join t0117 cluster assignments with the 68-d feature vectors (REQ-1).

Reads ``tasks/t0117_*/results/data/electrophys_clusters.csv`` and
``tasks/t0117_*/data/pooled_all_cells.parquet`` and joins on the canonical primary key
``(source_task, seed, generation, individual_idx)``. Returns one DataFrame with the cluster id,
DSI / PD-rate, and all 68 named feature columns ready for stratified sampling.
"""

from __future__ import annotations

import pandas as pd

from tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.constants import (
    ALL_PARAM_NAMES,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.constants import (
    CLUSTER_ID_COL,
    DSI_COL,
    GENERATION_COL,
    INDIVIDUAL_IDX_COL,
    PD_RATE_COL,
    SEED_COL,
    SOURCE_TASK_COL,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.paths import (
    T0117_ELECTROPHYS_CLUSTERS_CSV,
    T0117_POOLED_PARQUET,
)

# Primary key for the join (matches t0117 / t0116 / t0108 convention).
_PRIMARY_KEY_COLS: list[str] = [
    SOURCE_TASK_COL,
    SEED_COL,
    GENERATION_COL,
    INDIVIDUAL_IDX_COL,
]


def load_clusters_with_vectors() -> pd.DataFrame:
    """Load t0117 cluster assignments joined with 68-d vectors and DSI/PD per cell.

    Returns a DataFrame with one row per cell. Columns:
        - cluster_id (int)
        - source_task, seed, generation, individual_idx (primary key, taken from the cluster CSV)
        - dsi_vector_sum, pd_rate_hz (float)
        - all 68 named feature columns from ALL_PARAM_NAMES (float, in canonical order)

    Asserts the join produces exactly one row per (cluster CSV) row (no orphans).
    """
    clusters: pd.DataFrame = pd.read_csv(
        filepath_or_buffer=T0117_ELECTROPHYS_CLUSTERS_CSV,
    )
    pooled: pd.DataFrame = pd.read_parquet(path=T0117_POOLED_PARQUET)

    # Drop dsi_vector_sum and pd_rate_hz from pooled (they exist in clusters; avoid _x/_y suffix).
    pooled_for_join: pd.DataFrame = pooled.drop(
        columns=[DSI_COL, PD_RATE_COL],
    )

    expected_rows: int = len(clusters)
    joined: pd.DataFrame = pd.merge(
        left=clusters,
        right=pooled_for_join,
        on=_PRIMARY_KEY_COLS,
        how="left",
        validate="one_to_one",
    )

    # No orphan rows.
    assert len(joined) == expected_rows, (
        f"join produced {len(joined)} rows, expected {expected_rows}"
    )
    n_missing_morph: int = int(joined["morph_seed"].isna().sum())
    assert n_missing_morph == 0, (
        f"{n_missing_morph} cluster cells failed to join to pooled feature vectors"
    )

    # Sanity check: all 68 feature columns present.
    missing_features: list[str] = [c for c in ALL_PARAM_NAMES if c not in joined.columns]
    assert len(missing_features) == 0, f"missing feature columns: {missing_features[:5]}..."

    # Final column ordering: identifiers + DSI/PD + 68 features.
    front_cols: list[str] = [
        CLUSTER_ID_COL,
        *_PRIMARY_KEY_COLS,
        DSI_COL,
        PD_RATE_COL,
    ]
    feature_cols: list[str] = list(ALL_PARAM_NAMES)
    final_cols: list[str] = front_cols + feature_cols
    return joined[final_cols].copy()


def main() -> None:
    """CLI entry: load and print summary stats."""
    df: pd.DataFrame = load_clusters_with_vectors()
    print(f"loaded {len(df)} cells from t0117")
    print("per-cluster row counts:")
    print(df.groupby(CLUSTER_ID_COL).size())
    print("column count:", len(df.columns))


if __name__ == "__main__":
    main()
