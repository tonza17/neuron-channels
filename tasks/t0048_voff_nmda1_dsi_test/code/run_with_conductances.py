"""Thin Python wrapper around t0046's ``run_one_trial`` that records per-synapse conductances.

COPIED from ``tasks/t0047_validate_pp16_fig3_cond_noise/code/run_with_conductances.py``
per the project's cross-task code-reuse rule (t0047 is not a registered library
asset; only ``modeldb_189347_dsgc_exact`` from t0046 is library-registered, so its
recorder code must be COPIED into this task with attribution rather than imported).
Use case: t0048's Voff_bipNMDA = 1 sweep needs the same per-synapse NMDA / AMPA /
GABA recorder pattern that t0047 used so the two tasks' conductance values are
directly comparable. Only the ``constants`` import path was re-targeted from
``tasks.t0047...`` to ``tasks.t0048...``; the t0046 imports stay identical, and the
manual smoke-test block at the file's end was deleted (it is invoked only manually
and would re-import a t0047 path that no longer applies). Original attribution
preserved below.

The wrapper attaches NEURON ``Vector.record(syn._ref_*, dt_record_ms)`` handles to every
synapse's conductance state variable ONCE (after the first call to ``run_one_trial`` has
ensured the cell is built), then re-uses the same recorder vectors across all trials. After
each ``run_one_trial`` invocation, the wrapper extracts per-class summed peak conductance
in nS (max over time of the per-time-step sum across all ~282 synapses) and computes
per-class summed peak current offline as ``i_nA = (1e-3) * g_nS * (v_mV - e_mV)``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (
    Direction,
    ExperimentType,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import (
    TrialResult,
    _ensure_cell,
    run_one_trial,
)
from tasks.t0048_voff_nmda1_dsi_test.code.constants import (
    DT_RECORD_MS,
    E_BIPNMDA_MV,
    E_SACEXC_MV,
    E_SACINHIB_MV_OVERRIDE,
)


@dataclass(frozen=True, slots=True)
class ConductanceRecorders:
    """Container of NEURON Vector handles, one per synapse per channel.

    All four ``g_*`` lists have ``len == num_synapses`` and indices align across lists
    (i.e. ``g_ampa[i]`` and ``g_nmda[i]`` belong to ``BIPsyn[i]``).
    """

    g_ampa: list[Any]
    g_nmda: list[Any]
    g_sacexc: list[Any]
    g_sacinhib: list[Any]
    v_soma: Any
    t_rec: Any
    num_synapses: int


@dataclass(frozen=True, slots=True)
class TrialResultWithConductances:
    """One drifting-bar trial's PSP plus per-synapse-class peak conductance / current."""

    trial: TrialResult
    peak_g_nmda_summed_ns: float
    peak_g_ampa_summed_ns: float
    peak_g_sacexc_summed_ns: float
    peak_g_sacinhib_summed_ns: float
    peak_g_nmda_per_syn_mean_ns: float
    peak_g_ampa_per_syn_mean_ns: float
    peak_g_sacexc_per_syn_mean_ns: float
    peak_g_sacinhib_per_syn_mean_ns: float
    peak_i_nmda_summed_na: float
    peak_i_ampa_summed_na: float
    peak_i_sacexc_summed_na: float
    peak_i_sacinhib_summed_na: float
    v_trace_mv: list[float] | None = field(default=None)
    t_trace_ms: list[float] | None = field(default=None)


def build_cell_and_attach_recorders(
    *,
    dt_record_ms: float = DT_RECORD_MS,
) -> ConductanceRecorders:
    """Ensure t0046's cell is built (idempotent), then attach recorders to ``h``.

    This is the canonical entry point for sweep drivers; it guarantees that the cell is
    built exactly once per process before recorders are attached, satisfying the research
    finding that ``placeBIP()`` only re-binds Vinf playback vectors and the synapse
    POINT_PROCESS objects persist across trials.
    """
    h, _ = _ensure_cell()
    return attach_conductance_recorders(h=h, dt_record_ms=dt_record_ms)


