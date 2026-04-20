"""Weighted-Euclidean-in-normalised-space tuning-curve loss.

Given a target curve and a candidate curve, compute residuals on DSI, peak, null and HWHM,
normalise each by the corresponding envelope half-width, and combine them into a single
scalar loss with the supplied weights. Also compute RMSE on the 12 per-angle firing rates
and the split-half reliability for the candidate. The ``ScoreReport`` dataclass carries all
individual residuals, diagnostics, and the envelope pass flag.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.envelope import (
    DEFAULT_ENVELOPE,
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
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.weights import (
    DEFAULT_WEIGHTS,
    ENVELOPE_HALF_WIDTHS,
    load_weights_from_json,
    validate_weights,
)

# Mapping from the four scoring axes to the metric keys registered in meta/metrics/.
METRIC_KEY_DSI: str = "direction_selectivity_index"
METRIC_KEY_HWHM: str = "tuning_curve_hwhm_deg"
METRIC_KEY_RELIABILITY: str = "tuning_curve_reliability"
METRIC_KEY_RMSE: str = "tuning_curve_rmse"


@dataclass(frozen=True, slots=True)
class TuningCurveMetrics:
    """All four per-curve metrics, plus optional reliability when trials are present."""

    dsi: float
    peak_hz: float
    null_hz: float
    hwhm_deg: float
    reliability: float | None


@dataclass(frozen=True, slots=True)
class ScoreReport:
    """Full scoring output.

    Carries every individual residual (plan REQ-1 API surface) plus the ``residuals`` and
    ``normalized_residuals`` dicts used internally by the loss computation.
    """

    loss_scalar: float
    dsi_residual: float
    peak_residual_hz: float
    null_residual_hz: float
    hwhm_residual_deg: float
    rmse_vs_target: float | None
    reliability: float
    passes_envelope: bool
    per_target_pass: dict[str, bool]
    residuals: dict[str, float]
    normalized_residuals: dict[str, float]
    weights_used: dict[str, float]
    candidate_metrics: TuningCurveMetrics
    target_metrics: TuningCurveMetrics
    half_widths_used: dict[str, float] = field(default_factory=lambda: dict(ENVELOPE_HALF_WIDTHS))

    def to_metrics_dict(self) -> dict[str, float | None]:
        """Return a dict keyed by registered meta/metrics/ names.

        Caller can dump the dict straight into ``results/metrics.json``.
        """
        return {
            METRIC_KEY_DSI: self.candidate_metrics.dsi,
            METRIC_KEY_HWHM: self.candidate_metrics.hwhm_deg,
            METRIC_KEY_RELIABILITY: self.reliability,
            METRIC_KEY_RMSE: self.rmse_vs_target,
        }


# Alias exported so callers that prefer ``ScoreResult`` naming also work.
ScoreResult = ScoreReport


def _compute_metrics(*, curve: TuningCurve) -> TuningCurveMetrics:
    return TuningCurveMetrics(
        dsi=compute_dsi(curve=curve),
        peak_hz=compute_peak_hz(curve=curve),
        null_hz=compute_null_hz(curve=curve),
        hwhm_deg=compute_hwhm_deg(curve=curve),
        reliability=compute_reliability(curve=curve),
    )


def _rmse(*, target: TuningCurve, candidate: TuningCurve) -> float | None:
    if target.firing_rates_hz.shape != candidate.firing_rates_hz.shape:
        return None
    diff: np.ndarray = candidate.firing_rates_hz - target.firing_rates_hz
    return float(np.sqrt(np.mean(diff**2)))


def _resolve_weights(
    *,
    weights: dict[str, float] | None,
    weights_path: Path | None,
) -> dict[str, float]:
    if weights is not None and weights_path is not None:
        raise ValueError("pass only one of weights= or weights_path=, not both")
    if weights_path is not None:
        return load_weights_from_json(json_path=weights_path)
    if weights is not None:
        validate_weights(weights=weights)
        return dict(weights)
    return dict(DEFAULT_WEIGHTS)


def score_curves(
    *,
    target: TuningCurve,
    candidate: TuningCurve,
    weights: dict[str, float] | None = None,
    envelope: Envelope | None = None,
    weights_path: Path | None = None,
) -> ScoreReport:
    """Core scoring function operating on two ``TuningCurve`` objects."""
    resolved_weights: dict[str, float] = _resolve_weights(
        weights=weights,
        weights_path=weights_path,
    )
    env: Envelope = envelope if envelope is not None else DEFAULT_ENVELOPE

    target_metrics: TuningCurveMetrics = _compute_metrics(curve=target)
    candidate_metrics: TuningCurveMetrics = _compute_metrics(curve=candidate)

    residuals: dict[str, float] = {
        "dsi": candidate_metrics.dsi - target_metrics.dsi,
        "peak": candidate_metrics.peak_hz - target_metrics.peak_hz,
        "null": candidate_metrics.null_hz - target_metrics.null_hz,
        "hwhm": candidate_metrics.hwhm_deg - target_metrics.hwhm_deg,
    }
    normalized_residuals: dict[str, float] = {
        key: residuals[key] / ENVELOPE_HALF_WIDTHS[key] for key in residuals
    }

    squared_sum: float = 0.0
    for key, nrm in normalized_residuals.items():
        squared_sum += resolved_weights[key] * (nrm**2)
    loss_scalar: float = math.sqrt(squared_sum) if squared_sum > 0.0 else 0.0

    rmse: float | None = _rmse(target=target, candidate=candidate)

    envelope_report: EnvelopeReport = check_envelope(
        dsi=candidate_metrics.dsi,
        peak_hz=candidate_metrics.peak_hz,
        null_hz=candidate_metrics.null_hz,
        hwhm_deg=candidate_metrics.hwhm_deg,
        envelope=env,
    )

    # Reliability defaults to 1.0 when trials are absent (perfectly repeatable mean).
    reliability_value: float = (
        candidate_metrics.reliability if candidate_metrics.reliability is not None else 1.0
    )

    return ScoreReport(
        loss_scalar=loss_scalar,
        dsi_residual=residuals["dsi"],
        peak_residual_hz=residuals["peak"],
        null_residual_hz=residuals["null"],
        hwhm_residual_deg=residuals["hwhm"],
        rmse_vs_target=rmse,
        reliability=reliability_value,
        passes_envelope=envelope_report.passes_envelope,
        per_target_pass=envelope_report.per_target_pass,
        residuals=residuals,
        normalized_residuals=normalized_residuals,
        weights_used=resolved_weights,
        candidate_metrics=candidate_metrics,
        target_metrics=target_metrics,
    )


def score(
    simulated_curve_csv: Path,
    target_curve_csv: Path | None = None,
    *,
    weights: dict[str, float] | None = None,
    envelope: Envelope | None = None,
    weights_path: Path | None = None,
) -> ScoreReport:
    """High-level CSV -> ScoreReport entry point (plan REQ-1).

    ``target_curve_csv=None`` defaults to the canonical t0004 target. Accepts either
    CSV schema supported by ``load_tuning_curve``.
    """
    from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.paths import (
        TARGET_MEAN_CSV,
    )

    target_path: Path = target_curve_csv if target_curve_csv is not None else TARGET_MEAN_CSV
    target_curve: TuningCurve = load_tuning_curve(csv_path=target_path)
    candidate_curve: TuningCurve = load_tuning_curve(csv_path=simulated_curve_csv)
    return score_curves(
        target=target_curve,
        candidate=candidate_curve,
        weights=weights,
        envelope=envelope,
        weights_path=weights_path,
    )
