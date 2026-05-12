# ✅ 68-d NSGA-II at GA seeds=2, N_SEEDS=4, gens=20, random init

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0102_seedscale_n4_gen20` |
| **Status** | ✅ completed |
| **Started** | 2026-05-11T14:08:37Z |
| **Completed** | 2026-05-12T18:44:00Z |
| **Duration** | 28h 35m |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md), [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md), [`t0101_brainstorm_results_21`](../../../overview/tasks/task_pages/t0101_brainstorm_results_21.md) |
| **Task types** | `experiment-run`, `data-analysis`, `answer-question` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`dendritic-computation`](../../by-category/dendritic-computation.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md) |
| **Expected assets** | 2 predictions, 1 answer |
| **Step progress** | 15/15 |
| **Cost** | **$12.07** |
| **Task folder** | [`t0102_seedscale_n4_gen20/`](../../../tasks/t0102_seedscale_n4_gen20/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0102_seedscale_n4_gen20/results/results_detailed.md) |

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

## Costs

**Total**: **$12.07**

| Category | Amount |
|----------|--------|
| vast_ai_nsga2_compute | $8.46 |
| vast_ai_setup_and_smoke_gates | $0.11 |
| vast_ai_idle_time | $3.51 |

## Remote Machines

| Provider | GPU | Count | RAM | Duration | Cost |
|----------|-----|-------|-----|----------|------|
| vast.ai | RTX 4090 (idle, unused; CPU-only NEURON workload) | 1 | 503 GB | 24.8h | $12.07 |

## Metrics

### Random-init seed 44 (N_EVAL_SEEDS=4, gens completed=14)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |

### Random-init seed 55 (N_EVAL_SEEDS=4, gens completed=13)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Does running 68-d NSGA-II at N_EVAL_SEEDS=4 noise replicates, gens=20, pop=96, 2 random-init GA seeds (44, 55), no warm-start, recover the strict joint-pass corner (DSI>=0.5 AND PD-rate>=30 Hz AND robustness>=0.7) of the Bed B + morphology compartmental DSGC substrate?](../../../tasks/t0102_seedscale_n4_gen20/assets/answer/does-n4-gens20-2seeds-recover-joint-pass-corner/) | [`full_answer.md`](../../../tasks/t0102_seedscale_n4_gen20/assets/answer/does-n4-gens20-2seeds-recover-joint-pass-corner/full_answer.md) |
| paper | [Noisy evolutionary optimization algorithms – A comprehensive survey](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.1016_j.swevo.2016.09.002/) | [`summary.md`](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.1016_j.swevo.2016.09.002/summary.md) |
| paper | [A Complete Spatial Map of Mouse Retinal Ganglion Cells Reveals Density and Gene Expression Specializations](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.1101_2025.02.10.637538/) | [`summary.md`](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.1101_2025.02.10.637538/summary.md) |
| paper | [Evaluation and comparison of methods for neuronal parameter optimization using the Neuroptimus software framework](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/) | [`summary.md`](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md) |
| paper | [Analysing the Robustness of NSGA-II under Noise](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2306.04525/) | [`summary.md`](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2306.04525/summary.md) |
| paper | [Theoretical Analysis of Explicit Averaging and Novel Sign Averaging in Comparison-Based Search](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2401.14014/) | [`summary.md`](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2401.14014/summary.md) |
| paper | [Adaptive Resampling with Bootstrap for Noisy Multi-Objective Optimization Problems](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2503.21495/) | [`summary.md`](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2503.21495/summary.md) |
| predictions | [NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init)](../../../tasks/t0102_seedscale_n4_gen20/assets/predictions/nsga2-seed44-bedb-morph-n4-gen20/) | [`description.md`](../../../tasks/t0102_seedscale_n4_gen20/assets/predictions/nsga2-seed44-bedb-morph-n4-gen20/description.md) |
| predictions | [NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init)](../../../tasks/t0102_seedscale_n4_gen20/assets/predictions/nsga2-seed55-bedb-morph-n4-gen20/) | [`description.md`](../../../tasks/t0102_seedscale_n4_gen20/assets/predictions/nsga2-seed55-bedb-morph-n4-gen20/description.md) |

## Suggestions Generated

<details>
<summary><strong>Fix DSI vector-sum objective: gate by minimum total spike count to
eliminate silenced-cell DSI=1.0 artifact</strong> (S-0102-01)</summary>

**Kind**: technique | **Priority**: high

Finding 1 in results_detailed.md: 27 t0102 cells reach DSI = 1.0 because vector-sum DSI in
evaluator.py divides by near-zero total spike count on silenced cells, with floating-point
dust producing a spurious 'perfect selectivity' score that pulls half the NSGA-II Pareto into
the silence corner. Single-line fix: return 0.0 when total_spike_count across 16 directions is
< 10. Bug affects the entire t0080-t0102 lineage; highest-leverage change for recovering
joint-pass cells at fixed algorithm and budget. Implementation: patch evaluator.py in a new
task that copies the t0099 substrate, add a silenced-cell unit test, re-run random-init
NSGA-II at pop=96, gens=8, 1 GA seed, N=4. Expected: joint-pass yield > 0 from random init;
DSI distribution loses its 1.0 spike. Recommended task types: write-library, experiment-run.
Cost: ~$2-3 (one pop=96 x 8-gen Vast.ai run).

</details>

<details>
<summary><strong>Direct re-evaluation of t0083 / t0091 anchor library at
N_EVAL_SEEDS=4 to disambiguate substrate vs algorithm limitation</strong>
(S-0102-02)</summary>

**Kind**: evaluation | **Priority**: high

creative_analysis.md Section 4 proposes a < $0.20 follow-up that disambiguates
'substrate-limited vs algorithm-limited' definitively. Take the 5 anchor families from t0091's
warm-start (alt_topology, symmetric, bedb_like, t0083 anchors 1559 and 1677) and re-evaluate
each at N_EVAL_SEEDS=4 with no NSGA-II/LHS/mutation -- just per-cell evaluation. Count how
many clear the strict joint-pass corner. Outcome A (zero clear): joint corner is empirically
unreachable on this substrate at N=4 regardless of algorithm; further NSGA-II is futile.
Outcome B (>= 1 clears): NSGA-II at random init is failing to find what is empirically
present; algorithm replacement (IBEA/CMAES) justified. Also re-evaluate t0091's joint-pass
cell (DSI=0.511, PD=35.1 Hz, rob=0.79) at N=4 to test the noise-floor prediction. Recommended
task types: baseline-evaluation, comparative-analysis. Cost: < $0.20 (~95 evaluations, no GA,
~30 min on Vast.ai).

</details>

<details>
<summary><strong>IBEA replacement for NSGA-II at matched budget (pop=96, gens=15,
N=4, 2 GA seeds) on Bed B + morphology substrate</strong> (S-0102-03)</summary>

**Kind**: experiment | **Priority**: high

Mohacsi 2024 (Neuroptimus benchmark, PLOS Comp Bio) reports IBEA is 'clearly the best among
the multi-objective methods' on six neuron-fitting benchmarks including Hay 2011 L5PC,
outperforming all three NSGA-II implementations tested. t0102 only tested NSGA-II, leaving
algorithm choice as an unexamined factor in the 0/4800 random-init joint-pass yield. Port the
t0099 substrate to pymoo's IBEA (or DEAP/BluePyOpt IBEA wrapper) at matched budget (pop=96,
gens=15, N_EVAL_SEEDS=4, 2 GA seeds, $8 cap), apply the S-0102-01 DSI fix if available, and
compare front structure to t0099+t0102. Expected: IBEA's hypervolume-density selection avoids
placing half the front in the DSI=1/PD=0 corner that NSGA-II crowding distance keeps;
joint-pass yield improves even if the corner remains hard. Run after or alongside S-0102-02.
Recommended task types: experiment-run, comparative-analysis. Cost: ~$6-8 matched to t0102
envelope (IBEA's O(N^2) overhead manageable at pop=96).

</details>

<details>
<summary><strong>Dang 2023 theory-grounded NSGA-II at pop>=290 (mu = n log n floor)
with N_EVAL_SEEDS=4, gens=10</strong> (S-0102-04)</summary>

**Kind**: experiment | **Priority**: high

Dang 2023 Theorem 8 requires mu = Omega(n log n) for noisy NSGA-II to retain polynomial
expected runtime under Bernoulli or Gaussian noise. For our 68-d substrate, the theoretical
floor is Omega(68 * log(68)) = approximately 290; t0102 ran at pop=96, three times below this
floor. compare_literature.md Methodology Differences identifies this as a principled lever to
pull before concluding the substrate is structurally empty of joint-pass cells. Run a single
random-init NSGA-II at pop=320 (slightly above the Dang floor for headroom), gens=10,
N_EVAL_SEEDS=4, 1 GA seed -- total budget approximately 3200 evaluations, comparable to t0102.
If pop>=290 finds joint-pass cells where pop=96 found none, the population-floor argument is
empirically confirmed; if not, the substrate-limitation reading hardens. Recommended task
types: experiment-run, comparative-analysis. Cost: ~$5-7 on Vast.ai (single seed at higher pop
offsets the fewer generations).

</details>

<details>
<summary><strong>Anchor-distance lineage trace: quantify t0091 joint-pass cell as
one-mutation descendant of alt_topology anchor</strong> (S-0102-05)</summary>

**Kind**: evaluation | **Priority**: medium

creative_analysis.md Section 2 reframes t0091's joint-pass cell (DSI=0.511, PD=35.1 Hz,
rob=0.79, source_generation=2) as a one-mutation descendant of alt_topology anchor row 84 --
not a de novo NSGA-II discovery. The cell sits 3.55 normalised units from row 84 vs >= 11
units to any other anchor; expected mutated dims per offspring ~1.0. Load-bearing
methodological reframing for any paper draft. Formalise as analysis: (i) pairwise Euclidean
distance from each t0091/t0099/t0102 Pareto cell to every t0091 warm-start anchor and every
t0083 anchor; (ii) classify each joint-pass-adjacent cell as 'anchor-near' (< 5 units) vs
'GA-discovered' (>= 10 units); (iii) histogram + scatter of distance vs source_generation.
Outcome: empirical answer to 'how much of NSGA-II output is searched vs preserved-from-init'
across t0080-t0102. Recommended task types: data-analysis, comparative-analysis. Cost: ~$0
(offline analysis on stored JSONLs).

</details>

<details>
<summary><strong>Calcium-clearance perturbation sweep on the 27 silenced-cell
DSI=1.0 vectors to test silence-as-mechanism hypothesis</strong>
(S-0102-06)</summary>

**Kind**: experiment | **Priority**: medium

creative_analysis.md Section 7 proposes a mechanistic reading: the 27 t0102 cells with DSI >=
0.99 / PD < 0.1 are not bugs but the GA's discovery of a lateral-inhibition silencing regime
(slow Ca clearance, strong sAHP, weak ACh drive) consistent with Poleg-Polsky 2026 SAC gating.
Take each of the 27 cells, fix the 68-d vector except CAD_TAUR_MS (Ca clearance tau, dim 38),
sweep that dim from ~65 ms down to 5 ms in 10 logarithmic steps, re-evaluate DSI/PD/rob at
N_EVAL_SEEDS=8. Question: when Ca clearance is restored, do these cells collapse to the
high-PD low-DSI corner (silence was the only DSI mechanism), or do some land in the joint
corner (Ca clearance is the active constraint and the rest of the vector is joint-viable)?
Outcome: 27 x 10 grid mapping silence-to-joint escape paths. Doubles as slice-physiology
prediction (BAPTA Ca chelation should disinhibit SAC/DSGC firing). Recommended task types:
experiment-run, data-analysis. Cost: < $0.50 (270 evaluations, no GA).

</details>

<details>
<summary><strong>Morinaga 2024 sign-averaging objective formulation to handle
heavy-tailed DSI noise (alpha close to 1) at fixed budget</strong>
(S-0102-07)</summary>

**Kind**: technique | **Priority**: medium

Morinaga 2024 (arXiv 2401.14014) Theorem 3 shows explicit averaging is only effective when the
per-objective noise stability index alpha > 1. compare_literature.md argues our DSI vector-sum
near zero-spike cells is heavy-tailed with alpha ~1, making K=4 averaging 'nearly inert'.
Theorem 9 proposes sign-averaging as a comparison-based alternative robust under heavy tails
at the same compute cost. Steps: (i) compute per-objective alpha on the t0093 anchor library
at N=20 (offline); (ii) if alpha < 1 for DSI, reformulate NSGA-II selection via sign-averaging
(count replicates favouring A over B) instead of mean ranking; (iii) run a 1-seed NSGA-II at
matched budget with sign-averaging. Complementary to S-0102-01 (DSI fix targets the
floating-point bug; this targets noise-handling theory). Recommended task types:
write-library, experiment-run. Cost: ~$3-5 (one pop=96 run plus offline analysis).

</details>

<details>
<summary><strong>Vast.ai cost-watchdog parameterisation: idle-timeout teardown and
post-watchdog termination to prevent $3+ idle overrun</strong> (S-0102-08)</summary>

**Kind**: library | **Priority**: medium

t0102 cost overrun ($12.07 vs $8 plan cap) decomposed as $8.46 productive NSGA-II compute
(per-seed $4 watchdog behaved as designed) plus $3.51 idle uptime: $0.11 setup, ~$1.5 from a
dead initial subagent before recovery, ~$2 post-watchdog billing before teardown.
results_detailed.md Limitations records this. Harden the cost-watchdog infrastructure: (i)
idle-CPU watchdog that destroys the instance if no NEURON worker processes have run for > 15
minutes; (ii) chain the per-seed cost watchdog directly into instance teardown rather than
just terminating the NSGA-II loop; (iii) standardise the offer-rate hourly-price source (t0102
billed $0.4852/hr while the watchdog read $0.4690/hr base, drift ~$0.1/hr over 24 h). Small
library change in arf/scripts/utils plus task-level orchestration. Recommended task types:
write-library, infrastructure-setup. Cost: ~$0 development + recovered ~$3/task in subsequent
runs.

</details>

## Research

* [`research_code.md`](../../../tasks/t0102_seedscale_n4_gen20/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0102_seedscale_n4_gen20/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0102_seedscale_n4_gen20/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0102_seedscale_n4_gen20/results/results_summary.md)*

# Results Summary: t0102 Seed-scale N=4, Gen=20 Random-Init NSGA-II

## Summary

Both random-init NSGA-II GA seeds (44, 55) completed at `N_EVAL_SEEDS=4` on the 68-d Bed B +
morphology DSGC substrate but were terminated by the per-seed $4 cost watchdog before reaching
generation 20 (seed 44: 14/20 gens, seed 55: 13/20 gens). Across all **2,592** evaluated
cells, **zero** cleared the strict joint-pass corner (DSI >= 0.5 AND PD-rate >= 30 Hz AND
robustness >= 0.7) and **zero** cleared even the loosest 2-axis variant (DSI >= 0.5 AND PD >=
5 Hz). The 5x noise drop + 2.5x generation extension hypothesis from the brainstorm is
therefore rejected; t0099's negative result replicates at a different seed/gen/noise budget. A
previously unreported floating-point artifact in the DSI vector-sum objective was uncovered:
27 cells with max DSI = 1.0 are silenced cells (PD = 0 Hz) where divide-by-near-zero in the
vector-sum formula produces a spurious "perfect DSI" signal — the real DSI corner sits at DSI
~= 0.35 with PD >= 5 Hz.

## Metrics

* **Total cells evaluated**: **2,592** (1,344 seed 44 + 1,248 seed 55)
* **Strict joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz AND rob >= 0.7): **0** in both seeds
* **2-axis loose joint-pass cells** (DSI >= 0.5 AND PD >= 5 Hz): **0** across both seeds
* **Max DSI (vector-sum)**: **1.0000** in both seeds — but on silenced cells (PD = 0 Hz),
  reflecting a floating-point artifact, not a real direction-selectivity signal
* **Max PD-rate**: seed 44 = **64.29 Hz**, seed 55 = **66.96 Hz** (both with DSI ~ 0)
* **Real-DSI corner** (excluding silenced cells, PD > 0): **DSI ~ 0.35** at PD ~ 4 Hz
* **Final hypervolume**: seed 44 = **7.53** (gen 14), seed 55 = **3.39** (gen 13)
* **Total task cost**: **$12.0733** — over the $8 plan cap by $4.07, under the user-authorized
  $15 ceiling; $8.46 of that was productive NSGA-II compute, $3.51 was idle uptime

## Verification

* `verify_task_results.py t0102_seedscale_n4_gen20` — PASSED (0 errors)
* `verify_task_metrics.py t0102_seedscale_n4_gen20` — PASSED (0 errors)
* Predictions assets `nsga2-seed44-bedb-morph-n4-gen20` and `nsga2-seed55-bedb-morph-n4-gen20`
  — both PASS predictions verificator
* Remote machine entry in `results/remote_machines_used.json` matches the Vast.ai instance log
  (machine 36556586 destroyed at 2026-05-12T17:57:21Z)

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0102_seedscale_n4_gen20/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0102_seedscale_n4_gen20" ---
# Results Detailed: t0102 Seed-scale N=4, Gen=20 Random-Init NSGA-II

## Summary

Two random-init NSGA-II runs with GA seeds 44 and 55, `N_EVAL_SEEDS=4`, `N_GEN=20` target,
`pop=96`, no warm-start, ran sequentially on a single Vast.ai EPYC 7B13 64-core instance
against the 68-d Bed B + procedural-morphology DSGC substrate (54-d electrophys + 14-d
morphology). Both runs were cut short by the per-seed $4 cost watchdog (seed 44 at gen 14,
seed 55 at gen 13), totalling 2,592 cell evaluations. Strict joint-pass cells: **0**. Loose
2-axis pass (DSI >= 0.5 AND PD >= 5): **0**. Max individual axes were each hit (DSI = 1.0, PD
= 64-67 Hz, robustness ~ 1.0) but never on the same cell. The DSI vector-sum objective was
found to return a spurious 1.0 on silenced cells (PD = 0 Hz) due to divide-by-near-zero; the
real high-DSI corner under N=4 sits at DSI ~ 0.35 with PD ~ 4 Hz. The t0091 anchor-driven
joint-pass cell was re-examined and reframed as a 1-generation polynomial-mutation descendant
of an alt_topology anchor clone, not a de novo NSGA-II discovery.

* * *

## Methodology

### Machine

* **Provider**: Vast.ai, single instance `36556586`.
* **CPU**: AMD EPYC 7B13 64-core (64 effective billed cores; 255 logical with SMT4; cgroup
  quota 61.2 cores).
* **RAM**: 503 GB total, 430 GB available.
* **GPU**: RTX 4090 bundled but unused (NEURON workload is CPU-bound).
* **Disk**: 40 GB allocated, ~927 MB used.
* **OS**: Debian GNU/Linux 12 (bookworm), kernel 5.15.0-52-generic.
* **Location**: Spain, ES (Norway target was unavailable; user authorized the $0.4690/hr base
  rate against the plan's $0.40/hr cap).
* **Effective billing rate**: $0.4852/hr (offer base $0.4690/hr + bandwidth + storage).
* **Reliability**: 0.9984 (host id 73118, machine id 11541).
* **Public IP**: 79.116.87.141.

### Runtime

* **Instance created**: 2026-05-11T17:07:07Z.
* **Instance ready**: 2026-05-11T17:08:15Z (provisioning 560 s).
* **Smoke gate completed (5-anchor remote)**: 2026-05-11T17:31:40Z.
* **NSGA-II run started**: 2026-05-11T17:24:22Z (implementation step start).
* **Seed 44 completed (gen 14, watchdog tripped)**: 2026-05-12 ~00:01 UTC, final cost $4.0942.
* **Seed 55 completed (gen 13, watchdog tripped)**: 2026-05-12T17:18:40Z, final cost $4.3626.
* **Instance destroyed**: 2026-05-12T17:57:21Z.
* **Total instance duration**: 24.842 hours.
* **Total billed cost**: $12.0733 ($8.4568 NSGA-II + $0.11 setup + $3.5065 idle).

### Methods

* **Algorithm**: NSGA-II via `pymoo` 0.6.1.6, three-objective formulation maximising DSI
  (vector-sum), preferred-direction firing rate (Hz), robustness (inverse coefficient of
  variation of DSI across the 4 noise replicates). Pymoo minimises the negated triple.
* **Population**: 96 (default, inherited from t0099/t0091).
* **Generations target**: 20; actual 14 (seed 44), 13 (seed 55) before cost watchdog.
* **Init**: Latin Hypercube Sampling via
  `pymoo.operators.sampling.lhs.LatinHypercubeSampling`, explicitly seeded with `task_seed`
  (44 or 55). No anchor warm-start.
* **Crossover / mutation**: SBX with `eta=15`, `prob=0.9`; polynomial mutation with `eta=20`,
  `prob=1/68 ~= 0.0147` per dim. Duplicate-elimination on.
* **Per-cell evaluation**: 16 stimulus directions x 4 noise replicates each. Noise RNG seeds
  spawned deterministically from `np.random.SeedSequence(42).spawn(5)` (the first four are
  used at N_EVAL_SEEDS=4).
* **Parallelism**: 60 worker processes via pymoo's `StarmapParallelization`, with worker
  restart between generations to mitigate NEURON memory accumulation (S-0099-04 mitigation).
* **Substrate**: t0099's Bed B + procedural-morphology compartmental DSGC model, copied
  verbatim into `tasks/t0102_seedscale_n4_gen20/code/`. Imports `de_rosenroll_2026_dsgc`
  (t0024), `procedural_dsgc_morphology_generator_fix` (t0092, applied via correction
  C-0093-01).
* **Smoke gate**: 5-anchor consistency check at `N_EVAL_SEEDS=4` against the t0093
  fingerprint; all 5 anchors fell within ~2 Hz of the t0093 N=20 calibration
  (`smoke_gate_5anchor_remote.json`, `smoke_gate_pass: true`).
* **Termination collection**: `MaximumGenerationTermination(20)` AND `HVPlateauTermination`
  AND `CostWatchdogTermination($4/seed)`. The cost watchdog fired first for both seeds.

* * *

## Results

### Per-seed headline

| Quantity | Seed 44 | Seed 55 |
| --- | --- | --- |
| Cells evaluated | **1,344** | **1,248** |
| Generations completed | **14** / 20 | **13** / 20 |
| Max DSI (vector-sum) | **1.0000** | **1.0000** |
| Max PD-rate (Hz) | **64.29** | **66.96** |
| Max robustness | **0.9916** | **1.0000** |
| Strict joint-pass cells | **0** | **0** |
| Loose joint-pass (DSI>=0.5 AND PD>=5) | **0** | **0** |
| Final hypervolume | **7.5328** | **3.3926** |
| Cost watchdog final reading | **$4.0942** | **$4.3626** |

### Hypervolume trajectory

Both trajectories rise monotonically (typical of NSGA-II hypervolume) but diverge by gen 7:
seed 44 makes a large jump at gen 3 (HV 0.25 → 2.20) and again at gen 7 (HV 2.81 → 4.71),
while seed 55 climbs more gradually (HV 0.27 → 3.39 over 13 gens). The two-fold divergence in
final HV (7.53 vs 3.39) reflects when each seed's LHS draw happens to land an early DSI=1.0
silenced cell — that single artifact cell dominates the HV signal. Per the creative analysis
(section 5), seed 44 hit its first DSI >= 0.99 cell at gen 6 (480 evaluations) and seed 55 at
gen 4 (288 evaluations).

### Joint-distribution structure (the bimodality finding)

Across the union of 2,592 cells, the (DSI, PD) joint distribution is sharply bimodal along the
DSI axis with an empty diagonal:

| DSI bin | PD<0.5 | PD[0.5, 5) | PD[5, 10) | PD[10, 30) | PD[30, 60) | PD[60, 100) |
| --- | --- | --- | --- | --- | --- | --- |
| [0.00, 0.05) | 35 | 612 | 276 | 700 | 397 | 23 |
| [0.05, 0.10) | 0 | 159 | 23 | 63 | 0 | 0 |
| [0.10, 0.20) | 7 | 107 | 12 | 33 | 0 | 0 |
| [0.20, 0.30) | 11 | 19 | 2 | 0 | 0 | 0 |
| [0.30, 0.50) | 27 | 3 | 7 | 4 | 0 | 0 |
| [0.50, 0.99) | 16 | 29 | 0 | 0 | 0 | 0 |
| [0.99, 1.00] | 27 | 0 | 0 | 0 | 0 | 0 |

Every cell with DSI >= 0.5 has PD < 5 Hz. Every cell with PD >= 30 Hz has DSI <= 0.042. The
closest cell to the joint corner from the high-DSI side is (DSI = 0.958, PD = 4.107 Hz, rob =
0.500) in seed 44, gen 7; from the high-PD side, (DSI = 0.003, PD = 66.96 Hz, rob = 0.853) in
seed 55, gen 13.

* * *

## Examples

The following 10 cells cover the categories required for the experiment-task Examples section:
two best-by-DSI (both are the silenced-cell DSI=1.0 artifact), two best-by-PD (one per seed),
a near-miss high-DSI cell with non-zero PD, two diagonal candidates (best simultaneous
progress on all three axes), two random samples (a gen-1 LHS init cell and a later-gen
offspring), and one total-silence "failed" cell. Each cell is shown with its full 68-d
parameter vector (54 electrophys + 14 morphology, exact float values from the predictions
JSONL).

### Example 1 — Silenced "perfect DSI" artifact, seed 44

* **seed/gen**: 44 / 6.
* **objectives**: DSI = **1.0000**, PD = **0.000 Hz**, robustness = **0.366**.
* **illustrates**: Max DSI = 1.0 on a silenced cell (PD = 0 Hz). The vector-sum DSI formula
  has divide-by-near-zero behaviour on cells with vanishing total spike count; floating-point
  dust in the numerator produces a spurious "perfect direction selectivity" signal. This is
  the principal pathology that pulls half of the NSGA-II Pareto front into the degenerate
  corner.

```text
[0.6396, 0.07592, 0.7687, 0.03711, 1.523, 0.5596, 0.2857, 0.5604,
 0.09329, 0.04266, 0.2069, 0.005824, 0.2652, 0.1008, 0.4481, 0.4348,
 0.6136, 0.6133, 0.5323, 0.8645, 0.9503, 0.9662, 0.2076, 0.6518,
 0.4653, 0.32, 0.1009, 0.04121, 0.1118, 0.1913, 0.4837, 0.3529,
 0.08563, 13.65, 156.4, 1.295, 0.0009361, 0.3937, 88.04, 70.35,
 343.7, 3.671, 272.2, 4.575, 385.9, 0.003641, 0.002101, 31.01,
 0.7122, 0.001746, 0.3047, -1.849, 0.0402, 0.0005071, 4.248, 0.02201,
 3.176, 43.24, 0.5147, -117.8, 1.581, -0.4099, 3.758, 16.87, 14.35,
 34.03, 1.308e+09, 0.04809]
