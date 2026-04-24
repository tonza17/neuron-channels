"""Compute per-GABA tuning-curve metrics from the t0037 sweep tidy CSV.

Groups the tidy CSV rows by ``gaba_null_ns`` and computes:

* Primary DSI via the t0012 ``tuning_curve_loss.compute_dsi`` scorer (peak-minus-null).
* Vector-sum DSI (Mazurek & Kagan 2020).
* Peak firing rate (``compute_peak_hz``).
* Null firing rate (``compute_null_hz``) -- **the critical diagnostic** for this task.
* HWHM (``compute_hwhm_deg``).
* Reliability (``compute_reliability``) -- split-half repeatability.
* Preferred direction (vector-sum angle).
* Mean somatic peak voltage across all trials at that GABA level.

Writes ``results/data/metrics_per_gaba.csv``, ``results/data/dsi_by_gaba.csv``, and
``results/metrics.json`` (explicit multi-variant format, one variant per GABA level:
``variant_id = "gaba_<v>"``, ``dimensions = {"gaba_null_ns": <v>}``).

Structural clone of ``tasks/t0036_rerun_t0030_halved_null_gaba/code/analyse_sweep.py`` with the
aggregation key renamed from ``diameter_multiplier`` to ``gaba_null_ns``.
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
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.constants import (
    CSV_COL_DIRECTION_DEG,
    CSV_COL_FIRING_RATE_HZ,
    CSV_COL_GABA_NULL_NS,
    CSV_COL_PEAK_MV,
    METRIC_KEY_DSI,
    METRIC_KEY_HWHM,
    METRIC_KEY_RELIABILITY,
)
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.paths import (
    DSI_BY_GABA_CSV,
    METRICS_JSON,
    METRICS_NOTES_JSON,
    METRICS_PER_GABA_CSV,
    SWEEP_CSV,
    per_gaba_curve_csv,
)


@dataclass(frozen=True, slots=True)
class GabaMetrics:
    """Per-GABA-level metrics record."""

    gaba_null_ns: float
    peak_hz: float
    null_hz: float
    dsi_peak_null: float
    dsi_vector_sum: float
    hwhm_deg: float
    reliability: float
    preferred_dir_deg: float
    mean_peak_mv: float


def _mean(values: list[float]) -> float:
    if len(values) == 0:
        return float("nan")
    return sum(values) / len(values)


def _vector_sum_dsi(*, angles_deg: list[int], rates_hz: list[float]) -> tuple[float, float]:
    """Return ``(dsi, preferred_dir_deg)`` using the Mazurek & Kagan vector-sum convention."""
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


def _compute_one_gaba(
    *,
    gaba_null_ns: float,
    angle_to_rates: dict[int, list[float]],
    peak_mv_all_trials: list[float],
) -> GabaMetrics:
    """Compute metrics for one GABA level via the t0012 scorer (primary) + vector-sum (aux)."""
    curve_csv: Path = per_gaba_curve_csv(gaba_null_ns=gaba_null_ns)
    if not curve_csv.exists():
        raise FileNotFoundError(
            f"per-GABA canonical CSV missing for gaba_null_ns={gaba_null_ns!r}: {curve_csv}",
        )
    curve: TuningCurve = load_tuning_curve(csv_path=curve_csv)

    dsi_peak_null: float = float(compute_dsi(curve=curve))
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
    dsi_vec, preferred_dir = _vector_sum_dsi(angles_deg=angles, rates_hz=mean_rates)

    return GabaMetrics(
        gaba_null_ns=float(gaba_null_ns),
        peak_hz=peak_hz,
        null_hz=null_hz,
        dsi_peak_null=dsi_peak_null,
        dsi_vector_sum=dsi_vec,
        hwhm_deg=hwhm,
        reliability=reliability,
        preferred_dir_deg=preferred_dir,
        mean_peak_mv=_mean(peak_mv_all_trials),
    )


def compute_metrics_from_tidy(*, tidy_csv: Path) -> list[GabaMetrics]:
    """Return a list of per-GABA metric records sorted by ``gaba_null_ns`` ascending."""
    grouped_rates: dict[float, dict[int, list[float]]] = {}
    grouped_peak_mv: dict[float, list[float]] = {}
    with tidy_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            gaba_ns: float = float(row[CSV_COL_GABA_NULL_NS])
            angle: int = int(float(row[CSV_COL_DIRECTION_DEG]))
            rate: float = float(row[CSV_COL_FIRING_RATE_HZ])
            peak: float = float(row[CSV_COL_PEAK_MV])
            grouped_rates.setdefault(gaba_ns, {}).setdefault(angle, []).append(rate)
            grouped_peak_mv.setdefault(gaba_ns, []).append(peak)

    records: list[GabaMetrics] = []
    for gaba_ns in sorted(grouped_rates.keys()):
        records.append(
            _compute_one_gaba(
                gaba_null_ns=gaba_ns,
                angle_to_rates=grouped_rates[gaba_ns],
                peak_mv_all_trials=grouped_peak_mv[gaba_ns],
            ),
        )
    return records


def write_metrics_csv(*, records: list[GabaMetrics], out_path: Path) -> None:
    """Write the per-GABA metrics CSV."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "gaba_null_ns",
                "peak_hz",
                "null_hz",
                "dsi_peak_null",
                "dsi_vector_sum",
                "hwhm_deg",
                "reliability",
                "preferred_dir_deg",
                "mean_peak_mv",
            ],
        )
        writer.writeheader()
        for rec in records:
            writer.writerow(
                {
                    "gaba_null_ns": f"{rec.gaba_null_ns:.2f}",
                    "peak_hz": f"{rec.peak_hz:.4f}",
                    "null_hz": f"{rec.null_hz:.4f}",
                    "dsi_peak_null": f"{rec.dsi_peak_null:.6f}",
                    "dsi_vector_sum": f"{rec.dsi_vector_sum:.6f}",
                    "hwhm_deg": f"{rec.hwhm_deg:.4f}",
                    "reliability": f"{rec.reliability:.6f}",
                    "preferred_dir_deg": f"{rec.preferred_dir_deg:.2f}",
                    "mean_peak_mv": f"{rec.mean_peak_mv:.3f}",
                },
            )


