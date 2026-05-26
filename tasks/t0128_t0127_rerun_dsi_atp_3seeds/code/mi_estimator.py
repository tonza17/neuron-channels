"""Two-tier MI estimator for the t0123 NSGA-II run.

Tier 1 (inner loop): ``compute_mi_count_bits`` -- spike-count plug-in MI
on the (direction x spike_count_bin) contingency table with Miller-Madow
bias correction. Used as the cheap selection signal inside NSGA-II.

Tier 2 (post-hoc, top-10 only): ``compute_mi_strong_bialek_bits_per_sec``
-- Strong & Bialek 1998 direct-method MI with 1/T extrapolation. Used as
the literature-comparable bits/s quantity for the Niven 2007 comparison.

References:

* Strong et al., Phys Rev Lett 80, 197 (1998),
  DOI 10.1103/PhysRevLett.80.197 -- direct method for MI on spike trains.
* Miller & Madow (1955) bias correction:
  ``MI_corr = MI_plugin - (R-1)(C-1)/(2N ln 2)`` for R x C contingency
  table with N samples; correction in bits when ``MI_plugin`` is in
  bits.
* Niven et al., J Exp Biol 210, 1797 (2007), DOI 10.1242/jeb.005249 --
  the fly-photoreceptor bits/s vs cost curve we compare against.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.stats import linregress
from sklearn.metrics import mutual_info_score

N_SPIKE_COUNT_BINS_DEFAULT: int = 4
TRIAL_DURATION_MS_DEFAULT: float = 1400.0
DT_MS_DEFAULT: float = 5.0
WORD_LENGTHS_MS_DEFAULT: tuple[int, ...] = (25, 50, 75, 100)


@dataclass(frozen=True, slots=True)
class StrongBialekResult:
    """Strong-Bialek 1998 1/T-extrapolated MI rate (bits/s)."""

    bits_per_sec: float
    std_err_bits_per_sec: float
    r_squared: float
    h_total_per_t: dict[int, float]
    h_noise_per_t: dict[int, float]


def _bin_spike_counts(
    *,
    spike_counts: NDArray[np.int_],
    n_bins: int,
) -> NDArray[np.int_]:
    """Bin spike counts into ``n_bins`` quantile bins.

    Falls back to per-unique-value bins when ``len(unique) <= n_bins``.
    Returns an array of bin indices in ``[0, n_bins-1]``.
    """
    if spike_counts.size == 0:
        return np.zeros(0, dtype=np.int_)
    unique = np.unique(spike_counts)
    if unique.size <= n_bins:
        mapping: dict[int, int] = {int(v): i for i, v in enumerate(unique)}
        return np.array(
            [mapping[int(v)] for v in spike_counts],
            dtype=np.int_,
        )
    # Quantile-based binning otherwise.
    quantiles = np.linspace(0.0, 1.0, n_bins + 1)[1:-1]
    edges = np.quantile(spike_counts.astype(np.float64), quantiles)
    return np.digitize(spike_counts, edges).astype(np.int_)


def compute_mi_count_bits(
    *,
    direction_labels: NDArray[np.int_],
    spike_counts: NDArray[np.int_],
    n_bins: int = N_SPIKE_COUNT_BINS_DEFAULT,
) -> float:
    """Spike-count plug-in MI with Miller-Madow correction, in bits.

    ``direction_labels`` is an array of integer direction indices (one
    per trial); ``spike_counts`` is the corresponding integer spike count
    per trial. R = number of unique directions; C = number of unique
    spike-count bins after quantile binning; N = total trials.
    """
    if direction_labels.size == 0 or spike_counts.size == 0:
        return 0.0
    if direction_labels.size != spike_counts.size:
        return 0.0
    bins = _bin_spike_counts(spike_counts=spike_counts, n_bins=n_bins)
    # sklearn returns nats; divide by ln(2) for bits.
    mi_nats = float(mutual_info_score(direction_labels, bins))
    mi_bits_plugin = mi_nats / math.log(2.0)
    r = int(np.unique(direction_labels).size)
    c = int(np.unique(bins).size)
    n = int(direction_labels.size)
    if r < 2 or c < 2 or n < 2:
        return max(0.0, mi_bits_plugin)
    bias_bits = (r - 1) * (c - 1) / (2.0 * n * math.log(2.0))
    mi_bits = mi_bits_plugin - bias_bits
    return max(0.0, mi_bits)


def _spike_train_to_binary_word(
    *,
    spike_times_ms: NDArray[np.float64],
    word_start_ms: float,
    word_length_ms: float,
    dt_ms: float,
) -> tuple[int, ...]:
    n_bins = max(1, int(round(word_length_ms / dt_ms)))
    bins = np.zeros(n_bins, dtype=np.int_)
    if spike_times_ms.size > 0:
        in_window = (spike_times_ms >= word_start_ms) & (
            spike_times_ms < word_start_ms + word_length_ms
        )
        for t in spike_times_ms[in_window]:
            idx = int((t - word_start_ms) // dt_ms)
            if 0 <= idx < n_bins:
                bins[idx] = 1
    return tuple(int(b) for b in bins)


def _word_entropy_bits(*, words: list[tuple[int, ...]]) -> float:
    if len(words) == 0:
        return 0.0
    counts: dict[tuple[int, ...], int] = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    n = float(sum(counts.values()))
    h_bits = 0.0
    for c in counts.values():
        p = c / n
        if p > 0:
            h_bits -= p * math.log2(p)
    return h_bits


def compute_mi_strong_bialek_bits_per_sec(
    *,
    spike_trains_by_direction: dict[float, list[NDArray[np.float64]]],
    word_lengths_ms: tuple[int, ...] = WORD_LENGTHS_MS_DEFAULT,
    dt_ms: float = DT_MS_DEFAULT,
    trial_duration_ms: float = TRIAL_DURATION_MS_DEFAULT,
) -> StrongBialekResult:
    """Strong-Bialek 1998 direct-method MI with 1/T extrapolation, bits/s.

    For each word length ``T`` in ``word_lengths_ms``:

    * Discretise each trial into binary words at resolution ``dt_ms`` and
      length ``T``.
    * Pool words across all directions for ``H_total(T)``.
    * Average ``H_noise(T)`` across directions (per-direction word
      entropy at the same word boundary, averaged over trials).
    * ``MI_at_T = H_total - <H_noise>`` (bits).

    Fit ``MI_at_T / T`` against ``1/T`` via least-squares; the intercept
    is the asymptotic rate in bits/ms. Multiply by 1000 for bits/s.
    """
    if len(spike_trains_by_direction) == 0:
        return StrongBialekResult(
            bits_per_sec=float("nan"),
            std_err_bits_per_sec=float("nan"),
            r_squared=float("nan"),
            h_total_per_t={},
            h_noise_per_t={},
        )
    h_total_per_t: dict[int, float] = {}
    h_noise_per_t: dict[int, float] = {}
    mi_per_t_bits: dict[int, float] = {}
    for t_word_ms in word_lengths_ms:
        all_words: list[tuple[int, ...]] = []
        per_dir_h: list[float] = []
        for _direction, trials in spike_trains_by_direction.items():
            dir_words: list[tuple[int, ...]] = []
            for trial_spike_times in trials:
                t_starts = np.arange(
                    0.0,
                    trial_duration_ms - float(t_word_ms) + 1e-9,
                    float(t_word_ms),
                    dtype=np.float64,
                )
                for t_start in t_starts:
                    w = _spike_train_to_binary_word(
                        spike_times_ms=trial_spike_times,
                        word_start_ms=float(t_start),
                        word_length_ms=float(t_word_ms),
                        dt_ms=dt_ms,
                    )
                    dir_words.append(w)
                    all_words.append(w)
            if len(dir_words) > 0:
                per_dir_h.append(_word_entropy_bits(words=dir_words))
        h_total = _word_entropy_bits(words=all_words)
        h_noise = float(np.mean(per_dir_h)) if len(per_dir_h) > 0 else 0.0
        h_total_per_t[int(t_word_ms)] = h_total
        h_noise_per_t[int(t_word_ms)] = h_noise
        mi_per_t_bits[int(t_word_ms)] = max(0.0, h_total - h_noise)
    # Fit (MI_at_T / T_ms) vs (1 / T_ms); intercept = bits/ms.
    ts = np.array(sorted(mi_per_t_bits.keys()), dtype=np.float64)
    if ts.size < 2:
        return StrongBialekResult(
            bits_per_sec=float("nan"),
            std_err_bits_per_sec=float("nan"),
            r_squared=float("nan"),
            h_total_per_t=h_total_per_t,
            h_noise_per_t=h_noise_per_t,
        )
    inv_t = 1.0 / ts
    mi_rates = np.array([mi_per_t_bits[int(t)] / float(t) for t in ts], dtype=np.float64)
    fit = linregress(inv_t, mi_rates)
    intercept_bits_per_ms = float(fit.intercept)
    bits_per_sec = intercept_bits_per_ms * 1000.0
    r_squared = float(fit.rvalue) ** 2
    std_err_bits_per_sec = float(fit.intercept_stderr) * 1000.0
    return StrongBialekResult(
        bits_per_sec=bits_per_sec,
        std_err_bits_per_sec=std_err_bits_per_sec,
        r_squared=r_squared,
        h_total_per_t=h_total_per_t,
        h_noise_per_t=h_noise_per_t,
    )


__all__ = [
    "DT_MS_DEFAULT",
    "N_SPIKE_COUNT_BINS_DEFAULT",
    "StrongBialekResult",
    "TRIAL_DURATION_MS_DEFAULT",
    "WORD_LENGTHS_MS_DEFAULT",
    "compute_mi_count_bits",
    "compute_mi_strong_bialek_bits_per_sec",
]
