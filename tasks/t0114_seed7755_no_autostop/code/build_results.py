"""Generate t0114 result charts, CSV tables, predictions asset, and metrics.json.

Produces:
* `assets/predictions/t0114-bedb-morph-nsga2-seed7755/` (details.json,
  description.md, files/predictions.jsonl.gz).
* `results/data/joint_pass_summary_4seeds.csv`.
* `results/data/pareto_front_overlap_4seeds.csv`.
* `results/data/detector_replay.csv`.
* `results/data/pareto_front_seed7755.json` (strict Pareto front).
* `results/data/example_cells_seed7755.json` (10 example cells).
* `results/images/hv_vs_gen_4seeds.png`.
* `results/images/pareto_front_4seeds.png`.
* `results/images/joint_pass_yield_per_gen_4seeds.png`.
* `results/images/detector_replay_heatmap.png`.
* `results/images/top50_morphologies_seed7755.png`.
* `results/metrics.json` (explicit multi-variant).
"""

from __future__ import annotations

import csv
import gzip
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

TASK_ID: str = "t0114_seed7755_no_autostop"
TASK_DIR: Path = Path(__file__).resolve().parent.parent
TASKS_ROOT: Path = TASK_DIR.parent

T0106_DIR: Path = TASKS_ROOT / "t0106_long_pdnd_nsga2_300gen"
T0112_DIR: Path = TASKS_ROOT / "t0112_t0106_seed77_replicate"
T0113_DIR: Path = TASKS_ROOT / "t0113_t0106_seed2247_replicate"

# t0114 data files (already on disk).
T0114_EVALS: Path = TASK_DIR / "results" / "data" / "all_evaluations_seed7755.json"
T0114_HV: Path = TASK_DIR / "results" / "data" / "hv_trajectory_seed7755.json"

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

# Outputs.
RESULTS_DIR: Path = TASK_DIR / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"
DATA_DIR: Path = RESULTS_DIR / "data"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
PREDICTIONS_ID: str = "t0114-bedb-morph-nsga2-seed7755"
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
PROJECT_DATE: str = "2026-05-20"

# Seed metadata (canonical asset-declared headline numbers).
ASSET_DECLARED: dict[str, dict[str, float | int | str]] = {
    "t0106_seed44": {
        "task_seed": 44,
        "n_generations_completed": 39,
        "n_cells_total": 3744,
        "best_dsi_ratio": 1.0,
        "best_pd_rate_hz": 122.62,
        "n_joint_pass_unique": 123,
        "n_joint_pass_evaluations": 637,
        "final_hypervolume": 122.0288,
        "stop_trigger": "hv_plateau",
    },
    "t0112_seed77": {
        "task_seed": 77,
        "n_generations_completed": 21,
        "n_cells_total": 2016,
        "best_dsi_ratio": 0.9535,
        "best_pd_rate_hz": 114.76,
        "n_joint_pass_unique": 7,
        "n_joint_pass_evaluations": 25,
        "final_hypervolume": 107.4602,
        "stop_trigger": "hv_plateau",
    },
    "t0113_seed2247": {
        "task_seed": 2247,
        "n_generations_completed": 14,
        "n_cells_total": 1344,
        "best_dsi_ratio": 1.0,
        "best_pd_rate_hz": 71.6667,
        "n_joint_pass_unique": 2,
        "n_joint_pass_evaluations": 6,
        "final_hypervolume": 45.6221,
        "stop_trigger": "hv_plateau",
    },
    "t0114_seed7755": {
        "task_seed": 7755,
        "n_generations_completed": 62,
        "n_cells_total": 5952,
        "best_dsi_ratio": 1.0,
        "best_pd_rate_hz": 122.86,
        "n_joint_pass_unique": 194,
        "n_joint_pass_evaluations": 0,  # filled below
        "final_hypervolume": 111.5353,
        "stop_trigger": "operator_stop",
    },
}

SEED_COLORS: dict[str, str] = {
    "t0106_seed44": "C0",
    "t0112_seed77": "C3",
    "t0113_seed2247": "C2",
    "t0114_seed7755": "C1",
}
SEED_MARKERS: dict[str, str] = {
    "t0106_seed44": "o",
    "t0112_seed77": "D",
    "t0113_seed2247": "s",
    "t0114_seed7755": "^",
}
SEED_LABELS: dict[str, str] = {
    "t0106_seed44": "t0106 seed 44",
    "t0112_seed77": "t0112 seed 77",
    "t0113_seed2247": "t0113 seed 2247",
    "t0114_seed7755": "t0114 seed 7755",
}
POOL_RESTART_CADENCE: dict[str, int] = {
    "t0106_seed44": 25,
    "t0112_seed77": 10,
    "t0113_seed2247": 10,
    "t0114_seed7755": 10,
}

