"""Per-channel sensitivity plots: HWHM, vector-sum DSI, peak rate vs density.

For each of 8 channels, plot a 3-panel figure showing the channel's effect on
HWHM, vector-sum DSI, and peak rate at low / med / high density. Overlays the
baseline value as a horizontal dashed reference line. Outputs 8 PNGs:
``results/images/sensitivity_<channel>.png``.
"""

from __future__ import annotations

import sys
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.typing import NDArray

from tasks.t0074_channel_tuning_width_bed_a.code.constants import (
    BASELINE_CONDITION_ID,
    CHANNEL_DEFS,
    COL_CHANNEL_KIND,
    COL_CONDITION_ID,
    COL_DENSITY_LABEL,
    COL_DENSITY_MS_CM2,
    COL_HWHM_DEG,
    COL_PEAK_HZ,
    COL_VECTOR_SUM_DSI,
    DensityLabel,
)
from tasks.t0074_channel_tuning_width_bed_a.code.paths import (
    IMAGES_DIR,
    METRICS_SUMMARY_CSV,
)

DENSITY_ORDER: tuple[DensityLabel, ...] = (
    DensityLabel.LOW,
    DensityLabel.MED,
    DensityLabel.HIGH,
)


def _load_metrics_summary() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=METRICS_SUMMARY_CSV)
    return df


def _baseline_row(*, df: pd.DataFrame) -> pd.Series:
    rows: pd.DataFrame = df[df[COL_CONDITION_ID] == BASELINE_CONDITION_ID]
    if len(rows) == 0:
        raise RuntimeError("Baseline condition not found in metrics_summary.csv")
    return rows.iloc[0]


def _channel_rows(*, df: pd.DataFrame, channel_kind_value: str) -> pd.DataFrame:
    rows: pd.DataFrame = df[df[COL_CHANNEL_KIND] == channel_kind_value].copy()
    rows = rows.set_index(keys=COL_DENSITY_LABEL)
    ordered: pd.DataFrame = rows.reindex(
        index=[lab.value for lab in DENSITY_ORDER],
    )
    return ordered.reset_index()


def _plot_one_channel(
    *,
    channel_kind_value: str,
    suffix: str,
    df: pd.DataFrame,
    baseline: pd.Series,
) -> None:
    rows: pd.DataFrame = _channel_rows(df=df, channel_kind_value=channel_kind_value)
    if len(rows) == 0:
        print(f"  No rows found for channel {channel_kind_value}; skipping plot")
        return

    densities_mS_cm2: NDArray[np.float64] = rows[COL_DENSITY_MS_CM2].to_numpy(
        dtype=np.float64,
    )
    hwhm: NDArray[np.float64] = rows[COL_HWHM_DEG].to_numpy(dtype=np.float64)
    vec_dsi: NDArray[np.float64] = rows[COL_VECTOR_SUM_DSI].to_numpy(dtype=np.float64)
    peak: NDArray[np.float64] = rows[COL_PEAK_HZ].to_numpy(dtype=np.float64)

    base_hwhm: float = (
        float(baseline[COL_HWHM_DEG]) if pd.notna(baseline[COL_HWHM_DEG]) else float("nan")
    )
    base_vec: float = float(baseline[COL_VECTOR_SUM_DSI])
    base_peak: float = float(baseline[COL_PEAK_HZ])

    fig: Any
    axes: Any
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), dpi=120)
    titles: tuple[str, str, str] = (
        "HWHM (deg)",
        "Vector-sum DSI",
        "Peak rate (Hz)",
    )
    series: tuple[NDArray[np.float64], ...] = (hwhm, vec_dsi, peak)
    baselines: tuple[float, float, float] = (base_hwhm, base_vec, base_peak)

    for ax, title, y, base_val in zip(axes, titles, series, baselines, strict=True):
        valid_mask: NDArray[np.bool_] = ~np.isnan(y)
        ax.plot(
            densities_mS_cm2[valid_mask],
            y[valid_mask],
            "o-",
            color="#0072B2",
            label=channel_kind_value,
        )
        if not np.isnan(base_val):
            ax.axhline(y=base_val, linestyle="--", color="#666666", label="baseline")
        ax.set_xlabel("density (mS/cm^2)")
        ax.set_xscale("log")
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best", fontsize=8)

    fig.suptitle(f"Channel sensitivity: {channel_kind_value}", fontsize=14)
    fig.tight_layout()
    out_png = IMAGES_DIR / f"sensitivity_{suffix}.png"
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {out_png}", flush=True)


def main() -> int:
    df: pd.DataFrame = _load_metrics_summary()
    baseline: pd.Series = _baseline_row(df=df)
    for ch in CHANNEL_DEFS:
        suffix: str = ch.kind.value.replace(".", "").lower()
        _plot_one_channel(
            channel_kind_value=ch.kind.value,
            suffix=suffix,
            df=df,
            baseline=baseline,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
