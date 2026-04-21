---
spec_version: "3"
paper_id: "10.1523_JNEUROSCI.17-16-06023.1997"
citation_key: "Single1997"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# Dendritic Computation of Direction Selectivity and Gain Control in Visual Interneurons

## Metadata

* **File**: `files/single_1997_dendritic-ds-gain-control.pdf`
* **Published**: 1997-08-15
* **Authors**: Sandra Single, Juergen Haag, Alexander Borst (all DE)
* **Venue**: The Journal of Neuroscience, 17(16):6023-6030
* **DOI**: `10.1523/JNEUROSCI.17-16-06023.1997`

## Abstract

The extraction of motion information from time varying retinal images is a fundamental task of
visual systems. Accordingly, neurons that selectively respond to visual motion are found in almost
all species investigated so far. Despite its general importance, the cellular mechanisms underlying
direction selectivity are not yet understood in most systems. Blocking inhibitory input to fly
visual interneurons by picrotoxinin (PTX), we demonstrate that their direction selectivity arises
largely from interactions between postsynaptic signals elicited by excitatory and inhibitory input
elements, which are themselves only weakly tuned to opposite directions of motion. Their joint
activation by preferred as well as null direction motion leads to a mixed reversal potential at
which the postsynaptic response settles for large field stimuli. Assuming the activation ratio of
these opponent inputs to be a function of pattern velocity can explain how the postsynaptic membrane
potential saturates with increasing pattern size at different levels for different pattern
velocities ("gain control"). Accordingly, we find that after blocking the inhibitory input by PTX,
gain control is abolished.

## Overview

This paper studies direction selectivity and gain control in lobula plate tangential cells (LPTCs)
of the blowfly Calliphora erythrocephala — an invertebrate preparation — combining intracellular
electrophysiology with a three-dimensionally reconstructed passive compartmental model. LPTCs
(VS-cells, CH-cells, and the spiking H1 neuron) pool signals from a retinotopic array of local
elementary motion detectors (EMDs) across large dendritic trees and have long served as a canonical
model for dendritic integration of motion.

The central question is whether direction selectivity is already fully encoded in the presynaptic
EMD inputs, or whether it is enhanced postsynaptically by dendritic integration. The authors block
GABAergic inhibition with picrotoxinin (PTX) and observe that direction selectivity collapses: under
PTX, cells respond with excitation to motion in both the preferred and the null directions. This
implies that the underlying motion detectors themselves are only weakly tuned; it is the opponent
interaction between excitatory and inhibitory synapses across the dendrite that sharpens direction
selectivity at the cell body.

Using a reconstructed LPTC morphology populated with 32 EMD inputs (each contributing one excitatory
and one inhibitory conductance), the authors show that a purely passive dendrite equipped with
opponent conductance-based synapses reproduces the measured direction tuning and large-field
saturation ("gain control"). Dendritic morphology is not varied as an explicit parameter here, but
the paper establishes the foundational result that the spatial layout and passive cable properties
of the LPTC dendrite jointly gate direction selectivity through shunting interactions — a result
that subsequent morphology-variation studies build on. A simple isopotential analytical model
recovers the same velocity- and size-dependent saturation, grounding the simulation in a transparent
circuit-level mechanism.

## Architecture, Models and Methods

Preparation. Adult female Calliphora erythrocephala blowflies were waxed onto a holder, and the back
of the head capsule was opened to expose the lobula plate. Intracellular recordings were made from
VS-cells (n = 4) and CH-cells (n = 3) with glass microelectrodes (20 MOhm resistance, filled with 2
M KAc plus 0.5 M KCl). A switched-clamp amplifier sampled membrane potential and injected current at
20 kHz, and signals were digitized at 2 kHz. Long-duration (2-3 h) extracellular recordings were
obtained from the spiking H1 neuron using tungsten electrodes. Motion stimuli were square-wave
gratings (wavelength 18 deg) presented on a CRT at pattern velocities of 72 deg/s and 360 deg/s,
with variable stimulus area to probe size-dependent saturation.

Pharmacology. Picrotoxinin (PTX) was applied either by bath-side injection into the hemolymph (1 x
10^-4 M) after puncturing the neurolemma, or by pressure injection directly into the lobula plate;
intracellular experiments proceeded 15-30 min after application. A higher concentration (3 x 10^-4
M) was used for multi-hour extracellular H1 recordings.

