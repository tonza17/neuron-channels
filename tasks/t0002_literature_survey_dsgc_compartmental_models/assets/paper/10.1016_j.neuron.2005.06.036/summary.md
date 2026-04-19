---
spec_version: "3"
paper_id: "10.1016_j.neuron.2005.06.036"
citation_key: "Oesch2005"
summarized_by_task: "t0002_literature_survey_dsgc_compartmental_models"
date_summarized: "2026-04-19"
---
# Direction-Selective Dendritic Action Potentials in Rabbit Retina

## Metadata

* **File**: `files/oesch_2005_ds-dendritic-aps.pdf`
* **Published**: 2005
* **Authors**: Nicholas Oesch 🇺🇸, Thomas Euler 🇩🇪, W. Rowland Taylor 🇺🇸
* **Venue**: Neuron, Vol. 47, pp. 739-750
* **DOI**: `10.1016/j.neuron.2005.06.036`

## Abstract

Dendritic spikes that propagate toward the soma are well documented, but their physiological role
remains uncertain. Our in vitro patch-clamp recordings and two-photon calcium imaging show that
direction-selective retinal ganglion cells (DSGCs) utilize orthograde dendritic spikes during
physiological activity. DSGCs signal the direction of image motion. Excitatory subthreshold
postsynaptic potentials are observed in DSGCs for motion in all directions and provide a weakly
tuned directional signal. However, spikes are generated over only a narrow range of motion angles,
indicating that spike generation greatly enhances directional tuning. Our results indicate that
spikes are initiated at multiple sites within the dendritic arbors of DSGCs and that each dendritic
spike initiates a somatic spike. We propose that dendritic spike failure, produced by local
inhibitory inputs, might be a critical factor that enhances directional tuning of somatic spikes.

## Overview

Oesch, Euler, and Taylor ask whether active dendritic conductances play a functional role in the
direction-selective computation of rabbit ON/OFF DSGCs. Prior work had shown that directional
selectivity is substantially presynaptic -- GABAergic starburst amacrine cells provide asymmetric
inhibition -- but it was unclear whether the DSGC itself contributes postsynaptic nonlinearities.
The key observation motivating the paper is that PSPs recorded at the soma are weakly directional
while the cell spike output is sharply directional, and the authors investigate what bridges this
gap.

The authors combine whole-cell patch-clamp with local TTX pressure-ejection and two-photon calcium
imaging to show that DSGCs generate TTX-sensitive dendritic Na+ spikes during physiological light
stimulation. When TTX is applied locally to the soma, large somatic spikes are replaced by smaller,
direction-tuned events (~7.4 mV) consistent with dendritic spikes that can no longer trigger the
full somatic action potential. Applying TTX to a dendritic segment suppresses calcium transients
locally while sparing distal sites, directly localising TTX-sensitive Na+ channel activation to
specific dendritic branches.

Two complementary findings establish that spike initiation does not occur at the soma during light
stimulation. First, injecting current at the soma with a waveform matched to the light-evoked PSP
produces far fewer spikes (11 +/- 9 vs. 59 +/- 21 spikes/stimulus) at lower rates (41 +/- 47 Hz vs.
148 +/- 30 Hz modal ISI rate), even when the injected current depolarises the soma slightly more.
Second, the distribution of light-evoked spike thresholds (peak at -56 mV, half-width ~8 mV) is
broadly distributed around the mean PSP amplitude, indicating that somatic membrane potential does
not predict spike occurrence -- a hallmark of remotely-initiated spikes from the dendrites.

The proposed mechanism is that GABAergic inputs from starburst amacrine cells, positioned between
excitatory spike initiation sites and the soma along the null-direction path, cause null-direction
dendritic spikes to fail before reaching the soma. Preferred-direction spikes escape this veto
because inhibition is distal to the excitation, not interposed along the propagation path. This
spatial arrangement also explains the non-directional zone on the preferred side of the receptive
field, where inhibition is not interposed between excitation and soma.

