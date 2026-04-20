---
spec_version: "3"
paper_id: "10.1016_j.cub.2018.03.001"
citation_key: "Morrie2018"
summarized_by_task: "t0013_resolve_morphology_provenance"
date_summarized: "2026-04-20"
---
# A Dense Starburst Plexus Is Critical for Generating Direction Selectivity

## Metadata

* **File**: `files/morrie_2018_dense-starburst-plexus.pdf`
* **Published**: 2018-04-23 (Curr Biol 28(8): 1204-1212.e5)
* **Authors**: Ryan D. Morrie 🇺🇸, Marla B. Feller 🇺🇸
* **Venue**: Current Biology (Elsevier)
* **DOI**: `10.1016/j.cub.2018.03.001`
* **PMID**: 29606419; PMCID: PMC5916530

## Abstract

Starburst amacrine cell (SAC) morphology is considered central to retinal direction selectivity. In
Sema6A-/- mice, SAC dendritic arbors are smaller and no longer radially symmetric, leading to a
reduction in SAC dendritic plexus density. Sema6A-/- mice also have a dramatic reduction in the
directional tuning of retinal direction-selective ganglion cells (DSGCs). Here we show that the loss
of DSGC tuning in Sema6A-/- mice is due to reduced null direction inhibition, even though strong
asymmetric SAC-DSGC connectivity and SAC dendritic direction selectivity are maintained. Hence, the
reduced coverage factor of SAC dendrites leads specifically to a loss of null direction inhibition.
Moreover, SAC dendrites are no longer strictly tuned to centrifugal motion, indicating that SAC
morphology is critical in coordinating synaptic connectivity and dendritic integration to generate
direction selectivity.

## Overview

The paper dissects which components of the starburst amacrine cell (SAC) to direction-selective
ganglion cell (DSGC) circuit are degraded when SAC morphology is experimentally truncated. Using the
Sema6A-/- mouse, in which SACs develop with smaller, radially asymmetric arbors and therefore a ~50%
reduction in SAC plexus coverage factor, the authors separately probe DSGC directional tuning,
paired SAC-DSGC inhibitory conductances, SAC varicosity Ca2+ directional tuning, and the geometry of
SAC dendrites around each imaged release site. The headline result is a dissociation: asymmetric
SAC-to-DSGC wiring and subcellular SAC varicosity direction selectivity are preserved, yet DSGC
directional tuning collapses because null-direction inhibition is weaker.

Mechanistically, the authors show that SAC varicosities in Sema6A-/- mice are no longer strictly
tuned to centrifugal motion; their directional preference instead follows the orientation of a short
(~10-40 micrometres) distal neurite segment bearing glutamate receptors. The tortuous, misaligned
Sema6A-/- dendrites therefore produce a population of SAC release sites whose preferred directions
are partly misaligned with the SAC-DSGC wiring axis. An IPSC simulation using each reconstructed
SAC's varicosity geometry reproduces the observed IPSC tuning loss, supporting the morphology-driven
explanation.

For the Feller-lab DSGC morphology provenance question, the relevant operational details sit in the
Methods. The paper uses paired SAC-DSGC patch recordings with AlexaFluor-filled cells, 2-photon
imaging of SAC varicosities in CNT (ChAT-Cre/nGFP/TrHr) mice aged p25-120, and manual SAC
reconstruction in FIJI Simple Neurite Tracer exported to SWC and analysed in the TREES toolbox.
Notably, the Methods do NOT describe biocytin fills, Neurolucida reconstruction, a NeuroMorpho.Org
deposition, a cell labelled `141009` or `Pair1DSGC`, or recordings dated 9 October 2014; only SAC
morphologies (not DSGC morphologies) are reconstructed, and the archived data policy is "available
from the corresponding author on request."

## Architecture, Models and Methods

**Animals**: Mice aged p25-120, both sexes. Three crossed lines defined the CNT (ChAT-Cre/nGFP/TrHr)
reporter used to visualise SACs and ON-OFF DSGCs under 2-photon. Sema6A-/- (B6;129P2-Sema6Atm1Ddg/J)
mice were genotyped per Jackson Laboratories. Retinas were dark-adapted 30 min, isolated in
oxygenated Ames' medium at 32-34 degrees C.

**Electrophysiology**: Whole-cell voltage clamp used a CsMeSO4-based internal (110 CsMeSO4, 2.8
NaCl, 20 HEPES, 4 EGTA, 5 TEA-Cl, 4 Mg-ATP, 0.3 Na3GTP, 10 Na2Phosphocreatine, 0.025 mM
AlexaFluor488; pH 7.2, 290 mOsm, ECl- = -74 mV) for DSGCs, with 0.1 mM EGTA and AlexaFluor594 for
SACs. Spiking DSGC responses used standard ACSF. Light stimuli were moving bars in eight directions
and full-field flashes from a PICO projector.

