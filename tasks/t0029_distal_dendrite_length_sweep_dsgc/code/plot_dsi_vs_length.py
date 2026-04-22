"""Plot DSI vs distal length multiplier (primary deliverable) and per-length polar diagnostics.

Primary chart ``results/images/dsi_vs_length.png``: two-panel Cartesian plot sharing the x-axis
(length multiplier), left axis ``direction_selectivity_index`` (blue, Okabe-Ito), right axis
``peak_hz`` (orange). If the classification is ``monotonic`` the regression line is overlaid on the
DSI axis; if ``saturating`` a vertical dashed line at the saturation multiplier is drawn. Baseline
(1.0x) is marked with a star. Structurally cloned from the summary-plot function in
``tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/plot_polar_tuning.py``.

Diagnostic charts (one per length multiplier):
``results/images/polar_L<m>.png`` — polar tuning curve rendered via the t0011
``tuning_curve_viz.plot_polar_tuning_curve`` helper.
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

from tasks.t0011_response_visualization_library.code.tuning_curve_viz import (
    plot_polar_tuning_curve,
)
from tasks.t0029_distal_dendrite_length_sweep_dsgc.code.constants import (
    LENGTH_MULTIPLIERS,
    SHAPE_MONOTONIC,
    SHAPE_SATURATING,
)
from tasks.t0029_distal_dendrite_length_sweep_dsgc.code.paths import (
    CURVE_SHAPE_JSON,
    DSI_VS_LENGTH_PNG,
    METRICS_PER_LENGTH_CSV,
    per_length_curve_csv,
    polar_png,
)

# Okabe-Ito colour palette (matches the project's tuning_curve_viz library).
COLOR_DSI: str = "#0072B2"  # blue
COLOR_PEAK: str = "#E69F00"  # orange
COLOR_REGRESSION: str = "#009E73"  # green
COLOR_SATURATION: str = "#CC79A7"  # magenta


@dataclass(frozen=True, slots=True)
class MetricsRow:
    """One row of ``metrics_per_length.csv`` used for plotting."""

    length_multiplier: float
    peak_hz: float
    null_hz: float
    dsi_peak_null: float
    hwhm_deg: float


def _read_metrics_csv(*, metrics_csv: Path) -> list[MetricsRow]:
    """Load and sort by multiplier."""
    rows: list[MetricsRow] = []
    with metrics_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(
                MetricsRow(
                    length_multiplier=float(row["length_multiplier"]),
                    peak_hz=float(row["peak_hz"]),
                    null_hz=float(row["null_hz"]),
                    dsi_peak_null=float(row["dsi_peak_null"]),
                    hwhm_deg=float(row["hwhm_deg"]),
                ),
            )
    rows.sort(key=lambda r: r.length_multiplier)
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
    """Two-panel Cartesian plot: DSI (left axis) + peak_hz (right axis) vs length multiplier."""
    xs: list[float] = [m.length_multiplier for m in metrics]
    dsi: list[float] = [m.dsi_peak_null for m in metrics]
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

    shape_class: str = str(shape_info["shape_class"])
    if shape_class == SHAPE_MONOTONIC:
        slope: float = float(shape_info["slope"])
        intercept: float = float(shape_info["intercept"])
        xs_line: list[float] = [min(xs), max(xs)]
        ys_line: list[float] = [slope * x + intercept for x in xs_line]
        ax_dsi.plot(
            xs_line,
            ys_line,
            color=COLOR_REGRESSION,
            linestyle=":",
            linewidth=1.5,
            label=f"regression (slope={slope:.3f})",
        )
    if shape_class == SHAPE_SATURATING and shape_info.get("saturation_multiplier") is not None:
        sat_mul: float = float(shape_info["saturation_multiplier"])
        ax_dsi.axvline(
            x=sat_mul,
            color=COLOR_SATURATION,
            linestyle="--",
            linewidth=1.5,
            alpha=0.7,
            label=f"saturation @ {sat_mul:.2f}x",
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

    ax_dsi.set_xlabel("Distal dendrite length multiplier")
    ax_dsi.set_ylabel("DSI (peak - null) / (peak + null)", color=COLOR_DSI)
    ax_dsi.tick_params(axis="y", labelcolor=COLOR_DSI)
    ax_dsi.set_ylim(0.0, 1.05)
    ax_dsi.grid(True, alpha=0.35)

    ax_peak.set_ylabel("Firing rate (Hz)", color=COLOR_PEAK)
    ax_peak.tick_params(axis="y", labelcolor=COLOR_PEAK)
    peak_top: float = max(max(peak_hz), max(null_hz)) if len(peak_hz) > 0 else 1.0
    ax_peak.set_ylim(0.0, 1.15 * (peak_top if peak_top > 0.0 else 1.0))

    ax_dsi.set_title(
        f"DSI vs distal length (t0022 testbed) — class: {shape_class}",
    )

    # Combined legend.
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


def plot_polar_diagnostics(*, multipliers: tuple[float, ...]) -> list[Path]:
    """Emit one polar plot per length multiplier using the t0011 library."""
    out_paths: list[Path] = []
    for multiplier in multipliers:
        curve_csv: Path = per_length_curve_csv(multiplier=multiplier)
        if not curve_csv.exists():
            print(
                f"[plot_dsi_vs_length] SKIP polar for {multiplier}: {curve_csv} missing",
                flush=True,
            )
            continue
        out_png: Path = polar_png(multiplier=multiplier)
        out_png.parent.mkdir(parents=True, exist_ok=True)
        plot_polar_tuning_curve(
            curve_csv=curve_csv,
            out_png=out_png,
        )
        print(f"[plot_dsi_vs_length] wrote {out_png}", flush=True)
        out_paths.append(out_png)
    return out_paths


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--metrics",
        type=str,
        default=None,
        help="override per-length metrics CSV input path",
    )
    parser.add_argument(
        "--curve-shape",
        type=str,
        default=None,
        help="override curve-shape JSON input path",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="override primary chart output path",
    )
    parser.add_argument(
        "--no-polar",
        action="store_true",
        help="skip per-length polar diagnostic charts",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    metrics_csv: Path = Path(args.metrics) if args.metrics is not None else METRICS_PER_LENGTH_CSV
    shape_json: Path = Path(args.curve_shape) if args.curve_shape is not None else CURVE_SHAPE_JSON
    out_png: Path = Path(args.output) if args.output is not None else DSI_VS_LENGTH_PNG

    if not metrics_csv.exists():
        print(f"[plot_dsi_vs_length] ERROR: metrics CSV missing ({metrics_csv})", flush=True)
        return 1
    if not shape_json.exists():
        print(f"[plot_dsi_vs_length] ERROR: curve-shape JSON missing ({shape_json})", flush=True)
        return 1

    metrics: list[MetricsRow] = _read_metrics_csv(metrics_csv=metrics_csv)
    shape_info: dict[str, Any] = _read_curve_shape(curve_shape_json=shape_json)

    plot_primary(metrics=metrics, shape_info=shape_info, out_path=out_png)
    print(f"[plot_dsi_vs_length] wrote primary chart -> {out_png}", flush=True)

    if not args.no_polar:
        plot_polar_diagnostics(multipliers=LENGTH_MULTIPLIERS)

    return 0


if __name__ == "__main__":
    sys.exit(main())
