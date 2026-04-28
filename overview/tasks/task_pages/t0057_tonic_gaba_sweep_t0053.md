# ✅ Tonic GABA + amplitude sweep on t0053 spatial DSGC

[Back to all tasks](../README.md)

> Tuning Curve RMSE (Hz): **17.178292988536434**

## Overview

| Field | Value |
|---|---|
| **ID** | `t0057_tonic_gaba_sweep_t0053` |
| **Status** | ✅ completed |
| **Started** | 2026-04-28T14:18:58Z |
| **Completed** | 2026-04-28T18:02:00Z |
| **Duration** | 3h 43m |
| **Dependencies** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Source suggestion** | `S-0053-01` |
| **Task types** | `build-model`, `experiment-run` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`synaptic-integration`](../../by-category/synaptic-integration.md) |
| **Expected assets** | 1 library |
| **Step progress** | 10/15 |
| **Task folder** | [`t0057_tonic_gaba_sweep_t0053/`](../../../tasks/t0057_tonic_gaba_sweep_t0053/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0057_tonic_gaba_sweep_t0053/task_description.md)*

# Tonic GABA + Amplitude Sweep on t0053 Spatial DSGC

## Source

Approved in brainstorm session 10 (t0056) and covers suggestion **S-0053-01** (GABA
conductance sweep on t0053 spatial DSGC to recover a non-zero FULL tuning curve).

## Motivation

t0053 reported a degenerate FULL-mode tuning curve of 0 Hz across all 12 directions because 2
nS GABA on roughly half of 100 synapses (100 nS mean total per trial) fully suppressed spiking
on the t0009-calibrated morphology. While reviewing t0053's traces, the researcher noticed a
second, more fundamental issue: GABA conductance is only present in a narrow ~100-200 ms
window per trial because each spatial-gating GABA synapse fires exactly once at the
bar-arrival time (`t_onset = (x*cos(theta) + y*sin(theta)) / velocity + 100 ms`) and the
Exp2Syn decay is only `tau2 = 20 ms`. With a 1500 ms trial, this leaves the cell uninhibited
for the remaining ~1100 ms — biologically wrong (real SAC→DSGC IPSCs envelope over 100-300 ms
via multiple GABA release events) and the likely root cause of the t0053 amplitude-calibration
sensitivity.

This task fixes the timing problem with a **tonic GABA conductance gated by stimulus window**
(brainstorm-10 Option C: simplest "always-on during stimulus" model) and then sweeps the
per-synapse peak conductance to find the operating point that produces a non-zero FULL-mode
tuning curve while preserving direction selectivity.

## Objective

Build a new GABA mechanism (`gaba_tonic.mod`) that delivers a sustained conductance over a
configurable `(t_on, t_off)` window per synapse, integrate it into the t0053 minimal DSGC code
as a drop-in replacement for the current Exp2Syn GABA mechanism, sweep per-synapse peak
conductance across five values, and report the directional response.

## Model Specification

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (the t0009 Strahler-calibrated 141009_Pair1DSGC
  reconstruction). Identical to t0053.

### Sections and Channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` channel mechanism.
* All dendritic sections: passive only. `Rm = 5999 ohm.cm^2`, `Ra = 100 ohm.cm`, `cm = 1
  uF/cm^2`.
* V_rest: -65 mV.
* Identical to t0053.

### Synapses

* 100 E + 100 I synapses, **co-located in pairs**, uniform random over dendrites with the same
  fixed seed (0) as t0052 / t0053. Identical placement so the placement_seed0 fixture from
  t0053 applies bit-for-bit.

### Excitatory mechanism (identical to t0053)

* `Exp2Syn`: rise = 0.5 ms, decay = 2.5 ms, e = 0 mV, peak 0.5 nS.
* Position-gated firing: each E synapse fires once when bar leading edge crosses it;
  direction-independent waveform.

### Inhibitory mechanism (NEW — tonic gated by stimulus window)

* New point process: **`gaba_tonic.mod`** with parameters `(g, e, t_on, t_off)`:
  * Sustained conductance `g` (in microsiemens) between simulation times `t_on` and `t_off`.
  * Zero conductance outside that window.
  * Reversal `e = -75 mV` (matches `GABA_E_MV` from t0053).
  * Rise / fall envelope at the window edges: piecewise constant is acceptable, but a 1-2 ms
    cosine ramp to avoid step-function artefacts in the integrator is preferred.
* Per-synapse instance: each pair gets one `gaba_tonic` mechanism.
* **Spatial gating preserved from t0053**: gated synapses are those whose
  `cos(radians(theta_stim - theta_centrifugal_synapse)) < 0`. For each direction:
  * Active synapses: `g = GABA_BASE_NS` (the swept value), `t_on = 100 ms`, `t_off = 1400 ms`.
  * Silent synapses: `g = 0`.
* The `(t_on, t_off) = (100 ms, 1400 ms)` window matches the trial duration minus the 100 ms
  BASE_OFFSET buffer; effectively the GABA conductance is on throughout the entire stimulus
  presentation interval for the active half of the synapse population.

### Stimulus protocol

* Identical to t0053: 12 directions, 10 trials each, bar 200 um x full arena, 1000 um/s, T =
  1500 ms, dt = 0.025 ms.

## Sweep

