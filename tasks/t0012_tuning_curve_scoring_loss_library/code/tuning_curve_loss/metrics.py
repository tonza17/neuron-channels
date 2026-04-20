"""Tuning-curve metrics: DSI, peak, null, HWHM, and split-half reliability.

Formulas mirror t0004 ``compute_dsi`` so ``compute_dsi(target) == analytical_dsi`` to within
machine precision. HWHM uses linear interpolation on the 6 angles on each side of the peak and
returns the mean of the two half-widths; for a flat curve it returns 180.0.
"""

from __future__ import annotations

import numpy as np

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader import (
    TuningCurve,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.paths import (
    ANGLE_STEP_DEG,
)

FLAT_HWHM_DEG: float = 180.0
FULL_CIRCLE_DEG: float = 360.0


def _preferred_index(*, curve: TuningCurve) -> int:
    return int(np.argmax(curve.firing_rates_hz))


def _null_index(*, curve: TuningCurve) -> int:
    n: int = curve.firing_rates_hz.shape[0]
    return (_preferred_index(curve=curve) + n // 2) % n


def compute_peak_hz(*, curve: TuningCurve) -> float:
    return float(np.max(curve.firing_rates_hz))


def compute_null_hz(*, curve: TuningCurve) -> float:
    null_idx: int = _null_index(curve=curve)
    return float(curve.firing_rates_hz[null_idx])


def compute_dsi(*, curve: TuningCurve) -> float:
    r_pref: float = compute_peak_hz(curve=curve)
    r_null: float = compute_null_hz(curve=curve)
    denom: float = r_pref + r_null
    if denom == 0.0:
        return 0.0
    return float((r_pref - r_null) / denom)


def compute_hwhm_deg(*, curve: TuningCurve) -> float:
    """Linear-interpolation HWHM on a rotated 12-angle grid.

    Rotates the firing-rate vector so the peak sits at index ``n//2``; then on each side the
    rate is monotone decreasing (for any well-behaved tuning curve). Linear interpolation finds
    the angular distance from the peak where rate == ``(peak + null)/2``; the returned value is
    the average of the two sides. If the curve is flat (peak == null) returns ``180.0``.
    """
    rates: np.ndarray = curve.firing_rates_hz
    n: int = rates.shape[0]
    peak: float = float(np.max(rates))
    null: float = compute_null_hz(curve=curve)
    if peak == null:
        return FLAT_HWHM_DEG

    half_max: float = (peak + null) / 2.0
    pref_idx: int = _preferred_index(curve=curve)
    target_idx: int = n // 2
    shift: int = target_idx - pref_idx
    rotated: np.ndarray = np.roll(rates, shift=shift)

    # Offsets in degrees from the peak: -180, -150, ..., 0, ..., +150.
    offsets_deg: np.ndarray = (np.arange(n) - target_idx) * ANGLE_STEP_DEG

    # Right side: indices target_idx ... target_idx + n//2 (monotone decreasing to null).
    right_rates: np.ndarray = rotated[target_idx : target_idx + n // 2 + 1]
    right_offsets: np.ndarray = offsets_deg[target_idx : target_idx + n // 2 + 1]

    # Left side: indices target_idx ... target_idx - n//2 (reverse so increasing offsets).
    # We want offsets going from 0 to +180 on the "left" (mirrored).
    left_rates: np.ndarray = rotated[: target_idx + 1][::-1]
    left_offsets_abs: np.ndarray = (-offsets_deg[: target_idx + 1])[::-1]

    def _half_width(
        *,
        rates_side: np.ndarray,
        offsets_side: np.ndarray,
    ) -> float:
        # rates_side is decreasing in ``offsets_side`` (from peak to null).
        # We need the offset at which rates_side crosses ``half_max``.
        # Use np.interp, which needs the xp (offsets) to be increasing in the value we query.
        # Since rates are decreasing, invert: treat rate as x-axis, offset as y.
        # Sort by rate ascending for np.interp.
        order: np.ndarray = np.argsort(rates_side)
        xp: np.ndarray = rates_side[order]
        fp: np.ndarray = offsets_side[order]
        # Defend against a plateau at half_max: np.interp handles ties by linear interpolation.
        return float(np.interp(x=half_max, xp=xp, fp=fp))

    right_hwhm: float = _half_width(rates_side=right_rates, offsets_side=right_offsets)
    left_hwhm: float = _half_width(rates_side=left_rates, offsets_side=left_offsets_abs)
    return (right_hwhm + left_hwhm) / 2.0


def compute_reliability(*, curve: TuningCurve) -> float | None:
    """Split-half Pearson correlation between even- and odd-trial means.

    Returns ``None`` if no trials are available, fewer than 2 trials, or either split has zero
    variance (Pearson r undefined). Result is clamped to [0, 1].
    """
    trials: np.ndarray | None = curve.trials
    if trials is None:
        return None
    n_trials: int = trials.shape[1]
    if n_trials < 2:
        return None
    even: np.ndarray = trials[:, 0::2].mean(axis=1)
    odd: np.ndarray = trials[:, 1::2].mean(axis=1)
    if even.std() == 0.0 or odd.std() == 0.0:
        return None
    with np.errstate(invalid="ignore"):
        r: float = float(np.corrcoef(even, odd)[0, 1])
    if np.isnan(r):
        return None
    # Clamp to [0, 1] per project convention.
    return max(0.0, min(1.0, r))
