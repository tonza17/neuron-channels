---
spec_version: "3"
task_id: "t0124_bedb_dsi_atp_per_spike_nsga2"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-25T02:23:38Z"
completed_at: "2026-05-25T02:40:00Z"
---
# Step 12: results

## Summary

Wrote results_summary.md and results_detailed.md from the implementation outputs. Both files
synthesize: 5-cell Pareto front, best legit DSI 0.882, min ATP 2.11e6, Carter-Bean smoke-gate PASS
at 6.137e8 ATP/AP/cm (within first-principles [3e7, 3e9] band), bootstrap r(DSI, ATP) = +0.806.
results_detailed.md includes 10 concrete examples per the experiment-task standard, full metrics
tables, all 5 charts embedded, and the Task Requirement Coverage section closing out the 26 REQs (25
done + 1 partial REQ-15 on the 9/60 gen truncation).

## Actions Taken

1. Cross-checked metrics.json (4 variants) against the implementation subagent's reported numbers
   — all match exactly.
2. Read pareto_front_seed6650.json: 5 cells, F = (-DSI, +ATP); cell 1 is best_legit at DSI 0.882,
   cell 4 is min-ATP at DSI 0.
3. Read comparator_report.json: all 5 Pareto cells in Carter-Bean PASS band; Howarth signalling-
   budget fractions returned NaN (whole-tissue anchor not available from t0124's evaluator).
4. Wrote results_summary.md with the 3 mandatory sections (Summary, Metrics, Verification).
5. Wrote results_detailed.md with all mandatory sections plus the experiment-task-required
   `## Examples` section (10 concrete instances) and the `## Task Requirement Coverage` section (26
   REQs accounted for).
6. Embedded all 5 charts with descriptive captions per the task-documents rule.
7. Numbers in markdown match metrics.json exactly — no rounding, no "approximately".

## Outputs

* tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/results_summary.md
* tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/results_detailed.md
* tasks/t0124_bedb_dsi_atp_per_spike_nsga2/logs/steps/012_results/step_log.md

## Issues

REQ-15 marked partial in `## Task Requirement Coverage` — 9/60 generations completed. The Howarth
signalling-ATP comparison is incomplete (NaN cells) because the whole-tissue ATP turnover anchor
isn't part of the t0124 evaluator. Both limitations are surfaced prominently in the
Analysis/Discussion and Limitations sections.
