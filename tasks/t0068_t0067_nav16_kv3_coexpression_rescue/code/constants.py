"""Constants for t0068 Nav1.6+Kv3 co-expression rescue."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Direction(StrEnum):
    PD = "PD"
    ND = "ND"


@dataclass(frozen=True, slots=True)
class Condition:
    condition_id: str
    nav16_mS_cm2: float
    kv3_mS_cm2: float


# 9 conditions: baseline + Nav1.6 anchors x Kv3 sweep.
CONDITIONS: tuple[Condition, ...] = (
    Condition(condition_id="baseline", nav16_mS_cm2=0.0, kv3_mS_cm2=0.0),
    Condition(condition_id="nav16_med", nav16_mS_cm2=30.0, kv3_mS_cm2=0.0),
    Condition(condition_id="nav16_med_kv3_low", nav16_mS_cm2=30.0, kv3_mS_cm2=7.0),
    Condition(condition_id="nav16_med_kv3_med", nav16_mS_cm2=30.0, kv3_mS_cm2=20.0),
    Condition(condition_id="nav16_med_kv3_high", nav16_mS_cm2=30.0, kv3_mS_cm2=60.0),
    Condition(condition_id="nav16_high", nav16_mS_cm2=90.0, kv3_mS_cm2=0.0),
    Condition(condition_id="nav16_high_kv3_low", nav16_mS_cm2=90.0, kv3_mS_cm2=7.0),
    Condition(condition_id="nav16_high_kv3_med", nav16_mS_cm2=90.0, kv3_mS_cm2=20.0),
    Condition(condition_id="nav16_high_kv3_high", nav16_mS_cm2=90.0, kv3_mS_cm2=60.0),
)

# All 5 mechanism suffixes get inserted on the soma; only Nav1.6 + Kv3 may be non-zero.
ALL_MECH_SUFFIXES: tuple[str, ...] = ("nav16t67", "napt67", "nart67", "kv3t67", "kv4t67")
NAV16_SUFFIX: str = "nav16t67"
KV3_SUFFIX: str = "kv3t67"

GABA_MOD_PD: float = 0.33
GABA_MOD_ND: float = 0.99
N_SEEDS_PER_CONDITION: int = 5
SEED_BASE: int = 1
TSTOP_MS: float = 1000.0
AP_THRESHOLD_MV: float = -10.0
BASELINE_WINDOW_MS: float = 50.0

INSTABILITY_PEAK_HIGH_MV: float = 60.0
INSTABILITY_PEAK_LOW_MV: float = -80.0

METRIC_KEY_DSI: str = "direction_selectivity_index"
