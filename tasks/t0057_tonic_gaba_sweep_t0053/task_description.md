# Tonic GABA + Amplitude Sweep on t0053 Spatial DSGC

## Source

Approved in brainstorm session 10 (t0056) and covers suggestion **S-0053-01** (GABA conductance
sweep on t0053 spatial DSGC to recover a non-zero FULL tuning curve).

## Motivation

t0053 reported a degenerate FULL-mode tuning curve of 0 Hz across all 12 directions because 2 nS
GABA on roughly half of 100 synapses (100 nS mean total per trial) fully suppressed spiking on the
t0009-calibrated morphology. While reviewing t0053's traces, the researcher noticed a second, more
fundamental issue: GABA conductance is only present in a narrow ~100-200 ms window per trial because
each spatial-gating GABA synapse fires exactly once at the bar-arrival time
(`t_onset = (x*cos(theta) + y*sin(theta)) / velocity + 100 ms`) and the Exp2Syn decay is only
`tau2 = 20 ms`. With a 1500 ms trial, this leaves the cell uninhibited for the remaining ~1100 ms
— biologically wrong (real SAC→DSGC IPSCs envelope over 100-300 ms via multiple GABA release
events) and the likely root cause of the t0053 amplitude-calibration sensitivity.

This task fixes the timing problem with a **tonic GABA conductance gated by stimulus window**
(brainstorm-10 Option C: simplest "always-on during stimulus" model) and then sweeps the per-synapse
peak conductance to find the operating point that produces a non-zero FULL-mode tuning curve while
preserving direction selectivity.

## Objective

Build a new GABA mechanism (`gaba_tonic.mod`) that delivers a sustained conductance over a
configurable `(t_on, t_off)` window per synapse, integrate it into the t0053 minimal DSGC code as a
drop-in replacement for the current Exp2Syn GABA mechanism, sweep per-synapse peak conductance
across five values, and report the directional response.

## Model Specification

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (the t0009 Strahler-calibrated 141009_Pair1DSGC
  reconstruction). Identical to t0053.

### Sections and Channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` channel mechanism.
* All dendritic sections: passive only. `Rm = 5999 ohm.cm^2`, `Ra = 100 ohm.cm`, `cm = 1 uF/cm^2`.
* V_rest: -65 mV.
* Identical to t0053.

### Synapses

* 100 E + 100 I synapses, **co-located in pairs**, uniform random over dendrites with the same fixed
  seed (0) as t0052 / t0053. Identical placement so the placement_seed0 fixture from t0053 applies
  bit-for-bit.

### Excitatory mechanism (identical to t0053)

* `Exp2Syn`: rise = 0.5 ms, decay = 2.5 ms, e = 0 mV, peak 0.5 nS.
* Position-gated firing: each E synapse fires once when bar leading edge crosses it;
  direction-independent waveform.

### Inhibitory mechanism (NEW — tonic gated by stimulus window)

* New point process: **`gaba_tonic.mod`** with parameters `(g, e, t_on, t_off)`:
  * Sustained conductance `g` (in microsiemens) between simulation times `t_on` and `t_off`.
  * Zero conductance outside that window.
  * Reversal `e = -75 mV` (matches `GABA_E_MV` from t0053).
  * Rise / fall envelope at the window edges: piecewise constant is acceptable, but a 1-2 ms cosine
    ramp to avoid step-function artefacts in the integrator is preferred.
* Per-synapse instance: each pair gets one `gaba_tonic` mechanism.
* **Spatial gating preserved from t0053**: gated synapses are those whose
  `cos(radians(theta_stim - theta_centrifugal_synapse)) < 0`. For each direction:
  * Active synapses: `g = GABA_BASE_NS` (the swept value), `t_on = 100 ms`, `t_off = 1400 ms`.
  * Silent synapses: `g = 0`.
* The `(t_on, t_off) = (100 ms, 1400 ms)` window matches the trial duration minus the 100 ms
  BASE_OFFSET buffer; effectively the GABA conductance is on throughout the entire stimulus
  presentation interval for the active half of the synapse population.

### Stimulus protocol

* Identical to t0053: 12 directions, 10 trials each, bar 200 um x full arena, 1000 um/s, T = 1500
  ms, dt = 0.025 ms.

## Sweep

