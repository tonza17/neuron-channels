---
spec_version: "3"
paper_id: "10.1523_JNEUROSCI.1461-23.2024"
citation_key: "Tworig2024"
summarized_by_task: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
date_summarized: "2026-05-04"
---

# Differential Expression Analysis Identifies Candidate Synaptogenic Molecules for Wiring Direction-Selective Circuits in the Retina

## Metadata

* **File**: `files/tworig_2024_cbln4-dsgc-wiring.pdf`
* **Published**: 2024-03-21
* **Authors**: Joshua M. Tworig 🇺🇸, Ryan D. Morrie 🇺🇸, Karina Bistrong 🇺🇸,
  Rachana D. Somaiya 🇺🇸, Shaw Hsu 🇺🇸, Jocelyn Liang 🇺🇸, Karen G. Cornejo 🇺🇸,
  Marla B. Feller 🇺🇸
* **Venue**: The Journal of Neuroscience 44(18):e1461232024
* **DOI**: `10.1523/JNEUROSCI.1461-23.2024`

## Abstract

An organizational feature of neural circuits is the specificity of synaptic connections. A striking
example is the direction-selective (DS) circuit of the retina. There are multiple subtypes of DS
retinal ganglion cells (DSGCs) that prefer motion along one of four preferred directions. This
computation is mediated by selective wiring of a single inhibitory interneuron, the starburst
amacrine cell (SAC), with each DSGC subtype preferentially receiving input from a subset of SAC
processes. We hypothesize that the molecular basis of this wiring is mediated in part by unique
expression profiles of DSGC subtypes. To test this, we first performed paired recordings from
isolated mouse retinas of both sexes to determine that postnatal day 10 (P10) represents the age at
which asymmetric synapses form. Second, we performed RNA sequencing and differential expression
analysis on isolated P10 ON-OFF DSGCs tuned for either nasal or ventral motion and identified
candidates which may promote direction-specific wiring. We then used a conditional knock-out
strategy to test the role of one candidate, the secreted synaptic organizer cerebellin-4 (Cbln4),
in the development of DS tuning. Using two-photon calcium imaging, we observed a small deficit in
directional tuning among ventral-preferring DSGCs lacking Cbln4, though whole-cell voltage-clamp
recordings did not identify a significant change in inhibitory inputs. This suggests that Cbln4
does not function primarily via a cell-autonomous mechanism to instruct wiring of DS circuits.
Nevertheless, our transcriptomic analysis identified unique candidate factors for gaining insights
into the molecular mechanisms that instruct wiring specificity in the DS circuit.

## Overview

Tworig et al. tackle the developmental question of how each DSGC subtype acquires its asymmetric
SAC-to-DSGC inhibitory wiring during a brief postnatal window. The work proceeds in three stages:
(1) paired patch-clamp recordings between SACs and ON-OFF DSGCs across P7-P14 to localize the day
on which null-side asymmetric inhibition emerges; (2) bulk RNA sequencing of FACS-isolated
GFP-labeled DSGCs from three transgenic lines (Drd4-GFP and Trhr-GFP for nasal-preferring
populations, Hb9-GFP for the ventral-preferring population) at the identified critical day P10;
and (3) a conditional RGC-targeted knockout of one top-ranked candidate, the C1q-family secreted
synaptic organizer Cbln4, with two-photon calcium imaging and whole-cell voltage-clamp readouts of
DS tuning and synaptic currents.

The transcriptomic screen identifies hundreds of differentially expressed transcripts between
nasal- and ventral-preferring DSGCs, including members of the C1q/cerebellin family, protein
tyrosine phosphatases, clustered protocadherins, and splice isoforms of teneurin-3 (Tenm3). Cbln4
is one of the strongest hits, with ~100-fold enrichment in ventral-preferring (Hb9-GFP) DSGCs and
effectively absent expression in nasal-preferring DSGCs. The functional knockout nonetheless yields
a comparatively modest phenotype: a small DSI reduction across all ventral-preferring DSGCs imaged
via population two-photon calcium imaging, with no detectable change in EPSC or IPSC amplitude,
asymmetry, timing, or dendritic morphology in voltage-clamp recordings. The authors interpret this
as evidence that Cbln4 does not act cell-autonomously in DSGCs to instruct asymmetric SAC->DSGC
inhibitory wiring, while still validating the screen as a discovery tool for candidate synaptogenic
molecules.

## Architecture, Models and Methods

This is an experimental wet-lab paper combining electrophysiology, molecular biology, and
transcriptomics. No compartmental modelling is performed.

