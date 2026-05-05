"""Substrate-consistency smoke gate (REQ-7).

Re-evaluates the 5 t0080 Pareto cells using the freshly compiled v3 substrate
(local Windows build OR remote Linux build) and confirms DSI / PD reproduce
within tolerance ``DSI_TOLERANCE`` / ``PD_TOLERANCE_HZ`` of the t0080 recorded
values. Writes a JSON record to ``logs/smoke_gate.json`` and exits with code
1 if any cell diverges.
"""

from __future__ import annotations

import argparse
import json
import sys
import time

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
from tasks.t0081_bedb_v3_warmstart_nsga2.code.paths import (
    SMOKE_GATE_JSON,
    T0080_PARETO_FRONT_JSON,
    ensure_directories,
)

DSI_TOLERANCE: float = 0.05
PD_TOLERANCE_HZ: float = 1.0


def _run_smoke_gate(*, n_seeds: int, max_workers: int) -> int:
    ensure_directories()
    raw = json.loads(T0080_PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    cells = raw["cells"]
    print(f"[smoke_gate] re-evaluating {len(cells)} t0080 Pareto cells", flush=True)
    records: list[dict[str, object]] = []
    n_pass: int = 0
    n_fail: int = 0
    for cell in cells:
        cell_index: int = int(cell["cell_index"])
        ref_dsi: float = float(cell["dsi"])
        ref_pd: float = float(cell["pd_rate_hz"])
        params_natural = np.asarray(cell["params"], dtype=np.float64)
        assert params_natural.shape == (N_PARAMS,)
        # t0080's BedBV3Problem declares xl/xu in natural units, so pymoo
        # samples and writes natural-unit values into ``params``. Pass them
        # straight to ParameterVector.
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
                    "cell_index": cell_index,
                    "ref_dsi": ref_dsi,
                    "ref_pd_rate_hz": ref_pd,
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
        delta_dsi: float = res.dsi - ref_dsi
        delta_pd: float = res.pd_rate_hz - ref_pd
        is_pass: bool = (
            abs(delta_dsi) <= DSI_TOLERANCE
            and abs(delta_pd) <= PD_TOLERANCE_HZ
            and not res.is_unstable
        )
        records.append(
            {
                "cell_index": cell_index,
                "ref_dsi": ref_dsi,
                "ref_pd_rate_hz": ref_pd,
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
            f"[smoke_gate] cell {cell_index}: ref=(DSI={ref_dsi:.3f}, PD={ref_pd:.2f}Hz) "
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
        "records": records,
        "n_seeds": n_seeds,
        "max_workers": max_workers,
    }
    SMOKE_GATE_JSON.parent.mkdir(parents=True, exist_ok=True)
    SMOKE_GATE_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(
        f"[smoke_gate] {n_pass}/{len(cells)} pass, {n_fail} fail; wrote {SMOKE_GATE_JSON}",
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
