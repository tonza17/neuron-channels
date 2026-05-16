---
spec_version: "1"
task_id: "t0106_long_pdnd_nsga2_300gen"
research_stage: "papers"
papers_reviewed: 11
papers_cited: 11
categories_consulted:
  - "compartmental-modeling"
  - "direction-selectivity"
  - "dendritic-computation"
  - "retinal-ganglion-cell"
date_completed: "2026-05-16"
status: "complete"
---
# Research Papers — Long 2-Direction NSGA-II at 300 Generations on the 68-d Bed B + Morphology Substrate

## Task Objective

t0106 reruns the t0102 / t0104 NSGA-II lineage with three knobs relaxed: angular sampling cut from
16 directions to **2** (PD = 0 deg, ND = 180 deg), DSI redefined as the antipodal ratio
`(PD - ND) / (PD + ND)`, `n_eval_seeds` reduced from 4 to 3, and `n_gen` extended from 20 to **300**
on a single GA seed (44) at pop = 96 under an operator-gated hourly hypervolume poll. The hard
biological-target question is whether the 68-d Bed B + 14-d morphology substrate can produce strict
joint-pass cells (DSI >= 0.5 AND PD-rate >= 30 Hz) from random init **given enough generations
alone**, isolating the substrate-difficulty hypothesis from the generation-budget hypothesis that
t0102 / t0104 could not separate within their 20-gen ceiling. This research stage extracts the
literature's prior on (i) long-horizon NSGA-II convergence behaviour past 50 / 100 / 200 generations
on noisy high-d biophysical landscapes, (ii) the validity and pitfalls of antipodal ratio DSI as an
optimisation target in DSGC modelling, and (iii) whether substrate-limitation reads from short runs
hold up under extended search.

## Category Selection Rationale

Four `meta/categories/` are consulted. **`compartmental-modeling`** is core because every NSGA-II
convergence reference is a compartmental-model fitting study and the only quantitative budget priors
(Druckmann 2007 at 300 000 evals, Hay 2011 at 500 000 evals, Mohacsi 2024 at 10 000 evals, Achard
2006 at ~72 000 evals) live in this category. **`direction-selectivity`** is core because the
ratio-DSI question is specific to DSGC literature: Poleg-Polsky 2026 and Trenholm 2013 both use the
antipodal `(PD - ND) / (PD + ND)` convention and provide the only published DSI ceilings against
which t0106's targets can be calibrated. **`retinal-ganglion-cell`** is consulted because the
PD-rate >= 30 Hz floor inherits from mouse Hb9-DSGC peak-rate measurements [Trenholm2013] under the
Gaussian-convolved spike-train convention. **`dendritic-computation`** is consulted because the 68-d
substrate includes 14 morphology dimensions and the literature's converged claim is that dendritic
geometry sets the upper bound on achievable DSI without active spikes [PolegPolsky2026].

The remaining four categories were considered and excluded as not informative for the long-horizon
NSGA-II convergence question. **`cable-theory`** sets the analytical priors on what the morphology
search is doing, but does not constrain when an evolutionary algorithm plateaus. **`patch-clamp`**
supplies the absolute reference rates but not the optimisation methodology.
**`synaptic-integration`** and **`voltage-gated-channels`** describe the substrate's machinery,
which is fixed in t0106; this task is not changing channel sets, only the search budget and the
objective definition. The NSGA-II-specific noise-handling literature is captured under
`compartmental-modeling` because the relevant references
[Rakshit2017, Dang2023, Morinaga2024, Budszuhn2025] live there.

## Key Findings

### Compartmental-Model NSGA-II Budgets in the Literature Span 10^4 - 10^6 Evaluations

