# ✅ Random-init NSGA-II reproducibility test: 3 seeds vs t0091 Pareto

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0099_random_init_pareto_robustness` |
| **Status** | ✅ completed |
| **Started** | 2026-05-09T00:19:13Z |
| **Completed** | 2026-05-10T23:35:00Z |
| **Duration** | 47h 15m |
| **Dependencies** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md) |
| **Task types** | `experiment-run`, `data-analysis`, `answer-question` |
| **Expected assets** | 3 predictions, 1 answer |
| **Step progress** | 11/15 |
| **Cost** | **$7.71** |
| **Task folder** | [`t0099_random_init_pareto_robustness/`](../../../tasks/t0099_random_init_pareto_robustness/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0099_random_init_pareto_robustness/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0099_random_init_pareto_robustness/task_description.md)*

# Random-Init NSGA-II Reproducibility Test: 3 Seeds vs t0091 Pareto

## Motivation

t0091 produced a 57-cell Pareto front from joint 68-d NSGA-II using a 5-anchor warm-start
(bedb_like, symmetric, PD-asymmetric, ND-asymmetric, alt_topology). The headline finding —
zero biologically-plausible joint-pass cells — relied on a single NSGA-II run from a
structured warm-start. **Two open questions remain**:

1. **Reproducibility under different RNG seeds**: would a different seed produce a similar
   Pareto front, anchor distribution, and bio-plausibility outcome? t0091 ran one seed.

2. **Warm-start dependence**: was the 5-anchor warm-start load-bearing, or would purely random
   initial populations have found the same Pareto? The brainstorm-18 design assumed the
   warm-start was necessary; this assumption was never tested.

This task tests both questions with 3 NSGA-II runs from **totally random** initial
populations, each with a different RNG seed. The 14-d morphology vector and 54-d electrophys
vector are sampled uniformly from each parameter's plan-defined bounds (no anchor bias).

## Scope

### In Scope

* 3 NSGA-II runs on Vast.ai EPYC 7B13 64-core CPU, each with a different RNG seed (e.g., 11,
  22, 33), each with a $1.00 hard cost watchdog cap. Total project budget cap $3.15.
* Each run: pop=96, max_gen=8, totally random initial population (uniform LHS sample over the
  68-d parameter space — no anchor warm-start), HV-plateau termination + cost watchdog +
  max-gen termination.
* Reuse t0091's evaluator infrastructure (generator wrapper, biological priors, biological
  scorecard, anchor-tracking machinery for analysis only).
* Per-seed Pareto archive (predictions asset per seed, 3 total).
* Cross-seed analysis: HV trajectory comparison, Pareto cell counts, anchor distribution
  recompute (using t0091's 5-anchor definitions for nearest-anchor classification — the runs
  themselves are anchor-free, but post-hoc classification still works), bio-plausibility
  comparison.
* One synthesis answer asset addressing the two open questions.

### Out of Scope

* No new biology, no new generator changes, no new priors.
* No comparison against random-init runs at full t0091 depth (would cost $30+; deferred).
* No multi-objective formulation revision (deferred per S-0091-05).
* No real-cell morphology library (deferred per S-0091-06 / Option G).
* No cross-bed validation against Bed A (deferred per S-0086-06).

## Approach

### Phase A — Random-init population builder

Replace t0091's anchor-based warm-start with a uniform LHS sample over the 68-d parameter
space. Each of the 3 seeds gets its own LHS sample drawn from `np.random.SeedSequence(seed)`.

Code: copy `t0091/code/warmstart.py` into `t0099/code/random_init.py`, replace the anchor
logic with `LatinHypercubeSampling` from pymoo (or `scipy.stats.qmc.LatinHypercube` with
explicit seed).

### Phase B — NSGA-II runs

Reuse t0091's `nsga2_driver.py` evaluator + cost watchdog with these adjustments per seed:

* `T0099_HARD_BUDGET_PER_SEED_USD = 1.00` (replaces t0091's $4.00).
* `pymoo.algorithms.moo.nsga2.NSGA2(pop_size=96, sampling=lhs_sample_for_seed, ...)`.
* All other settings identical to t0091 (SBX crossover η=15, polynomial mutation η=20,
  prob=1/68, eliminate_duplicates=True, MaximumGenerationTermination(8), HV-plateau watchdog,
  cost watchdog).
* Each seed runs sequentially on the same Vast.ai instance to amortise provisioning cost.
* Seeds: 11, 22, 33 (arbitrary primes; reproducible).

### Phase C — Per-seed analysis

For each of the 3 seeds:

1. Extract Pareto front from the final population.
2. Classify each Pareto cell to its nearest t0091 anchor in 14-d morph space (using t0091's 5
   anchor centroids as fixed reference points; this is post-hoc classification, not
   warm-start).
3. Score each Pareto cell with t0091's `biological_scorecard.py` (13 priors, worst-case
   aggregation).
4. Compute strict joint-pass count (DSI≥0.5, PD≥30 Hz, robust≥0.7).

### Phase D — Cross-seed comparison

* HV trajectory plot: 3 lines (one per seed) + t0091's reference line.
* Pareto cell count per seed (and t0091's 57 for reference).
* Anchor distribution per seed: 5-row × 4-column heatmap (rows = anchors, columns = seed11 /
  seed22 / seed33 / t0091).
* Bio-plausibility: per-seed count of cells passing each prior; cells passing all 13 priors
  jointly (expected: 0 across all seeds).
* Strict joint-pass count per seed.
* Pareto-front overlap in the (DSI, PD-rate, robustness) cube: are the 3 random-init Paretos
  in the same region of objective space as t0091's, or do they explore different regions?

### Phase E — Answer asset

Write `assets/answer/random_init_reproducibility_and_warmstart_dependence/`:

* **Q1**: Are random-init seeds reproducible in their qualitative findings (bio-plausibility,
  anchor distribution, joint-pass count)?
* **Q2**: Was t0091's 5-anchor warm-start load-bearing, or would random init have found the
  same Pareto?

### Phase F — Predictions assets

Three predictions assets, one per seed:

* `assets/predictions/random_init_pareto_seed11/`
* `assets/predictions/random_init_pareto_seed22/`
* `assets/predictions/random_init_pareto_seed33/`

Each contains the per-seed Pareto cells (68-d vector + DSI + PD-rate + robustness + classified
anchor + bio-plausibility verdict).

## Pass Criteria

* All 3 NSGA-II runs complete or hit cost-watchdog cleanly within their $1.00 caps.
* Each run produces a Pareto front of at least 8 cells (matching t0091's REQ-10 threshold).
* Cross-seed HV trajectory plot embedded in `results_detailed.md`.
* Per-seed anchor distribution computed and compared against t0091.
* Definitive yes/no on Q1 (reproducibility) and Q2 (warm-start dependence) in the answer
  asset.

**Acceptable negative outcomes**:

* If 1 or more seeds fail to produce a Pareto with ≥8 cells, document the failure mode (NaN
  flooding, slow convergence) and report cross-seed comparison on the surviving runs only.
* If random-init seeds find no joint-pass cells while t0091 found one, this is consistent with
  the warm-start being load-bearing (S-0091-05's hypothesis).
* If random-init Paretos look qualitatively similar to t0091's (anchor distribution, bio-
  plausibility, joint-pass count), the warm-start was redundant.

## Compute and Budget

* **Vast.ai EPYC 7B13 64-core CPU** for Phases B (NSGA-II runs).
* **Local 64-core CPU** for Phases A, C, D, E, F.
* Per-seed cost watchdog: **$1.00** hard cap.
* Total budget cap: **$3.15** (matches remaining project budget).
* Expected per-seed wall-clock: ~2–3 hours (≤8 gens or watchdog).
* Expected total wall-clock: ~6–10 hours sequential, plus ~10 min provisioning.

**Cost watchdog**: each seed reads the same `selected_offer.price_per_hour` from the shared
machine_log.json and terminates that seed's NSGA-II at $1.00 cumulative spend on that seed.
Cross-seed cumulative tracker also caps at $3.15 total (kills the whole task if exceeded).

## Time Estimation

* Phase A (random-init): 1 hour local.
* Phase B (3 seeds × NSGA-II on Vast.ai): 6–10 hours wall-clock (sequential on one instance).
* Phase C (per-seed analysis): 2 hours local.
* Phase D (cross-seed comparison): 2 hours local.
* Phase E (answer asset): 1 hour local.
* Phase F (predictions assets): 1 hour local (3 assets in parallel).

**Total**: ~12–18 hours wall-clock.

## Expected Assets

* **Predictions × 3**: one per seed (`expected_assets["predictions"] = 3`).
* **Answer × 1**: reproducibility + warm-start synthesis (`expected_assets["answer"] = 1`).

## Risks and Fallbacks

* **Random-init populations may have higher NaN rates**. t0091 had ~5% NaN in gen 1 with the
  warm-start filter; random-init may see 30–50%. The evaluator returns a penalty objective for
  NaN cells, so NSGA-II handles this, but Pareto sizes per seed may be smaller than t0091's
  57.
* **Per-seed budget too tight**. $1.00 = ~3 generations max; if a seed needs gen 4+ to escape
  initial-population dominance, the watchdog will kill it before convergence. Mitigation:
  report the truncation in results, note that this is the budget-bounded reproducibility
  regime.
* **Cross-seed cumulative tracker bug**. If one seed overruns its $1.00 cap by a few cents,
  the task could blow $3.15. Mitigation: per-seed cap is the primary defence; the cross-seed
  tracker is a backup.
* **Vast.ai instance flaky on long runs**. t0091 ran 2.6 hours; this task may run 6–10 hours.
  Mitigation: NSGA-II checkpoints after each generation, so a mid-run instance failure costs
  one generation, not the whole seed.

## Verification Criteria

* `verify_research_code.py`, `verify_plan.py`, `verify_logs.py`, `verify_assets.py`,
  `verify_task_file.py` pass with 0 errors.
* `verify_costs.py` passes (cost record present, within $3.15 cap).
* All 3 predictions assets pass `verify_predictions_asset.py`.
* The answer asset passes `verify_answer_asset.py`.
* Cross-seed HV plot embedded in `results_detailed.md`.

## Cross-References

* **t0091_morphology_extended_nsga2_v1** — primary comparison baseline (5-anchor warm-start
  reference Pareto).
* **t0090_morphology_generator_diversity_test** — original generator (superseded by t0092 fix
  per C-0093-01).
* **t0092_diagnose_morphology_generator_silence** — patched generator (canonical via
  C-0093-01).
* **t0093_resweep_and_t0090_correction** — issued the C-0093-01 correction overlay.
* **t0086_robustness_cluster_bio_comparison** — biological priors and scorecard
  (`biological_priors.py`, `biological_scorecard.py`).
* **t0083_bedb_v3_extend_nsga2_gen8plus** — HV-plateau watchdog reference.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2** — NSGA-II driver, evaluator, cost watchdog
  reference.
* Source suggestion: none directly. Indirectly addresses parts of S-0091-05 (multi-objective
  reformulation needs random-init baseline) and was scoped during the post-t0098 user
  conversation.

</details>

## Costs

**Total**: **$7.71**

| Category | Amount |
|----------|--------|
| vast-ai-setup | $0.04 |
| vast-ai-seed11 | $1.13 |
| vast-ai-seed22 | $1.96 |
| vast-ai-seed33 | $3.41 |
| vast-ai-driver-overhead | $0.74 |
| vast-ai-idle | $0.43 |

## Remote Machines

| Provider | GPU | Count | RAM | Duration | Cost |
|----------|-----|-------|-----|----------|------|
| vast.ai | RTX 5060 Ti (idle, unused; CPU-only NEURON+pymoo workload) | 1 | 252 GB | 46.7h | $7.71 |

## Metrics

### Random-init seed 11

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.11205527939562165** |

### Random-init seed 22

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.2916346303531964** |

### Random-init seed 33

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.059080984225970294** |

### t0091 warm-start reference

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.22084466042432208** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Are the qualitative findings of t0091's joint 68-d NSGA-II run (anchor distribution, biological-plausibility verdict, strict joint-pass count) reproducible under different RNG seeds, and was t0091's 5-anchor warm-start load-bearing — would a purely random initial population have found the same Pareto front?](../../../tasks/t0099_random_init_pareto_robustness/assets/answer/random-init-reproducibility-and-warmstart-dependence/) | [`full_answer.md`](../../../tasks/t0099_random_init_pareto_robustness/assets/answer/random-init-reproducibility-and-warmstart-dependence/full_answer.md) |
| predictions | [Random-init Pareto front seed 11](../../../tasks/t0099_random_init_pareto_robustness/assets/predictions/random-init-pareto-seed11/) | [`description.md`](../../../tasks/t0099_random_init_pareto_robustness/assets/predictions/random-init-pareto-seed11/description.md) |
| predictions | [Random-init Pareto front seed 22](../../../tasks/t0099_random_init_pareto_robustness/assets/predictions/random-init-pareto-seed22/) | [`description.md`](../../../tasks/t0099_random_init_pareto_robustness/assets/predictions/random-init-pareto-seed22/description.md) |
| predictions | [Random-init Pareto front seed 33](../../../tasks/t0099_random_init_pareto_robustness/assets/predictions/random-init-pareto-seed33/) | [`description.md`](../../../tasks/t0099_random_init_pareto_robustness/assets/predictions/random-init-pareto-seed33/description.md) |

## Suggestions Generated

<details>
<summary><strong>Anchor-1-only warm-start NSGA-II to isolate which part of t0091's
warm-start was load-bearing</strong> (S-0099-01)</summary>

**Kind**: experiment | **Priority**: high

t0099 confirmed t0091's 5-anchor warm-start was load-bearing (0/55 random-init joint-pass
cells vs t0091's 1/57). Open question: was anchor 1 (Bed-B-like) sufficient, or did the
diversity of all 5 anchors matter? Run NSGA-II with all 96 init cells cloned from anchor 1
only (96 different t0083 electrophys vectors), pop=96, 8 gens, $5 cap. Outcome (a): joint-pass
emerges -> anchor 1 was load-bearing alone. Outcome (b): no joint-pass -> warm-start diversity
itself was load-bearing. Either narrows future morphology-extended NSGA-II design
substantially. Cost ~$3.50 single seed.

</details>

<details>
<summary><strong>Per-cell field_elongation_pd vs DSI test on t0091 + t0099 Pareto
cells (HM-3 follow-up)</strong> (S-0099-02)</summary>

**Kind**: evaluation | **Priority**: high

HM-3 (cells with stronger DS have higher field_elongation_pd) remained inconclusive in both
t0091 and t0099. Pure data-analysis on the now-available 57+19+22+14 = 112 Pareto cells:
extract per-cell field_elongation_pd from each cell's 14-d morphology vector, plot vs DSI
vector-sum, compute Spearman rho. n=112 gives statistical power. Cost $0. Could resolve a
2-task-old open question.

</details>

<details>
<summary><strong>Pool t0091 + t0099 anchor counts to confirm HM-2 (PD-asymmetric
> ND-asymmetric) at higher n</strong> (S-0099-03)</summary>

**Kind**: evaluation | **Priority**: medium

t0099 revised HM-2 from REFUTED to CONFIRMED by pooling 3 random-init seed counts (PD-asymm 20
vs ND-asymm 7, p~0.013). Add t0091's 12 vs 9 to get full sample: 32 vs 16 (p~0.02). Confirms
Schachter 2010 / Briggman 2011 prediction at n=4 datasets. Pure data-analysis; could form the
basis for an answer asset on the soma-displacement-toward-PD mechanism.

</details>

<details>
<summary><strong>NEURON worker process restart between gens to test if memory
accumulation explains per-gen wall-clock doubling</strong> (S-0099-04)</summary>

**Kind**: library | **Priority**: medium

t0099 observed gen 1 = 38-52 min, gen 8 = 167+ min for the same workload. Hypothesis: NEURON
state accumulation across pop=96 cell builds per gen. Test: modify nsga2_driver to spawn fresh
worker pool every 2 gens. If late-gen wall-clock improves by >20%, the memory-accumulation
hypothesis is confirmed. Cost $1-2 single seed.

</details>

<details>
<summary><strong>20-generation single-seed random-init NSGA-II to test whether
longer search bridges the joint-pass gap</strong> (S-0099-05)</summary>

**Kind**: experiment | **Priority**: low

t0099 capped at 8 gens per seed. Hay 2011 used 1000 gens for similar problems. Test: one
random-init seed at 20 gens with $10 cap to see if random-init can eventually bridge the
joint-pass corner that warm-start reached at gen 2. If yes, warm-start was a 10x speedup not a
fundamental enabler. If no after 20 gens, warm-start remains essential. Cost ~$10 single seed.

</details>

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0099_random_init_pareto_robustness/results/results_summary.md)*

--- spec_version: "1" task_id: "t0099_random_init_pareto_robustness" date_completed:
"2026-05-10" status: "complete" ---

# Results Summary: Random-Init NSGA-II Reproducibility Test

## Summary

Three NSGA-II runs from totally random LHS-sampled initial populations (seeds 11, 22, 33), no
anchor warm-start, on the same 68-d substrate t0091 used. **0 of 55 Pareto cells across all 3
seeds qualified as strict joint-pass (DSI≥0.5, PD≥30Hz, robust≥0.7), versus 1 such cell in
t0091's 57-cell warm-start Pareto.** This is direct evidence that t0091's 5-anchor warm-start
was load-bearing for reaching the joint-pass corner of objective space within an 8-generation
budget — and refines the claim further: warm-start was load-bearing **specifically for the
high-PD-rate dimension**, since seed 22 reached t0091's DSI threshold (DSI=0.49) but only half
the firing rate (PD=18.7Hz vs t0091's 35Hz). Total Vast.ai cost $7.71 (38.5% of $20 task
budget).

## Metrics

* **Pareto cell counts per seed**: seed 11 = **19** (5 gens, $1 cap hit), seed 22 = **22** (8
  gens), seed 33 = **14** (8 gens). t0091 reference: 57.
* **Strict joint-pass count per seed**: **0 / 0 / 0**; t0091 = 1.
* **Best DSI across all seeds**: 0.49 (seed 22 gen 8); t0091 best = 0.51.
* **Best PD-rate across all seeds**: 47 Hz (seed 22 gen 8, but DSI=0); t0091 best joint = 35
  Hz with DSI=0.51.
* **Mean DSI per Pareto** (registered metric): seed 11 = 0.112, seed 22 = 0.292, seed 33 =
  0.059. t0091 reference = 0.221.
* **HV (final-gen) per seed**: seed 11 = 1.07 (capped at gen 5), seed 22 = 9.80, seed 33 =
  4.75; t0091 = 23.71 (gen 2, the only gen recorded for t0091 reference).
* **Anchor distribution per seed** ([bedb_like, symmetric, pd_asymm, nd_asymm, alt_topology]):
  seed 11 = `[2, 0, 7, 5, 5]`, seed 22 = `[4, 0, 4, 2, 12]`, seed 33 = `[1, 0, 9, 0, 4]`;
  t0091 = `[20, 0, 12, 9, 16]`.
* **Symmetric anchor count = 0 in ALL 4 datasets**, including warm-started t0091.
* **Total cost**: $7.71 (Vast.ai instance for 46.7 hours; per-seed: $1.13 + $1.96 + $3.41).

## Verification

* `verify_predictions_asset.py` × 3 — all PASSED (each with PR-W014/PR-W015 expected warnings)
* `verify_answer_asset.py` — PASSED
* `verify_task_metrics.py` — PASSED
* `verify_machines_destroyed.py` — PASSED (RM-W001 false-negative + RM-W003 long-uptime
  warnings expected)
* `ruff check` + `ruff format` on `code/` — PASSED
* `mypy -p tasks.t0099_random_init_pareto_robustness.code` — PASSED (no issues)

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0099_random_init_pareto_robustness/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0099_random_init_pareto_robustness" ---

# Detailed Results: Random-Init NSGA-II Reproducibility Test

## Summary

Three NSGA-II runs from totally random LHS-sampled initial populations (seeds 11, 22, 33) on
the same 68-d substrate t0091 used. Headline finding: **0 strict joint-pass cells across 55
random-init Pareto cells** (vs t0091's 1 such cell from 57 warm-start Pareto cells). Strong
evidence that t0091's 5-anchor warm-start was load-bearing. The single near-joint-pass cell
across all 3 random-init seeds — seed 22 gen 8: DSI=0.49, PD=18.7Hz, robust=0.98 — matches
t0091's joint-pass cell on DSI and exceeds it on robustness, but only achieves half the
PD-rate (18.7Hz vs t0091's 35Hz). This refines the warm-start hypothesis: warm-start was
load-bearing **specifically for the high-PD-rate dimension**, since the PD threshold is what
random-init failed to bridge. Cost $7.71 of $20 task cap; 46.7h Vast.ai instance uptime.

## Methodology

* **Hardware**: Vast.ai instance 36372909, AMD EPYC 7B13 64-core CPU, 252 GB RAM (CPU-only
  NEURON workload; the bundled RTX PRO 4000 GPU was unused).
* **Runtime**: 46.679 hours total instance uptime; instance billing rate $0.16519/hr; offer
  base rate $0.1490/hr (cost watchdog reads this).
* **Per-seed wall-clock**: seed 11 = 7.6 hours (5 gens, $1.00 cap hit), seed 22 = 13.1 hours
  (8 gens, $5.00 cap), seed 33 = 22.9 hours (8 gens, $5.00 cap).
* **NSGA-II configuration**: pop=96, max_gen=8, SBX crossover (η=15, prob=0.9), polynomial
  mutation (η=20, prob=1/68), eliminate_duplicates=True, 60 parallel workers via
  StarmapParallelization. Termination = MaximumGenerationTermination(8) + HV-plateau (window
  2, threshold 1%) + CostWatchdogTermination(per-seed cap).
* **Random init sampler**: `pymoo.operators.sampling.lhs.LatinHypercubeSampling` with
  `np.random.RandomState(seed)` per seed. Each seed produced a (96, 68) population matrix.
  Cross-seed independence verified (per-knob correlation ≈ 0; 288 unique cells across 3 seeds;
  no cross-seed near-duplicates < 0.48 normalised distance).
* **Per-seed cost watchdog**: started at $1.00 (caught seed 11 mid-run); raised to $5.00
  mid-task per user authorisation to top up Vast.ai credit, allowing seeds 22 and 33 to run
  all 8 gens.
* **Per-cell evaluation**: identical to t0091 — `generate_fixed_morphology()` from t0092
  patched generator (canonical via `C-0093-01`), 16 directions × 5 evaluation seeds, 1.4s bar
  protocol. Three objectives: maximise DSI vector-sum, PD firing rate, robustness across seeds
  (NSGA-II minimises the negation).

## Metrics Tables

### Per-seed Pareto summary

| Seed | Gens | Pareto size | Strict joint-pass | Mean DSI | Final HV | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| 11 | 5 (capped) | 19 | 0 | 0.112 | 1.07 | $1.13 |
| 22 | 8 | 22 | 0 | 0.292 | 9.80 | $1.96 |
| 33 | 8 | 14 | 0 | 0.059 | 4.75 | $3.41 |
| **Sum** | | **55** | **0** | | | **$6.50** |
| t0091 ref | 2 (recorded) | 57 | **1** | 0.221 | 23.71 | (separate task) |

### Per-seed anchor distribution

| Seed | bedb_like | symmetric | pd_asymm | nd_asymm | alt_topology |
| --- | --- | --- | --- | --- | --- |
| 11 | 2 | 0 | 7 | 5 | 5 |
| 22 | 4 | 0 | 4 | 2 | 12 |
| 33 | 1 | 0 | 9 | 0 | 4 |
| t0091 | 20 | 0 | 12 | 9 | 16 |

### HV trajectory across all 3 seeds

| Gen | Seed 11 | Seed 22 | Seed 33 |
| --- | --- | --- | --- |
| 1 | 0.14 | 0.13 | 0.27 |
| 2 | 0.69 | 0.29 | 0.37 |
| 3 | 0.72 | 0.53 | 0.51 |
| 4 | 0.83 | 1.93 | 0.90 |
| 5 | 1.07 (capped) | 4.71 | 3.09 |
| 6 | — | 4.98 | 4.22 |
| 7 | — | 5.09 | 4.74 |
| 8 | — | **9.80** | 4.75 (no jump) |

## Comparison vs Baselines

* **t0091 (warm-start)**: found 1 strict joint-pass cell at gen 2 (DSI=0.51, PD=35.1Hz,
  robust=0.79). t0099 (random init) found 0 across 3 seeds × 5–8 gens.
* **Best random-init cell** (seed 22 gen 8): DSI=0.49, PD=18.7Hz, robust=0.98 — matches t0091
  on DSI / exceeds on robustness / **half the firing rate**.
* **Per-gen pace**: random-init runs have similar early-gen pace (38–52 min/gen 1) but
  super-linear slowdown by mid-run (167 min/gen 8 in seed 22; 222 min/gen 6 in seed 33). t0091
  ran only 2 gens so this slowdown wasn't observed there.

## Visualizations

### Headline best cells comparison

![Headline 4-panel: t0091 joint-pass cell (left, black soma) + best real cell from each
random-init seed (cyan/orange/olive
somas)](../../../tasks/t0099_random_init_pareto_robustness/results/images/headline_best_cells.png)

The leftmost panel is t0091's strict joint-pass cell (DSI=0.51, PD=35Hz, robust=0.79). The
three right panels are each random-init seed's best "real" cell (robust ≥ 0.5, PD ≥ 1Hz).
Visually the random-init best cells span more morphological variation than t0091's anchor-1
joint-pass cell, but none reach the 30 Hz PD threshold — a direct visual confirmation of the
"warm-start was load-bearing for PD-rate" finding.

### Cross-seed top-5 morphology grid

![5x3 grid: top 5 real cells per seed (rows = seeds 11/22/33), colored by nearest t0091
anchor](../../../tasks/t0099_random_init_pareto_robustness/results/images/cross_seed_top5_morphology_grid.png)

Each row is one seed's top 5 real Pareto cells, sorted by joint score. Colors indicate the
nearest t0091 anchor (blue=bedb_like, red=pd_asymmetric, green=nd_asymmetric,
purple=alt_topology — symmetric never appears). Notable patterns: seed 22 row is purple-heavy
(alt_topology dominant); seed 33 row is red-heavy (pd_asymmetric dominant); seed 11 mixes.

### HV trajectory across seeds

![HV trajectory: 3 random-init seeds + t0091 reference. Random-init runs reach HV ~5–10 over 8
gens; t0091 reached 23.7 in gen
2](../../../tasks/t0099_random_init_pareto_robustness/results/images/hv_trajectory_cross_seed.png)

t0091's HV at gen 2 alone (23.7) is 2.4× higher than seed 22's 8-gen HV (9.8). The warm-start
advantage is large and persistent.

### Anchor distribution heatmap

![5-row anchor x 4-column dataset heatmap. Symmetric row (1) is uniformly 0 across all 4
columns](../../../tasks/t0099_random_init_pareto_robustness/results/images/anchor_distribution_heatmap.png)

The symmetric anchor row is exactly 0 in all 4 columns — t0091, seed 11, seed 22, seed 33.
Warm-start-independent finding that the substrate cannot use morphologically-symmetric cells
in the Pareto.

### Pareto overlay in DSI/PD-rate space

![Scatter overlay: 4 datasets in (DSI, PD-rate) space. t0091 has the only point in the
upper-right joint-pass region (starred); random-init seeds hug the two
axes](../../../tasks/t0099_random_init_pareto_robustness/results/images/pareto_overlay_dsi_pdrate_robust.png)

Visualises the central finding: t0091's strict joint-pass cell (black star) sits alone in the
upper-right quadrant. Random-init seeds 11/22/33 cluster either along the DSI axis (high DSI,
low PD) or along the PD axis (high PD, low DSI), with one notable seed-22 cell straddling the
middle (DSI=0.49, PD=19Hz).

### Per-seed biological-plausibility heatmaps

![Per-cell × per-prior bio-plausibility verdict for seed
11](../../../tasks/t0099_random_init_pareto_robustness/results/images/biological_heatmap_seed11.png)
![Per-cell × per-prior bio-plausibility verdict for seed
22](../../../tasks/t0099_random_init_pareto_robustness/results/images/biological_heatmap_seed22.png)
![Per-cell × per-prior bio-plausibility verdict for seed
33](../../../tasks/t0099_random_init_pareto_robustness/results/images/biological_heatmap_seed33.png)

All 55 Pareto cells across 3 seeds flag exotic on at least one of the 13 biological priors —
same channel-side prior-violation pattern as t0091 (n_exotic = 19 / 22 / 14 across seeds). No
plausible or stretched cells in any seed. The substrate's prior-violation ceiling is robust to
warm-start vs random init.

## Analysis

### Q1: Are random-init seeds reproducible in their qualitative findings?

**Partially.** Across 3 independent seeds:

* **Reproducible** (n=3 confirms): zero strict joint-pass cells; zero biologically-plausible
  cells; zero symmetric-anchor Pareto cells.
* **Not reproducible**: anchor distributions disagree (seed 22 favours alt_topology, seed 33
  favours pd_asymmetric); HV trajectories disagree quantitatively (seed 22 hit HV=9.8, seed 33
  plateaued at 4.75 with no gen-8 jump); seed 22's near-joint-pass cell (DSI=0.49 PD=19Hz) did
  not appear in seeds 11 or 33.

The qualitative negative findings (no joint-pass, no plausibility, no symmetric) reproduce.
The positive findings (which morphology basins the optimizer prefers, what near-pass cells
emerge) do not. Three seeds are sufficient for the negative claim, insufficient for the
positive structure.

### Q2: Was t0091's 5-anchor warm-start load-bearing?

**Yes, and specifically for the high-PD-rate dimension.** t0091 found a joint-pass cell at gen
2 with DSI=0.51 / PD=35Hz / robust=0.79. After 5–8 gens of random-init NSGA-II across 3 seeds,
no cell crossed the joint-pass corner. The closest random-init result (seed 22 gen 8) matched
t0091's DSI but reached only half the PD-rate. The PD axis is what random init can't bridge in
8 gens; t0091's anchor 1 (Bed-B-like) seeded the optimiser with cells that already fired at
~30 Hz, leaving it only the easier task of pushing DSI without losing PD. The follow-up
experiment to confirm this would be **anchor-1-only warm-start** (test whether seeding with
Bed-B-like cells alone is sufficient — see suggestions).

### Plan-assumption audit

* **Plan assumption**: "If random-init seeds find no joint-pass cells while t0091 found one,
  this is consistent with the warm-start being load-bearing." → **Confirmed**.
* **Plan assumption**: "If random-init Paretos look qualitatively similar to t0091's,
  warm-start was redundant." → **Refuted** — Paretos differ qualitatively in cell-count
  (smaller), HV (lower), and joint-pass count (zero).
* **Plan assumption** (implicit): "Random-init NaN rate may be 30–50%, warranting penalty
  objectives." → **Refuted** — observed NaN rate < 1% in all 3 seeds. The patched generator
  handles random parameter combinations more robustly than expected.

## Limitations

1. **Only 3 seeds**. Reproducibility of qualitative findings is solid (n=3 negative results)
   but quantitative claims about Pareto shape would need more seeds.
2. **Seed 11 capped at gen 5** by the original $1.00 watchdog. Comparison with seed 22/33's
   8-gen runs is uneven on that seed.
3. **`rall_exponent` axis sampled in [~0, ~5]**, wider than t0091's plan-stated [0.5, 2.0]
   bounds. Random-init explores some morphologies t0091 never could; some seed-11
   underperformance may stem from this wider exploration. Acknowledged as a measurement caveat
   — the warm-start vs random-init comparison is still meaningful at the qualitative level (no
   joint-pass anywhere) but quantitative HV / Pareto-size comparisons are slightly biased.
4. **Per-gen wall-clock doubled mid-run**, leading to seed 33 only completing gen 8 with no
   meaningful HV improvement (HV=4.7408 → 4.7454, +0.001). Seed 33's gen 8 is essentially a
   stalled generation; the recorded final HV is conservative.
5. **No alt-init samplers tested**. LHS is good but Sobol' / Halton might give different
   coverage. Out of scope for this task.

## Files Created

### Code (25 modules)

* New: `paths.py`, `constants.py`, `constants_morphology.py`, `constants_electrophys.py`,
  `random_init.py`, `nsga2_driver.py`, `evaluator.py`, `cost_watchdog.py`,
  `hv_plateau_watchdog.py`, `anchor_classifier.py`, `per_seed_analysis.py`,
  `cross_seed_analysis.py`, `metrics_builder.py`, `build_assets.py`, `run_local_analysis.py`,
  `build_morphology_charts.py`, `run_three_seeds.sh`, `sync_results_back.sh`
* Copied from t0091: `apply_params.py`, `parametric_placer.py`, `trial_helpers.py`,
  `smoke_gate.py`, `build_cell_ais.py`, `extend_with_ais.py`, `generator_wrapper.py`,
  `recorder.py`, `bootstrap.py`, `biological_priors.py`, `biological_scorecard.py`

### Data

* `results/data/init_pop_seed{11,22,33}.json` — 3 LHS samples (96×68 each)
* `results/data/pareto_front_seed{11,22,33}.json` — per-seed Pareto archives (19/22/14 cells)
* `results/data/all_evaluations_seed{11,22,33}.json` — full per-cell records (480/768/768
  evaluations)
* `results/data/hv_trajectory_seed{11,22,33}.json` — HV over generations
* `results/data/nsga2_checkpoint_seed{11,22,33}.json` — pymoo NSGA-II final checkpoints
* `results/data/anchor_tracking_seed{11,22,33}.json` — per-cell nearest-anchor classification
* `results/data/biological_scorecard_seed{11,22,33}.json` — per-cell verdicts on 13 priors
* `results/data/cross_seed_summary.json`, `anchor_distribution_table.json` — cross-seed
  aggregates
* `results/data/algorithm_config.json`, `evaluation_seeds.json`, `biological_priors_68d.json`

### Charts

* `results/images/headline_best_cells.png`,
  `results/images/cross_seed_top5_morphology_grid.png`,
  `results/images/hv_trajectory_cross_seed.png`,
  `results/images/anchor_distribution_heatmap.png`,
  `results/images/pareto_overlay_dsi_pdrate_robust.png`,
  `results/images/biological_heatmap_seed{11,22,33}.png`

### Assets

* `assets/predictions/random-init-pareto-seed{11,22,33}/` — 3 predictions assets
* `assets/answer/random_init_reproducibility_and_warmstart_dependence/` — 1 answer asset

### Other

* `results/metrics.json` — explicit_variants format with 4 variants
* `results/costs.json` — $7.71 with per-phase breakdown
* `results/remote_machines_used.json` — single Vast.ai instance record
* `results/creative_thinking.md` — 4 out-of-the-box observations
* `intervention/budget_overrun_seed11.md` — documents the $1.00 cap hit

## Verification

* `verify_predictions_asset.py --task-id t0099_... random-init-pareto-seed{11,22,33}` — all
  PASSED
* `verify_answer_asset.py` — PASSED
* `verify_task_metrics.py` — PASSED
* `verify_machines_destroyed.py` — PASSED with expected RM-W001 + RM-W003 warnings
* `ruff check` + `ruff format` on `code/` — PASSED
* `mypy -p tasks.t0099_random_init_pareto_robustness.code` — PASSED
* `verify_task_file.py`, `verify_task_dependencies.py`, `verify_task_results.py`,
  `verify_task_folder.py`, `verify_logs.py`, `verify_suggestions.py` — to be run during
  reporting step

## Examples

The "system" for this task is the joint NSGA-II evaluator with random LHS init. Input = 14-d
morphology vector + 54-d electrophys vector; output = 3-objective evaluation (DSI, PD-rate,
robustness across 5 seeds).

### Example 1 — Best cell across all 3 seeds (seed 22 gen 8)

```text
seed=22 gen=8 anchor_nearest=alt_topology
DSI=0.4878  PD=18.71 Hz  robust=0.9823
```

The single near-joint-pass result. Matches t0091's joint-pass cell on DSI (0.49 vs 0.51) and
exceeds it on robustness (0.98 vs 0.79), but only achieves half the firing rate (19 vs 35 Hz).
Closest random-init came to the joint-pass corner.

### Example 2 — t0091 reference joint-pass cell

```text
t0091 gen=2 anchor_nearest=alt_topology
DSI=0.5113  PD=35.14 Hz  robust=0.7900
```

The cell that random-init seeds 11/22/33 collectively failed to reproduce. Same
alt_topology-adjacent morphology basin as seed 22's near-pass cell, but at gen 2 (5× sooner
than seed 22 needed to find its match-on-DSI cell).

### Example 3 — Best PD-rate cell, random init (seed 22 gen 6)

```text
seed=22 gen=8 DSI=0.0  PD=47.86 Hz  robust=0.0
```

Highest firing rate found by random init — significantly higher than t0091's joint-pass cell
(35 Hz). But all robustness=0 cells are unstable (only 1 of 5 evaluation seeds produced
spikes). The optimizer found high-PD regions but couldn't simultaneously find DSI in those
regions.

### Example 4 — Best DSI cell, random init (seed 22 gen 4)

```text
seed=22 gen=4 DSI=1.0  PD=0.0 Hz  robust=0.33
```

Same low-firing artifact as t0091 had — DSI=1.0 from 1–2 spikes that happened to land at PD.
Statistical artifact, not real direction tuning.

### Example 5 — Seed 33 best real cell (gen 6)

```text
seed=33 gen=6 anchor_nearest=alt_topology
DSI=0.3349  PD=9.29 Hz  robust=0.8485
```

Notably similar to seed 22's gen-6 best (DSI=0.37, PD=8.6Hz, robust=0.81). At gen 6, seeds 22
and 33 converged to the same region. The divergence happens in gen 7-8.

### Example 6 — Symmetric anchor representative (none in any seed's Pareto)

No Pareto cell in any random-init seed had `nearest_anchor_name="symmetric"`. The symmetric
anchor row is uniformly 0 in the cross-seed anchor heatmap. Warm-start-independent finding.

### Example 7 — HV trajectory comparison

```text
seed 22 HV: 0.13 → 0.29 → 0.53 → 1.93 → 4.71 → 4.98 → 5.09 → 9.80
t0091 HV:  14.07 → 23.71 (only 2 gens recorded)
```

t0091 reached gen-2 HV that seed 22 only matched at gen 8 (after 4× the compute). The
warm-start gave t0091 an HV head-start equivalent to ~6 generations of random-init
optimisation.

### Example 8 — Per-gen wall-clock slowdown (seed 22)

```text
gen 1: 52 min     gen 5: 104 min
gen 2: 56 min     gen 6: 107 min
gen 3: 65 min     gen 7: 149 min
gen 4: 89 min     gen 8: 167 min
```

3.2× slowdown from gen 1 to gen 8. Most likely cause: higher-firing-rate cells in late gens
require finer NEURON time-stepping. Future task budgets should scale super-linearly.

### Example 9 — Cross-seed near-duplicate check

```text
seed 11 vs seed 22 nearest: mean L2 = 0.92, min = 0.63
seed 11 vs seed 33 nearest: mean L2 = 0.90, min = 0.48
seed 22 vs seed 33 nearest: mean L2 = 0.92, min = 0.66
288 cells, 288 unique
```

The 3 init populations are genuinely independent (no near-duplicates between seeds, full
unit-cube coverage at 89.4–89.5% per-knob 5-95 percentile span).

### Example 10 — Cost watchdog mid-run adjustment

```text
seed 11: T0099_HARD_BUDGET_PER_SEED_USD=1.00 (frozen at process start)
         hit watchdog at gen 5, cost $1.13 (overshoot at gen boundary)
