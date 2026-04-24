"""Plot primary DSI and vector-sum DSI vs electrotonic length L/lambda for both sweeps (REQ-2).

Produces three 300 dpi PNG overlays under ``results/images/``:

1. ``primary_dsi_vs_L_over_lambda.png`` — primary DSI vs L/lambda for t0034 (length sweep) and
   t0035 (diameter sweep) on the same axes, with distinct colour + marker per sweep. t0034
   spike-failure operating points (1.5x and 2.0x length multiplier) are drawn as hollow markers
   so the reader can see where the cable-theory collapse model is expected to fail.
2. ``vector_sum_dsi_vs_L_over_lambda.png`` — identical layout with vector-sum (Mazurek) DSI.
3. ``peak_hz_vs_L_over_lambda.png`` — peak firing rate vs L/lambda, context panel that helps
   diagnose whether any breakdown of collapse is tracking a spike-rate transition.

The plot style template (Okabe-Ito palette, 300 dpi, single-panel Cartesian figures, baseline
(``multiplier == 1.0``) marked with a star) is copied from
``tasks/t0034_distal_dendrite_length_sweep_t0024/code/plot_sweep.py`` per the cross-task import
rule.
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # noqa: E402 -- non-interactive backend for headless runs.
import matplotlib.pyplot as plt

from tasks.t0041_electrotonic_length_collapse_t0034_t0035.code.constants import (
    BASELINE_MULTIPLIER,
    OUT_COL_DSI_PRIMARY,
    OUT_COL_DSI_VECTOR_SUM,
    OUT_COL_L_OVER_LAMBDA,
    OUT_COL_MULTIPLIER,
    OUT_COL_PEAK_HZ,
    OUT_COL_SPIKE_FAILURE,
    OUT_COL_SWEEP,
    SWEEP_DIAMETER,
    SWEEP_LENGTH,
)
from tasks.t0041_electrotonic_length_collapse_t0034_t0035.code.paths import (
    ELECTROTONIC_TABLE_CSV,
    PEAK_HZ_COLLAPSE_PNG,
    PRIMARY_DSI_COLLAPSE_PNG,
    VECTOR_SUM_DSI_COLLAPSE_PNG,
)

# Okabe-Ito palette: length = blue, diameter = orange.
COLOR_LENGTH: str = "#0072B2"
COLOR_DIAMETER: str = "#E69F00"
COLOR_BASELINE: str = "#D55E00"
COLOR_SPIKE_FAILURE_EDGE: str = "#000000"

MARKER_LENGTH: str = "s"  # square
MARKER_DIAMETER: str = "o"  # circle


@dataclass(frozen=True, slots=True)
class CollapsePoint:
    """One row of the electrotonic-length table, parsed for plotting."""

    sweep: str
    multiplier: float
    L_over_lambda: float
    dsi_primary: float
    dsi_vector_sum: float
    peak_hz: float
    spike_failure_flag: bool


def read_collapse_points(*, csv_path: Path) -> list[CollapsePoint]:
    """Read the electrotonic-length table CSV into a list of CollapsePoint records."""
    assert csv_path.exists(), f"electrotonic-length table CSV must exist: {csv_path}"
    rows: list[CollapsePoint] = []
    with csv_path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            rows.append(
                CollapsePoint(
                    sweep=raw[OUT_COL_SWEEP],
                    multiplier=float(raw[OUT_COL_MULTIPLIER]),
                    L_over_lambda=float(raw[OUT_COL_L_OVER_LAMBDA]),
                    dsi_primary=float(raw[OUT_COL_DSI_PRIMARY]),
                    dsi_vector_sum=float(raw[OUT_COL_DSI_VECTOR_SUM]),
                    peak_hz=float(raw[OUT_COL_PEAK_HZ]),
                    spike_failure_flag=(raw[OUT_COL_SPIKE_FAILURE] == "1"),
                ),
            )
    return rows


def _split_by_sweep(
    *,
    points: list[CollapsePoint],
) -> tuple[list[CollapsePoint], list[CollapsePoint]]:
    """Return ``(length_points, diameter_points)``, sorted by L/lambda within each sweep."""
    length_points: list[CollapsePoint] = sorted(
        (p for p in points if p.sweep == SWEEP_LENGTH),
        key=lambda p: p.L_over_lambda,
    )
    diameter_points: list[CollapsePoint] = sorted(
        (p for p in points if p.sweep == SWEEP_DIAMETER),
        key=lambda p: p.L_over_lambda,
    )
    return (length_points, diameter_points)


def _plot_one_series(
    *,
    ax: plt.Axes,
    points: list[CollapsePoint],
    y_values: list[float],
    color: str,
    marker: str,
    label: str,
) -> None:
    """Scatter + line plot, with hollow markers on spike-failure points."""
    xs: list[float] = [p.L_over_lambda for p in points]
    # Solid line through all points (for visual continuity).
    ax.plot(
        xs,
        y_values,
        color=color,
        linewidth=1.6,
        alpha=0.55,
        zorder=2,
    )
    # Healthy (non-spike-failure) points as filled markers.
    healthy_idx: list[int] = [i for i, p in enumerate(points) if not p.spike_failure_flag]
    if len(healthy_idx) > 0:
        ax.scatter(
            [xs[i] for i in healthy_idx],
            [y_values[i] for i in healthy_idx],
            color=color,
            marker=marker,
            s=72.0,
            edgecolors=color,
            linewidths=1.0,
            zorder=3,
            label=label,
        )
    # Spike-failure points as hollow markers with black edge.
    failure_idx: list[int] = [i for i, p in enumerate(points) if p.spike_failure_flag]
    if len(failure_idx) > 0:
        ax.scatter(
            [xs[i] for i in failure_idx],
            [y_values[i] for i in failure_idx],
            facecolors="none",
            edgecolors=COLOR_SPIKE_FAILURE_EDGE,
            marker=marker,
            s=96.0,
            linewidths=1.4,
            zorder=4,
            label=f"{label} (spike-failure)",
        )


def _plot_baseline_marker(
    *,
    ax: plt.Axes,
    points: list[CollapsePoint],
    y_values: list[float],
) -> None:
    """Draw a star at each sweep's baseline (multiplier == 1.0) operating point."""
    for i, p in enumerate(points):
        if p.multiplier == BASELINE_MULTIPLIER:
            ax.plot(
                [p.L_over_lambda],
                [y_values[i]],
                marker="*",
                markersize=18.0,
                color=COLOR_BASELINE,
                markeredgecolor="black",
                markeredgewidth=1.0,
                zorder=10,
            )


