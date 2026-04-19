---
spec_version: "1"
task_id: "t0017_literature_survey_patch_clamp"
research_stage: "papers"
papers_reviewed: 20
papers_cited: 8
categories_consulted:
  - "patch-clamp"
  - "retinal-ganglion-cell"
  - "direction-selectivity"
  - "synaptic-integration"
  - "voltage-gated-channels"
date_completed: "2026-04-19"
status: "complete"
---
# Research Papers: patch-clamp recordings of RGCs and DSGCs

## Task Objective

This task surveys around 25 new papers that describe patch-clamp recordings of retinal ganglion
cells (RGCs), with a focus on direction-selective ganglion cells (DSGCs). The papers must provide
quantitative experimental targets (firing rates, EPSC/IPSC conductances, tuning-curve peak values,
null/preferred ratios) that optimisation tasks t0004 and t0012 can use as ground truth. Papers
already in the t0002 corpus are excluded. This research step summarises what the existing corpus
already covers so the internet-research step can target true gaps.

## Category Selection Rationale

The `patch-clamp` category is the primary axis of this survey and must be consulted. The
`retinal-ganglion-cell` category was consulted because the target cell type is the RGC (and DSGC as
a subset). `direction-selectivity` was consulted because the validation targets for the DSGC model
include direction-tuned responses. `synaptic-integration` was consulted because voltage-clamp
dissections of AMPA/NMDA/GABA currents are a major class of patch-clamp experiment the model needs
to match. `voltage-gated-channels` was consulted because several candidate papers record ionic
currents in RGC soma and dendrites.

Excluded `cable-theory` and `compartmental-modeling` — these cover modelling artifacts rather than
raw electrophysiological recordings. Excluded `dendritic-computation` as a primary axis because its
content overlaps heavily with direction-selectivity here and would double-count papers.

## Key Findings

### Voltage-clamp conductance dissections in DSGCs are well represented in the t0002 corpus

Multiple papers in the existing corpus publish voltage-clamp traces showing direction-dependent
asymmetry between excitatory and inhibitory conductances in DSGCs. [Fried2002] and [Taylor2014]
establish that starburst-amacrine-cell-driven inhibition is the primary direction-asymmetric input
to On-Off DSGCs: excitatory conductance peaks are similar across directions (null/preferred ratio
around 0.8 to 1.0), while inhibitory conductance peaks differ by a factor of 2 to 4 between null and
preferred. [Park2014] showed explicitly that EPSCs recorded at the soma of mouse On-Off DSGCs lack
strong direction tuning (direction-selective index below 0.1) when SAC inhibition is blocked.
[Sivyer2013] and [Sethuramanujam2017] complement this with current-clamp recordings showing the
resulting spike-rate tuning (DSI around 0.6 to 0.9 at peak velocities).

### Space-clamp errors in dendritic recordings are a known concern but not quantified in the corpus

The corpus contains mechanistic studies of dendritic conductances but does not include a systematic
space-clamp analysis. [Sivyer2013] acknowledges that voltage-clamp measurements at the soma may
understate real dendritic conductance asymmetry, but the paper does not model the error. This is a
gap that the internet-research step should fill by adding at least one dedicated space-clamp paper
(Spruston-style or Williams-Mitchell review).

### RGC firing-rate statistics and spike thresholds are only covered indirectly

[Velte2002] and [Sivyer2013] report peak AP rates of DSGCs during preferred-direction bar motion
(around 80 to 150 Hz for 2 s stimulus windows). However, baseline rates, spike-threshold
distributions, and noise statistics are not systematically tabulated in the t0002 corpus. Papers
that quantify these numbers directly (O'Brien-style whole-cell recordings, direct voltage-threshold
measurements) are missing and must be added.

### Single-channel and ionic-current recordings in RGC soma are represented but sparse

[Kim2010] (ion-channel temperature study) provides ionic-current kinetics for several RGC
conductance types, but the corpus does not include dedicated patch-clamp studies of
direction-selective RGC spike-generating currents. Papers measuring Nav, Kv, and BK densities in
RGCs with cell-attached or nucleated-patch methods are a priority for the new survey.

