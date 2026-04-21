---
spec_version: "1"
task_id: "t0024_port_de_rosenroll_2026_dsgc"
research_stage: "papers"
papers_reviewed: 16
papers_cited: 15
categories_consulted:
  - "compartmental-modeling"
  - "direction-selectivity"
  - "retinal-ganglion-cell"
  - "voltage-gated-channels"
  - "dendritic-computation"
  - "synaptic-integration"
date_completed: "2026-04-21"
status: "complete"
---
# Research Papers: Port de Rosenroll 2026 DSGC

## Task Objective

Port de Rosenroll et al. 2026 (Cell Reports, `10.1016/j.celrep.2025.116833`) into the project as a
third DSGC library asset with modern ion channels (Nav1.6 / Nav1.2 AIS split, updated Kv / Cav), and
evaluate it with the same 12-angle moving-bar protocol used in t0022 and t0023. Corpus evidence must
pin channel densities, AIS geometry, synaptic conductances, and the target tuning envelope before
implementation begins, since the de Rosenroll PDF was not retrievable at the start of this step (see
`10.1016_j.celrep.2025.116833/details.json` `download_failure_reason`); that gap is now closed by
the manually-uploaded PDF handled in research-internet.

## Category Selection Rationale

Six categories from `meta/categories/` are directly relevant. `direction-selectivity` and
`retinal-ganglion-cell` together cover the DSGC-specific papers (Taylor 2000, Schachter 2010,
Poleg-Polsky 2016, Hanson 2019, Poleg-Polsky 2026, Sivyer 2010, Koren 2017) that define the target
envelope, synaptic architecture, and protocol conventions. `compartmental-modeling` and
`voltage-gated-channels` cover the channel-biophysics priors (Fohlmeister-Miller 1997, Fohlmeister
2010, Van Wart 2007, Kole 2008, Kole-Letzkus 2007, Hu 2009, Werginz 2020, Dhingra 2004) needed to
parameterise the Nav1.6 / Nav1.2 AIS split, Kv1.2 distal microdomain, and modern Kv / Cav set.
`dendritic-computation` and `synaptic-integration` surfaced Schachter 2010 local-spike thresholds
and Hanson 2019 E / I offsets used as sanity checks. Unrelated categories (`cable-theory`,
`patch-clamp`) were scanned for relevance but their indexed papers duplicate content already covered
by the six selected categories.

## Key Findings

### DS Protocol Conventions (Parameter-Swap vs Spatial Rotation)

Direction selectivity in Poleg-Polsky-lineage DSGC models is driven by swapping the `gabaMOD` scalar
between preferred (0.33) and null (0.99) trials, not by rotating the bar in space. t0008 reached
only DSI 0.316 using spatial rotation on ModelDB 189347; t0020 reached DSI 0.784 on the same
geometry with the native parameter-swap [PolegPolsky2016]. [Hanson2019] methods prescribe a
sigmoidal GABA release probability `Pr` from ~0.5 (null) to ~0.012 (preferred) plus a fixed
cholinergic `Pr = 0.5`. The standard DSI metric is `DSI = (R_PD - R_ND) / (R_PD + R_ND)`
[Schachter2010, PolegPolsky2016, Hanson2019]. [Hanson2019] uses a normalised vector sum over 8
directions; t0022 extends to 12.

### Nav1.6 / Nav1.2 AIS Split Priors

[VanWart2006] establishes that rodent RGC axon initial segments contain a Nav1.1-enriched proximal
microdomain spatially segregated from a Nav1.6-enriched distal microdomain, with Kv1.2 present only
in the distal microdomain. [Werginz2020] quantifies the AIS-to-soma Na density ratio at
approximately 7x and names AIS length as the dominant morphological predictor of both maximum
sustained firing rate and depolarisation-block threshold. [Kole2008] and [Hu2009] support the Nav1.6
/ Nav1.2 split qualitatively for cortical neurons (Nav1.6 distal, Nav1.2 proximal, Nav1.6 drives AP
initiation and backpropagation threshold) but their exact numeric kinetic parameters (V_half, tau,
slope) are not in the current corpus and must be fetched during research-internet. [KoleLetzkus2007]
demonstrates that AIS Kv1 channels control spike waveform and synaptic efficacy.

