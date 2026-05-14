"""Stratified morphology gallery from the primary cohort.

Implements REQ-5. Adapted from the prototype `scratch_t0102_t0104_morph_compare.py`
with stratified sampling by (asym_class, source_task), per-stratum top-by-DSI*PD
ordering, and per-panel asym_score annotation. Outputs:

* results/images/morphology_gallery.png
* results/data/gallery_quota_table.json
"""

from __future__ import annotations

import contextlib
import json
import math
from dataclasses import dataclass
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
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.constants import (
    ALL_SOURCE_TASKS,
    CHART_DPI,
    CLASS_ASYMMETRIC,
    CLASS_SYMMETRIC,
    GALLERY_MAX_CELLS,
    MORPH_OFFSET,
    MORPHOLOGY_PARAM_NAMES,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.paths import (
    GALLERY_QUOTA_TABLE_PATH,
    MORPHOLOGY_GALLERY_PATH,
    RESULTS_DATA_DIR,
    RESULTS_IMAGES_DIR,
    SELECTED_CELLS_PRIMARY_PATH,
)

MAX_MORPH_SEED: int = 2**31 - 1


@dataclass(frozen=True, slots=True)
class GalleryPick:
    source_task: str
    seed: int | None
    generation: int
    dsi: float
    pd_rate_hz: float
    asym_score: float
    asym_class: str
    vector_68d: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class SectionPts:
    name: str
    xs: list[float]
    ys: list[float]
    diams: list[float]


def _load_primary() -> list[GalleryPick]:
    with open(SELECTED_CELLS_PRIMARY_PATH, encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
    cells_obj: Any = data["cells"]
    assert isinstance(cells_obj, list)
    picks: list[GalleryPick] = []
    for cell in cells_obj:
        assert isinstance(cell, dict)
        seed_val: Any = cell["seed"]
        seed_int: int | None = int(seed_val) if seed_val is not None else None
        picks.append(
            GalleryPick(
                source_task=str(cell["source_task"]),
                seed=seed_int,
                generation=int(cell["generation"]),
                dsi=float(cell["dsi"]),
                pd_rate_hz=float(cell["pd_rate_hz"]),
                asym_score=float(cell["asym_score"]),
                asym_class=str(cell["asym_class"]),
                vector_68d=tuple(float(v) for v in cell["vector_68d"]),
            )
        )
    return picks


def _stratify(*, picks: list[GalleryPick]) -> dict[tuple[str, str], list[GalleryPick]]:
    strata: dict[tuple[str, str], list[GalleryPick]] = {}
    for cls in (CLASS_SYMMETRIC, CLASS_ASYMMETRIC):
        for src in ALL_SOURCE_TASKS:
            strata[(cls, src)] = []
    for pick in picks:
        key: tuple[str, str] = (pick.asym_class, pick.source_task)
        strata[key].append(pick)
    return strata


def _select_quota(
    *,
    strata: dict[tuple[str, str], list[GalleryPick]],
    max_cells: int,
) -> tuple[list[GalleryPick], dict[str, int]]:
    nonempty: list[tuple[str, str]] = [k for k, v in strata.items() if len(v) > 0]
    nonempty_n: int = len(nonempty)
    if nonempty_n == 0:
        return [], {}
    per_stratum_quota: int = max(1, math.ceil(max_cells / nonempty_n))
    selected: list[GalleryPick] = []
    quota_used: dict[str, int] = {}
    for key in nonempty:
        bucket: list[GalleryPick] = strata[key]
        # Sort descending by DSI * PD-rate (data-driven, deterministic).
        bucket_sorted: list[GalleryPick] = sorted(bucket, key=lambda p: -(p.dsi * p.pd_rate_hz))
        take_n: int = min(per_stratum_quota, len(bucket_sorted))
        # Don't blow past max_cells.
        if len(selected) + take_n > max_cells:
            take_n = max_cells - len(selected)
        if take_n <= 0:
            break
        selected.extend(bucket_sorted[:take_n])
        quota_used[f"{key[0]}::{key[1]}"] = take_n
    return selected, quota_used


def _to_morph_params(*, vec: tuple[float, ...]) -> MorphologyParams:
    morph_slice: tuple[float, ...] = vec[MORPH_OFFSET:]
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


@dataclass(frozen=True, slots=True)
class BuiltMorph:
    soma: SectionPts
    dends: list[SectionPts]


def _build_and_extract(*, params: MorphologyParams) -> BuiltMorph:
    result: Any = generate_fixed_morphology(params=params)
    h: Any = result.h
    soma_pts: SectionPts = _extract_section_pts(h=h, sec=result.soma)
    dend_pts: list[SectionPts] = [_extract_section_pts(h=h, sec=s) for s in result.all_dends]
    for s in list(result.all_dends) + [result.soma]:
        with contextlib.suppress(RuntimeError, AttributeError):
            h.delete_section(sec=s)
    return BuiltMorph(soma=soma_pts, dends=dend_pts)


def _normalise_axes(*, axes: list[plt.Axes], built: list[BuiltMorph]) -> None:
    all_x: list[float] = []
    all_y: list[float] = []
    for bm in built:
        all_x.extend(bm.soma.xs)
        all_y.extend(bm.soma.ys)
        for sp in bm.dends:
            all_x.extend(sp.xs)
            all_y.extend(sp.ys)
    if len(all_x) == 0:
        return
    pad: float = 30.0
    xlo: float = min(all_x) - pad
    xhi: float = max(all_x) + pad
    ylo: float = min(all_y) - pad
    yhi: float = max(all_y) + pad
    side: float = max(xhi - xlo, yhi - ylo)
    cx: float = (xlo + xhi) / 2.0
    cy: float = (ylo + yhi) / 2.0
    for ax in axes:
        ax.set_xlim(cx - side / 2.0, cx + side / 2.0)
        ax.set_ylim(cy - side / 2.0, cy + side / 2.0)


def _plot_cell(
    *,
    ax: plt.Axes,
    built: BuiltMorph,
    pick: GalleryPick,
) -> None:
    for dp in built.dends:
        if len(dp.xs) < 2:
            continue
        avg_d: float = float(np.mean(dp.diams)) if len(dp.diams) > 0 else 1.0
        lw: float = max(0.3, min(2.0, avg_d * 2.0))
        ax.plot(dp.xs, dp.ys, color="#1f77b4", lw=lw, alpha=0.85, solid_capstyle="round")
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
        fontsize=8,
        color="#666666",
    )
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    seed_label: str = "n/a" if pick.seed is None else str(pick.seed)
    title: str = (
        f"{pick.source_task} seed={seed_label} gen={pick.generation}\n"
        f"DSI={pick.dsi:.3f}  PD={pick.pd_rate_hz:.1f} Hz\n"
        f"asym={pick.asym_score:.2f} ({pick.asym_class})"
    )
    ax.set_title(title, fontsize=8)


def main() -> None:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    picks_all: list[GalleryPick] = _load_primary()
    strata: dict[tuple[str, str], list[GalleryPick]] = _stratify(picks=picks_all)

    selected, quota_used = _select_quota(strata=strata, max_cells=GALLERY_MAX_CELLS)
    print(f"Selected {len(selected)} cells from {len(picks_all)} primary cells.")
    for stratum_key, qty in sorted(quota_used.items()):
        print(f"  {stratum_key}: {qty}")

    n_cells: int = len(selected)
    cols: int = 5
    rows: int = math.ceil(n_cells / cols) if n_cells > 0 else 1
    fig, axes_2d = plt.subplots(rows, cols, figsize=(cols * 3.0, rows * 3.4))
    if rows == 1 and cols == 1:
        axes_flat: list[plt.Axes] = [axes_2d]
    else:
        axes_flat = list(np.asarray(axes_2d).ravel())

    built_list: list[BuiltMorph] = []
    plot_axes: list[plt.Axes] = []
    for idx, pick in enumerate(selected):
        ax: plt.Axes = axes_flat[idx]
        print(
            f"  building cell {idx + 1}/{n_cells}: {pick.source_task} seed={pick.seed} "
            f"DSI={pick.dsi:.3f} PD={pick.pd_rate_hz:.1f} ..."
        )
        try:
            params: MorphologyParams = _to_morph_params(vec=pick.vector_68d)
            built: BuiltMorph = _build_and_extract(params=params)
            built_list.append(built)
            plot_axes.append(ax)
            _plot_cell(ax=ax, built=built, pick=pick)
        except (RuntimeError, ValueError, AssertionError) as exc:
            print(f"    FAILED ({type(exc).__name__}): {exc}")
            ax.text(
                0.5,
                0.5,
                f"build failed:\n{type(exc).__name__}",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=8,
            )
            ax.set_xticks([])
            ax.set_yticks([])

    for idx in range(n_cells, rows * cols):
        ax_blank: plt.Axes = axes_flat[idx]
        ax_blank.axis("off")

    if len(built_list) > 0:
        _normalise_axes(axes=plot_axes, built=built_list)

    fig.suptitle(
        "Primary cohort (DSI > 0.1 AND PD > 2.0): stratified gallery (by class x source)",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(MORPHOLOGY_GALLERY_PATH, dpi=CHART_DPI)
    plt.close(fig)

    with open(GALLERY_QUOTA_TABLE_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {
                "max_cells": GALLERY_MAX_CELLS,
                "n_selected": n_cells,
                "quota_used": quota_used,
                "n_nonempty_strata": sum(1 for v in strata.values() if len(v) > 0),
            },
            f,
            indent=2,
        )

    print()
    print(f"Wrote: {MORPHOLOGY_GALLERY_PATH}")
    print(f"Wrote: {GALLERY_QUOTA_TABLE_PATH}")


if __name__ == "__main__":
    main()
