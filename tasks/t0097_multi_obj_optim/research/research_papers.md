---
spec_version: "1"
task_id: "t0097_multi_obj_optim"
research_stage: "papers"
papers_reviewed: 22
papers_cited: 9
categories_consulted:
  - "compartmental-modeling"
  - "dendritic-computation"
  - "cable-theory"
  - "voltage-gated-channels"
  - "retinal-ganglion-cell"
date_completed: "2026-05-08"
status: "partial"
---
## Task Objective

This task is a literature survey of multi-objective optimisation (MOO) of single-neuron
compartmental models, broadening the project beyond the DSI-plus-firing-rate objective pair used in
every prior MOBO/MOEA task here (t0076, t0078, t0080, t0081, t0083, t0086, t0091). The deliverable
is a catalogue of every objective function used in the published single-neuron MOO literature with
formula, units, NEURON-side computational recipe, and biological plausibility notes, together with a
ranked list of future MOBO tasks this project should commission. Four objective categories are
mandatory in the catalogue: information transfer rate, metabolic energy / ATP per spike, cytoplasm
volume / wiring cost, and robustness / degeneracy. The species and cell type are unrestricted; the
must-find category list is what scopes the survey.

The frontmatter `status` is `partial` because the project's existing paper corpus is dominated by
DSGC/direction-selectivity work (see the Gaps and Limitations section). Only a small fraction of the
already-downloaded papers genuinely address the survey's methodological scope. The bulk of the
methodology and biological-objective literature for this survey will come from the next stage,
`research-internet`, which will pull in Druckmann 2007/2011, Achard & De Schutter 2006,
BluePyOpt/Van Geit, Attwell & Laughlin 2001, Niven & Laughlin 2008, Sengupta et al. 2010, Marder &
Goaillard 2006, Prinz, Bucher & Marder 2004, and the Bialek/Strong/De Ruyter van Steveninck
information-theory canon. This file documents only what the existing corpus genuinely contributes.

## Category Selection Rationale

Five categories from `meta/categories/` were consulted: `compartmental-modeling` (the fundamental
substrate of every paper relevant to single-neuron MOO), `dendritic-computation` (overlaps with
wiring economy and morphology-vs-function trade-offs), `cable-theory` (overlaps with
cytoplasm-volume and electrotonic-compartmentalisation reasoning), `voltage-gated-channels` (because
ATP-per-spike is computed from HH ionic currents), and `retinal-ganglion-cell` (because the
project's downstream consumer is a DSGC and the only existing information-transfer-rate measurement
in the corpus, Dhingra & Smith 2004, is in an RGC).

Excluded categories: `direction-selectivity` was scanned but contributes only DSGC-mechanism papers
that do not address MOO methodology or biological objective functions; the few papers that do touch
multi-objective fitting (e.g., Hay et al. 2011) live under `compartmental-modeling`. `patch-clamp`
and `synaptic-integration` were briefly inspected but their papers are data-acquisition-focused and
do not address optimisation methodology. The project does not yet have dedicated categories for
`multi-objective-optimisation`, `metabolic-energy`, `wiring-economy`, or `information-theory`; the
research-internet stage should propose these as new categories if the catalogue grows large enough
to warrant them.

## Key Findings

### Multi-Objective Optimisation Is the Standard for Conductance-Based Single-Neuron Fits

The corpus contains exactly one canonical methodology paper that uses MOO end-to-end on a
compartmental model: Hay et al. 2011 [Hay2011]. They fit conductance densities of nine ion channels
plus Ca-buffer parameters in a thick-tufted L5b pyramidal cell to **20 firing-feature objectives**
(10 perisomatic step-current features, 10 BAP-activated Ca-spike "BAC" features), each expressed in
units of the corresponding experimental SD. The optimiser is an elitist non-dominated sorting
evolutionary algorithm — the same NSGA-style algorithm pymoo currently runs in t0091 — with
**population 1000, 500 generations, 22 free parameters, 240-1024 CPU cores, 2-5 days of wall
clock**. Models are accepted when every feature lies within **2-3 SD** of the experimental mean. The
published artefact is a set of about **2000 acceptable models** (ModelDB accession 139653) that
serve as a Pareto-acceptable ensemble rather than a single best fit.

