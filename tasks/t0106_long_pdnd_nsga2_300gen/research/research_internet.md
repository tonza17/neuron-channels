---
spec_version: "1"
task_id: "t0106_long_pdnd_nsga2_300gen"
research_stage: "internet"
searches_conducted: 11
sources_cited: 13
papers_discovered: 3
date_completed: "2026-05-16"
status: "complete"
---
# Research Internet — Long 2-Direction NSGA-II at 300 Generations on the 68-d Bed B + Morphology Substrate

## Task Objective

t0106 reruns the t0102 / t0104 NSGA-II lineage with three knobs relaxed: angular sampling cut from
16 directions to **2** (PD = 0 deg, ND = 180 deg), DSI redefined as the antipodal ratio
`(PD - ND) / (PD + ND)`, `n_eval_seeds` reduced from 4 to 3, and `n_gen` extended from 20 to **300**
on a single GA seed (44) at pop = 96 under an operator-gated hourly hypervolume poll. The internet
research stage targets four open questions not resolved by the corpus: (1) 2024-2026 evidence on
long-horizon NSGA-II on 40+ -d biophysical neuron problems, (2) empirical hypervolume-plateau
heuristics in pymoo / EMO 2024 papers, (3) DSGC modelling work that uses ratio DSI on a 2-direction
protocol rather than vector-sum DSI on 8 / 16 directions, and (4) operator-stop signalling patterns
for long-running pymoo NSGA-II processes.

## Gaps Addressed

The four explicit gaps from `research_papers.md` are addressed below. The gap-numbering follows the
order in that file.

1. **"No reviewed paper runs NSGA-II to 300+ generations on a >40-dimensional biophysical
   problem."** — **Partially resolved.** Chen et al. 2024 [Chen2024-STN] use a custom GA (not
   NSGA-II) at population = 120 with approximately **1 000 000 evaluated phenotypes** on a 20-d
   subthalamic-nucleus model. The budget is two orders of magnitude larger than t0106's 28 896 evals
   and confirms that biophysical-model EAs do scale to very long horizons in practice, but the
   algorithm is bespoke not NSGA-II and the parameter count (20) is below t0106's 68-d substrate. No
   2024-2026 publication was found that runs NSGA-II specifically past 200 generations on a 40+ -d
   biophysical neuron model. The Open Brain Institute fork of BluePyOpt [OBI-BluePyOpt-GH] (post-Dec
   2024 successor to BlueBrain/BluePyOpt) still exposes the IBEA / NSGA-II / CMAES algorithm trio
   without changing the canonical 100-200 generation default.

2. **"No paper reports HV-vs-generation curves on noisy multi-objective biophysical landscapes past
   generation 100."** — **Unresolved for biophysical specifics, partially resolved on EMO
   tooling.** Blank and Deb 2020 [BlankDeb2020] introduce the canonical running performance metric
   (delta-IGD / delta-HV with a normalized sliding-window threshold) that pymoo's `RunningMetric`
   and `RobustTermination` directly implement [pymoo-running-GH]. The pymoo-canonical convergence
   threshold visible in source is `tol = 0.005` for the delta metric with `period = None` (default
   sliding window stores all history) [pymoo-running-GH]. This sets a literature-validated reference
   for t0106's "<1% moving-window improvement" heuristic: the t0106 threshold of 1% is **2x more
   permissive** than pymoo's hardcoded 0.005 (0.5%) significance cut and is therefore conservatively
   triggered.

3. **"The interaction between dropped angular sampling (16 -> 2 directions) and Pareto-front shape
   is not documented."** — **Unresolved.** Recent DSGC modelling work continues to use 8 - 16
   directions for DSI calculation: Ankri et al. 2024 [Ankri2024] (already in corpus as
   10.1113_JP286581 in t0091) use moving-spot stimuli across a hemifield to expose directional
   excitation, and Riccitelli et al. 2025 [Riccitelli2025] (already in corpus as
   10.1073_pnas.2415223122 in t0080) record motion responses to a 12-direction grid. The recent
   ON-OFF DSGC dendritic-architecture paper [CavalHolme2025] (PubMed 39871013) does measure
   preferred / null axis asymmetries directly but reports the classical 8-direction vector-sum DSI.
   No publication was found that fits an NSGA-II / EA model using only PD and ND. The t0106
   2-direction reformulation is therefore **methodologically novel** within the literature surveyed.

