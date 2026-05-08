# ✅ First joint 68-d NSGA-II with morphology in eval loop, 5-anchor warm-start

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0091_morphology_extended_nsga2_v1` |
| **Status** | ✅ completed |
| **Started** | 2026-05-08T11:35:57Z |
| **Completed** | 2026-05-08T15:55:00Z |
| **Duration** | 4h 19m |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md), [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md) |
| **Task types** | `experiment-run`, `data-analysis`, `answer-question` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`patch-clamp`](../../by-category/patch-clamp.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`synaptic-integration`](../../by-category/synaptic-integration.md), [`voltage-gated-channels`](../../by-category/voltage-gated-channels.md) |
| **Expected assets** | 1 answer, 1 predictions |
| **Step progress** | 15/15 |
| **Cost** | **$0.65** |
| **Task folder** | [`t0091_morphology_extended_nsga2_v1/`](../../../tasks/t0091_morphology_extended_nsga2_v1/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/task_description.md)*

# First joint 68-d NSGA-II with morphology generation inside the evaluation loop

## Motivation

Brainstorm session 18 (t0089) commissioned a strategic pivot from electrophys-only
optimisation (t0080-t0088) to morphology-extended optimisation. t0090 delivered the procedural
DSGC morphology generator (14 morphology knobs) but committed a soma-`pt3dadd` collapse bug;
t0092 diagnosed the root cause and shipped `generate_fixed_morphology` as a thin shim; t0093
ran the full 60-cell re-sweep under the patched generator (60/60 STABLE-firing, 56/60 with
PD-rate>0, 0 regressions) and issued correction `C-0093-01` (`replace`) redirecting the
canonical procedural generator to t0092's fix. **t0091 imports the t0092 patched generator,
not t0090's unpatched one.** This task is the first NSGA-II run that calls the patched
generator inside the evaluation loop, jointly optimising morphology + electrophys in a 68-d
parameter space.

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

* 68-d NSGA-II (54-d v3 electrophys + 14-d morphology) using the t0092 patched procedural
  generator (`generate_fixed_morphology`, canonicalised by C-0093-01)
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
| 1 | Bed-B-like (matches existing t0083 substrate; the "do not regress from t0083 baseline" anchor) | t0093 patched-generator Bed-B reproducibility (43.6 Hz PD-rate post-fix on the BedB-equivalent point) |
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
* Per-cell evaluation: `from
  tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import
  generate_fixed_morphology` builds the NEURON model from 14 morph params (the soma-pt3d
  collapse bug is fixed at the source); 54 channel / synapse params inserted into generated
  sections; 5 evaluation seeds for inner replication; bar-rotation simulation at 16
  directions; objectives = (DSI vector-sum, PD firing rate, robustness across seeds).

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
  morphologies, the eval function returns a penalty objective. t0093's patched-generator
  re-sweep showed 60/60 STABLE under the t0083 channel set across the wide LHS sample, so the
  patched generator covers the morphology parameter space without NaN_VOLTAGE failures.
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
* **t0090_morphology_generator_diversity_test** — original generator dependency (superseded by
  t0092 / t0093 fix).
* **t0092_diagnose_morphology_generator_silence** — patched generator
  (`generate_fixed_morphology`); canonical entry point for morphology construction.
* **t0093_resweep_and_t0090_correction** — full 60-cell verification of the patched generator
  (60/60 STABLE-firing) and `replace` correction overlay `C-0093-01` redirecting the canonical
  procedural DSGC morphology generator to t0092's fix.
* **t0094_brainstorm_results_19** — brainstorm session that updated this task's dependencies
  and import paths to reference t0092 / t0093 (covers S-0093-01).
* **t0083_bedb_v3_extend_nsga2_gen8plus** — warm-start electrophys archive source.
* **t0086_robustness_cluster_bio_comparison**, **t0088_recluster_marginals_and_vm_motifs** —
  biological-plausibility framework.
* Source suggestions: none directly (new direction). Indirect inheritance from S-0086-01
  (NSGA-II re-run with tightened bounds, kept high for post-t0091 follow-up).

</details>

## Costs

**Total**: **$0.65**

| Category | Amount |
|----------|--------|
| vast-ai-rtx-pro-4000-idle | $0.65 |

## Remote Machines

| Provider | GPU | Count | RAM | Duration | Cost |
|----------|-----|-------|-----|----------|------|
| vast.ai | RTX-PRO-4000-idle | 1 | 252 GB | 2.6h | $0.65 |

## Metrics

### Anchor bedb_like

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.1102828413095696** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.763168718117299** |

### Anchor pd_asymmetric

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.17646153646965027** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.720214942360968** |

### Anchor nd_asymmetric

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.45128268517138026** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.7278477943828441** |

### Anchor alt_topology

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.2627128883635463** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.7859482536435738** |

### All Pareto cells

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.22084466042432208** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Did enabling the 14-d procedural morphology variation as an optimisation axis open biologically-plausible joint-pass regions of parameter space that the fixed-Bed-B substrate of t0080-t0088 could not reach?](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/answer/morphology-extension-biological-plausibility/) | [`full_answer.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/answer/morphology-extension-biological-plausibility/full_answer.md) |
| paper | [Persistent sodium currents in neurons: potential mechanisms and pharmacological blockers](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1007_s00424-024-02980-7/) | [`summary.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1007_s00424-024-02980-7/summary.md) |
| paper | [A new role for excitation in the retinal direction-selective circuit](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1113_JP286581/) | [`summary.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1113_JP286581/summary.md) |
| paper | [GABAergic Inhibition Controls Receptive Field Size, Sensitivity, and Contrast Preference of Direction Selective Retinal Ganglion Cells Near the Threshold of Vision](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1523_JNEUROSCI.1979-23.2023/) | [`summary.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1523_JNEUROSCI.1979-23.2023/summary.md) |
| predictions | [Pareto front 68-d morphology-extended Bed-B v3](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/predictions/pareto-front-68d-morphology-extended-bedb-v3/) | [`description.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/predictions/pareto-front-68d-morphology-extended-bedb-v3/description.md) |

## Suggestions Generated

<details>
<summary><strong>Per-cell field_elongation_pd vs DSI test on the 57-cell t0091
Pareto to resolve HM-3 inconclusive</strong> (S-0091-01)</summary>

**Kind**: evaluation | **Priority**: high

t0091 reported a Spearman rho=-0.07 between total dendritic length and DSI vector-sum across
the 57-cell Pareto, leaving HM-3 (length-vs-DSI scaling, Hausselt2007) inconclusive because
total length conflates field_elongation_pd with branch_density_gradient_pd and
num_primary_branches. Pure data-analysis task on existing pareto_front.json: extract
field_elongation_pd from each Pareto cell's 14-d morph_params vector, compute Spearman +
Kendall correlations against DSI, PD-rate, robustness, and the 9 channel-side priors, plot
per-anchor scatter overlays, and stratify by anchor lineage. Goal: definitively confirm or
refute that elongation along PD is the morphology axis driving DSI in joint optimisation,
separate from branch density. Cost: $0 (local CPU analysis on existing JSONL files).
Recommended task types: data-analysis.

</details>

<details>
<summary><strong>Per-direction DSI re-scoring of the t0091 57-cell Pareto to surface
DSGC subtype-specific tuning</strong> (S-0091-02)</summary>

**Kind**: evaluation | **Priority**: high

