"""Phase B plot generation: UMAP, silhouette curve, dendrogram, classification bar.

Outputs:
* results/images/cluster_umap.png
* results/images/cluster_silhouette.png
* results/images/cluster_dendrogram.png
* results/images/robustness_classification.png
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    LOWER_BOUNDS,
    UPPER_BOUNDS,
)
from tasks.t0086_robustness_cluster_bio_comparison.code.paths import (
    CELL_CLASSIFICATION_JSON,
    CLUSTERING_RESULTS_JSON,
    RESULTS_IMAGES_DIR,
    SELECTED_CELLS_JSON,
    ensure_directories,
)

UMAP_PNG: Path = RESULTS_IMAGES_DIR / "cluster_umap.png"
SILHOUETTE_PNG: Path = RESULTS_IMAGES_DIR / "cluster_silhouette.png"
DENDROGRAM_PNG: Path = RESULTS_IMAGES_DIR / "cluster_dendrogram.png"
CLASSIFICATION_PNG: Path = RESULTS_IMAGES_DIR / "robustness_classification.png"


def _normalise_matrix(*, mat: np.ndarray) -> np.ndarray:
    lower = np.asarray(LOWER_BOUNDS, dtype=np.float64)
    upper = np.asarray(UPPER_BOUNDS, dtype=np.float64)
    span = upper - lower
    span[span == 0] = 1.0
    return (mat - lower) / span


def plot_classification_bar() -> None:
    payload = json.loads(CELL_CLASSIFICATION_JSON.read_text(encoding="utf-8"))
    summary = payload["summary"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    categories = ["Genuine", "Marginal", "Stochastic"]
    counts = [int(summary[c]) for c in categories]
    colors = ["#1b9e77", "#d95f02", "#7570b3"]
    bars = ax.bar(categories, counts, color=colors)
    ax.set_ylabel("Number of cells (out of 20)")
    ax.set_title("Phase A robustness classification (5/5 reps = Genuine)")
    for bar, c in zip(bars, counts, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.2,
            f"{c}",
            ha="center",
            fontsize=12,
            fontweight="bold",
        )
    ax.set_ylim(0, max(20, max(counts) + 2))
    fig.tight_layout()
    fig.savefig(CLASSIFICATION_PNG, dpi=200)
    plt.close(fig)
    print(f"[plot_phase_b] wrote {CLASSIFICATION_PNG}")


def plot_silhouette() -> None:
    payload = json.loads(CLUSTERING_RESULTS_JSON.read_text(encoding="utf-8"))
    kmeans = payload["kmeans"]
    if len(kmeans) == 0:
        print("[plot_phase_b] no k-means results; skipping silhouette plot")
        return
    ks = [int(e["k"]) for e in kmeans]
    sils = [float(e["silhouette"]) if e["silhouette"] is not None else float("nan") for e in kmeans]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(ks, sils, "-o", color="#1b9e77", linewidth=2)
    best_k = payload.get("best_k")
    if best_k is not None:
        ax.axvline(int(best_k), color="red", linestyle="--", label=f"best_k={best_k}")
        ax.legend()
    ax.set_xlabel("k (number of clusters)")
    ax.set_ylabel("Silhouette score")
    ax.set_title("k-means silhouette score vs k (Genuine cells)")
    ax.set_xticks(ks)
    fig.tight_layout()
    fig.savefig(SILHOUETTE_PNG, dpi=200)
    plt.close(fig)
    print(f"[plot_phase_b] wrote {SILHOUETTE_PNG}")


def plot_dendrogram() -> None:
    payload = json.loads(CLUSTERING_RESULTS_JSON.read_text(encoding="utf-8"))
    cell_ids = payload.get("cell_ids", [])
    if len(cell_ids) < 2:
        print("[plot_phase_b] insufficient Genuine cells; skipping dendrogram")
        return
    selected = json.loads(SELECTED_CELLS_JSON.read_text(encoding="utf-8"))
    selection_by_cell = {
        int(c["cell_index"]): c for c in selected["joint_pass_cells"] + selected["near_pass_cells"]
    }
    params_matrix = np.array(
        [list(selection_by_cell[cid]["params"]) for cid in cell_ids],
        dtype=np.float64,
    )
    normalised = _normalise_matrix(mat=params_matrix)
    z = linkage(pdist(normalised, metric="euclidean"), method="average")
    fig, ax = plt.subplots(figsize=(10, 5))
    dendrogram(z, labels=[str(cid) for cid in cell_ids], ax=ax, leaf_font_size=10)
    ax.set_title("Hierarchical clustering of Genuine cells (euclidean + average linkage)")
    ax.set_ylabel("Distance")
    fig.tight_layout()
    fig.savefig(DENDROGRAM_PNG, dpi=200)
    plt.close(fig)
    print(f"[plot_phase_b] wrote {DENDROGRAM_PNG}")


def plot_umap() -> None:
    payload = json.loads(CLUSTERING_RESULTS_JSON.read_text(encoding="utf-8"))
    cell_ids = payload.get("cell_ids", [])
    best_k = payload.get("best_k")
    kmeans = payload.get("kmeans", [])
    if len(cell_ids) < 3 or best_k is None:
        print("[plot_phase_b] insufficient Genuine cells for UMAP; skipping")
        return
    best = next((e for e in kmeans if int(e["k"]) == int(best_k)), None)
    if best is None:
        return
    labels = np.asarray(best["labels"], dtype=np.int64)
    selected = json.loads(SELECTED_CELLS_JSON.read_text(encoding="utf-8"))
    selection_by_cell = {
        int(c["cell_index"]): c for c in selected["joint_pass_cells"] + selected["near_pass_cells"]
    }
    params_matrix = np.array(
        [list(selection_by_cell[cid]["params"]) for cid in cell_ids],
        dtype=np.float64,
    )
    normalised = _normalise_matrix(mat=params_matrix)
    try:
        import umap

        reducer = umap.UMAP(
            n_components=2,
            n_neighbors=min(5, len(cell_ids) - 1),
            min_dist=0.3,
            random_state=42,
        )
        embedding = reducer.fit_transform(normalised)
    except (ImportError, ValueError) as exc:
        print(f"[plot_phase_b] umap-learn unavailable ({exc}); falling back to PCA")
        from sklearn.decomposition import PCA

        embedding = PCA(n_components=2, random_state=42).fit_transform(normalised)

    fig, ax = plt.subplots(figsize=(8, 6))
    palette = plt.cm.tab10(np.linspace(0, 1, max(int(best_k), 1)))
    for cluster_id in range(int(best_k)):
        mask = labels == cluster_id
        if mask.sum() == 0:
            continue
        ax.scatter(
            embedding[mask, 0],
            embedding[mask, 1],
            s=80,
            color=palette[cluster_id % len(palette)],
            label=f"Cluster {cluster_id} (n={mask.sum()})",
            edgecolor="black",
            linewidth=0.5,
        )
    for i, cid in enumerate(cell_ids):
        ax.annotate(
            str(cid),
            (embedding[i, 0], embedding[i, 1]),
            fontsize=8,
            xytext=(3, 3),
            textcoords="offset points",
        )
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("UMAP 2")
    ax.set_title("UMAP embedding of Genuine cells (54-d -> 2-d)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(UMAP_PNG, dpi=200)
    plt.close(fig)
    print(f"[plot_phase_b] wrote {UMAP_PNG}")


def main() -> None:
    ensure_directories()
    plot_classification_bar()
    plot_silhouette()
    plot_dendrogram()
    plot_umap()


if __name__ == "__main__":
    main()
