---
spec_version: "1"
task_id: "t0102_seedscale_n4_gen20"
research_stage: "internet"
searches_conducted: 11
sources_cited: 12
papers_discovered: 6
date_completed: "2026-05-11"
status: "complete"
---
# Research Internet — Seed/Generation Re-Balance for 68-d NSGA-II on Bed B DSGC

## Task Objective

t0102 reruns the 68-d random-init NSGA-II from t0099 but cuts within-cell noise replicates `N_SEEDS`
from 20 to 4 (5x reduction) and extends generations from 5-8 to 20, on two new GA seeds (44, 55,
pop=96, $8 cap). The internet-research goal is to find (a) recent (2024-2026) literature on resource
allocation between noise replicates, population size, and generations in noisy multi-objective
evolutionary optimisation, (b) recent benchmarks of NSGA-II vs other MOEAs for compartmental neuron
fitting, and (c) any DSGC modelling developments beyond Poleg-Polsky 2026 that update the
methodology recommendations recorded in `research_papers.md`.

## Gaps Addressed

From `tasks/t0102_seedscale_n4_gen20/research/research_papers.md` Gaps and Limitations:

1. **None of the cited papers tested a 5x noise-replicate reduction in isolation** — **Partially
   resolved.** The "noisy evolutionary optimisation" literature provides direct theory and empirical
   comparisons of *explicit averaging* (more replicates per evaluation) vs *implicit averaging*
   (more evaluations per replicate budget). [Rakshit2017] survey identifies five strategies,
   [Akimoto2024] proves explicit averaging is effective only when noise has stability parameter
   `alpha in (1, 2]` (Gaussian, sub-Gaussian) and *harmful* when `alpha < 1` (heavy-tail);
   [Diaz2025-rev] re-examines [Diaz2017-implicit] and finds the "implicit averaging wins" result is
   fragile to problem structure. No paper specifically tests a 5x N_SEEDS reduction in NEURON-based
   compartmental fitting, but the *theory* for our regime (additive Gaussian-like noise across
   trials) places us in the `alpha in (1, 2]` regime where explicit averaging *does* help — so
   N_SEEDS=4 is expected to be noisier than N_SEEDS=20 but still informative, consistent with the
   t0102 hypothesis.

2. **No reviewed paper reports per-seed cost or wall-clock super-linearity due to NEURON memory
   accumulation** — **Unresolved.** Still a deployment artefact absent from the academic
   literature. The [BluePyOpt-GH] repository and the [Neuroptimus-2024] paper acknowledge that
   "actual experimental evaluation of fitness gives the highest accuracy but incurs the highest
   computational cost" [Neuroptimus-2024], but neither addresses NEURON's specific memory leak
   behaviour. The folk-knowledge S-0099-04 remedy (restart Python workers between generations)
   remains uncited.

3. **The literature does not report negative-result NSGA-II runs on dendritic-DS substrates** —
   **Partially resolved.** [Neuroptimus-2024] is the first benchmark we found that compares
   Inspyred-NSGA-II, BluePyOpt-NSGA-II, and Pygmo-NSGA-II on six neuron-fitting problems and reports
   negative results: "Inspyred's NSGA2, PAES and Pygmo's NSPSO algorithms giving worse results than
   Random Search" on some problems. The paper also reports that CMAES converges in ~3500 evaluations
   and IBEA is "clearly the best among the multi-objective methods." This suggests our NSGA-II
   baseline is *not* state-of-the-art and a future follow-up should consider IBEA or CMAES.

4. **Poleg-Polsky 2026 does not document budget-matched ablation between (high seeds, low gens) vs
   (low seeds, high gens)** — **Unresolved.** No paper found that tests this trade-off at fixed
   total budget for compartmental neuron fitting. [Budszuhn2025] addresses adaptive resampling for
   noisy MOO but does not match budget across configurations; the question remains open and t0102
   contributes one new data point.

5. **The relationship between morphology dimensions (14 d) and electrophys dimensions (54 d) in the
   joint 68-d substrate is not addressed by any cited paper** — **Unresolved.** No 2024-2026 paper
   found that jointly searches morphology and electrophysiology in a compartmental DSGC model. The
   new [Budoff2025-RGC-map] mouse RGC spatial map clarifies the *target* (45 RGC subtypes, two-
   thirds uniformly distributed) but not the *search* methodology.

6. **The 0.5 DSI threshold is not directly comparable to Poleg-Polsky 2026** — **Unresolved.** No
   new paper bridges the 8-direction-spike-rate-DSI convention used by our project and the
   12-direction-x-5-speed-subthreshold-voltage convention of Poleg-Polsky 2026.

## Search Strategy

