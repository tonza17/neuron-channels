---
spec_version: "3"
task_id: "t0055_nmda_mg_block_dsi_recovery"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-04-28T13:43:16Z"
completed_at: "2026-04-28T13:46:00Z"
---
## Summary

Composed `results_summary.md`, `results_detailed.md`, `costs.json`, and `remote_machines_used.json`.
Headline finding: Mg-block NMDA recovers vector-sum DSI to 0.7464 (9× recovery vs t0054's 0.082) at
every gNMDA value, but peak rate stays at the baseline 0.667 Hz because the scalar gabaMOD
inhibition prevents the cell from depolarising above the Mg-unblock threshold. S-0054-01 pass
criterion is partial: DSI half PASS, peak-Hz half FAIL. 19 of 20 REQ items Done; REQ-20 (EPSP decay
tau) is Not done for the same inherited-protocol reason as in t0054 (window too short + HH active
during measurement).

## Actions Taken

1. Read `metrics.json` and `derived_quantities.json` produced by the implementation step.
2. Wrote `results/results_summary.md` with 2-3 sentence summary, ≥3 bullet metrics, and
   verification block.
3. Wrote `results/results_detailed.md` covering all 11 mandatory sections (Summary, Methodology,
   Metrics Tables, Comparison vs Baselines, Visualizations, Analysis, Limitations, Verification,
   Files Created, Examples, Task Requirement Coverage).
4. Wrote `results/costs.json` (`{"total_cost_usd": 0, "breakdown": {}}`) and
   `results/remote_machines_used.json` (`[]`) — local CPU only, $0 cost.

## Outputs

* `tasks/t0055_nmda_mg_block_dsi_recovery/results/results_summary.md`
* `tasks/t0055_nmda_mg_block_dsi_recovery/results/results_detailed.md`
* `tasks/t0055_nmda_mg_block_dsi_recovery/results/costs.json`
* `tasks/t0055_nmda_mg_block_dsi_recovery/results/remote_machines_used.json`
* `tasks/t0055_nmda_mg_block_dsi_recovery/logs/steps/012_results/step_log.md`

## Issues

The user-flagged HH-during-EPSP protocol issue is documented prominently in the Limitations section
of `results_detailed.md` and acknowledged in the Task Requirement Coverage row for REQ-20. The
underlying fix is not applied in t0055 — it lives as a project-wide standing issue captured in the
feedback memory and tracked via follow-up suggestions to be generated in step 14.
