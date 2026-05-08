---
spec_version: "3"
paper_id: "10.1007_s00424-024-02980-7"
citation_key: "Muller2024"
summarized_by_task: "t0091_morphology_extended_nsga2_v1"
date_summarized: "2026-05-08"
---
# Persistent sodium currents in neurons: potential mechanisms and pharmacological blockers

## Metadata

* **File**: `files/muller_2024_persistent-sodium-currents-review.pdf`
* **Published**: 2024-07-05 (online), Vol 476:1445-1473
* **Authors**: Peter Mueller 🇩🇪, Andreas Draguhn 🇩🇪, Alexei V. Egorov 🇩🇪
* **Venue**: Pfluegers Archiv - European Journal of Physiology (Springer Nature, CC-BY)
* **DOI**: `10.1007/s00424-024-02980-7`

## Abstract

Persistent sodium current (INaP) is an important activity-dependent regulator of neuronal
excitability. It is involved in a variety of physiological and pathological processes, including
pacemaking, prolongation of sensory potentials, neuronal injury, chronic pain and diseases such as
epilepsy and amyotrophic lateral sclerosis. Despite its importance, neither the molecular basis nor
the regulation of INaP are sufficiently understood. Of particular significance is a solid knowledge
and widely accepted consensus about pharmacological tools for analysing the function of INaP and for
developing new therapeutic strategies. However, the literature on INaP is heterogeneous, with
varying definitions and methodologies used across studies. To address these issues, we provide a
systematic review of the current state of knowledge on INaP, with focus on mechanisms and effects of
this current in the central nervous system. We provide an overview of the specificity and efficacy
of the most widely used INaP blockers: amiodarone, cannabidiol, carbamazepine, cenobamate,
eslicarbazepine, ethosuximide, gabapentin, GS967, lacosamide, lamotrigine, lidocaine, NBI-921352,
oxcarbazepine, phenytoine, PRAX-562, propofol, ranolazine, riluzole, rufinamide, topiramate,
valproaic acid and zonisamide. We conclude that there is strong variance in the pharmacological
effects of these drugs, and in the available information. At present, GS967 and riluzole can be
regarded bona fide INaP blockers, while phenytoin and lacosamide are blockers that only act on the
slowly inactivating component of sodium currents.

## Overview

This is a systematic review of persistent sodium current (INaP) in CNS neurons, organised around two
themes: (1) the biophysical and molecular mechanisms that produce a non-inactivating or slowly
inactivating component of voltage-gated sodium current, and (2) a comprehensive pharmacological
catalogue of 22 drugs that have been claimed to block INaP. The authors performed a PubMed search
using
`(persistent OR slow inactivation OR late) AND (sodium current) AND (block OR inhibit OR reduce)`,
retrieving 2,586 hits, then applied a per-drug second pass for each candidate substance. Inclusion
required voltage-clamp data from CNS neurons or HEK/CHO cells expressing brain-relevant
alpha-subunits (Nav1.1, Nav1.2, Nav1.3, Nav1.6) using a recognised INaP isolation protocol.

The review proposes a clear taxonomy of four candidate mechanisms underlying INaP: (i) modified
Hodgkin-Huxley window current with non-zero asymptotic inactivation; (ii) Markov-style channel
gating that allows inactivated-state-from-closed transitions or modal gating with sustained
openings; (iii) subtype-specific contributions from Nav1.6, Nav1.1, Nav1.2 and Nav1.3 alpha-subunits
plus auxiliary beta1/beta4 modulation; and (iv) supra-molecular cooperative gating between adjacent
sodium channels. None alone explains all observations - the authors argue these mechanisms co-exist
and reveal themselves differently across cell types and stimulus protocols.

The pharmacological catalogue is the second major contribution. For each drug it tabulates
preparation, voltage-clamp protocol (step-pulse, slow ramp, slow steady-state inactivation), IC50 or
EC50, effect on INaP versus on transient INaT, holding potential, and the original study. The review
concludes that GS967 and riluzole are the only drugs with consistent strong effects on INaP across
both step and ramp protocols at submicromolar to low-micromolar concentrations and without dominant
off-target actions; phenytoin and lacosamide selectively block the slowly inactivating component
(intermediate and slow inactivation respectively) but spare the truly non-inactivating component;
all other 18 drugs are confounded by off-target effects on calcium channels, GABA receptors, hERG
potassium channels, or by missing data on slow inactivation.

