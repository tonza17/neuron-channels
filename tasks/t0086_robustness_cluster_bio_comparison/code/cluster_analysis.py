"""Phase B: cluster Genuine cells in 54-d parameter space.

* k-means k=2..6 with random_state=42 and n_init="auto"; compute silhouette + BIC.
* hierarchical clustering with cosine + euclidean metrics, average linkage.
* 50-sample bootstrap stability ARI vs full-sample labels.
* Per-cluster centroids in normalised + unnormalised space.
* Within / between cluster variance.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    LOWER_BOUNDS,
    N_PARAMS,
    UPPER_BOUNDS,
)
from tasks.t0086_robustness_cluster_bio_comparison.code.paths import (
    CELL_CLASSIFICATION_JSON,
    CLUSTER_CENTROIDS_JSON,
    CLUSTERING_RESULTS_JSON,
    SELECTED_CELLS_JSON,
    ensure_directories,
)

K_MIN: int = 2
K_MAX: int = 6
RANDOM_STATE: int = 42
N_BOOTSTRAP: int = 50
BOOTSTRAP_SUBSAMPLE_FRAC: float = 0.8


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
    """Heuristic BIC for k-means: lower is better.

    BIC = -2 * log_lik + p * log(N), where log_lik approximated under
    spherical Gaussians per cluster.
    """
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
    p = k * d + k - 1  # centroids + cluster sizes - 1
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


def _hierarchical_labels(*, points: NDArray[np.float64], k: int, metric: str) -> list[int]:
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


def run_phase_b() -> None:
    ensure_directories()
    selected = json.loads(SELECTED_CELLS_JSON.read_text(encoding="utf-8"))
    classification_payload = json.loads(CELL_CLASSIFICATION_JSON.read_text(encoding="utf-8"))
    selection_by_cell = {
        int(c["cell_index"]): c for c in selected["joint_pass_cells"] + selected["near_pass_cells"]
    }
    genuine_cells = [c for c in classification_payload["cells"] if c["classification"] == "Genuine"]
    if len(genuine_cells) < K_MIN:
        print(
            f"[cluster_analysis] only {len(genuine_cells)} Genuine cells; "
            f"clustering not meaningful (need >= {K_MIN}). Writing empty results.",
            flush=True,
        )
        CLUSTERING_RESULTS_JSON.write_text(
            json.dumps(
                {
                    "n_genuine_cells": len(genuine_cells),
                    "kmeans": [],
                    "hierarchical_cosine_labels": [],
                    "hierarchical_euclidean_labels": [],
                    "bootstrap_ari": {"mean": 0.0, "sd": 0.0, "n_bootstrap": 0},
                    "best_k": None,
                    "note": "insufficient Genuine cells for clustering",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        CLUSTER_CENTROIDS_JSON.write_text(
            json.dumps({"n_clusters": 0, "centroids": []}, indent=2),
            encoding="utf-8",
        )
        return

    # Build the params matrix in the order of cell_ids.
    cell_ids: list[int] = sorted(int(c["cell_id"]) for c in genuine_cells)
    params_matrix = np.array(
        [list(selection_by_cell[cell_id]["params"]) for cell_id in cell_ids],
        dtype=np.float64,
    )
    assert params_matrix.shape == (len(cell_ids), N_PARAMS), (
        f"params_matrix shape {params_matrix.shape} != ({len(cell_ids)}, {N_PARAMS})"
    )

    normalised = _normalise(params_matrix=params_matrix)

    # k-means k=2..6.
    kmeans_results = [
        _kmeans_eval(points=normalised, k=k) for k in range(K_MIN, K_MAX + 1) if k <= len(cell_ids)
    ]
    best_k = _select_best_k(evals=kmeans_results)

    # Hierarchical clustering at best_k.
    hierarchical_cosine = _hierarchical_labels(points=normalised, k=best_k, metric="cosine")
    hierarchical_euclidean = _hierarchical_labels(points=normalised, k=best_k, metric="euclidean")

    # Best k-means labels.
    best_eval = next((e for e in kmeans_results if e.k == best_k), None)
    if best_eval is None or len(best_eval.labels) == 0:
        kmeans_labels: NDArray[np.int64] = np.zeros(len(cell_ids), dtype=np.int64)
    else:
        kmeans_labels = np.asarray(best_eval.labels, dtype=np.int64)

    # Bootstrap stability ARI.
    bootstrap = _bootstrap_ari(
        points=normalised,
        full_labels=kmeans_labels,
        k=best_k,
        n_bootstrap=N_BOOTSTRAP,
        subsample_frac=BOOTSTRAP_SUBSAMPLE_FRAC,
    )

    # Cross-method ARI.
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

    # Centroids.
    centroids: list[ClusterCentroidEntry] = []
    for cluster_id in range(best_k):
        mask = kmeans_labels == cluster_id
        members = [int(cell_ids[i]) for i in np.where(mask)[0]]
        if mask.sum() == 0:
            continue
        centroid_norm = normalised[mask].mean(axis=0)
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

    # Between-cluster distance matrix (normalised).
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

    out_clustering: dict[str, object] = {
        "n_genuine_cells": len(cell_ids),
        "cell_ids": cell_ids,
        "k_min": K_MIN,
        "k_max": K_MAX,
        "best_k": best_k,
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
    CLUSTERING_RESULTS_JSON.write_text(json.dumps(out_clustering, indent=2), encoding="utf-8")

    out_centroids: dict[str, object] = {
        "n_clusters": len(centroids),
        "best_k": best_k,
        "between_cluster_distance_matrix": between_distances,
        "centroids": [asdict(c) for c in centroids],
    }
    CLUSTER_CENTROIDS_JSON.write_text(json.dumps(out_centroids, indent=2), encoding="utf-8")
    print(
        f"[cluster_analysis] k_min={K_MIN} k_max={K_MAX} best_k={best_k} "
        f"silhouette[best]={best_eval.silhouette if best_eval else None} "
        f"bootstrap_ari_mean={bootstrap['mean']:.3f} "
        f"n_genuine={len(cell_ids)}",
        flush=True,
    )


def main() -> None:
    run_phase_b()


if __name__ == "__main__":
    main()