def write_dsi_by_gaba_csv(*, records: list[GabaMetrics], out_path: Path) -> None:
    """Write the focused DSI + null-Hz deliverable table."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "gaba_null_ns",
                "direction_selectivity_index",
                "dsi_vector_sum",
                "peak_hz",
                "null_hz",
                "hwhm_deg",
            ],
        )
        writer.writeheader()
        for rec in records:
            writer.writerow(
                {
                    "gaba_null_ns": f"{rec.gaba_null_ns:.2f}",
                    "direction_selectivity_index": f"{rec.dsi_peak_null:.6f}",
                    "dsi_vector_sum": f"{rec.dsi_vector_sum:.6f}",
                    "peak_hz": f"{rec.peak_hz:.4f}",
                    "null_hz": f"{rec.null_hz:.4f}",
                    "hwhm_deg": f"{rec.hwhm_deg:.4f}",
                },
            )


def _round_or_none(value: float, *, digits: int) -> float | None:
    if math.isnan(value):
        return None
    return round(value, digits)


def write_metrics_json(*, records: list[GabaMetrics], out_path: Path) -> None:
    """Write the explicit multi-variant ``metrics.json`` (one variant per GABA level)."""
    variants: list[dict[str, object]] = []
    for rec in records:
        variant_id: str = f"gaba_{rec.gaba_null_ns:.2f}".replace(".", "p")
        variants.append(
            {
                "variant_id": variant_id,
                "label": f"null-GABA = {rec.gaba_null_ns:.2f} nS",
                "dimensions": {
                    "gaba_null_ns": rec.gaba_null_ns,
                },
                "metrics": {
                    METRIC_KEY_DSI: _round_or_none(rec.dsi_peak_null, digits=6),
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
            "task only null-direction GABA conductance changes; the stimulus and biophysics "
            "otherwise match the t0022 baseline. Target-fit RMSE is not informative for a GABA "
            "ladder sweep, so we report DSI / HWHM / reliability but omit RMSE."
        ),
        "primary_metric": "direction_selectivity_index",
        "critical_diagnostic": "null_hz",
        "secondary_metrics_recorded": [
            "dsi_vector_sum",
            "peak_hz",
            "null_hz",
            "hwhm_deg",
            "reliability",
            "preferred_dir_deg",
            "mean_peak_mv",
        ],
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

    records: list[GabaMetrics] = compute_metrics_from_tidy(tidy_csv=tidy_csv)
    write_metrics_csv(records=records, out_path=METRICS_PER_GABA_CSV)
    write_dsi_by_gaba_csv(records=records, out_path=DSI_BY_GABA_CSV)
    write_metrics_json(records=records, out_path=METRICS_JSON)
    write_metrics_notes(out_path=METRICS_NOTES_JSON)
    print(f"[analyse_sweep] wrote {METRICS_PER_GABA_CSV}", flush=True)
    print(f"[analyse_sweep] wrote {DSI_BY_GABA_CSV}", flush=True)
    print(f"[analyse_sweep] wrote {METRICS_JSON}", flush=True)
    print(f"[analyse_sweep] wrote {METRICS_NOTES_JSON}", flush=True)

    print(
        f"  {'G_nS':>6s}  {'peak_hz':>7s}  {'null_hz':>7s}  "
        f"{'dsi_pn':>6s}  {'dsi_vs':>6s}  {'hwhm':>6s}  {'rel':>5s}  "
        f"{'pref':>6s}  {'peak_mv':>7s}",
        flush=True,
    )
    for rec in records:
        print(
            f"  {rec.gaba_null_ns:6.2f}  {rec.peak_hz:7.2f}  {rec.null_hz:7.2f}  "
            f"{rec.dsi_peak_null:6.3f}  {rec.dsi_vector_sum:6.3f}  "
            f"{rec.hwhm_deg:6.1f}  {rec.reliability:5.3f}  "
            f"{rec.preferred_dir_deg:6.1f}  {rec.mean_peak_mv:+7.1f}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
