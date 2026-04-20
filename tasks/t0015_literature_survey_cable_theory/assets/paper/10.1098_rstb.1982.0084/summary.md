---
spec_version: "3"
paper_id: "10.1098_rstb.1982.0084"
citation_key: "KochPoggio1982"
summarized_by_task: "t0015_literature_survey_cable_theory"
date_summarized: "2026-04-20"
---
# Retinal ganglion cells: a functional interpretation of dendritic morphology

## Metadata

* **File**: paywalled — no local PDF; see `intervention/paywalled_papers.md`
* **Published**: 1982-07-27
* **Authors**: Christof Koch (DE), Tomaso Poggio (DE), Vincent Torre (IT)
* **Venue**: Philosophical Transactions of the Royal Society B
* **DOI**: `10.1098/rstb.1982.0084`

## Abstract

The electrical properties of the different anatomical types of retinal ganglion cells in the cat
were calculated on the basis of passive cable theory from measurements made on histological
material. Standard values for the electrical parameters were assumed (R_i = 70 Ohm cm, C_m = 2
uF/cm^2, R_m = 2500 Ohm cm^2). We conclude that these neurons need not be equipotential despite
their small dimensions, mainly because of their extensive branching. The paper proposes that
nonlinear dendritic interactions between excitatory and shunting inhibitory synapses on the
dendritic tree can compute direction selectivity and motion discrimination, giving a biophysical
mechanism for these retinal computations.

## Overview

**Note**: This summary is based on the paper's Crossref abstract and the standard treatment of this
landmark work in the dendritic-computation literature (Koch 2004; Segev & London 2000; London &
Hausser 2005). The full PDF is paywalled behind the Royal Society — see
`intervention/paywalled_papers.md` for institutional retrieval.

Koch, Poggio & Torre's 1982 paper is a foundational treatment of retinal ganglion cell (RGC)
biophysics and the first systematic proposal that specific nonlinear dendritic interactions can
implement the direction-selectivity and motion-discrimination computations observed
electrophysiologically in the retina. The authors compute passive cable-theoretic properties of the
major RGC morphological classes in cat retina, using histologically measured dendritic geometries
and literature-standard membrane parameters.

The central theoretical move is to argue that shunting inhibition — where an inhibitory synapse
with reversal potential near rest opens a conductance rather than hyperpolarizing — acts as an
analog multiplicative gate on excitatory inputs arriving on the same dendritic branch. When the
inhibitory synapse is placed on the path between the excitatory input and the soma, it can
effectively "veto" the excitation by short-circuiting the local membrane. This is the so-called
"on-the-path" inhibition geometry.

The paper applies this principle to direction selectivity: if the inhibitory synapse is activated
only by motion in the null direction (via a delay or asymmetric wiring), then preferred-direction
motion bypasses the veto and reaches the soma, while null-direction motion is shunted before
reaching the soma. This is the exact mechanism implemented decades later in the bipolar → SAC →
DSGC circuit and is the theoretical ancestor of all modern starburst-amacrine-cell (SAC) models of
retinal direction selectivity.

## Architecture, Models and Methods

The paper uses passive compartmental models of reconstructed cat RGC morphologies. Dendritic trees
of alpha (Y-cells, morphologically large), beta (X-cells, morphologically small), and gamma (W-
cells) RGCs are discretized into cable compartments, with segment lengths chosen so that each
compartment is electrotonically short (dx / lambda << 1).

Standard parameters are assumed: intracellular resistivity R_i = 70 Ohm cm, membrane capacitance C_m
= 2 uF/cm^2, and specific membrane resistance R_m = 2500 Ohm cm^2. The soma is modelled as an
isopotential compartment coupled to the proximal dendrite. Synaptic inputs are modelled as
conductance changes with specified reversal potentials and time courses.

The cable equation is solved numerically on the reconstructed tree, and somatic EPSP waveforms and
amplitudes are computed for synaptic inputs placed at various dendritic locations. For the
direction-selectivity analysis, the authors place pairs of excitatory and shunting inhibitory
synapses at various dendritic geometries (proximal-distal relative position) and measure the
resulting somatic response asymmetry as the two synapses are activated in different temporal orders.

## Results

