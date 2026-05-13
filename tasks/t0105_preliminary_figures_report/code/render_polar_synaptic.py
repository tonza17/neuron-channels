"""Render two-point polar synaptic plots for Bed A and Bed B.

Only PD (0 deg) and ND (180 deg) data are available in either dependency task,
confirmed in research_code.md. Plot is rendered as a two-radius polar with PD at 0
deg and ND at 180 deg, and the title makes the two-point limitation explicit.

Sources:
* Bed A: ``tasks/t0046_reproduce_poleg_polsky_2016_exact/results/data/fig1_psp.csv``
  (peak_psp_mv, mean over the four trial seeds per direction, gnmda_ns=0.5 condition).
* Bed B: ``tasks/t0066_t0024_epsp_ipsp_vm_protocol/data/voltage_traces.csv`` (peak
  depolarisation v_mv.max() - v_mv.min() for mode=FULL, per direction, mean over
  trials).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # type: ignore[import-untyped]
from matplotlib.projections.polar import PolarAxes
from numpy import dtype
from pandas.api.extensions import ExtensionDtype  # type: ignore[import-untyped]

from tasks.t0105_preliminary_figures_report.code import constants as cst
from tasks.t0105_preliminary_figures_report.code import paths as pth


@dataclass(frozen=True, slots=True)
class PolarTwoPoint:
    bed_label: str
    pd_radius: float
    nd_radius: float
    radial_unit: str
    title_extra: str


T0046_PSP_DTYPES: dict[str, dtype[np.generic] | ExtensionDtype] = {
    "trial_seed": pd.Int64Dtype(),
    "direction_label": pd.StringDtype(),
    "direction_deg": pd.Int64Dtype(),
    "peak_psp_mv": np.dtype("float64"),
}

T0066_TRACES_DTYPES: dict[str, dtype[np.generic] | ExtensionDtype] = {
    "mode": pd.StringDtype(),
    "direction": pd.StringDtype(),
    "trial": pd.Int64Dtype(),
    "t_ms": np.dtype("float64"),
    "v_mv": np.dtype("float64"),
}


def _load_bed_a_two_point() -> PolarTwoPoint:
    df: pd.DataFrame = pd.read_csv(
        filepath_or_buffer=pth.T0046_PSP_CSV,
        dtype=T0046_PSP_DTYPES,
        usecols=list(T0046_PSP_DTYPES.keys()),
    )
    assert len(df) > 0, "t0046 fig1_psp.csv non-empty"
    means: pd.Series[float] = df.groupby(by=cst.COL_DIRECTION_LABEL)[cst.COL_PEAK_PSP_MV].mean()
    pd_radius: float = float(means.loc[cst.DIRECTION_PD])
    nd_radius: float = float(means.loc[cst.DIRECTION_ND])
    return PolarTwoPoint(
        bed_label=cst.BED_A_LABEL,
        pd_radius=pd_radius,
        nd_radius=nd_radius,
        radial_unit="mean peak PSP (mV)",
        title_extra="(source: t0046/fig1_psp.csv, mean across 4 seeds)",
    )


def _load_bed_b_two_point() -> PolarTwoPoint:
    df: pd.DataFrame = pd.read_csv(
        filepath_or_buffer=pth.T0066_TRACES_CSV,
        dtype=T0066_TRACES_DTYPES,
        usecols=list(T0066_TRACES_DTYPES.keys()),
    )
    assert len(df) > 0, "t0066 voltage_traces.csv non-empty"
    df_full: pd.DataFrame = df[df[cst.COL_MODE] == cst.MODE_FULL].copy()
    # Per-trial peak depolarisation, then mean across trials per direction.
    peaks: pd.DataFrame = (
        df_full.groupby(by=[cst.COL_DIRECTION, cst.COL_TRIAL])[cst.COL_V_MV]
        .agg(lambda series: float(series.max()) - float(series.min()))
        .reset_index(name="peak_dep_mv")
    )
    mean_peaks: pd.Series[float] = peaks.groupby(by=cst.COL_DIRECTION)["peak_dep_mv"].mean()
    pd_radius: float = float(mean_peaks.loc[cst.DIRECTION_PD])
    nd_radius: float = float(mean_peaks.loc[cst.DIRECTION_ND])
    return PolarTwoPoint(
        bed_label=cst.BED_B_LABEL,
        pd_radius=pd_radius,
        nd_radius=nd_radius,
        radial_unit="mean peak depolarisation (mV)",
        title_extra="(source: t0066/voltage_traces.csv FULL mode, peak Vm)",
    )


def _draw_two_point_polar(
    *,
    point: PolarTwoPoint,
    out_png: Path,
) -> None:
    angles_rad: np.ndarray = np.array(
        [np.deg2rad(cst.PD_ANGLE_DEG), np.deg2rad(cst.ND_ANGLE_DEG)],
        dtype=np.float64,
    )
    radii: np.ndarray = np.array([point.pd_radius, point.nd_radius], dtype=np.float64)
    fig, ax_raw = plt.subplots(
        figsize=(6.5, 6.5),
        dpi=cst.DPI,
        subplot_kw={"projection": "polar"},
    )
    ax: PolarAxes = cast(PolarAxes, ax_raw)
    ax.set_theta_direction(direction=1)
    ax.set_theta_offset(offset=0.0)
    # Plot the two-point segment plus markers.
    ax.plot(
        angles_rad,
        radii,
        color="tab:blue",
        linewidth=2.0,
        marker="o",
        markersize=12,
        label="PD vs ND",
    )
    # Annotate each point.
    ax.annotate(
        text=f"PD ({point.pd_radius:.2f})",
        xy=(angles_rad[0], radii[0]),
        xytext=(10, 10),
        textcoords="offset points",
        fontsize=11,
    )
    ax.annotate(
        text=f"ND ({point.nd_radius:.2f})",
        xy=(angles_rad[1], radii[1]),
        xytext=(-10, -20),
        textcoords="offset points",
        fontsize=11,
    )
    # Preferred-direction arrow (the direction with the larger radius).
    pref_idx: int = int(np.argmax(radii))
    ax.annotate(
        text="",
        xy=(float(angles_rad[pref_idx]), float(radii[pref_idx])),
        xytext=(0.0, 0.0),
        xycoords="polar",
        arrowprops={"arrowstyle": "->", "color": "red", "lw": 2.0},
    )
    title: str = (
        f"{point.bed_label} two-point polar -- full angular tuning not measured\n"
        f"{point.radial_unit}\n{point.title_extra}"
    )
    ax.set_title(label=title, fontsize=11, pad=18.0)
    ax.legend(loc="lower right", frameon=True, bbox_to_anchor=(1.15, -0.05))
    fig.tight_layout()
    fig.savefig(
        fname=out_png,
        dpi=cst.DPI,
        facecolor=cst.FACECOLOR,
        bbox_inches=cst.BBOX_INCHES,
    )
    plt.close(fig=fig)


def render_polar_synaptic() -> None:
    pth.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    pth.DATA_DIR.mkdir(parents=True, exist_ok=True)
    bed_a: PolarTwoPoint = _load_bed_a_two_point()
    _draw_two_point_polar(point=bed_a, out_png=pth.FIG04_BED_A_POLAR_PNG)
    bed_b: PolarTwoPoint = _load_bed_b_two_point()
    _draw_two_point_polar(point=bed_b, out_png=pth.FIG04_BED_B_POLAR_PNG)


def main() -> None:
    render_polar_synaptic()
    print(f"[t0105] wrote {pth.FIG04_BED_A_POLAR_PNG}")
    print(f"[t0105] wrote {pth.FIG04_BED_B_POLAR_PNG}")


if __name__ == "__main__":
    main()