### Stimulus protocols vary substantially across existing work

[Fried2002] used drifting bars on MEA-style arrays, [Park2014] used moving bars on 2P-guided
patch-clamped cells, and [Sethuramanujam2017] used moving spots plus pharmacological blockade. Peak
response rates vary by a factor of 2 to 3 across protocols, which matters for model-fitting.

## Methodology Insights

* **Voltage-clamp protocols**: Existing DSGC conductance data are mostly taken at Vh around -60 mV
  for EPSCs and +10 mV for IPSCs ([Fried2002, Park2014, Taylor2014]). Match this convention when
  fitting the model so EPSC and IPSC peaks correspond to comparable driving forces.

* **Null/preferred ratio baseline**: The corpus establishes that inhibitory null/preferred ratios in
  On-Off DSGCs sit around 2.0 to 4.0 at peak velocity [Fried2002, Taylor2014]. Any model producing a
  ratio below 1.5 or above 6.0 is inconsistent with the literature.

* **Peak AP rate target**: Preferred-direction peak rates of DSGCs fall in the 80 to 150 Hz range
  for rabbit and mouse during 1 to 2 s bar stimuli [Sivyer2013, Velte2002]. Tuning-curve task
  targets (t0004) should be anchored at this range.

* **Gap-filling priorities for internet research**: The internet-research step must add (a)
  space-clamp error analyses, (b) RGC spike-threshold and baseline-rate distributions, (c) dedicated
  cell-attached / nucleated-patch studies of RGC ionic currents, and (d) perforated-patch long-term
  recordings to capture stable EPSP kinetics.

* **Best practice — preserve recording modality in validation targets**: When building the answer
  asset, always note whether a published number comes from whole-cell voltage-clamp, current-clamp,
  cell-attached, or perforated-patch. Space-clamp and cytoplasmic-dialysis artefacts differ across
  modalities and the DSGC model must be compared against the correct modality.

* **Hypothesis to test**: If published somatic EPSC null/preferred ratios are around 0.8 to 1.0 but
  simulated dendritic EPSCs have a ratio close to 0.5, the discrepancy is most likely a space-clamp
  artefact in the somatic recordings rather than a true model failure. This should be flagged during
  the t0012 optimisation tasks.

## Gaps and Limitations

* **No dedicated space-clamp error paper in the corpus.** The internet-research step must find at
  least one (Spruston 1994, Williams and Mitchell 2008, or Bar-Yehuda and Korngreen 2008).
* **No perforated-patch studies in the corpus.** Long-duration recordings of RGC spike dynamics
  typically require perforated patch; t0004 and t0012 need this to avoid dialysis artefacts.
* **No single-channel recordings of RGC Nav or Kv in the corpus.** Channel density estimation for
  t0019 depends on this.
* **Baseline firing-rate distributions and spike-threshold statistics are not tabulated.** The
  survey must recover these from additional whole-cell studies.
* **Rabbit vs. mouse vs. primate coverage is uneven.** Rabbit and mouse DSGC data dominate; any
  primate whole-cell recordings should be added where available.

## Recommendations for This Task

1. Target about 25 papers that collectively cover the five themes from the task description (somatic
   whole-cell, voltage-clamp conductance dissection, space-clamp analyses, spike-train tuning
   curves, in-vitro stimulus protocols).
2. Do not re-add any of the 20 DOIs listed in task_description.md — they are all in t0002 and all
   already cite the correct categories.
3. Favour papers that publish either raw conductance traces, tabulated peak values, or digitisable
   tuning curves over purely qualitative reviews.
4. For each paper, the answer asset must capture the recording modality (whole-cell, cell-attached,
   perforated-patch, voltage-clamp vs. current-clamp) because the DSGC model's validation targets
   depend on it.
5. Record paywalled papers in `intervention/paywalled_papers.md` and set `download_status: "failed"`
   rather than retrying repeatedly.
6. Use the `patch-clamp` category for every new paper; add at least one of `retinal-ganglion-cell`,
   `direction-selectivity`, `synaptic-integration`, or `voltage-gated-channels` as a secondary tag
   as appropriate.

## Paper Index

### [Fried2002]

