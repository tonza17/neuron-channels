"""Constants for t0067 channel-density sweep."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ChannelKind(StrEnum):
    NONE = "none"
    NAV16 = "Nav1.6"
    NAP = "NaP"
    NAR = "NaR"
    KV3 = "Kv3"
    KV4 = "Kv4"


class DensityLabel(StrEnum):
    NONE = "n/a"
    LOW = "low"
    MED = "med"
    HIGH = "high"


class Direction(StrEnum):
    PD = "PD"
    ND = "ND"


@dataclass(frozen=True, slots=True)
class ChannelDef:
    kind: ChannelKind
    suffix: str
    densities_mS_cm2: dict[DensityLabel, float]


CHANNEL_DEFS: tuple[ChannelDef, ...] = (
    ChannelDef(
        kind=ChannelKind.NAV16,
        suffix="nav16t67",
        densities_mS_cm2={DensityLabel.LOW: 10.0, DensityLabel.MED: 30.0, DensityLabel.HIGH: 90.0},
    ),
    ChannelDef(
        kind=ChannelKind.NAP,
        suffix="napt67",
        densities_mS_cm2={DensityLabel.LOW: 0.3, DensityLabel.MED: 0.8, DensityLabel.HIGH: 2.4},
    ),
    ChannelDef(
        kind=ChannelKind.NAR,
        suffix="nart67",
        densities_mS_cm2={DensityLabel.LOW: 3.0, DensityLabel.MED: 8.0, DensityLabel.HIGH: 24.0},
    ),
    ChannelDef(
        kind=ChannelKind.KV3,
        suffix="kv3t67",
        densities_mS_cm2={DensityLabel.LOW: 7.0, DensityLabel.MED: 20.0, DensityLabel.HIGH: 60.0},
    ),
    ChannelDef(
        kind=ChannelKind.KV4,
        suffix="kv4t67",
        densities_mS_cm2={DensityLabel.LOW: 4.0, DensityLabel.MED: 12.0, DensityLabel.HIGH: 36.0},
    ),
)

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
