"""Generate the four t0104 analysis charts required by the reporting brief.

Produces in ``results/images/``:

1. ``pareto_front_combined.png`` — scatter of all 2,208 cells with the combined
   Pareto front highlighted, color-coded by seed, axes (DSI, PD-rate).
2. ``hv_trajectory.png`` — HV vs generation for both seeds on the same axes,
   with annotations for seed 55's gen-8 breakthrough and watchdog trip points.
3. ``dsi_distribution.png`` — histogram of DSI values across all 2,208 cells,
   with the silence-guard floor (DSI = 0.0) called out separately.
4. ``comparison_vs_t0102.png`` — side-by-side scatter of t0104's Pareto front
   and t0102's Pareto front in the (DSI, PD) plane.

Run with
``uv run python -m tasks.t0114_seed7755_no_autostop.code.build_analysis_charts``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from tasks.t0114_seed7755_no_autostop.code.paths import (
    IMAGES_DIR,
    REPO_ROOT,
    RESULTS_DATA_DIR,
)

JOINT_PASS_DSI_MIN: float = 0.5
JOINT_PASS_PD_RATE_HZ_MIN: float = 30.0

SEED_COLORS: dict[int, str] = {44: "#1f77b4", 55: "#d62728"}
T0102_COLOR: str = "#7f7f7f"

T0102_DATA_DIR: Path = REPO_ROOT / "tasks" / "t0102_seedscale_n4_gen20" / "results" / "data"


@dataclass(frozen=True, slots=True)
class CellPoint:
    dsi: float
    pd_rate_hz: float
    generation: int


@dataclass(frozen=True, slots=True)
class SeedData:
    seed: int
    cells: list[CellPoint]
    pareto_dsi: list[float]
    pareto_pd: list[float]
    hv_generations: list[int]
    hv_values: list[float]
    hv_costs: list[float]


def _read_json(*, path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _load_seed_data(*, seed: int) -> SeedData:
    evals_raw = _read_json(path=RESULTS_DATA_DIR / f"all_evaluations_seed{seed}.json")
    assert isinstance(evals_raw, dict)
    evaluations = evals_raw.get("evaluations")
    assert isinstance(evaluations, list)
    cells: list[CellPoint] = []
    for entry in evaluations:
        assert isinstance(entry, dict)
        cells.append(
            CellPoint(
                dsi=float(entry["dsi_vector_sum"]),
                pd_rate_hz=float(entry["pd_rate_hz"]),
                generation=int(entry["generation"]),
            )
        )

    pareto_raw = _read_json(path=RESULTS_DATA_DIR / f"pareto_front_seed{seed}.json")
    assert isinstance(pareto_raw, dict)
    pareto_cells = pareto_raw.get("cells")
    assert isinstance(pareto_cells, list)
    pareto_dsi: list[float] = []
    pareto_pd: list[float] = []
    for cell in pareto_cells:
        assert isinstance(cell, dict)
        pareto_dsi.append(float(cell["dsi_vector_sum"]))
        pareto_pd.append(float(cell["pd_rate_hz"]))

    hv_raw = _read_json(path=RESULTS_DATA_DIR / f"hv_trajectory_seed{seed}.json")
    assert isinstance(hv_raw, dict)
    traj = hv_raw.get("trajectory")
    assert isinstance(traj, list)
    hv_gens: list[int] = []
    hv_vals: list[float] = []
    hv_costs: list[float] = []
    for entry in traj:
        assert isinstance(entry, dict)
        hv_gens.append(int(entry["generation"]))
        hv_vals.append(float(entry["hypervolume"]))
        hv_costs.append(float(entry["cumulative_cost_usd"]))

    return SeedData(
        seed=seed,
        cells=cells,
        pareto_dsi=pareto_dsi,
        pareto_pd=pareto_pd,
        hv_generations=hv_gens,
        hv_values=hv_vals,
        hv_costs=hv_costs,
    )


def _combined_pareto(*, all_seeds: list[SeedData]) -> tuple[list[float], list[float]]:
    """Compute the 2-D Pareto front across the union of per-seed Pareto cells."""
    pts: list[tuple[float, float]] = []
    for sd in all_seeds:
        for dsi, pd_rate in zip(sd.pareto_dsi, sd.pareto_pd, strict=True):
            pts.append((dsi, pd_rate))
    # Both objectives are maximised; non-dominated set in (DSI, PD).
    pts_sorted = sorted(pts, key=lambda p: (-p[0], -p[1]))
    front: list[tuple[float, float]] = []
    max_pd_so_far: float = -np.inf
    for dsi, pd_rate in pts_sorted:
        # Going from highest DSI down — keep cells whose PD is the highest seen so far.
        if pd_rate > max_pd_so_far:
            front.append((dsi, pd_rate))
            max_pd_so_far = pd_rate
    front.sort(key=lambda p: p[0])
    return [p[0] for p in front], [p[1] for p in front]


def _plot_pareto_front_combined(*, seeds: list[SeedData], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 6.5), dpi=180)
    for sd in seeds:
        dsi_arr = np.array([c.dsi for c in sd.cells])
        pd_arr = np.array([c.pd_rate_hz for c in sd.cells])
        ax.scatter(
            dsi_arr,
            pd_arr,
            s=8,
            alpha=0.30,
            color=SEED_COLORS[sd.seed],
            label=f"seed {sd.seed} (n={len(sd.cells)})",
        )
    combined_dsi, combined_pd = _combined_pareto(all_seeds=seeds)
    ax.plot(
        combined_dsi,
        combined_pd,
        marker="o",
        linestyle="-",
        color="black",
        markersize=7,
        linewidth=1.5,
        label=f"Combined Pareto front (n={len(combined_dsi)})",
    )
    # Joint-pass corner overlay.
    ax.axvline(JOINT_PASS_DSI_MIN, color="green", linestyle="--", linewidth=1.0, alpha=0.6)
    ax.axhline(
        JOINT_PASS_PD_RATE_HZ_MIN,
        color="green",
        linestyle="--",
        linewidth=1.0,
        alpha=0.6,
    )
    ax.fill_betweenx(
        y=[JOINT_PASS_PD_RATE_HZ_MIN, 100],
        x1=JOINT_PASS_DSI_MIN,
        x2=1.05,
        color="green",
        alpha=0.07,
        label="Strict joint-pass corner",
    )
    ax.set_xlim(-0.02, 1.0)
    ax.set_ylim(-2.0, 85.0)
    ax.set_xlabel("DSI (vector-sum, guard-cleaned)")
    ax.set_ylabel("Preferred-direction firing rate (Hz)")
    ax.set_title(
        "t0104 NSGA-II — All 2,208 evaluated cells with combined Pareto front\n"
        "Strict joint-pass corner (green): DSI >= 0.5 AND PD >= 30 Hz — 0 cells inside"
    )
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _plot_hv_trajectory(*, seeds: list[SeedData], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=180)
    for sd in seeds:
        ax.plot(
            sd.hv_generations,
            sd.hv_values,
            marker="o",
            markersize=6,
            color=SEED_COLORS[sd.seed],
            label=f"seed {sd.seed} (last gen {sd.hv_generations[-1]}, "
            f"final HV {sd.hv_values[-1]:.2f})",
        )
    # Seed 55 gen-8 breakthrough annotation.
    for sd in seeds:
        if sd.seed == 55:
            try:
                idx_8 = sd.hv_generations.index(8)
                idx_7 = sd.hv_generations.index(7)
                ax.annotate(
                    f"Seed 55 gen-8 breakthrough\nHV {sd.hv_values[idx_7]:.2f} -> "
                    f"{sd.hv_values[idx_8]:.2f}\n"
                    "(discovered DSI~0.42 / PD~15 region)",
                    xy=(8, sd.hv_values[idx_8]),
                    xytext=(2.2, sd.hv_values[idx_8] - 1.0),
                    fontsize=9,
                    arrowprops={
                        "arrowstyle": "->",
                        "color": "black",
                        "lw": 0.7,
                    },
                )
            except ValueError:
                pass
    # Watchdog trip annotations.
    for sd in seeds:
        last_gen = sd.hv_generations[-1]
        last_cost = sd.hv_costs[-1]
        ax.annotate(
            f"watchdog trip\ncost ${last_cost:.2f}",
            xy=(last_gen, sd.hv_values[-1]),
            xytext=(last_gen - 1.5, sd.hv_values[-1] + 0.6),
            fontsize=8,
            color=SEED_COLORS[sd.seed],
            arrowprops={
                "arrowstyle": "->",
                "color": SEED_COLORS[sd.seed],
                "lw": 0.6,
            },
        )
    ax.set_xlabel("NSGA-II generation")
    ax.set_ylabel("Hypervolume (2-D, ref point (0,0))")
    ax.set_title(
        "t0104 NSGA-II — Hypervolume trajectory per seed (2-objective DSI + PD)\n"
        "Per-seed $4 cost watchdog truncated both runs before planned gen 20"
    )
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.3)
    ax.set_xlim(0.5, 13.5)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _plot_dsi_distribution(*, seeds: list[SeedData], out_path: Path) -> None:
    all_dsi: list[float] = []
    for sd in seeds:
        all_dsi.extend(c.dsi for c in sd.cells)
    all_arr = np.array(all_dsi)
    floor_mask = all_arr == 0.0
    nonzero = all_arr[~floor_mask]
    n_floor = int(np.sum(floor_mask))
    n_total = int(all_arr.size)

    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=180)
    # Histogram of non-zero DSI values.
    bins = np.linspace(0.0, 1.0, 41)
    ax.hist(
        nonzero,
        bins=bins,
        color="#1f77b4",
        edgecolor="black",
        linewidth=0.4,
        alpha=0.85,
        label=f"DSI > 0 cells (n={int(nonzero.size)})",
    )
    # Silence-guard floor as separate orange bar at x=0.
    bin_width = bins[1] - bins[0]
    ax.bar(
        [0.0],
        [n_floor],
        width=bin_width,
        color="#ff7f0e",
        edgecolor="black",
        linewidth=0.4,
        align="edge",
        label=(f"DSI = 0.0 silence-guard floor (n={n_floor}, {100 * n_floor / n_total:.1f}%)"),
    )
    ax.axvline(JOINT_PASS_DSI_MIN, color="green", linestyle="--", linewidth=1.2)
    ax.text(
        JOINT_PASS_DSI_MIN + 0.01,
        ax.get_ylim()[1] * 0.6,
        "joint-pass DSI threshold",
        color="green",
        fontsize=9,
    )
    ax.set_xlabel("DSI (vector-sum, guard-cleaned)")
    ax.set_ylabel("Number of cells")
    ax.set_title(
        "t0104 DSI distribution across all 2,208 evaluated cells\n"
        "(seeds 44 + 55 combined; silence guard at SILENCE_SPIKE_COUNT_THRESHOLD=10)"
    )
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _load_t0102_pareto(*, seed: int) -> tuple[list[float], list[float]]:
    pareto_raw = _read_json(path=T0102_DATA_DIR / f"pareto_front_seed{seed}.json")
    assert isinstance(pareto_raw, dict)
    cells = pareto_raw.get("cells")
    assert isinstance(cells, list)
    dsis: list[float] = []
    pds: list[float] = []
    for cell in cells:
        assert isinstance(cell, dict)
        dsis.append(float(cell["dsi_vector_sum"]))
        pds.append(float(cell["pd_rate_hz"]))
    return dsis, pds


def _plot_comparison_vs_t0102(*, seeds: list[SeedData], out_path: Path) -> None:
    # t0102 Pareto cells from both seeds (3-obj projected onto DSI/PD).
    t102_dsi: list[float] = []
    t102_pd: list[float] = []
    for s in (44, 55):
        d, p = _load_t0102_pareto(seed=s)
        t102_dsi.extend(d)
        t102_pd.extend(p)

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.5), dpi=180, sharey=True)

    # Left: t0102 (3-obj, no DSI guard).
    ax_l = axes[0]
    ax_l.scatter(
        t102_dsi,
        t102_pd,
        s=40,
        color=T0102_COLOR,
        edgecolor="black",
        alpha=0.85,
        label=f"t0102 Pareto cells (n={len(t102_dsi)})",
    )
    ax_l.set_title(
        "t0102 (3-obj NSGA-II, no DSI guard)\nSilence-corner DSI=1.0 artifact contaminates front"
    )
    ax_l.set_xlabel("DSI (vector-sum, RAW)")
    ax_l.set_ylabel("Preferred-direction firing rate (Hz)")

    # Right: t0104 (2-obj, DSI guard active).
    ax_r = axes[1]
    for sd in seeds:
        ax_r.scatter(
            sd.pareto_dsi,
            sd.pareto_pd,
            s=40,
            color=SEED_COLORS[sd.seed],
            edgecolor="black",
            alpha=0.85,
            label=f"t0104 seed {sd.seed} Pareto (n={len(sd.pareto_dsi)})",
        )
    combined_dsi, combined_pd = _combined_pareto(all_seeds=seeds)
    ax_r.plot(
        combined_dsi,
        combined_pd,
        marker="o",
        linestyle="-",
        color="black",
        markersize=5,
        linewidth=1.0,
        label=f"t0104 combined Pareto (n={len(combined_dsi)})",
    )
    ax_r.set_title(
        "t0104 (2-obj NSGA-II, DSI guard active)\nSilence-corner removed; max DSI cleanly 0.54"
    )
    ax_r.set_xlabel("DSI (vector-sum, guard-cleaned)")

    for ax in axes:
        ax.axvline(JOINT_PASS_DSI_MIN, color="green", linestyle="--", linewidth=1.0, alpha=0.6)
        ax.axhline(
            JOINT_PASS_PD_RATE_HZ_MIN,
            color="green",
            linestyle="--",
            linewidth=1.0,
            alpha=0.6,
        )
        ax.fill_betweenx(
            y=[JOINT_PASS_PD_RATE_HZ_MIN, 100],
            x1=JOINT_PASS_DSI_MIN,
            x2=1.05,
            color="green",
            alpha=0.07,
        )
        ax.set_xlim(-0.02, 1.05)
        ax.set_ylim(-2.0, 85.0)
        ax.grid(alpha=0.3)
        ax.legend(loc="upper right", fontsize=8)

    fig.suptitle(
        "Pareto front comparison: t0102 3-obj vs t0104 2-obj (DSI vs PD)",
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    seeds: list[SeedData] = [_load_seed_data(seed=44), _load_seed_data(seed=55)]

    _plot_pareto_front_combined(
        seeds=seeds,
        out_path=IMAGES_DIR / "pareto_front_combined.png",
    )
    print(f"[build_analysis_charts] wrote {IMAGES_DIR / 'pareto_front_combined.png'}")
    _plot_hv_trajectory(seeds=seeds, out_path=IMAGES_DIR / "hv_trajectory.png")
    print(f"[build_analysis_charts] wrote {IMAGES_DIR / 'hv_trajectory.png'}")
    _plot_dsi_distribution(seeds=seeds, out_path=IMAGES_DIR / "dsi_distribution.png")
    print(f"[build_analysis_charts] wrote {IMAGES_DIR / 'dsi_distribution.png'}")
    _plot_comparison_vs_t0102(
        seeds=seeds,
        out_path=IMAGES_DIR / "comparison_vs_t0102.png",
    )
    print(f"[build_analysis_charts] wrote {IMAGES_DIR / 'comparison_vs_t0102.png'}")
    print("[build_analysis_charts] DONE")


if __name__ == "__main__":
    main()
