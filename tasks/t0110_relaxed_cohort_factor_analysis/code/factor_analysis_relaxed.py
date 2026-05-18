"""Varimax factor analysis at the relaxed cohort (DSI > 0.2 AND PD > 3), and side-by-side
comparison to t0108's strict cohort (DSI > 0.5 AND PD > 10).

Outputs:
  results/data/filtered_cells.json
  results/data/factor_analysis_relaxed.json
  results/images/factor_correlations_comparison.png
  results/images/factor_loadings_heatmap_relaxed.png

Usage:
  uv run python -m tasks.t0110_relaxed_cohort_factor_analysis.code.factor_analysis_relaxed
"""

from __future__ import annotations

import gzip
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

from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.constants import (
    ALL_PARAM_NAMES,
    CHART_DPI,
    JOINT_FACTOR_R_THRESHOLD,
    KAISER_FACTOR_CAP,
    N_TOTAL_DIMS,
)
from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.factor_analysis import (
    varimax_rotation,
)

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0110_relaxed_cohort_factor_analysis"
T0106_EVALUATIONS_GZ: Path = (
    REPO_ROOT
    / "tasks"
    / "t0106_long_pdnd_nsga2_300gen"
    / "results"
    / "data"
    / "all_evaluations_seed44.json.gz"
)
T0108_FACTOR_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0108_t0106_cluster_factor_dsi05_pd10"
    / "results"
    / "data"
    / "factor_analysis.json"
)

FILTERED_CELLS_JSON: Path = TASK_ROOT / "results" / "data" / "filtered_cells.json"
FACTOR_ANALYSIS_RELAXED_JSON: Path = TASK_ROOT / "results" / "data" / "factor_analysis_relaxed.json"
FACTOR_LOADINGS_PNG: Path = TASK_ROOT / "results" / "images" / "factor_loadings_heatmap_relaxed.png"
FACTOR_CORR_COMPARISON_PNG: Path = (
    TASK_ROOT / "results" / "images" / "factor_correlations_comparison.png"
)

DSI_THRESHOLD: float = 0.2
PD_THRESHOLD_HZ: float = 3.0
DEDUP_DECIMALS: int = 6
EPS_STD: float = 1e-8


@dataclass(frozen=True, slots=True)
class FilteredCell:
    generation: int
    dsi: float
    pd_rate_hz: float
    vector_68d: list[float]


def _load_and_filter() -> tuple[list[FilteredCell], dict[str, int]]:
    with gzip.open(T0106_EVALUATIONS_GZ, "rt", encoding="utf-8") as f:
        payload = json.load(f)
    evaluations: list[dict] = payload["evaluations"]
    passing: list[dict] = [
        e
        for e in evaluations
        if e["dsi_vector_sum"] > DSI_THRESHOLD and e["pd_rate_hz"] > PD_THRESHOLD_HZ
    ]
    seen: dict[tuple[float, ...], FilteredCell] = {}
    for e in passing:
        vec: list[float] = list(e["vector_68d"])
        key: tuple[float, ...] = tuple(round(x, DEDUP_DECIMALS) for x in vec)
        if key in seen:
            continue
        seen[key] = FilteredCell(
            generation=int(e["generation"]),
            dsi=float(e["dsi_vector_sum"]),
            pd_rate_hz=float(e["pd_rate_hz"]),
            vector_68d=vec,
        )
    unique: list[FilteredCell] = list(seen.values())
    report: dict[str, int] = {
        "n_raw": len(evaluations),
        "n_passing_raw": len(passing),
        "n_unique": len(unique),
    }
    return unique, report


def _zscore(matrix: NDArray[np.float64]) -> NDArray[np.float64]:
    mu: NDArray[np.float64] = matrix.mean(axis=0)
    sigma: NDArray[np.float64] = matrix.std(axis=0, ddof=0)
    sigma_safe: NDArray[np.float64] = np.where(sigma < EPS_STD, 1.0, sigma)
    return (matrix - mu) / sigma_safe


def _drop_constant_columns(
    matrix: NDArray[np.float64],
) -> tuple[NDArray[np.float64], list[int]]:
    sigma: NDArray[np.float64] = matrix.std(axis=0, ddof=0)
    keep_mask: NDArray[np.bool_] = sigma >= EPS_STD
    kept_indices: list[int] = [int(i) for i in np.where(keep_mask)[0]]
    return matrix[:, keep_mask], kept_indices


