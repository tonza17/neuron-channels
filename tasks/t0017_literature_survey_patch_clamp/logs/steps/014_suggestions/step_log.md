---
spec_version: "3"
task_id: "t0017_literature_survey_patch_clamp"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-04-20T11:06:50Z"
completed_at: "2026-04-20T11:07:30Z"
---
## Summary

Wrote four follow-up suggestions S-0017-01 through S-0017-04 covering manual PDF retrieval,
follow-up survey coverage, downstream DSGC model build implementation, and category registration
hygiene.

## Actions Taken

1. Replaced the placeholder `results/suggestions.json` with four populated suggestions following the
   spec v2 schema (id, title, description, kind, priority, source_task, source_paper, categories,
   status, date_added).
2. S-0017-01 (high): manual PDF retrieval and numerical-claim verification for the 5 paywalled
   papers.
3. S-0017-02 (medium): extend the survey to DSGC-specific dynamic-clamp, Ih/HCN, AIS, and
   model-fitting sub-areas.
4. S-0017-03 (high): implement AIS compartment, NMDARs, and simulated voltage-clamp block in the
   downstream DSGC model build task with the 7-point specification as the design target.
5. S-0017-04 (low): verify that the six category slugs used by this task's assets are registered in
   `meta/categories/`.

## Outputs

* `results/suggestions.json` with four populated suggestions.

## Issues

None.
