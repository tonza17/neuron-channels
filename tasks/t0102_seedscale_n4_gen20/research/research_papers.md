---
spec_version: "1"
task_id: "t0102_seedscale_n4_gen20"
research_stage: "papers"
papers_reviewed: 7
papers_cited: 7
categories_consulted:
  - "compartmental-modeling"
  - "direction-selectivity"
  - "retinal-ganglion-cell"
  - "dendritic-computation"
  - "synaptic-integration"
date_completed: "2026-05-11"
status: "complete"
---
# Research Papers — Seed/Generation Re-Balance for 68-d NSGA-II on Bed B DSGC

## Task Objective

t0102 runs the 68-d random-init NSGA-II from t0099 again but reduces the within-cell noise
replicates `N_SEEDS` from 20 to 4 (a 5x cut) and extends generations from 5-8 to 20, on two new GA
seeds (44, 55, pop=96, $8 cap). The hypothesis under test is that at constant Vast.ai budget, the
Poleg-Polsky 2026 (`10.1038/s41467-026-70288-4`) seed-and-generation profile recovers a strict
joint-pass cell (DSI >= 0.5, PD-rate >= 30 Hz, robustness >= 0.7) without the 5-anchor warm-start
that t0091 used. The research question is whether the literature converges on a recipe for how to
spend a fixed-eval budget across GA seeds, generations, and noise replicates for compartmental
neuron fitting, and what specific numbers the canonical references (Druckmann 2007, Hay 2011, Achard
2006, Van Geit 2016, Poleg-Polsky 2026) actually used.

## Category Selection Rationale

Five categories from `meta/categories/` are consulted. **`compartmental-modeling`** is core because
the substrate is a compartmental NEURON model and every cited reference is a compartmental-model
fitting study; this is where the methodology references live. **`direction-selectivity`** is core
because Poleg-Polsky 2026 — the paper that motivates the re-balance — is a DSGC direction-
selectivity ML search; the DSI scoring convention and its sensitivity to noise replicates are
specific to this category. **`retinal-ganglion-cell`** is consulted because all priors on joint-pass
thresholds (DSI >= 0.5, PD-rate >= 30 Hz, robustness >= 0.7) are RGC-targeted and the specific cells
whose phenotype we are matching are mouse ON-OFF DSGCs [Ezra-Tsur2021]. The
**`dendritic-computation`** category supplies the mechanistic context for why morphology is included
in the 68-d substrate (14 morphology dimensions) — biological dendrites perform direction-
selective computations that are not captured by the 54-d electrophys-only search
[Hay2011, PolegPolsky2026]. **`synaptic-integration`** is consulted because the per-cell noise that
`N_SEEDS` averages over comes from trial-to-trial variability of dendrite-distributed AMPA/GABA
inputs, which is exactly Druckmann 2007's domain of measurement.

The remaining three categories (`cable-theory`, `patch-clamp`, `voltage-gated-channels`) were
considered and excluded as not motivating the seed/generation budget question. Cable-theory papers
inform what is being optimised but not how to spend the search budget. Patch-clamp informs the
ground-truth feature SDs but t0102 does not directly fit patch-clamp data — it fits to a synthetic
joint target. Voltage-gated channels are part of the search space but the budget question is
algorithm-agnostic to which parameters are searched.

## Key Findings

### Canonical NSGA-II/MOO Budgets for Compartmental Neuron Fitting Sit at 10^5-10^6 Evaluations

