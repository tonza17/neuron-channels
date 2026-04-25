---
spec_version: "3"
task_id: "t0048_voff_nmda1_dsi_test"
step_number: 13
step_name: "compare-literature"
status: "completed"
started_at: "2026-04-25T09:21:14Z"
completed_at: "2026-04-25T09:26:00Z"
---
## Summary

Wrote `results/compare_literature.md` (spec_version "1") comparing this task's Voff=1 DSI sweep
against Poleg-Polsky 2016 Fig 3F bottom claim (DSI approximately constant 0.30 across gNMDA). The
comparison table contains 10 numeric and qualitative data rows. Key finding: NMDA voltage-dependence
accounts for 60-70% of the deposited code's DSI-vs-gNMDA collapse; the residual ~0.20 gap to the
paper's flat 0.30 line must come from AMPA/GABA balance.

## Actions Taken

1. Drafted `compare_literature.md` with all five mandatory sections covering the H2 verdict,
   methodology differences, mechanistic interpretation, and limitations.
2. Identified concrete next-step recommendation for the broader project: switch from exptype=1 to
   exptype=2 (Voff_bipNMDA=1) as the canonical control choice for DSGC simulations, since the
   paper's biological NMDA is voltage-independent.

## Outputs

* tasks/t0048_voff_nmda1_dsi_test/results/compare_literature.md

## Issues

No issues encountered. The spec's minimum 2 data rows is exceeded (10 rows); minimum 150-word total
is exceeded.
