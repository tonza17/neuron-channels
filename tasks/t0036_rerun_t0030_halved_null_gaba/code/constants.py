"""Canonical constants for the t0036 distal-diameter sweep with halved null-GABA.

Defines the sweep grid, CSV column names, the metric keys used in ``results/metrics.json``, the
mechanism-classification thresholds used by ``classify_slope.py``, and the two task-specific
additions:

* ``GABA_CONDUCTANCE_NULL_NS_OVERRIDE`` — the halved null-direction GABA conductance applied via
  ``gaba_override.py`` at import time (6.0 nS, down from the t0022 default of 12.0 nS).
* ``NULL_HZ_MIN_PRECONDITION_HZ`` — the minimum mean null-direction firing rate at the 1.0x
  baseline multiplier that must be reached for the DSI-slope mechanism classification to be
  treated as complete rather than ``_partial``.

Structural clone of ``tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/constants.py``.
"""

from __future__ import annotations

# Sweep grid (REQ-4). Seven equally spaced multipliers from 0.5x to 2.0x of baseline seg.diam.
DIAMETER_MULTIPLIERS: tuple[float, ...] = (
    0.5,
    0.75,
    1.0,
    1.25,
    1.5,
    1.75,
    2.0,
)

# Preflight sweep grid (validation gate): extremes plus baseline.
PREFLIGHT_DIAMETER_MULTIPLIERS: tuple[float, ...] = (0.5, 1.0, 2.0)
PREFLIGHT_ANGLES_DEG: tuple[int, ...] = (0, 120, 240)
PREFLIGHT_N_TRIALS: int = 2

# Distal identification thresholds (REQ-3).
DISTAL_MIN_DEPTH: int = 3
DISTAL_MIN_COUNT: int = 50

# Tidy-CSV column names (REQ-4, REQ-7).
CSV_COL_DIAMETER_MULTIPLIER: str = "diameter_multiplier"
CSV_COL_TRIAL: str = "trial"
CSV_COL_DIRECTION_DEG: str = "direction_deg"
CSV_COL_SPIKE_COUNT: str = "spike_count"
CSV_COL_PEAK_MV: str = "peak_mv"
CSV_COL_FIRING_RATE_HZ: str = "firing_rate_hz"

TIDY_CSV_HEADER: tuple[str, ...] = (
    CSV_COL_DIAMETER_MULTIPLIER,
    CSV_COL_TRIAL,
    CSV_COL_DIRECTION_DEG,
    CSV_COL_SPIKE_COUNT,
    CSV_COL_PEAK_MV,
    CSV_COL_FIRING_RATE_HZ,
)

# Per-diameter canonical tuning-curve CSV header (accepted by t0012 load_tuning_curve).
CURVE_CSV_HEADER: tuple[str, ...] = (
    "angle_deg",
    "trial_seed",
    "firing_rate_hz",
)

# Metric keys registered under ``meta/metrics/``.
METRIC_KEY_DSI: str = "direction_selectivity_index"
METRIC_KEY_HWHM: str = "tuning_curve_hwhm_deg"
METRIC_KEY_RELIABILITY: str = "tuning_curve_reliability"

# Mechanism classification thresholds (REQ-7, REQ-10, REQ-12).
MIN_SLOPE_MAGNITUDE: float = 0.05
MAX_P_VALUE: float = 0.05
DSI_SATURATION_THRESHOLD: float = 0.02
DSI_RANGE_MIN_FOR_CONFIDENT_LABEL: float = 0.05

# Mechanism labels.
MECHANISM_SCHACHTER2010: str = "schachter2010_amplification"
MECHANISM_PASSIVE: str = "passive_filtering"
MECHANISM_FLAT: str = "flat"

MECHANISM_LABELS: tuple[str, ...] = (
    MECHANISM_SCHACHTER2010,
    MECHANISM_PASSIVE,
    MECHANISM_FLAT,
)

# Slope sign labels.
SLOPE_SIGN_POSITIVE: str = "+"
SLOPE_SIGN_NEGATIVE: str = "-"
SLOPE_SIGN_FLAT: str = "~"

# Distal-identification rule label (recorded in logs/preflight/distal_sections.json).
DISTAL_IDENTIFICATION_RULE: str = "hoc_leaves_on_arbor_depth_ge_3"

# Baseline multiplier value (sanity-check constant).
BASELINE_MULTIPLIER: float = 1.0

# Section-diameter assertion tolerance (micrometres). NEURON stores ``seg.diam`` in single
# precision internally, so round-trip rescaling can introduce up to a few ``1e-8`` um error at
# multipliers near the float-precision edge (e.g. baseline 0.499999... um -> 0.999999... um
# read back as 1.0 um). Set tolerance at 1e-6 um (= 1 angstrom) which is far below any
# physiologically meaningful scale.
DIAMETER_ASSERT_TOL_UM: float = 1e-6

# Midpoint-snapshot tolerance (um). 3D point coordinates are NOT mutated by seg.diam writes in
# NEURON, so this should hold to floating-point exactness.
MIDPOINT_ASSERT_TOL_UM: float = 1e-9

# t0036-specific additions (REQ-2, REQ-10).
# Halved null-direction GABA conductance applied at import time via ``gaba_override.py``.
# The t0022 default is 12.0 nS; Schachter2010 reports ~6 nS compound null inhibition.
GABA_CONDUCTANCE_NULL_NS_OVERRIDE: float = 6.0

# Minimum mean null-direction firing rate at the 1.0x baseline multiplier for the DSI-slope
# mechanism classification to be treated as complete (vs. ``_partial``). Set to 0.1 Hz: below
# this, the GABA reduction has not unpinned null firing enough for the primary DSI to be
# interpretable.
NULL_HZ_MIN_PRECONDITION_HZ: float = 0.1
