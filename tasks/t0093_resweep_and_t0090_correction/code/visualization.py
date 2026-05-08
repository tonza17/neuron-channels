"""Visualisations for the t0093 patched-generator re-sweep.

Three charts:

1. ``post_fix_morphology_grid.png`` — 6x10 grid (60 cells) coloured by post-fix
   stability flag (stable_firing / stable_silent / nan_voltage / diverged /
   disconnected).
2. ``pre_vs_post_spike_counts.png`` — paired bar chart (pre red / post green)
   per cell, sorted by post-fix spike count descending.
3. ``transition_flow.png`` — stacked-bar transition flow (pre / post columns)
   broken down by stability flag and per-cell transition label.

Adapted from t0090's ``visualization.py`` (``plot_dendrogram``,
``_line_segments_for_cell``, ``OKABE_ITO_PALETTE``, ``make_grid_panel``).
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import matplotlib

matplotlib.use("Agg")  # headless rendering on Windows
import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.patches import Patch

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
    MorphologyResult,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (
    generate_fixed_morphology,
)
from tasks.t0093_resweep_and_t0090_correction.code.constants import (
    DISPLAY_FLAG_STABLE_FIRING,
    DISPLAY_FLAG_STABLE_SILENT,
    FIELD_MORPH_ID,
    FIELD_PD_RATE_HZ,
    FIELD_PER_DIRECTION_SPIKES,
    FIELD_POPULATION,
    FIELD_PRE_FIX_SPIKE_COUNT_TOTAL,
    FIELD_STABILITY_FLAG,
    OKABE_ITO_BLUE,
    OKABE_ITO_VERMILLION,
    STABILITY_FLAG_DISCONNECTED,
    STABILITY_FLAG_DIVERGED,
    STABILITY_FLAG_NAN_VOLTAGE,
    STABILITY_FLAG_STABLE,
    STABILITY_FLAG_TO_COLOR,
)
from tasks.t0093_resweep_and_t0090_correction.code.paths import (
    DATA_POST_FIX_VERIFICATION_JSON,
    DATA_PRE_POST_DELTA_JSON,
    POST_FIX_GRID_PNG,
    PRE_VS_POST_BAR_PNG,
    T0090_DIFFERENT_DIR,
    T0090_SIMILAR_DIR,
    TRANSITION_FLOW_PNG,
    ensure_directories,
)

GRID_NCOLS: int = 10
GRID_NROWS: int = 6


@dataclass(frozen=True, slots=True)
class CellRowSummary:
    population: str
    morph_id: str
    stability_flag: str
    pd_rate_hz: float | None
    post_spike_count_total: int
    pre_fix_spike_count_total: int


def _line_segments_for_cell(
    *,
    cell: MorphologyResult,
) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """Return a list of ((x0,y0),(x1,y1)) line segments per dendrite."""
    out: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for sec in cell.all_dends:
        name = sec.name()
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


def _row_summary(*, row: dict[str, Any]) -> CellRowSummary:
    per_dir: dict[str, int] = row.get(FIELD_PER_DIRECTION_SPIKES, {}) or {}
    return CellRowSummary(
        population=str(row[FIELD_POPULATION]),
        morph_id=str(row[FIELD_MORPH_ID]),
        stability_flag=str(row[FIELD_STABILITY_FLAG]),
        pd_rate_hz=(None if row.get(FIELD_PD_RATE_HZ) is None else float(row[FIELD_PD_RATE_HZ])),
        post_spike_count_total=int(sum(int(v) for v in per_dir.values())),
        pre_fix_spike_count_total=int(row.get(FIELD_PRE_FIX_SPIKE_COUNT_TOTAL, 0) or 0),
    )


def _display_flag_for(*, summary: CellRowSummary) -> str:
    if summary.stability_flag == STABILITY_FLAG_STABLE:
        if summary.pd_rate_hz is not None and summary.pd_rate_hz > 0.0:
            return DISPLAY_FLAG_STABLE_FIRING
        return DISPLAY_FLAG_STABLE_SILENT
    return summary.stability_flag


def _morph_path_for(*, summary: CellRowSummary) -> Path:
    base = T0090_DIFFERENT_DIR if summary.population == "different" else T0090_SIMILAR_DIR
    return base / f"{summary.morph_id}.json"


def make_post_fix_grid_panel(
    *,
    summary_path: Path,
    output_png: Path,
) -> None:
    """Build a 6x10 grid (60 cells) coloured by post-fix stability flag."""
    raw = json.loads(summary_path.read_text())
    assert isinstance(raw, list), f"expected list, got {type(raw).__name__}"
    summaries: list[CellRowSummary] = [_row_summary(row=r) for r in raw if isinstance(r, dict)]
    # Sort: different first then similar; preserve morph_index ordering.
    summaries.sort(key=lambda s: (s.population, s.morph_id))

    fig, axes = plt.subplots(
        nrows=GRID_NROWS,
        ncols=GRID_NCOLS,
        figsize=(GRID_NCOLS * 2.2, GRID_NROWS * 2.2),
    )
    fig.suptitle(
        "Post-fix morphology grid (60 cells, coloured by stability flag)",
        fontsize=14,
    )
    axes_flat = axes.flatten()
    for i, summary in enumerate(summaries[: GRID_NCOLS * GRID_NROWS]):
        ax = cast(matplotlib.axes.Axes, axes_flat[i])
        morph_path = _morph_path_for(summary=summary)
        flag = _display_flag_for(summary=summary)
        color = STABILITY_FLAG_TO_COLOR.get(flag, OKABE_ITO_BLUE)
        try:
            params = MorphologyParams.from_dict(data=json.loads(morph_path.read_text()))
            cell = generate_fixed_morphology(
                params=params,
                morph_seed=int(params.morph_seed),
            )
            plot_dendrogram(cell=cell, ax=ax, color=color)
        except (RuntimeError, ValueError, ArithmeticError, AssertionError) as exc:
            ax.text(
                0.5,
                0.5,
                f"build failed:\n{type(exc).__name__}",
                ha="center",
                va="center",
                fontsize=6,
            )
            ax.set_xticks([])
            ax.set_yticks([])
        ax.set_title(
            f"{summary.population[:3]}/{summary.morph_id}\n{flag}",
            fontsize=6,
        )

    # Build a legend using the colour map.
    legend_handles: list[Patch] = []
    for label, hex_color in STABILITY_FLAG_TO_COLOR.items():
        legend_handles.append(Patch(facecolor=hex_color, edgecolor="black", label=label))
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        ncol=len(legend_handles),
        bbox_to_anchor=(0.5, -0.02),
        fontsize=8,
    )

    fig.tight_layout(rect=(0.0, 0.04, 1.0, 0.96))
    fig.savefig(str(output_png), dpi=150, bbox_inches="tight")
    plt.close(fig)


def make_paired_bar_chart(
    *,
    summary_path: Path,
    output_png: Path,
) -> None:
    """Per-cell paired bar chart (pre red / post green), sorted by post desc."""
    raw = json.loads(summary_path.read_text())
    summaries: list[CellRowSummary] = [_row_summary(row=r) for r in raw if isinstance(r, dict)]
    summaries.sort(key=lambda s: -s.post_spike_count_total)

    n = len(summaries)
    x = np.arange(n)
    width = 0.4

    pre_counts = np.array(
        [s.pre_fix_spike_count_total for s in summaries],
        dtype=np.float64,
    )
    post_counts = np.array(
        [s.post_spike_count_total for s in summaries],
        dtype=np.float64,
    )

    fig, ax = plt.subplots(figsize=(max(12.0, n * 0.18), 5.0))
    ax.bar(
        x - width / 2.0,
        pre_counts,
        width=width,
        color=OKABE_ITO_VERMILLION,
        label="pre-fix (t0090)",
    )
    ax.bar(
        x + width / 2.0,
        post_counts,
        width=width,
        color="#009E73",
        label="post-fix (t0093 patched)",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(
        [f"{s.population[:3]}/{s.morph_id[-2:]}" for s in summaries],
        rotation=90,
        fontsize=6,
    )
    ax.set_ylabel("Total spikes across 8 directions")
    ax.set_xlabel("Cells (sorted by post-fix spike count, descending)")
    ax.set_title("Pre-fix vs post-fix per-cell total spike count")
    ax.legend()
    fig.tight_layout()
    fig.savefig(str(output_png), dpi=150, bbox_inches="tight")
    plt.close(fig)


def _stack_flag_for(*, stability_flag: str, spike_count: int, pd_rate: float | None) -> str:
    if stability_flag == STABILITY_FLAG_STABLE:
        if (pd_rate is not None and pd_rate > 0.0) or spike_count > 0:
            return DISPLAY_FLAG_STABLE_FIRING
        return DISPLAY_FLAG_STABLE_SILENT
    return stability_flag


def make_transition_flow_chart(
    *,
    delta_path: Path,
    output_png: Path,
) -> None:
    """Stacked-bar transition flow: two columns (pre / post), stacked by flag."""
    payload = json.loads(delta_path.read_text())
    cells = payload["cells"]
    assert isinstance(cells, list)

    flag_order: list[str] = [
        DISPLAY_FLAG_STABLE_FIRING,
        DISPLAY_FLAG_STABLE_SILENT,
        STABILITY_FLAG_NAN_VOLTAGE,
        STABILITY_FLAG_DIVERGED,
        STABILITY_FLAG_DISCONNECTED,
    ]
    pre_counts: dict[str, int] = {f: 0 for f in flag_order}
    post_counts: dict[str, int] = {f: 0 for f in flag_order}

    for c in cells:
        pre_flag = _stack_flag_for(
            stability_flag=str(c["pre_stability_flag"]),
            spike_count=int(c["pre_spike_count_total"]),
            pd_rate=(None if c.get("pre_pd_rate_hz") is None else float(c["pre_pd_rate_hz"])),
        )
        post_flag = _stack_flag_for(
            stability_flag=str(c["post_stability_flag"]),
            spike_count=int(c["post_spike_count_total"]),
            pd_rate=(None if c.get("post_pd_rate_hz") is None else float(c["post_pd_rate_hz"])),
        )
        pre_counts[pre_flag] = pre_counts.get(pre_flag, 0) + 1
        post_counts[post_flag] = post_counts.get(post_flag, 0) + 1

    fig, ax = plt.subplots(figsize=(7.0, 6.0))
    columns: list[str] = ["pre-fix (t0090)", "post-fix (t0093 patched)"]
    x = np.arange(len(columns))
    bottoms = np.zeros(len(columns), dtype=np.float64)
    for flag in flag_order:
        heights = np.array([pre_counts[flag], post_counts[flag]], dtype=np.float64)
        color = STABILITY_FLAG_TO_COLOR.get(flag, OKABE_ITO_BLUE)
        ax.bar(
            x,
            heights,
            bottom=bottoms,
            color=color,
            edgecolor="black",
            label=flag,
        )
        # Annotate the count inside each segment.
        for xi, h, b in zip(x, heights, bottoms, strict=True):
            if h > 0:
                ax.text(
                    xi,
                    b + h / 2.0,
                    f"{int(h)}",
                    ha="center",
                    va="center",
                    fontsize=9,
                    color="black",
                )
        bottoms += heights

    ax.set_xticks(x)
    ax.set_xticklabels(columns)
    ax.set_ylabel("Cells")
    ax.set_title("Stability transition flow: pre-fix -> post-fix")
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=9)
    fig.tight_layout()
    fig.savefig(str(output_png), dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-grid", action="store_true")
    args = parser.parse_args()
    ensure_directories()

    if not args.skip_grid:
        print(f"rendering grid -> {POST_FIX_GRID_PNG}")
        make_post_fix_grid_panel(
            summary_path=DATA_POST_FIX_VERIFICATION_JSON,
            output_png=POST_FIX_GRID_PNG,
        )
    print(f"rendering paired bars -> {PRE_VS_POST_BAR_PNG}")
    make_paired_bar_chart(
        summary_path=DATA_POST_FIX_VERIFICATION_JSON,
        output_png=PRE_VS_POST_BAR_PNG,
    )
    print(f"rendering transition flow -> {TRANSITION_FLOW_PNG}")
    make_transition_flow_chart(
        delta_path=DATA_PRE_POST_DELTA_JSON,
        output_png=TRANSITION_FLOW_PNG,
    )
    print("done")


if __name__ == "__main__":
    main()
