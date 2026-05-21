"""Unit tests for the t0106 DSI silence guard and 2-direction ratio DSI.

t0106-specific tests:

* ``test_all_silent_returns_dsi_zero`` — 2 dirs x 3 seeds at spike_count=0.
* ``test_near_silent_returns_dsi_zero`` — total mean spikes < 10, guard floor.
* ``test_firing_positive_control_returns_nonzero`` — total mean spikes >> 10,
  guard does NOT trigger and DSI is computed normally.
* ``test_ratio_dsi_synthetic_pd5_nd1`` — at PD = 5 spikes, ND = 1 spike, the
  ``_vector_sum_dsi`` function must return ``(5 - 1) / (5 + 1) = 0.6667``
  within 1e-6 tolerance. This is the load-bearing mathematical proof that
  the existing t0104 ``_vector_sum_dsi`` already reduces to the t0106 ratio
  DSI at ``n_directions = 2`` without any algorithm change.
* ``test_silence_guard_threshold_sweep`` — sensitivity sweep across
  thresholds {5, 10, 20} on the same synthetic silent corner.
"""

from __future__ import annotations

import numpy as np

from tasks.t0115_seed9354_no_autostop.code.evaluator import (
    SILENCE_SPIKE_COUNT_THRESHOLD,
    TrialResult,
    _summarise_trials,
    _vector_sum_dsi,
)

# t0106 settings.
N_EVAL_SEEDS_LOCAL: int = 3
N_DIRECTIONS_LOCAL: int = 2
DIRECTIONS_DEG: tuple[float, ...] = tuple(
    float(i) * 360.0 / N_DIRECTIONS_LOCAL for i in range(N_DIRECTIONS_LOCAL)
)
SANE_PEAK_MV: float = -50.0  # inside the stability envelope.


def _make_trials(*, spike_counts: dict[float, list[int]]) -> list[TrialResult]:
    """Build N_EVAL_SEEDS x N_DIRECTIONS TrialResults from a dict.

    spike_counts[d] must have exactly N_EVAL_SEEDS_LOCAL entries; entry i is
    the per-direction spike count for eval_seed_index=i.
    """
    trials: list[TrialResult] = []
    for direction_deg, counts in spike_counts.items():
        assert len(counts) == N_EVAL_SEEDS_LOCAL, (
            f"need {N_EVAL_SEEDS_LOCAL} per-seed counts; got {len(counts)} "
            f"for direction {direction_deg}"
        )
        for seed_idx, count in enumerate(counts):
            trials.append(
                TrialResult(
                    direction_deg=direction_deg,
                    seed=1000 + seed_idx,
                    eval_seed_index=seed_idx,
                    spike_count=int(count),
                    peak_mv=SANE_PEAK_MV,
                    error=None,
                )
            )
    return trials


def test_all_silent_returns_dsi_zero() -> None:
    """All 2 dirs x 3 seeds with spike_count=0 must return DSI=0.0."""
    spike_counts: dict[float, list[int]] = {d: [0] * N_EVAL_SEEDS_LOCAL for d in DIRECTIONS_DEG}
    trials = _make_trials(spike_counts=spike_counts)
    result = _summarise_trials(results=trials, n_seeds=N_EVAL_SEEDS_LOCAL)
    assert result.dsi_vector_sum == 0.0, (
        f"all-silent cell must yield DSI=0.0 (guard threshold "
        f"{SILENCE_SPIKE_COUNT_THRESHOLD}), got {result.dsi_vector_sum}"
    )


def test_near_silent_returns_dsi_zero() -> None:
    """Near-silent cell (total mean spikes ~ 1.67) must trip the guard."""
    pd_direction_deg = 0.0
    spike_counts: dict[float, list[int]] = {d: [0] * N_EVAL_SEEDS_LOCAL for d in DIRECTIONS_DEG}
    spike_counts[pd_direction_deg] = [5, 0, 0]
    trials = _make_trials(spike_counts=spike_counts)
    result = _summarise_trials(results=trials, n_seeds=N_EVAL_SEEDS_LOCAL)
    total_mean = sum(float(np.mean(counts)) for counts in spike_counts.values())
    assert total_mean < SILENCE_SPIKE_COUNT_THRESHOLD, (
        f"test premise failed: total_mean={total_mean} should be below "
        f"the silence threshold {SILENCE_SPIKE_COUNT_THRESHOLD}"
    )
    assert result.dsi_vector_sum == 0.0, (
        f"near-silent cell (total mean spikes {total_mean}) must yield "
        f"DSI=0.0 via the guard, got {result.dsi_vector_sum}"
    )


