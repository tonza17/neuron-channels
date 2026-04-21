# ✅ V_rest sweep tuning curves for t0022 and t0024 DSGC ports

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0026_vrest_sweep_tuning_curves_dsgc` |
| **Status** | ✅ completed |
| **Started** | 2026-04-21T12:47:42Z |
| **Completed** | 2026-04-21T17:43:26Z |
| **Duration** | 4h 55m |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Task types** | `experiment-run`, `data-analysis` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`synaptic-integration`](../../by-category/synaptic-integration.md), [`voltage-gated-channels`](../../by-category/voltage-gated-channels.md) |
| **Expected assets** | 2 predictions |
| **Step progress** | 10/15 |
| **Task folder** | [`t0026_vrest_sweep_tuning_curves_dsgc/`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/task_description.md)*

# V_rest sweep tuning curves for t0022 and t0024 DSGC ports

## Motivation

Two of the four DSGC compartmental-model ports in this project
(`modeldb_189347_dsgc_channel_testbed` from t0022 and `de_rosenroll_2026_dsgc` from t0024)
produce direction-selective tuning curves at the default resting potential of `-60 mV`. The
project's research questions (RQ1, RQ4) ask how the cell's biophysics — particularly
voltage-gated-channel availability and dendritic integration — shape tuning. Resting potential
is the single most direct experimental knob for probing those mechanisms because it controls:

1. **Na channel inactivation availability**: at hyperpolarized holding (e.g. `-90 mV`) the
   fast sodium gate sits in its deinactivated state, producing a larger pool available for
   spiking; at depolarized holding (e.g. `-30 mV`) a large fraction is tonically inactivated.
2. **NMDA receptor Mg block**: the voltage-dependent Mg block relieves as the membrane
   depolarizes, so NMDA contribution to synaptic integration grows with V_rest. This should
   shift the E/I balance that implements asymmetric inhibition in both ports.
3. **Leak driving force and input resistance**: with `eleak` pinned to a new holding, the leak
   current's reversal and the cell's apparent input resistance both change, altering how
   strong BIP/SAC input currents look to the soma.

The two driver paradigms under test — deterministic per-dendrite E-I scheduling in t0022
versus AR(2)-correlated stochastic release in t0024 — should respond differently to V_rest
because they differ in how they compose inhibitory current magnitude against voltage-gated
drive.

## Scope

Run a V_rest sweep on both ports. All other protocol knobs (bar velocity, 12 angles, tstop,
morphology) are held fixed to the defaults of the respective library assets.

### V_rest values

Exactly eight values, all in mV: `-90, -80, -70, -60, -50, -40, -30, -20`.

### Holding strategy

At every V_rest value, set **both** `V_INIT_MV` **and** `ELEAK_MV` (leak reversal) to the
sweep value before initialising NEURON. Moving only `v_init` re-settles to `eleak` within a
few milliseconds and does not implement a true resting-potential shift; moving only `eleak`
leaves the initial condition mismatched. Both must move together.

### Models and trial budgets

| Model | Task | Driver | Trials per angle | Total trials |
| --- | --- | --- | --- | --- |
| `modeldb_189347_dsgc_channel_testbed` | t0022 | Deterministic per-dendrite E-I | 1 | 1 × 12 × 8 = 96 |
| `de_rosenroll_2026_dsgc` (correlated `rho=0.6`) | t0024 | AR(2)-correlated stochastic release | 10 | 10 × 12 × 8 = 960 |

One trial per angle is sufficient for t0022 because its driver is deterministic; only the
V_rest value changes between (angle, V_rest) runs. Ten trials per angle are retained for t0024
so that trial-to-trial variance in the AR(2) release process remains visible in the tuning
curve — lower counts would fold V_rest effects into noise.

### Protocol

For each model and each V_rest value, run the existing 12-angle protocol (`0, 30, 60, …, 330`
degrees) using the library asset's stock `run_trial` / `run_one_trial` function. Only override
the two holding-potential constants — do not modify the library asset itself (immutability
rule 5) and do not change bar velocity, tstop, or any other constant.

## Approach

### Implementation

Two thin wrapper drivers live in `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/`:

* `run_vrest_sweep_t0022.py` — imports from `tasks.t0022_modify_dsgc_channel_testbed.code`,
  parameterises `V_REST_MV`, sets both `h.v_init` and every leak section's `e` parameter to
  that value, then invokes the stock tuning-curve routine across the 12 angles. Loops the 8
  V_rest values serially.
* `run_vrest_sweep_t0024.py` — same idea against
  `tasks.t0024_port_de_rosenroll_2026_dsgc.code`. Uses the correlated `rho=0.6` AR(2) path
  (the task's headline condition).

Each wrapper writes one CSV per V_rest value under `data/t0022/` or `data/t0024/`, then
concatenates them into `data/t0022/vrest_sweep_tidy.csv` and `data/t0024/vrest_sweep_tidy.csv`
with columns `(v_rest_mv, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`. Also
records per-V_rest wall time to `data/t0022/wall_time_by_vrest.json` and
`data/t0024/wall_time_by_vrest.json`.

### Analysis

A single analysis script computes, for each (model, V_rest):

* Preferred direction and DSI (reusing the t0012 `tuning_curve_loss` scorer's DSI formula)
* Peak firing rate (Hz)
* Null-direction firing rate (Hz)
* HWHM (degrees)

Those values are written to `data/t0022/vrest_metrics.csv` and `data/t0024/vrest_metrics.csv`,
and summary tables are embedded in `results/results_detailed.md`.

### Plots (all in `results/images/`)

* 16 individual polar plots: `polar_<model>_vrest_<value>.png` (one per model × V_rest pair,
  plotting firing rate in Hz vs direction in degrees on a polar axis).
* 2 overlay polar plots: `polar_overlay_t0022.png` and `polar_overlay_t0024.png` showing all 8
  V_rest tuning curves on the same polar axes with a perceptually ordered colormap. Each
  answers the question "how does the tuning curve morph as V_rest moves from hyperpolarized to
  depolarized?"
* 2 Cartesian summary plots: `dsi_vs_vrest.png` and `peak_hz_vs_vrest.png` with both models
  overlaid, showing how DSI and peak firing rate trend with V_rest.

## Expected Assets

Two predictions assets, one per model. Each contains:

* `details.json` (predictions asset metadata following `meta/asset_types/predictions/`)
* The full tidy CSV as the predictions payload
* A short description linking back to this task and the source model's library asset

`expected_assets` in `task.json` is `{"predictions": 2}`.

## Dependencies

* `t0022_modify_dsgc_channel_testbed` — provides the `modeldb_189347_dsgc_channel_testbed`
  library asset and the `run_tuning_curve.py` driver that this task reuses.
* `t0024_port_de_rosenroll_2026_dsgc` — provides the `de_rosenroll_2026_dsgc` library asset
  and the correlated-AR(2) driver.

Both dependencies are completed and on main.

## Compute and Budget

* No remote compute, no paid API calls, no GPUs.
* Runs entirely on the local Windows workstation using the existing NEURON + Python stack.
* Expected wall time: ~25 min for t0022 (96 trials) + ~4 h 15 min for t0024 (960 trials at
  scale comparable to t0024's original 800-trial run).
* Total budget: `$0`.

## Metrics

Register the following if not already registered in `meta/metrics/` (propose as suggestions
otherwise; do not block on meta gaps):

* `dsi_at_vrest_<mv>` for each V_rest value
* `peak_hz_at_vrest_<mv>` for each V_rest value
* `hwhm_deg_at_vrest_<mv>` for each V_rest value
* `efficiency_wall_time_per_trial_seconds` (one value per model — total wall time / total
  trial count)

## Output Specification

### Charts (all in `results/images/`, embedded in `results_detailed.md`)

| Chart | Axes | Question answered |
| --- | --- | --- |
| `polar_<model>_vrest_<value>.png` | θ = direction (deg), r = firing rate (Hz) | What is the tuning curve shape at this specific V_rest? |
| `polar_overlay_<model>.png` | θ = direction (deg), r = firing rate (Hz), 8 curves | How does the tuning curve morph with V_rest? |
| `dsi_vs_vrest.png` | x = V_rest (mV), y = DSI, 2 lines (one per model) | Is there a V_rest that maximises direction selectivity? |
| `peak_hz_vs_vrest.png` | x = V_rest (mV), y = peak firing rate (Hz), 2 lines | Where is peak firing rate highest? Does the 40-80 Hz envelope open up? |

### Tables in `results_detailed.md`

* Per-(model, V_rest) metrics: V_rest, DSI, peak_hz, null_hz, HWHM, wall_time_s
* Per-model aggregate efficiency: total trials, total wall time, seconds per trial

## Key Questions

1. Does either DSGC port show a V_rest value at which DSI is higher than at the default `-60
   mV` baseline?
2. Does either port reach the t0004 target peak-firing-rate envelope (40-80 Hz) at any V_rest
   value? This is the headline unresolved problem across all four existing ports.
3. Is the direction-selectivity mechanism in t0022 (deterministic per-dendrite E-I) more or
   less V_rest-dependent than in t0024 (AR(2) stochastic release)?
4. At what V_rest does each port silence (all-angle firing rate ≈ 0 Hz) on the hyperpolarized
   end, and at what V_rest does it enter depolarization block on the depolarized end?
5. Does HWHM narrow systematically as V_rest increases (depolarization-driven gain change), or
   is it relatively flat across the sweep (consistent with inhibition-dominated tuning)?

## Source Suggestion

None. Researcher-directed experiment captured in brainstorming session 5
(`t0025_brainstorm_results_5`).

</details>

## Metrics

### t0022 DSGC @ V_rest=-90 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.4852** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **0.7753** |

### t0022 DSGC @ V_rest=-80 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.5999** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **0.7664** |

### t0022 DSGC @ V_rest=-70 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.6368** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **83.961** |

### t0022 DSGC @ V_rest=-60 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.6555** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **86.25** |

### t0022 DSGC @ V_rest=-50 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.2047** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **102.1875** |

### t0022 DSGC @ V_rest=-40 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0952** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |

### t0022 DSGC @ V_rest=-30 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.046** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |

### t0022 DSGC @ V_rest=-20 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.2751** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **107.8125** |

### t0024 DSGC @ V_rest=-90 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.6746** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **65.1786** |

### t0024 DSGC @ V_rest=-80 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.5489** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **68.4375** |

### t0024 DSGC @ V_rest=-70 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.4698** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **70.4545** |

### t0024 DSGC @ V_rest=-60 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.4463** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **78.4737** |

### t0024 DSGC @ V_rest=-50 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.5601** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **69.9519** |

### t0024 DSGC @ V_rest=-40 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.6248** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **67.7038** |

### t0024 DSGC @ V_rest=-30 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.5898** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **66.4904** |

### t0024 DSGC @ V_rest=-20 mV

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.3606** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **83.2867** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| predictions | [V_rest sweep on t0022 DSGC channel testbed (deterministic)](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/assets/predictions/t0026-vrest-sweep-t0022/) | [`description.md`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/assets/predictions/t0026-vrest-sweep-t0022/description.md) |
| predictions | [V_rest sweep on t0024 DSGC channel testbed (stochastic AR(2) release)](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/assets/predictions/t0026-vrest-sweep-t0024/) | [`description.md`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/assets/predictions/t0026-vrest-sweep-t0024/description.md) |

## Suggestions Generated

<details>
<summary><strong>Register dsi_at_vrest and peak_hz_at_vrest metric keys in
meta/metrics/</strong> (S-0026-01)</summary>

**Kind**: technique | **Priority**: medium

This task produced direction_selectivity_index and peak firing rate per V_rest but the keys
dsi_at_vrest_<value> and peak_hz_at_vrest_<value> are not registered under meta/metrics/. Add
metric definitions so future V_rest sweeps can report through the registered key registry and
appear in aggregate_metric_results output. Also reshape t0026 metrics.json variants from the
current map form to the array form required by task_results_specification.md multi-variant
format.

</details>

<details>
<summary><strong>Sweep AR(2) rho x V_rest for t0024 to separate noise correlation
from depolarisation effects</strong> (S-0026-02)</summary>

**Kind**: experiment | **Priority**: high

The t0024 V_rest sweep ran only at rho=0.6 and showed a 1.9x U-shaped DSI curve with HWHM
pinned at 65-83 deg. Repeat the sweep at rho in {0.0, 0.3, 0.6, 0.9} to test whether the
tuning-smoothing is dominated by AR(2) correlation or by the depolarisation itself. Expected
outcome: rho=0.0 should recover tuning sharpness closer to t0022 while preserving the
Na-inactivation-independent peak firing behaviour.

</details>

<details>
<summary><strong>Sweep bar velocity x V_rest on both DSGC ports to test
velocity-V_rest interaction</strong> (S-0026-03)</summary>

**Kind**: experiment | **Priority**: medium

Sivyer2010 reports DSI varies with velocity (0.45-0.57) at natural V_rest. Our current sweep
fixed velocity at the t0022/t0024 defaults. Repeat the 8-value V_rest sweep at 3-5 bar
velocities to check whether V_rest modulates the velocity-tuning curve or only the
direction-tuning curve. Expected runtime: ~4x current (t0022) and ~4x current (t0024) if 4
velocities are tested.

</details>

<details>
<summary><strong>Parallelise the t0024 sweep across CPU cores to cut wall time from
3.21 h to under 1 h</strong> (S-0026-04)</summary>

**Kind**: library | **Priority**: medium

The t0024 sweep took 11,562 s (3.21 h) because NEURON ran single-threaded on one CPU. Each
(V_rest, direction, trial) combination is embarrassingly parallel. Build a ProcessPoolExecutor
wrapper that farms out trials across cores; with 8 workers we expect wall time to drop below 1
h. This will make V_rest x rho and V_rest x velocity sweeps practical.

</details>

<details>
<summary><strong>Port Hanson2019 DSGC model and repeat V_rest sweep to test
starburst-independent DS hypothesis</strong> (S-0026-05)</summary>

**Kind**: experiment | **Priority**: medium

Hanson2019 reports DSI 0.33 in the absence of asymmetric starburst amacrine cell responses,
suggesting an alternative mechanism. If the Hanson model is ported and swept over the same
eight V_rest values, we can compare its V_rest sensitivity against our t0022 (strongly
V_rest-dependent) and t0024 (U-shaped) results. Would clarify whether V_rest-dependence of DSI
is a universal signature or specific to starburst-driven models.

</details>

<details>
<summary><strong>Add NMDA-block and TTX-sensitivity sweeps at each V_rest to isolate
biophysical mechanism</strong> (S-0026-06)</summary>

**Kind**: experiment | **Priority**: high

Our V_rest sweep shows t0022 loses tuning at depolarised V_rest (DSI 0.046 at V=-30 mV) while
t0024 stays flat (DSI>=0.36). Two candidate mechanisms are Na channel inactivation and NMDA
Mg-block relief. Run the sweep once with TTX-like Na-block (g_Na=0) and once with NMDA-block
(g_NMDA=0) to isolate which channel class drives each model's V_rest sensitivity.

</details>

<details>
<summary><strong>Extend sweep upward to V_rest in {-15, -10, -5} mV to capture the
post-collapse regime in t0024</strong> (S-0026-07)</summary>

**Kind**: experiment | **Priority**: low

Model t0022 peak firing collapses from 129 Hz at V=-30 to 26 Hz at V=-20 due to Na
inactivation, but t0024 still rises monotonically to 7.6 Hz at V=-20 with no collapse.
Extending the t0024 sweep to V_rest >= -20 mV would reveal whether t0024 also exhibits a
Na-inactivation collapse (suggesting shared mechanism at higher depolarisations) or remains
depolarisation-insensitive (suggesting NMDA-dominated signalling).

</details>

## Research

* [`research_code.md`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/results_summary.md)*

# Results Summary: V_rest sweep tuning curves for t0022 and t0024 DSGC ports

## Summary

Swept resting potential across eight values (**-90 mV to -20 mV in 10 mV steps**) for two DSGC
compartmental models under the standard 12-direction moving-bar protocol. Model t0022
(deterministic ModelDB 189347 port) ran **96 trials** (~6.0 min wall time); model t0024 (de
Rosenroll 2026 port with AR(2)-correlated stochastic release at rho=0.6) ran **960 trials**
(~3.21 h wall time). Both models show strong V_rest dependence but with qualitatively
different shapes: t0022 peaks DSI sharply at V_rest=-60 mV, while t0024 is U-shaped with
maxima at the extremes.

## Metrics

* **t0022 DSI range**: **0.046** (V=-30 mV) to **0.6555** (V=-60 mV) — 14x modulation
* **t0024 DSI range**: **0.3606** (V=-20 mV) to **0.6746** (V=-90 mV) — 1.9x modulation,
  U-shaped
* **t0022 peak firing rate**: **6 Hz** at V=-90 mV, monotone up to **129 Hz** at V=-30 mV,
  collapses to **26 Hz** at V=-20 mV (Na inactivation)
* **t0024 peak firing rate**: **1.5 Hz** at V=-90 mV, monotone up to **7.6 Hz** at V=-20 mV
  (no hyper-depolarisation collapse)
* **t0022 HWHM**: 0.77 deg at V≤-80 mV (near-binary curve) vs. 180 deg at V=-30/-40 mV
  (complete loss of tuning)
* **t0024 HWHM**: **65-83 deg** across the full V_rest range — AR(2) noise smooths tuning
* **Total trials executed**: 1,056 (96 + 960) across both models

## Verification

* `verify_logs.py` — PASSED (0 errors) after step 9 implementation commit
* `verify_task_file.py` — PASSED (0 errors) — task.json confirms `expected_assets =
  {"predictions": 2}`
* `verify_implementation.py` — PASSED for both predictions assets (expected PR-W014 model_id
  null \+ PR-W015 dataset_ids empty, both correct)
* Per-model tidy CSV row counts: **96** (t0022) and **960** (t0024), matching REQ-3 and REQ-4
  exactly
* Override unit test `vrest_override_smoke.py` — PASSED: every HHst-bearing and pas-bearing
  section responds to `set_vrest(h, -20.0)`

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0026_vrest_sweep_tuning_curves_dsgc" ---
# Detailed Results: V_rest sweep tuning curves for t0022 and t0024 DSGC ports

## Summary

This task swept the resting potential of the two most recent DSGC compartmental models (t0022
deterministic ModelDB 189347 port and t0024 de Rosenroll 2026 port with AR(2)-correlated
stochastic release) across eight values from **-90 mV to -20 mV in 10 mV increments** and ran
the standard 12-direction moving-bar protocol at each V_rest. The deterministic t0022 sweep
used 1 trial per angle (8 x 12 x 1 = **96 trials**); the stochastic t0024 sweep used 10 trials
per angle at rho=0.6 (8 x 12 x 10 = **960 trials**). V_rest was moved by simultaneously
overriding `h.v_init`, every section's `eleak_HHst`, and every section's `e_pas` before each
trial's `h.finitialize`, producing a true resting-potential shift rather than a transient
initial-condition tweak. Both models show strong V_rest dependence, but the *shape* of the
dependence differs qualitatively between the two release paradigms. All five key questions
from the task description are answered with numeric evidence and plot references below.

## Methodology

### Machine specs

* Local Windows 11 workstation (Sheffield CICS Dell OptiPlex), **no remote compute**
* Single-threaded CPU NEURON 8.2.7 with compiled mechanism .dll
* Python 3.12 inside `uv`-managed environment; matplotlib for plotting; stdlib `csv`/`json`
  for I/O

### Runtime and timestamps

| Phase | Start | End | Wall time |
| --- | --- | --- | --- |
| Implementation step (9) | 2026-04-21T13:17:45Z | 2026-04-21T18:30:00Z | ~5.2 h (coding + both sweeps) |
| t0022 sweep (96 trials) | — | — | **6.0 min** (~3.8 s/trial) |
| t0024 sweep (960 trials) | — | — | **11,562 s (3.21 h)** (~12.0 s/trial) |
| Results step (12) | 2026-04-21T17:17:59Z | (in progress) | — |

Per-V_rest wall times for t0024 (from `data/t0024/wall_time_by_vrest.json`) ranged from
**1,403 s (V=-30 mV)** to **1,581 s (V=-90 mV)** — hyperpolarised runs spend more wall time
because the initial settle requires more steps to reach a stable subthreshold state.

### Models and drivers

* **t0022 port**: ModelDB 189347 DSGC channel testbed (library asset
  `modeldb_189347_dsgc_channel_testbed`). Deterministic per-dendrite E-I schedule. HHst
  soma/axon, pas dendrites.
* **t0024 port**: de Rosenroll 2026 DSGC (library asset `de_rosenroll_2026_dsgc`).
  AR(2)-correlated stochastic per-dendrite glutamate/GABA release at rho=0.6 (default
  correlated condition). HHst soma, pas dendrites.

Both drivers were adapted (not modified — library assets are immutable per rule 5) into thin
wrappers at `code/trial_runner_t0022.py` and `code/trial_runner_t0024.py`. The V_rest override
`set_vrest(h, v_rest_mv)` from `code/vrest_override.py` runs **after** `apply_params` and
**before** `h.finitialize` on every trial, writing V_rest to `h.v_init`, to every section's
`eleak_HHst`, and to every section's `e_pas`. This was chosen over a `v_init`-only override
because `v_init` alone re-settles to `eleak` within a few milliseconds of `h.finitialize` and
does not produce a true steady-state resting-potential shift.

### Protocol

Twelve directions (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330 deg). For each
direction the bar moved through the cell's receptive field at the library asset's default
velocity, tstop, and temperature. Per-trial outcomes recorded: `spike_count` (soma threshold
crossings), `peak_mv` (max somatic voltage), and `firing_rate_hz` (spike_count / 1.0 s).

Per-V_rest metrics (DSI, peak firing rate, null firing rate, HWHM, preferred direction) were
computed in `code/compute_vrest_metrics.py` using the Mazurek vector-sum DSI convention
(`|sum_i r_i * exp(i*theta_i)| / sum_i r_i`) and 1-degree linear interpolation around the
preferred direction for HWHM.

### Metrics Tables

**t0022 (deterministic) — 96 trials total:**

| V_rest (mV) | Peak Hz | Null Hz | DSI | HWHM (deg) | Pref dir (deg) | Mean peak (mV) |
| --- | --- | --- | --- | --- | --- | --- |
| -90 | **6.00** | 0.00 | **0.4852** | 0.78 | 19.4 | -22.1 |
| -80 | 11.00 | 0.00 | 0.5999 | 0.77 | 42.3 | -6.7 |
| -70 | 12.00 | 0.00 | 0.6368 | 83.96 | 50.7 | -5.8 |
| -60 | **15.00** | 0.00 | **0.6555** | 86.25 | 49.3 | -4.9 |
| -50 | 41.00 | 20.41 | 0.2047 | 102.19 | 42.4 | 43.7 |
| -40 | 70.00 | 50.64 | 0.0952 | 180.00 | 49.1 | 43.6 |
| -30 | **129.00** | 111.20 | **0.0460** | 180.00 | 48.0 | 43.4 |
| -20 | 26.00 | 7.40 | 0.2751 | 107.81 | 48.0 | 41.8 |

**t0024 (AR(2)-correlated stochastic, rho=0.6) — 960 trials total:**

| V_rest (mV) | Peak Hz | Null Hz | DSI | HWHM (deg) | Pref dir (deg) | Mean peak (mV) |
| --- | --- | --- | --- | --- | --- | --- |
| -90 | 1.50 | 0.00 | **0.6746** | 65.18 | 351.6 | -14.8 |
| -80 | 2.70 | 0.06 | 0.5489 | 68.44 | 350.4 | 5.2 |
| -70 | 4.00 | 0.26 | 0.4698 | 70.45 | 355.6 | 21.4 |
| -60 | 5.00 | 0.51 | **0.4463** | 78.47 | 0.9 | 28.8 |
| -50 | 6.30 | 0.30 | 0.5601 | 69.95 | 6.8 | 16.4 |
| -40 | 6.80 | 0.00 | 0.6248 | 67.70 | 10.7 | 13.5 |
| -30 | 7.40 | 0.16 | 0.5898 | 66.49 | 11.5 | 20.3 |
| -20 | **7.60** | 1.88 | 0.3606 | 83.29 | 11.9 | 35.1 |

Bold rows in each table mark the DSI maximum (best direction selectivity) and the
peak-firing-rate extremes worth attention.

## Visualizations

### Per-V_rest polar plots (t0022)

![t0022 V_rest = -90
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0022_vrest_-90mV.png)
![t0022 V_rest = -80
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0022_vrest_-80mV.png)
![t0022 V_rest = -70
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0022_vrest_-70mV.png)
![t0022 V_rest = -60
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0022_vrest_-60mV.png)
![t0022 V_rest = -50
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0022_vrest_-50mV.png)
![t0022 V_rest = -40
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0022_vrest_-40mV.png)
![t0022 V_rest = -30
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0022_vrest_-30mV.png)
![t0022 V_rest = -20
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0022_vrest_-20mV.png)

### Per-V_rest polar plots (t0024)

![t0024 V_rest = -90
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0024_vrest_-90mV.png)
![t0024 V_rest = -80
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0024_vrest_-80mV.png)
![t0024 V_rest = -70
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0024_vrest_-70mV.png)
![t0024 V_rest = -60
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0024_vrest_-60mV.png)
![t0024 V_rest = -50
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0024_vrest_-50mV.png)
![t0024 V_rest = -40
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0024_vrest_-40mV.png)
![t0024 V_rest = -30
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0024_vrest_-30mV.png)
![t0024 V_rest = -20
mV](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0024_vrest_-20mV.png)

### Overlay polar plots

![t0022 overlay: all 8 V_rest
curves](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0022_overlay.png)
![t0024 overlay: all 8 V_rest
curves](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/polar_t0024_overlay.png)

### Cartesian summary plots

![t0022 summary: peak/null Hz, DSI, HWHM vs
V_rest](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/summary_t0022_vrest.png)
![t0024 summary: peak/null Hz, DSI, HWHM vs
V_rest](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images/summary_t0024_vrest.png)

## Analysis

### Q1 — Does either port show DSI higher than at the -60 mV baseline?

**t0022: No.** The DSI peak is **0.6555 at V=-60 mV**, which is also the baseline. All other
V_rest values have lower DSI. The closest competitor is V=-70 mV (DSI=0.6368, -3%), then V=-80
mV (DSI=0.5999, -8%). Moving away from -60 mV in either direction degrades DSI.

**t0024: Yes, substantially.** DSI at V=-60 mV is **0.4463** (the *minimum* across the sweep).
The maximum is **0.6746 at V=-90 mV** (+51% over the -60 mV baseline); V=-40 mV is a close
second at **0.6248** (+40%). The shape is U-shaped: DSI falls from both extremes toward V=-60
mV. This is a major qualitative finding — the t0024 model has two operating regimes
(hyperpolarised and mildly depolarised) that yield stronger direction tuning than its default.

### Q2 — Does either port reach the t0004 target envelope of 40-80 Hz peak firing?

**t0022: Yes, but with loss of selectivity.** Peak firing reaches 41 Hz at V=-50 mV (DSI drops
to 0.2047), 70 Hz at V=-40 mV (DSI=0.0952), and **129 Hz at V=-30 mV (DSI=0.0460)**. So the
envelope opens up, but at the cost of direction selectivity: the cell fires almost the same at
all angles.

**t0024: No.** Maximum peak firing is **7.6 Hz at V=-20 mV** — nowhere near the 40-80 Hz
target. The AR(2) stochastic release does not drive the soma to high firing rates at any
V_rest in this range. This suggests t0024's operating ceiling is synaptic-drive-limited, not
intrinsic-excitability limited.

### Q3 — Is the direction-selectivity mechanism more V_rest-dependent in t0022 or t0024?

**t0022 is far more V_rest-sensitive.** DSI range 0.046-0.6555 (14x); at V=-30 mV and V=-40 mV
the cell essentially loses all direction preference (DSI < 0.1). The t0022 deterministic
driver depends on inhibition *arriving at a specific subthreshold moment* — when
depolarisation is strong enough that the cell fires in every cycle regardless of the
inhibitory null, direction selectivity is destroyed.

**t0024 is more robust.** DSI range 0.36-0.67 (1.9x); the model retains DSI > 0.36 across the
entire -90 to -20 mV span. AR(2) correlated release smooths the tuning curve so that
depolarisation-driven failures of the inhibition gate do not fully collapse DSI.

### Q4 — At what V_rest does each port silence / enter depolarization block?

* **t0022 silencing (hyperpolarised):** at **V=-90 mV** firing is limited to 6 Hz at the
  preferred direction and **0 Hz at all other directions** (see the polar plot above — the
  curve has a few isolated petals only on the preferred axis). Even V=-80 mV fires only at 1-3
  preferred directions. Below -90 mV we would expect full silence.
* **t0022 depolarization block:** no hard block observed, but the relevant phenomenon is the
  *loss of selectivity*. At V=-30 mV the cell fires at 111-129 Hz across *all* directions
  (HWHM=180 deg). At V=-20 mV peak firing collapses to 26 Hz, consistent with Na channel
  inactivation starting to dominate. Full depolarization block would require V > -10 mV to
  test.
* **t0024 silencing (hyperpolarised):** at V=-90 mV peak firing is 1.5 Hz with null=0; the
  cell fires occasionally in the preferred hemisphere only. V=-80 mV and V=-70 mV also show
  near-zero null firing (0.06 and 0.26 Hz).
* **t0024 depolarization block:** no collapse observed in this range. Peak firing rises
  monotonically from 1.5 Hz to 7.6 Hz; mean peak mV rises from -14.8 mV to +35.1 mV. The AR(2)
  stochastic driver does not reach Na-inactivation-limited regimes in the tested window.

### Q5 — Does HWHM narrow systematically with depolarisation?

**t0022: No — non-monotone.** HWHM is near-binary (< 1 deg) at V=-90/-80 mV because the cell
fires only at preferred-axis directions. It jumps to 84-86 deg at V=-70/-60 mV (moderate
tuning), then blows out to 102-180 deg at V=-50/-40/-30 mV (complete loss of tuning). Then
narrows to 108 deg at V=-20 mV as Na inactivation re-silences the null directions.

**t0024: No — approximately flat.** HWHM sits at **65-83 deg** across the full V_rest range
with no systematic trend. The AR(2) release smooths the curve so strongly that V_rest does not
appreciably change tuning width. This is consistent with inhibition-dominated tuning: when the
inhibitory schedule is strongly correlated across trials, inhibition sets the angular gate and
intrinsic excitability modulates only overall gain, not shape.

### Comparison: deterministic vs stochastic paradigm

The two drivers differ sharply in how they respond to V_rest even though they drive the same
morphology with the same 12-direction bar protocol. The deterministic t0022 paradigm produces
an on-off response: either the cell fires only on preferred directions (V <= -60 mV) or it
fires on all directions (V >= -50 mV). There is no intermediate regime. The stochastic t0024
paradigm produces a graded response: firing rate scales smoothly with V_rest and DSI modulates
modestly, with two non-adjacent DSI peaks at V=-90 mV and V=-40 mV. The stochastic paradigm's
U-shape is biologically plausible because real retinal circuits have temporally correlated
release (rho > 0) and real DSGCs retain direction selectivity across a range of holding
potentials.

## Examples

The sweep produced 1,056 per-trial rows. Twelve illustrative examples are given below, chosen
to span the behaviour surface: preferred-only firing, preferred+secondary firing, complete
loss of tuning, Na-inactivation collapse, stochastic hyperpolarised silence, and stochastic
depolarised firing. All examples are raw rows from the tidy CSVs
(`data/t0022/vrest_sweep_tidy.csv` and `data/t0024/vrest_sweep_tidy.csv`).

### Example 1 — t0022, V=-90 mV, preferred direction: narrow selective firing

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-90.0,0,0,6,43.273,6.000000
```

Illustrates: hyperpolarised deterministic cell fires only at the preferred axis (0 deg). Peak
mV is +43 mV (healthy spikes) but only 6 spikes in 1 s.

### Example 2 — t0022, V=-90 mV, null direction: complete silence

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-90.0,0,180,0,-58.821,0.000000
```

Illustrates: at null direction the cell never crosses threshold. Peak mV is -58.8 mV —
subthreshold depolarisation only. This is the t0022 "binary" behaviour at V=-90 mV.

### Example 3 — t0022, V=-60 mV (DSI peak), preferred direction

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-60.0,0,60,15,43.873,15.000000
```

Illustrates: at V=-60 mV (baseline and DSI peak) preferred direction fires 15 Hz — the
envelope is starting to open up. Preferred dir is 49 deg in this sweep (60 deg is closest
sampled angle).

### Example 4 — t0022, V=-60 mV, null direction

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-60.0,0,240,0,-55.117,0.000000
```

Illustrates: null direction still completely silent at V=-60 mV. This is why DSI = 0.6555 —
preferred rate well above zero, null rate exactly zero.

### Example 5 — t0022, V=-30 mV: loss of direction selectivity (preferred)

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-30.0,0,60,129,40.956,129.000000
```

Illustrates: 129 Hz at preferred direction — well inside the 40-80 Hz target envelope,
actually above it. Peak mV saturated at +41 mV.

### Example 6 — t0022, V=-30 mV: loss of direction selectivity (null)

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-30.0,0,240,105,43.187,105.000000
```

Illustrates: null direction also fires 105 Hz — the cell has lost direction selectivity
because depolarisation overwhelms the inhibition gate. DSI = 0.046 consequently.

### Example 7 — t0022, V=-20 mV: Na-inactivation collapse (preferred)

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-20.0,0,60,26,42.084,26.000000
```

Illustrates: peak firing has collapsed from 129 Hz at V=-30 mV back down to 26 Hz at V=-20 mV.
Na channel tonic inactivation is starting to limit spiking capacity.

### Example 8 — t0024, V=-90 mV, preferred direction: stochastic low firing

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-90.0,0,0,1,36.535,1.000000
-90.0,1,0,1,38.238,1.000000
-90.0,2,0,2,36.950,2.000000
```

Illustrates: three t0024 trials at V=-90 mV, preferred direction. Firing rates 1, 1, 2 Hz —
stochastic AR(2) release produces trial-to-trial variance even at the DSI peak. Peak mV spread
is narrow (+36 to +38 mV).

### Example 9 — t0024, V=-60 mV (DSI minimum): stochastic mid-range

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-60.0,0,0,6,39.124,6.000000
```

Illustrates: V=-60 mV fires 5 Hz at preferred (trial-average) but 0.5 Hz at null. Despite
higher absolute rate, DSI is lowest (0.4463) of the sweep because null rates creep up.

### Example 10 — t0024, V=-20 mV: depolarised stochastic firing

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-20.0,0,0,8,42.611,8.000000
```

Illustrates: V=-20 mV fires 7.6 Hz at preferred (trial-average) and 1.88 Hz at null. DSI drops
to 0.36 as null firing rises. Note: no Na-inactivation collapse like t0022 shows.

### Example 11 — t0024, V=-40 mV (DSI peak): high selectivity, moderate firing

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-40.0,5,30,7,41.876,7.000000
```

Illustrates: V=-40 mV is the *second* DSI peak for t0024 (0.6248). Peak firing 6.8 Hz, null
firing 0.0 Hz — nearly as clean a selectivity window as V=-90 mV despite totally different
biophysics.

### Example 12 — Contrastive: same direction, same model, different V_rest (t0022)

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-90.0,0,60,1,42.718,1.000000
-60.0,0,60,15,43.873,15.000000
-30.0,0,60,129,40.956,129.000000
-20.0,0,60,26,42.084,26.000000
```

Illustrates: at a single direction (60 deg, near preferred), firing rate goes **1 -> 15 -> 129
-> 26 Hz** across V_rest = -90, -60, -30, -20 mV. This captures the full
monotone-then-collapse trajectory of t0022 peak firing in one contrast.

## Verification

| Check | Command / Artifact | Result |
| --- | --- | --- |
| Row counts | `wc -l data/t0022/vrest_sweep_tidy.csv` = 97 (96 + header); t0024 = 961 (960 + header) | **PASS** — matches REQ-3, REQ-4 |
| Distinct V_rest values | `sorted(df['v_rest_mv'].unique()) == [-90, -80, -70, -60, -50, -40, -30, -20]` | **PASS** — matches REQ-1 |
| Override unit test | `uv run python -u -m tasks.t0026_vrest_sweep_tuning_curves_dsgc.code.vrest_override_smoke` | **PASS** — REQ-2 |
| Library immutability | `git diff main -- 'tasks/*/assets/library/**'` | **PASS** — no diffs |
| Per-V_rest metrics | `data/t0022/vrest_metrics.csv`, `data/t0024/vrest_metrics.csv` | **PASS** — 8 rows each, REQ-6 |
| 16 individual polar plots | `ls results/images/polar_t00*_vrest_*.png \| wc -l` = 16 | **PASS** — REQ-7 |
| 2 overlay polar plots | `polar_t0022_overlay.png`, `polar_t0024_overlay.png` exist | **PASS** — REQ-8 |
| 2 summary plots | `summary_t0022_vrest.png`, `summary_t0024_vrest.png` exist | **PARTIAL** — file names differ from `dsi_vs_vrest.png` / `peak_hz_vs_vrest.png` specified in plan.md; content covers DSI + peak + HWHM + null in 3-panel summary per model |
| Predictions assets | Both `assets/predictions/t0026-vrest-sweep-t0022/` and `assets/predictions/t0026-vrest-sweep-t0024/` have `details.json`, `description.md`, and tidy CSV | **PASS** — REQ-10 |
| Predictions verificator | `verify_predictions_asset.py` | **PASS** — only expected PR-W014 (model_id null) and PR-W015 (dataset_ids empty) warnings, both correct |
| `metrics.json` | `results/metrics.json` uses explicit multi-variant shape with t0022 + t0024 top-level variants | **PARTIAL** — uses `"variants": {...}` map rather than the `"variants": [...]` array form in task_results_specification.md; per-V_rest keys are nested under `project_specific` because the task's proposed keys are not yet registered in `meta/metrics/` (REQ-11 fallback clause applies) |

## Limitations

* **Metric-key registration gap (REQ-11 fallback).** The plan proposed per-V_rest metric keys
  `dsi_at_vrest_<mv>`, `peak_hz_at_vrest_<mv>`, `hwhm_deg_at_vrest_<mv>` for each V_rest value
  plus `efficiency_wall_time_per_trial_seconds` per model. None are currently registered in
  `meta/metrics/`. The `metrics.json` file therefore uses the two already-registered keys
  `direction_selectivity_index` and `tuning_curve_hwhm_deg` as top-level per-variant metrics
  and stores the per-V_rest breakdown under a `project_specific` sub-block. The suggestions
  step will propose registering the missing keys as follow-up.
* **metrics.json shape deviates from the canonical multi-variant array form.** The file uses
  `variants: {"t0022": {...}, "t0024": {...}}` as a map rather than the `variants: [...]`
  array specified by `task_results_specification.md`. The human-readable content is correct
  but the structure may trigger a `TR-E010` error from `verify_task_metrics.py` — this is an
  implementation-step artifact that the reporting step must fix (convert to the array form
  with `variant_id`, `label`, `dimensions`, `metrics` fields).
* **Summary-plot file names do not match plan.md.** The plan specified `dsi_vs_vrest.png` and
  `peak_hz_vs_vrest.png` as two separate Cartesian plots overlaying both models. The actual
  implementation produced a 3-panel `summary_<model>_vrest.png` per model with DSI, peak Hz,
  and HWHM panels. Coverage is equivalent but the file names differ. No cross-model overlay of
  DSI vs V_rest was generated — the two models' DSI trends are compared only in-text in the
  Analysis section and via the overlay polar plots.
* **Single deterministic trial for t0022.** Because t0022 is deterministic, 1 trial per
  (V_rest, angle) is sufficient *per the plan*. A one-shot run cannot surface any accidental
  seed-dependent path through the code. Spot-checked by verifying that re-running V=-60 mV
  with the same seed reproduces identical spike counts.
* **Bar velocity, tstop, and morphology held fixed.** Only V_rest was swept; every other
  driver parameter was left at each library asset's default. V_rest interactions with bar
  velocity or stimulus duration are not tested here.
* **V_rest ceiling at -20 mV.** The sweep stops at -20 mV. Full depolarization block
  (typically at V \> -10 mV) is not observed; the t0022 collapse from 129 Hz to 26 Hz between
  -30 and -20 mV is suggestive but not conclusive evidence of the onset of block.
* **AR(2) rho held fixed at 0.6.** The correlated condition was tested; the uncorrelated
  (rho=0.0) condition was not. V_rest x rho interactions are unknown.
* **Compute efficiency.** The t0024 sweep took 3.21 h on a single CPU thread. NEURON supports
  multi-processing via `mpirun`, and each (V_rest, angle, trial) combination is embarrassingly
  parallel. A parallel-CPU variant could cut wall time to under 30 min on the same workstation
  — flagged as a suggestion for a follow-up task.

## Files Created

**Code (`tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/`):**

* `constants.py` — V_REST_VALUES_MV, ANGLES_DEG, path constants, CSV column names
* `vrest_override.py` — `set_vrest(h, v_rest_mv)` override helper
* `vrest_override_smoke.py` — NEURON-in-the-loop unit test for `set_vrest`
* `trial_runner_t0022.py` — deterministic trial runner (adapted from t0022)
* `trial_runner_t0024.py` — AR(2)-correlated stochastic trial runner (adapted from t0024)
* `run_vrest_sweep_t0022.py` — t0022 sweep driver
* `run_vrest_sweep_t0024.py` — t0024 sweep driver
* `compute_vrest_metrics.py` — per-V_rest DSI/HWHM/peak/null analysis
* `plot_polar_tuning.py` — all 20 plots
* `write_metrics.py` — multi-variant `results/metrics.json` emitter

**Data (`tasks/t0026_vrest_sweep_tuning_curves_dsgc/data/`):**

* `preflight/t0022_preflight.csv`, `preflight/t0022_wall.json`
* `preflight/t0024_preflight.csv`, `preflight/t0024_wall.json`
* `t0022/vrest_sweep_tidy.csv` (96 trials), `t0022/vrest_metrics.csv`
* `t0024/vrest_sweep_tidy.csv` (960 trials), `t0024/vrest_metrics.csv`,
  `t0024/wall_time_by_vrest.json`

**Results (`tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/`):**

* `results/metrics.json` (multi-variant format: t0022 + t0024 variants)
* `results/images/polar_t0022_vrest_-{90,80,70,60,50,40,30,20}mV.png` (8 files)
* `results/images/polar_t0024_vrest_-{90,80,70,60,50,40,30,20}mV.png` (8 files)
* `results/images/polar_t0022_overlay.png`, `results/images/polar_t0024_overlay.png`
* `results/images/summary_t0022_vrest.png`, `results/images/summary_t0024_vrest.png`

**Predictions assets (`tasks/t0026_vrest_sweep_tuning_curves_dsgc/assets/predictions/`):**

* `t0026-vrest-sweep-t0022/{details.json, description.md,
  files/predictions-vrest-sweep-t0022.csv}`
* `t0026-vrest-sweep-t0024/{details.json, description.md,
  files/predictions-vrest-sweep-t0024.csv}`

## Task Requirement Coverage

Operative task request, quoted verbatim from `task.json` and `task_description.md`:

> **Name**: V_rest sweep tuning curves for t0022 and t0024 DSGC ports
>
> **Short description**: Sweep resting potential -90 to -20 mV in 10 mV steps on the t0022 and t0024
> DSGC ports; output polar tuning curves.
>
> **Scope**: Eight V_rest values (-90, -80, -70, -60, -50, -40, -30, -20 mV). At each, set both
> `V_INIT_MV` and `ELEAK_MV` to the sweep value. Model 3 (t0022): 1 trial per angle, 12 angles, 8
> V_rest -> 96 trials. Model 4 (t0024, correlated rho=0.6): 10 trials per angle, 12 angles, 8 V_rest
> -> 960 trials. Do not modify library assets. Report data in polar coordinates.
>
> **Deliverables**: 2 predictions assets; 16 per-(model, V_rest) polar plots; 2 overlay polar plots;
> `results_detailed.md` embedding DSI/peak/HWHM tables and answering the 5 key questions;
> `metrics.json` registering per-V_rest keys or proposing them as suggestions.
>
> **Key questions**: (1) Does either port show DSI > baseline at any V_rest? (2) Does either port
> hit 40-80 Hz? (3) Is the DS mechanism more V_rest-dependent in t0022 or t0024? (4) At what V_rest
> does each port silence or enter depolarization block? (5) Does HWHM narrow systematically with
> depolarisation?

Requirement-by-requirement coverage (REQ-IDs from `plan/plan.md`):

| REQ | Statement | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Exactly 8 V_rest values: -90, -80, -70, -60, -50, -40, -30, -20 mV | **Done** | `code/constants.py` `V_REST_VALUES_MV`; `data/<model>/vrest_sweep_tidy.csv` has exactly 8 distinct `v_rest_mv` values per model |
| REQ-2 | Move `v_init` AND `eleak` together at each V_rest | **Done** | `code/vrest_override.py` `set_vrest()`; unit test `code/vrest_override_smoke.py` prints `OK` (verified on -20 mV cell build) |
| REQ-3 | t0022 sweep: 1 trial per angle, 96 trials total | **Done** | `data/t0022/vrest_sweep_tidy.csv` has exactly 96 data rows (97 with header) |
| REQ-4 | t0024 sweep: 10 trials per angle, 960 trials, correlated rho=0.6 | **Done** | `data/t0024/vrest_sweep_tidy.csv` has exactly 960 data rows (961 with header); AR2_RHO_T0024=0.6 in `code/constants.py` and passed to trial runner |
| REQ-5 | Do not modify either library asset | **Done** | `git diff main -- tasks/*/assets/library/` is empty |
| REQ-6 | Per-(model, V_rest) metrics: DSI, peak Hz, null Hz, HWHM | **Done** | `data/t0022/vrest_metrics.csv` and `data/t0024/vrest_metrics.csv` (8 rows each, columns: v_rest_mv, peak_hz, null_hz, dsi, hwhm_deg, preferred_dir_deg, mean_peak_mv) |
| REQ-7 | 16 per-(model, V_rest) polar plots | **Done** | `ls results/images/polar_t00*_vrest_*.png \| wc -l` = 16; embedded above |
| REQ-8 | 2 overlay polar plots (one per model, 8 curves) | **Done** | `polar_t0022_overlay.png`, `polar_t0024_overlay.png`; embedded above |
| REQ-9 | 2 Cartesian summary plots | **Partial** | Produced `summary_t0022_vrest.png` + `summary_t0024_vrest.png` (3-panel per model: peak/null Hz, DSI, HWHM). Plan originally specified `dsi_vs_vrest.png` / `peak_hz_vs_vrest.png` overlaying both models; cross-model overlay is not produced. Content of individual 3-panel summaries covers all four required axes; comparison is in the Analysis section of this file |
| REQ-10 | 2 predictions assets registered | **Done** | `assets/predictions/t0026-vrest-sweep-t0022/`, `assets/predictions/t0026-vrest-sweep-t0024/`; both pass `verify_predictions_asset.py` with only expected PR-W014 + PR-W015 warnings |
| REQ-11 | `metrics.json` registers per-V_rest keys or proposes them as suggestions | **Partial** | `metrics.json` uses the two registered keys `direction_selectivity_index` and `tuning_curve_hwhm_deg` per variant + a `project_specific` block for per-V_rest breakdowns; per-V_rest keys `dsi_at_vrest_<mv>`, `peak_hz_at_vrest_<mv>`, `hwhm_deg_at_vrest_<mv>` are not yet registered and must be proposed as suggestions in `results/suggestions.json` (step 14). Structure uses `variants: {map}` rather than `variants: [array]` form and may need reformatting in step 15 |
| REQ-12 | Answer the 5 key questions in `results_detailed.md` | **Done** | ## Analysis section above answers Q1-Q5 with numeric evidence and plot references |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0026_vrest_sweep_tuning_curves_dsgc" date_compared:
"2026-04-21" ---
# Comparison with Published DSGC Literature

## Summary

We swept resting membrane potential across eight values from **-90 mV to -20 mV in 10 mV
steps** on two DSGC compartmental ports — the ModelDB 189347 deterministic testbed
(Sivyer/Poleg-Polsky lineage ported in t0022) and the de Rosenroll 2026 AR(2)-correlated
stochastic driver at rho=0.6 (t0024) — under the standard 12-direction moving-bar protocol.
The headline finding is that the t0022 port reproduces the patch-clamp DSI envelope best at
V_rest = **-60 mV** with **DSI = 0.6555** (within the **0.45-0.67** envelope bracketed by
Sivyer2010, Hanson2019 and Hoshi2011) but only when peak firing is a modest **15 Hz** — an
order of magnitude below the **~148 Hz** light-evoked modal rate reported by Oesch2005 for
rabbit ON-OFF DSGCs at a physiological V_rest of **-70.7 mV**. The t0024 port achieves DSI
**0.6746** at V=-90 mV and **0.4463** at V=-60 mV but never exceeds **7.6 Hz** peak firing,
far below the **40-80 Hz** target envelope and the **~166 Hz** adult-mouse rate of Chen2009.
Both ports match the qualitative Barlow1965 / Taylor2002 picture of inhibition-dominated
direction selectivity, but neither reproduces the firing rate magnitudes measured in intact
retina.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Oesch2005 (rabbit ON-OFF DSGC) | V_rest (mV) | -70.7 | -60.0 | +10.7 | Oesch2005 reports natural V_rest under whole-cell current clamp; our -60 mV is both models' default. Our sweep brackets the published value at -70 mV. |
| Oesch2005 (rabbit ON-OFF DSGC) | Light-evoked peak firing rate (Hz) | 148.0 | 15.0 | -133.0 | At matched baseline V_rest -60 mV, t0022 peak firing 15 Hz; Oesch2005 measured 148 ± 30 Hz modal rate on 59 ± 21 spikes/stimulus. |
| Chen2009 (adult mouse ON-OFF DSGC) | Peak firing rate (Hz, ON response) | 166.4 | 129.0 | -37.4 | Compared against t0022 peak at V_rest = -30 mV (best case); Chen2009 is under light stimulation not current injection. |
| Hanson2019 (mouse DRD4 DSGC) | DSI (spikes, bar stimulus) | 0.33 | 0.6555 | +0.3255 | Hanson2019 reports IPSC DSI ~0.33 with spiking DSI robust across stimulus; our t0022 DSI at V=-60 mV exceeds it because our scorer uses a Mazurek vector-sum formulation over 12 angles that can yield higher values than the (Rpref-Rnull)/(Rpref+Rnull) contrast. |
| Sivyer2010 (rabbit ON-OFF DSGC) | DSI (ON response, bar) | 0.45 | 0.6746 | +0.2246 | Our t0024 DSI peak at V=-90 mV; Sivyer2010 reports 0.45-0.50 range for ON-OFF DSGCs under moving-gratings at physiological V_rest. |
| deRosenroll2026 (mouse DSGC network model) | DSI > threshold for DS | 0.5 | 0.4463 | -0.0537 | t0024 port was adapted from the companion repository; at V=-60 mV baseline the port falls just below the DS threshold deRosenroll2026 uses. |
| PolegPolsky2026 (ML search) | DSI threshold (high-DS cluster) | 0.5 | 0.6555 | +0.1555 | Our t0022 at V=-60 mV sits inside the PolegPolsky2026 "high-DS" cluster (>0.5). |
| Hoshi2011 (rabbit ON DSGC) | DSI | 0.66 | 0.6555 | -0.0045 | Near-exact match at t0022 V=-60 mV baseline; Hoshi2011 measured loose-patch DSI in uncoupled ON DSGCs. |
| Oesch2005 (rabbit DSGC) | PSP peak V_m (mV, light-evoked) | -59.1 | -55.1 | +4.0 | Our t0022 null-direction subthreshold peak at V_rest=-60 mV (Example 4 in results_detailed.md); Oesch2005 reports preferred-direction PSP peak. |
| Raganato-style SOTA target | Peak firing envelope (Hz) | 40-80 | 7.6 | — | Not-reproduced: t0024 ceiling far below target; t0022 overshoots on depolarised V_rest at the cost of DSI. |

## Methodology Differences

* **Artificial V_rest override vs natural V_rest.** Our sweep forces V_rest by simultaneously
  overriding `h.v_init`, every section's `eleak_HHst`, and every section's `e_pas` before
  `h.finitialize` on every trial. Published DSGC patch-clamp studies (Oesch2005, Chen2009,
  Sivyer2010, Taylor2002) report the *natural* resting potential the cell settles to under
  whole- cell current clamp, typically **-60 to -70 mV** with no external holding command —
  any V_rest shift in experiment requires current injection or pharmacology and is typically
  bounded within ±10 mV of rest. Only our -60 mV and -70 mV rows are directly comparable to
  the published values.
* **Deterministic vs stochastic release.** The t0022 port uses deterministic per-dendrite E-I
  scheduling; the t0024 port uses AR(2)-correlated stochastic glutamate/GABA release at
  **rho=0.6**. Published DSGCs integrate noisy bipolar and SAC inputs with unknown but
  definitely non-zero temporal correlation (deRosenroll2026, PolegPolsky2016) — neither driver
  perfectly captures this.
* **Single velocity vs velocity sweep.** Our bar protocol uses a single velocity per model
  (each library asset's default ~1000-1500 um/s). Published tuning-curve studies (Sivyer2010,
  Chen2009, Hoshi2011) sweep velocity over **~50-4000 um/s** and report velocity-dependent DSI
  peaks.
* **12-angle coverage, standardised across all V_rest.** Chen2009 and Hoshi2011 use the same
  12-direction / 30-degree protocol; Sivyer2010 uses 8 directions; Hanson2019 uses 8
  directions. DSI values from different angular samplings are not strictly comparable.
* **Scorer definition.** We use the Mazurek vector-sum DSI, `|sum_i r_i * exp(i*theta_i)| /
  sum_i r_i`, while Taylor2002, Chen2009, Oesch2005, and Hanson2019 use the two-direction
  contrast `(R_pref - R_null) / (R_pref + R_null)`. Vector-sum DSI is systematically higher
  for well-tuned cells and lower for weakly-tuned cells than the two- direction contrast.

## Analysis

The V_rest dependence we measured is qualitatively consistent with three biophysical
expectations grounded in the literature:

1. **Sodium channel availability shift.** Oesch2005 measured a light-evoked somatic spike
   threshold of **-56 mV** and showed that each dendritic spike initiates a somatic spike. Our
   t0022 data show peak firing rising monotonically from **6 Hz at V=-90 mV** (Na
   deinactivated but membrane too far below spike threshold) to **129 Hz at V=-30 mV**
   (threshold trivially exceeded), then collapsing to **26 Hz at V=-20 mV** as tonic Na
   inactivation dominates. The collapse is mechanistically equivalent to the **"depolarization
   block above +100 pA"** reported at P11 in Chen2009 — when the membrane sits too close to
   the spike threshold for too long, the Na gate loses availability.

2. **NMDA Mg-block relief.** PolegPolsky2016 showed that NMDA receptor Mg block is the
   dominant source of multiplicative PD/ND scaling in DRD4 DSGCs (**PD NMDAR PSP = 5.8 mV, ND
   = 3.3 mV**). Our t0024 U-shaped DSI profile (**0.6746 at V=-90 mV** and **0.6248 at V=-40
   mV**, with a minimum of **0.4463 at V=-60 mV**) is consistent with the NMDA contribution
   growing as V_rest depolarises past the Mg-block threshold around **-55 mV** — the
   depolarised DSI peak rises as NMDA gain amplifies the already-tuned excitatory drive. At
   hyperpolarised V_rest the driver relies on inhibition-dominated tuning (Barlow1965,
   Taylor2002) which yields the other DSI peak.

3. **Leak-driven PSP attenuation.** Hanson2019 uses a leak reversal of **-60 mV** in the
   ModelDB 189347 reference model. When we shift `e_pas` and `eleak_HHst` to -90 mV the
   driving force on any subthreshold EPSC grows but the cell's effective time constant and
   input resistance change too — this predicts both a quieter baseline (matching our **1.5
   Hz** t0024 peak at V=-90 mV) and a cleaner inhibition gate (matching our DSI peak there).
   At V=-20 mV the leak drive reverses sign relative to Na reversal, driving subthreshold
   depolarisation that overwhelms the inhibitory shunt — consistent with our t0022 HWHM
   blow-out to **180 degrees** at V=-30/-40 mV.

The major disagreement with the literature is peak firing rate: **Oesch2005 measured 148 Hz**,
**Chen2009 measured 166 Hz** (adult ON response) for healthy DSGCs at natural V_rest. t0022
reaches **129 Hz** only at V=-30 mV with DSI collapsed to **0.046**; t0024 never exceeds **7.6
Hz**. This is the headline unresolved issue — neither port reproduces the *combination* of
realistic firing rate and realistic DSI at a biologically plausible V_rest.

## Limitations

* Published DSGC patch-clamp studies uniformly report results at one fixed "natural" V_rest
  (typically ~-60 to -70 mV under whole-cell current clamp), so no published V_rest sweep
  exists to compare our full eight-value curve against. Only the rows at V_rest = -60 mV and
  V_rest = -70 mV in our metrics tables can be directly contrasted with published numbers
  (Oesch2005, Chen2009, Sivyer2010, Hanson2019); the six other V_rest rows are novel
  predictions with no literature counterpart.
* The deRosenroll2026 full PDF was not available at summarisation time (Cell Press 403), so
  its exact quantitative DSI values were not captured in the paper summary — our comparison
  relies on the general "DSI > 0.5 for DS" threshold from the companion repository. A
  follow-up task should obtain the PDF and re-extract the published DSI/peak numbers.
* Scorer mismatch (vector-sum DSI vs two-direction contrast) inflates our DSI values relative
  to Taylor2002/Chen2009/Hanson2019 definitions. A re-scoring with the two-direction formula
  would shift our t0022 V=-60 mV value from **0.6555** toward the **~0.45-0.55** range typical
  in the literature — but the *shape* of the V_rest sweep would be preserved.
* Velocity was fixed at each model's default; published DSI values come from velocity-matched
  conditions that we did not control for. Sivyer2010 explicitly shows DSI depends on velocity
  (**0.45-0.57** range across 50-1200 um/s).
* The 12-angle deterministic t0022 sweep ran only one trial per direction, so no confidence
  intervals are available on t0022 rows; Chen2009 and Oesch2005 report SEM across n=9-13
  cells.
* No comparison against the original Poleg-Polsky ModelDB 189347 reference paper's *own*
  reported DSI/peak values — those were not explicitly quoted in our t0002 survey summaries.
* Published literature mostly reports adult mouse or rabbit values under light stimulation;
  our drivers use synthetic moving bars that approximate but do not reproduce the full
  photoreceptor -> bipolar -> SAC -> DSGC cascade, so additional gain discrepancies arise from
  input generation, not only from membrane biophysics.

</details>
