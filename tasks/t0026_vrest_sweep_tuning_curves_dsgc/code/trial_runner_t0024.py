"""t0024 de Rosenroll correlated-AR(2) trial runner with V_rest override.

Close copy of the per-trial driver from
``tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`` with two
modifications:

1. ``run_one_trial_vrest`` accepts a ``v_rest_mv`` parameter and calls
   ``set_vrest(h, v_rest_mv)`` after all per-trial setup and before
   ``h.finitialize``. The ``h.finitialize`` call uses ``v_rest_mv`` instead of
   ``C.V_INIT_MV``.
2. The helper ``build_cell_and_synapses`` builds the DSGC cell and its ACh/GABA
   NetCon bundle exactly once; the context is reused across the (V_rest, angle,
   trial) sweep.

Library imports (permitted cross-task because the source files are listed in
t0024's ``module_paths``): ``tasks.t0024_port_de_rosenroll_2026_dsgc.code.*``.
"""

from __future__ import annotations

from dataclasses import dataclass

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
from tasks.t0026_vrest_sweep_tuning_curves_dsgc.code.vrest_override import (
    set_vrest,
)


@dataclass(slots=True)
class CellContextT0024:
    """Holds the built DSGC cell plus its ACh/GABA synapse bundle."""

    cell: DSGCCell
    bundle: SynapseBundle


@dataclass(frozen=True, slots=True)
class TrialOutcomeT0024:
    """Per-trial outcome: firing rate, spike count, and peak voltage."""

    spike_count: int
    peak_mv: float
    firing_rate_hz: float


def build_cell_context() -> CellContextT0024:
    """Build the DSGC cell and set up ACh + GABA synapses (correlated GABA).

    GABA weight scale is 1.0 for the correlated condition. The correlated /
    uncorrelated distinction lives in the ``rho`` argument passed to
    ``run_one_trial_vrest`` below, not in the synapse setup.
    """
    cell = build_dsgc_cell()
    bundle = _setup_synapses(cell=cell, gaba_weight_scale=1.0)
    return CellContextT0024(cell=cell, bundle=bundle)


def run_one_trial_vrest(
    *,
    ctx: CellContextT0024,
    direction_deg: float,
    rho: float,
    seed: int,
    v_rest_mv: float,
) -> TrialOutcomeT0024:
    """Run one t0024 bar-sweep trial at ``direction_deg`` with V_rest override.

    Steps match t0024's ``run_single_trial`` except that after setting
    ``h.celsius``, ``h.dt``, ``h.steps_per_ms``, and ``h.tstop`` we call
    ``set_vrest`` (which in turn sets ``h.v_init`` and every section's
    ``eleak_HHst``) before ``h.finitialize(v_rest_mv)``.
    """
    cell = ctx.cell
    bundle = ctx.bundle
    h = cell.h

    n_syn = len(cell.terminal_dends)
    n_bins = int(np.ceil(C.TSTOP_MS / RATE_DT_MS))

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
        rho=rho,
        seed=seed,
    )

    gaba_prob = _gaba_prob_for_direction(direction_deg)
    ach_probs = np.full(n_syn, BASE_ACH_PROB, dtype=np.float64)
    gaba_probs = np.full(n_syn, gaba_prob, dtype=np.float64)

    rng = np.random.default_rng(seed + 1_000_003)
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

    # V_rest override — MUST run after the per-trial h.* setters above, and
    # BEFORE h.finitialize so the steady-state solver uses the new leak
    # reversals when equilibrating the membrane.
    set_vrest(h=h, v_rest_mv=v_rest_mv)

    h.finitialize(float(v_rest_mv))
    _ = fih  # keep alive
    h.run()

    v = np.array(v_vec.to_python(), dtype=np.float64)
    spike_count = _count_spikes(v, C.AP_THRESHOLD_MV)
    peak_mv = float(v.max()) if v.size else float("nan")
    tstop_s: float = C.TSTOP_MS / 1000.0
    firing_rate_hz: float = float(spike_count) / tstop_s
    return TrialOutcomeT0024(
        spike_count=int(spike_count),
        peak_mv=peak_mv,
        firing_rate_hz=firing_rate_hz,
    )