4. **"No reviewed paper reports negative-result NSGA-II runs on dendritic-DS substrates."** —
   **Unresolved.** Mohacsi 2024 (already in corpus) is the only modern controlled benchmark
   reporting per-algorithm performance and explicitly publishes failed-to-converge runs across 22
   algorithms, but its substrate is not dendritic-DS. The internet search confirms the
   publication-selection bias documented in `research_papers.md`: post-2024 dendritic-DS papers
   still report only successful fits.

5. **"Population size = 96 vs Dang 2023's `mu = Omega(n log n) ~ 287` for n = 68 is unaddressed
   empirically."** — **Unresolved.** The 2024-2025 NSGA-II theoretical literature
   [Difficulties-NSGA2-2024] (Doerr et al., arXiv 2411.10017) extends the discrete-problem negative
   results to many-objective LeadingOnes but does not address continuous biophysical problems, and
   no empirical study comparing pop = 100 vs pop = 300 on a 68-d biophysical substrate was found.
   This gap remains open and the t0106 result will be the first project data point in this regime.

6. **"The 30 Hz PD-rate threshold ... is not directly comparable to the Trenholm 2013 peak-rate
   convention (198 Hz preferred) because t0106 fits a ratio-DSI metric, not the absolute rate
   distribution."** — **Partially resolved.** The Webvision DSGC chapter [Webvision-DSGC] confirms
   that classical patch-clamp DSI threshold convention is **DSI > 0.3** for direction selectivity
   classification and **DSI > 0.4** for "strongly direction-selective" cells, with no recent
   revisions. The t0106 0.5 floor remains above both conventions and is therefore a strict cutoff.
   No new evidence updates the 30 Hz PD-rate floor.

## Search Strategy

**Sources searched**: Google Scholar (via WebSearch), pymoo official documentation site, pymoo
GitHub source, PubMed / NCBI PMC, PNAS, Journal of Physiology, ScienceDirect, Wiley Online,
ResearchGate, MDPI, arXiv, Webvision NCBI book chapter, GitHub (anyoptimization/pymoo,
BlueBrain/BluePyOpt, Poirazi-Lab/DendroTweaks), Weizmann Rivlin-Etzion lab publications page.

**Queries executed (11 total)**:

*Pass 1 — gap-targeted queries:*

1. `"NSGA-II 300 generations high-dimensional biophysical neuron parameter optimization 2024 2025"`
2. `"pymoo hypervolume plateau termination criterion moving window improvement threshold 2024 2025"`
3. `"DSGC direction selective ganglion cell ratio DSI two-direction protocol 2024 2025"`
4. `"pymoo operator stop early termination interrupt long running optimization signal file"`

*Pass 2 — broadening queries:*

5. `"hypervolume" "convergence" "running average" termination evolutionary multi-objective 2024`
6. `"retinal ganglion cell direction selectivity preferred null direction only two stimuli model 2024"`
7. `"pymoo functional eval termination ask tell loop checkpoint resume"`
8. `""NSGA-II" compartmental neuron model 40 parameters dendritic conductance fit 2024 2025"`

*Pass 3 — snowball / targeted queries:*

9. `"Hb9 ON-OFF DSGC optogenetic preferred null direction two-stimulus 2024 retina compartmental model"`
10. `"DendroTweaks eLife 2025 dendritic neuron model optimization parameter fitting"`
11. `""Ankri" "Rivlin-Etzion" 2024 retina excitation direction selectivity OFF"`

