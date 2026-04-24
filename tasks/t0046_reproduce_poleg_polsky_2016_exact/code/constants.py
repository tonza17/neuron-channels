"""Canonical constants for t0046 (exact reproduction of Poleg-Polsky 2016).

Values are read verbatim from ``main.hoc`` of ModelDB 189347 at commit
``87d669dcef18e9966e29c88520ede78bc16d36ff``. Where ``main.hoc`` overrides a MOD-file
PARAMETER default at module load, the ``main.hoc`` value wins (per
``research/research_code.md``); the discrepancy is recorded in the answer asset's
discrepancy catalogue.
"""

from __future__ import annotations

from enum import IntEnum

# ----------------------------------------------------------------------
# ModelDB provenance pin.
# ----------------------------------------------------------------------
MODELDB_COMMIT_SHA: str = "87d669dcef18e9966e29c88520ede78bc16d36ff"
MODELDB_AUTHORED_DATE: str = "2019-05-31"


# ----------------------------------------------------------------------
# Simulation timing (from main.hoc).
# ----------------------------------------------------------------------
TSTOP_MS: float = 1000.0
DT_MS: float = 0.1
CELSIUS_DEG_C: float = 32.0
V_INIT_MV: float = -65.0
V_REST_MV: float = -60.0  # RGCepas in init_active().


# ----------------------------------------------------------------------
# Synaptic conductances (main.hoc lines 41-47).
# ----------------------------------------------------------------------
B2GAMPA_NS: float = 0.25
B2GNMDA_CODE: float = 0.5
B2GNMDA_PAPER: float = 2.5
S2GGABA_NS: float = 0.5
S2GACH_NS: float = 0.5
GABAMOD_PD: float = 0.33
GABAMOD_ND: float = 0.99
ACHMOD_LOAD: float = 0.25
ACHMOD_SIMPLERUN: float = 0.33  # simplerun() rebinds achMOD at every call.


# ----------------------------------------------------------------------
# Visual stimulus geometry (main.hoc lines 63-70).
# ----------------------------------------------------------------------
LIGHTSTART_MS: float = -100.0
LIGHTSPEED_UM_PER_MS: float = 1.0
LIGHTWIDTH_UM: float = 500.0
LIGHT_X_START_UM: float = -100.0
LIGHT_X_END_UM: float = 200.0
LIGHT_Y_START_UM: float = -130.0
LIGHT_Y_END_UM: float = 100.0


# ----------------------------------------------------------------------
# Synaptic / VGC parameters (main.hoc lines 77-101).
# main.hoc overrides MOD PARAMETER defaults for several rows; the
# main.hoc values are canonical here.
# ----------------------------------------------------------------------
VAMPK_BIPNMDA: float = 5.0
VAMPT: float = 1.0
TRANSIENT_MS: float = 250.0
N_BIPNMDA: float = 0.3  # main.hoc 0.3 vs MOD default 0.25
GAMA_BIPNMDA: float = 0.07  # main.hoc 0.07 vs MOD default 0.08
NEWVES_BIPNMDA: float = 0.002  # main.hoc 0.002 vs MOD default 0.01
TAU1NMDA_BIPNMDA: float = 60.0  # main.hoc 60 vs MOD default 50
TAU_SACEXC_MS: float = 3.0
E_SACINHIB_MV: float = -60.0  # main.hoc -60 vs MOD default -65
TAU_SACINHIB_MS: float = 30.0  # main.hoc 30 vs MOD default 10
VSHIFT_HHST_MV: float = -4.0
RSYN_CHANCE: float = 1.0
SACDUR_MS: float = 500.0
NMDASPIKE_DUR_MS: float = 30.0
NMDASPIKE_V_MV: float = -40.0
VOFF_BIPNMDA_DEFAULT: float = 0.0
VSET_BIPNMDA_MV: float = -43.0


