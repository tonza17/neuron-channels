---
spec_version: "3"
task_id: "t0054_minimal_dsgc_ampa_nmda_scalar_gaba"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-04-28T04:36:59Z"
completed_at: "2026-04-28T04:42:00Z"
---
# Step 12 — Results

## Summary

Wrote results_summary.md, results_detailed.md (with 27 REQ verdicts and 3 example trial-level
pairs), costs.json, remote_machines_used.json. The detailed document embeds 6 headline figures (3
sweep-summary, 1 voltage trace, 2 EPSPs) and documents the quantitative findings across the 4 gNMDA
values plus the partial REQ-20 (epsp_decay returned null).

## Actions Taken

1. Ran prestep results.
2. Read metrics.json and derived_quantities.json; verified that all numbers in markdown match the
   JSON source.
3. Wrote results_summary.md with mandatory sections (Summary, Metrics, Verification).
4. Wrote results_detailed.md with all required sections (Summary, Methodology, Metrics,
   Visualisations, Examples, Analysis, Limitations, Files Created, Verification, Task Requirement
   Coverage).
5. Wrote costs.json (zero) and remote_machines_used.json (empty).

## Outputs

* `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/results_summary.md`
* `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/results_detailed.md`
* `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/costs.json`
* `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/remote_machines_used.json`
* `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/logs/steps/012_results/step_log.md`

## Issues

REQ-20 (epsp_decay_to_1e_ms) is Partial — the metric returned null because the EPSP at gNMDA > 0
doesn't decay below 1/e within the 1500-ms trial window. This is documented in the Limitations
section. REQ-27 (wall-clock budget) is Partial — the sweep took 4 h 19 min vs the planned ~75 min,
but does not affect correctness.
