"""Plot null-Hz and DSI against null-GABA conductance (5 charts).

Five outputs:

* **HEADLINE** ``results/images/null_hz_vs_gaba.png`` -- single-panel Cartesian, null_hz (Hz) vs
  null-GABA conductance (nS), Okabe-Ito palette, horizontal dashed red line at
  ``NULL_HZ_UNPINNING_THRESHOLD_HZ = 0.1 Hz``. The critical diagnostic for this task.
* ``results/images/primary_dsi_vs_gaba.png`` -- primary DSI (peak-minus-null) vs GABA. Expected
  to drop below 1.0 if any level unpins.
* ``results/images/vector_sum_dsi_vs_gaba.png`` -- vector-sum DSI vs GABA; complementary metric
  less sensitive to null pinning.
* ``results/images/peak_hz_vs_gaba.png`` -- preferred-direction peak firing rate vs GABA; the
  pre-condition gate chart (must stay >= 10 Hz at 4 nS).
* ``results/images/polar_overlay.png`` -- 5-colour polar overlay of all 5 per-GABA tuning curves
  via ``tuning_curve_viz.plot_multi_model_overlay``.

Structural clone of ``tasks/t0036_rerun_t0030_halved_null_gaba/code/plot_sweep.py`` with X-axis
labels and chart filenames rewritten for a GABA X-axis.
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
    plot_multi_model_overlay,
)
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.constants import (
    GABA_LEVELS_NS,
    NULL_HZ_UNPINNING_THRESHOLD_HZ,
    PEAK_HZ_MIN_PRECONDITION_HZ,
)
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.paths import (
    CURVE_SHAPE_JSON,
    METRICS_PER_GABA_CSV,
    NULL_HZ_VS_GABA_PNG,
    PEAK_HZ_VS_GABA_PNG,
    POLAR_OVERLAY_PNG,
    PRIMARY_DSI_VS_GABA_PNG,
    VECTOR_SUM_DSI_VS_GABA_PNG,
    gaba_label,
    per_gaba_curve_csv,
)

# Okabe-Ito colour palette (matches the project's tuning_curve_viz library).
COLOR_DSI: str = "#0072B2"  # blue
COLOR_DSI_VS: str = "#56B4E9"  # sky blue
COLOR_PEAK: str = "#E69F00"  # orange
COLOR_NULL: str = "#D55E00"  # vermillion
COLOR_BASELINE_STAR: str = "#CC79A7"  # magenta
COLOR_THRESHOLD: str = "#CC0000"  # red for the threshold line


@dataclass(frozen=True, slots=True)
class MetricsRow:
    """One row of ``metrics_per_gaba.csv`` used for plotting."""

    gaba_null_ns: float
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
                    gaba_null_ns=float(row["gaba_null_ns"]),
                    peak_hz=float(row["peak_hz"]),
                    null_hz=float(row["null_hz"]),
                    dsi_peak_null=float(row["dsi_peak_null"]),
                    dsi_vector_sum=float(row["dsi_vector_sum"]),
                    hwhm_deg=float(row["hwhm_deg"]),
                ),
            )
    rows.sort(key=lambda r: r.gaba_null_ns)
    return rows


def _read_curve_shape(*, curve_shape_json: Path) -> dict[str, Any]:
    payload: Any = json.loads(curve_shape_json.read_text(encoding="utf-8"))
    assert isinstance(payload, dict), "curve_shape JSON is a top-level object"
    return payload


def plot_null_hz_vs_gaba(
    *,
    metrics: list[MetricsRow],
    shape_info: dict[str, Any],
    out_path: Path,
) -> None:
    """HEADLINE chart: null-Hz vs GABA with unpinning threshold line."""
    xs: list[float] = [m.gaba_null_ns for m in metrics]
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
    ax.axhline(
        y=NULL_HZ_UNPINNING_THRESHOLD_HZ,
        linestyle="--",
        color=COLOR_THRESHOLD,
        linewidth=1.5,
        alpha=0.85,
        label=f"unpinning threshold ({NULL_HZ_UNPINNING_THRESHOLD_HZ} Hz)",
    )

    threshold_raw: object = shape_info.get("unpinning_threshold_ns")
    if threshold_raw is not None:
        threshold_ns: float = float(threshold_raw)  # type: ignore[arg-type]
        ax.axvline(
            x=threshold_ns,
            linestyle=":",
            color=COLOR_BASELINE_STAR,
            linewidth=1.5,
            alpha=0.85,
            label=f"unpinning at G={threshold_ns:.2f} nS",
        )

    y_max_observed: float = max(null_hz) if len(null_hz) > 0 else 0.0
    y_top: float = max(y_max_observed, NULL_HZ_UNPINNING_THRESHOLD_HZ) * 1.5
    if y_top <= 0.0:
        y_top = NULL_HZ_UNPINNING_THRESHOLD_HZ * 2.0
    ax.set_ylim(0.0, y_top)

    ax.set_xlabel("Null-GABA conductance (nS)")
    ax.set_ylabel("Null-direction firing rate (Hz)")
    ax.grid(True, alpha=0.35)
    ax.set_title(
        "Null-direction firing rate vs null-GABA conductance (t0022 DSGC, 1.0x distal diameter)",
    )
    ax.legend(loc="best", fontsize=9, framealpha=0.9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_primary_dsi_vs_gaba(
    *,
    metrics: list[MetricsRow],
    out_path: Path,
) -> None:
    """Primary DSI (peak-minus-null) vs GABA."""
    xs: list[float] = [m.gaba_null_ns for m in metrics]
    dsi: list[float] = [m.dsi_peak_null for m in metrics]

    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ax.plot(
        xs,
        dsi,
        marker="o",
        color=COLOR_DSI,
        linewidth=2.0,
        markersize=7.0,
        label="DSI (peak - null) / (peak + null)",
    )
    ax.set_xlabel("Null-GABA conductance (nS)")
    ax.set_ylabel("Primary DSI")
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, alpha=0.35)
    ax.set_title("Primary DSI vs null-GABA conductance (t0022 DSGC, 1.0x distal diameter)")
    ax.legend(loc="best", fontsize=9, framealpha=0.9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_vector_sum_dsi_vs_gaba(
    *,
    metrics: list[MetricsRow],
    out_path: Path,
) -> None:
    """Vector-sum DSI vs GABA (Mazurek & Kagan 2020 convention)."""
    xs: list[float] = [m.gaba_null_ns for m in metrics]
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
    ax.set_xlabel("Null-GABA conductance (nS)")
    ax.set_ylabel("DSI (vector sum, Mazurek & Kagan 2020)")
    y_min: float = min(dsi_vs) if len(dsi_vs) > 0 else 0.0
    y_max: float = max(dsi_vs) if len(dsi_vs) > 0 else 1.0
    y_pad: float = max(0.01, 0.2 * (y_max - y_min))
    ax.set_ylim(max(0.0, y_min - y_pad), min(1.0, y_max + y_pad))
    ax.grid(True, alpha=0.35)
    ax.set_title(
        "Vector-sum DSI vs null-GABA conductance (t0022 DSGC, 1.0x distal diameter)",
    )
    ax.legend(loc="best", fontsize=9, framealpha=0.9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_peak_hz_vs_gaba(
    *,
    metrics: list[MetricsRow],
    out_path: Path,
) -> None:
    """Peak-Hz pre-condition chart: preferred-direction peak firing vs GABA."""
    xs: list[float] = [m.gaba_null_ns for m in metrics]
    peak_hz: list[float] = [m.peak_hz for m in metrics]

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
    ax.axhline(
        y=PEAK_HZ_MIN_PRECONDITION_HZ,
        linestyle="--",
        color=COLOR_THRESHOLD,
        linewidth=1.5,
        alpha=0.85,
        label=f"pre-condition threshold ({PEAK_HZ_MIN_PRECONDITION_HZ} Hz)",
    )
    ax.set_xlabel("Null-GABA conductance (nS)")
    ax.set_ylabel("Peak firing rate (Hz)")
    y_top: float = max(max(peak_hz), PEAK_HZ_MIN_PRECONDITION_HZ) * 1.2 if len(peak_hz) > 0 else 1.0
    ax.set_ylim(0.0, y_top)
    ax.grid(True, alpha=0.35)
    ax.set_title("Peak firing rate vs null-GABA conductance (pre-condition gate)")
    ax.legend(loc="best", fontsize=9, framealpha=0.9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_polar_overlay_all(*, out_path: Path) -> Path | None:
    """Emit a 5-colour polar overlay of per-GABA tuning curves via the t0011 library."""
    curves: dict[str, Path] = {}
    for gaba_ns in GABA_LEVELS_NS:
        curve_csv: Path = per_gaba_curve_csv(gaba_null_ns=gaba_ns)
        if not curve_csv.exists():
            print(
                f"[plot_sweep] SKIP overlay for G={gaba_ns}: {curve_csv} missing",
                flush=True,
            )
            continue
        label: str = f"G{gaba_label(gaba_null_ns=gaba_ns)}"
        curves[label] = curve_csv
    if len(curves) == 0:
        print("[plot_sweep] no per-GABA curves available; skipping polar overlay", flush=True)
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
        help="override per-GABA metrics CSV input path",
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

    metrics_csv: Path = Path(args.metrics) if args.metrics is not None else METRICS_PER_GABA_CSV
    shape_json: Path = Path(args.curve_shape) if args.curve_shape is not None else CURVE_SHAPE_JSON

    if not metrics_csv.exists():
        print(f"[plot_sweep] ERROR: metrics CSV missing ({metrics_csv})", flush=True)
        return 1
    if not shape_json.exists():
        print(f"[plot_sweep] ERROR: curve-shape JSON missing ({shape_json})", flush=True)
        return 1

    metrics: list[MetricsRow] = _read_metrics_csv(metrics_csv=metrics_csv)
    shape_info: dict[str, Any] = _read_curve_shape(curve_shape_json=shape_json)

    plot_null_hz_vs_gaba(metrics=metrics, shape_info=shape_info, out_path=NULL_HZ_VS_GABA_PNG)
    print(f"[plot_sweep] wrote HEADLINE null-Hz chart -> {NULL_HZ_VS_GABA_PNG}", flush=True)

    plot_primary_dsi_vs_gaba(metrics=metrics, out_path=PRIMARY_DSI_VS_GABA_PNG)
    print(f"[plot_sweep] wrote primary DSI chart -> {PRIMARY_DSI_VS_GABA_PNG}", flush=True)

    plot_vector_sum_dsi_vs_gaba(metrics=metrics, out_path=VECTOR_SUM_DSI_VS_GABA_PNG)
    print(
        f"[plot_sweep] wrote vector-sum DSI chart -> {VECTOR_SUM_DSI_VS_GABA_PNG}",
        flush=True,
    )

    plot_peak_hz_vs_gaba(metrics=metrics, out_path=PEAK_HZ_VS_GABA_PNG)
    print(f"[plot_sweep] wrote peak-Hz chart -> {PEAK_HZ_VS_GABA_PNG}", flush=True)

    if not args.no_overlay:
        overlay_path: Path | None = plot_polar_overlay_all(out_path=POLAR_OVERLAY_PNG)
        if overlay_path is not None:
            print(f"[plot_sweep] wrote polar overlay -> {overlay_path}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