### Modern Kv / Cav Formulations for Retinal Neurons

[Fohlmeister2010] provides a temperature-calibrated five-channel set (Na, K_DR, Ca, K_A, K_Ca) with
per-compartment G-bar tables and Q10s (kinetic ~1.95, permeability ~1.6 between 23 and 37 degrees
C); the rate constants derive from [FohlmeisterMiller1997]. The published Fohlmeister rat Type I
densities (dendrite / soma / IS / TS / axon, mS/cm^2, 35 C) are: Na 79.5 / 72.0 / 141.1 / 231.1 /
124; K_DR 23.4 / 50.4 / 67.8 / 74.6 / 50; Ca 1.2 / 1.2 / 0.753 / 0 / 0; K_A approximately 36 on soma
and dendrites. Peak axonal Na reaches 448.5 mS/cm^2 in cat alpha cells on a thin segment 50-130 um
distal to the soma.

### Quantitative Envelope Targets

Target envelope from t0004 `metrics.json`: DSI 0.8824, HWHM 68.51 deg. Prior ports on the same
ModelDB 189347 geometry: t0008 (spatial-rotation proxy) DSI 0.316; t0020 (parameter-swap) DSI 0.784.
[Hanson2019] conductance set (soma / primary dendrite / terminal dendrite): Na 150 / 150 / 30, K
rectifier 70 / 70 / 35, delayed rectifier 3 / 0.8 / 0.4 mS/cm^2; Cm 1 uF/cm^2, Ra 100 Ohm cm, E_leak
-60 mV. [Schachter2010] dendritic Na is 40 mS/cm^2 uniform (or 45 -> 20 gradient), somatic Na 150
mS/cm^2; Oesch-derived compound synaptic conductances are g_exc 6.5 / g_inh 3.5 nS (PD) vs 2.5 / 6.0
nS (ND); local spike threshold drops from 3-4 nS proximal to ~1 nS distal; inhibition of 4-10 nS
blocks initiation and ~85 nS is required to block propagation.

### Synaptic Architecture and E / I Timing

[PolegPolsky2016] equips the reconstructed DRD4 DSGC (ModelDB 189347) ON dendrites with 177 AMPA +
177 NMDA + 177 GABA_A synapses; NMDA-receptor block reduces PD PSPs by ~35 % and ND PSPs by ~34 %
(multiplicative), and requires Mg2+ block. [Hanson2019] E / I offset: excitation leads inhibition by
~50 ms in PD and 0 ms in ND; there is a fixed 25-30 um spatial offset between ACh and GABA release
sites across bar velocities from 500 to 2400 um/s; hexamethonium delays the PD EPSC onset by 26 +/-
2 ms. [Sivyer2010] corroborates velocity-tuning timing. [Koren2017] adds cross-compartmental
modulation of dendritic signals as a secondary DS mechanism.

### de Rosenroll 2026 Headline and Independent Cross-Check

