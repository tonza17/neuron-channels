"""Single-trial NEURON runner for the t0053 minimal DSGC (spatial centripetal-gating GABA).

Adapted from t0052's ``trial.py`` per CLAUDE.md rule 3 (cross-task code is copied, not imported).
The scalar ``gaba_mod_theta`` is replaced by the per-synapse ``i_fired_mask`` returned from
``schedule_ei_onsets``; ``i_active_fraction`` is the fraction of I synapses that fired this trial.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from tasks.t0053_minimal_dsgc_spatial_gaba.code.cell import CellHandles
from tasks.t0053_minimal_dsgc_spatial_gaba.code.constants import (
    AMPA_PEAK_NS,
    AP_THRESHOLD_MV,
    BAR_VELOCITY_UM_PER_MS,
    DT_MS,
    GABA_BASE_NS,
    TSTOP_MS,
    V_INIT_MV,
    TrialMode,
)
from tasks.t0053_minimal_dsgc_spatial_gaba.code.synapses import (
    EiPair,
    ScheduleResult,
    schedule_ei_onsets,
)


@dataclass(frozen=True, slots=True)
class TrialResult:
    mode: TrialMode
    angle_deg: float
    trial_seed: int
    t_ms: np.ndarray
    v_soma_mv: np.ndarray
    spike_times_ms: list[float]
    synapse_onset_times_ms: list[float]
    firing_rate_hz: float
    i_fired_mask: list[bool]
    i_active_fraction: float


def _apply_mode_weights(*, pairs: list[EiPair], mode: TrialMode) -> None:
    """Override per-mode weights *after* :func:`schedule_ei_onsets` has set the FULL weights.

    * FULL: keep the FULL-mode weights set by schedule_ei_onsets (gated I, full E).
    * AMPA_ONLY: zero every GABA NetCon weight regardless of the gate.
    * GABA_ONLY: zero every AMPA NetCon weight; I weights stay as set by the gate.
    """
    if mode == TrialMode.FULL:
        return
    if mode == TrialMode.AMPA_ONLY:
        for pair in pairs:
            pair.gaba_netcon.weight[0] = 0.0
        return
    if mode == TrialMode.GABA_ONLY:
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
) -> TrialResult:
    """Run one trial and return a :class:`TrialResult`.

    The seed parameter is propagated for reproducibility tracking; the underlying simulation is
    deterministic (NetStim with ``noise=0``), so the seed only labels the row in output CSVs.
    """
    _ = trial_seed  # currently advisory; trial is deterministic with noise=0

    h.dt = DT_MS

    schedule: ScheduleResult = schedule_ei_onsets(
        pairs=pairs,
        angle_deg=angle_deg,
        velocity_um_per_ms=BAR_VELOCITY_UM_PER_MS,
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

    h.finitialize(V_INIT_MV)
    h.continuerun(TSTOP_MS)

    v_arr: np.ndarray = np.array(list(v_rec), dtype=np.float64)
    t_arr: np.ndarray = np.array(list(t_rec), dtype=np.float64)
    spike_times_ms: list[float] = [float(s) for s in spike_vec]
    firing_rate_hz: float = float(len(spike_times_ms)) / (TSTOP_MS / 1000.0)

    # Restore base FULL-mode weights for the next trial in this run loop. Although
    # schedule_ei_onsets re-writes them at the next call, defensive resets ensure the cell is
    # in a known state if the caller pauses the loop or inspects pair state between trials.
    if mode == TrialMode.AMPA_ONLY:
        gaba_full_weight_us: float = GABA_BASE_NS * 1e-3
        for pair, fires in zip(pairs, schedule.i_fired_mask, strict=True):
            pair.gaba_netcon.weight[0] = gaba_full_weight_us if fires else 0.0
    elif mode == TrialMode.GABA_ONLY:
        ampa_weight_us: float = AMPA_PEAK_NS * 1e-3
        for pair in pairs:
            pair.ampa_netcon.weight[0] = ampa_weight_us

    return TrialResult(
        mode=mode,
        angle_deg=angle_deg,
        trial_seed=trial_seed,
        t_ms=t_arr,
        v_soma_mv=v_arr,
        spike_times_ms=spike_times_ms,
        synapse_onset_times_ms=schedule.onset_times_ms,
        firing_rate_hz=firing_rate_hz,
        i_fired_mask=schedule.i_fired_mask,
        i_active_fraction=i_active_fraction,
    )