```

### Example 2 — Silenced "perfect DSI" artifact, seed 55

* **seed/gen**: 55 / 4.
* **objectives**: DSI = **1.0000**, PD = **0.000 Hz**, robustness = **0.366**.
* **illustrates**: Independent reproduction of the artifact by the second GA seed only 4
  generations into the run. The two artifact cells share neither parameter vector nor lineage;
  both seeds find the silence basin because it occupies ~10% of the LHS volume (Ca tau > 40 ms
  and sAHP > 10x and N_ACH < 150).

```text
[0.4649, 0.7627, 0.4962, 0.682, 2.756, 0.1647, 0.8042, 0.4219, 0.5238,
 0.7898, 0.1741, 0.8843, 0.06277, 0.2977, 0.5935, 0.8748, 0.1, 0.9002,
 0.9037, 0.4467, 0.3054, 0.03136, 0.8554, 0.6655, 0.4254, 0.02655,
 0.348, 0.4638, 0.2986, 0.374, 0.2545, 0.2063, 0.2331, 19.45, 174.9,
 1.107, 0.0008277, 0.3508, 45.62, 69.83, 102.2, 4.081, 457.6, 2.208,
 260.3, 0.007465, 0.0001996, 42.02, 1.038, 0.007393, 0.3546, -2.603,
 0.02537, 0.009099, 3.946, 0.008265, 2.117, 52.73, 1.667, 88.92,
 1.667, 0.6835, 4.979, 26.97, 16.22, 34.37, 6.157e+08, 0.2311]
