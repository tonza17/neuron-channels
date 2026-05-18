"""Build a morphology gallery with up to 10 examples per t0108 morphology cluster.

Sort cells within each cluster by descending DSI * PD-rate; take the top min(10, n_cluster);
build each morphology with the project generator; render a 4-row x 10-col PNG.

Usage:
    uv run python -m tasks.t0109_t0108_morph_cluster_gallery.code.build_cluster_gallery
"""

from __future__ import annotations

import contextlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (
    generate_fixed_morphology,
)

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0109_t0108_morph_cluster_gallery"
T0108_DATA: Path = (
    REPO_ROOT / "tasks" / "t0108_t0106_cluster_factor_dsi05_pd10" / "results" / "data"
)
FILTERED_CELLS_JSON: Path = T0108_DATA / "filtered_cells.json"
MORPHOLOGY_CLUSTERS_JSON: Path = T0108_DATA / "morphology_clusters.json"

OUTPUT_PNG: Path = TASK_ROOT / "results" / "images" / "morphology_gallery_by_cluster.png"
OUTPUT_PICKS_JSON: Path = TASK_ROOT / "results" / "data" / "gallery_picks.json"

N_ELECTROPHYS_DIMS: int = 54
N_PER_CLUSTER: int = 10
CHART_DPI: int = 150
MAX_MORPH_SEED: int = 2**31 - 1

MORPHOLOGY_PARAM_NAMES: tuple[str, ...] = (
    "num_primary_branches",
    "branch_prob_per_um",
    "max_strahler_depth",
    "mean_branching_angle_deg",
    "rall_exponent",
    "soma_offset_pd_um",
    "field_elongation_pd",
    "branch_density_gradient_pd",
    "primary_branch_pd_concentration",
    "mean_segment_length_um",
    "soma_diameter_um",
    "ais_length_um",
    "morph_seed",
    "branch_length_cv",
)


@dataclass(frozen=True, slots=True)
class CellRecord:
    cluster: int
    generation: int
    dsi: float
    pd_rate_hz: float
    vector_68d: tuple[float, ...]
    source_task: str


@dataclass(frozen=True, slots=True)
class SectionPts:
    name: str
    xs: list[float]
    ys: list[float]
    diams: list[float]


@dataclass(frozen=True, slots=True)
class BuiltMorph:
    soma: SectionPts
    dends: list[SectionPts]


def _load_cells() -> list[CellRecord]:
    cells_data = json.loads(FILTERED_CELLS_JSON.read_text(encoding="utf-8"))
    clusters_data = json.loads(MORPHOLOGY_CLUSTERS_JSON.read_text(encoding="utf-8"))
    cells = cells_data["cells"]
    labels: list[int] = clusters_data["cluster_labels"]
    assert len(cells) == len(labels), "cells and labels must align"
    records: list[CellRecord] = []
    for cell, label in zip(cells, labels, strict=True):
        records.append(
            CellRecord(
                cluster=int(label),
                generation=int(cell["generation"]),
                dsi=float(cell["dsi"]),
                pd_rate_hz=float(cell["pd_rate_hz"]),
                vector_68d=tuple(float(x) for x in cell["vector_68d"]),
                source_task=str(cell["source_task"]),
            )
        )
    return records


def _select_top_per_cluster(
    *, records: list[CellRecord], n_per_cluster: int
) -> dict[int, list[CellRecord]]:
    by_cluster: dict[int, list[CellRecord]] = {}
    for r in records:
        by_cluster.setdefault(r.cluster, []).append(r)
    picks: dict[int, list[CellRecord]] = {}
    for cid, lst in by_cluster.items():
        ranked = sorted(lst, key=lambda r: -(r.dsi * r.pd_rate_hz))
        picks[cid] = ranked[:n_per_cluster]
    return picks


def _to_morph_params(*, vec: tuple[float, ...]) -> MorphologyParams:
    morph_slice: tuple[float, ...] = vec[N_ELECTROPHYS_DIMS:]
    raw: dict[str, float | int] = dict(zip(MORPHOLOGY_PARAM_NAMES, morph_slice, strict=True))
    raw["num_primary_branches"] = int(round(float(raw["num_primary_branches"])))
    raw["max_strahler_depth"] = int(round(float(raw["max_strahler_depth"])))
    raw["morph_seed"] = int(float(raw["morph_seed"])) % MAX_MORPH_SEED
    return MorphologyParams.from_dict(data=raw)