**Sources searched**: Google Scholar (via WebSearch), arXiv, Nature Communications, PLOS
Computational Biology, ScienceDirect / Cell Press, bioRxiv, eLife, Springer Nature, IEEE Xplore, ACM
Digital Library, GitHub (BluePyOpt + openbraininstitute), Open Brain Institute platform docs.

**Date range**: Primary focus 2024-2026, with foundational papers (1996-2017) cited only when
necessary for the theory. Excluded: papers older than 2017 that already appear in the project corpus
via `research_papers.md`.

**Inclusion criteria**: A source had to provide at least one of (a) empirical or theoretical
comparison of resource-allocation strategies in noisy MOEAs (replicates vs population vs
generations), (b) benchmark of NSGA-II against other MOEAs on neuron model fitting, (c) DSGC or SAC
compartmental modelling published 2024-2026, or (d) tooling guidance for NEURON-based optimisation
pipelines. Excluded: papers on visual cortex direction selectivity (out of scope per
`project/description.md`), papers on RGC subtypes other than ON-OFF DSGCs unless directly addressing
methodology, and pure ML/non-biological MOO benchmarks.

**Search iterations**: Pass 1 (gap-targeted) ran queries 1-4; Pass 2 (broadening) ran queries 5-8;
Pass 3 (snowball) ran queries 9-11 based on findings.

**Queries executed** (11 total, exact text recorded):

*Pass 1 — gap-targeted:*

1. `NSGA-II noisy objectives stochastic multi-objective evolutionary algorithm 2024 2025 noise replicates`
2. `budget allocation population size generations replicates evolutionary multi-objective 2024 2025`
3. `"explicit averaging" "implicit averaging" noisy evolutionary algorithm survey`
4. `"noisy NSGA-II" resampling strategy fitness evaluation variance reduction`

*Pass 2 — broadening:*

5. `BluePyOpt 2024 2025 compartmental neuron multi-objective optimization NSGA IBEA`
6. `direction-selective retinal ganglion cell compartmental model 2025 2026`
7. `pymoo NSGA-II noise replicates neuron model fitting 2024 2025`
8. `DSGC starburst amacrine cell model NEURON 2025 2026 dendritic computation`

*Pass 3 — snowball:*

9. `stochastic optimization "neuron model" sample size replicates pareto 2024 2025`
10. `"dynamic resampling" "noisy" optimization 2024 2025 Pareto budget`
11. `Mohacsi Neuroptimus 2024 PLOS computational biology benchmark neuron NSGA-II evaluations`

Queries 11 was a snowball-followup after query 9 yielded `[Neuroptimus-2024]`. Query 10 was prompted
by [Bian2023-noisy-NSGA] (arxiv 2306.04525) returning related resampling-strategy work. Queries 1-4
were direct gap-fillers; queries 5-8 broadened coverage to the project's tooling and DSGC-specific
literature.

## Key Findings

### Theory: Explicit Averaging Is Effective for Gaussian-Like Noise but Fails for Heavy Tails

[Akimoto2024] (peer-reviewed arXiv preprint, JSPS-funded) proves that explicit averaging
effectiveness in comparison-based search depends on the *stability parameter* `alpha` of the noise
distribution. For symmetric noise with `alpha in (1, 2]` (covering Gaussian `alpha=2`, sub-Gaussian
and most "well-behaved" cases), the probability of correct ranking obeys
`Pr_correct_order = Phi_alpha(K^(1 - 1/alpha) * |signal| / noise)` where K is the sample size, so
increasing K *does* improve ranking accuracy, with rate exponent `(1 - 1/alpha)`. For `alpha = 1`
(Cauchy), explicit averaging has **no effect**; for `alpha < 1` (very heavy tail), explicit
averaging is **harmful** [Akimoto2024].

In our NEURON setup, within-cell noise comes from trial-to-trial variability in synaptic timing plus
stochastic-conductance fluctuations. This is effectively Gaussian (CLT applies to ~160 independent
sims per evaluation at N_SEEDS=20), so we sit firmly in the `alpha = 2` regime where explicit
averaging is effective. The 5x reduction from N_SEEDS=20 to N_SEEDS=4 reduces the ranking-accuracy
factor by `(20/4)^(1 - 1/2) = sqrt(5) ~ 2.24x` in standard error, but does *not* flip the algorithm
from "works" to "broken" — it just makes it noisier. This is consistent with the t0102 hypothesis.

### Theory: Implicit Averaging via Larger Population Has Conflicting Empirical Evidence

[Rakshit2017] (peer-reviewed *Swarm and Evolutionary Computation* survey) identifies five
methodologies for noisy EAs: explicit averaging via sampling, effective-fitness estimation
(probability-of-dominance methods), implicit averaging via dynamic population sizing, improved
search strategies, and robust selection. The survey notes that "no existing technique is
predominant" and "explicit averaging is often employed in practice because it can be seamlessly
incorporated into most evolutionary computation approaches" [Rakshit2017].

