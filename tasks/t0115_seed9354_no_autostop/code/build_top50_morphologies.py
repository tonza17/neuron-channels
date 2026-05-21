"""Render the t0115 top-50 morphology grid with FULL DENDRITE TREES.

Operator feedback (CRITICAL): t0114's `top50_morphologies_seed7755.png` drew
only soma dots and was rejected. This script draws every dendrite section of
every cell using the project's `generate_fixed_morphology` helper, exactly
like t0099 / t0102 / t0103 cross-seed morphology grids.

10 rows x 5 columns = 50 cells, ranked by joint-pass tier (LEGIT joint-pass
first, then silence-guard joint-pass, then legit non-joint-pass, then other)
then by legit DSI then by PD-rate.

Verification step in the orchestrator's step log includes a visual sanity
check of the saved PNG to confirm dendrite branches are drawn.
"""

from __future__ import annotations

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
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0115_seed9354_no_autostop"
EVALS_PATH: Path = TASK_ROOT / "results" / "data" / "all_evaluations_seed9354.json"
OUT_IMAGES_DIR: Path = TASK_ROOT / "results" / "images"
OUT_PATH: Path = OUT_IMAGES_DIR / "top50_morphologies_seed9354.png"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Monkey-patch the t0080 / t0090 DLL loader so morphology generation works
# without compiled MOD libraries (we only need geometry, not biophysics).
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


# ---------------------------------------------------------------------------
# Data containers
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class CellGeometry:
    rank: int
    generation: int
    dsi: float
    pd_rate_hz: float
    tier_color: str
    dendrite_segments: np.ndarray
    soma_xy: np.ndarray


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


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
    return (tier, legit_dsi, float(c["pd_rate_hz"]))


def _build_geometry(
    *,
    rank: int,
    cell: dict[str, Any],
) -> CellGeometry:
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
        generation=int(cell["generation"]),
        dsi=float(cell["dsi_vector_sum"]),
        pd_rate_hz=float(cell["pd_rate_hz"]),
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
    title = f"#{geom.rank} g{geom.generation}\nDSI={geom.dsi:.3f}  PD={geom.pd_rate_hz:.1f}Hz"
    ax.set_title(title, fontsize=7)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    OUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[morph] loading {EVALS_PATH}")
    data = json.loads(EVALS_PATH.read_text(encoding="utf-8"))
    evals = data["evaluations"] if isinstance(data, dict) else data
    print(f"[morph] total evaluations: {len(evals)}")

    # Deduplicate by full 68-d vector.
    seen_keys: set[tuple[float, ...]] = set()
    unique_cells: list[dict[str, Any]] = []
    for c in evals:
        k = tuple(c["vector_68d"])
        if k not in seen_keys:
            seen_keys.add(k)
            unique_cells.append(c)
    print(f"[morph] unique cells: {len(unique_cells)}")

    sorted_cells = sorted(unique_cells, key=_rank_key, reverse=True)
    top = sorted_cells[:TOP_K_MORPHOLOGY]
    print(f"[morph] selected top-{len(top)} cells")

    # Build geometries.
    geoms: list[CellGeometry] = []
    for i, c in enumerate(top):
        geom = _build_geometry(rank=i + 1, cell=c)
        geoms.append(geom)
        if (i + 1) % 10 == 0:
            print(f"[morph]   built geometry {i + 1}/{len(top)}")
    print(f"[morph] built {len(geoms)} geometries")

    # Render 5 rows x 10 columns to match task spec (10x5 grid).
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
        f"t0115 seed 9354: top-50 cells with FULL dendrite trees "
        f"(unique cells={len(unique_cells)} of {len(evals)} evals).  "
        f"Colour: green = LEGIT joint-pass, red = silence-guard DSI>=0.9999, "
        f"blue = neither, orange = silence-guard joint-pass.  Ranked by "
        f"tier then legit DSI then PD-rate.",
        fontsize=11,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.95))
    fig.savefig(OUT_PATH, dpi=110)
    plt.close(fig)
    print(f"[morph] wrote {OUT_PATH}")
    print(f"[morph] file size = {OUT_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