def _extract_section_pts(*, h: Any, sec: Any) -> SectionPts:
    name: str = str(sec.name())
    sec.push()
    try:
        n: int = int(h.n3d())
        xs: list[float] = [float(h.x3d(i)) for i in range(n)]
        ys: list[float] = [float(h.y3d(i)) for i in range(n)]
        diams: list[float] = [float(h.diam3d(i)) for i in range(n)]
    finally:
        h.pop_section()
    return SectionPts(name=name, xs=xs, ys=ys, diams=diams)


def _build_and_extract(*, params: MorphologyParams) -> BuiltMorph:
    result: Any = generate_fixed_morphology(params=params)
    h: Any = result.h
    soma_pts: SectionPts = _extract_section_pts(h=h, sec=result.soma)
    dend_pts: list[SectionPts] = [_extract_section_pts(h=h, sec=s) for s in result.all_dends]
    for s in list(result.all_dends) + [result.soma]:
        with contextlib.suppress(RuntimeError, AttributeError):
            h.delete_section(sec=s)
    return BuiltMorph(soma=soma_pts, dends=dend_pts)


def _global_extents(built_list: list[BuiltMorph]) -> tuple[float, float, float, float]:
    all_x: list[float] = []
    all_y: list[float] = []
    for bm in built_list:
        all_x.extend(bm.soma.xs)
        all_y.extend(bm.soma.ys)
        for sp in bm.dends:
            all_x.extend(sp.xs)
            all_y.extend(sp.ys)
    pad: float = 30.0
    xlo: float = min(all_x) - pad
    xhi: float = max(all_x) + pad
    ylo: float = min(all_y) - pad
    yhi: float = max(all_y) + pad
    side: float = max(xhi - xlo, yhi - ylo)
    cx: float = (xlo + xhi) / 2.0
    cy: float = (ylo + yhi) / 2.0
    return cx - side / 2.0, cx + side / 2.0, cy - side / 2.0, cy + side / 2.0


def _plot_cell(*, ax: plt.Axes, built: BuiltMorph, record: CellRecord) -> None:
    for dp in built.dends:
        if len(dp.xs) < 2:
            continue
        avg_d: float = float(np.mean(dp.diams)) if len(dp.diams) > 0 else 1.0
        lw: float = max(0.3, min(2.0, avg_d * 2.0))
        ax.plot(
            dp.xs,
            dp.ys,
            color="#1f77b4",
            lw=lw,
            alpha=0.85,
            solid_capstyle="round",
        )
    soma_pts: SectionPts = built.soma
    if len(soma_pts.xs) > 0:
        cx: float = float(np.mean(soma_pts.xs))
        cy: float = float(np.mean(soma_pts.ys))
        soma_r: float = max(
            4.0,
            float(np.mean(soma_pts.diams)) / 2.0 if len(soma_pts.diams) > 0 else 5.0,
        )
        ax.add_patch(mpatches.Circle((cx, cy), soma_r, color="#d62728", zorder=10))
    ax.annotate(
        "",
        xy=(0.96, 0.07),
        xytext=(0.78, 0.07),
        xycoords="axes fraction",
        arrowprops={"arrowstyle": "->", "color": "#888888", "lw": 1.0},
    )
    ax.text(
        0.87,
        0.11,
        "PD",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=7,
        color="#666666",
    )
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    title: str = f"gen {record.generation}\nDSI {record.dsi:.3f}\nPD {record.pd_rate_hz:.1f} Hz"
    ax.set_title(title, fontsize=7)


