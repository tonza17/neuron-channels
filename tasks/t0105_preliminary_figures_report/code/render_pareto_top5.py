"""Render the top-5 Pareto cells from t0102 (3-objective NSGA-II) as a 5x2 mini-grid.

Adapted from ``tasks/t0098_visualise_pareto_morphologies/code/build_charts.py`` with
two corrections per research_code.md and the t0105 plan:
1. Morphology slice is ``vector_68d[54:]`` (the t0100 correction applied to t0099).
2. Cells are filtered ``pd_rate_hz >= PD_RATE_MIN_HZ = 5.0`` before joint-rank
   ranking on (dsi_vector_sum, pd_rate_hz, robustness) so silenced cells with the
   degenerate dsi_vector_sum = 1.0 artifact are excluded.

The DLL-loader monkey-patch is preserved verbatim from t0098: ``ensure_t80_dll_loaded``
in both ``t0080`` and ``t0090`` is replaced with a no-op before importing
``generate_fixed_morphology``.

Polar tuning per cell is a two-point polar (PD at 0 deg, ND at 180 deg) because
per-angle tuning is not in t0102's data folder and re-running NEURON is out of scope.
PD radius is ``pd_rate_hz``; ND radius is ``pd_rate_hz * (1 - dsi_vector_sum)``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle
from matplotlib.projections.polar import PolarAxes
from pydantic import BaseModel, ConfigDict, TypeAdapter
from scipy.stats import rankdata  # type: ignore[import-untyped]

from tasks.t0105_preliminary_figures_report.code import constants as cst
from tasks.t0105_preliminary_figures_report.code import paths as pth

# --- Monkey-patch NEURON DLL loaders BEFORE importing generate_fixed_morphology. ---


def _noop_ensure_dll_loaded(*, h: Any) -> None:  # noqa: ARG001
    return None


from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code import (  # noqa: E402
    apply_params as _t80_apply_params,
)

_t80_apply_params.ensure_t80_dll_loaded = _noop_ensure_dll_loaded

from tasks.t0090_morphology_generator_diversity_test.code import (  # noqa: E402
    generator as _t90_generator,
)

_t90_generator.ensure_t80_dll_loaded = _noop_ensure_dll_loaded  # type: ignore[attr-defined]

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (  # noqa: E402
    MorphologyParams,
    MorphologyResult,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (  # noqa: E402
    generate_fixed_morphology,
)

# --- Pydantic schema for the t0102 Pareto JSON. ---


class ParetoCellRecord(BaseModel):
    """One Pareto cell from t0102's pareto_front_seedXX.json."""

    model_config = ConfigDict(extra="ignore")

    cell_id: int
    vector_68d: list[float]
    morphology_vector_14d: list[float]
    dsi_vector_sum: float
    pd_rate_hz: float
    robustness: float


class ParetoFrontFile(BaseModel):
    model_config = ConfigDict(extra="ignore")

    seed: int
    n_total: int
    cells: list[ParetoCellRecord]


_PARETO_FILE_ADAPTER: TypeAdapter[ParetoFrontFile] = TypeAdapter(ParetoFrontFile)


@dataclass(frozen=True, slots=True)
class CellRecord:
    cell_id: int
    seed: int
    dsi: float
    pd_rate_hz: float
    robustness: float
    morphology_vector_14d: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class CellGeometry:
    cell_id: int
    seed: int
    dsi: float
    pd_rate_hz: float
    robustness: float
    dendrite_segments: np.ndarray
    ais_segments: np.ndarray
    soma_xy: np.ndarray


def _color_for_seed(*, seed: int) -> str:
    return cst.SEED_COLORS.get(seed, cst.DEFAULT_SEED_COLOR)


def _params_from_14d(*, vec: tuple[float, ...]) -> MorphologyParams:
    assert len(vec) == 14, f"expected 14-d morphology vector, got len={len(vec)}"
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


def _load_all_cells() -> list[CellRecord]:
    """Load both seed44 and seed55 Pareto fronts, applying the vector_68d[54:] slice."""
    out: list[CellRecord] = []
    for json_path, expected_seed in (
        (pth.T0102_PARETO_SEED44_JSON, 44),
        (pth.T0102_PARETO_SEED55_JSON, 55),
    ):
        parsed: ParetoFrontFile = _PARETO_FILE_ADAPTER.validate_json(
            json_path.read_bytes(),
        )
        assert parsed.seed == expected_seed, (
            f"expected seed={expected_seed} in {json_path.name}, got {parsed.seed}"
        )
        for cell in parsed.cells:
            # t0100 fix: use vector_68d[54:] morphology slice, not [:14].
            morph_vec: tuple[float, ...] = tuple(float(v) for v in cell.vector_68d[54:])
            assert len(morph_vec) == 14, f"vector_68d[54:] has length {len(morph_vec)}, expected 14"
            out.append(
                CellRecord(
                    cell_id=cell.cell_id,
                    seed=parsed.seed,
                    dsi=cell.dsi_vector_sum,
                    pd_rate_hz=cell.pd_rate_hz,
                    robustness=cell.robustness,
                    morphology_vector_14d=morph_vec,
                )
            )
    return out


