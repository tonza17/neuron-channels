"""PCA on the 54-d electrophys submatrix + Mann-Whitney U on PC1/PC2 classes.

Implements REQ-6 and REQ-7. Reusable: ``run_pca_pipeline`` is called from
``run_strict_cohort.py`` with the strict cohort path. Outputs (primary cohort):

* results/data/pca_results.json
* results/data/pca_mannwhitney.json
* results/images/pca_electrophys_panels.png
* results/images/eigenvalue_scree.png
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from scipy.stats import mannwhitneyu
from sklearn.decomposition import PCA

from tasks.t0105_cluster_factor_analysis_dsi_pd.code.constants import (
    ALL_SOURCE_TASKS,
    CHART_DPI,
    CLASS_ASYMMETRIC,
    CLASS_SYMMETRIC,
    ELECTROPHYS_PARAM_NAMES,
    N_ELECTROPHYS_DIMS,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.paths import (
    EIGENVALUE_SCREE_PATH,
    PCA_MANNWHITNEY_PATH,
    PCA_PANELS_PATH,
    PCA_RESULTS_PATH,
    RESULTS_DATA_DIR,
    RESULTS_IMAGES_DIR,
    SELECTED_CELLS_PRIMARY_PATH,
)

EPS_STD: float = 1e-12


@dataclass(frozen=True, slots=True)
class PcaOutputs:
    pc_scores: NDArray[np.float64]
    explained_variance_ratio: list[float]
    eigenvalues: list[float]
    pc_loadings_top5: dict[str, list[tuple[int, str, float]]]
    n_cells: int


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


def _build_matrix_and_meta(
    *,
    cells: list[dict[str, Any]],
) -> tuple[NDArray[np.float64], list[str], list[str], NDArray[np.float64], NDArray[np.float64]]:
    n: int = len(cells)
    x_arr: NDArray[np.float64] = np.zeros((n, N_ELECTROPHYS_DIMS), dtype=np.float64)
    classes: list[str] = []
    sources: list[str] = []
    dsi_arr: NDArray[np.float64] = np.zeros(n, dtype=np.float64)
    pd_arr: NDArray[np.float64] = np.zeros(n, dtype=np.float64)
    for i, cell in enumerate(cells):
        vec_obj: Any = cell["vector_68d"]
        assert isinstance(vec_obj, list)
        x_arr[i, :] = np.array(vec_obj[:N_ELECTROPHYS_DIMS], dtype=np.float64)
        classes.append(str(cell["asym_class"]))
        sources.append(str(cell["source_task"]))
        dsi_arr[i] = float(cell["dsi"])
        pd_arr[i] = float(cell["pd_rate_hz"])
    return x_arr, classes, sources, dsi_arr, pd_arr


def _zscore_columns(*, x_arr: NDArray[np.float64]) -> NDArray[np.float64]:
    mu: NDArray[np.float64] = x_arr.mean(axis=0)
    sigma: NDArray[np.float64] = x_arr.std(axis=0, ddof=0)
    sigma_safe: NDArray[np.float64] = np.where(sigma < EPS_STD, 1.0, sigma)
    return (x_arr - mu) / sigma_safe


def run_pca_pipeline(
    *,
    cells: list[dict[str, Any]],
    n_components: int = 3,
) -> tuple[PcaOutputs, list[str], list[str], NDArray[np.float64], NDArray[np.float64]]:
    """Standardise, fit PCA, return PcaOutputs + class/source/DSI/PD metadata."""
    x_arr, classes, sources, dsi_arr, pd_arr = _build_matrix_and_meta(cells=cells)
    x_std: NDArray[np.float64] = _zscore_columns(x_arr=x_arr)
    pca: PCA = PCA(n_components=n_components)
    scores: NDArray[np.float64] = pca.fit_transform(x_std)
    # Eigenvalues of correlation matrix: variance per PC equals eigenvalue when
    # input is standardised. Use np.linalg.eigvalsh on cov matrix for the full
    # 54 eigenvalues.
    corr: NDArray[np.float64] = np.cov(x_std, rowvar=False, ddof=0)
    eigvals_full: NDArray[np.float64] = np.linalg.eigvalsh(corr)[::-1]

    pc_loadings_top5: dict[str, list[tuple[int, str, float]]] = {}
    for pc_idx in range(n_components):
        components: NDArray[np.float64] = pca.components_[pc_idx]
        # Sort by absolute magnitude descending; take top 5.
        order: NDArray[np.intp] = np.argsort(-np.abs(components))[:5]
        entries: list[tuple[int, str, float]] = []
        for j in order:
            entries.append((int(j), ELECTROPHYS_PARAM_NAMES[int(j)], float(components[int(j)])))
        pc_loadings_top5[f"PC{pc_idx + 1}"] = entries

    outputs = PcaOutputs(
        pc_scores=scores,
        explained_variance_ratio=[float(v) for v in pca.explained_variance_ratio_],
        eigenvalues=[float(v) for v in eigvals_full],
        pc_loadings_top5=pc_loadings_top5,
        n_cells=len(cells),
    )
    return outputs, classes, sources, dsi_arr, pd_arr


@dataclass(frozen=True, slots=True)
class MannWhitneyResult:
    pc1_u: float
    pc1_p: float
    pc2_u: float
    pc2_p: float
    n_symmetric: int
    n_asymmetric: int


def run_mannwhitney(
    *,
    pc_scores: NDArray[np.float64],
    classes: list[str],
) -> MannWhitneyResult:
    classes_arr: NDArray[np.str_] = np.array(classes)
    sym_mask: NDArray[np.bool_] = classes_arr == CLASS_SYMMETRIC
    asym_mask: NDArray[np.bool_] = classes_arr == CLASS_ASYMMETRIC
    n_sym: int = int(sym_mask.sum())
    n_asym: int = int(asym_mask.sum())
    if n_sym == 0 or n_asym == 0:
        # Cannot compute U; return NaN to make this explicit downstream.
        return MannWhitneyResult(
            pc1_u=float("nan"),
            pc1_p=float("nan"),
            pc2_u=float("nan"),
            pc2_p=float("nan"),
            n_symmetric=n_sym,
            n_asymmetric=n_asym,
        )
    pc1_sym: NDArray[np.float64] = pc_scores[sym_mask, 0]
    pc1_asym: NDArray[np.float64] = pc_scores[asym_mask, 0]
    pc2_sym: NDArray[np.float64] = pc_scores[sym_mask, 1]
    pc2_asym: NDArray[np.float64] = pc_scores[asym_mask, 1]
    u1, p1 = mannwhitneyu(pc1_sym, pc1_asym, alternative="two-sided")
    u2, p2 = mannwhitneyu(pc2_sym, pc2_asym, alternative="two-sided")
    return MannWhitneyResult(
        pc1_u=float(u1),
        pc1_p=float(p1),
        pc2_u=float(u2),
        pc2_p=float(p2),
        n_symmetric=n_sym,
        n_asymmetric=n_asym,
    )


def _plot_panels(
    *,
    pc_scores: NDArray[np.float64],
    classes: list[str],
    sources: list[str],
    dsi: NDArray[np.float64],
    pd_rate: NDArray[np.float64],
    output_path: Path,
    title_suffix: str,
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 10.0))
    axes_flat: list[plt.Axes] = list(np.asarray(axes).ravel())

    classes_arr: NDArray[np.str_] = np.array(classes)
    sources_arr: NDArray[np.str_] = np.array(sources)

    # Panel (a): class-coloured.
    ax_a: plt.Axes = axes_flat[0]
    sym_mask: NDArray[np.bool_] = classes_arr == CLASS_SYMMETRIC
    asym_mask: NDArray[np.bool_] = classes_arr == CLASS_ASYMMETRIC
    ax_a.scatter(
        pc_scores[sym_mask, 0],
        pc_scores[sym_mask, 1],
        c="#1f77b4",
        s=40,
        alpha=0.8,
        edgecolor="black",
        linewidth=0.4,
        label="symmetric",
    )
    ax_a.scatter(
        pc_scores[asym_mask, 0],
        pc_scores[asym_mask, 1],
        c="#d62728",
        s=40,
        alpha=0.8,
        edgecolor="black",
        linewidth=0.4,
        label="asymmetric",
    )
    ax_a.set_xlabel("PC1")
    ax_a.set_ylabel("PC2")
    ax_a.set_title("(a) Coloured by asymmetry class")
    ax_a.legend(loc="best")

    # Panel (b): DSI continuous.
    ax_b: plt.Axes = axes_flat[1]
    sc_b = ax_b.scatter(
        pc_scores[:, 0],
        pc_scores[:, 1],
        c=dsi,
        cmap="viridis",
        s=40,
        alpha=0.85,
        edgecolor="black",
        linewidth=0.4,
    )
    ax_b.set_xlabel("PC1")
    ax_b.set_ylabel("PC2")
    ax_b.set_title("(b) Coloured by DSI")
    fig.colorbar(sc_b, ax=ax_b, label="DSI")

    # Panel (c): PD continuous.
    ax_c: plt.Axes = axes_flat[2]
    sc_c = ax_c.scatter(
        pc_scores[:, 0],
        pc_scores[:, 1],
        c=pd_rate,
        cmap="plasma",
        s=40,
        alpha=0.85,
        edgecolor="black",
        linewidth=0.4,
    )
    ax_c.set_xlabel("PC1")
    ax_c.set_ylabel("PC2")
    ax_c.set_title("(c) Coloured by PD rate (Hz)")
    fig.colorbar(sc_c, ax=ax_c, label="PD rate (Hz)")

    # Panel (d): source-task categorical.
    ax_d: plt.Axes = axes_flat[3]
    colour_map: dict[str, str] = {
        "t0091": "#1f77b4",
        "t0099": "#2ca02c",
        "t0102": "#ff7f0e",
        "t0104": "#9467bd",
    }
    for src in ALL_SOURCE_TASKS:
        mask: NDArray[np.bool_] = sources_arr == src
        if mask.sum() == 0:
            continue
        ax_d.scatter(
            pc_scores[mask, 0],
            pc_scores[mask, 1],
            c=colour_map[src],
            s=40,
            alpha=0.8,
            edgecolor="black",
            linewidth=0.4,
            label=src,
        )
    ax_d.set_xlabel("PC1")
    ax_d.set_ylabel("PC2")
    ax_d.set_title("(d) Coloured by source task")
    ax_d.legend(loc="best")

    fig.suptitle(f"PCA on 54-d electrophys submatrix {title_suffix}", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def _plot_scree(*, eigenvalues: list[float], output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.0, 4.5))
    xs: list[int] = list(range(1, len(eigenvalues) + 1))
    ax.plot(xs, eigenvalues, marker="o", color="#1f77b4", lw=1.2)
    ax.axhline(y=1.0, color="#d62728", lw=1.0, linestyle="--", label="Kaiser threshold = 1")
    ax.set_xlabel("Component index")
    ax.set_ylabel("Eigenvalue (correlation-matrix scale)")
    ax.set_title("Scree plot of the 54-d electrophys correlation matrix")
    ax.legend(loc="upper right")
    ax.set_yscale("log")
    fig.tight_layout()
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def write_pca_outputs(
    *,
    outputs: PcaOutputs,
    classes: list[str],
    sources: list[str],
    pca_path: Path,
    mw_path: Path,
    mw_result: MannWhitneyResult,
) -> None:
    pca_serial: dict[str, Any] = {
        "n_cells": outputs.n_cells,
        "n_components": outputs.pc_scores.shape[1],
        "explained_variance_ratio": outputs.explained_variance_ratio,
        "eigenvalues": outputs.eigenvalues,
        "pc_loadings_top5": {
            pc_key: [
                {"param_index": idx, "param_name": name, "loading": load}
                for (idx, name, load) in entries
            ]
            for pc_key, entries in outputs.pc_loadings_top5.items()
        },
        "pc_scores": outputs.pc_scores.tolist(),
        "classes": classes,
        "sources": sources,
    }
    with open(pca_path, "w", encoding="utf-8") as f:
        json.dump(pca_serial, f, indent=2)

    pc1_interp: str = (
        f"PC1 separation between symmetric and asymmetric cells: U={mw_result.pc1_u:.2f}, "
        f"p={mw_result.pc1_p:.4g}. "
        + (
            "Statistically significant at alpha=0.05."
            if mw_result.pc1_p < 0.05
            else "Not significant at alpha=0.05; consistent with shared electrophys regime on PC1."
        )
    )
    pc2_interp: str = f"PC2 separation: U={mw_result.pc2_u:.2f}, p={mw_result.pc2_p:.4g}. " + (
        "Statistically significant at alpha=0.05."
        if mw_result.pc2_p < 0.05
        else "Not significant at alpha=0.05."
    )
    mw_serial: dict[str, Any] = {
        "n_symmetric": mw_result.n_symmetric,
        "n_asymmetric": mw_result.n_asymmetric,
        "pc1_u": mw_result.pc1_u,
        "pc1_p": mw_result.pc1_p,
        "pc2_u": mw_result.pc2_u,
        "pc2_p": mw_result.pc2_p,
        "interpretation": {"pc1": pc1_interp, "pc2": pc2_interp},
    }
    with open(mw_path, "w", encoding="utf-8") as f:
        json.dump(mw_serial, f, indent=2)


def main() -> None:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    cells: list[dict[str, Any]] = _load_cells(path=SELECTED_CELLS_PRIMARY_PATH)
    outputs, classes, sources, dsi, pd_rate = run_pca_pipeline(cells=cells, n_components=3)

    print(f"PCA on N={outputs.n_cells} primary cells, 54 features.")
    for i, ratio in enumerate(outputs.explained_variance_ratio):
        print(f"  PC{i + 1}: variance_ratio={ratio:.4f}")
    for pc_key, entries in outputs.pc_loadings_top5.items():
        print(f"  Top-5 loadings on {pc_key}:")
        for idx, name, load in entries:
            print(f"    {idx:>3} {name:<30s} {load:+.4f}")

    mw_result: MannWhitneyResult = run_mannwhitney(pc_scores=outputs.pc_scores, classes=classes)
    print(f"  Mann-Whitney U (PC1): U={mw_result.pc1_u:.2f} p={mw_result.pc1_p:.4g}")
    print(f"  Mann-Whitney U (PC2): U={mw_result.pc2_u:.2f} p={mw_result.pc2_p:.4g}")

    write_pca_outputs(
        outputs=outputs,
        classes=classes,
        sources=sources,
        pca_path=PCA_RESULTS_PATH,
        mw_path=PCA_MANNWHITNEY_PATH,
        mw_result=mw_result,
    )
    _plot_panels(
        pc_scores=outputs.pc_scores,
        classes=classes,
        sources=sources,
        dsi=dsi,
        pd_rate=pd_rate,
        output_path=PCA_PANELS_PATH,
        title_suffix=f"(primary cohort, N={outputs.n_cells})",
    )
    _plot_scree(eigenvalues=outputs.eigenvalues, output_path=EIGENVALUE_SCREE_PATH)
    print()
    print(f"Wrote: {PCA_RESULTS_PATH}")
    print(f"Wrote: {PCA_MANNWHITNEY_PATH}")
    print(f"Wrote: {PCA_PANELS_PATH}")
    print(f"Wrote: {EIGENVALUE_SCREE_PATH}")


if __name__ == "__main__":
    main()
