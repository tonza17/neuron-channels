"""Smoke test: run every plot type on real project data and save the PNGs.

This module is intentionally not picked up by ``pytest`` (the filename matches the
``test_*.py`` convention but every public callable starts with an underscore or the
function :func:`run_all`; there are no ``def test_*`` functions). Invoke with::

    uv run python -u -m tasks.t0011_response_visualization_library\\
        .code.tuning_curve_viz.test_smoke

Outputs 7 PNGs into ``assets/library/tuning_curve_viz/files/``:

1. ``target_cartesian.png`` — t0004 target curve (mean + trials).
2. ``target_polar.png`` — t0004 target curve in polar form.
3. ``t0008_cartesian.png`` — t0008 simulated curve in Cartesian form with target overlay.
4. ``t0008_polar.png`` — t0008 simulated curve in polar form with target overlay.
5. ``overlay_target_vs_t0008.png`` — two-model overlay with target dashed overlay.
6. ``raster_psth_0deg.png`` — synthetic Poisson raster+PSTH at 0 deg.
7. ``raster_psth_90deg.png`` — synthetic Poisson raster+PSTH at 90 deg.

The raster+PSTH plots use a deterministic :class:`numpy.random.Generator` fixture
(seed = :data:`SMOKE_RNG_SEED`). No spike-time CSV ships with the library asset.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

from tasks.t0011_response_visualization_library.code.tuning_curve_viz.cartesian import (
    plot_cartesian_tuning_curve,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants import (
    SMOKE_RNG_SEED,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.overlay import (
    plot_multi_model_overlay,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.paths import (
    LIBRARY_ASSET_FILES_DIR,
    SMOKE_OVERLAY_PNG,
    SMOKE_RASTER_PSTH_0_PNG,
    SMOKE_RASTER_PSTH_PREF_PNG,
    SMOKE_T0008_CARTESIAN_PNG,
    SMOKE_T0008_POLAR_PNG,
    SMOKE_TARGET_CARTESIAN_PNG,
    SMOKE_TARGET_POLAR_PNG,
    T0004_TARGET_MEAN_CSV,
    T0008_SIMULATED_CURVE_CSV,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.polar import (
    plot_polar_tuning_curve,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.raster_psth import (
    ANGLE_DEG_COLUMN,
    SPIKE_TIME_COLUMN,
    TRIAL_INDEX_COLUMN,
    plot_angle_raster_psth,
)

# Synthetic raster fixture parameters.
_N_TRIALS_PER_ANGLE: int = 8
_TRIAL_DURATION_S: float = 1.0
_BASELINE_RATE_HZ: float = 5.0
_PEAK_RATE_HZ: float = 40.0
_PREFERRED_DIR_DEG: float = 90.0
_TUNING_HALF_WIDTH_DEG: float = 45.0


def _synthesize_poisson_spikes(
    *,
    angles_deg: np.ndarray,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate a per-trial Poisson spike-time DataFrame with cos-tuned rates.

    The rate at each angle follows a raised-cosine tuning around
    :data:`_PREFERRED_DIR_DEG` with half-width :data:`_TUNING_HALF_WIDTH_DEG` so the
    0-deg raster looks clearly sparser than the 90-deg raster.
    """
    rows: list[dict[str, float | int]] = []
    for angle_deg in angles_deg:
        angle_offset_rad: float = float(
            np.deg2rad((angle_deg - _PREFERRED_DIR_DEG + 180.0) % 360.0 - 180.0)
        )
        tuning_factor: float = float(np.clip(a=np.cos(angle_offset_rad), a_min=0.0, a_max=1.0))
        rate_hz: float = _BASELINE_RATE_HZ + (_PEAK_RATE_HZ - _BASELINE_RATE_HZ) * tuning_factor
        for trial_index in range(_N_TRIALS_PER_ANGLE):
            expected_count: float = rate_hz * _TRIAL_DURATION_S
            n_spikes: int = int(rng.poisson(lam=expected_count))
            if n_spikes == 0:
                continue
            spike_times: np.ndarray = np.sort(
                rng.uniform(low=0.0, high=_TRIAL_DURATION_S, size=n_spikes)
            )
            for spike_time in spike_times:
                rows.append(
                    {
                        ANGLE_DEG_COLUMN: float(angle_deg),
                        TRIAL_INDEX_COLUMN: int(trial_index),
                        SPIKE_TIME_COLUMN: float(spike_time),
                    }
                )
    return pd.DataFrame(data=rows)


