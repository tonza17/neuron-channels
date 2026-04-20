"""Side-by-side Cartesian + polar multi-model overlay plot.

Accepts a mapping from model label to CSV path. Draws each model in its own
Okabe-Ito colour on both subplots. The optional target curve is always dashed black.
When more than :data:`MAX_OVERLAY_MODELS` models are supplied the overlay emits a
:class:`UserWarning` and truncates to the first six keys (sorted insertion order).
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.projections.polar import PolarAxes

from tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants import (
    DEFAULT_BBOX_INCHES,
    DEFAULT_DPI,
    DEFAULT_FACECOLOR,
    MAX_OVERLAY_MODELS,
    MODEL_COLORS,
    TARGET_COLOR,
    TARGET_LINESTYLE,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.loaders import (
    TuningCurve,
    load_curve,
)


def _close_polar_curve(
    *,
    angles_rad: np.ndarray,
    values: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    closed_angles: np.ndarray = np.concatenate([angles_rad, angles_rad[:1]])
    closed_values: np.ndarray = np.concatenate([values, values[:1]])
    return closed_angles, closed_values


def _cap_models(*, curves_dict: dict[str, Path]) -> dict[str, Path]:
    """Cap ``curves_dict`` at :data:`MAX_OVERLAY_MODELS` entries.

    Preserves insertion order. Emits a :class:`UserWarning` when the cap is triggered.
    """
    if len(curves_dict) <= MAX_OVERLAY_MODELS:
        return curves_dict
    warnings.warn(
        message=(
            f"plot_multi_model_overlay: {len(curves_dict)} models supplied; "
            f"truncating to the first {MAX_OVERLAY_MODELS} keys to preserve "
            "Okabe-Ito colour distinguishability."
        ),
        category=UserWarning,
        stacklevel=2,
    )
    capped_keys: list[str] = list(curves_dict.keys())[:MAX_OVERLAY_MODELS]
    return {key: curves_dict[key] for key in capped_keys}


def plot_multi_model_overlay(
    curves_dict: dict[str, Path],
    out_png: Path,
    *,
    target_csv: Path | None = None,
) -> None:
    """Side-by-side Cartesian + polar overlay of several tuning curves.

    Parameters
    ----------
    curves_dict:
        Mapping from model label to the CSV path. Up to :data:`MAX_OVERLAY_MODELS`
        models are rendered; extras are dropped with a :class:`UserWarning`.
    out_png:
        Destination PNG path; parent directory must exist.
    target_csv:
        Optional target curve, drawn as dashed black on both subplots.
    """
    if len(curves_dict) == 0:
        raise ValueError("plot_multi_model_overlay requires at least one curve")
    capped: dict[str, Path] = _cap_models(curves_dict=curves_dict)

    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(13.0, 5.5))
    cartesian_ax = fig.add_subplot(1, 2, 1)
    polar_ax: PolarAxes = cast(PolarAxes, fig.add_subplot(1, 2, 2, projection="polar"))
    polar_ax.set_theta_direction(direction=1)
    polar_ax.set_theta_offset(offset=0.0)

    for model_idx, (model_label, csv_path) in enumerate(iterable=capped.items()):
        curve: TuningCurve = load_curve(csv_path=csv_path)
        color: str = MODEL_COLORS[model_idx]
        cartesian_ax.plot(
            curve.angles_deg,
            curve.firing_rates_hz,
            color=color,
            linewidth=2.0,
            marker="o",
            label=model_label,
        )
        angles_rad: np.ndarray = np.deg2rad(curve.angles_deg)
        closed_angles, closed_values = _close_polar_curve(
            angles_rad=angles_rad,
            values=curve.firing_rates_hz,
        )
        polar_ax.plot(
            closed_angles,
            closed_values,
            color=color,
            linewidth=2.0,
            marker="o",
            label=model_label,
        )

    if target_csv is not None:
        target_curve: TuningCurve = load_curve(csv_path=target_csv)
        cartesian_ax.plot(
            target_curve.angles_deg,
            target_curve.firing_rates_hz,
            color=TARGET_COLOR,
            linestyle=TARGET_LINESTYLE,
            linewidth=1.5,
            label="target",
        )
        target_angles_rad: np.ndarray = np.deg2rad(target_curve.angles_deg)
        closed_target_angles, closed_target_values = _close_polar_curve(
            angles_rad=target_angles_rad,
            values=target_curve.firing_rates_hz,
        )
        polar_ax.plot(
            closed_target_angles,
            closed_target_values,
            color=TARGET_COLOR,
            linestyle=TARGET_LINESTYLE,
            linewidth=1.5,
            label="target",
        )

    cartesian_ax.set_xlabel("Direction (deg)")
    cartesian_ax.set_ylabel("Firing rate (Hz)")
    cartesian_ax.set_title("Cartesian overlay")
    cartesian_ax.grid(visible=True, alpha=0.3)
    cartesian_ax.legend(loc="best", frameon=True)

    polar_ax.set_title("Polar overlay")
    polar_ax.legend(loc="lower right", bbox_to_anchor=(1.25, -0.05), frameon=True)

    fig.tight_layout()
    fig.savefig(
        fname=out_png,
        dpi=DEFAULT_DPI,
        facecolor=DEFAULT_FACECOLOR,
        bbox_inches=DEFAULT_BBOX_INCHES,
    )
    plt.close(fig=fig)
