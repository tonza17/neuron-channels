"""Phase E.1: 2D dendrogram + grid panel rendering.

Reads ``MorphologyParams`` JSONs, builds the procedural cell, and produces:

* ``results/images/morphology_grid_different.png`` (5x6 panel)
* ``results/images/morphology_grid_similar.png`` (5x6 panel)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless rendering on Windows
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from tasks.t0090_morphology_generator_diversity_test.code.generator import (
    generate_morphology,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
    MorphologyResult,
)
from tasks.t0090_morphology_generator_diversity_test.code.paths import (
    DATA_DIFFERENT_DIR,
    DATA_SIMILAR_DIR,
    RESULTS_IMAGES_DIR,
    ensure_directories,
)

# Okabe-Ito palette (re-used inline so we do not couple to t0011's exact path).
OKABE_ITO_PALETTE: tuple[str, ...] = (
    "#000000",
    "#E69F00",
    "#56B4E9",
    "#009E73",
    "#F0E442",
    "#0072B2",
    "#D55E00",
    "#CC79A7",
)

GRID_NCOLS: int = 6
GRID_NROWS: int = 5
DEFAULT_LINE_COLOR_DIFFERENT: str = "#0072B2"
DEFAULT_LINE_COLOR_SIMILAR: str = "#D55E00"


def _line_segments_for_cell(
    *, cell: MorphologyResult
) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """Return a list of ((x0,y0), (x1,y1)) line segments per dendrite."""
    out: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for sec in cell.all_dends:
        name = sec.name()
        # Strip the "_t90" suffix to match the section_endpoints_xy keys.
        stripped = name[:-4] if name.endswith("_t90") else name
        endpoints = cell.section_endpoints_xy.get(stripped)
        if endpoints is None:
            continue
        x0, y0, x1, y1 = endpoints
        out.append(((float(x0), float(y0)), (float(x1), float(y1))))
    return out


def plot_dendrogram(
    *,
    cell: MorphologyResult,
    ax: matplotlib.axes.Axes,
    color: str,
    line_width_scale: float = 0.8,
) -> None:
    """Plot a 2D dendrogram of the procedural cell on a matplotlib axis."""
    segments = _line_segments_for_cell(cell=cell)
    diam_widths: list[float] = []
    for sec in cell.all_dends:
        diam_widths.append(float(sec.diam) * line_width_scale)
    if len(segments) > 0:
        lc = LineCollection(segments, linewidths=diam_widths, colors=color, alpha=0.85)
        ax.add_collection(lc)
    # Mark the soma with a circle.
    soma_x, soma_y = cell.origin_xy
    ax.scatter([soma_x], [soma_y], s=20, c="black", marker="o", zorder=5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    if len(segments) > 0:
        all_x = [p[0] for seg in segments for p in seg] + [soma_x]
        all_y = [p[1] for seg in segments for p in seg] + [soma_y]
        if len(all_x) > 1:
            ax.set_xlim(min(all_x) - 20.0, max(all_x) + 20.0)
            ax.set_ylim(min(all_y) - 20.0, max(all_y) + 20.0)


def make_grid_panel(
    *,
    morph_jsons: list[Path],
    output_png: Path,
    title: str,
    line_color: str,
) -> None:
    """Build a 5x6 grid of dendrograms and save to PNG."""
    fig, axes = plt.subplots(
        nrows=GRID_NROWS,
        ncols=GRID_NCOLS,
        figsize=(GRID_NCOLS * 2.4, GRID_NROWS * 2.4),
    )
    fig.suptitle(title, fontsize=14)
    axes_flat = axes.flatten()
    for i, morph_path in enumerate(morph_jsons[: GRID_NCOLS * GRID_NROWS]):
        data = json.loads(morph_path.read_text())
        params = MorphologyParams.from_dict(data=data)
        try:
            cell = generate_morphology(params=params, morph_seed=int(params.morph_seed))
            plot_dendrogram(cell=cell, ax=axes_flat[i], color=line_color)
            axes_flat[i].set_title(f"{morph_path.stem}", fontsize=7)
        except (RuntimeError, ValueError, ArithmeticError, AssertionError) as exc:
            axes_flat[i].text(
                0.5,
                0.5,
                f"build failed:\n{type(exc).__name__}",
                ha="center",
                va="center",
                fontsize=6,
            )
            axes_flat[i].set_xticks([])
            axes_flat[i].set_yticks([])
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    fig.savefig(output_png, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    ensure_directories()

    different_jsons = sorted(DATA_DIFFERENT_DIR.glob("morph_*.json"))
    similar_jsons = sorted(DATA_SIMILAR_DIR.glob("morph_*.json"))
    if args.limit is not None:
        different_jsons = different_jsons[: args.limit]
        similar_jsons = similar_jsons[: args.limit]

    out_diff = RESULTS_IMAGES_DIR / "morphology_grid_different.png"
    out_sim = RESULTS_IMAGES_DIR / "morphology_grid_similar.png"

    print(f"rendering {len(different_jsons)} different morphologies -> {out_diff}")
    make_grid_panel(
        morph_jsons=different_jsons,
        output_png=out_diff,
        title="30 Very-Different Morphologies (Latin Hypercube over 14-d space)",
        line_color=DEFAULT_LINE_COLOR_DIFFERENT,
    )
    print(f"rendering {len(similar_jsons)} similar morphologies -> {out_sim}")
    make_grid_panel(
        morph_jsons=similar_jsons,
        output_png=out_sim,
        title="30 Very-Similar Morphologies (+/- 5 percent jitter around BedB)",
        line_color=DEFAULT_LINE_COLOR_SIMILAR,
    )
    print("done")


if __name__ == "__main__":
    main()