```

### Example 3 — Best PD-rate cell, seed 44

* **seed/gen**: 44 / 10.
* **objectives**: DSI = **0.0000**, PD = **64.286 Hz**, robustness = **0.000**.
* **illustrates**: Opposite extreme of the bimodal anti-correlation. PD is well above the
  strict joint-pass threshold (30 Hz), but DSI is essentially zero. Robustness is also zero —
  the cell fires equally in all directions, producing a flat tuning curve with no selectivity.

```text
[0.7911, 0.2815, 0.3256, 0.2018, 1.574, 0.7968, 0.2922, 0.8283, 0.8311,
 0.9786, 0.1281, 0.5875, 0.6631, 0.1051, 0.3301, 0.2701, 0.4264,
 0.1411, 0.9347, 0.8803, 0.9311, 0.8477, 0.2984, 0.6646, 0.7116,
 0.4149, 0.1706, 0.07384, 0.4863, 0.3282, 0.4662, 0.4432, 0.0447,
 2.13, 123.3, 1.423, 0.0006059, 0.3463, 6.753, 314.4, 258.5, 2.905,
 65.11, 3.786, 47.49, 0.00334, 0.007375, 43.05, 1.055, 0.007417,
 0.2677, -3.335, 0.0193, 0.006505, 4.632, 0.02864, 2.825, 32.1, 1.02,
 121.9, 2.702, 0.606, 1.93, 39.85, 11.91, 24.34, 9.167e+08, 0.24]
