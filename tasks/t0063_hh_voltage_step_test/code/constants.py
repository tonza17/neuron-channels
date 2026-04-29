"""Voltage-step protocol parameters for t0063."""

from __future__ import annotations

TARGET_MV_VALUES: tuple[float, ...] = (-60.0, -50.0, -40.0, -30.0, -20.0, -10.0)
HOLD_MV: float = -65.0
DUR1_MS: float = 50.0  # initial hold at HOLD_MV
DUR2_MS: float = 200.0  # voltage step
DUR3_MS: float = 50.0  # post-step return
TSTOP_MS: float = 300.0
RS_MOHM: float = 0.001  # tight clamp
DT_MS: float = 0.025
