---
spec_version: "3"
paper_id: "10.1038_s41593-017-0046-4"
citation_key: "Gruntman2018"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# Simple integration of fast excitation and offset, delayed inhibition computes directional selectivity in Drosophila

## Metadata

* **File**: `files/gruntman_2018_t4-directional-selectivity.pdf`
* **Published**: 2018 (online 8 January 2018; print Feb 2018, Nat. Neurosci. 21(2):250-257)
* **Authors**: Eyal Gruntman \U0001F1FA\U0001F1F8, Sandro Romani \U0001F1FA\U0001F1F8, Michael B.
  Reiser \U0001F1FA\U0001F1F8 (Janelia Research Campus, HHMI)
* **Venue**: Nature Neuroscience (journal article)
* **DOI**: `10.1038/s41593-017-0046-4`

## Abstract

A neuron that extracts directionally selective motion information from upstream signals lacking this
selectivity must compare visual responses from spatially offset inputs. Distinguishing among
prevailing algorithmic models for this computation requires measuring fast neuronal activity and
inhibition. In the Drosophila melanogaster visual system, a fourth-order neuron\u2014T4\u2014is the
first cell type in the ON pathway to exhibit directionally selective signals. Here we use in vivo
whole-cell recordings of T4 to show that directional selectivity originates from simple integration
of spatially offset fast excitatory and slow inhibitory inputs, resulting in a suppression of
responses to the nonpreferred motion direction. We constructed a passive, conductance-based model of
a T4 cell that accurately predicts the neuron's response to moving stimuli. These results connect
the known circuit anatomy of the motion pathway to the algorithmic mechanism by which the direction
of motion is computed.

## Overview

**Invertebrate flag: Drosophila T4 neuron.** Demonstrates direction selectivity emerges from
asymmetric arrangement of excitatory and delayed-inhibitory inputs along the dendrite \u2014 a
morphology-as-input-layout mechanism. This is the canonical fly T4 paper for linking single- neuron
dendritic integration to DS, and it makes the strong claim that the elaborate T4 arbor is not itself
the computational substrate of DS but serves to spatially sample offset inputs.

Gruntman, Romani and Reiser resolve a long-standing ambiguity in invertebrate motion detection by
using targeted in vivo whole-cell patch-clamp recordings of Drosophila T4 neurons \u2014 the fourth-
order columnar cells that are the first site of DS in the fly ON motion pathway. Prior work on T4
relied primarily on calcium imaging, which is insensitive to hyperpolarization and too slow to
resolve the sub-ommatidial timing that would distinguish Hassenstein\u2013Reichardt (HR) preferred-
direction enhancement from Barlow\u2013Levick (BL) null-direction suppression. By recording membrane
potential directly, the authors map the T4 receptive field (RF) with single-position bar flashes
(SPFRs) and two-step apparent-motion stimuli.

Their central empirical finding is that the T4 RF has a spatially and temporally asymmetric input
arrangement: the leading side is purely excitatory and fast; the trailing side carries delayed,
slower inhibitory input. The peak-to-peak E\u2013I spatial offset is approximately 6\u00B0 of visual
angle \u2014 the spacing between neighboring ommatidia. Crucially, excitatory onset time is
invariant across the RF; the directional asymmetry comes from trailing-side inhibition, not from an
upstream delay line. Two-step apparent motion yields DS produced entirely by null-direction
suppression (no preferred-direction enhancement). Superposition of stationary single-position
responses already reproduces the directional asymmetry, implying the integration is close to linear
rather than the strongly nonlinear multiplication of HR or the AND-NOT veto of BL.

To link biophysics to function, the authors build a passive, conductance-based multicompartment
model of a single T4 cell whose morphology was reconstructed from FIB-SEM electron microscopy
(Janelia FlyEM). The fitted model reproduces both SPFR responses (training data) and moving-bar
responses (held-out generalization) quantitatively. Ablating inhibition abolishes DS at every tested
speed; and \u2014 strikingly \u2014 collapsing all 154 synapses onto the base of the dendrite or
replacing the cell with a single compartment leaves DS essentially unchanged. The morphology-
related variable that matters is the 1D spatial layout of E and I inputs along the PD\u2013ND axis,
not the passive cable properties of the T4 arbor.

