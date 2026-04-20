---
spec_version: "1"
task_id: "t0008_port_modeldb_189347"
research_stage: "papers"
papers_reviewed: 12
papers_cited: 10
categories_consulted:
  - "compartmental-modeling"
  - "direction-selectivity"
  - "dendritic-computation"
  - "retinal-ganglion-cell"
  - "synaptic-integration"
  - "voltage-gated-channels"
  - "patch-clamp"
date_completed: "2026-04-20"
status: "complete"
---
# Research: Porting ModelDB 189347 (Poleg-Polsky 2016) and Sibling DSGC Compartmental Models

## Task Objective

This task ports ModelDB 189347, the multi-compartmental NEURON model of a mouse ON-OFF DRD4 DSGC
from [PolegPolsky2016], into the project as a library asset, swaps in the calibrated morphology from
t0009, and reproduces the published tuning curve to verify the envelope (DSI **0.7-0.85**, preferred
peak **40-80 Hz**, null residual **< 10 Hz**, HWHM **60-90°**). Phase B then hunts for and surveys
sibling DSGC compartmental models (Schachter 2010, Koren 2017, Ding 2016, Hanson 2019, Jain 2020) to
decide which can be ported in addition. This literature review extracts the exact simulation
protocol, model architecture, and reported metrics from the primary paper and from every other DSGC
compartmental model in the project corpus.

## Category Selection Rationale

Consulted six categories that together cover the methodological and biological scope of this task.
`compartmental-modeling` is the methodology itself — every sibling-model paper lives here.
`direction-selectivity` filters for the functional property being reproduced.
`dendritic-computation` covers subunit integration, dendritic spikes, and NMDAR nonlinearity, all of
which constrain model architecture choices. `retinal-ganglion-cell` narrows to the target cell
class. `synaptic-integration` captures the AMPA+NMDA+GABA synaptic wiring that drives the tuning
curve. `voltage-gated-channels` is included because active dendritic vs passive dendritic
configurations are an explicit research question. Excluded `cable-theory` and `patch-clamp` as
primary filters: the task is a code-reproduction rather than a theoretical derivation, and
patch-clamp data enters only as validation targets already quoted by the modelling papers above. The
excluded categories still contribute papers that appear under multi-tag queries ([Oesch2005] has
both).

## Key Findings

### Simulation Protocol in Poleg-Polsky 2016

The canonical stimulus in [PolegPolsky2016] is a bright bar moving across the retina at **1 mm/sec**
along its long axis in **8 directions** (45° spacing), not 12 directions — the task plan's 12-angle
requirement is an extension introduced for this project. Noise-free and noisy conditions are both
tested; the noisy stimulus varies background and bar luminance independently every **50 ms** with SD
= 0%, 10%, 30%, or 50% of mean luminance. Spike responses are recorded in cell-attached
configuration (n = **25 cells** control, **21** AP5, **34** 0 Mg²⁺). The reported DSI across control
cells in noise-free conditions is unchanged by AP5 blockade (DSI statistically indistinguishable
from control, p > 0.5 paired Wilcoxon), but no single numeric control-condition peak firing rate or
HWHM is given anywhere in the text or figures I can extract from the PMC NIHMS manuscript:
Experimental Procedures values for peak firing rate, HWHM, and integration timestep are not found in
paper. The project envelope values (peak **40-80 Hz**, HWHM **60-90°**) therefore cannot be
attributed to [PolegPolsky2016] alone — they must be interpreted as project targets drawn from the
broader DSGC literature rather than reproduction of a single published curve.

The reported DSI values are **qualitative**: the paper repeatedly states DSI is preserved or reduced
without a single aggregate DSI numeric value in the main text (figures 1H, 5G, 6G, 8E use median ±
quartile box plots). Reproduction therefore requires the t0012 scoring library to score the envelope
compliance flag rather than to score an exact numeric match.

### Model Architecture in Poleg-Polsky 2016

