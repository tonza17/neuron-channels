"""Constants and enums for the t0120 morphology generator geometry audit."""

from __future__ import annotations

from enum import StrEnum

# Re-export the 14 morphology parameter names from t0117 so they stay in sync.
from tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.constants import (
    MORPHOLOGY_PARAM_NAMES,
)

__all__ = [
    "ASYMMETRY_PARAM_NAMES",
    "BEDB_SYMMETRIC_CONTROL_REFS",
    "CELL_ID_COL",
    "CHECK1_PRIMARY_START_COL",
    "CHECK2_PARENT_CHILD_COL",
    "CHECK3_SYNAPSE_FRAME_COL",
    "CHECK_ABS_TOL",
    "CHECK_REL_TOL",
    "DSI_COL",
    "GENERATION_COL",
    "INDIVIDUAL_IDX_COL",
    "MORPHOLOGY_PARAM_NAMES",
    "MORPH_SEED_COL",
    "PD_RATE_COL",
    "SEED_COL",
    "SOURCE_TASK_COL",
    "STRATUM_TAG_COL",
    "SYMMETRIC_FRACTIONAL_TOL",
    "StratumTag",
    "TARGET_MIN_CELLS",
    "TARGET_MAX_CELLS",
]

# ---------------------------------------------------------------------------
# Column names in the t0117 pooled parquet (also used in this task's outputs).
# ---------------------------------------------------------------------------

SOURCE_TASK_COL: str = "source_task"
SEED_COL: str = "seed"
GENERATION_COL: str = "generation"
INDIVIDUAL_IDX_COL: str = "individual_idx"
DSI_COL: str = "dsi_vector_sum"
PD_RATE_COL: str = "pd_rate_hz"
MORPH_SEED_COL: str = "morph_seed"
CELL_ID_COL: str = "cell_id"
STRATUM_TAG_COL: str = "stratum_tag"

# Check result columns produced by run_checks.py.
CHECK1_PRIMARY_START_COL: str = "check1_primary_start"
CHECK2_PARENT_CHILD_COL: str = "check2_parent_child"
CHECK3_SYNAPSE_FRAME_COL: str = "check3_synapse_frame"

# ---------------------------------------------------------------------------
# Audit thresholds (per the research_code.md recommendation).
# ---------------------------------------------------------------------------

CHECK_ABS_TOL: float = 1e-6
CHECK_REL_TOL: float = 1e-9

# ---------------------------------------------------------------------------
# Stratification parameters
# ---------------------------------------------------------------------------

ASYMMETRY_PARAM_NAMES: tuple[str, ...] = (
    "soma_offset_pd_um",
    "field_elongation_pd",
    "branch_density_gradient_pd",
    "primary_branch_pd_concentration",
)

# BEDB_BASE_POINT reference values for symmetric-control selection.
# Source: tasks/t0090_morphology_generator_diversity_test/code/constants.py
BEDB_SYMMETRIC_CONTROL_REFS: dict[str, float] = {
    "soma_offset_pd_um": 0.0,
    "field_elongation_pd": 1.0,
    "branch_density_gradient_pd": 0.0,
    "primary_branch_pd_concentration": 0.0,
}

# Fractional tolerance for matching the BEDB_BASE_POINT defaults.
# For zero-valued refs (soma_offset, branch_density_gradient,
# primary_branch_pd_concentration) this is an absolute tolerance.
# For unit-valued refs (field_elongation_pd) this is a fractional tolerance.
SYMMETRIC_FRACTIONAL_TOL: float = 0.10

TARGET_MIN_CELLS: int = 15
TARGET_MAX_CELLS: int = 20


class StratumTag(StrEnum):
    """Stratum classification for a sampled cell."""

    SOMA_OFFSET_TOP = "SOMA_OFFSET_TOP"
    ELONGATION_TOP = "ELONGATION_TOP"
    ELONGATION_BOTTOM = "ELONGATION_BOTTOM"
    BRANCH_DENSITY_TOP = "BRANCH_DENSITY_TOP"
    PRIMARY_CONCENTRATION_TOP = "PRIMARY_CONCENTRATION_TOP"
    WORST_LOOKING = "WORST_LOOKING"
    SYMMETRIC_CONTROL = "SYMMETRIC_CONTROL"