## Architecture, Models and Methods

**Experimental side.** Targeted in vivo whole-cell current-clamp recordings (Axon MultiClamp 700B,
10 kHz low-pass) of GFP-labelled T4 neurons in female Drosophila, n = 17 recorded cells (most
analyses on n = 16\u201317 cells; two-step apparent motion from n = 3 cells). Visual stimuli on an
LED arena with approximately 2\u00B0 pixels. Key stimulus sets: (1) moving bars (approximately
2\u00B0 wide, 1 \u00D7 9 pixels) in 8 directions at 4 speeds corresponding to per-step durations of
20, 40, 80 and 160 ms (approximately 112, 56, 28 and 14 \u00B0/s); (2) single-position bar flashes
(SPFRs) at 13+ positions along the PD\u2013ND axis at each of the 4 durations; (3) two-step
apparent-motion pairs separated by 2\u201310\u00B0 at 14 \u00B0/s. PD was estimated from the
vector-average of eight- direction responses. DSI was defined as (R_PD \u2212 R_ND) / R_PD where
each response is the 0.995 quantile of the Vm trace during the stimulus window \u2014 applied
identically to measured, summed, and simulated traces.

**Compartmental model.** The model used a T4 morphology reconstructed from FIB-SEM at 8 nm isotropic
voxels (Janelia FlyEM T4 cell, shared by K. Shinomiya; same data lineage as the later hemibrain
connectome). The reconstructed cell contains **344 sections**, of which **235 form the dendritic
arbor** (approximately 20 \u03BCm span in medulla; axon to lobula plate). Diameters were smoothed
with a 5-section moving average using the TREES toolbox. Simulations in NEURON v7.4. The dendritic
axis was projected to a 1D coordinate x* in [0, 1] and divided into **M = 11 intervals** matching
the 11-position SPFR stimulus grid. Each interval received **N_E = 9 excitatory and N_I = 5
inhibitory** randomly placed analog synapses (total **99 E + 55 I = 154 synapses**). E reversal V_E
= 0 mV, I reversal V_I = \u221270 mV, resting V_L = \u221265 mV. C_m was fixed at **1
\u03BCF/cm\u00B2**; R_m and R_a (axial resistivity) were free. Synapses were implemented as single-
electrode voltage clamps injecting the inverse of a conductance waveform defined by rise/decay time
constants (\u03C4_C,rise, \u03C4_C,decay) and a Gaussian spatial weighting a_C(x*) = A_C \u00B7
exp(\u2212(x* \u2212 \u03BC_C)\u00B2 / (2 \u03C3_C\u00B2)). The synaptic input I_C(t,x*) was a
unit-amplitude pulse of duration T in {20, 40, 80, 160} ms. Fit was nonlinear least squares (Matlab
lsqcurvefit) over 44 SPFR responses (11 positions \u00D7 4 durations); the fitted model was then
used to predict moving-bar responses without re-fitting.

**Model manipulations (morphology-as-layout ablations).** Three variants with all other parameters
held constant: (a) all 154 synapses moved to the first dendritic section; (b) inhibitory conductance
zeroed (g_I = 0); (c) an independent single-compartment variant fit to the same SPFRs. These are
exactly the comparisons a morphology-to-DS modelling study wants.

## Results

* **Measured T4 DSI is strongly speed-dependent**; significant DS at all four speeds (p < 0.05,
  one-sided unpaired t-test, n = 17 cells), with the two slower speeds (14 and 28 \u00B0/s)
  significantly more selective than the two faster speeds (p < 0.05, paired t-test).
* **Two-step apparent-motion reveals pure ND suppression with no PD enhancement.** Trailing-side bar
  pairs give mean **DSI = 0.46** (individual-cell values 0.47, 0.50, 0.16) while leading- side bar
  pairs are motion-blind at **DSI = 0.03** (0.02, 0.06, 0.10); bar pairs approximately 10\u00B0
  apart show neither enhancement nor suppression.