Compartmental model. A three-dimensionally reconstructed VS-cell (cobalt-stained material) was
simulated in the Nemosys compartmental simulator with purely passive membrane: Rm = 2 kOhm.cm^2, Cm
= 0.8 uF/cm^2, Ri = 40 Ohm.cm. Thirty-two elementary motion detectors, each modeled as a
correlation-type Reichardt detector with two input sensors, drove the cell through 32 pairs of
conductance-based synapses distributed over four dendritic membrane regions along the main dendrite
(branchlet diameter under 4 um; membrane area 31-70 x 10^-6 cm^2 per region). Two synaptic regimes
were tested: weakly tuned EMDs (Eexc = +40 mV, Einh = -30 mV) and strongly tuned EMDs (Eexc = +24
mV, Einh = -13 mV). Peak per-detector conductances were 1-2 mS/cm^2. An isopotential analytical
reduction (Equations 1-3) was derived to show that the opponent ratio c = gi/ge determines the
saturation level, and that c itself is a deterministic function of pattern velocity.

## Results

* Under control conditions, motion in both the preferred and the null direction reduces input
  resistance of VS-cells by about **13-14 percent**, confirming simultaneous activation of
  excitatory and inhibitory conductances in both directions.
* PTX application reduces the motion-induced input-resistance change to **less than 50 percent** of
  the control value for null-direction motion and to **about 60 percent** for preferred- direction
  motion, consistent with selective block of the inhibitory component.
* After PTX, null-direction stimuli that had previously elicited hyperpolarization now produce
  **depolarizing** responses of the same sign as preferred-direction responses, demonstrating that
  direction selectivity of LPTCs is not inherited intact from the EMD array but is generated
  postsynaptically.
* The compartmental model reproduces the measured responses with just **32** EMDs feeding **4**
  dendritic compartmental regions of 31-70 x 10^-6 cm^2 each, using weakly tuned EMDs (Eexc = +40
  mV, Einh = -30 mV); strongly tuned EMDs (Eexc = +24 mV, Einh = -13 mV) also fit the control data
  but fail to reproduce PTX behaviour, falsifying the DS-already-at-EMD hypothesis.
* The large-field saturation level of the response differs for **72 deg/s versus 360 deg/s** pattern
  velocities, reproducing the classical gain-control phenomenon from the same passive dendritic
  machinery, with no additional feedback or adaptation required.
* The isopotential reduction V = (Ee ge + Ei gi) / (ge + gi + gleak) shows analytically that the
  saturating membrane potential is set by **Ee (1 - c) / (1 + c)** with c = gi/ge, i.e. purely by
  the opponent synaptic ratio — a result that survives the transition to the full reconstructed
  morphology.
* After PTX, gain control is **abolished**: the response grows monotonically with stimulus size
  instead of saturating, linking gain control mechanistically to inhibitory opponent input on the
  dendrite.

## Innovations

### First Passive Compartmental LPTC Model Grounded in 3D Reconstruction

Although earlier LPTC studies (Borst and Haag, 1996) used sphere-and-cable approximations, Single et
al. (1997) couple a three-dimensionally reconstructed VS-cell morphology to retinotopically
distributed conductance-based EMD inputs. This made dendritic geometry an explicit component of the
direction-selectivity computation and set the template for all subsequent morphology-aware LPTC
modelling (including the explicit morphology-manipulation studies in the HS-cell literature that
followed).

### Opponent Dendritic Shunting as the Mechanism of Direction Selectivity

The paper establishes the now-canonical opponent-conductance account of fly-LPTC direction
selectivity: weakly tuned EMDs push the dendrite toward a mixed reversal potential whose sign is set
by the excitation-to-inhibition ratio, and the passive dendrite performs the subtraction. This
differed sharply from contemporary vertebrate models that located direction selectivity in
starburst-amacrine-like presynaptic asymmetries.

### Unified Mechanism for Direction Selectivity and Gain Control

A single pair of opponent conductance-based inputs simultaneously explains (i) direction
selectivity, (ii) size-dependent response saturation, and (iii) velocity-dependent saturation level.
The analytical reduction makes this concrete: c = gi/ge is a cosine ratio of a velocity- dependent
argument. Gain control thus needs no separate biophysical mechanism.

### Pharmacological Dissociation of EMD Tuning from Cell Tuning

By showing that PTX flips null-direction responses from hyperpolarization to depolarization, the
authors provide the first direct experimental demonstration that the presynaptic EMDs are only
weakly direction-tuned, and that the sharp direction selectivity of the tangential cell is a
postsynaptic-dendritic product.

## Datasets

This is a biological and computational paper; no shareable datasets are published. Experimental data
consist of:

