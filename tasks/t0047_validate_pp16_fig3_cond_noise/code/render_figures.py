"""Render the seven required reproduction PNGs to ``RESULTS_IMAGES_DIR``.

Reads CSVs / JSON from ``RESULTS_DATA_DIR``. Uses raw matplotlib because the t0011
``tuning_curve_viz`` API is for 12-angle curves only. The Okabe-Ito ``MODEL_COLORS``
palette is imported from t0011 for visual consistency.
"""

from __future__ import annotations

import json
import sys
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants import (  # noqa: E402
    MODEL_COLORS,
)
from tasks.t0047_validate_pp16_fig3_cond_noise.code.constants import (  # noqa: E402
    AMPA_ND_TARGET_NS,
    AMPA_PD_TARGET_NS,
    B2GNMDA_GRID_NS,
    COL_B2GNMDA_NS,
    COL_DIRECTION,
    COL_PEAK_G_AMPA_SUMMED_NS,
    COL_PEAK_G_NMDA_SUMMED_NS,
    COL_PEAK_G_SACINHIB_SUMMED_NS,
    COL_T_MS,
    COL_V_MV,
    DIRECTION_ND_LABEL,
    DIRECTION_PD_LABEL,
    DSI_FIG3F_TOLERANCE,
    DSI_PAPER_FIG3F_TARGET,
    FLICKER_VAR_GRID,
    GABA_ND_TARGET_NS,
    GABA_PD_TARGET_NS,
    NMDA_ND_TARGET_NS,
    NMDA_PD_TARGET_NS,
    PSP_TRACE_GNMDA_VALUES_NS,
    NoiseCondition,
)
from tasks.t0047_validate_pp16_fig3_cond_noise.code.paths import (  # noqa: E402
    DSI_AUC_BY_COND_NOISE_JSON,
    DSI_BY_GNMDA_JSON,
    FIG3A_PNG,
    FIG3B_PNG,
    FIG3C_PNG,
    FIG3F_BOTTOM_PNG,
    FIG3F_TOP_PNG,
    FIG6_PNG,
    FIG7_PNG,
    GNMDA_TRIALS_CSV,
    PSP_TRACES_CSV,
    RESULTS_IMAGES_DIR,
)

_PD_COLOR: str = MODEL_COLORS[0]  # orange (E69F00)
_ND_COLOR: str = MODEL_COLORS[1]  # sky-blue (56B4E9)


