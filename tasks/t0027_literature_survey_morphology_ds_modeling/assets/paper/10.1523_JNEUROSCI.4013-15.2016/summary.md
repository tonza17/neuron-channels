---
spec_version: "3"
paper_id: "10.1523_JNEUROSCI.4013-15.2016"
citation_key: "PolegPolsky2016"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# Retinal Circuitry Balances Contrast Tuning of Excitation and Inhibition to Enable Reliable Computation of Direction Selectivity

## Metadata

* **File**: `files/poleg-polsky_2016_ei-contrast-tuning-ds.pdf`
* **Published**: 2016-05-25
* **Authors**: Alon Poleg-Polsky 🇺🇸, Jeffrey S. Diamond 🇺🇸
* **Venue**: *The Journal of Neuroscience*, vol. 36, issue 21, pp. 5861-5876
* **DOI**: `10.1523/JNEUROSCI.4013-15.2016`
* **PMCID**: PMC4879202

## Abstract

Feedforward (FF) inhibition is a common motif in many neural networks. Typically, excitatory inputs
drive both principal neurons and interneurons; the interneurons then inhibit the principal neurons,
thereby regulating the strength and timing of the FF signal. The interneurons introduce a likely
nonlinear processing step that could distort the excitation/inhibition (E/I) ratio in the principal
neuron, potentially degrading the reliability of computation in the circuit. In the retina, FF
inhibition is an essential feature of the circuitry underlying direction selectivity (DS):
glutamatergic bipolar cells (BCs) provide excitatory input to direction-selective ganglion cells
(DSGCs) and GABAergic starburst amacrine cells (SACs), and the SACs then provide FF inhibition onto
DSGCs. Robust DS computation requires a consistent synaptic E/I ratio in the DSGC in various visual
conditions. Here, we show in mouse retina that the E/I ratio is maintained in DSGCs over a wide
stimulus contrast range due to compensatory mechanisms in the diverse population of presynaptic BCs.
BC inputs to SACs exhibit higher contrast sensitivity, so that the subsequent nonlinear
transformation in SACs reduces the contrast sensitivity of FF inhibition to match the sensitivity of
direct excitatory inputs onto DSGCs. Measurements of light-evoked responses from individual BC
synaptic terminals suggest that the distinct sensitivity of BC inputs reflects different contrast
sensitivity between BC subtypes. Numerical simulations suggest that this network arrangement is
crucial for reliable DS computation.

## Overview

This paper dissects why the retinal direction-selective circuit maintains a stable excitation /
inhibition (E/I) ratio at the direction-selective ganglion cell (DSGC) across a wide range of visual
stimulus contrasts, despite the feedforward (FF) architecture that inserts a nonlinear interneuron
(the starburst amacrine cell, SAC) between bipolar cells (BCs) and the DSGC. Using patch-clamp
recordings in intact mouse retina, two-photon calcium imaging, and iGluSnFR-based glutamate sensing,
Poleg-Polsky and Diamond show that BC input to SACs activates at substantially lower contrasts than
BC input to DSGCs, exactly compensating for a sigmoidal dendritic Ca-release threshold in SACs.
Pharmacological dissection further shows that cholinergic and glutamatergic excitation to DSGCs
carry the same contrast sensitivity, so the balance arises presynaptically through bipolar-cell
subtype diversity rather than through postsynaptic receptor differences.

Relevance to the morphology-on-DS survey (**borderline inclusion**): the primary contribution is a
circuit-level account of contrast tuning and E/I balance, and morphology is held fixed across
simulations. The DSGC compartmental model, however, uses an explicit multi-compartment dendritic
tree (121 ON-layer compartments) with BC and SAC synapses distributed along it, together with active
voltage-gated sodium and potassium conductances. The model is used specifically to test how the
distribution of E and I across the dendritic tree affects the reliability of DS at threshold. I
therefore include the paper to document the mechanism by which E/I-on-morphology — not morphology
itself — shapes DS computation, complementing the later Poleg-Polsky 2026 DSGC paper in our corpus.

The authors conclude that BC subtype heterogeneity is the compensatory element that linearizes the
overall FF pathway at the level of the DSGC and that this BC-tuning diversity is a general strategy
by which retinal circuits preserve E/I balance in the face of nonlinear interneurons.

