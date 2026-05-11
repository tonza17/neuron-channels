"""Constants for the Baden 2016 DS-cell extraction.

The authoritative DS group set is `{2, 6, 12, 13, 16, 25, 26, 29}`, taken
directly from Baden et al. 2016 (Nature) main text, "Direction and orientation
selectivity":

    "Most DS cells (70%) were sorted into 8 groups (G 2, 6, 12, 13, 16, 25, 26,
    29)."

The labels are taken from `plotStamp.m` lines 35-39 of the Baden lab
visualisation MATLAB zip (`data/visualization_code/plotStamp.m`).
"""

from __future__ import annotations

PAPER_ID: str = "10.1038_nature16468"
DATASET_ID: str = "baden-2016-ds-cells"

# Authoritative DS group set (the paper's own enumeration).
DS_GROUP_IDS: list[int] = [2, 6, 12, 13, 16, 25, 26, 29]

# Group labels (canonical names from plotStamp.m's `names` array).
DS_GROUP_LABELS: dict[int, str] = {
    2: "OFF DS",
    6: "(ON-)OFF JAM-B mix",
    12: "ON-OFF DS 1",
    13: "ON-OFF DS 2",
    16: "ON DS trans.",
    25: "ON DS sust. 1",
    26: "ON slow",
    29: "ON local sust. OS",
}

# Full per-cell field count expected in the .mat container (sanity check;
# updated empirically by `load_baden_mat.py`).
TOTAL_BADEN_CELLS_EXPECTED: int = 11210

# Source URLs (recorded in download_manifest.json entries).
DRYAD_DOI: str = "10.5061/dryad.d9v38"
DRYAD_DOI_URL: str = "https://doi.org/10.5061/dryad.d9v38"
DRYAD_DATASET_URL: str = "https://datadryad.org/dataset/doi:10.5061/dryad.d9v38"
DRYAD_README_URL: str = "https://datadryad.org/downloads/file_stream/3407"

PAPER_DOI: str = "10.1038/nature16468"
PAPER_URL: str = "https://www.nature.com/articles/nature16468"
PAPER_PMC_ID: str = "PMC4724341"
PAPER_PMID: str = "26735013"
PAPER_PUB_DATE: str = "2016-01-21"
PAPER_YEAR: int = 2016

VISUALIZATION_ZIP_URL: str = (
    "http://retinal-functomics.net/wp-content/uploads/2015/12/Baden_et_al_2016_visualization.zip"
)

# Field-name constants used when serialising per-cell records.
FIELD_CELL_INDEX: str = "cell_index"
FIELD_GROUP_ID: str = "group_id"
FIELD_GROUP_LABEL: str = "group_label"
FIELD_CLUSTER_ID: str = "cluster_id"
FIELD_SELECTED: str = "selected"
FIELD_SOMA_AREA: str = "soma_area_um2"
FIELD_SOMA_VOLUME: str = "soma_volume_um3"
FIELD_DSI: str = "dsi"
FIELD_OSI: str = "osi"
FIELD_DSI_PVALUE: str = "dsi_pvalue"
FIELD_OSI_PVALUE: str = "osi_pvalue"
FIELD_FF_INDEX: str = "ff_index"
FIELD_ON_OFF_INDEX: str = "on_off_index"
FIELD_CHIRP_QI: str = "chirp_qi"
FIELD_BAR_QI: str = "bar_qi"
FIELD_COLOR_QI: str = "color_qi"
FIELD_RF_QI: str = "rf_qi"
FIELD_CHIRP_SCALING: str = "chirp_scaling"
FIELD_RF_SIZE: str = "rf_diameter_um"
FIELD_RF_GAUSS_MEAN_X: str = "rf_gauss_mean_x"
FIELD_RF_GAUSS_MEAN_Y: str = "rf_gauss_mean_y"
FIELD_RF_GAUSS_STD_X: str = "rf_gauss_std_x"
FIELD_RF_GAUSS_STD_Y: str = "rf_gauss_std_y"
FIELD_IMMUNO_CHAT: str = "immuno_chat"
FIELD_IMMUNO_GAD: str = "immuno_gad"
FIELD_IMMUNO_MELANOPSIN: str = "immuno_melanopsin"
FIELD_IMMUNO_SMI: str = "immuno_smi32"
FIELD_GENETICS_PV: str = "genetics_pv"
FIELD_GENETICS_PCP: str = "genetics_pcp"
FIELD_DATE: str = "recording_date"
FIELD_MOUSE_ID: str = "mouse_id"
FIELD_EYE_ID: str = "eye_id"
FIELD_SCAN_NUM: str = "scan_num"
FIELD_STIM_NUM: str = "stim_num"
FIELD_CELL_NUM: str = "cell_num"
FIELD_CHIRP_AVG: str = "chirp_avg"
FIELD_BAR_TC: str = "bar_tc"
FIELD_BAR_BYREPEAT_BYDIR_MEAN: str = "bar_byrepeat_bydir_mean"
FIELD_COLOR_AVG: str = "color_avg"
FIELD_RF_TC: str = "rf_tc"
FIELD_NOISE_TRACE: str = "noise_trace"