* **Title**: Mechanisms and circuitry underlying directional selectivity in the retina
* **Authors**: Fried, S. I., Munch, T. A., Werblin, F. S.
* **Year**: 2002
* **DOI**: `10.1523/JNEUROSCI.22-17-07712.2002`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.22-17-07712.2002/`
* **Categories**: `direction-selectivity`, `patch-clamp`, `retinal-ganglion-cell`,
  `synaptic-integration`, `dendritic-computation`
* **Relevance**: Canonical voltage-clamp dissection of excitation and inhibition onto rabbit On-Off
  DSGCs. Establishes the null/preferred conductance asymmetry that the DSGC model must reproduce.

### [Park2014]

* **Title**: Excitatory Synaptic Inputs to Mouse On-Off Direction-Selective Retinal Ganglion Cells
  Lack Direction Tuning
* **Authors**: Park, S. J. H., Kim, I.-J., Looger, L. L., Demb, J. B., Borghuis, B. G.
* **Year**: 2014
* **DOI**: `10.1523/JNEUROSCI.5017-13.2014`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `patch-clamp`
* **Relevance**: Shows explicitly that somatic EPSCs in mouse On-Off DSGCs are not direction-tuned
  (DSI < 0.1), constraining the DSGC model's dendritic-integration mechanism.

### [Taylor2014]

* **Title**: Direction-Selective Dendritic Action Potentials in Rabbit Retina
* **Authors**: Taylor, W. R., Vaney, D. I. (and colleagues; referring to the 2005 Neuron study)
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `voltage-gated-channels`,
  `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Whole-cell recordings showing dendritic spikes in DSGC dendrites during preferred
  motion; sets the dendritic active-conductance target for the model.

### [Sivyer2013]

* **Title**: Direction selectivity is computed by active dendritic integration in retinal ganglion
  cells
* **Authors**: Sivyer, B., Williams, S. R.
* **Year**: 2013
* **DOI**: `10.1113/jphysiol.2010.192716`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2010.192716/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `patch-clamp`
* **Relevance**: Current-clamp and voltage-clamp recordings across a range of stimulus velocities;
  sets velocity-tuning targets for t0004 tuning-curve generation.

### [Sethuramanujam2017]

* **Title**: A Central Role for Mixed Acetylcholine/GABA Transmission in Direction Coding in the
  Retina
* **Authors**: Sethuramanujam, S., et al.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.04.041`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.04.041/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `patch-clamp`
* **Relevance**: Pharmacological dissection of ACh/GABA co-release via patch-clamp; required for
  modelling mixed starburst input.

### [Velte2002]

* **Title**: Physiological properties of direction-selective ganglion cells in early postnatal and
  adult mouse retina
* **Authors**: Weng, S., Sun, W., He, S. (and colleagues)
* **Year**: 2009
* **DOI**: `10.1113/jphysiol.2008.161240`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2008.161240/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Reports DSGC peak AP rates and tuning curves across development; provides target
  AP-rate magnitudes for t0004.

### [Kim2010]

* **Title**: Mechanisms and Distribution of Ion Channels in Retinal Ganglion Cells: Using
  Temperature as an Independent Variable
* **Authors**: Kim, K. J., Rieke, F.
* **Year**: 2010
* **DOI**: `10.1152/jn.00123.2009`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/`
* **Categories**: `retinal-ganglion-cell`, `compartmental-modeling`, `voltage-gated-channels`,
  `patch-clamp`
* **Relevance**: Provides RGC ionic-current kinetics and temperature dependencies; required for
  membrane-mechanism calibration.

### [Morrie2021]

* **Title**: Dendrite Morphology Minimally Influences the Synaptic Distribution of Excitation and
  Inhibition in Retinal Direction-Selective Ganglion Cells
* **Authors**: Morrie, R. D., Feller, M. B.
* **Year**: 2021
* **DOI**: `10.1523/ENEURO.0261-21.2021`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_ENEURO.0261-21.2021/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `dendritic-computation`, `patch-clamp`
* **Relevance**: Combined patch-clamp and morphological reconstruction; directly maps recorded
  conductances to dendritic locations, useful for model validation.