* `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS — five conductance values.
* Total: 12 directions x 10 trials x 3 modes (FULL / AMPA_ONLY / GABA_ONLY) x 5 conductances =
  1800 trials.
* Estimated wall-clock: ~25-30 min on local CPU per the t0052 / t0053 wall-clock data (19m 13s
  for 360 trials / 17m 11s for 360 trials respectively).

## Outputs

For each conductance value in the sweep:

1. Soma V(t) per direction (12 PNGs).
2. Aggregate EPSP at soma per direction (12 PNGs).
3. Aggregate IPSP at soma per direction (12 PNGs) — the new headline observable; should now
   span the full trial window 100-1400 ms instead of collapsing at ~200 ms.
4. Firing-rate PSTH per direction (12 PNGs).
5. Polar tuning curve (peak Hz, primary DSI, vector-sum DSI, preferred direction).
6. Per-synapse activation-time histogram per direction (still informative — synapse onset
   times match t0053 even though the conductance envelope differs).
7. Polar plot of "fraction of I synapses active vs direction" (carried over from t0053; should
   match t0053's 0.34-0.66 modulation since the spatial gating rule is unchanged).

Cross-conductance summary plots:

* DSI (primary) vs `GABA_BASE_NS` — single curve.
* DSI (vector-sum) vs `GABA_BASE_NS` — single curve.
* Peak Hz vs `GABA_BASE_NS` — preferred-direction firing rate as a function of inhibition
  mass.
* Null Hz vs `GABA_BASE_NS` — null-direction firing rate as a function of inhibition mass.
* HWHM vs `GABA_BASE_NS` — tuning sharpness as a function of inhibition mass.
* RMSE vs t0004 target curve at each `GABA_BASE_NS` — distance from project target tuning
  curve.

## Library Asset

Produce one library asset: **`minimal_dsgc_tonic_gaba_sweep`** (or similar slug). Same
component structure as `minimal_dsgc_spatial_gaba` except the inhibition driver uses the new
`gaba_tonic` point process instead of Exp2Syn. The library should expose `GABA_BASE_NS` as a
public parameter so the sweep harness can vary it without re-importing.

## Key Questions

1. Does the tonic-GABA mechanism produce a non-zero FULL-mode tuning curve at any of the swept
   conductance values? If so, at which value(s)?
2. How does direction selectivity (primary DSI, vector-sum DSI) scale with `GABA_BASE_NS`?
   Specifically, is there a window of conductances where DSI is both non-trivial (not 1.0
   single-spike-degenerate, not 0.0 fully-suppressed) and biologically plausible?
3. Does the IPSP somatic voltage envelope now span the full stimulus window (100-1400 ms) as
   intended, or does driving-force saturation still cause the IPSP voltage to collapse early?
4. At the conductance value matching t0053's 2 nS, does the tonic mechanism produce any
   spiking (vs t0053's 0 Hz across all directions), and if so what DSI does it report? This is
   the direct head-to-head against t0053.
5. How does the cross-conductance peak Hz vs target tuning curve compare? Does any single
   `GABA_BASE_NS` value land within an order of magnitude of the t0004 target peak (32 Hz)?

## Compute and Budget

Local CPU only. Estimated wall-clock: ~25-30 min for the simulation sweep, plus implementation
and verification time. Cost: $0.00.

## Out of Scope

* NMDA receptors (AMPA-only minimal model by design, matching t0053).
* Active dendritic conductances (passive dendrites by design).
* Synaptic noise (deterministic NetStim trials).
* Propagation of the tonic-GABA mechanism back to t0052 (scalar gabaMOD) — deferred to a
  future brainstorm if t0057 results justify it.
* Network-level inputs.

## Verification Criteria

* Library asset validates against `meta/asset_types/library/specification.md`.
* All 12 directions x 5 conductances produce per-direction PNG plots in `results/images/` and
  selected representatives are embedded in `results_detailed.md`.
* Cross-conductance summary plots (DSI / Peak Hz / Null Hz / HWHM / RMSE vs `GABA_BASE_NS`)
  exist and are embedded in `results_detailed.md`.
* `results/metrics.json` contains, for each `GABA_BASE_NS` value: primary DSI, vector-sum DSI,
  preferred direction, peak Hz, null Hz, HWHM, RMSE vs t0004 target.
* IPSP voltage trace at the tonic window matches the tonic-GABA design (sustained over
  100-1400 ms, modulo driving-force saturation effects); regression test asserts the IPSP
  voltage at t = 1300 ms is at least 50% of the IPSP voltage at t = 200 ms in the most-active
  direction.
* Same fixed placement seed (0) as t0052 / t0053; placement_seed0_match test passes
  bit-for-bit against t0053's placement_seed0.json.
* AMPA_ONLY mode produces the same 0.667 Hz uniform peak rate as t0052 / t0053 (regression
  gate on the unchanged AMPA path).
* `verify_research_code.py`, `verify_plan.py`, `verify_task_metrics.py`, and the library asset
  verificator all pass with 0 errors.

</details>

## Metrics

### GABA=0.25 nS / FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.66947867777781** |

### GABA=0.25 nS / AMPA_ONLY

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |

### GABA=0.50 nS / FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.66947867777781** |

### GABA=0.50 nS / AMPA_ONLY

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |

### GABA=1.00 nS / FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.66947867777781** |

### GABA=1.00 nS / AMPA_ONLY

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |

### GABA=1.50 nS / FULL

| Metric | Value |
|--------|-------|
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **17.178292988536434** |

### GABA=1.50 nS / AMPA_ONLY

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |

### GABA=2.00 nS / FULL

| Metric | Value |
|--------|-------|
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **17.178292988536434** |

### GABA=2.00 nS / AMPA_ONLY

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [Minimal DSGC with Tonic GABA Sweep](../../../tasks/t0057_tonic_gaba_sweep_t0053/assets/library/minimal_dsgc_tonic_gaba_sweep/) | [`description.md`](../../../tasks/t0057_tonic_gaba_sweep_t0053/assets/library/minimal_dsgc_tonic_gaba_sweep/description.md) |

## Suggestions Generated

<details>
<summary><strong>Sub-0.25 nS tonic GABA finer sweep on t0057 to test
graded-suppression hypothesis</strong> (S-0057-01)</summary>

**Kind**: experiment | **Priority**: medium

t0057 swept GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0} nS and found a binary regime: gaba <=
1.0 nS produces uniform 0.667 Hz single-spike-per-trial (tonic too weak to override AMPA
spike) and gaba >= 1.5 nS produces 0 Hz full suppression. The sub-0.25 nS regime is
uncharacterised and may host a graded-suppression operating point where the tonic envelope
partially vetoes the AMPA spike on subset of trials, producing a probabilistic firing-rate
signal that could carry direction information. Run a finer sweep at GABA_BASE_NS in {0.05,
0.10, 0.125, 0.15, 0.175, 0.20, 0.225} nS on the t0057 minimal_dsgc_tonic_gaba_sweep library
at 12 directions x 10 trials x 3 modes (2520 trials, ~75 min wall-clock). Pass criterion:
identify any conductance with FULL-mode peak Hz != null Hz (i.e., non-degenerate primary DSI),
or rule out the existence of such a graded operating point in the sub-AMPA-spike-veto regime.
Recommended task types: experiment-run.

</details>

<details>
<summary><strong>AMPA conductance escape sweep on t0057 tonic-GABA substrate to
enter multi-spike regime first</strong> (S-0057-02)</summary>

**Kind**: experiment | **Priority**: high

t0057 confirmed (alongside t0052, t0053, t0054) that AMPA = 0.5 nS x 100 synapses gives at
most one spike per trial; this binary regime cannot produce graded DSI under any inhibition
mechanism. S-0052-01 proposes the AMPA escape on the t0052 scalar-gabaMOD substrate; this
suggestion proposes the matching experiment on the t0057 tonic substrate so the AMPA-escape
and tonic-GABA-amplitude axes are directly cross-comparable. Sweep AMPA per-synapse
conductance in {0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0} nS at fixed GABA_BASE_NS in {0.5, 1.0, 1.5}
nS (21 grid cells, 7560 trials). Report peak Hz, FULL-mode primary and vector-sum DSI, HWHM,
and reliability per cell. Pass criterion: locate at least one (gAMPA, gGABA) point on the
tonic substrate with peak Hz in 5-50 Hz AND vector-sum DSI > 0.3, or rule out such a point in
the sustained-envelope regime. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Hybrid tonic + transient GABA envelope on minimal DSGC to model
multi-event SAC release</strong> (S-0057-03)</summary>

**Kind**: experiment | **Priority**: medium

Real SAC->DSGC IPSCs envelope over 100-300 ms via multiple GABA release events per varicosity,
between t0057's single 1300 ms pulse and t0053's single ~80 ms decay tail. Build a hybrid
mechanism whose conductance envelope is the sum of a low-amplitude tonic floor (g_tonic over
[t_on, t_off]) and a sequence of transient Exp2Syn events (rise 1 ms, decay 20 ms) at rate r
in {25, 50, 100} Hz over the same window. Keep the t0053 spatial centripetal gating rule and
t0057 placement seed unchanged so this isolates envelope-shape effects. Sweep g_tonic in {0.0,
0.05, 0.1, 0.2} nS x g_event in {0.5, 1.0, 2.0} nS x rate r in {25, 50, 100} Hz (36 grid
cells, 12960 trials). Report peak Hz, primary and vector-sum DSI, IPSP envelope variance, and
IPSP autocorrelation timescale. Pass criterion: locate at least one (g_tonic, g_event, r)
triple with peak Hz != null Hz in FULL mode AND IPSP envelope tau within 100-300 ms biological
band. Recommended task types: build-model, experiment-run.

</details>

<details>
<summary><strong>Per-synapse stimulus-window-tied (t_on, t_off) tonic GABA on t0057
to model bar-arrival-locked inhibition</strong> (S-0057-04)</summary>

**Kind**: experiment | **Priority**: high

t0057 used a global (t_on, t_off) = (100 ms, 1400 ms) for every active synapse regardless of
dendritic position. Biological SAC inhibition is bar-arrival-locked: each SAC outputs GABA
only as the bar passes its dendritic field, producing a synapse-specific window of width
~100-300 ms. On t0057's minimal_dsgc_tonic_gaba_sweep substrate, modify schedule_ei_onsets so
each centripetally-active I synapse gets t_on = (x*cos(theta) + y*sin(theta))/v + offset_ms
and t_off = t_on + window_ms, where (x, y) is synapse coordinate, theta is bar direction, v is
bar velocity, and window_ms is swept in {50, 100, 200, 400} ms. Keep GABA_BASE_NS at 1.0 nS
(borderline single-spike regime). Run 12 dir x 10 trials x 3 modes per window (1440 trials,
~85 min). Pass criterion: locate at least one window where the per-synapse onset gradient
produces direction-dependent IPSP timing that breaks the FULL-mode degeneracy (peak Hz != null
Hz). Recommended task types: build-model, experiment-run.

</details>

<details>
<summary><strong>Sustained-envelope gabaMOD on t0052 minimal scalar architecture
(tonic-mechanism back-port)</strong> (S-0057-05)</summary>

**Kind**: experiment | **Priority**: medium

t0057 introduced a sustained (1300 ms) tonic envelope on the t0053 spatial substrate; the
back-port question is whether applying the same envelope to t0052's scalar gabaMOD inhibition
(graded amplitude, all 100 synapses fire) breaks t0052's binary single-spike DSI usefully.
Build a t0052 variant that replaces per-event Exp2Syn(rise=1, decay=20 ms) inhibition with a
sustained gabaMOD-envelope using gaba_tonic.mod from t0057, holding g(theta) = gabaMOD(theta)
* GABA_BASE_NS over (t_on, t_off) = (100, 1400) ms per synapse. Sweep GABA_BASE_NS in {0.05,
0.1, 0.25, 0.5, 1.0, 2.0} nS at gabaMOD_PD = 0.33, gabaMOD_ND = 0.99 (matching t0052). Run 12
dir x 10 trials x 3 modes per conductance (2160 trials, ~2 h). Pass criterion: identify a
GABA_BASE_NS where FULL-mode peak Hz is non-zero AND primary DSI is non-degenerate, or rule it
out. Decomposes inhibition-envelope-shape from spatial-pattern. Recommended task types:
build-model, experiment-run.

</details>

<details>
<summary><strong>Tonic GABA + Mg-block NMDA combination on t0054-style architecture
to test multiplicative gain rescue</strong> (S-0057-06)</summary>

**Kind**: experiment | **Priority**: high

Cumulative project evidence (t0054, t0055, t0057) converges on PolegPolsky2016's argument that
voltage-dependent NMDA Mg-block is necessary for non-trivial DSI. t0055 added Mg-block NMDA
but kept scalar gabaMOD inhibition; t0057 swapped inhibition to tonic but kept AMPA-only
excitation. Neither tested the combination. Build a minimal architecture combining (a) AMPA +
Jahr-Stevens Mg-block NMDA (t0055 NMDA_MgBlock.mod) on each E synapse and (b) tonic GABA via
gaba_tonic.mod (t0057) with the t0053 spatial centripetal gating predicate on each I synapse.
Sweep gNMDA in {0.0, 0.25, 0.5, 1.0} nS x GABA_BASE_NS in {0.1, 0.25, 0.5, 1.0} nS at fixed
gAMPA = 0.5 nS, seed 0 (16 grid cells, 5760 trials). Pass criterion: locate at least one
(gNMDA, GABA_BASE_NS) point with vector-sum DSI > 0.3 AND peak Hz >= 5 Hz, or rule it out.
Distinct from S-0054-02 (voltage-independent NMDA + scalar GABA) and S-0055-03 (Mg-block NMDA
+ scalar GABA ladder). Recommended task types: build-model, experiment-run.

</details>

## Research

* [`research_code.md`](../../../tasks/t0057_tonic_gaba_sweep_t0053/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/results_summary.md)*

# Results Summary: Tonic GABA + Amplitude Sweep on t0053 Spatial DSGC

## Summary

Replaced t0053's per-event Exp2Syn GABA with a sustained `gaba_tonic` POINT_PROCESS
(conductance held over a configurable `(t_on, t_off) = (100 ms, 1400 ms)` window) and ran a
1800-trial sweep across `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS. Headline negative
finding: no operating point in the swept grid produces non-trivial direction selectivity.
Below 1.5 nS the cell fires its single-spike-per-trial regime uniformly across all directions
(peak = null = 0.667 Hz, identical to AMPA_ONLY); at 1.5 and 2.0 nS the cell is fully
suppressed (peak = null = 0 Hz). The active-fraction modulation (0.34 → 0.66 across
directions) confirms the spatial centripetal-gating rule is intact; the failure is amplitude
calibration interacting with the sustained mechanism, not the gating.

