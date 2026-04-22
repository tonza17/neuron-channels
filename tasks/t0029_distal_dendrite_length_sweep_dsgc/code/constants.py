"""Canonical constants for the t0029 distal-length sweep task.

Defines the sweep grid, CSV column names, the metric keys used in ``results/metrics.json``, and the
classification thresholds used by ``classify_curve_shape.py``.
"""

from __future__ import annotations

# Sweep grid (REQ-3). Seven equally spaced multipliers from 0.5x to 2.0x of baseline distal L.
LENGTH_MULTIPLIERS: tuple[float, ...] = (
    0.5,
    0.75,
    1.0,
    1.25,
    1.5,
    1.75,
    2.0,
)

# Preflight sweep grid (validation gate): exercise extremes plus baseline.
PREFLIGHT_LENGTH_MULTIPLIERS: tuple[float, ...] = (0.5, 1.0, 2.0)
PREFLIGHT_ANGLES_DEG: tuple[int, ...] = (0, 120, 240)
PREFLIGHT_N_TRIALS: int = 2

# Distal identification thresholds (REQ-2).
DISTAL_MIN_DEPTH: int = 3
DISTAL_MIN_COUNT: int = 50

# Tidy-CSV column names (REQ-4, REQ-8).
CSV_COL_LENGTH_MULTIPLIER: str = "length_multiplier"
CSV_COL_TRIAL: str = "trial"
CSV_COL_DIRECTION_DEG: str = "direction_deg"
CSV_COL_SPIKE_COUNT: str = "spike_count"
CSV_COL_PEAK_MV: str = "peak_mv"
CSV_COL_FIRING_RATE_HZ: str = "firing_rate_hz"

TIDY_CSV_HEADER: tuple[str, ...] = (
    CSV_COL_LENGTH_MULTIPLIER,
    CSV_COL_TRIAL,
    CSV_COL_DIRECTION_DEG,
    CSV_COL_SPIKE_COUNT,
    CSV_COL_PEAK_MV,
    CSV_COL_FIRING_RATE_HZ,
)

# Per-length canonical tuning-curve CSV header (accepted by t0012 load_tuning_curve).
CURVE_CSV_HEADER: tuple[str, ...] = (
    "angle_deg",
    "trial_seed",
    "firing_rate_hz",
)

# Metric keys registered under ``meta/metrics/``.
METRIC_KEY_DSI: str = "direction_selectivity_index"
METRIC_KEY_HWHM: str = "tuning_curve_hwhm_deg"
METRIC_KEY_RELIABILITY: str = "tuning_curve_reliability"

# Classification thresholds (REQ-5, REQ-6).
MONOTONIC_SLOPE_MIN_PER_UNIT: float = 0.05
MONOTONIC_P_MAX: float = 0.05
SATURATION_FRACTION_OF_MAX: float = 0.95
SATURATION_MULTIPLIER_MAX: float = 1.25
SATURATION_MAX_DELTA_DSI: float = 0.05
NON_DECREASING_TOLERANCE: float = 1e-3

# Shape-class labels.
SHAPE_MONOTONIC: str = "monotonic"
SHAPE_SATURATING: str = "saturating"
SHAPE_NON_MONOTONIC: str = "non_monotonic"

# Valid shape-class set for verification.
SHAPE_CLASSES: tuple[str, ...] = (
    SHAPE_MONOTONIC,
    SHAPE_SATURATING,
    SHAPE_NON_MONOTONIC,
)

# Distal-identification rule label (recorded in logs/preflight/distal_sections.json).
DISTAL_IDENTIFICATION_RULE: str = "hoc_leaves_on_arbor_depth_ge_3"

# Baseline multiplier value (sanity-check constant).
BASELINE_MULTIPLIER: float = 1.0

# Section-length assertion tolerance (micrometres).
LENGTH_ASSERT_TOL_UM: float = 1e-9
