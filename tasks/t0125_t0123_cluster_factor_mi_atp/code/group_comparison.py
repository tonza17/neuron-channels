"""High vs low group comparison for all 68 parameters on the spiking cohort.

For each of the 68 parameters compute:
  * mean and std for high-MI, low-MI, high-ATP, low-ATP groups
  * Mann-Whitney U two-sided p-value for high vs low MI and high vs low ATP
  * Cliff's delta for the same two pairs

Outputs:
    results/data/group_comparison.csv
    results/images/cliffs_delta_high_vs_low_mi.png
    results/images/cliffs_delta_high_vs_low_atp.png
"""

from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy.stats import mannwhitneyu

from tasks.t0125_t0123_cluster_factor_mi_atp.code.constants import (
    ALL_PARAM_NAMES,
    CHART_DPI,
    CLIFFS_DELTA_TOP_N,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.effect_sizes import cliffs_delta
from tasks.t0125_t0123_cluster_factor_mi_atp.code.load_t0123_cells import (
    ATP_PER_SPIKE_COLUMN,
    MI_COLUMN,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.paths import (
    CLIFFS_DELTA_ATP_PNG,
    CLIFFS_DELTA_MI_PNG,
    GROUP_COMPARISON_CSV,
    GROUP_THRESHOLDS_JSON,
    T0123_SPIKING_CELLS_PARQUET,
)

PARAMETER_COLUMN: str = "parameter"


def _compute_group_masks(
    *,
    df: pd.DataFrame,
    thresholds: dict[str, float],
) -> tuple[NDArray[np.bool_], NDArray[np.bool_], NDArray[np.bool_], NDArray[np.bool_]]:
    mi_vals: NDArray[np.float64] = df[MI_COLUMN].to_numpy(dtype=np.float64)
    atp_vals: NDArray[np.float64] = df[ATP_PER_SPIKE_COLUMN].to_numpy(dtype=np.float64)
    high_mi: NDArray[np.bool_] = mi_vals >= thresholds["mi_q3"]
    low_mi: NDArray[np.bool_] = mi_vals <= thresholds["mi_q1"]
    high_atp: NDArray[np.bool_] = atp_vals >= thresholds["atp_q3"]
    low_atp: NDArray[np.bool_] = atp_vals <= thresholds["atp_q1"]
    return high_mi, low_mi, high_atp, low_atp


def _per_parameter_row(
    *,
    name: str,
    values_high_mi: NDArray[np.float64],
    values_low_mi: NDArray[np.float64],
    values_high_atp: NDArray[np.float64],
    values_low_atp: NDArray[np.float64],
) -> dict[str, object]:
    p_mi: float
    delta_mi: float
    if len(values_high_mi) > 0 and len(values_low_mi) > 0:
        _u_mi, p_mi_raw = mannwhitneyu(values_high_mi, values_low_mi, alternative="two-sided")
        p_mi = float(p_mi_raw)
        delta_mi = cliffs_delta(values_high_mi, values_low_mi)
    else:
        p_mi = float("nan")
        delta_mi = float("nan")
    p_atp: float
    delta_atp: float
    if len(values_high_atp) > 0 and len(values_low_atp) > 0:
        _u_atp, p_atp_raw = mannwhitneyu(values_high_atp, values_low_atp, alternative="two-sided")
        p_atp = float(p_atp_raw)
        delta_atp = cliffs_delta(values_high_atp, values_low_atp)
    else:
        p_atp = float("nan")
        delta_atp = float("nan")
    return {
        PARAMETER_COLUMN: name,
        "mean_high_mi": float(values_high_mi.mean()) if len(values_high_mi) > 0 else float("nan"),
        "std_high_mi": float(values_high_mi.std(ddof=0))
        if len(values_high_mi) > 0
        else float("nan"),
        "mean_low_mi": float(values_low_mi.mean()) if len(values_low_mi) > 0 else float("nan"),
        "std_low_mi": float(values_low_mi.std(ddof=0)) if len(values_low_mi) > 0 else float("nan"),
        "mwu_p_mi": float(p_mi),
        "cliffs_delta_mi": float(delta_mi),
        "mean_high_atp": float(values_high_atp.mean())
        if len(values_high_atp) > 0
        else float("nan"),
        "std_high_atp": float(values_high_atp.std(ddof=0))
        if len(values_high_atp) > 0
        else float("nan"),
        "mean_low_atp": float(values_low_atp.mean()) if len(values_low_atp) > 0 else float("nan"),
        "std_low_atp": float(values_low_atp.std(ddof=0))
        if len(values_low_atp) > 0
        else float("nan"),
        "mwu_p_atp": float(p_atp),
        "cliffs_delta_atp": float(delta_atp),
    }


def _render_top_n_bar_chart(
    *,
    df: pd.DataFrame,
    delta_column: str,
    output_path,
    title: str,
    bar_color: str,
) -> None:
    df_sorted: pd.DataFrame = (
        df.assign(_abs_delta=df[delta_column].abs())
        .sort_values(by="_abs_delta", ascending=False)
        .head(CLIFFS_DELTA_TOP_N)
        .iloc[::-1]
    )
    fig, ax = plt.subplots(figsize=(8, 0.4 * len(df_sorted) + 2), dpi=CHART_DPI)
    y_pos: NDArray[np.int_] = np.arange(len(df_sorted))
    bars = ax.barh(
        y_pos,
        df_sorted[delta_column].to_numpy(),
        color=bar_color,
        alpha=0.85,
        edgecolor="black",
    )
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_sorted[PARAMETER_COLUMN].tolist(), fontsize=8)
    ax.axvline(0.0, color="black", linewidth=0.8)
    ax.set_xlabel("Cliff's delta")
    ax.set_title(title)
    for bar_obj, val in zip(bars, df_sorted[delta_column].tolist(), strict=True):
        ax.text(
            bar_obj.get_width(),
            bar_obj.get_y() + bar_obj.get_height() / 2,
            f"{val:+.3f}",
            va="center",
            ha="left" if val >= 0 else "right",
            fontsize=7,
            color="black",
        )
    ax.grid(True, alpha=0.3, axis="x")
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)
    print(f"Wrote {output_path}", flush=True)


