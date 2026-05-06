"""Substrate-consistency smoke gate for t0083 (REQ-10).

Re-evaluates 5 reference cells from t0081 (cell 767, the joint-pass anchor,
plus the highest-DSI Pareto cell from each of gens 4, 5, 6, 7) using the
freshly compiled v3 substrate on the new Vast.ai instance and confirms
DSI / PD reproduce within ``DSI_TOLERANCE`` / ``PD_TOLERANCE_HZ`` of the
t0081 recorded values. Writes a JSON record to ``logs/smoke_gate.json`` and
exits with code 1 if any cell diverges.

Note: t0081's Pareto front contains no gen-4 cell (gens 0/1/3/5/6/7 only).
For gen 4 the highest-DSI feasible non-unstable cell across the whole gen
is taken from ``all_evaluations.json`` as a substitute reference cell.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass

import numpy as np

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    ANGLES_8DIR_DEG,
    N_PARAMS,
    N_SEEDS,
    ParameterVector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import (
    EvalResult,
    evaluate_parameter_vector,
)
from tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code import paths

DSI_TOLERANCE: float = 0.05
PD_TOLERANCE_HZ: float = 1.0
TARGET_GENS: tuple[int, ...] = (4, 5, 6, 7)
ANCHOR_CELL_INDEX: int = 767  # cell 767 is the joint-pass anchor in t0081


@dataclass(frozen=True, slots=True)
class ReferenceCell:
    cell_index: int
    generation: int
    params: list[float]
    dsi: float
    pd_rate_hz: float


def _load_t0081_pareto_cells() -> list[dict[str, object]]:
    raw = json.loads(paths.T0081_PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    cells = raw.get("cells", raw) if isinstance(raw, dict) else raw
    assert isinstance(cells, list)
    return cells


def _load_t0081_all_cells() -> list[dict[str, object]]:
    raw = json.loads(paths.T0081_ALL_EVALUATIONS_JSON.read_text(encoding="utf-8"))
    cells = raw.get("evaluations", raw) if isinstance(raw, dict) else raw
    assert isinstance(cells, list)
    return cells


def _select_reference_cells() -> list[ReferenceCell]:
    """Cell 767 + highest-DSI Pareto cell from each of gens 4, 5, 6, 7.

    If gen 4 has no Pareto cell (true for t0081), fall back to the
    highest-DSI feasible non-unstable cell across all gen-4 evaluations.
    """
    pareto = _load_t0081_pareto_cells()
    pareto_by_gen: dict[int, list[dict[str, object]]] = {}
    for c in pareto:
        pareto_by_gen.setdefault(int(c["generation"]), []).append(c)
    selected: dict[int, dict[str, object]] = {}
    # Anchor cell first.
    anchor = next((c for c in pareto if int(c["cell_index"]) == ANCHOR_CELL_INDEX), None)
    assert anchor is not None, f"anchor cell {ANCHOR_CELL_INDEX} not in t0081 Pareto front"
    selected[ANCHOR_CELL_INDEX] = anchor
    # One cell per target gen (excluding the anchor's gen if already covered
    # — anchor is gen 7 and we add the highest-DSI gen-7 below; if it's
    # the same cell we keep just one).
    for gen in TARGET_GENS:
        candidates_pareto = pareto_by_gen.get(gen, [])
        if len(candidates_pareto) == 0:
            # Fall back to highest-DSI feasible non-unstable cell from
            # all_evaluations for this generation.
            all_cells = _load_t0081_all_cells()
            cands = [
                c
                for c in all_cells
                if int(c["generation"]) == gen
                and bool(c["is_feasible"])
                and not bool(c["is_unstable"])
            ]
            if len(cands) == 0:
                # Skip if no feasible non-unstable cell exists at all for this gen.
                continue
            best = max(cands, key=lambda c: float(c["dsi"]))
        else:
            best = max(candidates_pareto, key=lambda c: float(c["dsi"]))
        cidx = int(best["cell_index"])
        if cidx in selected:
            continue
        selected[cidx] = best
    out: list[ReferenceCell] = []
    for c in selected.values():
        out.append(
            ReferenceCell(
                cell_index=int(c["cell_index"]),
                generation=int(c["generation"]),
                params=[float(v) for v in c["params"]],  # type: ignore[arg-type]
                dsi=float(c["dsi"]),
                pd_rate_hz=float(c["pd_rate_hz"]),
            ),
        )
    return out


def _run_smoke_gate(*, n_seeds: int, max_workers: int) -> int:
    paths.ensure_directories()
    cells = _select_reference_cells()
    print(
        f"[smoke_gate] re-evaluating {len(cells)} t0081 reference cells "
        f"(anchor={ANCHOR_CELL_INDEX}, target gens={TARGET_GENS})",
        flush=True,
    )
    records: list[dict[str, object]] = []
    n_pass: int = 0
    n_fail: int = 0
    for cell in cells:
        params_natural = np.asarray(cell.params, dtype=np.float64)
        assert params_natural.shape == (N_PARAMS,)
        params = ParameterVector(values=params_natural)
        t0 = time.time()
        try:
            res: EvalResult = evaluate_parameter_vector(
                params=params,
                angles_deg=ANGLES_8DIR_DEG,
                n_seeds=n_seeds,
                max_workers=max_workers,
            )
        except (RuntimeError, ValueError, ArithmeticError, AssertionError) as exc:
            records.append(
                {
                    "cell_index": cell.cell_index,
                    "generation": cell.generation,
                    "ref_dsi": cell.dsi,
                    "ref_pd_rate_hz": cell.pd_rate_hz,
                    "obs_dsi": None,
                    "obs_pd_rate_hz": None,
                    "delta_dsi": None,
                    "delta_pd_rate_hz": None,
                    "is_pass": False,
                    "error": f"{type(exc).__name__}: {exc}",
                    "elapsed_s": time.time() - t0,
                }
            )
            n_fail += 1
            continue
        delta_dsi: float = res.dsi - cell.dsi
        delta_pd: float = res.pd_rate_hz - cell.pd_rate_hz
        is_pass: bool = (
            abs(delta_dsi) <= DSI_TOLERANCE
            and abs(delta_pd) <= PD_TOLERANCE_HZ
            and not res.is_unstable
        )
        records.append(
            {
                "cell_index": cell.cell_index,
                "generation": cell.generation,
                "ref_dsi": cell.dsi,
                "ref_pd_rate_hz": cell.pd_rate_hz,
                "obs_dsi": float(res.dsi),
                "obs_pd_rate_hz": float(res.pd_rate_hz),
                "delta_dsi": float(delta_dsi),
                "delta_pd_rate_hz": float(delta_pd),
                "is_unstable": bool(res.is_unstable),
                "peak_vm_mv": float(res.peak_vm_mv),
                "is_pass": bool(is_pass),
                "error": None,
                "elapsed_s": time.time() - t0,
            }
        )
        if is_pass:
            n_pass += 1
        else:
            n_fail += 1
        marker = "PASS" if is_pass else "FAIL"
        print(
            f"[smoke_gate] cell {cell.cell_index} (gen {cell.generation}): "
            f"ref=(DSI={cell.dsi:.3f}, PD={cell.pd_rate_hz:.2f}Hz) "
            f"obs=(DSI={res.dsi:.3f}, PD={res.pd_rate_hz:.2f}Hz) "
            f"delta=(DSI={delta_dsi:+.3f}, PD={delta_pd:+.2f}Hz) "
            f"unstable={res.is_unstable} -> {marker}",
            flush=True,
        )
    summary: dict[str, object] = {
        "tolerance_dsi": DSI_TOLERANCE,
        "tolerance_pd_rate_hz": PD_TOLERANCE_HZ,
        "n_cells": len(cells),
        "n_pass": n_pass,
        "n_fail": n_fail,
        "anchor_cell_index": ANCHOR_CELL_INDEX,
        "target_gens": list(TARGET_GENS),
        "cells": records,
        "n_seeds": n_seeds,
        "max_workers": max_workers,
    }
    paths.SMOKE_GATE_JSON.parent.mkdir(parents=True, exist_ok=True)
    paths.SMOKE_GATE_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(
        f"[smoke_gate] {n_pass}/{len(cells)} pass, {n_fail} fail; wrote {paths.SMOKE_GATE_JSON}",
        flush=True,
    )
    return 0 if n_fail == 0 else 1


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-seeds", type=int, default=N_SEEDS)
    parser.add_argument("--max-workers", type=int, default=0)
    args = parser.parse_args()
    return _run_smoke_gate(n_seeds=args.n_seeds, max_workers=args.max_workers)


if __name__ == "__main__":
    sys.exit(_main())
