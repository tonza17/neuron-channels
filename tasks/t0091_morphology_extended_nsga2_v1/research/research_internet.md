---
spec_version: "1"
task_id: "t0091_morphology_extended_nsga2_v1"
research_stage: "internet"
searches_conducted: 14
sources_cited: 18
papers_discovered: 4
date_completed: "2026-05-08"
status: "complete"
---
## Task Objective

t0091 runs the project's first joint 68-d NSGA-II (54-d v3 electrophys + 14-d morphology) with the
t0092-patched procedural DSGC morphology generator inside the evaluation loop. The optimisation uses
pop 96, up to 8 generations, an adaptive HV-plateau stop, a $4.00 cost watchdog, and a 5-anchor
warm-start (Bed-B-like + symmetric + PD-asymmetric + ND-asymmetric + alternative-topology). Internet
research for this task targets four areas where `research_papers.md` has gaps: pymoo NSGA-II best
practices for mixed integer-real problems at d>=68, 2024-2026 retinal direction-selectivity
publications that postdate the corpus, cost-watchdog patterns for compute-budgeted NSGA-II, and any
recent biological reference values that update the per-spine NMDA prior, the distal NaP prior, and
the GABA spatial-gradient prior used in the biological-plausibility scorecard.

## Gaps Addressed

The six gaps from `research_papers.md` Gaps and Limitations were reviewed against internet search
results:

1. **No prior NSGA-II at d > 40 in retinal compartmental modelling** — **Partially resolved**. The
   pymoo team and recent benchmarks confirm NSGA-II scales well past d=40 and even handles
   `n_var = 131,072` on ZDT1/ZDT2 with auto-configuration [Lopez-Camacho-2022]. However, no peer-
   reviewed retinal compartmental study at d=68 was found; the closest published precedent remains
   Hay 2011 at d~30 and Ezra-Tsur 2021 at d=8 from the corpus. Best-practice mutation rate
   `prob = 1/L` (L = decision-variable count) and SBX/poly-mutation distribution indices `eta_c=15
   - 30, eta_m=20` are confirmed as standard [Pymoo-NSGA2-Docs, Lopez-Camacho-2022].

2. **No quantitative biological-plausibility scorecard for joint morphology + electrophys cells in
   the literature** — **Unresolved**. No internet source provided a cross-validated 9-prior
   scorecard. The project-specific scorecard (t0086 / t0088) remains the only available framework.

3. **No published soma-displacement-vs-DSI experimental data in DSGC** — **Partially resolved**.
   `[Wei2011-PMC, Webvision-2024]` confirm that "DSGCs with asymmetric dendrites exhibit stronger
   directionally tuned inhibition than symmetric DSGCs" but the *DSGC's own soma position relative
   to its dendritic field* still has no systematic experimental sweep in the literature. t0091's PD-
   vs ND-asymmetric anchor mirror remains a novel test.

