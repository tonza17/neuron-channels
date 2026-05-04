---
spec_version: "3"
paper_id: "10.1523_JNEUROSCI.0808-13.2013"
citation_key: "Trenholm2013"
summarized_by_task: "t0078_bedb_mobo_v2_ais_tiered_ahp"
date_summarized: "2026-05-03"
---
# Dynamic Tuning of Electrical and Chemical Synaptic Transmission in a Network of Motion Coding Retinal Neurons

## Metadata

* **File**: `files/trenholm_2013_dsgc-electrical-coupling.pdf`
* **Published**: 2013-09-11
* **Authors**: Stuart Trenholm 🇨🇦, Amanda J. McLaughlin 🇨🇦, David J. Schwab 🇺🇸,
  Gautam B. Awatramani 🇨🇦
* **Venue**: The Journal of Neuroscience, 33(37):14927–14938
* **DOI**: `10.1523/JNEUROSCI.0808-13.2013`

## Abstract

Recently, we demonstrated that gap junction coupling in the population of superior coding ON-OFF
directionally selective ganglion cells (DSGCs) genetically labeled in the Hb9::eGFP mouse retina
allows the passage of lateral anticipatory signals that help track moving stimuli. Here, we examine
the properties of gap junctions in the DSGC network, and address how interactions between electrical
and chemical synapses and intrinsic membrane properties contribute to the dynamic tuning of lateral
anticipatory signals. When DSGC subtypes coding all four cardinal directions were individually
loaded with the gap junction-permeable tracer Neurobiotin, only superior coding DSGCs exhibited
homologous coupling. Consistent with these anatomical findings, gap junction-dependent feedback
spikelets were only observed in Hb9+ DSGCs. Recordings from pairs of neighboring Hb9+ DSGCs revealed
that coupling was reciprocal, non-inactivating, and relatively weak, and provided a substrate for an
extensive subthreshold excitatory receptive field around each cell. This subthreshold activity
appeared to boost coincident light-driven chemical synaptic responses. However, during responses to
moving stimuli, gap junction-mediated boosting appeared to be dynamically modulated such that
upstream DSGCs primed downstream cells, but not vice versa, giving rise to highly skewed responses
in individual cells. We show that the asymmetry in priming arises from a combination of spatially
offset GABAergic inhibition and activity-dependent changes in intrinsic membrane properties of
DSGCs. Thus, dynamic interactions between electrical and chemical synapses and intrinsic membrane
properties allow the network of DSGCs to propagate anticipatory responses most effectively along
their preferred direction without leading to runaway excitation.

## Overview

This study uses the Hb9::eGFP transgenic mouse retina to characterise how gap junctions, chemical
synapses, and intrinsic membrane properties jointly shape direction-selective ganglion cell (DSGC)
responses to moving stimuli. Using Neurobiotin tracer-coupling, paired whole-cell patch-clamp
recordings, and pharmacological manipulations (TTX, 18-beta-glycyrrhetinic acid, picrotoxin), the
authors first establish that only superior-coding DSGCs (the GFP+ population) form a homologously
coupled electrical network in mouse retina. They then dissect the network dynamics: gap junctions
are reciprocal, weak (coupling coefficient ~0.14, gap-junction conductance ~1 nS), low-pass with
corner frequency ~10 Hz, and crucially non-inactivating to sustained voltage steps.

The functional payoff is a lateral priming mechanism: upstream coupled DSGCs add subthreshold
excitatory drive to downstream neighbours via gap junctions, lowering the contrast threshold and
allowing moving stimuli to drive spikes ~100 um outside the classical receptive field. The first
spikes during preferred-direction motion are gap-junction-dependent (eliminated by 18-beta-GA),
giving the network its anticipatory, lag-normalising behaviour described in the companion Nat
Neurosci paper (Trenholm, Schwab, Balasubramanian, Awatramani 2013, cited within this paper).

