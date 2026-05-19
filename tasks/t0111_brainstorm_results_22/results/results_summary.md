---
spec_version: "1"
task_id: "t0111_brainstorm_results_22"
date_completed: "2026-05-19"
status: "complete"
---
# Results Summary: Brainstorm Session 22 — Seed-77 Replicate of t0106

## Summary

Twenty-second strategic brainstorm. The researcher opened with a specific direction (replicate t0106
at a fresh seed, with a tighter NEURON pool-restart cadence), which the session converged on as a
single minimum-change task: `t0112_t0106_seed77_replicate`. No corrections, reprioritisations, or
task cancellations were applied.

## Session Overview

* **Date**: 2026-05-19
* **Trigger**: researcher's read of the t0106 -> t0110 wave, with t0106 producing the first
  joint-pass cells in the entire t0080 -> t0104 lineage (123 unique cells, DSI >= 0.5 AND PD >= 30
  Hz) on a single GA seed and t0107 showing that the absolute DSI numbers fall sharply under
  conventional 8-direction protocol (mean DSI = 0.519 vs t0106's 0.939) while rank order was
  preserved.
* **Inputs read**: `aggregate_tasks`, `aggregate_suggestions --uncovered`, `aggregate_costs`,
  results summaries for t0106 - t0110 and `t0105_preliminary_figures_report`, t0106
  `compare_literature.md`, recent answer assets, and `tasks/t0106_long_pdnd_nsga2_300gen/code/`
  (`constants.py` and `nsga2_driver.py`) for the exact run configuration.
* **No new research, no asset production** — pure decision-recording.

## Decisions

1. **Commission `t0112_t0106_seed77_replicate`**. Substrate identical to t0106 (68-d Bed B + 14-d
   morphology, pop=96, N_EVAL_SEEDS=3, N_DIRECTIONS=2, ratio DSI, random LHS init, HV-plateau
   operator-stop). Only changes from t0106:
   * GA seed: 77 (vs t0106's 44; chosen as unused across the project's NSGA-II history).
   * `_POOL_RESTART_EVERY`: 10 generations (vs t0106's 25), motivated by NEURON memory creep
     reported in the t0106 logs.
   * Gen ceiling: 60 (vs t0106's 300, which never bound) so a slower plateau is not artificially cut
     while keeping the budget bounded.
   * Cost cap: $25 (same per-task cap); expected actual ~$10-11 mirroring t0106.
   * Source suggestion: none. Generates a follow-up suggestion from its own
     `results/suggestions.json`.

2. **No suggestion rejections, reprioritisations, or task cancellations**. The 325 uncovered
   suggestions (31 high, 241 medium, 53 low) remain at their current priorities pending the t0112
   outcome. A proposal to reprioritise four high-priority items (S-0106-01, S-0102-03, S-0102-04,
   S-0104-04) to medium was put to the researcher and declined; cleanup is deferred to the next
   brainstorm.

## Metrics

| Item | Count |
| --- | --- |
| New tasks created | 1 |
| Suggestions new | 0 |
| Suggestions rejected | 0 |
| Suggestions reprioritised | 0 |
| Tasks cancelled | 0 |
| Tasks updated | 0 |
| Corrections written | 0 |
| Answer assets produced | 0 |

## Verification

* `verify_task_file t0111_brainstorm_results_22` — PASSED (0 errors).
* `verify_corrections t0111_brainstorm_results_22` — PASSED (0 errors; no corrections this
  session).
* `verify_suggestions t0111_brainstorm_results_22` — PASSED (0 errors; empty suggestions list).
* `verify_logs t0111_brainstorm_results_22` — PASSED (0 errors; `TS-W001` and `LG-W005` expected
  and accepted for the brainstorm flow).
* `verify_pr_premerge t0111_brainstorm_results_22 --pr-number <N>` — PASSED before merge.

## Next Steps

* Execute `t0112_t0106_seed77_replicate` next. Single seed, ~$10 expected.
* Defer all suggestion-cleanup work to the next brainstorm. The t0112 result will dictate which
  follow-ups remain load-bearing.
* If t0112 reproduces the t0106 joint-pass yield within order of magnitude, the next wave should
  prioritise (a) 8-direction polar re-evaluation of all joint-pass cells across t0106 + t0112
  combined, and (b) extension of t0108 / t0110 cluster + factor analysis to the larger cohort.
* If t0112 substantially under-produces, the next wave should pivot to multi-seed and / or
  alternative-optimiser comparisons (IBEA, Dang2023 mu = n log n NSGA-II) before any literature
  claim.
