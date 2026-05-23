# ✅ Brainstorm results session 23

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0119_brainstorm_results_23` |
| **Status** | ✅ completed |
| **Started** | 2026-05-23T00:00:00Z |
| **Completed** | 2026-05-23T00:00:00Z |
| **Duration** | 0s |
| **Dependencies** | [`t0101_brainstorm_results_21`](../../../overview/tasks/task_pages/t0101_brainstorm_results_21.md), [`t0111_brainstorm_results_22`](../../../overview/tasks/task_pages/t0111_brainstorm_results_22.md), [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md), [`t0113_t0106_seed2247_replicate`](../../../overview/tasks/task_pages/t0113_t0106_seed2247_replicate.md), [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md), [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md), [`t0118_resimulate_t0117_cluster_samples_ge_gi_vm`](../../../overview/tasks/task_pages/t0118_resimulate_t0117_cluster_samples_ge_gi_vm.md) |
| **Task types** | `brainstorming` |
| **Step progress** | 4/4 |
| **Task folder** | [`t0119_brainstorm_results_23/`](../../../tasks/t0119_brainstorm_results_23/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0119_brainstorm_results_23/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0119_brainstorm_results_23/task_description.md)*

# Brainstorm Results Session 23

## Trigger

Researcher inspected the t0115 `top50_morphologies_seed9354.png` morphology grid and flagged
that in several panels the soma appears far from the dendrite tree and not visually connected.
Concern: if the soma is genuinely disconnected from the dendrites (rather than a rendering
artefact), every 68-d morphology-extended NSGA-II result from t0091 onwards (t0091, t0099,
t0102, t0104, t0106, t0112-t0115) could be electrically invalid and would need to be re-run.

## Inputs Read

* Aggregator outputs: `aggregate_tasks`, `aggregate_suggestions --uncovered`,
  `aggregate_costs`.
* Recent task results: `results_summary.md` for t0112, t0113, t0114, t0115, t0116, t0117,
  t0118 and t0114's `compare_literature.md`.
* Generator code: `tasks/t0090_morphology_generator_diversity_test/code/generator.py` (the
  `_apply_asymmetry` transform) and
  `tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py`.
* Synapse-placement code path:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_helpers.py`
  (`_section_midpoint_xy`) and `trial_driver.py` (`_bar_arrival_times`).
* The t0115 top-50 morphology PNG.

## Decisions

1. **Gating diagnostic** — create `t0120_morph_generator_geometry_audit`. Stratified-sample
   15-20 visually-diverse cells across asymmetry-parameter extremes (high
   `|soma_offset_pd_um|`, extreme `field_elongation_pd`, extreme `branch_density_gradient_pd`,
   high `primary_branch_pd_concentration`) plus symmetric controls. Dump full
   `section_endpoints_xy`, NEURON `h.x3d/h.y3d` pt3d, primary-stem origin verification,
   parent/child endpoint match check. Recompute one synapse-arrival projection per cell to
   confirm the synapse-vs-soma coordinate frame is consistent. Output: 1 answer asset, 1 PNG
   gallery, 1 CSV with per-cell pass/fail. Cost <$0.10.

2. **Canonical 5-seed substrate-rate report** — create
   `t0121_5seed_substrate_rate_canonical_report` covering S-0115-02. Pure write-up
   consolidating the t0106 / t0112 / t0113 / t0114 / t0115 5-seed batch into one comparable
   document with harmonised metric conventions, 5-seed mean / SD / SE / 95% CI, per-seed
   acceptance, and the Hay 2011 / Druckmann 2007 baselines. Cost <$0.20.

3. **New NSGA-II optimisation** — create `t0122_dsi_cytoplasm_volume_nsga2` covering
   S-0097-01. Bed B + 14-d morphology substrate, 2-objective NSGA-II maximising DSI and
   minimising cytoplasm volume (per-section pi * d * L summed over soma + dendrites + AIS), 1
   random GA seed, pop=96, N_EVAL_SEEDS=3, HV-plateau auto-stop DISABLED, $8 cap. **Gated on
   t0120 passing.**

