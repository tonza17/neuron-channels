"""Produce PD-vs-ND synaptic-conductance schematic PNGs for Bed A and Bed B.

Each PNG is a two-row figure: top row = preferred direction (PD), bottom row = null
direction (ND). Conductance traces are computed from the kinetic constants in
`constants.py`, scaled by the bed-specific direction-encoding mechanism (Bed A:
`gabaMOD` modulation-envelope scalar; Bed B: per-synapse arrival-time shift plus
sigmoidal release-probability), and plotted over a single representative trial
window of `TRACE_DURATION_MS` milliseconds. The traces are illustrative — they are
generated analytically, not by a NEURON simulation — so the figures support the
writeup's documentation purpose without re-running the t0065/t0066 protocols.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from tasks.t0070_writeup_two_model_beds.code.constants import (
    BAR_ARRIVAL_BASELINE_MS,
    BED_A_AMPA_PEAK_NS,
    BED_A_AMPA_TAU_MS,
    BED_A_GABA_PEAK_NS,
    BED_A_GABA_TAU_MS,
    BED_A_GABAMOD_ND,
    BED_A_GABAMOD_PD,
    BED_A_NMDA_PEAK_NS,
    BED_A_NMDA_TAU_DECAY_MS,
    BED_A_NMDA_TAU_RISE_MS,
    BED_B_ACH_TAU_DECAY_MS,
    BED_B_ACH_TAU_RISE_MS,
    BED_B_ACH_WEIGHT_US,
    BED_B_BAR_VELOCITY_UM_PER_MS,
    BED_B_GABA_PROB_ND,
    BED_B_GABA_PROB_PD,
    BED_B_GABA_TAU_DECAY_MS,
    BED_B_GABA_TAU_RISE_MS,
    BED_B_GABA_WEIGHT_US,
    BED_B_TERMINAL_SPACING_UM,
    COLOR_ACH,
    COLOR_GABA,
    COLOR_NMDA,
    FIG_DPI,
    FIG_HEIGHT_IN,
    FIG_WIDTH_IN,
    TRACE_DT_MS,
    TRACE_DURATION_MS,
)
from tasks.t0070_writeup_two_model_beds.code.paths import (
    BED_A_SYNDIAG_PNG,
    BED_B_SYNDIAG_PNG,
    IMAGES_DIR,
)
from tasks.t0070_writeup_two_model_beds.code.schematic_helpers import (
    bi_exponential_trace,
    single_exponential_trace,
    time_axis,
)

N_BED_B_REPRESENTATIVE_TERMINALS: int = 5


def _plot_bed_a_panel(*, ax: Axes, gabamod: float, panel_title: str) -> None:
    t_ms: np.ndarray = time_axis(duration_ms=TRACE_DURATION_MS, dt_ms=TRACE_DT_MS)

    g_ampa: np.ndarray = single_exponential_trace(
        t_ms=t_ms,
        t0_ms=BAR_ARRIVAL_BASELINE_MS,
        tau_ms=BED_A_AMPA_TAU_MS,
        peak=BED_A_AMPA_PEAK_NS,
    )
    g_nmda: np.ndarray = bi_exponential_trace(
        t_ms=t_ms,
        t0_ms=BAR_ARRIVAL_BASELINE_MS,
        tau_rise_ms=BED_A_NMDA_TAU_RISE_MS,
        tau_decay_ms=BED_A_NMDA_TAU_DECAY_MS,
        peak=BED_A_NMDA_PEAK_NS,
    )
    g_gaba_unscaled: np.ndarray = single_exponential_trace(
        t_ms=t_ms,
        t0_ms=BAR_ARRIVAL_BASELINE_MS,
        tau_ms=BED_A_GABA_TAU_MS,
        peak=BED_A_GABA_PEAK_NS,
    )
    g_gaba: np.ndarray = g_gaba_unscaled * gabamod

    ax.plot(t_ms, g_ampa, color="orange", lw=1.6, label="g_AMPA (bipNMDA)")
    ax.plot(t_ms, g_nmda, color=COLOR_NMDA, lw=1.6, label="g_NMDA (bipNMDA, Mg-block)")
    ax.plot(
        t_ms,
        g_gaba,
        color=COLOR_GABA,
        lw=1.8,
        label=f"g_GABA × gabaMOD={gabamod:.2f} (SACinhib)",
    )
    ax.axvline(x=BAR_ARRIVAL_BASELINE_MS, color="gray", ls="--", lw=0.6, alpha=0.7)
    ax.text(
        x=BAR_ARRIVAL_BASELINE_MS + 1.0,
        y=ax.get_ylim()[1] * 0.05 if ax.get_ylim()[1] != 0 else 0.02,
        s="bar arrival",
        fontsize=7,
        color="gray",
    )
    ax.set_xlim(0.0, TRACE_DURATION_MS)
    ax.set_ylabel(ylabel="g (nS)")
    ax.set_title(label=panel_title, fontsize=10)
    ax.grid(visible=True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=7, framealpha=0.9)


def _plot_bed_a_synaptic_diagram(*, save_path) -> None:  # type: ignore[no-untyped-def]
    fig, axes = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(FIG_WIDTH_IN, FIG_HEIGHT_IN),
        dpi=FIG_DPI,
        sharex=True,
        sharey=True,
    )
    _plot_bed_a_panel(
        ax=axes[0],
        gabamod=BED_A_GABAMOD_PD,
        panel_title=(
            f"Bed A — Preferred direction (PD): gabaMOD = {BED_A_GABAMOD_PD:.2f} "
            f"(weak inhibition); excitation symmetric across PD/ND"
        ),
    )
    _plot_bed_a_panel(
        ax=axes[1],
        gabamod=BED_A_GABAMOD_ND,
        panel_title=(
            f"Bed B — Null direction (ND): gabaMOD = {BED_A_GABAMOD_ND:.2f} "
            f"(strong inhibition, ~3× PD); excitation unchanged"
        ),
    )
    axes[1].set_xlabel(xlabel="time (ms)")

    # Patch the second-row title to read "Bed A —" not "Bed B —"
    axes[1].set_title(
        label=(
            f"Bed A — Null direction (ND): gabaMOD = {BED_A_GABAMOD_ND:.2f} "
            f"(strong inhibition, ~3× PD); excitation unchanged"
        ),
        fontsize=10,
    )

    fig.suptitle(
        t=(
            "Bed A synaptic conductance schematic — gabaMOD modulation-envelope swap "
            "(t0020 / t0065 PD/ND convention)"
        ),
        fontsize=12,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    fig.savefig(fname=save_path, dpi=FIG_DPI)
    plt.close(fig=fig)


def _bed_b_arrival_times(
    *,
    direction_deg: float,
    n_terminals: int,
    spacing_um: float,
    velocity_um_per_ms: float,
    baseline_ms: float,
) -> np.ndarray:
    """Compute illustrative bar arrival times for `n_terminals` synapses.

    Mirrors `_bar_arrival_times` (run_tuning_curve.py:L92-109): synapses placed at
    `x = i * spacing_um` along the bar's velocity axis are activated at staggered
    times `baseline + x_proj / velocity`. For PD (`direction_deg == 0.0`) the
    leftmost synapse arrives first; for ND (`direction_deg == 180.0`) the order is
    reversed because the velocity vector flips.
    """
    assert direction_deg in (0.0, 180.0), "direction is PD (0°) or ND (180°)"
    positions_um: np.ndarray = np.arange(n_terminals) * spacing_um
    if direction_deg == 0.0:
        proj_um: np.ndarray = positions_um
    else:
        proj_um = positions_um.max() - positions_um
    return baseline_ms + proj_um / velocity_um_per_ms


def _plot_bed_b_panel(
    *,
    ax: Axes,
    direction_deg: float,
    gaba_release_prob: float,
    panel_title: str,
) -> None:
    t_ms: np.ndarray = time_axis(duration_ms=TRACE_DURATION_MS, dt_ms=TRACE_DT_MS)
    arrival_times_ms: np.ndarray = _bed_b_arrival_times(
        direction_deg=direction_deg,
        n_terminals=N_BED_B_REPRESENTATIVE_TERMINALS,
        spacing_um=BED_B_TERMINAL_SPACING_UM,
        velocity_um_per_ms=BED_B_BAR_VELOCITY_UM_PER_MS,
        baseline_ms=BAR_ARRIVAL_BASELINE_MS,
    )

    # Sum of per-terminal Exp2Syn ACh conductances. Each Exp2Syn delivers a unit
    # weight `BED_B_ACH_WEIGHT_US` (µS) per release event, normalised to peak.
    g_ach_total: np.ndarray = np.zeros_like(t_ms)
    for t0 in arrival_times_ms:
        g_ach_total = g_ach_total + bi_exponential_trace(
            t_ms=t_ms,
            t0_ms=float(t0),
            tau_rise_ms=BED_B_ACH_TAU_RISE_MS,
            tau_decay_ms=BED_B_ACH_TAU_DECAY_MS,
            peak=BED_B_ACH_WEIGHT_US * 1000.0,  # µS → nS for visual scaling
        )

    # GABA: same arrival-time staggering, scaled by direction-encoded release prob.
    g_gaba_total: np.ndarray = np.zeros_like(t_ms)
    for t0 in arrival_times_ms:
        g_gaba_total = g_gaba_total + bi_exponential_trace(
            t_ms=t_ms,
            t0_ms=float(t0),
            tau_rise_ms=BED_B_GABA_TAU_RISE_MS,
            tau_decay_ms=BED_B_GABA_TAU_DECAY_MS,
            peak=gaba_release_prob * BED_B_GABA_WEIGHT_US * 1000.0,
        )

    ax.plot(
        t_ms,
        g_ach_total,
        color=COLOR_ACH,
        lw=1.8,
        label=f"Σ g_ACh ({N_BED_B_REPRESENTATIVE_TERMINALS} terminals, Exp2Syn)",
    )
    ax.plot(
        t_ms,
        g_gaba_total,
        color=COLOR_GABA,
        lw=1.8,
        label=(
            f"Σ g_GABA × p_rel = {gaba_release_prob:.2f} "
            f"({N_BED_B_REPRESENTATIVE_TERMINALS} terminals, Exp2Syn)"
        ),
    )
    for i, t0 in enumerate(arrival_times_ms):
        ax.axvline(x=float(t0), color="gray", ls=":", lw=0.4, alpha=0.7)
        ax.text(
            x=float(t0) + 0.5,
            y=0.01,
            s=f"t{i}",
            fontsize=6,
            color="gray",
        )
    ax.set_xlim(0.0, TRACE_DURATION_MS)
    ax.set_ylabel(ylabel="Σ g (nS, illustrative)")
    ax.set_title(label=panel_title, fontsize=10)
    ax.grid(visible=True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=7, framealpha=0.9)


def _plot_bed_b_synaptic_diagram(*, save_path) -> None:  # type: ignore[no-untyped-def]
    fig, axes = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(FIG_WIDTH_IN, FIG_HEIGHT_IN),
        dpi=FIG_DPI,
        sharex=True,
        sharey=True,
    )
    _plot_bed_b_panel(
        ax=axes[0],
        direction_deg=0.0,
        gaba_release_prob=BED_B_GABA_PROB_PD,
        panel_title=(
            "Bed B — Preferred direction (PD, 0°): bar sweeps left→right; per-synapse "
            f"GABA p_rel ≈ {BED_B_GABA_PROB_PD:.2f}"
        ),
    )
    _plot_bed_b_panel(
        ax=axes[1],
        direction_deg=180.0,
        gaba_release_prob=BED_B_GABA_PROB_ND,
        panel_title=(
            "Bed B — Null direction (ND, 180°): bar sweeps right→left; per-synapse "
            f"GABA p_rel ≈ {BED_B_GABA_PROB_ND:.2f}"
        ),
    )
    axes[1].set_xlabel(xlabel="time (ms)")
    fig.suptitle(
        t=(
            "Bed B synaptic conductance schematic — bar-direction swap + sigmoidal "
            "release-probability (t0024 / t0066 PD/ND convention)"
        ),
        fontsize=12,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    fig.savefig(fname=save_path, dpi=FIG_DPI)
    plt.close(fig=fig)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    _plot_bed_a_synaptic_diagram(save_path=BED_A_SYNDIAG_PNG)
    _plot_bed_b_synaptic_diagram(save_path=BED_B_SYNDIAG_PNG)
    print(f"wrote {BED_A_SYNDIAG_PNG} ({BED_A_SYNDIAG_PNG.stat().st_size} bytes)")
    print(f"wrote {BED_B_SYNDIAG_PNG} ({BED_B_SYNDIAG_PNG.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