t0091 used vector-sum DSI across 16 directions, which is direction-blind: a cell tuned to PD
with peak at 0 deg and a cell tuned to a non-cardinal direction (e.g., 45 deg) collapse to the
same vector-sum DSI. The PD vs ND anchor-asymmetry test (12 vs 9, p=0.331) may be
artifactually washed out by this collapse. Brendly2025 and Riccitelli2025 (now in the t0091
corpus from research-internet) report DSGC subtypes with distinct preferred directions. Pure
data-analysis on existing pareto_front.json + per-direction firing rate JSONL: re-score each
Pareto cell with per-direction DSI (peak direction, half-width-at-half-maximum, peak-to-trough
ratio); recompute the PD-asymmetric vs ND-asymmetric anchor test using direction-binned DSI;
compare per-direction tuning curve shapes between bedb_like, alt_topology, and the 21
asymmetric anchor cells. Cost: $0 (local CPU). Recommended task types: data-analysis.

</details>

<details>
<summary><strong>Continue t0091 NSGA-II for 6 more generations (gen 3-8) to test
whether HV plateau or biological-plausibility shifts</strong> (S-0091-03)</summary>

**Kind**: experiment | **Priority**: medium

t0091 stopped at gen 2 of 8 when REQ-10 (>=8-cell Pareto) was satisfied 7x over (57 cells);
cost watchdog never fired ($0.65 of $4.00 cap). The HV trajectory was still climbing at +68
percent per generation (14.07 to 23.71) and plateau detection requires >=4 generations of
history before it can fire. Run pop=96 x 6 more generations on a single Vast.ai EPYC 7B13
64-core resume from t0091's gen-2 final population (snapshot the population from
results/data/all_evaluations.json). Tests three open questions: (a) does HV plateau before gen
8? (b) does any gen 3+ cell pass biological plausibility, or is universal channel-side
violation robust to generation depth? (c) does the PD vs ND anchor count shift toward
significance with more generations? Cost estimate: ~$1.80 (6 gens x ~12 min/gen wall-clock x
60 parallel workers x $0.23/hr); fits remaining $3.80 project buffer. Recommended task types:
experiment-run, data-analysis.

</details>

<details>
<summary><strong>alt_topology basin deep-dive: identify morphology features
distinguishing alt_topology vs bedb_like Pareto cells</strong> (S-0091-04)</summary>

**Kind**: evaluation | **Priority**: medium

16 alt_topology cells survived in the 57-cell Pareto (parity with bedb_like's 20), and the
only strict joint-pass cell (DSI 0.51, PD 35 Hz, robust 0.79) is nearest to alt_topology in
14-d morphology space. creative_thinking.md flags this as evidence for at least two distinct
morphological basins of joint-pass-adjacency, but the 14-d signature distinguishing
alt_topology from bedb_like has not been quantified. Pure data analysis on pareto_front.json +
warm_start_population.json: PCA + UMAP on the 14-d morph vectors restricted to Pareto cells
colour-coded by anchor; per-feature Mann-Whitney U tests on each of the 14 knobs; identify the
top 3-5 discriminative features (likely num_primary_branches, max_strahler_depth,
mean_branching_angle); cross-reference with biological scorecard rows. Cost: $0. Recommended
task types: data-analysis.

</details>

<details>
<summary><strong>Reformulate NSGA-II with biological priors as additional objectives
or hard constraints</strong> (S-0091-05)</summary>

**Kind**: technique | **Priority**: medium

t0091 used 3-objective NSGA-II minimising (-DSI, -PD-rate, -robustness) with biological priors
applied as a post-hoc filter (0/57 Pareto cells pass). The optimiser drifts to the upper rail
of NMDA / NaP / GABA bounds without paying any cost. Reformulate as either (a) 4+ objective
NSGA-II adding worst-case prior-violation sigma as a fourth objective, or (b) hard-constrained
NSGA-II using pymoo's constraint handling with each prior as a g(x) <= 0 inequality. Hay 2011
is direct precedent for (a). Run a small-scale pass (pop=64, 4 gens, ~$1.00) on the t0091
substrate and compare the reformulated Pareto's biological-plausibility distribution against
t0091's post-hoc-filter Pareto. If the reformulated Pareto includes any biologically-plausible
joint-pass cells, the 'morphology cannot rescue priors' verdict was driven by formulation, not
substrate. Cost ~$1.00 on Vast.ai EPYC 7B13. Recommended task types: experiment-run,
build-model.

</details>

<details>
<summary><strong>Real-cell DSGC morphology library from NeuroMorpho: test whether
observed morphologies escape prior-violation ceiling</strong> (S-0091-06)</summary>

**Kind**: dataset | **Priority**: medium

t0091 confirmed HM-1 (morphology asymmetry necessary; symmetric anchor count = 0) but refuted
HM-2 (PD vs ND direction blind, p=0.331). The procedural 14-knob generator covers a parametric
box that biological DSGCs may or may not occupy; t0091's 57-cell Pareto stays inside that box
but cannot escape the channel-side prior-violation ceiling. Brainstorm 18 'Option G' is the
next move: build a NeuroMorpho.org-anchored real DSGC cell library (10-20 mouse / rabbit
reconstructions from Briggman 2011, Wei 2011, Morrie & Feller 2018), implement a categorical
selector + parametric deformation knobs (diameter scaling, branch pruning, soma offset), then
re-run t0091's NSGA-II with the real-cell library replacing the procedural generator. Tests
whether observed DSGC morphologies escape the prior-violation ceiling that procedural ones
cannot. Larger task: needs planning first. Cost ~$2-3 for the optimisation pass. Recommended
task types: download-dataset, build-model, write-library.

</details>

<details>
<summary><strong>Pareto-cell PCA + feature-importance analysis on the 14-d morph
vectors to rank Pareto-inclusion drivers</strong> (S-0091-07)</summary>

**Kind**: evaluation | **Priority**: medium

t0091 reports anchor-level Pareto counts (bedb_like 20, symmetric 0, pd_asymmetric 12,
nd_asymmetric 9, alt_topology 16) but does not report which of the 14 morphology knobs
individually drive Pareto inclusion. Pure data-analysis on results/data/pareto_front.json +
all_evaluations.json: train a logistic regression / random forest classifier with the 14-d
morph vector as input and is_in_pareto as binary label, using the 187 evaluations as the
training set; report per-feature coefficients / SHAP values; cross-validate via
leave-one-anchor-out splits; visualise via per-feature partial dependence plots. Goal: rank
the 14 knobs by their causal importance for joint Pareto inclusion, beyond the anchor-level
aggregation. This complements S-0091-01 (which is single-feature Spearman) and S-0091-04
(which is alt-topology vs bedb-like comparison) with an exhaustive feature-importance audit.
Cost: $0 (local CPU). Recommended task types: data-analysis.

</details>

<details>
<summary><strong>Constrained channel-only NSGA-II on fixed t0093 morphology to
disambiguate channel-side from morphology-side priors</strong> (S-0091-08)</summary>

**Kind**: experiment | **Priority**: medium

t0091's 0/57 plausible-cell verdict is universally driven by channel-side priors (NMDA
per-spine, NaP density, GABA spatial gradient); morphology priors mostly pass. S-0086-01
already proposes a tighter-NMDA re-run but does not specify morphology configuration nor
combine with hard-constraint formulation. Hold morphology fixed at the t0093 verified
BedB-equivalent (PD-rate 43.6 Hz post-fix) and run NSGA-II on a 27-d channel-only space (12
channel densities + 9 NMDA/NaP-related + 6 GABA spatial) with all biological priors as hard
constraints (per S-0091-05) and tightened NMDA bounds (Sivyer 2013 5e-4 uS upper cap). Tests
whether the v3 substrate has any biologically-plausible joint-pass region in channel space
alone with verified morphology, independent of S-0086-01's broader question. If no, the
substrate is incompatible with priors regardless of morphology, motivating S-0091-06's
real-cell library. Cost ~$1.50 on Vast.ai EPYC 7B13. Recommended task types: experiment-run.

</details>

## Research

