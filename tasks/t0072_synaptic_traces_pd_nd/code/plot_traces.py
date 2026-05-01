"""Generate the Bed A and Bed B multi-panel synaptic-trace figures.

Loads ``data/aggregated.npz`` and produces two PNGs in ``results/images/``:

* ``bed_a_synaptic_traces.png`` — 4 rows (AMPA, NMDA, GABA, ACh) x 2 cols (g, I)
* ``bed_b_synaptic_traces.png`` — 2 rows (ACh, GABA) x 2 cols (g, I)

Each panel overlays PD (blue) and ND (red) population mean as a solid line plus a
+/- 1 SD shaded band, so the direction-encoding mechanism is visually obvious per
synapse type.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from tasks.t0072_synaptic_traces_pd_nd.code.constants import (
    QTY_G,
    QTY_I,
    STAT_MEAN,
    STAT_SD,
    T_MS_KEY,
    Bed,
    Direction,
    RecordedSynapseType,
)
from tasks.t0072_synaptic_traces_pd_nd.code.paths import (
    AGGREGATED_NPZ,
    BED_A_FIG_PNG,
    BED_B_FIG_PNG,
    IMAGES_DIR,
)

# Matplotlib colour conventions.
PD_COLOUR: str = "C0"  # blue
ND_COLOUR: str = "C3"  # red
SD_BAND_ALPHA: float = 0.25
LINE_WIDTH: float = 1.5
DPI: int = 150


def _aggregated_key(
    *,
    bed: Bed,
    direction: Direction,
    synapse_type: RecordedSynapseType,
    quantity: str,
    stat: str,
) -> str:
    return f"{bed.value}_{direction.value}_{synapse_type.value}_{quantity}_{stat}"


def _plot_one_panel(
    *,
    ax: plt.Axes,
    t_ms: np.ndarray,
    pd_mean: np.ndarray,
    pd_sd: np.ndarray,
    nd_mean: np.ndarray,
    nd_sd: np.ndarray,
    title: str,
    y_label: str,
    show_legend: bool,
) -> None:
    """Draw PD and ND mean +/- SD on one panel."""
    ax.plot(t_ms, pd_mean, color=PD_COLOUR, linewidth=LINE_WIDTH, label="PD")
    ax.fill_between(
        t_ms,
        pd_mean - pd_sd,
        pd_mean + pd_sd,
        color=PD_COLOUR,
        alpha=SD_BAND_ALPHA,
        linewidth=0,
    )
    ax.plot(t_ms, nd_mean, color=ND_COLOUR, linewidth=LINE_WIDTH, label="ND")
    ax.fill_between(
        t_ms,
        nd_mean - nd_sd,
        nd_mean + nd_sd,
        color=ND_COLOUR,
        alpha=SD_BAND_ALPHA,
        linewidth=0,
    )
    ax.set_title(title, fontsize=10)
    ax.set_ylabel(y_label, fontsize=9)
    ax.grid(True, linewidth=0.3, alpha=0.5)
    ax.tick_params(axis="both", labelsize=8)
    if show_legend:
        ax.legend(loc="upper right", fontsize=8)


def _plot_bed_figure(
    *,
    bed: Bed,
    synapse_types: list[RecordedSynapseType],
    output_path: Path,
    title: str,
    fig_size: tuple[float, float],
) -> None:
    """Render and save one bed's multi-panel figure."""
    data = np.load(AGGREGATED_NPZ)
    t_ms: np.ndarray = data[T_MS_KEY]

    n_rows: int = len(synapse_types)
    fig: Figure
    fig, axes_arr = plt.subplots(nrows=n_rows, ncols=2, figsize=fig_size, sharex=True)
    # Normalise axes_arr to a 2D ndarray of Axes whether n_rows == 1 or > 1.
    axes: np.ndarray = np.atleast_2d(axes_arr)

    for row, syn_type in enumerate(synapse_types):
        # g (col 0) and I (col 1).
        for col, (qty, units, qty_label) in enumerate(
            [(QTY_G, "nS", "conductance"), (QTY_I, "pA", "current")]
        ):
            pd_mean: np.ndarray = data[
                _aggregated_key(
                    bed=bed,
                    direction=Direction.PD,
                    synapse_type=syn_type,
                    quantity=qty,
                    stat=STAT_MEAN,
                )
            ]
            pd_sd: np.ndarray = data[
                _aggregated_key(
                    bed=bed,
                    direction=Direction.PD,
                    synapse_type=syn_type,
                    quantity=qty,
                    stat=STAT_SD,
                )
            ]
            nd_mean: np.ndarray = data[
                _aggregated_key(
                    bed=bed,
                    direction=Direction.ND,
                    synapse_type=syn_type,
                    quantity=qty,
                    stat=STAT_MEAN,
                )
            ]
            nd_sd: np.ndarray = data[
                _aggregated_key(
                    bed=bed,
                    direction=Direction.ND,
                    synapse_type=syn_type,
                    quantity=qty,
                    stat=STAT_SD,
                )
            ]
            _plot_one_panel(
                ax=axes[row, col],
                t_ms=t_ms,
                pd_mean=pd_mean,
                pd_sd=pd_sd,
                nd_mean=nd_mean,
                nd_sd=nd_sd,
                title=f"{syn_type.value.upper()} {qty_label} ({qty} in {units})",
                y_label=f"{qty} ({units})",
                show_legend=(row == 0 and col == 0),
            )
    # x labels on bottom row only.
    for col in range(2):
        axes[n_rows - 1, col].set_xlabel("Time (ms)", fontsize=9)

    fig.suptitle(title, fontsize=12, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.99))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {output_path.name}: size={output_path.stat().st_size} B (n_rows={n_rows})")


def main() -> int:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating Bed A figure (4 rows x 2 cols)...")
    _plot_bed_figure(
        bed=Bed.BED_A,
        synapse_types=[
            RecordedSynapseType.AMPA,
            RecordedSynapseType.NMDA,
            RecordedSynapseType.GABA,
            RecordedSynapseType.ACH,
        ],
        output_path=BED_A_FIG_PNG,
        title=(
            "Bed A (Poleg-Polsky 2016 deposited DSGC) - "
            "synaptic conductances and currents, PD vs ND, "
            "population mean +/- 1 SD across 282 ON-dendrite synapses"
        ),
        fig_size=(12.0, 14.0),
    )

    print("\nGenerating Bed B figure (2 rows x 2 cols)...")
    _plot_bed_figure(
        bed=Bed.BED_B,
        synapse_types=[RecordedSynapseType.ACH, RecordedSynapseType.GABA],
        output_path=BED_B_FIG_PNG,
        title=(
            "Bed B (de Rosenroll 2026 DSGC port) - "
            "synaptic conductances and currents, PD vs ND, "
            "population mean +/- 1 SD across terminal-dendrite synapses"
        ),
        fig_size=(12.0, 7.5),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