**Paired SAC-DSGC recordings**: Inhibitory conductance was reconstructed from SAC-DSGC pairs
following the algorithm of Miller and Lisberger (2013). DSGCs were held from -100 to +20 mV while
SACs were depolarized three times from -70 mV to 0 mV for 50 ms. Putative synaptic sites were
counted by colocalization of SAC and DSGC volumes in Imaris 9 (Bitplane), with a "Spots" overlap
metric applied to the outer third of the SAC arbor within plus or minus 67 degrees of the null
direction.

**SAC morphology reconstruction**: After recording, 2-photon 1024x1024 stacks (0.5 micrometre step,
780 nm or 930 nm excitation) of AlexaFluor-filled SACs were acquired, then manually traced in FIJI
Simple Neurite Tracer, exported as SWC, and imported into the TREES toolbox in MATLAB for analysis
of branch length, tortuosity and distal-segment orientation. Imaged Ca2+ varicosities were labeled
on the SWC trace. **No DSGC morphology reconstruction, biocytin fill, Neurolucida reconstruction, or
NeuroMorpho.Org deposition is described.**

**IPSC simulation**: Directional SAC-DSGC IPSCs were simulated by placing release sites on the null
half of each reconstructed SAC, weighting by each site's measured Ca2+ tuning curve and preferred
direction, and summing across sites under varying SAC-DSGC wiring misalignment assumptions.

**Data & Software Availability**: "Datasets generated... and all custom scripts and functions
generated or used... are available from the corresponding author on request." (Morrie & Feller 2018,
Methods, p. 15.)

**Sample sizes**: Fig 1 DSGC tuning n = 12 Control / 15 Sema6A-/- cells; Fig 2 paired SAC-DSGC n =
12 Control / 9 Sema6A-/- null-pairs / 6 Sema6A-/- preferred-pairs; Fig 3 Ca2+ imaging n = 6 Control
SACs / 7 Sema6A-/- SACs with 50-100 varicosities per cell; Fig 4 distal-segment analysis used the
same SACs.

## Results

* DSGC ON-direction vector sum magnitude is reduced from **0.40** in Control to **0.10** in
  Sema6A-/- mice (Fig 1B, D; 1-way ANOVA p < 0.001), with no change in OFF tuning.
* Peak ON inhibitory conductance to DSGCs collapses from ~**4 nS** in Control null-direction to
  ~**1.5 nS** in Sema6A-/- null-direction (Fig 1F), with loss of the null-preferred asymmetry.
* Paired SAC-DSGC peak inhibitory conductance in null-oriented pairs is preserved per synapse:
  Control = ~**0.8 nS**, Sema6A-/- null = ~**0.6 nS**, Sema6A-/- preferred = ~**0.25 nS** (Fig 2E;
  1-way ANOVA p = 0.0135, Tukey-Kramer Control vs Sema6A-/- preferred p = 0.014).
* Per-synapse conductance scales linearly with the number of putative synaptic sites in both Control
  and Sema6A-/- pairs (Fig 2F), confirming preserved wiring rule.
* SAC varicosity Ca2+ direction selectivity index (DSI) is comparable between Control and Sema6A-/-
  (Fig 3C; mean DSI Control ~**0.35**, Sema6A-/- ~**0.32**), i.e. intrinsic SAC DS is unaffected.
* **~30-40%** of Sema6A-/- SAC varicosities are no longer tuned to centrifugal motion and instead
  follow local distal-segment orientation (Fig 4C,D), compared to <10% in Controls.
* Varicosity preferred direction correlates with the orientation of the distal **10-40 micrometres**
  of dendrite proximal to the release site, independent of soma-to-varicosity vector (Fig 4F).
* IPSC simulation with measured Sema6A-/- varicosity preferred directions reproduces the observed
  DSGC IPSC tuning loss only when SAC coverage is also reduced to the Sema6A-/- level (Fig 5E,F).

## Innovations

### Morphology-only genetic dissection of the SAC-DSGC motif

Exploits Sema6A-/- as a targeted morphology perturbation: SAC arbors are smaller and asymmetric
while SAC-SAC GABA transmission, ChAT cholinergic output, and DSGC cell-intrinsic properties are
spared, so the loss of directional tuning is unambiguously attributable to SAC morphology, not to
altered excitatory input, altered DSGC intrinsic excitability, or altered SAC release machinery.

### Dissociation of circuit wiring from circuit function

First demonstration that strongly asymmetric SAC-DSGC wiring and subcellular SAC varicosity DS can
coexist with a collapsed DSGC directional tuning. This constrains which elements of the canonical
"asymmetric inhibition" model are sufficient, and shows that dense SAC plexus coverage is a
separate, necessary ingredient.

### Distal-segment rule for SAC varicosity directionality

Each SAC varicosity preferred direction is set by the orientation of a short (10-40 micrometres)
distal neurite segment bearing glutamate receptors, not by the soma-to-varicosity vector. This is a
concrete cable-level rule that downstream compartmental models can implement directly.

## Datasets

* **Electrophysiology and 2-photon imaging dataset**: paired SAC-DSGC recordings and Ca2+ imaging of
  SAC varicosities from Control (CNT) and Sema6A-/- mice. Not publicly archived; per the Methods
  "available from the corresponding author on request."