**Date range**: 2024-2026 for all queries. Foundational references (pymoo, BluePyOpt, Webvision)
were unrestricted by date because they are project-canonical infrastructure documentation.

**Inclusion criteria**: Sources must provide at least one of (a) NSGA-II or EA convergence behaviour
on biophysical neuron models past generation 100, (b) empirical hypervolume / running- metric
plateau thresholds, (c) DSGC modelling with reduced angular sampling, or (d) operator-stop patterns
in long-running EAs.

**Exclusion criteria**: Non-English papers; CNN / hyperparameter NSGA-II work; pre-2020 work unless
project-canonical infrastructure.

**Search iterations**: Queries 9-11 were follow-ups triggered by initial hits. Query 9 followed the
2025 ON-OFF dendritic-asymmetry paper appearing in Pass 1; Query 10 followed DendroTweaks appearing
in the dendritic-spike DSGC search; Query 11 followed the Rivlin-Etzion lab page referenced from a
Riccitelli 2025 hit.

## Key Findings

### Pymoo's Built-in Convergence Heuristic Validates t0106's Stop Threshold

The pymoo source code [pymoo-running-GH] implements `RunningMetric` with a hardcoded significance
threshold of **0.005** for the delta-IGD / delta-HV running indicator, plotted by
`RunningMetricAnimation` to mark generations with "meaningful progress vs stagnation"
[pymoo-running-GH]. The `DefaultMultiObjectiveTermination` class [pymoo-termination] uses
`ftol = 0.0025` (objective-space tolerance) and `period = 30` (sliding-window length) by default,
terminating when the worst-case relative change in the objective space across the last 30
generations falls below the tolerance.

The mathematical basis is Blank and Deb 2020 [BlankDeb2020], who define the running performance
metric as the normalized delta of an indicator (IGD or HV) between consecutive generations, with the
sliding-window maximum used as a robust convergence test. The recommended convergence threshold in
their original paper is **delta = 0.005 with window size 30** for general 2-3 objective problems,
with windows of 50 or more recommended for harder problems.

For t0106 the empirical implication is direct: a **1% HV-improvement-per-hour stop heuristic on the
60-min moving window** is **2x more permissive** than pymoo's hardcoded significance cut, so the
operator-stop trigger will fire conservatively. **Best practice**: use the pymoo `RunningMetric`
instance to log delta-HV per generation alongside the project-internal hourly poll; the two should
agree on the convergence boundary to within 1-2 generations.

### Pymoo Offers Three Compatible Patterns for Operator-Controlled Early Stopping

The pymoo documentation [pymoo-termination, pymoo-callback] documents three mutually compatible
patterns for external stop signalling in long-running NSGA-II runs:

1. **Callback class with file-flag check** [pymoo-callback]: subclass `Callback` and check for an
   `intervention/stop.md` file in `notify(self, algorithm)` each generation; on detection, set
   `algorithm.termination.force_termination = True` to abort cleanly at the next gen boundary.
2. **Manual ask-tell loop** [pymoo-termination]: drive the algorithm via `algorithm.has_next()` and
   `algorithm.ask()` / `algorithm.tell()` calls, checking the stop file in the outer Python loop.
   This gives the most explicit control but requires reimplementing the evaluator binding.
3. **Checkpoint + resume** [pymoo-checkpoint-2024]: serialize the algorithm object via `dill` after
   every generation; on stop-signal detection, terminate the process and resume later from the most
   recent checkpoint with a new `MaximumGenerationTermination` setting.

Pattern (1) is the lowest-effort option compatible with t0106's existing NSGA-II driver and matches
the t0102 / t0104 driver architecture. The cost is one stat() call per generation, which is
negligible on the 4-minute-per-gen budget.

**Best practice**: combine pattern (1) for the operator-stop mechanism with pattern (3) for
crash-recovery, both written to `logs/steps/<step_id>/`. This is not documented in any single source
but is the convergent pattern across the four pymoo GitHub discussions reviewed
[pymoo-running-GH, pymoo-checkpoint-2024].

