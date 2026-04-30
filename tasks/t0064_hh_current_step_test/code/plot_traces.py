"""t0064 — plot voltage response to current-step injection."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tasks.t0064_hh_current_step_test.code.constants import (
    CURRENT_NA_VALUES,
    DELAY_MS,
    DURATION_MS,
)
from tasks.t0064_hh_current_step_test.code.paths import (
    IMAGES_DIR,
    VOLTAGE_GRID_PNG,
    VOLTAGE_OVERLAY_PNG,
    VOLTAGE_TRACES_CSV,
)


def _load_traces() -> pd.DataFrame:
    return pd.read_csv(filepath_or_buffer=VOLTAGE_TRACES_CSV)


def _plot_grid(*, df: pd.DataFrame) -> None:
    n: int = len(CURRENT_NA_VALUES)
    n_cols: int = 3
    n_rows: int = (n + n_cols - 1) // n_cols
    fig, axes = plt.subplots(
        nrows=n_rows,
        ncols=n_cols,
        figsize=(n_cols * 4.5, n_rows * 3.0),
        sharex=True,
        sharey=True,
    )
    axes_flat = np.array(axes).flatten()
    for idx, current_na in enumerate(CURRENT_NA_VALUES):
        ax = axes_flat[idx]
        sub_full = df[
            (np.isclose(df["current_na"], current_na)) & (df["mode"] == "full")
        ].sort_values("sample_idx")
        sub_passive = df[
            (np.isclose(df["current_na"], current_na)) & (df["mode"] == "epsp_passive")
        ].sort_values("sample_idx")
        ax.plot(
            sub_full["t_ms"].to_numpy(),
            sub_full["v_soma_mv"].to_numpy(),
            color="C3",
            linestyle="-",
            label="FULL (HH on)",
            linewidth=1.5,
        )
        ax.plot(
            sub_passive["t_ms"].to_numpy(),
            sub_passive["v_soma_mv"].to_numpy(),
            color="C0",
            linestyle="--",
            label="EPSP_PASSIVE (HH off)",
            linewidth=1.2,
        )
        ax.axvline(x=DELAY_MS, color="grey", linestyle=":", alpha=0.5)
        ax.axvline(x=DELAY_MS + DURATION_MS, color="grey", linestyle=":", alpha=0.5)
        ax.set_title(f"I = {current_na:.2f} nA")
        ax.set_xlabel("time (ms)")
        ax.set_ylabel("V_soma (mV)")
        ax.grid(visible=True, alpha=0.3)
        if idx == 0:
            ax.legend(loc="lower right", fontsize=8)
    for idx in range(len(CURRENT_NA_VALUES), len(axes_flat)):
        axes_flat[idx].axis("off")
    fig.suptitle(
        "t0064: soma V(t) under IClamp current step (200 ms); HH on (red) vs HH off (blue)",
        fontsize=13,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(VOLTAGE_GRID_PNG, dpi=110)
    plt.close(fig)
    print(f"[t0064] wrote {VOLTAGE_GRID_PNG}", flush=True)


def _plot_overlay(*, df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(11.0, 6.5))
    cmap = plt.get_cmap(name="viridis")
    n: int = len(CURRENT_NA_VALUES)
    for idx, current_na in enumerate(CURRENT_NA_VALUES):
        colour = cmap(idx / max(1, n - 1))
        sub_full = df[
            (np.isclose(df["current_na"], current_na)) & (df["mode"] == "full")
        ].sort_values("sample_idx")
        sub_passive = df[
            (np.isclose(df["current_na"], current_na)) & (df["mode"] == "epsp_passive")
        ].sort_values("sample_idx")
        ax.plot(
            sub_full["t_ms"].to_numpy(),
            sub_full["v_soma_mv"].to_numpy(),
            color=colour,
            label=f"I = {current_na:.2f} nA, FULL",
            linestyle="-",
            linewidth=1.4,
        )
        ax.plot(
            sub_passive["t_ms"].to_numpy(),
            sub_passive["v_soma_mv"].to_numpy(),
            color=colour,
            label=f"I = {current_na:.2f} nA, EPSP_PASSIVE",
            linestyle="--",
            linewidth=1.0,
        )
    ax.set_title(
        "t0064: soma V(t) under IClamp current step; all 12 traces; viridis = current",
        fontsize=12,
    )
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("V_soma (mV)")
    ax.grid(visible=True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=7, ncol=2)
    fig.tight_layout()
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(VOLTAGE_OVERLAY_PNG, dpi=110)
    plt.close(fig)
    print(f"[t0064] wrote {VOLTAGE_OVERLAY_PNG}", flush=True)


def main() -> None:
    df: pd.DataFrame = _load_traces()
    _plot_grid(df=df)
    _plot_overlay(df=df)


if __name__ == "__main__":
    main()
