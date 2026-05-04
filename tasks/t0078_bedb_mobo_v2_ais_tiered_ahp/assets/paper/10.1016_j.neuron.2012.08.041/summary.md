---
spec_version: "3"
paper_id: "10.1016_j.neuron.2012.08.041"
citation_key: "RivlinEtzion2012"
summarized_by_task: "t0078_bedb_mobo_v2_ais_tiered_ahp"
date_summarized: "2026-05-03"
---

# Visual Stimulation Reverses the Directional Preference of Direction-Selective Retinal Ganglion Cells

## Metadata

* **File**: `files/rivlin-etzion_2012_directional-preference-reversal.xml` (PMC NLM fulltext XML),
  `files/rivlin-etzion_2012_directional-preference-reversal.md` (markdown conversion)
* **Published**: 2012 (Neuron, Vol. 76, Issue 3, pp. 518-525)
* **Authors**: Michal Rivlin-Etzion 🇺🇸, Wei Wei 🇺🇸, Marla B. Feller 🇺🇸
* **Venue**: Neuron (Elsevier)
* **DOI**: `10.1016/j.neuron.2012.08.041`

## Abstract

Direction selectivity in the retina is mediated by direction selective ganglion cells. These cells
are part of a circuit in which they are asymmetrically wired to inhibitory neurons. Thus, they
respond strongly to an image moving in the preferred direction and weakly to an image moving in the
opposite (null) direction. Here, for the first time, we demonstrate that adaptation with short
visual stimulation of a direction selective ganglion cell using drifting gratings can reverse this
cell's directional preference by 180 degrees. This reversal is robust, long-lasting, and independent
of the animal's age. Our findings indicate that, even within circuits that are hardwired, the
computation of direction can be altered by dynamic circuit mechanisms that are guided by visual
stimulation.

## Overview

This paper challenges the prevailing "hardwired" model of direction selectivity in the mouse retina
by showing that brief drifting-grating adaptation can fully reverse the preferred direction (PD) of
ON-OFF direction-selective ganglion cells (DSGCs) by 180 degrees. The reversed PD is robust
(persisting for the duration of the recording, up to 23 minutes), insensitive to the animal's age,
and does not require the adapting stimulus to move along the original P-N axis. The same cell can
later be reverted by additional stimulation, indicating that "stable" and "reversed" cells are not
intrinsically different cell classes but distinct circuit states of a shared population.

Methodologically, the study uses two-photon-targeted loose-patch (cell-attached) recordings from
genetically identified posteriorly-tuned ON-OFF DSGCs in the DRD4-GFP and TRHR-GFP transgenic mouse
lines, plus whole-cell voltage clamp recordings to dissect synaptic mechanisms. Directional
preference is measured with a "DS test": 3 s of square-wave drifting gratings in 12 directions,
repeated 3-5 times in pseudo-random order, with cells classified as DS when both the vector-sum
magnitude exceeds 0.2 and the direction-selective index (DSI) exceeds 0.3.

The central mechanistic finding is that the reversed PD is mediated by a redistribution of
asymmetric inhibition rather than by changes in excitatory wiring: after adaptation, GABAergic
inhibitory currents become larger for the original PD (now the new ND) while excitatory currents
become larger for the original ND (now the new PD). Bath-applied gabazine (5 uM) abolishes the
reversed DS response, confirming GABA-A dependence. Additional experiments with the mGluR6 agonist
L-AP4 show that the ON pathway and ON-OFF crossover circuits play a critical role: blocking ON input
prevents most reversals and uncovers a delayed OFF response in the original ND that the ON pathway
normally masks.

Critically for this project, the paper reports paired DSI + mean preferred-direction firing rate
measurements from the same cells. Pre-adaptation, stable cells (n = 8) had DSI 0.78 +/- 0.19 and a
mean PD firing rate of 10.38 +/- 8.53 Hz over a 3 s grating window; reversed cells (n = 8) had DSI
0.63 +/- 0.23 and a mean PD firing rate of 9.95 +/- 5.42 Hz. These are spike rates from
cell-attached recordings of mouse posterior-preferring ON-OFF DSGCs (DRD4-GFP and TRHR-GFP
populations combined), not peak rates over sub-second windows. Post-adaptation, mean PD firing rates
dropped to 5.85 +/- 5.31 Hz (stable) and 2.73 +/- 2.68 Hz (reversed).

## Architecture, Models and Methods

