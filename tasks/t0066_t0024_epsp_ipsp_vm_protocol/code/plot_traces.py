"""Render the t0066 EPSP/IPSP/FULL plots from voltage_traces.csv.

Six PNG outputs:

1. ``vm_full_pd_vs_nd.png`` — FULL mode mean trace + IQR shading, PD vs ND.
2. ``epsp_pd_vs_nd.png`` — EPSP_PASSIVE mean + IQR, PD vs ND.
3. ``ipsp_pd_vs_nd.png`` — IPSP_PASSIVE mean + IQR, PD vs ND.
4. ``three_mode_pd_overlay.png`` — PD direction across all 3 modes (mean + IQR).
5. ``three_mode_nd_overlay.png`` — ND direction across all 3 modes (mean + IQR).
6. ``comparison_t0065_vs_t0066_ipsp.png`` — cross-model IPSP_PASSIVE comparison.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.typing import NDArray
from pandas import DataFrame

from tasks.t0066_t0024_epsp_ipsp_vm_protocol.code.constants import (
    CSV_COLUMNS,
    DIRECTION_COLUMN,
    MODE_COLUMN,
    T_MS_COLUMN,
    TRIAL_COLUMN,
    V_MV_COLUMN,
    Condition,
    TrialMode,
)
from tasks.t0066_t0024_epsp_ipsp_vm_protocol.code.paths import (
    COMPARISON_T0065_T0066_PNG,
    EPSP_PNG,
    IMAGES_DIR,
    IPSP_PNG,
    T0065_VOLTAGE_TRACES_CSV,
    THREE_MODE_ND_PNG,
    THREE_MODE_PD_PNG,
    VM_FULL_PNG,
    VOLTAGE_TRACES_CSV,
)

MODE_COLOURS: dict[str, str] = {
    TrialMode.FULL.value: "#222222",
    TrialMode.EPSP_PASSIVE.value: "#2ca02c",
    TrialMode.IPSP_PASSIVE.value: "#9467bd",
}
DIRECTION_COLOURS: dict[str, str] = {
    Condition.PD.value: "#1f77b4",
    Condition.ND.value: "#d62728",
}

CSV_DTYPES: dict[str, str] = {
    MODE_COLUMN: "string",
    DIRECTION_COLUMN: "string",
    TRIAL_COLUMN: "Int32",
    T_MS_COLUMN: "float64",
    V_MV_COLUMN: "float64",
}


def _load_traces(*, csv_path: str) -> DataFrame:
    return pd.read_csv(filepath_or_buffer=csv_path, dtype=CSV_DTYPES, usecols=CSV_COLUMNS)


def _trial_mean_iqr(
    *, df: DataFrame, mode: str, direction: str
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Return (t_ms, mean_v, q25_v, q75_v) for a (mode, direction) cell across trials."""
    sub = df[(df[MODE_COLUMN] == mode) & (df[DIRECTION_COLUMN] == direction)]
    if sub.empty:
        empty = np.empty(0, dtype=np.float64)
        return empty, empty, empty, empty
    pivot = sub.pivot_table(
        index=T_MS_COLUMN,
        columns=TRIAL_COLUMN,
        values=V_MV_COLUMN,
        aggfunc="mean",
    )
    pivot_arr = pivot.to_numpy(dtype=np.float64)
    t = pivot.index.to_numpy(dtype=np.float64)
    mean_v = np.nanmean(pivot_arr, axis=1)
    q25_v = np.nanpercentile(pivot_arr, 25, axis=1)
    q75_v = np.nanpercentile(pivot_arr, 75, axis=1)
    return t, mean_v, q25_v, q75_v