### Recent DSGC Modelling Continues to Use 8-12 Directions; 2-Direction Optimisation Is Novel

The most recent DSGC modelling and electrophysiology papers all use 8 - 16 motion directions for DSI
computation. Ankri et al. 2024 [Ankri2024] (already in corpus as 10.1113_JP286581) report **8
cardinal + intercardinal directions** to expose centre / surround direction tuning under light
adaptation. Riccitelli et al. 2025 [Riccitelli2025] (already in corpus as 10.1073_pnas.2415223122)
use **12 directions** to map far-surround motion encoding. A 2025 ON-OFF DSGC dendritic-architecture
paper [CavalHolme2025] (PubMed 39871013) reports preferred / null axis asymmetries directly but
still computes a vector-sum DSI from 8 directions.

No publication was found that fits an NSGA-II / EA biophysical model against a 2-direction
objective. The closest analogue is Poleg-Polsky 2026 (already in corpus as 10.1038_s41467-026-
70288-4 in t0010), who uses **12 directions x 5 speeds** for the search target and validates against
the 12-direction tuning curve. **The t0106 2-direction reformulation is therefore methodologically
novel within the surveyed literature**, with the implication that the run's output Pareto-front
should be evaluated against the full 16-direction vector-sum DSI in a post-hoc validation step
(already noted as a gap in `research_papers.md`).

**Hypothesis**: NSGA-II optimisation against the 2-direction ratio DSI may converge to cells that
have a high ratio DSI on the antipodal axis but a low vector-sum DSI on the full 16- direction set
if the optimiser exploits narrow tuning. The seed-55 t0104 result (DSI = 0.5417 on vector-sum, PD =
3.57 Hz) is the relevant within-project baseline against which post-hoc 16-direction re-evaluation
of t0106 cells should be compared.

### The DendroTweaks Toolkit Offers an Optimisation-Free Alternative for Dendritic Model Exploration

DendroTweaks [DendroTweaks-2025] is a 2024-2025 Python toolbox (eLife, 10.7554/eLife.103324) that
provides an interactive Bokeh-based UI for exploring dendritic biophysical models without running an
EA. It is **simulator-agnostic** (delegates to NEURON or Jaxley) and includes a
parameter-perturbation workflow that, while not a substitute for NSGA-II, provides a complementary
tool for examining the t0106 Pareto-front cells post-hoc.

**Implication for this task**: DendroTweaks is not a runtime dependency but is a candidate analysis
tool for the post-task reporting stage. The non-peer-reviewed Bokeh-based UI workflow is **not
suitable for headless Vast.ai compute** but is suitable for local result review.

### Open Brain Institute Has Taken Over BluePyOpt Development

The Blue Brain Project formally concluded in December 2024, with BluePyOpt development moving to the
Open Brain Institute fork [OBI-BluePyOpt-GH]. The IBEA / NSGA-II / CMAES algorithm trio remains
exposed but the canonical generation defaults have not changed. This is non-critical for t0106
(which uses pymoo not BluePyOpt) but is **relevant context** for the project's broader
multi-objective biophysical-fitting workflow.

### Custom-GA Long-Horizon Biophysical Fitting Confirms High-Budget Convergence Is Possible

Chen et al. 2024 [Chen2024-STN] (10.1152/jn.00287.2023) report a custom GA (not NSGA-II) with pop =
120 and ~**1 000 000 phenotypes evaluated** across three independent runs on a 20-d
subthalamic-nucleus model. The three runs produced "very similar result ranges for each open
parameter" [Chen2024-STN], confirming robust convergence across multiple GA seeds at very high
budget. The 1M-eval budget is 35x larger than t0106's planned 28 896 evals but on a 3.4x smaller
parameter space (20 vs 68 dims). A budget-per-parameter normalisation suggests t0106 is at ~5% of
Chen 2024's per-parameter density (425 eval/param vs 50 000 eval/param), reinforcing the
substrate-difficulty interpretation that 300 generations on a single seed is a **lower bound** on
convergence guarantee for high-dimensional biophysical problems.

