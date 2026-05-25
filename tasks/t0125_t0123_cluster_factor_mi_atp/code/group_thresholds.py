"""Compute MI / ATP quartile and median thresholds + per-corner counts on the spiking cohort.

Outputs:
    results/data/group_thresholds.json
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from tasks.t0125_t0123_cluster_factor_mi_atp.code.cluster_helpers import write_json
from tasks.t0125_t0123_cluster_factor_mi_atp.code.constants import (
    ATP_QUARTILE_BOTTOM_QUANTILE,
    ATP_QUARTILE_TOP_QUANTILE,
    CORNER_HIGH_MI_HIGH_ATP,
    CORNER_HIGH_MI_LOW_ATP,
    CORNER_LOW_MI_HIGH_ATP,
    CORNER_LOW_MI_LOW_ATP,
    MEDIAN_QUANTILE,
    MI_QUARTILE_BOTTOM_QUANTILE,
    MI_QUARTILE_TOP_QUANTILE,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.load_t0123_cells import (
    ATP_PER_SPIKE_COLUMN,
    MI_COLUMN,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.paths import (
    GROUP_THRESHOLDS_JSON,
    T0123_SPIKING_CELLS_PARQUET,
)


@dataclass(frozen=True, slots=True)
class GroupThresholds:
    mi_q1: float
    mi_median: float
    mi_q3: float
    atp_q1: float
    atp_median: float
    atp_q3: float


def compute_thresholds(*, df_spiking: pd.DataFrame) -> GroupThresholds:
    mi: np.ndarray = df_spiking[MI_COLUMN].to_numpy(dtype=np.float64)
    atp: np.ndarray = df_spiking[ATP_PER_SPIKE_COLUMN].to_numpy(dtype=np.float64)
    return GroupThresholds(
        mi_q1=float(np.quantile(mi, MI_QUARTILE_BOTTOM_QUANTILE)),
        mi_median=float(np.quantile(mi, MEDIAN_QUANTILE)),
        mi_q3=float(np.quantile(mi, MI_QUARTILE_TOP_QUANTILE)),
        atp_q1=float(np.quantile(atp, ATP_QUARTILE_BOTTOM_QUANTILE)),
        atp_median=float(np.quantile(atp, MEDIAN_QUANTILE)),
        atp_q3=float(np.quantile(atp, ATP_QUARTILE_TOP_QUANTILE)),
    )


def assign_corner_label(*, mi_val: float, atp_val: float, thresholds: GroupThresholds) -> str:
    """Assign a 2x2 corner label using the median split on both axes."""
    high_mi: bool = mi_val >= thresholds.mi_median
    low_atp: bool = atp_val < thresholds.atp_median
    if high_mi and low_atp:
        return CORNER_HIGH_MI_LOW_ATP
    if high_mi and not low_atp:
        return CORNER_HIGH_MI_HIGH_ATP
    if not high_mi and low_atp:
        return CORNER_LOW_MI_LOW_ATP
    return CORNER_LOW_MI_HIGH_ATP


def main() -> None:
    df_spiking: pd.DataFrame = pd.read_parquet(T0123_SPIKING_CELLS_PARQUET)
    print(f"Loaded {len(df_spiking)} spiking cells", flush=True)

    thresholds: GroupThresholds = compute_thresholds(df_spiking=df_spiking)
    print(
        f"  MI: q1={thresholds.mi_q1:.4f}, med={thresholds.mi_median:.4f}, "
        f"q3={thresholds.mi_q3:.4f}",
        flush=True,
    )
    print(
        f"  ATP: q1={thresholds.atp_q1:.3e}, med={thresholds.atp_median:.3e}, "
        f"q3={thresholds.atp_q3:.3e}",
        flush=True,
    )

    mi_vals: np.ndarray = df_spiking[MI_COLUMN].to_numpy(dtype=np.float64)
    atp_vals: np.ndarray = df_spiking[ATP_PER_SPIKE_COLUMN].to_numpy(dtype=np.float64)
    high_mi_mask: np.ndarray = mi_vals >= thresholds.mi_q3
    low_mi_mask: np.ndarray = mi_vals <= thresholds.mi_q1
    high_atp_mask: np.ndarray = atp_vals >= thresholds.atp_q3
    low_atp_mask: np.ndarray = atp_vals <= thresholds.atp_q1

    corner_counts: dict[str, int] = {
        CORNER_HIGH_MI_LOW_ATP: 0,
        CORNER_HIGH_MI_HIGH_ATP: 0,
        CORNER_LOW_MI_LOW_ATP: 0,
        CORNER_LOW_MI_HIGH_ATP: 0,
    }
    for mi_v, atp_v in zip(mi_vals.tolist(), atp_vals.tolist(), strict=True):
        label: str = assign_corner_label(mi_val=mi_v, atp_val=atp_v, thresholds=thresholds)
        corner_counts[label] += 1

    payload: dict[str, object] = {
        "mi_q1": thresholds.mi_q1,
        "mi_median": thresholds.mi_median,
        "mi_q3": thresholds.mi_q3,
        "atp_q1": thresholds.atp_q1,
        "atp_median": thresholds.atp_median,
        "atp_q3": thresholds.atp_q3,
        "spiking_cohort_count": int(len(df_spiking)),
        "high_mi_count": int(high_mi_mask.sum()),
        "low_mi_count": int(low_mi_mask.sum()),
        "high_atp_count": int(high_atp_mask.sum()),
        "low_atp_count": int(low_atp_mask.sum()),
        "corner_counts": corner_counts,
    }
    write_json(payload=payload, path=GROUP_THRESHOLDS_JSON)
    print(f"Wrote {GROUP_THRESHOLDS_JSON}", flush=True)
    print(
        f"  corner_counts: {corner_counts} (sum={sum(corner_counts.values())} "
        f"== spiking_cohort_count={len(df_spiking)})",
        flush=True,
    )
    assert sum(corner_counts.values()) == len(df_spiking)


if __name__ == "__main__":
    main()
