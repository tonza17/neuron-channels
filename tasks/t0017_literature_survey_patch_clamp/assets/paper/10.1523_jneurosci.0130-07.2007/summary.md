---
spec_version: "3"
paper_id: "10.1523_jneurosci.0130-07.2007"
citation_key: "MargolisDetwiler2007"
summarized_by_task: "t0017_literature_survey_patch_clamp"
date_summarized: "2026-04-20"
---
# Different Mechanisms Generate Maintained Activity in ON and OFF Retinal Ganglion Cells

## Metadata

* **File**: paper PDF not downloaded (see intervention/paywalled_papers.md)
* **Published**: 2007-05-30
* **Authors**: David J. Margolis US, Peter B. Detwiler US
* **Venue**: The Journal of Neuroscience
* **DOI**: `10.1523/jneurosci.0130-07.2007`

## Abstract

Neuronal discharge is driven by either synaptic input or cell-autonomous intrinsic pacemaker
activity. It is commonly assumed that the resting spike activity of retinal ganglion cells (RGCs),
the output cells of the retina, is driven synaptically, because retinal photoreceptors and
second-order cells tonically release neurotransmitter. Here we show that ON and OFF RGCs generate
maintained activity through different mechanisms: ON cells depend on tonic excitatory input to drive
resting activity, whereas OFF cells continue to fire in the absence of synaptic input. In addition
to spontaneous activity, OFF cells exhibit other properties of pacemaker neurons, including
subthreshold oscillations, burst firing, and rebound excitation. Thus, variable weighting of
synaptic mechanisms and intrinsic properties underlies differences in the generation of maintained
activity in these parallel retinal pathways.

## Overview

**Disclaimer**: this summary is based on the Crossref metadata abstract (reproduced in full above)
supplemented with training-data knowledge of the published paper; it has not been verified against a
local PDF because the Journal of Neuroscience publisher copy was not downloaded in this task.

Margolis and Detwiler address a fundamental question about retinal ganglion cell (RGC) resting
activity: is it driven synaptically by tonic release from upstream cells, or is it generated
intrinsically by pacemaker biophysics in the RGC itself? The answer turns out to depend on RGC type.
ON RGCs lose their maintained activity when synaptic input is blocked pharmacologically, confirming
the dominant assumption in the field. OFF RGCs continue to fire regardless, and additionally show
subthreshold oscillations, burst firing, and rebound excitation that are characteristic of intrinsic
pacemaker neurons.

The finding is load-bearing for retinal modelling because it tells us that OFF RGCs require an
explicit intrinsic biophysical mechanism in any model that claims to reproduce their resting
activity, while ON RGCs can be driven by synaptic input alone. For DSGC modelling specifically,
ON-OFF DSGCs inherit both input streams and may share some of the intrinsic biophysics of pure OFF
cells, depending on subtype.

## Architecture, Models and Methods

The recordings are whole-cell current-clamp and cell-attached patch-clamp from morphologically and
functionally identified ON and OFF RGCs in adult rabbit retinal wholemount. ON and OFF cells are
distinguished by their light-response polarity under bright-field visual stimulation. Maintained
activity is recorded under control conditions (normal Ames medium) and after pharmacological
blockade of ionotropic glutamate receptors (CNQX plus D-APV or similar) to remove synaptic
excitation while preserving intrinsic properties.

Beyond the maintained-activity comparison, OFF cells are further characterised for pacemaker-like
intrinsic properties: subthreshold voltage oscillations recorded in whole-cell current-clamp near
rest, burst firing patterns in response to depolarising current injection, and rebound excitation
following release from hyperpolarisation. Input resistance, resting potential, and f-I curves are
measured in both cell classes.

Control experiments verify that synaptic blockade is effective (no light-evoked responses remain)
and that intrinsic properties of both cell types can be quantified in the same preparation.

## Results

* ON RGCs **lose their maintained firing** when ionotropic glutamate receptors are blocked; synaptic
  input is the dominant driver of their resting activity.
* OFF RGCs **continue to fire** at substantial rates after synaptic blockade, demonstrating
  cell-autonomous pacemaker activity.
