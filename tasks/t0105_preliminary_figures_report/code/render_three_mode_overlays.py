"""Render the 2x2 (bed x direction) three-mode somatic Vm overlay panel.

Each subplot overlays three traces (mode=FULL, EPSP_PASSIVE, IPSP_PASSIVE) from the
corresponding ``voltage_traces.csv`` file. Bed A schema is (mode, direction, t_ms,
v_mv); Bed B has an extra ``trial`` column which we mean-collapse per (mode,
direction, t_ms).
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # type: ignore[import-untyped]
from matplotlib.axes import Axes
from numpy import dtype
from pandas.api.extensions import ExtensionDtype  # type: ignore[import-untyped]

from tasks.t0105_preliminary_figures_report.code import constants as cst
from tasks.t0105_preliminary_figures_report.code import paths as pth


@dataclass(frozen=True, slots=True)
class TracesByMode:
    bed_short: str
    direction: str
    t_ms_by_mode: dict[str, np.ndarray]
    v_mv_by_mode: dict[str, np.ndarray]


T0065_DTYPES: dict[str, dtype[np.generic] | ExtensionDtype] = {
    "mode": pd.StringDtype(),
    "direction": pd.StringDtype(),
    "t_ms": np.dtype("float64"),
    "v_mv": np.dtype("float64"),
}

T0066_DTYPES: dict[str, dtype[np.generic] | ExtensionDtype] = {
    "mode": pd.StringDtype(),
    "direction": pd.StringDtype(),
    "trial": pd.Int64Dtype(),
    "t_ms": np.dtype("float64"),
    "v_mv": np.dtype("float64"),
}

ALL_MODES: tuple[str, ...] = (cst.MODE_EPSP_PASSIVE, cst.MODE_IPSP_PASSIVE, cst.MODE_FULL)


def _extract_traces_for_direction(
    *,
    df: pd.DataFrame,
    direction: str,
    has_trial: bool,
    bed_short: str,
) -> TracesByMode:
    df_dir: pd.DataFrame = df[df[cst.COL_DIRECTION] == direction]
    t_by_mode: dict[str, np.ndarray] = {}
    v_by_mode: dict[str, np.ndarray] = {}
    for mode in ALL_MODES:
        sub: pd.DataFrame = df_dir[df_dir[cst.COL_MODE] == mode]
        if len(sub) == 0:
            continue
        if has_trial:
            # Mean across trials per t_ms.
            grouped: pd.DataFrame = sub.groupby(by=cst.COL_T_MS)[cst.COL_V_MV].mean().reset_index()
            grouped = grouped.sort_values(by=cst.COL_T_MS)
            t_by_mode[mode] = grouped[cst.COL_T_MS].to_numpy(dtype=np.float64)
            v_by_mode[mode] = grouped[cst.COL_V_MV].to_numpy(dtype=np.float64)
        else:
            sub_sorted: pd.DataFrame = sub.sort_values(by=cst.COL_T_MS)
            t_by_mode[mode] = sub_sorted[cst.COL_T_MS].to_numpy(dtype=np.float64)
            v_by_mode[mode] = sub_sorted[cst.COL_V_MV].to_numpy(dtype=np.float64)
    return TracesByMode(
        bed_short=bed_short,
        direction=direction,
        t_ms_by_mode=t_by_mode,
        v_mv_by_mode=v_by_mode,
    )


def _load_bed_traces() -> dict[tuple[str, str], TracesByMode]:
    bed_a_df: pd.DataFrame = pd.read_csv(
        filepath_or_buffer=pth.T0065_TRACES_CSV,
        dtype=T0065_DTYPES,
        usecols=list(T0065_DTYPES.keys()),
    )
    bed_b_df: pd.DataFrame = pd.read_csv(
        filepath_or_buffer=pth.T0066_TRACES_CSV,
        dtype=T0066_DTYPES,
        usecols=list(T0066_DTYPES.keys()),
    )
    out: dict[tuple[str, str], TracesByMode] = {}
    for direction in (cst.DIRECTION_PD, cst.DIRECTION_ND):
        out[(cst.BED_A_SHORT, direction)] = _extract_traces_for_direction(
            df=bed_a_df,
            direction=direction,
            has_trial=False,
            bed_short=cst.BED_A_SHORT,
        )
        out[(cst.BED_B_SHORT, direction)] = _extract_traces_for_direction(
            df=bed_b_df,
            direction=direction,
            has_trial=True,
            bed_short=cst.BED_B_SHORT,
        )
    return out


def _plot_panel(*, ax: Axes, traces: TracesByMode, show_legend: bool) -> None:
    for mode in ALL_MODES:
        if mode not in traces.t_ms_by_mode:
            continue
        ax.plot(
            traces.t_ms_by_mode[mode],
            traces.v_mv_by_mode[mode],
            color=cst.MODE_COLORS[mode],
            linewidth=1.0,
            label=mode,
        )
    ax.set_title(label=f"{traces.bed_short} -- {traces.direction}", fontsize=10)
    ax.set_xlabel(xlabel="t (ms)", fontsize=9)
    ax.set_ylabel(ylabel="V_m (mV)", fontsize=9)
    ax.grid(visible=True, alpha=0.3)
    if show_legend:
        ax.legend(loc="upper right", fontsize=8, frameon=True)


def render_three_mode_overlays() -> None:
    pth.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    traces_by_panel: dict[tuple[str, str], TracesByMode] = _load_bed_traces()
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(13.0, 7.5), dpi=cst.DPI)
    # Layout: rows = bed (A top, B bottom); cols = direction (PD left, ND right).
    panel_grid: tuple[tuple[tuple[str, str], ...], ...] = (
        ((cst.BED_A_SHORT, cst.DIRECTION_PD), (cst.BED_A_SHORT, cst.DIRECTION_ND)),
        ((cst.BED_B_SHORT, cst.DIRECTION_PD), (cst.BED_B_SHORT, cst.DIRECTION_ND)),
    )
    for row_idx, row in enumerate(panel_grid):
        for col_idx, key in enumerate(row):
            traces: TracesByMode = traces_by_panel[key]
            show_legend: bool = row_idx == 0 and col_idx == 1
            _plot_panel(
                ax=axes[row_idx][col_idx],
                traces=traces,
                show_legend=show_legend,
            )
    fig.suptitle(
        t=(
            "Somatic Vm three-mode overlays (HH off for EPSP_PASSIVE / IPSP_PASSIVE;"
            " HH on for FULL)"
        ),
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    fig.savefig(
        fname=pth.FIG05_THREE_MODE_PNG,
        dpi=cst.DPI,
        facecolor=cst.FACECOLOR,
        bbox_inches=cst.BBOX_INCHES,
    )
    plt.close(fig=fig)


def main() -> None:
    render_three_mode_overlays()
    print(f"[t0105] wrote {pth.FIG05_THREE_MODE_PNG}")


if __name__ == "__main__":
    main()