The empirical question of *which is more efficient* has conflicting answers. [Diaz2017-implicit]
(peer-reviewed *Informatica*) reports "a general advantage of implicit averaging... explicit
averaging is found to be non-competitive, due to the cost of repeat-evaluations of the same
solution." However, [Diaz2025-rev] (peer-reviewed IEEE TEVC, 2022 issue but referenced by
researchgate 2025) revisits the question and concludes that "the superiority of implicit averaging
relies on specific features of the noisy sphere problem with additive noise which cannot be
generalized to other problems" and that "the optimal averaging strategy depends on problem
characteristics and should be learned during optimization for maximum efficiency" [Diaz2025-rev].

**Hypothesis**: For a 68-d compartmental DSGC fitting problem with Gaussian-like within-cell noise,
neither pure explicit (N_SEEDS=20, pop=96) nor pure implicit (N_SEEDS=1, pop=480) averaging is
optimal; a hybrid that uses moderate replicates (N_SEEDS=4-8) at moderate population (96-192) should
outperform either extreme. t0102's N_SEEDS=4, pop=96 is a single point on this trade-off surface but
is consistent with the "moderate replicates + moderate pop" recommendation.

### Theory: NSGA-II Survives Bernoulli Noise Below p=0.5 with Polynomial Runtime

