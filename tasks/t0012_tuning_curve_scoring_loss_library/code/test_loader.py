"""Tests for ``tuning_curve_loss.loader``."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader import (
    load_tuning_curve,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.paths import (
    ANGLE_COLUMN,
    FIRING_RATE_COLUMN,
    N_ANGLES,
    TARGET_MEAN_CSV,
    TARGET_TRIALS_CSV,
    TRIAL_SEED_COLUMN,
)


def test_load_target_curve_from_t0004() -> None:
    curve = load_tuning_curve(csv_path=TARGET_MEAN_CSV)
    assert curve.angles_deg.shape == (N_ANGLES,), "12 angles"
    assert curve.firing_rates_hz.shape == (N_ANGLES,), "12 firing rates"
    # Peak at 90 deg = 32 Hz; null at 270 deg = 2 Hz.
    assert float(curve.firing_rates_hz[3]) == pytest.approx(32.0), "peak at 90 deg"
    assert float(curve.firing_rates_hz[9]) == pytest.approx(2.0), "null at 270 deg"
    # Trials sibling auto-loaded.
    assert curve.trials is not None, "t0004 sibling curve_trials.csv populates trials"
    assert curve.trials.shape == (N_ANGLES, 20), "20 trials per angle"


def test_load_with_trials_csv_from_t0004() -> None:
    curve = load_tuning_curve(csv_path=TARGET_TRIALS_CSV)
    assert curve.trials is not None, "trials CSV yields a per-trial matrix"
    assert curve.trials.shape == (N_ANGLES, 20), "shape is (n_angles, n_trials)"
    # Mean over trials matches the analytic curve to well under 1 Hz (noise_sd_hz=3, n_trials=20).
    np.testing.assert_allclose(
        curve.firing_rates_hz,
        curve.trials.mean(axis=1),
        rtol=0.0,
        atol=1e-9,
    )


def test_load_canonical_trials_schema(tmp_path: Path) -> None:
    # Build a tiny 2-trial-per-angle synthetic CSV with the canonical schema.
    angles: np.ndarray = np.linspace(start=0.0, stop=360.0, num=N_ANGLES, endpoint=False)
    seeds: list[int] = [101, 102]
    rows: list[dict[str, float | int]] = []
    for angle in angles:
        for seed in seeds:
            rows.append(
                {
                    ANGLE_COLUMN: float(angle),
                    TRIAL_SEED_COLUMN: seed,
                    FIRING_RATE_COLUMN: 5.0 + 0.1 * seed + float(angle) * 0.01,
                }
            )
    df: pd.DataFrame = pd.DataFrame(data=rows)
    csv_path: Path = tmp_path / "canonical.csv"
    df.to_csv(path_or_buf=csv_path, index=False)
    curve = load_tuning_curve(csv_path=csv_path)
    assert curve.trials is not None, "canonical schema populates trials"
    assert curve.trials.shape == (N_ANGLES, 2), "2 trials per angle"


def test_load_missing_file_raises(tmp_path: Path) -> None:
    missing: Path = tmp_path / "does_not_exist.csv"
    with pytest.raises(FileNotFoundError):
        load_tuning_curve(csv_path=missing)


def test_load_malformed_csv_raises(tmp_path: Path) -> None:
    bad_path: Path = tmp_path / "bad.csv"
    bad_path.write_text(data="foo,bar\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_tuning_curve(csv_path=bad_path)


def test_load_non_uniform_grid_raises(tmp_path: Path) -> None:
    # 12 angles but not a 30 deg grid.
    bad_angles: list[float] = [
        0.0,
        10.0,
        20.0,
        40.0,
        80.0,
        160.0,
        180.0,
        190.0,
        200.0,
        220.0,
        260.0,
        340.0,
    ]
    rows: list[dict[str, float]] = [{ANGLE_COLUMN: a, "mean_rate_hz": 1.0} for a in bad_angles]
    df: pd.DataFrame = pd.DataFrame(data=rows)
    csv_path: Path = tmp_path / "non_uniform.csv"
    df.to_csv(path_or_buf=csv_path, index=False)
    with pytest.raises(ValueError):
        load_tuning_curve(csv_path=csv_path)
