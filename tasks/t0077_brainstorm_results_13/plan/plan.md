# Plan: Brainstorm Results Session 13

## Objective

Run an interactive strategic brainstorming session on 2026-05-03 after t0074 (channel tuning-width
sweep on Bed A) and t0076 (25-d Bed B multi-objective Bayesian optimisation) both completed. Act on
the t0076 headline negative result (the bare 25-d Bed B substrate cannot reach DSI >= 0.4 AND PD
rate >= 30 Hz simultaneously) by commissioning a single bundled follow-up MOBO task that adds the
three architectural ingredients identified by the t0076 compare-literature analysis: an AIS section,
tier-stratified channel densities, and a slow Kv-mediated AHP. Reject fifteen suggestions covered by
the new task or made stale by the project's pivot away from the from-scratch DSGC family. Cancel
t0045 (CoreNEURON-on-GPU benchmark) which has been superseded by t0076's actual Vast.ai-CPU run.

## Approach

Follow the `/human-brainstorm` skill end-to-end: aggregate project state, read every results summary
and compare-literature file for tasks completed since brainstorm 12 (t0074 and t0076), present an
independent priority reassessment of the 20 high-priority active uncovered suggestions, conduct the
three-round discussion (one bundled task; suggestion cleanup; confirmation), scaffold the
brainstorm-results folder, write sixteen correction files, edit t0045's `task.json` to set
`status: "cancelled"`, and create the new not-started t0078 task folder via the `/create-task`
skill.

## Cost Estimation

No paid services. No remote compute. Local CPU only. Zero dollar cost.

## Step by Step

1. Review project state: run task / suggestion / cost aggregators; read `results_summary.md` and
   `compare_literature.md` for t0074 and t0076; rebuild `overview/`.
2. Form an independent reassessment of the 20 high-priority active uncovered suggestions, focusing
   on the four t0076-derived high-priority suggestions and the eleven from-scratch-family
   high-priority suggestions that the project has pivoted away from.
3. Present project state and reassessed priorities to the researcher.
4. Three-round discussion: agree on the bundled t0078 scope (AIS + tier-stratification + slow-AHP +
   implementation fixes; SK_E2 chosen for AHP; 40 - 50 d parameter space; fresh Sobol restart;
   Vast.ai compute estimate); agree on sixteen rejections plus the t0045 cancellation; explicit
   go-ahead authorising the entire remaining lifecycle.
5. Scaffold `tasks/t0077_brainstorm_results_13/` with full folder structure.
6. Write sixteen suggestion-correction files under `corrections/`: all `update` actions setting
   `status: "rejected"`, with rationale identifying the covering task or the from-scratch-family
   strategic-frame change.
7. Cancel t0045 by editing its `task.json` to set `status: "cancelled"`.
8. Create t0078 (`bedb_mobo_v2_ais_tiered_ahp`) folder via `/create-task`.
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

Approximately 70 min of interactive discussion plus 35 min of scaffolding, correction authoring,
t0045 cancellation, and child-task creation plus 25 min of verification, PR, and merge.

## Risks & Fallbacks

* **Task index drift mid-session**: a parallel session merges another task to main while this
  brainstorm runs. Mitigation: re-run the task aggregator before reserving the brainstorm task
  index; rename branch and folder if a collision is detected.
* **Researcher unavailable mid-session**: skill allows resumption from any phase boundary.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history
  per `task_git_specification` rule 14.
* **Correction-file typos**: caught by `verify_corrections.py`; fix in place before commit.
* **t0045 cancellation timing**: t0045 has been not_started since 2026-04-24 with no in-flight work
  attached. Cancellation is a single-line edit and carries no risk of data loss.
* **t0078 dependency surface**: t0078 depends on t0024, t0069, and t0076. All three are completed
  and not at risk of being rewritten on main.

## Verification Criteria

* `verify_task_file.py t0077_brainstorm_results_13` passes with 0 errors.
* `verify_logs.py t0077_brainstorm_results_13` passes with 0 errors (LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance).
* `verify_corrections.py t0077_brainstorm_results_13` passes with 0 errors for all 16 correction
  files.
* `verify_suggestions.py t0077_brainstorm_results_13` passes with 0 errors (empty array).
* The new child task (t0078) exists on disk with valid `task.json`.
* `verify_task_file.py t0078_bedb_mobo_v2_ais_tiered_ahp` passes with 0 errors.
* t0045's `task.json` parses with `status: "cancelled"`.
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
