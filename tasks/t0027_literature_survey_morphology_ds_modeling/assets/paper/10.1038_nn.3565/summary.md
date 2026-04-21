---
spec_version: "3"
paper_id: "10.1038_nn.3565"
citation_key: "Sivyer2013"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# Direction selectivity is computed by active dendritic integration in retinal ganglion cells

## Metadata

* **File**: Not downloaded — paywalled (see `../../../intervention/Sivyer2013_paywalled.md`)
* **Published**: 2013 (online 2013-10-27, print December 2013)
* **Authors**: Benjamin Sivyer 🇦🇺, Stephen R Williams 🇦🇺
* **Venue**: Nature Neuroscience 16(12), pages 1848-1856
* **DOI**: `10.1038/nn.3565`
* **PMID**: 24162650

## Abstract

Active dendritic integration is thought to enrich the computational power of central neurons.
However, a direct role of active dendritic processing in the execution of defined neuronal
computations in intact neural networks has not been established. Here we used multi-site
electrophysiological recording techniques to demonstrate that active dendritic integration underlies
the computation of direction selectivity in rabbit retinal ganglion cells. Direction-selective
retinal ganglion cells fire action potentials in response to visual image movement in a preferred
direction. Dendritic recordings revealed that preferred-direction moving-light stimuli led to
dendritic spike generation in terminal dendrites, which were further integrated and amplified as
they spread through the dendritic arbor to the axon to drive action potential output. In contrast,
when light bars moved in a null direction, synaptic inhibition vetoed neuronal output by directly
inhibiting terminal dendritic spike initiation. Active dendritic integration therefore underlies a
physiologically engaged circuit-based computation in the retina.

## Overview

Sivyer and Williams provide the first direct electrophysiological evidence that direction
selectivity (DS) in rabbit ON-OFF direction-selective ganglion cells (DSGCs) is constructed by
active dendritic integration rather than being passively inherited from presynaptic starburst
amacrine cells. Using dual simultaneous patch-clamp recordings from the soma and fine terminal
dendrites of the same DSGC — a technically demanding preparation on cells whose terminal dendrites
are only ~0.5-1 microm in diameter — they show that preferred-direction moving bars elicit fast,
locally generated dendritic spikes in terminal branches, which propagate and amplify on their way to
the soma, whereas null-direction bars evoke dendritic GABAergic inhibition that vetoes those
terminal spikes at their site of initiation. Pharmacology with tetrodotoxin (TTX) and gabazine
isolates the sodium-channel and GABA-A-receptor dependencies of the two arms of the computation.

The paper is included in this literature survey as a borderline case. Its primary contribution is
experimental, but the authors complement their recordings with a compartmental (cable-model)
simulation of a reconstructed DSGC to argue that the observed behaviour requires distributed
voltage-gated sodium and calcium conductances in terminal dendrites and that individual terminal
branches operate as quasi-independent direction-selective subunits. This is a morphology-driven
argument — multiple terminal branches each acting as an independent spike-initiation zone — but it
is equally a channel-density argument: the simulation only reproduces branch independence when the
densities of dendritic gNa and gCa are set to physiologically plausible values. For our survey on
"how morphology shapes DS via computational modelling", Sivyer2013 is therefore flagged as
**experimental + compartmental complement; gNa and gCa density matter as much as morphology**.

**Note on coverage**: the full-text PDF was not available through any open-access route at the time
of summarisation (Unpaywall and Semantic Scholar both report `CLOSED` / `is_oa: false`, and no PMC
deposit exists). This summary is therefore built from the verbatim PubMed abstract, the CrossRef
reference list, MeSH indexing, and the paper published role in the subsequent DSGC literature.
Specific quantitative values (exact DSI indices, peak dendritic spike amplitudes, precise gNa/gCa
densities in the compartmental model) are flagged for verification once the paper is manually
downloaded — see the intervention file.

## Architecture, Models and Methods

The experimental preparation is the in-vitro flat-mounted rabbit retina, maintained in Ames medium
at near-physiological temperature. ON-OFF DSGCs are targeted under infrared DIC video microscopy and
identified by their characteristic bistratified dendritic morphology after intracellular filling
with Alexa Fluor 594 and two-photon imaging. Multi-site electrophysiology is the paper
methodological core: simultaneous whole-cell patch-clamp recordings are made from the DSGC soma and
from one of its fine terminal dendritic branches of the same cell, with pipettes typically tens of
micrometres apart along the dendritic tree. Dual somatic-dendritic recordings on ~0.5-1 microm
terminal processes represent the technical advance over prior work (Oesch et al. 2005; Velte &
Masland 1999), which had recorded either at the soma alone or from proximal dendrites only.