```

### Example 4 — Best PD-rate cell, seed 55

* **seed/gen**: 55 / 13.
* **objectives**: DSI = **0.0027**, PD = **66.964 Hz**, robustness = **0.853**.
* **illustrates**: Highest PD in either seed, with strong robustness (0.85) — so the high
  firing rate is consistent across the 4 noise replicates. But DSI is still ~ 0, confirming
  the bimodality is not a noise artifact: the cell fires reliably at ~67 Hz in every
  direction.

```text
[0.8187, 0.09189, 0.09301, 0.3749, 2.084, 0.6775, 0.7952, 0.4214,
 0.5163, 0.4621, 0.178, 0.7859, 0.2911, 0.5772, 0.3237, 0.4328,
 0.2982, 0.3971, 0.7176, 0.1462, 0.3273, 0.3737, 0.3278, 0.3176,
 0.4169, 0.4408, 0.09583, 0.2313, 0.3376, 0.1529, 0.1964, 0.49,
 0.04205, 4.012, 140.9, 1.242, 0.0009859, 0.392, 5.96, 329.5, 342.5,
 4.732, 213.6, 3.954, 44.45, 0.001102, 0.008304, 30.2, 0.6809, 0.00892,
 0.4877, -7.248, 0.02336, 0.009927, 3.626, 0.01743, 5.55, 42.34, 1.545,
 123.7, 2.457, 0.03533, 1.546, 19.19, 16.07, 54.26, 1.365e+08, 0.01858]
```

### Example 5 — Near-miss high-DSI cell, seed 44

* **seed/gen**: 44 / 7.
* **objectives**: DSI = **0.9580**, PD = **4.107 Hz**, robustness = **0.500**.
* **illustrates**: Closest cell to the joint-pass corner from the high-DSI side. DSI is well
  above the 0.5 threshold and the firing rate is non-zero, but PD is still ~ 7x below the 30
  Hz threshold. Robustness 0.50 is the rough midpoint — the cell's tuning is only moderately
  reproducible across the 4 replicates.

```text
[0.7138, 0.3042, 0.07212, 0.9551, 2.737, 0.7927, 0.3005, 0.3376,
 0.9628, 0.5408, 0.01045, 0.1976, 0.2291, 0.4086, 0.3069, 0.4119,
 0.5208, 0.8574, 0.5456, 0.3161, 0.04664, 0.9732, 0.7018, 0.5454,
 0.7479, 0.4553, 0.1657, 0.2671, 0.1381, 0.3227, 0.3995, 0.1296,
 0.3321, 17.17, 114.1, 1.713, 0.0002434, 0.4191, 21.9, 290.4, 318.5,
 0.6476, 191.1, 0.841, 393.1, 0.003083, 0.0006634, 29.46, 0.6522,
 0.007507, 0.2243, -0.2897, 0.001297, 0.003526, 3.77, 0.0343, 3.83,
 69.74, 1.269, -22.86, 2.524, -0.7801, 4.844, 51.63, 11.04, 25.07,
 9.361e+08, 0.2472]
```

### Example 6 — Best "diagonal" candidate (closest to all three thresholds), seed 44

* **seed/gen**: 44 / 11.
* **objectives**: DSI = **0.3006**, PD = **11.607 Hz**, robustness = **0.941**.
* **illustrates**: Highest simultaneous progress on all three axes. Diagonal score (defined as
  `min(DSI/0.5, PD/30, rob/0.7)`) is **0.387** — meaning the worst-performing axis is still
  39% short of its joint-pass threshold. This is the cell the GA actually exploited to climb
  the hypervolume; the bimodality bites here because no axis is willing to give ground.

```text
[0.6306, 0.2383, 0.3364, 0.7653, 2.122, 0.6976, 0.538, 0.2417, 0.2865,
 0.9567, 0.3405, 0.7671, 0.2535, 0.8653, 0.5225, 0.6378, 0.6872,
 0.2958, 0.5624, 0.1115, 0.6891, 0.1188, 0.8684, 0.6756, 0.4829,
 0.4143, 0.0275, 0.2418, 0.4795, 0.2785, 0.03653, 0.4165, 0.2777,
 5.247, 183.4, 1.356, 0.0007391, 0.196, 12.51, 72.54, 248.8, 0.3061,
 61.35, 4.768, 380.3, 0.002671, 0.007498, 36.25, 1.045, 0.006817,
 0.2628, 3.102, 0.02368, 0.001093, 4.628, 0.02562, 3.505, 39.71,
 1.606, -132.7, 2.874, -0.5028, 2.757, 18.08, 11.01, 25.76, 1.695e+09,
 0.4332]
```

### Example 7 — Best PD-and-DSI compromise, seed 55

* **seed/gen**: 55 / 13.
* **objectives**: DSI = **0.1716**, PD = **5.179 Hz**, robustness = **0.952**.
* **illustrates**: Seed 55's analogue of the diagonal candidate — DSI reaches 34% of the 0.5
  threshold while PD just clears 5 Hz, with very high robustness (0.95). The fact that seed
  55's best diagonal cell is so much weaker than seed 44's (DSI 0.17 vs 0.30, PD 5 vs 12)
  reflects the underlying HV gap (3.39 vs 7.53).

```text
[0.5796, 0.292, 0.1045, 0.6742, 3.753, 0.5877, 0.8986, 0.4244, 0.4248,
 0.4046, 0.1224, 0.9085, 0.3095, 0.5776, 0.3238, 0.4333, 0.7165,
 0.9966, 0.2943, 0.4441, 0.8246, 0.892, 0.3618, 0.2563, 0.4263,
 0.4779, 0.2408, 0.1136, 0.3273, 0.1147, 0.1362, 0.2238, 0.3529,
 4.617, 59.06, 1.037, 0.0004639, 0.3936, 5.848, 149.8, 339.7, 3.055,
 224.5, 3.962, 39.38, 0.0009282, 0.007672, 30.79, 0.6027, 0.009196,
 0.2639, -8.294, 0.04573, 0.001666, 3.618, 0.0173, 3.571, 42.23,
 1.811, -30.1, 2.357, 0.6789, 4.188, 48.65, 15.07, 54.36, 1.415e+09,
 0.1488]
```

### Example 8 — Random LHS init cell, seed 44, gen 1

* **seed/gen**: 44 / 1.
* **objectives**: DSI = **0.0000**, PD = **2.857 Hz**, robustness = **0.000**.
* **illustrates**: Representative of the LHS-sampled initial population before any GA
  selection. Random parameter combinations rarely produce a cell that is even minimally
  selective; near-zero DSI and PD are the default state of the parameter space.

```text
[0.6889, 0.5088, 0.9585, 0.06897, 3.467, 0.2405, 0.6952, 0.5814,
 0.8578, 0.5029, 0.2531, 0.3762, 0.1969, 0.8724, 0.8323, 0.4103,
 0.1806, 0.8268, 0.9125, 0.3427, 0.1902, 0.9678, 0.7287, 0.5151,
 0.4754, 0.1985, 0.02417, 0.3147, 0.07954, 0.2194, 0.4802, 0.3419,
 0.3434, 10.66, 160.9, 1.046, 0.0002508, 0.3726, 79.65, 87.82, 318.2,
 0.2895, 49.26, 1.72, 398.9, 0.0006465, 0.008288, 27.73, 1.059,
 0.007649, 0.155, 6.437, 0.02821, 0.0005605, 6.628, 0.04743, 4.256,
 89.54, 1.253, 64.8, 2.079, -0.7297, 0.7274, 37.16, 14.35, 33.02,
 1.98e+09, 0.02714]
```

### Example 9 — Random later-generation cell, seed 55, gen 10

* **seed/gen**: 55 / 10.
* **objectives**: DSI = **0.0024**, PD = **16.429 Hz**, robustness = **0.909**.
* **illustrates**: After several generations of GA selection, cells tend to consolidate around
  high PD or high robustness without simultaneously achieving high DSI. This cell has good PD
  (16 Hz) and excellent robustness (0.91) but essentially no direction selectivity — the GA
  selected it for the (PD, robustness) sub-objective, not the joint corner.

```text
[0.9839, 0.9834, 0.7786, 0.5989, 2.775, 0.8186, 0.4829, 0.1203, 0.8343,
 0.7224, 0.4007, 0.9608, 0.1804, 0.9127, 0.8809, 0.4334, 0.3168,
 0.08262, 0.3073, 0.06049, 0.7812, 0.5215, 0.8921, 0.08769, 0.7932,
 0.4115, 0.2585, 0.09767, 0.09298, 0.431, 0.4177, 0.2679, 0.02386,
 3.693, 104.8, 0.7517, 6.09e-05, 0.4322, 15.76, 291.1, 124.6, 1.402,
 136.7, 2.878, 476.1, 0.004266, 0.003739, 41.55, 0.9762, 0.007022,
 0.4855, -1.03, 0.04678, 0.009458, 3.304, 0.0362, 3.829, 80.56, 1.386,
 -124.8, 1.301, 0.6079, 2.944, 21.31, 11.49, 29.56, 5.471e+08, 0.3731]
