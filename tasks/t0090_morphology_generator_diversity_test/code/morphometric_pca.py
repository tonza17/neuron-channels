"""Phase E.2: morphometric PCA (and optional UMAP) over 60 morphologies.

Computes 6 morphometric features per cell and produces:

* ``results/images/morphometric_pca.png`` — PC1 vs PC2 scatter, colour-coded
* ``results/images/morphometric_umap.png`` — only if ``umap-learn`` is installed
* ``data/morphometric_summary.json`` — per-morph features, PCA loadings, cluster radii
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from sklearn.decomposition import PCA  # type: ignore[import-untyped]

from tasks.t0090_morphology_generator_diversity_test.code.generator import (
    generate_morphology,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0090_morphology_generator_diversity_test.code.paths import (
    DATA_DIFFERENT_DIR,
    DATA_MORPHOMETRIC_SUMMARY_JSON,
    DATA_SIMILAR_DIR,
    RESULTS_IMAGES_DIR,
    ensure_directories,
)

FEATURE_COLUMNS: tuple[str, ...] = (
    "total_dendritic_length_um",
    "branch_count",
    "max_strahler_depth",
    "electrotonic_length_lambda",
    "soma_displacement_um",
    "field_major_axis_length_um",
)
N_FEATURES: int = len(FEATURE_COLUMNS)

DIFFERENT_COLOR: str = "#0072B2"
SIMILAR_COLOR: str = "#D55E00"


@dataclass(frozen=True, slots=True)
class _MorphRecord:
    morph_id: str
    population: str
    features: NDArray[np.float64]


def _load_morph_features(*, json_path: Path, population: str) -> _MorphRecord:
    data = json.loads(json_path.read_text())
    params = MorphologyParams.from_dict(data=data)
    cell = generate_morphology(params=params, morph_seed=int(params.morph_seed))
    summary = cell.morphometric_summary
    feats = np.array(
        [
            float(summary.total_dendritic_length_um),
            float(summary.branch_count),
            float(summary.max_strahler_depth),
            float(summary.electrotonic_length_lambda),
            float(summary.soma_displacement_um),
            float(summary.field_major_axis_length_um),
        ],
        dtype=np.float64,
    )
    assert feats.shape == (N_FEATURES,)
    return _MorphRecord(morph_id=json_path.stem, population=population, features=feats)


def collect_features() -> tuple[list[_MorphRecord], NDArray[np.float64]]:
    different_jsons = sorted(DATA_DIFFERENT_DIR.glob("morph_*.json"))
    similar_jsons = sorted(DATA_SIMILAR_DIR.glob("morph_*.json"))
    records: list[_MorphRecord] = []
    for jp in different_jsons:
        records.append(_load_morph_features(json_path=jp, population="different"))
    for jp in similar_jsons:
        records.append(_load_morph_features(json_path=jp, population="similar"))
    matrix = np.stack([r.features for r in records], axis=0)
    return records, matrix


def standardise(*, features: NDArray[np.float64]) -> NDArray[np.float64]:
    """Z-score per feature column. Columns with zero variance are left untouched."""
    mu = features.mean(axis=0)
    sigma = features.std(axis=0)
    safe_sigma = np.where(sigma > 1e-12, sigma, 1.0)
    out: NDArray[np.float64] = (features - mu) / safe_sigma
    return out


def run_pca(
    *, features_z: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
    """Run 2-component PCA; return (scores, components, total_variance_explained)."""
    pca = PCA(n_components=2)
    scores = pca.fit_transform(features_z)
    var_total = float(pca.explained_variance_ratio_.sum())
    return np.asarray(scores), np.asarray(pca.components_), var_total


def _plot_scatter(
    *,
    scores: NDArray[np.float64],
    records: list[_MorphRecord],
    title: str,
    xlabel: str,
    ylabel: str,
    output_png: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 6.0))
    diff_mask = np.array([r.population == "different" for r in records])
    sim_mask = ~diff_mask
    ax.scatter(
        scores[diff_mask, 0],
        scores[diff_mask, 1],
        c=DIFFERENT_COLOR,
        s=50,
        alpha=0.85,
        label=f"different (n={int(diff_mask.sum())})",
        edgecolors="white",
        linewidths=0.5,
    )
    ax.scatter(
        scores[sim_mask, 0],
        scores[sim_mask, 1],
        c=SIMILAR_COLOR,
        s=50,
        alpha=0.85,
        label=f"similar (n={int(sim_mask.sum())})",
        edgecolors="white",
        linewidths=0.5,
    )
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_png, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _try_umap(
    *,
    features_z: NDArray[np.float64],
    records: list[_MorphRecord],
    output_png: Path,
) -> bool:
    try:
        import umap  # type: ignore[import-not-found,unused-ignore]
    except ImportError:
        print("umap-learn not installed; PCA-only fallback")
        return False
    reducer = umap.UMAP(n_neighbors=15, n_components=2, random_state=42)
    scores = reducer.fit_transform(features_z)
    _plot_scatter(
        scores=np.asarray(scores),
        records=records,
        title="UMAP of morphometric features (60 morphologies)",
        xlabel="UMAP 1",
        ylabel="UMAP 2",
        output_png=output_png,
    )
    return True


def _cluster_radius(*, scores: NDArray[np.float64], mask: NDArray[np.bool_]) -> float:
    """Return the 95th percentile distance from cluster centroid in 2D."""
    pts = scores[mask]
    if pts.shape[0] == 0:
        return 0.0
    centroid = pts.mean(axis=0)
    distances = np.linalg.norm(pts - centroid, axis=1)
    return float(np.percentile(distances, 95))


def main() -> None:
    ensure_directories()

    print("collecting features for 60 morphologies ...")
    records, features = collect_features()
    print(f"  matrix shape={features.shape}")

    features_z = standardise(features=features)
    pca_scores, pca_components, var_total = run_pca(features_z=features_z)
    print(f"  PC1+PC2 variance explained: {var_total:.3f}")

    diff_mask = np.array([r.population == "different" for r in records])
    similar_radius = _cluster_radius(scores=pca_scores, mask=~diff_mask)
    different_radius = _cluster_radius(scores=pca_scores, mask=diff_mask)
    pc1_range = float(pca_scores[:, 0].max() - pca_scores[:, 0].min())
    similar_radius_pct = (similar_radius / pc1_range) * 100.0 if pc1_range > 0 else 0.0
    print(
        f"  similar set 95th-pct PCA radius: {similar_radius:.3f} "
        f"({similar_radius_pct:.1f} % of PC1 range)"
    )

    out_pca = RESULTS_IMAGES_DIR / "morphometric_pca.png"
    _plot_scatter(
        scores=pca_scores,
        records=records,
        title=f"Morphometric PCA (PC1+PC2 var = {var_total:.2%})",
        xlabel="PC1",
        ylabel="PC2",
        output_png=out_pca,
    )
    print(f"wrote {out_pca}")

    out_umap = RESULTS_IMAGES_DIR / "morphometric_umap.png"
    has_umap = _try_umap(features_z=features_z, records=records, output_png=out_umap)
    if has_umap:
        print(f"wrote {out_umap}")

    summary = {
        "n_morphologies": len(records),
        "feature_columns": list(FEATURE_COLUMNS),
        "pc1_variance_explained": float((pca_components[0] ** 2).sum() / N_FEATURES * var_total),
        "pc1_pc2_variance_explained": var_total,
        "pca_loadings": pca_components.tolist(),
        "similar_cluster_radius_p95": similar_radius,
        "different_cluster_radius_p95": different_radius,
        "similar_radius_pct_of_pc1_range": similar_radius_pct,
        "pc1_range": pc1_range,
        "umap_available": has_umap,
        "per_morph_records": [
            {
                "morph_id": r.morph_id,
                "population": r.population,
                "features": dict(zip(FEATURE_COLUMNS, r.features.tolist(), strict=True)),
                "pc1": float(pca_scores[i, 0]),
                "pc2": float(pca_scores[i, 1]),
            }
            for i, r in enumerate(records)
        ],
    }
    DATA_MORPHOMETRIC_SUMMARY_JSON.write_text(json.dumps(summary, indent=2))
    print(f"wrote {DATA_MORPHOMETRIC_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
