# Plan: Brainstorm Results Session 11

## Objective

Run an interactive strategic brainstorming session on 2026-04-29 after t0055 (Mg-block NMDA recovery
test) and t0057 (tonic-GABA amplitude sweep on t0053 spatial substrate) both completed; act on the
convergent finding that every from-scratch minimal DSGC variant (t0052/t0053/t0054/t0055/ t0057) is
stuck in a binary regime (single-spike-per-trial OR full suppression); commission a single new task
that combines per-synapse bar-arrival-locked tonic GABA windows (S-0057-04) with an AMPA escape
sweep (S-0057-02), a sub-veto GABA sweep (S-0057-01), and the project-wide measurement- protocol fix
(S-0055-01) into one substrate; reject seven covered or superseded high-priority suggestions;
reprioritise seventeen high-priority suggestions to medium where the brainstorm-9 from-scratch pivot
or recent results have de-urgented them.

## Approach

Follow the `/human-brainstorm` skill end-to-end: aggregate project state, read every results summary
for tasks completed since brainstorm 10 (t0055, t0057), present an independent priority reassessment
of the 32 high-priority active suggestions, conduct the three-round discussion (new task, suggestion
cleanup, confirmation), scaffold the brainstorm-results folder, write twenty-five correction files,
and create one new not-started task folder via the `/create-task` skill.

## Cost Estimation

No paid services. No remote compute. Local CPU only. Zero dollar cost.

## Step by Step

1. Review project state: run task / suggestion / cost aggregators; read `results_summary.md` for
   t0055 and t0057; rebuild `overview/`.
2. Form an independent reassessment of the 32 high-priority active suggestions, focusing on those
   covered by completed work and those superseded by the brainstorm-9 pivot or by t0055/t0057
   results.
3. Present project state and reassessed priorities to the researcher.
4. Three-round discussion: agree on the combined t0059 task design (bar-locked GABA + AMPA escape
   + protocol fix); agree on seven rejections and eighteen reprioritisations; explicit go-ahead.
5. Scaffold `tasks/t0058_brainstorm_results_11/` with full folder structure.
6. Write twenty-five suggestion-correction files under `corrections/`: seven `update` actions
   setting `status: "rejected"`, eighteen `update` actions setting `priority: "medium"`.
7. Create t0059 (`bar_locked_gaba_ampa_sweep_t0057`) folder via `/create-task` with valid
   `task.json` and `task_description.md`.
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

Approximately 50 min of interactive discussion + 30 min of scaffolding, correction authoring, and
child-task creation + 10 min of verification, PR, and merge.

## Risks & Fallbacks

* **Researcher unavailable mid-session**: skill allows resumption from any phase boundary.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history
  per `task_git_specification` rule 14.
* **Correction-file typos**: caught by `verify_corrections.py`; fix in place before commit.
* **Compute-budget creep on t0059**: wall-clock estimate is ~8.75 h on local CPU for 9000 trials. If
  overnight runs are not acceptable, t0059 can be split or trimmed at planning time without
  affecting the brainstorm task itself.

## Verification Criteria

* `verify_task_file.py t0058_brainstorm_results_11` passes with 0 errors.
* `verify_logs.py t0058_brainstorm_results_11` passes with 0 errors (LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance).
* `verify_corrections.py t0058_brainstorm_results_11` passes with 0 errors for all 25 correction
  files.
* `verify_suggestions.py t0058_brainstorm_results_11` passes with 0 errors (empty array).
* The new child task (t0059) exists on disk with valid `task.json`.
* `verify_task_file.py` passes for t0059.
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
