"""Validation gate: passive rest run with no synapses; V_rest = -65 mV +/- 0.5 mV.

Copied from ``tasks/t0057_tonic_gaba_sweep_t0053/code/test_quiescent_rest.py`` per CLAUDE.md
rule 3 with import-path rewrites only. The cell, channel, and passive parameters are unchanged
between t0057 and t0059.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.cell import (
    build_dsgc_from_swc,
    summarize_cell,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants import (
    DT_MS,
    V_INIT_MV,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.neuron_bootstrap import (
    ensure_neuron_importable,
    load_stdrun,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.paths import MORPHOLOGY_SWC_PATH

V_REST_TOLERANCE_MV: float = 0.5
QUIESCENT_DURATION_MS: float = 200.0


def test_quiescent_rest() -> None:
    """Build the cell, run 200 ms passive, check the soma stays at V_init within tolerance."""
    ensure_neuron_importable()
    load_stdrun()
    from neuron import h  # noqa: PLC0415

    h.dt = DT_MS

    cell = build_dsgc_from_swc(swc_path=MORPHOLOGY_SWC_PATH)
    summary = summarize_cell(cell=cell)
    print(
        f"[quiescent] cell: n_dendrites={summary.n_dendrites} "
        f"total_dendritic_length_um={summary.total_dendritic_length_um:.2f} "
        f"soma_L_um={summary.soma_length_um:.2f} soma_diam_um={summary.soma_diameter_um:.2f}",
        flush=True,
    )

    v_rec: Any = h.Vector()
    v_rec.record(cell.soma(0.5)._ref_v)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t)

    h.finitialize(V_INIT_MV)
    h.continuerun(QUIESCENT_DURATION_MS)

    v_arr: np.ndarray = np.array(list(v_rec), dtype=np.float64)
    t_arr: np.ndarray = np.array(list(t_rec), dtype=np.float64)

    sample_indices: list[int] = [
        0,
        int(0.5 * len(v_arr)),
        len(v_arr) - 1,
    ]
    print("[quiescent] soma voltage samples:", flush=True)
    for idx in sample_indices:
        print(f"  t={t_arr[idx]:7.3f} ms  V={v_arr[idx]:7.3f} mV", flush=True)

    final_v: float = float(v_arr[-1])
    delta_mv: float = abs(final_v - V_INIT_MV)
    print(
        f"[quiescent] final V_soma = {final_v:.4f} mV "
        f"(target {V_INIT_MV} +/- {V_REST_TOLERANCE_MV} mV; |delta| = {delta_mv:.4f} mV)",
        flush=True,
    )
    assert delta_mv <= V_REST_TOLERANCE_MV, (
        f"V_rest {final_v:.4f} mV outside [{V_INIT_MV - V_REST_TOLERANCE_MV}, "
        f"{V_INIT_MV + V_REST_TOLERANCE_MV}]"
    )


if __name__ == "__main__":
    test_quiescent_rest()
    print("[quiescent] PASS", flush=True)
