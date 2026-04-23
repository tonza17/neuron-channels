"""Plot four charts summarising the t0035 distal-diameter sweep on the t0024 DSGC testbed.

1. ``dsi_vs_diameter.png`` (primary, REQ-8): two-panel Cartesian -- left axis ``dsi_primary``,
   right axis ``peak_hz``. Overlays a regression line if ``mechanism_class`` != ``flat``.
   Baseline (1.0x) marked with a star.
2. ``vector_sum_dsi_vs_diameter.png`` (defensive fallback, REQ-9): single-panel Cartesian,
   ``dsi_vector_sum`` vs ``diameter_multiplier``.
3. ``polar_overlay.png`` (REQ-10): polar axes with seven viridis-coloured tuning curves, one per
   diameter multiplier, directly from the per-diameter canonical CSVs.
4. ``peak_hz_vs_diameter.png`` (REQ-11): single-panel Cartesian, peak & null Hz vs multiplier.

All PNGs are saved at 300 dpi.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")  # noqa: E402  -- non-interactive backend for CI / headless runs.
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.constants import (
    DIAMETER_MULTIPLIERS,
    MECHANISM_FLAT,
)
from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.paths import (
    CURVE_SHAPE_JSON,
    DSI_VS_DIAMETER_PNG,
    METRICS_PER_DIAMETER_CSV,
    PEAK_HZ_VS_DIAMETER_PNG,
    POLAR_OVERLAY_PNG,
    VECTOR_SUM_DSI_VS_DIAMETER_PNG,
    per_diameter_curve_csv,
)

# Okabe-Ito colour palette.
COLOR_DSI: str = "#0072B2"  # blue
COLOR_PEAK: str = "#E69F00"  # orange
COLOR_NULL: str = "#009E73"  # green
COLOR_REGRESSION: str = "#009E73"
COLOR_VECTOR_SUM: str = "#56B4E9"  # sky blue


@dataclass(frozen=True, slots=True)
class MetricsRow:
    """One row of ``metrics_per_diameter.csv`` used for plotting."""

    diameter_multiplier: float
    peak_hz: float
    null_hz: float
    dsi_primary: float
    dsi_vector_sum: float
    hwhm_deg: float


def _read_metrics_csv(*, metrics_csv: Path) -> list[MetricsRow]:
    """Load and sort by multiplier."""
    rows: list[MetricsRow] = []
    with metrics_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(
                MetricsRow(
                    diameter_multiplier=float(row["diameter_multiplier"]),
                    peak_hz=float(row["peak_hz"]),
                    null_hz=float(row["null_hz"]),
                    dsi_primary=float(row["dsi_primary"]),
                    dsi_vector_sum=float(row["dsi_vector_sum"]),
                    hwhm_deg=float(row["hwhm_deg"]),
                ),
            )
    rows.sort(key=lambda r: r.diameter_multiplier)
    return rows


def _read_curve_shape(*, curve_shape_json: Path) -> dict[str, Any]:
    payload: Any = json.loads(curve_shape_json.read_text(encoding="utf-8"))
    assert isinstance(payload, dict), "curve_shape JSON is a top-level object"
    return payload


def plot_primary(
    *,
    metrics: list[MetricsRow],
    shape_info: dict[str, Any],
    out_path: Path,
) -> None:
    """Two-panel Cartesian plot: DSI (left axis) + peak_hz (right axis) vs diameter multiplier."""
    xs: list[float] = [m.diameter_multiplier for m in metrics]
    dsi: list[float] = [m.dsi_primary for m in metrics]
    peak_hz: list[float] = [m.peak_hz for m in metrics]
    null_hz: list[float] = [m.null_hz for m in metrics]

    fig, ax_dsi = plt.subplots(figsize=(7.2, 4.5))
    ax_peak = ax_dsi.twinx()

    ax_dsi.plot(
        xs,
        dsi,
        marker="o",
        color=COLOR_DSI,
        linewidth=2.0,
        markersize=7.0,
        label="DSI (peak-null)",
    )
    ax_peak.plot(
        xs,
        peak_hz,
        marker="s",
        color=COLOR_PEAK,
        linewidth=2.0,
        markersize=6.0,
        label="peak firing (Hz)",
    )
    ax_peak.plot(
        xs,
        null_hz,
        marker="^",
        color=COLOR_PEAK,
        linewidth=1.0,
        linestyle="--",
        markersize=5.0,
        alpha=0.55,
        label="null firing (Hz)",
    )

    mechanism_class: str = str(shape_info["mechanism_class"])
    if mechanism_class != MECHANISM_FLAT:
        slope: float = float(shape_info["slope"])
        intercept: float = float(shape_info["intercept"])
        # Regression in log2-space: dsi = slope * log2(multiplier) + intercept.
        xs_line: list[float] = [min(xs), max(xs)]
        ys_line: list[float] = [slope * np.log2(x) + intercept for x in xs_line]
        ax_dsi.plot(
            xs_line,
            ys_line,
            color=COLOR_REGRESSION,
            linestyle=":",
            linewidth=1.5,
            label=f"regression (slope={slope:.3f}/log2(x))",
        )

    # Baseline star.
    if 1.0 in xs:
        i: int = xs.index(1.0)
        ax_dsi.plot(
            [xs[i]],
            [dsi[i]],
            marker="*",
            markersize=18.0,
            color="#D55E00",
            markeredgecolor="black",
            markeredgewidth=1.0,
            zorder=10,
            label="baseline (1.0x)",
        )

    ax_dsi.set_xlabel("Distal dendrite diameter multiplier")
    ax_dsi.set_xscale("log", base=2)
    ax_dsi.set_ylabel("DSI (peak - null) / (peak + null)", color=COLOR_DSI)
    ax_dsi.tick_params(axis="y", labelcolor=COLOR_DSI)
    ax_dsi.set_ylim(0.0, 1.05)
    ax_dsi.grid(True, alpha=0.35)

    ax_peak.set_ylabel("Firing rate (Hz)", color=COLOR_PEAK)
    ax_peak.tick_params(axis="y", labelcolor=COLOR_PEAK)
    peak_top: float = max(max(peak_hz), max(null_hz)) if len(peak_hz) > 0 else 1.0
    ax_peak.set_ylim(0.0, 1.15 * (peak_top if peak_top > 0.0 else 1.0))

    ax_dsi.set_title(
        f"DSI vs distal diameter (t0024 testbed) -- class: {mechanism_class}",
    )

    lines_1, labels_1 = ax_dsi.get_legend_handles_labels()
    lines_2, labels_2 = ax_peak.get_legend_handles_labels()
    ax_dsi.legend(
        lines_1 + lines_2,
        labels_1 + labels_2,
        loc="lower right",
        fontsize=9,
        framealpha=0.9,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_vector_sum(
    *,
    metrics: list[MetricsRow],
    shape_info: dict[str, Any],
    out_path: Path,
) -> None:
    """Single-panel Cartesian plot of vector-sum DSI vs diameter multiplier."""
    xs: list[float] = [m.diameter_multiplier for m in metrics]
    dsi_vs: list[float] = [m.dsi_vector_sum for m in metrics]

    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ax.plot(
        xs,
        dsi_vs,
        marker="o",
        color=COLOR_VECTOR_SUM,
        linewidth=2.0,
        markersize=7.0,
        label="vector-sum DSI",
    )

    if 1.0 in xs:
        i: int = xs.index(1.0)
        ax.plot(
            [xs[i]],
            [dsi_vs[i]],
            marker="*",
            markersize=18.0,
            color="#D55E00",
            markeredgecolor="black",
            markeredgewidth=1.0,
            zorder=10,
            label="baseline (1.0x)",
        )

    ax.set_xlabel("Distal dendrite diameter multiplier")
    ax.set_xscale("log", base=2)
    ax.set_ylabel("Vector-sum DSI (Mazurek)")
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, alpha=0.35)
    secondary_class: str = str(shape_info.get("shape_class_vector_sum", "unknown"))
    ax.set_title(
        f"Vector-sum DSI vs distal diameter (t0024 testbed) -- class: {secondary_class}",
    )
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_polar_overlay(
    *,
    multipliers: tuple[float, ...],
    out_path: Path,
) -> None:
    """Polar axes with one line per diameter multiplier (viridis palette)."""
    fig, ax_raw = plt.subplots(
        figsize=(7.0, 7.0),
        subplot_kw={"projection": "polar"},
    )
    ax: Any = ax_raw
    ax.set_theta_direction(1)
    ax.set_theta_offset(0.0)

    cmap = matplotlib.colormaps["viridis"]

    max_rate_seen: float = 0.0
    n_lines: int = len(multipliers)
    for i, multiplier in enumerate(multipliers):
        curve_csv: Path = per_diameter_curve_csv(multiplier=multiplier)
        if not curve_csv.exists():
            print(
                f"[plot_sweep] SKIP polar line for D={multiplier:.2f}: {curve_csv} missing",
                flush=True,
            )
            continue
        angle_to_rates: dict[int, list[float]] = {}
        with curve_csv.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                angle: int = int(float(row["angle_deg"]))
                rate: float = float(row["firing_rate_hz"])
                angle_to_rates.setdefault(angle, []).append(rate)
        sorted_angles: list[int] = sorted(angle_to_rates.keys())
        mean_rates: list[float] = [
            sum(angle_to_rates[a]) / len(angle_to_rates[a]) for a in sorted_angles
        ]
        if len(mean_rates) > 0:
            max_rate_seen = max(max_rate_seen, max(mean_rates))
        # Close the polygon.
        closed_angles_deg: list[int] = sorted_angles + [sorted_angles[0]]
        closed_rates: list[float] = mean_rates + [mean_rates[0]]
        theta_rad: np.ndarray = np.deg2rad(np.asarray(closed_angles_deg, dtype=np.float64))
        colour_val: float = i / max(1, n_lines - 1)
        ax.plot(
            theta_rad,
            np.asarray(closed_rates, dtype=np.float64),
            color=cmap(colour_val),
            linewidth=1.8,
            marker="o",
            markersize=4.0,
            label=f"D x {multiplier:.2f}",
        )

    ax.set_rlim(0.0, max(1.0, 1.10 * max_rate_seen))
    ax.set_title(
        "Tuning curve per distal diameter multiplier (t0024 testbed)",
        pad=20.0,
    )
    ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.10), fontsize=8, framealpha=0.9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_peak_hz(
    *,
    metrics: list[MetricsRow],
    out_path: Path,
) -> None:
    """Single-panel Cartesian plot of peak & null firing rate vs diameter multiplier."""
    xs: list[float] = [m.diameter_multiplier for m in metrics]
    peak_hz: list[float] = [m.peak_hz for m in metrics]
    null_hz: list[float] = [m.null_hz for m in metrics]

    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ax.plot(
        xs,
        peak_hz,
        marker="s",
        color=COLOR_PEAK,
        linewidth=2.0,
        markersize=7.0,
        label="peak Hz",
    )
    ax.plot(
        xs,
        null_hz,
        marker="^",
        color=COLOR_NULL,
        linewidth=2.0,
        markersize=7.0,
        label="null Hz",
    )
    ax.set_xlabel("Distal dendrite diameter multiplier")
    ax.set_xscale("log", base=2)
    ax.set_ylabel("Firing rate (Hz)")
    ax.grid(True, alpha=0.35)
    ax.set_title("Peak & null firing rate vs distal diameter (t0024 testbed)")
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--metrics",
        type=str,
        default=None,
        help="override per-diameter metrics CSV input path",
    )
    parser.add_argument(
        "--curve-shape",
        type=str,
        default=None,
        help="override curve-shape JSON input path",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    metrics_csv: Path = Path(args.metrics) if args.metrics is not None else METRICS_PER_DIAMETER_CSV
    shape_json: Path = Path(args.curve_shape) if args.curve_shape is not None else CURVE_SHAPE_JSON

    if not metrics_csv.exists():
        print(f"[plot_sweep] ERROR: metrics CSV missing ({metrics_csv})", flush=True)
        return 1
    if not shape_json.exists():
        print(f"[plot_sweep] ERROR: curve-shape JSON missing ({shape_json})", flush=True)
        return 1

    metrics: list[MetricsRow] = _read_metrics_csv(metrics_csv=metrics_csv)
    shape_info: dict[str, Any] = _read_curve_shape(curve_shape_json=shape_json)

    plot_primary(metrics=metrics, shape_info=shape_info, out_path=DSI_VS_DIAMETER_PNG)
    print(f"[plot_sweep] wrote primary chart -> {DSI_VS_DIAMETER_PNG}", flush=True)

    plot_vector_sum(
        metrics=metrics,
        shape_info=shape_info,
        out_path=VECTOR_SUM_DSI_VS_DIAMETER_PNG,
    )
    print(
        f"[plot_sweep] wrote vector-sum chart -> {VECTOR_SUM_DSI_VS_DIAMETER_PNG}",
        flush=True,
    )

    plot_polar_overlay(multipliers=DIAMETER_MULTIPLIERS, out_path=POLAR_OVERLAY_PNG)
    print(f"[plot_sweep] wrote polar overlay -> {POLAR_OVERLAY_PNG}", flush=True)

    plot_peak_hz(metrics=metrics, out_path=PEAK_HZ_VS_DIAMETER_PNG)
    print(f"[plot_sweep] wrote peak-Hz chart -> {PEAK_HZ_VS_DIAMETER_PNG}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
