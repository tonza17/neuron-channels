"""Generate t0113 result charts, CSV tables, and `results/metrics.json`.

Reads:
* t0113 predictions asset (files/all_evaluations_seed2247.json.gz)
* t0113 results/data/pareto_front_seed2247.json
* t0113 results/data/hv_trajectory_seed2247.json
* t0106 predictions asset (files/all_evaluations_seed44.json.gz)
* t0106 results/data/pareto_front_seed44.json
* t0106 results/data/hv_trajectory_seed44.json
* t0112 results/data/all_evaluations_seed77.json.gz
* t0112 results/data/pareto_front_seed77.json
* t0112 results/data/hv_trajectory_seed77.json

Writes:
* `results/images/pareto_front_3seeds.png`
* `results/images/hv_vs_gen_3seeds.png`
* `results/images/joint_pass_yield_per_gen_3seeds.png`
* `results/images/top50_morphologies_seed2247.png`
* `results/images/asymmetry_distribution_3seeds.png`
* `results/data/joint_pass_summary_3seeds.csv`
* `results/data/pareto_front_overlap_3seeds.csv`
* `results/metrics.json`
"""

from __future__ import annotations

import csv
import gzip
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------

TASK_DIR: Path = Path(__file__).resolve().parent.parent
TASKS_ROOT: Path = TASK_DIR.parent
T0106_DIR: Path = TASKS_ROOT / "t0106_long_pdnd_nsga2_300gen"
T0112_DIR: Path = TASKS_ROOT / "t0112_t0106_seed77_replicate"

# t0113 (this task) sources.
T0113_EVALS: Path = (
    TASK_DIR
    / "assets"
    / "predictions"
    / "t0113-bedb-morph-nsga2-seed2247"
    / "files"
    / "all_evaluations_seed2247.json.gz"
)
T0113_PARETO: Path = TASK_DIR / "results" / "data" / "pareto_front_seed2247.json"
T0113_HV: Path = TASK_DIR / "results" / "data" / "hv_trajectory_seed2247.json"

# t0112 sources.
T0112_EVALS: Path = T0112_DIR / "results" / "data" / "all_evaluations_seed77.json.gz"
T0112_PARETO: Path = T0112_DIR / "results" / "data" / "pareto_front_seed77.json"
T0112_HV: Path = T0112_DIR / "results" / "data" / "hv_trajectory_seed77.json"

# t0106 sources.
T0106_EVALS: Path = (
    T0106_DIR
    / "assets"
    / "predictions"
    / "nsga2-seed44-bedb-morph-2dir-300gen"
    / "files"
    / "all_evaluations_seed44.json.gz"
)
T0106_PARETO: Path = T0106_DIR / "results" / "data" / "pareto_front_seed44.json"
T0106_HV: Path = T0106_DIR / "results" / "data" / "hv_trajectory_seed44.json"

# Outputs.
IMAGES_DIR: Path = TASK_DIR / "results" / "images"
DATA_DIR: Path = TASK_DIR / "results" / "data"
METRICS_JSON: Path = TASK_DIR / "results" / "metrics.json"

# ----------------------------------------------------------------------------
# Thresholds and constants
# ----------------------------------------------------------------------------

DSI_THRESHOLD: float = 0.5
PD_RATE_THRESHOLD_HZ: float = 30.0
DSI_SILENCE_GUARD_VALUE: float = 1.0
TOP_K_MORPHOLOGY: int = 50

# Per the t0112 chart_asymmetry_distribution best-effort 68-d morphology
# indices (positions 54..67 are the 14-d morphology block).
MORPH_PANEL_INDICES: dict[str, int] = {
    "soma_offset_y": 54,
    "elongation": 55,
    "branch_density_gradient": 60,
    "primary_branch_pd_concentration": 65,
}