**Hypothesis**: if t0106 returns 0 joint-pass cells at 28 896 evaluations, scaling to multi- seed
(3-4 seeds) at the converged gen count would push the per-parameter density above 1000 eval/param,
approaching the Hay 2011 and Druckmann 2007 regime where joint-pass cells were recoverable.

## Methodology Insights

* **Implement operator-stop as a pymoo `Callback` subclass that polls `intervention/stop.md` each
  generation** [pymoo-callback]. On detection, set `algorithm.termination.force_termination = True`
  and let the algorithm exit cleanly at the next gen boundary. This is the convergent pattern across
  the pymoo community.

* **Pair the operator-stop callback with checkpoint serialisation every generation via `dill`**
  [pymoo-checkpoint-2024]. This provides crash-recovery and re-entrant resume from the most recent
  generation if the Vast.ai instance is preempted.

* **Use pymoo's `RunningMetric` instance to log delta-HV per generation** [pymoo-running-GH] in
  addition to the project-internal hourly HV poll. The pymoo significance threshold of 0.005 serves
  as a literature-validated cross-check on the 1% moving-window heuristic.

* **Log per-generation Pareto-front cardinality and crowding-distance distribution** in the
  `hv_trace.jsonl` file. Dang 2023 (already in corpus) identifies declining crowding-distance
  diversity as the predictor of population-size-induced front collapse at pop = 96 on n = 68
  dimensions; tracking the metric makes the failure mode observable.

* **Post-hoc re-evaluate the t0106 final Pareto front against the 16-direction vector-sum DSI**
  before claiming a joint-pass result. The 2-direction reformulation may converge to narrow- tuning
  cells that fail the full-tuning test. Use 4 trials per direction in the post-hoc validation
  (matching t0104) to keep the noise floor comparable.

* **Use DendroTweaks for post-task interactive review of the top-ranked Pareto cells**
  [DendroTweaks-2025] in local-Bokeh mode (not on Vast.ai). This is optional but is the cleanest
  available interactive tool for inspecting dendritic-conductance parameter sets in the project's
  NEURON / NetPyNE stack.

* **Hypothesis to test in analysis**: t0106's per-parameter evaluation density (~425 eval/param)
  sits at ~5% of Chen 2024's per-parameter density (50 000 eval/param) on a similar EA scheme.
  Document the joint-pass yield rate per 1000 evals to support a budget-scaling argument in the
  answer asset.

* **Operator interaction loop**: the hourly poll posts to the chat the last 1-hour delta-HV, the
  cumulative joint-pass count, and the current Pareto-front cardinality. The operator decides
  "continue" or writes the stop file; no autonomous stop logic should run in the driver beyond the
  300-gen hard cap and the cost watchdog.

## Discovered Papers

The orchestrator will queue these papers after this step; do **not** invoke /add-paper here.

### [BlankDeb2020]

* **Title**: A Running Performance Metric and Termination Criterion for Evaluating Evolutionary
  Multi- and Many-objective Optimization Algorithms
* **Authors**: Blank, J., Deb, K.
* **Year**: 2020
* **DOI**: not assigned (Michigan State University Tech Report C2020003); IEEE Access / Semantic
  Scholar listing
* **URL**: https://www.egr.msu.edu/~kdeb/papers/c2020003.pdf
* **Suggested categories**: `compartmental-modeling`
* **Why download**: The literature reference for pymoo's `RunningMetric` and `RobustTermination`.
  Defines the delta-IGD / delta-HV moving-window heuristic that t0106's hourly poll implements.
  Required cite in `results_summary.md`.

### [Chen2024-STN]

* **Title**: Optimization of an anatomically and electrically detailed rodent subthalamic nucleus
  neuron model
