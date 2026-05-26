"""Unit tests for the t0122 DSI silence guard and 2-direction ratio DSI.

t0122-specific tests:

* ``test_all_silent_returns_dsi_zero`` -- 2 dirs x 3 seeds at
  spike_count=0; guard floor at ``pd_spikes_sum < 3``.
* ``test_one_pd_spike_returns_dsi_zero`` -- pd_spikes_sum=1 < 3 trips
  the new t0122 guard.
* ``test_two_pd_spikes_returns_dsi_zero`` -- pd_spikes_sum=2 < 3 trips
  the new t0122 guard.
* ``test_three_pd_spikes_does_not_trip_guard`` -- pd_spikes_sum=3 is at
  the threshold; the guard does NOT trip and DSI is computed normally.
* ``test_firing_positive_control_returns_nonzero`` -- pd_spikes_sum >> 3,
  guard does NOT trigger and DSI is computed normally. Expected ratio
  DSI at PD=10, ND=2: (10-2)/(10+2) = 0.6667.
* ``test_ratio_dsi_synthetic_pd5_nd1`` -- at PD = 5, ND = 1, the
  ``_vector_sum_dsi`` function returns 0.6667 within 1e-6 tolerance.
* ``test_silence_pd_threshold_value`` -- regression guard:
  ``SILENCE_PD_SPIKES_THRESHOLD == 3``.
"""

from __future__ import annotations

from tasks.t0128_t0127_rerun_dsi_atp_3seeds.code.evaluator import (
    SILENCE_PD_SPIKES_THRESHOLD,
    TrialResult,
    _summarise_trials,
    _vector_sum_dsi,
)

N_EVAL_SEEDS_LOCAL: int = 3
N_DIRECTIONS_LOCAL: int = 2
DIRECTIONS_DEG: tuple[float, ...] = tuple(
    float(i) * 360.0 / N_DIRECTIONS_LOCAL for i in range(N_DIRECTIONS_LOCAL)
)
SANE_PEAK_MV: float = -50.0  # inside the stability envelope.


def _make_trials(*, spike_counts: dict[float, list[int]]) -> list[TrialResult]:
    """Build N_EVAL_SEEDS x N_DIRECTIONS TrialResults from a dict."""
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


def test_silence_pd_threshold_value() -> None:
    """Regression guard: t0122's tightened silence threshold == 3."""
    assert SILENCE_PD_SPIKES_THRESHOLD == 3, (
        f"t0122 silence threshold must be 3 PD spikes; got {SILENCE_PD_SPIKES_THRESHOLD}"
    )


def test_all_silent_returns_dsi_zero() -> None:
    """All 2 dirs x 3 seeds with spike_count=0 must return DSI=0.0."""
    spike_counts: dict[float, list[int]] = {d: [0] * N_EVAL_SEEDS_LOCAL for d in DIRECTIONS_DEG}
    trials = _make_trials(spike_counts=spike_counts)
    result = _summarise_trials(
        results=trials,
        n_seeds=N_EVAL_SEEDS_LOCAL,
        n_directions=N_DIRECTIONS_LOCAL,
    )
    assert result.dsi_vector_sum == -1.0, (
        f"all-silent cell must yield DSI=-1.0 (guard threshold "
        f"{SILENCE_PD_SPIKES_THRESHOLD} PD spikes; t0128 sentinel), "
        f"got {result.dsi_vector_sum}"
    )
    assert result.silence_failed is True
    assert result.mi_count_bits == 0.0


def test_one_pd_spike_returns_dsi_zero() -> None:
    """pd_spikes_sum=1 must trip the new t0122 guard (< 3)."""
    pd_direction_deg = 0.0
    spike_counts: dict[float, list[int]] = {d: [0] * N_EVAL_SEEDS_LOCAL for d in DIRECTIONS_DEG}
    spike_counts[pd_direction_deg] = [1, 0, 0]
    trials = _make_trials(spike_counts=spike_counts)
    result = _summarise_trials(
        results=trials,
        n_seeds=N_EVAL_SEEDS_LOCAL,
        n_directions=N_DIRECTIONS_LOCAL,
    )
    assert result.dsi_vector_sum == -1.0, (
        f"pd_spikes_sum=1 < {SILENCE_PD_SPIKES_THRESHOLD} must yield DSI=-1.0 "
        f"(t0128 sentinel); got {result.dsi_vector_sum}"
    )


