"""Compute per-length tuning-curve metrics from the t0034 sweep tidy CSV.

Groups the tidy CSV rows by ``length_multiplier`` and computes:

* DSI via the t0012 ``tuning_curve_loss.compute_dsi`` scorer (primary) -- peak-minus-null.
* DSI via vector-sum (secondary, diagnostic) -- Mazurek convention.
* Peak firing rate (``compute_peak_hz``).
* Null firing rate (``compute_null_hz``).
* HWHM (``compute_hwhm_deg``).
* Reliability (``compute_reliability``) -- split-half repeatability.
* Preferred-direction angle (argmax of per-angle mean firing rate).
* Preferred-direction firing rate.
* Mean somatic peak voltage across all trials at that length.

Writes ``results/data/metrics_per_length.csv`` and ``results/metrics.json`` (explicit multi-variant
format: one variant per sweep point with ``variant_id = "length_<m>"``, ``dimensions``, and
``metrics`` containing the three project-registered metric keys). Also writes a short
``results/data/metrics_notes.json`` documenting the intentional omission of ``tuning_curve_rmse``.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (
    TuningCurve,
    compute_dsi,
    compute_hwhm_deg,
    compute_null_hz,
    compute_peak_hz,
    compute_reliability,
    load_tuning_curve,
)
from tasks.t0034_distal_dendrite_length_sweep_t0024.code.constants import (
    CSV_COL_DIRECTION_DEG,
    CSV_COL_FIRING_RATE_HZ,
    CSV_COL_LENGTH_MULTIPLIER,
    CSV_COL_PEAK_MV,
    METRIC_KEY_DSI,
    METRIC_KEY_HWHM,
    METRIC_KEY_RELIABILITY,
)
from tasks.t0034_distal_dendrite_length_sweep_t0024.code.paths import (
    METRICS_JSON,
    METRICS_NOTES_JSON,
    METRICS_PER_LENGTH_CSV,
    SWEEP_CSV,
    per_length_curve_csv,
)


@dataclass(frozen=True, slots=True)
class LengthMetrics:
    """Per-length metrics record."""

    length_multiplier: float
    peak_hz: float
    null_hz: float
    dsi_primary: float
    dsi_vector_sum: float
    hwhm_deg: float
    reliability: float
    preferred_direction_deg: float
    preferred_hz: float
    mean_peak_mv: float


def _mean(values: list[float]) -> float:
    if len(values) == 0:
        return float("nan")
    return sum(values) / len(values)


def _vector_sum_dsi(
    *,
    angles_deg: list[int],
    rates_hz: list[float],
) -> tuple[float, float]:
    """Return ``(dsi, preferred_dir_deg)`` using the Mazurek vector-sum convention."""
    real_part: float = 0.0
    imag_part: float = 0.0
    rate_sum: float = 0.0
    for angle, rate in zip(angles_deg, rates_hz, strict=True):
        theta: float = math.radians(angle)
        real_part += rate * math.cos(theta)
        imag_part += rate * math.sin(theta)
        rate_sum += rate
    if rate_sum <= 0.0:
        return (0.0, float("nan"))
    magnitude: float = math.hypot(real_part, imag_part)
    dsi: float = magnitude / rate_sum
    preferred_dir_deg: float = math.degrees(math.atan2(imag_part, real_part)) % 360.0
    return (dsi, preferred_dir_deg)


def _preferred_angle_from_mean(
    *,
    angles_deg: list[int],
    mean_rates: list[float],
) -> tuple[float, float]:
    """Return ``(angle_deg, rate_hz)`` of the angle with the highest mean firing rate."""
    if len(angles_deg) == 0:
        return (float("nan"), float("nan"))
    idx_peak: int = 0
    peak_val: float = mean_rates[0]
    for i, val in enumerate(mean_rates):
        if val > peak_val:
            peak_val = val
            idx_peak = i
    return (float(angles_deg[idx_peak]), float(peak_val))


def _compute_one_length(
    *,
    multiplier: float,
    angle_to_rates: dict[int, list[float]],
    peak_mv_all_trials: list[float],
) -> LengthMetrics:
    """Compute metrics for one multiplier using the t0012 scorer + vector-sum helpers."""
    curve_csv: Path = per_length_curve_csv(multiplier=multiplier)
    if not curve_csv.exists():
        raise FileNotFoundError(
            f"per-length canonical CSV missing for multiplier {multiplier!r}: {curve_csv}",
        )
    curve: TuningCurve = load_tuning_curve(csv_path=curve_csv)

    dsi_primary: float = float(compute_dsi(curve=curve))
    peak_hz: float = float(compute_peak_hz(curve=curve))
    null_hz: float = float(compute_null_hz(curve=curve))
    hwhm: float = float(compute_hwhm_deg(curve=curve))
    try:
        reliability_raw = compute_reliability(curve=curve)
        reliability: float = float(reliability_raw) if reliability_raw is not None else float("nan")
    except ValueError:
        reliability = float("nan")

    angles: list[int] = sorted(angle_to_rates.keys())
    mean_rates: list[float] = [_mean(angle_to_rates[a]) for a in angles]
    dsi_vec, _vector_preferred_dir = _vector_sum_dsi(angles_deg=angles, rates_hz=mean_rates)
    preferred_dir_deg, preferred_hz = _preferred_angle_from_mean(
        angles_deg=angles,
        mean_rates=mean_rates,
    )

    return LengthMetrics(
        length_multiplier=float(multiplier),
        peak_hz=peak_hz,
        null_hz=null_hz,
        dsi_primary=dsi_primary,
        dsi_vector_sum=dsi_vec,
        hwhm_deg=hwhm,
        reliability=reliability,
        preferred_direction_deg=preferred_dir_deg,
        preferred_hz=preferred_hz,
        mean_peak_mv=_mean(peak_mv_all_trials),
    )


def compute_metrics_from_tidy(*, tidy_csv: Path) -> list[LengthMetrics]:
    """Return a list of per-length metric records sorted by ``length_multiplier``."""
    grouped_rates: dict[float, dict[int, list[float]]] = {}
    grouped_peak_mv: dict[float, list[float]] = {}
    with tidy_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            multiplier: float = float(row[CSV_COL_LENGTH_MULTIPLIER])
            angle: int = int(float(row[CSV_COL_DIRECTION_DEG]))
            rate: float = float(row[CSV_COL_FIRING_RATE_HZ])
            peak: float = float(row[CSV_COL_PEAK_MV])
            grouped_rates.setdefault(multiplier, {}).setdefault(angle, []).append(rate)
            grouped_peak_mv.setdefault(multiplier, []).append(peak)

    records: list[LengthMetrics] = []
    for multiplier in sorted(grouped_rates.keys()):
        records.append(
            _compute_one_length(
                multiplier=multiplier,
                angle_to_rates=grouped_rates[multiplier],
                peak_mv_all_trials=grouped_peak_mv[multiplier],
            ),
        )
    return records


def write_metrics_csv(*, records: list[LengthMetrics], out_path: Path) -> None:
    """Write the per-length metrics CSV."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "length_multiplier",
                "peak_hz",
                "null_hz",
                "dsi_primary",
                "dsi_vector_sum",
                "hwhm_deg",
                "reliability",
                "preferred_direction_deg",
                "preferred_hz",
                "mean_peak_mv",
            ],
        )
        writer.writeheader()
        for rec in records:
            writer.writerow(
                {
                    "length_multiplier": f"{rec.length_multiplier:.2f}",
                    "peak_hz": f"{rec.peak_hz:.4f}",
                    "null_hz": f"{rec.null_hz:.4f}",
                    "dsi_primary": f"{rec.dsi_primary:.6f}",
                    "dsi_vector_sum": f"{rec.dsi_vector_sum:.6f}",
                    "hwhm_deg": f"{rec.hwhm_deg:.4f}",
                    "reliability": f"{rec.reliability:.6f}",
                    "preferred_direction_deg": f"{rec.preferred_direction_deg:.2f}",
                    "preferred_hz": f"{rec.preferred_hz:.4f}",
                    "mean_peak_mv": f"{rec.mean_peak_mv:.3f}",
                },
            )


