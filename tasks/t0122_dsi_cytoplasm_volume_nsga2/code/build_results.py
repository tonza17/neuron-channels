"""Build t0122 results JSONs from the per-cell trace and HV trajectory.

Reads the side-channel JSONL trace written by the evaluator and the
per-generation snapshots written by the NSGA-II driver. Produces:

* ``results/data/pareto_front_seed<S>.json`` -- one entry per
  Pareto-optimal cell in (DSI, cytoplasm_volume_um3) space, with
  ``dsi_vector_sum``, ``cytoplasm_volume_um3``, ``pd_rate_hz``,
  ``vector_68d``, ``silence_failed_bool``, and ``legit_bool``.
* ``results/data/all_evaluations_seed<S>.json`` -- every per-cell
  evaluation across all generations, in the same format as t0115's
  ``all_evaluations`` (including ``cytoplasm_volume_um3`` and
  ``pd_rate_hz``).

The Pareto front is computed on the deduplicated trace using the
classic non-dominated subset definition: a cell ``a`` dominates a cell
``b`` iff ``a.dsi >= b.dsi AND a.volume <= b.volume`` with at least one
strict inequality.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.paths import (
    RESULTS_DATA_DIR,
    all_evaluations_json,
    ensure_directories,
    pareto_front_json,
)

DSI_LEGIT_THRESHOLD: float = 0.5
PD_RATE_LEGIT_THRESHOLD_HZ: float = 30.0
DSI_SILENCE_CEILING: float = 0.9999
VOLUME_LEGIT_CEILING_UM3: float = 50000.0


def _is_silence_failed(cell: dict[str, Any]) -> bool:
    # The silence guard sets DSI = 0 (post-guard); a "silence failed"
    # cell is one whose pre-guard DSI saturated at 1.0 (silence corner)
    # OR whose pd_spikes were below the new t0122 threshold (~ 0 PD
    # rate). The simplest detectable surrogate: DSI >= 0.9999.
    return float(cell["dsi_vector_sum"]) >= DSI_SILENCE_CEILING


def _is_legit(cell: dict[str, Any]) -> bool:
    return (
        not _is_silence_failed(cell)
        and float(cell["dsi_vector_sum"]) >= DSI_LEGIT_THRESHOLD
        and float(cell["pd_rate_hz"]) >= PD_RATE_LEGIT_THRESHOLD_HZ
        and float(cell["cytoplasm_volume_um3"]) <= VOLUME_LEGIT_CEILING_UM3
    )


def _load_cells_from_trace(*, trace_path: Path) -> list[dict[str, Any]]:
    cells: list[dict[str, Any]] = []
    with trace_path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line == "":
                continue
            try:
                cells.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return cells


def _pareto_front(*, cells: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return cells that are non-dominated in (DSI, volume) space."""
    if len(cells) == 0:
        return []
    sorted_cells = sorted(
        cells,
        key=lambda c: (
            -float(c["dsi_vector_sum"]),
            float(c["cytoplasm_volume_um3"]),
        ),
    )
    front: list[dict[str, Any]] = []
    best_volume_so_far: float | None = None
    for c in sorted_cells:
        v = float(c["cytoplasm_volume_um3"])
        if best_volume_so_far is None or v < best_volume_so_far:
            front.append(c)
            best_volume_so_far = v
    return front


def _enrich_cell(*, cell: dict[str, Any], generation: int | None = None) -> dict[str, Any]:
    enriched: dict[str, Any] = {
        "vector_68d": [float(v) for v in cell["vector_68d"]],
        "dsi_vector_sum": float(cell["dsi_vector_sum"]),
        "pd_rate_hz": float(cell["pd_rate_hz"]),
        "robustness": float(cell.get("robustness", 0.0)),
        "cytoplasm_volume_um3": float(cell["cytoplasm_volume_um3"]),
        "objective_F_minimised": [
            -float(cell["dsi_vector_sum"]),
            float(cell["cytoplasm_volume_um3"]),
        ],
        "silence_failed_bool": _is_silence_failed(cell),
        "legit_bool": _is_legit(cell),
    }
    if generation is not None:
        enriched["generation"] = int(generation)
    return enriched


def build_results(*, seed: int) -> dict[str, Path]:
    """Build the Pareto front and all-evaluations JSONs."""
    ensure_directories()
    trace_path = RESULTS_DATA_DIR / f"cell_trace_seed{seed}.jsonl"
    if not trace_path.exists():
        raise FileNotFoundError(
            f"per-cell trace JSONL not found at {trace_path}; "
            f"ensure the NSGA-II driver was run with "
            f"T0122_CELL_TRACE_JSONL={trace_path} set in the environment"
        )
    cells = _load_cells_from_trace(trace_path=trace_path)
    print(f"[build_results] loaded {len(cells)} per-cell records from {trace_path}")

    # Deduplicate by 68-d vector.
    seen_keys: set[tuple[float, ...]] = set()
    unique_cells: list[dict[str, Any]] = []
    for c in cells:
        k = tuple(float(v) for v in c["vector_68d"])
        if k not in seen_keys:
            seen_keys.add(k)
            unique_cells.append(c)
    print(f"[build_results] {len(unique_cells)} unique cells")

    pareto = _pareto_front(cells=unique_cells)
    print(f"[build_results] Pareto front: {len(pareto)} cells")

    pareto_payload: dict[str, Any] = {
        "seed": int(seed),
        "n_total": len(pareto),
        "definition": (
            "non-dominated cells in (DSI maximised, cytoplasm_volume_um3 "
            "minimised) space; legit_bool = DSI >= 0.5 AND PD-rate >= 30 Hz "
            "AND volume <= 50000 um^3 AND NOT silence-failed (DSI < 0.9999)"
        ),
        "cells": [_enrich_cell(cell=c) for c in pareto],
    }
    pareto_path = pareto_front_json(seed=seed)
    pareto_path.write_text(json.dumps(pareto_payload, indent=2), encoding="utf-8")
    print(f"[build_results] wrote {pareto_path}")

    all_payload: dict[str, Any] = {
        "seed": int(seed),
        "n_total_records": len(cells),
        "n_unique_cells": len(unique_cells),
        "evaluations": [_enrich_cell(cell=c) for c in unique_cells],
    }
    all_path = all_evaluations_json(seed=seed)
    all_path.write_text(json.dumps(all_payload, indent=2), encoding="utf-8")
    print(f"[build_results] wrote {all_path}")

    return {"pareto_front": pareto_path, "all_evaluations": all_path}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    build_results(seed=int(args.seed))


if __name__ == "__main__":
    main()
