---
spec_version: "3"
paper_id: "10.1113_JP286581"
citation_key: "Ankri2024"
summarized_by_task: "t0091_morphology_extended_nsga2_v1"
date_summarized: "2026-05-08"
---
# A new role for excitation in the retinal direction-selective circuit

## Metadata

* **File**: `files/ankri_2024_dsgc-light-adaptation-surround.pdf`
* **Published**: 2024-10-27 (online), Vol 602.22, pages 6301-6328
* **Authors**: Lea Ankri 🇮🇱, Serena Riccitelli 🇮🇱, Michal Rivlin-Etzion 🇮🇱
* **Venue**: The Journal of Physiology (Wiley, on behalf of The Physiological Society)
* **DOI**: `10.1113/JP286581`

## Abstract

A key feature of the receptive field of neurons in the visual system is their centre-surround
antagonism, whereby the centre and the surround exhibit responses of opposite polarity. This
organization is thought to enhance visual acuity, but whether and how such antagonism plays a role
in more complex processing remains poorly understood. Here, we investigate the role of centre and
surround receptive fields in retinal direction selectivity by exposing posterior-preferring On-Off
direction-selective ganglion cells (pDSGCs) to adaptive light and recording their response to
globally moving objects. We reveal that light adaptation leads to surround expansion in pDSGCs. The
pDSGCs maintain their original directional tuning in the centre receptive field, but present the
oppositely tuned response in their surround. Notably, although inhibition is the main substrate for
retinal direction selectivity, we found that following light adaptation, both the centre- and
surround-mediated responses originate from directionally tuned excitatory inputs. Multi-electrode
array recordings show similar oppositely tuned responses in other DSGC subtypes. Together, these
data attribute a new role for excitation in the direction-selective circuit. This excitation carries
an antagonistic centre-surround property, possibly designed to sharpen the detection of motion
direction in the retina.

## Overview