# ----------------------------------------------------------------------
# Noise driver parameters (main.hoc lines 99-101). flickerVAR and
# stimnoiseVAR are zero by default; Figures 6-8 set them to 0.10, 0.30,
# 0.50 (10% / 30% / 50% SD).
# ----------------------------------------------------------------------
FLICKERTIME_MS: float = 50.0
FLICKER_VAR_DEFAULT: float = 0.0
STIMNOISE_VAR_DEFAULT: float = 0.0
NOISE_SD_LEVELS: tuple[float, ...] = (0.0, 0.10, 0.30, 0.50)


# ----------------------------------------------------------------------
# Cell morphology constants from RGCmodel.hoc.
# ----------------------------------------------------------------------
N_SYNAPSES_EACH_TYPE_CODE: int = 282  # ModelDB code value (countON).
N_SYNAPSES_PAPER_CLAIM: int = 177  # paper text value.
NUM_SOMA_SECTIONS: int = 1
NUM_DEND_SECTIONS: int = 350
DEND_NAV_GBAR_S_PER_CM2: float = 2e-4  # dendritic Na density (small but non-zero).


# ----------------------------------------------------------------------
# Sweep grids.
# ----------------------------------------------------------------------
N_TRIALS_PSP: int = 3  # cut down from paper's 12-19 for wall-clock.
N_TRIALS_NOISE: int = 2  # noise sweep trials per (condition, noise level).
N_TRIALS_FIG3: int = 2  # gNMDA sweep trials per gNMDA value.
N_TRIALS_FIG8: int = 2  # spike-condition trials.
DIRECTIONS_DEG: tuple[int, ...] = (0, 45, 90, 135, 180, 225, 270, 315)
GNMDA_SWEEP_VALUES_NS: tuple[float, ...] = (0.0, 0.5, 1.5, 2.5)


# ----------------------------------------------------------------------
# Spike detection.
# ----------------------------------------------------------------------
AP_THRESHOLD_MV: float = 0.0  # Figure 8 NetCon threshold.
PSP_BASELINE_MS: float = 100.0  # window length for pre-stimulus baseline.


# ----------------------------------------------------------------------
# Bootstrap sentinel env-var (renamed per task to avoid collision).
# ----------------------------------------------------------------------
NEURONHOME_SENTINEL_ENV: str = "_T0046_NEURONHOME_BOOTSTRAPPED"


# ----------------------------------------------------------------------
# Metric registry keys (registered under meta/metrics/).
# ----------------------------------------------------------------------
METRIC_KEY_DSI: str = "direction_selectivity_index"
METRIC_KEY_HWHM: str = "tuning_curve_hwhm_deg"
METRIC_KEY_RELIABILITY: str = "tuning_curve_reliability"
METRIC_KEY_RMSE: str = "tuning_curve_rmse"


# ----------------------------------------------------------------------
# Enumerations.
# ----------------------------------------------------------------------
class ExperimentType(IntEnum):
    """Maps to the integer ``simplerun($1, $2)`` first arg in main.hoc."""

    CONTROL = 1
    ZERO_MG = 2
    HIGH_CL = 3


class Direction(IntEnum):
    """Maps to the integer ``simplerun($1, $2)`` second arg.

    PD: gabaMOD = 0.33 (preferred, weak inhibition).
    ND: gabaMOD = 0.99 (null, strong inhibition).
    """

    PREFERRED = 0
    NULL = 1


# ----------------------------------------------------------------------
# CSV column names.
# ----------------------------------------------------------------------
COL_TRIAL_SEED: str = "trial_seed"
COL_DIRECTION_LABEL: str = "direction_label"
COL_DIRECTION_DEG: str = "direction_deg"
COL_EXPTYPE: str = "exptype"
COL_FLICKER_VAR: str = "flicker_var"
COL_STIMNOISE_VAR: str = "stim_noise_var"
COL_B2GNMDA_NS: str = "b2gnmda_ns"
COL_PEAK_PSP_MV: str = "peak_psp_mv"
COL_BASELINE_PSP_MV: str = "baseline_psp_mv"
COL_SPIKE_COUNT: str = "spike_count"
COL_AP_RATE_HZ: str = "ap_rate_hz"
COL_NOTES: str = "notes"
COL_GNMDA_NS: str = "gnmda_ns"
COL_VARIANT: str = "variant"