4. **Aggressive suggestion cleanup**:
   * **Reject (9)**: S-0106-01, S-0112-02, S-0112-03, S-0113-02, S-0114-01, S-0114-07,
     S-0115-01, S-0116-01, S-0116-02. (S-0113-02 and S-0114-07 reject reason: deferred to next
     NSGA-II driver iteration. S-0114-01, S-0115-01 reject reason: moot per project's
     DISABLED-autostop policy.)
   * **Downgrade high -> medium (21)**: S-0067-01, S-0070-01, S-0074-01, S-0074-02, S-0076-04,
     S-0086-01, S-0090-02, S-0090-03, S-0099-01, S-0099-02, S-0102-01, S-0102-02, S-0102-03,
     S-0102-04, S-0104-01, S-0104-02, S-0104-04, S-0105-01, S-0105-02, S-0105-04, S-0106-02.

5. **Framework infra note** — S-0116-06 (`verify_answer_asset.py`) remains active high; needs
   to be picked up by the `self-improvement` skill in a future infra session (not handled in
   this brainstorm per CLAUDE.md rule 0).

## Out of Scope

* No new research, paper downloads, or experiments in this brainstorm task itself.
* Suggestion creation: only the brainstorm-recording suggestions (none planned).
* All cohort-artefact follow-ups (S-0117-01, S-0117-02, S-0117-03, S-0116-03), S-0118-*
  mechanistic follow-ups, and the dill/autostop NSGA-II driver overhaul are deferred to later
  sessions.

</details>

## Research

* [`research_code.md`](../../../tasks/t0119_brainstorm_results_23/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0119_brainstorm_results_23/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0119_brainstorm_results_23/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0119_brainstorm_results_23/results/results_summary.md)*

--- spec_version: "1" task_id: "t0119_brainstorm_results_23" date_completed: "2026-05-23"
status: "complete" ---
# Results Summary: Brainstorm Session 23

## Summary

Twenty-third strategic brainstorm. Researcher raised a critical concern about the procedural
morphology generator's geometry after inspecting t0115's `top50_morphologies_seed9354.png`
(soma appeared disconnected from dendrite tree in many panels). The session gated the next
NSGA-II wave on a 15-20-cell morphology-geometry audit (t0120), and conditionally commissioned
a biologically-grounded cytoplasm-volume NSGA-II run (t0122, S-0097-01) plus a write-up of the
closed 5-seed substrate-rate batch (t0121, S-0115-02). The session also aggressively pruned
the high-priority suggestion backlog: 9 rejections + 21 high-to-medium downgrades (30
corrections total). Active high-priority suggestions drop from 51 to ~21 after the wave.

## Session Overview

* **Date**: 2026-05-23
* **Trigger**: researcher inspected the t0115 top-50 morphology grid and flagged the
  soma-disconnected-from-dendrites visual artefact as a possible geometry bug that would
  invalidate every 68-d morphology-extended NSGA-II run (t0091, t0099, t0102, t0104, t0106,
  t0112-t0115) if real.
* **Inputs read**: `aggregate_tasks`, `aggregate_suggestions --uncovered`, `aggregate_costs`,
  results summaries for t0112-t0118, t0114's `compare_literature.md`, recent answer assets
  including the t0117 "truncated cohort artefact confirmed" answer, the morphology generator
  source (`tasks/t0090.../code/generator.py`,
  `tasks/t0092.../code/morphology_generator_fix.py`), and the synapse-placement code path
  (`tasks/t0080.../code/trial_helpers.py`, `trial_driver.py`).
* **No new research, no asset production in this brainstorm task itself**.

## Decisions

