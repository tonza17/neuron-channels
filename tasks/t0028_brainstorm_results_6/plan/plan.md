# Plan: Brainstorm Results Session 6

## Objective

Run an interactive strategic brainstorming session after completion of t0026 and t0027, decide the
next batch of experimental tasks, and record decisions in a brainstorm-results task folder.

## Approach

Follow the `/human-brainstorm` skill workflow: aggregate project state, present findings, conduct
structured discussion with the researcher across three rounds (new tasks, suggestion cleanup,
confirmation), apply decisions by scaffolding a brainstorm-results task folder and chaining
`/create-task` invocations for each approved child task, finalize with verificators and a PR.

## Cost Estimation

No paid services. No remote compute. Local CPU only. Zero dollar cost.

## Step by Step

1. Review project state: aggregate tasks, suggestions, costs; read recent `results_summary.md` and
   `compare_literature.md`; rebuild `overview/`.
2. Present to researcher and run clarifying questions.
3. Structured discussion across three rounds.
4. Determine next task IDs and scaffold `tasks/t0028_brainstorm_results_6/`.
5. Chain `/create-task` for each approved child task (t0029, t0030, t0031).
6. Write step logs, session log, and results files.
7. Run all relevant verificators (`verify_task_file`, `verify_logs`, `verify_task_results`,
   `verify_pr_premerge`).
8. Commit per step, push branch, open PR, merge, rebuild `overview/` on main.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None. `expected_assets = {}`.

## Time Estimation

Approximately 1 hour of interactive session + 30 min of scaffolding and verification + 10 min of PR
/ merge / overview sync.

## Risks & Fallbacks

* **Researcher unavailable mid-session**: skill allows resumption from any phase boundary.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history
  per task_git_specification rule 14.
* **Child `/create-task` auto-indexing race**: scaffolding t0028 first guarantees auto-index picks
  29+ for child tasks per human-brainstorm Phase 3 ordering invariant.

## Verification Criteria

* `verify_task_file.py t0028_brainstorm_results_6` passes with 0 errors.
* `verify_logs.py t0028_brainstorm_results_6` passes with 0 errors.
* `verify_task_results.py t0028_brainstorm_results_6` passes with 0 errors.
* All three child tasks (t0029, t0030, t0031) exist on disk with valid `task.json`.
* PR opens, CI passes, merge to main succeeds, `overview/` rebuilds cleanly on main.
