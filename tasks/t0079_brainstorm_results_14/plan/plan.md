# Plan: Brainstorm Results Session 14

## Objective

Run an interactive strategic brainstorming session on 2026-05-04 after t0078 (49-d Bed B v2 BoTorch
qLogNEHVI multi-objective Bayesian optimisation with AIS, tier-stratified channels, and slow Kv-AHP)
completed. Act on the t0078 architectural diagnostic (the AIS-augmented substrate expanded HV by
+36% over t0076 but missed the joint pass criterion `DSI >= 0.4 AND PD >= 10 Hz` by 0.084 on DSI and
0.32 Hz on PD; the high-DSI rail's PD ceiling pinned at 2.86 Hz signals missing dendritic-spike
machinery; iter-81's `nav16_ais` collapsed to the search-space floor four orders below the Kole 2008
prior, signalling a MOBO-on-biophysics failure mode) by commissioning a single bundled follow-up
MOBO v3 task that adds dendritic-spike machinery, switches the optimiser from BO to NSGA-II, and
enforces biological hard lower bounds. Reject three suggestions covered by the new task. No
reprioritisations; no other task changes.

## Approach

Follow the `/human-brainstorm` skill end-to-end: aggregate project state, read every results summary
and compare-literature file for tasks completed since brainstorm 13 (t0078), present an independent
priority reassessment of the 7 high-priority active uncovered suggestions (with focus on the eight
t0078-derived suggestions newly added to the backlog), conduct the three-round discussion (one
bundled task; suggestion cleanup; confirmation), scaffold the brainstorm-results folder, write three
correction files, and create the new not-started t0080 task folder via the `/create-task` skill.

## Cost Estimation

No paid services. No remote compute. Local CPU only. Zero dollar cost.

## Step by Step

1. Review project state: run task / suggestion / cost aggregators; read `results_summary.md`,
   `results_detailed.md`, and `compare_literature.md` for t0078; rebuild `overview/`.
2. Form an independent reassessment of the 7 high-priority active uncovered suggestions, focusing on
   the eight t0078-derived suggestions and the architectural arc the project is now on (passive Bed
   B -> AIS+tier+slow-AHP Bed B -> dendritic-spike Bed B).
3. Present project state and reassessed priorities to the researcher.
4. Three-round discussion: agree on the bundled t0080 scope (dendritic-spike machinery + NSGA-II +
   biological hard bounds; tau_ca_multiplier kept at 20x; S-0078-02 and S-0078-08 folded in; compute
   envelope ~$1.00 - $1.50 with $2.00 hard cap on Vast.ai 64-core CPU); agree on three rejections;
   explicit go-ahead authorising the entire remaining lifecycle.
5. Scaffold `tasks/t0079_brainstorm_results_14/` with full folder structure.
6. Write three suggestion-correction files under `corrections/`: all `update` actions setting
   `status: "rejected"`, with rationale identifying t0080 as the covering task.
7. Create t0080 (`bedb_mobo_v3_dendritic_spike_nsga2`) folder via `/create-task`.
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

Approximately 45 min of interactive discussion plus 15 min of scaffolding, correction authoring, and
child-task creation, plus 15 min of verification, PR, and merge. Total ~75 min wall-clock.

## Risks & Fallbacks

* **Task index drift mid-session**: a parallel session merges another task to main while this
  brainstorm runs. Mitigation: re-run the task aggregator before reserving the brainstorm task
  index; rename branch and folder if a collision is detected.
* **Researcher unavailable mid-session**: skill allows resumption from any phase boundary.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history
  per `task_git_specification` rule 14.
* **Correction-file typos**: caught by `verify_corrections.py`; fix in place before commit.
* **t0080 dependency surface**: t0080 depends on t0024, t0069, t0076, t0078. All four are completed
  and not at risk of being rewritten on main.
* **NSGA-II vs BO regression**: if NSGA-II at pop 96 / gen 40 fails to match t0078's HV 11.41 on the
  v3 substrate, that is itself a useful methodological finding documented as part of t0080's
  results, not a brainstorm-level risk.

## Verification Criteria

* `verify_task_file.py t0079_brainstorm_results_14` passes with 0 errors.
* `verify_logs.py t0079_brainstorm_results_14` passes with 0 errors (LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance).
* `verify_corrections.py t0079_brainstorm_results_14` passes with 0 errors for all 3 correction
  files.
* `verify_suggestions.py t0079_brainstorm_results_14` passes with 0 errors (empty array).
* The new child task (t0080) exists on disk with valid `task.json`.
* `verify_task_file.py t0080_bedb_mobo_v3_dendritic_spike_nsga2` passes with 0 errors.
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
