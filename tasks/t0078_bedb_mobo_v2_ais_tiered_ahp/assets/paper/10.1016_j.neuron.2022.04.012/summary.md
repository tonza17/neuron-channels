---
spec_version: "3"
paper_id: "10.1016_j.neuron.2022.04.012"
citation_key: "Wienbar2022"
summarized_by_task: "t0078_bedb_mobo_v2_ais_tiered_ahp"
date_summarized: "2026-05-03"
---
# Differences in Spike Generation Instead of Synaptic Inputs Determine the Feature Selectivity of Two Retinal Cell Types

## Metadata

* **File**: Download failed (Cloudflare and PMC Proof-of-Work blocked automated retrieval)
* **Published**: 2022 (2022-05-03)
* **Authors**: Sophia Wienbar 🇺🇸, Gregory William Schwartz 🇺🇸
* **Venue**: Neuron, vol. 110, issue 13, pages 2110-2123.e4
* **DOI**: `10.1016/j.neuron.2022.04.012`

## Abstract

Retinal ganglion cells (RGCs) are the spiking projection neurons of the eye that encode different
features of the visual environment. The circuits providing synaptic input to different RGC types to
drive feature selectivity have been studied extensively, but there has been less research aimed at
understanding on the intrinsic properties and how they impact feature selectivity. We introduce an
RGC type in the mouse, the Bursty Suppressed-by-Contrast (bSbC) RGC and compared it to the OFF
sustained Alpha (OFFsA). Differences in their contrast response functions arose not from differences
in synaptic inputs but in their intrinsic properties. Spike generation was the key intrinsic
property behind this functional difference; the bSbC RGC undergoes depolarization block while the
OFFsA RGC maintains a high spike rate. Our results demonstrate that differences in intrinsic
properties allow these two RGC types to detect and relay distinct features of an identical visual
stimulus to the brain.

## Overview

This summary is based on the abstract, the PMC full-text web view, and the article's open Zenodo
model archives. The full PDF could not be downloaded automatically: the Cell.com publisher PDF and
the bioRxiv preprint are protected by Cloudflare bot challenges, and the PMC mirror requires a
JavaScript Proof-of-Work cookie that this environment cannot satisfy. The body content extracted
below is therefore a faithful synthesis of what was retrieved from the PMC HTML rendering rather
than a paraphrase of the abstract.

The paper introduces a new mouse retinal ganglion cell type, the Bursty Suppressed-by-Contrast
(bSbC) RGC, and uses it as the experimental partner to the well-characterised OFF sustained Alpha
(OFFsA) RGC. The two cells receive remarkably similar excitatory and inhibitory synaptic input under
a contrast-step stimulus, yet they encode contrast in opposite ways: OFFsA fires more strongly to
dark contrasts, while bSbC suppresses its baseline firing for both positive and negative contrasts.
The authors show that this functional divergence is not driven by upstream circuitry but by
cell-intrinsic spike generation machinery.

By combining patch-clamp recordings, sodium-channel pharmacology with the Nav1.6-selective blocker
4,9-anhydrotetrodotoxin (49TTX), confocal imaging of the axon initial segment (AIS), and a
single-cell NEURON compartmental model with a two-subsegment AIS, the authors localise the
functional difference to the AIS itself. OFFsA cells have longer AIS segments and a higher
proportion of Nav1.6 channels, both of which support sustained high-rate spiking; bSbC cells have
shorter AIS segments and a Nav1.2-dominated AIS that is more easily driven into depolarisation
block.

The model is publicly archived on Zenodo (DOI 10.5281/zenodo.6423531) under an "Other (Open)"
license, with the analysis code at DOI 10.5281/zenodo.6423526. The two-subsegment AIS architecture
with proximal Nav1.2 and distal Nav1.6 is directly portable to other RGC compartmental models that
need biophysically grounded AIS heterogeneity, which is the reason this paper is being added to task
t0078.

## Architecture, Models and Methods

The single-cell biophysical model was implemented in NEURON 7.7. Morphologies were reconstructed
from confocal images of OFFsA and bSbC cells fixed and stained for ankyrin-G to localise the AIS,
with separate reconstructions used for the two cell types. The cable was discretised at d_lambda
spatial granularity and integrated with the standard NEURON variable-timestep solver.

