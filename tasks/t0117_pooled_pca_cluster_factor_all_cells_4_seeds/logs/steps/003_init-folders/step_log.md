---
spec_version: "3"
task_id: "t0117_pooled_pca_cluster_factor_all_cells_4_seeds"
step_number: 3
step_name: "init-folders"
status: "completed"
started_at: "2026-05-22T12:02:36Z"
completed_at: "2026-05-22T12:02:50Z"
---
# Step 3: init-folders

## Summary

Created the mandatory task folder structure (12 directories with `.gitkeep` placeholders plus
`__init__.py` files for the task package and the `code/` subpackage) by invoking
`arf.scripts.utils.init_task_folders`. The asset subdirectory `assets/answer/` was created based on
`task.json` `expected_assets`. The `--step-log-dir` flag rejected the absolute path on Windows, so
the `folders_created.txt` manifest was written manually with the same content the script would have
produced.

## Actions Taken

1. Ran `prestep` for `init-folders`.
2. Ran `arf.scripts.utils.init_task_folders t0117_pooled_pca_cluster_factor_all_cells_4_seeds`
   wrapped in `run_with_logs`. The script created 12 directories with `.gitkeep` files plus the
   task-package `__init__.py` and `code/__init__.py`. The `--step-log-dir` flag failed with an
   absolute path, so `folders_created.txt` was not auto-written.
3. Wrote `logs/steps/003_init-folders/folders_created.txt` manually mirroring the script's stdout.

## Outputs

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/{plan,research,results,results/images,corrections,intervention,code,logs/commands,logs/searches,logs/sessions,logs/steps,assets/answer}/`
  with `.gitkeep` placeholders
* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/__init__.py`
* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/__init__.py`
* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/logs/steps/003_init-folders/folders_created.txt`

## Issues

`init_task_folders --step-log-dir <absolute path>` rejects absolute paths on Windows. Worked around
by writing `folders_created.txt` manually. Worth surfacing as a minor ARF-infra portability issue
for the init script.
