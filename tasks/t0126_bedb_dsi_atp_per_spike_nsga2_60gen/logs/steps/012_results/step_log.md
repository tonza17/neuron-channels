---
spec_version: "3"
task_id: "t0126_bedb_dsi_atp_per_spike_nsga2_60gen"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-25T20:16:19Z"
completed_at: "2026-05-25T20:55:00Z"
---
# Step 12 -- Results

## Summary

Wrote `results/results_summary.md` and `results/results_detailed.md` from the t0126 60-gen NSGA-II
run data (final HV 1.999e10, +37.6% vs t0124; bootstrap r(DSI, ATP) = +0.980 [0.972, 1.000] on the
6-cell Pareto front; verdict INSUFFICIENT_EVIDENCE per S-0124-01 due to n=6 < 20). Both files were
Flowmark-normalised and then validated against `verify_task_results` and `verify_task_metrics` --
both PASS.

## Actions Taken

1. Read the task scope (`task.json`, `task_description.md`, `plan/plan.md` REQ-1 through REQ-29),
   the results data (`metrics.json`, `pareto_front_seed8929.json`, `comparator_report.json`,
   `hv_trajectory_seed8929.json`, `costs.json`, `remote_machines_used.json`), the predictions asset
   (`details.json`), the answer asset (`short_answer.md`), and the smoke-gate output
   (`logs/steps/009_implementation/smoke_gate.json`).
2. Inspected `results/data/all_evaluations_seed8929.json` (5,760 evaluations) via `uv run python` to
   find diverse Examples cases: silenced cells (gen 1), earliest DSI=1.0 cell (gen 34), boundary
   DSI~0.5 cells, cheapest ATP, and gen-60 final-pop samples.
3. Wrote `results/results_summary.md` (frontmatter + Summary + Metrics + Verification; 6 bullet
   points in Metrics with specific numbers; 8 verificator entries).
4. Wrote `results/results_detailed.md` (frontmatter `spec_version: "2"`; Summary, Methodology,
   Examples with 12 concrete instances, Metrics Tables with per-cell + aggregate + distribution
   tables, Comparison vs Baselines for t0124 / t0122 / t0123 / Carter-Bean / Howarth / Niven,
   Visualizations embedding all 8 PNGs, Analysis/Discussion answering the three primary questions,
   Limitations, Verification, Files Created, Next Steps/Suggestions, Task Requirement Coverage with
   all 29 REQ items answered).
5. Ran `uv run flowmark --inplace --nobackup` on both files.
6. Ran `verify_task_results` and `verify_task_metrics` via `run_with_logs.py` and confirmed PASS.
7. Wrote this step log.

## Outputs

* `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/results_summary.md`
* `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/results_detailed.md`
* `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/logs/steps/012_results/step_log.md` (this file)

## Issues

No issues encountered. One REQ marked `Partial` (REQ-29) because the Pareto front converged to n=6
cells (below the plan-mandated n>=20 minimum for the S-0124-01 decision rule). This is a
quantitative result with a documented limitation, not a missing deliverable; the multi-seed
follow-up (S-t0126-multi-seed) is the principled fix and is pre-flagged in `results_detailed.md`
`## Next Steps / Suggestions`.
