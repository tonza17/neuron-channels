---
spec_version: "3"
paper_id: "10.1038_s41467-024-46234-7"
citation_key: "Aldor2024"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# Dendritic mGluR2 and perisomatic Kv3 signaling regulate dendritic computation of mouse starburst amacrine cells

## Metadata

* **File**: `files/aldor_2024_sac-mglur2-kv3.pdf`
* **Published**: 2024-02-28
* **Authors**: Hector Acaron Ledesma 🇺🇸, Jennifer Ding 🇺🇸, Swen Oosterboer 🇺🇸, Xiaolin Huang 🇺🇸,
  Qiang Chen 🇺🇸, Sui Wang 🇺🇸, Michael Z. Lin 🇺🇸, Wei Wei 🇺🇸
* **Venue**: Nature Communications 15:1819 (2024)
* **DOI**: `10.1038/s41467-024-46234-7`

## Abstract

Dendritic mechanisms driving input-output transformation in starburst amacrine cells (SACs) are not
fully understood. Here, we combine two-photon subcellular voltage and calcium imaging and
electrophysiological recording to determine the computational architecture of mouse SAC dendrites.
We found that the perisomatic region integrates motion signals over the entire dendritic field,
providing a low-pass-filtered global depolarization to dendrites. Dendrites integrate local synaptic
inputs with this global signal in a direction-selective manner. Coincidental local synaptic inputs
and the global motion signal in the outward motion direction generate local suprathreshold calcium
transients. Moreover, metabotropic glutamate receptor 2 (mGluR2) signaling in SACs modulates the
initiation of calcium transients in dendrites but not at the soma. In contrast, voltage-gated
potassium channel 3 (Kv3) dampens fast voltage transients at the soma. Together, complementary
mGluR2 and Kv3 signaling in different subcellular regions leads to dendritic compartmentalization
and direction selectivity, highlighting the importance of these mechanisms in dendritic computation.

## Overview

This paper dissects how two classes of membrane conductances — dendritic mGluR2 and perisomatic Kv3
— shape direction-selective dendritic computation in mouse starburst amacrine cells (SACs). The
authors use simultaneous two-photon voltage imaging with the genetically encoded indicator ASAP3,
calcium imaging with GCaMP6f, and whole-cell patch-clamp recordings to measure subcellularly
resolved responses to moving-bar stimuli. By pharmacologically blocking mGluR2 (with LY341495) and
Kv3 channels (with low-dose 1 mM extracellular TEA), they isolate how each mechanism contributes to
the soma-vs-dendrite partitioning of motion signals.

**Borderline note — SAC, not DSGC**: this paper concerns the direction-selective interneuron
(starburst amacrine cell), not the direction-selective ganglion cell (DSGC). SACs produce
dendrite-branch-specific GABA release that in turn drives DSGC directional tuning. Findings here
bear on upstream mechanisms of retinal DS rather than DSGC spiking per se.

**Critical note — morphology was NOT swept**: despite the task framing, this paper does not
construct a compartmental biophysical model, nor does it systematically vary SAC morphology. The
study is fundamentally experimental. The spatial element enters through (a) endogenous biological
localization — Kv3 is anatomically restricted to the perisomatic region while mGluR2 is distributed
dendritically, confirmed by immunostaining — and (b) imaging at multiple radial distances from the
soma (0, 15, 35, 65, 85, 105 µm) to characterize how directional calcium responses depend on
dendritic location. Channel densities are not parametrically manipulated. The paper cites Tukker,
Taylor & Smith (2004) for prior compartmental modeling of SAC DS but does not extend that modeling
work. For a morphology-focused computational survey, Aldor2024 contributes ground-truth empirical
constraints on where along the dendrite each conductance acts and what DS-relevant observables
(directional calcium, somatic Vm variance, calcium channel threshold) each conductance controls — it
does not contribute a morphology sweep.

## Architecture, Models and Methods

**Preparation**: Whole-mount retinas from adult Chat-IRES-Cre mice crossed with floxed tdTomato
reporters, targeting On SACs in ventral retina. Animals of both sexes were used. Experiments follow
University of Chicago IACUC protocols.

**Stimuli**: Moving bright bar 275 µm × 440 µm traveling at 440 µm/s across the SAC receptive field,
focused on outer-segment plane. Direction-selectivity is assessed by comparing inward (centripetal,
tip-to-soma) versus outward (centrifugal, soma-to-tip) motion along individual dendritic branches.

**Voltage imaging**: ASAP3 (gift from M. Lin) introduced into SACs, imaged with a two-photon
microscope. Simultaneous somatic voltage-clamp with ASAP3 imaging converts fluorescence to mV via a
per-cell calibration curve spanning -95 to -5 mV. ROIs placed at 0, 15, 35, 65, 85, 105 µm from the
soma.

**Calcium imaging**: GCaMP6f (gift from S. Wang) expressed in SACs, two-photon imaged along
individual dendritic branches at matched radial locations; responses normalized and binned by
fractional dendritic radius.

