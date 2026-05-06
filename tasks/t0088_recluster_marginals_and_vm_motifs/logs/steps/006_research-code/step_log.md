---
spec_version: "3"
task_id: "t0088_recluster_marginals_and_vm_motifs"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-06T19:47:40Z"
completed_at: "2026-05-06T19:55:00Z"
---
# Step 6 -- Research Code

## Summary

Inventoried code from t0086 (clustering core, biological scoring) and t0084 (Vm-trace deep-dive
recording, attribution metric, plotting) for re-use in this task; verified that all 13 target cell
parameter vectors live in t0083's `all_evaluations.json`; produced `research/research_code.md`
documenting the recommended file copy + import-rebinding plan plus run order across the three
phases.

## Actions Taken

1. Read `tasks/t0086_robustness_cluster_bio_comparison/code/cluster_analysis.py` (359 LOC),
   `biological_priors.py` (179 LOC), `biological_scorecard.py` (201 LOC), and `paths.py` to
   characterise the clustering + scoring infrastructure for re-use.
2. Read `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/run_deepdive.py` (439 LOC),
   `attribution_metric.py` (155 LOC), `plot_figures.py` (230 LOC), `constants.py`, and `paths.py` to
   characterise the Vm-trace deep-dive recording pattern.
3. Confirmed availability of all 13 target cells' parameter vectors in
   `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json` via a one-liner
   load + intersection check. None require fallback loading from t0081's `all_evaluations.json`.
4. Wrote `research/research_code.md` with all 8 mandatory sections (Task Objective, Library
   Landscape, Architecture Overview, Reusable Code and Assets, Methodology Review, Key Findings,
   Lessons Learned, Recommendations for This Task, Task Index, References).
5. Verified `verify_research_code` passes with 0 errors.

## Outputs

* `tasks/t0088_recluster_marginals_and_vm_motifs/research/research_code.md`

## Issues

No issues encountered.