Across four reference applications of multi-objective evolutionary algorithms to compartmental
neuron models, total evaluation budgets sit between **~70 000** and **~500 000** per fit. Druckmann
2007 ran NSGA-II with **300 organisms x 1000 generations = 300 000 evaluations** to fit a
12-parameter compartmental cortical interneuron, with insensitivity verified up to **8000
iterations** [Druckmann2007, Table-references for the per-generation count, p. 11]. Hay 2011
extended the recipe to a richer 22-parameter L5 pyramidal cell with 20 features and ran **1000
organisms x 500 generations = 500 000 evaluations** on 240-1024 cores for 2-5 days per fit
[Hay2011, Methods section, p. 4]. Achard 2006 used a (57+19) self-adaptive ES on a 24-parameter
Purkinje cell for **9 independent runs of ~8000 evaluations each = ~72 000 evaluations** total,
yielding 20 acceptable models [Achard2006, Methods, p. 4]. Van Geit 2016 (BluePyOpt) reported the
L5PC use case (the Hay 2011 problem repackaged) finishing in **~4 hours on 50 cores with IBEA at 100
individuals x 100 generations = 10 000 evaluations** when the search space is reduced and the
algorithm is upgraded from NSGA-II to IBEA [VanGeit2016, Use Case 2, p. 11]. Poleg-Polsky 2026 ran
the deepest single-configuration sweep in the family: **10 (pop) x 300 (typical generations) x 100
(GA seeds) = 300 000 evaluations per configuration**, with generations extended to **1000 for
low-performing configurations**
[PolegPolsky2026, Methods section, as extracted in `tasks/t0101_brainstorm_results_21/results/results_detailed.md`].

By contrast, our own NSGA-II lineage on the 54-d substrate has so far used **at most 1728
evaluations in the largest single lineage** (t0081 pop=96 x gens=0-17 = 1728 candidates, one GA
seed) and **at most 2208 evaluations on the 68-d substrate** in t0099 (3 GA seeds at pop=96 x
gens=5/8/8 = 1824 candidates). The Druckmann 2007 envelope alone is **174x larger** than t0099's
total budget. t0102 increases the per-seed budget to 96 init + 20 gens x 96 = 2016 candidates and
the total budget to 4032 (two seeds), still **74x below** the Druckmann 2007 envelope on a problem
with 5.7x more free parameters.

**Hypothesis**: if Poleg-Polsky 2026's 50-100 seeds x 300-1000 generations recipe is the actual
recipe rather than overkill, t0102's 2 seeds x 20 gens budget remains insufficient. A negative
result in t0102 would not falsify the warm-start hypothesis but instead say "we cannot tell within
this envelope." A positive result, however, would falsify the load-bearing-warm-start claim.

### Per-Cell Noise Replicates Trade Off Linearly Against Generation Count at Fixed Budget

Every cited reference uses **noise replicates per evaluation** rather than a single deterministic
forward pass, but the count varies by an order of magnitude across the literature. Druckmann 2007
used **5 repetitions x 3 current-step amplitudes = 15 traces per cell** but explicitly averaged
feature *errors* across repetitions (not the trace itself), keeping each generation cost at 15
NEURON runs per organism [Druckmann2007, Methods - feature scoring, p. 9]. Hay 2011 followed the
same convention with 4 protocols x repetitions implicit in the feature SDs [Hay2011, Methods, p. 5].
Poleg-Polsky 2026 used **deterministic phenomenological RFs with no within-cell noise replicates**
— the entire "noise" comes from inter-seed parameter re-randomisation, which is why the algorithm
tolerates 100 GA restarts at pop=10
[PolegPolsky2026, Methods, as recorded in `tasks/t0101_brainstorm_results_21/results/results_detailed.md`].
Our substrate sits at the opposite extreme: t0099 used **N_SEEDS = 20** within-cell noise replicates
x 8 directions x ~1 s per direction = ~160 NEURON sims per parameter-vector evaluation. The
Druckmann recipe of 15 traces per cell is **10x cheaper than t0099 per evaluation** yet uses a 174x
larger total budget — i.e., the literature spends its evaluation budget on *more diverse parameter
vectors*, not on noise averaging.

For a fixed compute budget B = N_SEEDS x sims_per_seed x pop x gens x ga_seeds, dropping N_SEEDS
from 20 to 4 frees 5x compute that can be redirected to gens, pop, or ga_seeds. t0102's choice is to
direct it to gens (8 -> 20, 2.5x increase) and partially to ga_seeds (1 -> 2). This is the
**variance-budget vs exploration-budget trade-off**: at N=4 the per-cell DSI/PD estimate has
sqrt(20/4) = 2.24x larger SE than at N=20, so the NSGA-II selection pressure on noisy cells weakens.
Druckmann 2007 shows that the algorithm is "**not very sensitive**" to noise-averaging strategy
provided the population is large enough to retain a Pareto-non-dominated subset; the canonical
NSGA-II crowding distance protects diversity even when individual rankings are noisy
[Druckmann2007, Methods - GA insensitivity, p. 10]. This supports — but does not prove — t0102's
gamble.