A persistent (pun intended) message is methodological: the term "persistent" is misleading,
INaP-isolation protocols disagree, and slow voltage ramps may underestimate INaP via slow
inactivation during the ramp itself. The authors recommend that all future INaP studies combine
brief steps (50-100 ms), intermediate-inactivation steps (500-1000 ms), slow-inactivation steps
(5-10 s), and slow ramps (<= 50 mV/s) with TTX-subtraction controls.

## Architecture, Models and Methods

This is a non-experimental review. Methods are split between the literature-search procedure and a
critical analysis of voltage-clamp protocols.

* **Literature search**: PubMed query
  `(((persistent) OR (slow inactivation) OR (late)) AND (sodium current)) AND ((block) OR (inhibit) OR (reduce))`
  returned **2,586 results**. Papers were screened to retain pharmacological agents with potential
  clinical use, excluding endogenous substances, toxins (with TTX as a methodological exception),
  insecticides, dyes, and intracellular agents like QX-314. A second drug-specific PubMed search was
  then run for each candidate. Eligibility required voltage-clamp protocols on CNS neurons or
  HEK/CHO cells expressing Nav1.1, Nav1.2, Nav1.3 or Nav1.6.

* **Mechanistic taxonomy**: Four hypotheses are formalised. (1) The original Hodgkin-Huxley model
  window-current is too small to explain INaP and predicts the wrong voltage dependence; the
  Taddese-Bean modified window-current makes h-infinity depend on m-infinity and produces a residual
  current even at depolarised potentials. (2) Markov gating models with two open states or with
  modal gating (sustained burst-like openings) reproduce INaP equivalently to the modified
  window-current. (3) Subtype-specific generation: Nav1.6 carries the largest CNS INaP contribution
  but ~50 percent of INaP remains after Nav1.6 knockout in cortical layer-5 pyramidal neurons;
  Nav1.1, Nav1.2, Nav1.3 all generate INaP; Nav1.8 and Nav1.9 carry DRG INaP but are absent from
  cortex (single-cell transcriptomic evidence). The beta1 subunit normalises INaP, beta4 increases
  it, and beta1 knockout makes some sodium-channel blockers paradoxically enhance INaP. (4) Coupled
  gating: physical interactions between adjacent Nav channels alter their effective gating kinetics.

* **Voltage-clamp protocol catalogue** (Fig. 2 of the paper): four protocols are formally defined.
  (a) Brief step pulse (50-500 ms) where current at the end of the pulse is the persistent
  component. (b) Entry-into-slow-inactivation: long depolarising prepulse (1-30 s), short
  hyperpolarising recovery (0.5-1 s), short test pulse (15 ms). (c) Slow steady-state inactivation:
  variable prepulse from -120 to +50 mV (1-10 s), brief recovery (0.5-1 s), test pulse (10 ms). (d)
  Slow voltage ramp at 10-70 mV/s from -80 to +10 mV with TTX-subtraction. Each protocol picks up a
  different subset of the inactivation manifold, and the review emphasises that brief pulses miss
  slow inactivation while slow ramps may include it artefactually.

* **Drug analysis**: 22 substances analysed: amiodarone, cannabidiol, carbamazepine, cenobamate,
  eslicarbazepine, ethosuximide, gabapentin, GS967, lacosamide, lamotrigine, lidocaine, NBI-921352,
  oxcarbazepine, phenytoin, PRAX-562, propofol, ranolazine, riluzole, rufinamide, topiramate, TTX,
  valproic acid, zonisamide. Each is tabulated by IC50/EC50, preparation, protocol, holding
  potential, and effects on INaP versus INaT (Table 1, ~5 pages of structured data).

## Results

* **Best CNS INaP blockers**: GS967 and riluzole are the only two drugs with strong effects on INaP
  across both step and ramp protocols at clinically relevant concentrations (riluzole IC50 **< 10
  uM** in step and ramp; GS967 in low-micromolar range in cortical and CA3 neurons), without
  dominant off-target actions on Ca, K, or GABA targets.
* **Best slow-inactivation enhancers**: Lacosamide is the prototypic slow-inactivation enhancer;
  phenytoin selectively enhances intermediate inactivation. Both leave the truly non-inactivating
  component largely unaffected when measured with brief 50 ms steps - they appear as INaP blockers
  only when slow ramps or long pulses are used.
* **Carbamazepine** is a fast-inactivation enhancer (EC50 **16 uM** for amplitude of Nav1.3 step
  pulse, **8 mV** left shift of V0.5 of steady-state inactivation; **48 percent** ramp-amplitude
  block at 100 uM in dentate gyrus; multiple HEK studies). It is sodium-specific but does not
  primarily target INaP.
