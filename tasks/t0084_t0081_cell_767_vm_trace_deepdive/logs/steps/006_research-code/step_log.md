---
spec_version: "3"
task_id: "t0084_t0081_cell_767_vm_trace_deepdive"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-05T15:46:21Z"
completed_at: "2026-05-05T15:55:00Z"
---
## Summary

Reviewed the t0080 v3 dendritic-spike substrate library and t0081 NSGA-II evaluation harness to
identify all entry points, recordable NEURON variables, and parameter data layout needed for the
24-simulation deep-dive. Confirmed cell 767/637/762 parameter vectors, Exp2NMDA `g` variable
semantics, Nav1.6 and NaP `i` RANGE variables, and sequential-mode recording constraint.

## Actions Taken

1. Examined 20 registered library assets; identified `de_rosenroll_2026_dsgc_ais_dendritic_spike`
   (t0080) as the single relevant library.
2. Read `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/` — trial_driver.py, constants.py,
   apply_params.py, build_cell_ais.py, recorder.py, trial_helpers.py, and all .mod files to
   determine RANGE variables for recording.
3. Read `tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json` and confirmed 54-d
   parameter vectors for cells 767, 637, 762. Confirmed pareto_front.json lists all three.
4. Inspected `Exp2NMDA.mod` in t0024 library sources; identified `g` (uS) as the correct variable to
   record (Mg-block-modulated conductance, not `gmax`).
5. Verified t0083 has no code directory yet; confirmed no file-isolation risk.
6. Wrote `research/research_code.md` with all 7 mandatory sections and 2 task citations.
7. Ran `verify_research_code t0084_t0081_cell_767_vm_trace_deepdive` — PASSED, 0 errors, 0
   warnings.

## Outputs

* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/research/research_code.md` — code research with
  library landscape, key findings (cell data layout, entry points, NEURON variables), reusable
  code/assets, lessons learned, and recommendations.

## Issues

No issues encountered. Budget gate skipped (all task types with external costs have $0 spend for
local CPU task; budget is $11.87 remaining with no thresholds triggered).
