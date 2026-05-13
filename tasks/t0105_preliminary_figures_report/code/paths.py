"""Centralised pathlib.Path constants for t0105_preliminary_figures_report.

All input and output paths used by the figure renderers and the deck builder live here.
Inputs reference 13 dependency tasks; outputs land under results/images/, results/data/,
and the top-level results/ folder for the .pptx and metrics.json.
"""

from __future__ import annotations

from pathlib import Path

# Worktree root: tasks/t0105_.../code/paths.py -> three parents up.
REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0105_preliminary_figures_report"

# Output directories.
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"
DATA_DIR: Path = RESULTS_DIR / "data"

# Input CSVs and JSONs from dependency tasks.
T0046_PSP_CSV: Path = (
    REPO_ROOT
    / "tasks"
    / "t0046_reproduce_poleg_polsky_2016_exact"
    / "results"
    / "data"
    / "fig1_psp.csv"
)
T0065_TRACES_CSV: Path = (
    REPO_ROOT / "tasks" / "t0065_t0020_epsp_ipsp_vm_protocol" / "data" / "voltage_traces.csv"
)
T0066_TRACES_CSV: Path = (
    REPO_ROOT / "tasks" / "t0066_t0024_epsp_ipsp_vm_protocol" / "data" / "voltage_traces.csv"
)
T0067_DSI_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0067_t0065_soma_channel_addition_sweep"
    / "data"
    / "dsi_by_condition.json"
)
T0068_DSI_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0068_t0067_nav16_kv3_coexpression_rescue"
    / "data"
    / "dsi_by_condition.json"
)
T0069_DSI_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0069_t0067_ais_localised_channel_sweep"
    / "data"
    / "dsi_by_condition.json"
)
T0070_BED_A_MORPH_PNG: Path = (
    REPO_ROOT
    / "tasks"
    / "t0070_writeup_two_model_beds"
    / "results"
    / "images"
    / "bed_a_morphology.png"
)
T0070_BED_B_MORPH_PNG: Path = (
    REPO_ROOT
    / "tasks"
    / "t0070_writeup_two_model_beds"
    / "results"
    / "images"
    / "bed_b_morphology.png"
)
T0102_PARETO_SEED44_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0102_seedscale_n4_gen20"
    / "results"
    / "data"
    / "pareto_front_seed44.json"
)
T0102_PARETO_SEED55_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0102_seedscale_n4_gen20"
    / "results"
    / "data"
    / "pareto_front_seed55.json"
)

# Output PNG paths (one per figure).
FIG01_HH_EQUATIONS_PNG: Path = IMAGES_DIR / "fig01_hh_equations.png"
FIG02_TABLE_BED_A_PNG: Path = IMAGES_DIR / "fig02_conductance_table_bed_a.png"
FIG02_TABLE_BED_B_PNG: Path = IMAGES_DIR / "fig02_conductance_table_bed_b.png"
FIG03_BED_A_MORPH_PNG: Path = IMAGES_DIR / "fig03_bed_a_morphology.png"
FIG03_BED_B_MORPH_PNG: Path = IMAGES_DIR / "fig03_bed_b_morphology.png"
FIG04_BED_A_POLAR_PNG: Path = IMAGES_DIR / "fig04_polar_synaptic_bed_a.png"
FIG04_BED_B_POLAR_PNG: Path = IMAGES_DIR / "fig04_polar_synaptic_bed_b.png"
FIG05_THREE_MODE_PNG: Path = IMAGES_DIR / "fig05_three_mode_overlays.png"
FIG06_CHANNEL_EFFECT_PNG: Path = IMAGES_DIR / "fig06_channel_effect_on_dsi.png"
FIG07_TOP5_PARETO_PNG: Path = IMAGES_DIR / "fig07_top5_pareto_3obj.png"

# Sidecar data outputs.
FIG07_TOP5_CELLS_JSON: Path = DATA_DIR / "fig07_top5_cells.json"

# Deck and metrics.
DECK_PPTX: Path = RESULTS_DIR / "preliminary_figures_slides.pptx"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
