---
spec_version: "3"
paper_id: "10.1101_2025.02.10.637538"
citation_key: "Budoff2025"
summarized_by_task: "t0102_seedscale_n4_gen20"
date_summarized: "2026-05-11"
---
# A Complete Spatial Map of Mouse Retinal Ganglion Cells Reveals Density and Gene Expression Specializations

## Metadata

* **File**: `files/budoff_2025_rgc-spatial-map.pdf`
* **Published**: 2025 (bioRxiv preprint, posted 2025-02-12)
* **Authors**: Samuel A. Budoff 🇺🇸, Alon Poleg-Polsky 🇺🇸
* **Venue**: bioRxiv
* **DOI**: `10.1101/2025.02.10.637538`

## Abstract

Retinal ganglion cells (RGCs) transmit visual information from the eye to the brain. In mice,
several RGC subtypes show nonuniform spatial distributions, potentially mediating specific visual
functions. However, the full extent of RGC specialization remains unknown. Here, we used en-face
cryosectioning, spatial transcriptomics, and machine learning to map the spatial distribution of all
RGC subtypes identified in previous single-cell studies. While two-thirds of RGC subtypes were
evenly distributed, others showed strong biases toward ventral or dorso-temporal regions associated
with sky vision and the area retinae temporalis (ART), the predicted homolog of the area centralis.
Additionally, we observed unexpected spatial variation in gene expression within several subtypes
along the dorso-ventral axis or within vs. outside the ART, independent of RGC density profiles.
Finally, we found limited correlations between the gene profiles of the ART and the primate macula,
suggesting divergent specialization between the mouse and primate central vision.

## Overview

This study from the Poleg-Polsky lab produces the first complete spatial atlas of all 45 genetically
defined mouse retinal ganglion cell (RGC) subtypes. Prior to this work, only about 17 of these
subtypes had been spatially mapped, leaving most of the population's retinal topography unknown.
Budoff and Poleg-Polsky combine three methodological pieces -- en-face (horizontal) cryosectioning
of the ganglion cell layer, 10X Genomics Xenium spatial transcriptomics with a custom 300-gene
panel, and two neural-network classifiers (GraSP for gene-panel selection and CuttleNet for
two-stage cell-class then subtype inference) -- to assign every cell in the ganglion cell layer to
one of the 130 retinal subtypes catalogued by single-cell RNA-seq studies, then project them onto a
normalized retina aligned by the dorsal-ventral s/m-opsin gradient.

The resulting atlas covers five C57BL/6J retinas and 130,575 classified RGCs. Roughly two-thirds of
subtypes tile the retina nearly uniformly, while the remaining one-third cluster either in the
ventral retina (sky-facing) or the dorso-temporal retina (the candidate area retinae temporalis,
ART, the proposed rodent homolog of the primate area centralis/macula). The authors also discover
that gene expression itself varies within several subtypes as a function of retinal position, mostly
along the dorso-ventral axis, independent of RGC density. A cross-species comparison of
synaptic-receptor and voltage-gated channel gene expression between the mouse ART and the primate
macula reveals only modest correspondence -- sodium channel expression is conservatively correlated,
but GABA/glycine receptors are anti-correlated -- suggesting the ART and macula are behavioral but
not transcriptomic homologs.

For a project targeting direction-selective RGCs, the most operationally relevant finding is the
spatial atlas itself: the maps of α sustained (αONS = T43, αOFFS = T42, αONT = T41), J-RGCs
(T5), W3 (T2/T3/T4/T6/T21/T23/T30), and several intrinsically photosensitive RGC types are all
reported with their preferred retinal regions. This grounds the regional context in which a
single-cell DSGC model lives, and pins the regional location of the αRGC family that is
mechanistically closest to ON-OFF DSGCs.

## Architecture, Models and Methods

The pipeline integrates wet-lab tissue handling, high-plex in situ hybridization, and two custom
machine-learning models.

* **Animals**: Five adult C57BL/6J mice (3 female, 2 male). All procedures NIH-approved through the
  University of Colorado IACUC.
* **En-face cryosectioning**: After enucleation and cleaning, eye cups were flash-frozen with the
  ganglion cell layer pressed flat against a coverslip in OCT, then cryosectioned at -18 °C into 20
  µm horizontal slices, collected on 10X Genomics Xenium slides.
