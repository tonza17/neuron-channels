"""Varimax factor analysis on the full 68-d standardised matrix.

Implements REQ-8. Reusable: ``run_factor_pipeline`` is called by both the
primary-cohort entry point here and the strict-cohort orchestrator. Outputs
(primary cohort):

* results/data/factor_loadings.json
* results/data/factor_scores.json
* results/images/factor_loadings.png
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

# Compatibility shim: factor_analyzer==0.5.1 passes ``force_all_finite`` to
# sklearn.utils.check_array, but sklearn>=1.6 renamed this keyword to
# ``ensure_all_finite``. Patch both sklearn.utils.check_array and the symbol
# already imported into factor_analyzer.factor_analyzer (where it is called).
from sklearn import utils as _sk_utils  # noqa: E402

_original_check_array: Any = _sk_utils.check_array


def _check_array_shim(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-untyped-def]
    if "force_all_finite" in kwargs:
        kwargs["ensure_all_finite"] = kwargs.pop("force_all_finite")
    return _original_check_array(*args, **kwargs)


_sk_utils.check_array = _check_array_shim

import factor_analyzer.factor_analyzer as _fa_module  # noqa: E402

_fa_module.check_array = _check_array_shim

from factor_analyzer import FactorAnalyzer  # noqa: E402

from tasks.t0105_cluster_factor_analysis_dsi_pd.code.constants import (  # noqa: E402
    ALL_PARAM_NAMES,
    CHART_DPI,
    KAISER_FACTOR_CAP,
    N_TOTAL_DIMS,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.paths import (  # noqa: E402
    FACTOR_LOADINGS_HEATMAP_PATH,
    FACTOR_LOADINGS_PATH,
    FACTOR_SCORES_PATH,
    RESULTS_DATA_DIR,
    RESULTS_IMAGES_DIR,
    SELECTED_CELLS_PRIMARY_PATH,
)

EPS_STD: float = 1e-12


@dataclass(frozen=True, slots=True)
class FactorOutputs:
    n_factors: int
    eigenvalues_above_1_count: int
    eigenvalues: list[float]
    loadings: NDArray[np.float64]  # (68, n_factors)
    scores: NDArray[np.float64]  # (N_cells, n_factors)
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


def _build_full_matrix(*, cells: list[dict[str, Any]]) -> NDArray[np.float64]:
    n: int = len(cells)
    x_arr: NDArray[np.float64] = np.zeros((n, N_TOTAL_DIMS), dtype=np.float64)
    for i, cell in enumerate(cells):
        vec_obj: Any = cell["vector_68d"]
        assert isinstance(vec_obj, list)
        assert len(vec_obj) == N_TOTAL_DIMS
        x_arr[i, :] = np.array(vec_obj, dtype=np.float64)
    return x_arr


def _zscore_columns(*, x_arr: NDArray[np.float64]) -> NDArray[np.float64]:
    mu: NDArray[np.float64] = x_arr.mean(axis=0)
    sigma: NDArray[np.float64] = x_arr.std(axis=0, ddof=0)
    sigma_safe: NDArray[np.float64] = np.where(sigma < EPS_STD, 1.0, sigma)
    return (x_arr - mu) / sigma_safe


def _drop_constant_columns(
    *,
    x_arr: NDArray[np.float64],
    param_names: tuple[str, ...],
) -> tuple[NDArray[np.float64], list[int], list[str]]:
    """Return matrix with constant columns dropped + lists of kept indices and names."""
    sigma: NDArray[np.float64] = x_arr.std(axis=0, ddof=0)
    keep_mask: NDArray[np.bool_] = sigma >= EPS_STD
    kept_indices: list[int] = [int(i) for i in np.where(keep_mask)[0]]
    kept_names: list[str] = [param_names[i] for i in kept_indices]
    return x_arr[:, keep_mask], kept_indices, kept_names


def run_factor_pipeline(
    *,
    cells: list[dict[str, Any]],
    factor_cap: int = KAISER_FACTOR_CAP,
) -> tuple[FactorOutputs, list[int], list[str]]:
    """Fit varimax FA. Returns (outputs, kept_param_indices, kept_param_names).

    Constant columns (variance ~ 0) are silently dropped before fitting because
    factor_analyzer's correlation matrix would otherwise be singular.
    """
    x_arr: NDArray[np.float64] = _build_full_matrix(cells=cells)
    x_kept, kept_indices, kept_names = _drop_constant_columns(
        x_arr=x_arr, param_names=ALL_PARAM_NAMES
    )
    x_std: NDArray[np.float64] = _zscore_columns(x_arr=x_kept)
    # Eigenvalues of the correlation matrix.
    corr: NDArray[np.float64] = np.cov(x_std, rowvar=False, ddof=0)
    eigvals_full: NDArray[np.float64] = np.linalg.eigvalsh(corr)[::-1]
    eigvals_above_1: int = int((eigvals_full > 1.0).sum())
    # Cap and floor.
    n_factors: int = max(1, min(eigvals_above_1, factor_cap))

    fa = FactorAnalyzer(rotation="varimax", n_factors=n_factors, method="minres")
    fa.fit(x_std)
    loadings_kept: NDArray[np.float64] = np.asarray(fa.loadings_, dtype=np.float64)
    assert loadings_kept.shape == (x_std.shape[1], n_factors), (
        f"unexpected loadings shape {loadings_kept.shape}"
    )
    # Re-expand loadings to the full 68-d vector with NaN for dropped dims.
    loadings_full: NDArray[np.float64] = np.full(
        (N_TOTAL_DIMS, n_factors), fill_value=np.nan, dtype=np.float64
    )
    for kept_local_idx, full_idx in enumerate(kept_indices):
        loadings_full[full_idx, :] = loadings_kept[kept_local_idx, :]
    scores: NDArray[np.float64] = np.asarray(fa.transform(x_std), dtype=np.float64)

    outputs = FactorOutputs(
        n_factors=n_factors,
        eigenvalues_above_1_count=eigvals_above_1,
        eigenvalues=[float(v) for v in eigvals_full],
        loadings=loadings_full,
        scores=scores,
        n_cells=len(cells),
    )
    return outputs, kept_indices, kept_names


def _top5_per_factor(
    *,
    loadings: NDArray[np.float64],
) -> dict[str, list[dict[str, Any]]]:
    n_factors: int = loadings.shape[1]
    result: dict[str, list[dict[str, Any]]] = {}
    for fac_idx in range(n_factors):
        col: NDArray[np.float64] = loadings[:, fac_idx]
        # Replace NaN with 0 for ordering (constant-column dims).
        col_for_order: NDArray[np.float64] = np.where(np.isnan(col), 0.0, col)
        order: NDArray[np.intp] = np.argsort(-np.abs(col_for_order))[:5]
        entries: list[dict[str, Any]] = []
        for j in order:
            jj: int = int(j)
            entries.append(
                {
                    "param_index": jj,
                    "param_name": ALL_PARAM_NAMES[jj],
                    "loading": float(col[jj]) if not np.isnan(col[jj]) else None,
                }
            )
        result[f"F{fac_idx + 1}"] = entries
    return result


def _plot_loadings_heatmap(
    *,
    loadings: NDArray[np.float64],
    output_path: Path,
    title: str,
) -> None:
    n_factors: int = loadings.shape[1]
    fig_h: float = max(8.0, N_TOTAL_DIMS * 0.18)
    fig, ax = plt.subplots(figsize=(2.0 + n_factors * 0.9, fig_h))
    # Replace NaN with 0 so imshow doesn't blank out constant dims.
    plot_loadings: NDArray[np.float64] = np.where(np.isnan(loadings), 0.0, loadings)
    raw_max: float = float(np.nanmax(np.abs(loadings)))
    vmax: float = raw_max if np.isfinite(raw_max) else 1.0
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


def write_factor_outputs(
    *,
    outputs: FactorOutputs,
    kept_indices: list[int],
    kept_names: list[str],
    loadings_path: Path,
    scores_path: Path,
) -> None:
    top5: dict[str, list[dict[str, Any]]] = _top5_per_factor(loadings=outputs.loadings)
    loadings_serial: list[list[float | None]] = []
    for row_idx in range(outputs.loadings.shape[0]):
        row: list[float | None] = []
        for col_idx in range(outputs.loadings.shape[1]):
            v: float = float(outputs.loadings[row_idx, col_idx])
            row.append(None if np.isnan(v) else v)
        loadings_serial.append(row)
    json_obj: dict[str, Any] = {
        "n_cells": outputs.n_cells,
        "n_factors": outputs.n_factors,
        "eigenvalues_above_1_count": outputs.eigenvalues_above_1_count,
        "factor_cap": KAISER_FACTOR_CAP,
        "eigenvalues": outputs.eigenvalues,
        "param_names": list(ALL_PARAM_NAMES),
        "kept_param_indices": kept_indices,
        "kept_param_names": kept_names,
        "loadings": loadings_serial,
        "per_factor_top_loadings": top5,
    }
    with open(loadings_path, "w", encoding="utf-8") as f:
        json.dump(json_obj, f, indent=2)
    scores_serial: dict[str, Any] = {
        "n_cells": outputs.n_cells,
        "n_factors": outputs.n_factors,
        "scores": outputs.scores.tolist(),
    }
    with open(scores_path, "w", encoding="utf-8") as f:
        json.dump(scores_serial, f, indent=2)


def main() -> None:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    cells: list[dict[str, Any]] = _load_cells(path=SELECTED_CELLS_PRIMARY_PATH)
    outputs, kept_indices, kept_names = run_factor_pipeline(cells=cells)

    print(f"Factor analysis on N={outputs.n_cells} primary cells, full 68-d matrix.")
    print(
        f"  eigenvalues > 1: {outputs.eigenvalues_above_1_count} "
        f"(cap = {KAISER_FACTOR_CAP}) -> n_factors = {outputs.n_factors}"
    )
    print(
        f"  kept {len(kept_indices)} non-constant dims (dropped "
        f"{N_TOTAL_DIMS - len(kept_indices)} constants)."
    )
    top5: dict[str, list[dict[str, Any]]] = _top5_per_factor(loadings=outputs.loadings)
    for fac_key, entries in top5.items():
        print(f"  Top-5 loadings on {fac_key}:")
        for e in entries:
            load_val: float | None = e["loading"]
            load_str: str = "nan" if load_val is None else f"{load_val:+.4f}"
            print(f"    {int(e['param_index']):>3} {str(e['param_name']):<35s} {load_str}")

    write_factor_outputs(
        outputs=outputs,
        kept_indices=kept_indices,
        kept_names=kept_names,
        loadings_path=FACTOR_LOADINGS_PATH,
        scores_path=FACTOR_SCORES_PATH,
    )
    _plot_loadings_heatmap(
        loadings=outputs.loadings,
        output_path=FACTOR_LOADINGS_HEATMAP_PATH,
        title=f"Varimax factor loadings (primary cohort, N={outputs.n_cells})",
    )
    print()
    print(f"Wrote: {FACTOR_LOADINGS_PATH}")
    print(f"Wrote: {FACTOR_SCORES_PATH}")
    print(f"Wrote: {FACTOR_LOADINGS_HEATMAP_PATH}")


if __name__ == "__main__":
    main()
