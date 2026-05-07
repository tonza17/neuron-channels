"""Frozen dataclasses for the procedural DSGC morphology generator API.

The 14 typed parameter fields match the task description's parameter table. A
deterministic ``(MorphologyParams, morph_seed)`` pair always produces the same
``MorphologyResult``. The result mirrors the t0080 ``DSGCCellWithAIS`` field
layout (``soma``, ``all_dends``, ``primary_dends``, ``non_terminal_dends``,
``terminal_dends``, ``terminal_locs_xy``, ``origin_xy``, ``ais_proximal``,
``ais_distal``) so that ``apply_parameter_vector`` consumes it without
modification.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    BEDB_BASE_POINT,
    INT_PARAM_NAMES,
    PARAM_AIS_LENGTH_UM,
    PARAM_BRANCH_DENSITY_GRADIENT_PD,
    PARAM_BRANCH_LENGTH_CV,
    PARAM_BRANCH_PROB_PER_UM,
    PARAM_FIELD_ELONGATION_PD,
    PARAM_MAX_STRAHLER_DEPTH,
    PARAM_MEAN_BRANCHING_ANGLE_DEG,
    PARAM_MEAN_SEGMENT_LENGTH_UM,
    PARAM_MORPH_SEED,
    PARAM_NAMES,
    PARAM_NUM_PRIMARY_BRANCHES,
    PARAM_PRIMARY_BRANCH_PD_CONCENTRATION,
    PARAM_RALL_EXPONENT,
    PARAM_SOMA_DIAMETER_UM,
    PARAM_SOMA_OFFSET_PD_UM,
    StabilityKind,
)


@dataclass(frozen=True, slots=True)
class MorphologyParams:
    """The 14 morphology knobs (3 ints + 11 floats)."""

    num_primary_branches: int
    branch_prob_per_um: float
    max_strahler_depth: int
    mean_branching_angle_deg: float
    rall_exponent: float
    soma_offset_pd_um: float
    field_elongation_pd: float
    branch_density_gradient_pd: float
    primary_branch_pd_concentration: float
    mean_segment_length_um: float
    soma_diameter_um: float
    ais_length_um: float
    morph_seed: int
    branch_length_cv: float

    def to_dict(self) -> dict[str, float | int]:
        return {
            PARAM_NUM_PRIMARY_BRANCHES: int(self.num_primary_branches),
            PARAM_BRANCH_PROB_PER_UM: float(self.branch_prob_per_um),
            PARAM_MAX_STRAHLER_DEPTH: int(self.max_strahler_depth),
            PARAM_MEAN_BRANCHING_ANGLE_DEG: float(self.mean_branching_angle_deg),
            PARAM_RALL_EXPONENT: float(self.rall_exponent),
            PARAM_SOMA_OFFSET_PD_UM: float(self.soma_offset_pd_um),
            PARAM_FIELD_ELONGATION_PD: float(self.field_elongation_pd),
            PARAM_BRANCH_DENSITY_GRADIENT_PD: float(self.branch_density_gradient_pd),
            PARAM_PRIMARY_BRANCH_PD_CONCENTRATION: float(self.primary_branch_pd_concentration),
            PARAM_MEAN_SEGMENT_LENGTH_UM: float(self.mean_segment_length_um),
            PARAM_SOMA_DIAMETER_UM: float(self.soma_diameter_um),
            PARAM_AIS_LENGTH_UM: float(self.ais_length_um),
            PARAM_MORPH_SEED: int(self.morph_seed),
            PARAM_BRANCH_LENGTH_CV: float(self.branch_length_cv),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MorphologyParams:
        missing: list[str] = [name for name in PARAM_NAMES if name not in data]
        assert len(missing) == 0, f"missing parameter fields: {missing}"
        return cls(
            num_primary_branches=int(data[PARAM_NUM_PRIMARY_BRANCHES]),
            branch_prob_per_um=float(data[PARAM_BRANCH_PROB_PER_UM]),
            max_strahler_depth=int(data[PARAM_MAX_STRAHLER_DEPTH]),
            mean_branching_angle_deg=float(data[PARAM_MEAN_BRANCHING_ANGLE_DEG]),
            rall_exponent=float(data[PARAM_RALL_EXPONENT]),
            soma_offset_pd_um=float(data[PARAM_SOMA_OFFSET_PD_UM]),
            field_elongation_pd=float(data[PARAM_FIELD_ELONGATION_PD]),
            branch_density_gradient_pd=float(data[PARAM_BRANCH_DENSITY_GRADIENT_PD]),
            primary_branch_pd_concentration=float(data[PARAM_PRIMARY_BRANCH_PD_CONCENTRATION]),
            mean_segment_length_um=float(data[PARAM_MEAN_SEGMENT_LENGTH_UM]),
            soma_diameter_um=float(data[PARAM_SOMA_DIAMETER_UM]),
            ais_length_um=float(data[PARAM_AIS_LENGTH_UM]),
            morph_seed=int(data[PARAM_MORPH_SEED]),
            branch_length_cv=float(data[PARAM_BRANCH_LENGTH_CV]),
        )

    @classmethod
    def from_bedb_base_point(cls) -> MorphologyParams:
        return cls.from_dict(data=dict(BEDB_BASE_POINT))


assert set(INT_PARAM_NAMES) == {
    PARAM_NUM_PRIMARY_BRANCHES,
    PARAM_MAX_STRAHLER_DEPTH,
    PARAM_MORPH_SEED,
}


@dataclass(frozen=True, slots=True)
class MorphometricSummary:
    """Six morphometric summary features used by Phase E PCA/UMAP."""

    total_dendritic_length_um: float
    branch_count: int
    max_strahler_depth: int
    electrotonic_length_lambda: float
    soma_displacement_um: float
    field_major_axis_length_um: float

    def to_dict(self) -> dict[str, float | int]:
        return {
            "total_dendritic_length_um": float(self.total_dendritic_length_um),
            "branch_count": int(self.branch_count),
            "max_strahler_depth": int(self.max_strahler_depth),
            "electrotonic_length_lambda": float(self.electrotonic_length_lambda),
            "soma_displacement_um": float(self.soma_displacement_um),
            "field_major_axis_length_um": float(self.field_major_axis_length_um),
        }


@dataclass(frozen=True, slots=True)
class MorphologyResult:
    """A built procedural cell that duck-types as t0080 ``DSGCCellWithAIS``.

    Fields mirror ``DSGCCellWithAIS`` so that ``apply_parameter_vector`` writes
    the 54-d parameter vector to ``soma + all_dends + ais_*`` without
    modification. Additional fields (``stability_flag``, ``morphometric_summary``,
    ``connectivity``) are read by t0090 verification only.
    """

    h: Any
    rgc: Any
    soma: Any
    all_dends: list[Any]
    primary_dends: list[Any]
    non_terminal_dends: list[Any]
    terminal_dends: list[Any]
    terminal_locs_xy: Any
    origin_xy: tuple[float, float]
    ais_proximal: Any
    ais_distal: Any
    stability_flag: StabilityKind
    morphometric_summary: MorphometricSummary
    connectivity: dict[str, str]
    section_endpoints_xy: dict[str, tuple[float, float, float, float]]
