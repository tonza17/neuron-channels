"""Build t0123 results JSONs from the per-cell trace and HV trajectory.

Reads the side-channel JSONL trace written by the evaluator and the
per-generation snapshots written by the NSGA-II driver. Produces:

* ``results/data/pareto_front_seed<S>.json`` -- one entry per
  Pareto-optimal cell in (MI maximised, ATP/spike minimised) space,
  with ``mi_count_bits``, ``atp_per_spike_molecules``, per-direction
  firing, DSI / PD-rate diagnostics, and ``silence_failed_bool`` /
  ``legit_bool`` flags.
* ``results/data/all_evaluations_seed<S>.json`` -- every per-cell
  evaluation across all generations, in the same enriched format.

The Pareto front is computed on the deduplicated trace using the
classic non-dominated subset definition: cell ``a`` dominates ``b`` iff
``a.mi >= b.mi AND a.atp <= b.atp`` with at least one strict inequality.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tasks.t0128_t0127_rerun_dsi_atp_3seeds.code.paths import (
    RESULTS_DATA_DIR,
    all_evaluations_json,
    ensure_directories,
    pareto_front_json,
)

DSI_LEGIT_THRESHOLD: float = 0.5
PD_RATE_LEGIT_THRESHOLD_HZ: float = 30.0


def _is_silence_failed(cell: dict[str, Any]) -> bool:
    return bool(cell.get("silence_failed", False))


def _is_legit(cell: dict[str, Any]) -> bool:
    return (
        not _is_silence_failed(cell)
        and float(cell.get("dsi_vector_sum", 0.0)) >= DSI_LEGIT_THRESHOLD
        and float(cell.get("pd_rate_hz", 0.0)) >= PD_RATE_LEGIT_THRESHOLD_HZ
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
    """Return cells non-dominated in (MI max, ATP/spike min) space."""
    if len(cells) == 0:
        return []
    sorted_cells = sorted(
        cells,
        key=lambda c: (
            -float(c.get("mi_count_bits", 0.0)),
            float(c.get("atp_per_spike_molecules", float("inf"))),
        ),
    )
    front: list[dict[str, Any]] = []
    best_atp_so_far: float | None = None
    for c in sorted_cells:
        atp = float(c.get("atp_per_spike_molecules", float("inf")))
        if best_atp_so_far is None or atp < best_atp_so_far:
            front.append(c)
            best_atp_so_far = atp
    return front


def _enrich_cell(*, cell: dict[str, Any]) -> dict[str, Any]:
    mi = float(cell.get("mi_count_bits", 0.0))
    atp = float(cell.get("atp_per_spike_molecules", float("nan")))
    enriched: dict[str, Any] = {
        "vector_68d": [float(v) for v in cell["vector_68d"]],
        "mi_count_bits": mi,
        "atp_per_spike_molecules": atp,
        "atp_per_ap_molecules": float(cell.get("atp_per_ap_molecules", atp)),
        "atp_per_ap_compartment_breakdown": dict(cell.get("atp_per_ap_compartment_breakdown", {})),
        "firing_hz_per_dir": dict(cell.get("firing_hz_per_dir", {})),
        "dsi_vector_sum": float(cell.get("dsi_vector_sum", 0.0)),
        "pd_rate_hz": float(cell.get("pd_rate_hz", 0.0)),
        "robustness": float(cell.get("robustness", 0.0)),
        "objective_F_minimised": [-mi, atp],
        "silence_failed_bool": _is_silence_failed(cell),
        "legit_bool": _is_legit(cell),
    }
    return enriched


def build_results(*, seed: int) -> dict[str, Path]:
    """Build the Pareto front and all-evaluations JSONs."""
    ensure_directories()
    trace_path = RESULTS_DATA_DIR / f"cell_trace_seed{seed}.jsonl"
    if not trace_path.exists():
        raise FileNotFoundError(
            f"per-cell trace JSONL not found at {trace_path}; "
            f"ensure the NSGA-II driver was run with "
            f"T0128_CELL_TRACE_JSONL={trace_path} set in the environment"
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
            "non-dominated cells in (MI_count_bits maximised, "
            "atp_per_spike_molecules minimised) space; legit_bool = DSI "
            ">= 0.5 AND PD-rate >= 30 Hz AND NOT silence-failed"
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
