"""t0062 — plot voltage traces (NMDA + AMPA-priming, mirror of t0061 plotter)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tasks.t0062_nmda_escape_with_ampa_priming.code.constants import (
    GAMPA_PRIMING_NS,
    GNMDA_NS_VALUES,
)
from tasks.t0062_nmda_escape_with_ampa_priming.code.paths import (
    IMAGES_DIR,
    VOLTAGE_GRID_PNG,
    VOLTAGE_OVERLAY_PNG,
    VOLTAGE_TRACES_CSV,
)


def _load_traces() -> pd.DataFrame:
    return pd.read_csv(filepath_or_buffer=VOLTAGE_TRACES_CSV)


def _plot_grid(*, df: pd.DataFrame) -> None:
    n: int = len(GNMDA_NS_VALUES)
    n_cols: int = 4
    n_rows: int = (n + n_cols - 1) // n_cols
    fig, axes = plt.subplots(
        nrows=n_rows,
        ncols=n_cols,
        figsize=(n_cols * 4.0, n_rows * 3.0),
        sharex=True,
        sharey=True,
    )
    axes_flat = np.array(axes).flatten()
    for idx, gnmda_ns in enumerate(GNMDA_NS_VALUES):
        ax = axes_flat[idx]
        sub_full: pd.DataFrame = df[
            (np.isclose(df["gnmda_ns"], gnmda_ns)) & (df["mode"] == "full")
        ].sort_values("sample_idx")
        sub_passive: pd.DataFrame = df[
            (np.isclose(df["gnmda_ns"], gnmda_ns)) & (df["mode"] == "epsp_passive")
        ].sort_values("sample_idx")
        ax.plot(
            sub_full["t_ms"].to_numpy(),
            sub_full["v_soma_mv"].to_numpy(),
            color="C3",
            linestyle="-",
            label="FULL (HH on)",
        )
        ax.plot(
            sub_passive["t_ms"].to_numpy(),
            sub_passive["v_soma_mv"].to_numpy(),
            color="C0",
            linestyle="--",
            label="EPSP_PASSIVE (HH off)",
        )
        ax.set_title(f"gNMDA = {gnmda_ns:.1f} nS")
        ax.set_xlabel("time (ms)")
        ax.set_ylabel("V_soma (mV)")
        ax.grid(visible=True, alpha=0.3)
        if idx == 0:
            ax.legend(loc="lower right", fontsize=8)
    for idx in range(len(GNMDA_NS_VALUES), len(axes_flat)):
        axes_flat[idx].axis("off")
    fig.suptitle(
        f"t0062: soma V(t) at theta = 0 deg, GABA = 0, AMPA = {GAMPA_PRIMING_NS} nS priming; "
        f"NMDA escape sweep",
        fontsize=14,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.97))
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(VOLTAGE_GRID_PNG, dpi=110)
    plt.close(fig)
    print(f"[t0062] wrote {VOLTAGE_GRID_PNG}", flush=True)


def _plot_overlay(*, df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(11.0, 6.5))
    cmap = plt.get_cmap(name="viridis")
    n: int = len(GNMDA_NS_VALUES)
    for idx, gnmda_ns in enumerate(GNMDA_NS_VALUES):
        colour = cmap(idx / max(1, n - 1))
        sub_full: pd.DataFrame = df[
            (np.isclose(df["gnmda_ns"], gnmda_ns)) & (df["mode"] == "full")
        ].sort_values("sample_idx")
        sub_passive: pd.DataFrame = df[
            (np.isclose(df["gnmda_ns"], gnmda_ns)) & (df["mode"] == "epsp_passive")
        ].sort_values("sample_idx")
        ax.plot(
            sub_full["t_ms"].to_numpy(),
            sub_full["v_soma_mv"].to_numpy(),
            color=colour,
            label=f"gNMDA = {gnmda_ns:.1f} nS, FULL",
            linestyle="-",
            linewidth=1.4,
        )
        ax.plot(
            sub_passive["t_ms"].to_numpy(),
            sub_passive["v_soma_mv"].to_numpy(),
            color=colour,
            label=f"gNMDA = {gnmda_ns:.1f} nS, EPSP_PASSIVE",
            linestyle="--",
            linewidth=1.0,
        )
    ax.set_title(
        f"t0062: soma V(t) at theta = 0 deg, GABA = 0, AMPA = {GAMPA_PRIMING_NS} nS priming; "
        f"all 16 traces",
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
    print(f"[t0062] wrote {VOLTAGE_OVERLAY_PNG}", flush=True)


def main() -> None:
    df: pd.DataFrame = _load_traces()
    _plot_grid(df=df)
    _plot_overlay(df=df)


if __name__ == "__main__":
    main()