def attach_conductance_recorders(
    *,
    h: Any,
    dt_record_ms: float = DT_RECORD_MS,
) -> ConductanceRecorders:
    """Attach per-synapse Vector.record handles for all four channels.

    Idempotent in the sense that a fresh ConductanceRecorders is returned each call;
    the caller is responsible for using a single instance for the duration of a sweep.
    """
    num_synapses: int = int(h.RGC.numsyn)
    g_ampa: list[Any] = []
    g_nmda: list[Any] = []
    g_sacexc: list[Any] = []
    g_sacinhib: list[Any] = []

    for idx in range(num_synapses):
        bip = h.RGC.BIPsyn[idx]
        sacexc = h.RGC.SACexcsyn[idx]
        sacinhib = h.RGC.SACinhibsyn[idx]

        v_ampa: Any = h.Vector()
        v_ampa.record(bip._ref_gAMPA, dt_record_ms)
        g_ampa.append(v_ampa)

        v_nmda: Any = h.Vector()
        v_nmda.record(bip._ref_gNMDA, dt_record_ms)
        g_nmda.append(v_nmda)

        v_sacexc: Any = h.Vector()
        v_sacexc.record(sacexc._ref_g, dt_record_ms)
        g_sacexc.append(v_sacexc)

        v_sacinhib: Any = h.Vector()
        v_sacinhib.record(sacinhib._ref_g, dt_record_ms)
        g_sacinhib.append(v_sacinhib)

    v_soma: Any = h.Vector()
    v_soma.record(h.RGC.soma(0.5)._ref_v, dt_record_ms)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t, dt_record_ms)

    return ConductanceRecorders(
        g_ampa=g_ampa,
        g_nmda=g_nmda,
        g_sacexc=g_sacexc,
        g_sacinhib=g_sacinhib,
        v_soma=v_soma,
        t_rec=t_rec,
        num_synapses=num_synapses,
    )


def _peak_summed_g_ns(*, vectors: list[Any]) -> tuple[float, np.ndarray]:
    """Return (peak of per-step sum across synapses, the per-step sum trace)."""
    if len(vectors) == 0:
        return 0.0, np.zeros(0, dtype=np.float64)
    arrays: list[np.ndarray] = [np.array(list(v), dtype=np.float64) for v in vectors]
    # Some vectors may be of different lengths if the recorder was attached after
    # the simulation began; reject this defensively.
    sizes: set[int] = {arr.size for arr in arrays}
    assert len(sizes) == 1, (
        f"Recorder vectors have inconsistent lengths: {sorted(sizes)}; recorder may "
        "have been attached after some traces started recording."
    )
    summed: np.ndarray = np.sum(np.stack(arrays, axis=0), axis=0)
    return float(summed.max()), summed


def _peak_summed_i_na(
    *,
    g_summed_ns: np.ndarray,
    v_mv: np.ndarray,
    e_mv: float,
) -> float:
    """Compute peak abs(i) over the trial: i_nA = (1e-3) * g_nS_summed * (v_mV - e_mV)."""
    if g_summed_ns.size == 0 or v_mv.size == 0:
        return 0.0
    n: int = min(g_summed_ns.size, v_mv.size)
    i_na: np.ndarray = 1e-3 * g_summed_ns[:n] * (v_mv[:n] - e_mv)
    return float(np.max(np.abs(i_na)))


def _reset_recorders(*, recorders: ConductanceRecorders) -> None:
    """Discard recorded data so the next trial starts at sample index 0."""
    for v in recorders.g_ampa:
        v.resize(0)
    for v in recorders.g_nmda:
        v.resize(0)
    for v in recorders.g_sacexc:
        v.resize(0)
    for v in recorders.g_sacinhib:
        v.resize(0)
    recorders.v_soma.resize(0)
    recorders.t_rec.resize(0)