* **SAC morphology SWC files**: Manually traced SAC dendritic arbors from 2-photon image stacks,
  used as input to the TREES toolbox IPSC simulation. Not deposited on NeuroMorpho.Org as of the
  paper's publication (no deposition statement in the Methods); the NeuroMorpho LinkOut for this
  PMID resolves to SACs (and not the DSGC reconstructions this project's task is chasing).
* **No DSGC morphology reconstruction dataset** is produced or referenced; the paired-recording
  figures (Fig 2A-C) show SAC traces with putative synaptic sites annotated, but the DSGCs
  themselves are not reconstructed in this paper.

## Main Ideas

* **This paper does not, anywhere in its text, reference a DSGC labelled `141009`, a pair identifier
  `Pair1DSGC`, biocytin fills, Neurolucida reconstruction, or an October 2014 recording date.** The
  NeuroMorpho.org record for neuron 102976 (`141009_Pair1DSGC`) lists this DOI as its single
  reference, but the paper's Methods only describe SAC reconstructions via FIJI Simple Neurite
  Tracer. This is direct evidence that the NeuroMorpho linkage is either incorrect, inherited from
  an unpublished lab dataset, or points to an unreported companion DSGC reconstruction produced by
  the Feller lab and deposited separately.
* The paper is strong evidence that dense SAC dendritic overlap (not individual SAC connectivity or
  subcellular Ca2+ DS) is the critical determinant of DSGC directional tuning. Our compartmental
  model must therefore treat SAC coverage/overlap density (not just per-synapse weight) as a
  first-class parameter when generating null-direction inhibition.
* The "distal 10-40 micrometre rule" for varicosity preferred direction gives a concrete spatial
  scale for the directionally tuned GABAergic inputs that our DSGC model should receive: inhibition
  on each null-oriented dendrite segment should be computed from the orientation of the presynaptic
  SAC distal neurite, not from a global centrifugal prior.
* The IPSC simulation framework (null-half SAC release sites, Ca2+-weighted preferred directions,
  TREES toolbox geometry) is a directly reusable template if this project needs to generate
  angle-dependent GABAergic drive for the single-DSGC compartmental model without simulating a full
  SAC population.

## Summary

Morrie and Feller ask which morphological feature of the starburst amacrine cell plexus is necessary
for direction-selective tuning in retinal ganglion cells. Prior work established that asymmetric
SAC-to-DSGC inhibition is central to DS, and that SAC dendrites themselves are tuned to centrifugal
motion, but it was unknown whether loss of DS in morphology-mutant mice reflected broken wiring,
broken subcellular computation, or a broken circuit geometry. The Sema6A-/- mouse offers a clean
dissection because it preserves SAC cell number and GABAergic identity but reduces arbor size and
plexus overlap.

The authors combine cell-attached DSGC spike recordings, whole-cell voltage-clamp IPSC measurements,
paired SAC-DSGC patch recordings with dye fills (AlexaFluor488 for DSGCs, AlexaFluor594 for SACs),
2-photon OGB1 Ca2+ imaging of SAC varicosities, manual morphology tracing in FIJI Simple Neurite
Tracer exported as SWC files to the TREES toolbox, and a custom IPSC simulation in MATLAB. Mice were
p25-120 CNT (ChAT-Cre/nGFP/TrHr) reporter crosses. The experimental design cleanly separates wiring
(paired recordings), subcellular computation (Ca2+ imaging), and geometric arrangement
(reconstructed SAC arbors with varicosity positions and distal-segment orientations).

Three findings carry the paper. First, DSGC directional tuning collapses in Sema6A-/- because
null-direction inhibition is halved (~4 nS to ~1.5 nS) while preferred-direction inhibition is
unchanged. Second, paired SAC-DSGC recordings show that asymmetric wiring and per-synapse
conductance are preserved. Third, Ca2+ imaging shows that SAC varicosity-level DS is preserved but
that ~30-40% of Sema6A-/- varicosities are not tuned to centrifugal motion; instead their preferred
direction follows the orientation of a short distal (10-40 micrometre) neurite segment, and a
TREES-toolbox-based IPSC simulation with each SAC's measured varicosity geometry reproduces the
observed DSGC IPSC tuning loss.

For this project the paper's relevance is both scientific and operational. Scientifically, it
establishes that our compartmental DSGC model must couple SAC plexus coverage and local
distal-segment orientation to the amplitude and preferred direction of each GABAergic input; a model
that only varies per-synapse weight will miss the dominant mechanism of null-direction inhibition.
Operationally, for task t0013 the paper provides decisive negative evidence: its Methods describe
only SAC reconstructions (FIJI to SWC to TREES), never DSGC reconstructions, biocytin fills,
Neurolucida tracings, a `141009` or `Pair1DSGC` identifier, or a NeuroMorpho deposition statement.
The NeuroMorpho.org linkage of neuron 102976 to this DOI is therefore not supported by the paper
itself and must be resolved by inspecting a different Feller-lab source (lab repository, earlier
paired-recording paper, or unpublished deposition metadata).