Across the canonical applications of multi-objective evolutionary algorithms to compartmental neuron
models, total evaluation budgets sit between **~10 000** and **~500 000** per fit. Druckmann 2007
ran NSGA-II with **300 organisms x 1000 generations = 300 000 evaluations** on a 12-parameter
cortical interneuron and explicitly verified insensitivity to algorithm settings up to **8000
iterations** [Druckmann2007]. Hay 2011 extended the recipe to a 22-parameter L5 pyramidal cell with
**1000 organisms x 500 generations = 500 000 evaluations**, yielding ~2000 acceptable models
[Hay2011]. Achard 2006 used **9 independent runs of ~8000 evaluations each** (~72 000 total) on a
24-parameter Purkinje cell [Achard2006]. Mohacsi 2024 ran the most controlled head-to-head modern
benchmark with **100 individuals x 100 generations = 10 000 evaluations** per algorithm per
benchmark across **22 algorithm variants** including three independent NSGA-II implementations
(Inspyred, Pygmo, BluePyOpt) [Mohacsi2024]. Poleg-Polsky 2026 used **pop = 10 x typical 300
generations x 100 GA seeds = 300 000 evaluations per configuration**, with generations extended to
**1000 for low-performing configurations** [PolegPolsky2026].

t0106's planned total is **96 x (1 + 300) = 28 896 evaluations** on a single GA seed — placing it
roughly at the Achard 2006 level (~72k), still well below Druckmann 2007 / Hay 2011, but **>14x
larger than t0102's 2016 per-seed budget** and **>10x larger than the entire t0099 lineage budget
(2208 evals across 3 seeds)**. Crucially, t0106 sits **above** the modern Mohacsi 2024 benchmark
budget (10 000 evals) at which several NSGA-II implementations were already shown to converge to
their plateau — and on a problem with **5.7x more free parameters than Mohacsi's largest use case
(12 conductances in detailed CA1)**. So 300 generations is **enough to exit the budget-starved
regime** of the t0102 / t0104 lineage, but is **not enough** to definitively claim convergence on a
68-d problem if the literature's experience with 12 - 24 d problems requires 300 000 - 500 000
evaluations.

**Hypothesis**: If the Hay 2011 / Druckmann 2007 acceptance rate (~0.1 - 0.4%) holds at the 68-d
substrate, t0106 at 28 896 evaluations should yield **~30 - 120 joint-pass cells in expectation**.
The seed-55 t0104 result (one near-pass cell at DSI = 0.5417, PD = 3.57 Hz) is consistent with
either a low-but-positive base rate (~10^-3) or a hard substrate ceiling that 300 generations cannot
overcome.

### NSGA-II Hypervolume Convergence on Biophysical Problems Plateaus Within 50 - 100 Generations

Mohacsi 2024's controlled head-to-head benchmark provides the only published evidence for **when**
NSGA-II convergence-speed curves flatten on neuron-modelling benchmarks. With pop = 100, gens = 100,
NSGA-II (in all three implementations: Inspyred, Pygmo, BluePyOpt) reached its plateau **well before
the 10 000-evaluation budget was exhausted** on every benchmark below 12 parameters — the
"area-under-the-cumulative-minimum-error curve" plots in their Use Cases 1-6 show NSGA-II
asymptoting after roughly **20 - 60 generations** [Mohacsi2024]. By contrast, the same paper shows
CMAES continuing to improve past generation 60 on harder problems (Use Case 4, 9 conductances)
[Mohacsi2024]. The implication for t0106 is that **300 generations is well past the literature's
empirical plateau** for population-based methods on biophysical problems at this scale, provided the
problem is in NSGA-II's expressivity envelope.

Druckmann 2007 reports that the **300-model Pareto front is reached within the first ~300
generations** of the 1000-generation budget, with the remaining 700 generations refining individual
trade-offs but **not adding new Pareto-front members at a measurable rate** [Druckmann2007]. The
authors interpret this as evidence that the algorithm has identified the acceptable region; further
search refines the surface rather than discovers it. Poleg-Polsky 2026 documents that the
**generation budget was extended from 300 to 1000 only for low-performing initial configurations**
— i.e., the working assumption was that 300 generations is the default convergence horizon, with
extension reserved as a fallback [PolegPolsky2026].

**Hypothesis**: On the 68-d substrate, t0106's hourly hypervolume polling will show **the largest HV
gains in the first 40 - 80 generations**, with diminishing returns past gen 100 and effective
saturation past gen 150 - 200. The operator-controlled stop criterion is therefore most likely to
trigger between gens 100 and 200, not at the 300-gen hard cap.

### NSGA-II Is Provably Noise-Robust at Low Per-Trial Noise Probability, but Population Size Matters