* Intracellular VS-cell recordings (n = 4) and CH-cell recordings (n = 3) in Calliphora
  erythrocephala.
* Extracellular H1-neuron spike recordings (multi-hour, for PTX gain-control experiments).
* One three-dimensionally reconstructed VS-cell morphology (cobalt stain, reconstructed by the
  authors); morphology is described but not released with the paper. Later LPTC reconstructions in
  public repositories (e.g. NeuroMorpho.Org) descend from this line of work.

No public-domain software or data release is associated with the paper; simulations were run in
Nemosys, an in-house academic simulator pre-dating the NEURON release cycle relevant to this era.

## Main Ideas

* Dendritic direction selectivity in fly LPTCs is generated postsynaptically by opponent
  excitatory-inhibitory conductances on a passive dendrite; it is not inherited directly from the
  EMD array. Any morphology-manipulation experiment in LPTCs must preserve the opponent synaptic
  architecture to remain meaningful.
* A reconstructed passive compartmental model with four dendritic regions and 32 retinotopic EMD
  inputs is already sufficient to reproduce both direction selectivity and size-velocity gain
  control — active conductances are not required to account for these behaviours, which sets the
  null model for subsequent HS-VS morphology studies.
* Gain control and direction selectivity share a single mechanism: the ratio c = gi/ge of opponent
  conductances. Any morphological manipulation that changes the effective spatial distribution or
  coupling of excitation versus inhibition is expected to alter DSI and gain control in a coupled,
  predictable way.
* The isopotential analytical reduction (V as a function of Ee, Ei, ge, gi, gleak) provides a clean
  quantitative benchmark against which full-morphology simulations can be compared, useful for
  interpreting DSI-vs-morphology regressions in later work.
* PTX as a knockout of the inhibitory arm is a highly informative perturbation for computational
  replication: any candidate model that matches control responses but not PTX responses is
  falsified. This is directly applicable when validating LPTC models built on modern
  reconstructions.

## Summary

Single, Haag, and Borst (1997) address one of the oldest questions in invertebrate visual
neuroscience: where, along the chain from photoreceptor to wide-field motion-sensitive cell, is
direction selectivity generated? The prevailing assumption had been that the elementary motion
detectors (EMDs) feeding lobula plate tangential cells were themselves strongly direction-tuned and
that the large LPTC dendrite served primarily as a spatial integrator. The authors set out to test
this assumption directly by combining pharmacology with a biophysically grounded compartmental model
of a reconstructed VS-cell from the blowfly Calliphora erythrocephala.

They use picrotoxinin to block GABAergic inhibition in vivo while recording intracellularly from VS-
and CH-cells and extracellularly from the H1 neuron. In parallel, they build a passive compartmental
model (Rm = 2 kOhm.cm^2, Ri = 40 Ohm.cm, Cm = 0.8 uF/cm^2) in which 32 opponent
excitatory-inhibitory EMD synapses are distributed over four dendritic regions along the main
dendrite. An isopotential reduction yields the closed-form saturation expression Ee (1 - c) / (1 +
c), with c = gi/ge a velocity-dependent opponent ratio, clarifying how a single synaptic machinery
can underlie two ostensibly distinct phenomena.

The key findings are that (i) motion-induced input resistance drops by about 13-14 percent in both
directions under control, implying simultaneous excitatory-inhibitory activation; (ii) PTX reduces
this change to less than 50 percent (null) and about 60 percent (preferred) of control and flips
null-direction responses from hyperpolarization to depolarization, revealing that the underlying
EMDs are only weakly directionally tuned; and (iii) the passive compartmental model, with weakly
tuned EMDs, quantitatively reproduces the classical size- and velocity-dependent saturation ("gain
control"), which is abolished once inhibition is blocked. Direction selectivity and gain control
therefore share a single dendritic mechanism.

For this project's literature survey on how morphology shapes direction selectivity via
computational modeling, Single et al. (1997) is the foundational LPTC entry: it is the first
reconstructed-morphology compartmental model of a fly tangential cell, it fixes the passive-
dendrite "null model" against which morphology-manipulation experiments must be read, and it
establishes the opponent-conductance mechanism that any subsequent morphology-to-DSI regression in
the HS-VS literature inherits. The paper's main limitation for our purposes is that dendritic
morphology is held fixed — it is a same-morphology, varied-synapse study — so it sets the stage for,
rather than directly implements, explicit morphology-variation experiments on DSI. It is
invertebrate (fly, Calliphora erythrocephala), a flag to bear in mind when generalizing to
vertebrate retinal-ganglion or cortical DS models.
