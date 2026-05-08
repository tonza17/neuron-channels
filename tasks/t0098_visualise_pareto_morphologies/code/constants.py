"""Constants for t0098_visualise_pareto_morphologies chart generation."""

from __future__ import annotations

ANCHOR_COLORS: dict[str, str] = {
    "bedb_like": "tab:blue",
    "symmetric": "tab:gray",
    "pd_asymmetric": "tab:red",
    "nd_asymmetric": "tab:green",
    "alt_topology": "tab:purple",
}
DEFAULT_COLOR: str = "black"

DSI_THRESHOLD: float = 0.5
PD_THRESHOLD_HZ: float = 30.0
ROBUSTNESS_THRESHOLD: float = 0.7

GRID_ROWS: int = 8
GRID_COLS: int = 8
DPI: int = 120
GRID_FIGSIZE_IN: tuple[float, float] = (16.0, 16.0)
BAR_FIGSIZE_IN: tuple[float, float] = (14.0, 5.0)
SCATTER_FIGSIZE_IN: tuple[float, float] = (8.0, 6.5)

SOMA_SECTION_NAME: str = "soma"
SOMA_RADIUS_DRAW_UM: float = 8.0
DENDRITE_LINEWIDTH: float = 0.5
AIS_LINEWIDTH: float = 1.0
PANEL_TITLE_FONTSIZE: int = 7
SUPTITLE_FONTSIZE: int = 14
LEGEND_FONTSIZE: int = 8
