"""CSV -> TuningCurve loader.

Accepts three schemas:
1. Canonical trials schema ``(angle_deg, trial_seed, firing_rate_hz)`` — many rows per angle.
2. Legacy trials schema ``(angle_deg, trial_index, rate_hz)`` produced by t0004 curve_trials.csv.
3. Two-column mean schema ``(angle_deg, mean_rate_hz)`` produced by t0004 curve_mean.csv.

In the two trials schemas the loader folds trials into per-angle means and populates the
``trials`` field with a ``(n_angles, n_trials)`` matrix. In the mean schema the ``trials`` field
is ``None``. Angles are sorted ascending; any 12-row grid with 30 deg spacing is accepted but the
loader does not require an exact start at 0 deg (only uniform spacing and ``N_ANGLES`` points).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.paths import (
    ANGLE_COLUMN,
    ANGLE_STEP_DEG,
    FIRING_RATE_COLUMN,
    MEAN_RATE_COLUMN,
    N_ANGLES,
    TRIAL_INDEX_COLUMN,
    TRIAL_RATE_COLUMN,
    TRIAL_SEED_COLUMN,
)


@dataclass(frozen=True, slots=True)
class TuningCurve:
    """Sorted 12-angle tuning curve plus optional per-trial firing rates."""

    angles_deg: np.ndarray
    firing_rates_hz: np.ndarray
    trials: np.ndarray | None


def _detect_schema(*, columns: list[str]) -> str:
    col_set: frozenset[str] = frozenset(columns)
    if {ANGLE_COLUMN, TRIAL_SEED_COLUMN, FIRING_RATE_COLUMN}.issubset(col_set):
        return "canonical_trials"
    if {ANGLE_COLUMN, TRIAL_INDEX_COLUMN, TRIAL_RATE_COLUMN}.issubset(col_set):
        return "t0004_trials"
    if {ANGLE_COLUMN, MEAN_RATE_COLUMN}.issubset(col_set):
        return "t0004_mean"
    raise ValueError(
        f"Unrecognised CSV schema. Got columns {columns!r}; expected one of the supported "
        "schemas: canonical (angle_deg, trial_seed, firing_rate_hz), t0004 trials "
        "(angle_deg, trial_index, rate_hz), or t0004 mean (angle_deg, mean_rate_hz)."
    )


def _validate_angle_grid(*, angles_deg: np.ndarray) -> None:
    assert angles_deg.ndim == 1, "angles_deg is 1-D"
    if len(angles_deg) != N_ANGLES:
        raise ValueError(
            f"Expected {N_ANGLES} unique angles; got {len(angles_deg)}. "
            f"Angles: {angles_deg.tolist()!r}"
        )
    diffs: np.ndarray = np.diff(angles_deg)
    if not np.allclose(diffs, ANGLE_STEP_DEG, atol=1e-6):
        raise ValueError(
            f"Expected uniform {ANGLE_STEP_DEG} deg grid; diffs are {diffs.tolist()!r}"
        )


def _load_from_trials(
    *,
    df: pd.DataFrame,
    rate_column: str,
) -> TuningCurve:
    grouped: pd.DataFrame = (
        df.groupby(by=ANGLE_COLUMN, sort=True)[rate_column].apply(list).reset_index()
    )
    angles_deg: np.ndarray = grouped[ANGLE_COLUMN].to_numpy(dtype=np.float64)
    _validate_angle_grid(angles_deg=angles_deg)

    # Build a (n_angles, n_trials) matrix; require same trial count per angle.
    trial_counts: set[int] = {len(lst) for lst in grouped[rate_column].tolist()}
    if len(trial_counts) != 1:
        raise ValueError(
            f"Inconsistent trial count per angle: {trial_counts!r}. "
            "All angles must share the same number of trials."
        )
    trials: np.ndarray = np.array(
        [np.asarray(a=row, dtype=np.float64) for row in grouped[rate_column].tolist()],
        dtype=np.float64,
    )
    firing_rates_hz: np.ndarray = trials.mean(axis=1)
    return TuningCurve(
        angles_deg=angles_deg,
        firing_rates_hz=firing_rates_hz,
        trials=trials,
    )


def _load_from_mean(*, df: pd.DataFrame) -> TuningCurve:
    df_sorted: pd.DataFrame = df.sort_values(by=ANGLE_COLUMN).reset_index(drop=True)
    angles_deg: np.ndarray = df_sorted[ANGLE_COLUMN].to_numpy(dtype=np.float64)
    _validate_angle_grid(angles_deg=angles_deg)
    firing_rates_hz: np.ndarray = df_sorted[MEAN_RATE_COLUMN].to_numpy(dtype=np.float64)
    return TuningCurve(
        angles_deg=angles_deg,
        firing_rates_hz=firing_rates_hz,
        trials=None,
    )


def load_tuning_curve(*, csv_path: Path) -> TuningCurve:
    """Load a tuning curve from a CSV file.

    Detects the schema from the column headers and dispatches to the right loader. Raises
    ``FileNotFoundError`` if the file is missing, ``ValueError`` if the schema is unrecognised
    or the angle grid is invalid.

    If ``csv_path`` points at a mean-only CSV but a sibling ``curve_trials.csv`` exists next to
    it, the loader also reads the sibling trials CSV to populate the ``trials`` field.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Tuning-curve CSV not found: {csv_path}")

    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=csv_path)
    schema: str = _detect_schema(columns=df.columns.tolist())

    if schema == "canonical_trials":
        return _load_from_trials(df=df, rate_column=FIRING_RATE_COLUMN)
    if schema == "t0004_trials":
        return _load_from_trials(df=df, rate_column=TRIAL_RATE_COLUMN)

    # t0004_mean: also check for a sibling curve_trials.csv to populate trials.
    mean_curve: TuningCurve = _load_from_mean(df=df)
    sibling_trials: Path = csv_path.parent / "curve_trials.csv"
    if sibling_trials.exists():
        df_trials: pd.DataFrame = pd.read_csv(filepath_or_buffer=sibling_trials)
        trials_schema: str = _detect_schema(columns=df_trials.columns.tolist())
        if trials_schema == "canonical_trials":
            trials_curve: TuningCurve = _load_from_trials(
                df=df_trials,
                rate_column=FIRING_RATE_COLUMN,
            )
        elif trials_schema == "t0004_trials":
            trials_curve = _load_from_trials(
                df=df_trials,
                rate_column=TRIAL_RATE_COLUMN,
            )
        else:
            # Sibling is another mean file; ignore.
            return mean_curve
        # Prefer the (more precise) mean from the supplied CSV, but attach trials.
        return TuningCurve(
            angles_deg=mean_curve.angles_deg,
            firing_rates_hz=mean_curve.firing_rates_hz,
            trials=trials_curve.trials,
        )
    return mean_curve
