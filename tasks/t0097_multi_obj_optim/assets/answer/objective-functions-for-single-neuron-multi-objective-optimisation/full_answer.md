---
spec_version: "2"
answer_id: "objective-functions-for-single-neuron-multi-objective-optimisation"
answered_by_task: "t0097_multi_obj_optim"
date_answered: "2026-05-08"
confidence: "high"
---
# Catalogue of Multi-Objective Single-Neuron Objective Functions

## Question

Which objective functions have been used in published multi-objective optimisation of single-neuron
compartmental models, and what is each one's formula, units, and NEURON-side computational recipe on
a t0091-style 8-direction trial output?

## Short Answer

The published multi-objective single-neuron optimisation literature converges on four canonical
biological objective categories that fit directly on top of the project's existing pymoo NSGA-II
loop: stimulus-spike-train mutual information via the direct method with 1/T extrapolation,
ATP-per-spike via per-compartment integration of Na+ inward current divided by three (the Na+/K+
ATPase stoichiometry), cytoplasm volume as the sum of pi*r^2*L over compartments (novel as an
explicit MOO target on a single neuron), and Marder-style robustness as the standard deviation of
DSI under +/-10% perturbation of all channel densities. Each catalogued objective is implemented as
one pymoo evaluator callable on the project's existing 8-direction 1400-ms trial output and is
reported with a uniform 8-field record. Two additional well-defined objectives surfaced in the
survey are also catalogued: coincidence-detection accuracy and bits-per-ATP efficiency. The
methodology synthesis adopts per-feature SD-normalisation, the 2-3 SD acceptance threshold and
ensemble-as-experiment reporting pattern, and a clear optimiser-selection rule (NSGA-II for high-d
2-3-objective problems, NSGA-III for high-d many-objective problems, qLogNEHVI for low-d constrained
problems).

## Research Process

The catalogue was assembled in three stages.

**Stage 1 — Existing-corpus review.** The project's 22 paper assets across categories
`compartmental-modeling`, `dendritic-computation`, `cable-theory`, `voltage-gated-channels`, and
`retinal-ganglion-cell` were screened for multi-objective methodology and biological objective
formulas. Nine corpus papers genuinely contributed: Hay et al. 2011 (the canonical 20-objective NSGA
fit of a cortical L5b pyramidal cell), Cuntz et al. 2010 (the Cajal cytoplasm-conservation
arbor-growth model), Ament et al. 2023 (qLogNEHVI vs canonical qNEHVI for noisy MOBO), Dhingra and
Smith 2004 (the only direct MI measurement in a real RGC in the corpus), Koch and Poggio 1982,
Mainen and Sejnowski 1996, Fohlmeister and Miller 1997, Hines and Carnevale 1997, and London and
Hausser 2005. The output is `research/research_papers.md`. The corpus review found four major gaps:
no Druckmann-style methodology paper, no biological energy-budget paper, no robustness/degeneracy
paper, and no information-theory canon paper.

**Stage 2 — Internet research to close gaps.** Eighteen targeted searches across PubMed/PMC,
Google Scholar, PLOS, Frontiers, Nature, JNeurosci, Physical Review Letters, IEEE TEC, GitHub, Read
the Docs, and ModelDB surfaced 21 primary discovered papers and 5 lower-priority discoveries that
together resolve every research_papers.md gap. The output is `research/research_internet.md`. The
discovered methodology line is Druckmann et al. 2007 (per-feature SD-normalisation Pareto-front
framework), Druckmann et al. 2011 (stimulus-protocol design study), Achard and De Schutter 2006
(first MOEA Purkinje fit and the loose-hyperplanes parameter-landscape finding), Van Geit et al.
2007 (NeuroFitter), Van Geit et al. 2016 (BluePyOpt), and Gouwens et al. 2018 (170-cell
high-throughput Allen application). The discovered biological-objective lines are Attwell and
Laughlin 2001 / Niven and Laughlin 2008 / Sengupta et al. 2010 / Carter and Bean 2009 / Hallermann
et al. 2012 / Niven et al. 2007 / Remme et al. 2018 (energy), Marder and Goaillard 2006 / Prinz et
al. 2004 / Goldman et al. 2001 / Olypher and Calabrese 2007 (robustness), Strong et al. 1998 / Borst
and Theunissen 1999 / Brenner et al. 2000 / Victor and Purpura 1997 (information theory), and
Chklovskii et al. 2002 / Cherniak 1992 / Wen and Chklovskii 2006 (wiring economy).

**Stage 3 — Catalogue construction.** Each must-find objective category was assigned a uniform
8-field record (name, LaTeX formula, units, NEURON-side quantities, recipe step-by-step from a
t0091-style 8-direction 1400-ms trial output, biological-plausibility note,
direction-of-optimisation, supporting paper citations). Two additional well-defined objectives
surfaced by the surveys (coincidence-detection accuracy and bits-per-ATP efficiency) were catalogued
with the same record format. A methodology synthesis section unifies Druckmann et al.'s
SD-normalisation, Hay et al.'s acceptance-threshold reporting, Achard and De Schutter's
loose-hyperplanes finding, Van Geit's CellEvaluator/Protocol/EFeature triple, and the
optimiser-selection rule grounded in Ament et al. 2023's vanishing-gradient diagnosis and the
project's own t0078 budget overrun. Conflicting evidence was minimal — the only methodology
disagreement was the choice between BluePyOpt's IBEA-default selector (which the project does not
use) and pymoo NSGA-II (which the project does use); resolved by adopting BluePyOpt's structural
template only (CellEvaluator+Protocol+EFeature) while keeping pymoo NSGA-II as the optimiser.

## Evidence from Papers

The 21 newly catalogued papers and 9 corpus papers together cover every must-find objective
category. The strongest pieces of paper-derived evidence are:

* **Druckmann et al. 2007** [Druckmann2007][druckmann2007] established the multi-objective
  evolutionary framework every subsequent methodology paper inherits. Per-feature SD-normalisation
  expresses every feature as `(value - mean_experimental) / SD_experimental`, returning the Pareto
  front of feature combinations rather than a single best fit. This is the foundational template.

* **Hay et al. 2011** [Hay2011][hay2011] fit conductance densities of nine ion channels plus
  Ca-buffer parameters in a thick-tufted L5b pyramidal cell to 20 firing-feature objectives (10
  perisomatic step-current + 10 BAP-activated Ca-spike features). The optimiser was an elitist
  non-dominated sorting EA — population 1000, 500 generations, 22 free parameters, 240-1024 CPU
  cores, 2-5 days. Models are accepted when every feature lies within 2-3 SD of the experimental
  mean. The published artefact is ~2000 acceptable models (ModelDB 139653) — a Pareto-acceptable
  ensemble, not a single fit. Joint perisomatic + BAC fitting was strictly necessary: BAC-only
  yielded 899 acceptable models that failed perisomatic targets (e.g., apical Nat 82.5 pS/um^2 vs
  the BAC-acceptable 101-133.5 pS/um^2 when perisomatic was added back); perisomatic-only yielded 52
  acceptable models. The two single-target acceptable sets do not overlap on the joint feature
  space.

