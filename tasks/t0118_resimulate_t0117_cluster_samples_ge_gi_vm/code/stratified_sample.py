"""Stratified DSI x PD-rate sampler producing 10 cells per cluster (REQ-2, REQ-3).

For each cluster c in {0, 1, 2, 3}:
1. Compute 5 DSI quintile edges and 5 PD-rate quintile edges over the cluster's cells.
2. Assign each cell its (dsi_quintile, pd_quintile) bin index (in [0..4]).
3. Walk the 25 bins in canonical raster order (dsi_quintile ascending, then pd_quintile ascending)
   taking one cell per occupied bin until 10 are selected. Tie-break inside a bin by
   ``numpy.random.default_rng(SAMPLE_SEED).choice``.
4. If fewer than 10 occupied bins exist, top up by picking the next-most-distant cell in the
   standardised DSI x PD plane until 10 are selected.

Writes the resulting 40-row manifest to ``results/data/selected_cells.csv`` with the column order
from ``SELECTED_CELLS_COLUMNS``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.constants import (
    CLUSTER_ID_COL,
    DSI_COL,
    DSI_QUINTILE_COL,
    GENERATION_COL,
    INDIVIDUAL_IDX_COL,
    N_CELLS_PER_CLUSTER,
    N_CLUSTERS,
    N_DSI_QUINTILES,
    N_PD_QUINTILES,
    N_SELECTED_CELLS_TOTAL,
    PD_QUINTILE_COL,
    PD_RATE_COL,
    SAMPLE_SEED,
    SEED_COL,
    SELECTED_CELLS_COLUMNS,
    SOURCE_TASK_COL,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.load_t0117_clusters import (
    load_clusters_with_vectors,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.paths import (
    SELECTED_CELLS_CSV,
)


def _assign_quintile(*, values: np.ndarray, n_quintiles: int) -> np.ndarray:
    """Return per-row quintile index in [0..n_quintiles-1] using pd.qcut with duplicates='drop'.

    If the data is highly degenerate (fewer unique values than n_quintiles), assigns all rows to
    the lowest bin. The returned array has the same length as ``values``.
    """
    series: pd.Series = pd.Series(values)
    bins: pd.Series = pd.qcut(
        x=series,
        q=n_quintiles,
        labels=False,
        duplicates="drop",
    )
    # If qcut collapses bins, integers may still go up to fewer than n_quintiles-1.
    # NaN values become NaN; coerce to 0 for safety, but no NaN expected here.
    return bins.fillna(0).astype(np.int64).to_numpy()


def _select_one_cluster(
    *,
    df_cluster: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Pick 10 cells from one cluster's DataFrame via raster-order quintile bin walk + top-up."""
    n_avail: int = len(df_cluster)
    assert n_avail >= N_CELLS_PER_CLUSTER, (
        f"cluster has only {n_avail} cells; cannot pick {N_CELLS_PER_CLUSTER}"
    )

    df: pd.DataFrame = df_cluster.copy().reset_index(drop=True)
    df[DSI_QUINTILE_COL] = _assign_quintile(
        values=df[DSI_COL].to_numpy(),
        n_quintiles=N_DSI_QUINTILES,
    )
    df[PD_QUINTILE_COL] = _assign_quintile(
        values=df[PD_RATE_COL].to_numpy(),
        n_quintiles=N_PD_QUINTILES,
    )

    selected_idx: list[int] = []
    # Walk bins in raster order: dsi_quintile ascending, pd_quintile ascending.
    for d_bin in range(N_DSI_QUINTILES):
        for p_bin in range(N_PD_QUINTILES):
            if len(selected_idx) >= N_CELLS_PER_CLUSTER:
                break
            mask = (df[DSI_QUINTILE_COL] == d_bin) & (df[PD_QUINTILE_COL] == p_bin)
            candidates: np.ndarray = np.flatnonzero(mask.to_numpy())
            if candidates.size == 0:
                continue
            # Pick one cell from this bin (deterministic with rng for tie-break).
            chosen: int = int(rng.choice(candidates))
            selected_idx.append(chosen)
        if len(selected_idx) >= N_CELLS_PER_CLUSTER:
            break

    # Top-up rule: pick max-Euclidean-distance cells in standardised (DSI, PD) until 10 are picked.
    if len(selected_idx) < N_CELLS_PER_CLUSTER:
        dsi_std: float = float(df[DSI_COL].std())
        pd_std: float = float(df[PD_RATE_COL].std())
        dsi_std = dsi_std if dsi_std > 1e-9 else 1.0
        pd_std = pd_std if pd_std > 1e-9 else 1.0

        dsi_z: np.ndarray = (df[DSI_COL].to_numpy() - df[DSI_COL].mean()) / dsi_std
        pd_z: np.ndarray = (df[PD_RATE_COL].to_numpy() - df[PD_RATE_COL].mean()) / pd_std

        while len(selected_idx) < N_CELLS_PER_CLUSTER:
            sel_arr: np.ndarray = np.asarray(selected_idx, dtype=np.int64)
            sel_dsi: np.ndarray = dsi_z[sel_arr]
            sel_pd: np.ndarray = pd_z[sel_arr]
            best_idx: int = -1
            best_dist: float = -1.0
            for i in range(len(df)):
                if i in selected_idx:
                    continue
                dx = dsi_z[i] - sel_dsi
                dy = pd_z[i] - sel_pd
                dists = np.sqrt(dx * dx + dy * dy)
                min_dist: float = float(dists.min())
                if min_dist > best_dist:
                    best_dist = min_dist
                    best_idx = i
            assert best_idx >= 0, "top-up search failed to find a candidate"
            selected_idx.append(best_idx)

    assert len(selected_idx) == N_CELLS_PER_CLUSTER
    return df.iloc[selected_idx].copy()


