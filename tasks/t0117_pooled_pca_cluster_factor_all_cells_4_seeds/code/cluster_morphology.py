"""KMeans on the union-pool z-scored 14-d morphology subspace, k ∈ {3, 4, 5, 6, 7} silhouette
auto-pick. For each cluster, build a 15-row representative listing ranked descending by
`dsi * pd_rate_hz`, with electrophys PC1/PC2/PC3 from the pre-fitted 3-component PCA.

Inputs:
    data/pooled_all_cells.parquet
    data/pooled_standardiser.npz
    data/pca_models.pkl

Outputs:
    results/images/morphology_silhouette.png
    results/data/morphology_clusters.csv
    results/data/morphology_cluster_<cluster_id>_representatives.csv (one per cluster)

Usage:
    uv run python -u -m \
        tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.cluster_morphology
"""

from __future__ import annotations

import pickle
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.typing import NDArray
from sklearn.decomposition import PCA

from tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.cluster_helpers import (
    KMeansSweepResult,
    PooledStandardiser,
    load_standardiser,
    run_kmeans_sweep,
)
from tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.constants import (
    ALL_PARAM_NAMES,
    CHART_DPI,
    K_SWEEP,
    N_ELECTROPHYS_DIMS,
    N_REPRESENTATIVES_PER_CLUSTER,
)
from tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.paths import (
    MORPHOLOGY_CLUSTERS_CSV,
    MORPHOLOGY_SILHOUETTE_PNG,
    PCA_MODELS_PKL,
    POOLED_ALL_CELLS_PARQUET,
    POOLED_STANDARDISER_NPZ,
    morphology_cluster_representatives_csv,
)

SOURCE_TASK_COLUMN: str = "source_task"
SEED_COLUMN: str = "seed"
GENERATION_COLUMN: str = "generation"
INDIVIDUAL_IDX_COLUMN: str = "individual_idx"
DSI_COLUMN: str = "dsi_vector_sum"
PD_COLUMN: str = "pd_rate_hz"
CLUSTER_ID_COLUMN: str = "cluster_id"
PC1_COMBINED_COLUMN: str = "pc1_combined"
PC2_COMBINED_COLUMN: str = "pc2_combined"
EPHYS_PC1_COLUMN: str = "ephys_pc1"
EPHYS_PC2_COLUMN: str = "ephys_pc2"
EPHYS_PC3_COLUMN: str = "ephys_pc3"


