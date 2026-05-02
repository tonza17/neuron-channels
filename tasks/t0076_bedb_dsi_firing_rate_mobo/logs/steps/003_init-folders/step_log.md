---
spec_version: "3"
task_id: "t0076_bedb_dsi_firing_rate_mobo"
step_number: 3
step_name: "init-folders"
status: "completed"
started_at: "2026-05-02T20:31:45Z"
completed_at: "2026-05-02T20:32:00Z"
---
## Summary

Created the standard task folder layout (12 mandatory subdirectories with .gitkeep files plus
**init**.py for the task package) using init_task_folders.

## Actions Taken

1. Ran `prestep init-folders`.
2. Ran `init_task_folders` (wrapped in run_with_logs).
3. Wrote `folders_created.txt` based on the script's stdout.

## Outputs

* `assets/`, `code/`, `corrections/`, `intervention/`, `logs/{commands,searches,sessions,steps}/`,
  `plan/`, `research/`, `results/{,images/}` directories with .gitkeep
* `__init__.py`, `code/__init__.py`
* `logs/steps/003_init-folders/folders_created.txt`

## Issues

None.
