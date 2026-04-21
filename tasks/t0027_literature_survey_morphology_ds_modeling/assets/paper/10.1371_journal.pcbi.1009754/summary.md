---
spec_version: "3"
paper_id: "10.1371_journal.pcbi.1009754"
citation_key: "Ezra-Tsur2021"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# Realistic retinal modeling unravels the differential role of excitation and inhibition to starburst amacrine cells in direction selectivity

## Metadata

* **File**: `files/ezra-tsur_2021_morphology-direction-selective.pdf`
* **Published**: 2021-12-30
* **Authors**: Elishai Ezra-Tsur IL, Oren Amsalem IL, Lea Ankri IL, Pritish Patil IL, Idan Segev IL,
  Michal Rivlin-Etzion IL
* **Venue**: PLOS Computational Biology (journal)
* **DOI**: `10.1371/journal.pcbi.1009754`

## Abstract

Retinal direction-selectivity originates in starburst amacrine cells (SACs), which display a
centrifugal preference, responding with greater depolarization to a stimulus expanding from soma to
dendrites than to a collapsing stimulus. Various mechanisms were hypothesized to underlie SAC
centrifugal preference, but dissociating them is experimentally challenging and the mechanisms
remain debatable. To address this issue, we developed the Retinal Stimulation Modeling Environment
(RSME), a multifaceted data-driven retinal model that encompasses detailed neuronal morphology and
biophysical properties, retina-tailored connectivity scheme and visual input. Using a genetic
algorithm, we demonstrated that spatiotemporally diverse excitatory inputs - sustained in the
proximal and transient in the distal processes - are sufficient to generate experimentally validated
centrifugal preference in a single SAC. Reversing these input kinetics did not produce any
centrifugal-preferring SAC. We then explored the contribution of SAC-SAC inhibitory connections in
establishing the centrifugal preference. SAC inhibitory network enhanced the centrifugal preference,
but failed to generate it in its absence. Embedding a direction selective ganglion cell (DSGC) in a
SAC network showed that the known SAC-DSGC asymmetric connectivity by itself produces direction
selectivity. Still, this selectivity is sharpened in a centrifugal-preferring SAC network. Finally,
we use RSME to demonstrate the contribution of SAC-SAC inhibitory connections in mediating direction
selectivity and recapitulate recent experimental findings. Thus, using RSME, we obtained a
mechanistic understanding of SAC centrifugal preference and its contribution to direction
selectivity.

## Overview

**Morphology variable studied.** This paper varies the SAC synaptic input arrangement (the spatial
distribution and temporal kinetics of bipolar-cell excitation along SAC processes, plus the strength
of reciprocal SAC-SAC inhibition) while holding DSGC biophysics and the DSGC own morphology fixed
(passive model built on NeuroMorpho ID NMO_05318 with 1013 compartments). The SAC itself uses a
fixed reconstructed morphology (NMO_139062, 1013 compartments, passive only) and the authors use a
genetic algorithm (GA) to sweep an 8-dimensional input-layout/kinetics parameter space and read out
how SAC centrifugal preference (CSI, RTI) and downstream DSGC direction-selectivity (DSI, PD
activation) depend on where and how inputs land on the dendritic tree.

The paper develops the Retinal Stimulation Modeling Environment (RSME), a NEURON-encapsulating
framework with XML/SBML specification for morphology, biophysics, connectivity, and visual stimuli,
and uses it to probe three nested questions. First, can single-cell input arrangement alone
reproduce the centrifugal preference (CF preference: larger depolarization to soma-to-distal
expanding rings than to distal-to-soma collapsing rings) that is seen experimentally in On-SACs?
Second, does reciprocal SAC-SAC GABAergic inhibition create or merely sharpen CF preference? Third,
when a reconstructed DSGC is embedded in a 13-SAC network with asymmetric null-side wiring, how do
SAC CF preference, SAC-SAC inhibition, and background noise jointly shape DSGC
direction-selectivity?

The headline finding is that spatiotemporally diverse excitation - **sustained proximally and
transient distally** - is sufficient to generate CF preference in a single passive SAC, while
**reversing** this arrangement (transient proximal, sustained distal) produces no CF-preferring SACs
under the same GA. Reciprocal SAC-SAC inhibition **enhances but cannot generate** CF preference, and
**asymmetric SAC-to-DSGC wiring is sufficient** to produce DSGC direction-selectivity even when the
SAC network is not CF-preferring, though CF preference sharpens the tuning and SAC-SAC inhibition
becomes important in the presence of visual noise. The paper thereby dissects which components of
the circuit are necessary versus sufficient for each level of the DS computation.

## Architecture, Models and Methods

