"""t0022-compatible per-dendrite E-I trial runner with a runtime null-GABA conductance override.

Structural clone of ``tasks/t0036_rerun_t0030_halved_null_gaba/code/trial_runner_diameter.py``
with three substantive edits:

1. **No import-time GABA patch.** t0036 imported ``gaba_override`` at line 1 as a module-load
   side-effect that patched ``GABA_CONDUCTANCE_NULL_NS`` to a single hard-coded value. t0037's
   ``gaba_override`` instead exposes a callable ``set_null_gaba_ns(value_ns=...)`` that is invoked
   once per trial. This allows a multi-level ladder sweep inside one process.
2. **Lazy re-read of ``GABA_CONDUCTANCE_NULL_NS`` inside every trial.** The value is read from
   the t0022 module AFTER ``set_null_gaba_ns`` fires, so the ``schedule_ei_onsets`` assertion at
   ``run_tuning_curve.py:327`` sees a consistent binding every trial.
3. **No diameter override.** ``set_distal_diameter_multiplier`` is never called; distal diameter
   stays at 1.0x baseline. A post-simulation ``assert_distal_diameters(..., multiplier=1.0)`` is
   kept as an integrity guard against silent drift.
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
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.constants import (
    BASELINE_DIAMETER_MULTIPLIER,
    MIDPOINT_ASSERT_TOL_UM,
)
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.diameter_override import (
    assert_distal_diameters,
    identify_distal_sections,
    snapshot_distal_diameters,
)
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.gaba_override import (
    set_null_gaba_ns,
)


@dataclass(frozen=True, slots=True)
class PairMidpoint:
    """Snapshot of an E-I pair's 3D midpoint coordinates (x_mid_um, y_mid_um) at build time."""

    x_mid_um: float
    y_mid_um: float


@dataclass(slots=True)
class CellContext:
    """Holds the NEURON handle, E-I pairs, baselines, and distal-section snapshot."""

    h: Any
    pairs: list[EiPair]
    baseline_coords: list[SynapseCoords]
    baseline_gaba_mod: float
    distal_sections: list[Any]
    baseline_diam: dict[tuple[int, float], float]
    pair_midpoints: list[PairMidpoint]


@dataclass(frozen=True, slots=True)
class TrialOutcome:
    """Per-trial outcome: firing rate, spike count, and peak voltage."""

    spike_count: int
    peak_mv: float
    firing_rate_hz: float


def build_cell_context() -> CellContext:
    """Preload nrnmech.dll, build the DSGC cell, E-I pairs, and distal-diameter snapshot."""
    _preload_nrnmech_dll()
    h = build_dsgc()
    _source_channel_partition_hoc(h=h)
    pairs: list[EiPair] = build_ei_pairs(h=h)
    baseline_coords: list[SynapseCoords] = read_synapse_coords(h=h)
    baseline_gaba_mod: float = float(h.gabaMOD)
    distal_sections: list[Any] = identify_distal_sections(h=h)
    baseline_diam: dict[tuple[int, float], float] = snapshot_distal_diameters(
        h=h,
        distal_sections=distal_sections,
    )
    pair_midpoints: list[PairMidpoint] = [
        PairMidpoint(x_mid_um=float(p.x_mid_um), y_mid_um=float(p.y_mid_um)) for p in pairs
    ]
    return CellContext(
        h=h,
        pairs=pairs,
        baseline_coords=baseline_coords,
        baseline_gaba_mod=baseline_gaba_mod,
        distal_sections=distal_sections,
        baseline_diam=baseline_diam,
        pair_midpoints=pair_midpoints,
    )


