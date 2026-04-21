# Research Papers: Port de Rosenroll 2026 DSGC

## Objective

Port de Rosenroll et al. 2026 (Cell Reports, `10.1016/j.celrep.2025.116833`) into the project as a
third DSGC library asset with modern ion channels (Nav1.6/Nav1.2 AIS split, updated Kv/Cav), and
evaluate it with the same 12-angle moving-bar protocol as t0022/t0023. Corpus evidence must fix
channel densities, AIS geometry, synaptic conductances, and target tuning envelope before
implementation begins, because the de Rosenroll PDF itself could not be retrieved (see
`10.1016_j.celrep.2025.116833/details.json` `download_failure_reason`).

## Background

DSGC compartmental modelling descends from two lineages. Taylor 2000 / Schachter 2010 established
postsynaptic dendritic DS via local subunit thresholding plus spatially offset inhibition. The
Awatramani lineage (Poleg-Polsky and Diamond 2016, Hanson et al. 2019, de Rosenroll et al. 2026)
extended the single-inhibition picture to differential SAC->DSGC wiring of GABA, ACh, and
(eventually) a 3-neurotransmitter network in which the subcellular alignment of ACh and GABA release
is itself the DS primitive. de Rosenroll 2026 sits at the end of this lineage: same geometry family
as t0008/t0020/t0022, but with explicit ACh kinetics and a companion NEURON + Python repository
(`geoffder/ds-circuit-ei-microarchitecture`, MIT, Zenodo 10.5281/zenodo.17666157) shipping
`HHst_noiseless.mod`, `Exp2NMDA.mod`, `cadecay.mod`, and `RGCmodelGD.hoc`. Poleg-Polsky 2026 offers
an independent 352-segment ML-search DSGC for cross-checking.

## Methodology Review

* Spatial-rotation vs parameter-swap DS protocols: t0008 reached only DSI 0.316 with rotation; t0020
  reached DSI 0.784 on the same geometry using the native gabaMOD parameter-swap (PD=0.33, ND=0.99).
  Hanson 2019 methods give sigmoidal GABA `Pr` from ~0.5 (null) to ~0.012 (preferred) plus a fixed
  cholinergic `Pr = 0.5`. Adopt parameter-swap; reject rotation as a proxy.
* Nav1.6/Nav1.2 AIS split priors: Van Wart 2007 shows Nav1.1-proximal / Nav1.6-distal microdomains
  in rodent RGC AIS with Kv1.2 only in the distal subsegment. Werginz 2020 quantifies AIS-to-soma Na
  density at approximately 7x and names AIS length the dominant predictor of max firing and
  depolarisation-block threshold. Kole 2008 and Hu 2009 support the split qualitatively; their
  numeric values are not in the corpus and must come via research-internet.
* Modern Kv/Cav formulations for retinal neurons: Fohlmeister 2010 provides a temperature-calibrated
  Five-channel set (Na, K_DR, Ca, K_A, K_Ca) with per-compartment G-bar tables and Q10s (kinetic
  ~1.95, permeability ~1.6 at 23-37 C); rate constants derive from Fohlmeister-Miller 1997. Adopt
  these wholesale and layer Nav1.6/Nav1.2 subunit identities on top of the Fohlmeister Na kinetics.
* Tuning-curve scoring conventions: DSI = (R_PD - R_ND) / (R_PD + R_ND) (Poleg-Polsky 2016,
  Schachter 2010, Hanson 2019). Hanson uses normalised vector-sum over 8 directions; t0022 extends
  to 12. The t0004 target is DSI 0.8824 / HWHM 68.51 deg. Report both whole-cell and subunit-level
  DSI because de Rosenroll shows AChE block preserves whole-cell DSI but collapses subunit DSI.

## Key Findings

* Target envelope (t0004 `metrics.json`): DSI 0.8824, HWHM 68.51 deg. t0008 rotation proxy: DSI
  0.316; t0020 parameter-swap: DSI 0.784.
* Hanson 2019 conductance set (soma / primary dendrite / terminal dendrite): Na 150/150/30, K
  rectifier 70/70/35, delayed rectifier 3/0.8/0.4 mS/cm^2; Cm 1 uF/cm^2, Ra 100 Ohm cm, E_leak -60
  mV.
* Fohlmeister 2010 rat Type I (dendrite/soma/IS/TS/axon, mS/cm^2, 35 C): Na 79.5/72.0/141.1/231.1/
  124; K_DR 23.4/50.4/67.8/74.6/50; Ca 1.2/1.2/0.753/0/0; K_A ~36 on soma/dendrites. Peak axonal Na
  reaches 448.5 mS/cm^2 in cat alpha, on a thin segment 50-130 um distal to the soma.
* Werginz 2020: AIS-to-soma Na density ratio ~7x; AIS length is the dominant morphological predictor
  of max sustained firing rate and depolarisation-block threshold.
* Van Wart 2007: rodent RGC AIS has Nav1.1-enriched proximal microdomain spatially segregated from
  Nav1.6-enriched distal microdomain; Kv1.2 present only in the distal microdomain.
* Schachter 2010: dendritic Na 40 mS/cm^2 uniform (or 45 -> 20 gradient), somatic Na 150 mS/cm^2.
  Oesch-derived compound synaptic conductances: g_exc 6.5 / g_inh 3.5 nS (PD) vs 2.5 / 6.0 nS (ND).
  Local spike threshold drops from 3-4 nS proximal to ~1 nS distal; inhibition of 4-10 nS blocks
  initiation, ~85 nS needed to block propagation.