* **Nav1.6 dominance**: Nav1.6 carries a major share of CNS INaP. Nav1.6 knockout in rat cortical
  layer-5 leaves ~**50 percent** of INaP intact, indicating substantial Nav1.1/1.2/1.3 contribution.
  The Nav1.6-driven left shift of INaP activation relative to INaT is consistent with this
  dominance.
* **Subunit beta-effects**: beta4 increases INaP, beta1 neutralises this. Knockout of beta1
  paradoxically flips some sodium channel blockers into INaP enhancers, a confound for any in vivo
  INaP pharmacology.
* **Drugs disqualified for INaP work**: cannabidiol (IC50 ~**3 uM** for INaT in HEK Nav1.6;
  inconsistent INaP data), ethosuximide, gabapentin, rufinamide, zonisamide (insufficient or null
  data); ranolazine and amiodarone (poor blood-brain-barrier penetration, **only 10 percent**
  brain/heart for amiodarone, **one third** for ranolazine); cenobamate, eslicarbazepine,
  lamotrigine, oxcarbazepine, propofol, topiramate, valproic acid (large off-target effects on Ca
  channels, GABA-A, hERG, mGluR5, or carbonic anhydrase).
* **NBI-921352 and PRAX-562**: novel Nav1.6-preferential drugs from Xenon and Praxis Precision
  Medicines respectively; show promise as INaP blockers in HEK assays but lack neuronal data.
* **Methodological pitfall**: slow voltage ramps at 10-70 mV/s span tens of seconds, so they
  partially measure slow inactivation rather than pure non-inactivating current. The well-known
  ramp-direction hysteresis is a direct signature of this contamination. Faster ramps (>233 mV/s)
  instead trigger voltage-clamp escape action currents in cortical pyramidal neurons.
* **Recommended INaP toolkit**: combine brief steps (~50 ms), intermediate-inactivation steps
  (500-1000 ms), slow steady-state inactivation steps (5-10 s), and slow ramps (~50 mV/s) with TTX
  subtraction. Pharmacologically, claims of INaP involvement should require concordant effects of at
  least two drugs **or** a non-pharmacological corroboration like dynamic clamp cancellation.

## Innovations

### Comprehensive 22-Drug INaP Pharmacological Catalogue

The first systematic per-drug catalogue (Table 1, ~70 study rows) of INaP pharmacology in CNS
neurons and brain-relevant Nav-expressing heterologous cells. Each row reports preparation,
voltage-clamp protocol, IC50/EC50, holding potential, and parallel effects on INaP versus INaT. This
is the new community reference for choosing INaP-blocking drugs and interpreting prior literature.

### Protocol-Mechanism Correspondence

Explicit mapping between voltage-clamp protocols and the inactivation kinetic component each
isolates: brief steps probe non-inactivating current, 500-1000 ms steps probe intermediate
inactivation, 5-10 s steps probe slow inactivation, 10-70 mV/s ramps mix all three. The review shows
that the literature longstanding disagreement about whether phenytoin or lacosamide block INaP
largely dissolves once protocol-component correspondence is acknowledged.

### Bona Fide vs Conditional INaP-Blocker Classification

Operational distinction between bona fide INaP blockers (GS967, riluzole - act on the truly
non-inactivating component at brief steps and at slow ramps) and conditional blockers (phenytoin,
lacosamide - only act on slowly inactivating components). This classification reframes the
antiseizure-drug literature, which had loosely lumped all of these as INaP blockers.

### Mechanism Pluralism

Argues that no single mechanism fully accounts for INaP, and that window-current, Markov gating,
subtype-specific generation, and supra-molecular cooperativity all coexist. The review uses this
pluralism to explain why pharmacological isolation is inherently difficult and why no future drug is
likely to be a perfectly clean INaP blocker.

## Datasets

This is a literature-review paper - no experimental datasets are produced. The systematic-review
inputs are listed in the methods:

* **PubMed corpus**: 2,586 papers retrieved by the primary query, then filtered to ~70 studies
  contributing to Table 1.
* **Per-drug second-pass searches**: one PubMed query per candidate substance (22 drugs).
* **References list**: 256 cited papers spanning 1952-2024, with strong representation of the
  Hodgkin-Huxley, Taddese-Bean, French-Sah, Crill, Bean, Yaari, Dichter, and Catterall schools on
  sodium-channel kinetics and pharmacology.

