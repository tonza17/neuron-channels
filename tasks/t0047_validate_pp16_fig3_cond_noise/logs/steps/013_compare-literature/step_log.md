---
spec_version: "3"
task_id: "t0047_validate_pp16_fig3_cond_noise"
step_number: 13
step_name: "compare-literature"
status: "completed"
started_at: "2026-04-24T23:50:06Z"
completed_at: "2026-04-24T23:55:30Z"
---
## Summary

Wrote `results/compare_literature.md` (spec_version "1") comparing this task's reproduction against
Poleg-Polsky and Diamond 2016 Fig 3A-F simulation targets and Fig 6-7 noise qualitative claims. The
comparison table contains 12 numeric and qualitative data rows; the key finding is that the
deposited control's `Voff_bipNMDA = 0` (voltage-dependent NMDA) is the most plausible mechanistic
source of the DSI-vs-gNMDA collapse, and the `Voff_bipNMDA = 1` re-test (paper's biologically-stated
voltage-independent NMDA) is the highest-value next test.

## Actions Taken

1. Drafted `results/compare_literature.md` with all five mandatory sections (`## Summary`,
   `## Comparison Table`, `## Methodology Differences`, `## Analysis`, `## Limitations`).
2. Populated the comparison table with one row per quantitative paper claim (Fig 3A-C conductances;
   Fig 3F bottom DSI sweep at three gNMDA values) plus three qualitative rows for the noise-sweep
   claims.
3. Identified the diagnostic mechanism: the deposited control is voltage-dependent NMDA; paper's
   biological NMDA is voltage-independent. This is the highest-value next test for a follow-up task.

## Outputs

* tasks/t0047_validate_pp16_fig3_cond_noise/results/compare_literature.md

## Issues

No issues encountered. The spec's minimum 2 data rows is exceeded (12 rows); minimum 150-word total
is exceeded.