* **Animals**: mixed C57BL/6 mice of both sexes, P15-35 for adult experiments and P7-P14 for
  developmental experiments. Transgenic lines: Drd4-GFP and Trhr-GFP (nasal-preferring DSGCs),
  Hb9-GFP (ventral-preferring DSGCs), Chat-Cre, Chat-CreER, VGlut2-Cre, Cbln4-flox (JAX 032960).
* **Paired patch-clamp**: SAC->DSGC paired recordings in Chat-Cre;nGFP;Trhr-GFP whole-mount retinas
  in oxygenated Ames medium at 32-34 C. SACs depolarized to 0 mV, DSGCs voltage-clamped at varying
  holding potentials. n = 4 DSGCs at P9, n = 5 DSGCs at P10.
* **Varicosity imaging**: sparse SAC tdTomato labeling via Chat-CreER x Ai9 with low-dose tamoxifen
  (200 ug in 125 ul sunflower oil at P4); confocal Z-stacks with Plan-Apochromat 40x/60x oil
  objectives at 100 nm pixel size; varicosities marked manually in Imaris.
* **FACS RNA-seq**: P10 retinas dissociated with papain (1 U/ul, 21 min at 37 C); single cells
  sorted on BD FACSAria Fusion; cDNA libraries prepared via Smart-Seq. Three biological replicates
  per genotype. Sequencing on Illumina HiSeq 4000, 100 bp paired-end. ~64.5M fragments per sample,
  77.8% genomic alignment via Hisat2 + featureCounts; parallel Kallisto pseudoalignment to the
  mouse transcriptome (mm10) with Sleuth Wald tests for differential expression. Significance cuts
  applied at adjusted p < 0.01 and beta effect size > 2 or < -2; Benjamini-Hochberg FDR. GO
  enrichment via GO::TermFinder.
* **Cbln4 conditional knockout**: Cbln4^fl/fl x VGlut2-Cre to delete Cbln4 from RGCs, with
  IRES-mVenus reporter in floxed allele and tdTomato switch in Cre-recombined allele.
* **Two-photon calcium imaging**: AAV-syn-GCaMP6f population imaging; moving bar stimuli in 8
  directions; DSI = (R_PD - R_ND) / (R_PD + R_ND); permutation test for direction selectivity at
  the 95th percentile cutoff; k-means clustering by preferred direction.
* **Voltage-clamp**: whole-cell EPSCs (V_h = -60 mV) and IPSCs (V_h = 0 mV) during drifting bars at
  250 um/s and 1,000 um/s; Alexa-594 dye fills for 3D morphology reconstruction; Sholl analysis
  with 5 um concentric rings; dendritic asymmetry index from convex-hull soma offset.

## Results

* **Cbln4 mRNA enrichment** in ventral-preferring DSGCs is ~100-fold over nasal-preferring DSGCs
  (Drd4-GFP **19.96 +/- 5.29** counts, Trhr-GFP **11.03 +/- 3.33**, Hb9-GFP **2,654 +/- 71.25**;
  Wald q = 1.97e-47, n = 3 biological replicates per genotype).
* **FISH puncta per cell at P10** confirms differential expression: Drd4-GFP **4.6 +/- 2.1**,
  Trhr-GFP **3.0 +/- 1.5**, Hb9-GFP **25.8 +/- 3.1** (one-way ANOVA p = 1.14e-6).
* Asymmetric inhibitory SAC->DSGC connectivity emerges between **P9 and P10** (paired-recording
  null-side conductance increases significantly at P10, t-test p = 0.014); SAC varicosities first
  rise at P10 and reach mature levels by P12 (Kruskal-Wallis p < 0.01).
* Bulk RNA-seq identifies **2,270 transcripts and 979 genes** differentially expressed between
  nasal- and ventral-preferring DSGCs at P10 (adj p < 0.01, |beta| > 2). GO enrichment includes
  cell periphery (659 genes, p = 8.7e-25), plasma membrane (602 genes, p = 1.4e-22), neuron
  projection (242 genes, p = 1.4e-11), and neuron->neuron synapse (98 genes, p = 2.2e-9).
* RGC-targeted Cbln4 KO produces a **small but significant reduction in DSI/vector sum** across all
  ventral-preferring DSGCs in two-photon calcium imaging, but **no significant DSI difference** in
  the Hb9-GFP subset (Hb9 = 28% of all ventral DSGCs in WT, 30% in KO).
* Whole-cell voltage-clamp shows **no significant difference** in IPSC magnitude (preferred or null
  direction), IPSC DSI, EPSC magnitude, or EPSC/IPSC timing offset in Cbln4 KO ventral DSGCs at
  either 250 um/s or 1,000 um/s drifting-bar speeds; cell counts n = 35 WT vs n = 17 KO
  ventral-preferring DSGCs (10 vs 8 mice).