4. **No measurement of how t0090's 14 generator knobs map to in-vivo morphological variation** —
   **Unresolved**. NETMORPH, NeuGen, and TREES are alternative procedural-morphology toolboxes
   [NETMORPH-2009, NeuGen-2006] but none publishes a DSGC-specific knob-to-physiology mapping. The
   Cuntz `bf` parameter (project's foundation) remains the best-validated cell-class generator.

5. **Limited published data on per-section vs per-segment NaP density gradients along DSGC
   dendrites** — **Partially resolved**. The 2024 Pflugers Archiv review [MullerEgorov2024]
   confirms that *no* published direct measurement of dendritic NaP density gradient exists in DSGC;
   the Stuart-style cortical priors used in t0086 / t0088 remain the best available baseline. The
   2021 Astman J Neurosci finding that AIS NaP density is "about twofold lower than in the soma" in
   cortical pyramids [Astman-2021] is a useful cross-cell update but does not change the DSGC
   exotic-ness flagging.

6. **Cost-budget watchdog limits the depth of Phase D anchor-tracking analysis** — **Resolved
   (methodology)**. Internet sources confirm that wrapping NSGA-II evaluation calls with a
   cumulative-cost monitor that raises an `EarlyTermination` when budget is exceeded is the standard
   pattern [Pymoo-Termination-Docs]. The pymoo `Termination` API supports compound termination
   conditions that can combine HV-plateau detection with a cost cap. This is exactly the pattern
   t0091 should adopt; specific reference code is documented in the Implementation Patterns section.

## Search Strategy

**Sources searched**: pymoo official documentation (pymoo.org), Google Scholar, PubMed, PNAS, eLife,
Cell Reports, Journal of Neuroscience, Journal of Physiology, Nature, Nature Neuroscience,
ResearchGate, Springer / SpringerLink, MDPI, GitHub (anyoptimization/pymoo issues), Webvision NCBI
Bookshelf, Weizmann Institute lab pages.

**Date range**: 2023-2026 for "recent advances" passes; no date restriction for foundational pymoo /
NSGA-II references.

**Inclusion criteria**: Papers must address either (a) NSGA-II / multi-objective evolutionary
optimisation methodology relevant to d=68 mixed integer-real problems, (b) DSGC / SAC /
direction-selectivity biology with publication date 2024 or later, (c) cost-aware termination /
budget management for evolutionary algorithms, or (d) recent updates to the NMDA / NaP / GABA
biological priors used in the project's scorecard. Excluded: foundation models for retinal disease
imaging (RETFound and similar), non-DS retinal cell research, and pre-2023 references already in the
corpus.

**Queries executed (14 total)**:

*Pass 1 - Gap-targeted queries (NSGA-II at d=68 mixed integer-real)*:

1. `pymoo NSGA-II mixed variable integer real high-dimensional optimization best practices 2024 2025`
2. `NSGA-II mixed integer continuous variables polynomial mutation SBX crossover high-dimensional 60 70 dimensions`
3. `pymoo MixedVariableGA tutorial integer continuous parameter bounds NSGA2`
4. `large-scale benchmark NSGA-II 50+ dimensions multi-objective convergence rate population size guidelines`
5. `pymoo seeding warm-start initial population custom NSGA-II pattern`
6. `NSGA-II hypervolume convergence stopping criteria d>40 high dimensional cost-aware termination`

*Pass 2 - Recent retinal DS biology (2024-2026)*:

7. `retinal direction selective ganglion cell morphology asymmetry 2024 2025 dendrite`
8. `DSGC starburst amacrine cell connectomics 2024 2025 EM reconstruction direction selectivity`
9. `Riccitelli Rivlin-Etzion 2024 2025 PNAS retinal extraclassical receptive field motion direction`
10. `retinal direction selectivity glycinergic amacrine cell 2024 2025 Rivlin-Etzion`

*Pass 3 - Snowball / cost-watchdog / NaP / morphology generators*:

11. `cost watchdog evolutionary algorithm budget limit early stopping NSGA-II compute budget`
12. `multi-objective optimization compute budget early termination cost monitoring genetic algorithm`
13. `"persistent sodium current" NaP cortical pyramidal dendrite 2023 2024 density distal Stuart Sakmann update`
14. `Beg 2024 procedural neuron morphology generator stochastic dendritic tree retinal NEURON`

**Search iterations**: Queries 9 and 10 were follow-ups after query 7 surfaced Riccitelli 2025.
Query 13 was prompted by gap 5 from `research_papers.md` (NaP priors). Query 6 was a follow-up to
queries 1-2 after pymoo termination patterns surfaced as the best mechanism for the cost watchdog.
Query 5 was added when issue #642 in the pymoo repo confirmed warm-start mechanics for the 5-anchor
seed.

## Key Findings

### NSGA-II Mixed Integer-Real at d=68: Pymoo MixedVariableGA Is the Right Building Block

The pymoo `MixedVariableGA` algorithm is the canonical pattern for problems combining integer and
real variables [Pymoo-Mixed-Docs]. The recommended structure is to declare each variable explicitly
in the problem `vars` dict using `Integer(bounds=(lo, hi))` and `Real(bounds=(lo, hi))` types; for
multi-objective problems, instantiate
`MixedVariableGA(pop_size=N, survival=RankAndCrowdingSurvival())` where `RankAndCrowdingSurvival` is
the NSGA-II survival selection imported from `pymoo.algorithms.moo.nsga2`. This is more robust than
passing real-valued variables and rounding to integers post-hoc, because the
SBX-and-polynomial-mutation operators applied to real variables can produce off-grid values that
mutation rounding then clusters at integer boundaries, biasing the search.

**Best practice**: For t0091's 14-d morphology vector containing two integer parameters
(`num_primary_branches`, `max_strahler_depth`) and 12 real parameters, plus the 54-d real
electrophys vector, declare variables as
`vars = {"num_primary_branches": Integer(bounds=(3, 8)), "max_strahler_depth": Integer(bounds=(2, 6)), ..., "electrophys_param_0": Real(bounds=(...)), ...}`
and use `MixedVariableGA(pop_size=96, survival=RankAndCrowdingSurvival())`.

**Hypothesis (HM-4)**: Implementing integer parameters via `MixedVariableGA` rather than
real-with-rounding will reduce premature convergence at the integer-grid boundaries by 10-30 percent
in HV growth at gen 4-6, based on the pymoo team's comments in [Pymoo-Issue-126, Pymoo-Mixed-Docs].

### NSGA-II Scales To Very High Dimensions When Tuned Correctly

A 2022 Mathematical and Computational Applications paper [Lopez-Camacho-2022] benchmarks
auto-configured NSGA-II on ZDT1 / ZDT2 problems with `n_var` up to **131,072 decision variables**.
Standard NSGA-II at d > 100 stalls on the default configuration (pop=100, eta_c=20, eta_m=20,
mut_prob=1/L), but auto-configured variants reach acceptable HV in **<25 million evaluations**. The
key tuning lever is the **mutation distribution index `eta_m`**: for high-d problems, lowering
`eta_m` from 20 to 10-15 produces wider mutation spread per gene, which compensates for the small
fraction of genes mutated each generation under `prob = 1/L`. **A 2025 arXiv paper "Speeding Up the
NSGA-II via Dynamic Population Sizes" [Doerr-2024-arXiv] reports that reducing offspring population
size while increasing generations leads to "similar or statistically significantly better results in
92% of experiments" vs the default NSGA-II configuration**. This validates the project's standing
choice of NSGA-II over BoTorch GP-BO for d > 40 (per the userMemory `nsga2-for-high-d-mobo`).

**Best practice for t0091**: Use `eta_c = 15` (already in plan) and `eta_m = 20`. Mutation
probability `1/68 = 0.0147` is correct. Population 96 with 8 generations gives **768 evaluations**;
this is a small budget for d=68 even with warm-start. The 5-anchor warm-start frontloads ~20 percent
of the population around known-good regions, which is the dominant convergence mechanism here, not
parameter tuning [Pymoo-Initialization-Docs].

### NSGA-II Scaling Studies On Many-Objective vs High-Dimensional Distinction

[Lopez-Camacho-2022] explicitly distinguishes "many-objective" (k > 3 objectives, where NSGA-III is
preferred) from "large-scale" / "high-dimensional" (n_var > 100, where NSGA-II + auto-config still
works). For t0091 with 3 objectives (DSI vector-sum, PD firing rate, robustness) and 68 decision
variables, the regime is **moderately high-dimensional, low-objective-count** — the regime NSGA-II
was designed for. NSGA-III is *not* a better choice here.

### Cost-Watchdog Pattern Via Pymoo Termination Composition

Pymoo termination criteria can be composed [Pymoo-Termination-Docs]. The standard pattern is:

```python
from pymoo.termination.collection import TerminationCollection
from pymoo.termination.max_gen import MaximumGenerationTermination
from pymoo.termination.robust import RobustTermination
from pymoo.indicators.hv import HV

termination = TerminationCollection(
    MaximumGenerationTermination(n_max_gen=8),
    HVPlateauTermination(window=2, tol=0.01),  # custom 1% HV growth check
    CostWatchdogTermination(max_cost_usd=4.00),  # custom callable wrapping cost log
)
```

The `CostWatchdogTermination` is a custom subclass of `pymoo.core.termination.Termination` that
queries the cumulative cost log after each generation and returns `True` (terminate) when the
running spend exceeds the threshold. This is the same pattern documented for compound stopping
criteria in [Lopez-Camacho-2022] and routinely used for budget-constrained surrogate-assisted MOEA
in expensive simulation problems [Tabatabaei-2017-Survey, MOTA-2008].

**Best practice**: Implement `CostWatchdogTermination` as a thin wrapper around the project's
existing cost log (`tasks/t0091_morphology_extended_nsga2_v1/results/costs.json`); evaluate after
each NSGA-II generation, not per-cell, to avoid mid-generation truncation of the population (which
would corrupt the Pareto front).

### Riccitelli 2025 PNAS: Direction Selectivity Beyond The Classical Receptive Field

**Riccitelli, Ankri, Cohen-Kashi-Malina, Rivlin-Etzion (2025)** published in PNAS Vol 122 Issue 1
the discovery that a subset of *non-DS* RGCs in mouse retina exhibit **asymmetric activity selective
to motion direction in response to stimuli crossing an area far beyond the classical receptive
field** [Riccitelli2025]. Mechanistic findings:

* The extraclassical DS response arises from inputs from an **asymmetric distal zone**.
* It is **enhanced by desensitisation mechanisms and an inherent DS component**, creating a network
  of neurons preferring motion toward the optic disc.
* Pharmacological manipulations reveal **glycinergic amacrine cells are necessary** for this
  response (a new amacrine class beyond the cholinergic + GABAergic SAC story dominant in the
  classical-RF DS literature).
* In-vivo LGN recordings show similar extraclassical DS responses, indicating downstream relevance.

**Update to research_papers.md**: This finding *does not contradict* the project's classical-RF DS
mechanism (SAC asymmetric wiring + dendritic spike threshold). It adds a *second, parallel* DS
mechanism operating outside the classical RF that is mediated by glycinergic rather than GABAergic
inhibition. **For t0091's interpretation framework, this means the biological-plausibility
scorecard's GABA-spatial-gradient prior is specifically about classical-RF SAC-mediated inhibition;
glycinergic-mediated extraclassical DS is a separate axis t0091 does not score against**.

### Ankri 2024 J Physiol: Excitation Gains A New Role In Retinal DS

**Ankri, Riccitelli, Rivlin-Etzion (2024)** published in J Physiol [Ankri2024JPhysiol] the finding
that under light adaptation, the surround of posterior-preferring On-Off DSGCs (pDSGCs) expands
substantially, and **both centre-mediated and surround-mediated responses originate from
directionally tuned excitatory inputs** rather than the classical inhibition-dominated mechanism.
Specifically:

* The pDSGC maintains its preferred-direction tuning in the *centre* RF.
* In the *surround* RF (light-adaptation-expanded), the response is tuned to the **opposite**
  direction.
* The excitation carries an *antagonistic centre-surround* property.
* This is "a new role for excitation in the direction-selective circuit", per the title.

**Implication for t0091**: The traditional inhibition-dominated DS picture
(`[PolegPolsky2016, Schachter2010]`) is correct under standard photopic stimulation; the
surround-direction-flipping excitation under light-adaptation is a separate regime. **t0091's
stimulation protocol uses standard photopic 16-direction bar rotation, so the Ankri 2024 finding
does not directly affect the 68-d search**, but it does inform the answer asset's discussion of
biological-plausibility ceilings: a Pareto cell that achieves joint-pass under a single fixed
stimulus regime represents only one operating point on the DSGC's adaptive repertoire.

### Roy Et Al. 2024 J Neurosci: GABA Sensitivity And RF Size Of S-DSGC At Threshold

**Roy, Yao, Rathinavelu, Field (2024)** in J Neurosci [Roy2024JNeurosci] showed that under scotopic
conditions, **superior-preferring DSGCs (s-DSGCs) are 10-fold more sensitive to dim flashes** than
other ooDSGCs and have larger receptive fields, but this size difference does not fully explain
sensitivity. **GABA-mediated inhibition contributes to the difference in absolute sensitivity and RF
size at low light levels; connexin36 gap junction coupling plays only a minor role**. Key numbers:

* s-DSGCs: ~10x higher absolute light sensitivity vs other ooDSGCs.
* Removing GABA inhibition unmasks an OFF response under scotopic conditions (ON-only response is
  lost).

**Implication for t0091**: This update *does not* change the per-spine NMDA prior (~0.1 nS, from
Sivyer 2013 and Sethuramanujam 2017) or the GABA spatial-gradient prior (from Poleg-Polsky 2016);
the Roy 2024 finding is about *sensitivity* (response threshold) and *receptive field size*, not
channel density. The GABA spatial-gradient prior in t0086 / t0088's scorecard remains canonical.

### Persistent Sodium NaP Updates: 2024 Review Confirms Current DSGC Priors

The **Muller, Draguhn, Egorov 2024** Pflugers Archiv review [MullerEgorov2024] systematises NaP
mechanisms across the CNS but does not provide DSGC-specific updates. Key takeaways relevant to
t0091:

* No direct DSGC dendritic-NaP density measurement is published. The Stuart-style cortical-pyramidal
  prior (sub-1% of Nav at distal sites) remains the best available baseline.
* A 2021 J Neurosci study on cortical pyramidal AIS NaP found "AIS NaP density is approximately
  **twofold lower than in the soma**" [Astman-2021], complicating the picture of where peak NaP
  sits.
* Slow-depolarisation voltage-ramp measurements may *underestimate* NaP because of slow inactivation
  [MullerEgorov2024]. This is a methodological caution not affecting the model.

**Conclusion for t0091**: The biological-plausibility scorecard's NaP prior does not need to be
revised based on these 2024 publications. The +9 to +34 sigma exotic-ness of v3 substrate distal NaP
remains relative to the Stuart 1999 / cortical pyramidal prior.

## Methodology Insights

* **Use `MixedVariableGA` with `RankAndCrowdingSurvival`, not real-with-rounding**, for the 14-d
  morphology integer parameters. The `MixedVariableGA` defines per-type operators
  (`SimulatedBinaryCrossover` for reals, custom integer crossover for integers) that respect
  variable types throughout the GA cycle [Pymoo-Mixed-Docs, Pymoo-NSGA2-Docs].

* **Pass the 5-anchor warm-start as a 2-D numpy array via `sampling=`** [Pymoo-Initialization-Docs].
  pymoo accepts `(n_individuals, n_var)`-shaped arrays directly. The full warm-start array (95 cells
  + 1 random sample) can be precomputed in Phase A and passed to
    `NSGA2(sampling=warm_start_array, ...)`. **CAUTION (from Pymoo-NSGA2-Docs)**: per the original
    NSGA-II paper, the elitism of the initial population is not preserved — good initial solutions
    will be subjected to ranking and crowding-distance selection, so dominated warm-start cells may
    be filtered out in gen 1. Frontload the warm-start with cells that are *known* to dominate
    random samples.

* **Mutation distribution index `eta_m=20` is correct for d=68**. Lopez-Camacho-2022's auto-config
  benchmark suggests `eta_m=20` is near-optimal for moderate-d problems; lowering `eta_m` to 10-15
  may help if HV growth stalls at gen 4-5, but should not be the first attempted intervention.

* **Compose termination**:
  `TerminationCollection(MaximumGenerationTermination(8), HVPlateauTermination(window=2, tol=0.01), CostWatchdogTermination(max_cost_usd=4.00))`.
  Evaluate the cost watchdog after each generation, not per-cell, to avoid mid-generation Pareto
  corruption.

* **Compute the v_opt = 2 * lambda / tau_m for every Pareto cell** as Phase D sanity check
  [research_papers.md, Anderson1999]. The cable-theoretic preferred velocity should land in the 100
  - 1000 um/s range (consistent with the Trenholm 2013 600 um/s preferred bar velocity); cells whose
    v_opt is far outside this band should be flagged as "DSI-by-cable-mismatch" exotic.

* **Best practice for cost monitoring**: log cumulative spend after every generation in
  `tasks/t0091_morphology_extended_nsga2_v1/results/costs.json` with timestamps; the
  `CostWatchdogTermination` reads this file (not in-memory state) so termination state is
  recoverable from disk on restart. This matches the `MOTA-2008` pattern of reproducible
  budget-aware MOEA logging.

* **Hypothesis (HM-5)**: Per [Doerr-2024-arXiv]'s finding that smaller offspring populations
  outperform default NSGA-II in 92 percent of cases, the project should consider testing
  `n_offsprings = 48` (half of `pop_size = 96`) in a follow-up if HV converges adequately by gen 6
  in t0091 — this would extend the effective generation budget at the same wall-clock cost.

* **Avoid NSGA-III**: NSGA-III is for *many-objective* (k > 3) problems. t0091's 3 objectives sit
  squarely in NSGA-II's design regime [Lopez-Camacho-2022, Pymoo-NSGA3-Docs].

## Discovered Papers

The following 4 papers were not found in the existing project corpus (75 papers as of 2026-05-08)
and are relevant to t0091 or the project's broader DS / DSGC research:

### [Riccitelli2025]

* **Title**: Retinal ganglion cells encode the direction of motion outside their classical receptive
  field
* **Authors**: Riccitelli, S., Ankri, L., Cohen-Kashi-Malina, K., Rivlin-Etzion, M.
* **Year**: 2025 (published December 30, 2024)
* **DOI**: `10.1073/pnas.2415223122`
* **URL**: https://www.pnas.org/doi/10.1073/pnas.2415223122
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: First peer-reviewed report of glycinergic-mediated DS *outside* the classical
  RF, in non-DS RGCs. Adds a parallel DS mechanism beyond classical SAC-DSGC inhibition. Directly
  expands the biological-plausibility framing for t0091 by clarifying that the GABA spatial-gradient
  prior applies to classical-RF DS only.

### [Ankri2024JPhysiol]

* **Title**: A new role for excitation in the retinal direction-selective circuit
* **Authors**: Ankri, L., Riccitelli, S., Rivlin-Etzion, M.
* **Year**: 2024
* **DOI**: `10.1113/JP286581`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/10.1113/JP286581
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: Documents a regime (light-adapted) where DSGC tuning *flips* in the surround,
  driven by directionally tuned *excitation* rather than the classical inhibition mechanism. A
  cautionary update to the inhibition-dominated DS picture; relevant to interpreting t0091's
  Pareto-front cells under photopic stimulation as a single operating point.

### [Roy2024JNeurosci]

* **Title**: GABAergic Inhibition Controls Receptive Field Size, Sensitivity, and Contrast
  Preference of Direction Selective Retinal Ganglion Cells Near the Threshold of Vision
* **Authors**: Roy, S., Yao, X., Rathinavelu, J., Field, G. D.
* **Year**: 2024
* **DOI**: `10.1523/JNEUROSCI.1979-23.2023`
* **URL**: https://www.jneurosci.org/content/44/11/e1979232023
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: Quantifies absolute sensitivity differences (s-DSGCs ~10x more sensitive) and
  receptive-field-size effects of GABAergic inhibition under scotopic conditions. Relevant context
  for interpreting Pareto-cell firing rates at low-stimulus conditions; supplements the Trenholm
  2013 photopic peak-rate prior.

### [MullerEgorov2024]

* **Title**: Persistent sodium currents in neurons: potential mechanisms and pharmacological
  blockers
* **Authors**: Muller, P., Draguhn, A., Egorov, A. V.
* **Year**: 2024
* **DOI**: `10.1007/s00424-024-02980-7`
* **URL**: https://link.springer.com/article/10.1007/s00424-024-02980-7
* **Suggested categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Why download**: 2024 systematic review of CNS NaP mechanisms with attention to measurement
  pitfalls (slow-ramp inactivation underestimating INaP). Relevant for the biological-plausibility
  scorecard's distal NaP prior; confirms that no DSGC-specific NaP density measurement exists,
  validating the cortical-pyramidal-based prior used in t0086 / t0088.

## Recommendations for This Task

1. **Use `MixedVariableGA` with explicit `Integer()` and `Real()` types for the 68-d problem**. This
   updates the t0091 plan, which currently mentions "mixed integer-real handling" without a concrete
   API choice. The pattern is `MixedVariableGA(pop_size=96, survival=RankAndCrowdingSurvival())` per
   [Pymoo-Mixed-Docs]. **Priority: HIGH; affects Phase B directly.**

2. **Pass the 5-anchor warm-start as a 2D numpy array via `sampling=` to `NSGA2()`** per
   [Pymoo-Initialization-Docs]. Frontload with cells known to dominate random samples to avoid
   first-generation elitism loss. **Priority: HIGH; affects Phase A and Phase B handoff.**

3. **Implement the cost watchdog as a `TerminationCollection` member** combining 8-gen cap,
   HV-plateau (window=2, tol=0.01), and `CostWatchdogTermination` reading the project cost log.
   Evaluate after each generation, not per-cell. **Priority: HIGH; affects Phase B safety.**

4. **Do NOT switch to NSGA-III for t0091**. With 3 objectives, NSGA-II is the design-target
   algorithm; NSGA-III is for many-objective (k > 3) problems [Lopez-Camacho-2022]. **Priority:
   informational; reaffirms existing plan.**

5. **Add Riccitelli2025 and Ankri2024JPhysiol to the corpus before t0091 reporting** so the answer
   asset can frame the v3 substrate's biological-plausibility ceiling against both the classical-RF
   and the recently-discovered extraclassical/surround DS regimes. **Priority: MEDIUM; affects Phase
   E framing only.**

6. **In Phase E discussion, explicitly note that the GABA spatial-gradient prior applies to
   classical-RF SAC-mediated DS only**. The Riccitelli2025 glycinergic-mediated extraclassical DS
   pathway is a separate axis the scorecard does not score against. This avoids overclaiming
   biological plausibility (or implausibility) on a prior that is mechanism-specific. **Priority:
   MEDIUM; affects Phase E framing.**

7. **Keep the existing distal NaP prior (Stuart 1999 cortical pyramidal baseline)** for the
   scorecard. The 2024 review [MullerEgorov2024] confirms no DSGC-specific NaP measurement exists;
   the cortical-pyramidal cross-cell prior remains the best baseline. **Priority: LOW; reaffirms
   existing plan.**

8. **If HV growth stalls at gen 4-5 below the 1 percent threshold, drop `eta_m` from 20 to 12-15**
   per [Lopez-Camacho-2022]'s auto-config findings, before considering algorithm change. Document
   this fallback explicitly in the plan. **Priority: LOW; conditional fallback only.**

## Tool and Library Landscape

* **pymoo** [Pymoo-NSGA2-Docs, Pymoo-Mixed-Docs, Pymoo-Initialization-Docs, Pymoo-Termination-Docs]
  — current version 0.6.1.6, actively maintained as of 2024-2025. Provides `NSGA2`,
  `MixedVariableGA`, `RankAndCrowdingSurvival`, `TerminationCollection`, `Sampling`, `Population`.
  The right toolkit for t0091.
* **BluePyOpt** [BluePyOpt-2016] — Blue Brain's evolutionary optimisation framework for neural
  models. Supports CMA-ES, NSGA-II via DEAP, parallel evaluation. **Note**: as of December 2024 the
  Blue Brain Project concluded; future development moves to `openbraininstitute/BluePyOpt`. Mature
  and widely cited (Hay 2011-style optimisations) but heavier than pymoo for direct embedding in a
  custom evaluation loop.
* **DEAP** — pymoo's older Python competitor; more flexible but less mature documentation. Not the
  best choice when pymoo offers the same algorithms with better APIs.
* **TREES toolbox** (Cuntz 2010, already in corpus) — MATLAB plugin for procedural-morphology
  generation; the academic ancestor of t0090's procedural generator. Out of scope for direct use
  (Python project) but useful cross-reference.
* **NETMORPH** [NETMORPH-2009] — C++/MATLAB stochastic-growth simulator for large neural networks.
  Heavier than t0090's procedural generator and oriented toward developmental simulation rather than
  parameterised generation. Not appropriate for embedding in an NSGA-II eval loop.
* **NeuGen** [NeuGen-2006] — older procedural-morphology generator for cortex. Not
  retinal-specific and not actively maintained.

The conclusion is that pymoo + the project's t0092 patched generator + a custom Python eval loop is
the right stack; no migration to BluePyOpt or other frameworks is warranted.

## Implementation Patterns

The pseudocode below summarises the t0091 NSGA-II setup based on
[Pymoo-Mixed-Docs, Pymoo-Initialization-Docs, Pymoo-Termination-Docs]:

```python
from pymoo.algorithms.moo.nsga2 import NSGA2, RankAndCrowdingSurvival
from pymoo.core.mixed import MixedVariableGA
from pymoo.core.variable import Real, Integer
from pymoo.optimize import minimize
from pymoo.termination.collection import TerminationCollection
from pymoo.termination.max_gen import MaximumGenerationTermination

# variable specification: 68 = 12 morph reals + 2 morph ints + 54 electrophys reals
vars_dict = {
    "soma_offset_pd_um": Real(bounds=(-150.0, 150.0)),
    # ... 11 other morph reals ...
    "num_primary_branches": Integer(bounds=(3, 8)),
    "max_strahler_depth": Integer(bounds=(2, 6)),
    "gnap_dend_distal": Real(bounds=(...)),
    # ... 53 other electrophys reals ...
}

# warm-start: 95 anchor cells + 1 random sample, packed as numpy array
warm_start_array = build_5_anchor_warmstart(...)  # shape (96, 68)

algorithm = MixedVariableGA(
    pop_size=96,
    sampling=warm_start_array,
    survival=RankAndCrowdingSurvival(),
    eliminate_duplicates=True,
)

termination = TerminationCollection(
    MaximumGenerationTermination(n_max_gen=8),
    HVPlateauTermination(window=2, tol=0.01),  # custom
    CostWatchdogTermination(max_cost_usd=4.00),  # custom
)

result = minimize(problem, algorithm, termination, seed=42, verbose=True)
```

The `HVPlateauTermination` and `CostWatchdogTermination` are project-specific subclasses of
`pymoo.core.termination.Termination` evaluated post-generation. The `HVPlateauTermination` reads the
last `window` HV values from `result.history` and returns `True` when
`(HV[-1] - HV[-window]) / HV[-window] < tol`. The `CostWatchdogTermination` reads the cumulative
cost from `tasks/t0091_morphology_extended_nsga2_v1/results/costs.json` and returns `True` when
cumulative > threshold.

## Source Index

### [Pymoo-Mixed-Docs]

* **Type**: documentation
* **Title**: Mixed Variable Problem - pymoo: Multi-objective Optimization in Python 0.6.1.6
* **Author/Org**: Blank, J. and the pymoo team
* **Date**: 2024 (current docs version 0.6.1.6)
* **URL**: https://pymoo.org/customization/mixed.html
* **Peer-reviewed**: no
* **Relevance**: Authoritative reference for `MixedVariableGA` API, the right pattern for t0091's
  68-d mixed integer-real problem. Provides `Integer(bounds=...)` and `Real(bounds=...)` syntax,
  recommended pop sizes for mixed problems, and the `MixedVariableGA + RankAndCrowdingSurvival`
  pattern for multi-objective optimisation.

### [Pymoo-NSGA2-Docs]

* **Type**: documentation
* **Title**: NSGA-II: Non-dominated Sorting Genetic Algorithm - pymoo 0.6.1.6
* **Author/Org**: Blank, J. and the pymoo team
* **Date**: 2024
* **URL**: https://pymoo.org/algorithms/moo/nsga2.html
* **Peer-reviewed**: no (companion to peer-reviewed pymoo paper)
* **Relevance**: Canonical reference for the NSGA-II implementation in pymoo: SBX crossover,
  polynomial mutation, RankAndCrowdingSurvival selection, and the warning that elitism of the
  initial population is *not* preserved (so warm-start cells go through gen-1 selection).

### [Pymoo-Initialization-Docs]

* **Type**: documentation
* **Title**: Biased Initialization - pymoo 0.6.1.6
* **Author/Org**: Blank, J. and the pymoo team
* **Date**: 2024
* **URL**: https://pymoo.org/customization/initialization.html
* **Peer-reviewed**: no
* **Relevance**: Documents the three options for warm-starting NSGA-II: custom `Sampling`,
  pre-evaluated `Population`, or 2-D numpy array. The numpy-array pattern is the simplest for
  t0091's 5-anchor warm-start.

### [Pymoo-Termination-Docs]

* **Type**: documentation
* **Title**: Termination Criterion - pymoo 0.6.1.6
* **Author/Org**: Blank, J. and the pymoo team
* **Date**: 2024
* **URL**: https://pymoo.org/interface/termination.html
* **Peer-reviewed**: no
* **Relevance**: Documents `TerminationCollection`, `MaximumGenerationTermination`, and the pattern
  for custom termination subclasses. The right mechanism for the cost-watchdog + HV-plateau + 8-gen
  composite termination t0091 needs.

### [Pymoo-NSGA3-Docs]

* **Type**: documentation
* **Title**: NSGA-III - pymoo 0.6.1.6
* **Author/Org**: Blank, J. and the pymoo team
* **Date**: 2024
* **URL**: https://pymoo.org/algorithms/moo/nsga3.html
* **Peer-reviewed**: no
* **Relevance**: Confirms NSGA-III is for many-objective (k > 3) problems; t0091's 3-objective setup
  correctly uses NSGA-II.

### [Pymoo-Issue-126]

* **Type**: forum
* **Title**: NSGA2 with mixed variable problem (Issue #126)
* **Author/Org**: anyoptimization/pymoo GitHub
* **Date**: 2020 (closed); pattern still current as of 2024-2025
* **URL**: https://github.com/anyoptimization/pymoo/issues/126
* **Peer-reviewed**: no
* **Relevance**: Forum-confirmed pattern for combining `MixedVariableGA` survival selection with
  NSGA-II RankAndCrowdingSurvival. Cited by the pymoo team as the canonical mixed-variable +
  multi-objective recipe.

### [Lopez-Camacho-2022]

* **Type**: paper
* **Title**: Is NSGA-II Ready for Large-Scale Multi-Objective Optimization?
* **Authors**: Lopez-Camacho, E., Garcia-Godoy, M. J., Garcia-Nieto, J., Nebro, A. J.,
  Aldana-Montes, J. F.
* **Year**: 2022
* **DOI**: `10.3390/mca27060103`
* **URL**: https://www.mdpi.com/2297-8747/27/6/103
* **Peer-reviewed**: yes (Mathematical and Computational Applications, MDPI)
* **Relevance**: Benchmarks NSGA-II on ZDT1/ZDT2 up to `n_var=131,072` with auto-configuration; key
  finding is that with proper tuning, NSGA-II handles very high dimensionality. Direct precedent for
  t0091's choice to stay on NSGA-II at d=68 rather than switch to NSGA-III or BO methods.

### [Doerr-2024-arXiv]

* **Type**: paper
* **Title**: Speeding Up the NSGA-II via Dynamic Population Sizes
* **Authors**: Doerr, B., et al.
* **Year**: 2024 (arXiv preprint)
* **URL**: https://arxiv.org/html/2509.01739v1
* **Peer-reviewed**: no (arXiv preprint, not yet peer-reviewed)
* **Relevance**: Reports that smaller offspring populations + more generations beat default NSGA-II
  in 92 percent of experiments. Suggests a follow-up tuning lever for t0091 if HV converges at gen 6
  with budget remaining.

### [Riccitelli2025]

* **Type**: paper
* **Title**: Retinal ganglion cells encode the direction of motion outside their classical receptive
  field
* **Authors**: Riccitelli, S., Ankri, L., Cohen-Kashi-Malina, K., Rivlin-Etzion, M.
* **Year**: 2025 (published December 30, 2024)
* **DOI**: `10.1073/pnas.2415223122`
* **URL**: https://www.pnas.org/doi/10.1073/pnas.2415223122
* **Peer-reviewed**: yes (PNAS)
* **Relevance**: Documents glycinergic-mediated extraclassical-RF DS in non-DS RGCs. Adds a parallel
  DS mechanism beyond the classical-RF SAC-mediated story. Used here to clarify that t0091's GABA
  spatial-gradient prior applies to classical-RF DS only.

### [Ankri2024JPhysiol]

* **Type**: paper
* **Title**: A new role for excitation in the retinal direction-selective circuit
* **Authors**: Ankri, L., Riccitelli, S., Rivlin-Etzion, M.
* **Year**: 2024
* **DOI**: `10.1113/JP286581`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/10.1113/JP286581
* **Peer-reviewed**: yes (Journal of Physiology)
* **Relevance**: Documents directionally-tuned excitation in light-adapted DSGC surround tuning
  opposite-to-centre. Cautionary update to the inhibition-dominated DS picture relevant to t0091's
  Phase E framing.

### [Roy2024JNeurosci]

* **Type**: paper
* **Title**: GABAergic Inhibition Controls Receptive Field Size, Sensitivity, and Contrast
  Preference of Direction Selective Retinal Ganglion Cells Near the Threshold of Vision
* **Authors**: Roy, S., Yao, X., Rathinavelu, J., Field, G. D.
* **Year**: 2024
* **DOI**: `10.1523/JNEUROSCI.1979-23.2023`
* **URL**: https://www.jneurosci.org/content/44/11/e1979232023
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Quantifies scotopic-condition GABA-mediated sensitivity differences (~10x for
  s-DSGC vs other ooDSGCs). Adds context to firing-rate priors but does not change the photopic
  per-spine NMDA / per-section NaP / GABA spatial-gradient priors used in t0086 / t0088 scorecard.

### [MullerEgorov2024]

* **Type**: paper
* **Title**: Persistent sodium currents in neurons: potential mechanisms and pharmacological
  blockers
* **Authors**: Muller, P., Draguhn, A., Egorov, A. V.
* **Year**: 2024
* **DOI**: `10.1007/s00424-024-02980-7`
* **URL**: https://link.springer.com/article/10.1007/s00424-024-02980-7
* **Peer-reviewed**: yes (Pflugers Archiv - European Journal of Physiology)
* **Relevance**: 2024 systematic review of NaP mechanisms; confirms no DSGC-specific NaP density
  measurement is available, validating the cortical-pyramidal-based prior used in the t0086 / t0088
  biological-plausibility scorecard.

### [Astman-2021]

* **Type**: paper
* **Title**: Subcellular Distribution of Persistent Sodium Conductance in Cortical Pyramidal Neurons
* **Authors**: Astman, N., Gutnick, M. J., Fleidervish, I. A.
* **Year**: 2021 (cited via [MullerEgorov2024] for t0091 context, not added to corpus)
* **URL**: https://www.jneurosci.org/content/41/29/6190
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Reports that AIS NaP density is approximately twofold lower than soma in cortical
  pyramidal cells, a useful cross-cell calibration check for the t0091 scorecard but not requiring
  an immediate scorecard update.

### [BluePyOpt-2016]

* **Type**: paper
* **Title**: BluePyOpt: Leveraging Open Source Software and Cloud Infrastructure to Optimise Model
  Parameters in Neuroscience
* **Authors**: Van Geit, W., Gevaert, M., Chindemi, G., Roessert, C., et al.
* **Year**: 2016
* **DOI**: `10.3389/fninf.2016.00017`
* **URL**:
  https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2016.00017/full
* **Peer-reviewed**: yes (Frontiers in Neuroinformatics)
* **Relevance**: Establishes BluePyOpt as the mature Python optimisation framework for neural
  compartmental models. t0091 stays with pymoo for direct evaluation-loop control; BluePyOpt is
  cross-referenced here for scope justification.

### [NETMORPH-2009]

* **Type**: paper
* **Title**: NETMORPH: A Framework for the Stochastic Generation of Large Scale Neuronal Networks
  With Realistic Neuron Morphologies
* **Authors**: Koene, R. A., Tijms, B., van Hees, P., Postma, F., et al.
* **Year**: 2009
* **DOI**: `10.1007/s12021-009-9052-3`
* **URL**: https://link.springer.com/article/10.1007/s12021-009-9052-3
* **Peer-reviewed**: yes (Neuroinformatics)
* **Relevance**: Alternative procedural-morphology generator framework. Cited here to explain why
  t0091 uses the project's own t0092-patched generator (Cuntz-style) rather than NETMORPH (which
  models developmental growth, not parameterised generation suitable for an NSGA-II eval loop).

### [NeuGen-2006]

* **Type**: paper
* **Title**: NeuGen: A tool for the generation of realistic morphology of cortical neurons and
  neural networks in 3D
* **Authors**: Eberhard, J. P., Wanner, A., Wittum, G.
* **Year**: 2006
* **DOI**: `10.1016/j.neucom.2006.03.007`
* **URL**: https://www.sciencedirect.com/science/article/abs/pii/S0925231206001135
* **Peer-reviewed**: yes (Neurocomputing)
* **Relevance**: Older cortical procedural-morphology generator. Not retinal-specific; cited for
  scope justification.

### [Tabatabaei-2017-Survey]

* **Type**: paper
* **Title**: A survey on handling computationally expensive multiobjective optimization problems
  with evolutionary algorithms
* **Authors**: Tabatabaei, M., Hakanen, J., Hartikainen, M., Miettinen, K., Sindhya, K.
* **Year**: 2017
* **DOI**: `10.1007/s00500-017-2965-0`
* **URL**: https://link.springer.com/article/10.1007/s00500-017-2965-0
* **Peer-reviewed**: yes (Soft Computing)
* **Relevance**: Survey of evaluation-budget-aware MOEA approaches. Establishes that wrapping
  expensive evaluation calls with cumulative-cost monitoring is the standard pattern for
  computationally expensive multi-objective problems.

### [MOTA-2008]

* **Type**: paper
* **Title**: Multiobjective Optimization on a Budget of 250 Evaluations
* **Authors**: Knowles, J., Hughes, E. J.
* **Year**: 2005 (Springer chapter, conference proceedings reference often listed as 2008 reprint)
* **DOI**: `10.1007/978-3-540-31880-4_13`
* **URL**: https://link.springer.com/chapter/10.1007/978-3-540-31880-4_13
* **Peer-reviewed**: yes (EMO 2005 Springer chapter)
* **Relevance**: Foundational paper on MOEA with strict evaluation budgets. Establishes the
  cost-monitoring + early-termination pattern for budget-constrained multi-objective problems.
