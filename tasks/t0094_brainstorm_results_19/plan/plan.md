# Plan: Brainstorm Results Session 19

## Objective

Run an interactive strategic brainstorming session on 2026-05-08 after t0093
(`resweep_and_t0090_correction`) merged to main with 60/60 cells STABLE-firing under the t0092
patched generator and `C-0093-01` correction overlay in place. The session's purpose is to update
t0091 (`morphology_extended_nsga2_v1`) so it imports the patched generator and depends on t0092 +
t0093, then greenlight its execute-task launch.

## Approach

Follow the `/human-brainstorm` skill end-to-end. The researcher's directive was direct: "well it's
time to run an optimisation. Update the t0091 if you haven't yet done so and run it. How much budget
do we need? Is there enough?" Phase 2 Round 3 confirmation arrived implicitly via the responses to
two clarifying questions (keep S-0090-03 separate; cost watchdog $4.00). All decisions:

1. Update t0091 task.json + task_description.md with dependencies + import paths + cross-refs.
2. Reject S-0092-03 (already done by t0093).
3. Reject S-0090-04 (premise invalidated by t0093's 60/60 STABLE).

## Cost Estimation

Zero dollars for this brainstorm. No paid services, no remote compute, no API spend. The
commissioned downstream work (t0091 execute-task) is estimated at $3.00–3.50 within the existing
$4.00 cost watchdog and $4.45 remaining budget.

## Step by Step

1. Aggregate project state: tasks, suggestions (uncovered, by priority), costs, answers (manual glob
   since no aggregator exists for this asset kind in this branch).
2. Read results summaries for tasks completed since t0089: t0090, t0092, t0093.
3. Form independent priority reassessment of the 12 active high-priority suggestions; identify
   S-0092-03 and S-0090-04 as falsified by t0093.
4. Present project state to the researcher with concrete metrics, mean DSI, budget breakdown, and
   reassessed suggestion priorities.
5. Answer researcher's clarifying questions about the soma-pt3d bug, the fix, the validation
   evidence, the per-cell DSI spread, and where to find per-cell data.
6. Receive launch directive; answer budget question with the $4.45 / $3.00–3.50 / $4.00 watchdog
   breakdown.
7. Two-question clarification: NMDA calibration scope (kept separate); watchdog cap ($4.00).
8. Scaffold `tasks/t0094_brainstorm_results_19/` with the full mandatory folder structure.
9. Update t0091 task.json (add t0092 + t0093 to dependencies; refresh short_description) and
   task_description.md (swap generator import path; refresh anchor reference; refresh
   risk-and-fallback; extend cross-references).
10. Write 2 suggestion-rejection correction files under `corrections/`.
11. Write step logs, session log, results files.
12. Capture session transcripts via `capture_task_sessions`.
13. Run verificators (`verify_task_file`, `verify_logs`, `verify_corrections`,
    `verify_suggestions`).
14. Re-run materialiser; format markdown; commit, push, PR, premerge, merge.

## Remote Machines

None for this brainstorm task.

## Assets Needed

None.

## Expected Assets

None. `expected_assets = {}`.

## Time Estimation

Approximately 25 minutes of interactive discussion (researcher led with bug-explanation questions
plus a per-cell DSI lookup) plus 10 minutes of scaffolding + correction authoring + t0091 update,
plus 10 minutes of verification, PR, and merge. Total ~45 minutes wall-clock.

## Risks & Fallbacks

* **Task index drift mid-session**: parallel session merges another task to main while this
  brainstorm runs. Mitigation: re-run task aggregator before reserving the brainstorm task index; no
  parallel branch was active.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history.
* **t0091 update introduces typos in import paths or dependency IDs**: caught by
  `verify_task_file.py t0091` after the edit; retest before commit.
* **Correction-file typos**: caught by `verify_corrections.py`; fix in place before commit.

## Verification Criteria

* `verify_task_file.py t0094_brainstorm_results_19` passes with 0 errors.
* `verify_task_file.py t0091_morphology_extended_nsga2_v1` passes with 0 errors after the update.
* `verify_logs.py t0094_brainstorm_results_19` passes with 0 errors (LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture).
* `verify_corrections.py t0094_brainstorm_results_19` passes with 0 errors for 2 correction files.
* `verify_suggestions.py t0094_brainstorm_results_19` passes with 0 errors (empty array).
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