def _filter_and_rank(*, cells: list[CellRecord]) -> list[CellRecord]:
    filtered: list[CellRecord] = [c for c in cells if c.pd_rate_hz >= cst.PD_RATE_MIN_HZ]
    assert len(filtered) >= cst.TOP_K_PARETO_CELLS, (
        f"only {len(filtered)} cells survive pd_rate_hz>={cst.PD_RATE_MIN_HZ} filter;"
        f" need at least {cst.TOP_K_PARETO_CELLS}"
    )
    # Joint rank: all three objectives maximised. Higher is better, so we negate before
    # rankdata (which ranks ascending). Then sum the ranks; the lowest joint rank wins.
    dsi_array: np.ndarray = np.array([-c.dsi for c in filtered], dtype=np.float64)
    pd_array: np.ndarray = np.array([-c.pd_rate_hz for c in filtered], dtype=np.float64)
    rob_array: np.ndarray = np.array([-c.robustness for c in filtered], dtype=np.float64)
    dsi_ranks: np.ndarray = rankdata(a=dsi_array, method="average")
    pd_ranks: np.ndarray = rankdata(a=pd_array, method="average")
    rob_ranks: np.ndarray = rankdata(a=rob_array, method="average")
    joint: np.ndarray = dsi_ranks + pd_ranks + rob_ranks
    order: np.ndarray = np.argsort(a=joint)
    top: list[CellRecord] = [filtered[int(i)] for i in order[: cst.TOP_K_PARETO_CELLS]]
    return top


def _extract_segments(
    *, result: MorphologyResult, soma_section_name: str
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
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
        else np.zeros(shape=(0, 2, 2), dtype=np.float64)
    )
    ais_arr: np.ndarray = (
        np.array(ais_segments, dtype=np.float64)
        if len(ais_segments) > 0
        else np.zeros(shape=(0, 2, 2), dtype=np.float64)
    )
    soma_arr: np.ndarray = np.array(soma_xy, dtype=np.float64)
    return dend_arr, ais_arr, soma_arr


def _build_geometry(*, record: CellRecord) -> CellGeometry:
    params: MorphologyParams = _params_from_14d(vec=record.morphology_vector_14d)
    result: MorphologyResult = generate_fixed_morphology(
        params=params,
        morph_seed=int(params.morph_seed),
    )
    dend_arr, ais_arr, soma_arr = _extract_segments(
        result=result,
        soma_section_name=cst.SOMA_SECTION_NAME,
    )
    return CellGeometry(
        cell_id=record.cell_id,
        seed=record.seed,
        dsi=record.dsi,
        pd_rate_hz=record.pd_rate_hz,
        robustness=record.robustness,
        dendrite_segments=dend_arr,
        ais_segments=ais_arr,
        soma_xy=soma_arr,
    )


