---
spec_version: "1"
task_id: "t0097_multi_obj_optim"
research_stage: "internet"
searches_conducted: 18
sources_cited: 42
papers_discovered: 21
date_completed: "2026-05-08"
status: "complete"
---
## Task Objective

Survey the published literature on multi-objective optimisation (MOO) of single-neuron compartmental
models and broaden the project's MOBO objective space beyond the DSI-plus-firing-rate pair used in
every prior optimisation task here (t0076, t0078, t0080, t0081, t0083, t0086, t0091). The internet
research stage closes the four canonical-objective gaps identified in `research_papers.md`
(information transfer rate, metabolic energy / ATP per spike, cytoplasm volume / wiring economy,
robustness / degeneracy) and the methodology gap (Druckmann, Achard & De Schutter, Van Geit /
NeuroFitter / BluePyOpt, NSGA-II / NSGA-III, eFEL). It produces a ranked catalogue of objective
functions that can be implemented on top of the project's existing pymoo NSGA-II loop without
infrastructure rewrites.

## Gaps Addressed

This section explicitly addresses every gap from the Gaps and Limitations section of
`research_papers.md`:

1. **No methodology paper on Druckmann-style multi-objective single-neuron optimisation in the
   corpus** — **Resolved**. Located the canonical methodology line: Druckmann et al. 2007
   [Druckmann2007] (the framework paper), Druckmann et al. 2011 [Druckmann2011] (the
   stimulus-protocol paper that became the eFEL reference application), Achard & De Schutter 2006
   [Achard2006] (first MOEA Purkinje fit and the parameter-landscape-as-hyperplanes finding), Van
   Geit et al. 2007 [VanGeit2007] (NeuroFitter, phase-plane trajectory density error metric), Van
   Geit et al. 2016 [VanGeit2016] (BluePyOpt, the project's de-facto methodology cousin), the
   BluePyOpt repository [BluePyOpt-GH] and its Read the Docs API [BluePyOpt-Docs]. Also located eFEL
   [eFEL-GH] and the systematic Allen-cell-types-database fits by Gouwens et al. 2018 [Gouwens2018]
   together with the AllenSDK biophysical-model docs [AllenSDK-Docs].

2. **No biological energy-budget paper in the corpus** — **Resolved**. Located the canonical
   energy-budget line: Attwell & Laughlin 2001 [Attwell2001] (the brain-grey-matter ATP budget,
   action potentials = 47% of signalling cost), Niven & Laughlin 2008 [Niven2008] (energy as a
   selective pressure on sensory-system evolution), Sengupta et al. 2010 [Sengupta2010] (action
   potential energy efficiency varies by neuron type, Na/K overlap as the controlling parameter),
   Carter & Bean 2009 [Carter2009] (sodium entry efficiency, fast-spiking GABAergic cells use 2x the
   theoretical minimum sodium), Hallermann et al. 2012 [Hallermann2012] (state and location
   dependence of metabolic cost — the Na/K charge-overlap recipe explicitly applied to a cortical
   pyramidal model), Niven et al. 2007 [Niven2007] (fly photoreceptor energy-information trade-off,
   the canonical bits-per-ATP Pareto curve).

3. **No robustness/degeneracy paper in the corpus** — **Resolved**. Located Marder & Goaillard
   2006 [Marder2006] (the canonical review of variability, compensation and homeostasis), Prinz,
   Bucher & Marder 2004 [Prinz2004] (20 million STG models showing similar network activity from
   disparate parameters — the empirical foundation for treating robustness as a population
   statistic), Goldman et al. 2001 [Goldman2001] (global structure / compensatory directions /
   activity-pattern manifold in a 5-conductance model), Olypher & Calabrese 2007 [Olypher2007]
   (implicit-function theorem framework for compensatory parameter manifolds — the formal
   mathematics underlying "neutral directions" in conductance space).

4. **No information-theory canon in the corpus** — **Resolved**. Located Strong et al. 1998
   [Strong1998] (the direct method and extrapolation correction for spike-train MI; the Bialek-group
   canonical paper), Borst & Theunissen 1999 [Borst1999] (the canonical review of information theory
   and neural coding in *Nature Neuroscience*), Brenner et al. 2000 [Brenner2000] (synergy in a
   neural code, joint-vs-marginal MI decomposition for spike pairs), Victor & Purpura 1997
   [Victor1997] (metric-space analysis of spike trains; provides spike-distance metrics that
   complement direct MI estimation), Koch 1999 [Koch1999] (the canonical single-neuron
   information-processing textbook for context).

5. **No wiring-cost / cytoplasm-volume measurement on real DSGC morphology** — **Partially
   resolved**. Located the canonical wiring-economy line: Cherniak 1992 [Cherniak1992] (Steiner-tree
   formalism, local volume optimisation as the dominant objective at branch junctions), Chklovskii
   et al. 2002 [Chklovskii2002] (cortex is wired so that wire occupies ~3/5 of grey-matter volume,
   matching the optimum predicted from minimising delays + attenuation + length), Wen & Chklovskii
   2006 [Wen2006] (relating arbor structure to function via wiring optimisation). DSGC-specific
   ground-truth remains unmeasured in the literature; the catalogue confirms that this is a genuine
   open question and that the project's existing DSGC morphologies make a measurement feasible as a
   side effect of implementing the cytoplasm-volume objective.

6. **Existing corpus is DSGC-dominated** — **Resolved by design**. The discovered-paper list below
   is deliberately broad: cerebellar Purkinje (Achard & De Schutter), STG / pyloric crustacean
   (Prinz, Marder & Goaillard, Goldman, Olypher & Calabrese), L5 cortical pyramidal (Druckmann, Hay
   already in corpus, Hallermann), fly photoreceptors (Niven, Anderson, Laughlin), MSO mammalian
   auditory brainstem (Remme), and Allen-mouse-V1 (Gouwens). The methodology line is cell-agnostic.

7. **No paper in the corpus uses both DSI and a non-DSI objective in a multi-objective Pareto
   setup** — **Partially resolved**. No paper directly pairs DSI with energy/wiring/robustness,
   but Remme et al. 2018 [Remme2018] is a strong precedent: it pairs *coincidence-detection
   function* with *energy* in MSO neurons and is methodologically the closest published analogue to
   the project's planned DSI-vs-energy MOBO. Treating Remme as the methodology template, a
   DSI-vs-energy experiment is a direct compositional generalisation.

## Search Strategy

**Sources searched**: Google Scholar, PubMed / PMC, PLOS journals (Computational Biology, Biology),
Frontiers (Neuroinformatics, Neuroscience), *Nature Communications* / *Nature Reviews Neuroscience*
/ *Nature Neuroscience*, *Journal of Neuroscience*, *Journal of Cerebral Blood Flow and Metabolism*,
*Journal of Experimental Biology*, *Physical Review Letters*, *IEEE Transactions on Evolutionary
Computation*, *Neural Computation*, GitHub (BlueBrain/BluePyOpt, BlueBrain/eFEL,
anyoptimization/pymoo), Read the Docs (BluePyOpt, AllenSDK, pymoo), ModelDB (citations and model
accessions), Semantic Scholar, ResearchGate.

**Queries executed** (18 total, exact text):

*Methodology line:*

1. `Druckmann 2007 "novel multiple objective optimization framework" conductance-based neuron models Frontiers Neuroscience`
2. `Achard De Schutter 2006 "complex parameter landscape" Purkinje cell evolutionary algorithm PLOS Computational Biology`
3. `Van Geit BluePyOpt 2016 Frontiers Neuroinformatics Bluepyopt python optimization neuron models`
4. `Van Geit Achard 2007 Neurofitter automated tuning neuron compartmental models software`
5. `Druckmann 2011 cortical pyramidal cell efeatures "evolutionary algorithm" eFEL multi-objective`
6. `Druckmann Berger Schurmann Hill Markram Segev 2011 "effective stimuli for constructing reliable neuron models" PLOS Computational Biology`
7. `Markram 2018 "systematic generation of biophysically detailed models for diverse cortical neuron types" Nature Communications`
8. `Deb 2002 NSGA-II "fast and elitist multiobjective genetic algorithm" IEEE Transactions Evolutionary Computation`
9. `Blank Deb 2020 pymoo "multi-objective optimization in python" IEEE Access`
10. `Deb Jain 2014 NSGA-III "evolutionary many-objective optimization algorithm using reference-point" IEEE Trans Evol Comput`
11. `Zitzler Thiele 1998 "multiobjective evolutionary algorithms comparative case study and the strength Pareto approach"`

*Energy / metabolic line:*

12. `Attwell Laughlin 2001 "energy budget for signaling in the grey matter of the brain" Journal Cerebral Blood Flow Metabolism`
13. `Niven Laughlin 2008 "energy limitation as a selective pressure on the evolution of sensory systems" Journal Experimental Biology`
14. `Sengupta 2010 "action potential energy efficiency varies among neuron types" PLOS Computational Biology Na K overlap`
15. `Carter Bean 2009 sodium potassium overlap action potential energy efficiency cortical neurons Neuron`
16. `Hallermann de Kock 2012 "state and location dependence of action potential metabolic cost" Nature Neuroscience cortical pyramidal`
17. `Niven Anderson Laughlin 2007 "fly photoreceptor energy bits per second" Current Biology information-energy trade-off`
18. `"function and energy consumption constrain neuronal biophysics" coincidence detection 2018 PLOS Computational Biology Mainen`
    *(returned Remme et al. 2018)*

*Robustness / degeneracy line:*

* `Marder Goaillard 2006 "Variability compensation and homeostasis in neuron and network function" Nature Reviews Neuroscience`
* `Prinz Bucher Marder 2004 "similar network activity from disparate circuit parameters" Nature Neuroscience`
* `Goldman Golowasch Marder Abbott 2001 "global structure robustness and modulation of neuronal models" Journal Neuroscience`
* `Olypher Calabrese 2007 "using constraints on neuronal activity to reveal compensatory changes in neuronal parameters" Journal Neurophysiology`

*Information theory line:*

* `Strong Koberle de Ruyter van Steveninck Bialek 1998 "entropy and information in neural spike trains" Physical Review Letters`
* `Borst Theunissen 1999 "information theory and neural coding" Nature Neuroscience review`
* `Brenner Strong Koberle Bialek de Ruyter 2000 "synergy in a neural code" Neural Computation`
* `"victor purpura" 1996 "spike train metrics" Network Computation Neural Systems metric-space spike timing`

*Wiring economy line:*

* `Chklovskii Schikorski Stevens 2002 "wiring optimization in cortical circuits" Neuron`
* `Cherniak 1992 "local optimization of neuron arbors" Biological Cybernetics dendritic tree minimum`
* `Wen Chklovskii 2008 "neuronal arbor optimization" "neuronal architecture" "wire-saving" dendrite axon volume`

*Codebase / Pareto-analysis surveys (WebFetch):*

* `https://github.com/BlueBrain/BluePyOpt` *(API surface, IBEA/DEAP integration, archive status)*
* `https://github.com/BlueBrain/eFEL` *(feature library, C++/Python split)*
* `https://bluepyopt.readthedocs.io/en/latest/index.html` *(modules and class layout)*
* `https://pymoo.org/` *(NSGA-II/-III/MOEA-D, hypervolume/IGD/GD+, mixed-variable, joblib parallel)*
* `"paretoset" OR "DEAP" OR "platypus" python pareto front non-dominated sorting library hypervolume indicator`

**Date range**: No restriction (canonical references span 1992-2025). Methodology codebase
documentation pulled May 2026.

**Inclusion criteria**: A source must satisfy at least one of (a) supplies a formula or
implementation recipe for one of the four must-find objective categories, (b) is a methodology
reference for multi-objective single-neuron compartmental fitting in NEURON or NEURON-compatible
code, (c) provides a Pareto-analysis primitive (NSGA-II/III, hypervolume, IGD) the project's pymoo
loop already uses, or (d) provides a published precedent for pairing a function objective with a
biological cost objective on a single compartmental neuron.

**Exclusion criteria**: Network-level optimisation (multi-neuron); reinforcement-learning or
deep-learning policy optimisation; phenomenological integrate-and-fire models without compartmental
structure; engineering MOO benchmarks unconnected to neuron modelling.

**Search iterations**: Queries 6-7, 14-18 and Remme/Olypher were follow-ups prompted by initial
results. Query 15 (Carter & Bean) was triggered by Sengupta et al.'s repeated citation of it as the
empirical anchor for Na/K overlap. Query 18 (Remme) was triggered by Sengupta et al.'s downstream
citation graph and surfaced the closest published analogue to the project's planned DSI-vs-energy
MOBO. The wiring-economy line was iterated last because [Cuntz2010] is already in the corpus and the
gap was explicitly the *missing* canonical ancestors.

## Key Findings

### Druckmann-Style Multi-Objective Methodology Is the Field's De-Facto Standard

[Druckmann2007] introduced the multi-objective evolutionary framework that every subsequent
methodology paper (including [Hay2011] already in the corpus) inherits, and the project's own
NSGA-II loop indirectly inherits via BluePyOpt-derived MOD files. The framework expresses every
electrophysiological feature (spike count, spike width, AHP depth, etc.) as an independent objective
whose target is the experimental mean and whose unit is the experimental SD; the optimiser returns
the Pareto front of feature combinations rather than a single best fit. [Druckmann2011]
[Druckmann2011] extends the framework with a stimulus-protocol design study showing that a
combination of step + ramp current injections provides the most informative constraints on
parameters. The [Druckmann2007] framework was operationalised first as NeuroFitter [VanGeit2007],
which combined NEURON with stochastic optimisation algorithms via a phase-plane-trajectory-density
error metric (insensitive to spike-time jitter), and then as **BluePyOpt** [VanGeit2016] which
became the field standard. BluePyOpt wraps DEAP and ships an IBEA selector by default; the
[BluePyOpt-GH] repository (archived Feb 2025; further development at the Open Brain Institute) and
the [BluePyOpt-Docs] documentation expose `bluepyopt.ephys.evaluators.CellEvaluator`,
`bluepyopt.ephys.protocols.StepProtocol`, and `bluepyopt.ephys.efeatures` as the canonical
evaluator/protocol/feature triple. eFEL [eFEL-GH] is the underlying C++ feature library (40.7% C++,
57.9% Python wrapper) supplying features such as `AP_amplitude`, `voltage_base`, `bpap_attenuation`
and `ais_initiation`. [Gouwens2018] applied the entire stack to **170 individual neurons** of the
Allen mouse V1 cell types database, fitting 10 active conductances per cell to electrophysiological
features under BluePyOpt — the largest published systematic application of the methodology. The
**AllenSDK biophysical-model documentation** [AllenSDK-Docs] confirms NEURON as the simulation
substrate, with both perisomatic-only and all-active model variants available.

**Best practice** from [VanGeit2016] / [Gouwens2018]: structure the optimisation as
`CellEvaluator(cell_model, params, protocols, fitness_calculator)` where `fitness_calculator`
returns one objective per `eFeature`; this matches the project's NSGA-II per-direction-DSI +
firing-rate evaluator pattern with minimal modification. **Hypothesis**: switching the project's
hand-written t0091 evaluator for BluePyOpt's `CellEvaluator` would preserve every objective the
project currently computes and add eFEL-derived features (spike threshold, AHP depth, etc.) as a
side-effect, enabling a Druckmann-style 20+ objective fit on the project's existing DSGC substrate.

### Achard & De Schutter 2006: Parameter Landscapes Are Loose Hyperplanes, Not Single Optima

[Achard2006] performed the first MOEA fit of a complex (Purkinje) cell with 24 free conductance
densities. Using an evolution strategy and a phase-plane fitness function, they obtained **20 very
different models** all reproducing the experimental firing pattern — including the fine details of
the complex spike. The **parameter landscape of acceptable solutions is a set of loosely connected
hyperplanes**, not a single basin. **Best practice**: grid search and random search will miss these
hyperplanes; only directed search (evolutionary or gradient-based with diversity preservation)
recovers them. **Hypothesis**: the project's t0091 NSGA-II run on 68-d morphology + channels will
produce a hyperplane structure analogous to [Achard2006]'s; the project should report this structure
explicitly (e.g., PCA of the Pareto-acceptable ensemble) rather than reporting only the
hypervolume-maximising point. This is consistent with [Hay2011]'s ensemble-as-experiment pattern
already in `research_papers.md`.

### Energy as a Selectable Pressure: Attwell-Laughlin Budget and ATP-per-Spike Recipes

[Attwell2001] derived the canonical energy budget for cortical signalling using stoichiometric
Na+/K+/Ca2+ accounting on the rat grey-matter neuron: **action potentials consume 47% of total
signalling ATP, postsynaptic glutamate effects 34%, resting potential 13%, glutamate recycling 3%**.
[Niven2008] elevates this from a budget to a selective pressure: across sensory systems, evolution
demonstrably reduces metabolic cost subject to functional constraints. [Niven2007] supplies the
clearest empirical Pareto curve in the literature: across four fly species, photoreceptor
information rates from **200 bits/s (D. melanogaster) to 1000 bits/s (S. carnaria)** scale
super-linearly with ATP cost, with a fixed cost of **~20% of maximum consumption** — a
bits-per-ATP Pareto front is *measurable in the same cell type across species*.

[Sengupta2010] makes the recipe operational: ATP per spike = (Na+ influx during AP) / 3, where the
factor 3 reflects three Na+ ions exchanged per ATP by the Na+/K+ pump. The neuron's **Na/K-current
overlap** during the AP controls the multiplier above the theoretical minimum: in mammalian cortical
pyramidal cells the overlap is small (~25% above minimum, [Carter2009]); in fast-spiking cerebellar
Purkinje cells and cortical interneurons the overlap is large (~100% above minimum, [Carter2009]).
[Hallermann2012] applies the recipe at compartment level in a cortical pyramidal NEURON model: AIS
and nodes of Ranvier have the highest cost-per-area, but backpropagation into dendrites and axon
collaterals dominates total cell energy consumption. **Best practice** for the project's catalogue:
compute ATP-per-spike per compartment by integrating Na+ inward current `INa` over each AP and
dividing by 3; sum over compartments per trial; report total ATP per direction and total ATP per
spike. **Hypothesis**: the DSGC's GABAergic-style fast-spiking behaviour ([Carter2009] family)
implies the cell already pays a high Na/K-overlap penalty, so a DSI-vs-energy Pareto front should
expand toward dramatically lower energy as Na+ density and overlap are jointly reduced — at the
cost of DSI sharpness.

[Remme2018] is the **methodologically closest published analogue** to the project's planned
DSI-vs-energy experiment: in mammalian MSO coincidence-detector neurons, function (coincidence
detection accuracy) and energy (Attwell-Laughlin-style ATP per AP integrated across compartments)
are jointly optimised in a conductance-based NEURON model, and the Pareto front predicts optimal
ranges for cell morphology and membrane properties. **The MSO coincidence-detection precedent
generalises directly to the DSGC direction-selectivity computation.** This contradicts no finding in
`research_papers.md`; it provides a methodology template the corpus did not previously contain.

### Robustness / Degeneracy Is Best Treated as a Population Statistic

[Prinz2004] simulated **20 million** versions of the three-cell crustacean pyloric network with
combinatorial channel-density and synapse-strength variation, finding "virtually indistinguishable
network activity from widely disparate sets of underlying mechanisms" — the empirical foundation
for the modern view that there is no single best parameter set, only a *manifold* of acceptable
sets. [Marder2006] is the canonical synthesis: variability across animals + compensation across
parameters + homeostasis across time produce stable function from inherently variable parts.
[Goldman2001] showed that even a small (5-conductance) neuron model has **directions in parameter
space** along which the activity pattern is invariant ("compensatory directions"). [Olypher2007]
gives the formal mathematics: by the implicit-function theorem, the manifold of parameter sets
producing fixed activity characteristics has codimension equal to the number of independent fixed
characteristics, and locally these manifolds are smooth.

For the catalogue's `robustness_under_perturbation` objective the recipe is: at each Pareto point,
sample +/- 10% (or +/- 20%) Gaussian or uniform perturbations of all channel densities (Marder-style
ensemble); recompute DSI for each perturbed sample; report the standard deviation (or the fraction
of samples whose DSI drops below a threshold) as the robustness objective. **Best practice** from
[Prinz2004] and [Goldman2001]: report robustness as a population statistic across an ensemble of
perturbations rather than a single sensitivity number; the [Olypher2007] formal framework provides
the principled choice of which directions to perturb. **Hypothesis**: a Pareto front jointly
optimising DSI vs robustness (DSI-stability under +/- 10% channel-density perturbation) on the
project's DSGC substrate will recover [Goldman2001]'s compensatory-direction structure automatically
— the highest-DSI / highest-robustness corner will lie along the compensatory hyperplane rather
than at a parameter-space extreme.

### Information Transfer Rate: Strong-Bialek Direct Method and Bias-Corrected Estimators

[Strong1998] introduced the **direct method** for estimating mutual information (MI) between
stimulus and spike train: discretise the spike train into binary words of length T at resolution dt,
compute the empirical word distribution, take the entropy, subtract a noise-entropy estimate at each
fixed stimulus, and **extrapolate to infinite data length** using a 1/T linear regression to correct
for finite-data bias. The fly H1 motion-sensitive neuron measurements topped out at **90 bits/s —
within a factor of 2 of the spike-train entropy ceiling**. [Borst1999] is the canonical
neuroscience-readers' review of information theory and neural coding; [Brenner2000] extends the
direct method to spike pairs and demonstrates that pairs close in time carry more than 2x the
information of single spikes (positive synergy in the H1 code).

For the project's t0091-style 8-direction trial-output format, the recommended recipe is: bin spike
counts in 25-50 ms windows over the trial; treat the 8-way stimulus direction as the discrete input
class; estimate H(spike-count vector | direction) via a direct method per direction; subtract from
H(spike-count vector across all directions); apply Strong's 1/T extrapolation correction *or* a
Panzeri-Treves NSB Bayesian-bias correction (which works better for short data). [Victor1997]
supplies an alternative path: compute the Victor-Purpura cost-distance between spike trains, then
treat the inter-class median distance / intra-class median distance ratio as a discrimination metric
— this avoids binning artefacts but is not directly an MI value. **Hypothesis**: the [Dhingra2004]
result already in the corpus (~60% gray-level loss spikes-vs-graded-potential) gives a
within-cell-type calibration anchor for the project's recipe; if the Strong-style estimate on the
project's DSGC trial output recovers comparable loss between graded-potential MI (HH off, EPSP/IPSP
trio) and spike-train MI (HH on), the recipe is validated. [Koch1999] supplies the textbook context
tying single-cell information capacity to cable theory.