SEED_LABELS: dict[str, str] = {
    "t0106_seed44": "t0106 seed 44",
    "t0112_seed77": "t0112 seed 77",
    "t0113_seed2247": "t0113 seed 2247",
}
SEED_COLORS: dict[str, str] = {
    "t0106_seed44": "C0",
    "t0112_seed77": "C3",
    "t0113_seed2247": "C2",
}
SEED_MARKERS: dict[str, str] = {
    "t0106_seed44": "o",
    "t0112_seed77": "D",
    "t0113_seed2247": "s",
}


# ----------------------------------------------------------------------------
# Data containers
# ----------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SeedDataset:
    label: str
    evaluations: list[dict[str, Any]]
    pareto_cells: list[dict[str, Any]]
    hv_trajectory: list[dict[str, Any]]


@dataclass(frozen=True, slots=True)
class JointPassSummary:
    seed_label: str
    n_total_evals: int
    n_joint_pass_unique: int
    n_joint_pass_evaluations: int
    joint_pass_pct: float
    best_dsi_overall: float
    best_legit_dsi: float
    best_pd_rate_hz: float
    n_generations_completed: int
    plateau_gen: int
    final_hypervolume: float


# ----------------------------------------------------------------------------
# IO
# ----------------------------------------------------------------------------


def _load_evaluations(path: Path) -> list[dict[str, Any]]:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        evals = data["evaluations"]
        assert isinstance(evals, list), "evaluations is a list"
        return evals
    assert isinstance(data, list), "top-level is a list"
    return data