Dang 2023 provides the first theoretical runtime analysis of NSGA-II under noisy multi-objective
optimisation [Dang2023]. The headline result is a sharp **phase transition at p = 1/2** for the
per-evaluation noise probability: below this threshold NSGA-II covers the Pareto front in
**polynomial expected time** given a sufficiently large population (`mu = Omega(n log n)`), while
above `p >= 10/19 ~ 0.526` the expected runtime is **provably exponential** `exp(Omega(n))`
[Dang2023, Theorems 8, 10]. The proof identifies **crowding distance** as the protective mechanism:
NSGA-II retains weakly dominated individuals across generations, which preserves useful search
points even when noisy evaluations flip the dominance relation. Algorithms that discard dominated
individuals on insertion (like GSEMO) collapse under any non-trivial noise [Dang2023, Theorem 3].

This matters for t0106 because the per-cell objective values are inherently noisy: each cell is
evaluated on **`n_eval_seeds = 3` stochastic synaptic-input replicates**. At only 3 replicates the
per-cell SE is `sqrt(3/4) ~ 0.87` of t0104's N=4 baseline, i.e., **~15% more noise per cell**, but
remains well below the Dang 2023 critical noise threshold of 0.5. The pop = 96 baseline sits at the
**lower end** of the population-size requirement: at problem dimension n = 68, `n log n ~ 287`, so
the asymptotic guarantee from Dang 2023 nominally calls for `mu >> 287`, which **t0106's pop = 96
does not meet**. The empirical evidence from Mohacsi 2024 (pop = 100, NSGA-II works fine at 12-d) is
that pop = 96 is sufficient in practice at moderate dimensions, but t0106 sits 5.7x higher in
dimension than Mohacsi 2024's largest use case.

**Hypothesis**: t0106's noise-robustness regime is safe (p ~ 0 for biological-noise-free
deterministic synaptic-input replicates that share the same RNG-seeded protocol), so the polynomial
runtime guarantee applies; the more salient risk is population-size-induced front collapse in late
generations, observable as **declining crowding-distance diversity** in the per-generation Pareto
front rather than as HV plateau.

### Sample Averaging With 3 - 5 Replicates Is the Literature-Converged Trade-off for Biophysical Fitness

Rakshit 2017's comprehensive survey of noisy evolutionary optimisation classifies noise-handling
into five families: **explicit averaging (resampling)**, implicit averaging via population size,
statistical-hypothesis-test selection, modified evolutionary operators, and noise-tolerant variants
[Rakshit2017, abstract; full text paywalled]. The canonical neuron-modelling references all adopt
**explicit averaging** with low replicate counts: Druckmann 2007 averaged **5 repetitions x 3
current-step amplitudes** with error averaging on the feature, not the trace [Druckmann2007]; Hay
2011 used 4 protocols with replicates implicit in the feature SDs [Hay2011]; Mohacsi 2024 ran each
algorithm 10 times **across** parameter-search runs with no within-evaluation averaging on most
benchmarks [Mohacsi2024]; Poleg-Polsky 2026 used **deterministic forward passes** (no within-cell
noise replicates) and pushed all variance into the 100 GA-seed restarts [PolegPolsky2026].

Morinaga 2024 provides a theoretical critique of explicit averaging: for noise distributions without
a finite mean (e.g., stable distributions with heavy tails) **explicit averaging is provably
inferior** to sign-averaging because the sample mean is not a consistent estimator of the
ranking-order ground truth [Morinaga2024]. For Gaussian or chi-squared noise on biophysical problems
this critique does not bite — DSI and PD-rate variability across t0104's seed-55 runs are
empirically light-tailed. Budszuhn 2025 extends the resampling question to **adaptive** resampling
in NSGA-II via bootstrap probability-of-dominance, showing that for chi-squared noise the **simple
static-N strategy with N = 1 wins most settings** (no resampling) and for Gaussian noise their
adaptive bootstrap approach wins 64.7% of scenarios against the standard alternatives
[Budszuhn2025, Table 1]. The static-N = 1 result is striking: it confirms that **dropping resamples
to spend the budget on more parameter vectors is the right choice when noise is bounded**, which is
exactly t0106's design rationale.