* **Achard and De Schutter 2006** [Achard2006][achard2006] performed the first MOEA fit of a complex
  Purkinje cell with 24 free conductance densities, obtaining 20 very different models all
  reproducing the experimental firing pattern (including complex-spike fine details). The parameter
  landscape of acceptable solutions is a set of loosely connected hyperplanes, not a single basin.
  Grid search and random search miss these hyperplanes; only directed search recovers them.

* **Van Geit et al. 2016** [VanGeit2016][vangeit2016] supplied BluePyOpt, the field's de-facto MOO
  toolchain, with the canonical structural template
  `CellEvaluator(cell_model, params, protocols, fitness_calculator)`. The template is
  library-agnostic — directly portable to pymoo NSGA-II while preserving every objective the
  project currently computes.

* **Druckmann et al. 2011** [Druckmann2011][druckmann2011] showed that step + ramp current-injection
  combinations best constrain conductance-based models. Direct precursor of eFEL feature design.

* **Gouwens et al. 2018** [Gouwens2018][gouwens2018] applied the BluePyOpt stack to 170 individual
  mouse V1 neurons fitting 10 active conductances per cell to electrophysiological features. The
  largest published systematic application of the methodology.

* **Strong et al. 1998** [Strong1998][strong1998] introduced the direct method for estimating
  spike-train MI: discretise the spike train into binary words of length T at resolution dt, compute
  the empirical word distribution, take the entropy, subtract a noise-entropy estimate at each fixed
  stimulus, and extrapolate to infinite data length using a 1/T linear regression to correct for
  finite-data bias. The fly H1 motion-sensitive neuron measurements topped out at 90 bits/s —
  within a factor of 2 of the spike-train entropy ceiling.

* **Brenner et al. 2000** [Brenner2000][brenner2000] extended the direct method to spike pairs and
  demonstrated that pairs close in time carry more than 2x the information of single spikes
  (positive synergy in the H1 code).

* **Borst and Theunissen 1999** [Borst1999][borst1999] is the canonical neuroscience-readers' review
  of information theory and neural coding.

* **Victor and Purpura 1997** [Victor1997][victor1997] supply spike-distance metrics that complement
  direct MI estimation in the short-data regime.

* **Dhingra and Smith 2004** [Dhingra2004][dhingra2004] is the only direct MI measurement in a real
  RGC in the corpus. Detection threshold from graded potential = 1.5% contrast vs from spikes = 3.8%
  contrast (~2.5x degradation by the spike generator); spikes carry roughly 60% fewer
  distinguishable gray levels than the graded potential. The information loss is dominated by the
  spike-generator threshold nonlinearity, not stochastic noise. Provides a within-cell-type
  calibration anchor for the catalogue's MI recipe.

* **Attwell and Laughlin 2001** [Attwell2001][attwell2001] derived the canonical brain energy budget
  on the rat grey-matter neuron: action potentials consume 47% of total signalling ATP, postsynaptic
  glutamate effects 34%, resting potential 13%, glutamate recycling 3%. Establishes the
  stoichiometric Na+/K+/Ca2+ accounting framework that every subsequent ATP-per-spike paper builds
  on.

* **Niven and Laughlin 2008** [Niven2008][niven2008] elevates the budget to a selective pressure:
  across sensory systems, evolution demonstrably reduces metabolic cost subject to functional
  constraints.

* **Sengupta et al. 2010** [Sengupta2010][sengupta2010] makes the recipe operational: ATP per spike
  = (integrated Na+ influx during AP) / 3, where the factor 3 reflects three Na+ ions exchanged per
  ATP by the Na+/K+ pump. The neuron's Na/K-current overlap during the AP controls the multiplier
  above the theoretical minimum.

* **Carter and Bean 2009** [Carter2009][carter2009] supplies the empirical anchor: in mammalian
  cortical pyramidal cells the Na/K overlap is small (~25% above minimum); in fast-spiking
  cerebellar Purkinje cells and cortical interneurons the overlap is large (~100% above minimum).
  This is the calibration benchmark for the project's ATP-per-spike recipe.

* **Hallermann et al. 2012** [Hallermann2012][hallermann2012] applies the Na/K-overlap recipe at
  compartment level in a cortical pyramidal NEURON model. AIS and nodes of Ranvier have the highest
  cost-per-area, but backpropagation into dendrites and axon collaterals dominates total cell energy
  consumption. Direct methodology template for the project's per-compartment integration.

* **Niven et al. 2007** [Niven2007][niven2007] supplies the clearest empirical Pareto curve in the
  literature: across four fly species, photoreceptor information rates from 200 bits/s (D.
  melanogaster) to 1000 bits/s (S. carnaria) scale super-linearly with ATP cost, with a fixed cost
  of ~20% of maximum consumption. A bits-per-ATP Pareto front is measurable in the same cell type
  across species.

* **Remme et al. 2018** [Remme2018][remme2018] is the methodologically closest published analogue to
  the project's planned DSI-vs-energy experiment: in mammalian MSO coincidence-detector neurons,
  function (coincidence detection accuracy) and energy (Attwell-Laughlin-style ATP per AP integrated
  across compartments) are jointly optimised in a conductance-based NEURON model, and the Pareto
  front predicts optimal ranges for cell morphology and membrane properties. The MSO precedent
  generalises directly to the DSGC direction-selectivity computation.

* **Marder and Goaillard 2006** [Marder2006][marder2006] is the canonical synthesis: variability
  across animals
  + compensation across parameters + homeostasis across time produce stable function from inherently
    variable parts.

* **Prinz et al. 2004** [Prinz2004][prinz2004] simulated 20 million versions of the three-cell
  crustacean pyloric network with combinatorial channel-density and synapse-strength variation,
  finding "virtually indistinguishable network activity from widely disparate sets of underlying
  mechanisms" — the empirical foundation for the manifold-of-acceptable-solutions view.

* **Goldman et al. 2001** [Goldman2001][goldman2001] showed that even a small (5-conductance) neuron
  model has directions in parameter space along which the activity pattern is invariant
  ("compensatory directions").

* **Olypher and Calabrese 2007** [Olypher2007][olypher2007] gives the formal mathematics: by the
  implicit-function theorem, the manifold of parameter sets producing fixed activity characteristics
  has codimension equal to the number of independent fixed characteristics, and locally these
  manifolds are smooth.

* **Cuntz et al. 2010** [Cuntz2010][cuntz2010] grounds the cytoplasm-volume objective biologically:
  their arbor-growth construction minimises a scalar
  `total_cost = wiring_cost + bf * path_length_cost`, with biologically realistic arbors clustering
  at `bf` in [0.2, 0.7] across fly LPTCs, mammalian CA1 pyramidal cells, and cerebellar Purkinje
  cells. The limits bf=0 (pure MST) and bf->infinity (star graph) are unphysical. Synthetic Cuntz
  arbors match real reconstructions on total dendritic length within a few percent.

* **Chklovskii et al. 2002** [Chklovskii2002][chklovskii2002] makes the wiring-3/5-of-grey-matter
  rule evolutionarily explicit: minimising delays + cable attenuation + wire length predicts wire
  should occupy 3/5 of grey-matter volume, matching direct measurement.

* **Cherniak 1992** [Cherniak1992][cherniak1992] establishes that local branch-junction geometry
  minimises volume, not length, at finer-than-segment scale (Steiner-tree formalism).

