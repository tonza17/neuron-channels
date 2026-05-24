"""Threshold, literature, and bootstrap constants for t0121.

These mirror the canonical t0115 thresholds bit-for-bit; any drift is a
real bug. The bootstrap constants ``BOOTSTRAP_B``, ``BOOTSTRAP_SEED``,
``BOOTSTRAP_PERCENTILES`` are new in t0121 and are pinned for reproducibility.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Acceptance-rate thresholds (copy from t0115)
# ---------------------------------------------------------------------------

DSI_THRESHOLD: float = 0.5
PD_RATE_THRESHOLD_HZ: float = 30.0
LEGIT_DSI_CEILING: float = 0.9999
SILENCE_GUARD_DSI: float = 1.0

# ---------------------------------------------------------------------------
# Literature baselines
# ---------------------------------------------------------------------------

# Hay 2011 envelope upper bound: ~2000 accepted / 500K evaluations on the
# 22-d L5b pyramidal cell substrate ("[Hay2011, p. 4]").
HAY_2011_RATE_PCT: float = 0.40

# Hay 2011 perisomatic-only bottleneck: 52 accepted / 500K evaluations,
# the "substrate-limited counterexample" ("[Hay2011, p. 6]").
HAY_2011_PERISOMATIC_RATE_PCT: float = 0.0104

# Druckmann 2007 baseline: 300 accepted / 300K evaluations on the 12-d
# cortical interneuron substrate ("[Druckmann2007, Fig 3 + Methods]").
DRUCKMANN_2007_RATE_PCT: float = 0.10

# ---------------------------------------------------------------------------
# Bootstrap-CI configuration
# ---------------------------------------------------------------------------

BOOTSTRAP_B: int = 10000
BOOTSTRAP_SEED: int = 42
BOOTSTRAP_PERCENTILES: tuple[float, float] = (2.5, 97.5)

# ---------------------------------------------------------------------------
# Canonical 5-seed verification anchors (pinned from t0115 substrate_rate_5seed.csv)
# ---------------------------------------------------------------------------
# Source: tasks/t0115_seed9354_no_autostop/results/data/substrate_rate_5seed.csv

EXPECTED_N_EVALS: dict[str, int] = {
    "t0106_seed44": 3744,
    "t0112_seed77": 2016,
    "t0113_seed2247": 1344,
    "t0114_seed7755": 5952,
    "t0115_seed9354": 5280,
}

EXPECTED_LEGIT_COUNT: dict[str, int] = {
    "t0106_seed44": 121,
    "t0112_seed77": 7,
    "t0113_seed2247": 0,
    "t0114_seed7755": 484,
    "t0115_seed9354": 63,
}

# Source: t0115 substrate_rate_5seed.csv (5-seed mean = 2.5808, SE = 1.4969).
EXPECTED_MEAN_PCT: float = 2.58
EXPECTED_SE_PCT: float = 1.50
EXPECTED_N_SEEDS_ABOVE_HAY: int = 3  # seeds 44, 7755, 9354

# Per the project memory note: this report is dated 2026-05-24.
DATE_CREATED: str = "2026-05-24"
