"""Morphology rendering helpers copied from t0109 (build_cluster_gallery.py, lines 112-222).

Uses the canonical NEURON pt3d extraction path (`h.x3d / y3d / diam3d` over `result.all_dends`) to
render full dendrite trees (not just somas). The `h.delete_section(sec=s)` cleanup at the end of
`_build_and_extract` is mandatory to prevent NEURON RSS creep when many cells are built in one
process. The `morph_seed % (2**31 - 1)` coercion in `_to_morph_params` is also mandatory.

Only library imports (registered procedural_dsgc_morphology_generator and
procedural_dsgc_morphology_generator_fix) cross task boundaries; the helpers themselves are
re-implemented here to comply with the cross-task-import rule.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from typing import Any

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (
    generate_fixed_morphology,
)
from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.constants import (
    MAX_MORPH_SEED,
    MORPHOLOGY_PARAM_NAMES,
    N_ELECTROPHYS_DIMS,
)


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


@dataclass(frozen=True, slots=True)
class CellLabel:
    """Per-panel annotation values for the cluster-morph grid."""

    source_task: str
    seed: int
    generation: int
    dsi: float
    pd_rate_hz: float


def to_morph_params(*, vec: tuple[float, ...]) -> MorphologyParams:
    """Coerce the 14-d morphology slice into a valid MorphologyParams instance.

    The three int-typed fields need `int(round(...))` coercion and `morph_seed` must be
    `% (2**31 - 1)` (per t0109 line 130) before construction to avoid INT32 overflow.
    """
    assert len(vec) == N_ELECTROPHYS_DIMS + len(MORPHOLOGY_PARAM_NAMES) or len(vec) == len(
        MORPHOLOGY_PARAM_NAMES
    ), f"vec length {len(vec)} unexpected for morphology slice"
    morph_slice: tuple[float, ...] = (
        vec[N_ELECTROPHYS_DIMS:] if len(vec) > len(MORPHOLOGY_PARAM_NAMES) else vec
    )
    raw: dict[str, float | int] = dict(zip(MORPHOLOGY_PARAM_NAMES, morph_slice, strict=True))
    raw["num_primary_branches"] = int(round(float(raw["num_primary_branches"])))
    raw["max_strahler_depth"] = int(round(float(raw["max_strahler_depth"])))
    raw["morph_seed"] = int(float(raw["morph_seed"])) % MAX_MORPH_SEED
    return MorphologyParams.from_dict(data=raw)


def extract_section_pts(*, h: Any, sec: Any) -> SectionPts:
    """Pull (x, y, diam) pt3d arrays from a single NEURON section."""
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


def build_and_extract(*, params: MorphologyParams) -> BuiltMorph:
    """Build a single morphology, extract its pt3d arrays, and delete sections to free RAM."""
    result: Any = generate_fixed_morphology(params=params)
    h: Any = result.h
    soma_pts: SectionPts = extract_section_pts(h=h, sec=result.soma)
    dend_pts: list[SectionPts] = [extract_section_pts(h=h, sec=s) for s in result.all_dends]
    for s in list(result.all_dends) + [result.soma]:
        with contextlib.suppress(RuntimeError, AttributeError):
            h.delete_section(sec=s)
    return BuiltMorph(soma=soma_pts, dends=dend_pts)


def global_extents(built_list: list[BuiltMorph]) -> tuple[float, float, float, float]:
    """Return (xlo, xhi, ylo, yhi) square extent that covers all cells in the list."""
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


def plot_cell(*, ax: plt.Axes, built: BuiltMorph, label: CellLabel) -> None:
    """Render dendrites as line segments + soma as a circle + PD arrow + annotation label."""
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
    short_task: str = label.source_task[-5:]
    title: str = (
        f"{short_task}/s{label.seed}\n"
        f"gen={label.generation}\n"
        f"DSI={label.dsi:.3f}\n"
        f"PD={label.pd_rate_hz:.1f}Hz"
    )
    ax.set_title(title, fontsize=7)