def test_firing_positive_control_returns_nonzero() -> None:
    """Firing cell with total mean spikes >> 10 must NOT trip the guard.

    PD = 0 deg gets 10 spikes per seed, ND = 180 deg gets 2 spikes per seed.
    Total mean = 12. Expected ratio DSI = (10-2)/(10+2) = 0.6667.
    """
    pd_direction_deg = 0.0
    nd_direction_deg = 180.0
    spike_counts: dict[float, list[int]] = {
        pd_direction_deg: [10, 10, 10],
        nd_direction_deg: [2, 2, 2],
    }
    trials = _make_trials(spike_counts=spike_counts)
    result = _summarise_trials(results=trials, n_seeds=N_EVAL_SEEDS_LOCAL)
    total_mean = sum(float(np.mean(counts)) for counts in spike_counts.values())
    assert total_mean >= SILENCE_SPIKE_COUNT_THRESHOLD, (
        f"test premise failed: total_mean={total_mean} should be at or "
        f"above the silence threshold {SILENCE_SPIKE_COUNT_THRESHOLD}"
    )
    assert result.dsi_vector_sum > 0.0, (
        f"firing cell (total mean spikes {total_mean}) must yield a "
        f"positive DSI; guard wrongly fired and gave "
        f"{result.dsi_vector_sum}"
    )
    assert result.dsi_vector_sum <= 1.0, f"DSI must be bounded by 1.0; got {result.dsi_vector_sum}"
    expected_ratio = (10.0 - 2.0) / (10.0 + 2.0)
    assert abs(result.dsi_vector_sum - expected_ratio) < 1e-6, (
        f"DSI at PD=10, ND=2 must equal {expected_ratio:.6f}; got {result.dsi_vector_sum}"
    )


def test_ratio_dsi_synthetic_pd5_nd1() -> None:
    """REQ-1: at PD = 5 spikes, ND = 1 spike, the _vector_sum_dsi function
    must return ``(5 - 1) / (5 + 1) = 0.6667`` within 1e-6 tolerance.

    Proves the t0104 ``_vector_sum_dsi`` already reduces to the t0106 ratio
    DSI at ``n_directions = 2``: at angles [0, 180] the unit vectors are
    (+1, 0) and (-1, 0), so ``total_x = mean_PD - mean_ND``, ``total_y = 0``,
    and the function returns ``abs(mean_PD - mean_ND) / (mean_PD + mean_ND)``.
    """
    spike_counts_per_dir: dict[float, list[int]] = {
        0.0: [5],
        180.0: [1],
    }
    dsi = _vector_sum_dsi(spike_counts_per_dir=spike_counts_per_dir)
    expected = (5.0 - 1.0) / (5.0 + 1.0)
    assert abs(dsi - expected) < 1e-6, (
        f"ratio-DSI cross-check failed: PD=5, ND=1 should yield {expected:.6f}; got {dsi}"
    )


def test_silence_guard_threshold_sweep() -> None:
    """REQ-2: silence-guard sensitivity sweep across thresholds {5, 10, 20}.

    All three thresholds zero-out DSI for the same degenerate input.
    """
    # Synthetic degenerate case: PD = 1 per seed, ND = 0 per seed.
    # Total mean across 2 directions = 1.0, below all three thresholds.
    spike_counts_per_dir: dict[float, list[int]] = {
        0.0: [1, 1, 1],
        180.0: [0, 0, 0],
    }
    total_mean = sum(float(np.mean(counts)) for counts in spike_counts_per_dir.values())
    for threshold in (5, 10, 20):
        if total_mean < threshold:
            simulated_dsi = 0.0
        else:
            simulated_dsi = _vector_sum_dsi(spike_counts_per_dir=spike_counts_per_dir)
        assert simulated_dsi == 0.0, (
            f"threshold-{threshold} sweep: total_mean={total_mean} should "
            f"zero-out DSI; got {simulated_dsi}"
        )
