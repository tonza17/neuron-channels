"""5-seed substrate-rate statistics (mean / SD / SE / normal-approx CI / bootstrap CI).

The bootstrap CI is the new t0121 computation: ``B = 10000`` resamples of
the 5 per-seed rates with replacement, mean of each resample, 2.5/97.5
percentiles. Reproducibility comes from the fixed ``BOOTSTRAP_SEED = 42``
into ``numpy.random.default_rng``.

Both stats outputs (mean, SE) are asserted against the brainstorm-session-23
anchor (2.58% / 1.50%) before any chart or asset is written.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from tasks.t0121_5seed_substrate_rate_canonical_report.code.constants import (
    BOOTSTRAP_B,
    BOOTSTRAP_PERCENTILES,
    BOOTSTRAP_SEED,
    EXPECTED_MEAN_PCT,
    EXPECTED_N_SEEDS_ABOVE_HAY,
    EXPECTED_SE_PCT,
    HAY_2011_RATE_PCT,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.per_seed import (
    PerSeedSummary,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.seed_metadata import (
    ALL_SEED_KEYS,
)

_NORMAL_APPROX_Z: float = 1.96


@dataclass(frozen=True, slots=True)
class SubstrateStats:
    mean_pct: float
    sample_sd_pct: float
    sample_se_pct: float
    normal_approx_ci_lo_pct: float
    normal_approx_ci_hi_pct: float
    bootstrap_ci_lo_pct: float
    bootstrap_ci_hi_pct: float
    n_seeds_above_hay_envelope: int


def compute_substrate_stats(
    *,
    summaries: dict[str, PerSeedSummary],
) -> SubstrateStats:
    """Compute 5-seed mean / SD / SE / both 95% CIs from the per-seed summaries.

    Asserts that the result matches the brainstorm-session-23 anchor
    (mean = 2.58, SE = 1.50, n_seeds_above_hay = 3) within rounding.
    """
    rates: list[float] = [summaries[k].acceptance_rate_pct for k in ALL_SEED_KEYS]
    rates_arr: np.ndarray = np.asarray(rates, dtype=np.float64)
    n: int = rates_arr.shape[0]
    assert n == len(ALL_SEED_KEYS), "n_rates equals the canonical seed count"

    mean_pct: float = float(np.mean(rates_arr))
    sample_sd_pct: float = float(np.std(rates_arr, ddof=1))
    sample_se_pct: float = sample_sd_pct / float(np.sqrt(n))

    normal_lo: float = mean_pct - _NORMAL_APPROX_Z * sample_se_pct
    normal_hi: float = mean_pct + _NORMAL_APPROX_Z * sample_se_pct

    rng = np.random.default_rng(seed=BOOTSTRAP_SEED)
    samples: np.ndarray = rng.choice(rates_arr, size=(BOOTSTRAP_B, n), replace=True)
    sample_means: np.ndarray = samples.mean(axis=1)
    bootstrap_lo, bootstrap_hi = (
        float(p) for p in np.percentile(sample_means, list(BOOTSTRAP_PERCENTILES))
    )

    n_above_hay: int = int(sum(1 for r in rates if r > HAY_2011_RATE_PCT))

    assert abs(mean_pct - EXPECTED_MEAN_PCT) < 0.01, (
        f"5-seed mean is {EXPECTED_MEAN_PCT} +/- 0.01, got {mean_pct:.4f}"
    )
    assert abs(sample_se_pct - EXPECTED_SE_PCT) < 0.01, (
        f"5-seed sample SE is {EXPECTED_SE_PCT} +/- 0.01, got {sample_se_pct:.4f}"
    )
    assert n_above_hay == EXPECTED_N_SEEDS_ABOVE_HAY, (
        f"n_seeds above Hay envelope is {EXPECTED_N_SEEDS_ABOVE_HAY}, got {n_above_hay}"
    )

    return SubstrateStats(
        mean_pct=mean_pct,
        sample_sd_pct=sample_sd_pct,
        sample_se_pct=sample_se_pct,
        normal_approx_ci_lo_pct=normal_lo,
        normal_approx_ci_hi_pct=normal_hi,
        bootstrap_ci_lo_pct=bootstrap_lo,
        bootstrap_ci_hi_pct=bootstrap_hi,
        n_seeds_above_hay_envelope=n_above_hay,
    )
