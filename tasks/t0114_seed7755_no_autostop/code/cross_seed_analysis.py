"""Phase D: cross-seed comparison.

Produces:

* `cross_seed_summary.json` — per-seed Pareto sizes, strict joint-pass counts,
  bio-plausibility verdict counts, anchor distribution.
* `anchor_distribution_table.json` — 5x4 table (5 anchors x 4 columns: 3 t0099
  seeds + t0091 reference).
* `images/hv_trajectory_cross_seed.png` — 4 lines (3 seeds + t0091).
* `images/anchor_distribution_heatmap.png` — 5x4 heatmap.
* `images/pareto_overlay_dsi_pdrate_robust.png` — 3 scatter panels (DSI-vs-PD,
  DSI-vs-robust, PD-vs-robust) overlaying t0099 seeds + t0091.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from tasks.t0114_seed7755_no_autostop.code.constants import (
    ANCHOR_NAMES,
    N_ANCHORS,
    T0104_SEEDS,
)
from tasks.t0114_seed7755_no_autostop.code.paths import (
    ANCHOR_DISTRIBUTION_TABLE_JSON,
    ANCHOR_HEATMAP_PNG,
    CROSS_SEED_SUMMARY_JSON,
    HV_TRAJECTORY_CROSS_SEED_PNG,
    PARETO_OVERLAY_PNG,
    T0091_ANCHOR_TRACKING_JSON,
    T0091_BIOLOGICAL_SCORECARD_JSON,
    T0091_HV_TRAJECTORY_JSON,
    T0091_PARETO_FRONT_JSON,
    anchor_tracking_json,
    biological_scorecard_json,
    ensure_directories,
    hv_trajectory_json,
    pareto_front_json,
)
from tasks.t0114_seed7755_no_autostop.code.per_seed_analysis import (
    strict_joint_pass_count_for_seed,
)

T0091_LABEL: str = "t0091 (warm-start)"


@dataclass(frozen=True, slots=True)
class SeedSummary:
    seed: int
    n_pareto_cells: int
    n_strict_joint_pass: int
    n_plausible: int
    n_stretched: int
    n_exotic: int
    counts_per_anchor: tuple[int, ...]


def _load_json(*, path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _summarise_seed(*, seed: int) -> SeedSummary:
    pareto = _load_json(path=pareto_front_json(seed=seed))
    bio = _load_json(path=biological_scorecard_json(seed=seed))
    anchor = _load_json(path=anchor_tracking_json(seed=seed))
    n_pareto = int(pareto["n_total"]) if pareto is not None else 0
    n_plausible = 0
    n_stretched = 0
    n_exotic = 0
    if bio is not None:
        for cell in bio["cells"]:
            v = str(cell.get("verdict", ""))
            if v == "plausible":
                n_plausible += 1
            elif v == "stretched":
                n_stretched += 1
            elif v == "exotic":
                n_exotic += 1
    counts_list: list[int] = (
        list(anchor["counts_per_anchor"]) if anchor is not None else [0] * N_ANCHORS
    )
    while len(counts_list) < N_ANCHORS:
        counts_list.append(0)
    strict = strict_joint_pass_count_for_seed(seed=seed)
    return SeedSummary(
        seed=seed,
        n_pareto_cells=n_pareto,
        n_strict_joint_pass=int(strict["n_strict_joint_pass"]),
        n_plausible=n_plausible,
        n_stretched=n_stretched,
        n_exotic=n_exotic,
        counts_per_anchor=tuple(int(c) for c in counts_list[:N_ANCHORS]),
    )


def _summarise_t0091() -> SeedSummary | None:
    pareto = _load_json(path=T0091_PARETO_FRONT_JSON)
    bio = _load_json(path=T0091_BIOLOGICAL_SCORECARD_JSON)
    anchor = _load_json(path=T0091_ANCHOR_TRACKING_JSON)
    if pareto is None:
        return None
    n_pareto = int(pareto.get("n_total", 0))
    n_plausible = 0
    n_stretched = 0
    n_exotic = 0
    if bio is not None:
        for cell in bio["cells"]:
            v = str(cell.get("verdict", ""))
            if v == "plausible":
                n_plausible += 1
            elif v == "stretched":
                n_stretched += 1
            elif v == "exotic":
                n_exotic += 1
    n_strict_pass = 0
    cells = pareto.get("cells", [])
    for c in cells:
        if (
            float(c.get("dsi_vector_sum", 0.0)) >= 0.5
            and float(c.get("pd_rate_hz", 0.0)) >= 30.0
            and float(c.get("robustness", 0.0)) >= 0.7
        ):
            n_strict_pass += 1
    counts_list_91: list[int] = (
        list(anchor["counts_per_anchor"]) if anchor is not None else [0] * N_ANCHORS
    )
    while len(counts_list_91) < N_ANCHORS:
        counts_list_91.append(0)
    return SeedSummary(
        seed=-1,
        n_pareto_cells=n_pareto,
        n_strict_joint_pass=n_strict_pass,
        n_plausible=n_plausible,
        n_stretched=n_stretched,
        n_exotic=n_exotic,
        counts_per_anchor=tuple(int(c) for c in counts_list_91[:N_ANCHORS]),
    )


def _plot_hv_trajectories(*, seed_summaries: list[SeedSummary]) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    colours = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    for i, s in enumerate(seed_summaries):
        traj = _load_json(path=hv_trajectory_json(seed=s.seed))
        if traj is None:
            continue
        gens = [int(t["generation"]) for t in traj["trajectory"]]
        hvs = [float(t["hypervolume"]) for t in traj["trajectory"]]
        ax.plot(gens, hvs, marker="o", color=colours[i % len(colours)], label=f"seed {s.seed}")
    t0091_traj = _load_json(path=T0091_HV_TRAJECTORY_JSON)
    if t0091_traj is not None:
        gens91 = [int(t["generation"]) for t in t0091_traj["trajectory"]]
        hvs91 = [float(t["hypervolume"]) for t in t0091_traj["trajectory"]]
        ax.plot(gens91, hvs91, marker="x", linestyle="--", color="black", label=T0091_LABEL)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Hypervolume")
    ax.set_title("HV trajectory: 3 random-init seeds vs t0091 warm-start")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(HV_TRAJECTORY_CROSS_SEED_PNG, dpi=200)
    plt.close(fig)
    print(f"[cross_seed_analysis] wrote {HV_TRAJECTORY_CROSS_SEED_PNG}")


def _plot_anchor_heatmap(
    *,
    seed_summaries: list[SeedSummary],
    t0091_summary: SeedSummary | None,
) -> None:
    columns: list[str] = [f"seed{s.seed}" for s in seed_summaries]
    data_cols: list[NDArray[np.int64]] = [
        np.array(s.counts_per_anchor, dtype=np.int64) for s in seed_summaries
    ]
    if t0091_summary is not None:
        columns.append("t0091")
        data_cols.append(np.array(t0091_summary.counts_per_anchor, dtype=np.int64))
    if len(columns) == 0:
        print("[cross_seed_analysis] no anchor data; skipping heatmap")
        return
    matrix = np.stack(data_cols, axis=1)  # (5, n_cols)

    fig, ax = plt.subplots(figsize=(max(4, 1.3 * len(columns)), 4))
    im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(columns)))
    ax.set_xticklabels(columns)
    ax.set_yticks(range(N_ANCHORS))
    ax.set_yticklabels(list(ANCHOR_NAMES))
    for i in range(N_ANCHORS):
        for j, _ in enumerate(columns):
            ax.text(
                j,
                i,
                int(matrix[i, j]),
                ha="center",
                va="center",
                color="black",
                fontsize=10,
            )
    ax.set_title("Anchor distribution: random-init seeds vs t0091 warm-start")
    fig.colorbar(im, ax=ax, label="# Pareto cells")
    fig.tight_layout()
    fig.savefig(ANCHOR_HEATMAP_PNG, dpi=200)
    plt.close(fig)
    print(f"[cross_seed_analysis] wrote {ANCHOR_HEATMAP_PNG}")


def _plot_pareto_overlay() -> None:
    """3-panel overlay scatter: (DSI vs PD), (DSI vs robust), (PD vs robust)."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    colours = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    seeds_data: list[tuple[int, list[float], list[float], list[float]]] = []
    for i, seed in enumerate(T0104_SEEDS):
        p = _load_json(path=pareto_front_json(seed=seed))
        if p is None:
            continue
        dsis: list[float] = []
        pds: list[float] = []
        robs: list[float] = []
        for c in p["cells"]:
            dsis.append(float(c.get("dsi_vector_sum", 0.0)))
            pds.append(float(c.get("pd_rate_hz", 0.0)))
            robs.append(float(c.get("robustness", 0.0)))
        seeds_data.append((seed, dsis, pds, robs))
        axes[0].scatter(dsis, pds, color=colours[i % 3], alpha=0.7, label=f"seed {seed}")
        axes[1].scatter(dsis, robs, color=colours[i % 3], alpha=0.7, label=f"seed {seed}")
        axes[2].scatter(pds, robs, color=colours[i % 3], alpha=0.7, label=f"seed {seed}")
    p91 = _load_json(path=T0091_PARETO_FRONT_JSON)
    if p91 is not None:
        d91 = [float(c.get("dsi_vector_sum", 0.0)) for c in p91["cells"]]
        pd91 = [float(c.get("pd_rate_hz", 0.0)) for c in p91["cells"]]
        r91 = [float(c.get("robustness", 0.0)) for c in p91["cells"]]
        axes[0].scatter(d91, pd91, color="black", marker="x", alpha=0.5, label=T0091_LABEL)
        axes[1].scatter(d91, r91, color="black", marker="x", alpha=0.5, label=T0091_LABEL)
        axes[2].scatter(pd91, r91, color="black", marker="x", alpha=0.5, label=T0091_LABEL)
    axes[0].set_xlabel("DSI vector-sum")
    axes[0].set_ylabel("PD-rate (Hz)")
    axes[1].set_xlabel("DSI vector-sum")
    axes[1].set_ylabel("Robustness")
    axes[2].set_xlabel("PD-rate (Hz)")
    axes[2].set_ylabel("Robustness")
    for ax in axes:
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle("Pareto overlay: random-init seeds vs t0091 warm-start")
    fig.tight_layout()
    fig.savefig(PARETO_OVERLAY_PNG, dpi=200)
    plt.close(fig)
    print(f"[cross_seed_analysis] wrote {PARETO_OVERLAY_PNG}")


