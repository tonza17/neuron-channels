---
spec_version: "1"
task_id: "t0119_brainstorm_results_23"
date_completed: "2026-05-23"
status: "complete"
---
# Results Summary: Brainstorm Session 23

## Summary

Twenty-third strategic brainstorm. Researcher raised a critical concern about the procedural
morphology generator's geometry after inspecting t0115's `top50_morphologies_seed9354.png` (soma
appeared disconnected from dendrite tree in many panels). The session gated the next NSGA-II wave on
a 15-20-cell morphology-geometry audit (t0120), and conditionally commissioned a
biologically-grounded cytoplasm-volume NSGA-II run (t0122, S-0097-01) plus a write-up of the closed
5-seed substrate-rate batch (t0121, S-0115-02). The session also aggressively pruned the
high-priority suggestion backlog: 9 rejections + 21 high-to-medium downgrades (30 corrections
total). Active high-priority suggestions drop from 51 to ~21 after the wave.

## Session Overview

* **Date**: 2026-05-23
* **Trigger**: researcher inspected the t0115 top-50 morphology grid and flagged the
  soma-disconnected-from-dendrites visual artefact as a possible geometry bug that would invalidate
  every 68-d morphology-extended NSGA-II run (t0091, t0099, t0102, t0104, t0106, t0112-t0115) if
  real.
* **Inputs read**: `aggregate_tasks`, `aggregate_suggestions --uncovered`, `aggregate_costs`,
  results summaries for t0112-t0118, t0114's `compare_literature.md`, recent answer assets including
  the t0117 "truncated cohort artefact confirmed" answer, the morphology generator source
  (`tasks/t0090.../code/generator.py`, `tasks/t0092.../code/morphology_generator_fix.py`), and the
  synapse-placement code path (`tasks/t0080.../code/trial_helpers.py`, `trial_driver.py`).
* **No new research, no asset production in this brainstorm task itself**.

## Decisions

1. **Commission `t0120_morph_generator_geometry_audit` (gating diagnostic)**. Sample 15-20
   visually-diverse cells across asymmetry-parameter extremes (high `|soma_offset_pd_um|`, extreme
   `field_elongation_pd`, extreme `branch_density_gradient_pd`, high
   `primary_branch_pd_concentration`) plus symmetric controls. Dump `section_endpoints_xy` and
   NEURON `h.x3d/h.y3d` pt3d. Verify (a) primary stems start at `origin_xy`, (b) parent/child
   endpoints match, (c) synapse-vs-soma coordinate frame consistency. Output: 1 answer asset, 1 PNG
   gallery, 1 CSV pass/fail. Cost <$0.10.

2. **Commission `t0121_5seed_substrate_rate_canonical_report`** (covers S-0115-02). Pure write-up
   consolidating the t0106/t0112/t0113/t0114/t0115 5-seed batch into one canonical document with
   harmonised conventions, 5-seed mean 2.58% +/- SE 1.50%, Hay 2011 / Druckmann 2007 comparisons,
   charts. Cost <$0.20.

3. **Commission `t0122_dsi_cytoplasm_volume_nsga2`** (covers S-0097-01, **gated on t0120 passing**).
   NSGA-II on 68-d Bed B + 14-d morphology substrate, 2-objective (maximise DSI, minimise cytoplasm
   volume per Cuntz 2010), pop=96, N_EVAL_SEEDS=3, auto-stop DISABLED, gen ceiling 60, 1 random GA
   seed via `secrets.randbelow(10000)`. Falsifiable prediction: high-DSI cells in Cuntz's
   balancing-factor `[0.2, 0.7]` band. Cost ~$4-8, $8 cap.

4. **Reject 9 suggestions** as superseded or moot:
   * **S-0106-01** — done by 5-seed batch.
   * **S-0112-02** (cadence isolation), **S-0112-03** (autostop sensitivity) — superseded by
     t0114/t0115.
   * **S-0113-02 + S-0114-07** (dill checkpoint) — deferred to the next NSGA-II driver iteration
     (commissioned implicitly via t0122).
   * **S-0114-01 + S-0115-01** (W=3/T=0.015 plateau defaults) — moot per project's DISABLED
     auto-stop policy.
   * **S-0116-01** (5-seed pool adding t0113) — superseded by t0117 unfiltered analysis.
   * **S-0116-02** (relaxed cohort DSI>0.5) — subsumed by S-0117-01 parametric sweep.

5. **Downgrade 21 pre-t0111 stale highs from high to medium**:
   * **NSGA-II era (post-t0091)**: S-0099-01, S-0099-02, S-0102-01, S-0102-02, S-0102-03, S-0102-04,
     S-0104-01, S-0104-02, S-0104-04, S-0105-01, S-0105-02, S-0105-04, S-0106-02.
   * **Pre-NSGA-II era**: S-0067-01, S-0070-01, S-0074-01, S-0074-02, S-0076-04, S-0086-01,
     S-0090-02, S-0090-03.

6. **Framework infra note** — **S-0116-06** (`verify_answer_asset.py`) remains active high; needs
   to be picked up by the `self-improvement` skill in a future infra session (not handled in this
   brainstorm per CLAUDE.md rule 0).

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
* `verify_corrections t0119_brainstorm_results_23` — **expected PASSED** (0 errors; 30 corrections
  to verify).
* `verify_suggestions t0119_brainstorm_results_23` — **expected PASSED** (no new suggestions this
  session; empty array).
* `verify_logs t0119_brainstorm_results_23` — **expected PASSED** (0 errors; warnings `LG-W005`,
  `LG-W007`, `LG-W008` may be present and are non-blocking for a pure-planning brainstorm).
* `verify_pr_premerge t0119_brainstorm_results_23 --pr-number <N>` — **expected PASSED** before
  merge.

## Next Steps

* **Execute `t0120_morph_generator_geometry_audit` first** -- it gates t0122. ~30 min local.
* **Execute `t0121_5seed_substrate_rate_canonical_report` in parallel** -- independent of t0120. ~1
  hour local.
* **If t0120 passes (rendering-only verdict)**: execute `t0122_dsi_cytoplasm_volume_nsga2` next.
  ~6-12 hours wall-clock on Vast.ai EPYC.
* **If t0120 fails (real geometry bug)**: cancel t0122 and open a follow-up brainstorm session to
  decide whether to patch `_apply_asymmetry` and re-run all 68-d morphology-extended NSGA-II lineage
  tasks (t0091, t0099, t0102, t0104, t0106, t0112-t0115).
* **Future brainstorm should pick up the cohort-artefact follow-ups** that this session
  intentionally deferred: S-0117-01 (DSI sweep), S-0117-02 (per-seed FA), S-0117-03 (bootstrap F1),
  S-0116-03 (topological basin), S-0118-02 (g_I sweep on cluster-2), S-0118-03 (evaluator bug fix),
  plus the S-0103 Baden / Bae / Ran morphology grounding line.
* **Framework infra**: invoke `self-improvement` skill on S-0116-06 (`verify_answer_asset.py`) in a
  separate infrastructure branch.
