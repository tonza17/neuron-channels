---
spec_version: "3"
paper_id: "10.1016_j.neuron.2016.02.020"
citation_key: "Vlasits2016"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# A Role for Synaptic Input Distribution in a Dendritic Computation of Motion Direction in the Retina

## Metadata

* **File**: `files/vlasits_2016_synaptic-input-distribution.pdf`
* **Published**: 2016-03-16
* **Authors**: Anna L. Vlasits 🇺🇸, Ryan D. Morrie 🇺🇸, Alexandra Tran-Van-Minh 🇫🇷, Adam Bleckert 🇺🇸,
  Christian F. Gainer 🇺🇸, David A. DiGregorio 🇫🇷, Marla B. Feller 🇺🇸
* **Venue**: Neuron 89(6), 1317-1330
* **DOI**: `10.1016/j.neuron.2016.02.020`

## Abstract

The starburst amacrine cell in the mouse retina presents an opportunity to examine the precise role
of sensory input location on neuronal computations. Using visual receptive field mapping, glutamate
uncaging, two-photon Ca2+ imaging, and genetic labeling of putative synapses, we identify a unique
arrangement of excitatory inputs and neurotransmitter release sites on starburst amacrine cell
dendrites: the excitatory input distribution is skewed away from the release sites. By comparing
computational simulations with Ca2+ transients recorded near release sites, we show that this
anatomical arrangement of inputs and outputs supports a dendritic mechanism for computing motion
direction. Direction selective Ca2+ transients persist in the presence of a GABA-A receptor
antagonist, though the directional tuning is reduced. These results indicate a synergistic
interaction between dendritic and circuit mechanisms for generating direction selectivity in the
starburst amacrine cell.

## Overview

This paper asks whether the spatial distribution of excitatory synaptic inputs along a dendrite is
itself a computational variable, independent of morphology, for the generation of direction
selectivity (DS) in the mouse retina. The target neuron is the starburst amacrine cell (SAC), whose
radiating distal varicosities each behave as independent DS sub-units preferentially responding to
motion from the soma outward. Prior work had attributed SAC DS chiefly to cable filtering imposed by
thin dendrites and to GABAergic lateral interactions in the retinal network. Here the Feller lab and
their Institut Pasteur collaborators combine four experimental modalities with a compartmental
biophysical model to show that the *location* of inputs along the dendrite is not uniform and that
its skewed, proximal-restricted layout is essential for the dendritic computation.

The experimental core maps where excitatory inputs land on the SAC dendrite using visual spot and
ring receptive-field mapping, dendritic glutamate uncaging, PSD95-YFP puncta labeling, and a
re-analysis of the Briggman et al. (2011) serial block-face EM reconstruction. All four techniques
converge on the same surprising anatomy: bipolar-cell excitatory contacts are concentrated on the
proximal two-thirds of the dendrite, while release-site varicosities occupy the distal third, so
inputs and outputs are displaced from each other rather than co-localized. A passive ball-and-stick
NEURON model driven by moving-bar stimuli then shows that this displaced proximal-restricted input
profile generates a robust centrifugal (outward-preferring) voltage difference at the release zone,
whereas a symmetric full-length input profile of matched density does not. Ca2+ imaging of
individual varicosities confirms the model predictions in tissue. The paper therefore reframes SAC
direction selectivity as a joint product of morphology, input placement, and circuit inhibition —
with input placement identified as a necessary, under-studied ingredient.

## Architecture, Models and Methods

The compartmental model was built in **NEURON v7.3** as a passive ball-and-stick SAC with the soma
replaced by a single sphere and a straight dendrite whose diameter was tapered in accordance with
two-photon anatomical measurements (<0.3 µm in the distal portion). The reference dendrite length
was ~150 µm (maximum radius ~160 µm in example cells). No active conductances were included in the
core analysis, isolating the passive cable contribution; a supplementary model with voltage-gated
Ca2+ channels in the varicosities was used to show that active channels amplify but do not create
DS.

Four synaptic-input distributions were simulated on the **same morphology** at **matched total
synapse count and matched mean density**, making this a classical morphology-matched control
comparison:

* **Skewed-uncaging**: density 0.09 synapses/µm over the proximal 69% of the dendrite, derived from
  glutamate-uncaging-detected postsynaptic sites.
