"""Canonical constants for the t0020 gabaMOD-swap port.

Re-exports the canonical paper parameters from t0008's library (no
duplication of values) and adds the gabaMOD-swap-specific constants that
only make sense in the two-condition protocol.
"""

from __future__ import annotations

from enum import StrEnum

from tasks.t0008_port_modeldb_189347.code.constants import (
    AP_THRESHOLD_MV,
    DT_MS,
    GABA_MOD,
    TSTOP_MS,
    V_INIT_MV,
)

# Re-exports from t0008 (imported for downstream use by the driver).
__all__ = [
    "AP_THRESHOLD_MV",
    "DSI_ENVELOPE",
    "DT_MS",
    "GABA_MOD",
    "GABA_MOD_ND",
    "GABA_MOD_PD",
    "N_TRIALS_PER_CONDITION",
    "PEAK_ENVELOPE_HZ",
    "TSTOP_MS",
    "V_INIT_MV",
    "Condition",
]


# gabaMOD-swap protocol constants.
GABA_MOD_PD: float = 0.33
GABA_MOD_ND: float = 0.99

# Default trial count per condition (total trials = 2 * N_TRIALS_PER_CONDITION).
N_TRIALS_PER_CONDITION: int = 20

# Unwidened literature envelope (Poleg-Polsky & Diamond 2016).
DSI_ENVELOPE: tuple[float, float] = (0.70, 0.85)
PEAK_ENVELOPE_HZ: tuple[float, float] = (40.0, 80.0)

# Score report protocol name.
PROTOCOL_NAME: str = "gabamod_swap"

# CSV column names for data/tuning_curves.csv.
CONDITION_COLUMN: str = "condition"
TRIAL_SEED_COLUMN: str = "trial_seed"
FIRING_RATE_COLUMN: str = "firing_rate_hz"

# Metric keys for results/metrics.json.
METRIC_KEY_DSI: str = "dsi"
METRIC_KEY_PEAK_HZ: str = "peak_hz"
METRIC_KEY_MEAN_PD_HZ: str = "mean_pd_hz"
METRIC_KEY_MEAN_ND_HZ: str = "mean_nd_hz"
METRIC_KEY_GATE_PASSED: str = "gate_passed"


class Condition(StrEnum):
    """Two-condition labels used in data/tuning_curves.csv."""

    PD = "PD"
    ND = "ND"
