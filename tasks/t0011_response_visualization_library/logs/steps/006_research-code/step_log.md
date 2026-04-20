---
spec_version: "3"
task_id: "t0011_response_visualization_library"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-20T15:10:03Z"
completed_at: "2026-04-20T15:30:00Z"
---
# Research Code

## Summary

Surveyed 17 completed tasks and 2 registered libraries. Identified `tuning_curve_loss` [t0012] as
the canonical CSV loader to import, confirmed t0004/t0008 CSV schemas, flagged the absence of any
spike-time data asset, and wrote a 7-section research_code.md with explicit import-vs-copy labels
and a task index citing t0004, t0008, t0009, t0012.

## Actions Taken

1. Ran `aggregate_tasks --status completed` to enumerate 17 completed tasks and review their task
   types and outputs.
2. Walked `tasks/*/assets/library/*/details.json` with Glob (no `aggregate_libraries.py` exists) to
   discover `tuning_curve_loss` and `modeldb_189347_dsgc`.
3. Read `tuning_curve_loss.loader` to confirm its three supported schemas match this task's inputs.
4. Wrote `research/research_code.md` with 7 mandatory sections and correct v1 frontmatter fields.
5. Ran `flowmark` to normalize markdown; ran `verify_research_code` — clean pass with no errors or
   warnings.

## Outputs

* `tasks/t0011_response_visualization_library/research/research_code.md`

## Issues

No issues encountered.