The most distinctive contribution of this paper is the explanation for why responses are
asymmetrically skewed toward the leading edge despite the underlying gap-junction conductance being
electrically symmetric. The authors show that two postsynaptic mechanisms gate gap-junction
efficacy: (i) spatially offset GABAergic inhibition from starburst amacrine cells (offset 52 +/- 9
um toward the null side), and (ii) activity-dependent intrinsic gain control that raises the
apparent spike threshold during a sustained spike train (recovery time constant 604 +/- 158 ms). The
second mechanism is dominant: even with GABA-A receptors blocked by picrotoxin, responses remain
skewed toward the leading edge for both preferred and null directions.

This work is directly relevant to projects modelling DSGC firing rates, because it provides the
authoritative source for the **peak (not mean)** firing rates that researchers often quote for mouse
Hb9+ DSGCs in standard moving-bar protocols: peak preferred-direction rate **198 +/- 14 Hz** and
peak null-direction rate **27 +/- 12 Hz** under control conditions, rising to **244 +/- 18 Hz** and
**202 +/- 14 Hz** respectively under picrotoxin (GABA-A block).

## Architecture, Models and Methods

This is an experimental electrophysiology study, not a modelling paper. The preparation is the
whole-mount retina from adult C57BL/6 wild-type or Hb9::eGFP transgenic mice of either sex,
maintained on 12-h light/dark cycles and dark-adapted 30-60 min before dissection. Retinas are
perfused with bicarbonate Ringer at 35-37 C (110 NaCl, 2.5 KCl, 1 CaCl2, 1.6 MgCl2, 10 dextrose, 22
NaHCO3, bubbled 95% O2 / 5% CO2, pH 7.4).

GFP+ DSGCs are visually targeted under two-photon imaging at 950 nm (low-bleach for photoreceptors)
on an upright Olympus BX51 WI scope with a 40x water-immersion lens. Recordings use a MultiClamp
700B at 10 kHz. Three pipette solutions are used: (a) Ringer for loose cell-attached extracellular
spike recording (5-10 MOhm); (b) Cs-methanesulfonate (112.5 CH3CsO3S, 1 MgSO4, 10 EGTA, 10 HEPES, 4
ATP-Mg, 0.5 GTP-Na, 5 QX-314, 0.025 Alexa 594, 7.75 Neurobiotin, pH 7.2-7.3 with CsOH) for
voltage-clamp at +40 / 0 / -60 mV; (c) K-gluconate (115 K-gluconate, 9.7 KCl, 1 MgCl2, 0.5 CaCl2,
1.5 EGTA, 10 HEPES, 4 ATP-Mg, 0.5 GTP-Na, 0.025 Alexa 594, 7.75 Neurobiotin, pH 7.2-7.3 with KOH)
for current-clamp. Estimated GABA reversal is approximately -60 mV. Pharmacology: 1 uM TTX (Na
block), 25 uM 18-beta-glycyrrhetinic acid (gap-junction block, applied 10-20 min), 50 uM picrotoxin
(GABA-A block).

Stimuli are generated by a digital projector (Hitachi Cpx1, 75 Hz) with Psychtoolbox; ambient
intensity 3 x 10^12 photons/s/cm^2. The standard moving stimulus is a 300 x 300 um bar at 96%
positive Weber contrast moving at 600 um/s in eight directions; preferred direction and DSI are
computed from the vector sum of peak spike rates as (Pref - Null) / (Pref + Null). Receptive fields
are mapped with a 40 um spot flashed for 1 s at pseudorandom positions; spike trains are converted
to firing rate by Gaussian convolution (sigma = 25 ms). Transmission delays are estimated from the
flashing-bar onset latency (~60 ms -> 36 um spatial offset at 600 um/s) and used to align moving
responses to static receptive fields. Coupling is quantified by coupling coefficient (acceptor dV /
donor dV at +/-80 / +120 / +200 pA DC steps and 1-100 Hz pulses) and gap-junction conductance via
the Fortier and Bagna (2006) method. Skew is quantified by skew index SI = (start-to-peak) /
(peak-to-end). Statistics are paired/unpaired t-tests, with Mann-Whitney / signed-rank as
non-parametric fallbacks; n is cells or pairs (typically 5-25). Data are mean +/- SEM throughout.

## Results

