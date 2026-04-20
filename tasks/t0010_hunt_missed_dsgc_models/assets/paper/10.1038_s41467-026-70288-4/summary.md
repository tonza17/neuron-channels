---
spec_version: "3"
paper_id: "10.1038_s41467-026-70288-4"
citation_key: "PolegPolsky2026"
summarized_by_task: "t0010_hunt_missed_dsgc_models"
date_summarized: "2026-04-20"
---

# Machine learning discovers numerous new computational principles underlying direction selectivity in the retina

## Metadata

* **File**: `files/polegpolsky_2026_ml-motion-primitives.pdf`
* **Published**: 2026 (Nature Communications)
* **Authors**: Alon Poleg-Polsky (US)
* **Venue**: Nature Communications (journal)
* **DOI**: `10.1038/s41467-026-70288-4`
* **Companion code**: https://github.com/PolegPolskyLab/DS-mechanisms

## Abstract

Direction selectivity is a canonical example of neural computation in the retina, yet the full
repertoire of biophysical mechanisms that can produce it remains unclear. Here, a machine
learning pipeline explores an enormous space of compartmental models of a 352-segment
direction-selective ganglion cell (DSGC) receiving bipolar-cell inputs with varying spatial
offsets, weights, kinetics, and dendritic biophysics. The search discovers multiple novel
computational primitives that each produce robust direction selectivity, including velocity-
dependent coincidence detection, distance-graded delay lines, and NMDA-mediated
multiplicative gating. These primitives complement - rather than replace - the classical
starburst-amacrine-cell-based inhibitory mechanism, suggesting the retinal DS circuit relies
on a richer set of mechanisms than previously appreciated.

## Overview

This paper uses a large-scale machine-learning parameter search to enumerate biophysical
compartmental-model configurations of a single DSGC that produce robust direction selectivity.
Rather than hand-designing mechanisms, the author instantiates a 352-segment biophysical
model in NEURON with a large parameter space (synaptic weights, kinetics, NMDA presence,
voltage-gated channel densities, bipolar-cell input offsets and timing), generates thousands
of candidates, evaluates their DSI under standardised moving-bar stimuli, and mines the
parameter clusters that score well.

The analysis reveals that multiple qualitatively distinct biophysical configurations can
produce high DSI, most of which do not depend on SAC-style null-direction inhibition. Instead,
the model discovers that the DSGC itself can implement direction selectivity via (i)
velocity-dependent coincidence detection on dendrites, (ii) distance-graded delay lines created
by passive dendritic propagation, (iii) NMDA-mediated multiplicative gating, and several
hybrid combinations. Poleg-Polsky argues these primitives are anatomically plausible given
existing connectomic constraints and that the DSGC dendrite is a richer computational
substrate than previously appreciated.

For the t0010 task, this paper is an important candidate because it (i) is published by the
same senior author as the project canonical Poleg-Polsky and Diamond 2016 model already
ported by t0008, (ii) ships a public compartmental DSGC model in NEURON + Python with all
parameter files needed to reproduce the ML-discovered configurations, and (iii) introduces
novel direction-selectivity mechanisms that our project input-pattern experiments can directly
test. The main porting risk is the missing LICENSE file in the GitHub repo.

## Architecture, Models and Methods

Model: a 352-segment compartmental model of a mouse ON-OFF DSGC implemented in NEURON 8.2
with Python drivers. The dendritic morphology is taken from published DSGC reconstructions
and discretised to meet the space-constant criterion. Passive parameters (Rm, Cm, Ra) are
fitted to match published physiology.

Active biophysics include classical Hodgkin-Huxley sodium and potassium, an A-type potassium
channel on distal dendrites, and NMDA receptors at excitatory synapses. The density and
distribution of each channel are parameters in the ML search.

Synaptic inputs: bipolar-cell excitation delivered at dendritic sites with tunable spatial
offsets, weights, rise/decay kinetics, and AMPA-to-NMDA ratio. An optional SAC-derived
inhibitory conductance is present but can be scaled to zero to test whether SACs are
required.

Stimulus: moving bars or spots at 12 directions across a grid of velocities. Evaluation is
direction-selectivity index (DSI) computed from spike rates (or somatic peak voltage in
subthreshold regimes).

Search pipeline: a machine-learning outer loop (the repository README describes gradient-free
optimisation + surrogate-model-assisted search) explores the joint parameter space. Tens of
thousands of configurations are simulated; candidates with DSI > threshold are clustered to
identify distinct biophysical strategies. Each cluster is post-hoc dissected to determine the
causal mechanism (e.g., ablating NMDA vs. ablating A-type potassium).

