# Creative Thinking: Morphology and Direction Selectivity

## Objective

This file captures out-of-the-box angles on morphology-to-DS modeling surfaced during the 20-paper
synthesis that do not fit the standard "morphology variable -> mechanism -> DS outcome" taxonomy. It
seeds t0022 (DSGC channel testbed) and t0024 (de Rosenroll 2026 port) with hypotheses the corpus has
left on the table.

## Unconventional Morphology Variables

* Spine density on DSGC distal dendrites. None of the 20 papers sweeps spines; [Sivyer2013] and
  [Schachter2010] treat terminals as smooth cables. Varying t0022 spine density tests whether
  spine-head capacitance shifts dendritic-spike threshold gradients.
* Dendritic varicosities as discrete RC discontinuities. [Morrie2018] and [Vlasits2016] treat them
  as output sites but not geometric compartments; a t0024 sweep separates release-site layout from
  local-cable effects.
* Axon initial segment (AIS) geometry as DS readout. Every corpus paper stops at the soma; AIS
  length and Nav1.6 density plausibly convert subthreshold DSI into output DSI differently across
  morphologies.
* Soma size and soma-dendrite impedance mismatch. [Wu2023] sweeps dendritic but not soma diameter; a
  2x soma-radius sweep on t0022 tests whether the somatic current sink linearizes or sharpens
  dendritic DS.
* Secondary-branch angle. [Cuntz2010] parameterizes branching by a scalar bf; no paper varies branch
  angle at fixed length. Angle controls receptive-field footprint relative to the preferred axis,
  independent of cable properties.
* Dendrite-to-dendrite gap-junction coupling between neighboring SACs. Known biologically, absent
  from reviewed compartmental DS models.
* Non-planar drift of the dendritic tree. Corpus models assume planar arbors; a z-axis tilt sweep
  asks how robust DSI is to real-tissue warping.

## Cross-System Transfer Hypotheses

* Transfer-resistance weighting from fly VS cells [Dan2018] may govern alpha-RGC dendrite-to-axon
  integration but has never been modeled in mammalian RGCs.
* SAC kinetic tiling (sustained-proximal, transient-distal) from [Srivastava2022] and
  [Ezra-Tsur2021] may apply to cortical L2/3 pyramidal DS cells, where thalamic vs. intracortical
  inputs tile by depth; [Anderson1999] rejects geometry alone but did not test kinetic tiling.
* Dendritic-spike branch independence [Sivyer2013] is a retinal finding; the same motif could
  explain subunit DS in zebrafish tectal neurons that no current model addresses.
* Plexus-density control of centrifugal tuning [Morrie2018] may have an analog in cortical
  interneuron axon-arbor density, untested in DS contexts.
* NMDA multiplicative gating as an independent DS mechanism [PolegPolsky2026] may dominate in
  cortical rather than retinal DS, reconciling [Anderson1999] with the retinal picture.

## Falsifiable Predictions for Our Testbeds

1. Scaling distal dendrites by 1.5x on t0022 reduces DSI by more than 30% if passive TR weighting
   [Dan2018] dominates, but leaves DSI within 10% if dendritic-spike branch independence
   [Sivyer2013] dominates.
2. Swapping sustained and transient BC input kinetics on t0024 reverses preferred direction if
   [Srivastava2022] tiling is causal, but only reduces DSI magnitude if [Kim2014] cable delay is
   causal.
3. Thickening distal branches on t0022 (halving distal input resistance) abolishes dendritic-spike
   gain [Schachter2010] while preserving subthreshold DSI, separating active amplification from
   passive filtering.
4. Ablating 25% of random terminal branches on t0022 drops global DSI by less than 15% if branch
   independence [Sivyer2013] holds, but by more than 40% if global TR summation dominates.
5. Collapsing t0024 to a single compartment reproduces full-model DSI-vs-speed if T4-style
   geometry-nullity [Gruntman2018] extends to DSGCs, but fails if the de Rosenroll local-DSI
   mechanism is load-bearing.

## What the Field is NOT Asking

* No paper varies morphology and active conductance densities *simultaneously*; all sweeps hold one
  axis fixed.
* No paper compares reconstructed vs. matched-statistics synthetic morphologies (TREES-style
  [Cuntz2010]) for the same cell type.
* No paper quantifies how DSI degrades under stochastic distal-branch ablation, the natural in vivo
  perturbation from disease or aging.
* No paper separates soma-size from dendrite effects; soma radius is a silent knob.
* No paper asks whether morphology imposes an upper bound on achievable DSI for a given biophysical
  repertoire.

## Risks of Over-Indexing on This Synthesis

* The corpus is SAC-and-DSGC-heavy, biasing mechanism hypotheses toward subcellular
  asymmetric-inhibition wiring; cortical and invertebrate mechanisms are underweighted.
* Roughly a quarter of the corpus comes from one senior-author cluster (Poleg-Polsky, Awatramani,
  Taylor), correlating methods and priors across papers.
* No mammalian in vivo DS data appears; all claims are slice, ex vivo retina, or pure modeling.
  Predictions here should not be evaluated solely against in vivo tuning curves.
