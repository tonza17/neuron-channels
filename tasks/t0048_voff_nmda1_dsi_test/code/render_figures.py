"""Render the two PNG comparison artifacts.

Outputs:
    * ``DSI_OVERLAY_PNG``               — single panel: x = gNMDA in nS, y = DSI; two
      curves (Voff = 0 from t0047, Voff = 1 from this task) plus a horizontal
      paper-claim reference line at 0.30 with a +/- 0.05 band.
    * ``CONDUCTANCE_COMPARISON_PNG``    — bar chart at b2gnmda = 0.5 nS comparing the
      mean per-class summed peak conductance (NMDA / AMPA / GABA) for Voff = 0 (t0047)
      vs Voff = 1 (this task), separated by direction (PD / ND).
"""

from __future__ import annotations

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tasks.t0048_voff_nmda1_dsi_test.code.constants import (
    B2GNMDA_GRID_NS,
    COL_DIRECTION,
    COL_PEAK_G_AMPA_SUMMED_NS,
    COL_PEAK_G_NMDA_SUMMED_NS,
    COL_PEAK_G_SACINHIB_SUMMED_NS,
    DIRECTION_ND_LABEL,
    DIRECTION_PD_LABEL,
    DSI_FIG3F_TOLERANCE,
    DSI_PAPER_FIG3F_TARGET,
)
from tasks.t0048_voff_nmda1_dsi_test.code.paths import (
    CONDUCTANCE_COMPARISON_PNG,
    DSI_BY_GNMDA_VOFF0_FROM_T0047_JSON,
    DSI_BY_GNMDA_VOFF1_JSON,
    DSI_OVERLAY_PNG,
    GNMDA_TRIALS_VOFF1_CSV,
    RESULTS_IMAGES_DIR,
    T0047_GNMDA_TRIALS_CSV,
)

_GNMDA_FOR_CONDUCTANCE_PANEL_NS: float = 0.5
_DSI_FIG_HEIGHT_INCHES: float = 5.0
_DSI_FIG_WIDTH_INCHES: float = 7.5
_BAR_FIG_HEIGHT_INCHES: float = 5.5
_BAR_FIG_WIDTH_INCHES: float = 9.0
_DPI: int = 120


def _load_dsi_dict(*, path: str) -> dict[float, float]:
    with open(file=path, encoding="utf-8") as fh:
        raw: dict[str, float | None] = json.load(fh)
    out: dict[float, float] = {}
    for key, value in raw.items():
        assert value is not None, f"None DSI value at {path} key={key}"
        out[float(key)] = float(value)
    return out


def _render_dsi_overlay(
    *,
    voff0: dict[float, float],
    voff1: dict[float, float],
    out_path: str,
) -> None:
    grid: list[float] = sorted(set(voff0.keys()) | set(voff1.keys()))
    voff0_y: list[float] = [voff0[g] for g in grid]
    voff1_y: list[float] = [voff1[g] for g in grid]

    fig, ax = plt.subplots(
        figsize=(_DSI_FIG_WIDTH_INCHES, _DSI_FIG_HEIGHT_INCHES),
    )
    ax.plot(
        grid,
        voff0_y,
        marker="o",
        linewidth=2.0,
        color="#1f77b4",
        label="Voff_bipNMDA = 0 (t0047 baseline)",
    )
    ax.plot(
        grid,
        voff1_y,
        marker="s",
        linewidth=2.0,
        color="#d62728",
        label="Voff_bipNMDA = 1 (this task)",
    )
    ax.axhline(
        DSI_PAPER_FIG3F_TARGET,
        color="grey",
        linestyle="--",
        linewidth=1.5,
        label=f"paper claim = {DSI_PAPER_FIG3F_TARGET:.2f}",
    )
    ax.axhspan(
        DSI_PAPER_FIG3F_TARGET - DSI_FIG3F_TOLERANCE,
        DSI_PAPER_FIG3F_TARGET + DSI_FIG3F_TOLERANCE,
        color="grey",
        alpha=0.15,
        label=f"+/- {DSI_FIG3F_TOLERANCE:.2f} band",
    )
    ax.set_xlabel("b2gnmda (nS)")
    ax.set_ylabel("DSI = (PD - ND) / (PD + ND)")
    ax.set_title("DSI vs gNMDA: Voff = 0 (t0047) vs Voff = 1 (t0048) vs paper")
    ax.set_xticks(grid)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=_DPI)
    plt.close(fig)
    print(f"[render_figures] wrote {out_path}", flush=True)


