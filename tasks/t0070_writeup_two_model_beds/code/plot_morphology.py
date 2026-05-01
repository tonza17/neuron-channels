"""Produce schematic morphology PNGs for Bed A and Bed B.

The two PNGs are illustrative axial schematics — they show compartment topology
(soma + radiating dendrites) and the location of synaptic point processes, but they
are NOT 3D NEURON renderings of `RGCmodel.hoc`'s `shape3d_*` procs (L212-11722).
The figure captions in `results_detailed.md` make this explicit.
"""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np

from tasks.t0070_writeup_two_model_beds.code.constants import (
    BED_A_N_OFF_DEND,
    BED_A_N_ON_DEND,
    BED_B_N_DEND,
    BED_B_N_NONTERM_DEND_APPROX,
    BED_B_N_PRIMARY_DEND_APPROX,
    BED_B_N_TERMINAL_DEND_APPROX,
    COLOR_DEND_NONTERM,
    COLOR_DEND_OFF,
    COLOR_DEND_ON,
    COLOR_DEND_PRIMARY,
    COLOR_DEND_TERM,
    COLOR_GABA,
    COLOR_NMDA,
    COLOR_SOMA,
    FIG_DPI,
    FIG_HEIGHT_IN,
    FIG_WIDTH_IN,
)
from tasks.t0070_writeup_two_model_beds.code.paths import (
    BED_A_MORPH_PNG,
    BED_B_MORPH_PNG,
    IMAGES_DIR,
)
from tasks.t0070_writeup_two_model_beds.code.schematic_helpers import (
    SynapsePlacement,
    draw_dendritic_tree,
)

SOMA_RADIUS_UM: float = 8.0
BRANCH_LENGTH_UM: float = 90.0


def _bed_a_synapses() -> list[SynapsePlacement]:
    """Three triple-marker synapses placed on representative ON dendrite midpoints.

    Each ON dendrite in Bed A carries one BIPsyn (AMPA+NMDA, orange), one SACinhibsyn
    (GABA, blue) and one SACexcsyn (ACh, red), placed at the section midpoint by
    `RGCmodel.hoc:L11825-11851`. We illustrate the placement on 12 representative ON
    branches sampled around the dendritic field.
    """
    n_show: int = 12
    angles_deg: np.ndarray = np.linspace(start=0.0, stop=360.0, num=n_show, endpoint=False)
    radius_um: float = SOMA_RADIUS_UM + 0.5 * BRANCH_LENGTH_UM
    placements: list[SynapsePlacement] = []
    for ang in angles_deg:
        rad: float = math.radians(ang)
        cx: float = radius_um * math.cos(rad)
        cy: float = radius_um * math.sin(rad)
        # Three offset markers per dendrite to denote the synapse triple.
        offset: float = 4.0
        placements.append(
            SynapsePlacement(
                x_um=cx + offset * math.cos(rad + math.pi / 2),
                y_um=cy + offset * math.sin(rad + math.pi / 2),
                color=COLOR_NMDA,  # BIPsyn (AMPA+NMDA bipolar drive)
                marker="o",
                size=12.0,
            )
        )
        placements.append(
            SynapsePlacement(
                x_um=cx,
                y_um=cy,
                color=COLOR_GABA,  # SACinhibsyn (GABA)
                marker="s",
                size=12.0,
            )
        )
        placements.append(
            SynapsePlacement(
                x_um=cx - offset * math.cos(rad + math.pi / 2),
                y_um=cy - offset * math.sin(rad + math.pi / 2),
                color="darkorange",  # SACexcsyn (ACh)
                marker="^",
                size=10.0,
            )
        )
    return placements


