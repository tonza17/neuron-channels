---
spec_version: "1"
task_id: "t0016_literature_survey_dendritic_computation"
research_stage: "papers"
papers_reviewed: 20
papers_cited: 10
categories_consulted:
  - "dendritic-computation"
  - "direction-selectivity"
  - "compartmental-modeling"
  - "retinal-ganglion-cell"
  - "synaptic-integration"
  - "voltage-gated-channels"
  - "cable-theory"
  - "patch-clamp"
date_completed: "2026-04-19"
status: "complete"
---
## Task Objective

Survey the existing corpus to identify which aspects of dendritic computation are already covered
and where gaps remain. The downstream literature search must target ~25 **new** papers on dendritic
nonlinearities (NMDA spikes, Na+/Ca2+ dendritic spikes, plateau potentials, branch-level
integration, sublinear-to-supralinear transitions, active vs passive modelling) that can inform DSGC
direction-selectivity modelling, without duplicating DOIs already downloaded by
`t0002_literature_survey_dsgc_compartmental_models`.

## Category Selection Rationale

Consulted `dendritic-computation` as the central category for this task and `direction-selectivity`
because the goal is to translate generic dendritic motifs into DSGC-specific predictions. Consulted
`compartmental-modeling` and `cable-theory` because the task explicitly contrasts active and passive
dendritic models. Consulted `synaptic-integration` for the sublinear/linear/supralinear summation
axis and `voltage-gated-channels` because the mechanisms of interest are Na+/Ca2+/NMDA conductances.
Consulted `retinal-ganglion-cell` and `patch-clamp` to ground the findings in DSGC empirical data.

Excluded purely circuit-level or molecular categories because this task is not about wiring or
receptor pharmacology; it focuses on biophysical integration inside the postsynaptic dendritic tree.
Excluded `calcium-imaging` as a standalone category because it is methodological rather than
conceptual.

## Key Findings

### Dendritic spikes drive DSGC output, not somatic integration

Direct in vitro recordings in rabbit DSGCs show a six-fold sharpening of directional tuning between
the soma's subthreshold EPSP (DSI ~0.09-0.14) and the spike output (DSI ~0.67-0.74), with
light-evoked somatic spikes failing to be reproduced by matched-amplitude somatic current injection
[Oesch2005]. Local TTX puffing onto dendrites reduced light-evoked spiking by **41.5 +/- 15%** while
sparing depolarization-evoked spikes, and two-photon Ca2+ imaging revealed direction-tuned,
TTX-sensitive dendritic Ca2+ transients [Oesch2005]. A realistic compartmental model reproduced this
sharpening only when dendritic Na+ spikes were inserted and multiple independent spike initiation
zones (one per dendritic subtree) were allowed [Schachter2010]. The electrotonic partitioning of the
DSGC arbor into near-independent dendritic sectors is therefore a load-bearing assumption for any
biophysical DSGC model.

**Best practice**: Insert active TTX-sensitive Na+ channels along dendrites at densities sufficient
to support ~7 mV orthograde spikelets while keeping the somatic threshold at approximately -49 mV so
that only dendrite-initiated events cross threshold [Oesch2005, Schachter2010].

**Hypothesis**: The number of electrotonically independent initiation zones in DSGCs scales with the
number of dendritic primary branches; reducing primary branches in silico should proportionally
compress the spike DSI while leaving PSP DSI unchanged.

### NMDA-mediated multiplicative gain sharpens motion discrimination

In mouse DSGCs, NMDAR conductances multiplicatively scale visual inputs rather than summing linearly
with AMPA drive, which improves motion discrimination in noisy conditions without narrowing
directional tuning [PolegPolsky2016]. Pharmacologically blocking NMDARs reduces the gain of the
direction-tuning curve but leaves the preferred direction intact, demonstrating that NMDA spikes act
as a nonlinear amplifier rather than a tuning mechanism [PolegPolsky2016]. Cortical evidence from
pyramidal neurons reinforces this: two-photon uncaging-evoked sequential activation along a single
basal dendrite shows that **NMDA-receptor-mediated nonlinearities combined with impedance
gradients** produce sequence-selective somatic spikes, with centripetal (tip-to-soma) sequences
producing **~30% larger EPSPs** than centrifugal sequences and driving **2-3x more somatic APs**
[Branco2010]. These results generalise across cell types and provide the canonical mechanism by
which DSGC NMDA spikes could multiply excitatory drive preferentially in the preferred direction.

