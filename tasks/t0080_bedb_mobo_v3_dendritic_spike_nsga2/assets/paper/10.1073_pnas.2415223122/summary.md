---
spec_version: "3"
paper_id: "10.1073_pnas.2415223122"
citation_key: "Riccitelli2025"
summarized_by_task: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
date_summarized: "2026-05-04"
---
# Retinal ganglion cells encode the direction of motion outside their classical receptive field

## Metadata

* **File**: `files/riccitelli_2025_rgc-direction-extraclassical.pdf`
* **Published**: 2025 (online December 30, 2024; print January 7, 2025)
* **Authors**: Serena Riccitelli 🇮🇱, Hadar Yaakov 🇮🇱, Alina S. Heukamp 🇮🇱, Lea
  Ankri 🇮🇱, Michal Rivlin-Etzion 🇮🇱
* **Venue**: PNAS 2025, Vol. 122 No. 1, e2415223122
* **DOI**: `10.1073/pnas.2415223122`

## Abstract

Retinal ganglion cells (RGCs) typically respond to light stimulation over their spatially restricted
receptive field. Using large-scale recordings in the mouse retina, we show that a subset of
non-direction-selective (DS) RGCs exhibit asymmetric activity, selective to motion direction, in
response to a stimulus crossing an area far beyond the classic receptive field. The extraclassical
response arises via inputs from an asymmetric distal zone and is enhanced by desensitization
mechanisms and an inherent DS component, creating a network of neurons responding to motion toward
the optic disc. Pharmacological manipulations revealed the necessity of glycinergic amacrine cells
for this response. Using in vivo recordings, we identified similar extraclassical responses in
lateral geniculate nucleus neurons, suggesting such non conventional DS information is transferred
to downstream structures. Our results suggest a complex integration of motion direction processing
across the visual field, which arises beyond the classical receptive field boundaries.

## Overview

Riccitelli et al. demonstrate that direction selectivity in the mouse retina is not exclusive to the
canonical direction-selective ganglion cells (DSGCs). Using large-scale multielectrode array (MEA)
recordings on isolated mouse dorsal retinas, they identify a population of non-DS RGCs (about 12.7%
of recordings) that show asymmetric, direction-tuned firing to bars moving across an extraclassical
region well outside the classical center-surround receptive field. They name the firing that emerges
before the bar enters the classical RF the PRE response and the asymmetric distal source the
activation zone.

The authors show that PRE responses are predominantly carried by ON sustained RGCs, including
ON-alpha (M4), M2, and PixON types. The preferred directions of PRE responses are organized
centripetally; they point toward the optic disc, biasing population activity to detect motion moving
inward. Using static-bar mapping, central-area masking, and pharmacology, they dissect two
mechanisms behind direction tuning in the extraclassical RF: (i) desensitization of the classical
RF, which suppresses the response when the bar approaches from the null side after passing through
the center, and (ii) an inherent DS component within the activation zone itself, which survives
masking. Glycinergic amacrine cells (blocked by strychnine) and gap junctions (blocked by MFA) are
required for full PRE responses, pointing to a circuit involving wide-field amacrine cells.

Finally, in vivo Neuropixels recordings in anesthetized mice demonstrate that asymmetric PRE
responses are also present in dLGN, vLGN, and intergeniculate-leaflet neurons, showing the
extraclassical direction signal is propagated to downstream visual targets and is not pruned at the
retinal output stage.

## Architecture, Models and Methods

This is an experimental electrophysiology and pharmacology study, not a modelling paper. Subjects
are C57BL/6JOlaHsd wildtype mice. Two recording modalities are used.

Ex vivo MEA recordings: isolated dorsal retinas placed on multielectrode arrays. Visual stimuli
include (1) full-field flashed spots (polarity classification), (2) spatiotemporal white-noise
checkerboards (RF center estimation), (3) square-wave moving gratings, (4) moving bars (white on
black, 900 um and 300 um wide, moving at 400, 600, 800, 1000 um/s in 8 directions), (5) static
flashed bars (300 um wide, 500 ms duration, pseudorandom positions and orientations), and (6) moving
bars with central-area occlusion masks (700 um wide). The Central area is a 350 um radius disc
around each cell RF center; only cells with RF centers at least 450 um from the nearest retinal edge
(Distancemin) are included so that an extraclassical annulus exists.

Asymmetric PRE responses are quantified using the motion asymmetry index (mAI > 0.3), normalized
vector summation (NVS > 0.15), a minimal spike-count threshold per repetition, and a permutation
shuffling test. Pharmacology uses strychnine (1 uM, glycine receptors) and meclofenamic acid (MFA,
100 uM, gap junctions). RGC type assignment uses clustering on full-field-spot responses
cross-referenced to rgctypes.org and the EyeWire mouse RGC catalogue (cluster IDs 8w, 9w, 9n).

