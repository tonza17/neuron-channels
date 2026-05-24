"""Step 9: render the visual diagnostic gallery PNG (REQ-12).

Renders a 5x4 grid of 20 cells with:

* Soma as a `matplotlib.patches.Circle` with `radius = soma_diameter_um / 2` (not the fixed 6 px
  from t0115's renderer).
* Every dendrite section drawn as a thin blue line segment via `LineCollection(linewidths=0.8)`.
* **Primary stems** highlighted in `tab:red` with `linewidths=2.0` so the soma -> primary-stem
  connection is visually unambiguous.
* A thin debug line (linewidth 0.5, alpha 0.5) from `origin_xy` to each primary stem's `end_xy`
  to make any geometric gap immediately visible (always zero gap, by Check 1 above).
* Per-panel xy bounds: square centred on the cell's geometric centre with
  `half_width = max(x_max - x_min, y_max - y_min) * 0.6 + 15.0`.
* Per-panel title in 8 pt font listing cell_id, stratum_tag, the 4 asymmetry parameters, and the
  3 check booleans (color-coded green / red).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.collections import LineCollection  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402

from tasks.t0120_morph_generator_geometry_audit.code.constants import (  # noqa: E402
    CELL_ID_COL,
    CHECK1_PRIMARY_START_COL,
    CHECK2_PARENT_CHILD_COL,
    CHECK3_SYNAPSE_FRAME_COL,
    STRATUM_TAG_COL,
)
from tasks.t0120_morph_generator_geometry_audit.code.paths import (  # noqa: E402
    COORDINATE_CONSISTENCY_CHECKS_CSV,
    GEOMETRY_AUDIT_GALLERY_PNG,
    SECTION_ENDPOINTS_DUMP_JSON,
    ensure_directories,
)

GRID_ROWS: int = 5
GRID_COLS: int = 4

# Panel size in inches (t0115 used ~22/10 x 12/5 ≈ 2.2 x 2.4. We double-up to ~4 x 4.).
PANEL_INCH_W: float = 4.5
PANEL_INCH_H: float = 4.5

DPI: int = 150

PRIMARY_COLOR: str = "tab:red"
SECONDARY_COLOR: str = "tab:blue"
DEBUG_LINE_COLOR: str = "black"
SOMA_FACE_COLOR: str = "lightgray"

PASS_COLOR: str = "#1a7c1a"
FAIL_COLOR: str = "#c0392b"


@dataclass(frozen=True, slots=True)
class CellPanelData:
    cell_id: str
    stratum_tag: str
    origin_xy: tuple[float, float]
    soma_diameter_um: float
    primary_segments: np.ndarray  # shape (n_primary, 2, 2)
    non_primary_segments: np.ndarray  # shape (n_non_primary, 2, 2)
    soma_offset_pd_um: float
    field_elongation_pd: float
    branch_density_gradient_pd: float
    primary_branch_pd_concentration: float
    check1_pass: bool
    check2_pass: bool
    check3_pass: bool
    soma_frame_offset_um: float


def _segments_for_kind(
    *,
    sections: list[dict[str, Any]],
    section_kinds: set[str],
) -> np.ndarray:
    segs: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for sec in sections:
        if sec["section_kind"] not in section_kinds:
            continue
        start_raw: list[float] | None = sec["python_start_xy"]
        end_raw: list[float] | None = sec["python_end_xy"]
        if start_raw is None or end_raw is None:
            continue
        segs.append(
            (
                (float(start_raw[0]), float(start_raw[1])),
                (float(end_raw[0]), float(end_raw[1])),
            )
        )
    if len(segs) == 0:
        return np.zeros((0, 2, 2), dtype=np.float64)
    return np.array(segs, dtype=np.float64)


def _build_panel_data(
    *,
    cell: dict[str, Any],
    checks_row: pd.Series,
) -> CellPanelData:
    sections: list[dict[str, Any]] = cell["sections"]
    asym: dict[str, float] = cell["asymmetry_params"]
    return CellPanelData(
        cell_id=cell["cell_id"],
        stratum_tag=cell["stratum_tag"],
        origin_xy=(float(cell["origin_xy"][0]), float(cell["origin_xy"][1])),
        soma_diameter_um=float(asym["soma_diameter_um"]),
        primary_segments=_segments_for_kind(sections=sections, section_kinds={"primary"}),
        non_primary_segments=_segments_for_kind(
            sections=sections,
            section_kinds={"non_terminal", "terminal"},
        ),
        soma_offset_pd_um=float(asym["soma_offset_pd_um"]),
        field_elongation_pd=float(asym["field_elongation_pd"]),
        branch_density_gradient_pd=float(asym["branch_density_gradient_pd"]),
        primary_branch_pd_concentration=float(asym["primary_branch_pd_concentration"]),
        check1_pass=bool(checks_row[CHECK1_PRIMARY_START_COL]),
        check2_pass=bool(checks_row[CHECK2_PARENT_CHILD_COL]),
        check3_pass=bool(checks_row[CHECK3_SYNAPSE_FRAME_COL]),
        soma_frame_offset_um=float(cell["soma_frame_offset_um"]),
    )


def _pass_str(*, b: bool) -> str:
    return "PASS" if b else "FAIL"


def _render_panel(*, ax: Any, data: CellPanelData) -> None:
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_yticks([])

    if data.non_primary_segments.shape[0] > 0:
        ax.add_collection(
            LineCollection(
                segments=data.non_primary_segments,
                colors=SECONDARY_COLOR,
                linewidths=0.8,
                alpha=0.7,
            )
        )
    if data.primary_segments.shape[0] > 0:
        ax.add_collection(
            LineCollection(
                segments=data.primary_segments,
                colors=PRIMARY_COLOR,
                linewidths=2.0,
                alpha=0.95,
                zorder=8,
            )
        )
        # Debug line: origin_xy -> each primary stem's end_xy.
        for prim_seg in data.primary_segments:
            end_xy: tuple[float, float] = (
                float(prim_seg[1][0]),
                float(prim_seg[1][1]),
            )
            ax.plot(
                [data.origin_xy[0], end_xy[0]],
                [data.origin_xy[1], end_xy[1]],
                color=DEBUG_LINE_COLOR,
                linewidth=0.5,
                alpha=0.4,
                zorder=6,
            )

    # Soma circle scaled to soma_diameter_um.
    soma_radius: float = max(1.0, data.soma_diameter_um / 2.0)
    ax.add_patch(
        Circle(
            xy=data.origin_xy,
            radius=soma_radius,
            facecolor=SOMA_FACE_COLOR,
            edgecolor="black",
            linewidth=0.6,
            alpha=0.85,
            zorder=10,
        )
    )

    # Per-panel bounds.
    pts: list[np.ndarray] = []
    if data.primary_segments.shape[0] > 0:
        pts.append(data.primary_segments.reshape(-1, 2))
    if data.non_primary_segments.shape[0] > 0:
        pts.append(data.non_primary_segments.reshape(-1, 2))
    pts.append(np.array([data.origin_xy], dtype=np.float64))
    pts_combined: np.ndarray = np.concatenate(pts, axis=0)
    x_min: float = float(pts_combined[:, 0].min())
    x_max: float = float(pts_combined[:, 0].max())
    y_min: float = float(pts_combined[:, 1].min())
    y_max: float = float(pts_combined[:, 1].max())
    cx: float = (x_min + x_max) / 2.0
    cy: float = (y_min + y_max) / 2.0
    half: float = max(x_max - x_min, y_max - y_min) * 0.6 + 15.0
    ax.set_xlim(cx - half, cx + half)
    ax.set_ylim(cy - half, cy + half)

    # Title.
    title_top: str = f"{data.cell_id}  [{data.stratum_tag}]"
    pbc: float = data.primary_branch_pd_concentration
    title_mid: str = (
        f"soma_off={data.soma_offset_pd_um:+.1f}um  elong={data.field_elongation_pd:.2f}\n"
        f"bdg={data.branch_density_gradient_pd:+.2f}  pbc={pbc:.2f}"
    )
    ax.set_title(f"{title_top}\n{title_mid}", fontsize=7)

    # Check booleans annotation in the bottom-right corner.
    ax.text(
        x=0.98,
        y=0.02,
        s=(
            f"C1={_pass_str(b=data.check1_pass)}  "
            f"C2={_pass_str(b=data.check2_pass)}  "
            f"C3={_pass_str(b=data.check3_pass)}\n"
            f"soma_frame_off={data.soma_frame_offset_um:.1f}um"
        ),
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=6,
        color=(
            PASS_COLOR
            if (data.check1_pass and data.check2_pass and data.check3_pass)
            else FAIL_COLOR
        ),
        bbox={
            "facecolor": "white",
            "edgecolor": "lightgray",
            "alpha": 0.85,
            "boxstyle": "round,pad=0.2",
        },
    )


def main() -> None:
    ensure_directories()
    print(f"[gallery] reading {SECTION_ENDPOINTS_DUMP_JSON}", flush=True)
    cells: list[dict[str, Any]] = json.loads(
        SECTION_ENDPOINTS_DUMP_JSON.read_text(encoding="utf-8")
    )
    print(f"[gallery] loaded {len(cells)} cells", flush=True)

    df_checks: pd.DataFrame = pd.read_csv(COORDINATE_CONSISTENCY_CHECKS_CSV)
    checks_by_cell: dict[str, pd.Series] = {
        str(row[CELL_ID_COL]): row for _, row in df_checks.iterrows()
    }

    # Order cells by stratum tag for visual grouping, then by cell_id within stratum.
    stratum_order: list[str] = [
        "SOMA_OFFSET_TOP",
        "ELONGATION_TOP",
        "ELONGATION_BOTTOM",
        "BRANCH_DENSITY_TOP",
        "PRIMARY_CONCENTRATION_TOP",
        "WORST_LOOKING",
        "SYMMETRIC_CONTROL",
    ]

    def _sort_key(c: dict[str, Any]) -> tuple[int, str]:
        try:
            idx: int = stratum_order.index(c[STRATUM_TAG_COL])
        except ValueError:
            idx = len(stratum_order)
        return (idx, c["cell_id"])

    cells_sorted: list[dict[str, Any]] = sorted(cells, key=_sort_key)

    panels: list[CellPanelData] = []
    for cell in cells_sorted:
        cell_id: str = str(cell["cell_id"])
        checks_row: pd.Series = checks_by_cell[cell_id]
        panels.append(_build_panel_data(cell=cell, checks_row=checks_row))

    fig, axes = plt.subplots(
        nrows=GRID_ROWS,
        ncols=GRID_COLS,
        figsize=(GRID_COLS * PANEL_INCH_W, GRID_ROWS * PANEL_INCH_H),
        dpi=DPI,
    )
    axes_flat = axes.flatten()
    for i, ax in enumerate(axes_flat):
        ax.set_xticks([])
        ax.set_yticks([])
        if i >= len(panels):
            ax.set_axis_off()
            ax.text(
                x=0.5,
                y=0.5,
                s="(empty)",
                ha="center",
                va="center",
                fontsize=10,
                color="lightgray",
                transform=ax.transAxes,
            )
            continue
        _render_panel(ax=ax, data=panels[i])

    n_pass_all: int = sum(1 for p in panels if p.check1_pass and p.check2_pass and p.check3_pass)
    fig.suptitle(
        f"t0120 morphology generator geometry audit gallery: "
        f"{len(panels)} cells stratified across asymmetry-parameter extremes. "
        f"All-checks-pass: {n_pass_all}/{len(panels)}. "
        f"Red = primary stems (linewidth 2.0), blue = non-primary dendrites, "
        f"grey circle = soma scaled to soma_diameter_um. "
        f"Thin black debug line from origin_xy to each primary-stem tip.",
        fontsize=10,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.97))
    fig.savefig(GEOMETRY_AUDIT_GALLERY_PNG, dpi=DPI)
    plt.close(fig)
    size_kb: float = GEOMETRY_AUDIT_GALLERY_PNG.stat().st_size / 1024.0
    print(
        f"[gallery] saved gallery with {len(panels)} panels to {GEOMETRY_AUDIT_GALLERY_PNG} "
        f"(size = {size_kb:.1f} KB)",
        flush=True,
    )
    # Sanity check: file should be > 50 KB (a 4x5 grid at dpi=150 should be ~hundreds of KB).
    if size_kb < 50.0:
        raise RuntimeError(
            f"Gallery PNG suspiciously small ({size_kb:.1f} KB); rendering may have failed."
        )


if __name__ == "__main__":
    # quiet unused-import warning for math
    _ = math.pi
    main()