def _plot_bed_a_morphology(*, save_path) -> None:  # type: ignore[no-untyped-def]
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=(FIG_WIDTH_IN, FIG_HEIGHT_IN),
        dpi=FIG_DPI,
    )

    # OFF dendrites in the top hemisphere, ON dendrites in the bottom hemisphere
    # purely for illustration; the real Poleg-Polsky sort lives in
    # RGCmodel.hoc:L11801-11803 and uses the z3d/y3d coordinates of each dendrite.
    draw_dendritic_tree(
        ax=ax,
        n_branches=BED_A_N_OFF_DEND,
        branch_color=COLOR_DEND_OFF,
        soma_color=COLOR_SOMA,
        branch_length_um=BRANCH_LENGTH_UM * 0.85,
        soma_radius_um=SOMA_RADIUS_UM,
        synapses=None,
        branch_alpha=0.35,
        branch_lw=0.45,
        angle_start_deg=0.0,
        angle_end_deg=180.0,
    )
    draw_dendritic_tree(
        ax=ax,
        n_branches=BED_A_N_ON_DEND,
        branch_color=COLOR_DEND_ON,
        soma_color=COLOR_SOMA,
        branch_length_um=BRANCH_LENGTH_UM,
        soma_radius_um=SOMA_RADIUS_UM,
        synapses=_bed_a_synapses(),
        branch_alpha=0.55,
        branch_lw=0.55,
        angle_start_deg=180.0,
        angle_end_deg=360.0,
    )

    ax.set_aspect(aspect="equal")
    ax.set_xlim(
        -(SOMA_RADIUS_UM + BRANCH_LENGTH_UM + 25.0), (SOMA_RADIUS_UM + BRANCH_LENGTH_UM + 25.0)
    )
    ax.set_ylim(
        -(SOMA_RADIUS_UM + BRANCH_LENGTH_UM + 25.0), (SOMA_RADIUS_UM + BRANCH_LENGTH_UM + 25.0)
    )
    ax.set_xlabel(xlabel="x (μm, illustrative — not to scale)")
    ax.set_ylabel(ylabel="y (μm, illustrative — not to scale)")
    ax.set_title(
        label=(
            "Bed A: Poleg-Polsky 2016 (t0008) — 1 soma + 350 dends, "
            f"{BED_A_N_ON_DEND} ON / {BED_A_N_OFF_DEND} OFF, 846 point processes"
        ),
        fontsize=11,
    )

    # Legend handles
    legend_handles = [
        plt.Line2D(  # type: ignore[attr-defined]
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=COLOR_SOMA,
            markeredgecolor="black",
            markersize=10,
            label="soma",
        ),
        plt.Line2D(  # type: ignore[attr-defined]
            [0],
            [0],
            color=COLOR_DEND_ON,
            lw=2,
            label=f"ON dendrite (n={BED_A_N_ON_DEND})",
        ),
        plt.Line2D(  # type: ignore[attr-defined]
            [0],
            [0],
            color=COLOR_DEND_OFF,
            lw=2,
            label=f"OFF dendrite (n={BED_A_N_OFF_DEND})",
        ),
        plt.Line2D(  # type: ignore[attr-defined]
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=COLOR_NMDA,
            markeredgecolor="black",
            markersize=8,
            label="BIPsyn (AMPA+NMDA)",
        ),
        plt.Line2D(  # type: ignore[attr-defined]
            [0],
            [0],
            marker="s",
            color="w",
            markerfacecolor=COLOR_GABA,
            markeredgecolor="black",
            markersize=8,
            label="SACinhibsyn (GABA)",
        ),
        plt.Line2D(  # type: ignore[attr-defined]
            [0],
            [0],
            marker="^",
            color="w",
            markerfacecolor="darkorange",
            markeredgecolor="black",
            markersize=8,
            label="SACexcsyn (ACh)",
        ),
    ]
    ax.legend(handles=legend_handles, loc="upper right", fontsize=8, framealpha=0.9)
    ax.grid(visible=True, alpha=0.2)

    fig.tight_layout()
    fig.savefig(fname=save_path, dpi=FIG_DPI)
    plt.close(fig=fig)


def _bed_b_synapses() -> list[SynapsePlacement]:
    """ACh + GABA markers placed at terminal-tier dendrite tips only.

    Each terminal dendrite carries one Exp2Syn ACh (orange) and one Exp2Syn GABA
    (blue) per `_setup_synapses` (run_tuning_curve.py:L189-226). We show 12
    representative terminals around the dendritic field.
    """
    n_show: int = 12
    angles_deg: np.ndarray = np.linspace(start=0.0, stop=360.0, num=n_show, endpoint=False)
    tip_radius_um: float = SOMA_RADIUS_UM + BRANCH_LENGTH_UM - 2.0
    placements: list[SynapsePlacement] = []
    for ang in angles_deg:
        rad: float = math.radians(ang)
        cx: float = tip_radius_um * math.cos(rad)
        cy: float = tip_radius_um * math.sin(rad)
        offset: float = 4.0
        placements.append(
            SynapsePlacement(
                x_um=cx + offset * math.cos(rad + math.pi / 2),
                y_um=cy + offset * math.sin(rad + math.pi / 2),
                color="darkorange",  # ACh Exp2Syn
                marker="^",
                size=14.0,
            )
        )
        placements.append(
            SynapsePlacement(
                x_um=cx - offset * math.cos(rad + math.pi / 2),
                y_um=cy - offset * math.sin(rad + math.pi / 2),
                color=COLOR_GABA,  # GABA Exp2Syn
                marker="s",
                size=14.0,
            )
        )
    return placements


