---
spec_version: "3"
paper_id: "10.1523_JNEUROSCI.23-12-04899.2003"
citation_key: "Khaliq2003"
summarized_by_task: "t0078_bedb_mobo_v2_ais_tiered_ahp"
date_summarized: "2026-05-03"
---
# The Contribution of Resurgent Sodium Current to High-Frequency Firing in Purkinje Neurons: An Experimental and Modeling Study

## Metadata

* **File**: `files/khaliq_2003_resurgent-na-purkinje.pdf`
* **Published**: 2003-06-15 (J. Neurosci. 23(12):4899-4912)
* **Authors**: Zayd M. Khaliq 🇺🇸, Nathan W. Gouwens 🇺🇸, Indira M. Raman 🇺🇸
* **Venue**: The Journal of Neuroscience (refereed journal article)
* **DOI**: `10.1523/JNEUROSCI.23-12-04899.2003`

## Abstract

Purkinje neurons generate high-frequency action potentials and express voltage-gated,
tetrodotoxin-sensitive sodium channels with distinctive kinetics. Their sodium currents activate and
inactivate during depolarization, as well as reactivate during repolarization from positive
potentials, producing a "resurgent" current. This reopening of channels not only generates inward
current after each action potential, but also permits rapid recovery from inactivation, leading to
the hypothesis that resurgent current may facilitate high-frequency firing.

Mutant med mice are ataxic and lack expression of the Scn8a gene, which encodes the NaV1.6 protein.
In med Purkinje cells, transient sodium current inactivates more rapidly than in wild-type cells,
and resurgent current is nearly abolished. To investigate how NaV1.6-specific kinetics influence
firing patterns, we recorded action potentials of Purkinje neurons isolated from wild-type and med
mice. We also recorded non-sodium currents from Purkinje cells of both genotypes to test whether the
Scn8a mutation induced changes in other ion channels. Last, we modeled action potential firing by
simulating eight currents directly recorded from Purkinje cells in both wild-type and med mice.

Regular, high-frequency firing was slowed in med Purkinje neurons. In addition to disrupted sodium
currents, med neurons had small but significant changes in potassium and leak currents. Simulations
indicated that these modified non-sodium currents could not account for the reduced excitability of
med cells but instead slightly facilitated spiking. The loss of NaV1.6-specific kinetics, however,
slowed simulated spontaneous activity. Together, the data suggest that across a range of conditions,
sodium currents with a resurgent component promote and accelerate firing.

## Overview

This paper combines whole-cell patch-clamp electrophysiology of acutely dissociated mouse cerebellar
Purkinje neurons with a NEURON-based single-compartment biophysical model to dissect the
contribution of NaV1.6-mediated resurgent sodium current to high-frequency firing. The authors
exploit the Scn8a-deficient med mouse line, in which NaV1.6 is absent and resurgent current is
reduced by approximately 90 percent, as a natural knockout of the resurgent component. They record
action potentials from wild-type and med Purkinje somata, characterise five non-sodium currents
(three voltage-gated K currents, BK calcium-activated K, Ih, and a passive leak) by pharmacological
subtraction, and use these recordings to parameterise an eight-current Hodgkin-Huxley plus
state-model NEURON simulation.

The headline experimental finding is that med Purkinje cells fire spontaneously at roughly one
quarter of the wild-type rate, are less likely to be spontaneously active at all, and cannot be
driven to wild-type firing frequencies by depolarising current injection. Beyond the sodium-channel
phenotype, med cells show small but reproducible changes in passive leak conductance (raising input
resistance) and in the half-activation voltage of the highly TEA-sensitive Kfast current. The
modeling component then dissects which of these changes matter: it shows that the non-sodium
modifications, taken alone, would actually facilitate firing, so the slowed firing in med cells must
be attributed predominantly to the loss of resurgent kinetics in the sodium channel itself.

The significance for compartmental-modeling work is twofold. First, this paper is the canonical
source of the kinetic schemes and Hodgkin-Huxley parameter values for the BK ("bkpkj"), Kfast, Kmid,
Kslow, P-type Ca, Ih, and leak currents of mouse Purkinje somata - parameters that have been re-used
widely in NEURON model libraries, including the bkpkj.mod and resurgent-Na NaR implementations
vendored in the present project Bed B substrate. Second, it is the source paper for the
Raman-Bean-style state-machine model of NaV1.6 with explicit open-channel block, the formalism used
by every downstream NaR mod-file derivative. The paper therefore anchors the kinetic foundations of
the t0078 NaR tier-stratified MOD that runs on the AIS-augmented Bed B substrate.

