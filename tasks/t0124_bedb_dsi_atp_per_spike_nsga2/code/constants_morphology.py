"""t0124-specific constants for the 68-d random-init NSGA-II run.

Forked from t0123 with one delta:

* ``N_DIRECTIONS = 2`` (was ``4`` in t0123): halved back to the antipodal
  pair at 0/180 deg per task_description ``Hard Constraints``. The per-cell
  trial budget shrinks from 12 (3 eval seeds x 4 dirs) to 6 (3 eval seeds
  x 2 dirs). DSI only needs the antipodal pair; ATP-per-spike is
  direction-independent under per-spike normalisation.

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
from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.constants_electrophys import (
    INT_PARAM_INDICES as ELECTROPHYS_INT_INDICES,
)
from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.constants_electrophys import (
    LOWER_BOUNDS as LOWER_BOUNDS_54,
)
from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.constants_electrophys import (
    N_PARAMS as N_PARAMS_54,
)
from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.constants_electrophys import (
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
# t0123 inherits t0122's N_GEN = 60 per task_description.md ``Hard Constraints``
# section (``N_GEN_MAX = 60``). HV-plateau auto-stop remains DISABLED;
# budget cap and operator stop are binding.
N_GEN: int = 60
SBX_ETA: int = 15
SBX_PROB: float = 0.9
PM_ETA: int = 20
PM_PROB: float = 1.0 / 68

# HV plateau watchdog (REQ-6).
# t0106: raised MIN_HV_HISTORY from 4 -> 60 (1-hour sliding window at ~60s/gen)
# so the t0102 watchdog does not spuriously trigger inside the 300-gen run.
HV_PLATEAU_REL_THRESHOLD: float = 0.01
HV_PLATEAU_WINDOW: int = 2
HV_PLATEAU_MIN_HV_HISTORY: int = 60

# Cost watchdog hard cap (REQ-7).
T0104_HARD_BUDGET_USD: float = 4.00

# Eval defaults (REQ-4, REQ-5).
# t0124: N_EVAL_SEEDS = 3; N_DIRECTIONS = 2 (antipodal pair at 0/180 deg).
N_EVAL_SEEDS: int = 3
N_DIRECTIONS: int = 2
DSI_TOLERANCE_SMOKE: float = 0.05
PD_RATE_TOLERANCE_HZ_SMOKE: float = 1.0

# Reference point for hypervolume.
# t0123: objectives are 2-d (negated MI, +ATP_per_spike); the F-sign of
# the ATP axis is POSITIVE because it is minimised directly (not negated).
# REF_POINT_HV is therefore a 2-entry pair: 0.0 for the negated-MI axis
# (worst case = MI 0 -> -0 = 0), and WORST_CASE_ATP_PER_SPIKE for the ATP
# axis (pessimistic upper bound).
HV_UTOPIA_MI_BITS: float = 1.5
# Pessimistic / sentinel ATP-per-spike upper bound, used as both the HV
# reference point and the worst-case fallback for silent / failed cells.
ATP_PER_SPIKE_MAX_REF: float = 1e10
HV_UTOPIA_ATP_PER_SPIKE: float = 1e9
WORST_CASE_MI_BITS: float = 0.0
WORST_CASE_ATP_PER_SPIKE: float = ATP_PER_SPIKE_MAX_REF * 2.0
REF_POINT_HV: tuple[float, float] = (0.0, WORST_CASE_ATP_PER_SPIKE)
HV_UTOPIA_DSI: float = 0.7
HV_UTOPIA_PD_RATE_HZ: float = 80.0  # retained for diagnostics; not in F
HV_UTOPIA_ROBUSTNESS: float = 1.0  # retained for diagnostics; not in F

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