* **Skewed-PSD95**: density 0.20 synapses/µm over the proximal region, derived from averaged
  PSD95-YFP puncta data.
* **Regular full-length**: uniform density 0.09/µm spread over 0-100% of the dendrite.
* **Regular proximal-restricted**: uniformly spaced synapses ending at 71% path length, matched
  density.

Moving bars travelled at 500 µm/s (replicated at 1000 µm/s). Outputs were peak dendritic voltage
sampled across space-time; DS was quantified as the difference between outward-motion and
inward-motion peaks at the release zone.

Experimental methods supporting the model inputs included: whole-cell voltage clamp (Vhold = -72 mV,
Cs-based internal for electrophysiology, K-based for imaging, 4-10 sweep averaging); two-photon Ca2+
imaging of OGB-1-filled dendrites during moving-square stimulation (25 µm squares at 75% or 100%
dendritic-radius extents); spatially targeted MNI-glutamate uncaging along single dendrites (n = 20
dendrites from 15 cells); PSD95-YFP transgenic labeling (n = 8 cells from 5 retinas, 10 µm
sliding-window density profiles, log-ratio threshold 1.0); GABA-A pharmacology with 5 µM gabazine ±
1 µM strychnine (n = 9 cells).

## Results

* Excitatory receptive field from visual spot stimulation decays to <5% maximum at **74 ± 13%** of
  dendritic radius (**n = 15** cells), and from ring stimulation at **77 ± 10%** (n = 6) — inputs
  occupy only the proximal two-thirds of the dendrite.
* Glutamate uncaging confirms a proximal-restricted excitatory field extending to **69 ± 9%** of
  dendritic path length (n = 20 dendrites, 15 cells); PSD95 puncta density also peaks near the soma
  and declines distally (n = 8 cells, 5 retinas).
* Re-analysis of serial block-face EM of **24 SACs** (Briggman et al., 2011) shows only **~25%** of
  GABAergic output sites onto DSGCs overlap with the excitatory input field — input and output
  distributions are significantly skewed from one another (**Wilcoxon rank test, p < 0.05**).
* Direction selectivity index at distal varicosities (outside the excitatory receptive field, **n =
  25**) is **DSI = 0.34 ± 0.23**, versus **DSI = 0.11 ± 0.18** at proximal varicosities inside the
  receptive field (**n = 8**) — a ~3x DSI increase associated with proximal-restricted input
  placement (Student t-test, p < 0.05).
* Morphology-matched symmetric-input control in the NEURON model: the regular full-length
  distribution produces only weak, progressively increasing DS beyond ~45 µm, whereas the skewed
  proximal-restricted distribution produces strong outward DS over a consistent ~30 µm of distal
  dendrite at matched total density.
* Extending the visual bar from 75% to 100% of dendritic radius increases DSI in control (**ΔDSI =
  0.16 ± 0.10**, n = 22) but not in 5 µM gabazine (**ΔDSI = 0.02 ± 0.23**, n = 9; repeated-measures
  ANOVA p < 0.05), showing that GABAergic inhibition sharpens but does not create the underlying
  dendritic DS.

## Innovations

### Morphology-Matched Symmetric-Input Control

The paper establishes a clean methodological template for dissociating morphology from input
placement. The authors simulate four synaptic-input distributions on the **same reconstructed SAC
dendrite**, with total synapse number and mean density held constant, and vary only whether inputs
are clustered proximally (as observed) or spread symmetrically along the full dendrite. Because
every other biophysical factor — cable diameter, taper, sealed-end boundary, passive parameters — is
identical, any difference in the resulting DS is attributable exclusively to input geometry. This
morphology-matched symmetric-input control is the canonical design used in subsequent work
(including Ding et al. 2016 and Poleg-Polsky et al.) to isolate the contribution of input spatial
statistics from the contribution of the dendritic tree itself.

### Four-Modality Input-Map Triangulation

Rather than inferring input locations from a single technique, the study cross-validates the
proximal-restricted excitatory map using visual spot mapping, ring mapping, glutamate uncaging, and
PSD95-YFP puncta density, then anchors the output map to a third-party EM reconstruction. Agreement
across four orthogonal techniques (each with different biases) makes the displaced input-output
anatomy unusually robust as a target for modeling.

### Reframing SAC DS as Synergistic