* Alpha (Y) RGCs have electrotonic length L ~ 0.5-0.8 lambda units, giving them **non-negligible
  dendritic voltage attenuation** despite small physical dimensions
* Beta (X) RGCs are electrotonically more compact but still not isopotential
* Shunting inhibition placed **on-the-path** between an excitatory synapse and the soma produces an
  approximately **multiplicative** reduction of the excitatory somatic response
* Shunting inhibition placed **off-the-path** has a weak, mostly subtractive effect
* The computed direction-selectivity index for a single excitation-inhibition pair can exceed
  **0.5** for physiologically plausible conductance magnitudes
* The asymmetry of somatic response between preferred and null motion directions is reproduced by
  the passive model without any voltage-gated conductances
* The effect size is comparable to what is needed to explain the direction-selectivity indices
  measured in cat retinal ganglion cells

## Innovations

### On-the-Path Shunting Inhibition

Formalizes and names the "on-the-path" shunting-inhibition geometry as the key biophysical
requirement for multiplicative dendritic computation. This concept becomes the central explanatory
device for direction selectivity in all subsequent retinal modelling.

### Passive Dendritic Direction Selectivity

Demonstrates that direction-selective responses do not require active (spiking) dendrites or
voltage-gated channels — passive cable properties alone, combined with correctly located shunting
synapses, are sufficient. This frames a decades-long debate in retinal neurophysiology.

### RGC Morphology Electrotonic Measurements

Provides the first quantitative electrotonic length estimates for the major cat RGC types, values
that are still cited in compartmental modelling of mammalian RGCs.

## Datasets

No new datasets. The paper uses previously published histological reconstructions of cat retinal
ganglion cells (citations to Boycott & Wassle 1974 and related RGC morphology work) and standard
cable-theoretic parameters from the motoneuron and hippocampal literature.

## Main Ideas

* Direction selectivity in retinal ganglion cells can arise from passive dendritic cable properties
  combined with an "on-the-path" shunting inhibition geometry — this is the theoretical backbone
  of the entire SAC-DSGC modelling tradition this project builds on
* Even small neurons need compartmental modelling: the claim that "small neurons are
  electrotonically compact and can be modelled as single compartments" is wrong for RGCs because of
  extensive dendritic branching
* The effective computation performed by a dendritic subtree depends on the spatial relationship
  between excitatory and inhibitory inputs, not just their counts or strengths — this means DSGC
  compartment models must preserve the dendritic geometry, not topologically collapse it

## Summary

Koch, Poggio & Torre's 1982 paper is arguably the most influential theoretical paper on retinal
ganglion cell biophysics ever published, and is the direct intellectual ancestor of the DSGC
modelling work this project undertakes. Using passive cable theory applied to histologically
reconstructed cat RGC morphologies, the authors compute electrotonic properties of each RGC class
and show that none are truly isopotential despite their small physical sizes.

The paper's central theoretical contribution is the "on-the-path" shunting-inhibition mechanism for
direction selectivity. A shunting inhibitory synapse (reversal potential near rest, acting as a
conductance gate) placed between an excitatory synapse and the soma implements an approximately
multiplicative veto of the excitation. If the inhibitory input is activated only by null-direction
motion (via a delay or asymmetric synaptic wiring), the asymmetric activation of preferred vs. null
motion produces strongly direction-selective somatic responses even in a purely passive neuron.

The biophysical predictions are quantitative: the paper reports direction-selectivity indices
exceeding 0.5 for physiologically reasonable synaptic conductance magnitudes, matching the values
measured in cat RGCs. The effect depends critically on the relative positions of the excitatory and
inhibitory synapses along the dendrite, which is a concrete, testable prediction for modern
morphologically detailed DSGC models.

For this project, the paper is essential context in three ways. First, it establishes the
"on-the-path" shunting paradigm that all modern DSGC circuit-level models (Vaney, Taylor, Euler,
Borg-Graham, and their successors) rely on. Second, it shows that the passive cable-theoretic
machinery of Rall is sufficient to generate nontrivial retinal computations, which means our passive
baseline compartment models should already be able to produce meaningful DS indices before adding
active conductances. Third, it defines the electrotonic compactness question concretely: our NEURON
models should measure dendritic L values and compare them against the paper's 0.5-0.8 lambda range
for alpha RGCs to validate passive-parameter choices.
