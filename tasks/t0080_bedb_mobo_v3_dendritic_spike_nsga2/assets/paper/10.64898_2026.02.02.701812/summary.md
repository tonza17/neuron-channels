---
spec_version: "3"
paper_id: "10.64898_2026.02.02.701812"
citation_key: "Pitcher2026"
summarized_by_task: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
date_summarized: "2026-05-04"
---

# Retinal Waves Shape Starburst Amacrine Cell Dendrite Development Through a Direction-Selective Dendritic Computation

## Metadata

* **File**: `files/pitcher_2026_sac-dendrite-retinal-waves.pdf`
* **Published**: 2026-02-04 (bioRxiv preprint)
* **Authors**: Miah N. Pitcher (US), Aanica S. B. Gonzales (US), Raul Habib (US),
  Marla B. Feller (US)
* **Venue**: bioRxiv
* **DOI**: `10.64898/2026.02.02.701812`

## Abstract

During development, dendrites undergo structural plasticity in response to neural activity;
however, whether spatiotemporal activity patterns can instruct dendritic growth remains unclear.
Prior to vision, the developing mouse retina exhibits spontaneous retinal waves with a nasal
propagation bias that mimics forward optic flow. Here, we reveal that starburst amacrine cells use
direction-selective dendritic computations to transform this propagation bias into asymmetric
dendrite growth, linking activity patterns to structural development.

## Overview

This paper shows that starburst amacrine cell (SAC) dendrites perform direction-selective dendritic
computations during development, not just in adulthood, and that this computation reads out the
nasal propagation bias of stage-3 retinal waves to drive asymmetric dendrite outgrowth. The work
ties together two previously separate findings: that SACs have compartmentalised, centrifugally
tuned dendrites in the adult, and that retinal waves before P11 propagate preferentially in a
nasal direction.

The authors show with two-photon calcium imaging in mouse retina aged P7-P13 that SAC dendrites
already exhibit centrifugal-preferred direction selectivity to retinal waves by P10, with tuning
strength rising as a function of distance from the soma. Disrupting wave activity (b2-nAChR
knockout) reduces SAC dendrite length and complexity at P8; disrupting wave propagation bias
(FRMD7tm) abolishes the nasal-versus-temporal asymmetry in dendritic outgrowth at P9-P11.
Pharmacologically blocking the K+ channel Kv3.1 (with TEA), which normally electrically
compartmentalises adult SAC dendrites, abolishes the direction selectivity in young SAC dendrites
as well, establishing that the same biophysical mechanism (compartmentalisation plus
spatiotemporal summation) underlies both the developmental and adult computation.

The paper does not measure DSGC firing or DSGC IPSC amplitudes directly. It is a SAC morphology
and SAC dendritic-Ca2+ paper, with implications for downstream DSGC tuning that the authors note
in the discussion but do not test.

## Architecture, Models and Methods

The study is an experimental neuroscience paper, not a modelling paper. Methods cover:

* **Mouse models**: ChAT-Cre/nGFP for SAC labeling, b2-nAChR knockout (disrupts cholinergic
  retinal waves), FRMD7tm (loss-of-function in *FRMD7*; reduces wave propagation bias without
  abolishing waves themselves). Ages P7 to P120, both sexes.
* **Two-photon calcium imaging** of single SAC dendrites at 5.92 Hz, 128 x 128 pixels, with
  920 nm excitation. SACs filled with 8 mM Calbryte 520 via sharp-electrode iontophoresis
  (100-150 MOhm pipettes, -10 to -20 nA, 500 ms pulses). Recordings at ~32 deg C in oxygenated
  Ames media (light experiments) or ACSF (wave experiments).
* **Stimuli**: moving bars (25 x 500 um) at 500 um/s in 8 pseudorandomised directions, delivered
  via DMD with UV LED (375 nm) on the fast-axis scan flyback to avoid PMT contamination.
* **Direction selective index for waves (DSI_wave)**: normalised difference in calcium response
  between centrifugal-propagating and centripetal-propagating waves per dendritic quadrant.
* **Pharmacology**: bath TEA to block multiple K+ channels including Kv3.1, the channel known
  to electrically compartmentalise adult SAC dendrites near the soma.
* **Morphology**: SACs filled with 2 mM Alexa Fluor 594 and reconstructed in 3D for total
  dendrite length, distal complexity (Sholl-style), and per-quadrant dendritic density.
* **Statistics**: per-cell DSI distributions, with cell size and dendrite distance as
  continuous predictors. Sample sizes are reported per figure (typically n = 5-15 cells per
  condition, dendrite-level n in the tens).

The relevant biophysical claim for compartmental modelling is that **Kv3.1 in proximal SAC
dendrites is necessary and (in combination with cable summation) sufficient** for the
direction-selective dendritic computation in young SACs, just as in adults, because TEA
abolishes the directional tuning while leaving the wave stimulus intact.

## Results

* SAC dendrites first exhibit consistent direction-selective responses to moving bars at **P12**,
  prior to eye opening. Tuning at P12-P13 is comparable to adult.
* SAC dendrites show direction-selective responses to retinal **waves** by **P10**, with stronger
  centrifugal than centripetal responses.
* DSI_wave correlates with cell size: **larger SACs show stronger directional tuning**, consistent
  with cable-theory summation along the dendrite.
* In P9-P11 SACs, tuning strength **increases monotonically with distance from the soma** along
  individual dendrites, due to selective enhancement of the centrifugal response. This mirrors
  the distance-dependent tuning seen in adult SACs.
