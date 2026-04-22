# ⏹ Distal-dendrite diameter sweep on t0022 DSGC

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0030_distal_dendrite_diameter_sweep_dsgc` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source suggestion** | `S-0027-03` |
| **Task types** | `experiment-run` |
| **Task folder** | [`t0030_distal_dendrite_diameter_sweep_dsgc/`](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/task_description.md)*

# Distal-Dendrite Diameter Sweep on t0022 DSGC

## Motivation

The t0027 literature synthesis identified distal-dendrite diameter as a second-axis
discriminator between competing DS mechanisms that are individually consistent with our
current t0022 tuning data (DSI peak 0.6555 at V_rest = -60 mV, 15 Hz input):

* **Schachter2010 active-dendrite amplification** predicts DSI increases with distal
  thickening, because thicker distal compartments host more Na+ channel substrate per unit
  length and therefore amplify preferred-direction local spikes more strongly than passive
  EPSPs.
* **Passive-filtering alternatives** predict DSI decreases with distal thickening, because
  thicker dendrites have lower input impedance and less local depolarisation per unit synaptic
  current, so the directional contrast from asymmetric input patterns is damped.

A single-parameter sweep of distal diameter on the t0022 testbed, measuring DSI only, will
discriminate these mechanisms — a positive slope favours Schachter2010 active dendrites; a
negative slope favours passive filtering. Source suggestion **S-0027-03** (high priority) from
the t0027 literature synthesis.

## Scope

1. Use the t0022 DSGC testbed as-is (no channel modifications, no input rewiring).
2. Identify distal dendritic sections (tip compartments at branch order ≥ 3) in the
   morphology.
3. Sweep distal diameter in at least 7 values spanning from 0.5× to 2.0× the baseline diameter
   (e.g., 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0×). Apply the multiplier to all distal branches
   uniformly.
4. For each diameter value, run the standard 12-direction tuning protocol (15 Hz preferred-
   direction input) and compute DSI.
5. Plot DSI vs diameter and classify slope sign: positive (active-dendrite amplification),
   negative (passive filtering), flat (neither).

## Approach

* Local CPU only. No remote compute, no paid API.
* Reuse t0022 testbed code — copy relevant scripts into this task's `code/` directory.
* Vary the `diam` attribute on distal compartments by the sweep multiplier in a single
  experiment driver script.
* Use the existing tuning-curve scoring library from t0012 for DSI computation (consistent
  with t0022/t0026).
* Save per-sweep-point results to `results/data/sweep_results.csv`.
* Generate DSI-vs-diameter chart at `results/images/dsi_vs_diameter.png`.

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary with headline DSI-vs-diameter
  slope sign and mechanism classification.
* `results/results_detailed.md` — full methodology, per-direction breakdown at each diameter
  value, slope sign classification, and discussion of which mechanism the data favours.
* `results/images/dsi_vs_diameter.png` — DSI-vs-diameter plot.
* `results/metrics.json` — DSI values at each diameter point.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* Local CPU only. Expected runtime: 30-90 minutes.
* $0 external cost.

## Measurement

* Primary metric: **DSI** at each diameter value.
* Secondary (recorded but not primary): per-direction spike counts, preferred-direction firing
  rate, peak voltage at a reference distal compartment (to confirm passive-impedance changes).

## Key Questions

1. Is the DSI-vs-diameter slope positive, negative, or flat?
2. If positive, is the slope consistent with Na+ channel-density amplification as predicted by
   Schachter2010?
3. If negative, does the preferred-direction firing rate drop alongside DSI (consistent with
   general damping) or does only the null-direction rate change?

## Dependencies

* **t0022_modify_dsgc_channel_testbed** (completed) — provides the DSGC morphology and channel
  set including Nav density.

## Scientific Context

Source suggestion **S-0027-03** (high priority). Complementary to t0029 distal-length sweep:
length varies the spatial extent of distal integration, diameter varies the local impedance
and channel substrate. Together they span the two most important biophysical axes highlighted
in the t0027 synthesis.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 synthesis already did this), and
  `setup-machines` / `teardown` (local CPU).
* Include `compare-literature` — compare the DSI-vs-diameter curve to Schachter2010
  predictions.
* Can be executed in parallel with t0029 in a separate worktree.

</details>