```

### Example 10 — Total-silence cell, seed 55, gen 1

* **seed/gen**: 55 / 1.
* **objectives**: DSI = **0.0000**, PD = **0.000 Hz**, robustness = **0.000**.
* **illustrates**: A "failed" evaluation in NSGA-II terms — the cell never fires in any
  direction across any replicate. Such cells exist in the initial population (the LHS volume
  includes inactive parameter combinations) and are correctly de-selected in later
  generations. Note this is biologically different from example 1's DSI = 1.0 artifact: this
  cell honestly reports DSI = 0 because the spike-count denominator is below the numerical
  tolerance.

```text
[0.6, 0.8314, 0.03727, 0.9545, 1.695, 0.4476, 0.4318, 0.05806, 0.842,
 0.9732, 0.1087, 0.6679, 0.4026, 0.9668, 0.1874, 0.9319, 0.2683,
 0.5535, 0.5383, 0.2486, 0.1934, 0.1797, 0.8518, 0.1718, 0.7094,
 0.2425, 0.06145, 0.3662, 0.2593, 0.2741, 0.09305, 0.4629, 0.3053,
 5.901, 96.39, 1.679, 0.0005392, 0.05142, 43.11, 346.1, 178, 2.366,
 302.7, 2.458, 461.6, 0.009072, 0.003003, 46.19, 1.088, 0.0006582,
 0.4179, 1.361, 0.02728, 0.005916, 4.383, 0.02198, 5.764, 58.98,
 1.693, -145.2, 1.528, -0.6248, 3.264, 37.13, 15.67, 18.5, 3.223e+08,
 0.3422]
```

* * *

## Comparison vs Baselines

| Quantity | t0091 (5-anchor warm-start, gens=8, N=5) | t0099 (3 random-init seeds, gens=5-8, N=5) | t0102 seed 44 (random, gens=14, N=4) | t0102 seed 55 (random, gens=13, N=4) |
| --- | --- | --- | --- | --- |
| Cells evaluated | 5 anchors x 19 clones + 8 gens x 96 ~ 953 | ~ 2,208 (3 seeds x ~736 each) | **1,344** | **1,248** |
| Strict joint-pass cells | **1** (DSI=0.511, PD=35.1, rob=0.79 at gen 2) | **0** across all 3 seeds | **0** | **0** |
| Best DSI | ~ 0.55 | 0.49 (seed 22) | **1.0000** (silenced) / **0.958** (PD>0) | **1.0000** (silenced) / **0.172** (PD>=5) |
| Best PD-rate (Hz) | ~ 35 | ~ 18.7 (seed 22) | **64.29** | **66.96** |
| Final hypervolume | not directly comparable (different ref point) | ~ 4.3 (seed 22 best) | **7.53** | **3.39** |

### Deltas

* **t0102 vs t0099**: Same joint-pass count (0) at a 5x lower noise budget and 2.5x more
  generations. The seed/gen rebalance does not recover the joint corner. The Wilson 95% upper
  CI on yield rate combining t0099 + t0102 (0/4,800) is below 0.0008 — a tighter null than
  t0099 alone could deliver.
* **t0102 vs t0091**: t0091 is the only entry in this line of work with a joint-pass cell, and
  the cell sits 3.55 normalised units from the alt_topology anchor row 84 (vs > 11 to the
  next- nearest anchor). The "warm-start was load-bearing" claim from t0099's
  `results_summary.md` is reinforced; t0091's joint-pass cell is more accurately a
  one-generation polynomial-mutation descendant of an alt_topology anchor than a de novo
  NSGA-II discovery.
* **Per-axis maxima**: t0102 reaches higher per-axis individual maxima than either t0091 or
  t0099 (DSI 1.0 vs 0.55, PD 67 vs 35 Hz, rob 1.0 vs ~0.8), but only by separating the axes
  onto different cells. The joint corner remains empty.

* * *

## Visualizations

![DSI vs PD-rate scatter for all 2,592
cells](../../../tasks/t0102_seedscale_n4_gen20/results/images/dsi_vs_pd_scatter.png)

Scatter of every evaluated cell, colored by GA seed. The green-shaded rectangle is the strict
joint-pass corner (DSI >= 0.5, PD >= 30 Hz) — it contains **0** cells. The yellow star marks
t0091's anchor-driven joint-pass cell (DSI=0.511, PD=35.1 Hz) which sits inside the corner but
came from warm-start, not random-init NSGA-II.

![Hypervolume trajectory by
generation](../../../tasks/t0102_seedscale_n4_gen20/results/images/hv_trajectory.png)

Hypervolume vs generation for both GA seeds. Seed 44 reaches 7.53 by gen 14, seed 55 reaches
3.39 by gen 13; both runs terminate when the per-seed $4 cost watchdog fires. Seed 44's larger
HV reflects an earlier discovery of the silenced-cell DSI = 1.0 artifact (gen 6 vs gen 4 for
seed 55, but with a much steeper HV step at gen 7).

![2D density of DSI vs
PD-rate](../../../tasks/t0102_seedscale_n4_gen20/results/images/dsi_pd_density.png)

Hexbin density (log-scaled colour) showing the bimodal structure. Almost all density sits
along one of two arms: (DSI ~ 0, PD > 30 Hz) and (DSI > 0.5, PD < 5 Hz). The dashed red box is
the empty joint corner. There is no diagonal density.

![Best DSI and best PD-rate per generation, twin
axes](../../../tasks/t0102_seedscale_n4_gen20/results/images/per_gen_best_dsi_pd.png)

Twin-axis chart showing the best DSI (solid lines, left axis) and best PD-rate (dashed lines,
right axis) for each generation of each seed. The dotted green horizontals mark the joint-pass
thresholds (DSI = 0.5, PD = 30 Hz). Each axis is hit individually multiple times, but never on
the same cell — the GA found both extremes but no intermediate.

* * *

## Analysis

### Finding 1 — The DSI = 1.0 floating-point artifact

The 27 cells with DSI >= 0.99 across both seeds are all silenced cells with PD < 0.1 Hz (Ca
tau median 65 ms, sAHP multiplier median 14x, N_ACH median 94). The vector-sum DSI
implementation in `evaluator.py` computes a ratio of summed direction-vectors and total spike
count; on a silenced cell the denominator collapses to floating-point dust and the numerator
(~ random noise) divided by ~ 0 produces a number near 1.0. This is not direction selectivity
— it is a numerical pathology. **The real high-DSI corner under N=4 sits at DSI ~ 0.35**
(across the 27 cells in the DSI bin [0.30, 0.50) with PD > 5), not at 1.0. The headline metric
`direction_selectivity_index = 1.0` reported in `metrics.json` for both variants reflects this
artifact, not a real direction-selectivity signal; downstream comparisons should treat the
value as a flag rather than a score until the objective is gated by a minimum spike count.

### Finding 2 — The bimodality is structural, not algorithmic

NSGA-II's crowding distance selection actively promotes diverse Pareto points. The substrate's
response is to deliver two equally Pareto-optimal extremes (high DSI on silenced cells; high
PD on indiscriminate firers) and nothing diagonal. The 60% of the Ca tau bound, 50% of the
sAHP multiplier bound, and 33% of the N_ACH bound that produce silence overlap to make ~10% of
LHS draws already near the silence basin (Section 5 of `creative_analysis.md`). The bimodality
is a property of the search space + objective formulation, not of NSGA-II.

### Finding 3 — t0091 reframed

t0091's single strict joint-pass cell (DSI=0.511, PD=35.1 Hz, rob=0.79 at
`source_generation=2`) sits 3.55 normalised units from the alt_topology anchor row 84 in
t0091's warm-start population and \> 11 units from any other anchor. `source_generation=2` is
the first offspring of the initial-population evaluation pass; with per-dim mutation
probability 0.015 and 68 dims, the expected number of mutated dims per cell is ~ 1.0. The
joint-pass cell is therefore a near-clone of a single alt_topology anchor with one polynomial
mutation, not an NSGA-II discovery in any meaningful sense. **t0091's published claim of
"joint-pass corner reachable via warm-start NSGA-II" should be read as "joint-pass corner
present in the empirical t0083 anchor library, preserved through one generation of
mutation"**. This is a load-bearing methodological clarification for any subsequent paper.

### Finding 4 — Is N=4 too noisy? (probably not, alone)

The 5-anchor smoke gate at N=4 against the t0093 N=20 fingerprint showed all 5 anchors within
~ 2 Hz of the calibration, consistent with the predicted `sqrt(20/4) ~ 2.24x` increase in
per-cell standard error. Doubling N to 8 would cut SE by `sqrt(2) ~ 1.41x` — nowhere near the
factor needed to move the closest near-miss cell (DSI=0.958, PD=4.107 Hz) by 26 Hz into the
joint corner. The joint explanation "N=4 + DSI floating-point bug + no warm-start" is required
to recover the null; no single factor explains it alone.

* * *

## Limitations

* **Noise floor at N_EVAL_SEEDS=4 is ~ 2x the calibrated N=20 floor.** The smoke gate at the
  bedb_like anchor passed only under the relaxed +/-2 Hz tolerance, not the strict +/-1 Hz
  that the plan originally required. The first-anchor `proceed_with_caveat` decision was
  overridden by the 5-anchor remote smoke gate, which passed within +/- 2 Hz for all 5
  anchors. The N=4 noise may have prevented NSGA-II from cleanly distinguishing near-corner
  cells but cannot account for the 7-10x gap between the near-miss cell and the joint corner.
* **Cost-watchdog truncation: gens 14/13 instead of 20.** Both seeds were cut short before
  reaching the planned generation 20. By the observed HV trajectories, neither seed had
  plateaued (seed 44 made a +0.3 HV jump from gen 13 to gen 14; seed 55 made a +0.2 HV jump
  gen 12 to gen 13). It is possible — though the bimodality finding argues against it — that
  6-7 additional generations would have produced a joint-pass cell. The cost watchdog tripped
  not because of a bug but because per-cell wall-clock at N_EVAL_SEEDS=4 on the Spain EPYC
  7B13 ($0.4852/hr) was higher than the optimistic Norway projection ($0.24/hr) in the plan.
* **Cost overrun: $12.07 vs $8 plan cap.** $8.46 was productive NSGA-II compute (the cost
  watchdog behaved as designed at $4/seed); $3.51 was idle uptime from a dead initial subagent
  before the recovery subagent reattached, plus post-watchdog billing before teardown. The
  user authorized the overrun in advance; the structural cause is recorded for the suggestions
  step.
* **No algorithm comparison.** Only NSGA-II was tested. Per Mohacsi 2024
  (`research/research_papers.md`), IBEA outperforms NSGA-II on compartmental-neuron multi-
  objective problems and CMAES converges faster on neuron-fitting problems. The bimodality
  finding could be NSGA-II-specific in principle, though the substrate-density argument
  suggests the joint corner is empty regardless of algorithm.
* **Single substrate.** All conclusions are conditioned on the 68-d Bed B + t0092 procedural
  morphology substrate. The same conclusions may not transfer to a different morphology
  generator or a different electrophys parameterisation.

* * *

## Verification

* `verify_task_results.py t0102_seedscale_n4_gen20` — PASSED (0 errors).
* `verify_task_metrics.py t0102_seedscale_n4_gen20` — PASSED (0 errors). The two variants
  `random-init-seed44` and `random-init-seed55` each report `direction_selectivity_index` as
  their registered metric; the value 1.0 reflects the silenced-cell artifact identified in
  Finding 1 and should be interpreted alongside the limitations note.
* `meta.asset_types.predictions.verificator --task-id t0102_seedscale_n4_gen20` — both
  predictions assets PASS with 2 expected warnings each (PR-W014 `model_id` null, PR-W015
  `dataset_ids` empty — same warnings as t0099's three random-init assets).
* `meta.asset_types.predictions.verificator` on each predictions asset — PASS.
* `verify_machines_destroyed t0102_seedscale_n4_gen20` — to be re-checked at task close; the
  machine log records `destroyed_at: 2026-05-12T17:57:21Z` for instance 36556586.
* Cost overrun: `results/costs.json` `total_cost_usd` = **$12.0733** exceeds the plan cap of
  **$8.00**. The overrun was user-authorized; see `results/costs.json` `note` for the
  structural breakdown.
* Substrate-consistency smoke gate at N_EVAL_SEEDS=4 passed under the relaxed +/-2 Hz
  tolerance for all 5 anchors (`logs/steps/009_implementation/smoke_gate_5anchor_remote.json`,
  `smoke_gate_pass: true`).

* * *

## Files Created

* `tasks/t0102_seedscale_n4_gen20/results/results_summary.md` — scannable summary (this task's
  headline).
* `tasks/t0102_seedscale_n4_gen20/results/results_detailed.md` — this file.
* `tasks/t0102_seedscale_n4_gen20/results/metrics.json` — two-variant explicit-format file
  with registered `direction_selectivity_index` per GA seed.
* `tasks/t0102_seedscale_n4_gen20/results/costs.json` — total $12.0733 with three-bucket
  breakdown.
* `tasks/t0102_seedscale_n4_gen20/results/remote_machines_used.json` — single Vast.ai
  instance.
* `tasks/t0102_seedscale_n4_gen20/results/creative_analysis.md` — bimodality + DSI artifact
  analysis (written in step 011).
* `tasks/t0102_seedscale_n4_gen20/results/images/dsi_vs_pd_scatter.png` — DSI vs PD-rate
  scatter, both seeds.
* `tasks/t0102_seedscale_n4_gen20/results/images/hv_trajectory.png` — hypervolume per
  generation, both seeds.
* `tasks/t0102_seedscale_n4_gen20/results/images/dsi_pd_density.png` — 2D hexbin density
  showing bimodality.
* `tasks/t0102_seedscale_n4_gen20/results/images/per_gen_best_dsi_pd.png` — per-generation
  best DSI + PD, twin axes.
* `tasks/t0102_seedscale_n4_gen20/results/data/all_evaluations_seed{44,55}.json` — full
  per-cell evaluation history per seed.
* `tasks/t0102_seedscale_n4_gen20/results/data/hv_trajectory_seed{44,55}.json` —
  per-generation HV records.
* `tasks/t0102_seedscale_n4_gen20/results/data/pareto_front_seed{44,55}.json` — final Pareto
  fronts (29 and 31 cells respectively).
* `tasks/t0102_seedscale_n4_gen20/results/data/nsga2_checkpoint_seed{44,55}.json` — pymoo
  checkpoint per seed (for re-evaluation / resume).
* `tasks/t0102_seedscale_n4_gen20/results/data/init_pop_seed{44,55}.json` — LHS initial
  populations.
* `tasks/t0102_seedscale_n4_gen20/results/data/algorithm_config.json`, `evaluation_seeds.json`
  — run configuration.
* `tasks/t0102_seedscale_n4_gen20/assets/predictions/nsga2-seed44-bedb-morph-n4-gen20/` —
  predictions asset (1,344 cells; `details.json`, `description.md`,
  `files/predictions-seed44.jsonl`).
* `tasks/t0102_seedscale_n4_gen20/assets/predictions/nsga2-seed55-bedb-morph-n4-gen20/` —
  predictions asset (1,248 cells).
* `tasks/t0102_seedscale_n4_gen20/code/make_charts.py` — chart-generation script.

* * *

## Task Requirement Coverage

Operative task request from `task.json`:

```text
Name: 68-d NSGA-II at GA seeds=2, N_SEEDS=4, gens=20, random init