**Electrophysiology**: Whole-cell patch-clamp in current- or voltage-clamp with K+-based (recording
Kv3 conductance) or Cs+/TEA-internal (blocking intracellular K+) pipette solutions, 3.5-4.5 MΩ
electrodes.

**Pharmacology**: LY341495 (selective mGluR2 antagonist) bath-applied to block endogenous mGluR2
signaling; 1 mM external TEA to selectively block Kv3 (validated against mouse bipolar cells which
lack Kv3); ω-conotoxin + ω-agatoxin to confirm N/P/Q-type VGCC dependence; paired SAC-DSGC
recordings validate downstream directional IPSC.

**Statistics**: Two-sided paired/unpaired t-test, Kolmogorov-Smirnov, ANOVA, Bonferroni correction.
Cell counts reported per experiment (typical n = 6-17 cells). Data reported as mean ± SEM. No formal
biophysical/compartmental model is constructed.

## Results

* **Global low-pass perisomatic signal**: a moving bar produces a slow somatic depolarization that
  accrues as the bar crosses the entire receptive field; restricting the bar to a 66 µm stripe 110
  µm from the soma still drives somatic Vm, demonstrating that perisomatic potential reflects
  integration across the whole dendritic field rather than local input only.
* **Direction selectivity emerges at the outer half of the dendrite (~distal 50% of dendritic
  radius)**: normalized GCaMP6f responses are weak and non-directional at the soma and proximal
  half; an abrupt step-increase in outward-tuned calcium response appears beyond ~0.5 of fractional
  dendritic radius (Kolmogorov-Smirnov **p < 0.01, n = 11 cells**).
* **mGluR2 blockade abolishes dendritic DS by releasing inward calcium transients**: LY341495
  application causes previously weak inward responses to become suprathreshold in the distal half of
  dendrites (paired t-test **p = 0.03, n = 10 cells**); outward response amplitude is essentially
  unchanged, and somatic calcium and somatic Vm waveforms are unaffected — confirming mGluR2 acts
  dendritically, not perisomatically.
* **mGluR2 raises the VGCC activation threshold**: in voltage-clamp ramps, LY341495 shifts the
  N/P-Q-type calcium-current activation to a more hyperpolarized threshold (paired t-test **p =
  0.0002, n = 10 cells**). mGluR2 blockade also prolongs distal dendritic calcium-transient
  half-width, consistent with increased VGCC conductance.
* **Kv3 (1 mM TEA) selectively dampens fast somatic Vm transients without changing resting potential
  or slow depolarization**: resting Vm control **-64.8 ± 1.2 mV (n = 17)** vs. TEA **-66.4 ± 3.1 mV
  (n = 7)**, n.s.; slow moving-bar depolarization 19.9 ± 0.9 mV vs. 21.2 ± 1.8 mV, n.s.; somatic Vm
  variance **1.6 ± 2.5 (control, 6 cells)** vs. **4.3 ± 1.5 under TEA (5 cells)**, **p = 0.006** —
  Kv3 specifically suppresses fast voltage transients >15 mV at the soma.
* **Complete K+ block reveals additional somatic conductances**: Cs-based/5 mM TEA internal solution
  elevates resting Vm to **-36.7 ± 3.7 mV (n = 12)**, ANOVA p < 0.0001, and produces even larger
  transients, indicating Kv3 is the dominant but not exclusive perisomatic K+ conductance.
* **Kv3 + mGluR2 co-blockade abolishes DSGC direction selectivity**: simultaneous LY341495 + 1 mM
  TEA drives DSGCs into tonic inhibition and eliminates directional tuning of postsynaptic IPSCs in
  paired SAC-DSGC recordings, demonstrating that both mechanisms together are required for
  functional compartmentalization.
* **Immunostaining anatomy**: Kv3.1 protein is restricted to a ring around the SAC soma, while
  mGluR2 is distributed throughout the dendritic plexus, giving each conductance a distinct
  subcellular substrate.

## Innovations

### First subcellular voltage readout of SAC dendrites during motion

This is the first use of ASAP3 genetically encoded voltage imaging to track moving-bar-evoked Vm
along individual SAC dendrites. Prior work relied on somatic patch-clamp or calcium imaging, which
either lack spatial resolution or report only suprathreshold calcium entry. ASAP3 reveals the
subthreshold global signal that drives dendrite-local direction selectivity.

### Pharmacological separation of dendritic vs. perisomatic control of DS

By showing that LY341495 (mGluR2) alters only dendritic calcium transients while 1 mM TEA (Kv3)
alters only somatic fast Vm, the paper provides a clean subcellular dissociation: two different
conductances, anatomically and functionally separated, implement two halves of the SAC DS
computation.

### Two-mechanism model of SAC compartmentalization

