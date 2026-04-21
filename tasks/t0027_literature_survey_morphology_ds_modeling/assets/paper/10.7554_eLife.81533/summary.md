---
spec_version: "3"
paper_id: "10.7554_eLife.81533"
citation_key: "Srivastava2022"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# Spatiotemporal properties of glutamate input support direction selectivity in the dendrites of retinal starburst amacrine cells

## Metadata

* **File**: `files/srivastava_2022_sac-glutamate-ds.pdf`
* **Published**: 2022-11-08
* **Authors**: Prerna Srivastava 🇨🇦, Geoff de Rosenroll 🇨🇦, Akihiro Matsumoto 🇩🇰, Tracy Michaels 🇨🇦,
  Zachary Turple 🇨🇦, Varsha Jain 🇨🇦, Santhosh Sethuramanujam 🇨🇦, Benjamin L Murphy-Baum 🇨🇦, Keisuke
  Yonehara 🇩🇰, Gautam B Awatramani 🇨🇦
* **Venue**: eLife (open access, CC-BY 4.0)
* **DOI**: `10.7554/eLife.81533`

## Abstract

The asymmetric summation of kinetically distinct glutamate inputs across the dendrites of retinal
"starburst" amacrine cells is one of the several mechanisms that have been proposed to underlie
their direction-selective properties, but experimentally verifying input kinetics has been a
challenge. Here, we used two-photon glutamate sensor (iGluSnFR) imaging to directly measure the
input kinetics across individual starburst dendrites. We found that signals measured from proximal
dendrites were relatively sustained compared to those measured from distal dendrites. These
differences were observed across a range of stimulus sizes and appeared to be shaped mainly by
excitatory rather than inhibitory network interactions. Temporal deconvolution analysis suggests
that the steady-state vesicle release rate was ~3 times larger at proximal sites compared to distal
sites. Using a connectomics-inspired computational model, we demonstrate that input kinetics play an
important role in shaping direction selectivity at low stimulus velocities. Taken together, these
results provide direct support for the "space-time wiring" model for direction selectivity.

## Overview

This paper combines two-photon iGluSnFR glutamate imaging with a compartmental NEURON model to
directly test the "space-time wiring" model of direction selectivity (DS) in the mouse retina. The
space-time wiring hypothesis, motivated by connectomic reconstructions (Kim et al. 2014; Greene et
al. 2016), predicts that proximal and distal dendrites of ON starburst amacrine cells (SACs) receive
input from kinetically distinct bipolar cells (BCs) — sustained BC7 proximally and transient BC5
subtypes (5i/o/t) distally — such that centrifugal motion from soma to dendrite tip causes an
optimal, temporally-aligned summation of glutamate release along the dendrite. Prior iGluSnFR
surveys (Franke et al. 2017) reported that most BCs of the same polarity share similar temporal
kernels, appearing to contradict the model; Srivastava et al. reconcile these findings by showing
that kinetic divergence only emerges for stimuli larger than the BC receptive field.

Using AAV-delivered flex-iGluSnFR selectively expressed in ChAT-Cre SACs, the authors resolved
glutamate input at ~5 µm spatial grain along individual dendrites and across population fields of
view. They found a clear and robust proximal-to-distal gradient in sustained/transient index (STi),
which persisted when inhibition was pharmacologically blocked. Deconvolution with a fitted iGluSnFR
quantal kernel yielded per-site instantaneous vesicle release rates, which were fed as
Poisson-discretized event trains into a ball-and-stick NEURON model. Systematically swapping or
homogenizing the proximal/distal kinetic profiles reversed or abolished the model's preferred
direction, providing the first mechanistic, input-kinetics-grounded confirmation of the space-time
wiring hypothesis. The authors note this direction-selectivity benefit is specific to slow motion (<
0.5 mm/s) and must be complemented by other mechanisms at high velocities.