* **Ament et al. 2023** [Ament2023][ament2023] diagnoses and fixes the vanishing-gradient pathology
  of the canonical EHVI/qNEHVI used in BoTorch. As the BO loop closes its optimality gap and the GP
  posterior becomes informative, canonical EI's argument falls into a floating-point regime where
  the function evaluates to literal zero across most of the domain and multistart gradient-based
  optimisation degenerates into random search. qLogNEHVI fixes this. Across benchmarks, canonical
  qNEHVI plateaus while qLogNEHVI continues to improve.

* **Hines and Carnevale 1997** [Hines1997][hines1997] establishes the <=20-um compartment
  discretisation convention NEURON-based catalogue objectives depend on for mesh-density invariance.

* **London and Hausser 2005** [LondonHausser2005][londonhausser2005] articulates the design space
  the catalogue must populate: dendrites can act as passive cables, active spike conductors,
  amplifiers, coincidence detectors, and direction-discriminators. Justifies pairing every
  dendritic-computation objective with a dendritic-cost objective.

* **Koch and Poggio 1982** [KochPoggio1982][kochpoggio1982] is the historical anchor for treating
  dendritic morphology as a functional axis. **Mainen and Sejnowski 1996** [Mainen1996][mainen1996]
  shows that dendritic morphology alone determines firing pattern when the same channel set is
  distributed across morphologies. **Fohlmeister and Miller 1997**
  [FohlmeisterMiller1997][fohlmeistermiller1997] reinforces the same in amphibian RGC.

## Evidence from Internet Sources

Five external references were consulted as live methodology sources:

