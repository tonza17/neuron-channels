# Plan: Brainstorm Results Session 10

## Objective

Run an interactive strategic brainstorming session on 2026-04-28 after the from-scratch minimal DSGC
wave (t0052, t0053, t0054) completed and t0055 (Mg-block NMDA recovery test) started; act on a
researcher observation that t0053's GABA conductance is only present in a narrow ~100-200 ms window
per trial; commission a single new task that replaces the per-event Exp2Syn GABA mechanism with a
sustained-window tonic GABA point process and sweeps the per-synapse peak conductance to recover
non-zero FULL-mode tuning curves; reject four covered or superseded high-priority suggestions;
reprioritise nineteen high-priority suggestions to medium where brainstorm-9 pivot or recent results
have de-urgented them.

## Approach

Follow the `/human-brainstorm` skill end-to-end: aggregate project state, read every results summary
and `compare_literature.md` for tasks completed since brainstorm 9 (t0052, t0053, t0054), read the
t0055 task description for in-flight context, present an independent priority reassessment of the 50
high-priority active suggestions, conduct the three-round discussion (new task, suggestion cleanup,
confirmation), scaffold the brainstorm-results folder, write twenty-three correction files, and
create one new not-started task folder via the `/create-task` skill.

## Cost Estimation

No paid services. No remote compute. Local CPU only. Zero dollar cost.

## Step by Step

1. Review project state: run task / suggestion / cost aggregators; read every results summary and
   `compare_literature.md` for t0052, t0053, t0054; read t0055's `task.json` for in-flight context;
   rebuild `overview/`.
2. Form an independent reassessment of the 50 high-priority active suggestions, focusing on those
   covered by completed work and those superseded by the brainstorm-9 pivot or by t0052-t0054
   results.
3. Present project state and reassessed priorities to the researcher.
4. Three-round discussion: agree on the t0057 tonic-GABA + amplitude sweep task; agree on four
   rejections and nineteen reprioritisations; explicit go-ahead.
5. Scaffold `tasks/t0056_brainstorm_results_10/` with full folder structure.
6. Write twenty-three suggestion-correction files under `corrections/`: four `update` actions
   setting `status: "rejected"`, nineteen `update` actions setting `priority: "medium"`.
7. Create t0057 (`tonic_gaba_sweep_t0053`) folder via `/create-task` with valid `task.json` and
   `task_description.md`.
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

Approximately 35 min of interactive discussion + 15 min of scaffolding, correction authoring, and
child-task creation + 10 min of verification, PR, and merge.

## Risks & Fallbacks

* **Researcher unavailable mid-session**: skill allows resumption from any phase boundary.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history
  per `task_git_specification` rule 14.
* **Correction-file typos**: caught by `verify_corrections.py`; fix in place before commit.
* **t0055 in flight**: brainstorm decisions do not modify the t0055 task folder; t0055 will complete
  on its own branch under the existing GABA timing, and any retroactive re-run on the new tonic-GABA
  architecture is deferred to a future brainstorm informed by both t0055 and t0057 outputs.

## Verification Criteria

* `verify_task_file.py t0056_brainstorm_results_10` passes with 0 errors.
* `verify_logs.py t0056_brainstorm_results_10` passes with 0 errors (LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance).
* `verify_corrections.py t0056_brainstorm_results_10` passes with 0 errors for all 23 correction
  files.
* `verify_suggestions.py t0056_brainstorm_results_10` passes with 0 errors (empty array).
* The new child task (t0057) exists on disk with valid `task.json`.
* `verify_task_file.py` passes for t0057.
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