**Borderline / scope note**: This paper studies the SAC (starburst amacrine cell), not the DSGC
itself. It is included in the survey because it jointly (a) builds a compartmental SAC model and (b)
varies the spatiotemporal pattern of bipolar→SAC glutamate release *on the dendrite* — an
"input-on-dendrite morphology" manipulation that is directly relevant to how DSGC-afferent circuitry
computes direction.

## Architecture, Models and Methods

**Imaging.** Intravitreal AAV (pAAV.hSyn.Flex.iGluSnFR) in ChAT-IRES-Cre mice (P21+, C57BL/6J),
imaged 3+ weeks post-injection at 920 nm with 8 kHz resonant-galvo-galvo scanning. Frame rate 58.25
Hz (256×256 px) for sequential proximal/distal planes, or 22.5 Hz with an electrically-tunable lens
for near-simultaneous dual-plane acquisition. ROIs of 5×5 µm (and 10×10 µm for grid tiling) were
placed along SAC dendrites, with SNR > 4 selection. Stimuli were static spots of diameter 100, 200,
400, or 800 µm presented 2 s; background ~1000 photon/µm²/s.

**Pharmacology.** 20 µM CNQX, 100 µM TPMPA, 5 µM SR-95531 (a.k.a. gabazine). Cocktail blocks
inhibitory (GABA_A, GABA_C) pathways and ionotropic glutamate receptors on amacrine/horizontal
cells.

**Temporal deconvolution.** Division in the Fourier domain of the measured iGluSnFR response by an
idealized quantal waveform (2 ms rise, 30 ms decay, fit from spontaneous quantal events). Quantal
size per ROI estimated as QSE = 2σ²/µ (Katz–Miledi). The resulting instantaneous release rate was
discretized via a 1 ms-timestep Poisson process, yielding per-site vesicle release event trains.

**Compartmental model.** NEURON ball-and-stick SAC with one soma and three dendritic compartments
(initial, middle, terminal) per Ding et al. 2016 and Vlasits et al. 2016. For each trial, **6
proximal** (BC7, sustained) and **12 distal** (BC5, transient) synapses were sampled pseudo-randomly
from Ding 2016's empirical BC location PDFs. A 400 µm-wide moving bar activated BCs sequentially at
velocities 0.1–2 mm/s; each BC's output terminated when the bar exited its 60 µm receptive field.
Each vesicle triggered an AMPA miniature (rise 0.14 ms, decay 0.54 ms, reversal 0 mV); synaptic
conductances scaled linearly from **172.2 pS proximally to 68.6 pS distally**. DSi was defined as
the normalized difference between centrifugal and centripetal peak terminal Ca²⁺ concentration.

## Results

* Peak iGluSnFR ΔF/F was approximately stable along single dendrites, but the sustained-phase
  amplitude fell from **ΔF/F = 0.80 ± 0.29 proximally to 0.29 ± 0.16 distally** (20 dendrites, 4
  retinas, 4 mice; p < 0.001, t-test).
* Sustained/Transient index STi dropped from **0.33 ± 0.06 proximal to 0.16 ± 0.05 distal** on
  single dendrites, and from **0.34 ± 0.07 (n=242) to 0.21 ± 0.07 (n=563)** in population ROIs
  across 10 FOVs from 8 retinas (p < 0.001, t-test).
* Kinetic proximal/distal differences persisted under the full inhibition blockade cocktail (5 µM
  gabazine, 100 µM TPMPA, 20 µM CNQX; n=71 proximal and 431 distal ROIs, p < 0.001, KS-test); the
  plateau phase actually grew by **~23% proximally and ~20% distally** between 200 and 800 µm spots,
  revealing a lateral-excitation network beyond the 50 µm BC dendritic field.
* Temporal deconvolution estimated steady-state release rates of **~3 vesicles/s at proximal BC7
  sites vs ~1 vesicle/s at distal BC5 sites** (3× ratio), with peak instantaneous release of **5–10
  vesicles/s** per BC terminal.
