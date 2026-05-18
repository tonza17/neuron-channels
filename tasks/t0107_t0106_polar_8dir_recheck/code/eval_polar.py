"""Re-evaluate 10 sampled t0106 cells at 8 directions for polar plots.

For each of the 10 cells in `code/selected_cells.json`:

* Call `evaluator.evaluate_68d_vector(vector_68d, n_directions=8, eval_seeds=[111, 222, 333])`.
* Extract the per-direction firing rates (Hz) from the result.
* Compute the 8-direction vector-sum DSI from the firing rates.
* Compute a 2-direction ratio DSI sanity check from the 0/180-degree rates.

Writes `results/data/per_cell_polar_eval.json` with one record per cell.
"""

from __future__ import annotations

import json
import time
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
    raise ValueError(f"angle {target_angle_deg} not found in angles_deg list {angles_deg}")


def _ratio_dsi(*, pd_rate_hz: float, nd_rate_hz: float) -> float:
    denom = pd_rate_hz + nd_rate_hz
    if denom <= 1e-12:
        return 0.0
    return float((pd_rate_hz - nd_rate_hz) / denom)


CHECKPOINT_JSON: Path = RESULTS_DATA_DIR / "per_cell_polar_eval.checkpoint.json"


def _load_checkpoint() -> dict[str, object]:
    if not CHECKPOINT_JSON.exists():
        return {
            "n_directions": N_DIRECTIONS_T0107,
            "eval_seeds": EVAL_SEEDS_T0107,
            "wall_clock_total_s": 0.0,
            "evaluations": [],
        }
    return json.loads(CHECKPOINT_JSON.read_text(encoding="utf-8"))


def _write_checkpoint(*, payload: dict[str, object]) -> None:
    CHECKPOINT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ensure_directories()
    cells = _load_cells(path=SELECTED_CELLS_JSON)
    print(f"Evaluating {len(cells)} cells at {N_DIRECTIONS_T0107} directions")
    print(f"  eval_seeds: {EVAL_SEEDS_T0107}")
    print(f"  expected angles (deg): {[d * 45 for d in range(8)]}")

    payload = _load_checkpoint()
    records: list[dict[str, object]] = list(payload["evaluations"])  # type: ignore[arg-type]
    done_ranks: set[int] = {int(r["t0106_rank"]) for r in records}  # type: ignore[arg-type]
    if len(done_ranks) > 0:
        print(f"  Resuming from checkpoint: {len(done_ranks)} cells already done")

    t_run_start = time.time()
    accum_elapsed: float = float(payload.get("wall_clock_total_s", 0.0))  # type: ignore[arg-type]
    for i, c in enumerate(cells):
        if c.t0106_rank in done_ranks:
            print(f"  cell {i + 1}/{len(cells)}  rank={c.t0106_rank:2d}  SKIP (checkpoint)")
            continue
        print(
            f"  cell {i + 1}/{len(cells)}  rank={c.t0106_rank:2d}  "
            f"DSI(t0106)={c.t0106_dsi:.3f}  PD(t0106)={c.t0106_pd_hz:.1f} Hz",
            flush=True,
        )
        t_cell = time.time()
        vec = np.array(c.vector_68d, dtype=np.float64)
        result = evaluate_68d_vector(
            vector_68d=vec,
            eval_seeds=EVAL_SEEDS_T0107,
            n_directions=N_DIRECTIONS_T0107,
        )
        cell_elapsed = time.time() - t_cell
        rates: list[float] = list(result.per_direction_rates_hz)
        angles: list[float] = list(result.per_direction_angles_deg)
        if len(rates) == 0:
            print(
                f"    WARNING: cell rank={c.t0106_rank} returned no per-direction "
                f"rates (n_errors={result.n_errors}, n_trials={result.n_trials})",
                flush=True,
            )
            dsi_vsum = 0.0
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
        print(
            f"    -> vsum-DSI={dsi_vsum:.3f}  PD@0={pd_at_0:.2f} Hz  "
            f"ND@180={nd_at_180:.2f} Hz  ratio-DSI={ratio_sanity:.3f}  "
            f"({cell_elapsed:.1f} s)",
            flush=True,
        )
        records.append(
            {
                "t0106_rank": c.t0106_rank,
                "t0106_generation": c.t0106_generation,
                "t0106_dsi": c.t0106_dsi,
                "t0106_pd_hz": c.t0106_pd_hz,
                "vector_68d": list(c.vector_68d),
                "angles_deg": angles,
                "per_direction_rates_hz": rates,
                "t0107_dsi_8dir_vsum": dsi_vsum,
                "t0107_pd_at_0deg": pd_at_0,
                "t0107_nd_at_180deg": nd_at_180,
                "t0107_dsi_2dir_ratio_sanity": ratio_sanity,
                "t0107_eval_seeds": EVAL_SEEDS_T0107,
                "t0107_n_directions": N_DIRECTIONS_T0107,
                "t0107_eval_elapsed_s": cell_elapsed,
            }
        )
        accum_elapsed += cell_elapsed
        # Checkpoint after every cell so a kill doesn't lose progress.
        checkpoint_payload: dict[str, object] = {
            "n_directions": N_DIRECTIONS_T0107,
            "eval_seeds": EVAL_SEEDS_T0107,
            "wall_clock_total_s": accum_elapsed,
            "evaluations": records,
        }
        _write_checkpoint(payload=checkpoint_payload)
        done_ranks.add(c.t0106_rank)

    total_elapsed = time.time() - t_run_start
    final_payload: dict[str, object] = {
        "n_directions": N_DIRECTIONS_T0107,
        "eval_seeds": EVAL_SEEDS_T0107,
        "wall_clock_total_s": accum_elapsed,
        "wall_clock_this_session_s": total_elapsed,
        "evaluations": records,
    }
    PER_CELL_POLAR_JSON.write_text(
        json.dumps(final_payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nWrote {PER_CELL_POLAR_JSON}")
    print(f"Total accum NEURON wall clock: {accum_elapsed:.1f} s")
    print(f"This-session NEURON wall clock: {total_elapsed:.1f} s")


if __name__ == "__main__":
    main()
