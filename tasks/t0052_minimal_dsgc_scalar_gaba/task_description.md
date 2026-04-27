# Minimal From-Scratch DSGC with Scalar gabaMOD Inhibition

## Source

Approved in brainstorm session 9 (t0051) as Task A of a paired wave (t0052 scalar gabaMOD, t0053
spatial PD/ND-asymmetric). No upstream suggestion ID; this task is created directly from the
session's strategic pivot away from the deposited Poleg-Polsky 2016 lineage and the t0022
channel-testbed lineage.

## Motivation

The t0046–t0050 reproduction wave demonstrated that the deposited ModelDB 189347 code does not
implement the mechanism described in the Poleg-Polsky 2016 paper text, and that the t0022
modified-port lineage carries accumulated deviations from that paper as well. Brainstorm session 9
commissioned a new from-scratch minimal DSGC built on the project's calibrated baseline morphology
so that all parameters and mechanisms are explicit, audited, and clean of upstream-code legacy.

This task implements the **scalar gabaMOD** variant of deRosenroll-style direction-dependent
inhibition, which is the form actually published in Poleg-Polsky 2016 and also a faithful
abstraction of de Rosenroll 2026's effective DSGC inhibition: every inhibitory synapse fires when
the bar covers it, but its amplitude is scaled by a direction-dependent scalar so that inhibition is
strongest in null direction and weakest in preferred direction.

The sibling task t0053 implements a true spatial PD/ND-asymmetric variant.

## Objective

Build and run a minimal compartmental DSGC model with the following specification, then report
per-direction voltage and firing-rate data so the behaviour can be compared against the project's
target tuning curve and against t0053.

## Model Specification

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (the t0009 Strahler-calibrated 141009_Pair1DSGC
  reconstruction).
* Compartments: as defined in the asset; standard NEURON section discretisation.

### Sections and Channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` channel mechanism (Na, K active
  conductances; leak built into the mechanism). Default densities from `hh.mod` unless explicit
  re-tuning is required to keep the cell silent at rest with V_rest = -65 mV.
* All dendritic sections: passive only. `Rm = 5999 ohm.cm^2`, `Ra = 100 ohm.cm`, `cm = 1 uF/cm^2`
  (matching t0024 baseline).
* V_rest: -65 mV.

### Synapses

* 100 excitatory (E) + 100 inhibitory (I) synapses, **co-located in pairs**.
* Placement: 100 dendritic locations sampled uniformly at random from the dendritic length (no
  distal bias; no exclusion of soma- or AIS-adjacent sections beyond the soma/AIS themselves). Each
  location hosts exactly one E + one I synapse.
* Random seed for placement: fixed (0) and reported in `results/results_detailed.md`.

### Excitatory mechanism (direction-independent, position-gated)

* `Exp2Syn` configured as a classical EPSP: rise = 0.5 ms, decay = 2.5 ms, e = 0 mV.
* Peak conductance per synapse: 0.5 nS.
* Trigger: each E synapse fires **one event** when the moving bar's leading edge crosses the
  synapse's (x, y) position projected along the bar's normal direction.
* Direction-independent waveform: identical EPSC shape regardless of bar direction.

### Inhibitory mechanism (direction-dependent via scalar gabaMOD)

* `Exp2Syn` configured as classical IPSC: rise = 1 ms, decay = 20 ms, e = -75 mV.
* Peak conductance per synapse: 2 nS times `gabaMOD(theta)`.
* `gabaMOD(theta) = 0.33 + 0.66 * (1 - cos(theta - theta_ND)) / 2`, where `theta_ND` is the null
  direction of the cell. By convention, set `theta_PD = 0` (rightward), `theta_ND = 180` (leftward);
  `theta` is the bar direction.
* Trigger: each I synapse fires **one event** when the moving bar's leading edge crosses the
  synapse's (x, y) position; the event's amplitude is scaled by `gabaMOD(theta)`.

### Stimulus protocol

* 12 bar directions: 0, 30, 60, ..., 330 degrees.
* Bar dimensions: 200 um wide x full arena length.
* Bar speed: 1000 um/s.
* Trial duration: 1500 ms.
* Trials per direction: 10.
* Total trials: 120.

## Outputs

For each of the 12 directions, produce:

1. **Soma V(t)** — mean trace +/- SD across the 10 trials. PNG under `results/images/`, embedded
   in `results_detailed.md`.
2. **Aggregate EPSP at soma** — sum of EPSC-driven somatic depolarisation per trial, mean trace
   +/- SD across trials. (Computed by simulating the synapse population with only E active.)
3. **Aggregate IPSP at soma** — analogous, with only I active.
4. **Firing-rate PSTH** — 5 ms bins, mean across 10 trials.
5. **Polar tuning curve** — peak firing rate (Hz) vs direction; primary DSI; vector-sum DSI;
   preferred direction.
6. **Per-synapse activation-time histogram** (sanity check): for each direction, histogram of when
   each E synapse fires. Confirms position-gating logic is correct.

## Library Asset

Produce one library asset: `minimal_dsgc_scalar_gaba`. Contents:

* Cell builder (morphology load + section channel assignment + V_rest setup).
* Synapse placer (uniform random over dendrites, 100 co-located pairs, fixed seed).
* Excitation driver (position-gated AMPA event scheduler).
* Inhibition driver (position-gated GABA event scheduler with scalar gabaMOD scaling).
* Trial runner (12 directions x 10 trials, deterministic seeds).
* Recording helpers (soma V, EPSC/IPSC components, spike times).

Follow the project's library asset specification (`meta/asset_types/library/specification.md`).

## Key Questions

1. With AMPA-only excitation, what peak firing rate does the cell produce in the preferred direction
   at default HH densities?
2. What is the primary DSI of this minimal model? Does it land in the project's target band (Park
   2014 in vivo: 0.40 - 0.60)?
3. Does the position-gated firing pattern match expectations (E synapses on the leading edge of the
   bar fire first, trailing-edge last)?
4. How do EPSP and IPSP aggregate amplitudes scale with direction under scalar gabaMOD?

## Compute and Budget

Local CPU only. Estimated wall-clock: ~1 week including library development and reporting. Cost:
$0.00.

## Out of Scope

* NMDA receptors (this is an AMPA-only minimal model by design).
* Active dendritic conductances.
* Synaptic noise (deterministic protocol; one event per synapse per trial).
* Network-level inputs (no SAC network; inhibition is a phenomenological scalar gating).
* Cross-comparison to t0053 (handled by a downstream task once both finish).

## Verification Criteria

* Library asset structure validates against `meta/asset_types/library/specification.md`.
* All 12 directions produce a per-direction PNG plot in `results/images/` and are embedded in
  `results_detailed.md`.
* `results/metrics.json` contains primary DSI, vector-sum DSI, preferred direction, peak Hz, null Hz
  at minimum.
* Sanity check: in the null direction, IPSP aggregate should be approximately 3x the
  preferred-direction IPSP aggregate (`gabaMOD(180)/gabaMOD(0) = 1.0/0.33`).