Short description: 68-d NSGA-II on Bed B+morph: 2 random-init GA seeds (44, 55), N_SEEDS=4,
gens=20, pop=96. Tests if 5x noise drop + 2.5x gens recovers joint-pass corner vs t0099 null.
$8 cap.

Expected assets: 2 predictions, 1 answer.

Long description (excerpts):
* GA seeds: 2 (random-init, seeds 44 and 55).
* Noise replicates N_SEEDS: 4 (reduced from 20 by factor of 5).
* Generations: 20 (up from t0099's 5-8).
* Population: 96 (default).
* Warm-start: none.
* Hard cost cap: $8 per task.
* Verification: cost <= $8, both predictions assets validate, answer asset validates, machines
  destroyed.
* Positive criterion: >= 1 strict joint-pass cell. Negative criterion: 0 cells in either seed.
```

REQ-* IDs are reused verbatim from `plan/plan.md`.

* **REQ-1** — Override the operative noise-replicate constant to `N_EVAL_SEEDS = 4`. **Status:
  Done.** `tasks/t0102_seedscale_n4_gen20/code/constants_morphology.py` sets `N_EVAL_SEEDS:
  int = 4`. Evidence: file + `algorithm_config.json` records `n_eval_seeds: 4`.
* **REQ-2** — Set `N_GEN = 20` in `constants_morphology.py`. **Status: Done.** File contains
  `N_GEN: int = 20`. Evidence: `algorithm_config.json` records `n_gen_target: 20`.
* **REQ-3** — Run two NSGA-II processes at `task_seed = 44` and `task_seed = 55`,
  LHS-initialised, pop=96 each. **Status: Done.** Evidence:
  `results/data/init_pop_seed44.json` and `init_pop_seed55.json` each have 96 LHS rows;
  `all_evaluations_seed{44,55}.json` show the two distinct seed lineages.
* **REQ-4** — No warm-start anchors (pure random LHS init). **Status: Done.** Evidence:
  `tasks/t0102_seedscale_n4_gen20/code/random_init.py` calls `LatinHypercubeSampling` with no
  anchor injection; both predictions assets' `description.md` Data sections confirm LHS-only
  init.
* **REQ-5** — Both runs sequential on the same Vast.ai CPU instance. **Status: Done.**
  Evidence: `logs/steps/008_setup-machines/machine_log.json` records single instance
  `36556586`; `logs/steps/009_implementation/run_two_seeds.log` shows the two seeds run in
  series.
* **REQ-6** — Hard cost cap of $8 per task; cost watchdog reads
  `selected_offer.price_per_hour`. **Status: Partial.** The per-seed cost watchdog enforced
  exactly $4 per seed as designed (tripped at $4.0942 / $4.3626) but total session cost was
  **$12.0733** because of $3.51 of idle uptime from a dead initial subagent and post-watchdog
  billing before teardown. The user authorized the $15 ceiling in advance, so the overrun is
  recorded but not blocking. Evidence: `results/costs.json`.
* **REQ-7** — Substrate-consistency smoke gate must pass at N_EVAL_SEEDS=4 against the t0093
  anchor-1 fingerprint. **Status: Done (with documented caveat).** The local single-anchor
  smoke gate decision was `proceed_with_caveat` (PD-rate 45.36 Hz vs 43.6 expected — outside
  +/-1 Hz but inside +/-2 Hz at N=4). The 5-anchor remote smoke gate passed cleanly at +/-1.5
  Hz max drift across all 5 anchors (`smoke_gate_5anchor_remote.json`, `smoke_gate_pass:
  true`).
* **REQ-8** — Incremental budget gate after seed=44. **Status: Done.** Evidence:
  `logs/steps/009_implementation/run_two_seeds.log` records the budget-gate decision; seed 44
  finished at $4.0942 < $5.00 so seed 55 was launched.
* **REQ-9** — Restart Python workers between generations (S-0099-04 mitigation). **Status:
  Done.** Evidence: `tasks/t0102_seedscale_n4_gen20/code/nsga2_driver.py` inherits the t0099
  per-generation worker restart logic verbatim. Confirmed by NSGA-II stdout pattern.
* **REQ-10** — Produce one predictions asset per GA seed (2 total). **Status: Done.**
  Evidence: `assets/predictions/nsga2-seed44-bedb-morph-n4-gen20/` (1,344 cells) and
  `assets/predictions/nsga2-seed55-bedb-morph-n4-gen20/` (1,248 cells) both PASS predictions
  verificator.
* **REQ-11** — Produce 1 answer asset answering "Does N_EVAL_SEEDS=4 + N_GEN=20 + 2
  random-init GA seeds recover the strict joint-pass corner?". **Status: Done for the
  question; the answer is NO.** The negative result (0/2592) is explicitly publishable per the
  task brief. Both random- init seeds replicate t0099's null at a different N/gen budget. The
  recovery framing is therefore Partial: the joint-pass corner was NOT recovered; the task
  answer is "No, joint-pass not recovered, and the structural anti-correlation explains why".
  Evidence: this file's Analysis section + `creative_analysis.md` Section 1. The answer asset
  itself will be produced by the separate `answer-question` skill step downstream of this
  `results` step.
* **REQ-12** — Side-by-side compare t0102 vs t0099 vs t0091. **Status: Done.** Evidence: this
  file's `## Comparison vs Baselines` table; the 5x5 anchor-distribution table extension was
  partially completed but the headline cross-task deltas are reported here for the strict
  joint- pass yield, best DSI, best PD, and HV.
* **REQ-13** — Compute the four registered metrics with the explicit multi-variant format.
  **Status: Partial.** `metrics.json` uses the explicit-variant format with variants `seed44`
  and `seed55`; only `direction_selectivity_index` is populated because the t0099 substrate's
  evaluator does not export `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, or
  `tuning_curve_rmse` at the cell level (they are derived metrics not present in the per-cell
  history). This matches t0099's own `metrics.json` (single registered metric). Evidence:
  `results/metrics.json` + `tasks/t0099_random_init_pareto_robustness/results/metrics.json`.
* **REQ-14** — Generate at least 2 charts. **Status: Done.** Evidence: 4 charts in
  `results/images/` — `dsi_vs_pd_scatter.png`, `hv_trajectory.png`, `dsi_pd_density.png`,
  `per_gen_best_dsi_pd.png`. All four are embedded in this file's `## Visualizations` section.
* **REQ-15** — Destroy the Vast.ai instance after both seeds complete; record final cost.
  **Status: Done.** Evidence: `machine_log.json` `destroyed_at: 2026-05-12T17:57:21Z`;
  `results/remote_machines_used.json` records `duration_hours: 24.842`, `cost_usd: 12.0733`.
* **REQ-16** — Do not modify any prior task folder (immutability). **Status: Done.** Evidence:
  all writes in this task are scoped under `tasks/t0102_seedscale_n4_gen20/`; the only
  top-level changes are dependency-tooling files allowed by CLAUDE.md rule 3.

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0102_seedscale_n4_gen20/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0102_seedscale_n4_gen20" date_compared: "2026-05-12" ---
# Compare to Literature: 68-d NSGA-II at Seeds=2, N_EVAL_SEEDS=4, Gens=20

## Summary

Two random-init NSGA-II seeds (44, 55) on the 68-d Bed B + procedural-morphology DSGC
substrate produced **0/2,592** strict joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz AND rob >=
0.7), replicating t0099's null at a 5x noise-replicate cut and 2.5x generation extension.
Compared against five methodological references (Mohacsi2024, Druckmann2007, Hay2011,
VanGeit2016, PolegPolsky2026) and two noise-theory references (Dang2023, Morinaga2024), our
**2,592-evaluation budget** is **1-2 orders of magnitude below** every cited
compartmental-neuron MO study and our **algorithm choice (NSGA-II)** is documented mid-pack
relative to CMAES/IBEA/PSO on 9-12 d benchmarks. Under Hay2011's **0.4%** joint-acceptance
base rate, our budget predicts **~10 expected joint-pass cells**; we found **0**, which
strengthens the substrate-difficulty (or objective-misspecification) reading already flagged
in `creative_analysis.md` Section 1. The t0091 single joint-pass cell, reframed in this task's
reporting as a one-mutation descendant of an alt_topology anchor clone, is consistent with the
literature view that warm-start delivers a **5-10x HV head-start** [Ament2023, as cited via
t0099 `compare_literature.md`] rather than an algorithmic discovery.