[PolegPolsky2016] documents the following architecture: "Multicompartmental numerical simulations
were performed in the NEURON simulation environment using morphology of one reconstructed DSGC. The
cell was stimulated by a network of **282 presynaptic cells**, releasing simulated vesicles based on
the presynaptic membrane potential." Synaptic inputs: **177 AMPA + 177 NMDA + 177 GABA_A
+ nicotinic AChR** on ON dendrites, distributed homogeneously following [Jeon2002]. NMDAR
  conductance is voltage-dependent with Jahr-Stevens Mg²⁺ block; tested value g_NMDA = **2.5 nS**
  (Figure 3). DS is implemented by making the GABAergic conductance stronger in the null direction
  (tuned inhibition), with excitation untuned, consistent with [Park2014]. Dendrites are passive:
  "We did not detect dendritic spikes in DRD4 DSGCs, and our computer simulations did not require
  regenerative dendritic events to replicate experimentally recorded PSP and (somatic) AP responses
  and DSI values." The model therefore requires somatic Nav + Kv but no dendritic active
  conductances for the Phase A reproduction.

Exact passive membrane parameters (Ri, Rm, Cm) are not found in the PMC manuscript Experimental
Procedures section, which is truncated in the author-manuscript XML available in the corpus.
Ground-truth values must be read from the ModelDB 189347 source files directly during Phase A
implementation.

### Morphology-Conditioned Tuning

[PolegPolsky2016] uses a single reconstructed morphology bundled with ModelDB 189347.
[ElQuessny2021] shows that global dendritic morphology influences inhibitory tuning strength (IPSC
DSI: asymmetric vDSGCs significantly higher than symmetric nDSGCs) but does not dictate E/I spatial
organisation. This predicts that the t0009 calibrated morphology swap could quantitatively shift the
tuning curve — the task must treat envelope failure after morphology swap as a scientific result
rather than a bug. [Jain2020] localises DS computation to **~5-10 µm** dendritic subunits and shows
that CaV/NMDA nonlinearities, not somatic integration, drive the sharp output tuning.

### Role of Dendritic Spikes — Species and Subtype Specific

Mouse DRD4 DSGCs have passive dendrites in [PolegPolsky2016]. Rabbit ON-OFF DSGCs have regenerative
dendritic spikes [Oesch2005, Schachter2010]: Oesch et al. measured large **~55 mV** somatic and **~7
mV** dendritic spikelets; Schachter et al. showed that each dendritic spike initiates a somatic
spike **1:1** and that DSI is amplified from **~0.2** (PSP) to **~0.8** (spike) by local
spike-threshold nonlinearity. This disagreement between species motivates the task's Phase B
sibling-model survey: porting Schachter2010 (if its NeuronC code is available) produces a second
point on the active-dendrite dimension that the Phase A mouse model cannot cover.

### Subunit Spacing and E/I Wiring

Subunit integration scales are reported as: [Schachter2010] ~150 µm arbor radius with subunit spike
thresholds dropping from **3-4 nS** proximally to **~1 nS** distally; [Jain2020] **5-10 µm**
Ca²⁺-defined subunits; [Koren2017] ~**132 µm** full-field vs subregion stimulation spacing.
Inhibition is placed within **~20 µm** of each excitatory input in [Schachter2010], with peak
compound conductances g_exc ≈ **6.5 nS** / g_inh ≈ **3.5 nS** PD and g_exc ≈ **2.5 nS** / g_inh ≈
**6.0 nS** ND. [Hanson2019] reports a **25-30 µm** spatial offset between cholinergic excitation and
GABAergic inhibition (velocity-dependent onset offset up to **50 ms** in PD). [PolegPolsky2016]
places 177 synapses homogeneously on ON dendrites without local E-I pairing, which is the simpler
configuration the port must preserve.

### Best Practices for Reproduction

Multiple converging best practices emerge:

* Distribute synapses homogeneously on ON dendrites, **1 AMPA + 1 NMDA + 1 GABA per site**, 177
  sites total [PolegPolsky2016, Jeon2002].
