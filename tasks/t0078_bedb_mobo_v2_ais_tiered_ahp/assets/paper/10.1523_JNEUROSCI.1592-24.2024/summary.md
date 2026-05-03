---
spec_version: "3"
paper_id: "10.1523_JNEUROSCI.1592-24.2024"
citation_key: "Werginz2024"
summarized_by_task: "t0078_bedb_mobo_v2_ais_tiered_ahp"
date_summarized: "2026-05-03"
---
# Differential Intrinsic Firing Properties in Sustained and Transient Mouse alpha-RGCs

## Metadata

* **File**: `files/werginz_2024_alpha-rgc-firing.pdf`
* **Published**: 2024-11-08
* **Authors**: Paul Werginz (AT), Viktoria Kiraly (AT), Guenther Zeck (AT)
* **Venue**: The Journal of Neuroscience (Vol. 45, Issue 2, e1592242024)
* **DOI**: `10.1523/JNEUROSCI.1592-24.2024`

## Abstract

Retinal ganglion cells (RGCs) are the neuronal connections between the eye and the brain conveying
multiple features of the outside world through parallel pathways. While there is a large body of
literature on how these pathways arise in the retinal network, the process of converting presynaptic
inputs into RGC spiking output is little understood. In this study, we show substantial differences
in the spike generator across three types of alpha-RGCs in female and male mice, the alpha-ON
sustained, alpha-OFF sustained, and alpha-OFF transient RGC. The differences in their intrinsic
spiking responses match the differences in the light responses across RGC types. While sustained RGC
types have spike generators that are able to generate sustained trains of action potentials at high
rates, the transient RGC type fired shortest action potentials enabling it to fire high-frequency
transient bursts. The observed differences were also present in late-stage photoreceptor-degenerated
retina demonstrating long-term functional stability of RGC responses even when presynaptic circuitry
is deteriorated for long periods of time. Our results demonstrate that intrinsic cell properties
support the presynaptic retinal computation and are, once established, independent of them.

## Overview

Werginz, Kiraly, and Zeck combine targeted whole-cell patch-clamp recordings with multi-compartment
biophysical modeling to dissect how three classes of mouse alpha retinal ganglion cells (alpha-ON
sustained, alpha-OFF sustained, and alpha-OFF transient) convert injected current into spike trains.
The authors deliberately remove synaptic input by bath-blocking glutamatergic and GABAergic
transmission, so the measured firing differences reflect intrinsic spike-generator properties rather
than upstream circuitry. They classify cells using soma diameter, dendritic stratification depth in
the inner plexiform layer, and a multi-feature spike-shape clustering procedure (adjusted Rand index
0.8).

The headline finding is that the spike generator itself is tuned to the cell light-response
phenotype: sustained alpha-RGCs fire long, lower-frequency trains with broad action potentials,
while alpha-OFF transient cells fire short, fast bursts with the shortest action potentials and the
steepest hyperpolarization rates. These differences are quantitatively large (factor of ~1.5 in
spike duration, factor of ~1.8 in sustained-to-peak ratio) and survive in the rd10
photoreceptor-degeneration model up to p227, demonstrating that the spike-generator phenotype is
established during development and then becomes circuit-independent.

The study includes a multi-compartment NEURON model of an alpha-RGC with five distinct compartment
tiers (dendrites, soma, soma-AIS, AIS, axon) whose channel densities are reported in Table 1. The
model is used to demonstrate that the experimentally observed differences in firing properties can
be reproduced by modulating the AIS sodium- and potassium-channel densities and the soma input
resistance, identifying these as the principal biophysical degrees of freedom that distinguish the
three alpha-RGC types. Importantly, the channel densities in Table 1 are mouse alpha-RGC values,
calibrated against the same patch-clamp recordings reported in the paper.

## Architecture, Models and Methods

