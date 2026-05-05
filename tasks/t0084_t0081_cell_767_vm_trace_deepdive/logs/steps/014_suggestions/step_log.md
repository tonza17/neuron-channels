---
spec_version: "3"
task_id: "t0084_t0081_cell_767_vm_trace_deepdive"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-05-05T16:38:45Z"
completed_at: "2026-05-05T16:55:00Z"
---
# Suggestions Step Log

## Summary

Generated six follow-up suggestions arising from the t0084 NaP-dominant attribution finding,
covering causal NaP-knockout testing, per-seed mechanism decomposition, multi-section spatial
heterogeneity, AIS-localised NaP placement, a knockout-based causal attribution metric, and
promotion of the t0084 pipeline into a reusable library asset. Deduplicated against the existing
uncovered suggestions (S-0081-01 multi-replicate confirmation, S-0081-04 param-space pruning,
S-0081-05 Bed A cross-bed validation, S-0081-06 HV recompute, and S-0002-06 NMDA gain ablation): the
t0084 suggestions extend rather than duplicate these.

## Actions Taken

1. Read t0084 task.json, plan, results_summary.md, and results_detailed.md to identify the
   actionable findings: (a) NaP-dominant 93% / 98.5% / 99.9% attribution across cells 767, 637, 762;
   (b) single-replicate failure to reproduce t0081's 5-seed mean DSI; (c) single-section recording
   at terminal_dends[0]; (d) correlative-not-causal nature of the integrated-current metric.
2. Ran `aggregate_suggestions --uncovered --detail short` and `aggregate_tasks --detail short` to
   list existing uncovered suggestions and existing tasks, and identified the t0081-derived
   suggestions (S-0081-01, S-0081-04, S-0081-05, S-0081-06) that scope adjacent but distinct
   experiments.
3. Drafted six candidate suggestions: NaP density knockout sweep (S-0084-01); per-seed mechanism
   decomposition (S-0084-02); multi-section dendritic recording (S-0084-03); AIS-localised NaP
   placement test (S-0084-04); channel-knockout DSI causal-attribution variant (S-0084-05);
   library-asset promotion of the t0084 pipeline (S-0084-06).
4. Wrote `results/suggestions.json` (spec_version "1") with six suggestions; ran
   `verify_suggestions` and shortened titles / descriptions until all SG-W warnings cleared. Final
   verifier outcome: 0 errors, 0 warnings.

## Outputs

* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/suggestions.json` (6 suggestions)

## Issues

* No issues encountered. Initial draft had several SG-W001 (title > 120 chars) and SG-W003
  (description > 1000 chars) warnings; resolved by tightening wording.