* Use Jahr-Stevens Mg²⁺-block kinetics for the NMDAR conductance; physiological extracellular Mg²⁺
  is **1 mM** [PolegPolsky2016].
* Implement DS by scaling the GABA conductance higher in the null direction; keep excitation
  untuned, consistent with [Park2014]'s finding that bipolar cell inputs are not directionally
  tuned.
* Passive dendrites are sufficient for mouse DRD4 DSGC [PolegPolsky2016]; do not add dendritic
  Nav/Kv unless explicitly porting Schachter2010.
* Run **≥ 10 trials per direction** with fresh seeds
  [Jain2020 uses 7-cell averages; Hanson2019 uses 4-10 repetitions]. Task plan's 20 trials × 12
  angles is above literature floor.

**Hypothesis (testable this task)**: Swapping the ModelDB 189347 bundled morphology for the t0009
calibrated morphology will preserve envelope compliance because [ElQuessny2021] shows morphology
affects inhibitory tuning magnitude but not spatial organisation, and project RQ2 is primarily an
internal sensitivity test.

**Hypothesis (testable later)**: Adding the Schachter2010 active-dendrite configuration to the mouse
model will sharpen DSI beyond the [PolegPolsky2016] envelope upper bound, because
[Oesch2005, Schachter2010] show active dendrites amplify DSI from **~0.2** (subthreshold) to
**~0.8** (spike output) in rabbit.

### Validation Targets Beyond DSI

[PolegPolsky2016] reports several quantitative subthreshold features the model must reproduce before
spike-level envelope comparison: NMDAR-mediated PD PSP component **5.8 ± 3.1 mV**, ND **3.3 ± 2.8
mV** (p = 0.001, n = 19, Figure 1D); slope of NMDAR scaling **62.5 ± 14.2°** (multiplicative) vs
expected **59.4 ± 10.7°** (Figure 1H); AP5 reduction of PD PSP **~35%** and ND PSP **~34%**
(proportional, Figure 1E); 0 Mg²⁺ produces additive scaling (slope **45.5 ± 5.3°**, Figure 5G);
high-Cl⁻ internal also produces additive scaling (slope **45.5 ± 3.7°**, Figure 4G). These are
supplementary validation checks beyond the tuning-curve envelope and are not required for Phase A
success but should appear in the answer asset.

## Methodology Insights

* **Port in two stages**: (1) download ModelDB 189347 and compile MOD files with `nrnivmodl`, then
  run the shipped demo unmodified to confirm the port is intact; (2) only after step 1 passes the
  smoke test, swap in the t0009 calibrated morphology. This ordering isolates port-breakage bugs
  from morphology-induced envelope shifts — critical because [ElQuessny2021] predicts the morphology
  swap may quantitatively shift tuning.
* **Use 8 directions in reproduction, 12 directions for envelope scoring**: The paper uses 8
  directions [PolegPolsky2016], but the envelope targets (HWHM 60-90°) require finer angular
  sampling. Run both protocols. Report the 8-direction DSI for comparison with the paper; use the
  12-direction run for envelope scoring with the t0012 library.
* **Do not implement presynaptic vesicle-release dynamics unless needed**: the paper's 282-cell
  presynaptic network with vesicle-release kinetics [PolegPolsky2016] is reproducible architecture
  detail. Check ModelDB sources first — if the published code already implements this, keep it;
  otherwise stub with per-synapse NetStim-driven spike trains and record this as a documented
  simplification.
* **NMDAR conductance calibration**: use g_NMDA = **2.5 nS** as the reference point
  [PolegPolsky2016 Figure 3]. If the port's somatic PSP amplitudes differ from paper values (PD
  NMDAR component **5.8 ± 3.1 mV**), adjust only g_NMDA, not AMPA or GABA, until PSP targets match.
* **Envelope scoring workflow**: run 12 angles × 20 seeded trials → write tuning_curve.csv with
  (angle_deg, trial_seed, firing_rate_hz) → pass to t0012 scoring library → record DSI, peak, null,
  HWHM in the answer asset's verification table.