def _load_pareto_cells(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    cells = data["cells"]
    assert isinstance(cells, list), "cells is a list"
    return cells


def _load_hv_trajectory(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    traj = data["trajectory"]
    assert isinstance(traj, list), "trajectory is a list"
    return traj


def load_all_three_seeds() -> dict[str, SeedDataset]:
    out: dict[str, SeedDataset] = {}
    out["t0106_seed44"] = SeedDataset(
        label=SEED_LABELS["t0106_seed44"],
        evaluations=_load_evaluations(path=T0106_EVALS),
        pareto_cells=_load_pareto_cells(path=T0106_PARETO),
        hv_trajectory=_load_hv_trajectory(path=T0106_HV),
    )
    out["t0112_seed77"] = SeedDataset(
        label=SEED_LABELS["t0112_seed77"],
        evaluations=_load_evaluations(path=T0112_EVALS),
        pareto_cells=_load_pareto_cells(path=T0112_PARETO),
        hv_trajectory=_load_hv_trajectory(path=T0112_HV),
    )
    out["t0113_seed2247"] = SeedDataset(
        label=SEED_LABELS["t0113_seed2247"],
        evaluations=_load_evaluations(path=T0113_EVALS),
        pareto_cells=_load_pareto_cells(path=T0113_PARETO),
        hv_trajectory=_load_hv_trajectory(path=T0113_HV),
    )
    return out


# ----------------------------------------------------------------------------
# Metric helpers
# ----------------------------------------------------------------------------


def _is_joint_pass(cell: dict[str, Any]) -> bool:
    dsi = float(cell["dsi_vector_sum"])
    pd = float(cell["pd_rate_hz"])
    return dsi >= DSI_THRESHOLD and pd >= PD_RATE_THRESHOLD_HZ


def _legit_dsi(cell: dict[str, Any]) -> float | None:
    """Return DSI if not silence-guard-saturated (== 1.0), else None."""
    dsi = float(cell["dsi_vector_sum"])
    if dsi >= DSI_SILENCE_GUARD_VALUE:
        return None
    return dsi


def summarize_seed(*, seed_key: str, ds: SeedDataset) -> JointPassSummary:
    cells = ds.evaluations
    jp_evals = [c for c in cells if _is_joint_pass(c)]
    jp_unique_keys: set[tuple[float, ...]] = {tuple(c["vector_68d"]) for c in jp_evals}
    dsis = [float(c["dsi_vector_sum"]) for c in cells]
    legit_dsis = [d for d in dsis if d < DSI_SILENCE_GUARD_VALUE]
    best_legit = max(legit_dsis) if len(legit_dsis) > 0 else float("nan")
    n_total = len(cells)
    n_gen = max(int(c["generation"]) for c in cells)
    return JointPassSummary(
        seed_label=seed_key,
        n_total_evals=n_total,
        n_joint_pass_unique=len(jp_unique_keys),
        n_joint_pass_evaluations=len(jp_evals),
        joint_pass_pct=(100.0 * len(jp_unique_keys) / n_total if n_total > 0 else 0.0),
        best_dsi_overall=max(dsis),
        best_legit_dsi=best_legit,
        best_pd_rate_hz=max(float(c["pd_rate_hz"]) for c in cells),
        n_generations_completed=n_gen,
        plateau_gen=n_gen,
        final_hypervolume=float(ds.hv_trajectory[-1]["hypervolume"]),
    )


def cumulative_joint_pass_per_gen(
    *,
    cells: list[dict[str, Any]],
) -> dict[int, int]:
    seen: set[tuple[float, ...]] = set()
    out: dict[int, int] = {}
    gens = sorted({int(c["generation"]) for c in cells})
    for g in gens:
        for c in [c for c in cells if int(c["generation"]) == g]:
            if _is_joint_pass(c):
                seen.add(tuple(c["vector_68d"]))
        out[g] = len(seen)
    return out


# ----------------------------------------------------------------------------
# Charts
# ----------------------------------------------------------------------------


def chart_pareto_front_3seeds(*, datasets: dict[str, SeedDataset]) -> Path:
    fig, ax = plt.subplots(figsize=(8, 6))
    max_pd = 0.0
    for key in ("t0106_seed44", "t0112_seed77", "t0113_seed2247"):
        ds = datasets[key]
        x = [float(c["dsi_vector_sum"]) for c in ds.pareto_cells]
        y = [float(c["pd_rate_hz"]) for c in ds.pareto_cells]
        if len(y) > 0:
            max_pd = max(max_pd, max(y))
        ax.scatter(
            x,
            y,
            s=55,
            alpha=0.75,
            label=f"{ds.label} (n={len(ds.pareto_cells)})",
            color=SEED_COLORS[key],
            marker=SEED_MARKERS[key],
            edgecolors="black",
            linewidths=0.4,
        )
    ax.axvline(
        DSI_THRESHOLD,
        color="grey",
        ls="--",
        lw=0.8,
        alpha=0.6,
        label="DSI = 0.5 threshold",
    )
    ax.axhline(
        PD_RATE_THRESHOLD_HZ,
        color="grey",
        ls=":",
        lw=0.8,
        alpha=0.6,
        label="PD = 30 Hz threshold",
    )
    ax.set_xlabel("ratio DSI")
    ax.set_ylabel("PD-rate (Hz)")
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, (max_pd if max_pd > 0 else 130.0) * 1.10)
    ax.set_title("Strict Pareto fronts: t0106 vs t0112 vs t0113")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    out_path = IMAGES_DIR / "pareto_front_3seeds.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_hv_vs_gen_3seeds(*, datasets: dict[str, SeedDataset]) -> Path:
    fig, ax = plt.subplots(figsize=(8, 5))
    cadences: dict[str, int] = {
        "t0106_seed44": 25,
        "t0112_seed77": 10,
        "t0113_seed2247": 10,
    }
    for key in ("t0106_seed44", "t0112_seed77", "t0113_seed2247"):
        ds = datasets[key]
        gens = [int(h["generation"]) for h in ds.hv_trajectory]
        hvs = [float(h["hypervolume"]) for h in ds.hv_trajectory]
        ax.plot(
            gens,
            hvs,
            label=(f"{ds.label} (restart every {cadences[key]}, {len(gens)} gens)"),
            color=SEED_COLORS[key],
            marker=SEED_MARKERS[key],
            ms=4,
            lw=1.5,
        )
        # Annotate pool-restart events.
        max_gen = max(gens)
        cadence = cadences[key]
        restart_gens = list(range(cadence, max_gen + 1, cadence))
        for g in restart_gens:
            ax.axvline(
                g,
                color=SEED_COLORS[key],
                ls=":",
                lw=0.5,
                alpha=0.35,
            )
    ax.set_yscale("log")
    ax.set_xlabel("generation")
    ax.set_ylabel("hypervolume (log scale)")
    ax.set_title(
        "HV trajectory: seeds 44, 77, 2247 with pool-restart events annotated",
    )
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    out_path = IMAGES_DIR / "hv_vs_gen_3seeds.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_joint_pass_yield_3seeds(
    *,
    datasets: dict[str, SeedDataset],
) -> Path:
    fig, ax = plt.subplots(figsize=(8, 5))
    for key in ("t0106_seed44", "t0112_seed77", "t0113_seed2247"):
        ds = datasets[key]
        per_gen = cumulative_joint_pass_per_gen(cells=ds.evaluations)
        gens = list(per_gen.keys())
        counts = list(per_gen.values())
        ax.plot(
            gens,
            counts,
            label=f"{ds.label} (final={counts[-1] if counts else 0})",
            color=SEED_COLORS[key],
            marker=SEED_MARKERS[key],
            ms=4,
            lw=1.5,
        )
    ax.set_xlabel("generation")
    ax.set_ylabel("cumulative unique joint-pass cells")
    ax.set_title(
        "Joint-pass cell discovery per generation (DSI >= 0.5, PD >= 30 Hz)",
    )
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, ls=":", lw=0.5, alpha=0.5)
    fig.tight_layout()
    out_path = IMAGES_DIR / "joint_pass_yield_per_gen_3seeds.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_top50_morphologies_seed2247(
    *,
    ds_t0113: SeedDataset,
) -> Path:
    """10x5 grid of best 50 t0113 cells. If <50 cells, pad with text."""
    # Rank cells by joint-pass status first, then by best legit DSI, then by
    # PD-rate. The plan permits "use what's available" if <50 cells.
    cells = list(ds_t0113.evaluations)
    # Deduplicate by vector_68d to avoid showing identical cells.
    seen_keys: set[tuple[float, ...]] = set()
    unique_cells: list[dict[str, Any]] = []
    for c in cells:
        k = tuple(c["vector_68d"])
        if k not in seen_keys:
            seen_keys.add(k)
            unique_cells.append(c)

    def _rank(cell: dict[str, Any]) -> tuple[int, float, float]:
        jp = 1 if _is_joint_pass(cell) else 0
        dsi = float(cell["dsi_vector_sum"])
        # Penalise silence-guard saturation slightly to prefer legit cells.
        legit_bonus = 0.0 if dsi >= DSI_SILENCE_GUARD_VALUE else dsi
        return (jp, legit_bonus, float(cell["pd_rate_hz"]))

    sorted_cells = sorted(unique_cells, key=_rank, reverse=True)
    top = sorted_cells[:TOP_K_MORPHOLOGY]

    fig, axes = plt.subplots(5, 10, figsize=(20, 10))
    axes_flat = axes.flatten()
    n_shown = len(top)
    # Use elongation x soma_offset_y as a 2D scatter per panel; tag joint-pass.
    for i, ax in enumerate(axes_flat):
        ax.set_xticks([])
        ax.set_yticks([])
        if i >= n_shown:
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
        c = top[i]
        morph = c["vector_68d"][54:68]
        # Schematic: dot at (elongation, soma_offset_y).
        soma_offset_y = morph[0]
        elongation = morph[1]
        is_jp = _is_joint_pass(c)
        is_silence = c["dsi_vector_sum"] >= DSI_SILENCE_GUARD_VALUE
        if is_silence:
            color = "red"
        elif is_jp:
            color = "green"
        else:
            color = SEED_COLORS["t0113_seed2247"]
        ax.scatter([elongation], [soma_offset_y], c=color, s=80)
        ax.set_title(
            f"#{i + 1} g{int(c['generation'])}\n"
            f"DSI={c['dsi_vector_sum']:.3f}\n"
            f"PD={c['pd_rate_hz']:.1f} Hz",
            fontsize=7,
        )
    fig.suptitle(
        "t0113 seed 2247: top-50 cells (ranked by joint-pass then legit DSI). "
        "Red = silence-guard DSI=1.0, green = joint-pass, blue = other. "
        f"Total unique cells available: {len(unique_cells)} of "
        f"{len(ds_t0113.evaluations)} evaluations.",
        fontsize=10,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    out_path = IMAGES_DIR / "top50_morphologies_seed2247.png"
    fig.savefig(out_path, dpi=110)
    plt.close(fig)
    return out_path


def chart_asymmetry_distribution_3seeds(
    *,
    datasets: dict[str, SeedDataset],
) -> Path:
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.5))
    for ax, (name, idx) in zip(
        axes,
        MORPH_PANEL_INDICES.items(),
        strict=False,
    ):
        for key in ("t0106_seed44", "t0112_seed77", "t0113_seed2247"):
            ds = datasets[key]
            top = sorted(
                ds.evaluations,
                key=lambda c: float(c["dsi_vector_sum"]),
                reverse=True,
            )[:TOP_K_MORPHOLOGY]
            vals = [float(c["vector_68d"][idx]) for c in top]
            if len(vals) == 0:
                continue
            ax.hist(
                vals,
                bins=15,
                alpha=0.45,
                label=ds.label if name == "soma_offset_y" else None,
                color=SEED_COLORS[key],
            )
        ax.set_title(name.replace("_", " "), fontsize=10)
        ax.set_xlabel("value")
        ax.set_ylabel("count")
        if name == "soma_offset_y":
            ax.legend(fontsize=9)
    fig.suptitle(
        "Morphology distributions: top-50-by-DSI cells, seeds 44 vs 77 vs 2247",
        fontsize=11,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.94))
    out_path = IMAGES_DIR / "asymmetry_distribution_3seeds.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