def run_one_trial_with_conductances(
    *,
    recorders: ConductanceRecorders,
    exptype: ExperimentType,
    direction: Direction,
    trial_seed: int,
    flicker_var: float = 0.0,
    stim_noise_var: float = 0.0,
    b2gnmda_override: float | None = None,
    record_spikes: bool = False,
    return_traces: bool = False,
) -> TrialResultWithConductances:
    """Run one trial via t0046's ``run_one_trial`` and extract per-class peak g and i."""
    trial: TrialResult = run_one_trial(
        exptype=exptype,
        direction=direction,
        trial_seed=trial_seed,
        flicker_var=flicker_var,
        stim_noise_var=stim_noise_var,
        b2gnmda_override=b2gnmda_override,
        record_spikes=record_spikes,
    )

    peak_g_ampa_summed_ns, summed_g_ampa = _peak_summed_g_ns(vectors=recorders.g_ampa)
    peak_g_nmda_summed_ns, summed_g_nmda = _peak_summed_g_ns(vectors=recorders.g_nmda)
    peak_g_sacexc_summed_ns, summed_g_sacexc = _peak_summed_g_ns(
        vectors=recorders.g_sacexc,
    )
    peak_g_sacinhib_summed_ns, summed_g_sacinhib = _peak_summed_g_ns(
        vectors=recorders.g_sacinhib,
    )

    v_arr: np.ndarray = np.array(list(recorders.v_soma), dtype=np.float64)
    t_arr: np.ndarray = np.array(list(recorders.t_rec), dtype=np.float64)

    peak_i_ampa_summed_na: float = _peak_summed_i_na(
        g_summed_ns=summed_g_ampa,
        v_mv=v_arr,
        e_mv=E_BIPNMDA_MV,
    )
    peak_i_nmda_summed_na: float = _peak_summed_i_na(
        g_summed_ns=summed_g_nmda,
        v_mv=v_arr,
        e_mv=E_BIPNMDA_MV,
    )
    peak_i_sacexc_summed_na: float = _peak_summed_i_na(
        g_summed_ns=summed_g_sacexc,
        v_mv=v_arr,
        e_mv=E_SACEXC_MV,
    )
    peak_i_sacinhib_summed_na: float = _peak_summed_i_na(
        g_summed_ns=summed_g_sacinhib,
        v_mv=v_arr,
        e_mv=E_SACINHIB_MV_OVERRIDE,
    )

    n_syn: int = max(1, recorders.num_synapses)
    v_trace_mv: list[float] | None = [float(x) for x in v_arr] if return_traces else None
    t_trace_ms: list[float] | None = [float(x) for x in t_arr] if return_traces else None

    result: TrialResultWithConductances = TrialResultWithConductances(
        trial=trial,
        peak_g_nmda_summed_ns=peak_g_nmda_summed_ns,
        peak_g_ampa_summed_ns=peak_g_ampa_summed_ns,
        peak_g_sacexc_summed_ns=peak_g_sacexc_summed_ns,
        peak_g_sacinhib_summed_ns=peak_g_sacinhib_summed_ns,
        peak_g_nmda_per_syn_mean_ns=peak_g_nmda_summed_ns / n_syn,
        peak_g_ampa_per_syn_mean_ns=peak_g_ampa_summed_ns / n_syn,
        peak_g_sacexc_per_syn_mean_ns=peak_g_sacexc_summed_ns / n_syn,
        peak_g_sacinhib_per_syn_mean_ns=peak_g_sacinhib_summed_ns / n_syn,
        peak_i_nmda_summed_na=peak_i_nmda_summed_na,
        peak_i_ampa_summed_na=peak_i_ampa_summed_na,
        peak_i_sacexc_summed_na=peak_i_sacexc_summed_na,
        peak_i_sacinhib_summed_na=peak_i_sacinhib_summed_na,
        v_trace_mv=v_trace_mv,
        t_trace_ms=t_trace_ms,
    )

    _reset_recorders(recorders=recorders)
    return result
