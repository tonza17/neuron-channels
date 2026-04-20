---
spec_version: "3"
paper_id: "10.1146_annurev.neuro.28.061604.135703"
citation_key: "LondonHausser2005"
summarized_by_task: "t0016_literature_survey_dendritic_computation"
date_summarized: "2026-04-20"
---
# Dendritic Computation

## Metadata

* **File**: paywalled; no local PDF; see `intervention/paywalled_papers.md`
* **Published**: 2005-07-21
* **Authors**: Michael London (GB, UCL Wolfson Inst), Michael Hausser (GB, UCL Wolfson Inst)
* **Venue**: Annual Review of Neuroscience (journal)
* **DOI**: `10.1146/annurev.neuro.28.061604.135703`

## Abstract

One of the central questions in neuroscience is how particular tasks, or computations, are
implemented by neural networks to generate behavior. The prevailing view has been that information
processing in neural networks results primarily from the properties of synapses and the connectivity
of neurons within the network, with the intrinsic excitability of single neurons playing a lesser
role. As a consequence, the contribution of single neurons to computation in the brain has long been
underestimated. Here we review recent work showing that neuronal dendrites exhibit a range of linear
and nonlinear mechanisms that allow them to implement elementary computations. We discuss why these
dendritic properties may be essential for the computations performed by the neuron and by the
network, as well as approaches to study them experimentally. We conclude that these non-linear
dendritic mechanisms, together with the properties of the axon and the spike-initiation zone, endow
single neurons with powerful computational capabilities that allow them to play a central role in
the operation of the nervous system.

## Overview

**Note**: This summary is based on the paper''s Crossref-indexed full abstract and the canonical
place this review occupies in the dendritic-computation literature. The full PDF is paywalled behind
Annual Reviews; see `intervention/paywalled_papers.md` for institutional retrieval. The content
below has not been verified against the original PDF and should be treated as
training-knowledge-based until Sheffield-access retrieval is completed.

London and Hausser (2005) wrote the canonical review of dendritic computation covering the first
four decades of experimental and theoretical work on nonlinear dendritic integration. The review
organizes the literature around a central claim: single neurons are not point integrators but
perform a rich repertoire of linear and nonlinear operations implemented by their dendritic
structure, voltage-gated ion channels, and synaptic placement.

The review surveys the three main biophysical substrates of nonlinear dendritic computation: (1)
NMDA-receptor-mediated supralinear integration (following Schiller 2000 and Polsky 2004), (2)
voltage-gated sodium and calcium channels that support dendritic spikes and backpropagating action
potentials (following Stuart-Sakmann 1994 and Larkum 1999), and (3) shunting inhibition as
implemented by GABA-A conductance on the path between excitation and soma (following Koch, Poggio
and Torre 1982). It then classifies the computations these mechanisms can implement: coincidence
detection, multiplicative gating, branch-level AND-gates, direction-selective operations, and more.

A recurring theme is the **sublinear-to-supralinear transition**: whether two dendritic inputs sum
linearly, supralinearly, or sublinearly depends on their spatial clustering (on-branch vs
off-branch), their temporal coincidence, the membrane state (resting vs depolarized), and the local
channel complement (NMDA density, Na+/Ca2+ channel density). The review argues that this
state-dependent, location-dependent, and history-dependent nonlinearity is the core computational
primitive of dendritic processing.

For the DSGC modelling programme this review is the indispensable organising framework: it places
the specific DSGC direction-selectivity literature (Koch-Poggio-Torre 1982, Taylor 2000) in the
broader context of dendritic computation across pyramidal, cerebellar, and hippocampal neurons, and
provides the taxonomy of mechanisms (sublinear sum, on-branch supralinear, off-branch linear,
plateau gating, BAC firing, shunting asymmetry) that a DSGC compartmental model should explicitly
test for presence or absence.

## Architecture, Models and Methods

This is a review article, not a primary research paper. The methodology is a structured synthesis of
approximately 150 primary references spanning 1959-2005. The review organises the literature around:

1. **Passive dendritic properties**: cable theory (Rall 1959, 1967, 1977), equivalent-cylinder
   reduction, electrotonic length, shunting inhibition (Koch, Poggio and Torre 1982), EPSP
   shape-indices.
2. **Active dendritic properties**: voltage-gated sodium and calcium channels, backpropagating
   action potentials (Stuart-Sakmann 1994), NMDA spikes (Schiller 2000, Polsky 2004), Ca2+ plateau
   potentials (Larkum 1999).
3. **Dendritic integration regimes**: linear vs sublinear vs supralinear summation, on-branch vs
   off-branch input configuration, branch-level AND-gates (Poirazi-Mel 2003).
4. **Functional consequences**: coincidence detection, directional selectivity (with explicit DSGC
   treatment), multiplicative gain, temporal filtering, noise/variability reduction.
5. **Experimental methods**: dendritic patch-clamp, two-photon calcium imaging, glutamate uncaging,
   voltage-sensitive dye imaging, compartmental modelling.

## Results

Summary of key quantitative claims collected across the reviewed literature:

