"""95 percent bootstrap confidence-interval computation for per-angle firing rates.

Uses :func:`scipy.stats.bootstrap` by default with the constants from
:mod:`tuning_curve_viz.constants`. Falls back to a deterministic NumPy percentile
bootstrap if scipy is unavailable at import time — this keeps the plotting code path
functional even in minimal environments.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants import (
    BOOTSTRAP_CONFIDENCE_LEVEL,
    BOOTSTRAP_METHOD,
    BOOTSTRAP_N_RESAMPLES,
    SMOKE_RNG_SEED,
)

try:
    from scipy.stats import bootstrap as _scipy_bootstrap

    _HAS_SCIPY: bool = True
except ImportError:  # pragma: no cover - exercised only in scipy-less envs
    _HAS_SCIPY = False


@dataclass(frozen=True, slots=True)
class BootstrapCI:
    """95 percent confidence band: two 1-D arrays aligned with ``angles_deg``."""

    ci_low_hz: np.ndarray
    ci_high_hz: np.ndarray


def bootstrap_ci(
    *,
    per_angle_trials: np.ndarray,
    n_resamples: int = BOOTSTRAP_N_RESAMPLES,
    confidence_level: float = BOOTSTRAP_CONFIDENCE_LEVEL,
    rng_seed: int = SMOKE_RNG_SEED,
) -> BootstrapCI:
    """Compute the 95 percent bootstrap CI on the per-angle mean firing rate.

    ``per_angle_trials`` has shape ``(n_angles, n_trials)``. For each angle the bootstrap
    resamples trials with replacement ``n_resamples`` times and reports the percentile
    interval. Uses :func:`scipy.stats.bootstrap` when available; otherwise uses a
    seeded NumPy percentile bootstrap.
    """
    assert per_angle_trials.ndim == 2, "per_angle_trials is 2-D (n_angles, n_trials)"
    n_angles: int = per_angle_trials.shape[0]
    ci_low_hz: np.ndarray = np.empty(shape=(n_angles,), dtype=np.float64)
    ci_high_hz: np.ndarray = np.empty(shape=(n_angles,), dtype=np.float64)

    if _HAS_SCIPY:
        for angle_idx in range(n_angles):
            row: np.ndarray = per_angle_trials[angle_idx]
            result = _scipy_bootstrap(
                (row,),
                statistic=np.mean,
                n_resamples=n_resamples,
                confidence_level=confidence_level,
                method=BOOTSTRAP_METHOD,
                vectorized=True,
                random_state=np.random.default_rng(seed=rng_seed + angle_idx),
            )
            ci_low_hz[angle_idx] = float(result.confidence_interval.low)
            ci_high_hz[angle_idx] = float(result.confidence_interval.high)
        return BootstrapCI(ci_low_hz=ci_low_hz, ci_high_hz=ci_high_hz)

    # NumPy fallback: deterministic seeded percentile bootstrap.
    rng: np.random.Generator = np.random.default_rng(seed=rng_seed)
    alpha: float = (1.0 - confidence_level) / 2.0
    lower_percentile: float = 100.0 * alpha
    upper_percentile: float = 100.0 * (1.0 - alpha)
    for angle_idx in range(n_angles):
        row = per_angle_trials[angle_idx]
        resamples: np.ndarray = rng.choice(
            a=row,
            size=(n_resamples, len(row)),
            replace=True,
        )
        resample_means: np.ndarray = resamples.mean(axis=1)
        ci_low_hz[angle_idx] = float(np.percentile(a=resample_means, q=lower_percentile))
        ci_high_hz[angle_idx] = float(np.percentile(a=resample_means, q=upper_percentile))
    return BootstrapCI(ci_low_hz=ci_low_hz, ci_high_hz=ci_high_hz)
