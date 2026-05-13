"""Render the Hodgkin-Huxley membrane equation plus per-channel current blocks as a PNG.

Source text transcribed verbatim from
``tasks/t0070_writeup_two_model_beds/results/results_detailed.md`` lines 120-134 (Bed A)
and 405-415 (Bed B). Matplotlib mathtext is used so no LaTeX install is required.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from tasks.t0105_preliminary_figures_report.code import constants as cst
from tasks.t0105_preliminary_figures_report.code import paths as pth

# Bed A: HHst.mod L190-L222 BREAKPOINT block (Ca currents zeroed by init_active).
BED_A_MEMBRANE_EQUATION: str = r"$C_m \frac{dV}{dt} = -\sum_i I_i - I_{syn} - I_{inj}$"

BED_A_CHANNEL_LINES: tuple[str, ...] = (
    r"$I_{Na}   = g_{Na}  \cdot m^3 \cdot h \cdot (V - E_{Na})$"
    r"     HHst Na fast",
    r"$I_{Kdr}  = g_{Kdr} \cdot n^4 \cdot (V - E_K)$"
    r"           HHst K delayed rectifier",
    r"$I_{Km}   = g_{Km}  \cdot n_m \cdot (V - E_K)$"
    r"             HHst K M-type",
    r"$I_{leak} = g_{leak} \cdot (V - E_{leak})$"
    r"                 HHst leak (Ca currents zeroed)",
)

# Bed B: HHst_noiseless.mod L184-L222 BREAKPOINT block (Ca currents at defaults).
BED_B_MEMBRANE_EQUATION: str = BED_A_MEMBRANE_EQUATION

BED_B_CHANNEL_LINES: tuple[str, ...] = (
    r"$I_{Na}   = g_{Na}  \cdot m^3 \cdot h \cdot (V - E_{Na})$"
    r"           HHst Na fast (deterministic)",
    r"$I_{Kdr}  = g_{Kdr} \cdot n^4 \cdot (V - E_K)$"
    r"                     HHst K delayed rectifier",
    r"$I_{Km}   = g_{Km}  \cdot n_m \cdot (V - E_K)$"
    r"                       HHst K M-type",
    r"$I_{leak} = g_{leak} \cdot (V - E_{leak})$"
    r"                           HHst leak",
    r"$I_{CaL}  = g_{CaL} \cdot l_m^2 \cdot l_h \cdot (V - E_{Ca})$"
    r"     HHst L-type Ca (active)",
    r"$I_{CaT}  = g_{CaT} \cdot t_m^2 \cdot t_h \cdot (V - E_{Ca})$"
    r"     HHst T-type Ca (active)",
)


def _draw_block(
    *,
    ax: Axes,
    title: str,
    membrane_eq: str,
    channel_lines: tuple[str, ...],
    y_top: float,
) -> None:
    ax.text(
        x=0.0,
        y=y_top,
        s=title,
        fontsize=14,
        fontweight="bold",
        family="sans-serif",
        transform=ax.transAxes,
    )
    ax.text(
        x=0.0,
        y=y_top - 0.10,
        s=membrane_eq,
        fontsize=15,
        family="serif",
        transform=ax.transAxes,
    )
    line_step: float = 0.075
    for idx, line in enumerate(channel_lines):
        ax.text(
            x=0.02,
            y=y_top - 0.22 - idx * line_step,
            s=line,
            fontsize=11,
            family="serif",
            transform=ax.transAxes,
        )


def render_hh_equations_png() -> None:
    pth.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams["text.usetex"] = False
    fig, ax = plt.subplots(figsize=(11.0, 8.5), dpi=cst.DPI)
    ax.axis("off")
    fig.suptitle(
        t="Hodgkin-Huxley membrane equations for the two DSGC model beds",
        fontsize=15,
        fontweight="bold",
    )
    _draw_block(
        ax=ax,
        title=cst.BED_A_LABEL,
        membrane_eq=BED_A_MEMBRANE_EQUATION,
        channel_lines=BED_A_CHANNEL_LINES,
        y_top=0.96,
    )
    _draw_block(
        ax=ax,
        title=cst.BED_B_LABEL,
        membrane_eq=BED_B_MEMBRANE_EQUATION,
        channel_lines=BED_B_CHANNEL_LINES,
        y_top=0.48,
    )
    fig.tight_layout()
    fig.savefig(
        fname=pth.FIG01_HH_EQUATIONS_PNG,
        dpi=cst.DPI,
        facecolor=cst.FACECOLOR,
        bbox_inches=cst.BBOX_INCHES,
    )
    plt.close(fig=fig)


def main() -> None:
    render_hh_equations_png()
    print(f"[t0105] wrote {pth.FIG01_HH_EQUATIONS_PNG}")


if __name__ == "__main__":
    main()
