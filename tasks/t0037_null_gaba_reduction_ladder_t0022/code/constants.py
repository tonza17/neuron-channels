"""Canonical constants for the t0037 null-GABA reduction ladder on t0022.

Defines the sweep grid (5 GABA levels), CSV column names, metric keys, preflight configuration,
and the two task-specific thresholds:

* ``NULL_HZ_UNPINNING_THRESHOLD_HZ`` -- null-Hz level above which null firing is considered
  "unpinned" from the zero corner. Used by ``classify_slope.py`` to pick the smallest GABA level
  that crosses this bar.
* ``PEAK_HZ_MIN_PRECONDITION_HZ`` -- minimum peak-Hz at the 4 nS (highest-GABA) level to consider
  the ladder interpretable. Below this, the ladder is flagged suspect.

Structural clone of ``tasks/t0036_rerun_t0030_halved_null_gaba/code/constants.py``.
"""

from __future__ import annotations

# Sweep grid (REQ-4). Five GABA null-direction conductances in nS, high-to-low.
GABA_LEVELS_NS: tuple[float, ...] = (4.0, 2.0, 1.0, 0.5, 0.0)

# Preflight sweep grid (validation gate): three GABA levels + three angles + two trials = 18
# trials. Angles and trials match t0036's preflight structure; GABA levels cover both extremes
# (0 and 4 nS) plus a midpoint (2 nS) so the rebind discipline is stressed across values.
PREFLIGHT_GABA_LEVELS_NS: tuple[float, ...] = (0.0, 2.0, 4.0)
PREFLIGHT_ANGLES_DEG: tuple[int, ...] = (0, 90, 180)
PREFLIGHT_N_TRIALS: int = 2

# Distal identification thresholds (kept for bookkeeping even though distal diameter is not
# varied in this task -- the preflight still exercises the identification rule).
DISTAL_MIN_DEPTH: int = 3
DISTAL_MIN_COUNT: int = 50

# Tidy-CSV column names (REQ-4, REQ-5).
CSV_COL_GABA_NULL_NS: str = "gaba_null_ns"
CSV_COL_TRIAL: str = "trial"
CSV_COL_DIRECTION_DEG: str = "direction_deg"
CSV_COL_SPIKE_COUNT: str = "spike_count"
CSV_COL_PEAK_MV: str = "peak_mv"
CSV_COL_FIRING_RATE_HZ: str = "firing_rate_hz"

TIDY_CSV_HEADER: tuple[str, ...] = (
    CSV_COL_GABA_NULL_NS,
    CSV_COL_TRIAL,
    CSV_COL_DIRECTION_DEG,
    CSV_COL_SPIKE_COUNT,
    CSV_COL_PEAK_MV,
    CSV_COL_FIRING_RATE_HZ,
)

# Per-GABA canonical tuning-curve CSV header (accepted by t0012 load_tuning_curve).
CURVE_CSV_HEADER: tuple[str, ...] = (
    "angle_deg",
    "trial_seed",
    "firing_rate_hz",
)

# Metric keys registered under ``meta/metrics/``.
METRIC_KEY_DSI: str = "direction_selectivity_index"
METRIC_KEY_HWHM: str = "tuning_curve_hwhm_deg"
METRIC_KEY_RELIABILITY: str = "tuning_curve_reliability"

# Distal-identification rule label (recorded in logs/preflight/distal_sections.json).
DISTAL_IDENTIFICATION_RULE: str = "hoc_leaves_on_arbor_depth_ge_3"

# Baseline distal diameter multiplier -- never changed in this task; present only so
# ``assert_distal_diameters`` can be called with multiplier=1.0 as a post-simulation integrity
# check (REQ-1).
BASELINE_DIAMETER_MULTIPLIER: float = 1.0

# Section-diameter assertion tolerance (micrometres). See t0036 constants.py for the rationale
# behind the 1e-6 um (= 1 angstrom) tolerance at multipliers near float-precision edges.
DIAMETER_ASSERT_TOL_UM: float = 1e-6

# Midpoint-snapshot tolerance (um). 3D point coordinates are NOT mutated by seg.diam writes in
# NEURON, so this should hold to floating-point exactness.
MIDPOINT_ASSERT_TOL_UM: float = 1e-9

# t0037-specific thresholds (REQ-8, REQ-9).
# The smallest mean null-direction firing rate (Hz) at which null firing is considered
# "unpinned" from the zero corner. Set to 0.1 Hz to match t0036's partial-result threshold for
# continuity with the prior null-Hz pre-condition literature.
NULL_HZ_UNPINNING_THRESHOLD_HZ: float = 0.1

# Pre-condition gate: minimum peak-Hz on the preferred direction at the highest GABA level
# (4 nS) below which the ladder is flagged suspect because preferred-direction firing is broken
# by the override sequencing. Does not halt; records ``_suspect`` suffix on the classifier label.
PEAK_HZ_MIN_PRECONDITION_HZ: float = 10.0
