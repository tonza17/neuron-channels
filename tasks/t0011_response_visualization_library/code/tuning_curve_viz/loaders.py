"""Thin wrappers around the ``tuning_curve_loss`` library CSV loader.

Re-exports :func:`load_tuning_curve` and :class:`TuningCurve` so callers never need to
import the t0012 library directly. Adds a permissive angle-grid validator that accepts
8, 12, or 16 uniform angles (in contrast to the strict 12-angle validator in t0012).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants import (
    ACCEPTED_ANGLE_COUNTS,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader import (
    TuningCurve,
    load_tuning_curve,
)

__all__ = [
    "TuningCurve",
    "load_curve",
    "load_tuning_curve",
    "validate_angle_grid",
]


def load_curve(*, csv_path: Path) -> TuningCurve:
    """Load a tuning curve from ``csv_path`` via the t0012 canonical loader.

    Thin re-export wrapper; see
    ``tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader.load_tuning_curve``
    for the schema details.
    """
    return load_tuning_curve(csv_path=csv_path)


def validate_angle_grid(*, angles_deg: np.ndarray) -> None:
    """Permissive angle-grid validator for the viz library.

    Accepts any of the counts in :data:`ACCEPTED_ANGLE_COUNTS` as long as the grid is
    uniform. Raises :class:`ValueError` on non-uniform grids or on unaccepted counts.
    The viz library does not call this on the raw :func:`load_tuning_curve` return value
    (the t0012 loader already enforces 12-angle grids); it is exposed so that downstream
    callers who want to handle heterogeneous grids can check before plotting.
    """
    assert angles_deg.ndim == 1, "angles_deg is 1-D"
    n_angles: int = len(angles_deg)
    if n_angles not in ACCEPTED_ANGLE_COUNTS:
        raise ValueError(
            f"Unsupported angle-grid size {n_angles}; "
            f"accepted counts are {ACCEPTED_ANGLE_COUNTS}. "
            f"Angles: {angles_deg.tolist()!r}"
        )
    diffs: np.ndarray = np.diff(angles_deg)
    expected_step: float = 360.0 / n_angles
    if not np.allclose(diffs, expected_step, atol=1e-6):
        raise ValueError(
            f"Non-uniform angle grid (expected step {expected_step:.4f} deg); "
            f"diffs are {diffs.tolist()!r}"
        )