def _plot_pd_vs_nd(*, df: DataFrame, mode: str, title: str, png_path: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=120)
    for direction in (Condition.PD.value, Condition.ND.value):
        t, mean_v, q25_v, q75_v = _trial_mean_iqr(df=df, mode=mode, direction=direction)
        if t.size == 0:
            continue
        colour = DIRECTION_COLOURS[direction]
        ax.fill_between(t, q25_v, q75_v, alpha=0.20, color=colour, linewidth=0)
        ax.plot(t, mean_v, color=colour, linewidth=1.5, label=f"{direction} (mean)")
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("V$_m$ (mV)")
    ax.set_title(title)
    ax.legend(loc="upper right", framealpha=0.9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(png_path)
    plt.close(fig)


def _plot_three_modes(*, df: DataFrame, direction: str, title: str, png_path: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=120)
    for mode in (TrialMode.FULL.value, TrialMode.EPSP_PASSIVE.value, TrialMode.IPSP_PASSIVE.value):
        t, mean_v, q25_v, q75_v = _trial_mean_iqr(df=df, mode=mode, direction=direction)
        if t.size == 0:
            continue
        colour = MODE_COLOURS[mode]
        ax.fill_between(t, q25_v, q75_v, alpha=0.18, color=colour, linewidth=0)
        ax.plot(t, mean_v, color=colour, linewidth=1.5, label=f"{mode} (mean)")
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("V$_m$ (mV)")
    ax.set_title(title)
    ax.legend(loc="upper right", framealpha=0.9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(png_path)
    plt.close(fig)


def _plot_cross_model_ipsp(*, t0066_df: DataFrame, png_path: str) -> None:
    """Side-by-side: t0065 IPSP_PASSIVE (1 trial each) vs t0066 IPSP_PASSIVE (20-trial mean+IQR)."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 4.5), dpi=120, sharey=True)

    # t0065: read its CSV with its own column convention (no `trial` column).
    t0065_df = pd.read_csv(filepath_or_buffer=str(T0065_VOLTAGE_TRACES_CSV))
    ax_left = axes[0]
    for direction in (Condition.PD.value, Condition.ND.value):
        sub = t0065_df[
            (t0065_df["mode"] == TrialMode.IPSP_PASSIVE.value)
            & (t0065_df["direction"] == direction)
        ]
        if sub.empty:
            continue
        colour = DIRECTION_COLOURS[direction]
        ax_left.plot(
            sub["t_ms"].to_numpy(dtype=np.float64),
            sub["v_mv"].to_numpy(dtype=np.float64),
            color=colour,
            linewidth=1.5,
            label=f"{direction}",
        )
    ax_left.set_title("t0065 (deposited Poleg-Polsky): IPSP_PASSIVE, 1 trial")
    ax_left.set_xlabel("time (ms)")
    ax_left.set_ylabel("V$_m$ (mV)")
    ax_left.legend(loc="upper right", framealpha=0.9)
    ax_left.grid(alpha=0.3)

    # t0066: 20-trial mean + IQR from this task's CSV.
    ax_right = axes[1]
    for direction in (Condition.PD.value, Condition.ND.value):
        t, mean_v, q25_v, q75_v = _trial_mean_iqr(
            df=t0066_df, mode=TrialMode.IPSP_PASSIVE.value, direction=direction
        )
        if t.size == 0:
            continue
        colour = DIRECTION_COLOURS[direction]
        ax_right.fill_between(t, q25_v, q75_v, alpha=0.20, color=colour, linewidth=0)
        ax_right.plot(t, mean_v, color=colour, linewidth=1.5, label=f"{direction} (mean)")
    ax_right.set_title("t0066 (de Rosenroll 2026): IPSP_PASSIVE, 20-trial mean ± IQR")
    ax_right.set_xlabel("time (ms)")
    ax_right.legend(loc="upper right", framealpha=0.9)
    ax_right.grid(alpha=0.3)

    fig.suptitle(
        "Cross-model IPSP_PASSIVE comparison: both models flat at e_GABA = v_rest = -60 mV",
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(png_path, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    df = _load_traces(csv_path=str(VOLTAGE_TRACES_CSV))
    print(f"Loaded {len(df):,} samples from {VOLTAGE_TRACES_CSV}")

    _plot_pd_vs_nd(
        df=df,
        mode=TrialMode.FULL.value,
        title="FULL mode: somatic V$_m$, PD vs ND (20-trial mean ± IQR)",
        png_path=str(VM_FULL_PNG),
    )
    _plot_pd_vs_nd(
        df=df,
        mode=TrialMode.EPSP_PASSIVE.value,
        title="EPSP_PASSIVE: PD vs ND (excitation only, HH off; mean ± IQR)",
        png_path=str(EPSP_PNG),
    )
    _plot_pd_vs_nd(
        df=df,
        mode=TrialMode.IPSP_PASSIVE.value,
        title="IPSP_PASSIVE: PD vs ND (inhibition only, HH off; mean ± IQR)",
        png_path=str(IPSP_PNG),
    )
    _plot_three_modes(
        df=df,
        direction=Condition.PD.value,
        title="PD direction: three-mode overlay (mean ± IQR)",
        png_path=str(THREE_MODE_PD_PNG),
    )
    _plot_three_modes(
        df=df,
        direction=Condition.ND.value,
        title="ND direction: three-mode overlay (mean ± IQR)",
        png_path=str(THREE_MODE_ND_PNG),
    )
    _plot_cross_model_ipsp(t0066_df=df, png_path=str(COMPARISON_T0065_T0066_PNG))

    print("Wrote 6 PNGs to results/images/.")


if __name__ == "__main__":
    main()