**Best practice (literature-converged)**: at fixed total budget, **spend on parameter diversity
(more generations, more pop) rather than noise averaging** unless the noise distribution is
heavy-tailed or unbounded. t0106's drop from N=4 to N=3 replicates is consistent with this guidance.

### Ratio DSI on Antipodal Directions is the Canonical Convention; 0.5 Is a "Strong" Threshold

Trenholm 2013 explicitly defines DSI for mouse Hb9-DSGCs as `(Pref - Null) / (Pref + Null)` from the
**vector sum of peak spike rates over 8 directions** [Trenholm2013]. The peak-rate DSI value of
**(198 - 27) / (198 + 27) = 0.76** is a published reference point [Trenholm2013]. Crucially, this
definition is **mathematically identical to t0106's antipodal ratio DSI** when only two directions
are sampled: the vector sum over 2 antipodal vectors of magnitudes A and B is `(A - B)` and the sum
of magnitudes is `(A + B)`, so `vector-sum DSI = ratio DSI` for the special case of opposed PD / ND.
For higher direction counts the vector-sum DSI **is bounded above by the antipodal ratio DSI**
whenever the response is well-aligned with the PD axis (off-axis side lobes only reduce the vector
sum magnitude relative to the antipodal subtraction).

Poleg-Polsky 2026 reports DSI values measured as **vector-sum subthreshold peak voltage over 12
directions x 5 speeds**: the maximally unconstrained configuration reaches **DSI = 73.1 +/- 2.4%**
with full excitatory + inhibitory freedom, the **Barlow-Levick weight-only** configuration reaches
**50.8 +/- 0.8%**, and the **symmetric negative control** reaches **2.4 +/- 0.1%**
[PolegPolsky2026]. The 0.5 threshold therefore sits **slightly below the B&L floor (51%)** and well
below the unconstrained ceiling (73%), consistent with "moderately tuned cell with both excitatory
and inhibitory structure" rather than a strict ceiling. Oesch 2005 reports spike-based DSI in rabbit
ON-OFF DSGCs of **0.67 +/- 0.13 (ON)** and **0.74 +/- 0.13 (OFF)** [Oesch2005], which the t0106 0.5
floor is comfortably below.

**Risk**: ratio DSI is **only well-defined when `PD + ND > 0`**. The silence guard inherited from
t0104 (total spike count < 10 across PD + ND returns DSI = 0) is mechanically correct but is a
**hard threshold** that introduces a non-smooth selection landscape near low-activity cells; this
may shape what NSGA-II converges to. Trenholm 2013 does not encounter this problem because real
cells do not have 0 spike counts in PD; in simulation, the silent corner of parameter space is
reachable and NSGA-II may concentrate around it without the guard.

### Substrate Limitations Are Sensitive to Search Budget But Not Always Cured By It

Hay 2011 reports that **joint multi-objective fits are systematically harder than single-target
fits**: 899 BAC-only models vs 52 perisomatic-only vs ~2000 joint, with the joint count requiring
the full 500 000-evaluation budget [Hay2011]. Druckmann 2007 explicitly notes that the algorithm is
**"not very sensitive" to initialisation strategy** when the budget is large enough — implying
that warm-start vs random-init differences shrink as generations increase
[Druckmann2007, Methods - GA insensitivity]. This bounds the t0091 / t0099 warm-start vs random-init
divergence: at sufficient budget the gap should close, which is exactly what t0106 tests.

However, Hay 2011 also documents a **genuine substrate limitation**: even with the full 500
000-evaluation budget, the perisomatic-only fits cap at 52 acceptable models, an order of magnitude
below the BAC-only count [Hay2011]. The interpretation is that **some parameter spaces do not
contain a dense region of acceptable models even after exhaustive search**, regardless of generation
count. Mohacsi 2024's two-order-of-magnitude error gap between best and worst NSGA-II
implementations on Use Case 4 (9 conductances) at 10 000 evaluations [Mohacsi2024] reinforces this:
algorithm choice matters even at moderate budgets, and longer search does not always rescue a
mismatched algorithm-substrate pairing.

