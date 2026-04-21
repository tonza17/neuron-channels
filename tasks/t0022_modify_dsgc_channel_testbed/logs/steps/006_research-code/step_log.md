---
spec_version: "3"
task_id: "t0022_modify_dsgc_channel_testbed"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-20T23:08:45Z"
completed_at: "2026-04-21T00:30:00Z"
---
## Summary

Produced `research/research_code.md` synthesizing prior-task code relevant to t0022: libraries
(`modeldb_189347_dsgc`, `tuning_curve_loss`, `tuning_curve_viz`, `modeldb_189347_dsgc_gabamod`), the
t0008 cell-build and driver entrypoints, and the t0020 scoring-glue patterns. Every reusable item is
labelled "import via library" or "copy into task" with file paths, function signatures, and
approximate line counts. Verificator passes with 0 errors and 0 warnings. Body 3035 words, 4
libraries (all relevant), 13 tasks reviewed / 12 cited.

## Actions Taken

1. Ran prestep for `research-code`, which created the `logs/steps/006_research-code/` folder.
2. Spawned a general-purpose subagent to enumerate prior-task code via the task aggregator and read
   each library's `details.json` + `description.md` directly. The asset-type aggregators
   (`aggregate_libraries`, `aggregate_answers`, `aggregate_datasets`) referenced by the spec are not
   present in this project's `arf/scripts/aggregators/`; the subagent documented the fallback inside
   the research file.
3. Subagent read `tasks/t0008_port_modeldb_189347/code/*` and
   `tasks/t0020_reproduce_modeldb_189347_dsgc_gabamod_swap/code/*` to extract exact function
   signatures, line numbers, and the driver / scoring glue skeletons that t0022 can copy.
4. Subagent wrote `research/research_code.md` with YAML frontmatter, all 7 mandatory sections, and
   additional task-specific sections capturing t0020 vs t0008 comparison anchors (DSI 0.316 / peak
   18.1 Hz for t0008 under rotation proxy; DSI 0.7838 / peak 14.85 Hz for t0020 under gabaMOD-swap
   proxy).
5. Subagent ran `flowmark` and `verify_research_code`. Final pass: 0 errors, 0 warnings.

## Outputs

* `tasks/t0022_modify_dsgc_channel_testbed/research/research_code.md` (3035 words, 4 libraries, 12
  task citations)
* `tasks/t0022_modify_dsgc_channel_testbed/logs/steps/006_research-code/step_log.md`

## Issues

Two notable findings surfaced for planning: (a) t0020 is the `modeldb_189347_dsgc_gabamod` sibling
using a 2-condition CSV schema, so its 208-line `score_envelope.py` is NOT reusable — t0008's
101-line scoring glue is the correct template; (b) t0020 contains a 55-line Windows NEURON bootstrap
(`_ensure_neuron_importable()`) not present in t0008 that should be adopted verbatim for the new
library.
