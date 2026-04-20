"""Polar firing-rate vs angle plot with preferred-direction annotation."""

from __future__ import annotations

from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.projections.polar import PolarAxes

from tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants import (
    DEFAULT_BBOX_INCHES,
    DEFAULT_DPI,
    DEFAULT_FACECOLOR,
    MODEL_COLORS,
    PREFERRED_ARROW_COLOR,
    TARGET_COLOR,
    TARGET_LINESTYLE,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.loaders import (
    TuningCurve,
    load_curve,
)


def _compute_preferred_direction_rad(
    *,
    angles_deg: np.ndarray,
    firing_rates_hz: np.ndarray,
) -> tuple[float, float, float]:
    """Return ``(theta_pref_rad, theta_pref_deg, r_peak_hz)`` from the per-angle mean."""
    peak_idx: int = int(np.argmax(a=firing_rates_hz))
    theta_pref_deg: float = float(angles_deg[peak_idx])
    theta_pref_rad: float = float(np.deg2rad(theta_pref_deg))
    r_peak_hz: float = float(firing_rates_hz[peak_idx])
    return theta_pref_rad, theta_pref_deg, r_peak_hz


def _close_polar_curve(
    *,
    angles_rad: np.ndarray,
    values: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Append the first sample at the end so the polar curve closes visually."""
    closed_angles: np.ndarray = np.concatenate([angles_rad, angles_rad[:1]])
    closed_values: np.ndarray = np.concatenate([values, values[:1]])
    return closed_angles, closed_values


def plot_polar_tuning_curve(
    curve_csv: Path,
    out_png: Path,
    *,
    target_csv: Path | None = None,
) -> None:
    """Plot firing rate vs direction in polar coordinates.

    Uses matplotlib polar defaults (``theta_direction=1`` CCW, ``theta_offset=0`` at
    east) and never transforms input angles. The preferred direction is annotated with
    a red arrow from the origin.

    Parameters
    ----------
    curve_csv:
        CSV of the candidate tuning curve.
    out_png:
        Destination PNG path; parent directory must exist.
    target_csv:
        Optional path to the target curve CSV. When supplied, overlaid as a dashed
        black line labelled "target".
    """
    curve: TuningCurve = load_curve(csv_path=curve_csv)
    angles_rad: np.ndarray = np.deg2rad(curve.angles_deg)
    mean_hz: np.ndarray = curve.firing_rates_hz

    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig, ax_raw = plt.subplots(
        figsize=(6.5, 6.5),
        subplot_kw={"projection": "polar"},
    )
    ax: PolarAxes = cast(PolarAxes, ax_raw)
    # Explicit defaults for clarity.
    ax.set_theta_direction(direction=1)
    ax.set_theta_offset(offset=0.0)

    closed_angles, closed_mean = _close_polar_curve(
        angles_rad=angles_rad,
        values=mean_hz,
    )
    ax.plot(
        closed_angles,
        closed_mean,
        color=MODEL_COLORS[0],
        linewidth=2.0,
        marker="o",
        label="mean",
    )

    if target_csv is not None:
        target_curve: TuningCurve = load_curve(csv_path=target_csv)
        target_angles_rad: np.ndarray = np.deg2rad(target_curve.angles_deg)
        closed_target_angles, closed_target_values = _close_polar_curve(
            angles_rad=target_angles_rad,
            values=target_curve.firing_rates_hz,
        )
        ax.plot(
            closed_target_angles,
            closed_target_values,
            color=TARGET_COLOR,
            linestyle=TARGET_LINESTYLE,
            linewidth=1.5,
            label="target",
        )

    # Preferred-direction annotation drawn from the per-angle mean.
    theta_pref_rad, theta_pref_deg, r_peak_hz = _compute_preferred_direction_rad(
        angles_deg=curve.angles_deg,
        firing_rates_hz=mean_hz,
    )
    ax.annotate(
        text="",
        xy=(theta_pref_rad, r_peak_hz),
        xytext=(0.0, 0.0),
        xycoords="polar",
        arrowprops={
            "arrowstyle": "->",
            "color": PREFERRED_ARROW_COLOR,
            "lw": 2.0,
        },
    )
    ax.set_title(f"Polar tuning curve (preferred direction = {theta_pref_deg:.0f} deg)")
    ax.legend(loc="lower right", frameon=True, bbox_to_anchor=(1.15, -0.05))

    fig.tight_layout()
    fig.savefig(
        fname=out_png,
        dpi=DEFAULT_DPI,
        facecolor=DEFAULT_FACECOLOR,
        bbox_inches=DEFAULT_BBOX_INCHES,
    )
    plt.close(fig=fig)