**Patch-clamp protocol.** Whole-cell current-clamp recordings were obtained from flat-mount mouse
retinae (wild-type C57BL/6, 18 retinae, p48-p143, mean p97, 10 females + 8 males; rd10 degenerate
strain, 8 retinae, p193-p227, mean p206, 4 females + 4 males). Synaptic transmission was blocked
pharmacologically (DNQX, AP5, gabazine, strychnine, TPMPA). Alpha-RGCs were targeted by soma size
(>20 um) and confirmed post hoc by dendritic stratification. Recordings: alpha-ONs n=31, alpha-OFFs
n=19, alpha-OFFt n=23 (wild-type); rd10 alpha-ONs+alpha-OFFs n=34, alpha-OFFt n=14; non-alpha-RGC
controls n=51; clustering analysis spanned 119 cells total.

**Spike-feature analysis.** Action potentials were extracted from rheobase + 200 pA traces. Features
quantified per cell: spike duration (full-width at half-maximum), peak depolarization rate, peak
hyperpolarization rate, hyperpolarization-to-depolarization rate ratio, sustained-to-peak firing
ratio (mean over last 200 ms / peak over first 100 ms), peak firing rate at depolarization block,
break amplitude (current at which firing collapses), break voltage, and input resistance from
sub-threshold steps. Cell-type clustering used UMAP + Gaussian mixture model on the multi-feature
space.

**Compartmental model.** A reconstructed alpha-RGC morphology was implemented in NEURON. The cell is
partitioned into five compartment tiers - dendrites, soma, soma-AIS (a transition segment between
soma and axon initial segment), AIS, and axon - each with its own ion-channel density set (reported
in Table 1). Channels modeled: Nav (HH-style), Kv (delayed rectifier), Cav (L-type + T-type mix),
K(Ca) (calcium-dependent K), HCN (Ih), and a passive leak. Channel densities (mS/cm^2) per tier:

| Channel | Dendrites | Soma | Soma-AIS | AIS | Axon |
| --- | --- | --- | --- | --- | --- |
| **gNa** | 75 | 75 | 75 | **1300** | 65 |
| **gK** | 48 | 48 | 48 | **800** | 40 |
| **gCa** | 1 | 1 | 1 | 1 | 1 |
| **gK,Ca** | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 |
| **gH** | 0.56 | 0.43 | 0.43 | 0.43 | 0.43 |
| **gL** | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 |

The AIS-to-soma ratios are **17.3x** for Nav and **16.7x** for Kv; dendritic Ih is **1.30x** the
somatic value; K(Ca) and Cav are uniform across compartments at 0.1 and 1 mS/cm^2 respectively.
Sustained vs transient phenotypes are reproduced in the model by scaling AIS Nav and the soma input
resistance (the latter via the leak conductance).

## Results

* Sustained-to-peak firing ratios under sustained current injection differ by a factor of ~1.8:
  alpha-ONs **0.57 +/- 0.06**, alpha-OFFs **0.49 +/- 0.06**, alpha-OFFt **0.32 +/- 0.07**.
* Peak firing rate at depolarization block: alpha-ONs **278 +/- 37 Hz**, alpha-OFFs **270 +/- 53
  Hz**, alpha-OFFt **346 +/- 44 Hz** - the transient cell reaches the highest peak rate.
* Action potential duration (FWHM): alpha-ONs **0.31 +/- 0.03 ms**, alpha-OFFs **0.28 +/- 0.03 ms**,
  alpha-OFFt **0.21 +/- 0.02 ms** - alpha-OFFt spikes are ~33% shorter than alpha-ONs.
* Hyperpolarization/depolarization rate ratio: alpha-ONs **0.49 +/- 0.04**, alpha-OFFs **0.48 +/-
  0.05**, alpha-OFFt **0.59 +/- 0.03** - transient cells repolarize faster relative to
  depolarization.
* Depolarization-block break current: alpha-ONs **792 +/- 132 pA**, alpha-OFFs **369 +/- 63 pA**,
  alpha-OFFt **560 +/- 154 pA**; break voltage: alpha-ONs **-37.9 +/- 3.8 mV**, alpha-OFFs **-43.2
  +/- 3.0 mV**, alpha-OFFt **-45.3 +/- 3.8 mV**.
