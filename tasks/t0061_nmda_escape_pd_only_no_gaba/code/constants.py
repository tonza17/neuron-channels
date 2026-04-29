"""Sweep parameters for t0061 (NMDA-only, GABA = 0, theta = 0 deg)."""

from __future__ import annotations

GABA_BASE_NS: float = 0.0
ANGLE_DEG: int = 0
N_TRIALS: int = 1
GNMDA_NS_VALUES: tuple[float, ...] = (0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0)
