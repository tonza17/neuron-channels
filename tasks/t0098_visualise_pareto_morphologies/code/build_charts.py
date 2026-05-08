"""Build visualization charts for the 57 Pareto cells from t0091.

Reads ``tasks/t0091_morphology_extended_nsga2_v1/results/data/`` and writes 4
PNGs to ``tasks/t0098_visualise_pareto_morphologies/results/images/``.

Charts produced:
1. morphology_grid_57cells.png  - 8x8 grid of top-down dendritic trees
2. pareto_dsi_bar.png           - sorted bar chart of DSI per cell
3. pareto_pd_bar.png            - sorted bar chart of PD firing rate per cell
4. pareto_dsi_vs_pd_scatter.png - DSI vs PD scatter, joint-pass star

The script regenerates each cell's morphology by calling
``generate_fixed_morphology`` (canonical via correction C-0093-01) and reads
``section_endpoints_xy`` to plot 2D x-y line segments. No NEURON simulation.
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Patch

from tasks.t0098_visualise_pareto_morphologies.code import constants as cst
from tasks.t0098_visualise_pareto_morphologies.code import paths as pth

if str(pth.REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(pth.REPO_ROOT))


from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code import (  # noqa: E402
    apply_params as _t80_apply_params,
)


def _noop_ensure_dll_loaded(*, h: Any) -> None:  # noqa: ARG001
    return None


_t80_apply_params.ensure_t80_dll_loaded = _noop_ensure_dll_loaded  # type: ignore[assignment]

from tasks.t0090_morphology_generator_diversity_test.code import (  # noqa: E402
    generator as _t90_generator,
)

_t90_generator.ensure_t80_dll_loaded = _noop_ensure_dll_loaded  # type: ignore[assignment]

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (  # noqa: E402
    MorphologyParams,
    MorphologyResult,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (  # noqa: E402
    generate_fixed_morphology,
)


@dataclass(frozen=True, slots=True)
class CellRecord:
    cell_id: int
    anchor_name: str
    dsi: float
    pd_rate_hz: float
    robustness: float
    morphology_vector_14d: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class CellGeometry:
    cell_id: int
    anchor_name: str
    dsi: float
    pd_rate_hz: float
    robustness: float
    dendrite_segments: np.ndarray
    ais_segments: np.ndarray
    soma_xy: np.ndarray


def _color_for_anchor(*, anchor_name: str) -> str:
    return cst.ANCHOR_COLORS.get(anchor_name, cst.DEFAULT_COLOR)


def _params_from_14d(*, vec: tuple[float, ...]) -> MorphologyParams:
    assert len(vec) == 14, f"expected 14-d vector, got len={len(vec)}"
    return MorphologyParams(
        num_primary_branches=int(round(vec[0])),
        branch_prob_per_um=float(vec[1]),
        max_strahler_depth=int(round(vec[2])),
        mean_branching_angle_deg=float(vec[3]),
        rall_exponent=float(vec[4]),
        soma_offset_pd_um=float(vec[5]),
        field_elongation_pd=float(vec[6]),
        branch_density_gradient_pd=float(vec[7]),
        primary_branch_pd_concentration=float(vec[8]),
        mean_segment_length_um=float(vec[9]),
        soma_diameter_um=float(vec[10]),
        ais_length_um=float(vec[11]),
        morph_seed=int(round(vec[12])),
        branch_length_cv=float(vec[13]),
    )


def _load_records() -> list[CellRecord]:
    pareto_data: dict[str, Any] = json.loads(pth.PARETO_PATH.read_text(encoding="utf-8"))
    tracking_data: dict[str, Any] = json.loads(pth.ANCHOR_TRACKING_PATH.read_text(encoding="utf-8"))
    anchor_by_cell_id: dict[int, str] = {
        int(c["cell_id"]): str(c["nearest_anchor_name"]) for c in tracking_data["cells"]
    }
    records: list[CellRecord] = []
    for cell in pareto_data["cells"]:
        cell_id: int = int(cell["cell_id"])
        anchor_name: str = anchor_by_cell_id.get(cell_id, "unknown")
        records.append(
            CellRecord(
                cell_id=cell_id,
                anchor_name=anchor_name,
                dsi=float(cell["dsi_vector_sum"]),
                pd_rate_hz=float(cell["pd_rate_hz"]),
                robustness=float(cell["robustness"]),
                morphology_vector_14d=tuple(float(v) for v in cell["morphology_vector_14d"]),
            )
        )
    return records


def _extract_segments(
    *, result: MorphologyResult, soma_section_name: str
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (dendrite_segments, ais_segments, soma_xy).

    dendrite_segments shape (N, 2, 2): first axis = segment, second = endpoint,
    third = (x, y). ais_segments same shape. soma_xy shape (2,).
    """
    dend_segments: list[tuple[tuple[float, float], tuple[float, float]]] = []
    ais_segments: list[tuple[tuple[float, float], tuple[float, float]]] = []
    soma_xy: tuple[float, float] = (
        float(result.origin_xy[0]),
        float(result.origin_xy[1]),
    )
    for sec_name, (x0, y0, x1, y1) in result.section_endpoints_xy.items():
        endpoint = (
            (float(x0), float(y0)),
            (float(x1), float(y1)),
        )
        if sec_name == soma_section_name:
            continue
        if "ais" in sec_name.lower():
            ais_segments.append(endpoint)
        else:
            dend_segments.append(endpoint)
    dend_arr: np.ndarray = (
        np.array(dend_segments, dtype=np.float64)
        if len(dend_segments) > 0
        else np.zeros((0, 2, 2), dtype=np.float64)
    )
    ais_arr: np.ndarray = (
        np.array(ais_segments, dtype=np.float64)
        if len(ais_segments) > 0
        else np.zeros((0, 2, 2), dtype=np.float64)
    )
    soma_arr: np.ndarray = np.array(soma_xy, dtype=np.float64)
    return dend_arr, ais_arr, soma_arr