## Architecture, Models and Methods

**Preparation and recording.** Cerebellar Purkinje somata were acutely dissociated from postnatal
day 14-20 wild-type and homozygous Scn8a-med mice (genotyped by PCR). Cells were enzymatically
liberated with protease XXIII (3 mg/mL, 7 min, 31 deg C) and patched in Tyrode solution at room
temperature using borosilicate pipettes (3-5 MOhm for current clamp, 1-3 MOhm for voltage clamp).
Action potentials were recorded with a Dagan BVC amplifier in bridge mode; voltage-clamped currents
with an Axopatch 200B and series-resistance compensation of 90 percent. Three pipette solutions
(K-methanesulfonate, K-gluconate low EGTA at 0.9 mM, K-gluconate high EGTA at 9 mM) were tested and
gave indistinguishable firing; data were pooled.

**Pharmacological isolation.** Voltage-gated K currents were measured in 2 mM Co (replacing Ca) plus
900 nM TTX, with TEA dose-response curves at 30 microM to 5 mM. Currents were separated into "highly
TEA-sensitive" (control minus 100 microM TEA), "moderately TEA-sensitive" (300 microM minus 1 mM
TEA), and "1 mM TEA-resistant" components. Ih was evoked by 1 sec hyperpolarisations from -50 mV.
Iberiotoxin-sensitive K(Ca) (BK) currents used 100-300 nM iberiotoxin in normal Tyrode plus 1 mg/mL
cytochrome c. Leak was measured by hyperpolarising steps from -60 mV to -70 / -90 mV.

**Computational model.** A single-compartment cylindrical NEURON model (length 20 microm, radius 10
microm, 19 pF capacitance) integrated eight currents: a state-model NaV1.6 sodium current based on
Raman and Bean (2001) (closed-inactivated-open-blocked scheme with rate constants alpha, beta,
gamma, delta, epsilon, zeta, Con, Coff, Oon, Ooff and amplitude-scaling factors a, b),
Hodgkin-Huxley K_fast (m^3 h, Gmax 40 pS/cm^2, V1/2 = -24 mV / k = 15.4 mV for m), K_mid (m^4, Gmax
20), K_slow (m^4, Gmax 40, V1/2 = -16.5 mV), P-type Ca (m, GHK current eq.), BK (m^3 z^2 h, Gmax 70,
calcium-dependent z gate with zcoef 0.001 mM), Ih (single m, Gmax 1, V1/2 = -90.1 mV), and a linear
leak (Gmax 0.5, Eleak = -60 mV). Calcium was modeled in a 100 nm submembrane shell with extrusion
rate beta = 1/msec and clamp at 100 nM minimum. ENa = 60 mV, EK = -88 mV.

**Med-channel modeling.** To replicate med-like sodium kinetics, the transition rate epsilon into
the blocked state was reduced to 1e-12/msec (eliminating block) and Oon was increased from 0.75/msec
to 2.3/msec (accelerating fast inactivation). Combined, these changes reproduced the faster
transient decay, negatively shifted steady-state inactivation, and 90 percent reduction in resurgent
current observed experimentally. Statistics: mean +/- SE; t-tests; n typically 4-18 cells per
condition.

## Results

* Wild-type Purkinje somata fired spontaneously at **35 +/- 4 Hz**; med somata fired at **9 +/- 2
  Hz** when active (p < 0.0001), with only **10 of 18 med cells** spontaneously active vs **15 of 18
  wild-type**.
* At a 50 pA current injection, wild-type fired at **65 +/- 7 spikes/sec** (n=18) versus med at **13
  +/- 5 spikes/sec** (n=18; p < 0.0001).
* Even among the most reliably firing cells, maximal sustained rates were **107 +/- 6 spikes/sec at
  225 +/- 36 pA** (wild-type, n=15) versus **65 +/- 10 spikes/sec at 185 +/- 60 pA** (med, n=4; p =
  0.02).
* Peak sodium current was **2.8 +/- 0.3 nA** wild-type vs **2.1 +/- 0.3 nA** med (p < 0.1; ~25
  percent reduction); cell capacitances were indistinguishable (17.6 +/- 3.5 pF vs 16.0 +/- 1.7 pF;
  p = 0.12), so the change was channel density / kinetics, not cell size.
