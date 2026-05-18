"""PCA + K-means on the 54-d electrophys submatrix, with 14-d morphology overlays.

Outputs:
  results/data/electrophys_clusters.json
  results/images/pca_electrophys_by_cluster.png
  results/images/pca_electrophys_by_dsi_pd.png
  results/images/morph_overlay_by_electrophys_cluster.png

Usage:
  uv run python -m tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.cluster_electrophys
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
    ELECTROPHYS_CLUSTERS_JSON,
    FILTERED_CELLS_JSON,
    MORPH_OVERLAY_PNG,
    PCA_ELECTROPHYS_BY_CLUSTER_PNG,
    PCA_ELECTROPHYS_BY_DSI_PD_PNG,
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


@dataclass(frozen=True, slots=True)
class ClusterAnalysisOutput:
    n_cells: int
    headline_k: int
    headline_silhouette: float
    cluster_sizes: list[int]
    sweep: list[dict[str, float | int]]
    pca_explained_variance_ratio: list[float]
    pca_top_loadings: list[list[tuple[str, float]]]
    cluster_labels: list[int]
    pc_scores: list[list[float]]
    overlay_tests: list[ParamGroupTest]


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
    ax.set_title(f"PCA on 54-d electrophys, K-means k={k}")
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
    axes[0].set_title("Electrophys PCA — coloured by DSI")
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
    axes[1].set_title("Electrophys PCA — coloured by PD rate")
    axes[1].grid(True, alpha=0.3)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def _plot_morphology_overlays(
    *,
    morph_matrix: NDArray[np.float64],
    labels: NDArray[np.int64],
    feature_names: tuple[str, ...],
    overlay_tests: list[ParamGroupTest],
    output_path: Path,
) -> None:
    n_features: int = morph_matrix.shape[1]
    n_cols: int = 4
    n_rows: int = (n_features + n_cols - 1) // n_cols
    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(4 * n_cols, 3 * n_rows),
        dpi=CHART_DPI,
    )
    axes_flat = axes.flatten() if n_rows > 1 else [axes] if n_features == 1 else list(axes)
    unique_labels: list[int] = sorted(set(labels.tolist()))
    cmap = plt.get_cmap("tab10")
    for j in range(n_features):
        ax = axes_flat[j]
        data_groups: list[NDArray[np.float64]] = [
            morph_matrix[labels == lab, j] for lab in unique_labels
        ]
        bp = ax.boxplot(
            data_groups,
            tick_labels=[str(lab) for lab in unique_labels],
            patch_artist=True,
            widths=0.5,
        )
        for patch, lab in zip(bp["boxes"], unique_labels, strict=True):
            patch.set_facecolor(cmap(lab))
            patch.set_alpha(0.6)
        test = overlay_tests[j]
        sig: str = "**" if test.p_bonferroni < 0.05 else ""
        ax.set_title(
            f"{feature_names[j]}\nH={test.H:.1f}, p_bonf={test.p_bonferroni:.2g}{sig}",
            fontsize=9,
        )
        ax.set_xlabel("cluster")
        ax.grid(True, alpha=0.3)
    for j in range(n_features, len(axes_flat)):
        axes_flat[j].set_visible(False)
    fig.suptitle(
        "Morphology distributions overlaid on electrophys K-means clusters",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def main() -> None:
    vec_68d, dsi, pd_rate = _load_cells(path=FILTERED_CELLS_JSON)
    electrophys: NDArray[np.float64] = vec_68d[:, :N_ELECTROPHYS_DIMS]
    morphology: NDArray[np.float64] = vec_68d[:, N_ELECTROPHYS_DIMS:]
    assert electrophys.shape[1] == N_ELECTROPHYS_DIMS
    assert morphology.shape[1] == N_MORPHOLOGY_DIMS

    z_electrophys, means_e, stds_e = zscore_matrix(matrix=electrophys)
    pca = run_pca(
        matrix_zscored=z_electrophys,
        n_components=3,
        feature_means=means_e,
        feature_stds=stds_e,
    )
    sweep: KMeansSweepResult = run_kmeans_sweep(matrix_zscored=z_electrophys)
    labels: NDArray[np.int64] = sweep.headline_labels
    cluster_sizes: list[int] = [int((labels == c).sum()) for c in sorted(set(labels.tolist()))]
    top_loadings: list[list[tuple[str, float]]] = [
        top_k_loadings(component=pca.components[i], feature_names=ELECTROPHYS_PARAM_NAMES, k=5)
        for i in range(pca.components.shape[0])
    ]

    overlay_tests: list[ParamGroupTest] = _run_group_tests(
        matrix=morphology,
        labels=labels,
        feature_names=MORPHOLOGY_PARAM_NAMES,
    )

    output = ClusterAnalysisOutput(
        n_cells=int(electrophys.shape[0]),
        headline_k=sweep.headline_k,
        headline_silhouette=sweep.headline_silhouette,
        cluster_sizes=cluster_sizes,
        sweep=[
            {
                "k": r.k,
                "inertia": r.inertia,
                "silhouette": r.silhouette,
            }
            for r in sweep.sweep
        ],
        pca_explained_variance_ratio=[float(x) for x in pca.explained_variance_ratio],
        pca_top_loadings=top_loadings,
        cluster_labels=[int(x) for x in labels.tolist()],
        pc_scores=pca.scores.tolist(),
        overlay_tests=overlay_tests,
    )

    payload: dict[str, object] = {
        "n_cells": output.n_cells,
        "headline_k": output.headline_k,
        "headline_silhouette": output.headline_silhouette,
        "cluster_sizes": output.cluster_sizes,
        "sweep": output.sweep,
        "pca_explained_variance_ratio": output.pca_explained_variance_ratio,
        "pca_top_loadings": [
            [{"parameter": name, "loading": val} for name, val in row]
            for row in output.pca_top_loadings
        ],
        "cluster_labels": output.cluster_labels,
        "pc_scores": output.pc_scores,
        "overlay_tests": [asdict(t) for t in output.overlay_tests],
    }
    write_json(payload=payload, path=ELECTROPHYS_CLUSTERS_JSON)

    _plot_pca_by_cluster(
        pca=pca,
        labels=labels,
        k=output.headline_k,
        output_path=PCA_ELECTROPHYS_BY_CLUSTER_PNG,
    )
    _plot_pca_by_dsi_pd(
        pca=pca,
        dsi=dsi,
        pd_rate=pd_rate,
        output_path=PCA_ELECTROPHYS_BY_DSI_PD_PNG,
    )
    _plot_morphology_overlays(
        morph_matrix=morphology,
        labels=labels,
        feature_names=MORPHOLOGY_PARAM_NAMES,
        overlay_tests=overlay_tests,
        output_path=MORPH_OVERLAY_PNG,
    )

    print(f"N cells: {output.n_cells}")
    print(f"Headline k: {output.headline_k}, silhouette: {output.headline_silhouette:.3f}")
    print(f"Cluster sizes: {output.cluster_sizes}")
    print(f"Sweep: {output.sweep}")
    print(f"PCA var ratios PC1..3: {output.pca_explained_variance_ratio}")
    print("Significant morph parameters (Bonferroni p < 0.05):")
    for t in output.overlay_tests:
        if t.p_bonferroni < 0.05:
            print(f"  {t.parameter}: H={t.H:.2f}, p_bonf={t.p_bonferroni:.3g}")


if __name__ == "__main__":
    main()
