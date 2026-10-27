"""Part 1 calibration: fit (s_Na, s_K) to voltage-clamp ratios ONLY.

This module deliberately uses no spike or firing quantity and imports nothing from the
current-clamp module (a structural unit test checks that). Inputs are per-grid-point clamp
metrics: sustained outward current and isolated Na transient; targets are their ratios to the
(1.0, 1.0) reference run on the same cell.
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.interpolate import RegularGridInterpolator
from scipy.optimize import minimize

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    LOSS_SCALE_SUSTAINED,
    LOSS_SCALE_TRANSIENT,
    MAX_SUSTAINED_FAIL_THRESHOLD,
    S_K_GRID,
    S_NA_GRID,
    SUSTAINED_RATIO_TOLERANCE,
    TARGET_SUSTAINED_RATIO,
    TARGET_TRANSIENT_RATIO,
)


@dataclass(frozen=True, slots=True)
class GridPoint:
    s_na: float
    s_k: float
    sustained_na: float
    na_transient_na: float


@dataclass(frozen=True, slots=True)
class RatioGrids:
    sustained: NDArray[np.float64]
    transient: NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class CellFit:
    cell_id: str
    s_na_fit: float
    s_k_fit: float
    pred_sustained_ratio: float
    pred_transient_ratio: float
    loss: float
    grid_best_s_na: float
    grid_best_s_k: float
    grid_best_loss: float
    max_grid_sustained_ratio: float
    failed_sustained_reach: bool


def ratio_grids(*, points: list[GridPoint]) -> RatioGrids:
    by_key: dict[str, GridPoint] = {f"{p.s_na:.4f}|{p.s_k:.4f}": p for p in points}
    ref = by_key["1.0000|1.0000"]
    assert ref.sustained_na > 0.0, "reference sustained current is positive (outward)"
    assert ref.na_transient_na < 0.0, "reference Na transient is inward (negative)"
    sus = np.zeros((len(S_NA_GRID), len(S_K_GRID)), dtype=np.float64)
    tra = np.zeros_like(sus)
    for i, sn in enumerate(S_NA_GRID):
        for j, sk in enumerate(S_K_GRID):
            p = by_key[f"{sn:.4f}|{sk:.4f}"]
            sus[i, j] = p.sustained_na / ref.sustained_na
            tra[i, j] = p.na_transient_na / ref.na_transient_na
    return RatioGrids(sustained=sus, transient=tra)


def loss_value(*, sustained_ratio: float, transient_ratio: float, target_transient: float) -> float:
    a = (sustained_ratio - TARGET_SUSTAINED_RATIO) / LOSS_SCALE_SUSTAINED
    b = (transient_ratio - target_transient) / LOSS_SCALE_TRANSIENT
    return float(a * a + b * b)


def fit_cell(
    *,
    cell_id: str,
    grids: RatioGrids,
    target_transient: float = TARGET_TRANSIENT_RATIO,
) -> CellFit:
    loss_grid = np.zeros_like(grids.sustained)
    for i in range(loss_grid.shape[0]):
        for j in range(loss_grid.shape[1]):
            loss_grid[i, j] = loss_value(
                sustained_ratio=float(grids.sustained[i, j]),
                transient_ratio=float(grids.transient[i, j]),
                target_transient=target_transient,
            )
    flat_idx = int(np.argmin(loss_grid))
    bi, bj = np.unravel_index(flat_idx, loss_grid.shape)
    grid_best_loss = float(loss_grid[bi, bj])
    interp_s = RegularGridInterpolator(
        (np.array(S_NA_GRID), np.array(S_K_GRID)), np.log(grids.sustained)
    )
    interp_t = RegularGridInterpolator(
        (np.array(S_NA_GRID), np.array(S_K_GRID)), np.log(grids.transient)
    )

    def objective(x: NDArray[np.float64]) -> float:
        pt = np.array([[x[0], x[1]]], dtype=np.float64)
        s = float(np.exp(interp_s(pt)[0]))
        t = float(np.exp(interp_t(pt)[0]))
        return loss_value(sustained_ratio=s, transient_ratio=t, target_transient=target_transient)

    bounds = [(S_NA_GRID[0], S_NA_GRID[-1]), (S_K_GRID[0], S_K_GRID[-1])]
    order = np.argsort(loss_grid, axis=None)[:4]
    best_x: NDArray[np.float64] = np.array([S_NA_GRID[int(bi)], S_K_GRID[int(bj)]])
    best_f: float = grid_best_loss
    for idx in order:
        ii, jj = np.unravel_index(int(idx), loss_grid.shape)
        x0 = np.array([S_NA_GRID[int(ii)], S_K_GRID[int(jj)]], dtype=np.float64)
        res = minimize(objective, x0, method="Nelder-Mead", bounds=bounds)
        if float(res.fun) < best_f:
            best_f = float(res.fun)
            best_x = np.asarray(res.x, dtype=np.float64)
    pt = np.array([[best_x[0], best_x[1]]], dtype=np.float64)
    max_s = float(grids.sustained.max())
    return CellFit(
        cell_id=cell_id,
        s_na_fit=float(best_x[0]),
        s_k_fit=float(best_x[1]),
        pred_sustained_ratio=float(np.exp(interp_s(pt)[0])),
        pred_transient_ratio=float(np.exp(interp_t(pt)[0])),
        loss=best_f,
        grid_best_s_na=S_NA_GRID[int(bi)],
        grid_best_s_k=S_K_GRID[int(bj)],
        grid_best_loss=grid_best_loss,
        max_grid_sustained_ratio=max_s,
        failed_sustained_reach=max_s < MAX_SUSTAINED_FAIL_THRESHOLD,
    )


def within_tolerance(*, sustained_ratio: float) -> bool:
    return abs(sustained_ratio - TARGET_SUSTAINED_RATIO) <= SUSTAINED_RATIO_TOLERANCE