* **Gene panel selection (GraSP)**: GraSP is a dimensionality-reduction algorithm using neural
  network ensembles, each trained on 50% target / 50% distractor cells. Applied to published
  scRNA-seq atlases, it ranked genes by importance for distinguishing all 130 retinal subtypes; the
  top 225 genes were combined with 75 manually selected genes covering synaptic proteins and
  voltage-gated channels, giving a custom 300-gene Xenium panel.
* **Xenium imaging + IHC**: 10X Xenium in situ hybridization was performed per manufacturer
  protocol; tissue was then co-stained with rabbit anti-RBPMS (Invitrogen MA5-46928) plus
  AF549-conjugated secondary to mark all RGCs and tomato lectin (TL-AF649) for vasculature, then
  imaged on a Keyence BZX800 microscope with structured-illumination optical sectioning.
* **Cell segmentation (Baysor)**: A Bayesian segmentation algorithm using Xenium-derived nuclear
  priors and gene-expression boundaries assigned puncta to individual cells; the ganglion cell layer
  was manually annotated using Grm6 (bipolar), Prox1 (amacrine), Rbpms (RGC) gene markers and the
  RBPMS protein stain.
* **Cell classification (CuttleNet)**: A two-stage hierarchical deep neural network. A "head" module
  assigns each cell to a class (photoreceptor, bipolar, amacrine, glia, RGC) and dynamically routes
  RGC cells to a "tentacle" subnetwork that predicts the specific Tran-cluster subtype. Initial
  training used integrated scRNA-seq datasets from Tran 2019, plus Yan and Macosko data; fine-tuning
  used Xenium-vs-scRNAseq scaling factors per gene. Final RGC class precision was **89.5%** with
  recall **98.5%** on 255 human-labeled RBPMS cells.
* **Registration**: All retinas were rotated to align via the Opn1sw / Opn1mw dorsal-ventral
  gradient and projected onto a normalized Cartesian grid with the optic nerve head at (0,0). For
  global analysis, relief cuts were digitally filled in by radial spreading.
* **Spatial statistics**: Local mosaicism was tested with the Voronoi Domain Regularity Index
  (VDRI), effective radius, and Nearest Neighbor Regularity Index (NNRI) across 14 study regions,
  with bootstrap nulls drawn from the local RGC population. Global clustering used Moran's I (for
  spatial randomness) plus Kulldorff's scan statistic to locate Statistically Significant Spatial
  Clusters (SSSCs); SSSC overlap with binocular-sky, binocular-ground, peripheral-sky and
  peripheral-ground masks was scored via F1, then hierarchically clustered into four spatial groups.
  DEGs were tested by ANOVA with multiple-comparison correction, restricted to genes with mean
  expression > 1 puncta/cell.

The pipeline ultimately classifies **1,434,195 total cells** (300 genes/cell expression matrix) and
**130,575 RGCs** after filtering.

## Results

* Mapped all **45** genetically defined mouse RGC subtypes; previous work had only mapped about
  **17**.
* Final cell-type assignment performance for RGC class: **precision 89.5%, recall 98.5%** on n = 255
  manually labeled cells.
* Relative subtype counts correlated with the Tran scRNA-seq reference at **R² = 0.71**.
* Subtype marker validation: **96.4%** of CuttleNet-classified T6 cells contained at least one Zic1
  puncta (vs **96.5%** in the Tran reference); **72%** of T45 cells expressed Kcnip2 (vs **85-100%**
  in prior work -- slight under-detection attributed to T45 rarity in training).
* Local mosaic structure: **18 of 26** well-represented RGC subtypes had effective radii
  significantly larger than random; NNRI was elevated for the majority; VDRI flagged only **6**
  subtypes as significantly non-random. T7 and T10 were notable exceptions with statistically random
  local distributions.
* Global distribution: about **two-thirds (29/45)** of subtypes tile the retina broadly; the
  remaining one-third split into a ventral/sky-preferring group (7 subtypes, including half of the
  ipRGCs) and a dorso-temporal/ART-preferring group (9 subtypes, including the other ipRGCs).
* αONS (T43), αONT (T41), and αOFFS (T42) reproduced the known dorso-temporal enrichment; W3
  cells correspond to multiple Tran clusters (T2, T3, T4, T6, T21, T23, T30, possibly T1/T13); M1
  ipRGCs (T33, T40) showed a bimodal ventral-plus-temporal peak; M5 ipRGCs (T22) were strongly
  ventral. J-RGCs (T5) showed central clustering.
