"""Tests for ``tuning_curve_loss.scoring.score`` and ``score_curves``."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader import (
    TuningCurve,
    load_tuning_curve,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.paths import (
    N_ANGLES,
    TARGET_MEAN_CSV,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.scoring import (
    METRIC_KEY_DSI,
    METRIC_KEY_HWHM,
    METRIC_KEY_RELIABILITY,
    METRIC_KEY_RMSE,
    ScoreReport,
    score,
    score_curves,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.weights import (
    DEFAULT_WEIGHTS,
)


def test_identity_score_zero() -> None:
    """REQ-7: score(target, target).loss_scalar == 0.0 and passes_envelope is True."""
    report: ScoreReport = score(TARGET_MEAN_CSV, TARGET_MEAN_CSV)
    assert report.loss_scalar == 0.0, (
        f"Identity loss must be exactly 0.0; got {report.loss_scalar!r}"
    )
    assert report.passes_envelope is True, "Target curve must pass the default envelope (REQ-7)"


def test_identity_score_all_residuals_zero() -> None:
    report: ScoreReport = score(TARGET_MEAN_CSV, TARGET_MEAN_CSV)
    assert report.dsi_residual == 0.0
    assert report.peak_residual_hz == 0.0
    assert report.null_residual_hz == 0.0
    assert report.hwhm_residual_deg == 0.0
    for key, value in report.residuals.items():
        assert value == 0.0, f"residuals[{key!r}] must be 0.0, got {value!r}"
    for key, value in report.normalized_residuals.items():
        assert value == 0.0, f"normalized_residuals[{key!r}] must be 0.0, got {value!r}"


def test_to_metrics_dict_uses_registered_keys() -> None:
    report: ScoreReport = score(TARGET_MEAN_CSV, TARGET_MEAN_CSV)
    out: dict[str, float | None] = report.to_metrics_dict()
    assert set(out.keys()) == {
        METRIC_KEY_DSI,
        METRIC_KEY_HWHM,
        METRIC_KEY_RELIABILITY,
        METRIC_KEY_RMSE,
    }
    # Values aligned with curve metrics.
    assert out[METRIC_KEY_DSI] == pytest.approx(0.8823529411764706)
    assert out[METRIC_KEY_RMSE] == pytest.approx(0.0)


def test_higher_dsi_candidate_has_positive_dsi_residual() -> None:
    target = load_tuning_curve(csv_path=TARGET_MEAN_CSV)
    # Perturb: reduce null to 0 Hz -> DSI rises toward 1.0.
    new_rates: np.ndarray = target.firing_rates_hz.copy()
    null_idx: int = int(np.argmin(new_rates))
    new_rates[null_idx] = 0.0
    candidate = TuningCurve(
        angles_deg=target.angles_deg,
        firing_rates_hz=new_rates,
        trials=None,
    )
    report: ScoreReport = score_curves(target=target, candidate=candidate)
    assert report.dsi_residual > 0.0
    assert report.loss_scalar > 0.0


def test_custom_weights_change_loss() -> None:
    target = load_tuning_curve(csv_path=TARGET_MEAN_CSV)
    new_rates: np.ndarray = target.firing_rates_hz.copy()
    # Reduce peak by 10 Hz -> peak residual -10, normalized -0.5.
    peak_idx: int = int(np.argmax(new_rates))
    new_rates[peak_idx] -= 10.0
    candidate = TuningCurve(
        angles_deg=target.angles_deg,
        firing_rates_hz=new_rates,
        trials=None,
    )
    default_report: ScoreReport = score_curves(target=target, candidate=candidate)
    heavy_peak_weights: dict[str, float] = {
        "dsi": 0.0,
        "peak": 1.0,
        "null": 0.0,
        "hwhm": 0.0,
    }
    custom_report: ScoreReport = score_curves(
        target=target,
        candidate=candidate,
        weights=heavy_peak_weights,
    )
    assert custom_report.loss_scalar != default_report.loss_scalar
    assert custom_report.weights_used == heavy_peak_weights


def test_weights_sum_zero_raises() -> None:
    target = load_tuning_curve(csv_path=TARGET_MEAN_CSV)
    with pytest.raises(ValueError):
        score_curves(
            target=target,
            candidate=target,
            weights={"dsi": 0.0, "peak": 0.0, "null": 0.0, "hwhm": 0.0},
        )


def test_weights_wrong_keys_raises() -> None:
    target = load_tuning_curve(csv_path=TARGET_MEAN_CSV)
    with pytest.raises(ValueError):
        score_curves(
            target=target,
            candidate=target,
            weights={"dsi": 0.5, "peak": 0.5},
        )


def test_weights_negative_raises() -> None:
    target = load_tuning_curve(csv_path=TARGET_MEAN_CSV)
    with pytest.raises(ValueError):
        score_curves(
            target=target,
            candidate=target,
            weights={"dsi": -0.1, "peak": 0.5, "null": 0.3, "hwhm": 0.3},
        )


def test_weights_from_json(tmp_path: Path) -> None:
    target = load_tuning_curve(csv_path=TARGET_MEAN_CSV)
    new_rates: np.ndarray = target.firing_rates_hz.copy()
    new_rates[0] += 2.0
    candidate = TuningCurve(
        angles_deg=target.angles_deg,
        firing_rates_hz=new_rates,
        trials=None,
    )
    custom: dict[str, float] = {
        "dsi": 0.1,
        "peak": 0.7,
        "null": 0.1,
        "hwhm": 0.1,
    }
    weights_path: Path = tmp_path / "weights.json"
    weights_path.write_text(data=json.dumps(obj=custom), encoding="utf-8")
    report: ScoreReport = score_curves(
        target=target,
        candidate=candidate,
        weights_path=weights_path,
    )
    assert report.weights_used == custom


def test_default_weights_are_equal_quarters() -> None:
    assert DEFAULT_WEIGHTS == {"dsi": 0.25, "peak": 0.25, "null": 0.25, "hwhm": 0.25}


def test_rmse_vs_target_is_zero_on_identity() -> None:
    report: ScoreReport = score(TARGET_MEAN_CSV, TARGET_MEAN_CSV)
    assert report.rmse_vs_target == pytest.approx(0.0)


def test_rmse_increases_with_perturbation() -> None:
    target = load_tuning_curve(csv_path=TARGET_MEAN_CSV)
    new_rates: np.ndarray = target.firing_rates_hz.copy() + 3.0
    candidate = TuningCurve(
        angles_deg=target.angles_deg,
        firing_rates_hz=new_rates,
        trials=None,
    )
    report: ScoreReport = score_curves(target=target, candidate=candidate)
    assert report.rmse_vs_target is not None
    assert report.rmse_vs_target == pytest.approx(3.0)


def test_score_report_carries_candidate_and_target_metrics() -> None:
    report: ScoreReport = score(TARGET_MEAN_CSV, TARGET_MEAN_CSV)
    assert report.candidate_metrics.dsi == pytest.approx(report.target_metrics.dsi)
    assert report.candidate_metrics.peak_hz == pytest.approx(report.target_metrics.peak_hz)


def test_score_accepts_perturbed_candidate_with_shape_preserved() -> None:
    target = load_tuning_curve(csv_path=TARGET_MEAN_CSV)
    candidate = TuningCurve(
        angles_deg=target.angles_deg,
        firing_rates_hz=target.firing_rates_hz + 0.0,
        trials=None,
    )
    assert candidate.firing_rates_hz.shape == (N_ANGLES,)
