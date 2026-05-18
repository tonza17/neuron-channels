"""Parallel driver for the 10-cell x 8-direction polar evaluation.

Runs ``evaluate_68d_vector`` on all 10 selected cells in parallel using a
``ProcessPoolExecutor`` with one worker per cell. Designed for the Vast.ai
EPYC instance where 10+ effective cores are available.

Writes ``results/data/per_cell_polar_eval.json`` with the same schema as
the original ``eval_polar.py`` so downstream plotters and asset builders
do not need changes.
"""

from __future__ import annotations

import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from tasks.t0107_t0106_polar_8dir_recheck.code.evaluator import (
    evaluate_68d_vector,
)
from tasks.t0107_t0106_polar_8dir_recheck.code.paths import (
    CODE_DIR,
    RESULTS_DATA_DIR,
    ensure_directories,
)

SELECTED_CELLS_JSON: Path = CODE_DIR / "selected_cells.json"
PER_CELL_POLAR_JSON: Path = RESULTS_DATA_DIR / "per_cell_polar_eval.json"

N_DIRECTIONS_T0107: int = 8
EVAL_SEEDS_T0107: list[int] = [111, 222, 333]
PD_ANGLE_DEG: float = 0.0
ND_ANGLE_DEG: float = 180.0
ANGLE_TOL_DEG: float = 1e-6
MAX_WORKERS: int = 10


@dataclass(frozen=True, slots=True)
class CellRecord:
    t0106_rank: int
    t0106_generation: int
    t0106_dsi: float
    t0106_pd_hz: float
    vector_68d: tuple[float, ...]


def _load_cells(*, path: Path) -> list[CellRecord]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cells: list[dict[str, object]] = payload["cells"]  # type: ignore[index]
    out: list[CellRecord] = []
    for c in cells:
        out.append(
            CellRecord(
                t0106_rank=int(c["t0106_rank"]),  # type: ignore[arg-type]
                t0106_generation=int(c["t0106_generation"]),  # type: ignore[arg-type]
                t0106_dsi=float(c["t0106_dsi"]),  # type: ignore[arg-type]
                t0106_pd_hz=float(c["t0106_pd_hz"]),  # type: ignore[arg-type]
                vector_68d=tuple(float(x) for x in c["vector_68d"]),  # type: ignore[arg-type]
            )
        )
    return out


def _vector_sum_dsi_from_rates(
    *,
    angles_deg: list[float],
    rates_hz: list[float],
) -> float:
    if len(rates_hz) == 0:
        return 0.0
    total_x: float = 0.0
    total_y: float = 0.0
    total_r: float = 0.0
    for a, r in zip(angles_deg, rates_hz, strict=True):
        rad = np.deg2rad(a)
        total_x += r * float(np.cos(rad))
        total_y += r * float(np.sin(rad))
        total_r += r
    if total_r <= 1e-12:
        return 0.0
    return float(np.hypot(total_x, total_y) / total_r)


def _find_rate_at_angle(
    *,
    angles_deg: list[float],
    rates_hz: list[float],
    target_angle_deg: float,
) -> float:
    for a, r in zip(angles_deg, rates_hz, strict=True):
        if abs(a - target_angle_deg) < ANGLE_TOL_DEG:
            return r
    raise ValueError(f"angle {target_angle_deg} not found in {angles_deg}")


def _ratio_dsi(*, pd_rate_hz: float, nd_rate_hz: float) -> float:
    denom = pd_rate_hz + nd_rate_hz
    if denom <= 1e-12:
        return 0.0
    return float((pd_rate_hz - nd_rate_hz) / denom)


