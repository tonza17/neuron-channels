"""Canonical constants for t0057 (tonic GABA + amplitude sweep on t0053 spatial DSGC).

Adapted from t0053 ``constants.py``. The GABA Exp2Syn kinetics constants are removed (the new
``gaba_tonic`` POINT_PROCESS uses a sustained envelope, not a dual-exponential decay), and three
new constants are added: ``GABA_BASE_NS_VALUES`` (the swept conductance values), ``T_ON_MS`` /
``T_OFF_MS`` (the tonic window edges), and ``GABA_RAMP_MS`` (the optional cosine-ramp width).

All numeric parameters are pinned here per the task description and plan. No code outside this
module hardcodes simulation parameters.
"""

from __future__ import annotations

from enum import StrEnum

# ----------------------------------------------------------------------
# Simulation timing.
# ----------------------------------------------------------------------
TSTOP_MS: float = 1500.0
DT_MS: float = 0.025
CELSIUS_DEG_C: float = 36.0
V_INIT_MV: float = -65.0
AP_THRESHOLD_MV: float = -20.0


# ----------------------------------------------------------------------
# Bar stimulus geometry.
# ----------------------------------------------------------------------
BAR_WIDTH_UM: float = 200.0
# Bar speed: spec says 1000 um/s == 1.0 um/ms.
BAR_VELOCITY_UM_PER_MS: float = 1.0
ANGLES_DEG: tuple[int, ...] = (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)
N_TRIALS_PER_ANGLE: int = 10
BASE_OFFSET_MS: float = 100.0


# ----------------------------------------------------------------------
# Synapse placement.
# ----------------------------------------------------------------------
N_PAIRS: int = 100
PLACEMENT_SEED: int = 0


# ----------------------------------------------------------------------
# Passive cable parameters.
# ----------------------------------------------------------------------
RM_OHM_CM2: float = 5999.0
RA_OHM_CM: float = 100.0
CM_UF_PER_CM2: float = 1.0


# ----------------------------------------------------------------------
# Synthetic axon initial segment (SWC has no axon).
# ----------------------------------------------------------------------
AIS_LENGTH_UM: float = 30.0
AIS_DIAMETER_UM: float = 2.0
AIS_GNABAR_S_PER_CM2: float = 1.2
AIS_GKBAR_S_PER_CM2: float = 0.04
AIS_GL_S_PER_CM2: float = 0.008
AIS_EL_HH_MV: float = -65.0


# ----------------------------------------------------------------------
# AMPA Exp2Syn parameters (unchanged from t0053; bit-identical AMPA path).
# ----------------------------------------------------------------------
AMPA_TAU1_MS: float = 0.5
AMPA_TAU2_MS: float = 2.5
AMPA_E_MV: float = 0.0
AMPA_PEAK_NS: float = 0.5


# ----------------------------------------------------------------------
# Tonic GABA mechanism parameters (NEW vs t0053).
# ----------------------------------------------------------------------
GABA_E_MV: float = -75.0
# Tonic-window edges (ms): GABA conductance is on for active synapses across the full stimulus
# presentation interval minus the BASE_OFFSET buffer.
T_ON_MS: float = 100.0
T_OFF_MS: float = 1400.0
# Optional cosine ramp width at the window edges (ms) to avoid integrator step-function artefacts.
GABA_RAMP_MS: float = 1.0
# Swept per-synapse peak conductance values (nS). Used by the outer loop in run_tuning_curve.py.
GABA_BASE_NS_VALUES: tuple[float, ...] = (0.25, 0.5, 1.0, 1.5, 2.0)


# ----------------------------------------------------------------------
# Spatial gating soft sanity bounds for the cross-direction mean active fraction (carried over
# from t0053; the spatial-gating predicate is unchanged so the bounds apply identically).
# ----------------------------------------------------------------------
ACTIVE_FRACTION_LOWER: float = 0.4
ACTIVE_FRACTION_UPPER: float = 0.6


# ----------------------------------------------------------------------
# IPSP-sustained-window regression (REQ-13). The most-active direction was empirically
# theta = 210 deg in t0053; the gate asserts |v(1300) - V_init| >= ratio * |v(200) - V_init|.
# ----------------------------------------------------------------------
IPSP_SUSTAINED_THETA_DEG: int = 210
IPSP_SUSTAINED_RATIO: float = 0.5
IPSP_SUSTAINED_T_EARLY_MS: float = 200.0
IPSP_SUSTAINED_T_LATE_MS: float = 1300.0


# ----------------------------------------------------------------------
# AMPA_ONLY no-regression sentinel (REQ-14).
# ----------------------------------------------------------------------
AMPA_ONLY_PEAK_HZ_EXPECTED: float = 0.6667
AMPA_ONLY_PEAK_HZ_TOLERANCE: float = 1e-3


# ----------------------------------------------------------------------
# Bootstrap sentinel env-var (renamed per task to avoid collision).
# ----------------------------------------------------------------------
NEURONHOME_SENTINEL_ENV: str = "_T0057_NEURONHOME_BOOTSTRAPPED"


# ----------------------------------------------------------------------
# Metric registry keys (registered under meta/metrics/).
# ----------------------------------------------------------------------
METRIC_KEY_DSI: str = "direction_selectivity_index"
METRIC_KEY_HWHM: str = "tuning_curve_hwhm_deg"
METRIC_KEY_RELIABILITY: str = "tuning_curve_reliability"
METRIC_KEY_RMSE: str = "tuning_curve_rmse"


# ----------------------------------------------------------------------
# CSV column names.
# ----------------------------------------------------------------------
COL_GABA_BASE_NS: str = "gaba_base_ns"
COL_ANGLE_DEG: str = "angle_deg"
COL_TRIAL_SEED: str = "trial_seed"
COL_TRIAL_INDEX: str = "trial_index"
COL_FIRING_RATE_HZ: str = "firing_rate_hz"
COL_SPIKE_TIME_S: str = "spike_time_s"
COL_SAMPLE_IDX: str = "sample_idx"
COL_T_MS: str = "t_ms"
COL_VOLTAGE_MV: str = "voltage_mv"
COL_SYNAPSE_INDEX: str = "synapse_index"
COL_ONSET_TIME_MS: str = "onset_time_ms"
COL_IS_FIRED: str = "is_fired"
COL_ACTIVE_FRACTION: str = "active_fraction"


# ----------------------------------------------------------------------
# Trial mode enumeration.
# ----------------------------------------------------------------------
class TrialMode(StrEnum):
    FULL = "full"
    AMPA_ONLY = "ampa_only"
    GABA_ONLY = "gaba_only"