[Hay2011] establishes a methodology pattern that this project's t0078, t0080 and t0091 already
inherit indirectly through BluePyOpt-derived MOD files, but with a much broader objective set than
the project's current DSI+firing-rate pair. Two single-target sub-fits in the same paper give a
quantitative case for joint optimisation: BAC-only fitting yields **899 acceptable models** but
those models then fail perisomatic targets (e.g., the example BAC-only fit had apical Nat density
**82.5 pS/um^2** below the BAC-acceptable range of **101-133.5 pS/um^2** when the perisomatic
constraint was added back in); perisomatic-only fitting yields only **52 acceptable models**. The
two single-target acceptable sets do not overlap on the joint feature space. **Best practice**: when
a project has two distinct firing regimes or two distinct physiological constraints, fit both
jointly under MOO rather than fitting one and validating against the other.

The acquisition-function side of the methodology has moved on since 2011. The current
state-of-the-art for noisy multi-objective Bayesian optimisation is **qLogNEHVI** [Ament2023], which
fixes a vanishing-gradient pathology in the canonical EHVI/qNEHVI used by BoTorch. Across
benchmarks, canonical qNEHVI plateaus while qLogNEHVI continues to improve (e.g., on a 30D
multi-objective cell-network problem, qLogEHVI reaches a hypervolume of **about 0.06** vs canonical
qEHVI topping out near **0.04**; on 16D Ackley with batch q=32, joint-optimised qLogEI matches or
exceeds sequential-greedy qLogEI). [Ament2023] proves (Theorem 1) that as the BO loop closes its
optimality gap and the GP posterior becomes informative, canonical EI's argument falls into a
floating-point regime where the function evaluates to literal zero across most of the domain and
multistart gradient-based optimisation degenerates into random search. **Hypothesis**: the
inconsistent and budget-blown MOBO results in this project's t0078 (qNEHVI-based) versus its
NSGA-II-based replacements (t0080, t0091) are at least partially attributable to this
vanishing-gradient pathology rather than a fundamental algorithmic deficit of EI-family acquisitions
— this is exactly the failure mode [Ament2023] documents, and it is the reason the personal-memory
note from earlier MOBO follow-ups recommends NSGA-II via pymoo for >40-d problems instead of BoTorch
qLogNEHVI.

### Cytoplasm Volume / Wiring Economy as a Biological Objective

