"""Canonical constants for the t0035 distal-diameter sweep on the t0024 DSGC port.

Defines the sweep grid, CSV column names, the metric keys used in ``results/metrics.json``, and the
slope-sign classification thresholds used by ``classify_slope.py``. Merges t0030's diameter-sweep
constants (slope-sign taxonomy) with t0034's t0024-specific seed/AR(2) constants
(``N_TRIALS_T0024``, ``AR2_RHO``, seed-stride formulas).
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

# Preflight sweep grid (validation gate): exercise extremes plus baseline.
PREFLIGHT_DIAMETER_MULTIPLIERS: tuple[float, ...] = (0.5, 1.0, 2.0)
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

# Slope-sign classification thresholds (REQ-8, REQ-9, REQ-12).
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
DISTAL_IDENTIFICATION_RULE: str = "t0024_terminal_dends"

# Baseline multiplier value (sanity-check constant).
BASELINE_MULTIPLIER: float = 1.0

# Section-diameter assertion tolerance (micrometres). NEURON stores ``seg.diam`` in single
# precision internally, so round-trip rescaling can introduce up to a few ``1e-8`` um error at
# multipliers near the float-precision edge. Set tolerance at 1e-6 um which is far below any
# physiologically meaningful scale.
DIAMETER_ASSERT_TOL_UM: float = 1e-6

# Seed formula constants (REQ-16, seed uniqueness across 840 trials).
SEED_DIAMETER_STRIDE: int = 10_000_003
SEED_ANGLE_STRIDE: int = 1000