**Simulator and framework.** All simulations run in NEURON 7.7 with a 0.025 ms time step,
orchestrated by RSME (available at `https://github.com/NBELab/RSME`). RSME is organized in 5 layers:
meta parameters, visual stimulation, network architecture, cell morphology, and biophysical
properties; biophysical and mathematical rules are declared in XML/SBML. Simulation duration per
trial is 1500 ms.

**SAC cell model.** A single reconstructed On-SAC (NeuroMorpho ID NMO_139062) is discretized into
**1013 compartments**. The cell is **passive only** in this work: cytoplasmic resistivity 75 Ohm.cm,
specific membrane capacitance 1 uF/cm2, passive conductance 0.00006 S/cm2, resting potential -60 mV,
yielding an input resistance of **84 MOhm** (within the experimental range). An ad-hoc morphology
correction halves all section radii to undo a tracing artifact.

**DSGC cell model.** A reconstructed DSGC (NeuroMorpho ID NMO_05318) is instantiated from a
precompiled NEURON .hoc file with **1013 compartments**, same passive parameters as the SAC but
resting potential -52 mV (measured in GABA-A-blocked DSGCs); spiking threshold is set to -49 mV
based on current-clamp measurements from 15/16 DSGCs (151 spikes analysed).

**Bipolar-cell to SAC synapse model.** Exp2Syn with rise/decay 0.89/1.84 ms and 0 mV reversal
potential. Each synapse has a **stochastic vesicle pool** of 70 vesicles with release probability p
and refilling rate r that both vary with distance d from the soma. p and r are parameterized so that
kinetics transition from **sustained near the soma to transient at the distal processes** between
`k_transition_start_point` and `k_transition_end_point`. Synapse density along the process follows a
sigmoid parameterized by proximal density, distal density, `anatomical_transition_point`, and
`scaling_factor`/`offset`.

**8-dimensional GA parameter sweep.** The genetic algorithm (DEAP, 100 individuals, 20-45
generations, crossover/mutation probability 0.4) searches: refilling rate (0.01-1 vesicles/ms),
release probability (0.01-0.75), kinetic transition start (0.01-0.5 of dendritic length), kinetic
transition end (2-210 um), synaptic conductance (0.0001-0.2 nS), anatomical transition point (2-210
um), scaling factor (0.01-0.4), and offset (0.1-0.99). GA objectives maximize (1) Amp(CF)-Amp(CP)
with weight 1.0, (2) RT(CP)-RT(CF) with weight 0.3, (3) a penalty keeping peak voltage below -10 mV
with weight 0.08. Three selection algorithms (NSGA-II, IBEA, and rank-based) are compared; results
are qualitatively identical across six seeds.

**SAC network.** Two overlaid grids (3x3 and 2x2, 125 um spacing, 13 SACs total) surround a central
recorded SAC. Every SAC in a given network receives the same input distribution/kinetics (derived
from one GA-selected individual). SAC-SAC GABAergic synapses (Exp2Syn; rise/decay 3/30 ms; reversal
-75 mV; presynaptic activation at 200 Hz above -50 mV) are placed at process intersections, with
release sites confined to the distal 1/3. 76 networks are built from GA-selected CF-preferring SACs;
conductance is swept from 0 to 1 nS.

**Direction-selective circuit.** A reconstructed DSGC is added to the SAC network with asymmetric
SAC-to-DSGC wiring: synapse-formation probability is the inverse cosine of the angle between SAC
process orientation and DSGC preferred direction. SAC-DSGC synapses use 0.5 nS conductance (matching
Wei et al. 2011: ~9 nS total / ~14 contacts) and reversal -60 mV. Stimuli are preferred-direction
vs. null-direction bars (1000 um/s, 250x600 um), with and without 30 randomly flickering 25-um
background spots at 15 Hz. Metrics are **DSI** (area between voltage trace and -60 mV) and **PD
activation** (area above spiking threshold during preferred motion).

**Experimental validation.** Current-clamp recordings from On-SACs (mGluR2-EGFP mice, n=27 cells)
with expanding/collapsing rings (25 um soma mask, 450 um/cycle, 2 Hz, 900 um/s) and from DSGCs
(Trhr-EGFP mice) with moving bars. Observed CSI = 0.18 +/- 0.17 and RTI = 0.33 +/- 0.22 (mean +/-
STD) are the experimental targets the simulations try to match. Simulations ran on a Blue Brain V
HPC (Intel Xeon 6140, 384 GB) for the GA; single-SAC run time 70.66 s, SAC-network 421.47 s, full
DSGC circuit 492.36 s after precompilation.

## Results

* With the **natural spatiotemporal arrangement** (sustained excitation proximal, transient distal)
  the GA converges on multiple parameter sets that reproduce experimentally measured CF preference;
  the sustained-transient index drops steeply around the mid-dendrite by generation 45 and its
  midpoint converges to **0.5** (Fig 3E-G).