* **BluePyOpt repository** [BluePyOpt-GH](https://github.com/BlueBrain/BluePyOpt)
  (`github.com/BlueBrain/BluePyOpt`) — last release 1.14.17 (Nov 2024); GitHub repo archived Feb
  2025; future development at the Open Brain Institute. Modules: `bluepyopt.ephys.evaluators`
  (`CellEvaluator`), `bluepyopt.ephys.protocols` (`StepProtocol` etc.), `bluepyopt.ephys.efeatures`,
  `bluepyopt.objectives`, `bluepyopt.deapext` (DEAP integration). Wraps DEAP and ships an IBEA
  selector by default.

* **BluePyOpt documentation**
  [BluePyOpt-Docs](https://bluepyopt.readthedocs.io/en/latest/index.html)
  (`bluepyopt.readthedocs.io`) — exposes the canonical evaluator/protocol/feature triple. Confirms
  the structural template `CellEvaluator(cell_model, params, protocols, fitness_calculator)` where
  `fitness_calculator` returns one objective per `eFeature`.

* **eFEL** [eFEL-GH](https://github.com/BlueBrain/eFEL) (`github.com/BlueBrain/eFEL`) —
  electrophys feature extraction library, C++ core (40.7%) + Python wrapper (57.9%). Headline
  features: `AP_amplitude`, `voltage_base`, `bpap_attenuation`, `ais_initiation`, plus dozens more.
  Drop-in feature library for the catalogue evaluator.

* **pymoo documentation** [pymoo-Docs](https://pymoo.org/) (`pymoo.org`) — the project's
  optimiser. Algorithms: NSGA-II, R-NSGA-II, NSGA-III, R-NSGA-III, U-NSGA-III, MOEA/D, AGE-MOEA,
  AGE-MOEA2, RVEA, SMS-EMOA, CMOPSO. Indicators: GD, GD+, IGD, IGD+, Hypervolume, KKTPM. Mixed
  variables (binary, discrete, permutation, custom); vectorised matrix ops, joblib, GPU
  acceleration.

* **AllenSDK biophysical-model documentation**
  [AllenSDK-Docs](https://allensdk.readthedocs.io/en/latest/biophysical_models.html)
  (`allensdk.readthedocs.io/.../biophysical_models.html`) — confirms NEURON as the simulation
  substrate, with both perisomatic-only and all-active model variants available. Useful for
  cross-cell-type validation.

## Evidence from Code or Experiments

This is a literature survey. No new code was written and no new experiments were run. The only
project-internal reference is `t0091_morphology_extended_nsga2_v1`, which is the catalogue's
downstream consumer: the project's existing pymoo NSGA-II loop validated end-to-end over 68 free
parameters on a procedurally generated DSGC. Every catalogued recipe is designed to compose with
t0091's 8-direction 1400-ms trial-output format without infrastructure rewrites. The recipes
themselves are not validated by experiment in this task; recipe validation belongs in the future
MOBO task suggestions rather than as a prerequisite for emitting the catalogue.

## Synthesis

The catalogue below assigns a uniform 8-field record to every objective: **Name**, **Mathematical
formula** (LaTeX), **Units**, **NEURON-side quantities required**, **Recipe** (step-by-step
computation from a t0091-style 8-direction 1400-ms trial output), **Biological plausibility**,
**Direction of optimisation**, **Supporting paper citations**. The four mandatory categories are
catalogued first, followed by additional well-defined objectives and the methodology synthesis.

### mutual_information_stimulus_spike_train

* **Name**: `mutual_information_stimulus_spike_train`
* **Mathematical formula**: $I(D; S) = H(S) - H(S \mid D) = \lim_{T \to
  \infty}\frac{1}{T}\bigl[H_{\text{total}}(T) - \langle H_{\text{noise}}(T) \rangle_D\bigr]$ where
  $D$ is the discrete 8-way stimulus direction, $S$ is the binary spike-word of length $T$ at
  resolution $\Delta t$, $H_{\text{total}}(T)$ is the entropy of the full word distribution pooled
  across directions, and $H_{\text{noise}}(T)$ is the within-direction conditional entropy. The
  infinite-data limit is approximated by linear regression of $H/T$ against $1/T$ across several $T$
  values per the Strong-Bialek direct method.
* **Units**: bits per second (when reporting the rate at the 1/T extrapolation intercept) or bits
  per trial (when reporting at a fixed $T$).
* **NEURON-side quantities required**: spike times per direction (already produced by t0091 in
  `FULL` mode with HH on); optionally Vm trace per compartment per direction (used when HH is off
  for the EPSP/IPSP-passive trio, to compute graded-potential MI as a calibration check against
  Dhingra and Smith 2004's ~60% gray-level loss).
* **Recipe** (5 steps):
  1. Discretise each trial's spike train into binary words at resolution $\Delta t = 5$ ms. Choose
     $T \in \{25, 50, 75, 100\}$ ms; this gives word lengths $L = T/\Delta t \in \{5, 10, 15, 20\}$
     bits per word per trial.
  2. Pool words across all trials and all 8 directions to estimate the empirical distribution
     $P(S_T)$. Compute $H_{\text{total}}(T) = -\sum_w P(w) \log_2 P(w)$.
  3. For each of the 8 stimulus directions $d$, pool words across that direction's trials only.
     Estimate $P(S_T \mid D = d)$ and its entropy $H(S_T \mid D = d)$. Average across the 8
     directions to get $\langle H_{\text{noise}}(T) \rangle_D$.
  4. Plot $[H_{\text{total}}(T) - \langle H_{\text{noise}}(T) \rangle_D]/T$ against $1/T$. Fit a
     linear regression. Take the intercept at $1/T = 0$. This is the bias-corrected mutual
     information rate $I(D; S)$ in bits per second.
  5. (Optional cross-check) Compute the Panzeri-Treves NSB Bayesian-bias correction as a second
     estimator. Validate the two estimators agree within 10%.
* **Biological plausibility**: information capacity is a hard biological constraint. RGCs publish in
  the 200-1000 bits/s range across species. Within-cell-type calibration anchor: Dhingra and Smith
  2004 measured ~60% gray-level loss between graded-potential MI and spike-train MI in a
  brisk-transient guinea-pig RGC. The project should reproduce a comparable HH-on/HH-off ratio on
  its DSGC substrate as a sanity check before deploying the recipe inside an MOBO loop.
* **Direction of optimisation**: maximise.
* **Supporting paper citations**: [Strong1998][strong1998], [Brenner2000][brenner2000],
  [Borst1999][borst1999], [Dhingra2004][dhingra2004], [Victor1997][victor1997].

### metabolic_energy_atp_per_spike

* **Name**: `metabolic_energy_atp_per_spike`
* **Mathematical formula**: $E_{\text{AP}} = \frac{1}{3}\sum_{c \in \text{compartments}} \frac{1}{e}
  \int_{t_{\text{AP-start}}}^{t_{\text{AP-end}}} I_{Na}^{(c)}(t)\, dt$ where $I_{Na}^{(c)}(t)$ is
  the inward sodium current in compartment $c$ at time $t$, $e$ is the elementary charge ($1.602
  \times 10^{-19}$ C), the integration window $[t_{\text{AP-start}}, t_{\text{AP-end}}]$ is the
  per-spike window detected from the somatic Vm threshold crossing, and the factor $1/3$ is the
  Na+/K+ ATPase stoichiometry: three Na+ ions exchanged per ATP molecule hydrolysed.
* **Units**: ATP molecules per spike (per compartment, summed across compartments). May be
  aggregated to ATP per direction (sum across all spikes in that direction's trial) and ATP per
  trial (sum across all directions).
* **NEURON-side quantities required**: inward Na+ current `seg.ina` per segment per direction
  (recorded via NEURON's `Vector.record(&seg._ref_ina, dt_record)` API for every section, every
  segment, with `dt_record` <= the simulation `dt` to capture the AP shape); somatic Vm trace for
  AP-window detection.
* **Recipe** (6 steps):
  1. For each direction's trial, record `seg.ina` per compartment at the simulation `dt`. The
     project's existing EPSP/IPSP/FULL trio already records Vm; the FULL mode (HH on) is the only
     mode that produces a meaningful Na+ current. EPSP/IPSP-passive modes produce zero ATP
     contribution and should be skipped.
  2. Detect AP windows from the somatic Vm threshold crossing. Use a threshold of -20 mV with a
     minimum 1.0 ms refractory window between consecutive crossings to avoid double-counting mid-AP
     fluctuations. The AP-start time is the upward crossing; the AP-end time is the next downward
     crossing back through -20 mV (typically 1.5-3 ms later).
  3. For each detected AP window and each compartment, integrate $I_{Na}^{(c)}(t)$ over the window
     using the trapezoidal rule. The integral is in coulombs (NEURON's `ina` is in mA/cm^2; multiply
     by segment surface area in cm^2 to get total current per compartment, then integrate in
     seconds).
  4. Convert each compartment's per-AP charge to ATP molecules via $N_{\text{ATP}}^{(c, \text{AP})}
     = (Q^{(c, \text{AP})} / e) / 3$.
  5. Sum across compartments to get per-AP per-cell ATP cost. Sum across all APs in the trial to get
     per-direction ATP. Sum across all 8 directions to get total ATP per trial. Report the per-
     spike average (total ATP / total spikes) as the headline objective.
  6. (Validation) Compare the cell-aggregate ATP/AP against Carter and Bean 2009's
     ~25%-above-minimum benchmark for cortical pyramidal and ~100%-above-minimum benchmark for
     fast-spiking cells. Discrepancies > 30% indicate either a recipe error (most commonly in
     surface-area conversion) or a genuine biophysical mismatch worth investigating.
* **Biological plausibility**: ATP per spike is the canonical Attwell-Laughlin energy budget — APs
  consume 47% of cortical signalling ATP. The project's existing HH model substrate already exposes
  the required currents per compartment; the Na/K-overlap recipe is the standard treatment in the
  field (Sengupta et al. 2010, Hallermann et al. 2012). The objective is a hard biological
  constraint, not a soft regulariser.
* **Direction of optimisation**: minimise.
* **Supporting paper citations**: [Attwell2001][attwell2001], [Sengupta2010][sengupta2010],
  [Carter2009][carter2009], [Hallermann2012][hallermann2012], [Niven2008][niven2008],
  [Remme2018][remme2018].

### cytoplasm_volume

* **Name**: `cytoplasm_volume`
* **Mathematical formula**: $V_{\text{cyto}} = \sum_{i \in \text{compartments}} \pi r_i^2 L_i$ where
  $r_i$ is the radius of compartment $i$ (NEURON `seg.diam / 2` in micrometres) and $L_i$ is the
  segment length in micrometres. Optional alternative formulations: total surface area
  $A_{\text{tot}} = \sum_i 2 \pi r_i L_i$ in $\mu\text{m}^2$, and bare wiring cost $W = \sum_i L_i$
  in $\mu\text{m}$ (the latter ignores diameters).
* **Units**: cubic micrometres ($\mu\text{m}^3$).
* **NEURON-side quantities required**: per-section `diam` (or per-segment `seg.diam` after enforcing
  variable nseg) and `L`. The procedural morphology generator that t0091 uses already exposes these
  for every section.
* **Recipe** (4 steps):
  1. Enforce <=20 um per compartment by setting `nseg = max(1, int(L / 20.0))` per section. This
     follows the Hines and Carnevale 1997 / Hay et al. 2011 convention for mesh-density invariance.
  2. Iterate over every section. For each segment in the section, accumulate $V_i = \pi
     (\text{seg.diam}/2)^2 \cdot (\text{L}/\text{nseg})$.
  3. Sum across all segments to get $V_{\text{cyto}}$. Report in $\mu\text{m}^3$.
  4. (Optional) Repeat at `nseg_max = 10 um` (double resolution) and confirm the volume changes by
     less than 5%. Larger discrepancies indicate the morphology generator is producing tapered
     sections that need finer discretisation.
* **Biological plausibility**: cytoplasm volume is one half of the Cajal-cytoplasm-conservation
  trade-off the cell faces against conduction time (Cuntz et al. 2010). Real arbors cluster at the
  morphology-generator balancing factor `bf` in [0.2, 0.7] across fly LPTCs, mammalian CA1 pyramidal
  cells, and cerebellar Purkinje cells. The 3/5-of-grey-matter wiring rule (Chklovskii et al. 2002)
  makes the evolutionary justification explicit. **Novel contribution annotation**: no paper in the
  surveyed literature implements cytoplasm volume as an *explicit* MOO target on a single-neuron
  compartmental fit. Cuntz et al. 2010 use it as a generator constraint, not as an optimisation
  objective. The project has a genuine opportunity to produce a methodologically novel result by
  running DSI vs cytoplasm-volume MOBO on its existing DSGC substrate.
* **Direction of optimisation**: minimise.
* **Supporting paper citations**: [Cuntz2010][cuntz2010], [Chklovskii2002][chklovskii2002],
  [Cherniak1992][cherniak1992], [LondonHausser2005][londonhausser2005], [Hines1997][hines1997].

### robustness_under_perturbation

* **Name**: `robustness_under_perturbation`

* **Mathematical formula** (display form):

  ```latex
  R(\theta) = \operatorname{std}_{k=1..K} \mathrm{DSI}(\theta + \delta_k)
  ```

  with $\delta_k \sim \operatorname{Uniform}(-0.10\,\theta, +0.10\,\theta)$ applied independently
  per parameter. Equivalent below-threshold form:

  ```latex
  R_{\text{thresh}}(\theta) = \frac{1}{K} \sum_{k=1}^{K}
      \mathbb{1}\bigl[\mathrm{DSI}(\theta + \delta_k) < \mathrm{DSI}(\theta) - \tau\bigr]
  ```

  for a threshold $\tau$ (recommended $\tau = 0.1$).

* **Units**: dimensionless ratio (DSI is itself dimensionless).

* **NEURON-side quantities required**: a re-evaluable simulation pipeline that produces DSI from the
  8-direction trial output for arbitrary parameter vectors. The project's t0091 evaluator already
  provides this.

* **Recipe** (5 steps):
  1. At each Pareto point $\theta$ from the NSGA-II front, sample $K \in [50, 200]$ perturbation
     vectors $\delta_k$ from $\operatorname{Uniform}(-0.10\,\theta, +0.10\,\theta)$ independently
     per parameter.
  2. For each $\delta_k$, run the project's full 8-direction 1400-ms simulation pipeline and compute
     $\mathrm{DSI}(\theta + \delta_k)$ from the response.
  3. Report $R(\theta) = \operatorname{std}_k \mathrm{DSI}(\theta + \delta_k)$ as the robustness
     objective.
  4. (Alternative) Report $R_{\text{thresh}}(\theta)$ as the fraction of perturbations whose DSI
     drops more than $\tau$ below the unperturbed value. This is more interpretable when the DSI
     distribution is heavy-tailed.
  5. (Analysis stage, post-MOBO) Run PCA on the perturbation set $\{\delta_k\}$ to expose
     compensatory directions per Goldman et al. 2001 / Olypher and Calabrese 2007. Report which
     parameter directions are compensatory (low DSI sensitivity) vs which are critical (high DSI
     sensitivity).

* **Biological plausibility**: Marder and Goaillard 2006 establish that biological robustness is
  best measured as a population statistic over a parameter manifold. Prinz et al. 2004's 20 million
  STG models, Goldman et al. 2001's compensatory directions, and Olypher and Calabrese 2007's
  implicit-function-theorem framework collectively justify the Marder-style ensemble protocol.
  Direct relevance to the researcher's recurring concern that pure-DSI maximisation admits
  non-physical solutions: a high-DSI solution that collapses under +/-10% perturbation is exactly
  the non-physical solution the joint objective rules out.

* **Direction of optimisation**: minimise the standard deviation (equivalently, maximise
  robustness).

* **Supporting paper citations**: [Marder2006][marder2006], [Prinz2004][prinz2004],
  [Goldman2001][goldman2001], [Olypher2007][olypher2007].

## Methodology Synthesis

The catalogue's methodology unifies five threads from the surveyed literature:

* **Per-feature SD-normalisation** [Druckmann2007][druckmann2007] [Hay2011][hay2011]. Express every
  objective in units of the corresponding experimental SD (or, when no experimental SD is available,
  the best-effort biological tolerance). This is the canonical solution to the "objectives in
  incompatible units" problem the catalogue faces when mixing bits/s (information), ATP/spike
  (energy), $\mu\text{m}^3$ (volume), and dimensionless DSI. For objectives without an experimental
  SD (cytoplasm volume on a procedurally generated morphology has no experimental SD per se), use a
  best-effort biological tolerance band. For ATP-per-spike, use the Sengupta et al. cross-cell-type
  range as the tolerance.

* **2-3 SD acceptance threshold and ensemble-as-experiment reporting** [Hay2011][hay2011]
  [Achard2006][achard2006]. Accept all solutions whose every feature is within 2-3 SD of the target
  rather than picking the single hypervolume-maximising point. Report the full Pareto front and the
  ensemble parameter distribution. This is the canonical reporting pattern in the field. The
  project's t0091 reporting should follow this convention, not the single-best-model convention. Use
  PCA / clustering on the ensemble parameter distribution to expose compensatory-direction structure
  [Goldman2001][goldman2001] [Olypher2007][olypher2007].

* **Loose-hyperplanes parameter-landscape interpretation** [Achard2006][achard2006]. The parameter
  landscape of acceptable solutions is a set of loosely connected hyperplanes, not a single basin.
  Grid search and random search miss these hyperplanes; only directed search (NSGA-II / NSGA-III)
  recovers them. The project's t0091 NSGA-II run on 68-d morphology + channels should report the
  hyperplane structure explicitly.

* **CellEvaluator + Protocol + EFeature structural template** [VanGeit2016][vangeit2016]
  [Gouwens2018][gouwens2018]. Adopt BluePyOpt's
  `CellEvaluator(cell_model, params, protocols, fitness_calculator)` pattern as the structural
  template for the catalogue's evaluator while keeping pymoo NSGA-II as the optimiser. This
  preserves the t0091 NSGA-II workflow while gaining eFEL-feature compatibility. Adopt eFEL
  [eFEL-GH](https://github.com/BlueBrain/eFEL) as the feature-extraction substrate for any
  catalogued objective that reduces to a per-spike or per-trace feature (spike count, AP amplitude,
  AHP depth, ISI CV, voltage base, etc.).

* **Optimiser-selection rule** [Deb2002][deb2002] [Deb2014][deb2014] [Blank2020](https://pymoo.org/)
  [Ament2023][ament2023]. Use NSGA-II via pymoo for high-d 2-3-objective problems. Use NSGA-III via
  pymoo for high-d many-objective (>3 objectives) problems; the catalogue's planned 5-way DSI + MI +
  energy + volume + robustness Pareto exceeds NSGA-II's effective range and requires NSGA-III's
  reference-point-based nondominated sorting. Use qLogNEHVI per Ament et al. 2023 only for low-d
  (<=20) constrained problems with budget for GP evaluation. **Never use canonical qNEHVI**: Ament
  et al. 2023's Theorem 1 proves the vanishing-gradient pathology renders multistart gradient-based
  optimisation effectively random as the BO loop closes its optimality gap. The project's own t0078
  budget overrun is consistent with this diagnosis.

* **Function-objective + cost-objective pairing rule** [LondonHausser2005][londonhausser2005]
  [Chklovskii2002][chklovskii2002] [Cuntz2010][cuntz2010]. Pair every function objective with at
  least one biological-cost objective. The dendritic-computation literature converges on this rule
  because lone function objectives admit non-physical solutions. The catalogue's recommended pairs:
  DSI vs cytoplasm volume, DSI vs ATP-per-spike, MI vs ATP-per-spike, DSI vs robustness, MI vs
  cytoplasm volume.

* **Hypervolume + IGD as convergence indicators** [Blank2020](https://pymoo.org/)
  [Zitzler1999](https://ieeexplore.ieee.org/document/797969/) [Deb2014][deb2014]. Use hypervolume as
  the primary convergence indicator with a fixed reference point above the worst observed values per
  objective; supplement with IGD when a reference Pareto front is available. pymoo's
  `pymoo.indicators.hv.HV` and `pymoo.indicators.igd.IGD` are drop-in.

## Additional Catalogued Objectives

Two well-defined additional objective categories surfaced beyond the four mandatory ones. They are
ranked by biological plausibility and computational feasibility on the project's existing
infrastructure.

### coincidence_detection_accuracy

* **Name**: `coincidence_detection_accuracy`
* **Mathematical formula**: $A_{\text{coinc}} = P(\text{spike} \mid \text{coincident}) -
  P(\text{spike} \mid \text{non-coincident})$ where coincident inputs are PD+ND synaptic events
  arriving within a window $\Delta t \le 1$ ms and non-coincident events arrive separated by $> 5$
  ms. The headline number is the difference in spike-output probability under the two input regimes.
* **Units**: dimensionless probability difference (range $[-1, 1]$, biologically positive).
* **NEURON-side quantities required**: paired synaptic event scheduler (PD/ND, AMPA/NMDA/GABA);
  somatic spike counter; ability to manipulate inter-event delay $\Delta t$.
* **Recipe** (4 steps):
  1. For each Pareto point, run two protocols: a coincident-input protocol with PD and ND events
     synchronised to within $\Delta t \le 1$ ms; a non-coincident protocol with PD and ND events
     separated by $> 5$ ms.
  2. Repeat each protocol 100 times with frozen synaptic noise. Count somatic spikes per trial.
  3. Compute $P(\text{spike} \mid \text{coincident})$ and $P(\text{spike} \mid
     \text{non-coincident})$ as the fraction of trials with at least one spike in each protocol.
  4. Report the difference $A_{\text{coinc}}$.
* **Biological plausibility**: Remme et al. 2018's MSO coincidence-detection MOBO is the closest
  published function-vs-energy analogue to the project's planned DSI-vs-energy work. The recipe
  generalises directly. The DSGC's PD/ND synaptic asymmetry is naturally a coincidence-detection
  computation in the same sense.
* **Direction of optimisation**: maximise.
* **Supporting paper citations**: [Remme2018][remme2018], [LondonHausser2005][londonhausser2005].

### bits_per_atp_efficiency

* **Name**: `bits_per_atp_efficiency`
* **Mathematical formula**: $\eta_{\text{bits/ATP}} = I(D; S) / E_{\text{trial}}$ where $I(D; S)$ is
  the mutual information rate from `mutual_information_stimulus_spike_train` (in bits/s) and
  $E_{\text{trial}}$ is the total ATP-per-trial from `metabolic_energy_atp_per_spike` (sum across
  all 8 directions, in ATP per trial, divided by trial duration to get ATP/s).
* **Units**: bits per ATP molecule.
* **NEURON-side quantities required**: same as the two parent objectives combined.
* **Recipe** (3 steps):
  1. Run `mutual_information_stimulus_spike_train` recipe to get $I(D; S)$ in bits/s.
  2. Run `metabolic_energy_atp_per_spike` recipe to get total ATP per trial; divide by trial
     duration (1.4 s for t0091's 8x 175 ms protocol; or by total trial duration if the protocol
     differs) to get ATP/s.
  3. Take the ratio $\eta_{\text{bits/ATP}} = I(D; S) / (\text{ATP}/s)$.
* **Biological plausibility**: Niven et al. 2007 measured this ratio across four fly species,
  recovering the canonical empirical bits-per-ATP Pareto curve in the literature: photoreceptor
  information rates from 200 bits/s (D. melanogaster) to 1000 bits/s (S. carnaria) scale
  super-linearly with ATP cost, with a fixed cost of ~20% of maximum consumption. The DSGC
  bits-per-ATP ratio should be benchmarked against this curve.
* **Direction of optimisation**: maximise.
* **Supporting paper citations**: [Niven2007][niven2007], [Niven2008][niven2008],
  [Sengupta2010][sengupta2010].

Three further candidates (`spike_train_distance` per Victor and Purpura 1997,
`parameter_manifold_dimension` per Olypher and Calabrese 2007, and a Druckmann-style aggregate
`feature_sd_score` per Druckmann et al. 2007 / Hay et al. 2011) are listed but not detailed because
they either (a) duplicate the information in `mutual_information_stimulus_spike_train` (spike-train
distance is a binning-free alternative MI surrogate) or (b) are methodology-level rather than
biology-level objectives (parameter-manifold dimension and feature-SD-score are useful for
analysis-stage reporting but not as primary MOBO objectives in the catalogue's sense).

## Recommended Future MOBO Tasks

Five ranked future MOBO task suggestions, ordered by combined biological plausibility + budget
feasibility. Each is implementable on top of the project's existing pymoo NSGA-II infrastructure
(validated by t0091) without infrastructure rewrites.

### 1. Bed B NSGA-II maximising DSI and minimising cytoplasm volume

* **Title**: Bed B NSGA-II maximising DSI and minimising cytoplasm volume.
* **Kind**: experiment.
* **Priority**: high.
* **Categories**: `compartmental-modeling`, `dendritic-computation`.
* **Objectives optimised**: DSI (maximise) vs `cytoplasm_volume` (minimise).
* **Source paper**: [Cuntz2010][cuntz2010], [Chklovskii2002][chklovskii2002] (cost objective
  grounding); the project's own t0091 (DSI evaluator).
* **Biological plausibility**: highest. Cytoplasm volume is the most evolutionarily grounded cost
  objective in the catalogue (Cajal cytoplasm-conservation, 3/5-of-grey-matter wiring rule). The
  infrastructure is already in place via the procedural morphology generator validated in t0093. The
  high-DSI corner of the front should cluster at `bf` in [0.2, 0.7], a falsifiable prediction.
* **Budget feasibility**: 12-24 h on Vast.ai EPYC 7763 with 64 cores at $0.30/h, total cost $4-8
  within the per-task default $5 limit (assuming budget bump to $8 if needed). Same population and
  generation budget as t0091.
* **Cross-references**: [`cytoplasm_volume`](#cytoplasm_volume).

### 2. Bed B NSGA-II maximising DSI and minimising ATP-per-spike

* **Title**: Bed B NSGA-II maximising DSI and minimising ATP-per-spike.
* **Kind**: experiment.
* **Priority**: high.
* **Categories**: `compartmental-modeling`, `voltage-gated-channels`.
* **Objectives optimised**: DSI (maximise) vs `metabolic_energy_atp_per_spike` (minimise).
* **Source paper**: [Sengupta2010][sengupta2010], [Carter2009][carter2009],
  [Hallermann2012][hallermann2012] (recipe and validation benchmarks); [Remme2018][remme2018]
  (closest published function-vs-energy MOBO analogue); [Attwell2001][attwell2001] (energy budget).
* **Biological plausibility**: high. ATP per spike is the canonical Attwell-Laughlin energy budget;
  APs consume 47% of cortical signalling ATP. Remme et al. 2018 demonstrated MSO function-vs-energy
  MOBO works in NEURON, providing a methodology template that generalises directly. The DSGC's
  GABAergic-style fast-spiking behaviour should produce a Na/K-overlap penalty similar to Carter and
  Bean 2009's fast-spiking benchmark; a DSI-vs-energy front should expand toward dramatically lower
  energy as Na+ density and overlap are jointly reduced.
* **Budget feasibility**: 24-48 h on Vast.ai EPYC 7763 with 64 cores at $0.30/h, total cost $8-15.
  May exceed per-task default; flag for explicit budget approval.
* **Cross-references**: [`metabolic_energy_atp_per_spike`](#metabolic_energy_atp_per_spike).

### 3. Bed B NSGA-II maximising DSI and robustness under +/-10% channel-density perturbation

* **Title**: Bed B NSGA-II maximising DSI and robustness under +/-10% channel-density perturbation.
* **Kind**: experiment.
* **Priority**: high.
* **Categories**: `compartmental-modeling`, `voltage-gated-channels`.
* **Objectives optimised**: DSI (maximise) vs `robustness_under_perturbation` (minimise SD).
* **Source paper**: [Marder2006][marder2006], [Prinz2004][prinz2004], [Goldman2001][goldman2001],
  [Olypher2007][olypher2007].
* **Biological plausibility**: high. Directly addresses the researcher's recurring biological-
  plausibility concern with pure-DSI maximisation. Marder-style population-statistic robustness is
  the field-standard treatment. The high-DSI / high-robustness corner should lie along compensatory
  hyperplanes, falsifying the hypothesis that DSI maximisation drives the optimiser to fragile
  parameter-space extremes.
* **Budget feasibility**: 36-72 h on Vast.ai EPYC 7763 with 64 cores at $0.30/h, total cost $11-22.
  Robustness evaluation requires K=50-200 perturbation simulations per Pareto point, multiplying
  t0091's per-individual cost by 50-200. Either reduce population/generations or request a $25
  budget cap for this experiment.
* **Cross-references**: [`robustness_under_perturbation`](#robustness_under_perturbation).

### 4. Bed B NSGA-II maximising DSI and information transfer rate

* **Title**: Bed B NSGA-II maximising DSI and information transfer rate.
* **Kind**: experiment.
* **Priority**: medium.
* **Categories**: `compartmental-modeling`, `retinal-ganglion-cell`.
* **Objectives optimised**: DSI (maximise) vs `mutual_information_stimulus_spike_train` (maximise).
* **Source paper**: [Strong1998][strong1998], [Dhingra2004][dhingra2004],
  [Brenner2000][brenner2000], [Borst1999][borst1999].
* **Biological plausibility**: medium-high. The recipe is well-established (Strong-Bialek direct
  method with 1/T extrapolation) and validates against the Dhingra and Smith 2004 ~60% gray-level
  loss benchmark. However, the project's 8-direction protocol may be too information-poor (only 3
  bits of stimulus uncertainty) to give the MI estimator meaningful dynamic range; the catalogue
  should validate the recipe against the project's existing DSGC trial output before launching the
  full MOBO.
* **Budget feasibility**: 18-36 h on Vast.ai EPYC 7763 with 64 cores at $0.30/h, total cost $5-11.
  MI estimation is post-hoc and adds little simulation cost vs t0091; the budget overhead is mostly
  in extra population to populate the MI Pareto direction.
* **Cross-references**:
  [`mutual_information_stimulus_spike_train`](#mutual_information_stimulus_spike_train).

### 5. Bed B NSGA-II maximising MI and minimising ATP-per-spike (bits-per-ATP front)

* **Title**: Bed B NSGA-II maximising MI and minimising ATP-per-spike.
* **Kind**: experiment.
* **Priority**: medium.
* **Categories**: `compartmental-modeling`, `voltage-gated-channels`, `retinal-ganglion-cell`.
* **Objectives optimised**: `mutual_information_stimulus_spike_train` (maximise) vs
  `metabolic_energy_atp_per_spike` (minimise). The bits-per-ATP Pareto curve directly comparable to
  Niven et al. 2007's fly photoreceptor 200-1000 bits/s super-linear cost-vs-information curve.
* **Source paper**: [Niven2007][niven2007], [Sengupta2010][sengupta2010], [Strong1998][strong1998].
* **Biological plausibility**: medium. Decouples function (information) from selectivity (DSI) and
  produces a result directly comparable to Niven et al. 2007's empirical bits-per-ATP Pareto curve.
  The DSGC bits-per-ATP ratio is unmeasured in the literature, so the experiment closes a genuine
  open question. Tradeoff: this experiment does not directly serve the project's first-question DSGC
  mission (DSI is not optimised); ranked medium because it serves a broader scientific question
  rather than the project's specific deliverable.
* **Budget feasibility**: 24-48 h on Vast.ai EPYC 7763 with 64 cores at $0.30/h, total cost $8-15.
  Comparable to suggestion 2 since both objectives reuse the same simulation outputs.
* **Cross-references**:
  [`mutual_information_stimulus_spike_train`](#mutual_information_stimulus_spike_train),
  [`metabolic_energy_atp_per_spike`](#metabolic_energy_atp_per_spike).

## Limitations

* **Cytoplasm volume has no published precedent as an explicit single-neuron MOO objective.** The
  catalogue flags it as a novel contribution (Cuntz et al. 2010 use it as a generator constraint,
  not an optimisation objective). The recipe is mathematically trivial and the biological grounding
  via Cuntz et al. 2010's `bf` band and Chklovskii et al. 2002's 3/5-of-grey-matter rule is well-
  established, but reviewers may correctly flag the absence of a published MOO precedent. The
  catalogue should be read as proposing this objective for the first time, not summarising existing
  practice.

* **Information transfer rate on an 8-direction protocol may be information-poor.** The 8-way
  stimulus has only 3 bits of input entropy, so the MI estimator's ceiling is 3 bits per trial (per
  direction-class) regardless of how good the spike train is. The recipe's validation benchmark
  (Dhingra and Smith 2004's ~60% gray-level loss) was measured on a much richer flashed-spot
  contrast stimulus set. The catalogue's MI recipe should be validated against the project's
  existing DSGC trial output before the full MOBO; if the MI estimator is saturated, the protocol
  may need to be enriched (e.g., to 16-32 directions or to a continuous-angle drift) to give the
  optimiser meaningful dynamic range on the MI axis.

* **ATP-per-spike requires per-compartment INa recording, which is heavier than t0091's existing
  trial output.** The project's standard EPSP/IPSP/FULL trio records only somatic Vm by default;
  enabling per-segment `ina` recording for every section roughly triples the per-trial output size
  and may require a tweak to the existing pipeline. The plan's Risks section flagged this; the
  catalogue's recipe is sound but the infrastructure cost should be budgeted in advance of any
  DSI-vs-energy MOBO.

* **Robustness evaluation is K=50-200x more expensive than vanilla t0091.** The Marder-style
  ensemble protocol requires re-running the full 8-direction simulation pipeline for every
  perturbation sample at every Pareto point. The catalogue should be read as defining the objective
  recipe correctly, not as guaranteeing it fits inside the project's per-task default $5 budget. The
  recommended robustness MOBO (suggestion 3) requests an explicit $25 budget cap.

* **Coincidence-detection accuracy is generalised from MSO to DSGC by analogy, not by precedent.**
  Remme et al. 2018's MSO recipe is binaural (two PD/ND inputs separated by interaural time delay);
  the DSGC PD/ND analogue uses GABA-PD vs cholinergic-ND inputs, which is a different biological
  substrate with different timing scales. The catalogue's recipe is plausible but unvalidated on
  DSGC; future work should run the recipe on the project's existing minimal-DSGC models
  (t0052/t0053/t0054) before deploying it inside an MOBO loop.

* **Bits-per-ATP efficiency does not directly serve the project's first-question DSGC mission.** It
  optimises MI vs ATP without DSI, so a bits-per-ATP solution may not be DSI-selective at all. The
  catalogue includes it for completeness because it is the canonical Niven et al. 2007 Pareto curve
  in the field, but the project should treat it as a secondary research question, not a primary
  deliverable.

* **The catalogue is a literature survey, not a benchmarking task.** No catalogued recipe was
  validated by experiment in this task; recipe validation belongs in the future MOBO task
  suggestions. The catalogue's confidence rating ("high") reflects the strength of the literature
  evidence and the simplicity of the recipes, not experimental validation on the project's
  substrate.

* **The catalogue does not cover network-level optimisation, RL/deep-learning policy optimisation,
  or phenomenological integrate-and-fire models.** These are explicitly out of scope per
  `task_description.md`. Researchers wishing to optimise multi-neuron networks should treat this
  catalogue as a single-cell building block, not a complete framework.

## Sources

### Newly catalogued papers (t0097)

* Paper: `10.3389_neuro.01.1.1.001.2007` (Druckmann et al. 2007)
* Paper: `10.1371_journal.pcbi.1002133` (Druckmann et al. 2011)
* Paper: `10.1371_journal.pcbi.0020094` (Achard and De Schutter 2006)
* Paper: `10.3389_neuro.11.001.2007` (Van Geit et al. 2007)
* Paper: `10.3389_fninf.2016.00017` (Van Geit et al. 2016)
* Paper: `10.1038_s41467-017-02718-3` (Gouwens et al. 2018)
* Paper: `10.1097_00004647-200110000-00001` (Attwell and Laughlin 2001)
* Paper: `10.1242_jeb.017574` (Niven and Laughlin 2008)
* Paper: `10.1371_journal.pcbi.1000840` (Sengupta et al. 2010)
* Paper: `10.1016_j.neuron.2009.12.011` (Carter and Bean 2009)
* Paper: `10.1038_nn.3132` (Hallermann et al. 2012)
* Paper: `10.1371_journal.pbio.0050116` (Niven et al. 2007)
* Paper: `10.1371_journal.pcbi.1006612` (Remme et al. 2018)
* Paper: `10.1038_nrn1949` (Marder and Goaillard 2006)
* Paper: `10.1038_nn1352` (Prinz et al. 2004)
* Paper: `10.1523_JNEUROSCI.21-14-05229.2001` (Goldman et al. 2001)
* Paper: `10.1152_jn.00842.2007` (Olypher and Calabrese 2007)
* Paper: `10.1103_PhysRevLett.80.197` (Strong et al. 1998)
* Paper: `10.1038_14731` (Borst and Theunissen 1999)
* Paper: `10.1162_089976600300015259` (Brenner et al. 2000)
* Paper: `10.1016_S0896-6273(02)00679-7` (Chklovskii et al. 2002)

### Corpus papers (cited from prior tasks)

* Paper: `10.1371_journal.pcbi.1002107` (Hay et al. 2011, in t0078)
* Paper: `10.1371_journal.pcbi.1000877` (Cuntz et al. 2010, in t0027)
* Paper: `no-doi_Ament2023_logei-bo` (Ament et al. 2023, in t0078)
* Paper: `10.1523_jneurosci.5346-03.2004` (Dhingra and Smith 2004, in t0015)
* Paper: `10.1098_rstb.1982.0084` (Koch and Poggio 1982, in t0015)
* Paper: `10.1038_382363a0` (Mainen and Sejnowski 1996, in t0015)
* Paper: `10.1152_jn.1997.78.4.1948` (Fohlmeister and Miller 1997, in t0019)
* Paper: `10.1162_neco.1997.9.6.1179` (Hines and Carnevale 1997, in t0002)
* Paper: `10.1146_annurev.neuro.28.061604.135703` (London and Hausser 2005, in t0016)

### Tasks

* Task: `t0091_morphology_extended_nsga2_v1` (the catalogue's downstream consumer)

### URLs

* URL: <https://github.com/BlueBrain/BluePyOpt>
* URL: <https://bluepyopt.readthedocs.io/en/latest/index.html>
* URL: <https://github.com/BlueBrain/eFEL>
* URL: <https://pymoo.org/>
* URL: <https://allensdk.readthedocs.io/en/latest/biophysical_models.html>

### Markdown reference link definitions

[druckmann2007]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md
[druckmann2011]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1002133/summary.md
[achard2006]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/summary.md
[vangeit2007]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.3389_neuro.11.001.2007/summary.md
[vangeit2016]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.3389_fninf.2016.00017/summary.md
[gouwens2018]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_s41467-017-02718-3/summary.md
[attwell2001]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/summary.md
[niven2008]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1242_jeb.017574/summary.md
[sengupta2010]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/summary.md
[carter2009]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1016_j.neuron.2009.12.011/summary.md
[hallermann2012]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_nn.3132/summary.md
[niven2007]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pbio.0050116/summary.md
[remme2018]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1006612/summary.md
[marder2006]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_nrn1949/summary.md
[prinz2004]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_nn1352/summary.md
[goldman2001]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1523_JNEUROSCI.21-14-05229.2001/summary.md
[olypher2007]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1152_jn.00842.2007/summary.md
[strong1998]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1103_PhysRevLett.80.197/summary.md
[borst1999]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_14731/summary.md
[brenner2000]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1162_089976600300015259/summary.md
[chklovskii2002]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1016_S0896-6273(02)00679-7/summary.md
[cherniak1992]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1007_BF00204115/summary.md
[hay2011]: ../../../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md
[cuntz2010]: ../../../../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000877/summary.md
[ament2023]: ../../../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/no-doi_Ament2023_logei-bo/summary.md
[dhingra2004]: ../../../../../tasks/t0015_literature_survey_cable_theory/assets/paper/10.1523_jneurosci.5346-03.2004/summary.md
[kochpoggio1982]: ../../../../../tasks/t0015_literature_survey_cable_theory/assets/paper/10.1098_rstb.1982.0084/summary.md
[mainen1996]: ../../../../../tasks/t0015_literature_survey_cable_theory/assets/paper/10.1038_382363a0/summary.md
[fohlmeistermiller1997]: ../../../../../tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1152_jn.1997.78.4.1948/summary.md
[hines1997]: ../../../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/summary.md
[londonhausser2005]: ../../../../../tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1146_annurev.neuro.28.061604.135703/summary.md
[victor1997]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1088_0954-898X_8_2_003/summary.md
[deb2002]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1109_4235.996017/summary.md
[deb2014]: ../../../../../tasks/t0097_multi_obj_optim/assets/paper/10.1109_TEVC.2013.2281535/summary.md
[blank2020]: <https://pymoo.org/>
[zitzler1999]: <https://ieeexplore.ieee.org/document/797969/>
[bluepyopt-gh]: <https://github.com/BlueBrain/BluePyOpt>
[bluepyopt-docs]: <https://bluepyopt.readthedocs.io/en/latest/index.html>
[efel-gh]: <https://github.com/BlueBrain/eFEL>
[pymoo-docs]: <https://pymoo.org/>
[allensdk-docs]: <https://allensdk.readthedocs.io/en/latest/biophysical_models.html>
[t0091]: ../../../../../tasks/t0091_morphology_extended_nsga2_v1/
