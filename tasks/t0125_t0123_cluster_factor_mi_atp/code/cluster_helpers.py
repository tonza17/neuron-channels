"""Shared cluster + PCA helpers (copied from t0117, namespace updated)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

from tasks.t0125_t0123_cluster_factor_mi_atp.code.constants import (
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


@dataclass(frozen=True, slots=True)
class PooledStandardiser:
    """Z-score standardiser fitted ONCE on the union pool; reused everywhere."""

    mean: NDArray[np.float64]
    std: NDArray[np.float64]

    def transform(self, matrix: NDArray[np.float64]) -> NDArray[np.float64]:
        assert matrix.shape[1] == self.mean.shape[0], (
            f"matrix has {matrix.shape[1]} cols but standardiser expects {self.mean.shape[0]}"
        )
        return (matrix - self.mean) / self.std


def fit_pooled_standardiser(matrix: NDArray[np.float64]) -> PooledStandardiser:
    """Fit a z-score standardiser on the union pool 68-d matrix.

    Zero-std columns (constant features) are clipped to 1.0 to avoid division-by-zero. The fitted
    mean / std are saved alongside the data so every downstream step reuses the same fit.
    """
    means: NDArray[np.float64] = matrix.mean(axis=0)
    stds_raw: NDArray[np.float64] = matrix.std(axis=0, ddof=0)
    stds_safe: NDArray[np.float64] = np.where(stds_raw == 0.0, 1.0, stds_raw)
    return PooledStandardiser(mean=means.astype(np.float64), std=stds_safe.astype(np.float64))


def save_standardiser(*, standardiser: PooledStandardiser, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, mean=standardiser.mean, std=standardiser.std)


def load_standardiser(*, path: Path) -> PooledStandardiser:
    payload = np.load(path)
    return PooledStandardiser(
        mean=np.asarray(payload["mean"], dtype=np.float64),
        std=np.asarray(payload["std"], dtype=np.float64),
    )


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