* With the **reversed arrangement** (transient proximal, sustained distal) **0 CF-preferring SACs**
  are found; some simulated SACs even display a slight centripetal preference. When kinetics are
  held **fixed** across the dendrite, only **4 of 2125** simulated SACs barely cross the CF
  inclusion threshold.
* Over 76 SAC networks, **SAC-SAC reciprocal inhibition modulates CF preference non-monotonically**:
  CSI rises moderately up to ~0.1 nS then declines in a subset of cells at >0.1 nS (those with
  denser distal excitation); RTI rises monotonically and plateaus near **0.1 nS** (Fig 5C-F). Sparse
  distal excitatory density is needed to keep CSI positive under strong inhibition.
* For 12 non-CF-preferring SACs and 10 reversed-kinetics SACs, **adding reciprocal inhibition at any
  strength fails to generate CF preference**; some cells develop negative CSI and RTI (Figs S8,
  5G-I).
* At the DSGC level, **random SAC-to-DSGC wiring produces no direction-selectivity** (DSI ~ 0; Fig
  6A); enforcing the **asymmetric null-side rule** produces positive DSI even in the absence of
  SAC-SAC inhibition (Fig 6C, left).
* Adding SAC-SAC inhibition (0.1 nS) on a **noiseless background** slightly increases DSGC DSI and
  PD activation; on a **noisy background** (flickering 15 Hz spots) SAC-SAC inhibition produces a
  **substantially larger DSI gain** (Fig 6D-E), reproducing the Chen et al. 2020 short-term
  depression rescue mechanism.
* With a **non-CF SAC network** plus asymmetric wiring, DSGCs **retain direction-selectivity**
  (reduced magnitude) - consistent with Hanson et al.; reciprocal inhibition has little effect in
  this regime because it cannot generate CF preference from scratch (Fig 6F).
* In the SAC input-density sweep, the **anatomical transition point** (proximal 1/2-2/3 of dendrites
  carrying denser input) is a necessary but not unique constraint: CF preference also arises with
  inputs confined closer to soma than biology, but biological SACs probably avoid this to maximise
  their excitatory receptive field.
* Somatic and distal-dendritic voltage traces closely track each other in CF preference and
  amplitude (small delay of a few ms across 5 recording sites; Fig 4, n=68 cells).

## Innovations

### RSME: morphology-first retinal circuit simulator

RSME is a NEURON-based framework with XML/SBML-parsed specifications for visual stimuli, network
architecture, reconstructed morphology, and biophysics. It supports grid/mosaic placement,
connectivity rules based on process intersections, and light/dark-activated synapses that can stand
in for photoreceptor+bipolar stacks. The whole framework is open-source on GitHub with a companion
GitBook, which is unusual at this level of retina-specific detail.

### Genetic-algorithm dissection of an 8-D SAC input parameter space

The paper treats excitatory input layout and kinetics as an explicit 8-dimensional design space and
uses DEAP/NSGA-II/IBEA to find all parameter combinations consistent with the measured SAC CF
preference. This reframes the question of what input pattern produces CF preference as a
multi-objective optimisation and exposes a robust manifold of valid solutions rather than a single
tuned model.

### Necessity/sufficiency decomposition of the DS circuit

By independently toggling (i) input kinetics direction, (ii) SAC-SAC inhibition strength, (iii)
SAC-to-DSGC wiring rule, and (iv) background noise, the paper constructs a clean decomposition:
input spatiotemporal arrangement is **sufficient** for SAC CF preference; SAC-SAC inhibition is a
**modulator**, not a generator; asymmetric SAC-to-DSGC wiring is **sufficient** for DSGC DS even
without CF preference; SAC-SAC inhibition becomes **important** only under noisy visual conditions.

## Datasets

* **Reconstructed On-SAC morphology**: NeuroMorpho.org ID **NMO_139062** (used for the single-SAC
  model and replicated 13x in network simulations).
* **Reconstructed DSGC morphology**: NeuroMorpho.org ID **NMO_05318**, provided as a NEURON .hoc
  file (1013 compartments).
* **SAC current-clamp recordings**: n = 27 On-SACs from mGluR2-EGFP mice (Weizmann IACUC-approved),
  combining previously published data from the authors Ankri et al. study with new recordings.
  Measured CSI = 0.18 +/- 0.17, RTI = 0.33 +/- 0.22.
* **DSGC intracellular recordings**: n = 15 DSGCs from Trhr-EGFP mice (posterior-preferring), used
  to set the -52 mV baseline and -49 mV spiking threshold; 151 spikes analysed.
* **Simulation output**: three supporting-information ZIP bundles are released (S1_EphysData,
  S2_DSGC_simulation, S3_GA_SingleSAC_and_Network). All data are open access.