* **Reciprocal homologous coupling** is exclusive to Hb9+ (superior-coding) DSGCs: GFP+ cells are
  Neurobiotin-coupled to **7.4 +/- 0.7** neighbours (n = 5/5), while GFP- DSGCs (4 inferior, 2
  anterior, 11 posterior) show no tracer or feedback-spikelet coupling (n = 0/17).
* Voltage-clamp at +40 mV in Hb9+ DSGCs evokes inward gap-junction-mediated spikelets of **21 +/- 2
  pA** (n = 6) that disappear under 1 uM TTX or 25 uM 18-beta-GA; spikelets peak **0.44 +/- 0.04
  ms** after the prejunctional spike (n = 10 pairs).
* Coupling between paired Hb9+ DSGCs is **symmetric along the preferred-null axis** (CC = **0.14 +/-
  0.01** preferred-to-null vs **0.13 +/- 0.01** null-to-preferred; n = 11 pairs; preferred-vs-null
  regression slope **0.94 +/- 0.07**) and the inferred gap-junction conductance is **~1 nS** (~1
  GOhm resistance).
* Gap junctions act as **low-pass filters** with corner frequency **~10 Hz**; 200 pA current
  injection drives an **84 +/- 4 Hz** spike train and **13 +/- 1 mV** plateau in the donor but only
  **0.5-2 mV** spikelets in the acceptor (n = 12 cells from 6 pairs).
* Hb9+ DSGCs have a large subthreshold excitatory receptive field of **36,183 +/- 3,350 um^2** (n =
  6\) extending 50-100 um beyond the classical receptive field, vs **17,986 +/- 2,594 um^2** for
  uncoupled DSGCs (n = 5; **p = 0.002**).
* Under physiological motion, coupled DSGC spiking begins **100 +/- 25 um outside** the classical
  receptive field (n = 6) vs **10 +/- 5 um inside** for uncoupled cells (n = 7); 18-beta-GA delays
  the onset by **97 +/- 10 um** (n = 7) while only mildly reducing the peak rate (**21 +/- 7%**).
* Skew indices for 600 um/s preferred-direction bars: **SI = 1.6 +/- 0.1** for coupled (n = 25) vs
  **1.1 +/- 0.1** for uncoupled (n = 8; **p = 0.009**); 18-beta-GA reduces coupled SI to **0.7 +/-
  0.1** (n = 7; **p = 0.001**).
* Inhibitory receptive fields are spatially offset from excitatory ones by **52 +/- 9 um** toward
  null (n = 5; **p = 0.008**); blocking GABA-A with picrotoxin raises preferred-direction peak rate
  from **198 +/- 14 Hz** to **244 +/- 18 Hz** (n = 6; **p = 0.03**), and null-direction peak from
  **27 +/- 12 Hz** to **202 +/- 14 Hz** (n = 4; **p = 0.001**); skew survives (SI **2.3 +/- 0.3**
  preferred, **3.1 +/- 0.5** null in picrotoxin).
* Excitatory current at half-maximum spike rate is **88 +/- 22 pA** during the rising phase vs **193
  +/- 36 pA** during the falling phase (n = 7; **p = 0.029**) - gain control raises the apparent
  spike threshold during the response.
* A preconditioning spike train (200 pA, 500 ms, ~85 Hz) applied before stimulus onset reduces
  initial-300-ms spike count by **70 +/- 6%** (n = 6) and reduces SI from **1.71 +/- 0.35** to
  **1.05 +/- 0.12** (**p < 0.05**); attenuation recovers with **tau = 604 +/- 158 ms**.

## Innovations

### Identification of the Sole Strongly Coupled DSGC Subtype in Mouse

By combining Hb9::eGFP genetic labelling with Neurobiotin tracer coupling and feedback-spikelet
analysis in voltage-clamp, the paper resolves a long-standing ambiguity in mouse retina: only the
superior-coding Hb9+ ON-OFF DSGC population is strongly electrically coupled. Other ON-OFF DSGC
subtypes (inferior, anterior, posterior coding) show no detectable functional coupling. This
provides a clean genetic handle for dissecting the function of dendrodendritic gap junctions between
ganglion cells.

