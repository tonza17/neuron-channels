---
spec_version: "3"
paper_id: "10.1016_j.celrep.2025.116833"
citation_key: "deRosenroll2026"
summarized_by_task: "t0024_port_de_rosenroll_2026_dsgc"
date_summarized: "2026-04-21"
---
# Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective circuit

## Metadata

* **File**: `files/derosenroll_2026_ds-microarchitecture.pdf`
* **Published**: 2026-02-24 (Cell Reports 45, 116833)
* **Authors**: Geoff deRosenroll CA, Santhosh Sethuramanujam IN, Gautam B. Awatramani CA
* **Venue**: Cell Reports (journal)
* **DOI**: `10.1016/j.celrep.2025.116833`
* **Companion code**: Zenodo DOI `10.5281/zenodo.17666158`; GitHub
  `geoffder/ds-circuit-ei-microarchitecture`

## Abstract

GABAergic/cholinergic starburst amacrine cells play a crucial role in shaping direction selectivity
in the dendrites of downstream direction-selective (DS) ganglion cells (DSGCs) in the retina by
providing "null" inhibitory and "preferred" excitatory signals. The extent to which GABA and
acetylcholine (ACh) signals are co-transmitted at the subcellular level is challenging to assess,
making it difficult to fully appreciate the mechanisms underlying this dendritic computation. Here,
two-photon Ca2+ imaging reveals that processing within local dendritic "DS subunits" is compromised
when ACh dynamics are perturbed regionally with an acetylcholinesterase blocker. A network model
that captures the specific anatomical "wiring" of the DS circuit reveals how minor perturbations in
the spatiotemporal properties of ACh--that do not disrupt the global excitation/inhibition (E/I)
balance--uncouple E/I locally and compromise direction selectivity. These results reveal the inner
workings of the "hidden" synaptic microarchitecture that mediates diverse, localized direction
computations across the DSGC dendritic field.

## Overview

deRosenroll, Sethuramanujam, and Awatramani combine two-photon calcium imaging in mouse retina with
a biophysically detailed compartmental network model to test how the subcellular spatial pattern of
co-released acetylcholine (ACh) and GABA from starburst amacrine cells (SACs) shapes direction
selectivity (DS) in ON-OFF DSGCs. The central experimental finding is that application of the
acetylcholinesterase (AChE) blocker ambenonium (AMB) broadens the diffusion footprint of ACh without
altering the global excitation/inhibition (E/I) balance measured somatically, and causes DS to
collapse specifically in the dendritic subunits close to the pipette tip, while distant subunits and
the somatic spike output remain relatively spared.

The modeling component reverse-engineers the circuit at single-synapse resolution. Starburst
varicosities are positioned on a morphologically reconstructed DSGC using the Briggman et al. 2011
wiring diagram. Each SAC release site co-transmits ACh and GABA with correlated, noisy release rates
(AR(2) process, multivariate Gaussian release correlation). By systematically detuning local
ACh/GABA co-release, either by unbalancing their relative gains, decorrelating their release, or
spatially spreading ACh, the model reproduces the AMB phenotype: globally matched E/I coexists with
locally uncoupled E/I, and the direction selectivity index (DSI) falls. Simulations that preserve
local correlation (correlated release) yield DSI around 0.39, while uncorrelated release collapses
DSI to around 0.25, demonstrating that subcellular E/I coordination rather than dendrite-averaged
E/I ratios determines DSGC spike tuning.

The paper significance lies in explicitly showing that the micro-scale wiring of SACs onto DSGCs is
not redundant with the global E/I envelope. It recasts DS as a computation built by thousands of
tiny, spatially localized E/I packages and provides a quantitative, mechanistically grounded model
that future compartmental reimplementations (including this NEURON port) can use as a benchmark.

## Architecture, Models and Methods

The computational model is implemented in NEURON (Hines and Carnevale 1997) with a Python driver and
HOC morphology. A single ON-OFF DSGC with 341 membrane sections is simulated; the reconstructed
morphology is imported through `RGCmodelGD.hoc`. Passive properties in the code repository are Ra =
100 Ohm*cm, cm = 1 uF/cm^2, gleak = 5e-5 S/cm^2, eleak = -60 mV (the paper text reports Ra = 200
Ohm*cm and eleak = -65 mV, a minor discrepancy worth preserving both values during the port). Active
conductances on soma/primary/tertiary dendrites use the custom `HHst_noiseless.mod` mechanism
(Hodgkin-Huxley style Na+ and K+ without stochastic channel noise). Code-based densities are gbar_Na
= 150, 200, 30 mS/cm^2 and gbar_K = 35, 40, 25 mS/cm^2 for soma, primary, and distal compartments;
paper text quotes 200, 70, 35 and 40, 12, 18 mS/cm^2, respectively; both are recorded for the port.
There is no explicit axon-initial-segment section and no Nav1.6/Nav1.2 split: spikes are somatic
Na-driven. `cadecay.mod` supplies intracellular Ca2+ buffering with a 10 ms decay time constant.