def run_all() -> None:
    """Run every smoke-test plot and write outputs into the library asset folder."""
    LIBRARY_ASSET_FILES_DIR.mkdir(parents=True, exist_ok=True)

    target_mean_csv: Path = T0004_TARGET_MEAN_CSV
    t0008_csv: Path = T0008_SIMULATED_CURVE_CSV

    if not target_mean_csv.exists():
        raise FileNotFoundError(f"Expected t0004 target CSV at {target_mean_csv}")
    if not t0008_csv.exists():
        raise FileNotFoundError(f"Expected t0008 simulated CSV at {t0008_csv}")

    # 1-2. t0004 target curve: Cartesian (with trials + CI) and polar.
    plot_cartesian_tuning_curve(
        curve_csv=target_mean_csv,
        out_png=SMOKE_TARGET_CARTESIAN_PNG,
        show_trials=True,
        target_csv=None,
    )
    plot_polar_tuning_curve(
        curve_csv=target_mean_csv,
        out_png=SMOKE_TARGET_POLAR_PNG,
        target_csv=None,
    )

    # 3-4. t0008 simulated curve with target overlay: Cartesian and polar.
    plot_cartesian_tuning_curve(
        curve_csv=t0008_csv,
        out_png=SMOKE_T0008_CARTESIAN_PNG,
        show_trials=True,
        target_csv=target_mean_csv,
    )
    plot_polar_tuning_curve(
        curve_csv=t0008_csv,
        out_png=SMOKE_T0008_POLAR_PNG,
        target_csv=target_mean_csv,
    )

    # 5. Two-model overlay with target dashed overlay.
    plot_multi_model_overlay(
        curves_dict={
            "t0004_target_mean": target_mean_csv,
            "t0008_simulated": t0008_csv,
        },
        out_png=SMOKE_OVERLAY_PNG,
        target_csv=target_mean_csv,
    )

    # 6-7. Raster+PSTH on a synthetic deterministic Poisson fixture at 0 deg and 90 deg.
    rng: np.random.Generator = np.random.default_rng(seed=SMOKE_RNG_SEED)
    angles_deg: np.ndarray = np.arange(0.0, 360.0, 45.0, dtype=np.float64)
    spike_df: pd.DataFrame = _synthesize_poisson_spikes(angles_deg=angles_deg, rng=rng)
    # Write to a temporary CSV so we go through the real CSV path rather than an
    # in-memory fixture; deleted after the plot is rendered.
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
        encoding="utf-8",
        newline="",
    ) as fh:
        tmp_spike_csv: Path = Path(fh.name)
    try:
        spike_df.to_csv(path_or_buf=tmp_spike_csv, index=False)
        plot_angle_raster_psth(
            spike_times_csv=tmp_spike_csv,
            out_png=SMOKE_RASTER_PSTH_0_PNG,
            angle_deg=0.0,
        )
        plot_angle_raster_psth(
            spike_times_csv=tmp_spike_csv,
            out_png=SMOKE_RASTER_PSTH_PREF_PNG,
            angle_deg=90.0,
        )
    finally:
        if tmp_spike_csv.exists():
            tmp_spike_csv.unlink()


def main() -> int:
    run_all()
    expected_outputs: list[Path] = [
        SMOKE_TARGET_CARTESIAN_PNG,
        SMOKE_TARGET_POLAR_PNG,
        SMOKE_T0008_CARTESIAN_PNG,
        SMOKE_T0008_POLAR_PNG,
        SMOKE_OVERLAY_PNG,
        SMOKE_RASTER_PSTH_0_PNG,
        SMOKE_RASTER_PSTH_PREF_PNG,
    ]
    missing: list[Path] = [p for p in expected_outputs if not p.exists()]
    if len(missing) > 0:
        for m in missing:
            sys.stderr.write(f"MISSING: {m}\n")
        return 1
    for p in expected_outputs:
        sys.stdout.write(f"OK: {p}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
