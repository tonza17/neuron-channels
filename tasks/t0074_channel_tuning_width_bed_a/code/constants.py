"""Constants for t0074 channel tuning-width sweep on Bed A."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ChannelKind(StrEnum):
    BASELINE = "baseline"
    NAV16 = "Nav1.6"
    NAP = "NaP"
    NAR = "NaR"
    KV3 = "Kv3"
    KV4 = "Kv4"
    BK = "BK"
    SK = "SK"
    KV7 = "Kv7"


class DensityLabel(StrEnum):
    NONE = "n/a"
    LOW = "low"
    MED = "med"
    HIGH = "high"


class TrialMode(StrEnum):
    FULL = "FULL"
    EPSP_PASSIVE = "EPSP_PASSIVE"
    IPSP_PASSIVE = "IPSP_PASSIVE"


@dataclass(frozen=True, slots=True)
class ChannelDef:
    kind: ChannelKind
    suffix: str
    gbar_attr: str
    low_ms_cm2: float
    med_ms_cm2: float
    high_ms_cm2: float

    def density_for(self, *, label: DensityLabel) -> float:
        if label == DensityLabel.LOW:
            return self.low_ms_cm2
        if label == DensityLabel.MED:
            return self.med_ms_cm2
        if label == DensityLabel.HIGH:
            return self.high_ms_cm2
        raise ValueError(f"Unsupported density label for value lookup: {label}")


# 8 channels: 5 forked from t0067 (suffix renamed from *t67 to *t74) plus 3 newly
# vendored {BK, SK, Kv7}. Densities for the 5 t0067 channels match t0067 exactly.
CHANNEL_DEFS: tuple[ChannelDef, ...] = (
    ChannelDef(
        kind=ChannelKind.NAV16,
        suffix="nav16t74",
        gbar_attr="gbar_nav16t74",
        low_ms_cm2=10.0,
        med_ms_cm2=30.0,
        high_ms_cm2=90.0,
    ),
    ChannelDef(
        kind=ChannelKind.NAP,
        suffix="napt74",
        gbar_attr="gbar_napt74",
        low_ms_cm2=0.3,
        med_ms_cm2=0.8,
        high_ms_cm2=2.4,
    ),
    ChannelDef(
        kind=ChannelKind.NAR,
        suffix="nart74",
        gbar_attr="gbar_nart74",
        low_ms_cm2=3.0,
        med_ms_cm2=8.0,
        high_ms_cm2=24.0,
    ),
    ChannelDef(
        kind=ChannelKind.KV3,
        suffix="kv3t74",
        gbar_attr="gbar_kv3t74",
        low_ms_cm2=7.0,
        med_ms_cm2=20.0,
        high_ms_cm2=60.0,
    ),
    ChannelDef(
        kind=ChannelKind.KV4,
        suffix="kv4t74",
        gbar_attr="gbar_kv4t74",
        low_ms_cm2=4.0,
        med_ms_cm2=12.0,
        high_ms_cm2=36.0,
    ),
    ChannelDef(
        kind=ChannelKind.BK,
        suffix="bk74",
        gbar_attr="gbar_bk74",
        low_ms_cm2=0.3,
        med_ms_cm2=1.0,
        high_ms_cm2=3.0,
    ),
    ChannelDef(
        kind=ChannelKind.SK,
        suffix="sk74",
        gbar_attr="gbar_sk74",
        low_ms_cm2=0.06,
        med_ms_cm2=0.2,
        high_ms_cm2=0.6,
    ),
    ChannelDef(
        kind=ChannelKind.KV7,
        suffix="kv7t74",
        gbar_attr="gbar_kv7t74",
        low_ms_cm2=0.0001,
        med_ms_cm2=0.001,
        high_ms_cm2=0.005,
    ),
)


# All channel suffixes registered in this task's nrnmech.dll (8 channels + cad).
ALL_CHANNEL_SUFFIXES: tuple[str, ...] = tuple(ch.suffix for ch in CHANNEL_DEFS)
CALCIUM_POOL_SUFFIX: str = "cad"

# gabaMOD-swap protocol values (used by Stage 2 regression gate only).
GABA_MOD_PD: float = 0.33
GABA_MOD_ND: float = 0.99
GABA_MOD_OFF: float = 0.0
ACH_MOD_OFF: float = 0.0

# Synaptic conductance overrides for passive modes (per t0065 protocol).
B_AMPA_OFF_NS: float = 0.0
B_NMDA_OFF_NS: float = 0.0
S_GABA_OFF_NS: float = 0.0
S_ACH_OFF_NS: float = 0.0

# exptype values: 1 = HH on (FULL); 2 = HH off (passive PSP measurements).
EXPTYPE_HH_ON: int = 1
EXPTYPE_HH_OFF: int = 2

# 12-angle bar-rotation protocol parameters (Bed A native).
N_ANGLES: int = 12
ANGLE_STEP_DEG: float = 30.0
N_SEEDS_FULL: int = 5
N_SEEDS_PASSIVE: int = 1
SEED_BASE: int = 1

# Trial timing.
TSTOP_MS: float = 1000.0
BASELINE_END_MS: float = 100.0
AP_THRESHOLD_MV: float = -10.0

# Instability thresholds.
INSTABILITY_VM_MAX: float = 60.0
INSTABILITY_VM_MIN: float = -80.0

# Stage 2 regression gate values.
# Source: tasks/t0067_t0065_soma_channel_addition_sweep/results/metrics.json
T0067_BASELINE_DSI: float = 0.7974683544303798
REGRESSION_TOLERANCE: float = 1e-3

# HWHM null-out threshold per Chen 2009 convention (sub-1 Hz curves).
LOW_RATE_HZ_THRESHOLD: float = 1.0

# Pass criterion thresholds (REQ-19).
DELTA_HWHM_THRESHOLD_DEG: float = 5.0
DELTA_VECTOR_SUM_DSI_THRESHOLD: float = 0.05

# Per-trial CSV column names.
COL_CONDITION_ID: str = "condition_id"
COL_CHANNEL_KIND: str = "channel_kind"
COL_DENSITY_LABEL: str = "density_label"
COL_DENSITY_MS_CM2: str = "density_ms_cm2"
COL_ANGLE_DEG: str = "angle_deg"
COL_TRIAL_SEED: str = "trial_seed"
COL_TRIAL_MODE: str = "trial_mode"
COL_N_SPIKES: str = "n_spikes"
COL_FIRING_RATE_HZ: str = "firing_rate_hz"
COL_PEAK_VM_MV: str = "peak_vm_mv"
COL_BASELINE_VM_MV: str = "baseline_vm_mv"
COL_IS_UNSTABLE: str = "is_unstable"

# Tuning-curves CSV (canonical t0012 schema).
COL_TC_ANGLE_DEG: str = "angle_deg"
COL_TC_TRIAL_SEED: str = "trial_seed"
COL_TC_FIRING_RATE_HZ: str = "firing_rate_hz"

# Metrics summary CSV column names.
COL_PEAK_HZ: str = "peak_hz"
COL_NULL_HZ: str = "null_hz"
COL_DSI_PD_ND: str = "dsi_pd_nd"
COL_HWHM_DEG: str = "hwhm_deg"
COL_VECTOR_SUM_DSI: str = "vector_sum_dsi"
COL_PD_ANGLE_DEG: str = "pd_angle_deg"
COL_RATE_AT_PD_HZ: str = "rate_at_pd_hz"
COL_RATE_AT_ND_HZ: str = "rate_at_nd_hz"
COL_RMSE_VS_T0004: str = "rmse_vs_t0004"
COL_TUNING_CURVE_RELIABILITY: str = "tuning_curve_reliability"
COL_DELTA_HWHM_DEG: str = "delta_hwhm_deg"
COL_DELTA_VECTOR_SUM_DSI: str = "delta_vector_sum_dsi"
COL_IS_INERT: str = "is_inert"

# Registered project metric keys (must match meta/metrics/).
METRIC_KEY_DSI: str = "direction_selectivity_index"
METRIC_KEY_HWHM: str = "tuning_curve_hwhm_deg"
METRIC_KEY_RELIABILITY: str = "tuning_curve_reliability"
METRIC_KEY_RMSE: str = "tuning_curve_rmse"

BASELINE_CONDITION_ID: str = "baseline"
