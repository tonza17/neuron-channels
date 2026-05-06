"""Phase A driver: load 13-cell pool, re-cluster, write centroids + reps.

Combines the loader, clustering core (adapted from t0086 cluster_analysis.py
with input changed from Genuine-only to Genuine + Marginal pool), and
representative selection (closest cell to centroid in 54-d Euclidean
distance). Output JSONs:
* ``recluster_assignments.json`` - per-cell cluster assignment + clustering
  metadata.
* ``recluster_centroids.json`` - per-cluster centroids + within-cluster
  variance + between-cluster distance matrix.
* ``representative_cells.json`` - one representative cell per cluster.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.spatial.distance import pdist
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    LOWER_BOUNDS,
    N_PARAMS,
    UPPER_BOUNDS,
)
from tasks.t0088_recluster_marginals_and_vm_motifs.code.constants import (
    BOOTSTRAP_SUBSAMPLE_FRAC,
    K_MAX,
    K_MIN,
    N_BOOTSTRAP,
    RANDOM_STATE,
    TARGET_CELL_IDS,
)
from tasks.t0088_recluster_marginals_and_vm_motifs.code.paths import (
    CLUSTER_DENDROGRAM_PNG,
    CLUSTER_PCA_PNG,
    CLUSTER_SILHOUETTE_PNG,
    CLUSTER_UMAP_PNG,
    RECLUSTER_ASSIGNMENTS_JSON,
    RECLUSTER_CENTROIDS_JSON,
    REPRESENTATIVE_CELLS_JSON,
    T0083_ALL_EVALUATIONS_JSON,
    T0086_CELL_CLASSIFICATION_JSON,
    ensure_directories,
)


@dataclass(frozen=True, slots=True)
class CellEntry:
    cell_id: int
    classification: str
    params: list[float]


@dataclass(frozen=True, slots=True)
class KMeansEval:
    k: int
    silhouette: float | None
    bic: float | None
    inertia: float
    labels: list[int]


@dataclass(frozen=True, slots=True)
class ClusterCentroidEntry:
    cluster_id: int
    n_cells: int
    cell_ids: list[int]
    centroid_normalised: list[float]
    centroid_unnormalised: list[float]
    within_cluster_variance: float


def _load_cell_entries() -> list[CellEntry]:
    """Load the 13 target cells with classification + 54-d parameter vector.

    Loads classifications from t0086 cell_classification.json and parameter
    vectors from t0083 all_evaluations.json. Asserts all 13 cells found.
    """
    classification_payload = json.loads(T0086_CELL_CLASSIFICATION_JSON.read_text(encoding="utf-8"))
    classifications: dict[int, str] = {
        int(c["cell_id"]): str(c["classification"]) for c in classification_payload["cells"]
    }
    raw_evals: list[dict[str, Any]] = json.loads(
        T0083_ALL_EVALUATIONS_JSON.read_text(encoding="utf-8")
    )
    params_by_cell: dict[int, list[float]] = {}
    for record in raw_evals:
        cid: int = int(record["cell_index"])
        if cid in TARGET_CELL_IDS:
            params_by_cell.setdefault(cid, list(record["params"]))

    entries: list[CellEntry] = []
    missing: list[int] = []
    for cid in TARGET_CELL_IDS:
        if cid not in params_by_cell:
            missing.append(cid)
            continue
        if cid not in classifications:
            missing.append(cid)
            continue
        entries.append(
            CellEntry(
                cell_id=cid,
                classification=classifications[cid],
                params=params_by_cell[cid],
            )
        )
    assert len(missing) == 0, f"Missing cells in t0083 / t0086 inputs: {missing}"
    assert len(entries) == 13, f"Expected 13 entries, got {len(entries)}"
    return entries


def _normalise(*, params_matrix: NDArray[np.float64]) -> NDArray[np.float64]:
    """Min-max normalise per parameter using LOWER/UPPER bounds."""
    lower = np.asarray(LOWER_BOUNDS, dtype=np.float64)
    upper = np.asarray(UPPER_BOUNDS, dtype=np.float64)
    span = upper - lower
    span[span == 0] = 1.0
    return (params_matrix - lower) / span


def _unnormalise_vector(*, vec: NDArray[np.float64]) -> NDArray[np.float64]:
    lower = np.asarray(LOWER_BOUNDS, dtype=np.float64)
    upper = np.asarray(UPPER_BOUNDS, dtype=np.float64)
    span = upper - lower
    return lower + vec * span


def _bic(*, points: NDArray[np.float64], labels: NDArray[np.int64]) -> float:
    n, d = points.shape
    k = int(labels.max() + 1) if labels.size > 0 else 1
    if k <= 0 or n <= k:
        return float("inf")
    sigma2 = 0.0
    for cl in range(k):
        mask = labels == cl
        if mask.sum() == 0:
            continue
        cluster_points = points[mask]
        centroid = cluster_points.mean(axis=0)
        sigma2 += float(((cluster_points - centroid) ** 2).sum())
    sigma2 /= max(n - k, 1) * d
    sigma2 = max(sigma2, 1e-12)
    log_lik = -0.5 * n * d * np.log(2 * np.pi * sigma2) - 0.5 * (n - k) * d
    p = k * d + k - 1
    return float(-2.0 * log_lik + p * np.log(n))


def _kmeans_eval(*, points: NDArray[np.float64], k: int) -> KMeansEval:
    if len(points) <= k:
        return KMeansEval(k=k, silhouette=None, bic=None, inertia=0.0, labels=[])
    km = KMeans(n_clusters=k, n_init="auto", random_state=RANDOM_STATE)
    km.fit(points)
    labels: NDArray[np.int64] = km.labels_  # type: ignore[assignment]
    silhouette: float | None = None
    if len(np.unique(labels)) >= 2:
        silhouette = float(silhouette_score(points, labels))
    bic_value = _bic(points=points, labels=labels)
    return KMeansEval(
        k=k,
        silhouette=silhouette,
        bic=bic_value,
        inertia=float(km.inertia_),
        labels=[int(x) for x in labels],
    )


def _hierarchical_labels(
    *,
    points: NDArray[np.float64],
    k: int,
    metric: str,
) -> list[int]:
    if len(points) <= k:
        return []
    if metric == "cosine":
        dist = pdist(points, metric="cosine")
    elif metric == "euclidean":
        dist = pdist(points, metric="euclidean")
    else:
        raise ValueError(f"unknown metric {metric}")
    z = linkage(dist, method="average")
    labels = fcluster(z, t=k, criterion="maxclust") - 1
    return [int(x) for x in labels]


def _bootstrap_ari(
    *,
    points: NDArray[np.float64],
    full_labels: NDArray[np.int64],
    k: int,
    n_bootstrap: int,
    subsample_frac: float,
) -> dict[str, float]:
    n = len(points)
    if n <= k or n < 4:
        return {"mean": 0.0, "sd": 0.0, "n_bootstrap": 0}
    rng = np.random.default_rng(RANDOM_STATE)
    sample_size = max(k + 1, int(n * subsample_frac))
    aris: list[float] = []
    for _ in range(n_bootstrap):
        idx = rng.choice(n, size=sample_size, replace=False)
        sub = points[idx]
        if len(np.unique(full_labels[idx])) < 2:
            continue
        try:
            km = KMeans(n_clusters=k, n_init="auto", random_state=RANDOM_STATE)
            sub_labels = km.fit_predict(sub)
        except (ValueError, ArithmeticError):
            continue
        ari = adjusted_rand_score(full_labels[idx], sub_labels)
        aris.append(float(ari))
    if len(aris) == 0:
        return {"mean": 0.0, "sd": 0.0, "n_bootstrap": 0}
    arr = np.asarray(aris)
    return {
        "mean": float(arr.mean()),
        "sd": float(arr.std(ddof=0)),
        "n_bootstrap": int(len(aris)),
    }


def _select_best_k(*, evals: list[KMeansEval]) -> int:
    valid = [e for e in evals if e.silhouette is not None]
    if len(valid) == 0:
        return K_MIN
    best = max(valid, key=lambda e: e.silhouette or float("-inf"))
    return best.k


def _within_cluster_variance(
    *,
    points: NDArray[np.float64],
    labels: NDArray[np.int64],
    cluster_id: int,
) -> float:
    mask = labels == cluster_id
    if mask.sum() <= 1:
        return 0.0
    cluster_points = points[mask]
    centroid = cluster_points.mean(axis=0)
    return float(((cluster_points - centroid) ** 2).sum(axis=1).mean())


def _plot_silhouette(*, evals: list[KMeansEval]) -> None:
    ks = [e.k for e in evals if e.silhouette is not None]
    sils = [float(e.silhouette) for e in evals if e.silhouette is not None]
    if len(ks) == 0:
        return
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(ks, sils, "o-", label="silhouette")
    ax.set_xlabel("k")
    ax.set_ylabel("silhouette score")
    ax.set_title("Silhouette score vs k")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(CLUSTER_SILHOUETTE_PNG, dpi=200)
    plt.close(fig)
    print(f"[select_representatives] wrote {CLUSTER_SILHOUETTE_PNG}")


def _plot_dendrogram(*, points: NDArray[np.float64], cell_ids: list[int]) -> None:
    if len(points) < 2:
        return
    z = linkage(pdist(points, metric="euclidean"), method="average")
    fig, ax = plt.subplots(figsize=(10, 5))
    dendrogram(z, ax=ax, labels=[str(c) for c in cell_ids])
    ax.set_xlabel("cell ID")
    ax.set_ylabel("distance (euclidean)")
    ax.set_title("Hierarchical clustering dendrogram (average linkage, euclidean)")
    fig.tight_layout()
    fig.savefig(CLUSTER_DENDROGRAM_PNG, dpi=200)
    plt.close(fig)
    print(f"[select_representatives] wrote {CLUSTER_DENDROGRAM_PNG}")


def _plot_2d_scatter(
    *,
    points: NDArray[np.float64],
    labels: NDArray[np.int64],
    cell_ids: list[int],
    classifications: list[str],
) -> None:
    """Try UMAP first; fall back to PCA(n=2) on failure or if umap missing."""
    coords: NDArray[np.float64]
    method: str
    try:
        # umap-learn is not in the project's dependencies; use PCA fallback.
        # Importing umap inside the try/except keeps this self-contained.
        import umap  # type: ignore[import-not-found]

        reducer = umap.UMAP(  # type: ignore[attr-defined]
            n_neighbors=min(5, len(points) - 1),
            n_components=2,
            random_state=RANDOM_STATE,
        )
        coords = reducer.fit_transform(points)
        method = "umap"
    except (ImportError, RuntimeError, ValueError):
        pca = PCA(n_components=2, random_state=RANDOM_STATE)
        coords = pca.fit_transform(points)
        method = "pca"

    fig, ax = plt.subplots(figsize=(8, 6))
    cmap = plt.get_cmap("tab10")
    for cl in sorted(set(int(label) for label in labels)):
        mask = labels == cl
        ax.scatter(
            coords[mask, 0],
            coords[mask, 1],
            color=cmap(cl % 10),
            label=f"cluster {cl}",
            s=80,
            edgecolor="black",
        )
    for i, cid in enumerate(cell_ids):
        marker_text = f"{cid}\n({classifications[i][0]})"
        ax.annotate(
            marker_text,
            xy=(coords[i, 0], coords[i, 1]),
            xytext=(3, 3),
            textcoords="offset points",
            fontsize=7,
        )
    ax.set_xlabel(f"{method.upper()}-1")
    ax.set_ylabel(f"{method.upper()}-2")
    ax.set_title(f"13-cell re-cluster ({method.upper()} 2D); G = Genuine, M = Marginal")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out_path = CLUSTER_UMAP_PNG if method == "umap" else CLUSTER_PCA_PNG
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"[select_representatives] wrote {out_path}")


def _select_representative(
    *,
    cluster_id: int,
    points_normalised: NDArray[np.float64],
    labels: NDArray[np.int64],
    cell_ids: list[int],
    centroid_norm: NDArray[np.float64],
) -> tuple[int, float]:
    """Cell with min Euclidean distance to centroid (deterministic tiebreak)."""
    mask = labels == cluster_id
    cluster_indices = [i for i, m in enumerate(mask) if m]
    if len(cluster_indices) == 0:
        return -1, float("nan")
    distances: list[tuple[float, int, int]] = []
    for i in cluster_indices:
        d = float(np.linalg.norm(points_normalised[i] - centroid_norm))
        distances.append((d, cell_ids[i], i))
    # Sort by (distance, cell_id) for deterministic tie-breaking.
    distances.sort(key=lambda x: (x[0], x[1]))
    best_distance, best_cell, _ = distances[0]
    return best_cell, best_distance


def run_phase_a() -> None:
    ensure_directories()
    print("[select_representatives] Phase A: re-cluster 13 cells", flush=True)
    entries = _load_cell_entries()
    cell_ids: list[int] = [e.cell_id for e in entries]
    classifications: list[str] = [e.classification for e in entries]
    params_matrix = np.array([e.params for e in entries], dtype=np.float64)
    assert params_matrix.shape == (13, N_PARAMS), (
        f"params_matrix shape {params_matrix.shape} != (13, {N_PARAMS})"
    )
    normalised = _normalise(params_matrix=params_matrix)

    # k-means k=2..6
    kmeans_results = [
        _kmeans_eval(points=normalised, k=k) for k in range(K_MIN, K_MAX + 1) if k <= len(cell_ids)
    ]
    best_k = _select_best_k(evals=kmeans_results)
    print(f"[select_representatives] best_k = {best_k}", flush=True)

    # Hierarchical clustering at best_k
    hierarchical_cosine = _hierarchical_labels(points=normalised, k=best_k, metric="cosine")
    hierarchical_euclidean = _hierarchical_labels(points=normalised, k=best_k, metric="euclidean")

    # Best k-means labels
    best_eval = next((e for e in kmeans_results if e.k == best_k), None)
    if best_eval is None or len(best_eval.labels) == 0:
        kmeans_labels: NDArray[np.int64] = np.zeros(len(cell_ids), dtype=np.int64)
    else:
        kmeans_labels = np.asarray(best_eval.labels, dtype=np.int64)

    # Bootstrap stability ARI
    bootstrap = _bootstrap_ari(
        points=normalised,
        full_labels=kmeans_labels,
        k=best_k,
        n_bootstrap=N_BOOTSTRAP,
        subsample_frac=BOOTSTRAP_SUBSAMPLE_FRAC,
    )

    # Cross-method ARI
    ari_cosine = (
        float(adjusted_rand_score(kmeans_labels, np.asarray(hierarchical_cosine)))
        if len(hierarchical_cosine) == len(kmeans_labels)
        else None
    )
    ari_euclidean = (
        float(adjusted_rand_score(kmeans_labels, np.asarray(hierarchical_euclidean)))
        if len(hierarchical_euclidean) == len(kmeans_labels)
        else None
    )

    # Centroids
    centroids: list[ClusterCentroidEntry] = []
    centroid_norm_by_cluster: dict[int, NDArray[np.float64]] = {}
    for cluster_id in range(best_k):
        mask = kmeans_labels == cluster_id
        members = [int(cell_ids[i]) for i in np.where(mask)[0]]
        if mask.sum() == 0:
            continue
        centroid_norm = normalised[mask].mean(axis=0)
        centroid_norm_by_cluster[cluster_id] = centroid_norm
        centroid_unnorm = _unnormalise_vector(vec=centroid_norm)
        within_var = _within_cluster_variance(
            points=normalised, labels=kmeans_labels, cluster_id=cluster_id
        )
        centroids.append(
            ClusterCentroidEntry(
                cluster_id=cluster_id,
                n_cells=int(mask.sum()),
                cell_ids=members,
                centroid_normalised=[float(v) for v in centroid_norm],
                centroid_unnormalised=[float(v) for v in centroid_unnorm],
                within_cluster_variance=within_var,
            )
        )

    # Between-cluster distance matrix (normalised)
    between_distances: list[list[float]] = []
    for ci in centroids:
        row: list[float] = []
        for cj in centroids:
            d = float(
                np.linalg.norm(
                    np.asarray(ci.centroid_normalised) - np.asarray(cj.centroid_normalised)
                )
            )
            row.append(d)
        between_distances.append(row)

    # Plots
    _plot_silhouette(evals=kmeans_results)
    _plot_dendrogram(points=normalised, cell_ids=cell_ids)
    _plot_2d_scatter(
        points=normalised,
        labels=kmeans_labels,
        cell_ids=cell_ids,
        classifications=classifications,
    )

    # Representatives
    representatives: list[dict[str, object]] = []
    for centroid in centroids:
        cluster_id = centroid.cluster_id
        rep_cell, rep_dist = _select_representative(
            cluster_id=cluster_id,
            points_normalised=normalised,
            labels=kmeans_labels,
            cell_ids=cell_ids,
            centroid_norm=centroid_norm_by_cluster[cluster_id],
        )
        representatives.append(
            {
                "cluster_id": cluster_id,
                "representative_cell_id": int(rep_cell),
                "distance_to_centroid_normalised": rep_dist,
                "n_cells_in_cluster": centroid.n_cells,
                "all_cell_ids_in_cluster": list(centroid.cell_ids),
            }
        )
        print(
            f"[select_representatives] cluster {cluster_id}: representative cell "
            f"{rep_cell} (distance {rep_dist:.4f})",
            flush=True,
        )

    # Output JSONs
    out_assignments: dict[str, object] = {
        "n_cells": len(cell_ids),
        "cell_ids": cell_ids,
        "classifications": classifications,
        "k_min": K_MIN,
        "k_max": K_MAX,
        "best_k": best_k,
        "kmeans_labels_at_best_k": [int(x) for x in kmeans_labels.tolist()],
        "kmeans": [
            {
                "k": e.k,
                "silhouette": e.silhouette,
                "bic": e.bic,
                "inertia": e.inertia,
                "labels": e.labels,
            }
            for e in kmeans_results
        ],
        "hierarchical_cosine_labels": hierarchical_cosine,
        "hierarchical_euclidean_labels": hierarchical_euclidean,
        "ari_kmeans_vs_hierarchical_cosine": ari_cosine,
        "ari_kmeans_vs_hierarchical_euclidean": ari_euclidean,
        "bootstrap_ari": bootstrap,
    }
    RECLUSTER_ASSIGNMENTS_JSON.write_text(json.dumps(out_assignments, indent=2), encoding="utf-8")
    print(f"[select_representatives] wrote {RECLUSTER_ASSIGNMENTS_JSON}", flush=True)

    out_centroids: dict[str, object] = {
        "n_clusters": len(centroids),
        "best_k": best_k,
        "between_cluster_distance_matrix": between_distances,
        "centroids": [asdict(c) for c in centroids],
    }
    RECLUSTER_CENTROIDS_JSON.write_text(json.dumps(out_centroids, indent=2), encoding="utf-8")
    print(f"[select_representatives] wrote {RECLUSTER_CENTROIDS_JSON}", flush=True)

    out_reps: dict[str, object] = {
        "n_representatives": len(representatives),
        "best_k": best_k,
        "representatives": representatives,
    }
    REPRESENTATIVE_CELLS_JSON.write_text(json.dumps(out_reps, indent=2), encoding="utf-8")
    print(f"[select_representatives] wrote {REPRESENTATIVE_CELLS_JSON}", flush=True)


def main() -> None:
    run_phase_a()


if __name__ == "__main__":
    main()