def _plot_bed_b_morphology(*, save_path) -> None:  # type: ignore[no-untyped-def]
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=(FIG_WIDTH_IN, FIG_HEIGHT_IN),
        dpi=FIG_DPI,
    )

    # Inner ring: primary dends (short, dark).
    draw_dendritic_tree(
        ax=ax,
        n_branches=BED_B_N_PRIMARY_DEND_APPROX,
        branch_color=COLOR_DEND_PRIMARY,
        soma_color=COLOR_SOMA,
        branch_length_um=BRANCH_LENGTH_UM * 0.25,
        soma_radius_um=SOMA_RADIUS_UM,
        synapses=None,
        branch_alpha=0.95,
        branch_lw=2.2,
    )
    # Mid ring: non-terminal dends (medium length, mid green).
    draw_dendritic_tree(
        ax=ax,
        n_branches=BED_B_N_NONTERM_DEND_APPROX,
        branch_color=COLOR_DEND_NONTERM,
        soma_color=COLOR_SOMA,
        branch_length_um=BRANCH_LENGTH_UM * 0.55,
        soma_radius_um=SOMA_RADIUS_UM + BRANCH_LENGTH_UM * 0.25,
        synapses=None,
        branch_alpha=0.55,
        branch_lw=0.45,
    )
    # Outer ring: terminal dends (long, light, bear ACh+GABA markers).
    draw_dendritic_tree(
        ax=ax,
        n_branches=BED_B_N_TERMINAL_DEND_APPROX,
        branch_color=COLOR_DEND_TERM,
        soma_color=COLOR_SOMA,
        branch_length_um=BRANCH_LENGTH_UM * 0.20,
        soma_radius_um=SOMA_RADIUS_UM + BRANCH_LENGTH_UM * 0.80,
        synapses=_bed_b_synapses(),
        branch_alpha=0.85,
        branch_lw=0.5,
    )

    ax.set_aspect(aspect="equal")
    ax.set_xlim(
        -(SOMA_RADIUS_UM + BRANCH_LENGTH_UM + 25.0), (SOMA_RADIUS_UM + BRANCH_LENGTH_UM + 25.0)
    )
    ax.set_ylim(
        -(SOMA_RADIUS_UM + BRANCH_LENGTH_UM + 25.0), (SOMA_RADIUS_UM + BRANCH_LENGTH_UM + 25.0)
    )
    ax.set_xlabel(xlabel="x (μm, illustrative — not to scale)")
    ax.set_ylabel(ylabel="y (μm, illustrative — not to scale)")
    ax.set_title(
        label=(
            "Bed B: de Rosenroll 2026 (t0024) — 1 soma + "
            f"{BED_B_N_DEND} dends, ~{BED_B_N_PRIMARY_DEND_APPROX} primary / "
            f"~{BED_B_N_NONTERM_DEND_APPROX} mid / "
            f"~{BED_B_N_TERMINAL_DEND_APPROX} terminal"
        ),
        fontsize=11,
    )

    legend_handles = [
        plt.Line2D(  # type: ignore[attr-defined]
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=COLOR_SOMA,
            markeredgecolor="black",
            markersize=10,
            label="soma",
        ),
        plt.Line2D(  # type: ignore[attr-defined]
            [0],
            [0],
            color=COLOR_DEND_PRIMARY,
            lw=2,
            label=f"primary (~{BED_B_N_PRIMARY_DEND_APPROX})",
        ),
        plt.Line2D(  # type: ignore[attr-defined]
            [0],
            [0],
            color=COLOR_DEND_NONTERM,
            lw=2,
            label=f"non-terminal (~{BED_B_N_NONTERM_DEND_APPROX})",
        ),
        plt.Line2D(  # type: ignore[attr-defined]
            [0],
            [0],
            color=COLOR_DEND_TERM,
            lw=2,
            label=f"terminal (~{BED_B_N_TERMINAL_DEND_APPROX})",
        ),
        plt.Line2D(  # type: ignore[attr-defined]
            [0],
            [0],
            marker="^",
            color="w",
            markerfacecolor="darkorange",
            markeredgecolor="black",
            markersize=8,
            label="ACh Exp2Syn",
        ),
        plt.Line2D(  # type: ignore[attr-defined]
            [0],
            [0],
            marker="s",
            color="w",
            markerfacecolor=COLOR_GABA,
            markeredgecolor="black",
            markersize=8,
            label="GABA Exp2Syn",
        ),
    ]
    ax.legend(handles=legend_handles, loc="upper right", fontsize=8, framealpha=0.9)
    ax.grid(visible=True, alpha=0.2)

    fig.tight_layout()
    fig.savefig(fname=save_path, dpi=FIG_DPI)
    plt.close(fig=fig)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    _plot_bed_a_morphology(save_path=BED_A_MORPH_PNG)
    _plot_bed_b_morphology(save_path=BED_B_MORPH_PNG)
    print(f"wrote {BED_A_MORPH_PNG} ({BED_A_MORPH_PNG.stat().st_size} bytes)")
    print(f"wrote {BED_B_MORPH_PNG} ({BED_B_MORPH_PNG.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