This is an experimental electrophysiology paper, not a modelling paper; "architecture" refers to the
experimental and circuit-analysis design.

* **Animals**: Transgenic mouse lines DRD4-GFP and TRHR-GFP (both label posteriorly-tuned ON-OFF
  DSGCs) plus wild-type C57BL/6 controls. Both sexes, post-natal day P14 to P88. Reagents from the
  NIH MMRRC (DRD4-GFP 000231-UNC, TRHR-GFP 030036-UCD).
* **Preparation**: Flat-mount retina; recordings target GFP+ DSGCs identified by two-photon imaging.
* **Recording modes**: (a) Loose-patch cell-attached recordings to monitor spiking with minimal
  perturbation. (b) Whole-cell voltage-clamp recordings to isolate excitatory and inhibitory
  synaptic currents.
* **Visual stimulation**: Delivered through a 60x objective (Olympus LUMPlanFl/IR360/0.90W) over a
  ~225 um diameter field. Stimuli are square-wave drifting gratings.
* **DS test**: 3 s gratings in 12 directions (default 900 um/s, 225 um/cycle), 3-5 repetitions per
  direction, pseudo-randomly ordered. Variations cover 15 vs 30 deg/s speeds and 225 to 1800
  um/cycle spatial frequencies.
* **Adaptation protocols**: Four protocols, each inserted between two DS tests. P-N (40 s gratings
  in PD then 40 s in ND), Null only (40 s ND), P-O (40 s PD then 40 s orthogonal to P-N axis), and
  counter-phase (4-8 Hz contrast reversal, no motion). A no-stimulus 5-9 min gray-screen control was
  also run.
* **Tuning measures**: Vector sum of normalised responses across 12 directions (magnitude indicates
  tuning strength, angle defines PD). Direction-selective index DSI = (PD - ND) / (PD + ND), and
  DSI* recomputed against the post-adaptation PD. Cells classified as DS when vector-sum magnitude >
  0.2 and DSI > 0.3.
* **Reversal classification**: A cell whose post-adaptation PD differs from its pre-adaptation PD by
  more than 90 deg is "reversed"; less than 90 deg and still sharply tuned is "stable"; vector-sum
  magnitude < 0.2 or DSI* < 0.3 is "ambiguous".
* **Pharmacology**: Bath-applied gabazine (5 uM) to test GABA-A dependence; L-AP4 (5-20 uM) to block
  ON-bipolar input.
* **Statistics**: Mann-Whitney U for comparisons (e.g., stable vs reversed DSI: P < 0.02; PD rate
  pre- vs post-adapt: P < 0.01 for reversed cells, P < 0.02 for stable cells). Sample sizes: 74
  cells across all protocols; n = 24 P-N, n = 18 Null, n = 9 P-O, n = 12 counter-phase, n = 11
  control. Voltage-clamp synaptic measurements n = 9. L-AP4 cohort n = 21 (15 retained DS).
* **Data exclusion**: 14 of 88 GFP+ candidate DSGCs (16%) failed the DS-test threshold and were
  excluded.

## Results

* Of all DSGCs combined across protocols, **30 of 74 (41%)** reversed their preferred direction,
  **15 of 74 (20%)** became ambiguous (non-DS), and **29 of 74 (39%)** remained stable.
* Pre-adaptation stable cells had **DSI 0.78 +/- 0.19** with mean PD firing rate **10.38 +/- 8.53
  Hz** measured over the 3 s grating window; pre-adaptation reversed cells had **DSI 0.63 +/- 0.23**
  and mean PD firing rate **9.95 +/- 5.42 Hz** (mean +/- SD; n = 8 each subgroup; P < 0.02
  Mann-Whitney for DSI difference).
* Adaptation reduced mean PD firing rates significantly: **stable cells fell to 5.85 +/- 5.31 Hz**
  (P < 0.02) and **reversed cells fell to 2.73 +/- 2.68 Hz** (P < 0.01) over the same 3 s window.
* The Preferred-Null (P-N) protocol produced **38% reversal (9/24)**, **38% ambiguous (9/24)**, and
  **25% stable (6/24)**. Null-only adaptation: **22% reversed (4/18)**, **22% ambiguous (4/18)**,
  **56% stable (10/18)**. P-O adaptation: **44% reversed (4/9)**, **22% ambiguous (2/9)**, **33%
  stable (3/9)**. Counter-phase: **25% reversed (3/12)**, **17% ambiguous (2/12)**, **58% stable
  (7/12)** with no significant DSI change across the population.
