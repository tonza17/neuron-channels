---
spec_version: "3"
task_id: "t0110_relaxed_cohort_factor_analysis"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-18T18:32:00Z"
completed_at: "2026-05-18T18:33:00Z"
---

# Step 6: research-code

## Summary

Reviewed t0108 code/factor_analysis.py to identify the varimax rotation routine and reuse it via absolute import. Confirmed the t0108 result file shape so we can load it for the comparison plot.

## Actions Taken

* Read tasks/t0108_*/code/factor_analysis.py for the varimax routine.
* Read tasks/t0108_*/results/data/factor_analysis.json schema.

## Outputs

* varimax_rotation reusable via import; factor_analysis.json schema matches our needs.

## Issues

* None.
