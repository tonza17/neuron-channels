"""Plot DSI vs distal-diameter multiplier (primary + secondary + polar + null-Hz diagnostic).

Five outputs (t0030 produced four; this task adds the new ``null_hz_vs_diameter.png``
pre-condition diagnostic):

* Primary ``results/images/dsi_vs_diameter.png`` -- two-panel Cartesian, Okabe-Ito palette:
  primary DSI (left axis) + peak/null Hz (right axis) vs ``diameter_multiplier``. Baseline
  (1.0x) annotated with a star. If ``mechanism_label != "flat"``, overlay the regression line
  on the DSI panel.
* Secondary ``results/images/vector_sum_dsi_vs_diameter.png`` -- single-panel vector-sum DSI
  vs ``diameter_multiplier`` (the REQ-12 slope-sign diagnostic that remains informative under
  primary DSI saturation).
* Diagnostic ``results/images/peak_hz_vs_diameter.png`` -- single-panel peak Hz + null Hz vs
  ``diameter_multiplier`` (mitigation against primary DSI saturation).
* **NEW** ``results/images/null_hz_vs_diameter.png`` -- the pre-condition diagnostic: single
  panel Cartesian with a horizontal dashed line at the pre-condition threshold.
* Optional ``results/images/polar_overlay.png`` -- seven-colour polar overlay of the
  per-diameter tuning curves via ``tuning_curve_viz.plot_multi_model_overlay``.

Structurally cloned from
``tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/plot_sweep.py`` with cross-task import
rewrites and the new ``_plot_null_hz_vs_diameter`` function.
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
import math

import matplotlib.pyplot as plt

from tasks.t0011_response_visualization_library.code.tuning_curve_viz import (
    plot_multi_model_overlay,
)
from tasks.t0036_rerun_t0030_halved_null_gaba.code.constants import (
    DIAMETER_MULTIPLIERS,
    MECHANISM_FLAT,
    NULL_HZ_MIN_PRECONDITION_HZ,
)
from tasks.t0036_rerun_t0030_halved_null_gaba.code.paths import (
    CURVE_SHAPE_JSON,
    DSI_VS_DIAMETER_PNG,
    METRICS_PER_DIAMETER_CSV,
    NULL_HZ_VS_DIAMETER_PNG,
    PEAK_HZ_VS_DIAMETER_PNG,
    POLAR_OVERLAY_PNG,
    VECTOR_SUM_DSI_VS_DIAMETER_PNG,
    multiplier_label,
    per_diameter_curve_csv,
)

# Okabe-Ito colour palette (matches the project's tuning_curve_viz library).
COLOR_DSI: str = "#0072B2"  # blue
COLOR_DSI_VS: str = "#56B4E9"  # sky blue
COLOR_PEAK: str = "#E69F00"  # orange
COLOR_NULL: str = "#D55E00"  # vermillion
COLOR_REGRESSION: str = "#009E73"  # green
COLOR_BASELINE_STAR: str = "#CC79A7"  # magenta
COLOR_THRESHOLD: str = "#CC0000"  # red for the pre-condition threshold line


@dataclass(frozen=True, slots=True)
class MetricsRow:
    """One row of ``metrics_per_diameter.csv`` used for plotting."""

    diameter_multiplier: float
    peak_hz: float
    null_hz: float
    dsi_peak_null: float
    dsi_vector_sum: float
    hwhm_deg: float


def _read_metrics_csv(*, metrics_csv: Path) -> list[MetricsRow]:
    rows: list[MetricsRow] = []
    with metrics_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(
                MetricsRow(
                    diameter_multiplier=float(row["diameter_multiplier"]),
                    peak_hz=float(row["peak_hz"]),
                    null_hz=float(row["null_hz"]),
                    dsi_peak_null=float(row["dsi_peak_null"]),
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
    """Two-panel Cartesian plot: primary DSI (left axis) + peak_hz/null_hz (right axis)."""
    xs: list[float] = [m.diameter_multiplier for m in metrics]
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
        color=COLOR_NULL,
        linewidth=1.0,
        linestyle="--",
        markersize=5.0,
        alpha=0.75,
        label="null firing (Hz)",
    )

    mechanism_label: str = str(shape_info["mechanism_label"])
    # Strip _partial for the "is-flat?" decision -- we still want to draw the regression line
    # if the underlying label (pre-suffix) is non-flat.
    base_label: str = str(shape_info.get("base_mechanism_label", mechanism_label))
    if base_label != MECHANISM_FLAT:
        primary_slope: float = float(shape_info["primary_regression"]["slope"])
        primary_intercept: float = float(shape_info["primary_regression"]["intercept"])
        xs_line: list[float] = [min(xs), max(xs)]
        ys_line: list[float] = [primary_slope * math.log2(x) + primary_intercept for x in xs_line]
        ax_dsi.plot(
            xs_line,
            ys_line,
            color=COLOR_REGRESSION,
            linestyle=":",
            linewidth=1.5,
            label=f"regression (slope={primary_slope:.3f} per log2 m)",
        )

    if 1.0 in xs:
        i: int = xs.index(1.0)
        ax_dsi.plot(
            [xs[i]],
            [dsi[i]],
            marker="*",
            markersize=18.0,
            color=COLOR_BASELINE_STAR,
            markeredgecolor="black",
            markeredgewidth=1.0,
            zorder=10,
            label="baseline (1.0x)",
        )

    ax_dsi.set_xlabel("Distal dendrite diameter multiplier")
    ax_dsi.set_ylabel("DSI (peak - null) / (peak + null)", color=COLOR_DSI)
    ax_dsi.tick_params(axis="y", labelcolor=COLOR_DSI)
    ax_dsi.set_ylim(0.0, 1.05)
    ax_dsi.grid(True, alpha=0.35)

    ax_peak.set_ylabel("Firing rate (Hz)", color=COLOR_PEAK)
    ax_peak.tick_params(axis="y", labelcolor=COLOR_PEAK)
    peak_top: float = max(max(peak_hz), max(null_hz)) if len(peak_hz) > 0 else 1.0
    ax_peak.set_ylim(0.0, 1.15 * (peak_top if peak_top > 0.0 else 1.0))

    ax_dsi.set_title(
        f"DSI vs distal diameter (t0022 testbed, halved null-GABA) -- mechanism: {mechanism_label}",
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
    """Single-panel vector-sum DSI vs diameter multiplier (REQ-12 mitigation)."""
    xs: list[float] = [m.diameter_multiplier for m in metrics]
    dsi_vs: list[float] = [m.dsi_vector_sum for m in metrics]

    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ax.plot(
        xs,
        dsi_vs,
        marker="D",
        color=COLOR_DSI_VS,
        linewidth=2.0,
        markersize=7.0,
        label="DSI (vector sum)",
    )

    vs_slope: float = float(shape_info["vector_sum_regression"]["slope"])
    vs_intercept: float = float(shape_info["vector_sum_regression"]["intercept"])
    xs_line: list[float] = [min(xs), max(xs)]
    ys_line: list[float] = [vs_slope * math.log2(x) + vs_intercept for x in xs_line]
    ax.plot(
        xs_line,
        ys_line,
        color=COLOR_REGRESSION,
        linestyle=":",
        linewidth=1.5,
        label=f"regression (slope={vs_slope:.4f} per log2 m)",
    )

    if 1.0 in xs:
        i: int = xs.index(1.0)
        ax.plot(
            [xs[i]],
            [dsi_vs[i]],
            marker="*",
            markersize=18.0,
            color=COLOR_BASELINE_STAR,
            markeredgecolor="black",
            markeredgewidth=1.0,
            zorder=10,
            label="baseline (1.0x)",
        )

    y_min: float = min(dsi_vs)
    y_max: float = max(dsi_vs)
    y_pad: float = max(0.01, 0.2 * (y_max - y_min))
    ax.set_ylim(max(0.0, y_min - y_pad), min(1.0, y_max + y_pad))
    ax.set_xlabel("Distal dendrite diameter multiplier")
    ax.set_ylabel("DSI (vector sum, Mazurek & Kagan 2020)")
    ax.grid(True, alpha=0.35)
    mechanism_label: str = str(shape_info["mechanism_label"])
    used_fallback: bool = bool(shape_info.get("used_fallback_vector_sum_dsi", False))
    title_suffix: str = " (REQ-12 fallback)" if used_fallback else ""
    ax.set_title(
        f"Vector-sum DSI vs distal diameter -- mechanism: {mechanism_label}{title_suffix}",
    )
    ax.legend(loc="best", fontsize=9, framealpha=0.9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_peak_hz(*, metrics: list[MetricsRow], out_path: Path) -> None:
    """Diagnostic single-panel peak Hz + null Hz vs diameter multiplier."""
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
        label="peak firing (Hz)",
    )
    ax.plot(
        xs,
        null_hz,
        marker="^",
        color=COLOR_NULL,
        linewidth=1.5,
        markersize=6.0,
        label="null firing (Hz)",
    )
    ax.set_xlabel("Distal dendrite diameter multiplier")
    ax.set_ylabel("Firing rate (Hz)")
    ax.grid(True, alpha=0.35)
    ax.set_title("Peak / null firing rate vs distal diameter")
    ax.legend(loc="best", fontsize=9, framealpha=0.9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_null_hz_vs_diameter(
    *,
    metrics: list[MetricsRow],
    shape_info: dict[str, Any],
    out_path: Path,
) -> None:
    """NEW pre-condition diagnostic: null-Hz vs diameter with threshold line."""
    xs: list[float] = [m.diameter_multiplier for m in metrics]
    null_hz: list[float] = [m.null_hz for m in metrics]

    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ax.plot(
        xs,
        null_hz,
        marker="^",
        color=COLOR_NULL,
        linewidth=2.0,
        markersize=7.0,
        label="null firing (Hz)",
    )

    # Horizontal dashed threshold line.
    ax.axhline(
        y=NULL_HZ_MIN_PRECONDITION_HZ,
        linestyle="--",
        color=COLOR_THRESHOLD,
        linewidth=1.5,
        alpha=0.85,
        label=f"pre-condition threshold ({NULL_HZ_MIN_PRECONDITION_HZ} Hz)",
    )

    # Baseline annotation and pre-condition pass/fail star.
    precondition_pass: bool = bool(shape_info.get("precondition_pass", False))
    baseline_color: str = COLOR_BASELINE_STAR if precondition_pass else COLOR_THRESHOLD
    if 1.0 in xs:
        i: int = xs.index(1.0)
        ax.plot(
            [xs[i]],
            [null_hz[i]],
            marker="*",
            markersize=18.0,
            color=baseline_color,
            markeredgecolor="black",
            markeredgewidth=1.0,
            zorder=10,
            label=(f"baseline (1.0x) -- pre-condition {'PASS' if precondition_pass else 'FAIL'}"),
        )

    y_max_observed: float = max(null_hz) if len(null_hz) > 0 else 0.0
    y_top: float = max(y_max_observed, NULL_HZ_MIN_PRECONDITION_HZ) * 1.3
    if y_top <= 0.0:
        y_top = NULL_HZ_MIN_PRECONDITION_HZ * 2.0
    ax.set_ylim(0.0, y_top)

    ax.set_xlabel("Distal dendrite diameter multiplier")
    ax.set_ylabel("Null-direction firing rate (Hz)")
    ax.grid(True, alpha=0.35)
    ax.set_title("Null-direction firing rate vs distal diameter (halved null-GABA)")
    ax.legend(loc="best", fontsize=9, framealpha=0.9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_polar_overlay_all(*, out_path: Path) -> Path | None:
    """Emit a 7-colour polar overlay of per-diameter tuning curves via the t0011 library."""
    curves: dict[str, Path] = {}
    for multiplier in DIAMETER_MULTIPLIERS:
        curve_csv: Path = per_diameter_curve_csv(multiplier=multiplier)
        if not curve_csv.exists():
            print(
                f"[plot_sweep] SKIP overlay for {multiplier}: {curve_csv} missing",
                flush=True,
            )
            continue
        label: str = f"D{multiplier_label(multiplier=multiplier)}"
        curves[label] = curve_csv
    if len(curves) == 0:
        print("[plot_sweep] no per-diameter curves available; skipping polar overlay", flush=True)
        return None
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plot_multi_model_overlay(curves_dict=curves, out_png=out_path)
    return out_path


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
    parser.add_argument(
        "--no-overlay",
        action="store_true",
        help="skip the polar overlay diagnostic chart",
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
    print(f"[plot_sweep] wrote vector-sum chart -> {VECTOR_SUM_DSI_VS_DIAMETER_PNG}", flush=True)

    plot_peak_hz(metrics=metrics, out_path=PEAK_HZ_VS_DIAMETER_PNG)
    print(f"[plot_sweep] wrote peak-hz chart -> {PEAK_HZ_VS_DIAMETER_PNG}", flush=True)

    plot_null_hz_vs_diameter(
        metrics=metrics,
        shape_info=shape_info,
        out_path=NULL_HZ_VS_DIAMETER_PNG,
    )
    print(f"[plot_sweep] wrote null-hz chart -> {NULL_HZ_VS_DIAMETER_PNG}", flush=True)

    if not args.no_overlay:
        overlay_path: Path | None = plot_polar_overlay_all(out_path=POLAR_OVERLAY_PNG)
        if overlay_path is not None:
            print(f"[plot_sweep] wrote polar overlay -> {overlay_path}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