* **Dendritic morphology preserved**: total dendrite length, dendrite-soma center-of-mass offset,
  number of branch points, ON-OFF index, ON and OFF Sholl profiles all unchanged between
  Cbln4^fl/fl and VGlut2-Cre;Cbln4^fl/fl ventral-preferring DSGCs (n = 16 WT vs n = 18 KO;
  mixed-ANOVA over Sholl radii non-significant).
* Cbln4 KO reduces inhibitory **center-surround index** in small-receptive-field ON-OFF RGCs and
  increases OFF-pathway speed-tuning index in suppressed-by-contrast RGCs (both p < 0.05), but
  EPSC/IPSC amplitudes during full-field flashes are otherwise unchanged in non-DS RGC types.
* Other top differentially expressed gene families with biological-prior synaptogenic relevance
  include C1q/TNF (Cbln4, C1qtnf1, C1qtnf6, C1ra, C1s1), protein tyrosine phosphatases (Ptprs,
  Ptpru, Ptprd, Ptprj, Ptprk, Ptprf, Ptprh), and clustered protocadherins (Pcdhga4, Pcdhgb6,
  Pcdhgb2, Pcdhga10, Pcdhgb7, Pcdh1, Pcdhga3, Pcdhgb8, Pcdha6, Pcdh11x), plus distinct Tenm3 splice
  isoforms (Tenm3-201 in nasal, Tenm3-206 in ventral DSGCs).

## Innovations

### P10 Critical-Window Identification

Direct paired-recording evidence that null-side SAC->DSGC inhibitory conductance asymmetry appears
between P9 and P10, combined with sparse-label varicosity counting that pins SAC presynaptic-
structure formation to the same window. This dual electrophysiology + morphology calibration
anchors the choice of P10 as the molecular-screen sampling time point.

### Subtype-Resolved P10 Bulk RNA-seq of Three DSGC Lines

First differential-expression screen of three orthogonal-direction DSGC populations (Drd4-GFP,
Trhr-GFP, Hb9-GFP) at the P10 wiring-onset day. Bulk read depth allows splice-isoform-level
discovery (e.g. Tenm3-201 vs Tenm3-206), which is not feasible with shallower scRNA-seq datasets
covering the same cell types.

### RGC-Specific Cbln4 Conditional Knockout Tool

Crossing the Cbln4^fl/fl reporter line with VGlut2-Cre yields RGC-targeted Cbln4 deletion with
mVenus/tdTomato reporter switching, enabling targeted live-cell electrophysiology and morphology on
Cbln4-positive vs Cbln4-null RGCs in the same retina. This is the first published use of this tool
combination in the retinal DS circuit and establishes a negative-result control: Cbln4 in RGCs is
not required for asymmetric SAC->DSGC inhibitory synaptogenesis.

## Datasets

* **Bulk RNA-seq**: 9 samples (3 biological replicates x 3 genotypes), Illumina HiSeq 4000, 100 bp
  paired-end, ~64.5M fragments per sample. Aligned to GRCm38/mm10 via Hisat2 and pseudoaligned to
  the mouse transcriptome via Kallisto. Reference scRNA-seq: GSE185671 (Shekhar et al. 2022),
  GSE137400 (Tran et al. 2019), GSE149715 (Yan et al. 2020), accessed via the Broad Single Cell
  Portal.
* **Paired patch-clamp**: SAC->DSGC pairs at P9 (n = 4 DSGCs), P10 (n = 5 DSGCs); reference adult
  data from Wei et al. 2010.
* **Two-photon calcium imaging**: 265 Hb9-GFP DSGCs from 5 Cbln4^fl/fl mice; 252 Hb9-GFP DSGCs from
  4 VGlut2-Cre;Cbln4^fl/fl mice; 163 ventral-preferring + 171 nasal-preferring DS cells in WT vs
  96 + 133 in KO.
* **Voltage-clamp**: 35 ventral-preferring DSGCs from 10 WT mice and 17 from 8 KO mice; total
  population includes 65 mVenus+ and 68 tdTomato+ Cbln4-expressing RGCs across all subtypes.
* **Morphology**: 16 WT and 18 KO ventral-preferring DSGC dendritic reconstructions.
* All transgenic mouse lines are publicly available (JAX/MMRRC strain numbers reported in the
  Materials and Methods section).

## Main Ideas