### Wiring Economy: 3/5 Volume Rule and the Cytoplasm-Volume Recipe

[Cherniak1992] established that local branch-junction geometry minimises **volume**, not length, at
finer-than-segment scale. [Chklovskii2002] extended this to a quantitative cortical-circuit
prediction: minimising delays + cable attenuation + wire length predicts that wire (axons +
dendrites) should occupy **3/5 of grey-matter volume**, and direct measurement of cortical tissue
matches this ratio. [Wen2006] formalises the link between wiring optimisation and arbor structure /
function. Together with [Cuntz2010] (already in corpus), these references ground the
cytoplasm-volume objective biologically: cytoplasm is not just a regulariser, it is one half of an
evolutionarily-tuned trade-off the cell faces against conduction time and computational fidelity.

The catalogue's `cytoplasm_volume` recipe is unchanged from `research_papers.md`: sum over NEURON
sections of `pi * r^2 * L` after discretising every section to <= 20 um per compartment. **Best
practice**: pair every dendritic-computation objective (DSI, MI, coincidence, etc.) with at least
one wiring-economy cost objective so the optimiser cannot escape by inflating the morphology
arbitrarily — this is the rule [LondonHausser2005] (in the existing corpus) implies and that
[Chklovskii2002] makes evolutionarily explicit. **Hypothesis**: a Pareto front jointly optimising
DSI against cytoplasm volume on the project's procedurally generated DSGC morphologies will
qualitatively match [Cuntz2010]'s `bf in [0.2, 0.7]` band — the high-DSI corner will lie at
biologically realistic cytoplasm densities, not at degenerate extremes.

