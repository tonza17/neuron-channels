"""Path constants for the t0041 electrotonic-length collapse analysis task.

All filesystem paths used by the L/lambda computation, the collapse plot generator, the Pearson r
collapse tester, and the answer-asset writer are centralised here per the project Python style
guide. Paths are anchored relative to this file so the task runs correctly regardless of the
current working directory.
"""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0041_electrotonic_length_collapse_t0034_t0035"

# This task's own output directories.
RESULTS_DIR: Path = TASK_ROOT / "results"
DATA_DIR: Path = RESULTS_DIR / "data"
IMAGES_DIR: Path = RESULTS_DIR / "images"
LOGS_DIR: Path = TASK_ROOT / "logs"

ELECTROTONIC_TABLE_CSV: Path = RESULTS_DIR / "electrotonic_length_table.csv"
COLLAPSE_STATS_JSON: Path = RESULTS_DIR / "collapse_stats.json"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"

PRIMARY_DSI_COLLAPSE_PNG: Path = IMAGES_DIR / "primary_dsi_vs_L_over_lambda.png"
VECTOR_SUM_DSI_COLLAPSE_PNG: Path = IMAGES_DIR / "vector_sum_dsi_vs_L_over_lambda.png"
PEAK_HZ_COLLAPSE_PNG: Path = IMAGES_DIR / "peak_hz_vs_L_over_lambda.png"

# Upstream inputs from the two completed dependency tasks.
T0034_TASK_DIR: Path = TASK_ROOT.parent / "t0034_distal_dendrite_length_sweep_t0024"
T0035_TASK_DIR: Path = TASK_ROOT.parent / "t0035_distal_dendrite_diameter_sweep_t0024"

T0034_METRICS_PER_LENGTH_CSV: Path = T0034_TASK_DIR / "results" / "data" / "metrics_per_length.csv"
T0035_METRICS_PER_DIAMETER_CSV: Path = (
    T0035_TASK_DIR / "results" / "data" / "metrics_per_diameter.csv"
)

# Distal-section preflight snapshots (produced by each dependency's preflight step).
T0034_DISTAL_SECTIONS_JSON: Path = T0034_TASK_DIR / "logs" / "preflight" / "distal_sections.json"
T0035_DISTAL_SECTIONS_JSON: Path = T0035_TASK_DIR / "logs" / "preflight" / "distal_sections.json"

# Answer asset location.
ANSWER_ID: str = "electrotonic-length-collapse-of-length-and-diameter-sweeps"
ANSWER_ASSET_DIR: Path = TASK_ROOT / "assets" / "answer" / ANSWER_ID
ANSWER_DETAILS_JSON: Path = ANSWER_ASSET_DIR / "details.json"
ANSWER_SHORT_MD: Path = ANSWER_ASSET_DIR / "short_answer.md"
ANSWER_FULL_MD: Path = ANSWER_ASSET_DIR / "full_answer.md"