* Input resistance: alpha-ONs **80 +/- 18 MOhm**, alpha-OFFs **108 +/- 30 MOhm**, alpha-OFFt **60
  +/- 16 MOhm** - the transient cell has the lowest Rin, consistent with a larger somatic leak.
* In rd10 retina (p200+), sustained-vs-transient distinction persists: rd10 sustained S/P **0.55 +/-
  0.13**, rd10 transient **0.30 +/- 0.11**; rd10 sustained spike duration **0.29 +/- 0.05 ms** vs
  transient **0.22 +/- 0.05 ms**.
* Compartmental model with Table 1 densities reproduces all three alpha-RGC firing phenotypes when
  AIS Nav and somatic leak are scaled within +/- 20% of nominal values.

## Innovations

### Mouse-Specific Tier-Stratified Channel Densities for alpha-RGCs

This paper is one of the very few sources reporting per-compartment channel densities (Nav, Kv, Cav,
K(Ca), Ih, leak) calibrated against mouse - not rat or cat - alpha-RGC patch-clamp recordings. The
five-tier partition (dendrites, soma, soma-AIS, AIS, axon) and the explicit AIS hot-spot densities
(1300 mS/cm^2 Nav, 800 mS/cm^2 Kv) provide a directly usable parameter set for biophysical models
that target mouse RGC physiology.

### Intrinsic Discrimination of Sustained vs Transient Phenotypes

The work demonstrates that alpha-ON sustained, alpha-OFF sustained, and alpha-OFF transient mouse
alpha-RGCs can be distinguished by intrinsic spike-generator properties alone, with no synaptic
input. This is methodologically important: it isolates the cell-autonomous biophysical features (AIS
density, somatic leak, K(Ca) recovery) from upstream circuit influences and shows that a small set
of compartment-level conductance changes is sufficient to produce the three phenotypes.

### Long-Term Stability of Intrinsic Properties in rd10 Degeneration

The persistence of alpha-RGC firing-type identity into late-stage rd10 (p227) photoreceptor
degeneration shows that the spike generator is established once and then operates independently of
presynaptic circuitry. This has both basic-science implications (developmental tuning of RGC
intrinsic properties) and translational relevance for retinal-prosthesis design, since prosthesis
stimulation must drive intrinsically-different cell types toward the same target output.

## Datasets

* **Wild-type whole-cell patch recordings**: 18 mouse retinae, 73 alpha-RGCs (alpha-ONs n=31,
  alpha-OFFs n=19, alpha-OFFt n=23) plus 51 non-alpha-RGC controls. Mice age range p48-p143 (mean
  p97).
* **rd10 degenerate whole-cell patch recordings**: 8 mouse retinae, 48 alpha-RGCs (rd10
  alpha-ONs+alpha-OFFs n=34, alpha-OFFt n=14). Mice age range p193-p227 (mean p206).
* **Total clustered cells**: 119 across all conditions.
* All recordings are the authors own; they are not publicly released as a dataset, but the per-cell
  summary statistics in the paper tables and Table 1 channel densities are sufficient to
  parameterize a downstream model. No external datasets were reused.

## Main Ideas

* **Per-compartment channel-density table is the load-bearing finding for t0078.** Table 1 provides
  mouse-specific Nav, Kv, Cav, K(Ca), Ih, and leak densities partitioned into five tiers (dendrites,
  soma, soma-AIS, AIS, axon), replacing the Fohlmeister 2010 rat/cat priors that research_papers.md
  currently leans on. The AIS-to-soma ratios - **17.3x** for Nav, **16.7x** for Kv - and the
  dendritic Ih ratio of **1.30x** the somatic value should be encoded as the central tendency of the
  t0078 49-d parameter-space tier bounds, with sigma taken from the inter-cell-type spread.
