"""Post-hoc Strong-Bialek 1998 direct-method MI on the top-10 Pareto cells.

After the NSGA-II run terminates, this script:

1. Loads ``results/data/pareto_front_seed<S>.json``.
2. Ranks cells by ``mi_count_bits`` descending and takes the top N (default 10).
3. For each cell:
   a. Reconstructs the morphology + electrophys via the same pipeline used
      by the inner-loop evaluator (``_ensure_worker_cell`` +
      ``_ensure_synapse_bundle``).
   b. Runs ``n_directions`` (default 8) x ``n_trials`` (default 20) per
      direction in FULL mode, recording per-trial spike times from somatic
      Vm threshold crossings.
   c. Calls ``compute_mi_strong_bialek_bits_per_sec`` from
      ``mi_estimator.py`` with the dt=5 ms, T in {25, 50, 75, 100} ms
      schedule.
4. Writes ``results/data/post_hoc_strong_bialek_mi_top10.json`` with per-cell
   ``bits_per_sec``, ``std_err_bits_per_sec``, ``r_squared``, plus
   diagnostics.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0123_bedb_mi_atp_per_spike_nsga2.code import (
    bootstrap as _bootstrap,  # noqa: F401
)
from tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.constants import T0123_SEEDS
from tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.constants_electrophys import (
    AP_THRESHOLD_MV,
    DT_MS,
    SEED_BASE,
    TSTOP_MS,
    ParameterVector,
)
from tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.evaluator import (
    _ensure_synapse_bundle,
    _ensure_worker_cell,
    _run_one_trial,
)
from tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.generator_wrapper import (
    hash_morphology_vector,
    morphology_params_from_vector,
    split_68d_vector,
)
from tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.mi_estimator import (
    DT_MS_DEFAULT,
    TRIAL_DURATION_MS_DEFAULT,
    WORD_LENGTHS_MS_DEFAULT,
    compute_mi_strong_bialek_bits_per_sec,
)
from tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.paths import RESULTS_DATA_DIR

OUT_PATH: Path = RESULTS_DATA_DIR / "post_hoc_strong_bialek_mi_top10.json"


@dataclass(frozen=True, slots=True)
class CellResult:
    rank: int
    cell_index: int
    mi_count_bits: float
    atp_per_spike_molecules: float
    bits_per_sec: float
    std_err_bits_per_sec: float
    r_squared: float
    h_total_per_t: dict[int, float]
    h_noise_per_t: dict[int, float]
    n_directions: int
    n_trials_per_direction: int
    total_trials: int
    elapsed_s: float


def _extract_spike_times_from_trial(
    *, t_ms: NDArray[np.float64], v_soma_mv: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Detect upward threshold crossings at ``AP_THRESHOLD_MV``."""
    if v_soma_mv.size < 2:
        return np.zeros(0, dtype=np.float64)
    above = v_soma_mv >= AP_THRESHOLD_MV
    crossings = np.where((~above[:-1]) & above[1:])[0] + 1
    return t_ms[crossings].astype(np.float64)


def _run_post_hoc_for_cell(
    *,
    rank: int,
    cell_record: dict[str, Any],
    n_directions: int,
    n_trials_per_direction: int,
) -> CellResult:
    t0 = time.time()
    vec_68d = np.asarray(cell_record["vector_68d"], dtype=np.float64)
    electrophys_54d, morph_14d = split_68d_vector(vector_68d=vec_68d)
    morph_hash = hash_morphology_vector(vector=morph_14d)
    electrophys_hash = hash(electrophys_54d.tobytes())
    morph_params = morphology_params_from_vector(morph_vector_14d=morph_14d)
    electrophys_params = ParameterVector(values=electrophys_54d)
    placer_seed = SEED_BASE + (electrophys_hash & 0xFFFF)
    cell = _ensure_worker_cell(morph_params=morph_params, morph_hash=morph_hash)
    bundle = _ensure_synapse_bundle(
        cell=cell,
        electrophys_params=electrophys_params,
        placer_seed=placer_seed,
        electrophys_hash=electrophys_hash,
    )
    angles_deg: list[float] = [float(d) * (360.0 / n_directions) for d in range(n_directions)]
    spike_trains_by_direction: dict[float, list[NDArray[np.float64]]] = {}
    total_trials = 0
    for direction_deg in angles_deg:
        spike_trains_by_direction.setdefault(direction_deg, [])
        for trial_idx in range(n_trials_per_direction):
            seed = int(electrophys_hash) % (2**31 - 1) + int(direction_deg) * 13 + trial_idx * 7919
            trial = _run_one_trial(
                cell=cell,
                bundle=bundle,
                direction_deg=direction_deg,
                seed=seed,
                eval_seed_index=trial_idx,
                record_ina_for_atp=False,
            )
            spike_times_ms = np.array(trial.spike_times_ms, dtype=np.float64)
            spike_trains_by_direction[direction_deg].append(spike_times_ms)
            total_trials += 1
    sb_result = compute_mi_strong_bialek_bits_per_sec(
        spike_trains_by_direction=spike_trains_by_direction,
        word_lengths_ms=WORD_LENGTHS_MS_DEFAULT,
        dt_ms=DT_MS_DEFAULT,
        trial_duration_ms=TRIAL_DURATION_MS_DEFAULT,
    )
    elapsed_s = time.time() - t0
    return CellResult(
        rank=rank,
        cell_index=int(cell_record.get("cell_id", rank - 1)),
        mi_count_bits=float(cell_record.get("mi_count_bits", 0.0)),
        atp_per_spike_molecules=float(cell_record.get("atp_per_spike_molecules", float("nan"))),
        bits_per_sec=float(sb_result.bits_per_sec),
        std_err_bits_per_sec=float(sb_result.std_err_bits_per_sec),
        r_squared=float(sb_result.r_squared),
        h_total_per_t={int(k): float(v) for k, v in sb_result.h_total_per_t.items()},
        h_noise_per_t={int(k): float(v) for k, v in sb_result.h_noise_per_t.items()},
        n_directions=n_directions,
        n_trials_per_direction=n_trials_per_direction,
        total_trials=total_trials,
        elapsed_s=elapsed_s,
    )