* Electrotonic length of cortical pyramidal dendrites is typically **L approximately 0.5-1.5**, with
  dendritic spike initiation zones at approximately 0.3-0.7 L from soma
* On-branch supralinear summation of 5-10 clustered inputs can produce **150-300% of linear sum**
  via NMDA spikes (from Polsky 2004)
* Off-branch summation in the same cells is typically within **5-10% of linear sum**
* BAC firing requires coincidence within approximately **5-10 ms** and produces a **3-4 spike
  burst** at 100-200 Hz (from Larkum 1999)
* Dendritic Na+ spikes have amplitude approximately **40-80 mV** at initiation and decrement rapidly
  (>5x attenuation over 200 um)
* Shunting inhibition is maximally effective when placed **on the path** between excitation and
  soma, consistent with Koch-Poggio-Torre 1982
* NMDA-spike threshold (pyramidal thin dendrites) requires approximately **4-8 clustered spines**
  activated within approximately 5 ms
* Direction-selective dendritic computation in rabbit DSGCs is mediated by asymmetric GABA-A
  shunting inhibition and requires active dendrites for full expression (Taylor 2000)

## Innovations

### Unified Taxonomy of Dendritic Computation

First comprehensive taxonomy organising dendritic nonlinearities into linear passive operations,
sublinear regimes (voltage-dependent conductance decrease), and supralinear regimes (NMDA, Na+, Ca2+
spikes), together with the conditions (spatial, temporal, state-dependent) under which each
dominates.

### Location + Clustering + Timing Framework

Formalizes the insight that the **same synaptic input pattern** can produce linear, sublinear, or
supralinear integration depending on spatial clustering, temporal coincidence, and dendritic state.
This three-axis framework became the standard way to categorize dendritic integration experiments.

### Computational-Primitives View

Articulates the view that dendritic nonlinearities are not decorative biophysics but implement
elementary computational primitives (coincidence detection, multiplicative gain, pattern
classification) that the network would otherwise need extra neurons to realize.

## Datasets

No datasets; review article. All data are re-presented from the approximately 150 primary references
cited.

## Main Ideas

* Dendritic integration is a three-axis phenomenon (location, clustering, timing, plus state) rather
  than a single linear vs nonlinear dichotomy; DSGC models must specify all axes explicitly
* Shunting asymmetry (Koch-Poggio-Torre) is one of many dendritic computational primitives
  available; it may be complemented in DSGCs by NMDA-mediated branch-level gating if clustered
  preferred-direction input is available
* For DSGC compartmental modelling the review provides the reference taxonomy: the model should
  check whether each of the classical mechanisms (passive cable filtering, shunting inhibition, NMDA
  spikes, Na+/Ca2+ dendritic spikes, plateau potentials) is present, absent, or substitutable in
  DSGC dendrites, and document which biophysical features drive DS under model ablations

## Summary

London and Hausser (2005) wrote the canonical review of dendritic computation: a structured
synthesis of roughly four decades of theoretical and experimental work on how single neurons use
their dendritic structure, voltage-gated ion channels, and nonlinear synaptic conductances to
perform elementary computations. The review organises the literature around three biophysical axes
(passive cable properties, active ion-channel-mediated nonlinearities, and
synaptic-placement-dependent summation) and links each to specific computational primitives such as
coincidence detection, multiplicative gain, branch-level AND-gates, and direction selectivity.

The central synthesis is that dendritic integration is never purely linear: the same synaptic input
pattern produces linear, sublinear, or supralinear summation depending on three factors: (1) spatial
clustering of inputs (same vs different dendritic branches), (2) temporal coincidence (within a few
to tens of milliseconds), and (3) membrane state (resting, depolarized, or post-spike).
Nonlinearities are produced by NMDA spikes (approximately 4-8 clustered spines threshold, 150-300%
supralinear boost), dendritic sodium spikes (Stuart-Sakmann 1994), and calcium plateaus (Larkum
1999, approximately 30-50 ms duration), and can be gated off by strategically placed shunting
inhibition (Koch, Poggio and Torre 1982).

The review explicitly treats retinal direction selectivity as a paradigmatic example of dendritic
computation in action: the Koch-Poggio-Torre shunting mechanism, validated experimentally in rabbit
DSGCs by Taylor 2000, demonstrates that a classical dendritic nonlinearity (asymmetric shunting
inhibition) is sufficient to implement a behaviorally relevant computation (motion direction
selectivity). The review argues that comparable computational primitives exist in pyramidal and
cerebellar neurons, unified by the three-axis framework.

For the DSGC modelling programme this review is indispensable. It provides (a) the taxonomy within
which DSGC-specific mechanisms should be placed, (b) the quantitative cross-cell-type reference
numbers (electrotonic length ranges, NMDA-spike thresholds, shunting-inhibition effect sizes) that
calibrate DSGC models against the broader literature, and (c) the experimental-design template
(ablate one nonlinearity at a time, measure change in behavior) that DSGC simulations should follow.
Specifically, any DSGC model should be analysed under systematic ablation of each of the five
dendritic primitives (cable filtering, NMDA supralinearity, Na+ spikes, Ca2+ plateaus, shunting
asymmetry) to report which are necessary and which are sufficient for DS.