### NSGA-II / NSGA-III via pymoo Is the Right Optimiser for This Project

[Deb2002] established NSGA-II as the canonical fast-and-elitist Pareto sorting algorithm with
O(MN^2) complexity, where M is the number of objectives and N the population size. [Deb2014]
extended it to NSGA-III for many-objective problems (>3 objectives) using reference-point-based
nondominated sorting, which is necessary when scaling beyond ~3 objectives because crowding distance
becomes ineffective. [Zitzler1999] established the SPEA family and the comparative-study methodology
that drives the field's empirical-benchmark practice. [Blank2020] ships pymoo, the project's
optimiser, and exposes **NSGA-II, NSGA-III, R-NSGA-III, U-NSGA-III, MOEA/D, AGE-MOEA, AGE-MOEA2,
RVEA, SMS-EMOA**; performance indicators **GD, GD+, IGD, IGD+, Hypervolume, KKTPM**; and joblib +
GPU parallelisation through pymoo Read the Docs [pymoo-Docs]. The complementary Python ecosystem
includes **DEAP** [DEAP-Docs] (the underlying selector library BluePyOpt wraps), **Platypus**
(multi-objective-focused engineering library), and **paretoset** [paretoset-PyPI] (lightweight
non-dominated-set utility for post-hoc analysis).

**Best practice** from [Deb2014] / [Blank2020]: switch from NSGA-II to NSGA-III when the catalogue
exceeds 3 objectives (the planned DSI + energy + cytoplasm + robustness + MI Pareto would be 5
objectives, so NSGA-III is mandatory); use hypervolume as the primary convergence indicator with a
fixed reference point above the worst observed values per objective. **Hypothesis** (extending
`research_papers.md`): the NSGA-II vs qLogNEHVI [Ament2023] decision in the corpus is supplemented
here by a third option — **NSGA-III for >3-objective settings** — which is what the project will
need once the catalogue is operationalised. The [Ament2023] qLogNEHVI advantage is restricted to
low-d (<= 20) constrained problems; NSGA-II is right for high-d 2-3 objective problems; NSGA-III is
right for high-d many-objective problems. The project's catalogue lives in the third regime.

## Methodology Insights

* **Use BluePyOpt's `CellEvaluator(cell_model, params, protocols, fitness_calculator)` pattern as
  the structural template for the catalogue's evaluator** [VanGeit2016] [BluePyOpt-Docs]. Keep the
  project's existing pymoo loop as the optimiser (BluePyOpt itself is built on DEAP/IBEA, but the
  evaluator/protocol/feature triple is library-agnostic and directly portable to pymoo). This
  preserves the t0091 NSGA-II workflow while gaining eFEL-feature compatibility.

* **Adopt eFEL [eFEL-GH] as the feature-extraction substrate** for any catalogued objective that
  reduces to a per-spike or per-trace feature (spike count, AP amplitude, AHP depth, ISI CV, voltage
  base, etc.). For directional / information / energy / volume objectives, supply a custom feature;
  for everything else, eFEL has it.