def main() -> None:
    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PICKS_JSON.parent.mkdir(parents=True, exist_ok=True)

    records = _load_cells()
    cluster_sizes_full: dict[int, int] = {}
    for r in records:
        cluster_sizes_full[r.cluster] = cluster_sizes_full.get(r.cluster, 0) + 1
    print(f"Cluster sizes (all 150 cells): {dict(sorted(cluster_sizes_full.items()))}")

    picks_per_cluster: dict[int, list[CellRecord]] = _select_top_per_cluster(
        records=records, n_per_cluster=N_PER_CLUSTER
    )
    cluster_ids: list[int] = sorted(picks_per_cluster.keys())
    n_rows: int = len(cluster_ids)
    n_cols: int = N_PER_CLUSTER

    fig, axes_2d = plt.subplots(n_rows, n_cols, figsize=(n_cols * 2.6, n_rows * 2.8), dpi=CHART_DPI)

    # Build all morphologies first so we can normalise axes to a common extent.
    built_per_panel: dict[tuple[int, int], BuiltMorph | None] = {}
    all_built: list[BuiltMorph] = []
    for row_idx, cid in enumerate(cluster_ids):
        picks: list[CellRecord] = picks_per_cluster[cid]
        for col_idx in range(n_cols):
            if col_idx >= len(picks):
                built_per_panel[(row_idx, col_idx)] = None
                continue
            rec: CellRecord = picks[col_idx]
            print(
                f"  building cluster {cid} cell {col_idx + 1}/{len(picks)}: "
                f"gen={rec.generation} DSI={rec.dsi:.3f} PD={rec.pd_rate_hz:.1f} ..."
            )
            try:
                params = _to_morph_params(vec=rec.vector_68d)
                built = _build_and_extract(params=params)
                built_per_panel[(row_idx, col_idx)] = built
                all_built.append(built)
            except (RuntimeError, ValueError, AssertionError) as exc:
                print(f"    FAILED ({type(exc).__name__}): {exc}")
                built_per_panel[(row_idx, col_idx)] = None

    xlo: float = 0.0
    xhi: float = 1.0
    ylo: float = 0.0
    yhi: float = 1.0
    if len(all_built) > 0:
        xlo, xhi, ylo, yhi = _global_extents(all_built)

    for row_idx, cid in enumerate(cluster_ids):
        picks = picks_per_cluster[cid]
        for col_idx in range(n_cols):
            ax: plt.Axes = axes_2d[row_idx, col_idx] if n_rows > 1 else axes_2d[col_idx]
            built = built_per_panel[(row_idx, col_idx)]
            if built is None:
                if col_idx < len(picks):
                    ax.text(
                        0.5,
                        0.5,
                        "build\nfailed",
                        ha="center",
                        va="center",
                        transform=ax.transAxes,
                        fontsize=8,
                    )
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_aspect("equal")
                continue
            rec = picks[col_idx]
            _plot_cell(ax=ax, built=built, record=rec)
            ax.set_xlim(xlo, xhi)
            ax.set_ylim(ylo, yhi)
        # Row label on the leftmost panel.
        left_ax: plt.Axes = axes_2d[row_idx, 0] if n_rows > 1 else axes_2d[0]
        row_label: str = (
            f"Cluster {cid}\n(n={cluster_sizes_full.get(cid, 0)} total, {len(picks)} shown)"
        )
        left_ax.set_ylabel(row_label, fontsize=10, rotation=90, labelpad=14)

    fig.suptitle(
        "t0108 morphology K-means clusters (k=4): top examples by DSI*PD",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(OUTPUT_PNG, dpi=CHART_DPI)
    plt.close(fig)
    print(f"\nWrote: {OUTPUT_PNG}")

    picks_payload: dict[str, object] = {
        "n_per_cluster_requested": N_PER_CLUSTER,
        "cluster_sizes_total": cluster_sizes_full,
        "picks": {
            str(cid): [
                {
                    "cluster": rec.cluster,
                    "generation": rec.generation,
                    "dsi": rec.dsi,
                    "pd_rate_hz": rec.pd_rate_hz,
                    "source_task": rec.source_task,
                }
                for rec in picks_per_cluster[cid]
            ]
            for cid in cluster_ids
        },
    }
    OUTPUT_PICKS_JSON.write_text(json.dumps(picks_payload, indent=2), encoding="utf-8")
    print(f"Wrote: {OUTPUT_PICKS_JSON}")


if __name__ == "__main__":
    main()
