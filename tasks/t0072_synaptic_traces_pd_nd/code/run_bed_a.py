"""Bed A (Poleg-Polsky 2016 deposited DSGC) PD + ND trial runner with per-synapse recording.

Records gAMPA, gNMDA, g_GABA (SACinhibsyn), g_ACh (SACexcsyn), and the local membrane
voltage v at the synapse insertion point for every one of the 282 ON-dendrite synapses.
PD/ND swap is implemented by overriding h.gabaMOD between trials.

Recorder pattern adapted from
``tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py`` (lines 100-150;
``attach_conductance_recorders`` and ``ConductanceRecorders``). The single extension
over t0048's pattern is per-synapse local v via ``pp.get_segment()._ref_v``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from tasks.t0008_port_modeldb_189347.code.build_cell import (
    apply_params,
    build_dsgc,
)
from tasks.t0072_synaptic_traces_pd_nd.code.constants import (
    BED_A_N_SYNAPSES,
    E_ACH_BED_A_MV,
    E_AMPA_MV,
    E_GABA_BED_A_MV,
    E_NMDA_MV,
    E_REV_MV_KEY,
    G_TRACES_KEY,
    GABA_MOD_ND,
    GABA_MOD_PD,
    RECORD_DT_MS,
    SEED,
    T_MS_KEY,
    TSTOP_MS,
    V_INIT_MV,
    V_LOCAL_TRACES_KEY,
    Direction,
    RecordedSynapseType,
)
from tasks.t0072_synaptic_traces_pd_nd.code.paths import (
    BED_A_ND_ACH_NPZ,
    BED_A_ND_AMPA_NPZ,
    BED_A_ND_GABA_NPZ,
    BED_A_ND_NMDA_NPZ,
    BED_A_PD_ACH_NPZ,
    BED_A_PD_AMPA_NPZ,
    BED_A_PD_GABA_NPZ,
    BED_A_PD_NMDA_NPZ,
    DATA_DIR,
)


@dataclass(slots=True)
class BedARecorders:
    """NEURON Vector handles, one per synapse per channel, plus shared per-syn v_local."""

    g_ampa: list[Any]
    g_nmda: list[Any]
    g_gaba: list[Any]
    g_ach: list[Any]
    v_local: list[Any]
    t_rec: Any
    num_synapses: int


def _attach_bed_a_recorders(*, h: Any) -> BedARecorders:
    """Attach Vector.record handles for the four Bed A channels and per-synapse v_local."""
    num_synapses: int = int(h.RGC.numsyn)
    g_ampa: list[Any] = []
    g_nmda: list[Any] = []
    g_gaba: list[Any] = []
    g_ach: list[Any] = []
    v_local: list[Any] = []

    for idx in range(num_synapses):
        bip: Any = h.RGC.BIPsyn[idx]
        sacinhib: Any = h.RGC.SACinhibsyn[idx]
        sacexc: Any = h.RGC.SACexcsyn[idx]

        v_a: Any = h.Vector()
        v_a.record(bip._ref_gAMPA, RECORD_DT_MS)
        g_ampa.append(v_a)

        v_n: Any = h.Vector()
        v_n.record(bip._ref_gNMDA, RECORD_DT_MS)
        g_nmda.append(v_n)

        v_g: Any = h.Vector()
        v_g.record(sacinhib._ref_g, RECORD_DT_MS)
        g_gaba.append(v_g)

        v_e: Any = h.Vector()
        v_e.record(sacexc._ref_g, RECORD_DT_MS)
        g_ach.append(v_e)

        # All four Bed A synapses share the same ON-dendrite section midpoint,
        # so a single v_local recording per synapse index suffices.
        seg: Any = bip.get_segment()
        v_v: Any = h.Vector()
        v_v.record(seg._ref_v, RECORD_DT_MS)
        v_local.append(v_v)

    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t, RECORD_DT_MS)

    return BedARecorders(
        g_ampa=g_ampa,
        g_nmda=g_nmda,
        g_gaba=g_gaba,
        g_ach=g_ach,
        v_local=v_local,
        t_rec=t_rec,
        num_synapses=num_synapses,
    )


def _vectors_to_2d_array(*, vectors: list[Any]) -> np.ndarray:
    """Stack a list of NEURON Vectors into a (n_synapses, n_samples) numpy array."""
    assert len(vectors) > 0, "vector list is non-empty"
    arrays: list[np.ndarray] = [np.array(list(v), dtype=np.float64) for v in vectors]
    sizes: set[int] = {arr.size for arr in arrays}
    assert len(sizes) == 1, (
        f"Recorder vectors have inconsistent lengths: {sorted(sizes)}; recorder may "
        "have been attached after some traces started recording."
    )
    return np.stack(arrays, axis=0)


def _save_one_type(
    *,
    output_path: Path,
    g_vectors: list[Any],
    v_vectors: list[Any],
    t_rec: Any,
    e_rev_mv: float,
) -> None:
    """Stack vectors to numpy and save a compressed .npz with g_traces, v_local_traces, t_ms."""
    g_traces: np.ndarray = _vectors_to_2d_array(vectors=g_vectors)
    v_local_traces: np.ndarray = _vectors_to_2d_array(vectors=v_vectors)
    t_ms: np.ndarray = np.array(list(t_rec), dtype=np.float64)
    assert g_traces.shape == v_local_traces.shape, (
        f"g_traces shape {g_traces.shape} != v_local_traces shape {v_local_traces.shape}"
    )
    assert g_traces.shape[1] == t_ms.size, (
        f"g_traces n_samples {g_traces.shape[1]} != t_ms size {t_ms.size}"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output_path,
        **{
            G_TRACES_KEY: g_traces.astype(np.float64),
            V_LOCAL_TRACES_KEY: v_local_traces.astype(np.float64),
            T_MS_KEY: t_ms.astype(np.float64),
            E_REV_MV_KEY: np.array(e_rev_mv, dtype=np.float64),
        },
    )
    print(
        f"  wrote {output_path.name}: g_traces={g_traces.shape}, "
        f"v_local_traces={v_local_traces.shape}, t_ms={t_ms.shape}, "
        f"e_rev={e_rev_mv} mV, size={output_path.stat().st_size} B"
    )


def _save_bed_a_direction(
    *,
    direction: Direction,
    recorders: BedARecorders,
) -> None:
    """Save four .npz files (AMPA, NMDA, GABA, ACh) for one direction."""
    file_for_type: dict[RecordedSynapseType, Path] = {
        RecordedSynapseType.AMPA: (
            BED_A_PD_AMPA_NPZ if direction == Direction.PD else BED_A_ND_AMPA_NPZ
        ),
        RecordedSynapseType.NMDA: (
            BED_A_PD_NMDA_NPZ if direction == Direction.PD else BED_A_ND_NMDA_NPZ
        ),
        RecordedSynapseType.GABA: (
            BED_A_PD_GABA_NPZ if direction == Direction.PD else BED_A_ND_GABA_NPZ
        ),
        RecordedSynapseType.ACH: (
            BED_A_PD_ACH_NPZ if direction == Direction.PD else BED_A_ND_ACH_NPZ
        ),
    }
    g_for_type: dict[RecordedSynapseType, list[Any]] = {
        RecordedSynapseType.AMPA: recorders.g_ampa,
        RecordedSynapseType.NMDA: recorders.g_nmda,
        RecordedSynapseType.GABA: recorders.g_gaba,
        RecordedSynapseType.ACH: recorders.g_ach,
    }
    e_for_type: dict[RecordedSynapseType, float] = {
        RecordedSynapseType.AMPA: E_AMPA_MV,
        RecordedSynapseType.NMDA: E_NMDA_MV,
        RecordedSynapseType.GABA: E_GABA_BED_A_MV,
        RecordedSynapseType.ACH: E_ACH_BED_A_MV,
    }
    for syn_type in (
        RecordedSynapseType.AMPA,
        RecordedSynapseType.NMDA,
        RecordedSynapseType.GABA,
        RecordedSynapseType.ACH,
    ):
        _save_one_type(
            output_path=file_for_type[syn_type],
            g_vectors=g_for_type[syn_type],
            v_vectors=recorders.v_local,
            t_rec=recorders.t_rec,
            e_rev_mv=e_for_type[syn_type],
        )


def _run_bed_a_one_direction(
    *,
    h: Any,
    direction: Direction,
    gabamod_value: float,
) -> None:
    """Apply params, attach fresh recorders, run one trial, save .npz files."""
    print(f"\n=== Bed A {direction.value.upper()} (gabaMOD={gabamod_value:.2f}) ===")
    apply_params(h, seed=SEED)
    h.gabaMOD = gabamod_value
    h("update()")
    h("placeBIP()")

    recorders: BedARecorders = _attach_bed_a_recorders(h=h)
    assert recorders.num_synapses == BED_A_N_SYNAPSES, (
        f"Expected {BED_A_N_SYNAPSES} ON synapses, got {recorders.num_synapses}"
    )

    h.finitialize(V_INIT_MV)
    h.continuerun(TSTOP_MS)

    _save_bed_a_direction(direction=direction, recorders=recorders)


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Building Bed A cell (Poleg-Polsky 2016 deposited)...")
    h: Any = build_dsgc()
    n_syn: int = int(h.RGC.numsyn)
    print(f"Bed A cell ready: numsyn={n_syn}")
    assert n_syn == BED_A_N_SYNAPSES, f"Expected {BED_A_N_SYNAPSES} ON synapses, got {n_syn}"

    _run_bed_a_one_direction(h=h, direction=Direction.PD, gabamod_value=GABA_MOD_PD)
    _run_bed_a_one_direction(h=h, direction=Direction.ND, gabamod_value=GABA_MOD_ND)
    print("\nBed A trials complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