* `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS — five conductance values.
* Total: 12 directions x 10 trials x 3 modes (FULL / AMPA_ONLY / GABA_ONLY) x 5 conductances = 1800
  trials.
* Estimated wall-clock: ~25-30 min on local CPU per the t0052 / t0053 wall-clock data (19m 13s for
  360 trials / 17m 11s for 360 trials respectively).

## Outputs

For each conductance value in the sweep:

1. Soma V(t) per direction (12 PNGs).
2. Aggregate EPSP at soma per direction (12 PNGs).
3. Aggregate IPSP at soma per direction (12 PNGs) — the new headline observable; should now span
   the full trial window 100-1400 ms instead of collapsing at ~200 ms.
4. Firing-rate PSTH per direction (12 PNGs).
5. Polar tuning curve (peak Hz, primary DSI, vector-sum DSI, preferred direction).
6. Per-synapse activation-time histogram per direction (still informative — synapse onset times
   match t0053 even though the conductance envelope differs).
7. Polar plot of "fraction of I synapses active vs direction" (carried over from t0053; should match
   t0053's 0.34-0.66 modulation since the spatial gating rule is unchanged).

Cross-conductance summary plots:

* DSI (primary) vs `GABA_BASE_NS` — single curve.
* DSI (vector-sum) vs `GABA_BASE_NS` — single curve.
* Peak Hz vs `GABA_BASE_NS` — preferred-direction firing rate as a function of inhibition mass.
* Null Hz vs `GABA_BASE_NS` — null-direction firing rate as a function of inhibition mass.
* HWHM vs `GABA_BASE_NS` — tuning sharpness as a function of inhibition mass.
* RMSE vs t0004 target curve at each `GABA_BASE_NS` — distance from project target tuning curve.

## Library Asset

Produce one library asset: **`minimal_dsgc_tonic_gaba_sweep`** (or similar slug). Same component
structure as `minimal_dsgc_spatial_gaba` except the inhibition driver uses the new `gaba_tonic`
point process instead of Exp2Syn. The library should expose `GABA_BASE_NS` as a public parameter so
the sweep harness can vary it without re-importing.

## Key Questions

1. Does the tonic-GABA mechanism produce a non-zero FULL-mode tuning curve at any of the swept
   conductance values? If so, at which value(s)?
2. How does direction selectivity (primary DSI, vector-sum DSI) scale with `GABA_BASE_NS`?
   Specifically, is there a window of conductances where DSI is both non-trivial (not 1.0
   single-spike-degenerate, not 0.0 fully-suppressed) and biologically plausible?
3. Does the IPSP somatic voltage envelope now span the full stimulus window (100-1400 ms) as
   intended, or does driving-force saturation still cause the IPSP voltage to collapse early?
4. At the conductance value matching t0053's 2 nS, does the tonic mechanism produce any spiking (vs
   t0053's 0 Hz across all directions), and if so what DSI does it report? This is the direct
   head-to-head against t0053.
5. How does the cross-conductance peak Hz vs target tuning curve compare? Does any single
   `GABA_BASE_NS` value land within an order of magnitude of the t0004 target peak (32 Hz)?

## Compute and Budget

Local CPU only. Estimated wall-clock: ~25-30 min for the simulation sweep, plus implementation and
verification time. Cost: $0.00.

## Out of Scope

* NMDA receptors (AMPA-only minimal model by design, matching t0053).
* Active dendritic conductances (passive dendrites by design).
* Synaptic noise (deterministic NetStim trials).
* Propagation of the tonic-GABA mechanism back to t0052 (scalar gabaMOD) — deferred to a future
  brainstorm if t0057 results justify it.
* Network-level inputs.

## Verification Criteria

* Library asset validates against `meta/asset_types/library/specification.md`.
* All 12 directions x 5 conductances produce per-direction PNG plots in `results/images/` and
  selected representatives are embedded in `results_detailed.md`.
* Cross-conductance summary plots (DSI / Peak Hz / Null Hz / HWHM / RMSE vs `GABA_BASE_NS`) exist
  and are embedded in `results_detailed.md`.
* `results/metrics.json` contains, for each `GABA_BASE_NS` value: primary DSI, vector-sum DSI,
  preferred direction, peak Hz, null Hz, HWHM, RMSE vs t0004 target.
* IPSP voltage trace at the tonic window matches the tonic-GABA design (sustained over 100-1400 ms,
  modulo driving-force saturation effects); regression test asserts the IPSP voltage at t = 1300 ms
  is at least 50% of the IPSP voltage at t = 200 ms in the most-active direction.
* Same fixed placement seed (0) as t0052 / t0053; placement_seed0_match test passes bit-for-bit
  against t0053's placement_seed0.json.
* AMPA_ONLY mode produces the same 0.667 Hz uniform peak rate as t0052 / t0053 (regression gate on
  the unchanged AMPA path).
* `verify_research_code.py`, `verify_plan.py`, `verify_task_metrics.py`, and the library asset
  verificator all pass with 0 errors.
