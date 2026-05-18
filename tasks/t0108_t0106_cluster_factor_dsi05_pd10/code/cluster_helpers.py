"""Shared cluster + PCA helpers for t0108."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.constants import (
    K_SWEEP,
    KMEANS_RANDOM_STATE,
    N_INIT_KMEANS,
)


@dataclass(frozen=True, slots=True)
class PCAResult:
    components: NDArray[np.float64]
    explained_variance_ratio: NDArray[np.float64]
    scores: NDArray[np.float64]
    feature_means: NDArray[np.float64]
    feature_stds: NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class KMeansResult:
    k: int
    labels: NDArray[np.int64]
    inertia: float
    silhouette: float


@dataclass(frozen=True, slots=True)
class KMeansSweepResult:
    sweep: list[KMeansResult]
    headline_k: int
    headline_labels: NDArray[np.int64]
    headline_silhouette: float


def zscore_matrix(
    matrix: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    means: NDArray[np.float64] = matrix.mean(axis=0)
    stds: NDArray[np.float64] = matrix.std(axis=0, ddof=0)
    stds_safe: NDArray[np.float64] = np.where(stds == 0.0, 1.0, stds)
    z: NDArray[np.float64] = (matrix - means) / stds_safe
    return z, means, stds


def run_pca(
    *,
    matrix_zscored: NDArray[np.float64],
    n_components: int,
    feature_means: NDArray[np.float64],
    feature_stds: NDArray[np.float64],
) -> PCAResult:
    pca = PCA(n_components=n_components, random_state=KMEANS_RANDOM_STATE)
    scores: NDArray[np.float64] = pca.fit_transform(matrix_zscored)
    return PCAResult(
        components=pca.components_.astype(np.float64),
        explained_variance_ratio=pca.explained_variance_ratio_.astype(np.float64),
        scores=scores.astype(np.float64),
        feature_means=feature_means,
        feature_stds=feature_stds,
    )


def run_kmeans_sweep(*, matrix_zscored: NDArray[np.float64]) -> KMeansSweepResult:
    sweep: list[KMeansResult] = []
    for k in K_SWEEP:
        kmeans = KMeans(
            n_clusters=k,
            random_state=KMEANS_RANDOM_STATE,
            n_init=N_INIT_KMEANS,
        )
        labels: NDArray[np.int64] = kmeans.fit_predict(matrix_zscored).astype(np.int64)
        silhouette: float = float(silhouette_score(matrix_zscored, labels))
        sweep.append(
            KMeansResult(
                k=k,
                labels=labels,
                inertia=float(kmeans.inertia_),
                silhouette=silhouette,
            )
        )
    best: KMeansResult = max(sweep, key=lambda r: r.silhouette)
    return KMeansSweepResult(
        sweep=sweep,
        headline_k=best.k,
        headline_labels=best.labels,
        headline_silhouette=best.silhouette,
    )


def top_k_loadings(
    *,
    component: NDArray[np.float64],
    feature_names: tuple[str, ...],
    k: int = 5,
) -> list[tuple[str, float]]:
    """Return top-k features ranked by absolute loading magnitude, signed values preserved."""
    abs_loadings: NDArray[np.float64] = np.abs(component)
    top_indices: list[int] = list(np.argsort(abs_loadings)[::-1][:k])
    return [(feature_names[i], float(component[i])) for i in top_indices]


def write_json(*, payload: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=_default_encode), encoding="utf-8")


def _default_encode(obj: object) -> object:
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    raise TypeError(f"non-serialisable: {type(obj).__name__}")