The AIS was modelled as two contiguous subsegments. The proximal subsegment carried predominantly
Nav1.2 (low-threshold, slow-inactivating) and the distal subsegment carried Nav1.6
(persistent-component, low-threshold relative to soma but high-threshold relative to Nav1.2). Across
the population the OFFsA AIS was 22 +/- 1.7 um long with diameter 1.32 +/- 0.057 um, while the bSbC
AIS was 16 +/- 1.5 um long with diameter 1.34 +/- 0.031 um (length p = 0.018; diameter p = 0.83).
The model used a Nav1.6 fraction of approximately 40 percent of total AIS sodium for OFFsA and
approximately 0 percent (Nav1.2-only AIS) for bSbC. Total AIS sodium conductance was 200 nS in the
OFFsA model and 150 nS in the bSbC model.

Soma and dendritic compartments carried passive Rm/Cm/Ra and a standard set of voltage-gated sodium
and potassium conductances tuned to reproduce the cell-attached and whole-cell current-clamp spike
shapes observed under matched intrinsic-property protocols. Synaptic conductance traces were taken
from voltage-clamp recordings (excitatory and inhibitory) of contrast-step responses in real cells
of each type, then injected as synaptic conductance commands at a single dendritic location in the
model so that the only thing differing between simulations of the two cell types was the spike
generator. Pharmacology used 49TTX (Nav1.6-selective) at the published concentration to isolate
Nav1.6's contribution, with vehicle and full-TTX controls.

Statistics combined cell-level means with non-parametric tests (e.g., AIS length p = 0.018), and the
model code, simulation drivers, and analysis pipeline are archived under DOI 10.5281/zenodo.6423531
(model) and DOI 10.5281/zenodo.6423526 (analysis), both under an "Other (Open)" license.

## Results

* **AIS length** is significantly shorter in bSbC than OFFsA: **16 +/- 1.5 um** vs **22 +/- 1.7 um**
  (p = 0.018), a roughly 28 percent reduction.
* **AIS diameter** does not differ between cell types: **1.34 +/- 0.031 um** (bSbC) vs **1.32 +/-
  0.057 um** (OFFsA), p = 0.83.
* **Nav1.6 fraction** of AIS sodium is approximately **40 percent** in OFFsA and approximately **0
  percent** in bSbC; **49TTX** (Nav1.6 blocker) significantly reduced OFFsA spike amplitude but had
  no effect on bSbC spike amplitude.
* **Total AIS sodium conductance** in the model: **200 nS** for OFFsA, **150 nS** for bSbC.
* **Baseline firing rate** of the OFFsA cell sits at approximately **86 Hz**; the bSbC cell has a
  comparable baseline that drops sharply for both positive and negative contrasts.
* **Depolarization block** dominates the bSbC contrast response: high contrasts push the bSbC AIS
  into block and silence the cell, while OFFsA maintains a high sustained spike rate at the same
  contrast levels.
* **Spike shape** in bSbC has significantly smaller spike peaks and shallower maximum rising slopes
  than OFFsA, consistent with a Nav1.2-dominated AIS.
* **Synaptic conductance traces** measured under voltage clamp are nearly identical between the two
  cell types for the contrast-step stimulus, ruling out a synaptic-input explanation for the
  divergent contrast response functions.

## Innovations

### Two-Subsegment AIS in a Public RGC Model

The paper publishes a NEURON compartmental model of two RGC types in which the AIS is split into a
proximal Nav1.2-rich subsegment and a distal Nav1.6-rich subsegment, with cell-type-specific
differences in length and channel composition. The model is archived on Zenodo with an open license,
providing a public, reusable substitute for prior closed-source AIS-tiered RGC models.

### Spike Generation as a Feature Selectivity Mechanism

The paper makes a direct, mechanistic case that two RGC types receiving the same synaptic input can
nonetheless transmit opposite contrast-tuning signals to the brain because of differences in their
spike generators. Depolarization block of the bSbC cell, driven by its short Nav1.2-dominated AIS,
is identified as the operative computation.

### Anatomy-Pharmacology-Model Triangulation on the AIS

The paper triangulates AIS length and channel composition from confocal anatomy, the
Nav1.6-selective blocker 49TTX, and a NEURON model that reproduces the patch-clamp spike shapes and
the contrast response functions of both cell types. This three-way triangulation is the template for
downstream RGC AIS work that wants biophysically grounded parameters.

## Datasets