def test_two_pd_spikes_returns_dsi_zero() -> None:
    """pd_spikes_sum=2 must trip the new t0122 guard (< 3)."""
    pd_direction_deg = 0.0
    spike_counts: dict[float, list[int]] = {d: [0] * N_EVAL_SEEDS_LOCAL for d in DIRECTIONS_DEG}
    spike_counts[pd_direction_deg] = [2, 0, 0]
    trials = _make_trials(spike_counts=spike_counts)
    result = _summarise_trials(
        results=trials,
        n_seeds=N_EVAL_SEEDS_LOCAL,
        n_directions=N_DIRECTIONS_LOCAL,
    )
    assert result.dsi_vector_sum == -1.0, (
        f"pd_spikes_sum=2 < {SILENCE_PD_SPIKES_THRESHOLD} must yield DSI=-1.0 "
        f"(t0128 sentinel); got {result.dsi_vector_sum}"
    )


def test_three_pd_spikes_does_not_trip_guard() -> None:
    """pd_spikes_sum=3 is at the threshold; guard does NOT trip."""
    pd_direction_deg = 0.0
    nd_direction_deg = 180.0
    spike_counts: dict[float, list[int]] = {
        pd_direction_deg: [3, 0, 0],
        nd_direction_deg: [0, 0, 0],
    }
    trials = _make_trials(spike_counts=spike_counts)
    result = _summarise_trials(
        results=trials,
        n_seeds=N_EVAL_SEEDS_LOCAL,
        n_directions=N_DIRECTIONS_LOCAL,
    )
    # PD mean spikes = 1.0, ND mean spikes = 0.0 -> DSI = (1-0)/(1+0) = 1.0
    # via the vector-sum reduction. The guard does NOT trip because
    # pd_spikes_sum=3 is at the threshold.
    assert result.dsi_vector_sum > 0.0, (
        f"pd_spikes_sum=3 at threshold must NOT trip guard; got DSI={result.dsi_vector_sum}"
    )


def test_firing_positive_control_returns_nonzero() -> None:
    """Firing cell with pd_spikes_sum=30 >> 3 must NOT trip the guard.

    PD = 0 deg gets 10 spikes per seed, ND = 180 deg gets 2 spikes per seed.
    pd_spikes_sum = 30. Expected ratio DSI = (10-2)/(10+2) = 0.6667.
    """
    pd_direction_deg = 0.0
    nd_direction_deg = 180.0
    spike_counts: dict[float, list[int]] = {
        pd_direction_deg: [10, 10, 10],
        nd_direction_deg: [2, 2, 2],
    }
    trials = _make_trials(spike_counts=spike_counts)
    result = _summarise_trials(
        results=trials,
        n_seeds=N_EVAL_SEEDS_LOCAL,
        n_directions=N_DIRECTIONS_LOCAL,
    )
    pd_sum: int = sum(spike_counts[pd_direction_deg])
    assert pd_sum >= SILENCE_PD_SPIKES_THRESHOLD, (
        f"test premise failed: pd_spikes_sum={pd_sum} should be at or "
        f"above the silence threshold {SILENCE_PD_SPIKES_THRESHOLD}"
    )
    assert result.dsi_vector_sum > 0.0, (
        f"firing cell (pd_spikes_sum={pd_sum}) must yield a positive DSI; "
        f"guard wrongly fired and gave {result.dsi_vector_sum}"
    )
    assert result.dsi_vector_sum <= 1.0, f"DSI must be bounded by 1.0; got {result.dsi_vector_sum}"
    expected_ratio = (10.0 - 2.0) / (10.0 + 2.0)
    assert abs(result.dsi_vector_sum - expected_ratio) < 1e-6, (
        f"DSI at PD=10, ND=2 must equal {expected_ratio:.6f}; got {result.dsi_vector_sum}"
    )


def test_ratio_dsi_synthetic_pd5_nd1() -> None:
    """At PD = 5 spikes, ND = 1 spike, ``_vector_sum_dsi`` returns 0.6667."""
    spike_counts_per_dir: dict[float, list[int]] = {
        0.0: [5],
        180.0: [1],
    }
    dsi = _vector_sum_dsi(spike_counts_per_dir=spike_counts_per_dir)
    expected = (5.0 - 1.0) / (5.0 + 1.0)
    assert abs(dsi - expected) < 1e-6, (
        f"ratio-DSI cross-check failed: PD=5, ND=1 should yield {expected:.6f}; got {dsi}"
    )