**Best practice**: Represent NMDAR as a Mg2+-blocked conductance with voltage-dependent unblock, not
as a pure AMPA-like linear input. The Jahr-Stevens formulation used in [PolegPolsky2016] is a
documented default.

### Dendritic compartmentalisation is finer than the whole cell

In mouse DSGCs, inhibition shapes direction selectivity independently within dendritic segments
**smaller than 10 um**, implying that the parallel processing of direction can be more fine-grained
than previously thought [Jain2020]. In starburst amacrine cells, mGluR2 signalling on voltage-gated
calcium channels selectively restricts cross-sector propagation, preserving sector-by-sector
direction tuning even when neighbouring sectors are being driven [Koren2017]. In DSGCs with both
symmetric and asymmetric dendrites, excitation and inhibition are locally correlated in strength
despite differing global morphologies [ElQuessny2021]. Temporal asymmetries between excitation and
inhibition also generate direction selectivity even when upstream starburst dendrites are made
non-directional [Hanson2019]. Together these results show that branch- or sector-level computation,
not whole-cell integration, is the relevant scale for DSGC models.

**Hypothesis**: A DSGC compartmental model restricted to whole-arbor integration (i.e., collapsed
dendrites into one compartment per arbor) will overestimate preferred-direction spiking and
underestimate null-direction suppression by at least the factor reported in [Oesch2005] (roughly
6x).

### Quantitative targets for a biophysical DSGC model

Across the reviewed DSGC papers, the model must simultaneously match:

* Somatic resting potential **~-70 mV**, input resistance **~80 Mohm**, f-I slope **~0.31 Hz/pA**
  [Oesch2005]
* Light-evoked PSP peak **~-59 mV** (12 mV depolarisation), somatic spike threshold **~-49 mV**,
  modal firing rate **~148 Hz** [Oesch2005]
* Dendritic spikelet amplitude **~7 mV** at the soma and near-unity dendritic-to-somatic spike
  propagation [Oesch2005]
* Spike DSI **~0.6-0.7** versus PSP DSI **~0.1** [Oesch2005, Schachter2010]
* NMDA-mediated multiplicative scaling that preserves the preferred-direction angle while increasing
  motion-discrimination accuracy [PolegPolsky2016]
* Direction-tuned inhibition acting at sub-10 um dendritic scales [Jain2020]

No single reviewed paper provides all six targets in one dataset; a DSGC modelling task must
triangulate them.

## Methodology Insights

* **Active dendrite requirement**: Any DSGC compartmental model must include TTX-sensitive Na+
  channels along the dendritic arbor with multiple independent initiation zones. Passive dendrites
  cannot reproduce the ~6x spike-vs-PSP DSI gap observed experimentally [Oesch2005, Schachter2010].

* **Electrotonic partitioning**: Represent each major dendritic subtree as an effectively
  electrically isolated local integrator. [Schachter2010] demonstrates that the separation between
  initiation zones tracks the dendritic branching geometry; lumping branches collapses this
  mechanism.

* **NMDA conductance model**: Use a voltage-dependent (Mg2+-unblock) NMDA conductance, not a linear
  AMPA-only drive. [PolegPolsky2016] provides the functional signature (multiplicative gain without
  tuning-angle shift) and [Branco2010] provides the canonical biophysics (impedance gradient + NMDA
  nonlinearity) to validate against.

* **On-the-path inhibition**: Place GABAergic inhibitory synapses on the dendritic path between
  bipolar excitation and the soma rather than lumping inhibition globally, because dendritic spike
  failure depends on the geometry of this layout [Oesch2005, Schachter2010].

* **Fine-grained inhibition**: Model direction-tuned inhibition at sub-10 um dendritic scales,
  because whole-dendrite inhibition produces weaker DSI sharpening than the empirically observed
  segment-level pattern [Jain2020, ElQuessny2021].

* **Calibration targets**: Use the quantitative anchors listed in Key Findings as simultaneous
  constraints. Rejecting models that miss any single anchor by >20% is a more disciplined validation
  strategy than single-metric fitting.

* **Temperature matters**: DSGC channel kinetics and morphology-dependent spike thresholds vary with
  temperature; published recordings at 34-36 C should be used as the calibration baseline
  [Oesch2005].

