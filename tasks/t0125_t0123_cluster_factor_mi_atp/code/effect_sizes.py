"""Non-parametric effect-size helpers (Cliff's delta)."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def cliffs_delta(x: NDArray[np.float64], y: NDArray[np.float64]) -> float:
    """Cliff's delta = (#x>y - #x<y) / (n_x * n_y).

    Uses sorted-y + np.searchsorted for O((n_x + n_y) log n_y) time. Ties contribute 0 to
    numerator (neither #greater nor #less); this is the canonical ties-aware definition.
    """
    n_x: int = len(x)
    n_y: int = len(y)
    if n_x == 0 or n_y == 0:
        return float("nan")
    y_sorted: NDArray[np.float64] = np.sort(np.asarray(y, dtype=np.float64))
    # For each x_i: searchsorted(y, x_i, "left") = #y_j < x_i; "right" = #y_j <= x_i.
    less_counts: NDArray[np.int64] = np.searchsorted(y_sorted, x, side="left").astype(np.int64)
    le_counts: NDArray[np.int64] = np.searchsorted(y_sorted, x, side="right").astype(np.int64)
    # #y_j < x_i (x_i strictly greater than y_j)
    n_x_gt_y: int = int(less_counts.sum())
    # #y_j == x_i counts:
    n_x_eq_y: int = int((le_counts - less_counts).sum())
    # #y_j > x_i (x_i strictly less than y_j) = n_y - le_counts
    n_x_lt_y: int = int((n_y - le_counts).sum())
    # Sanity: n_x_gt_y + n_x_eq_y + n_x_lt_y == n_x * n_y
    assert n_x_gt_y + n_x_eq_y + n_x_lt_y == n_x * n_y
    return float(n_x_gt_y - n_x_lt_y) / float(n_x * n_y)
