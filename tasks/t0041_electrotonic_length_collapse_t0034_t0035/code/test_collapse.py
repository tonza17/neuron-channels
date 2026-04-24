"""Test whether t0034 length and t0035 diameter sweeps collapse onto one DSI-vs-L/lambda curve.

REQ-3 and REQ-4 of the t0041 plan:

1. Interpolate the t0035 diameter sweep onto the L/lambda grid visited by the t0034 length sweep
   (linear interpolation), yielding paired (t0034, t0035_interp) samples on a shared L/lambda
   axis.
2. Compute Pearson r between the two sweeps on the paired grid for both primary DSI and
   vector-sum DSI. Verdict:
   * ``collapse_confirmed`` if r > ``PEARSON_R_COLLAPSE_MIN`` (0.9) for BOTH metrics.
   * ``collapse_rejected`` otherwise.
3. Report the Pearson r *with* and *without* the two t0034 spike-failure operating points (1.5x
   and 2.0x length multiplier) so the reader can see whether the collapse fails for non-cable
   reasons (active spike failure) or for genuine cable-theory reasons.
4. Fit a single degree-2 polynomial to the combined (pooled) dataset and compute residual RMSE
   both pooled and per-sweep so the non-cable variance is quantified.

Writes ``results/collapse_stats.json`` and ``results/metrics.json``. The metrics JSON follows
the explicit multi-variant format with one variant per operating point, so each variant carries
the registered ``direction_selectivity_index`` metric keyed by L/lambda.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy import stats  # type: ignore[import-untyped]

from tasks.t0041_electrotonic_length_collapse_t0034_t0035.code.constants import (
    OUT_COL_DSI_PRIMARY,
    OUT_COL_DSI_VECTOR_SUM,
    OUT_COL_L_OVER_LAMBDA,
    OUT_COL_MULTIPLIER,
    OUT_COL_SPIKE_FAILURE,
    OUT_COL_SWEEP,
    PEARSON_R_COLLAPSE_MIN,
    POLYNOMIAL_DEGREE,
    SWEEP_DIAMETER,
    SWEEP_LENGTH,
    VERDICT_COLLAPSE_CONFIRMED,
    VERDICT_COLLAPSE_REJECTED,
)
from tasks.t0041_electrotonic_length_collapse_t0034_t0035.code.paths import (
    COLLAPSE_STATS_JSON,
    ELECTROTONIC_TABLE_CSV,
    METRICS_JSON,
)


@dataclass(frozen=True, slots=True)
class SweepPoint:
    """Minimal per-sweep record used by the collapse test."""

    sweep: str
    multiplier: float
    L_over_lambda: float
    dsi_primary: float
    dsi_vector_sum: float
    spike_failure_flag: bool


@dataclass(frozen=True, slots=True)
class PearsonSummary:
    """One Pearson-r correlation summary between two paired sequences."""

    n_points: int
    r: float
    p_value: float


@dataclass(frozen=True, slots=True)
class PolyFit:
    """Degree-2 polynomial fit of a scalar y against a scalar x."""

    coefficients_high_to_low: list[float]
    rmse_pooled: float
    rmse_length_sweep: float
    rmse_diameter_sweep: float


@dataclass(frozen=True, slots=True)
class CollapseReport:
    """Full collapse-test report emitted to ``collapse_stats.json``."""

    n_t0034_points: int
    n_t0035_points: int
    l_over_lambda_overlap_min: float
    l_over_lambda_overlap_max: float
    n_paired_points_full: int
    n_paired_points_no_spike_failure: int
    pearson_primary_full: PearsonSummary
    pearson_primary_no_spike_failure: PearsonSummary
    pearson_vector_sum_full: PearsonSummary
    pearson_vector_sum_no_spike_failure: PearsonSummary
    poly_fit_primary: PolyFit
    poly_fit_vector_sum: PolyFit
    verdict_primary: str
    verdict_vector_sum: str
    verdict_overall: str
    pearson_r_threshold: float


def read_sweep_points(*, csv_path: Path) -> list[SweepPoint]:
    """Read the electrotonic-length table into a flat list of SweepPoint records."""
    assert csv_path.exists(), f"electrotonic-length table CSV must exist: {csv_path}"
    rows: list[SweepPoint] = []
    with csv_path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            rows.append(
                SweepPoint(
                    sweep=raw[OUT_COL_SWEEP],
                    multiplier=float(raw[OUT_COL_MULTIPLIER]),
                    L_over_lambda=float(raw[OUT_COL_L_OVER_LAMBDA]),
                    dsi_primary=float(raw[OUT_COL_DSI_PRIMARY]),
                    dsi_vector_sum=float(raw[OUT_COL_DSI_VECTOR_SUM]),
                    spike_failure_flag=(raw[OUT_COL_SPIKE_FAILURE] == "1"),
                ),
            )
    return rows


def _split_by_sweep(
    *,
    points: list[SweepPoint],
) -> tuple[list[SweepPoint], list[SweepPoint]]:
    """Return ``(length_points, diameter_points)``, both sorted by L/lambda."""
    length_points: list[SweepPoint] = sorted(
        (p for p in points if p.sweep == SWEEP_LENGTH),
        key=lambda p: p.L_over_lambda,
    )
    diameter_points: list[SweepPoint] = sorted(
        (p for p in points if p.sweep == SWEEP_DIAMETER),
        key=lambda p: p.L_over_lambda,
    )
    return (length_points, diameter_points)


def _pearson(*, xs: list[float], ys: list[float]) -> PearsonSummary:
    """Return a PearsonSummary for two paired sequences; n < 2 gives NaN r."""
    assert len(xs) == len(ys), "pearson inputs must have equal length"
    if len(xs) < 2:
        return PearsonSummary(n_points=len(xs), r=float("nan"), p_value=float("nan"))
    # Constant-input edge case (pearsonr undefined): return 0 r, NaN p.
    if max(xs) == min(xs) or max(ys) == min(ys):
        return PearsonSummary(n_points=len(xs), r=float("nan"), p_value=float("nan"))
    result = stats.pearsonr(np.asarray(xs, dtype=np.float64), np.asarray(ys, dtype=np.float64))
    return PearsonSummary(
        n_points=len(xs),
        r=float(result.statistic),
        p_value=float(result.pvalue),
    )


def _interpolate_y_at_x(
    *,
    source_points: list[SweepPoint],
    metric: str,
    target_x: list[float],
) -> list[float]:
    """Linearly interpolate the named metric of ``source_points`` onto ``target_x``.

    target_x values that fall outside the source range are clipped to the range so no
    extrapolation occurs. Any target that cannot be paired (empty source) is excluded by
    the caller.
    """
    assert len(source_points) >= 2, "interpolation needs at least 2 source points"
    xs_src: list[float] = [p.L_over_lambda for p in source_points]
    if metric == "dsi_primary":
        ys_src: list[float] = [p.dsi_primary for p in source_points]
    elif metric == "dsi_vector_sum":
        ys_src = [p.dsi_vector_sum for p in source_points]
    else:
        raise ValueError(f"unknown metric for interpolation: {metric!r}")
    interp: list[float] = list(
        np.interp(
            np.asarray(target_x, dtype=np.float64),
            np.asarray(xs_src, dtype=np.float64),
            np.asarray(ys_src, dtype=np.float64),
        ),
    )
    return interp


def _pair_inside_overlap(
    *,
    length_points: list[SweepPoint],
    diameter_points: list[SweepPoint],
) -> tuple[list[SweepPoint], float, float]:
    """Return the subset of length-sweep points whose L/lambda lies in the diameter-sweep range.

    Pearson r is computed only on points that lie inside the interpolation range of the other
    sweep; otherwise the test would be evaluating at extrapolated (clipped) values.
    """
    d_min: float = min(p.L_over_lambda for p in diameter_points)
    d_max: float = max(p.L_over_lambda for p in diameter_points)
    inside: list[SweepPoint] = [p for p in length_points if d_min <= p.L_over_lambda <= d_max]
    return (inside, d_min, d_max)


def _compute_pearson_summaries(
    *,
    length_points: list[SweepPoint],
    diameter_points: list[SweepPoint],
    metric: str,
) -> tuple[PearsonSummary, PearsonSummary]:
    """Compute Pearson r for paired samples, both including and excluding spike-failure points."""
    paired, _d_min, _d_max = _pair_inside_overlap(
        length_points=length_points,
        diameter_points=diameter_points,
    )
    if len(paired) < 2:
        nan = PearsonSummary(n_points=len(paired), r=float("nan"), p_value=float("nan"))
        return (nan, nan)
    xs_full: list[float] = [
        p.dsi_primary if metric == "dsi_primary" else p.dsi_vector_sum for p in paired
    ]
    target_x: list[float] = [p.L_over_lambda for p in paired]
    ys_full: list[float] = _interpolate_y_at_x(
        source_points=diameter_points,
        metric=metric,
        target_x=target_x,
    )
    full_summary: PearsonSummary = _pearson(xs=xs_full, ys=ys_full)

    paired_no_spike: list[SweepPoint] = [p for p in paired if not p.spike_failure_flag]
    if len(paired_no_spike) < 2:
        no_spike_summary: PearsonSummary = PearsonSummary(
            n_points=len(paired_no_spike),
            r=float("nan"),
            p_value=float("nan"),
        )
        return (full_summary, no_spike_summary)
    xs_no_spike: list[float] = [
        p.dsi_primary if metric == "dsi_primary" else p.dsi_vector_sum for p in paired_no_spike
    ]
    target_x_no_spike: list[float] = [p.L_over_lambda for p in paired_no_spike]
    ys_no_spike: list[float] = _interpolate_y_at_x(
        source_points=diameter_points,
        metric=metric,
        target_x=target_x_no_spike,
    )
    no_spike_summary = _pearson(xs=xs_no_spike, ys=ys_no_spike)
    return (full_summary, no_spike_summary)


def _fit_polynomial(
    *,
    length_points: list[SweepPoint],
    diameter_points: list[SweepPoint],
    metric: str,
) -> PolyFit:
    """Fit a degree-2 polynomial to the pooled dataset and report RMSE pooled + per-sweep."""
    all_points: list[SweepPoint] = length_points + diameter_points
    xs_all: np.ndarray = np.asarray(
        [p.L_over_lambda for p in all_points],
        dtype=np.float64,
    )
    ys_all: np.ndarray = np.asarray(
        [p.dsi_primary if metric == "dsi_primary" else p.dsi_vector_sum for p in all_points],
        dtype=np.float64,
    )
    coeffs: np.ndarray = np.polyfit(xs_all, ys_all, POLYNOMIAL_DEGREE)
    predicted_all: np.ndarray = np.polyval(coeffs, xs_all)
    rmse_pooled: float = float(math.sqrt(float(np.mean((ys_all - predicted_all) ** 2))))

    xs_len: np.ndarray = np.asarray(
        [p.L_over_lambda for p in length_points],
        dtype=np.float64,
    )
    ys_len: np.ndarray = np.asarray(
        [p.dsi_primary if metric == "dsi_primary" else p.dsi_vector_sum for p in length_points],
        dtype=np.float64,
    )
    predicted_len: np.ndarray = np.polyval(coeffs, xs_len)
    rmse_len: float = float(math.sqrt(float(np.mean((ys_len - predicted_len) ** 2))))

    xs_dia: np.ndarray = np.asarray(
        [p.L_over_lambda for p in diameter_points],
        dtype=np.float64,
    )
    ys_dia: np.ndarray = np.asarray(
        [p.dsi_primary if metric == "dsi_primary" else p.dsi_vector_sum for p in diameter_points],
        dtype=np.float64,
    )
    predicted_dia: np.ndarray = np.polyval(coeffs, xs_dia)
    rmse_dia: float = float(math.sqrt(float(np.mean((ys_dia - predicted_dia) ** 2))))

    return PolyFit(
        coefficients_high_to_low=[float(c) for c in coeffs],
        rmse_pooled=rmse_pooled,
        rmse_length_sweep=rmse_len,
        rmse_diameter_sweep=rmse_dia,
    )


def compute_collapse_report(*, points: list[SweepPoint]) -> CollapseReport:
    """Run the full collapse test and return a structured report."""
    length_points, diameter_points = _split_by_sweep(points=points)
    assert len(length_points) >= 2, "need >= 2 length-sweep points for collapse test"
    assert len(diameter_points) >= 2, "need >= 2 diameter-sweep points for collapse test"

    _paired, overlap_min, overlap_max = _pair_inside_overlap(
        length_points=length_points,
        diameter_points=diameter_points,
    )

    pearson_primary_full, pearson_primary_no_spike = _compute_pearson_summaries(
        length_points=length_points,
        diameter_points=diameter_points,
        metric="dsi_primary",
    )
    pearson_vs_full, pearson_vs_no_spike = _compute_pearson_summaries(
        length_points=length_points,
        diameter_points=diameter_points,
        metric="dsi_vector_sum",
    )
    poly_primary: PolyFit = _fit_polynomial(
        length_points=length_points,
        diameter_points=diameter_points,
        metric="dsi_primary",
    )
    poly_vs: PolyFit = _fit_polynomial(
        length_points=length_points,
        diameter_points=diameter_points,
        metric="dsi_vector_sum",
    )

    verdict_primary: str = _verdict_from_r(r=pearson_primary_full.r)
    verdict_vs: str = _verdict_from_r(r=pearson_vs_full.r)
    verdict_overall: str = (
        VERDICT_COLLAPSE_CONFIRMED
        if verdict_primary == VERDICT_COLLAPSE_CONFIRMED
        and verdict_vs == VERDICT_COLLAPSE_CONFIRMED
        else VERDICT_COLLAPSE_REJECTED
    )

    return CollapseReport(
        n_t0034_points=len(length_points),
        n_t0035_points=len(diameter_points),
        l_over_lambda_overlap_min=overlap_min,
        l_over_lambda_overlap_max=overlap_max,
        n_paired_points_full=pearson_primary_full.n_points,
        n_paired_points_no_spike_failure=pearson_primary_no_spike.n_points,
        pearson_primary_full=pearson_primary_full,
        pearson_primary_no_spike_failure=pearson_primary_no_spike,
        pearson_vector_sum_full=pearson_vs_full,
        pearson_vector_sum_no_spike_failure=pearson_vs_no_spike,
        poly_fit_primary=poly_primary,
        poly_fit_vector_sum=poly_vs,
        verdict_primary=verdict_primary,
        verdict_vector_sum=verdict_vs,
        verdict_overall=verdict_overall,
        pearson_r_threshold=PEARSON_R_COLLAPSE_MIN,
    )


def _verdict_from_r(*, r: float) -> str:
    """Return ``collapse_confirmed`` if ``r > threshold``, else ``collapse_rejected``."""
    if math.isnan(r):
        return VERDICT_COLLAPSE_REJECTED
    if r > PEARSON_R_COLLAPSE_MIN:
        return VERDICT_COLLAPSE_CONFIRMED
    return VERDICT_COLLAPSE_REJECTED


def write_collapse_stats_json(*, report: CollapseReport, out_path: Path) -> None:
    """Serialize the full CollapseReport to JSON for archival + downstream aggregator use."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, object] = {
        "spec_version": "1",
        "pearson_r_threshold": report.pearson_r_threshold,
        "n_t0034_points": report.n_t0034_points,
        "n_t0035_points": report.n_t0035_points,
        "l_over_lambda_overlap_min": report.l_over_lambda_overlap_min,
        "l_over_lambda_overlap_max": report.l_over_lambda_overlap_max,
        "n_paired_points_full": report.n_paired_points_full,
        "n_paired_points_no_spike_failure": report.n_paired_points_no_spike_failure,
        "pearson_primary_full": asdict(report.pearson_primary_full),
        "pearson_primary_no_spike_failure": asdict(report.pearson_primary_no_spike_failure),
        "pearson_vector_sum_full": asdict(report.pearson_vector_sum_full),
        "pearson_vector_sum_no_spike_failure": asdict(
            report.pearson_vector_sum_no_spike_failure,
        ),
        "poly_fit_primary": asdict(report.poly_fit_primary),
        "poly_fit_vector_sum": asdict(report.poly_fit_vector_sum),
        "verdict_primary": report.verdict_primary,
        "verdict_vector_sum": report.verdict_vector_sum,
        "verdict_overall": report.verdict_overall,
    }
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_metrics_json(*, points: list[SweepPoint], out_path: Path) -> None:
    """Write metrics.json in the explicit multi-variant format, one variant per operating point.

    Each variant records the registered ``direction_selectivity_index`` metric keyed by sweep +
    multiplier, with L/lambda included in the ``dimensions`` block.
    """
    variants: list[dict[str, object]] = []
    for p in points:
        variant_id: str = f"{p.sweep}_m{p.multiplier:.2f}".replace(".", "p")
        label_prefix: str = "length" if p.sweep == SWEEP_LENGTH else "diameter"
        variants.append(
            {
                "variant_id": variant_id,
                "label": f"t0034/t0035 {label_prefix} x {p.multiplier:.2f}",
                "dimensions": {
                    "sweep": p.sweep,
                    "multiplier": p.multiplier,
                    "l_over_lambda": p.L_over_lambda,
                    "spike_failure_flag": p.spike_failure_flag,
                },
                "metrics": {
                    "direction_selectivity_index": p.dsi_primary,
                },
            },
        )
    payload: dict[str, object] = {"variants": variants}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--table-csv",
        type=str,
        default=None,
        help="override the electrotonic-length table CSV input path",
    )
    return parser.parse_args(argv)