## Architecture, Models and Methods

**Tissue preparation.** Dark-adapted Dutch-belted rabbit retinas prepared as flat-mounts adhered
photoreceptor-side down to poly-L-lysine or Cell-Tak coverslips, perfused at ~4 ml/min with
oxygenated bicarbonate-buffered Ames medium at 34-36 degrees C (composition: 120 mM NaCl, 23 mM
NaHCO3, 3.1 mM KCl, 1.15 mM CaCl2, 1.24 mM MgCl2, pH 7.4).

**Electrophysiology.** Borosilicate patch electrodes (4-8 MOhm) used first for loose-patch
extracellular recording to confirm DSGC identity and determine preferred direction, then replaced
with a whole-cell intracellular electrode. Intracellular solution: 110 mM K-methylsulfonate, 10 mM
NaCl, 5 mM Na-HEPES, 1 mM K-EGTA, 1 mM Na-ATP, 0.1 mM Na-GTP. Signals filtered at 2 kHz (4-pole
Bessel), digitized at 5-10 kHz. Liquid junction potential of 10 mV subtracted from all voltages.
Bridge balance monitored during whole-cell recordings.

**Pharmacology.** Local TTX (0.2-1 uM in Ames medium) pressure-ejected from a second pipette
positioned ~10 um from the soma or a dendritic segment. Bath TTX applied at 0.5 uM. Intracellular
QX-314 (1-10 mM, lidocaine derivative) back-filled in the recording electrode, diffusing over 10-20
min to selectively block somatic sodium channels while sparing distal dendritic channels.

**Light stimulation.** Moving bar (250 um width, 800-1200 um/s on retina, 30%-100% Michelson
contrast) projected through a 20x 0.95 NA water-immersion objective via a CRT monitor (85 Hz
refresh) focused onto the photoreceptor outer segments. Stimuli presented in 12 directions evenly
spanning 360 degrees.

**Two-photon calcium imaging.** Cells loaded with Oregon Green BAPTA-1 (100-200 uM in pipette,
diffusion time 3-5 min). Custom upright multiphoton microscope with Ti:Sapphire laser (Mira-900,
Coherent) tuned to 920-930 nm. Image regions 64 x 8 pixels at 62.5 Hz or line scans 64 pixels at 500
Hz. Fluorescence delta-F/F computed after background subtraction. A separate visible-wavelength LCD
stimulus (30 Hz, ~2.1 um/pixel, band-pass filtered 578 BP 10 nm) focused ~100 um above the imaging
plane provided independent photoreceptor stimulation during imaging.

**Directional tuning analysis.** DSI computed as normalised resultant vector length from 12 polar
responses. Von Mises distributions fitted to polar tuning data. Spike threshold defined as the
membrane potential at the point where the second derivative of the voltage trace fell below -2x10^5
V/s^2.

**Sample sizes.** Core DSI comparison: n = 12 cells; input resistance / threshold experiments: n =
9-13 cells; local somatic TTX: n = 12 cells; local dendritic TTX: n = 4 cells; ISI refractory
analysis: n = 9 cells; hyperpolarisation experiments: n = 10 cells.

## Results

* Spike DSI: **0.67 +/- 0.13** (ON) and **0.74 +/- 0.13** (OFF) in current-clamp; extracellular
  spike DSI in the same 12 cells: **0.53 +/- 0.13** and **0.64 +/- 0.12**.
* PSP DSI (spike-blanked): only **0.09 +/- 0.05** (ON) and **0.14 +/- 0.08** (OFF), approximately
  **6-fold lower** than the corresponding spike DSI.
* PSP amplitude difference (preferred vs. null): mean **3.7 +/- 1.7 mV** (ON) and **3.8 +/- 3.0 mV**
  (OFF), ranging 0-10.1 mV across cells.
* ON vs. OFF preferred direction alignment: **12 +/- 9 degrees** for spikes vs. **38 +/- 52
  degrees** for PSPs, confirming spike generation sharpens the common directional axis.
