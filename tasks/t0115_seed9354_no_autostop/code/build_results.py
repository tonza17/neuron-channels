"""Generate t0115 result charts, CSV tables, predictions asset, and metrics.json.

Produces:
* `assets/predictions/t0115-bedb-morph-nsga2-seed9354/` (details.json,
  description.md, files/predictions.jsonl.gz).
* `results/data/joint_pass_summary_5seeds.csv`.
* `results/data/pareto_front_overlap_5seeds.csv`.
* `results/data/substrate_rate_5seed.csv`.
* `results/data/pareto_front_seed9354.json` (strict Pareto front).
* `results/data/example_cells_seed9354.json` (10 example cells).
* `results/images/hv_vs_gen_5seeds.png`.
* `results/images/pareto_front_5seeds.png`.
* `results/images/joint_pass_yield_per_gen_5seeds.png`.
* `results/images/substrate_rate_5seed_with_literature.png`.
* `results/metrics.json` (explicit multi-variant).

Note: `results/images/top50_morphologies_seed9354.png` (full dendrite tree
grid) is built by `build_top50_morphologies.py` — see operator feedback in
step log.
"""

from __future__ import annotations

import csv
import gzip
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from math import sqrt
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

TASK_ID: str = "t0115_seed9354_no_autostop"
TASK_DIR: Path = Path(__file__).resolve().parent.parent
TASKS_ROOT: Path = TASK_DIR.parent

T0106_DIR: Path = TASKS_ROOT / "t0106_long_pdnd_nsga2_300gen"
T0112_DIR: Path = TASKS_ROOT / "t0112_t0106_seed77_replicate"
T0113_DIR: Path = TASKS_ROOT / "t0113_t0106_seed2247_replicate"
T0114_DIR: Path = TASKS_ROOT / "t0114_seed7755_no_autostop"

# t0115 data files (already on disk).
T0115_EVALS: Path = TASK_DIR / "results" / "data" / "all_evaluations_seed9354.json"
T0115_HV: Path = TASK_DIR / "results" / "data" / "hv_trajectory_seed9354.json"

# Prior-seed evaluations (predictions assets).
T0106_EVALS: Path = (
    T0106_DIR
    / "assets"
    / "predictions"
    / "nsga2-seed44-bedb-morph-2dir-300gen"
    / "files"
    / "all_evaluations_seed44.json.gz"
)
T0106_HV: Path = T0106_DIR / "results" / "data" / "hv_trajectory_seed44.json"
T0106_PARETO: Path = T0106_DIR / "results" / "data" / "pareto_front_seed44.json"

T0112_EVALS: Path = T0112_DIR / "results" / "data" / "all_evaluations_seed77.json.gz"
T0112_HV: Path = T0112_DIR / "results" / "data" / "hv_trajectory_seed77.json"
T0112_PARETO: Path = T0112_DIR / "results" / "data" / "pareto_front_seed77.json"

T0113_EVALS: Path = (
    T0113_DIR
    / "assets"
    / "predictions"
    / "t0113-bedb-morph-nsga2-seed2247"
    / "files"
    / "all_evaluations_seed2247.json.gz"
)
T0113_HV: Path = T0113_DIR / "results" / "data" / "hv_trajectory_seed2247.json"
T0113_PARETO: Path = T0113_DIR / "results" / "data" / "pareto_front_seed2247.json"

T0114_EVALS: Path = T0114_DIR / "results" / "data" / "all_evaluations_seed7755.json"
T0114_HV: Path = T0114_DIR / "results" / "data" / "hv_trajectory_seed7755.json"
T0114_PARETO: Path = T0114_DIR / "results" / "data" / "pareto_front_seed7755.json"

# Outputs.
RESULTS_DIR: Path = TASK_DIR / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"
DATA_DIR: Path = RESULTS_DIR / "data"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
PREDICTIONS_ID: str = "t0115-bedb-morph-nsga2-seed9354"
PREDICTIONS_DIR: Path = TASK_DIR / "assets" / "predictions" / PREDICTIONS_ID
PREDICTIONS_FILES_DIR: Path = PREDICTIONS_DIR / "files"
PREDICTIONS_OUTPUT_JSONL_GZ: Path = PREDICTIONS_FILES_DIR / "predictions.jsonl.gz"

# ---------------------------------------------------------------------------
# Thresholds and constants
# ---------------------------------------------------------------------------

DSI_THRESHOLD: float = 0.5
PD_RATE_THRESHOLD_HZ: float = 30.0
LEGIT_DSI_CEILING: float = 0.9999
SILENCE_GUARD_DSI: float = 1.0
TOP_K_MORPHOLOGY: int = 50
PROJECT_DATE: str = "2026-05-21"

# Literature baselines for substrate-rate comparison.
HAY_2011_RATE_PCT: float = 0.40
DRUCKMANN_2007_RATE_PCT: float = 0.10

# Seed metadata (canonical asset-declared headline numbers).
ASSET_DECLARED: dict[str, dict[str, float | int | str]] = {
    "t0106_seed44": {
        "task_seed": 44,
        "n_generations_completed": 39,
        "n_cells_total": 3744,
        "final_hypervolume": 122.0288,
        "stop_trigger": "hv_plateau",
    },
    "t0112_seed77": {
        "task_seed": 77,
        "n_generations_completed": 21,
        "n_cells_total": 2016,
        "final_hypervolume": 107.4602,
        "stop_trigger": "hv_plateau",
    },
    "t0113_seed2247": {
        "task_seed": 2247,
        "n_generations_completed": 14,
        "n_cells_total": 1344,
        "final_hypervolume": 45.6221,
        "stop_trigger": "hv_plateau",
    },
    "t0114_seed7755": {
        "task_seed": 7755,
        "n_generations_completed": 62,
        "n_cells_total": 5952,
        "final_hypervolume": 111.5353,
        "stop_trigger": "operator_stop",
    },
    "t0115_seed9354": {
        "task_seed": 9354,
        "n_generations_completed": 55,
        "n_cells_total": 5280,
        "final_hypervolume": 50.5646,
        "stop_trigger": "operator_stop",
    },
}

SEED_COLORS: dict[str, str] = {
    "t0106_seed44": "C0",
    "t0112_seed77": "C3",
    "t0113_seed2247": "C2",
    "t0114_seed7755": "C1",
    "t0115_seed9354": "C4",
}
SEED_MARKERS: dict[str, str] = {
    "t0106_seed44": "o",
    "t0112_seed77": "D",
    "t0113_seed2247": "s",
    "t0114_seed7755": "^",
    "t0115_seed9354": "v",
}
SEED_LABELS: dict[str, str] = {
    "t0106_seed44": "t0106 seed 44",
    "t0112_seed77": "t0112 seed 77",
    "t0113_seed2247": "t0113 seed 2247",
    "t0114_seed7755": "t0114 seed 7755",
    "t0115_seed9354": "t0115 seed 9354",
}
POOL_RESTART_CADENCE: dict[str, int] = {
    "t0106_seed44": 25,
    "t0112_seed77": 10,
    "t0113_seed2247": 10,
    "t0114_seed7755": 10,
    "t0115_seed9354": 10,
}
ALL_SEED_KEYS: tuple[str, ...] = (
    "t0106_seed44",
    "t0112_seed77",
    "t0113_seed2247",
    "t0114_seed7755",
    "t0115_seed9354",
)


# ---------------------------------------------------------------------------
# Data containers
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SeedDataset:
    key: str
    label: str
    evaluations: list[dict[str, Any]]
    hv_trajectory: list[dict[str, Any]]
    pareto_cells: list[dict[str, Any]]