def main() -> None:
    df_spiking: pd.DataFrame = pd.read_parquet(T0123_SPIKING_CELLS_PARQUET)
    thresholds: dict[str, float] = json.loads(GROUP_THRESHOLDS_JSON.read_text(encoding="utf-8"))
    high_mi_mask, low_mi_mask, high_atp_mask, low_atp_mask = _compute_group_masks(
        df=df_spiking, thresholds=thresholds
    )
    print(
        f"Group sizes: high_mi={int(high_mi_mask.sum())}, low_mi={int(low_mi_mask.sum())}, "
        f"high_atp={int(high_atp_mask.sum())}, low_atp={int(low_atp_mask.sum())}",
        flush=True,
    )

    rows: list[dict[str, object]] = []
    for name in ALL_PARAM_NAMES:
        values: NDArray[np.float64] = df_spiking[name].to_numpy(dtype=np.float64)
        rows.append(
            _per_parameter_row(
                name=name,
                values_high_mi=values[high_mi_mask],
                values_low_mi=values[low_mi_mask],
                values_high_atp=values[high_atp_mask],
                values_low_atp=values[low_atp_mask],
            )
        )
    out_df: pd.DataFrame = pd.DataFrame(rows)
    GROUP_COMPARISON_CSV.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(GROUP_COMPARISON_CSV, index=False)
    print(f"Wrote {GROUP_COMPARISON_CSV} (n_rows={len(out_df)})", flush=True)

    _render_top_n_bar_chart(
        df=out_df,
        delta_column="cliffs_delta_mi",
        output_path=CLIFFS_DELTA_MI_PNG,
        title=(
            f"Top {CLIFFS_DELTA_TOP_N} parameters by |Cliff's delta| (high MI vs low MI, "
            f"spiking cohort n={len(df_spiking)})"
        ),
        bar_color="#1f77b4",
    )
    _render_top_n_bar_chart(
        df=out_df,
        delta_column="cliffs_delta_atp",
        output_path=CLIFFS_DELTA_ATP_PNG,
        title=(
            f"Top {CLIFFS_DELTA_TOP_N} parameters by |Cliff's delta| (high ATP vs low ATP, "
            f"spiking cohort n={len(df_spiking)})"
        ),
        bar_color="#d62728",
    )


if __name__ == "__main__":
    main()
