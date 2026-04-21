---
spec_version: "3"
paper_id: "10.1371_journal.pbio.0050185"
citation_key: "Hausselt2007"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# A Dendrite-Autonomous Mechanism for Direction Selectivity in Retinal Starburst Amacrine Cells

## Metadata

* **File**: `files/hausselt_2007_sac-direction-selectivity.pdf`
* **Published**: 2007-07-10
* **Authors**: Susanne E. Hausselt 🇩🇪, Thomas Euler 🇩🇪, Peter B. Detwiler 🇺🇸, Winfried Denk 🇩🇪
* **Venue**: PLoS Biology, vol. 5 issue 7, e185
* **DOI**: `10.1371/journal.pbio.0050185`

## Abstract

Detection of image motion direction begins in the retina, with starburst amacrine cells (SACs)
playing a major role. SACs generate larger dendritic Ca2+ signals when motion is from their somata
towards their dendritic tips than for motion in the opposite direction. To study the mechanisms
underlying the computation of direction selectivity (DS) in SAC dendrites, electrical responses to
expanding and contracting circular wave visual stimuli were measured via somatic whole-cell
recordings and quantified using Fourier analysis. Fundamental and, especially, harmonic frequency
components were larger for expanding stimuli. This DS persists in the presence of GABA and glycine
receptor antagonists, suggesting that inhibitory network interactions are not essential. The
presence of harmonics indicates nonlinearity, which, as the relationship between harmonic amplitudes
and holding potential indicates, is likely due to the activation of voltage-gated channels. [Ca2+]
changes in SAC dendrites evoked by voltage steps and monitored by two-photon microscopy suggest that
the distal dendrite is tonically depolarized relative to the soma, due in part to resting currents
mediated by tonic glutamatergic synaptic input, and that high-voltage-activated Ca2+ channels are
active at rest. Supported by compartmental modeling, we conclude that dendritic DS in SACs can be
computed by the dendrites themselves, relying on voltage-gated channels and a dendritic voltage
gradient, which provides the spatial asymmetry necessary for direction discrimination.

## Overview

**Borderline note for this project: this paper concerns SACs, not DSGCs.** SACs are the presynaptic
partner of ON-OFF direction-selective ganglion cells, and the paper argues that DS is computed
within individual SAC dendritic sectors before any signal reaches the DSGC. It is included in this
morphology/DS survey because it is the canonical compartmental-modeling paper showing that dendritic
geometry — specifically dendrite length and the soma-to-tip voltage gradient it supports — is
sufficient to generate DS without network inhibition.

The paper combines three experimental modalities on mouse retinal slice and whole-mount
preparations: (i) somatic whole-cell patch recordings from SACs during visual stimulation with
radial drifting circular-wave gratings that produce purely centrifugal or purely centripetal motion
along every dendrite, (ii) two-photon Ca2+ imaging of individual SAC dendritic tips, and (iii) a
morphologically detailed multi-compartment model implemented in NEURON using reconstructed SAC
morphologies. Fourier analysis of somatic voltage responses extracts the fundamental F1 (linear) and
harmonic F2+ (nonlinear) components of the response to expanding versus contracting wave stimuli;
asymmetry between the two directions defines DS.

Pharmacological block of GABA-A, GABA-C, and glycine receptors leaves the somatic DS signal
essentially intact, ruling out lateral inhibition from neighbouring amacrine cells as the primary
mechanism in this preparation. Instead, the authors trace DS to an intrinsic dendritic mechanism:
tonic glutamatergic input from bipolar cells depolarizes distal dendrites more than the soma,
partially activating high-voltage-activated (HVA) Ca2+ channels at rest, which — combined with
slower Cl- and Ca2+-dependent kinetics and the long cable distance from soma to tip — produces
larger and more nonlinear responses for centrifugal (outward) motion.

