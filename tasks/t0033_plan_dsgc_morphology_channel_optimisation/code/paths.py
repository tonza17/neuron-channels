"""Centralised file-path constants for task t0033.

All file paths produced or consumed by this planning task live here. Scripts
must import from this module rather than hard-coding paths inline.
"""

from pathlib import Path

TASK_ID: str = "t0033_plan_dsgc_morphology_channel_optimisation"
ANSWER_ID: str = "vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation"

# Repository root and task root.
REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / TASK_ID

# Task subfolders.
CODE_DIR: Path = TASK_ROOT / "code"
DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
ASSETS_ANSWER_DIR: Path = TASK_ROOT / "assets" / "answer" / ANSWER_ID

# Scripted data outputs (under `data/`).
MORPHOLOGY_PARAMS_JSON: Path = DATA_DIR / "morphology_params.json"
CHANNEL_PARAMS_HHST_JSON: Path = DATA_DIR / "channel_params_hhst.json"
TOP10_VGCS_JSON: Path = DATA_DIR / "top10_vgcs.json"
PARAM_SUMMARY_JSON: Path = DATA_DIR / "parameter_summary.json"

SEARCH_SPACE_CSV: Path = DATA_DIR / "search_space_table.csv"
WALL_TIME_BASE_CSV: Path = DATA_DIR / "sim_wall_time.csv"
WALL_TIME_PER_TIER_CSV: Path = DATA_DIR / "per_tier_wall_time.csv"
PRICING_JSON: Path = DATA_DIR / "vastai_pricing_snapshot.json"
COST_ENVELOPE_CSV: Path = DATA_DIR / "cost_envelope.csv"
SENSITIVITY_CSV: Path = DATA_DIR / "sensitivity_grid.csv"

# Chart outputs.
COST_BAR_CHART_PNG: Path = RESULTS_IMAGES_DIR / "cost_by_strategy_and_tier.png"
SENSITIVITY_HEATMAP_PNG: Path = RESULTS_IMAGES_DIR / "sensitivity_heatmap.png"
PARAM_COUNT_CHART_PNG: Path = RESULTS_IMAGES_DIR / "parameter_count_breakdown.png"

# Answer-asset documents.
ANSWER_DETAILS_JSON: Path = ASSETS_ANSWER_DIR / "details.json"
ANSWER_SHORT_MD: Path = ASSETS_ANSWER_DIR / "short_answer.md"
ANSWER_FULL_MD: Path = ASSETS_ANSWER_DIR / "full_answer.md"