* Reversal is GABA-A dependent: **bath-applied gabazine (5 uM) abolished the reversed DS response in
  4 of 4 cells**, increasing firing in all directions.
* Voltage-clamp recordings (n = 9) showed that after adaptation, **inhibitory currents became larger
  for the new ND (= original PD)** and **excitatory currents became larger for the new PD (=
  original ND)**, with simultaneous onset of E and I to ND gratings indicating shunting inhibition.
* Reversal is long-lasting: in 9 cells held for **2 to 23 minutes** post-adaptation, the reversed PD
  persisted for the entire recording.
* Vector-sum magnitudes were also lower for reversed (**0.38 +/- 0.17**) than stable (**0.53 +/-
  0.17**) cells (P < 0.01), reinforcing the conclusion that initial tuning sharpness predicts
  adaptation outcome.
* L-AP4 blockade of the ON pathway prevented most reversals: only **3 of 15 retained-DS cells
  (20%)** reversed under ON blockade, mean DSI fell from **0.54 +/- 0.23** to **0.18 +/- 0.63**, and
  **6 of 21 cells (29%)** stopped responding to gratings entirely. Post-adaptation, **40% (6/15)**
  of cells exhibited a new ON response despite mGluR6 blockade, implicating crossover circuits.

## Innovations

### First Demonstration that "Hardwired" Retinal Direction Selectivity is Plastic

Prior to this paper, the dominant model attributed retinal direction selectivity entirely to
asymmetric SAC-DSGC wiring (Briggman et al., 2011 EM reconstruction; Fried et al., 2002; Wei et al.,
2011). This study shows that despite that fixed anatomical scaffold, brief visual experience can
reverse a DSGC's preferred direction by 180 degrees, forcing a revision of the
"circuit-equals-function" assumption.

### Adaptation-Driven Redistribution of Asymmetric Inhibition

The paper establishes that the reversed PD is implemented not by new synaptic connections but by a
redistribution of which side of the cell receives the larger GABAergic inhibitory current.
Voltage-clamp recordings show inhibition flips from being ND-biased to PD-biased after adaptation,
while excitation flips in the opposite sense. This is the first direct synaptic-current
demonstration of a flexible inhibition-driven directional code in the retina.

### Crossover ON-OFF Circuits Required for Reversal

By blocking ON-bipolar input with L-AP4, the authors uncover a delayed OFF response that is normally
masked by the ON pathway and that becomes the carrier of the new PD after adaptation. This is the
first paper to assign a functional role to ON-OFF crossover circuits in adaptive direction
computation.

### Paired DSI plus Long-Window Mean Firing Rate Reporting

The supplemental Figure S2/S3 panels report DSI and mean PD firing rates measured on the **same
cells** over a fixed 3 s grating window. Most prior DSGC papers report either DSI alone (often via
peak rates) or report rates over short sub-second windows. The paired joint measurement is what
makes this paper a clean reference for calibrating model utopia points and pass criteria.

## Datasets

This is an in-vitro electrophysiology paper rather than a publicly released computational dataset.
Primary data are spike trains and voltage-clamp current traces from 88 candidate DSGCs (74 retained
after DS-test screening) across multiple protocols, plus 21 cells in the L-AP4 condition. Animals:
DRD4-GFP and TRHR-GFP transgenic mice (NIH MMRRC, IDs 000231-UNC and 030036-UCD respectively) and
C57BL/6 wild type. The summary statistics relevant to this project (DSI 0.78 +/- 0.19 with mean PD
rate 10.38 +/- 8.53 Hz for stable cells, n = 8; DSI 0.63 +/- 0.23 with mean PD rate 9.95 +/- 5.42 Hz
for reversed cells, n = 8) are reported in Supplementary Figure S2/S3 and Table S1. The raw data
themselves are not deposited in a public archive; the methods, analysis code, and processed
statistics are described in the main text and supplement.

## Main Ideas

* **Pass-criterion anchor for t0078**: The paper provides a paired joint measurement of **DSI 0.78
  +/- 0.19** and mean preferred-direction firing rate **10.38 +/- 8.53 Hz** in the same mouse ON-OFF
  DSGCs (DRD4-GFP / TRHR-GFP, n = 8 stable cells, 3 s grating window). This is the cleanest
  peer-reviewed source justifying revising the t0078 pass criterion from "DSI >= 0.4 AND PD rate >=
  30 Hz" to "DSI >= 0.4 AND PD rate >= 10 Hz". The 30-80 Hz target previously used in the project
  conflated peak firing rates from short windows with mean rates from long windows; the
  Rivlin-Etzion mean-rate baseline is 10.4 Hz, not 30+ Hz.
