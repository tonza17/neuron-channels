"""Task-local constants for t0088_recluster_marginals_and_vm_motifs."""

from __future__ import annotations

# 13 target cell IDs: 6 Genuine + 7 Marginal from t0086 cell_classification.json.
TARGET_CELL_IDS: tuple[int, ...] = (
    767,
    1304,
    1379,
    1504,
    1517,
    1559,
    1604,
    1624,
    1634,
    1639,
    1663,
    1677,
    1721,
)

# 16 stimulus directions at 22.5 deg spacing (every 22.5 degrees in [0, 360)).
ANGLES_16DIR_DEG: tuple[float, ...] = (
    0.0,
    22.5,
    45.0,
    67.5,
    90.0,
    112.5,
    135.0,
    157.5,
    180.0,
    202.5,
    225.0,
    247.5,
    270.0,
    292.5,
    315.0,
    337.5,
)

# Integration window for attribution metric (ms). Matches t0084.
RESPONSE_WINDOW_START_MS: float = 200.0
RESPONSE_WINDOW_END_MS: float = 1200.0

# Recording timestep (matches RECORD_DT_MS from t0080 / t0084).
RECORD_DT_MS: float = 1.0

# Exp2NMDA reversal potential (from Exp2NMDA.mod parameter e = 0).
NMDA_EREV_MV: float = 0.0

# Human-readable channel names matching the attribution result fields.
CHANNEL_NAMES: tuple[str, str, str] = ("nmda", "nav16", "nap")

# PD direction (preferred direction; bar moves +x).
PD_DIRECTION_DEG: float = 0.0

# ND direction (null direction; bar moves -x).
ND_DIRECTION_DEG: float = 180.0

# Clustering hyperparameters (match t0086).
K_MIN: int = 2
K_MAX: int = 6
RANDOM_STATE: int = 42
N_BOOTSTRAP: int = 50
BOOTSTRAP_SUBSAMPLE_FRAC: float = 0.8

# Verdict thresholds (sigma) for biological scorecard (match t0086).
PLAUSIBLE_THRESHOLD_SIGMA: float = 2.0
STRETCHED_THRESHOLD_SIGMA: float = 5.0