* Input resistance was **624 +/- 54 MOhm** wild-type vs **763 +/- 38 MOhm** med (p = 0.04),
  indicating reduced leak conductance in med cells; Ih was unchanged (121 +/- 17 pA wild-type vs 99
  +/- 14 pA med at -120 mV; p = 0.34).
* The highly TEA-sensitive Kfast current showed an **8 mV positive shift in V1/2** in med cells;
  Kmid, Kslow, and BK V1/2 and Gmax were statistically indistinguishable between genotypes (Table 2
  of the paper).
* TEA dose-response was voltage-dependent: IC50 = **48 microM at +20 mV** vs **219 microM at -20
  mV** in wild-type (n=16), consistent with multiple K-channel populations.
* The wild-type model spontaneously fired at **27 spikes/sec**, matching the experimental mean of 29
  Hz; replacing wild-type Na kinetics with med-like kinetics slowed simulated firing by **19-31
  percent** across sodium-current amplitudes, with the "no-block" variant reducing rates by **17-38
  percent** and "fast-inactivation alone" by **7-17 percent**.
* In the model, modifying non-sodium currents toward the med phenotype (positive Kfast V1/2 shift,
  30 percent leak reduction) **increased** rather than decreased simulated firing, showing the
  non-sodium changes are compensatory, not causal.

## Innovations

### State-Machine Model of NaV1.6 with Open-Channel Block

The paper Equation-1 kinetic scheme (Closed - Inactivated - Open - Open-Blocked, with rate constants
alpha, beta, gamma, delta, epsilon, zeta, Con, Coff, Oon, Ooff and amplitude factors a and b)
provides the canonical implementation of resurgent Na current. Raman and Bean earlier 2001
formulation was extended here with the a/b factors that allow tuning of state-coupling amplitudes.
Every downstream "NaR" or "naRsg" mod-file in the NEURON model database traces to this scheme.

### Eight-Current Purkinje Soma Model in NEURON

First fully self-consistent single-compartment Purkinje soma model in which all eight current
parameter sets (Kfast, Kmid, Kslow, BK, Pca, Ih, leak, NaV1.6) were derived from currents recorded
from the same cell type and species. Table 1 of the paper provides V1/2, k, Gmax, gating exponents,
and reversal potentials for every current; this table is the parameter source for the bkpkj.mod and
Kpurk-family mod files vendored in the present project.

### Genetic Knockout Dissection of Resurgent Component

Use of the med (Scn8a -/-) mouse as a "natural knockout" of resurgent current and exploitation of
modeling to disentangle direct from compensatory effects: the paper shows that even though med cells
have changed Kfast V1/2 and reduced leak, those changes alone would speed firing - so the observed
slowing must be attributed to the lost resurgent kinetics specifically.

### Calcium Microdomain Modeling for BK

The 100 nm submembrane Ca shell with extrusion rate beta = 1/msec and zcoef = 0.001 mM provides a
simple but effective coupling between P-type Ca current and BK gating that reproduces observed BK
activation during AP repolarisation. This formalism is reused in the project bkpkj.mod.

## Datasets

* **Acutely dissociated mouse Purkinje neurons** from Scn8a-med (-/-) and wild-type littermates,
  postnatal day 14-20, Jackson Laboratories breeders. n = 18 wild-type and 18 med cells for
  current-clamp characterisation; smaller cohorts (n = 4-16) for each pharmacologically isolated
  current type. Genotyping by PCR (190 bp wild-type vs 370 bp mutant amplicon).
* No public dataset deposit; raw traces and parameter tables are reproduced in the paper figures and
  Table 1 / Table 2.
* The NEURON model files derived from this work are available in ModelDB as accession 48332
  ("Cerebellar Purkinje Cell: resurgent Na current and high frequency firing (Khaliq et al. 2003)").
  The bkpkj.mod and Naresurgent.mod files distributed with that ModelDB entry are the canonical
  source vendored by downstream model libraries including this project t0074 channel bundle.

## Main Ideas

* The bkpkj.mod and resurgent-Na NaR mod-file vendored on the BedB substrate trace directly to this
  paper Table 1 and Equation-1 state model. When stratifying NaR density across AIS tiers in t0078,
  the kinetic parameters (rate constants, V1/2, k, calcium-shell zcoef) inherited from this paper
  are the fixed scaffold; only Gmax (channel density) varies across tiers.
