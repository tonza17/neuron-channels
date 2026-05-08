# Plan: Brainstorm Results Session 20

## Objective

Run an interactive strategic brainstorming session on 2026-05-08 while t0091
(`morphology_extended_nsga2_v1`) is in flight on Vast.ai. The session's purpose is to commission a
single consolidated literature survey of multi-objective optimisation in single-neuron compartmental
models, broadening the MOBO objective space beyond DSI + firing rate to include information transfer
rate, metabolic energy, cytoplasm volume, and robustness objectives.

## Approach

Follow the `/human-brainstorm` skill end-to-end. The researcher led with a strategic broadening
request: "Now that we have working optimisation for both morphology and channel composition we can
optimise for different things... DSI and information transfer rate; DSI and energy spent; DSI and
minimisation of cytoplasm volume etc. Perform an extensive literature search and find papers that
use different forms of optimisation. It does not need to be DSGC but can be any neurons." Three
multi-choice clarifications resolved scope (broad / one consolidated survey / catalogue + formulas +
recipes); explicit confirmation arrived as "fire away".

## Cost Estimation

Zero dollars for this brainstorm. The commissioned t0096 literature survey is also $0 (paper
download + reading + writing locally; no remote compute, no paid APIs).

## Step by Step

1. Aggregate project state: tasks, suggestions (uncovered, by priority), costs.
2. Read recent task results: t0090, t0092, t0093, t0094.
3. Form independent priority reassessment of the 10 active high-priority suggestions; identify
   S-0093-01 and S-0074-03 as already covered by completed / planned work.
4. Present state to researcher with metrics, budget, dependency graph, and reassessed priorities.
5. Receive strategic broadening directive: catalogue alternative MOBO objectives via literature
   survey.
6. Three-question clarification: scope (any neuron) / bundling (one consolidated survey) / output
   depth (catalogue + formulas + recipes).
7. Receive explicit confirmation ("fire away").
8. Scaffold `tasks/t0095_brainstorm_results_20/` with the full mandatory folder structure.
9. Invoke `/create-task` with the t0096 description; verify it creates a valid not_started task
   folder with task.json + task_description.md only.
10. Write 2 suggestion-rejection correction files under `corrections/`.
11. Write step logs, session log, results files, plan, research stubs.
12. Capture session transcripts via `capture_task_sessions`.
13. Run verificators (`verify_task_file`, `verify_logs`, `verify_corrections`,
    `verify_suggestions`).
14. Re-run materialiser; format markdown; commit, push, PR, premerge, merge.

## Remote Machines

None for this brainstorm task.

## Assets Needed

None.

## Expected Assets

None. `expected_assets = {}`. The commissioned t0096 will produce its own assets (papers, answer)
when executed.

## Time Estimation

Approximately 25 minutes of interactive discussion plus 15 minutes of scaffolding + correction
authoring + t0096 creation, plus 10 minutes of verification, PR, and merge. Total ~50 minutes
wall-clock.

## Risks & Fallbacks

* **Task index drift mid-session**: parallel session merges another task to main. Mitigation: task
  aggregator was the source of truth at session start; t0091 is the only in-progress task and runs
  in a separate worktree without competing for new task indices.
* **t0096 task description too broad and ambiguous for `/create-task`**: produced a structured
  bullet list of must-find objectives + methodology papers + deliverables to guide the slug and
  task-types extraction.
* **Verificator failures at Phase 6**: fix in place and re-run.
* **Correction-file typos**: caught by `verify_corrections.py`; fix in place before commit.

## Verification Criteria

* `verify_task_file.py t0095_brainstorm_results_20` passes with 0 errors.
* `verify_task_file.py t0096_literature_survey_multi_objective_neuron_optimisation` passes with 0
  errors after creation.
* `verify_logs.py t0095_brainstorm_results_20` passes with 0 errors (LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture).
* `verify_corrections.py t0095_brainstorm_results_20` passes with 0 errors for 2 correction files.
* `verify_suggestions.py t0095_brainstorm_results_20` passes with 0 errors (empty array).
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
