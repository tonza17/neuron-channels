---
spec_version: "3"
task_id: "t0125_t0123_cluster_factor_mi_atp"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-24T23:32:33Z"
completed_at: "2026-05-24T23:45:00Z"
---
## Summary

Spawned the `/research-code` skill subagent which inventoried the cluster + factor analysis pipeline
across t0108 / t0116 / t0117 (~2,374 lines of reusable code), the t0109 morphology gallery rendering
pattern, the t0123 predictions schema, and three prior answer assets on cluster structure (t0086,
t0088, t0117). Verificator passed with zero errors and zero warnings.

## Actions Taken

1. Ran prestep for research-code.
2. Spawned a subagent to execute `/research-code` from `arf/skills/research-code/SKILL.md`. Passed
   pointers to the five critical source code locations: t0108, t0116, t0117, t0109, t0123.
3. Subagent produced `research/research_code.md` (662 lines, 9 mandatory sections + a 10-entry task
   index) following `research_code_specification.md`.
4. Subagent ran the verificator which returned "PASSED - no errors or warnings".

## Outputs

* `tasks/t0125_t0123_cluster_factor_mi_atp/research/research_code.md`

## Issues

* The `aggregate_libraries`, `aggregate_models`, `aggregate_datasets`, and `aggregate_answers`
  aggregators referenced in the orchestrator prompt do not exist in this fork (only 8 generic
  aggregators are implemented). Subagent fell back to direct filesystem walks of
  `tasks/*/assets/{library,answer}/` and documented this fallback in the Library Landscape section.
  Out of scope to fix here (would be an arf/ infrastructure change).
* Key takeaway for implementation: import the two morphology libraries from t0090 and t0092
  directly; copy t0117's pipeline modules into `code/` with namespace updates; rewrite the loader
  for the single-seed jsonl.gz source with the dual full / spiking cohort; rename
  cluster-seed-purity to cluster-group-purity (NMI vs MI / ATP quartile groups instead of vs seed);
  change within-cluster representative ranking from DSI*PD to bits-per-ATP; add four new modules
  (effect_sizes, group_comparison, corner_heatmap, atp_compartment_shares).
