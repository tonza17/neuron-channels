"""Canonical constants for the t0022 DSGC dendritic-computation port.

Values inherit verbatim from t0008's ``constants.py`` (Poleg-Polsky & Diamond
2016 source ``main.hoc``, commit ``87d669dcef18e9966e29c88520ede78bc16d36ff``)
plus the per-dendrite E-I scheduler constants that this task introduces.

New constants are grounded in ``research/research_papers.md`` (Park 2014 E-I
conductance priors, Koch-Poggio 1982/1983 on-the-path timing window) and
``research/research_internet.md`` (ModelDB community conventions).
"""

from __future__ import annotations

import os

# NEURON install location on this workstation (validated by t0007, reused by t0008/t0020).
NEURONHOME_DEFAULT: str = r"C:\Users\md1avn\nrn-8.2.7"
os.environ.setdefault("NEURONHOME", NEURONHOME_DEFAULT)

# Simulation timing (from main.hoc, unchanged from t0008).
TSTOP_MS: float = 1000.0
DT_MS: float = 0.1
CELSIUS_DEG_C: float = 32.0

# Poleg-Polsky NMDA kinetics (unchanged from t0008).
TAU1_NMDA_BIP_MS: float = 60.0
E_SAC_INHIB_MV: float = -60.0

# Stimulus geometry (unchanged from t0008).
LIGHTSPEED_UM_PER_MS: float = 1.0
LIGHTWIDTH_UM: float = 500.0
LIGHTSTART_MS: float = -100.0
LIGHT_X_START_UM: float = -100.0
LIGHT_X_END_UM: float = 200.0
LIGHT_Y_START_UM: float = -130.0
LIGHT_Y_END_UM: float = 100.0
LIGHT_REVERSE: int = 0

# Synaptic conductances used by the underlying HOC model (unchanged).
B2GAMPA_NS: float = 0.25
B2GNMDA_NS: float = 0.5
S2GGABA_NS: float = 0.5
S2GACH_NS: float = 0.5
GABA_MOD: float = 0.33
ACH_MOD: float = 0.25
V_SHIFT_HHST_MV: float = -4.0
N_NMDA_V_DEP: float = 0.3
GAMMA_NMDA_V_DEP: float = 0.07
R_SYN_CHANCE: float = 1.0

# Simulation grid (matches the t0022 12-angle sweep plan).
N_ANGLES: int = 12
N_TRIALS: int = 10
ANGLE_STEP_DEG: float = 30.0

# AP detection threshold for firing-rate counting (unchanged).
AP_THRESHOLD_MV: float = -10.0

# Resting potential for initialization (unchanged).
V_INIT_MV: float = -65.0

# Per-dendrite E-I scheduler constants (NEW to t0022).
# Sign convention: positive offset means I arrives *after* E (E leads I).
# Preferred direction: E leads I by +10 ms (open window before shunt).
# Null direction: I leads E by 10 ms (shunt arrives first, vetoes E).
# Values within [Koch-Poggio 1982/1983] 5-20 ms window; midpoint pick per
# research_internet.md "Methodology Insights" testable hypothesis.
EI_OFFSET_PREFERRED_MS: float = 10.0
EI_OFFSET_NULL_MS: float = -10.0
EI_OFFSET_BAND_MS: tuple[float, float] = (5.0, 20.0)

# Per-dendrite conductances (nS). E is direction-untuned per Park2014.
# I scales with null/preferred ratio 4x (preserved: 12 / 3 = 4).
# Values calibrated empirically against the t0008 baseline: each Exp2Syn
# receives only N_SYN_EVENTS short events per trial (vs. the bundled
# Poleg-Polsky BIPsyn which emits ~20 evoked events per second of bar
# sweep). Preferred GABA is held well below Park2014's single-event
# value so that the +10 ms E-I delay actually produces somatic spikes
# before the shunt arrives; the null/preferred ratio of 4x is
# preserved from Park2014. Preflight peak firing at the preferred
# direction lands near 13-14 Hz, matching the t0008 baseline of ~15 Hz.
AMPA_CONDUCTANCE_NS: float = 6.0
GABA_CONDUCTANCE_PREFERRED_NS: float = 3.0
GABA_CONDUCTANCE_NULL_NS: float = 12.0
GABA_NULL_PREF_RATIO: float = 4.0