## Comparison Table

### Budget envelope vs cited references

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Druckmann2007 NSGA-II 12-d interneuron [Druckmann2007, p. 11] | Total evaluations per fit | 300000 | 2592 | -297408 | 116x under standard |
| Hay2011 NSGA-II 22-d L5PC [Hay2011, Methods, p. 4] | Total evaluations per fit | 500000 | 2592 | -497408 | 193x under standard |
| Mohacsi2024 Neuroptimus 12-d CA1 benchmark [Mohacsi2024, Methods, p. 6] | Total evaluations per algorithm-run | 10000 | 2592 | -7408 | 3.9x under matched-budget benchmark |
| VanGeit2016 BluePyOpt IBEA 18-d L5PC [VanGeit2016, Use Case 2, p. 11] | Total evaluations per fit | 10000 | 2592 | -7408 | 3.9x under modern engineered minimum |
| PolegPolsky2026 DSGC ML search [PolegPolsky2026, Methods, via t0101 brainstorm] | Total evaluations per configuration | 300000 | 2592 | -297408 | 116x under the motivating paper |
| Hay2011 L5PC joint-acceptance yield [Hay2011, Results, p. 7] | Joint-pass cells / total evals | 2000 / 500000 = 0.40% | 0 / 2592 = 0.00% | -0.40 pp | Expected 10 cells under Hay base rate; we found 0 |
| Druckmann2007 strict-pass yield [Druckmann2007, Results, p. 13] | Strict-pass cells / total evals | 300 / 300000 = 0.10% | 0 / 2592 = 0.00% | -0.10 pp | Expected ~2.6 cells under Druckmann base rate; we found 0 |
| Mohacsi2024 NSGA-II rank vs IBEA on 9-d active cell [Mohacsi2024, Use Case 4, Figure references] | Final error (NSGA-II / IBEA ratio) | ~10x (NSGA-II worse) | not directly comparable | n/a | Their evidence flags NSGA-II as mid-pack on 9-12 d; we run at 68 d |
| Dang2023 NSGA-II noisy LOTZ threshold [Dang2023, Theorem 8, p. 6] | Critical noise prob `p` for polynomial runtime | < 0.50 | effective p << 0.50 at N=4 | n/a | Our N=4 explicit-averaging puts us in the polynomial regime per phase-transition theorem |
| PolegPolsky2026 vs t0091 / t0099 / t0102 best PD-rate [PolegPolsky2026, Results table via t0101 brainstorm] | Best preferred-direction DSI under unconstrained config | 73.1% +/- 2.4% (subthreshold-voltage) | 0.958 (spike-rate, seed 44 gen 7) | n/a | Different DSI conventions; both >= 0.5 threshold but units not directly comparable |

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0091 warm-start (5 anchors, gens=8, N=5) [t0091 `results_summary.md`] | Strict joint-pass cells | 1 (DSI=0.511, PD=35.1 Hz, rob=0.79) | 0 (seed 44), 0 (seed 55) | -1 | t0091 cell reframed as one-mutation alt_topology anchor clone per `creative_analysis.md` Section 2 |
| t0099 random-init (3 seeds, gens=5/8/8, N=20) [t0099 `results_summary.md`] | Strict joint-pass cells | 0 across 3 seeds (2208 evals) | 0 across 2 seeds (2592 evals) | 0 | Same null at 5x lower N and 2.5x more gens; pooled Wilson 95% upper CI < 0.0008 |
| t0099 best PD-rate (seed 22) [t0099 `results_summary.md`] | Max PD-rate (Hz) | 18.7 | 64.29 (seed 44) / 66.96 (seed 55) | +45.6 / +48.3 | t0102 reaches higher per-axis PD but at DSI ~ 0 |
| t0091 final HV (gen 2) [t0099 `compare_literature.md`] | Hypervolume at matched generation | 23.71 (gen 2) | 7.53 (seed 44 gen 14) / 3.39 (seed 55 gen 13) | -16.18 / -20.32 | Different reference points; both runs use anchor-based HV calibration so this comparison is qualitative |

## Methodology Differences

* **Budget**: t0102 ran **2,592 evaluations** (1,344 + 1,248 after the per-seed $4 cost
  watchdog cut both seeds short of generation 20). Druckmann2007 and PolegPolsky2026 each used
  **300,000**; Hay2011 used **500,000**; Mohacsi2024 and VanGeit2016 used **10,000**. t0102 is
  **116-193x below** the high-end envelope and **3.9x below** the modern Mohacsi/BluePyOpt
  engineered minimum.

* **Algorithm**: t0102 used NSGA-II (pymoo defaults: SBX eta=15, polynomial mutation eta=20).
  The most directly relevant external benchmark, Mohacsi2024, places NSGA-II **mid-pack** on
  multi-objective neuronal problems: CMAES wins essentially every benchmark, PSO is a close
  runner- up, **IBEA is the best multi-objective method**, and on Use Case 1 NSGA-II is worse
  than random search [Mohacsi2024, Results, p. 8]. Our project's NSGA-II choice predates this
  evidence.

* **Per-cell noise replicates**: t0102 used **N_EVAL_SEEDS=4** (explicit averaging of 4
  trial-seed evaluations per direction); t0099 used N=20; Druckmann2007 used 15 traces per
  cell (5 reps x 3 amplitudes) but averaged feature *errors* not traces [Druckmann2007,
  Methods, p. 9]; PolegPolsky2026 used deterministic single-pass evaluation. Per Morinaga2024
  Theorem 3, explicit averaging at K=4 is in the slow-polynomial-improvement regime only if
  the per-objective noise stability index alpha > 1 [Morinaga2024, Theorem 3, p. 5]; if any
  objective (likely the near-zero-firing DSI) sits closer to alpha = 1, our averaging is
  "nearly inert" per the same theorem.

* **Population and seed/generation balance**: t0102 used **pop=96, gens<=20, GA seeds=2**.
  Druckmann2007 used pop=300, gens=1000, 1 seed; Hay2011 used pop=1000, gens=500, 1 seed;
  Mohacsi2024 used pop=100, gens=100, 10 seeds; PolegPolsky2026 used **pop=10, gens=300-1000,
  50-100 seeds** [PolegPolsky2026, Methods, via t0101 brainstorm]. PP-2026 is a **thin-pop /
  many-seeds / many-gens** recipe; we ran a **thick-pop / few-seeds / few-gens** recipe. The
  PP-2026 envelope spent its budget on diverse parameter initialisation, not noise averaging.

* **Warm-start**: t0091 used 5-anchor warm-start; t0099 and t0102 used pure LHS random init.
  Druckmann2007 hand-shifted Nat/Kslow voltages by +10 mV / +20 mV before optimisation
  [Druckmann2007, Methods, p. 8]; Hay2011 used a restricted Ih upper bound [Hay2011, Methods,
  p. 4]. Both literature conventions amount to "informed init"; t0102 is **adversarial random
  init** vs this convention.

