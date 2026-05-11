---
spec_version: "3"
task_id: "t0100_fix_t0099_morph_charts"
step_number: 6
step_name: "research-code"
status: "skipped"
started_at: null
completed_at: null
---

## Summary

Skipped: the relevant t0099, t0091, and t0098 code references are already enumerated inline in
the task_description.md and confirmed in the diagnosis grep at task creation. No further
prior-code research is required; the implementation copies one Python file and changes one
slice.

## Actions Taken

1. Confirmed t0099/code/build_morphology_charts.py is the only source file to copy.
2. Confirmed t0091/code/{biological_priors.py:31, anchor_tracking.py:160} establishes the
   correct 68-d slice convention (`MORPH_OFFSET = 54`).
3. Confirmed t0098/code/build_charts.py reads `cell["morphology_vector_14d"]` directly and
   therefore was not affected by the bug.

## Outputs

* None (skipped step).

## Issues

No issues encountered.
