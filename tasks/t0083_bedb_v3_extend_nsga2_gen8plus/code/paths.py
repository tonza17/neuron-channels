"""Centralised path constants for the t0083 NSGA-II continuation task.

Reuses the t0080 v3 substrate library + harness; this module overrides the
result-output paths so writes go to t0083's own results dir, and adds
dependency-pointer constants for t0081's saved evaluation outputs (the
input dataset for the gen-7 reload).
"""

from __future__ import annotations

from pathlib import Path

_THIS_FILE: Path = Path(__file__).resolve()
TASK_ROOT: Path = _THIS_FILE.parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

CODE_DIR: Path = TASK_ROOT / "code"

# Local result outputs.
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
IMAGES_DIR: Path = RESULTS_DIR / "images"
INTERVENTION_DIR: Path = TASK_ROOT / "intervention"
LOGS_DIR: Path = TASK_ROOT / "logs"

PARETO_FRONT_JSON: Path = RESULTS_DATA_DIR / "pareto_front.json"
ALL_EVALUATIONS_JSON: Path = RESULTS_DATA_DIR / "all_evaluations.json"
HV_TRAJECTORY_JSON: Path = RESULTS_DATA_DIR / "hv_trajectory.json"
PARAMETER_DISTRIBUTION_JSON: Path = RESULTS_DATA_DIR / "parameter_distribution.json"
RELOADED_GEN7_SURVIVORS_JSON: Path = RESULTS_DATA_DIR / "reloaded_gen7_survivors.json"
SMOKE_GATE_JSON: Path = LOGS_DIR / "smoke_gate.json"

BUDGET_OVERRUN_MD: Path = INTERVENTION_DIR / "budget_overrun.md"

# t0081 dependency paths (continuation data sources).
T0081_TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0081_bedb_v3_warmstart_nsga2"
T0081_ALL_EVALUATIONS_JSON: Path = T0081_TASK_ROOT / "results" / "data" / "all_evaluations.json"
T0081_PARETO_FRONT_JSON: Path = T0081_TASK_ROOT / "results" / "data" / "pareto_front.json"
T0081_HV_TRAJECTORY_JSON: Path = T0081_TASK_ROOT / "results" / "data" / "hv_trajectory.json"

# t0080 dependency paths (kept for reference / cross-task comparison).
T0080_TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
T0080_PARETO_FRONT_JSON: Path = T0080_TASK_ROOT / "results" / "data" / "pareto_front.json"


def ensure_directories() -> None:
    """Create all output directories (idempotent)."""
    for d in (RESULTS_DIR, RESULTS_DATA_DIR, IMAGES_DIR, LOGS_DIR, INTERVENTION_DIR):
        d.mkdir(parents=True, exist_ok=True)
