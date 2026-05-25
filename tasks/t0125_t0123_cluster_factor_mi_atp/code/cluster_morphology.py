"""KMeans on the union-pool z-scored 14-d morphology subspace, k in K_SWEEP silhouette auto-pick.

Outputs:
    results/images/morphology_silhouette.png
    results/data/morphology_clusters.csv
    results/data/morphology_cluster_<cluster_id>_representatives.csv
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

from tasks.t0125_t0123_cluster_factor_mi_atp.code.cluster_helpers import (
    KMeansSweepResult,
    PooledStandardiser,
    load_standardiser,
    run_kmeans_sweep,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.constants import (
    ALL_PARAM_NAMES,
    CHART_DPI,
    K_SWEEP,
    N_ELECTROPHYS_DIMS,
    N_REPRESENTATIVES_PER_CLUSTER,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.load_t0123_cells import (
    ATP_AIS_COLUMN,
    ATP_DENDRITES_COLUMN,
    ATP_PER_SPIKE_COLUMN,
    ATP_SOMA_COLUMN,
    CELL_INDEX_COLUMN,
    DSI_COLUMN,
    GENERATION_COLUMN,
    MI_COLUMN,
    PD_COLUMN,
    SILENCE_FAILED_COLUMN,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.paths import (
    MORPHOLOGY_CLUSTERS_CSV,
    MORPHOLOGY_SILHOUETTE_PNG,
    PCA_MODELS_PKL,
    T0123_CELLS_PARQUET,
    T0123_STANDARDISER_NPZ,
    morphology_cluster_representatives_csv,
)

CLUSTER_ID_COLUMN: str = "cluster_id"
PC1_COMBINED_COLUMN: str = "pc1_combined"
PC2_COMBINED_COLUMN: str = "pc2_combined"
EPHYS_PC1_COLUMN: str = "ephys_PC1"
EPHYS_PC2_COLUMN: str = "ephys_PC2"
EPHYS_PC3_COLUMN: str = "ephys_PC3"
SOMA_SHARE_ATP_COLUMN: str = "soma_share_atp"
BITS_PER_ATP_COLUMN: str = "bits_per_atp"


def _plot_silhouette_curve(
    *,
    sweep: KMeansSweepResult,
    output_path: Path,
    title: str,
    line_color: str,
) -> None:
    ks: list[int] = [r.k for r in sweep.sweep]
    silhouettes: list[float] = [r.silhouette for r in sweep.sweep]
    fig, ax = plt.subplots(figsize=(7, 5), dpi=CHART_DPI)
    ax.plot(ks, silhouettes, marker="o", color=line_color, linewidth=1.5)
    for r in sweep.sweep:
        marker_style: str = "*" if r.k == sweep.headline_k else "o"
        marker_color: str = "#d62728" if r.k == sweep.headline_k else line_color
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
    df: pd.DataFrame = pd.read_parquet(T0123_CELLS_PARQUET)
    standardiser: PooledStandardiser = load_standardiser(path=T0123_STANDARDISER_NPZ)
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
        line_color="#2ca02c",
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
            GENERATION_COLUMN,
            CELL_INDEX_COLUMN,
            MI_COLUMN,
            ATP_PER_SPIKE_COLUMN,
            DSI_COLUMN,
            PD_COLUMN,
            PC1_COMBINED_COLUMN,
            PC2_COMBINED_COLUMN,
        ]
    ]
    df_out.to_csv(MORPHOLOGY_CLUSTERS_CSV, index=False)
    print(f"Wrote {MORPHOLOGY_CLUSTERS_CSV} (n_rows={len(df_out)})", flush=True)

    sizes_by_cluster: pd.Series = df_out.groupby(CLUSTER_ID_COLUMN).size()
    print(f"\nCluster sizes:\n{sizes_by_cluster.to_string()}", flush=True)

    # Representative tables per cluster: 15 rows ranked by bits-per-ATP within the spiking cohort.
    total_ap_atp: pd.Series = (
        df_with_clusters[ATP_SOMA_COLUMN]
        + df_with_clusters[ATP_AIS_COLUMN]
        + df_with_clusters[ATP_DENDRITES_COLUMN]
    )
    df_with_clusters[SOMA_SHARE_ATP_COLUMN] = df_with_clusters[ATP_SOMA_COLUMN] / total_ap_atp
    bits_per_atp_series: pd.Series = df_with_clusters[MI_COLUMN] / df_with_clusters[
        ATP_PER_SPIKE_COLUMN
    ].replace(0.0, np.nan)
    df_with_clusters[BITS_PER_ATP_COLUMN] = bits_per_atp_series

    spiking_mask: pd.Series = (df_with_clusters[PD_COLUMN] > 1.0) & (
        ~df_with_clusters[SILENCE_FAILED_COLUMN].astype(bool)
    )
    df_spiking: pd.DataFrame = df_with_clusters[spiking_mask].copy()

    print("\nWriting per-cluster representative tables...", flush=True)
    df_spiking_sorted: pd.DataFrame = df_spiking.sort_values(
        by=BITS_PER_ATP_COLUMN, ascending=False
    )
    for cluster_id, group in df_spiking_sorted.groupby(CLUSTER_ID_COLUMN, sort=True):
        top: pd.DataFrame = group.head(N_REPRESENTATIVES_PER_CLUSTER).reset_index(drop=True)
        repr_df: pd.DataFrame = top[
            [
                GENERATION_COLUMN,
                CELL_INDEX_COLUMN,
                MI_COLUMN,
                ATP_PER_SPIKE_COLUMN,
                DSI_COLUMN,
                PD_COLUMN,
                EPHYS_PC1_COLUMN,
                EPHYS_PC2_COLUMN,
                EPHYS_PC3_COLUMN,
                SOMA_SHARE_ATP_COLUMN,
            ]
        ]
        out_path: Path = morphology_cluster_representatives_csv(cluster_id=int(cluster_id))
        repr_df.to_csv(out_path, index=False)
        print(f"  cluster {cluster_id} (size={len(group)}) -> {out_path}", flush=True)


if __name__ == "__main__":
    main()