def run_relaxed_fa(
    *,
    matrix_68d: NDArray[np.float64],
    dsi: NDArray[np.float64],
    pd_rate: NDArray[np.float64],
) -> dict[str, object]:
    kept_matrix, kept_indices = _drop_constant_columns(matrix_68d)
    z_matrix: NDArray[np.float64] = _zscore(kept_matrix)
    corr: NDArray[np.float64] = np.cov(z_matrix, rowvar=False, ddof=0)
    eigvals_full: NDArray[np.float64] = np.linalg.eigvalsh(corr)[::-1]
    eigvals_above_1: int = int((eigvals_full > 1.0).sum())
    n_factors: int = max(1, min(eigvals_above_1, KAISER_FACTOR_CAP))

    fa = FactorAnalysis(n_components=n_factors, rotation=None, random_state=42)
    fa.fit(z_matrix)
    unrotated_loadings: NDArray[np.float64] = fa.components_.T.astype(np.float64)
    loadings_kept: NDArray[np.float64] = varimax_rotation(loadings=unrotated_loadings)
    loadings_full: NDArray[np.float64] = np.full(
        (N_TOTAL_DIMS, n_factors), fill_value=np.nan, dtype=np.float64
    )
    for local_idx, full_idx in enumerate(kept_indices):
        loadings_full[full_idx, :] = loadings_kept[local_idx, :]
    scores: NDArray[np.float64] = (
        z_matrix @ loadings_kept @ np.linalg.pinv(loadings_kept.T @ loadings_kept)
    )

    dsi_corr: list[dict[str, float]] = []
    pd_corr: list[dict[str, float]] = []
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

    top_loadings_per_factor: list[list[dict[str, object]]] = []
    for f_idx in range(n_factors):
        col_full: NDArray[np.float64] = loadings_full[:, f_idx]
        col_for_order: NDArray[np.float64] = np.where(np.isnan(col_full), 0.0, col_full)
        order: NDArray[np.intp] = np.argsort(-np.abs(col_for_order))[:5]
        entries: list[dict[str, object]] = []
        for j in order:
            jj: int = int(j)
            loading: float | None = None if np.isnan(col_full[jj]) else float(col_full[jj])
            entries.append(
                {
                    "param_index": jj,
                    "param_name": ALL_PARAM_NAMES[jj],
                    "loading": loading,
                }
            )
        top_loadings_per_factor.append(entries)

    joint_factor_indices: list[int] = []
    for d_entry, p_entry in zip(dsi_corr, pd_corr, strict=True):
        if (
            abs(d_entry["pearson_r"]) > JOINT_FACTOR_R_THRESHOLD
            and abs(p_entry["pearson_r"]) > JOINT_FACTOR_R_THRESHOLD
        ):
            joint_factor_indices.append(int(d_entry["factor_index"]))

    return {
        "n_cells": int(matrix_68d.shape[0]),
        "n_factors": n_factors,
        "eigenvalues_above_1_count": eigvals_above_1,
        "eigenvalues": [float(v) for v in eigvals_full],
        "loadings_full": loadings_full.tolist(),
        "factor_scores": scores.tolist(),
        "top_loadings_per_factor": top_loadings_per_factor,
        "dsi_correlations": dsi_corr,
        "pd_correlations": pd_corr,
        "joint_factor_threshold": JOINT_FACTOR_R_THRESHOLD,
        "joint_factor_indices": joint_factor_indices,
    }


