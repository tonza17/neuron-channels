"""Constants for t0050 audit (channel kinds, midline rules, t0049 cross-references, columns).

The deposited DSGC ``placeBIP()`` does NOT classify synapses as PD vs ND with a sign threshold;
instead the wave-direction logic uses each synapse's continuous ``locx`` value to compute per-
synapse ``starttime``. For audit reporting we adopt our own midline classification rule:

    midline rule: synapse.bip_locx_um < x_soma -> "side_a" (PD-side); else "side_b" (ND-side)

Robustness checks are reported for two alternative midlines (x = 0 and the median of all
BIPsyn.locx values). See research/research_code.md and plan/plan.md for the rationale.
"""

from __future__ import annotations

from enum import StrEnum


class ChannelKind(StrEnum):
    """Per-channel-class identifier matching the deposited HOC array names."""

    BIP = "BIPsyn"
    SAC_EXC = "SACexcsyn"
    SAC_INHIB = "SACinhibsyn"


CHANNEL_DISPLAY_NAMES: dict[ChannelKind, str] = {
    ChannelKind.BIP: "NMDA + AMPA (BIP)",
    ChannelKind.SAC_EXC: "SAC excitatory (ACh)",
    ChannelKind.SAC_INHIB: "SAC inhibitory (GABA)",
}


# Symmetry threshold rule: count_side_a / count_side_b in [0.9, 1.1] -> symmetric.
SYMMETRY_RATIO_LOW: float = 0.9
SYMMETRY_RATIO_HIGH: float = 1.1


# t0049 GABA SEClamp cross-reference values (for synthesis discussion only; not measured here).
# Source: tasks/t0049_seclamp_cond_remeasure/results/data/seclamp_comparison_table.csv (PD ~47.47,
# ND ~48.04 nS GABA somatic SEClamp; DSI ~ -0.006, contradicting paper PD 12.5 / ND 30 nS DSI ~
# -0.41).
T0049_GABA_PD_NS: float = 47.47
T0049_GABA_ND_NS: float = 48.04
T0049_GABA_DSI: float = -0.006


# Midline conventions explored for sensitivity.
MIDLINE_KIND_SOMA_X: str = "soma_x"
MIDLINE_KIND_ZERO: str = "zero"
MIDLINE_KIND_BIP_MEDIAN: str = "bipsyn_locx_median"
MIDLINE_KINDS: tuple[str, ...] = (
    MIDLINE_KIND_SOMA_X,
    MIDLINE_KIND_ZERO,
    MIDLINE_KIND_BIP_MEDIAN,
)


# Side labels.
SIDE_A: str = "side_a"
SIDE_B: str = "side_b"


# CSV column names for synapse_coordinates.csv (per-synapse extraction; 17 columns total).
COLUMN_INDEX: str = "index"
COLUMN_BIP_LOCX_UM: str = "bip_locx_um"
COLUMN_BIP_LOCY_UM: str = "bip_locy_um"
COLUMN_BIP_Z_UM: str = "bip_z_um"
COLUMN_SAC_INHIB_LOCX_UM: str = "sac_inhib_locx_um"
COLUMN_SAC_INHIB_LOCY_UM: str = "sac_inhib_locy_um"
COLUMN_SAC_INHIB_Z_UM: str = "sac_inhib_z_um"
COLUMN_SAC_EXC_LOCX_UM: str = "sac_exc_locx_um"
COLUMN_SAC_EXC_LOCY_UM: str = "sac_exc_locy_um"
COLUMN_SAC_EXC_Z_UM: str = "sac_exc_z_um"
COLUMN_PARENT_SECTION_NAME: str = "parent_section_name"
COLUMN_PARENT_SECTION_LENGTH_UM: str = "parent_section_length_um"
COLUMN_PARENT_SECTION_CENTROID_X_UM: str = "parent_section_centroid_x_um"
COLUMN_PARENT_SECTION_CENTROID_Y_UM: str = "parent_section_centroid_y_um"
COLUMN_PARENT_SECTION_CENTROID_Z_UM: str = "parent_section_centroid_z_um"
COLUMN_PATH_DISTANCE_UM: str = "path_distance_um"
COLUMN_RADIAL_DISTANCE_UM: str = "radial_distance_from_soma_um"


# Per-channel locx column lookup (used by stats/figures to fetch each channel's x-coordinate).
CHANNEL_LOCX_COLUMNS: dict[ChannelKind, str] = {
    ChannelKind.BIP: COLUMN_BIP_LOCX_UM,
    ChannelKind.SAC_EXC: COLUMN_SAC_EXC_LOCX_UM,
    ChannelKind.SAC_INHIB: COLUMN_SAC_INHIB_LOCX_UM,
}


# CSV column names for per_channel_density_stats.csv (one row per channel x midline).
COLUMN_CHANNEL: str = "channel"
COLUMN_MIDLINE_KIND: str = "midline_kind"
COLUMN_MIDLINE_X_UM: str = "midline_x_um"
COLUMN_COUNT_TOTAL: str = "count_total"
COLUMN_COUNT_SIDE_A: str = "count_side_a"
COLUMN_COUNT_SIDE_B: str = "count_side_b"
COLUMN_COUNT_RATIO: str = "count_ratio_side_a_over_b"
COLUMN_MEAN_RADIAL_SIDE_A: str = "mean_radial_distance_side_a_um"
COLUMN_SD_RADIAL_SIDE_A: str = "sd_radial_distance_side_a_um"
COLUMN_MEAN_RADIAL_SIDE_B: str = "mean_radial_distance_side_b_um"
COLUMN_SD_RADIAL_SIDE_B: str = "sd_radial_distance_side_b_um"
COLUMN_MEAN_PATH_SIDE_A: str = "mean_path_distance_side_a_um"
COLUMN_SD_PATH_SIDE_A: str = "sd_path_distance_side_a_um"
COLUMN_MEAN_PATH_SIDE_B: str = "mean_path_distance_side_b_um"
COLUMN_SD_PATH_SIDE_B: str = "sd_path_distance_side_b_um"
COLUMN_TOTAL_LENGTH_SIDE_A: str = "total_length_side_a_um"
COLUMN_TOTAL_LENGTH_SIDE_B: str = "total_length_side_b_um"
COLUMN_DENSITY_SIDE_A: str = "density_side_a_per_um"
COLUMN_DENSITY_SIDE_B: str = "density_side_b_per_um"
COLUMN_VERDICT_SYMMETRIC: str = "verdict_symmetric"


# Expected synapse count from the deposited model.
EXPECTED_NUMSYN: int = 282
