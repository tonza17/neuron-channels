---
spec_version: "3"
task_id: "t0017_literature_survey_patch_clamp"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-20T00:05:00Z"
completed_at: "2026-04-20T00:10:00Z"
---
# Step 6: research-code

## Summary

Reviewed eight prior completed tasks to identify reusable assets, conventions, and guardrails for
this literature-survey task. Produced `research/research_code.md` with all seven mandatory sections
and eight Task Index entries. Key findings: no `assets/library/` exists project-wide, so there is
nothing to import; the paper and answer asset workflows from `[t0002]`, `[t0003]`, and `[t0007]`
supply the structural templates this task must follow; `[t0004]` defines the numerical tuning-curve
targets the surveyed papers must match; `[t0005]`'s mouse ooDSGC morphology guides species-matching
when prioritizing papers; `[t0002]`'s paywall-failure rate informs planning for this task's
`intervention/paywalled_papers.md`.

## Actions Taken

1. Enumerated completed tasks via `aggregate_tasks --status completed` to scope the review (eight
   completed tasks: t0001-t0007 plus t0014).
2. Inspected reusable code locations via Glob (`tasks/t00*/code/*.py`,
   `tasks/t00*/assets/library/**`, `tasks/t00*/assets/answer/**`) and confirmed no library assets
   exist and the project has no `aggregate_libraries` aggregator.
3. Drafted `research/research_code.md` organized by topic (paper workflow, answer format, tuning-
   curve targets, morphology, simulator stack, exclusion list, brainstorm traceability) with six
   actionable Reusable Code and Assets bullets plus prioritized recommendations.
4. Ran `flowmark` and `verify_research_code`. The first verification run flagged two RC-E006 errors
   for uncited `[t0006]` and `[t0014]` references; added Task Index entries for both and incremented
   `tasks_cited` from 6 to 8. Second run passed with zero errors and zero warnings.

## Outputs

* `tasks/t0017_literature_survey_patch_clamp/research/research_code.md`
* `tasks/t0017_literature_survey_patch_clamp/logs/steps/006_research-code/step_log.md`

## Issues

Two initial RC-E006 errors for `[t0006]` and `[t0014]` inline citations lacking Task Index entries
were resolved by adding the missing entries and updating `tasks_cited`. No outstanding issues.