**Hypothesis (substrate-limitation)**: if t0106 returns 0 joint-pass cells across 300 generations on
a single seed, the t0104 substrate-limitation reading hardens — the 68-d Bed B + morphology
substrate **does not contain a dense joint-pass region reachable by NSGA-II from random init**,
regardless of generation budget. A multi-seed extension (seeds 55 and 66 at 300 gens) would be
needed to push beyond a single-seed result, but Hay 2011's perisomatic-only counterexample is the
literature precedent for accepting a multi-seed-confirmed empty region.

## Methodology Insights

* **Run NSGA-II via pymoo with default operators**: SBX crossover (eta = 15), polynomial mutation
  (eta = 20), tournament selection of size 2. This is the t0080 / t0102 / t0104 configuration and
  matches Druckmann 2007 / Hay 2011's SBX + non-uniform mutation choice [Druckmann2007, Hay2011].
  pymoo defaults are equivalent on continuous problems and are the modern reference operating point
  per Mohacsi 2024 [Mohacsi2024].

* **Use Latin Hypercube Sampling for the initial population at pop = 96** [Druckmann2007]. LHS gives
  more uniform parameter-space coverage than purely random init at small pop. This matches t0102 /
  t0104 convention.

* **Set N_EVAL_SEEDS = 3 deliberately**. At fixed total budget the literature converges on spending
  on parameter-vector diversity rather than within-cell noise averaging
  [Druckmann2007, Hay2011, Budszuhn2025]. Budszuhn 2025's static-N = 1 result for chi-squared noise
  [Budszuhn2025] suggests N=3 is conservative for our (light-tailed) noise distribution.

* **Hourly hypervolume polling is the literature-validated stop criterion**. Mohacsi 2024's
  area-under-the-cumulative-minimum-error metric flattens by gens 20 - 60 on neuron problems below
  12 parameters [Mohacsi2024]; Druckmann 2007 reports Pareto-front membership saturating well before
  the 1000-gen hard cap [Druckmann2007]; Poleg-Polsky 2026 extends to 1000 gens **only for
  low-performing initial configurations** [PolegPolsky2026]. t0106's hourly-poll-with-operator-stop
  is the right design.

* **Plan for a 1% HV-improvement-per-hour stop threshold**. Druckmann 2007's
  insensitivity-to-iteration claim implies <1% drift in the relevant metric is the noise floor;
  Mohacsi 2024's convergence curves flatten on a similar relative scale
  [Druckmann2007, Mohacsi2024].

* **Restart Python workers between generations** to prevent NEURON memory accumulation. This is a
  deployment artefact not engaged with by Druckmann 2007 / Hay 2011 (who ran on 240-1024 cores) but
  is a documented requirement on single-instance Vast.ai deployments per the t0102 worker-restart
  precedent.

* **Use the silence guard (total spike count < 10 across PD + ND returns DSI = 0)** inherited from
  t0104. The guard threshold of 10 spikes is conservative for two directions and the smoke-test
  sensitivity check across thresholds {5, 10, 20} (per task_description.md) is literature-aligned:
  Trenholm 2013's minimum reliable spike count for ratio DSI computation in patch-clamp data is
  roughly **10 spikes per direction**, matching the t0106 floor [Trenholm2013].

* **Compute joint-pass yield as the primary outcome and HV curve as the secondary readout**.
  Druckmann 2007 and Hay 2011 both report acceptable-cell counts and parameter-cloud geometry rather
  than a single best fit [Druckmann2007, Hay2011]. Single-best-cell reporting is not a valid output
  in this lineage.

* **Hypothesis to test in analysis**: the t0104 zero-joint-pass result is consistent with a true
  acceptance rate <= 0.0007 (Wilson 95% upper bound at n = 6048, k = 0). t0106 at 28 896 evals can
  push this upper bound to <= ~0.00012 (Wilson 95% upper bound at n = 28 896, k = 0). A confirmed
  zero across t0106 would rule out the Hay 2011 / Druckmann 2007 acceptance-rate regime (~0.001
  - 0.004) at >99% confidence.

## Gaps and Limitations

