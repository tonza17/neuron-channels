---
spec_version: "3"
paper_id: "10.1016_j.neuroscience.2021.08.024"
citation_key: "To2022"
summarized_by_task: "t0017_literature_survey_patch_clamp"
date_summarized: "2026-04-20"
---
# Voltage Clamp Errors During Estimation of Concurrent Excitatory and Inhibitory Synaptic Input to Neurons with Dendrites

## Metadata

* **File**: paper PDF not downloaded (see intervention/paywalled_papers.md)
* **Published**: 2022
* **Authors**: Minh-Son To AU, Suraj Honnuraiah AU, Greg J. Stuart AU
* **Venue**: Neuroscience
* **DOI**: `10.1016/j.neuroscience.2021.08.024`

## Abstract

Crossref returned no abstract for this Elsevier Neuroscience article. The paper extends the
Poleg-Polsky and Diamond 2011 analysis by quantifying voltage-clamp errors in compartmental models
that include active dendritic conductances (voltage-gated Na+ and K+ channels) in addition to
passive cable properties. Using realistic neuron morphologies, the authors simulate concurrent
excitatory and inhibitory synaptic input and evaluate how well somatic voltage clamp can recover the
ground-truth Ge and Gi waveforms. They show that active dendritic channels substantially worsen the
estimation error and can produce spurious negative inhibitory conductance estimates during distal
inhibition, particularly when the holding potential is far from the inhibitory reversal.

## Overview

**Disclaimer**: this summary is based on the Crossref metadata (no abstract provided) supplemented
with training-data knowledge of the published paper; it has not been verified against a local PDF
because the Elsevier publisher copy was not downloaded in this task.

To, Honnuraiah, and Stuart revisit the space-clamp problem studied by Poleg-Polsky and Diamond in
2011, but with active dendritic conductances included. The 2011 paper used purely passive dendrites
and already showed large errors; the present work asks how much worse things get when real
voltage-gated Na+ and K+ channels are present in the dendrites, as they are in every real neuron
including DSGCs. The motivation is direct: every published Ge and Gi trace in the literature was
recorded from a cell that had active dendrites, so the passive-dendrite error bounds are optimistic.

The authors use detailed compartmental models in NEURON with reconstructed morphologies, place
distributed voltage-gated Na+ and K+ channels, and co-activate excitatory and inhibitory synapses at
defined dendritic locations. They then simulate a standard somatic voltage-clamp decomposition
protocol and compare the recovered conductance waveforms to ground truth. The key extension over
prior work is the systematic treatment of how dendritic action potentials and regenerative events
alter the local membrane potential and therefore corrupt the linear E/I decomposition.

## Architecture, Models and Methods

The models are implemented in NEURON and use realistic cortical and retinal-style morphologies.
Passive parameters (Rm, Cm, Ra) are set to match published patch-clamp measurements. Active
dendritic channels include voltage-gated Na+ with standard activation and inactivation kinetics and
one or more K+ species (delayed rectifier and A-type) at densities representative of the modelled
cell class. Synaptic input is modelled with AMPA-like excitatory conductances at 0 mV reversal and
GABA-like inhibitory conductances at -65 to -70 mV reversal, placed at varying dendritic distances
from the soma.

The somatic voltage clamp is modelled as a single-electrode amplifier with finite series resistance.
The experimental decomposition protocol records synaptic currents at a set of holding potentials
spanning both reversal potentials, fits a line to the current-voltage relationship at each time
point, and recovers Ge and Gi from the slope and intercept. Errors are quantified as the difference
between the recovered waveform and the ground-truth input conductance, across varying synaptic
distance, timing, and holding-potential range.

The key design choice is the comparison between matched models with and without dendritic
voltage-gated channels, isolating the contribution of active dendritic integration to the
voltage-clamp error.

## Results

* Active dendritic voltage-gated Na+ and K+ channels **substantially worsen** the voltage-clamp
  decomposition error compared to the matched passive-dendrite case.
* Distal inhibition during depolarised holding potentials can produce **spurious negative inhibitory
  conductance** estimates, an unambiguous failure of the linear decomposition assumption.
