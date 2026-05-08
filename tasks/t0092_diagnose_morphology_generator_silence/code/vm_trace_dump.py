"""Phase C: soma Vm trace comparison under PD bar (REQ-3).

Builds both cells, applies the t0083 best-cell parameter vector, places synapses
with ``placer_seed=42``, runs a single PD-direction bar trial at ``SEED_BASE``,
and writes:

* ``data/vm_trace_procedural.npy`` — soma Vm trace at 0.1 ms resolution
* ``data/vm_trace_handcoded.npy`` — soma Vm trace at 0.1 ms resolution
* ``results/images/vm_trace_comparison.png`` — overlaid traces

Validation gate: if the hand-coded cell does NOT spike under the t0083 best-cell
vector, we halt here — the bug is not in the generator. The Phase D analysis
records this as the primary cause and the rest of the pipeline routes into the
acceptable-negative branch (REQ-5).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    DT_MS,
    PD_DIRECTION_DEG,
    SEED_BASE,
    TSTOP_MS,
)
from tasks.t0090_morphology_generator_diversity_test.code.load_default_params import (
    load_t0083_best_cell_param_vector,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import (
    insert_baseline_channels,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.build_cells import (
    TwoCells,
    build_both_cells,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.paths import (
    DATA_DIR,
    VM_TRACE_COMPARISON_PNG,
    VM_TRACE_HANDCODED_NPY,
    VM_TRACE_PROCEDURAL_NPY,
    ensure_directories,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.synapse_dump import (
    run_synapse_dump,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.trial_with_trace import (
    TraceResult,
    run_one_trial_with_trace,
)


@dataclass(frozen=True, slots=True)
class CellTraceStats:
    cell_kind: str
    spike_count: int
    peak_vm_mv: float
    time_to_peak_ms: float
    epsp_area_mv_ms: float
    npy_path: str


def _trace_stats(*, cell_kind: str, result: TraceResult, npy_path: str) -> CellTraceStats:
    return CellTraceStats(
        cell_kind=cell_kind,
        spike_count=int(result.spike_count),
        peak_vm_mv=float(result.peak_mv) if np.isfinite(result.peak_mv) else float("nan"),
        time_to_peak_ms=float(result.time_to_peak_ms),
        epsp_area_mv_ms=float(result.epsp_area_mv_ms),
        npy_path=npy_path,
    )


def _save_trace(*, trace: NDArray[np.float64], npy_path: str) -> None:
    np.save(npy_path, trace)


def _plot_overlay(
    *,
    proc_trace: NDArray[np.float64],
    hand_trace: NDArray[np.float64],
    out_png: str,
) -> None:
    n_proc = proc_trace.shape[0]
    n_hand = hand_trace.shape[0]
    n = max(n_proc, n_hand)
    t_axis = np.arange(n, dtype=np.float64) * float(DT_MS)
    fig, ax = plt.subplots(figsize=(10, 5))
    if n_proc > 0:
        ax.plot(
            t_axis[:n_proc],
            proc_trace,
            label="procedural_bedb",
            color="tab:red",
            linewidth=1.0,
        )
    if n_hand > 0:
        ax.plot(
            t_axis[:n_hand],
            hand_trace,
            label="handcoded_bedb",
            color="tab:blue",
            linewidth=1.0,
        )
    ax.axhline(-10.0, color="grey", linestyle=":", linewidth=0.6, label="AP threshold (-10 mV)")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Soma Vm (mV)")
    ax.set_title("PD-direction bar (t0083 best-cell channels): procedural vs hand-coded BedB")
    ax.legend(loc="lower right")
    ax.grid(True, linestyle=":", linewidth=0.4, alpha=0.6)
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


def run_vm_trace_dump(*, two: TwoCells) -> dict[str, Any]:
    pv = load_t0083_best_cell_param_vector()

    insert_baseline_channels(h=two.h, cell=two.procedural_bedb)
    insert_baseline_channels(h=two.h, cell=two.handcoded_bedb)

    apply_parameter_vector(cell=two.procedural_bedb, params=pv)  # type: ignore[arg-type]
    apply_parameter_vector(cell=two.handcoded_bedb, params=pv)

    _, bundle_proc, bundle_hand = run_synapse_dump(two=two)

    proc_result = run_one_trial_with_trace(
        cell=two.procedural_bedb,
        bundle=bundle_proc,
        direction_deg=float(PD_DIRECTION_DEG),
        seed=int(SEED_BASE),
    )
    hand_result = run_one_trial_with_trace(
        cell=two.handcoded_bedb,
        bundle=bundle_hand,
        direction_deg=float(PD_DIRECTION_DEG),
        seed=int(SEED_BASE),
    )

    _save_trace(trace=proc_result.v_trace, npy_path=str(VM_TRACE_PROCEDURAL_NPY))
    _save_trace(trace=hand_result.v_trace, npy_path=str(VM_TRACE_HANDCODED_NPY))

    _plot_overlay(
        proc_trace=proc_result.v_trace,
        hand_trace=hand_result.v_trace,
        out_png=str(VM_TRACE_COMPARISON_PNG),
    )

    proc_stats = _trace_stats(
        cell_kind="procedural_bedb",
        result=proc_result,
        npy_path=str(VM_TRACE_PROCEDURAL_NPY),
    )
    hand_stats = _trace_stats(
        cell_kind="handcoded_bedb",
        result=hand_result,
        npy_path=str(VM_TRACE_HANDCODED_NPY),
    )

    payload: dict[str, Any] = {
        "spec_version": "1",
        "tstop_ms": float(TSTOP_MS),
        "dt_ms": float(DT_MS),
        "direction_deg": float(PD_DIRECTION_DEG),
        "seed": int(SEED_BASE),
        "procedural_bedb": {
            "cell_kind": proc_stats.cell_kind,
            "spike_count": proc_stats.spike_count,
            "peak_vm_mv": proc_stats.peak_vm_mv,
            "time_to_peak_ms": proc_stats.time_to_peak_ms,
            "epsp_area_mv_ms": proc_stats.epsp_area_mv_ms,
            "npy_path": proc_stats.npy_path,
            "error": proc_result.error,
        },
        "handcoded_bedb": {
            "cell_kind": hand_stats.cell_kind,
            "spike_count": hand_stats.spike_count,
            "peak_vm_mv": hand_stats.peak_vm_mv,
            "time_to_peak_ms": hand_stats.time_to_peak_ms,
            "epsp_area_mv_ms": hand_stats.epsp_area_mv_ms,
            "npy_path": hand_stats.npy_path,
            "error": hand_result.error,
        },
        "validation_gate": {
            "handcoded_spikes": hand_stats.spike_count > 0,
            "diagnosis": (
                "handcoded_spikes_proceed_to_phase_d"
                if hand_stats.spike_count > 0
                else "handcoded_silent_route_to_acceptable_negative_branch"
            ),
        },
    }
    return payload


def main() -> int:
    ensure_directories()
    two = build_both_cells()
    payload = run_vm_trace_dump(two=two)
    out_json = DATA_DIR / "vm_trace_summary.json"
    out_json.write_text(json.dumps(payload, indent=2))
    proc = payload["procedural_bedb"]
    hand = payload["handcoded_bedb"]
    print(
        "procedural: spikes={}, peak_vm={:.2f} mV, epsp_area={:.2f} mV*ms, error={}".format(
            proc["spike_count"], proc["peak_vm_mv"], proc["epsp_area_mv_ms"], proc["error"]
        )
    )
    print(
        "handcoded:  spikes={}, peak_vm={:.2f} mV, epsp_area={:.2f} mV*ms, error={}".format(
            hand["spike_count"], hand["peak_vm_mv"], hand["epsp_area_mv_ms"], hand["error"]
        )
    )
    print(f"validation_gate: {payload['validation_gate']['diagnosis']}")
    print(f"wrote {VM_TRACE_PROCEDURAL_NPY}")
    print(f"wrote {VM_TRACE_HANDCODED_NPY}")
    print(f"wrote {VM_TRACE_COMPARISON_PNG}")
    print(f"wrote {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