* **Wiring-specificity molecules act developmentally on a fixed substrate**, distinct from the
  electrophysiological-property optimisation that t0080 performs. This paper addresses how the
  asymmetric SAC->DSGC inhibitory pattern is laid down between P9 and P10; t0080 takes that pattern
  as given and instead optimises Na/K conductance distributions, AIS geometry, and dendritic-spike
  parameters on top of it.
* **Hb9-GFP subset is not representative of all ventral-preferring DSGCs** (28-30% of the
  population). When citing ventral-preferring DSGC properties from this paper, distinguish between
  the broader k-means-clustered ventral DSGC population and the molecularly defined Hb9-GFP subset
  -- the two diverge in the Cbln4 KO phenotype.
* **Cbln4 is not the bottleneck for asymmetric inhibition**: voltage-clamp IPSC magnitude,
  asymmetry, and timing are unchanged in the KO. Project plans should not assume that perturbing
  one C1q-family synaptic-organiser gene will substantially reshape the inhibitory tuning curve
  that is the t0080 target reference.
* **Excitatory inputs onto ventral-preferring DSGCs are weakly directional with a ventral
  preference**, with peak EPSCs larger in the ventral direction but tuning much weaker than IPSCs
  (consistent with Park 2014, Pei 2015, Percival 2019, El-Quessny 2020, Summers 2021). This matters
  for any future task that revisits the t0080 fixed E/I substrate -- the model can keep a near-
  symmetric AMPA input distribution as a reasonable first-order approximation.
* **Splice-isoform-level differences (Tenm3-201 vs Tenm3-206) discriminate nasal- from
  ventral-preferring DSGCs**, hinting that future morphology-coupled studies should treat these as
  separate cell types, not as a single bucket of ON-OFF DSGCs.

## Summary

Tworig and colleagues address one specific developmental question: which molecules instruct the
asymmetric inhibitory wiring between starburst amacrine cell processes and the four ON-OFF DSGC
subtypes during the brief P9-P10 critical period? Prior work had shown that the asymmetric
inhibitory pattern emerges within roughly two postnatal days and persists in the absence of visual
input, suggesting an instructive molecular code, but the responsible molecules were unknown. The
authors target the postsynaptic side of this wiring problem in mouse retina with a transcriptomic
screen and a single conditional knockout follow-up.

The methodology combines paired patch-clamp (to time-stamp the wiring-onset day at P10), bulk
RNA-seq on FACS-isolated GFP-labelled nasal- vs ventral-preferring DSGCs from three transgenic
lines, and a Cbln4 conditional RGC knockout (Cbln4^fl/fl x VGlut2-Cre). Functional readouts use
two-photon population calcium imaging and whole-cell voltage-clamp during 8-direction drifting-bar
stimuli at 250 and 1,000 um/s, plus 3D dye-fill morphology reconstruction with Sholl analysis.
Statistical testing uses Wald tests with Benjamini-Hochberg FDR for differential expression and
permutation tests for direction-selective cell classification.

The screen yields **2,270 differentially expressed transcripts** including strong candidates from
the C1q/cerebellin family, protein tyrosine phosphatases, clustered protocadherins, and Tenm3
splice isoforms. Cbln4 is **~100-fold enriched** in ventral-preferring (Hb9-GFP) DSGCs, but the
RGC-targeted KO produces only a **small DSI reduction** in the broader ventral-preferring DSGC
population and **no detectable difference** in IPSC amplitude, asymmetry, or timing, EPSC
properties, or dendritic morphology in voltage-clamp recordings. The authors conclude that Cbln4
does not function cell-autonomously in DSGCs to instruct asymmetric SAC->DSGC wiring, while still
validating the differential-expression screen as a discovery tool for other candidate molecules.

For this project, the paper is tangential to t0080 optimisation aims because t0080 operates on a
fixed deposited E/I substrate rather than reshaping it. The relevance is contextual: it documents
the developmental origin of the asymmetric inhibitory wiring that t0080 takes as a fixed biological
prior, validates that ventral-preferring DSGCs receive stronger inhibition for dorsal motion (a
hallmark feature already encoded in our target tuning curve), and reports that excitation onto
these cells is weakly direction-tuned with a ventral preference -- supporting the project
continued treatment of the AMPA input distribution as approximately symmetric. The ~100-fold Cbln4
enrichment hit with a small DSI phenotype is also a useful negative-result anchor: it shows that
single-gene perturbations of synaptic organisers do not substantially redistribute the inhibitory
tuning curve, so future tasks should keep the project E/I substrate fixed at the canonical
t0078/t0080 levels rather than attempting biologically motivated perturbations of single
synaptogenic molecules.
