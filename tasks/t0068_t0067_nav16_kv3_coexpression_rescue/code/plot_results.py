"""Plot the t0068 Nav1.6+Kv3 co-expression rescue results."""

from __future__ import annotations

import json
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0068_t0067_nav16_kv3_coexpression_rescue.code.paths import (
    DSI_BY_CONDITION_JSON,
    DSI_RESCUE_PNG,
    FIRING_RATE_RESCUE_PNG,
    IMAGES_DIR,
)

KV3_DENSITY_LABELS: tuple[str, ...] = ("0", "7", "20", "60")  # mS/cm² ticks
KV3_DENSITY_VALUES: tuple[float, ...] = (0.0, 7.0, 20.0, 60.0)


def _load_summary() -> list[dict[str, Any]]:
    with open(file=DSI_BY_CONDITION_JSON, encoding="utf-8") as f:
        return list(json.load(f)["conditions"])


def _baseline(summary: list[dict[str, Any]]) -> dict[str, Any]:
    for s in summary:
        if s["condition_id"] == "baseline":
            return s
    raise ValueError("No baseline condition")


def _rows_for_nav16(*, summary: list[dict[str, Any]], nav16_mS: float) -> list[dict[str, Any]]:
    """Get the 4 rows (Kv3 = 0, 7, 20, 60) for a given Nav1.6 density level."""
    rows = [
        s
        for s in summary
        if abs(s["nav16_mS_cm2"] - nav16_mS) < 1e-6 and s["condition_id"] != "baseline"
    ]
    rows.sort(key=lambda s: s["kv3_mS_cm2"])
    return rows


def _plot_dsi_rescue(*, summary: list[dict[str, Any]]) -> None:
    baseline = _baseline(summary)
    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
    for nav16_mS, color, label in [
        (30.0, "#1f77b4", "Nav1.6 = 30 mS/cm² (med)"),
        (90.0, "#d62728", "Nav1.6 = 90 mS/cm² (high)"),
    ]:
        rows = _rows_for_nav16(summary=summary, nav16_mS=nav16_mS)
        if not rows:
            continue
        x = np.array([r["kv3_mS_cm2"] for r in rows])
        y = np.array([r["dsi"] for r in rows])
        ax.plot(x, y, "o-", color=color, linewidth=2, markersize=10, label=label)
    ax.axhline(
        baseline["dsi"],
        color="black",
        linestyle="--",
        alpha=0.6,
        label=f"baseline DSI = {baseline['dsi']:.2f}",
    )
    ax.set_xlabel("Kv3 density (mS/cm²)")
    ax.set_ylabel("DSI = (PD − ND) / (PD + ND)")
    ax.set_title("DSI rescue: does Kv3 co-expression restore DSI lost to Nav1.6?")
    ax.set_ylim(-0.3, 1.0)
    ax.set_xticks(KV3_DENSITY_VALUES)
    ax.set_xticklabels(KV3_DENSITY_LABELS)
    ax.legend(loc="best")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(str(DSI_RESCUE_PNG), bbox_inches="tight")
    plt.close(fig)


def _plot_firing_rate_rescue(*, summary: list[dict[str, Any]]) -> None:
    baseline = _baseline(summary)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=120, sharey=True)
    for ax, nav16_mS, label in [
        (axes[0], 30.0, "Nav1.6 = 30 mS/cm² (med)"),
        (axes[1], 90.0, "Nav1.6 = 90 mS/cm² (high)"),
    ]:
        rows = _rows_for_nav16(summary=summary, nav16_mS=nav16_mS)
        if not rows:
            ax.set_title(f"{label} (no data)")
            continue
        x = np.array([r["kv3_mS_cm2"] for r in rows])
        pd_means = np.array([r["spike_count_pd_mean"] for r in rows])
        pd_sds = np.array([r["spike_count_pd_sd"] for r in rows])
        nd_means = np.array([r["spike_count_nd_mean"] for r in rows])
        nd_sds = np.array([r["spike_count_nd_sd"] for r in rows])
        ax.errorbar(
            x, pd_means, yerr=pd_sds, fmt="o-", color="#1f77b4", linewidth=2, capsize=4, label="PD"
        )
        ax.errorbar(
            x, nd_means, yerr=nd_sds, fmt="s-", color="#d62728", linewidth=2, capsize=4, label="ND"
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
        ax.set_xlabel("Kv3 density (mS/cm²)")
        ax.set_xticks(KV3_DENSITY_VALUES)
        ax.set_xticklabels(KV3_DENSITY_LABELS)
        ax.set_title(label)
        ax.grid(alpha=0.3)
        if nav16_mS == 30.0:
            ax.set_ylabel("Spikes / trial (mean ± SD, n=5)")
        ax.legend(loc="best", fontsize=8)
    fig.suptitle("Firing rate rescue: PD/ND spike count vs Kv3 density at fixed Nav1.6", y=1.02)
    fig.tight_layout()
    fig.savefig(str(FIRING_RATE_RESCUE_PNG), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    summary = _load_summary()
    print(f"Loaded {len(summary)} conditions")
    _plot_dsi_rescue(summary=summary)
    _plot_firing_rate_rescue(summary=summary)
    print("Wrote 2 PNGs to results/images/.")


if __name__ == "__main__":
    main()
