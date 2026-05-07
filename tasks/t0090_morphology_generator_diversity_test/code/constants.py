"""Constants for the t0090 procedural DSGC morphology generator task.

The 14 morphology parameter bounds and base point come from the task description's
parameter table in ``task_description.md``. The Bed-B-equivalent base point is
calibrated to the deRosenroll 2026 port from t0024 (matching ~341 sections / ~1300 um
total dendritic length).
"""

from __future__ import annotations

from enum import Enum

# ---------------------------------------------------------------------------
# Parameter names (typed string constants used throughout the codebase).
# ---------------------------------------------------------------------------

PARAM_NUM_PRIMARY_BRANCHES: str = "num_primary_branches"
PARAM_BRANCH_PROB_PER_UM: str = "branch_prob_per_um"
PARAM_MAX_STRAHLER_DEPTH: str = "max_strahler_depth"
PARAM_MEAN_BRANCHING_ANGLE_DEG: str = "mean_branching_angle_deg"
PARAM_RALL_EXPONENT: str = "rall_exponent"
PARAM_SOMA_OFFSET_PD_UM: str = "soma_offset_pd_um"
PARAM_FIELD_ELONGATION_PD: str = "field_elongation_pd"
PARAM_BRANCH_DENSITY_GRADIENT_PD: str = "branch_density_gradient_pd"
PARAM_PRIMARY_BRANCH_PD_CONCENTRATION: str = "primary_branch_pd_concentration"
PARAM_MEAN_SEGMENT_LENGTH_UM: str = "mean_segment_length_um"
PARAM_SOMA_DIAMETER_UM: str = "soma_diameter_um"
PARAM_AIS_LENGTH_UM: str = "ais_length_um"
PARAM_MORPH_SEED: str = "morph_seed"
PARAM_BRANCH_LENGTH_CV: str = "branch_length_cv"

PARAM_NAMES: tuple[str, ...] = (
    PARAM_NUM_PRIMARY_BRANCHES,
    PARAM_BRANCH_PROB_PER_UM,
    PARAM_MAX_STRAHLER_DEPTH,
    PARAM_MEAN_BRANCHING_ANGLE_DEG,
    PARAM_RALL_EXPONENT,
    PARAM_SOMA_OFFSET_PD_UM,
    PARAM_FIELD_ELONGATION_PD,
    PARAM_BRANCH_DENSITY_GRADIENT_PD,
    PARAM_PRIMARY_BRANCH_PD_CONCENTRATION,
    PARAM_MEAN_SEGMENT_LENGTH_UM,
    PARAM_SOMA_DIAMETER_UM,
    PARAM_AIS_LENGTH_UM,
    PARAM_MORPH_SEED,
    PARAM_BRANCH_LENGTH_CV,
)
assert len(PARAM_NAMES) == 14, "expected 14 morphology parameters"

INT_PARAM_NAMES: tuple[str, ...] = (
    PARAM_NUM_PRIMARY_BRANCHES,
    PARAM_MAX_STRAHLER_DEPTH,
    PARAM_MORPH_SEED,
)

# ---------------------------------------------------------------------------
# Parameter bounds: (lo, hi) per task description.
# ---------------------------------------------------------------------------

PARAM_BOUNDS: dict[str, tuple[float, float]] = {
    PARAM_NUM_PRIMARY_BRANCHES: (3.0, 7.0),
    PARAM_BRANCH_PROB_PER_UM: (0.005, 0.05),
    PARAM_MAX_STRAHLER_DEPTH: (2.0, 6.0),
    PARAM_MEAN_BRANCHING_ANGLE_DEG: (30.0, 90.0),
    PARAM_RALL_EXPONENT: (0.5, 2.0),
    PARAM_SOMA_OFFSET_PD_UM: (-150.0, 150.0),
    PARAM_FIELD_ELONGATION_PD: (1.0, 3.0),
    PARAM_BRANCH_DENSITY_GRADIENT_PD: (-1.0, 1.0),
    PARAM_PRIMARY_BRANCH_PD_CONCENTRATION: (0.0, 5.0),
    PARAM_MEAN_SEGMENT_LENGTH_UM: (10.0, 60.0),
    PARAM_SOMA_DIAMETER_UM: (8.0, 18.0),
    PARAM_AIS_LENGTH_UM: (15.0, 60.0),
    PARAM_MORPH_SEED: (0.0, float(2**31 - 1)),
    PARAM_BRANCH_LENGTH_CV: (0.0, 0.5),
}
assert set(PARAM_BOUNDS.keys()) == set(PARAM_NAMES)


# ---------------------------------------------------------------------------
# Bed-B-equivalent base point (matches t0024 / de Rosenroll 2026 morphology).
# Values calibrated to ~341 sections / ~1300 um total dendritic length when
# integer parameters are at their published Bed B counts (4 primaries) and
# floats default to mid-range or to the canonical Rall 3/2 exponent.
# ---------------------------------------------------------------------------

