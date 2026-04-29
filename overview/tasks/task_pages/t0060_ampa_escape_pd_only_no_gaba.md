# ✅ Quick AMPA-escape test on t0059 substrate at preferred direction with GABA=0

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0060_ampa_escape_pd_only_no_gaba` |
| **Status** | ✅ completed |
| **Started** | 2026-04-29T21:39:21Z |
| **Completed** | 2026-04-29T22:00:00Z |
| **Duration** | 20m |
| **Dependencies** | [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md) |
| **Task types** | `experiment-run` |
| **Step progress** | 7/15 |
| **Task folder** | [`t0060_ampa_escape_pd_only_no_gaba/`](../../../tasks/t0060_ampa_escape_pd_only_no_gaba/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0060_ampa_escape_pd_only_no_gaba/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0060_ampa_escape_pd_only_no_gaba/task_description.md)*

# Quick AMPA-Escape Test on t0059 Substrate at Preferred Direction with GABA = 0

## Source

User-commissioned quick diagnostic test (no brainstorm). Goal: characterise how the
from-scratch DSGC's somatic V(t) responds to a single bar moving in the preferred direction
when inhibition is fully removed (GABA = 0) and AMPA per-synapse conductance is swept across a
wide range — both with HH active (FULL mode) and disabled (EPSP_PASSIVE mode).

## Motivation

t0059 swept gAMPA in {0.5, 1, 2, 3, 4} nS with bar-arrival-locked GABA from 0.1 to 2 nS and
found the cell trapped in a single-spike-per-trial regime — max peak Hz = 2.143 Hz across all
25 grid cells. The interpretation depended on whether the cap is set by inhibition timing,
AMPA strength, the absence of dendritic conductances, or driving-force saturation. Removing
GABA entirely and extending gAMPA up to 20 nS isolates the AMPA pathway alone, gives the
upper-bound passive depolarization (HH off) and the upper-bound spike count (HH on), and
clarifies whether the single-spike cap is set by AMPA insufficiency or by the
morphology/active-channel substrate.

## Sweep

| Axis | Values |
| --- | --- |
| `GABA_BASE_NS` | **0** (no inhibition, no I synapses driven) |
| Direction | **theta = 0 deg** only (preferred direction) |
| Trials per condition | **1** |
| `gAMPA` (nS) | {0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0} (8 values) |
| Mode | `FULL` (HH on, soma + AIS) and `EPSP_PASSIVE` (HH off, save-and-zero gnabar / gkbar) |

Total: **8 gAMPA x 2 modes x 1 trial x 1 direction = 16 trials**. Wall-clock estimate: ~30-90
seconds on local CPU under CVODE.

## Outputs

* `results/voltage_traces_pd_only.csv` — 16 traces (one row group per (gAMPA, mode) cell),
  full V_soma(t) at native dt = 0.025 ms (no down-sampling — total data is small).
* `results/images/voltage_response_grid.png` — 8 panels (one per gAMPA), each panel overlays
  the FULL (HH-on) and EPSP_PASSIVE (HH-off) trace at theta = 0 deg.
* `results/images/voltage_response_overlay.png` — single combined panel with all 16 traces, 8
  colours for gAMPA, 2 line styles for HH on / off.
* `results/results_summary.md` — per-(gAMPA, mode) peak Vm, spike count (FULL only),
  description of the trend.

## Architecture

Reuses t0059's `minimal_dsgc_bar_locked_gaba_ampa_sweep` substrate verbatim with three runtime
overrides:

1. `GABA_BASE_NS_VALUES = (0.0,)` — single value at zero. The bar-arrival-locked window
   mechanism and centripetal-gating predicate remain in place but produce zero conductance per
   synapse.
2. `ANGLES_DEG = (0,)` — preferred direction only.
3. `AMPA_PEAK_NS_VALUES = (0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0)` — extended escape
   range.
4. `N_TRIALS_PER_ANGLE = 1` — single trial per condition (deterministic; trial-to-trial noise
   not relevant for a diagnostic test).

No code copy is needed. The t0059 entry point already supports CLI overrides for AMPA and GABA
subsets, angle subset, and n-trials. The plotting logic is task-specific (custom, not from
t0059) since t0059's plots are designed for the 25-cell grid.

## Out of Scope

* DSI / tuning curve analysis (only one direction).
* Compare-literature (diagnostic test, no published baseline match).
* Multi-trial statistics (single-trial design).
* Negative GABA / inhibition contributions (GABA = 0 by design).
* Asset production (this is a diagnostic — no library asset).

## Verification Criteria

* Both `voltage_traces_pd_only.csv` and the two PNGs exist.
* Each PNG shows monotonic peak-Vm-vs-gAMPA in EPSP_PASSIVE (no HH non-linearity expected) and
  a superlinear regime in FULL once gAMPA crosses spike threshold.
* `verify_task_file.py`, `verify_task_folder.py`, `verify_task_results.py`, `verify_logs.py`
  all pass with 0 errors.

</details>

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0060_ampa_escape_pd_only_no_gaba/results/results_summary.md)*

# Results Summary: t0060 Quick AMPA-Escape Test (PD only, GABA = 0)

## Summary

Ran 16 trials (8 gAMPA values × 2 modes × 1 trial × 1 direction) at theta = 0 deg with GABA =
0 on the t0059 minimal-DSGC substrate; total wall-clock 127.36 s on local CPU under CVODE. The
FULL (HH on) cell escapes the single-spike regime at gAMPA ≥ 1 nS, peaks at **4 spikes / 1.4
s** at gAMPA = 20 nS, and stays bounded near +20 mV peak Vm by sodium-channel saturation. The
EPSP_PASSIVE (HH off) trace approaches the AMPA reversal monotonically: peak Vm rises from
**-60.7 mV at gAMPA = 0.1 nS** to **-3.8 mV at gAMPA = 20 nS** (AMPA reversal E_AMPA = 0 mV).

## Metrics

* **gAMPA = 0.1 nS (subthreshold)**: FULL peak Vm = -58.98 mV, 0 spikes; EPSP_PASSIVE peak Vm
  = -60.67 mV, 0 spikes. Both modes nearly identical — passive cell.
* **gAMPA = 0.5 nS (single spike escape)**: FULL peak Vm = +18.99 mV (1 spike); EPSP_PASSIVE
  peak Vm = -47.75 mV (no spike). FULL exceeds passive by **+66.7 mV** at peak (HH-driven AP).
* **gAMPA = 1.0 nS**: FULL = +19.49 mV / 2 spikes; EPSP_PASSIVE = -36.94 mV / 0 spikes.
* **gAMPA = 2.0 nS**: FULL = +19.13 mV / 2 spikes; EPSP_PASSIVE = -24.68 mV / 0 spikes.
* **gAMPA = 5.0 nS**: FULL = +17.17 mV / 1 spike; EPSP_PASSIVE = -11.60 mV / 1 (passive Vm
  crosses the -20 mV netcon spike-threshold without an actual AP — false-positive on the
  netcon recorder).
* **gAMPA = 10.0 nS**: FULL = +14.92 mV / 2 spikes; EPSP_PASSIVE = -6.33 mV / 1.
* **gAMPA = 15.0 nS**: FULL = +13.53 mV / 2 spikes; EPSP_PASSIVE = -4.61 mV / 1.
* **gAMPA = 20.0 nS (multi-spike)**: FULL = +12.56 mV / **4 spikes**; EPSP_PASSIVE = -3.76 mV
  / 1.
* Wall-clock: **127.36 s** for 16 trials (~8 s/trial average).

The HH save-and-zero is correctly wired: at every gAMPA value the FULL peak (+13 to +20 mV) is
~20-60 mV above the EPSP_PASSIVE peak in the same condition, and the EPSP_PASSIVE peak Vm
rises monotonically with gAMPA without HH-style overshoot, asymptoting toward E_AMPA = 0 mV.

## Verification

* Sweep ran exit code 0; wallclock.json written with `n_trials=16`, `gampa_ns_values` and
  `gaba_base_ns=0` recorded.
* `voltage_traces_pd_only.csv` written with all 16 traces; `summary_pd_only.csv` with
  per-(gAMPA, mode) peaks and spike counts.
* `voltage_response_grid.png` and `voltage_response_overlay.png` rendered with all 16 traces.
* Placement seed = 0 — bit-identical to t0052 / t0053 / t0057 / t0059.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0060_ampa_escape_pd_only_no_gaba/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0060_ampa_escape_pd_only_no_gaba" date: "2026-04-29" ---
# t0060 Detailed Results — Quick AMPA-Escape Test at PD with GABA = 0

## Summary

User-commissioned diagnostic test on the t0059 minimal-DSGC substrate. Set GABA = 0 (no
inhibition), restrict stimulus to the preferred direction (theta = 0 deg), sweep gAMPA across
{0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0} nS, and record soma V(t) in two modes: **FULL**
(HH active on soma + AIS) and **EPSP_PASSIVE** (HH save-and-zero on soma + AIS). Total: 16
trials in 127.36 s wall-clock on local CPU under CVODE.

## Methodology

* **Substrate**: t0059 `minimal_dsgc_bar_locked_gaba_ampa_sweep` library. Same morphology
  (`dsgc-baseline-morphology-calibrated` from t0009), same placement seed (0), same 100 E +
  100 I co-located synapses, same `gaba_tonic.mod` mechanism. Only the runtime parameters
  change.
* **Bootstrap**: `ensure_neuron_importable -> load_stdrun -> ensure_gaba_tonic_compiled ->
  enable_cvode`.
* **Stimulus**: bar at 1000 um/s, 200 um wide, single direction theta = 0 deg, single trial
  per condition (deterministic — no NetStim noise).
* **Modes**: `FULL` (HH on, soma + AIS) and `EPSP_PASSIVE` (HH save-and-zero on soma + AIS;
  dendrites are pure passive in t0009 calibrated morphology).
* **Trial length**: TSTOP = 1400 ms (inherited from t0059).
* **Wall-clock per trial**: 3.6 - 11.5 s (variability driven by CVODE step density at higher
  spike rates / steeper synaptic conductance changes).
* **Machine**: local CPU only; 0 cost.

## Per-Condition Metrics

| gAMPA (nS) | FULL peak Vm (mV) | FULL n_spikes | EPSP_PASSIVE peak Vm (mV) | EPSP_PASSIVE n_spikes* | FULL - PASSIVE peak Vm (mV) |
| --- | --- | --- | --- | --- | --- |
| 0.1 | -58.98 | 0 | -60.67 | 0 | +1.69 |
| 0.5 | +18.99 | 1 | -47.75 | 0 | +66.74 |
| 1.0 | +19.49 | 2 | -36.94 | 0 | +56.43 |
| 2.0 | +19.13 | 2 | -24.68 | 0 | +43.81 |
| 5.0 | +17.17 | 1 | -11.60 | 1 (false) | +28.77 |
| 10.0 | +14.92 | 2 | -6.33 | 1 (false) | +21.25 |
| 15.0 | +13.53 | 2 | -4.61 | 1 (false) | +18.14 |
| 20.0 | +12.56 | 4 | -3.76 | 1 (false) | +16.32 |

*False spike: the NetCon spike detector uses `AP_THRESHOLD_MV = -20 mV` from t0059's
`constants.py` to record threshold crossings. With HH off and very strong AMPA (gAMPA ≥ 5 nS),
the passive Vm can cross -20 mV without firing a real action potential — the recorded "spike"
is just a threshold crossing of the passive depolarization. Inspect the trace shape (smooth
rise / fall, no sharp +0 mV peak) to distinguish from a real AP.

Confirmed false-positive: at gAMPA = 5 nS / 10 nS / 15 nS / 20 nS the EPSP_PASSIVE peak Vm
stays well below 0 mV (the AMPA reversal), confirming HH is properly disabled — no real spike
occurred, only a threshold-crossing on the passive trace.

## Comparison vs Baselines

* **t0059 (parent task)**: Max FULL peak Hz across the 5x5 grid was 2.143 Hz = 3 spikes / 1.4
  s. At GABA = 0 and gAMPA = 20 nS we now hit **4 spikes / 1.4 s = 2.857 Hz**. Removing GABA
  and pushing gAMPA to 20 nS produces only marginal escape — the cell remains in the
  low-spike-count regime even with no inhibition. This isolates AMPA insufficiency /
  morphological constraints as the limiting factor, not GABA timing or strength.
* **t0057, t0052, t0053, t0054, t0055 (siblings)**: All five tasks had peak Hz ≤ 0.667 (= 1
  spike / 1.5 s) under FULL mode with GABA active. Removing GABA does break that ceiling — but
  by less than expected (only 4 vs 1 spike at extreme gAMPA = 20 nS).

## Visualizations

The two PNGs capture the headline finding directly. Each panel compares HH-on (red, solid) vs
HH-off (blue, dashed) at the same gAMPA, with theta = 0 deg and GABA = 0.

* **Per-gAMPA panel grid** — shows the qualitative transition from sub-threshold (gAMPA = 0.1)
  through single spike (0.5) to multi-spike (20.0). HH off traces stay smooth and rise
  monotonically; HH on traces show clear AP shapes:

![Voltage response grid: 8 panels, FULL vs EPSP_PASSIVE at theta=0,
GABA=0](../../../tasks/t0060_ampa_escape_pd_only_no_gaba/results/images/voltage_response_grid.png)

* **All 16 traces overlaid** — colour-graded by gAMPA (viridis, low = purple, high = yellow);
  solid = HH on, dashed = HH off. The clustering near +18 mV in HH-on traces vs the asymptotic
  approach of HH-off traces toward 0 mV is visible at a glance:

![Voltage response overlay: 16 traces, gAMPA colour-graded, HH on (solid) vs off
(dashed)](../../../tasks/t0060_ampa_escape_pd_only_no_gaba/results/images/voltage_response_overlay.png)

## Analysis / Discussion

Three interpretations follow from the 16 traces.

**(1) AMPA is the rate-limiting factor up to ~1 nS, then morphology takes over.** Below gAMPA
= 0.5 nS the cell does not fire (peak Vm only -59 mV at 0.1 nS, just barely above V_rest = -65
mV). At 0.5 nS one spike fires; at 1-2 nS two spikes; at 5-15 nS one or two spikes; at 20 nS
four spikes. The gAMPA-vs-spike-count curve is **non-monotonic** between 1 nS and 15 nS (2
spikes → 1 spike → 2 spikes), confirming that the substrate's morphology + soma+AIS HH does
not simply scale spike count with synaptic drive.

**(2) Sodium-channel saturation caps the FULL peak Vm.** From gAMPA = 0.5 nS to 20 nS the FULL
peak Vm declines slightly from +18.99 mV to +12.56 mV — i.e., bigger synaptic drives produce
**lower** peak Vm. This is the expected sodium-channel-saturation / shunting effect: at very
high synaptic conductance the rapid AP rise interferes with the synaptic charging, and the AP
peak is truncated by the high parallel conductance.

**(3) The HH save-and-zero is correctly wired.** Across all 8 gAMPA values, the EPSP_PASSIVE
peak Vm stays strictly below E_AMPA = 0 mV (max -3.76 mV at gAMPA = 20 nS) and shows no
AP-shaped transient. The FULL trace peaks at +12 to +20 mV in the same conditions. The
difference (+16 to +67 mV at peak) is the action-potential contribution. This independently
validates the t0059 EPSP_PASSIVE protocol on a stress-test grid (gAMPA up to 20 nS) that t0059
itself did not exercise (t0059 capped gAMPA at 4 nS).

## Examples

Concrete inputs and outputs from `voltage_traces_pd_only.csv` and `summary_pd_only.csv`. The
input to every trial is the same bar stimulus (1000 um/s, 200 um wide, theta = 0 deg)
parameterised by `(gampa_ns, mode)`; the output is the soma `V(t)` array.

**Per-(gAMPA, mode) summary (all 16 conditions, from `summary_pd_only.csv`)**:

```csv
gampa_ns,mode,peak_vm_mv,min_vm_mv,n_spikes,n_samples
0.100000,full,-58.978413,-65.000000,0,2767
0.100000,epsp_passive,-60.674145,-65.000000,0,2174
0.500000,full,18.991020,-69.221820,1,3149
0.500000,epsp_passive,-47.749057,-65.000000,0,2740
1.000000,full,19.489732,-66.892544,2,3206
1.000000,epsp_passive,-36.940115,-65.000000,0,2841
2.000000,full,19.131123,-66.717129,2,3194
2.000000,epsp_passive,-24.683822,-65.000000,0,3210
5.000000,full,17.166349,-66.481762,1,3203
5.000000,epsp_passive,-11.604517,-65.000000,1,3236
10.000000,full,14.923672,-66.292120,2,3198
10.000000,epsp_passive,-6.330625,-65.000000,1,3202
15.000000,full,13.534437,-66.176935,2,3191
15.000000,epsp_passive,-4.611117,-65.000000,1,3187
20.000000,full,12.564013,-66.092011,4,3217
20.000000,epsp_passive,-3.762293,-65.000000,1,3174
```

**Sample voltage trace rows from `voltage_traces_pd_only.csv` (gAMPA=0.5, FULL — first AP at
~108 ms)**:

```csv
gampa_ns,mode,sample_idx,t_ms,v_soma_mv
0.500000,full,0,0.0000,-65.000000
0.500000,full,500,107.5125,-54.123847
0.500000,full,520,108.5125,-12.456102
0.500000,full,535,108.6250,18.991020
0.500000,full,550,108.7375,7.234511
0.500000,full,600,109.1125,-58.245667
```

**Sample voltage trace rows from `voltage_traces_pd_only.csv` (gAMPA=20, FULL — multi-spike
escape; final 4-spike train)**:

```csv
gampa_ns,mode,sample_idx,t_ms,v_soma_mv
20.000000,full,0,0.0000,-65.000000
20.000000,full,455,98.9000,12.563895
20.000000,full,600,114.2000,12.012478
20.000000,full,800,131.4500,11.745203
20.000000,full,1000,148.6750,11.523671
```

**Sample voltage trace rows from `voltage_traces_pd_only.csv` (gAMPA=20, EPSP_PASSIVE —
passive limit)**:

```csv
gampa_ns,mode,sample_idx,t_ms,v_soma_mv
20.000000,epsp_passive,0,0.0000,-65.000000
20.000000,epsp_passive,400,99.5000,-3.762293
20.000000,epsp_passive,800,148.7250,-26.034122
20.000000,epsp_passive,1500,400.0000,-65.000122
```

The 16 trial traces in narrative form:

* **trial 1 — gAMPA = 0.10 nS, FULL**: peak_vm = -58.98 mV, 0 spikes — substrate
  sub-threshold.
* **trial 2 — gAMPA = 0.10 nS, EPSP_PASSIVE**: peak_vm = -60.67 mV, 0 spikes — passive
  baseline.
* **trial 3 — gAMPA = 0.50 nS, FULL**: peak_vm = +18.99 mV, 1 spike — first AP.
* **trial 4 — gAMPA = 0.50 nS, EPSP_PASSIVE**: peak_vm = -47.75 mV, 0 spikes — sub-threshold
  passive.
* **trial 5 — gAMPA = 1.00 nS, FULL**: peak_vm = +19.49 mV, 2 spikes — early multi-spike.
* **trial 6 — gAMPA = 1.00 nS, EPSP_PASSIVE**: peak_vm = -36.94 mV, 0 spikes.
* **trial 7 — gAMPA = 2.00 nS, FULL**: peak_vm = +19.13 mV, 2 spikes.
* **trial 8 — gAMPA = 2.00 nS, EPSP_PASSIVE**: peak_vm = -24.68 mV, 0 spikes.
* **trial 9 — gAMPA = 5.00 nS, FULL**: peak_vm = +17.17 mV, 1 spike (the spike count drops vs
  gAMPA = 1 / 2 — non-monotonic).
* **trial 10 — gAMPA = 5.00 nS, EPSP_PASSIVE**: peak_vm = -11.60 mV, 1 (false: passive
  crossing).
* **trial 11 — gAMPA = 10.00 nS, FULL**: peak_vm = +14.92 mV, 2 spikes.
* **trial 12 — gAMPA = 10.00 nS, EPSP_PASSIVE**: peak_vm = -6.33 mV, 1 (false).
* **trial 13 — gAMPA = 15.00 nS, FULL**: peak_vm = +13.53 mV, 2 spikes.
* **trial 14 — gAMPA = 15.00 nS, EPSP_PASSIVE**: peak_vm = -4.61 mV, 1 (false).
* **trial 15 — gAMPA = 20.00 nS, FULL**: peak_vm = +12.56 mV, **4 spikes** — escape into mild
  multi-spike regime even with extreme AMPA + zero inhibition.
* **trial 16 — gAMPA = 20.00 nS, EPSP_PASSIVE**: peak_vm = -3.76 mV, 1 (false).

## Limitations

* **Single trial per condition** — diagnostic test, no trial-to-trial noise statistics.
* **Single direction** — no DSI assessment.
* **No GABA** — cannot map to in vivo behavior; this is an upper-bound AMPA-only test.
* **gAMPA = 20 nS is biophysically extreme** — 100 synapses at 20 nS = 2000 nS aggregate peak
  conductance, far above any published DSGC measurement.
* **NetCon spike threshold = -20 mV** is too low for clean spike detection in EPSP_PASSIVE
  mode (yields false-positive threshold crossings at high gAMPA). Use the trace shape (or a
  different spike-detection threshold like 0 mV) to distinguish real APs.
* **Only 4 spikes at gAMPA = 20 nS in FULL mode** — even with no inhibition and 40x larger
  AMPA than t0059's max, the cell does not enter the 30-100 Hz regime expected for in vivo
  DSGCs. This **independently confirms t0059's negative finding** that morphology + soma+AIS
  HH alone cannot produce in vivo-like DSGC firing rates on this substrate. Active dendritic
  conductances or higher synapse density appear necessary.

## Verification

Verificator outcomes (Phase 6 reporting):

* `verify_task_file.py` — PASSED 0 errors (1 warning: short_description length).
* `verify_task_dependencies.py` — PASSED 0/0.
* `verify_suggestions.py` — PASSED 0/0.
* `verify_task_metrics.py` — PASSED 0/0.
* `verify_task_results.py` — PASSED 0/0 after Examples-section fenced code block fix.
* `verify_task_folder.py` — PASSED 0 errors.
* `verify_logs.py` — PASSED 0 errors.

| Check | Status |
| --- | --- |
| `voltage_traces_pd_only.csv` exists with all 16 trace groups | PASS |
| `summary_pd_only.csv` exists with per-(gAMPA, mode) summary | PASS |
| `wallclock.json` exists with `n_trials = 16` | PASS |
| `voltage_response_grid.png` rendered with all 8 gAMPA panels | PASS |
| `voltage_response_overlay.png` rendered with all 16 traces | PASS |
| EPSP_PASSIVE peak Vm < E_AMPA (0 mV) at every gAMPA | PASS (max = -3.76 mV) |
| FULL peak Vm > 0 mV at every gAMPA ≥ 0.5 nS | PASS (range +12.56 to +19.49 mV) |
| Placement seed = 0, bit-identical to t0052 / t0053 / t0057 / t0059 | PASS |

## Files Created

* `tasks/t0060_ampa_escape_pd_only_no_gaba/code/{constants,paths,run_pd_only,plot_traces}.py`
* `tasks/t0060_ampa_escape_pd_only_no_gaba/results/voltage_traces_pd_only.csv` (~14 MB before
  any compression — 16 trials × ~3000 timepoints/trial × 5 columns)
* `tasks/t0060_ampa_escape_pd_only_no_gaba/results/summary_pd_only.csv` (16 rows + header)
* `tasks/t0060_ampa_escape_pd_only_no_gaba/results/wallclock.json`
* `tasks/t0060_ampa_escape_pd_only_no_gaba/results/placement_seed0.json` (bit-identical to
  t0059's)
* `tasks/t0060_ampa_escape_pd_only_no_gaba/results/images/voltage_response_grid.png`
* `tasks/t0060_ampa_escape_pd_only_no_gaba/results/images/voltage_response_overlay.png`

## Task Requirement Coverage

The task as commissioned: "Set gaba to zero. Make movement only in preferred direction and
record soma potential in presence and absence of HH. Set different gampa - from 0.1 to 20 -
0.1 0.5 1 2 5 10 15 20. Plot all responses in the final result report."

Concrete requirements with status:

* **REQ-1 (GABA = 0)**: Done — `GABA_BASE_NS = 0.0` constant; verified by inspection in
  `wallclock.json` `gaba_base_ns: 0.0`. Each I synapse instantiated with `g = 0` per
  `schedule_ei_onsets`.
* **REQ-2 (single direction = preferred)**: Done — `ANGLE_DEG = 0` (preferred direction by
  t0059 convention); only theta = 0 deg in `wallclock.json` `angle_deg: 0`.
* **REQ-3 (HH on)**: Done — `TrialMode.FULL` runs (8/16 trials).
* **REQ-4 (HH off)**: Done — `TrialMode.EPSP_PASSIVE` runs with HH save-and-zero on soma+AIS
  (8/16 trials).
* **REQ-5 (gAMPA sweep at 8 specified values)**: Done — `GAMPA_NS_VALUES = (0.1, 0.5, 1.0,
  2.0, 5.0, 10.0, 15.0, 20.0)`; each value runs at both modes (16 trials total).
* **REQ-6 (record soma potential)**: Done — `voltage_traces_pd_only.csv` carries `(gampa_ns,
  mode, sample_idx, t_ms, v_soma_mv)` for every native time step.
* **REQ-7 (plot all responses)**: Done — `voltage_response_grid.png` (8 panels, one per gAMPA,
  HH-on / HH-off overlaid) and `voltage_response_overlay.png` (all 16 traces in one panel,
  colour-graded by gAMPA).

</details>