## Metrics

* **Primary DSI (FULL) at all 5 conductances**: **0.0** (degenerate — peak = null at every
  swept value).
* **Vector-sum DSI (FULL) at all 5 conductances**: **0.0** (3.2e-17 numerical floor for the
  three sub-threshold-suppression values; 0.0 exact for the two fully-suppressed values).
* **Peak Hz at gaba in {0.25, 0.5, 1.0} nS**: **0.667 Hz** (identical to AMPA_ONLY
  single-spike regime — tonic GABA at these levels is too weak to override the single AMPA
  spike).
* **Peak Hz at gaba in {1.5, 2.0} nS**: **0.0 Hz** (full suppression — tonic GABA strong
  enough to keep V below threshold continuously).
* **AMPA_ONLY peak Hz** at all 5 conductances: **0.6667 Hz** uniformly across all 12
  directions — bit-identical to t0052 / t0053 AMPA_ONLY result. **REQ-14 PASS.**
* **Tuning-curve RMSE vs t0004 target** (FULL): **16.67 Hz** (gaba ≤ 1.0 nS) and **17.18 Hz**
  (gaba ≥ 1.5 nS) — large because the t0004 target peaks near 32 Hz while this model peaks at
  0.667 Hz or 0 Hz.
* **Active-fraction modulation** across directions: **0.34 (θ = 30°) to 0.66 (θ = 210°)**;
  mean **0.500** ∈ [0.4, 0.6] soft band — **PASS**. Bit-identical to t0053 since the spatial
  gating rule is unchanged.
* **Aggregate IPSP voltage envelope** (most-active direction θ = 210°, FULL mode):
  * gaba = 0.25 nS: peak **3.17 mV**
  * gaba = 0.50 nS: peak **4.88 mV**
  * gaba = 1.00 nS: peak **6.55 mV**
  * gaba = 1.50 nS: peak **7.38 mV**
  * gaba = 2.00 nS: peak **7.87 mV**
  * IPSP grows sub-linearly with gaba — driving-force saturation as Vm approaches `E_GABA =
    -75 mV`. The 0.25 → 2.0 nS conductance ratio of 8x produces only a 2.5x voltage-envelope
    ratio.
* **Aggregate EPSP magnitude** (peak ≈ 84 mV above V_rest at all directions and all
  conductances) — confirms AMPA mechanism untouched and direction-independent.
* **Wall-clock**: **6318.34 s = 105.31 min** for 1800 trials (single-threaded local CPU).

## Verification

* `verify_library_asset.py minimal_dsgc_tonic_gaba_sweep` — **PASSED** (0/0).
* `verify_task_metrics.py t0057_tonic_gaba_sweep_t0053` — **PASSED** (0/0).
* `ruff check` and `ruff format` — clean across all task code modules.
* `mypy -p tasks.t0057_tonic_gaba_sweep_t0053.code` — no issues.
* AMPA_ONLY 0.667 Hz regression sentinel (REQ-14): **PASSED** at all 5 conductances.
* IPSP-sustained-window regression test (REQ-13): **PASSED** at all 5 conductances (IPSP at t
  = 1300 ms is at least 50% of IPSP at t = 200 ms in the most-active direction — the new tonic
  mechanism is delivering sustained conductance over the full window as designed).
* Placement bit-identical to t0052 / t0053 (`test_placement_seed0_match.py`): **PASSED**.
* Quiescent-rest gate (`test_quiescent_rest.py`, V_rest = -65 mV ± 0.5 mV): **PASSED**.
* Spatial-gating unit test (`test_spatial_gating.py`): **PASSED**.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0057_tonic_gaba_sweep_t0053" date_completed: "2026-04-28" ---
# Results Detailed: Tonic GABA + Amplitude Sweep on t0053 Spatial DSGC

## Summary

Replaced t0053's per-event Exp2Syn GABA mechanism with a new `gaba_tonic` POINT_PROCESS that
holds a sustained conductance over a configurable `(t_on, t_off)` window per synapse, and ran
a 1800-trial sweep across `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS. The headline
finding is a meaningful negative result: no operating point in the swept grid produces
non-trivial direction selectivity. The spatial centripetal-gating rule from t0053 was
preserved bit-for-bit (active fraction 0.34 → 0.66 across directions, mean 0.500); the failure
is amplitude calibration interacting with the sustained-window mechanism rather than the
gating itself. AMPA_ONLY regression sentinel (0.667 Hz) and IPSP-sustained-window regression
sentinel both pass at all 5 conductances, validating that (a) the AMPA path is unchanged from
t0052 / t0053 and (b) the new tonic mechanism is delivering sustained conductance over the
full 100-1400 ms window as designed.

## Methodology

* **Machine**: local CPU (single-threaded NEURON simulation).
* **Wall-clock**: 6318.34 s (105.31 min) for 1800 trials = 3.51 s / trial.
* **Sweep grid**: `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS x 12 directions x 10 trials
  x 3 modes (FULL / AMPA_ONLY / GABA_ONLY) = 1800 trials.
* **Tonic GABA window**: `t_on = 100 ms`, `t_off = 1400 ms` per active synapse (1300 ms
  sustained-conductance window, with 1-2 ms cosine ramps at the edges to avoid integrator
  step-function artefacts).
* **Spatial gating** (preserved from t0053 bit-for-bit): each I synapse fires only when
  `cos(radians(theta_stim - theta_centrifugal_synapse)) < 0`. When fired, `g = GABA_BASE_NS`
  (in microsiemens, scaled by 1e-3 from nS); when silent, `g = 0`.
* **Bar stimulus**: 200 µm wide, 1.0 µm/ms (1000 µm/s), 1500 ms trial duration, dt = 0.025 ms.
* **Morphology**: `dsgc-baseline-morphology-calibrated` (the t0009 calibrated 141009_Pair1DSGC
  reconstruction). Identical to t0052 and t0053.
* **Synapse population**: 100 E + 100 I co-located pairs, uniform random over dendrites, fixed
  placement seed 0 (bit-identical to t0052 and t0053; `test_placement_seed0_match.py` passes).
* **Excitation**: AMPA `Exp2Syn` (rise = 0.5 ms, decay = 2.5 ms, e = 0 mV, peak 0.5 nS),
  position-gated single events. Identical to t0052 and t0053.
* **Spike detection**: somatic V > -20 mV with NetCon record(); per-trial spike times in
  `spike_times_<mode>.csv`.
