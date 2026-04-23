"""t0022-compatible per-dendrite E-I trial runner with a distal-diameter override hook.

Structural clone of
``tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/trial_runner_diameter.py``. Two
substantive edits over the t0030 original:

1. Line 1 imports ``gaba_override`` so the monkey-patch of
   ``tasks.t0022_modify_dsgc_channel_testbed.code.constants.GABA_CONDUCTANCE_NULL_NS`` runs
   BEFORE the ``run_tuning_curve`` import below. The t0022 driver module snapshots
   ``GABA_CONDUCTANCE_NULL_NS`` at its own import time (line 77 of
   ``run_tuning_curve.py``); unpatched it would see 12.0 nS and the assertion at
   ``run_tuning_curve.py:327`` would fire on every trial because ``gaba_null_pref_ratio`` is
   2.0 here, so ``null_weight_us = 6e-3`` but the snapshot ``GABA_CONDUCTANCE_NULL_NS * 1e-3``
   would be 12e-3. Post-patch, both evaluate to 6e-3 and the assertion passes.
2. This module's local ``GABA_CONDUCTANCE_NULL_NS`` binding is also rebound to 6.0 so the
   ``gaba_null_pref_ratio`` expression below evaluates to ``6.0 / 3.0 = 2.0`` (not 4.0).

Other behaviour matches t0030 verbatim:

* ``run_one_trial_diameter`` accepts ``distal_sections``, ``baseline_diam``, and ``multiplier``
  parameters. It calls ``set_distal_diameter_multiplier`` after ``apply_params`` /
  ``_silence_baseline_hoc_synapses`` / ``_assert_bip_and_gabamod_baseline`` / midpoint-snapshot
  check and before ``h.finitialize``. An ``assert_distal_diameters`` call immediately follows
  the override as a per-trial guard against silent rescale failures.
* The NEURON bootstrap import runs at module scope before any ``neuron`` imports are attempted.
* The cell context is built once via ``build_cell_context`` and reused across every (diameter,
  angle, trial) combination to amortise the ~1.6 s NEURON build cost.
* Per-trial midpoint-snapshot assertion confirms the diameter override does not perturb 3D
  coordinates (``pair.x_mid_um`` / ``y_mid_um``), within 1e-9 um tolerance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import tasks.t0036_rerun_t0030_halved_null_gaba.code.gaba_override  # noqa: F401  # MUST run first
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
from tasks.t0036_rerun_t0030_halved_null_gaba.code.constants import (
    GABA_CONDUCTANCE_NULL_NS_OVERRIDE as GABA_CONDUCTANCE_NULL_NS,
)
from tasks.t0036_rerun_t0030_halved_null_gaba.code.constants import (
    MIDPOINT_ASSERT_TOL_UM,
)
from tasks.t0036_rerun_t0030_halved_null_gaba.code.diameter_override import (
    assert_distal_diameters,
    identify_distal_sections,
    set_distal_diameter_multiplier,
    snapshot_distal_diameters,
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


def run_one_trial_diameter(
    *,
    ctx: CellContext,
    angle_deg: float,
    trial_seed: int,
    multiplier: float,
) -> TrialOutcome:
    """Run one per-dendrite E-I trial at ``angle_deg`` with the distal-diameter override applied.

    Override sequence (see plan/plan.md Milestone A step 4):

    1. ``apply_params(h, seed=trial_seed)`` -- re-seeds Random123, resets v_init.
    2. ``_silence_baseline_hoc_synapses`` -- zeros out bundled HOC synapses (mandatory).
    3. ``_assert_bip_and_gabamod_baseline`` -- guards against mutations upstream.
    4. Midpoint-snapshot assertion -- confirms 3D coordinates unchanged.
    5. ``set_distal_diameter_multiplier`` -- the sweep-specific override.
    6. ``assert_distal_diameters`` -- per-trial rescale verification.
    7. ``schedule_ei_onsets`` -- bar-arrival-time-driven onsets per pair; the
       ``gaba_null_pref_ratio`` passed in evaluates to 2.0 (6.0 / 3.0), matching the patched
       ``GABA_CONDUCTANCE_NULL_NS = 6.0`` inside ``run_tuning_curve.py``.
    8. ``h.finitialize(V_INIT_MV)`` + ``h.continuerun(TSTOP_MS)``.
    """
    h: Any = ctx.h

    apply_params(h, seed=trial_seed)
    _silence_baseline_hoc_synapses(h=h)
    _assert_bip_and_gabamod_baseline(
        h=h,
        baseline_coords=ctx.baseline_coords,
        baseline_gaba_mod=ctx.baseline_gaba_mod,
    )
    _assert_pair_midpoints_unchanged(ctx=ctx)

    # Distal diameter override -- must run AFTER apply_params (which resets v_init and
    # Random123) and BEFORE h.finitialize.
    set_distal_diameter_multiplier(
        h=h,
        distal_sections=ctx.distal_sections,
        baseline_diam=ctx.baseline_diam,
        multiplier=multiplier,
    )
    assert_distal_diameters(
        h=h,
        distal_sections=ctx.distal_sections,
        baseline_diam=ctx.baseline_diam,
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