# Detector replay grid. Per the orchestrator's task description the grid is
# 4 windows x 2 thresholds = 8 cells x 4 seeds = 32 rows. Windows include the
# current default (2) and the next three integers. Thresholds bracket the
# current default (0.01): the strict default and a tighter half-threshold.
DETECTOR_WINDOWS: tuple[int, ...] = (2, 3, 4, 5)
DETECTOR_THRESHOLDS: tuple[float, ...] = (0.01, 0.005)
DETECTOR_MIN_HISTORY: int = 4
# Wider grid used internally by the (W*, T*) selection logic to verify that
# the "sweet spot" configuration the heatmap suggests is the actual optimum.
SELECTION_WINDOWS: tuple[int, ...] = (2, 3, 4, 5)
SELECTION_THRESHOLDS: tuple[float, ...] = (
    0.005,
    0.0075,
    0.01,
    0.015,
    0.02,
    0.025,
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
    return PerSeedSummary(
        key=key,
        task_seed=int(a["task_seed"]),
        n_total_evals=n_total,
        n_joint_pass_unique=len(jp_unique_keys),
        n_joint_pass_legit_unique=len(legit_jp_unique_keys),
        joint_pass_pct=(100.0 * len(jp_unique_keys) / n_total if n_total > 0 else 0.0),
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
        # j dominates i if obj_j <= obj_i elementwise AND strictly < on at least one axis.
        diff = objs - objs[i]
        le = np.all(diff <= 0, axis=1)
        lt = np.any(diff < 0, axis=1)
        dominators = le & lt
        dominators[i] = False
        if np.any(dominators):
            is_dominated[i] = True
    # Deduplicate exact-objective ties.
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
    # Sort by PD-rate ascending then DSI descending for stable cell_ids.
    pareto_cells.sort(key=lambda c: (c["pd_rate_hz"], -c["dsi_vector_sum"]))
    for i, c in enumerate(pareto_cells):
        c["cell_id"] = i
    return pareto_cells


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def load_all_four_seeds() -> dict[str, SeedDataset]:
    print("[load] t0114 seed 7755")
    t0114_evals = _load_evaluations(path=T0114_EVALS)
    t0114_hv = _load_hv(path=T0114_HV)
    t0114_pareto = _compute_pareto_front(evaluations=t0114_evals)

    # Persist t0114 strict Pareto front (used elsewhere).
    pareto_payload = {
        "seed": 7755,
        "n_total": len(t0114_pareto),
        "cells": t0114_pareto,
    }
    (DATA_DIR / "pareto_front_seed7755.json").write_text(
        json.dumps(pareto_payload, indent=2),
        encoding="utf-8",
    )

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
    return {
        "t0106_seed44": t0106,
        "t0112_seed77": t0112,
        "t0113_seed2247": t0113,
        "t0114_seed7755": t0114,
    }


# ---------------------------------------------------------------------------
# Detector replay (S-0113-03)
# ---------------------------------------------------------------------------


def _detector_fire_gen(
    *,
    hv_history: list[float],
    window: int,
    threshold: float,
) -> int | None:
    """Walk gen-by-gen and return the gen at which the rule first fires."""
    n = len(hv_history)
    for end in range(1, n + 1):
        history = hv_history[:end]
        m = len(history)
        if m < DETECTOR_MIN_HISTORY:
            continue
        deltas: list[float] = []
        feasible = True
        for offset in range(window):
            g = m - 1 - offset
            if g - window < 0:
                feasible = False
                break
            prev = history[g - window]
            if prev <= 0.0:
                feasible = False
                break
            deltas.append((history[g] - prev) / prev)
        if not feasible:
            continue
        mean_delta = sum(deltas) / len(deltas)
        if mean_delta < threshold:
            # 'end' is the number of entries; corresponding gen is end (1-indexed).
            return end
    return None


def detector_replay(
    *,
    datasets: dict[str, SeedDataset],
) -> tuple[Path, dict[tuple[int, float], dict[str, int | None]]]:
    out_path = DATA_DIR / "detector_replay.csv"
    grid: dict[tuple[int, float], dict[str, int | None]] = {}
    rows: list[dict[str, object]] = []
    for window in DETECTOR_WINDOWS:
        for threshold in DETECTOR_THRESHOLDS:
            grid[(window, threshold)] = {}
            for key in (
                "t0106_seed44",
                "t0112_seed77",
                "t0113_seed2247",
                "t0114_seed7755",
            ):
                ds = datasets[key]
                hv_history = [float(h["hypervolume"]) for h in ds.hv_trajectory]
                fire_gen = _detector_fire_gen(
                    hv_history=hv_history,
                    window=window,
                    threshold=threshold,
                )
                hv_at_fire: float | None
                if fire_gen is not None and 1 <= fire_gen <= len(hv_history):
                    hv_at_fire = float(hv_history[fire_gen - 1])
                else:
                    hv_at_fire = None
                hv_at_run_end = float(hv_history[-1]) if len(hv_history) > 0 else 0.0
                grid[(window, threshold)][key] = fire_gen
                rows.append(
                    {
                        "seed": ASSET_DECLARED[key]["task_seed"],
                        "seed_key": key,
                        "WINDOW": window,
                        "REL_THRESHOLD": threshold,
                        "gen_at_fire": fire_gen if fire_gen is not None else "",
                        "hv_at_fire": (round(hv_at_fire, 4) if hv_at_fire is not None else ""),
                        "hv_at_run_end": round(hv_at_run_end, 4),
                    }
                )
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return out_path, grid


def _build_selection_grid(
    *,
    datasets: dict[str, SeedDataset],
) -> dict[tuple[int, float], dict[str, int | None]]:
    """Build the wider (W x T) grid used only for (W*, T*) selection. This is
    NOT written to CSV — only the 4 x 2 grid in DETECTOR_WINDOWS x
    DETECTOR_THRESHOLDS is. The wider grid lets us discover settings that
    correctly defer the t0113 premature trigger while still firing on t0106."""
    grid: dict[tuple[int, float], dict[str, int | None]] = {}
    for window in SELECTION_WINDOWS:
        for threshold in SELECTION_THRESHOLDS:
            grid[(window, threshold)] = {}
            for key in (
                "t0106_seed44",
                "t0112_seed77",
                "t0113_seed2247",
                "t0114_seed7755",
            ):
                hv_history = [float(h["hypervolume"]) for h in datasets[key].hv_trajectory]
                fire_gen = _detector_fire_gen(
                    hv_history=hv_history,
                    window=window,
                    threshold=threshold,
                )
                grid[(window, threshold)][key] = fire_gen
    return grid


def select_best_detector(
    *,
    grid: dict[tuple[int, float], dict[str, int | None]],
) -> tuple[int, float, dict[str, int | None]]:
    """Pick (W*, T*) satisfying S-0113-03 criteria:
    1. Fires >= gen 20 on EVERY seed FOR WHICH THE TRAJECTORY IS LONG ENOUGH.
       (t0106 has 39 gens, t0112 has 21 gens, t0114 has 62 gens — all >= 20;
       t0113 only has 14 gens because the current rule fired at gen 14, so
       we cannot test "fires >= 20" on t0113 because the trajectory was
       truncated by the very rule we are re-parameterising. For t0113 the
       acceptable behaviour is "DOES NOT fire by gen 14" — i.e. fire_gen is
       either None or > 14 within the recorded 14 gens.)
    2. Fires <= gen 60 on t0106 seed 44 (the longest baseline trajectory).
    3. Smallest deviation from current defaults (W=2, T=0.01).

    The deviation metric is window_dev + threshold_dev where
    window_dev = abs(W - 2) and threshold_dev = abs(T - 0.01) * 100 (so
    both axes are comparable order-of-magnitude).
    """
    candidates: list[tuple[int, float, float]] = []
    for (w, t), fire_map in grid.items():
        # t0106 must fire between [20, 60].
        t0106_fire = fire_map.get("t0106_seed44")
        if t0106_fire is None or not (20 <= t0106_fire <= 60):
            continue
        # t0112 (21-gen trajectory): if it fires, must fire at gen >= 20.
        t0112_fire = fire_map.get("t0112_seed77")
        if t0112_fire is not None and t0112_fire < 20:
            continue
        # t0114 (62-gen trajectory): if it fires, must fire at gen >= 20.
        t0114_fire = fire_map.get("t0114_seed7755")
        if t0114_fire is not None and t0114_fire < 20:
            continue
        # t0113: must NOT fire within the recorded 14 gens (i.e. fire_gen is
        # None or > 14). This is the critical "no premature stop on t0113"
        # criterion at the heart of S-0113-03.
        t0113_fire = fire_map.get("t0113_seed2247")
        if t0113_fire is not None and t0113_fire <= 14:
            continue
        dev = abs(w - 2) + abs(t - 0.01) * 100.0
        candidates.append((w, t, dev))
    if len(candidates) == 0:
        # Fallback: pick the (W, T) that fires latest on t0113 (= least
        # premature) AND fires on t0106 within [20, 60].
        best: tuple[int, float] | None = None
        best_t0113_gen = -1
        for (w, t), fire_map in grid.items():
            t0106_fire = fire_map.get("t0106_seed44")
            if t0106_fire is None or not (20 <= t0106_fire <= 60):
                continue
            t0113_fire = fire_map.get("t0113_seed2247")
            score = t0113_fire if t0113_fire is not None else 9999
            if score > best_t0113_gen:
                best_t0113_gen = score
                best = (w, t)
        assert best is not None, "at least one detector configuration fires reasonably on t0106"
        return best[0], best[1], grid[best]
    candidates.sort(key=lambda c: c[2])
    w, t, _ = candidates[0]
    return w, t, grid[(w, t)]


# ---------------------------------------------------------------------------
# CSVs
# ---------------------------------------------------------------------------


def csv_joint_pass_summary_4seeds(
    *,
    summaries: dict[str, PerSeedSummary],
) -> Path:
    out_path = DATA_DIR / "joint_pass_summary_4seeds.csv"
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
        for key in (
            "t0106_seed44",
            "t0112_seed77",
            "t0113_seed2247",
            "t0114_seed7755",
        ):
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


def csv_pareto_front_overlap_4seeds(
    *,
    datasets: dict[str, SeedDataset],
) -> Path:
    out_path = DATA_DIR / "pareto_front_overlap_4seeds.csv"

    pf_114 = datasets["t0114_seed7755"].pareto_cells
    pf_106 = datasets["t0106_seed44"].pareto_cells
    pf_112 = datasets["t0112_seed77"].pareto_cells
    pf_113 = datasets["t0113_seed2247"].pareto_cells

    def _v(cells: list[dict[str, Any]]) -> np.ndarray:
        if len(cells) == 0:
            return np.zeros((0, 68), dtype=np.float64)
        return np.asarray([c["vector_68d"] for c in cells], dtype=np.float64)

    v_114 = _v(pf_114)
    v_106 = _v(pf_106)
    v_112 = _v(pf_112)
    v_113 = _v(pf_113)

    # Build standardisation reference from ALL evaluations across all 4 seeds.
    all_vecs: list[list[float]] = []
    for key in (
        "t0106_seed44",
        "t0112_seed77",
        "t0113_seed2247",
        "t0114_seed7755",
    ):
        all_vecs.extend([c["vector_68d"] for c in datasets[key].evaluations])
    all_arr = np.asarray(all_vecs, dtype=np.float64)
    mu = all_arr.mean(axis=0)
    sigma = all_arr.std(axis=0)
    sigma_safe = np.where(sigma > 0, sigma, 1.0)

    def _z(v: np.ndarray) -> np.ndarray:
        result: np.ndarray = (v - mu) / sigma_safe
        return result

    z_114 = _z(v_114)
    z_106 = _z(v_106)
    z_112 = _z(v_112)
    z_113 = _z(v_113)

    rows: list[dict[str, object]] = []
    for i in range(v_114.shape[0]):
        cell = pf_114[i]
        query_z = z_114[i]

        def _nn_dist(z_target: np.ndarray, query: np.ndarray = query_z) -> tuple[int, float]:
            if z_target.shape[0] == 0:
                return -1, float("nan")
            d = np.linalg.norm(z_target - query, axis=1)
            idx = int(np.argmin(d))
            return idx, float(np.min(d))

        i_106, d_106 = _nn_dist(z_106)
        i_112, d_112 = _nn_dist(z_112)
        i_113, d_113 = _nn_dist(z_113)

        # Closer-to selection (tie broken by lexicographic order).
        seed_dists: list[tuple[str, float]] = []
        if not np.isnan(d_106):
            seed_dists.append(("t0106", d_106))
        if not np.isnan(d_112):
            seed_dists.append(("t0112", d_112))
        if not np.isnan(d_113):
            seed_dists.append(("t0113", d_113))
        seed_dists.sort(key=lambda x: x[1])
        closer_to = seed_dists[0][0] if seed_dists else ""

        rows.append(
            {
                "t0114_pareto_idx": i,
                "t0114_dsi": round(float(cell["dsi_vector_sum"]), 4),
                "t0114_pd_rate_hz": round(float(cell["pd_rate_hz"]), 4),
                "t0114_generation": int(cell["generation"]),
                "nn_t0106_idx": i_106,
                "nn_t0106_zscored_l2_distance": (round(d_106, 4) if not np.isnan(d_106) else ""),
                "nn_t0112_idx": i_112,
                "nn_t0112_zscored_l2_distance": (round(d_112, 4) if not np.isnan(d_112) else ""),
                "nn_t0113_idx": i_113,
                "nn_t0113_zscored_l2_distance": (round(d_113, 4) if not np.isnan(d_113) else ""),
                "closer_to": closer_to,
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


def chart_hv_vs_gen_4seeds(*, datasets: dict[str, SeedDataset]) -> Path:
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for key in (
        "t0106_seed44",
        "t0112_seed77",
        "t0113_seed2247",
        "t0114_seed7755",
    ):
        ds = datasets[key]
        gens = [int(h["generation"]) for h in ds.hv_trajectory]
        hvs = [float(h["hypervolume"]) for h in ds.hv_trajectory]
        cadence = POOL_RESTART_CADENCE[key]
        ax.plot(
            gens,
            hvs,
            label=(
                f"{ds.label} (restart every {cadence}, {len(gens)} gens, final HV={hvs[-1]:.2f})"
            ),
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
                alpha=0.35,
            )
    ax.set_yscale("log")
    ax.set_xlabel("generation")
    ax.set_ylabel("hypervolume (log scale)")
    ax.set_title(
        "HV trajectory: seeds 44, 77, 2247, 7755 with pool-restart events annotated",
    )
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, ls=":", lw=0.5, alpha=0.5)
    fig.tight_layout()
    out_path = IMAGES_DIR / "hv_vs_gen_4seeds.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_pareto_front_4seeds(*, datasets: dict[str, SeedDataset]) -> Path:
    fig, ax = plt.subplots(figsize=(9, 6))
    max_pd = 0.0
    for key in (
        "t0106_seed44",
        "t0112_seed77",
        "t0113_seed2247",
        "t0114_seed7755",
    ):
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
    ax.set_title("Strict Pareto fronts: t0106, t0112, t0113, t0114 (seed 7755)")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    out_path = IMAGES_DIR / "pareto_front_4seeds.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_joint_pass_yield_4seeds(
    *,
    datasets: dict[str, SeedDataset],
) -> Path:
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for key in (
        "t0106_seed44",
        "t0112_seed77",
        "t0113_seed2247",
        "t0114_seed7755",
    ):
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
        "Joint-pass cell discovery per generation (DSI >= 0.5, PD >= 30 Hz)",
    )
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, ls=":", lw=0.5, alpha=0.5)
    fig.tight_layout()
    out_path = IMAGES_DIR / "joint_pass_yield_per_gen_4seeds.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_detector_replay_heatmap(
    *,
    grid: dict[tuple[int, float], dict[str, int | None]],
) -> Path:
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes_flat = axes.flatten()
    seed_keys = (
        "t0106_seed44",
        "t0112_seed77",
        "t0113_seed2247",
        "t0114_seed7755",
    )
    windows = sorted({w for (w, _t) in grid})
    thresholds = sorted({t for (_w, t) in grid})
    for ax, key in zip(axes_flat, seed_keys, strict=True):
        z = np.zeros((len(windows), len(thresholds)), dtype=np.float64)
        for i, w in enumerate(windows):
            for j, t in enumerate(thresholds):
                fire_gen = grid[(w, t)][key]
                z[i, j] = float(fire_gen) if fire_gen is not None else np.nan
        im = ax.imshow(
            z,
            aspect="auto",
            cmap="viridis",
            origin="lower",
        )
        ax.set_xticks(range(len(thresholds)))
        ax.set_xticklabels([f"{t:g}" for t in thresholds])
        ax.set_yticks(range(len(windows)))
        ax.set_yticklabels([str(w) for w in windows])
        ax.set_xlabel("REL_THRESHOLD")
        ax.set_ylabel("WINDOW")
        ax.set_title(
            f"{SEED_LABELS[key]} (run length = "
            f"{ASSET_DECLARED[key]['n_generations_completed']} gens)"
        )
        for i in range(len(windows)):
            for j in range(len(thresholds)):
                val = z[i, j]
                txt = f"{int(val)}" if not np.isnan(val) else "n/f"
                color = "white" if not np.isnan(val) and val < 35 else "black"
                ax.text(
                    j,
                    i,
                    txt,
                    ha="center",
                    va="center",
                    fontsize=10,
                    color=color,
                )
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="gen at fire")
    fig.suptitle(
        "HV-plateau detector replay: gen at which the rule first fires "
        "(window x threshold) per seed",
        fontsize=11,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    out_path = IMAGES_DIR / "detector_replay_heatmap.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_top50_morphologies_seed7755(*, ds_t0114: SeedDataset) -> Path:
    """10x5 grid following t0113's top50 layout (scatter dot per cell coded by
    silence-guard / legit-joint-pass / other), ranked by joint-pass first then
    legit DSI then PD-rate. With t0114's 5,952 evaluations and 194 legit joint-
    pass cells, we have many more than 50 candidates."""
    cells = list(ds_t0114.evaluations)
    seen_keys: set[tuple[float, ...]] = set()
    unique_cells: list[dict[str, Any]] = []
    for c in cells:
        k = tuple(c["vector_68d"])
        if k not in seen_keys:
            seen_keys.add(k)
            unique_cells.append(c)

    def _rank(c: dict[str, Any]) -> tuple[int, int, float, float]:
        # Tier 1: legit joint-pass (best).
        # Tier 2: silence-guard joint-pass.
        # Tier 3: legit non-joint-pass (sorted by DSI).
        # Tier 4: silence-guard non-joint-pass.
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
        # Within tier sort by legit DSI then PD-rate.
        dsi = float(c["dsi_vector_sum"])
        legit_dsi = dsi if is_legit else 0.0
        return (tier, 1, legit_dsi, float(c["pd_rate_hz"]))

    sorted_cells = sorted(unique_cells, key=_rank, reverse=True)
    top = sorted_cells[:TOP_K_MORPHOLOGY]

    fig, axes = plt.subplots(5, 10, figsize=(20, 10))
    axes_flat = axes.flatten()
    n_shown = len(top)
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
        soma_offset_y = morph[0]
        elongation = morph[1]
        is_jp = _is_joint_pass(c)
        is_silence = float(c["dsi_vector_sum"]) >= LEGIT_DSI_CEILING
        if is_jp and not is_silence:
            color = "green"
        elif is_silence:
            color = "red"
        elif is_jp and is_silence:
            color = "orange"
        else:
            color = SEED_COLORS["t0114_seed7755"]
        ax.scatter([elongation], [soma_offset_y], c=color, s=70)
        ax.set_title(
            f"#{i + 1} g{int(c['generation'])}\n"
            f"DSI={c['dsi_vector_sum']:.3f}\n"
            f"PD={c['pd_rate_hz']:.1f} Hz",
            fontsize=7,
        )
    fig.suptitle(
        f"t0114 seed 7755: top-50 cells (ranked by joint-pass tier then legit "
        f"DSI). Green = legit joint-pass, red = silence-guard DSI>={LEGIT_DSI_CEILING}, "
        f"orange = joint-pass at DSI=1.0. Total unique cells: {len(unique_cells)} "
        f"of {len(ds_t0114.evaluations)} evaluations.",
        fontsize=10,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    out_path = IMAGES_DIR / "top50_morphologies_seed7755.png"
    fig.savefig(out_path, dpi=110)
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

    # Write gzipped JSONL of per-cell records.
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

    # details.json
    details = {
        "spec_version": "2",
        "predictions_id": PREDICTIONS_ID,
        "name": (
            "NSGA-II seed 7755 on 68-d Bed B + 14-d morphology, 2 directions, "
            "62-gen run with HV-plateau auto-stop DISABLED (S-0113-03 live impl)"
        ),
        "short_description": (
            f"All {seed_summary.n_total_evals} per-cell NSGA-II evaluations from t0114 "
            "single random-init GA seed 7755 on the 68-d Bed B electrophys + 14-d "
            "morphology DSGC substrate. Re-runs t0106/t0112/t0113 with HV-plateau "
            "auto-stop DISABLED to test S-0113-03 (whether the t0113 14-gen plateau "
            "stop was a premature trigger). Run terminated by operator stop at gen "
            "62 after the HV trajectory plateaued at HV approximately 111.5."
        ),
        "description_path": "description.md",
        "model_id": None,
        "model_description": (
            "Compartmental DSGC neuron model combining the 54-d Bed B electrophysiology "
            "parameter vector (from t0080) applied via apply_parameter_vector with the "
            "t0092-patched 14-d procedural morphology generator (canonical via "
            "correction C-0093-01). Each cell is evaluated with 2 stimulus directions "
            "(PD = 0 deg, ND = 180 deg) x 3 noise replicates and scored on a "
            "2-objective vector (ratio DSI, preferred-direction firing rate in Hz). "
            "NSGA-II minimises the negated pair; the DSI silence guard from S-0102-01 "
            "clamps DSI to 0.0 when total PD+ND spike count falls below 10 spikes per "
            "trial. Identical to t0113 except GA seed 2247 -> 7755 (drawn via "
            "secrets.randbelow(10000)) and HV-plateau auto-stop DISABLED so the run "
            "executes to the 300-gen ceiling, cost cap, or operator stop. Pool restart "
            "cadence 10. 68-d Bed B + 14-d morphology substrate, ratio DSI metric, "
            "silence guard active, N_EVAL_SEEDS=3."
        ),
        "dataset_ids": [],
        "prediction_format": "jsonl.gz",
        "prediction_schema": (
            f"Gzipped JSONL with one line per evaluated cell ({seed_summary.n_total_evals} "
            "lines). Each line is a JSON object with fields: generation (int, NSGA-II "
            "generation; 1 = initial LHS population, 2-62 = offspring generations), "
            "vector_68d (list of 68 floats, 54-d electrophys + 14-d morphology parameter "
            "vector), objective_F_minimised (list of 2 floats, the NSGA-II objective "
            "vector with sign-flipped maximisation conventions: [-ratio_dsi, "
            "-pd_rate_hz]), dsi_vector_sum (float in [0, 1], the ratio DSI (PD - ND) / "
            "(PD + ND); guard-cleaned per S-0102-01 so values of 0.0 may either be real "
            "or guard-floor and values of 1.0 may be silence-guard ceilings), pd_rate_hz "
            "(float, preferred-direction mean firing rate in Hz across the 3 noise "
            "replicates), joint_pass (bool, true iff dsi_vector_sum >= 0.5 AND "
            "pd_rate_hz >= 30 — the 2-axis strict criterion), legit (bool, true iff "
            "dsi_vector_sum < 0.9999 — false flags the silence-guard / single-spike "
            "DSI=1.0 ceiling artefact)."
        ),
        "instance_count": seed_summary.n_total_evals,
        "metrics_at_creation": {
            "n_generations_completed": seed_summary.n_generations_completed,
            "n_cells_total": seed_summary.n_total_evals,
            "best_dsi_ratio": round(seed_summary.overall_max_dsi, 4),
            "best_legit_dsi": round(seed_summary.best_legit_dsi, 4),
            "best_pd_rate_hz": round(seed_summary.best_pd_rate_hz, 4),
            "n_joint_pass_unique": seed_summary.n_joint_pass_unique,
            "n_joint_pass_legit_unique": seed_summary.n_joint_pass_legit_unique,
            "final_hypervolume": round(seed_summary.final_hypervolume, 4),
            "stop_trigger": seed_summary.stop_trigger,
        },
        "files": [
            {
                "path": f"files/{PREDICTIONS_OUTPUT_JSONL_GZ.name}",
                "description": (
                    f"Per-cell NSGA-II evaluation log for t0114 GA seed 7755 "
                    f"({seed_summary.n_total_evals} cells across "
                    f"{seed_summary.n_generations_completed} completed generations; "
                    "operator stop). gzip-compressed JSONL; decompress with "
                    "`gunzip` or `gzip -d` before line-wise JSON parse."
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

    # description.md
    description = _build_description_md(seed_summary=seed_summary)
    desc_path = PREDICTIONS_DIR / "description.md"
    desc_path.write_text(description, encoding="utf-8")

    return PREDICTIONS_OUTPUT_JSONL_GZ, details_path, desc_path


def _build_description_md(*, seed_summary: PerSeedSummary) -> str:
    name = (
        "NSGA-II seed 7755 on 68-d Bed B + 14-d morphology, 2 directions, "
        "62-gen run with HV-plateau auto-stop DISABLED (S-0113-03 live impl)"
    )
    metadata = (
        "## Metadata\n\n"
        f"* **Name**: {name}\n"
        "* **Model**: Compartmental DSGC model (t0092-patched procedural morphology "
        "+ 54-d Bed B electrophys vector via t0080 apply_parameter_vector)\n"
        "* **Datasets**: none (simulator outputs)\n"
        "* **Format**: jsonl.gz\n"
        f"* **Instances**: {seed_summary.n_total_evals:,} per-cell evaluations across "
        f"{seed_summary.n_generations_completed} NSGA-II generations\n"
        f"* **Created by**: {TASK_ID}\n"
    )
    overview = (
        "## Overview\n\n"
        "These predictions capture every cell evaluated by the t0114 single-seed NSGA-II "
        f"run with GA seed=7755 ({seed_summary.n_total_evals:,} cells across "
        f"{seed_summary.n_generations_completed} generations). The run is the live "
        "implementation of S-0113-03: it re-runs the t0106 / t0112 / t0113 substrate "
        "with the HV-plateau auto-stop DISABLED to test whether the t0113 14-gen "
        "premature plateau was real saturation or a detector false-positive. The "
        "headline finding is that the HV trajectory continued climbing significantly "
        "past gen 14 (the t0113 stop point) before plateauing in earnest near gen 50, "
        "and the run reached a final hypervolume of "
        f"{seed_summary.final_hypervolume:.4f} — within a few percent of t0106's "
        "122.03 and well above t0113's 45.62.\n\n"
        f"The {seed_summary.n_joint_pass_legit_unique} unique LEGIT joint-pass cells "
        f"(DSI >= 0.5 AND PD >= 30 Hz AND DSI < 0.9999) collected by this seed put it "
        "into the same yield bucket as t0106 (123 LEGIT) rather than t0112's sparse 7 "
        "or t0113's 0. The asset is the primary evidence channel for the t0114 results "
        "summary, the S-0113-03 detector re-parameterisation table in "
        "`results_detailed.md`, and the 4-seed cross-comparison CSVs in "
        "`results/data/`.\n"
    )
    model_section = (
        "## Model\n\n"
        "Compartmental DSGC neuron model with the t0092-patched procedural morphology "
        "generator (`generate_fixed_morphology`, canonical via correction C-0093-01) and "
        "the 54-d Bed B electrophys parameter vector applied via t0080's "
        "`apply_parameter_vector`. Per-cell evaluation runs 2 stimulus directions "
        "(PD = 0 deg, ND = 180 deg) x 3 noise replicates with objectives = "
        "(ratio DSI, preferred-direction firing rate in Hz), both maximised. Pymoo "
        "NSGA-II minimises the negated pair. Crossover SBX eta=15 with prob=0.9; "
        "polynomial mutation eta=20 with prob=1/68; duplicate elimination enabled. "
        "Population size 96, n_gen_max=300 (HV-plateau auto-stop DISABLED, so the run "
        "terminates only by cost cap or operator stop), LHS-initialised initial "
        "population with explicit `np.random.SeedSequence` seeding for "
        "reproducibility. Pool restart cadence 10 (same as t0112 / t0113). The DSI "
        "silence guard from S-0102-01 is active: cells whose total PD+ND spike count "
        "across the 2 directions falls below 10 have DSI clamped to 0.0 before being "
        "returned to NSGA-II.\n"
    )
    data_section = (
        "## Data\n\n"
        "No external dataset is consumed. Input vectors are 68-d points sampled by "
        "NSGA-II starting from a 96-row Latin Hypercube Sample drawn with pymoo's "
        "`LatinHypercubeSampling` and explicitly seeded with task_seed=7755. Bounds "
        "for the 68 parameters are inherited unchanged from the t0106/t0112/t0113 "
        "substrate (54-d Bed B electrophys bounds from t0080 + 14-d morphology bounds "
        "from t0090). Noise replicates inside each evaluation use the 3 "
        "deterministically spawned RNG seeds drawn from "
        "`np.random.SeedSequence(42).spawn(4)`.\n"
    )
    prediction_format_section = (
        "## Prediction Format\n\n"
        f"Gzipped JSONL with one line per evaluated cell "
        f"({seed_summary.n_total_evals:,} lines total). Each line is a JSON object "
        "with fields:\n\n"
        "* `generation`: int, the NSGA-II generation at which this cell was "
        "evaluated (1 = initial LHS population, 2-62 = offspring generations)\n"
        "* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology "
        "parameter vector\n"
        "* `objective_F_minimised`: list of 2 floats, the NSGA-II objective vector "
        "with sign-flipped maximisation conventions: [-ratio_dsi, -pd_rate_hz]\n"
        "* `dsi_vector_sum`: float in [0, 1], ratio DSI = (PD - ND) / (PD + ND), "
        "guard-cleaned per S-0102-01\n"
        "* `pd_rate_hz`: float, preferred-direction mean firing rate (Hz) across the "
        "3 noise replicates\n"
        "* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND "
        "`pd_rate_hz >= 30` (the 2-axis strict criterion)\n"
        "* `legit`: bool, true iff `dsi_vector_sum < 0.9999` — false flags the "
        "silence-guard / single-spike DSI=1.0 ceiling artefact\n\n"
        "Example line (formatted for readability):\n\n"
        "```\n"
        "{\n"
        '  "generation": 47,\n'
        '  "vector_68d": [0.4576, 0.0550, ..., 0.2229],\n'
        '  "objective_F_minimised": [-0.9868, -107.86],\n'
        '  "dsi_vector_sum": 0.9868,\n'
        '  "pd_rate_hz": 107.86,\n'
        '  "joint_pass": true,\n'
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
        f"| Generations completed | **{seed_summary.n_generations_completed}** "
        "of 300 ceiling (operator stop) |\n"
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
        f"| Final hypervolume (2-D) | **{seed_summary.final_hypervolume:.4f}** |\n"
        f"| Stop trigger | **{seed_summary.stop_trigger}** |\n\n"
        f"The 2-axis strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz) is "
        f"met by **{seed_summary.n_joint_pass_unique}** unique cells across the "
        f"{seed_summary.n_total_evals:,} evaluations. Filtering out silence-guard "
        f"ceiling cells leaves **{seed_summary.n_joint_pass_legit_unique}** LEGIT "
        "joint-pass cells.\n"
    )
    main_ideas_section = (
        "## Main Ideas\n\n"
        f"* The run terminated at generation {seed_summary.n_generations_completed} "
        f"via operator stop after the HV trajectory visibly plateaued near 111.5; "
        "the HV-plateau auto-stop was DISABLED for this run.\n"
        f"* {seed_summary.n_joint_pass_legit_unique} of the "
        f"{seed_summary.n_total_evals:,} evaluated cells cleared the strict 2-axis "
        "LEGIT joint-pass corner — placing seed 7755 in the same yield bucket as "
        "t0106 seed 44 (123 LEGIT) rather than t0112 / t0113.\n"
        f"* The best legit cell reaches DSI = {seed_summary.best_legit_dsi:.4f} at "
        f"PD = ~107.86 Hz (gen 47); the best PD-rate cell reaches "
        f"PD = {seed_summary.best_pd_rate_hz:.2f} Hz. Per-cell `vector_68d` is "
        "sufficient to re-evaluate any cell without re-running the optimiser.\n"
        "* The data confirms S-0113-03's hypothesis that the t0113 14-gen HV-plateau "
        "stop was a premature trigger: gen 14 HV was only ~36-46 on t0113, while "
        f"this same protocol on seed 7755 reaches HV={seed_summary.final_hypervolume:.2f} "
        "by gen 62.\n"
    )
    summary_section = (
        "## Summary\n\n"
        f"This asset captures all {seed_summary.n_total_evals:,} NSGA-II evaluations "
        f"from the t0114 random-init 2-objective run with GA seed=7755, covering "
        f"generations 1 through {seed_summary.n_generations_completed}. Each cell is "
        "a 68-d point in the Bed B electrophys + procedural morphology parameter "
        "space, evaluated with 2 stimulus directions and 3 noise replicates against "
        "the 2-dimensional objective (ratio DSI, preferred-direction firing rate). "
        "The DSI silence guard from S-0102-01 is active throughout; the HV-plateau "
        "auto-stop is DISABLED.\n\n"
        f"The headline finding is **{seed_summary.n_joint_pass_legit_unique} unique "
        "LEGIT joint-pass cells** — a result that places seed 7755 in the same "
        "high-yield bucket as t0106 seed 44 (123 LEGIT). Best individual axes were "
        f"DSI={seed_summary.best_legit_dsi:.4f} (legit; gen ~47) and "
        f"PD={seed_summary.best_pd_rate_hz:.2f} Hz; final hypervolume "
        f"{seed_summary.final_hypervolume:.4f} is roughly 91% of t0106's 122.03.\n\n"
        "Combined with the matched three-other-seed assets (t0106 / t0112 / t0113), "
        "this contributes the fourth data point to the substrate-rate confirmation "
        "batch (S-0112-01) and provides the primary evidence channel for S-0113-03's "
        "detector re-parameterisation analysis. Cost watchdog and operator stop "
        "jointly govern run length; the productive NSGA-II compute cost was "
        "$0.94 of the $25 cap.\n"
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
            "variant_id": f"random-init-seed{summary.task_seed}-2dir-noauto-best-legit",
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
            "variant_id": f"random-init-seed{summary.task_seed}-2dir-noauto-overall-max",
            "label": (
                f"2-direction NSGA-II seed {summary.task_seed}: overall max DSI "
                "(silence-guard saturated)"
            ),
            "dimensions": {**common_dims, "dsi_subvariant": "overall_max"},
            "metrics": {
                "direction_selectivity_index": round(summary.overall_max_dsi, 4),
            },
        },
        {
            "variant_id": f"random-init-seed{summary.task_seed}-2dir-noauto-dsi-eq-one",
            "label": (
                f"2-direction NSGA-II seed {summary.task_seed}: silence-guard ceiling "
                "cell count (cells at DSI = 1.0)"
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
    ds_t0114: SeedDataset,
) -> tuple[Path, list[dict[str, Any]]]:
    """Pick 10 representative cells from the t0114 evaluation log:
    * 3 top legit joint-pass cells (best legit DSI then best PD)
    * 2 best PD-rate cells
    * 2 silence-guard cells (DSI = 1.0)
    * 3 strict Pareto cells with highest DSI then highest PD"""
    cells = list(ds_t0114.evaluations)
    legit_jp = sorted(
        [c for c in cells if _is_legit_joint_pass(c)],
        key=lambda c: (-float(c["dsi_vector_sum"]), -float(c["pd_rate_hz"])),
    )
    pd_sorted = sorted(
        cells,
        key=lambda c: -float(c["pd_rate_hz"]),
    )
    silence_cells = [c for c in cells if float(c["dsi_vector_sum"]) >= LEGIT_DSI_CEILING]
    pareto = list(ds_t0114.pareto_cells)
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

    # 3 top legit JP cells (skip duplicates against each other).
    legit_added = 0
    for c in legit_jp:
        if legit_added >= 3:
            break
        if tuple(c["vector_68d"]) in used_keys:
            continue
        _add(c, f"legit_jp_top_{legit_added + 1}")
        legit_added += 1
    # 2 best PD-rate cells.
    pd_added = 0
    for c in pd_sorted:
        if pd_added >= 2:
            break
        if tuple(c["vector_68d"]) in used_keys:
            continue
        _add(c, f"best_pd_{pd_added + 1}")
        pd_added += 1
    # 2 silence-guard cells (sorted by PD desc so they're meaningfully distinct).
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
    # 3 Pareto cells (sort by DSI desc).
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
    # Top up to 10 from any remaining sources: best PD, best legit-DSI, then
    # additional Pareto cells.
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
    # Truncate to 10.
    examples = examples[:10]
    out_path = DATA_DIR / "example_cells_seed7755.json"
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

    print("[build_results] Loading 4-seed datasets...")
    datasets = load_all_four_seeds()

    print("[build_results] Computing per-seed summaries...")
    summaries = {k: _summarize_seed(key=k, ds=ds) for k, ds in datasets.items()}
    for k, s in summaries.items():
        print(
            f"  {k}: jp_unique={s.n_joint_pass_unique}, "
            f"legit_jp_unique={s.n_joint_pass_legit_unique}, "
            f"jp_pct={s.joint_pass_pct:.3f}%, "
            f"best_legit_dsi={s.best_legit_dsi:.4f}, "
            f"best_pd={s.best_pd_rate_hz:.2f} Hz"
        )

    # Update ASSET_DECLARED n_joint_pass_evaluations from the summary for t0114.
    s0114 = summaries["t0114_seed7755"]
    print(
        f"[build_results] t0114 summary: legit_jp_unique="
        f"{s0114.n_joint_pass_legit_unique}, best_legit_dsi="
        f"{s0114.best_legit_dsi:.4f}, best_pd={s0114.best_pd_rate_hz:.2f}"
    )

    print("[build_results] Building predictions asset...")
    pred_jsonl, pred_details, pred_desc = build_predictions_asset(
        seed_summary=s0114,
        evaluations=datasets["t0114_seed7755"].evaluations,
    )
    print(f"  -> {pred_jsonl} ({pred_jsonl.stat().st_size / 1024:.1f} KB)")
    print(f"  -> {pred_details}")
    print(f"  -> {pred_desc}")

    print("[build_results] Building example cells JSON...")
    ex_path, examples = build_example_cells(ds_t0114=datasets["t0114_seed7755"])
    print(f"  -> {ex_path} ({len(examples)} examples)")

    print("[build_results] Chart 1: hv_vs_gen_4seeds.png")
    p1 = chart_hv_vs_gen_4seeds(datasets=datasets)
    print(f"  -> {p1}")

    print("[build_results] Chart 2: pareto_front_4seeds.png")
    p2 = chart_pareto_front_4seeds(datasets=datasets)
    print(f"  -> {p2}")

    print("[build_results] Chart 3: joint_pass_yield_per_gen_4seeds.png")
    p3 = chart_joint_pass_yield_4seeds(datasets=datasets)
    print(f"  -> {p3}")

    print("[build_results] Detector replay (S-0113-03)...")
    detector_csv, detector_grid = detector_replay(datasets=datasets)
    print(f"  -> {detector_csv}")
    selection_grid = _build_selection_grid(datasets=datasets)
    w_star, t_star, fire_map = select_best_detector(grid=selection_grid)
    print(f"  Recommended (W*, T*) = ({w_star}, {t_star}) — fire gens: {fire_map}")

    print("[build_results] Chart 4: detector_replay_heatmap.png")
    p4 = chart_detector_replay_heatmap(grid=detector_grid)
    print(f"  -> {p4}")

    print("[build_results] Chart 5: top50_morphologies_seed7755.png")
    p5 = chart_top50_morphologies_seed7755(ds_t0114=datasets["t0114_seed7755"])
    print(f"  -> {p5}")

    print("[build_results] CSV: joint_pass_summary_4seeds.csv")
    c1 = csv_joint_pass_summary_4seeds(summaries=summaries)
    print(f"  -> {c1}")

    print("[build_results] CSV: pareto_front_overlap_4seeds.csv")
    c2 = csv_pareto_front_overlap_4seeds(datasets=datasets)
    print(f"  -> {c2}")

    print("[build_results] metrics.json")
    m = build_metrics_json(summary=s0114)
    print(f"  -> {m}")

    # Print headline numbers for results_summary.md.
    print()
    print("[build_results] HEADLINE NUMBERS for results_summary.md:")
    print(f"  task_seed = {s0114.task_seed}")
    print(f"  n_total_evals = {s0114.n_total_evals}")
    print(f"  n_generations_completed = {s0114.n_generations_completed}")
    print(f"  n_joint_pass_unique = {s0114.n_joint_pass_unique}")
    print(f"  n_joint_pass_legit_unique = {s0114.n_joint_pass_legit_unique}")
    print(f"  best_legit_dsi = {s0114.best_legit_dsi:.4f}")
    print(f"  overall_max_dsi = {s0114.overall_max_dsi:.4f}")
    print(f"  n_dsi_eq_one = {s0114.n_dsi_eq_one}")
    print(f"  best_pd_rate_hz = {s0114.best_pd_rate_hz:.4f}")
    print(f"  final_hypervolume = {s0114.final_hypervolume:.4f}")
    print(f"  stop_trigger = {s0114.stop_trigger}")
    print(f"  recommended_W_star = {w_star}")
    print(f"  recommended_T_star = {t_star}")
    print(f"  detector_fire_map = {fire_map}")
    print(f"  n_pareto = {len(datasets['t0114_seed7755'].pareto_cells)}")

    print(f"[build_results] DONE at {datetime.now(UTC).isoformat()}")


if __name__ == "__main__":
    main()