## Architecture, Models and Methods

**Experimental preparation.** Flat-mount mouse retina from eGFP-DRD4/Chat-Cre/TdTomato mice
(postnatal days 14-56, either sex) at near-physiological 35 °C in oxygenated Ames medium. DRD4+
ON-OFF DSGCs and labeled SACs were targeted under two-photon visualization. Recordings combined
cell-attached spike counts, whole-cell voltage-clamp (`E_rev` at -65 mV for EPSCs, 0 mV for IPSCs),
whole-cell current-clamp (TTX 1 µM or intracellular QX-314 5 mM to block Na+ channels), two-photon
Ca2+ imaging with OGB-1 or Fluo-4 (0.2 mM), and Cre-dependent or Cre-independent AAV-delivered
iGluSnFR for direct readout of presynaptic glutamate release. Cholinergic (hexamethonium 100 µM,
atropine 5 µM) and NMDAR blockers (AP5 50 µM or MK-801 10 µM) were used to dissect EPSC components.

**Visual stimulation.** 405 nm LED through a 240x240 LCD focused at the photoreceptor plane,
background 30 000 R* rod⁻¹ s⁻¹. Stimuli were 500x2000 µm rectangles moving at 1 mm/s in eight
directions, delivered at 10-15 s intervals, at a wide range of Michelson contrasts on a fixed
background.

**Compartmental DSGC model.** A numerical DSGC with a dendritic tree discretized into **121 ON-layer
compartments**, each innervated by a colocalized BC-like excitatory and SAC-like inhibitory point
source. Three synapse classes: (1) ohmic AMPA/nAChR (instantaneous rise, 2 ms decay, 0.5 nS unitary
conductance, `E_rev` = 0 mV); (2) NMDAR with 2 ms rise, 60 ms decay, 0.5 nS peak conductance,
voltage-dependent `G_NMDA = 1 / (1 + 0.3 * exp(-0.07 * V))` following Jahr and Stevens (1990); (3)
GABAergic input with instantaneous rise, 30 ms decay, 0.5 nS, `E_rev` = -60 mV. Stochastic
Hodgkin-Huxley Na+ and K+ channels generate noisy spike output (Linaro et al. 2011). Each
presynaptic terminal has a 10-vesicle readily-releasable pool with release probability set by a
contrast-dependent depolarization (rise 50 ms, decay 200 ms) and replenishment at 500 ms⁻¹.
Null-direction was simulated first; preferred-direction responses were produced by reducing GABA
release threefold. Ten 0.5 s trials per condition at dt = 0.1 ms. Three contrast-tuning scenarios
were compared: (i) matched E and I, (ii) more sensitive E, (iii) more sensitive I.

**Statistics.** Wilcoxon signed-rank, paired t-test, one-way and two-way ANOVA with Bonferroni
correction, sample sizes 5-43 cells per condition.

## Results

* DRD4+ DSGCs maintain reliable direction selectivity across a broad contrast range in both
  subthreshold PSPs and spikes; spike contrast threshold **68 ± 24 % (n = 43)** is higher than PSP
  threshold **45 ± 25 % (n = 13)** (**p = 0.03**, Wilcoxon), because sub-threshold PSPs fail to
  trigger spikes.
* EPSC and IPSC contrast thresholds in DSGCs are statistically indistinguishable (**38 ± 14 %** vs.
  **39 ± 30 %**, n = 23, p = 0.3), and the E/I amplitude ratio is effectively contrast-independent
  (Pearson **r = 0.94** across the tested contrast range).
* SAC EPSC transient component is reliably detected at **15.2 ± 8.5 %** contrast with half-maximal
  **C½ = 32.5 ± 13.5 %**, while the sustained component has **C½ = 50 ± 27 %** (**p = 0.02**, paired
  t-test, n = 13) — both markedly more sensitive than DSGC EPSCs (**p < 0.01**, one-way ANOVA).
* SAC dendritic Ca2+ signals are undetectable below **38 ± 32 %** contrast and have **C½ = 66 ± 35
  %**, vs **26 ± 17 %** for somatic PSPs (**p = 0.0005**, paired t-test, n = 11), establishing a
  nonlinear SAC input-output transformation that matches SAC outputs to DSGC EPSC contrast tuning.
