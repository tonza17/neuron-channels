# ⏳ 68-d NSGA-II at GA seeds=2, N_SEEDS=4, gens=20, random init

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0102_seedscale_n4_gen20` |
| **Status** | ⏳ in_progress |
| **Started** | 2026-05-11T14:08:37Z |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md), [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md), [`t0101_brainstorm_results_21`](../../../overview/tasks/task_pages/t0101_brainstorm_results_21.md) |
| **Task types** | `experiment-run`, `data-analysis`, `answer-question` |
| **Expected assets** | 2 predictions, 1 answer |
| **Task folder** | [`t0102_seedscale_n4_gen20/`](../../../tasks/t0102_seedscale_n4_gen20/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source: [`task_description.md`](../../../tasks/t0102_seedscale_n4_gen20/task_description.md)*

# t0102 — 68-d NSGA-II at GA seeds=2, N_SEEDS=4, gens=20, random init

## Context

Commissioned by t0101 (brainstorm session 21) after a Poleg-Polsky 2026 deep-dive showed PP
runs 50-100 independent GA-restart seeds at pop=10, 300-1000 generations, while our convention
is 1-3 seeds at pop=24-96, 8-17 generations. t0099 ran 3 random-init seeds (11/22/33) at
pop=96, 5-8 generations, N_SEEDS=20 and produced **zero strict joint-pass cells across 55
Pareto cells**, demonstrating that the t0091 5-anchor warm-start was load-bearing for the
joint-pass corner.

This task rebalances the budget toward PP's seed/generation profile while staying on our 68-d
substrate (54-d electrophys + 14-d morphology):

* **GA seeds**: 2 (random-init, seeds 44 and 55 — no overlap with t0099's 11/22/33).
* **Noise replicates `N_SEEDS`**: 4 (reduced from 20 by factor of 5).
* **Generations**: 20 (up from t0099's 5-8).
* **Population**: 96 (default).
* **Warm-start**: none — purely random LHS-sampled initial populations like t0099.

## Goal

Test the hypothesis: at constant Vast.ai budget, replacing 20 within-cell noise replicates
with 4 and extending generations 2.5x recovers the joint-pass corner of objective space
without needing the warm-start that t0091 used. If it does, we have a cheaper recipe for
NSGA-II on this substrate; if it does not, the warm-start was the load-bearing ingredient.

## Approach

Use `tasks/t0099_random_init_pareto_robustness/code/run_loop.py` as the substrate (literally —
same 68-d evaluation pipeline, same morphology generator, same evaluation library) but
override two parameters and one count:

1. **`N_SEEDS` constant override**: import-shadow the value from t0080's `constants.py` inside
   the t0102 driver so the substrate is unmodified but the per-cell evaluation uses 4
   trial-seeds. Validate that the substrate-consistency smoke gate (REQ-7 in t0081) still
   passes within widened tolerance for the lower replicate count.
2. **NSGA-II generations**: set `n_gen = 20` in the pymoo driver.
3. **GA seeds**: run two NSGA-II processes with `seed=44` and `seed=55` (LHS-init), pop=96
   each, on the **same Vast.ai instance, sequentially** (not parallel; one instance is enough
   since total wall-clock at 5x cheaper eval should fit in ~20 hours).

Output one predictions asset per seed (96 init + 20 gens x 96 = 2 016 cells per seed) plus one
answer asset comparing t0102 vs t0099 vs t0091 on (DSI, PD, joint-pass count, robustness,
anchor distribution).

## Cost Estimation

| Item | Estimate |
| --- | --- |
| Vast.ai instance | $0.24/hr (RTX 4090 / EPYC 7B13 64-core, same as t0099) |
| Per-cell eval at N=4 | ~5x faster than t0099's N=20 |
| Cells per seed | 96 + 20 x 96 = 2 016 |
| Cells total | 4 032 |
| Wall-clock estimate | ~20-25 hours (4 032 cells x ~18 s = ~20 h) |
| **Predicted spend** | **~$5-6** |
| **Hard cost cap** | **$8** (per-task limit after 2026-05-11 budget bump) |

## Step by Step

Canonical step IDs from `arf/specifications/task_steps_specification.md`:

1. `preflight` — verify dependencies completed; smoke-test that t0099's pipeline runs locally
   on one cell with `N_SEEDS=4`.
2. `research-papers` — re-read Poleg-Polsky 2026 Methods on seed/generation balance; document
   the PP-2026 numbers in `research/research_papers.md`.
3. `research-code` — audit `tasks/t0080_*/code/`, `tasks/t0099_*/code/`, and the morphology
   generator at `tasks/t0090_*/code/` to confirm the substrate is reusable verbatim.
4. `planning` — produce `plan/plan.md` with the exact cost / time / risk table; agree
   REQ-1..REQ-N.
5. `setup-machines` — provision one Vast.ai instance; record `machine_log.json`.
6. `implementation` —
   * 6a. SCP code to instance.
   * 6b. Run substrate-consistency smoke gate at N_SEEDS=4 (REQ-7-equivalent).
   * 6c. Run NSGA-II seed=44, pop=96, gens=20.
   * 6d. Run NSGA-II seed=55, pop=96, gens=20.
   * 6e. Pull predictions back, build per-seed predictions assets.
7. `destroy-machines` — Vast.ai instance teardown; record final cost.
8. `analysis` — clustering, anchor distribution, hypervolume curves, joint-pass tally;
   side-by-side comparison plots vs t0091 / t0099.
9. `reporting` — write `results/results_summary.md`, `results/results_detailed.md`, embed
   plots in `results/images/`, populate `metrics.json` and `suggestions.json`.

## Remote Machines

One Vast.ai instance, matching t0099's spec:

* GPU tier: not required (NEURON is CPU-bound)
* CPU: AMD EPYC 7B13, 64 effective cores
* RAM: 503 GB (default)
* Location: Norway preferred (consistent with t0099 pricing $0.24/hr)
* Hard runtime cap: 30 hours per `tasks/t0099_*/results/results_summary.md` `RM-W003` envelope

## Assets Needed

* Substrate: `tasks/t0024_port_de_rosenroll_2026_dsgc` Bed B compartmental model
* Driver: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/`
* NSGA-II loop: `tasks/t0099_random_init_pareto_robustness/code/run_loop.py`
* Morphology generator: `tasks/t0093_resweep_and_t0090_correction/code/` (post-patch)
* Anchor / clustering: `tasks/t0086_robustness_cluster_bio_comparison/code/`

