# ✅ Brainstorm results session 22

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0111_brainstorm_results_22` |
| **Status** | ✅ completed |
| **Started** | 2026-05-19T00:00:00Z |
| **Completed** | 2026-05-19T00:00:00Z |
| **Duration** | 0s |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0094_brainstorm_results_19`](../../../overview/tasks/task_pages/t0094_brainstorm_results_19.md), [`t0095_brainstorm_results_20`](../../../overview/tasks/task_pages/t0095_brainstorm_results_20.md), [`t0101_brainstorm_results_21`](../../../overview/tasks/task_pages/t0101_brainstorm_results_21.md), [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0107_t0106_polar_8dir_recheck`](../../../overview/tasks/task_pages/t0107_t0106_polar_8dir_recheck.md), [`t0108_t0106_cluster_factor_dsi05_pd10`](../../../overview/tasks/task_pages/t0108_t0106_cluster_factor_dsi05_pd10.md), [`t0109_t0108_morph_cluster_gallery`](../../../overview/tasks/task_pages/t0109_t0108_morph_cluster_gallery.md), [`t0110_relaxed_cohort_factor_analysis`](../../../overview/tasks/task_pages/t0110_relaxed_cohort_factor_analysis.md) |
| **Task types** | `brainstorming` |
| **Step progress** | 4/4 |
| **Task folder** | [`t0111_brainstorm_results_22/`](../../../tasks/t0111_brainstorm_results_22/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0111_brainstorm_results_22/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0111_brainstorm_results_22/task_description.md)*

# Brainstorm Session 22: Seed-77 Replicate of t0106 Joint-Pass Breakthrough

## Context

t0106 achieved the first joint-pass cells (DSI >= 0.5 AND PD-rate >= 30 Hz) in the entire
t0080 -> t0104 NSGA-II lineage: 123 unique cells across 3,744 evaluations from a single
random-init GA seed (44) over 40 generations on the 68-d Bed B + 14-d morphology substrate.
The breakthrough was driven by switching from 16-direction vector-sum DSI to 2-direction ratio
DSI rather than by additional compute. t0107 immediately followed with an 8-direction polar
re-evaluation of 10 random top-50 cells, showing that the absolute DSI numbers fall sharply
under the conventional 8-direction protocol (mean t0106 ratio DSI = 0.939 vs t0107 8-dir
vector-sum DSI = 0.519) while rank order is preserved (Spearman rho = 0.758).

The open question this brainstorm addresses: is the t0106 result a seed-specific lucky run, or
is the joint-pass corner genuinely populated on this substrate? Without seed-replication, the
headline "123 unique joint-pass cells" cannot be claimed in any writeup as a substrate
property; it is at best a single-realisation point estimate.

## Decisions

A single new task `t0112_t0106_seed77_replicate` is commissioned: a minimum-change t0106
replicate that varies only the GA seed (44 -> 77) and the multiprocessing pool restart cadence
(`_POOL_RESTART_EVERY` 25 -> 10 generations, motivated by NEURON's known memory creep). All
other parameters are held identical to t0106: pop=96, N_EVAL_SEEDS=3, N_DIRECTIONS=2, ratio
DSI objective, random LHS init, HV-plateau operator-stop criterion. Gen ceiling raised to 60
(from t0106's 300) so a slower plateau is not artificially cut while keeping the budget
bounded.

No suggestion rejections, reprioritisations, or task cancellations were applied in this
session. The 325 uncovered suggestions remain at their current priorities pending the t0112
outcome, which will either promote the suggestion backlog (if the replicate confirms substrate
population) or trigger a different next-wave plan (if it does not).

## Expected Outcomes

Two qualitatively distinct outcomes are possible from t0112:

1. **Replicate succeeds** (>= 40 unique joint-pass cells at the strict DSI >= 0.5 AND PD >= 30
   Hz threshold): t0106 is confirmed as a substrate-population effect, not a seed-specific
   artefact. This promotes downstream analysis tasks (8-dir polar re-evaluation of all
   joint-pass cells, cluster + factor analysis extension, mechanism dissection) to high
   priority.

2. **Replicate fails** (substantially fewer joint-pass cells, or zero): the joint-pass
   acceptance rate has wide seed-variance; multi-seed replication and / or alternative
   optimiser (IBEA, Dang2023 mu = n log n NSGA-II) must precede any literature claim.

In either case, the result feeds the next brainstorm session's strategic direction.

## Budget

* This brainstorm task: $0 (planning only)
* Commissioned task t0112: $25 cost cap; expected actual ~$10-11 mirroring t0106
* Project envelope: $18.20 remaining of $75 prior to this session; ~$7-8 reserve after t0112
  spend

</details>

## Research

* [`research_code.md`](../../../tasks/t0111_brainstorm_results_22/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0111_brainstorm_results_22/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0111_brainstorm_results_22/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0111_brainstorm_results_22/results/results_summary.md)*

--- spec_version: "1" task_id: "t0111_brainstorm_results_22" date_completed: "2026-05-19"
status: "complete" ---

# Results Summary: Brainstorm Session 22 — Seed-77 Replicate of t0106

## Summary

Twenty-second strategic brainstorm. The researcher opened with a specific direction (replicate
t0106 at a fresh seed, with a tighter NEURON pool-restart cadence), which the session
converged on as a single minimum-change task: `t0112_t0106_seed77_replicate`. No corrections,
reprioritisations, or task cancellations were applied.

## Session Overview

* **Date**: 2026-05-19
* **Trigger**: researcher's read of the t0106 -> t0110 wave, with t0106 producing the first
  joint-pass cells in the entire t0080 -> t0104 lineage (123 unique cells, DSI >= 0.5 AND PD
  >= 30 Hz) on a single GA seed and t0107 showing that the absolute DSI numbers fall sharply
  under conventional 8-direction protocol (mean DSI = 0.519 vs t0106's 0.939) while rank order
  was preserved.
* **Inputs read**: `aggregate_tasks`, `aggregate_suggestions --uncovered`, `aggregate_costs`,
  results summaries for t0106 - t0110 and `t0105_preliminary_figures_report`, t0106
  `compare_literature.md`, recent answer assets, and
  `tasks/t0106_long_pdnd_nsga2_300gen/code/` (`constants.py` and `nsga2_driver.py`) for the
  exact run configuration.
* **No new research, no asset production** — pure decision-recording.

## Decisions

1. **Commission `t0112_t0106_seed77_replicate`**. Substrate identical to t0106 (68-d Bed B +
   14-d morphology, pop=96, N_EVAL_SEEDS=3, N_DIRECTIONS=2, ratio DSI, random LHS init,
   HV-plateau operator-stop). Only changes from t0106:
   * GA seed: 77 (vs t0106's 44; chosen as unused across the project's NSGA-II history).
   * `_POOL_RESTART_EVERY`: 10 generations (vs t0106's 25), motivated by NEURON memory creep
     reported in the t0106 logs.
   * Gen ceiling: 60 (vs t0106's 300, which never bound) so a slower plateau is not
     artificially cut while keeping the budget bounded.
   * Cost cap: $25 (same per-task cap); expected actual ~$10-11 mirroring t0106.
   * Source suggestion: none. Generates a follow-up suggestion from its own
     `results/suggestions.json`.

2. **No suggestion rejections, reprioritisations, or task cancellations**. The 325 uncovered
   suggestions (31 high, 241 medium, 53 low) remain at their current priorities pending the
   t0112 outcome. A proposal to reprioritise four high-priority items (S-0106-01, S-0102-03,
   S-0102-04, S-0104-04) to medium was put to the researcher and declined; cleanup is deferred
   to the next brainstorm.

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
* `verify_suggestions t0111_brainstorm_results_22` — PASSED (0 errors; empty suggestions
  list).
* `verify_logs t0111_brainstorm_results_22` — PASSED (0 errors; `TS-W001` and `LG-W005`
  expected and accepted for the brainstorm flow).
* `verify_pr_premerge t0111_brainstorm_results_22 --pr-number <N>` — PASSED before merge.

## Next Steps

* Execute `t0112_t0106_seed77_replicate` next. Single seed, ~$10 expected.
* Defer all suggestion-cleanup work to the next brainstorm. The t0112 result will dictate
  which follow-ups remain load-bearing.
* If t0112 reproduces the t0106 joint-pass yield within order of magnitude, the next wave
  should prioritise (a) 8-direction polar re-evaluation of all joint-pass cells across t0106 +
  t0112 combined, and (b) extension of t0108 / t0110 cluster + factor analysis to the larger
  cohort.
* If t0112 substantially under-produces, the next wave should pivot to multi-seed and / or
  alternative-optimiser comparisons (IBEA, Dang2023 mu = n log n NSGA-II) before any
  literature claim.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0111_brainstorm_results_22/results/results_detailed.md)*

--- spec_version: "1" task_id: "t0111_brainstorm_results_22" date_completed: "2026-05-19"
status: "complete" ---

# Results Detailed: Brainstorm Session 22

## Summary

Twenty-second strategic brainstorm. Single decision: commission
`t0112_t0106_seed77_replicate`, a minimum-change replicate of t0106 varying only the GA seed
(44 -> 77) and the multiprocessing pool restart cadence (`_POOL_RESTART_EVERY` 25 -> 10
generations) to test whether the t0106 joint-pass breakthrough is seed-specific or
substrate-general.

## Methodology

1. **Aggregate**: ran `aggregate_tasks --format json --detail short`, `aggregate_suggestions
   --format json --detail short --uncovered`, and `aggregate_costs --format json --detail
   short`. Populations: 111 tasks (103 completed, 1 intervention_blocked, 2 not_started, 5
   cancelled); 325 uncovered suggestions (31 high, 241 medium, 53 low); $56.80 of $75 spent
   (75.7%), $18.20 remaining.
2. **Read recent results**: `results_summary.md` for t0106 - t0110 and
   `t0105_preliminary_figures_report`; `compare_literature.md` for t0106; three recent answer
   assets (t0106 joint-pass-recovery, t0108 strict-cohort factor decomposition, t0110 PD
   correlation sign-flip).
3. **Inspect non-completed tasks**: `t0023_port_hanson_2019_dsgc` (intervention_blocked),
   `t0031_fetch_paywalled_morphology_papers` (not_started),
   `t0075_bio_realistic_ais_param_sweep` (not_started).
4. **Materialise overview**: ran `arf.scripts.overview.materialize` to update `overview/` for
   GitHub browsing.
5. **Independent priority reassessment**: re-evaluated the 31 high-priority suggestions
   against the t0106 + t0107 + t0108 + t0110 findings. Identified four candidates for high ->
   medium reprioritisation (S-0106-01, S-0102-03, S-0102-04, S-0104-04).
6. **Round 1 (new tasks)**: proposed `t0112_t0106_seed77_replicate` after inspecting
   `tasks/t0106_long_pdnd_nsga2_300gen/code/nsga2_driver.py:97` (`_POOL_RESTART_EVERY = 25`),
   `constants.py:58` (`T0106_SEEDS = (44,)`), and the t0106 results to quote settings exactly.
   Researcher chose seed 77, HV-plateau stop with gen ceiling 60, and minimum-change
   otherwise.
7. **Round 2 (suggestion cleanup)**: presented the 4-suggestion reprioritisation proposal.
   Researcher chose to skip cleanup.
8. **Round 3 (confirmation)**: summarised the final decision list and obtained authorisation
   to proceed through merge.
9. **Phase 4 - 6**: created the brainstorm task folder, invoked `/create-task` for t0112,
   wrote the session transcript and step logs, captured CLI sessions, ran verificators,
   materialised the overview, committed, pushed, opened the PR, ran pre-merge verificator,
   merged.

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

## Limitations

Planning task, no experiments run. All scientific claims (the t0106 breakthrough, the t0107
metric-artefact caveat, the t0108 morphology-cluster dominance, the t0110 truncation-artifact
correction) are inherited from the cited tasks and not re-validated in this session.

## Files Created

* `tasks/t0111_brainstorm_results_22/__init__.py`
* `tasks/t0111_brainstorm_results_22/task.json`
* `tasks/t0111_brainstorm_results_22/task_description.md`
* `tasks/t0111_brainstorm_results_22/step_tracker.json`
* `tasks/t0111_brainstorm_results_22/plan/plan.md`
* `tasks/t0111_brainstorm_results_22/research/research_papers.md`
* `tasks/t0111_brainstorm_results_22/research/research_internet.md`
* `tasks/t0111_brainstorm_results_22/research/research_code.md`
* `tasks/t0111_brainstorm_results_22/assets/.gitkeep`
* `tasks/t0111_brainstorm_results_22/intervention/.gitkeep`
* `tasks/t0111_brainstorm_results_22/results/results_summary.md`
* `tasks/t0111_brainstorm_results_22/results/results_detailed.md`
* `tasks/t0111_brainstorm_results_22/results/metrics.json`
* `tasks/t0111_brainstorm_results_22/results/costs.json`
* `tasks/t0111_brainstorm_results_22/results/remote_machines_used.json`
* `tasks/t0111_brainstorm_results_22/results/suggestions.json`
* `tasks/t0111_brainstorm_results_22/logs/session_log.md`
* `tasks/t0111_brainstorm_results_22/logs/sessions/capture_report.json` (+ optional captured
  `.jsonl` files when available)
* `tasks/t0111_brainstorm_results_22/logs/steps/001_review-project-state/step_log.md`
* `tasks/t0111_brainstorm_results_22/logs/steps/002_discuss-decisions/step_log.md`
* `tasks/t0111_brainstorm_results_22/logs/steps/003_apply-decisions/step_log.md`
* `tasks/t0111_brainstorm_results_22/logs/steps/004_finalize/step_log.md`
* `tasks/t0112_t0106_seed77_replicate/task.json`
* `tasks/t0112_t0106_seed77_replicate/task_description.md`

## Verification

* `verify_task_file t0111_brainstorm_results_22` — PASSED, 0 errors.
* `verify_corrections t0111_brainstorm_results_22` — PASSED, 0 errors.
* `verify_suggestions t0111_brainstorm_results_22` — PASSED, 0 errors.
* `verify_logs t0111_brainstorm_results_22` — PASSED, 0 errors (`TS-W001` and `LG-W005`
  warnings expected and accepted for the brainstorm flow).
* `verify_pr_premerge t0111_brainstorm_results_22 --pr-number <N>` — PASSED before merge.

</details>
