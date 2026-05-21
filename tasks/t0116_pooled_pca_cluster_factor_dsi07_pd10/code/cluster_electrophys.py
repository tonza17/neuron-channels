"""KMeans on the union-pool z-scored 54-d electrophys subspace, k ∈ {3, 4, 5, 6, 7} silhouette
auto-pick. Emit the silhouette curve and per-cell cluster assignments with PC1/PC2 coords from the
combined 68-d PCA fitted in Step 5.

Inputs:
    data/pooled_survivors.parquet
    data/pooled_standardiser.npz
    data/pca_models.pkl

Outputs:
    results/images/electrophys_silhouette.png
    results/data/electrophys_clusters.csv

Usage:
    uv run python -u -m tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.cluster_electrophys
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

from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.cluster_helpers import (
    KMeansSweepResult,
    PooledStandardiser,
    load_standardiser,
    run_kmeans_sweep,
)
from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.constants import (
    ALL_PARAM_NAMES,
    CHART_DPI,
    K_SWEEP,
    N_ELECTROPHYS_DIMS,
)
from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.paths import (
    ELECTROPHYS_CLUSTERS_CSV,
    ELECTROPHYS_SILHOUETTE_PNG,
    PCA_MODELS_PKL,
    POOLED_STANDARDISER_NPZ,
    POOLED_SURVIVORS_PARQUET,
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


def _plot_silhouette_curve(
    *,
    sweep: KMeansSweepResult,
    output_path: str,
    title: str,
) -> None:
    ks: list[int] = [r.k for r in sweep.sweep]
    silhouettes: list[float] = [r.silhouette for r in sweep.sweep]
    fig, ax = plt.subplots(figsize=(7, 5), dpi=CHART_DPI)
    ax.plot(ks, silhouettes, marker="o", color="#1f77b4", linewidth=1.5)
    for r in sweep.sweep:
        marker_style: str = "*" if r.k == sweep.headline_k else "o"
        marker_color: str = "#d62728" if r.k == sweep.headline_k else "#1f77b4"
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
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def main() -> None:
    df: pd.DataFrame = pd.read_parquet(POOLED_SURVIVORS_PARQUET)
    standardiser: PooledStandardiser = load_standardiser(path=POOLED_STANDARDISER_NPZ)
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
        output_path=str(ELECTROPHYS_SILHOUETTE_PNG),
        title=(
            f"Electrophys 54-d KMeans silhouette sweep (k={sweep.headline_k} headline, n={len(df)})"
        ),
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
    df_out.to_csv(ELECTROPHYS_CLUSTERS_CSV, index=False)
    print(f"Wrote {ELECTROPHYS_CLUSTERS_CSV} (n_rows={len(df_out)})", flush=True)

    # Per-cluster size.
    sizes_by_cluster: pd.Series[int] = df_out.groupby(CLUSTER_ID_COLUMN).size()
    print(f"\nCluster sizes:\n{sizes_by_cluster.to_string()}", flush=True)
    # Seed x cluster crosstab.
    crosstab: pd.DataFrame = pd.crosstab(df_out[SEED_COLUMN], df_out[CLUSTER_ID_COLUMN])
    print(f"\nSeed x cluster crosstab:\n{crosstab.to_string()}", flush=True)


if __name__ == "__main__":
    main()