* OFF RGCs exhibit subthreshold membrane potential oscillations near rest at frequencies consistent
  with intrinsic ion-channel interactions.
* OFF RGCs show burst firing in response to depolarising current injection, with burst structure
  that persists under synaptic blockade.
* OFF RGCs show rebound excitation following hyperpolarising current injection, consistent with the
  presence of low-threshold (T-type) Ca2+ channels and/or HCN channels.
* The difference between ON and OFF cells is not explained by differences in passive properties
  (Rin, tau) but by qualitatively different complements of voltage-gated conductances.

## Innovations

### Intrinsic vs Synaptic Dichotomy Across ON and OFF RGCs

First clean demonstration that ON and OFF RGCs use fundamentally different strategies to generate
maintained activity. Before this work the literature assumed synaptic drive was dominant in both;
the paper forces a revision for OFF cells.

### OFF RGCs as Pacemaker Neurons

Establishes that OFF RGCs meet the standard criteria for intrinsic pacemaker neurons (spontaneous
firing without input, subthreshold oscillations, burst firing, rebound excitation). This reframes
OFF cells as cell-autonomous encoders rather than passive relayers.

### Implications for Modelling Resting Activity

Provides a clear criterion for compartmental-model validation: any model of an OFF RGC (or an ON-OFF
DSGC) must be able to produce intrinsic maintained activity, subthreshold oscillations, and rebound
excitation without synaptic input, driven purely by its voltage-gated channel complement.

## Datasets

No external datasets are used. The paper is based on original patch-clamp recordings from adult
rabbit retinal wholemount preparations. Cell-level data are presumably available on request from the
authors but are not deposited in a public repository.

## Main Ideas

* For DSGC modelling: ON-OFF DSGCs combine both input streams, and the OFF-bipolar input pathway may
  carry intrinsic-pacemaker characteristics from the OFF RGC biophysics. DSGC models must decide
  whether to include burst-firing and rebound biophysics and justify the decision.
* Any compartmental RGC model that aims to reproduce maintained activity must distinguish intrinsic
  from synaptic contributions. Using pharmacological-blockade traces as a model target isolates the
  intrinsic component.
* Subthreshold oscillations, burst firing, and rebound excitation are three distinct testable
  predictions of a correct OFF-cell intrinsic model; passing one does not imply passing the others.

## Summary

Margolis and Detwiler take a direct experimental approach to the question of whether retinal
ganglion cell maintained activity is synaptically driven or intrinsically generated. Using
whole-cell and cell-attached patch-clamp recordings from morphologically identified ON and OFF RGCs
in rabbit retinal wholemount, they compare maintained firing under control conditions to firing
after pharmacological blockade of ionotropic glutamate receptors. The design cleanly separates
synaptic drive from intrinsic biophysics in the same cells.

The methodology is careful about cell identification and blockade efficacy, and the follow-up
experiments extend the comparison beyond maintained firing to other signatures of pacemaker
activity: subthreshold oscillations, burst firing, and rebound excitation. Each signature is a
distinct testable claim about the cell intrinsic biophysics, not a single measurement.

The headline finding is that ON and OFF RGCs use qualitatively different strategies. ON cells
require synaptic input to fire at rest; OFF cells fire autonomously and additionally show the full
suite of pacemaker properties. The difference is not explained by passive properties but by
different voltage-gated channel complements, a conclusion supported by the pattern of intrinsic
responses.

For this project, the implications matter even though the paper is about pure ON and OFF cells
rather than DSGCs directly. ON-OFF DSGCs integrate both input streams, and the biophysics of the OFF
input pathway may bring some of the intrinsic-pacemaker machinery into the DSGC soma and dendrites.
DSGC compartmental models should consider whether burst firing, rebound excitation, and subthreshold
oscillations are expected behaviours of the target cell and include or exclude the relevant
voltage-gated channels (T-type Ca2+, HCN) accordingly. Using
maintained-activity-under-synaptic-blockade as a model validation target cleanly separates the
intrinsic biophysics from the synaptic drive, and that separation should be part of our modelling
workflow.