def _conductance_means_at_gnmda(
    *,
    df: pd.DataFrame,
    b2gnmda_ns: float,
) -> dict[tuple[str, str], float]:
    """Return {(channel_label, direction_label): mean peak summed g (nS)}."""
    cell: pd.DataFrame = df[df["b2gnmda_ns"].round(6) == round(float(b2gnmda_ns), 6)]
    out: dict[tuple[str, str], float] = {}
    for chan_label, col in (
        ("NMDA", COL_PEAK_G_NMDA_SUMMED_NS),
        ("AMPA", COL_PEAK_G_AMPA_SUMMED_NS),
        ("GABA", COL_PEAK_G_SACINHIB_SUMMED_NS),
    ):
        for dir_label in (DIRECTION_PD_LABEL, DIRECTION_ND_LABEL):
            sub: pd.Series = cell[cell[COL_DIRECTION] == dir_label][col]
            out[(chan_label, dir_label)] = float(sub.astype(float).mean())
    return out


def _render_conductance_comparison(
    *,
    voff0_means: dict[tuple[str, str], float],
    voff1_means: dict[tuple[str, str], float],
    b2gnmda_ns: float,
    out_path: str,
) -> None:
    channels: tuple[str, ...] = ("NMDA", "AMPA", "GABA")
    n_channels: int = len(channels)
    # Four bar groups per channel: (Voff0,PD) (Voff0,ND) (Voff1,PD) (Voff1,ND).
    bar_width: float = 0.18
    fig, ax = plt.subplots(
        figsize=(_BAR_FIG_WIDTH_INCHES, _BAR_FIG_HEIGHT_INCHES),
    )
    centres: np.ndarray = np.arange(n_channels, dtype=np.float64)
    offsets: tuple[float, ...] = (
        -1.5 * bar_width,
        -0.5 * bar_width,
        0.5 * bar_width,
        1.5 * bar_width,
    )
    series: tuple[tuple[str, str, str, str, dict[tuple[str, str], float]], ...] = (
        ("Voff = 0 PD (t0047)", "#1f77b4", "PD", "//", voff0_means),
        ("Voff = 0 ND (t0047)", "#aec7e8", "ND", "//", voff0_means),
        ("Voff = 1 PD (this task)", "#d62728", "PD", "..", voff1_means),
        ("Voff = 1 ND (this task)", "#ff9896", "ND", "..", voff1_means),
    )
    for offset, (label, color, dir_label, hatch, means) in zip(
        offsets,
        series,
        strict=True,
    ):
        heights: list[float] = [means[(chan, dir_label)] for chan in channels]
        ax.bar(
            centres + offset,
            heights,
            width=bar_width,
            color=color,
            edgecolor="black",
            linewidth=0.6,
            hatch=hatch,
            label=label,
        )

    ax.set_xticks(centres)
    ax.set_xticklabels(list(channels))
    ax.set_xlabel("Synapse class")
    ax.set_ylabel("Mean peak summed conductance (nS)")
    ax.set_title(
        f"Per-class summed peak conductance at b2gnmda = {b2gnmda_ns:.2f} nS (mean over 4 trials)",
    )
    ax.legend(loc="best", fontsize="small")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=_DPI)
    plt.close(fig)
    print(f"[render_figures] wrote {out_path}", flush=True)


def main() -> int:
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    voff0: dict[float, float] = _load_dsi_dict(
        path=str(DSI_BY_GNMDA_VOFF0_FROM_T0047_JSON),
    )
    voff1: dict[float, float] = _load_dsi_dict(
        path=str(DSI_BY_GNMDA_VOFF1_JSON),
    )
    expected_grid: set[float] = {float(g) for g in B2GNMDA_GRID_NS}
    assert set(voff0.keys()) == expected_grid, (
        f"Voff=0 DSI grid mismatch: got {sorted(voff0.keys())}"
    )
    assert set(voff1.keys()) == expected_grid, (
        f"Voff=1 DSI grid mismatch: got {sorted(voff1.keys())}"
    )

    _render_dsi_overlay(
        voff0=voff0,
        voff1=voff1,
        out_path=str(DSI_OVERLAY_PNG),
    )

    df_voff0: pd.DataFrame = pd.read_csv(T0047_GNMDA_TRIALS_CSV)
    df_voff1: pd.DataFrame = pd.read_csv(GNMDA_TRIALS_VOFF1_CSV)
    voff0_means: dict[tuple[str, str], float] = _conductance_means_at_gnmda(
        df=df_voff0,
        b2gnmda_ns=_GNMDA_FOR_CONDUCTANCE_PANEL_NS,
    )
    voff1_means: dict[tuple[str, str], float] = _conductance_means_at_gnmda(
        df=df_voff1,
        b2gnmda_ns=_GNMDA_FOR_CONDUCTANCE_PANEL_NS,
    )
    _render_conductance_comparison(
        voff0_means=voff0_means,
        voff1_means=voff1_means,
        b2gnmda_ns=_GNMDA_FOR_CONDUCTANCE_PANEL_NS,
        out_path=str(CONDUCTANCE_COMPARISON_PNG),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
