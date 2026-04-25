"""Render the two PNG charts for t0049.

* ``seclamp_conductance_pd_vs_nd.png`` — bar chart, 6 channel x direction cells, two bars
  per cell: paper Fig 3A-E target vs SEClamp this task (with SEClamp SD error bars).
* ``seclamp_vs_per_syn_direct_modality_comparison.png`` — bar chart, same x-axis, three
  bars per cell: paper target vs SEClamp this task vs t0047 per-synapse-summed; log y-axis.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from tasks.t0049_seclamp_cond_remeasure.code.constants import (  # noqa: E402
    CHANNEL_AMPA_LABEL,
    CHANNEL_GABA_LABEL,
    CHANNEL_NMDA_LABEL,
    COL_CHANNEL,
    COL_DIRECTION,
    COL_G_SECLAMP_MEAN_NS,
    COL_G_SECLAMP_SD_NS,
    COL_PAPER_TARGET_NS,
    COL_T0047_SUMMED_NS,
    DIRECTION_ND_LABEL,
    DIRECTION_PD_LABEL,
)
from tasks.t0049_seclamp_cond_remeasure.code.paths import (  # noqa: E402
    SECLAMP_COMPARISON_CSV,
    SECLAMP_MODALITY_PNG,
    SECLAMP_PD_VS_ND_PNG,
)

CELL_ORDER: tuple[tuple[str, str], ...] = (
    (CHANNEL_NMDA_LABEL, DIRECTION_PD_LABEL),
    (CHANNEL_NMDA_LABEL, DIRECTION_ND_LABEL),
    (CHANNEL_AMPA_LABEL, DIRECTION_PD_LABEL),
    (CHANNEL_AMPA_LABEL, DIRECTION_ND_LABEL),
    (CHANNEL_GABA_LABEL, DIRECTION_PD_LABEL),
    (CHANNEL_GABA_LABEL, DIRECTION_ND_LABEL),
)


def _ordered_values(*, df: pd.DataFrame, column: str) -> list[float]:
    values: list[float] = []
    for channel, direction in CELL_ORDER:
        mask = (df[COL_CHANNEL] == channel) & (df[COL_DIRECTION] == direction)
        sub = df[mask]
        assert len(sub) == 1, (
            f"Expected exactly one row for ({channel}, {direction}), got {len(sub)}"
        )
        values.append(float(sub.iloc[0][column]))
    return values


def _render_paper_vs_seclamp(*, df_compare: pd.DataFrame) -> None:
    cell_labels: list[str] = [f"{c.upper()}\n{d}" for (c, d) in CELL_ORDER]
    paper_vals: list[float] = _ordered_values(df=df_compare, column=COL_PAPER_TARGET_NS)
    seclamp_means: list[float] = _ordered_values(df=df_compare, column=COL_G_SECLAMP_MEAN_NS)
    seclamp_sds: list[float] = _ordered_values(df=df_compare, column=COL_G_SECLAMP_SD_NS)

    x: np.ndarray = np.arange(len(cell_labels))
    width: float = 0.36

    fig, ax = plt.subplots(figsize=(11.0, 5.5))
    bars_paper = ax.bar(
        x - width / 2,
        paper_vals,
        width=width,
        label="Paper Fig 3A-E target",
        color="#888888",
    )
    bars_seclamp = ax.bar(
        x + width / 2,
        seclamp_means,
        width=width,
        yerr=seclamp_sds,
        capsize=3,
        label="SEClamp (this task, gNMDA = 0.5 nS)",
        color="#1f77b4",
    )

    ax.set_xticks(x)
    ax.set_xticklabels(cell_labels)
    ax.set_ylabel("Conductance (nS)")
    ax.set_title(
        "Somatic SEClamp conductance vs Poleg-Polsky 2016 Fig 3A-E target (gNMDA = 0.5 nS)",
    )
    ax.legend(loc="best")
    ax.grid(axis="y", alpha=0.3)

    # Annotate bars.
    for bar, value in zip(bars_paper, paper_vals, strict=True):
        ax.annotate(
            f"{value:.2f}",
            xy=(bar.get_x() + bar.get_width() / 2.0, value),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
        )
    for bar, value in zip(bars_seclamp, seclamp_means, strict=True):
        ax.annotate(
            f"{value:.2f}",
            xy=(bar.get_x() + bar.get_width() / 2.0, value),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    fig.tight_layout()
    fig.savefig(SECLAMP_PD_VS_ND_PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[figures] Wrote {SECLAMP_PD_VS_ND_PNG}", flush=True)


def _render_modality_comparison(*, df_compare: pd.DataFrame) -> None:
    cell_labels: list[str] = [f"{c.upper()}\n{d}" for (c, d) in CELL_ORDER]
    paper_vals: list[float] = _ordered_values(df=df_compare, column=COL_PAPER_TARGET_NS)
    seclamp_means: list[float] = _ordered_values(df=df_compare, column=COL_G_SECLAMP_MEAN_NS)
    t0047_summed: list[float] = _ordered_values(df=df_compare, column=COL_T0047_SUMMED_NS)

    x: np.ndarray = np.arange(len(cell_labels))
    width: float = 0.27

    fig, ax = plt.subplots(figsize=(11.0, 6.0))
    bars_paper = ax.bar(
        x - width,
        paper_vals,
        width=width,
        label="Paper Fig 3A-E target",
        color="#888888",
    )
    bars_seclamp = ax.bar(
        x,
        seclamp_means,
        width=width,
        label="SEClamp (this task)",
        color="#1f77b4",
    )
    bars_t0047 = ax.bar(
        x + width,
        t0047_summed,
        width=width,
        label="t0047 per-syn direct (summed)",
        color="#d62728",
    )

    ax.set_xticks(x)
    ax.set_xticklabels(cell_labels)
    ax.set_ylabel("Conductance (nS, log scale)")
    ax.set_yscale("log")
    ax.set_title(
        "Conductance modality comparison at gNMDA = 0.5 nS: "
        "paper Fig 3A-E vs SEClamp vs per-synapse-direct (t0047)",
    )
    ax.legend(loc="best")
    ax.grid(axis="y", which="both", alpha=0.3)

    # Annotate bars.
    for group_bars, group_vals in (
        (bars_paper, paper_vals),
        (bars_seclamp, seclamp_means),
        (bars_t0047, t0047_summed),
    ):
        for bar, value in zip(group_bars, group_vals, strict=True):
            ax.annotate(
                f"{value:.1f}",
                xy=(bar.get_x() + bar.get_width() / 2.0, value),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=7,
            )

    fig.tight_layout()
    fig.savefig(SECLAMP_MODALITY_PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[figures] Wrote {SECLAMP_MODALITY_PNG}", flush=True)


def main() -> None:
    print(f"[figures] Reading {SECLAMP_COMPARISON_CSV}", flush=True)
    df_compare: pd.DataFrame = pd.read_csv(SECLAMP_COMPARISON_CSV)
    _render_paper_vs_seclamp(df_compare=df_compare)
    _render_modality_comparison(df_compare=df_compare)


if __name__ == "__main__":
    main()