* **Sustained vs transient phenotypes are reproducible by modulating AIS Nav and somatic leak.** The
  model demonstrates that scaling AIS Nav by +/- 20% and somatic leak/Rin by a similar amount is
  sufficient to interpolate between the three alpha-RGC firing types. This bounds the meaningful
  range of the AIS Nav and soma-leak parameters in the MOBO search and warns against tier scalings
  that depart by more than ~2x from the Werginz nominal values.
* **K(Ca) and Cav are uniform at 0.1 and 1 mS/cm^2 across compartments** in the Werginz model. This
  contradicts some priors that placed K(Ca) selectively at the soma; for t0078 it suggests the K(Ca)
  and Cav tier bounds can be much narrower (uniform prior with small sigma) than the Nav/Kv bounds,
  freeing optimization budget for the high-leverage parameters.
* **Per-cell-type calibration matters.** Because the same Table 1 densities reproduce all three
  alpha-RGC types after small AIS- and leak-level adjustments, fitting a single morphology to a
  population-mean firing target (rather than to an individual cell-type target) is the right initial
  regime; cell-type-specific fits should follow only after the population fit converges.
* **rd10 stability provides a test for over-fitting.** A model fitted on wild-type targets that
  generalizes to rd10 firing statistics (within the reported +/- 0.1 sustained-to-peak ratio band)
  is likely capturing genuine intrinsic biophysics rather than memorizing synaptic-input-driven
  features, since the rd10 retina has degenerated presynaptic circuitry.

## Summary

Werginz, Kiraly, and Zeck (2024) ask whether the spike generator of mouse alpha-RGCs is itself tuned
to each cell type downstream computational role, or whether sustained-vs-transient firing phenotypes
arise purely from upstream synaptic circuitry. They isolate the spike generator pharmacologically,
record from 73 wild-type and 48 rd10-degenerate alpha-RGCs across three subtypes (alpha-ON
sustained, alpha-OFF sustained, alpha-OFF transient), and quantify nine spike-shape and
firing-pattern features per cell.

The methodology combines whole-cell current-clamp recordings (with all major synaptic transmission
blocked) and a five-tier compartmental NEURON model. The model partitions an alpha-RGC into
dendrites, soma, soma-AIS, AIS, and axon, each with its own densities of Nav, Kv, Cav, K(Ca), Ih,
and leak - all calibrated to mouse rather than the historical rat/cat parameter sets. AIS densities
are particularly high (1300 mS/cm^2 Nav, 800 mS/cm^2 Kv), establishing the AIS as the dominant
spike-generation locus. UMAP + GMM clustering of the spike-feature vectors achieves an adjusted Rand
index of 0.8 against the morphological cell-type labels.

The paper finds that the three alpha-RGC types differ substantially in intrinsic spike output:
alpha-OFF transient cells have the shortest spikes (**0.21 ms** vs **0.31 ms** for alpha-ON
sustained), the lowest sustained-to-peak ratio (**0.32** vs **0.57**), and the highest peak firing
rates (**346 Hz** vs **278 Hz**). The compartmental model reproduces these differences via small
modulations of AIS Nav density and somatic leak conductance. Crucially, the same firing-type
distinctions persist in rd10 photoreceptor-degenerated retina up to p227, demonstrating that
alpha-RGC intrinsic properties are circuit-independent once established.

For the t0078 multi-tier MOBO project, this paper is the most directly load-bearing source we have
seen for the 49-dimensional parameter-space tier bounds. The Werginz Table 1 densities provide
mouse-specific central tendencies for all six channels across all five compartments; the soma-vs-AIS
ratios (17.3x Nav, 16.7x Kv) and the dendritic Ih (1.30x somatic) define the tier stratification
structure that t0078 was designed around. The within-cell-type variance also provides empirical
sigma values for the prior, replacing the previously assumed values lifted from Fohlmeister 2010.
The model demonstration that +/- 20% modulation of AIS Nav and somatic leak suffices to reproduce
sustained-vs-transient differences provides a tight prior for the most important search dimensions
and justifies narrower bounds on K(Ca) and Cav, freeing search budget for the high-leverage
parameters.