**Hypothesis to test during execution**: A minimal DSGC model with (1) passive soma+axon, (2)
dendritic Hodgkin-Huxley Na+ channels, (3) NMDA synapses, and (4) on-the-path GABA synapses should
reproduce the Oesch2005 spike-vs-PSP DSI split within 15%. If not, additional mechanisms (Ca2+
spikes, SK/BK channels, plateau potentials) are required.

## Gaps and Limitations

* The existing corpus contains **strong DSGC-specific evidence for dendritic Na+ spikes** but
  **limited cross-cell-type coverage of NMDA spike biophysics**. Only [Branco2010] probes NMDA
  spikes in detail and it does so in cortical pyramidal neurons, not DSGCs.

* **Plateau potentials** (slow, Ca2+-mediated, long-lasting depolarisations) are not covered at all.
  No paper in the corpus quantifies plateau amplitude, duration, or Ca2+ channel composition in DSGC
  or functionally analogous neurons.

* **Sublinear-to-supralinear integration transitions** - the axis along which passive cable
  summation gives way to active amplification - is not surveyed quantitatively. [Schachter2010]
  addresses the supralinear end; no paper maps the crossover.

* **Branch-level morphology effects** beyond DSGCs (e.g., cortical basal vs apical dendrites, CA1
  pyramidal, cerebellar Purkinje) are almost absent; the corpus draws only from retina-plus-one
  cortical example.

* **Quantitative Na+/Ca2+ channel densities** in DSGC dendrites are not tabulated. [Oesch2005]
  infers their presence from TTX sensitivity but does not quantify densities in the way a modeller
  needs.

* **Active versus passive modelling trade-off** studies are missing: no paper systematically ablates
  dendritic conductances in a DSGC model and measures the resulting deviation from experimental
  tuning curves.

* **Cable-theoretic foundations** (Rall, Koch-type theory, impedance matching) are largely implicit;
  only [Branco2010] touches on impedance gradients explicitly.

## Recommendations for This Task

1. Target the internet search at **NMDA dendritic spike biophysics** papers - canonical Schiller,
   Major, Polsky, and Magee/Larkum studies - because [Branco2010] is the only corpus exemplar and
   the DSGC NMDA evidence from [PolegPolsky2016] demands cross-validation.

2. Target **plateau potential** papers covering CA1, cortical L5, and DSGC-adjacent retinal circuits
   (e.g., ipRGC, starburst amacrine), because the corpus has zero coverage.

3. Target classic **Na+/Ca2+ dendritic spike** papers (Stuart and Sakmann, Larkum and Zhu, Helmchen
   et al.) to anchor the channel-density assumptions [Oesch2005] leaves implicit.

4. Target **sublinear-to-supralinear integration** papers (Cash and Yuste, Longordo et al.,
   Tran-Van-Minh et al.) to map where passive-cable predictions break down.

5. Target **branch-level integration** papers (Polsky et al., Losonczy and Magee) that quantify how
   nonlinearities depend on branch identity, because DSGC arbors have stereotyped branch
   hierarchies.

6. Target **active vs passive modelling** reviews and methodological papers (London and Hausser
   review, Poirazi et al., Jadi et al.) to build a defensible modelling decision tree.

7. Prioritise open-access venues (eLife, PLoS CB, bioRxiv) to minimise paywalled-paper failure rate;
   mark Nature/Neuron/Science candidates as fallbacks with explicit paywalled handling per task
   spec.

8. When extracting quantitative targets from new papers, record channel densities, time constants,
   and spatial scales in a dedicated table so the downstream answer asset can synthesise them
   alongside the corpus-derived Oesch2005 quantities above.

## Paper Index

### [Oesch2005]

* **Title**: Direction-Selective Dendritic Action Potentials in Rabbit Retina
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `retinal-ganglion-cell`,
  `patch-clamp`
* **Relevance**: Provides the DSGC-specific quantitative anchors (DSI ~0.7 spike vs ~0.1 PSP,
  spikelet ~7 mV, threshold ~-49 mV) that any dendritic-computation model for DSGCs must reproduce.

### [Schachter2010]

* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, M. J., Oesch, N., Smith, R. G., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `compartmental-modeling`
* **Relevance**: Only existing compartmental model demonstrating that electrotonic partitioning plus
  local dendritic Na+ spikes reproduces the Oesch2005 DSI gap; sets the reference architecture
  against which new dendritic mechanisms (NMDA, Ca2+, plateau) must be compared.

### [PolegPolsky2016]

