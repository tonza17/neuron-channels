"""Phase G.3: causal NaP knockout per cluster representative.

For each of the 4 cluster representatives (1604, 1634, 767, 1639):

1. Load its 54-d params from t0083 all_evaluations.json.
2. Override ``params[NAP_DEND_DISTAL] = 0.0``.
3. Run the 16-direction Vm-trace deepdive (1400 ms each, HH on) at the
   BedB-equivalent procedural cell.
4. Compute knockout DSI per cell; classify as ``nap_dominant`` (DSI <= 0.2),
   ``nap_partial`` (0.2 < DSI <= 0.4), or ``nap_minor`` (DSI > 0.4).

Outputs:

* ``data/g3_nap_knockout.json``
* ``data/g3_traces/cell{cell_id}_dir{direction_int_tenths}_traces.npz`` (64 files)
"""

from __future__ import annotations

import json
import time
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    SEED_BASE,
    ParameterVector,
    ParamIndex,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import (
    run_one_trial,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import (
    setup_synapses_parametric,
)
from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    ANGLES_16DIR_DEG,
    REPRESENTATIVE_CELL_IDS,
)
from tasks.t0090_morphology_generator_diversity_test.code.generator import (
    generate_morphology,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0090_morphology_generator_diversity_test.code.paths import (
    DATA_G3_KNOCKOUT_JSON,
    DATA_G3_TRACES_DIR,
    T0083_ALL_EVALUATIONS_JSON,
    ensure_directories,
)
from tasks.t0090_morphology_generator_diversity_test.code.verification import (
    _LIVE_CELLS,
    _insert_baseline_channels,
)


def _classify_verdict(*, dsi: float) -> str:
    if dsi <= 0.2:
        return "nap_dominant"
    if dsi <= 0.4:
        return "nap_partial"
    return "nap_minor"


def _load_cell_params(*, cell_id: int) -> ParameterVector:
    all_evals = json.loads(T0083_ALL_EVALUATIONS_JSON.read_text())
    for e in all_evals:
        if int(e["cell_index"]) == int(cell_id):
            return ParameterVector(values=np.array(e["params"], dtype=np.float64))
    raise ValueError(f"cell_id {cell_id} not found in t0083 all_evaluations.json")


def _knockout_params(*, original: ParameterVector) -> ParameterVector:
    out = original.values.copy()
    out[int(ParamIndex.NAP_DEND_DISTAL)] = 0.0
    return ParameterVector(values=out)


def _build_cell() -> Any:
    bedb = MorphologyParams.from_bedb_base_point()
    cell = generate_morphology(params=bedb, morph_seed=int(bedb.morph_seed))
    _LIVE_CELLS.append(cell)
    _insert_baseline_channels(cell=cell)
    return cell


def _record_v_traces(*, cell: Any) -> Any:
    """Set up h.Vector recorders on soma + a representative dendrite tip."""
    h = cell.h
    v_soma = h.Vector()
    v_soma.record(cell.soma(0.5)._ref_v)
    v_dend: Any | None = None
    if len(cell.terminal_dends) > 0:
        v_dend = h.Vector()
        v_dend.record(cell.terminal_dends[0](0.5)._ref_v)
    t_vec = h.Vector()
    t_vec.record(h._ref_t)
    return v_soma, v_dend, t_vec


def _save_traces(
    *,
    cell_id: int,
    direction_deg: float,
    v_soma: NDArray[np.float64],
    v_dend: NDArray[np.float64] | None,
    t: NDArray[np.float64],
) -> None:
    direction_int = int(round(direction_deg * 10))
    out_path = DATA_G3_TRACES_DIR / f"cell{cell_id}_dir{direction_int}_traces.npz"
    if v_dend is not None:
        np.savez_compressed(str(out_path), v_soma=v_soma, t=t, v_dend=v_dend)
    else:
        np.savez_compressed(str(out_path), v_soma=v_soma, t=t)


def _run_16dir_deepdive(
    *,
    cell: Any,
    params_pv: ParameterVector,
    cell_id: int,
    save_traces: bool,
) -> dict[float, dict[str, Any]]:
    """For each of 16 directions, run one trial; record spikes + traces if requested."""
    apply_parameter_vector(cell=cell, params=params_pv)
    placer_seed = SEED_BASE + (int(hash(params_pv.values.tobytes())) & 0xFFFF)
    bundle = setup_synapses_parametric(
        cell=cell,
        n_ach=params_pv.n_ach,
        n_gaba=params_pv.n_gaba,
        rho_0_ach=params_pv.rho0_ach,
        lambda_ach_um=params_pv.lambda_ach_um,
        rho_0_gaba=params_pv.rho0_gaba,
        lambda_gaba_um=params_pv.lambda_gaba_um,
        w_ach_us=params_pv.w_ach_us,
        w_gaba_us=params_pv.w_gaba_us,
        placer_seed=placer_seed,
        gnmda_dend=params_pv.gnmda_dend,
        mg_conc_mm=params_pv.mg_conc_mm,
        voff_nmda=params_pv.voff_nmda,
    )

    out: dict[float, dict[str, Any]] = {}
    for angle in ANGLES_16DIR_DEG:
        if save_traces:
            v_soma, v_dend, t_vec = _record_v_traces(cell=cell)
        result = run_one_trial(
            cell=cell,
            bundle=bundle,
            direction_deg=float(angle),
            seed=SEED_BASE + cell_id + int(angle),
        )
        out[float(angle)] = {
            "spike_count": int(result.spike_count),
            "peak_mv": float(result.peak_mv) if np.isfinite(result.peak_mv) else None,
            "error": result.error,
        }
        if save_traces:
            v_soma_arr = np.asarray(v_soma.to_python(), dtype=np.float64)
            t_arr = np.asarray(t_vec.to_python(), dtype=np.float64)
            v_dend_arr: NDArray[np.float64] | None = None
            if v_dend is not None:
                v_dend_arr = np.asarray(v_dend.to_python(), dtype=np.float64)
            _save_traces(
                cell_id=cell_id,
                direction_deg=float(angle),
                v_soma=v_soma_arr,
                v_dend=v_dend_arr,
                t=t_arr,
            )
    return out


def _spike_counts_to_dsi(*, spikes_by_angle: dict[float, dict[str, Any]]) -> float:
    pd = float(spikes_by_angle.get(0.0, {}).get("spike_count", 0))
    nd = float(spikes_by_angle.get(180.0, {}).get("spike_count", 0))
    if pd + nd <= 0:
        return 0.0
    return float((pd - nd) / (pd + nd))


def evaluate_one_cell(*, cell_id: int) -> dict[str, Any]:
    """Run original + knockout 16-direction sweeps; return summary."""
    t0 = time.time()
    original_pv = _load_cell_params(cell_id=cell_id)
    knockout_pv = _knockout_params(original=original_pv)

    proc_cell = _build_cell()
    print(f"  cell {cell_id}: running ORIGINAL sweep ...")
    original_sweep = _run_16dir_deepdive(
        cell=proc_cell,
        params_pv=original_pv,
        cell_id=cell_id,
        save_traces=False,
    )
    original_dsi_proc = _spike_counts_to_dsi(spikes_by_angle=original_sweep)

    proc_cell_ko = _build_cell()
    print(f"  cell {cell_id}: running KNOCKOUT sweep ...")
    ko_sweep = _run_16dir_deepdive(
        cell=proc_cell_ko,
        params_pv=knockout_pv,
        cell_id=cell_id,
        save_traces=True,
    )
    ko_dsi = _spike_counts_to_dsi(spikes_by_angle=ko_sweep)
    verdict = _classify_verdict(dsi=ko_dsi)

    return {
        "cell_id": cell_id,
        "original_t0083_dsi": float(original_pv.values[0]),  # placeholder; actual stored separately
        "original_proc_dsi": original_dsi_proc,
        "knockout_dsi": ko_dsi,
        "verdict": verdict,
        "elapsed_s": time.time() - t0,
        "original_sweep": {f"{k:.1f}": v for k, v in sorted(original_sweep.items())},
        "knockout_sweep": {f"{k:.1f}": v for k, v in sorted(ko_sweep.items())},
    }


def _validation_gate_check(*, cell_id: int = 1604) -> dict[str, Any]:
    """[CRITICAL] gate: run cell 1604 first; halt if knockout DSI ~ original (>99 percent match)."""
    print(f"=== validation gate: cell {cell_id} only ===")
    summary = evaluate_one_cell(cell_id=cell_id)
    proc_orig_dsi = summary["original_proc_dsi"]
    ko_dsi = summary["knockout_dsi"]
    if abs(proc_orig_dsi) > 1e-6:
        match_ratio = abs(ko_dsi - proc_orig_dsi) / abs(proc_orig_dsi)
    else:
        match_ratio = abs(ko_dsi - proc_orig_dsi)
    halt = match_ratio < 0.01  # less than 1 percent change == essentially identical
    summary["gate_match_ratio"] = match_ratio
    summary["gate_halt"] = halt
    return summary


def main() -> None:
    ensure_directories()

    cell_summaries: list[dict[str, Any]] = []

    # Validation gate: run cell 1604 first.
    gate = _validation_gate_check(cell_id=1604)
    cell_summaries.append(gate)
    if gate["gate_halt"]:
        print(
            f"GATE HALT: knockout DSI {gate['knockout_dsi']:.3f} matches original "
            f"{gate['original_proc_dsi']:.3f} too closely "
            f"(match_ratio={gate['gate_match_ratio']:.4f})."
        )
        DATA_G3_KNOCKOUT_JSON.write_text(
            json.dumps({"halted_at_gate": True, "cells": cell_summaries}, indent=2)
        )
        return

    # Continue with the remaining 3 cells.
    for cell_id in REPRESENTATIVE_CELL_IDS:
        if cell_id == 1604:
            continue  # Already done in the gate.
        summary = evaluate_one_cell(cell_id=cell_id)
        cell_summaries.append(summary)

    # Aggregate verdict.
    knockout_dsis = [s["knockout_dsi"] for s in cell_summaries]
    n_dominant = sum(1 for s in cell_summaries if s["verdict"] == "nap_dominant")
    n_partial = sum(1 for s in cell_summaries if s["verdict"] == "nap_partial")
    n_minor = sum(1 for s in cell_summaries if s["verdict"] == "nap_minor")
    if n_dominant == len(cell_summaries):
        overall = "nap_causally_dominant"
    elif n_dominant + n_partial >= len(cell_summaries) // 2:
        overall = "nap_causally_partial"
    else:
        overall = "nap_attribution_partial"

    DATA_G3_KNOCKOUT_JSON.write_text(
        json.dumps(
            {
                "halted_at_gate": False,
                "n_cells": len(cell_summaries),
                "knockout_dsis": knockout_dsis,
                "n_dominant": n_dominant,
                "n_partial": n_partial,
                "n_minor": n_minor,
                "overall_verdict": overall,
                "cells": cell_summaries,
            },
            indent=2,
        )
    )
    print(f"wrote {DATA_G3_KNOCKOUT_JSON}")
    print(f"verdicts: dominant={n_dominant}, partial={n_partial}, minor={n_minor}")
    print(f"overall: {overall}")


if __name__ == "__main__":
    main()
