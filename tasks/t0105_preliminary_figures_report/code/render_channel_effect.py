"""Render the unified channel-effect-on-DSI panel from t0067 / t0068 / t0069.

Three subpanels:
* Soma sweep (t0067): DSI vs channel density, one line per channel.
* Nav1.6+Kv3 rescue (t0068): DSI vs nav16 density, coloured by kv3 density.
* AIS-localised sweep (t0069): DSI vs channel density, one line per channel.

Y-axis (DSI) is shared across all three subplots for visual comparability.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from pydantic import BaseModel, ConfigDict, TypeAdapter

from tasks.t0105_preliminary_figures_report.code import constants as cst
from tasks.t0105_preliminary_figures_report.code import paths as pth


class SweepCondition(BaseModel):
    """One row from a dsi_by_condition.json sweep."""

    model_config = ConfigDict(extra="ignore")

    condition_id: str
    channel: str | None = None
    density_label: str | None = None
    density_mS_cm2: float | None = None
    nav16_mS_cm2: float | None = None
    kv3_mS_cm2: float | None = None
    dsi: float | None = None


class SweepFile(BaseModel):
    model_config = ConfigDict(extra="ignore")

    conditions: list[SweepCondition]


_SWEEP_FILE_ADAPTER: TypeAdapter[SweepFile] = TypeAdapter(SweepFile)


def _load_sweep(*, json_path: Path) -> list[SweepCondition]:
    parsed: SweepFile = _SWEEP_FILE_ADAPTER.validate_json(
        json_path.read_bytes(),
    )
    return parsed.conditions


def _plot_soma_sweep(
    *,
    ax: Axes,
    conditions: list[SweepCondition],
    title: str,
) -> None:
    # Group by channel; skip baseline (channel=='none').
    by_channel: dict[str, list[SweepCondition]] = {}
    baseline_dsi: float | None = None
    for c in conditions:
        if c.channel is None or c.channel == "none":
            if c.dsi is not None:
                baseline_dsi = c.dsi
            continue
        by_channel.setdefault(c.channel, []).append(c)
    cmap = plt.get_cmap("tab10")
    for idx, (channel, rows) in enumerate(sorted(by_channel.items())):
        rows_sorted: list[SweepCondition] = sorted(
            rows,
            key=lambda r: r.density_mS_cm2 if r.density_mS_cm2 is not None else 0.0,
        )
        xs: list[float] = [
            r.density_mS_cm2 if r.density_mS_cm2 is not None else 0.0 for r in rows_sorted
        ]
        ys: list[float] = [r.dsi if r.dsi is not None else 0.0 for r in rows_sorted]
        ax.plot(
            xs,
            ys,
            marker="o",
            label=channel,
            color=cmap(idx),
            linewidth=1.5,
        )
    if baseline_dsi is not None:
        ax.axhline(
            y=baseline_dsi,
            color="black",
            linestyle="--",
            linewidth=1.0,
            alpha=0.6,
            label=f"baseline (DSI={baseline_dsi:.2f})",
        )
    ax.set_xscale(value="symlog", linthresh=1.0)
    ax.set_xlabel(xlabel="channel density (mS/cm^2, symlog)", fontsize=9)
    ax.set_ylabel(ylabel="DSI", fontsize=9)
    ax.set_title(label=title, fontsize=10)
    ax.set_ylim(bottom=cst.DSI_Y_MIN, top=cst.DSI_Y_MAX)
    ax.grid(visible=True, alpha=0.3)
    ax.legend(loc="lower left", fontsize=7, frameon=True)


def _plot_rescue(
    *,
    ax: Axes,
    conditions: list[SweepCondition],
    title: str,
) -> None:
    # Bubble-style scatter: x = nav16 density, y = DSI, colour = kv3 density.
    xs: list[float] = []
    ys: list[float] = []
    cs: list[float] = []
    for c in conditions:
        if c.nav16_mS_cm2 is None or c.dsi is None:
            continue
        xs.append(c.nav16_mS_cm2)
        ys.append(c.dsi)
        cs.append(c.kv3_mS_cm2 if c.kv3_mS_cm2 is not None else 0.0)
    sc = ax.scatter(
        x=xs,
        y=ys,
        c=cs,
        cmap="viridis",
        s=80,
        edgecolors="black",
        linewidths=0.5,
    )
    plt.colorbar(mappable=sc, ax=ax, label="Kv3 density (mS/cm^2)")
    ax.set_xlabel(xlabel="Nav1.6 density (mS/cm^2)", fontsize=9)
    ax.set_ylabel(ylabel="DSI", fontsize=9)
    ax.set_title(label=title, fontsize=10)
    ax.set_ylim(bottom=cst.DSI_Y_MIN, top=cst.DSI_Y_MAX)
    ax.grid(visible=True, alpha=0.3)


def render_channel_effect() -> None:
    pth.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    soma_conds: list[SweepCondition] = _load_sweep(json_path=pth.T0067_DSI_JSON)
    rescue_conds: list[SweepCondition] = _load_sweep(json_path=pth.T0068_DSI_JSON)
    ais_conds: list[SweepCondition] = _load_sweep(json_path=pth.T0069_DSI_JSON)
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18.0, 5.5), dpi=cst.DPI)
    _plot_soma_sweep(
        ax=axes[0],
        conditions=soma_conds,
        title="A) Soma sweep (t0067) -- DSI vs channel density",
    )
    _plot_rescue(
        ax=axes[1],
        conditions=rescue_conds,
        title="B) Nav1.6 + Kv3 rescue (t0068)",
    )
    _plot_soma_sweep(
        ax=axes[2],
        conditions=ais_conds,
        title="C) AIS-localised sweep (t0069)",
    )
    # Unify y-axis.
    for ax in axes.ravel():
        ax.set_ylim(bottom=cst.DSI_Y_MIN, top=cst.DSI_Y_MAX)
    # Sanity print of available y-ranges for the three sweeps.
    print(
        "[t0105] channel-effect DSI ranges:",
        f"soma=[{min(c.dsi for c in soma_conds if c.dsi is not None):.2f},"
        f"{max(c.dsi for c in soma_conds if c.dsi is not None):.2f}]",
        f"rescue=[{min(c.dsi for c in rescue_conds if c.dsi is not None):.2f},"
        f"{max(c.dsi for c in rescue_conds if c.dsi is not None):.2f}]",
        f"ais=[{min(c.dsi for c in ais_conds if c.dsi is not None):.2f},"
        f"{max(c.dsi for c in ais_conds if c.dsi is not None):.2f}]",
    )
    fig.suptitle(
        t="Channel-introduction effect on DSI -- shared y-axis across t0067, t0068, t0069",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.94))
    fig.savefig(
        fname=pth.FIG06_CHANNEL_EFFECT_PNG,
        dpi=cst.DPI,
        facecolor=cst.FACECOLOR,
        bbox_inches=cst.BBOX_INCHES,
    )
    plt.close(fig=fig)


def main() -> None:
    render_channel_effect()
    print(f"[t0105] wrote {pth.FIG06_CHANNEL_EFFECT_PNG}")


if __name__ == "__main__":
    main()