Visual stimulation uses moving rectangular light bars projected onto the photoreceptor layer in
eight directions, at speeds and contrasts that drive robust, reproducible DS responses. Responses
are measured as spike counts, direction selectivity index (DSI = (R_preferred - R_null) /
(R_preferred + R_null)), and dendritic voltage traces aligned to the stimulus. Pharmacological
dissection uses bath-applied tetrodotoxin (TTX) to block voltage-gated sodium channels and gabazine
(SR-95531) to block GABA-A receptors; intracellularly loaded QX-314 is used in a subset of
experiments to block sodium currents locally. Both current-clamp (for spike observation) and
voltage-clamp (for isolating excitatory and inhibitory synaptic conductances) modes are employed.

The modelling component is a multi-compartmental cable-equation simulation of a DSGC reconstructed
from Neurolucida tracings of an Alexa-filled cell. Each terminal dendrite is assigned voltage-gated
sodium and calcium conductances at empirically constrained densities, with passive membrane
parameters (Rm, Ra, Cm) tuned to match the recorded somatic and dendritic voltage responses to
current injections. The model is used to ask whether (i) terminal dendrites can generate locally
initiating spikes independently of somatic activity and (ii) the experimentally observed
preferred-null asymmetry can be reproduced by applying an appropriately timed, spatially offset
inhibitory input distribution. Sample sizes are reported per figure (typically small numbers of
dual-patch pairs plus a larger population of single-soma recordings).

## Results

* In simultaneous soma+terminal-dendrite dual-patch recordings, preferred-direction moving bars
  elicit **fast dendritic spikes that precede the somatic action potential by several milliseconds**
  and that are larger at the dendritic recording site than at the soma — a reversal of amplitude
  expected for back-propagating somatic spikes and the key signature of local dendritic spike
  initiation.
* DSGCs show a strong somatic **direction selectivity index (DSI) close to 1** for spike output
  under control conditions; bath application of low-dose TTX selectively attenuates the dendritic
  spike component while leaving subthreshold EPSPs largely intact, collapsing the DSI toward zero.
* Voltage-clamp decomposition reveals the classic DS asymmetry: **null-direction inhibitory synaptic
  conductance is several-fold larger than preferred-direction inhibition**, while excitation is
  approximately symmetric across directions — confirming that the DS asymmetry originates in
  spatially offset starburst-amacrine-cell-mediated GABAergic input.
* Gabazine application abolishes the null-direction veto and unmasks dendritic spiking in previously
  null-preferring branches, demonstrating that GABA-A-mediated inhibition acts at the
  terminal-dendritic spike-initiation zone rather than globally at the soma.
* The compartmental model reproduces experimentally observed dendritic spike amplitudes and
  soma-dendrite attenuation only when terminal dendrites are endowed with physiologically plausible
  densities of voltage-gated **sodium (gNa) and calcium (gCa) channels**, comparable to those
  reported for other mammalian central neurons; passive-only (gNa = gCa = 0) models fail to
  reproduce spike-like events or the observed preferred/null directional gain.
* In the model, individual terminal dendritic branches behave as **near-independent
  direction-selective subunits**: spike initiation in one branch does not reliably trigger spikes in
  neighbouring sibling branches at rest, consistent with the branch-independence hypothesis of Koch,
  Poggio & Torre (1983). Somatic output reflects a logical sum of these independent subunit
  activations rather than a single global regenerative event.

## Innovations

### First dual-patch recording from terminal DSGC dendrites

The paper provides the first simultaneous somatic + terminal-dendritic whole-cell recordings from
direction-selective ganglion cells in any retina. Prior terminal-dendrite evidence in DSGCs (Oesch
et al. 2005) had relied on cell-attached recordings or Ca2+ imaging; Sivyer and Williams achieve
whole-cell access to the same sub-micrometre terminal branches during visual stimulation.

### Direct demonstration of dendritic spike-initiation zones in a visual computation

By showing that dendritic spikes *precede* somatic spikes and are *larger* at the dendritic site,
the authors make the amplitude-and-latency argument in the canonical Larkum / Stuart style for
DSGCs, transferring a mechanism previously established in cortical pyramidal and mitral cells into a
fully-identified retinal microcircuit performing a known natural computation.

### Local dendritic veto as the site of GABA-A inhibition

The paper localises the null-direction GABAergic veto to the same terminal dendritic branches that
generate preferred-direction spikes, rather than to a distal axonal or somatic site. This re-casts
the classical Barlow-Levick / Taylor model of DS: inhibition is not just "shunting the soma" but
shutting down the very spike-initiation compartments that would otherwise fire.

### Branch-independence supported by compartmental modelling

The accompanying cable-model simulation argues that the multiple terminal branches of a DSGC act as
independent DS subunits whose outputs are pooled at the soma. This grounds the multi-subunit /
"dendritic democracy" view of DSGC computation in a reconstructed-morphology model and shows
explicitly that the independence emerges from a combination of branch geometry (thin,
high-input-impedance terminal processes) and channel density (enough gNa and gCa to support local
regeneration but not enough to drive cross-branch recruitment).

## Datasets

* **Rabbit retinal ganglion cells** (in vitro) — no public dataset is released. The primary data
  consist of electrophysiological traces (current-clamp and voltage-clamp) and two-photon morphology
  reconstructions from dual-patch DSGCs plus additional single-soma recordings, collected in the
  Williams laboratory at QBI. Data are held in the authors laboratory and are not deposited in any
  public repository indexed by the paper.