Synaptic inputs comprise excitatory ACh (Exp2Syn, tau1/tau2 = 0.5/6 ms, E_rev = 0 mV, gmax = 140.85
pS), inhibitory GABA (Exp2Syn, 0.5/35 ms, E_rev = -60 mV, gmax = 450.72 pS), and NMDA
(`Exp2NMDA.mod` with voltage-dependent Mg2+ block, 2/80 ms, E_rev = 0 mV, gmax = 140.85 pS).
Bipolar-cell glutamate drives a separate AMPA Exp2Syn (0.2/4 ms). SAC varicosities are placed on the
DSGC per the Briggman et al. 2011 connectome (minimum offset 30 um between SAC soma and contact),
and each varicosity co-releases ACh + GABA with a correlated AR(2) (phi = [0.9, -0.1]) Gaussian
noise process, correlation peak 0.6. Moving-bar stimuli span 8 directions at 1 mm/s using a 250 um
bar width; DSI is computed as the normalized vector sum of spike counts. Simulations run at 36.9 C
with dt = 0.1 ms. E/I noise is cross-validated against Cafaro and Rieke (2010) oscillating
voltage-clamp statistics, and GABA is scaled 1.8x to compensate for modeled chloride driving force.

## Results

* Correlated ACh/GABA co-release at SAC varicosities yields **DSI 0.39**, whereas uncorrelated
  release collapses DSI to **0.25** (about 36 percent reduction) without changing somatic E/I
  envelopes.
* Ambenonium (AMB) broadens the effective ACh spatial footprint with a decay constant of **tau 27
  um**, degrading DS locally in subunits adjacent to the pipette while sparing subunits over 100 um
  away.
* Global somatic E/I ratio remains unchanged under AMB (p > 0.05), yet subcellular dendritic Ca2+ DS
  tuning falls significantly, direct evidence that global E/I is not a sufficient readout of circuit
  computation.
* Modeled SAC to DSGC circuit requires **1.8x GABA conductance scaling** to match the empirically
  observed I:E ratio given the model chloride reversal and shunting dynamics.
* AR(2) noise with phi = [0.9, -0.1] and peak cross-channel correlation **0.6** reproduces the
  Cafaro-Rieke (2010) E/I noise correlation spectrum measured in real DSGCs.
* Bipolar-cell glutamatergic drive remains non-directional (tuning index near 0) while cholinergic
  drive, though untuned globally, is **locally DS-tuned** at subunit scale, confirming the hidden
  microarchitecture hypothesis.
* Peak synaptic conductances used: **ACh 140.85 pS, GABA 450.72 pS, NMDA 140.85 pS** per varicosity;
  341 sections; Hodgkin-Huxley Na/K active in soma and primary dendrites only.

## Innovations

### Connectome-Constrained Single-Synapse DSGC Network Model

The model is the first, to our knowledge, to place each SAC varicosity on a reconstructed DSGC using
the Briggman et al. 2011 connectome and co-release correlated ACh + GABA at single-synapse
resolution. Prior DSGC models collapsed SAC input into a handful of lumped compartments; this work
resolves over 1000 individual release sites.

### Subcellular vs Global E/I Decoupling

The paper introduces a precise conceptual and quantitative distinction between global E/I (somatic
recordings) and subcellular E/I (dendritic microdomains). By showing these can dissociate under AMB,
the authors establish that somatic E/I is an insufficient summary statistic for DS circuits.

### AR(2)-Driven Correlated Release Noise

Release-rate noise at each varicosity uses an autoregressive AR(2) Gaussian process with phi =
[0.9, -0.1] and cross-transmitter correlation 0.6, calibrated against Cafaro and Rieke (2010)
oscillating voltage-clamp data. This yields realistic E/I noise spectra that earlier models lacked.

### Quantitative AChE-Block Phenotype

The AMB decay constant tau 27 um and the correlated-vs-uncorrelated DSI contrast (0.39 vs 0.25)
provide crisp numerical targets that downstream reimplementations and in vivo studies can use.

## Datasets

* **Two-photon Ca2+ imaging**: mouse (C57BL/6J) ON-OFF DSGCs, whole-mount retina, 16-32 dendritic
  subunits per cell, moving-bar stimuli at 8 directions, 1 mm/s, 250 um bar width. Conditions:
  control and AMB (1-10 uM local puff).