* **Adopt NSGA-III via pymoo for >3-objective catalogue runs** [Deb2014] [Blank2020]. The
  catalogue's planned 5-way DSI + MI + energy + volume + robustness Pareto exceeds NSGA-II's
  effective range. NSGA-III's reference-point structure also gives the operator explicit control
  over which Pareto regions are preferentially sampled — important when the runtime budget per
  evaluation is heavy.

* **Compute ATP per spike as `int(INa) dt / 3` per compartment per AP, summed over compartments**
  [Sengupta2010] [Carter2009] [Hallermann2012]. The factor 3 reflects the Na/K-ATPase stoichiometry.
  Use NEURON's `INa` recording per section (already implemented in the project's EPSP/IPSP/FULL trio
  for HH-on traces) and integrate over each AP window. Validate the recipe against [Carter2009]'s
  25%/100%-above-minimum benchmarks on the project's existing HH model.

* **Compute information transfer rate via Strong-Bialek direct method with 1/T extrapolation**
  [Strong1998]. For the project's 8-direction, 1400-ms trial: bin spikes at dt = 5 ms, build binary
  words of length T = 25-100 ms, repeat across many trials per direction, estimate H(spike word |
  direction) and H(spike word) by counting, take the difference, repeat at multiple T values, fit a
  1/T regression and take the intercept. Apply Panzeri-Treves NSB correction as a second estimator
  for cross-validation.

* **Compute robustness as the standard deviation (or below-threshold fraction) of DSI under +/- 10%
  random perturbation of all channel densities** [Prinz2004] [Goldman2001] [Olypher2007]. Use a
  Monte Carlo sample of size 50-200 around each Pareto point. Report the full distribution, not just
  the SD, in the final analysis stage.

* **Compute cytoplasm volume as `sum_compartments(pi * r^2 * L)` after enforcing <= 20 um
  compartmentation** [Hines1997] [Cherniak1992] [Chklovskii2002] [Cuntz2010]. Validate mesh-density
  invariance by comparing 20 um and 10 um discretisations. The project's existing morphology
  generator already exposes `r` and `L` per section, so the recipe is a one-line addition.

* **Pair every function objective with at least one biological-cost objective** [LondonHausser2005]
  [Chklovskii2002] [Cuntz2010]. The dendritic-computation literature converges on this pairing rule
  because lone function objectives admit non-physical solutions (the project's recurring concern
  with pure-DSI maximisation). The catalogue's recommended pairs: DSI vs cytoplasm volume, DSI vs
  ATP-per-spike, MI vs ATP-per-spike, DSI vs robustness, MI vs cytoplasm volume.

* **Report the Pareto-acceptable ensemble, not a single best fit** [Hay2011] [Achard2006]
  [Prinz2004]. Use PCA / clustering on the ensemble parameter distribution to expose
  compensatory-direction structure [Goldman2001] [Olypher2007]. This is the canonical reporting
  pattern in the field and the natural extension of the project's existing Pareto-front reporting.

* **Per-objective experimental-SD normalisation when SDs are available** [Druckmann2007] [Hay2011].
  For objectives without an experimental SD (cytoplasm volume on a procedurally generated morphology
  has no experimental SD per se), use a best-effort biological tolerance band; for ATP-per-spike,
  use the Sengupta et al. cross-cell-type range as the tolerance.

* **Use hypervolume as the primary convergence indicator** [Blank2020] [Zitzler1999]; supplement
  with IGD when a reference Pareto front is available [Deb2014]. The pymoo `pymoo.indicators.hv.HV`
  and `pymoo.indicators.igd.IGD` classes are drop-in.

## Discovered Papers

The following papers are not yet in the project's corpus and should be downloaded / catalogued. The
orchestrator will spawn `/add-paper` for each.

### [Druckmann2007]

* **Title**: A novel multiple objective optimization framework for constraining conductance-based
  neuron models by experimental data
* **Authors**: Druckmann, S., Banitt, Y., Gidon, A., Schuermann, F., Markram, H., Segev, I.
* **Year**: 2007
* **DOI**: `10.3389/neuro.01.1.1.001.2007`
* **URL**:
  <https://www.frontiersin.org/journals/neuroscience/articles/10.3389/neuro.01.1.1.001.2007/full>
* **Suggested categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Why download**: The canonical multi-objective methodology paper for conductance-based
  single-neuron models. Establishes the per-feature SD-normalisation and Pareto-front-of-features
  framework that every subsequent paper (including [Hay2011] in corpus) inherits.

### [Druckmann2011]

* **Title**: Effective stimuli for constructing reliable neuron models
* **Authors**: Druckmann, S., Berger, T. K., Schuermann, F., Hill, S., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002133`
* **URL**: <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002133>
* **Suggested categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Why download**: Stimulus-protocol design study showing step + ramp combinations best constrain
  conductance-based models. Direct precursor of eFEL feature design.

### [Achard2006]

* **Title**: Complex parameter landscape for a complex neuron model
* **Authors**: Achard, P., De Schutter, E.
* **Year**: 2006
* **DOI**: `10.1371/journal.pcbi.0020094`
* **URL**: <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.0020094>
* **Suggested categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Why download**: First MOEA fit of a complex Purkinje model with 24 free conductances. The
  parameter-landscape-as-loose-hyperplanes finding directly informs how the project should report
  its NSGA-II Pareto-acceptable ensemble.

### [VanGeit2007]

* **Title**: Neurofitter: a parameter tuning package for a wide range of electrophysiological neuron
  models
* **Authors**: Van Geit, W., Achard, P., De Schutter, E.
* **Year**: 2007
* **DOI**: `10.3389/neuro.11.001.2007`
* **URL**:
  <https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/neuro.11.001.2007/full>
* **Suggested categories**: `compartmental-modeling`
* **Why download**: First parameter-tuning package interfacing NEURON with stochastic optimisation.
  Phase-plane-trajectory-density error metric is jitter-insensitive and may be useful for the
  project's stochastic-input simulations.

### [VanGeit2016]

* **Title**: BluePyOpt: leveraging open source software and cloud infrastructure to optimise model
  parameters in neuroscience
* **Authors**: Van Geit, W., Gevaert, M., Chindemi, G., Roessert, C., Courcol, J.-D., Muller, E.,
  Schuermann, F., Segev, I., Markram, H.
* **Year**: 2016
* **DOI**: `10.3389/fninf.2016.00017`
* **URL**:
  <https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2016.00017/full>
* **Suggested categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Why download**: The canonical multi-objective optimisation toolchain in the field. The
  CellEvaluator/Protocol/EFeature triple is the structural template the project's catalogue should
  adopt.

### [Gouwens2018]

* **Title**: Systematic generation of biophysically detailed models for diverse cortical neuron
  types
* **Authors**: Gouwens, N. W., Berg, J., Feng, D., Sorensen, S. A., Zeng, H., Hawrylycz, M. J.,
  Koch, C., Arkhipov, A.
* **Year**: 2018
* **DOI**: `10.1038/s41467-017-02718-3`
* **URL**: <https://www.nature.com/articles/s41467-017-02718-3>
* **Suggested categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Why download**: Largest published systematic application of BluePyOpt-style optimisation — 170
  individual mouse V1 neurons fit to electrophysiological features. Establishes the field's
  high-throughput Druckmann-methodology benchmark.

### [Attwell2001]

* **Title**: An energy budget for signaling in the grey matter of the brain
* **Authors**: Attwell, D., Laughlin, S. B.
* **Year**: 2001
* **DOI**: `10.1097/00004647-200110000-00001`
* **URL**: <https://journals.sagepub.com/doi/10.1097/00004647-200110000-00001>
* **Suggested categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Why download**: Canonical brain energy budget. Establishes the stoichiometric Na+/K+/Ca2+
  framework for translating ionic flux into ATP cost — the foundation of the catalogue's
  metabolic-energy-per-spike recipe.

### [Niven2008]

* **Title**: Energy limitation as a selective pressure on the evolution of sensory systems
* **Authors**: Niven, J. E., Laughlin, S. B.
* **Year**: 2008
* **DOI**: `10.1242/jeb.017574`
* **URL**: <https://journals.biologists.com/jeb/article/211/11/1792/9506>
* **Suggested categories**: `voltage-gated-channels`, `retinal-ganglion-cell`
* **Why download**: Establishes energy as a selective pressure (not just a budget). Justifies
  treating ATP-per-spike as a hard biological objective rather than a soft regulariser.

### [Sengupta2010]

* **Title**: Action potential energy efficiency varies among neuron types in vertebrates and
  invertebrates
* **Authors**: Sengupta, B., Stemmler, M., Laughlin, S. B., Niven, J. E.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000840`
* **URL**: <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000840>
* **Suggested categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Why download**: Operationalises ATP-per-spike via Na/K-current overlap. Directly supplies the
  catalogue's metabolic-energy recipe and establishes that overlap can be a 10x energy multiplier.

### [Carter2009]

* **Title**: Sodium entry during action potentials of mammalian neurons: incomplete inactivation and
  reduced metabolic efficiency in fast-spiking neurons