[deRosenroll2026] headline (from the paper's public abstract and figures): perturbation of ACh via
AChE block preserves whole-cell E / I balance but collapses subunit-level DSI. Exact quantitative
drops are not in the corpus and must be extracted from the uploaded PDF in research-internet.
[PolegPolsky2026] provides an independent 352-segment ON-OFF DSGC in NEURON 8.2 + Python showing
that DSI above 0.5 is achievable via velocity-coincidence, passive delay lines, or NMDA
multiplicative gating alone, independent of SAC inhibition; this is a useful null-model cross-check
for the de Rosenroll port. [Dhingra2004] sets the spike-generator efficiency ceiling.

## Methodology Insights

Adopt the Hanson / de Rosenroll parameter-swap protocol (GABA Pr PD = 0.33, ND = 0.99; ACh Pr fixed
0.5) and reject the t0008 spatial-rotation proxy, which demonstrably under-shoots DSI by ~0.5 units
on the same geometry [PolegPolsky2016, Hanson2019]. Build the channel library in two layers: a
Fohlmeister 2010 five-channel set (Na, K_DR, Ca, K_A, K_Ca) with Table-1 G-bar maps and Q10 scaling
as the non-AIS default [Fohlmeister2010, FohlmeisterMiller1997], then overlay a two-subsegment AIS
(proximal Nav1.2 / Nav1.1, distal Nav1.6 + Kv1.2, AIS-to-soma Na ratio ~7x) following
[VanWart2006, Werginz2020]; keep dendritic Na in the Schachter range (40 mS/cm^2 uniform, or 45 ->
20 gradient) [Schachter2010]. Evaluate on the same 12-angle moving-bar sweep as t0022 with 20 trials
per angle; report whole-cell DSI, HWHM, and subunit-level DSI separately, because the de Rosenroll
headline is that AChE block dissociates whole-cell from subunit DSI and a single scalar will obscure
the port's correctness. Use the 26 ms hexamethonium-induced EPSC delay and the 25-30 um ACh / GABA
spatial offset as held-out sanity checks that must reproduce without retuning [Hanson2019].

## Gaps and Limitations

The corpus does not contain the quantitative AChE-block DSI drops from [deRosenroll2026] itself, nor
numeric V_half / tau / slope parameters for Nav1.6 and Nav1.2 from [Kole2008] and [Hu2009]
(CrossRef-only entries in the corpus), nor the Kv1.2 AIS density from [KoleLetzkus2007]. MOD-file
parameter values for the companion repository `geoffder/ds-circuit-ei-microarchitecture` (Zenodo
10.5281/zenodo.17666158) are also missing. All four gaps are flagged for research-internet, where
the manually-uploaded PDF, the Zenodo archive, and the GitHub repo will be read directly. No paper
corpus entry quantifies whole-cell-vs-subunit DSI dissociation magnitude.

## Recommendations for This Task

Start implementation from the Hanson 2019 conductance recipe and overlay a two-subsegment AIS
parameterised from Van Wart 2007 and Werginz 2020; use the Fohlmeister 2010 channel set as the
non-AIS default and drive with the parameter-swap protocol, not spatial rotation. Cross-check
against (a) the t0020 Poleg-Polsky parameter-swap envelope (DSI 0.784) and (b) the t0004 target (DSI
0.8824 / HWHM 68.51 deg); expect the de Rosenroll port to match or slightly exceed the
Hanson-lineage DSI thanks to the ACh spatial offset plus the Nav1.6-driven AIS. Treat the 26 ms
HEX-induced EPSC delay, the 25-30 um E / I offset, and the ~85 nS propagation-block threshold as
held-out validation targets that must hold without retuning.

## Paper Index

### deRosenroll2026

* **Title**: Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective
  circuit
* **Authors**: de Rosenroll, Awatramani et al.
* **Year**: 2026
* **DOI**: `10.1016/j.celrep.2025.116833`
* **Asset path**:
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/`
* **Categories**: direction-selectivity, retinal-ganglion-cell, synaptic-integration
* **Relevance**: Primary source for this port; headline is the AChE-block whole-cell-vs-subunit DSI
  dissociation.

### PolegPolsky2016

* **Title**: NMDA Receptors Multiplicatively Scale Visual Signals and Enhance Directional Motion
  Discrimination in Retinal Ganglion Cells
* **Authors**: Poleg-Polsky, Diamond
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.02.013`
* **Asset path**: `tasks/t0001_download_first_papers/assets/paper/10.1016_j.neuron.2016.02.013/`
* **Categories**: direction-selectivity, retinal-ganglion-cell, synaptic-integration
* **Relevance**: ModelDB 189347 geometry and AMPA / NMDA / GABA_A architecture; parameter-swap
  protocol source.

### Hanson2019

* **Title**: Retinal direction selectivity in the absence of asymmetric starburst amacrine cell
  responses
* **Authors**: Hanson, Awatramani et al.
* **Year**: 2019
* **DOI**: `10.7554/eLife.42392`
* **Asset path**: `tasks/t0001_download_first_papers/assets/paper/10.7554_eLife.42392/`
* **Categories**: direction-selectivity, retinal-ganglion-cell, synaptic-integration
* **Relevance**: GABA Pr sigmoid PD / ND, fixed ACh Pr, E / I timing offset, 26 ms HEX delay,
  conductance recipe.

### PolegPolsky2026

* **Title**: Machine learning discovers numerous new computational principles underlying direction
  selectivity in the retina
* **Authors**: Poleg-Polsky et al.
* **Year**: 2026
* **DOI**: `10.1038/s41467-026-70288-4`
* **Asset path**: `tasks/t0003_download_polegpolsky_2026/assets/paper/10.1038_s41467-026-70288-4/`
* **Categories**: direction-selectivity, retinal-ganglion-cell, compartmental-modeling
* **Relevance**: Independent 352-segment DSGC baseline; velocity-coincidence / NMDA null models.

### Schachter2010

* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, Oesch, Taylor, Werblin
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset path**: `tasks/t0002_second_wave_papers/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: direction-selectivity, dendritic-computation, compartmental-modeling
* **Relevance**: Dendritic / somatic Na densities, compound PD / ND conductances, local-spike
  thresholds, ~85 nS propagation-block threshold.

### Taylor2000

* **Title**: Dendritic Computation of Direction Selectivity by Retinal Ganglion Cells
* **Authors**: Taylor, He, Levick, Vaney
* **Year**: 2000
* **DOI**: `10.1126/science.289.5488.2347`
* **Asset path**: `tasks/t0002_second_wave_papers/assets/paper/10.1126_science.289.5488.2347/`
* **Categories**: direction-selectivity, dendritic-computation
* **Relevance**: Foundational dendritic-DS hypothesis; sets the subunit-thresholding frame.

### Fohlmeister2010

* **Title**: Mechanisms and Distribution of Ion Channels in Retinal Ganglion Cells: Using
  Temperature as an Independent Variable
* **Authors**: Fohlmeister, Cohen, Newman
* **Year**: 2010
* **DOI**: `10.1152/jn.00123.2009`
* **Asset path**: `tasks/t0005_fohlmeister_ion_channel_papers/assets/paper/10.1152_jn.00123.2009/`
* **Categories**: compartmental-modeling, voltage-gated-channels, retinal-ganglion-cell
* **Relevance**: Five-channel set, per-compartment G-bar table, temperature Q10s for non-AIS
  default.

### FohlmeisterMiller1997

* **Title**: Mechanisms by Which Cell Geometry Controls Repetitive Impulse Firing in Retinal
  Ganglion Cells
* **Authors**: Fohlmeister, Miller
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **Asset path**:
  `tasks/t0005_fohlmeister_ion_channel_papers/assets/paper/10.1152_jn.1997.78.4.1948/`
* **Categories**: compartmental-modeling, voltage-gated-channels
* **Relevance**: Rate-constant derivations feeding the 2010 temperature calibration.

### Werginz2020

* **Title**: Tailoring of the axon initial segment shapes the conversion of synaptic inputs into
  spiking output in OFF-alpha T retinal ganglion cells
* **Authors**: Werginz et al.
* **Year**: 2020
* **DOI**: `10.1126/sciadv.abb6642`
* **Asset path**: `tasks/t0006_ais_papers/assets/paper/10.1126_sciadv.abb6642/`
* **Categories**: retinal-ganglion-cell, voltage-gated-channels, compartmental-modeling
* **Relevance**: AIS-to-soma Na ratio ~7x; AIS length as dominant predictor of firing rate and
  depolarisation block.

### VanWart2006

* **Title**: Polarized distribution of ion channels within microdomains of the axon initial segment
* **Authors**: Van Wart, Trimmer, Matthews
* **Year**: 2007
* **DOI**: `10.1002/cne.21173`
* **Asset path**: `tasks/t0006_ais_papers/assets/paper/10.1002_cne.21173/`
* **Categories**: retinal-ganglion-cell, voltage-gated-channels
* **Relevance**: Nav1.1-proximal / Nav1.6-distal microdomain split; Kv1.2 in distal microdomain
  only.

### Kole2008

* **Title**: Action potential generation requires a high sodium channel density in the axon initial
  segment
* **Authors**: Kole et al.
* **Year**: 2008
* **DOI**: `10.1038/nn2040`
* **Asset path**: `tasks/t0006_ais_papers/assets/paper/10.1038_nn2040/`
* **Categories**: voltage-gated-channels, compartmental-modeling
* **Relevance**: Qualitative AIS Na-density argument (CrossRef-only entry; numbers needed via
  research-internet).

### KoleLetzkus2007

* **Title**: Axon Initial Segment Kv1 Channels Control Axonal Action Potential Waveform and Synaptic
  Efficacy
* **Authors**: Kole, Letzkus, Stuart
* **Year**: 2007
* **DOI**: `10.1016/j.neuron.2007.07.031`
* **Asset path**: `tasks/t0006_ais_papers/assets/paper/10.1016_j.neuron.2007.07.031/`
* **Categories**: voltage-gated-channels, synaptic-integration
* **Relevance**: AIS Kv1 control of spike waveform; Kv1.2 density needed via research-internet.

### Hu2009

* **Title**: Distinct contributions of Nav1.6 and Nav1.2 in action potential initiation and
  backpropagation
* **Authors**: Hu, Tian, Li, Shu, Yu
* **Year**: 2009
* **DOI**: `10.1038/nn.2359`
* **Asset path**: `tasks/t0006_ais_papers/assets/paper/10.1038_nn.2359/`
* **Categories**: voltage-gated-channels, compartmental-modeling
* **Relevance**: Nav1.6-distal / Nav1.2-proximal functional split (CrossRef-only; kinetic parameters
  needed via research-internet).

### Sivyer2010

* **Title**: Synaptic inputs and timing underlying the velocity tuning of direction-selective
  ganglion cells in rabbit retina
* **Authors**: Sivyer, Williams
* **Year**: 2010
* **DOI**: `10.1113/jphysiol.2010.192716`
* **Asset path**: `tasks/t0002_second_wave_papers/assets/paper/10.1113_jphysiol.2010.192716/`
* **Categories**: direction-selectivity, synaptic-integration
* **Relevance**: Velocity-tuning timing data corroborating Hanson E / I offsets.

### Koren2017

* **Title**: Cross-compartmental Modulation of Dendritic Signals for Retinal Direction Selectivity
* **Authors**: Koren et al.
* **Year**: 2017
* **DOI**: `10.1016/j.neuron.2017.07.020`
* **Asset path**: `tasks/t0002_second_wave_papers/assets/paper/10.1016_j.neuron.2017.07.020/`
* **Categories**: direction-selectivity, dendritic-computation
* **Relevance**: Secondary cross-compartmental DS mechanism.

### Dhingra2004

* **Title**: Spike Generator Limits Efficiency of Information Transfer in a Retinal Ganglion Cell
* **Authors**: Dhingra, Smith
* **Year**: 2004
* **DOI**: `10.1523/jneurosci.5346-03.2004`
* **Asset path**: `tasks/t0002_second_wave_papers/assets/paper/10.1523_jneurosci.5346-03.2004/`
* **Categories**: retinal-ganglion-cell, voltage-gated-channels
* **Relevance**: Spike-generator efficiency ceiling for sanity-checking firing rates.