* **Excitation\u2013inhibition spatial offset of approximately 6\u00B0 of visual angle** (matches
  the inter-ommatidial angle), with excitation on the leading side of the RF and hyperpolarization
  only on the trailing side.
* **Excitatory onset time is invariant across RF position**; only decay time varies (significant
  position effect), indicating no upstream time delay in the Hassenstein\u2013Reichardt sense.
  Directional asymmetry arises from trailing-side inhibition, not from a delayed excitatory line.
* **EM-constrained multicompartment model quantitatively reproduces moving-bar responses** at all
  four speeds despite being fit only to stationary SPFRs \u2014 successful generalization from 44
  static responses to 4 speeds \u00D7 2 directions of moving-bar data (**99 E + 55 I = 154
  synapses** on a **344-section, approximately 20 \u03BCm** T4 dendrite).
* **Removing inhibition abolishes DSI in the model at every tested speed** \u2014 depolarizing
  inputs alone cannot produce DS, ruling out a pure cable-theory/PD-enhancement account.
* **Morphology as spatial layout, not cable geometry, carries DS:** collapsing all 154 synapses onto
  the first dendritic section or running an independent single-compartment model both reproduce the
  measured DSI-vs-speed curve within negligible differences from the full multicompartment
  simulation, while preserving the 6\u00B0 E\u2013I spatial offset in the input model.

## Innovations

### First in vivo whole-cell recording of T4 membrane potential

Prior T4 literature was dominated by calcium imaging, which is blind to hyperpolarization and too
slow to resolve HR-style temporal delays. Direct current-clamp recordings expose the trailing- side
inhibition and the position-invariance of excitatory onset \u2014 two facts calcium imaging cannot
see.

### EM-constrained, parameter-optimized compartmental model of a T4 neuron

The first biophysical T4 model built on an FIB-SEM reconstruction and fit to per-position SPFRs,
with held-out generalization to moving-bar stimuli. Establishes a template for morphology-to-
function modelling in invertebrate DS cells.

### Explicit morphology-ablation test

By collapsing all synaptic inputs to the dendritic base and comparing against a single- compartment
variant, the authors directly test whether the elaborate T4 dendrite is computationally required for
DS. It is not \u2014 the arbor's role reduces to spatially sampling offset inputs, not nonlinearly
integrating them. An unusually clean null result for morphology- dependent computation.

### Reframing T4 as linear integration plus dynamic shunting

The authors argue T4's DS is better described as a Torre\u2013Poggio-style linear sum of offset E
and delayed-I filters followed by a passive dynamic shunting nonlinearity (E \u2212 \u03B1 I) / (1 +
E + I), rather than HR multiplication or BL veto. This places T4 closer to the Adelson\u2013Bergen
motion- energy family than to the classical fly motion-detector caricature.

## Datasets

* **Whole-cell recording dataset**: n = 17 T4 neurons (female Drosophila), Vm traces for 8-
  direction moving bars (4 speeds), SPFRs at 11+ positions \u00D7 4 durations, two-step apparent-
  motion pairs (n = 3 cells). Raw data and code stated as "available to editors and reviewers upon
  request" in the Reporting Summary.
* **T4 EM morphology**: a single T4 cell reconstructed from Janelia FlyEM FIB-SEM data (153 \u00D7
  85 \u00D7 180 \u03BCm optic-lobe volume, 8 nm isotropic voxels), shared by K. Shinomiya. 344
  sections, 235 dendritic sections. Reconstruction with NeuTu-EM. Same data lineage as the later
  Janelia hemibrain connectome.
* No independent training/test split beyond the SPFR-to-moving-bar generalization described above.

## Main Ideas

* **Morphology in invertebrate DS can reduce to a 1D spatial layout variable.** For T4, what matters
  is the E\u2013I offset along the PD\u2013ND dendritic axis (approximately 6\u00B0 of visual
  angle); the detailed dendritic arbor geometry and cable properties do not contribute beyond input
  sampling. For our vertebrate RGC work this provides a clean null to beat: any DS contribution from
  RGC morphology beyond input layout must be explicitly demonstrated against a single-compartment
  control.