* **Authors**: Carter, B. C., Bean, B. P.
* **Year**: 2009
* **DOI**: `10.1016/j.neuron.2009.12.011`
* **URL**: <https://www.sciencedirect.com/science/article/pii/S0896627309010010>
* **Suggested categories**: `voltage-gated-channels`
* **Why download**: Empirical anchor for the Na/K-overlap metric. Shows fast-spiking GABAergic cells
  use 2x the theoretical-minimum sodium — the calibration benchmark for the project's
  ATP-per-spike recipe.

### [Hallermann2012]

* **Title**: State and location dependence of action potential metabolic cost in cortical pyramidal
  neurons
* **Authors**: Hallermann, S., de Kock, C. P. J., Stuart, G. J., Kole, M. H. P.
* **Year**: 2012
* **DOI**: `10.1038/nn.3132`
* **URL**: <https://www.nature.com/articles/nn.3132>
* **Suggested categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Why download**: Applies the Na/K-overlap recipe at compartment level in a NEURON pyramidal
  model. Direct methodology template for the project's per-compartment ATP integration.

### [Niven2007]

* **Title**: Fly photoreceptors demonstrate energy-information trade-offs in neural coding
* **Authors**: Niven, J. E., Anderson, J. C., Laughlin, S. B.
* **Year**: 2007
* **DOI**: `10.1371/journal.pbio.0050116`
* **URL**: <https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.0050116>
* **Suggested categories**: `voltage-gated-channels`, `retinal-ganglion-cell`
* **Why download**: The canonical empirical bits-per-ATP Pareto curve in the literature (200-1000
  bits/s across fly species; super-linear cost-vs-information). Sets the empirical baseline against
  which the project's DSI-vs-information-vs-energy front can be benchmarked.

### [Remme2018]

* **Title**: Function and energy consumption constrain neuronal biophysics in a canonical
  computation: coincidence detection
* **Authors**: Remme, M. W. H., Rinzel, J., Schreiber, S.
* **Year**: 2018
* **DOI**: `10.1371/journal.pcbi.1006612`
* **URL**: <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006612>
* **Suggested categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Why download**: Methodologically the closest published analogue to the project's planned
  DSI-vs-energy MOBO. Pairs MSO coincidence-detection function with Attwell-Laughlin-style energy in
  a NEURON conductance-based model and recovers the Pareto front of cell properties.

### [Marder2006]

* **Title**: Variability, compensation and homeostasis in neuron and network function
* **Authors**: Marder, E., Goaillard, J.-M.
* **Year**: 2006
* **DOI**: `10.1038/nrn1949`
* **URL**: <https://www.nature.com/articles/nrn1949>
* **Suggested categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Why download**: Canonical review of robustness / compensation / homeostasis. Justifies treating
  the project's robustness objective as a population statistic over a parameter manifold rather than
  a single sensitivity number.

### [Prinz2004]

* **Title**: Similar network activity from disparate circuit parameters
* **Authors**: Prinz, A. A., Bucher, D., Marder, E.
* **Year**: 2004
* **DOI**: `10.1038/nn1352`
* **URL**: <https://www.nature.com/articles/nn1352>
* **Suggested categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Why download**: Empirical foundation of the manifold-of-acceptable-solutions view. The
  20-million-parameter STG database is the methodological template for the project's Marder-style
  DSI-stability robustness objective.

### [Goldman2001]

* **Title**: Global structure, robustness, and modulation of neuronal models
* **Authors**: Goldman, M. S., Golowasch, J., Marder, E., Abbott, L. F.
* **Year**: 2001
* **DOI**: `10.1523/JNEUROSCI.21-14-05229.2001`
* **URL**: <https://www.jneurosci.org/content/21/14/5229>
* **Suggested categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Why download**: Compensatory-direction analysis on a 5-conductance model. Mathematical and
  empirical underpinning for reporting the project's DSI-vs-robustness Pareto front along
  compensatory hyperplanes rather than along arbitrary parameter axes.

### [Olypher2007]

* **Title**: Using constraints on neuronal activity to reveal compensatory changes in neuronal
  parameters
* **Authors**: Olypher, A. V., Calabrese, R. L.
* **Year**: 2007
* **DOI**: `10.1152/jn.00842.2007`
* **URL**: <https://pubmed.ncbi.nlm.nih.gov/17855581/>
* **Suggested categories**: `compartmental-modeling`
* **Why download**: Implicit-function-theorem framework for the dimension and structure of parameter
  manifolds compatible with fixed activity. Formal justification for the Marder-style perturbation
  recipe and for [Goldman2001]'s compensatory-direction analysis.

### [Strong1998]

* **Title**: Entropy and information in neural spike trains
* **Authors**: Strong, S. P., Koberle, R., de Ruyter van Steveninck, R. R., Bialek, W.
* **Year**: 1998
* **DOI**: `10.1103/PhysRevLett.80.197`
* **URL**: <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.80.197>
* **Suggested categories**: `retinal-ganglion-cell`, `compartmental-modeling`
* **Why download**: Canonical direct method + 1/T extrapolation correction for spike-train MI.
  Directly supplies the catalogue's information-transfer-rate recipe; the methodological reference
  for any rigorous MI estimate from a finite-trial neural recording.

### [Borst1999]

* **Title**: Information theory and neural coding
* **Authors**: Borst, A., Theunissen, F. E.
* **Year**: 1999
* **DOI**: `10.1038/14731`
* **URL**: <https://www.nature.com/articles/nn1199_947>
* **Suggested categories**: `retinal-ganglion-cell`, `compartmental-modeling`
* **Why download**: The canonical neuroscience-readers' review of information theory and neural
  coding. Useful as the introductory framing reference for the catalogue's MI section.

### [Brenner2000]

* **Title**: Synergy in a neural code
* **Authors**: Brenner, N., Strong, S. P., Koberle, R., Bialek, W., de Ruyter van Steveninck, R. R.
* **Year**: 2000
* **DOI**: `10.1162/089976600300015259`
* **URL**: <https://direct.mit.edu/neco/article-abstract/12/7/1531/6387>
* **Suggested categories**: `retinal-ganglion-cell`, `compartmental-modeling`
* **Why download**: Extends Strong et al. to spike-pair coding with explicit synergy decomposition.
  Useful when the project's DSGC trial output is rich enough to compute pair-MI as a refined
  information objective.

### [Chklovskii2002]

* **Title**: Wiring optimization in cortical circuits
* **Authors**: Chklovskii, D. B., Schikorski, T., Stevens, C. F.
* **Year**: 2002
* **DOI**: `10.1016/S0896-6273(02)00679-7`
* **URL**: <https://www.sciencedirect.com/science/article/pii/S0896627302006797>
* **Suggested categories**: `cable-theory`, `compartmental-modeling`, `dendritic-computation`
* **Why download**: Quantitative cortical-circuit wiring-optimisation prediction (3/5-volume rule).
  Evolutionary justification for the catalogue's cytoplasm-volume objective and for the
  function-objective + cost-objective pairing rule.

## Optional Discovered Papers (Lower Priority)

These five additional references are catalogued for completeness but ranked behind the 21 primary
discoveries above. They should be downloaded only if budget permits or if specific catalogue
sections require them.

### [Cherniak1992]

* **Title**: Local optimization of neuron arbors
* **Authors**: Cherniak, C.
* **Year**: 1992
* **DOI**: `10.1007/BF00204115`
* **URL**: <https://link.springer.com/article/10.1007/BF00204115>
* **Suggested categories**: `cable-theory`, `dendritic-computation`
* **Why download**: Establishes Steiner-tree formalism for neuron arbors and that local volume
  minimisation dominates over length / surface / speed at branch junctions. Historical anchor for
  the cytoplasm-volume objective.

### [Wen2006]

* **Title**: Wiring optimization can relate neuronal structure and function
* **Authors**: Wen, Q., Chklovskii, D. B.
* **Year**: 2006
* **DOI**: `10.1073/pnas.0506806103`
* **URL**: <https://www.pnas.org/doi/10.1073/pnas.0506806103>
* **Suggested categories**: `cable-theory`, `dendritic-computation`
* **Why download**: Connects wiring-optimisation theory to specific dendritic / axonal arbor
  structure-function relationships. Useful supplement to [Chklovskii2002] for the catalogue's
  cytoplasm-volume biological-justification section.

### [Victor1997]

* **Title**: Metric-space analysis of spike trains: theory, algorithms and application
* **Authors**: Victor, J. D., Purpura, K. P.
* **Year**: 1997
* **DOI**: `10.1088/0954-898X_8_2_003`
* **URL**: <https://www.tandfonline.com/doi/abs/10.1088/0954-898X_8_2_003>
* **Suggested categories**: `retinal-ganglion-cell`, `compartmental-modeling`
* **Why download**: Spike-distance metrics that complement direct MI estimation. Useful when MI
  estimation is bias-prone (short-data regime) or as a binning-free discrimination measure.

### [Deb2002]

* **Title**: A fast and elitist multiobjective genetic algorithm: NSGA-II
* **Authors**: Deb, K., Pratap, A., Agarwal, S., Meyarivan, T.
* **Year**: 2002
* **DOI**: `10.1109/4235.996017`
* **URL**: <https://ieeexplore.ieee.org/document/996017/>
* **Suggested categories**: `compartmental-modeling`
* **Why download**: Canonical NSGA-II reference. The project's pymoo NSGA-II loop already implements
  this algorithm; the citation is needed for any methodology section referencing the optimiser's
  complexity, crowding distance, or non-dominated sorting.

