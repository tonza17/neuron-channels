---
spec_version: "3"
task_id: "t0121_5seed_substrate_rate_canonical_report"
step_number: 10
step_name: "results"
status: "completed"
started_at: "2026-05-24T02:02:39Z"
completed_at: "2026-05-24T02:06:00Z"
---
# Step 10: Results

## Summary

Wrote results_summary.md, results_detailed.md, metrics.json (empty `{}` -- no registered project
metrics apply to a write-up task), costs.json (zero), remote_machines_used.json (`[]`). The detailed
file documents the conventions adopted, all per-seed numbers, the bootstrap CI analysis,
convention-drift reconciliation, and the 16-item Task Requirement Coverage table.

## Actions Taken

1. Wrote results/metrics.json as `{}` and documented the empty-metrics rationale in
   results_detailed.md.
2. Wrote results/costs.json as zero-cost.
3. Wrote results/remote_machines_used.json as `[]`.
4. Wrote results/results_summary.md with Summary / Metrics / Verification sections.
5. Wrote results/results_detailed.md with all mandatory sections plus Analysis (covering plan
   assumption check + convention drift + seed-77/2247 underyield analysis) and the 16-item Task
   Requirement Coverage table.
6. Embedded all 3 PNGs via Markdown image syntax in results_detailed.md Visualizations section.

## Outputs

* `tasks/t0121_5seed_substrate_rate_canonical_report/results/results_summary.md`
* `tasks/t0121_5seed_substrate_rate_canonical_report/results/results_detailed.md`
* `tasks/t0121_5seed_substrate_rate_canonical_report/results/metrics.json` (= `{}`)
* `tasks/t0121_5seed_substrate_rate_canonical_report/results/costs.json` (zero)
* `tasks/t0121_5seed_substrate_rate_canonical_report/results/remote_machines_used.json` (`[]`)
* `tasks/t0121_5seed_substrate_rate_canonical_report/logs/steps/010_results/step_log.md`

## Metrics Cross-Check

The numbers in results_summary.md / results_detailed.md come from the 5 CSV / 1 parquet output files
in results/data/. No registered project metrics from meta/metrics/ apply to a pure write-up.

## Issues

No issues encountered.
