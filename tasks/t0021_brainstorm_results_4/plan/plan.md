# Plan — Brainstorm Session 4

## Objective

Decide the next task wave in a structured researcher-AI dialogue, record the decisions as
corrections / suggestions / new task folders, and close out with a merged PR.

## Approach

Four-step brainstorm flow:

1. Aggregate project state (tasks, suggestions, costs, answers) and present to the researcher.
2. Discuss: propose new tasks, review suggestion backlog, confirm.
3. Apply: scaffold brainstorm task folder, create child task folders, write intervention files for
   deferred child tasks.
4. Finalize: write results, step logs, session capture, verificators, PR, merge.

## Cost Estimation

Zero external cost. Pure planning task.

## Step by Step

1. Run `aggregate_tasks`, `aggregate_suggestions`, `aggregate_costs`, `aggregate_answers` and read
   recent task summaries (t0020 and t0015-t0019).
2. Present state + gap (no DSGC model suitable for channel-mechanism testing) to researcher.
3. Iterate until researcher confirms task list: one active t0022, two `intervention_blocked`
   comparison ports (t0023, t0024).
4. Create `task/t0021_brainstorm_results_4` branch.
5. Scaffold mandatory folder structure for t0021.
6. Invoke `/create-task` for t0022, t0023, t0024.
7. Mark t0023 and t0024 as `intervention_blocked` and write intervention files explaining the
   deferral pending t0022 results.
8. Write results_summary, results_detailed, step logs, session log.
9. Run verificators (`verify_task_file`, `verify_corrections`, `verify_suggestions`, `verify_logs`).
10. Materialize overview, push, open PR, run `verify_pr_premerge`, merge.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None (brainstorming task).

## Time Estimation

~4 hours wall-clock including aggregator reads, literature-blueprint review, and three child-task
scaffolds. Child task execution is scoped separately per-task after merge.

## Risks & Fallbacks

* **Risk**: researcher disagrees with modify-existing over new-port. **Fallback**: re-open
  discussion and re-scope the active task.
* **Risk**: `/create-task` picks overlapping `task_index` values. **Fallback**: serialise
  `/create-task` invocations if the aggregator-based index selection races.
* **Risk**: `verify_pr_premerge` flags unrelated file changes. **Fallback**: restrict staged files
  to the brainstorm folder and the three child task folders.

## Verification Criteria

* All step log folders contain valid `step_log.md` files with frontmatter and 4 mandatory sections.
* `verify_task_file`, `verify_corrections`, `verify_suggestions`, `verify_logs` pass with zero
  errors.
* t0022 exists with status `not_started`; t0023 and t0024 exist with status `intervention_blocked`
  and matching intervention files.
* PR merged to main; overview rebuilt.