def _format_pearson(*, label: str, summary: PearsonSummary) -> str:
    return f"  {label}: n={summary.n_points} r={summary.r:+.4f} p={summary.p_value:.4g}"


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    table_csv: Path = Path(args.table_csv) if args.table_csv is not None else ELECTROTONIC_TABLE_CSV
    if not table_csv.exists():
        print(
            f"[test_collapse] ERROR: table CSV missing ({table_csv})",
            flush=True,
        )
        return 1
    points: list[SweepPoint] = read_sweep_points(csv_path=table_csv)
    report: CollapseReport = compute_collapse_report(points=points)
    write_collapse_stats_json(report=report, out_path=COLLAPSE_STATS_JSON)
    write_metrics_json(points=points, out_path=METRICS_JSON)

    print(
        f"[test_collapse] verdict_overall = {report.verdict_overall} "
        f"(primary: {report.verdict_primary}, vector_sum: {report.verdict_vector_sum})",
        flush=True,
    )
    print(
        f"[test_collapse] paired samples (overlap "
        f"{report.l_over_lambda_overlap_min:.4f}-{report.l_over_lambda_overlap_max:.4f}):",
        flush=True,
    )
    print(
        _format_pearson(
            label="primary      (with spike-failure)",
            summary=report.pearson_primary_full,
        ),
        flush=True,
    )
    print(
        _format_pearson(
            label="primary      (no  spike-failure)",
            summary=report.pearson_primary_no_spike_failure,
        ),
        flush=True,
    )
    print(
        _format_pearson(
            label="vector_sum   (with spike-failure)",
            summary=report.pearson_vector_sum_full,
        ),
        flush=True,
    )
    print(
        _format_pearson(
            label="vector_sum   (no  spike-failure)",
            summary=report.pearson_vector_sum_no_spike_failure,
        ),
        flush=True,
    )
    print(
        f"[test_collapse] poly2 RMSE (primary):    pooled="
        f"{report.poly_fit_primary.rmse_pooled:.4f} "
        f"length={report.poly_fit_primary.rmse_length_sweep:.4f} "
        f"diameter={report.poly_fit_primary.rmse_diameter_sweep:.4f}",
        flush=True,
    )
    print(
        f"[test_collapse] poly2 RMSE (vector_sum): pooled="
        f"{report.poly_fit_vector_sum.rmse_pooled:.4f} "
        f"length={report.poly_fit_vector_sum.rmse_length_sweep:.4f} "
        f"diameter={report.poly_fit_vector_sum.rmse_diameter_sweep:.4f}",
        flush=True,
    )
    print(f"[test_collapse] wrote {COLLAPSE_STATS_JSON}", flush=True)
    print(f"[test_collapse] wrote {METRICS_JSON}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
