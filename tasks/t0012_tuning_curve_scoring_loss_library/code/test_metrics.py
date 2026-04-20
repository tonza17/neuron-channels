"""Tests for ``tuning_curve_loss.metrics``."""

from __future__ import annotations

import numpy as np
import pytest

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader import (
    TuningCurve,
    load_tuning_curve,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics import (
    FLAT_HWHM_DEG,
    compute_dsi,
    compute_hwhm_deg,
    compute_null_hz,
    compute_peak_hz,
    compute_reliability,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.paths import (
    ANGLE_STEP_DEG,
    N_ANGLES,
    TARGET_MEAN_CSV,
)


def _synthetic_cosine_squared_curve(
    *,
    n_angles: int,
    theta_pref_deg: float,
    r_base: float,
    r_peak: float,
    n: float,
) -> TuningCurve:
    angles_deg: np.ndarray = np.linspace(
        start=0.0,
        stop=360.0,
        num=n_angles,
        endpoint=False,
    )
    angles_rad: np.ndarray = np.deg2rad(angles_deg)
    theta_pref_rad: float = float(np.deg2rad(theta_pref_deg))
    cos_term: np.ndarray = (1.0 + np.cos(angles_rad - theta_pref_rad)) / 2.0
    amplitude: float = r_peak - r_base
    rates: np.ndarray = r_base + amplitude * (cos_term**n)
    return TuningCurve(
        angles_deg=angles_deg,
        firing_rates_hz=rates,
        trials=None,
    )


def test_peak_and_null_match_target() -> None:
    curve = load_tuning_curve(csv_path=TARGET_MEAN_CSV)
    assert compute_peak_hz(curve=curve) == pytest.approx(32.0)
    assert compute_null_hz(curve=curve) == pytest.approx(2.0)


def test_dsi_matches_t0004_formula() -> None:
    curve = load_tuning_curve(csv_path=TARGET_MEAN_CSV)
    expected: float = (32.0 - 2.0) / (32.0 + 2.0)  # = 0.8823529411764706
    assert compute_dsi(curve=curve) == pytest.approx(expected, rel=0.0, abs=1e-12)


def test_dsi_zero_denominator_returns_zero() -> None:
    rates: np.ndarray = np.zeros(shape=N_ANGLES, dtype=np.float64)
    angles: np.ndarray = np.linspace(0.0, 360.0, N_ANGLES, endpoint=False)
    curve = TuningCurve(angles_deg=angles, firing_rates_hz=rates, trials=None)
    assert compute_dsi(curve=curve) == 0.0


def test_hwhm_symmetric_cosine_squared() -> None:
    curve = _synthetic_cosine_squared_curve(
        n_angles=N_ANGLES,
        theta_pref_deg=90.0,
        r_base=2.0,
        r_peak=32.0,
        n=2.0,
    )
    # Closed-form: ((1 + cos phi)/2)^2 = 0.5 => phi = arccos(sqrt(2) - 1) approx 65.53 deg.
    analytical: float = float(np.rad2deg(np.arccos(np.sqrt(2.0) - 1.0)))
    interpolated: float = compute_hwhm_deg(curve=curve)
    # On a 30 deg grid the linear interpolation is within ~1 deg of the analytical value.
    assert abs(interpolated - analytical) < 2.0, (
        f"HWHM off grid: interpolated={interpolated:.3f}, analytical={analytical:.3f}"
    )


def test_hwhm_flat_curve_returns_flat_sentinel() -> None:
    angles: np.ndarray = np.linspace(0.0, 360.0, N_ANGLES, endpoint=False)
    rates: np.ndarray = np.full(shape=N_ANGLES, fill_value=7.5, dtype=np.float64)
    curve = TuningCurve(angles_deg=angles, firing_rates_hz=rates, trials=None)
    assert compute_hwhm_deg(curve=curve) == FLAT_HWHM_DEG


def test_hwhm_peak_not_at_index_6_rotates_correctly() -> None:
    # Preferred direction at 0 deg (index 0) instead of 90 deg (index 3).
    curve = _synthetic_cosine_squared_curve(
        n_angles=N_ANGLES,
        theta_pref_deg=0.0,
        r_base=2.0,
        r_peak=32.0,
        n=2.0,
    )
    hwhm: float = compute_hwhm_deg(curve=curve)
    analytical: float = float(np.rad2deg(np.arccos(np.sqrt(2.0) - 1.0)))
    assert abs(hwhm - analytical) < 2.0, (
        f"HWHM with wrap-around peak: got {hwhm:.3f}, expected ~{analytical:.3f}"
    )


def test_reliability_none_when_trials_absent() -> None:
    angles: np.ndarray = np.linspace(0.0, 360.0, N_ANGLES, endpoint=False)
    rates: np.ndarray = np.linspace(2.0, 30.0, N_ANGLES)
    curve = TuningCurve(angles_deg=angles, firing_rates_hz=rates, trials=None)
    assert compute_reliability(curve=curve) is None


def test_reliability_one_for_identical_halves() -> None:
    # Interleave a single realization so even-index and odd-index columns carry the
    # SAME per-trial draw at every angle, guaranteeing even-mean == odd-mean per angle
    # and therefore Pearson r == 1.0 exactly.
    rng: np.random.Generator = np.random.default_rng(seed=7)
    angles: np.ndarray = np.linspace(0.0, 360.0, N_ANGLES, endpoint=False)
    mean_curve: np.ndarray = 10.0 + 15.0 * np.cos(np.deg2rad(angles - 90.0)) ** 2
    n_pairs: int = 4
    base: np.ndarray = mean_curve[:, None] + rng.normal(
        loc=0.0, scale=0.1, size=(N_ANGLES, n_pairs)
    )
    # Repeat each column twice so columns [0, 1] share a value, [2, 3] share a value, ...
    # Even indices (0, 2, 4, 6) and odd indices (1, 3, 5, 7) then have identical per-angle means.
    trials: np.ndarray = np.repeat(a=base, repeats=2, axis=1)
    curve = TuningCurve(
        angles_deg=angles,
        firing_rates_hz=trials.mean(axis=1),
        trials=trials,
    )
    r: float | None = compute_reliability(curve=curve)
    assert r is not None
    assert r == pytest.approx(1.0, abs=1e-12), (
        f"Identical even/odd halves should give reliability 1.0, got {r}"
    )


def test_reliability_zero_variance_returns_none() -> None:
    angles: np.ndarray = np.linspace(0.0, 360.0, N_ANGLES, endpoint=False)
    # Every trial at every angle equals 5.0 -> zero variance -> Pearson undefined.
    trials: np.ndarray = np.full(shape=(N_ANGLES, 4), fill_value=5.0, dtype=np.float64)
    curve = TuningCurve(
        angles_deg=angles,
        firing_rates_hz=trials.mean(axis=1),
        trials=trials,
    )
    assert compute_reliability(curve=curve) is None


def test_reliability_separates_high_vs_low_noise() -> None:
    # Same underlying mean curve, different noise SDs -> different reliability values.
    rng: np.random.Generator = np.random.default_rng(seed=11)
    angles: np.ndarray = np.linspace(0.0, 360.0, N_ANGLES, endpoint=False)
    mean_curve: np.ndarray = 10.0 + 15.0 * np.cos(np.deg2rad(angles - 90.0)) ** 2
    n_trials: int = 40

    low_noise_trials: np.ndarray = np.clip(
        a=mean_curve[:, None] + rng.normal(loc=0.0, scale=0.1, size=(N_ANGLES, n_trials)),
        a_min=0.0,
        a_max=None,
    )
    high_noise_trials: np.ndarray = np.clip(
        a=mean_curve[:, None] + rng.normal(loc=0.0, scale=15.0, size=(N_ANGLES, n_trials)),
        a_min=0.0,
        a_max=None,
    )
    curve_low = TuningCurve(
        angles_deg=angles,
        firing_rates_hz=low_noise_trials.mean(axis=1),
        trials=low_noise_trials,
    )
    curve_high = TuningCurve(
        angles_deg=angles,
        firing_rates_hz=high_noise_trials.mean(axis=1),
        trials=high_noise_trials,
    )
    r_low: float | None = compute_reliability(curve=curve_low)
    r_high: float | None = compute_reliability(curve=curve_high)
    assert r_low is not None and r_high is not None
    assert r_low > 0.9, f"low-noise reliability expected > 0.9, got {r_low}"
    assert r_low > r_high, f"low-noise reliability ({r_low}) must exceed high-noise ({r_high})"


def test_angle_step_is_30_deg() -> None:
    # Sanity: the library's grid constant aligns with the t0004 12-angle grid.
    assert ANGLE_STEP_DEG == 30.0
