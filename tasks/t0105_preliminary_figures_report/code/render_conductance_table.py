"""Render per-bed conductance density tables as PNGs.

Row values transcribed verbatim from
``tasks/t0070_writeup_two_model_beds/results/results_detailed.md``: Bed A at lines
158-169 (11 rows), Bed B at lines 452-465 (12 rows). Columns: Channel, gbar (S/cm^2),
E_rev (mV), V_half_act (mV), tau_m, V_half_inact (mV), tau_h, source code/<file>:line.

Kinetic columns reproduce t0070's full audited expressions where they exist; "n/a"
indicates the column is not applicable for that channel (e.g. Km has no inactivation).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt

from tasks.t0105_preliminary_figures_report.code import constants as cst
from tasks.t0105_preliminary_figures_report.code import paths as pth


@dataclass(frozen=True, slots=True)
class ConductanceRow:
    channel: str
    gbar: str
    e_rev: str
    v_half_act: str
    tau_m: str
    v_half_inact: str
    tau_h: str
    source: str


# Bed A: t0070 results_detailed.md L158-L169 (11 rows).
BED_A_ROWS: tuple[ConductanceRow, ...] = (
    ConductanceRow(
        channel="Na (soma)",
        gbar="0.4",
        e_rev="+60",
        v_half_act="(see kinetics: alpha=-0.6*vtrap(V+30,-10))",
        tau_m="1/(alpha+beta)",
        v_half_inact="-44",
        tau_h="hslow/((1+exp((V+30)/4)))+exp(-(V+50)/2))+hfast",
        source="main.hoc:L148 RGCsomana; HHst.mod:L249-L266",
    ),
    ConductanceRow(
        channel="Na (dend)",
        gbar="2e-4",
        e_rev="+60",
        v_half_act="(same kinetics as soma)",
        tau_m="(same)",
        v_half_inact="(same)",
        tau_h="(same)",
        source="main.hoc:L152 RGCdendna",
    ),
    ConductanceRow(
        channel="Kdr (soma)",
        gbar="0.07",
        e_rev="-90",
        v_half_act="(alpha=-0.02*vtrap(V+40,-10))",
        tau_m="1/(alpha+beta)",
        v_half_inact="n/a",
        tau_h="n/a",
        source="main.hoc:L149 RGCsomakv; HHst.mod:L294-L297",
    ),
    ConductanceRow(
        channel="Kdr (dend)",
        gbar="7e-3",
        e_rev="-90",
        v_half_act="(same kinetics as soma)",
        tau_m="(same)",
        v_half_inact="n/a",
        tau_h="n/a",
        source="main.hoc:L153 RGCdendkv",
    ),
    ConductanceRow(
        channel="Km (soma)",
        gbar="5e-4",
        e_rev="-90",
        v_half_act="(linear, taukm=1; alpha=-0.001/taukm*vtrap(V+30,-9))",
        tau_m="1/(alpha+beta)",
        v_half_inact="n/a",
        tau_h="n/a",
        source="main.hoc:L150 RGCsomakm; HHst.mod:L70, L315-L318",
    ),
    ConductanceRow(
        channel="Km (dend)",
        gbar="0",
        e_rev="-90",
        v_half_act="(same kinetics as soma)",
        tau_m="(same)",
        v_half_inact="n/a",
        tau_h="n/a",
        source="main.hoc:L154 RGCdendkm (set to 0)",
    ),
    ConductanceRow(
        channel="Leak (passive)",
        gbar="5e-5",
        e_rev="-60",
        v_half_act="n/a",
        tau_m="n/a",
        v_half_inact="n/a",
        tau_h="n/a",
        source="main.hoc:L161-L162 RGCgpas, e_pas",
    ),
    ConductanceRow(
        channel="Leak (active)",
        gbar="5.5e-4",
        e_rev="-60",
        v_half_act="n/a",
        tau_m="n/a",
        v_half_inact="n/a",
        tau_h="n/a",
        source="main.hoc:L161 RGCgpas*(1+active*10)",
    ),
    ConductanceRow(
        channel="CaL (zeroed)",
        gbar="0",
        e_rev="E_Ca",
        v_half_act="-27 (alpha=0.055*vtrap(-(V+27),3.8))",
        tau_m="1/(alpha+beta)",
        v_half_inact="-13 (alpha=4.57e-4*exp((-13-V)/50))",
        tau_h="1/(alpha+beta)",
        source="main.hoc:L155, L302; HHst.mod:L326-L334",
    ),
    ConductanceRow(
        channel="CaT (zeroed)",
        gbar="0",
        e_rev="E_Ca",
        v_half_act="-50 (tm_inf=1/(1+exp(-(V+50)/7.4)))",
        tau_m="4/(exp((V+25)/20)+exp(-(V+100)/15))",
        v_half_inact="-78 (th_inf=1/(1+exp((V+78)/5)))",
        tau_h="86/(exp((V+46)/4)+exp(-(V+405)/50))",
        source="main.hoc:L156, L303; HHst.mod:L355-L360",
    ),
    ConductanceRow(
        channel="vshift_HHst",
        gbar="n/a",
        e_rev="n/a",
        v_half_act="-4 mV (global voltage shift)",
        tau_m="n/a",
        v_half_inact="n/a",
        tau_h="n/a",
        source="main.hoc:L91; build_cell.py:L312 V_SHIFT_HHST_MV",
    ),
)

# Bed B: t0070 results_detailed.md L452-L465 (12 rows). Units: S/cm^2 throughout.
BED_B_ROWS: tuple[ConductanceRow, ...] = (
    ConductanceRow(
        channel="Na (soma)",
        gbar="0.150",
        e_rev="+60",
        v_half_act="(alpha=-0.6*vtrap(V+30,-10))",
        tau_m="1/(alpha+beta)",
        v_half_inact="-44",
        tau_h="hslow/((1+exp((V+30)/4))+exp(-(V+50)/2))+hfast",
        source="constants.py:L34 GNA_SOMA_MS=150; HHst_noiseless.mod:L244-L261",
    ),
    ConductanceRow(
        channel="Na (primary)",
        gbar="0.200",
        e_rev="+60",
        v_half_act="(same kinetics)",
        tau_m="(same)",
        v_half_inact="(same)",
        tau_h="(same)",
        source="constants.py:L35 GNA_PRIMARY_MS=200",
    ),
    ConductanceRow(
        channel="Na (non-terminal)",
        gbar="0 (zeroed)",
        e_rev="+60",
        v_half_act="(same kinetics)",
        tau_m="(same)",
        v_half_inact="(same)",
        tau_h="(same)",
        source="constants.py:L36 GNA_NON_TERMINAL_MS=0",
    ),
    ConductanceRow(
        channel="Na (terminal)",
        gbar="0.030",
        e_rev="+60",
        v_half_act="(same kinetics)",
        tau_m="(same)",
        v_half_inact="(same)",
        tau_h="(same)",
        source="constants.py:L37 GNA_TERMINAL_MS=30",
    ),
    ConductanceRow(
        channel="Kdr (soma)",
        gbar="0.035",
        e_rev="-90",
        v_half_act="(alpha=-0.02*vtrap(V+40,-10))",
        tau_m="1/(alpha+beta)",
        v_half_inact="n/a",
        tau_h="n/a",
        source="constants.py:L38 GK_SOMA_MS=35; HHst_noiseless.mod:L289-L292",
    ),
    ConductanceRow(
        channel="Kdr (primary)",
        gbar="0.035",
        e_rev="-90",
        v_half_act="(same kinetics)",
        tau_m="(same)",
        v_half_inact="n/a",
        tau_h="n/a",
        source="constants.py:L39 GK_PRIMARY_MS=35",
    ),
    ConductanceRow(
        channel="Kdr (non-term + term)",
        gbar="0.025",
        e_rev="-90",
        v_half_act="(same kinetics)",
        tau_m="(same)",
        v_half_inact="n/a",
        tau_h="n/a",
        source="constants.py:L40 GK_NON_TERMINAL_MS=25",
    ),
    ConductanceRow(
        channel="Km (uniform)",
        gbar="0.003",
        e_rev="-90",
        v_half_act="(linear, taukm=1)",
        tau_m="1/(alpha+beta)",
        v_half_inact="n/a",
        tau_h="n/a",
        source="constants.py:L41 GKM_MS=3; HHst_noiseless.mod:L68",
    ),
    ConductanceRow(
        channel="Leak (uniform)",
        gbar="1.667e-4",
        e_rev="-60",
        v_half_act="n/a",
        tau_m="n/a",
        v_half_inact="n/a",
        tau_h="n/a",
        source="constants.py:L42 G_LEAK_MS=0.1667; build_cell.py:L195,L210",
    ),
    ConductanceRow(
        channel="CaL (uniform)",
        gbar="3e-4",
        e_rev="+132",
        v_half_act="-27 (alpha=0.055*vtrap(-(V+27),3.8))",
        tau_m="1/(alpha+beta)",
        v_half_inact="-13 (alpha=4.57e-4*exp((-13-V)/50))",
        tau_h="1/(alpha+beta)",
        source="HHst_noiseless.mod:L57, L321-L329 (PARAMETER default)",
    ),
    ConductanceRow(
        channel="CaT (uniform)",
        gbar="3e-4",
        e_rev="+132",
        v_half_act="-50 (tm_inf=1/(1+exp(-(V+50)/7.4)))",
        tau_m="4/(exp((V+25)/20)+exp(-(V+100)/15))",
        v_half_inact="-78 (th_inf=1/(1+exp((V+78)/5)))",
        tau_h="86/(exp((V+46)/4)+exp(-(V+405)/50))",
        source="HHst_noiseless.mod:L58, L350-L355 (PARAMETER default)",
    ),
    ConductanceRow(
        channel="cad (Ca decay)",
        gbar="n/a",
        e_rev="n/a",
        v_half_act="depth=0.1 um, cainf=2e-4 mM",
        tau_m="taur=5 ms",
        v_half_inact="n/a",
        tau_h="n/a",
        source="cadecay.mod:L44-L46; build_cell.py:L194, L208",
    ),
)

COLUMN_LABELS: tuple[str, ...] = (
    "Channel",
    "gbar (S/cm^2)",
    "E_rev (mV)",
    "V_half_act (mV)",
    "tau_m",
    "V_half_inact (mV)",
    "tau_h",
    "Source",
)


def _rows_to_cells(*, rows: tuple[ConductanceRow, ...]) -> list[list[str]]:
    return [
        [
            row.channel,
            row.gbar,
            row.e_rev,
            row.v_half_act,
            row.tau_m,
            row.v_half_inact,
            row.tau_h,
            row.source,
        ]
        for row in rows
    ]


def _render_table_png(
    *,
    title: str,
    rows: tuple[ConductanceRow, ...],
    out_png: Path,
) -> None:
    cells: list[list[str]] = _rows_to_cells(rows=rows)
    fig, ax = plt.subplots(figsize=(20.0, 0.5 + 0.55 * (len(rows) + 1)), dpi=cst.DPI)
    ax.axis("off")
    fig.suptitle(t=title, fontsize=14, fontweight="bold")
    table = ax.table(
        cellText=cells,
        colLabels=list(COLUMN_LABELS),
        loc="center",
        cellLoc="left",
        colLoc="left",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(7.5)
    # Wider source column for readability. Positional args because matplotlib
    # Rectangle.set_width / set_height do not accept keyword arguments.
    col_widths: list[float] = [0.09, 0.05, 0.04, 0.18, 0.10, 0.10, 0.18, 0.26]
    cell_height: float = 0.06
    for col_idx, width in enumerate(col_widths):
        for row_idx in range(len(rows) + 1):
            cell = table[row_idx, col_idx]
            cell.set_width(width)
            cell.set_height(cell_height)
    # Bold header.
    for col_idx in range(len(COLUMN_LABELS)):
        header_cell = table[0, col_idx]
        header_cell.set_text_props(weight="bold")
        header_cell.set_facecolor("#dddddd")
    fig.tight_layout()
    fig.savefig(
        fname=out_png,
        dpi=cst.DPI,
        facecolor=cst.FACECOLOR,
        bbox_inches=cst.BBOX_INCHES,
    )
    plt.close(fig=fig)


def render_conductance_tables() -> None:
    pth.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    _render_table_png(
        title=f"Conductance audit: {cst.BED_A_LABEL}",
        rows=BED_A_ROWS,
        out_png=pth.FIG02_TABLE_BED_A_PNG,
    )
    _render_table_png(
        title=f"Conductance audit: {cst.BED_B_LABEL}",
        rows=BED_B_ROWS,
        out_png=pth.FIG02_TABLE_BED_B_PNG,
    )


def main() -> None:
    render_conductance_tables()
    print(f"[t0105] wrote {pth.FIG02_TABLE_BED_A_PNG}")
    print(f"[t0105] wrote {pth.FIG02_TABLE_BED_B_PNG}")


if __name__ == "__main__":
    main()