def stratified_sample_cells() -> pd.DataFrame:
    """Produce the 40-cell manifest: 10 cells per cluster, stratified by DSI x PD quintile."""
    df_all: pd.DataFrame = load_clusters_with_vectors()
    cluster_ids_present: list[int] = sorted(int(x) for x in df_all[CLUSTER_ID_COL].unique())
    assert cluster_ids_present == list(range(N_CLUSTERS)), (
        f"expected cluster ids {list(range(N_CLUSTERS))}, got {cluster_ids_present}"
    )

    rng: np.random.Generator = np.random.default_rng(SAMPLE_SEED)
    parts: list[pd.DataFrame] = []
    for c in range(N_CLUSTERS):
        df_cluster: pd.DataFrame = df_all.loc[df_all[CLUSTER_ID_COL] == c]
        picked: pd.DataFrame = _select_one_cluster(df_cluster=df_cluster, rng=rng)
        parts.append(picked)

    manifest: pd.DataFrame = pd.concat(parts, ignore_index=True)
    assert len(manifest) == N_SELECTED_CELLS_TOTAL, (
        f"manifest has {len(manifest)} rows, expected {N_SELECTED_CELLS_TOTAL}"
    )
    # Uniqueness check on primary key.
    key_cols: list[str] = [SOURCE_TASK_COL, SEED_COL, GENERATION_COL, INDIVIDUAL_IDX_COL]
    n_unique: int = manifest.groupby(key_cols).ngroups
    assert n_unique == N_SELECTED_CELLS_TOTAL, (
        f"primary key not unique: {n_unique} unique tuples for {N_SELECTED_CELLS_TOTAL} rows"
    )
    # Per-cluster row count.
    for c in range(N_CLUSTERS):
        n_c: int = int((manifest[CLUSTER_ID_COL] == c).sum())
        expected: int = N_CELLS_PER_CLUSTER
        assert n_c == expected, f"cluster {c}: got {n_c} rows (expected {expected})"

    return manifest


def main() -> None:
    """CLI: produce selected_cells.csv with the canonical column order."""
    manifest_full: pd.DataFrame = stratified_sample_cells()
    SELECTED_CELLS_CSV.parent.mkdir(parents=True, exist_ok=True)
    # Project manifest to required columns only.
    out: pd.DataFrame = manifest_full[list(SELECTED_CELLS_COLUMNS)].copy()
    out.to_csv(path_or_buf=SELECTED_CELLS_CSV, index=False)
    print(f"wrote manifest with {len(out)} rows to {SELECTED_CELLS_CSV}")
    print("per-cluster cell counts:")
    print(out.groupby(CLUSTER_ID_COL).size())


if __name__ == "__main__":
    main()
