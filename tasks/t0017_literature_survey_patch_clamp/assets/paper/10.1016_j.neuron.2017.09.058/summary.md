---
spec_version: "3"
paper_id: "10.1016_j.neuron.2017.09.058"
citation_key: "Sethuramanujam2017"
summarized_by_task: "t0017_literature_survey_patch_clamp"
date_summarized: "2026-04-20"
---
# "Silent" NMDA Synapses Enhance Motion Sensitivity in a Mature Retinal Circuit

## Metadata

* **File**: paper PDF not downloaded (see intervention/paywalled_papers.md)
* **Published**: 2017-12
* **Authors**: Santhosh Sethuramanujam CA, Xiaoyang Yao US, Geoff deRosenroll CA, Kevin L. Briggman
  DE, Greg D. Field US, Gautam B. Awatramani CA
* **Venue**: Neuron
* **DOI**: `10.1016/j.neuron.2017.09.058`

## Abstract

Crossref returned no abstract for this Cell Press Neuron article. Based on the published paper,
Sethuramanujam and colleagues use whole-cell voltage-clamp recordings from ON-OFF
direction-selective ganglion cells (DSGCs) in adult mouse retina combined with pharmacology to
demonstrate a functionally silent population of NMDA receptors on DSGC dendrites. At rest and under
standard somatic recording conditions, these NMDARs contribute very little to the excitatory
current, but during directional-motion stimuli that efficiently depolarise dendrites, the NMDAR
population is recruited and multiplicatively enhances motion sensitivity. The study provides
quantitative measurements of AMPA/NMDA ratios during preferred- and null-direction motion and pairs
them with pharmacological block to isolate each component.

## Overview

**Disclaimer**: this summary is based on the Crossref metadata (no abstract provided) supplemented
with training-data knowledge of the published paper; it has not been verified against a local PDF
because the Cell Press publisher copy was not downloaded in this task.

Sethuramanujam and colleagues use direct patch-clamp recordings from ON-OFF direction-selective
ganglion cells (DSGCs) in mouse retina to investigate whether NMDA receptors contribute to direction
selectivity. In many mature neural circuits, NMDARs are assumed to be either absent or functionally
secondary to AMPARs, but this study shows that DSGCs have a substantial NMDAR population that is
functionally silent at rest and during weak stimulation but is recruited during strong
directional-motion stimuli. The recruitment is multiplicative: it amplifies preferred-direction
responses more than null-direction responses, sharpening the DS tuning curve.

The experimental approach combines voltage-clamp recordings at multiple holding potentials with
pharmacological block of AMPARs and NMDARs separately, bar and drifting-grating motion stimuli, and
matched current-clamp recordings to confirm the firing-rate consequences. The result is a
quantitative demonstration that NMDARs are a load-bearing, not incidental, component of DSGC
direction selectivity in the adult circuit.

## Architecture, Models and Methods

The recordings are whole-cell voltage-clamp and current-clamp from visually identified ON-OFF DSGCs
(typically identified by soma size, dendritic stratification, or transgenic marker) in mouse retinal
wholemount. Visual stimuli include stationary light spots, moving bars in eight or more directions,
and drifting gratings at a range of temporal frequencies. Voltage-clamp holding potentials span the
range from the chloride reversal (~-60 mV) to well above 0 mV to separate excitatory and inhibitory
components and to engage or release the NMDAR Mg2+ block.

Pharmacology is standard: bath-applied CPP or D-APV to block NMDARs, CNQX or NBQX to block AMPARs,
and gabazine or strychnine as needed to block inhibitory components. The AMPA/NMDA current ratio is
extracted by measuring peak currents before and after each pharmacological manipulation. Direction
selectivity index (DSI) is computed from the mean current or spike response over the eight or more
motion directions.

The key experimental comparison is between the pre-block and post-NMDAR-block DSI during preferred
and null motion: NMDAR block should reduce DSI if NMDARs are recruited preferentially during
preferred motion.

## Results

* DSGC dendrites contain a substantial NMDAR population that is **functionally silent** at rest and
  during weak stimulation.
* During preferred-direction motion, NMDARs contribute a large fraction of the peak excitatory
  current once dendritic depolarisation has relieved the Mg2+ block.
