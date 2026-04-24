"""Classify the null-Hz unpinning threshold on the t0037 GABA ladder.

Reads ``results/data/metrics_per_gaba.csv`` and scans the 5 GABA levels from lowest to highest
to find the smallest ``gaba_null_ns`` with mean ``null_hz >= NULL_HZ_UNPINNING_THRESHOLD_HZ``
(0.1 Hz). Emits one of two outcomes:

* **Unpinned** (``label = "unpinned"``): at least one GABA level crosses the threshold. The
  smallest such level is reported as ``unpinning_threshold_ns``. The recommendation suggests a
  follow-up full diameter sweep at that GABA value.
* **All-levels-pinned** (``label = "all_levels_pinned"``): no level crosses the threshold,
  including 0 nS full GABA block. ``unpinning_threshold_ns`` is ``null``. The recommendation
  explicitly states that the AMPA EPSP never reaches AP threshold at null angles on t0022
  independent of GABA, and pivots to S-0030-02 (Poisson noise) or S-0030-06 (vector-sum DSI).

Pre-condition gate (REQ-9): the mean peak_hz at the highest GABA level (4 nS) must be
>= ``PEAK_HZ_MIN_PRECONDITION_HZ`` (10 Hz). If not, the label is suffixed with ``_suspect`` and
``precondition_note`` records the failure. The ladder data is still saved for post-hoc
inspection; this gate does not halt the task.

Writes ``results/data/curve_shape.json`` with every underlying quantity so a human can override
the classification in ``results_detailed.md``.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

from tasks.t0037_null_gaba_reduction_ladder_t0022.code.constants import (
    GABA_LEVELS_NS,
    NULL_HZ_UNPINNING_THRESHOLD_HZ,
    PEAK_HZ_MIN_PRECONDITION_HZ,
)
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.paths import (
    CURVE_SHAPE_JSON,
    METRICS_PER_GABA_CSV,
)

# Comparator pointer for the compare-literature stage (t0036 was the immediate predecessor).
_COMPARATOR_TASK_IDS: tuple[str, ...] = ("t0036",)

# Label constants.
_LABEL_UNPINNED: str = "unpinned"
_LABEL_ALL_PINNED: str = "all_levels_pinned"
_SUSPECT_SUFFIX: str = "_suspect"

# Highest GABA level in the ladder -- anchored to the constants tuple so adding/removing levels
# cannot silently decouple this value from the sweep grid.
_HIGHEST_GABA_NS: float = float(max(GABA_LEVELS_NS))


@dataclass(frozen=True, slots=True)
class MetricsRow:
    """Subset of ``metrics_per_gaba.csv`` needed for classification."""

    gaba_null_ns: float
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
                    gaba_null_ns=float(row["gaba_null_ns"]),
                    dsi_peak_null=float(row["dsi_peak_null"]),
                    dsi_vector_sum=float(row["dsi_vector_sum"]),
                    peak_hz=float(row["peak_hz"]),
                    null_hz=float(row["null_hz"]),
                ),
            )
    rows.sort(key=lambda r: r.gaba_null_ns)
    return rows


def _lookup_at(*, rows: list[MetricsRow], target: float, field: str) -> float:
    for row in rows:
        if math.isclose(row.gaba_null_ns, target, abs_tol=1e-9):
            return float(getattr(row, field))
    return float("nan")


def _find_unpinning_threshold_ns(
    *,
    rows: list[MetricsRow],
    threshold_hz: float,
) -> float | None:
    """Scan rows ascending by ``gaba_null_ns`` and return the smallest level with null_hz >= thr.

    Returns ``None`` if no level crosses the threshold.
    """
    # Rows are already sorted ascending by gaba_null_ns in _read_metrics.
    for row in rows:
        if row.null_hz >= threshold_hz:
            return float(row.gaba_null_ns)
    return None


def _build_recommendation_text(
    *,
    label: str,
    unpinning_threshold_ns: float | None,
) -> str:
    if label == _LABEL_UNPINNED:
        assert unpinning_threshold_ns is not None, "unpinned label requires a threshold value"
        return (
            f"The unpinning threshold is {unpinning_threshold_ns:.2f} nS. A follow-up "
            "full-diameter sweep at this GABA level is warranted to measure the DSI-vs-diameter "
            "slope once null firing is unpinned."
        )
    if label == _LABEL_ALL_PINNED:
        return (
            "No GABA level in {4, 2, 1, 0.5, 0} nS unpins null firing on the t0022 "
            "deterministic schedule. This includes 0 nS (full GABA block), implying the AMPA "
            "EPSP never reaches AP threshold at null angles on t0022 independent of GABA. "
            "Recommend pivot to Poisson-noise rescue (S-0030-02) or vector-sum DSI objective "
            "(S-0030-06). Conductance-axis rescue is exhausted."
        )
    raise ValueError(f"unknown label {label!r}")


def classify_ladder(*, rows: list[MetricsRow]) -> dict[str, object]:
    """Classify the null-Hz ladder and return a JSON-serialisable payload."""
    if len(rows) == 0:
        raise ValueError("classify_ladder called with empty rows list")

    unpinning_threshold_ns: float | None = _find_unpinning_threshold_ns(
        rows=rows,
        threshold_hz=NULL_HZ_UNPINNING_THRESHOLD_HZ,
    )
    base_label: str = _LABEL_UNPINNED if unpinning_threshold_ns is not None else _LABEL_ALL_PINNED

    # Pre-condition gate: peak_hz at the highest GABA level must clear the threshold.
    precondition_peak_hz: float = _lookup_at(
        rows=rows,
        target=_HIGHEST_GABA_NS,
        field="peak_hz",
    )
    precondition_pass: bool = (
        not math.isnan(precondition_peak_hz) and precondition_peak_hz >= PEAK_HZ_MIN_PRECONDITION_HZ
    )
    precondition_note: str | None
    if precondition_pass:
        label: str = base_label
        precondition_note = None
    else:
        label = f"{base_label}{_SUSPECT_SUFFIX}"
        precondition_note = (
            f"Pre-condition FAILED: mean peak_hz at {_HIGHEST_GABA_NS:.1f} nS = "
            f"{precondition_peak_hz:.4f} Hz, below threshold "
            f"{PEAK_HZ_MIN_PRECONDITION_HZ} Hz. Preferred-direction firing is broken at the "
            "highest GABA level in the ladder; the ladder interpretation is SUSPECT. Inspect "
            "the per-GABA polar overlay and the per-trial spike counts before trusting the "
            "unpinning classification."
        )
        print(
            f"[classify_slope] WARNING: pre-condition failed; label -> {label!r}",
            flush=True,
        )

    recommendation_text: str = _build_recommendation_text(
        label=base_label,
        unpinning_threshold_ns=unpinning_threshold_ns,
    )

    null_hz_by_gaba: dict[str, float] = {
        f"{row.gaba_null_ns:.2f}": float(row.null_hz) for row in rows
    }
    primary_dsi_by_gaba: dict[str, float] = {
        f"{row.gaba_null_ns:.2f}": float(row.dsi_peak_null) for row in rows
    }
    peak_hz_by_gaba: dict[str, float] = {
        f"{row.gaba_null_ns:.2f}": float(row.peak_hz) for row in rows
    }
    vector_sum_dsi_by_gaba: dict[str, float] = {
        f"{row.gaba_null_ns:.2f}": float(row.dsi_vector_sum) for row in rows
    }

    out: dict[str, object] = {
        "label": label,
        "base_label": base_label,
        "unpinning_threshold_ns": (
            None if unpinning_threshold_ns is None else float(unpinning_threshold_ns)
        ),
        "unpinning_threshold_hz": float(NULL_HZ_UNPINNING_THRESHOLD_HZ),
        "null_hz_by_gaba": null_hz_by_gaba,
        "primary_dsi_by_gaba": primary_dsi_by_gaba,
        "peak_hz_by_gaba": peak_hz_by_gaba,
        "vector_sum_dsi_by_gaba": vector_sum_dsi_by_gaba,
        "precondition_peak_hz_at_4ns": (
            None if math.isnan(precondition_peak_hz) else float(precondition_peak_hz)
        ),
        "precondition_pass": bool(precondition_pass),
        "precondition_threshold_hz": float(PEAK_HZ_MIN_PRECONDITION_HZ),
        "precondition_note": precondition_note,
        "recommendation_text": recommendation_text,
        "comparator_task_ids": list(_COMPARATOR_TASK_IDS),
    }
    return out


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--metrics",
        type=str,
        default=None,
        help="override per-GABA metrics CSV input path",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    metrics_csv: Path = Path(args.metrics) if args.metrics is not None else METRICS_PER_GABA_CSV
    if not metrics_csv.exists():
        print(f"[classify_slope] ERROR: metrics CSV missing ({metrics_csv})", flush=True)
        return 1

    rows: list[MetricsRow] = _read_metrics(metrics_csv=metrics_csv)
    payload: dict[str, object] = classify_ladder(rows=rows)

    CURVE_SHAPE_JSON.parent.mkdir(parents=True, exist_ok=True)
    CURVE_SHAPE_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"[classify_slope] wrote {CURVE_SHAPE_JSON}", flush=True)
    label: str = str(payload["label"])
    threshold: object = payload["unpinning_threshold_ns"]
    precondition_pass: object = payload["precondition_pass"]
    print(
        f"[classify_slope] label = {label}  unpinning_threshold_ns = {threshold!r}  "
        f"precondition_pass = {precondition_pass!r}",
        flush=True,
    )
    print(f"[classify_slope] recommendation: {payload['recommendation_text']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
