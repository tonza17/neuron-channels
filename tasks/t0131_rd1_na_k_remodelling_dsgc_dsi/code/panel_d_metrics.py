"""Metrics for the three-pulse response (panel D): shared by the toy model and NEURON test."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    BASELINE_WINDOWS_MS,
    PULSE_CENTERS_MS,
    PULSE_SIGMA_MS,
)

PEAK_SEARCH_HALF_WIDTH_MS: float = 100.0


@dataclass(frozen=True, slots=True)
class PulseMetrics:
    peak_heights: list[float]
    mean_peak: float
    baseline_abs: float
    baseline_rel: float | None
    mean_min_between: float | None
    distinctness: float | None
    mean_fwhm_ms: float | None
    locking_r: float | None


def input_signal(*, t_ms: NDArray[np.float64]) -> NDArray[np.float64]:
    env = np.zeros_like(t_ms)
    for c in PULSE_CENTERS_MS:
        env += np.exp(-0.5 * ((t_ms - c) / PULSE_SIGMA_MS) ** 2)
    return env / float(env.max())


def gaussian_smooth(*, y: NDArray[np.float64], sigma_bins: float) -> NDArray[np.float64]:
    if sigma_bins <= 0.0:
        return y.copy()
    half = int(np.ceil(4.0 * sigma_bins))
    x = np.arange(-half, half + 1, dtype=np.float64)
    k = np.exp(-0.5 * (x / sigma_bins) ** 2)
    k /= k.sum()
    padded = np.pad(y, (half, half), mode="edge")
    return np.convolve(padded, k, mode="valid")


def pulse_metrics(*, t_ms: NDArray[np.float64], y: NDArray[np.float64]) -> PulseMetrics:
    """Metrics on a response trace ``y`` sampled at ``t_ms`` (unnormalised units)."""
    heights: list[float] = []
    peak_t: list[float] = []
    for c in PULSE_CENTERS_MS:
        m = (t_ms >= c - PEAK_SEARCH_HALF_WIDTH_MS) & (t_ms <= c + PEAK_SEARCH_HALF_WIDTH_MS)
        idx = np.nonzero(m)[0]
        j = int(idx[int(np.argmax(y[idx]))])
        heights.append(float(y[j]))
        peak_t.append(float(t_ms[j]))
    mean_peak = float(np.mean(heights))
    base_mask = np.zeros_like(t_ms, dtype=bool)
    for lo, hi in BASELINE_WINDOWS_MS:
        base_mask |= (t_ms >= lo) & (t_ms < hi)
    baseline_abs = float(np.mean(y[base_mask]))
    mins: list[float] = []
    for a, b in zip(peak_t[:-1], peak_t[1:], strict=True):
        m = (t_ms >= a) & (t_ms <= b)
        mins.append(float(np.min(y[m])))
    mean_min = float(np.mean(mins)) if len(mins) > 0 else None
    fwhms: list[float] = []
    for hgt, tp, c in zip(heights, peak_t, PULSE_CENTERS_MS, strict=True):
        m = (t_ms >= c - PEAK_SEARCH_HALF_WIDTH_MS) & (t_ms <= c + PEAK_SEARCH_HALF_WIDTH_MS)
        local_min = float(np.min(y[m]))
        half = local_min + 0.5 * (hgt - local_min)
        above = (y >= half) & m
        if hgt - local_min <= 0.0 or not bool(above.any()):
            continue
        tt = t_ms[above]
        fwhms.append(float(tt.max() - tt.min()))
        _ = tp
    inp = input_signal(t_ms=t_ms)
    locking: float | None = None
    if float(np.std(y)) > 0.0:
        locking = float(np.corrcoef(y, inp)[0, 1])
    distinct: float | None = None
    if mean_min is not None and mean_peak > 0.0:
        distinct = (mean_peak - mean_min) / mean_peak
    return PulseMetrics(
        peak_heights=heights,
        mean_peak=mean_peak,
        baseline_abs=baseline_abs,
        baseline_rel=(baseline_abs / mean_peak) if mean_peak > 0.0 else None,
        mean_min_between=mean_min,
        distinctness=distinct,
        mean_fwhm_ms=float(np.mean(fwhms)) if len(fwhms) > 0 else None,
        locking_r=locking,
    )
