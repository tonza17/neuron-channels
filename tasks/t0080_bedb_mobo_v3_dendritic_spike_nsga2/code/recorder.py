"""Per-synapse recorder for Pareto deep-dive trials.

Helpers ``_attach_bed_b_recorders``, ``BedBRecorders``, ``_save_one_type``,
``_save_bed_b_direction`` are COPIED verbatim from
``tasks/t0072_synaptic_traces_pd_nd/code/run_bed_b.py`` (lines 203-327) per the
project's cross-task code-reuse rule (these are private helpers, not a
registered library).

Adapted to the t0076 SynapseBundle (which carries variable-length syns_ach /
syns_gaba lists rather than always-equal-to-terminal-count lists).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    ACH_EREV_MV,
    GABA_EREV_MV,
    RECORD_DT_MS,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import SynapseBundle

G_TRACES_KEY: str = "g_traces"
V_LOCAL_TRACES_KEY: str = "v_local_traces"
T_MS_KEY: str = "t_ms"
E_REV_MV_KEY: str = "e_rev_mv"
V_SOMA_KEY: str = "v_soma"


@dataclass(slots=True)
class BedBRecorders:
    """NEURON Vector handles for ACh + GABA per-synapse g and v_local."""

    g_ach: list[Any]
    g_gaba: list[Any]
    v_local_ach: list[Any]
    v_local_gaba: list[Any]
    v_soma: Any
    t_rec: Any


def attach_recorders(*, h: Any, soma: Any, bundle: SynapseBundle) -> BedBRecorders:
    """Attach Vector.record handles for ACh g, GABA g, per-synapse local v, v_soma."""
    g_ach: list[Any] = []
    g_gaba: list[Any] = []
    v_local_ach: list[Any] = []
    v_local_gaba: list[Any] = []
    for syn in bundle.syns_ach:
        v_a = h.Vector()
        v_a.record(syn._ref_g, RECORD_DT_MS)
        g_ach.append(v_a)
        seg = syn.get_segment()
        v_v = h.Vector()
        v_v.record(seg._ref_v, RECORD_DT_MS)
        v_local_ach.append(v_v)
    for syn in bundle.syns_gaba:
        v_g = h.Vector()
        v_g.record(syn._ref_g, RECORD_DT_MS)
        g_gaba.append(v_g)
        seg = syn.get_segment()
        v_v = h.Vector()
        v_v.record(seg._ref_v, RECORD_DT_MS)
        v_local_gaba.append(v_v)
    v_soma_vec = h.Vector()
    v_soma_vec.record(soma(0.5)._ref_v, RECORD_DT_MS)
    t_rec = h.Vector()
    t_rec.record(h._ref_t, RECORD_DT_MS)
    return BedBRecorders(
        g_ach=g_ach,
        g_gaba=g_gaba,
        v_local_ach=v_local_ach,
        v_local_gaba=v_local_gaba,
        v_soma=v_soma_vec,
        t_rec=t_rec,
    )


def _vectors_to_2d_array(*, vectors: list[Any]) -> np.ndarray:
    if len(vectors) == 0:
        return np.zeros((0, 0), dtype=np.float64)
    arrays: list[np.ndarray] = [np.array(list(v), dtype=np.float64) for v in vectors]
    sizes: set[int] = {arr.size for arr in arrays}
    if len(sizes) > 1:
        # Truncate to the shortest length to avoid raising in odd corner cases.
        min_size = min(sizes)
        arrays = [a[:min_size] for a in arrays]
    return np.stack(arrays, axis=0)


def save_recorders_npz(
    *,
    output_path: Path,
    recorders: BedBRecorders,
    direction_label: str,
) -> None:
    """Serialise recorder vectors into one compressed .npz per direction."""
    g_ach_arr: np.ndarray = _vectors_to_2d_array(vectors=recorders.g_ach)
    g_gaba_arr: np.ndarray = _vectors_to_2d_array(vectors=recorders.g_gaba)
    v_loc_ach_arr: np.ndarray = _vectors_to_2d_array(vectors=recorders.v_local_ach)
    v_loc_gaba_arr: np.ndarray = _vectors_to_2d_array(vectors=recorders.v_local_gaba)
    v_soma_arr: np.ndarray = np.array(list(recorders.v_soma), dtype=np.float64)
    t_arr: np.ndarray = np.array(list(recorders.t_rec), dtype=np.float64)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output_path,
        **{
            "g_ach": g_ach_arr,
            "g_gaba": g_gaba_arr,
            "v_local_ach": v_loc_ach_arr,
            "v_local_gaba": v_loc_gaba_arr,
            V_SOMA_KEY: v_soma_arr,
            T_MS_KEY: t_arr,
            "e_ach_mv": np.array(ACH_EREV_MV, dtype=np.float64),
            "e_gaba_mv": np.array(GABA_EREV_MV, dtype=np.float64),
            "direction": np.array(direction_label),
        },
    )