### [Deb2014]

* **Title**: An evolutionary many-objective optimization algorithm using reference-point-based
  nondominated sorting approach, Part I: solving problems with box constraints
* **Authors**: Deb, K., Jain, H.
* **Year**: 2014
* **DOI**: `10.1109/TEVC.2013.2281535`
* **URL**: <https://ieeexplore.ieee.org/document/6600851/>
* **Suggested categories**: `compartmental-modeling`
* **Why download**: NSGA-III reference. Mandatory citation if the catalogue's >3-objective follow-up
  tasks are commissioned.

## Recommendations for This Task

1. **Download all 21 primary discovered papers** (Druckmann2007, Druckmann2011, Achard2006,
   VanGeit2007, VanGeit2016, Gouwens2018, Attwell2001, Niven2008, Sengupta2010, Carter2009,
   Hallermann2012, Niven2007, Remme2018, Marder2006, Prinz2004, Goldman2001, Olypher2007,
   Strong1998, Borst1999, Brenner2000, Chklovskii2002). Five lower-priority discoveries
   (Cherniak1992, Wen2006, Victor1997, Deb2002, Deb2014) are nice-to-have. Together they cover every
   gap from `research_papers.md`.

2. **Adopt the BluePyOpt structural template (CellEvaluator + protocols + eFeature) for the
   catalogue's evaluator** — keep pymoo NSGA-II as the optimiser; port the
   evaluator/protocol/feature triple. Updates `research_papers.md` recommendation 1, which deferred
   methodology-toolchain choice to research-internet.

3. **Switch from NSGA-II to NSGA-III when the catalogue's MOBO follow-ups exceed 3 objectives**
   [Deb2014] [Blank2020]. Updates `research_papers.md` recommendation 5, which only contrasted
   NSGA-II vs qLogNEHVI. The full optimiser-selection rule is now: qLogNEHVI for low-d (<= 20)
   constrained problems; NSGA-II for high-d 2-3 objective problems; NSGA-III for high-d
   many-objective problems.

4. **Implement the four catalogued objective recipes immediately** — cytoplasm volume (already
   trivial from morphology generator), ATP-per-spike from `int(INa) dt / 3` per compartment,
   information transfer rate via Strong-Bialek direct method with 1/T extrapolation, and robustness
   as Marder-style +/- 10% perturbation SD. All four are computable from t0091's existing trial
   output without infrastructure rewrites.

5. **Pair every function objective with at least one biological-cost objective** [LondonHausser2005]
   [Chklovskii2002] [Cuntz2010]. Recommended catalogue pairs: DSI vs cytoplasm volume, DSI vs
   ATP-per-spike, DSI vs robustness, MI vs ATP-per-spike, MI vs cytoplasm volume. This is a new
   methodology constraint not present in `research_papers.md`'s recommendations.

6. **Treat Remme et al. 2018 as the closest published analogue and cite it as the canonical
   precedent for the project's planned DSI-vs-energy MOBO** [Remme2018]. The MSO
   coincidence-detection protocol generalises directly to the DSGC direction-selectivity
   computation.

7. **Validate the catalogue's metabolic-energy recipe against [Carter2009] benchmarks** (~25%
   above-minimum for cortical pyramidal cells, ~100% above-minimum for fast-spiking neurons) on the
   project's existing HH model before launching any DSI-vs-energy MOBO. This is a cheap sanity check
   that should be a planning-stage prerequisite.

8. **Validate the catalogue's information-transfer recipe against [Dhingra2004] (~60%
   spike-vs-graded-potential gray-level loss in a real RGC) on the project's HH-on / HH-off trial
   trio**. This is the within-cell-type calibration anchor identified in `research_papers.md`
   methodology insights.

## Tool and Library Landscape

* **BluePyOpt** [VanGeit2016] [BluePyOpt-GH] [BluePyOpt-Docs]: BlueBrain's open-source
  multi-objective optimisation framework for compartmental neuron models. Wraps DEAP and ships an
  IBEA selector. Last release 1.14.17 (Nov 2024); GitHub repo archived Feb 2025; future development
  at the Open Brain Institute. Modules: `bluepyopt.ephys.evaluators` (CellEvaluator),
  `bluepyopt.ephys.protocols` (StepProtocol etc.), `bluepyopt.ephys.efeatures`,
  `bluepyopt.objectives`, `bluepyopt.deapext` (DEAP integration). Active import surface for any
  catalogue evaluator port.

* **eFEL** [eFEL-GH]: Electrophys feature extraction library, C++ core (40.7%) + Python wrapper
  (57.9%). Headline features: `AP_amplitude`, `voltage_base`, `bpap_attenuation`, `ais_initiation`,
  plus dozens more (spike count, AHP depth, ISI CV, time-to-first-spike, etc.). Drop-in feature
  library for the catalogue evaluator.

* **pymoo** [Blank2020] [pymoo-Docs]: the project's optimiser. Algorithms: NSGA-II, R-NSGA-II,
  NSGA-III, R-NSGA-III, U-NSGA-III, MOEA/D, AGE-MOEA, AGE-MOEA2, RVEA, SMS-EMOA, CMOPSO. Indicators:
  GD, GD+, IGD, IGD+, Hypervolume, KKTPM. Mixed variables (binary, discrete, permutation, custom);
  vectorised matrix ops, joblib, GPU acceleration, custom parallelisation.

* **DEAP** [DEAP-Docs]: BluePyOpt's underlying selector library; supports the Generalized Reduced
  Run-Time Complexity Non-Dominated Sorting Algorithm; computes hypervolume that is dominated by a
  non-dominated set (assumes minimisation).

* **Platypus** (Python): multi-objective-focused engineering library; alternative to pymoo if the
  project ever needs algorithms not in pymoo. Lower priority for the catalogue.

* **paretoset** [paretoset-PyPI]: lightweight non-dominated-set utility, useful for post-hoc Pareto
  analysis on the project's NSGA-II output without invoking the full pymoo Indicator API.

* **AllenSDK** [AllenSDK-Docs]: Allen Institute software development kit; ships biophysical-model
  loaders for the [Gouwens2018] models in both perisomatic-only and all-active variants; runs on
  NEURON. Useful as a methodology cross-check / external comparison if the catalogue's results need
  cross-cell-type validation.

* **NeuroFitter** [VanGeit2007]: predecessor to BluePyOpt. Phase-plane-trajectory-density error
  metric. Source code on SourceForge (legacy). Mostly of historical interest.

## Source Index

### [Druckmann2007]

* **Type**: paper
* **Title**: A novel multiple objective optimization framework for constraining conductance-based
  neuron models by experimental data
* **Authors**: Druckmann, S., Banitt, Y., Gidon, A., Schuermann, F., Markram, H., Segev, I.
* **Year**: 2007
* **DOI**: `10.3389/neuro.01.1.1.001.2007`
* **URL**:
  <https://www.frontiersin.org/journals/neuroscience/articles/10.3389/neuro.01.1.1.001.2007/full>
* **Peer-reviewed**: yes (Frontiers in Neuroscience)
* **Relevance**: Canonical multi-objective methodology paper; per-feature SD-normalisation +
  Pareto-front-of-features framework adopted by the catalogue.

### [Druckmann2011]