def _draw_overlay(
    *,
    length_points: list[CollapsePoint],
    diameter_points: list[CollapsePoint],
    length_y: list[float],
    diameter_y: list[float],
    y_label: str,
    title: str,
    out_path: Path,
    y_min: float | None,
    y_max: float | None,
) -> None:
    """Shared helper for DSI / peak-Hz overlays."""
    fig, ax_raw = plt.subplots(figsize=(7.6, 4.8))
    ax: plt.Axes = ax_raw

    _plot_one_series(
        ax=ax,
        points=length_points,
        y_values=length_y,
        color=COLOR_LENGTH,
        marker=MARKER_LENGTH,
        label="t0034 length sweep",
    )
    _plot_one_series(
        ax=ax,
        points=diameter_points,
        y_values=diameter_y,
        color=COLOR_DIAMETER,
        marker=MARKER_DIAMETER,
        label="t0035 diameter sweep",
    )
    _plot_baseline_marker(ax=ax, points=length_points, y_values=length_y)
    _plot_baseline_marker(ax=ax, points=diameter_points, y_values=diameter_y)

    ax.set_xlabel("Electrotonic length L / lambda (dimensionless)")
    ax.set_ylabel(y_label)
    ax.grid(True, alpha=0.35)
    ax.set_title(title)
    if y_min is not None and y_max is not None:
        ax.set_ylim(y_min, y_max)
    ax.legend(loc="best", fontsize=9, framealpha=0.9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_primary_dsi(*, points: list[CollapsePoint], out_path: Path) -> None:
    """Overlay primary DSI vs L/lambda for both sweeps."""
    length_points, diameter_points = _split_by_sweep(points=points)
    _draw_overlay(
        length_points=length_points,
        diameter_points=diameter_points,
        length_y=[p.dsi_primary for p in length_points],
        diameter_y=[p.dsi_primary for p in diameter_points],
        y_label="Primary DSI (peak - null) / (peak + null)",
        title="Primary DSI vs electrotonic length L/lambda (t0024 testbed)",
        out_path=out_path,
        y_min=0.0,
        y_max=1.05,
    )


def plot_vector_sum_dsi(*, points: list[CollapsePoint], out_path: Path) -> None:
    """Overlay vector-sum (Mazurek) DSI vs L/lambda for both sweeps."""
    length_points, diameter_points = _split_by_sweep(points=points)
    _draw_overlay(
        length_points=length_points,
        diameter_points=diameter_points,
        length_y=[p.dsi_vector_sum for p in length_points],
        diameter_y=[p.dsi_vector_sum for p in diameter_points],
        y_label="Vector-sum DSI (Mazurek)",
        title="Vector-sum DSI vs electrotonic length L/lambda (t0024 testbed)",
        out_path=out_path,
        y_min=0.0,
        y_max=1.05,
    )


def plot_peak_hz(*, points: list[CollapsePoint], out_path: Path) -> None:
    """Overlay peak firing rate vs L/lambda for both sweeps."""
    length_points, diameter_points = _split_by_sweep(points=points)
    length_peak: list[float] = [p.peak_hz for p in length_points]
    diameter_peak: list[float] = [p.peak_hz for p in diameter_points]
    y_top: float = 1.15 * max(max(length_peak), max(diameter_peak))
    _draw_overlay(
        length_points=length_points,
        diameter_points=diameter_points,
        length_y=length_peak,
        diameter_y=diameter_peak,
        y_label="Peak firing rate (Hz)",
        title="Peak firing rate vs electrotonic length L/lambda (t0024 testbed)",
        out_path=out_path,
        y_min=0.0,
        y_max=y_top,
    )


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--table-csv",
        type=str,
        default=None,
        help="override the electrotonic-length table CSV input path",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    table_csv: Path = Path(args.table_csv) if args.table_csv is not None else ELECTROTONIC_TABLE_CSV
    if not table_csv.exists():
        print(
            f"[plot_collapse] ERROR: table CSV missing ({table_csv})",
            flush=True,
        )
        return 1
    points: list[CollapsePoint] = read_collapse_points(csv_path=table_csv)
    plot_primary_dsi(points=points, out_path=PRIMARY_DSI_COLLAPSE_PNG)
    print(f"[plot_collapse] wrote {PRIMARY_DSI_COLLAPSE_PNG}", flush=True)
    plot_vector_sum_dsi(points=points, out_path=VECTOR_SUM_DSI_COLLAPSE_PNG)
    print(f"[plot_collapse] wrote {VECTOR_SUM_DSI_COLLAPSE_PNG}", flush=True)
    plot_peak_hz(points=points, out_path=PEAK_HZ_COLLAPSE_PNG)
    print(f"[plot_collapse] wrote {PEAK_HZ_COLLAPSE_PNG}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
