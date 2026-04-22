"""t0022-compatible per-dendrite E-I trial runner with a distal-length override hook.

Structural clone of ``tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/trial_runner_t0022.py``.
Differences:

1. ``run_one_trial_length`` accepts ``distal_sections``, ``baseline_L``, and ``multiplier``
   parameters. It calls ``set_distal_length_multiplier`` after ``apply_params`` /
   ``_silence_baseline_hoc_synapses`` / ``_assert_bip_and_gabamod_baseline`` and before
   ``h.finitialize``. An ``assert_distal_lengths`` call immediately follows the override as a
   per-trial guard against silent rescale failures.
2. The NEURON bootstrap import runs at module scope before any ``neuron`` imports are attempted.
3. The cell context is built once via ``build_cell_context`` and reused across every (length,
   angle, trial) combination to amortise the ~1.6 s NEURON build cost (see research_code.md
   "The t0022 cell context must be built once per process, not per sweep point").

All t0022 helpers (``build_ei_pairs``, ``schedule_ei_onsets``, ``_preload_nrnmech_dll``,
``_source_channel_partition_hoc``, ``_silence_baseline_hoc_synapses``,
``_assert_bip_and_gabamod_baseline``, ``_count_threshold_crossings``) are imported from the t0022
library (the same pattern used by t0026 — these modules are registered in the
``modeldb_189347_dsgc_dendritic`` library ``module_paths``).
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
    V_INIT_MV,
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
from tasks.t0029_distal_dendrite_length_sweep_dsgc.code.length_override import (
    assert_distal_lengths,
    identify_distal_sections,
    set_distal_length_multiplier,
    snapshot_distal_lengths,
)


@dataclass(slots=True)
class CellContext:
    """Holds the NEURON handle, E-I pairs, baselines, and distal-section snapshot."""

    h: Any
    pairs: list[EiPair]
    baseline_coords: list[SynapseCoords]
    baseline_gaba_mod: float
    distal_sections: list[Any]
    baseline_L: dict[int, float]


@dataclass(frozen=True, slots=True)
class TrialOutcome:
    """Per-trial outcome: firing rate, spike count, and peak voltage."""

    spike_count: int
    peak_mv: float
    firing_rate_hz: float


def build_cell_context() -> CellContext:
    """Preload nrnmech.dll, build the DSGC cell, E-I pairs, and distal snapshot."""
    _preload_nrnmech_dll()
    h = build_dsgc()
    _source_channel_partition_hoc(h=h)
    pairs: list[EiPair] = build_ei_pairs(h=h)
    baseline_coords: list[SynapseCoords] = read_synapse_coords(h=h)
    baseline_gaba_mod: float = float(h.gabaMOD)
    distal_sections: list[Any] = identify_distal_sections(h=h)
    baseline_L: dict[int, float] = snapshot_distal_lengths(
        h=h,
        distal_sections=distal_sections,
    )
    return CellContext(
        h=h,
        pairs=pairs,
        baseline_coords=baseline_coords,
        baseline_gaba_mod=baseline_gaba_mod,
        distal_sections=distal_sections,
        baseline_L=baseline_L,
    )


def run_one_trial_length(
    *,
    ctx: CellContext,
    angle_deg: float,
    trial_seed: int,
    multiplier: float,
) -> TrialOutcome:
    """Run one per-dendrite E-I trial at ``angle_deg`` with the distal-length override applied.

    Steps match ``run_one_trial_dendritic`` (t0022) and ``run_one_trial_vrest`` (t0026) with
    ``set_distal_length_multiplier`` inserted after baseline-drift assertions and before
    ``h.finitialize``. ``apply_params`` is kept inside the trial loop so Random123 streams are
    re-seeded every trial (see research_code.md lesson about hoisting ``apply_params``).
    """
    h: Any = ctx.h

    apply_params(h, seed=trial_seed)
    _silence_baseline_hoc_synapses(h=h)
    _assert_bip_and_gabamod_baseline(
        h=h,
        baseline_coords=ctx.baseline_coords,
        baseline_gaba_mod=ctx.baseline_gaba_mod,
    )

    # Distal length override — must run AFTER apply_params (which is length-agnostic but
    # resets v_init and Random123) and BEFORE h.finitialize.
    set_distal_length_multiplier(
        h=h,
        distal_sections=ctx.distal_sections,
        baseline_L=ctx.baseline_L,
        multiplier=multiplier,
    )
    assert_distal_lengths(
        h=h,
        distal_sections=ctx.distal_sections,
        baseline_L=ctx.baseline_L,
        multiplier=multiplier,
    )

    schedule_ei_onsets(
        h=h,
        pairs=ctx.pairs,
        angle_deg=angle_deg,
        velocity_um_per_ms=BAR_VELOCITY_UM_PER_MS,
        gaba_null_pref_ratio=GABA_CONDUCTANCE_NULL_NS / GABA_CONDUCTANCE_PREFERRED_NS,
        trial_seed=trial_seed,
    )

    v_rec: Any = h.Vector()
    v_rec.record(h.RGC.soma(0.5)._ref_v)

    h.finitialize(V_INIT_MV)
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