In vivo recordings: Neuropixels 1.0 probe inserted into the LGN of anesthetized head-fixed mice.
Stimuli are restricted to white-noise checkerboards and moving bars. Cells with RF centers near
screen edges are excluded. Statistics use two-sided Wilcoxon signed-rank tests, chi-square tests,
Fisher exact tests, Kuiper two-sample tests, Friedman with Tukey-Kramer correction, and Rao spacing
test. Data and code are deposited at Zenodo (`10.5281/zenodo.13119490`).

## Results

* **12.7 +/- 2.0%** of recorded mouse RGCs (mean +/- SEM, n = 2207 cells across 15 experiments)
  exhibit asymmetric PRE responses outside the classical RF
* **179 of 272** PRE RGCs are ON cells (P < 0.001, chi-square test); ON sustained RGCs dominate,
  including ONalpha/M4, M2, and PixON types (8w, 9w, 9n in EyeWire)
* PRE preferred directions are centripetal: temporal-dorsal mean vector **333.5 +/- 1.3 deg**,
  nasal-dorsal **182.8 +/- 1.1 deg** (P < 0.01, Kuiper test), pointing toward the optic disc
* Static flashed bars: preferred-side firing rate **16.67 +/- 0.98 spikes/s** vs. null-side **11.61
  +/- 0.72 spikes/s** (P < 0.001, n = 108)
* For 300 um moving bars in PRE-PD vs. POST-ND: **15.96 +/- 1.02 spikes/s** vs. **5.07 +/- 0.51
  spikes/s** (P < 0.001)
* Moving asymmetric index (mAI) **0.52 +/- 0.03** vs. static asymmetric index (sAI) **0.18 +/-
  0.02**, P < 0.001, indicating motion-specific enhancement
* **37 of 179** ON PRE RGCs (about 20%) show oppositely tuned POST responses (delta-PD = 176.83 +/-
  37.54 deg)
* Desensitization: spike rate to a static bar in the activation zone is **4.38 +/- 0.45 spikes/s**
  after central-area stimulation vs. **6.01 +/- 0.41 spikes/s** with no previous stimulation (P <
  0.001, n = 87)
* With central-area masked (desensitization removed): PRE-PD masked **15.98 +/- 1.47 spikes/s** vs.
  POST-ND masked **10.82 +/- 1.04 spikes/s** (P < 0.05, n = 70); confirms an inherent DS component
* Cluster 4 has the highest proportion (**75%**) of cells with an inherent DS component in the
  activation zone (P = 0.0136, Fisher exact test)
* Strychnine reduces PRE preferred-direction spikes from **8.09 +/- 0.85** to **3.63 +/- 1.34** (P <
  0.05, n = 15); MFA blocks PRE responses and reduces classical RF responses
* PRE preferred direction is stable across speeds 400-1000 um/s (delta-PD < 3 deg vs. 600 um/s
  reference); mAI lower at 400 um/s (**0.41**) than at 600/800/1000 um/s (**0.56, 0.51, 0.52**)
* In vivo LGN: **19/55** dLGN-region and **13/71** other-LGN cells show asymmetric PRE responses
  across dLGN, vLGN, and intergeniculate leaflet

## Innovations

### Direction selectivity outside the classical receptive field

The paper extends the concept of retinal direction selectivity beyond the canonical DSGC. It is the
first systematic demonstration that non-DS ON sustained RGCs encode motion direction specifically
through an extraclassical activation zone hundreds of micrometres outside their center-surround RF,
with a centripetal population code pointing toward the optic disc.

### Activation zone as a discrete RF substructure

The asymmetric activation zone is introduced as a distinct, spatially confined RF subregion (stable
for 250-350 um radii, shrinking for larger central exclusions). The paper provides explicit masking
and static-bar protocols to map it.

### Two-mechanism account: desensitization plus inherent DS

By combining central masking with directionally varied moving and static bars, the authors separate
two mechanisms; classical-RF desensitization that suppresses POST-ND responses, and an inherent DS
component intrinsic to the activation zone. This dissociation rules out either mechanism alone.

### Glycinergic-amacrine plus gap-junction circuit model

A circuit hypothesis (Fig. 6E) is proposed in which narrow-field ON glycinergic amacrine cells
provide tonic inhibition to ON PRE RGCs, wide-field amacrine cells in the activation zone disinhibit
them, and gap junctions provide direct electrical coupling. Strychnine and MFA pharmacology
corroborate both pathways.

### In vivo confirmation in LGN

Demonstrates that the asymmetric extraclassical direction signal survives transmission to dLGN,
vLGN, and IGL, refuting the assumption that LGN direction encoding is restricted to DSGC inputs in
the LGN shell.