* Resurgent kinetics primarily affect **steady-state firing rate**, not action-potential threshold
  or shape - removing the blocked-state pathway slowed simulated firing by 19-38 percent without
  changing AP waveforms qualitatively. This means MOBO objectives that target firing rate are
  sensitive to NaR density, while AP-shape objectives are not - useful for diagnosing which
  parameters drive which DSGC objective in t0078.
* Non-sodium currents in the med model **compensate** for resurgent loss rather than amplify it; a
  positive shift in Kfast V1/2 plus reduced leak conductance both promote excitability. This argues
  that AIS K-channel densities and somatic leak should be co-optimized with NaR density rather than
  treated as independent axes - relevant to t0078 tier-stratified design.
* The eight-current parameter set in Table 1 (V1/2, k, Gmax, gating exponents) provides a validated
  default for any Purkinje-derived channel reused in DSGC modeling. When the t0078 MOBO proposes
  parameter regions for NaR or BK, this paper measured ranges (e.g. BK Gmax 26-113 nS in wild-type,
  K_fast V1/2 = -24 mV) define biologically plausible priors.
* The single-compartment 20 microm x 10 microm x 19 pF geometry is the simplest valid Purkinje-soma
  testbed for sanity-checking that vendored mod-files reproduce the paper ~27 Hz spontaneous firing
  rate before deploying them on the multi-compartment DSGC substrate - a useful regression test for
  the t0074 channel bundle.

## Summary

Khaliq, Gouwens, and Raman (2003) ask whether and how the resurgent component of NaV1.6 sodium
current promotes high-frequency action-potential firing in cerebellar Purkinje neurons. The question
matters because resurgent current - sodium current that flows when the channel exits an
open-channel-block state during repolarisation - is a peculiar, structurally distinctive feature of
NaV1.6 that had been correlated with rapid firing but never causally attributed to it. The authors
scope is somatic firing in dissociated Purkinje cells from wild-type and Scn8a-med mice; they hold
dendrites and synaptic input out of the analysis to focus on intrinsic excitability.

Methodologically, the paper combines whole-cell current-clamp action-potential recordings from
acutely dissociated Purkinje somata with voltage-clamped pharmacological isolation of seven
non-sodium currents (Kfast, Kmid, Kslow, BK, Pca, Ih, leak) and a NEURON-based single-compartment
model that integrates these seven currents with an explicit Raman-Bean state-machine model of NaV1.6
sodium current. The med phenotype - which lacks NaV1.6 and therefore has 90 percent reduced
resurgent current - is used as a natural knockout. The model is validated by reproducing wild-type
spontaneous firing at 27 spikes/sec (matching the 29 Hz experimental mean) and is then used to ask
which of the changes seen in med cells (lost resurgent current, modified Kfast V1/2, reduced leak)
actually drive the slower firing.

The headline finding is that resurgent kinetics specifically and consistently accelerate firing. Med
cells fired at 9 +/- 2 Hz spontaneously vs 35 +/- 4 Hz wild-type, and at 13 +/- 5 vs 65 +/- 7
spikes/sec under 50 pA injection, a deficit that survived even strong current injection (maximum
sustained rate 65 +/- 10 spikes/sec med vs 107 +/- 6 wild-type). Crucially, the model showed that
the small Kfast V1/2 shift and reduced leak found in med cells would, if anything, **speed** firing
\- so the observed slowdown must come from the sodium-channel kinetics. Replacing wild-type with
med-like Na kinetics in the model slowed simulated firing by 19-31 percent, reproducing the
experimental phenotype.

For the present project this paper is the kinetic foundation of the BedB substrate voltage-gated
channel library. The bkpkj.mod calcium-activated K channel and the NaR resurgent sodium mod-file
vendored in t0074 trace directly to this paper Equation-1 state model and Table 1 parameter set. For
t0078 specifically, the AIS-tiered NaR optimization treats this paper kinetic schemes as the fixed
scaffold and varies only channel density per tier - so any biological plausibility argument about
NaR density gradients ultimately rests on the parameter ranges established here. The paper 19 pF
single-compartment geometry also provides a minimal regression-test target: vendored mod-files
should reproduce ~27 Hz spontaneous firing in that geometry before being deployed on the
multi-compartment DSGC substrate.
