"""Module-level constants for tuning_curve_viz.

Defines the Okabe-Ito colour-blind-safe palette, matplotlib save defaults, the multi-model
overlay cap, PSTH bin width, and bootstrap parameters. All plotting functions read these
constants; do not hardcode equivalent values elsewhere in the package.
"""

from __future__ import annotations

# Okabe & Ito (2008) Color Universal Design palette. Eight hex codes, in order:
# black, orange, sky blue, bluish green, yellow, blue, vermillion, reddish purple.
# Black is reserved for the target curve on every overlay; yellow has low contrast on
# white and is therefore placed last in the model-colour rotation.
OKABE_ITO: tuple[str, ...] = (
    "#000000",
    "#E69F00",
    "#56B4E9",
    "#009E73",
    "#F0E442",
    "#0072B2",
    "#D55E00",
    "#CC79A7",
)

# Target curve is always black and dashed on overlays.
TARGET_COLOR: str = "#000000"
TARGET_LINESTYLE: str = "--"

# Model-curve colours drawn from Okabe-Ito minus black (reserved for target).
MODEL_COLORS: tuple[str, ...] = OKABE_ITO[1:]

# matplotlib PNG save defaults.
DEFAULT_DPI: int = 150
DEFAULT_FACECOLOR: str = "white"
DEFAULT_BBOX_INCHES: str = "tight"

# Multi-model overlay cap. >6 models would exhaust the black-less Okabe-Ito palette
# and produce illegible overlays.
MAX_OVERLAY_MODELS: int = 6

# PSTH bin width in seconds. 10 ms matches t0008's spike-time resolution per
# research_internet.md.
PSTH_BIN_WIDTH_S: float = 0.010

# scipy.stats.bootstrap parameters for the 95 percent CI band.
BOOTSTRAP_N_RESAMPLES: int = 1000
BOOTSTRAP_CONFIDENCE_LEVEL: float = 0.95
BOOTSTRAP_METHOD: str = "percentile"

# Permissive angle-grid counts accepted by the validator. Non-uniform grids raise.
ACCEPTED_ANGLE_COUNTS: tuple[int, ...] = (8, 12, 16)

# CI band alpha used by matplotlib's fill_between.
CI_BAND_ALPHA: float = 0.3

# Preferred-direction arrow colour.
PREFERRED_ARROW_COLOR: str = "red"

# Seed for synthetic raster+PSTH fixtures used by the smoke tests.
SMOKE_RNG_SEED: int = 42
