# Plan: Brainstorm Results Session 16

## Objective

Run an interactive strategic brainstorming session on 2026-05-06 after t0083
(`bedb_v3_extend_nsga2_gen8plus`) extended t0081's NSGA-II from gen 7 through gen 17 and **expanded
the joint-pass cell population from 1 to 15 cells** with hypervolume +118%, plus t0084
(`t0081_cell_767_vm_trace_deepdive`) produced the cell-767 mechanism-attribution answer asset. The
session bundles three previously open suggestions (S-0083-02 motif clustering on Pareto cells,
S-0083-05 multi-seed smoke gate / robustness check, multi-replicate aspect of S-0081-01) into a
single combined task t0086 (`robustness_cluster_bio_comparison`) and rejects the three covered
suggestions. No reprioritisations; no other task changes; t0075 stays queued.

## Approach

Follow the `/human-brainstorm` skill end-to-end: aggregate project state, read every results summary
and compare-literature file for tasks completed since brainstorm 15 (t0083 and t0084), present an
independent priority reassessment of the active uncovered suggestions (highlighting the three now
superseded by t0086), conduct the three-round discussion (one consolidated new task; suggestion
cleanup; confirmation), scaffold the brainstorm-results folder, write three correction files, and
create the new not-started t0086 task folder.

## Cost Estimation

No paid services. No remote compute for this brainstorm task. Local CPU only. Zero dollar cost. The
child task t0086 carries an estimated cost of $1.93-$2.57 with a $3.50 hard cap (1.5x of estimate);
cost-watchdog rate-fix REQ in t0086's plan prevents a t0083-style overrun.

## Step by Step

1. Review project state: run task / suggestion / cost aggregators; read `results_summary.md`,
   `results_detailed.md`, and `compare_literature.md` for t0083 and t0084 (the two tasks completed
   since brainstorm 15); rebuild `overview/`.
2. Form an independent reassessment of the active uncovered suggestions, focusing on S-0083-02,
   S-0083-05, and S-0081-01 which are bundled and superseded by t0086.
3. Present project state and reassessed priorities to the researcher; highlight the budget context
   ($13.96 / $20.00 spent; $6.04 remaining).
4. Three-round discussion: agree on one consolidated new task (t0086 robustness + cluster +
   biological-plausibility analysis at $3.50 hard cap with cost-watchdog rate-fix REQ); agree on
   three rejections (S-0083-02, S-0083-05, S-0081-01); explicit go-ahead authorising the entire
   remaining lifecycle.
5. Scaffold `tasks/t0085_brainstorm_results_16/` with full folder structure.
6. Write three suggestion-correction files under `corrections/`: all `update` actions setting
   `status: "rejected"`, with rationale identifying t0086 as the covering task.
7. Create t0086 (`robustness_cluster_bio_comparison`) folder.
8. Write step logs, session log, and results files.
9. Capture session transcripts via `capture_task_sessions`.
10. Run all relevant verificators (`verify_task_file`, `verify_logs`, `verify_corrections`,
    `verify_suggestions`).
11. Commit, push branch, open PR, run pre-merge verificator, merge.

## Remote Machines

None.

## Assets Needed

None. The brainstorm task itself produces no assets.

## Expected Assets

None. `expected_assets = {}`.

## Time Estimation

Approximately 20 min of interactive discussion plus 15 min of scaffolding, correction authoring, and
child-task creation, plus 15 min of verification, PR, and merge. Total ~50 min wall-clock.

## Risks & Fallbacks

* **Task index drift mid-session**: a parallel session merges another task to main while this
  brainstorm runs. Mitigation: re-run the task aggregator before reserving the brainstorm task
  index.
* **Researcher unavailable mid-session**: skill allows resumption from any phase boundary.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history
  per `task_git_specification` rule 14.
* **Correction-file typos**: caught by `verify_corrections.py`; fix in place before commit.
* **Researcher prefers separate tasks over a consolidated task**: revisit decomposition in the
  three-round discussion; the consolidated bundle is consistent with the recorded researcher
  preference for one combined task over many small tasks.
* **t0086 cost-watchdog rate-fix REQ overlooked**: planning-phase verificator targets this REQ;
  implementation-phase code review enforces the rate is sourced from `machine_log.json`.

## Verification Criteria

* `verify_task_file.py t0085_brainstorm_results_16` passes with 0 errors.
* `verify_logs.py t0085_brainstorm_results_16` passes with 0 errors (LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance).
* `verify_corrections.py t0085_brainstorm_results_16` passes with 0 errors for all 3 correction
  files.
* `verify_suggestions.py t0085_brainstorm_results_16` passes with 0 errors (empty array).
* The new child task t0086 exists on disk with valid `task.json`.
* `verify_task_file.py t0086_robustness_cluster_bio_comparison` passes with 0 errors.
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
