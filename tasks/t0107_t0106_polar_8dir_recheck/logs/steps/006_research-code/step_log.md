---
spec_version: "3"
task_id: "t0107_t0106_polar_8dir_recheck"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-18T02:38:29Z"
completed_at: "2026-05-18T02:39:00Z"
---
# Step 6: research-code

## Summary

Confirmed the t0106 evaluator can be reused with only a minimal patch (add per-direction firing
rates to the return value). Identified the 8 source files to copy verbatim and 3 new files to write
(sample_top10, eval_polar, plot_polar). The full procedure runs locally in ~90 s.

## Actions Taken

1. Audited `tasks/t0106_long_pdnd_nsga2_300gen/code/evaluator.py`: `evaluate_68d_vector` already
   supports a configurable `n_directions` argument and reads `ANGLES_8DIR_DEG` from the constants
   module, so the 8-direction protocol needs no algorithm patch.
2. Noted the only schema gap: per-direction firing rates are computed internally but not exposed.
   Added a minor patch to the local copy that adds `per_direction_rates_hz` to the return dataclass.
3. Wrote the migration plan in `research/research_code.md` listing the 8 files to copy verbatim and
   the 3 t0107-specific scripts to author.

## Outputs

* `research/research_code.md`

## Issues

No issues.
