---
spec_version: "3"
paper_id: "10.1126_science.aan3846"
citation_key: "Bittner2017"
summarized_by_task: "t0016_literature_survey_dendritic_computation"
date_summarized: "2026-04-20"
---
# Behavioral time scale synaptic plasticity underlies CA1 place fields

## Metadata

* **File**: paywalled; no local PDF; see `intervention/paywalled_papers.md`
* **Published**: 2017-09-08
* **Authors**: Katie C. Bittner (US, HHMI Janelia), Aaron D. Milstein (US, HHMI Janelia + Stanford
  Neurosurgery), Christine Grienberger (US, HHMI Janelia), Sandro Romani (US, HHMI Janelia), Jeffrey
  C. Magee (US, HHMI Janelia)
* **Venue**: Science (journal)
* **DOI**: `10.1126/science.aan3846`

## Abstract

Learning is primarily mediated by activity-dependent modifications of synaptic strength within
neuronal circuits. We discovered that place fields in hippocampal area CA1 are produced by a
synaptic potentiation notable for its driving signal, a dendritic plateau potential, and the
temporal scale of its synaptic eligibility trace, which is seconds in duration. The dendritic
plateau potentials were produced by input from entorhinal cortex and could be triggered
naturalistically or artificially to rapidly form place fields. This behavioral time scale synaptic
plasticity is a non-Hebbian form of plasticity that efficiently stores entire behavioral sequences
within the synaptic weights of hippocampal neurons to provide a potential substrate for rapid
learning of episodes and navigational routes.

## Overview

**Note**: This summary is based on the Crossref-indexed abstract and the canonical treatment of
behavioral time scale synaptic plasticity (BTSP) in the plateau-potential literature. The full PDF
is paywalled behind AAAS; see `intervention/paywalled_papers.md` for institutional retrieval. The
content below has not been verified against the original PDF and should be treated as
training-knowledge-based until Sheffield-access retrieval is completed.

Bittner and colleagues (2017) report the discovery of a non-Hebbian form of synaptic plasticity in
hippocampal area CA1, driven by dendritic plateau potentials, whose critical time window is orders
of magnitude longer than classical spike-timing-dependent plasticity (STDP). The authors call it
**behavioral time scale synaptic plasticity (BTSP)**: a single dendritic plateau potential pairs
with synaptic inputs arriving anywhere in a window of approximately plus-or-minus 1-2 seconds around
the plateau, and induces rapid, robust potentiation that creates an entire place field in one trial.

The plateau potentials (duration approximately 50-300 ms) are triggered by input from entorhinal
cortex layer III (EC3) onto the distal apical tuft of CA1 pyramidal cells and are either evoked
naturalistically (during exploratory behavior) or artificially (by current injection). A single
pairing of a plateau with running through a corridor is sufficient to induce a place field at the
paired location, with place-field half-width of approximately 1.5-2 seconds (corresponding to about
15-20 cm at typical running speeds). BTSP is symmetric in time (potentiation for both
pre-before-post and post-before-pre pairings) and does not depend on the classical Hebbian
requirement of near-coincident pre- and post-synaptic spiking.

For the DSGC modelling programme this paper is relevant in two complementary ways. First, it
reinforces the dendritic-plateau framing already established by Larkum (1999): the relevant
dendritic nonlinearity for behavior is not the sub-millisecond sodium spike but the tens-to-hundreds
of milliseconds long plateau. Second, it generalises plateau-driven computation beyond
pyramidal-cell BAC firing to a hippocampal place-field mechanism that converts sustained dendritic
depolarization into a long-timescale plasticity readout. Whether analogous plateau-driven mechanisms
operate in DSGC dendrites (which are much shorter and non-tufted) is an open question, but the
Bittner framework provides the mechanistic template and the quantitative targets.

## Architecture, Models and Methods

The authors use in vivo whole-cell patch-clamp recordings from CA1 pyramidal neurons in head-fixed
mice running on a linear treadmill. Dendritic plateau potentials are identified by their stereotyped
waveform (sustained depolarization of 30-60 mV amplitude and duration 50-300 ms) and by targeted
stimulation experiments that selectively drive EC3 inputs onto the apical tuft.

To induce BTSP artificially, the authors deliver a large somatic current injection (1-2 nA for 300
ms) at a chosen location along the treadmill and pair this with a burst of synaptic activity from
presynaptic CA3 Schaffer-collateral inputs. The induced place field is then measured on subsequent
laps. Temporal offsets between plateau onset and Schaffer-input pairing are varied systematically
from approximately -4 seconds to +4 seconds to map the BTSP time-window.

