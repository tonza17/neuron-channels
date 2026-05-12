"""t0102-specific constants for the 68-d random-init NSGA-II run.

Adapted verbatim from t0099, with two operative overrides per plan REQ-1/REQ-2:

* ``N_EVAL_SEEDS = 4`` (was ``5`` in t0099): reduce within-cell noise replicates
  by a factor of 5 from t0080's stale ``N_SEEDS = 20`` (Poleg-Polsky 2026 inspired
  schedule).
* ``N_GEN = 20`` (was ``8`` in t0099): extend generations 2.5x at the constant
  $8 task budget to test joint-pass corner recovery.

All other constants inherited from t0099 unchanged. See task plan
``tasks/t0102_seedscale_n4_gen20/plan/plan.md`` Step by Step Step 2.

Concatenates the t0080 54-d electrophys bounds with the t0090 14-d morphology
bounds (via t0092's library re-export) to form `LOWER_BOUNDS_68` /
`UPPER_BOUNDS_68`.

The 14 morphology dim names (in field order from t0090.morphology_params) are:
    0: num_primary_branches      (int, [3, 7])
    1: branch_prob_per_um        (float, [0.005, 0.05])
    2: max_strahler_depth        (int, [2, 6])
    3: mean_branching_angle_deg  (float, [30, 90])
    4: rall_exponent             (float, [0.5, 2.0])
    5: soma_offset_pd_um         (float, [-150, 150])
    6: field_elongation_pd       (float, [1.0, 3.0])
    7: branch_density_gradient_pd (float, [-1, 1])
    8: primary_branch_pd_concentration (float, [0, 5])
    9: mean_segment_length_um    (float, [10, 60])
   10: soma_diameter_um          (float, [8, 18])
   11: ais_length_um             (float, [15, 60])
   12: morph_seed                (int, [0, 2147483647])
   13: branch_length_cv          (float, [0, 0.5])
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    INT_PARAM_NAMES as MORPH_INT_PARAM_NAMES,
)
from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    PARAM_BOUNDS as MORPH_PARAM_BOUNDS,
)
from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    PARAM_NAMES as MORPH_PARAM_NAMES,
)
from tasks.t0102_seedscale_n4_gen20.code.constants_electrophys import (
    INT_PARAM_INDICES as ELECTROPHYS_INT_INDICES,
)
from tasks.t0102_seedscale_n4_gen20.code.constants_electrophys import (
    LOWER_BOUNDS as LOWER_BOUNDS_54,
)
from tasks.t0102_seedscale_n4_gen20.code.constants_electrophys import (
    N_PARAMS as N_PARAMS_54,
)
from tasks.t0102_seedscale_n4_gen20.code.constants_electrophys import (
    UPPER_BOUNDS as UPPER_BOUNDS_54,
)

# 14-d morphology bounds in field order.
N_MORPH_PARAMS: int = 14
assert len(MORPH_PARAM_NAMES) == N_MORPH_PARAMS, (
    f"morphology PARAM_NAMES has {len(MORPH_PARAM_NAMES)} entries, expected {N_MORPH_PARAMS}"
)


def _build_morph_bounds() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    lo: list[float] = []
    hi: list[float] = []
    for name in MORPH_PARAM_NAMES:
        b = MORPH_PARAM_BOUNDS[name]
        lo.append(float(b[0]))
        hi.append(float(b[1]))
    return np.array(lo, dtype=np.float64), np.array(hi, dtype=np.float64)


MORPHOLOGY_LOWER_BOUNDS, MORPHOLOGY_UPPER_BOUNDS = _build_morph_bounds()
assert MORPHOLOGY_LOWER_BOUNDS.shape == (N_MORPH_PARAMS,)
assert MORPHOLOGY_UPPER_BOUNDS.shape == (N_MORPH_PARAMS,)

# 68-d concatenated bounds: electrophys (54) + morphology (14).
N_PARAMS_68: int = N_PARAMS_54 + N_MORPH_PARAMS
assert N_PARAMS_68 == 68

LOWER_BOUNDS_68: NDArray[np.float64] = np.concatenate([LOWER_BOUNDS_54, MORPHOLOGY_LOWER_BOUNDS])
UPPER_BOUNDS_68: NDArray[np.float64] = np.concatenate([UPPER_BOUNDS_54, MORPHOLOGY_UPPER_BOUNDS])
assert LOWER_BOUNDS_68.shape == (N_PARAMS_68,)
assert UPPER_BOUNDS_68.shape == (N_PARAMS_68,)


def _build_int_indices_68() -> tuple[int, ...]:
    """Combined integer indices: 2 electrophys (39, 40) + 3 morphology (54+0, 54+2, 54+12)."""
    out: list[int] = list(ELECTROPHYS_INT_INDICES)  # (39, 40)
    for name in MORPH_INT_PARAM_NAMES:
        morph_local = MORPH_PARAM_NAMES.index(name)
        out.append(N_PARAMS_54 + morph_local)
    return tuple(sorted(set(out)))


INT_PARAM_INDICES_68: tuple[int, ...] = _build_int_indices_68()
# Expected: (39, 40, 54, 56, 66) — 5 indices.
assert len(INT_PARAM_INDICES_68) == 5, (
    f"expected 5 int indices, got {len(INT_PARAM_INDICES_68)}: {INT_PARAM_INDICES_68}"
)

# NSGA-II / pymoo defaults (REQ-2, REQ-5, REQ-6).
POP_SIZE: int = 96
# t0102 plan REQ-2: extend N_GEN from t0099's 8 to 20 (2.5x more generations).
N_GEN: int = 20
SBX_ETA: int = 15
SBX_PROB: float = 0.9
PM_ETA: int = 20
PM_PROB: float = 1.0 / 68

# HV plateau watchdog (REQ-6).
HV_PLATEAU_REL_THRESHOLD: float = 0.01
HV_PLATEAU_WINDOW: int = 2
HV_PLATEAU_MIN_HV_HISTORY: int = 4

# Cost watchdog hard cap (REQ-7).
T0102_HARD_BUDGET_USD: float = 4.00

# Eval defaults (REQ-8).
# t0102 plan REQ-1: reduce N_EVAL_SEEDS from t0099's 5 to 4 (5x reduction from t0080's stale 20).
N_EVAL_SEEDS: int = 4
N_DIRECTIONS: int = 16
DSI_TOLERANCE_SMOKE: float = 0.05
PD_RATE_TOLERANCE_HZ_SMOKE: float = 1.0

# Reference point for hypervolume; objectives are negated DSI, negated PD-rate,
# and inverse-CV robustness so we minimise. All 3 worst-case bounds at ~0.
REF_POINT_HV: tuple[float, float, float] = (0.0, 0.0, 0.0)
HV_UTOPIA_DSI: float = 0.7
HV_UTOPIA_PD_RATE_HZ: float = 80.0
HV_UTOPIA_ROBUSTNESS: float = 1.0

# 5 anchor names (REQ-4).
ANCHOR_NAMES: tuple[str, ...] = (
    "bedb_like",
    "symmetric",
    "pd_asymmetric",
    "nd_asymmetric",
    "alt_topology",
)
N_ANCHORS: int = 5

# Worst-case fallback for failed evaluations (penalty).
WORST_CASE_DSI: float = -1.0
WORST_CASE_PD_RATE_HZ: float = 0.0
WORST_CASE_ROBUSTNESS: float = 0.0

# Anchor warmstart layout: 5 anchors x 19 electrophys clones + 1 random = 96.
N_CLONES_PER_ANCHOR: int = 19
N_RANDOM_FILL: int = 1
assert N_ANCHORS * N_CLONES_PER_ANCHOR + N_RANDOM_FILL == POP_SIZE