1. **Commission `t0120_morph_generator_geometry_audit` (gating diagnostic)**. Sample 15-20
   visually-diverse cells across asymmetry-parameter extremes (high `|soma_offset_pd_um|`,
   extreme `field_elongation_pd`, extreme `branch_density_gradient_pd`, high
   `primary_branch_pd_concentration`) plus symmetric controls. Dump `section_endpoints_xy` and
   NEURON `h.x3d/h.y3d` pt3d. Verify (a) primary stems start at `origin_xy`, (b) parent/child
   endpoints match, (c) synapse-vs-soma coordinate frame consistency. Output: 1 answer asset,
   1 PNG gallery, 1 CSV pass/fail. Cost <$0.10.

2. **Commission `t0121_5seed_substrate_rate_canonical_report`** (covers S-0115-02). Pure
   write-up consolidating the t0106/t0112/t0113/t0114/t0115 5-seed batch into one canonical
   document with harmonised conventions, 5-seed mean 2.58% +/- SE 1.50%, Hay 2011 / Druckmann
   2007 comparisons, charts. Cost <$0.20.

3. **Commission `t0122_dsi_cytoplasm_volume_nsga2`** (covers S-0097-01, **gated on t0120
   passing**). NSGA-II on 68-d Bed B + 14-d morphology substrate, 2-objective (maximise DSI,
   minimise cytoplasm volume per Cuntz 2010), pop=96, N_EVAL_SEEDS=3, auto-stop DISABLED, gen
   ceiling 60, 1 random GA seed via `secrets.randbelow(10000)`. Falsifiable prediction:
   high-DSI cells in Cuntz's balancing-factor `[0.2, 0.7]` band. Cost ~$4-8, $8 cap.

4. **Reject 9 suggestions** as superseded or moot:
   * **S-0106-01** — done by 5-seed batch.
   * **S-0112-02** (cadence isolation), **S-0112-03** (autostop sensitivity) — superseded by
     t0114/t0115.
   * **S-0113-02 + S-0114-07** (dill checkpoint) — deferred to the next NSGA-II driver
     iteration (commissioned implicitly via t0122).
   * **S-0114-01 + S-0115-01** (W=3/T=0.015 plateau defaults) — moot per project's DISABLED
     auto-stop policy.
   * **S-0116-01** (5-seed pool adding t0113) — superseded by t0117 unfiltered analysis.
   * **S-0116-02** (relaxed cohort DSI>0.5) — subsumed by S-0117-01 parametric sweep.

5. **Downgrade 21 pre-t0111 stale highs from high to medium**:
   * **NSGA-II era (post-t0091)**: S-0099-01, S-0099-02, S-0102-01, S-0102-02, S-0102-03,
     S-0102-04, S-0104-01, S-0104-02, S-0104-04, S-0105-01, S-0105-02, S-0105-04, S-0106-02.
   * **Pre-NSGA-II era**: S-0067-01, S-0070-01, S-0074-01, S-0074-02, S-0076-04, S-0086-01,
     S-0090-02, S-0090-03.

6. **Framework infra note** — **S-0116-06** (`verify_answer_asset.py`) remains active high;
   needs to be picked up by the `self-improvement` skill in a future infra session (not
   handled in this brainstorm per CLAUDE.md rule 0).

## Metrics

| Item | Count |
| --- | --- |
| New tasks created | 3 |
| Suggestions rejected | 9 |
| Suggestions reprioritised (high -> medium) | 21 |
| Corrections written | 30 |
| Suggestions kept at high | 12 |
| Active high-priority suggestions before wave | 51 |
| Active high-priority suggestions after wave | 21 (12 carried over + ~9 dependency tasks that remain or are added) |
| Tasks cancelled | 0 |
| Tasks updated (existing) | 0 |
| Answer assets produced by this task | 0 |
| Budget committed by this wave | ~$5-9 of $37 remaining |

## Verification