* In the NEURON model, **swapping** proximal-distal kinetics reversed the preferred direction (DSi
  became negative), and **homogenizing** all BCs to either all-sustained or all-transient strongly
  decreased DSi. The native sustained-transient arrangement produced significantly higher DSi than
  all-sustained up to 0.5 mm/s (p < 0.0005, t-test), and manipulation effects on DSi were
  significant up to **1 mm/s** (p < 0.05, one-way ANOVA).
* Incrementally converting proximal (sustained) synapses into transient ones, starting from the site
  furthest from the soma, decreased DSi linearly at 0.15 mm/s stimulus velocity.
* The magnitude of DSi scaled linearly with the mean proximal-distal BC separation distance on each
  trial (R² ≈ 0.208 native, R² ≈ 0.269 swapped-kinetics condition).
* White-noise reverse-correlation kernels were biphasic but indistinguishable between proximal and
  distal inputs, indicating that the kinetic advantage only manifests for step/flash stimuli, not
  for continuously-stimulated regimes.

## Innovations

### Direct measurement of glutamate input kinetics on a single SAC dendrite

First study to resolve sustained vs transient glutamate release kinetics on single starburst
dendrites using cell-targeted Cre-dependent iGluSnFR at ~5 µm ROI grain — circumventing the
post-synaptic ambiguity of somatic voltage-clamp and the bulk-average limitation of non-targeted
iGluSnFR.

### Quantal deconvolution to recover vesicle release rates per site

Transformation of iGluSnFR fluorescence into per-ROI instantaneous vesicle release rates, using a
fitted quantal kernel and fluctuation-analysis-based quantal size. Converts an indicator-shaped
signal into a biophysically-interpretable input drive usable inside a compartmental model.

### Connectomics-constrained, release-rate-driven compartmental model

Ball-and-stick NEURON SAC model whose synapses are sampled from Ding et al. 2016 BC location PDFs (6
BC7 proximal + 12 BC5 distal per trial) and whose synaptic inputs are driven by experimentally
measured release rates — rather than being optimized by an algorithm to maximize DS (as in Ezra-Tsur
et al. 2021) or being a phenomenological LN cascade (as in Kim et al. 2014). Systematic
swap/homogenize/graded-conversion manipulations provide a causal in silico test of the space-time
wiring hypothesis.

### Reconciliation of conflicting iGluSnFR surveys

Resolves the apparent contradiction between connectomic predictions and prior BC surveys (Franke et
al. 2017) by showing kinetic divergence is stimulus-size dependent — invisible for small spots
covering only a single BC receptive field but robust for the 200–800 µm stimuli that actually drive
SAC dendrites during natural motion.

## Datasets

