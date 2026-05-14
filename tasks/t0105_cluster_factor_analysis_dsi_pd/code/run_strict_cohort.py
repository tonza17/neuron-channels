"""Repeat headline analyses on the strict cohort (DSI > 0.2 AND PD > 3.0).

Implements REQ-11. Re-uses helper functions from pca_electrophys.py,
factor_analysis.py, and factor_correlations.py. Outputs:

* results/data/pca_results_strict.json
* results/data/pca_mannwhitney_strict.json
* results/data/factor_loadings_strict.json
* results/data/factor_correlations_strict.json
* results/images/pca_electrophys_panels_strict.png
* results/images/factor_loadings_strict.png
* results/images/factor_correlations_strict.png
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from tasks.t0105_cluster_factor_analysis_dsi_pd.code.constants import (
    ALL_PARAM_NAMES,
    CHART_DPI,
    KAISER_FACTOR_CAP,
    N_TOTAL_DIMS,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.factor_analysis import (
    run_factor_pipeline,
    write_factor_outputs,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.factor_correlations import (
    compute_correlations,
    find_joint_factors,
    top3_by_abs,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.paths import (
    FACTOR_CORRELATIONS_STRICT_PATH,
    FACTOR_CORRELATIONS_STRICT_PATH_PNG,
    FACTOR_LOADINGS_STRICT_PATH,
    FACTOR_LOADINGS_STRICT_PATH_PNG,
    PCA_MANNWHITNEY_STRICT_PATH,
    PCA_PANELS_STRICT_PATH,
    PCA_RESULTS_STRICT_PATH,
    RESULTS_DATA_DIR,
    RESULTS_IMAGES_DIR,
    SELECTED_CELLS_STRICT_PATH,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.pca_electrophys import (
    run_mannwhitney,
    run_pca_pipeline,
    write_pca_outputs,
)

# Strict cohort needs a separate factor scores file (separate from the headline).
FACTOR_SCORES_STRICT_PATH: Path = RESULTS_DATA_DIR / "factor_scores_strict.json"

# Skip threshold: if strict cohort N < this, refuse factor analysis but keep PCA.
STRICT_MIN_FOR_FACTOR_ANALYSIS: int = 10


def _load_cells(*, path: Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
    cells_obj: Any = data["cells"]
    assert isinstance(cells_obj, list)
    out: list[dict[str, Any]] = []
    for c in cells_obj:
        assert isinstance(c, dict)
        out.append(c)
    return out


def _plot_panels_simple(
    *,
    pc_scores: NDArray[np.float64],
    classes: list[str],
    sources: list[str],
    dsi: NDArray[np.float64],
    pd_rate: NDArray[np.float64],
    output_path: Path,
    n_cells: int,
) -> None:
    """Wrapper that re-uses the panel layout from pca_electrophys but with a strict title."""
    # Re-import the plotting function via a thin wrapper using the same layout.
    from tasks.t0105_cluster_factor_analysis_dsi_pd.code.pca_electrophys import (
        _plot_panels,  # type: ignore[attr-defined]
    )

    _plot_panels(
        pc_scores=pc_scores,
        classes=classes,
        sources=sources,
        dsi=dsi,
        pd_rate=pd_rate,
        output_path=output_path,
        title_suffix=f"(strict cohort, N={n_cells})",
    )


def _plot_factor_loadings_heatmap(
    *,
    loadings: NDArray[np.float64],
    output_path: Path,
    title: str,
) -> None:
    n_factors: int = loadings.shape[1]
    fig_h: float = max(8.0, N_TOTAL_DIMS * 0.18)
    fig, ax = plt.subplots(figsize=(2.0 + n_factors * 0.9, fig_h))
    plot_loadings: NDArray[np.float64] = np.where(np.isnan(loadings), 0.0, loadings)
    vmax_val: float = float(np.nanmax(np.abs(loadings)))
    vmax: float = vmax_val if np.isfinite(vmax_val) else 1.0
    im = ax.imshow(plot_loadings, cmap="RdBu_r", aspect="auto", vmin=-vmax, vmax=vmax)
    ax.set_xticks(list(range(n_factors)))
    ax.set_xticklabels([f"F{i + 1}" for i in range(n_factors)])
    ax.set_yticks(list(range(N_TOTAL_DIMS)))
    ax.set_yticklabels(list(ALL_PARAM_NAMES), fontsize=6)
    ax.set_xlabel("Factor")
    ax.set_ylabel("Parameter (54 electrophys + 14 morphology)")
    ax.set_title(title)
    fig.colorbar(im, ax=ax, label="Loading", shrink=0.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def _plot_correlations_chart(
    *,
    per_factor: list[dict[str, Any]],
    output_path: Path,
    title_suffix: str,
) -> None:
    n_factors: int = len(per_factor)
    xs: NDArray[np.float64] = np.arange(n_factors, dtype=np.float64)
    bar_w: float = 0.4
    fig, ax = plt.subplots(figsize=(max(6.0, n_factors * 0.8), 4.5))
    r_dsi: list[float] = [abs(float(e["r_dsi"])) for e in per_factor]
    r_pd: list[float] = [abs(float(e["r_pd"])) for e in per_factor]
    ax.bar(xs - bar_w / 2, r_dsi, bar_w, color="#1f77b4", label="|r| vs DSI")
    ax.bar(xs + bar_w / 2, r_pd, bar_w, color="#d62728", label="|r| vs PD")
    ax.axhline(
        y=0.3, color="#888888", lw=1.0, linestyle="--", label="joint-factor threshold |r| = 0.3"
    )
    ax.set_xticks(xs)
    ax.set_xticklabels([str(e["factor"]) for e in per_factor])
    ax.set_ylabel("|Pearson r|")
    ax.set_xlabel("Factor")
    ax.set_title(f"Factor correlation with DSI and PD {title_suffix}")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def main() -> None:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    cells: list[dict[str, Any]] = _load_cells(path=SELECTED_CELLS_STRICT_PATH)
    n_cells: int = len(cells)
    print(f"Strict cohort: N={n_cells}")

    # === PCA + Mann-Whitney ===
    pca_outputs, classes, sources, dsi, pd_rate = run_pca_pipeline(cells=cells, n_components=3)
    mw_result = run_mannwhitney(pc_scores=pca_outputs.pc_scores, classes=classes)
    print(
        f"  PCA variance: PC1={pca_outputs.explained_variance_ratio[0]:.4f} "
        f"PC2={pca_outputs.explained_variance_ratio[1]:.4f} "
        f"PC3={pca_outputs.explained_variance_ratio[2]:.4f}"
    )
    print(f"  MW PC1: U={mw_result.pc1_u:.2f} p={mw_result.pc1_p:.4g}")
    print(f"  MW PC2: U={mw_result.pc2_u:.2f} p={mw_result.pc2_p:.4g}")
    write_pca_outputs(
        outputs=pca_outputs,
        classes=classes,
        sources=sources,
        pca_path=PCA_RESULTS_STRICT_PATH,
        mw_path=PCA_MANNWHITNEY_STRICT_PATH,
        mw_result=mw_result,
    )
    _plot_panels_simple(
        pc_scores=pca_outputs.pc_scores,
        classes=classes,
        sources=sources,
        dsi=dsi,
        pd_rate=pd_rate,
        output_path=PCA_PANELS_STRICT_PATH,
        n_cells=n_cells,
    )

    # === Factor analysis ===
    if n_cells < STRICT_MIN_FOR_FACTOR_ANALYSIS:
        print(
            f"  Strict-cohort N={n_cells} < {STRICT_MIN_FOR_FACTOR_ANALYSIS}; "
            "skipping factor analysis."
        )
        skip_payload: dict[str, Any] = {
            "strict_cohort_factor_analysis_skipped": True,
            "n_cells": n_cells,
            "reason": f"Strict-cohort N={n_cells} below minimum {STRICT_MIN_FOR_FACTOR_ANALYSIS}; "
            "factor analysis would be numerically degenerate.",
        }
        with open(FACTOR_LOADINGS_STRICT_PATH, "w", encoding="utf-8") as f:
            json.dump(skip_payload, f, indent=2)
        with open(FACTOR_CORRELATIONS_STRICT_PATH, "w", encoding="utf-8") as f:
            json.dump(skip_payload, f, indent=2)
        print(
            f"Wrote skip markers to {FACTOR_LOADINGS_STRICT_PATH} and "
            f"{FACTOR_CORRELATIONS_STRICT_PATH}"
        )
        return

    factor_outputs, kept_indices, kept_names = run_factor_pipeline(
        cells=cells, factor_cap=KAISER_FACTOR_CAP
    )
    print(
        f"  Factor analysis: n_factors={factor_outputs.n_factors} "
        f"(eigvals>1: {factor_outputs.eigenvalues_above_1_count})"
    )
    write_factor_outputs(
        outputs=factor_outputs,
        kept_indices=kept_indices,
        kept_names=kept_names,
        loadings_path=FACTOR_LOADINGS_STRICT_PATH,
        scores_path=FACTOR_SCORES_STRICT_PATH,
    )
    _plot_factor_loadings_heatmap(
        loadings=factor_outputs.loadings,
        output_path=FACTOR_LOADINGS_STRICT_PATH_PNG,
        title=f"Varimax factor loadings (strict cohort, N={n_cells})",
    )

    # === Factor correlations ===
    correlations = compute_correlations(scores=factor_outputs.scores, dsi=dsi, pd_rate=pd_rate)
    top3_d = top3_by_abs(correlations=correlations, outcome="dsi")
    top3_p = top3_by_abs(correlations=correlations, outcome="pd")
    joint = find_joint_factors(correlations=correlations)
    per_factor: list[dict[str, Any]] = [
        {
            "factor": f"F{c.factor_index + 1}",
            "factor_index": c.factor_index,
            "r_dsi": c.r_dsi,
            "p_dsi": c.p_dsi,
            "r_pd": c.r_pd,
            "p_pd": c.p_pd,
        }
        for c in correlations
    ]
    print(f"  Top-3 vs DSI: {[(e['factor'], round(e['r'], 3)) for e in top3_d]}")
    print(f"  Top-3 vs PD:  {[(e['factor'], round(e['r'], 3)) for e in top3_p]}")
    print(f"  Joint factors (|r| > 0.3 both): {len(joint)}")
    fc_payload: dict[str, Any] = {
        "n_factors": len(correlations),
        "joint_r_threshold": 0.3,
        "per_factor": per_factor,
        "top3_dsi": top3_d,
        "top3_pd": top3_p,
        "joint_factors": joint,
    }
    with open(FACTOR_CORRELATIONS_STRICT_PATH, "w", encoding="utf-8") as f:
        json.dump(fc_payload, f, indent=2)
    _plot_correlations_chart(
        per_factor=per_factor,
        output_path=FACTOR_CORRELATIONS_STRICT_PATH_PNG,
        title_suffix="(strict cohort)",
    )

    print()
    print(f"Wrote: {PCA_RESULTS_STRICT_PATH}")
    print(f"Wrote: {PCA_MANNWHITNEY_STRICT_PATH}")
    print(f"Wrote: {PCA_PANELS_STRICT_PATH}")
    print(f"Wrote: {FACTOR_LOADINGS_STRICT_PATH}")
    print(f"Wrote: {FACTOR_LOADINGS_STRICT_PATH_PNG}")
    print(f"Wrote: {FACTOR_CORRELATIONS_STRICT_PATH}")
    print(f"Wrote: {FACTOR_CORRELATIONS_STRICT_PATH_PNG}")


if __name__ == "__main__":
    main()