@dataclass(frozen=True, slots=True)
class PerSeedSummary:
    key: str
    task_seed: int
    n_total_evals: int
    n_joint_pass_unique: int
    n_joint_pass_legit_unique: int
    joint_pass_pct: float
    best_legit_dsi: float
    overall_max_dsi: float
    n_dsi_eq_one: int
    best_pd_rate_hz: float
    n_generations_completed: int
    plateau_gen: int
    final_hypervolume: float
    stop_trigger: str


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------


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


def _load_hv(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    traj = data.get("trajectory", data) if isinstance(data, dict) else data
    assert isinstance(traj, list), "hv trajectory is a list"
    return traj


def _load_pareto_cells(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    cells = data["cells"]
    assert isinstance(cells, list), "cells is a list"
    return cells


# ---------------------------------------------------------------------------
# Cell-level helpers
# ---------------------------------------------------------------------------


def _is_joint_pass(cell: dict[str, Any]) -> bool:
    dsi = float(cell["dsi_vector_sum"])
    pd = float(cell["pd_rate_hz"])
    return dsi >= DSI_THRESHOLD and pd >= PD_RATE_THRESHOLD_HZ


def _is_legit(cell: dict[str, Any]) -> bool:
    return float(cell["dsi_vector_sum"]) < LEGIT_DSI_CEILING


def _is_legit_joint_pass(cell: dict[str, Any]) -> bool:
    return _is_joint_pass(cell) and _is_legit(cell)


def _summarize_seed(*, key: str, ds: SeedDataset) -> PerSeedSummary:
    a = ASSET_DECLARED[key]
    cells = ds.evaluations
    legit_dsis = [float(c["dsi_vector_sum"]) for c in cells if _is_legit(c)]
    best_legit = max(legit_dsis) if len(legit_dsis) > 0 else float("nan")
    jp_unique_keys: set[tuple[float, ...]] = set()
    legit_jp_unique_keys: set[tuple[float, ...]] = set()
    for c in cells:
        k = tuple(c["vector_68d"])
        if _is_joint_pass(c):
            jp_unique_keys.add(k)
            if _is_legit(c):
                legit_jp_unique_keys.add(k)
    n_dsi_eq_one = sum(1 for c in cells if float(c["dsi_vector_sum"]) >= SILENCE_GUARD_DSI)
    n_total = len(cells)
    legit_pct = 100.0 * len(legit_jp_unique_keys) / n_total if n_total > 0 else 0.0
    return PerSeedSummary(
        key=key,
        task_seed=int(a["task_seed"]),
        n_total_evals=n_total,
        n_joint_pass_unique=len(jp_unique_keys),
        n_joint_pass_legit_unique=len(legit_jp_unique_keys),
        joint_pass_pct=legit_pct,
        best_legit_dsi=best_legit,
        overall_max_dsi=max(float(c["dsi_vector_sum"]) for c in cells),
        n_dsi_eq_one=n_dsi_eq_one,
        best_pd_rate_hz=max(float(c["pd_rate_hz"]) for c in cells),
        n_generations_completed=int(a["n_generations_completed"]),
        plateau_gen=int(a["n_generations_completed"]),
        final_hypervolume=float(a["final_hypervolume"]),
        stop_trigger=str(a["stop_trigger"]),
    )


def cumulative_joint_pass_per_gen(
    *,
    cells: list[dict[str, Any]],
) -> dict[int, int]:
    seen: set[tuple[float, ...]] = set()
    gens = sorted({int(c["generation"]) for c in cells})
    out: dict[int, int] = {}
    for g in gens:
        for c in cells:
            if int(c["generation"]) == g and _is_joint_pass(c):
                seen.add(tuple(c["vector_68d"]))
        out[g] = len(seen)
    return out


# ---------------------------------------------------------------------------
# Strict Pareto front (2D minimisation in objective_F_minimised)
# ---------------------------------------------------------------------------


def _compute_pareto_front(
    *,
    evaluations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Strict non-dominated set in (objective_F_minimised[0], [1]) space."""
    objs = np.asarray(
        [c["objective_F_minimised"] for c in evaluations],
        dtype=np.float64,
    )
    n = objs.shape[0]
    is_dominated = np.zeros(n, dtype=bool)
    for i in range(n):
        if is_dominated[i]:
            continue
        diff = objs - objs[i]
        le = np.all(diff <= 0, axis=1)
        lt = np.any(diff < 0, axis=1)
        dominators = le & lt
        dominators[i] = False
        if np.any(dominators):
            is_dominated[i] = True
    seen_obj: set[tuple[float, float]] = set()
    pareto_cells: list[dict[str, Any]] = []
    cell_id = 0
    for i in range(n):
        if is_dominated[i]:
            continue
        key = (float(objs[i, 0]), float(objs[i, 1]))
        if key in seen_obj:
            continue
        seen_obj.add(key)
        c = evaluations[i]
        pareto_cells.append(
            {
                "cell_id": cell_id,
                "vector_68d": list(c["vector_68d"]),
                "params": list(c["vector_68d"][:54]),
                "morphology_vector_14d": list(c["vector_68d"][54:68]),
                "objective_F_minimised": list(c["objective_F_minimised"]),
                "dsi_vector_sum": float(c["dsi_vector_sum"]),
                "pd_rate_hz": float(c["pd_rate_hz"]),
                "generation": int(c["generation"]),
            }
        )
        cell_id += 1
    pareto_cells.sort(key=lambda c: (c["pd_rate_hz"], -c["dsi_vector_sum"]))
    for i, c in enumerate(pareto_cells):
        c["cell_id"] = i
    return pareto_cells


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def load_all_five_seeds() -> dict[str, SeedDataset]:
    print("[load] t0115 seed 9354")
    t0115_evals = _load_evaluations(path=T0115_EVALS)
    t0115_hv = _load_hv(path=T0115_HV)
    t0115_pareto = _compute_pareto_front(evaluations=t0115_evals)

    pareto_payload = {
        "seed": 9354,
        "n_total": len(t0115_pareto),
        "cells": t0115_pareto,
    }
    (DATA_DIR / "pareto_front_seed9354.json").write_text(
        json.dumps(pareto_payload, indent=2),
        encoding="utf-8",
    )

    print("[load] t0114 seed 7755")
    t0114_evals = _load_evaluations(path=T0114_EVALS)
    t0114_hv = _load_hv(path=T0114_HV)
    if T0114_PARETO.exists():
        t0114_pareto = _load_pareto_cells(path=T0114_PARETO)
    else:
        t0114_pareto = _compute_pareto_front(evaluations=t0114_evals)

    print("[load] t0113 seed 2247")
    t0113 = SeedDataset(
        key="t0113_seed2247",
        label=SEED_LABELS["t0113_seed2247"],
        evaluations=_load_evaluations(path=T0113_EVALS),
        hv_trajectory=_load_hv(path=T0113_HV),
        pareto_cells=_load_pareto_cells(path=T0113_PARETO),
    )
    print("[load] t0112 seed 77")
    t0112 = SeedDataset(
        key="t0112_seed77",
        label=SEED_LABELS["t0112_seed77"],
        evaluations=_load_evaluations(path=T0112_EVALS),
        hv_trajectory=_load_hv(path=T0112_HV),
        pareto_cells=_load_pareto_cells(path=T0112_PARETO),
    )
    print("[load] t0106 seed 44")
    t0106 = SeedDataset(
        key="t0106_seed44",
        label=SEED_LABELS["t0106_seed44"],
        evaluations=_load_evaluations(path=T0106_EVALS),
        hv_trajectory=_load_hv(path=T0106_HV),
        pareto_cells=_load_pareto_cells(path=T0106_PARETO),
    )
    t0114 = SeedDataset(
        key="t0114_seed7755",
        label=SEED_LABELS["t0114_seed7755"],
        evaluations=t0114_evals,
        hv_trajectory=t0114_hv,
        pareto_cells=t0114_pareto,
    )
    t0115 = SeedDataset(
        key="t0115_seed9354",
        label=SEED_LABELS["t0115_seed9354"],
        evaluations=t0115_evals,
        hv_trajectory=t0115_hv,
        pareto_cells=t0115_pareto,
    )
    return {
        "t0106_seed44": t0106,
        "t0112_seed77": t0112,
        "t0113_seed2247": t0113,
        "t0114_seed7755": t0114,
        "t0115_seed9354": t0115,
    }


# ---------------------------------------------------------------------------
# CSVs
# ---------------------------------------------------------------------------


def csv_joint_pass_summary_5seeds(
    *,
    summaries: dict[str, PerSeedSummary],
) -> Path:
    out_path = DATA_DIR / "joint_pass_summary_5seeds.csv"
    fieldnames = [
        "seed_label",
        "task_seed",
        "n_total_evals",
        "n_joint_pass_unique",
        "n_joint_pass_legit_unique",
        "joint_pass_pct",
        "best_dsi_overall",
        "best_legit_dsi",
        "best_pd_rate_hz",
        "n_generations_completed",
        "plateau_gen",
        "final_hypervolume",
        "stop_trigger",
    ]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for key in ALL_SEED_KEYS:
            s = summaries[key]
            writer.writerow(
                {
                    "seed_label": key,
                    "task_seed": s.task_seed,
                    "n_total_evals": s.n_total_evals,
                    "n_joint_pass_unique": s.n_joint_pass_unique,
                    "n_joint_pass_legit_unique": s.n_joint_pass_legit_unique,
                    "joint_pass_pct": round(s.joint_pass_pct, 4),
                    "best_dsi_overall": round(s.overall_max_dsi, 4),
                    "best_legit_dsi": round(s.best_legit_dsi, 4),
                    "best_pd_rate_hz": round(s.best_pd_rate_hz, 4),
                    "n_generations_completed": s.n_generations_completed,
                    "plateau_gen": s.plateau_gen,
                    "final_hypervolume": round(s.final_hypervolume, 4),
                    "stop_trigger": s.stop_trigger,
                }
            )
    return out_path


def csv_pareto_front_overlap_5seeds(
    *,
    datasets: dict[str, SeedDataset],
) -> Path:
    """For each t0115 strict Pareto cell, compute nearest-neighbour z-scored L2
    distance to the closest cell from each of t0106 / t0112 / t0113 / t0114."""
    out_path = DATA_DIR / "pareto_front_overlap_5seeds.csv"

    pf_115 = datasets["t0115_seed9354"].pareto_cells
    pf_106 = datasets["t0106_seed44"].pareto_cells
    pf_112 = datasets["t0112_seed77"].pareto_cells
    pf_113 = datasets["t0113_seed2247"].pareto_cells
    pf_114 = datasets["t0114_seed7755"].pareto_cells

    def _v(cells: list[dict[str, Any]]) -> np.ndarray:
        if len(cells) == 0:
            return np.zeros((0, 68), dtype=np.float64)
        return np.asarray([c["vector_68d"] for c in cells], dtype=np.float64)

    v_115 = _v(pf_115)
    v_106 = _v(pf_106)
    v_112 = _v(pf_112)
    v_113 = _v(pf_113)
    v_114 = _v(pf_114)

    all_vecs: list[list[float]] = []
    for key in ALL_SEED_KEYS:
        all_vecs.extend([c["vector_68d"] for c in datasets[key].evaluations])
    all_arr = np.asarray(all_vecs, dtype=np.float64)
    mu = all_arr.mean(axis=0)
    sigma = all_arr.std(axis=0)
    sigma_safe = np.where(sigma > 0, sigma, 1.0)

    def _z(v: np.ndarray) -> np.ndarray:
        result: np.ndarray = (v - mu) / sigma_safe
        return result

    z_115 = _z(v_115)
    z_106 = _z(v_106)
    z_112 = _z(v_112)
    z_113 = _z(v_113)
    z_114 = _z(v_114)

    rows: list[dict[str, object]] = []
    for i in range(v_115.shape[0]):
        cell = pf_115[i]
        query_z = z_115[i]

        def _nn_dist(z_target: np.ndarray, query: np.ndarray = query_z) -> tuple[int, float]:
            if z_target.shape[0] == 0:
                return -1, float("nan")
            d = np.linalg.norm(z_target - query, axis=1)
            idx = int(np.argmin(d))
            return idx, float(np.min(d))

        i_106, d_106 = _nn_dist(z_106)
        i_112, d_112 = _nn_dist(z_112)
        i_113, d_113 = _nn_dist(z_113)
        i_114, d_114 = _nn_dist(z_114)

        seed_dists: list[tuple[str, float]] = []
        if not np.isnan(d_106):
            seed_dists.append(("t0106", d_106))
        if not np.isnan(d_112):
            seed_dists.append(("t0112", d_112))
        if not np.isnan(d_113):
            seed_dists.append(("t0113", d_113))
        if not np.isnan(d_114):
            seed_dists.append(("t0114", d_114))
        seed_dists.sort(key=lambda x: x[1])
        closer_to = seed_dists[0][0] if seed_dists else ""

        rows.append(
            {
                "t0115_pareto_idx": i,
                "t0115_dsi": round(float(cell["dsi_vector_sum"]), 4),
                "t0115_pd_rate_hz": round(float(cell["pd_rate_hz"]), 4),
                "t0115_generation": int(cell["generation"]),
                "nn_t0106_idx": i_106,
                "nn_t0106_zscored_l2_distance": (round(d_106, 4) if not np.isnan(d_106) else ""),
                "nn_t0112_idx": i_112,
                "nn_t0112_zscored_l2_distance": (round(d_112, 4) if not np.isnan(d_112) else ""),
                "nn_t0113_idx": i_113,
                "nn_t0113_zscored_l2_distance": (round(d_113, 4) if not np.isnan(d_113) else ""),
                "nn_t0114_idx": i_114,
                "nn_t0114_zscored_l2_distance": (round(d_114, 4) if not np.isnan(d_114) else ""),
                "closer_to": closer_to,
            }
        )
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return out_path


@dataclass(frozen=True, slots=True)
class SubstrateStats:
    rates_pct: dict[str, float]
    mean_pct: float
    sd_pct: float
    se_pct: float


def _compute_substrate_stats(
    *,
    summaries: dict[str, PerSeedSummary],
) -> SubstrateStats:
    rates: dict[str, float] = {}
    for key in ALL_SEED_KEYS:
        s = summaries[key]
        rate = 100.0 * s.n_joint_pass_legit_unique / s.n_total_evals
        rates[key] = rate
    n = len(rates)
    mean = sum(rates.values()) / n
    sd = sqrt(sum((r - mean) ** 2 for r in rates.values()) / (n - 1))
    se = sd / sqrt(n)
    return SubstrateStats(rates_pct=rates, mean_pct=mean, sd_pct=sd, se_pct=se)


def csv_substrate_rate_5seed(
    *,
    summaries: dict[str, PerSeedSummary],
    stats: SubstrateStats,
) -> Path:
    out_path = DATA_DIR / "substrate_rate_5seed.csv"
    rows: list[dict[str, object]] = []
    for key in ALL_SEED_KEYS:
        s = summaries[key]
        rate = stats.rates_pct[key]
        rows.append(
            {
                "seed_label": key,
                "task_seed": s.task_seed,
                "n_total_evals": s.n_total_evals,
                "n_legit_joint_pass_unique": s.n_joint_pass_legit_unique,
                "acceptance_rate_pct": round(rate, 4),
                "convention": "unique_legit_jp_cells_per_total_evals",
            }
        )
    rows.append(
        {
            "seed_label": "5seed_mean",
            "task_seed": "",
            "n_total_evals": "",
            "n_legit_joint_pass_unique": "",
            "acceptance_rate_pct": round(stats.mean_pct, 4),
            "convention": "unique_legit_jp_cells_per_total_evals",
        }
    )
    rows.append(
        {
            "seed_label": "5seed_sample_sd",
            "task_seed": "",
            "n_total_evals": "",
            "n_legit_joint_pass_unique": "",
            "acceptance_rate_pct": round(stats.sd_pct, 4),
            "convention": "unique_legit_jp_cells_per_total_evals",
        }
    )
    rows.append(
        {
            "seed_label": "5seed_sample_se",
            "task_seed": "",
            "n_total_evals": "",
            "n_legit_joint_pass_unique": "",
            "acceptance_rate_pct": round(stats.se_pct, 4),
            "convention": "unique_legit_jp_cells_per_total_evals",
        }
    )
    rows.append(
        {
            "seed_label": "hay_2011_envelope_upper",
            "task_seed": "",
            "n_total_evals": "",
            "n_legit_joint_pass_unique": "",
            "acceptance_rate_pct": HAY_2011_RATE_PCT,
            "convention": "literature_baseline",
        }
    )
    rows.append(
        {
            "seed_label": "druckmann_2007_baseline",
            "task_seed": "",
            "n_total_evals": "",
            "n_legit_joint_pass_unique": "",
            "acceptance_rate_pct": DRUCKMANN_2007_RATE_PCT,
            "convention": "literature_baseline",
        }
    )
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return out_path


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------


def chart_hv_vs_gen_5seeds(*, datasets: dict[str, SeedDataset]) -> Path:
    fig, ax = plt.subplots(figsize=(10, 6))
    for key in ALL_SEED_KEYS:
        ds = datasets[key]
        gens = [int(h["generation"]) for h in ds.hv_trajectory]
        hvs = [float(h["hypervolume"]) for h in ds.hv_trajectory]
        cadence = POOL_RESTART_CADENCE[key]
        ax.plot(
            gens,
            hvs,
            label=(f"{ds.label} (restart {cadence}, {len(gens)} gens, final HV={hvs[-1]:.2f})"),
            color=SEED_COLORS[key],
            marker=SEED_MARKERS[key],
            ms=3.0,
            lw=1.4,
        )
        max_gen = max(gens) if len(gens) > 0 else 0
        restart_gens = list(range(cadence, max_gen + 1, cadence))
        for g in restart_gens:
            ax.axvline(
                g,
                color=SEED_COLORS[key],
                ls=":",
                lw=0.4,
                alpha=0.30,
            )
    ax.set_yscale("log")
    ax.set_xlabel("generation")
    ax.set_ylabel("hypervolume (log scale)")
    ax.set_title(
        "HV trajectory: seeds 44, 77, 2247, 7755, 9354 with pool-restart events annotated",
    )
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, ls=":", lw=0.5, alpha=0.5)
    fig.tight_layout()
    out_path = IMAGES_DIR / "hv_vs_gen_5seeds.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_pareto_front_5seeds(*, datasets: dict[str, SeedDataset]) -> Path:
    fig, ax = plt.subplots(figsize=(10, 6))
    max_pd = 0.0
    for key in ALL_SEED_KEYS:
        ds = datasets[key]
        x = [float(c["dsi_vector_sum"]) for c in ds.pareto_cells]
        y = [float(c["pd_rate_hz"]) for c in ds.pareto_cells]
        if len(y) > 0:
            max_pd = max(max_pd, max(y))
        ax.scatter(
            x,
            y,
            s=45,
            alpha=0.7,
            label=f"{ds.label} (n={len(ds.pareto_cells)})",
            color=SEED_COLORS[key],
            marker=SEED_MARKERS[key],
            edgecolors="black",
            linewidths=0.3,
        )
    ax.axvline(
        DSI_THRESHOLD,
        color="grey",
        ls="--",
        lw=0.7,
        alpha=0.6,
        label="DSI = 0.5",
    )
    ax.axhline(
        PD_RATE_THRESHOLD_HZ,
        color="grey",
        ls=":",
        lw=0.7,
        alpha=0.6,
        label="PD = 30 Hz",
    )
    ax.set_xlabel("ratio DSI")
    ax.set_ylabel("PD-rate (Hz)")
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, (max_pd if max_pd > 0 else 130.0) * 1.10)
    ax.set_title("Strict Pareto fronts: t0106, t0112, t0113, t0114, t0115 (seed 9354)")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    out_path = IMAGES_DIR / "pareto_front_5seeds.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_joint_pass_yield_5seeds(
    *,
    datasets: dict[str, SeedDataset],
) -> Path:
    fig, ax = plt.subplots(figsize=(10, 6))
    for key in ALL_SEED_KEYS:
        ds = datasets[key]
        per_gen = cumulative_joint_pass_per_gen(cells=ds.evaluations)
        gens = list(per_gen.keys())
        counts = list(per_gen.values())
        final = counts[-1] if len(counts) > 0 else 0
        ax.plot(
            gens,
            counts,
            label=f"{ds.label} (final={final})",
            color=SEED_COLORS[key],
            marker=SEED_MARKERS[key],
            ms=3.5,
            lw=1.4,
        )
    ax.set_xlabel("generation")
    ax.set_ylabel("cumulative unique joint-pass cells")
    ax.set_title(
        "Joint-pass cell discovery per generation (DSI >= 0.5, PD >= 30 Hz; 5 seeds)",
    )
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, ls=":", lw=0.5, alpha=0.5)
    fig.tight_layout()
    out_path = IMAGES_DIR / "joint_pass_yield_per_gen_5seeds.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_substrate_rate_5seed_with_literature(
    *,
    summaries: dict[str, PerSeedSummary],
    stats: SubstrateStats,
) -> Path:
    fig, ax = plt.subplots(figsize=(9, 6))
    seed_labels: list[str] = []
    rate_values: list[float] = []
    bar_colors: list[str] = []
    for key in ALL_SEED_KEYS:
        seed_labels.append(SEED_LABELS[key])
        rate_values.append(stats.rates_pct[key])
        bar_colors.append(SEED_COLORS[key])
    seed_labels.append("5-seed mean")
    rate_values.append(stats.mean_pct)
    bar_colors.append("black")

    xs = np.arange(len(seed_labels))
    bars = ax.bar(xs, rate_values, color=bar_colors, alpha=0.75, edgecolor="black")
    ax.errorbar(
        x=xs[-1],
        y=stats.mean_pct,
        yerr=stats.se_pct,
        fmt="none",
        ecolor="black",
        capsize=6,
        lw=1.8,
        label=f"5-seed SE = {stats.se_pct:.2f}%",
    )
    ax.axhline(
        HAY_2011_RATE_PCT,
        color="crimson",
        ls="--",
        lw=1.6,
        label=f"Hay 2011 envelope upper = {HAY_2011_RATE_PCT:.2f}%",
    )
    ax.axhline(
        DRUCKMANN_2007_RATE_PCT,
        color="darkblue",
        ls=":",
        lw=1.6,
        label=f"Druckmann 2007 baseline = {DRUCKMANN_2007_RATE_PCT:.2f}%",
    )
    for b in bars:
        h = b.get_height()
        ax.text(
            b.get_x() + b.get_width() / 2,
            h + max(rate_values) * 0.01,
            f"{h:.2f}%",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.set_xticks(xs)
    ax.set_xticklabels(seed_labels, rotation=20, ha="right")
    ax.set_ylabel("LEGIT joint-pass acceptance rate (%)")
    ax.set_title(
        "5-seed substrate-rate estimate vs literature baselines (Hay 2011, Druckmann 2007)",
    )
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, ls=":", lw=0.5, alpha=0.5, axis="y")
    fig.tight_layout()
    out_path = IMAGES_DIR / "substrate_rate_5seed_with_literature.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


# ---------------------------------------------------------------------------
# Predictions asset
# ---------------------------------------------------------------------------


def build_predictions_asset(
    *,
    seed_summary: PerSeedSummary,
    evaluations: list[dict[str, Any]],
) -> tuple[Path, Path, Path]:
    PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
    PREDICTIONS_FILES_DIR.mkdir(parents=True, exist_ok=True)

    with gzip.open(PREDICTIONS_OUTPUT_JSONL_GZ, "wt", encoding="utf-8") as gz:
        for c in evaluations:
            dsi = float(c["dsi_vector_sum"])
            pd_rate = float(c["pd_rate_hz"])
            rec = {
                "generation": int(c["generation"]),
                "vector_68d": list(c["vector_68d"]),
                "objective_F_minimised": list(c["objective_F_minimised"]),
                "dsi_vector_sum": dsi,
                "pd_rate_hz": pd_rate,
                "joint_pass": dsi >= DSI_THRESHOLD and pd_rate >= PD_RATE_THRESHOLD_HZ,
                "legit": dsi < LEGIT_DSI_CEILING,
            }
            gz.write(json.dumps(rec))
            gz.write("\n")

    details = {
        "spec_version": "2",
        "predictions_id": PREDICTIONS_ID,
        "name": (
            "NSGA-II seed 9354 on 68-d Bed B + 14-d morphology, 2 directions, "
            "55-gen run with HV-plateau auto-stop DISABLED "
            "(5th seed of S-0112-01 batch)"
        ),
        "short_description": (
            f"All {seed_summary.n_total_evals} per-cell NSGA-II evaluations "
            "from t0115 single random-init GA seed 9354 on the 68-d Bed B "
            "electrophys + 14-d morphology DSGC substrate. Final 5th seed of "
            "the S-0112-01 substrate-rate confirmation batch; re-runs "
            "t0106/t0112/t0113/t0114 with HV-plateau auto-stop DISABLED. Run "
            "terminated by operator stop at gen 55 after the HV trajectory "
            f"plateaued near HV approximately {seed_summary.final_hypervolume:.2f}."
        ),
        "description_path": "description.md",
        "model_id": None,
        "model_description": (
            "Compartmental DSGC neuron model combining the 54-d Bed B "
            "electrophysiology parameter vector (from t0080) applied via "
            "apply_parameter_vector with the t0092-patched 14-d procedural "
            "morphology generator (canonical via correction C-0093-01). Each "
            "cell is evaluated with 2 stimulus directions (PD = 0 deg, ND = "
            "180 deg) x 3 noise replicates and scored on a 2-objective vector "
            "(ratio DSI, preferred-direction firing rate in Hz). NSGA-II "
            "minimises the negated pair; the DSI silence guard from S-0102-01 "
            "clamps DSI to 0.0 when total PD+ND spike count falls below 10 "
            "spikes per trial. Identical to t0114 except GA seed 7755 -> 9354 "
            "(drawn via secrets.randbelow(10000)) and the same HV-plateau "
            "auto-stop DISABLED control. Pool restart cadence 10. 68-d Bed B + "
            "14-d morphology substrate, ratio DSI metric, silence guard "
            "active, N_EVAL_SEEDS=3."
        ),
        "dataset_ids": [],
        "prediction_format": "jsonl.gz",
        "prediction_schema": (
            f"Gzipped JSONL with one line per evaluated cell "
            f"({seed_summary.n_total_evals} lines). Each line is a JSON object "
            "with fields: generation (int, NSGA-II generation; 1 = initial "
            "LHS population, 2-55 = offspring generations), vector_68d (list "
            "of 68 floats, 54-d electrophys + 14-d morphology parameter "
            "vector), objective_F_minimised (list of 2 floats, the NSGA-II "
            "objective vector with sign-flipped maximisation conventions: "
            "[-ratio_dsi, -pd_rate_hz]), dsi_vector_sum (float in [0, 1], the "
            "ratio DSI (PD - ND) / (PD + ND); guard-cleaned per S-0102-01 so "
            "values of 0.0 may either be real or guard-floor and values of "
            "1.0 may be silence-guard ceilings), pd_rate_hz (float, "
            "preferred-direction mean firing rate in Hz across the 3 noise "
            "replicates), joint_pass (bool, true iff dsi_vector_sum >= 0.5 "
            "AND pd_rate_hz >= 30 — the 2-axis strict criterion), legit "
            "(bool, true iff dsi_vector_sum < 0.9999 — false flags the "
            "silence-guard / single-spike DSI=1.0 ceiling artefact)."
        ),
        "instance_count": seed_summary.n_total_evals,
        "metrics_at_creation": {
            "n_generations_completed": seed_summary.n_generations_completed,
            "n_cells_total": seed_summary.n_total_evals,
            "best_dsi_ratio": round(seed_summary.overall_max_dsi, 4),
            "best_legit_dsi": round(seed_summary.best_legit_dsi, 4),
            "best_pd_rate_hz": round(seed_summary.best_pd_rate_hz, 4),
            "n_joint_pass_unique": seed_summary.n_joint_pass_unique,
            "n_joint_pass_legit_unique": (seed_summary.n_joint_pass_legit_unique),
            "final_hypervolume": round(seed_summary.final_hypervolume, 4),
            "stop_trigger": seed_summary.stop_trigger,
        },
        "files": [
            {
                "path": f"files/{PREDICTIONS_OUTPUT_JSONL_GZ.name}",
                "description": (
                    f"Per-cell NSGA-II evaluation log for t0115 GA seed 9354 "
                    f"({seed_summary.n_total_evals} cells across "
                    f"{seed_summary.n_generations_completed} completed "
                    "generations; operator stop). gzip-compressed JSONL; "
                    "decompress with `gunzip` or `gzip -d` before line-wise "
                    "JSON parse."
                ),
                "format": "jsonl.gz",
            }
        ],
        "categories": [
            "direction-selectivity",
            "compartmental-modeling",
            "retinal-ganglion-cell",
        ],
        "created_by_task": TASK_ID,
        "date_created": PROJECT_DATE,
    }
    details_path = PREDICTIONS_DIR / "details.json"
    details_path.write_text(
        json.dumps(details, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    description = _build_description_md(seed_summary=seed_summary)
    desc_path = PREDICTIONS_DIR / "description.md"
    desc_path.write_text(description, encoding="utf-8")

    return PREDICTIONS_OUTPUT_JSONL_GZ, details_path, desc_path


def _build_description_md(*, seed_summary: PerSeedSummary) -> str:
    name = (
        "NSGA-II seed 9354 on 68-d Bed B + 14-d morphology, 2 directions, "
        "55-gen run with HV-plateau auto-stop DISABLED "
        "(5th seed of S-0112-01 batch)"
    )
    metadata = (
        "## Metadata\n\n"
        f"* **Name**: {name}\n"
        "* **Model**: Compartmental DSGC model (t0092-patched procedural "
        "morphology + 54-d Bed B electrophys vector via t0080 "
        "apply_parameter_vector)\n"
        "* **Datasets**: none (simulator outputs)\n"
        "* **Format**: jsonl.gz\n"
        f"* **Instances**: {seed_summary.n_total_evals:,} per-cell evaluations "
        f"across {seed_summary.n_generations_completed} NSGA-II generations\n"
        f"* **Created by**: {TASK_ID}\n"
    )
    overview = (
        "## Overview\n\n"
        "These predictions capture every cell evaluated by the t0115 "
        f"single-seed NSGA-II run with GA seed=9354 "
        f"({seed_summary.n_total_evals:,} cells across "
        f"{seed_summary.n_generations_completed} generations). The run is the "
        "5th and final seed in the S-0112-01 substrate-rate confirmation "
        "batch: t0106 (seed 44), t0112 (seed 77), t0113 (seed 2247), t0114 "
        "(seed 7755), and t0115 (seed 9354). Like t0114 it disables the "
        "HV-plateau auto-stop and terminates by operator decision; the run "
        "reached gen 55 before being stopped after the HV trajectory visibly "
        f"plateaued near HV = {seed_summary.final_hypervolume:.2f}.\n\n"
        f"The {seed_summary.n_joint_pass_legit_unique} unique LEGIT "
        "joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz AND DSI < 0.9999) "
        "collected by this seed contribute the fifth data point to the "
        "substrate-rate estimate. The asset is the primary evidence channel "
        "for the t0115 results summary, the 5-seed cross-comparison CSVs in "
        "`results/data/`, and the literature comparison against Hay 2011 "
        "(0.40%) and Druckmann 2007 (0.10%).\n"
    )
    model_section = (
        "## Model\n\n"
        "Compartmental DSGC neuron model with the t0092-patched procedural "
        "morphology generator (`generate_fixed_morphology`, canonical via "
        "correction C-0093-01) and the 54-d Bed B electrophys parameter "
        "vector applied via t0080's `apply_parameter_vector`. Per-cell "
        "evaluation runs 2 stimulus directions (PD = 0 deg, ND = 180 deg) x "
        "3 noise replicates with objectives = (ratio DSI, preferred-direction "
        "firing rate in Hz), both maximised. Pymoo NSGA-II minimises the "
        "negated pair. Crossover SBX eta=15 with prob=0.9; polynomial "
        "mutation eta=20 with prob=1/68; duplicate elimination enabled. "
        "Population size 96, n_gen_max=300 (HV-plateau auto-stop DISABLED, "
        "so the run terminates only by cost cap or operator stop), "
        "LHS-initialised initial population with explicit "
        "`np.random.SeedSequence` seeding for reproducibility. Pool restart "
        "cadence 10 (same as t0112 / t0113 / t0114). The DSI silence guard "
        "from S-0102-01 is active: cells whose total PD+ND spike count "
        "across the 2 directions falls below 10 have DSI clamped to 0.0 "
        "before being returned to NSGA-II.\n"
    )
    data_section = (
        "## Data\n\n"
        "No external dataset is consumed. Input vectors are 68-d points "
        "sampled by NSGA-II starting from a 96-row Latin Hypercube Sample "
        "drawn with pymoo's `LatinHypercubeSampling` and explicitly seeded "
        "with task_seed=9354. Bounds for the 68 parameters are inherited "
        "unchanged from the t0106/t0112/t0113/t0114 substrate (54-d Bed B "
        "electrophys bounds from t0080 + 14-d morphology bounds from "
        "t0090). Noise replicates inside each evaluation use the 3 "
        "deterministically spawned RNG seeds drawn from "
        "`np.random.SeedSequence(42).spawn(4)`.\n"
    )
    prediction_format_section = (
        "## Prediction Format\n\n"
        f"Gzipped JSONL with one line per evaluated cell "
        f"({seed_summary.n_total_evals:,} lines total). Each line is a JSON "
        "object with fields:\n\n"
        "* `generation`: int, the NSGA-II generation at which this cell was "
        "evaluated (1 = initial LHS population, 2-55 = offspring "
        "generations)\n"
        "* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d "
        "morphology parameter vector\n"
        "* `objective_F_minimised`: list of 2 floats, the NSGA-II objective "
        "vector with sign-flipped maximisation conventions: [-ratio_dsi, "
        "-pd_rate_hz]\n"
        "* `dsi_vector_sum`: float in [0, 1], ratio DSI = "
        "(PD - ND) / (PD + ND), guard-cleaned per S-0102-01\n"
        "* `pd_rate_hz`: float, preferred-direction mean firing rate (Hz) "
        "across the 3 noise replicates\n"
        "* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND "
        "`pd_rate_hz >= 30` (the 2-axis strict criterion)\n"
        "* `legit`: bool, true iff `dsi_vector_sum < 0.9999` — false flags "
        "the silence-guard / single-spike DSI=1.0 ceiling artefact\n\n"
        "Example line (formatted for readability):\n\n"
        "```\n"
        "{\n"
        '  "generation": 54,\n'
        '  "vector_68d": [0.4576, 0.0550, ..., 0.2229],\n'
        '  "objective_F_minimised": [-0.9833, -28.33],\n'
        '  "dsi_vector_sum": 0.9833,\n'
        '  "pd_rate_hz": 28.33,\n'
        '  "joint_pass": false,\n'
        '  "legit": true\n'
        "}\n"
        "```\n"
    )
    metrics_section = (
        "## Metrics\n\n"
        "Headline metrics computed at asset creation time:\n\n"
        "| Metric | Value |\n"
        "|--------|-------|\n"
        f"| Cells evaluated | **{seed_summary.n_total_evals:,}** |\n"
        f"| Generations completed | "
        f"**{seed_summary.n_generations_completed}** of 300 ceiling "
        "(operator stop) |\n"
        f"| Best DSI overall | **{seed_summary.overall_max_dsi:.4f}** "
        "(silence-guard ceiling) |\n"
        f"| Best legit DSI (non-silence-guard) | "
        f"**{seed_summary.best_legit_dsi:.4f}** |\n"
        f"| Best PD-rate | **{seed_summary.best_pd_rate_hz:.2f} Hz** |\n"
        f"| Unique joint-pass cells (DSI >= 0.5 AND PD >= 30) | "
        f"**{seed_summary.n_joint_pass_unique}** |\n"
        f"| Unique LEGIT joint-pass cells (DSI < 0.9999) | "
        f"**{seed_summary.n_joint_pass_legit_unique}** |\n"
        f"| Cells at DSI = 1.0 ceiling (silence-guard) | "
        f"**{seed_summary.n_dsi_eq_one}** |\n"
        f"| Final hypervolume (2-D) | "
        f"**{seed_summary.final_hypervolume:.4f}** |\n"
        f"| Stop trigger | **{seed_summary.stop_trigger}** |\n\n"
        "The 2-axis strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= "
        f"30 Hz) is met by **{seed_summary.n_joint_pass_unique}** unique "
        f"cells across the {seed_summary.n_total_evals:,} evaluations. "
        "Filtering out silence-guard ceiling cells leaves "
        f"**{seed_summary.n_joint_pass_legit_unique}** LEGIT joint-pass "
        "cells.\n"
    )
    main_ideas_section = (
        "## Main Ideas\n\n"
        f"* The run terminated at generation "
        f"{seed_summary.n_generations_completed} via operator stop after the "
        f"HV trajectory visibly plateaued near "
        f"{seed_summary.final_hypervolume:.2f}; the HV-plateau auto-stop was "
        "DISABLED for this run.\n"
        f"* {seed_summary.n_joint_pass_legit_unique} of the "
        f"{seed_summary.n_total_evals:,} evaluated cells cleared the strict "
        "2-axis LEGIT joint-pass corner — adding seed 9354 as the fifth "
        "data point for the S-0112-01 substrate-rate estimate.\n"
        f"* The best legit cell reaches DSI = {seed_summary.best_legit_dsi:.4f} "
        f"and the best PD-rate cell reaches PD = "
        f"{seed_summary.best_pd_rate_hz:.2f} Hz. Per-cell `vector_68d` is "
        "sufficient to re-evaluate any cell without re-running the "
        "optimiser.\n"
        "* Seed 9354 lands in an intermediate yield bucket between the "
        "high-yield t0106 / t0114 seeds and the sparse t0112 / t0113 seeds, "
        "providing useful variance to characterise the substrate-rate "
        "distribution.\n"
    )
    summary_section = (
        "## Summary\n\n"
        f"This asset captures all {seed_summary.n_total_evals:,} NSGA-II "
        f"evaluations from the t0115 random-init 2-objective run with GA "
        f"seed=9354, covering generations 1 through "
        f"{seed_summary.n_generations_completed}. Each cell is a 68-d point "
        "in the Bed B electrophys + procedural morphology parameter space, "
        "evaluated with 2 stimulus directions and 3 noise replicates against "
        "the 2-dimensional objective (ratio DSI, preferred-direction firing "
        "rate). The DSI silence guard from S-0102-01 is active throughout; "
        "the HV-plateau auto-stop is DISABLED.\n\n"
        f"The headline finding is **{seed_summary.n_joint_pass_legit_unique} "
        "unique LEGIT joint-pass cells** — the fifth and final data point "
        "for the S-0112-01 substrate-rate confirmation batch. Best individual "
        f"axes were DSI={seed_summary.best_legit_dsi:.4f} (legit) and "
        f"PD={seed_summary.best_pd_rate_hz:.2f} Hz; final hypervolume "
        f"{seed_summary.final_hypervolume:.4f}.\n\n"
        "Combined with the matched four-other-seed assets (t0106 / t0112 / "
        "t0113 / t0114), this contributes the fifth data point to the "
        "substrate-rate confirmation batch and provides the primary evidence "
        "channel for the 5-seed mean +/- SE bar chart vs Hay 2011 (0.40%) "
        "and Druckmann 2007 (0.10%) literature baselines. Cost watchdog and "
        "operator stop jointly govern run length; the productive NSGA-II "
        "compute cost was $2.39 of the $25 cap.\n"
    )
    return (
        "---\n"
        f'spec_version: "2"\n'
        f'predictions_id: "{PREDICTIONS_ID}"\n'
        f'documented_by_task: "{TASK_ID}"\n'
        f'date_documented: "{PROJECT_DATE}"\n'
        "---\n\n"
        f"# {name}\n\n"
        f"{metadata}\n"
        f"{overview}\n"
        f"{model_section}\n"
        f"{data_section}\n"
        f"{prediction_format_section}\n"
        f"{metrics_section}\n"
        f"{main_ideas_section}\n"
        f"{summary_section}"
    )


# ---------------------------------------------------------------------------
# metrics.json
# ---------------------------------------------------------------------------


def build_metrics_json(*, summary: PerSeedSummary) -> Path:
    common_dims: dict[str, object] = {
        "task_seed": summary.task_seed,
        "init_method": "lhs_random",
        "n_obj": 2,
        "n_directions": 2,
        "dsi_metric": "ratio",
        "dsi_silence_guard_active": True,
        "n_eval_seeds": 3,
        "n_generations_target": 300,
        "n_generations_completed": summary.n_generations_completed,
        "n_cells": summary.n_total_evals,
        "pool_restart_every": 10,
        "hv_plateau_auto_stop_disabled": True,
        "stop_trigger": summary.stop_trigger,
    }
    variants: list[dict[str, object]] = [
        {
            "variant_id": (f"random-init-seed{summary.task_seed}-2dir-noauto-best-legit"),
            "label": (
                f"2-direction NSGA-II seed {summary.task_seed}: best legit DSI "
                "(highest non-silence-guard cell)"
            ),
            "dimensions": {**common_dims, "dsi_subvariant": "best_legit"},
            "metrics": {
                "direction_selectivity_index": round(summary.best_legit_dsi, 4),
            },
        },
        {
            "variant_id": (f"random-init-seed{summary.task_seed}-2dir-noauto-overall-max"),
            "label": (
                f"2-direction NSGA-II seed {summary.task_seed}: overall max "
                "DSI (silence-guard saturated)"
            ),
            "dimensions": {**common_dims, "dsi_subvariant": "overall_max"},
            "metrics": {
                "direction_selectivity_index": round(summary.overall_max_dsi, 4),
            },
        },
        {
            "variant_id": (f"random-init-seed{summary.task_seed}-2dir-noauto-dsi-eq-one"),
            "label": (
                f"2-direction NSGA-II seed {summary.task_seed}: silence-guard "
                "ceiling cell count (cells at DSI = 1.0)"
            ),
            "dimensions": {
                **common_dims,
                "dsi_subvariant": "dsi_eq_one_count",
                "n_dsi_eq_one": int(summary.n_dsi_eq_one),
            },
            "metrics": {
                "direction_selectivity_index": 1.0,
            },
        },
    ]
    payload: dict[str, object] = {"variants": variants}
    METRICS_JSON.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    return METRICS_JSON


# ---------------------------------------------------------------------------
# Example cells for results_detailed.md
# ---------------------------------------------------------------------------


def build_example_cells(
    *,
    ds_t0115: SeedDataset,
) -> tuple[Path, list[dict[str, Any]]]:
    """Pick 10 representative cells from the t0115 evaluation log:
    * 3 top legit joint-pass cells (best legit DSI then best PD)
    * 2 best PD-rate cells
    * 2 silence-guard cells (DSI = 1.0)
    * 3 strict Pareto cells with highest DSI then highest PD"""
    cells = list(ds_t0115.evaluations)
    legit_jp = sorted(
        [c for c in cells if _is_legit_joint_pass(c)],
        key=lambda c: (-float(c["dsi_vector_sum"]), -float(c["pd_rate_hz"])),
    )
    pd_sorted = sorted(
        cells,
        key=lambda c: -float(c["pd_rate_hz"]),
    )
    silence_cells = [c for c in cells if float(c["dsi_vector_sum"]) >= LEGIT_DSI_CEILING]
    pareto = list(ds_t0115.pareto_cells)
    examples: list[dict[str, Any]] = []
    used_keys: set[tuple[float, ...]] = set()

    def _add(c: dict[str, Any], tag: str) -> None:
        k = tuple(c["vector_68d"])
        if k in used_keys:
            return
        used_keys.add(k)
        examples.append(
            {
                "tag": tag,
                "generation": int(c["generation"]),
                "dsi_vector_sum": float(c["dsi_vector_sum"]),
                "pd_rate_hz": float(c["pd_rate_hz"]),
                "objective_F_minimised": list(c["objective_F_minimised"]),
                "vector_68d": list(c["vector_68d"]),
            }
        )

    legit_added = 0
    for c in legit_jp:
        if legit_added >= 3:
            break
        if tuple(c["vector_68d"]) in used_keys:
            continue
        _add(c, f"legit_jp_top_{legit_added + 1}")
        legit_added += 1
    pd_added = 0
    for c in pd_sorted:
        if pd_added >= 2:
            break
        if tuple(c["vector_68d"]) in used_keys:
            continue
        _add(c, f"best_pd_{pd_added + 1}")
        pd_added += 1
    silence_sorted = sorted(
        silence_cells,
        key=lambda c: -float(c["pd_rate_hz"]),
    )
    silence_added = 0
    for c in silence_sorted:
        if silence_added >= 2:
            break
        if tuple(c["vector_68d"]) in used_keys:
            continue
        _add(c, f"silence_guard_{silence_added + 1}")
        silence_added += 1
    pareto_sorted = sorted(
        pareto,
        key=lambda c: (-float(c["dsi_vector_sum"]), -float(c["pd_rate_hz"])),
    )
    pareto_added = 0
    for c in pareto_sorted:
        if pareto_added >= 3:
            break
        if tuple(c["vector_68d"]) in used_keys:
            continue
        _add(c, f"pareto_cell_id_{c['cell_id']}")
        pareto_added += 1
    fill_sources: list[list[dict[str, Any]]] = [pd_sorted, legit_jp, pareto_sorted]
    for src in fill_sources:
        for c in src:
            if len(examples) >= 10:
                break
            if tuple(c["vector_68d"]) in used_keys:
                continue
            tag_kind = (
                "extra_pd"
                if src is pd_sorted
                else "extra_legit_dsi"
                if src is legit_jp
                else f"pareto_cell_id_{c.get('cell_id', '?')}"
            )
            _add(c, f"{tag_kind}_{len(examples) + 1}")
        if len(examples) >= 10:
            break
    examples = examples[:10]
    out_path = DATA_DIR / "example_cells_seed9354.json"
    out_path.write_text(
        json.dumps({"examples": examples}, indent=2),
        encoding="utf-8",
    )
    return out_path, examples


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
    PREDICTIONS_FILES_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[build_results] start at {datetime.now(UTC).isoformat()}")

    print("[build_results] Loading 5-seed datasets...")
    datasets = load_all_five_seeds()

    print("[build_results] Computing per-seed summaries...")
    summaries = {k: _summarize_seed(key=k, ds=ds) for k, ds in datasets.items()}
    for k, s in summaries.items():
        print(
            f"  {k}: jp_unique={s.n_joint_pass_unique}, "
            f"legit_jp_unique={s.n_joint_pass_legit_unique}, "
            f"legit_pct={s.joint_pass_pct:.3f}%, "
            f"best_legit_dsi={s.best_legit_dsi:.4f}, "
            f"best_pd={s.best_pd_rate_hz:.2f} Hz"
        )

    s0115 = summaries["t0115_seed9354"]
    print(
        f"[build_results] t0115 summary: legit_jp_unique="
        f"{s0115.n_joint_pass_legit_unique}, best_legit_dsi="
        f"{s0115.best_legit_dsi:.4f}, best_pd={s0115.best_pd_rate_hz:.2f}"
    )

    print("[build_results] Building predictions asset...")
    pred_jsonl, pred_details, pred_desc = build_predictions_asset(
        seed_summary=s0115,
        evaluations=datasets["t0115_seed9354"].evaluations,
    )
    print(f"  -> {pred_jsonl} ({pred_jsonl.stat().st_size / 1024:.1f} KB)")
    print(f"  -> {pred_details}")
    print(f"  -> {pred_desc}")

    print("[build_results] Building example cells JSON...")
    ex_path, examples = build_example_cells(ds_t0115=datasets["t0115_seed9354"])
    print(f"  -> {ex_path} ({len(examples)} examples)")

    print("[build_results] Chart 1: hv_vs_gen_5seeds.png")
    p1 = chart_hv_vs_gen_5seeds(datasets=datasets)
    print(f"  -> {p1}")

    print("[build_results] Chart 2: pareto_front_5seeds.png")
    p2 = chart_pareto_front_5seeds(datasets=datasets)
    print(f"  -> {p2}")

    print("[build_results] Chart 3: joint_pass_yield_per_gen_5seeds.png")
    p3 = chart_joint_pass_yield_5seeds(datasets=datasets)
    print(f"  -> {p3}")

    print("[build_results] Substrate-rate stats")
    stats = _compute_substrate_stats(summaries=summaries)
    print(f"  rates: {stats.rates_pct}")
    print(f"  mean = {stats.mean_pct:.4f}%, sd = {stats.sd_pct:.4f}%, se = {stats.se_pct:.4f}%")

    print("[build_results] Chart 4: substrate_rate_5seed_with_literature.png")
    p4 = chart_substrate_rate_5seed_with_literature(summaries=summaries, stats=stats)
    print(f"  -> {p4}")

    print("[build_results] CSV: joint_pass_summary_5seeds.csv")
    c1 = csv_joint_pass_summary_5seeds(summaries=summaries)
    print(f"  -> {c1}")

    print("[build_results] CSV: pareto_front_overlap_5seeds.csv")
    c2 = csv_pareto_front_overlap_5seeds(datasets=datasets)
    print(f"  -> {c2}")

    print("[build_results] CSV: substrate_rate_5seed.csv")
    c3 = csv_substrate_rate_5seed(summaries=summaries, stats=stats)
    print(f"  -> {c3}")

    print("[build_results] metrics.json")
    m = build_metrics_json(summary=s0115)
    print(f"  -> {m}")

    print()
    print("[build_results] HEADLINE NUMBERS for results_summary.md:")
    print(f"  task_seed = {s0115.task_seed}")
    print(f"  n_total_evals = {s0115.n_total_evals}")
    print(f"  n_generations_completed = {s0115.n_generations_completed}")
    print(f"  n_joint_pass_unique = {s0115.n_joint_pass_unique}")
    print(f"  n_joint_pass_legit_unique = {s0115.n_joint_pass_legit_unique}")
    print(f"  best_legit_dsi = {s0115.best_legit_dsi:.4f}")
    print(f"  overall_max_dsi = {s0115.overall_max_dsi:.4f}")
    print(f"  n_dsi_eq_one = {s0115.n_dsi_eq_one}")
    print(f"  best_pd_rate_hz = {s0115.best_pd_rate_hz:.4f}")
    print(f"  final_hypervolume = {s0115.final_hypervolume:.4f}")
    print(f"  stop_trigger = {s0115.stop_trigger}")
    print(f"  n_pareto = {len(datasets['t0115_seed9354'].pareto_cells)}")
    print()
    print("[build_results] 5-SEED SUBSTRATE STATS:")
    for k, r in stats.rates_pct.items():
        print(f"  {k}: {r:.4f}%")
    print(f"  mean: {stats.mean_pct:.4f}%")
    print(f"  sd:   {stats.sd_pct:.4f}%")
    print(f"  se:   {stats.se_pct:.4f}%")
    print(f"  Hay 2011 baseline: {HAY_2011_RATE_PCT}%")
    print(f"  Druckmann 2007 baseline: {DRUCKMANN_2007_RATE_PCT}%")

    print(f"[build_results] DONE at {datetime.now(UTC).isoformat()}")


if __name__ == "__main__":
    main()