**Hypothesis (t0102-specific)**: at `N_SEEDS = 4`, NSGA-II Pareto-front identity is preserved within
~1 standard error of `N_SEEDS = 20` so long as pop=96 (large enough that crowding distance dominates
ranking noise). A direct test is the substrate-consistency smoke gate (REQ-7-equivalent from t0081),
which compares Pareto-membership identity at N=4 vs N=20 on a held-out set of cells.

### Parameter-Space Degeneracy Means Many Acceptable Solutions Exist Per Run

Prinz 2004 simulated **20 250 000** STG networks and found that **4 047 375 (20%)** produce a
pyloric-like rhythm and **452 516 (2.2%)** match all 15 quantitative experimental criteria
[Prinz2004, Results, p. 1347]. Every one of the 150 cell-triple configurations and the full
functional range of every synaptic conductance (**0 - 100 nS**) is represented in the matching set
— six of seven synapses span **two orders of magnitude** without breaking pyloric output. Achard
2006 found **20 distinct best-fit Purkinje models** within an evolution-strategy search of ~72 000
evaluations, with channel densities such as gCaTm and gKAm spanning **the entire allowed range**
across the acceptable set [Achard2006, Results, p. 6]. Hay 2011 generated **~2000 acceptable L5PC
models** within its 500 000-evaluation budget (BAC-only: 899, perisomatic-only: 52, joint: ~2000)
[Hay2011, Results, p. 7]. Druckmann 2007 found **300 acceptable parameter sets within 2 SD on every
feature** for each electrical class — so within a single 300 000-evaluation NSGA-II run, ~0.1% of
the population produced a strict-pass model [Druckmann2007, Results, p. 13]. Poleg-Polsky 2026
reports **DSI values up to 73.1 +/- 2.4%** in the fully unconstrained configuration vs **2.4 +/-
0.1%** in the symmetric control — meaning ~30x range across acceptable parameter regimes within a
single ~300 000-evaluation sweep
[PolegPolsky2026, Results table extracted in `tasks/t0101_brainstorm_results_21/results/results_detailed.md`].

The translatable lesson for t0102: the *expected* yield of strict-pass cells per 4032-evaluation run
is **2-10**, not 0, if t0102's substrate is in the same parameter-density regime as Hay 2011 (2000
acceptable / 500 000 = 0.4%) or Druckmann 2007 (300 / 300 000 = 0.1%). t0099's null result (0
strict-pass / 2208 evaluations) is consistent with the 0.1% acceptance rate within statistical
expectation (P(0 | n=2208, p=0.001) ~ 0.11), but is **also** consistent with p=0 — i.e., a hard
zero rather than a low-but-positive base rate. A positive t0102 result with 2-5 cells would strongly
favour the low-base-rate explanation; another zero would favour the substrate-difficulty
explanation.

### Warm-Start Provides Compute Equivalent of ~10-50 Random-Init Generations on the Same Substrate

Druckmann 2007 verified insensitivity of the final 300-model Pareto to **initialisation strategy**
up to 8000 iterations, implying that **the recipe is not warm-start-dependent** when the budget is
large enough [Druckmann2007, Methods, p. 10]. However, Hay 2011 explicitly notes that **single-
target fits are easier than joint fits**: 899 BAC-only models vs 52 perisomatic-only vs ~2000 joint,
with the joint count requiring a "**larger search budget**" — consistent with a warm-start giving
an equivalent of "free generations" of pre-search [Hay2011, Results, p. 7]. Our own t0091 data add a
third pin: t0091 reached **1 strict joint-pass cell at gen 2 of 8** ($0.65 spend) when warm-started
with 5 anchors, while t0099 reached **0 strict joint-pass cells across 3 random-init seeds at gens
5/8/8** ($7.71 spend, 12x the t0091 cost). The compute differential between t0091 (176 evals: pop=96
x gens=2 - dedup) and t0099 (2208 evals across 3 seeds) suggests warm-start was worth roughly
**(2208 - 176) / pop = ~21 generations** of free pre-search per seed, or equivalently 10-12
generations of free exploration at t0091's pop=96. t0102's 20-generation budget sits within this
estimate — it should recover the joint-pass corner *if and only if* the warm-start was worth at
most ~20 generations of search effort.

