---
spec_version: "3"
task_id: "t0046_reproduce_poleg_polsky_2016_exact"
step_number: 7
step_name: "planning"
status: "completed"
started_at: "2026-04-24T14:02:36Z"
completed_at: "2026-04-24T14:15:00Z"
---
## Summary

Produced `plan/plan.md` via the `/planning` skill subagent with 20 REQ-1..REQ-20 requirement items
and 19 Step-by-Step actions grouped into 6 milestones (A-F). Morphology decision locked in:
HOC-embedded `pt3dadd` reconstruction from `RGCmodel.hoc` is used verbatim; t0005's SWC is
explicitly NOT swapped in because `placeBIP()` depends on section ordering and an ON/OFF cut plane.
Plan retains the corrected task targets (PSPs / slopes / ROC, not spike rates). Verificator passed
with zero errors.

## Actions Taken

1. Spawned a `/planning` subagent with all three research outputs plus the corrected
   task_description.md, and explicit constraints (no fork of t0008/t0020/t0022, cross-task copy
   rule, gNMDA 0.5 nS primary / 2.5 nS secondary, morphology choice, achMOD=0.33 rebind).
2. Subagent wrote `plan/plan.md` with the 11 mandatory sections plus 20 REQ items and a 19-step
   milestone-grouped Step-by-Step.
3. Ran `verify_plan.py` wrapped in `run_with_logs.py`; passed with zero errors and zero warnings.
4. Captured the plan's flagged risk for escalation: noise-driver behaviour at non-zero SD.
   `placeBIP()` has the driver authored but has never been exercised in the shipped code at
   `flickerVAR != 0`. Figures 6-8 pass criteria depend on it producing Gaussian perturbations with
   the requested SD. A latent bug here could force an explicit seeded `rnoise` fallback during
   Milestone E.

## Outputs

* tasks/t0046_reproduce_poleg_polsky_2016_exact/plan/plan.md
* tasks/t0046_reproduce_poleg_polsky_2016_exact/logs/steps/007_planning/step_log.md

## Issues

No blocking issues. One substantive risk flagged for the orchestrator: the luminance-noise driver
has never been exercised at non-zero SD in the shipped ModelDB code. Figures 6-8 reproduction may
need a seeded `rnoise` fallback if the authored driver misbehaves. Plan includes a pre-sweep
empirical-SD assertion to surface this early.