* **Inhibition is load-bearing for DS in invertebrate T4.** Zeroing g_I abolishes DS at every speed.
  This mirrors the vertebrate starburst/DSGC story and argues for modelling AMPA + GABA inputs
  (rather than excitation-only HR) in any morphology-to-DS study.
* **The E/I spatial-offset-vs-temporal-delay distinction is experimentally falsifiable.** The
  invariant excitatory onset time across RF position directly rules out an HR delay-line mechanism
  for T4. Our project should adopt analogous SPFR-onset-time and two-position superposition analyses
  when probing DS in a morphology-varying model.
* **Methodology transfer:** SPFR-to-moving-bar generalization is a strong validation pattern. Fit
  parameters to stationary-input responses, then predict moving responses. Adopt this pattern when
  we fit our compartmental RGC model to patch-clamp SPFR-analogue data.
* **Target metric conventions:** DSI = (R_PD \u2212 R_ND) / R_PD with R as the 0.995 quantile of the
  stimulus-window Vm. This is the in vivo invertebrate convention for Vm-based DSI and should be
  reported alongside our project's AP-frequency DSI for cross-paper comparability.

## Summary

This paper asks how direction selectivity is implemented in Drosophila T4 neurons, the first site in
the fly ON motion pathway where directionally selective signals appear. The motivation is to resolve
which of the classical algorithmic motion detectors \u2014 Hassenstein\u2013Reichardt
multiplication, Barlow\u2013Levick veto, or an Adelson\u2013Bergen motion-energy filter \u2014 the
fly circuit actually implements. The authors focus on T4 because prior calcium-imaging evidence had
been ambiguous: the indicator is blind to hyperpolarization and too slow to resolve the sub-
ommatidial timing differences that would distinguish these models.

Methodologically, the study combines targeted in vivo whole-cell patch-clamp of GFP-labelled T4
cells (n = 17) with a biophysical, compartmental model of a single T4 cell whose morphology was
reconstructed from Janelia FlyEM FIB-SEM. They map the receptive field with single-position bar
flashes and with two-step apparent-motion pairs, extract per-position onset-time and decay-time, and
then fit a passive conductance-based model (99 excitatory and 55 inhibitory synapses on a
344-section dendrite) to the stationary SPFRs. They test generalization by predicting moving-bar
responses the model never saw, and they run three clean model ablations: remove inhibition, collapse
all synapses to the dendritic base, and replace the whole cell with a single compartment.

The headline findings are that T4's direction selectivity arises from spatially offset fast
excitatory and delayed inhibitory inputs (approximately 6\u00B0 E\u2013I offset along the PD\u2013ND
axis) with invariant excitatory onset times across the receptive field, so there is no HR-style
delay line. Two-step apparent motion produces pure null-direction suppression (DSI approximately
0.46 on the trailing side versus DSI approximately 0.03 on the leading side), with no preferred-
direction enhancement. The conductance-based model reproduces DSI vs speed quantitatively for moving
stimuli; removing inhibition abolishes DSI at every speed; and \u2014 critically for
morphology-modelling work \u2014 collapsing all synapses to the dendritic base or using a single-
compartment variant reproduces the full-dendrite DSI almost exactly. The T4 arbor's role is
therefore input sampling, not nonlinear integration.

For this project's literature survey on morphology-to-DS modelling, this is the canonical
invertebrate reference and a strong null result: the morphology-related variable that drives DS in
T4 is not dendritic cable geometry but the 1D spatial layout of excitatory and inhibitory inputs
along the PD\u2013ND dendritic axis, combined with a dynamic passive shunting nonlinearity. That
gives our compartmental RGC model a precise contrastive hypothesis: if dendritic morphology
contributes to DS beyond input layout in vertebrate DSGCs, it must do so via active conductances,
asymmetric passive cable properties, or structured dendritic branching that goes beyond the
mechanisms sufficient for T4. We should reuse Gruntman et al.'s SPFR-to-moving-bar generalization
protocol, their DSI = (R_PD \u2212 R_ND) / R_PD convention, and their collapse-to-base vs full-arbor
ablation design as template comparisons in our own modelling work.
