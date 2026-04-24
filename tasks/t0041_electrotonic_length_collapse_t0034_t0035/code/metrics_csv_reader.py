# Copied and adapted from tasks/t0034_distal_dendrite_length_sweep_t0024/code/plot_sweep.py
# lines 56-85 (MetricsRow dataclass + ``_read_metrics_csv``) per the cross-task import rule.
# Generalised to accept an arbitrary multiplier-column name so one reader handles both
# metrics_per_length.csv (column ``length_multiplier``) and metrics_per_diameter.csv (column
# ``diameter_multiplier``).
"""Reader for the per-multiplier metrics CSVs emitted by t0034 and t0035.

The upstream CSV schemas differ only in the name of the first column (`length_multiplier` in
t0034 vs `diameter_multiplier` in t0035); the remaining 9 columns are identical. This module
exposes a single dataclass ``MetricsRow`` and a ``read_metrics_csv`` function that takes the
multiplier-column name as a keyword argument, so the same parser handles both sweeps.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from tasks.t0041_electrotonic_length_collapse_t0034_t0035.code.constants import (
    DSI_PRIMARY_COLUMN,
    DSI_VECTOR_SUM_COLUMN,
    NULL_HZ_COLUMN,
    PEAK_HZ_COLUMN,
)


@dataclass(frozen=True, slots=True)
class MetricsRow:
    """One row of a per-multiplier metrics CSV."""

    multiplier: float
    peak_hz: float
    null_hz: float
    dsi_primary: float
    dsi_vector_sum: float


def read_metrics_csv(*, metrics_csv: Path, multiplier_column: str) -> list[MetricsRow]:
    """Read a per-multiplier metrics CSV sorted by multiplier."""
    assert metrics_csv.exists(), f"metrics CSV must exist: {metrics_csv}"
    rows: list[MetricsRow] = []
    with metrics_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            rows.append(
                MetricsRow(
                    multiplier=float(raw[multiplier_column]),
                    peak_hz=float(raw[PEAK_HZ_COLUMN]),
                    null_hz=float(raw[NULL_HZ_COLUMN]),
                    dsi_primary=float(raw[DSI_PRIMARY_COLUMN]),
                    dsi_vector_sum=float(raw[DSI_VECTOR_SUM_COLUMN]),
                ),
            )
    rows.sort(key=lambda row: row.multiplier)
    return rows