### Quantification of a Subthreshold Excitatory Surround from Gap Junctions

Whole-cell patch reveals that the classical (spike-mapped) receptive field misses a real, ~50-100 um
wide ring of subthreshold excitatory drive around each coupled DSGC, contributed by 7-8 coupled
neighbours. Spike-only mapping had hidden this surround in earlier studies. The result reframes DSGC
receptive fields as centre + subthreshold surround rather than the textbook centre-surround
antagonism, with implications for spatiotemporal models of ganglion-cell firing.

### Functional Rectification Without Connexin Rectification

The paper resolves an apparent paradox: skewed responses look like rectified gap junctions, yet the
gap-junction conductance itself is electrically symmetric and non-inactivating. The authors show
that the rectification is *functional*, produced postsynaptically by (a) offset starburst- amacrine
GABAergic inhibition and (b) activity-dependent intrinsic gain control that raises the apparent
spike threshold during a spike train. The intrinsic mechanism (proposed to involve Na- channel slow
inactivation and Ca-activated K+ build-up, with tau ~600 ms) dominates: response skew survives
picrotoxin in both preferred and null directions.

### Peak Versus Mean Firing Rate Distinction for Mouse Hb9::eGFP DSGCs

This paper is the canonical source of **peak** firing rates for mouse Hb9+ DSGCs in standard
moving-bar protocols. Reported peak preferred-direction rates of **198 +/- 14 Hz** (control) and
**244 +/- 18 Hz** (picrotoxin), with peak null rates of **27 +/- 12 Hz** (control) and **202 +/- 14
Hz** (picrotoxin), are substantially higher than the trial-averaged mean rates (~10 Hz preferred)
reported elsewhere (e.g., Rivlin-Etzion et al. 2012). This distinction is essential for any
modelling work that fits biological firing rates: "peak instantaneous rate from a Gaussian-convolved
spike train" and "trial-averaged firing rate" are not interchangeable targets.

## Datasets

This is an experimental electrophysiology paper; no machine-learning datasets are released. The
biological "dataset" is whole-mount mouse retina recordings:

* **Animals**: adult wild-type C57BL/6 and Hb9::eGFP transgenic mice of both sexes, maintained on
  12-h light/dark cycles. Available from the authors and standard transgenic repositories (Hb9::eGFP
  characterised in Trenholm et al., 2011).
* **Cells recorded**: ~20 GFP+ Hb9 DSGCs and 17 GFP- DSGCs (4 inferior, 2 anterior, 11 posterior
  coding) for tracer-coupling and feedback-spikelet experiments; 11+ paired recordings of coupled
  Hb9+ neighbours; 6+ paired recordings under picrotoxin; 7 cells for gain-control experiments.
* No raw electrophysiology trace dataset is publicly archived; results are reported as per-cell
  summary statistics in figures and text.
* Stimulus parameters are fully specified (300 x 300 um bars, 96% Weber contrast, 600 um/s, eight
  directions, 40 um spot mapping at 1 s flashes) and are sufficient to reproduce the protocol in a
  model.

## Main Ideas

* The mouse Hb9::eGFP DSGC peak preferred-direction firing rate is **~198 Hz** in control and **~244
  Hz** in picrotoxin; the peak null rate is **~27 Hz** control and **~202 Hz** picrotoxin. Any
  project that quotes "30-80 Hz" for these cells almost certainly refers to mean (trial- or
  time-averaged) rates, not peak instantaneous rates from Gaussian-convolved spike trains. The
  project should explicitly distinguish these two metrics in fitting targets and reports.
* The DSI computed from peak rates is **(198 - 27) / (198 + 27) = 0.76**, matching the value often
  quoted for picrotoxin-treated Hb9 DSGCs; this is a peak-rate DSI, not a mean-rate DSI.
* Gap junction coupling alone is **insufficient** to drive postsynaptic spikes; gap junctions
  contribute by lowering the effective contrast threshold of *coincident* chemical synaptic input.
  Models that treat lateral electrical coupling as a passive linear summation will overestimate
  coupling-driven firing.
