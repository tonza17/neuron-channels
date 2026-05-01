"""Plot t0069 AIS-localised channel sweep results, including soma-vs-AIS comparison."""

from __future__ import annotations

import json
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0069_t0067_ais_localised_channel_sweep.code.constants import (
    CHANNEL_DEFS,
)
from tasks.t0069_t0067_ais_localised_channel_sweep.code.paths import (
    DSI_BY_CONDITION_JSON,
    DSI_PNG,
    FIRING_RATE_PNG,
    IMAGES_DIR,
    SOMA_VS_AIS_PNG,
    T0067_DSI_BY_CONDITION_JSON,
)

DENSITY_LABELS_ORDER: tuple[str, ...] = ("low", "med", "high")


def _load_summary(path: str) -> list[dict[str, Any]]:
    with open(file=path, encoding="utf-8") as f:
        return list(json.load(f)["conditions"])


def _baseline(summary: list[dict[str, Any]], cid: str) -> dict[str, Any]:
    for s in summary:
        if s["condition_id"] == cid:
            return s
    raise ValueError(f"No condition {cid} found")


def _channel_rows(
    *, summary: list[dict[str, Any]], suffix: str, suffix_extra: str = ""
) -> list[dict[str, Any]]:
    short = suffix.replace("t67", "")
    if suffix_extra:
        rows = [
            s
            for s in summary
            if s["condition_id"].startswith(f"{short}_")
            and s["condition_id"].endswith(suffix_extra)
        ]
    else:
        rows = [s for s in summary if s["condition_id"].startswith(f"{short}_")]
    rows.sort(key=lambda s: DENSITY_LABELS_ORDER.index(s["density_label"]))
    return rows


def _plot_firing_rate(*, summary: list[dict[str, Any]]) -> None:
    baseline = _baseline(summary, "baseline_ais")
    fig, axes = plt.subplots(1, 5, figsize=(18, 4), dpi=120, sharey=True)
    for ax, ch in zip(axes, CHANNEL_DEFS, strict=True):
        rows = _channel_rows(summary=summary, suffix=ch.suffix, suffix_extra="_ais")
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
            label="baseline_ais PD",
        )
        ax.axhline(
            baseline["spike_count_nd_mean"],
            color="#d62728",
            linestyle="--",
            alpha=0.5,
            label="baseline_ais ND",
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
    fig.suptitle("AIS-localised channels: FULL-mode firing rate vs density", y=1.02)
    fig.tight_layout()
    fig.savefig(str(FIRING_RATE_PNG), bbox_inches="tight")
    plt.close(fig)


def _plot_dsi(*, summary: list[dict[str, Any]]) -> None:
    baseline = _baseline(summary, "baseline_ais")
    fig, axes = plt.subplots(1, 5, figsize=(18, 4), dpi=120, sharey=True)
    for ax, ch in zip(axes, CHANNEL_DEFS, strict=True):
        rows = _channel_rows(summary=summary, suffix=ch.suffix, suffix_extra="_ais")
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
            label=f"baseline_ais ({baseline['dsi']:.2f})",
        )
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_xlabel("density")
        ax.set_ylim(-0.3, 1.1)
        ax.set_title(ch.kind.value)
        ax.grid(alpha=0.3)
        if ch == CHANNEL_DEFS[0]:
            ax.set_ylabel("DSI")
        if ch == CHANNEL_DEFS[-1]:
            ax.legend(loc="best", fontsize=8)
    fig.suptitle("AIS-localised channels: DSI vs density", y=1.02)
    fig.tight_layout()
    fig.savefig(str(DSI_PNG), bbox_inches="tight")
    plt.close(fig)


def _plot_soma_vs_ais(
    *, t69_summary: list[dict[str, Any]], t67_summary: list[dict[str, Any]]
) -> None:
    """Side-by-side bar chart: per-channel ΔDSI from baseline at low/med/high for soma vs AIS."""
    t69_baseline = _baseline(t69_summary, "baseline_ais")
    t67_baseline = _baseline(t67_summary, "baseline")
    fig, axes = plt.subplots(1, 5, figsize=(18, 4.5), dpi=120, sharey=True)
    bar_width = 0.35
    for ax, ch in zip(axes, CHANNEL_DEFS, strict=True):
        soma_rows = [
            s
            for s in t67_summary
            if s["condition_id"].startswith(f"{ch.suffix.replace('t67', '')}_")
            and not s["condition_id"].endswith("_ais")
        ]
        ais_rows = _channel_rows(summary=t69_summary, suffix=ch.suffix, suffix_extra="_ais")
        soma_rows.sort(key=lambda s: DENSITY_LABELS_ORDER.index(s["density_label"]))
        ais_rows.sort(key=lambda s: DENSITY_LABELS_ORDER.index(s["density_label"]))
        if not soma_rows or not ais_rows:
            ax.set_title(f"{ch.kind.value} (no data)")
            continue
        x = np.arange(len(ais_rows))
        labels = [r["density_label"] for r in ais_rows]
        soma_deltas = [r["dsi"] - t67_baseline["dsi"] for r in soma_rows]
        ais_deltas = [r["dsi"] - t69_baseline["dsi"] for r in ais_rows]
        ax.bar(x - bar_width / 2, soma_deltas, bar_width, color="#ff7f0e", label="soma (t0067)")
        ax.bar(x + bar_width / 2, ais_deltas, bar_width, color="#2ca02c", label="AIS (t0069)")
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_xlabel("density")
        ax.set_title(ch.kind.value)
        ax.grid(alpha=0.3, axis="y")
        if ch == CHANNEL_DEFS[0]:
            ax.set_ylabel("ΔDSI (vs respective baseline)")
        if ch == CHANNEL_DEFS[-1]:
            ax.legend(loc="best", fontsize=8)
    t67_dsi = t67_baseline["dsi"]
    t69_dsi = t69_baseline["dsi"]
    title = (
        f"Soma vs AIS insertion: ΔDSI from each task's own baseline "
        f"(t0067 = {t67_dsi:.2f}; t0069 baseline_ais = {t69_dsi:.2f})"
    )
    fig.suptitle(title, y=1.02)
    fig.tight_layout()
    fig.savefig(str(SOMA_VS_AIS_PNG), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    t69_summary = _load_summary(str(DSI_BY_CONDITION_JSON))
    t67_summary = _load_summary(str(T0067_DSI_BY_CONDITION_JSON))
    print(f"t0069 conditions: {len(t69_summary)}; t0067 conditions: {len(t67_summary)}")
    _plot_firing_rate(summary=t69_summary)
    _plot_dsi(summary=t69_summary)
    _plot_soma_vs_ais(t69_summary=t69_summary, t67_summary=t67_summary)
    print("Wrote 3 PNGs to results/images/.")


if __name__ == "__main__":
    main()