* **TEA bath application** abolishes the directional tuning of SAC dendrites at P9-P11; they
  respond equally to all wave directions, without changing wave propagation statistics or
  saturating the calcium sensor. Implicates Kv3.1 (and other K+ channels) in the developmental
  computation.
* **b2-nAChR knockout** SACs (no cholinergic waves) show significantly reduced spontaneous
  calcium transients at P8 and significantly **reduced total dendrite length and complexity at
  P8** versus littermate controls.
* In wild-type P9-P11 SACs the **nasal quadrant has greater dendritic length and distal
  complexity than the temporal quadrant**, consistent with preferential activation by
  nasalward-propagating waves.
* **FRMD7tm** SACs (reduced wave propagation bias) show no nasal-vs-temporal asymmetry in
  dendrite length or density, while still computing wave direction at the dendrite level. This
  decouples the direction-selective dendritic computation from the wave bias and shows that the
  bias is required to translate the computation into asymmetric growth.
* In wild-type SACs, nasal dendrites have higher peak DSI_wave than temporal dendrites due to
  their greater length; in FRMD7tm there is no such peak-tuning difference.

## Innovations

### Direction-selective dendritic computation appears before light responses

First demonstration that the canonical SAC centrifugal-preferred dendritic computation is
operational at P10, days before the retina becomes light-responsive at P12, using spontaneous
retinal waves as the natural drive.

### Activity propagation bias as an instructive signal for dendrite morphology

First evidence that the spatiotemporal *direction* of population activity (not just rate or
correlation) instructs dendritic structural development. Hebbian-style covariance rules cannot
explain the nasal-vs-temporal asymmetry; a subcellular direction-selective decoder is required.

### Mechanistic chain from waves to DSGC circuitry

Connects the previously isolated facts that (a) waves have a nasal bias, (b) FRMD7tm and
b2-nAChR-KO mice have abnormal direction-selective ganglion-cell circuitry along the
horizontal axis, and (c) SAC dendrites compartmentalise via Kv3.1, into a single causal chain
in which SAC dendrite asymmetry is the developmental hinge between wave statistics and adult
DSGC tuning.

## Datasets

This is a primary experimental neuroscience paper using new mouse retinal recordings. No public
datasets were used or released as such. Reagents: ChAT-Cre (Jackson #031661), nGFP (Jackson
#008516), FRMD7tm (MMRRC #047759-UCD), and an in-house b2-nAChR knockout line. Calcium-imaging
movies and SAC reconstructions are not stated to be deposited in a public repository in the
preprint.

## Main Ideas

* SAC dendritic direction-selectivity is in place before vision and is driven by the same
  Kv3.1-mediated compartmentalisation plus cable summation that operates in the adult, so any
  compartmental SAC model in this project should expect the centrifugal-preferred computation
  to be present at the developmental ages of the source data.
* The nasal-temporal asymmetry in SAC dendritic outgrowth provides an *anatomical* asymmetry
  upstream of DSGC inhibition that the t0080 substrate (Bed B) holds fixed via a stylised
  symmetric SAC drive. This paper does not change t0080's substrate but flags that the assumed
  symmetry is a developmental simplification that becomes inaccurate in mouse models with
  altered waves.
* Directly relevant *biological prior* for follow-up tasks: if a future task ever varies the
  inhibitory machinery onto the DSGC, the asymmetric SAC dendrite reach reported here is a
  candidate source for asymmetric IPSC amplitude/kinetics on the null-side dendrite, but
  reproducing this would require modelling SAC growth, not the DSGC itself.

## Summary

Pitcher et al. ask whether spontaneous retinal waves can instruct dendritic morphology through a
local dendritic computation, using developing mouse SACs as a model. The work spans calcium
imaging in P7-P13 retina, pharmacological dissection with TEA, two genetic models (b2-nAChR-KO
for activity loss, FRMD7tm for loss of wave propagation bias), and 3D dendrite reconstructions
across the same ages.

The methodology combines two-photon imaging of GCaMP-loaded single SAC dendrites with
quadrant-resolved DSI metrics for moving bars and propagating waves, plus reconstruction-based
quantification of nasal-vs-temporal dendrite length and distal complexity. The experimental
design is elegant: it shows that the dendritic computation is present (P10 imaging), that it
depends on K+-channel-based compartmentalisation (TEA experiment), that activity is required
for outgrowth (b2-nAChR-KO), and that wave *direction*, not just wave existence, is required
for the morphological asymmetry (FRMD7tm).

The headline finding is that SAC dendrites at P9-P11 exhibit centrifugal-preferred direction
selectivity to retinal waves; that dendritic tuning rises with distance from the soma; that
TEA abolishes this tuning; and that wild-type SACs have nasal dendrites longer than temporal
dendrites (a difference absent when wave propagation bias is removed). Together these results
identify SACs as the earliest known cellular decoder of retinal-wave propagation bias and link
that decoding to a structural morphological asymmetry that persists into the adult
direction-selective circuit.

For this project the paper is upstream context, not a direct input. t0080 (Bed B v3) treats the
SAC drive onto the DSGC as a fixed, idealised null-side inhibitory waveform; it does not model
SAC morphology development. Pitcher 2026 is therefore relevant only as developmental background
for *why* the SAC inhibitory drive has its asymmetric form in the mature retina, and as a
flagged source of biological asymmetry that future tasks could optionally model if the
inhibitory machinery onto the DSGC is ever brought back into the optimisation.
