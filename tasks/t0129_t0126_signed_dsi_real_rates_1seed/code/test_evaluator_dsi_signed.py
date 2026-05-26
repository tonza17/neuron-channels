"""Unit tests for the t0129 signed antipodal DSI helper and silence guard.

t0129-specific tests:

* ``test_silence_pd_threshold_value`` -- regression guard:
  ``SILENCE_PD_SPIKES_THRESHOLD == 3``.
* ``test_all_silent_returns_dsi_minus_one`` -- 2 dirs x 3 seeds at
  ``spike_count = 0`` returns ``WORST_CASE_DSI = -1.0``.
* ``test_one_pd_spike_returns_dsi_minus_one`` -- ``pd_spikes_sum=1 < 3``
  trips the silence guard, returns -1.0.
* ``test_two_pd_spikes_returns_dsi_minus_one`` -- ``pd_spikes_sum=2 < 3``
  trips the silence guard, returns -1.0.
* ``test_three_pd_spikes_does_not_trip_guard`` -- ``pd_spikes_sum=3``
  at threshold; guard does NOT trip. ``(PD=3, ND=0) -> dsi_signed = 1.0``.
* ``test_firing_positive_control_pd_dominant`` -- PD=10, ND=2 per seed;
  ``dsi_signed = (10-2)/(10+2) = 0.6667``.
* ``test_signed_dsi_synthetic_pd5_nd1_positive`` -- helper direct call:
  ``_signed_antipodal_dsi({0.0: [5], 180.0: [1]}) -> 0.6667 +- 1e-6``.
* ``test_signed_dsi_negative_when_nd_dominates`` -- NEW for t0129:
  ``_signed_antipodal_dsi({0.0: [2], 180.0: [10]}) -> -0.6667 +- 1e-6``.
* ``test_signed_dsi_zero_when_pd_equals_nd`` -- NEW for t0129:
  ``_signed_antipodal_dsi({0.0: [5], 180.0: [5]}) -> 0.0``.
* ``test_signed_dsi_silence_sentinel_when_both_zero`` -- helper direct
  call with zero denominator returns ``WORST_CASE_DSI = -1.0``.
"""

from __future__ import annotations

from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.constants_morphology import (
    WORST_CASE_DSI,
)
from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.evaluator import (
    SILENCE_PD_SPIKES_THRESHOLD,
    TrialResult,
    _signed_antipodal_dsi,
    _summarise_trials,
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
        f"silence threshold must be 3 PD spikes; got {SILENCE_PD_SPIKES_THRESHOLD}"
    )


def test_all_silent_returns_dsi_minus_one() -> None:
    """All 2 dirs x 3 seeds with spike_count=0 must return dsi_signed = -1.0."""
    spike_counts: dict[float, list[int]] = {d: [0] * N_EVAL_SEEDS_LOCAL for d in DIRECTIONS_DEG}
    trials = _make_trials(spike_counts=spike_counts)
    result = _summarise_trials(
        results=trials,
        n_seeds=N_EVAL_SEEDS_LOCAL,
        n_directions=N_DIRECTIONS_LOCAL,
    )
    assert result.dsi_signed == WORST_CASE_DSI, (
        f"all-silent cell must yield dsi_signed=-1.0 (silence sentinel); got {result.dsi_signed}"
    )
    assert result.silence_failed is True
    assert result.mi_count_bits == 0.0


def test_one_pd_spike_returns_dsi_minus_one() -> None:
    """pd_spikes_sum=1 must trip the silence guard (< 3)."""
    pd_direction_deg = 0.0
    spike_counts: dict[float, list[int]] = {d: [0] * N_EVAL_SEEDS_LOCAL for d in DIRECTIONS_DEG}
    spike_counts[pd_direction_deg] = [1, 0, 0]
    trials = _make_trials(spike_counts=spike_counts)
    result = _summarise_trials(
        results=trials,
        n_seeds=N_EVAL_SEEDS_LOCAL,
        n_directions=N_DIRECTIONS_LOCAL,
    )
    assert result.dsi_signed == WORST_CASE_DSI, (
        f"pd_spikes_sum=1 < {SILENCE_PD_SPIKES_THRESHOLD} must yield dsi_signed=-1.0; "
        f"got {result.dsi_signed}"
    )


