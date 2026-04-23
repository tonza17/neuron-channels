"""t0024 de Rosenroll correlated-AR(2) per-trial runner for the distal-diameter sweep.

Close copy of ``tasks/t0034_distal_dendrite_length_sweep_t0024/code/trial_runner_length_t0024.py``
with ``sec.L`` replaced by ``seg.diam``:

1. The context carries the distal section list + baseline ``seg.diam`` snapshot + current multiplier
   so the outer sweep driver can call ``set_distal_diameter_multiplier`` ONCE per sweep point
   (``seg.diam`` is persistent state; rescaling per trial is wasted work).
2. ``run_one_trial_diameter`` does NOT accept ``rho`` as a parameter. The AR(2) cross-correlation
   is captured once at module scope from ``constants.AR2_CROSS_CORR_RHO_CORRELATED = 0.6`` (REQ-6).

All t0024 helpers (``_bar_arrival_times``, ``_rates_with_ar2_noise``, ``_rates_to_events``,
``_gaba_prob_for_direction``, ``_count_spikes``, ``_setup_synapses``, ``SynapseBundle``,
``BASE_ACH_PROB``, ``RATE_DT_MS``) are imported from the ``de_rosenroll_2026_dsgc`` library at
``tasks/t0024_port_de_rosenroll_2026_dsgc/code/``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import (
    DSGCCell,
    build_dsgc_cell,
)
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.run_tuning_curve import (
    BASE_ACH_PROB,
    RATE_DT_MS,
    SynapseBundle,
    _bar_arrival_times,
    _count_spikes,
    _gaba_prob_for_direction,
    _rates_to_events,
    _rates_with_ar2_noise,
    _setup_synapses,
)
from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.diameter_override_t0024 import (
    snapshot_distal_diameters,
)
from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.distal_selector_t0024 import (
    identify_distal_sections_t0024,
)

# AR(2) rho captured once at module scope. Never overridden at call sites (REQ-6).
_AR2_RHO: float = C.AR2_CROSS_CORR_RHO_CORRELATED


@dataclass(slots=True)
class CellContextT0024Diameter:
    """Holds the built DSGC cell, synapse bundle, distal snapshot, and current multiplier."""

    cell: DSGCCell
    bundle: SynapseBundle
    distal_sections: list[Any]
    baseline_diam: dict[tuple[int, float], float]
    current_multiplier: float


@dataclass(frozen=True, slots=True)
class TrialOutcomeT0024Diameter:
    """Per-trial outcome: firing rate, spike count, and peak voltage."""

    spike_count: int
    peak_mv: float
    firing_rate_hz: float


def build_cell_context() -> CellContextT0024Diameter:
    """Build the DSGC cell, set up ACh + GABA synapses, snapshot distal ``seg.diam``.

    GABA weight scale is 1.0 (correlated condition). The outer sweep driver is responsible for
    calling ``set_distal_diameter_multiplier`` once per sweep point; ``current_multiplier`` is
    initialised to 1.0 (baseline) here.
    """
    cell = build_dsgc_cell()
    bundle = _setup_synapses(cell=cell, gaba_weight_scale=1.0)
    distal_sections: list[Any] = identify_distal_sections_t0024(cell=cell)
    baseline_diam: dict[tuple[int, float], float] = snapshot_distal_diameters(
        h=cell.h,
        distal_sections=distal_sections,
    )
    return CellContextT0024Diameter(
        cell=cell,
        bundle=bundle,
        distal_sections=distal_sections,
        baseline_diam=baseline_diam,
        current_multiplier=1.0,
    )


def run_one_trial_diameter(
    *,
    ctx: CellContextT0024Diameter,
    direction_deg: float,
    trial_seed: int,
) -> TrialOutcomeT0024Diameter:
    """Run one t0024 bar-sweep trial at ``direction_deg`` with the current distal-diam override.

    Mirrors t0024's ``run_single_trial`` per-trial sequence:
    ``_bar_arrival_times`` -> ``_rates_with_ar2_noise(rho=_AR2_RHO, seed=trial_seed)`` ->
    ``_rates_to_events`` -> NetCon event queue via ``FInitializeHandler`` (keep-alive) ->
    ``h.finitialize(C.V_INIT_MV)`` -> ``h.run()`` -> ``_count_spikes``.

    Does NOT mutate ``seg.diam``; the outer sweep driver handles that once per sweep point.
    """
    cell: DSGCCell = ctx.cell
    bundle: SynapseBundle = ctx.bundle
    h: Any = cell.h

    n_syn: int = len(cell.terminal_dends)
    n_bins: int = int(np.ceil(C.TSTOP_MS / RATE_DT_MS))

    arrival = _bar_arrival_times(
        syn_xy=cell.terminal_locs_xy,
        origin_xy=cell.origin_xy,
        direction_deg=direction_deg,
    )

    ach_rates, gaba_rates = _rates_with_ar2_noise(
        n_syn=n_syn,
        n_bins=n_bins,
        rate_dt_ms=RATE_DT_MS,
        arrival_times_ms=arrival,
        rho=_AR2_RHO,
        seed=trial_seed,
    )

    gaba_prob: float = _gaba_prob_for_direction(direction_deg)
    ach_probs = np.full(n_syn, BASE_ACH_PROB, dtype=np.float64)
    gaba_probs = np.full(n_syn, gaba_prob, dtype=np.float64)

    rng = np.random.default_rng(trial_seed + 1_000_003)
    ach_events = _rates_to_events(
        rates_hz=ach_rates,
        release_prob=ach_probs,
        rate_dt_ms=RATE_DT_MS,
        rng=rng,
    )
    gaba_events = _rates_to_events(
        rates_hz=gaba_rates,
        release_prob=gaba_probs,
        rate_dt_ms=RATE_DT_MS,
        rng=rng,
    )

    def _queue() -> None:
        for i, nc in enumerate(bundle.ncs_ach):
            for t in ach_events[i]:
                if t < C.TSTOP_MS:
                    nc.event(t)
        for i, nc in enumerate(bundle.ncs_gaba):
            for t in gaba_events[i]:
                if t < C.TSTOP_MS:
                    nc.event(t)

    fih = h.FInitializeHandler(_queue)

    v_vec = h.Vector()
    v_vec.record(cell.soma(0.5)._ref_v)

    h.celsius = C.CELSIUS_DEG_C
    h.dt = C.DT_MS
    h.steps_per_ms = C.STEPS_PER_MS
    h.tstop = C.TSTOP_MS

    h.finitialize(C.V_INIT_MV)
    _ = fih  # keep alive -- without this the event queue is empty
    h.run()

    v = np.array(v_vec.to_python(), dtype=np.float64)
    spike_count: int = _count_spikes(v, C.AP_THRESHOLD_MV)
    peak_mv: float = float(v.max()) if v.size else float("nan")
    tstop_s: float = C.TSTOP_MS / 1000.0
    firing_rate_hz: float = float(spike_count) / tstop_s
    return TrialOutcomeT0024Diameter(
        spike_count=int(spike_count),
        peak_mv=peak_mv,
        firing_rate_hz=firing_rate_hz,
    )