def _build_geometry(*, record: CellRecord) -> CellGeometry:
    params = _params_from_14d(vec=record.morphology_vector_14d)
    result = generate_fixed_morphology(
        params=params,
        morph_seed=int(params.morph_seed),
    )
    dend_arr, ais_arr, soma_arr = _extract_segments(
        result=result, soma_section_name=cst.SOMA_SECTION_NAME
    )
    return CellGeometry(
        cell_id=record.cell_id,
        anchor_name=record.anchor_name,
        dsi=record.dsi,
        pd_rate_hz=record.pd_rate_hz,
        robustness=record.robustness,
        dendrite_segments=dend_arr,
        ais_segments=ais_arr,
        soma_xy=soma_arr,
    )


def _plot_grid(*, geometries: list[CellGeometry]) -> Path:
    sorted_geoms: list[CellGeometry] = sorted(geometries, key=lambda g: g.dsi, reverse=True)
    fig, axes = plt.subplots(
        nrows=cst.GRID_ROWS,
        ncols=cst.GRID_COLS,
        figsize=cst.GRID_FIGSIZE_IN,
        dpi=cst.DPI,
    )
    axes_flat = axes.flatten()
    n_panels: int = cst.GRID_ROWS * cst.GRID_COLS
    for panel_idx in range(n_panels):
        ax = axes_flat[panel_idx]
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        if panel_idx >= len(sorted_geoms):
            ax.axis("off")
            continue
        geom = sorted_geoms[panel_idx]
        color = _color_for_anchor(anchor_name=geom.anchor_name)
        if geom.dendrite_segments.shape[0] > 0:
            lc = LineCollection(
                segments=geom.dendrite_segments,
                colors=color,
                linewidths=cst.DENDRITE_LINEWIDTH,
                alpha=0.85,
            )
            ax.add_collection(lc)
        if geom.ais_segments.shape[0] > 0:
            lc_ais = LineCollection(
                segments=geom.ais_segments,
                colors="black",
                linewidths=cst.AIS_LINEWIDTH,
                alpha=0.9,
            )
            ax.add_collection(lc_ais)
        soma_circle = Circle(
            xy=(float(geom.soma_xy[0]), float(geom.soma_xy[1])),
            radius=cst.SOMA_RADIUS_DRAW_UM,
            facecolor=color,
            edgecolor="black",
            linewidth=0.5,
            zorder=10,
        )
        ax.add_patch(soma_circle)
        all_pts: list[np.ndarray] = []
        if geom.dendrite_segments.shape[0] > 0:
            all_pts.append(geom.dendrite_segments.reshape(-1, 2))
        if geom.ais_segments.shape[0] > 0:
            all_pts.append(geom.ais_segments.reshape(-1, 2))
        all_pts.append(geom.soma_xy.reshape(1, 2))
        pts_combined: np.ndarray = np.concatenate(all_pts, axis=0)
        x_min, y_min = pts_combined.min(axis=0)
        x_max, y_max = pts_combined.max(axis=0)
        cx: float = float(0.5 * (x_min + x_max))
        cy: float = float(0.5 * (y_min + y_max))
        half_extent: float = float(max(x_max - x_min, y_max - y_min) * 0.55 + 10.0)
        ax.set_xlim(cx - half_extent, cx + half_extent)
        ax.set_ylim(cy - half_extent, cy + half_extent)
        title = f"{geom.anchor_name[:6]} DSI={geom.dsi:.2f} PD={geom.pd_rate_hz:.1f}Hz"
        ax.set_title(title, fontsize=cst.PANEL_TITLE_FONTSIZE)
    fig.suptitle(
        "t0091 Pareto front - 57 cells (sorted by DSI descending)",
        fontsize=cst.SUPTITLE_FONTSIZE,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.97))
    fig.savefig(pth.GRID_PATH, dpi=cst.DPI)
    plt.close(fig)
    return pth.GRID_PATH


