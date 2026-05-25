"""Varimax factor analysis on the full union-pool z-scored 68-d matrix, with correlations vs
four outcome metrics: mi_count_bits, atp_per_spike_molecules, dsi_vector_sum, pd_rate_hz.

Outputs:
    results/images/factor_loadings_heatmap.png
    results/data/factor_correlations.csv
    results/data/factor_loadings.csv
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy.stats import pearsonr
from sklearn.decomposition import FactorAnalysis

from tasks.t0125_t0123_cluster_factor_mi_atp.code.cluster_helpers import (
    PooledStandardiser,
    load_standardiser,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.constants import (
    ALL_PARAM_NAMES,
    CHART_DPI,
    JOINT_FACTOR_R_THRESHOLD,
    KAISER_FACTOR_CAP,
    N_TOTAL_DIMS,
    RANDOM_SEED,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.load_t0123_cells import (
    ATP_PER_SPIKE_COLUMN,
    DSI_COLUMN,
    MI_COLUMN,
    PD_COLUMN,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.paths import (
    FACTOR_CORRELATIONS_CSV,
    FACTOR_LOADINGS_CSV,
    FACTOR_LOADINGS_HEATMAP_PNG,
    T0123_CELLS_PARQUET,
    T0123_STANDARDISER_NPZ,
)

VARIMAX_GAMMA: float = 1.0
VARIMAX_TOL: float = 1e-6
VARIMAX_MAX_ITER: int = 500
EPS_STD: float = 1e-8


def varimax_rotation(
    *,
    loadings: NDArray[np.float64],
    gamma: float = VARIMAX_GAMMA,
    tol: float = VARIMAX_TOL,
    max_iter: int = VARIMAX_MAX_ITER,
) -> NDArray[np.float64]:
    """Apply Kaiser varimax rotation via iterative SVD (gamma=1.0, copied from t0117)."""
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
    n_eig_above_one: int
    eigenvalues: list[float]
    loadings_full: NDArray[np.float64]
    scores: NDArray[np.float64]
    kept_param_indices: list[int]
    kept_param_names: list[str]
    var_explained_per_factor: list[float]
    total_var_explained: float


@dataclass(frozen=True, slots=True)
class _DropConstantResult:
    matrix: NDArray[np.float64]
    kept_indices: list[int]
    kept_names: list[str]


def _drop_constant_columns(*, matrix: NDArray[np.float64]) -> _DropConstantResult:
    sigma: NDArray[np.float64] = matrix.std(axis=0, ddof=0)
    keep_mask: NDArray[np.bool_] = sigma >= EPS_STD
    kept_indices: list[int] = [int(i) for i in np.where(keep_mask)[0]]
    kept_names: list[str] = [ALL_PARAM_NAMES[i] for i in kept_indices]
    return _DropConstantResult(
        matrix=matrix[:, keep_mask],
        kept_indices=kept_indices,
        kept_names=kept_names,
    )


def run_factor_analysis(
    *,
    z_matrix: NDArray[np.float64],
    factor_cap: int = KAISER_FACTOR_CAP,
) -> FactorResult:
    """Run FA + varimax on a pre-standardised matrix; Kaiser cut via correlation eigenvalues."""
    dropped = _drop_constant_columns(matrix=z_matrix)
    kept_matrix: NDArray[np.float64] = dropped.matrix
    corr: NDArray[np.float64] = np.cov(kept_matrix, rowvar=False, ddof=0)
    eigvals_full: NDArray[np.float64] = np.linalg.eigvalsh(corr)[::-1]
    n_eig_above_one: int = int((eigvals_full > 1.0).sum())
    n_factors: int = max(1, min(n_eig_above_one, factor_cap))

    fa = FactorAnalysis(n_components=n_factors, rotation=None, random_state=RANDOM_SEED)
    fa.fit(kept_matrix)
    unrotated_loadings: NDArray[np.float64] = fa.components_.T.astype(np.float64)
    rotated_kept: NDArray[np.float64] = varimax_rotation(loadings=unrotated_loadings)
    loadings_full: NDArray[np.float64] = np.full(
        (N_TOTAL_DIMS, n_factors), fill_value=np.nan, dtype=np.float64
    )
    for local_idx, full_idx in enumerate(dropped.kept_indices):
        loadings_full[full_idx, :] = rotated_kept[local_idx, :]
    rotated_scores: NDArray[np.float64] = (
        kept_matrix @ rotated_kept @ np.linalg.pinv(rotated_kept.T @ rotated_kept)
    )

    sum_sq_per_factor: NDArray[np.float64] = (rotated_kept**2).sum(axis=0)
    var_explained_per_factor: list[float] = [
        float(s / len(dropped.kept_indices)) for s in sum_sq_per_factor
    ]
    total_var_explained: float = float(sum(var_explained_per_factor))

    return FactorResult(
        n_factors=n_factors,
        n_eig_above_one=n_eig_above_one,
        eigenvalues=[float(v) for v in eigvals_full],
        loadings_full=loadings_full,
        scores=rotated_scores,
        kept_param_indices=dropped.kept_indices,
        kept_param_names=dropped.kept_names,
        var_explained_per_factor=var_explained_per_factor,
        total_var_explained=total_var_explained,
    )


def _plot_loadings_heatmap(*, loadings_full: NDArray[np.float64]) -> None:
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
    ax.set_title(
        f"Varimax factor loadings on 68 parameters (n_factors={n_factors}, t0123 full cohort)"
    )
    plt.colorbar(im, ax=ax, label="loading")
    fig.tight_layout()
    FACTOR_LOADINGS_HEATMAP_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FACTOR_LOADINGS_HEATMAP_PNG, dpi=CHART_DPI)
    plt.close(fig)


def _classify_factor(
    *,
    r_mi: float,
    r_atp: float,
    r_dsi: float,
    r_pd: float,
    threshold: float,
) -> str:
    mi_loaded: bool = abs(r_mi) > threshold
    atp_loaded: bool = abs(r_atp) > threshold
    dsi_loaded: bool = abs(r_dsi) > threshold
    pd_loaded: bool = abs(r_pd) > threshold
    if mi_loaded and atp_loaded and dsi_loaded:
        return "joint_mi_atp_dsi"
    if mi_loaded and atp_loaded and pd_loaded:
        return "joint_mi_atp_pd"
    if mi_loaded and atp_loaded:
        return "joint_mi_atp"
    if dsi_loaded and pd_loaded:
        return "joint_dsi_pd"
    if mi_loaded:
        return "mi_only"
    if atp_loaded:
        return "atp_only"
    if dsi_loaded:
        return "dsi_only"
    if pd_loaded:
        return "pd_only"
    return "none"


def main() -> None:
    df: pd.DataFrame = pd.read_parquet(T0123_CELLS_PARQUET)
    standardiser: PooledStandardiser = load_standardiser(path=T0123_STANDARDISER_NPZ)
    matrix_68d: NDArray[np.float64] = df[list(ALL_PARAM_NAMES)].to_numpy(dtype=np.float64)
    z_full: NDArray[np.float64] = standardiser.transform(matrix_68d)
    mi: NDArray[np.float64] = df[MI_COLUMN].to_numpy(dtype=np.float64)
    atp: NDArray[np.float64] = df[ATP_PER_SPIKE_COLUMN].to_numpy(dtype=np.float64)
    dsi: NDArray[np.float64] = df[DSI_COLUMN].to_numpy(dtype=np.float64)
    pd_rate: NDArray[np.float64] = df[PD_COLUMN].to_numpy(dtype=np.float64)
    print(f"FA matrix shape={z_full.shape}", flush=True)

    result: FactorResult = run_factor_analysis(z_matrix=z_full)
    print(
        f"\nKaiser eigenvalues > 1: {result.n_eig_above_one} (cap = {KAISER_FACTOR_CAP})",
        flush=True,
    )
    print(f"n_factors retained: {result.n_factors}", flush=True)
    print(f"Total variance explained: {result.total_var_explained:.4f}", flush=True)

    _plot_loadings_heatmap(loadings_full=result.loadings_full)
    print(f"Wrote {FACTOR_LOADINGS_HEATMAP_PNG}", flush=True)

    loadings_df: pd.DataFrame = pd.DataFrame(
        result.loadings_full,
        index=list(ALL_PARAM_NAMES),
        columns=[f"F{i + 1}" for i in range(result.n_factors)],
    )
    loadings_df.to_csv(FACTOR_LOADINGS_CSV)
    print(f"Wrote {FACTOR_LOADINGS_CSV}", flush=True)

    corr_rows: list[dict[str, object]] = []
    for f_idx in range(result.n_factors):
        col: NDArray[np.float64] = result.scores[:, f_idx]
        r_mi, p_mi = pearsonr(col, mi)
        r_atp, p_atp = pearsonr(col, atp)
        r_dsi, p_dsi = pearsonr(col, dsi)
        r_pd, p_pd = pearsonr(col, pd_rate)
        joint_flag: bool = (
            abs(float(r_mi)) > JOINT_FACTOR_R_THRESHOLD
            and abs(float(r_atp)) > JOINT_FACTOR_R_THRESHOLD
        )
        classification: str = _classify_factor(
            r_mi=float(r_mi),
            r_atp=float(r_atp),
            r_dsi=float(r_dsi),
            r_pd=float(r_pd),
            threshold=JOINT_FACTOR_R_THRESHOLD,
        )
        corr_rows.append(
            {
                "factor_id": f"F{f_idx + 1}",
                "variance_explained": result.var_explained_per_factor[f_idx],
                "r_mi": float(r_mi),
                "p_mi": float(p_mi),
                "r_atp": float(r_atp),
                "p_atp": float(p_atp),
                "r_dsi": float(r_dsi),
                "p_dsi": float(p_dsi),
                "r_pd": float(r_pd),
                "p_pd": float(p_pd),
                "joint_mi_atp_flag": bool(joint_flag),
                "factor_classification": classification,
            }
        )
    corr_df: pd.DataFrame = pd.DataFrame(corr_rows)
    corr_df.to_csv(FACTOR_CORRELATIONS_CSV, index=False)
    print(f"Wrote {FACTOR_CORRELATIONS_CSV}", flush=True)
    print(corr_df.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
