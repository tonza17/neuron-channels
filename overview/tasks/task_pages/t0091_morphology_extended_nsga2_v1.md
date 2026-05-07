# ⏹ First joint 68-d NSGA-II with morphology in eval loop, 5-anchor warm-start

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0091_morphology_extended_nsga2_v1` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md), [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **Task types** | `experiment-run`, `data-analysis`, `answer-question` |
| **Expected assets** | 1 answer, 1 predictions |
| **Task folder** | [`t0091_morphology_extended_nsga2_v1/`](../../../tasks/t0091_morphology_extended_nsga2_v1/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/task_description.md)*

# First joint 68-d NSGA-II with morphology generation inside the evaluation loop

## Motivation

Brainstorm session 18 (t0089) commissioned a strategic pivot from electrophys-only
optimisation (t0080-t0088) to morphology-extended optimisation. t0090 delivers the procedural
DSGC morphology generator (14 morphology knobs) plus a validated diversity test plus a Bed-B
reproducibility check. This task t0091 is the first NSGA-II run that calls the generator
inside the evaluation loop, jointly optimising morphology + electrophys in a 68-d parameter
space.

The strategic question is whether enabling morphology in the optimisation opens
biologically-plausible joint-pass regions that t0080-t0088's fixed-Bed-B substrate could not
reach. t0086 + t0088 established that all v3 substrate joint-pass / near-joint-pass cells are
NaP-dominant in their PD-vs-ND mechanism and exotic by the biological scorecard (NMDA
per-synapse +85 to +116 sigma above Sivyer 2013, distal NaP +9 to +34 sigma above Stuart 1999,
GABA spatial-gradient violations). If morphology variation can shift cells toward biologically
plausible NMDA / NaP regimes while maintaining joint-pass DSI / firing rate, the project's
direction-selectivity story has a second mechanism (morphological asymmetry) on top of the
channel mechanism. If morphology pegs at near-Bed-B defaults across the entire Pareto, the v3
substrate's biological-plausibility ceiling is not raised by morphology and we revisit with a
real-cell library (Option G from the brainstorm) in a future task.

A secondary question concerns the asymmetry direction: if PD-asymmetric anchor cells are
preserved more than their ND-asymmetric mirrors in the final Pareto, that is strong evidence
for soma-displacement-toward-PD as a functional DS mechanism (Schachter 2010, Trenholm 2013,
Briggman 2011).

## Scope

### In Scope

* 68-d NSGA-II (54-d v3 electrophys + 14-d morphology) using the t0090 procedural generator
* Pop 96, up to 8 generations, adaptive HV-plateau stop, cost watchdog
* 5-anchor warm-start population (Bed-B-like + symmetric + PD-asymmetric + ND-asymmetric +
  alternative-topology), each anchor cloned with ~19 t0083 Pareto electrophys variants
* Pareto-front analysis: comparison to t0083's 54-d front; biological-plausibility scoring per
  t0086 / t0088 framework extended to 68-d cells
* Anchor-tracking analysis: which of the 5 anchors are over- vs under-represented in the final
  Pareto?
* One answer asset on biological plausibility under morphology variation
* One predictions asset (the 68-d Pareto-front cells, with per-cell DSI / PD / robustness /
  morphology vector / electrophys vector)

### Out of Scope

* Topology-changing perturbations beyond t0090's 14 generator knobs
* Real-cell morphology library (deferred to a future task if t0091 negative result motivates)
* NSGA-II at >68-d (e.g., 80-d with extra channels)

## Approach

### Phase A — Build the 5-anchor warm-start population

Pop 96 = 5 anchors x ~19 t0083 Pareto electrophys variants per anchor + 1 random sample.

Anchors:

| Anchor | Description | Source |
| --- | --- | --- |
| 1 | Bed-B-like (matches existing t0083 substrate; the "do not regress from t0083 baseline" anchor) | t0090 Phase F validated point |
| 2 | Symmetric: `soma_offset_pd_um=0`, `field_elongation_pd=1.0`, `branch_density_gradient_pd=0`, `primary_branch_pd_concentration=0` | Tests whether DS can emerge purely from channel/synapse mechanism without morphological asymmetry |
| 3 | PD-asymmetric: soma offset +100 um toward PD, field elongated 2x along PD, branches biased toward PD | Tests whether morphological asymmetry along PD opens biologically-plausible joint-pass |
| 4 | ND-asymmetric: mirror of #3, soma offset -100 um | Mirror sanity check; if optimiser preserves #3 and discards #4, that is strong evidence for soma-displacement-toward-PD as a functional DS mechanism |
| 5 | Alternative topology: more primary branches (`num_primary_branches=6-7`), deeper Strahler depth, smaller field | Diversifies topology axis specifically |

For each anchor:
* Sample ~19 different electrophys vectors from t0083's gen-17 Pareto archive (using the t0086
  classification: prefer Genuine + Marginal cells over Stochastic ones).
* Combine each electrophys vector with the anchor's morphology vector to produce a complete
  68-d warm-start cell.

Total: 95 warm-start cells from 5 anchors x 19 + 1 random sample = pop 96.

**Time**: ~1-2 hours local. **Cost**: $0.

### Phase B — Joint NSGA-II run

68-d NSGA-II using `pymoo` with NSGA-II algorithm, mixed integer-real handling for the
`num_primary_branches` and `max_strahler_depth` integer parameters.

Settings:
* Population size: 96
* Generations: up to 8 (adaptive HV-plateau stop fires earlier if HV growth < 1 percent for 2
  consecutive gens)
* Crossover: SBX with eta = 15
* Mutation: polynomial mutation with eta = 20, prob = 1 / 68
* Cost watchdog: $4.00 hard cap (well below remaining $4.44 buffer)
* Per-cell evaluation: t0090 generator builds NEURON model from 14 morph params; 54 channel /
  synapse params inserted into generated sections; 5 evaluation seeds for inner replication;
  bar-rotation simulation at 16 directions; objectives = (DSI vector-sum, PD firing rate,
  robustness across seeds).

**Hardware**: Vast.ai EPYC 7B13 64-core. 96 cells x 5 seeds x 16 directions x ~60 s/sim / 64
parallel = ~12 minutes per generation. 8 generations: ~1.6 hours / generation x 8 = ~12.8
hours. With overhead: ~14-16 hours wall-clock.

**Cost estimate**: 14-16 hours x $0.40/hr = ~$5.60-6.40. Optimise: drop pop 96 to pop 80 if
cost overshoot looks likely (~80 cells x 8 gens = ~13.3 hours x $0.40 = ~$5.32; still tight).
Fall back: 6 generations (cost watchdog stops at gen 6), ~9-10 hours = ~$3.60-4.00.
**Realistic budget: $3.00-3.50 with adaptive stop or 6-gen cap.**

### Phase C — Pareto-front + biological-plausibility analysis

* Extract 68-d Pareto front from final population.
* Run t0086's `biological_priors.py` + `biological_scorecard.py` on every Pareto cell
  (corrected-units NMDA score from t0090 Phase G.2 validation).
* Compare biological-plausibility distribution to t0083's 54-d Pareto:
  * Do morph-extended cells reach lower NMDA / NaP / GABA exotic-ness while maintaining
    joint-pass DSI / PD / robustness?
  * Do any cells score "plausible" or "stretched" on all 9 priors simultaneously?

### Phase D — Anchor-tracking analysis

For each Pareto cell, compute its 14-d morphology vector's nearest anchor (Euclidean distance
in normalised morph-param space). Tabulate Pareto-cell counts per anchor:

| Anchor | Warm-start contribution (cells) | Final Pareto representation (cells) |
| --- | --- | --- |
| 1 (Bed-B-like) | 19 | ? |
| 2 (Symmetric) | 19 | ? |
| 3 (PD-asymmetric) | 19 | ? |
| 4 (ND-asymmetric) | 19 | ? |
| 5 (Alt-topology) | 19 | ? |

If anchor 3 (PD-asymmetric) is over-represented and anchor 4 (ND-asymmetric) is
under-represented, that is strong evidence for soma-displacement-toward-PD as a functional DS
mechanism. Compute statistical significance via bootstrap.

### Phase E — Answer asset

One answer asset at `assets/answer/morphology-extension-biological-plausibility/`
synthesising:

* Did morphology extension open biologically-plausible joint-pass regions?
* Which of the 5 anchors did the optimiser preserve in the final Pareto?
* Specifically: PD-asymmetric vs ND-asymmetric — is the optimiser-preferred asymmetry
  direction consistent with the published DS mechanism?
* What is the biological-plausibility ceiling of the morphology-extended substrate?
* What follow-ups does this open?

## Pass Criteria

* Phase B converges (HV plateau or 8-gen cap reached) within budget; no NaN propagation; cost
  watchdog not triggered.
* Phase C produces a 68-d Pareto front with at least 8 cells (matching t0083 minimum-Pareto
  threshold).
* Phase D produces a definitive anchor-tracking table with bootstrap-significance p-values.
* Phase E lands a definitive yes / no on whether morphology extension reaches biologically
  plausible cells, with quantitative thresholds.

**Acceptable negative**: optimiser pegs all anchors back toward Bed-B-like (anchor 1 dominates
final Pareto >80 percent) — conclusion is the v3 substrate's biological-plausibility ceiling
is not raised by morphology variation in this parametrisation. Follow-up: Option G real-cell
library in a future task.

## Compute and Budget

* **Vast.ai EPYC 7B13 64-core** for Phase B NSGA-II
* **Local 64-core CPU** for Phases A, C, D, E

**Estimated cost**: $3.00-3.50 (Phase B with adaptive HV-plateau stop or 6-gen cap). Buffer
remaining after t0091: ~$0.94-1.44.

**Cost watchdog**: hard cap at $4.00 (lockout terminates the NSGA-II if cumulative remote
spend exceeds threshold).

## Time Estimation

* Phase A (warm-start): 1-2 h local
* Phase B (NSGA-II): 14-16 h Vast.ai
* Phase C (Pareto analysis): 2-3 h local
* Phase D (anchor-tracking): 2 h local
* Phase E (answer asset): 1 h local

**Total wall-clock**: ~20-24 hours (mostly Phase B remote).

## Expected Assets

* **Answer asset**: morphology-extension biological plausibility synthesis
  (`expected_assets["answer"] = 1`)
* **Predictions asset**: 68-d Pareto-front cells with per-cell DSI / PD / robustness /
  morphology vector / electrophys vector (`expected_assets["predictions"] = 1`)

## Risks and Fallbacks

* **NSGA-II fails to converge in 8 gens**: 68-d is 25 percent more than 54-d; warm-start gives
  strong prior. If HV is still growing at 8 gens, document it and propose extension as a
  future task (only if budget allows).
* **Cost overshoot**: cost watchdog at $4.00 hard cap; drop to 6 gens if approaching.
* **Generator instability under NSGA-II mutation**: if mutated morph_params produce degenerate
  morphologies, the eval function returns a penalty objective; t0090 Phase D verification
  should have caught most degenerate parameter combinations.
* **Anchor 4 ND-asymmetric cells fail to reproduce on the optimiser's seed**: indicates the
  warm-start anchor is unstable; replace with a symmetric anchor variant.
* **All anchors converge to anchor 1 (Bed-B-like)**: acceptable negative; useful finding;
  motivates Option G real-cell library follow-up.

## Verification Criteria

* `verify_research_code.py`, `verify_plan.py`, `verify_logs.py`, `verify_assets.py`,
  `verify_task_file.py` pass with 0 errors.
* `verify_costs.py` passes (cost record present, within budget).
* The answer asset passes `verify_answer.py`.
* The predictions asset passes `verify_predictions.py`.

## Cross-References

* **t0089_brainstorm_results_18** — commissioning brainstorm session.
* **t0090_morphology_generator_diversity_test** — generator dependency.
* **t0083_bedb_v3_extend_nsga2_gen8plus** — warm-start electrophys archive source.
* **t0086_robustness_cluster_bio_comparison**, **t0088_recluster_marginals_and_vm_motifs** —
  biological-plausibility framework.
* Source suggestions: none directly (new direction). Indirect inheritance from S-0086-01
  (NSGA-II re-run with tightened bounds, kept high for post-t0091 follow-up).

</details>
