"""Extra tuning-curve metrics not provided by the t0012 ``tuning_curve_loss`` library.

Adds vector-sum DSI and the preferred-direction angle (degrees) computed from the per-angle mean
firing rates as the magnitude / angle of the complex sum of unit-radius vectors weighted by rate.
"""

from __future__ import annotations

import numpy as np

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (
    TuningCurve,
)


def compute_vector_sum_dsi(*, curve: TuningCurve) -> float:
    """Vector-sum DSI: ``|sum_k r_k * exp(i * theta_k)| / sum_k r_k``.

    Returns 0.0 if the rate sum is zero.
    """
    angles_rad: np.ndarray = np.deg2rad(curve.angles_deg)
    rates: np.ndarray = curve.firing_rates_hz
    total_rate: float = float(np.sum(rates))
    if total_rate == 0.0:
        return 0.0
    complex_sum: complex = complex(np.sum(rates * np.exp(1j * angles_rad)))
    return float(abs(complex_sum) / total_rate)


def compute_preferred_direction_deg(*, curve: TuningCurve) -> float:
    """Preferred-direction angle in degrees from the complex sum of (rate, angle).

    Returns 0.0 if the rate sum is zero. Result is wrapped to [0, 360).
    """
    angles_rad: np.ndarray = np.deg2rad(curve.angles_deg)
    rates: np.ndarray = curve.firing_rates_hz
    total_rate: float = float(np.sum(rates))
    if total_rate == 0.0:
        return 0.0
    complex_sum: complex = complex(np.sum(rates * np.exp(1j * angles_rad)))
    angle_deg: float = float(np.rad2deg(np.angle(complex_sum)))
    if angle_deg < 0.0:
        angle_deg += 360.0
    return angle_deg