The review Table 1 itself functions as a structured derived dataset: drug x preparation x protocol x
IC50/EC50 x HP x effect-on-INaP x effect-on-INaT x source-citation. This table is publicly
distributed under CC-BY 4.0 with the article.

## Main Ideas

* **No DSGC-specific INaP measurement is reported** in this review. The systematic search did not
  surface a study measuring the dendritic-to-somatic INaP density gradient in any retinal ganglion
  cell, let alone a direction-selective ganglion cell. The cortical-pyramidal Stuart 1999 / Astman
  2021 priors used in this project biological-plausibility scorecard remain the best available
  cross-cell baseline; t0091 distal-NaP density bounds do not need to be revised because of new DSGC
  data - there is no new DSGC data.
* **Slow voltage ramps may underestimate INaP** because slow inactivation accumulates during the
  ramp itself. This is a methodological caution for any future DSGC patch-clamp measurements but
  does not affect t0091 NSGA-II morphology sweep, which uses NEURON Hodgkin-Huxley channels with
  deterministic kinetics rather than empirical voltage-clamp measurements.
* **Most CNS INaP comes from Nav1.6**, but ~50 percent persists after Nav1.6 knockout in cortical
  layer-5. For DSGC compartmental modelling this implies that a single NaP density parameter is a
  coarse but defensible abstraction over a heterogeneous subunit mixture - which is exactly what the
  project existing NaP NMODL implementation assumes.
* **beta-subunit knockout flips some blockers into INaP enhancers**. This is a confound for any
  pharmacological validation strategy and reinforces this project policy of staying in pure
  computational-model territory rather than attempting wet-lab pharmacology.
* **GS967 and riluzole are the two reliable INaP-isolating drugs** for any future
  experimental-validation step that the project might pursue. If dynamic-clamp-style in-silico
  cancellation experiments are ever attempted, riluzole-equivalent block at 10 uM is the
  conventional reference manipulation.

## Summary

Mueller, Draguhn, and Egorov publish a systematic review of persistent sodium current (INaP) in CNS
neurons in Pfluegers Archiv (Springer Nature, open access). The motivation is that INaP is a
clinically important regulator of excitability - implicated in epilepsy, amyotrophic lateral
sclerosis, neuropathic pain, hemiplegic migraine, and post-injury hyperexcitability - but the
literature is fragmented across heterogeneous voltage-clamp protocols, inconsistent definitions of
persistent versus slowly inactivating, and a sprawling catalogue of putative blocker drugs whose
specificities have never been compared head-to-head.

The review proceeds in two parts. The first part formalises four candidate mechanisms (modified
Hodgkin-Huxley window current; Markov gating with closed-state inactivation or modal gating;
subtype-specific generation by Nav1.1/1.2/1.3/1.6 plus beta1/beta4 modulation; supra-molecular
coupled gating) and four canonical voltage-clamp protocols (brief step, entry-into-slow
inactivation, slow steady-state inactivation, slow ramp). It explicitly maps which protocol isolates
which kinetic component, dissolving longstanding terminological disagreements. The second part is a
22-drug catalogue (Table 1) tabulating IC50/EC50, holding potential, preparation, protocol, and
effects on INaP versus INaT for each substance.

The headline finding is that GS967 and riluzole are the only bona fide INaP blockers - they act on
the truly non-inactivating component across both brief-step and slow-ramp protocols at clinically
achievable concentrations and with limited off-target action. Phenytoin and lacosamide are
reclassified as selective enhancers of intermediate and slow inactivation respectively, not INaP
blockers proper. All other 18 surveyed substances are disqualified by off-target Ca, K, GABA, or
mGluR effects, by poor blood-brain-barrier penetration, or by inadequate slow-inactivation data. The
review concludes with a methodological recommendation: combine brief steps, slow-inactivation steps,
and slow ramps with TTX subtraction, and require concordant effects of two drugs or a dynamic-clamp
control before claiming an INaP role for any physiological phenomenon.

For this project, the review most important message is a negative one: there is no DSGC-specific
INaP density measurement in the surveyed literature, so the cortical-pyramidal Stuart 1999 / Astman
2021 priors used in t0086 / t0088 / t0091 remain the best cross-cell baseline and the
morphology-extended NSGA-II distal-NaP density bounds do not need to be revised. The methodological
caution that slow ramps underestimate INaP is a prior to keep on file for any future patch-clamp
validation step but does not affect the present in-silico NEURON-based optimisation pipeline. The
drug catalogue is a useful reference if the project ever extends into dynamic-clamp
INaP-cancellation experiments, where riluzole-equivalent block at 10 uM is the canonical reference
manipulation.