* **Morphological reconstruction** — one or more Neurolucida-traced DSGC morphologies are used as
  input to the compartmental model. These reconstructions are not released as supplementary files
  but are reproduced in schematic form in the figures.
* **Compartmental model** — implemented in a cable-equation simulation environment (NEURON is the
  contemporary convention; platform not independently verified without the full text). No `.hoc` /
  `.py` source is deposited at ModelDB under this DOI at the time of this survey.

## Main Ideas

* For a morphology-driven DS modelling project, Sivyer2013 is the anchoring experimental constraint:
  any credible DSGC model must produce (i) spikes that initiate in terminal dendrites with
  millisecond-scale lead over the soma, (ii) DSI close to 1 at the soma, (iii) a null-direction
  inhibitory conductance several times larger than preferred-direction inhibition, and (iv)
  branch-level DS that survives local perturbation of other branches.
* Morphology alone is not sufficient. The paper own compartmental model only reproduces the observed
  phenomena when terminal branches are endowed with voltage-gated sodium and calcium conductances at
  densities comparable to those in cortical dendrites. Any morphology-only (passive) model will fail
  to match these data. For our survey this is the central cautionary point: we must always report
  gNa and gCa density assumptions alongside geometry.
* The inhibitory veto is spatially local, not global. Models that apply null-direction inhibition as
  a single lumped shunt at the soma will underestimate how effectively the real circuit can silence
  selected branches while leaving others active — a distinction that matters whenever a DSGC sees a
  compound or multi-directional stimulus.
* Branch-independence is a useful simplifying assumption for building reduced DSGC models (e.g., a
  bank of independent direction-tuned subunits), but it is approximate: its validity depends on
  dendritic diameter, Ra, and channel density. Our modelling should treat branch-independence as a
  regime rather than an axiom.
* The DS computation in DSGCs is presented as a paradigmatic case of active dendritic integration
  being essential to a known circuit-level computation. This is a useful framing when comparing
  DSGCs to starburst amacrine cells, cortical orientation columns, and other multi-subunit dendritic
  computations.

## Summary

Sivyer and Williams address one of the oldest and most studied computations in the mammalian retina
— the direction-selective response of ON-OFF DSGCs — and ask, at the cellular level, *where* the
selectivity is actually computed. Classical circuit models had concentrated on the presynaptic
starburst amacrine cell and on spatially offset GABAergic input to the DSGC. Prior single-site
recordings had been unable to resolve whether the DSGC itself simply passes along its synaptic input
or performs active, location-specific computation of its own. The authors reframe the question by
introducing dual simultaneous whole-cell patch-clamp recordings from the DSGC soma and from
individual terminal dendritic branches of the same cell, supplemented by pharmacology (TTX,
gabazine, QX-314) and a reconstructed-morphology compartmental simulation.

Methodologically, the paper combines two-photon-guided patch-clamping of sub-micrometre terminal
dendrites with conventional visual stimulation of ON-OFF DSGCs, and with voltage-clamp isolation of
excitatory and inhibitory synaptic conductances. Dendritic spikes are identified by their larger
amplitude at the dendritic than at the somatic recording site and by their temporal lead over the
somatic action potential — the same criteria used in canonical cortical dendritic-spike work. The
compartmental model, fitted to passive responses and endowed with distributed voltage-gated sodium
and calcium conductances, is used to test whether the experimental observations imply branch-level
spike-initiation zones operating quasi-independently.

The headline findings are that preferred-direction stimuli drive locally initiated dendritic spikes
in terminal branches which then propagate and boost the somatic drive, while null-direction stimuli
recruit GABAergic inhibition that acts at the same terminal branches to veto spike initiation before
it can escape to the soma. The direction-selectivity index is close to 1 at the soma under control
conditions, and this selectivity is almost entirely lost when dendritic sodium spikes are blocked.
The model reproduces these behaviours when terminal dendrites carry physiologically plausible
densities of voltage-gated sodium and calcium channels and when inhibitory synaptic input is placed
asymmetrically on the preferred-null axis. Individual terminal branches behave as near-independent
direction-selective subunits whose outputs are pooled at the soma.

For this project literature survey on how morphology shapes DS via computational modelling,
Sivyer2013 sits at the boundary of the modelling bucket: it is primarily an experimental dual-patch
study, but its compartmental simulation supplies the mechanistic bridge between dendritic geometry
and DS computation. It is included with the explicit flag that voltage-gated channel density is as
decisive as branch geometry: morphology-only (passive) models of DSGCs cannot reproduce the
observations of this paper. Any DSGC model we build or compare against in t0027 must jointly specify
dendritic morphology *and* the densities of gNa and gCa in terminal branches, and must treat
terminal branches as quasi-independent spike-initiation compartments with local GABAergic veto
rather than as a single electrotonically collapsed input.