* iGluSnFR measured directly on post-synaptic SAC vs. DSGC dendrites shows BC glutamate release is
  detected at **16.2 ± 8 %** contrast onto SACs but only at **65.5 ± 17 %** onto DSGCs (**p <
  0.00001**, t-test, n = 8 SACs, 9 DSGCs), localizing the contrast-sensitivity difference to
  presynaptic BC subtypes.
* Within single BC axon terminals, contrast sensitivity is highly uniform (peak-to-peak **33 ± 14
  %**, SD **12 ± 5 %**, n = 13), whereas across 30 ON BCs the C½ spans the full gap between SAC- and
  DSGC-like tuning (**p < 0.001**, Mann-Whitney).
* High-sensitivity BCs stratify higher and more narrowly in the IPL than low-sensitivity BCs (**p <
  0.05**, t-test with Bonferroni), linking morphology/subtype identity to contrast tuning.
* Compartmental DSGC simulations (121 dendritic compartments, stochastic channels): the balanced E/I
  scenario produces the highest suprathreshold DSI across the tested contrast range; making
  inhibition *less* contrast-sensitive degrades DSI over a wide range, and making inhibition *more*
  contrast-sensitive suppresses spiking at low contrasts, lowering suprathreshold DSI despite
  improved subthreshold DS.
* Cholinergic block (hexamethonium + atropine), NMDAR block (AP5), and AMPA isolation all leave the
  DSGC EPSC *contrast-sensitivity curve* unchanged (**p > 0.2**, t-test for thresholds; **p > 0.5**,
  two-way ANOVA on normalized curves), so the balance is not set by postsynaptic receptor
  composition.

## Innovations

### Quantitative Demonstration of Stable E/I Despite a Nonlinear FF Interneuron

This is the first study to directly measure all four legs of the retinal DS feedforward circuit
(BC→SAC excitation, BC→DSGC excitation, SAC dendritic Ca2+, SAC→DSGC inhibition) in the same
preparation and show, with matched moving-bar stimuli, that a steeply nonlinear SAC dendritic output
transform is precisely compensated by higher-sensitivity BC input to SACs.

### Compartmental Modeling of E/I Contrast Matching

The authors introduce a stochastic 121-compartment DSGC model with distributed BC and SAC synapses
and physiologically parameterized AMPA/NMDA/GABA conductances, and use it to show that E/I balance
across the dendritic tree — rather than in aggregate — is what guarantees robust DS at threshold.
This connects circuit-level contrast tuning to a concrete dendritic integration mechanism and
foreshadows later DSGC compartmental studies.

### Bipolar-Cell Subtype Heterogeneity as a Circuit Linearizer

By mapping contrast sensitivity of 30 ON BCs against their IPL stratification, the paper introduces
the idea that the retinal circuit exploits BC subtype heterogeneity to linearize the
feedforward-inhibition pathway, assigning a concrete computational role to BC diversity.

### Combined iGluSnFR + Patch + Bouton Imaging Protocol

The methodology pairs SAC- and DSGC-specific iGluSnFR expression (AAV-FLEX and non-Cre) with
whole-cell patch and OGB-1/Fluo-4 imaging from mechanically labeled single BC terminals, showing
that within-terminal contrast sensitivity is homogeneous but between-BC sensitivity is broadly
distributed.

## Datasets

This is an experimental paper; no publicly released datasets were produced. Primary data are
electrophysiological recordings and two-photon imaging traces from mouse retina:

* 43 DRD4+ ON-OFF DSGCs (cell-attached + whole-cell PSP recordings).
* 23 DSGCs (voltage-clamp EPSC/IPSC across contrast range).
* 13 SACs (EPSC contrast tuning), 11-12 SACs (simultaneous PSP + OGB-1 Ca2+ imaging), additional
  cohorts of 5-7 SACs for Fluo-4 and sharp-electrode controls.
* 11 SACs and 8 DSGCs with AAV-iGluSnFR and 9 DSGCs with Cre-independent iGluSnFR.
* 30 ON BCs imaged for axonal Ca2+ responses; 13 BCs for within-terminal uniformity.
* Numerical simulations: 10 trials x 3 E/I scenarios x multiple contrast levels on a 121-compartment
  DSGC model.

