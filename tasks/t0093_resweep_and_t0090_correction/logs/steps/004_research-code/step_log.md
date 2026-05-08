---
spec_version: "3"
task_id: "t0093_resweep_and_t0090_correction"
step_number: 4
step_name: "research-code"
status: "completed"
started_at: "2026-05-08T00:50:27Z"
completed_at: "2026-05-08T00:55:00Z"
---
# Step 4 -- Research code

## Summary

Spawned the `/research-code` subagent. Subagent surveyed 17 libraries (3 directly relevant: t0090
generator, t0092 fix shim, t0024 hand-coded Bed B reference), cited 7 prior tasks, and answered the
5 focused diagnostic-validation questions: t0090 verification.py pattern (worker-pickleable
ProcessPoolExecutor), t0092 fix shim API (drop-in compatible with t0090's generate_morphology),
corrections spec for `replace` action on library assets (`verify_corrections.py` validates the
JSON), library aggregator NOT present in this branch (same gap as t0092 reported), and visualisation
utilities (copy t0090's grid + dendrogram + Okabe-Ito helpers; add stability-flag colour map).
Verificator PASSES 0/0.

## Actions Taken

1. Ran prestep for `research-code`.
2. Spawned a general-purpose subagent with the `/research-code` skill prompt and the 5 focused
   questions.
3. Subagent walked t0090 / t0092 / t0024 / t0011 / t0080 code; identified the exact import path for
   `generate_fixed_morphology` and the exact corrections JSON shape.
4. Subagent wrote `research/research_code.md` (~600 lines, all 7 mandatory sections + 9 Key Findings
   subsections + 10 Recommendations).
5. Subagent ran `verify_research_code.py` -- PASSED 0/0.

## Outputs

* `tasks/t0093_resweep_and_t0090_correction/research/research_code.md`

## Issues

`aggregate_libraries.py` is still not present in this branch. Library survey was done by walking
`tasks/*/assets/library/*/details.json` directly. The corrections framework's `replace` action on
library assets is fully supported by `verify_corrections.py` and `arf/scripts/common/artifacts.py`,
so the correction overlay will be valid even without a dedicated library aggregator.
