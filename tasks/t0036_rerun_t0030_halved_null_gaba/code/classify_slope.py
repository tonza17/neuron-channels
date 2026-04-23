"""Classify the DSI-vs-diameter slope sign for mechanism discrimination (t0036 halved null-GABA).

Reads ``results/data/metrics_per_diameter.csv``, fits a linear regression of DSI vs
``log2(multiplier)`` (so the curve is symmetric around 1.0x), and classifies the slope sign for
mechanism discrimination:

* ``schachter2010_amplification`` -- positive slope with p < 0.05 and ``dsi_range_extremes``
  >= 0.05 (thicker distal dendrites amplify DSI, consistent with dendritic Nav / Ca substrate
  tipping preferred-direction EPSPs over the dendritic-spike threshold).
* ``passive_filtering`` -- negative slope with p < 0.05 and ``dsi_range_extremes`` <= -0.05
  (thicker distal dendrites damp DSI, consistent with cable-theory low-impedance attenuation).
* ``flat`` -- otherwise (insufficient evidence to discriminate the mechanisms).

**Pre-condition gate (REQ-10)**: before any slope interpretation, the mean null-direction firing
rate at the 1.0x baseline multiplier must be >= ``NULL_HZ_MIN_PRECONDITION_HZ`` (0.1 Hz). If the
gate fails, the mechanism label is suffixed with ``_partial`` (e.g. ``flat_partial``) and a
recommendation is written to ``precondition_note``. The null-Hz pre-condition is the informative
readout that confirms the 6 nS GABA reduction unpinned null firing at all.

**REQ-12 fallback** (inherited from t0030): if the primary DSI saturates
(``max - min <= DSI_SATURATION_THRESHOLD``), re-fit the regression on vector-sum DSI and use that
for the slope-sign decision.

Writes ``results/data/curve_shape.json`` and ``results/data/slope_classification.json`` with every
underlying quantity so a human can override the classification in ``results_detailed.md``.
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

from tasks.t0036_rerun_t0030_halved_null_gaba.code.constants import (
    BASELINE_MULTIPLIER,
    DSI_RANGE_MIN_FOR_CONFIDENT_LABEL,
    DSI_SATURATION_THRESHOLD,
    GABA_CONDUCTANCE_NULL_NS_OVERRIDE,
    MAX_P_VALUE,
    MECHANISM_FLAT,
    MECHANISM_PASSIVE,
    MECHANISM_SCHACHTER2010,
    MIN_SLOPE_MAGNITUDE,
    NULL_HZ_MIN_PRECONDITION_HZ,
    SLOPE_SIGN_FLAT,
    SLOPE_SIGN_NEGATIVE,
    SLOPE_SIGN_POSITIVE,
)
from tasks.t0036_rerun_t0030_halved_null_gaba.code.paths import (
    CURVE_SHAPE_JSON,
    METRICS_PER_DIAMETER_CSV,
    SLOPE_CLASSIFICATION_JSON,
)

# Comparator pointers for the compare-literature stage (Key Question 4).
_COMPARATOR_TASK_IDS: tuple[str, ...] = ("t0030", "t0035")

_PARTIAL_LABEL_SUFFIX: str = "_partial"


@dataclass(frozen=True, slots=True)
class RegressionSummary:
    """Linear regression summary with slope CI and p-value."""

    slope: float
    intercept: float
    r_squared: float
    p_value: float
    slope_95_ci_low: float
    slope_95_ci_high: float


@dataclass(frozen=True, slots=True)
class MetricsRow:
    """Subset of metrics_per_diameter.csv needed for classification."""

    diameter_multiplier: float
    dsi_peak_null: float
    dsi_vector_sum: float
    peak_hz: float
    null_hz: float


def _read_metrics(*, metrics_csv: Path) -> list[MetricsRow]:
    rows: list[MetricsRow] = []
    with metrics_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(
                MetricsRow(
                    diameter_multiplier=float(row["diameter_multiplier"]),
                    dsi_peak_null=float(row["dsi_peak_null"]),
                    dsi_vector_sum=float(row["dsi_vector_sum"]),
                    peak_hz=float(row["peak_hz"]),
                    null_hz=float(row["null_hz"]),
                ),
            )
    rows.sort(key=lambda r: r.diameter_multiplier)
    return rows


def _linear_regression(*, xs: list[float], ys: list[float]) -> RegressionSummary:
    """Run linear regression and return slope, intercept, r^2, p-value, and slope 95% CI."""
    xs_arr: np.ndarray = np.asarray(xs, dtype=np.float64)
    ys_arr: np.ndarray = np.asarray(ys, dtype=np.float64)
    result = stats.linregress(xs_arr, ys_arr)
    slope: float = float(result.slope)
    intercept: float = float(result.intercept)
    r_value: float = float(result.rvalue)
    p_value: float = float(result.pvalue)
    stderr: float = float(result.stderr)
    n: int = len(xs)
    dof: int = max(n - 2, 1)
    t_crit: float = float(stats.t.ppf(1.0 - 0.025, dof))
    ci_half: float = t_crit * stderr
    return RegressionSummary(
        slope=slope,
        intercept=intercept,
        r_squared=r_value * r_value,
        p_value=p_value,
        slope_95_ci_low=slope - ci_half,
        slope_95_ci_high=slope + ci_half,
    )


def _lookup_at(*, rows: list[MetricsRow], target: float, field: str) -> float:
    for row in rows:
        if math.isclose(row.diameter_multiplier, target, abs_tol=1e-9):
            return float(getattr(row, field))
    return float("nan")


def _slope_sign(*, slope: float, magnitude_threshold: float) -> str:
    if slope >= magnitude_threshold:
        return SLOPE_SIGN_POSITIVE
    if slope <= -magnitude_threshold:
        return SLOPE_SIGN_NEGATIVE
    return SLOPE_SIGN_FLAT


def _mechanism_label(
    *,
    slope: float,
    p_value: float,
    dsi_range_extremes: float,
) -> str:
    if (
        slope > 0
        and p_value < MAX_P_VALUE
        and dsi_range_extremes >= DSI_RANGE_MIN_FOR_CONFIDENT_LABEL
    ):
        return MECHANISM_SCHACHTER2010
    if (
        slope < 0
        and p_value < MAX_P_VALUE
        and dsi_range_extremes <= -DSI_RANGE_MIN_FOR_CONFIDENT_LABEL
    ):
        return MECHANISM_PASSIVE
    return MECHANISM_FLAT


def classify_slope(*, rows: list[MetricsRow]) -> dict[str, object]:
    """Classify the DSI-vs-diameter slope sign and return a JSON-serialisable payload."""
    if len(rows) == 0:
        raise ValueError("classify_slope called with empty rows list")

    multipliers: list[float] = [r.diameter_multiplier for r in rows]
    log2_x: list[float] = [math.log2(m) for m in multipliers]
    dsi_primary: list[float] = [r.dsi_peak_null for r in rows]
    dsi_vs: list[float] = [r.dsi_vector_sum for r in rows]
    peak_hz: list[float] = [r.peak_hz for r in rows]
    null_hz: list[float] = [r.null_hz for r in rows]

    primary_regression: RegressionSummary = _linear_regression(xs=log2_x, ys=dsi_primary)
    vs_regression: RegressionSummary = _linear_regression(xs=log2_x, ys=dsi_vs)
    peak_regression: RegressionSummary = _linear_regression(xs=log2_x, ys=peak_hz)
    null_regression: RegressionSummary = _linear_regression(xs=log2_x, ys=null_hz)

    dsi_at_0p5: float = _lookup_at(rows=rows, target=0.5, field="dsi_peak_null")
    dsi_at_2p0: float = _lookup_at(rows=rows, target=2.0, field="dsi_peak_null")
    dsi_range_extremes_primary: float = dsi_at_2p0 - dsi_at_0p5

    dsi_vs_at_0p5: float = _lookup_at(rows=rows, target=0.5, field="dsi_vector_sum")
    dsi_vs_at_2p0: float = _lookup_at(rows=rows, target=2.0, field="dsi_vector_sum")
    dsi_range_extremes_vs: float = dsi_vs_at_2p0 - dsi_vs_at_0p5

    # REQ-12 fallback: if primary DSI saturates, use vector-sum DSI for slope decision.
    primary_range: float = max(dsi_primary) - min(dsi_primary)
    used_fallback: bool = primary_range <= DSI_SATURATION_THRESHOLD

    if used_fallback:
        active_regression: RegressionSummary = vs_regression
        active_range_extremes: float = dsi_range_extremes_vs
    else:
        active_regression = primary_regression
        active_range_extremes = dsi_range_extremes_primary

    slope_sign: str = _slope_sign(
        slope=active_regression.slope,
        magnitude_threshold=MIN_SLOPE_MAGNITUDE,
    )
    base_mechanism_label: str = _mechanism_label(
        slope=active_regression.slope,
        p_value=active_regression.p_value,
        dsi_range_extremes=active_range_extremes,
    )

    preferred_and_null_both_drop: bool | None = None
    if base_mechanism_label == MECHANISM_PASSIVE:
        preferred_and_null_both_drop = peak_regression.slope < 0.0 and null_regression.slope <= 0.0

    # Pre-condition gate (REQ-10): mean null-Hz at 1.0x baseline must clear the threshold.
    precondition_null_hz_at_baseline: float = _lookup_at(
        rows=rows,
        target=BASELINE_MULTIPLIER,
        field="null_hz",
    )
    precondition_pass: bool = (
        not math.isnan(precondition_null_hz_at_baseline)
        and precondition_null_hz_at_baseline >= NULL_HZ_MIN_PRECONDITION_HZ
    )
    precondition_note: str | None
    if precondition_pass:
        mechanism_label: str = base_mechanism_label
        precondition_note = None
    else:
        mechanism_label = f"{base_mechanism_label}{_PARTIAL_LABEL_SUFFIX}"
        precondition_note = (
            f"Null-Hz pre-condition FAILED: mean null firing at 1.0x baseline = "
            f"{precondition_null_hz_at_baseline:.4f} Hz, below threshold "
            f"{NULL_HZ_MIN_PRECONDITION_HZ} Hz. DSI slope interpretation is PARTIAL: primary "
            "DSI is still effectively pinned at the null-zero corner. Recommend a further "
            "reduction of GABA_CONDUCTANCE_NULL_NS (currently "
            f"{GABA_CONDUCTANCE_NULL_NS_OVERRIDE} nS), e.g. to 4 nS."
        )
        print(
            f"[classify_slope] WARNING: pre-condition failed; label -> {mechanism_label!r}",
            flush=True,
        )

    qualitative_description: str
    if base_mechanism_label == MECHANISM_SCHACHTER2010:
        qualitative_description = (
            f"DSI increases with distal diameter (slope={active_regression.slope:.4f} per "
            f"log2(multiplier), p={active_regression.p_value:.4g}); consistent with "
            "Schachter2010 active-dendrite amplification."
        )
    elif base_mechanism_label == MECHANISM_PASSIVE:
        qualitative_description = (
            f"DSI decreases with distal diameter (slope={active_regression.slope:.4f} per "
            f"log2(multiplier), p={active_regression.p_value:.4g}); consistent with passive "
            "cable filtering."
        )
    else:
        qualitative_description = (
            f"DSI vs diameter slope is not distinguishable from zero "
            f"(slope={active_regression.slope:.4f} per log2(multiplier), "
            f"p={active_regression.p_value:.4g}, "
            f"dsi_range_extremes={active_range_extremes:.4f}); "
            "neither Schachter2010 nor passive filtering is supported."
        )
    if not precondition_pass:
        qualitative_description = f"{qualitative_description} [PARTIAL: {precondition_note}]"

    out: dict[str, object] = {
        "slope": float(active_regression.slope),
        "slope_95_ci_low": float(active_regression.slope_95_ci_low),
        "slope_95_ci_high": float(active_regression.slope_95_ci_high),
        "slope_p_value": float(active_regression.p_value),
        "slope_r_squared": float(active_regression.r_squared),
        "slope_sign": slope_sign,
        "dsi_range_extremes": float(active_range_extremes),
        "dsi_range_extremes_primary": float(dsi_range_extremes_primary),
        "dsi_range_extremes_vector_sum": float(dsi_range_extremes_vs),
        "primary_regression": {
            "slope": float(primary_regression.slope),
            "intercept": float(primary_regression.intercept),
            "r_squared": float(primary_regression.r_squared),
            "p_value": float(primary_regression.p_value),
            "slope_95_ci_low": float(primary_regression.slope_95_ci_low),
            "slope_95_ci_high": float(primary_regression.slope_95_ci_high),
        },
        "vector_sum_regression": {
            "slope": float(vs_regression.slope),
            "intercept": float(vs_regression.intercept),
            "r_squared": float(vs_regression.r_squared),
            "p_value": float(vs_regression.p_value),
            "slope_95_ci_low": float(vs_regression.slope_95_ci_low),
            "slope_95_ci_high": float(vs_regression.slope_95_ci_high),
        },
        "peak_hz_trend_slope": float(peak_regression.slope),
        "peak_hz_trend_p_value": float(peak_regression.p_value),
        "null_hz_trend_slope": float(null_regression.slope),
        "null_hz_trend_p_value": float(null_regression.p_value),
        "preferred_and_null_both_drop": preferred_and_null_both_drop,
        "used_fallback_vector_sum_dsi": bool(used_fallback),
        "dsi_primary_range": float(primary_range),
        "dsi_saturation_threshold": float(DSI_SATURATION_THRESHOLD),
        "base_mechanism_label": base_mechanism_label,
        "mechanism_label": mechanism_label,
        "qualitative_description": qualitative_description,
        "precondition_null_hz_at_baseline": (
            None
            if math.isnan(precondition_null_hz_at_baseline)
            else float(precondition_null_hz_at_baseline)
        ),
        "precondition_pass": bool(precondition_pass),
        "precondition_threshold_hz": float(NULL_HZ_MIN_PRECONDITION_HZ),
        "precondition_note": precondition_note,
        "gaba_conductance_null_ns_effective": float(GABA_CONDUCTANCE_NULL_NS_OVERRIDE),
        "comparator_task_ids": list(_COMPARATOR_TASK_IDS),
    }
    return out


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--metrics",
        type=str,
        default=None,
        help="override per-diameter metrics CSV input path",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    metrics_csv: Path = Path(args.metrics) if args.metrics is not None else METRICS_PER_DIAMETER_CSV
    if not metrics_csv.exists():
        print(f"[classify_slope] ERROR: metrics CSV missing ({metrics_csv})", flush=True)
        return 1

    rows: list[MetricsRow] = _read_metrics(metrics_csv=metrics_csv)
    payload: dict[str, object] = classify_slope(rows=rows)

    CURVE_SHAPE_JSON.parent.mkdir(parents=True, exist_ok=True)
    CURVE_SHAPE_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    SLOPE_CLASSIFICATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    SLOPE_CLASSIFICATION_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"[classify_slope] wrote {CURVE_SHAPE_JSON}", flush=True)
    print(f"[classify_slope] wrote {SLOPE_CLASSIFICATION_JSON}", flush=True)
    slope_val: float = float(payload["slope"])  # type: ignore[arg-type]
    p_val: float = float(payload["slope_p_value"])  # type: ignore[arg-type]
    range_val: float = float(payload["dsi_range_extremes"])  # type: ignore[arg-type]
    print(
        f"[classify_slope] mechanism_label = {payload['mechanism_label']}  "
        f"slope = {slope_val:.4f}  p = {p_val:.4g}  "
        f"dsi_range_extremes = {range_val:.4f}  "
        f"used_fallback = {payload['used_fallback_vector_sum_dsi']}  "
        f"precondition_pass = {payload['precondition_pass']}",
        flush=True,
    )
    print(
        f"[classify_slope] {payload['qualitative_description']}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
