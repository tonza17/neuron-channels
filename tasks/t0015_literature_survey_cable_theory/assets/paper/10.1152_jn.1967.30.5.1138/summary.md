---
spec_version: "3"
paper_id: "10.1152_jn.1967.30.5.1138"
citation_key: "Rall1967"
summarized_by_task: "t0015_literature_survey_cable_theory"
date_summarized: "2026-04-20"
---
# Distinguishing theoretical synaptic potentials computed for different soma-dendritic distributions of synaptic input

## Metadata

* **File**: paywalled — no local PDF; see `intervention/paywalled_papers.md`
* **Published**: 1967-09-01
* **Authors**: Wilfrid Rall (US, NIH)
* **Venue**: Journal of Neurophysiology (APS)
* **DOI**: `10.1152/jn.1967.30.5.1138`

## Abstract

Abstract not available in Crossref or OpenAlex public metadata for this 1967 paper. The paper
analytically computes EPSP waveforms at the soma as a function of synaptic input location along the
soma-dendritic axis of a Rall equivalent-cylinder neuron model, and proposes shape-index
measurements (rise time and half-width) as empirical diagnostics of synaptic input location.

## Overview

**Note**: This summary is based on the paper's metadata and well-known treatment of the work in the
cable-theory literature (Rall 1977; Koch 2004; Segev & London 2000). The full PDF is paywalled
behind APS — see `intervention/paywalled_papers.md` for institutional retrieval.

Rall's 1967 paper extends the equivalent-cylinder formalism to ask a simple, empirically important
question: can an experimenter infer the dendritic location of a synaptic input by measuring only the
shape of the resulting EPSP at the soma? Rall computes theoretical EPSP waveforms at the soma for a
range of synaptic input locations along a passive soma-dendritic model, from inputs placed directly
on the soma to inputs placed at increasing electrotonic distances out along the dendritic tree.

The central finding is that the EPSP shape — specifically the ratio of rise time to half-width —
varies systematically and predictably with input location. Somatic inputs produce fast, sharply
peaked EPSPs; distal dendritic inputs produce slower, more rounded EPSPs whose peak is substantially
delayed and broadened by the low-pass-filter action of the intervening dendritic cable. Rall
proposes a two-dimensional "shape index" plot (rise time on one axis, half-width on the other) as a
graphical diagnostic: each dendritic input location traces out a specific curve in shape-index
space.

The paper is foundational for two reasons relevant to this project. First, it establishes that
dendritic cable filtering has experimentally measurable signatures in somatic recordings — an
essential fact for any modelling of retinal ganglion cells where synaptic inputs are distributed
across dendritic arbors. Second, the shape-index methodology became a standard tool for inferring
dendritic input location from experimental intracellular records, and continues to inform how
modellers validate reduced-compartment neuron models against somatic EPSP data.

## Architecture, Models and Methods

Rall uses the equivalent-cylinder reduction of a branched passive dendritic tree, in which all
dendritic branches satisfy the "3/2-power" branching rule and impedance-matching conditions that
allow the full dendritic arbor to be mapped onto a single cylinder of equivalent electrotonic
length. The soma is treated as an isopotential compartment coupled to the proximal end of the
cylinder, and the distal end is sealed.

Synaptic input is modelled as a transient conductance change (alpha function or similar waveform)
with a fixed reversal potential, applied at a specified electrotonic distance from the soma. The
cable equation is solved analytically in the Laplace domain for the resulting somatic voltage
response. The methodology is purely theoretical — no in vitro or in vivo experiments are reported
in the paper itself — but the computed waveforms are compared qualitatively to published
experimental EPSPs from motoneurons.

Key parameters varied in the simulations: electrotonic input location (0 to several length
constants), synaptic conductance time course, and membrane time constant. The derived observables
are EPSP rise time (time from onset to peak) and half-width (total duration at half maximum
amplitude), both measured at the soma.

## Results

* Somatic input produces the fastest EPSP: short rise time, narrow half-width
* Distal dendritic input produces slower EPSPs with rise time and half-width both increasing
  monotonically with electrotonic distance
* The ratio half-width / rise time increases with electrotonic distance, providing a
  distance-independent-ish shape discriminator
* The shape-index (rise time, half-width) plane separates inputs at different locations into
  distinguishable regions
* Peak EPSP amplitude at the soma decreases sharply with electrotonic distance due to cable
  attenuation, independently of the shape changes
* The temporal dispersion of distal inputs is driven primarily by the membrane time constant
  combined with cable filtering, not by any active process

## Innovations

### Shape-Index Diagnostic

Introduces the shape-index plot as a practical tool for inferring synaptic input location from
somatic recordings. This became a standard methodology in cellular neurophysiology.

### Quantitative Linking of Cable Theory to Experiment

Moves equivalent-cylinder theory beyond steady-state impedance and steady-state voltage attenuation
(the focus of Rall's earlier work) into the domain of transient synaptic responses, which is where
most intracellular experimental data lives.

### Compartment-to-Morphology Validation Target

Provides quantitative predictions that any compartmental model of a passive-dendritic neuron must
reproduce — shape-index curves are still used today as a sanity check for reduced-compartment
neuron models.

## Datasets

No datasets. The paper is analytical and presents theoretical waveforms computed from closed-form
solutions of the cable equation on the equivalent-cylinder geometry. Comparison to experimental data
is qualitative and drawn from published motoneuron records cited within the paper.

## Main Ideas

* Dendritic cable filtering produces systematic, measurable distortion of synaptic transients at the
  soma — relevant for interpreting somatic recordings from DSGCs and for validating reduced models
* The shape-index (rise time, half-width) plane is a standard diagnostic for inferring input
  location; DSGC modelling work should report these indices when validating compartment models
  against patch data
* The equivalent-cylinder reduction gives analytical tractability but requires the 3/2-power
  branching rule — real DSGC dendritic morphologies may violate this, so compartmental simulation
  is required for quantitative accuracy

## Summary

Rall's 1967 paper asks whether the shape of a somatic EPSP carries information about where along the
dendritic tree the underlying synaptic input was delivered. Using the equivalent-cylinder formalism
and closed-form solutions of the passive cable equation, Rall computes theoretical EPSP waveforms
for inputs at a range of electrotonic distances from the soma.

The paper's methodological contribution is the shape-index plot: a two-dimensional graph of EPSP
rise time versus half-width in which different input locations trace out distinguishable curves.
Somatic inputs produce fast, narrow EPSPs; distal dendritic inputs produce slower, broader EPSPs
whose temporal profile is dominated by cable low-pass filtering.

The main result is that input location is recoverable from EPSP shape with useful accuracy, provided
the underlying neuron approximately satisfies the equivalent-cylinder assumptions. Rall also reports
the expected dramatic attenuation of distal-input amplitude at the soma, and discusses the interplay
between membrane time constant and cable filtering in shaping the observed waveform.

For the direction-selective retinal ganglion cell (DSGC) modelling work in this project, the paper
is relevant in three ways. First, it establishes that somatically-recorded EPSPs from DSGC patch
experiments can in principle be used to estimate input location, informing how we interpret
experimental data. Second, it defines a standard validation target (shape-index curves) that our
reduced compartment models should reproduce. Third, it warns that the equivalent-cylinder
simplification depends on branching-rule assumptions that real dendritic arbors — including the
starburst amacrine and DSGC arbors we care about — do not satisfy exactly, motivating the use of
full morphological compartmental simulation in NEURON rather than reduced analytical models.