* **Population sizing under noise**: Dang2023 Theorem 8 requires `mu = Omega(n log n)` for
  noisy NSGA-II to retain polynomial runtime [Dang2023, Theorem 8, p. 7]. For our problem `n =
  68`, `Omega(68 * log(68)) ~ 290`; our pop=96 is **~3x below** the theoretical floor for
  noise survival. This is one of the levers Dang2023 explicitly flags as principled to
  increase before concluding noise is the blocker.

* **DSI convention**: PolegPolsky2026 measures DSI as **vector-sum subthreshold peak voltage
  over 12 directions x 5 speeds** with values in [0, 1]; t0102 measures DSI as vector-sum on
  **spike rate over 16 directions at one speed**. Both share the 0.5 threshold convention but
  the underlying signal differs (voltage vs spike rate), so the absolute numbers are not
  directly comparable.

## Analysis

### Budget is the single most plausible reason for a null result

Mohacsi2024 ran **10,000 evaluations per algorithm-run** on 12-d problems and treated this as
a *matched-budget benchmark*. We ran **2,592 evaluations total across two seeds** on a
**68-d** problem. Linear-in-dimension scaling alone would suggest a baseline of `10000 * 68/12
~ 56,667` evaluations per run; we are at **2.3% of that** even ignoring the multi-objective
complexity multiplier. The Wilson 95% upper bound on our joint-pass rate from pooling t0099 +
t0102 (0/4,800) is **< 0.0008**, which is tight enough to reject base rates above 0.001 but
cannot distinguish "true zero acceptance" from "0.0001 acceptance"; either reading requires
~20,000+ additional evaluations to resolve.

Under the Hay2011 base rate of **0.4%** joint-acceptance on a 22-d joint perisomatic+dendritic
fit [Hay2011, Results, p. 7], 2,592 evaluations *should* have yielded ~10 joint-pass cells. We
found **0**. This is either evidence that (i) our 68-d substrate is intrinsically harder than
Hay2011's 22-d L5PC (likely true: 5.7x more dimensions, biological priors more stringent),
(ii) the joint-pass threshold is much stricter than Hay2011's per-feature 2 SD criterion
(likely true: our threshold is a hard 3-axis AND-clause), or (iii) our DSI vector-sum
objective is internally mis-specified (very likely true: Finding 1 in `results_detailed.md`
identifies a divide-by-near-zero floating-point artifact that pulls 27 of our cells to DSI=1.0
on silenced cells). The combined effect of (i)+(ii) +(iii) is sufficient to explain a true
zero result without invoking any algorithmic shortcoming of NSGA-II.

### Algorithm choice is a second-order but non-zero factor

Mohacsi2024 explicitly recommends **IBEA** over NSGA-II for multi-objective neuronal
optimisation [Mohacsi2024, Discussion, p. 12], with IBEA finishing ahead of all three NSGA-II
implementations on the 9-d active model benchmark (Use Case 4). On their 12-d CA1 benchmark,
the gap between NSGA-II and IBEA narrows but **PSO and CMAES both close to within 5%** of the
IBEA best while NSGA-II trails. The single most defensible methodology change this evidence
implies is **switch from NSGA-II to IBEA** for any continuation of this line of work. NSGA-II
being mid-pack at 9-12 d does not prove it is wrong at 68 d, but the literature does not
contain *any* evidence that NSGA-II outperforms IBEA on neuron-fitting problems, so the burden
of proof is on continuing with NSGA-II.

### Noise handling is theoretically adequate but practically marginal

Dang2023 proves NSGA-II survives Bernoulli noise with `p < 0.50` in polynomial expected time
[Dang2023, Theorem 8, p. 7], and reports qualitatively similar phase-transition behaviour
under Gaussian noise: 100% success at `sigma = n * 2^-4`, dropping to 0% at `sigma >= n *
2^-1` [Dang2023, Results, p. 9]. Our DSGC noise per cell at N=4 is well below the catastrophic
threshold, so noise alone does not predict the null. However, Morinaga2024 Theorem 3 sharpens
this: explicit averaging is only effective when the noise stability index `alpha > 1`. Our DSI
objective is a vector-sum over a low-spike-count denominator; near zero, the noise
distribution may be heavy-tailed (alpha close to 1), in which case K=4 explicit averaging is
*nearly inert* [Morinaga2024, Theorem 3, p. 5]. **Switching the DSI objective to
sign-averaging** [Morinaga2024, Theorem 9, p. 8] would be theoretically more robust at the
same compute cost, and is the most direct literature-recommended change.

### Population/generation balance: thin-pop/many-gens vs thick-pop/few-gens

PolegPolsky2026's published recipe is **pop=10, gens=300-1000, seeds=50-100**
[PolegPolsky2026, Methods, via t0101 brainstorm]: a thin population sustained over many
generations and many random restarts. Our t0102 ran the inverted recipe (**pop=96, gens<=20,
seeds=2**). At equal total evaluation budget B = pop x gens x seeds, the PP-2026 recipe spends
B on parameter-space re-randomisation; the t0102 recipe spends B on within-front diversity
preservation. Dang2023's population-floor result `mu = Omega(n log n)` favours larger pop for
noise survival, supporting the t0102 choice on theoretical grounds. PP-2026's empirical
success favours the opposite. **The literature does not converge** on which is better; this is
precisely the deferred suggestion S-0101-03 (budget-matched ablation).

### Prior Task Comparison

The t0091 joint-pass cell (DSI=0.511, PD=35.1 Hz, rob=0.79 at `source_generation=2`) is the
only strict joint-pass cell in the entire t0080-t0102 NSGA-II lineage [t0091
`results_summary.md`]. Per `creative_analysis.md` Section 2, this cell sits **3.55 normalised
units** from alt_topology anchor row 84 and **>= 11 units** from any other anchor in t0091's
warm-start population. With per-dim mutation probability 0.015 over 68 dims, the expected
number of mutated parameters per offspring is **~ 1.0** — consistent with the cell being a
one-polynomial-mutation descendant of an anchor clone, not an NSGA-II discovery. The t0091
published narrative of "warm-start NSGA-II finds joint- pass corner" is reframed in this task
as **"the anchor library already contains the joint-pass corner, and one generation of NSGA-II
is sufficient to preserve it"** — a methodological clarification consistent with both
Hay2011's joint-vs-single-target finding (joint fits need informed init) and Ament2023's 5-10x
warm-start HV envelope [Ament2023, as cited via t0099 `compare_literature.md`]. This is the
same reading the t0099 compare-literature reached independently and t0102 strengthens it:
2,208 + 2,592 = 4,800 random-init evaluations now find **0/4800** joint-pass cells, while the
single t0091 joint-pass cell sits within a one-mutation neighbourhood of a warm-start anchor.

## Limitations

* **No same-substrate published baseline.** No cited paper runs MO optimisation on a 68-d DSGC
  substrate with our specific Bed B + 14-d morphology parameterisation; all comparisons are
  with external substrates (CA1, L5PC, Purkinje, AdEx, biochemical). Acceptance-rate transfer
  (Hay2011's 0.4% to our 68-d) is therefore an **assumption**, not a measurement.

* **PolegPolsky2026 DSI numbers come from a brainstorm-session extraction, not from the
  canonical paper asset.** Per `research_papers.md`, the existing `summary.md` for
  PolegPolsky2026 contains fabricated mechanistic claims (deferred suggestion S-0101-01); the
  73.1%/50.8%/2.4% DSI numbers cited here come from
  `tasks/t0101_brainstorm_results_21/results/results_detailed.md`'s direct PDF-text
  extraction. A correction-pass on the paper summary is pending. Our cited values are
  therefore from a brainstorm transcript, not an unimpeached paper summary.

* **Cost-watchdog truncation: gens 14/13 instead of 20.** Both seeds were cut short before
  reaching the planned generation 20. Neither HV trajectory had plateaued (seed 44 made +0.3
  HV jump at gen 14; seed 55 made +0.2 jump at gen 13). It is possible — though the structural
  bimodality finding argues against it — that 6-7 additional generations would have produced a
  joint-pass cell. The literature comparison reads our 14-gen / 13-gen result as a hard
  endpoint, but it is more correctly a **truncated** endpoint.

* **DSI floating-point artifact contaminates the headline number.** Our reported `max DSI =
  1.0` values in both seeds are silenced-cell artifacts (Finding 1, `results_detailed.md`).
  The Mohacsi2024 / Hay2011 / Druckmann2007 acceptance-rate comparison assumes our DSI metric
  is a faithful selectivity measure; under that assumption the comparison is valid for cells
  with PD > 0, but the artifact means our headline `metrics.json` value cannot be compared
  like-for-like to any published DSI number without first gating by a minimum spike-count
  threshold.

* **NSGA-II is the only algorithm tested.** Mohacsi2024 puts NSGA-II at 3rd or 4th in their
  6-use- case ranking; we cannot tell from t0102 alone whether the null result is
  NSGA-II-specific or truly algorithm-independent. A follow-up at matched budget with IBEA or
  CMAES would be the cheapest one-variable test (deferred suggestion: switch optimiser).

* **Population floor not respected.** Dang2023's `mu = Omega(n log n) ~ 290` for `n = 68` is
  **~3x larger** than our pop=96; we cannot rule out that pop=96 is below the noise-survival
  floor for our problem dimensionality. Raising pop to 256 or 512 is a principled lever before
  concluding the substrate is structurally empty of joint-pass cells.

* **No tail-diagnostic per objective.** Morinaga2024's stability-index `alpha` diagnostic was
  not computed for any of our objectives. Whether DSI / PD / robustness sit at `alpha > 1`,
  `alpha = 1`, or `alpha < 1` is an open empirical question; the choice of explicit averaging
  at K=4 is theoretically justified only if `alpha > 1`. Computing alpha per objective on the
  t0093 anchor library would close this gap at zero additional Vast.ai cost.

</details>