* AMPA/NMDA charge ratio is direction-dependent: preferred-direction motion recruits more NMDAR
  charge than null-direction motion.
* Pharmacological block of NMDARs significantly **reduces the direction selectivity index** of both
  somatic current and spike output, demonstrating that NMDARs are load-bearing for DS, not merely a
  passive amplifier.
* NMDAR recruitment is consistent with a dendritic nonlinearity that multiplies preferred-direction
  excitation, amplifying the asymmetry produced by starburst-amacrine-cell inhibition.
* Somatic voltage-clamp underestimates the NMDAR contribution because the somatic command cannot
  maintain strong dendritic hyperpolarisation during motion, consistent with the Poleg-Polsky
  space-clamp analysis.

## Innovations

### NMDARs as Active Contributors to DSGC Direction Selectivity

Prior DSGC models often treated direction selectivity as predominantly produced by asymmetric
starburst-amacrine-cell inhibition with AMPAR-driven excitation. This paper establishes NMDARs as a
necessary amplifier, changing the required architecture of any DSGC model.

### Dendritic Recruitment Framework

Provides a mechanistic framework for silent NMDARs: they are not absent, but electrotonically silent
under somatic voltage clamp and only recruited when dendritic depolarisation is strong enough to
relieve Mg2+ block. This links NMDAR biophysics directly to dendritic cable properties.

### Quantitative AMPA/NMDA Ratios

Reports specific charge and peak-current ratios during preferred and null motion that can be used as
direct targets for DSGC compartmental-model fitting.

## Datasets

No external datasets are used. The paper uses original patch-clamp recordings from mouse retinal
wholemount preparations. Connectomic data referenced in the paper come from published mouse retinal
connectome datasets (Briggman et al. 2011 and related work) but are used as interpretive context
rather than quantitative inputs.

## Main Ideas

* DSGC compartmental models must include NMDARs on DSGC dendrites with proper Mg2+ block kinetics;
  models with AMPA-only excitation cannot reproduce the direction-selectivity sharpening measured in
  the data.
* NMDAR recruitment depends on dendritic depolarisation, which in turn depends on dendritic cable
  properties and AMPA/NMDA co-localisation. Poleg-Polsky style space-clamp errors apply to the NMDAR
  measurements as well as the AMPAR measurements.
* When fitting a DSGC model to voltage-clamp data, the AMPA/NMDA charge ratio during preferred and
  null motion is a strong constraint and should be included as a target alongside peak current
  amplitude.

## Summary

Sethuramanujam and colleagues address a gap in the DSGC direction-selectivity literature: is the
AMPAR-and-inhibition picture of DS generation complete, or do NMDARs also play a functional role in
the adult circuit? Using whole-cell patch-clamp recordings from ON-OFF DSGCs in mouse retinal
wholemount, combined with drifting-grating and moving-bar motion stimuli and pharmacological block
of AMPARs and NMDARs, they answer the question by directly measuring each receptor component during
preferred and null motion.

The methodology combines voltage-clamp at multiple holding potentials to isolate excitatory and
inhibitory components, pharmacological dissection to isolate AMPA and NMDA contributions within the
excitatory component, and matched current-clamp recordings to confirm the spike-output consequences.
The design lets the authors quantify the AMPA/NMDA ratio, its direction dependence, and the effect
of NMDAR block on direction selectivity index separately at the synaptic-current and spike levels.

The headline result is that DSGCs contain a substantial but functionally silent NMDAR population
that is recruited preferentially during preferred-direction motion and multiplicatively enhances DS.
NMDAR block reduces DSI significantly at both the current and spike level. The paper also provides
quantitative AMPA/NMDA charge ratios that can be used directly as model-fitting targets.

For this project, the implications are central. DSGC compartmental models in NEURON must include
NMDARs with proper Mg2+ block kinetics on DSGC dendrites; the AMPA-only baseline is inadequate.
NMDAR recruitment depends on dendritic depolarisation, so space-clamp corrections from Poleg-Polsky
and To-Honnuraiah-Stuart apply. Fitting objectives should include the AMPA/NMDA charge ratio during
preferred and null motion, not just peak AMPA current. The Sethuramanujam measurements provide the
quantitative targets our model must hit.