* `verify_task_file t0119_brainstorm_results_23` — **expected PASSED** (0 errors).
* `verify_corrections t0119_brainstorm_results_23` — **expected PASSED** (0 errors; 30
  corrections to verify).
* `verify_suggestions t0119_brainstorm_results_23` — **expected PASSED** (no new suggestions
  this session; empty array).
* `verify_logs t0119_brainstorm_results_23` — **expected PASSED** (0 errors; warnings
  `LG-W005`, `LG-W007`, `LG-W008` may be present and are non-blocking for a pure-planning
  brainstorm).
* `verify_pr_premerge t0119_brainstorm_results_23 --pr-number <N>` — **expected PASSED**
  before merge.

## Next Steps

* **Execute `t0120_morph_generator_geometry_audit` first** -- it gates t0122. ~30 min local.
* **Execute `t0121_5seed_substrate_rate_canonical_report` in parallel** -- independent of
  t0120. ~1 hour local.
* **If t0120 passes (rendering-only verdict)**: execute `t0122_dsi_cytoplasm_volume_nsga2`
  next. ~6-12 hours wall-clock on Vast.ai EPYC.
* **If t0120 fails (real geometry bug)**: cancel t0122 and open a follow-up brainstorm session
  to decide whether to patch `_apply_asymmetry` and re-run all 68-d morphology-extended
  NSGA-II lineage tasks (t0091, t0099, t0102, t0104, t0106, t0112-t0115).
* **Future brainstorm should pick up the cohort-artefact follow-ups** that this session
  intentionally deferred: S-0117-01 (DSI sweep), S-0117-02 (per-seed FA), S-0117-03 (bootstrap
  F1), S-0116-03 (topological basin), S-0118-02 (g_I sweep on cluster-2), S-0118-03 (evaluator
  bug fix), plus the S-0103 Baden / Bae / Ran morphology grounding line.
* **Framework infra**: invoke `self-improvement` skill on S-0116-06 (`verify_answer_asset.py`)
  in a separate infrastructure branch.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0119_brainstorm_results_23/results/results_detailed.md)*

--- spec_version: "1" task_id: "t0119_brainstorm_results_23" date_completed: "2026-05-23"
status: "complete" ---
# Results Detailed: Brainstorm Session 23

## Summary

Twenty-third strategic brainstorm. Researcher raised a critical concern about the procedural
morphology generator's geometry after inspecting t0115's `top50_morphologies_seed9354.png`
(soma appeared disconnected from dendrite tree in many panels). The session gated the next
NSGA-II wave on a 15-20-cell morphology-geometry audit (t0120), and conditionally commissioned
a biologically-grounded cytoplasm-volume NSGA-II run (t0122, S-0097-01) plus a write-up of the
closed 5-seed substrate-rate batch (t0121, S-0115-02). The session also aggressively pruned
the high-priority suggestion backlog: 9 rejections + 21 downgrades (30 correction files).

## Methodology

1. **Phase 1 (Review project state)**:
   * Ran `aggregate_tasks --format json --detail short` (119 tasks).
   * Ran `aggregate_suggestions --format json --detail short --uncovered` (372 active
     uncovered; 51 high, 261 medium, 60 low) and `--detail full --priority high` (51 highs
     read in full).
   * Ran `aggregate_costs --format json --detail short` ($62.90 / $100 spent; $37.10 left; no
     thresholds tripped).
   * Read `results/results_summary.md` for t0112, t0113, t0114, t0115, t0116, t0117, t0118.
   * Read `results/compare_literature.md` for t0114.
   * Read the recent answer asset
     `t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-truncated-cohort-artefact-test/short_answer.md`.
   * Ran the overview materialiser (`arf.scripts.overview.materialize`).
   * Formed an independent priority reassessment grouping suggestions into top-priority,
     superseded, and stale.

