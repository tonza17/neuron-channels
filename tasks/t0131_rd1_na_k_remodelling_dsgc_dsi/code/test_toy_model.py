"""Unit tests for the panel D toy model anchors and the pulse metrics helpers."""

import numpy as np
import pytest

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.panel_d_metrics import (
    gaussian_smooth,
    input_signal,
    pulse_metrics,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.run_toy_model import (
    fit_toy,
    static_value,
    temporal_metrics,
)


def test_toy_anchors_hold_on_fitted_parameters() -> None:
    fit = fit_toy()
    sat_wt = static_value(params=fit.wt, u=20.0) / static_value(params=fit.wt, u=100.0)
    sat_rd1 = static_value(params=fit.rd1, u=20.0) / static_value(params=fit.rd1, u=100.0)
    assert sat_wt < 0.6, "WT-like toy output grows gradually"
    assert sat_rd1 >= 0.9, "rd1-like toy output saturates early"
    assert 0.25 <= temporal_metrics(params=fit.rd1).baseline_abs <= 0.45
    assert temporal_metrics(params=fit.wt).baseline_abs < 0.05


def test_pulse_metrics_on_input_itself() -> None:
    t = np.arange(0.0, 1000.0, 1.0)
    m = pulse_metrics(t_ms=t, y=input_signal(t_ms=t))
    assert m.baseline_abs == pytest.approx(0.0, abs=1e-3)
    assert m.distinctness is not None and m.distinctness > 0.99
    assert m.locking_r == pytest.approx(1.0)
    assert m.mean_fwhm_ms is not None and m.mean_fwhm_ms == pytest.approx(2.355 * 20.0, abs=3.0)


def test_gaussian_smooth_preserves_mean() -> None:
    y = np.zeros(200)
    y[100] = 1.0
    s = gaussian_smooth(y=y, sigma_bins=3.0)
    assert float(s.sum()) == pytest.approx(1.0, abs=1e-6)