The paper proposes a concentric-architecture scheme (their Fig. 9) where Kv3 enforces a stable
global voting signal at the soma and mGluR2 sets the threshold for directional calcium spikes in
distal dendrites. This refines and mechanistically grounds earlier shunt-based proposals (Vlasits
2016; Koren et al. 2017).

## Datasets

This is a primary experimental study; no publicly released datasets are created or consumed.

* **Animals**: Chat-IRES-Cre × floxed-tdTomato mice; pharmacology rather than genetic knockout is
  used.
* **Sample sizes**: n = 5-17 cells per condition, typical across experiments; individual experiments
  range 2-17 cells.
* **Source data**: Source-data Excel files are provided per Nature Communications policy at the
  article page.
* **Genetic tools**: ASAP3 plasmid (Michael Lin lab, Stanford); GCaMP6f (Sui Wang lab, Stanford).

## Main Ideas

* **SAC direction selectivity is a compartmentalized two-mechanism computation**: Kv3 keeps the soma
  quiet and non-directional (low-pass global signal), while mGluR2 sets the dendritic VGCC threshold
  so that only coincident local + global depolarization (outward motion) triggers suprathreshold
  calcium. For any DS model of SAC dendrites, both mechanisms must be present or the model cannot
  reproduce the DS collapse seen under TEA + LY341495.
* **Anatomical localization is the morphology-dependent variable here, not branch geometry**: the
  paper morphology dependence is the fact that Kv3 and mGluR2 live at different subcellular
  locations relative to the soma. Modelers cannot lump both into a single uniform density —
  perisomatic-only Kv3 and dendritic-only mGluR2 distributions are required to match the
  experimental phenotype.
* **VGCC activation threshold is mGluR2-tunable** (**threshold shift ~5-10 mV**, paired t-test p =
  0.0002): any compartmental SAC model that assumes fixed VGCC thresholds will misrepresent
  endogenous DS because threshold is a dynamic, neuromodulatory variable.
* **Low-pass global somatic depolarization (~20 mV slow, variance ~1.6 mV^2 under control) is the
  substrate that dendritic local inputs are biased against** — models that electrotonically isolate
  dendrites from soma will miss this shared global signal.
* **Aldor2024 (Ledesma 2024) is a constraint source, not a modeling source**: for a morphology
  survey it should be cited as an empirical ground-truth target against which compartmental models
  are validated, rather than a methodological example of morphology-parameter sweeps.

## Summary

This Nature Communications paper from the Wei lab at the University of Chicago (with genetic-tool
collaborations from the Lin and Wang labs at Stanford) uses genetically encoded voltage (ASAP3) and
calcium (GCaMP6f) imaging together with whole-cell patch-clamp to ask how starburst amacrine cell
dendrites convert concentrically distributed synaptic inputs into branch-specific
direction-selective outputs. The study focuses on two specific membrane conductances — metabotropic
glutamate receptor 2 (mGluR2) and voltage-gated potassium channel Kv3 — whose subcellular
distributions are non-uniform: Kv3 clusters around the soma while mGluR2 extends throughout the
dendritic arbor.

Methodologically, the authors combine subcellular two-photon imaging at multiple radial distances
(0-105 µm from soma) with targeted pharmacology: LY341495 to block endogenous mGluR2 signaling and 1
mM TEA to selectively block Kv3 while leaving bipolar-cell excitatory inputs intact. Paired SAC-DSGC
recordings verify that manipulations at the SAC level propagate to direction-selective ganglion-cell
IPSCs. No biophysical compartmental model is constructed; this is a strictly experimental paper.

The headline findings are: (1) direction-selective calcium transients emerge abruptly only in the
distal half of each SAC dendrite; (2) mGluR2 blockade releases suprathreshold calcium in the inward
direction by lowering the VGCC activation threshold (paired t-test p = 0.0002, n = 10), abolishing
dendritic DS while leaving somatic responses untouched; (3) Kv3 blockade triples somatic Vm variance
(1.6 -> 4.3 mV^2, p = 0.006) and introduces fast transients >15 mV at the soma without changing slow
depolarization; (4) co-blockade of both eliminates DSGC direction selectivity downstream,
demonstrating that the two mechanisms are jointly necessary.

For this project literature survey on how morphology shapes direction selectivity via computational
modeling, Aldor2024 (Ledesma et al. 2024) is a borderline inclusion. It is SAC rather than DSGC
biology, and — critically — it does not perform morphology sweeps or build a compartmental model.
Its contribution to a morphology-focused survey is as an empirical constraint: it identifies two
anatomically localized conductances that any honest compartmental SAC DS model must include with
their correct spatial distributions (perisomatic Kv3, dendritic mGluR2), and it quantifies the
DS-relevant observables (calcium threshold shifts, somatic Vm variance, directional calcium onset at
fractional radius ~0.5) that such a model must reproduce. Use it as a validation target when
sweeping morphology or channel distribution in a SAC model; do not cite it as a morphology-sweep
example.