## Results

* Multiple qualitatively distinct mechanisms, not just SAC-based inhibition, can produce
  DSI > 0.5 in the 352-segment DSGC model.
* Velocity-dependent coincidence detection on dendrites produces DSI that peaks at a
  characteristic preferred velocity set by dendritic length and membrane time constant.
* Distance-graded delay lines from passive dendritic propagation produce DSI even with
  symmetric bipolar-cell kinetics and no SAC input.
* NMDA-mediated multiplicative gating amplifies preferred-direction responses while
  suppressing null-direction responses, boosting DSI substantially compared to AMPA-only
  inputs.
* Hybrid configurations that combine dendritic mechanisms with SAC-style inhibition achieve
  the highest DSI, approaching published experimental values.
* Ablation analyses confirm each primitive is causally responsible for DSI in its own
  cluster, and the mechanisms are largely independent.

*Specific quantitative DSI values and velocity thresholds are available in the PDF (which is
downloaded) but are not reproduced here; see `files/polegpolsky_2026_ml-motion-primitives.pdf`
for exact numbers.*

## Innovations

### ML-Driven Enumeration of DS Mechanisms

First systematic machine-learning search of compartmental-model parameter space to enumerate
biophysical primitives that produce direction selectivity in a single DSGC.

### Dendrite-Intrinsic DS Primitives

Identifies multiple dendrite-intrinsic mechanisms (coincidence detection, delay lines,
NMDA multiplicative gating) that produce DSI without requiring SAC inhibition - challenging
the long-held assumption that SAC is the dominant source of DSGC direction selectivity.

### Cluster-Based Mechanism Discovery

Introduces a methodology of clustering successful parameter sets and dissecting each cluster
via targeted ablations - a general approach for discovering computational primitives in
biophysical neuron models.

## Datasets

No new experimental datasets are introduced. The model uses a previously published
reconstructed DSGC morphology (cited in the Methods section; exact ID in PDF). Simulated
data (DSI scores per parameter configuration) are released in the companion GitHub
repository as CSVs.

## Main Ideas

* The DSGC dendrite is a **computationally rich substrate** that can implement direction
  selectivity via multiple independent mechanisms, not just via inherited SAC inhibition.
* Any t0010 port of this model should expose **bipolar-cell input offsets, kinetics, NMDA
  strength, and A-type potassium density** as tunable knobs, matching the original ML
  search axes.
* The published candidate configurations (one per discovered mechanism) are themselves a
  useful library - each produces a distinct tuning curve shape, giving our project a
  diverse test set of DSGC behaviours.
* The missing LICENSE on the GitHub repo is a **porting risk**: the code cannot be
  redistributed inside the project library asset unless permission is obtained or the
  author publishes under an explicit licence.

## Summary

Poleg-Polsky uses a machine-learning parameter search over a 352-segment biophysical model
of a mouse ON-OFF DSGC to enumerate mechanisms that can produce direction selectivity. The
search space includes bipolar-cell input geometry, synaptic kinetics, NMDA receptor
placement and strength, dendritic voltage-gated channel densities, and the presence or
absence of SAC-derived inhibition. Thousands of candidate configurations are simulated under
standardised moving-bar stimuli and scored on DSI.

The search reveals that many qualitatively different mechanisms can produce robust direction
selectivity. Dendrite-intrinsic primitives - velocity-dependent coincidence detection,
distance-graded passive delay lines, NMDA-mediated multiplicative gating - are each
sufficient on their own. Hybrid configurations that combine these primitives with
SAC-derived inhibition match experimental DSI most closely. Targeted ablations confirm each
primitive is causally responsible for DSI within its cluster.

The paper challenges the textbook view that starburst amacrine cells are the dominant
substrate of DSGC direction selectivity. Instead, it argues the DSGC dendrite itself is a
richer computational organ capable of producing DS via multiple biophysically plausible
strategies, and that the retinal circuit likely exploits several of them in parallel.

For t0010_hunt_missed_dsgc_models, this paper is a high-priority candidate. The companion
code (`PolegPolskyLab/DS-mechanisms`) provides a NEURON + Python 352-segment DSGC model
exposing exactly the parameters our project is interested in probing - bipolar-cell input
structure, kinetics, NMDA strength, and dendritic biophysics. The ML-discovered
configurations give us a library of distinct tuning-curve shapes to include in comparative
analyses. The primary porting risk is the absent LICENSE file; a licence clarification
intervention or fork-under-MIT may be required before the code can be redistributed.
