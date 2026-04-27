# Plan: Brainstorm Results Session 9

## Objective

Run an interactive strategic brainstorming session on 2026-04-25 after the t0046–t0050
reproduction wave; reframe the project around a new from-scratch minimal-DSGC substrate; commission
two parallel implementation tasks (scalar `gabaMOD` vs spatial PD/ND-asymmetric inhibition); cancel
three obsolete `intervention_blocked` tasks; reprioritise six follow-up suggestions whose urgency
the new substrate dissolves.

## Approach

Follow the `/human-brainstorm` skill end-to-end: aggregate project state, read every recent results
summary, present an independent priority reassessment, conduct the three-round discussion (new
tasks, suggestion cleanup, confirmation), scaffold the brainstorm-results folder, write three
task-cancellation edits, six suggestion corrections, and create two new not-started task folders.

## Cost Estimation

No paid services. No remote compute. Local CPU only. Zero dollar cost.

## Step by Step

1. Review project state: run task / suggestion / cost aggregators; read every results summary for
   t0041, t0046, t0047, t0048, t0049, t0050; rebuild `overview/`.
2. Form an independent reassessment of the 49 high-priority active suggestions, focusing on those
   superseded by the new from-scratch substrate.
3. Present project state and reassessed priorities to the researcher.
4. Three-round discussion: agree on Task A (scalar gabaMOD) and Task B (spatial asymmetry); agree on
   cancellations of t0042/t0043/t0044; agree on six suggestion reprioritisations.
5. Scaffold `tasks/t0051_brainstorm_results_9/` with full folder structure.
6. Cancel t0042/t0043/t0044 by editing their `task.json` `status` to `"cancelled"`.
7. Write six suggestion-update correction files under `corrections/`.
8. Create t0052 (`minimal_dsgc_scalar_gaba`) and t0053 (`minimal_dsgc_spatial_gaba`) folders with
   valid `task.json` and `task_description.md`.
9. Write step logs, session log, and results files.
10. Capture session transcripts via `capture_task_sessions`.
11. Run all relevant verificators (`verify_task_file`, `verify_logs`, `verify_corrections`,
    `verify_suggestions`).
12. Commit, push branch, open PR, run pre-merge verificator, merge.

## Remote Machines

None.

## Assets Needed

None. The brainstorm task itself produces no assets.

## Expected Assets

None. `expected_assets = {}`.

## Time Estimation

Approximately 30 min of interactive discussion + 45 min of scaffolding, cancellation edits,
correction authoring, and child-task creation + 15 min of verification, PR, and merge.

## Risks & Fallbacks

* **Researcher unavailable mid-session**: skill allows resumption from any phase boundary.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history
  per `task_git_specification` rule 14.
* **Cancellation race**: t0042/t0043/t0044 edits happen on the brainstorm branch and merge
  atomically; no risk of interleaving with other tasks because no execution is running on those
  folders.
* **Correction-file typos**: caught by `verify_corrections.py`; fix in place before commit.

## Verification Criteria

* `verify_task_file.py t0051_brainstorm_results_9` passes with 0 errors.
* `verify_logs.py t0051_brainstorm_results_9` passes with 0 errors.
* `verify_corrections.py t0051_brainstorm_results_9` passes with 0 errors for all 6 correction
  files.
* `verify_suggestions.py t0051_brainstorm_results_9` passes with 0 errors (empty suggestions array).
* Both child tasks (t0052, t0053) exist on disk with valid `task.json`.
* `verify_task_file.py` passes for t0052 and t0053.
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