def _plot_comparison(
    *,
    t0108_dsi: list[dict[str, float]],
    t0108_pd: list[dict[str, float]],
    t0110_dsi: list[dict[str, float]],
    t0110_pd: list[dict[str, float]],
    output_path: Path,
) -> None:
    n108: int = len(t0108_dsi)
    n110: int = len(t0110_dsi)
    idx108: NDArray[np.intp] = np.arange(n108)
    idx110: NDArray[np.intp] = np.arange(n110)
    width: float = 0.4

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=CHART_DPI, sharey=True)
    for ax, dsi_corr, pd_corr, idx, title, n_cells in [
        (
            axes[0],
            t0108_dsi,
            t0108_pd,
            idx108,
            "t0108 strict (DSI > 0.5 AND PD > 10)",
            150,
        ),
        (
            axes[1],
            t0110_dsi,
            t0110_pd,
            idx110,
            "t0110 relaxed (DSI > 0.2 AND PD > 3)",
            247,
        ),
    ]:
        dsi_vals: list[float] = [float(d["pearson_r"]) for d in dsi_corr]
        pd_vals: list[float] = [float(d["pearson_r"]) for d in pd_corr]
        ax.bar(
            idx - width / 2,
            dsi_vals,
            width=width,
            color="tab:blue",
            edgecolor="black",
            label="r vs DSI",
        )
        ax.bar(
            idx + width / 2,
            pd_vals,
            width=width,
            color="tab:orange",
            edgecolor="black",
            label="r vs PD rate",
        )
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axhline(JOINT_FACTOR_R_THRESHOLD, color="grey", linestyle="--", linewidth=0.6)
        ax.axhline(-JOINT_FACTOR_R_THRESHOLD, color="grey", linestyle="--", linewidth=0.6)
        ax.set_xticks(idx)
        ax.set_xticklabels([f"F{i + 1}" for i in idx])
        ax.set_xlabel("factor (varimax)")
        ax.set_title(f"{title}\nN={n_cells} unique cells")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best", fontsize=9)
    axes[0].set_ylabel("Pearson r")
    fig.suptitle(
        "Factor-score correlations with DSI / PD: t0108 strict vs t0110 relaxed cohort",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


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
    ax.set_title("t0110 relaxed cohort: varimax factor loadings on 68 parameters")
    plt.colorbar(im, ax=ax, label="loading")
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def main() -> None:
    print("Loading t0106 evaluations and filtering...")
    cells, report = _load_and_filter()
    print(f"  N raw:     {report['n_raw']}")
    print(f"  N passing: {report['n_passing_raw']}")
    print(f"  N unique:  {report['n_unique']}")

    FILTERED_CELLS_JSON.parent.mkdir(parents=True, exist_ok=True)
    FILTERED_CELLS_JSON.write_text(
        json.dumps(
            {
                "report": {
                    **report,
                    "dsi_threshold": DSI_THRESHOLD,
                    "pd_threshold_hz": PD_THRESHOLD_HZ,
                    "source_task": "t0106_long_pdnd_nsga2_300gen",
                    "source_seed": 44,
                },
                "cells": [
                    {
                        "generation": c.generation,
                        "dsi": c.dsi,
                        "pd_rate_hz": c.pd_rate_hz,
                        "vector_68d": c.vector_68d,
                    }
                    for c in cells
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    vec_68d: NDArray[np.float64] = np.array([c.vector_68d for c in cells], dtype=np.float64)
    dsi: NDArray[np.float64] = np.array([c.dsi for c in cells], dtype=np.float64)
    pd_rate: NDArray[np.float64] = np.array([c.pd_rate_hz for c in cells], dtype=np.float64)

    print("\nRunning varimax FA on relaxed cohort...")
    result = run_relaxed_fa(matrix_68d=vec_68d, dsi=dsi, pd_rate=pd_rate)

    FACTOR_ANALYSIS_RELAXED_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")

    n_factors: int = int(result["n_factors"])
    eigvals_above_1: int = int(result["eigenvalues_above_1_count"])
    print(f"  Eigenvalues > 1: {eigvals_above_1}")
    print(f"  Factors retained: {n_factors}")
    print(f"  Joint factors |r_DSI|>0.3 AND |r_PD|>0.3: {result['joint_factor_indices']}")

    dsi_corr_relaxed: list[dict[str, float]] = result["dsi_correlations"]
    pd_corr_relaxed: list[dict[str, float]] = result["pd_correlations"]

    print("\nFactor-outcome sign counts (t0110 relaxed):")
    n_dsi_pos: int = sum(1 for d in dsi_corr_relaxed if d["pearson_r"] > 0)
    n_dsi_neg: int = sum(1 for d in dsi_corr_relaxed if d["pearson_r"] < 0)
    n_pd_pos: int = sum(1 for d in pd_corr_relaxed if d["pearson_r"] > 0)
    n_pd_neg: int = sum(1 for d in pd_corr_relaxed if d["pearson_r"] < 0)
    print(f"  DSI: {n_dsi_pos} positive, {n_dsi_neg} negative")
    print(f"  PD:  {n_pd_pos} positive, {n_pd_neg} negative")

    print("\nLoading t0108 strict-cohort FA for comparison...")
    t0108 = json.loads(T0108_FACTOR_JSON.read_text(encoding="utf-8"))
    t0108_dsi: list[dict[str, float]] = t0108["dsi_correlations"]
    t0108_pd: list[dict[str, float]] = t0108["pd_correlations"]

    print("\nRendering comparison and loadings charts...")
    _plot_comparison(
        t0108_dsi=t0108_dsi,
        t0108_pd=t0108_pd,
        t0110_dsi=dsi_corr_relaxed,
        t0110_pd=pd_corr_relaxed,
        output_path=FACTOR_CORR_COMPARISON_PNG,
    )
    _plot_loadings_heatmap(
        loadings_full=np.array(result["loadings_full"], dtype=np.float64),
        output_path=FACTOR_LOADINGS_PNG,
    )
    print(f"  Wrote: {FACTOR_CORR_COMPARISON_PNG}")
    print(f"  Wrote: {FACTOR_LOADINGS_PNG}")
    print(f"  Wrote: {FILTERED_CELLS_JSON}")
    print(f"  Wrote: {FACTOR_ANALYSIS_RELAXED_JSON}")


if __name__ == "__main__":
    main()