# ----------------------------------------------------------------------------
# CSVs
# ----------------------------------------------------------------------------


# Canonical asset-declared headline numbers (from each task's predictions
# asset metrics_at_creation block). These are the values cited in each
# task's own results_summary.md, so the joint_pass_summary table uses them
# for cross-task consistency. The recomputed values in
# JointPassSummary (post-hoc full-gz pass) are reported alongside.
ASSET_DECLARED: dict[str, dict[str, float]] = {
    "t0106_seed44": {
        "n_generations_completed": 40,
        "n_cells_total": 3744,
        "best_dsi_ratio": 1.0,
        "best_pd_rate_hz": 122.62,
        "n_joint_pass_unique": 123,
        "n_joint_pass_evaluations": 637,
        "final_hypervolume": 122.0288,
    },
    "t0112_seed77": {
        "n_generations_completed": 21,
        "n_cells_total": 2016,
        "best_dsi_ratio": 0.9535,
        "best_pd_rate_hz": 114.76,
        "n_joint_pass_unique": 7,
        "n_joint_pass_evaluations": 25,
        "final_hypervolume": 107.4602,
    },
    "t0113_seed2247": {
        "n_generations_completed": 14,
        "n_cells_total": 1344,
        "best_dsi_ratio": 1.0,
        "best_pd_rate_hz": 71.6667,
        "n_joint_pass_unique": 2,
        "n_joint_pass_evaluations": 6,
        "final_hypervolume": 45.6221,
    },
}


