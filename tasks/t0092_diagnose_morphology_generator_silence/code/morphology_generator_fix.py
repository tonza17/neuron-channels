"""Drop-in fix for t0090's procedural DSGC morphology generator.

Public entry point: ``generate_fixed_morphology(*, params, morph_seed)`` —
same signature as ``generate_morphology`` from
``tasks.t0090_morphology_generator_diversity_test.code.generator``.

Implementation
--------------

The function is a thin wrapper. It calls the unmodified
``generate_morphology`` from t0090, then patches the soma section to fix the
"degenerate-zero-area" bug confirmed by Phase D of t0092:

* t0090's ``_materialise_neuron_sections`` emits two ``pt3dadd`` points at
  ``(start_xy[0], start_xy[1], 0.0, soma_diameter)`` and ``(end_xy[0],
  end_xy[1], 0.0, soma_diameter)``. For the BedB-equivalent base point both
  ``start_xy`` and ``end_xy`` are ``(0, 0)``, so the two pt3d points coincide
  and NEURON computes the cumulative pt3d distance as ~0 — overriding
  ``sec.L = soma_diameter_um`` to ~1e-9 um. The soma's surface area collapses
  to ~9.4e-14 um^2 and synaptic input drives the somatic Vm to NaN within a
  few ms.

The fix calls ``h.pt3dclear()`` on the soma, then re-emits two pt3d points
along the **z-axis** — ``(0, 0, 0, d_target)`` and ``(0, 0, soma_diameter_um,
d_target)``. The cumulative pt3d distance is now ``soma_diameter_um`` so
``sec.L = soma_diameter_um``. The diameter ``d_target`` is chosen so the
resulting cylinder surface area matches the t0024 hand-coded reference
(~220 um^2): ``d_target = BEDB_AREA_TARGET_UM2 / (pi * soma_diameter_um)``.

This patches the soma in place inside the returned ``MorphologyResult``. All
other fields (dendrite sections, AIS sections, terminal_locs_xy,
section_endpoints_xy, morphometric_summary) are preserved as-is. The
``_LIVE_CELLS`` defense from t0090's verification harness is the caller's
responsibility — same as the underlying ``generate_morphology``.

Determinism
-----------

Same ``(params, morph_seed)`` -> structurally identical output across two
calls. The fix is purely a post-hoc soma patch and does not introduce any new
randomness.
"""

from __future__ import annotations

import math
from typing import Any

from tasks.t0090_morphology_generator_diversity_test.code.generator import (
    generate_morphology,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
    MorphologyResult,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.constants import (
    BEDB_AREA_TARGET_UM2,
)


def _patch_soma_geometry(*, h: Any, soma: Any, soma_diameter_um: float) -> None:
    """Re-emit the soma's pt3d as a z-axis cylinder of the target surface area.

    The cylinder length is ``soma_diameter_um`` (the t0090-intended value) and
    the diameter is chosen so ``pi * d * L = BEDB_AREA_TARGET_UM2``.
    """
    assert soma_diameter_um > 0, "soma_diameter_um must be positive"
    d_target = float(BEDB_AREA_TARGET_UM2) / (math.pi * float(soma_diameter_um))
    soma.push()
    try:
        h.pt3dclear()
        h.pt3dadd(0.0, 0.0, 0.0, float(d_target))
        h.pt3dadd(0.0, 0.0, float(soma_diameter_um), float(d_target))
    finally:
        h.pop_section()


def generate_fixed_morphology(
    *,
    params: MorphologyParams,
    morph_seed: int | None = None,
) -> MorphologyResult:
    """Build a procedural DSGC cell with the t0090 soma-area bug patched.

    Drop-in replacement for
    ``tasks.t0090_morphology_generator_diversity_test.code.generator.generate_morphology``.
    Returns the same ``MorphologyResult`` shape; the only difference is that
    the soma section's pt3d points define a cylinder with ~220 um^2 surface
    area (matching the t0024 hand-coded reference) instead of the degenerate
    ~0 um^2 cylinder produced by the unpatched generator.
    """
    result = generate_morphology(params=params, morph_seed=morph_seed)
    _patch_soma_geometry(
        h=result.h,
        soma=result.soma,
        soma_diameter_um=float(params.soma_diameter_um),
    )
    return result