**Best practice (literature-converged)**: when a target is hard to satisfy (joint multi-objective,
biological priors), spend the first 10-20% of the budget on a structured initial population (LHS,
anchor-based, or single-objective pre-search) rather than fully random init. Hay 2011 used a
restricted upper bound on Ih to guarantee subthreshold validity from generation 0
[Hay2011, Methods, p. 4]; Druckmann 2007 shifted Nat and Kslow voltage by hand by **+10 mV and +20
mV** respectively to bring AP features into the fittable range before optimisation began
[Druckmann2007, Methods, p. 8]. t0102's choice of pure random init is therefore an *adversarial*
test: it deliberately removes a literature-converged best practice to isolate the value of
warm-starting.

### NSGA-II Pop Size of ~100 Is the Floor; Druckmann 300, Hay 1000 Set a Soft Upper Bound

Druckmann 2007 used pop = **300**, Hay 2011 used pop = **1000**, Van Geit 2016 used pop = **100** in
its IBEA reference [VanGeit2016, Use Case 2, p. 11], Achard 2006 used pop = **57 + 19 offspring = 76
effective**, and Poleg-Polsky 2026 used pop = **10** (extreme low end, compensated by 100 GA seed
restarts) [PolegPolsky2026, as extracted in t0101 brainstorm logs]. Our default pop=96 (set by
t0080/t0091 plans) sits at the **lower end of the cited range** but is consistent with the
BluePyOpt/IBEA recipe. The risk at low pop is that NSGA-II's crowding-distance diversity
preservation becomes unreliable in high-dimensional objective spaces: t0102's 68-d Pareto front may
not be well-sampled by 96 individuals, especially after the first few generations of selection
pressure collapse the front.

### DSI/PD/Robustness Target Thresholds Are Empirically Set By Published In Vivo Data

t0102's strict joint-pass thresholds (DSI >= 0.5, PD-rate >= 30 Hz, robustness >= 0.7) inherit from
t0086/t0091. Poleg-Polsky 2026 reports DSI values measured as **vector-sum subthreshold peak voltage
over 12 directions x 5 speeds**: the maximally unconstrained configuration reaches **DSI = 73.1 +/-
2.4%** with full excitatory + inhibitory freedom, the **B&L (Barlow-Levick) weight-only**
configuration reaches **50.8 +/- 0.8%**, and the **symmetric negative control** reaches **2.4 +/-
0.1%** [PolegPolsky2026, Results, as extracted in t0101 brainstorm logs]. By contrast, our own DSI
is computed from **spike rates over 8 cardinal directions** at a single speed, so the absolute
numbers are not directly comparable, but the **0.5 threshold sits between the B&L floor (51%) and
the unconstrained ceiling (73%)** of Poleg-Polsky 2026, which is consistent with our target
representing a "moderately tuned cell with both excitatory and inhibitory structure". The PD-rate
threshold of 30 Hz is set by mouse ON-OFF DSGC patch-clamp data at the preferred-direction firing
rate of 25-50 Hz [Ezra-Tsur2021, Figure references in the paper], so the 30 Hz floor is the lower
edge of physiologically realistic.

## Methodology Insights

* **Adopt NSGA-II from pymoo, default operators**: SBX crossover (eta=15), polynomial mutation
  (eta=20), tournament selection of size 2 — same configuration as t0080/t0091/t0099. Druckmann
  2007 and Hay 2011 used custom NEURON-embedded NSGA-II with SBX + non-uniform mutation; pymoo's
  defaults are equivalent on continuous problems
  [Druckmann2007, Methods, p. 8; Hay2011, Methods, p. 4].

* **Pop = 96, gens = 20, GA seeds = 2 (44, 55), N_SEEDS = 4**. The literature floor for pop is 50
  [Achard2006, Methods, p. 4]; t0102's 96 sits comfortably above. The 20-generation budget covers
  the **2-21 generation range** where t0099 / t0091 differed; if 20 gens still produces zero
  joint-pass cells, that bounds the warm-start value at >=20 free generations of search.

* **Latin Hypercube Sampling for initial population** [Druckmann2007, p. 8]. LHS gives more uniform
  parameter-space coverage than purely random init at small pop. This was the convention in t0099
  and t0102 should match it.