* Apparent rectification of lateral signals is **post-synaptic, not synaptic**. In a compartmental
  model, asymmetric (rising-vs-falling) responsiveness to identical synaptic input must come from
  intrinsic gain-control conductances (Na-channel slow inactivation, Ca-activated K+) and from
  spatially offset GABA, not from biased gap-junction conductances.
* The intrinsic gain-control timescale is **tau ~604 ms**, i.e. several hundred ms of post-burst
  attenuation. Models targeting realistic Hb9+ DSGC behaviour should include a slow recovery process
  at this timescale (slow Na inactivation or Ca-activated K) rather than only fast spike AHP.
* GABAergic inhibition onto DSGCs is **spatially offset by ~52 um toward null**, with reversal near
  **-60 mV**; in a model this becomes a starburst-amacrine input that arrives later and from a
  null-side spatial offset relative to the excitatory input.

## Summary

This paper asks how a network of mouse retinal direction-selective ganglion cells (DSGCs) combines
weak electrical coupling, chemical synapses, and intrinsic membrane properties to produce
direction-tuned, anticipatory responses without runaway excitation. The motivation is that earlier
work (Trenholm et al. 2013, Nat. Neurosci.) had shown that the same Hb9::eGFP-labelled superior-
coding DSGCs perform "lag normalisation" - they detect a moving edge at the same retinal location
regardless of speed - but the mechanistic basis for the asymmetric, leading-edge-skewed response
underlying that computation was unknown.

The methodology pairs Neurobiotin tracer-coupling, two-photon-targeted whole-cell and cell-attached
patch-clamp from single and paired DSGCs, voltage- and current-clamp characterisation of gap
junctions (TTX, 18-beta-glycyrrhetinic acid), receptive-field mapping with stationary spots and
moving bars, and pharmacological dissection of GABAergic inhibition with picrotoxin and intrinsic
gain control with preconditioning current pulses. The key design choice is to distinguish three
mutually exclusive explanations for response skew - gap-junction rectification, GABAergic
inhibition, intrinsic gain control - and test each independently.

The headline findings are: (i) only Hb9+ (superior-coding) DSGCs are strongly coupled, with ~1 nS
symmetric reciprocal gap junctions and ~10 Hz low-pass filtering; (ii) gap junctions provide a
~50-100 um subthreshold excitatory surround that primes coincident chemical synaptic input,
extending the effective receptive field and producing leading-edge-skewed motion responses (SI **1.6
+/- 0.1** vs **1.1 +/- 0.1** in uncoupled cells); (iii) the leading-edge skew survives picrotoxin in
both preferred and null directions, ruling out GABA as the sole cause; (iv) preconditioning spike
trains attenuate initial-response spikes by **70 +/- 6%** and abolish skew, with **tau ~604 ms**
recovery, implicating activity-dependent intrinsic gain control as the dominant rectifying
mechanism. Reported peak rates are **198 +/- 14 Hz** (preferred, control), **27 +/- 12 Hz** (null,
control), and **244 +/- 18 Hz** / **202 +/- 14 Hz** under picrotoxin.

For this project, the paper is a primary literature anchor for the firing-rate target of Hb9::eGFP
mouse DSGCs and clarifies a critical interpretation issue: the project domain-knowledge "30-80 Hz"
preferred-direction figure most likely originates from mean / trial-averaged rates (consistent with
Rivlin-Etzion et al. 2012's ~10 Hz), whereas this paper's 198 Hz preferred and 27 Hz null are peak
rates from Gaussian-convolved spike trains, and the corresponding peak-rate DSI is 0.76. The MOBO
objective for the AIS-tiered AHP task should explicitly state which metric (peak vs mean) it targets
to avoid mixing scales. The paper also constrains AIS / soma model choices: a realistic Hb9 DSGC
model needs slow (~600 ms) intrinsic gain control (Na slow inactivation or Ca-activated K),
spatially offset GABA inhibition (~52 um null-side, E_GABA near -60 mV), and weak symmetric
reciprocal gap-junction coupling - all properties that bias which ion-channel parameter sets and AHP
regimes can simultaneously hit the peak-rate target and the DSI target.