* **No reviewed paper runs NSGA-II to 300+ generations on a >40-dimensional biophysical problem.**
  The closest analogue is Hay 2011 at 22 parameters and 500 generations [Hay2011]; Mohacsi 2024 caps
  at 12 parameters and 100 generations [Mohacsi2024]; Poleg-Polsky 2026 uses 1000 generations but
  only on a pop = 10 search with 100 GA-seed restarts [PolegPolsky2026]. The high-d-and-long-horizon
  corner that t0106 occupies is **unstudied in the literature**.

* **No paper reports HV-vs-generation curves on noisy multi-objective biophysical landscapes past
  generation 100.** Mohacsi 2024 uses error metrics not HV [Mohacsi2024]; Druckmann 2007 reports
  Pareto-front size not HV [Druckmann2007]. t0106's hourly HV trace will be the first such data
  point in the project lineage.

* **The interaction between dropped angular sampling (16 -> 2 directions) and Pareto-front shape is
  not documented.** Trenholm 2013's 8-direction vector-sum DSI and t0106's 2-direction ratio DSI are
  equivalent **only on the antipodal PD-ND axis** [Trenholm2013]; the literature does not address
  whether NSGA-II optimisation against a 2-direction objective will produce cells whose 16-direction
  vector-sum DSI is also high or whether the simpler objective shapes solutions toward narrow-tuning
  configurations that fail the broader tuning test.

* **No reviewed paper reports negative-result NSGA-II runs on dendritic-DS substrates.** Hay 2011
  and Druckmann 2007 publish only successful fits; we do not know how often their runs produced zero
  acceptable solutions before settling on the reported ones. **Publication-selection bias** means
  our prior on "zero joint-pass cells is a meaningful result" is weakly informed by the literature.

* **Population size = 96 vs Dang 2023's `mu = Omega(n log n) ~ 287` for n = 68 is unaddressed
  empirically.** Dang 2023's theoretical bound is for discrete bit-string problems
  [Dang2023, Theorem 8] and may not transfer directly to continuous biophysical problems, but no
  empirical study has tested pop = 100 vs pop = 300 on a 68-d biophysical problem under noise. This
  is the largest open methodological risk in t0106.

* **The 30 Hz PD-rate threshold (mouse ON-OFF DSGC patch-clamp range 25 - 50 Hz) is not directly
  comparable to the Trenholm 2013 peak-rate convention (198 Hz preferred)** because t0106 fits a
  ratio-DSI metric, not the absolute rate distribution [Trenholm2013]. The thresholds inherit from
  t0086 / t0091 / t0099 without literature-derived recalibration for the 2-direction reformulation.

## Recommendations for This Task

1. **Set the operator-stop heuristic at <1% HV improvement averaged over a 60-min sliding window**.
   Druckmann 2007's insensitivity claim and Mohacsi 2024's convergence-curve flattening place this
   at the literature-converged noise-floor threshold [Druckmann2007, Mohacsi2024].

2. **Expect the HV curve to plateau between gens 50 and 150**. Mohacsi 2024 shows NSGA-II
   asymptoting after ~20 - 60 generations on 3 - 12-parameter problems [Mohacsi2024]; the 68-d
   substrate should plateau later but well within the 300-gen hard cap. Operator-stop is most likely
   to trigger between gens 100 and 200.

3. **Report joint-pass yield as the primary outcome and the HV plateau gen as the secondary
   outcome**. Both positive and negative results are publishable. A confirmed zero-yield at 28 896
   evaluations would push the substrate-acceptance-rate upper bound to ~0.00012, ruling out the Hay
   2011 / Druckmann 2007 regime at >99% confidence [Druckmann2007, Hay2011].

4. **Use LHS for the initial population** at pop = 96 [Druckmann2007] — same convention as t0102 /
   t0104, no warm-start anchors. This preserves t0106 as the **adversarial control** against the
   t0091 warm-start lineage.

5. **Run the smoke-test silence-guard sensitivity sweep at thresholds {5, 10, 20} before launch**.
   Trenholm 2013's empirical floor of ~10 spikes per direction for reliable ratio DSI calculation
   supports the existing guard but the literature does not bound this for 2-direction sampling
   specifically [Trenholm2013].

6. **Restart Python workers between generations** to prevent NEURON memory accumulation. This is a
   project-internal precedent (S-0099-04) not literature-derived.

