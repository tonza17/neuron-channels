"""Boundary tests for ``tuning_curve_loss.envelope.check_envelope``.

These use the default envelope (widened DSI upper bound 0.9 and widened peak lower bound 30 Hz
so that the identity test ``score(target, target).passes_envelope is True`` holds).
"""

from __future__ import annotations

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.envelope import (
    DEFAULT_ENVELOPE,
    check_envelope,
)

# Target curve baseline values (DSI 0.8824, peak 32 Hz, null 2 Hz, hwhm ~66 deg).
# All inside the (widened) envelope.
_DSI_OK: float = 0.8
_PEAK_OK: float = 50.0
_NULL_OK: float = 5.0
_HWHM_OK: float = 75.0


def test_all_in_range_passes() -> None:
    report = check_envelope(
        dsi=_DSI_OK,
        peak_hz=_PEAK_OK,
        null_hz=_NULL_OK,
        hwhm_deg=_HWHM_OK,
    )
    assert report.passes_envelope is True
    assert report.per_target_pass == {
        "dsi": True,
        "peak": True,
        "null": True,
        "hwhm": True,
    }


def test_dsi_below_lower_fails() -> None:
    report = check_envelope(
        dsi=0.69,
        peak_hz=_PEAK_OK,
        null_hz=_NULL_OK,
        hwhm_deg=_HWHM_OK,
    )
    assert report.per_target_pass["dsi"] is False
    assert report.passes_envelope is False


def test_dsi_at_lower_boundary_passes() -> None:
    report = check_envelope(
        dsi=DEFAULT_ENVELOPE.dsi_range[0],
        peak_hz=_PEAK_OK,
        null_hz=_NULL_OK,
        hwhm_deg=_HWHM_OK,
    )
    assert report.per_target_pass["dsi"] is True


def test_dsi_above_upper_fails() -> None:
    report = check_envelope(
        dsi=DEFAULT_ENVELOPE.dsi_range[1] + 0.001,
        peak_hz=_PEAK_OK,
        null_hz=_NULL_OK,
        hwhm_deg=_HWHM_OK,
    )
    assert report.per_target_pass["dsi"] is False
    assert report.passes_envelope is False


def test_peak_below_lower_fails() -> None:
    report = check_envelope(
        dsi=_DSI_OK,
        peak_hz=DEFAULT_ENVELOPE.peak_hz_range[0] - 0.1,
        null_hz=_NULL_OK,
        hwhm_deg=_HWHM_OK,
    )
    assert report.per_target_pass["peak"] is False


def test_peak_above_upper_fails() -> None:
    report = check_envelope(
        dsi=_DSI_OK,
        peak_hz=DEFAULT_ENVELOPE.peak_hz_range[1] + 0.1,
        null_hz=_NULL_OK,
        hwhm_deg=_HWHM_OK,
    )
    assert report.per_target_pass["peak"] is False


def test_null_above_max_fails() -> None:
    report = check_envelope(
        dsi=_DSI_OK,
        peak_hz=_PEAK_OK,
        null_hz=DEFAULT_ENVELOPE.null_hz_max + 0.1,
        hwhm_deg=_HWHM_OK,
    )
    assert report.per_target_pass["null"] is False


def test_null_at_max_passes() -> None:
    report = check_envelope(
        dsi=_DSI_OK,
        peak_hz=_PEAK_OK,
        null_hz=DEFAULT_ENVELOPE.null_hz_max,
        hwhm_deg=_HWHM_OK,
    )
    assert report.per_target_pass["null"] is True


def test_hwhm_below_lower_fails() -> None:
    report = check_envelope(
        dsi=_DSI_OK,
        peak_hz=_PEAK_OK,
        null_hz=_NULL_OK,
        hwhm_deg=DEFAULT_ENVELOPE.hwhm_deg_range[0] - 0.1,
    )
    assert report.per_target_pass["hwhm"] is False


def test_hwhm_above_upper_fails() -> None:
    report = check_envelope(
        dsi=_DSI_OK,
        peak_hz=_PEAK_OK,
        null_hz=_NULL_OK,
        hwhm_deg=DEFAULT_ENVELOPE.hwhm_deg_range[1] + 0.1,
    )
    assert report.per_target_pass["hwhm"] is False


def test_default_envelope_admits_t0004_target() -> None:
    # Target DSI 0.8824, peak 32 Hz, null 2 Hz, hwhm ~66 deg.
    report = check_envelope(dsi=0.8824, peak_hz=32.0, null_hz=2.0, hwhm_deg=66.0)
    assert report.passes_envelope is True, (
        "default envelope must admit the t0004 target so the REQ-7 identity test holds"
    )