def _grouped_bar_pd_vs_nd(
    *,
    df_gnmda: pd.DataFrame,
    column: str,
    target_pd_ns: float,
    target_nd_ns: float,
    title: str,
    ylabel: str,
    out_path: Any,
) -> None:
    """Grouped bar chart: x = b2gnmda value, two bars per cell PD vs ND."""
    grid: list[float] = list(B2GNMDA_GRID_NS)
    pd_means: list[float] = []
    pd_stds: list[float] = []
    nd_means: list[float] = []
    nd_stds: list[float] = []

    for b2gnmda_ns in grid:
        pd_cell: pd.Series = df_gnmda[
            (df_gnmda[COL_DIRECTION] == DIRECTION_PD_LABEL)
            & (df_gnmda[COL_B2GNMDA_NS].round(6) == round(float(b2gnmda_ns), 6))
        ][column].astype(float)
        nd_cell: pd.Series = df_gnmda[
            (df_gnmda[COL_DIRECTION] == DIRECTION_ND_LABEL)
            & (df_gnmda[COL_B2GNMDA_NS].round(6) == round(float(b2gnmda_ns), 6))
        ][column].astype(float)
        pd_means.append(float(pd_cell.mean()) if len(pd_cell) > 0 else float("nan"))
        pd_stds.append(float(pd_cell.std(ddof=1)) if len(pd_cell) > 1 else 0.0)
        nd_means.append(float(nd_cell.mean()) if len(nd_cell) > 0 else float("nan"))
        nd_stds.append(float(nd_cell.std(ddof=1)) if len(nd_cell) > 1 else 0.0)

    x: np.ndarray = np.arange(len(grid))
    width: float = 0.38

    fig, ax = plt.subplots(figsize=(8.5, 5.0), dpi=150)
    ax.bar(
        x - width / 2,
        pd_means,
        width=width,
        yerr=pd_stds,
        label="PD",
        color=_PD_COLOR,
        edgecolor="black",
        capsize=3,
    )
    ax.bar(
        x + width / 2,
        nd_means,
        width=width,
        yerr=nd_stds,
        label="ND",
        color=_ND_COLOR,
        edgecolor="black",
        capsize=3,
    )
    ax.axhline(
        target_pd_ns,
        color=_PD_COLOR,
        linestyle="--",
        alpha=0.7,
        label=f"Paper PD ~{target_pd_ns:g} nS",
    )
    ax.axhline(
        target_nd_ns,
        color=_ND_COLOR,
        linestyle="--",
        alpha=0.7,
        label=f"Paper ND ~{target_nd_ns:g} nS",
    )
    ax.set_xticks(x)
    ax.set_xticklabels([f"{g:.1f}" for g in grid])
    ax.set_xlabel("b2gnmda (nS)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _render_fig3_abc(*, df_gnmda: pd.DataFrame) -> None:
    _grouped_bar_pd_vs_nd(
        df_gnmda=df_gnmda,
        column=COL_PEAK_G_NMDA_SUMMED_NS,
        target_pd_ns=NMDA_PD_TARGET_NS,
        target_nd_ns=NMDA_ND_TARGET_NS,
        title="Fig 3A: NMDA peak conductance, PD vs ND (summed across synapses)",
        ylabel="peak g_NMDA summed (nS)",
        out_path=FIG3A_PNG,
    )
    _grouped_bar_pd_vs_nd(
        df_gnmda=df_gnmda,
        column=COL_PEAK_G_AMPA_SUMMED_NS,
        target_pd_ns=AMPA_PD_TARGET_NS,
        target_nd_ns=AMPA_ND_TARGET_NS,
        title="Fig 3B: AMPA peak conductance, PD vs ND (summed across synapses)",
        ylabel="peak g_AMPA summed (nS)",
        out_path=FIG3B_PNG,
    )
    _grouped_bar_pd_vs_nd(
        df_gnmda=df_gnmda,
        column=COL_PEAK_G_SACINHIB_SUMMED_NS,
        target_pd_ns=GABA_PD_TARGET_NS,
        target_nd_ns=GABA_ND_TARGET_NS,
        title="Fig 3C: GABA peak conductance (SACinhib), PD vs ND (summed across synapses)",
        ylabel="peak g_GABA summed (nS)",
        out_path=FIG3C_PNG,
    )


def _render_fig3f_top(*, df_traces: pd.DataFrame) -> None:
    n_rows: int = len(PSP_TRACE_GNMDA_VALUES_NS)
    fig, axes = plt.subplots(
        n_rows,
        2,
        figsize=(11.0, 2.5 * n_rows),
        dpi=150,
        sharex=True,
    )
    if n_rows == 1:
        axes = np.array([axes])

    for ri, b2gnmda_ns in enumerate(PSP_TRACE_GNMDA_VALUES_NS):
        for ci, dir_label in enumerate((DIRECTION_PD_LABEL, DIRECTION_ND_LABEL)):
            ax = axes[ri, ci]
            cell: pd.DataFrame = df_traces[
                (df_traces[COL_B2GNMDA_NS].round(6) == round(float(b2gnmda_ns), 6))
                & (df_traces[COL_DIRECTION] == dir_label)
            ].sort_values(COL_T_MS)
            color: str = _PD_COLOR if dir_label == DIRECTION_PD_LABEL else _ND_COLOR
            ax.plot(cell[COL_T_MS], cell[COL_V_MV], color=color, linewidth=1.0)
            ax.set_title(f"gNMDA={b2gnmda_ns:.1f} nS, {dir_label}", fontsize=10)
            ax.set_ylabel("v_soma (mV)")
            ax.grid(True, alpha=0.3)
            if ri == n_rows - 1:
                ax.set_xlabel("t (ms)")

    fig.suptitle("Fig 3F top: simulated PSP traces (PD vs ND)", fontsize=12)
    fig.tight_layout()
    FIG3F_TOP_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG3F_TOP_PNG, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _render_fig3f_bottom(*, dsi_by_gnmda: dict[str, float | None]) -> None:
    grid: list[float] = list(B2GNMDA_GRID_NS)
    ours: list[float] = []
    for b2gnmda_ns in grid:
        v: float | None = dsi_by_gnmda.get(f"{b2gnmda_ns:.2f}")
        ours.append(float("nan") if v is None else float(v))

    # t0046's preliminary observed series (per plan REQ-6 / discrepancy catalogue).
    t0046_grid: tuple[float, ...] = (0.0, 0.5, 1.5, 2.5)
    t0046_dsi: tuple[float, ...] = (0.124, 0.204, 0.049, 0.026)

    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=150)
    ax.plot(grid, ours, marker="o", color=MODEL_COLORS[0], label="t0047 (this task)")
    ax.plot(
        t0046_grid,
        t0046_dsi,
        marker="s",
        color=MODEL_COLORS[2],
        linestyle="--",
        label="t0046 (prior reproduction)",
    )
    ax.axhline(
        DSI_PAPER_FIG3F_TARGET,
        color="black",
        linestyle="--",
        alpha=0.6,
        label=f"Paper Fig 3F target = {DSI_PAPER_FIG3F_TARGET:.2f}",
    )
    ax.fill_between(
        [min(grid), max(grid)],
        DSI_PAPER_FIG3F_TARGET - DSI_FIG3F_TOLERANCE,
        DSI_PAPER_FIG3F_TARGET + DSI_FIG3F_TOLERANCE,
        color="black",
        alpha=0.08,
        label=(f"Paper +/- {DSI_FIG3F_TOLERANCE:.2f} band"),
    )
    ax.set_xlabel("b2gnmda (nS)")
    ax.set_ylabel("DSI = (PD - ND)/(PD + ND)")
    ax.set_title("Fig 3F bottom: DSI vs gNMDA")
    ax.set_xlim(min(grid) - 0.1, max(grid) + 0.1)
    ax.set_ylim(-0.1, max(0.5, max(ours + list(t0046_dsi)) + 0.05))
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    FIG3F_BOTTOM_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG3F_BOTTOM_PNG, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _render_fig6_or_7(
    *,
    payload: dict[str, dict[str, dict[str, float | None]]],
    metric_key: str,
    title: str,
    ylabel: str,
    out_path: Any,
) -> None:
    """Three lines (one per condition), x = flickerVAR, y = metric_key."""
    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=150)
    color_map: dict[str, str] = {
        NoiseCondition.CONTROL.value: MODEL_COLORS[0],
        NoiseCondition.AP5.value: MODEL_COLORS[1],
        NoiseCondition.ZERO_MG.value: MODEL_COLORS[2],
    }
    marker_map: dict[str, str] = {
        NoiseCondition.CONTROL.value: "o",
        NoiseCondition.AP5.value: "s",
        NoiseCondition.ZERO_MG.value: "^",
    }
    for cond_value in (
        NoiseCondition.CONTROL.value,
        NoiseCondition.AP5.value,
        NoiseCondition.ZERO_MG.value,
    ):
        cells: dict[str, dict[str, float | None]] = payload.get(cond_value, {})
        xs: list[float] = []
        ys: list[float] = []
        for f_var in FLICKER_VAR_GRID:
            v: float | None = cells.get(f"{f_var:.2f}", {}).get(metric_key)
            if v is None:
                continue
            xs.append(float(f_var))
            ys.append(float(v))
        ax.plot(
            xs,
            ys,
            marker=marker_map[cond_value],
            color=color_map[cond_value],
            label=cond_value,
        )
    ax.set_xlabel("flickerVAR (noise SD fraction)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(list(FLICKER_VAR_GRID))
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> int:
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    df_gnmda: pd.DataFrame = pd.read_csv(GNMDA_TRIALS_CSV)
    df_traces: pd.DataFrame = pd.read_csv(PSP_TRACES_CSV)
    dsi_by_gnmda: dict[str, float | None] = json.loads(
        DSI_BY_GNMDA_JSON.read_text(encoding="utf-8"),
    )
    dsi_auc_by_cond_noise: dict[str, dict[str, dict[str, float | None]]] = json.loads(
        DSI_AUC_BY_COND_NOISE_JSON.read_text(encoding="utf-8"),
    )

    _render_fig3_abc(df_gnmda=df_gnmda)
    print("[render_figures] wrote Fig 3A/B/C", flush=True)

    _render_fig3f_top(df_traces=df_traces)
    print("[render_figures] wrote Fig 3F top", flush=True)

    _render_fig3f_bottom(dsi_by_gnmda=dsi_by_gnmda)
    print("[render_figures] wrote Fig 3F bottom", flush=True)

    _render_fig6_or_7(
        payload=dsi_auc_by_cond_noise,
        metric_key="dsi",
        title="Fig 6: DSI vs flickerVAR per condition",
        ylabel="DSI = (PD - ND)/(PD + ND)",
        out_path=FIG6_PNG,
    )
    _render_fig6_or_7(
        payload=dsi_auc_by_cond_noise,
        metric_key="auc",
        title="Fig 7: ROC AUC (PD peak vs trial baselines) vs flickerVAR per condition",
        ylabel="ROC AUC (PD peaks vs baselines)",
        out_path=FIG7_PNG,
    )
    print("[render_figures] wrote Fig 6 and Fig 7", flush=True)
    print("[render_figures] done", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