def _add_anchor_legend(*, ax: Any, geometries: list[CellGeometry]) -> None:
    counts: dict[str, int] = {}
    for g in geometries:
        counts[g.anchor_name] = counts.get(g.anchor_name, 0) + 1
    handles: list[Any] = []
    labels: list[str] = []
    for anchor_name, color in cst.ANCHOR_COLORS.items():
        if counts.get(anchor_name, 0) == 0:
            continue
        handles.append(Patch(facecolor=color, edgecolor="black"))
        labels.append(f"{anchor_name} (n={counts[anchor_name]})")
    handles.append(
        plt.Line2D(
            xdata=[0],
            ydata=[0],
            color="black",
            linestyle="--",
            linewidth=1.0,
        )
    )
    labels.append("threshold")
    ax.legend(
        handles=handles,
        labels=labels,
        loc="upper right",
        fontsize=cst.LEGEND_FONTSIZE,
    )


def _plot_dsi_bar(*, geometries: list[CellGeometry]) -> Path:
    sorted_geoms: list[CellGeometry] = sorted(geometries, key=lambda g: g.dsi, reverse=True)
    n: int = len(sorted_geoms)
    xs: np.ndarray = np.arange(n)
    dsis: np.ndarray = np.array([g.dsi for g in sorted_geoms], dtype=np.float64)
    colors: list[str] = [_color_for_anchor(anchor_name=g.anchor_name) for g in sorted_geoms]
    fig, ax = plt.subplots(figsize=cst.BAR_FIGSIZE_IN, dpi=cst.DPI)
    ax.bar(x=xs, height=dsis, color=colors, edgecolor="black", linewidth=0.3)
    ax.axhline(
        y=cst.DSI_THRESHOLD,
        color="black",
        linestyle="--",
        linewidth=1.0,
    )
    ax.set_xlabel("Pareto cell rank (sorted by DSI)")
    ax.set_ylabel("DSI (vector sum)")
    ax.set_title("t0091 Pareto cells - DSI sorted (color = nearest anchor)")
    ax.set_xlim(-0.5, n - 0.5)
    _add_anchor_legend(ax=ax, geometries=geometries)
    fig.tight_layout()
    fig.savefig(pth.DSI_BAR_PATH, dpi=cst.DPI)
    plt.close(fig)
    return pth.DSI_BAR_PATH


def _plot_pd_bar(*, geometries: list[CellGeometry]) -> Path:
    sorted_geoms: list[CellGeometry] = sorted(geometries, key=lambda g: g.pd_rate_hz, reverse=True)
    n: int = len(sorted_geoms)
    xs: np.ndarray = np.arange(n)
    pds: np.ndarray = np.array([g.pd_rate_hz for g in sorted_geoms], dtype=np.float64)
    colors: list[str] = [_color_for_anchor(anchor_name=g.anchor_name) for g in sorted_geoms]
    fig, ax = plt.subplots(figsize=cst.BAR_FIGSIZE_IN, dpi=cst.DPI)
    ax.bar(x=xs, height=pds, color=colors, edgecolor="black", linewidth=0.3)
    ax.axhline(
        y=cst.PD_THRESHOLD_HZ,
        color="black",
        linestyle="--",
        linewidth=1.0,
    )
    ax.set_xlabel("Pareto cell rank (sorted by PD rate)")
    ax.set_ylabel("PD firing rate (Hz)")
    ax.set_title("t0091 Pareto cells - PD rate sorted (color = nearest anchor)")
    ax.set_xlim(-0.5, n - 0.5)
    _add_anchor_legend(ax=ax, geometries=geometries)
    fig.tight_layout()
    fig.savefig(pth.PD_BAR_PATH, dpi=cst.DPI)
    plt.close(fig)
    return pth.PD_BAR_PATH


