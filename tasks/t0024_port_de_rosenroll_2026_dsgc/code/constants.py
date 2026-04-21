"""Canonical constants for the t0024 de Rosenroll 2026 DSGC port.

Values are taken from the [dsMicro-GH] companion code (commit
``a23f642aa6557a23a51bf76f51e420e8149773fa``) at
``https://github.com/geoffder/ds-circuit-ei-microarchitecture``. Code values are
authoritative when the paper text disagrees with the code (see
``research/research_internet.md`` for the full audit).
"""

from __future__ import annotations

import os

# NEURON install location on this workstation.
NEURONHOME_DEFAULT: str = r"C:\Users\md1avn\nrn-8.2.7"
os.environ.setdefault("NEURONHOME", NEURONHOME_DEFAULT)

# Simulation timing (authoritative: upstream ei_balance.py Model defaults).
CELSIUS_DEG_C: float = 36.9
DT_MS: float = 0.1
STEPS_PER_MS: float = 10.0
TSTOP_MS: float = 1000.0
V_INIT_MV: float = -60.0
AP_THRESHOLD_MV: float = -10.0

# Passive cable properties (upstream Model.set_default_params, code-authoritative).
RA_OHM_CM: float = 100.0
CM_UF_CM2: float = 1.0
GLEAK_S_CM2: float = 0.0001667  # 1.667e-4 S/cm^2 from ei_balance.py
ELEAK_MV: float = -60.0

# Active channel densities per compartment class (upstream ei_balance.py
# defaults in S/cm^2; plan constants are expressed in mS/cm^2 for consistency).
GBAR_NA_SOMA_MS_CM2: float = 150.0  # 0.15 S/cm^2
GBAR_NA_PRIMARY_MS_CM2: float = 200.0  # 0.20 S/cm^2
GBAR_NA_DISTAL_MS_CM2: float = 30.0  # 0.03 S/cm^2
GBAR_K_SOMA_MS_CM2: float = 35.0  # 0.035 S/cm^2
GBAR_K_PRIMARY_MS_CM2: float = 35.0  # 0.035 S/cm^2 (upstream uses same as soma)
GBAR_K_DISTAL_MS_CM2: float = 25.0  # 0.025 S/cm^2
GBAR_KM_SOMA_MS_CM2: float = 3.0  # 0.003 S/cm^2
GBAR_KM_PRIMARY_MS_CM2: float = 3.0
GBAR_KM_DISTAL_MS_CM2: float = 3.0

# Synaptic kinetics / reversals (upstream synprops).
ACH_TAU1_MS: float = 0.1
ACH_TAU2_MS: float = 4.0
ACH_EREV_MV: float = 0.0
ACH_WEIGHT_US: float = 0.001  # NetCon weight for E synapses (uS)

GABA_TAU1_MS: float = 0.5
GABA_TAU2_MS: float = 12.0
GABA_EREV_MV: float = -60.0
GABA_WEIGHT_US: float = 0.003
GABA_SCALE_UNCORRELATED: float = 1.8  # per plan REQ-5 / research spec

NMDA_TAU1_MS: float = 2.0
NMDA_TAU2_MS: float = 7.0
NMDA_EREV_MV: float = 0.0
NMDA_WEIGHT_US: float = 0.0015
NMDA_N: float = 0.25
NMDA_GAMMA: float = 0.08

# Calcium decay (cadecay.mod default).
CA_DECAY_TAU_MS: float = 10.0

# AR(2) release-rate noise process (plan REQ-1).
AR2_PHI: tuple[float, float] = (0.9, -0.1)
AR2_CROSS_CORR_RHO_CORRELATED: float = 0.6
AR2_CROSS_CORR_RHO_UNCORRELATED: float = 0.0
AR2_INNOV_SCALE: float = 1.0
AR2_BASE_RATE_HZ: float = 50.0  # baseline firing rate for release process

# Briggman connectome / spatial offsets (paper methods).
SAC_SOMA_MIN_OFFSET_UM: float = 30.0
AMB_DECAY_TAU_UM: float = 27.0

# Moving-bar stimulus geometry (upstream light_bar defaults).
BAR_VELOCITY_UM_PER_MS: float = 1.0
BAR_WIDTH_UM: float = 250.0
BAR_X_START_UM: float = -40.0
BAR_X_END_UM: float = 200.0
BAR_Y_START_UM: float = 25.0
BAR_Y_END_UM: float = 225.0
BAR_START_TIME_MS: float = 0.0

# Direction sweeps.
ANGLES_8DIR_DEG: tuple[int, ...] = (0, 45, 90, 135, 180, 225, 270, 315)
ANGLES_12ANG_DEG: tuple[int, ...] = tuple(range(0, 360, 30))
N_TRIALS_PER_ANGLE: int = 20

# Paper-text alternatives (recorded for sensitivity-sweep only; NOT used by
# the main driver). See research/research_internet.md for the audit.
RA_OHM_CM_PAPER_TEXT: float = 200.0
ELEAK_MV_PAPER_TEXT: float = -70.0

# Scoring / metric keys (registered under meta/metrics/).
METRIC_KEY_DSI: str = "direction_selectivity_index"
METRIC_KEY_HWHM: str = "tuning_curve_hwhm_deg"
METRIC_KEY_RELIABILITY: str = "tuning_curve_reliability"
METRIC_KEY_RMSE: str = "tuning_curve_rmse"

# Task-local metric keys for port-fidelity gate (plan REQ-5).
METRIC_KEY_DSI_CORR_8DIR: str = "de_rosenroll_dsi_correlated_8dir"
METRIC_KEY_DSI_UNCORR_8DIR: str = "de_rosenroll_dsi_uncorrelated_8dir"
METRIC_KEY_DSI_CORR_12ANG: str = "de_rosenroll_dsi_correlated_12ang"
METRIC_KEY_DSI_UNCORR_12ANG: str = "de_rosenroll_dsi_uncorrelated_12ang"
METRIC_KEY_PEAK_CORR_8DIR: str = "de_rosenroll_peak_hz_correlated_8dir"
METRIC_KEY_PEAK_UNCORR_8DIR: str = "de_rosenroll_peak_hz_uncorrelated_8dir"
METRIC_KEY_PORT_FIDELITY_PASS: str = "de_rosenroll_port_fidelity_gate_pass"

# Port-fidelity gate thresholds (plan REQ-5).
PORT_FIDELITY_DSI_CORR_MIN: float = 0.30
PORT_FIDELITY_DSI_CORR_MAX: float = 0.50
PORT_FIDELITY_DSI_UNCORR_MIN: float = 0.18
PORT_FIDELITY_DSI_UNCORR_MAX: float = 0.35
PORT_FIDELITY_DSI_DROP_MIN_FRAC: float = 0.20

# Upstream commit SHA for provenance.
DE_ROSENROLL_COMMIT_SHA: str = "a23f642aa6557a23a51bf76f51e420e8149773fa"
