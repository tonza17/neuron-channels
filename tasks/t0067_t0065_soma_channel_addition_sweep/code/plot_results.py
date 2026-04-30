"""Render the t0067 channel-density sweep plots from dsi_by_condition.json."""

from __future__ import annotations

import json
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0067_t0065_soma_channel_addition_sweep.code.constants import (
    CHANNEL_DEFS,
)
from tasks.t0067_t0065_soma_channel_addition_sweep.code.paths import (
    DSI_BY_CONDITION_JSON,
    DSI_PNG,
    FIRING_RATE_PNG,
    HEATMAP_PNG,
    IMAGES_DIR,
)

DENSITY_LABELS_ORDER: tuple[str, ...] = ("low", "med", "high")


def _load_summary() -> list[dict[str, Any]]:
    with open(file=DSI_BY_CONDITION_JSON, encoding="utf-8") as f:
        return list(json.load(f)["conditions"])


def _baseline(summary: list[dict[str, Any]]) -> dict[str, Any]:
    for s in summary:
        if s["condition_id"] == "baseline":
            return s
    raise ValueError("No baseline condition found in summary")


def _channel_rows(*, summary: list[dict[str, Any]], suffix: str) -> list[dict[str, Any]]:
    short = suffix.replace("t67", "")
    rows = [s for s in summary if s["condition_id"].startswith(f"{short}_")]
    rows.sort(key=lambda s: DENSITY_LABELS_ORDER.index(s["density_label"]))
    return rows


def _plot_firing_rate(*, summary: list[dict[str, Any]]) -> None:
    baseline = _baseline(summary)
    fig, axes = plt.subplots(1, 5, figsize=(18, 4), dpi=120, sharey=True)
    for ax, ch in zip(axes, CHANNEL_DEFS, strict=True):
        rows = _channel_rows(summary=summary, suffix=ch.suffix)
        if not rows:
            ax.set_title(f"{ch.kind.value} (no data)")
            continue
        x = np.arange(len(rows))
        labels = [r["density_label"] for r in rows]
        pd_means = [r["spike_count_pd_mean"] for r in rows]
        pd_sds = [r["spike_count_pd_sd"] for r in rows]
        nd_means = [r["spike_count_nd_mean"] for r in rows]
        nd_sds = [r["spike_count_nd_sd"] for r in rows]
        ax.errorbar(
            x - 0.1,
            pd_means,
            yerr=pd_sds,
            fmt="o-",
            color="#1f77b4",
            linewidth=2,
            capsize=4,
            label="PD",
        )
        ax.errorbar(
            x + 0.1,
            nd_means,
            yerr=nd_sds,
            fmt="s-",
            color="#d62728",
            linewidth=2,
            capsize=4,
            label="ND",
        )
        ax.axhline(
            baseline["spike_count_pd_mean"],
            color="#1f77b4",
            linestyle="--",
            alpha=0.5,
            label="baseline PD",
        )
        ax.axhline(
            baseline["spike_count_nd_mean"],
            color="#d62728",
            linestyle="--",
            alpha=0.5,
            label="baseline ND",
        )
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_xlabel("density")
        ax.set_title(ch.kind.value)
        ax.grid(alpha=0.3)
        if ch == CHANNEL_DEFS[0]:
            ax.set_ylabel("Spikes / trial (mean ± SD, n=5)")
        if ch == CHANNEL_DEFS[-1]:
            ax.legend(loc="best", fontsize=8)
    fig.suptitle("FULL-mode firing rate vs added-channel density", y=1.02)
    fig.tight_layout()
    fig.savefig(str(FIRING_RATE_PNG), bbox_inches="tight")
    plt.close(fig)


def _plot_dsi(*, summary: list[dict[str, Any]]) -> None:
    baseline = _baseline(summary)
    fig, axes = plt.subplots(1, 5, figsize=(18, 4), dpi=120, sharey=True)
    for ax, ch in zip(axes, CHANNEL_DEFS, strict=True):
        rows = _channel_rows(summary=summary, suffix=ch.suffix)
        if not rows:
            ax.set_title(f"{ch.kind.value} (no data)")
            continue
        x = np.arange(len(rows))
        labels = [r["density_label"] for r in rows]
        dsis = [r["dsi"] for r in rows]
        ax.plot(x, dsis, "o-", color="#2ca02c", linewidth=2, markersize=8, label="DSI")
        ax.axhline(
            baseline["dsi"],
            color="black",
            linestyle="--",
            alpha=0.6,
            label=f"baseline ({baseline['dsi']:.2f})",
        )
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_xlabel("density")
        ax.set_ylim(-0.1, 1.1)
        ax.set_title(ch.kind.value)
        ax.grid(alpha=0.3)
        if ch == CHANNEL_DEFS[0]:
            ax.set_ylabel("DSI = (PD - ND) / (PD + ND)")
        if ch == CHANNEL_DEFS[-1]:
            ax.legend(loc="best", fontsize=8)
    fig.suptitle("Direction Selectivity Index vs added-channel density", y=1.02)
    fig.tight_layout()
    fig.savefig(str(DSI_PNG), bbox_inches="tight")
    plt.close(fig)


def _plot_heatmap(*, summary: list[dict[str, Any]]) -> None:
    n_channels = len(CHANNEL_DEFS)
    n_densities = len(DENSITY_LABELS_ORDER)
    pd_grid = np.full((n_channels, n_densities), np.nan)
    nd_grid = np.full((n_channels, n_densities), np.nan)
    channel_labels = [ch.kind.value for ch in CHANNEL_DEFS]
    for i, ch in enumerate(CHANNEL_DEFS):
        rows = _channel_rows(summary=summary, suffix=ch.suffix)
        for r in rows:
            j = DENSITY_LABELS_ORDER.index(r["density_label"])
            pd_grid[i, j] = r["spike_count_pd_mean"]
            nd_grid[i, j] = r["spike_count_nd_mean"]
    baseline = _baseline(summary)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=120)
    for ax, grid, title, cmap in [
        (
            axes[0],
            pd_grid,
            f"PD spike count (baseline = {baseline['spike_count_pd_mean']:.1f})",
            "Reds",
        ),
        (
            axes[1],
            nd_grid,
            f"ND spike count (baseline = {baseline['spike_count_nd_mean']:.1f})",
            "Blues",
        ),
    ]:
        im = ax.imshow(grid, cmap=cmap, aspect="auto")
        ax.set_xticks(range(n_densities))
        ax.set_xticklabels(DENSITY_LABELS_ORDER)
        ax.set_yticks(range(n_channels))
        ax.set_yticklabels(channel_labels)
        ax.set_xlabel("Density")
        ax.set_title(title)
        for i in range(n_channels):
            for j in range(n_densities):
                val = grid[i, j]
                txt_color = "white" if val > np.nanmax(grid) * 0.5 else "black"
                ax.text(j, i, f"{val:.1f}", ha="center", va="center", color=txt_color, fontsize=10)
        plt.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(str(HEATMAP_PNG), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    summary = _load_summary()
    print(f"Loaded {len(summary)} conditions from {DSI_BY_CONDITION_JSON}")
    _plot_firing_rate(summary=summary)
    _plot_dsi(summary=summary)
    _plot_heatmap(summary=summary)
    print("Wrote 3 PNGs to results/images/.")


if __name__ == "__main__":
    main()
