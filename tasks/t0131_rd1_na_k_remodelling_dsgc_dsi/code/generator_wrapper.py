"""Thin adapter around the t0092 patched morphology generator (copied from t0129)."""

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

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
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    N_MORPH_PARAMS,
    N_PARAMS_54,
    N_PARAMS_68,
)

LIVE_CELLS: list[MorphologyResult] = []


@dataclass(frozen=True, slots=True)
class SplitVector:
    electrophys_54d: NDArray[np.float64]
    morphology_14d: NDArray[np.float64]


def hash_morphology_vector(*, vector: NDArray[np.float64]) -> int:
    return hash(np.asarray(vector, dtype=np.float64).tobytes())


def split_68d_vector(*, vector_68d: NDArray[np.float64]) -> SplitVector:
    assert vector_68d.shape == (N_PARAMS_68,), f"expected 68-d vector, got {vector_68d.shape}"
    return SplitVector(
        electrophys_54d=vector_68d[:N_PARAMS_54],
        morphology_14d=vector_68d[N_PARAMS_54:],
    )


def morphology_params_from_vector(*, morph_vector_14d: NDArray[np.float64]) -> MorphologyParams:
    assert morph_vector_14d.shape == (N_MORPH_PARAMS,), "morphology vector is 14-d"
    v = morph_vector_14d
    return MorphologyParams(
        num_primary_branches=int(round(float(v[0]))),
        branch_prob_per_um=float(v[1]),
        max_strahler_depth=int(round(float(v[2]))),
        mean_branching_angle_deg=float(v[3]),
        rall_exponent=float(v[4]),
        soma_offset_pd_um=float(v[5]),
        field_elongation_pd=float(v[6]),
        branch_density_gradient_pd=float(v[7]),
        primary_branch_pd_concentration=float(v[8]),
        mean_segment_length_um=float(v[9]),
        soma_diameter_um=float(v[10]),
        ais_length_um=float(v[11]),
        morph_seed=int(round(float(v[12]))),
        branch_length_cv=float(v[13]),
    )


def build_cell(*, h: Any, morph_params: MorphologyParams) -> MorphologyResult:
    cell = generate_fixed_morphology(params=morph_params, morph_seed=morph_params.morph_seed)
    insert_baseline_channels(h=h, cell=cell)
    LIVE_CELLS.append(cell)
    return cell