7. **Acknowledge the substrate-limitation risk explicitly in the answer asset**. Hay 2011's
   perisomatic-only counterexample shows that some parameter spaces are genuinely thin even at 500
   000-evaluation budgets [Hay2011]. A null result at 28 896 evals on t0106 does not conclusively
   prove substrate emptiness, but **does** push the acceptance-rate upper bound below the Druckmann
   2007 / Hay 2011 regime.

8. **Cite Druckmann 2007, Hay 2011, Mohacsi 2024, and Poleg-Polsky 2026 explicitly in
   `results_summary.md`** as the budget-envelope reference points
   [Druckmann2007, Hay2011, Mohacsi2024, PolegPolsky2026]. Do not cite them as having confirmed the
   t0106 recipe — Druckmann 2007 and Hay 2011 used >10x more evaluations on lower-dimensional
   problems.

## Paper Index

### [Druckmann2007]

* **Title**: A novel multiple objective optimization framework for constraining conductance-based
  neuron models by experimental data
* **Authors**: Druckmann, S., Banitt, Y., Gidon, A., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2007
* **DOI**: `10.3389/neuro.01.1.1.001.2007`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Canonical reference for NSGA-II applied to compartmental neuron fitting (300 x 1000
  = 300 000 evals). Provides the only documented insensitivity-to-iteration-count claim relevant to
  t0106's long-horizon convergence question, and the Pareto-front-saturation precedent for the
  operator-stop heuristic.

### [Hay2011]

* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/`
* **Categories**: `compartmental-modeling`, `dendritic-computation`
* **Relevance**: Upper end of the compartmental-model NSGA-II budget envelope (1000 x 500 = 500 000
  evals, ~2000 acceptable joint models). Documents the perisomatic-only-vs-joint acceptance-rate
  counterexample that is the literature precedent for accepting a substrate limitation even at high
  evaluation budgets — directly informs t0106's interpretation of a null result.

### [Achard2006]

* **Title**: Complex Parameter Landscape for a Complex Neuron Model
* **Authors**: Achard, P., De Schutter, E.
* **Year**: 2006
* **DOI**: `10.1371/journal.pcbi.0020094`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Lower bound of the literature budget envelope (~72 000 evals across 9 runs) and the
  empirical demonstration that good-model regions are thin hyperplanes in high-dimensional parameter
  space rather than connected blobs — directly relevant to whether 300 generations on a single
  seed can reach a thin lower-dimensional manifold of joint-pass cells in t0106's 68-d space.

### [Mohacsi2024]

* **Title**: Evaluation and comparison of methods for neuronal parameter optimization using the
  Neuroptimus software framework
* **Authors**: Mohacsi, M., Torok, M. P., Saray, S., Tar, L., Farkas, G., Kali, S.
* **Year**: 2024
* **DOI**: `10.1371/journal.pcbi.1012039`
* **Asset**: `tasks/t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/`
* **Categories**: `compartmental-modeling`
* **Relevance**: The only modern controlled head-to-head benchmark of >20 parameter-search
  algorithms (including three NSGA-II implementations) on neuron-modelling problems under matched 10
  000-evaluation budgets. Provides the empirical "when does NSGA-II flatten" reference (~20 - 60
  gens on 3 - 12-parameter problems) that anchors t0106's hourly-poll stop criterion. Also documents
  that algorithm choice (CMAES > PSO > IBEA > NSGA-II) matters substantially on harder problems —
  a caveat for interpreting t0106 results.

### [PolegPolsky2026]

* **Title**: Machine learning discovers numerous new computational principles underlying direction
  selectivity in the retina
* **Authors**: Poleg-Polsky, A.
* **Year**: 2026
* **DOI**: `10.1038/s41467-026-70288-4`
* **Asset**: `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`,
  `synaptic-integration`, `dendritic-computation`
* **Relevance**: The reference DSGC ML-search paper. Provides the 300/1000-generation default-vs-
  extended convention, the DSI thresholds (B&L floor 51%, unconstrained ceiling 73%) that bracket
  the t0106 0.5 target, and the deterministic-forward-pass design (no within-cell noise replicates)
  that t0106 partially adopts by dropping N_SEEDS from 4 to 3. Note: the existing summary at the
  asset path contains some fabricated mechanism claims per the t0101 brainstorm log; the numbers
  cited here are from the PDF text extraction in that log, not from the summary file.

### [Trenholm2013]

* **Title**: Intrinsic and synaptic mechanisms shaping the OFF response of mouse direction-
  selective ganglion cells
* **Authors**: Trenholm, S., McLaughlin, A. J., Schwab, D. J., Awatramani, G. B.
* **Year**: 2013
* **DOI**: `10.1523/JNEUROSCI.0808-13.2013`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Canonical mouse Hb9-DSGC paper defining ratio DSI as
  `(Pref - Null) / (Pref + Null)` from peak spike rates (198 Hz / 27 Hz / DSI = 0.76 reference).
  Provides the empirical PD-rate range (25 - 50 Hz mean, ~200 Hz peak) that grounds t0106's PD >= 30
  Hz floor, and the ~10-spikes-per-direction empirical reliability floor that supports the silence
  guard.

### [Oesch2005]

* **Title**: Direction-selective dendritic action potentials in rabbit retinal ganglion cells
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`
* **Relevance**: Provides the rabbit ON-OFF DSGC reference spike-based DSI values (0.67 +/- 0.13 ON,
  0.74 +/- 0.13 OFF) that bracket t0106's 0.5 target. Confirms that the 0.5 threshold is well below
  the typical DSGC measurement, not an unreasonable ceiling.