* **Type**: paper
* **Title**: Effective stimuli for constructing reliable neuron models
* **Authors**: Druckmann, S., Berger, T. K., Schuermann, F., Hill, S., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002133`
* **URL**: <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002133>
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Stimulus-protocol design study; precursor to eFEL feature design.

### [Achard2006]

* **Type**: paper
* **Title**: Complex parameter landscape for a complex neuron model
* **Authors**: Achard, P., De Schutter, E.
* **Year**: 2006
* **DOI**: `10.1371/journal.pcbi.0020094`
* **URL**: <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.0020094>
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: First MOEA Purkinje fit; loose-hyperplanes parameter-landscape finding informs the
  project's Pareto-acceptable-ensemble reporting.

### [VanGeit2007]

* **Type**: paper
* **Title**: Neurofitter: a parameter tuning package for a wide range of electrophysiological neuron
  models
* **Authors**: Van Geit, W., Achard, P., De Schutter, E.
* **Year**: 2007
* **DOI**: `10.3389/neuro.11.001.2007`
* **URL**:
  <https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/neuro.11.001.2007/full>
* **Peer-reviewed**: yes (Frontiers in Neuroinformatics)
* **Relevance**: Predecessor to BluePyOpt; phase-plane-trajectory-density error metric.

### [VanGeit2016]

* **Type**: paper
* **Title**: BluePyOpt: leveraging open source software and cloud infrastructure to optimise model
  parameters in neuroscience
* **Authors**: Van Geit, W., Gevaert, M., Chindemi, G., et al.
* **Year**: 2016
* **DOI**: `10.3389/fninf.2016.00017`
* **URL**:
  <https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2016.00017/full>
* **Peer-reviewed**: yes (Frontiers in Neuroinformatics)
* **Relevance**: Canonical MOO toolchain in the field; the project's catalogue evaluator template.

### [Gouwens2018]

* **Type**: paper
* **Title**: Systematic generation of biophysically detailed models for diverse cortical neuron
  types
* **Authors**: Gouwens, N. W., Berg, J., Feng, D., et al.
* **Year**: 2018
* **DOI**: `10.1038/s41467-017-02718-3`
* **URL**: <https://www.nature.com/articles/s41467-017-02718-3>
* **Peer-reviewed**: yes (Nature Communications)
* **Relevance**: 170-cell systematic Druckmann-methodology benchmark on Allen mouse V1 data.

### [Attwell2001]

* **Type**: paper
* **Title**: An energy budget for signaling in the grey matter of the brain
* **Authors**: Attwell, D., Laughlin, S. B.
* **Year**: 2001
* **DOI**: `10.1097/00004647-200110000-00001`
* **URL**: <https://journals.sagepub.com/doi/10.1097/00004647-200110000-00001>
* **Peer-reviewed**: yes (Journal of Cerebral Blood Flow and Metabolism)
* **Relevance**: Stoichiometric Na+/K+/Ca2+ energy budget; foundation of ATP-per-spike recipe.

### [Niven2008]

* **Type**: paper
* **Title**: Energy limitation as a selective pressure on the evolution of sensory systems
* **Authors**: Niven, J. E., Laughlin, S. B.
* **Year**: 2008
* **DOI**: `10.1242/jeb.017574`
* **URL**: <https://journals.biologists.com/jeb/article/211/11/1792/9506>
* **Peer-reviewed**: yes (Journal of Experimental Biology)
* **Relevance**: Energy as selective pressure; justifies treating ATP-per-spike as a hard biological
  objective.

### [Sengupta2010]

* **Type**: paper
* **Title**: Action potential energy efficiency varies among neuron types in vertebrates and
  invertebrates
* **Authors**: Sengupta, B., Stemmler, M., Laughlin, S. B., Niven, J. E.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000840`
* **URL**: <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000840>
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Operationalises ATP-per-spike via Na/K-current overlap; supplies the recipe.

### [Carter2009]

* **Type**: paper
* **Title**: Sodium entry during action potentials of mammalian neurons: incomplete inactivation and
  reduced metabolic efficiency in fast-spiking neurons
* **Authors**: Carter, B. C., Bean, B. P.
* **Year**: 2009
* **DOI**: `10.1016/j.neuron.2009.12.011`
* **URL**: <https://www.sciencedirect.com/science/article/pii/S0896627309010010>
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: Empirical Na/K-overlap calibration benchmarks (25%/100% above-minimum).

### [Hallermann2012]

* **Type**: paper
* **Title**: State and location dependence of action potential metabolic cost in cortical pyramidal
  neurons
* **Authors**: Hallermann, S., de Kock, C. P. J., Stuart, G. J., Kole, M. H. P.
* **Year**: 2012
* **DOI**: `10.1038/nn.3132`
* **URL**: <https://www.nature.com/articles/nn.3132>
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Per-compartment ATP integration in a NEURON pyramidal model; methodology template.

### [Niven2007]

* **Type**: paper
* **Title**: Fly photoreceptors demonstrate energy-information trade-offs in neural coding
* **Authors**: Niven, J. E., Anderson, J. C., Laughlin, S. B.
* **Year**: 2007
* **DOI**: `10.1371/journal.pbio.0050116`
* **URL**: <https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.0050116>
* **Peer-reviewed**: yes (PLOS Biology)
* **Relevance**: Canonical empirical bits-per-ATP Pareto curve across fly species.

### [Remme2018]

* **Type**: paper
* **Title**: Function and energy consumption constrain neuronal biophysics in a canonical
  computation: coincidence detection
* **Authors**: Remme, M. W. H., Rinzel, J., Schreiber, S.
* **Year**: 2018
* **DOI**: `10.1371/journal.pcbi.1006612`
* **URL**: <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006612>
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Closest published analogue to the project's DSI-vs-energy MOBO; MSO
  function-vs-energy Pareto in a NEURON conductance model.

### [Marder2006]

* **Type**: paper
* **Title**: Variability, compensation and homeostasis in neuron and network function
* **Authors**: Marder, E., Goaillard, J.-M.
* **Year**: 2006
* **DOI**: `10.1038/nrn1949`
* **URL**: <https://www.nature.com/articles/nrn1949>
* **Peer-reviewed**: yes (Nature Reviews Neuroscience)
* **Relevance**: Canonical robustness review; manifold-of-acceptable-solutions framing.

### [Prinz2004]

* **Type**: paper
* **Title**: Similar network activity from disparate circuit parameters
* **Authors**: Prinz, A. A., Bucher, D., Marder, E.
* **Year**: 2004
* **DOI**: `10.1038/nn1352`
* **URL**: <https://www.nature.com/articles/nn1352>
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: 20-million-parameter STG database; methodology template for Marder-style
  perturbation robustness objective.

### [Goldman2001]

* **Type**: paper
* **Title**: Global structure, robustness, and modulation of neuronal models
* **Authors**: Goldman, M. S., Golowasch, J., Marder, E., Abbott, L. F.
* **Year**: 2001
* **DOI**: `10.1523/JNEUROSCI.21-14-05229.2001`
* **URL**: <https://www.jneurosci.org/content/21/14/5229>
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Compensatory-direction analysis; foundation for reporting robustness Pareto along
  hyperplanes.

### [Olypher2007]

* **Type**: paper
* **Title**: Using constraints on neuronal activity to reveal compensatory changes in neuronal
  parameters
* **Authors**: Olypher, A. V., Calabrese, R. L.
* **Year**: 2007
* **DOI**: `10.1152/jn.00842.2007`
* **URL**: <https://pubmed.ncbi.nlm.nih.gov/17855581/>
* **Peer-reviewed**: yes (Journal of Neurophysiology)
* **Relevance**: Implicit-function-theorem framework for parameter-manifold dimension and structure.

### [Strong1998]

* **Type**: paper
* **Title**: Entropy and information in neural spike trains
* **Authors**: Strong, S. P., Koberle, R., de Ruyter van Steveninck, R. R., Bialek, W.
* **Year**: 1998
* **DOI**: `10.1103/PhysRevLett.80.197`
* **URL**: <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.80.197>
* **Peer-reviewed**: yes (Physical Review Letters)
* **Relevance**: Direct method + 1/T extrapolation correction; the catalogue's MI recipe.

### [Borst1999]

* **Type**: paper
* **Title**: Information theory and neural coding
* **Authors**: Borst, A., Theunissen, F. E.
* **Year**: 1999
* **DOI**: `10.1038/14731`
* **URL**: <https://www.nature.com/articles/nn1199_947>
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Canonical neuroscience-readers' review of information theory and neural coding.

### [Brenner2000]

* **Type**: paper
* **Title**: Synergy in a neural code
* **Authors**: Brenner, N., Strong, S. P., Koberle, R., Bialek, W., de Ruyter van Steveninck, R. R.
* **Year**: 2000
* **DOI**: `10.1162/089976600300015259`
* **URL**: <https://direct.mit.edu/neco/article-abstract/12/7/1531/6387>
* **Peer-reviewed**: yes (Neural Computation)
* **Relevance**: Spike-pair coding extension of Strong et al.; useful for refined pair-MI catalogue
  objective.

### [Chklovskii2002]

* **Type**: paper
* **Title**: Wiring optimization in cortical circuits
* **Authors**: Chklovskii, D. B., Schikorski, T., Stevens, C. F.
* **Year**: 2002
* **DOI**: `10.1016/S0896-6273(02)00679-7`
* **URL**: <https://www.sciencedirect.com/science/article/pii/S0896627302006797>
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: 3/5-volume rule; evolutionary justification for the cytoplasm-volume objective and
  function-cost pairing.

### [Cherniak1992]

* **Type**: paper
* **Title**: Local optimization of neuron arbors
* **Authors**: Cherniak, C.
* **Year**: 1992
* **DOI**: `10.1007/BF00204115`
* **URL**: <https://link.springer.com/article/10.1007/BF00204115>
* **Peer-reviewed**: yes (Biological Cybernetics)
* **Relevance**: Steiner-tree formalism + local volume minimisation at branch junctions.

### [Wen2006]

* **Type**: paper
* **Title**: Wiring optimization can relate neuronal structure and function
* **Authors**: Wen, Q., Chklovskii, D. B.
* **Year**: 2006
* **DOI**: `10.1073/pnas.0506806103`
* **URL**: <https://www.pnas.org/doi/10.1073/pnas.0506806103>
* **Peer-reviewed**: yes (PNAS)
* **Relevance**: Wiring-optimisation theory linked to specific arbor structure-function.

### [Victor1997]

* **Type**: paper
* **Title**: Metric-space analysis of spike trains: theory, algorithms and application
* **Authors**: Victor, J. D., Purpura, K. P.
* **Year**: 1997
* **DOI**: `10.1088/0954-898X_8_2_003`
* **URL**: <https://www.tandfonline.com/doi/abs/10.1088/0954-898X_8_2_003>
* **Peer-reviewed**: yes (Network: Computation in Neural Systems)
* **Relevance**: Spike-distance metrics complementing direct MI estimation.

### [Deb2002]

