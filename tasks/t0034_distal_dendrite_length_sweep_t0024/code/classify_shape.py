"""Classify the DSI-vs-length curve shape for both primary and vector-sum DSI.

Reads ``results/data/metrics_per_length.csv`` and runs a linear regression of DSI vs multiplier.
Classifies the curve as:

* ``monotonic``: non-decreasing AND slope >= ``MONOTONIC_SLOPE_MIN_PER_UNIT`` AND p < 0.05.
* ``saturating``: ``saturation_multiplier <= SATURATION_MULTIPLIER_MAX`` AND
  ``max(dsi) - dsi(m >= m*) <= SATURATION_MAX_DELTA_DSI``.
* ``non_monotonic`` otherwise.

Writes ``results/data/curve_shape.json`` with the primary-DSI classification plus a secondary
vector-sum-DSI classification (``shape_class_vector_sum``, REQ-9 defensive fallback).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy import stats  # type: ignore[import-untyped]

from tasks.t0034_distal_dendrite_length_sweep_t0024.code.constants import (
    MONOTONIC_P_MAX,
    MONOTONIC_SLOPE_MIN_PER_UNIT,
    NON_DECREASING_TOLERANCE,
    SATURATION_FRACTION_OF_MAX,
    SATURATION_MAX_DELTA_DSI,
    SATURATION_MULTIPLIER_MAX,
    SHAPE_MONOTONIC,
    SHAPE_NON_MONOTONIC,
    SHAPE_SATURATING,
)
from tasks.t0034_distal_dendrite_length_sweep_t0024.code.paths import (
    CURVE_SHAPE_JSON,
    METRICS_PER_LENGTH_CSV,
)


@dataclass(frozen=True, slots=True)
class RegressionSummary:
    """Linear regression summary for DSI vs multiplier."""

    slope: float
    intercept: float
    r_squared: float
    p_value: float


def _read_metrics(
    *,
    metrics_csv: Path,
) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    """Return ``(primary_records, vector_sum_records)`` sorted by multiplier.

    Primary records are ``(length_multiplier, dsi_primary)`` tuples; vector-sum records are
    ``(length_multiplier, dsi_vector_sum)`` tuples.
    """
    primary: list[tuple[float, float]] = []
    vector_sum: list[tuple[float, float]] = []
    with metrics_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            mul: float = float(row["length_multiplier"])
            primary.append((mul, float(row["dsi_primary"])))
            vector_sum.append((mul, float(row["dsi_vector_sum"])))
    primary.sort(key=lambda r: r[0])
    vector_sum.sort(key=lambda r: r[0])
    return (primary, vector_sum)


def _linear_regression(*, xs: list[float], ys: list[float]) -> RegressionSummary:
    """Run linear regression of ys on xs via scipy.stats.linregress."""
    xs_arr: np.ndarray = np.asarray(xs, dtype=np.float64)
    ys_arr: np.ndarray = np.asarray(ys, dtype=np.float64)
    result = stats.linregress(xs_arr, ys_arr)
    slope: float = float(result.slope)
    intercept: float = float(result.intercept)
    r_value: float = float(result.rvalue)
    p_value: float = float(result.pvalue)
    return RegressionSummary(
        slope=slope,
        intercept=intercept,
        r_squared=r_value * r_value,
        p_value=p_value,
    )


def _is_non_decreasing(*, ys: list[float], tol: float = NON_DECREASING_TOLERANCE) -> bool:
    return all(curr + tol >= prev for prev, curr in zip(ys[:-1], ys[1:], strict=True))


def _find_saturation_multiplier(*, xs: list[float], ys: list[float]) -> float | None:
    """Return smallest ``m`` such that ``ys[i] >= fraction * max(ys)`` for every i with xs[i]>=m.

    Returns ``None`` if no such ``m`` exists.
    """
    if len(ys) == 0:
        return None
    peak: float = max(ys)
    if peak <= 0.0:
        return None
    threshold: float = SATURATION_FRACTION_OF_MAX * peak
    n: int = len(xs)
    first_saturated: int = n  # sentinel: no saturated tail
    for i in range(n - 1, -1, -1):
        if ys[i] + NON_DECREASING_TOLERANCE >= threshold:
            first_saturated = i
        else:
            break
    if first_saturated >= n:
        return None
    return float(xs[first_saturated])


def _lookup_dsi_at(*, xs: list[float], ys: list[float], target: float) -> float:
    for x, y in zip(xs, ys, strict=True):
        if math.isclose(x, target, abs_tol=1e-9):
            return y
    return float("nan")


def classify_shape(*, records: list[tuple[float, float]]) -> dict[str, object]:
    """Classify a DSI-vs-length curve and return a JSON-serialisable dict."""
    if len(records) == 0:
        raise ValueError("classify_shape called with empty records list")

    xs: list[float] = [r[0] for r in records]
    ys: list[float] = [r[1] for r in records]

    regression: RegressionSummary = _linear_regression(xs=xs, ys=ys)
    non_decreasing: bool = _is_non_decreasing(ys=ys)
    saturation_multiplier: float | None = _find_saturation_multiplier(xs=xs, ys=ys)

    plateau_dsi: float | None = None
    shape_class: str
    qualitative_description: str
    dsi_range: float = max(ys) - min(ys)

    if (
        saturation_multiplier is not None
        and saturation_multiplier <= SATURATION_MULTIPLIER_MAX
        and (max(ys) - min(ys[xs.index(saturation_multiplier) :])) <= SATURATION_MAX_DELTA_DSI
    ):
        shape_class = SHAPE_SATURATING
        tail_start: int = xs.index(saturation_multiplier)
        plateau_dsi = float(sum(ys[tail_start:]) / len(ys[tail_start:]))
        qualitative_description = (
            f"DSI saturates at multiplier {saturation_multiplier:.2f} and remains within "
            f"{SATURATION_MAX_DELTA_DSI:.3f} of its maximum for all larger multipliers. "
            f"Plateau DSI = {plateau_dsi:.4f}. DSI range across the sweep = {dsi_range:.4f}."
        )
    elif (
        non_decreasing
        and regression.slope >= MONOTONIC_SLOPE_MIN_PER_UNIT
        and regression.p_value < MONOTONIC_P_MAX
    ):
        shape_class = SHAPE_MONOTONIC
        qualitative_description = (
            f"DSI is non-decreasing with slope {regression.slope:.4f} per unit multiplier "
            f"(p = {regression.p_value:.4g}, r^2 = {regression.r_squared:.3f})."
        )
    else:
        shape_class = SHAPE_NON_MONOTONIC
        qualitative_description = (
            f"DSI is neither monotonically increasing nor saturating within the sweep. "
            f"Regression slope = {regression.slope:.4f} per unit multiplier "
            f"(p = {regression.p_value:.4g}). DSI range = {dsi_range:.4f}. "
            f"Non-decreasing check: {non_decreasing}."
        )

    dsi_at_half: float = _lookup_dsi_at(xs=xs, ys=ys, target=0.5)
    dsi_at_two: float = _lookup_dsi_at(xs=xs, ys=ys, target=2.0)
    dsi_range_extremes: float = dsi_at_two - dsi_at_half

    return {
        "shape_class": shape_class,
        "slope": float(regression.slope),
        "intercept": float(regression.intercept),
        "r_squared": float(regression.r_squared),
        "p_value": float(regression.p_value),
        "non_decreasing": bool(non_decreasing),
        "saturation_multiplier": (
            float(saturation_multiplier) if saturation_multiplier is not None else None
        ),
        "plateau_dsi": plateau_dsi,
        "dsi_at_0.5": float(dsi_at_half),
        "dsi_at_2.0": float(dsi_at_two),
        "dsi_range_extremes": float(dsi_range_extremes),
        "dsi_min": float(min(ys)),
        "dsi_max": float(max(ys)),
        "qualitative_description": qualitative_description,
    }


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--metrics",
        type=str,
        default=None,
        help="override per-length metrics CSV input path",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    metrics_csv: Path = Path(args.metrics) if args.metrics is not None else METRICS_PER_LENGTH_CSV
    if not metrics_csv.exists():
        print(f"[classify_shape] ERROR: metrics CSV missing ({metrics_csv})", flush=True)
        return 1

    primary_records, vector_sum_records = _read_metrics(metrics_csv=metrics_csv)
    primary_payload: dict[str, object] = classify_shape(records=primary_records)
    vector_sum_payload: dict[str, object] = classify_shape(records=vector_sum_records)

    # Combined payload: primary fields at top level, vector-sum as nested / prefixed fields.
    combined: dict[str, object] = dict(primary_payload)
    combined["shape_class_vector_sum"] = vector_sum_payload["shape_class"]
    combined["vector_sum_details"] = vector_sum_payload

    CURVE_SHAPE_JSON.parent.mkdir(parents=True, exist_ok=True)
    CURVE_SHAPE_JSON.write_text(json.dumps(combined, indent=2) + "\n", encoding="utf-8")
    print(f"[classify_shape] wrote {CURVE_SHAPE_JSON}", flush=True)
    slope_val: float = float(primary_payload["slope"])  # type: ignore[arg-type]
    p_val: float = float(primary_payload["p_value"])  # type: ignore[arg-type]
    range_val: float = float(primary_payload["dsi_range_extremes"])  # type: ignore[arg-type]
    print(
        f"[classify_shape] shape_class = {primary_payload['shape_class']}  "
        f"vector_sum = {vector_sum_payload['shape_class']}  "
        f"slope = {slope_val:.4f}  p = {p_val:.4g}  "
        f"dsi_range_extremes = {range_val:.4f}",
        flush=True,
    )
    print(
        f"[classify_shape] {primary_payload['qualitative_description']}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
