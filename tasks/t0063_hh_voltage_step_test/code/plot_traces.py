"""t0063 — plot voltage and clamp current traces with proper zoom."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tasks.t0063_hh_voltage_step_test.code.constants import (
    DUR1_MS,
    DUR2_MS,
    TARGET_MV_VALUES,
)
from tasks.t0063_hh_voltage_step_test.code.paths import (
    CLAMP_CURRENT_GRID_PNG,
    IMAGES_DIR,
    VOLTAGE_GRID_PNG,
    VOLTAGE_TRACES_CSV,
)


def _load_traces() -> pd.DataFrame:
    return pd.read_csv(filepath_or_buffer=VOLTAGE_TRACES_CSV)


def _plot_vm_grid(*, df: pd.DataFrame) -> None:
    n: int = len(TARGET_MV_VALUES)
    n_cols: int = 3
    n_rows: int = (n + n_cols - 1) // n_cols
    fig, axes = plt.subplots(
        nrows=n_rows,
        ncols=n_cols,
        figsize=(n_cols * 4.5, n_rows * 3.0),
        sharex=True,
    )
    axes_flat = np.array(axes).flatten()
    for idx, target_mv in enumerate(TARGET_MV_VALUES):
        ax = axes_flat[idx]
        sub_full = df[
            (np.isclose(df["target_mv"], target_mv)) & (df["mode"] == "full")
        ].sort_values("sample_idx")
        sub_passive = df[
            (np.isclose(df["target_mv"], target_mv)) & (df["mode"] == "epsp_passive")
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
        ax.axvline(x=DUR1_MS, color="grey", linestyle=":", alpha=0.5)
        ax.axvline(x=DUR1_MS + DUR2_MS, color="grey", linestyle=":", alpha=0.5)
        ax.set_title(f"target = {target_mv:.0f} mV")
        ax.set_xlabel("time (ms)")
        ax.set_ylabel("V_soma (mV)")
        ax.grid(visible=True, alpha=0.3)
        if idx == 0:
            ax.legend(loc="lower right", fontsize=8)
    for idx in range(len(TARGET_MV_VALUES), len(axes_flat)):
        axes_flat[idx].axis("off")
    fig.suptitle(
        "t0063: SEClamp voltage steps from -65 mV to {-60..-10} mV for 200 ms; HH on vs HH off",
        fontsize=13,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(VOLTAGE_GRID_PNG, dpi=110)
    plt.close(fig)
    print(f"[t0063] wrote {VOLTAGE_GRID_PNG}", flush=True)


def _plot_iclamp_grid(*, df: pd.DataFrame) -> None:
    """Plot SEClamp current with y-axis zoomed to exclude capacitive transients.

    Two y-axes: top row shows the FULL-vs-PASSIVE traces (zoomed); bottom row shows the
    difference (FULL - PASSIVE) which is the pure HH contribution.
    """
    n: int = len(TARGET_MV_VALUES)
    n_cols: int = 3
    n_rows: int = (n + n_cols - 1) // n_cols
    fig, axes = plt.subplots(
        nrows=n_rows * 2,
        ncols=n_cols,
        figsize=(n_cols * 4.5, n_rows * 5.5),
        sharex=True,
    )
    for idx, target_mv in enumerate(TARGET_MV_VALUES):
        row_top: int = (idx // n_cols) * 2
        row_bot: int = row_top + 1
        col: int = idx % n_cols
        ax_top = axes[row_top, col]
        ax_bot = axes[row_bot, col]

        sub_full = df[
            (np.isclose(df["target_mv"], target_mv)) & (df["mode"] == "full")
        ].sort_values("sample_idx")
        sub_passive = df[
            (np.isclose(df["target_mv"], target_mv)) & (df["mode"] == "epsp_passive")
        ].sort_values("sample_idx")
        t_full: np.ndarray = sub_full["t_ms"].to_numpy()
        i_full: np.ndarray = sub_full["i_clamp_na"].to_numpy()
        t_passive: np.ndarray = sub_passive["t_ms"].to_numpy()
        i_passive: np.ndarray = sub_passive["i_clamp_na"].to_numpy()

        # Top panel: clamp current zoomed to show steady state during step.
        # Compute zoom limits separately for each trace (CVODE step size differs).
        zoom_full: np.ndarray = (t_full > 60.0) & (t_full < 250.0)
        zoom_passive: np.ndarray = (t_passive > 60.0) & (t_passive < 250.0)
        if np.any(zoom_full) and np.any(zoom_passive):
            i_min: float = float(min(np.min(i_full[zoom_full]), np.min(i_passive[zoom_passive])))
            i_max: float = float(max(np.max(i_full[zoom_full]), np.max(i_passive[zoom_passive])))
            margin: float = max(50.0, (i_max - i_min) * 0.1)
            ax_top.set_ylim(i_min - margin, i_max + margin)
        ax_top.plot(t_full, i_full, color="C3", linestyle="-", linewidth=1.5, label="FULL (HH on)")
        ax_top.plot(
            t_passive,
            i_passive,
            color="C0",
            linestyle="--",
            linewidth=1.2,
            label="EPSP_PASSIVE (HH off)",
        )
        ax_top.axvline(x=DUR1_MS, color="grey", linestyle=":", alpha=0.5)
        ax_top.axvline(x=DUR1_MS + DUR2_MS, color="grey", linestyle=":", alpha=0.5)
        ax_top.set_title(f"target = {target_mv:.0f} mV  (zoomed I_clamp)")
        ax_top.set_ylabel("I_clamp (nA)")
        ax_top.grid(visible=True, alpha=0.3)
        if idx == 0:
            ax_top.legend(loc="upper right", fontsize=7)

        # Bottom panel: FULL - PASSIVE difference = pure HH contribution.
        # Need to align time grids; CVODE gives different sample times.
        if len(t_full) > 0 and len(t_passive) > 0:
            common_t: np.ndarray = np.linspace(0.0, t_full[-1], 1500)
            i_full_interp: np.ndarray = np.interp(common_t, t_full, i_full)
            i_passive_interp: np.ndarray = np.interp(common_t, t_passive, i_passive)
            diff: np.ndarray = i_full_interp - i_passive_interp
            # Zoom the diff plot too — exclude the brief capacitive transient mismatch.
            diff_mask: np.ndarray = (common_t > 55.0) & (common_t < 250.0)
            if np.any(diff_mask):
                d_min: float = float(np.min(diff[diff_mask]))
                d_max: float = float(np.max(diff[diff_mask]))
                margin = max(20.0, (d_max - d_min) * 0.15)
                ax_bot.set_ylim(d_min - margin, d_max + margin)
            ax_bot.plot(common_t, diff, color="C2", linewidth=1.4)
            ax_bot.axvline(x=DUR1_MS, color="grey", linestyle=":", alpha=0.5)
            ax_bot.axvline(x=DUR1_MS + DUR2_MS, color="grey", linestyle=":", alpha=0.5)
            ax_bot.axhline(y=0, color="black", linewidth=0.5)
        ax_bot.set_xlabel("time (ms)")
        ax_bot.set_ylabel("I_HH = FULL - PASSIVE (nA)")
        ax_bot.grid(visible=True, alpha=0.3)

    fig.suptitle(
        "t0063: SEClamp clamp current; top = zoomed FULL vs PASSIVE, bottom = pure HH (difference)",
        fontsize=13,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.97))
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(CLAMP_CURRENT_GRID_PNG, dpi=110)
    plt.close(fig)
    print(f"[t0063] wrote {CLAMP_CURRENT_GRID_PNG}", flush=True)


def main() -> None:
    df: pd.DataFrame = _load_traces()
    _plot_vm_grid(df=df)
    _plot_iclamp_grid(df=df)


if __name__ == "__main__":
    main()