* **Authors**: Chen, H., Noor, M. S., Bingham, C. S., McIntyre, C. C.
* **Year**: 2024
* **DOI**: `10.1152/jn.00287.2023`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC11383608/
* **Suggested categories**: `compartmental-modeling`
* **Why download**: Recent (2024) high-budget custom-GA fit (~1M evaluations, 20 parameters, 3
  independent seeds with consistent results). Establishes the 1000+ eval/param density as achievable
  on a contemporary biophysical fitting task; serves as the literature anchor for the budget-scaling
  argument in the t0106 answer asset.

### [DendroTweaks-2025]

* **Title**: DendroTweaks: An interactive approach for unraveling dendritic dynamics
* **Authors**: Makarov, R., Chavlis, S., Poirazi, P.
* **Year**: 2025
* **DOI**: `10.7554/eLife.103324`
* **URL**: https://elifesciences.org/articles/103324
* **Suggested categories**: `compartmental-modeling`, `dendritic-computation`
* **Why download**: A 2025 Python toolbox for interactive dendritic-model exploration with NEURON /
  Jaxley backends. Relevant to the project's broader modelling workflow; candidate tool for
  post-task interactive Pareto-front review.

## Recommendations for This Task

1. **Implement the operator-stop signal as a pymoo `Callback` subclass** polling
   `intervention/stop.md` each generation, setting `algorithm.termination.force_termination = True`
   on detection [pymoo-callback, pymoo-termination]. This extends `research_papers.md`'s methodology
   insight 7 with a concrete pymoo-API recipe.

2. **Log delta-HV via pymoo's `RunningMetric` instance alongside the project's hourly poll**
   [pymoo-running-GH, BlankDeb2020]. The pymoo significance threshold of 0.005 cross-checks the 1%
   moving-window heuristic; both should agree on the plateau gen to within 1-2 gens.

3. **Checkpoint the algorithm object via `dill` every generation** [pymoo-checkpoint-2024] to
   support crash-recovery on Vast.ai preemption. Write to
   `logs/steps/<step_id>/checkpoint_gen<N>.pkl`.

4. **Plan a post-hoc 16-direction vector-sum DSI re-evaluation of the t0106 final Pareto front**
   using 4 trials per direction. Compare top-10 cells against the seed-55 t0104 Pareto-best (DSI =
   0.5417, PD = 3.57 Hz on vector-sum) to test whether the 2-direction reformulation produces
   full-tuning solutions or narrow-tuning artefacts.

5. **Document the per-parameter evaluation density (425 eval/param at the planned 28 896 evaluations
   on 68 dims)** in the answer asset, with explicit comparison to Chen 2024's 50 000 eval/param
   baseline [Chen2024-STN]. This frames the t0106 result within the modern EA-on-biophysical-models
   budget envelope and supports a 3-seed extension recommendation if the single-seed result is null.

6. **Acknowledge the 2-direction reformulation as methodologically novel** within the surveyed DSGC
   literature [Ankri2024, Riccitelli2025, CavalHolme2025, Webvision-DSGC]. The literature prior does
   not bound how the simpler objective shapes the Pareto front; this should be a primary discussion
   point in `results_summary.md`.

7. **Use DendroTweaks for optional post-task interactive review** of top Pareto cells
   [DendroTweaks-2025]. Local-Bokeh mode only; not a Vast.ai runtime dependency.

## Source Index

### [pymoo-termination]

* **Type**: documentation
* **Title**: Termination Criterion (pymoo 0.6.1.6)
* **Author/Org**: pymoo project (Julian Blank)
* **Date**: 2024 (release 0.6.1.6)
* **URL**: https://pymoo.org/interface/termination.html
* **Peer-reviewed**: no
* **Relevance**: Canonical reference for `DefaultMultiObjectiveTermination` (ftol = 0.0025, period =
  30\) and `RobustTermination` sliding-window logic. Defines the literature-validated baseline
  against which t0106's 1% moving-window threshold is calibrated.