## Expected Assets

* 2 predictions assets (one per seed, 2 016 cells each).
* 1 answer asset: "Does N_SEEDS=4 + gens=20 + 2 random-init seeds recover joint-pass corner?"

## Time Estimation

* Local prep + smoke + provisioning: 1-2 h
* Vast.ai NSGA-II runs (2 seeds sequential): 18-24 h
* Analysis + reporting: 3-4 h
* **Total wall-clock**: 22-30 h.

## Risks & Fallbacks

* **Risk**: per-cell DSI/PD variance at N_SEEDS=4 is so high that NSGA-II selection becomes
  random, yielding no joint-pass cells regardless of generation count. **Fallback**: in the
  analysis step, recompute DSI/PD on a held-out set of high-Pareto cells at N_SEEDS=20 and
  report the variance gap. If gap > 1 SD on either axis, declare N_SEEDS=4 too noisy and
  recommend N_SEEDS=8 in a follow-up.

* **Risk**: per-seed wall-clock grows super-linearly due to NEURON memory accumulation (a
  known failure pattern from t0099 `S-0099-04`). **Fallback**: restart Python worker between
  generations (S-0099-04 suggestion). If still too slow, cut second seed at gen 15.

* **Risk**: Vast.ai instance fails to provision in $0.24/hr range; takes >$0.40/hr instead.
  **Fallback**: still under $8 cap if wall-clock stays within 20 hours.

* **Risk**: t0090 / t0093 morphology generator silently produces empty trees again.
  **Fallback**: smoke gate REQ-7-equivalent must pass before committing to long run.

## Verification Criteria

* `verify_task_metrics t0102_seedscale_n4_gen20` passes with 0 errors.
* `verify_machines_destroyed t0102_seedscale_n4_gen20` confirms Vast.ai instance is destroyed.
* `verify_research_code t0102_seedscale_n4_gen20` and `verify_plan t0102_seedscale_n4_gen20`
  pass.
* Both predictions assets validate.
* Total cost in `results/costs.json` does not exceed $8.00.
* At least one of the following is true (positive or negative result both publishable):
  - **Positive**: >= 1 strict joint-pass cell (DSI >= 0.5, PD >= 30 Hz, robustness >= 0.7)
    found in at least one seed.
  - **Negative**: 0 strict joint-pass cells in either seed, confirming t0099's null result is
    robust to the seed/generation re-balance.

## Out of Scope

* Modifying `tasks/t0080_*/code/constants.py` N_SEEDS default (deferred suggestion S-0101-02).
* Correcting Poleg-Polsky 2026 `summary.md` (deferred suggestion S-0101-01).
* Few-seeds-many-gens vs many-seeds-few-gens budget-matched ablation (deferred suggestion
  S-0101-03).
* Adding new biological mechanisms or expanding the search space beyond the 68-d substrate.

</details>
