"""Per-synapse recorder for Pareto deep-dive trials, plus per-segment
``seg.ina`` recorder used by the t0123 ATP-per-spike recipe.

Helpers ``_attach_bed_b_recorders``, ``BedBRecorders``, ``_save_one_type``,
``_save_bed_b_direction`` are COPIED verbatim from
``tasks/t0072_synaptic_traces_pd_nd/code/run_bed_b.py`` (lines 203-327) per the
project's cross-task code-reuse rule (these are private helpers, not a
registered library).

Adapted to the t0076 SynapseBundle (which carries variable-length syns_ach /
syns_gaba lists rather than always-equal-to-terminal-count lists).

t0123 extension: ``attach_ina_recorders_for_atp`` attaches per-segment
``Vector.record(seg._ref_ina, RECORD_DT_MS)`` handles for soma + AIS
proximal + AIS distal + every dendrite segment. Used inside FULL-mode
trials by ``evaluator.evaluate_68d_vector`` to integrate inward Na
charge per AP per compartment via ``atp_per_spike.compute_atp_per_ap``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyResult,
)
from tasks.t0128_t0127_rerun_dsi_atp_3seeds.code.atp_per_spike import UM2_TO_CM2
from tasks.t0128_t0127_rerun_dsi_atp_3seeds.code.constants_electrophys import (
    ACH_EREV_MV,
    DT_MS,
    GABA_EREV_MV,
    RECORD_DT_MS,
)
from tasks.t0128_t0127_rerun_dsi_atp_3seeds.code.trial_helpers import SynapseBundle

# ATP recipe sampling interval: record seg.ina, soma Vm, and the time
# vector at the simulation timestep (DT_MS = 0.1 ms) so the AP-window
# integration has enough samples to capture each ~1-2 ms AP. The legacy
# RECORD_DT_MS = 1.0 ms used by the per-synapse recorder is too coarse
# to integrate the fast Na transient.
ATP_RECORD_DT_MS: float = DT_MS

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


@dataclass(slots=True)
class InaRecorders:
    """Per-segment ``seg.ina`` Vector handles grouped by compartment kind.

    ``soma_ina[i] = (vec, area_cm2)`` where ``vec`` is the NEURON Vector
    handle and ``area_cm2 = seg.area() * UM2_TO_CM2``. Same shape for
    ``ais_ina`` and ``dend_ina``. ``v_soma`` and ``t_rec`` are convenience
    handles so AP detection can run on the somatic Vm trace from the same
    recording window.
    """

    soma_ina: list[tuple[Any, float]] = field(default_factory=list)
    ais_ina: list[tuple[Any, float]] = field(default_factory=list)
    dend_ina: list[tuple[Any, float]] = field(default_factory=list)
    v_soma: Any = None
    t_rec: Any = None


def _attach_section_ina(*, h: Any, sec: Any, sink: list[tuple[Any, float]]) -> None:
    for seg in sec:
        vec = h.Vector()
        vec.record(seg._ref_ina, ATP_RECORD_DT_MS)
        area_cm2 = float(seg.area()) * UM2_TO_CM2
        sink.append((vec, area_cm2))


def attach_ina_recorders_for_atp(*, h: Any, cell: MorphologyResult) -> InaRecorders:
    """Attach ``Vector.record(seg._ref_ina, ATP_RECORD_DT_MS)`` to every
    segment in soma + AIS proximal + AIS distal + every dendrite section.

    Per-segment ``seg.area()`` is captured once at attach time (the
    realised geometry returned by the t0092 patched generator does not
    change over the trial). Handles are reset whenever NEURON re-initialises
    via ``h.finitialize`` -- the caller must re-attach before each trial.

    Returns an ``InaRecorders`` with the per-segment Vector handles plus
    the somatic Vm recorder (for AP detection) and a time recorder. All
    recordings sample at ``ATP_RECORD_DT_MS = DT_MS = 0.1 ms`` so the AP
    window integration has enough samples to capture the fast Na transient.
    """
    out = InaRecorders()
    _attach_section_ina(h=h, sec=cell.soma, sink=out.soma_ina)
    for sec in (cell.ais_proximal, cell.ais_distal):
        _attach_section_ina(h=h, sec=sec, sink=out.ais_ina)
    for sec in cell.all_dends:
        _attach_section_ina(h=h, sec=sec, sink=out.dend_ina)
    v_soma_vec = h.Vector()
    v_soma_vec.record(cell.soma(0.5)._ref_v, ATP_RECORD_DT_MS)
    out.v_soma = v_soma_vec
    t_rec = h.Vector()
    t_rec.record(h._ref_t, ATP_RECORD_DT_MS)
    out.t_rec = t_rec
    return out


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
