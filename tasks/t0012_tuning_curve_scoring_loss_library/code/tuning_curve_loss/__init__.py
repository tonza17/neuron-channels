"""Public API for the ``tuning_curve_loss`` library.

Re-exports the scoring entry points, the four ``compute_*`` helpers, the canonical dataclasses,
the tuning-curve CSV schema constant, and the weight / envelope defaults.
"""

from __future__ import annotations

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.envelope import (
    DEFAULT_ENVELOPE,
    DSI_ENVELOPE,
    HWHM_ENVELOPE_DEG,
    NULL_ENVELOPE_HZ,
    PEAK_ENVELOPE_HZ,
    Envelope,
    EnvelopeReport,
    check_envelope,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader import (
    TuningCurve,
    load_tuning_curve,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics import (
    compute_dsi,
    compute_hwhm_deg,
    compute_null_hz,
    compute_peak_hz,
    compute_reliability,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.paths import (
    TUNING_CURVE_CSV_COLUMNS,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.scoring import (
    METRIC_KEY_DSI,
    METRIC_KEY_HWHM,
    METRIC_KEY_RELIABILITY,
    METRIC_KEY_RMSE,
    ScoreReport,
    ScoreResult,
    TuningCurveMetrics,
    score,
    score_curves,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.weights import (
    DEFAULT_WEIGHTS,
    ENVELOPE_HALF_WIDTHS,
    load_weights_from_json,
    validate_weights,
)

# Public compute_preferred_peak_hz / compute_null_residual_hz aliases for the plan's REQ-2 API.
compute_preferred_peak_hz = compute_peak_hz
compute_null_residual_hz = compute_null_hz


__all__ = [
    "DEFAULT_ENVELOPE",
    "DEFAULT_WEIGHTS",
    "DSI_ENVELOPE",
    "ENVELOPE_HALF_WIDTHS",
    "Envelope",
    "EnvelopeReport",
    "HWHM_ENVELOPE_DEG",
    "METRIC_KEY_DSI",
    "METRIC_KEY_HWHM",
    "METRIC_KEY_RELIABILITY",
    "METRIC_KEY_RMSE",
    "NULL_ENVELOPE_HZ",
    "PEAK_ENVELOPE_HZ",
    "ScoreReport",
    "ScoreResult",
    "TUNING_CURVE_CSV_COLUMNS",
    "TuningCurve",
    "TuningCurveMetrics",
    "check_envelope",
    "compute_dsi",
    "compute_hwhm_deg",
    "compute_null_hz",
    "compute_null_residual_hz",
    "compute_peak_hz",
    "compute_preferred_peak_hz",
    "compute_reliability",
    "load_tuning_curve",
    "load_weights_from_json",
    "score",
    "score_curves",
    "validate_weights",
]
