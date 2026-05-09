# Random-Init NSGA-II Reproducibility Test: 3 Seeds vs t0091 Pareto

## Motivation

t0091 produced a 57-cell Pareto front from joint 68-d NSGA-II using a 5-anchor warm-start
(bedb_like, symmetric, PD-asymmetric, ND-asymmetric, alt_topology). The headline finding — zero
biologically-plausible joint-pass cells — relied on a single NSGA-II run from a structured
warm-start. **Two open questions remain**:

1. **Reproducibility under different RNG seeds**: would a different seed produce a similar Pareto
   front, anchor distribution, and bio-plausibility outcome? t0091 ran one seed.

2. **Warm-start dependence**: was the 5-anchor warm-start load-bearing, or would purely random
   initial populations have found the same Pareto? The brainstorm-18 design assumed the warm-start
   was necessary; this assumption was never tested.

This task tests both questions with 3 NSGA-II runs from **totally random** initial populations, each
with a different RNG seed. The 14-d morphology vector and 54-d electrophys vector are sampled
uniformly from each parameter's plan-defined bounds (no anchor bias).

## Scope

### In Scope

* 3 NSGA-II runs on Vast.ai EPYC 7B13 64-core CPU, each with a different RNG seed (e.g., 11, 22,
  33), each with a $1.00 hard cost watchdog cap. Total project budget cap $3.15.
* Each run: pop=96, max_gen=8, totally random initial population (uniform LHS sample over the 68-d
  parameter space — no anchor warm-start), HV-plateau termination + cost watchdog + max-gen
  termination.
* Reuse t0091's evaluator infrastructure (generator wrapper, biological priors, biological
  scorecard, anchor-tracking machinery for analysis only).
* Per-seed Pareto archive (predictions asset per seed, 3 total).
* Cross-seed analysis: HV trajectory comparison, Pareto cell counts, anchor distribution recompute
  (using t0091's 5-anchor definitions for nearest-anchor classification — the runs themselves are
  anchor-free, but post-hoc classification still works), bio-plausibility comparison.
* One synthesis answer asset addressing the two open questions.

### Out of Scope

* No new biology, no new generator changes, no new priors.
* No comparison against random-init runs at full t0091 depth (would cost $30+; deferred).
* No multi-objective formulation revision (deferred per S-0091-05).
* No real-cell morphology library (deferred per S-0091-06 / Option G).
* No cross-bed validation against Bed A (deferred per S-0086-06).

## Approach

### Phase A — Random-init population builder

Replace t0091's anchor-based warm-start with a uniform LHS sample over the 68-d parameter space.
Each of the 3 seeds gets its own LHS sample drawn from `np.random.SeedSequence(seed)`.

Code: copy `t0091/code/warmstart.py` into `t0099/code/random_init.py`, replace the anchor logic with
`LatinHypercubeSampling` from pymoo (or `scipy.stats.qmc.LatinHypercube` with explicit seed).

### Phase B — NSGA-II runs

Reuse t0091's `nsga2_driver.py` evaluator + cost watchdog with these adjustments per seed:

* `T0099_HARD_BUDGET_PER_SEED_USD = 1.00` (replaces t0091's $4.00).
* `pymoo.algorithms.moo.nsga2.NSGA2(pop_size=96, sampling=lhs_sample_for_seed, ...)`.
* All other settings identical to t0091 (SBX crossover η=15, polynomial mutation η=20, prob=1/68,
  eliminate_duplicates=True, MaximumGenerationTermination(8), HV-plateau watchdog, cost watchdog).
* Each seed runs sequentially on the same Vast.ai instance to amortise provisioning cost.
* Seeds: 11, 22, 33 (arbitrary primes; reproducible).

### Phase C — Per-seed analysis

For each of the 3 seeds:

1. Extract Pareto front from the final population.
2. Classify each Pareto cell to its nearest t0091 anchor in 14-d morph space (using t0091's 5 anchor
   centroids as fixed reference points; this is post-hoc classification, not warm-start).
3. Score each Pareto cell with t0091's `biological_scorecard.py` (13 priors, worst-case
   aggregation).
4. Compute strict joint-pass count (DSI≥0.5, PD≥30 Hz, robust≥0.7).

### Phase D — Cross-seed comparison

* HV trajectory plot: 3 lines (one per seed) + t0091's reference line.
* Pareto cell count per seed (and t0091's 57 for reference).
* Anchor distribution per seed: 5-row × 4-column heatmap (rows = anchors, columns = seed11 / seed22
  / seed33 / t0091).
* Bio-plausibility: per-seed count of cells passing each prior; cells passing all 13 priors jointly
  (expected: 0 across all seeds).
* Strict joint-pass count per seed.
* Pareto-front overlap in the (DSI, PD-rate, robustness) cube: are the 3 random-init Paretos in the
  same region of objective space as t0091's, or do they explore different regions?

### Phase E — Answer asset

Write `assets/answer/random_init_reproducibility_and_warmstart_dependence/`:

* **Q1**: Are random-init seeds reproducible in their qualitative findings (bio-plausibility, anchor
  distribution, joint-pass count)?
* **Q2**: Was t0091's 5-anchor warm-start load-bearing, or would random init have found the same
  Pareto?

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
* Definitive yes/no on Q1 (reproducibility) and Q2 (warm-start dependence) in the answer asset.

**Acceptable negative outcomes**:

* If 1 or more seeds fail to produce a Pareto with ≥8 cells, document the failure mode (NaN
  flooding, slow convergence) and report cross-seed comparison on the surviving runs only.
* If random-init seeds find no joint-pass cells while t0091 found one, this is consistent with the
  warm-start being load-bearing (S-0091-05's hypothesis).
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
  warm-start filter; random-init may see 30–50%. The evaluator returns a penalty objective for NaN
  cells, so NSGA-II handles this, but Pareto sizes per seed may be smaller than t0091's 57.
* **Per-seed budget too tight**. $1.00 = ~3 generations max; if a seed needs gen 4+ to escape
  initial-population dominance, the watchdog will kill it before convergence. Mitigation: report the
  truncation in results, note that this is the budget-bounded reproducibility regime.
* **Cross-seed cumulative tracker bug**. If one seed overruns its $1.00 cap by a few cents, the task
  could blow $3.15. Mitigation: per-seed cap is the primary defence; the cross-seed tracker is a
  backup.
* **Vast.ai instance flaky on long runs**. t0091 ran 2.6 hours; this task may run 6–10 hours.
  Mitigation: NSGA-II checkpoints after each generation, so a mid-run instance failure costs one
  generation, not the whole seed.

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
* **t0090_morphology_generator_diversity_test** — original generator (superseded by t0092 fix per
  C-0093-01).
* **t0092_diagnose_morphology_generator_silence** — patched generator (canonical via C-0093-01).
* **t0093_resweep_and_t0090_correction** — issued the C-0093-01 correction overlay.
* **t0086_robustness_cluster_bio_comparison** — biological priors and scorecard
  (`biological_priors.py`, `biological_scorecard.py`).
* **t0083_bedb_v3_extend_nsga2_gen8plus** — HV-plateau watchdog reference.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2** — NSGA-II driver, evaluator, cost watchdog
  reference.
* Source suggestion: none directly. Indirectly addresses parts of S-0091-05 (multi-objective
  reformulation needs random-init baseline) and was scoped during the post-t0098 user conversation.
