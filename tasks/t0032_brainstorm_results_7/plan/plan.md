# Plan: Brainstorm Results Session 7

## Objective

Run an interactive strategic brainstorming session on 2026-04-22, a few hours after the t0028
brainstorm-session-6 merge, and record the researcher's decision to commission a single planning
task (t0033) that scopes and costs a future joint DSGC morphology + top-10 voltage-gated channel
DSI-maximisation optimisation on Vast.ai GPU.

## Approach

Follow the `/human-brainstorm` skill workflow: aggregate project state, present findings, conduct
structured discussion with the researcher across three rounds (new tasks, suggestion cleanup,
confirmation), apply decisions by scaffolding a brainstorm-results task folder and chaining a single
`/create-task` invocation for the approved child task (t0033), finalize with verificators and a PR.

## Cost Estimation

No paid services. No remote compute. Local CPU only. Zero dollar cost.

## Step by Step

1. Review project state: aggregate tasks, suggestions, costs; read recent results summaries; rebuild
   `overview/`.
2. Present to researcher and run clarifying questions.
3. Structured discussion across three rounds.
4. Determine next task IDs and scaffold `tasks/t0032_brainstorm_results_7/`.
5. Chain `/create-task` for the one approved child task (t0033).
6. Write step logs, session log, and results files.
7. Run all relevant verificators (`verify_task_file`, `verify_logs`, `verify_corrections`,
   `verify_suggestions`, `verify_pr_premerge`).
8. Commit per step, push branch, open PR, merge, rebuild `overview/` on main.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None. `expected_assets = {}`.

## Time Estimation

Approximately 15 minutes of interactive session + 20 min of scaffolding and verification + 10 min of
PR / merge / overview sync.

## Risks & Fallbacks

* **Researcher unavailable mid-session**: skill allows resumption from any phase boundary.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history
  per `task_git_specification` rule 14.
* **Child `/create-task` auto-indexing race**: scaffolding t0032 first guarantees auto-index picks
  33+ for the child task per human-brainstorm Phase 3 ordering invariant.
* **Parallel brainstorm risk**: t0029 is currently in_progress in its own worktree; this session
  writes only new files under `tasks/t0032_brainstorm_results_7/` and `tasks/t0033_*/`, so there is
  no file contention with the t0029 worktree.

## Verification Criteria

* `verify_task_file.py t0032_brainstorm_results_7` passes with 0 errors.
* `verify_logs.py t0032_brainstorm_results_7` passes with 0 errors.
* `verify_corrections.py t0032_brainstorm_results_7` passes with 0 errors.
* `verify_suggestions.py t0032_brainstorm_results_7` passes with 0 errors.
* The child task t0033 exists on disk with valid `task.json`.
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