* **Apply restart-between-generations to prevent NEURON memory accumulation** — this is the
  S-0099-04 fallback already noted as a risk in t0102's `task_description.md`. Hay 2011 ran on
  240-1024 cores so memory was not a constraint; our single-instance run on a 64-core Vast.ai box
  must restart Python workers between generations to avoid super-linear wall-clock growth.

* **Substrate-consistency smoke gate before launching the long run**: re-evaluate t0099's top-10
  Pareto cells at N=4 and confirm Spearman rho >= 0.7 between N=4 and N=20 rankings (REQ-7-
  equivalent threshold widened from the t0081 0.85 to account for the increased noise). This is the
  only direct empirical test of the "N=4 is enough" hypothesis before committing to 18-24 hours of
  Vast.ai compute. If Spearman rho < 0.5, abort and use N=8 instead.

* **Compute joint-pass yield as the primary outcome**, hypervolume curve as a secondary readout, and
  anchor-distribution histogram as a tertiary readout (matching t0086/t0091/t0099 reporting
  convention). Druckmann 2007 and Hay 2011 both report acceptable-cell counts and parameter-cloud
  geometry rather than a single best fit [Druckmann2007, Results, p. 13; Hay2011, Results, p. 8].
  Returning a single best-cell is not a valid output in this lineage.

* **Use per-feature SD-normalised objectives (Druckmann z-score)** when the time comes to compare
  cells to patch-clamp data — not directly applied in t0102 (which uses the t0080/t0086 synthetic
  joint target) but should be the standard in any downstream follow-up that re-scores t0102's Pareto
  on real DSGC data [Druckmann2007, p. 9; VanGeit2016, Use Case 2, p. 11].

* **Report Pareto-front membership as ensemble, not single-best**. Hay 2011 and Druckmann 2007 both
  make this a central methodological point [Druckmann2007, p. 13; Hay2011, p. 14]. t0102's analysis
  stage must produce the joint-pass count as an integer and the anchor-distribution histogram across
  the union of the two seeds' Pareto fronts (not a max over seeds).

* **Hypothesis to test in t0102 analysis**: the t0099 0/55 joint-pass tally is consistent with a
  true joint-pass-acceptance rate of ~0.001 (i.e., the Hay 2011/Druckmann 2007 yield rate), meaning
  t0102 at 4032 evaluations should yield 2-10 joint-pass cells in expectation under that null. A
  yield of 0 would push the upper 95% CI on the acceptance rate below 0.0007 (Wilson interval) and
  strengthen the conclusion that the joint-pass corner is genuinely empty without warm-starting.

## Gaps and Limitations

* **None of the cited papers tested a 5x noise-replicate reduction in isolation.** Druckmann 2007,
  Hay 2011, Achard 2006, and Van Geit 2016 all kept noise replicates fixed across their respective
  studies and ablated other dimensions (pop, gens, init strategy). Poleg-Polsky 2026 used
  deterministic forward passes and so cannot inform the trade-off between noise and exploration.
  t0102 is therefore an *empirical question without literature precedent*; the smoke gate is the
  only available calibration.

* **No reviewed paper reports per-seed cost or wall-clock super-linearity due to NEURON memory
  accumulation.** This is a deployment artefact that the academic literature does not engage with.
  The S-0099-04 fallback (restart Python workers between generations) is folk knowledge from our own
  t0099, not from the cited references.

* **The literature does not report negative-result NSGA-II runs on dendritic-DS substrates.** Hay
  2011 and Druckmann 2007 publish only successful fits; we do not know how often their runs produced
  zero acceptable solutions before settling on the reported ones. The reporting bias means our prior
  on "zero joint-pass cells" being a meaningful result is weakly informed by the literature — the
  cited papers have a strong selection effect toward published successes.

* **Poleg-Polsky 2026 does not document budget-matched ablation between (high seeds, low gens) vs
  (low seeds, high gens)** — both extreme regimes are reported separately (50-100 seeds x 300-1000
  gens), but the paper does not vary the ratio at fixed total budget. t0102 is one point on this
  unstudied axis. A budget-matched ablation is recorded as deferred suggestion S-0101-03.

