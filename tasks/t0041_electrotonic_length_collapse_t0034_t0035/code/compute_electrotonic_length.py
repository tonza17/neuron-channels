"""Compute section-mean electrotonic length L/lambda for t0034 and t0035 operating points.

For every (length multiplier, diameter multiplier) operating point in the combined t0034 union
t0035 dataset, this script:

1. Reads the upstream per-multiplier metrics CSVs (DSI and firing rates already computed).
2. Computes effective distal-section length ``L`` and diameter ``d`` from the baseline section-
   mean values and the per-sweep multiplier.
3. Computes ``lambda = sqrt(d * Rm / (4 * Ra))`` with explicit micrometre-to-centimetre unit
   conversion.
4. Writes ``results/electrotonic_length_table.csv`` with one row per operating point, labelled by
   sweep (``length`` or ``diameter``), along with the original DSI / peak / null values copied
   over from the upstream CSV.

Cable-theory formula (REQ-1): ``lambda = sqrt(d * Rm / (4 * Ra))`` with ``d`` in cm,
``Rm`` in ohm.cm^2, and ``Ra`` in ohm.cm, so ``lambda`` is in cm; ``L/lambda`` is dimensionless.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import dataclass
from pathlib import Path

from tasks.t0041_electrotonic_length_collapse_t0034_t0035.code.constants import (
    BASELINE_DISTAL_DIAM_UM,
    BASELINE_DISTAL_LENGTH_UM,
    OUT_COL_DSI_PRIMARY,
    OUT_COL_DSI_VECTOR_SUM,
    OUT_COL_EFFECTIVE_D_UM,
    OUT_COL_EFFECTIVE_L_UM,
    OUT_COL_L_OVER_LAMBDA,
    OUT_COL_LAMBDA_UM,
    OUT_COL_MULTIPLIER,
    OUT_COL_NULL_HZ,
    OUT_COL_PEAK_HZ,
    OUT_COL_SPIKE_FAILURE,
    OUT_COL_SWEEP,
    OUTPUT_CSV_HEADER,
    RA_OHM_CM,
    RM_OHM_CM2,
    SWEEP_DIAMETER,
    SWEEP_LENGTH,
    T0034_MULTIPLIER_COLUMN,
    T0034_SPIKE_FAILURE_MULTIPLIERS,
    T0035_MULTIPLIER_COLUMN,
    UM_PER_CM,
)
from tasks.t0041_electrotonic_length_collapse_t0034_t0035.code.metrics_csv_reader import (
    MetricsRow,
    read_metrics_csv,
)
from tasks.t0041_electrotonic_length_collapse_t0034_t0035.code.paths import (
    ELECTROTONIC_TABLE_CSV,
    T0034_METRICS_PER_LENGTH_CSV,
    T0035_METRICS_PER_DIAMETER_CSV,
)


@dataclass(frozen=True, slots=True)
class ElectrotonicRow:
    """Per-operating-point electrotonic-length record for the combined dataset."""

    sweep: str
    multiplier: float
    effective_L_um: float
    effective_d_um: float
    lambda_um: float
    L_over_lambda: float
    dsi_primary: float
    dsi_vector_sum: float
    peak_hz: float
    null_hz: float
    spike_failure_flag: bool


def compute_lambda_um(*, diameter_um: float) -> float:
    """Return electrotonic space constant ``lambda`` in micrometres.

    Formula: ``lambda = sqrt(d * Rm / (4 * Ra))`` with ``d`` in cm, ``Rm`` in ohm.cm^2,
    ``Ra`` in ohm.cm; result is converted back to micrometres.
    """
    assert diameter_um > 0.0, "diameter must be strictly positive"
    diameter_cm: float = diameter_um / UM_PER_CM
    lambda_cm: float = math.sqrt(diameter_cm * RM_OHM_CM2 / (4.0 * RA_OHM_CM))
    return lambda_cm * UM_PER_CM


def _to_electrotonic_row(
    *,
    sweep: str,
    metrics_row: MetricsRow,
) -> ElectrotonicRow:
    """Convert one upstream MetricsRow to an ElectrotonicRow with L/lambda computed."""
    if sweep == SWEEP_LENGTH:
        effective_L_um: float = BASELINE_DISTAL_LENGTH_UM * metrics_row.multiplier
        effective_d_um: float = BASELINE_DISTAL_DIAM_UM
        spike_failure: bool = metrics_row.multiplier in T0034_SPIKE_FAILURE_MULTIPLIERS
    elif sweep == SWEEP_DIAMETER:
        effective_L_um = BASELINE_DISTAL_LENGTH_UM
        effective_d_um = BASELINE_DISTAL_DIAM_UM * metrics_row.multiplier
        spike_failure = False
    else:
        raise ValueError(f"unknown sweep label: {sweep!r}")
    lambda_um: float = compute_lambda_um(diameter_um=effective_d_um)
    L_over_lambda: float = effective_L_um / lambda_um
    return ElectrotonicRow(
        sweep=sweep,
        multiplier=metrics_row.multiplier,
        effective_L_um=effective_L_um,
        effective_d_um=effective_d_um,
        lambda_um=lambda_um,
        L_over_lambda=L_over_lambda,
        dsi_primary=metrics_row.dsi_primary,
        dsi_vector_sum=metrics_row.dsi_vector_sum,
        peak_hz=metrics_row.peak_hz,
        null_hz=metrics_row.null_hz,
        spike_failure_flag=spike_failure,
    )


def build_electrotonic_table(
    *,
    t0034_metrics_csv: Path,
    t0035_metrics_csv: Path,
) -> list[ElectrotonicRow]:
    """Read both upstream CSVs and return the combined electrotonic-length table."""
    length_rows: list[MetricsRow] = read_metrics_csv(
        metrics_csv=t0034_metrics_csv,
        multiplier_column=T0034_MULTIPLIER_COLUMN,
    )
    diameter_rows: list[MetricsRow] = read_metrics_csv(
        metrics_csv=t0035_metrics_csv,
        multiplier_column=T0035_MULTIPLIER_COLUMN,
    )
    assert len(length_rows) > 0, "t0034 metrics CSV must contain at least one row"
    assert len(diameter_rows) > 0, "t0035 metrics CSV must contain at least one row"
    combined: list[ElectrotonicRow] = []
    for row in length_rows:
        combined.append(_to_electrotonic_row(sweep=SWEEP_LENGTH, metrics_row=row))
    for row in diameter_rows:
        combined.append(_to_electrotonic_row(sweep=SWEEP_DIAMETER, metrics_row=row))
    return combined


def write_electrotonic_table_csv(
    *,
    rows: list[ElectrotonicRow],
    out_path: Path,
) -> None:
    """Write the combined electrotonic-length table as CSV."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(list(OUTPUT_CSV_HEADER))
        for row in rows:
            writer.writerow(
                [
                    row.sweep,
                    f"{row.multiplier:.2f}",
                    f"{row.effective_L_um:.6f}",
                    f"{row.effective_d_um:.6f}",
                    f"{row.lambda_um:.6f}",
                    f"{row.L_over_lambda:.6f}",
                    f"{row.dsi_primary:.6f}",
                    f"{row.dsi_vector_sum:.6f}",
                    f"{row.peak_hz:.4f}",
                    f"{row.null_hz:.4f}",
                    "1" if row.spike_failure_flag else "0",
                ],
            )
    _ = (
        OUT_COL_SWEEP,
        OUT_COL_MULTIPLIER,
        OUT_COL_EFFECTIVE_L_UM,
        OUT_COL_EFFECTIVE_D_UM,
        OUT_COL_LAMBDA_UM,
        OUT_COL_L_OVER_LAMBDA,
        OUT_COL_DSI_PRIMARY,
        OUT_COL_DSI_VECTOR_SUM,
        OUT_COL_PEAK_HZ,
        OUT_COL_NULL_HZ,
        OUT_COL_SPIKE_FAILURE,
    )


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--t0034-csv",
        type=str,
        default=None,
        help="override the t0034 per-length metrics CSV path",
    )
    parser.add_argument(
        "--t0035-csv",
        type=str,
        default=None,
        help="override the t0035 per-diameter metrics CSV path",
    )
    parser.add_argument(
        "--out-csv",
        type=str,
        default=None,
        help="override the output electrotonic-length CSV path",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    t0034_csv: Path = (
        Path(args.t0034_csv) if args.t0034_csv is not None else T0034_METRICS_PER_LENGTH_CSV
    )
    t0035_csv: Path = (
        Path(args.t0035_csv) if args.t0035_csv is not None else T0035_METRICS_PER_DIAMETER_CSV
    )
    out_csv: Path = Path(args.out_csv) if args.out_csv is not None else ELECTROTONIC_TABLE_CSV

    if not t0034_csv.exists():
        print(
            f"[compute_electrotonic_length] ERROR: t0034 metrics CSV missing ({t0034_csv})",
            flush=True,
        )
        return 1
    if not t0035_csv.exists():
        print(
            f"[compute_electrotonic_length] ERROR: t0035 metrics CSV missing ({t0035_csv})",
            flush=True,
        )
        return 1

    rows: list[ElectrotonicRow] = build_electrotonic_table(
        t0034_metrics_csv=t0034_csv,
        t0035_metrics_csv=t0035_csv,
    )
    write_electrotonic_table_csv(rows=rows, out_path=out_csv)
    print(
        f"[compute_electrotonic_length] wrote {len(rows)} rows -> {out_csv}",
        flush=True,
    )

    # Quick-look preview for step-log traceability.
    for row in rows:
        print(
            f"  sweep={row.sweep:9s} m={row.multiplier:.2f} "
            f"L={row.effective_L_um:7.3f} d={row.effective_d_um:6.4f} "
            f"lambda={row.lambda_um:7.3f} L/lambda={row.L_over_lambda:.4f} "
            f"dsi_primary={row.dsi_primary:.4f} dsi_vs={row.dsi_vector_sum:.4f}"
            f" spike_fail={int(row.spike_failure_flag)}",
            flush=True,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