def _assert_pair_midpoints_unchanged(*, ctx: CellContext) -> None:
    """Verify that no E-I pair's 3D midpoint drifted since ``build_cell_context`` was called.

    NEURON does not mutate 3D points when ``seg.diam`` is assigned, but this guard makes that
    invariant explicit at every trial and will fire loudly if it is ever violated.
    """
    bad: list[tuple[int, float, float, float, float]] = []
    for idx, (pair, snap) in enumerate(
        zip(ctx.pairs, ctx.pair_midpoints, strict=True),
    ):
        dx: float = abs(float(pair.x_mid_um) - snap.x_mid_um)
        dy: float = abs(float(pair.y_mid_um) - snap.y_mid_um)
        if dx > MIDPOINT_ASSERT_TOL_UM or dy > MIDPOINT_ASSERT_TOL_UM:
            bad.append(
                (idx, snap.x_mid_um, snap.y_mid_um, float(pair.x_mid_um), float(pair.y_mid_um)),
            )
    if len(bad) > 0:
        preview: list[tuple[int, float, float, float, float]] = bad[:3]
        raise AssertionError(
            f"E-I pair midpoint drift detected: {preview!r} (and {len(bad) - 3} more)",
        )


def run_single_trial_gaba(
    *,
    ctx: CellContext,
    angle_deg: float,
    trial_seed: int,
    gaba_null_ns: float,
) -> TrialOutcome:
    """Run one per-dendrite E-I trial at ``angle_deg`` with the null-GABA override applied.

    Override sequence (see plan/plan.md Milestone A step 4):

    1. ``set_null_gaba_ns(value_ns=gaba_null_ns)`` -- runtime patch of
       ``t0022.constants.GABA_CONDUCTANCE_NULL_NS`` and its caller-local copy in
       ``run_tuning_curve``. Runs FIRST so the ``schedule_ei_onsets`` assertion sees the
       refreshed value.
    2. ``apply_params(h, seed=trial_seed)`` -- re-seeds Random123, resets v_init.
    3. ``_silence_baseline_hoc_synapses`` -- zeros out bundled HOC synapses (mandatory).
    4. ``_assert_bip_and_gabamod_baseline`` -- guards against mutations upstream.
    5. Midpoint-snapshot assertion -- confirms 3D coordinates unchanged.
    6. ``schedule_ei_onsets`` -- bar-arrival-time-driven onsets per pair; the
       ``gaba_null_pref_ratio`` passed in is ``gaba_null_ns / GABA_CONDUCTANCE_PREFERRED_NS``.
    7. ``h.finitialize(V_INIT_MV)`` + ``h.continuerun(TSTOP_MS)``.
    8. Post-simulation ``assert_distal_diameters(..., multiplier=1.0)`` -- distal seg.diam must
       not have drifted (diameter never mutated in this task).
    """
    # STEP 1: runtime GABA patch BEFORE reading the module-level value.
    set_null_gaba_ns(value_ns=gaba_null_ns)

    # Lazy re-read of the patched value from the t0022 module.
    from tasks.t0022_modify_dsgc_channel_testbed.code.constants import (
        GABA_CONDUCTANCE_NULL_NS as _effective_gaba_null_ns,
    )

    h: Any = ctx.h

    apply_params(h, seed=trial_seed)
    _silence_baseline_hoc_synapses(h=h)
    _assert_bip_and_gabamod_baseline(
        h=h,
        baseline_coords=ctx.baseline_coords,
        baseline_gaba_mod=ctx.baseline_gaba_mod,
    )
    _assert_pair_midpoints_unchanged(ctx=ctx)

    gaba_null_pref_ratio: float = float(_effective_gaba_null_ns) / float(
        GABA_CONDUCTANCE_PREFERRED_NS,
    )
    schedule_ei_onsets(
        h=h,
        pairs=ctx.pairs,
        angle_deg=angle_deg,
        velocity_um_per_ms=BAR_VELOCITY_UM_PER_MS,
        gaba_null_pref_ratio=gaba_null_pref_ratio,
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

    # Post-simulation distal-diameter integrity check. Diameter is never mutated in this task,
    # so the multiplier is always 1.0x baseline; this guards against silent drift inside
    # NEURON between trials.
    assert_distal_diameters(
        h=h,
        distal_sections=ctx.distal_sections,
        baseline_diam=ctx.baseline_diam,
        multiplier=BASELINE_DIAMETER_MULTIPLIER,
    )

    return TrialOutcome(
        spike_count=spike_count,
        peak_mv=peak_mv,
        firing_rate_hz=firing_rate_hz,
    )