# Top-level worker function (must be top-level for pickling).
def _worker_evaluate(
    *,
    t0106_rank: int,
    t0106_generation: int,
    t0106_dsi: float,
    t0106_pd_hz: float,
    vector_68d: tuple[float, ...],
) -> dict[str, object]:
    t_start = time.time()
    vec = np.array(vector_68d, dtype=np.float64)
    result = evaluate_68d_vector(
        vector_68d=vec,
        eval_seeds=EVAL_SEEDS_T0107,
        n_directions=N_DIRECTIONS_T0107,
    )
    elapsed = time.time() - t_start
    rates: list[float] = list(result.per_direction_rates_hz)
    angles: list[float] = list(result.per_direction_angles_deg)
    if len(rates) == 0:
        dsi_vsum: float = 0.0
        pd_at_0: float = 0.0
        nd_at_180: float = 0.0
        ratio_sanity: float = 0.0
    else:
        dsi_vsum = _vector_sum_dsi_from_rates(angles_deg=angles, rates_hz=rates)
        pd_at_0 = _find_rate_at_angle(
            angles_deg=angles, rates_hz=rates, target_angle_deg=PD_ANGLE_DEG
        )
        nd_at_180 = _find_rate_at_angle(
            angles_deg=angles, rates_hz=rates, target_angle_deg=ND_ANGLE_DEG
        )
        ratio_sanity = _ratio_dsi(pd_rate_hz=pd_at_0, nd_rate_hz=nd_at_180)
    return {
        "t0106_rank": t0106_rank,
        "t0106_generation": t0106_generation,
        "t0106_dsi": t0106_dsi,
        "t0106_pd_hz": t0106_pd_hz,
        "vector_68d": list(vector_68d),
        "angles_deg": angles,
        "per_direction_rates_hz": rates,
        "t0107_dsi_8dir_vsum": dsi_vsum,
        "t0107_pd_at_0deg": pd_at_0,
        "t0107_nd_at_180deg": nd_at_180,
        "t0107_dsi_2dir_ratio_sanity": ratio_sanity,
        "t0107_eval_seeds": EVAL_SEEDS_T0107,
        "t0107_n_directions": N_DIRECTIONS_T0107,
        "t0107_eval_elapsed_s": elapsed,
        "t0107_n_errors": int(result.n_errors),
        "t0107_n_trials": int(result.n_trials),
    }


def main() -> None:
    ensure_directories()
    cells = _load_cells(path=SELECTED_CELLS_JSON)
    n = len(cells)
    print(
        f"Parallel eval: {n} cells x {N_DIRECTIONS_T0107} directions x "
        f"{len(EVAL_SEEDS_T0107)} seeds; max_workers={MAX_WORKERS}",
        flush=True,
    )
    t_start = time.time()
    records: list[dict[str, object]] = []
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(
                _worker_evaluate,
                t0106_rank=c.t0106_rank,
                t0106_generation=c.t0106_generation,
                t0106_dsi=c.t0106_dsi,
                t0106_pd_hz=c.t0106_pd_hz,
                vector_68d=c.vector_68d,
            ): c
            for c in cells
        }
        for n_done, fut in enumerate(as_completed(futures), start=1):
            c = futures[fut]
            try:
                rec = fut.result()
            except Exception as exc:  # noqa: BLE001
                print(
                    f"  cell rank={c.t0106_rank} FAILED: {type(exc).__name__}: {exc}",
                    flush=True,
                )
                rec = {
                    "t0106_rank": c.t0106_rank,
                    "t0106_generation": c.t0106_generation,
                    "t0106_dsi": c.t0106_dsi,
                    "t0106_pd_hz": c.t0106_pd_hz,
                    "vector_68d": list(c.vector_68d),
                    "angles_deg": [],
                    "per_direction_rates_hz": [],
                    "t0107_dsi_8dir_vsum": 0.0,
                    "t0107_pd_at_0deg": 0.0,
                    "t0107_nd_at_180deg": 0.0,
                    "t0107_dsi_2dir_ratio_sanity": 0.0,
                    "t0107_eval_seeds": EVAL_SEEDS_T0107,
                    "t0107_n_directions": N_DIRECTIONS_T0107,
                    "t0107_eval_elapsed_s": 0.0,
                    "t0107_n_errors": -1,
                    "t0107_n_trials": 0,
                    "t0107_error": f"{type(exc).__name__}: {exc}",
                }
            records.append(rec)
            wall = time.time() - t_start
            print(
                f"  [{n_done:2d}/{n}] rank={int(rec['t0106_rank']):2d}  "
                f"vsum-DSI={float(rec['t0107_dsi_8dir_vsum']):.3f}  "
                f"PD@0={float(rec['t0107_pd_at_0deg']):6.2f} Hz  "
                f"ratio-DSI={float(rec['t0107_dsi_2dir_ratio_sanity']):.3f}  "
                f"(cell={float(rec['t0107_eval_elapsed_s']):.1f}s, "
                f"wall={wall:.1f}s)",
                flush=True,
            )

    # Sort by rank ascending for deterministic output.
    records.sort(key=lambda r: int(r["t0106_rank"]))
    total_elapsed = time.time() - t_start
    payload: dict[str, object] = {
        "n_directions": N_DIRECTIONS_T0107,
        "eval_seeds": EVAL_SEEDS_T0107,
        "max_workers": MAX_WORKERS,
        "wall_clock_total_s": total_elapsed,
        "evaluations": records,
    }
    PER_CELL_POLAR_JSON.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nWrote {PER_CELL_POLAR_JSON}", flush=True)
    print(f"Total wall clock: {total_elapsed:.1f} s ({total_elapsed / 60:.2f} min)", flush=True)


if __name__ == "__main__":
    main()