def _summary_to_dict(*, summary: SeedSummary) -> dict[str, object]:
    return {
        "seed": summary.seed,
        "n_pareto_cells": summary.n_pareto_cells,
        "n_strict_joint_pass": summary.n_strict_joint_pass,
        "n_plausible": summary.n_plausible,
        "n_stretched": summary.n_stretched,
        "n_exotic": summary.n_exotic,
        "counts_per_anchor": list(summary.counts_per_anchor),
    }


def main() -> dict[str, object]:
    ensure_directories()
    seed_summaries: list[SeedSummary] = []
    for seed in T0104_SEEDS:
        if pareto_front_json(seed=seed).exists():
            seed_summaries.append(_summarise_seed(seed=int(seed)))
    t0091_summary = _summarise_t0091()

    out: dict[str, object] = {
        "t0099_seeds": list(T0104_SEEDS),
        "anchor_names": list(ANCHOR_NAMES),
        "per_seed": [_summary_to_dict(summary=s) for s in seed_summaries],
        "t0091_reference": _summary_to_dict(summary=t0091_summary)
        if t0091_summary is not None
        else None,
        "t0091_label": T0091_LABEL,
    }
    CROSS_SEED_SUMMARY_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[cross_seed_analysis] wrote {CROSS_SEED_SUMMARY_JSON}")

    # Anchor distribution table.
    columns: list[dict[str, object]] = []
    for s in seed_summaries:
        columns.append({"label": f"seed{s.seed}", "counts": list(s.counts_per_anchor)})
    if t0091_summary is not None:
        columns.append({"label": "t0091", "counts": list(t0091_summary.counts_per_anchor)})
    ANCHOR_DISTRIBUTION_TABLE_JSON.write_text(
        json.dumps(
            {"anchor_names": list(ANCHOR_NAMES), "columns": columns},
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[cross_seed_analysis] wrote {ANCHOR_DISTRIBUTION_TABLE_JSON}")

    _plot_hv_trajectories(seed_summaries=seed_summaries)
    _plot_anchor_heatmap(seed_summaries=seed_summaries, t0091_summary=t0091_summary)
    _plot_pareto_overlay()
    return out


if __name__ == "__main__":
    main()
