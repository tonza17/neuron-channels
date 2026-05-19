# Plan: Brainstorm Session 22

## Objective

Decide the next experimental task after the t0106 -> t0110 NSGA-II + analysis wave. The central open
question is whether the t0106 joint-pass result (123 unique cells, DSI >= 0.5 AND PD >= 30 Hz)
replicates across GA seeds, or is a seed-specific artefact.

## Approach

1. Aggregate project state (tasks, suggestions, costs, recent answers and results).
2. Form an independent reassessment of suggestion priorities given t0106 / t0107 / t0108 / t0110.
3. Discuss with the researcher in three structured rounds: new tasks, suggestion cleanup,
   confirmation.
4. Apply decisions and create a new minimum-change replicate task.
5. Record the session in step logs and the session transcript.

## Cost Estimation

This task: $0. Commissions one child task (`t0112_t0106_seed77_replicate`) with a $25 cap; expected
actual ~$10-11 mirroring t0106.

## Step by Step

1. Run aggregators (`aggregate_tasks`, `aggregate_suggestions`, `aggregate_costs`) and read recent
   `results_summary.md` and `compare_literature.md` files.
2. Materialise the overview so the latest state is browsable on GitHub.
3. Present project state plus an independent priority reassessment.
4. Round 1: propose t0112.
5. Round 2: propose suggestion cleanup; researcher chooses to skip cleanup.
6. Round 3: confirm decision list.
7. Phase 4: create this brainstorm task folder.
8. Phase 5: create child task `t0112_t0106_seed77_replicate` via `/create-task`.
9. Phase 6: write results, step logs, session transcript, verificators, push, PR, merge.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None. Brainstorm-only task.

## Time Estimation

Brainstorm session: ~1 hour. Child task t0112: ~3-5 hours wall-clock on Vast.ai.

## Risks & Fallbacks

* If the `/create-task` skill fails to claim index 112, retry once; if it still fails, manually
  create the t0112 folder following `arf/specifications/task_file_specification.md`.
* If verificators surface unexpected errors at the finalize step, fix and re-run; do not commit with
  errors.

## Verification Criteria

* `verify_task_file t0111_brainstorm_results_22` passes with 0 errors.
* `verify_corrections t0111_brainstorm_results_22` passes with 0 errors (no corrections this
  session).
* `verify_suggestions t0111_brainstorm_results_22` passes with 0 errors (no new suggestions this
  session).
* `verify_logs t0111_brainstorm_results_22` passes with 0 errors (warnings LG-W005, LG-W007, LG-W008
  may be present and are non-blocking for a pure-planning brainstorm).
* `verify_pr_premerge t0111_brainstorm_results_22 --pr-number <N>` passes with 0 errors before
  merge.