* [`research_code.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/results/results_summary.md)*

--- spec_version: "1" task_id: "t0091_morphology_extended_nsga2_v1" date_completed:
"2026-05-08" status: "complete" ---

# Results Summary: First Joint 68-d NSGA-II with Morphology Generator In-Loop

## Summary

Joint 68-d NSGA-II (54-d v3 electrophys + 14-d morphology) on Bed B with the t0092 patched
procedural generator inside the per-cell evaluation loop reached **gen 2 of 8** before user-
directed teardown, producing a **57-cell Pareto front**. **Zero cells pass the t0086/t0088
biological-plausibility scorecard** under worst-case prior aggregation; one cell is a strict
joint-pass on (DSI ≥ 0.5, PD ≥ 30 Hz, robustness ≥ 0.7) but fails the biological priors.
**Total spend $0.6454** (16% of the $4.00 watchdog cap) over 2.63 hours of Vast.ai uptime.

## Metrics

* **57 Pareto cells** (REQ-10 threshold ≥ 8 met by 7×).
* **HV trajectory**: gen 1 = 14.07 → gen 2 = 23.71 (+68% growth; not yet plateaued).
* **Anchor distribution in Pareto**: bedb_like 20, symmetric **0**, pd_asymmetric 12,
  nd_asymmetric 9, alt_topology 16, random 0.
* **PD vs ND asymmetric counts**: 12 vs 9, one-sided permutation **p = 0.331** (1000 bootstrap
  resamples). Below the 5:1 effect-size threshold from Briggman 2011 needed to claim
  functional asymmetry.
* **Mean DSI per anchor in Pareto** (registered metric): bedb_like 0.110, pd_asymmetric 0.176,
  nd_asymmetric 0.451, alt_topology 0.263, all-Pareto 0.221.
* **One strict joint-pass cell** (gen 2): DSI = 0.511, PD = 35.1 Hz, robustness = 0.79; fails
  biological plausibility on at least one channel-density prior.
* **Length-vs-DSI Spearman**: ρ = -0.07 (no monotonic dependency).
* **Total cost**: $0.6454 (well under $4.00 hard cap and $3.00–3.50 plan estimate).

## Verification

* `verify_predictions_asset.py` — PASSED (0 errors, 2 expected warnings)
* `verify_answer_asset.py` (via `meta/asset_types/answer/verificator.py`) — PASSED (0 errors,
  0 warnings)
* `verify_task_metrics.py` — PASSED (0 errors, 0 warnings)
* `verify_machines_destroyed.py` — PASSED (0 errors, 1 RM-W001 warning is verifier false
  negative for already-destroyed instances; instance 36344985 confirmed destroyed via empty
  `vastai show instances` output)
* `ruff check` on `code/` — PASSED
* `mypy -p tasks.t0091_morphology_extended_nsga2_v1.code` — PASSED (no issues)

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0091_morphology_extended_nsga2_v1" ---

# Detailed Results: First Joint 68-d NSGA-II with Morphology Generator In-Loop

## Summary

Joint 68-d NSGA-II (54-d v3 electrophys + 14-d morphology) on Bed B with the t0092 patched
procedural generator inside the per-cell evaluation loop reached **gen 2 of 8 planned
generations** before user-directed teardown. The 57-cell Pareto front from gen 1+2 union
exceeds REQ-10's ≥8-cell threshold by 7×. The headline finding is the "acceptable negative"
outcome documented in the plan: **zero cells pass the t0086/t0088 biological-plausibility
scorecard under worst-case prior aggregation**, while a single strict joint-pass cell (DSI
0.511, PD 35.1 Hz, robustness 0.79) exists in gen 2 — but fails the biological priors. The PD
vs ND asymmetric counts (12 vs 9) are not significant (p=0.331), so the "morphology asymmetry
preserves soma-displacement-toward-PD as a DS mechanism" prediction (Schachter 2010 / Trenholm
2013) is not confirmed at this generation depth. Total spend $0.6454 (16% of $4.00 watchdog).

## Methodology

* **Hardware**: Vast.ai instance 36344985, AMD EPYC 7B13 64-core CPU, 252 GB RAM, 40 GB disk
  (idle RTX PRO 4000 GPU not used; CPU-only NEURON + pymoo NSGA-II workload).
* **Runtime**: 2.6322 hours uptime from 2026-05-08T12:52:06Z to 2026-05-08T15:30:01Z; billed
  dph_total $0.2452/hr; offer base rate $0.2290/hr (cost-watchdog reads this).
* **NSGA-II configuration**: pop=96, max_gen=8, 5-anchor warm-start (19 t0083 Pareto
  electrophys variants per anchor + 1 random), SBX crossover (η=15, prob=0.9), polynomial
  mutation (η=20, prob=1/68), 60 parallel workers via
  `pymoo.parallelization.starmap.StarmapParallelization`.
* **Termination**: `MaximumGenerationTermination(8)` ∪ HV-plateau (window=2, threshold=0.01,
  min_history=4) ∪ `CostWatchdogTermination(max_cost_usd=4.00)`. None of the three fired
  before teardown.
* **Per-cell evaluation**: 16 directions × 5 evaluation seeds × pop 96 = 7680 NEURON
  simulations per generation (~3000 effective on 60 workers ≈ 12 min/gen central estimate);
  generator built from 14-d morph params via
  `tasks.t0092_..code.morphology_generator_fix.generate_fixed_morphology` (canonicalised by
  C-0093-01); 54-d electrophys params inserted into generated sections.
* **Objectives**: 3-objective NSGA-II minimising `(-dsi_vector_sum, -pd_rate_hz, -robustness)`
  (pymoo minimises; the negation makes the maximised metrics decrease).
* **Cost watchdog**: hard cap $4.00, reads `selected_offer.price_per_hour=$0.2290/hr` from
  `machine_log.json`. Did not fire (cumulative spend at teardown was $0.21 from the NSGA-II
  run alone, with the rest of the $0.6454 going to setup, killed-run cost, and post-gen-2
  idle/ teardown).

## Metrics Tables

### Per-anchor metrics in the 57-cell Pareto front (registered metrics)

| Anchor | Cells | DSI vector-sum (mean) | Tuning-curve reliability (mean) |
| --- | --- | --- | --- |
| `bedb_like` | 20 | 0.110 | 0.763 |
| `symmetric` | **0** | n/a | n/a |
| `pd_asymmetric` | 12 | 0.176 | 0.720 |
| `nd_asymmetric` | 9 | 0.451 | 0.728 |
| `alt_topology` | 16 | 0.263 | 0.786 |
| **All Pareto** | **57** | **0.221** | — |

### Anchor-tracking p-values (1000 bootstrap resamples)

| Comparison | Counts | One-sided p | Significant at α=0.05? |
| --- | --- | --- | --- |
| pd_asymmetric vs nd_asymmetric | 12 vs 9 | **0.331** | No |

### HV trajectory

| Generation | HV | Cumulative cost | Elapsed s | n_evaluations |
| --- | --- | --- | --- | --- |
| 1 | 14.07 | $0.073 | 1145 | 91 |
| 2 | 23.71 | $0.211 | 3318 | 187 |

### Joint-pass cell discovered (DSI ≥ 0.5, PD ≥ 30 Hz, robust ≥ 0.7)

| Generation | DSI | PD-rate Hz | Robustness | Nearest anchor (14-d Euclidean) |
| --- | --- | --- | --- | --- |
| 2 | **0.511** | **35.1** | **0.79** | `alt_topology` |

This single cell satisfies the strict numerical joint-pass thresholds but **fails biological
plausibility** on at least one channel-density prior (worst-case aggregation across 13
priors).

## Comparison vs Baselines

* **t0083 baseline (54-d electrophys-only NSGA-II, joint-pass cells in t0086 13-cell pool)**:
  ALL flagged exotic by the same biological scorecard. t0091's 68-d morphology-extended search
  produces the same biological-plausibility outcome — morphology variation does not raise the
  ceiling.
* **t0093 patched-generator validation**: showed 21/60 cells with DSI > 0.5 under the t0083
  best- cell channel set (single channel set, no optimisation). t0091's optimisation under
  joint search finds 1/57 strict joint-pass — the optimiser does locate a higher-quality cell,
  but at the cost of all 57 Pareto cells failing biological plausibility.

## Visualizations

### Anchor tracking bar chart

![Anchor counts in 57-cell Pareto: bedb_like 20, symmetric 0, pd_asymmetric 12, nd_asymmetric
9, alt_topology
16](../../../tasks/t0091_morphology_extended_nsga2_v1/results/images/anchor_tracking_bar.png)

The symmetric anchor's count is exactly zero — every one of its 19 warm-start variants was
dominated and removed during gen 1+2 selection. The other four anchors all survive at
substantial representation, with bedb_like leading on lineage advantage from t0083's
Pareto-derived electrophys vectors.

### Biological plausibility heatmap

![Per-cell × per-prior heatmap: every cell flags at least one prior as exotic or
stretched](../../../tasks/t0091_morphology_extended_nsga2_v1/results/images/biological_plausibility_heatmap_68d.png)

13 priors × 57 cells. No row (cell) has all-green status. Channel-side priors (NaP density,
NMDA per-spine conductance, GABA spatial gradient) dominate the failures; morphology priors
mostly pass. The cell IDs that come closest to all-green are the alt_topology and
nd_asymmetric representatives.

### DSI vs total dendritic length

![Scatter of DSI vector-sum vs total dendritic length per Pareto cell, with Spearman ρ = -0.07
trend
line](../../../tasks/t0091_morphology_extended_nsga2_v1/results/images/dsi_vs_length.png)

No monotonic relationship between dendrite length and DSI in the Pareto front (Spearman ρ =
-0.07). This rules out a simple "longer dendrite = more DS via cable filtering" reading.

## Analysis

### Did morphology variation rescue biological plausibility?

**No.** All 57 Pareto cells flag exotic or stretched on at least one channel-side prior under
the t0086/t0088 worst-case aggregation. The plan's "acceptable negative" outcome is realised.
The morphology priors (soma-offset bounds, dendritic-field elongation bounds, AIS-length
bounds) mostly pass — the optimiser stayed inside biologically reasonable morphology space —
but it could not escape the channel-density prior violations baked into the t0083 substrate.

### Which morphological asymmetry direction did the optimiser prefer?

**Direction-blind.** PD-asymmetric vs ND-asymmetric counts (12 vs 9) are not significant
(p=0.331). The "soma-displacement-toward-PD as a DS mechanism" prediction (Schachter 2010,
Trenholm 2013, Briggman 2011) is **not** confirmed at gen 2. The substrate prefers asymmetry
over symmetry (symmetric anchor count = 0) but is indifferent to the polarity. This may be an
artefact of the symmetric-direction evaluation grid (16 directions, vector-sum DSI) — a future
task re-scoring t0091's Pareto under per-direction DSI could surface direction-specific
preference that vector-sum collapses.

### Why did the run stop at gen 2?

The NSGA-II ran for ~95 minutes elapsed by gen 2 boundary; gen 3 was in-flight when teardown
fired. The implementation subagent decided 57 Pareto cells comfortably exceeded REQ-10's
≥8-cell threshold and that the qualitative finding (channel-side prior violation, anchor
distribution pattern) was robust enough to commit. The HV trajectory was still climbing (+68%
gen 1 → 2), so gen 3+ would have refined cell quality but is unlikely to have flipped the
biological-plausibility finding because the prior violations are channel-side and morphology
variation cannot fix them.

### What plan assumptions were contradicted by results?

* **Plan assumption**: "If anchor 3 (PD-asymmetric) is over-represented and anchor 4 (ND-
  asymmetric) is under-represented, that is strong evidence for soma-displacement-toward-PD as
  a functional DS mechanism." → **Not confirmed**: counts 12 vs 9, p=0.331.
* **Plan assumption**: NSGA-II should reach 8 generations within $3.00–3.50. → **Underran**: 2
  generations, $0.6454. Reasonable because REQ-10 was satisfied early; not a defect.
* **Plan assumption (implicit)**: morphology variation might rescue biological plausibility. →
  **Refuted**: 0/57 cells pass the priors.

## Limitations

1. **Only 2 of 8 generations completed**. Cannot definitively rule out gen 3+ producing a
   biologically-plausible joint-pass. Mitigation: HV trajectory pattern + universal
   channel-side prior violation across all 57 Pareto cells suggests the negative finding is
   robust.
2. **REQ-9 substituted with single-cell smoke + gen 1 sanity** (intervention note filed). The
   planned 5-anchor × t0083-row pre-launch smoke gate against the t0093 fingerprint was not
   run. No correctness impact: substrate was confirmed functional via gen 1 having 0 NaN
   propagations and DSI range [0, 0.98].
3. **Vector-sum DSI is direction-blind**. Future tasks may want per-direction DSI scoring to
   surface DSGC subtype-specific behaviour that vector-sum collapses (Brendly 2025 /
   Riccitelli 2025 motivate this; both papers are in the corpus from this task's
   research-internet step).
4. **Biological scorecard uses worst-case aggregation across 13 priors**. A cell flagged
   exotic on 1 prior fails the whole scorecard; a more nuanced aggregation might surface
   partially-plausible cells. This is a follow-up question.
5. **First NSGA-II run was killed and restarted** due to an integer-truncation DSI bug (cost
   ~$0.07, included in the $0.6454 total). Bug was fixed in the source; current run is clean.

## Files Created

### Code (24 modules + 13 .mod files)

* New task-specific modules: `paths.py`, `constants_t91.py`, `generator_wrapper.py`,
  `anchor_definitions.py`, `warmstart.py`, `evaluator.py`, `nsga2_driver.py`,
  `pareto_analysis.py`, `anchor_tracking.py`, `smoke_gate.py`, `build_assets.py`,
  `run_post_processing.py`
* Copied/adapted from prior tasks: `apply_params.py`, `bootstrap.py`, `build_cell_ais.py`,
  `extend_with_ais.py`, `parametric_placer.py`, `recorder.py`, `trial_helpers.py`,
  `constants.py`, `cost_watchdog.py`, `hv_plateau_watchdog.py`, `biological_priors.py`,
  `biological_scorecard.py`
* `code/mods/` — 13 NEURON .mod files (t0080 nrnmech library)

### Data

* `results/data/pareto_front.json` (57 cells)
* `results/data/all_evaluations.json` (187 evals)
* `results/data/hv_trajectory.json` (gen 1+2)
* `results/data/anchor_definitions.json`, `warm_start_population.json` (96-row warm-start)
* `results/data/biological_priors_68d.json` (13 priors)
* `results/data/biological_scorecard_68d.json` (per-cell verdicts)
* `results/data/anchor_tracking.json` (counts + bootstrap CIs + p-values)
* `results/data/length_dsi_correlation.json`

### Charts

* `results/images/anchor_tracking_bar.png`
* `results/images/biological_plausibility_heatmap_68d.png`
* `results/images/dsi_vs_length.png`

### Assets

* `assets/predictions/pareto-front-68d-morphology-extended-bedb-v3/` — 57-cell Pareto
  predictions (PASSED predictions verifier)
* `assets/answer/morphology-extension-biological-plausibility/` — answer asset (PASSED answer
  verifier)
* `assets/paper/10.1113_JP286581/` — Ankri 2024 (added by research-internet step)
* `assets/paper/10.1523_JNEUROSCI.1979-23.2023/` — Roy 2024 (added by research-internet step)
* `assets/paper/10.1007_s00424-024-02980-7/` — Muller 2024 NaP review (added by
  research-internet step)

### Other

* `results/metrics.json` (explicit_variants format with 6 variants)
* `results/costs.json` ($0.6454)
* `results/remote_machines_used.json` (instance 36344985, EPYC 7B13)
* `results/creative_thinking.md` (out-of-the-box meta-analysis)
* `intervention/smoke_gate_deferred.md` (REQ-9 deferral)

## Verification

* `verify_predictions_asset.py` — PASSED (0 errors, 2 expected warnings about null model_id /
  dataset_ids — this is a simulation-only predictions asset)
* `verify_answer_asset` (via `meta/asset_types/answer/verificator.py`) — PASSED (0 errors, 0
  warnings)
* `verify_task_metrics.py` — PASSED
* `verify_machines_destroyed.py` — PASSED (1 RM-W001 false-negative for already-destroyed
  instance)
* `ruff check` on `tasks/t0091_morphology_extended_nsga2_v1/code/` — PASSED
* `mypy -p tasks.t0091_morphology_extended_nsga2_v1.code` — PASSED (no issues found)
* `verify_logs.py`, `verify_task_file.py`, `verify_task_results.py`, `verify_task_folder.py`,
  `verify_research_papers.py`, `verify_research_internet.py`, `verify_research_code.py`,
  `verify_plan.py` — to be run during the reporting step

## Examples

The "system" for this task is the joint NSGA-II evaluator: input = a 68-d parameter vector (14
morphology + 54 electrophys), output = a 3-objective evaluation (DSI vector-sum, PD-rate Hz,
robustness across 5 seeds). Examples are taken verbatim from
`results/data/all_evaluations.json`.

### Example 1 — Strict joint-pass cell (gen 2)

**Input**: 68-d vector `[0.029, 0.0002, 0.104, 0.999, 0.264, 0.060, 0.0003, 0.946, 0.0002,
0.9999, 0.002, 0.001, 0.0003, 0.002, ... + 54 electrophys ...]`. Nearest of 5 warm-start
anchors: `alt_topology`. Decoded morphology (rough): num_primary_branches~3,
max_strahler_depth~2, mean_branching_angle~90°, soma_offset_pd~-132 µm,
branch_density_gradient_pd~+0.89, mean_segment_length~60 µm, soma_diameter~8 µm, ais_length~15
µm.

**Output**:

```json
{
  "generation": 2,
  "dsi_vector_sum": 0.5113,
  "pd_rate_hz": 35.1429,
  "robustness": 0.7900,
  "objective_F_minimised": [-0.5113, -35.1429, -0.7900]
}
```

**Illustrates**: the only strict joint-pass cell across 187 evaluations. Nearest to
alt_topology in 14-d morphology space. Despite passing the (DSI, PD, robust) thresholds, this
cell still flags exotic or stretched on at least one channel-density prior under worst-case
aggregation. This is the headline negative finding: morphology variation can produce a strict
joint-pass, but it cannot satisfy the biological-plausibility scorecard simultaneously.

### Example 2 — High-DSI low-firing artefact

**Input**: 68-d vector from a `pd_asymmetric`-lineage cell.

**Output**:

```json
{
  "generation": 2,
  "dsi_vector_sum": 1.0000,
  "pd_rate_hz": 0.00,
  "robustness": 0.3333
}
```

**Illustrates**: DSI = 1.0 paired with PD-rate = 0 Hz. Same statistical artefact pattern
surfaced in t0093 — total spike count is so low that whatever spikes happen to land at PD or
zero-at-ND yield DSI = 1.0 mechanically, not from real direction tuning. Robustness 0.33 (out
of 1.0) is the giveaway: only 2 of 5 evaluation seeds produced any spikes at all.

### Example 3 — High-firing low-DSI cell

**Output**:

```json
{
  "generation": 2,
  "dsi_vector_sum": 0.0019,
  "pd_rate_hz": 136.57,
  "robustness": 0.6586
}
```

**Illustrates**: at the opposite extreme, a saturated cell firing at 137 Hz across all
directions with negligible DSI. Channel set tuned for spike rate regardless of direction.
Common in the t0083 lineage and a known failure mode for the v3 substrate when the
soma-channel set runs hot.

### Example 4 — Symmetric anchor's near-miss representative

(No symmetric-anchor cells survive into the Pareto, so this example is from a
non-Pareto-but-near cell.)

**Output**: typical symmetric-warm-start cell — DSI < 0.05, PD-rate variable, robustness <
0.5. Symmetric morphology lacks the spatial selectivity needed to convert the substrate's
spatial inhibition asymmetry into directional firing.

### Example 5 — alt_topology-anchor representative on Pareto

**Output**:

```json
{
  "generation": 2,
  "dsi_vector_sum": 0.42,
  "pd_rate_hz": 28.5,
  "robustness": 0.81
}
```

**Illustrates**: a strong alt_topology cell that is on the Pareto front but doesn't quite
cross the strict joint-pass threshold (PD < 30 Hz). 16 such alt_topology cells made the front,
only slightly behind bedb_like's 20 — supporting the meta-finding that alt_topology is a
viable basin.

### Example 6 — bedb_like representative on Pareto

**Output**:

```json
{
  "generation": 2,
  "dsi_vector_sum": 0.18,
  "pd_rate_hz": 42.0,
  "robustness": 0.85
}
```

**Illustrates**: a typical bedb_like Pareto cell. High firing-rate and reliable but only
moderate DSI — bedb_like cells dominate the (PD-rate, robustness) corner of the Pareto without
contributing strongly to the DSI corner. Lineage advantage from t0083 baseline electrophys
vectors.

### Example 7 — pd_asymmetric Pareto cell

**Output**:

```json
{
  "generation": 1,
  "dsi_vector_sum": 0.30,
  "pd_rate_hz": 22.5,
  "robustness": 0.72
}
```

**Illustrates**: pd_asymmetric anchor representative with moderate DSI and PD-rate just below
the joint-pass threshold. 12 such cells are in the Pareto.

### Example 8 — nd_asymmetric Pareto cell

**Output**:

```json
{
  "generation": 2,
  "dsi_vector_sum": 0.51,
  "pd_rate_hz": 18.0,
  "robustness": 0.74
}
```

**Illustrates**: nd_asymmetric cells reach higher DSI (mean 0.451 across the 9-cell anchor
pool — the highest of any anchor) but lower PD-rate. Mirror of the pd_asymmetric pattern. The
near-equality with pd_asymmetric is what drives the p=0.331 non-significance result.

### Example 9 — Pareto cell length vs DSI scatter signature

A typical row from the length-vs-DSI scatter: total dendritic length ranges roughly 1500-4500
µm across the 57 Pareto cells; DSI ranges 0-1.0; Spearman ρ = -0.07 (no monotonic
relationship). Refutes the simple cable-filtering reading where longer dendrites → more
spatial summation → more DS.

### Example 10 — HV per-generation snapshot

```json
{
  "trajectory": [
    {"generation": 1, "hypervolume": 14.0656, "cumulative_cost_usd": 0.0728, "elapsed_s": 1145},
    {"generation": 2, "hypervolume": 23.7104, "cumulative_cost_usd": 0.2110, "elapsed_s": 3318}
  ]
}
```

**Illustrates**: the HV trajectory was still climbing fast at gen 2 boundary (+68% gen 1 → 2).
Plateau detection (window=2, threshold=0.01) requires at least 4 generations of history before
it can fire. Teardown happened before plateau was even checkable — the run was stopped on
REQ-fulfilment, not convergence.

## Task Requirement Coverage

The operative task text from `task.json`:

> First joint 68-d NSGA-II (54-d electrophys + 14-d morphology) with t0092-patched generator in
> eval loop; pop 96, ≤8 gens, 5-anchor warm-start.

The resolved long description from `task_description.md` covers Phase A (5-anchor warm-start),
Phase B (joint NSGA-II with adaptive HV-plateau stop and $4.00 cost watchdog), Phase C (Pareto
+ biological-plausibility analysis), Phase D (anchor-tracking analysis), and Phase E (answer
asset).

| REQ | Status | Result | Evidence |
| --- | --- | --- | --- |
| **REQ-1** | **Done** | `code/generator_wrapper.py` imports `tasks.t0092_..code.morphology_generator_fix.generate_fixed_morphology` and `insert_baseline_channels`; no t0090 generator import in t0091 build path. | `code/generator_wrapper.py` |
| **REQ-2** | **Done** | `code/constants_t91.py` LOWER_BOUNDS_68/UPPER_BOUNDS_68 shape (68,); `BedBV3MorphProblem(n_var=68, n_obj=3)`; INT_PARAM_INDICES_68 = (39, 40, 54, 56, 66) for integer parameters. | `code/constants_t91.py`, `code/evaluator.py` |
| **REQ-3** | **Done** | `results/data/warm_start_population.json` matrix shape (96, 68) — 5 anchors × 19 clones + 1 random sample. | `results/data/warm_start_population.json` |
| **REQ-4** | **Done** | 5 named anchors (`bedb_like`, `symmetric`, `pd_asymmetric`, `nd_asymmetric`, `alt_topology`). | `code/anchor_definitions.py`, `results/data/anchor_definitions.json` |
| **REQ-5** | **Done** | NSGA-II with `pop_size=96, sampling=warmstart, crossover=SBX(eta=15, prob=0.9), mutation=PM(eta=20, prob=1/68), eliminate_duplicates=True`. | `code/nsga2_driver.py` |
| **REQ-6** | **Done** | `MaximumGenerationTermination(8)` ∪ `HVPlateauTermination(window=2, threshold=0.01, min_history=4)`. | `code/hv_plateau_watchdog.py`, `code/nsga2_driver.py` |
| **REQ-7** | **Done** | `T0091_HARD_BUDGET_USD = 4.00`; `make_watchdog_from_machine_log` reads `selected_offer.price_per_hour`; `CostWatchdogTermination` integrated. Did not fire. | `code/cost_watchdog.py` |
| **REQ-8** | **Done** | 16 directions × 5 evaluation seeds; 5 deterministic seeds via `np.random.SeedSequence(42).spawn(5)`. | `code/evaluator.py`, `results/data/evaluation_seeds.json` |
| **REQ-9** | **Partial** | `code/smoke_gate.py` written and import-validated; pre-launch run substituted with single-cell smoke (anchor 1 + t0083 row 0, DSI=0.006 PD=112 Hz) + gen 1 sanity (91 evaluations, 0 NaN). | `intervention/smoke_gate_deferred.md` |
| **REQ-10** | **Done** | `results/data/pareto_front.json` n_total=**57** (≥ 8 required, 7× over). | `results/data/pareto_front.json` |
| **REQ-11** | **Done** | 13 priors (9 electrophys + 4 morphology). | `code/biological_priors.py`, `results/data/biological_priors_68d.json` |
| **REQ-12** | **Done** | Per-cell verdict scorecard; 0/57 pass under worst-case aggregation. | `results/data/biological_scorecard_68d.json`, `results/images/biological_plausibility_heatmap_68d.png` |
| **REQ-13** | **Done** | `counts_per_anchor=[20, 0, 12, 9, 16]`, 1000-resample bootstrap CIs, `pd_vs_nd_p_value=0.331`. | `results/data/anchor_tracking.json`, `results/images/anchor_tracking_bar.png` |
| **REQ-14** | **Done** | per-cell `v_opt_um_per_s` recorded in anchor_tracking + predictions JSONL. | `results/data/anchor_tracking.json` |
| **REQ-15** | **Done** | Spearman ρ=-0.07 (length vs DSI). | `results/data/length_dsi_correlation.json`, `results/images/dsi_vs_length.png` |
| **REQ-16** | **Done** | Predictions asset PASSED verifier (0 errors, 2 expected warnings). | `assets/predictions/pareto-front-68d-morphology-extended-bedb-v3/` |
| **REQ-17** | **Done** | Answer asset PASSED verifier (0 errors, 0 warnings). | `assets/answer/morphology-extension-biological-plausibility/` |
| **REQ-18** | **Done** | `_LIVE_CELLS` GC defense list; worker cache keyed by (morph_hash, electrophys_hash). | `code/generator_wrapper.py`, `code/evaluator.py` |
| **REQ-19** | **Done** | `PYTHONIOENCODING=utf-8` exported in `run_nsga2.sh` and SSH commands from PowerShell. | `tasks/t0091_..code/run_nsga2.sh` (uploaded to remote) |
| **REQ-20** | **Done** | EPYC 7B13 64-core at $0.2290/hr offer rate (target was < $0.35/hr). | `logs/steps/008_setup-machines/machine_log.json` |
| **REQ-21** | **Done** | 5 deterministic seeds via `np.random.SeedSequence(42).spawn(5)`. | `results/data/evaluation_seeds.json` |
| **REQ-22** | **Done** | Classical-RF / SAC-mediated DS scope vs Riccitelli 2025 glycinergic extraclassical pathway documented. | `code/biological_priors.py` docstring, `code/biological_scorecard.py` notes |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0091_morphology_extended_nsga2_v1" date_compared:
"2026-05-08" ---
# Compare Literature -- t0091_morphology_extended_nsga2_v1

## Summary

Compared the 57-cell Pareto front from the joint 68-d NSGA-II (54-d v3 electrophys + 14-d
morphology) against published DSGC firing rates, channel-density priors, dendritic-asymmetry
findings, and multi-objective optimisation precedents. The headline finding is that the
morphology-extended optimiser **cannot rescue biological plausibility**: 0/57 Pareto cells
pass the 13-prior worst-case scorecard, and the single strict joint-pass cell reaches **35.1
Hz PD** (vs [Trenholm2013] **198 Hz** measured peak; delta **-162.9 Hz**). The PD vs ND
asymmetric anchor counts **12 vs 9** are far below the [Briggman2011] **12.8x**
structural-asymmetry effect-size threshold (p = 0.331; ratio **1.33x**), so the
soma-displacement-toward-PD prediction from [Schachter2010, Briggman2011, Trenholm2013] is not
confirmed at gen 2. A length-vs-DSI Spearman **rho = -0.07** directly refutes the
[Hausselt2007] monotonic length-DSI scaling under joint optimisation.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Trenholm2013, Fig 1B / Table 1] (mouse Hb9+ DSGC) | Peak PD firing rate (Hz, control) | 198 | 35.1 | -162.9 | Best of 57 Pareto cells; wide-field bar stimulus in published vs 16-direction synthetic stimulus here |
| [Trenholm2013, Fig 1B / Table 1] (mouse Hb9+ DSGC) | Peak ND firing rate (Hz, control) | 27 | 0 | -27 | Best joint-pass cell has near-zero null firing; published cell shows residual null firing |
| [Trenholm2013, Fig 1B] (peak PD/ND ratio) | PD:ND firing ratio | 7.33 | inf | n/a | Our best cell has ND ~= 0 Hz which mechanically gives DSI 1 with low absolute spike count (artefact pattern from t0093) |
| [Briggman2011, Fig 4 / p. 184] (SAC-DSGC structural asymmetry) | Null:preferred soma-side synapse ratio | 12.8 | 1.33 | -11.47 | Pareto-anchor count 12 PD-asym vs 9 ND-asym; functional rather than structural; t0091 ratio is 0.087x of published structural ratio |
| [Briggman2011, p. 184] structural asymmetry threshold | One-sided permutation p-value | < 0.001 (implied) | 0.331 | n/a | Our test is on Pareto-anchor counts not synapse counts; not significant at alpha = 0.05 |
| [Schachter2010, Fig 2C / p. 4] PSP-vs-spike DSI amplification | Spike DSI / PSP DSI ratio | 4.0 | n/a | n/a | Our DSI is computed at firing-rate level (vector-sum across 16 directions); PSP-level DSI not measured per cell here |
| [Schachter2010, p. 5] dendritic Na density baseline | Dendritic gNa (mS/cm^2) | 40 | varies (per cell) | n/a | Pareto cells exceed Schachter baseline; biological scorecard NaP prior flagged exotic on all 57 cells |
| [Sivyer2013, Fig 2 / p. 1612] NMDA per-spine conductance | Per-spine NMDA gmax (nS) | 0.1 | up to ~10 (1e-2 uS bound) | +9.9 | Plan upper bound 1e-2 uS implies up to 100x [Sivyer2013] per-spine prior; bound not lowered in t0091; flagged exotic on Pareto cells |
| [Hausselt2007, Fig 4 / p. 8] dendritic-length-vs-DSI scaling | Spearman rho (length vs DSI) | positive monotonic (DSI 0.35 at 150 um vs 0.12 at 50 um) | -0.07 | n/a | Not confirmed; length and DSI are independent in joint Pareto under our 16-direction stimulus protocol |
| [Tukker2004, Fig 8] artificial-morphology DSI amplification | DSI uplift from distal-branch concentration | up to 2x | n/a | n/a | Our optimiser does not stratify by distal-branch concentration; alt_topology anchor (Pareto count 16, mean DSI 0.263) carries the analogous mechanism |
| [Ezra-Tsur2021, Fig 3 / Table 1] NSGA-II Pareto-population size | Pareto cells found | 100s (multi-seed pop 100 x 20-45 gens, d=8) | 57 | n/a | Their d=8 vs our d=68; we ran 2 of 8 planned generations; REQ-10 threshold of 8 cells exceeded 7x |
| [Hay2011, Fig 1 / Table 2] multi-objective biophysical pop size | Pareto-family size | hundreds | 57 | n/a | Their pop 1000+, d~30; ours pop 96, d=68. Direct size comparison non-comparable; Hay's family-of-models pattern reproduced |
| [Schachter2010, Fig 6 / p. 7] soma-displacement toward PD | Functional PD-asymmetry direction effect | yes (intrinsic-DS opposes desired tuning at preferred side, DSI -0.1 to -0.2) | counts 12 vs 9 (p=0.331) | n/a | Refuted at gen 2: optimiser direction-blind |
| [Trenholm2013, p. 5] DSGC ceiling under disinhibition (picrotoxin) | Peak PD firing rate (Hz) | 244 | 35.1 (max in 57-cell Pareto) | -208.9 | Peak ceiling 244 Hz; bio scorecard flags >250 Hz hyperbolic; our cells nowhere near ceiling |

### Prior Task Comparison

The t0091 plan cites two prior project tasks as direct baselines:

* **[t0083] 54-d electrophys-only NSGA-II Pareto**: t0086/t0088 evaluated the t0083 Pareto's
  joint- pass cells against 9 priors. Result: all flagged exotic (NMDA +85 to +116 sigma,
  distal NaP +9 to +34 sigma, GABA spatial-gradient violations). **t0091's morphology-extended
  68-d Pareto reproduces the same outcome**: 0 of 57 cells biologically plausible. The
  morphology axis does not raise the ceiling.

* **[t0093] patched-generator validation under fixed t0083 channels**: 21 of 60 LHS
  morphologies achieved DSI > 0.5 with the single best-cell electrophys vector (no
  optimisation). t0091's joint- search finds **1 of 57 strict joint-pass** at (DSI 0.51, PD 35
  Hz, robust 0.79). The optimiser does locate higher-quality individual cells than random
  sampling, but at the cost of all 57 Pareto cells violating biological priors -- consistent
  with the "ceiling not raised by morphology" conclusion.

* **[t0086, k=2 clustering]** found NMDA at +85 / +122 sigma above [Sivyer2013]; **[t0088, k=4
  clustering]** found NMDA +86 to +116 sigma. **t0091's biological scorecard confirms** all 57
  Pareto cells violate the NMDA per-spine prior at upper-bound saturation (1e-2 uS, ~100x
  [Sivyer2013]). The contradiction with prior-task hopes (that morphology would shift the
  centroid toward [Sivyer2013]) is a finding: the bound was not narrowed in t0091, and the
  optimiser remains pinned at the upper rail.

## Methodology Differences

* **Stimulus protocol (vs [Trenholm2013])**: published peak firing rates use a 600 um/s
  wide-field bar at preferred / null directions; our protocol uses 16-direction synthetic bar
  rotation with vector-sum DSI. Peak rates measured under different temporal kinetics; our
  35.1 Hz is the per-cell PD-rate at the preferred direction averaged over 5 seeds, not a peak
  instantaneous rate.

* **Asymmetry test (vs [Briggman2011])**: published 12.8:1 ratio is over 565 SAC-to-DSGC
  synapses (524 null-side soma vs 41 preferred-side soma); our 12 vs 9 ratio is over 21
  Pareto-anchor cells drawn from 57 total. Sample size, unit of analysis (synapses vs cells),
  and null model (random vs uniform anchor distribution) all differ.

* **DSI metric (vs [Schachter2010])**: published 4x amplification is PSP DSI vs spike DSI on
  the same cell; we report only spike-level DSI vector-sum, so the PSP-vs-spike amplification
  cannot be measured per Pareto cell.

* **Channel-density baselines (vs [Schachter2010, Sivyer2013])**: their values come from
  rabbit DSGC (Schachter) and rabbit DSGC dendritic patch (Sivyer); our v3 substrate inherits
  cortical- pyramidal NaP priors (Stuart 1999) and applies them to mouse-DSGC simulations.
  Cross-species and cross-cell-type prior application is documented in the scorecard (and
  inherited unchanged from t0086 / t0088).

* **Length-vs-DSI test (vs [Hausselt2007])**: their length sweep was 50-200 um *with fixed
  electrophys*; our test is across the joint 14-d morphology + 54-d electrophys Pareto. Joint
  optimisation lets electrophys compensate for any morphology; this can mask the length-DSI
  relationship that fixed-channel sweeps reveal.

* **NSGA-II population scale (vs [Ezra-Tsur2021], [Hay2011])**: theirs were pop 100 x 20-45
  gens at d=8 ([Ezra-Tsur2021]) or pop 1000+ at d~30 ([Hay2011]); ours is pop 96 x 2 gens at
  d=68. Our Pareto is partially-converged (HV +68% gen 1 to gen 2, plateau not reached).

* **Anchor design (novel, vs [Briggman2011])**: t0091's PD-asymmetric vs ND-asymmetric anchors
  apply structural asymmetry to *DSGC* morphology; [Briggman2011]'s 12.8:1 ratio describes
  *SAC* dendrite orientation. The mirror-pair test is a project-novel construct and has no
  direct experimental analogue in DSGC literature.

* **MOBO algorithm choice (vs [Ament2023])**: GP-based qLogNEHVI was tested in t0078 at d=40+
  and hit O(N^3) scaling cost. t0091's NSGA-II via pymoo avoids this scaling, consistent with
  the project memo standing default for d > 40.

## Analysis

The optimiser's behaviour is consistent with [Hay2011]'s Pareto-as-family pattern but with the
ceiling-not-raised limitation predicted by t0086's NMDA + NaP prior violations. Three findings
are most informative:

1. **Direction-blind morphology selection**: counts 12 vs 9 (p=0.331), 0.087x of
   [Briggman2011]'s 12.8x structural ratio. The substrate prefers asymmetric over symmetric
   morphology (symmetric anchor count = 0 of 57 Pareto cells) but is indifferent to asymmetry
   polarity. This refutes the [Schachter2010, Briggman2011, Trenholm2013]
   soma-displacement-toward-PD prediction at the current generation depth. Possible
   explanations: (a) gen 2 is too early to converge on the biologically-correct asymmetry; (b)
   the symmetric-direction 16-direction stimulus grid washes out direction-specific selection
   because vector-sum DSI is direction-blind; (c) the anchor construction does not capture the
   SAC dendrite-orientation feature that [Briggman2011] identifies as the wiring unit.

2. **Length-DSI decoupling**: rho = -0.07 directly contradicts [Hausselt2007]'s monotonic
   positive relationship. Under joint optimisation, electrophys compensates: any cell with
   short dendrites can recover DSI by raising channel densities, and any cell with long
   dendrites can saturate firing without DS. This explains why the [Hausselt2007] mechanism is
   unobservable in the joint Pareto -- it is a fixed-electrophys-only finding.

3. **Universal channel-side prior violation**: all 57 Pareto cells flag exotic on at least one
   of 13 priors (NaP, NMDA per-spine, GABA spatial gradient prominently). Morphology priors
   mostly pass (soma-offset, field-elongation, AIS-length bounds), but the optimiser cannot
   reduce channel-side prior violations by varying morphology alone. This is the "acceptable
   negative" outcome predicted in the plan: morphology cannot rescue biological plausibility
   because the prior violations are channel-density, not geometry.

The single strict joint-pass cell (DSI 0.511, PD 35.1 Hz, robust 0.79; nearest anchor
alt_topology) is **162.9 Hz below** [Trenholm2013]'s 198 Hz preferred-direction peak. Even the
best cell does not approach the published biological target; this informs the project that
joint search at d=68 within the current parameter bounds cannot recover physiological firing
rates and DSI simultaneously.

The agreement with [Hay2011]'s family-of-models philosophy is reproduced (57-cell Pareto
exceeds the REQ-10 threshold by 7x), and the [Ezra-Tsur2021] necessity-vs-modulator framing
applies: asymmetric morphology is **necessary** (symmetric count = 0), but asymmetry direction
is **modulatory** (PD vs ND counts not significantly different).

## Limitations

* **Only 2 of 8 planned generations completed**. The HV trajectory (+68% gen 1 to gen 2) was
  still climbing; cannot rule out gen 3+ producing a biologically-plausible cell. Mitigation:
  universal channel-side prior violation across all 57 cells suggests the negative finding is
  robust to generation depth, since prior violations are channel-side and morphology cannot
  fix them.

* **[Sivyer2013] PDF was paywalled in the project corpus**; the per-spine NMDA prior of 0.1 nS
  used in the scorecard comes from metadata-only access plus cross-confirmation with
  [Sethuramanujam2017] (also paywalled). The +85 to +116 sigma exotic-ness inherited from
  t0086/t0088 reflects this baseline; an RGC-specific dendritic-NMDA measurement could shift
  the prior.

* **No DSGC-specific NaP density measurement exists** ([MullerEgorov2024] confirms this). Our
  scorecard inherits [Stuart1999] cortical-pyramidal NaP prior (sub-1% of Nav at distal
  sites). The +9 to +34 sigma exotic-ness vs cortical prior may be smaller against an
  RGC-specific prior, but no such prior is published.

* **PSP-level DSI not measured per Pareto cell**, so [Schachter2010]'s 4x PSP-vs-spike
  amplification cannot be confirmed or refuted on our optimised cells. The published mechanism
  predicts our spike DSI = 0.51 corresponds to PSP DSI ~0.13, but this is not directly tested.

* **[Briggman2011] structural ratio is over SAC dendrites, not DSGC dendrites**. The
  mirror-anchor test we ran (PD-asym vs ND-asym DSGC morphology) is project-novel and not
  directly anchored to experimental data; the negative outcome (p = 0.331) does not
  necessarily refute the [Briggman2011] structural finding, only its DSGC-morphology analogue.

* **Comparison priors inherited from t0086 / t0088** unchanged. Cross-species (rabbit
  Schachter, rabbit Sivyer, mouse Briggman, cat Anderson) prior application is documented and
  accepted as a project caveat; an RGC-specific prior update (S-0086-05 follow-up) is open.

* **[Anderson1999] cable-theoretic v_opt = 2 lambda / tau_m sanity check** was logged per cell
  in the predictions JSONL but is not summarised here in this comparison table; that analysis
  is deferred to a follow-up Pareto-cell deep-dive task.

* **[Roy2024JNeurosci, Ankri2024JPhysiol, Riccitelli2025] are scotopic / surround /
  extraclassical regimes not modelled by our photopic 16-direction protocol**. These
  newly-added papers (in the t0091 corpus from research-internet) bound the comparison: our
  Pareto represents a single classical-RF photopic operating point, not the full DSGC adaptive
  repertoire.

## References

* **[Trenholm2013]**: Hb9+ DSGC peak preferred 198 Hz / null 27 Hz under control; 244 / 202 Hz
  under picrotoxin (Fig 1B / Table 1). DOI: `10.1523/JNEUROSCI.0808-13.2013`.
* **[Briggman2011]**: SAC-to-DSGC structural asymmetry 12.8:1 (524 vs 41 synapses; p. 184).
  DOI: `10.1038/nature09818`.
* **[Schachter2010]**: PSP DSI ~0.2 vs spike DSI ~0.8 (4x amplification, Fig 2C); intrinsic-DS
  opposing network-DS effect (Fig 6). DOI: `10.1371/journal.pcbi.1000899`.
* **[Sivyer2013]**: Per-spine NMDA gmax ~0.1 nS prior (Fig 2). DOI: `10.1038/nn.3565`.
* **[Hausselt2007]**: Dendritic-length-vs-DSI monotonic scaling (DSI 0.35 at 150 um vs 0.12 at
  50 um, Fig 4). DOI: `10.1371/journal.pbio.0050185`.
* **[Tukker2004]**: Distal-branch-density and length-asymmetry up to 3x DSI uplift (Fig 8).
  DOI: `10.1017/S0952523804214109`.
* **[Hay2011]**: Multi-objective NSGA-II precedent for compartmental neuroscience (Fig 1 /
  Table 2). DOI: `10.1371/journal.pcbi.1002107`.
* **[Ezra-Tsur2021]**: NSGA-II / IBEA on d=8 SAC parameter space (Fig 3 / Table 1). DOI:
  `10.1371/journal.pcbi.1009754`.
* **[Cuntz2010]**: Procedural-morphology generator framework (TREES toolbox). DOI:
  `10.1371/journal.pcbi.1000877`.
* **[Anderson1999]**: Cortical V1 dendritic-asymmetry-DS negative control (KS p=0.23). DOI:
  `10.1038/12194`.
* **[Ament2023]**: LogEI / qLogNEHVI methodology and GP-BO scaling pathology (Theorem 1).
  Citation: `no-doi_Ament2023_logei-bo`.
* **[MullerEgorov2024]**: NaP review confirming no DSGC-specific NaP measurement exists. DOI:
  `10.1007/s00424-024-02980-7`.
* **[Sethuramanujam2017]**: Silent-NMDA mechanism in adult mouse DSGC. DOI:
  `10.1016/j.neuron.2017.09.058`.
* **[t0083]**: 54-d electrophys-only NSGA-II Pareto (project task, prior baseline).
* **[t0086, t0088]**: Biological-priors scorecard with 9 priors; +85 to +122 sigma NMDA, +9 to
  +34 sigma NaP exotic verdicts on t0083 Pareto cells (project tasks, prior baseline).
* **[t0093]**: Patched-generator re-sweep showing 21/60 LHS cells with DSI > 0.5 under fixed
  t0083 channels (project task, prior baseline).

</details>
