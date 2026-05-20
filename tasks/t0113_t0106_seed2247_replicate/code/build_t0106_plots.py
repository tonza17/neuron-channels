"""Build all t0106 result figures from the saved seed44 evaluations + HV trace.

Produces in tasks/t0113_t0106_seed2247_replicate/results/images/:
  * top50_morphologies.png   10x5 grid of the best 50 cells by joint-corner score
  * pareto_front.png         DSI vs PD scatter coloured by generation
  * hv_vs_gen.png            hypervolume trajectory with annotations
  * asymmetry_distribution.png   soma offset / elongation distributions (top50 vs all)
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (
    MorphologyResult,
    generate_fixed_morphology,
)

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
IMPL_DIR: Path = TASK_ROOT / "logs" / "steps" / "009_implementation"
EVALS_PATH: Path = IMPL_DIR / "snapshots" / "all_evaluations_seed44_latest.json"
HV_TRACE_PATH: Path = IMPL_DIR / "hv_trace.jsonl"
OUT_DIR: Path = TASK_ROOT / "results" / "images"


@dataclass(frozen=True, slots=True)
class CellRecord:
    rank: int
    generation: int
    dsi: float
    pd_rate_hz: float
    vector_68d: list[float]


def _joint_score(*, dsi: float, pd_rate_hz: float) -> float:
    return min(dsi / 0.5, 1.0) * min(pd_rate_hz / 30.0, 1.0)


def _load_top_n(*, evals: list[dict[str, Any]], n: int) -> list[CellRecord]:
    sorted_evals = sorted(
        evals,
        key=lambda x: (
            _joint_score(dsi=x["dsi_vector_sum"], pd_rate_hz=x["pd_rate_hz"]),
            x["dsi_vector_sum"] + x["pd_rate_hz"] / 100,
        ),
        reverse=True,
    )
    seen: set[tuple[float, float]] = set()
    out: list[CellRecord] = []
    for e in sorted_evals:
        key = (round(e["dsi_vector_sum"], 4), round(e["pd_rate_hz"], 2))
        if key in seen:
            continue
        seen.add(key)
        out.append(
            CellRecord(
                rank=len(out) + 1,
                generation=int(e["generation"]),
                dsi=float(e["dsi_vector_sum"]),
                pd_rate_hz=float(e["pd_rate_hz"]),
                vector_68d=list(e["vector_68d"]),
            )
        )
        if len(out) >= n:
            break
    return out


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


@dataclass(frozen=True, slots=True)
class CellGeometry:
    label: str
    color: str
    soma_xy: np.ndarray
    dendrite_segments: np.ndarray


def _build_geometry(*, cell: CellRecord) -> CellGeometry:
    morph_vec: tuple[float, ...] = tuple(cell.vector_68d[54:68])
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
        dend_segments.append((((float(x0), float(y0))), (float(x1), float(y1))))
    dend_arr: np.ndarray = (
        np.array(dend_segments, dtype=np.float64)
        if dend_segments
        else np.zeros((0, 2, 2), dtype=np.float64)
    )
    soma = float(cell.vector_68d[59])
    if soma > 50:
        color = "#d62728"  # red - PD-soma (dends point ND)
    elif soma < -50:
        color = "#1f77b4"  # blue - ND-soma (dends point PD; classical DSGC)
    else:
        color = "#2ca02c"  # green - central
    return CellGeometry(
        label=f"#{cell.rank} g{cell.generation}\nDSI={cell.dsi:.3f} PD={cell.pd_rate_hz:.1f}Hz",
        color=color,
        soma_xy=np.array(soma_xy, dtype=np.float64),
        dendrite_segments=dend_arr,
    )


def _render_panel(*, ax: Any, geom: CellGeometry) -> None:
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_yticks([])
    if geom.dendrite_segments.shape[0] > 0:
        lc = LineCollection(
            segments=geom.dendrite_segments,
            colors=geom.color,
            linewidths=0.4,
            alpha=0.85,
        )
        ax.add_collection(lc)
    soma_circle = Circle(
        xy=(float(geom.soma_xy[0]), float(geom.soma_xy[1])),
        radius=8.0,
        facecolor=geom.color,
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
    cx, cy = 0.5 * (x_min + x_max), 0.5 * (y_min + y_max)
    half = float(max(x_max - x_min, y_max - y_min) * 0.55 + 10.0)
    ax.set_xlim(cx - half, cx + half)
    ax.set_ylim(cy - half, cy + half)
    ax.set_title(geom.label, fontsize=7)


def plot_top50_morphologies(*, top50: list[CellRecord]) -> None:
    fig, axes = plt.subplots(nrows=10, ncols=5, figsize=(15, 30), dpi=110)
    for i in range(50):
        ax = axes.flatten()[i]
        if i >= len(top50):
            ax.axis("off")
            continue
        geom = _build_geometry(cell=top50[i])
        _render_panel(ax=ax, geom=geom)
    fig.suptitle(
        "t0106 - top 50 cells by joint-corner score\n"
        "blue = ND-soma (classical DSGC, dends toward PD), "
        "green = central, red = PD-soma (dends toward ND)\n"
        "PD axis is horizontal (+x); bar moves toward soma in PD direction",
        fontsize=13,
        y=1.0,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.98))
    out: Path = OUT_DIR / "top50_morphologies.png"
    fig.savefig(out, dpi=110, bbox_inches="tight")
    plt.close(fig)
    print(f"[plot] wrote {out}")


def plot_pareto_front(*, evals: list[dict[str, Any]]) -> None:
    gens = np.array([e["generation"] for e in evals])
    dsi = np.array([e["dsi_vector_sum"] for e in evals])
    pd = np.array([e["pd_rate_hz"] for e in evals])

    fig, ax = plt.subplots(figsize=(10, 7), dpi=120)
    sc = ax.scatter(pd, dsi, c=gens, cmap="viridis", s=15, alpha=0.6, edgecolors="none")
    cb = fig.colorbar(sc, ax=ax)
    cb.set_label("Generation", fontsize=11)
    # Joint-pass corner
    ax.axhline(0.5, linestyle="--", color="red", linewidth=1, alpha=0.6, label="DSI = 0.5")
    ax.axvline(30, linestyle="--", color="red", linewidth=1, alpha=0.6, label="PD = 30 Hz")
    # Pareto front: take the non-dominated set
    pts = np.column_stack([pd, dsi])
    is_pareto = np.ones(len(pts), dtype=bool)
    for i, p in enumerate(pts):
        if is_pareto[i]:
            # dominated if any other point has greater or equal in both AND strictly greater in one
            dom = (pts[:, 0] >= p[0]) & (pts[:, 1] >= p[1])
            dom[i] = False
            strict = (pts[:, 0] > p[0]) | (pts[:, 1] > p[1])
            is_pareto[i] = not np.any(dom & strict)
    pf = pts[is_pareto]
    pf = pf[np.argsort(pf[:, 0])]
    ax.plot(
        pf[:, 0],
        pf[:, 1],
        "-",
        color="black",
        linewidth=1.5,
        label=f"Pareto front ({len(pf)} cells)",
    )
    ax.set_xlabel("PD firing rate (Hz)", fontsize=12)
    ax.set_ylabel("Ratio DSI = (PD - ND) / (PD + ND)", fontsize=12)
    ax.set_title(
        f"t0106 Pareto front: {len(evals)} evaluations, seed 44\n"
        f"Joint-pass corner: DSI >= 0.5 AND PD >= 30 Hz (red dashed)",
        fontsize=13,
    )
    ax.set_xlim(0, max(pd.max() * 1.05, 130))
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out: Path = OUT_DIR / "pareto_front.png"
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"[plot] wrote {out}")


def plot_hv_trajectory() -> None:
    raw_lines = HV_TRACE_PATH.read_text().strip().splitlines()
    recs = [json.loads(line) for line in raw_lines]
    gens = np.array([r["gen"] for r in recs])
    hvs = np.array([r["hv"] for r in recs])
    wall_h = np.array([r["wall_clock_s"] / 3600 for r in recs])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), dpi=120, sharex=True)
    ax1.plot(gens, hvs, "-o", color="#1f77b4", markersize=4, linewidth=1.3)
    ax1.set_ylabel("Hypervolume", fontsize=12)
    ax1.set_yscale("log")
    ax1.grid(alpha=0.3)
    ax1.set_title(
        f"t0106 HV trajectory — {len(recs)} generations, final HV = {hvs[-1]:.2f}", fontsize=13
    )
    # Annotate breakthrough gens (jumps > 50%)
    for i in range(1, len(recs)):
        if hvs[i] > hvs[i - 1] * 1.5:
            ax1.annotate(
                f"g{recs[i]['gen']}: +{((hvs[i] - hvs[i - 1]) / hvs[i - 1] * 100):.0f}%",
                xy=(gens[i], hvs[i]),
                xytext=(5, 8),
                textcoords="offset points",
                fontsize=8,
                color="darkred",
            )
    # Mark pool restart at gen 26
    if len(gens) > 26:
        ax1.axvline(26, linestyle="--", color="green", alpha=0.6, linewidth=1)
        ax1.text(26.3, hvs.max() * 0.5, "Pool restart\n(gen 26)", fontsize=9, color="green")

    # Per-gen wall-clock
    dt_min = np.diff(np.concatenate([[0], wall_h])) * 60
    ax2.plot(gens, dt_min, "-o", color="#d62728", markersize=4, linewidth=1.3)
    ax2.set_ylabel("Generation wall-clock (min)", fontsize=12)
    ax2.set_xlabel("Generation", fontsize=12)
    ax2.grid(alpha=0.3)
    if len(gens) > 26:
        ax2.axvline(26, linestyle="--", color="green", alpha=0.6, linewidth=1)
    fig.tight_layout()
    out: Path = OUT_DIR / "hv_vs_gen.png"
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"[plot] wrote {out}")


def plot_asymmetry_distribution(*, top50: list[CellRecord], evals: list[dict[str, Any]]) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), dpi=120)
    all_soma = np.array([e["vector_68d"][59] for e in evals])
    all_elong = np.array([e["vector_68d"][60] for e in evals])
    all_brgrad = np.array([e["vector_68d"][61] for e in evals])
    all_brconc = np.array([e["vector_68d"][62] for e in evals])

    top_soma = np.array([c.vector_68d[59] for c in top50])
    top_elong = np.array([c.vector_68d[60] for c in top50])
    top_brgrad = np.array([c.vector_68d[61] for c in top50])
    top_brconc = np.array([c.vector_68d[62] for c in top50])

    bins_soma = np.linspace(-150, 150, 21)
    bins_elong = np.linspace(1, 3, 21)
    bins_brgrad = np.linspace(-1, 1, 21)
    bins_brconc = np.linspace(0, 5, 21)

    axes[0, 0].hist(
        [all_soma, top_soma],
        bins=bins_soma,
        color=["lightgray", "#1f77b4"],
        label=["all evals", "top 50"],
        stacked=False,
        density=True,
    )
    axes[0, 0].set_title("Soma offset (PD axis), um", fontsize=11)
    axes[0, 0].axvline(0, linestyle="--", color="black", alpha=0.5)
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].set_xlabel("um")
    axes[0, 0].grid(alpha=0.3)

    axes[0, 1].hist(
        [all_elong, top_elong],
        bins=bins_elong,
        color=["lightgray", "#1f77b4"],
        label=["all evals", "top 50"],
        stacked=False,
        density=True,
    )
    axes[0, 1].set_title("Field elongation along PD axis", fontsize=11)
    axes[0, 1].axvline(1, linestyle="--", color="black", alpha=0.5)
    axes[0, 1].legend(fontsize=9)
    axes[0, 1].grid(alpha=0.3)

    axes[1, 0].hist(
        [all_brgrad, top_brgrad],
        bins=bins_brgrad,
        color=["lightgray", "#1f77b4"],
        label=["all evals", "top 50"],
        stacked=False,
        density=True,
    )
    axes[1, 0].set_title("Branch density gradient PD", fontsize=11)
    axes[1, 0].axvline(0, linestyle="--", color="black", alpha=0.5)
    axes[1, 0].legend(fontsize=9)
    axes[1, 0].grid(alpha=0.3)

    axes[1, 1].hist(
        [all_brconc, top_brconc],
        bins=bins_brconc,
        color=["lightgray", "#1f77b4"],
        label=["all evals", "top 50"],
        stacked=False,
        density=True,
    )
    axes[1, 1].set_title("Primary branch PD concentration", fontsize=11)
    axes[1, 1].legend(fontsize=9)
    axes[1, 1].grid(alpha=0.3)

    fig.suptitle(
        "t0106 asymmetry parameter distributions — all evals (gray) vs top-50 (blue)",
        fontsize=13,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    out: Path = OUT_DIR / "asymmetry_distribution.png"
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"[plot] wrote {out}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = json.loads(EVALS_PATH.read_text())
    evals: list[dict[str, Any]] = data["evaluations"]
    n_gen = max(e["generation"] for e in evals) + 1
    print(f"Loaded {len(evals)} evaluations across {n_gen} generations")
    top50 = _load_top_n(evals=evals, n=50)
    best_pd = max(c.pd_rate_hz for c in top50)
    print(f"Top 50 picked. Best DSI = {top50[0].dsi:.4f}, best PD = {best_pd:.2f} Hz")
    plot_pareto_front(evals=evals)
    plot_hv_trajectory()
    plot_asymmetry_distribution(top50=top50, evals=evals)
    plot_top50_morphologies(top50=top50)


if __name__ == "__main__":
    main()