* **Presynaptic signal shape**: [PolegPolsky2016] drives synapses via simulated vesicle release
  gated on presynaptic membrane potential, not fixed spike trains. If ModelDB 189347 bundles the
  presynaptic network, keep it. Otherwise, approximate with a 1 mm/sec bar-crossing time profile
  mapped to per-synapse NetStim activations, recording the simplification explicitly.
* **Best practice — report median and quartiles, not mean ± SD, for DSI**:
  [PolegPolsky2016, Figures 1G, 4F, 5G, 6G, 8E] consistently uses median ± quartile boxplots for DSI
  because the underlying distribution is non-Gaussian. The t0012 scoring library output should match
  this convention.
* **Skip the 0 Mg²⁺ and high-Cl⁻ controls for Phase A**: these reproduce the additive-scaling result
  [PolegPolsky2016 Figures 4, 5] but are not part of the envelope test. They can become a later
  suggestion if the ported model works.
* **Phase B model-triage rule**: for each sibling found, test `nrnivmodl` + single-angle simulation
  before committing to full reproduction. [Schachter2010] uses NeuronC (Smith lab custom solver)
  which does not run in NEURON — port feasibility is low; record it in the answer asset as a failed
  candidate. [Hanson2019] explicitly references `geoffder/Spatial-Offset-DSGC-NEURON-Model` which is
  a modified Poleg-Polsky NEURON model — high feasibility, attempt port. [Ding2016] uses Neuron-C
  (Smith lab again) — low feasibility.

## Gaps and Limitations

* **No published numeric peak firing rate or HWHM**: [PolegPolsky2016] reports DSI and PSP slopes in
  depth but never reports a peak firing rate number for the preferred direction, nor a
  half-width-at-half-maximum tuning-curve value. The project's 40-80 Hz peak and 60-90° HWHM
  envelope is therefore a project-specific target, not a paper-reproduction target, and must be
  treated as such in the answer asset (not found in paper for both values).
* **PMC author-manuscript XML truncates Experimental Procedures**: specific NEURON integration
  timestep (`dt`), specific passive membrane values (Ri, Rm, Cm), sodium/potassium channel
  densities, and synaptic decay time constants are not present in the corpus paper file. These must
  be read directly from ModelDB 189347 source code during Phase A implementation. If ModelDB source
  disagrees with the paper's narrative, the task must treat the ModelDB values as canonical (they
  are what produced the published simulations) and record the gap in the answer asset.
* **No erratum review yet**: this literature survey did not check for post-publication corrections
  to [PolegPolsky2016]. Phase A should check PubMed/publisher for any erratum before treating the
  port as complete; none of the other papers in this corpus mention one, but absence of mention is
  not evidence of absence.
* **Active-dendrite configuration underspecified for mouse**: [PolegPolsky2016] explicitly rules out
  dendritic spikes for DRD4 DSGCs but does not parameterise what dendritic Nav/Kv densities would
  produce if hypothetically added. Project RQ4 (active vs passive) cannot be answered for mouse from
  literature alone — it becomes an experimental task downstream of this port.
* **Sibling-model code availability is uneven**: [Hanson2019] references
  `geoffder/Spatial-Offset-DSGC-NEURON-Model` as a GitHub repo, but the other sibling papers do not
  publish code URLs in their Methods text. Phase B search effort should prioritise ModelDB listings
  and the Awatramani/Diamond/Taylor lab GitHub organisations.
* **No reproducibility data on seed stability**: none of the papers reviewed reports how DSI or peak
  firing rate vary across random-seed repetitions. Task plan's 20-seed trial count is conservative
  relative to the literature's typical 4-10 cell averages.

## Recommendations for This Task

1. **Run Phase A with 8 directions to match paper, then re-run with 12 directions for envelope
   scoring.** Report both in the answer asset. The paper uses 8 directions [PolegPolsky2016]; the
   envelope targets require 12.
