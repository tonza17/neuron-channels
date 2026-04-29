"""Canonical constants for t0059 (bar-arrival-locked tonic GABA + AMPA sweep on t0057 substrate).

Adapted from ``tasks/t0057_tonic_gaba_sweep_t0053/code/constants.py``. Five edits per the t0059
plan:

* ``TSTOP_MS = 1500.0`` -> ``TSTOP_MS = 1400.0`` (S-0055-01 protocol fix).
* ``TrialMode`` members renamed: ``AMPA_ONLY`` / ``GABA_ONLY`` -> ``EPSP_PASSIVE`` /
  ``IPSP_PASSIVE`` (HH save-and-zero protocol fix).
* ``GABA_BASE_NS_VALUES`` rebound from ``(0.25, 0.5, 1.0, 1.5, 2.0)`` to
  ``(0.1, 0.2, 0.5, 1.0, 2.0)`` (lower-conductance regime where AMPA escape is plausible).
* ``AMPA_PEAK_NS_VALUES = (0.5, 1.0, 2.0, 3.0, 4.0)`` added (the new outer-loop axis).
* ``WINDOW_MS = 200.0`` added (per-synapse bar-arrival-locked window width).
* ``T_OFF_MS`` dropped (window edges are now per-synapse, computed in ``synapses.py``).
* ``IPSP_SUSTAINED_*`` and ``AMPA_ONLY_PEAK_HZ_EXPECTED`` regression sentinels dropped (these are
  direction-dependent under bar-locked windows; replaced by the bar-locked IPSP envelope test).
* ``COL_GAMPA_NS`` added for the new CSV column.

The bootstrap sentinel env-var is renamed ``_T0059_NEURONHOME_BOOTSTRAPPED`` to avoid cross-task
re-exec collisions.
"""

from __future__ import annotations

from enum import StrEnum

# ----------------------------------------------------------------------
# Simulation timing.
# ----------------------------------------------------------------------
TSTOP_MS: float = 1400.0
DT_MS: float = 0.025
CELSIUS_DEG_C: float = 36.0
V_INIT_MV: float = -65.0
AP_THRESHOLD_MV: float = -20.0
# Passive-mode peak-Vm sanity gate: HH off limits Vm strictly below E_AMPA = 0 mV. Allow a
# small headroom (5 mV) for numerical overshoot. A trip of this gate indicates HH save-and-zero
# is wired incorrectly; AP_THRESHOLD_MV is too strict for passive responses at high gAMPA where
# 100 synapses x 4 nS x (0 - V_rest) drives the soma close to the synaptic reversal.
EPSP_PASSIVE_PEAK_VM_GATE_MV: float = 5.0


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
# AMPA Exp2Syn parameters (unchanged from t0057; bit-identical AMPA path).
# AMPA_PEAK_NS is the legacy default value; the t0059 sweep overrides it via the public
# AMPA_PEAK_NS_VALUES constant in run_tuning_curve.py.
# ----------------------------------------------------------------------
AMPA_TAU1_MS: float = 0.5
AMPA_TAU2_MS: float = 2.5
AMPA_E_MV: float = 0.0
AMPA_PEAK_NS: float = 0.5

# Outer-loop AMPA peak conductance values (nS) — REQ-7. Threaded through schedule_ei_onsets,
# run_one_trial, and run_full_sweep as the new ``gampa_ns`` parameter.
AMPA_PEAK_NS_VALUES: tuple[float, ...] = (0.5, 1.0, 2.0, 3.0, 4.0)


# ----------------------------------------------------------------------
# Tonic GABA mechanism parameters.
# ----------------------------------------------------------------------
GABA_E_MV: float = -75.0
# Per-synapse window width (ms) — REQ-1. The window opens at each synapse's bar-arrival time
# (computed in synapses.py from the synapse coordinate and stimulus angle) and closes at
# t_on_i + WINDOW_MS.
WINDOW_MS: float = 200.0
# Optional cosine ramp width at the window edges (ms) to avoid integrator step-function artefacts.
GABA_RAMP_MS: float = 1.0
# Swept per-synapse peak conductance values (nS). Used by the inner GABA loop in run_tuning_curve.
GABA_BASE_NS_VALUES: tuple[float, ...] = (0.1, 0.2, 0.5, 1.0, 2.0)


# ----------------------------------------------------------------------
# Spatial gating soft sanity bounds for the cross-direction mean active fraction (carried over
# from t0053 / t0057; the spatial-gating predicate is unchanged so the bounds apply identically).
# ----------------------------------------------------------------------
ACTIVE_FRACTION_LOWER: float = 0.4
ACTIVE_FRACTION_UPPER: float = 0.6


# ----------------------------------------------------------------------
# Bootstrap sentinel env-var (renamed per task to avoid cross-task re-exec collision).
# ----------------------------------------------------------------------
NEURONHOME_SENTINEL_ENV: str = "_T0059_NEURONHOME_BOOTSTRAPPED"


# ----------------------------------------------------------------------
# Metric registry keys (registered under meta/metrics/).
# ----------------------------------------------------------------------
METRIC_KEY_DSI: str = "direction_selectivity_index"
METRIC_KEY_HWHM: str = "tuning_curve_hwhm_deg"
METRIC_KEY_RELIABILITY: str = "tuning_curve_reliability"
METRIC_KEY_RMSE: str = "tuning_curve_rmse"


# ----------------------------------------------------------------------
# CSV column names. ``COL_GAMPA_NS`` is the new leading column for the 5x5 grid CSVs.
# ----------------------------------------------------------------------
COL_GAMPA_NS: str = "gampa_ns"
COL_GABA_BASE_NS: str = "gaba_base_ns"
COL_ANGLE_DEG: str = "angle_deg"
COL_TRIAL_SEED: str = "trial_seed"
COL_TRIAL_INDEX: str = "trial_index"
COL_FIRING_RATE_HZ: str = "firing_rate_hz"
COL_SPIKE_TIME_S: str = "spike_time_s"
COL_SAMPLE_IDX: str = "sample_idx"
COL_T_MS: str = "t_ms"
COL_VOLTAGE_MV: str = "voltage_mv"
COL_ACTIVE_FRACTION: str = "active_fraction"


# ----------------------------------------------------------------------
# Trial mode enumeration. ``EPSP_PASSIVE`` and ``IPSP_PASSIVE`` save-and-zero the HH conductances
# on the soma and AIS (per the S-0055-01 measurement-protocol fix); FULL keeps them active.
# ----------------------------------------------------------------------
class TrialMode(StrEnum):
    FULL = "full"
    EPSP_PASSIVE = "epsp_passive"
    IPSP_PASSIVE = "ipsp_passive"