# Per-synapse burst parameters. Each NetStim fires N_SYN_EVENTS events
# at SYN_EVENT_INTERVAL_MS spacing starting at the scheduled onset time.
# Mimics the BIPsyn's continuous drive across the bar-sweep window
# (6 events x 30 ms spacing = 150 ms burst per pair).
N_SYN_EVENTS: int = 6
SYN_EVENT_INTERVAL_MS: float = 30.0

# Bar speed for onset calculation: t_onset = (x cos theta + y sin theta)/v.
# Value matches LIGHTSPEED_UM_PER_MS (1 um/ms) but kept as a separate
# constant because the bar-scheduling math is logically distinct from the
# HOC ``lightspeed`` global.
BAR_VELOCITY_UM_PER_MS: float = 1.0

# Global onset offset to keep all per-synapse onsets positive in the
# simulation window (accounts for negative x coordinates in morphology).
BAR_BASE_ONSET_MS: float = 200.0

# AMPA Exp2Syn kinetics (ms, mV). Values per Park2014 + DSGC-Poirazi-GH.
AMPA_TAU1_MS: float = 0.2
AMPA_TAU2_MS: float = 1.5
AMPA_REVERSAL_MV: float = 0.0

# GABA_A Exp2Syn kinetics (ms, mV). Values per Park2014 + DSGC-Poirazi-GH.
GABA_TAU1_MS: float = 0.5
GABA_TAU2_MS: float = 8.0
GABA_REVERSAL_MV: float = -70.0

# Synapse placement convention: distal AMPA, proximal GABA (on-the-path).
AMPA_SEG_LOCATION: float = 0.9
GABA_SEG_LOCATION: float = 0.3

# Task-local ID strings.
TASK_ID: str = "t0022_modify_dsgc_channel_testbed"
LIBRARY_ID: str = "modeldb_189347_dsgc_dendritic"

# Bootstrap sentinel env-var (renamed per plan to avoid cross-task collision).
NEURONHOME_SENTINEL_ENV: str = "_T0022_NEURONHOME_BOOTSTRAPPED"

# Preflight validation gate values (Milestone C).
PREFLIGHT_ANGLES_DEG: tuple[float, ...] = (0.0, 90.0, 180.0, 270.0)
PREFLIGHT_N_TRIALS: int = 2
PREFLIGHT_MIN_PEAK_FIRING_HZ: float = 5.0

# Acceptance gate (REQ-4).
ACCEPTANCE_MIN_DSI: float = 0.5
ACCEPTANCE_MIN_PEAK_HZ: float = 10.0

# Metric keys registered under meta/metrics/ (shared with t0008/t0012).
METRIC_KEY_DSI: str = "direction_selectivity_index"
METRIC_KEY_HWHM: str = "tuning_curve_hwhm_deg"
METRIC_KEY_RELIABILITY: str = "tuning_curve_reliability"
METRIC_KEY_RMSE: str = "tuning_curve_rmse"

# CSV schema column names (canonical t0004/t0012 schema).
CSV_COLUMN_ANGLE_DEG: str = "angle_deg"
CSV_COLUMN_TRIAL_SEED: str = "trial_seed"
CSV_COLUMN_FIRING_RATE_HZ: str = "firing_rate_hz"

# ModelDB 189347 pinned commit SHA (unchanged from t0008).
MODELDB_COMMIT_SHA: str = "87d669dcef18e9966e29c88520ede78bc16d36ff"
