"""Render the t0122 top-50 morphology grid with FULL DENDRITE TREES.

Per memory ``feedback_top50_morphologies_full_dendrites.md`` and the
t0114 operator-rejection precedent: this chart MUST draw the full
dendrite trees, NOT just soma dots. Every dendrite section of every cell
is drawn using the procedural ``generate_fixed_morphology`` entry point;
the soma is overlaid as a coloured circle.

The 50 cells are ranked by joint-pass tier and DSI. PD-rate is recovered
from the per-cell JSONL trace written by the evaluator (see
``T0122_CELL_TRACE_JSONL`` env var inside ``evaluator.py``). The chart
is saved as ``top50_morphologies_seed<S>.png`` in
``results/images/``.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle

# ---------------------------------------------------------------------------
# Paths and project bootstrap
# ---------------------------------------------------------------------------

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0122_dsi_cytoplasm_volume_nsga2"
RESULTS_DATA_DIR: Path = TASK_ROOT / "results" / "data"
OUT_IMAGES_DIR: Path = TASK_ROOT / "results" / "images"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Monkey-patch the t0080 / t0090 DLL loader so morphology generation works
# without compiled MOD libraries locally (we only need geometry, not biophysics).
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

# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------

DSI_THRESHOLD: float = 0.5
PD_RATE_THRESHOLD_HZ: float = 30.0
LEGIT_DSI_CEILING: float = 0.9999
TOP_K_MORPHOLOGY: int = 50
VOLUME_CEILING_UM3: float = 50000.0


@dataclass(frozen=True, slots=True)
class CellGeometry:
    rank: int
    generation: int
    dsi: float
    pd_rate_hz: float
    volume_um3: float
    tier_color: str
    dendrite_segments: np.ndarray
    soma_xy: np.ndarray


def _params_from_14d(*, vec: tuple[float, ...]) -> MorphologyParams:
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


def _is_joint_pass(c: dict[str, Any]) -> bool:
    return (
        float(c["dsi_vector_sum"]) >= DSI_THRESHOLD
        and float(c["pd_rate_hz"]) >= PD_RATE_THRESHOLD_HZ
        and float(c["cytoplasm_volume_um3"]) <= VOLUME_CEILING_UM3
    )


def _is_legit(c: dict[str, Any]) -> bool:
    return float(c["dsi_vector_sum"]) < LEGIT_DSI_CEILING


def _tier_color(c: dict[str, Any]) -> str:
    is_jp = _is_joint_pass(c)
    is_silence = float(c["dsi_vector_sum"]) >= LEGIT_DSI_CEILING
    if is_jp and not is_silence:
        return "green"
    if is_silence:
        return "red"
    if not is_silence and not is_jp:
        return "tab:blue"
    return "orange"


def _rank_key(c: dict[str, Any]) -> tuple[int, float, float]:
    is_jp = _is_joint_pass(c)
    is_legit = _is_legit(c)
    if is_jp and is_legit:
        tier = 3
    elif is_jp and not is_legit:
        tier = 2
    elif is_legit:
        tier = 1
    else:
        tier = 0
    dsi = float(c["dsi_vector_sum"])
    legit_dsi = dsi if is_legit else 0.0
    # t0122: lower cytoplasm volume is better (cost objective).
    inv_volume = -float(c["cytoplasm_volume_um3"])
    return (tier, legit_dsi, inv_volume)


def _build_geometry(*, rank: int, cell: dict[str, Any]) -> CellGeometry:
    morph_vec: tuple[float, ...] = tuple(cell["vector_68d"][54:68])
    params = _params_from_14d(vec=morph_vec)
    result: MorphologyResult = generate_fixed_morphology(
        params=params, morph_seed=int(params.morph_seed)
    )
    dend_segments: list[tuple[tuple[float, float], tuple[float, float]]] = []
    soma_xy: tuple[float, float] = (
        float(result.origin_xy[0]),
        float(result.origin_xy[1]),
    )
    for sec_name, (x0, y0, x1, y1) in result.section_endpoints_xy.items():
        if sec_name == "soma":
            continue
        if "ais" in sec_name.lower():
            continue
        dend_segments.append(
            (
                (float(x0), float(y0)),
                (float(x1), float(y1)),
            )
        )
    dend_arr: np.ndarray = (
        np.array(dend_segments, dtype=np.float64)
        if len(dend_segments) > 0
        else np.zeros((0, 2, 2), dtype=np.float64)
    )
    return CellGeometry(
        rank=rank,
        generation=int(cell.get("generation", -1)),
        dsi=float(cell["dsi_vector_sum"]),
        pd_rate_hz=float(cell["pd_rate_hz"]),
        volume_um3=float(cell["cytoplasm_volume_um3"]),
        tier_color=_tier_color(cell),
        dendrite_segments=dend_arr,
        soma_xy=np.array(soma_xy, dtype=np.float64),
    )


def _render_panel(*, ax: Any, geom: CellGeometry) -> None:
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_yticks([])
    if geom.dendrite_segments.shape[0] > 0:
        lc = LineCollection(
            segments=geom.dendrite_segments,
            colors=geom.tier_color,
            linewidths=0.4,
            alpha=0.85,
        )
        ax.add_collection(lc)
    soma_circle = Circle(
        xy=(float(geom.soma_xy[0]), float(geom.soma_xy[1])),
        radius=6.0,
        facecolor=geom.tier_color,
        edgecolor="black",
        linewidth=0.4,
        zorder=10,
    )
    ax.add_patch(soma_circle)
    pts: list[np.ndarray] = []
    if geom.dendrite_segments.shape[0] > 0:
        pts.append(geom.dendrite_segments.reshape(-1, 2))
    pts.append(geom.soma_xy.reshape(1, 2))
    pts_combined = np.concatenate(pts, axis=0)
    x_min, y_min = pts_combined.min(axis=0)
    x_max, y_max = pts_combined.max(axis=0)
    cx: float = float(0.5 * (x_min + x_max))
    cy: float = float(0.5 * (y_min + y_max))
    half: float = float(max(x_max - x_min, y_max - y_min) * 0.55 + 10.0)
    ax.set_xlim(cx - half, cx + half)
    ax.set_ylim(cy - half, cy + half)
    title = (
        f"#{geom.rank} g{geom.generation}\n"
        f"DSI={geom.dsi:.3f}  V={geom.volume_um3:.0f}um^3\n"
        f"PD={geom.pd_rate_hz:.1f}Hz"
    )
    ax.set_title(title, fontsize=6)


def _load_cells_from_trace(*, trace_path: Path) -> list[dict[str, Any]]:
    """Read all per-cell records from the side-channel JSONL trace."""
    cells: list[dict[str, Any]] = []
    with trace_path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line == "":
                continue
            try:
                cells.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return cells


def build_top50_grid(*, seed: int) -> Path:
    """Build the top-50 morphology grid PNG for the given GA seed."""
    OUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    trace_path = RESULTS_DATA_DIR / f"cell_trace_seed{seed}.jsonl"
    out_path = OUT_IMAGES_DIR / f"top50_morphologies_seed{seed}.png"

    print(f"[morph] loading {trace_path}")
    cells = _load_cells_from_trace(trace_path=trace_path)
    print(f"[morph] total cell records: {len(cells)}")

    # Deduplicate by full 68-d vector.
    seen_keys: set[tuple[float, ...]] = set()
    unique_cells: list[dict[str, Any]] = []
    for c in cells:
        k = tuple(float(v) for v in c["vector_68d"])
        if k not in seen_keys:
            seen_keys.add(k)
            unique_cells.append(c)
    print(f"[morph] unique cells: {len(unique_cells)}")

    sorted_cells = sorted(unique_cells, key=_rank_key, reverse=True)
    top = sorted_cells[:TOP_K_MORPHOLOGY]
    print(f"[morph] selected top-{len(top)} cells")

    geoms: list[CellGeometry] = []
    for i, c in enumerate(top):
        geom = _build_geometry(rank=i + 1, cell=c)
        geoms.append(geom)
        if (i + 1) % 10 == 0:
            print(f"[morph]   built geometry {i + 1}/{len(top)}")
    print(f"[morph] built {len(geoms)} geometries")

    fig, axes = plt.subplots(5, 10, figsize=(22, 12), dpi=110)
    axes_flat = axes.flatten()
    for i, ax in enumerate(axes_flat):
        ax.set_xticks([])
        ax.set_yticks([])
        if i >= len(geoms):
            ax.text(
                0.5,
                0.5,
                "n/a",
                ha="center",
                va="center",
                fontsize=10,
                color="lightgrey",
                transform=ax.transAxes,
            )
            ax.set_axis_off()
            continue
        _render_panel(ax=ax, geom=geoms[i])
    fig.suptitle(
        f"t0122 seed {seed}: top-50 cells with FULL dendrite trees "
        f"(unique cells={len(unique_cells)} of {len(cells)} records).  "
        f"Colour: green = LEGIT joint-pass (DSI >= 0.5, PD >= 30 Hz, "
        f"vol <= 50000), red = silence-guard DSI >= 0.9999, "
        f"blue = neither, orange = silence-guard joint-pass.  "
        f"Ranked by tier then legit DSI then -volume.",
        fontsize=10,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.94))
    fig.savefig(out_path, dpi=110)
    plt.close(fig)
    print(f"[morph] wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    build_top50_grid(seed=int(args.seed))


if __name__ == "__main__":
    main()
