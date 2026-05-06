"""Generate 4 figures per representative cell from deep-dive simulation traces.

Adapted from
``tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/plot_figures.py``:

* Subplot grid columns / bin counts: 8 -> 16.
* Trace file naming: cell{id}_dir{int_tenths}_traces.npz.

Figure 1: Per-direction Vm traces (3-row x 16-col grid).
Figure 2: NMDA conductance trajectories (16-line overlay).
Figure 3: Nav1.6 / NaP current decomposition (16-direction subplots in 4 x 4
grid).
Figure 4: AIS spike onset histogram per direction (16-bin polar bar chart).

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
from tasks.t0088_recluster_marginals_and_vm_motifs.code.constants import (
    ANGLES_16DIR_DEG,
    ND_DIRECTION_DEG,
    PD_DIRECTION_DEG,
)
from tasks.t0088_recluster_marginals_and_vm_motifs.code.paths import (
    REPRESENTATIVE_CELLS_JSON,
    RESULTS_DATA_DIR,
    RESULTS_IMAGES_DIR,
    ensure_directories,
)

_CMAP: list[str] = [
    "#e6194b",
    "#3cb44b",
    "#4363d8",
    "#f58231",
    "#911eb4",
    "#42d4f4",
    "#f032e6",
    "#bfef45",
    "#fabebe",
    "#469990",
    "#dcbeff",
    "#9A6324",
    "#fffac8",
    "#800000",
    "#aaffc3",
    "#808000",
]


def _trace_path(*, cell_id: int, direction_deg: float) -> Path:
    dir_int_tenths: int = int(round(direction_deg * 10))
    return RESULTS_DATA_DIR / f"cell{cell_id}_dir{dir_int_tenths}_traces.npz"


def _load_npz(*, cell_id: int, direction_deg: float) -> dict[str, NDArray[np.float64]]:
    path: Path = _trace_path(cell_id=cell_id, direction_deg=direction_deg)
    assert path.exists(), f"Missing trace: {path}"
    return dict(np.load(path))


def _count_spikes(
    v_arr: NDArray[np.float64],
    threshold_mv: float,
) -> int:
    crossings: NDArray[np.bool_] = (v_arr[:-1] < threshold_mv) & (v_arr[1:] >= threshold_mv)
    return int(np.sum(crossings))


def plot_fig1_vm_traces(*, cell_id: int) -> Path:
    """Figure 1: 3-row x 16-col grid of Vm traces."""
    n_dirs = len(ANGLES_16DIR_DEG)
    fig, axes = plt.subplots(
        nrows=3,
        ncols=n_dirs,
        figsize=(2.0 * n_dirs, 9),
        sharey="row",
        sharex=True,
    )
    row_labels: list[str] = ["Soma", "Mid dendrite", "Distal dendrite"]
    keys: list[str] = ["v_soma_mv", "v_mid_mv", "v_distal_mv"]

    for col, direction in enumerate(ANGLES_16DIR_DEG):
        data = _load_npz(cell_id=cell_id, direction_deg=direction)
        t: NDArray[np.float64] = data["t_ms"]
        for row, (key, label) in enumerate(zip(keys, row_labels, strict=True)):
            ax: Axes = axes[row, col]
            ax.plot(t, data[key], color=_CMAP[col], linewidth=0.7)
            if row == 0:
                ax.set_title(f"{direction:.1f}°", fontsize=8)
            if col == 0:
                ax.set_ylabel(f"{label}\nVm (mV)", fontsize=8)
            if row == 2:
                ax.set_xlabel("t (ms)", fontsize=7)
            ax.tick_params(labelsize=6)

    fig.suptitle(
        f"Cell {cell_id}: Per-direction Vm traces (16 dirs)",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    out_path: Path = RESULTS_IMAGES_DIR / f"vm_traces_{cell_id}.png"
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_fig2_nmda_conductance(*, cell_id: int) -> Path:
    """Figure 2: Total NMDA conductance per direction (16-line overlay)."""
    fig, ax = plt.subplots(figsize=(12, 6))

    for i, direction in enumerate(ANGLES_16DIR_DEG):
        data = _load_npz(cell_id=cell_id, direction_deg=direction)
        t: NDArray[np.float64] = data["t_ms"]
        g_total: NDArray[np.float64] = np.sum(data["g_nmda_us"], axis=0)
        ax.plot(t, g_total, color=_CMAP[i], label=f"{direction:.1f}°", linewidth=1.0)

    ax.set_xlabel("t (ms)", fontsize=11)
    ax.set_ylabel("Total NMDA g (uS)", fontsize=11)
    ax.set_title(
        f"Cell {cell_id}: NMDA conductance per direction (16 dirs)",
        fontsize=12,
        fontweight="bold",
    )
    ax.legend(fontsize=8, ncol=4, loc="upper right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out_path: Path = RESULTS_IMAGES_DIR / f"nmda_conductance_{cell_id}.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_fig3_nav16_nap_current(*, cell_id: int) -> Path:
    """Figure 3: Nav1.6 / NaP current decomposition, 16 subplots (4x4)."""
    fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(16, 14), sharey=False, sharex=True)

    for idx, direction in enumerate(ANGLES_16DIR_DEG):
        row, col = divmod(idx, 4)
        ax: Axes = axes[row, col]
        data = _load_npz(cell_id=cell_id, direction_deg=direction)
        t: NDArray[np.float64] = data["t_ms"]
        sec_area: float = float(data["sec_area_cm2"])
        i_nav16: NDArray[np.float64] = np.sum(data["i_nav16_ma_cm2"], axis=0) * sec_area * 1e6
        i_nap: NDArray[np.float64] = np.sum(data["i_nap_ma_cm2"], axis=0) * sec_area * 1e6
        ax.plot(t, i_nav16, color="#1f78b4", linewidth=0.9, label="Nav1.6")
        ax.plot(t, i_nap, color="#e31a1c", linewidth=0.9, label="NaP")
        ax.set_title(f"{direction:.1f}°", fontsize=9)
        ax.set_ylabel("nA", fontsize=7)
        ax.tick_params(labelsize=7)
        if idx == 0:
            ax.legend(fontsize=7, loc="upper right")

    for c in range(4):
        axes[-1, c].set_xlabel("t (ms)", fontsize=9)

    fig.suptitle(
        f"Cell {cell_id}: Nav1.6 / NaP current at distal dendrite (16 dirs)",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    out_path: Path = RESULTS_IMAGES_DIR / f"nav_decomp_{cell_id}.png"
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_fig4_ais_spikes(*, cell_id: int) -> Path:
    """Figure 4: AIS spike counts per direction (16-bin polar bar chart)."""
    spike_counts: list[int] = []
    for direction in ANGLES_16DIR_DEG:
        data = _load_npz(cell_id=cell_id, direction_deg=direction)
        v_ais: NDArray[np.float64] = data["v_ais_mv"]
        n: int = _count_spikes(v_ais, AP_THRESHOLD_MV)
        spike_counts.append(n)

    theta = np.deg2rad(np.array(ANGLES_16DIR_DEG, dtype=np.float64))
    width = np.deg2rad(22.5)
    colors: list[str] = []
    for d in ANGLES_16DIR_DEG:
        if abs(d - PD_DIRECTION_DEG) < 1e-6:
            colors.append("#ff7f00")  # PD = orange
        elif abs(d - ND_DIRECTION_DEG) < 1e-6:
            colors.append("#1f78b4")  # ND = blue
        else:
            colors.append("#b2b2b2")

    fig = plt.figure(figsize=(8, 8))
    ax: Axes = fig.add_subplot(111, projection="polar")
    bars = ax.bar(
        theta,
        spike_counts,
        width=width,
        color=colors,
        edgecolor="black",
        linewidth=0.7,
        align="center",
    )
    ax.set_theta_zero_location("E")
    ax.set_theta_direction(-1)
    ax.set_xticks(theta)
    ax.set_xticklabels([f"{d:.1f}°" for d in ANGLES_16DIR_DEG], fontsize=8)
    for bar, count, t_rad in zip(bars, spike_counts, theta, strict=True):
        ax.text(
            t_rad,
            bar.get_height() + 0.2,
            str(count),
            ha="center",
            va="bottom",
            fontsize=8,
        )
    ax.set_title(
        f"Cell {cell_id}: AIS spike counts per direction (polar)",
        fontsize=12,
        fontweight="bold",
        pad=20,
    )
    ax.legend(
        handles=[
            Patch(color="#ff7f00", label=f"PD ({PD_DIRECTION_DEG:.0f}°)"),
            Patch(color="#1f78b4", label=f"ND ({ND_DIRECTION_DEG:.0f}°)"),
        ],
        fontsize=10,
        loc="upper right",
    )
    fig.tight_layout()
    out_path: Path = RESULTS_IMAGES_DIR / f"ais_spike_onset_{cell_id}.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    ensure_directories()
    reps_payload = json.loads(REPRESENTATIVE_CELLS_JSON.read_text(encoding="utf-8"))
    for rep in reps_payload["representatives"]:
        cell_id = int(rep["representative_cell_id"])
        print(f"Generating figures for cell {cell_id}...", flush=True)
        p1 = plot_fig1_vm_traces(cell_id=cell_id)
        print(f"  Fig 1: {p1.name}", flush=True)
        p2 = plot_fig2_nmda_conductance(cell_id=cell_id)
        print(f"  Fig 2: {p2.name}", flush=True)
        p3 = plot_fig3_nav16_nap_current(cell_id=cell_id)
        print(f"  Fig 3: {p3.name}", flush=True)
        p4 = plot_fig4_ais_spikes(cell_id=cell_id)
        print(f"  Fig 4: {p4.name}", flush=True)
    print("[DONE] 4 figures per representative cell generated.", flush=True)


if __name__ == "__main__":
    main()