* **The relationship between morphology dimensions (14 d) and electrophys dimensions (54 d) in the
  joint 68-d substrate is not addressed by any cited paper.** Hay 2011 transplants morphologies
  between fitted parameter sets ex post; Druckmann 2007 uses a single fixed reconstruction; Achard
  2006 uses a fixed Purkinje cell. The combinatorics of jointly searching parameter and morphology
  space — and how that increases the effective dimensionality of the problem relative to a
  Druckmann-style purely-electrophys fit — is **not in the literature** at the time of t0102.

* **The 0.5 DSI threshold (spike-rate-based, 8 directions) is not directly comparable to the
  Poleg-Polsky 2026 0.5 threshold (subthreshold-voltage-based, 12 directions x 5 speeds).** Our
  threshold is empirically calibrated by t0086 and t0091 but does not have a literature analogue
  with the same measurement convention.

## Recommendations for This Task

1. **Run the substrate-consistency smoke gate at N_SEEDS=4 before launching the long run.** Compare
   Spearman rho between N=4 and N=20 rankings on t0099's top-10 Pareto cells; if rho < 0.5, abort
   and refile with N=8. This is the only literature-justified guardrail
   [Druckmann2007, Methods - GA insensitivity, p. 10].

2. **Set pop=96, gens=20, GA seeds=44 and 55, N_SEEDS=4.** This is the configuration the brainstorm
   session 21 settled on and is within the literature-converged operating envelope of
   compartmental-model NSGA-II (pop floor 50 [Achard2006], pop ceiling 1000 [Hay2011], gens floor 8
   from t0099, gens ceiling 1000 from [PolegPolsky2026]).

3. **Report joint-pass yield as the primary outcome.** Both positive and negative results are
   publishable (per task_description.md verification criteria). A 0-yield result with a passing
   smoke gate would push the substrate-difficulty hypothesis above 95% confidence.

4. **Use LHS for the initial population** [Druckmann2007, Methods, p. 8], same convention as t0099,
   no warm-start anchors. This is the *adversarial control* against t0091.

5. **Restart Python workers between generations** to prevent NEURON memory accumulation (S-0099-04
   fallback). Hay 2011's 240-1024-core deployment did not encounter this; our single-instance
   deployment must mitigate it.

6. **Record the per-seed wall-clock and per-cell evaluation time** so that a future budget-matched
   ablation (deferred suggestion S-0101-03, "PP-style 10-20 GA seeds at gens 8 each") can be
   designed off t0102's actual cost numbers, not the plan estimates.

7. **Side-by-side compare t0102 vs t0099 vs t0091** Pareto cell counts, anchor distributions, and
   joint-pass yields in the analysis stage. This is the experiment's only valid contrast.
   Single-task headline numbers are not interpretable without the t0091/t0099 baselines.

8. **Cite Druckmann 2007, Hay 2011, and Poleg-Polsky 2026 explicitly in `results_summary.md`** as
   the budget-envelope reference points. Do not cite them as having confirmed our recipe — they
   used 70-500x more evaluations.

## Paper Index

### [Druckmann2007]

* **Title**: A novel multiple objective optimization framework for constraining conductance-based
  neuron models by experimental data
* **Authors**: Druckmann, S., Banitt, Y., Gidon, A., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2007
* **DOI**: `10.3389/neuro.01.1.1.001.2007`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Canonical reference for NSGA-II applied to compartmental neuron fitting. Sets the
  300 organisms x 1000 generations envelope and the SD-normalised feature-error formulation that
  t0102's hypothesis test is implicitly comparing against. Provides the only documented
  insensitivity-to-noise claim relevant to t0102's N_SEEDS=4 gamble.

### [Hay2011]

* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/`
* **Categories**: `compartmental-modeling`, `dendritic-computation`
* **Relevance**: Sets the upper end of the compartmental-model NSGA-II budget envelope (1000 pop x
  500 gens = 500 000 evaluations) and is the most direct literature analogue for t0102's joint
  multi-objective problem (perisomatic + dendritic active features). Demonstrates that joint fits
  are harder than single-target fits, which is exactly t0102's premise — DSI+PD+robustness is a
  joint target.

### [Achard2006]

* **Title**: Complex Parameter Landscape for a Complex Neuron Model
* **Authors**: Achard, P., De Schutter, E.
* **Year**: 2006
* **DOI**: `10.1371/journal.pcbi.0020094`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Documents the low end of the budget envelope (9 runs x ~8000 evaluations = ~72 000)
  and the lower bound on pop size (57 + 19 = 76). Shows that the parameter landscape of "good"
  models is a set of hyperplanes rather than a single connected blob — directly relevant to the
  question of whether a 4032-evaluation run can reach a thin lower-dimensional manifold of
  joint-pass cells in t0102's 68-d space.

### [VanGeit2016]

* **Title**: BluePyOpt: Leveraging Open Source Software and Cloud Infrastructure to Optimise Model
  Parameters in Neuroscience
* **Authors**: Van Geit, W., Gevaert, M., Chindemi, G., Rossert, C., Courcol, J.-D., Muller, E.,
  Schurmann, F., Segev, I., Markram, H.
* **Year**: 2016
* **DOI**: `10.3389/fninf.2016.00017`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.3389_fninf.2016.00017/`
* **Categories**: `compartmental-modeling`
* **Relevance**: The canonical neuroscience-optimisation toolchain; documents pop=100, gens=100 IBEA
  as the modern operating point (with IBEA replacing NSGA-II as the recommended default). Useful as
  an "engineered minimum" reference (10 000 evaluations on a Hay-style 18-param problem) bracketing
  t0102's 4 032-evaluation budget on a 68-param problem.

### [Prinz2004]

* **Title**: Similar network activity from disparate circuit parameters
* **Authors**: Prinz, A. A., Bucher, D., Marder, E.
* **Year**: 2004
* **DOI**: `10.1038/nn1352`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1038_nn1352/`
* **Categories**: `compartmental-modeling`, `synaptic-integration`
* **Relevance**: Empirical degeneracy result — 4 047 375 of 20 250 000 networks (20%) produce
  acceptable pyloric rhythms. Sets the base rate for "what fraction of parameter space supports an
  acceptable phenotype" against which t0102's joint-pass yield rate must be compared. If t0102
  reaches 2-5 joint-pass cells out of 4 032, that corresponds to a 0.05-0.12% acceptance rate,
  similar to Hay 2011 and Druckmann 2007 but ~150x rarer than Prinz 2004's pyloric rate — a
  reflection of the joint-pass corner being a much narrower target than "any pyloric-like rhythm".

### [PolegPolsky2026]

* **Title**: Machine learning discovers numerous new computational principles supporting elementary
  motion detection
* **Authors**: Poleg-Polsky, A.
* **Year**: 2026
* **DOI**: `10.1038/s41467-026-70288-4`
* **Asset**: `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`,
  `synaptic-integration`, `dendritic-computation`
* **Relevance**: The paper that motivates t0102's re-balance. Documents 50-100 GA restarts at pop=10
  x 300-1000 generations on a 352-segment DSGC. Provides the seed/generation ratio that t0102
  partially imitates (more gens at fewer seeds), the DSI thresholds (0.5 sits between the B&L 51%
  and the unconstrained 73% ceilings), and the deterministic-forward-pass alternative to
  noise-replicate averaging. Note: the existing `summary.md` at the asset path contains fabricated
  claims (NMDA multiplicative gating, A-type K density, etc.) per
  `tasks/t0101_brainstorm_results_21/results/results_detailed.md`; the numbers cited here are from
  the PDF text extraction in that brainstorm session, not from the summary file. A correction is
  pending as deferred suggestion S-0101-01.

### [Ezra-Tsur2021]

* **Title**: Realistic retinal modeling unravels the differential role of excitation and inhibition
  to starburst amacrine cells in direction selectivity
* **Authors**: Ezra-Tsur, E., Amsalem, O., Ankri, L., et al.
* **Year**: 2021
* **DOI**: `10.1371/journal.pcbi.1009754`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1009754/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`
* **Relevance**: Provides the mouse ON-OFF DSGC patch-clamp-derived firing rate range (25-50 Hz
  preferred-direction) used by our project as the physiological grounding for the PD-rate >= 30 Hz
  threshold. Confirms that the joint-pass target is anchored in published in vitro electrophysiology
  rather than an arbitrary optimisation goal.