Before this paper, SAC DS was most often explained either by cable filtering on a uniform input
field or by GABAergic circuit interactions. By demonstrating dendritic DS in TTX-free passive
simulations and in gabazine-isolated Ca2+ transients, the authors reframe the computation as a
synergy of three factors — passive cable, input placement, and circuit inhibition — and quantify
each contribution separately.

## Datasets

* Two-photon Ca2+ imaging recordings from 33 SAC varicosities across multiple cells (in-house,
  unpublished raw data).
* Whole-cell voltage-clamp recordings from 15 SACs for visual receptive-field mapping.
* Glutamate-uncaging-derived postsynaptic-site maps from 20 dendrites of 15 cells.
* PSD95-YFP transgenic confocal image stacks from 8 SACs in 5 retinas.
* Re-analysis of the publicly available **Briggman et al. (2011) serial block-face EM volume** of 24
  SACs with DSGC output contacts (Max-Planck Institute / Connectomics). This dataset underlies the
  input-output overlap analysis and is the only externally released resource used.

All in-house experimental data appear to be available on request; no public data-release identifiers
are listed in the paper.

## Main Ideas

* Synaptic input spatial distribution is an independent computational variable for dendritic DS,
  beyond dendritic morphology and beyond circuit inhibition. Any morphology-only model of a DS
  neuron is incomplete without an empirically measured input map.
* The **morphology-matched symmetric-input control** is the right experimental and modeling template
  for any future task in this project that asks whether input placement matters — hold morphology,
  total synapse count, and mean density constant; vary only spatial arrangement.
* Multi-modality triangulation of input and output locations (visual mapping + uncaging + molecular
  marker + EM) is more reliable than any single technique; our compartmental modeling tasks should
  budget for cross-validation rather than relying on one source.
* DS measured at release-site varicosities (DSI ~0.3) is a meaningful, readily reproducible
  benchmark for our own SAC/DSGC simulations; values substantially below this suggest the input map
  has been oversimplified.

## Summary

Vlasits et al. (2016) address a longstanding question in retinal direction selectivity: whether the
*location* of excitatory inputs along a starburst amacrine cell dendrite matters, separately from
morphology and network inhibition. They combine four experimental techniques — visual receptive
field mapping with spots and rings, MNI-glutamate uncaging, PSD95-YFP genetic labeling, and
re-analysis of the Briggman et al. connectome — to show that excitatory bipolar inputs are
concentrated on the proximal ~70% of the SAC dendrite, while neurotransmitter release sites
(varicosities) occupy the distal third. Inputs and outputs are spatially displaced.

Methodologically, the authors build a passive ball-and-stick NEURON model of a reconstructed SAC
dendrite and drive it with simulated moving bars under four synaptic-input distributions matched in
total synapse count and mean density but differing only in spatial placement: the empirical skewed
distribution and a symmetric full-length distribution, each in two variants. This
**morphology-matched symmetric-input control** isolates the effect of input geometry from cable
properties, producing a clean comparison that has become the reference design in the field.
Two-photon Ca2+ imaging of individual varicosities and pharmacological isolation of the GABA-A
component provide the in-tissue test of the model predictions.

The key finding is that the measured proximal-restricted input distribution produces robust
outward-motion-preferring voltage at the distal release zone (varicosity DSI = 0.34 ± 0.23, n = 25),
whereas a density-matched symmetric input distribution does not. Only ~25% of DSGC-directed release
sites overlap with the excitatory receptive field. GABA-A blockade with gabazine reduces but does
not abolish the computation, confirming that dendritic mechanisms and circuit inhibition act
synergistically. Adding voltage-gated Ca2+ channels to the varicosities amplifies DS
multiplicatively but is not required to generate it.

For this project literature survey on how morphology-driven models shape DS, Vlasits2016 is the
canonical reference for two reasons. First, it is the clearest demonstration that synaptic-input
spatial statistics are a morphology-independent degree of freedom that must be respected by any
compartmental DS model. Second, its morphology-matched symmetric-input design is the methodological
template we should import when our own tasks compare cable theory, input placement, and active
channels as DS determinants. Any compartmental SAC or DSGC model we build that matches morphology
alone but ignores input placement should be expected to underestimate DS or distribute DS
incorrectly across the dendrite, and the numerical targets in this paper (varicosity DSI ~ 0.3,
input field extending to ~70% of dendritic radius, ~25% input-output overlap) are the benchmarks our
simulations should hit.
