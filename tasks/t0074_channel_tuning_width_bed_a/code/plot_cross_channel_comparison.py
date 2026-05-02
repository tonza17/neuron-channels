"""Cross-channel comparison plot: vector-sum DSI vs density for all 8 channels.

One line per channel (Okabe-Ito palette). Horizontal dashed line at the baseline
vector_sum_dsi value. Output: ``results/images/all_channels_dsi_vs_density.png``.
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
    COL_VECTOR_SUM_DSI,
    DensityLabel,
)
from tasks.t0074_channel_tuning_width_bed_a.code.paths import (
    IMAGES_DIR,
    METRICS_SUMMARY_CSV,
)

# Okabe-Ito palette (8 colour-blind-friendly entries).
OKABE_ITO_PALETTE: tuple[str, ...] = (
    "#000000",
    "#E69F00",
    "#56B4E9",
    "#009E73",
    "#F0E442",
    "#0072B2",
    "#D55E00",
    "#CC79A7",
)

DENSITY_ORDER: tuple[DensityLabel, ...] = (
    DensityLabel.LOW,
    DensityLabel.MED,
    DensityLabel.HIGH,
)


def main() -> int:
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=METRICS_SUMMARY_CSV)
    baseline_rows: pd.DataFrame = df[df[COL_CONDITION_ID] == BASELINE_CONDITION_ID]
    baseline_vec: float = (
        float(baseline_rows.iloc[0][COL_VECTOR_SUM_DSI]) if len(baseline_rows) > 0 else 0.0
    )

    fig: Any
    ax: Any
    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=120)
    for idx, ch in enumerate(CHANNEL_DEFS):
        rows: pd.DataFrame = df[df[COL_CHANNEL_KIND] == ch.kind.value].copy()
        rows = rows.set_index(keys=COL_DENSITY_LABEL)
        ordered: pd.DataFrame = rows.reindex(
            index=[lab.value for lab in DENSITY_ORDER],
        ).reset_index()
        if len(ordered) == 0:
            continue
        densities: NDArray[np.float64] = ordered[COL_DENSITY_MS_CM2].to_numpy(
            dtype=np.float64,
        )
        vec_dsi: NDArray[np.float64] = ordered[COL_VECTOR_SUM_DSI].to_numpy(
            dtype=np.float64,
        )
        ax.plot(
            densities,
            vec_dsi,
            "o-",
            color=OKABE_ITO_PALETTE[idx % len(OKABE_ITO_PALETTE)],
            label=ch.kind.value,
        )
    ax.axhline(
        y=baseline_vec,
        linestyle="--",
        color="#888888",
        label=f"baseline ({baseline_vec:.3f})",
    )
    ax.set_xlabel("density (mS/cm^2)")
    ax.set_xscale("log")
    ax.set_ylabel("vector-sum DSI")
    ax.set_title("Vector-sum DSI vs density per channel")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=9, ncol=2)
    fig.tight_layout()
    out_png = IMAGES_DIR / "all_channels_dsi_vs_density.png"
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_png}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