* The only conflict with prior maps was αOFFT (T45), reported as uniformly distributed previously
  but here showing a modest ventral-temporal peak consistent with a proposed role detecting
  approaching aerial predators.
* Within-subtype DEG analysis: out of 50 genes meeting the > 1 puncta/cell expression criterion,
  **6** had significantly different mean expression across the four spatial RGC groups (ANOVA,
  multiple-comparison-corrected). Of all gene x subtype combinations tested, **0.9%** showed
  statistically different expression within a subtype as a function of retinal position; the
  sky-vs-ground division accounted for over half of these.
* Subtypes with the most position-dependent DEGs: **T6 (7 DEGs)**, **T8, T14, T16, T17, T36 (5-6
  DEGs each)**.
* Cross-species comparison of mouse ART vs primate macula gene expression: only modest overall
  correlations; **voltage-gated sodium channel** genes were significantly positively correlated,
  while **GABA and glycine receptor** subunits were significantly anti-correlated; the Na-channel
  correlation was driven by ventral-retina Group-3 subtypes that lie outside the ART itself.

## Innovations

### Complete Spatial Atlas of All 45 Mouse RGC Subtypes

First study to spatially map every genetically defined mouse RGC subtype in a single coherent
coordinate frame, more than doubling prior coverage (17 -> 45 subtypes). The result is a publishable
atlas that fixes the regional preferences of subtypes that were previously known only from scRNA-seq
abundance.

### En-Face Cryosectioning for Xenium

Adapting horizontal (en-face) cryosectioning to 10X Xenium slides preserves large intact pieces of
the ganglion cell layer instead of the vertical cross-sections used by previous spatial-
transcriptomic retina studies. This preserves the en-face spatial relationships required to detect
dorso-temporal or ventral specialization at all, and avoids fragmenting cell mosaics.

### GraSP + CuttleNet ML Stack

A two-stage hierarchical deep neural network ("head" + dynamically routed "tentacles") trained on
combined scRNA-seq atlases and fine-tuned with Xenium scaling factors, supported by a custom
neural-network-ensemble feature selector (GraSP). Together they enable subtype-level inference from
a 300-gene panel with high RGC precision/recall (89.5/98.5).

### Functional Decoupling of Density and Gene Expression

Demonstrates that within-subtype gene expression varies across retinal position independently of the
subtype's density distribution. This challenges the simple "subtype = single uniform transcriptomic
identity" assumption and supports a continuous-variation account where regional specialization is
partly a within-subtype gene-expression phenomenon.

### Quantitative Mouse-Primate Specialization Comparison

First systematic transcriptomic comparison of the ART (proposed rodent homolog of the macula)
against the primate macula using matched synaptic-receptor and voltage-gated channel gene families.
The finding of weak global correlation but specific positive Na-channel and negative GABA/glycine
receptor patterns nuances the homology claim and warns against using ART as a one-to-one macular
model.

## Datasets

* **Primary dataset (this study)**: 10X Genomics Xenium en-face spatial transcriptomics on 5
  C57BL/6J mouse retinas (3 female, 2 male), custom 300-gene panel, RBPMS + tomato lectin IHC
  co-stain. Final processed dataset: 1,434,195 segmented cells and 130,575 classified RGCs.
* **scRNA-seq training data**: Integrated published mouse retinal scRNA-seq atlases (Tran et al.,
  Yan et al., Macosko et al.), used both for GraSP gene-panel selection and for CuttleNet training.
* **Primate scRNA-seq data**: Published primate retinal scRNA-seq datasets used for the
  mouse-vs-primate comparison of synaptic-receptor and voltage-gated channel gene expression. The
  paper restricts the comparison to orthologous genes.
* **Availability**: This is a bioRxiv preprint with CC-BY-NC-ND 4.0 license. Source data and code
  availability are described in the manuscript; data are sufficient to support all reported figures.

## Main Ideas

* The Poleg-Polsky lab (origin of the DSGC model used in this project) has now published a
  high-resolution map of where every RGC subtype sits in the mouse retina -- this provides the
  regional context for any single-cell DSGC simulation and explicitly localizes the α-RGC family
  that is mechanistically closest to ON-OFF DSGCs to the dorso-temporal retina.
* Within-subtype spatial variation in voltage-gated channel and synaptic-receptor gene expression
  (sodium channel and GABA receptor families especially) is real and statistically significant. This
  is direct biological evidence that a single DSGC subtype need not have one fixed Na/K conductance
  setting -- supporting the project's premise that parametric exploration of those conductances is
  biologically meaningful.