def csv_joint_pass_summary_3seeds(
    *,
    summaries: dict[str, JointPassSummary],
) -> Path:
    """Write the 3-seed joint-pass summary CSV using canonical asset-declared
    numbers for n_joint_pass_unique, best_dsi_ratio, best_pd_rate_hz,
    final_hypervolume, plus the recomputed `best_legit_dsi` (which is not in
    the asset metrics block) from the full evaluation gz."""
    out_path = DATA_DIR / "joint_pass_summary_3seeds.csv"
    rows: list[dict[str, object]] = []
    for key in ("t0106_seed44", "t0112_seed77", "t0113_seed2247"):
        s = summaries[key]
        a = ASSET_DECLARED[key]
        n_total = int(a["n_cells_total"])
        jp_unique = int(a["n_joint_pass_unique"])
        rows.append(
            {
                "seed_label": key,
                "task_seed": (
                    44 if key == "t0106_seed44" else 77 if key == "t0112_seed77" else 2247
                ),
                "n_total_evals": n_total,
                "n_joint_pass_unique": jp_unique,
                "n_joint_pass_evaluations": int(
                    a["n_joint_pass_evaluations"],
                ),
                "joint_pass_pct": round(
                    100.0 * jp_unique / n_total if n_total > 0 else 0.0,
                    4,
                ),
                "best_dsi_overall": float(a["best_dsi_ratio"]),
                "best_legit_dsi": round(s.best_legit_dsi, 4),
                "best_pd_rate_hz": round(float(a["best_pd_rate_hz"]), 4),
                "n_generations_completed": int(a["n_generations_completed"]),
                "plateau_gen": int(a["n_generations_completed"]),
                "final_hypervolume": round(float(a["final_hypervolume"]), 4),
            }
        )
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return out_path