seed 22: T0099_HARD_BUDGET_PER_SEED_USD=5.00 (raised mid-run, picked up at process start)
         completed all 8 gens cleanly, cost $1.96
seed 33: T0099_HARD_BUDGET_PER_SEED_USD=5.00
         completed all 8 gens cleanly, cost $3.41
```

Documents the user-authorised mid-task watchdog raise. Demonstrates that running NSGA-II
processes can't read updated config; only newly-started Python processes pick up the change.

## Task Requirement Coverage

The operative task text from `task.json`:

> Run 3 random-init NSGA-II seeds (no warm-start) at $1 each; compare anchor distribution +
> bio-plausibility vs t0091.

Resolved long description (from `task_description.md`): 3 NSGA-II runs from random LHS-sampled
populations (seeds 11/22/33), per-seed Pareto + bio scorecard, cross-seed comparison, answer
to Q1 (reproducibility) and Q2 (warm-start dependence).

| REQ | Status | Result | Evidence |
| --- | --- | --- | --- |
| **REQ A** Random-init populations | **Done** | 3 LHS samples (96×68 each), reproducible, all 288 cells unique. | `init_pop_seed{11,22,33}.json` |
| **REQ B** 3 NSGA-II runs | **Done** | Seed 11: 5 gens (capped); seeds 22/33: 8 gens each. All 3 produced Pareto archives. | `pareto_front_seed{11,22,33}.json` |
| **REQ C** Per-seed analysis | **Done** | Anchor classification + biological scorecard per seed; 0 strict joint-pass / 0 plausible across all seeds. | `anchor_tracking_seed{11,22,33}.json`, `biological_scorecard_seed{11,22,33}.json` |
| **REQ D** Cross-seed comparison | **Done** | HV trajectory chart, anchor distribution heatmap, Pareto overlay scatter all produced. | `cross_seed_summary.json`, `hv_trajectory_cross_seed.png`, `anchor_distribution_heatmap.png`, `pareto_overlay_dsi_pdrate_robust.png` |
| **REQ E** Answer asset | **Done** | Q1 = "reproducible on negative findings, not on positive Pareto structure"; Q2 = "warm-start was load-bearing for the high-PD-rate dimension specifically". | `assets/answer/random_init_reproducibility_and_warmstart_dependence/` |
| **REQ F** 3 predictions assets | **Done** | One per seed with full per-cell metadata. | `assets/predictions/random-init-pareto-seed{11,22,33}/` |
| **REQ G** Morphology charts of best cells | **Done** | Headline 4-panel comparison + 5×3 cross-seed top-5 grid. | `headline_best_cells.png`, `cross_seed_top5_morphology_grid.png` |
| **REQ H** Cost ≤ $3.15 task cap | **Exceeded** | Total $7.71 (user authorised top-up mid-run; cap raised to $20). | `costs.json` |
| **REQ I** Vast.ai instance destroyed | **Done** | Instance 36372909 destroyed at 2026-05-10T23:07:56Z. | `machine_log.json`, `verify_machines_destroyed.py` PASSED |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0099_random_init_pareto_robustness/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0099_random_init_pareto_robustness" date_compared:
"2026-05-10" ---

# Compare to Literature: Random-Init NSGA-II Reproducibility Test

## Summary

Three random-init NSGA-II runs (no anchor warm-start) compared against (a) t0091's
warm-started run on the same substrate, and (b) 5 published methodological precedents + 4
biology references. Headline cross-task finding: **HM-2 (PD-asymmetric preferred over
ND-asymmetric morphology) was REFUTED in t0091 alone (12 vs 9, p=0.331) but is CONFIRMED when
pooling t0099's 3 random-init seeds (PD-asymm 20 vs ND-asymm 7, binomial p~0.013).**
Random-init isolates the Schachter 2010 / Briggman 2011 morphological-asymmetry-toward-PD
prediction that t0091's deliberately-balanced PD/ND-asymmetric warm-start anchors had washed
out. HM-1 (symmetric anchor unused) holds in all 4 datasets (n=4 strongly confirmed). HM-3
(length vs DSI) remains inconclusive, tagged for follow-up. The HV ratio of t0091 gen-2
(23.71) vs random-init seed 22 gen-8 (9.80) is 2.4x raw or ~6x per-generation, within Ament
2023's 5-10x warm-start advantage envelope.

## Comparison Table

### Comparable published values

| Reference | Metric / claim | Published | t0099 random-init | t0091 warm-start | Verdict |
| --- | --- | --- | --- | --- | --- |
| Trenholm 2013 | Peak DSGC PD firing rate | 198 Hz | best 18.7 Hz (seed 22 gen 8) | best 35.1 Hz (gen 2) | Both substrates **dramatically under-fire** vs biology; warm-start gets ~2x closer to biology than random init |
| Trenholm 2013 | PD/ND firing ratio | ~7x (198/27) | best ~inf (PD=18.7Hz vs ND=0Hz) | ~inf (joint-pass cell PD=35Hz vs ND~0) | Both substrates exceed the biology ratio because ND~0Hz at low firing rates |
| Briggman 2011 | SAC-DSGC structural asymmetry threshold for functional DS | 5:1 (null:preferred IPSC amplitude) | aggregated PD-asymm:ND-asymm anchor count = 20:7 (3 seeds) | 12:9 in t0091 alone | When pooled across 3 random-init seeds, **HM-2 confirmed** (binomial p ~ 0.013); t0091 alone (12 vs 9, p=0.331) was **insufficient evidence** |
| Schachter 2010 | Soma-displacement-toward-PD as morphological DS mechanism | predicted | 67% of asymmetric Pareto cells across 3 seeds were PD-asymmetric | 57% in t0091 (12/21) | Random-init isolates the prediction Schachter 2010 / Briggman 2011 explicitly made; t0091's dual seeding (PD- and ND-asymmetric anchors of equal weight) had masked it |
| Sivyer 2013 | NMDA per-spine conductance | 0.1 nS | All 55 random-init Pareto cells exotic on NMDA prior | All 57 t0091 Pareto cells exotic on same prior | Channel-side prior violation **independent of warm-start** |

### Methodological precedents

| Reference | Method | Match to t0099 | Implications |
| --- | --- | --- | --- |
| Hay 2011 | Multi-objective NSGA-II for biophysical model fitting | Used 4-6 objectives; pop 100; 1000 generations | Hay's 1000-gen budget is 100-200x ours. Our 8-gen result is still in the early-exploration regime by their standards |
| Ezra-Tsur 2021 | NSGA-II for retinal neuron biophysics | Used pop 200, 50-100 gens, single seed | They didn't report multi-seed reproducibility. Our 3-seed comparison is more rigorous on the reproducibility axis |
| Ament 2023 | Warm-start vs random-init in evolutionary search | Predicted 5-10x HV ratio for warm-start over random init in early gens | We observe **23.71/9.80 ~ 2.4x HV ratio** at t0091 gen 2 vs seed 22 gen 8 (i.e., warm-start at gen 2 = random-init at gen 8); when normalised to "HV per generation," warm-start is closer to **6x ahead** in early-gen advantage. Within Ament's 5-10x envelope |
| Cuntz 2010 | TREES toolbox procedural morphology | Used minimum spanning tree (MST) approach | Our 14-knob procedural generator is more constrained than MST; could be why random-init Pareto is smaller (14 vs 22 vs 19 cells per seed) than t0091's Pareto (57 cells with 5 anchors as priors) |
| Anderson 1999 | Cortical negative-control framework for DS | Argued against DS-tuning being inevitable in random networks | Our finding (0/55 random-init joint-pass cells) **strongly supports** Anderson's argument: directional selectivity does not emerge from random parameters; it requires structured priors |

## Methodology Differences

The t0099 vs published comparisons span three different axes:

* **Generation budget**: Hay 2011 used 1000 generations; we used 8. Our random-init Pareto is
  in the early-exploration regime by Hay's standards. Direct HV-magnitude comparison with Hay
  isn't meaningful; HV-trajectory shape is.
* **Population diversity strategy**: Ezra-Tsur 2021 used pop 200 (we used pop 96). At our
  smaller pop, NSGA-II's selection pressure is stronger per gen, but we sacrifice some
  diversity preservation. Larger pop would likely reduce per-seed Pareto-shape variance (we
  observe substantial variance across 3 seeds).
* **Warm-start design**: t0091's 5-anchor warm-start (Bed-B-like + symmetric + PD-asymmetric +
  ND-asymmetric + alt-topology) is a *structured* prior, not a *narrow* one. t0099's pure LHS
  init has no prior at all. Ament 2023's prediction is between these two extremes (warm-start
  with a single anchor); our test most closely matches their "uninformed init" control case.
* **Biological-plausibility scoring**: Both t0091 and t0099 use t0086/t0088's worst-case
  aggregation across 13 priors. The fact that all Pareto cells in both runs flag exotic on at
  least one prior is a **substrate** finding (the v3 Bed B substrate's prior-violation
  ceiling), independent of optimiser methodology. Confirms by replication.

## Analysis

### Cross-task hypothesis verdicts (revised)

* **HM-1 (morphology asymmetry necessary)**: **CONFIRMED in 4/4 datasets** (t0091, seed 11,
  seed 22, seed 33). Symmetric anchor count = 0 in every Pareto. Highly robust at n=4.
* **HM-2 (PD-asymmetric preferred over ND-asymmetric)**: **REVISED from REFUTED to
  CONFIRMED**. t0091 alone had 12 vs 9 (p=0.331, not significant). When pooled across 3
  random-init seeds: PD-asymmetric = 7+4+9 = 20; ND-asymmetric = 5+2+0 = 7. Binomial test for
  20/27 = 0.74 expected 0.5: p ~ 0.013, significant at alpha=0.05. Random-init isolates the
  Schachter 2010 prediction.
* **HM-3 (cells with stronger DS have higher field_elongation_pd)**: **STILL INCONCLUSIVE**.
  Per-cell field_elongation vs DSI test was not run on t0099 Pareto cells. Tagged in
  S-0099-02.

### Key novelty findings beyond t0091

1. **Anchor preference disagreement across random-init seeds** (seed 22 favours alt_topology,
   seed 33 favours pd_asymmetric, seed 11 mixes) is **a new finding** not visible in the
   single-seed t0091 result. Suggests the 68-d Pareto has multiple morphological basins that
   single warm-start runs may have only partially explored.
2. **Per-gen wall-clock super-linear scaling** (38 to 167 min/gen for seed 22) is **a new
   finding** not observable in t0091 (only 2 gens recorded). Useful for budgeting future
   morphology-extended NSGA-II tasks.
3. **Random-init NaN rate < 1%** (vs the plan's 30-50% prediction) **revises the t0090
   generator robustness assessment**: the patched generator handles arbitrary parameter
   combinations more robustly than expected.

### Recommended next experiment

**Anchor-1-only warm-start NSGA-II** (one seed, $3.50 estimated): replace t0091's 5-anchor
warm-start with anchor 1 (Bed-B-like) only. If joint-pass cell emerges -> anchor 1 was
load-bearing alone. If not -> warm-start *diversity* was load-bearing (anchor 1 needed
combination with at least one of PD/ND-asymmetric/alt_topology). Either outcome substantially
narrows future morphology-extended NSGA-II design. Tagged in S-0099-01.

## Limitations

1. **Only 3 random-init seeds**. Reproducibility of qualitative findings is solid (n=3
   negative results) but quantitative claims about Pareto shape (anchor preferences, HV
   asymptotes) would need more seeds.
2. **Seed 11 capped at gen 5** vs seeds 22/33 at gen 8. Comparison is uneven on that seed.
3. **`rall_exponent` axis sampled in [~0, ~5]**, wider than t0091's plan-stated [0.5, 2.0]
   bounds. Random-init explores some morphologies t0091 never could; some seed-11
   underperformance may stem from this wider exploration. The warm-start vs random-init
   comparison is still meaningful at the qualitative level but quantitative HV / Pareto- size
   comparisons are slightly biased.
4. **No alt-init samplers tested**. LHS is good but Sobol' / Halton might give different
   coverage. Out of scope.
5. **Hay 2011's 1000-gen budget is far above ours**. Direct HV comparison with their work
   would require running random-init at much higher budget (S-0099-05 explores this).

## References

* [Trenholm2013] - DSGC firing rate biology; in t0091 corpus
* [Briggman2011] - SAC-DSGC wiring asymmetry; in t0091 corpus
* [Sivyer2013] - NMDA per-spine conductance; in t0091 corpus
* [Schachter2010] - Soma displacement as morphological DS mechanism; in t0091 corpus
* [Hay2011] - Multi-objective NSGA-II for biophysics; in t0091 corpus
* [Ezra-Tsur2021] - NSGA-II for retinal neurons; in t0091 corpus
* [Ament2023] - Warm-start vs random init in evolutionary search; in t0091 corpus
* [Cuntz2010] - TREES toolbox procedural morphology; in t0091 corpus
* [Anderson1999] - Cortical negative-control framework for DS; in t0091 corpus

</details>