* **Multiprocessing**: not used; single-threaded sequential trial loop. Estimated 4-thread
  pool would have brought wall-clock to ~26 min but introduced ordering nondeterminism.

## Headline Findings

### 1. No DSI-preserving operating point in the swept grid (Key Question 2 — answered NO)

| `GABA_BASE_NS` | FULL Peak Hz | FULL Null Hz | Primary DSI | Vector-sum DSI | HWHM |
| --- | --- | --- | --- | --- | --- |
| 0.25 nS | 0.667 | 0.667 | 0.0 | 3.2e-17 | 180° (degenerate) |
| 0.50 nS | 0.667 | 0.667 | 0.0 | 3.2e-17 | 180° (degenerate) |
| 1.00 nS | 0.667 | 0.667 | 0.0 | 3.2e-17 | 180° (degenerate) |
| 1.50 nS | 0.000 | 0.000 | null | 0.0 | null (degenerate) |
| 2.00 nS | 0.000 | 0.000 | null | 0.0 | null (degenerate) |

Two regimes: under 1.5 nS the tonic GABA is too weak to suppress the single AMPA-driven spike
(peak = null = 0.667 Hz across all 12 directions, identical to AMPA_ONLY); at and above 1.5 nS
the tonic GABA is strong enough to hold Vm sub-threshold continuously (peak = null = 0 Hz). No
single-spike-per-trial state in between produces direction selectivity because the binary
nature of the firing decision (one spike or none, deterministic across trials) is invariant to
whether the cell is suppressed or not.

### 2. The IPSP voltage envelope grows sub-linearly with conductance (Key Question 3 — driving-force saturation confirmed)

Aggregate IPSP voltage at the most-active direction (θ = 210°, peak active-fraction 0.66):

| `GABA_BASE_NS` | Peak IPSP voltage |
| --- | --- |
| 0.25 nS | 3.17 mV |
| 0.50 nS | 4.88 mV |
| 1.00 nS | 6.55 mV |
| 1.50 nS | 7.38 mV |
| 2.00 nS | 7.87 mV |

The 8x conductance ratio (0.25 → 2.0 nS) produces only a 2.5x voltage-envelope ratio — same
driving-force saturation mechanism documented in t0052 (1.54x voltage from 3.0x conductance)
and t0053 (1.24x voltage from 1.94x active-count ratio). With Vm driven toward `E_GABA = -75
mV` by sustained inhibition over 1300 ms, additional conductance produces sub-linear voltage
suppression. The IPSP-sustained-window regression sentinel (REQ-13) confirms that IPSP voltage
at t = 1300 ms is at least 50% of IPSP voltage at t = 200 ms — the new tonic mechanism does
deliver sustained conductance over the full window as designed (unlike t0053's per-event
Exp2Syn GABA which collapsed within ~80 ms after the last synapse fired).

### 3. Direct head-to-head against t0053 (Key Question 4 — answered)

At the conductance value matching t0053's 2 nS, the tonic mechanism produces **0.0 Hz** in
FULL mode — the same fully-suppressed result as t0053's per-event Exp2Syn GABA. The tonic
mechanism is *more* suppressive at 2.0 nS than t0053's brief-event mechanism because the
sustained-window conductance integrates over the full 1300 ms window vs t0053's ~80 ms decay
tail per event. The matched-amplitude head-to-head therefore does not produce a non-zero
firing rate that would let us isolate the timing-mechanism effect from the suppression
amplitude.

### 4. No conductance lands within an order of magnitude of the t0004 target peak (Key Question 5 — answered NO)

The t0004 target peak rate is **32 Hz**. None of the swept conductances produce any non-zero
firing — the peak rate is either 0.667 Hz (single-spike regime, ~48x below target) or 0 Hz
(suppression). The tuning-curve RMSE vs t0004 ranges from 16.67 Hz to 17.18 Hz — dominated by
the 32 Hz target peak vs the model's ≤ 0.667 Hz response.

### 5. Spatial gating intact (active-fraction polar plot)

Active-fraction modulation across directions: **0.34 (θ = 30°) to 0.66 (θ = 210°)**, mean
**0.500** — bit-identical to t0053 since the spatial gating rule is unchanged. Soft sanity
band [0.4, 0.6] for the mean: **PASS**.

## Metrics