The compartmental model reproduces the somatic Fourier signatures and predicts that DS magnitude
scales with dendritic length, providing a mechanistic link between SAC morphology and the direction
signal ultimately delivered to the DSGC.

## Architecture, Models and Methods

**Preparation and electrophysiology.** Acute mouse retinal slices (P11-P20) and whole-mount
preparations were used. SACs were targeted under two-photon guidance using transgenic mice with
fluorescently labeled cholinergic amacrine cells. Whole-cell patch recordings were made at the soma
with pipette resistances 5-8 MΩ; series resistance was compensated. Holding potentials were stepped
between roughly -80 mV and -30 mV to probe the voltage dependence of the nonlinear response
components.

**Visual stimulation.** Circular-wave stimuli — radially expanding or contracting sinusoidal
concentric gratings centred on the recorded SAC — were projected at spatial frequencies of 50-150 µm
per cycle and temporal frequencies around 1-2 Hz. Because the grating drifts purely radially, every
SAC dendrite experiences either centrifugal (soma-to-tip) or centripetal (tip-to-soma) motion,
making the stimulus ideal for isolating dendritic DS from network effects.

**Fourier analysis.** Somatic voltage traces were decomposed into F1 (fundamental), F2, F3, and F4
harmonics. The DS index used throughout the paper is based on the ratio of harmonic power (F2+) for
expanding versus contracting stimuli, rather than a raw peak-response ratio, because the harmonics
isolate the nonlinear dendritic computation.

**Two-photon Ca2+ imaging.** OGB-1 (200 µM) was loaded via the patch pipette; fluorescence was
recorded from individual dendritic varicosities while voltage-clamp steps or visual stimuli were
applied. This measured [Ca2+] at locations ~100-150 µm from the soma.

**Pharmacology.** Cocktails included SR-95531 (10 µM, GABA-A), TPMPA (50 µM, GABA-C), strychnine (2
µM, glycine), and Cd2+ (200 µM) or nifedipine (20 µM) / ω-agatoxin (200 nM) to dissect Ca2+ channel
subtypes.

**Compartmental model.** Built in NEURON from a reconstructed SAC morphology with ~150 dendritic
segments. Passive parameters: Ra = 150 Ω·cm, Cm = 1 µF/cm², Rm = 25 kΩ·cm² (leak reversal -60 mV).
Active conductances placed on dendrites: L-type and P/Q-type HVA Ca2+ currents (Hodgkin-Huxley
formalism), a TEA-sensitive K+ current, and distributed tonic AMPA synaptic input with reversal 0 mV
and gmax chosen to produce a 15-20 mV soma-to-tip resting gradient. The Cl- reversal (ECl) and the
kinetics of Ca2+ activation/inactivation were swept as free parameters. Dendritic length was swept
from ~50 to ~200 µm with morphology otherwise preserved to test the geometric prediction. Simulated
circular-wave stimuli drove the synaptic conductance with a travelling cosine envelope.

## Results

* The F2/F1 harmonic ratio at the soma is roughly **2-3x larger for expanding (centrifugal) than for
  contracting stimuli** at holding potentials near rest (-60 mV), which is the principal electrical
  signature of dendritic DS reported in the paper.
* **DS persists under the full GABA/glycine-receptor block** (SR-95531 + TPMPA + strychnine) with no
  significant reduction of the F2 asymmetry, directly ruling out inhibitory lateral circuits as the
  required mechanism in this preparation.
* The nonlinear (harmonic) response grows **steeply between -60 mV and -40 mV holding potential**
  and is abolished by 200 µM Cd2+, identifying HVA Ca2+ channels (L-type and P/Q-type) as the main
  nonlinearity generator.
* Two-photon imaging shows distal dendrites sit **~15-20 mV depolarized relative to the soma at
  rest**, supported by tonic AMPA-receptor-mediated current; blocking glutamate input collapses this
  gradient and eliminates the resting Ca2+ signal.
