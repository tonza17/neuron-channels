"""KMeans on the union-pool z-scored 54-d electrophys subspace, k in K_SWEEP silhouette auto-pick.

Inputs:
    data/t0125_cells.parquet
    data/t0125_standardiser.npz
    data/pca_models.pkl

Outputs:
    results/images/electrophys_silhouette.png
    results/data/electrophys_clusters.csv
"""

from __future__ import annotations

import pickle

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
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.load_t0123_cells import (
    ATP_PER_SPIKE_COLUMN,
    CELL_INDEX_COLUMN,
    DSI_COLUMN,
    GENERATION_COLUMN,
    MI_COLUMN,
    PD_COLUMN,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.paths import (
    ELECTROPHYS_CLUSTERS_CSV,
    ELECTROPHYS_SILHOUETTE_PNG,
    PCA_MODELS_PKL,
    T0123_CELLS_PARQUET,
    T0123_STANDARDISER_NPZ,
)

CLUSTER_ID_COLUMN: str = "cluster_id"
PC1_COMBINED_COLUMN: str = "pc1_combined"
PC2_COMBINED_COLUMN: str = "pc2_combined"
FIRING_HZ_MEAN_COLUMN: str = "firing_hz_mean"


def _plot_silhouette_curve(
    *,
    sweep: KMeansSweepResult,
    output_path,
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

    matrix_68d: NDArray[np.float64] = df[list(ALL_PARAM_NAMES)].to_numpy(dtype=np.float64)
    z_full: NDArray[np.float64] = standardiser.transform(matrix_68d)
    z_ephys: NDArray[np.float64] = z_full[:, :N_ELECTROPHYS_DIMS]
    print(f"Running KMeans on 54-d electrophys submatrix, shape={z_ephys.shape}", flush=True)

    sweep: KMeansSweepResult = run_kmeans_sweep(matrix_zscored=z_ephys)
    print(f"\nKMeans sweep (k in {K_SWEEP}):", flush=True)
    for r in sweep.sweep:
        print(f"  k={r.k}: silhouette={r.silhouette:.4f}, inertia={r.inertia:.2f}", flush=True)
    print(
        f"Headline k={sweep.headline_k}, silhouette={sweep.headline_silhouette:.4f}",
        flush=True,
    )

    _plot_silhouette_curve(
        sweep=sweep,
        output_path=ELECTROPHYS_SILHOUETTE_PNG,
        title=(
            f"Electrophys 54-d KMeans silhouette sweep (k={sweep.headline_k} headline, n={len(df)})"
        ),
        line_color="#1f77b4",
    )
    print(f"Wrote {ELECTROPHYS_SILHOUETTE_PNG}", flush=True)

    pc_combined: NDArray[np.float64] = pca_combined.transform(z_full)
    df_out: pd.DataFrame = df.assign(
        **{
            CLUSTER_ID_COLUMN: sweep.headline_labels.astype(int),
            PC1_COMBINED_COLUMN: pc_combined[:, 0],
            PC2_COMBINED_COLUMN: pc_combined[:, 1],
        }
    )[
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
    df_out.to_csv(ELECTROPHYS_CLUSTERS_CSV, index=False)
    print(f"Wrote {ELECTROPHYS_CLUSTERS_CSV} (n_rows={len(df_out)})", flush=True)

    sizes_by_cluster: pd.Series = df_out.groupby(CLUSTER_ID_COLUMN).size()
    print(f"\nCluster sizes:\n{sizes_by_cluster.to_string()}", flush=True)

    # Per-cluster mean MI / ATP / DSI / PD.
    summary: pd.DataFrame = (
        df_out.groupby(CLUSTER_ID_COLUMN)[[MI_COLUMN, ATP_PER_SPIKE_COLUMN, DSI_COLUMN, PD_COLUMN]]
        .mean()
        .reset_index()
    )
    summary["n_cells"] = df_out.groupby(CLUSTER_ID_COLUMN).size().values
    print(f"\nPer-cluster means:\n{summary.to_string(index=False)}", flush=True)


if __name__ == "__main__":
    main()
