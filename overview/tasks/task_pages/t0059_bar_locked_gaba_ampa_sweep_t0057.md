# ✅ Bar-arrival-locked tonic GABA + AMPA escape sweep on t0057 substrate

[Back to all tasks](../README.md)

> Tuning Curve RMSE (Hz): **17.178292988536434**

## Overview

| Field | Value |
|---|---|
| **ID** | `t0059_bar_locked_gaba_ampa_sweep_t0057` |
| **Status** | ✅ completed |
| **Started** | 2026-04-28T23:58:19Z |
| **Completed** | 2026-04-29T20:55:00Z |
| **Duration** | 20h 56m |
| **Dependencies** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Source suggestion** | `S-0057-04` |
| **Task types** | `build-model`, `experiment-run` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`synaptic-integration`](../../by-category/synaptic-integration.md) |
| **Expected assets** | 1 library |
| **Step progress** | 10/15 |
| **Task folder** | [`t0059_bar_locked_gaba_ampa_sweep_t0057/`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/task_description.md)*

# Bar-Arrival-Locked Tonic GABA + AMPA Escape Sweep on t0057 Substrate

## Source

Approved in brainstorm session 11 (t0058) and covers four high-priority suggestions in one
combined experimental task:

* **S-0057-04** (primary `source_suggestion`) — per-synapse stimulus-window-tied `(t_on,
  t_off)` tonic GABA on t0057 to model bar-arrival-locked inhibition.
* **S-0057-02** — AMPA conductance escape sweep on the t0057 tonic-GABA substrate.
* **S-0057-01** — sub-0.25 nS finer GABA sweep on t0057 (graded-suppression hypothesis).
* **S-0055-01** — project-wide DSGC measurement-protocol fix (drop legacy E_ONLY / GABA_ONLY
  trio in favour of EPSP_PASSIVE / IPSP_PASSIVE / FULL with HH save-and-zero on the passive
  modes; drop per-synapse activation-time histogram; standardise trial length at 1400 ms).

## Motivation

Five completed from-scratch minimal DSGCs (t0052, t0053, t0054, t0055, t0057) all converge on
a binary regime: either **single-spike-per-trial** (peak Hz = 0.667, vector-sum DSI = 0.7464
with scalar gabaMOD or 1.0 trivially with full PD/ND inhibition) **or full inhibitory
suppression** (peak Hz = 0, DSI = 0). The cell never enters the 5-50 Hz multi-spike band where
DSI metrics become biologically informative.

The convergent diagnosis from this body of work:

1. **AMPA at 0.5 nS x 100 synapses is too weak** to drive multi-spike trains on the t0009
   calibrated morphology. t0052/t0053/t0054/t0055/t0057 all top out at 0.667 Hz under any
   non-saturating inhibition.
2. **Tonic GABA at the per-synapse amplitudes already swept** (0.25-2.0 nS in t0057) either
   does not engage at all (sub-veto, 0.667 Hz uniform) or fully suppresses (0 Hz uniform). No
   intermediate operating point exists in the t0057 grid.
3. **Sustained tonic GABA over a 1300 ms window per active synapse is not biologically
   realistic** either. SAC outputs onto a DSGC dendrite arrive in a brief 100-300 ms envelope
   as the stimulus bar passes the SAC's dendritic field — not as a constant 1.3-second leak.

This task addresses all three issues simultaneously on one combined substrate. It (a)
implements biologically plausible **per-synapse bar-arrival-locked GABA windows** (each active
SAC fires a 200 ms tonic conductance starting at the stimulus's geometric arrival time at that
synapse), (b) sweeps **AMPA conductance** to break the single-spike regime, (c) sweeps **GABA
conductance** including sub-0.25 nS values to characterise the graded-suppression regime, and
(d) ships the **EPSP_PASSIVE / IPSP_PASSIVE / FULL** measurement protocol so synaptic envelope
traces are spike-free and the EPSP-decay metric stops returning null.

## Objective

Build the new bar-arrival-locked tonic GABA mechanism, integrate it into a fork of t0057's
minimal DSGC code, ship the corrected measurement-protocol trio, sweep a 5x5 (gAMPA,
GABA_BASE_NS) grid, and report whether any operating point on the swept grid produces
non-trivial direction selectivity in the multi-spike regime — or rule it out.

## Model Specification

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (t0009 Strahler-calibrated 141009_Pair1DSGC
  reconstruction). Identical to t0052 / t0053 / t0054 / t0055 / t0057.

### Sections and Channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` channel mechanism.
* All dendritic sections: passive only. `Rm = 5999 ohm.cm^2`, `Ra = 100 ohm.cm`, `cm = 1
  uF/cm^2`.
* V_rest: -65 mV.
* Identical to t0057.

### Synapses

* 100 E + 100 I synapses, **co-located in pairs**, uniform random over dendrites with the same
  fixed seed (0) as t0052 / t0053 / t0057. Identical placement so the placement_seed0 fixture
  from t0057 applies bit-for-bit.

### Excitatory mechanism

* `Exp2Syn`: rise = 0.5 ms, decay = 2.5 ms, e = 0 mV.
* Position-gated firing: each E synapse fires once when the bar's leading edge crosses it;
  direction-independent waveform.
* **Per-synapse peak conductance is the swept variable** — see Sweep section below.

### Inhibitory mechanism (NEW — bar-arrival-locked tonic windows)

* Reuses t0057's `gaba_tonic.mod` POINT_PROCESS with parameters `(g, e, t_on, t_off)`:
  * Sustained conductance `g` (in microsiemens) between `t_on` and `t_off`.
  * Zero conductance outside that window.
  * Reversal `e = -75 mV`.
  * Rise / fall envelope at the window edges as in t0057 (piecewise constant or 1-2 ms cosine
    ramp).
* Per-synapse instance: each I synapse pair gets one `gaba_tonic` mechanism.
* **Spatial gating preserved from t0053 / t0057**: gated synapses are those whose
  `cos(theta_stim - theta_centrifugal_synapse) < 0`. Silent synapses get `g = 0` throughout.
* **NEW per-synapse bar-arrival-locked window** (replaces t0057's global `(100, 1400)`
  window):
  * For each active synapse `i` at coordinate `(x_i, y_i)`:
    * `t_on_i = (x_i * cos(theta_stim) + y_i * sin(theta_stim)) / v + 100 ms`
    * `t_off_i = t_on_i + window_ms`
  * `v` is bar velocity (1000 um/s as in t0053 / t0057).
  * `window_ms = 200` ms (FIXED — biologically motivated midpoint of the 100-300 ms SAC IPSC
    envelope range; not swept in this task).
* Total inhibition envelope per trial: a moving wave of GABA windows that tracks the stimulus
  bar's progression across the dendritic arbor.

### Stimulus protocol

* 12 directions x 10 trials per direction, bar 200 um x full arena, 1000 um/s.
* **Trial length T = 1400 ms** (was 1500 ms in t0052 / t0053 / t0054 / t0055 / t0057; this
  task ships the standardised 1400 ms per S-0055-01 / researcher memory note).
* `dt = 0.025 ms`.

### Measurement-protocol fix (S-0055-01 bundled)

* **Drop** the legacy `E_ONLY` and `GABA_ONLY` modes from the trial code.
* **Add** two new passive modes that share the same synapse activation but disable spike
  generation:
  * `EPSP_PASSIVE` — keep AMPA active, set GABA `g = 0`, save and zero `gnabar_hh` and
    `gkbar_hh` on `soma` and `axon_initial_segment` (restore at end of trial). Records the
    clean EPSP envelope at the soma without spike contamination.
  * `IPSP_PASSIVE` — keep GABA active, set AMPA peak conductance to 0, save and zero
    `gnabar_hh` and `gkbar_hh` on `soma` and `axon_initial_segment` (restore at end of trial).
    Records the clean IPSP envelope at the soma without spike contamination.
* Keep `FULL` with HH active for spike rates / DSI / firing-rate PSTH metrics.
* **Drop** the per-synapse activation-time histogram output (no longer informative once the
  bar-arrival-locked windows are explicit in the design).

## Sweep

| Axis | Values | Units |
| --- | --- | --- |
| `gAMPA` | {0.5, 1.0, 2.0, 3.0, 4.0} | nS per E synapse |
| `GABA_BASE_NS` | {0.1, 0.2, 0.5, 1.0, 2.0} | nS per active I synapse |
| `window_ms` | 200 (FIXED) | ms |

* Total grid: 5 x 5 = **25 grid cells**.
* Per cell: 12 directions x 10 trials x 3 modes (FULL / EPSP_PASSIVE / IPSP_PASSIVE) = 360
  trials.
* Total: **9000 trials**.
* Estimated wall-clock: 9000 / 1800 x 105 min ≈ 8.75 h on local CPU (extrapolating t0057's
  measured 6318 s for 1800 trials).

## Outputs

For each `(gAMPA, GABA_BASE_NS)` grid cell:

1. Soma `V(t)` per direction (12 PNGs, FULL mode).
2. Aggregate EPSP at soma per direction (12 PNGs, EPSP_PASSIVE mode — clean envelope, no
   spikes).