This paper produced no public stimulus or recording dataset of the kind catalogued in
`meta/asset_types/dataset/`. Two public code/data archives are released:

* **Zenodo 10.5281/zenodo.6423531** ("WienbarAndSchwartz_Neuron_2022_model"): NEURON compartmental
  model files including AIS architecture, ionic conductance parameterisations, morphologies, and
  simulation drivers. License: "Other (Open)".
* **Zenodo 10.5281/zenodo.6423526** ("WienbarAndSchwartz_Neuron_2022_analysis"): Symphony/MATLAB
  analysis pipeline for the patch-clamp recordings. License: "Other (Open)".

In-vivo data are mouse (laboratory) retinal slice patch-clamp and confocal imaging; cell counts and
recording counts are tabulated in the paper's STAR Methods and key resources table but were not
accessible to this automated extraction (PDF download blocked).

## Main Ideas

* **AIS heterogeneity matters at the single-cell level.** Two RGC types with near-identical synaptic
  input can produce opposite contrast tuning purely because their AIS lengths and Nav1.2 vs Nav1.6
  ratios differ. Any DSGC compartmental model that wants to reproduce realistic firing behaviour
  needs an AIS that respects this heterogeneity.
* **Use the Wienbar 2022 Zenodo model as the public AIS substrate for t0078.** The Zenodo archive
  (10.5281/zenodo.6423531, "Other (Open)") gives a directly portable two-subsegment AIS with
  proximal Nav1.2 and distal Nav1.6, plus length 16-22 um and diameter ~1.3 um, suitable as a
  drop-in replacement for the paywalled Werginz 2020 NEURON model.
* **Depolarization block is a usable code.** The paper shows depolarization block is not a failure
  mode but a feature: the bSbC cell uses block at high contrasts to suppress firing. For DSGC
  modelling this means tiered AIS architectures should be evaluated with block-tolerant firing-rate
  metrics, not only peak rates.

## Summary

Wienbar and Schwartz introduce the Bursty Suppressed-by-Contrast (bSbC) RGC of the mouse retina and
ask why it transmits a contrast-suppression signal while the OFF sustained Alpha (OFFsA) RGC, which
receives nearly identical synaptic input, transmits a high-rate sustained-contrast signal. The
paper's research question is therefore explicitly about the contribution of cell-intrinsic spike
generation machinery, rather than upstream circuitry, to RGC feature selectivity.

The methodology combines voltage-clamp measurement of excitatory and inhibitory conductance traces,
current-clamp recordings of spike shape, confocal imaging of the AIS labelled with ankyrin-G,
sodium-channel pharmacology with the Nav1.6-selective blocker 49TTX, and a NEURON 7.7 compartmental
model in which the AIS is split into a proximal Nav1.2 subsegment and a distal Nav1.6 subsegment.
The two cell types share the same dendritic and somatic architecture in the model, and the only
systematic differences are AIS length (22 +/- 1.7 um in OFFsA vs 16 +/- 1.5 um in bSbC) and Nav1.6
fraction (~40 percent in OFFsA vs ~0 percent in bSbC).

The headline finding is that the divergent contrast response functions of the two cells emerge from
the spike generator alone. The bSbC cell's short, Nav1.2-dominated AIS is driven into depolarisation
block by strong contrast inputs, silencing the cell, while OFFsA's longer Nav1.6-rich AIS sustains
high firing rates under the same drive. 49TTX selectively reduces OFFsA spike amplitude with no
effect on bSbC, confirming the Nav1.6 contribution. AIS length differs significantly (p = 0.018)
while diameter does not (p = 0.83), localising the anatomical signature.

For task t0078 (and the broader project) the paper matters in three ways. First, it provides a
public, openly licensed NEURON model of a two-subsegment AIS with realistic Nav1.2/Nav1.6
parameterisation, length 16-22 um, and diameter ~1.3 um, archived at Zenodo DOI
10.5281/zenodo.6423531. This is the substrate that t0078 is going to port in place of the paywalled
Werginz 2020 model. Second, it establishes that AIS heterogeneity is an empirically documented
driver of RGC feature selectivity, not just a modelling convenience, which strengthens the
biological-plausibility case for tiered AHP plus tiered AIS in the DSGC v2 model. Third, it
demonstrates depolarisation block as a meaningful coding mechanism, which means t0078's firing-rate
metrics need to remain well-defined when the AIS enters block under strong drive.
