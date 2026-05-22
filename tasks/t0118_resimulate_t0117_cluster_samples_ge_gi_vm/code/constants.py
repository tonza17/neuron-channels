"""Sampling, simulation, metric, and figure constants for t0118.

All magic numbers and string keys used by the t0118 pipeline are defined here. See
``plan/plan.md`` Step 2 for the requirement-to-constant mapping.
"""

from __future__ import annotations

from enum import IntEnum, StrEnum

# ---------------------------------------------------------------------------
# Selection / sampling
# ---------------------------------------------------------------------------
SAMPLE_SEED: int = 117
N_CLUSTERS: int = 4
N_CELLS_PER_CLUSTER: int = 10
N_DSI_QUINTILES: int = 5
N_PD_QUINTILES: int = 5
N_SELECTED_CELLS_TOTAL: int = N_CLUSTERS * N_CELLS_PER_CLUSTER  # 40

# Cap for INT32-safe morph_seed handling (matches t0117/t0109 convention).
MAX_MORPH_SEED: int = 2**31 - 1

# ---------------------------------------------------------------------------
# Simulation / recording
# ---------------------------------------------------------------------------
RECORD_DT_MS: float = 1.0
TSTOP_MS: float = 1400.0
DT_MS: float = 0.1
EXPECTED_TRACE_ROWS: int = int(TSTOP_MS / RECORD_DT_MS)  # 1400 samples per trace

# AR(2) per-cell seeding: seed = SAMPLE_SEED + cell_index * 10_007 + int(direction_deg) * 13.
SEED_CELL_STRIDE: int = 10_007
SEED_DIRECTION_MULT: int = 13

# ---------------------------------------------------------------------------
# Trace parquet column names
# ---------------------------------------------------------------------------
T_MS_COL: str = "t_ms"
G_E_US_COL: str = "g_e_us"
G_I_US_COL: str = "g_i_us"
V_M_MV_COL: str = "v_m_mv"

# ---------------------------------------------------------------------------
# Per-cell metric keys (column names in per_cell_metrics.csv)
# ---------------------------------------------------------------------------
CLUSTER_ID_COL: str = "cluster_id"
SOURCE_TASK_COL: str = "source_task"
SEED_COL: str = "seed"
GENERATION_COL: str = "generation"
INDIVIDUAL_IDX_COL: str = "individual_idx"
DSI_COL: str = "dsi_vector_sum"
PD_RATE_COL: str = "pd_rate_hz"
DSI_QUINTILE_COL: str = "dsi_quintile"
PD_QUINTILE_COL: str = "pd_quintile"
DIRECTION_DEG_COL: str = "direction_deg"
PEAK_G_E_COL: str = "peak_g_e_us"
PEAK_G_E_TIME_MS_COL: str = "peak_g_e_time_ms"
PEAK_G_I_COL: str = "peak_g_i_us"
PEAK_G_I_TIME_MS_COL: str = "peak_g_i_time_ms"
GI_GE_RATIO_AT_PEAK_GE_COL: str = "gi_ge_ratio_at_peak_ge"
G_I_ONSET_LATENCY_MS_COL: str = "g_i_onset_latency_ms"
N_SPIKES_COL: str = "n_spikes"
MEAN_V_M_MV_COL: str = "mean_v_m_mv"
MAX_V_M_MV_COL: str = "max_v_m_mv"

# Quality check thresholds.
DSI_SANITY_THRESHOLD: float = 0.5
SPIKE_THRESHOLD_MV: float = -10.0
SPIKE_REFRACTORY_MS: float = 2.0

# Failure CSV columns.
FAILURE_CELL_KEY_COL: str = "cell_key"
FAILURE_MODE_COL: str = "mode"
FAILURE_DIRECTION_COL: str = "direction_deg"
FAILURE_ERROR_TYPE_COL: str = "error_type"
FAILURE_ERROR_MESSAGE_COL: str = "error_message"

# DSI sanity check columns.
SANITY_CELL_KEY_COL: str = "cell_key"
SANITY_N_SPIKES_PD_COL: str = "n_spikes_pd"
SANITY_N_SPIKES_ND_COL: str = "n_spikes_nd"
SANITY_PASSED_COL: str = "passed"


class TrialMode(StrEnum):
    """Three canonical mode-trio entries (matches t0066 convention)."""

    EPSP_PASSIVE = "EPSP_PASSIVE"
    IPSP_PASSIVE = "IPSP_PASSIVE"
    FULL = "FULL"


class Direction(IntEnum):
    """PD = 0 deg, ND = 180 deg per t0024 convention (PD is the cell's preferred direction)."""

    PD_DEG = 0
    ND_DEG = 180


# ---------------------------------------------------------------------------
# HH-off zero-out target lists.
# ---------------------------------------------------------------------------
# The 12 t80 channel suffixes inserted by apply_params._insert_channels_once on soma + all_dends,
# plus skahpt80 (on soma+dends+AIS) and HHst (inserted by t0092 baseline + by extend_with_ais).
# AIS additionally carries the AIS-permitted subset (Nav1.6, Kv3, Kv7) per extend_with_ais.
# The full zero-out list applied to every segment in EPSP/IPSP passive modes:
HH_OFF_T80_SUFFIXES: tuple[str, ...] = (
    "nav16t80",
    "napt80",
    "nart80",
    "kdrt80",
    "kv3t80",
    "kv4t80",
    "kv7t80",
    "iht80",
    "calt80",
    "catt80",
    "bkt80",
    "skt80",
)
HH_OFF_SLOW_AHP_SUFFIX: str = "skahpt80"
HH_OFF_HHST_PARAMS: tuple[str, ...] = ("gnabar_HHst", "gkbar_HHst", "gkmbar_HHst")

# Selected cells CSV column order.
SELECTED_CELLS_COLUMNS: tuple[str, ...] = (
    CLUSTER_ID_COL,
    SOURCE_TASK_COL,
    SEED_COL,
    GENERATION_COL,
    INDIVIDUAL_IDX_COL,
    DSI_COL,
    PD_RATE_COL,
    DSI_QUINTILE_COL,
    PD_QUINTILE_COL,
)

# Figure rendering constants.
FIGURE_DPI: int = 120
PER_CLUSTER_FIGSIZE_INCHES: tuple[float, float] = (15.0, 30.0)
CROSS_CLUSTER_FIGSIZE_INCHES: tuple[float, float] = (15.0, 12.0)
PD_LINESTYLE: str = "-"
ND_LINESTYLE: str = "--"
TRACE_COLOR_BY_CLUSTER: tuple[str, str, str, str] = (
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
)
