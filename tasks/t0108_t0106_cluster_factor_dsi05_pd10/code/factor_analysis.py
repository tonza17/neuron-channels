"""Varimax factor analysis on the full 68-d vector matrix.

Outputs:
  results/data/factor_analysis.json
  results/images/factor_loadings_heatmap.png
  results/images/factor_correlations_dsi_pd.png

Usage:
  uv run python -m tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.factor_analysis
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
from scipy.stats import pearsonr
from sklearn.decomposition import FactorAnalysis

from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.cluster_helpers import write_json
from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.constants import (
    ALL_PARAM_NAMES,
    CHART_DPI,
    JOINT_FACTOR_R_THRESHOLD,
    KAISER_FACTOR_CAP,
    N_TOTAL_DIMS,
)
from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.paths import (
    FACTOR_ANALYSIS_JSON,
    FACTOR_CORRELATIONS_PNG,
    FACTOR_LOADINGS_PNG,
    FILTERED_CELLS_JSON,
)

EPS_STD: float = 1e-8
VARIMAX_TOL: float = 1e-6
VARIMAX_MAX_ITER: int = 500


def varimax_rotation(
    *,
    loadings: NDArray[np.float64],
    gamma: float = 1.0,
    tol: float = VARIMAX_TOL,
    max_iter: int = VARIMAX_MAX_ITER,
) -> NDArray[np.float64]:
    """Apply Kaiser varimax rotation to a (p, k) loadings matrix.

    Iterative SVD of Lambda^T * (Lambda^3 - (gamma/p) * Lambda * diag(Lambda^T Lambda)).
    """
    p, k = loadings.shape
    if k < 2:
        return loadings.copy()
    rotation: NDArray[np.float64] = np.eye(k, dtype=np.float64)
    d: float = 0.0
    for _ in range(max_iter):
        d_old: float = d
        lambda_rotated: NDArray[np.float64] = loadings @ rotation
        third_moment: NDArray[np.float64] = lambda_rotated**3
        diag_term: NDArray[np.float64] = (
            (gamma / p) * lambda_rotated * np.diag(lambda_rotated.T @ lambda_rotated)
        )
        u_svd, s_svd, vt_svd = np.linalg.svd(
            loadings.T @ (third_moment - diag_term), full_matrices=False
        )
        rotation = u_svd @ vt_svd
        d = float(s_svd.sum())
        if d_old != 0.0 and (d - d_old) / d_old < tol:
            break
    return loadings @ rotation


@dataclass(frozen=True, slots=True)
class FactorResult:
    n_factors: int
    eigenvalues_above_1_count: int
    eigenvalues: list[float]
    loadings_full: NDArray[np.float64]
    scores: NDArray[np.float64]
    kept_param_indices: list[int]
    kept_param_names: list[str]


def _load_data(
    path: Path,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cells = payload["cells"]
    vec_68d: NDArray[np.float64] = np.array([c["vector_68d"] for c in cells], dtype=np.float64)
    dsi: NDArray[np.float64] = np.array([c["dsi"] for c in cells], dtype=np.float64)
    pd_rate: NDArray[np.float64] = np.array([c["pd_rate_hz"] for c in cells], dtype=np.float64)
    return vec_68d, dsi, pd_rate


def _drop_constant_columns(
    *,
    matrix: NDArray[np.float64],
) -> tuple[NDArray[np.float64], list[int], list[str]]:
    sigma: NDArray[np.float64] = matrix.std(axis=0, ddof=0)
    keep_mask: NDArray[np.bool_] = sigma >= EPS_STD
    kept_indices: list[int] = [int(i) for i in np.where(keep_mask)[0]]
    kept_names: list[str] = [ALL_PARAM_NAMES[i] for i in kept_indices]
    return matrix[:, keep_mask], kept_indices, kept_names


def _zscore(matrix: NDArray[np.float64]) -> NDArray[np.float64]:
    mu: NDArray[np.float64] = matrix.mean(axis=0)
    sigma: NDArray[np.float64] = matrix.std(axis=0, ddof=0)
    sigma_safe: NDArray[np.float64] = np.where(sigma < EPS_STD, 1.0, sigma)
    return (matrix - mu) / sigma_safe


def run_factor_analysis(
    *,
    matrix_68d: NDArray[np.float64],
    factor_cap: int = KAISER_FACTOR_CAP,
) -> FactorResult:
    kept_matrix, kept_indices, kept_names = _drop_constant_columns(matrix=matrix_68d)
    z_matrix: NDArray[np.float64] = _zscore(kept_matrix)
    corr: NDArray[np.float64] = np.cov(z_matrix, rowvar=False, ddof=0)
    eigvals_full: NDArray[np.float64] = np.linalg.eigvalsh(corr)[::-1]
    eigvals_above_1: int = int((eigvals_full > 1.0).sum())
    n_factors: int = max(1, min(eigvals_above_1, factor_cap))

    fa = FactorAnalysis(n_components=n_factors, rotation=None, random_state=42)
    fa.fit(z_matrix)
    unrotated_loadings: NDArray[np.float64] = fa.components_.T.astype(np.float64)
    assert unrotated_loadings.shape == (z_matrix.shape[1], n_factors)
    loadings_kept: NDArray[np.float64] = varimax_rotation(loadings=unrotated_loadings)
    loadings_full: NDArray[np.float64] = np.full(
        (N_TOTAL_DIMS, n_factors), fill_value=np.nan, dtype=np.float64
    )
    for local_idx, full_idx in enumerate(kept_indices):
        loadings_full[full_idx, :] = loadings_kept[local_idx, :]
    # Rotated factor scores via the regression method:
    #   scores = Z * Lambda * (Lambda^T Lambda)^-1
    # This is a closed-form approximation of the optimal score estimator under the FA model.
    rotated_scores: NDArray[np.float64] = (
        z_matrix @ loadings_kept @ np.linalg.pinv(loadings_kept.T @ loadings_kept)
    )
    scores: NDArray[np.float64] = rotated_scores

    return FactorResult(
        n_factors=n_factors,
        eigenvalues_above_1_count=eigvals_above_1,
        eigenvalues=[float(v) for v in eigvals_full],
        loadings_full=loadings_full,
        scores=scores,
        kept_param_indices=kept_indices,
        kept_param_names=kept_names,
    )


def _top_loadings_per_factor(
    *,
    loadings_full: NDArray[np.float64],
    top_k: int = 5,
) -> list[list[dict[str, object]]]:
    n_factors: int = loadings_full.shape[1]
    result: list[list[dict[str, object]]] = []
    for f_idx in range(n_factors):
        col: NDArray[np.float64] = loadings_full[:, f_idx]
        col_for_order: NDArray[np.float64] = np.where(np.isnan(col), 0.0, col)
        order: NDArray[np.intp] = np.argsort(-np.abs(col_for_order))[:top_k]
        entries: list[dict[str, object]] = []
        for j in order:
            jj: int = int(j)
            loading: float | None = None if np.isnan(col[jj]) else float(col[jj])
            entries.append(
                {
                    "param_index": jj,
                    "param_name": ALL_PARAM_NAMES[jj],
                    "loading": loading,
                }
            )
        result.append(entries)
    return result


def _correlate_factors_with_outcomes(
    *,
    scores: NDArray[np.float64],
    dsi: NDArray[np.float64],
    pd_rate: NDArray[np.float64],
) -> tuple[list[dict[str, float]], list[dict[str, float]]]:
    dsi_corr: list[dict[str, float]] = []
    pd_corr: list[dict[str, float]] = []
    n_factors: int = scores.shape[1]
    for f_idx in range(n_factors):
        col: NDArray[np.float64] = scores[:, f_idx]
        r_dsi, p_dsi = pearsonr(col, dsi)
        r_pd, p_pd = pearsonr(col, pd_rate)
        dsi_corr.append(
            {
                "factor_index": f_idx + 1,
                "pearson_r": float(r_dsi),
                "p_value": float(p_dsi),
            }
        )
        pd_corr.append(
            {
                "factor_index": f_idx + 1,
                "pearson_r": float(r_pd),
                "p_value": float(p_pd),
            }
        )
    return dsi_corr, pd_corr


def _identify_joint_factors(
    *,
    dsi_corr: list[dict[str, float]],
    pd_corr: list[dict[str, float]],
    threshold: float,
) -> list[int]:
    joint_factor_indices: list[int] = []
    for dsi_entry, pd_entry in zip(dsi_corr, pd_corr, strict=True):
        if abs(dsi_entry["pearson_r"]) > threshold and abs(pd_entry["pearson_r"]) > threshold:
            joint_factor_indices.append(int(dsi_entry["factor_index"]))
    return joint_factor_indices


def _plot_loadings_heatmap(
    *,
    loadings_full: NDArray[np.float64],
    output_path: Path,
) -> None:
    n_factors: int = loadings_full.shape[1]
    fig, ax = plt.subplots(
        figsize=(max(6, 0.6 * n_factors + 4), 0.18 * N_TOTAL_DIMS + 1),
        dpi=CHART_DPI,
    )
    data: NDArray[np.float64] = np.where(np.isnan(loadings_full), 0.0, loadings_full)
    vmax: float = float(np.nanmax(np.abs(loadings_full)))
    im = ax.imshow(data, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_xticks(range(n_factors))
    ax.set_xticklabels([f"F{i + 1}" for i in range(n_factors)])
    ax.set_yticks(range(N_TOTAL_DIMS))
    ax.set_yticklabels(ALL_PARAM_NAMES, fontsize=6)
    ax.set_title("Varimax factor loadings on 68 parameters")
    plt.colorbar(im, ax=ax, label="loading")
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def _plot_factor_correlations(
    *,
    dsi_corr: list[dict[str, float]],
    pd_corr: list[dict[str, float]],
    output_path: Path,
) -> None:
    n_factors: int = len(dsi_corr)
    factor_indices: NDArray[np.intp] = np.arange(n_factors)
    width: float = 0.4
    fig, ax = plt.subplots(figsize=(max(7, 0.6 * n_factors + 3), 5), dpi=CHART_DPI)
    dsi_vals: list[float] = [float(d["pearson_r"]) for d in dsi_corr]
    pd_vals: list[float] = [float(d["pearson_r"]) for d in pd_corr]
    ax.bar(
        factor_indices - width / 2,
        dsi_vals,
        width=width,
        color="tab:blue",
        edgecolor="black",
        label="r vs DSI",
    )
    ax.bar(
        factor_indices + width / 2,
        pd_vals,
        width=width,
        color="tab:orange",
        edgecolor="black",
        label="r vs PD rate",
    )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axhline(JOINT_FACTOR_R_THRESHOLD, color="grey", linestyle="--", linewidth=0.8)
    ax.axhline(-JOINT_FACTOR_R_THRESHOLD, color="grey", linestyle="--", linewidth=0.8)
    ax.set_xticks(factor_indices)
    ax.set_xticklabels([f"F{i + 1}" for i in range(n_factors)])
    ax.set_ylabel("Pearson r")
    ax.set_title("Factor-score correlations with DSI and PD rate")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def main() -> None:
    vec_68d, dsi, pd_rate = _load_data(path=FILTERED_CELLS_JSON)
    n_cells: int = vec_68d.shape[0]
    print(f"N cells: {n_cells}")

    result: FactorResult = run_factor_analysis(matrix_68d=vec_68d)
    print(f"Eigenvalues > 1: {result.eigenvalues_above_1_count}")
    print(f"Factors retained: {result.n_factors}")
    n_kept: int = len(result.kept_param_indices)
    print(f"Kept dims after constant-column drop: {n_kept} / {N_TOTAL_DIMS}")

    top_loadings: list[list[dict[str, object]]] = _top_loadings_per_factor(
        loadings_full=result.loadings_full
    )
    dsi_corr, pd_corr = _correlate_factors_with_outcomes(
        scores=result.scores, dsi=dsi, pd_rate=pd_rate
    )
    joint_factor_indices: list[int] = _identify_joint_factors(
        dsi_corr=dsi_corr, pd_corr=pd_corr, threshold=JOINT_FACTOR_R_THRESHOLD
    )

    print("\nTop 3 factors by |r vs DSI|:")
    for entry in sorted(dsi_corr, key=lambda x: -abs(x["pearson_r"]))[:3]:
        print(
            f"  F{int(entry['factor_index'])}: r={entry['pearson_r']:.3f} p={entry['p_value']:.2g}"
        )
    print("Top 3 factors by |r vs PD|:")
    for entry in sorted(pd_corr, key=lambda x: -abs(x["pearson_r"]))[:3]:
        print(
            f"  F{int(entry['factor_index'])}: r={entry['pearson_r']:.3f} p={entry['p_value']:.2g}"
        )
    print(
        f"\nJoint factors (|r_DSI| > {JOINT_FACTOR_R_THRESHOLD} AND "
        f"|r_PD| > {JOINT_FACTOR_R_THRESHOLD}): {joint_factor_indices}"
    )

    payload: dict[str, object] = {
        "n_cells": n_cells,
        "n_factors": result.n_factors,
        "eigenvalues_above_1_count": result.eigenvalues_above_1_count,
        "eigenvalues": result.eigenvalues,
        "kept_param_indices": result.kept_param_indices,
        "kept_param_names": result.kept_param_names,
        "loadings_full": result.loadings_full.tolist(),
        "top_loadings_per_factor": top_loadings,
        "factor_scores": result.scores.tolist(),
        "dsi_correlations": dsi_corr,
        "pd_correlations": pd_corr,
        "joint_factor_threshold": JOINT_FACTOR_R_THRESHOLD,
        "joint_factor_indices": joint_factor_indices,
    }
    write_json(payload=payload, path=FACTOR_ANALYSIS_JSON)

    _plot_loadings_heatmap(loadings_full=result.loadings_full, output_path=FACTOR_LOADINGS_PNG)
    _plot_factor_correlations(
        dsi_corr=dsi_corr, pd_corr=pd_corr, output_path=FACTOR_CORRELATIONS_PNG
    )
    print(f"\nWrote {FACTOR_ANALYSIS_JSON}")
    print(f"Wrote {FACTOR_LOADINGS_PNG}")
    print(f"Wrote {FACTOR_CORRELATIONS_PNG}")


if __name__ == "__main__":
    main()