def _load_pareto(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"pareto_front_seed{seed}.json"
    if not path.exists():
        raise FileNotFoundError(f"missing {path}; run build_results.py first")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("cells", []))


def run_post_hoc(
    *,
    seed: int,
    top_n: int = 10,
    n_directions: int = 8,
    n_trials: int = 20,
) -> Path:
    pareto = _load_pareto(seed=seed)
    if len(pareto) == 0:
        print(
            f"[post_hoc_strong_bialek] WARNING: no Pareto cells for seed {seed}; "
            f"writing empty result."
        )
        empty: dict[str, Any] = {
            "seed": int(seed),
            "n_top_cells_requested": int(top_n),
            "n_top_cells_actual": 0,
            "tstop_ms": float(TSTOP_MS),
            "dt_ms": float(DT_MS),
            "cells": [],
        }
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUT_PATH.write_text(json.dumps(empty, indent=2), encoding="utf-8")
        return OUT_PATH
    pareto_sorted = sorted(
        pareto,
        key=lambda c: -float(c.get("mi_count_bits", 0.0)),
    )
    top_cells = pareto_sorted[:top_n]
    results: list[CellResult] = []
    for i, cell_record in enumerate(top_cells):
        print(f"[post_hoc_strong_bialek] cell {i + 1}/{len(top_cells)}: starting")
        try:
            res = _run_post_hoc_for_cell(
                rank=i + 1,
                cell_record=cell_record,
                n_directions=n_directions,
                n_trials_per_direction=n_trials,
            )
        except (RuntimeError, ValueError, ArithmeticError) as exc:
            print(
                f"[post_hoc_strong_bialek] cell {i + 1} FAILED "
                f"({type(exc).__name__}: {exc}); writing NaN result"
            )
            res = CellResult(
                rank=i + 1,
                cell_index=int(cell_record.get("cell_id", i)),
                mi_count_bits=float(cell_record.get("mi_count_bits", 0.0)),
                atp_per_spike_molecules=float(
                    cell_record.get("atp_per_spike_molecules", float("nan"))
                ),
                bits_per_sec=float("nan"),
                std_err_bits_per_sec=float("nan"),
                r_squared=float("nan"),
                h_total_per_t={},
                h_noise_per_t={},
                n_directions=n_directions,
                n_trials_per_direction=n_trials,
                total_trials=0,
                elapsed_s=0.0,
            )
        results.append(res)
        print(
            f"[post_hoc_strong_bialek] cell {i + 1}/{len(top_cells)}: "
            f"bits_per_sec={res.bits_per_sec:.2f} r^2={res.r_squared:.3f} "
            f"({res.elapsed_s:.1f}s)"
        )

    payload: dict[str, Any] = {
        "seed": int(seed),
        "n_top_cells_requested": int(top_n),
        "n_top_cells_actual": len(results),
        "n_directions": int(n_directions),
        "n_trials_per_direction": int(n_trials),
        "word_lengths_ms": list(WORD_LENGTHS_MS_DEFAULT),
        "dt_ms": float(DT_MS_DEFAULT),
        "trial_duration_ms": float(TRIAL_DURATION_MS_DEFAULT),
        "cells": [asdict(r) for r in results],
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[post_hoc_strong_bialek] wrote {OUT_PATH}")
    return OUT_PATH


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=int(T0123_SEEDS[0]))
    parser.add_argument("--top-n", type=int, default=10)
    parser.add_argument("--n-directions", type=int, default=8)
    parser.add_argument("--n-trials", type=int, default=20)
    args = parser.parse_args()
    run_post_hoc(
        seed=int(args.seed),
        top_n=int(args.top_n),
        n_directions=int(args.n_directions),
        n_trials=int(args.n_trials),
    )


if __name__ == "__main__":
    main()