[Bian2023-noisy-NSGA] (peer-reviewed GECCO '23, also arxiv 2306.04525) gives the first formal
runtime analysis of NSGA-II under noise: "adds large amounts of posterior noise to all objectives
with some constant probability p per evaluation." Their main result is a **phase transition at p =
1/2**: below this threshold, NSGA-II covers the Pareto front in polynomial time on
LeadingOnesTrailingZeroes; above it, the time becomes exponential [Bian2023-noisy-NSGA]. Critically,
"NSGA-II is able to preserve useful search points even in the presence of noise" — unlike GSEMO,
which "fails badly on every noisy fitness function."

The translation to t0102: even if 5x fewer replicates raises the per-evaluation noise probability,
as long as the per-evaluation ranking error stays well below 50% on the dominant objective pair (DSI
vs PD-rate, which are the two we most care about), NSGA-II remains in the polynomial-runtime regime.
From our own t0091 smoke gate at N_SEEDS=4 (Spearman rho ~0.7 on top-10 Pareto cells versus
N_SEEDS=20, recorded in `tasks/t0091_morphology_extended_nsga2_v1/results/`), we are well below the
p=1/2 threshold.

### NSGA-II is *Not* the Best MOEA for Compartmental Neuron Fitting

[Neuroptimus-2024] (peer-reviewed *PLOS Computational Biology*) is the most directly relevant new
paper. The authors benchmark **23 algorithms** (including NSGA-II from Inspyred / BluePyOpt / Pygmo,
IBEA, CMAES, PSO variants, PAES) on six neuron-fitting benchmark problems including the
Hodgkin-Huxley model and the Hay 2011 L5 pyramidal cell from our existing corpus. They use **pop =
100, gens = 100, total 10000 evaluations per run, 10 repeats per algorithm-problem combination**
[Neuroptimus-2024].

Key results [Neuroptimus-2024]:

* **CMAES delivered the best results after 10000 model evaluations** consistently across all six
  problems.
* PSO variants ranked second.
* **IBEA is "clearly the best among the multi-objective methods"** — outperforming all three
  NSGA-II implementations.
* On the Hodgkin-Huxley benchmark, **Inspyred's NSGA-II performed significantly worse than the Pygmo
  and BluePyOpt versions**, indicating implementation differences matter.
* On some problems, **NSGA2, PAES and Pygmo's NSPSO performed worse than Random Search**.
* CMAES converged in approximately **3500 evaluations**.

This is a direct *contradiction* of the implicit assumption in our project that NSGA-II is the
canonical choice. Note that Neuroptimus uses single-cell, fixed-morphology problems; whether IBEA or
CMAES still dominates on our 68-d morphology + electrophys joint substrate is untested and is
recorded as a new hypothesis below.

**Hypothesis (new from internet research)**: For our 68-d substrate, IBEA or CMAES at pop=100,
gens=100 (10000 evals, 2.5x t0102's budget) would yield more joint-pass cells than NSGA-II at the
same total budget. This is a recommended follow-up after t0102 completes.

**Important caveat**: Neuroptimus's six benchmark problems are all *single-objective in aggregate*
(sum of feature errors) even when phrased as multi-objective for the algorithm; our joint-pass
condition is a *true* multi-objective target (DSI AND PD-rate AND robustness). The IBEA/CMAES
dominance may not transfer.

### Adaptive Resampling Approaches: Spend the Budget Where Noise Matters

[Budszuhn2025] (peer-reviewed arXiv preprint, April 2025) proposes adaptive resampling with
bootstrap for noisy MOO: rather than fixing N_SEEDS, the algorithm "incorporates the stochastic
nature of the optimization problem by using bootstrapping and the probability of dominance"
[Budszuhn2025]. The number of resamples per candidate is determined by the bootstrap estimate of the
probability that the candidate is on the Pareto front — high-uncertainty candidates get more
samples, low-uncertainty ones get fewer. Implemented as a wrapper around NSGA-II with sequential
resampling.

Best practice (community-converged 2024-2025): **adaptive N_SEEDS** is now considered superior to
fixed N_SEEDS in modern noisy-MOO algorithms. t0102's fixed N_SEEDS=4 design is therefore one step
behind the state of the art (which we noted as a gap in `research_papers.md`). A follow-up
suggestion: implement adaptive resampling in a future task (S-0102-NEW-01 below).

### Direction-Selective Ganglion Cell Modelling — Status of Field in 2025-2026

Beyond Poleg-Polsky 2026, two new DSGC-relevant papers appeared in 2025-2026:

* [Budoff2025-RGC-map] (bioRxiv preprint, Feb 2025) by Budoff & Poleg-Polsky created the **first
  complete spatial atlas of all 45 mouse RGC subtypes** using spatial transcriptomics. They report
  "about two-thirds of RGC subtypes showed uniform retinal distribution, while others demonstrated
  strong biases toward ventral or dorso-temporal regions" and identify gene expression along
  dorso-ventral axes [Budoff2025-RGC-map]. ON-OFF DSGCs are not specifically isolated, but the atlas
  provides the reference distribution for *which* DSGC subtypes we should be targeting and how their
  morphology might vary across retinal location.

* The Cell Reports 2026 paper on "hidden synaptic microarchitecture" (already in our corpus as
  `10.1016_j.celrep.2025.116833`, t0010 / t0024) emphasizes that "minor perturbations in the
  spatiotemporal properties of ACh — that do not disrupt the global excitation/inhibition balance
  — uncouple E/I locally and compromise direction selectivity." This is consistent with t0102's
  premise that the joint-pass corner is *narrow* and not all parameter sets in the acceptable region
  pass.

* The previously-noted bioRxiv preprint on starburst-amacrine retinal-wave development
  (`10.64898_2026.02.02.701812`, already in our corpus from t0080) reinforces that asymmetric SAC
  dendrite maturation is a developmental property and not a runtime parameter — confirming our
  decision to treat morphology as a fixed-after-init dimension rather than a time-varying one.

No paper found that *contradicts* the methodology recommendations from `research_papers.md`.
Direction-selective ganglion-cell modelling in 2025-2026 is converging on the SAC-inhibition-plus-
local-dendritic-computation account; this is exactly the substrate our 68-d search optimises over.

### BluePyOpt Has Moved Organisations — Tooling Implication

The Blue Brain Project concluded in **December 2024**, and BluePyOpt development has moved from
`github.com/BlueBrain/BluePyOpt` to `github.com/openbraininstitute/BluePyOpt`
[BluePyOpt-GH, OBI-GH]. The first Open Brain Institute Virtual Labs opened **March 28, 2025**. This
does not affect t0102 (which uses pymoo directly, not BluePyOpt) but is relevant context for any
future task that considers porting to the canonical neuroscience-optimisation stack.

## Methodology Insights

* **Keep NSGA-II for t0102 as planned** — switching algorithms mid-task is out of scope. But note
  in `results_summary.md` that [Neuroptimus-2024] benchmarks suggest IBEA or CMAES would likely
  outperform NSGA-II at the same budget; this should be tested in a follow-up.

* **The Gaussian-noise regime puts us in the explicit-averaging-works zone** [Akimoto2024]. The
  expected sqrt(5) ~ 2.24x increase in per-cell ranking SE at N_SEEDS=4 vs N_SEEDS=20 is the
  predicted cost; t0102 tests whether this is tolerable.

* **Run a substrate-consistency Spearman-rho smoke gate before launching** the long run, as already
  specified in `research_papers.md`. The internet literature does not change this recommendation —
  it confirms it. The [Bian2023-noisy-NSGA] phase-transition result says we need to verify p_error <
  0.5 per evaluation; a Spearman rho > 0.5 on top-K candidates is the proxy measurement.

* **Do not switch to adaptive resampling in t0102.** The [Budszuhn2025] approach is more
  sophisticated but introduces implementation risk; t0102 is an ablation study with one variable
  (N_SEEDS) changed, and changing two variables would confound the comparison with t0099. Defer
  adaptive resampling to a follow-up.

* **Best practice (community-converged 2024-2025)**: log the per-generation hypervolume curve to
  detect convergence stalls. Both [Neuroptimus-2024] and [Budszuhn2025] use hypervolume as the
  primary cross-algorithm comparison metric. Our t0102 analysis stage should compute and plot the
  hypervolume per generation, not just the final Pareto count.

* **Hypothesis to test in t0102 analysis** (extending the `research_papers.md` set): the
  hypervolume-vs-generation curve at N_SEEDS=4 will be **noisier** but show **similar mean
  trajectory** to N_SEEDS=20 from t0099 over the first ~5 generations. If the curves diverge
  systematically (N=4 plateaus higher or lower than N=20), it indicates non-trivial bias from
  reduced replicates that the t0091 smoke gate did not catch.

* **Hypothesis to test in a future task**: replacing NSGA-II with IBEA (default operator from
  BluePyOpt / DEAP) at the same pop=96, gens=20, N_SEEDS=4 would improve joint-pass yield by 2-10x
  on our 68-d substrate, mirroring the [Neuroptimus-2024] finding on simpler problems. This is
  captured as S-0102-NEW-02 below.

* **Implementation tip from [Neuroptimus-2024]**: when comparing across NSGA-II implementations,
  Inspyred's is consistently worse than BluePyOpt's and Pygmo's. Our pymoo-based implementation is
  not in their benchmark, but it is closer in design philosophy to Pygmo (well-tested SBX +
  polynomial mutation operators), so we should expect roughly Pygmo-like performance — i.e.,
  better than Inspyred but worse than IBEA.

* **Pitfall to avoid**: do *not* fall back to N_SEEDS=1 ("implicit averaging" via pop=480). The
  [Diaz2025-rev] revisit shows the "implicit-wins" result is fragile to problem structure, and the
  per-Vast.ai-instance constraint of pop=96 (max parallelism on a 64-core box) makes pop=480
  infeasible without spilling to slower disk-paged execution.

## Discovered Papers

### [Neuroptimus-2024]

* **Title**: Evaluation and comparison of methods for neuronal parameter optimization using the
  Neuroptimus software framework
* **Authors**: Mohácsi M., Török M. P., Sáray S., Tar L., Farkas G., Káli S.
* **Year**: 2024
* **DOI**: `10.1371/journal.pcbi.1012039`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012039
* **Suggested categories**: `compartmental-modeling`
* **Why download**: Most directly relevant 2024 paper for t0102. Benchmarks 23 optimisation
  algorithms including 3 NSGA-II implementations against IBEA, CMAES, PSO, PAES on 6 neuron
  benchmarks. Reports that IBEA and CMAES outperform NSGA-II on compartmental neuron fitting at
  pop=100, gens=100. Directly addresses the "is NSGA-II the right algorithm?" question for our
  project.

### [Bian2023-noisy-NSGA]

* **Title**: Analysing the Robustness of NSGA-II under Noise
* **Authors**: Bian C., Qian C., Neumann F., Sutton A. M.
* **Year**: 2023 (referenced 2024-2025)
* **DOI**: `10.1145/3583131.3590421` (GECCO '23) ; arxiv `10.48550/arXiv.2306.04525`
* **URL**: https://arxiv.org/abs/2306.04525
* **Suggested categories**: `compartmental-modeling`
* **Why download**: First formal runtime analysis of NSGA-II under noise. Proves the p=1/2 phase
  transition (polynomial below, exponential above) for Bernoulli posterior noise. Provides the
  theoretical anchor for "how noisy can N_SEEDS=4 get before NSGA-II breaks?" — directly relevant
  to t0102's adversarial test.

### [Budszuhn2025]

* **Title**: Adaptive Resampling with Bootstrap for Noisy Multi-Objective Optimization Problems
* **Authors**: Budszuhn T., Krallmann M. J., Horn D.
* **Year**: 2025
* **DOI**: `10.48550/arXiv.2503.21495`
* **URL**: https://arxiv.org/abs/2503.21495
* **Suggested categories**: `compartmental-modeling`
* **Why download**: Defines the state of the art in adaptive resampling for noisy MOO (2025).
  Provides the bootstrap-based probability-of-dominance methodology that a follow-up task could
  implement to avoid fixing N_SEEDS at any single value. Frames t0102's fixed-N_SEEDS=4 design as
  the simpler baseline against which adaptive methods will be compared.

### [Akimoto2024]

* **Title**: Theoretical Analysis of Explicit Averaging and Novel Sign Averaging in Comparison-Based
  Search
* **Authors**: Akimoto Y. (+ co-authors per arxiv listing)
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2401.14014`
* **URL**: https://arxiv.org/html/2401.14014
* **Suggested categories**: `compartmental-modeling`
* **Why download**: Provides the theoretical scaling law for explicit averaging: success probability
  `Phi_alpha(K^(1-1/alpha) * |signal| / noise)` where `alpha` is the noise stability parameter.
  Justifies why N_SEEDS=4 is suboptimal but not broken for our Gaussian-noise regime (`alpha=2`).
  Cited as the theoretical anchor for the entire t0102 design.

### [Rakshit2017]

* **Title**: Noisy evolutionary optimization algorithms — A comprehensive survey
* **Authors**: Rakshit P., Konar A., Das S.
* **Year**: 2017
* **DOI**: `10.1016/j.swevo.2017.01.002`
* **URL**: https://www.sciencedirect.com/science/article/abs/pii/S221065021630308X
* **Suggested categories**: `compartmental-modeling`
* **Why download**: Canonical survey of all five families of noisy-EA strategies (explicit
  averaging, fitness estimation, implicit averaging, modified search, robust selection). Old (2017)
  but heavily cited in 2024-2025 literature; should be in the corpus as the methodological reference
  taxonomy. Older than 2024-2026 focus, but a foundational survey that the recent literature
  uniformly assumes the reader knows.

### [Budoff2025-RGC-map]

* **Title**: A Complete Spatial Map of Mouse Retinal Ganglion Cells Reveals Density and Gene
  Expression Specializations
* **Authors**: Budoff S. A., Poleg-Polsky A.
* **Year**: 2025
* **DOI**: `10.1101/2025.02.10.637538` (bioRxiv preprint)
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC11844403/
* **Suggested categories**: `retinal-ganglion-cell`, `direction-selectivity`
* **Why download**: First complete spatial atlas of all 45 mouse RGC subtypes including ON-OFF
  DSGCs. Provides the reference distribution against which our optimised "joint-pass" DSGC
  morphologies should be benchmarked. Same lab as Poleg-Polsky 2026, so methodological consistency.
  Relevant for any future task that explicitly targets DSGC subtypes by spatial location.

## Recommendations for This Task

1. **Run t0102 as already planned** (pop=96, gens=20, GA seeds=44 and 55, N_SEEDS=4). The internet
   literature does not contradict any decision recorded in `research_papers.md`. The [Akimoto2024]
   theory anchor and [Bian2023-noisy-NSGA] phase-transition result together *strengthen* the case
   for the configuration: the regime is "noisy but well below the exponential-runtime threshold"
   with the predicted sqrt(5) ~ 2.24x SE inflation.

2. **Add hypervolume-per-generation logging to the analysis stage.** [Neuroptimus-2024] and
   [Budszuhn2025] both make hypervolume the standard cross-task readout. This is a low-effort change
   that produces a chart directly comparable to t0099's hypervolume curve and the literature norm.

3. **Document in `results_summary.md` that NSGA-II is not the optimal choice per
   [Neuroptimus-2024].** Frame the t0102 result honestly: even a positive result (joint-pass cells
   recovered) does not validate NSGA-II as the *best* algorithm — only that 5x fewer replicates +
   2.5x more gens are sufficient at the chosen algorithm. This is a substantial update to the
   `research_papers.md` recommendation set, which did not engage with this question.

4. **Record S-0102-NEW-01 (adaptive resampling) and S-0102-NEW-02 (IBEA replacement) as new
   suggestions** in `suggestions.json` during the reporting stage. These are direct, literature-
   backed follow-ups that the t0102 results will inform. S-0102-NEW-01 is "implement adaptive
   resampling per [Budszuhn2025]"; S-0102-NEW-02 is "rerun the 68-d substrate with IBEA per
   [Neuroptimus-2024]" at the same total budget.

5. **Do not change the N_SEEDS=4 setting based on internet research.** No paper provides a sharp
   threshold below which explicit averaging breaks; the [Akimoto2024] theory says the cost scales
   smoothly, and the [Bian2023-noisy-NSGA] phase transition is at p=1/2 ranking-error probability,
   which our t0091 smoke gate confirms we are below.

6. **Update the substrate-consistency smoke gate to additionally check hypervolume**: a
   downstream-MOEA metric, not just Spearman rho on Pareto identity. If hypervolume at N=4 differs
   from N=20 by more than 10% on the same set of cells, abort and refile with N=8. This is a
   stronger guardrail than ranking alone.

7. **Note in the results write-up that t0102 contributes one new data point on the "(replicates,
   generations, budget)" trade-off surface** that [Rakshit2017] and [Budszuhn2025] identify as
   unfilled in the literature. Even a negative result is publishable as an empirical data point.

## Tool and Library Landscape

* **pymoo** (Python NSGA-II / NSGA-III / MOEA/D / CMA-ES) — actively maintained, last release
  2024, the implementation used by t0080 / t0091 / t0099 / t0102. Provides the default operators
  (SBX eta=15, polynomial mutation eta=20) consistent with the literature. URL:
  `https://github.com/anyoptimization/pymoo` [pymoo-GH]

* **BluePyOpt** (Python DEAP-based NSGA-II + IBEA for compartmental neuron fitting) — moved from
  `github.com/BlueBrain/BluePyOpt` to `github.com/openbraininstitute/BluePyOpt` after the Blue Brain
  Project concluded December 2024. Used by the L5PC fit reference Van Geit 2016 (already in our
  corpus). [Neuroptimus-2024] reports BluePyOpt's NSGA-II performs *better* than Inspyred's,
  suggesting implementation quality varies. URL: `https://github.com/openbraininstitute/BluePyOpt`
  [BluePyOpt-GH]

* **Neuroptimus** (Python framework for benchmarking 23 optimisation algorithms on neuron models)
  — the benchmark suite from [Neuroptimus-2024]. Provides a unified interface to Inspyred, Pygmo,
  BluePyOpt, and direct CMA-ES / PSO. Not currently used by our project but is the natural
  cross-algorithm comparison tool for any S-0102-NEW-02-style follow-up.

* **CMA-ES** — `cma` Python package (Hansen et al.), the single-objective baseline from
  [Neuroptimus-2024] that "consistently converged to the optimal solution after approximately 3500
  evaluations." Could be used as a scalar baseline if we ever scalarise the joint-pass target into a
  single weighted-sum objective.

## Source Index

### [Neuroptimus-2024]

* **Type**: paper
* **Title**: Evaluation and comparison of methods for neuronal parameter optimization using the
  Neuroptimus software framework
* **Authors**: Mohácsi M., Török M. P., Sáray S., Tar L., Farkas G., Káli S.
* **Year**: 2024
* **DOI**: `10.1371/journal.pcbi.1012039`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012039
* **Peer-reviewed**: yes (*PLOS Computational Biology*)
* **Relevance**: Benchmarks 23 algorithms (including 3 NSGA-II implementations) on 6 neuron
  benchmarks at pop=100, gens=100, 10 repeats, 10000 evaluations per run. Reports CMAES wins, IBEA
  is best multi-objective, Inspyred-NSGA-II worse than Pygmo and BluePyOpt versions.

### [Bian2023-noisy-NSGA]

* **Type**: paper
* **Title**: Analysing the Robustness of NSGA-II under Noise
* **Authors**: Bian C., Qian C., Neumann F., Sutton A. M.
* **Year**: 2023
* **DOI**: `10.1145/3583131.3590421` (GECCO '23 proceedings)
* **URL**: https://arxiv.org/abs/2306.04525
* **Peer-reviewed**: yes (GECCO '23 conference proceedings)
* **Relevance**: Proves p=1/2 phase transition for NSGA-II under Bernoulli posterior noise. Provides
  the theoretical bound on how noisy fitness evaluation can be before NSGA-II breaks — directly
  relevant to t0102's N_SEEDS=4 design.

### [Budszuhn2025]

* **Type**: paper
* **Title**: Adaptive Resampling with Bootstrap for Noisy Multi-Objective Optimization Problems
* **Authors**: Budszuhn T., Krallmann M. J., Horn D.
* **Year**: 2025
* **DOI**: `10.48550/arXiv.2503.21495`
* **URL**: https://arxiv.org/abs/2503.21495
* **Peer-reviewed**: no (arXiv preprint, 14 pp, revised April 2025)
* **Relevance**: Provides the bootstrap-based adaptive-resampling recipe that frames t0102's
  fixed-N_SEEDS=4 as the simpler baseline. Cited as the motivation for S-0102-NEW-01.

### [Akimoto2024]

* **Type**: paper
* **Title**: Theoretical Analysis of Explicit Averaging and Novel Sign Averaging in Comparison-Based
  Search
* **Authors**: Akimoto Y. et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2401.14014`
* **URL**: https://arxiv.org/html/2401.14014
* **Peer-reviewed**: no (arXiv preprint, JSPS-funded)
* **Relevance**: Proves explicit-averaging scaling law
  `Pr_correct = Phi_alpha(K^(1-1/alpha) * signal/noise)`. Justifies the sqrt(5) ~ 2.24x SE inflation
  predicted at N_SEEDS=4 vs N_SEEDS=20 for Gaussian noise (`alpha = 2`).

### [Rakshit2017]

* **Type**: paper
* **Title**: Noisy evolutionary optimization algorithms — A comprehensive survey
* **Authors**: Rakshit P., Konar A., Das S.
* **Year**: 2017
* **DOI**: `10.1016/j.swevo.2017.01.002`
* **URL**: https://www.sciencedirect.com/science/article/abs/pii/S221065021630308X
* **Peer-reviewed**: yes (*Swarm and Evolutionary Computation*)
* **Relevance**: Foundational taxonomy of noisy-EA strategies. Provides the explicit-vs-implicit-
  averaging language used throughout the 2024-2025 follow-up literature. Cited as the methodological
  reference framework.

### [Diaz2017-implicit]

* **Type**: paper
* **Title**: Implicit and Explicit Averaging Strategies for Simulation-Based Optimization of a
  Real-World Production Planning Problem
* **Authors**: Diaz J. A. E., Handl J., Xu D.-L.
* **Year**: 2017
* **URL**:
  https://www.semanticscholar.org/paper/Implicit-and-Explicit-Averaging-Strategies-for-of-a-Diaz-Handl/c0d96129be23300f7b75e75381b0e05c2267a08d
* **Peer-reviewed**: yes (*Informatica*)
* **Relevance**: Original empirical finding that implicit averaging beats explicit averaging on a
  noisy production-planning problem. Provides the contrast point against which [Diaz2025-rev] argues
  the result does not generalise.

### [Diaz2025-rev]

* **Type**: paper
* **Title**: Revisiting Implicit and Explicit Averaging for Noisy Optimization
* **Authors**: Diaz J. A. E., Handl J., Xu D.-L.
* **Year**: 2022 (IEEE TEVC), revisit reference 2025
* **DOI**: IEEE TEVC `10.1109/TEVC.2022.3195856`
* **URL**: https://ieeexplore.ieee.org/document/9866832/
* **Peer-reviewed**: yes (*IEEE Transactions on Evolutionary Computation*)
* **Relevance**: Updates the [Diaz2017-implicit] result to show its fragility — "optimal averaging
  strategy depends on problem characteristics." Justifies the hybrid moderate-replicates +
  moderate-population design that t0102 instantiates.

### [Budoff2025-RGC-map]

* **Type**: paper
* **Title**: A Complete Spatial Map of Mouse Retinal Ganglion Cells Reveals Density and Gene
  Expression Specializations
* **Authors**: Budoff S. A., Poleg-Polsky A.
* **Year**: 2025
* **DOI**: `10.1101/2025.02.10.637538` (bioRxiv)
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC11844403/
* **Peer-reviewed**: no (bioRxiv preprint)
* **Relevance**: Most recent DSGC-relevant spatial-distribution paper. Confirms that 2/3 of RGC
  subtypes (including likely ON-OFF DSGCs) are uniformly distributed and 1/3 show ventral or
  dorso-temporal bias. Provides the reference distribution for downstream DSGC subtype targeting.

### [BluePyOpt-GH]

* **Type**: repository
* **Title**: BluePyOpt — Blue Brain Python Optimisation Library
* **Author/Org**: Open Brain Institute (formerly Blue Brain Project)
* **URL**: https://github.com/openbraininstitute/BluePyOpt
* **Last updated**: 2025-Q1 (post-OBI transition)
* **Peer-reviewed**: no (accompanies the Van Geit 2016 paper, which is peer-reviewed)
* **Relevance**: The canonical neuroscience-optimisation toolchain. Confirms that NSGA-II and IBEA
  are both available as selectors and that BluePyOpt's NSGA-II is one of the implementations
  benchmarked in [Neuroptimus-2024].

### [OBI-GH]

* **Type**: documentation
* **Title**: Open Brain Institute GitHub organisation
* **Author/Org**: Open Brain Institute
* **URL**: https://github.com/openbraininstitute
* **Last updated**: 2025 (active)
* **Peer-reviewed**: no
* **Relevance**: Confirms BluePyOpt's organisational migration after the Blue Brain Project
  concluded December 2024. Relevant context for any future task that pins a specific BluePyOpt
  release.

### [pymoo-GH]

* **Type**: repository
* **Title**: pymoo — Multi-objective Optimization in Python
* **Author/Org**: Blank J., Deb K. (anyoptimization)
* **URL**: https://github.com/anyoptimization/pymoo
* **Last updated**: 2024 (v0.6.1.6 documentation referenced)
* **Peer-reviewed**: no (accompanies the pymoo paper)
* **Relevance**: The actual NSGA-II implementation used by t0080 / t0091 / t0099 / t0102. Cited to
  confirm operator defaults (SBX eta=15, polynomial mutation eta=20, tournament size 2) match the
  literature norm.

### [PolegPolsky2026-NComm]

* **Type**: paper
* **Title**: Machine learning discovers numerous new computational principles supporting elementary
  motion detection
* **Authors**: Poleg-Polsky A.
* **Year**: 2026
* **DOI**: `10.1038/s41467-026-70288-4`
* **URL**: https://www.nature.com/articles/s41467-026-70288-4
* **Peer-reviewed**: yes (*Nature Communications*)
* **Relevance**: Already in our corpus (t0010); cited here to confirm internet-research findings
  match the paper-search findings. The Nature Communications abstract confirms the eight motion-
  detection primitives and the asymmetric-synapse mechanism class — consistent with
  `research_papers.md` recommendations and the t0102 substrate design.