2. **Do not attempt to reproduce an exact peak-firing-rate number from the paper.**
   [PolegPolsky2016] does not report one (not found in paper). Score the envelope using the
   project's 40-80 Hz target and label this clearly in the answer asset.
3. **Read simulation timestep, passive properties, and channel densities from ModelDB 189347 source
   files, not from the paper.** The PMC manuscript XML truncates Experimental Procedures; the
   canonical values live in the code.
4. **Keep dendrites passive for the Phase A baseline.** [PolegPolsky2016] explicitly states passive
   propagation is sufficient for DRD4 mouse DSGCs.
5. **In Phase B, prioritise the `geoffder/Spatial-Offset-DSGC-NEURON-Model` fork referenced by
   [Hanson2019]** over [Schachter2010] and [Ding2016] — the latter two use NeuronC, not NEURON, and
   therefore require a full rewrite rather than a port.
6. **Record the ModelDB 189347 commit/version hash** in `assets/library/dsgc-polegpolsky-2016/`
   metadata so that future morphology sweeps (S-0002-04) and E/I scans (S-0002-05) can branch from a
   pinned baseline.
7. **Log all subthreshold validation metrics** (PD NMDAR-mediated PSP = 5.8 ± 3.1 mV, ND = 3.3 ± 2.8
   mV, slope ≈ 62° for multiplicative scaling) in the answer asset as a supplementary correctness
   table, in addition to the envelope table.
8. **Treat any envelope failure after t0009 morphology swap as a scientific finding**, generate a
   suggestion for morphology-conditioned Na/K retuning, and do not retroactively adjust channel
   densities inside this task.

## Paper Index

### [PolegPolsky2016]

* **Title**: NMDA Receptors Multiplicatively Scale Visual Signals and Enhance Directional Motion
  Discrimination in Retinal Ganglion Cells
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.02.013`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `synaptic-integration`,
  `dendritic-computation`, `retinal-ganglion-cell`
* **Relevance**: The ModelDB 189347 source paper being ported. Defines the architecture (177 AMPA +
  177 NMDA + 177 GABA synapses, 282 presynaptic cells, passive dendrites, Jahr-Stevens NMDAR Mg²⁺
  block), the stimulus (1 mm/sec bar, 8 directions), and the validation targets (PSP amplitudes,
  multiplicative scaling slope ≈ 62°).

### [Schachter2010]

* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, M. J., Oesch, N., Smith, R. G., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`, `voltage-gated-channels`, `synaptic-integration`, `cable-theory`
* **Relevance**: Phase B sibling candidate — rabbit ON-OFF DSGC compartmental model with active
  dendrites. Uses NeuronC (Smith lab, not NEURON), so direct port is infeasible; included in the
  survey row as a failed candidate and as the active-dendrite reference for RQ4.

### [Koren2017]

* **Title**: Cross-compartmental Modulation of Dendritic Signals for Retinal Direction Selectivity
* **Authors**: Koren, D., Grove, J. C. R., Wei, W.
* **Year**: 2017
* **DOI**: `10.1016/j.neuron.2017.07.020`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2017.07.020/`
* **Categories**: `dendritic-computation`, `direction-selectivity`, `retinal-ganglion-cell`,
  `synaptic-integration`, `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Adds SAC-level mGluR2-gated calcium channel dynamics; relevant for Phase B as a
  richer presynaptic SAC model that could be swapped in if the Phase A reproduction requires it.
  Does not ship with a standalone NEURON DSGC model, so low porting priority.

### [Ding2016]

* **Title**: Species-specific wiring for direction selectivity in the mammalian retina
* **Authors**: Ding, H., Smith, R. G., Poleg-Polsky, A., Diamond, J. S., Briggman, K. L.
* **Year**: 2016
* **DOI**: `10.1038/nature18609`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature18609/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `compartmental-modeling`,
  `synaptic-integration`