Model code and sample traces are not deposited in a public repository (per the paper declaration at
publication time). Reagents used included commercial AAVs (Penn Vector Core) and mouse lines
(eGFP-DRD4, Chat-Cre, TdTomato).

## Main Ideas

* E/I balance in DSGCs is preserved across contrast not by postsynaptic receptor matching but by
  presynaptic BC-subtype heterogeneity — BCs driving SACs are intrinsically more contrast-sensitive
  than BCs driving DSGCs.
* The SAC dendrite is a sharply sigmoidal voltage-to-release element (Ca channels need strong
  depolarization); this nonlinearity is pre-compensated upstream by the BC pool, not downstream by
  the DSGC.
* When modeling DS in a compartmental DSGC, E/I conductance distributions across the dendritic tree
  matter: mismatched contrast tuning of E vs I degrades reliable DS either at low contrasts (weak
  inhibition) or by suppressing spiking (excess low-contrast inhibition).
* For a project that models DS in morphologically realistic DSGCs, use physiologically tuned
  AMPA/NMDA/GABA synapse parameters (AMPA 0.5 nS, 2 ms; NMDA 0.5 nS, 60 ms, Jahr-Stevens Mg block;
  GABA 0.5 nS, 30 ms, `E_rev` = -60 mV) and place BC/SAC inputs on a dense ON-dendrite
  compartmentalization (~10^2 compartments) with stochastic channel noise.
* Any morphology-on-DS study should treat BC-subtype contrast sensitivity as a boundary condition on
  presynaptic input statistics, not as a free parameter — DS results will otherwise be biased by
  whatever E/I balance assumption is implicit in the BC model.

## Summary

Poleg-Polsky and Diamond ask how the retinal direction-selective circuit, which is organized as a
feedforward inhibitory microcircuit (bipolar cell → starburst amacrine cell → direction-selective
ganglion cell), keeps its excitation / inhibition ratio stable across a wide contrast range even
though the SAC interposes a highly nonlinear dendritic release step. Using whole-cell recordings,
pharmacology, two-photon Ca2+ imaging, and iGluSnFR in mouse retina, they show that the DSGC E/I
ratio is indeed contrast-independent (r = 0.94) and that this is not because of postsynaptic
receptor differences between cholinergic, NMDAR and AMPAR components, which all share the same
contrast sensitivity.

The compensating mechanism lives in the bipolar-cell layer: BCs that drive SACs are far more
contrast-sensitive (detection threshold ~16 % contrast, half-activation ~32 %) than BCs that drive
DSGCs (threshold ~65 %). Direct imaging of SAC dendritic Ca2+ shows that the SAC I/O transform is
steeply sigmoidal (threshold ~38 %, half-activation ~66 %), so the elevated presynaptic sensitivity
of SAC-targeting BCs exactly offsets the SAC nonlinearity, leaving the feedforward GABAergic output
at the DSGC contrast-matched to the direct BC → DSGC excitation. Single-bouton recordings show this
sensitivity difference is between BC subtypes, not within them, and correlates with distinct IPL
stratification.

A stochastic compartmental DSGC model (121 ON-layer compartments; AMPA, NMDA and GABA conductances
with realistic kinetics and Jahr-Stevens NMDA voltage dependence; Hodgkin-Huxley spike generator) is
used to show that matched E/I contrast tuning maximizes suprathreshold DSI. Shifting E or I along
the contrast axis either leaks non-directional null responses through the circuit or quenches spikes
altogether, confirming that the presynaptic BC-heterogeneity mechanism is functionally necessary,
not merely present.

For this project the paper is a **borderline** but important inclusion. The morphology of the DSGC
is held fixed and the primary contribution is circuit-level, so it is not a morphology-on-DS
modeling paper in the strict sense. However, the compartmental DSGC model with spatially distributed
E and I inputs, and the explicit demonstration that the *distribution* of E/I contrast tuning across
dendritic compartments gates reliable DS computation, make this a key reference for how
E/I-on-morphology shapes DS. It should be cited alongside PolegPolsky2026 when arguing that DSGC
dendritic biophysics and synaptic spatial statistics — not just SAC wiring — determine
direction-selective reliability, and its synapse parameterization can be reused as a validated
starting point for our own DSGC simulations.
