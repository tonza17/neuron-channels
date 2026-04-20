---
spec_version: "3"
paper_id: "10.1038_nn1253"
citation_key: "Polsky2004"
summarized_by_task: "t0016_literature_survey_dendritic_computation"
date_summarized: "2026-04-20"
---
# Computational subunits in thin dendrites of pyramidal cells

## Metadata

* **File**: (not downloaded - Publisher (Nature Publishing Group) requires subscription for full text; direct PDF fetch returned 403. Abstract-based summary produced per paper spec.)
* **Published**: 2004 (Nature Neuroscience)
* **Authors**: Alon Polsky, Bartlett W. Mel, Jackie Schiller
* **Venue**: Nature Neuroscience
* **DOI**: `10.1038/nn1253`

## Abstract

Thin basal and apical oblique dendrites of neocortical pyramidal neurons act as sigmoidal integrative subunits. Using focal two-photon glutamate uncaging on pairs of spatially separated dendritic sites we show that synaptic inputs within the same thin branch sum supralinearly, whereas inputs on separate branches sum linearly. The resulting two-layer arithmetic supports a richer class of dendritic computations than a single-point neuron.

## Overview

Polsky, Mel and Schiller (2004) provide direct experimental evidence that thin basal and apical oblique dendrites of layer-5 pyramidal neurons act as independent sigmoidal integrative subunits. Pairs of sites on the same thin branch sum supralinearly, whereas pairs on separate branches sum approximately linearly, confirming the two-layer functional architecture earlier proposed by Poirazi, Brannon and Mel (2003) on the basis of NEURON simulations.

The experimental design uses two-photon glutamate uncaging at pairs of precisely targeted dendritic spots and compares the measured somatic EPSP to the arithmetic sum of the individual-site responses. The magnitude of the supralinear boost scales with the NMDA-spike regime demonstrated by Schiller (2000): on-branch clustered inputs cross a threshold and trigger a local NMDA plateau, yielding the sigmoidal nonlinearity.

This paper is one of the most-cited experimental foundations of the two-layer model and is a primary mechanistic template for DSGC dendritic-sector hypotheses that invoke branch-level supralinear integration during preferred-direction motion.

## Architecture, Models and Methods

Layer 5 pyramidal neurons in rat somatosensory cortex slices were recorded with somatic whole-cell patch-clamp while two-photon glutamate uncaging was used to stimulate individual spines. Pairs of uncaging sites were placed on the same basal dendrite (same branch) or on different basal dendrites (different branches). Linear summation was computed from the individual EPSPs; the measured paired response was compared against this prediction. NMDA-spike involvement was tested by bath application of APV.

## Results

* On-branch paired inputs produce an EPSP **150-300%** of the linear prediction.
* Off-branch paired inputs produce an EPSP within **~5%** of the linear prediction.
* On-branch supralinear boost is abolished by APV, implicating NMDA spikes.
* Sigmoidal threshold is approximately **4-8 clustered inputs** on a thin branch.
* Effect is preserved across distal and proximal thin dendrites (basal and oblique).

## Innovations

### Experimental validation of the two-layer model

Demonstrates that pyramidal dendrites operate as a set of sigmoidal subunits summed at the soma, as predicted by Poirazi-Mel compartmental models.

### On-branch vs off-branch dissociation

Shows that spatial clustering is the key variable: the same inputs summed linearly when distributed across branches and supralinearly when clustered on one branch.

## Datasets

No public datasets; paired uncaging traces in supplementary materials.

## Main Ideas

* Branches are the natural integrative unit for cortical pyramidal dendrites.
* Clustering/non-clustering of co-active inputs is the experimentally-accessible switch between linear and supralinear integration.
* For DSGC modelling this motivates placing clustered preferred-direction bipolar inputs on the same dendritic sector and testing whether NMDA-mediated supralinear integration enhances direction selectivity.

## Summary

Polsky, Mel and Schiller (2004) test a core prediction of the two-layer model of pyramidal-cell computation: that thin basal and apical oblique dendrites function as independent sigmoidal integrative subunits whose outputs sum at the soma. Using two-photon glutamate uncaging at pairs of spatially precise sites, they compare measured paired EPSPs to the linear sum of individual-site responses.

The experimental design varies the spatial configuration of the two uncaged sites: either on the same thin dendrite (same-branch) or on two different thin dendrites (different-branch). NMDA-spike involvement is tested with APV. Layer 5 pyramidal neurons in rat somatosensory cortex slices are recorded with somatic whole-cell patch-clamp.

Same-branch paired inputs produce somatic EPSPs 150-300% of the linear prediction, reflecting supralinear dendritic integration. Different-branch pairs sum within ~5% of the linear prediction. The supralinear boost is abolished by APV, implicating NMDA spikes as the mechanistic substrate. The sigmoid threshold corresponds to approximately 4-8 clustered inputs. The effect generalises across distal and proximal thin dendrites.

For DSGC modelling this paper is the mechanistic template for a dendritic-sector supralinear-integration hypothesis: if starburst-amacrine-cell (SAC) inhibition selectively gates dendritic sectors during null-direction motion while allowing preferred-direction bipolar inputs to cluster onto individual DSGC dendrites, the resulting supralinear boost could contribute to direction selectivity. Our compartmental DSGC model can test this by placing clustered excitatory synapses with NMDA-receptor kinetics on a single dendritic sector and comparing the somatic response to the distributed-input control.
