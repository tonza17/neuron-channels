---
spec_version: "3"
task_id: "t0033_plan_dsgc_morphology_channel_optimisation"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-22T14:32:06Z"
completed_at: "2026-04-22T14:48:00Z"
---
## Summary

Spawned a research-code subagent that inventoried the prior-task code, library assets, and Vast.ai
infrastructure that this plan will build on. The synthesis enumerates the 16 lumped-HHst gbar
parameters of the t0024 backbone, identifies the effective top-10 VGC list from t0019 priors plus
the t0022 channel-density table, anchors per-simulation wall-time on the t0026 baselines, and
documents the Vast.ai tier filters and reliability thresholds that bound the cost model.

## Actions Taken

1. Spawned a general-purpose subagent with the `/research-code` skill instructions and a focused
   prompt covering t0022 + t0024 channel inventories, t0019 top-10 VGC list, t0026 wall-time
   anchors, t0012 DSI scoring library, and Vast.ai infrastructure (vast_machines.py, remote machines
   spec).
2. Subagent ran the necessary aggregators (libraries, answers, datasets) wrapped in
   `run_with_logs.py`, read the relevant code and answer assets, and synthesised them into
   `research/research_code.md`.
3. Subagent ran `flowmark --inplace --nobackup` on the output and `verify_research_code.py` wrapped
   in `run_with_logs.py`. Verificator returned 0 errors, 0 warnings.

## Outputs

* `tasks/t0033_plan_dsgc_morphology_channel_optimisation/research/research_code.md`
* `tasks/t0033_plan_dsgc_morphology_channel_optimisation/logs/commands/...` (run_with_logs entries
  produced by the subagent)
* `tasks/t0033_plan_dsgc_morphology_channel_optimisation/logs/steps/006_research-code/step_log.md`
  (this file)

## Issues

The t0022 testbed AIS_PROXIMAL, AIS_DISTAL, and THIN_AXON regions are presently empty hooks awaiting
channel-swap work; the priors carried forward (Nav1.1, Nav1.6, Kv1.2, Kv3) come from the t0022
internet-research notes rather than instantiated MOD insertions. The plan's parameter count must
therefore distinguish "currently instantiated" vs "future channel-axis" parameters and the
implementation step must explicitly state both.
