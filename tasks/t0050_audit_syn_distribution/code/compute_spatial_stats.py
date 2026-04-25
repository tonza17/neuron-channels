"""Compute per-channel spatial statistics under three midline conventions.

Reads ``results/synapse_coordinates.csv`` and produces ``results/per_channel_density_stats.csv``
with one row per (channel, midline_kind) combination — 3 channels x 3 midlines = 9 rows.

For each combination, computes:

* Counts: total, side_a, side_b, ratio side_a / side_b
* Per-side radial-distance mean +- SD
* Per-side path-distance mean +- SD
* Per-side total dendritic length (sum of parent section length)
* Per-side density (count / total length)
* Verdict: symmetric if ratio in [SYMMETRY_RATIO_LOW, SYMMETRY_RATIO_HIGH]
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
import pandas as pd
from numpy import dtype as np_dtype
from pandas.api.extensions import ExtensionDtype

from tasks.t0050_audit_syn_distribution.code import paths
from tasks.t0050_audit_syn_distribution.code.constants import (
    CHANNEL_DISPLAY_NAMES,
    CHANNEL_LOCX_COLUMNS,
    COLUMN_BIP_LOCX_UM,
    COLUMN_CHANNEL,
    COLUMN_COUNT_RATIO,
    COLUMN_COUNT_SIDE_A,
    COLUMN_COUNT_SIDE_B,
    COLUMN_COUNT_TOTAL,
    COLUMN_DENSITY_SIDE_A,
    COLUMN_DENSITY_SIDE_B,
    COLUMN_MEAN_PATH_SIDE_A,
    COLUMN_MEAN_PATH_SIDE_B,
    COLUMN_MEAN_RADIAL_SIDE_A,
    COLUMN_MEAN_RADIAL_SIDE_B,
    COLUMN_MIDLINE_KIND,
    COLUMN_MIDLINE_X_UM,
    COLUMN_PARENT_SECTION_LENGTH_UM,
    COLUMN_PATH_DISTANCE_UM,
    COLUMN_RADIAL_DISTANCE_UM,
    COLUMN_SD_PATH_SIDE_A,
    COLUMN_SD_PATH_SIDE_B,
    COLUMN_SD_RADIAL_SIDE_A,
    COLUMN_SD_RADIAL_SIDE_B,
    COLUMN_TOTAL_LENGTH_SIDE_A,
    COLUMN_TOTAL_LENGTH_SIDE_B,
    COLUMN_VERDICT_SYMMETRIC,
    EXPECTED_NUMSYN,
    MIDLINE_KIND_BIP_MEDIAN,
    MIDLINE_KIND_SOMA_X,
    MIDLINE_KIND_ZERO,
    MIDLINE_KINDS,
    SYMMETRY_RATIO_HIGH,
    SYMMETRY_RATIO_LOW,
    ChannelKind,
)

# Soma centroid x-coordinate from extract_coordinates.py log output (logged when the script
# ran). Hardcoded here to avoid a second NEURON cell build; the value is also recoverable from
# results/synapse_coordinates.csv row 0 (the soma itself), but storing it explicitly here lets
# this script run without NEURON.
# Source: extract_coordinates.py stdout: "soma centroid (x,y,z) = (104.576, 121.779, 47.494) um"
SOMA_X_UM: float = 104.576


@dataclass(frozen=True, slots=True)
class PerChannelSpatialStats:
    """One row of the per-channel x per-midline statistics table."""

    channel: str
    midline_kind: str
    midline_x_um: float
    count_total: int
    count_side_a: int
    count_side_b: int
    count_ratio_side_a_over_b: float
    mean_radial_distance_side_a_um: float
    sd_radial_distance_side_a_um: float
    mean_radial_distance_side_b_um: float
    sd_radial_distance_side_b_um: float
    mean_path_distance_side_a_um: float
    sd_path_distance_side_a_um: float
    mean_path_distance_side_b_um: float
    sd_path_distance_side_b_um: float
    total_length_side_a_um: float
    total_length_side_b_um: float
    density_side_a_per_um: float
    density_side_b_per_um: float
    verdict_symmetric: bool


def _safe_mean(*, values: pd.Series) -> float:
    if len(values) == 0:
        return float("nan")
    return float(values.mean())


def _safe_std(*, values: pd.Series) -> float:
    if len(values) == 0:
        return float("nan")
    # Bessel-corrected SD; matches numpy default ddof=1 used in scientific reports.
    return float(values.std(ddof=1)) if len(values) > 1 else 0.0


def _safe_div(*, numerator: float, denominator: float) -> float:
    if denominator == 0.0:
        return float("nan")
    return numerator / denominator


def midline_x_for_kind(*, kind: str, df: pd.DataFrame) -> float:
    if kind == MIDLINE_KIND_SOMA_X:
        return SOMA_X_UM
    if kind == MIDLINE_KIND_ZERO:
        return 0.0
    if kind == MIDLINE_KIND_BIP_MEDIAN:
        return float(df[COLUMN_BIP_LOCX_UM].median())
    raise ValueError(f"Unknown midline kind: {kind}")


def compute_one(
    *,
    df: pd.DataFrame,
    channel: ChannelKind,
    midline_kind: str,
) -> PerChannelSpatialStats:
    """Compute statistics for one (channel, midline) cell."""
    locx_col: str = CHANNEL_LOCX_COLUMNS[channel]
    midline_x: float = midline_x_for_kind(kind=midline_kind, df=df)

    side_a_mask: pd.Series = df[locx_col] < midline_x
    side_b_mask: pd.Series = df[locx_col] >= midline_x

    df_side_a: pd.DataFrame = df[side_a_mask]
    df_side_b: pd.DataFrame = df[side_b_mask]

    count_total: int = int(len(df))
    count_side_a: int = int(side_a_mask.sum())
    count_side_b: int = int(side_b_mask.sum())
    assert count_side_a + count_side_b == count_total, (
        f"channel={channel.value} midline={midline_kind}: "
        f"side counts {count_side_a}+{count_side_b} != total {count_total}"
    )

    ratio: float = _safe_div(numerator=float(count_side_a), denominator=float(count_side_b))

    mean_rad_a: float = _safe_mean(values=df_side_a[COLUMN_RADIAL_DISTANCE_UM])
    sd_rad_a: float = _safe_std(values=df_side_a[COLUMN_RADIAL_DISTANCE_UM])
    mean_rad_b: float = _safe_mean(values=df_side_b[COLUMN_RADIAL_DISTANCE_UM])
    sd_rad_b: float = _safe_std(values=df_side_b[COLUMN_RADIAL_DISTANCE_UM])

    mean_path_a: float = _safe_mean(values=df_side_a[COLUMN_PATH_DISTANCE_UM])
    sd_path_a: float = _safe_std(values=df_side_a[COLUMN_PATH_DISTANCE_UM])
    mean_path_b: float = _safe_mean(values=df_side_b[COLUMN_PATH_DISTANCE_UM])
    sd_path_b: float = _safe_std(values=df_side_b[COLUMN_PATH_DISTANCE_UM])

    # The parent section is shared across all three channels for a given index, so the per-side
    # length total for the BIP locx is the per-side dendritic length for SAC channels too only
    # when classified by the SAME locx column. To be channel-correct, we use the same channel's
    # locx for both classification and length-summing.
    total_len_a: float = float(df_side_a[COLUMN_PARENT_SECTION_LENGTH_UM].sum())
    total_len_b: float = float(df_side_b[COLUMN_PARENT_SECTION_LENGTH_UM].sum())

    density_a: float = _safe_div(numerator=float(count_side_a), denominator=total_len_a)
    density_b: float = _safe_div(numerator=float(count_side_b), denominator=total_len_b)

    verdict: bool = SYMMETRY_RATIO_LOW <= ratio <= SYMMETRY_RATIO_HIGH

    return PerChannelSpatialStats(
        channel=channel.value,
        midline_kind=midline_kind,
        midline_x_um=midline_x,
        count_total=count_total,
        count_side_a=count_side_a,
        count_side_b=count_side_b,
        count_ratio_side_a_over_b=ratio,
        mean_radial_distance_side_a_um=mean_rad_a,
        sd_radial_distance_side_a_um=sd_rad_a,
        mean_radial_distance_side_b_um=mean_rad_b,
        sd_radial_distance_side_b_um=sd_rad_b,
        mean_path_distance_side_a_um=mean_path_a,
        sd_path_distance_side_a_um=sd_path_a,
        mean_path_distance_side_b_um=mean_path_b,
        sd_path_distance_side_b_um=sd_path_b,
        total_length_side_a_um=total_len_a,
        total_length_side_b_um=total_len_b,
        density_side_a_per_um=density_a,
        density_side_b_per_um=density_b,
        verdict_symmetric=verdict,
    )


def compute_all(*, df: pd.DataFrame) -> list[PerChannelSpatialStats]:
    rows: list[PerChannelSpatialStats] = []
    for channel in ChannelKind:
        for midline_kind in MIDLINE_KINDS:
            rows.append(compute_one(df=df, channel=channel, midline_kind=midline_kind))
    return rows


def write_stats_csv(*, rows: list[PerChannelSpatialStats]) -> None:
    records: list[dict[str, object]] = [asdict(r) for r in rows]
    out_df: pd.DataFrame = pd.DataFrame.from_records(data=records)

    dtype_spec: dict[str, np_dtype[Any] | ExtensionDtype] = {
        COLUMN_CHANNEL: pd.StringDtype(),
        COLUMN_MIDLINE_KIND: pd.StringDtype(),
        COLUMN_MIDLINE_X_UM: np.dtype("float64"),
        COLUMN_COUNT_TOTAL: pd.UInt32Dtype(),
        COLUMN_COUNT_SIDE_A: pd.UInt32Dtype(),
        COLUMN_COUNT_SIDE_B: pd.UInt32Dtype(),
        COLUMN_COUNT_RATIO: np.dtype("float64"),
        COLUMN_MEAN_RADIAL_SIDE_A: np.dtype("float64"),
        COLUMN_SD_RADIAL_SIDE_A: np.dtype("float64"),
        COLUMN_MEAN_RADIAL_SIDE_B: np.dtype("float64"),
        COLUMN_SD_RADIAL_SIDE_B: np.dtype("float64"),
        COLUMN_MEAN_PATH_SIDE_A: np.dtype("float64"),
        COLUMN_SD_PATH_SIDE_A: np.dtype("float64"),
        COLUMN_MEAN_PATH_SIDE_B: np.dtype("float64"),
        COLUMN_SD_PATH_SIDE_B: np.dtype("float64"),
        COLUMN_TOTAL_LENGTH_SIDE_A: np.dtype("float64"),
        COLUMN_TOTAL_LENGTH_SIDE_B: np.dtype("float64"),
        COLUMN_DENSITY_SIDE_A: np.dtype("float64"),
        COLUMN_DENSITY_SIDE_B: np.dtype("float64"),
        COLUMN_VERDICT_SYMMETRIC: pd.BooleanDtype(),
    }
    for col, dt in dtype_spec.items():
        out_df[col] = out_df[col].astype(dt)

    out_df.to_csv(path_or_buf=paths.PER_CHANNEL_DENSITY_STATS_CSV, index=False)


def print_headline_table(*, rows: list[PerChannelSpatialStats]) -> None:
    print("\n[stats] Headline midline = soma_x", flush=True)
    print(
        "| Channel | count_total | count_side_a | count_side_b | ratio | symmetric? |",
        flush=True,
    )
    print("|---|---|---|---|---|---|", flush=True)
    for row in rows:
        if row.midline_kind != MIDLINE_KIND_SOMA_X:
            continue
        channel_kind: ChannelKind = ChannelKind(row.channel)
        display_name: str = CHANNEL_DISPLAY_NAMES[channel_kind]
        print(
            f"| {display_name} | {row.count_total} | {row.count_side_a} | "
            f"{row.count_side_b} | {row.count_ratio_side_a_over_b:.3f} | "
            f"{row.verdict_symmetric} |",
            flush=True,
        )


def main() -> None:
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=paths.SYNAPSE_COORDINATES_CSV)
    assert df.shape == (EXPECTED_NUMSYN, 17), (
        f"synapse_coordinates.csv shape {df.shape} != expected ({EXPECTED_NUMSYN}, 17)"
    )

    rows: list[PerChannelSpatialStats] = compute_all(df=df)
    write_stats_csv(rows=rows)
    print(
        f"[stats] Wrote {len(rows)} rows to {paths.PER_CHANNEL_DENSITY_STATS_CSV}",
        flush=True,
    )
    print_headline_table(rows=rows)


if __name__ == "__main__":
    main()
