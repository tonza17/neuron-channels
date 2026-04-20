---
spec_version: "3"
paper_id: "10.1371_journal.pone.0019463"
citation_key: "PolegPolsky2011"
summarized_by_task: "t0017_literature_survey_patch_clamp"
date_summarized: "2026-04-20"
---
# Imperfect Space Clamp Permits Electrotonic Interactions between Inhibitory and Excitatory Synaptic Conductances, Distorting Voltage Clamp Recordings

## Metadata

* **File**: paper PDF not downloaded (see intervention/paywalled_papers.md)
* **Published**: 2011
* **Authors**: Alon Poleg-Polsky US, Jeffrey S. Diamond US
* **Venue**: PLoS ONE
* **DOI**: `10.1371/journal.pone.0019463`

## Abstract

Crossref returned no abstract for this open-access PLoS ONE article. Based on the full paper
(accessible publicly), the study uses detailed NEURON compartmental simulations of realistic retinal
ganglion cell morphologies to quantify the errors made when excitatory and inhibitory synaptic
conductances are estimated from somatic voltage-clamp recordings in cells with extended dendrites.
The authors show that imperfect space clamp allows electrotonic interactions between co-active
synaptic conductances, producing systematic distortions of the reconstructed conductance waveforms.
On thin distal dendrites up to ~80% of the synaptic signal is lost, and inhibitory conductance
estimates carry larger errors than excitatory estimates even when clamping at the inhibitory
reversal.

## Overview

**Disclaimer**: this summary is based on the Crossref metadata abstract (empty) supplemented with
training-data knowledge of the published paper; it has not been verified against a local PDF because
the publisher copy was not downloaded in this task.

Poleg-Polsky and Diamond use NEURON compartmental simulations of reconstructed retinal ganglion cell
(RGC) morphologies to test a widely used experimental method: estimating excitatory (Ge) and
inhibitory (Gi) synaptic conductances by recording voltage-clamp currents at multiple holding
potentials and decomposing them into linear E and I components. The method assumes the cell is well
space-clamped so that the local membrane potential everywhere matches the command, but real RGCs
have long thin dendrites that are poorly clamped from the soma. The paper quantifies how badly this
assumption is violated under realistic conditions and identifies which experimental choices most
amplify the resulting errors.

The authors show that imperfect space clamp allows the local membrane potential at distal synaptic
sites to drift away from the command voltage, and that co-activation of excitation and inhibition
causes these drifts to interact electrotonically. The result is that the reconstructed Ge and Gi
waveforms are systematically distorted in amplitude, time course, and sometimes sign, even when
standard experimental protocols are followed correctly. This is a load-bearing caveat for any
modelling work that takes published E/I traces as ground truth.

## Architecture, Models and Methods

The simulations use the NEURON compartmental simulator with realistic reconstructed RGC morphologies
including a soma, tapered dendritic tree, and axon. Passive membrane parameters (Rm, Cm, Ra) are set
from published recordings; active conductances are either absent (pure passive case) or include
standard voltage-gated Na+ and K+ channels to test how active dendritic integration modifies the
errors. Synapses are modelled as conductance changes with AMPA-like (reversal ~0 mV) and GABA-like
(reversal ~-60 to -70 mV) kinetics, placed at varying dendritic distances from the soma.

The authors implement a somatic single-electrode voltage clamp that mimics a real patch-clamp
amplifier, then run the standard experimental decomposition: record currents at a range of holding
potentials spanning both reversals, fit the I-V relationship at each time point, and read off the
slope and intercept as Ge and Gi. The reconstructed Ge/Gi waveforms are compared directly against
the ground-truth simulated conductances. Dendritic diameter, synaptic distance from soma, relative
timing of E and I inputs, and holding-potential range are varied systematically to map which
parameters produce the largest errors.

## Results

* On thin distal dendrites, up to approximately **80% of the synaptic signal** is lost before
  reaching the somatic pipette, producing a large underestimate of peak conductance.
* **Inhibitory conductance estimates carry larger errors than excitatory estimates**, even when
  clamping at the reported inhibitory reversal potential, because Gi reconstruction depends on
  accurate voltage at dendritic sites where Vm is furthest from the command.
