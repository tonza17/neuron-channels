# Plan: Brainstorm Session 24

## Objective

Turn the researcher's rd1 vs WT electrophysiology observations (`SomeResults.pdf`) into one
standalone modelling task, and record the session.

## Approach

1. Aggregate project state and read recent results (t0120-t0129).
2. Read the researcher's figures and extract approximate calibration targets.
3. Discuss and agree the task design with the researcher.
4. Create this brainstorm task folder, then create the child task via `/create-task`.
5. Record the session in step logs and the session transcript.

## Cost Estimation

This task: $0. The child task `t0131_rd1_na_k_remodelling_dsgc_dsi` is local simulation only, $0.

## Step by Step

1. Run aggregators and read results summaries.
2. Present state and read `SomeResults.pdf`.
3. Agree the task design and confirm.
4. Create the brainstorm task and the child task.
5. Write results, logs, run verificators, open PR and merge.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None. Brainstorm-only task.

## Time Estimation

Brainstorm session: about 1 hour.

## Risks & Fallbacks

* If `/create-task` fails, create the folder manually following
  `arf/specifications/task_file_specification.md`.
* If verificators report errors, fix them and re-run before committing.

## Verification Criteria

* `verify_task_file`, `verify_corrections`, `verify_suggestions` and `verify_logs` pass with 0
  errors for this task.
* `verify_pr_premerge` passes with 0 errors before merge.