## Main Ideas

* **The input-on-dendrite layout is the primary causal variable for SAC CF preference.** A sweep of
  the spatial density profile and temporal kinetics of bipolar-to-SAC synapses on a fixed passive
  SAC morphology is sufficient to reproduce measured CSI/RTI; reversing the kinetics pattern
  eliminates CF preference entirely. For this project, this is a textbook example of an
  input-layout-varied, biophysics-fixed compartmental DS study and should be cited as a direct
  precedent.
* **Morphology-fixed DSGC sweeps can still recover direction-selectivity solely from asymmetric
  wiring.** A single reconstructed DSGC with passive properties and 1013 compartments, when driven
  by a SAC network with the correct null-side wiring rule, produces positive DSI even without any
  SAC CF preference. This supports the project inclusion criterion that input-on-dendrite layout
  varied as a causal variable is a valid design pattern for morphology-to-DS modelling.
* **Reciprocal inhibition is a context-dependent modulator, not a generator.** Projects that omit
  SAC-SAC inhibition can still obtain DS; those that include it should also include visual noise to
  see the effect. For any follow-up modelling work the paper pins down the optimal SAC-SAC
  conductance (~0.1 nS) and the 20-contacts-per-pair assumption.
* **Specific numerical anchors to reuse**: 1013 compartments for both SAC and DSGC, 84 MOhm input
  resistance, -49 mV spiking threshold, -52 mV DSGC baseline, 0.1 nS SAC-SAC, 0.5 nS SAC-DSGC,
  Exp2Syn rise/decay 0.89/1.84 ms (BP-SAC) and 3/30 ms (SAC-SAC), 1500 ms simulation duration.
* **Release the code and morphologies.** RSME, morphologies (NeuroMorpho 139062 and 05318), and
  simulation data are all public - this paper is directly reproducible and should be attempted as a
  baseline before building new morphology-varying DS models in this project.

## Summary

Ezra-Tsur and colleagues attack a long-standing problem in retinal computation: determining which of
several competing mechanisms (input layout, input kinetics, intrinsic ion channels, reciprocal
inhibition) produces the centrifugal preference of SAC dendrites that, in turn, drives direction
selectivity in DSGCs. Because these mechanisms are experimentally difficult to isolate, the authors
build RSME - a NEURON-encapsulating framework that ties together detailed morphology, biophysics,
retinal connectivity rules, and visual stimuli - and use it as a counterfactual engine.

The methodological core is a genetic-algorithm sweep over an 8-dimensional parameter space that
controls the spatial density of bipolar-to-SAC synapses and the per-synapse release kinetics,
holding the passive SAC morphology (1013-compartment NeuroMorpho NMO_139062) fixed. By varying only
the input-on-dendrite layout the authors show that spatiotemporally diverse excitation - sustained
proximal, transient distal - is sufficient to reproduce experimentally measured CSI (~0.18) and RTI
(~0.33); reversing the arrangement eliminates CF preference (0/N cells), and fixing it gives 4/2125
barely-CF cells. In a subsequent 13-SAC network, reciprocal inhibition modulates but does not
generate CF preference, peaking at ~0.1 nS.

The DSGC results are the most load-bearing for this project morphology-focused survey: embedding a
reconstructed DSGC (NMO_05318, 1013 compartments, passive, -49 mV threshold, -52 mV baseline) in the
SAC network and flipping between random and asymmetric null-side SAC-to-DSGC wiring shows that
asymmetric wiring alone produces positive DSI and PD activation, even when the SAC network has no CF
preference. SAC-SAC inhibition improves DSI modestly under noiseless stimuli and strongly under
noisy stimuli - reproducing the Chen et al. short-term depression mechanism - while asymmetric
wiring remains necessary throughout. These are specific, quantitative necessity/sufficiency claims.

For this project on computational models linking neuronal morphology to direction-selectivity, the
paper is a clear inclusion: it uses compartmental models with explicit reconstructed morphology, it
varies the input-on-dendrite layout (and separately the SAC-SAC inhibition strength) as the causal
variable, and it measures DSGC outcome via DSI and related indices. It should be cited as the
canonical RSME reference, and the specific numerical anchors (compartment counts, conductances,
Exp2Syn parameters, 0.1 nS SAC-SAC, 0.5 nS SAC-DSGC, spiking threshold -49 mV) should be reused as
starting points or baselines in any follow-up morphology-sweep tasks that embed a DSGC in a SAC
network. A limitation is that SACs are passive-only (no ion channels), so claims about the role of
SAC intrinsic properties versus input layout are by construction bounded - this is explicitly
acknowledged in the Discussion, and the authors note RSME can implement active channels in future
studies.
