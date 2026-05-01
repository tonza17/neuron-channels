"""Pure matplotlib helpers shared by the two schematic plotting scripts.

These helpers are illustrative: they do not call NEURON, they take all arguments by
keyword, and they return numpy arrays or draw onto a passed-in `Axes`. The traces
produced by `single_exponential_trace` and `bi_exponential_trace` are normalised so
that their peak amplitude matches the `peak` argument exactly; this is the standard
NEURON `Exp2Syn` normalisation convention (see Exp2NMDA.mod L80-82 for the same
factor in the upstream code).
"""

import math
from dataclasses import dataclass

import matplotlib.patches as mpatches
import numpy as np
from matplotlib.axes import Axes


@dataclass(frozen=True, slots=True)
class SynapsePlacement:
    """A single synapse marker location for a dendritic-tree schematic."""

    x_um: float
    y_um: float
    color: str
    marker: str = "o"
    size: float = 14.0


def time_axis(*, duration_ms: float, dt_ms: float) -> np.ndarray:
    """Return a 1-D time axis in milliseconds covering [0, duration_ms]."""
    n_steps: int = int(round(duration_ms / dt_ms)) + 1
    return np.linspace(start=0.0, stop=duration_ms, num=n_steps)


def single_exponential_trace(
    *,
    t_ms: np.ndarray,
    t0_ms: float,
    tau_ms: float,
    peak: float,
) -> np.ndarray:
    """Instantaneous-rise / single-exponential-decay trace.

    Models the simplified NEURON `SAC2RGCinhib`-style conductance: at `t = t0_ms` the
    conductance jumps to `peak` and decays as `peak * exp(-(t - t0_ms) / tau_ms)`
    thereafter. Pre-onset values are zero.
    """
    assert tau_ms > 0.0, "tau_ms is positive"
    assert peak >= 0.0, "peak is non-negative"
    g: np.ndarray = np.zeros_like(t_ms)
    mask: np.ndarray = t_ms >= t0_ms
    g[mask] = peak * np.exp(-(t_ms[mask] - t0_ms) / tau_ms)
    return g


def bi_exponential_trace(
    *,
    t_ms: np.ndarray,
    t0_ms: float,
    tau_rise_ms: float,
    tau_decay_ms: float,
    peak: float,
) -> np.ndarray:
    """Difference-of-exponentials trace normalised to `peak` at its maximum.

    Mirrors the NEURON `Exp2Syn` / `Exp2NMDA` factor normalisation
    (Exp2NMDA.mod L80-82): after onset, `g(t) = peak * (exp(-(t-t0)/tau_decay) -
    exp(-(t-t0)/tau_rise)) / factor` where `factor` is chosen so the maximum equals
    `peak`. Requires `tau_decay_ms > tau_rise_ms` to be physically meaningful.
    """
    assert tau_decay_ms > tau_rise_ms > 0.0, "tau_decay > tau_rise > 0"
    assert peak >= 0.0, "peak is non-negative"

    # Time of the peak of the difference-of-exponentials, derived analytically.
    tp: float = (tau_rise_ms * tau_decay_ms / (tau_decay_ms - tau_rise_ms)) * math.log(
        tau_decay_ms / tau_rise_ms
    )
    factor: float = math.exp(-tp / tau_decay_ms) - math.exp(-tp / tau_rise_ms)

    g: np.ndarray = np.zeros_like(t_ms)
    mask: np.ndarray = t_ms >= t0_ms
    dt: np.ndarray = t_ms[mask] - t0_ms
    g[mask] = peak * (np.exp(-dt / tau_decay_ms) - np.exp(-dt / tau_rise_ms)) / factor
    return g


def draw_dendritic_tree(
    *,
    ax: Axes,
    n_branches: int,
    branch_color: str,
    soma_color: str,
    branch_length_um: float,
    soma_radius_um: float,
    synapses: list[SynapsePlacement] | None,
    branch_alpha: float = 0.6,
    branch_lw: float = 0.6,
    angle_start_deg: float = 0.0,
    angle_end_deg: float = 360.0,
) -> None:
    """Draw an axial-schematic dendritic tree with `n_branches` lines.

    The soma is a filled circle at the origin; each dendrite is a straight line of
    length `branch_length_um` radiating outward at evenly spaced angles in the arc
    `[angle_start_deg, angle_end_deg]`. Synapse markers are scattered at the
    coordinates supplied in `synapses` (list-of-`SynapsePlacement`, may be `None`).

    This is an illustrative diagram — it does not preserve the 3D coordinates of
    `RGCmodel.hoc`'s `shape3d_*` procs (L212-11722), and the writeup figure caption
    must say so explicitly.
    """
    assert n_branches >= 0, "n_branches is non-negative"
    assert branch_length_um > 0.0, "branch_length_um is positive"
    assert soma_radius_um > 0.0, "soma_radius_um is positive"
    assert angle_end_deg > angle_start_deg, "angle window is positive"

    soma = mpatches.Circle(
        xy=(0.0, 0.0),
        radius=soma_radius_um,
        facecolor=soma_color,
        edgecolor="black",
        linewidth=0.8,
        zorder=3,
    )
    ax.add_patch(p=soma)

    if n_branches > 0:
        angles_deg: np.ndarray = np.linspace(
            start=angle_start_deg,
            stop=angle_end_deg,
            num=n_branches,
            endpoint=False,
        )
        angles_rad: np.ndarray = np.deg2rad(angles_deg)
        x_outer: np.ndarray = (soma_radius_um + branch_length_um) * np.cos(angles_rad)
        y_outer: np.ndarray = (soma_radius_um + branch_length_um) * np.sin(angles_rad)
        x_inner: np.ndarray = soma_radius_um * np.cos(angles_rad)
        y_inner: np.ndarray = soma_radius_um * np.sin(angles_rad)
        for i in range(n_branches):
            ax.plot(
                [x_inner[i], x_outer[i]],
                [y_inner[i], y_outer[i]],
                color=branch_color,
                alpha=branch_alpha,
                linewidth=branch_lw,
                zorder=1,
            )

    if synapses is not None:
        for syn in synapses:
            ax.scatter(
                x=syn.x_um,
                y=syn.y_um,
                c=syn.color,
                marker=syn.marker,
                s=syn.size,
                edgecolors="black",
                linewidths=0.4,
                zorder=4,
            )