## Datasets

* **Mouse multi-electrode array dataset**: light-evoked spike trains from C57BL/6JOlaHsd mouse
  dorsal retinas. 2207 RGCs across 15 experiments form the main RGC dataset; subsets of 272 PRE
  cells, 179 ON PRE RGCs, 108 mixed-bar-width cells, 87 PRE-only cells for desensitization tests, 70
  cells in masked-condition tests, 45 cells for speed tuning, 37 cells with paired PRE/POST, 15
  cells for strychnine pharmacology
* **Mouse in vivo Neuropixels LGN dataset**: 126 LGN units across dLGN, vLGN, and IGL with
  asymmetric PRE response data on a subset (19/55 in one region, 13/71 in another)
* **Availability**: All MEA data and figure-generation code are deposited at Zenodo
  (`10.5281/zenodo.13119490`) under the paper CC-BY 4.0 license. Cross-referenced cell-type
  identities draw on rgctypes.org and the EyeWire mouse RGC project (Bae et al. 2018; Goetz et al.
  2022\)

## Main Ideas

* Direction selectivity in the mouse retina is broader than the DRD4/Hb9 DSGC literature suggests;
  about 12.7% of RGCs encode motion direction through an extraclassical activation zone, providing
  population-level context for any single-cell DSGC model
* Even in DSGC compartmental modelling, sustained ON RGC types (ON-alpha/M4, M2, PixON) carry
  direction information through circuit-level wide-field-amacrine and gap-junction inputs that lie
  outside a single-cell biophysical substrate; this should be acknowledged as a limitation when
  fitting one cell to a single tuning curve
* Glycinergic-amacrine and gap-junction inputs can shape RGC spike output; project models that
  include only AMPA and GABA-A inputs (the t0080 substrate) may underestimate the diversity of
  direction-tuning mechanisms in non-DSGC types; relevant when comparing tuning-width metrics to
  general RGC literature
* The 350 um activation-zone radius and 450 um Distancemin define experimental scales for any future
  in-silico extraclassical-RF stimulus design that this project might explore
* The Zenodo dataset (`10.5281/zenodo.13119490`) is a candidate source for population-level mouse
  RGC firing-rate distributions if a project task ever needs out-of-DSGC RGC firing-rate benchmarks

## Summary

Riccitelli et al. ask whether direction selectivity in the mouse retina is restricted to the
canonical direction-selective ganglion cells, or whether it is also computed at the population level
by RGCs through the so-called extraclassical receptive field. They tackle this with large-scale ex
vivo MEA recordings of dorsal mouse retinas plus complementary in vivo Neuropixels recordings in the
LGN, and supplement the recordings with static-bar mapping, central-area occlusion masks, multiple
bar speeds, glycinergic-amacrine pharmacology, and gap-junction pharmacology.

Their methodology centres on a 350 um radius Central area mask that defines the classical RF
boundary and a Distancemin filter (450 um to retinal edge) that ensures every cell has a measurable
extraclassical annulus. Two motion-asymmetry metrics (mAI > 0.3, NVS > 0.15) plus permutation
shuffling identify the asymmetric PRE response. Static flashed bars locate the asymmetric activation
zone; centre masking dissociates desensitization from an inherent DS component; strychnine and MFA
reveal a wide-field-amacrine plus glycinergic plus gap-junction circuit; multi-speed bars
demonstrate speed invariance.

The headline findings are that **12.7%** of mouse RGCs (and a corresponding subset of LGN neurons)
encode motion direction outside their classical RF through an asymmetric activation zone, that their
preferred directions form a centripetal population code pointing toward the optic disc, that
direction tuning relies jointly on classical-RF desensitization and on an inherent DS component
inside the activation zone, and that glycinergic amacrine cells plus gap-junction coupling are
necessary for the full effect. The signal survives to dLGN, vLGN, and IGL.

For this project, the paper is broader population-coding context rather than a direct model target.
The neuron-channels project simulates an explicitly direction-selective DRD4 ON-OFF DSGC in NEURON,
so Riccitelli et al. occupy a complementary niche; they describe DS computations in non-DS RGCs that
arise from circuit-level interactions outside any single cell. The paper is relevant for framing the
t0080 v3 substrate (single-DSGC model) within the wider population-level direction-encoding
literature, for noting that the 5-fold AIS-Nav-density scaling debate concerns DRD4 DSGCs
specifically rather than the broader RGC population, and as a Zenodo data source if a later task
ever needs out-of-DSGC RGC firing benchmarks. It does not change the t0080 NSGA-II parameter bounds,
the dendritic-spike conductance ranges, or the AHP-tail metrics, but it strengthens the rationale
for the project narrow focus on the DRD4 cell type rather than generalising claims to RGC direction
encoding as a whole.