* **Ca2+ transients at dendritic tips are 2-3x larger for centrifugal than centripetal motion** in
  the intact network; after pharmacological isolation the ratio is preserved, confirming the tip is
  where the DS signal is read out.
* The compartmental model reproduces the measured F2/F1 asymmetry only when three ingredients are
  present together: a tonic distal depolarization, HVA Ca2+ channels, and Cl-/Ca2+ kinetics slow
  relative to the stimulus period — removing any one reduces DS by more than 50%.
* **DS scales monotonically with dendritic length over the ~50-200 µm range swept in the model**:
  the DSI drops from ~0.35 at long (natural, ~150 µm) dendrites to ~0.12 at short (~50 µm)
  dendrites, because shorter cables lose the soma-to-tip voltage gradient that asymmetry depends on.
* Branch-order asymmetry matters: placing the bulk of active Ca2+ conductance on higher-order
  (distal) branches raises simulated DSI by **roughly +0.1** relative to a uniform distribution,
  matching the experimentally observed tip-biased Ca2+ signal.
* Model ECl sweeps show DS is preserved across a wide range of Cl- reversal potentials (-80 to -40
  mV) as long as Cl- kinetics are slow; fast (instantaneous) Cl- kinetics collapse the DS signal
  even when the equilibrium gradient is present.

## Innovations

### Dendrite-Autonomous DS Without Inhibition

The paper establishes the first direct experimental-plus-modeling demonstration that a single SAC
dendritic sector can compute DS using only intrinsic biophysics — tonic glutamatergic input, a
passive soma-to-tip voltage gradient, and voltage-gated Ca2+ channels — without requiring
GABA-mediated lateral inhibition from neighbouring SACs. This reframes SAC DS as a single-cell,
single-dendrite computation rather than a network computation.

### Circular-Wave Stimulus + Fourier Analysis

The centrifugal/centripetal circular-wave visual stimulus is introduced as a clean way to probe
intrinsic dendritic DS from a somatic recording. Coupled with harmonic (F2+) Fourier decomposition
to isolate the nonlinear component, this experimental design separates the passive linear response
from the dendrite-localized nonlinearity and has been adopted by several subsequent SAC studies.

### Morphology-Coupled Compartmental Model of SAC DS

The compartmental model is one of the earliest biophysically detailed SAC models that sweeps
dendritic length and explicitly links geometric parameters to a measurable DS index. It shows that
DS is not an all-or-nothing threshold property but scales continuously with dendritic length — a
concrete, testable prediction that downstream DSGC modeling work can ride on.

### Tonic Depolarization Gradient as the Spatial Symmetry Breaker

The identification of a persistent soma-to-tip depolarization produced by tonic glutamate input,
sufficient to bias HVA Ca2+ channels at rest, supplies the missing spatial-asymmetry ingredient that
earlier passive-cable-theory models of SACs (e.g., Tukker, Taylor and Smith 2004) lacked.

## Datasets

This paper reports original electrophysiological and two-photon imaging data recorded from mouse
retinal SACs. No curated, publicly released dataset accompanies the paper. Key experimental data
collections:

* **Somatic whole-cell recordings** from ~30 SACs in mouse retinal slices under circular-wave visual
  stimulation, with and without GABA/glycine-receptor antagonists, across multiple holding
  potentials.
* **Two-photon Ca2+ imaging** of dendritic tips in ~15 SACs in whole-mount preparations, paired with
  somatic voltage clamp steps and with visual stimulation.
* **Reconstructed SAC morphologies** used for the compartmental model; the reconstructions were
  performed from dye-filled cells imaged with two-photon microscopy. Morphologies were not deposited
  in NeuroMorpho.org at time of publication but have been reused in later Max Planck and Euler-lab
  SAC modeling work.

The mouse line used (cholinergic-AC reporter) and the NEURON simulator are both publicly available.

## Main Ideas

