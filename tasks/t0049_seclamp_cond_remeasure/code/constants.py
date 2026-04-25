"""Task-local constants for t0049 (SEClamp conductance re-measurement).

The reversal-potential constant ``E_GABA_MV`` is deliberately re-affirmed against t0046's
``E_SACINHIB_MV`` via an assertion at module load. If t0046's value drifts, this module will
fail to import and the discrepancy is surfaced loudly. Pattern adopted from t0047's
``code/constants.py``.
"""

from __future__ import annotations

from enum import Enum

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (
    E_SACINHIB_MV as _T0046_E_SACINHIB_MV,
)

# ----------------------------------------------------------------------
# SEClamp parameters.
# ----------------------------------------------------------------------
V_CLAMP_MV: float = -65.0
AMP1_MV: float = -65.0
RS_MOHM: float = 0.001
DT_RECORD_MS: float = 0.25
CLAMP_VOLTAGE_TOLERANCE_MV: float = 0.5

# ----------------------------------------------------------------------
# Reversal potentials (for offline current-to-conductance computation).
# ----------------------------------------------------------------------
E_NMDA_MV: float = 0.0
E_AMPA_MV: float = 0.0
E_GABA_MV: float = -60.0

assert E_GABA_MV == _T0046_E_SACINHIB_MV, (
    f"E_GABA_MV ({E_GABA_MV}) disagrees with t0046's E_SACINHIB_MV "
    f"({_T0046_E_SACINHIB_MV}); main.hoc canonical value drift?"
)

# ----------------------------------------------------------------------
# Paper Fig 3A-E targets and verdict tolerances.
# ----------------------------------------------------------------------
NMDA_PD_TARGET_NS: float = 7.0
NMDA_ND_TARGET_NS: float = 5.0
AMPA_PD_TARGET_NS: float = 3.5
AMPA_ND_TARGET_NS: float = 3.5
GABA_PD_TARGET_NS: float = 12.5
GABA_ND_TARGET_NS: float = 30.0

CONDUCTANCE_TOLERANCE_FRAC: float = 0.25
H0_TOLERANCE_FRAC: float = 0.10

# ----------------------------------------------------------------------
# t0047 per-synapse-summed baseline values, hard-coded at gNMDA = 0.5 nS.
# Source: tasks/t0047_validate_pp16_fig3_cond_noise/results/results_summary.md (lines 15-22).
# ----------------------------------------------------------------------
T0047_NMDA_PD_NS: float = 69.55
T0047_NMDA_ND_NS: float = 33.98
T0047_AMPA_PD_NS: float = 10.92
T0047_AMPA_ND_NS: float = 10.77
T0047_GABA_PD_NS: float = 106.13
T0047_GABA_ND_NS: float = 215.57
T0047_NUM_SYNAPSES: int = 282

# ----------------------------------------------------------------------
# Sweep grid.
# ----------------------------------------------------------------------
B2GNMDA_NS: float = 0.5
TRIALS_PER_CONDITION: int = 4
BASE_SEED: int = 20000
SEED_OFFSET_DIRECTION: int = 1000
SEED_OFFSET_CHANNEL: int = 100


# ----------------------------------------------------------------------
# Channel isolation enum.
# ----------------------------------------------------------------------
class ChannelIsolation(Enum):
    ALL = "all"
    AMPA_ONLY = "ampa_only"
    NMDA_ONLY = "nmda_only"
    GABA_ONLY = "gaba_only"


# ----------------------------------------------------------------------
# CSV column names.
# ----------------------------------------------------------------------
COL_DIRECTION: str = "direction"
COL_CHANNEL_ON: str = "channel_on"
COL_TRIAL_SEED: str = "trial_seed"
COL_B2GNMDA_NS: str = "b2gnmda_ns"
COL_PEAK_I_PA: str = "peak_i_pa"
COL_BASELINE_I_PA: str = "baseline_i_pa"
COL_PEAK_I_MINUS_BASELINE_PA: str = "peak_i_minus_baseline_pa"
COL_CLAMP_V_SD_MV: str = "clamp_v_sd_mv"

# Comparison-table columns.
COL_CHANNEL: str = "channel"
COL_G_SECLAMP_MEAN_NS: str = "g_seclamp_mean_ns"
COL_G_SECLAMP_SD_NS: str = "g_seclamp_sd_ns"
COL_N: str = "n"
COL_PAPER_TARGET_NS: str = "paper_target_ns"
COL_T0047_SUMMED_NS: str = "t0047_summed_ns"
COL_T0047_PER_SYN_MEAN_NS: str = "t0047_per_syn_mean_ns"
COL_DELTA_PAPER_FRAC: str = "delta_paper_frac"
COL_DELTA_T0047_FRAC: str = "delta_t0047_frac"
COL_VERDICT: str = "verdict"

# ----------------------------------------------------------------------
# Direction string labels.
# ----------------------------------------------------------------------
DIRECTION_PD_LABEL: str = "PD"
DIRECTION_ND_LABEL: str = "ND"

# ----------------------------------------------------------------------
# Channel string labels (for CSV / metrics).
# ----------------------------------------------------------------------
CHANNEL_NMDA_LABEL: str = "nmda"
CHANNEL_AMPA_LABEL: str = "ampa"
CHANNEL_GABA_LABEL: str = "gaba"

# ----------------------------------------------------------------------
# Verdict labels.
# ----------------------------------------------------------------------
VERDICT_H0: str = "H0"
VERDICT_H1: str = "H1"
VERDICT_H2: str = "H2"

# ----------------------------------------------------------------------
# Metric registry keys (registered under meta/metrics/).
# ----------------------------------------------------------------------
METRIC_KEY_DSI: str = "direction_selectivity_index"

# ----------------------------------------------------------------------
# Misc.
# ----------------------------------------------------------------------
PSP_BASELINE_MS: float = 100.0  # Baseline window for clamp current.
NA_TO_PA: float = 1000.0  # Convert NEURON's nA SEClamp current to pA.
