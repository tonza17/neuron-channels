"""Typed constants for t0065 EPSP/IPSP/FULL protocol on the deposited DSGC."""

from __future__ import annotations

from enum import Enum


class TrialMode(Enum):
    """Trial recording mode. Mirrors t0059's TrialMode enum spelling."""

    FULL = "FULL"
    EPSP_PASSIVE = "EPSP_PASSIVE"
    IPSP_PASSIVE = "IPSP_PASSIVE"


class Condition(Enum):
    """Direction condition. Mirrors t0020's Condition enum."""

    PD = "PD"
    ND = "ND"


# exptype values consumed by HOC init_active() at dsgc_model.hoc:114-152.
# exptype == 1: active mode, TTX = 0, RGCsomana = 0.4 (HH on).
# exptype == 2: TTX mode, RGCsomana = 0 (HH off via Na+ block).
EXPTYPE_HH_ON: int = 1
EXPTYPE_HH_OFF: int = 2

# gabaMOD scalars. PD = weak inhibition, ND = strong inhibition (Poleg-Polsky 2016).
GABA_MOD_PD: float = 0.33
GABA_MOD_ND: float = 0.99
GABA_MOD_OFF: float = 0.0

# Excitatory conductances zeroed in IPSP_PASSIVE. Both the bipolar (b2gampa, b2gnmda) and SAC
# cholinergic (s2gach, achMOD) pathways must be silenced for a strict inhibition-only trace —
# the deposited model drives RGC excitation through both.
B_AMPA_OFF_NS: float = 0.0
B_NMDA_OFF_NS: float = 0.0
S_ACH_OFF_NS: float = 0.0
ACH_MOD_OFF: float = 0.0

# Inhibitory conductance zeroed in EPSP_PASSIVE. gabaMOD = 0 zeroes the modulation envelope
# (placeBIP line `mulnoise.fill(VampT*gabaMOD,...)`); also zeroing s2ggaba removes baseline
# inhibitory leakage that the modulation envelope cannot reach.
S_GABA_OFF_NS: float = 0.0

# Per-trial seed. Single seed for this diagnostic task.
SEED: int = 1

# CSV column names.
MODE_COLUMN: str = "mode"
DIRECTION_COLUMN: str = "direction"
T_MS_COLUMN: str = "t_ms"
V_MV_COLUMN: str = "v_mv"

# Metrics keys.
PEAK_V_MV_KEY: str = "peak_v_mv"
BASELINE_V_MV_KEY: str = "baseline_v_mv"
PEAK_MINUS_BASELINE_MV_KEY: str = "peak_minus_baseline_mv"
SPIKE_COUNT_KEY: str = "spike_count"
N_SAMPLES_KEY: str = "n_samples"
TRIAL_KEY_KEY: str = "trial_key"

# Baseline window for baseline_v_mv computation: t < BASELINE_END_MS.
# The deposited model's drifting bar starts at lightstart = -100 ms in HOC
# time but the recorded t starts at 0. The first ~100 ms after t=0 is
# pre-bar quiescent depolarisation only, matching t0046's PSP_BASELINE_MS.
BASELINE_END_MS: float = 100.0