def csv_pareto_front_overlap_3seeds(
    *,
    datasets: dict[str, SeedDataset],
) -> Path:
    """For each t0113 Pareto cell, report nearest-neighbour distances to t0106
    and t0112 in both raw 68-d L2 and per-dimension z-scored L2 space. The
    z-scored standardisation uses every cell from all three predictions
    assets combined as the reference population (so the metric is comparable
    across the three seeds)."""

    out_path = DATA_DIR / "pareto_front_overlap_3seeds.csv"

    pf_113 = datasets["t0113_seed2247"].pareto_cells
    pf_106 = datasets["t0106_seed44"].pareto_cells
    pf_112 = datasets["t0112_seed77"].pareto_cells

    v_113 = np.asarray([c["vector_68d"] for c in pf_113], dtype=np.float64)
    v_106 = np.asarray([c["vector_68d"] for c in pf_106], dtype=np.float64)
    v_112 = np.asarray([c["vector_68d"] for c in pf_112], dtype=np.float64)

    # Build standardisation reference from ALL evaluations across all 3 seeds.
    all_evals: list[list[float]] = []
    for key in ("t0106_seed44", "t0112_seed77", "t0113_seed2247"):
        all_evals.extend([c["vector_68d"] for c in datasets[key].evaluations])
    all_arr = np.asarray(all_evals, dtype=np.float64)
    mu = all_arr.mean(axis=0)
    sigma = all_arr.std(axis=0)
    # Replace zero-variance dims with 1.0 to avoid divide-by-zero (no impact:
    # if sigma==0 then v - mu == 0 for every cell, distance contribution is 0).
    sigma_safe = np.where(sigma > 0, sigma, 1.0)

    def _z(v: np.ndarray) -> np.ndarray:
        result: np.ndarray = (v - mu) / sigma_safe
        return result

    z_113 = _z(v_113)
    z_106 = _z(v_106)
    z_112 = _z(v_112)

    rows: list[dict[str, object]] = []
    for i in range(v_113.shape[0]):
        # Raw and z-scored distances to t0106 Pareto cells.
        if v_106.shape[0] > 0:
            d_raw_106 = np.linalg.norm(v_106 - v_113[i], axis=1)
            d_z_106 = np.linalg.norm(z_106 - z_113[i], axis=1)
            nn_106_idx = int(np.argmin(d_z_106))
        else:
            d_raw_106 = np.array([np.nan])
            d_z_106 = np.array([np.nan])
            nn_106_idx = -1

        # Raw and z-scored distances to t0112 Pareto cells.
        if v_112.shape[0] > 0:
            d_raw_112 = np.linalg.norm(v_112 - v_113[i], axis=1)
            d_z_112 = np.linalg.norm(z_112 - z_113[i], axis=1)
            nn_112_idx = int(np.argmin(d_z_112))
        else:
            d_raw_112 = np.array([np.nan])
            d_z_112 = np.array([np.nan])
            nn_112_idx = -1

        rows.append(
            {
                "t0113_pareto_idx": i,
                "t0113_dsi": round(float(pf_113[i]["dsi_vector_sum"]), 4),
                "t0113_pd_rate_hz": round(float(pf_113[i]["pd_rate_hz"]), 4),
                "t0113_generation": int(pf_113[i].get("generation", -1)),
                "nn_t0106_idx_zscored": nn_106_idx,
                "nn_t0106_dsi": (
                    round(float(pf_106[nn_106_idx]["dsi_vector_sum"]), 4)
                    if nn_106_idx >= 0
                    else float("nan")
                ),
                "nn_t0106_pd_rate_hz": (
                    round(float(pf_106[nn_106_idx]["pd_rate_hz"]), 4)
                    if nn_106_idx >= 0
                    else float("nan")
                ),
                "nn_t0106_raw_l2_distance": round(
                    float(np.min(d_raw_106)),
                    4,
                ),
                "nn_t0106_zscored_l2_distance": round(
                    float(np.min(d_z_106)),
                    4,
                ),
                "nn_t0112_idx_zscored": nn_112_idx,
                "nn_t0112_dsi": (
                    round(float(pf_112[nn_112_idx]["dsi_vector_sum"]), 4)
                    if nn_112_idx >= 0
                    else float("nan")
                ),
                "nn_t0112_pd_rate_hz": (
                    round(float(pf_112[nn_112_idx]["pd_rate_hz"]), 4)
                    if nn_112_idx >= 0
                    else float("nan")
                ),
                "nn_t0112_raw_l2_distance": round(
                    float(np.min(d_raw_112)),
                    4,
                ),
                "nn_t0112_zscored_l2_distance": round(
                    float(np.min(d_z_112)),
                    4,
                ),
                "closer_to": ("t0106" if np.min(d_z_106) < np.min(d_z_112) else "t0112"),
            }
        )

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return out_path


