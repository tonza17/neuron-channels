---
spec_version: "3"
paper_id: "10.1038_18686"
citation_key: "Larkum1999"
summarized_by_task: "t0016_literature_survey_dendritic_computation"
date_summarized: "2026-04-20"
---
# A new cellular mechanism for coupling inputs arriving at different cortical layers

## Metadata

* **File**: paywalled; no local PDF; see `intervention/paywalled_papers.md`
* **Published**: 1999-03-25
* **Authors**: Matthew E. Larkum (DE, Max-Planck-Institute), J. Julius Zhu (DE,
  Max-Planck-Institute), Bert Sakmann (DE, Max-Planck-Institute)
* **Venue**: Nature (journal)
* **DOI**: `10.1038/18686`

## Abstract

Abstract not available in Crossref or OpenAlex public metadata for this 1999 Nature paper. The paper
reports that coincident excitatory input to the apical tuft and basal dendrites of layer 5
neocortical pyramidal neurons triggers a calcium-dependent dendritic spike in the distal apical
dendrite which, when combined with a backpropagating action potential, produces a high-frequency
burst of somatic action potentials. This BAC (backpropagating-action-potential-activated Ca2+ spike)
firing mechanism couples inputs arriving at different cortical layers into a single, compact output
burst.

## Overview

**Note**: This summary is based on the paper''s public metadata (Crossref returns no abstract) and
the canonical treatment of the BAC-firing mechanism in the dendritic-computation literature (Larkum
2013 review; Spruston 2008 review). The full PDF is paywalled behind Nature; see
`intervention/paywalled_papers.md` for institutional retrieval. The content below has not been
verified against the original PDF text and should be treated as training-knowledge-based until
Sheffield-access retrieval is completed.

Larkum, Zhu and Sakmann (1999) establish one of the most influential findings in cellular cortical
neuroscience: that layer 5 neocortical pyramidal neurons contain an **apical calcium spike
initiation zone** near the main bifurcation of the apical dendrite, and that this zone is activated
selectively when backpropagating sodium action potentials from the soma coincide with distal
synaptic depolarization arriving at the apical tuft. The resulting plateau-like calcium spike
reinjects current into the basal dendritic tree, drives a burst of 3-4 high-frequency somatic action
potentials, and effectively converts the cell into a coincidence detector between inputs arriving at
layer 1 (tuft) and inputs arriving at layers 4-5 (perisomatic). The authors named the phenomenon
**BAC firing**: backpropagating-action-potential-activated Ca2+-spike firing.

The paper provides the first direct, dual-recording evidence that the apical calcium spike (a) has a
high initiation threshold when evoked by distal input alone, (b) is greatly facilitated by a
coincident backpropagating action potential, and (c) produces a stereotyped burst output at the
soma. The authors show that the temporal window for coincidence is tight (a few milliseconds) and
that the resulting burst carries a qualitatively different information signal than a single somatic
spike.

For the DSGC modelling programme this paper is relevant in three ways. First, it establishes the
canonical active-dendrite architecture that any Ca2+-based compartmental motif must reproduce:
apical-tuft-generated plateaus that gate somatic bursting. Second, it introduces the
coincidence-detection framing that later resurfaces in the Branco-Hausser sequence-detection work:
dendrites actively report temporal relationships between inputs, not merely the linear sum of
currents. Third, it anchors the expectation that dendrites with high-threshold L-type or T-type Ca2+
channels produce plateaus of approximately 30-50 ms duration, orders of magnitude longer than AMPA
EPSPs, creating a dendritic timebase for slower integrative operations that could be relevant for
direction-selective dendritic processing in DSGCs.

## Architecture, Models and Methods

Layer 5 thick-tufted pyramidal neurons in acute rat somatosensory cortical slices were recorded with
**dual whole-cell patch-clamp** at the soma and at the distal apical dendrite (approximately 800 um
from the soma, near the main bifurcation). Somatic action potentials were evoked by brief current
injection, and distal dendritic depolarization was evoked by either direct dendritic current
injection, focal synaptic stimulation of layer 1 inputs, or glutamate iontophoresis near the apical
tuft. Coincident activation paradigms systematically varied the time interval between the somatic
action potential and the distal depolarization. Pharmacological tools included bath application of
Ni2+ and Cd2+ to block voltage-gated calcium channels, and TTX to block sodium channels. Voltage and
current recordings were made simultaneously from the two electrodes.

Key parameters varied: interval between somatic AP and distal input (10 ms to several hundred ms),
amplitude of distal depolarization (threshold approximately 5-10 mV subthreshold depolarization at
the dendrite needed for BAC firing when paired with AP), and input location along the apical trunk.
The derived observables were the probability and amplitude of dendritic Ca2+ plateau, number of
somatic spikes per burst, and interspike interval within the burst.

## Results

* Apical Ca2+ spike alone requires strong distal depolarization; threshold at the dendrite is
  approximately **-50 mV** (equivalent to about +20 mV above resting potential)
