"""Thin adapter around the t0092 patched morphology generator (REQ-1).

Imports `generate_fixed_morphology` (canonical per `C-0093-01`) and
`insert_baseline_channels` from t0092 library, plus the t0093 `_LIVE_CELLS`
GC-defense list (REQ-18) to retain references to all built cells across
worker processes.

This module is the ONLY entry point for cell construction in t0091; t0090's
unpatched `generate_morphology` MUST NOT be called directly anywhere in the
build path (REQ-1).
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

# Library imports (allowed cross-task per C-0093-01).
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
    MorphologyResult,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import (
    insert_baseline_channels,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (
    generate_fixed_morphology,
)
from tasks.t0114_seed7755_no_autostop.code.constants_morphology import (
    INT_PARAM_INDICES_68,
    N_PARAMS_54,
)

# REQ-18: module-level live-cell list to defend against cell-id reuse after
# garbage collection (per t0093 mitigation pattern).
_LIVE_CELLS: list[MorphologyResult] = []

# Hash cache used by the worker to detect morphology vector change.
_WORKER_MORPH_HASH: int | None = None
_WORKER_CELL: MorphologyResult | None = None


def hash_morphology_vector(*, vector: NDArray[np.float64]) -> int:
    """Deterministic hash for caching the worker cell across electrophys-only changes."""
    return hash(np.asarray(vector, dtype=np.float64).tobytes())


def split_68d_vector(
    *, vector_68d: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Split the 68-d joint vector into (54-d electrophys, 14-d morphology)."""
    assert vector_68d.shape == (68,), f"expected 68-d vector, got {vector_68d.shape}"
    return vector_68d[:N_PARAMS_54], vector_68d[N_PARAMS_54:]


def morphology_params_from_vector(*, morph_vector_14d: NDArray[np.float64]) -> MorphologyParams:
    """Construct a MorphologyParams from the 14-d float vector with int rounding."""
    assert morph_vector_14d.shape == (14,)
    # Field order matches t0090.morphology_params.MorphologyParams fields.
    return MorphologyParams(
        num_primary_branches=int(round(float(morph_vector_14d[0]))),
        branch_prob_per_um=float(morph_vector_14d[1]),
        max_strahler_depth=int(round(float(morph_vector_14d[2]))),
        mean_branching_angle_deg=float(morph_vector_14d[3]),
        rall_exponent=float(morph_vector_14d[4]),
        soma_offset_pd_um=float(morph_vector_14d[5]),
        field_elongation_pd=float(morph_vector_14d[6]),
        branch_density_gradient_pd=float(morph_vector_14d[7]),
        primary_branch_pd_concentration=float(morph_vector_14d[8]),
        mean_segment_length_um=float(morph_vector_14d[9]),
        soma_diameter_um=float(morph_vector_14d[10]),
        ais_length_um=float(morph_vector_14d[11]),
        morph_seed=int(round(float(morph_vector_14d[12]))),
        branch_length_cv=float(morph_vector_14d[13]),
    )


def build_cell(*, h: Any, morph_params: MorphologyParams) -> MorphologyResult:
    """Build a fresh procedurally-generated DSGC cell + baseline channels.

    Calls t0092's `generate_fixed_morphology` (canonical entry per C-0093-01),
    inserts HHst + cad baseline channels, and adds the result to `_LIVE_CELLS`
    to defend against GC-driven cell-id reuse.

    REQ-1: this is the ONLY path to cell construction in t0091 — the unpatched
    t0090 `generate_morphology` MUST NOT be imported or called.
    """
    cell = generate_fixed_morphology(params=morph_params, morph_seed=morph_params.morph_seed)
    insert_baseline_channels(h=h, cell=cell)
    _LIVE_CELLS.append(cell)
    return cell


__all__ = [
    "MorphologyParams",
    "MorphologyResult",
    "INT_PARAM_INDICES_68",
    "_LIVE_CELLS",
    "build_cell",
    "hash_morphology_vector",
    "morphology_params_from_vector",
    "split_68d_vector",
]
