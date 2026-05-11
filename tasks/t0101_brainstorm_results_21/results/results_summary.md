---
spec_version: "1"
task_id: "t0101_brainstorm_results_21"
date_completed: "2026-05-11"
status: "complete"
---
# Results Summary: Brainstorm Session 21 — Poleg-Polsky 2026 Deep-Dive

## Summary

Twenty-first strategic brainstorm, triggered by a researcher request to extract numerical specs from
Poleg-Polsky 2026 (`10.1038/s41467-026-70288-4`) and compare them against our NSGA-II / MOBO
history. The session (a) read seven concrete answers directly from the PDF, (b) flagged several
fabricated claims in our existing `summary.md`, (c) commissioned a follow-up NSGA-II task
`t0102_seedscale_n4_gen20` at GA-seeds=2 / N_SEEDS=4 / gens=20 on the 68-d substrate, and (d)
recorded the project-budget bump from 20 -> 35 USD (per-task 5 -> 8) that was committed to main
prior to the brainstorm task.

## Session Overview

* **Date**: 2026-05-11
* **Trigger**: researcher's seven-question deep-dive into Poleg-Polsky 2026 followed by an explicit
  ask to commission a follow-up NSGA-II run that mirrors PP's seed/generation balance.
* **Inputs read**:
  `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/files/polegpolsky_2026_ml-motion-primitives.pdf`,
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants.py`, and the `results_summary.md`
  of t0078 / t0080 / t0081 / t0083 / t0091 / t0099.
* **No new research, no asset production** — pure decision-recording.

## Decisions

1. **Commission t0102_seedscale_n4_gen20**. Substrate: 68-d joint electrophys+morphology (same as
   t0091, t0099). GA seeds: 2 (random init, seeds 44 and 55 to avoid overlap with t0099's 11/22/33).
   `N_SEEDS`: 4 (reduced from 20 by factor of 5). Generations: 20. Population: 96 (default). Cost
   cap: $8. Rationale: tests whether dropping noise replicates 5x and extending generations 2.5x
   recovers t0099's null result on the joint-pass corner without warm-start.

2. **Raise project budget** from $20 -> $35 total, $5 -> $8 per-task default (committed directly to
   main in commit `dd9ac77f` prior to this brainstorm task). Rationale: project was already 119.5%
   of original ceiling after t0099; t0102 plus expected future runs need an honest envelope.

3. **Three new suggestions recorded** (all forward-creating, none rejected):
   * `S-0101-01` (high, evaluation): correct fabricated content in PP-2026 `summary.md` via the
     corrections mechanism. The summary.md lists a wrong title, fabricated novel primitives ("NMDA
     multiplicative gating", "velocity-dependent coincidence detection", "distance-graded delay
     lines"), and fabricated search axes ("A-type potassium density") none of which appear in the
     published paper.
   * `S-0101-02` (medium, library): if t0102 reproduces t0099 DSI/PD scatter at N_SEEDS=4, lower the
     project-wide default in `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants.py:43`
     and propagate via the corrections mechanism.
   * `S-0101-03` (medium, experiment): PP-style ablation — budget-matched comparison of (a) 2
     seeds x pop=96 x 100 gens vs (b) 20 seeds x pop=10 x 100 gens on the same 68-d substrate.

4. **No suggestion rejections**, **no task cancellations**, **no reprioritisations** in this
   brainstorm. The active backlog from t0099 (S-0099-01 through S-0099-04) is preserved.

## Metrics

| Item | Count |
| --- | --- |
| New tasks created | 1 |
| New suggestions recorded | 3 |
| Suggestions rejected | 0 |
| Suggestions reprioritised | 0 |
| Tasks cancelled | 0 |
| Corrections written | 0 |
| Answer assets produced | 0 |

## Verification

* `verify_task_file t0101_brainstorm_results_21` — PASSED (run during Phase 6).
* `verify_corrections t0101_brainstorm_results_21` — PASSED (no correction files in this
  brainstorm).
* `verify_suggestions t0101_brainstorm_results_21` — PASSED (3 new suggestions validate against
  the suggestions spec).
* `verify_logs t0101_brainstorm_results_21` — PASSED with expected `TS-W001` (custom step names
  for brainstorm flow) and `LG-W005` (no wrapped command logs).

## Next Steps

1. Create `t0102_seedscale_n4_gen20` task folder on its own branch immediately after this brainstorm
   merges (per the framework's "one task = one branch" rule).
2. Execute `t0102` via the `/execute-task` skill to land the NSGA-II run on Vast.ai within the $8
   per-task cap.
3. Pick up `S-0101-01` as the next high-priority correction task once t0102 completes (it does not
   block t0102 since the correction only affects the PP-2026 asset, not the NSGA-II substrate).
