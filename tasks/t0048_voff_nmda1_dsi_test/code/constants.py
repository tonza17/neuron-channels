"""Task-local constants for t0048.

Sweep grid, recorder timing, reversal potentials, paper/verdict thresholds, CSV column
names, and direction labels for the Voff_bipNMDA = 1 DSI flatness test. The reversal-
potential constants in this module are deliberately re-affirmed from t0046's constants
module via an assertion at module load — if t0046's value drifts, this module will fail
to import and the discrepancy is surfaced loudly.

Most of the constants below are COPIED verbatim from
``tasks/t0047_validate_pp16_fig3_cond_noise/code/constants.py`` per the project's cross-
task code-reuse rule (t0047 is not a registered library asset). Source attribution is
preserved per constant where relevant. Three constants are NEW for t0048: the H1 range
threshold, the H1 slope threshold, and the t0047 empirical range used as the H2 reference.
"""

from __future__ import annotations

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (
    E_SACINHIB_MV as _T0046_E_SACINHIB_MV,
)

# ----------------------------------------------------------------------
# Sweep grids. (COPIED from t0047/code/constants.py:19-23)
# ----------------------------------------------------------------------
B2GNMDA_GRID_NS: tuple[float, ...] = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
TRIALS_PER_CELL: int = 4

# ----------------------------------------------------------------------
# Recorder timing. (COPIED from t0047/code/constants.py:28)
# ----------------------------------------------------------------------
DT_RECORD_MS: float = 0.25

# ----------------------------------------------------------------------
# Reversal potentials (for offline current computation, MOD-aligned).
# E_SACINHIB_MV_OVERRIDE is the main.hoc -60 mV value, NOT the MOD default -65.
# (COPIED from t0047/code/constants.py:34-41)
# ----------------------------------------------------------------------
E_BIPNMDA_MV: float = 0.0
E_SACEXC_MV: float = 0.0
E_SACINHIB_MV_OVERRIDE: float = -60.0

assert E_SACINHIB_MV_OVERRIDE == _T0046_E_SACINHIB_MV, (
    f"E_SACINHIB_MV_OVERRIDE ({E_SACINHIB_MV_OVERRIDE}) disagrees with t0046's "
    f"E_SACINHIB_MV ({_T0046_E_SACINHIB_MV}); main.hoc canonical value drift?"
)

# ----------------------------------------------------------------------
# Paper Fig 3F target and tolerance band.
# (COPIED from t0047/code/constants.py:54-55)
# ----------------------------------------------------------------------
DSI_PAPER_FIG3F_TARGET: float = 0.30
DSI_FIG3F_TOLERANCE: float = 0.05

# ----------------------------------------------------------------------
# H0 / H1 / H2 verdict thresholds (NEW for t0048).
#
# REQ-12 range test: H1 if max-min DSI across the 7 grid points <= 0.10.
# REQ-12 slope test: H1 if |linear-regression slope| < 0.02 per nS.
# T0047 empirical range = 0.192 - 0.018 = 0.174; used as the H2 reference threshold.
# T0047 empirical slope = approximately -0.058 per nS (linear fit of t0047's seven DSI
# values vs B2GNMDA_GRID_NS); used as the H2 slope reference threshold.
# ----------------------------------------------------------------------
DSI_RANGE_FLAT_THRESHOLD: float = 0.10
DSI_SLOPE_FLAT_THRESHOLD: float = 0.02
T0047_DSI_RANGE_REFERENCE: float = 0.174
T0047_DSI_SLOPE_REFERENCE_PER_NS: float = -0.058

# ----------------------------------------------------------------------
# CSV / JSON column names. (COPIED from t0047/code/constants.py:74-94)
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

# ----------------------------------------------------------------------
# Direction string labels (CSV-friendly mapping over t0046's IntEnum).
# (COPIED from t0047/code/constants.py:99-100)
# ----------------------------------------------------------------------
DIRECTION_PD_LABEL: str = "PD"
DIRECTION_ND_LABEL: str = "ND"

# ----------------------------------------------------------------------
# Metric registry keys (registered under meta/metrics/).
# (COPIED from t0047/code/constants.py:105)
# ----------------------------------------------------------------------
METRIC_KEY_DSI: str = "direction_selectivity_index"