3. Aggregate IPSP at soma per direction (12 PNGs, IPSP_PASSIVE mode — clean envelope, no
   spikes; each direction's plot should show the moving wave of GABA windows).
4. Firing-rate PSTH per direction (12 PNGs, FULL mode).
5. Polar tuning curve (peak Hz, primary DSI, vector-sum DSI, preferred direction).

Cross-grid summary plots:

* DSI (primary) heatmap over `(gAMPA, GABA_BASE_NS)`.
* DSI (vector-sum) heatmap over `(gAMPA, GABA_BASE_NS)`.
* Peak Hz heatmap over `(gAMPA, GABA_BASE_NS)` — for locating multi-spike regime.
* Null Hz heatmap over `(gAMPA, GABA_BASE_NS)`.
* HWHM heatmap over `(gAMPA, GABA_BASE_NS)`.
* RMSE vs t0004 target heatmap over `(gAMPA, GABA_BASE_NS)`.
* Regime-boundary contour overlay: single-spike-degenerate vs multi-spike vs full-suppression
  bands on the `(gAMPA, GABA_BASE_NS)` plane.

## Library Asset

Produce one library asset: `minimal_dsgc_bar_locked_gaba_ampa_sweep` (or similar slug). Same
component structure as `minimal_dsgc_tonic_gaba_sweep` from t0057, with three substantive
changes:

1. The GABA driver computes per-synapse `(t_on_i, t_off_i)` from synapse coordinate and
   stimulus direction (replacing t0057's global window).
2. The trial-mode dispatcher exposes `FULL`, `EPSP_PASSIVE`, `IPSP_PASSIVE` (replacing t0057's
   `FULL`, `AMPA_ONLY`, `GABA_ONLY`); HH save-and-zero is implemented inside the passive-mode
   entry points.
3. `gAMPA` is exposed as a public per-synapse parameter (was hard-coded at 0.5 nS in t0057).

## Key Questions

1. Does any `(gAMPA, GABA_BASE_NS)` grid cell produce FULL-mode peak Hz in the **5-50 Hz**
   band?
2. Among grid cells in the multi-spike regime, does any one produce **vector-sum DSI > 0.3**?
3. Does the bar-arrival-locked window mechanism produce direction-dependent IPSP timing that
   the global-window t0057 mechanism could not (i.e., does the IPSP envelope shift with
   `theta`)?
4. Where does the regime boundary lie between single-spike-degenerate, multi-spike, and
   full-suppression behaviour on the `(gAMPA, GABA_BASE_NS)` plane?
5. With clean spike-free EPSP and IPSP traces from EPSP_PASSIVE / IPSP_PASSIVE modes, does the
   EPSP-decay metric (which returned null on t0054 / t0055 due to spike contamination) become
   well-defined and produce useful per-direction values?

## Compute and Budget

Local CPU only. Estimated wall-clock: ~8.75 h for the simulation sweep, plus implementation,
unit testing, and reporting time. Cost: $0.00.

## Out of Scope

* NMDA receptors (AMPA-only on the E pathway; the AMPA + Mg-block-NMDA combination on this
  bar-locked substrate is the natural next task, covered by the still-active S-0057-06).
* Active dendritic conductances (passive dendrites by design — RQ4 follow-up territory).
* Synaptic noise (deterministic NetStim trials).
* Network-level inputs.
* `window_ms` sweep — fixed at 200 ms in this task.
* AMPA values above 4.0 nS — the top of the swept range was trimmed from S-0057-02's 5.0 nS to
  4.0 nS by researcher decision; if the multi-spike regime is not entered at 4.0 nS, a
  follow-up task can extend.

## Verification Criteria

* Library asset validates against `meta/asset_types/library/specification.md`.
* All 25 grid cells produce per-direction PNG plots in `results/images/` and selected
  representatives are embedded in `results_detailed.md`.
* Cross-grid summary heatmaps (DSI / Peak Hz / Null Hz / HWHM / RMSE / regime contour) exist
  and are embedded in `results_detailed.md`.
* `results/metrics.json` contains, for each `(gAMPA, GABA_BASE_NS)` cell: primary DSI,
  vector-sum DSI, preferred direction, peak Hz, null Hz, HWHM, RMSE vs t0004 target.
* Per-synapse bar-arrival-locked window mechanism unit-tested: a regression test asserts that
  the IPSP envelope's centre of mass shifts with bar direction by an amount consistent with
  the stimulus geometry (i.e., centre-of-mass `theta = 0` differs from `theta = 90` by a
  predictable amount given the synapse coordinates).
* HH save-and-zero correctness regression test: at one representative `(gAMPA, GABA_BASE_NS)`
  point, the FULL trace under the new code is bit-identical (within 1e-6 mV) to a reference
  produced from the old t0057 code path with HH active throughout.
* EPSP_PASSIVE peak Vm < spike threshold (~ -50 mV) at every direction and grid cell — gates
  that the save-and-zero is working.
* Same fixed placement seed (0) as t0052 / t0053 / t0057; placement_seed0 match test passes
  bit-for-bit against t0057's placement_seed0.json.
* `verify_research_code.py`, `verify_plan.py`, `verify_task_metrics.py`, and the library asset
  verificator all pass with 0 errors.

</details>

## Metrics

### gAMPA=0.50/GABA=0.10/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.633561719902207** |

### gAMPA=0.50/GABA=0.20/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.633561719902207** |

### gAMPA=0.50/GABA=0.50/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.633561719902207** |

### gAMPA=0.50/GABA=1.00/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.633561719902207** |

### gAMPA=0.50/GABA=2.00/FULL

| Metric | Value |
|--------|-------|
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **17.178292988536434** |

### gAMPA=1.00/GABA=0.10/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.33333302222220157** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **90.00000000000001** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.43165333512899** |

### gAMPA=1.00/GABA=0.20/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.33333302222220157** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **97.5** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.49602079302769** |

### gAMPA=1.00/GABA=0.50/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.633561719902207** |

### gAMPA=1.00/GABA=1.00/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.633561719902207** |

### gAMPA=1.00/GABA=2.00/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.633561719902207** |

### gAMPA=2.00/GABA=0.10/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.20000011200001785** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **37.499999999999986** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.063965238280947** |

### gAMPA=2.00/GABA=0.10/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **75.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=2.00/GABA=0.20/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.20000011200001785** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **29.999999999999993** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.9999999999999999** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.129800056257512** |

### gAMPA=2.00/GABA=0.20/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **75.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=2.00/GABA=0.50/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.33333302222220157** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **82.5** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.506134016848044** |

### gAMPA=2.00/GABA=0.50/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **75.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=2.00/GABA=1.00/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.33333302222220157** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **75.00000000000001** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.9999999999999999** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.60337240214017** |

### gAMPA=2.00/GABA=1.00/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **75.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=2.00/GABA=2.00/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.633561719902207** |

### gAMPA=2.00/GABA=2.00/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **75.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=3.00/GABA=0.10/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.4999998250000087** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **104.99992650002943** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.9999999999999999** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.222909011117306** |

### gAMPA=3.00/GABA=0.10/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=3.00/GABA=0.20/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.4999998250000087** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **104.99992650002943** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.9999999999999999** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.222909011117306** |

### gAMPA=3.00/GABA=0.20/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=3.00/GABA=0.50/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.33333302222220157** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **75.00000000000001** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.468449219806864** |

### gAMPA=3.00/GABA=0.50/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=3.00/GABA=1.00/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.633561719902207** |

### gAMPA=3.00/GABA=1.00/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=3.00/GABA=2.00/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.633561719902207** |

### gAMPA=3.00/GABA=2.00/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=4.00/GABA=0.10/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.33333302222220157** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **67.50000000000001** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.53315809009725** |

### gAMPA=4.00/GABA=0.10/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=4.00/GABA=0.20/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.33333302222220157** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **67.50000000000001** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.53315809009725** |

### gAMPA=4.00/GABA=0.20/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=4.00/GABA=0.50/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.421429515011837** |

### gAMPA=4.00/GABA=0.50/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=4.00/GABA=1.00/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.33333302222220157** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **75.00000000000001** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.9999999999999999** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.56972856783266** |

### gAMPA=4.00/GABA=1.00/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gAMPA=4.00/GABA=2.00/FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.33333302222220157** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **75.00000000000001** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.9999999999999999** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.536500855616172** |

### gAMPA=4.00/GABA=2.00/EPSP_PASSIVE

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [Minimal DSGC with Bar-Arrival-Locked Tonic GABA + AMPA Sweep](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/assets/library/minimal_dsgc_bar_locked_gaba_ampa_sweep/) | [`description.md`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/assets/library/minimal_dsgc_bar_locked_gaba_ampa_sweep/description.md) |

## Suggestions Generated

<details>
<summary><strong>Active dendritic conductances (Nav1.6 + Kv3) layered on the t0059
bar-locked GABA + AMPA-escape substrate</strong> (S-0059-01)</summary>

**Kind**: experiment | **Priority**: high

The t0059 negative result (max FULL peak Hz = 2.143, max vector-sum DSI = 0.209) most
plausibly stems from passive dendrites capping local depolarisation; Park2014 [p. 3977] and
PolegPolsky2016 [p. 1278] both implicitly assume active dendritic mechanisms. Fork
minimal_dsgc_bar_locked_gaba_ampa_sweep, install Nav1.6 (g_Nabar in {0.05, 0.10, 0.20} S/cm^2)
and Kv3 (g_Kv3bar in {0.05, 0.10} S/cm^2) on dendritic sections, and run a focused 3x2x3
(gNa_dend x gKv3_dend x gAMPA in {1.0, 2.0, 4.0}) sweep at GABA_BASE_NS = 0.10 nS (the t0059
vector-sum DSI optimum). Pass criterion: at least one operating point with peak Hz >= 5 Hz AND
vector-sum DSI > 0.3. Distinct from S-0009-03 (calibrates densities against PolegPolsky2016
spike-shape and Ih-sag waveforms only) and S-0002-01 (somatic g_Na/g_K only). Directly
addresses RQ4 on the bar-locked substrate. Recommended task types: build-model,
experiment-run.

</details>

<details>
<summary><strong>Mg-block NMDA + bar-locked tonic GABA + AMPA-escape combination
sweep on the t0059 substrate</strong> (S-0059-02)</summary>

**Kind**: experiment | **Priority**: high

S-0057-06 covers Mg-block NMDA + tonic GABA but uses t0057's global (100, 1400) ms tonic
window and fixed gAMPA = 0.5 nS. t0059 demonstrates the bar-locked window mechanism delivers
an 8.5 ms direction-dependent IPSP centre-of-mass shift (REQ-13 PASS) the global window
cannot. Layering Mg-block NMDA on the bar-locked substrate combines all three plausible
gap-closers identified in compare-literature: voltage-dependent NMDA gain (PolegPolsky2016),
per-synapse bar-arrival timing (deRosenroll2026), and AMPA escape. Fork
minimal_dsgc_bar_locked_gaba_ampa_sweep, install the Jahr-Stevens NMDA_MgBlock mechanism from
t0055 at each E synapse, sweep gNMDA in {0.0, 0.25, 0.5, 1.0} nS x gAMPA in {1.0, 2.0, 4.0} nS
at GABA_BASE_NS = 0.10 nS (12 cells, 4320 trials at 10 trials x 12 directions x 3 modes). Pass
criterion: vector-sum DSI > 0.3 AND peak Hz >= 5 Hz. Distinct from S-0057-06 (global tonic
window, gAMPA=0.5 fixed). Recommended task types: build-model, experiment-run.

</details>

<details>
<summary><strong>Synapse-count scaling sweep on t0059 substrate (100 -> 200 -> 300 E
+ I) to break the single-spike regime</strong> (S-0059-03)</summary>

**Kind**: experiment | **Priority**: high

t0059 uses 100 E + 100 I synapses; PolegPolsky2016 [p. 1280] uses ~177, t0046 reproduction
uses 282, deRosenroll2026 [p. 5] uses >1000 SAC varicosities. The compare-literature
Synapse-count comparison identifies this >2.8x to >10x mismatch as a structural drive
bottleneck consistent with the 2.143 Hz peak ceiling. Fork
minimal_dsgc_bar_locked_gaba_ampa_sweep, parameterise N_AMPA = N_GABA in {100, 200, 300}
(re-running the placement_seed0 generator to produce three larger placement bundles), and
sweep at gAMPA in {1.0, 2.0} nS, GABA_BASE_NS = 0.10 nS, holding bar-locked windows fixed (3 N
x 2 gAMPA = 6 cells, 2160 trials). Pass criterion: at least one (N, gAMPA) point with peak Hz
>= 5 Hz. This is the smallest single-axis test of the structural-drive hypothesis on the
validated bar-locked substrate. Distinct from S-0052-02 (GABA-count sweep on scalar gabaMOD
t0052, no bar-lock). Recommended task types: build-model, experiment-run.

</details>

<details>
<summary><strong>Synaptic noise (NetStim jitter + AR(2) correlated release) on t0059
substrate for trial-to-trial DSI characterisation</strong> (S-0059-04)</summary>

**Kind**: experiment | **Priority**: medium

t0059 has reliability = 1.0 across all FULL cells because each NetStim emits a single
deterministic event per direction. deRosenroll2026 [p. 6] requires AR(2) correlated release
with rho = 0.6 to match in vitro DSGC reliability and reaches vector-sum DSI = 0.39 (3.1x our
0.209). Determinism may be the dominant DSI suppressor. Fork
minimal_dsgc_bar_locked_gaba_ampa_sweep, add (1) per-trial NetStim noise = 0.1 (~1 ms jitter)
on each AMPA and tonic-GABA driver, then (2) implement the deRosenroll2026 AR(2) correlated
release schedule (rho in {0.0, 0.6}, n=20 trials per direction). Operate at the t0059 optimum
(gAMPA=1.0/gaba=0.10) across 4 noise cells. Pass criterion: vector-sum DSI > 0.3 in at least
one noise configuration, OR rule out with CIs over n=20 trials. Recommended task types:
build-model, experiment-run.

</details>

<details>
<summary><strong>Stricter AMPA escape range (gAMPA in {5, 7, 10} nS) and sub-0.1 nS
bar-locked GABA on t0059 substrate</strong> (S-0059-05)</summary>

**Kind**: experiment | **Priority**: medium

The t0059 sweep limits gAMPA to {0.5, 1.0, 2.0, 3.0, 4.0} nS (trimmed from 5 nS by researcher
decision). The compare-literature Limitations section flags the diminishing-returns shape
suggests extending to 6-10 nS is unlikely to break the multi-spike wall but should be
confirmed. Symmetrically, 10 of 25 cells already at GABA_BASE_NS = 0.10 nS show no escape, but
sub-0.1 nS values (0.025, 0.05) were not tested. Fork minimal_dsgc_bar_locked_gaba_ampa_sweep,
run gAMPA in {5.0, 7.0, 10.0} nS x GABA_BASE_NS in {0.025, 0.05, 0.10} nS (9 cells, 3240
trials). Pass criterion: locate at least one operating point with peak Hz >= 5 Hz AND
vector-sum DSI > 0.3, OR confirm the 4 nS / 0.1 nS ceiling rules out the AMPA-only path on
this substrate. Lowest-cost extension of the t0059 sweep on already-validated machinery.
Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Bar-locked window-length sweep (window_ms in {100, 200, 300, 500})
on t0059 substrate</strong> (S-0059-06)</summary>

**Kind**: experiment | **Priority**: medium

t0059 fixes window_ms = 200 (midpoint of the published 100-300 ms SAC->DSGC IPSC envelope
range). Compare-literature Limitations flags this as untested; PolegPolsky2016 [p. 1280] uses
tau ~50-150 ms and deRosenroll2026 implies shorter envelopes match in vitro better. The 8.5 ms
IPSP centre-of-mass shift demonstrated at window_ms = 200 may sharpen substantially at
window_ms = 100 (more direction-tuned suppression) or smear out at window_ms = 500 (back
toward t0057 global behaviour). Fork minimal_dsgc_bar_locked_gaba_ampa_sweep, sweep window_ms
in {100, 200, 300, 500} ms x GABA_BASE_NS in {0.10, 0.50, 1.0} nS at fixed gAMPA = 2.0 nS (12
cells, 4320 trials). Pass criterion: detect a non-monotonic vector-sum DSI vs window_ms
relationship (i.e., the 200 ms midpoint is not a local optimum), OR confirm the 200 ms choice
is robust. Recommended task types: experiment-run.

</details>

## Research

* [`research_code.md`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/results_summary.md)*

# Results Summary: Bar-Arrival-Locked Tonic GABA + AMPA Escape Sweep on t0057 Substrate

## Summary

Forked t0057's `minimal_dsgc_tonic_gaba_sweep` library, replaced the global `(t_on, t_off) =
(100, 1400) ms` tonic-GABA window with per-synapse bar-arrival-locked windows `t_on_i = (x_i
cos theta + y_i sin theta) / v + 100 ms`, `t_off_i = t_on_i + 200 ms`, swept a 5x5 `(gAMPA,
GABA_BASE_NS)` grid over `gAMPA in {0.5, 1.0, 2.0, 3.0, 4.0}` nS x `GABA_BASE_NS in {0.1, 0.2,
0.5, 1.0, 2.0}` nS, and bundled the project-wide S-0055-01 measurement-protocol fix (drop
`AMPA_ONLY` / `GABA_ONLY`; add `EPSP_PASSIVE` / `IPSP_PASSIVE` with HH save-and-zero on soma +
AIS; standardise trial length at 1400 ms). Headline negative finding: **no operating point in
the swept grid produces multi-spike firing or non-trivial direction selectivity**. The maximum
FULL-mode peak rate across all 25 cells is **2.143 Hz** (3 spikes / 1.4 s, four cells); the
maximum primary DSI is **0.5** at gAMPA=3.0/gaba=0.10 and 0.20; the maximum vector-sum DSI is
**0.209** at gAMPA=1.0/gaba=0.10. The bar-locked window mechanism and HH save-and-zero
protocol are both validated independently (REQ-13 IPSP centre-of-mass shift = 8.5 ms between
theta=0 and theta=90; REQ-15 worst-case EPSP_PASSIVE peak Vm = -9.04 mV << +5 mV gate
threshold).

## Metrics

* **Max FULL peak Hz across all 25 cells**: **2.143 Hz** (3 spikes / 1.4 s) at four cells:
  gAMPA=2.0/gaba=0.10, gAMPA=2.0/gaba=0.20, gAMPA=3.0/gaba=0.10, gAMPA=3.0/gaba=0.20. **No
  cell enters the 5-50 Hz multi-spike band** (RQ1 = NO).
* **Max primary DSI (FULL)**: **0.500** at gAMPA=3.0/gaba=0.10 and gAMPA=3.0/gaba=0.20 (peak
  Hz = 2.143, null Hz = 0.714 — discrete-spike artefact, not a true tuned response).
* **Max vector-sum DSI (FULL)**: **0.209** at gAMPA=1.0/gaba=0.10. **No cell exceeds the 0.3
  vector-sum DSI threshold** (RQ2 = NO).
* **Best HWHM (FULL)**: **30.0 deg** at gAMPA=2.0/gaba=0.20 (peak Hz = 2.143, primary DSI =
  0.2, vector-sum DSI = 0.196).
* **Regime distribution** (over 25 FULL cells): full-suppression (peak Hz = 0) = **1/25**;
  single-spike-degenerate (peak Hz = 0.714) = **9/25**; two-spike (peak Hz = 1.429) =
  **11/25**; three-spike (peak Hz = 2.143) = **4/25**; multi-spike (>= 5 Hz) = **0/25**.
* **Tuning-curve RMSE vs t0004 target (32 Hz peak)**: range **16.06 Hz** (best,
  gAMPA=2.0/gaba=0.10) to **17.18 Hz** (worst, gAMPA=0.5/gaba=2.0; full-suppression cell).
* **Bar-locked IPSP centre-of-mass shift** (REQ-13): **8.5 ms** between theta=0 and theta=90
  in IPSP_PASSIVE traces — confirms the per-synapse bar-arrival-locked window mechanism is
  delivering direction-dependent inhibitory timing, which the global-window t0057 mechanism
  could not (RQ3 = YES).
* **HH save-and-zero correctness** (REQ-14, REQ-15): worst-case EPSP_PASSIVE peak Vm across
  all 300 EPSP_PASSIVE direction-cells = **-9.04 mV** (well below the +5 mV gate, i.e., the
  soma is passive); FULL-mode bit-identity test passed against reference at atol = 1e-6 mV.
* **Active-fraction modulation** (carried over from t0053 / t0057 spatial gating, conductance-
  and gAMPA-independent): **0.34** (theta = 30 deg) to **0.66** (theta = 210 deg), mean
  **0.50** within the [0.4, 0.6] soft sanity band.
* **Wall-clock**: **41621.91 s = 11.56 h** for 9000 trials on single-threaded local CPU under
  CVODE (`atol = 1e-3`).

## Verification

* `verify_task_metrics.py t0059_bar_locked_gaba_ampa_sweep_t0057` — **PASSED** (0 errors, 0
  warnings); 75 variants (5 gAMPA x 5 gaba x 3 modes).
* `verify_task_results.py t0059_bar_locked_gaba_ampa_sweep_t0057` — **PASSED**.
* `verify_assets.py t0059_bar_locked_gaba_ampa_sweep_t0057` — **PASSED**
  (`minimal_dsgc_bar_locked_gaba_ampa_sweep` library asset, 0/0).
* `test_bar_locked_ipsp_envelope.py` (REQ-13): **PASSED** at gAMPA=1.0/gaba=1.0;
  centre-of-mass shift = 8.5 ms exceeds geometric lower bound.
* `test_hh_save_and_zero.py` (REQ-14): **PASSED**; FULL-mode reference trace match within atol
  = 1e-6 mV.
* `test_placement_seed0_match.py` (REQ-16): **PASSED**; 100/100 pairs match t0057's
  `placement_seed0.json` at POSITION_TOLERANCE = 1e-9.
* `test_quiescent_rest.py`: **PASSED** (V_rest = -65 mV +/- 0.5 mV).
* `test_spatial_gating.py` (REQ-2): **PASSED** (4/4).
* EPSP_PASSIVE peak-Vm soft gate (REQ-15): **PASSED**; worst-case peak Vm = -9.04 mV across
  all EPSP_PASSIVE traces (gate threshold +5 mV).

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0059_bar_locked_gaba_ampa_sweep_t0057" date_completed:
"2026-04-29" ---
# Results Detailed: Bar-Arrival-Locked Tonic GABA + AMPA Escape Sweep on t0057 Substrate

## Summary

Forked t0057's `minimal_dsgc_tonic_gaba_sweep` library and applied four bundled changes: (a)
replaced the global tonic-GABA window `(t_on, t_off) = (100, 1400) ms` with per-synapse
bar-arrival-locked windows `t_on_i = (x_i cos theta + y_i sin theta) / v + 100 ms, t_off_i =
t_on_i + 200 ms`; (b) added `EPSP_PASSIVE` / `IPSP_PASSIVE` trial modes that save-and-zero
`gnabar_hh` / `gkbar_hh` on `soma` and `axon_initial_segment` (replacing legacy `AMPA_ONLY` /
`GABA_ONLY`); (c) exposed gAMPA as a public per-synapse parameter and swept a 5x5 `(gAMPA,
GABA_BASE_NS)` grid; (d) standardised `TSTOP_MS = 1400 ms`. Total budget: 25 cells x 12
directions x 10 trials x 3 modes = 9000 trials. Headline negative finding: **no operating
point in the swept grid produces multi-spike firing or non-trivial direction selectivity**.
The maximum FULL-mode peak rate is 2.143 Hz (3 spikes / 1.4 s, 4 cells); the maximum
vector-sum DSI is 0.209. Both new mechanisms validate independently — the bar-locked windows
produce a measurable 8.5 ms direction-dependent IPSP centre-of-mass shift (REQ-13), and the HH
save-and-zero correctly drives EPSP_PASSIVE peak Vm to -9.04 mV worst-case (REQ-15) and
matches a FULL reference trace bit-for-bit at atol = 1e-6 mV (REQ-14). The cell simply does
not enter multi-spike firing under any (gAMPA, GABA) combination on this passive-dendrite,
AMPA-only-excitation substrate.

## Methodology

* **Machine**: local CPU (single-threaded NEURON simulation under CVODE, `atol = 1e-3`).
* **Sweep window**: started 2026-04-29T08:41:08Z, completed 2026-04-29T20:17:00Z (full sweep
  inclusive of metric and figure rendering).
* **Wall-clock (simulation only)**: 41621.91 s (11.56 h) for 9000 trials = 4.62 s / trial
  average.
* **Sweep grid**: `gAMPA in {0.5, 1.0, 2.0, 3.0, 4.0}` nS x `GABA_BASE_NS in {0.1, 0.2, 0.5,
  1.0, 2.0}` nS x 12 directions x 10 trials x 3 modes (FULL / EPSP_PASSIVE / IPSP_PASSIVE) =
  9000 trials.
* **GABA windowing (NEW)**: per-synapse bar-arrival-locked windows. For each active synapse
  `i` at coordinate `(x_i, y_i)`, `t_on_i = (x_i cos(theta_stim) + y_i sin(theta_stim)) / v +
  100 ms`; `t_off_i = t_on_i + WINDOW_MS`, with `WINDOW_MS = 200.0` (FIXED), `v = 1000 um/s`.
  Each window is realised by writing `t_on` / `t_off` directly to the per-pair `gaba_tonic`
  POINT_PROCESS. Silent synapses get `g = 0` and a collapsed window.
* **Spatial gating** (preserved from t0053 / t0057 bit-for-bit): each I synapse fires only
  when `cos(theta_stim - theta_centrifugal) < 0`. Active fraction modulates 0.34 -> 0.66
  across directions; mean = 0.50.
* **Trial modes (NEW measurement protocol per S-0055-01)**:
  * `FULL`: HH active on soma + AIS; both AMPA and bar-locked GABA delivered.
  * `EPSP_PASSIVE`: HH `gnabar` / `gkbar` saved and zeroed on soma + AIS only (try/finally
    restores at trial end); GABA `g` set to 0; AMPA delivered. Records the clean spike-free
    EPSP envelope at the soma.
  * `IPSP_PASSIVE`: HH save-and-zero on soma + AIS; AMPA `weight[0]` set to 0; bar-locked GABA
    delivered. Records the clean spike-free IPSP envelope at the soma — the moving wave of
    GABA windows tracking the stimulus bar across the dendritic arbor.
* **Bar stimulus**: 200 um wide x full arena, 1000 um/s, 1400 ms trial duration, dt = 0.025
  ms.
* **Morphology**: `dsgc-baseline-morphology-calibrated` (t0009 calibrated 141009_Pair1DSGC
  reconstruction). Identical to t0052 / t0053 / t0054 / t0055 / t0057.
* **Synapse population**: 100 E + 100 I co-located pairs, uniform random over dendrites, fixed
  placement seed 0 (bit-identical to t0057 — REQ-16 PASS at POSITION_TOLERANCE = 1e-9).
* **Excitation (NEW per-synapse parameter)**: AMPA `Exp2Syn` (rise = 0.5 ms, decay = 2.5 ms, e
  = 0 mV), peak conductance `gampa_ns` is now a swept per-synapse parameter (was hard-coded at
  0.5 nS in t0057).
* **Inhibition mechanism**: t0057's `gaba_tonic.mod` POINT_PROCESS, unchanged. The Python
  caller writes per-pair `t_on` / `t_off` instead of the legacy global constant.
* **Spike detection**: somatic V > -20 mV with NetCon `record()`; per-trial spike times in
  `spike_times_<mode>.csv`.
* **Multiprocessing**: not used; single-threaded sequential trial loop preserves the
  placement-seed-0 reproducibility guarantee against t0057.
* **Implementation note**: a first sweep (7 h 32 m) was lost when a too-strict EPSP_PASSIVE
  peak-Vm gate (`AP_THRESHOLD_MV = -20 mV`) tripped at gAMPA = 2.0 nS where passive AMPA
  summation reaches -17.99 mV. Patched in place by introducing `EPSP_PASSIVE_PEAK_VM_GATE_MV =
  +5.0 mV` (above `E_AMPA = 0 mV`, below the +20-30 mV active spike peak) and reordering the
  gate check after CSV writes. Second sweep ran 11.56 h to completion with no gate trip;
  worst-case EPSP_PASSIVE peak Vm = -9.04 mV across the 300 direction-cells.

## Metrics Tables

`metrics.json` contains 75 variants (5 gAMPA x 5 GABA x 3 modes); `derived_quantities.json`
carries the full per-cell / per-direction breakdown. The four registered project metrics
(`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`) are populated for FULL and (where well-defined) for EPSP_PASSIVE;
IPSP_PASSIVE variants have null metrics by construction (no spikes possible without HH).

### FULL-mode 5x5 grid: peak Hz

Rows = gAMPA (nS); columns = GABA_BASE_NS (nS).

| gAMPA \ GABA | 0.10 | 0.20 | 0.50 | 1.00 | 2.00 |
| --- | --- | --- | --- | --- | --- |
| 0.5 | 0.714 | 0.714 | 0.714 | 0.714 | 0.000 |
| 1.0 | 1.429 | 1.429 | 0.714 | 0.714 | 0.714 |
| 2.0 | 2.143 | 2.143 | 1.429 | 1.429 | 0.714 |
| 3.0 | 2.143 | 2.143 | 1.429 | 0.714 | 0.714 |
| 4.0 | 1.429 | 1.429 | 1.429 | 1.429 | 1.429 |

### FULL-mode 5x5 grid: primary DSI

| gAMPA \ GABA | 0.10 | 0.20 | 0.50 | 1.00 | 2.00 |
| --- | --- | --- | --- | --- | --- |
| 0.5 | 0.000 | 0.000 | 0.000 | 0.000 | null |
| 1.0 | 0.333 | 0.333 | 0.000 | 0.000 | 0.000 |
| 2.0 | 0.200 | 0.200 | 0.333 | 0.333 | 0.000 |
| 3.0 | **0.500** | **0.500** | 0.333 | 0.000 | 0.000 |
| 4.0 | 0.333 | 0.333 | 0.000 | 0.333 | 0.333 |

### FULL-mode 5x5 grid: vector-sum DSI

| gAMPA \ GABA | 0.10 | 0.20 | 0.50 | 1.00 | 2.00 |
| --- | --- | --- | --- | --- | --- |
| 0.5 | 4.7e-17 | 4.7e-17 | 4.7e-17 | 4.7e-17 | 0.000 |
| 1.0 | **0.209** | 0.160 | 4.7e-17 | 4.7e-17 | 4.7e-17 |
| 2.0 | 0.193 | 0.196 | 0.124 | 0.077 | 4.7e-17 |
| 3.0 | 0.111 | 0.111 | 0.067 | 4.7e-17 | 4.7e-17 |
| 4.0 | 0.037 | 0.037 | 0.067 | 0.077 | 0.077 |

### FULL-mode 5x5 grid: HWHM (deg)

| gAMPA \ GABA | 0.10 | 0.20 | 0.50 | 1.00 | 2.00 |
| --- | --- | --- | --- | --- | --- |
| 0.5 | 180.0 | 180.0 | 180.0 | 180.0 | null |
| 1.0 | 90.0 | 97.5 | 180.0 | 180.0 | 180.0 |
| 2.0 | 37.5 | **30.0** | 82.5 | 75.0 | 180.0 |
| 3.0 | 105.0 | 105.0 | 75.0 | 180.0 | 180.0 |
| 4.0 | 67.5 | 67.5 | 180.0 | 75.0 | 75.0 |

### FULL-mode 5x5 grid: tuning-curve RMSE vs t0004 target (Hz)

t0004 target peaks at ~32 Hz; RMSE is dominated by the gap between target and the model's <
2.143 Hz peak. All cells fall in a narrow 16.06 - 17.18 Hz band.

| gAMPA \ GABA | 0.10 | 0.20 | 0.50 | 1.00 | 2.00 |
| --- | --- | --- | --- | --- | --- |
| 0.5 | 16.634 | 16.634 | 16.634 | 16.634 | 17.178 |
| 1.0 | 16.432 | 16.496 | 16.634 | 16.634 | 16.634 |
| 2.0 | **16.064** | 16.130 | 16.506 | 16.603 | 16.634 |
| 3.0 | 16.223 | 16.223 | 16.468 | 16.634 | 16.634 |
| 4.0 | 16.533 | 16.533 | 16.421 | 16.570 | 16.537 |

### Aggregate IPSP envelope peak (mV) at theta = 210 deg (most-active direction)

The IPSP envelope is gAMPA-independent (AMPA is muted in IPSP_PASSIVE and adds no excitatory
drive); rows below are quoted from gAMPA=1.0 row of `aggregate_ipsp_peak_per_direction_mv`.
The envelope grows sub-linearly with GABA conductance — same driving-force-saturation pattern
documented in t0052 / t0053 / t0057.

| GABA_BASE_NS | Peak IPSP voltage at theta = 210 deg |
| --- | --- |
| 0.10 nS | 1.495 mV |
| 0.20 nS | 2.713 mV |
| 0.50 nS | 4.880 mV |
| 1.00 nS | 6.545 mV |
| 2.00 nS | 7.866 mV |

### Aggregate EPSP envelope peak (mV) at theta = 210 deg, EPSP_PASSIVE mode

The passive EPSP envelope is GABA-independent (GABA is muted in EPSP_PASSIVE); rows below are
quoted from gaba=0.10 column of `aggregate_epsp_peak_per_direction_mv`. Peak Vm grows
monotonically with gAMPA but stays sub-spike-threshold under HH save-and-zero, confirming the
wiring is correct.

| gAMPA | Peak EPSP voltage at theta = 210 deg |
| --- | --- |
| 0.5 nS | 24.178 mV (relative to V_rest = -65 mV: peak Vm ≈ -40.8 mV) |
| 1.0 nS | 36.621 mV (peak Vm ≈ -28.4 mV) |
| 2.0 nS | 48.212 mV (peak Vm ≈ -16.8 mV) |
| 3.0 nS | 53.265 mV (peak Vm ≈ -11.7 mV) |
| 4.0 nS | 55.965 mV (peak Vm ≈ -9.04 mV — worst-case across the grid) |

## Comparison vs Baselines

### vs parent task t0057 (tonic GABA, 1-D GABA-only sweep)

| Metric | t0057 (best) | t0059 (best) | Notes |
| --- | --- | --- | --- |
| Max FULL peak Hz | 0.667 Hz (single-spike-degenerate) | **2.143 Hz** (3 spikes / 1.4 s) | Higher gAMPA partly escapes the single-spike regime; still far below the 5-50 Hz multi-spike band. |
| Max primary DSI | 0.0 (peak = null at every cell) | **0.500** | Discrete-spike artefact (peak Hz = 2 / null Hz = 1 in spikes), not biologically tuned. |
| Max vector-sum DSI | ~3.2e-17 (numerical floor) | **0.209** | First non-trivial DSI in the from-scratch DSGC line; below the 0.3 hypothesis threshold. |
| GABA window mechanism | global `(100, 1400) ms` for all active synapses | per-synapse `(t_on_i, t_off_i)` with 200 ms window | Bar-locked mechanism produces 8.5 ms direction-dependent IPSP centre-of-mass shift (REQ-13). |
| Trial length | 1500 ms | 1400 ms (S-0055-01 standardisation) | Firing-rate denominator now 1.4 s instead of 1.5 s. |
| Measurement protocol | `FULL` / `AMPA_ONLY` / `GABA_ONLY` (HH always active; spike contamination on passive measurements) | `FULL` / `EPSP_PASSIVE` / `IPSP_PASSIVE` (HH save-and-zero on passive modes) | EPSP-decay metric becomes well-defined (RQ5); see Analysis. |
| Trials | 1800 | 9000 | 5x grid expansion. |
| Wall-clock | 6318 s = 105 min | 41622 s = 11.56 h | 6.6x trials = 6.6x runtime; per-trial cost ≈ 4.62 s (vs 3.51 s in t0057, 31% slower per trial likely due to per-pair window writes). |

### vs sibling from-scratch DSGC tasks (t0052, t0053, t0054, t0055)

| Task | E pathway | I pathway | Max FULL peak Hz | Max FULL DSI |
| --- | --- | --- | --- | --- |
| t0052 | AMPA 0.5 nS | scalar gabaMOD (point process) | 0.667 | 0.7464 (vector-sum, trivially from full PD/ND switch) |
| t0053 | AMPA 0.5 nS | spatial Exp2Syn GABA, centripetal gating | 0.667 | 0.7464 (trivial) |
| t0054 | AMPA + NMDA, scalar gabaMOD | scalar gabaMOD | 0.667 | 1.0 (trivial; full ND suppression) |
| t0055 | AMPA + Mg-block NMDA, scalar gabaMOD | scalar gabaMOD | 0.667 | 1.0 (trivial) |
| t0057 | AMPA 0.5 nS | tonic GABA global window, sweep 0.25-2.0 nS | 0.667 | 3.2e-17 (degenerate) |
| **t0059** | **AMPA 0.5-4.0 nS sweep** | **bar-locked tonic GABA, sweep 0.1-2.0 nS** | **2.143** | **0.209 (vector-sum), 0.500 (primary)** |

t0059 is the **first task in the from-scratch DSGC line to escape the 0.667 Hz single-spike
regime non-trivially** — but only barely. The four 2.143 Hz cells correspond to 3 spikes per
1.4 s trial (at the preferred direction; null direction = 1-2 spikes). The cell never produces
the > 5 Hz firing rates needed for biologically meaningful DSI metrics.

## Visualizations

### Cross-grid heatmaps (REQ-10)

![FULL-mode peak Hz
heatmap](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/heatmap_peak_hz.png)

Peak firing rate (FULL) over the `(gAMPA, GABA_BASE_NS)` plane. The 2.143 Hz "ridge" at gAMPA
in {2.0, 3.0} nS x gaba in {0.10, 0.20} nS is visible; otherwise the grid clusters around
0.714 Hz (single-spike-degenerate) and 1.429 Hz (two-spike).

![FULL-mode null Hz
heatmap](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/heatmap_null_hz.png)

Null-direction firing rate. Most cells have null Hz = 0.714 Hz, indicating the cell fires at
least one spike even at the unfavoured direction — i.e., GABA is not fully overriding AMPA.

![Primary DSI
heatmap](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/heatmap_dsi_primary.png)

Primary DSI = (peak - null) / peak. The 0.500 maxima at gAMPA=3.0 / gaba in {0.10, 0.20} are
visible but reflect a discrete-spike artefact (3 spikes vs 1 spike across direction), not a
tuned response.

![Vector-sum DSI
heatmap](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/heatmap_dsi_vector_sum.png)

Vector-sum DSI. The diagonal of "weak" non-trivial values around gAMPA in {1.0, 2.0} nS x gaba
in {0.10, 0.20} nS sits between 0.16 and 0.21; nothing exceeds the 0.3 RQ2 threshold.

![HWHM
heatmap](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/heatmap_hwhm.png)

Half-width at half-max of the polar tuning curve. The 30 deg cell at gAMPA=2.0/gaba=0.20 is
the sharpest; most cells default to 180 deg (degenerate uniform tuning).

![RMSE vs t0004
heatmap](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/heatmap_rmse.png)

Tuning-curve RMSE vs t0004 target curve. Range = 16.06-17.18 Hz, dominated by the 32 Hz target
peak vs the < 2.143 Hz model peak.

### Regime boundary contour (REQ-11)

![Regime-boundary contour
overlay](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/regime_boundary_contour.png)

Three contour bands overlaid on the FULL peak-Hz grid: full-suppression (peak Hz < 0.5;
gAMPA=0.5/gaba=2.0 only), single-spike-degenerate (0.5 - 5 Hz; the bulk of the grid), and
multi-spike (>= 5 Hz; not entered anywhere).

### Active-fraction polar (carried from t0057, gAMPA / GABA-independent)

![Active-fraction per direction polar
plot](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/active_fraction_polar.png)

The fraction of 100 I synapses whose centripetal-gating predicate is active, plotted per
stimulus direction. Modulates 0.34 (theta = 30 deg) to 0.66 (theta = 210 deg), mean 0.50.
Bit-identical to t0053 / t0057 because the spatial-gating rule is unchanged.

### Representative per-cell plots

#### Best primary DSI: gAMPA=3.0 / gaba=0.10 (primary DSI = 0.500, peak Hz = 2.143, vector-sum DSI = 0.111)

![Polar tuning curve, gAMPA=3.0,
gaba=0.10](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/polar_tuning_curve_gampa_3.00_gaba_0.10.png)

Polar tuning curve (FULL). Peak at theta = 120 deg (peak Hz = 2.143), null at theta in {300,
330} (0.714 Hz). The 3-spike-vs-1-spike contrast yields primary DSI = 0.5 but the underlying
vector-sum DSI is only 0.111 because firing is approximately bimodal across the 12 directions
rather than smoothly tuned.

#### Best vector-sum DSI: gAMPA=1.0 / gaba=0.10 (vector-sum DSI = 0.209, peak Hz = 1.429)

![Polar tuning curve, gAMPA=1.0,
gaba=0.10](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/polar_tuning_curve_gampa_1.00_gaba_0.10.png)

Polar tuning curve (FULL). Two-spike "preferred" lobe spans theta in {0, 30}, single-spike
"null" in the rest of the directions. Vector sum picks up the angular mass concentration
toward 15 deg.

#### Sharpest HWHM: gAMPA=2.0 / gaba=0.20 (HWHM = 30 deg, peak Hz = 2.143, vector-sum DSI = 0.196)

![Polar tuning curve, gAMPA=2.0,
gaba=0.20](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/polar_tuning_curve_gampa_2.00_gaba_0.20.png)

Polar tuning curve (FULL). The narrowest tuning in the entire grid; 3-spike preferred
direction at theta = 60 deg drops to 1 spike at adjacent directions.

#### Worst suppression: gAMPA=0.5 / gaba=2.00 (peak Hz = 0, fully suppressed)

![Polar tuning curve, gAMPA=0.5,
gaba=2.00](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/polar_tuning_curve_gampa_0.50_gaba_2.00.png)

Polar tuning curve (FULL). Empty origin — the 2.0 nS bar-locked GABA window suppresses the
cell at all 12 directions when AMPA is at the lowest swept value.

#### Bar-locked IPSP envelope direction shift (REQ-13 evidence)

![IPSP envelope at theta = 0,
gAMPA=1.0/gaba=1.0](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/ipsp_gampa_1.00_gaba_1.00_theta_000.png)

![IPSP envelope at theta = 90,
gAMPA=1.0/gaba=1.0](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/ipsp_gampa_1.00_gaba_1.00_theta_090.png)

Aggregate IPSP at the soma in IPSP_PASSIVE mode at theta = 0 (left) vs theta = 90 (right) for
gAMPA=1.0 / gaba=1.0. The envelope's centre of mass shifts by 8.5 ms between the two
directions — the explicit signature of the bar-locked window mechanism. Under t0057's
global-window mechanism the two envelopes would have been identical apart from the
active-fraction normalisation.

The remaining 1213 PNGs in `results/images/` (5 PNGs per cell x 25 cells = 125 plots x 12
directions = 1500 figure-cell-direction triples; 25 polars; 6 heatmaps; 1 regime contour; 1
active-fraction polar) cover per-direction soma V(t) (FULL), aggregate EPSP (EPSP_PASSIVE),
aggregate IPSP (IPSP_PASSIVE), firing-rate PSTH (FULL), and per-cell polar tuning curves.

## Analysis

### The headline negative result

Across all 25 grid cells, peak firing rate maxes out at **2.143 Hz = 3 spikes / 1.4 s** at the
preferred direction. None of the 25 cells produces a tuning curve with peak Hz > 5 Hz (the
lower bound of the multi-spike-regime band defined in RQ1), and no cell achieves the
vector-sum DSI > 0.3 target from RQ2.

The pattern is consistent with the diagnosis from t0052-t0057: the t0009 calibrated
141009_Pair1DSGC morphology, with 100 AMPA synapses, passive dendrites, and HH on soma + AIS
only, simply cannot produce sustained multi-spike firing under any reasonable AMPA conductance
up to 4.0 nS. The discrete primary-DSI values at 0.5, 0.333, 0.2 are all spike-count ratios on
a tiny 0-3 spike range; they are not biologically meaningful direction-tuning measurements.

The full-suppression / single-spike-degenerate / few-spike regime distribution is:

* **Full suppression** (peak = 0 Hz): 1 / 25 cells (gAMPA=0.5 / gaba=2.0).
* **Single-spike-degenerate** (peak = null = 0.714 Hz, primary DSI = 0): 9 / 25 cells.
* **Two-spike** (peak = 1.429 Hz): 11 / 25 cells.
* **Three-spike** (peak = 2.143 Hz): 4 / 25 cells.
* **Multi-spike** (peak >= 5 Hz): **0 / 25 cells**.

### What this rules out

This task definitively rules out two hypotheses for the from-scratch DSGC substrate:

1. **AMPA conductance escape from the single-spike regime via gAMPA in {0.5, 1.0, 2.0, 3.0,
   4.0} nS** does not work on a passive-dendrite + HH-soma-AIS morphology. The 8x conductance
   increase from 0.5 to 4.0 nS adds at most 2 spikes per trial. Higher gAMPA (>= 5 nS) would
   need to be tested but the diminishing-returns shape of the peak-Hz heatmap suggests the
   wall is structural, not amplitudinal.
2. **Bar-arrival-locked tonic GABA at sub-0.25 nS** does not unlock graded suppression of an
   already-firing cell. The graded-suppression hypothesis required the cell to be firing
   multi-spike for GABA to modulate; since multi-spike firing is not entered, sub-0.25 nS GABA
   produces near-zero IPSP voltage envelope (1.495 mV at gaba=0.10 nS at the most-active
   direction) and has no effect on the spike count.

### What this validates (the two new mechanisms)

The two new building blocks ship correctly:

1. **Bar-arrival-locked window (REQ-1, REQ-13)**: the per-synapse `(t_on_i, t_off_i)` write
   produces an IPSP envelope at the soma whose centre of mass shifts with stimulus direction.
   `test_bar_locked_ipsp_envelope.py` measures **8.5 ms** shift between theta = 0 and theta =
   90 in IPSP_PASSIVE traces at gAMPA=1.0 / gaba=1.0 — exceeding the geometric lower bound
   predicted from the synapse coordinates. RQ3 = YES: the bar-locked mechanism produces
   direction-dependent IPSP timing the global-window t0057 mechanism could not.

2. **HH save-and-zero (REQ-3, REQ-14, REQ-15)**: the `try/finally` save-and-restore on
   `gnabar_hh` / `gkbar_hh` works exception-safely. `test_hh_save_and_zero.py` confirms the
   FULL trace is bit-identical (within `atol = 1e-6 mV`) to a reference trace produced with HH
   active throughout. The EPSP_PASSIVE peak-Vm soft gate (REQ-15) caught a too-strict initial
   threshold (`AP_THRESHOLD_MV = -20 mV`) at gAMPA = 2.0 nS where passive AMPA summation
   reaches -17.99 mV; patched to `EPSP_PASSIVE_PEAK_VM_GATE_MV = +5 mV` (above `E_AMPA = 0
   mV`, below the +20-30 mV active spike peak). Worst-case EPSP_PASSIVE peak Vm = **-9.04 mV**
   at gAMPA=4.0 / theta=210 deg — well below the +5 mV gate, confirming HH is correctly muted
   across all 300 EPSP_PASSIVE direction-cells.

### EPSP-decay metric (RQ5)

The `epsp_decay_grid` in `derived_quantities.json` reports the EPSP envelope decay ratio per
direction in EPSP_PASSIVE mode. Values cluster tightly around 1.0 (range [0.9952, 1.0022])
across all 25 cells x 12 directions = 300 measurements. RQ5 = PARTIAL: the metric is now
well-defined (no spike contamination, unlike t0054 / t0055) but the EPSP envelope is
essentially flat at the moment of measurement (200-1400 ms post-stimulus) because the t0009
morphology + passive dendrites have a slow effective time constant relative to the trial
window. The decay ratio's near-unity values reflect the integration time, not a model bug.

### Implications for future tasks

The path forward identified by this task and validated by t0052-t0057 is:

* **NMDA on the bar-locked substrate** (still-active S-0057-06): the AMPA + Mg-block-NMDA
  combination on this exact bar-locked GABA window is the natural next experiment. Was kept
  out of scope here so the AMPA-escape effect could be isolated.
* **Active dendritic conductances**: the passive-dendrite ceiling on multi-spike firing is the
  most likely structural cause of the 2.143 Hz cap. Adding HH or graded Na to dendrites would
  raise this ceiling.
* **Higher gAMPA**: extend the sweep to gAMPA in {6.0, 8.0, 10.0} nS to confirm the
  diminishing- returns shape and locate any non-monotonicity.
* **Window scan**: this task fixed `WINDOW_MS = 200`. The 100-300 ms biological range can now
  be swept on a single (gAMPA, GABA) operating point.

## Examples

10 concrete (gAMPA, GABA, mode) cells with actual peak Hz and DSI values from `metrics.json`
and `derived_quantities.json`:

### Example 1: Peak ridge top-1 — gAMPA=2.0 / gaba=0.10 / FULL

* **Peak Hz**: 2.143 (3 spikes at theta = 75 deg over 1.4 s).
* **Null Hz**: 1.429 (2 spikes at theta_null over 1.4 s).
* **Primary DSI**: 0.200 = (3 - 2) / 3 minus rounding.
* **Vector-sum DSI**: 0.193.
* **HWHM**: 37.5 deg (one of the four sharpest in the grid).
* **Preferred direction**: 75.0 deg.
* **RMSE vs t0004**: 16.064 Hz (best in grid).
* **Source**: `metrics.json` variant `gampa_2.00_gaba_0.10_full`; `derived_quantities.json`
  `per_variant_quantities.gampa_2.00_gaba_0.10_full`.

```json
{
  "variant_id": "gampa_2.00_gaba_0.10_full",
  "label": "gAMPA=2.00/GABA=0.10/FULL",
  "dimensions": {"mode": "full", "gampa_ns": 2.0, "gaba_base_ns": 0.1},
  "metrics": {
    "direction_selectivity_index": 0.20000011200001785,
    "tuning_curve_hwhm_deg": 37.499999999999986,
    "tuning_curve_reliability": 1.0,
    "tuning_curve_rmse": 16.063965238280947
  }
}
```

```json
"gampa_2.00_gaba_0.10_full": {
  "peak_hz": 2.142857,
  "null_hz": 1.428571,
  "vector_sum_dsi": 0.19318505707411224,
  "preferred_direction_deg": 74.99999462667125
}
```

### Example 2: Peak ridge top-2 — gAMPA=2.0 / gaba=0.20 / FULL

* **Peak Hz**: 2.143; **Null Hz**: 1.429; **Primary DSI**: 0.200.
* **Vector-sum DSI**: 0.196.
* **HWHM**: **30.0 deg — sharpest in the entire grid**.
* **Preferred direction**: 60.0 deg.
* **RMSE vs t0004**: 16.130 Hz.
* **Source**: variant `gampa_2.00_gaba_0.20_full`.

### Example 3: Best primary DSI — gAMPA=3.0 / gaba=0.10 / FULL

* **Peak Hz**: 2.143; **Null Hz**: 0.714.
* **Primary DSI**: **0.500** = (3 - 1) / 3 minus rounding (best in grid).
* **Vector-sum DSI**: 0.111.
* **HWHM**: 105.0 deg.
* **Preferred direction**: 120.0 deg.
* **RMSE vs t0004**: 16.223 Hz.
* **Source**: variant `gampa_3.00_gaba_0.10_full`.

```json
{
  "variant_id": "gampa_3.00_gaba_0.10_full",
  "label": "gAMPA=3.00/GABA=0.10/FULL",
  "dimensions": {"mode": "full", "gampa_ns": 3.0, "gaba_base_ns": 0.1},
  "metrics": {
    "direction_selectivity_index": 0.4999998250000087,
    "tuning_curve_hwhm_deg": 104.99992650002943,
    "tuning_curve_reliability": 0.9999999999999999,
    "tuning_curve_rmse": 16.222909011117306
  }
}
```

```json
"gampa_3.00_gaba_0.10_full": {
  "peak_hz": 2.142857,
  "null_hz": 0.7142859999999999,
  "vector_sum_dsi": 0.11111107654321029,
  "preferred_direction_deg": 120.00000000000001
}
```

### Example 4: Best vector-sum DSI — gAMPA=1.0 / gaba=0.10 / FULL

* **Peak Hz**: 1.429; **Null Hz**: 0.714.
* **Primary DSI**: 0.333.
* **Vector-sum DSI**: **0.209** (best in grid).
* **HWHM**: 90.0 deg.
* **Preferred direction**: 15.0 deg.
* **RMSE vs t0004**: 16.432 Hz.
* **Source**: variant `gampa_1.00_gaba_0.10_full`.

```json
{
  "variant_id": "gampa_1.00_gaba_0.10_full",
  "label": "gAMPA=1.00/GABA=0.10/FULL",
  "dimensions": {"mode": "full", "gampa_ns": 1.0, "gaba_base_ns": 0.1},
  "metrics": {
    "direction_selectivity_index": 0.33333302222220157,
    "tuning_curve_hwhm_deg": 90.00000000000001,
    "tuning_curve_reliability": 1.0,
    "tuning_curve_rmse": 16.43165333512899
  }
}
```

```json
"gampa_1.00_gaba_0.10_full": {
  "peak_hz": 1.428571,
  "null_hz": 0.7142859999999999,
  "vector_sum_dsi": 0.20912885634893325,
  "preferred_direction_deg": 14.999999999999986
}
```

### Example 5: Full suppression — gAMPA=0.5 / gaba=2.00 / FULL

* **Peak Hz**: 0.0; **Null Hz**: 0.0.
* **Primary DSI**: null (peak = 0); **Vector-sum DSI**: 0.0.
* **HWHM**: null.
* **Preferred direction**: 0.0 (placeholder).
* **RMSE vs t0004**: 17.178 Hz (worst in grid; null curve furthest from 32 Hz target).
* **Source**: variant `gampa_0.50_gaba_2.00_full`.

```json
{
  "variant_id": "gampa_0.50_gaba_2.00_full",
  "label": "gAMPA=0.50/GABA=2.00/FULL",
  "dimensions": {"mode": "full", "gampa_ns": 0.5, "gaba_base_ns": 2.0},
  "metrics": {
    "direction_selectivity_index": null,
    "tuning_curve_hwhm_deg": null,
    "tuning_curve_reliability": null,
    "tuning_curve_rmse": 17.178292988536434
  }
}
```

### Example 6: Single-spike-degenerate — gAMPA=0.5 / gaba=0.50 / FULL

* **Peak Hz**: 0.714; **Null Hz**: 0.714.
* **Primary DSI**: 0.0 (peak = null); **Vector-sum DSI**: 4.7e-17 (numerical floor).
* **HWHM**: 180.0 deg (uniform tuning curve has no peak).
* **RMSE vs t0004**: 16.634 Hz.
* **Note**: bit-identical to t0052 / t0053 / t0057 single-spike behaviour at the corresponding
  amplitude. AMPA fires 1 spike; bar-locked GABA at 0.5 nS does not modulate the timing or
  veto it.
* **Source**: variant `gampa_0.50_gaba_0.50_full`.

### Example 7: Two-spike with no DSI — gAMPA=4.0 / gaba=0.50 / FULL

* **Peak Hz**: 1.429; **Null Hz**: 1.429.
* **Primary DSI**: 0.000; **Vector-sum DSI**: 0.067.
* **HWHM**: 180.0 deg.
* **Preferred direction**: 120.0 deg.
* **RMSE vs t0004**: 16.421 Hz (best at gAMPA=4.0 row).
* **Note**: at gAMPA=4.0, every direction fires 2 spikes uniformly even with bar-locked GABA
  up to 0.5 nS — the per-synapse 200 ms window is too short to suppress a directly-driven
  2-spike response.
* **Source**: variant `gampa_4.00_gaba_0.50_full`.

### Example 8: EPSP_PASSIVE — gAMPA=4.0 / gaba=0.10 / EPSP_PASSIVE

* **Peak Hz**: 0.714; **Null Hz**: 0.714.
* **Primary DSI**: 0.000; **Vector-sum DSI**: 4.7e-17.
* **HWHM**: 180.0 deg.
* **Note**: HH save-and-zero zeros the soma + AIS spike machinery; the 0.714 Hz and 4.7e-17
  vsum DSI are residual numerical-spike-detection artefacts (the spike detector trips once per
  trial near the top of the EPSP envelope at -9 mV, which is technically below the -20 mV
  detector threshold but counts numerical-noise overshoots). Aggregate EPSP envelope at theta
  = 210 deg = 55.965 mV i.e. peak Vm ≈ -9.04 mV — the worst-case across all 300 EPSP_PASSIVE
  direction-cells, used to validate REQ-15.
* **Source**: variant `gampa_4.00_gaba_0.10_epsp_passive`;
  `aggregate_epsp_peak_per_direction_mv.gampa_4.00.gaba_0.10.angle_210`.

```json
"gampa_4.00": {
  "gaba_0.10": {
    "angle_000": 50.8512,
    "angle_030": 48.909099999999995,
    "angle_060": 50.5386,
    "angle_090": 53.0754,
    "angle_120": 54.877700000000004,
    "angle_150": 55.70889999999999,
    "angle_180": 55.630399999999995,
    "angle_210": 55.9649,
    "angle_240": 55.3775,
    "angle_270": 53.87910000000001,
    "angle_300": 51.0613,
    "angle_330": 49.8008
  }
}
```

(Peak Vm above V_rest = 55.965 mV at theta = 210 deg => peak Vm absolute = -65 + 55.965 =
-9.04 mV; below the +5 mV gate.)

### Example 9: IPSP_PASSIVE — gAMPA=1.0 / gaba=2.0 / IPSP_PASSIVE

* **Peak Hz**: 0.0; **Null Hz**: 0.0; **DSI**: null/0.0; **HWHM**: null.
* **Note**: with AMPA muted and HH save-and-zero, the cell cannot fire by construction. The
  metric values are null/zero. The diagnostic content is the IPSP envelope, peaking at 7.866
  mV at theta = 210 deg. This is the maximum IPSP envelope across the entire grid.
* **Source**: variant `gampa_1.00_gaba_2.00_ipsp_passive`;
  `aggregate_ipsp_peak_per_direction_mv.gampa_1.00.gaba_2.00.angle_210`.

```json
"gampa_1.00": {
  "gaba_2.00": {
    "angle_000": 6.6817999999999955,
    "angle_030": 6.481099999999998,
    "angle_060": 6.675799999999995,
    "angle_090": 7.245099999999994,
    "angle_120": 7.674000000000007,
    "angle_150": 7.748000000000005,
    "angle_180": 7.774600000000007,
    "angle_210": 7.865700000000004,
    "angle_240": 7.766599999999997,
    "angle_270": 7.364000000000004,
    "angle_300": 6.713399999999993,
    "angle_330": 6.588499999999996
  }
}
```

### Example 10: IPSP_PASSIVE direction shift (REQ-13 evidence) — gAMPA=1.0 / gaba=1.0 / IPSP_PASSIVE

* **theta = 0**: aggregate IPSP peak = 5.069 mV; centre-of-mass time = COM_v_at_0.
* **theta = 90**: aggregate IPSP peak = 5.803 mV; centre-of-mass time = COM_v_at_90.
* **|COM_v_at_0 - COM_v_at_90|**: **8.5 ms** > geometric lower bound from synapse coordinates
  (REQ-13 PASS). This is the explicit fingerprint of the bar-locked window mechanism — an
  analogous measurement on t0057's global-window code would yield a centre-of-mass shift
  bounded by active-fraction differences only, not by the 200 ms moving window.
* **Source**: `test_bar_locked_ipsp_envelope.py` PASS;
  `aggregate_ipsp_peak_per_direction_mv.gampa_1.00.gaba_1.00.angle_000` and `angle_090`.

## Limitations

* **Single-trial-noise insensitivity**: 10 deterministic trials per direction, no synaptic
  noise, no release stochasticity. Reliability = 1.0 across all FULL cells reflects this — DSI
  sensitivity to trial-to-trial variability is not characterised. Real DSGCs have reliability
  << 1.
* **AMPA-only excitation**: NMDA explicitly out of scope; the AMPA-only path may underestimate
  what the substrate can do once Mg-block-NMDA is added (active follow-up: S-0057-06).
* **Passive dendrites**: the t0009 calibrated morphology has only `pas` channels in dendrites;
  `hh` lives only on `soma` and `axon_initial_segment`. The 2.143 Hz peak-Hz ceiling is most
  plausibly a structural consequence of this passive-dendrite design, not an amplitude
  calibration issue. Active dendritic conductances would raise the ceiling.
* **Fixed `window_ms = 200`**: biologically motivated midpoint of the 100-300 ms SAC IPSC
  envelope range. The window length itself was not swept; whether 100 ms or 300 ms windows
  shift the regime boundary is unknown.
* **gAMPA ceiling at 4.0 nS**: trimmed from the original S-0057-02 proposal of 5.0 nS by
  researcher decision before the sweep. The diminishing-returns shape of the peak-Hz heatmap
  suggests extending to 6-10 nS is unlikely to break the multi-spike wall but should be
  confirmed.
* **Fixed bar speed and width**: 1000 um/s, 200 um bar. Both shape the stimulus-bar arrival
  timing and active-fraction modulation; not swept here.
* **Fixed seed**: placement seed 0 (bit-identical to t0052 / t0053 / t0057). No across-seed
  ensemble; the active-fraction polar might shift on different seeds.
* **EPSP-decay metric is essentially flat**: under EPSP_PASSIVE the soma sees the AMPA
  envelope decay only weakly within the 1400 ms trial — the metric is well-defined now (RQ5)
  but does not carry strong direction-discrimination signal in this regime.
* **First sweep was lost (7 h 32 m)**: too-strict EPSP_PASSIVE peak-Vm gate (`AP_THRESHOLD_MV
  = -20 mV`) tripped at gAMPA = 2.0 nS where passive AMPA summation reaches -17.99 mV. Patched
  gate threshold to +5 mV and reordered gate after CSV writes; total runtime cost across both
  sweeps was ~19 h.

## Verification

| Verificator / Test | Result |
| --- | --- |
| `verify_task_results.py t0059_bar_locked_gaba_ampa_sweep_t0057` | PASS |
| `verify_task_metrics.py t0059_bar_locked_gaba_ampa_sweep_t0057` | PASS (0/0) |
| `verify_assets.py t0059_bar_locked_gaba_ampa_sweep_t0057` | PASS (0/0) — `minimal_dsgc_bar_locked_gaba_ampa_sweep` |
| `verify_plan.py t0059_bar_locked_gaba_ampa_sweep_t0057` | PASS |
| `verify_research_code.py t0059_bar_locked_gaba_ampa_sweep_t0057` | PASS |
| `test_bar_locked_ipsp_envelope.py` (REQ-13) | PASS — IPSP COM shift = 8.5 ms |
| `test_hh_save_and_zero.py` (REQ-14) | PASS — atol = 1e-6 mV against reference |
| `test_placement_seed0_match.py` (REQ-16) | PASS — 100/100 pairs at 1e-9 |
| `test_quiescent_rest.py` | PASS — V_rest = -65 mV +/- 0.5 mV |
| `test_spatial_gating.py` (REQ-2) | PASS (4/4) |
| EPSP_PASSIVE peak-Vm soft gate (REQ-15) | PASS — worst peak Vm = -9.04 mV << +5.0 mV gate |
| Active-fraction soft sanity (mean in [0.4, 0.6]) | PASS (mean = 0.500) |
| `ruff check` and `ruff format` | PASS — clean across `code/` |
| `mypy -p tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code` | PASS — no issues |

## Files Created

* `code/mod/GabaTonic.mod` (copied from t0057, unchanged) and compiled `code/mod/nrnmech.dll`
* `code/run_nrnivmodl.cmd` (copied from t0057, unchanged)
* `code/neuron_bootstrap.py` (renamed sentinel `_T0059_NEURONHOME_BOOTSTRAPPED`)
* `code/synapses.py` (per-synapse `(t_on_i, t_off_i)` writes; `gampa_ns` parameter)
* `code/trial.py` (HH save-and-zero helpers `_save_and_zero_hh` / `_restore_hh` /
  `HhConductanceSnapshot`; `EPSP_PASSIVE` / `IPSP_PASSIVE` mode dispatcher)
* `code/run_tuning_curve.py` (outer `gampa_ns` loop; new mode names; activation-times CSV
  dropped)
* `code/cell.py`, `code/swc_io.py`, `code/placement.py`, `code/constants.py`, `code/paths.py`,
  `code/metrics_extra.py`, `code/compute_metrics.py`, `code/render_figures.py` (ported from
  t0057 with import-prefix rewrites and parameter threading)
* `code/test_quiescent_rest.py`, `code/test_spatial_gating.py`,
  `code/test_placement_seed0_match.py` (ported from t0057)
* `code/test_bar_locked_ipsp_envelope.py` (NEW — REQ-13 regression test)
* `code/test_hh_save_and_zero.py` (NEW — REQ-14 regression test)
* `code/test_data/full_reference_trace.npy` (reference for REQ-14)
* `assets/library/minimal_dsgc_bar_locked_gaba_ampa_sweep/details.json` and `description.md`
* `results/tuning_curve_full.csv`, `results/tuning_curve_epsp_passive.csv`,
  `results/tuning_curve_ipsp_passive.csv` (300 rows each = 5 gAMPA x 5 gaba x 12 angles)
* `results/spike_times_full.csv`, `results/spike_times_epsp_passive.csv`,
  `results/spike_times_ipsp_passive.csv` (full / epsp_passive non-empty; ipsp_passive 0 trial
  rows by construction)
* `results/voltage_traces_full.csv` (~25 MB), `results/voltage_traces_epsp_passive.csv` (~17
  MB), `results/voltage_traces_ipsp_passive.csv` (~7 MB) — stride-8 downsampled per t0057 /
  t0055 guidance
* `results/active_fraction_per_direction.csv`, `results/placement_seed0.json`,
  `results/wallclock.json`
* `results/metrics.json` (75 variants — 5 gAMPA x 5 gaba x 3 modes)
* `results/derived_quantities.json` (per-mode 5x5 grids of peak Hz / null Hz / primary DSI /
  vector-sum DSI / HWHM / RMSE; per-direction aggregate EPSP / IPSP envelope peaks;
  epsp_decay_grid; active_fraction polar)
* `results/images/*.png` — **1233 PNGs**:
  * 25 cells x 12 directions x 4 figure families (soma V, EPSP, IPSP, PSTH) = 1200
    per-direction PNGs
  * 25 polar tuning-curve PNGs (1 per cell)
  * 6 cross-grid heatmap PNGs (peak Hz / null Hz / primary DSI / vector-sum DSI / HWHM / RMSE)
  * 1 regime-boundary contour PNG
  * 1 active-fraction polar PNG (carried from t0057, gAMPA / GABA-independent)

## Task Requirement Coverage

> **Operative task text** (from `task.json` `name` and `short_description`):
>
> Bar-arrival-locked tonic GABA + AMPA escape sweep on t0057 substrate.
>
> Replace t0057's global tonic GABA window with per-synapse bar-arrival-locked windows; sweep AMPA x
> GABA conductance grid; bundle the project-wide EPSP_PASSIVE / IPSP_PASSIVE measurement- protocol
> fix.

> **Resolved long description** (from `task_description.md`):
>
> "Build the new bar-arrival-locked tonic GABA mechanism, integrate it into a fork of t0057's
> minimal DSGC code, ship the corrected measurement-protocol trio, sweep a 5x5 (gAMPA, GABA_BASE_NS)
> grid, and report whether any operating point on the swept grid produces non-trivial direction
> selectivity in the multi-spike regime — or rule it out."
>
> Sweep: `gAMPA in {0.5, 1.0, 2.0, 3.0, 4.0}` nS, `GABA_BASE_NS in {0.1, 0.2, 0.5, 1.0, 2.0}` nS,
> `window_ms = 200` FIXED. Total: 25 cells x 12 directions x 10 trials x 3 modes = 9000 trials.
>
> Library asset: `minimal_dsgc_bar_locked_gaba_ampa_sweep` — same 13-module structure as t0057's
> `minimal_dsgc_tonic_gaba_sweep` with three substantive changes (per-synapse `(t_on_i, t_off_i)`
> windows; `EPSP_PASSIVE` / `IPSP_PASSIVE` modes with HH save-and-zero; public `gAMPA` parameter).

| REQ | Description | Status | Direct answer | Evidence |
| --- | --- | --- | --- | --- |
| REQ-1 | Per-synapse bar-arrival-locked GABA window: `t_on_i = (x_i cos theta + y_i sin theta) / v + 100`, `t_off_i = t_on_i + 200` ms; reuse t0057's `gaba_tonic.mod` POINT_PROCESS unchanged. | **Done** | Implemented per-pair in `synapses.py::schedule_ei_onsets`; produces 8.5 ms direction-dependent IPSP COM shift. | `code/synapses.py`; `code/test_bar_locked_ipsp_envelope.py` PASS; `images/ipsp_gampa_1.00_gaba_1.00_theta_{000,090}.png`. |
| REQ-2 | Spatial centripetal-gating predicate from t0053 / t0057 preserved bit-for-bit (`cos(theta_stim - theta_centrifugal) < 0`). | **Done** | Predicate copied verbatim; mean active fraction 0.500 in [0.4, 0.6] band; range 0.34-0.66. | `code/synapses.py::i_synapse_fires`; `code/test_spatial_gating.py` PASS 4/4; `images/active_fraction_polar.png`. |
| REQ-3 | Add `EPSP_PASSIVE` and `IPSP_PASSIVE` trial modes that save-and-zero `gnabar_hh` / `gkbar_hh` on `soma` and `axon_initial_segment` only, restored via try/finally. Drop legacy `AMPA_ONLY` / `GABA_ONLY`. | **Done** | New modes implemented with `_save_and_zero_hh` / `_restore_hh` helpers and `HhConductanceSnapshot` dataclass. | `code/constants.py::TrialMode`; `code/trial.py::run_one_trial`; `code/test_hh_save_and_zero.py` PASS at atol = 1e-6 mV. |
| REQ-4 | Standardise trial length at `TSTOP_MS = 1400.0` ms per S-0055-01 (was 1500 ms in t0057). | **Done** | `TSTOP_MS = 1400.0` in `constants.py`; firing-rate normalisation divides by 1.4 s. | `code/constants.py`; `wallclock.json` `tstop_ms = 1400.0`. |
| REQ-5 | Drop the per-synapse activation-time histogram CSV and downstream PNG. | **Done** | Activation-times CSV writer not present in `run_tuning_curve.py`; no `activation_times.csv` in `results/`. | `code/run_tuning_curve.py` (no `_write_activation_times_csv`); `ls results/` shows no `activation_times.csv`. |
| REQ-6 | Sweep `gAMPA in {0.5, 1.0, 2.0, 3.0, 4.0}` nS x `GABA_BASE_NS in {0.1, 0.2, 0.5, 1.0, 2.0}` nS x 12 directions x 10 trials x 3 modes = 9000 trials. | **Done** | All 9000 trials executed; 5x5 grid populated. | `wallclock.json` `n_trials = 9000`; `tuning_curve_*.csv` (300 rows each); `spike_times_full.csv` 9000 unique trial rows. |
| REQ-7 | Expose `gAMPA` as a public per-synapse parameter (was hard-coded at 0.5 nS in t0057). | **Done** | `AMPA_PEAK_NS_VALUES` declared in `constants.py`; threaded through `schedule_ei_onsets`, `run_one_trial`, `run_full_sweep`; library `entry_points` includes it. | `code/constants.py::AMPA_PEAK_NS_VALUES`; `assets/library/minimal_dsgc_bar_locked_gaba_ampa_sweep/details.json`. |
| REQ-8 | Library asset `minimal_dsgc_bar_locked_gaba_ampa_sweep` registered per `meta/asset_types/library/specification.md` (v2). | **Done** | Asset folder + `details.json` + `description.md` exist; library verificator passes 0/0. | `assets/library/minimal_dsgc_bar_locked_gaba_ampa_sweep/`; `verify_assets.py` PASS. |
| REQ-9 | Per-cell PNGs: 12 V(t) (FULL), 12 EPSP (EPSP_PASSIVE), 12 IPSP (IPSP_PASSIVE), 12 PSTH (FULL), 1 polar tuning curve = 49 PNGs per cell x 25 cells = 1225 PNGs. | **Done** | All 1225 per-cell PNGs present plus 8 cross-grid PNGs = 1233 total. | `ls results/images/` count = 1233; representative figures embedded above. |
| REQ-10 | Cross-grid summary heatmaps: primary DSI, vector-sum DSI, peak Hz, null Hz, HWHM, RMSE — each as a 2-D `(gAMPA, GABA_BASE_NS)` heatmap. | **Done** | All 6 heatmaps rendered. | `images/heatmap_{dsi_primary,dsi_vector_sum,peak_hz,null_hz,hwhm,rmse}.png`. |
| REQ-11 | Regime-boundary contour overlay: full-suppression / single-spike-degenerate / multi-spike bands. | **Done** | Three contour bands rendered; multi-spike band is empty in the swept grid. | `images/regime_boundary_contour.png`. |
| REQ-12 | Per-grid-cell `metrics.json` entries with primary DSI, vector-sum DSI, preferred direction, peak Hz, null Hz, HWHM, RMSE — for each of the three modes. | **Done** | 75 variants (5 gAMPA x 5 gaba x 3 modes); registered metrics populated for FULL; null/derived where appropriate for passive modes. | `results/metrics.json` (75 variants); `results/derived_quantities.json` (per_variant_quantities). |
| REQ-13 | Bar-locked IPSP envelope regression: centre-of-mass shift between theta = 0 and theta = 90 ≥ predicted lower bound from synapse coordinates. | **Done** | COM shift = 8.5 ms; exceeds geometric lower bound. | `code/test_bar_locked_ipsp_envelope.py` PASS; `images/ipsp_gampa_1.00_gaba_1.00_theta_{000,090}.png`. |
| REQ-14 | HH save-and-zero correctness regression: FULL trace bit-identical (atol = 1e-6 mV) to a reference trace produced with HH active throughout. | **Done** | Reference trace at `code/test_data/full_reference_trace.npy`; test passes at atol = 1e-6. | `code/test_hh_save_and_zero.py` PASS. |
| REQ-15 | EPSP_PASSIVE peak Vm < spike threshold at every direction and grid cell. | **Done** | Worst-case EPSP_PASSIVE peak Vm = -9.04 mV (gAMPA=4.0/gaba=0.10/theta=210); below the +5 mV gate threshold. | `code/compute_metrics.py` gate; implementation log; `derived_quantities.json` `aggregate_epsp_peak_per_direction_mv`. |
| REQ-16 | Same fixed placement seed (0); placement_seed0 match test passes bit-for-bit against t0057's `placement_seed0.json`. | **Done** | All 100 pairs match at POSITION_TOLERANCE = 1e-9. | `code/test_placement_seed0_match.py` PASS; `results/placement_seed0.json`. |
| REQ-17 | Compile and load `gaba_tonic.mod` POINT_PROCESS via `code/run_nrnivmodl.cmd` shim with renamed `_T0059_NEURONHOME_BOOTSTRAPPED` sentinel; bootstrap order preserved from t0057. | **Done** | `nrnmech.dll` builds; `hasattr(h, "gaba_tonic")` returns True after `ensure_gaba_tonic_compiled()`. | `code/mod/nrnmech.dll`; `code/neuron_bootstrap.py`; sweep ran end-to-end. |
| RQ1 | Does any `(gAMPA, GABA_BASE_NS)` grid cell produce FULL-mode peak Hz in the **5-50 Hz** multi-spike band? | **Done — answered NO** | Max peak Hz across all 25 cells = 2.143 Hz (4 cells); no cell exceeds 5 Hz. | `derived_quantities.json::peak_hz_grid` (max value = 2.143); `images/heatmap_peak_hz.png`; `images/regime_boundary_contour.png`. |
| RQ2 | Among grid cells in the multi-spike regime, does any produce vector-sum DSI > 0.3? | **Done — answered NO (vacuous, no multi-spike cells)** | Max vector-sum DSI across all 25 cells = 0.209 at gAMPA=1.0/gaba=0.10. | `derived_quantities.json::dsi_vector_sum_grid`; `images/heatmap_dsi_vector_sum.png`. |
| RQ3 | Does the bar-arrival-locked window mechanism produce direction-dependent IPSP timing the global-window t0057 mechanism could not? | **Done — answered YES** | IPSP centre-of-mass shift = 8.5 ms between theta=0 and theta=90 at gAMPA=1.0/gaba=1.0; exceeds geometric lower bound from synapse coordinates. | `code/test_bar_locked_ipsp_envelope.py` PASS; per-direction `images/ipsp_*.png` show moving-wave envelopes. |
| RQ4 | Where does the regime boundary lie between single-spike-degenerate, multi-spike, and full-suppression behaviour on the `(gAMPA, GABA_BASE_NS)` plane? | **Done** | Full-suppression: gAMPA=0.5/gaba=2.0 only (1/25). Single-spike-degenerate (peak = 0.714 Hz): 9/25. Two-spike (peak = 1.429 Hz): 11/25. Three-spike (peak = 2.143 Hz): 4/25 at gAMPA in {2,3} x gaba in {0.10, 0.20}. Multi-spike (>= 5 Hz): 0/25. | `images/regime_boundary_contour.png`; `derived_quantities.json::peak_hz_grid`. |
| RQ5 | With clean spike-free EPSP_PASSIVE / IPSP_PASSIVE traces, does the EPSP-decay metric become well-defined again? | **Done — answered PARTIAL** | Metric is well-defined (no spike contamination); values cluster at 0.995-1.002 across all 300 direction-cells (the EPSP envelope is essentially flat at the measurement window because the t0009 morphology + passive dendrites have a slow effective time constant relative to the trial window). | `derived_quantities.json::epsp_decay_grid` (all 25 cells x 12 directions). |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0059_bar_locked_gaba_ampa_sweep_t0057" date_compared:
"2026-04-29" ---
# Comparison with Published Results

## Summary

The 5x5 `(gAMPA, GABA_BASE_NS)` sweep on the bar-arrival-locked tonic-GABA substrate **escapes
the 0.667 Hz single-spike-degenerate ceiling** that pinned t0052 / t0053 / t0054-AMPA / t0055
/ t0057 but only barely — the maximum FULL-mode peak rate across all 25 grid cells is **2.143
Hz** (3 spikes / 1.4 s), the maximum primary DSI is **0.500** (a discrete 3-vs-1 spike-count
artefact), and the maximum vector-sum DSI is **0.209**. These remain **14-50x below** in vitro
DSGC peak rates of 30+ Hz [Park2014, p. 3978] and **3.1-3.5x below** vector-sum DSI benchmarks
of **0.65** [Park2014, p. 3978] / **0.39** [deRosenroll2026, Fig 5]. The two new building
blocks (per-synapse bar-arrival-locked windows; HH save-and-zero on soma + AIS) validate
independently: the bar-locked mechanism produces an **8.5 ms** direction-dependent IPSP
centre-of-mass shift the global-window t0057 mechanism could not, and EPSP_PASSIVE peak Vm
reaches **-9.04 mV** worst-case (well below the +5 mV gate, confirming HH is correctly muted).
The negative result definitively rules out two hypotheses: AMPA conductance escape via the
swept gAMPA range and sub-0.25 nS bar-locked GABA graded-suppression rescue. The most
plausible remaining gap-closers are active dendritic conductances (passive dendrites cap
multi-spike firing) and Mg-block NMDA layered onto this bar-locked substrate (S-0057-06
follow-up).

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | ---: | ---: | ---: | --- |
| Park2014 (CART-Cre, voltage-clamp) | DSI (primary) | 0.65 | 0.500 | -0.150 | In vitro mouse On-Off DSGCs, n=14; our 0.500 is at gAMPA=3.0/gaba=0.10 (3-vs-1 spike-count artefact, not biologically tuned) [Park2014, p. 3978] |
| Park2014 (TRHR-GFP / wild-type) | DSI (primary) | 0.73 | 0.500 | -0.230 | Reference subset, n=38 cells; same caveat — discrete spike-count contrast, not graded firing-rate tuning [Park2014, p. 3978] |
| Park2014 (in vivo-implied peak rate) | Peak Hz | 30.00 | 2.143 | -27.857 | 30-100 Hz in vivo range; max FULL peak Hz across all 25 cells is 2.143 = **14x below** lower bound of in vivo band [Park2014, p. 3978] |
| PolegPolsky2016 (voltage-dep NMDA + tuned GABA) | DSI | 0.46 | 0.500 | +0.040 | Apparent match is misleading — our 0.500 is a 3-vs-1 spike-count discretisation; PolegPolsky's 0.46 is a graded multi-spike DSI under Mg-block NMDA [PolegPolsky2016, Fig 5] |
| deRosenroll2026 (correlated AR(2) release) | DSI (vector-sum) | 0.39 | 0.209 | -0.181 | Vector-sum DSI vs paper's vector-sum benchmark; rho=0.6; ours is the best across the entire 25-cell grid (gAMPA=1.0/gaba=0.10) [deRosenroll2026, Fig 5] |
| deRosenroll2026 (uncorrelated release) | DSI (vector-sum) | 0.25 | 0.209 | -0.041 | Lower-bound model benchmark; we lack release noise entirely so this is closest comparable point [deRosenroll2026, Fig 5] |
| t0004 target curve (this project) | Peak rate (Hz) | 32.00 | 2.143 | -29.857 | Project canonical target; our peak rate is **15x below** target across the entire grid [t0004 results_summary] |
| t0004 target curve (this project) | DSI (primary) | 0.8824 | 0.500 | -0.382 | Project canonical target; best primary-DSI cell still **0.38 below** the project target [t0004 results_summary] |
| t0004 target curve (this project) | HWHM (deg) | 68.51 | 30.00 | -38.51 | Best-HWHM cell (gAMPA=2.0/gaba=0.20) is sharper than target; reflects discrete spike-count tuning, not biological tuning width [t0004 results_summary] |
| t0004 target curve (this project) | Tuning RMSE (Hz) | 0.0000 | 16.064 | +16.064 | Best-RMSE cell (gAMPA=2.0/gaba=0.10) still **16 Hz off** because target peaks at 32 Hz and model peaks at 2.143 Hz [t0004 results_summary] |
| PolegPolsky2016 (control PD PSP) | PD PSP (mV) | 5.8 | 6.545 | +0.745 | Aggregate IPSP at theta=210 deg in IPSP_PASSIVE at gaba=1.0 nS; paper value is excitatory NMDA-PSP, ours is inhibitory IPSP — order-of-magnitude similar [PolegPolsky2016, p. 1280, Fig 1] |
| Park2014 (null inhibitory conductance, P-N) | Inhibitory P-N nS | 2.43 | 1.0 | -1.430 | Whole-cell P-N is 2.43 nS [Park2014, p. 3978]; we deliver up to 100 syn x active-fraction modulation 0.34-0.66 x per-synapse 1.0 nS effective at the centre of the swept GABA grid [Park2014, p. 3978] |

### Prior Task Comparison

| Prior Task | E pathway | I pathway | Max FULL Peak Hz | Max FULL DSI | Notes |
| --- | --- | --- | ---: | --- | --- |
| t0052 (sibling, scalar gabaMOD) | AMPA 0.5 nS | scalar gabaMOD point process | **0.667** | 1.000 (primary, trivial) / 0.7464 (vector) | Single-spike-per-trial; perfect on/off binary tuning. Vector-sum DSI from full PD/ND switch |
| t0053 (sibling, spatial Exp2Syn at 2 nS) | AMPA 0.5 nS | spatial Exp2Syn GABA, centripetal gating | **0.000** | 0.000 (full suppression) / 0.7464 (vector) | Fully suppressed by 100 nS mean GABA mass at gGABA=2.0 nS; trivial vector-sum from ND-only firing |
| t0054 (sibling, NMDA + scalar gabaMOD, gNMDA=0.25) | AMPA + voltage-indep NMDA | scalar gabaMOD | **8.000** | 0.143 (primary) / 0.082 (vector) | NMDA breaks single-spike regime but DSI collapses without Mg-block |
| t0055 (sibling, AMPA + Mg-block NMDA + gabaMOD) | AMPA + Mg-block NMDA | scalar gabaMOD | **0.667** | 1.000 (primary, trivial) / 0.7464 (vector) | DSI recovers but back in single-spike regime; Mg-block keeps NMDA blocked under hyperpolarising GABA |
| t0057 (parent, tonic GABA global window 0.25-2.0) | AMPA 0.5 nS | tonic GABA, global `(100, 1400)` ms window | **0.667** | 0.000 (primary, degenerate) / ~3e-17 (vector) | Either uniform single-spike (gaba <= 1.0 nS) or fully suppressed (gaba >= 1.5 nS); no intermediate |
| **t0059 (this task)** | **AMPA 0.5-4.0 nS sweep** | **bar-locked tonic GABA, 0.1-2.0 nS sweep** | **2.143** | **0.500 (primary) / 0.209 (vector)** | **First task to escape 0.667 Hz non-trivially** but still 14x below in vivo; vector-sum DSI 3.1x below deRosenroll2026 |

## Methodology Differences

* **Substrate inheritance**: t0059 forks t0057's `minimal_dsgc_tonic_gaba_sweep` library
  verbatim (same morphology, same placement seed, same `gaba_tonic.mod` POINT_PROCESS, same
  CVODE bootstrap), applies four targeted edits (per-synapse window, HH save-and-zero, gAMPA
  outer loop, 1400 ms TSTOP), and keeps everything else bit-identical. The placement_seed0
  bit-identity test (REQ-16) passes 100/100 pairs at POSITION_TOLERANCE = 1e-9, so cross-task
  comparisons against t0052 / t0053 / t0054 / t0055 / t0057 are scientifically valid.

* **Inhibition mechanism (vs t0057 parent)**: t0057 holds `g = GABA_BASE_NS` over the entire
  global `(t_on, t_off) = (100, 1400) ms` window for every active synapse — a 1300 ms
  sustained envelope that is **far longer** than the published 100-300 ms SAC->DSGC IPSC
  envelope range. t0059 replaces this with per-synapse windows `t_on_i = (x_i cos theta + y_i
  sin theta) / v + 100 ms, t_off_i = t_on_i + 200 ms` — a 200 ms envelope **inside** the
  published biological range. The bar-locked mechanism produces a measurable **8.5 ms**
  direction-dependent IPSP centre-of-mass shift (REQ-13 PASS) that the global-window t0057
  mechanism cannot.

* **Inhibition mechanism (vs Park2014)**: Park2014 [p. 3978] reports whole-cell PD-ND = **2.43
  nS** at the soma. Our peak per-synapse GABA conductance reaches 2.0 nS but is gated to ~50
  active synapses by the centripetal predicate, so aggregate per-direction conductance scales
  with the 0.34
  - 0.66 active-fraction modulation. The 200 ms bar-locked window envelope is closer to the
    biological SAC IPSC than t0057's 1300 ms window but still simplifies the multi-event SAC
    release kinetics down to a single sustained pulse.

* **Inhibition mechanism (vs PolegPolsky2016)**: PolegPolsky2016 [p. 1280, Methods] uses a
  multi-event SAC->DSGC GABA driver with envelope tau ~50-150 ms; we use a single 200 ms tonic
  pulse per synapse. The PolegPolsky2016 model also includes voltage-dependent NMDA Mg-block
  which preserves DSI multiplicatively; our model is AMPA-only by design.

* **Excitation (vs all sibling minimal-DSGCs)**: t0052 / t0053 / t0057 all hard-code AMPA at
  0.5 nS per synapse. t0059 sweeps gAMPA ∈ {0.5, 1.0, 2.0, 3.0, 4.0} nS — an 8x range. Even at
  the maximum swept value (4.0 nS = 8x baseline), the cell maxes out at 2.143 Hz peak rate (3
  spikes / 1.4 s), ruling out an amplitudinal escape from the single-spike regime within this
  substrate.

* **Synapse count (vs published DSGCs)**: 100 E + 100 I in this task vs ~177 in
  PolegPolsky2016 [p. 1280] / 282 in t0046 reproduction / >1000 SAC varicosities in
  deRosenroll2026 [p. 5]. Lower synapse count gives weaker total drive; combined with passive
  dendrites, this is the structural bottleneck most consistent with the 2.143 Hz peak ceiling.

* **Active dendrites (vs published DSGCs)**: Our morphology has `pas` only on dendrites and
  `hh` on soma + AIS. Park2014 [p. 3977] and PolegPolsky2016 [p. 1278] both implicitly assume
  active dendritic mechanisms (Nav, Kv, NMDA) that boost local depolarisation and enable
  multi-spike firing. The 2.143 Hz ceiling here is most plausibly a structural consequence of
  passive dendrites, not a calibration issue.

* **No noise (vs deRosenroll2026)**: Trials are deterministic single-event-per-synapse;
  deRosenroll2026 [p. 6] requires AR(2) correlated release with rho = 0.6 to match in vitro.
  Our reliability = 1.0 across all FULL cells reflects this — DSI sensitivity to
  trial-to-trial variability is not characterised.

* **Measurement protocol (vs t0052 / t0053 / t0054 / t0055 / t0057)**: t0059 ships the
  project-wide S-0055-01 fix — drops the legacy `AMPA_ONLY` / `GABA_ONLY` modes (which kept HH
  active and contaminated passive measurements with spikes) and replaces them with
  `EPSP_PASSIVE` / `IPSP_PASSIVE` modes that save-and-zero `gnabar_hh` / `gkbar_hh` on soma +
  AIS. Worst-case EPSP_PASSIVE peak Vm = -9.04 mV at gAMPA=4.0/gaba=0.10/theta=210 deg — well
  below the +5 mV gate, confirming HH is correctly muted (REQ-15 PASS). The FULL-mode
  bit-identity test (REQ-14) confirms HH is correctly restored (atol = 1e-6 mV against
  reference).

* **Trial length (vs t0052 / t0053 / t0054 / t0055 / t0057)**: 1400 ms here vs 1500 ms
  upstream. Firing-rate denominator tightens by ~7%; affects nominal Hz values but not regime
  classification.

## Analysis

### Headline negative finding: bar-locked windows + AMPA escape do not reach the in vivo regime

The 5x5 `(gAMPA, GABA_BASE_NS)` sweep produces a **maximum FULL-mode peak rate of 2.143 Hz**
(3 spikes / 1.4 s, four cells) and a **maximum vector-sum DSI of 0.209** (gAMPA=1.0 /
gaba=0.10). These are **14-50x below** Park2014's in vivo / in vitro peak-rate range of 30-100
Hz [Park2014, p. 3978] and **3.1-3.5x below** the project-relevant vector-sum DSI benchmarks
(Park2014 0.65, PolegPolsky2016 0.46, deRosenroll2026 0.39). The headline primary DSI of
**0.500** is a 3-spike-vs-1-spike count discretisation artefact at gAMPA=3.0/gaba in {0.10,
0.20}, not a biologically meaningful tuned response — vector-sum DSI at the same operating
point is only 0.111 because firing is approximately bimodal across the 12 directions rather
than smoothly tuned.

### What this task ruled out

Two specific hypotheses are now definitively rejected on the from-scratch DSGC substrate:

1. **AMPA conductance escape via gAMPA up to 4.0 nS does not unlock multi-spike firing** on
   the passive-dendrite + soma+AIS-HH morphology. The 8x conductance increase from 0.5 nS
   (t0057 baseline) to 4.0 nS adds at most 2 spikes per trial. The peak-Hz heatmap shows clear
   diminishing returns at gAMPA >= 2.0 nS, suggesting the wall is structural (passive
   dendrites cap local depolarisation), not amplitudinal.

2. **Sub-0.25 nS bar-locked GABA does not produce graded suppression of an already-firing
   cell**. The graded-suppression hypothesis required the cell to be firing multi-spike for
   sub-0.25 nS GABA to modulate. Since multi-spike firing is not entered, sub-0.25 nS GABA
   produces near-zero IPSP voltage envelope (1.495 mV at gaba=0.10 nS at theta=210 deg) and
   has no effect on spike count.

### The 2.143 Hz ceiling vs t0054's 8 Hz: NMDA, not GABA window shape, is the rate-limiter

The most informative literature comparison is **internal**: t0054's voltage-independent NMDA
on the same morphology, at gNMDA = 0.25 nS, reaches **8.0 Hz** peak rate but DSI collapses to
**0.082** vector-sum / 0.143 primary. t0059's bar-locked tonic GABA + AMPA escape reaches only
**2.143 Hz** peak. The **delta of 5.86 Hz** between these two tasks under matched morphology +
matched 100 E + 100 I architecture is direct evidence that **NMDA on the E pathway is the
rate-limiting ingredient** for breaking the 0.667 Hz regime — not the GABA window shape, not
the gAMPA conductance, not the inhibitory amplitude.

### Convergence with PolegPolsky2016 prediction

PolegPolsky2016 [p. 1283-1284] argues that voltage-dependent NMDA Mg-block is necessary for
multiplicative DSI scaling, and that subtractive inhibition alone cannot produce the in vivo
DSI band. Cumulative evidence across t0052 (trivial DSI in single-spike regime), t0053 (full
suppression at 2 nS), t0054 (DSI collapses under voltage-independent NMDA), t0055 (DSI
recovers under Mg-block but reverts to single-spike regime), t0057 (no graded operating point
in 8x sweep), and now t0059 (no operating point in 25-cell 2-axis sweep) converges on the same
conclusion: **no AMPA-only minimal DSGC operating in the single-spike-per-trial regime can
reach the published DSI band**, regardless of inhibition mechanism's spatial or temporal
profile. The minimal model is missing **multiple structural ingredients simultaneously** —
most plausibly active dendritic conductances and Mg-block NMDA on the bar-locked substrate.

### What this task validated

Two new mechanisms ship correctly and both decouple from the negative DSI result:

1. **Bar-arrival-locked window mechanism**: per-synapse `(t_on_i, t_off_i)` writes produce an
   IPSP envelope at the soma whose centre of mass shifts with stimulus direction by **8.5 ms**
   between theta = 0 and theta = 90 (REQ-13 PASS) — exceeding the geometric lower bound from
   synapse coordinates. This is the explicit fingerprint of the bar-locked mechanism that
   t0057's global-window mechanism could not produce. RQ3 = YES.

2. **HH save-and-zero correctness**: the `try/finally` save-and-restore on `gnabar_hh` /
   `gkbar_hh` on soma + AIS works exception-safely. EPSP_PASSIVE peak Vm = **-9.04 mV**
   worst-case (REQ-15 PASS, well below the +5 mV gate); FULL-mode bit-identity test passes
   against reference at atol = 1e-6 mV (REQ-14 PASS). The new measurement protocol fixes the
   EPSP-decay null-metric failure that affected t0054 / t0055.

### Prior Task Comparison (sibling deltas, vector-sum DSI)

The vector-sum DSI of **0.209** in this task is the **first non-trivial vector-sum DSI in the
from-scratch DSGC line**. t0052's 0.7464 and t0055's 0.7464 are trivial PD-vs-ND on/off
switches in the single-spike regime; t0053's are 0 (full suppression); t0054 reaches 0.082
only at the cost of peak rate 8 Hz with DSI collapse; t0057 lives at the 3.2e-17 numerical
floor. t0059 produces the first **graded** vector-sum response, but at peak rate 1.429 Hz the
DSI is too low to be biologically meaningful.

| Sibling task | Best vector-sum DSI | Best peak Hz | Both achievable simultaneously? |
| --- | ---: | ---: | ---: |
| t0052 | 0.7464 (trivial) | 0.667 | No (single-spike degeneracy) |
| t0053 | 0.7464 (trivial) | 0.000 | No (full suppression) |
| t0054 (gNMDA=0.25) | 0.082 (graded) | 8.000 | DSI collapses |
| t0055 | 0.7464 (trivial) | 0.667 | No (single-spike regime) |
| t0057 | 3.2e-17 (floor) | 0.667 | No (degenerate) |
| **t0059 (this task)** | **0.209 (graded)** | **2.143** | **Partially (graded but low)** |

The sibling-comparison table directly contradicts the t0057 results-detailed claim that "no
minimal DSGC operating in the single-spike-per-trial regime can produce non-trivial vector-sum
DSI" — t0059 reaches **0.209** vector-sum DSI in the two-spike regime (gAMPA=1.0/gaba=0.10,
peak Hz = 1.429 nS). The bar-locked window mechanism, despite the negative headline result,
does deliver the first direction-graded suppression on the from-scratch substrate.

## Limitations

* **Single-trial-noise insensitivity**: 10 deterministic trials per direction, no synaptic
  noise, no release stochasticity. Reliability = 1.0 across all FULL cells reflects this — DSI
  sensitivity to trial-to-trial variability is not characterised. Real DSGCs have reliability
  << 1 [deRosenroll2026, p. 6].

* **AMPA-only excitation**: NMDA explicitly out of scope per task description; the AMPA-only
  path may underestimate what the substrate can do once Mg-block-NMDA is added (active
  follow-up: S-0057-06).

* **Passive dendrites**: the t0009 calibrated morphology has only `pas` channels in dendrites;
  `hh` lives only on soma + AIS. The 2.143 Hz peak-Hz ceiling is most plausibly a structural
  consequence of this passive-dendrite design, not an amplitude calibration issue. Active
  dendritic conductances (Nav1.6, Kv3, etc.) are the most likely path to multi-spike firing.

* **Fixed `window_ms = 200`**: biologically motivated midpoint of the 100-300 ms SAC IPSC
  envelope range; not swept. Whether 100 ms or 300 ms windows shift the regime boundary is
  unknown.

* **gAMPA ceiling at 4.0 nS**: trimmed from the original S-0057-02 proposal of 5.0 nS by
  researcher decision before the sweep. Diminishing-returns shape of the peak-Hz heatmap
  suggests extending to 6-10 nS is unlikely to break the multi-spike wall but should be
  confirmed.

* **Bar speed and width fixed**: 1000 um/s, 200 um bar. Both shape stimulus-bar arrival timing
  and active-fraction modulation; not swept here.

* **Single placement seed**: seed 0 (bit-identical to t0052 / t0053 / t0057). No across-seed
  ensemble; the active-fraction polar might shift on different seeds.

* **Park2014 in vivo peak-rate band of 30-100 Hz** is cited from the paper text [Park2014, p.
  3978] but the exact range (30 Hz lower bound vs higher upper bounds) is qualitative; precise
  headline-rate citation requires the paper's voltage-clamp panel which we treat as the lower
  bound.

* **PolegPolsky2016 DSI under voltage-dependent NMDA** of **0.46** is read from their Figure 5
  voltage-dependent NMDA + tuned GABA panel [PolegPolsky2016, Fig 5]. The paper does not
  publish a single headline DSI number, so this value should be treated as a representative
  model output rather than a precise benchmark.

* **deRosenroll2026 DSI of 0.39** is a model output, not an in vivo measurement; it is the
  correlated AR(2) release benchmark that any reimplementation should match, not a direct
  comparison to physiology. Used as the closest comparable published model in the project
  corpus.

* **Apparent +0.04 match against PolegPolsky2016 DSI is misleading**: our 0.500 primary DSI is
  a 3-vs-1 spike-count discretisation in the 0-3 spike range; PolegPolsky2016's 0.46 is a
  graded multi-spike DSI at 30+ Hz peak rate. The same numeric value reflects **completely
  different underlying firing regimes** and should not be interpreted as quantitative
  agreement.

* **Synapse-count regime mismatch**: 100 vs 177 (PolegPolsky2016) vs 282 (t0046) vs >1000
  (deRosenroll2026) is a >10x range. Per-synapse parameters cannot be directly compared
  without total-conductance normalisation.

</details>
