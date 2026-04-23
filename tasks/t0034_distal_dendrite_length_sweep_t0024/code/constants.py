"""Canonical constants for the t0034 distal-length sweep on the t0024 DSGC port.

Defines the sweep grid, CSV column names, the metric keys used in ``results/metrics.json``, and the
classification thresholds used by ``classify_shape.py``. Cloned from t0029's ``constants.py`` and
extended with t0024-specific aliases (``AR2_RHO``, ``N_TRIALS_T0024``).
"""

from __future__ import annotations

# Sweep grid (REQ-4). Seven equally spaced multipliers from 0.5x to 2.0x of baseline distal L.
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

# Per-sweep-point trial count for the full sweep (t0024 canonical: 10 trials per angle).
N_TRIALS_T0024: int = 10

# AR(2) correlation constant, pinned to the t0026 V_rest-sweep correlated default (REQ-6).
AR2_RHO: float = 0.6

# Distal identification thresholds (REQ-2). On t0024 these are warn-only (logged, not asserted),
# since the ``RGCmodelGD.hoc`` topology differs from t0022's ``RGCmodel.hoc``.
DISTAL_MIN_DEPTH: int = 3
DISTAL_MIN_COUNT: int = 50

# Tidy-CSV column names.
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

# Classification thresholds (REQ-8, REQ-12).
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
DISTAL_IDENTIFICATION_RULE: str = "t0024_terminal_dends"

# Baseline multiplier value (sanity-check constant).
BASELINE_MULTIPLIER: float = 1.0

# Section-length assertion tolerance (micrometres).
LENGTH_ASSERT_TOL_UM: float = 1e-9

# Seed formula constants (REQ-6, seed uniqueness across 840 trials).
SEED_LENGTH_STRIDE: int = 10_000_003
SEED_ANGLE_STRIDE: int = 1000