* **Type**: paper
* **Title**: A fast and elitist multiobjective genetic algorithm: NSGA-II
* **Authors**: Deb, K., Pratap, A., Agarwal, S., Meyarivan, T.
* **Year**: 2002
* **DOI**: `10.1109/4235.996017`
* **URL**: <https://ieeexplore.ieee.org/document/996017/>
* **Peer-reviewed**: yes (IEEE Transactions on Evolutionary Computation)
* **Relevance**: Canonical NSGA-II reference for the project's optimiser.

### [Deb2014]

* **Type**: paper
* **Title**: An evolutionary many-objective optimization algorithm using reference-point-based
  nondominated sorting approach, Part I: solving problems with box constraints
* **Authors**: Deb, K., Jain, H.
* **Year**: 2014
* **DOI**: `10.1109/TEVC.2013.2281535`
* **URL**: <https://ieeexplore.ieee.org/document/6600851/>
* **Peer-reviewed**: yes (IEEE Transactions on Evolutionary Computation)
* **Relevance**: NSGA-III reference for >3-objective catalogue follow-ups.

### [Blank2020]

* **Type**: paper
* **Title**: pymoo: multi-objective optimization in Python
* **Authors**: Blank, J., Deb, K.
* **Year**: 2020
* **DOI**: `10.1109/ACCESS.2020.2990567`
* **URL**: <https://ieeexplore.ieee.org/document/9078759>
* **Peer-reviewed**: yes (IEEE Access)
* **Relevance**: Canonical pymoo reference; the project's optimiser.

### [Zitzler1999]

* **Type**: paper
* **Title**: Multiobjective evolutionary algorithms: a comparative case study and the strength
  Pareto approach
* **Authors**: Zitzler, E., Thiele, L.
* **Year**: 1999
* **DOI**: `10.1109/4235.797969`
* **URL**: <https://ieeexplore.ieee.org/document/797969/>
* **Peer-reviewed**: yes (IEEE Transactions on Evolutionary Computation)
* **Relevance**: SPEA-family + comparative-benchmark methodology; foundation of pymoo's hypervolume
  / IGD primitives.

### [Koch1999]

* **Type**: paper
* **Title**: Biophysics of Computation: Information Processing in Single Neurons
* **Authors**: Koch, C.
* **Year**: 1999
* **DOI**: `10.1093/oso/9780195104912.001.0001`
* **URL**: <https://global.oup.com/academic/product/biophysics-of-computation-9780195181999>
* **Peer-reviewed**: yes (Oxford University Press textbook)
* **Relevance**: Canonical single-neuron information-processing textbook; framing reference for the
  catalogue's MI section.

### [BluePyOpt-GH]

* **Type**: repository
* **Title**: BluePyOpt — Blue Brain Python Optimisation Library
* **Author/Org**: Blue Brain Project, EPFL (now Open Brain Institute)
* **Date**: 2024-11
* **URL**: <https://github.com/BlueBrain/BluePyOpt>
* **Last updated**: 2024-11 (latest release 1.14.17); repo archived Feb 2025; future development at
  Open Brain Institute
* **Peer-reviewed**: no (accompanies peer-reviewed publication [VanGeit2016])
* **Relevance**: The canonical multi-objective optimisation library for compartmental neuron models.
  Module layout (CellEvaluator + protocols + efeatures) is the structural template the catalogue
  should adopt.

### [BluePyOpt-Docs]

* **Type**: documentation
* **Title**: BluePyOpt Read the Docs
* **Author/Org**: Blue Brain Project
* **URL**: <https://bluepyopt.readthedocs.io/en/latest/index.html>
* **Peer-reviewed**: no
* **Relevance**: API surface (bluepyopt.ephys.evaluators, bluepyopt.ephys.protocols,
  bluepyopt.ephys.efeatures, bluepyopt.objectives) for porting catalogue evaluators.

### [eFEL-GH]

* **Type**: repository
* **Title**: eFEL — Electrophys Feature Extraction Library
* **Author/Org**: Blue Brain Project
* **Date**: 2025
* **URL**: <https://github.com/BlueBrain/eFEL>
* **Peer-reviewed**: no
* **Relevance**: C++ feature library (40.7% C++, 57.9% Python); supplies headline features
  (AP_amplitude, voltage_base, bpap_attenuation, ais_initiation, plus dozens more) used by every
  Druckmann-methodology fit.

### [pymoo-Docs]

* **Type**: documentation
* **Title**: pymoo: Multi-objective Optimization in Python
* **Author/Org**: anyoptimization (J. Blank, K. Deb)
* **URL**: <https://pymoo.org/>
* **Peer-reviewed**: no (accompanies peer-reviewed [Blank2020])
* **Relevance**: Algorithm catalogue (NSGA-II, NSGA-III, MOEA/D, etc.), indicators (HV, IGD, GD+),
  parallelisation support; the project's optimiser documentation.

### [DEAP-Docs]

* **Type**: documentation
* **Title**: DEAP — Distributed Evolutionary Algorithms in Python
* **Author/Org**: DEAP Project
* **URL**: <https://deap.readthedocs.io/>
* **Peer-reviewed**: no
* **Relevance**: BluePyOpt's underlying selector library; supports non-dominated sorting and
  hypervolume.

### [paretoset-PyPI]

* **Type**: documentation
* **Title**: paretoset PyPI page
* **Author/Org**: tommyod (Tommy Odland)
* **URL**: <https://pypi.org/project/paretoset/>
* **Peer-reviewed**: no
* **Relevance**: Lightweight non-dominated-set utility for post-hoc Pareto analysis on the project's
  NSGA-II output.

### [AllenSDK-Docs]

* **Type**: documentation
* **Title**: AllenSDK Biophysical Models
* **Author/Org**: Allen Institute for Brain Science
* **URL**: <https://allensdk.readthedocs.io/en/latest/biophysical_models.html>
* **Peer-reviewed**: no (accompanies peer-reviewed [Gouwens2018])
* **Relevance**: Methodology cross-check / external comparison resource; runs Gouwens2018 models on
  NEURON.

### [Hay2011]

* **Type**: paper
* **Title**: Models of neocortical layer 5b pyramidal cells capturing a wide range of dendritic and
  perisomatic active properties
* **Authors**: Hay, E., Hill, S., Schuermann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **URL**: <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002107>
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Already in corpus
  (`tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/`). The
  20-objective NSGA-style L5b pyramidal fit referenced for the Pareto-acceptable-ensemble reporting
  pattern.

### [Cuntz2010]

* **Type**: paper
* **Title**: One rule to grow them all: a general theory of neuronal branching and its practical
  application
* **Authors**: Cuntz, H., Forstner, F., Borst, A., Hausser, M.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000877`
* **URL**: <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000877>
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Already in corpus
  (`tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000877/`).
  Cajal-cytoplasm-conservation grounding for the cytoplasm-volume objective.

### [Dhingra2004]

* **Type**: paper
* **Title**: Spike generator limits efficiency of information transfer in a retinal ganglion cell
* **Authors**: Dhingra, N. K., Smith, R. G.
* **Year**: 2004
* **DOI**: `10.1523/jneurosci.5346-03.2004`
* **URL**: <https://www.jneurosci.org/content/24/10/2914>
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Already in corpus
  (`tasks/t0015_literature_survey_cable_theory/assets/paper/10.1523_jneurosci.5346-03.2004/`). The
  ideal-observer recipe and within-cell-type calibration anchor for the project's MI estimator.

### [Ament2023]

* **Type**: paper
* **Title**: Unexpected improvements to expected improvement for Bayesian optimization
* **Authors**: Ament, S., Daulton, S., Eriksson, D., Balandat, M., Bakshy, E.
* **Year**: 2023
* **DOI**: `no-doi_Ament2023_logei-bo`
* **URL**: <https://arxiv.org/abs/2310.20708>
* **Peer-reviewed**: yes (NeurIPS 2023)
* **Relevance**: Already in corpus
  (`tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/no-doi_Ament2023_logei-bo/`). qLogNEHVI
  fixes vanishing gradients in EHVI/qNEHVI; the optimiser-selection rule referenced for low-d
  constrained MOBO.

### [Hines1997]

* **Type**: paper
* **Title**: The NEURON simulation environment
* **Authors**: Hines, M. L., Carnevale, N. T.
* **Year**: 1997
* **DOI**: `10.1162/neco.1997.9.6.1179`
* **URL**: <https://direct.mit.edu/neco/article/9/6/1179/6063>
* **Peer-reviewed**: yes (Neural Computation)
* **Relevance**: Already in corpus
  (`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/`).
  The <= 20 um compartment-discretisation convention for mesh-density invariance.

### [LondonHausser2005]

* **Type**: paper
* **Title**: Dendritic computation
* **Authors**: London, M., Hausser, M.
* **Year**: 2005
* **DOI**: `10.1146/annurev.neuro.28.061604.135703`
* **URL**: <https://www.annualreviews.org/doi/10.1146/annurev.neuro.28.061604.135703>
* **Peer-reviewed**: yes (Annual Review of Neuroscience)
* **Relevance**: Already in corpus
  (`tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1146_annurev.neuro.28.061604.135703/`).
  Justifies the function-objective + cost-objective pairing rule.