* **Title**: NMDA Receptors Multiplicatively Scale Visual Signals and Enhance Directional Motion
  Discrimination in Retinal Ganglion Cells
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.02.013`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/`
* **Categories**: `dendritic-computation`, `direction-selectivity`, `synaptic-integration`
* **Relevance**: Shows the DSGC-specific functional signature of NMDA spikes (multiplicative gain
  without tuning shift) that the new literature search must validate against cortical NMDA-spike
  biophysics.

### [Branco2010]

* **Title**: Dendritic Discrimination of Temporal Input Sequences in Cortical Neurons
* **Authors**: Branco, T., Clark, B. A., Hausser, M.
* **Year**: 2010
* **DOI**: `10.1126/science.1189664`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1126_science.1189664/`
* **Categories**: `dendritic-computation`, `synaptic-integration`, `voltage-gated-channels`
* **Relevance**: Canonical demonstration that NMDA nonlinearity plus dendritic impedance gradients
  produce sequence-selective computation; supplies the mechanism candidate that the new literature
  search must extend to branch-level DSGC integration.

### [Koren2017]

* **Title**: Cross-compartmental Modulation of Dendritic Signals for Retinal Direction Selectivity
* **Authors**: Koren, D., Grove, J. C. R., Wei, W.
* **Year**: 2017
* **DOI**: `10.1016/j.neuron.2017.07.020`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2017.07.020/`
* **Categories**: `dendritic-computation`, `direction-selectivity`, `synaptic-integration`
* **Relevance**: Demonstrates mGluR2-mediated compartmentalisation in starburst amacrine cells and
  its downstream effect on DSGC direction selectivity, reinforcing that dendritic sector isolation
  is an active regulatory mechanism.

### [Jain2020]

* **Title**: The functional organization of excitation and inhibition in the dendrites of mouse
  direction-selective ganglion cells
* **Authors**: Jain, V., Murphy-Baum, B. L., deRosenroll, G., et al.
* **Year**: 2020
* **DOI**: `10.7554/eLife.52949`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.52949/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `synaptic-integration`
* **Relevance**: Shows DSGC inhibition shapes direction selectivity at sub-10 um dendritic scales,
  directly constraining the granularity a new DSGC compartmental model must adopt.

### [Hanson2019]

* **Title**: Retinal direction selectivity in the absence of asymmetric starburst amacrine cell
  responses
* **Authors**: Hanson, L., Sethuramanujam, S., deRosenroll, G., Jain, V., Awatramani, G. B.
* **Year**: 2019
* **DOI**: `10.7554/eLife.42392`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/`
* **Categories**: `direction-selectivity`, `dendritic-computation`
* **Relevance**: Reveals a parallel postsynaptic mechanism for DSGC direction selectivity based on
  E/I temporal asymmetries, indicating that dendritic integration alone can carry direction
  information in the absence of asymmetric upstream tuning.

### [ElQuessny2021]

* **Title**: Dendrite Morphology Minimally Influences the Synaptic Distribution of Excitation and
  Inhibition in Retinal Direction-Selective Ganglion Cells
* **Authors**: El-Quessny, M., Feller, M. B.
* **Year**: 2021
* **DOI**: `10.1523/ENEURO.0261-21.2021`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_ENEURO.0261-21.2021/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `retinal-ganglion-cell`
* **Relevance**: Shows symmetric and asymmetric DSGCs share locally correlated E/I synapse strength
  even though global dendrite morphology differs, a useful null to test in branch-level integration
  models.

### [Vaney2012]

* **Title**: Direction selectivity in the retina: symmetry and asymmetry in structure and function
* **Authors**: Vaney, D. I., Sivyer, B., Taylor, W. R.
* **Year**: 2012
* **DOI**: `10.1038/nrn3165`
* **Asset**: `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `retinal-ganglion-cell`
* **Relevance**: Synthesises the circuit and dendritic perspectives on retinal direction selectivity
  and frames the open questions about postsynaptic dendritic computation this task must fill.

### [Carnevale1997]

* **Title**: The NEURON Simulation Environment
* **Authors**: Hines, M. L., Carnevale, N. T.
* **Year**: 1997
* **DOI**: `10.1162/neco.1997.9.6.1179`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/`
* **Categories**: `compartmental-modeling`, `cable-theory`
* **Relevance**: Defines the NEURON simulator used in this project; essential context when
  translating dendritic biophysics from the literature into executable models.