def _plot_silhouette_curve(
    *,
    sweep: KMeansSweepResult,
    output_path: Path,
    title: str,
) -> None:
    ks: list[int] = [r.k for r in sweep.sweep]
    silhouettes: list[float] = [r.silhouette for r in sweep.sweep]
    fig, ax = plt.subplots(figsize=(7, 5), dpi=CHART_DPI)
    ax.plot(ks, silhouettes, marker="o", color="#2ca02c", linewidth=1.5)
    for r in sweep.sweep:
        marker_style: str = "*" if r.k == sweep.headline_k else "o"
        marker_color: str = "#d62728" if r.k == sweep.headline_k else "#2ca02c"
        ax.scatter(
            [r.k],
            [r.silhouette],
            marker=marker_style,
            s=180 if r.k == sweep.headline_k else 50,
            color=marker_color,
            zorder=3,
            label=f"k={r.k}" + (" (headline)" if r.k == sweep.headline_k else ""),
        )
    ax.set_xticks(list(K_SWEEP))
    ax.set_xlabel("k")
    ax.set_ylabel("mean silhouette score")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def main() -> None:
    df: pd.DataFrame = pd.read_parquet(POOLED_ALL_CELLS_PARQUET)
    standardiser: PooledStandardiser = load_standardiser(path=POOLED_STANDARDISER_NPZ)
    with open(PCA_MODELS_PKL, "rb") as fh:
        pca_models: dict[str, PCA] = pickle.load(fh)  # noqa: S301 — repo-local pickle.
    pca_combined: PCA = pca_models["pca_combined"]
    pca_ephys_3d: PCA = pca_models["pca_ephys_3d"]

    matrix_68d: NDArray[np.float64] = df[list(ALL_PARAM_NAMES)].to_numpy(dtype=np.float64)
    z_full: NDArray[np.float64] = standardiser.transform(matrix_68d)
    z_morph: NDArray[np.float64] = z_full[:, N_ELECTROPHYS_DIMS:]
    print(f"Running KMeans on 14-d morphology submatrix, shape={z_morph.shape}", flush=True)

    sweep: KMeansSweepResult = run_kmeans_sweep(matrix_zscored=z_morph)
    print(f"\nKMeans sweep (k in {K_SWEEP}):", flush=True)
    for r in sweep.sweep:
        print(f"  k={r.k}: silhouette={r.silhouette:.4f}, inertia={r.inertia:.2f}", flush=True)
    print(
        f"Headline k={sweep.headline_k}, silhouette={sweep.headline_silhouette:.4f}",
        flush=True,
    )

    _plot_silhouette_curve(
        sweep=sweep,
        output_path=MORPHOLOGY_SILHOUETTE_PNG,
        title=(
            f"Morphology 14-d KMeans silhouette sweep (k={sweep.headline_k} headline, n={len(df)})"
        ),
    )
    print(f"Wrote {MORPHOLOGY_SILHOUETTE_PNG}", flush=True)

    pc_combined: NDArray[np.float64] = pca_combined.transform(z_full)
    pc_ephys_3d: NDArray[np.float64] = pca_ephys_3d.transform(z_full[:, :N_ELECTROPHYS_DIMS])
    df_with_clusters: pd.DataFrame = df.assign(
        **{
            CLUSTER_ID_COLUMN: sweep.headline_labels.astype(int),
            PC1_COMBINED_COLUMN: pc_combined[:, 0],
            PC2_COMBINED_COLUMN: pc_combined[:, 1],
            EPHYS_PC1_COLUMN: pc_ephys_3d[:, 0],
            EPHYS_PC2_COLUMN: pc_ephys_3d[:, 1],
            EPHYS_PC3_COLUMN: pc_ephys_3d[:, 2],
        }
    )

    df_out: pd.DataFrame = df_with_clusters[
        [
            CLUSTER_ID_COLUMN,
            SOURCE_TASK_COLUMN,
            SEED_COLUMN,
            GENERATION_COLUMN,
            INDIVIDUAL_IDX_COLUMN,
            DSI_COLUMN,
            PD_COLUMN,
            PC1_COMBINED_COLUMN,
            PC2_COMBINED_COLUMN,
        ]
    ]
    df_out.to_csv(MORPHOLOGY_CLUSTERS_CSV, index=False)
    print(f"Wrote {MORPHOLOGY_CLUSTERS_CSV} (n_rows={len(df_out)})", flush=True)

    sizes_by_cluster: pd.Series[int] = df_out.groupby(CLUSTER_ID_COLUMN).size()
    print(f"\nCluster sizes:\n{sizes_by_cluster.to_string()}", flush=True)
    crosstab: pd.DataFrame = pd.crosstab(df_out[SEED_COLUMN], df_out[CLUSTER_ID_COLUMN])
    print(f"\nSeed x cluster crosstab:\n{crosstab.to_string()}", flush=True)

    # Representative tables per cluster.
    print("\nWriting per-cluster representative tables...", flush=True)
    df_with_clusters = df_with_clusters.assign(
        _rank_score=df_with_clusters[DSI_COLUMN] * df_with_clusters[PD_COLUMN]
    ).sort_values(by="_rank_score", ascending=False)
    for cluster_id, group in df_with_clusters.groupby(CLUSTER_ID_COLUMN, sort=True):
        top: pd.DataFrame = group.head(N_REPRESENTATIVES_PER_CLUSTER).reset_index(drop=True)
        repr_df: pd.DataFrame = top[
            [
                SOURCE_TASK_COLUMN,
                SEED_COLUMN,
                GENERATION_COLUMN,
                DSI_COLUMN,
                PD_COLUMN,
                EPHYS_PC1_COLUMN,
                EPHYS_PC2_COLUMN,
                EPHYS_PC3_COLUMN,
            ]
        ]
        out_path: Path = morphology_cluster_representatives_csv(cluster_id=int(cluster_id))
        repr_df.to_csv(out_path, index=False)
        print(f"  cluster {cluster_id} (size={len(group)}) -> {out_path}", flush=True)


if __name__ == "__main__":
    main()
