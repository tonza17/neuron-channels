"""Compute per-(model, V_rest) tuning-curve metrics from tidy CSVs.

Reads each model's `vrest_sweep_tidy.csv` and emits a per-V_rest metrics CSV
with columns: ``v_rest_mv``, ``peak_hz``, ``null_hz``, ``dsi``, ``hwhm_deg``,
``preferred_dir_deg``, ``mean_peak_mv``. Also prints a tidy summary table to
stdout.

The DSI is computed as the magnitude of the vector-sum of mean firing rate
across angles, normalized by the sum of mean firing rates (Mazurek et al.
convention also used in ``tuning_curve_loss``):

    DSI = |sum_i r_i * exp(i * theta_i)| / sum_i r_i

where r_i is the mean firing rate at angle theta_i. HWHM is the angular
distance from the preferred direction at which firing rate falls to half the
peak; computed by linear interpolation around the preferred direction.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

from tasks.t0026_vrest_sweep_tuning_curves_dsgc.code.constants import (
    ANGLES_DEG,
    CSV_COL_DIRECTION_DEG,
    CSV_COL_FIRING_RATE_HZ,
    CSV_COL_PEAK_MV,
    CSV_COL_V_REST_MV,
    DATA_T0022_DIR,
    DATA_T0024_DIR,
    VREST_METRICS_T0022,
    VREST_METRICS_T0024,
    VREST_TIDY_T0022,
    VREST_TIDY_T0024,
)


def _mean(values: list[float]) -> float:
    if len(values) == 0:
        return float("nan")
    return sum(values) / len(values)


def _vector_sum_dsi(*, angles_deg: list[int], rates_hz: list[float]) -> tuple[float, float]:
    """Return (dsi, preferred_dir_deg) using Mazurek vector-sum convention."""
    real_part: float = 0.0
    imag_part: float = 0.0
    rate_sum: float = 0.0
    for angle, rate in zip(angles_deg, rates_hz, strict=True):
        theta = math.radians(angle)
        real_part += rate * math.cos(theta)
        imag_part += rate * math.sin(theta)
        rate_sum += rate
    if rate_sum <= 0.0:
        return (0.0, float("nan"))
    magnitude: float = math.hypot(real_part, imag_part)
    dsi: float = magnitude / rate_sum
    preferred_dir_deg: float = math.degrees(math.atan2(imag_part, real_part)) % 360.0
    return (dsi, preferred_dir_deg)


def _hwhm_deg(*, angles_deg: list[int], rates_hz: list[float], preferred_dir_deg: float) -> float:
    """Half-width-at-half-maximum in degrees around ``preferred_dir_deg``.

    Returns NaN if the curve cannot be characterised (e.g., zero peak).
    Uses linear interpolation along the angular axis on either side of the
    preferred direction.
    """
    if math.isnan(preferred_dir_deg):
        return float("nan")
    peak_rate: float = max(rates_hz)
    if peak_rate <= 0.0:
        return float("nan")
    half_rate: float = 0.5 * peak_rate

    # Build two cycles to allow wrapping around the angular axis.
    pairs: list[tuple[float, float]] = sorted(
        zip([float(a) for a in angles_deg], rates_hz, strict=True),
        key=lambda x: x[0],
    )
    extended: list[tuple[float, float]] = pairs + [(a + 360.0, r) for a, r in pairs]

    # Find the angle in [pref-180, pref+180] closest to the preferred direction.
    pref = preferred_dir_deg
    # Walk away from preferred direction until rate drops below half.
    half_widths: list[float] = []
    for sign in (+1.0, -1.0):
        previous_offset: float = 0.0
        previous_rate: float = peak_rate
        # Sample at 1-degree resolution around the curve via linear interpolation.
        for offset_deg in range(1, 181):
            target_angle: float = (pref + sign * offset_deg) % 360.0
            interp_rate: float = _interp_circular(extended=extended, angle_deg=target_angle)
            if interp_rate <= half_rate:
                # Linear interpolation between previous_offset and offset_deg.
                if previous_rate == interp_rate:
                    half_widths.append(float(offset_deg))
                else:
                    frac: float = (previous_rate - half_rate) / (previous_rate - interp_rate)
                    half_widths.append(previous_offset + frac * (offset_deg - previous_offset))
                break
            previous_offset = float(offset_deg)
            previous_rate = interp_rate
        else:
            half_widths.append(180.0)
    return float(_mean(half_widths))


def _interp_circular(*, extended: list[tuple[float, float]], angle_deg: float) -> float:
    # Normalise angle to [0, 360).
    angle_deg = angle_deg % 360.0
    # Find bracketing pair within first cycle [0, 360].
    # extended covers [0, 360) repeated up to 720, so any value in [0, 360] is bracketed.
    for i in range(len(extended) - 1):
        a0, r0 = extended[i]
        a1, r1 = extended[i + 1]
        if a0 <= angle_deg <= a1:
            if a1 == a0:
                return r0
            frac: float = (angle_deg - a0) / (a1 - a0)
            return r0 + frac * (r1 - r0)
    return float("nan")


def _null_dir_deg(preferred_dir_deg: float) -> float:
    return (preferred_dir_deg + 180.0) % 360.0


def _nearest_angle_rate(
    *,
    angles_deg: list[int],
    rates_hz: list[float],
    target_deg: float,
) -> float:
    # Use linear interpolation on the discrete sample set.
    pairs: list[tuple[float, float]] = sorted(
        zip([float(a) for a in angles_deg], rates_hz, strict=True),
        key=lambda x: x[0],
    )
    extended: list[tuple[float, float]] = pairs + [(a + 360.0, r) for a, r in pairs]
    return _interp_circular(extended=extended, angle_deg=target_deg)


def compute_metrics_from_tidy(*, tidy_csv: Path) -> list[dict[str, float]]:
    """Return a list of per-V_rest metric records sorted by ``v_rest_mv``."""
    grouped: dict[float, dict[int, list[float]]] = {}
    grouped_peak_mv: dict[float, list[float]] = {}
    with tidy_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            v_rest: float = float(row[CSV_COL_V_REST_MV])
            angle: int = int(float(row[CSV_COL_DIRECTION_DEG]))
            rate: float = float(row[CSV_COL_FIRING_RATE_HZ])
            peak: float = float(row[CSV_COL_PEAK_MV])
            grouped.setdefault(v_rest, {}).setdefault(angle, []).append(rate)
            grouped_peak_mv.setdefault(v_rest, []).append(peak)

    records: list[dict[str, float]] = []
    for v_rest in sorted(grouped.keys()):
        angle_to_rates = grouped[v_rest]
        angles: list[int] = sorted(angle_to_rates.keys())
        mean_rates: list[float] = [_mean(angle_to_rates[a]) for a in angles]
        peak_hz: float = max(mean_rates) if len(mean_rates) > 0 else float("nan")
        dsi, preferred_dir = _vector_sum_dsi(angles_deg=angles, rates_hz=mean_rates)
        null_dir = _null_dir_deg(preferred_dir) if not math.isnan(preferred_dir) else float("nan")
        null_hz: float = (
            _nearest_angle_rate(angles_deg=angles, rates_hz=mean_rates, target_deg=null_dir)
            if not math.isnan(null_dir)
            else float("nan")
        )
        hwhm = _hwhm_deg(angles_deg=angles, rates_hz=mean_rates, preferred_dir_deg=preferred_dir)
        records.append(
            {
                "v_rest_mv": v_rest,
                "peak_hz": peak_hz,
                "null_hz": null_hz,
                "dsi": dsi,
                "hwhm_deg": hwhm,
                "preferred_dir_deg": preferred_dir,
                "mean_peak_mv": _mean(grouped_peak_mv[v_rest]),
            },
        )
    return records


def write_metrics_csv(*, records: list[dict[str, float]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "v_rest_mv",
                "peak_hz",
                "null_hz",
                "dsi",
                "hwhm_deg",
                "preferred_dir_deg",
                "mean_peak_mv",
            ],
        )
        writer.writeheader()
        for rec in records:
            writer.writerow(
                {
                    "v_rest_mv": f"{rec['v_rest_mv']:.1f}",
                    "peak_hz": f"{rec['peak_hz']:.4f}",
                    "null_hz": f"{rec['null_hz']:.4f}",
                    "dsi": f"{rec['dsi']:.4f}",
                    "hwhm_deg": f"{rec['hwhm_deg']:.4f}",
                    "preferred_dir_deg": f"{rec['preferred_dir_deg']:.2f}",
                    "mean_peak_mv": f"{rec['mean_peak_mv']:.3f}",
                },
            )


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        choices=("t0022", "t0024", "all"),
        default="all",
        help="which model's tidy CSV to process",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    targets: list[tuple[str, Path, Path]] = []
    if args.model in ("t0022", "all"):
        targets.append(("t0022", VREST_TIDY_T0022, VREST_METRICS_T0022))
    if args.model in ("t0024", "all"):
        targets.append(("t0024", VREST_TIDY_T0024, VREST_METRICS_T0024))

    for label, tidy, out in targets:
        if not tidy.exists():
            print(f"[compute_vrest_metrics] {label}: SKIP (missing tidy CSV {tidy})", flush=True)
            continue
        records = compute_metrics_from_tidy(tidy_csv=tidy)
        write_metrics_csv(records=records, out_path=out)
        print(f"[compute_vrest_metrics] {label}: wrote {out}", flush=True)
        print(
            f"  {'V_rest':>7s}  {'peak_hz':>7s}  {'null_hz':>7s}  {'dsi':>5s}  "
            f"{'hwhm':>6s}  {'pref':>6s}  {'peak_mv':>7s}",
            flush=True,
        )
        for rec in records:
            print(
                f"  {rec['v_rest_mv']:+7.1f}  {rec['peak_hz']:7.2f}  {rec['null_hz']:7.2f}  "
                f"{rec['dsi']:5.3f}  {rec['hwhm_deg']:6.1f}  {rec['preferred_dir_deg']:6.1f}  "
                f"{rec['mean_peak_mv']:+7.1f}",
                flush=True,
            )

    _ = (DATA_T0022_DIR, DATA_T0024_DIR, ANGLES_DEG, CSV_COL_PEAK_MV)  # silence unused
    return 0


if __name__ == "__main__":
    sys.exit(main())
