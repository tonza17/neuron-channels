---
spec_version: "3"
task_id: "t0041_electrotonic_length_collapse_t0034_t0035"
step_number: 10
step_name: "results"
status: "completed"
started_at: "2026-04-24T12:08:34Z"
completed_at: "2026-04-24T12:12:00Z"
---
## Summary

Wrote results files. Verdict is `collapse_rejected` on both primary (r=+0.42) and vector-sum
(r=-0.68, sign inverted) DSI; recommendation for t0033 is to retain the 2-D (raw length x raw
diameter) morphology parameterisation. results_summary.md and results_detailed.md cover the
methodology, the 3-plot overlay, the 10-row Examples section, and the full REQ-1 to REQ-6 coverage
traceback.

## Actions Taken

1. Wrote `results/results_summary.md` (Summary, Metrics, Verification).
2. Wrote `results/results_detailed.md` with all mandatory sections: Summary, Methodology (incl. 3
   embedded plots), Metrics, Examples (10 concrete operating-point rows with inputs and outputs),
   Analysis, Limitations, Files Created, Verification, and Task Requirement Coverage (REQ-1 through
   REQ-6 all Done).
3. Wrote `results/costs.json` (zero-cost) and `results/remote_machines_used.json` (empty array).
4. Reused `results/metrics.json` and `results/collapse_stats.json` produced in the implementation
   step.

## Outputs

* tasks/t0041_electrotonic_length_collapse_t0034_t0035/results/results_summary.md
* tasks/t0041_electrotonic_length_collapse_t0034_t0035/results/results_detailed.md
* tasks/t0041_electrotonic_length_collapse_t0034_t0035/results/costs.json
* tasks/t0041_electrotonic_length_collapse_t0034_t0035/results/remote_machines_used.json
* tasks/t0041_electrotonic_length_collapse_t0034_t0035/logs/steps/010_results/step_log.md

## Issues

No issues encountered.
