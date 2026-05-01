# ⏹ Channel tuning-width sweep on Bed A with BK/SK/Kv7 vendoring

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0074_channel_tuning_width_bed_a` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md) |
| **Source suggestion** | `S-0068-01` |
| **Task types** | `build-model`, `experiment-run` |
| **Expected assets** | 1 library |
| **Task folder** | [`t0074_channel_tuning_width_bed_a/`](../../../tasks/t0074_channel_tuning_width_bed_a/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0074_channel_tuning_width_bed_a/task_description.md)*

# Channel Tuning-Width Sweep on Bed A with BK / SK / Kv7 Vendoring

## Motivation

The t0067 soma-channel-addition sweep on Bed A (deposited Poleg-Polsky DSGC, library
`modeldb_189347_dsgc` from t0008) measured DSI as a point estimate from PD vs ND only — a
2-angle protocol. That left the more biologically interesting question unanswered: do the
tested channels also reshape the *width* of the angle-to-AP-rate tuning curve, and if so, do
they sharpen or broaden it? t0067 reported NaP_high inverts DSI (sign flip), Nav1.6_high
erodes DSI from 0.80 to 0.23, and {NaR, Kv3, Kv4} are nearly inert at the chosen densities;
t0068 then falsified the Nav1.6 + Kv3 co-expression rescue. Three biologically natural rescue
candidates remain untested because their MOD mechanisms are not yet vendored in the project:
BK (KCa1.1 / KCNMA1), SK (KCa2 / KCNN), and Kv7 (KCNQ2 + KCNQ3, the M-current). All three are
calcium-activated or slow-activating and could in principle differentially suppress the
high-firing-rate PD direction and rescue DSI without flipping it. Adding them to the channel
sweep and measuring tuning width across all eight channels at three densities each closes both
gaps in one task.

This task addresses RQ1 (somatic VGC combinations) and provides a tuning-width baseline that
any future RQ4 active-dendrite test will compare against. Source suggestions covered:
S-0068-01 (BK / SK with Nav1.6), S-0068-02 (Kv7 with Nav1.6), S-0068-05 (Kv3 alone
validation).

## Scope

* Substrate: Bed A only (deposited Poleg-Polsky DSGC, t0008 library `modeldb_189347_dsgc`).
* Encoding: 12-angle bar-rotation protocol (the model's native protocol per t0046
  reproduction). Bar-arrival times sweep through 12 angles in 30-degree steps.
* Channel set: 8 channels — 5 already vendored {Nav1.6, NaP, NaR, Kv3, Kv4} plus 3 newly
  vendored {BK, SK, Kv7}. Each channel inserted on the soma at low / medium / high density (3
  densities each, matching the t0067 grid). Plus a baseline condition with no extra channels.
* **Conditions**: 1 baseline + 8 channels x 3 densities = **25 conditions**.
* **Trials**: 25 conditions x 12 angles x 5 seeds in FULL mode = 1500 trials. Plus 25 x 12
  angles x 1 seed x 2 passive modes (EPSP_PASSIVE / IPSP_PASSIVE) = 600 diagnostic trials.
  **Total: 2100 trials**, ~2.2 h wall-clock on local CPU under CVODE at the t0067 measured
  rate of ~3.75 s / trial.

## Approach

### Stage 1 — vendor 3 new MOD files plus calcium-pool mechanism

* Vendor a BK (KCa1.1) MOD file, sourced from a standard published model (e.g., Migliore CA1,
  Hines & Carnevale Purkinje). Validate kinetics against expected V- and Ca-dependence.
* Vendor an SK (KCa2 / SK2) MOD file from the same kind of source.
* Vendor a Kv7 / M-current MOD file (KCNQ2 + KCNQ3 mixture or composite Kv7) from a standard
  published model.
* Vendor a calcium-pool mechanism (single-shell `cad`-style decay model, mirrors Bed B's
  existing `cad`) to provide [Ca]_i for BK and SK.
* Un-zero CaL and CaT in Bed A's `init_active` so that the calcium pool has a current source.
  This is the only change to the existing Bed A model and must pass a regression gate (see
  Stage 2).

### Stage 2 — regression gate

* Run the t0067 baseline (no extra channels, no BK / SK / Kv7) under the new code path with
  CaL + CaT un-zeroed and the calcium-pool mechanism live but at zero density (BK = 0, SK = 0,
  Kv7 = 0).
* Pass criterion: baseline DSI matches t0067's reported DSI = 0.797 within 1e-3 (allowing
  sampling noise across the 5-seed mean). Failure means the un-zeroing introduced unintended
  dynamics; fix before proceeding to Stage 3.

### Stage 3 — 12-angle tuning-curve sweep

* For each of 25 conditions (1 baseline + 5 existing channels x 3 densities + 3 new channels x
  3 densities) run 12 angles x 5 seeds in FULL mode. Save:
  * Per-trial soma spike times.
  * Per-trial peak Vm and baseline Vm.
  * Per-condition tuning curve (mean +/- SD spike count per angle).
* Same channel insertion code as t0067 with three new branches for BK, SK, Kv7. Holds all
  other parameters at the t0067 baseline.

### Stage 4 — passive diagnostics (EPSP_PASSIVE / IPSP_PASSIVE)

* For each of 25 conditions run 12 angles x 1 seed x 2 passive modes = 600 trials.
* Save per-trial peak Vm in the EPSP_PASSIVE and IPSP_PASSIVE traces. These should be flat at
  -60 mV in IPSP_PASSIVE for all conditions (cross-checks with t0065's shunting-design
  finding) and direction-invariant in EPSP_PASSIVE under Bed A's gabaMOD = 0 zeroing.

### Stage 5 — width metrics and visualisation

* Per condition, compute:
  * **HWHM** (half-width at half-max) in degrees, by linear interpolation around the half-max
    points of the 12-angle tuning curve.
  * **Vector-sum DSI** = `|sum_i rate(theta_i) * exp(i * theta_i)| / sum_i rate(theta_i)` —
    circular concentration metric.
  * **Peak rate (Hz)** at the angle with maximum mean rate.
  * **Rate at PD** and **rate at PD + 180 deg** (ND).
  * **RMSE vs t0004 cosine target** — the canonical project tuning-curve loss, computed using
    the t0012 library.
* For any condition where the tuning curve has no clear peak (mean rate < 1 Hz at every
  angle), report HWHM as `null` rather than fabricating a value.
* Produce a per-channel sensitivity plot (HWHM, vector-sum DSI, peak rate vs density) using
  the t0011 visualisation library.

## Expected Outputs

* **Library asset**: a vendored channel pack containing the BK, SK, Kv7 MODs plus the
  calcium-pool mechanism, registered as a project library. This becomes a dependency for t0075
  and any future task that needs these channels.
* **Per-condition tuning curves** (25 CSVs, one per condition) and a combined
  `tuning_curves.csv` with all 25 x 12 = 300 (condition, angle) rows.
* **Width metrics table** (`results/metrics_summary.csv`): 25 rows x 6 columns (HWHM,
  vector-sum DSI, peak rate, PD rate, ND rate, RMSE vs cosine target).
* **Per-channel sensitivity plots** (8 PNGs in `results/images/`): HWHM, vector-sum DSI, peak
  rate vs density per channel.
* **Cross-channel comparison plot** (`results/images/all_channels_dsi_vs_density.png`):
  vector-sum DSI vs density for all 8 channels overlaid.
* `results/metrics.json` with the registered project metrics applied per condition.

## Pass Criteria

* Stage 2 regression gate passes (baseline DSI within 1e-3 of t0067 = 0.797).
* All 2100 trials complete with no instability flags.
* Width metrics table is fully populated (HWHM may be `null` for low-rate conditions;
  vector-sum DSI and peak rate must be defined for all 25 conditions).
* For each channel, at least one density produces a measurable change in either HWHM or
  vector-sum DSI (delta > 5 deg HWHM or delta > 0.05 vector-sum DSI relative to baseline).
  Channels that produce no measurable change at any density are reported as inert in the
  conclusion section.

## Compute Estimate

* ~2.2 h wall-clock on local CPU under CVODE for the 2100 trials.
* ~3-4 h coding time for the 3 channel MOD vendoring + calcium-pool mechanism + Stage 2
  regression gate.
* Local-CPU only. No remote machine. No paid API.

## Dependencies

* `t0008_port_modeldb_189347` — Bed A library `modeldb_189347_dsgc`.
* `t0011_response_visualization_library` — tuning-curve visualisation.
* `t0012_tuning_curve_scoring_loss_library` — RMSE vs cosine target.
* `t0067_t0065_soma_channel_addition_sweep` — channel-insertion code is forkable; baseline DSI
  = 0.797 reference for the regression gate.

## Risks and Fallbacks

* **Calcium-pool kinetics drift**: the un-zeroing of CaL / CaT in Bed A's `init_active` is the
  most disruptive change. If the regression gate (Stage 2) fails, fall back to a closed-form
  external calcium-pool mechanism that does not depend on CaL / CaT (e.g., feed [Ca]_i
  directly from a precomputed time series). This preserves BK / SK kinetics while leaving Bed
  A's existing HHst dynamics untouched.
* **BK / SK MOD source discrepancy**: if the chosen source MOD has different kinetics from the
  canonical RGC literature, validate against published whole-cell recordings (e.g., Pfeiffer &
  Friedrich 2012 mouse RGC BK; Wang et al. 2014 RGC SK). Document the source paper for each
  MOD in the library asset's `details.json`.
* **Kv7 expression density unclear**: Kv7 in DSGC AIS is documented but somatic Kv7 in DSGC is
  less studied. If the t0067 "low / medium / high" density grid produces only inert results
  across the Kv7 row, log the negative result and recommend an AIS-localised follow-up
  (deferring to t0075).

</details>