This is primarily an experimental study, not a shared-dataset paper. The empirical data were
collected from the authors' own ChAT-Cre mouse cohorts (P21+ C57BL/6J; 4 mice/4 retinas for
single-dendrite imaging, 8 mice/8 retinas for population imaging, 4 mice/4 retinas for drug-cocktail
experiments). The BC7/BC5 synapse location probability density functions used as the model priors
were taken from the public connectomic data of **Ding, Smith, Poleg-Polsky, Diamond, Briggman (2016,
*Nature* 535:105)**. Stimulus generation used the open-source StimGen Python toolbox
(https://github.com/benmurphybaum/StimGen). NEURON model source code and parameters are provided as
the paper's Figure 6-source data 1.

## Main Ideas

* **Space-time wiring is real but narrow.** The proximal-sustained / distal-transient glutamate
  kinetic gradient exists and helps SAC direction selectivity, but its contribution is confined to
  slow velocities (< 0.5–1 mm/s); faster motion must rely on other mechanisms (intrinsic dendritic
  nonlinearities, GABAergic inhibition, Ca²⁺-channel kinetics).
* **Input kinetics must be driven by release rates, not indicator fluorescence, inside a model.**
  iGluSnFR has its own kinetics that differ from native AMPARs; deconvolving to release rates and
  re-driving AMPA minis inside a compartmental model is the correct pipeline for linking imaging to
  dendritic computation. This is directly transferrable to DSGC modeling.
* **Stimulus geometry matters.** Small-spot iGluSnFR surveys underestimate kinetic diversity because
  the key mechanisms are excitatory-network lateral coupling that only engages for stimuli larger
  than one BC receptive field (~50–60 µm). Any DS modeling study that constrains BC kinetics from
  small-spot data alone will underestimate space-time wiring's contribution.
* **Connectomic BC location PDFs are usable priors.** Ding 2016 BC7/BC5 PDFs, combined with 6
  proximal + 12 distal per-trial Poisson sampling, give a tractable and biologically realistic input
  distribution — a template reusable for DSGC modeling where analogous connectomic priors exist.
* **SAC-level morphology-input interaction is a distinct layer of DS computation** upstream of DSGC
  spike generation; the morphological literature survey for DSGC DS must treat the SAC as a
  computationally distinct pre-processing stage whose DS is itself morphology-shaped.

## Summary

This paper addresses a longstanding open question in retinal direction selectivity: whether the
connectomically-inspired "space-time wiring" model — in which proximal starburst amacrine cell (SAC)
dendrites receive tonic/sustained glutamate release from BC7 bipolar cells and distal dendrites
receive transient release from BC5 subtypes — is experimentally verifiable and computationally
sufficient to shape SAC dendritic direction selectivity. Prior imaging surveys had reported uniform
BC kinetics, casting doubt on the model, while prior connectomic and voltage-clamp work had left the
input-kinetic verification gap unclosed. Srivastava et al. close this gap by combining SAC-targeted
iGluSnFR imaging with compartmental modeling.

Methodologically, the authors injected Cre-dependent iGluSnFR into ChAT-Cre mouse retinas and imaged
glutamate signals at 5 µm ROI resolution along individual ON-SAC dendrites and across population
fields of view, varying stimulus spot size from 100 to 800 µm and applying a GABA_A/GABA_C/AMPA
blocker cocktail to isolate network contributions. They then deconvolved the fluorescence with a
fitted quantal iGluSnFR kernel to recover per-site vesicle release rates, which they fed into a
ball-and-stick NEURON SAC model whose synapse positions were sampled from Ding et al. 2016
connectomic BC7/BC5 probability density functions (6 proximal + 12 distal per trial).

Empirically, they find a robust proximal-to-distal gradient in sustained/transient index (STi ≈ 0.33
proximal vs 0.16 distal on single dendrites, 0.34 vs 0.21 at population level), a 3× higher
steady-state release rate proximally (~3 vs ~1 vesicles/s), persistence of this gradient under full
inhibitory blockade, and — critically — in silico demonstrations that swapping the proximal/distal
kinetic arrangement reverses the SAC's preferred direction, that homogenizing kinetics abolishes DS,
and that DSi grows linearly with proximal-distal BC separation distance. The effect is statistically
significant up to 1 mm/s stimulus velocity and strongest below 0.5 mm/s.

For the present project's morphology-shapes-DS literature survey, this paper is important for three
reasons. First, it is a clean example of **input-on-dendrite morphology** shaping DS: the spatial
arrangement of kinetically distinct synaptic inputs *along* the SAC dendrite, rather than the
dendritic branching structure per se, produces the DS signal — a mechanism readily generalizable to
DSGC models constrained by connectomic priors. Second, it provides a validated pipeline (iGluSnFR →
temporal deconvolution → release-rate-driven NEURON model) reusable for DSGC studies. Third, it
delineates the **scope limitation** of the space-time-wiring mechanism (slow stimuli only), which
must be respected when extrapolating to DSGC DS where high-velocity DS is known to be robust. The
paper is tagged "SAC, not DSGC" in our survey: it operates one layer upstream of the canonical DSGC
but contributes a mechanism that any end-to-end morphology-DS model of the DSGC-afferent circuit
must incorporate.