[Cuntz2010] gives the only formal cytoplasm-volume objective function in the existing corpus, and it
does so as Cajal's law of conservation of cytoplasm. Their core construction grows a dendritic arbor
as the solution to a locally optimised graph that simultaneously minimises (i) total wiring length
(sum of segment lengths, i.e., a stand-in for total cytoplasm volume since the diameters are
assigned post-hoc by Rall's 3/2 rule) and (ii) path length from the root to every carrier point. The
two costs are combined into a single scalar objective:

```text
total_cost = wiring_cost + bf * path_length_cost
```

with `bf` a balancing factor weighing material cost against conduction time. **Best practice** from
[Cuntz2010]: across fly LPTCs, mammalian CA1 pyramidal cells and cerebellar Purkinje cells,
biologically realistic arbors cluster at **bf in [0.2, 0.7]**; the limits **bf = 0** (pure
minimum-spanning-tree, maximally branched, minimum cytoplasm) and **bf -> infinity** (star graph
from root, minimum conduction time, maximum cytoplasm) are unphysical. Synthetic Cuntz arbors match
real reconstructions on **total dendritic length within a few percent** when grown on the real
cell's spanning-field density profile.

[Cuntz2010]'s construction directly grounds the catalogue's `cytoplasm_volume` objective in biology:
cytoplasm-cost is not just a regulariser, it is one half of an actual evolutionary trade-off the
cell faces against conduction time. **Hypothesis**: a Pareto front jointly optimising DSI against
cytoplasm volume on a procedurally generated DSGC morphology will trace out the same
material-vs-time balancing curve [Cuntz2010] documents on natural arbors, with the highest-DSI
solutions clustering at **bf** values consistent with real DSGC reconstructions. Recipe (per
compartment): cytoplasm volume = sum over compartments of `pi * r^2 * L` where `r` and `L` are the
NEURON section radius and length. Wiring cost as an alternative is just the bare sum of `L`,
ignoring diameters; surface area as a third alternative is sum of `2 * pi * r * L`.

[KochPoggio1982] provides historical context: the very first formal cable-theoretic argument that
**dendritic morphology has a functional interpretation** rather than being arbitrary uses passive
cable theory on cat retinal ganglion cells with **R_i = 70 ohm.cm, C_m = 2 uF/cm^2, R_m = 2500
ohm.cm^2** to argue that branching geometry plus shunting inhibition can compute direction
selectivity. Together with [Mainen1996], which shows that dendritic morphology alone is sufficient
to determine firing pattern (regular-spiking vs bursting vs fast-spiking) when the same channel set
is distributed across all morphologies, these papers motivate **morphology as a legitimate free axis
in any multi-objective single-neuron fit**. They do not themselves use MOO, but they demolish the
alternative position that morphology is an irrelevant fixed background in conductance-density
optimisation. [FohlmeisterMiller1997] reinforces the same point in the project's home cell type
(amphibian RGC): cell geometry (soma-dendritic-axon proportions) controls the f-I curve in
multicompartmental ganglion-cell models with five nonlinear ion channels plus leak.

### Information Transfer Rate from a Retinal Ganglion Cell

[Dhingra2004] is the corpus's only direct measurement of information-transfer rate in a retinal
ganglion cell, and it provides a methodologically clean recipe that the catalogue can adopt
verbatim. The authors record intracellular sharp-electrode responses from brisk-transient guinea-pig
RGCs in flat-mounted retina at **37 deg C** to a flashed spot over the receptive-field centre, then
apply ideal-observer analysis to the graded-potential trace and to the spike train separately. Key
quantitative results: **detection threshold from graded potential = 1.5% contrast; from spikes =
3.8% contrast** (~2.5x degradation by the spike generator); **spikes carry roughly 60% fewer
distinguishable gray levels** than the graded potential; the graded-potential dipper onsets at **~2%
contrast** and the spike dipper at **~4% contrast**. The information loss is dominated by the
spike-generator threshold nonlinearity, not by stochastic noise. Critically, [Dhingra2004] documents
an explicit trade-off: **depolarisation reduces detection threshold but also reduces dynamic range**
— a Pareto trade-off in the same RGC type the project simulates.

For a t0091-style 8-direction trial-output format, the [Dhingra2004]-style recipe is: bin spike
counts in fixed time windows over the trial; compute mutual information between stimulus direction
(the discrete 8-way label) and the spike-count vector (or the graded-potential vector if HH is off,
which is exactly the EPSP/IPSP-passive trio in the project's standard simulation protocol). This is
a "direct method" estimate; the data length per direction in the project's 1400-ms fixed trial is
short, so a Strong-style extrapolation correction or a Panzeri-Treves bias correction will be needed
in the full-data regime. **Hypothesis** from [Dhingra2004]: jointly optimising DSI vs
mutual-information between stimulus angle and spike-count, on the project's 8-direction protocol,
will recover a Pareto front whose endpoints behave qualitatively like [Dhingra2004]'s depolarisation
experiment — high-DSI/low-MI extreme (over-tuned, narrow dynamic range) versus high-MI/lower-DSI
extreme (broad-tuned, full dynamic range).

### Dendritic Computation as a Scaffold for Objective-Function Design

[LondonHausser2005] is the canonical review of dendritic computation and articulates the design
space the catalogue must populate: dendrites can act as **passive cables, active spike conductors,
amplifiers, coincidence detectors, and direction-discriminators**, each with characteristic
biophysical signatures. The review does not itself use MOO, but it documents the menu of single-cell
computations that a multi-objective optimiser could optimise *for* (information transfer,
coincidence detection, directional tuning, etc.) and *against* (energy, cytoplasm, robustness). For
the catalogue, the review's value is that it justifies why information-transfer rate,
dendritic-spike-count, and direction-tuning sharpness are *all* legitimate biological objectives
rather than arbitrary engineering metrics. **Best practice** that emerges across
[LondonHausser2005], [Cuntz2010] and [KochPoggio1982]: every dendritic-computation objective should
be paired with a dendritic-cost objective (cytoplasm, wiring length, or membrane area) so the
optimiser cannot escape the trade-off by inflating the morphology arbitrarily.

### NEURON Is the Implementation Substrate Across the Field

Every methodologically relevant paper in the corpus runs in NEURON or NEURON-compatible code:
[Hay2011] explicitly uses NEURON 7.x with **Ra = 100 ohm.cm, Cm = 1 uF/cm^2 (soma/axon) or 2 uF/cm^2
(basal/apical, correcting for spines), ELeak = -90 mV, ENa = +50 mV, EK = -85 mV, EIh = -45 mV, Q10
= 2.3, junction-potential shift -10 mV**; [Cuntz2010] generates morphologies intended for direct
import into NEURON via Rall-3/2-rule diameter assignment; [Dhingra2004]'s threshold-nonlinearity
model is a one-compartment HH spike generator. The project's existing NEURON-based pipeline
(validated end-to-end by t0091 over 68 free parameters) is the right substrate for the catalogue.
**Best practice** from [Hines1997]: discretise compartments at <= 20 um (Hay 2011 follows this
convention exactly, giving ~200 compartments per L5b PC). The same discretisation rule should be
applied to the project's procedurally generated DSGC morphologies when computing cytoplasm-volume or
wiring-cost objectives so the answer is robust to mesh-density artefacts.

## Methodology Insights

* **Pareto-acceptable ensemble, not a single best fit**: from [Hay2011] — accept all solutions
  whose every feature is within 2-3 SD of the target rather than picking the single
  hypervolume-maximising point. Report the full Pareto front and the ensemble distribution. t0091's
  reporting should follow this convention, not the single-best-model convention.

* **Per-feature SD-normalisation of objectives**: from [Hay2011] — express every objective in
  units of the corresponding experimental SD (or, when no experimental SD is available, the
  best-effort biological tolerance). This is the canonical solution to the "objectives in
  incompatible units" problem the catalogue will face when mixing bits-per-second (information),
  ATP-per-spike (energy), um^3 (volume), and dimensionless DSI.

* **NSGA-II / NSGA-III preferred over BoTorch qLogNEHVI for >= 40-dimensional MOBO**: the combined
  evidence from [Ament2023] (qLogNEHVI fixes vanishing gradients but is still GP-based and thus
  O(N^3) in the number of evaluations) and the project's own t0078 budget overrun (memory note)
  recommends NSGA-II via pymoo for the catalogue's high-d MOBO follow-ups. qLogNEHVI remains the
  right tool for low-d (<= 20) constrained problems with budget for GP evaluation.

* **`bf` in [0.2, 0.7] as the biologically realistic morphology generator range** (from
  [Cuntz2010]): the cytoplasm-vs-conduction-time balancing factor that defines biologically
  realistic dendritic arbors lives in this band. When the catalogue's wiring/cytoplasm objective is
  paired with morphology generation, the prior on `bf` should be Uniform(0.2, 0.7) rather than the
  wider engineering-default of Uniform(0, 5).

* **Information-transfer recipe from [Dhingra2004]**: bin spike counts in fixed windows; use
  ideal-observer / mutual-information between stimulus class and spike-count vector. For the
  project's 8-direction, 1400-ms trial format, expect the direct-method MI estimator to be
  bias-prone — apply Strong-style extrapolation or Panzeri-Treves NSB correction. Validate against
  [Dhingra2004]'s ~60% gray-level loss as a sanity check on the spike-generator-induced MI
  reduction.

* **Cytoplasm-volume recipe**: sum over NEURON sections of `pi * r^2 * L` after discretising every
  section to <= 20 um per compartment ([Hines1997]/[Hay2011] convention). For the project's
  procedurally generated morphologies, the morphology generator already has access to all
  per-section radii and lengths, so the objective is a one-line computation in the existing
  morphology code.

* **Discretisation invariance check**: any catalogue objective that integrates over the morphology
  (cytoplasm, wiring, surface area, ATP-from-currents) must be regression-tested across two
  compartment-density settings (e.g., 20 um and 10 um). [Hay2011]'s 20-um convention is the floor;
  doubling resolution should not change the objective by more than a few percent or the recipe needs
  revisiting.

* **Robustness as an explicit objective rather than a sanity check**: although no paper in the
  existing corpus implements a Marder-style perturbation-sensitivity objective, the parameter-band
  analysis [Hay2011] performs on the Pareto-acceptable ensemble (e.g., apical Nat acceptable in
  [101, 133.5] pS/um^2 for BAC firing) is the same idea. The catalogue should include "DSI standard
  deviation under +/- 10% perturbation of all channel densities" as a robustness objective, computed
  from a small Monte Carlo sample around each Pareto point in the final reporting stage.

## Gaps and Limitations

* **No methodology paper on Druckmann-style multi-objective single-neuron optimisation in the
  corpus**: the canonical Druckmann 2007 ("A novel multiple objective optimization framework for
  constraining conductance-based neuron models by experimental data") and Druckmann 2011 (eFEL
  precursor) are not yet downloaded. These are the most-cited methodology references in the field
  and the research-internet stage must download both. Achard & De Schutter 2006 (first MOEA Purkinje
  fit) and Van Geit / NeuroFitter / BluePyOpt are also missing. This is the single largest gap.

* **No biological energy-budget paper in the corpus**: Attwell & Laughlin 2001 ("An energy budget
  for signaling in the grey matter of the brain"), Niven & Laughlin 2008 ("Energy limitation as a
  selective pressure on the evolution of sensory systems"), and Sengupta et al. 2010 ("Action
  potential energy efficiency varies among neuron types in vertebrates and invertebrates") are
  absent. The catalogue's `metabolic_energy_per_spike` recipe will have to be reconstructed from
  research-internet sources. Only the HH-current substrate that lets us *implement* the recipe
  (e.g., [Hay2011], [FohlmeisterMiller1997]) is in the corpus.

* **No robustness/degeneracy paper in the corpus**: Marder & Goaillard 2006 ("Variability,
  compensation and homeostasis in neuron and network function") and Prinz, Bucher & Marder 2004
  ("Similar network activity from disparate circuit parameters") are absent. The
  `robustness_under_perturbation` recipe will have to come entirely from research-internet.

* **No information-theory canon in the corpus**: Bialek's spike-train mutual-information work,
  Strong et al.'s "Entropy and information in neural spike trains" (the direct-method and
  extrapolation-correction reference), Brunel & Nadal's Fisher-information / discrimination-capacity
  framework, and Victor & Purpura / van Rossum spike-train metrics are all absent. [Dhingra2004]'s
  ideal-observer recipe is the only existing anchor and it is RGC-specific, not a general framework.
  Research-internet must close this gap.

* **No wiring-cost / cytoplasm-volume measurement on real DSGC morphology**: [Cuntz2010] grows
  synthetic arbors but does not ground-truth cytoplasm volume against real DSGC reconstructions.
  This is a true open question in the field and the catalogue should flag it as such — the
  project's own DSGC morphologies (t0005/t0008/t0009/t0023/t0024/t0033) are an opportunity to
  produce that measurement as a side effect of the catalogued objective implementation.

* **Existing corpus is DSGC-dominated**: of the 22 papers reviewed, only 9 are cited here. Most of
  the rest are DSGC-mechanism papers (Hanson 2019, Poleg-Polsky & Diamond 2016, Vaney 2012, Sivyer
  2010/2013, Sethuramanujam 2016/2017, Park 2014, Briggman 2011, Ding 2016, Trenholm 2013, Wienbar
  2022, Riccitelli 2025, etc.) that are highly relevant to DSI as an objective but do not themselves
  use MOO and do not introduce new objective functions. This is consistent with the task's explicit
  warning: the bulk of the t0097 literature must come from research-internet.

* **No paper in the corpus uses both DSI and a non-DSI objective in a multi-objective Pareto
  setup**: the canonical "DSI vs <X>" pairs the catalogue must populate (X in
  {information-transfer-rate, ATP-per-spike, cytoplasm-volume, robustness}) are not represented yet.
  This is the open research gap the catalogue itself is designed to fill, and the research-internet
  stage should preferentially seek out *any* paper that pairs DSI (or any selectivity index) with
  energy or wiring or robustness, even outside the retina.

## Recommendations for This Task

1. **Treat the existing corpus as a methodology and cell-substrate baseline only**: the answer
   asset's MOO-methodology section will draw heavily from [Hay2011] (joint perisomatic+BAC fit,
   ensemble-as-experiment analysis, 22-parameter NSGA-II, 2-3 SD acceptance threshold) and from
   [Ament2023] (qLogNEHVI replacement for canonical qNEHVI; vanishing-gradient diagnosis). For the
   four mandatory objective categories, defer biological-objective-origin sourcing to
   research-internet.

2. **Implement the cytoplasm-volume objective from [Cuntz2010]'s Cajal-cytoplasm-conservation
   formula**: `volume = sum over compartments of pi * r^2 * L`. Validate by reproducing
   [Cuntz2010]'s claim that biologically realistic Cuntz-MST trees recover total dendritic length
   within a few percent of real reconstructions when grown on the matching density profile. Use
   [Cuntz2010]'s `bf in [0.2, 0.7]` as the biologically realistic prior for procedural morphology
   generation in any future joint DSI-vs-volume MOBO.

3. **Adopt [Dhingra2004]'s ideal-observer recipe as the base information-transfer-rate estimator**:
   bin spike counts per direction; compute MI between stimulus class and spike-count vector; correct
   for short-data bias with Strong extrapolation or NSB. Use the project's existing 8-direction,
   1400-ms trial output directly. Validate against [Dhingra2004]'s ~60% gray-level loss as a sanity
   check.

4. **Adopt [Hay2011]'s per-feature-SD normalisation and Pareto-acceptable-ensemble reporting**:
   express every objective in units of the corresponding experimental SD (or biological tolerance
   when SD is unavailable); report the full Pareto front and the ensemble parameter distribution
   rather than the single hypervolume-maximising point. This is the canonical reporting pattern in
   the field.

5. **Recommend NSGA-II via pymoo over BoTorch qLogNEHVI for any catalogued >40-dimensional MOBO
   follow-up**: based on [Ament2023]'s diagnosis that qLogNEHVI still relies on a GP (O(N^3)
   scaling) and on the project's own t0078 budget overrun. Reserve qLogNEHVI for low-d (<= 20)
   constrained MOBO where the GP cost is bearable.

6. **Defer to research-internet for the energy, robustness, and information-theory canon**: the
   answer asset's per-objective recipes for ATP-per-spike, parameter-perturbation robustness, and
   stimulus-spike mutual-information all require sources not in the existing corpus. The
   research-internet stage must download Attwell & Laughlin 2001, Niven & Laughlin 2008, Sengupta et
   al. 2010, Marder & Goaillard 2006, Prinz, Bucher & Marder 2004, Druckmann 2007/2011, Achard & De
   Schutter 2006, Strong et al. 1998, and Bialek/De Ruyter van Steveninck spike-train MI papers.
   Without these, the catalogue will be incomplete.

7. **Flag cytoplasm volume as a novel objective contribution**: no paper in the existing corpus has
   *implemented* cytoplasm volume as an explicit MOO objective in a single-neuron compartmental fit.
   [Cuntz2010] uses it as a generator constraint, not as an optimisation target. The project has a
   genuine opportunity to produce a methodologically novel result by running DSI vs cytoplasm-volume
   MOBO on its existing DSGC substrate, even if research-internet does not turn up a published
   precedent.

## Paper Index

### [Hay2011]

* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`, `dendritic-computation`
* **Relevance**: Canonical multi-objective optimisation reference for conductance-based
  single-neuron models. 20-objective NSGA-style fit of L5b pyramidal cells with population 1000, 500
  generations, 22 free parameters, 2-3 SD acceptance threshold, and ensemble-as-experiment parameter
  analysis. The methodology template t0091 already inherits.

### [Cuntz2010]

* **Title**: One Rule to Grow Them All: A General Theory of Neuronal Branching and Its Practical
  Application
* **Authors**: Cuntz, H., Forstner, F., Borst, A., Hausser, M.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000877`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000877/`
* **Categories**: `compartmental-modeling`, `dendritic-computation`, `cable-theory`
* **Relevance**: Cajal-cytoplasm-conservation grounding for the cytoplasm-volume objective. Defines
  the wiring vs path-length trade-off via the balancing factor `bf`, with biologically realistic
  arbors clustering at `bf` in [0.2, 0.7]. Directly supplies the catalogue's cytoplasm-volume recipe
  and the morphology-generator prior for downstream joint DSI-vs-volume MOBO.

### [Ament2023]

* **Title**: Unexpected Improvements to Expected Improvement for Bayesian Optimization
* **Authors**: Ament, S., Daulton, S., Eriksson, D., Balandat, M., Bakshy, E.
* **Year**: 2023
* **DOI**: `no-doi_Ament2023_logei-bo`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/no-doi_Ament2023_logei-bo/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Diagnoses and fixes the vanishing-gradient pathology of the canonical EHVI/qNEHVI
  acquisition functions used in BoTorch. qLogNEHVI is the drop-in replacement for any future
  BO-based catalogued MOBO; together with the project's own NSGA-II preference for high-d problems,
  this paper sets the optimiser-selection rule in the answer asset.

### [Dhingra2004]

* **Title**: Spike Generator Limits Efficiency of Information Transfer in a Retinal Ganglion Cell
* **Authors**: Dhingra, N. K., Smith, R. G.
* **Year**: 2004
* **DOI**: `10.1523/jneurosci.5346-03.2004`
* **Asset**:
  `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1523_jneurosci.5346-03.2004/`
* **Categories**: `retinal-ganglion-cell`, `voltage-gated-channels`, `compartmental-modeling`
* **Relevance**: Only direct measurement of information-transfer rate in a retinal ganglion cell in
  the existing corpus. Provides the ideal-observer recipe (1.5% vs 3.8% contrast detection threshold
  from graded potential vs spikes; ~60% gray-level loss; sensitivity-vs-dynamic-range trade-off)
  that the catalogue's `mutual_information_stimulus_spike_train` objective adopts as its base
  estimator. Directly applicable to the project's 8-direction trial format.

### [KochPoggio1982]

* **Title**: Retinal ganglion cells: a functional interpretation of dendritic morphology
* **Authors**: Koch, C., Poggio, T.
* **Year**: 1982
* **DOI**: `10.1098/rstb.1982.0084`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1098_rstb.1982.0084/`
* **Categories**: `cable-theory`, `retinal-ganglion-cell`, `dendritic-computation`
* **Relevance**: Historical anchor for the claim that dendritic morphology has a functional
  interpretation rather than being arbitrary. Justifies including morphology as a free axis in any
  catalogued multi-objective single-neuron fit and supplies canonical passive-cable parameters
  (`R_i = 70 ohm.cm, C_m = 2 uF/cm^2, R_m = 2500 ohm.cm^2`) for the project's RGC compartmental
  models.

### [Mainen1996]

* **Title**: Influence of dendritic structure on firing pattern in model neocortical neurons
* **Authors**: Mainen, Z. F., Sejnowski, T. J.
* **Year**: 1996
* **DOI**: `10.1038/382363a0`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1038_382363a0/`
* **Categories**: `cable-theory`, `dendritic-computation`, `compartmental-modeling`
* **Relevance**: Demonstrates that dendritic morphology alone determines firing pattern when the
  same channel set is distributed across all morphologies. Supports treating morphology as a free
  axis in joint MOO and justifies the cytoplasm-volume objective as biologically meaningful (the
  cell pays a real material cost that buys functionally distinct firing).

### [FohlmeisterMiller1997]

* **Title**: Mechanisms by Which Cell Geometry Controls Repetitive Impulse Firing in Retinal
  Ganglion Cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **Asset**:
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1152_jn.1997.78.4.1948/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Relevance**: Project home cell type. Five-channel multicompartmental amphibian RGC model in
  which cell geometry controls f-I behaviour. Validates that the project's existing HH-channel
  substrate is the right place to compute the catalogue's ATP-per-spike objective (Na+, K+, leak
  ionic currents are all explicitly modelled).

### [Hines1997]

* **Title**: The NEURON Simulation Environment
* **Authors**: Hines, M. L., Carnevale, N. T.
* **Year**: 1997
* **DOI**: `10.1162/neco.1997.9.6.1179`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/`
* **Categories**: `compartmental-modeling`, `cable-theory`, `voltage-gated-channels`
* **Relevance**: Canonical reference for the simulation substrate every catalogued objective will
  ultimately be evaluated on. Establishes the <= 20-um compartment discretisation convention that
  cytoplasm-volume, wiring-cost, ATP-from-currents, and surface-area objectives all depend on for
  mesh-density invariance.

### [LondonHausser2005]

* **Title**: Dendritic Computation
* **Authors**: London, M., Hausser, M.
* **Year**: 2005
* **DOI**: `10.1146/annurev.neuro.28.061604.135703`
* **Asset**:
  `tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1146_annurev.neuro.28.061604.135703/`
* **Categories**: `dendritic-computation`, `cable-theory`, `compartmental-modeling`
* **Relevance**: Canonical review of dendritic computation. Justifies why information-transfer rate,
  dendritic-spike count, coincidence detection and direction-tuning sharpness are all legitimate
  biological objectives rather than arbitrary engineering metrics, and supports the pairing rule
  that every dendritic-computation objective should be paired with a dendritic-cost objective in the
  catalogue.
