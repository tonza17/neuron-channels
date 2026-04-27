# Minimal From-Scratch DSGC with Spatial PD/ND-Asymmetric Inhibition

## Source

Approved in brainstorm session 9 (t0051) as Task B of a paired wave (t0052 scalar gabaMOD, t0053
spatial PD/ND-asymmetric). No upstream suggestion ID; this task is created directly from the
session's strategic pivot to a from-scratch minimal-DSGC substrate.

## Motivation

This task is the spatial-asymmetry sibling of t0052. Where t0052 scales each I synapse's amplitude
by a global direction-dependent scalar, t0053 instead activates a synapse only when the moving
stimulus is approaching the synapse from outside the soma (centripetal motion). The aggregate effect
mimics the SAC network's known centrifugal preference (SAC dendrites release GABA preferentially
when stimuli move centrifugally over them, so from the post-synaptic DSGC's perspective inhibition
concentrates on dendrites being approached from the wrong side).

The two tasks isolate the impact of inhibition mechanism (scalar amplitude scaling vs spatial
gating) on direction selectivity at otherwise-identical morphology, excitation, spike generation,
and stimulus.

## Objective

Build and run a minimal compartmental DSGC model with the following specification, then report
per-direction voltage and firing-rate data so the behaviour can be compared against the project's
target tuning curve and against t0052.

## Model Specification

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (the t0009 Strahler-calibrated 141009_Pair1DSGC
  reconstruction).
* Compartments: as defined in the asset; standard NEURON section discretisation.

### Sections and Channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` channel mechanism.
* All dendritic sections: passive only. `Rm = 5999 ohm.cm^2`, `Ra = 100 ohm.cm`, `cm = 1 uF/cm^2`.
* V_rest: -65 mV.

### Synapses

* 100 E + 100 I synapses, **co-located in pairs**, uniform random over dendrites with the same fixed
  seed (0) as t0052. (Identical placement across the two tasks lets later comparison isolate the
  inhibition mechanism.)

### Excitatory mechanism (identical to t0052)

* `Exp2Syn`: rise = 0.5 ms, decay = 2.5 ms, e = 0 mV, peak 0.5 nS.
* Position-gated firing: each E synapse fires once when bar leading edge crosses it;
  direction-independent waveform.

### Inhibitory mechanism (spatial PD/ND-asymmetric, centripetal-only firing)

* `Exp2Syn`: rise = 1 ms, decay = 20 ms, e = -75 mV, peak 2 nS (no scalar scaling).
* For each I synapse i, define a centrifugal direction
  `theta_centrifugal_i = atan2(y_i - y_soma, x_i - x_soma)`.
* Synapse i fires only when the bar direction `theta_stim` satisfies
  `cos(theta_stim - theta_centrifugal_i) < 0`. Equivalently, the synapse fires when the stimulus
  motion has a component pointing back toward the soma (centripetal).
* When the firing condition is satisfied, the synapse fires one event at the moment the bar leading
  edge crosses its (x, y).
* Aggregate effect: for any given bar direction, only the half of I synapses whose centrifugal
  vectors point into the bar-incoming hemisphere will fire. Inhibition is spatially concentrated on
  the side of the dendritic field being approached "from the wrong end".

### Stimulus protocol

* Identical to t0052: 12 directions, 10 trials each, bar 200 um x full arena, 1000 um/s, T = 1500
  ms.

## Outputs

Same six output classes as t0052, plus one additional plot specific to the spatial mechanism:

1. Soma V(t) per direction.
2. Aggregate EPSP at soma per direction.
3. Aggregate IPSP at soma per direction.
4. Firing-rate PSTH per direction.
5. Polar tuning curve (peak Hz, primary DSI, vector-sum DSI, preferred direction).
6. Per-synapse activation-time histogram per direction.
7. **Polar plot of "fraction of I synapses active vs direction"** — confirms the
   centripetal-gating mechanism produces the expected directional asymmetry in the active I
   population.

## Library Asset

Produce one library asset: `minimal_dsgc_spatial_gaba`. Same component structure as
`minimal_dsgc_scalar_gaba` except the inhibition driver implements the centripetal-gating rule
instead of scalar gabaMOD scaling.

## Key Questions

1. Does spatial gating produce a higher or lower DSI than scalar gabaMOD on the same morphology and
   excitation?
2. Is the preferred direction of the model the same as t0052's, given that the underlying morphology
   is asymmetric (the soma is offset from the dendritic-field centroid)?
3. Does the "fraction of I synapses active" curve show the predicted ~50% modulation across
   direction, or does the morphology asymmetry produce a stronger / weaker modulation?
4. Does the spatial mechanism reproduce a biologically-realistic null-side-leading null inhibition
   timing pattern in the IPSP traces?

## Compute and Budget

Local CPU only. Estimated wall-clock: ~1 week. Cost: $0.00.

## Out of Scope

* NMDA receptors (AMPA-only minimal model by design).
* Active dendritic conductances.
* Synaptic noise.
* Network-level inputs.
* Cross-comparison to t0052 (handled by a downstream task once both finish).

## Verification Criteria

* Library asset validates against `meta/asset_types/library/specification.md`.
* All 12 directions produce a per-direction PNG plot in `results/images/` and are embedded in
  `results_detailed.md`.
* `results/metrics.json` contains primary DSI, vector-sum DSI, preferred direction, peak Hz, null Hz
  at minimum.
* The synapse-activation polar plot shows roughly 50% of I synapses active in each direction (any
  deviation must be explained by the dendritic-field asymmetry).
* Synapse placement uses the same fixed seed (0) as t0052 so the two tasks can be compared
  trial-for-trial in a downstream analysis.