Complementary intracellular pharmacology includes local application of NMDA-receptor antagonists and
voltage-gated-calcium-channel blockers to probe the plateau-generation mechanism. A computational
compartmental model accompanies the experiments to test whether the observed plasticity time window
is consistent with an intracellular calcium-activated synaptic eligibility trace.

## Results

* A single plateau potential paired with running induces a stable place field in **one trial**, with
  place-field duration (half-width) approximately **1.5-2 seconds** at typical running speeds
* The BTSP time window is approximately **plus-or-minus 1-2 seconds** (4 seconds wide total),
  roughly 1000-fold longer than the 20-40 ms STDP window
* BTSP is **symmetric in time**: pre-before-post and post-before-pre pairings both produce
  potentiation, unlike classical Hebbian STDP
* Plateau duration is approximately **50-300 ms** with amplitude **30-60 mV** at the soma
* Place-field formation rate under artificial induction is approximately **60-80%** per single
  pairing trial
* Plateau potentials are driven by EC3 input to the apical tuft; blocking NMDA receptors abolishes
  the plasticity induction
* Natural place-field formation in novel environments is preceded by spontaneous plateau potentials,
  providing strong correlational evidence that plateaus are causal

## Innovations

### Behavioral Time Scale Synaptic Plasticity

First demonstration of a synaptic plasticity rule whose critical pairing window is measured in
seconds rather than tens of milliseconds, shifting the plasticity literature from spike-timing rules
to behaviorally-relevant dendritic-plateau rules.

### Single-Trial Place Field Induction

First in vivo demonstration that a single artificially induced dendritic plateau can create a
complete place field in one trial, providing a causal mechanistic anchor for how hippocampal neurons
rapidly learn new environments.

### Non-Hebbian Symmetric Plasticity

Establishes that the BTSP rule does not require pre-before-post pairing: a plateau acts as a
powerful, location-specific "instructive" signal that potentiates any input active within a broad
temporal window, regardless of order.

## Datasets

No public datasets. The in vivo patch traces and behavioral trajectories are presented as figure
data and supplementary material; no deposition to a public repository is noted.

## Main Ideas

* Dendritic plateau potentials carry a behavioral-timescale instructive signal that reshapes
  synaptic weights at a time-scale matched to behavior, not to spike timing
* The plateau amplitude/duration numbers (30-60 mV, 50-300 ms) should be used as biophysical targets
  for any compartmental model that wants to test plateau-driven mechanisms
* For DSGC modelling the BTSP framework motivates asking whether transient plateau-like
  depolarisations in DSGC dendrites (perhaps triggered by coincident bipolar+NMDA input during
  preferred-direction motion) could gate longer-timescale direction-selective computations, although
  the DSGC dendritic geometry is very different from CA1 tuft architecture so direct transfer of
  parameters is not justified

## Summary

Bittner and colleagues (2017) discover a new form of synaptic plasticity in hippocampal area CA1
that operates on the behavioral time scale (seconds) and is driven by dendritic plateau potentials.
Using in vivo whole-cell patch-clamp from CA1 pyramidal neurons during running on a linear
treadmill, the authors combine natural observation of spontaneous plateaus with artificial plateau
induction (via somatic current injection) paired with Schaffer-collateral stimulation.

The methodology systematically varies the temporal offset between the plateau and the pairing
synaptic input, mapping the BTSP time window. Compartmental modelling and pharmacological block of
NMDA receptors and voltage-gated calcium channels identify the mechanistic substrate as a
calcium-activated intracellular eligibility trace that persists for seconds after a plateau.

The central finding is that a single plateau, paired with running, is sufficient to create a place
field in one trial. The BTSP time window extends approximately plus-or-minus 1-2 seconds on either
side of the plateau, is symmetric (non-Hebbian), and does not require classical pre-before-post
spike pairing. Place-field half-width is approximately 1.5-2 seconds (about 15-20 cm at typical
mouse speeds). Plateau potentials themselves are 30-60 mV in amplitude, 50-300 ms in duration, and
require EC3 input to the apical tuft plus active NMDA conductances.

For the DSGC modelling programme this paper is important in two ways. First, it generalizes
plateau-driven dendritic computation beyond Larkum-style cortical BAC firing to a hippocampal
place-field mechanism, establishing plateaus as a cross-cell-type computational motif. Second, the
quantitative BTSP rule (symmetric, seconds-wide, plateau-gated) provides a candidate mechanism that
DSGC models could test: if DSGC dendrites can host brief plateau-like depolarisations during
preferred-direction motion, these could in principle gate direction-selective plasticity on a
behaviorally relevant timescale. Whether DSGC dendritic geometry (short, non-tufted, compact)
supports such plateaus is an open empirical question that follow-up compartmental simulation can
address.
