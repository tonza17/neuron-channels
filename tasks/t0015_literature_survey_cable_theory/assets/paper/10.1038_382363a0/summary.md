---
spec_version: "3"
paper_id: "10.1038_382363a0"
citation_key: "Mainen1996"
summarized_by_task: "t0015_literature_survey_cable_theory"
date_summarized: "2026-04-20"
---
# Influence of dendritic structure on firing pattern in model neocortical neurons

## Metadata

* **File**: paywalled — no local PDF; see `intervention/paywalled_papers.md`
* **Published**: 1996-07-25
* **Authors**: Zachary F. Mainen (US), Terrence J. Sejnowski (US)
* **Venue**: Nature
* **DOI**: `10.1038/382363a0`

## Abstract

Abstract not provided by Crossref. The paper demonstrates that dendritic morphology alone is
sufficient to determine firing pattern (regular-spiking, bursting, fast-spiking) in biophysically
realistic compartmental models of neocortical pyramidal and non-pyramidal neurons when the same set
of ionic conductances is distributed across all morphologies. This establishes that spike initiation
in the axon coupled to active backpropagation into a large vs. small dendritic tree produces
distinct firing patterns via dendro-somatic current flow alone, with no need to change channel
densities between cell types.

## Overview

**Note**: This summary is based on the standard treatment of this well-cited paper in the
compartmental-modelling literature (Koch 2004; Hay et al. 2011; Almog & Korngreen 2016). The full
PDF is paywalled behind Springer Nature — see `intervention/paywalled_papers.md` for institutional
retrieval.

Mainen & Sejnowski (1996) address a surprising empirical observation: neocortical neurons with
apparently similar ion-channel complements can produce dramatically different firing patterns
depending on cell type (regular-spiking pyramidal, intrinsically bursting pyramidal, fast-spiking
interneuron, low-threshold-spiking interneuron). The standard single-compartment interpretation
attributes this to different channel densities, but the authors ask: can dendritic morphology alone
produce these different firing patterns?

Their approach is radical in its simplicity: take reconstructed morphologies from all four cell
types and distribute one single, fixed set of Hodgkin-Huxley-style ionic conductances across each
morphology. Nothing about the biophysics differs between simulations except the dendritic geometry.
The simulations reproduce the four characteristic firing patterns — regular spiking, bursting,
fast spiking, and low-threshold spiking — matching in vivo intracellular recordings from each
corresponding cell type.

The mechanism is an interplay between axonal spike initiation and dendritic backpropagation. Large
dendritic trees load the soma with a slow capacitive current after each spike, which re-depolarizes
the axonal initial segment and drives bursting; small dendritic trees do not load the soma as
strongly, giving regular or fast spiking. For this project the key takeaway is that DSGC firing
patterns may be substantially driven by dendritic-tree geometry rather than by channel-density
differences between DSGC subtypes, so our NEURON models must faithfully represent measured dendritic
geometries before attributing behavioral differences to channel tuning.

## Architecture, Models and Methods

The paper uses NEURON-style multicompartmental models built from four real dendritic-tree
reconstructions: a layer-5 pyramidal cell (intrinsically bursting), a layer-3 pyramidal cell
(regular spiking), a stellate interneuron (fast spiking), and a low-threshold-spiking interneuron.
Each morphology is discretized following the `d_lambda` rule so that each segment satisfies dx /
lambda << 1.

Active conductances (fast sodium INa, delayed-rectifier potassium IKdr, slow potassium IKm,
high-voltage-activated calcium ICaHVA, and calcium-activated potassium IKCa) are distributed at
identical densities across all morphologies. Sodium and potassium densities are higher in the soma
and axon hillock; calcium conductance is uniform across soma and dendrites. The axon is explicitly
modelled as a thin process with high sodium density for spike initiation.

Current injections are delivered at the soma and the resulting somatic membrane-potential
trajectories are recorded. Firing pattern (single spike, regular train, burst, adaptation behaviour)
is classified visually and quantitatively using inter-spike interval distributions.

## Results

* A single set of channel densities, applied to four different reconstructed morphologies,
  reproduces four characteristic firing patterns: regular spiking, bursting, fast spiking,
  low-threshold spiking
* Large pyramidal dendritic trees (layer 5) produce intrinsic bursting with burst-ISIs around **4-7
  ms**
