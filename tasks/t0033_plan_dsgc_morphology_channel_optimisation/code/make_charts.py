"""Render headline charts for the answer asset and results overlay.

Generates three PNGs under ``results/images/``:

1. ``cost_by_strategy_and_tier.png`` — grouped-bar chart of USD central
   cost per (strategy x tier) at tight parameterisation, excluding grid.
2. ``sensitivity_heatmap.png`` — 3x3 heatmap for the recommended cell
   (Surrogate-NN on RTX 4090, tight parameterisation).
3. ``parameter_count_breakdown.png`` — stacked bar of morphology vs VGC
   parameters at tight and rich parameterisations.
"""

from __future__ import annotations

import json
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code import paths
from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code.constants import (
    COL_COMPUTE_MODE,
    COL_COST_MULT,
    COL_PARAMETERISATION,
    COL_SAMPLE_MULT,
    COL_STRATEGY,
    COL_TIER,
    COL_USD_SENSITIVITY,
    COL_USD_TOTAL,
    PARAM_RICH,
    PARAM_TIGHT,
    ComputeMode,
    SearchStrategy,
    Tier,
)

RECOMMENDED_STRATEGY: str = SearchStrategy.SURROGATE_NN_GA.value
RECOMMENDED_COMPUTE: str = ComputeMode.SURROGATE_NN_GPU.value
RECOMMENDED_TIER: str = Tier.RTX_4090.value


def _load_envelope() -> pd.DataFrame:
    return pd.read_csv(paths.COST_ENVELOPE_CSV)


def _load_sensitivity() -> pd.DataFrame:
    return pd.read_csv(paths.SENSITIVITY_CSV)


def _load_param_summary() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(paths.PARAM_SUMMARY_JSON.read_text(encoding="utf-8"))
    return data


def plot_cost_by_strategy_and_tier() -> None:
    df = _load_envelope()
    df = df[df[COL_PARAMETERISATION] == PARAM_TIGHT]
    df = df[df[COL_STRATEGY] != SearchStrategy.GRID.value]

    # One panel per compute_mode; bars grouped by strategy x tier.
    compute_modes: list[str] = [m.value for m in ComputeMode]
    strategies: list[str] = [s.value for s in SearchStrategy if s is not SearchStrategy.GRID]

    fig, axes = plt.subplots(1, 3, figsize=(16, 6), sharey=False)
    for ax, mode in zip(axes, compute_modes, strict=True):
        sub = df[df[COL_COMPUTE_MODE] == mode]
        if sub.empty:
            ax.set_visible(False)
            continue
        tiers_present: list[str] = sorted(sub[COL_TIER].unique().tolist())
        x = np.arange(len(strategies))
        width: float = 0.8 / max(1, len(tiers_present))
        for i, tier in enumerate(tiers_present):
            values: list[float] = []
            for strategy in strategies:
                row = sub[(sub[COL_STRATEGY] == strategy) & (sub[COL_TIER] == tier)]
                values.append(float(row[COL_USD_TOTAL].iloc[0]) if not row.empty else 0.0)
            ax.bar(x + i * width, values, width, label=tier)
        ax.set_xticks(x + width * (len(tiers_present) - 1) / 2)
        ax.set_xticklabels(strategies, rotation=20, ha="right")
        ax.set_title(mode)
        ax.set_ylabel("USD (central)")
        ax.set_yscale("log")
        ax.legend(fontsize=8)
    fig.suptitle("Central-cell USD cost: strategy x tier, tight parameterisation (n_dims=25)")
    fig.tight_layout()
    paths.RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(paths.COST_BAR_CHART_PNG, dpi=120)
    plt.close(fig)
    print(f"Saved {paths.COST_BAR_CHART_PNG}")


def plot_sensitivity_heatmap() -> None:
    df = _load_sensitivity()
    sub = df[
        (df[COL_STRATEGY] == RECOMMENDED_STRATEGY)
        & (df[COL_COMPUTE_MODE] == RECOMMENDED_COMPUTE)
        & (df[COL_TIER] == RECOMMENDED_TIER)
        & (df[COL_PARAMETERISATION] == PARAM_TIGHT)
    ]
    assert len(sub) == 9, f"Expected 9 sensitivity cells, got {len(sub)}"

    pivot = sub.pivot(index=COL_SAMPLE_MULT, columns=COL_COST_MULT, values=COL_USD_SENSITIVITY)
    pivot = pivot.sort_index(ascending=True).reindex(columns=sorted(pivot.columns))

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(pivot.to_numpy(), aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([f"{c:g}x" for c in pivot.columns])
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([f"{r:g}x" for r in pivot.index])
    ax.set_xlabel("cost_mult (per-sim cost multiplier)")
    ax.set_ylabel("sample_mult (sample-count multiplier)")
    ax.set_title(
        f"Sensitivity: {RECOMMENDED_STRATEGY} / {RECOMMENDED_COMPUTE} / {RECOMMENDED_TIER}\n"
        f"USD at tight parameterisation (n_dims=25)"
    )
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            value = pivot.to_numpy()[i, j]
            ax.text(
                j,
                i,
                f"${value:,.0f}",
                ha="center",
                va="center",
                color="white" if value > pivot.to_numpy().mean() else "black",
                fontsize=9,
            )
    fig.colorbar(im, ax=ax, label="USD")
    fig.tight_layout()
    fig.savefig(paths.SENSITIVITY_HEATMAP_PNG, dpi=120)
    plt.close(fig)
    print(f"Saved {paths.SENSITIVITY_HEATMAP_PNG}")


def plot_parameter_count_breakdown() -> None:
    summary = _load_param_summary()
    labels: list[str] = [PARAM_TIGHT, PARAM_RICH]
    morphology_vals: list[int] = [summary["n_free_morphology"], summary["n_free_morphology"]]
    tight_channel: int = summary["n_free_tight_committed"] - summary["n_free_morphology"]
    rich_channel: int = summary["n_free_rich_committed"] - summary["n_free_morphology"]
    channel_vals: list[int] = [tight_channel, rich_channel]

    fig, ax = plt.subplots(figsize=(7, 5))
    x = np.arange(len(labels))
    width: float = 0.55
    ax.bar(x, morphology_vals, width, label="Morphology (Cuntz scalars)", color="#4c72b0")
    ax.bar(
        x,
        channel_vals,
        width,
        bottom=morphology_vals,
        label="Channel gbar parameters",
        color="#dd8452",
    )
    for i, _label in enumerate(labels):
        total = morphology_vals[i] + channel_vals[i]
        ax.text(x[i], total + 0.5, f"{total} free params", ha="center", va="bottom", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Number of free parameters")
    ax.set_title("Free-parameter breakdown: tight vs rich parameterisation")
    ax.legend()
    fig.tight_layout()
    fig.savefig(paths.PARAM_COUNT_CHART_PNG, dpi=120)
    plt.close(fig)
    print(f"Saved {paths.PARAM_COUNT_CHART_PNG}")


def main() -> None:
    paths.RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    plot_cost_by_strategy_and_tier()
    plot_sensitivity_heatmap()
    plot_parameter_count_breakdown()


if __name__ == "__main__":
    main()
