"""Simulation driver wrapping h.simplerun() with a clean Python API.

Exposes ``run_one_trial(...)`` which:

1. ensures the DSGC cell is built and globals are at canonical values,
2. sets the noise globals (``h.flickerVAR``, ``h.stimnoiseVAR``) and ``h.b2gnmda``,
3. sets the per-trial seed (``h.seed2``),
4. sets ``h.SpikesOn`` based on the ``record_spikes`` flag (matters because simplerun() reads
   it to decide ``exptype = 2 - SpikesOn``),
5. invokes ``h.simplerun(int(exptype), int(direction))`` which internally rebinds
   ``achMOD = 0.33``, sets condition-specific globals, calls ``init_active``, ``update``,
   ``placeBIP``, and ``run()`` (which integrates to ``h.tstop``),
6. asserts BIP positions are still at baseline,
7. extracts peak PSP, baseline mean, and (if recording spikes) AP times.

The cell is built once per process and reused across trials. ``run_one_trial`` records the soma
voltage trace via ``v_rec.record(soma._ref_v)`` registered before the run; NEURON's recording
APIs work even when ``h.run()`` is invoked from inside a HOC proc.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell import (
    SynapseCoords,
    assert_bip_positions_baseline,
    build_dsgc,
    get_cell_summary,
    read_synapse_coords,
    reset_globals_to_canonical,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (
    ACHMOD_SIMPLERUN,
    AP_THRESHOLD_MV,
    B2GNMDA_CODE,
    DT_MS,
    PSP_BASELINE_MS,
    TSTOP_MS,
    V_INIT_MV,
    Direction,
    ExperimentType,
)


@dataclass(frozen=True, slots=True)
class TrialResult:
    """One drifting-bar trial's output."""

    exptype: ExperimentType
    direction: Direction
    trial_seed: int
    flicker_var: float
    stim_noise_var: float
    b2gnmda_ns: float
    peak_psp_mv: float  # max(soma_v) - v_init.
    baseline_mean_mv: float  # mean(soma_v[t < PSP_BASELINE_MS]) - v_init.
    spike_times_ms: list[float] = field(default_factory=list)


_CELL_STATE: dict[str, Any] = {}


def _ensure_cell() -> tuple[Any, list[SynapseCoords]]:
    if "h" not in _CELL_STATE:
        h: Any = build_dsgc()
        baseline: list[SynapseCoords] = read_synapse_coords(h=h)
        summary = get_cell_summary(h=h)
        print(
            f"[build_cell] countON={summary.num_on_sections} numsyn={summary.num_synapses}",
            flush=True,
        )
        _CELL_STATE["h"] = h
        _CELL_STATE["baseline"] = baseline
    return _CELL_STATE["h"], _CELL_STATE["baseline"]