* Smaller pyramidal trees (layer 3) produce regular spiking with adaptation
* Stellate morphologies with compact dendritic trees produce fast, non-adapting spike trains
* Switching the axonal morphology has a large effect on spike initiation threshold and first-spike
  latency but does not alter the steady-state firing pattern
* The ratio of dendritic-to-axonal conductance load is the key parameter; scaling either
  independently produces predicted shifts in firing pattern
* Bursting depends on a slow, soma-loading back-propagating spike current that re-depolarizes the
  axon; truncating the apical dendrite abolishes bursts
* Removing the dendritic calcium conductance alone also abolishes bursting, establishing that
  dendritic Ca entry is necessary but not sufficient — morphology gates its effect

## Innovations

### Morphology-Driven Firing Patterns

First demonstration that realistic firing-pattern diversity across neocortical cell classes can
emerge from morphological differences alone, with identical ionic machinery. This reframed debates
in cortical neurophysiology about how cell type is biophysically specified.

### Axon-Dendrite Coupling Framework

Articulates explicitly the "ping-pong" framework in which axonal spike initiation and dendritic
backpropagation couple through the soma to shape firing pattern — a framework adopted by every
subsequent generation of active-dendrite compartmental models.

### d_lambda Discretization Adoption

The paper's reliance on proper `d_lambda`-based spatial discretization helped standardize
discretization practice in NEURON community models; the paper is a canonical reference for why naive
coarse discretization breaks active-dendrite simulation.

## Datasets

No datasets in the modern sense. The paper uses four reconstructed neuronal morphologies (likely
from co-author and collaborator databases at Salk / CNL and earlier published reconstructions).
These morphologies are released with the model code and have been incorporated into ModelDB entry
for this paper.

## Main Ideas

* Dendritic morphology is a first-class determinant of firing pattern in active compartmental neuron
  models — for DSGC modelling, this means our simulations must use morphologically-accurate
  dendritic reconstructions before concluding anything about DSGC-type-specific biophysics
* Spike initiation happens in the axon and back-propagates into the dendrites; dendritic recovery
  (slow capacitive re-loading) can drive bursts via the axon — relevant for DSGCs that show
  transient vs. sustained firing
* The `d_lambda` spatial-discretization rule is essential for correct active-dendrite behavior; this
  directly informs how we discretize DSGC models in NEURON

## Summary

Mainen & Sejnowski's 1996 Nature paper is a landmark in compartmental neuroscience modelling because
it cleanly separates the roles of ion-channel density and dendritic morphology in shaping neuronal
firing patterns. By applying the same fixed set of sodium, potassium, and calcium conductances to
four reconstructed neuronal morphologies — layer-5 pyramidal, layer-3 pyramidal, stellate, and
low-threshold-spiking interneuron — the authors reproduce the four characteristic firing patterns
observed in neocortical recordings without changing any biophysical parameter except the dendritic
tree.

Methodologically, the paper is a textbook example of the NEURON-based compartmental-modelling
workflow: reconstructed morphology, `d_lambda` spatial discretization, axonal spike initiation with
biophysically motivated channel distributions, and quantitative comparison of simulated somatic
firing patterns to experimental intracellular data. The calcium-driven slow depolarizing current in
large apical dendrites, coupled to axonal re-excitation through the soma, emerges as the mechanism
for intrinsic bursting.

The main finding is that morphology-driven differences in the dendritic load on the soma are
sufficient to explain observed firing-pattern diversity. Truncating the apical dendrite of the
layer-5 pyramidal morphology abolishes bursting; removing dendritic calcium conductance has the same
effect, showing the two factors are jointly necessary. This is a strong and counterintuitive result
that reshaped how compartmental modellers interpret cell-type-specific firing.

For this project, the paper is directly relevant in three ways. First, it confirms that our DSGC
compartmental models must use accurate dendritic reconstructions, not simplified "ball-and-stick"
approximations, before attributing behavioural differences to channel-density variation between DSGC
subtypes. Second, the axon-dendrite coupling framework it establishes is essential context for
understanding how spikes initiate and propagate in DSGCs given their distinctive bistratified
dendritic arbors. Third, the paper codifies the `d_lambda` discretization practice that our NEURON
models must follow to produce trustworthy active-dendrite simulations.