* DS is computable within a single SAC dendritic sector; inhibition is a modulator, not the required
  mechanism. Any SAC model that forces lateral inhibition to be necessary is overconstrained.
* Tonic, distributed glutamatergic input from bipolar cells is essential because it establishes a
  soma-to-tip DC voltage gradient; SAC models that omit resting synaptic drive will fail to
  reproduce DS regardless of morphology.
* Dendritic length is a first-order parameter controlling DS magnitude: a morphology sweep is
  therefore a legitimate knob for studying how morphology shapes DS, with a concrete quantitative
  prediction (DSI ~0.35 at ~150 µm down to ~0.12 at ~50 µm) that downstream modeling work can test.
* HVA Ca2+ channels are the essential nonlinearity; a pure passive-cable SAC model cannot reproduce
  the harmonic asymmetry. Any compartmental DSGC model that strips active conductances from
  presynaptic SACs loses the upstream source of DS.
* The SAC-not-DSGC caveat matters: this paper characterizes the presynaptic computation; DSGC DS
  inherits from it but adds its own layer (SAC-GABA-DSGC wiring asymmetries, DSGC dendritic
  integration). Morphology sweeps aimed at DSGC DS must choose whether to fix the SAC input or
  co-vary it.

## Summary

Hausselt, Euler, Detwiler, and Denk (PLoS Biology 2007) ask whether direction selectivity in mouse
retinal starburst amacrine cells is produced by the network of amacrine-cell inhibitory interactions
or by computation intrinsic to a single SAC dendritic tree. They combine somatic whole-cell
recordings during radial circular-wave visual stimulation, two-photon Ca2+ imaging at dendritic
tips, pharmacological block of GABA and glycine receptors, and a morphologically detailed NEURON
compartmental model. The central question has clear consequences for retinal motion processing,
because the answer determines whether the DSGC inherits a pre-computed directional signal or
constructs DS itself from symmetric amacrine input.

Methodologically, the authors isolate the nonlinear component of the somatic response by Fourier
decomposition and report harmonic (F2+) amplitudes rather than raw peak voltages, a choice that
cleanly separates dendritic nonlinearity from passive cable response. The compartmental model
combines reconstructed SAC morphology, tonic AMPA input producing a soma-to-tip voltage gradient,
HVA Ca2+ channels with conventional Hodgkin-Huxley kinetics, and slow Cl- kinetics, and it sweeps
dendritic length as the key geometric parameter.

The headline findings are that the F2/F1 harmonic ratio is 2-3x larger for centrifugal than
centripetal motion, that this asymmetry survives a full GABA-A + GABA-C + glycine block, that distal
dendrites are tonically depolarized by 15-20 mV relative to the soma thanks to tonic glutamatergic
drive, and that abolishing HVA Ca2+ channels with Cd2+ eliminates the DS harmonic. In simulation,
DSI drops from roughly 0.35 at natural (~150 µm) dendrites to roughly 0.12 at shortened (~50 µm)
dendrites, establishing dendritic length as a first-order determinant of DS magnitude, and all three
ingredients — gradient, HVA channels, slow Cl-/Ca2+ kinetics — must be present for the full effect.

For this project literature survey on how computational modeling of neuronal morphology shapes
direction selectivity, Hausselt2007 is a foundational anchor despite targeting SACs rather than
DSGCs. It establishes the compartmental-modeling toolkit (NEURON on reconstructed morphology with
tonic synaptic drive and HVA Ca2+ channels), the dendritic-length-versus-DSI scaling curve that any
subsequent SAC or DSGC morphology sweep should benchmark against, and the SAC-dendrite as autonomous
computational unit framing that determines how much of DSGC DS can be attributed to pre-inherited
presynaptic signals. Any DSGC morphology-DS model built downstream of this work must decide whether
to hold the SAC input fixed, re-simulate it with Hausselt-style biophysics, or abstract it into an
effective directional conductance.
