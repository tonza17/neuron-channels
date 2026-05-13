"""Named constants for t0105_preliminary_figures_report figure renderers."""

from __future__ import annotations

# Matplotlib output defaults.
DPI: int = 150
FACECOLOR: str = "white"
BBOX_INCHES: str = "tight"

# CSV / JSON column and key names.
COL_DIRECTION_LABEL: str = "direction_label"
COL_DIRECTION_DEG: str = "direction_deg"
COL_PEAK_PSP_MV: str = "peak_psp_mv"
COL_TRIAL_SEED: str = "trial_seed"
COL_MODE: str = "mode"
COL_DIRECTION: str = "direction"
COL_T_MS: str = "t_ms"
COL_V_MV: str = "v_mv"
COL_TRIAL: str = "trial"

# Polar layout.
PD_ANGLE_DEG: float = 0.0
ND_ANGLE_DEG: float = 180.0

# Direction labels.
DIRECTION_PD: str = "PD"
DIRECTION_ND: str = "ND"

# Vm trace modes.
MODE_FULL: str = "FULL"
MODE_EPSP_PASSIVE: str = "EPSP_PASSIVE"
MODE_IPSP_PASSIVE: str = "IPSP_PASSIVE"

# Bed labels.
BED_A_LABEL: str = "Bed A (t0008, Poleg-Polsky 2016)"
BED_B_LABEL: str = "Bed B (t0024, de Rosenroll 2026)"
BED_A_SHORT: str = "Bed A"
BED_B_SHORT: str = "Bed B"

# Three-mode colour map.
MODE_COLORS: dict[str, str] = {
    MODE_FULL: "black",
    MODE_EPSP_PASSIVE: "tab:blue",
    MODE_IPSP_PASSIVE: "tab:red",
}

# Figure 6 (channel-effect) DSI y-range.
DSI_Y_MIN: float = -0.5
DSI_Y_MAX: float = 1.05

# Figure 7 (Pareto top-5) filter and selection.
PD_RATE_MIN_HZ: float = 5.0
TOP_K_PARETO_CELLS: int = 5

# Morphology rendering constants (mirrored from t0098/code/constants.py).
SOMA_SECTION_NAME: str = "soma"
SOMA_RADIUS_DRAW_UM: float = 8.0
DENDRITE_LINEWIDTH: float = 0.5
AIS_LINEWIDTH: float = 1.0

# Seed colour map for figure 7 (cells coloured by Pareto seed of origin).
SEED_COLORS: dict[int, str] = {
    44: "tab:blue",
    55: "tab:orange",
}
DEFAULT_SEED_COLOR: str = "tab:gray"

# Slide deck layout (16:9 widescreen).
SLIDE_WIDTH_IN: float = 13.333
SLIDE_HEIGHT_IN: float = 7.5

# Metrics file keys.
METRIC_DSI: str = "direction_selectivity_index"

# Minimum PNG size sanity check (bytes).
MIN_PNG_BYTES: int = 5000
