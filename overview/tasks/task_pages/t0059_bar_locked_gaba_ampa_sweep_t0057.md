# ⏹ Bar-arrival-locked tonic GABA + AMPA escape sweep on t0057 substrate

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0059_bar_locked_gaba_ampa_sweep_t0057` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Source suggestion** | `S-0057-04` |
| **Task types** | `build-model`, `experiment-run` |
| **Expected assets** | 1 library |
| **Task folder** | [`t0059_bar_locked_gaba_ampa_sweep_t0057/`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/) |

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