* **Relevance**: Phase B sibling candidate using Neuron-C for a 7-SAC network model. Not a DSGC
  model itself, and Neuron-C is incompatible with this project's NEURON 8.2.7 stack — included in
  the survey as a failed port candidate. Provides SAC wiring measurements useful for later
  presynaptic-network refinement.

### [Hanson2019]

* **Title**: Retinal direction selectivity in the absence of asymmetric starburst amacrine cell
  responses
* **Authors**: Hanson, L., Sethuramanujam, S., deRosenroll, G., Jain, V., Awatramani, G. B.
* **Year**: 2019
* **DOI**: `10.7554/eLife.42392`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `compartmental-modeling`, `dendritic-computation`, `patch-clamp`
* **Relevance**: Uses a modified Poleg-Polsky NEURON DSGC model published at
  `geoffder/Spatial-Offset-DSGC-NEURON-Model`. Highest-priority Phase B port target because it is
  already a NEURON fork of the same codebase being ported in Phase A.

### [Jain2020]

* **Title**: The functional organization of excitation and inhibition in the dendrites of mouse
  direction-selective ganglion cells
* **Authors**: Jain, V., Murphy-Baum, B. L., deRosenroll, G., Sethuramanujam, S., Delsey, M.,
  Delaney, K. R., Awatramani, G. B.
* **Year**: 2020
* **DOI**: `10.7554/eLife.52949`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.52949/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`,
  `synaptic-integration`, `compartmental-modeling`, `patch-clamp`
* **Relevance**: Uses a multi-compartmental NEURON DSGC model with **177** directionally tuned
  inhibitory + untuned excitatory synapses — architecturally almost identical to [PolegPolsky2016].
  Phase B candidate; also constrains subunit size (~5-10 µm) for later E/I-ratio tasks.

### [Oesch2005]

* **Title**: Direction-Selective Dendritic Action Potentials in Rabbit Retina
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `voltage-gated-channels`,
  `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Evidence that rabbit DSGCs use dendritic spikes (somatic ~55 mV vs dendritic ~7 mV
  spikelets). Sets the baseline for contrasting active- vs passive-dendrite reproductions between
  mouse [PolegPolsky2016] and rabbit [Schachter2010].

### [Jeon2002]

* **Title**: Pattern of synaptic excitation and inhibition upon direction-selective retinal ganglion
  cells
* **Authors**: Jeon, C.-J., Kong, J.-H., Strettoi, E., Rockhill, R., Stasheff, S. F., Masland, R. H.
* **Year**: 2002
* **DOI**: `10.1002/cne.10288`
* **Asset**: (not in project corpus — referenced only through [PolegPolsky2016])
* **Categories**: `retinal-ganglion-cell`, `synaptic-integration`
* **Relevance**: Anatomical source cited by [PolegPolsky2016] for the homogeneous distribution of
  AMPA/NMDA/GABA synapses on ON dendrites — the spatial pattern that the Phase A port must preserve.

### [Park2014]

* **Title**: Excitatory Synaptic Inputs to Mouse On-Off Direction-Selective Retinal Ganglion Cells
  Lack Direction Tuning
* **Authors**: Park, S. J. H. et al.
* **Year**: 2014
* **DOI**: `10.1523/JNEUROSCI.5017-13.2014`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `patch-clamp`
* **Relevance**: Provides the experimental justification for the untuned-excitation / tuned-
  inhibition architecture used by [PolegPolsky2016] and by this port.

### [ElQuessny2021]

* **Title**: Dendrite Morphology Minimally Influences the Synaptic Distribution of Excitation and
  Inhibition in Retinal Direction-Selective Ganglion Cells
* **Authors**: El-Quessny, M., Feller, M. B.
* **Year**: 2021
* **DOI**: `10.1523/ENEURO.0261-21.2021`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_ENEURO.0261-21.2021/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `dendritic-computation`, `patch-clamp`
* **Relevance**: Evidence that morphology affects inhibitory DSI magnitude but not E/I spatial
  organisation — directly informs the expected outcome of the t0009 morphology swap in Phase A.