def run_one_trial(
    *,
    exptype: ExperimentType,
    direction: Direction,
    trial_seed: int,
    flicker_var: float = 0.0,
    stim_noise_var: float = 0.0,
    b2gnmda_override: float | None = None,
    record_spikes: bool = False,
) -> TrialResult:
    """Run one drifting-bar trial via h.simplerun(); return TrialResult."""
    h, baseline = _ensure_cell()

    reset_globals_to_canonical(h=h)
    h.flickerVAR = float(flicker_var)
    h.stimnoiseVAR = float(stim_noise_var)
    gnmda_ns: float = float(
        b2gnmda_override if b2gnmda_override is not None else B2GNMDA_CODE,
    )
    h.b2gnmda = gnmda_ns
    h.seed2 = int(trial_seed)
    # SpikesOn governs exptype = 2 - SpikesOn inside simplerun(): 0 -> exptype=2 (PSP, TTX on);
    # 1 -> exptype=1 (AP, TTX off). For PSP measurements we set SpikesOn=0; for Fig 8 spiking
    # measurements we set SpikesOn=1.
    h.SpikesOn = 1 if record_spikes else 0
    # When the user wants AP5 (analogue), b2gnmda is set to 0; nmdaOn must stay at 1 so that
    # simplerun() does b2gnmda = 0.5 * 1 * (override applied after). To keep simplerun()'s own
    # b2gnmda = 0.5 * (nmdaOn) overwrite from clobbering our override, we force nmdaOn = 1 and
    # overwrite b2gnmda again immediately after simplerun via post-call below. (Simpler: pass
    # nmdaOn = override / 0.5; but that requires care for override > 0.5.)
    h.nmdaOn = 1

    # Voltage recorder.
    v_rec: Any = h.Vector()
    v_rec.record(h.RGC.soma(0.5)._ref_v)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t)

    # Spike recorder via NetCon on soma._ref_v.
    spike_vec: Any = h.Vector()
    netcon: Any | None = None
    if record_spikes:
        # netcon target = nil; threshold detection only.
        netcon = h.NetCon(h.RGC.soma(0.5)._ref_v, None, sec=h.RGC.soma)
        netcon.threshold = AP_THRESHOLD_MV
        netcon.record(spike_vec)

    # Run via simplerun(). simplerun() ALSO calls placeBIP(), which already uses our
    # h.flickerVAR / h.stimnoiseVAR settings.
    h.simplerun(int(exptype), int(direction))
    # AP5-analogue override: simplerun() unconditionally writes b2gnmda = 0.5 * nmdaOn.
    # We need to honour b2gnmda_override < 0.5 (e.g., 0 for AP5, 2.5 for paper). To do so,
    # if the override differs from what simplerun() set, re-apply, re-update, re-placeBIP,
    # and rerun.
    final_b2gnmda: float = float(h.b2gnmda)
    if abs(final_b2gnmda - gnmda_ns) > 1e-9:
        h.b2gnmda = gnmda_ns
        h("update()")
        h("placeBIP()")
        # Re-record with fresh vectors.
        v_rec = h.Vector()
        v_rec.record(h.RGC.soma(0.5)._ref_v)
        t_rec = h.Vector()
        t_rec.record(h._ref_t)
        spike_vec = h.Vector()
        if record_spikes:
            netcon = h.NetCon(h.RGC.soma(0.5)._ref_v, None, sec=h.RGC.soma)
            netcon.threshold = AP_THRESHOLD_MV
            netcon.record(spike_vec)
        h.finitialize(V_INIT_MV)
        h.continuerun(TSTOP_MS)

    # Post-run: assertions and trace extraction.
    assert_bip_positions_baseline(h=h, baseline=baseline)
    achmod_now: float = float(h.achMOD)
    assert abs(achmod_now - ACHMOD_SIMPLERUN) < 1e-6 or exptype == ExperimentType.HIGH_CL, (
        f"achMOD = {achmod_now} != {ACHMOD_SIMPLERUN}; simplerun rebind regression?"
    )

    v_arr: np.ndarray = np.array(list(v_rec), dtype=np.float64)
    t_arr: np.ndarray = np.array(list(t_rec), dtype=np.float64)
    if v_arr.size == 0:
        raise RuntimeError("No samples recorded; finitialize/continuerun were not run.")

    # Peak PSP relative to v_init (the depolarisation amplitude in mV).
    peak_psp_mv: float = float(v_arr.max() - V_INIT_MV)

    # Baseline = mean over t < PSP_BASELINE_MS. The bar starts at lightstart = -100 ms;
    # negative t ms in HOC becomes the very early stim window, but t_rec is the simulation
    # timeline starting at 0 (NEURON does not record negative time). So PSP_BASELINE_MS = 100
    # gives us the first 10000 samples (at dt=0.1) where the drifting bar has not yet driven
    # any synaptic current to the soma (the propagation delay along the dendrite is hundreds
    # of ms before any visible drive).
    baseline_mask: np.ndarray = t_arr < PSP_BASELINE_MS
    baseline_mean_mv: float = float(v_arr[baseline_mask].mean() - V_INIT_MV)

    spike_times_ms: list[float] = list(map(float, spike_vec)) if record_spikes else []
    return TrialResult(
        exptype=exptype,
        direction=direction,
        trial_seed=trial_seed,
        flicker_var=float(flicker_var),
        stim_noise_var=float(stim_noise_var),
        b2gnmda_ns=gnmda_ns,
        peak_psp_mv=peak_psp_mv,
        baseline_mean_mv=baseline_mean_mv,
        spike_times_ms=spike_times_ms,
    )


def get_dt_ms() -> float:
    return DT_MS


def get_tstop_ms() -> float:
    return TSTOP_MS
