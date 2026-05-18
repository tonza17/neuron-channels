"""PCA + K-means on the 14-d morphology submatrix, with 54-d electrophys overlays.

Outputs:
  results/data/morphology_clusters.json
  results/images/pca_morphology_by_cluster.png
  results/images/pca_morphology_by_dsi_pd.png
  results/images/electrophys_overlay_by_morphology_cluster.png

Usage:
  uv run python -m tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.cluster_morphology
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from scipy.stats import kruskal

from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.cluster_helpers import (
    KMeansSweepResult,
    PCAResult,
    run_kmeans_sweep,
    run_pca,
    top_k_loadings,
    write_json,
    zscore_matrix,
)
from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.constants import (
    CHART_DPI,
    ELECTROPHYS_PARAM_NAMES,
    MORPHOLOGY_PARAM_NAMES,
    N_ELECTROPHYS_DIMS,
    N_MORPHOLOGY_DIMS,
)
from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.paths import (
    ELECTROPHYS_OVERLAY_PNG,
    FILTERED_CELLS_JSON,
    MORPHOLOGY_CLUSTERS_JSON,
    PCA_MORPHOLOGY_BY_CLUSTER_PNG,
    PCA_MORPHOLOGY_BY_DSI_PD_PNG,
)


@dataclass(frozen=True, slots=True)
class ParamGroupTest:
    parameter: str
    H: float
    p_raw: float
    p_bonferroni: float
    cluster_means: list[float]
    cluster_stds: list[float]
    cluster_medians: list[float]


def _load_cells(path: Path) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cells = payload["cells"]
    n: int = len(cells)
    vec_68d: NDArray[np.float64] = np.array(
        [c["vector_68d"] for c in cells],
        dtype=np.float64,
    )
    dsi: NDArray[np.float64] = np.array([c["dsi"] for c in cells], dtype=np.float64)
    pd_rate: NDArray[np.float64] = np.array([c["pd_rate_hz"] for c in cells], dtype=np.float64)
    assert vec_68d.shape == (n, 68)
    return vec_68d, dsi, pd_rate


def _run_group_tests(
    *,
    matrix: NDArray[np.float64],
    labels: NDArray[np.int64],
    feature_names: tuple[str, ...],
) -> list[ParamGroupTest]:
    n_features: int = matrix.shape[1]
    n_tests: int = n_features
    unique_labels: list[int] = sorted(set(labels.tolist()))
    tests: list[ParamGroupTest] = []
    for j in range(n_features):
        groups: list[NDArray[np.float64]] = [matrix[labels == lab, j] for lab in unique_labels]
        H_stat, p_val = kruskal(*groups)
        means: list[float] = [float(np.mean(g)) for g in groups]
        stds: list[float] = [float(np.std(g, ddof=0)) for g in groups]
        medians: list[float] = [float(np.median(g)) for g in groups]
        tests.append(
            ParamGroupTest(
                parameter=feature_names[j],
                H=float(H_stat),
                p_raw=float(p_val),
                p_bonferroni=min(1.0, float(p_val) * n_tests),
                cluster_means=means,
                cluster_stds=stds,
                cluster_medians=medians,
            )
        )
    return tests


def _plot_pca_by_cluster(
    *,
    pca: PCAResult,
    labels: NDArray[np.int64],
    k: int,
    output_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(7, 6), dpi=CHART_DPI)
    cmap = plt.get_cmap("tab10")
    for cluster_id in sorted(set(labels.tolist())):
        mask: NDArray[np.bool_] = labels == cluster_id
        ax.scatter(
            pca.scores[mask, 0],
            pca.scores[mask, 1],
            s=40,
            color=cmap(cluster_id),
            alpha=0.8,
            edgecolors="black",
            linewidths=0.4,
            label=f"cluster {cluster_id} (n={int(mask.sum())})",
        )
    pc1_pct: float = 100.0 * float(pca.explained_variance_ratio[0])
    pc2_pct: float = 100.0 * float(pca.explained_variance_ratio[1])
    ax.set_xlabel(f"PC1 ({pc1_pct:.1f}% var)")
    ax.set_ylabel(f"PC2 ({pc2_pct:.1f}% var)")
    ax.set_title(f"PCA on 14-d morphology, K-means k={k}")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def _plot_pca_by_dsi_pd(
    *,
    pca: PCAResult,
    dsi: NDArray[np.float64],
    pd_rate: NDArray[np.float64],
    output_path: Path,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 6), dpi=CHART_DPI)
    pc1_pct: float = 100.0 * float(pca.explained_variance_ratio[0])
    pc2_pct: float = 100.0 * float(pca.explained_variance_ratio[1])
    sc_dsi = axes[0].scatter(
        pca.scores[:, 0],
        pca.scores[:, 1],
        c=dsi,
        cmap="viridis",
        s=40,
        edgecolors="black",
        linewidths=0.4,
    )
    plt.colorbar(sc_dsi, ax=axes[0], label="DSI")
    axes[0].set_xlabel(f"PC1 ({pc1_pct:.1f}% var)")
    axes[0].set_ylabel(f"PC2 ({pc2_pct:.1f}% var)")
    axes[0].set_title("Morphology PCA — coloured by DSI")
    axes[0].grid(True, alpha=0.3)

    sc_pd = axes[1].scatter(
        pca.scores[:, 0],
        pca.scores[:, 1],
        c=pd_rate,
        cmap="plasma",
        s=40,
        edgecolors="black",
        linewidths=0.4,
    )
    plt.colorbar(sc_pd, ax=axes[1], label="PD rate (Hz)")
    axes[1].set_xlabel(f"PC1 ({pc1_pct:.1f}% var)")
    axes[1].set_ylabel(f"PC2 ({pc2_pct:.1f}% var)")
    axes[1].set_title("Morphology PCA — coloured by PD rate")
    axes[1].grid(True, alpha=0.3)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def _plot_electrophys_overlays(
    *,
    electrophys_matrix: NDArray[np.float64],
    labels: NDArray[np.int64],
    feature_names: tuple[str, ...],
    overlay_tests: list[ParamGroupTest],
    output_path: Path,
) -> None:
    n_features: int = electrophys_matrix.shape[1]
    n_cols: int = 6
    n_rows: int = (n_features + n_cols - 1) // n_cols
    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(2.4 * n_cols, 2.0 * n_rows),
        dpi=CHART_DPI,
    )
    axes_flat = axes.flatten()
    unique_labels: list[int] = sorted(set(labels.tolist()))
    cmap = plt.get_cmap("tab10")
    for j in range(n_features):
        ax = axes_flat[j]
        data_groups: list[NDArray[np.float64]] = [
            electrophys_matrix[labels == lab, j] for lab in unique_labels
        ]
        bp = ax.boxplot(
            data_groups,
            tick_labels=[str(lab) for lab in unique_labels],
            patch_artist=True,
            widths=0.5,
            showfliers=False,
        )
        for patch, lab in zip(bp["boxes"], unique_labels, strict=True):
            patch.set_facecolor(cmap(lab))
            patch.set_alpha(0.6)
        test = overlay_tests[j]
        sig: str = "**" if test.p_bonferroni < 0.05 else ""
        ax.set_title(
            f"{feature_names[j]}\np_bonf={test.p_bonferroni:.2g}{sig}",
            fontsize=7,
        )
        ax.tick_params(axis="both", which="major", labelsize=7)
        ax.grid(True, alpha=0.3)
    for j in range(n_features, len(axes_flat)):
        axes_flat[j].set_visible(False)
    fig.suptitle(
        "Electrophys distributions overlaid on morphology K-means clusters",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def main() -> None:
    vec_68d, dsi, pd_rate = _load_cells(path=FILTERED_CELLS_JSON)
    electrophys: NDArray[np.float64] = vec_68d[:, :N_ELECTROPHYS_DIMS]
    morphology: NDArray[np.float64] = vec_68d[:, N_ELECTROPHYS_DIMS:]
    assert electrophys.shape[1] == N_ELECTROPHYS_DIMS
    assert morphology.shape[1] == N_MORPHOLOGY_DIMS

    z_morphology, means_m, stds_m = zscore_matrix(matrix=morphology)
    pca = run_pca(
        matrix_zscored=z_morphology,
        n_components=3,
        feature_means=means_m,
        feature_stds=stds_m,
    )
    sweep: KMeansSweepResult = run_kmeans_sweep(matrix_zscored=z_morphology)
    labels: NDArray[np.int64] = sweep.headline_labels
    cluster_sizes: list[int] = [int((labels == c).sum()) for c in sorted(set(labels.tolist()))]
    top_loadings: list[list[tuple[str, float]]] = [
        top_k_loadings(component=pca.components[i], feature_names=MORPHOLOGY_PARAM_NAMES, k=5)
        for i in range(pca.components.shape[0])
    ]

    overlay_tests: list[ParamGroupTest] = _run_group_tests(
        matrix=electrophys,
        labels=labels,
        feature_names=ELECTROPHYS_PARAM_NAMES,
    )

    payload: dict[str, object] = {
        "n_cells": int(morphology.shape[0]),
        "headline_k": sweep.headline_k,
        "headline_silhouette": sweep.headline_silhouette,
        "cluster_sizes": cluster_sizes,
        "sweep": [
            {"k": r.k, "inertia": r.inertia, "silhouette": r.silhouette} for r in sweep.sweep
        ],
        "pca_explained_variance_ratio": [float(x) for x in pca.explained_variance_ratio],
        "pca_top_loadings": [
            [{"parameter": name, "loading": val} for name, val in row] for row in top_loadings
        ],
        "cluster_labels": [int(x) for x in labels.tolist()],
        "pc_scores": pca.scores.tolist(),
        "overlay_tests": [asdict(t) for t in overlay_tests],
    }
    write_json(payload=payload, path=MORPHOLOGY_CLUSTERS_JSON)

    _plot_pca_by_cluster(
        pca=pca,
        labels=labels,
        k=sweep.headline_k,
        output_path=PCA_MORPHOLOGY_BY_CLUSTER_PNG,
    )
    _plot_pca_by_dsi_pd(
        pca=pca,
        dsi=dsi,
        pd_rate=pd_rate,
        output_path=PCA_MORPHOLOGY_BY_DSI_PD_PNG,
    )
    _plot_electrophys_overlays(
        electrophys_matrix=electrophys,
        labels=labels,
        feature_names=ELECTROPHYS_PARAM_NAMES,
        overlay_tests=overlay_tests,
        output_path=ELECTROPHYS_OVERLAY_PNG,
    )

    print(f"N cells: {int(morphology.shape[0])}")
    print(f"Headline k: {sweep.headline_k}, silhouette: {sweep.headline_silhouette:.3f}")
    print(f"Cluster sizes: {cluster_sizes}")
    print(f"Sweep: {payload['sweep']}")
    print(f"PCA var ratios PC1..3: {payload['pca_explained_variance_ratio']}")
    print("Significant electrophys parameters (Bonferroni p < 0.05):")
    for t in overlay_tests:
        if t.p_bonferroni < 0.05:
            print(f"  {t.parameter}: H={t.H:.2f}, p_bonf={t.p_bonferroni:.3g}")


if __name__ == "__main__":
    main()
