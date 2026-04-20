"""Cartesian firing-rate vs angle plot with optional bootstrap CI band."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants import (
    CI_BAND_ALPHA,
    DEFAULT_BBOX_INCHES,
    DEFAULT_DPI,
    DEFAULT_FACECOLOR,
    MODEL_COLORS,
    TARGET_COLOR,
    TARGET_LINESTYLE,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.loaders import (
    TuningCurve,
    load_curve,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.stats import (
    bootstrap_ci,
)


def plot_cartesian_tuning_curve(
    curve_csv: Path,
    out_png: Path,
    *,
    show_trials: bool = True,
    target_csv: Path | None = None,
) -> None:
    """Plot firing rate vs direction in Cartesian coordinates.

    Draws per-trial scatter points (when available), the per-angle mean line, and a
    95 percent bootstrap CI band (when per-trial data is available). If ``target_csv`` is
    supplied, the target mean is overlaid as a dashed black line.

    Parameters
    ----------
    curve_csv:
        CSV of the candidate tuning curve; any of the three supported schemas.
    out_png:
        Destination PNG path; parent directory must exist.
    show_trials:
        When True and per-trial data is available, draws the per-trial scatter points.
    target_csv:
        Optional path to the target curve CSV. When supplied, overlaid as a dashed
        black line labelled "target".
    """
    curve: TuningCurve = load_curve(csv_path=curve_csv)
    angles_deg: np.ndarray = curve.angles_deg
    mean_hz: np.ndarray = curve.firing_rates_hz

    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    # Model curve colour (first non-black Okabe-Ito entry).
    model_color: str = MODEL_COLORS[0]

    # Per-trial scatter + bootstrap CI band if trials are present.
    if curve.trials is not None and show_trials:
        n_angles: int = curve.trials.shape[0]
        n_trials: int = curve.trials.shape[1]
        for trial_idx in range(n_trials):
            ax.scatter(
                angles_deg,
                curve.trials[:, trial_idx],
                s=12,
                color=model_color,
                alpha=0.25,
                edgecolors="none",
                label="trials" if trial_idx == 0 else None,
            )
        assert n_angles == angles_deg.shape[0], "trials row count == angle count"
        ci = bootstrap_ci(per_angle_trials=curve.trials)
        ax.fill_between(
            angles_deg,
            ci.ci_low_hz,
            ci.ci_high_hz,
            color=model_color,
            alpha=CI_BAND_ALPHA,
            label="95% CI",
        )

    ax.plot(
        angles_deg,
        mean_hz,
        color=model_color,
        linewidth=2.0,
        marker="o",
        label="mean",
    )

    if target_csv is not None:
        target_curve: TuningCurve = load_curve(csv_path=target_csv)
        ax.plot(
            target_curve.angles_deg,
            target_curve.firing_rates_hz,
            color=TARGET_COLOR,
            linestyle=TARGET_LINESTYLE,
            linewidth=1.5,
            label="target",
        )

    ax.set_xlabel("Direction (deg)")
    ax.set_ylabel("Firing rate (Hz)")
    ax.set_title("Cartesian tuning curve")
    ax.set_xlim(left=float(angles_deg.min()) - 5.0, right=float(angles_deg.max()) + 5.0)
    ax.grid(visible=True, alpha=0.3)
    ax.legend(loc="best", frameon=True)

    fig.tight_layout()
    fig.savefig(
        fname=out_png,
        dpi=DEFAULT_DPI,
        facecolor=DEFAULT_FACECOLOR,
        bbox_inches=DEFAULT_BBOX_INCHES,
    )
    plt.close(fig=fig)
