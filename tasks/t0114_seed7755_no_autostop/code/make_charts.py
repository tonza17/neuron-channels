"""Generate the four t0102 results charts.

Reads the per-cell predictions JSONL files and the per-seed HV trajectory JSON
files, then writes four PNG charts under ``results/images/``:

1. ``dsi_vs_pd_scatter.png`` — scatter of DSI vs PD-rate for all 2592 cells,
   colored by seed, with the strict joint-pass corner (DSI >= 0.5, PD >= 30 Hz)
   highlighted as a rectangle and the t0091 anchor cell marked for reference.
2. ``hv_trajectory.png`` — hypervolume vs generation for both seeds.
3. ``dsi_pd_density.png`` — 2D hexbin density of DSI vs PD-rate showing the
   bimodal anti-correlation pattern.
4. ``per_gen_best_dsi_pd.png`` — best DSI and best PD-rate per generation for
   each seed with two y-axes.

Run with ``uv run python -m tasks.t0114_seed7755_no_autostop.code.make_charts``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from tasks.t0114_seed7755_no_autostop.code.paths import (
    IMAGES_DIR,
    RESULTS_DATA_DIR,
    TASK_ROOT,
)

JOINT_PASS_DSI_MIN: float = 0.5
JOINT_PASS_PD_RATE_HZ_MIN: float = 30.0
JOINT_PASS_ROBUSTNESS_MIN: float = 0.7

# t0091's reported single joint-pass cell from anchor warm-start (for reference).
T0091_REFERENCE_CELL: dict[str, float] = {
    "dsi": 0.511,
    "pd_rate_hz": 35.1,
    "robustness": 0.79,
}

SEED_COLORS: dict[int, str] = {44: "#1f77b4", 55: "#d62728"}


@dataclass(frozen=True, slots=True)
class CellRecord:
    generation: int
    dsi: float
    pd_rate_hz: float
    robustness: float
    joint_pass: bool


@dataclass(frozen=True, slots=True)
class SeedHistory:
    seed: int
    cells: list[CellRecord]
    hv_generations: list[int]
    hv_values: list[float]


def _read_jsonl_cells(*, path: Path) -> list[CellRecord]:
    cells: list[CellRecord] = []
    with path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if line == "":
                continue
            entry = json.loads(line)
            cells.append(
                CellRecord(
                    generation=int(entry["generation"]),
                    dsi=float(entry["dsi_vector_sum"]),
                    pd_rate_hz=float(entry["pd_rate_hz"]),
                    robustness=float(entry["robustness"]),
                    joint_pass=bool(entry["joint_pass"]),
                )
            )
    return cells


def _read_hv_trajectory(*, path: Path) -> tuple[list[int], list[float]]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    trajectory = data["trajectory"]
    assert isinstance(trajectory, list)
    gens: list[int] = []
    hvs: list[float] = []
    for entry in trajectory:
        gens.append(int(entry["generation"]))
        hvs.append(float(entry["hypervolume"]))
    return gens, hvs


def _load_seed_history(*, seed: int) -> SeedHistory:
    jsonl_path = (
        TASK_ROOT
        / "assets"
        / "predictions"
        / f"nsga2-seed{seed}-bedb-morph-n4-gen20"
        / "files"
        / f"predictions-seed{seed}.jsonl"
    )
    cells = _read_jsonl_cells(path=jsonl_path)
    hv_path = RESULTS_DATA_DIR / f"hv_trajectory_seed{seed}.json"
    gens, hvs = _read_hv_trajectory(path=hv_path)
    return SeedHistory(seed=seed, cells=cells, hv_generations=gens, hv_values=hvs)


def _plot_dsi_vs_pd_scatter(*, histories: list[SeedHistory], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 6))
    for hist in histories:
        dsi = [c.dsi for c in hist.cells]
        pd = [c.pd_rate_hz for c in hist.cells]
        ax.scatter(
            pd,
            dsi,
            c=SEED_COLORS[hist.seed],
            alpha=0.45,
            s=12,
            label=f"seed {hist.seed} (n={len(hist.cells)})",
            edgecolors="none",
        )
    # Highlight the strict joint-pass corner.
    ax.axvspan(JOINT_PASS_PD_RATE_HZ_MIN, ax.get_xlim()[1] + 100, alpha=0.0)
    rect_x = JOINT_PASS_PD_RATE_HZ_MIN
    rect_y = JOINT_PASS_DSI_MIN
    ax.fill_between(
        x=[rect_x, 100],
        y1=rect_y,
        y2=1.0,
        color="#2ca02c",
        alpha=0.18,
        label=f"strict joint-pass\n(DSI>={rect_y}, PD>={rect_x} Hz)",
    )
    # t0091 reference anchor-warm-start cell.
    ax.scatter(
        [T0091_REFERENCE_CELL["pd_rate_hz"]],
        [T0091_REFERENCE_CELL["dsi"]],
        marker="*",
        s=280,
        c="#ffbf00",
        edgecolors="black",
        linewidths=1.0,
        label="t0091 anchor-driven cell (DSI=0.511, PD=35.1 Hz)",
        zorder=5,
    )
    ax.set_xlim(left=-2.0, right=72.0)
    ax.set_ylim(bottom=-0.05, top=1.05)
    ax.set_xlabel("Preferred-direction firing rate (Hz)")
    ax.set_ylabel("DSI (vector-sum)")
    ax.set_title(
        "t0102: DSI vs PD-rate across 2,592 cells (both random-init seeds)\n"
        "Strict joint-pass corner empty; t0091 anchor cell shown for reference"
    )
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.92)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


def _plot_hv_trajectory(*, histories: list[SeedHistory], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    for hist in histories:
        ax.plot(
            hist.hv_generations,
            hist.hv_values,
            marker="o",
            linewidth=2.0,
            markersize=6,
            color=SEED_COLORS[hist.seed],
            label=(
                f"seed {hist.seed}: final HV = {hist.hv_values[-1]:.2f} "
                f"@ gen {hist.hv_generations[-1]}"
            ),
        )
    ax.set_xlabel("NSGA-II generation")
    ax.set_ylabel("Hypervolume (maximised)")
    ax.set_title(
        "t0102: Hypervolume trajectory per GA seed\n"
        "Both seeds terminated by per-seed $4 cost watchdog before gen 20"
    )
    ax.grid(alpha=0.25)
    ax.set_xticks(range(1, 16))
    ax.legend(loc="lower right", framealpha=0.92)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


def _plot_dsi_pd_density(*, histories: list[SeedHistory], out_path: Path) -> None:
    all_dsi: list[float] = []
    all_pd: list[float] = []
    for hist in histories:
        for cell in hist.cells:
            all_dsi.append(cell.dsi)
            all_pd.append(cell.pd_rate_hz)
    dsi_arr = np.array(all_dsi)
    pd_arr = np.array(all_pd)

    fig, ax = plt.subplots(figsize=(9, 6))
    hb = ax.hexbin(
        pd_arr,
        dsi_arr,
        gridsize=40,
        cmap="viridis",
        bins="log",
        mincnt=1,
    )
    rect_x = JOINT_PASS_PD_RATE_HZ_MIN
    rect_y = JOINT_PASS_DSI_MIN
    ax.fill_between(
        x=[rect_x, 100],
        y1=rect_y,
        y2=1.0,
        color="white",
        alpha=0.0,
    )
    ax.plot(
        [rect_x, 100, 100, rect_x, rect_x],
        [rect_y, rect_y, 1.0, 1.0, rect_y],
        color="red",
        linewidth=2.0,
        linestyle="--",
        label=f"joint-pass corner (DSI>={rect_y}, PD>={rect_x} Hz): 0 cells",
    )
    cbar = fig.colorbar(hb, ax=ax)
    cbar.set_label("log10(cell count) per hexbin")
    ax.set_xlim(left=-2.0, right=72.0)
    ax.set_ylim(bottom=-0.05, top=1.05)
    ax.set_xlabel("Preferred-direction firing rate (Hz)")
    ax.set_ylabel("DSI (vector-sum)")
    ax.set_title(
        "t0102: 2D density of DSI vs PD-rate (2,592 cells)\n"
        "Bimodal anti-correlation: high DSI only at low PD, high PD only at low DSI"
    )
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.92)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


def _plot_per_gen_best_dsi_pd(*, histories: list[SeedHistory], out_path: Path) -> None:
    fig, ax_left = plt.subplots(figsize=(9, 5.5))
    ax_right = ax_left.twinx()

    for hist in histories:
        # Group by generation.
        gen_to_dsi: dict[int, list[float]] = {}
        gen_to_pd: dict[int, list[float]] = {}
        for cell in hist.cells:
            gen_to_dsi.setdefault(cell.generation, []).append(cell.dsi)
            gen_to_pd.setdefault(cell.generation, []).append(cell.pd_rate_hz)
        gens_sorted: list[int] = sorted(gen_to_dsi.keys())
        best_dsi: list[float] = [max(gen_to_dsi[g]) for g in gens_sorted]
        best_pd: list[float] = [max(gen_to_pd[g]) for g in gens_sorted]
        color = SEED_COLORS[hist.seed]
        ax_left.plot(
            gens_sorted,
            best_dsi,
            marker="o",
            color=color,
            linewidth=2.0,
            label=f"seed {hist.seed} best DSI",
        )
        ax_right.plot(
            gens_sorted,
            best_pd,
            marker="s",
            color=color,
            linewidth=1.4,
            linestyle="--",
            alpha=0.75,
            label=f"seed {hist.seed} best PD",
        )

    ax_left.axhline(
        y=JOINT_PASS_DSI_MIN,
        color="green",
        linestyle=":",
        linewidth=1.0,
        alpha=0.7,
    )
    ax_right.axhline(
        y=JOINT_PASS_PD_RATE_HZ_MIN,
        color="green",
        linestyle=":",
        linewidth=1.0,
        alpha=0.7,
    )

    ax_left.set_xlabel("NSGA-II generation")
    ax_left.set_ylabel("Best DSI (vector-sum)", color="#333333")
    ax_right.set_ylabel("Best PD-rate (Hz)", color="#333333")
    ax_left.set_ylim(bottom=-0.05, top=1.1)
    ax_right.set_ylim(bottom=-2.0, top=80.0)
    ax_left.set_title(
        "t0102: Best DSI and best PD-rate per generation, both seeds\n"
        "Each axis is hit individually but never simultaneously in the same cell"
    )
    ax_left.grid(alpha=0.25)
    lines_l, labels_l = ax_left.get_legend_handles_labels()
    lines_r, labels_r = ax_right.get_legend_handles_labels()
    ax_left.legend(
        lines_l + lines_r,
        labels_l + labels_r,
        loc="center right",
        fontsize=9,
        framealpha=0.92,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    histories: list[SeedHistory] = [
        _load_seed_history(seed=44),
        _load_seed_history(seed=55),
    ]
    _plot_dsi_vs_pd_scatter(
        histories=histories,
        out_path=IMAGES_DIR / "dsi_vs_pd_scatter.png",
    )
    _plot_hv_trajectory(
        histories=histories,
        out_path=IMAGES_DIR / "hv_trajectory.png",
    )
    _plot_dsi_pd_density(
        histories=histories,
        out_path=IMAGES_DIR / "dsi_pd_density.png",
    )
    _plot_per_gen_best_dsi_pd(
        histories=histories,
        out_path=IMAGES_DIR / "per_gen_best_dsi_pd.png",
    )


if __name__ == "__main__":
    main()
