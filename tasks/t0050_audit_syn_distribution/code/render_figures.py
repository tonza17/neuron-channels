"""Render the three diagnostic PNGs for the t0050 audit.

* ``syn_x_hist_per_channel.png`` — three subplots, one per channel; x-coordinate histogram with
  soma_x midline (vertical dashed line) and tick marks at the alternative midlines.
* ``syn_radial_distance_per_channel.png`` — three subplots, two overlaid histograms (side_a vs
  side_b under the soma_x midline) per channel.
* ``syn_count_pd_vs_nd_per_channel.png`` — single grouped bar chart (3 channels x 2 sides) using
  the soma_x midline.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from tasks.t0050_audit_syn_distribution.code import paths
from tasks.t0050_audit_syn_distribution.code.compute_spatial_stats import SOMA_X_UM
from tasks.t0050_audit_syn_distribution.code.constants import (
    CHANNEL_DISPLAY_NAMES,
    CHANNEL_LOCX_COLUMNS,
    COLUMN_BIP_LOCX_UM,
    COLUMN_RADIAL_DISTANCE_UM,
    MIDLINE_KIND_SOMA_X,
    ChannelKind,
)

HIST_BINS: int = 30
DPI: int = 150
SIDE_A_COLOUR: str = "#1f77b4"  # blue
SIDE_B_COLOUR: str = "#d62728"  # red


def _load_stats() -> pd.DataFrame:
    return pd.read_csv(filepath_or_buffer=paths.PER_CHANNEL_DENSITY_STATS_CSV)


def _load_coords() -> pd.DataFrame:
    return pd.read_csv(filepath_or_buffer=paths.SYNAPSE_COORDINATES_CSV)


def _stats_row_for(*, stats: pd.DataFrame, channel: ChannelKind) -> pd.Series:
    mask: pd.Series = (stats["channel"] == channel.value) & (
        stats["midline_kind"] == MIDLINE_KIND_SOMA_X
    )
    return stats[mask].iloc[0]


def render_x_histograms(*, coords: pd.DataFrame, stats: pd.DataFrame) -> None:
    fig: Figure
    axes: list[Axes]
    fig, axes = plt.subplots(
        nrows=3,
        ncols=1,
        figsize=(8.0, 9.0),
        sharex=True,
    )

    bipsyn_median: float = float(coords[COLUMN_BIP_LOCX_UM].median())

    for ax, channel in zip(axes, ChannelKind, strict=True):
        col: str = CHANNEL_LOCX_COLUMNS[channel]
        values: pd.Series = coords[col]
        ax.hist(
            values,
            bins=HIST_BINS,
            color="#7f7f7f",
            edgecolor="black",
            alpha=0.85,
        )

        # Midline markers.
        ax.axvline(SOMA_X_UM, color="black", linestyle="--", linewidth=1.5, label="soma_x")
        ax.axvline(0.0, color="green", linestyle=":", linewidth=1.0, label="x = 0")
        ax.axvline(
            bipsyn_median,
            color="purple",
            linestyle="-.",
            linewidth=1.0,
            label="BIPsyn locx median",
        )

        # Title with per-channel ratio under soma_x midline.
        row: pd.Series = _stats_row_for(stats=stats, channel=channel)
        ratio: float = float(row["count_ratio_side_a_over_b"])
        n_a: int = int(row["count_side_a"])
        n_b: int = int(row["count_side_b"])
        title: str = (
            f"{CHANNEL_DISPLAY_NAMES[channel]}  |  soma_x split: "
            f"side_a={n_a}, side_b={n_b}, ratio={ratio:.3f}"
        )
        ax.set_title(label=title, fontsize=10)
        ax.set_ylabel(ylabel="Synapse count")
        ax.legend(loc="upper right", fontsize=8)

    axes[-1].set_xlabel(xlabel="Synapse x-coordinate (μm)")
    fig.suptitle(
        t=("Per-channel x-coordinate histograms (deposited Poleg-Polsky 2016 DSGC, n=282)"),
        fontsize=11,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.97))
    fig.savefig(paths.SYN_X_HIST_PNG, dpi=DPI, bbox_inches="tight")
    plt.close(fig=fig)
    print(f"[figures] Wrote {paths.SYN_X_HIST_PNG}", flush=True)


def render_radial_histograms(*, coords: pd.DataFrame, stats: pd.DataFrame) -> None:
    fig: Figure
    axes: list[Axes]
    fig, axes = plt.subplots(
        nrows=3,
        ncols=1,
        figsize=(8.0, 9.0),
        sharex=True,
    )

    for ax, channel in zip(axes, ChannelKind, strict=True):
        locx_col: str = CHANNEL_LOCX_COLUMNS[channel]
        side_a_mask: pd.Series = coords[locx_col] < SOMA_X_UM
        side_b_mask: pd.Series = coords[locx_col] >= SOMA_X_UM

        rad_a: pd.Series = coords[side_a_mask][COLUMN_RADIAL_DISTANCE_UM]
        rad_b: pd.Series = coords[side_b_mask][COLUMN_RADIAL_DISTANCE_UM]

        ax.hist(
            rad_a,
            bins=HIST_BINS,
            color=SIDE_A_COLOUR,
            edgecolor="black",
            alpha=0.6,
            label=f"side_a (x < x_soma), n={len(rad_a)}",
        )
        ax.hist(
            rad_b,
            bins=HIST_BINS,
            color=SIDE_B_COLOUR,
            edgecolor="black",
            alpha=0.6,
            label=f"side_b (x >= x_soma), n={len(rad_b)}",
        )

        row: pd.Series = _stats_row_for(stats=stats, channel=channel)
        mean_a: float = float(row["mean_radial_distance_side_a_um"])
        sd_a: float = float(row["sd_radial_distance_side_a_um"])
        mean_b: float = float(row["mean_radial_distance_side_b_um"])
        sd_b: float = float(row["sd_radial_distance_side_b_um"])
        title: str = (
            f"{CHANNEL_DISPLAY_NAMES[channel]}  |  "
            f"side_a {mean_a:.1f}±{sd_a:.1f} μm, "
            f"side_b {mean_b:.1f}±{sd_b:.1f} μm"
        )
        ax.set_title(label=title, fontsize=10)
        ax.set_ylabel(ylabel="Synapse count")
        ax.legend(loc="upper right", fontsize=8)

    axes[-1].set_xlabel(xlabel="Radial distance from soma (μm)")
    fig.suptitle(
        t=("Per-channel radial-distance histograms by soma_x midline side"),
        fontsize=11,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.97))
    fig.savefig(paths.SYN_RADIAL_HIST_PNG, dpi=DPI, bbox_inches="tight")
    plt.close(fig=fig)
    print(f"[figures] Wrote {paths.SYN_RADIAL_HIST_PNG}", flush=True)


def render_count_bar(*, stats: pd.DataFrame) -> None:
    fig: Figure
    ax: Axes
    fig, ax = plt.subplots(figsize=(8.0, 5.5))

    channels: list[ChannelKind] = list(ChannelKind)
    n_chans: int = len(channels)
    bar_width: float = 0.35
    indices: list[float] = list(range(n_chans))

    side_a_counts: list[int] = []
    side_b_counts: list[int] = []
    for channel in channels:
        row: pd.Series = _stats_row_for(stats=stats, channel=channel)
        side_a_counts.append(int(row["count_side_a"]))
        side_b_counts.append(int(row["count_side_b"]))

    x_a: list[float] = [i - bar_width / 2 for i in indices]
    x_b: list[float] = [i + bar_width / 2 for i in indices]

    bars_a = ax.bar(
        x_a,
        side_a_counts,
        width=bar_width,
        color=SIDE_A_COLOUR,
        edgecolor="black",
        label="side_a (x < x_soma)",
    )
    bars_b = ax.bar(
        x_b,
        side_b_counts,
        width=bar_width,
        color=SIDE_B_COLOUR,
        edgecolor="black",
        label="side_b (x >= x_soma)",
    )

    for bar in (*bars_a, *bars_b):
        height: float = bar.get_height()
        ax.text(
            x=bar.get_x() + bar.get_width() / 2,
            y=height + 1,
            s=f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax.set_xticks(indices)
    ax.set_xticklabels([CHANNEL_DISPLAY_NAMES[c] for c in channels], rotation=10)
    ax.set_ylabel(ylabel="Synapse count")
    ax.set_title(
        label="Per-channel synapse counts by side (midline = x_soma = 104.576 μm)",
        fontsize=11,
    )
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.tight_layout()
    fig.savefig(paths.SYN_COUNT_BAR_PNG, dpi=DPI, bbox_inches="tight")
    plt.close(fig=fig)
    print(f"[figures] Wrote {paths.SYN_COUNT_BAR_PNG}", flush=True)


def main() -> None:
    coords: pd.DataFrame = _load_coords()
    stats: pd.DataFrame = _load_stats()
    render_x_histograms(coords=coords, stats=stats)
    render_radial_histograms(coords=coords, stats=stats)
    render_count_bar(stats=stats)


if __name__ == "__main__":
    main()
