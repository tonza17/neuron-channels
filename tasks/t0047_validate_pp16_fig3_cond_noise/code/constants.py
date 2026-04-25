"""Task-local constants for t0047.

The reversal-potential constants in this module are deliberately re-affirmed from t0046's
constants module via an assertion at module load — if t0046's value drifts, this module
will fail to import and the discrepancy is surfaced loudly.
"""

from __future__ import annotations

from enum import Enum

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (
    E_SACINHIB_MV as _T0046_E_SACINHIB_MV,
)

# ----------------------------------------------------------------------
# Sweep grids.
# ----------------------------------------------------------------------
B2GNMDA_GRID_NS: tuple[float, ...] = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
FLICKER_VAR_GRID: tuple[float, ...] = (0.0, 0.1, 0.3, 0.5)
PSP_TRACE_GNMDA_VALUES_NS: tuple[float, ...] = (0.0, 0.5, 2.5)

TRIALS_PER_CELL: int = 4

# ----------------------------------------------------------------------
# Recorder timing.
# ----------------------------------------------------------------------
DT_RECORD_MS: float = 0.25

# ----------------------------------------------------------------------
# Reversal potentials (for offline current computation, MOD-aligned).
# E_SACINHIB_MV_OVERRIDE is the main.hoc -60 mV value, NOT the MOD default -65.
# ----------------------------------------------------------------------
E_BIPNMDA_MV: float = 0.0
E_SACEXC_MV: float = 0.0
E_SACINHIB_MV_OVERRIDE: float = -60.0

assert E_SACINHIB_MV_OVERRIDE == _T0046_E_SACINHIB_MV, (
    f"E_SACINHIB_MV_OVERRIDE ({E_SACINHIB_MV_OVERRIDE}) disagrees with t0046's "
    f"E_SACINHIB_MV ({_T0046_E_SACINHIB_MV}); main.hoc canonical value drift?"
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
DSI_PAPER_FIG3F_TARGET: float = 0.30
DSI_FIG3F_TOLERANCE: float = 0.05
PSP_PEAK_TOLERANCE_FRAC: float = 0.20

# ----------------------------------------------------------------------
# Noise condition enum.
# ----------------------------------------------------------------------


class NoiseCondition(Enum):
    """Noise-extension condition labels (Fig 6/7 grouping)."""

    CONTROL = "control"
    AP5 = "AP5"
    ZERO_MG = "0Mg"


# ----------------------------------------------------------------------
# CSV / JSON column names.
# ----------------------------------------------------------------------
COL_B2GNMDA_NS: str = "b2gnmda_ns"
COL_DIRECTION: str = "direction"
COL_TRIAL_SEED: str = "trial_seed"
COL_PEAK_PSP_MV: str = "peak_psp_mv"
COL_BASELINE_MEAN_MV: str = "baseline_mean_mv"
COL_PEAK_G_NMDA_SUMMED_NS: str = "peak_g_nmda_summed_ns"
COL_PEAK_G_AMPA_SUMMED_NS: str = "peak_g_ampa_summed_ns"
COL_PEAK_G_SACEXC_SUMMED_NS: str = "peak_g_sacexc_summed_ns"
COL_PEAK_G_SACINHIB_SUMMED_NS: str = "peak_g_sacinhib_summed_ns"
COL_PEAK_G_NMDA_PER_SYN_MEAN_NS: str = "peak_g_nmda_per_syn_mean_ns"
COL_PEAK_G_AMPA_PER_SYN_MEAN_NS: str = "peak_g_ampa_per_syn_mean_ns"
COL_PEAK_G_SACEXC_PER_SYN_MEAN_NS: str = "peak_g_sacexc_per_syn_mean_ns"
COL_PEAK_G_SACINHIB_PER_SYN_MEAN_NS: str = "peak_g_sacinhib_per_syn_mean_ns"
COL_PEAK_I_NMDA_SUMMED_NA: str = "peak_i_nmda_summed_na"
COL_PEAK_I_AMPA_SUMMED_NA: str = "peak_i_ampa_summed_na"
COL_PEAK_I_SACEXC_SUMMED_NA: str = "peak_i_sacexc_summed_na"
COL_PEAK_I_SACINHIB_SUMMED_NA: str = "peak_i_sacinhib_summed_na"
COL_CONDITION: str = "condition"
COL_FLICKER_VAR: str = "flicker_var"
COL_T_MS: str = "t_ms"
COL_V_MV: str = "v_mv"

# ----------------------------------------------------------------------
# Direction string labels (CSV-friendly mapping over t0046's IntEnum).
# ----------------------------------------------------------------------
DIRECTION_PD_LABEL: str = "PD"
DIRECTION_ND_LABEL: str = "ND"

# ----------------------------------------------------------------------
# Metric registry keys (registered under meta/metrics/).
# ----------------------------------------------------------------------
METRIC_KEY_DSI: str = "direction_selectivity_index"