* Poleg-Polsky 2016 synaptic architecture: 177 AMPA + 177 NMDA + 177 GABA_A on ON dendrites of a
  reconstructed DRD4 DSGC (ModelDB 189347); NMDAR block reduces PD PSPs ~35% / ND PSPs ~34%
  (multiplicative), requires Mg2+ block.
* Hanson 2019 E/I offset: E leads I by ~50 ms in PD, 0 ms in ND; fixed 25-30 um spatial offset
  between ACh and GABA across 500-2400 um/s; hexamethonium delays PD EPSC onset by 26 +/- 2 ms.
* de Rosenroll 2026 headline: AChE-type perturbation of ACh preserves whole-cell E/I balance but
  collapses subunit-level DSI; quantitative drops not in corpus (PDF unavailable) -- flagged for
  research-internet.
* Poleg-Polsky 2026 baseline: 352-segment ON-OFF DSGC in NEURON 8.2 + Python; DSI above 0.5 is
  achievable via velocity-coincidence, passive delay lines, or NMDA multiplicative gating
  independent of SAC inhibition.

## Recommended Approach

* Start from the Hanson 2019 recipe (soma/dendrite Na 150/30, K_DR 70/35, delayed rectifier 3/0.4
  mS/cm^2; Cm 1 uF/cm^2, Ra 100 Ohm cm, E_leak -60 mV) and overlay a two-subsegment AIS (proximal
  Nav1.2/Nav1.1, distal Nav1.6 + Kv1.2, AIS-to-soma Na ratio ~7x) from Van Wart 2007 + Werginz 2020.
* Use the Fohlmeister 2010 Five-channel set with Table-1 G-bar maps and Q10 scaling as the non-AIS
  channel library; keep dendritic Na in the Schachter 2010 range (40 mS/cm^2, or 45 -> 20 gradient).
* Drive with the Hanson / de Rosenroll parameter-swap protocol (GABA Pr PD=0.33, ND=0.99, ACh Pr
  fixed 0.5), not spatial rotation; evaluate on the same 12-angle moving-bar sweep as t0022 and
  report whole-cell and subunit DSI separately.
* Cross-check against (a) Poleg-Polsky-lineage envelope (t0020 DSI 0.784) and (b) the t0004 target
  (DSI 0.8824 / HWHM 68.51 deg). Expect the de Rosenroll port to match or slightly exceed
  Hanson-lineage DSI thanks to the ACh offset plus Nav1.6 AIS.
* Use the 26 ms HEX-induced EPSC delay / 25-30 um E/I offset (Hanson 2019) and the ~85 nS
  propagation-block threshold (Schachter 2010) as sanity checks that must hold without retuning.

## References

* deRosenroll2026, 2026 -- Uncovering the "hidden" synaptic microarchitecture of the retinal
  direction selective circuit (`10.1016_j.celrep.2025.116833`)
* PolegPolsky2016, 2016 -- NMDA Receptors Multiplicatively Scale Visual Signals and Enhance
  Directional Motion Discrimination in Retinal Ganglion Cells (`10.1016_j.neuron.2016.02.013`)
* Hanson2019, 2019 -- Retinal direction selectivity in the absence of asymmetric starburst amacrine
  cell responses (`10.7554_eLife.42392`)
* PolegPolsky2026, 2026 -- Machine learning discovers numerous new computational principles
  underlying direction selectivity in the retina (`10.1038_s41467-026-70288-4`)
* Schachter2010, 2010 -- Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion
  in a Simulation of the Direction-Selective Ganglion Cell (`10.1371_journal.pcbi.1000899`)
* Taylor2000, 2000 -- Dendritic Computation of Direction Selectivity by Retinal Ganglion Cells
  (`10.1126_science.289.5488.2347`)
* Fohlmeister2010, 2010 -- Mechanisms and Distribution of Ion Channels in Retinal Ganglion Cells:
  Using Temperature as an Independent Variable (`10.1152_jn.00123.2009`)
* FohlmeisterMiller1997, 1997 -- Mechanisms by Which Cell Geometry Controls Repetitive Impulse
  Firing in Retinal Ganglion Cells (`10.1152_jn.1997.78.4.1948`)
* Werginz2020, 2020 -- Tailoring of the axon initial segment shapes the conversion of synaptic
  inputs into spiking output in OFF-alpha T retinal ganglion cells (`10.1126_sciadv.abb6642`)
* VanWart2006, 2007 -- Polarized distribution of ion channels within microdomains of the axon
  initial segment (`10.1002_cne.21173`)
* Kole2008, 2008 -- Action potential generation requires a high sodium channel density in the axon
  initial segment (`10.1038_nn2040`)
* KoleLetzkus2007, 2007 -- Axon Initial Segment Kv1 Channels Control Axonal Action Potential
  Waveform and Synaptic Efficacy (`10.1016_j.neuron.2007.07.031`)
* Hu2009, 2009 -- Distinct contributions of Nav1.6 and Nav1.2 in action potential initiation and
  backpropagation (`10.1038_nn.2359`)
* Sivyer2010, 2010 -- Synaptic inputs and timing underlying the velocity tuning of
  direction-selective ganglion cells in rabbit retina (`10.1113_jphysiol.2010.192716`)
* Koren2017, 2017 -- Cross-compartmental Modulation of Dendritic Signals for Retinal Direction
  Selectivity (`10.1016_j.neuron.2017.07.020`)
* Dhingra2004, 2004 -- Spike Generator Limits Efficiency of Information Transfer in a Retinal
  Ganglion Cell (`10.1523_jneurosci.5346-03.2004`)