def _round_or_none(value: float, *, digits: int) -> float | None:
    if math.isnan(value):
        return None
    return round(value, digits)


def write_metrics_json(*, records: list[LengthMetrics], out_path: Path) -> None:
    """Write the explicit multi-variant ``metrics.json`` (one variant per length multiplier)."""
    variants: list[dict[str, object]] = []
    for rec in records:
        variant_id: str = f"length_{rec.length_multiplier:.2f}".replace(".", "p")
        variants.append(
            {
                "variant_id": variant_id,
                "label": f"distal L x {rec.length_multiplier:.2f}",
                "dimensions": {
                    "length_multiplier": rec.length_multiplier,
                },
                "metrics": {
                    METRIC_KEY_DSI: _round_or_none(rec.dsi_primary, digits=6),
                    METRIC_KEY_HWHM: _round_or_none(rec.hwhm_deg, digits=4),
                    METRIC_KEY_RELIABILITY: _round_or_none(rec.reliability, digits=6),
                },
            },
        )
    payload: dict[str, object] = {"variants": variants}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_metrics_notes(*, out_path: Path) -> None:
    """Write a short JSON explaining which registered metrics are intentionally omitted."""
    payload: dict[str, object] = {
        "omitted_metrics": ["tuning_curve_rmse"],
        "rationale": (
            "tuning_curve_rmse is computed against the t0004 target tuning curve. For this "
            "task only distal sec.L changes; stimulus biophysics is otherwise unchanged "
            "(AR(2) rho=0.6, V_rest=-60 mV). Target-fit RMSE is not informative for a length "
            "sweep on the t0024 testbed, so we report DSI / HWHM / reliability but omit RMSE."
        ),
        "primary_metric": "direction_selectivity_index",
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tidy",
        type=str,
        default=None,
        help="override tidy CSV input path",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    tidy_csv: Path = Path(args.tidy) if args.tidy is not None else SWEEP_CSV
    if not tidy_csv.exists():
        print(f"[analyse_sweep] ERROR: tidy CSV missing ({tidy_csv})", flush=True)
        return 1

    records: list[LengthMetrics] = compute_metrics_from_tidy(tidy_csv=tidy_csv)
    write_metrics_csv(records=records, out_path=METRICS_PER_LENGTH_CSV)
    write_metrics_json(records=records, out_path=METRICS_JSON)
    write_metrics_notes(out_path=METRICS_NOTES_JSON)
    print(f"[analyse_sweep] wrote {METRICS_PER_LENGTH_CSV}", flush=True)
    print(f"[analyse_sweep] wrote {METRICS_JSON}", flush=True)
    print(f"[analyse_sweep] wrote {METRICS_NOTES_JSON}", flush=True)

    print(
        f"  {'L_mul':>6s}  {'peak_hz':>7s}  {'null_hz':>7s}  "
        f"{'dsi_pr':>6s}  {'dsi_vs':>6s}  {'hwhm':>6s}  {'rel':>5s}  "
        f"{'pref':>6s}  {'prefHz':>7s}  {'peak_mv':>7s}",
        flush=True,
    )
    for rec in records:
        print(
            f"  {rec.length_multiplier:6.2f}  {rec.peak_hz:7.2f}  {rec.null_hz:7.2f}  "
            f"{rec.dsi_primary:6.3f}  {rec.dsi_vector_sum:6.3f}  "
            f"{rec.hwhm_deg:6.1f}  {rec.reliability:5.3f}  "
            f"{rec.preferred_direction_deg:6.1f}  {rec.preferred_hz:7.2f}  "
            f"{rec.mean_peak_mv:+7.1f}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