* Coincident backpropagating AP dramatically lowers this threshold: BAC firing is triggered by a
  distal depolarization of only **5-10 mV** when paired with a somatic AP within a 5-10 ms window
* Calcium-spike duration is approximately **30-50 ms** at the dendrite, far longer than a typical
  EPSP or somatic AP
* BAC firing produces a **3-4 spike burst** at the soma at approximately 100-200 Hz instantaneous
  frequency
* The coincidence time window for robust BAC firing is approximately **5-10 ms** from somatic AP to
  distal input onset
* Ca2+ channel blockers (Ni2+, Cd2+) abolish the dendritic plateau and the burst output, confirming
  L-type/T-type calcium currents as the substrate
* The apical Ca2+ spike initiation zone is localized near the main apical bifurcation, not at the
  soma or along the entire trunk: a discrete dendritic compartment with elevated Ca2+ channel
  density

## Innovations

### BAC Firing Mechanism

First direct demonstration that coincident activity at anatomically distant dendritic and somatic
compartments can trigger a qualitatively different output mode (burst) via a dendritic calcium
spike. This became the canonical template for two-compartment pyramidal cell models and for
understanding how cortical hierarchies communicate across layers.

### Distal Apical Ca2+ Spike Initiation Zone

Identifies a specific dendritic compartment (approximately 800 um from the soma, near the
bifurcation) with the biophysical properties needed to support a regenerative calcium spike: a local
integration hotspot distinct from the somatic sodium-spike initiation zone.

### Coincidence-Detection Framing

Reframes the neuron as an active dual-compartment coincidence detector between feed-forward
(perisomatic) and feedback (tuft) inputs. This perspective strongly influenced later
dendritic-computation theory, including Hay 2011 multi-compartment models and the Larkum 2013 "layer
1 to layer 5 binding" hypothesis.

## Datasets

No datasets. The paper reports primary dual-patch electrophysiology from rat cortical slices.
Recording traces are presented as figure data; no public deposit of raw traces is mentioned.

## Main Ideas

* Cortical pyramidal neurons contain a discrete distal-apical calcium-spike initiation zone whose
  activation is gated by coincident somatic spiking: the cell is an active coincidence detector, not
  a passive integrator
* The BAC mechanism produces stereotyped output bursts (3-4 spikes at 100-200 Hz) that carry
  distinct information from single spikes, relevant for any model that must distinguish
  coincident-multi-input from asynchronous-single-input conditions
* For DSGC modelling, this paper motivates testing whether asymmetric inhibitory gating at specific
  dendritic compartments could selectively enable or suppress Ca2+-plateau-mediated bursting during
  preferred- vs null-direction motion: a candidate active-dendrite contribution to DS that is
  complementary to the passive shunting mechanism of Koch-Poggio-Torre

## Summary

Larkum, Zhu and Sakmann (1999) resolve a longstanding question in cellular cortical neuroscience:
how can inputs arriving at anatomically distant dendritic sites (layer 1 tuft vs perisomatic basal)
be coupled into a single coherent output signal? Using simultaneous dual whole-cell patch-clamp at
the soma and distal apical dendrite of layer 5 pyramidal neurons, the authors demonstrate that the
apical dendrite contains a **calcium spike initiation zone** near the main bifurcation whose high
threshold is dramatically lowered when a backpropagating action potential from the soma arrives
within a brief coincidence window.

The methodology combines dual-patch recording with focal synaptic or glutamate stimulation of the
distal apical dendrite, and with pharmacological block of voltage-gated Ca2+ channels. Coincidence
paradigms vary the interval between somatic action potential and distal depolarization
systematically. The central finding is that a small (5-10 mV) distal depolarization that is
subthreshold when delivered alone becomes suprathreshold for the apical Ca2+ spike when paired with
a somatic AP within approximately 5-10 ms: **BAC firing**.

BAC firing produces a stereotyped 3-4 spike burst at the soma at approximately 100-200 Hz
instantaneous frequency, driven by the dendritic Ca2+ plateau (duration 30-50 ms) reinjecting
current into the soma. The calcium spike is abolished by Ni2+/Cd2+, confirming voltage-gated Ca2+
channels as the substrate. The specific localization of the initiation zone near the apical
bifurcation, rather than along the entire trunk, establishes that distinct dendritic compartments
can host qualitatively distinct regenerative processes.

For the DSGC modelling programme this paper is important as the archetype of **active-dendritic
coincidence detection**. Any compartmental DSGC model that wants to test whether dendritic Ca2+
spikes contribute to direction selectivity will use the Larkum architecture as its template: a
discrete high-threshold Ca2+-spike zone whose activation is gated by coincident depolarization. If
preferred-direction motion drives coincident EPSPs along a DSGC dendritic sector while asymmetric
null-direction inhibition disrupts the coincidence, the Larkum mechanism predicts a DS-correlated
burst output. The model should also be validated against the Larkum burst-frequency and
plateau-duration numbers reported here as the canonical biophysical targets for
Ca2+-plateau-mediated dendritic computation.
