"""Per-cell ATP compartment shares (soma / AIS / dendrites) + ternary plot + violin panel.

For each cell in the spiking cohort:
  total_ap_atp = atp_soma + atp_ais + atp_dendrites_total
  share_soma   = atp_soma / total_ap_atp
  share_ais    = atp_ais / total_ap_atp
  share_dend   = atp_dendrites_total / total_ap_atp

Outputs:
    results/data/atp_compartment_shares.csv
    results/images/atp_share_ternary.png
    results/images/atp_share_violins.png
"""

from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy.stats import mannwhitneyu

from tasks.t0125_t0123_cluster_factor_mi_atp.code.constants import (
    CHART_DPI,
    CORNER_COLORS,
    CORNER_LABELS,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.group_thresholds import (
    GroupThresholds,
    assign_corner_label,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.load_t0123_cells import (
    ATP_AIS_COLUMN,
    ATP_DENDRITES_COLUMN,
    ATP_PER_SPIKE_COLUMN,
    ATP_SOMA_COLUMN,
    CELL_INDEX_COLUMN,
    GENERATION_COLUMN,
    MI_COLUMN,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.paths import (
    ATP_COMPARTMENT_SHARES_CSV,
    ATP_SHARE_TERNARY_PNG,
    ATP_SHARE_VIOLINS_PNG,
    GROUP_THRESHOLDS_JSON,
    T0123_SPIKING_CELLS_PARQUET,
)

CORNER_LABEL_COLUMN: str = "corner_label"
SHARE_SOMA_COLUMN: str = "share_soma"
SHARE_AIS_COLUMN: str = "share_ais"
SHARE_DEND_COLUMN: str = "share_dend"


def _compute_shares(df: pd.DataFrame) -> pd.DataFrame:
    total: pd.Series = df[ATP_SOMA_COLUMN] + df[ATP_AIS_COLUMN] + df[ATP_DENDRITES_COLUMN]
    safe_total: pd.Series = total.replace(0.0, np.nan)
    return df.assign(
        **{
            SHARE_SOMA_COLUMN: (df[ATP_SOMA_COLUMN] / safe_total).fillna(0.0),
            SHARE_AIS_COLUMN: (df[ATP_AIS_COLUMN] / safe_total).fillna(0.0),
            SHARE_DEND_COLUMN: (df[ATP_DENDRITES_COLUMN] / safe_total).fillna(0.0),
        }
    )


def _to_barycentric(
    *,
    share_soma: NDArray[np.float64],
    share_ais: NDArray[np.float64],
    share_dend: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Barycentric coordinates for a (soma, AIS, dend) triple.

    Soma at left vertex (0,0), AIS at right (1,0), dend at top (0.5, sqrt(3)/2).
    """
    x: NDArray[np.float64] = share_ais + 0.5 * share_dend
    y: NDArray[np.float64] = (np.sqrt(3.0) / 2.0) * share_dend
    return x, y


def _render_ternary(*, df_shares: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 7), dpi=CHART_DPI)
    # Triangle outline.
    tri_x: list[float] = [0.0, 1.0, 0.5, 0.0]
    tri_y: list[float] = [0.0, 0.0, float(np.sqrt(3.0) / 2.0), 0.0]
    ax.plot(tri_x, tri_y, color="black", linewidth=1.2)
    ax.text(-0.02, -0.04, "soma", ha="right", va="top", fontsize=11)
    ax.text(1.02, -0.04, "AIS", ha="left", va="top", fontsize=11)
    ax.text(
        0.5,
        float(np.sqrt(3.0) / 2.0) + 0.04,
        "dendrites",
        ha="center",
        va="bottom",
        fontsize=11,
    )

    for color, corner_label in zip(CORNER_COLORS, CORNER_LABELS, strict=True):
        sub: pd.DataFrame = df_shares[df_shares[CORNER_LABEL_COLUMN] == corner_label]
        if len(sub) == 0:
            continue
        x, y = _to_barycentric(
            share_soma=sub[SHARE_SOMA_COLUMN].to_numpy(dtype=np.float64),
            share_ais=sub[SHARE_AIS_COLUMN].to_numpy(dtype=np.float64),
            share_dend=sub[SHARE_DEND_COLUMN].to_numpy(dtype=np.float64),
        )
        ax.scatter(
            x,
            y,
            s=8,
            color=color,
            alpha=0.55,
            edgecolors="none",
            label=f"{corner_label} (n={len(sub)})",
        )
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, float(np.sqrt(3.0) / 2.0) + 0.15)
    ax.set_title("ATP-per-AP compartment shares (ternary, spiking cohort, by MI x ATP corner)")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    ATP_SHARE_TERNARY_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ATP_SHARE_TERNARY_PNG, dpi=CHART_DPI)
    plt.close(fig)
    print(f"Wrote {ATP_SHARE_TERNARY_PNG}", flush=True)


def _mwu_p(a: NDArray[np.float64], b: NDArray[np.float64]) -> float:
    if len(a) == 0 or len(b) == 0:
        return float("nan")
    _u, p = mannwhitneyu(a, b, alternative="two-sided")
    return float(p)


def _render_violins(
    *,
    df_shares: pd.DataFrame,
    thresholds: GroupThresholds,
) -> None:
    mi_vals: NDArray[np.float64] = df_shares[MI_COLUMN].to_numpy(dtype=np.float64)
    atp_vals: NDArray[np.float64] = df_shares[ATP_PER_SPIKE_COLUMN].to_numpy(dtype=np.float64)
    high_mi: NDArray[np.bool_] = mi_vals >= thresholds.mi_q3
    low_mi: NDArray[np.bool_] = mi_vals <= thresholds.mi_q1
    high_atp: NDArray[np.bool_] = atp_vals >= thresholds.atp_q3
    low_atp: NDArray[np.bool_] = atp_vals <= thresholds.atp_q1

    share_cols: list[str] = [SHARE_SOMA_COLUMN, SHARE_AIS_COLUMN, SHARE_DEND_COLUMN]
    share_labels: list[str] = ["soma", "AIS", "dendrites"]

    fig, axes = plt.subplots(3, 2, figsize=(10, 11), dpi=CHART_DPI)
    for row_idx, (col, lab) in enumerate(zip(share_cols, share_labels, strict=True)):
        # Left: MI axis (high vs low).
        ax_mi = axes[row_idx, 0]
        vals_high: NDArray[np.float64] = df_shares.loc[high_mi, col].to_numpy(dtype=np.float64)
        vals_low: NDArray[np.float64] = df_shares.loc[low_mi, col].to_numpy(dtype=np.float64)
        ax_mi.violinplot(
            [vals_high, vals_low],
            showmeans=True,
            showmedians=False,
        )
        ax_mi.set_xticks([1, 2])
        ax_mi.set_xticklabels([f"high MI\n(n={len(vals_high)})", f"low MI\n(n={len(vals_low)})"])
        ax_mi.set_ylabel(f"{lab} share")
        p_mi: float = _mwu_p(vals_high, vals_low)
        ax_mi.set_title(f"{lab} share by MI group (MWU p={p_mi:.2e})")
        ax_mi.grid(True, alpha=0.3)

        ax_atp = axes[row_idx, 1]
        vals_high_atp: NDArray[np.float64] = df_shares.loc[high_atp, col].to_numpy(dtype=np.float64)
        vals_low_atp: NDArray[np.float64] = df_shares.loc[low_atp, col].to_numpy(dtype=np.float64)
        ax_atp.violinplot(
            [vals_high_atp, vals_low_atp],
            showmeans=True,
            showmedians=False,
        )
        ax_atp.set_xticks([1, 2])
        ax_atp.set_xticklabels(
            [
                f"high ATP\n(n={len(vals_high_atp)})",
                f"low ATP\n(n={len(vals_low_atp)})",
            ]
        )
        ax_atp.set_ylabel(f"{lab} share")
        p_atp: float = _mwu_p(vals_high_atp, vals_low_atp)
        ax_atp.set_title(f"{lab} share by ATP group (MWU p={p_atp:.2e})")
        ax_atp.grid(True, alpha=0.3)
    fig.suptitle("ATP-per-AP compartment shares by quartile groups (spiking cohort)", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    ATP_SHARE_VIOLINS_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ATP_SHARE_VIOLINS_PNG, dpi=CHART_DPI)
    plt.close(fig)
    print(f"Wrote {ATP_SHARE_VIOLINS_PNG}", flush=True)


def main() -> None:
    df_spiking: pd.DataFrame = pd.read_parquet(T0123_SPIKING_CELLS_PARQUET)
    thresholds_payload: dict[str, object] = json.loads(
        GROUP_THRESHOLDS_JSON.read_text(encoding="utf-8")
    )
    thresholds: GroupThresholds = GroupThresholds(
        mi_q1=float(thresholds_payload["mi_q1"]),  # type: ignore[arg-type]
        mi_median=float(thresholds_payload["mi_median"]),  # type: ignore[arg-type]
        mi_q3=float(thresholds_payload["mi_q3"]),  # type: ignore[arg-type]
        atp_q1=float(thresholds_payload["atp_q1"]),  # type: ignore[arg-type]
        atp_median=float(thresholds_payload["atp_median"]),  # type: ignore[arg-type]
        atp_q3=float(thresholds_payload["atp_q3"]),  # type: ignore[arg-type]
    )

    df_shares_full: pd.DataFrame = _compute_shares(df_spiking)
    corner_labels_list: list[str] = [
        assign_corner_label(mi_val=float(m), atp_val=float(a), thresholds=thresholds)
        for m, a in zip(
            df_shares_full[MI_COLUMN].tolist(),
            df_shares_full[ATP_PER_SPIKE_COLUMN].tolist(),
            strict=True,
        )
    ]
    df_shares_full[CORNER_LABEL_COLUMN] = pd.Series(corner_labels_list, dtype="string")

    df_out: pd.DataFrame = df_shares_full[
        [
            GENERATION_COLUMN,
            CELL_INDEX_COLUMN,
            MI_COLUMN,
            ATP_PER_SPIKE_COLUMN,
            CORNER_LABEL_COLUMN,
            SHARE_SOMA_COLUMN,
            SHARE_AIS_COLUMN,
            SHARE_DEND_COLUMN,
        ]
    ]
    ATP_COMPARTMENT_SHARES_CSV.parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(ATP_COMPARTMENT_SHARES_CSV, index=False)
    print(f"Wrote {ATP_COMPARTMENT_SHARES_CSV} (n_rows={len(df_out)})", flush=True)

    _render_ternary(df_shares=df_shares_full)
    _render_violins(df_shares=df_shares_full, thresholds=thresholds)

    print(
        f"  Mean shares: soma={df_shares_full[SHARE_SOMA_COLUMN].mean():.3f}, "
        f"AIS={df_shares_full[SHARE_AIS_COLUMN].mean():.3f}, "
        f"dend={df_shares_full[SHARE_DEND_COLUMN].mean():.3f}",
        flush=True,
    )


if __name__ == "__main__":
    main()