2. **Phase 1.5 / 2 (Discuss decisions, with morphology diversion)**:
   * Researcher interrupted the standard 4-question clarification with the morphology-geometry
     concern.
   * AI traced the generator code path end-to-end:
     `tasks/t0090_morphology_generator_diversity_test/code/generator.py` `_apply_asymmetry`
     (lines 333-355), `_materialise_neuron_sections` (lines 358-505), `generate_morphology`
     (line 584),
     `tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py`,
     `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_helpers.py`
     `_section_midpoint_xy` (line 160) and synapse-placement (lines 244-310),
     `tasks/t0080.../code/trial_driver.py` `_bar_arrival_times`.
   * Confirmed: NEURON electrical topology is `sec.connect()`-based and indifferent to xy;
     synapse pt3d xy and `origin_xy` come from the same `pt3dadd` calls in
     `_materialise_neuron_sections`; the bar-arrival projection `(syn_xy - origin_xy)` is in a
     self-consistent frame.
   * Preliminary verdict: most likely a rendering / auto-zoom visual artefact, but needs
     empirical verification before next NSGA-II runs.
   * Researcher chose: morphology audit as gating task with 15-20 visually-diverse cells (not
     5), then proceed with new optimisation if audit passes.
   * Round 1: proposed t0120 (audit), t0121 (5-seed canonical report, S-0115-02), t0122
     (cytoplasm-volume NSGA-II, S-0097-01).
   * Round 2: proposed aggressive cleanup (9 rejects + 21 downgrades).
   * Round 3: researcher confirmed.

3. **Phase 3-4 (Create brainstorm task)**:
   * Created branch `task/t0119_brainstorm_results_23` from `main`.
   * Created full brainstorm task folder structure (per
     `arf/specifications/task_file_specification.md` and the brainstorm skill spec).
   * Wrote `task.json` (spec_version 4, status "completed", `expected_assets={}`),
     `task_description.md`, `step_tracker.json` (4 steps), `plan/plan.md`, 3 research
     placeholders, placeholders for `results/metrics.json` (`{}`), `costs.json` (zero),
     `remote_machines_used.json` (`[]`), `suggestions.json` (empty array), the 4 step logs,
     `logs/session_log.md`, and `.gitkeep` placeholders.

4. **Phase 5 (Apply decisions)**:
   * Created 3 child tasks with task.json + task_description.md only (no subdirectories per
     create-task skill spec):
     * `t0120_morph_generator_geometry_audit`
     * `t0121_5seed_substrate_rate_canonical_report`
     * `t0122_dsi_cytoplasm_volume_nsga2`
   * Wrote 30 correction files using a generator script
     (`C:\Users\md1avn\AppData\Local\Temp\write_corrections.py`): 9 rejections
     (`suggestion_S-*.json` with `action="update"`, `changes={"status": "rejected"}`) and 21
     downgrades (`changes={"priority": "medium"}`). Per-suggestion rationale documents the
     specific superseding task or policy decision.

5. **Phase 6 (Record and finalize)** (this section):
   * Wrote `results_summary.md` and `results_detailed.md`.
   * Captured CLI session transcripts via `arf.scripts.utils.capture_task_sessions --task-id
     t0119_brainstorm_results_23`.
   * Ran `flowmark --inplace --nobackup` on all edited markdown files.
   * Ran the four mandatory verificators: `verify_task_file`, `verify_corrections`,
     `verify_suggestions`, `verify_logs`.
   * Re-ran the overview materialiser so corrections show in `overview/`.
   * Committed, pushed `task/t0119_brainstorm_results_23`, opened PR, ran
     `verify_pr_premerge`, merged with a merge commit (not squash).

## Metrics

| Item | Count |
| --- | --- |
| Tasks aggregated | 119 |
| Suggestions aggregated (uncovered) | 372 |
| High-priority suggestions read in full | 51 |
| Source-task results summaries read | 7 (t0112-t0118) |
| Source-task compare_literature.md read | 1 (t0114) |
| Answer assets read | 1 (t0117 truncated-cohort artefact test) |
| New tasks created | 3 |
| Correction files written | 30 (9 rejections + 21 downgrades) |
| Suggestions kept at high after wave | 12 |
| Suggestions deferred to future sessions (still active) | ~349 |
| Budget committed by this wave | ~$5-9 |
| Budget left after this wave is executed | ~$28-32 of original $100 |

