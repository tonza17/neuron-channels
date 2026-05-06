# Plan: Brainstorm Results Session 17

## Objective

Run an interactive strategic brainstorming session on 2026-05-06 after t0086
(`robustness_cluster_bio_comparison`) classified the 20-cell test set as 6 Genuine + 7 Marginal + 7
Stochastic, found k=2 clusters on the 6 Genuine cells with both clusters classified exotic by the
biological scorecard (NMDA per-synapse +85-122 sigma above Sivyer 2013, NaP +7-24 sigma above Stuart
1999). The session commissions one consolidated combined task t0088
(`recluster_marginals_and_vm_motifs`) bundling re-clustering with the 7 Marginal cells included
(13-cell pool instead of 6) and per-cluster Vm-trace deep-dive at 16 directions (extension of
S-0086-03 scope). Rejects S-0086-03 as covered.

## Approach

Follow the `/human-brainstorm` skill end-to-end. The researcher provided a one-shot directive
explicitly extending S-0086-03's scope: "implement S-0086-03 but before doing this redo the
clustering including marginal cells as well. All in one task." Aggregate project state, read t0086's
results summary, scaffold the brainstorm-results folder, write one correction file, and create the
t0088 not-started task folder.

## Cost Estimation

No paid services. No remote compute. Local CPU only. Zero dollar cost. The child task t0088 carries
zero cost as well (local-CPU only); preserves the $4.44 buffer for subsequent S-0086-* follow-ups.

## Step by Step

1. Review project state: run task / suggestion / cost aggregators; read
   `tasks/t0086_robustness_cluster_bio_comparison/results/results_summary.md` (the only task
   completed since brainstorm 16); rebuild `overview/`.
2. Form an independent reassessment of the active uncovered suggestions, focusing on S-0086-03 which
   is the seed of the new task.
3. Present project state and reassessed priorities to the researcher; record the verbatim directive.
4. Three-round discussion: agree on one consolidated new task t0088 (re-cluster 13 cells +
   per-cluster Vm-trace deep-dive at 16 directions); agree on one rejection (S-0086-03 covered); the
   directive itself is the explicit go-ahead.
5. Scaffold `tasks/t0087_brainstorm_results_17/` with full folder structure.
6. Write one suggestion-correction file under `corrections/`: `update` action setting
   `status: "rejected"` for S-0086-03, with rationale identifying t0088 as the covering task.
7. Create t0088 (`recluster_marginals_and_vm_motifs`) folder.
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

Approximately 10 min of interactive discussion plus 15 min of scaffolding, correction authoring, and
child-task creation, plus 15 min of verification, PR, and merge. Total ~40-50 min wall-clock.

## Risks & Fallbacks

* **Task index drift mid-session**: a parallel session merges another task to main while this
  brainstorm runs. Mitigation: re-run the task aggregator before reserving the brainstorm task
  index.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history.
* **Correction-file typos**: caught by `verify_corrections.py`; fix in place before commit.
* **Researcher prefers separate clustering and deep-dive tasks**: not chosen; the researcher's
  directive explicitly bundles them: "All in one task."
* **t0088 deep-dive 16 directions per cell is slower than estimated**: still local-CPU $0; if
  wall-clock exceeds 2 hours, reduce to 12 directions and re-run.

## Verification Criteria

* `verify_task_file.py t0087_brainstorm_results_17` passes with 0 errors.
* `verify_logs.py t0087_brainstorm_results_17` passes with 0 errors (LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance).
* `verify_corrections.py t0087_brainstorm_results_17` passes with 0 errors for 1 correction file.
* `verify_suggestions.py t0087_brainstorm_results_17` passes with 0 errors (empty array).
* The new child task t0088 exists on disk with valid `task.json`.
* `verify_task_file.py t0088_recluster_marginals_and_vm_motifs` passes with 0 errors.
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