* The ART is not a transcriptomic copy of the primate macula. Conclusions drawn from a mouse-ART
  DSGC model should not be extrapolated to primate central-vision DSGCs without explicit
  acknowledgement of the divergence found here, particularly in GABA / glycine receptor expression.
* Mosaic regularity holds for most but not all RGC subtypes (18/26 well-represented subtypes with
  significantly larger effective radii than random; T7 and T10 are random). For the DSGC model, this
  argues that homotypic spacing should not be assumed perfectly regular if a future task scales up
  to a network simulation.
* The same group's two-stage neural-network classifier (CuttleNet) and gene-panel selector (GraSP)
  provide reusable references if any downstream task needs to identify or stratify cells by
  transcriptomic profile from sparse panels.

## Summary

Budoff and Poleg-Polsky (2025) present the first complete spatial atlas of all 45 mouse retinal
ganglion cell subtypes. The motivation is direct: scRNA-seq has catalogued ~45 mouse RGC subtypes,
but spatial mapping had reached only about 17 of them, leaving most of the population's retinal
topography and any regional specialization unknown. The study asks where each genetically defined
subtype lives, whether subtypes show local mosaic regularity, whether gene expression varies within
a subtype as a function of retinal position, and how the mouse area retinae temporalis (ART)
compares transcriptomically to the primate macula.

Methodologically the paper combines four pieces: (1) en-face cryosectioning of intact ganglion-cell
layers on 10X Genomics Xenium slides, (2) a custom 300-gene Xenium panel chosen by the GraSP
neural-network-ensemble feature selector (225 unbiased genes plus 75 manually picked
synaptic-protein and voltage-gated-channel genes), (3) Baysor Bayesian cell segmentation with Xenium
nuclear priors, and (4) CuttleNet, a two-stage hierarchical deep neural network with a class "head"
and dynamically routed subtype "tentacles" trained on integrated mouse scRNA-seq atlases. Five
C57BL/6J retinas were imaged, IHC-stained with RBPMS and tomato lectin, and projected onto a
normalized Cartesian retina aligned by the Opn1sw/mw opsin gradient. Local mosaicism was assessed
with VDRI/NNRI/effective-radius statistics against bootstrap nulls; global clustering used Moran's I
plus Kulldorff scan statistics and F1 overlap with ethologically relevant visual-field masks; DEGs
were tested by ANOVA with multiple-comparison correction.

The atlas reveals that about two-thirds of mouse RGC subtypes (29 of 45) tile the retina nearly
uniformly, with the remaining third splitting into a ventral, sky-facing group and a dorso-temporal,
ART-preferring group containing the α-RGC family and several intrinsically photosensitive RGC
subtypes. Local mosaic regularity was confirmed for 18 of 26 well-sampled subtypes. Most known maps
(αONS, αONT, αOFFS, W3, J-RGCs, M1/M2/M4/M5 ipRGCs) were reproduced, with the only material
disagreement being a modest ventral-temporal peak for αOFFT (T45) instead of the previously
reported uniform distribution. About 0.9% of gene x subtype combinations showed within-subtype
regional DEGs, mostly along the sky-vs-ground axis; T6, T8, T14, T16, T17, and T36 carried the most
DEGs. The mouse ART correlates weakly with the primate macula transcriptomically: voltage-gated
sodium channel expression is positively correlated (driven by ventral Group-3 subtypes), while GABA
and glycine receptors are anti-correlated.

For this project, the paper provides three concrete deliverables. First, it pins the dorso-temporal
location of the α-RGC family that is mechanistically closest to ON-OFF DSGCs, fixing the regional
context in which the project's single-cell DSGC model lives. Second, the demonstration that
voltage-gated sodium channel and GABA receptor gene expression varies within a subtype as a function
of retinal position gives direct biological support to the project's core premise that systematic
parametric exploration of Na/K conductance combinations is biologically realistic -- a single DSGC
subtype is not a single biophysical operating point. Third, the divergence between the mouse ART and
primate macula (especially for GABA/glycine receptors) warns against over-extrapolating any
optimised mouse-DSGC model to primate central vision. This paper also confirms the Poleg-Polsky
group's continued activity on mouse DSGC biology, which is relevant context for the de Rosenroll
2026 DSGC model that motivates this task.
