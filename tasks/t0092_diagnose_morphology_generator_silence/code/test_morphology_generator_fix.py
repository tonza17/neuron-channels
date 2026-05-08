"""Unit tests for ``morphology_generator_fix.generate_fixed_morphology`` (REQ-7)."""

from __future__ import annotations

import math

import numpy as np

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    CELSIUS_DEG_C,
    DT_MS,
    STEPS_PER_MS,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import (
    insert_baseline_channels,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.constants import (
    BEDB_AREA_TARGET_UM2,
    MORPH_SEED,
    NO_STIM_DURATION_MS,
    SOMA_AREA_TOLERANCE_FRAC,
    V_INIT_MV,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (
    generate_fixed_morphology,
)


def _section_area_um2(*, sec: object) -> float:
    total: float = 0.0
    for seg in sec:  # type: ignore[attr-defined]
        total += float(seg.area())
    return float(total)


def _section_signature(*, sec: object) -> tuple[float, float, int]:
    return (float(sec.L), float(sec.diam), int(sec.nseg))  # type: ignore[attr-defined]


def test_soma_area_within_tolerance() -> None:
    """The patched cell's soma surface area is within +/- 5% of 220 um^2."""
    params = MorphologyParams.from_bedb_base_point()
    cell = generate_fixed_morphology(params=params, morph_seed=MORPH_SEED)
    area = _section_area_um2(sec=cell.soma)
    tol = SOMA_AREA_TOLERANCE_FRAC * BEDB_AREA_TARGET_UM2
    assert abs(area - BEDB_AREA_TARGET_UM2) < tol, (
        f"soma area {area:.3f} um^2 is outside +/- {tol:.3f} of {BEDB_AREA_TARGET_UM2:.3f}"
    )


def test_determinism() -> None:
    """Same params + same morph_seed produce structurally identical sections."""
    params = MorphologyParams.from_bedb_base_point()
    a = generate_fixed_morphology(params=params, morph_seed=MORPH_SEED)
    b = generate_fixed_morphology(params=params, morph_seed=MORPH_SEED)
    # Soma signature
    assert _section_signature(sec=a.soma) == _section_signature(sec=b.soma)
    # Section count
    assert len(a.all_dends) == len(b.all_dends)
    assert len(a.primary_dends) == len(b.primary_dends)
    assert len(a.terminal_dends) == len(b.terminal_dends)
    assert len(a.non_terminal_dends) == len(b.non_terminal_dends)
    # Per-section dimension match
    for sec_a, sec_b in zip(a.all_dends, b.all_dends, strict=True):
        assert _section_signature(sec=sec_a) == _section_signature(sec=sec_b)


def test_no_nan_on_bedb_base_point() -> None:
    """Patched soma Vm under 50 ms unstimulated init has no NaN samples.

    Skips ``apply_parameter_vector`` (would re-trigger _INSERTED_CELLS caching
    across pytest runs); instead inserts the baseline HHst + cad channels and
    runs a passive 50 ms hold at V_init = -70 mV. The unpatched generator's
    soma fails this with NaN voltage because surface area ~0 makes the
    integration unstable; the patched soma stays at V_init throughout.
    """
    params = MorphologyParams.from_bedb_base_point()
    cell = generate_fixed_morphology(params=params, morph_seed=MORPH_SEED)
    h = cell.h
    insert_baseline_channels(h=h, cell=cell)

    h.celsius = float(CELSIUS_DEG_C)
    h.dt = float(DT_MS)
    h.steps_per_ms = float(STEPS_PER_MS)
    h.v_init = float(V_INIT_MV)
    h.tstop = float(NO_STIM_DURATION_MS)

    v_vec = h.Vector()
    v_vec.record(cell.soma(0.5)._ref_v)  # type: ignore[attr-defined]
    h.finitialize(float(V_INIT_MV))
    h.run()

    arr = np.asarray(v_vec.to_python(), dtype=np.float64)
    assert arr.shape[0] > 0, "expected a non-empty Vm trace"
    assert np.all(np.isfinite(arr)), "patched soma must not produce NaN voltage"
    # Resting Vm should stay reasonably close to V_init since there's no input.
    assert abs(float(arr.mean()) - float(V_INIT_MV)) < 5.0, (
        f"resting Vm drift too large: mean={arr.mean():.3f} mV vs V_init={V_INIT_MV:.3f}"
    )


def test_soma_pt3d_z_axis() -> None:
    """The patched soma has exactly 2 pt3d points along the z-axis."""
    params = MorphologyParams.from_bedb_base_point()
    cell = generate_fixed_morphology(params=params, morph_seed=MORPH_SEED)
    h = cell.h
    cell.soma.push()
    try:
        n = int(h.n3d())
        assert n == 2, f"expected 2 pt3d points after fix, got {n}"
        assert math.isclose(float(h.x3d(0)), 0.0, abs_tol=1e-6)
        assert math.isclose(float(h.y3d(0)), 0.0, abs_tol=1e-6)
        assert math.isclose(float(h.z3d(0)), 0.0, abs_tol=1e-6)
        assert math.isclose(float(h.x3d(1)), 0.0, abs_tol=1e-6)
        assert math.isclose(float(h.y3d(1)), 0.0, abs_tol=1e-6)
        # Second pt3d point sits at z = soma_diameter_um.
        assert math.isclose(
            float(h.z3d(1)),
            float(params.soma_diameter_um),
            rel_tol=1e-6,
        )
    finally:
        h.pop_section()