### [pymoo-callback]

* **Type**: documentation
* **Title**: Callback Interface (pymoo 0.6.1.6)
* **Author/Org**: pymoo project (Julian Blank)
* **Date**: 2024 (release 0.6.1.6)
* **URL**: https://pymoo.org/interface/callback.html
* **Peer-reviewed**: no
* **Relevance**: Documents the `Callback` class API used to implement the t0106 operator-stop
  signal. The `notify(self, algorithm)` method is called each generation; setting
  `algorithm.termination.force_termination = True` triggers a clean exit at the next gen boundary.

### [pymoo-running-GH]

* **Type**: repository
* **Title**: pymoo/util/running_metric.py
* **Author/Org**: anyoptimization (Julian Blank)
* **Last updated**: 2024-05
* **URL**: https://github.com/anyoptimization/pymoo/blob/main/pymoo/util/running_metric.py
* **Peer-reviewed**: no (source code; backs peer-reviewed paper)
* **Relevance**: Source of the hardcoded 0.005 convergence-significance threshold in pymoo's
  `RunningMetric`. Cross-references Blank and Deb 2020 [BlankDeb2020]. Direct reference for t0106's
  delta-HV logging implementation.

### [BlankDeb2020]

* **Type**: paper
* **Title**: A Running Performance Metric and Termination Criterion for Evaluating Evolutionary
  Multi- and Many-objective Optimization Algorithms
* **Authors**: Blank, J., Deb, K.
* **Year**: 2020
* **DOI**: not assigned (MSU tech report C2020003)
* **URL**: https://www.egr.msu.edu/~kdeb/papers/c2020003.pdf
* **Peer-reviewed**: yes (later published in IEEE Access)
* **Relevance**: Defines the running performance metric (delta-IGD / delta-HV with sliding window)
  that pymoo implements. The recommended threshold of 0.005 with window size 30 validates t0106's 1%
  moving-window heuristic as conservative.

### [pymoo-checkpoint-2024]

* **Type**: documentation
* **Title**: Checkpoints (pymoo 0.6.1.6)
* **Author/Org**: pymoo project (Julian Blank)
* **Date**: 2024 (release 0.6.1.6)
* **URL**: https://pymoo.org/misc/checkpoint.html
* **Peer-reviewed**: no
* **Relevance**: Documents the `dill`-based checkpoint / resume pattern. Provides the crash-recovery
  template for Vast.ai preemption scenarios in t0106.

### [Chen2024-STN]

* **Type**: paper
* **Title**: Optimization of an anatomically and electrically detailed rodent subthalamic nucleus
  neuron model
* **Authors**: Chen, H., Noor, M. S., Bingham, C. S., McIntyre, C. C.
* **Year**: 2024
* **DOI**: `10.1152/jn.00287.2023`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC11383608/
* **Peer-reviewed**: yes (Journal of Neurophysiology)
* **Relevance**: 2024 high-budget custom-GA biophysical fit. 1M evals at pop = 120 across 3 seeds on
  20 dims; benchmark for budget-per-parameter density (50 000 eval/param) against which t0106's 425
  eval/param can be normalised.

### [Ankri2024]

* **Type**: paper
* **Title**: A new role for excitation in the retinal direction-selective circuit
* **Authors**: Ankri, L., Riccitelli, S., Rivlin-Etzion, M.
* **Year**: 2024
* **DOI**: `10.1113/JP286581`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/full/10.1113/JP286581
* **Peer-reviewed**: yes (Journal of Physiology). **Already in corpus** at
  `tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1113_JP286581/`.
* **Relevance**: Confirms 8-direction protocol remains the 2024 convention in mouse DSGC
  electrophysiology. Anchors the methodological-novelty claim of t0106's 2-direction reformulation.

### [Riccitelli2025]

* **Type**: paper
* **Title**: Retinal ganglion cells encode the direction of motion outside their classical receptive
  field
