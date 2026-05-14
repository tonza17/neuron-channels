"""Unit tests for the t0104 DSI silence guard (REQ-7).

Tests assert the new guard in `_summarise_trials` returns
``dsi_vector_sum = 0.0`` whenever the cell's total mean spike count across
the 16 directions is below ``SILENCE_SPIKE_COUNT_THRESHOLD`` (= 10). This
eliminates the t0102 silence-corner artifact (27 cells at a spurious DSI =
1.0 caused by ``_vector_sum_dsi`` dividing by near-zero ``total_spikes_f``).

Three cases:
* test_all_silent_returns_dsi_zero — 16 dirs x 4 seeds at spike_count=0.
* test_near_silent_returns_dsi_zero — total mean spikes ~ 1.25, guard floor.
* test_firing_positive_control_returns_nonzero — total mean spikes >> 10,
  guard does NOT trigger and DSI is computed normally.
"""

from __future__ import annotations

import numpy as np

from tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.evaluator import (
    SILENCE_SPIKE_COUNT_THRESHOLD,
    TrialResult,
    _summarise_trials,
)

N_EVAL_SEEDS_LOCAL: int = 4
N_DIRECTIONS_LOCAL: int = 16
DIRECTIONS_DEG: tuple[float, ...] = tuple(
    float(i) * 360.0 / N_DIRECTIONS_LOCAL for i in range(N_DIRECTIONS_LOCAL)
)
SANE_PEAK_MV: float = -50.0  # inside [STABILITY_PEAK_VM_MIN_MV,
# STABILITY_PEAK_VM_MAX_MV] so is_unstable stays False.


def _make_trials(*, spike_counts: dict[float, list[int]]) -> list[TrialResult]:
    """Build N_EVAL_SEEDS x N_DIRECTIONS TrialResults from a {dir_deg:
    [count_per_seed]} dict.

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
    """All 16 dirs x 4 seeds with spike_count=0 must return DSI=0.0.

    Without the guard, _vector_sum_dsi short-circuits at total_spikes_f <=
    1e-12 and returns 0.0 by coincidence — this test pins the explicit
    silence guard behaviour, which fires before the 1e-12 fallback.
    """
    spike_counts: dict[float, list[int]] = {d: [0] * N_EVAL_SEEDS_LOCAL for d in DIRECTIONS_DEG}
    trials = _make_trials(spike_counts=spike_counts)
    result = _summarise_trials(results=trials, n_seeds=N_EVAL_SEEDS_LOCAL)
    assert result.dsi_vector_sum == 0.0, (
        f"all-silent cell must yield DSI=0.0 (guard threshold "
        f"{SILENCE_SPIKE_COUNT_THRESHOLD}), got {result.dsi_vector_sum}"
    )


def test_near_silent_returns_dsi_zero() -> None:
    """Near-silent cell (total mean spikes ~ 1.25) must trip the guard.

    Builds one direction with 5 PD spikes spread asymmetrically across the
    4 seeds (i.e., [5, 0, 0, 0] -> mean=1.25) and zero spikes everywhere
    else. Total mean across the 16 directions = 1.25, well below the
    SILENCE_SPIKE_COUNT_THRESHOLD = 10 floor.

    Without the guard, _vector_sum_dsi would return 1.0 because all spikes
    fall on a single direction — exactly the t0102 silence-corner artifact.
    """
    pd_direction_deg = 0.0
    spike_counts: dict[float, list[int]] = {d: [0] * N_EVAL_SEEDS_LOCAL for d in DIRECTIONS_DEG}
    spike_counts[pd_direction_deg] = [5, 0, 0, 0]
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

    Builds an asymmetric PD-biased spike distribution: PD direction (0
    deg) has 8 spikes per seed (mean=8 across 4 seeds), and 4 of the 15
    other directions have 2 spikes per seed each (mean=2), for a total
    mean of 8 + 4*2 = 16 spikes across the 16 directions — above the
    silence threshold of 10. The guard does NOT trigger and
    _vector_sum_dsi returns a finite positive DSI in (0, 1].
    """
    pd_direction_deg = 0.0
    spike_counts: dict[float, list[int]] = {d: [0] * N_EVAL_SEEDS_LOCAL for d in DIRECTIONS_DEG}
    spike_counts[pd_direction_deg] = [8, 8, 8, 8]
    for d in DIRECTIONS_DEG[1:5]:
        spike_counts[d] = [2, 2, 2, 2]
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
    assert result.dsi_vector_sum <= 1.0, (
        f"vector-sum DSI must be bounded by 1.0; got {result.dsi_vector_sum}"
    )