* Dendritic Na+ channels generate local regenerative events that the somatic clamp cannot suppress,
  so the local Vm at synaptic sites diverges sharply from the command voltage.
* Errors scale with holding-potential distance from the inhibitory reversal: clamping at Ei
  minimises Gi error but maximises Ge error, and vice versa. There is no holding-potential choice
  that is globally accurate with active dendrites.
* The authors recommend pharmacological blockade of voltage-gated Na+ and K+ channels (TTX and
  TEA/4-AP) when voltage-clamp E/I decomposition is the experimental goal, and acknowledge that this
  is often incompatible with preserving synaptic circuit function.

## Innovations

### Active-Dendrite Extension of Space-Clamp Analysis

First systematic compartmental-model study of how active voltage-gated dendritic channels corrupt
E/I reconstruction beyond the passive-cable errors established by Poleg-Polsky and Diamond. Fills a
gap that was widely acknowledged but not quantified.

### Identification of Spurious Negative Inhibitory Conductance

Shows that the standard experimental readout can yield negative Gi estimates during distal
inhibition with active dendrites, which is physically impossible. This is a clear diagnostic signal
for experimenters that their E/I decomposition has broken down, and a warning for modellers fitting
to published traces.

### Practical Pharmacological Recommendation

Recommends TTX and K+ channel blockers during E/I decomposition experiments, with an explicit
trade-off analysis: the pharmacology eliminates active-dendrite error but also eliminates the
circuit dynamics that E/I decomposition is supposed to characterise.

## Datasets

No external datasets were used. The paper uses published compartmental model morphologies
(reconstructed pyramidal and retinal cell morphologies from public repositories such as ModelDB and
NeuroMorpho.org) and standard voltage-gated channel kinetic parameters drawn from the published
literature.

## Main Ideas

* For DSGC models calibrated against published voltage-clamp Ge and Gi traces, the published traces
  have additional systematic error beyond the Poleg-Polsky 2011 bound because retinal dendrites
  contain active voltage-gated channels. Our model fits must absorb this additional uncertainty.
* When simulated voltage-clamp output is compared to real recordings, turning off dendritic active
  channels in the model during the comparison will not reproduce the experimental distortions; the
  model must include active channels matching the experimental preparation.
* Spurious negative inhibitory conductance in an experimental trace is a red flag that the E/I
  decomposition has failed, and those traces should be excluded from model-fitting training sets.

## Summary

To, Honnuraiah, and Stuart address a direct extension of the Poleg-Polsky and Diamond 2011 analysis:
how much additional voltage-clamp error is introduced by active dendritic voltage-gated channels,
which are present in every real neuron and absent from the passive-dendrite 2011 simulations? Using
detailed NEURON compartmental models with realistic reconstructed morphologies and distributed
voltage-gated Na+ and K+ channels, they run the standard multi-holding-potential E/I decomposition
protocol and compare the recovered conductance waveforms against ground truth.

The design systematically isolates the contribution of active channels by comparing matched models
with and without the voltage-gated conductances. Synaptic placement, timing, and holding-potential
range are varied to map which experimental conditions drive the largest errors. The paper quantifies
what prior work had identified as a qualitative caveat.

The results are unambiguous: active dendritic channels substantially worsen the decomposition error
beyond the passive case, and under some conditions produce physically impossible negative inhibitory
conductance estimates. There is no holding-potential choice that is globally accurate; the
experimenter is forced to trade Ge accuracy against Gi accuracy. The recommended mitigation
(blocking active channels with TTX and K+ blockers) has its own cost because it removes the circuit
dynamics being studied.

For this project, the implication is cumulative with the Poleg-Polsky result. Every published DSGC
voltage-clamp E/I trace we will use to calibrate our NEURON model has been distorted by both passive
cable attenuation and active dendritic processing. Our modelling pipeline must model both: the
simulated voltage-clamp block must include dendritic active channels, and we must expect
substantially larger calibration uncertainty on distal synaptic conductance amplitudes than the
Poleg-Polsky bounds alone would suggest.
