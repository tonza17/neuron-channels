"""Sweep parameters for t0062 (NMDA + AMPA-priming, GABA = 0, theta = 0)."""

from __future__ import annotations

GABA_BASE_NS: float = 0.0
GAMPA_PRIMING_NS: float = 0.5
ANGLE_DEG: int = 0
N_TRIALS: int = 1
GNMDA_NS_VALUES: tuple[float, ...] = (0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0)

AMPA_TAU1_MS: float = 0.5
AMPA_TAU2_MS: float = 2.5
AMPA_REVERSAL_MV: float = 0.0
