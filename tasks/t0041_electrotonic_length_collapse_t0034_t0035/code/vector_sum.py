# Copied from tasks/t0034_distal_dendrite_length_sweep_t0024/code/analyse_sweep.py
# lines 80-99 (function ``_vector_sum_dsi``) per the cross-task import rule: only
# assets/library/ code can be imported across tasks; analyse_sweep.py is not a library
# asset, so the helper is duplicated here with identical semantics.
"""Mazurek vector-sum DSI helper used for cross-check re-derivation of DSI.

t0041 consumes DSI values that are already present in the upstream per-multiplier metrics CSVs,
so this helper is not on the critical path. It is kept here for traceability and for any future
sanity-check that re-derives DSI from raw per-angle mean firing rates.
"""

from __future__ import annotations

import math


def vector_sum_dsi(
    *,
    angles_deg: list[int],
    rates_hz: list[float],
) -> tuple[float, float]:
    """Return ``(dsi, preferred_dir_deg)`` using the Mazurek vector-sum convention."""
    real_part: float = 0.0
    imag_part: float = 0.0
    rate_sum: float = 0.0
    for angle, rate in zip(angles_deg, rates_hz, strict=True):
        theta: float = math.radians(angle)
        real_part += rate * math.cos(theta)
        imag_part += rate * math.sin(theta)
        rate_sum += rate
    if rate_sum <= 0.0:
        return (0.0, float("nan"))
    magnitude: float = math.hypot(real_part, imag_part)
    dsi: float = magnitude / rate_sum
    preferred_dir_deg: float = math.degrees(math.atan2(imag_part, real_part)) % 360.0
    return (dsi, preferred_dir_deg)
