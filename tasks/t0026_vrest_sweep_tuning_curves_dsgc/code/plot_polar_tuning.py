"""Polar and Cartesian plots of V_rest-modulated tuning curves.

Generates per-model:

* 8 individual polar plots, one per V_rest value (filename:
  ``polar_<model>_vrest_<+/-NN>mV.png``)
* 1 overlay polar plot showing all 8 curves on the same axes
  (``polar_<model>_overlay.png``)
* 1 Cartesian summary plot of (DSI, peak Hz) versus V_rest
  (``summary_<model>_vrest.png``)

Inputs: the tidy CSV (mean firing rate per (V_rest, angle) is computed inline)
and the metrics CSV produced by ``compute_vrest_metrics.py``.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # noqa: E402  (non-interactive backend)
import matplotlib.pyplot as plt

from tasks.t0026_vrest_sweep_tuning_curves_dsgc.code.constants import (
    CSV_COL_DIRECTION_DEG,
    CSV_COL_FIRING_RATE_HZ,
    CSV_COL_V_REST_MV,
    IMAGES_DIR,
    MODEL_LABEL_T0022,
    MODEL_LABEL_T0024,
    VREST_METRICS_T0022,
    VREST_METRICS_T0024,
    VREST_TIDY_T0022,
    VREST_TIDY_T0024,
)


def _read_tidy_to_mean_curves(*, tidy_csv: Path) -> dict[float, list[tuple[int, float]]]:
    """Return ``{v_rest_mv: [(angle_deg, mean_rate_hz), ...]}`` sorted by angle."""
    grouped: dict[float, dict[int, list[float]]] = {}
    with tidy_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            v_rest: float = float(row[CSV_COL_V_REST_MV])
            angle: int = int(float(row[CSV_COL_DIRECTION_DEG]))
            rate: float = float(row[CSV_COL_FIRING_RATE_HZ])
            grouped.setdefault(v_rest, {}).setdefault(angle, []).append(rate)
    out: dict[float, list[tuple[int, float]]] = {}
    for v_rest, angle_to_rates in grouped.items():
        angles: list[int] = sorted(angle_to_rates.keys())
        out[v_rest] = [(a, sum(angle_to_rates[a]) / len(angle_to_rates[a])) for a in angles]
    return out


def _read_metrics(*, metrics_csv: Path) -> list[dict[str, float]]:
    records: list[dict[str, float]] = []
    with metrics_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            records.append({k: float(v) for k, v in row.items()})
    records.sort(key=lambda r: r["v_rest_mv"])
    return records


def _close_polar(*, theta_rad: list[float], r: list[float]) -> tuple[list[float], list[float]]:
    return (theta_rad + [theta_rad[0]], r + [r[0]])


def plot_individual_polar(
    *,
    model_label: str,
    v_rest_mv: float,
    curve: list[tuple[int, float]],
    out_path: Path,
) -> None:
    angles_rad: list[float] = [math.radians(a) for a in [c[0] for c in curve]]
    rates_hz: list[float] = [c[1] for c in curve]
    theta_closed, r_closed = _close_polar(theta_rad=angles_rad, r=rates_hz)

    fig = plt.figure(figsize=(5.0, 5.0))
    ax = fig.add_subplot(111, projection="polar")
    ax.plot(theta_closed, r_closed, marker="o", linewidth=2.0, color="#1f77b4")
    ax.fill(theta_closed, r_closed, alpha=0.15, color="#1f77b4")
    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)
    ax.set_title(f"{model_label}  V_rest = {v_rest_mv:+.0f} mV")
    rmax = max(rates_hz) if max(rates_hz) > 0 else 1.0
    ax.set_rmax(1.05 * rmax)
    ax.grid(True, alpha=0.5)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_overlay_polar(
    *,
    model_label: str,
    curves_by_vrest: dict[float, list[tuple[int, float]]],
    out_path: Path,
) -> None:
    fig = plt.figure(figsize=(7.0, 7.0))
    ax = fig.add_subplot(111, projection="polar")
    cmap = plt.get_cmap("viridis")
    sorted_vrest: list[float] = sorted(curves_by_vrest.keys())
    rmax: float = 0.0
    for i, v_rest in enumerate(sorted_vrest):
        curve = curves_by_vrest[v_rest]
        angles_rad: list[float] = [math.radians(a) for a in [c[0] for c in curve]]
        rates_hz: list[float] = [c[1] for c in curve]
        theta_closed, r_closed = _close_polar(theta_rad=angles_rad, r=rates_hz)
        color = cmap(i / max(1, len(sorted_vrest) - 1))
        ax.plot(
            theta_closed,
            r_closed,
            marker="o",
            linewidth=1.5,
            color=color,
            label=f"{v_rest:+.0f} mV",
            markersize=4.0,
        )
        rmax = max(rmax, max(rates_hz))
    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)
    ax.set_title(f"{model_label}  V_rest sweep (overlay)")
    if rmax <= 0.0:
        rmax = 1.0
    ax.set_rmax(1.05 * rmax)
    ax.grid(True, alpha=0.5)
    ax.legend(loc="lower right", bbox_to_anchor=(1.30, 0.0), fontsize=8, frameon=True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_cartesian_summary(
    *,
    model_label: str,
    metrics: list[dict[str, float]],
    out_path: Path,
) -> None:
    v_rest = [m["v_rest_mv"] for m in metrics]
    peak_hz = [m["peak_hz"] for m in metrics]
    null_hz = [m["null_hz"] for m in metrics]
    dsi = [m["dsi"] for m in metrics]
    hwhm = [m["hwhm_deg"] for m in metrics]

    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.5))
    ax_rate, ax_dsi, ax_hwhm = axes

    ax_rate.plot(v_rest, peak_hz, marker="o", color="#d62728", label="peak (preferred)")
    ax_rate.plot(v_rest, null_hz, marker="s", color="#1f77b4", label="null")
    ax_rate.set_xlabel("V_rest (mV)")
    ax_rate.set_ylabel("Firing rate (Hz)")
    ax_rate.set_title(f"{model_label}  Peak vs Null Firing")
    ax_rate.legend()
    ax_rate.grid(True, alpha=0.4)

    ax_dsi.plot(v_rest, dsi, marker="o", color="#2ca02c")
    ax_dsi.set_xlabel("V_rest (mV)")
    ax_dsi.set_ylabel("DSI")
    ax_dsi.set_title(f"{model_label}  Direction-Selectivity Index")
    ax_dsi.set_ylim(0.0, 1.0)
    ax_dsi.grid(True, alpha=0.4)

    ax_hwhm.plot(v_rest, hwhm, marker="o", color="#9467bd")
    ax_hwhm.set_xlabel("V_rest (mV)")
    ax_hwhm.set_ylabel("HWHM (deg)")
    ax_hwhm.set_title(f"{model_label}  Tuning HWHM")
    ax_hwhm.grid(True, alpha=0.4)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def render_model(
    *,
    model_label: str,
    tidy_csv: Path,
    metrics_csv: Path,
    images_dir: Path,
) -> None:
    if not tidy_csv.exists():
        print(f"[plot] {model_label}: SKIP (missing tidy CSV {tidy_csv})", flush=True)
        return
    if not metrics_csv.exists():
        print(f"[plot] {model_label}: SKIP (missing metrics CSV {metrics_csv})", flush=True)
        return

    curves = _read_tidy_to_mean_curves(tidy_csv=tidy_csv)
    metrics = _read_metrics(metrics_csv=metrics_csv)

    images_dir.mkdir(parents=True, exist_ok=True)

    for v_rest, curve in sorted(curves.items()):
        sign = "+" if v_rest >= 0 else "-"
        fname = f"polar_{model_label}_vrest_{sign}{int(abs(v_rest)):02d}mV.png"
        plot_individual_polar(
            model_label=model_label,
            v_rest_mv=v_rest,
            curve=curve,
            out_path=images_dir / fname,
        )
        print(f"[plot] wrote {images_dir / fname}", flush=True)

    overlay_path = images_dir / f"polar_{model_label}_overlay.png"
    plot_overlay_polar(
        model_label=model_label,
        curves_by_vrest=curves,
        out_path=overlay_path,
    )
    print(f"[plot] wrote {overlay_path}", flush=True)

    summary_path = images_dir / f"summary_{model_label}_vrest.png"
    plot_cartesian_summary(
        model_label=model_label,
        metrics=metrics,
        out_path=summary_path,
    )
    print(f"[plot] wrote {summary_path}", flush=True)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        choices=("t0022", "t0024", "all"),
        default="all",
        help="which model to plot",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    if args.model in ("t0022", "all"):
        render_model(
            model_label=MODEL_LABEL_T0022,
            tidy_csv=VREST_TIDY_T0022,
            metrics_csv=VREST_METRICS_T0022,
            images_dir=IMAGES_DIR,
        )
    if args.model in ("t0024", "all"):
        render_model(
            model_label=MODEL_LABEL_T0024,
            tidy_csv=VREST_TIDY_T0024,
            metrics_csv=VREST_METRICS_T0024,
            images_dir=IMAGES_DIR,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
