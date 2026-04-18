# Plan: Brainstorm Results Session 1

## Objective

Translate `project/description.md` and its five research questions into a concrete first wave of
tasks that the researcher can execute autonomously, and record all decisions made in the session.

## Approach

Run the `/human-brainstorm` skill interactively. Aggregate project state, ask clarifying questions,
propose initial tasks, iterate with the researcher, and then create the agreed task folders.

## Cost Estimation

No external cost. The session uses local LLM CLI time only; no paid APIs or remote compute.

## Step by Step

1. Aggregate tasks, suggestions, costs, answers to show project state.
2. Ask the researcher clarifying questions about morphology, target curve source, simulator choice,
   survey scope, and execution autonomy.
3. Propose a first wave of tasks, iterate to agreement.
4. Create brainstorm-results task folder and child task folders.
5. Write session log, step logs, results files.
6. Run verificators, create PR, merge.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None produced by this task directly. Four child task folders are created as a side effect and
tracked via the tasks aggregator, not as assets.

## Time Estimation

One interactive session; under one hour of researcher time.

## Risks & Fallbacks

* **Researcher rejects all proposed tasks**: restart the proposal round with narrower scope.
* **Verificators fail**: fix errors and re-run; do not merge until all pass.

## Verification Criteria

* `verify_task_file` passes on `t0001_brainstorm_results_1` and on each child task folder.
* `verify_logs` passes on `t0001_brainstorm_results_1`.
* `verify_corrections` and `verify_suggestions` pass (no corrections or suggestions produced this
  session).
* Pre-merge verificator passes before the PR is merged.