* **Utopia-point recalibration**: For Bayesian-optimisation hypervolume metrics, the utopia point
  should sit at approximately **(DSI 0.78, PD rate 10 Hz)** for mouse ON-OFF DSGCs measured over a 3
  s window, rather than the previously used (0.7, 80 Hz). Hypervolume comparisons across t0076 and
  t0078 must use this corrected reference for meaningful cross-task interpretation.
* **DSI computation convention**: The paper computes DSI as a polar-plot vector-sum metric over
  spike counts in a 3 s window across 12 directions, equivalent to the project-standard 8-direction
  polar DSI used in t0076. This confirms that the t0078 DSI computation should remain the
  polar/vector-sum form and not be replaced with a peak-rate ratio (which gives systematically
  higher values and is not directly comparable).
* **Stimulation protocol design hint**: The paper's "DS test" uses 3 s grating presentations in
  multiple directions; the t0078 trial length of 1400 ms is shorter than the published convention,
  which means "mean PD rate" in t0078 is computed over a window narrower than Rivlin-Etzion's 3 s
  window. If t0078 reports mean rates that fall slightly above the Rivlin-Etzion baseline, that may
  partly reflect the shorter integration window rather than a model-versus-data discrepancy.
* **Plasticity caveat for downstream tasks**: The paper shows that DSGC directional tuning is not
  fixed even on a minutes timescale. Future tasks that try to fit a single DSGC tuning curve to
  experimental data should use the **pre-adaptation** values as targets and treat
  post-adaptation/reversed values as a separate state, not aggregate them.

## Summary

Rivlin-Etzion, Wei, and Feller (2012, Neuron) ask whether the direction-selective response of mouse
ON-OFF retinal ganglion cells is rigidly determined by the asymmetric SAC-DSGC wiring revealed by EM
reconstruction, or whether it can be reshaped by recent visual experience. Their work targets the
dominant "hardwired retina" view of direction selectivity and tests it directly by applying brief
drifting-grating adaptation protocols and measuring whether DSGC preferred direction remains stable.

The methodology combines two-photon-targeted loose-patch recordings from genetically labelled
posterior-preferring ON-OFF DSGCs (DRD4-GFP and TRHR-GFP lines, P14-P88, both sexes) with whole-cell
voltage clamp to dissect synaptic mechanisms, plus pharmacology with gabazine to test GABA-A
involvement and L-AP4 to test ON-pathway involvement. Directional tuning is quantified with DSI and
vector-sum metrics computed from 3 s grating responses in 12 directions, using a pre/adaptation/post
design with four adaptation protocols (P-N, Null, P-O, counter-phase) plus a no-stimulus control.

The authors find that drifting-grating adaptation can fully reverse the PD of a substantial fraction
of ON-OFF DSGCs (41% of 74 cells across protocols) and that this reversal is robust, long-lasting
(persisting up to 23 min), GABA-A dependent, and mediated by a redistribution of asymmetric
inhibition rather than by new wiring. ON-pathway crossover circuits are necessary for the reversal:
L-AP4 blockade reduces reversal probability and reveals a delayed OFF response normally masked by
the ON pathway. Critically, the paper reports paired DSI plus mean preferred-direction firing rate
from the same cells: **DSI 0.78 +/- 0.19 with mean PD rate 10.38 +/- 8.53 Hz** for stable cells (n =
8\) and **DSI 0.63 +/- 0.23 with 9.95 +/- 5.42 Hz** for reversed cells (n = 8), measured over the 3
s grating window.

For task t0078, this paper is the primary literature anchor for revising the project's pass
criterion from "PD rate >= 30 Hz" to "PD rate >= 10 Hz". The previously assumed 30-80 Hz mean PD
firing rate range conflated peak rates over sub-second windows with mean rates over multi-second
windows; this paper establishes that the mean PD firing rate of mouse ON-OFF DSGCs is approximately
10 Hz when measured over a 3 s window, with paired DSI of 0.78. The result also informs the
Bayesian-optimisation utopia point used to compute hypervolume in t0078 and downstream model
selection. A secondary implication for downstream tasks is that DSGC tuning is plastic on a minutes
timescale, so model-fitting tasks should treat pre-adaptation values as the canonical target and not
aggregate them with post-adaptation states.
