"""Single-trial NEURON runner for the t0059 minimal DSGC.

Adapted from ``tasks/t0057_tonic_gaba_sweep_t0053/code/trial.py``. Three substantive changes per
the t0059 plan:

1. **Public ``gampa_ns`` parameter (REQ-7).** ``run_one_trial`` accepts ``gampa_ns`` and threads
   it into ``schedule_ei_onsets``. ``TrialResult`` carries the new ``gampa_ns`` field.

2. **HH save-and-zero on EPSP_PASSIVE / IPSP_PASSIVE (REQ-3).** The legacy ``AMPA_ONLY`` /
   ``GABA_ONLY`` modes are replaced by ``EPSP_PASSIVE`` / ``IPSP_PASSIVE``. Both passive modes
   save the HH ``gnabar`` / ``gkbar`` on each segment of the soma and AIS, then zero them, run
   the trial, and restore via try/finally. Dendrites have no HH mechanism so save-and-zero must
   NOT touch them.

3. **EPSP_PASSIVE zeros every fired pair's GABA**; **IPSP_PASSIVE zeros every pair's AMPA**.
   Both also save-and-zero HH so the soma response is the pure synaptic (passive) envelope.

The bar-locked GABA window comes from ``schedule_ei_onsets`` (no per-trial restore is needed
because the next ``schedule_ei_onsets`` call writes from a clean state).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.cell import CellHandles
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants import (
    AP_THRESHOLD_MV,
    BAR_VELOCITY_UM_PER_MS,
    DT_MS,
    TSTOP_MS,
    V_INIT_MV,
    TrialMode,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.synapses import (
    EiPair,
    ScheduleResult,
    schedule_ei_onsets,
)


@dataclass(frozen=True, slots=True)
class HhConductanceSnapshot:
    """Snapshot of the HH conductances on the soma + AIS taken before zeroing them.

    ``soma_gnabar`` / ``soma_gkbar`` / ``ais_gnabar`` / ``ais_gkbar`` are per-segment lists; the
    save-and-zero logic iterates ``for seg in section`` because NEURON's ``seg.hh.gnabar`` is
    segment-scoped. Most ``h.Section`` instances built from the t0009 SWC have a single segment
    (``nseg = 1``), but the snapshot supports the general case so changes to ``nseg`` do not
    silently drop conductance state.
    """

    soma_gnabar: list[float]
    soma_gkbar: list[float]
    ais_gnabar: list[float]
    ais_gkbar: list[float]


@dataclass(frozen=True, slots=True)
class TrialResult:
    mode: TrialMode
    angle_deg: float
    trial_seed: int
    gampa_ns: float
    gaba_base_ns: float
    t_ms: np.ndarray
    v_soma_mv: np.ndarray
    spike_times_ms: list[float]
    firing_rate_hz: float
    i_fired_mask: list[bool]
    i_active_fraction: float


def _save_and_zero_hh(*, cell: CellHandles) -> HhConductanceSnapshot:
    """Save HH gnabar / gkbar on every soma + AIS segment, then zero them.

    Dendrites are NOT touched (they have no ``hh`` mechanism in the t0009-calibrated
    morphology — only ``pas``). Attempting ``seg.hh.gnabar`` on a dendrite would raise.
    """
    soma_gnabar: list[float] = []
    soma_gkbar: list[float] = []
    for seg in cell.soma:
        soma_gnabar.append(float(seg.hh.gnabar))
        soma_gkbar.append(float(seg.hh.gkbar))
        seg.hh.gnabar = 0.0
        seg.hh.gkbar = 0.0

    ais_gnabar: list[float] = []
    ais_gkbar: list[float] = []
    for seg in cell.axon_initial_segment:
        ais_gnabar.append(float(seg.hh.gnabar))
        ais_gkbar.append(float(seg.hh.gkbar))
        seg.hh.gnabar = 0.0
        seg.hh.gkbar = 0.0

    return HhConductanceSnapshot(
        soma_gnabar=soma_gnabar,
        soma_gkbar=soma_gkbar,
        ais_gnabar=ais_gnabar,
        ais_gkbar=ais_gkbar,
    )


def _restore_hh(*, cell: CellHandles, snapshot: HhConductanceSnapshot) -> None:
    """Restore HH gnabar / gkbar on every soma + AIS segment from a snapshot.

    Idempotent: callers should always invoke this from a try/finally so HH is restored even when
    ``h.continuerun`` raises.
    """
    for idx, seg in enumerate(cell.soma):
        seg.hh.gnabar = snapshot.soma_gnabar[idx]
        seg.hh.gkbar = snapshot.soma_gkbar[idx]
    for idx, seg in enumerate(cell.axon_initial_segment):
        seg.hh.gnabar = snapshot.ais_gnabar[idx]
        seg.hh.gkbar = snapshot.ais_gkbar[idx]


def _apply_mode_weights(*, pairs: list[EiPair], mode: TrialMode) -> None:
    """Override per-mode weights *after* :func:`schedule_ei_onsets` has set the FULL weights.

    * FULL: keep the FULL-mode weights set by schedule_ei_onsets (gated I, full E).
    * EPSP_PASSIVE: zero every tonic GABA conductance regardless of the gate (so the trace is
      pure AMPA + passive cable).
    * IPSP_PASSIVE: zero every AMPA NetCon weight (so the trace is pure tonic GABA + passive
      cable).

    HH save-and-zero is performed by the caller (run_one_trial) inside a try/finally — not here.
    """
    if mode == TrialMode.FULL:
        return
    if mode == TrialMode.EPSP_PASSIVE:
        for pair in pairs:
            pair.gaba_syn.g = 0.0
            pair.gaba_syn.t_on = 0.0
            pair.gaba_syn.t_off = 0.0
        return
    if mode == TrialMode.IPSP_PASSIVE:
        for pair in pairs:
            pair.ampa_netcon.weight[0] = 0.0
        return
    raise AssertionError(f"Unhandled TrialMode: {mode}")


def run_one_trial(
    *,
    h: Any,
    cell: CellHandles,
    pairs: list[EiPair],
    mode: TrialMode,
    angle_deg: float,
    trial_seed: int,
    gampa_ns: float,
    gaba_base_ns: float,
) -> TrialResult:
    """Run one trial and return a :class:`TrialResult`.

    The seed parameter is propagated for reproducibility tracking; the underlying simulation is
    deterministic (NetStim with ``noise=0`` for AMPA, no NetStim/NetCon for tonic GABA), so the
    seed only labels the row in output CSVs.

    For EPSP_PASSIVE / IPSP_PASSIVE the HH conductances on soma and AIS are saved and zeroed
    before ``h.continuerun`` and restored in a finally block — so HH is never silently disabled
    for subsequent trials, even if the integrator raises mid-trial.
    """
    _ = trial_seed  # currently advisory; trial is deterministic with noise=0

    h.dt = DT_MS

    schedule: ScheduleResult = schedule_ei_onsets(
        pairs=pairs,
        angle_deg=angle_deg,
        velocity_um_per_ms=BAR_VELOCITY_UM_PER_MS,
        gampa_ns=gampa_ns,
        gaba_base_ns=gaba_base_ns,
    )
    n_pairs: int = len(schedule.i_fired_mask)
    assert n_pairs > 0, "ScheduleResult must contain at least one pair"
    i_active_fraction: float = float(sum(schedule.i_fired_mask)) / float(n_pairs)

    # FULL is the default scheduled state; mode-specific weight overrides happen here.
    _apply_mode_weights(pairs=pairs, mode=mode)

    # Voltage and time vectors.
    v_rec: Any = h.Vector()
    v_rec.record(cell.soma(0.5)._ref_v)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t)

    # Spike detection on soma._ref_v.
    spike_vec: Any = h.Vector()
    netcon: Any = h.NetCon(cell.soma(0.5)._ref_v, None, sec=cell.soma)
    netcon.threshold = AP_THRESHOLD_MV
    netcon.record(spike_vec)

    snapshot: HhConductanceSnapshot | None = None
    try:
        if mode in {TrialMode.EPSP_PASSIVE, TrialMode.IPSP_PASSIVE}:
            snapshot = _save_and_zero_hh(cell=cell)
        h.finitialize(V_INIT_MV)
        h.continuerun(TSTOP_MS)
    finally:
        if snapshot is not None:
            _restore_hh(cell=cell, snapshot=snapshot)

    v_arr: np.ndarray = np.array(list(v_rec), dtype=np.float64)
    t_arr: np.ndarray = np.array(list(t_rec), dtype=np.float64)
    spike_times_ms: list[float] = [float(s) for s in spike_vec]
    firing_rate_hz: float = float(len(spike_times_ms)) / (TSTOP_MS / 1000.0)

    # Restore base FULL-mode weights on the AMPA NetCons for IPSP_PASSIVE mode (so subsequent
    # trials' schedule_ei_onsets always writes from a clean state). For EPSP_PASSIVE the next
    # schedule_ei_onsets call resets gaba_syn.{g,t_on,t_off} regardless.
    if mode == TrialMode.IPSP_PASSIVE:
        ampa_weight_us: float = gampa_ns * 1e-3
        for pair in pairs:
            pair.ampa_netcon.weight[0] = ampa_weight_us

    return TrialResult(
        mode=mode,
        angle_deg=angle_deg,
        trial_seed=trial_seed,
        gampa_ns=gampa_ns,
        gaba_base_ns=gaba_base_ns,
        t_ms=t_arr,
        v_soma_mv=v_arr,
        spike_times_ms=spike_times_ms,
        firing_rate_hz=firing_rate_hz,
        i_fired_mask=schedule.i_fired_mask,
        i_active_fraction=i_active_fraction,
    )
