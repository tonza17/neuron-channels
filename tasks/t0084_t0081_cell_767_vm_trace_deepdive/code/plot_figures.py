"""Generate 4 figures per cell (12 total) from deep-dive simulation traces.

Figure 1: Per-direction Vm traces (3-row × 8-col grid).
Figure 2: NMDA conductance trajectories (8-line overlay).
Figure 3: Nav1.6 / NaP current decomposition (8-direction stacked subplots).
Figure 4: AIS spike onset histogram per direction (8-bin bar chart).

Saves PNGs to results/images/.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Patch
from numpy.typing import NDArray

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import AP_THRESHOLD_MV
from tasks.t0084_t0081_cell_767_vm_trace_deepdive.code.constants import CELL_IDS
from tasks.t0084_t0081_cell_767_vm_trace_deepdive.code.paths import (
    RESULTS_DATA_DIR,
    RESULTS_IMAGES_DIR,
    ensure_directories,
)

DIRECTIONS: tuple[int, ...] = (0, 45, 90, 135, 180, 225, 270, 315)
_CMAP: list[str] = [
    "#e6194b",
    "#3cb44b",
    "#4363d8",
    "#f58231",
    "#911eb4",
    "#42d4f4",
    "#f032e6",
    "#bfef45",
]


def _load_npz(cell_id: int, direction: int) -> dict[str, NDArray[np.float64]]:
    path: Path = RESULTS_DATA_DIR / f"cell{cell_id}_dir{direction}_traces.npz"
    assert path.exists(), f"Missing trace: {path}"
    return dict(np.load(path))


def _count_spikes(
    v_arr: NDArray[np.float64],
    threshold_mv: float,
) -> int:
    crossings: NDArray[np.bool_] = (v_arr[:-1] < threshold_mv) & (v_arr[1:] >= threshold_mv)
    return int(np.sum(crossings))


def _load_summary(cell_id: int) -> dict[str, object]:
    path: Path = RESULTS_DATA_DIR / f"cell{cell_id}_summary.json"
    return dict(json.loads(path.read_text(encoding="utf-8")))


def plot_fig1_vm_traces(*, cell_id: int) -> Path:
    """Figure 1: 3-row × 8-col grid of Vm traces."""
    fig, axes = plt.subplots(
        nrows=3,
        ncols=8,
        figsize=(24, 9),
        sharey="row",
        sharex=True,
    )
    row_labels: list[str] = ["Soma", "Mid dendrite", "Distal dendrite"]
    keys: list[str] = ["v_soma_mv", "v_mid_mv", "v_distal_mv"]

    for col, direction in enumerate(DIRECTIONS):
        data: dict[str, NDArray[np.float64]] = _load_npz(cell_id=cell_id, direction=direction)
        t: NDArray[np.float64] = data["t_ms"]
        for row, (key, label) in enumerate(zip(keys, row_labels, strict=True)):
            ax: Axes = axes[row, col]
            ax.plot(t, data[key], color=_CMAP[col], linewidth=0.8)
            if row == 0:
                ax.set_title(f"{direction}°", fontsize=9)
            if col == 0:
                ax.set_ylabel(f"{label}\nVm (mV)", fontsize=8)
            if row == 2:
                ax.set_xlabel("t (ms)", fontsize=8)
            ax.tick_params(labelsize=7)

    fig.suptitle(f"Cell {cell_id}: Per-direction Vm traces", fontsize=12, fontweight="bold")
    fig.tight_layout()
    out_path: Path = RESULTS_IMAGES_DIR / f"cell{cell_id}_fig1_vm_traces.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_fig2_nmda_conductance(*, cell_id: int) -> Path:
    """Figure 2: Total NMDA conductance per direction (8-line overlay)."""
    fig, ax = plt.subplots(figsize=(10, 5))

    for i, direction in enumerate(DIRECTIONS):
        data: dict[str, NDArray[np.float64]] = _load_npz(cell_id=cell_id, direction=direction)
        t: NDArray[np.float64] = data["t_ms"]
        g_total: NDArray[np.float64] = np.sum(data["g_nmda_us"], axis=0)
        ax.plot(t, g_total, color=_CMAP[i], label=f"{direction}°", linewidth=1.2)

    ax.set_xlabel("t (ms)", fontsize=11)
    ax.set_ylabel("Total NMDA g (uS)", fontsize=11)
    ax.set_title(f"Cell {cell_id}: NMDA conductance per direction", fontsize=12, fontweight="bold")
    ax.legend(fontsize=9, ncol=4, loc="upper right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out_path: Path = RESULTS_IMAGES_DIR / f"cell{cell_id}_fig2_nmda_conductance.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_fig3_nav16_nap_current(*, cell_id: int) -> Path:
    """Figure 3: Nav1.6 / NaP current decomposition, 8 subplots (4×2)."""
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(14, 16), sharey=False, sharex=True)

    for idx, direction in enumerate(DIRECTIONS):
        row, col = divmod(idx, 2)
        ax: Axes = axes[row, col]
        data: dict[str, NDArray[np.float64]] = _load_npz(cell_id=cell_id, direction=direction)
        t: NDArray[np.float64] = data["t_ms"]
        sec_area: float = float(data["sec_area_cm2"])

        i_nav16: NDArray[np.float64] = np.sum(data["i_nav16_ma_cm2"], axis=0) * sec_area * 1e6
        i_nap: NDArray[np.float64] = np.sum(data["i_nap_ma_cm2"], axis=0) * sec_area * 1e6

        ax.plot(t, i_nav16, color="#1f78b4", linewidth=1.0, label="Nav1.6")
        ax.plot(t, i_nap, color="#e31a1c", linewidth=1.0, label="NaP")
        ax.set_title(f"{direction}°", fontsize=10)
        ax.set_ylabel("Current (nA)", fontsize=8)
        ax.tick_params(labelsize=7)
        if idx == 0:
            ax.legend(fontsize=8, loc="upper right")

    axes[-1, 0].set_xlabel("t (ms)", fontsize=9)
    axes[-1, 1].set_xlabel("t (ms)", fontsize=9)

    fig.suptitle(
        f"Cell {cell_id}: Nav1.6 / NaP current at distal dendrite",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    out_path: Path = RESULTS_IMAGES_DIR / f"cell{cell_id}_fig3_nav16_nap_current.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_fig4_ais_spikes(*, cell_id: int) -> Path:
    """Figure 4: AIS spike counts per direction (8-bin bar chart)."""
    spike_counts: list[int] = []
    for direction in DIRECTIONS:
        data: dict[str, NDArray[np.float64]] = _load_npz(cell_id=cell_id, direction=direction)
        v_ais: NDArray[np.float64] = data["v_ais_mv"]
        n: int = _count_spikes(v_ais, AP_THRESHOLD_MV)
        spike_counts.append(n)

    colors: list[str] = []
    for d in DIRECTIONS:
        if d == 0:
            colors.append("#ff7f00")  # PD = orange
        elif d == 180:
            colors.append("#1f78b4")  # ND = blue
        else:
            colors.append("#b2b2b2")

    fig, ax = plt.subplots(figsize=(10, 5))
    x: list[int] = list(range(len(DIRECTIONS)))
    bars = ax.bar(x, spike_counts, color=colors, edgecolor="black", linewidth=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{d}°" for d in DIRECTIONS], fontsize=10)
    ax.set_ylabel("AIS spike count", fontsize=11)
    ax.set_xlabel("Stimulus direction", fontsize=11)
    ax.set_title(
        f"Cell {cell_id}: AIS spike counts per direction",
        fontsize=12,
        fontweight="bold",
    )
    # Annotate bars
    for bar, count in zip(bars, spike_counts, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_height() + 0.1,
            str(count),
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.legend(
        handles=[
            Patch(color="#ff7f00", label="PD (0°)"),
            Patch(color="#1f78b4", label="ND (180°)"),
        ],
        fontsize=10,
    )
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    out_path: Path = RESULTS_IMAGES_DIR / f"cell{cell_id}_fig4_ais_spikes.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    ensure_directories()
    for cell_id in CELL_IDS:
        print(f"Generating figures for cell {cell_id}...", flush=True)
        p1 = plot_fig1_vm_traces(cell_id=cell_id)
        print(f"  Fig 1: {p1.name}", flush=True)
        p2 = plot_fig2_nmda_conductance(cell_id=cell_id)
        print(f"  Fig 2: {p2.name}", flush=True)
        p3 = plot_fig3_nav16_nap_current(cell_id=cell_id)
        print(f"  Fig 3: {p3.name}", flush=True)
        p4 = plot_fig4_ais_spikes(cell_id=cell_id)
        print(f"  Fig 4: {p4.name}", flush=True)
    print("[DONE] 12 figures generated.", flush=True)


if __name__ == "__main__":
    main()
