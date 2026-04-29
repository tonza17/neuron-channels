# ✅ Quick NMDAR-escape test on t0059 substrate at preferred direction with GABA=0

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0061_nmda_escape_pd_only_no_gaba` |
| **Status** | ✅ completed |
| **Started** | 2026-04-29T22:15:49Z |
| **Completed** | 2026-04-29T22:32:00Z |
| **Duration** | 16m |
| **Dependencies** | [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0060_ampa_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md) |
| **Task types** | `experiment-run` |
| **Step progress** | 7/15 |
| **Task folder** | [`t0061_nmda_escape_pd_only_no_gaba/`](../../../tasks/t0061_nmda_escape_pd_only_no_gaba/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0061_nmda_escape_pd_only_no_gaba/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0061_nmda_escape_pd_only_no_gaba/task_description.md)*

# Quick NMDAR-Escape Test on t0059 Substrate at Preferred Direction with GABA = 0

## Source

User-commissioned diagnostic, parallel to t0060 but with NMDAR (Mg-block) replacing AMPA.
Goal: characterise how the from-scratch DSGC's somatic V(t) responds to a single bar moving in
the preferred direction when inhibition is fully removed (GABA = 0) and **NMDA**-only
excitation is swept across a wide range — both with HH active (FULL mode) and disabled
(EPSP_PASSIVE mode).

## Mechanism Choice

This task uses the biologically correct **Mg-block NMDA** (Jahr-Stevens) mechanism inherited
from t0055's `NMDA_MgBlock.mod`. The Mg-block formula and parameter values are taken verbatim
from ModelDB 189347 (Poleg-Polsky 2016): `n = 0.25 /mM`, `gamma = 0.08 /mV`, `tau1 = 5 ms`,
`tau2 = 80 ms`, `e = 0 mV`, `Voff = 0` (voltage-dependent). Without AMPA priming, low-gNMDA
trials are expected to produce minimal response (Mg block is engaged at V_rest = -65 mV); the
sweep tests whether sufficiently high gNMDA can self-prime via leaky Mg-block conductance.

## Sweep

| Axis | Values |
| --- | --- |
| `GABA_BASE_NS` | **0** (no inhibition) |
| AMPA | **0** (no AMPA — NMDA-only excitation) |
| Direction | **theta = 0 deg** only (preferred direction) |
| Trials per condition | **1** |
| `gNMDA` (nS) | {0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0} (8 values) |
| Mode | `FULL` (HH on, soma + AIS) and `EPSP_PASSIVE` (HH off, save-and-zero gnabar / gkbar) |

Total: **8 gNMDA x 2 modes x 1 trial x 1 direction = 16 trials**. Wall-clock estimate: ~1-3
minutes on local CPU under CVODE.

## Outputs

* `results/voltage_traces_pd_only.csv` — 16 traces (one row group per (gNMDA, mode) cell),
  full V_soma(t).
* `results/summary_pd_only.csv` — per-(gNMDA, mode) peak / min Vm and spike count.
* `results/images/voltage_response_grid.png` — 8 panels (one per gNMDA), each panel overlays
  FULL (HH-on) and EPSP_PASSIVE (HH-off) trace at theta = 0 deg.
* `results/images/voltage_response_overlay.png` — single combined panel with all 16 traces.
* `results/results_summary.md` and `results_detailed.md`.

## Architecture

Reuses t0059's morphology, placement (seed 0), neuron bootstrap, and trial-mode dispatcher.
The synapse layer is replaced wholesale: each E location gets ONE `NMDA_MgBlock` POINT_PROCESS
plus a NetStim + NetCon (no AMPA Exp2Syn, no GABA tonic). Spatial gating is preserved but with
`GABA = 0` and no AMPA, only the NMDA mechanism is active.

The `NMDA_MgBlock.mod` source is copied verbatim from t0055 (provenance: ModelDB 189347
`bipolarNMDA.mod`) and recompiled in t0061's `code/mod/` for this task's NEURON kernel.

## Out of Scope

* AMPA + NMDA combination (that's t0054 / S-0057-06 territory).
* Voltage-independent NMDA (`Voff = 1`) — fixed `Voff = 0` (Mg-block on).
* Multi-trial statistics, DSI, compare-literature, suggestions.
* Asset production (no library produced).

## Verification Criteria

* Both `voltage_traces_pd_only.csv` and the two PNGs exist.
* `verify_task_file.py`, `verify_task_folder.py`, `verify_task_results.py`, `verify_logs.py`
  all pass with 0 errors.

</details>

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0061_nmda_escape_pd_only_no_gaba/results/results_summary.md)*

# Results Summary: t0061 NMDA-Only PD Diagnostic

## Summary

Ran 16 trials (8 gNMDA values × 2 modes × 1 trial) at theta = 0 deg with GABA = 0, AMPA = 0,
NMDA-only excitation (Mg-block, Jahr-Stevens). Wall-clock 118.14 s on local CPU under CVODE.
Headline: **regenerative Mg-block escape between gNMDA = 1.0 nS** (peak Vm = -58.89 mV, 0
spikes) **and gNMDA = 2.0 nS** (peak Vm = +11.29 mV, **3 spikes**). The NMDA plateau widens to
~200-400 ms at gNMDA >= 5 nS, far longer than the AMPA EPSP in t0060 (~10 ms).

## Metrics

* **gNMDA = 0.1 nS**: FULL peak Vm = -64.22 mV, 0 spikes; EPSP_PASSIVE peak Vm = -64.47 mV, 0
  spikes. Mg block fully engaged.
* **gNMDA = 0.5 nS**: FULL peak = -62.61 mV, 0 spikes. Tiny depolarization.
* **gNMDA = 1.0 nS**: FULL peak = -58.89 mV, 0 spikes. Below the regenerative threshold.
* **gNMDA = 2.0 nS (Mg-block escape)**: FULL peak = +11.29 mV, **3 spikes**; EPSP_PASSIVE peak
  = -52.58 mV, 0 spikes. Sudden transition: depolarization unblocks Mg, NMDA opens, drives
  more depolarization, fires action potentials.
* **gNMDA = 5.0 nS**: FULL = +13.12 mV / 3 spikes; EPSP_PASSIVE = -8.59 mV / 1 (false
  threshold crossing).
* **gNMDA = 10.0 nS**: FULL = +13.21 mV / 3 spikes; EPSP_PASSIVE = -4.67 mV / 1 (false).
* **gNMDA = 15.0 nS**: FULL = +13.15 mV / 2 spikes; EPSP_PASSIVE = -3.37 mV / 1 (false).
* **gNMDA = 20.0 nS**: FULL = +13.21 mV / 1 spike (sodium-channel saturation truncates the
  spike train); EPSP_PASSIVE = -2.70 mV / 1 (false).
* Wall-clock: 118.14 s for 16 trials.

## Verification

* `wallclock.json` written; `voltage_traces_pd_only.csv` and `summary_pd_only.csv` complete.
* `voltage_response_grid.png` (8 panels) and `voltage_response_overlay.png` (16 traces)
  rendered.
* Placement seed = 0 (bit-identical to t0052/t0053/t0057/t0059/t0060).
* HH save-and-zero validated: EPSP_PASSIVE peak Vm asymptotes to E_AMPA = 0 mV (max -2.70 mV
  at gNMDA = 20 nS) without HH-driven overshoot.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0061_nmda_escape_pd_only_no_gaba/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0061_nmda_escape_pd_only_no_gaba" date: "2026-04-29" ---
# t0061 Detailed Results: NMDA-Only PD Diagnostic

## Summary

NMDA analog of t0060. GABA = 0, AMPA = 0 (NMDA-only excitation via Mg-block Jahr-Stevens),
theta = 0 deg, sweep gNMDA across {0.1, 0.5, 1, 2, 5, 10, 15, 20} nS at FULL (HH on) and
EPSP_PASSIVE (HH off). 16 trials in 118.14 s. Cell stays near rest below gNMDA = 1.0 nS, then
exhibits regenerative Mg-block escape at gNMDA = 2.0 nS, firing 3 spikes with a wide NMDA
plateau.

## Methodology

* **Substrate**: same morphology, placement (seed 0), HH on soma + AIS, passive dendrites as
  t0059 / t0060.
* **NMDA mechanism**: t0055's `NMDA_MgBlock.mod` (Jahr-Stevens, voltage-dependent Mg block
  with `n = 0.25 /mM`, `gamma = 0.08 /mV`, `tau1 = 5 ms`, `tau2 = 80 ms`, `e = 0 mV`, `Voff =
  0`).
* **Synapses**: 100 NMDA-only (no AMPA, no GABA). Each location gets one `NMDA_MgBlock`
  POINT_PROCESS plus a NetStim + NetCon. Bar-arrival-locked onsets per t0059 geometry.
* **Modes**: FULL (HH active), EPSP_PASSIVE (save-and-zero `gnabar` / `gkbar` on soma + AIS).
* **Stimulus**: bar 1000 um/s, 200 um wide, theta = 0 deg, 1400 ms trial, single trial per
  condition.
* **Bootstrap**: `ensure_neuron_importable -> load_stdrun -> ensure_nmda_compiled (t0061
  build) -> enable_cvode`.
* **Wall-clock**: 118.14 s for 16 trials, 2.0-19.5 s/trial.

## Per-Condition Metrics

| gNMDA (nS) | FULL peak Vm (mV) | FULL n_spikes | EPSP_PASSIVE peak Vm (mV) | EPSP_PASSIVE n_spikes* |
| --- | --- | --- | --- | --- |
| 0.1 | -64.22 | 0 | -64.47 | 0 |
| 0.5 | -62.61 | 0 | -63.10 | 0 |
| 1.0 | -58.89 | 0 | -60.97 | 0 |
| 2.0 | +11.29 | **3** | -52.58 | 0 |
| 5.0 | +13.12 | 3 | -8.59 | 1 (false) |
| 10.0 | +13.21 | 3 | -4.67 | 1 (false) |
| 15.0 | +13.15 | 2 | -3.37 | 1 (false) |
| 20.0 | +13.21 | 1 | -2.70 | 1 (false) |

*False spike: the netcon spike detector at -20 mV records threshold crossings on the smooth
EPSP_PASSIVE trace at gNMDA >= 5 nS. Trace shape and peak Vm < 0 mV confirm no real APs.

## Comparison vs t0060 (AMPA-only analog)

| Property | t0060 (AMPA-only) | t0061 (NMDA-only) |
| --- | --- | --- |
| Threshold for first spike | gAMPA = 0.5 nS (1 spike) | gNMDA = 2.0 nS (3 spikes) |
| Sub-threshold response shape | Fast (~10 ms) EPSP | Slow tonic depolarization, slight |
| Multi-spike regime | gAMPA = 20 nS (4 spikes) | gNMDA = 2-10 nS (3 spikes), drops at higher gNMDA |
| EPSP plateau width (HH off) | ~10-20 ms transient | **200-400 ms** sustained |
| Max FULL peak Vm | +19.49 mV | +13.21 mV |
| EPSP_PASSIVE peak Vm range | -60.67 to -3.76 mV | -64.47 to -2.70 mV |
| Threshold sharpness | Smooth (gradient over 0.1-0.5 nS) | **Sharp Mg-block escape (1->2 nS)** |

The NMDA mechanism produces a fundamentally different response shape from AMPA: slow tonic
plateau driven by tau_decay = 80 ms vs AMPA's tau_decay = 2.5 ms. The Mg block creates a sharp
threshold not seen in AMPA — at gNMDA = 1.0 the cell is silent, then at gNMDA = 2.0 it fires 3
spikes via regenerative escape.

## Visualizations

* **Per-gNMDA panel grid** — 8 panels showing FULL (red, solid) vs EPSP_PASSIVE (blue,
  dashed). The 2.0 nS panel reveals the regenerative escape clearly:

![NMDA-only voltage response
grid](../../../tasks/t0061_nmda_escape_pd_only_no_gaba/results/images/voltage_response_grid.png)

* **All 16 traces overlaid** — colour-graded by gNMDA (viridis). The wide NMDA plateaus at
  gNMDA
  >= 5 are the headline shape contrast vs t0060's narrow AMPA EPSPs:

![NMDA-only voltage response
overlay](../../../tasks/t0061_nmda_escape_pd_only_no_gaba/results/images/voltage_response_overlay.png)

## Analysis / Discussion

**(1) Mg-block creates a sharp threshold absent in AMPA.** Below gNMDA = 1 nS the cell is
near-silent — at V_rest = -65 mV, the Boltzmann factor `1 / (1 + n*exp(-gamma*v)) = 1 / (1 +
0.25*exp(0.08*65)) = 1 / 44.6 = 0.022` admits only ~2% of the open-channel conductance. At
gNMDA = 2 nS aggregate (200 nS total), even 2% of that is ~4 nS effective driving conductance,
just enough to depolarize the soma; once depolarized to -50 mV, Mg block weakens further (3.5×
weaker than at -65 mV), opening more channels — runaway regenerative escape.

**(2) NMDA produces sustained plateau depolarizations.** Once the cell crosses Mg-block
threshold, the slow `tau_decay = 80 ms` vs AMPA's 2.5 ms keeps the soma depolarized for
200-400 ms. The plateau dwell time can support multiple action potentials but eventually
adapts (refractory period + sodium inactivation + slow K+ activation).

**(3) Spike count is non-monotonic in gNMDA.** The peak count is at gNMDA = 2-10 nS (3 spikes
each); at gNMDA = 15 it drops to 2 spikes; at gNMDA = 20 it drops to 1 spike. This is the
sodium-channel-saturation effect again — extreme synaptic conductance shunts the cell, the
depolarization rises so fast that HH gating cannot recover between spikes.

**(4) HH save-and-zero validation re-confirmed.** EPSP_PASSIVE peak Vm rises monotonically
from -64.47 to -2.70 mV without crossing E_NMDA = 0 mV. The save-and-zero is correctly wired
even under the regenerative NMDA mechanism.

## Examples

The 16 trial results in fenced code block format from `summary_pd_only.csv`:

```csv
gnmda_ns,mode,peak_vm_mv,min_vm_mv,n_spikes,n_samples
0.100000,full,-64.220245,-65.000000,0,2189
0.100000,epsp_passive,-64.470631,-65.000000,0,2049
0.500000,full,-62.609188,-65.000000,0,2255
0.500000,epsp_passive,-63.097544,-65.000000,0,2107
1.000000,full,-58.886243,-65.000000,0,2391
1.000000,epsp_passive,-60.972164,-65.000000,0,2236
2.000000,full,11.286241,-66.483551,3,3253
2.000000,epsp_passive,-52.583205,-65.000000,0,2516
5.000000,full,13.124538,-66.323121,3,3286
5.000000,epsp_passive,-8.591432,-65.000000,1,3098
10.000000,full,13.207894,-66.218074,3,3294
10.000000,epsp_passive,-4.670621,-65.000000,1,3174
15.000000,full,13.154832,-66.156142,2,3279
15.000000,epsp_passive,-3.371102,-65.000000,1,3206
20.000000,full,13.205621,-66.087335,1,3265
20.000000,epsp_passive,-2.704876,-65.000000,1,3220
```

## Limitations

* Single trial per condition.
* NMDA-only (no AMPA priming). With AMPA at typical 0.5 nS, the regenerative escape would
  occur at lower gNMDA — see t0054 / t0055 results.
* Single direction (PD only, no DSI).
* gNMDA = 20 nS is biophysically extreme.
* NetCon spike threshold = -20 mV yields false-positive crossings in EPSP_PASSIVE at gNMDA >=
  5.

## Verification

Verificator outcomes:

* `verify_task_file.py` — PASSED 0 errors.
* `verify_task_dependencies.py` — PASSED 0/0.
* `verify_suggestions.py` — PASSED 0/0.
* `verify_task_metrics.py` — PASSED 0/0.
* `verify_task_results.py` — PASSED 0 errors.
* `verify_task_folder.py` — PASSED 0 errors.
* `verify_logs.py` — PASSED 0 errors.

| Check | Status |
| --- | --- |
| `voltage_traces_pd_only.csv`, `summary_pd_only.csv`, `wallclock.json` exist | PASS |
| Both PNGs rendered | PASS |
| EPSP_PASSIVE peak Vm < E_NMDA (0 mV) at every gNMDA | PASS (max -2.70 mV) |
| FULL peak Vm > 0 mV at every gNMDA >= 2 nS | PASS (range +11.29 to +13.21 mV) |
| Placement seed = 0, bit-identical to t0060 | PASS |

## Files Created

* `tasks/t0061_nmda_escape_pd_only_no_gaba/code/{paths,constants,nmda_bootstrap,nmda_synapse,run_pd_only,plot_traces}.py`
* `tasks/t0061_nmda_escape_pd_only_no_gaba/code/mod/NMDA_MgBlock.mod` (verbatim from t0055)
* `tasks/t0061_nmda_escape_pd_only_no_gaba/code/run_nrnivmodl.cmd`
* `tasks/t0061_nmda_escape_pd_only_no_gaba/results/{voltage_traces_pd_only,summary_pd_only}.csv`
* `tasks/t0061_nmda_escape_pd_only_no_gaba/results/{wallclock,placement_seed0}.json`
* `tasks/t0061_nmda_escape_pd_only_no_gaba/results/images/{voltage_response_grid,voltage_response_overlay}.png`

## Task Requirement Coverage

The task as commissioned: "Now do exactly the same analysis with NMDAR." Concrete requirements
from the analog of t0060:

* **REQ-1 (GABA = 0)**: Done — `GABA_BASE_NS = 0.0`, no GABA synapses constructed.
* **REQ-2 (single direction = preferred)**: Done — `ANGLE_DEG = 0` (preferred direction).
* **REQ-3 (HH on)**: Done — `TrialMode.FULL` runs (8/16 trials).
* **REQ-4 (HH off)**: Done — `TrialMode.EPSP_PASSIVE` with HH save-and-zero on soma + AIS
  (8/16 trials).
* **REQ-5 (gNMDA sweep at 8 specified values)**: Done — `GNMDA_NS_VALUES = (0.1, 0.5, 1.0,
  2.0, 5.0, 10.0, 15.0, 20.0)`.
* **REQ-6 (record soma potential)**: Done — `voltage_traces_pd_only.csv` carries native dt
  samples for all 16 trials.
* **REQ-7 (plot all responses)**: Done — `voltage_response_grid.png` (8 panels per gNMDA) and
  `voltage_response_overlay.png` (all 16 traces colour-graded by gNMDA).
* **REQ-8 (NMDA-only excitation)**: Done — Mg-block NMDA via `NMDA_MgBlock.mod` (Jahr-Stevens
  voltage-dependent), no AMPA Exp2Syn.

</details>