* **Briggman et al. 2011 connectome**: serial block-face EM reconstruction of mouse retina used to
  place SAC varicosities on the DSGC; publicly available.
* **Cafaro and Rieke (2010) oscillating voltage-clamp dataset**: used to calibrate E/I noise
  cross-correlations in the model.
* **Model code and parameters**: deposited at Zenodo (DOI 10.5281/zenodo.17666158) and GitHub
  (`geoffder/ds-circuit-ei-microarchitecture`); includes NEURON HOC morphology, MOD files
  (`HHst_noiseless.mod`, `cadecay.mod`, `Exp2NMDA.mod`), and Python simulation driver.
* No new publicly released imaging dataset is mentioned; source data are provided with the paper.

## Main Ideas

* **Port the SAC to DSGC microarchitecture faithfully.** Preserving single-varicosity ACh+GABA
  co-release (not lumped compartments) is essential; reducing granularity destroys the subcellular
  E/I decoupling that drives the result.
* **Adopt the AR(2) correlated noise model.** Replacing independent Poisson release with the AR(2)
  phi = [0.9, -0.1] and rho = 0.6 cross-correlation reproduces realistic E/I fluctuation statistics
  and is required for DSI to match experiment.
* **Treat DSI = 0.39 (correlated) vs DSI = 0.25 (uncorrelated) as the benchmark.** Any
  reimplementation must hit the correlated DSI 0.39 baseline and recover the 36 percent DSI drop
  under decorrelation or AMB-style ACh spreading.
* **Do not add a Nav1.6/Nav1.2 AIS split.** The deRosenroll model uses only `HHst_noiseless` on
  soma/primary dendrites with no dedicated axon section. Adding AIS kinetics would diverge from the
  source and is unnecessary for this port.
* **Log both paper-text and code-repository parameter values.** Discrepancies in Ra (100 vs 200),
  eleak (-60 vs -65), and Na/K densities between the published figures and the deposited code must
  be tracked explicitly; the code values are authoritative for the port.

## Summary

deRosenroll et al. investigate how the retinal direction-selective circuit, comprising starburst
amacrine cells (SACs) and downstream direction-selective ganglion cells (DSGCs), achieves robust
direction tuning despite the fact that its synaptic inputs (ACh, GABA, glutamate) are arranged in
ways that, globally, appear insufficient to explain strong DS. The authors combine two-photon Ca2+
imaging with a biophysically detailed compartmental network model to test whether the subcellular
spatial organization of co-released ACh and GABA from SACs carries DS information that is invisible
to somatic electrophysiology.

Methodologically, the study has two tightly coupled arms. Experimentally, they use local application
of the AChE blocker ambenonium to broaden ACh diffusion footprint and measure dendritic DSI in
individual Ca2+ subunits. Computationally, they build a NEURON model of a single reconstructed DSGC
(341 sections) receiving approximately 1000 SAC varicosities positioned per the Briggman 2011
connectome, each co-releasing ACh + GABA with AR(2) correlated release-rate noise calibrated to
Cafaro-Rieke 2010 voltage-clamp data. Passive and active properties, synaptic kinetics (ACh Exp2Syn
0.5/6 ms, GABA 0.5/35 ms, NMDA Exp2NMDA 2/80 ms), and a 1.8x GABA scaling factor are fully specified
in the deposited Zenodo/GitHub repository.

The headline results are that broadening ACh spread under AMB degrades dendritic-subunit DS locally
while leaving global somatic E/I intact, and that the model reproduces this phenotype only when SAC
release is locally correlated. Quantitatively, correlated co-release yields DSI around 0.39 whereas
uncorrelated (or AMB-broadened, tau 27 um) release collapses DSI to around 0.25. Globally untuned
ACh is, at subunit scale, locally DS-tuned, the hidden microarchitecture.

For this project, the paper is the direct source of truth: it defines the morphology, channel set
(`HHst_noiseless`, `cadecay`, `Exp2NMDA`, `Exp2Syn`), synaptic weights, noise process, stimulus
protocol, and DSI metric that the port must reproduce. Critically, the model contains no explicit
axon initial segment and does not use Nav1.6/Nav1.2 kinetics, which simplifies the port and resolves
an open question from the research_papers.md gap list. The benchmark DSI values (0.39 correlated vs
0.25 uncorrelated) and the AMB decay constant (tau 27 um) provide the quantitative targets against
which our NEURON reimplementation will be validated. Remaining ambiguities are confined to small
parameter discrepancies between the paper text and the repository code, which will be handled by
adopting the repository values and flagging the paper-text alternatives in the plan.