* Local somatic TTX: two discrete spike-amplitude populations at **7.4 +/- 1.9 mV** (dendritic) and
  **54.8 +/- 3.5 mV** (somatic); dendritic spike DSI matched somatic spike DSI (e.g., preferred
  directions 96 vs. 98 degrees, DSIs 0.56 vs. 0.62 in one representative cell).
* Light-evoked PSPs: peaked at **-59.1 +/- 1.5 mV** (11.6 +/- 1.5 mV depolarisation); generated **59
  +/- 21 spikes/stimulus** at modal ISI rate **148 +/- 30 Hz**.
* Equivalent somatic current-injected PSPs (reaching -56.8 +/- 1.3 mV, 2.3 mV more depolarised):
  only **11 +/- 9 spikes/stimulus** at **41 +/- 47 Hz** (p < 0.001, paired t-test).
* Somatic spike threshold during light stimulation: peak at **-56 mV**, half-width ~8 mV (2117
  spikes); during somatic current injection: peak at **-49 mV**, half-width ~4 mV (1233 spikes).
* Resting membrane potential: **-70.7 +/- 1.6 mV**; input resistance: **82.0 +/- 20.6 MOhm**; spike
  frequency vs. injected current slope: **0.31 +/- 0.18 Hz/pA**.
* Somatic absolute refractory period: **3.5 +/- 0.7 ms**; dendritic spikes showed superposition with
  no measurable absolute refractory period, consistent with multiple independent initiation sites
  across the arbor.
* Local dendritic TTX blocked calcium transients at the application site but not at distal sites,
  directly demonstrating TTX-sensitive Na+ channel activation in specific dendritic branches.
* Bath TTX (0.5 uM) completely abolished all spiking and all calcium transients; PSP-level
  depolarisation alone was insufficient to activate dendritic calcium channels.

## Innovations

### First Demonstration of Physiologically Evoked Dendritic Spikes in DSGCs

Prior work (Velte and Masland, 1999) showed dendritic spikes in alpha-ganglion cells only upon
direct current injection. Oesch et al. are the first to demonstrate dendritic spikes arising during
natural light-stimulated activity in a functionally characterised ganglion cell class, establishing
that active dendritic conductances are engaged under physiological conditions in DSGCs.

### Dendritic Spike Initiation as the Primary Source of Sharp Directional Tuning

The ~6-fold enhancement of DSI from PSPs to spikes is the core quantitative finding. The paper shows
that this amplification requires TTX-sensitive Na+ channels, placing active dendritic computation --
not just presynaptic starburst amacrine circuitry -- as a necessary contributor to directional
selectivity in DSGC spike output.

### Dendritic Spike Failure as a Spatial Veto Mechanism

The authors propose that GABAergic inhibitory inputs interposed along the null-direction propagation
path cause dendritic spikes to fail before reaching the soma. This does not require close apposition
of inhibitory and excitatory synapses (resolving a conflict with Jeon et al., 2002) and elegantly
accounts for the nondirectional zone on the preferred side of the receptive field.

### Two-Photon Imaging Combined with Local Pharmacology for Dendritic Excitability Mapping

Local TTX application paired with simultaneous calcium imaging in live intact retinal tissue allows
direct spatial localisation of dendritic spike initiation and backpropagation within identified
arbors, establishing a methodological paradigm for functional imaging of retinal ganglion cell
dendrites.

## Datasets

The paper uses acutely prepared flat-mounted rabbit retina from Dutch-belted rabbits. No dataset is
publicly deposited. Key experimental samples:

* Current-clamp DSI comparison: n = 12 DSGCs
* Local somatic TTX experiments: n = 12 cells
* Local dendritic TTX: n = 4 cells
* Hyperpolarisation and ISI experiments: n = 9-10 cells
* Calcium imaging: subset of cells loaded with Oregon Green BAPTA-1 (100-200 uM pipette)

