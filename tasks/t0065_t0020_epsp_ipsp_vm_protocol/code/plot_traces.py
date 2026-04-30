"""Plot per-mode and three-mode-overlay PNGs from data/voltage_traces.csv."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.api.extensions import ExtensionDtype

from tasks.t0065_t0020_epsp_ipsp_vm_protocol.code.constants import (
    DIRECTION_COLUMN,
    MODE_COLUMN,
    T_MS_COLUMN,
    V_MV_COLUMN,
    Condition,
    TrialMode,
)
from tasks.t0065_t0020_epsp_ipsp_vm_protocol.code.paths import (
    EPSP_PD_VS_ND_PNG,
    IMAGES_DIR,
    IPSP_PD_VS_ND_PNG,
    THREE_MODE_ND_OVERLAY_PNG,
    THREE_MODE_PD_OVERLAY_PNG,
    VM_FULL_PD_VS_ND_PNG,
    VOLTAGE_TRACES_CSV,
)

VOLTAGE_TRACES_DTYPE: dict[str, np.dtype | ExtensionDtype] = {
    MODE_COLUMN: pd.StringDtype(),
    DIRECTION_COLUMN: pd.StringDtype(),
    T_MS_COLUMN: np.dtype("float64"),
    V_MV_COLUMN: np.dtype("float64"),
}

PD_COLOR: str = "tab:blue"
ND_COLOR: str = "tab:red"
FULL_COLOR: str = "black"
EPSP_COLOR: str = "tab:green"
IPSP_COLOR: str = "tab:purple"


@dataclass(frozen=True, slots=True)
class TraceSlice:
    """One trace slice for plotting (mode, direction, t, v)."""

    mode: TrialMode
    direction: Condition
    t_ms: np.ndarray
    v_mv: np.ndarray


def _load_traces(*, csv_path: Path) -> DataFrame:
    return pd.read_csv(filepath_or_buffer=csv_path, dtype=VOLTAGE_TRACES_DTYPE)


def _slice_trace(
    *,
    df: DataFrame,
    mode: TrialMode,
    direction: Condition,
) -> TraceSlice:
    sub: DataFrame = df[(df[MODE_COLUMN] == mode.value) & (df[DIRECTION_COLUMN] == direction.value)]
    return TraceSlice(
        mode=mode,
        direction=direction,
        t_ms=sub[T_MS_COLUMN].to_numpy(dtype=np.float64),
        v_mv=sub[V_MV_COLUMN].to_numpy(dtype=np.float64),
    )


def _plot_mode_pd_vs_nd(
    *,
    df: DataFrame,
    mode: TrialMode,
    title: str,
    output_path: Path,
) -> None:
    pd_trace: TraceSlice = _slice_trace(df=df, mode=mode, direction=Condition.PD)
    nd_trace: TraceSlice = _slice_trace(df=df, mode=mode, direction=Condition.ND)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(pd_trace.t_ms, pd_trace.v_mv, color=PD_COLOR, label="PD", linewidth=1.0)
    ax.plot(nd_trace.t_ms, nd_trace.v_mv, color=ND_COLOR, label="ND", linewidth=1.0)
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Soma Vm (mV)")
    ax.set_title(title)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def _plot_three_mode_overlay(
    *,
    df: DataFrame,
    direction: Condition,
    title: str,
    output_path: Path,
) -> None:
    full_trace: TraceSlice = _slice_trace(df=df, mode=TrialMode.FULL, direction=direction)
    epsp_trace: TraceSlice = _slice_trace(df=df, mode=TrialMode.EPSP_PASSIVE, direction=direction)
    ipsp_trace: TraceSlice = _slice_trace(df=df, mode=TrialMode.IPSP_PASSIVE, direction=direction)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(full_trace.t_ms, full_trace.v_mv, color=FULL_COLOR, label="FULL", linewidth=1.0)
    ax.plot(
        epsp_trace.t_ms,
        epsp_trace.v_mv,
        color=EPSP_COLOR,
        label="EPSP_PASSIVE",
        linewidth=1.0,
    )
    ax.plot(
        ipsp_trace.t_ms,
        ipsp_trace.v_mv,
        color=IPSP_COLOR,
        label="IPSP_PASSIVE",
        linewidth=1.0,
    )
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Soma Vm (mV)")
    ax.set_title(title)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> int:
    if not VOLTAGE_TRACES_CSV.exists():
        print(
            f"voltage_traces.csv not found at {VOLTAGE_TRACES_CSV}; run run_protocol.py first.",
            flush=True,
        )
        return 1
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading traces from {VOLTAGE_TRACES_CSV}...", flush=True)
    df: DataFrame = _load_traces(csv_path=VOLTAGE_TRACES_CSV)
    print(f"  {len(df)} samples loaded.", flush=True)

    _plot_mode_pd_vs_nd(
        df=df,
        mode=TrialMode.FULL,
        title="Deposited DSGC (t0020) FULL: somatic Vm, PD vs ND",
        output_path=VM_FULL_PD_VS_ND_PNG,
    )
    print(f"  Wrote {VM_FULL_PD_VS_ND_PNG}", flush=True)

    _plot_mode_pd_vs_nd(
        df=df,
        mode=TrialMode.EPSP_PASSIVE,
        title="Deposited DSGC (t0020) EPSP_PASSIVE (HH off, GABA off): PD vs ND",
        output_path=EPSP_PD_VS_ND_PNG,
    )
    print(f"  Wrote {EPSP_PD_VS_ND_PNG}", flush=True)

    _plot_mode_pd_vs_nd(
        df=df,
        mode=TrialMode.IPSP_PASSIVE,
        title="Deposited DSGC (t0020) IPSP_PASSIVE (HH off, AMPA+NMDA off): PD vs ND",
        output_path=IPSP_PD_VS_ND_PNG,
    )
    print(f"  Wrote {IPSP_PD_VS_ND_PNG}", flush=True)

    _plot_three_mode_overlay(
        df=df,
        direction=Condition.PD,
        title="Deposited DSGC (t0020) PD: FULL vs EPSP_PASSIVE vs IPSP_PASSIVE",
        output_path=THREE_MODE_PD_OVERLAY_PNG,
    )
    print(f"  Wrote {THREE_MODE_PD_OVERLAY_PNG}", flush=True)

    _plot_three_mode_overlay(
        df=df,
        direction=Condition.ND,
        title="Deposited DSGC (t0020) ND: FULL vs EPSP_PASSIVE vs IPSP_PASSIVE",
        output_path=THREE_MODE_ND_OVERLAY_PNG,
    )
    print(f"  Wrote {THREE_MODE_ND_OVERLAY_PNG}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
