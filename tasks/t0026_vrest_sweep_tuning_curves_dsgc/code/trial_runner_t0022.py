"""t0022 per-dendrite E-I trial runner with a V_rest override hook.

This module is a close copy of the per-dendrite E-I trial runner from
``tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py`` with two
modifications:

1. ``run_one_trial_vrest`` accepts an additional ``v_rest_mv`` parameter and
   calls ``set_vrest(h, v_rest_mv)`` AFTER ``apply_params`` and BEFORE
   ``h.finitialize(...)``.
2. ``build_cell_and_pairs`` is factored out so the cell is built exactly once
   and reused across (V_rest, angle, trial) combinations.

Library imports (permitted cross-task because the source files are listed in
the t0008 and t0022 library-asset ``module_paths``):

* ``tasks.t0008_port_modeldb_189347.code.build_cell``
* ``tasks.t0022_modify_dsgc_channel_testbed.code.constants``
* ``tasks.t0022_modify_dsgc_channel_testbed.code.neuron_bootstrap``
* ``tasks.t0022_modify_dsgc_channel_testbed.code.paths``
* ``tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve`` (only for
  the helper builders that are stable across V_rest values).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tasks.t0022_modify_dsgc_channel_testbed.code.neuron_bootstrap import (
    ensure_neuron_importable,
)

ensure_neuron_importable()


# ruff: noqa: E402  -- deferred imports; NEURON bootstrap must run first.
from tasks.t0008_port_modeldb_189347.code.build_cell import (
    SynapseCoords,
    apply_params,
    build_dsgc,
    read_synapse_coords,
)
from tasks.t0022_modify_dsgc_channel_testbed.code.constants import (
    AP_THRESHOLD_MV,
    BAR_VELOCITY_UM_PER_MS,
    GABA_CONDUCTANCE_NULL_NS,
    GABA_CONDUCTANCE_PREFERRED_NS,
    TSTOP_MS,
)
from tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve import (
    EiPair,
    _assert_bip_and_gabamod_baseline,
    _count_threshold_crossings,
    _preload_nrnmech_dll,
    _silence_baseline_hoc_synapses,
    _source_channel_partition_hoc,
    build_ei_pairs,
    schedule_ei_onsets,
)
from tasks.t0026_vrest_sweep_tuning_curves_dsgc.code.vrest_override import (
    set_vrest,
)


@dataclass(slots=True)
class CellContext:
    """Holds the NEURON handle plus the pre-built E-I pair list.

    The cell is built once at import time of the full sweep, and this context
    is reused across all (V_rest, angle, trial) triples.
    """

    h: Any
    pairs: list[EiPair]
    baseline_coords: list[SynapseCoords]
    baseline_gaba_mod: float


@dataclass(frozen=True, slots=True)
class TrialOutcome:
    """Per-trial outcome: firing rate, spike count, and peak voltage."""

    spike_count: int
    peak_mv: float
    firing_rate_hz: float


def build_cell_context() -> CellContext:
    """Preload nrnmech.dll, build the DSGC cell, and construct E-I pairs."""
    _preload_nrnmech_dll()
    h = build_dsgc()
    _source_channel_partition_hoc(h=h)
    pairs: list[EiPair] = build_ei_pairs(h=h)
    baseline_coords: list[SynapseCoords] = read_synapse_coords(h=h)
    baseline_gaba_mod: float = float(h.gabaMOD)
    return CellContext(
        h=h,
        pairs=pairs,
        baseline_coords=baseline_coords,
        baseline_gaba_mod=baseline_gaba_mod,
    )


def run_one_trial_vrest(
    *,
    ctx: CellContext,
    angle_deg: float,
    trial_seed: int,
    v_rest_mv: float,
) -> TrialOutcome:
    """Run one per-dendrite E-I trial at ``angle_deg`` with V_rest override.

    Steps exactly match t0022's ``run_one_trial_dendritic`` with a
    ``set_vrest`` call inserted between ``apply_params`` (which would otherwise
    restore ``h.v_init`` and the per-section ``eleak_HHst`` / ``e_pas`` to
    their t0008 defaults) and ``h.finitialize`` (which reads ``v_init``).
    """
    h: Any = ctx.h

    apply_params(h, seed=trial_seed)
    _silence_baseline_hoc_synapses(h=h)
    _assert_bip_and_gabamod_baseline(
        h=h,
        baseline_coords=ctx.baseline_coords,
        baseline_gaba_mod=ctx.baseline_gaba_mod,
    )

    schedule_ei_onsets(
        h=h,
        pairs=ctx.pairs,
        angle_deg=angle_deg,
        velocity_um_per_ms=BAR_VELOCITY_UM_PER_MS,
        gaba_null_pref_ratio=GABA_CONDUCTANCE_NULL_NS / GABA_CONDUCTANCE_PREFERRED_NS,
        trial_seed=trial_seed,
    )

    # V_rest override: set v_init, eleak_HHst, and e_pas on every section.
    # Must run AFTER apply_params (which resets v_init) and BEFORE
    # h.finitialize (which equilibrates membrane voltage from v_init).
    set_vrest(h=h, v_rest_mv=v_rest_mv)

    v_rec: Any = h.Vector()
    v_rec.record(h.RGC.soma(0.5)._ref_v)

    h.finitialize(float(v_rest_mv))
    h.continuerun(TSTOP_MS)

    samples: list[float] = [float(v) for v in v_rec]
    spike_count: int = _count_threshold_crossings(
        samples=samples,
        threshold_mv=AP_THRESHOLD_MV,
    )
    peak_mv: float = max(samples) if len(samples) > 0 else float("nan")
    tstop_s: float = TSTOP_MS / 1000.0
    firing_rate_hz: float = float(spike_count) / tstop_s
    return TrialOutcome(
        spike_count=spike_count,
        peak_mv=peak_mv,
        firing_rate_hz=firing_rate_hz,
    )