All experiments conducted in vitro in flat-mounted rabbit retina. One figure in Supplemental Data
(QX-314 blocking experiment). No code or raw data repository is associated with this publication.

## Main Ideas

* Any compartmental DSGC model with passive dendrites will underestimate directional selectivity by
  ~6-fold; distributed dendritic Na+ conductances capable of generating local spikes are required to
  match the measured spike DSI of **0.67-0.74**.
* The null-direction inhibitory input geometry is a critical model constraint: GABAergic inputs must
  be positioned between excitatory spike initiation sites and the soma along the null-direction
  propagation path -- not merely co-localised with excitation -- to produce null-direction spike
  failure.
* Spikes are initiated at multiple independent sites across both ON and OFF dendritic arbors
  (non-refractory superposition); compartmental models need at least separate ON and OFF subarbors
  with independent dendritic spike initiation capability.
* The preferred-direction modal spike rate of **~148 Hz** vs. **~41 Hz** for equivalent somatic
  current injection is a quantitative benchmark: optimised Na/K conductance combinations should
  reproduce this ~3.6-fold amplification of spike rate contributed by the dendritic tree.
* All active spiking (somatic and dendritic) is TTX-sensitive; dendritic Na+ conductances in the
  model should be implemented as standard fast Hodgkin-Huxley-type Na+ channels, not slower
  persistent or Ca2+ spike conductances.

## Summary

Oesch, Euler, and Taylor address a fundamental question about rabbit direction-selective retinal
ganglion cells: does the DSGC itself perform active postsynaptic dendritic computation amplifying
directional selectivity, or is tuning entirely presynaptic? The motivation is a conspicuous mismatch
-- somatic PSPs have a DSI of only ~0.09-0.14, while spike output has a DSI of ~0.67-0.74, a ~6-fold
discrepancy that passive membrane integration cannot explain.

The study uses in vitro whole-cell patch-clamp recordings of rabbit DSGCs combined with local
pressure-application of TTX or intracellular QX-314 (selectively blocking somatic vs. dendritic
sodium channels) and two-photon calcium imaging (spatially localising spike initiation and
propagation within identified dendritic arbors). These converging methods show that DSGCs generate
TTX-sensitive Na+ spikes at multiple sites within their dendritic arbors during light stimulation,
that each dendritic spike reliably triggers a somatic spike, and that somatic membrane potential is
a poor predictor of spike initiation during light responses -- confirming the driving force
originates in the dendrites.

The key quantitative results are: spike DSI is ~6-fold greater than PSP DSI; local somatic TTX
reveals direction-tuned dendritic spikes at ~7.4 mV amplitude; local dendritic TTX suppresses spikes
globally; calcium transients require active Na+ spikes (PSP depolarisation alone is insufficient);
dendritic spikes show no absolute refractory period (superposition), consistent with multiple
independent initiation sites; and light-evoked preferred-direction stimulation generates **59 +/- 21
spikes/stimulus** at **148 +/- 30 Hz** while equivalent somatic current injection generates only
**11 +/- 9 spikes** at **41 +/- 47 Hz** (p < 0.001). The authors propose that null-direction
GABAergic inhibition, spatially interposed between excitatory inputs and the soma along the
dendritic propagation path, vetoes null-direction dendritic spike propagation.

For this project, the paper establishes three non-negotiable constraints on the compartmental DSGC
model. First, passive dendrites are insufficient: distributed dendritic Na+ conductances must be
present and capable of generating local spikes, or the model will underestimate directional
selectivity by ~6-fold. Second, the null-direction GABAergic input geometry must implement a spatial
veto with inhibition positioned along the dendritic propagation path toward the soma, not merely
co-localised with excitation. Third, the optimisation target should include the ~6-fold PSP-to-spike
DSI amplification and the modal preferred-direction spike rate of ~148 Hz as primary quantitative
benchmarks, alongside the target angle-to-AP-frequency tuning curve.
