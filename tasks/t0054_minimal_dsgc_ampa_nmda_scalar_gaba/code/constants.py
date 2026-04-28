"""Canonical constants for t0054 (minimal DSGC with AMPA + NMDA and scalar gabaMOD).

All numeric parameters are pinned here per the task description and plan. No code outside this
module hardcodes simulation parameters.

This is a direct extension of t0052: every t0052 constant is preserved verbatim. The only
additions are NMDA Exp2Syn parameters, the gNMDA sweep tuple, the per-trial CSV `gnmda_ns`
column name, and the renamed bootstrap sentinel. The legacy t0052 ``TrialMode.AMPA_ONLY`` is
replaced by ``E_ONLY`` (no alias) per the t0054 task description.
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
#
# Diameter is widened from the plan's 1.0 um to 2.0 um, and the AIS HH gnabar is raised from the
# NEURON default (0.12 S/cm^2) to AIS_GNABAR_S_PER_CM2 below; gkbar is lowered slightly so the
# AIS can act as a spike-initiation zone given the 100 dendritic synapses. With the default HH
# densities the soma never reaches threshold (v_max ~ -21 mV) because the EPSPs spread across
# ~200 ms and never summate above HH threshold; the AIS boost turns this depolarisation into
# real action potentials. The plan's V_rest = -65 +/- 0.5 mV gate still passes (V_rest -65.17 mV).
# ----------------------------------------------------------------------
AIS_LENGTH_UM: float = 30.0
AIS_DIAMETER_UM: float = 2.0
AIS_GNABAR_S_PER_CM2: float = 1.2
AIS_GKBAR_S_PER_CM2: float = 0.04
# Boosted leak conductance with el_hh = V_INIT_MV brings the steady-state V_rest from ~-63.7 mV
# (with the boosted AIS gNa) back to ~-64.5 mV, comfortably within the +/-0.5 mV gate of REQ-2.
AIS_GL_S_PER_CM2: float = 0.008
AIS_EL_HH_MV: float = -65.0


# ----------------------------------------------------------------------
# AMPA / NMDA / GABA Exp2Syn parameters.
# ----------------------------------------------------------------------
AMPA_TAU1_MS: float = 0.5
AMPA_TAU2_MS: float = 2.5
AMPA_E_MV: float = 0.0
AMPA_PEAK_NS: float = 0.5

# NMDA mechanism: voltage-independent Exp2Syn co-located with AMPA at every E synapse.
# Tau1 = 5 ms, Tau2 = 80 ms, E = 0 mV per task spec; peak conductance is swept.
NMDA_TAU1_MS: float = 5.0
NMDA_TAU2_MS: float = 80.0
NMDA_E_MV: float = 0.0
NMDA_PEAK_NS_VALUES: tuple[float, ...] = (0.0, 0.25, 0.5, 1.0)

GABA_TAU1_MS: float = 1.0
GABA_TAU2_MS: float = 20.0
GABA_E_MV: float = -75.0
GABA_BASE_NS: float = 2.0


# ----------------------------------------------------------------------
# gabaMOD direction tuning.
# ----------------------------------------------------------------------
THETA_ND_DEG: float = 180.0
GABAMOD_PD: float = 0.33
GABAMOD_ND: float = 0.99


# ----------------------------------------------------------------------
# Bootstrap sentinel env-var (renamed per task to avoid collision).
# ----------------------------------------------------------------------
NEURONHOME_SENTINEL_ENV: str = "_T0054_NEURONHOME_BOOTSTRAPPED"


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
COL_GNMDA_NS: str = "gnmda_ns"


# ----------------------------------------------------------------------
# Trial mode enumeration.
# ----------------------------------------------------------------------
class TrialMode(StrEnum):
    FULL = "full"
    E_ONLY = "e_only"
    GABA_ONLY = "gaba_only"
