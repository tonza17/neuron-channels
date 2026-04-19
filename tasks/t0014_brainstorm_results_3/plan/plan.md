# Plan — Brainstorm Session 3

## Objective

Decide the next task wave in a structured researcher-AI dialogue, record the decisions as
corrections / suggestions / new task folders, and close out with a merged PR.

## Approach

Four-step brainstorm flow:

1. Aggregate project state (tasks, suggestions, costs, answers) and present to the researcher.
2. Discuss: propose new tasks, review suggestion backlog, confirm.
3. Apply: scaffold brainstorm task folder, write suggestions, create child task folders, bump
   project budget.
4. Finalize: write results, step logs, session capture, verificators, PR, merge.

## Cost Estimation

Zero external cost. Pure planning task.

## Step by Step

1. Run `aggregate_tasks`, `aggregate_suggestions`, `aggregate_costs` aggregators.
2. Present state + concerns (category overlap, corpus redundancy, budget gate) to researcher.
3. Iterate until researcher confirms task list and budget resolution.
4. Create `task/t0014_brainstorm_results_3` branch.
5. Scaffold mandatory folder structure.
6. Write 5 `S-0014-NN` suggestions to `results/suggestions.json`.
7. Bump `project/budget.json` `total_budget` to $1.
8. Invoke `/create-task` for each of 5 child tasks (t0015-t0019).
9. Write results_summary, results_detailed, step logs, session log.
10. Run verificators (`verify_task_file`, `verify_suggestions`, `verify_logs`).
11. Materialize overview, push, open PR, run `verify_pr_premerge`, merge.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None (brainstorming task).

## Time Estimation

~30 minutes of wall-clock for the brainstorm + scaffolding; child task execution is scoped
separately per-task after merge.

## Risks & Fallbacks

* **Risk**: `verify_pr_premerge` flags unrelated file changes. **Fallback**: restrict staged files
  to the brainstorm folder + `project/budget.json`; leave other uncommitted state alone.
* **Risk**: budget bump blocked by `verify_task_folder` (files outside task folder). **Fallback**:
  the brainstorm skill explicitly allows project-state edits (suggestions, task.json of other
  not-started tasks); budget bump is an agreed decision recorded in this task's results.
* **Risk**: child task creation picks overlapping `task_index` values. **Fallback**: serialise
  `/create-task` invocations if the aggregator-based index selection races.

## Verification Criteria

* All step log folders contain valid `step_log.md` files with frontmatter and 4 mandatory sections.
* `verify_task_file`, `verify_suggestions`, `verify_logs` pass with zero errors.
* 5 child task folders exist at `tasks/t0015_*` through `tasks/t0019_*` with status
  `"not_started"`.
* `project/budget.json` `total_budget` is `1.0`.
* PR merged to main; overview rebuilt.