def _plot_dsi_vs_pd_scatter(*, geometries: list[CellGeometry]) -> Path:
    fig, ax = plt.subplots(figsize=cst.SCATTER_FIGSIZE_IN, dpi=cst.DPI)
    for anchor_name, color in cst.ANCHOR_COLORS.items():
        subset = [g for g in geometries if g.anchor_name == anchor_name]
        if len(subset) == 0:
            continue
        ax.scatter(
            x=[g.dsi for g in subset],
            y=[g.pd_rate_hz for g in subset],
            c=color,
            s=42,
            edgecolors="black",
            linewidths=0.4,
            label=f"{anchor_name} (n={len(subset)})",
        )
    joint_pass: list[CellGeometry] = [
        g
        for g in geometries
        if g.dsi >= cst.DSI_THRESHOLD
        and g.pd_rate_hz >= cst.PD_THRESHOLD_HZ
        and g.robustness >= cst.ROBUSTNESS_THRESHOLD
    ]
    if len(joint_pass) > 0:
        ax.scatter(
            x=[g.dsi for g in joint_pass],
            y=[g.pd_rate_hz for g in joint_pass],
            marker="*",
            c="black",
            s=180,
            label=f"joint-pass (n={len(joint_pass)})",
        )
    ax.axvline(
        x=cst.DSI_THRESHOLD,
        color="black",
        linestyle="--",
        linewidth=0.7,
        alpha=0.5,
    )
    ax.axhline(
        y=cst.PD_THRESHOLD_HZ,
        color="black",
        linestyle="--",
        linewidth=0.7,
        alpha=0.5,
    )
    ax.set_xlabel("DSI (vector sum)")
    ax.set_ylabel("PD firing rate (Hz)")
    ax.set_title(
        f"t0091 Pareto cells - DSI vs PD (joint-pass: DSI>="
        f"{cst.DSI_THRESHOLD}, PD>={cst.PD_THRESHOLD_HZ}Hz, "
        f"rob>={cst.ROBUSTNESS_THRESHOLD})"
    )
    ax.legend(loc="best", fontsize=cst.LEGEND_FONTSIZE)
    fig.tight_layout()
    fig.savefig(pth.SCATTER_PATH, dpi=cst.DPI)
    plt.close(fig)
    return pth.SCATTER_PATH


def main() -> None:
    pth.OUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    t_start: float = time.perf_counter()
    print(f"[t0098] reading {pth.PARETO_PATH.name}")
    records: list[CellRecord] = _load_records()
    print(f"[t0098] loaded {len(records)} Pareto cells; generating morphologies...")
    geometries: list[CellGeometry] = []
    for i, record in enumerate(records):
        geom = _build_geometry(record=record)
        geometries.append(geom)
        if (i + 1) % 10 == 0 or (i + 1) == len(records):
            print(
                f"[t0098]   built {i + 1}/{len(records)} (t+{time.perf_counter() - t_start:.1f}s)"
            )
    print("[t0098] writing charts...")
    p_grid: Path = _plot_grid(geometries=geometries)
    p_dsi_bar: Path = _plot_dsi_bar(geometries=geometries)
    p_pd_bar: Path = _plot_pd_bar(geometries=geometries)
    p_scatter: Path = _plot_dsi_vs_pd_scatter(geometries=geometries)
    elapsed: float = time.perf_counter() - t_start
    print(f"[t0098] DONE in {elapsed:.2f} s")
    print(f"  - {p_grid}")
    print(f"  - {p_dsi_bar}")
    print(f"  - {p_pd_bar}")
    print(f"  - {p_scatter}")


if __name__ == "__main__":
    main()
