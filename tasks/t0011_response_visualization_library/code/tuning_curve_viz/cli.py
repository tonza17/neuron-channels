"""Command-line entry point for tuning_curve_viz.

Usage::

    python -m tasks.t0011_response_visualization_library.code.tuning_curve_viz.cli \\
        --curve-csv <curve.csv> --out-dir <out/> \\
        [--target-csv <target.csv>] [--spike-times-csv <spikes.csv>]

Produces up to four plot types into ``--out-dir``: Cartesian, polar, overlay
(when ``--target-csv`` is supplied), and one raster+PSTH per distinct angle in
``--spike-times-csv`` (when supplied).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from tasks.t0011_response_visualization_library.code.tuning_curve_viz.cartesian import (
    plot_cartesian_tuning_curve,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.overlay import (
    plot_multi_model_overlay,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.polar import (
    plot_polar_tuning_curve,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.raster_psth import (
    ANGLE_DEG_COLUMN,
    plot_angle_raster_psth,
)


def _build_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="tuning_curve_viz.cli",
        description=(
            "Render Cartesian, polar, multi-model overlay, and per-angle raster+PSTH "
            "PNGs from a tuning-curve CSV."
        ),
    )
    parser.add_argument(
        "--curve-csv",
        type=Path,
        required=True,
        help="Path to the candidate tuning-curve CSV.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="Output directory for the generated PNGs.",
    )
    parser.add_argument(
        "--target-csv",
        type=Path,
        default=None,
        help="Optional target-curve CSV; enables the multi-model overlay.",
    )
    parser.add_argument(
        "--spike-times-csv",
        type=Path,
        default=None,
        help=(
            "Optional spike-time CSV; one raster+PSTH PNG is emitted per distinct angle_deg value."
        ),
    )
    parser.add_argument(
        "--curve-label",
        type=str,
        default="candidate",
        help="Label used for the candidate curve on the overlay plot.",
    )
    return parser


def main(*, argv: list[str] | None = None) -> int:
    parser: argparse.ArgumentParser = _build_parser()
    args: argparse.Namespace = parser.parse_args(args=argv)

    curve_csv: Path = args.curve_csv
    out_dir: Path = args.out_dir
    target_csv: Path | None = args.target_csv
    spike_times_csv: Path | None = args.spike_times_csv
    curve_label: str = args.curve_label

    if not curve_csv.exists():
        parser.error(message=f"curve-csv does not exist: {curve_csv}")
    if target_csv is not None and not target_csv.exists():
        parser.error(message=f"target-csv does not exist: {target_csv}")
    if spike_times_csv is not None and not spike_times_csv.exists():
        parser.error(message=f"spike-times-csv does not exist: {spike_times_csv}")

    out_dir.mkdir(parents=True, exist_ok=True)

    cartesian_png: Path = out_dir / "cartesian.png"
    polar_png: Path = out_dir / "polar.png"

    plot_cartesian_tuning_curve(
        curve_csv=curve_csv,
        out_png=cartesian_png,
        show_trials=True,
        target_csv=target_csv,
    )
    plot_polar_tuning_curve(
        curve_csv=curve_csv,
        out_png=polar_png,
        target_csv=target_csv,
    )

    if target_csv is not None:
        overlay_png: Path = out_dir / "overlay.png"
        plot_multi_model_overlay(
            curves_dict={curve_label: curve_csv},
            out_png=overlay_png,
            target_csv=target_csv,
        )

    if spike_times_csv is not None:
        df: pd.DataFrame = pd.read_csv(filepath_or_buffer=spike_times_csv)
        if ANGLE_DEG_COLUMN not in df.columns:
            parser.error(
                message=(f"spike-times-csv missing '{ANGLE_DEG_COLUMN}' column: {spike_times_csv}")
            )
        angles_deg: np.ndarray = np.array(
            sorted(set(df[ANGLE_DEG_COLUMN].astype(dtype=float))),
            dtype=np.float64,
        )
        for angle in angles_deg:
            raster_png: Path = out_dir / f"raster_psth_{int(round(angle))}deg.png"
            plot_angle_raster_psth(
                spike_times_csv=spike_times_csv,
                out_png=raster_png,
                angle_deg=float(angle),
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