def _draw_morphology_panel(*, ax: Axes, geom: CellGeometry) -> None:
    color: str = _color_for_seed(seed=geom.seed)
    if geom.dendrite_segments.shape[0] > 0:
        lc = LineCollection(
            segments=geom.dendrite_segments.tolist(),
            colors=color,
            linewidths=cst.DENDRITE_LINEWIDTH,
            alpha=0.85,
        )
        ax.add_collection(lc)
    if geom.ais_segments.shape[0] > 0:
        lc_ais = LineCollection(
            segments=geom.ais_segments.tolist(),
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
    ax.add_patch(p=soma_circle)
    # Auto-zoom around all points.
    all_pts: list[np.ndarray] = []
    if geom.dendrite_segments.shape[0] > 0:
        all_pts.append(geom.dendrite_segments.reshape(-1, 2))
    if geom.ais_segments.shape[0] > 0:
        all_pts.append(geom.ais_segments.reshape(-1, 2))
    all_pts.append(geom.soma_xy.reshape(1, 2))
    pts: np.ndarray = np.concatenate(all_pts, axis=0)
    x_min, y_min = pts.min(axis=0)
    x_max, y_max = pts.max(axis=0)
    cx: float = float(0.5 * (x_min + x_max))
    cy: float = float(0.5 * (y_min + y_max))
    half_extent: float = float(max(x_max - x_min, y_max - y_min) * 0.55 + 10.0)
    ax.set_xlim(left=cx - half_extent, right=cx + half_extent)
    ax.set_ylim(bottom=cy - half_extent, top=cy + half_extent)
    ax.set_aspect(aspect="equal", adjustable="box")
    ax.set_xticks(ticks=[])
    ax.set_yticks(ticks=[])
    ax.set_title(
        label=(
            f"cell {geom.cell_id} (seed {geom.seed})\n"
            f"DSI={geom.dsi:.2f} PD={geom.pd_rate_hz:.1f}Hz "
            f"rob={geom.robustness:.2f}"
        ),
        fontsize=8,
    )


def _draw_polar_panel(*, ax_raw: Axes, geom: CellGeometry) -> None:
    ax: PolarAxes = cast(PolarAxes, ax_raw)
    ax.set_theta_direction(direction=1)
    ax.set_theta_offset(offset=0.0)
    pd_radius: float = float(geom.pd_rate_hz)
    nd_radius: float = float(geom.pd_rate_hz * max(0.0, 1.0 - geom.dsi))
    angles_rad: np.ndarray = np.array(
        [np.deg2rad(cst.PD_ANGLE_DEG), np.deg2rad(cst.ND_ANGLE_DEG)],
        dtype=np.float64,
    )
    radii: np.ndarray = np.array([pd_radius, nd_radius], dtype=np.float64)
    color: str = _color_for_seed(seed=geom.seed)
    ax.plot(
        angles_rad,
        radii,
        color=color,
        linewidth=1.5,
        marker="o",
        markersize=8,
    )
    ax.annotate(
        text="",
        xy=(angles_rad[0], pd_radius),
        xytext=(0.0, 0.0),
        xycoords="polar",
        arrowprops={"arrowstyle": "->", "color": "red", "lw": 1.5},
    )
    # Per-cell max radius for the radial grid.
    rmax: float = float(max(pd_radius, nd_radius, 1.0)) * 1.15
    ax.set_ylim(bottom=0.0, top=rmax)
    ax.set_title(
        label=(f"two-point polar\nPD={pd_radius:.1f}Hz, ND={nd_radius:.1f}Hz"),
        fontsize=8,
    )
    ax.tick_params(labelsize=6)


def _write_sidecar_json(*, top_cells: list[CellRecord]) -> None:
    pth.DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "spec_version": "1",
        "source_seeds": [44, 55],
        "filter_pd_rate_min_hz": cst.PD_RATE_MIN_HZ,
        "selection_rule": (
            "joint rank (ascending) on negated objectives (dsi_vector_sum, pd_rate_hz, robustness)"
        ),
        "cells": [
            {
                "cell_id": c.cell_id,
                "seed": c.seed,
                "dsi_vector_sum": c.dsi,
                "pd_rate_hz": c.pd_rate_hz,
                "robustness": c.robustness,
            }
            for c in top_cells
        ],
    }
    pth.FIG07_TOP5_CELLS_JSON.write_text(
        data=json.dumps(obj=payload, indent=2),
        encoding="utf-8",
    )


def render_pareto_top5() -> list[CellRecord]:
    pth.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    all_cells: list[CellRecord] = _load_all_cells()
    print(f"[t0105] loaded {len(all_cells)} Pareto cells across seeds 44 + 55")
    top: list[CellRecord] = _filter_and_rank(cells=all_cells)
    print(f"[t0105] top {len(top)} cells after pd_rate>={cst.PD_RATE_MIN_HZ}:")
    for c in top:
        print(
            f"  cell={c.cell_id} seed={c.seed} dsi={c.dsi:.3f} "
            f"pd={c.pd_rate_hz:.2f}Hz rob={c.robustness:.3f}"
        )
    _write_sidecar_json(top_cells=top)
    geometries: list[CellGeometry] = [_build_geometry(record=r) for r in top]
    fig = plt.figure(figsize=(15.0, 18.0), dpi=cst.DPI)
    for row_idx, geom in enumerate(geometries):
        # Two columns: morphology (cartesian) on left, polar on right.
        ax_morph = fig.add_subplot(
            len(geometries),
            2,
            row_idx * 2 + 1,
        )
        _draw_morphology_panel(ax=ax_morph, geom=geom)
        ax_polar = fig.add_subplot(
            len(geometries),
            2,
            row_idx * 2 + 2,
            projection="polar",
        )
        _draw_polar_panel(ax_raw=ax_polar, geom=geom)
    fig.suptitle(
        t=(
            "Top-5 Pareto cells from t0102 (3-obj NSGA-II, seeds 44+55, "
            f"pd_rate >= {cst.PD_RATE_MIN_HZ:.1f} Hz)"
        ),
        fontsize=13,
        fontweight="bold",
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.97))
    fig.savefig(
        fname=pth.FIG07_TOP5_PARETO_PNG,
        dpi=cst.DPI,
        facecolor=cst.FACECOLOR,
        bbox_inches=cst.BBOX_INCHES,
    )
    plt.close(fig=fig)
    return top


def main() -> list[CellRecord]:
    top: list[CellRecord] = render_pareto_top5()
    print(f"[t0105] wrote {pth.FIG07_TOP5_PARETO_PNG}")
    print(f"[t0105] wrote {pth.FIG07_TOP5_CELLS_JSON}")
    return top


if __name__ == "__main__":
    main()