`metrics.json` contains 15 variants (5 conductances x 3 modes). The four registered project
metrics (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`) are recorded for each variant. `derived_quantities.json` contains the
full per-conductance / per-direction breakdown of peak Hz, null Hz, vector-sum DSI, EPSP and
IPSP voltage envelopes, active-fraction polar curve, and the cross-conductance summary arrays.

| Variant | Primary DSI | Vector-sum DSI | HWHM (deg) | RMSE vs t0004 target (Hz) |
| --- | --- | --- | --- | --- |
| gaba_0.25_full | 0.0 | 3.2e-17 | 180.0 | 16.67 |
| gaba_0.25_ampa_only | 0.0 | 3.2e-17 | 180.0 | n/a |
| gaba_0.25_gaba_only | n/a | 0.0 | n/a | n/a |
| gaba_0.50_full | 0.0 | 3.2e-17 | 180.0 | 16.67 |
| gaba_0.50_ampa_only | 0.0 | 3.2e-17 | 180.0 | n/a |
| gaba_0.50_gaba_only | n/a | 0.0 | n/a | n/a |
| gaba_1.00_full | 0.0 | 3.2e-17 | 180.0 | 16.67 |
| gaba_1.00_ampa_only | 0.0 | 3.2e-17 | 180.0 | n/a |
| gaba_1.00_gaba_only | n/a | 0.0 | n/a | n/a |
| gaba_1.50_full | null | 0.0 | null | 17.18 |
| gaba_1.50_ampa_only | 0.0 | 3.2e-17 | 180.0 | n/a |
| gaba_1.50_gaba_only | n/a | 0.0 | n/a | n/a |
| gaba_2.00_full | null | 0.0 | null | 17.18 |
| gaba_2.00_ampa_only | 0.0 | 3.2e-17 | 180.0 | n/a |
| gaba_2.00_gaba_only | n/a | 0.0 | n/a | n/a |

## Visualizations

### Cross-conductance summary plots

![DSI primary vs
gaba_base_ns](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/images/dsi_primary_vs_gaba.png)

Primary DSI vs `GABA_BASE_NS`. Flat at 0 across the swept grid: the cell either fires
uniformly or not at all, never producing direction discrimination.

![Peak Hz vs
gaba_base_ns](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/images/peak_hz_vs_gaba.png)

Peak firing rate (FULL mode) vs `GABA_BASE_NS`. Step function at 1.5 nS marking the transition
from single-spike-per-trial to full suppression. The t0004 target peak (32 Hz) is far above
the plotted range.

![Null Hz vs
gaba_base_ns](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/images/null_hz_vs_gaba.png)

Null-direction firing rate (FULL mode) vs `GABA_BASE_NS`. Identical to peak Hz curve — the
binary firing decision is invariant to direction at every sampled conductance.

![HWHM vs
gaba_base_ns](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/images/hwhm_vs_gaba.png)

Half-width at half-maximum vs `GABA_BASE_NS`. Either 180° (uniform firing — tuning curve has
no peak) or null (no firing at all).

![RMSE vs
gaba_base_ns](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/images/rmse_vs_gaba.png)

Tuning-curve RMSE vs t0004 target (FULL mode) vs `GABA_BASE_NS`. Dominated by the 32 Hz target
peak vs the model's ≤ 0.667 Hz response.

### Spatial gating sanity check

![Active fraction polar
plot](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/images/active_fraction_polar.png)

Per-direction active fraction of the 100 I synapses. Modulates from 0.34 at θ = 30° to 0.66 at
θ = 210° — bit-identical to t0053 since the spatial gating rule is unchanged. Mean across
directions = 0.500, well within the [0.4, 0.6] soft sanity band.

### Per-conductance polar tuning curves

![Polar tuning curve at gaba=0.25
nS](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/images/polar_tuning_curve_gaba_0.25.png)

FULL-mode polar tuning curve at gaba = 0.25 nS. Uniform circle at 0.667 Hz across all 12
directions — same shape at gaba = 0.50 nS and gaba = 1.00 nS.

![Polar tuning curve at gaba=2.00
nS](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/images/polar_tuning_curve_gaba_2.00.png)

FULL-mode polar tuning curve at gaba = 2.00 nS. Empty (zero) at all 12 directions — same shape
at gaba = 1.50 nS.

The remaining 348 PNGs in `results/images/` cover per-direction soma V(t), aggregate EPSP,
aggregate IPSP, raster + PSTH, and synapse-activation histogram for each (conductance,
direction) combination. They are not embedded individually here for brevity but are present in
the asset tree and referenced by the per-direction analysis sections of the cross-task
comparison documents.

## Limitations

* **Single-threaded sweep**: 105 min wall-clock for 1800 trials. Multiprocessing was not
  attempted; a 4-worker pool would have brought it to ~26 min but introduced ordering
  nondeterminism that complicates the placement-seed-0 reproducibility guarantee.
* **No noise**: Trials are deterministic single-event-per-synapse; reliability = 1.0 is
  artefactual. Not a flaw of this task per se, but worth noting that DSI sensitivity to
  release noise is not characterised here.
* **No NMDA**: AMPA-only by design (matching t0053's parent); the tonic-GABA + NMDA
  combination is left for a follow-up.
* **Coarse sweep grid**: 5 conductance values; sub-0.25 nS regime (where tonic GABA might
  produce graded suppression rather than the binary single-spike-vs-zero) is not
  characterised. A finer grid (e.g., 0.05, 0.10, 0.15, 0.20, 0.25 nS) would test whether any
  tonic operating point exists below the single-spike-threshold.
* **Single-spike-per-trial regime is the underlying problem**: the cell at this AMPA strength
  + morphology fires at most one spike per direction. This binary regime cannot produce
  meaningful DSI under any inhibition mechanism (scalar gabaMOD as in t0052, spatial Exp2Syn
  as in t0053, tonic as in t0057) — they all collapse to either 1-spike-uniform or
  0-spike-uniform. The path forward is to first escape the single-spike regime via higher AMPA
  conductance (S-0052-01) and then re-evaluate inhibition mechanisms in the multi-spike
  regime.
* **Tonic window is "always-on during stimulus"**: not biologically faithful — real SAC→DSGC
  IPSCs envelope over 100-300 ms via multiple GABA release events per varicosity rather than a
  single 1300 ms tonic pulse. Brainstorm-10 explicitly chose this simplest model (Option C)
  with the understanding that biological realism would be revisited if results justified it.

## Files Created

* `code/mod/GabaTonic.mod` (and compiled `.c`, `.o`, `nrnmech.dll`)
* `code/mod/run_nrnivmodl.cmd` (compilation shim)
* `code/neuron_bootstrap.py` (with `ensure_gaba_tonic_compiled()` hook)
* `code/synapses.py` (rewritten for direct `gaba_syn.g/t_on/t_off` attribute writes)
* `code/trial.py`, `code/run_tuning_curve.py`, `code/cell.py`, `code/swc_io.py`,
  `code/placement.py`, `code/constants.py`, `code/paths.py`, `code/metrics_extra.py`,
  `code/compute_metrics.py`, `code/render_figures.py`
* `code/test_gaba_tonic_envelope.py`, `code/test_placement_seed0_match.py`,
  `code/test_quiescent_rest.py`, `code/test_spatial_gating.py`
* `assets/library/minimal_dsgc_tonic_gaba_sweep/details.json`
* `assets/library/minimal_dsgc_tonic_gaba_sweep/description.md`
* `results/tuning_curve_{full,ampa_only,gaba_only}.csv` (60 rows each)
* `results/spike_times_{full,ampa_only,gaba_only}.csv`
* `results/voltage_traces_{full,ampa_only,gaba_only}.csv` (downsampled stride-8)
* `results/activation_times.csv`
* `results/active_fraction_per_direction.csv`
* `results/placement_seed0.json`
* `results/wallclock.json`
* `results/metrics.json` (15 variants)
* `results/derived_quantities.json`
* `results/images/*.png` (353 plots)

## Verification

| Verificator | Result |
| --- | --- |
| `verify_library_asset.py minimal_dsgc_tonic_gaba_sweep` | PASS (0 errors / 0 warnings) |
| `verify_task_metrics.py t0057_tonic_gaba_sweep_t0053` | PASS (0 / 0) |
| `ruff check tasks/t0057_tonic_gaba_sweep_t0053/code/` | PASS |
| `mypy -p tasks.t0057_tonic_gaba_sweep_t0053.code` | PASS (no issues) |
| `test_gaba_tonic_envelope.py` (REQ-13 IPSP-sustained-window) | PASS |
| `test_placement_seed0_match.py` (placement bit-identical to t0053) | PASS |
| `test_quiescent_rest.py` (V_rest = -65 mV ± 0.5 mV) | PASS |
| `test_spatial_gating.py` (centripetal-gating predicate) | PASS |
| AMPA_ONLY 0.667 Hz regression sentinel (REQ-14) | PASS at all 5 conductances |
| Active-fraction soft sanity (mean ∈ [0.4, 0.6]) | PASS (mean = 0.500) |

## Examples

### Example 1: One trial in the single-spike regime (gaba = 1.0 nS, θ = 0°, trial 0)

* **Input**: bar at 0° sweeping at 1.0 µm/ms across the dendritic field; tonic GABA active on
  the centripetal-half synapses (`cos(0 - theta_centrifugal) < 0`, ≈ 36% of 100 I synapses for
  this direction) at `g = 1.0 nS, t_on = 100 ms, t_off = 1400 ms`. AMPA fires once per E
  synapse at `t_onset = (x*cos(0) + y*sin(0)) / 1.0 + 100 ms`.
* **Output (raw)**: 1 spike at t ≈ 250 ms (recorded in `spike_times_full.csv` row
  `gaba_base_ns=1.0, angle_deg=0, trial_index=0`); firing rate = 0.667 Hz over 1500 ms. Soma
  voltage trace shows the spike in `images/voltage_full_gaba_1.00_dir_000.png`.

### Example 2: One trial in the suppressed regime (gaba = 2.0 nS, θ = 0°, trial 0)

* **Input**: bar at 0° sweeping at 1.0 µm/ms across the dendritic field; tonic GABA active on
  the centripetal-half synapses at `g = 2.0 nS, t_on = 100 ms, t_off = 1400 ms`.
* **Output (raw)**: 0 spikes (recorded in `spike_times_full.csv` row `gaba_base_ns=2.0,
  angle_deg=0, trial_index=0`); firing rate = 0.0 Hz over 1500 ms. Soma voltage trace shows
  the cell held below threshold in `images/voltage_full_gaba_2.00_dir_000.png`.

### Example 3: AMPA_ONLY mode (gaba = 1.0 nS, θ = 90°, trial 0)

* **Input**: bar at 90° sweeping at 1.0 µm/ms; AMPA fires per-position; GABA disabled
  (`AMPA_ONLY` mode sets all `gaba_syn.g = 0`).
* **Output (raw)**: 1 spike at t ≈ 350 ms (recorded in `spike_times_ampa_only.csv` row
  `gaba_base_ns=1.0, angle_deg=90, trial_index=0`); firing rate = 0.667 Hz. Bit-identical to
  t0052 / t0053 AMPA_ONLY results — REQ-14 regression sentinel.

### Example 4: GABA_ONLY mode (gaba = 1.5 nS, θ = 210°, trial 0)

* **Input**: bar at 210° sweeping at 1.0 µm/ms; AMPA disabled (`GABA_ONLY` mode sets all
  `ampa_netcon.weight[0] = 0`); tonic GABA active on the maximally-active half of synapses
  (active-fraction = 0.66 for this direction).
* **Output (raw)**: 0 spikes (recorded in `spike_times_gaba_only.csv` row `gaba_base_ns=1.5,
  angle_deg=210, trial_index=0`); firing rate = 0.0 Hz. Sanity check: inhibition without
  excitation produces no firing, as expected.

### Example 5: Per-pair tonic GABA configuration

The per-trial schedule writes `gaba_syn.g` directly. For each `pair`, the FULL-mode setup at
gaba = 1.0 nS, θ = 0° is:

```python
# In schedule_ei_onsets, for an active synapse (pair_index = 7, theta_centrifugal = 175°):
pair.gaba_syn.g = 1.0e-3  # 1.0 nS as microsiemens
pair.gaba_syn.t_on = 100.0  # ms
pair.gaba_syn.t_off = 1400.0  # ms
# For a silent synapse (pair_index = 12, theta_centrifugal = 10°):
pair.gaba_syn.g = 0.0
```

The `gaba_tonic` mechanism (in `code/mod/GabaTonic.mod`) implements:

```
g_actual(t) = g * envelope(t, t_on, t_off, ramp_ms)
i_syn = g_actual * (v - e)
```

where `envelope` is 0 outside `[t_on, t_off]`, 1 in the interior, and a 1-2 ms cosine ramp at
each edge.

## Task Requirement Coverage

> **Operative task text (from task.json)**: "Replace t0053's per-event Exp2Syn GABA with a tonic
> conductance gated by stimulus window; sweep per-synapse peak conductance to recover non-zero
> FULL-mode tuning curves."
>
> **Resolved long description**: see `task_description.md`. The task description specifies the tonic
> mechanism (`gaba_tonic.mod` with `(g, e, t_on, t_off)`), the sweep grid
> (`{0.25, 0.5, 1.0, 1.5, 2.0}` nS), the spatial centripetal-gating preservation, the library asset
> deliverable, and the verification criteria.

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Build `gaba_tonic.mod` POINT_PROCESS with `(g, e, t_on, t_off)`, sustained `g` between `t_on` and `t_off`, reversal `e = -75 mV`, optional cosine ramp | **Done** | `code/mod/GabaTonic.mod` + compiled `nrnmech.dll`; `test_gaba_tonic_envelope.py` PASS |
| REQ-2 | Compile and load via `run_nrnivmodl.cmd` shim and `ensure_gaba_tonic_compiled()` bootstrap | **Done** | `code/run_nrnivmodl.cmd`, `code/neuron_bootstrap.py`; sweep ran end-to-end |
| REQ-3 | Drop-in replacement: each E/I pair gets one `gaba_tonic` instance (no NetStim/NetCon GABA plumbing) | **Done** | `code/synapses.py` lines 121-180 — direct attribute writes |
| REQ-4 | Spatial centripetal-gating predicate from t0053 preserved bit-for-bit | **Done** | `i_synapse_fires` in `synapses.py` matches t0053; `test_spatial_gating.py` PASS; active-fraction polar matches t0053 |
| REQ-5 | Same fixed placement seed (0); bit-identical `placement_seed0.json` | **Done** | `test_placement_seed0_match.py` PASS |
| REQ-6 | AMPA mechanism unchanged from t0053 | **Done** | AMPA construction in `synapses.py` matches t0053; AMPA_ONLY peak Hz = 0.667 across all directions |
| REQ-7 | Sweep `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS x 12 dir x 10 trials x 3 modes = 1800 trials | **Done** | `tuning_curve_*.csv` contain 60 rows each (5 x 12); 1800 spike-times rows total; wallclock.json shows 1800 trials |
| REQ-8 | Library asset `minimal_dsgc_tonic_gaba_sweep` registered with `GABA_BASE_NS` exposed | **Done** | `assets/library/minimal_dsgc_tonic_gaba_sweep/details.json` + `description.md`; library verificator PASS 0/0 |
| REQ-9 | Per-conductance: 12 PNGs of soma V(t), EPSP, IPSP, PSTH, synapse activation, plus polar tuning curve | **Done** | 305 per-conductance PNGs in `results/images/` |
| REQ-10 | Active-fraction polar plot carried over from t0053 | **Done** | `results/images/active_fraction_polar.png` matches t0053 0.34-0.66 modulation |
| REQ-11 | Cross-conductance summary plots (DSI primary, DSI vector-sum, peak Hz, null Hz, HWHM, RMSE vs `GABA_BASE_NS`) | **Done** | 6 cross-conductance summary PNGs in `results/images/` |
| REQ-12 | Per-conductance metrics with primary DSI, vector-sum DSI, preferred direction, peak Hz, null Hz, HWHM, RMSE | **Done** | `results/metrics.json` (15 variants) + `derived_quantities.json` (per-conductance arrays) |
| REQ-13 | IPSP-sustained-window regression: IPSP at t = 1300 ms ≥ 50% of IPSP at t = 200 ms in the most-active direction | **Done** | `test_gaba_tonic_envelope.py` PASS at all 5 conductances |
| REQ-14 | AMPA_ONLY 0.667 Hz uniform peak rate regression | **Done** | `compute_metrics.py` regression line: PASS at all 5 conductances |
| REQ-15 | Tonic mechanism uses `(t_on, t_off) = (100 ms, 1400 ms)` per active synapse | **Done** | `constants.py`: `T_ON_MS = 100.0`, `T_OFF_MS = 1400.0`; `synapses.py` writes these per pair |
| REQ-16 | Direct head-to-head against t0053 at 2 nS — does the tonic mechanism produce non-zero firing? | **Done** (negative result) | `gaba_2.00_full` variant: peak = null = 0 Hz, primary DSI = null. The tonic mechanism is more suppressive than t0053's transient at this amplitude |
| REQ-17 | Cross-conductance peak Hz vs t0004 target — does any swept value land within order of magnitude of 32 Hz? | **Done** (negative result) | `derived_quantities.json` `peak_hz_vs_gaba`: max value 0.667 Hz, ~48x below target 32 Hz |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0057_tonic_gaba_sweep_t0053" date_compared: "2026-04-28" ---
# Comparison with Published Results

## Summary

The tonic-GABA sweep over `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS on the t0053 spatial
DSGC fails to recover any non-trivial direction selectivity. FULL-mode primary DSI is
**0.000** at every swept conductance: the cell either fires uniformly at **0.667 Hz** across
all 12 directions (`gaba <= 1.0 nS`, the AMPA-only single-spike-per-trial regime) or is fully
suppressed at **0.0 Hz** (`gaba >= 1.5 nS`). This is a wider negative result than the t0053
sibling: at the matched 2 nS operating point the tonic mechanism is **more** suppressive than
t0053's per-event Exp2Syn (both land at 0 Hz, but the tonic IPSP envelope persists for 1300 ms
vs t0053's ~80 ms decay tail). Vector-sum DSI is **0.000** (numerical floor 3.2e-17)
everywhere — well below the in vitro mouse On-Off DSGC band of **0.65 +/- 0.05** [Park2014, p.
3978], the PolegPolsky2016 voltage-dependent NMDA model output of **0.46** [PolegPolsky2016,
Fig 5], and the deRosenroll2026 correlated AR(2) benchmark of **0.39** [deRosenroll2026, Fig
5]. The active-fraction polar curve (0.34 -> 0.66) is bit-identical to t0053, confirming the
spatial centripetal-gating mechanism is intact and the failure is amplitude calibration
interacting with the new sustained-window mechanism, not the gating rule.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Park2014 (CART-Cre, voltage-clamp) | DSI (primary) | 0.65 | 0.000 | -0.65 | In vitro mouse On-Off DSGCs, n=14; FULL-mode degenerate (peak = null = 0.667 Hz at gaba <= 1.0 nS or 0 Hz at gaba >= 1.5 nS) at all 5 swept conductances [Park2014, p. 3978] |
| Park2014 (TRHR-GFP / wild-type) | DSI (primary) | 0.73 | 0.000 | -0.73 | Reference subset, n=38 cells; FULL-mode degenerate at all 5 swept conductances [Park2014, p. 3978] |
| PolegPolsky2016 (voltage-dependent NMDA + tuned GABA) | DSI | 0.46 | 0.000 | -0.46 | Their NEURON DSGC with Mg-block NMDA preserves DSI; ours is AMPA-only with tonic GABA and degenerates at every operating point [PolegPolsky2016, Fig 5] |
| deRosenroll2026 (correlated AR(2) release) | DSI (vector-sum) | 0.39 | 3.2e-17 | -0.39 | Vector-sum DSI vs paper's vector-sum benchmark; rho=0.6; our value is at the floating-point noise floor [deRosenroll2026, p. 6 / Fig 5] |
| deRosenroll2026 (uncorrelated release) | DSI (vector-sum) | 0.25 | 3.2e-17 | -0.25 | Lower-bound model benchmark; we lack release noise entirely [deRosenroll2026, p. 6 / Fig 5] |
| t0004 target curve (this project) | Peak rate (Hz) | 32.0 | 0.667 | -31.33 | Our peak rate is at most **48x below** the project target across the entire sweep; at gaba >= 1.5 nS it drops to 0 Hz [t0004 results_summary] |
| t0004 target curve (this project) | DSI | 0.8824 | 0.000 | -0.8824 | Project canonical target; FULL-mode degenerate [t0004 results_summary] |
| t0004 target curve (this project) | HWHM (deg) | 68.51 | 180.0 | +111.49 | Tuning curve is uniform (gaba <= 1.0 nS) — HWHM degenerates to 180 deg, vs target 68.51 deg [t0004 results_summary] |
| t0004 target curve (this project) | Tuning curve RMSE (Hz) | 0.0 (self) | 16.67 | +16.67 | gaba <= 1.0 nS RMSE; dominated by 32 Hz target peak vs 0.667 Hz model response [results_detailed.md] |
| Park2014 (null inhibitory conductance, P-N) | Inhibitory P-N (nS) | 2.43 | 1.5 | -0.93 | Per-direction effective P-N for the tonic mechanism: at gaba = 1.5 nS, ratio of (active@theta=210) - (active@theta=30) = (0.66 - 0.34) * 1.5 nS = 0.48 nS per synapse times 100 = ~48 nS aggregate, but voltage-side IPSP modulation is only 1.22x (7.38 mV / 6.05 mV) due to driving-force saturation [Park2014, p. 3978] |
| PolegPolsky2016 (Fig 1, control PD PSP) | PD PSP (mV) | 5.8 | 6.05 | +0.25 | Aggregate IPSP at preferred-side direction (theta=30 deg, minimum-active-fraction direction) at gaba = 1.5 nS; paper value is excitatory NMDA-PSP, ours is inhibitory IPSP — order-of-magnitude similar [PolegPolsky2016, p. 1280, Fig 1] |
| PolegPolsky2016 (Fig 1, control ND PSP) | ND PSP (mV) | 3.3 | 7.38 | +4.08 | Aggregate IPSP at null-side (theta=210 deg, max-active-fraction direction) at gaba = 1.5 nS; paper value is excitatory NMDA, ours is inhibitory IPSP — sign and mechanism differ [PolegPolsky2016, p. 1280, Fig 1] |

### Prior Task Comparison

| Prior Task | Variant | Primary DSI | Peak Hz | HWHM (deg) | Notes |
| --- | --- | --- | --- | --- | --- |
| t0052 (parent, scalar gabaMOD) | FULL | **1.000** | **0.667** | **82.5** | Single-spike-per-trial; perfect on/off binary tuning. Mean GABA mass 66 nS per trial. |
| t0053 (sibling, spatial Exp2Syn at 2 nS) | FULL | **0.000** | **0.000** | **180.0 (degen.)** | Fully suppressed by 100 nS mean GABA mass. Same morphology and placement seed as t0052. |
| t0054 (NMDA + scalar gabaMOD, gNMDA = 0.25 nS) | FULL | **0.143** | **8.000** | n/a | NMDA closes 12x of peak-rate gap but DSI collapses ~9x vs t0052. Voltage-independent NMDA. |
| t0054 (NMDA + scalar gabaMOD, gNMDA = 1.0 nS) | FULL | **0.000** | **4.667** | n/a | DSI collapses to zero entirely; the cell becomes direction-blind. |
| t0057 (this task, tonic GABA at 0.25 nS) | FULL | **0.000** | **0.667** | **180.0 (degen.)** | Tonic too weak to override single AMPA spike — uniform single-spike regime. |
| t0057 (this task, tonic GABA at 0.50 nS) | FULL | **0.000** | **0.667** | **180.0 (degen.)** | Same single-spike regime. |
| t0057 (this task, tonic GABA at 1.00 nS) | FULL | **0.000** | **0.667** | **180.0 (degen.)** | Same single-spike regime. |
| t0057 (this task, tonic GABA at 1.50 nS) | FULL | **null** | **0.000** | **null** | Step into full suppression — IPSP envelope 7.38 mV crosses the spike-veto threshold. |
| t0057 (this task, tonic GABA at 2.00 nS) | FULL | **null** | **0.000** | **null** | Fully suppressed; matches t0053's 2 nS suppression but via the persistent envelope. |

## Methodology Differences

* **Inhibition mechanism (vs t0053 sibling)**: t0053 uses per-event `Exp2Syn` GABA (rise 1 ms,
  decay 20 ms, e = -75 mV) fired once per active synapse at the bar-arrival time, so the
  conductance envelope is on for only ~100-200 ms per trial. t0057 replaces this with a new
  `gaba_tonic.mod` POINT_PROCESS that holds `g = GABA_BASE_NS` over the entire `(t_on, t_off)
  = (100 ms, 1400 ms)` stimulus window for active synapses (1300 ms sustained vs t0053's ~80
  ms decay tail). At matched 2 nS amplitude the tonic mechanism delivers **~16x more total
  inhibitory charge** than the per-event mechanism — and lands at the same 0 Hz suppression
  because both exceed the spike-veto threshold.

* **Inhibition mechanism (vs t0052 parent)**: t0052 modulates every I synapse's amplitude by a
  global direction-dependent scalar `gabaMOD(theta) = 0.33 + 0.66 * (1 - cos(theta -
  theta_PD)) / 2` applied uniformly to all 100 synapses for one Exp2Syn event per trial. t0057
  instead activates a binary subset of synapses (centripetal half) at full `GABA_BASE_NS`
  amplitude, sustained over the entire trial. Mean total GABA *charge* per trial is much
  larger in t0057 (0.25-2.0 nS x 50 syn x 1300 ms vs 0.66 nS x 100 syn x ~30 ms in t0052) — at
  the lower end of the sweep the active-fraction modulation cannot generate enough
  differential charge to break the binary AMPA-spike decision, while at the upper end the cell
  is held below threshold throughout.

* **Inhibition mechanism (vs Park2014)**: Park2014 [p. 3978] attributes DS to null-direction
  GABA from SACs (whole-cell P-N = 2.43 nS). The centripetal-gating predicate approximates the
  SAC network's centrifugal preference at the SAC-output level. The new tonic envelope is a
  closer match to the **biological SAC->DSGC IPSC envelope of 100-300 ms** than t0053's 20 ms
  Exp2Syn decay, but our 1300 ms persistence is **far longer** than even the slowest published
  SAC IPSC envelopes — biologically wrong in the opposite direction from t0053.

* **Inhibition mechanism (vs PolegPolsky2016)**: PolegPolsky2016 [p. 1280, Methods] uses a
  multi-event SAC->DSGC GABA driver with realistic envelope tau ~50-150 ms; we use a single
  tonic pulse (Brainstorm-10 explicitly chose this simplest "always-on during stimulus" Option
  C). The PolegPolsky2016 model also includes voltage-dependent NMDA Mg-block which preserves
  DSI multiplicatively; our model is AMPA-only.

* **Synapse count**: 100 E + 100 I (this task, t0052, t0053, t0054) vs ~177 in PolegPolsky2016
  [p. 1280] / 282 in t0046 reproduction / >1000 SAC varicosities in deRosenroll2026 [p. 5].
  Lower synapse count gives weaker total drive but does not by itself explain the 0-Hz FULL
  result — AMPA_ONLY produces the same 0.667 Hz at all 5 swept conductances.

* **Excitation tuning**: Park2014 [p. 3978] proves bipolar-cell glutamate is omnidirectional
  at release. Our model implements omnidirectional AMPA exactly as Park2014 prescribes — and
  AMPA_ONLY produces 0.667 Hz uniformly across all 12 directions at every conductance,
  confirming this is bit-identical to t0052/t0053 and the DSI degeneration is purely an
  inhibition-mechanism effect.

* **No NMDA**: Our model has AMPA only by design. PolegPolsky2016 emphasises NMDARs contribute
  multiplicatively at PD (5.8 mV / ~35% of total PSP). t0054 has shown that adding *voltage-
  independent* NMDA breaks DSI; PolegPolsky2016's voltage-*dependent* NMDA Mg-block is the
  identified path forward but is excluded from this task's scope.

* **No noise**: Trials are deterministic single-event-per-synapse; deRosenroll2026 [p. 6]
  requires AR(2) correlated release with rho = 0.6 to match in vitro. Reliability = 1.0 here
  is artefactual.

* **Sustained-window vs pulse-event timing**: This is the headline new methodology choice
  unique to t0057. The 1300 ms tonic window keeps the active half of synapses delivering full
  conductance for the entire stimulus presentation. The IPSP-sustained-window regression test
  (`test_gaba_tonic_envelope.py`) confirms IPSP voltage at t = 1300 ms is at least 50% of IPSP
  voltage at t = 200 ms — i.e., the new mechanism does deliver the designed envelope. The
  biological interpretation is that this is a "what if real SAC->DSGC IPSCs were perfectly
  sustained over the stimulus?" upper bound, not a faithful reproduction of multi-event SAC
  release kinetics.

* **DSI definition**: Park2014 uses primary DSI on AP counts; deRosenroll2026 uses vector-sum
  DSI on spike counts. Both versions are degenerate in our FULL mode (peak = null at every
  swept point).

## Analysis

### Headline negative finding: the entire sweep grid is degenerate

The tonic-GABA mechanism with `(t_on, t_off) = (100 ms, 1400 ms)` produces **zero meaningful
direction selectivity** across the swept range `{0.25, 0.5, 1.0, 1.5, 2.0}` nS. Below 1.5 nS
the tonic conductance is too weak to override the single AMPA-driven spike per trial (peak =
null = **0.667 Hz**, identical to AMPA_ONLY); at 1.5 nS and above the IPSP envelope (peak
depolarization **7.38 mV** at theta = 210 deg, GABA reversal -75 mV) crosses the
threshold-veto boundary and the cell stops firing entirely (peak = null = **0 Hz**). The gap
between the two regimes is binary: there is no `GABA_BASE_NS` value in the swept grid where
the cell fires *some* but not *all* of its otherwise-uniform single-spike responses. The
**-0.65** to **-0.73** delta against the in vitro Park2014 band is therefore a delta against a
fully-suppressed or uniformly-firing model, not a partially-suppressed model with a non-zero
null and peak. The negative result is wider than t0053's single-amplitude failure: the entire
8x conductance range fails for the same underlying reason.

### The tonic mechanism is more suppressive than t0053 at matched amplitude

At the matched 2 nS operating point, the tonic mechanism produces **0 Hz** in FULL mode — the
same fully-suppressed result as t0053's per-event Exp2Syn GABA. But the route to suppression
is different: t0053 delivers a brief, sharp shunt within ~100 ms of bar arrival; t0057 holds
the same amplitude shunt across the entire 1300 ms window. The peak somatic IPSP voltage at
theta = 210 deg grows from **3.17 mV** at 0.25 nS to **7.87 mV** at 2 nS — sub-linear (8x
conductance ratio yields 2.5x voltage ratio), confirming the same driving-force-saturation
mechanism documented in t0052 (1.54x voltage from 3.0x conductance) and t0053 (1.24x voltage
from 1.94x active-count ratio). The matched-amplitude head-to-head therefore does not produce
the timing-mechanism-isolation comparison that motivated the task — both mechanisms exceed the
spike-veto threshold at 2 nS and the tonic mechanism gets there sooner because of its
sustained envelope.

### Spatial gating intact; failure is amplitude calibration

The active-fraction polar curve (**0.34** at theta = 30 deg to **0.66** at theta = 210 deg,
mean **0.500**) is **bit-identical to t0053** because the centripetal-gating rule
`cos(theta_stim - theta_centrifugal_synapse) < 0` is unchanged. This is direct evidence that
the gating mechanism continues to work as designed — the failure is in the inhibition
*amplitude* that gates onto a single-spike-per-trial AMPA regime that cannot produce graded
direction-dependent firing rates. The four-way table below maps the parameter regime:

| Inhibition driver | t0052 (scalar gabaMOD) | t0053 (Exp2Syn 2 nS) | t0057 (tonic 0.25-1.0 nS) | t0057 (tonic 1.5-2.0 nS) |
| --- | --- | --- | --- | --- |
| Mean GABA mass per trial | 66 nS x 30 ms | 100 nS x 80 ms | 12.5-50 nS x 1300 ms | 75-100 nS x 1300 ms |
| Cell regime | Single-spike PD / silent ND | Suppressed everywhere | Uniform single-spike | Suppressed everywhere |
| Primary DSI | 1.000 (degenerate) | 0.000 (degenerate) | 0.000 (degenerate) | null (degenerate) |

### The single-spike-per-trial AMPA regime is the deeper bottleneck

t0057, t0053, and t0052 all fire **at most one spike per trial** at the highest-active
direction under the chosen AMPA conductance (0.5 nS per synapse, 100 synapses). Once the cell
is in this regime, no inhibition mechanism — graded scalar amplitude (t0052), spatial Exp2Syn
pulse (t0053), or sustained tonic conductance (t0057) — can produce a graded
direction-dependent firing rate. The decision is binary: spike fires or it does not. Direction
selectivity in the published literature requires a multi-spike-per-trial regime, which t0054
partially achieves with NMDA (8 Hz peak at gNMDA = 0.25 nS) but at the cost of DSI collapse
under voltage-independent kinetics. The path forward is therefore to **escape the single-spike
regime first** (via higher AMPA, NMDA with Mg-block, or both) and **then re-test inhibition
mechanisms** in the multi-spike regime where a graded suppression can produce graded
selectivity.

### IPSP envelope grows sub-linearly with conductance (driving-force saturation)

The aggregate IPSP voltage envelope at theta = 210 deg (max-active direction) grows from
**3.17 mV** at 0.25 nS to **7.87 mV** at 2 nS — a **2.5x voltage ratio** for an **8x
conductance ratio**. This is the same driving-force saturation observed in t0052 and t0053 but
in a different regime: the IPSP envelope here is sustained over 1300 ms instead of decaying
within 80-100 ms, so the voltage spends more time near E_GABA = -75 mV and the additional
conductance produces ever-smaller voltage suppression. The implication is that **sustained
inhibition mechanisms hit the driving-force ceiling sooner than pulse-event mechanisms at
matched amplitude** — t0057 lands at full suppression at 1.5 nS, while t0053's pulse-event
mechanism would presumably need somewhat higher conductance to reach the same suppression
level (untested in the t0053 sweep).

### Convergence with PolegPolsky2016 prediction

PolegPolsky2016 [p. 1283-1284] argues that voltage-dependent NMDA Mg-block is necessary for
multiplicative DSI scaling, and that subtractive inhibition alone cannot produce the in vivo
DSI band. Our cumulative evidence (t0052 trivial DSI in single-spike regime, t0053 spatial
inhibition suppresses everything at 2 nS, t0054 DSI collapses under voltage-independent NMDA,
and now t0057 no operating point in an 8x sweep produces non-trivial DSI) converges on the
same conclusion: **no AMPA-only minimal DSGC operating in the single-spike-per-trial regime
can reach the Park2014/deRosenroll2026/PolegPolsky2016 DSI band**, regardless of the
inhibition mechanism's spatial or temporal profile. The minimal model is missing the
multiplicative-NMDA ingredient.

## Limitations

* **Coarse sweep grid**: 5 conductance values, all at or above 0.25 nS. The sub-0.25 nS regime
  (where the tonic mechanism might produce graded suppression rather than the binary
  single-spike-vs-zero) is not characterised. A finer grid (e.g., 0.05, 0.10, 0.15, 0.20, 0.25
  nS) would test whether any tonic operating point exists below the AMPA-spike-veto threshold.

* **FULL-mode is degenerate at every swept point**: primary DSI is 0.000 or null at all 5
  conductances because peak = null. Vector-sum DSI is at the floating-point noise floor
  3.2e-17 (sub-1.5 nS) or exactly 0.0 (suppressed). All comparisons against published DSI
  values are therefore comparisons to a fully-suppressed or uniformly-firing model, not a
  partially- suppressed model with a meaningful peak/null contrast.

* **Tonic envelope is biologically extreme**: the 1300 ms `(t_on, t_off)` window is far longer
  than any published SAC->DSGC IPSC envelope (typical 100-300 ms). Brainstorm-10 explicitly
  chose this simplest "always-on during stimulus" model with the understanding that biological
  realism would be revisited if results justified it. The tonic mechanism is therefore an
  upper-bound test of "what if SAC inhibition were perfectly sustained?" rather than a
  faithful biological model.

* **No noise**: Trials are deterministic; deRosenroll2026 emphasises DSI is sensitive to
  release decorrelation (0.39 -> 0.25). Our protocol cannot test this; reliability would be
  artefactually 1.0 even if the cell spiked.

* **No NMDA**: AMPA-only by design (matching t0053 parent). The most likely path to a
  non-degenerate DSI is voltage-dependent NMDA Mg-block (cf. PolegPolsky2016 [Fig 5] and t0054
  results). The tonic-GABA + Mg-block-NMDA combination is left for a follow-up.

* **Park2014 in vivo DSI band** in earlier orchestrator messages ("0.40-0.60") could not be
  verified from the paper text. The paper reports CART-Cre cells DSI = 0.65 +/- 0.05 (n = 14)
  and TRHR-GFP / wild-type cells 0.73 +/- 0.03 (n = 38) [Park2014, p. 3978]. We use the values
  directly attributable to Park2014.

* **deRosenroll2026 DSI of 0.39** is a model output, not an in vivo measurement; it is the
  correlated AR(2) release benchmark that any reimplementation should match, not a direct
  comparison to physiology. Used as the closest comparable published model in the project
  corpus.

* **PolegPolsky2016 DSI under voltage-dependent NMDA** of **0.46** is read from their Figure 5
  voltage-dependent NMDA + tuned GABA panel. The paper does not publish a single headline DSI
  number, so this value should be treated as a representative model output rather than a
  precise benchmark.

* **Voltage-side ratios (1.22x at 1.5 nS, 2.5x across the full sweep) lack a direct literature
  anchor**: driving-force saturation is consistent qualitatively with PolegPolsky2016's
  multiplicative-vs-additive shunting framework [p. 1283] but the specific numerical mapping
  is not published in the project corpus.

* **Active-fraction polar curve has no direct published counterpart**: published SAC-network
  models (deRosenroll2026, Park2014) report aggregate GABA conductance modulation, not a
  per-direction count of active SAC outputs at the DSGC. The 0.34 - 0.66 modulation reported
  here is a model-internal observable rather than a literature-comparable measurement.

* **Synapse-count regime mismatch**: 100 vs 177 (PolegPolsky2016) vs 282 (t0046) vs >1000
  (deRosenroll2026) is a >10x range. Per-synapse parameters cannot be directly compared
  without total-conductance normalisation.

* **Single-spike-per-trial AMPA regime is the underlying problem**: the cell at this AMPA
  conductance (0.5 nS x 100 synapses) fires at most one spike per direction. This binary
  regime cannot produce meaningful DSI under any inhibition mechanism (scalar gabaMOD as in
  t0052, spatial Exp2Syn as in t0053, tonic as in t0057) — they all collapse to either
  1-spike-uniform or 0-spike-uniform. The path forward (S-0052-01) is to first escape the
  single-spike regime via higher AMPA conductance and then re-evaluate inhibition mechanisms
  in the multi-spike regime.

</details>
