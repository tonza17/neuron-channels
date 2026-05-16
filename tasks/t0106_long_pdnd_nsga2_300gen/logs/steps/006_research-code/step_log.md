---
spec_version: "3"
task_id: "t0106_long_pdnd_nsga2_300gen"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-16T23:00:46Z"
completed_at: "2026-05-16T23:10:00Z"
---
# Step 6 — research-code

## Summary

Audited the t0104 code base and ancestor lineage (t0099, t0102, t0091, t0080, t0092, t0093, t0024)
to pinpoint exact patch sites for the t0106 evaluator fork. Found that the t0104 evaluator already
parameterises `n_directions` and that `_vector_sum_dsi` reduces mathematically to ratio DSI at two
antipodal directions, so the 2-direction switch is a 4-constant patch rather than an evaluator
rewrite. Identified that the "per-generation worker pool restart" referenced by the task description
does not yet exist in the lineage and must be implemented from scratch. Cataloged all 13 t0080 MOD
files needed for Vast.ai SCP and specified a pymoo Termination + dill checkpointing skeleton plus a
five-step Windows local smoke-test plan. Wrote research_code.md with 11 task citations and the
verificator passes with zero errors and zero warnings.

## Actions Taken

1. Read task.json, task_description.md, research/research_papers.md, and research/research_internet
   for the t0106 task to extract objectives, hyperparameter changes, operator-stop requirements, and
   budget constraints.
2. Audited tasks/t0104_*/code/constants_electrophys.py, constants_morphology.py, constants.py,
   evaluator.py, nsga2_driver.py, paths.py, random_init.py, hv_plateau_watchdog.py, smoke_gate.py,
   trial_helpers.py, generator_wrapper.py, and bootstrap.py for exact line numbers of patch sites.
   Cross-checked the t0102 and t0099 drivers for the supposed per-generation worker restart pattern
   (does not exist; must be implemented).
3. Listed t0080 mods/ contents (13 .mod files) and resolved their canonical Linux compile path via
   t0104 paths.py. Enumerated 18 project libraries via direct details.json walk; identified t0024
   `de_rosenroll_2026_dsgc` as the only transitively-used library.
4. Wrote tasks/t0106_*/research/research_code.md with all 7 mandatory sections plus MOD-file list,
   pymoo Callback + dill skeleton, smoke-test plan, and unified-diff sketches for the four
   highest-impact patches. Ran flowmark, ran verify_research_code (initial 12 errors, fixed by
   converting Task Index entries to bold-field syntax and adding the missing t0091 entry), re-ran
   flowmark and verificator — PASSED with zero errors and zero warnings.

## Outputs

* `tasks/t0106_long_pdnd_nsga2_300gen/research/research_code.md` — code research document, 11
  tasks cited, all 7 mandatory sections plus 3 additional sections (MOD files, pymoo skeleton,
  smoke-test plan).

## Issues

* The `aggregate_libraries.py` aggregator referenced by the research-code SKILL is not present in
  this repo. Libraries were enumerated by direct filesystem walk of
  `tasks/*/assets/library/*/details.json`. The Library Landscape section documents this fallback.
* Initial verificator run produced 12 errors (Task Index entries used non-bold `Task ID:` field
  syntax; the verificator requires `* **Task ID**: value`). Fixed by reformatting all 11 entries
  with bold field names. Also added a missing t0091 Task Index entry to match the inline citation in
  the Lessons Learned section.
