# Plan: Brainstorm Results Session 2

## Objective

Translate the outputs of the first task wave (t0002-t0005) and the researcher's three-step
high-level goal (install NEURON+NetPyNE → port ModelDB 189347 and siblings → hunt missed models →
add visualisation and scoring libraries) into a concrete second wave of tasks, and record all
session decisions.

## Approach

Run the `/human-brainstorm` skill interactively. Aggregate project state, reassess all active
suggestions against completed-task findings, propose new tasks, iterate with the researcher, and
create the agreed task folders plus correction files.

## Cost Estimation

No external cost. Local LLM CLI time only.

## Step by Step

1. Aggregate tasks, suggestions, costs, answers; read `results_summary.md` for every completed task
   since the last brainstorm.
2. Independently reassess all active suggestions against what completed tasks actually produced
   (quantitative targets from t0002, simulator choice from t0003, target curve from t0004,
   morphology from t0005).
3. Propose second-wave tasks and iterate with the researcher.
4. Record researcher preferences: t0008 must use calibrated morphology (→ t0009 dependency), t0011
   smoke-tests against both target-tuning-curve and t0008 output, implement proper scoring library
   (t0012) rather than inline ad-hoc checks.
5. Write this brainstorm-results task folder and seven child task folders (t0007-t0013).
6. File correction files to reject S-0004-03 (redundant with S-0002-09 → t0012) and reprioritise
   S-0005-04 from HIGH to MEDIUM (deferred until at least one sim pipeline exists).
7. Run verificators, create PR, merge.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None produced by this task directly. Seven child task folders (t0007-t0013) are created as a side
effect and tracked via the tasks aggregator, not as assets.

## Time Estimation

One interactive session; approximately 90 minutes of researcher time.

## Risks & Fallbacks

* **Researcher rejects a proposed task**: drop it from the batch; keep the rest.
* **Verificators fail**: fix errors and re-run; do not merge until all pass.
* **Dependency cycle introduced between child tasks**: re-examine the dependency graph before
  writing `task.json` files; resolve by splitting or reordering.

## Verification Criteria

* `verify_task_file` passes on `t0006_brainstorm_results_2` and on each child task folder
  (t0007-t0013).
* `verify_logs` passes on `t0006_brainstorm_results_2`.
* `verify_corrections` passes on the two correction files written this session.
* `verify_suggestions` passes (no new suggestions produced this session).
* `verify_pr_premerge` passes before the PR is merged.