## Limitations

* This is a planning task, no experiments run.
* The morphology-geometry concern is being resolved by a separate task (t0120). The brainstorm
  itself only commissions the diagnostic; it does not run it.
* Aggressive cleanup involves judgement calls. The 21 high-to-medium downgrades remain
  reversible via further corrections in any future brainstorm; if a downgraded suggestion
  turns out to still be load-bearing, a future task can re-promote it.

## Files Created

* `tasks/t0119_brainstorm_results_23/__init__.py`
* `tasks/t0119_brainstorm_results_23/task.json`
* `tasks/t0119_brainstorm_results_23/task_description.md`
* `tasks/t0119_brainstorm_results_23/step_tracker.json`
* `tasks/t0119_brainstorm_results_23/plan/plan.md`
* `tasks/t0119_brainstorm_results_23/research/research_papers.md`
* `tasks/t0119_brainstorm_results_23/research/research_internet.md`
* `tasks/t0119_brainstorm_results_23/research/research_code.md`
* `tasks/t0119_brainstorm_results_23/assets/.gitkeep`
* `tasks/t0119_brainstorm_results_23/intervention/.gitkeep`
* `tasks/t0119_brainstorm_results_23/results/results_summary.md` (this batch)
* `tasks/t0119_brainstorm_results_23/results/results_detailed.md` (this file)
* `tasks/t0119_brainstorm_results_23/results/metrics.json`
* `tasks/t0119_brainstorm_results_23/results/suggestions.json`
* `tasks/t0119_brainstorm_results_23/results/costs.json`
* `tasks/t0119_brainstorm_results_23/results/remote_machines_used.json`
* `tasks/t0119_brainstorm_results_23/logs/session_log.md`
* `tasks/t0119_brainstorm_results_23/logs/commands/.gitkeep`
* `tasks/t0119_brainstorm_results_23/logs/searches/.gitkeep`
* `tasks/t0119_brainstorm_results_23/logs/sessions/.gitkeep`
* `tasks/t0119_brainstorm_results_23/logs/steps/001_review-project-state/step_log.md`
* `tasks/t0119_brainstorm_results_23/logs/steps/002_discuss-decisions/step_log.md`
* `tasks/t0119_brainstorm_results_23/logs/steps/003_apply-decisions/step_log.md`
* `tasks/t0119_brainstorm_results_23/logs/steps/004_finalize/step_log.md`
* `tasks/t0119_brainstorm_results_23/corrections/suggestion_S-*.json` (30 files)
* `tasks/t0120_morph_generator_geometry_audit/task.json`
* `tasks/t0120_morph_generator_geometry_audit/task_description.md`
* `tasks/t0121_5seed_substrate_rate_canonical_report/task.json`
* `tasks/t0121_5seed_substrate_rate_canonical_report/task_description.md`
* `tasks/t0122_dsi_cytoplasm_volume_nsga2/task.json`
* `tasks/t0122_dsi_cytoplasm_volume_nsga2/task_description.md`

## Verification

* `verify_task_file t0119_brainstorm_results_23` -- PASSED
* `verify_corrections t0119_brainstorm_results_23` -- PASSED (30 corrections)
* `verify_suggestions t0119_brainstorm_results_23` -- PASSED (empty array intentional)
* `verify_logs t0119_brainstorm_results_23` -- PASSED (LG-W005, LG-W007, LG-W008 may appear
  and are expected for a pure-planning brainstorm)
* `verify_pr_premerge t0119_brainstorm_results_23 --pr-number <N>` -- PASSED before merge

</details>