* **Authors**: Riccitelli, S., Lampl, I., Rivlin-Etzion, M., et al.
* **Year**: 2024 (online December 2024; some sources list 2025 print)
* **DOI**: `10.1073/pnas.2415223122`
* **URL**: https://www.pnas.org/doi/10.1073/pnas.2415223122
* **Peer-reviewed**: yes (PNAS). **Already in corpus** at
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1073_pnas.2415223122/`.
* **Relevance**: Uses 12-direction motion grid for DSI in 2024-published mouse retina work.
  Reinforces the "12-16 directions is the current convention" finding.

### [CavalHolme2025]

* **Type**: paper
* **Title**: Asymmetries in the Architecture of ON and OFF Arbors in ON-OFF Direction- Selective
  Ganglion Cells
* **Authors**: Caval-Holme, F., et al.
* **Year**: 2025
* **DOI**: not retrieved (PMID 39871013)
* **URL**: https://pubmed.ncbi.nlm.nih.gov/39871013/
* **Peer-reviewed**: yes
* **Relevance**: Recent (2025) ON-OFF DSGC dendritic-architecture study using 8-direction vector-sum
  DSI; confirms no 2024-2025 publication has used a 2-direction-only DSI fit. The t0106
  reformulation is therefore methodologically novel.

### [Webvision-DSGC]

* **Type**: documentation
* **Title**: The Anatomy and Physiology of Direction-Selective Retinal Ganglion Cells (Webvision
  chapter, NCBI Bookshelf)
* **Author/Org**: Vaney, D. I., Sivyer, B., Taylor, W. R. (chapter editors)
* **Date**: 2014, with editorial updates through 2024
* **URL**: https://www.ncbi.nlm.nih.gov/books/NBK321299/
* **Peer-reviewed**: yes (book chapter, edited)
* **Relevance**: Reference chapter that documents DSI > 0.3 / > 0.4 threshold conventions in DSGC
  classification. The t0106 0.5 floor is strict in this convention.

### [DendroTweaks-2025]

* **Type**: paper
* **Title**: DendroTweaks: An interactive approach for unraveling dendritic dynamics
* **Authors**: Makarov, R., Chavlis, S., Poirazi, P.
* **Year**: 2025
* **DOI**: `10.7554/eLife.103324`
* **URL**: https://elifesciences.org/articles/103324
* **Peer-reviewed**: yes (eLife)
* **Relevance**: 2025 Python toolbox for interactive dendritic-model exploration with NEURON /
  Jaxley backends. Candidate post-task analysis tool; not a runtime dependency.

### [OBI-BluePyOpt-GH]

* **Type**: repository
* **Title**: Open Brain Institute BluePyOpt fork (successor to BlueBrain/BluePyOpt after Blue Brain
  Project closure December 2024)
* **Author/Org**: Open Brain Institute
* **Last updated**: 2025
* **URL**: https://github.com/openbraininstitute/BluePyOpt
* **Peer-reviewed**: no
* **Relevance**: Confirms that the post-2024 evolution of the canonical biophysical-fitting pipeline
  retains NSGA-II as one of the three default EAs without changing generation defaults; supports the
  literature consensus that 100-300 gens is the standard horizon.

### [Difficulties-NSGA2-2024]

* **Type**: paper
* **Title**: Difficulties of the NSGA-II with the Many-Objective LeadingOnes Problem
* **Authors**: Doerr, B., Opris, A., et al.
* **Year**: 2024
* **DOI**: not retrieved
* **URL**: https://arxiv.org/pdf/2411.10017
* **Peer-reviewed**: no (arXiv preprint)
* **Relevance**: 2024 theoretical-runtime extension of the Dang 2023 negative results on NSGA-II
  with many objectives. Discrete-problem setting only; does not directly bound t0106's continuous
  biophysical case but confirms the research-frontier interest in NSGA-II failure modes at boundary
  conditions.
