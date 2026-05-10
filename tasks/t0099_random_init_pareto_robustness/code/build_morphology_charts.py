"""Render morphology charts for the t0099 random-init Pareto cells.

Two charts:
1. Cross-seed top-cell row (4 panels): t0091 joint-pass reference + best real cell
   from seeds 11/22/33.
2. Cross-seed top-15 grid (5 cols x 3 rows): top 5 real cells from each seed,
   colored by nearest t0091 anchor.

Reuses the t0098 visualisation pattern: monkey-patch the t0090 generator's DLL
loader, build the morphology, extract section_endpoints_xy, render with matplotlib.
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

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0099_random_init_pareto_robustness"
T0091_DATA_DIR: Path = (
    REPO_ROOT / "tasks" / "t0091_morphology_extended_nsga2_v1" / "results" / "data"
)
OUT_IMAGES_DIR: Path = TASK_ROOT / "results" / "images"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

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

ANCHOR_COLORS: dict[str, str] = {
    "bedb_like": "tab:blue",
    "symmetric": "tab:gray",
    "pd_asymmetric": "tab:red",
    "nd_asymmetric": "tab:green",
    "alt_topology": "tab:purple",
}
SEED_COLORS: dict[int, str] = {
    11: "tab:cyan",
    22: "tab:orange",
    33: "tab:olive",
}


@dataclass(frozen=True, slots=True)
class CellGeometry:
    label: str
    color: str
    dsi: float
    pd_rate_hz: float
    robustness: float
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


def _build_geometry(
    *,
    vector_68d: list[float],
    label: str,
    color: str,
    dsi: float,
    pd_rate_hz: float,
    robustness: float,
) -> CellGeometry:
    morph_vec: tuple[float, ...] = tuple(vector_68d[:14])
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
        label=label,
        color=color,
        dsi=dsi,
        pd_rate_hz=pd_rate_hz,
        robustness=robustness,
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
            colors=geom.color,
            linewidths=0.5,
            alpha=0.85,
        )
        ax.add_collection(lc)
    soma_circle = Circle(
        xy=(float(geom.soma_xy[0]), float(geom.soma_xy[1])),
        radius=8.0,
        facecolor=geom.color,
        edgecolor="black",
        linewidth=0.5,
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
        f"{geom.label}\nDSI={geom.dsi:.2f}  PD={geom.pd_rate_hz:.1f}Hz  rob={geom.robustness:.2f}"
    )
    ax.set_title(title, fontsize=8)


def _load_pareto(*, path: Path) -> list[dict[str, Any]]:
    d = json.loads(path.read_text(encoding="utf-8"))
    cells = d.get("cells") or d.get("pareto") or d.get("evaluations")
    if cells is None:
        return []
    return cells


def _load_anchor_tracking(*, seed: int) -> dict[int, str]:
    p = TASK_ROOT / "results" / "data" / f"anchor_tracking_seed{seed}.json"
    if not p.exists():
        return {}
    d = json.loads(p.read_text(encoding="utf-8"))
    out: dict[int, str] = {}
    for c in d.get("cells", []):
        out[int(c["cell_id"])] = str(c.get("nearest_anchor_name", ""))
    return out


def _top_n_real(*, cells: list[dict[str, Any]], n: int) -> list[dict[str, Any]]:
    real = [
        c
        for c in cells
        if (c.get("robustness") or 0) >= 0.5
        and (c.get("pd_rate_hz") or 0) >= 1.0
        and (c.get("dsi_vector_sum") or 0) > 0
    ]
    real.sort(key=lambda c: -(c["dsi_vector_sum"] * c["pd_rate_hz"] * c["robustness"]))
    return real[:n]


def main() -> None:
    OUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # ---------------- Headline cross-seed top-cell row ----------------
    # t0091 joint-pass reference cell
    t91_pareto = _load_pareto(path=T0091_DATA_DIR / "pareto_front.json")
    t91_joint = [
        c
        for c in t91_pareto
        if c["dsi_vector_sum"] >= 0.5 and c["pd_rate_hz"] >= 30 and c["robustness"] >= 0.7
    ]
    t91_best: dict[str, Any] | None = (
        t91_joint[0]
        if t91_joint
        else (sorted(t91_pareto, key=lambda c: -c["dsi_vector_sum"])[0] if t91_pareto else None)
    )

    # Per-seed Pareto + top cell
    seed_paretos: dict[int, list[dict[str, Any]]] = {}
    seed_top: dict[int, dict[str, Any]] = {}
    for s in (11, 22, 33):
        cells = _load_pareto(path=TASK_ROOT / "results" / "data" / f"pareto_front_seed{s}.json")
        seed_paretos[s] = cells
        top = _top_n_real(cells=cells, n=1)
        if top:
            seed_top[s] = top[0]

    geoms: list[CellGeometry] = []
    if t91_best is not None:
        geoms.append(
            _build_geometry(
                vector_68d=t91_best["vector_68d"],
                label="t0091 ref (warm-start joint-pass)",
                color="black",
                dsi=t91_best["dsi_vector_sum"],
                pd_rate_hz=t91_best["pd_rate_hz"],
                robustness=t91_best["robustness"],
            )
        )
    for s in (11, 22, 33):
        if s in seed_top:
            c = seed_top[s]
            geoms.append(
                _build_geometry(
                    vector_68d=c["vector_68d"],
                    label=f"seed {s} best real",
                    color=SEED_COLORS[s],
                    dsi=c["dsi_vector_sum"],
                    pd_rate_hz=c["pd_rate_hz"],
                    robustness=c["robustness"],
                )
            )

    n_panels = len(geoms)
    fig, axes = plt.subplots(nrows=1, ncols=n_panels, figsize=(4.0 * n_panels, 4.5), dpi=120)
    if n_panels == 1:
        axes = [axes]
    for ax, g in zip(axes, geoms, strict=False):
        _render_panel(ax=ax, geom=g)
    fig.suptitle(
        "Best cell comparison: t0091 warm-start vs t0099 random-init seeds 11/22/33",
        fontsize=12,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.93))
    out_headline: Path = OUT_IMAGES_DIR / "headline_best_cells.png"
    fig.savefig(out_headline, dpi=120)
    plt.close(fig)
    print(f"[morph] wrote {out_headline}")

    # ---------------- 5x3 cross-seed top-5 grid ----------------
    fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(20.0, 12.0), dpi=110)
    for row, s in enumerate((11, 22, 33)):
        anchors = _load_anchor_tracking(seed=s)
        top5 = _top_n_real(cells=seed_paretos[s], n=5)
        for col in range(5):
            ax = axes[row, col]
            ax.set_aspect("equal", adjustable="box")
            ax.set_xticks([])
            ax.set_yticks([])
            if col >= len(top5):
                ax.axis("off")
                continue
            cell = top5[col]
            cell_id: int = int(cell.get("cell_id", -1))
            anchor_name: str = anchors.get(cell_id, "unknown")
            color = ANCHOR_COLORS.get(anchor_name, "black")
            geom = _build_geometry(
                vector_68d=cell["vector_68d"],
                label=f"s{s} #{col + 1} ({anchor_name[:6]})",
                color=color,
                dsi=cell["dsi_vector_sum"],
                pd_rate_hz=cell["pd_rate_hz"],
                robustness=cell["robustness"],
            )
            _render_panel(ax=ax, geom=geom)
    fig.suptitle(
        "Top 5 real Pareto cells per seed (rows = seeds 11/22/33; color = nearest t0091 anchor)",
        fontsize=14,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.95))
    out_grid: Path = OUT_IMAGES_DIR / "cross_seed_top5_morphology_grid.png"
    fig.savefig(out_grid, dpi=110)
    plt.close(fig)
    print(f"[morph] wrote {out_grid}")


if __name__ == "__main__":
    main()
