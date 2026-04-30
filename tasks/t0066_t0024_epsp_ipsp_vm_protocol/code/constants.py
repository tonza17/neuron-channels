"""Constants for t0066 (de Rosenroll EPSP/IPSP/FULL protocol)."""

from __future__ import annotations

from enum import StrEnum


class TrialMode(StrEnum):
    FULL = "FULL"
    EPSP_PASSIVE = "EPSP_PASSIVE"
    IPSP_PASSIVE = "IPSP_PASSIVE"


class Condition(StrEnum):
    PD = "PD"
    ND = "ND"


DIRECTION_PD_DEG: float = 0.0
DIRECTION_ND_DEG: float = 180.0

N_TRIALS_PER_CELL: int = 20
SEED_BASE: int = 1
RHO_CORRELATED: float = 0.6

MODE_COLUMN: str = "mode"
DIRECTION_COLUMN: str = "direction"
TRIAL_COLUMN: str = "trial"
T_MS_COLUMN: str = "t_ms"
V_MV_COLUMN: str = "v_mv"
CSV_COLUMNS: list[str] = [
    MODE_COLUMN,
    DIRECTION_COLUMN,
    TRIAL_COLUMN,
    T_MS_COLUMN,
    V_MV_COLUMN,
]

METRIC_KEY_DSI: str = "direction_selectivity_index"

PEAK_V_MV_KEY: str = "peak_v_mv"
BASELINE_V_MV_KEY: str = "baseline_v_mv"
PEAK_MINUS_BASELINE_KEY: str = "peak_minus_baseline_mv"
SPIKE_COUNT_KEY: str = "spike_count"
N_SAMPLES_KEY: str = "n_samples"

BASELINE_WINDOW_MS: float = 50.0

CSV_SUBSAMPLE_STRIDE: int = 10
