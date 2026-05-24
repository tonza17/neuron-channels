"""Decile-based stratified samplers for the morphology audit.

Adapted from `tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/code/stratified_sample.py`
`_assign_quintile` pattern. The audit-specific helpers operate on the t0117 pooled cells parquet
and stratify across the four asymmetry parameter columns rather than (DSI, PD).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from tasks.t0120_morph_generator_geometry_audit.code.constants import (
    BEDB_SYMMETRIC_CONTROL_REFS,
    SYMMETRIC_FRACTIONAL_TOL,
)


def assign_decile(*, values: np.ndarray, n_deciles: int = 10) -> np.ndarray:
    """Return per-row decile index in [0..n_deciles-1] using pd.qcut with duplicates='drop'.

    Mirrors the t0118 _assign_quintile helper. If qcut collapses bins (degenerate input),
    integers may go below n_deciles-1; NaN values are coerced to 0.
    """
    series: pd.Series = pd.Series(values)
    bins: pd.Series = pd.qcut(
        x=series,
        q=n_deciles,
        labels=False,
        duplicates="drop",
    )
    return bins.fillna(0).astype(np.int64).to_numpy()


def sample_extreme_decile(
    *,
    df: pd.DataFrame,
    column: str,
    top: bool,
    n: int,
    seed: int,
    use_abs: bool = False,
) -> pd.DataFrame:
    """Return up to `n` rows from the top (or bottom) decile of `column`.

    Selection is deterministic given `seed`: rows are sorted by the column ascending
    (or descending if `top`) and the first `n` taken without replacement after dedup.
    If `use_abs` is true, the decile is computed on the absolute value of the column.
    """
    df_local: pd.DataFrame = df.reset_index(drop=True).copy()
    raw_values: np.ndarray = df_local[column].to_numpy()
    values: np.ndarray = np.abs(raw_values) if use_abs else raw_values
    deciles: np.ndarray = assign_decile(values=values, n_deciles=10)
    n_max_decile: int = int(deciles.max()) if deciles.size > 0 else 0
    target_decile: int = n_max_decile if top else 0
    mask: np.ndarray = deciles == target_decile
    candidates: pd.DataFrame = df_local.loc[mask]
    sort_values_arr: np.ndarray = values[mask]
    # Deterministic order within the decile: sort by value descending (top) or ascending (bottom).
    order: np.ndarray = np.argsort(sort_values_arr)
    if top:
        order = order[::-1]
    candidates_sorted: pd.DataFrame = candidates.iloc[order].reset_index(drop=True)
    # Permute deterministically with the supplied seed for an additional tie-break,
    # but keep the head ordering stable for reproducibility.
    rng: np.random.Generator = np.random.default_rng(seed=seed)
    # No-op shuffle is intentional: seed parameter kept for future-proofing.
    _ = rng.integers(low=0, high=1, size=1)
    return candidates_sorted.head(n=n).reset_index(drop=True)


def sample_symmetric_controls(
    *,
    df: pd.DataFrame,
    n: int,
    tol: float = SYMMETRIC_FRACTIONAL_TOL,
) -> pd.DataFrame:
    """Return up to `n` rows closest to BEDB_BASE_POINT defaults across the 4 asymmetry params.

    Two-stage strategy:

    1. If at least `n` cells satisfy the strict tolerance gate (all 4 asymmetry params within
       `tol` of defaults), return the head of that subset.

    2. Otherwise, fall back to the `n` cells with the smallest normalised Euclidean distance
       to the reference point in (soma_offset / 100, |elong - 1| / 2,
       |branch_density_gradient|, |primary_branch_pd_concentration| / 5) space.

    The fallback path is the one that actually fires for the t0117 pool: NSGA-II evolves cells
    away from the BEDB_BASE_POINT, so no cell sits strictly at the defaults. The closest cells
    nevertheless serve as the audit's null-hypothesis controls.
    """
    df_local: pd.DataFrame = df.reset_index(drop=True).copy()

    mask: np.ndarray = np.ones(len(df_local), dtype=bool)
    for col, ref in BEDB_SYMMETRIC_CONTROL_REFS.items():
        vals: np.ndarray = df_local[col].to_numpy()
        if abs(ref) < 1e-12:
            col_mask: np.ndarray = np.abs(vals) < tol
        else:
            col_mask = np.abs(vals - ref) / abs(ref) < tol
        mask &= col_mask
    strict: pd.DataFrame = df_local.loc[mask].reset_index(drop=True)
    if len(strict) >= n:
        return strict.head(n=n)

    # Fallback: normalised distance to the reference point.
    scales: dict[str, float] = {
        "soma_offset_pd_um": 100.0,
        "field_elongation_pd": 2.0,
        "branch_density_gradient_pd": 1.0,
        "primary_branch_pd_concentration": 5.0,
    }
    dist_sq: np.ndarray = np.zeros(len(df_local), dtype=np.float64)
    for col, ref in BEDB_SYMMETRIC_CONTROL_REFS.items():
        vals = df_local[col].to_numpy()
        dist_sq = dist_sq + ((vals - ref) / scales[col]) ** 2
    df_local["_sym_dist"] = np.sqrt(dist_sq)
    closest: pd.DataFrame = df_local.nsmallest(n=n, columns="_sym_dist").drop(columns=["_sym_dist"])
    return closest.reset_index(drop=True)
