---
spec_version: "3"
task_id: "t0086_robustness_cluster_bio_comparison"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-06T13:10:15Z"
completed_at: "2026-05-06T13:30:00Z"
---
# Step 6 -- Research Code

## Summary

Reviewed code from the six dependency tasks (t0024 / t0078 / t0080 / t0081 / t0083 / t0084) to
identify reusable entry points for t0086's three-phase pipeline. Wrote `research/research_code.md`
covering the v3 substrate library `de_rosenroll_2026_dsgc_ais_dendritic_spike` (single relevant
library), the canonical `evaluate_parameter_vector` per-cell evaluator, the SEED_BASE outer-seed
monkey-patch strategy for 5 replications, the cluster analysis stack (sklearn + UMAP-learn), and the
REQ-X cost-watchdog rate-fix pattern needed to avoid t0083's 16% overrun. Verificator passed with 0
errors.

## Actions Taken

1. Ran prestep research-code.
2. Read `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_driver.py`, `nsga2_loop.py`,
   `constants.py` to identify the per-cell evaluator entry point and the SEED_BASE / HOURLY_RATE_USD
   module-level constants.
3. Read `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/code/run_loop.py`,
   `tasks/t0083_*/results/data/{pareto_front.json, all_evaluations.json}` to understand the
   continuation pattern and the source data for joint-pass cell selection.
4. Read `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/` to understand the per-cell eval
   patterns and the answer-asset writer.
5. Wrote `research/research_code.md` with the 7 mandatory sections (Task Objective, Library
   Landscape, Architecture Overview, Key Findings, Reusable Code and Assets, Lessons Learned,
   Recommendations for This Task, Task Index for 6 dependency tasks).
6. Ran flowmark and verify_research_code; 0 errors after fixing initial frontmatter omission and
   Task Index field-bolding issues.

## Outputs

* `tasks/t0086_robustness_cluster_bio_comparison/research/research_code.md`
* `tasks/t0086_robustness_cluster_bio_comparison/logs/steps/006_research-code/step_log.md`

## Issues

The first two verification passes failed: the initial draft was missing YAML frontmatter (RC-E002)
and used unbold field labels in Task Index (RC-E007 x6). Both fixed in place. Initial draft also
cited [t0017] / [t0018] / [t0019] literature surveys without Task Index entries (RC-E006); removed
those citations since the corresponding biological priors come from the primary cited papers, not
from the survey tasks. Final pass: 0 errors.