Ankri and colleagues investigate how the receptive-field organisation of posterior-preferring On-Off
direction-selective ganglion cells (pDSGCs) reorganises under prolonged photopic illumination, a
regime they call "light-adapted". The classical retinal DS account (Briggman 2011, Wei 2011,
Yonehara 2011, and Ankri's own 2020 work) attributes direction selectivity almost entirely to
asymmetric inhibition from starburst amacrine cells (SACs); excitation has historically been
considered either non-directional or, when it appears directional, an artefact of imperfect
voltage-clamp space-clamp. The paper challenges that view by showing that light adaptation unmasks a
strong directionally tuned excitatory drive that survives any plausible space-clamp critique.

The authors combine two-photon-targeted patch-clamp recordings (Drd4-EGFP and Trhr-EGFP mice) with
252-electrode multi-electrode-array (MEA) recordings in C57BL/6 mice. They first demonstrate that
photopic adaptation expands the pDSGC receptive field asymmetrically toward the preferred side
(asymmetry index On = 0.44, Off = 0.15). They then show that this expanded surround generates a
delayed null-direction-tuned spiking phase that is absent before adaptation. Voltage-clamp
recordings reveal that the centre response is driven by preferred-direction-tuned excitation, and
the surround-driven delayed phase is driven by null-direction-tuned excitation; inhibition becomes
roughly symmetric in both regions after adaptation. Pharmacology with SR95531, strychnine, and L-AP4
dissects which inputs gate the new excitatory phase: GABA-A blockade unmasks non-directional
surround activity, glycinergic blockade abolishes surround excitation, and L-AP4 shows the On
pathway is the dominant carrier. The MEA data generalise the null-tuned delayed phase to other DSGC
subtypes (anterior, dorsal, ventral). The paper closes by linking these findings to the
visual-cortex extraclassical antagonistic surround literature (Keller 2020), proposing that the
centre/surround opposite-polarity directional code is a general motif for sharpening motion
discrimination.

## Architecture, Models and Methods

This is an experimental electrophysiology paper, not a computational study. The methodology covers
four pillars:

* **Animals**: Drd4-EGFP and Trhr-EGFP transgenic mice (4-12 weeks, either sex) labelled GFP in
  pDSGCs for two-photon-targeted patch recording. Wild-type C57BL/6JOlaHsd mice were used for the
  MEA experiments.

* **Two-photon-targeted patch-clamp**: Retinas were dark-adapted for 30+ min, dissected under dim
  red/infrared light, and perfused with carbogen-equilibrated Ames medium at 32-34 degrees C.
  GFP-positive pDSGCs were targeted at 920 nm. Loose-patch spike recordings used 4-7 MOhm pipettes
  filled with Ames; voltage-clamp whole-cell recordings used 5-9 MOhm pipettes with
  Cs-methanesulfonate-based intracellular solution (110 CsMeSO3, 4 EGTA, 5 TEA-Cl, 4 Mg-ATP,
  Na-phosphocreatine; pH 7.2; ECl = -73 mV). Excitation was isolated at 0 mV holding (after
  liquid-junction-potential correction) and inhibition at -60 mV. Data were filtered at 2 kHz and
  sampled at 10 kHz on a MultiClamp 700B with Digidata 1550 and pCLAMP10.

* **Multi-electrode array**: 252-electrode MEAs (MultiChannel Systems, 100 or 200 micrometre pitch),
  retina mounted ganglion-side-down on PDL-coated arrays, perfusion at 33.2 degrees C, 3.5 ml/min.
  Signals digitised at 20 kHz; spike sorting with Kilosort2.0 + manual curation in Phy
  (refractory-period violations < 1%).

* **Visual stimuli and adaptation protocols**: Two adaptation regimes were used: 3.0-5.5 min of
  stationary photopic full-field illumination, and 3.0-5.5 min of repetitive visual stimulation
  (RVS) with drifting gratings. Direction tuning was probed with bars travelling about 1 mm across
  the retina (sequentially activating centre and surround), and receptive-field structure with
  concentric spot stimuli of increasing radius. The asymmetry index (AI) was defined as a normalised
  weighted sum of preferred-side minus null-side responses across radii. Pharmacology used SR95531
  (50 micromolar; GABA-A block), strychnine (1 micromolar; glycine block), and L-AP4 (20 micromolar;
  mGluR6/On-pathway block). Statistics: chi-square goodness-of-fit for normality, then paired
  Student's t test or non-parametric equivalents; significance reported as *P* < 0.05, **P* < 0.01,
  ***P* < 0.001.

Sample sizes vary per figure: receptive-field expansion analysis used n = 10 cells before adaptation
and n = 16 after stationary light; baseline DSI distribution n = 38 cells.

## Results

* **Receptive field asymmetry**: Light adaptation expanded the pDSGC receptive field asymmetrically
  toward the preferred side. Asymmetry index for the On RF reached **0.44** versus **0.15** for the
  Off RF, with significant changes both for On (P-On = **0.002**) and Off (P-Off = **0.0001**)
  responses across cells.
* **Sustained On response**: Spike-response duration to spots more than doubled - On-response
  duration before adaptation was **305.00 +/- 255.44 ms** vs. **779.33 +/- 149.21 ms** after (*P* =
  **1.96e-4**), indicating sensitisation rather than simple gain change.
* **Baseline directional tuning**: Before adaptation, both On and Off phases were strongly
  preferred-direction-tuned with **DSI-on = 0.7 +/- 0.25** and **DSI-off = 0.65 +/- 0.3** (mean +/-
  SD; n = 38 cells).
* **Null-tuned delayed phase**: Light adaptation introduced a new delayed spiking phase tuned to the
  null direction in addition to the preserved preferred-direction main phase, observed in pDSGCs and
  reproduced across anterior, dorsal, and ventral DSGCs in MEA recordings.
* **Excitation flips between centre and surround**: Voltage-clamp showed that after adaptation
  centre excitation is preferred-direction-tuned while surround excitation is null-direction- tuned;
  inhibition becomes essentially symmetric, removing it as the dominant directional substrate.
* **Pharmacological dissection**: GABA-A blockade (SR95531) unmasked non-directional surround
  activity, indicating GABAergic inhibition gates surround spatial extent; glycine blockade
  (strychnine) abolished the null-tuned delayed surround excitation; L-AP4 (On-pathway block)
  eliminated most of the RVS-induced On response, identifying the On pathway as the main carrier of
  the new null-tuned phase.
* **On/Off ratio shift**: Light adaptation reversed the On vs. Off response ratio (P-before-RVS =
  **0.01**, P-before-stationary = **0.01**), with the On phase becoming dominant where the Off phase
  had previously been equal or stronger.
* **Generality across subtypes**: MEA recordings demonstrated null-tuned delayed phases in all four
  cardinal On-Off DSGC subtypes, supporting that the phenomenon is a general motif rather than a
  pDSGC peculiarity.

## Innovations

### Light-Adaptation-Gated Excitatory Direction Code

First demonstration that a luminance-regime change can switch the dominant substrate for retinal DS
computation from inhibition (the Briggman/Wei/Yonehara model) to excitation, with
preferred-direction tuning in the centre and null-direction tuning in the surround. This challenges
the textbook account that DS in the retina is a stationary, inhibition-dominated computation.

### Centre-Surround Antagonism Implemented in the Excitatory Channel

The directional centre-surround antagonism is implemented within the excitatory channel itself, not
just between excitation and inhibition. The centre carries preferred-direction excitation, the
expanded surround carries null-direction excitation, and inhibition becomes a symmetric modulator.
This is a structurally new circuit architecture for direction selectivity.

### Glycinergic Gating of Surround Excitation

Pharmacology cleanly identifies glycinergic amacrine-cell inputs as the gatekeeper for the
surround-mediated null-tuned excitation, and GABAergic inputs as the gatekeeper for surround spatial
extent. This dissociation maps two distinct inhibitory pathways onto two distinct features of the
light-adapted response.

### MEA Generalisation Across All On-Off DSGC Subtypes

Multi-electrode-array recordings demonstrate that the null-tuned delayed spiking phase is not
specific to posterior-preferring DSGCs but is a feature of all four cardinal On-Off DSGC subtypes,
reframing the phenomenon as a fundamental retinal motif.

## Datasets

This is an experimental electrophysiology paper; no public computational datasets are released or
used. All data are first-party recordings from the authors' laboratory at the Weizmann Institute of
Science (Department of Brain Sciences, Rehovot, Israel). The supporting information section hosts
peer-review documents but no raw recordings. The paper does not announce a public data deposit.

For our project, the actionable "data" are the published mean +/- SD values for spike duration, DSI
distributions, asymmetry indices, and the qualitative signature of a null-tuned surround excitation
phase, all of which can be used as biological-plausibility ceilings for cells produced by the t0091
NSGA-II search.

## Main Ideas

* **The classical inhibition-dominated DS substrate that the project models is correct only under
  one luminance regime.** Light adaptation flips the surround tuning of pDSGCs and shifts the
  dominant directional substrate to excitation. Our compartmental model and 16-direction wave
  protocol target the photopic, non-light-adapted regime, so the Ankri 2024 phenomena do not
  invalidate the t0091 search but do impose a known scope limit on its biological-plausibility
  claims.
* **Directionally tuned excitation is real, not a space-clamp artefact.** The paper provides
  positive evidence (asymmetric On-only excitation before adaptation, asymmetric null-tuned
  excitation after) that cannot be explained by inhibitory current distortion. For our
  forward-modelling work this means that any future v4-substrate variant that adds directional bias
  to AMPA inputs has direct biological precedent rather than being a modelling shortcut.
* **DSI between 0.65 and 0.70 with substantial across-cell variability (SD = 0.25-0.30) is the
  empirical baseline tuning strength** for healthy DSGCs in dark-adapted photopic recording. Our
  optimisation targets above this band should be flagged as super-biological in the answer asset's
  biological-plausibility discussion.
* **A delayed null-tuned spiking phase is part of the natural pDSGC response under light
  adaptation** and is generated by surround excitation gated by glycinergic amacrine cells. This is
  a separate axis the t0091 substrate does not score against and should be acknowledged as an
  out-of-scope phenomenon for the current v3 substrate.

## Summary

Ankri, Riccitelli, and Rivlin-Etzion examine how prolonged photopic illumination reshapes the
receptive field and directional code of posterior-preferring On-Off direction-selective ganglion
cells (pDSGCs) in mouse retina. The standard textbook view, including the authors' own prior work,
attributes retinal direction selectivity to asymmetric inhibition from starburst amacrine cells,
with directional excitation either absent or attributed to space-clamp artefact. The authors set out
to test whether luminance-state changes that are known to remodel centre-surround antagonism (Ankri
2020, Farrow 2013, Nath 2023) also reorganise the directional code itself.

Methodologically the study combines two-photon-targeted loose-patch and whole-cell voltage-clamp
recordings from genetically labelled pDSGCs (Drd4-EGFP and Trhr-EGFP mice) with 252-electrode MEA
recordings from wild-type retinas. Direction tuning is probed with 1 mm bars that traverse the
centre and surround sequentially, and receptive-field structure with concentric spot stimuli. Two
adaptation protocols are used (3-5.5 min of stationary photopic light, or repetitive visual
stimulation with drifting gratings). Pharmacology with SR95531, strychnine, and L-AP4 dissects the
GABAergic, glycinergic, and On-pathway contributions to the unmasked surround excitation.

Light adaptation expands the pDSGC receptive field asymmetrically toward the preferred side
(asymmetry index On = **0.44** vs. Off = **0.15**), more than doubles the On spike-response duration
(**305 +/- 255 ms** -> **779 +/- 149 ms**, *P* = **1.96e-4**), and adds a delayed
null-direction-tuned spiking phase to the cell's normal preferred-direction main phase.
Voltage-clamp recordings show that the centre is driven by preferred-direction-tuned excitation
while the surround is driven by null-direction-tuned excitation; inhibition becomes essentially
symmetric. The phenomenon generalises across all four cardinal On-Off DSGC subtypes in the MEA data.

For this project the paper has two consequences. First, it confirms that the classical
inhibition-dominated DS substrate that t0091's compartmental model implements is the correct target
for a non-light-adapted photopic 16-direction protocol but is one regime among at least two; the
answer asset should explicitly scope its biological-plausibility ceiling claims to photopic,
non-light-adapted conditions and acknowledge that the surround-direction-flipping excitation is a
separate axis the v3 substrate does not score against. Second, the published **DSI-on = 0.70 +/-
0.25** and **DSI-off = 0.65 +/- 0.30** baseline values serve as a hard biological reference for
evaluating whether any t0091 Pareto cell that achieves extremely high DSI is super-biological rather
than realistic.
