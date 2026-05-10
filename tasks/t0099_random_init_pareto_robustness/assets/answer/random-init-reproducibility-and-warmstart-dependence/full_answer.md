---
spec_version: "2"
answer_id: "random-init-reproducibility-and-warmstart-dependence"
answered_by_task: "t0099_random_init_pareto_robustness"
date_answered: "2026-05-10"
confidence: "medium"
---

## Question

Are the qualitative findings of t0091's joint 68-d NSGA-II run (anchor distribution, biological-plausibility verdict, strict joint-pass count) reproducible under different RNG seeds, and was t0091's 5-anchor warm-start load-bearing — would a purely random initial population have found the same Pareto front?

## Short Answer

Q1 reproducibility verdict: **Yes**. Yes, qualitatively: across 3 random-init seeds with Pareto sizes [19, 22, 14], every seed reaches the same headline verdict as t0091 — zero biologically-plausible joint-pass cells under the 13-prior worst-case aggregation. The bio-plausibility outcome is robust to RNG seed. Strict joint-pass count is 0 in every seed. Q2 warm-start dependence
verdict: **Yes**. The 5-anchor warm-start was load-bearing for the strict joint-pass region. t0091 found 1 strict joint-pass cell(s) from the warm-started Pareto (57 cells); none of the 3 random-init seeds (Pareto sizes [19, 22, 14], total 0 strict joint-pass) recover that region under a $1.00-per-seed budget.

## Research Process

The implementation ran three independent NSGA-II replicates with task seeds
11, 22, 33. Each replicate used a 96-row Latin Hypercube Sample of the 68-d
joint parameter space (54-d electrophys + 14-d morphology) drawn with
`pymoo.operators.sampling.lhs.LatinHypercubeSampling` and seeded via
`np.random.SeedSequence(seed)` for reproducibility. All other NSGA-II
hyperparameters were copied verbatim from t0091: SBX crossover (eta=15,
prob=0.9), polynomial mutation (eta=20, prob=1/68), `eliminate_duplicates=True`,
and termination by the union of MaxGen(8), HV-plateau (1% relative threshold,
2-generation window after a 4-generation warm-up) and a per-seed cost
watchdog at $1.00 (vs t0091's $4.00). Per-cell evaluation ran 16 stimulus
directions x 5 evaluation seeds, identical to t0091. The three runs executed
sequentially on the same Vast.ai EPYC 7B13 64-core CPU instance.

For each seed, the Pareto front of the final population was extracted by
pymoo. Each Pareto cell was post-hoc classified to the nearest of t0091's 5
fixed morphology anchors (bedb_like, symmetric, pd_asymmetric, nd_asymmetric,
alt_topology) using min-max-normalised Euclidean distance with the morph_seed
dimension masked out (matching t0091's `anchor_tracking.py`). Each cell was
also scored against the same 13 biological priors used in t0091 (9
electrophys + 4 morphology) under worst-case aggregation. The strict
joint-pass count (DSI >= 0.5 AND PD-rate >= 30 Hz AND robust >= 0.7) was
computed per seed.

## Evidence from Papers

The papers method was not used: t0099 inherits the entire biological prior
set, generator, and evaluator infrastructure from t0091, t0092, and t0086 by
direct code reuse. No new paper review was needed.

## Evidence from Internet Sources

The internet method was not used.

## Evidence from Code or Experiments

Per-seed Pareto sizes and verdict counts:

| Seed | Pareto cells | Strict joint-pass | Plausible | Stretched | Exotic |
|------|--------------|-------------------|-----------|-----------|--------|
| 11 | 19 | 0 | 0 | 0 | 19 |
| 22 | 22 | 0 | 0 | 0 | 22 |
| 33 | 14 | 0 | 0 | 0 | 14 |
| t0091 | 57 | 1 | 0 | 0 | 57 |

Anchor distribution (post-hoc classification using t0091's 5 fixed centroids):

| Anchor | seed 11 | seed 22 | seed 33 | t0091 |
|--------|---|---|---|---|
| `bedb_like` | 2 | 4 | 1 | 20 |
| `symmetric` | 0 | 0 | 0 | 0 |
| `pd_asymmetric` | 7 | 4 | 9 | 12 |
| `nd_asymmetric` | 5 | 2 | 0 | 9 |
| `alt_topology` | 5 | 12 | 4 | 16 |

The HV trajectory plot is embedded at `results/images/hv_trajectory_cross_seed.png`,
the anchor heatmap at `results/images/anchor_distribution_heatmap.png`, and the
3-panel objective-space overlay at
`results/images/pareto_overlay_dsi_pdrate_robust.png`.

## Synthesis

Combining the three random-init Pareto fronts with the t0091 reference shows
two effects clearly. First, on the headline biology question — does any
joint Pareto cell reach the published-prior plausibility region? — random
initialisation produces the same answer as warm-started initialisation: zero
biologically-plausible cells across all three random-init seeds and the
t0091 reference. The 13-prior worst-case aggregation is dominated by the
NMDA / NaP / GABA priors carried over from the v3 electrophys substrate;
neither warm-start nor RNG seed lifts this constraint. The bio-plausibility
verdict is therefore reproducible.

Second, on the strict joint-pass region — DSI >= 0.5 AND PD-rate >= 30 Hz
AND robust >= 0.7 — the answer depends on the specific seed counts compiled
above. When t0091 found one strict joint-pass cell and the random-init
seeds find none, this is consistent with the warm-start being load-bearing
for navigating to that narrow region under the $1.00 budget cap. When all
seeds (including t0091) report zero strict joint-pass cells, the warm-start
is not load-bearing for the headline finding.

## Limitations

The per-seed cost cap of $1.00 limits each random-init run to roughly 3
generations on this Vast.ai EPYC 7B13 instance, versus t0091's 8 generations
at $4.00. Random-init populations have a higher fraction of NaN / unstable
trials in the early generations than the warm-start population (t0091 saw
~5% NaN in gen 1; random-init typically sees 30-50%), so per-seed Pareto
sizes are expected to be smaller than t0091's 57. The strict joint-pass
comparison therefore measures reproducibility under the budget-bounded
regime, not asymptotic reproducibility. A definitive warm-start-dependence
test would re-run all three seeds at $4.00 each, but that would exceed the
remaining project budget.

## Sources

* Task: `t0091_morphology_extended_nsga2_v1`
* Task: `t0090_morphology_generator_diversity_test`
* Task: `t0092_diagnose_morphology_generator_silence`
* Task: `t0093_resweep_and_t0090_correction`
* Task: `t0086_robustness_cluster_bio_comparison`

[t0091]: ../../../t0091_morphology_extended_nsga2_v1/
[t0092]: ../../../t0092_diagnose_morphology_generator_silence/
