"""Constants for t0069 AIS-localised channel sweep."""

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

# AIS section properties (per t0019 priors).
AIS_LENGTH_UM: float = 30.0
AIS_DIAM_UM: float = 1.0
AIS_NSEG: int = 5
AIS_GNABAR_S_CM2: float = 0.030  # 30 mS/cm^2
AIS_GKBAR_S_CM2: float = 0.020  # 20 mS/cm^2
AIS_GKMBAR_S_CM2: float = 0.003  # 3 mS/cm^2

# Axon section properties.
AXON_LENGTH_UM: float = 1000.0
AXON_DIAM_UM: float = 1.0
AXON_NSEG: int = 50
AXON_GNABAR_S_CM2: float = 0.005  # 5 mS/cm^2
AXON_GKBAR_S_CM2: float = 0.003  # 3 mS/cm^2
AXON_GKMBAR_S_CM2: float = 0.003

# Passive properties for AIS + axon (matched to t0008 cell defaults).
PASSIVE_RA_OHM_CM: float = 100.0
PASSIVE_CM_UF_CM2: float = 1.0
PASSIVE_GLEAK_S_CM2: float = 5e-5
PASSIVE_ELEAK_MV: float = -60.0

METRIC_KEY_DSI: str = "direction_selectivity_index"
