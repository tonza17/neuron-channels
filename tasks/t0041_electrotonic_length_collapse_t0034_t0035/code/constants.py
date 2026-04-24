"""Canonical numeric constants for the t0041 electrotonic-length collapse analysis.

All cable-theory inputs (passive Rm, Ra, baseline distal L and d), sweep grids, CSV column names,
and collapse-test thresholds live here. Biophysics values are copied from t0024's ``constants.py``
(commit ``a23f642aa6557a23a51bf76f51e420e8149773fa`` of the upstream model). Baseline per-section
distal length and diameter come from the t0034 and t0035 preflight snapshots (``distal_sections``
preflight log).
"""

from __future__ import annotations

# Passive cable properties (copied verbatim from
# tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py lines 27-30).
RA_OHM_CM: float = 100.0
CM_UF_CM2: float = 1.0
GLEAK_S_CM2: float = 0.0001667
ELEAK_MV: float = -60.0

# Derived specific membrane resistance.
RM_OHM_CM2: float = 1.0 / GLEAK_S_CM2  # approx 5999 ohm.cm^2

# Baseline per-section distal dimensions on the t0024 RGCmodelGD morphology.
# These are the *section-mean* values over the 177 distal terminal dends, as measured in the
# t0034 and t0035 preflight snapshots.
#
# Source: tasks/t0034_distal_dendrite_length_sweep_t0024/logs/preflight/distal_sections.json
#   median_L_um = 14.78822195444683
#   total_L_um  = 4004.8279960449927
#   count       = 177 -> mean_L_um = total_L_um / count = 22.62615817 um
# Source: tasks/t0035_distal_dendrite_diameter_sweep_t0024/logs/preflight/distal_sections.json
#   mean_diam_um   = 0.5034757623765028
#   median_diam_um = 0.5000012516975404
#
# We take the arithmetic mean over sections as the scalar L/lambda summary because the plan's
# original placeholders (50.0 um, 0.5 um) do not match the real morphology; the actual mean L is
# 22.63 um, not 50 um. Using a section-mean scalar L/lambda is consistent with the research note
# that Rm and Ra are uniform across all distal sections (so lambda varies only with per-section
# diameter) and with the fact that every distal section is rescaled by the same multiplier.
N_DISTAL_SECTIONS: int = 177
TOTAL_DISTAL_L_UM: float = 4004.8279960449927
MEAN_DISTAL_L_UM: float = TOTAL_DISTAL_L_UM / N_DISTAL_SECTIONS
MEDIAN_DISTAL_L_UM: float = 14.78822195444683
MEAN_DISTAL_DIAM_UM: float = 0.5034757623765028
MEDIAN_DISTAL_DIAM_UM: float = 0.5000012516975404

# We report the collapse test using the MEAN section L and MEAN section diameter so that the
# scalar L/lambda summary equals a section-averaged electrotonic length. Median values are kept
# as documentation only.
BASELINE_DISTAL_LENGTH_UM: float = MEAN_DISTAL_L_UM
BASELINE_DISTAL_DIAM_UM: float = MEAN_DISTAL_DIAM_UM

# Unit conversions.
UM_PER_CM: float = 10_000.0

# Sweep grid (identical in t0034 and t0035: 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0).
SWEEP_MULTIPLIERS: tuple[float, ...] = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)
BASELINE_MULTIPLIER: float = 1.0

# t0034 operating points that landed in the spike-failure regime, per t0034's
# results_summary.md / classify_shape.py output. Flag these on the collapse plot with distinct
# markers and report Pearson r both including and excluding these points.
T0034_SPIKE_FAILURE_MULTIPLIERS: tuple[float, ...] = (1.5, 2.0)

# Sweep identifiers used in the output CSV.
SWEEP_LENGTH: str = "length"
SWEEP_DIAMETER: str = "diameter"
SWEEP_LABELS: tuple[str, ...] = (SWEEP_LENGTH, SWEEP_DIAMETER)

# Column names in the upstream per-multiplier metrics CSVs.
T0034_MULTIPLIER_COLUMN: str = "length_multiplier"
T0035_MULTIPLIER_COLUMN: str = "diameter_multiplier"
DSI_PRIMARY_COLUMN: str = "dsi_primary"
DSI_VECTOR_SUM_COLUMN: str = "dsi_vector_sum"
PEAK_HZ_COLUMN: str = "peak_hz"
NULL_HZ_COLUMN: str = "null_hz"

# Column names in this task's output electrotonic_length_table.csv.
OUT_COL_SWEEP: str = "sweep"
OUT_COL_MULTIPLIER: str = "multiplier"
OUT_COL_EFFECTIVE_L_UM: str = "effective_L_um"
OUT_COL_EFFECTIVE_D_UM: str = "effective_d_um"
OUT_COL_LAMBDA_UM: str = "lambda_um"
OUT_COL_L_OVER_LAMBDA: str = "L_over_lambda"
OUT_COL_DSI_PRIMARY: str = "dsi_primary"
OUT_COL_DSI_VECTOR_SUM: str = "dsi_vector_sum"
OUT_COL_PEAK_HZ: str = "peak_hz"
OUT_COL_NULL_HZ: str = "null_hz"
OUT_COL_SPIKE_FAILURE: str = "spike_failure_flag"

OUTPUT_CSV_HEADER: tuple[str, ...] = (
    OUT_COL_SWEEP,
    OUT_COL_MULTIPLIER,
    OUT_COL_EFFECTIVE_L_UM,
    OUT_COL_EFFECTIVE_D_UM,
    OUT_COL_LAMBDA_UM,
    OUT_COL_L_OVER_LAMBDA,
    OUT_COL_DSI_PRIMARY,
    OUT_COL_DSI_VECTOR_SUM,
    OUT_COL_PEAK_HZ,
    OUT_COL_NULL_HZ,
    OUT_COL_SPIKE_FAILURE,
)

# Collapse-test thresholds (REQ-3).
PEARSON_R_COLLAPSE_MIN: float = 0.9
POLYNOMIAL_DEGREE: int = 2

# Collapse verdict labels.
VERDICT_COLLAPSE_CONFIRMED: str = "collapse_confirmed"
VERDICT_COLLAPSE_REJECTED: str = "collapse_rejected"