BEDB_BASE_POINT: dict[str, float] = {
    PARAM_NUM_PRIMARY_BRANCHES: 4.0,
    PARAM_BRANCH_PROB_PER_UM: 0.025,
    PARAM_MAX_STRAHLER_DEPTH: 5.0,
    PARAM_MEAN_BRANCHING_ANGLE_DEG: 45.0,
    PARAM_RALL_EXPONENT: 1.5,
    PARAM_SOMA_OFFSET_PD_UM: 0.0,
    PARAM_FIELD_ELONGATION_PD: 1.0,
    PARAM_BRANCH_DENSITY_GRADIENT_PD: 0.0,
    PARAM_PRIMARY_BRANCH_PD_CONCENTRATION: 0.0,
    PARAM_MEAN_SEGMENT_LENGTH_UM: 30.0,
    PARAM_SOMA_DIAMETER_UM: 15.0,
    PARAM_AIS_LENGTH_UM: 31.0,
    PARAM_MORPH_SEED: 1234.0,
    PARAM_BRANCH_LENGTH_CV: 0.1,
}
assert set(BEDB_BASE_POINT.keys()) == set(PARAM_NAMES)


# ---------------------------------------------------------------------------
# d_lambda rule (t0080 extend_with_ais defaults).
# ---------------------------------------------------------------------------

LAMBDA_F_FREQ_HZ: float = 100.0
D_LAMBDA: float = 0.1


# ---------------------------------------------------------------------------
# Stability flag for verification.
# ---------------------------------------------------------------------------


class StabilityKind(Enum):
    STABLE = "stable"
    NAN_VOLTAGE = "nan_voltage"
    DIVERGED = "diverged"
    DISCONNECTED = "disconnected"


# ---------------------------------------------------------------------------
# Phase G constants.
# ---------------------------------------------------------------------------

# t0088 cluster 1 (cluster_id=1 in the 0-indexed JSON) cells.
CLUSTER_1_CELL_IDS: tuple[int, ...] = (1304, 1504, 1624, 1634)

# Cluster representatives (one per cluster, per t0088 representative_cells.json).
REPRESENTATIVE_CELL_IDS: tuple[int, ...] = (1604, 1634, 767, 1639)

# 16-direction angles in degrees, copied from t0088 run_deepdive.ANGLES_16DIR_DEG.
ANGLES_16DIR_DEG: tuple[float, ...] = tuple(i * 22.5 for i in range(16))

# Phase G.2 NMDA sweep levels (uS) — log-spaced over 1e-5 .. 1e-2.
GNMDA_SWEEP_US: tuple[float, ...] = (1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2)

# Soma Nav lower bound to detect floor-pinning in Phase G.1.
NAV16_SOMA_LOWER_BOUND_S_CM2: float = 1e-5

# Sivyer 2013 NMDA prior in per-spine conductance (nS).
SIVYER_NMDA_MEAN_NS: float = 0.1
SIVYER_NMDA_SIGMA_NS: float = 0.05


# ---------------------------------------------------------------------------
# Verification simulation settings.
# ---------------------------------------------------------------------------

VERIFY_NO_STIM_MS: float = 50.0
VERIFY_V_INIT_MV: float = -70.0
VERIFY_V_NAN_THRESHOLD_MV: float = 1e6  # voltage above this magnitude flags divergence.
VERIFY_TIMESTEP_MS: float = 0.1
VERIFY_CELSIUS_DEG_C: float = 36.9


# ---------------------------------------------------------------------------
# Sampling seeds.
# ---------------------------------------------------------------------------

LHS_DIFFERENT_SEED: int = 42
PERTURB_SIMILAR_SEED: int = 43
BEDB_PARETO_CHOICE_SEED: int = 0


# ---------------------------------------------------------------------------
# Geometry construction defaults (reused across generator + viz).
# ---------------------------------------------------------------------------

PARENT_TIP_LOC: float = 1.0  # NEURON normalised position used in connect()
CHILD_BASE_LOC: float = 0.0
DEFAULT_RA_OHM_CM: float = 100.0
DEFAULT_CM_UF_CM2: float = 1.0
DEFAULT_GLEAK_S_CM2: float = 1.667e-4
AIS_PROXIMAL_FRACTION: float = 0.5
AIS_DEFAULT_DIAMETER_UM: float = 0.8
DEFAULT_DENDRITE_DIAMETER_UM: float = 1.5
DEFAULT_TIP_DIAMETER_UM: float = 0.4

# 8-direction protocol angles for verification. PD = 0 deg.
ANGLES_8DIR_DEG: tuple[int, ...] = (0, 45, 90, 135, 180, 225, 270, 315)
PD_DIRECTION_DEG: float = 0.0
ND_DIRECTION_DEG: float = 180.0