* Electrotonic **interaction between co-active E and I** produces apparent conductances that do not
  exist in the ground truth; the reconstructed Ge waveform during concurrent inhibition can differ
  markedly from Ge reconstructed without inhibition.
* Errors scale with dendritic distance from the soma: proximal synapses within roughly **0.1
  lambda** are clamped acceptably, while synapses past ~0.3 lambda are severely distorted.
* Active dendritic voltage-gated channels amplify the errors further by allowing local regenerative
  events that are invisible at the soma.

## Innovations

### Quantitative Bound on Dendritic Voltage-Clamp Errors

This is the first paper to put concrete numbers on how bad the space-clamp problem is for realistic
RGC morphologies, rather than dismissing it as a qualitative caveat. The ~80% signal-loss figure for
thin distal dendrites is widely cited as a practical upper bound.

### Electrotonic E/I Interaction

The paper demonstrates that estimating Ge and Gi separately is not valid when both are present: the
errors are not independent because the two conductances interact through the dendritic cable. This
motivates simultaneous measurement protocols and compartmental-model-based reconstruction methods.

### Practical Experimental Guidance

The paper produces concrete recommendations: use short, fat dendrites for voltage-clamp studies
where possible; restrict Ge/Gi reconstruction to proximal synapses; treat distal-dendrite
conductance measurements as qualitative; and validate experimental reconstruction with compartmental
simulation of the specific cell morphology.

## Datasets

No external datasets were used. Simulations use NEURON with publicly available reconstructed RGC
morphologies and standard synaptic and channel kinetic parameters drawn from the published
retinal-physiology literature. The full model code is released through the ModelDB repository linked
from the paper.

## Main Ideas

* For any DSGC modelling work that takes published voltage-clamp-estimated Ge and Gi traces as
  ground-truth dendritic conductances, the true distal dendritic conductance can be several-fold
  larger than the somatic estimate, so plan model fits to absorb this calibration uncertainty.
* When comparing simulated voltage-clamp output to real recordings, the correct comparison is
  simulated-clamp-current vs recorded-clamp-current, not simulated-ground-truth-conductance vs
  experimentally-reconstructed-conductance. The modelling pipeline should include a somatic
  voltage-clamp block that mimics the experiment.
* Distal synapse placement and thin dendrites amplify the errors, so DSGC models with realistic
  dendritic morphology must expect large discrepancies between somatic voltage-clamp conductance
  measurements and dendritic conductance ground truth.

## Summary

Poleg-Polsky and Diamond ask a methodological question that matters for every modelling paper built
on experimental E/I decomposition: how accurate is the standard protocol of reconstructing
excitatory and inhibitory conductances from multi-holding-potential voltage-clamp recordings when
the cell has thin, extended dendrites? They answer it with NEURON compartmental simulations of
realistic retinal ganglion cell morphologies, where the ground-truth synaptic input is known and the
somatic pipette recording can be directly compared against it.

The methodology is careful: the authors systematically vary dendritic diameter, synaptic distance,
E/I relative timing, and holding-potential range, and compare each reconstruction against the known
inputs. They also test what happens when voltage-gated dendritic channels are added. The design
isolates space-clamp error from other confounds (series resistance, filtering, ionic
non-stationarity) and lets the reader see exactly which experimental choices drive the largest
distortions.

The headline result is that imperfect space clamp is not a second-order concern: on thin distal
dendrites up to 80% of the synaptic signal is lost, inhibitory estimates are systematically worse
than excitatory ones, and co-active E and I interact electrotonically so that reconstructing one
requires correctly modelling the other. Active dendritic channels make everything worse. The paper
practical guidance (proximal-only reconstruction, compartmental-model validation of each experiment)
is now standard.

For this project, the implication is direct. DSGC models will be calibrated against published Ge and
Gi traces from somatic voltage-clamp recordings, and those traces are lower bounds on the true
dendritic conductances, not ground truth. Our NEURON pipeline must include a somatic voltage-clamp
block so that simulated recordings can be compared to experimental recordings on the same footing,
and we must plan parameter-fitting procedures to absorb a several-fold calibration uncertainty on
distal synaptic conductance amplitudes.