def test_two_pd_spikes_returns_dsi_minus_one() -> None:
    """pd_spikes_sum=2 must trip the silence guard (< 3)."""
    pd_direction_deg = 0.0
    spike_counts: dict[float, list[int]] = {d: [0] * N_EVAL_SEEDS_LOCAL for d in DIRECTIONS_DEG}
    spike_counts[pd_direction_deg] = [2, 0, 0]
    trials = _make_trials(spike_counts=spike_counts)
    result = _summarise_trials(
        results=trials,
        n_seeds=N_EVAL_SEEDS_LOCAL,
        n_directions=N_DIRECTIONS_LOCAL,
    )
    assert result.dsi_signed == WORST_CASE_DSI, (
        f"pd_spikes_sum=2 < {SILENCE_PD_SPIKES_THRESHOLD} must yield dsi_signed=-1.0; "
        f"got {result.dsi_signed}"
    )


def test_three_pd_spikes_does_not_trip_guard() -> None:
    """pd_spikes_sum=3 is at the threshold; guard does NOT trip.

    (PD=3 across 3 seeds = 1 spike per seed mean; ND=0). Signed antipodal
    DSI = (1-0)/(1+0) = 1.0.
    """
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
    # mean(PD)=1.0, mean(ND)=0.0 -> dsi_signed = (1.0 - 0.0) / (1.0 + 0.0) = 1.0
    expected: float = 1.0
    assert abs(result.dsi_signed - expected) < 1e-9, (
        f"pd_spikes_sum=3 at threshold must NOT trip guard and should yield "
        f"dsi_signed={expected:.4f}; got {result.dsi_signed}"
    )


def test_firing_positive_control_pd_dominant() -> None:
    """PD=10/seed, ND=2/seed: dsi_signed = (10-2)/(10+2) = 0.6667."""
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
    expected_ratio: float = (10.0 - 2.0) / (10.0 + 2.0)
    assert abs(result.dsi_signed - expected_ratio) < 1e-6, (
        f"PD=10, ND=2 must yield dsi_signed={expected_ratio:.6f}; got {result.dsi_signed}"
    )
    assert -1.0 <= result.dsi_signed <= 1.0


def test_signed_dsi_synthetic_pd5_nd1_positive() -> None:
    """Direct helper call: (PD=5, ND=1) -> (5-1)/(5+1) = 0.6667."""
    dsi: float = _signed_antipodal_dsi(
        spike_counts_per_dir={0.0: [5], 180.0: [1]},
    )
    expected: float = (5.0 - 1.0) / (5.0 + 1.0)
    assert abs(dsi - expected) < 1e-6, (
        f"_signed_antipodal_dsi(PD=5, ND=1) should be {expected:.6f}; got {dsi}"
    )


def test_signed_dsi_negative_when_nd_dominates() -> None:
    """NEW for t0129: (PD=2, ND=10) -> (2-10)/(2+10) = -0.6667."""
    dsi: float = _signed_antipodal_dsi(
        spike_counts_per_dir={0.0: [2], 180.0: [10]},
    )
    expected: float = (2.0 - 10.0) / (2.0 + 10.0)
    assert abs(dsi - expected) < 1e-6, (
        f"_signed_antipodal_dsi(PD=2, ND=10) should be {expected:.6f}; got {dsi}"
    )
    assert dsi < 0.0, f"reversed-preference case must yield negative DSI; got {dsi}"


def test_signed_dsi_zero_when_pd_equals_nd() -> None:
    """NEW for t0129: (PD=5, ND=5) -> 0.0 exactly."""
    dsi: float = _signed_antipodal_dsi(
        spike_counts_per_dir={0.0: [5], 180.0: [5]},
    )
    assert abs(dsi - 0.0) < 1e-9, f"_signed_antipodal_dsi(PD=5, ND=5) should be 0.0; got {dsi}"


def test_signed_dsi_silence_sentinel_when_both_zero() -> None:
    """Direct helper call: zero denominator returns WORST_CASE_DSI = -1.0."""
    dsi: float = _signed_antipodal_dsi(
        spike_counts_per_dir={0.0: [0], 180.0: [0]},
    )
    assert dsi == WORST_CASE_DSI, (
        f"_signed_antipodal_dsi with zero denominator must return {WORST_CASE_DSI}; got {dsi}"
    )