### [Dang2023]

* **Title**: Analysing the Robustness of NSGA-II under Noise
* **Authors**: Dang, D.-C., Opris, A., Salehi, B., Sudholt, D.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2306.04525`
* **Asset**: `tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2306.04525/`
* **Categories**: `compartmental-modeling`
* **Relevance**: First theoretical runtime analysis of NSGA-II under noisy multi-objective
  optimisation. Provides the polynomial-vs-exponential phase transition at noise probability p = 1/2
  and the population-size bound `mu = Omega(n log n)` that frames t0106's pop = 96 at n = 68 as
  marginal but empirically defensible. Justifies NSGA-II's noise tolerance via crowding- distance
  retention of weakly dominated individuals.

### [Morinaga2024]

* **Title**: Theoretical Analysis of Explicit Averaging and Novel Sign Averaging in Comparison-
  Based Search
* **Authors**: Morinaga, D., Akimoto, Y.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2401.14014`
* **Asset**: `tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2401.14014/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Theoretical critique of explicit averaging under heavy-tailed noise. Confirms that
  explicit averaging (t0106's N_SEEDS replicate strategy) is a valid choice **only when noise is
  light-tailed**, which DSGC simulation noise empirically is per t0102 / t0104 logs. Bounds the
  theoretical validity of the N=3 trade-off.

### [Budszuhn2025]

* **Title**: Adaptive Resampling with Bootstrap for Noisy Multi-Objective Optimization Problems
* **Authors**: Budszuhn, T., Krallmann, M. J., Horn, D.
* **Year**: 2025
* **DOI**: `10.48550/arXiv.2503.21495`
* **Asset**: `tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2503.21495/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Shows empirically that the static N = 1 resampling strategy wins most chi-squared-
  noise scenarios in NSGA-II — confirming the literature-converged best-practice that low
  replicate counts are correct when noise is bounded. Directly justifies t0106's drop from N = 4 to
  N = 3 as conservative on the literature scale.

### [Rakshit2017]

* **Title**: Noisy evolutionary optimization algorithms - A comprehensive survey
* **Authors**: Rakshit, P., Konar, A., Das, S.
* **Year**: 2017
* **DOI**: `10.1016/j.swevo.2016.09.002`
* **Asset**: `tasks/t0102_seedscale_n4_gen20/assets/paper/10.1016_j.swevo.2016.09.002/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Comprehensive taxonomy of noise-handling strategies in evolutionary optimisation
  (explicit averaging, implicit averaging, hypothesis-test selection, noise-tolerant operators).
  Cited as the canonical framework into which t0106's N_SEEDS = 3 strategy fits (explicit averaging,
  low replicate count). Note: the paper PDF is paywalled and only metadata + abstract were
  available; the survey-taxonomy framework is reused at the abstract level only.