# ----------------------------------------------------------------------------
# metrics.json
# ----------------------------------------------------------------------------


def build_metrics_json(*, summary_2247: JointPassSummary) -> Path:
    """Explicit multi-variant format with one variant for t0113 seed 2247.

    Sub-variants are encoded as dimensions:
    * `dsi_subvariant`: "best_legit" or "dsi_eq_one_count".

    Per the plan, only `direction_selectivity_index` is a registered metric.
    `best_legit` holds the highest non-DSI=1.0 cell. `dsi_eq_one_count`
    holds the count of cells exactly at DSI = 1.0 (silence-guard or
    single-spike artefacts).
    """

    cells = _load_evaluations(path=T0113_EVALS)
    n_dsi_eq_one = sum(1 for c in cells if float(c["dsi_vector_sum"]) >= DSI_SILENCE_GUARD_VALUE)

    common_dims: dict[str, object] = {
        "task_seed": 2247,
        "init_method": "lhs_random",
        "n_obj": 2,
        "n_directions": 2,
        "dsi_metric": "ratio",
        "dsi_silence_guard_active": True,
        "n_eval_seeds": 3,
        "n_generations_target": 60,
        "n_generations_completed": summary_2247.n_generations_completed,
        "n_cells": summary_2247.n_total_evals,
        "pool_restart_every": 10,
    }

    variants: list[dict[str, object]] = [
        {
            "variant_id": "random-init-seed2247-2dir-60gen-restart10-best-legit",
            "label": (
                "2-direction NSGA-II seed 2247: best legit DSI (highest non-silence-guard cell)"
            ),
            "dimensions": {**common_dims, "dsi_subvariant": "best_legit"},
            "metrics": {
                "direction_selectivity_index": round(
                    summary_2247.best_legit_dsi,
                    4,
                ),
            },
        },
        {
            "variant_id": "random-init-seed2247-2dir-60gen-restart10-overall-max",
            "label": ("2-direction NSGA-II seed 2247: overall max DSI (silence-guard saturated)"),
            "dimensions": {**common_dims, "dsi_subvariant": "overall_max"},
            "metrics": {
                "direction_selectivity_index": round(
                    summary_2247.best_dsi_overall,
                    4,
                ),
            },
        },
        {
            "variant_id": "random-init-seed2247-2dir-60gen-restart10-dsi-eq-one",
            "label": (
                "2-direction NSGA-II seed 2247: silence-guard ceiling cell "
                "count (cells at DSI = 1.0)"
            ),
            "dimensions": {
                **common_dims,
                "dsi_subvariant": "dsi_eq_one_count",
                "n_dsi_eq_one": int(n_dsi_eq_one),
            },
            "metrics": {
                "direction_selectivity_index": 1.0,
            },
        },
    ]

    payload: dict[str, object] = {"variants": variants}
    METRICS_JSON.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    return METRICS_JSON


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("[build_t0113_results] Loading 3-seed datasets...")
    datasets = load_all_three_seeds()
    for k, ds in datasets.items():
        print(
            f"  {k}: {len(ds.evaluations)} cells, "
            f"{len(ds.pareto_cells)} Pareto cells, "
            f"{len(ds.hv_trajectory)} HV-trajectory points",
        )

    print("[build_t0113_results] Computing per-seed summaries...")
    summaries = {k: summarize_seed(seed_key=k, ds=ds) for k, ds in datasets.items()}
    for k, s in summaries.items():
        print(
            f"  {k}: jp_unique={s.n_joint_pass_unique}, "
            f"jp_pct={s.joint_pass_pct:.3f}%, "
            f"best_legit_dsi={s.best_legit_dsi:.4f}, "
            f"best_pd={s.best_pd_rate_hz:.2f} Hz",
        )

    print("[build_t0113_results] Chart 1: pareto_front_3seeds.png")
    p1 = chart_pareto_front_3seeds(datasets=datasets)
    print(f"  -> {p1}")

    print("[build_t0113_results] Chart 2: hv_vs_gen_3seeds.png")
    p2 = chart_hv_vs_gen_3seeds(datasets=datasets)
    print(f"  -> {p2}")

    print("[build_t0113_results] Chart 3: joint_pass_yield_per_gen_3seeds.png")
    p3 = chart_joint_pass_yield_3seeds(datasets=datasets)
    print(f"  -> {p3}")

    print("[build_t0113_results] Chart 4: top50_morphologies_seed2247.png")
    p4 = chart_top50_morphologies_seed2247(ds_t0113=datasets["t0113_seed2247"])
    print(f"  -> {p4}")

    print("[build_t0113_results] Chart 5: asymmetry_distribution_3seeds.png")
    p5 = chart_asymmetry_distribution_3seeds(datasets=datasets)
    print(f"  -> {p5}")

    print(
        "[build_t0113_results] CSV 1: joint_pass_summary_3seeds.csv",
    )
    c1 = csv_joint_pass_summary_3seeds(summaries=summaries)
    print(f"  -> {c1}")

    print(
        "[build_t0113_results] CSV 2: pareto_front_overlap_3seeds.csv",
    )
    c2 = csv_pareto_front_overlap_3seeds(datasets=datasets)
    print(f"  -> {c2}")

    print("[build_t0113_results] metrics.json (registered metrics)")
    m = build_metrics_json(summary_2247=summaries["t0113_seed2247"])
    print(f"  -> {m}")

    print("[build_t0113_results] Done.")


if __name__ == "__main__":
    main()
