# Plan: Brainstorm Results Session 8

## Objective

Run an interactive strategic brainstorming session on 2026-04-24 to audit every simulation test the
project has run against published data, identify recurring discrepancies (peak firing rate, DSI
pinning, missing Schachter active amplification), and commission four follow-up tasks that target
the top-leverage corrections.

## Approach

Follow the `/human-brainstorm` skill end-to-end: aggregate project state, delegate synthesis reads
to subagents, present master test table and published-data comparison table, conduct three-round
discussion (new tasks, suggestion cleanup, confirmation), scaffold brainstorm-results folder and
chain four `/create-task` invocations, write five suggestion correction files, finalise with
verificators and a PR.

## Cost Estimation

No paid services. No remote compute. Local CPU only. Zero dollar cost.

## Step by Step

1. Review project state: aggregate tasks, suggestions, costs; read recent task results
   (t0033–t0039) and all `compare_literature.md` files; rebuild `overview/`.
2. Delegate synthesis to subagents: Phase 1 state summary and test-vs-literature audit table.
3. Present master tables and recommended corrections to researcher.
4. Structured discussion: agree on four new tasks (t0041–t0044) and suggestion corrections.
5. Scaffold `tasks/t0040_brainstorm_results_8/` with full folder structure.
6. Write five correction files in `corrections/`.
7. Save master test table + published comparison under `results/test_vs_literature_table.md`.
8. Chain `/create-task` for each of the four approved child tasks.
9. Write step logs, session log, and results files.
10. Run all relevant verificators (`verify_task_file`, `verify_logs`, `verify_corrections`,
    `verify_suggestions`, `verify_pr_premerge`).
11. Commit per step, push branch, open PR, merge, rebuild `overview/` on main.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None. `expected_assets = {}`.

## Time Estimation

Approximately 45 min of interactive discussion + 30 min of scaffolding, correction authoring, and
child-task creation + 15 min of verification, PR, and merge.

## Risks & Fallbacks

* **Researcher unavailable mid-session**: skill allows resumption from any phase boundary.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history
  per `task_git_specification` rule 14.
* **Child `/create-task` auto-indexing race**: scaffolding t0040 first guarantees auto-index picks
  41+ for each child task per human-brainstorm Phase 3 ordering invariant.
* **Correction-file typos** (bad `target_task` or `target_id`): caught by `verify_corrections.py`;
  fix in place before commit.
* **t0031 and t0023 blocking interpretation of comparison table**: both are acknowledged in the
  session but neither is modified here; their states carry forward unchanged.

## Verification Criteria

* `verify_task_file.py t0040_brainstorm_results_8` passes with 0 errors.
* `verify_logs.py t0040_brainstorm_results_8` passes with 0 errors.
* `verify_corrections.py t0040_brainstorm_results_8` passes with 0 errors for all 5 correction
  files.
* `verify_suggestions.py t0040_brainstorm_results_8` passes with 0 errors (empty suggestions array).
* All four child tasks (t0041–t0044) exist on disk with valid `task.json`.
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
