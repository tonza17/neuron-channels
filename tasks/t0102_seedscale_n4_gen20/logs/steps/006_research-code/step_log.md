---
spec_version: "3"
task_id: "t0102_seedscale_n4_gen20"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-11T16:04:13Z"
completed_at: "2026-05-11T16:13:30Z"
---
# Step 6: research-code

## Summary

Audited 10 prior tasks to identify the substrate code, libraries, and morphology generator t0102
will reuse. Key finding: the operative noise-replicate constant is `N_EVAL_SEEDS = 5` in t0099's own
`constants_morphology.py`, not `N_SEEDS = 20` from t0080's `constants.py` as the task description
implied. The recommended import-shadow strategy is to copy t0099's `constants_morphology.py`
verbatim into `tasks/t0102_seedscale_n4_gen20/code/` and edit two lines:
`N_EVAL_SEEDS: int = 5 -> 4` and `N_GEN: int = 8 -> 20`. All other substrate modules (~22 files,
~5,500 lines) must be copied into t0102/code/ because the cross-task import rule forbids importing
from another task's `code/` directory. Two registered libraries (t0090 morphology kit and t0092
morphology kit / t0024 NEURON build) are allowed imports. Verificator passes 0 errors / 0 warnings.

## Actions Taken

1. Loaded the research-code skill, the task description, and the existing research_papers /
   research_internet docs.
2. Read t0099's full code directory, t0080's NSGA-II driver and constants, t0083's extension driver,
   t0086's clustering / anchor analysis, t0090/t0092/t0093's morphology generator and library
   registration, and t0091's warm-start results.
3. Wrote `research/research_code.md` (594 lines, 4,667 words) with sections: Reusable Code and
   Assets, Reusable Libraries, Code Patterns and Conventions, Recommended Approach, Known Issues and
   Gotchas, References. Documented the exact list of files to copy from t0099 and the two-line edit
   needed in `constants_morphology.py`.
4. Ran Flowmark on the document, then the verificator.

## Outputs

* `research/research_code.md`
* Verificator log entries 012-013 (passed)
* Flowmark log entry 011

## Issues

The task description has two minor inaccuracies that will be corrected in `plan/plan.md`:

1. The driver file is `nsga2_driver.py` (orchestrated by `run_three_seeds.sh`), not `run_loop.py` as
   stated in the task description.
2. The constant to override is `N_EVAL_SEEDS` (t0099's own constants), not `N_SEEDS` (t0080's
   constant which is not imported by t0099's substrate).

These do not change the experiment design — only the file names and constant names cited in the
plan.
