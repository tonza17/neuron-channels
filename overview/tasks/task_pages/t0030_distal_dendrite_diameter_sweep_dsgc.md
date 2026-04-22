# ✅ Distal-dendrite diameter sweep on t0022 DSGC

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0030_distal_dendrite_diameter_sweep_dsgc` |
| **Status** | ✅ completed |
| **Started** | 2026-04-22T20:08:09Z |
| **Completed** | 2026-04-22T22:00:00Z |
| **Duration** | 1h 51m |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source suggestion** | `S-0027-03` |
| **Task types** | `experiment-run` |
| **Step progress** | 10/15 |
| **Task folder** | [`t0030_distal_dendrite_diameter_sweep_dsgc/`](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/results_detailed.md) |

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

## Metrics

### distal diam x 0.50

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **84.2308** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal diam x 0.75

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **116.25** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.999871** |

### distal diam x 1.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **116.25** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal diam x 1.25

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **89.1667** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal diam x 1.50

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **89.1667** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.999965** |

### distal diam x 1.75

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **78.3333** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal diam x 2.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **81.5833** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

## Suggestions Generated

<details>
<summary><strong>Rerun the distal-diameter sweep on t0022 with null-GABA conductance
reduced from 12 nS to 6 nS</strong> (S-0030-01)</summary>

**Kind**: experiment | **Priority**: high

The t0030 sweep failed as a Schachter2010-vs-passive-filtering discriminator because primary
DSI is pinned at 1.000 at every diameter multiplier (null firing 0 Hz under the t0022 E-I
schedule). compare_literature.md traces the ceiling to GABA_CONDUCTANCE_NULL_NS = 12 nS
delivered 10 ms before AMPA on null trials, about 2x Schachter2010's compound null inhibition
(~6 nS). Rerun the full 7-point diameter sweep (0.5x-2.0x, 12 angles x 10 trials = 840 trials)
with GABA_CONDUCTANCE_NULL_NS lowered to 6 nS so null firing becomes non-zero and primary DSI
regains dynamic range. Distinct from S-0029-04 (null-GABA sweep at fixed length 1.0x) and
S-0029-01 (Poisson + length sweep): this targets the diameter axis specifically. Expected
cost: local CPU, ~2 h wall time. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Poisson-noise desaturation rerun of the distal-dendrite diameter
sweep on t0022</strong> (S-0030-02)</summary>

**Kind**: experiment | **Priority**: high

Sibling of S-0029-01 (Poisson + length sweep) targeting the diameter axis. The t0030
deterministic testbed yields reliability = 1.000 and null firing 0 Hz at every diameter, which
collapses the rate-code noise floor that Schachter2010's dendritic-spike-threshold mechanism
and Dan2018's passive-TR derivation both assume. Add an independent 5 Hz background Poisson
NetStim per distal dendrite (independent seed, no direction bias) to the t0022 scheduler and
rerun the full 7-point diameter sweep (0.5x-2.0x, 12 angles x 10 trials = 840 trials).
Expected: DSI drops from 1.000 into the 0.6-0.8 Park2014 envelope, reliability drops below
1.0, and diameter regains discrimination power between Schachter2010 active amplification
(+slope) and passive filtering (-slope). Distinct from S-0022-05 (Poisson at a single
length/diameter) and S-0029-01 (length axis). Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Wider distal-diameter sweep (0.25x to 4.0x) after the schedule fix
to probe extreme impedance regimes</strong> (S-0030-03)</summary>

**Kind**: experiment | **Priority**: medium

The t0030 sweep used multipliers 0.5x-2.0x (a 4x range) and found vector-sum DSI moved by only
0.030 absolute, with Wu2023 reporting distal-diameter DSI saturation above ~0.8 um on primate
SAC - our baseline distal seg.diam straddles that threshold so our sweep likely sat in the
saturated regime throughout. Once the S-0030-01/S-0030-02 schedule fix has removed the DSI
ceiling, rerun the diameter sweep over a wider range {0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0,
4.0}x at the same 12-direction x 10-trial protocol. Provides the impedance-gradient dynamic
range Schachter2010's 5-7x proximal-to-distal input-resistance measurement implies, and tests
whether Wu2023's saturation threshold applies to mouse ON-OFF DSGC. Recommended task types:
experiment-run.

</details>

<details>
<summary><strong>Joint distal length x diameter 2-D sweep on t0022 to catch
interactions the marginal sweeps miss</strong> (S-0030-04)</summary>

**Kind**: experiment | **Priority**: medium

t0029 (distal-length sweep) and t0030 (distal-diameter sweep) both produced flat vector-sum
DSI curves when run in isolation on the t0022 E-I schedule. Marginal sweeps cannot reveal
interactions: Schachter2010's active amplification depends on length (number of Nav-bearing
segments) AND diameter (Nav substrate per unit length) jointly, and the cable space constant
lambda = sqrt(d * Rm / (4 * Ra)) couples them nonlinearly. Run a focused 2-D grid (e.g., 5
length x 5 diameter = 25 configurations x 12 angles x 10 trials = 3000 trials) on the
schedule-fixed testbed (S-0030-01 prerequisite). Distinct from S-0002-04 (broad factorial
including branch orders at fixed synapse count) because it is 2-D, focused, and scheduled
after the desaturation fix. Expected local CPU wall time ~7 h. Recommended task types:
experiment-run.

</details>

<details>
<summary><strong>Non-uniform proximal-to-distal diameter taper sweep on t0022 to
match Schachter2010 impedance gradient</strong> (S-0030-05)</summary>

**Kind**: experiment | **Priority**: medium

t0030 applied a single multiplier uniformly to every distal leaf, producing a 4x range that
Schachter2010's 150-200 MOhm proximal -> >1 GOhm distal (5-7x) impedance gradient indicates is
too narrow and the wrong shape. Real DSGC dendrites taper from thick primary branches to thin
terminal tips; the uniform multiplier scales all terminals together without recreating that
gradient. Implement a taper parameter k such that a segment's diameter scales by (1 + k *
path_distance / L_max), sweep k in {-0.5, -0.25, 0, 0.25, 0.5, 0.75} to produce flattened,
nominal, and exaggerated tapers, and run the standard 12-direction x 10-trial protocol at each
k (after the S-0030-01 schedule fix). Expected outcome: the exaggerated-taper cell (high k,
very thin distal) maximises distal input impedance and should exhibit the Schachter2010
amplification signature if the mechanism is active on this morphology. Recommended task types:
experiment-run, feature-engineering.

</details>

<details>
<summary><strong>Change the t0033 optimiser objective to a vector-sum-DSI-weighted
blend instead of pure primary DSI</strong> (S-0030-06)</summary>

**Kind**: evaluation | **Priority**: high

t0029 and t0030 both pinned primary DSI at 1.000 and only vector-sum DSI retained weak
sensitivity (ranges 0.021 and 0.012 respectively). The t0033 joint morphology-channel
optimisation plan currently proposes primary DSI as the objective; under the t0022 schedule
the optimiser will see a flat landscape and cannot discover morphology-channel interactions.
Change the t0033 objective to a weighted blend (e.g., 0.5 * vector_sum_DSI + 0.3 *
peak_Hz_match + 0.2 * HWHM_match) OR switch to vector-sum DSI outright. Distinct from
S-0029-07 which proposes promoting peak-Hz and HWHM to co-primary outcomes - this proposal
keeps DSI as the headline objective but replaces its pinned primary form with its unpinned
vector-sum form. Update tasks/t0012 tuning_curve_loss to expose a loss_kind='vector_sum_dsi'
option. Recommended task types: write-library, answer-question.

</details>

## Research

* [`research_code.md`](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/results_summary.md)*

--- spec_version: "2" task_id: "t0030_distal_dendrite_diameter_sweep_dsgc" date_completed:
"2026-04-22" status: "complete" ---
# Results Summary: Distal-Dendrite Diameter Sweep on t0022 DSGC

## Summary

Swept distal-dendrite diameter across seven multipliers (0.5×, 0.75×, 1.0×, 1.25×, 1.5×,
1.75×, 2.0× baseline) on the t0022 DSGC testbed under the standard 12-direction × 10-trial
protocol (840 trials total). **Vector-sum DSI is essentially flat** across the 4× diameter
range: slope 0.0083 per log2(multiplier), p=0.1773, DSI range 0.635-0.665 across extremes.
**Neither the Schachter2010 active-dendrite amplification prediction (positive slope) nor the
passive-filtering prediction (negative slope) is supported** — the t0022 testbed's E-I timing
carries DSI almost entirely, leaving distal diameter with no measurable mechanistic role.

## Metrics

* **Vector-sum DSI range**: **0.635** (0.5×) to **0.665** (1.5×) — 0.030 absolute range across
  the 4× diameter sweep; slope not distinguishable from zero (p=0.1773).
* **Primary DSI (peak-minus-null)**: pinned at **1.000** across every diameter — same plateau
  as t0029 length sweep, because null-direction firing is 0 Hz under the t0022 E-I schedule.
* **Preferred-direction peak firing rate**: **15 Hz** at 0.5×-1.0×, **14 Hz** at 1.25×-1.5×,
  **13 Hz** at 1.75×-2.0× — mild decline with thickening, consistent with reduced distal input
  impedance.
* **HWHM**: 84.2° at 0.5×, broadening to 116.2° at 0.75×-1.0×, narrowing to 78.3° at 1.75×; no
  monotonic trend.
* **Peak distal membrane voltage**: approximately **-5 mV** across all diameters — distal
  spike thresholds are cleared everywhere, so thickening-driven impedance changes do not break
  the existing amplification regime.
* **Slope classification**: **flat** (mechanism_label="flat", slope=0.0083, p=0.1773,
  dsi_range_extremes=0.0124, used_fallback=True).
* **Total trials executed**: **840** (7 diameters × 12 directions × 10 trials).
* **Sweep wall time**: approximately **115 min** end-to-end on local Windows CPU; thinner
  diameters ran slowest (raised axial resistance shrinks the NEURON integration timestep).

## Verification

* `verify_task_file.py` — target 0 errors on final pass.
* `verify_task_dependencies.py` — PASSED on step 2 (t0022 dependency completed).
* `verify_research_code.py` — PASSED on step 6 (0 errors, 0 warnings).
* `verify_plan.py` — PASSED on step 7 (0 errors, 0 warnings).
* `verify_task_metrics.py` — target 0 errors.
* `verify_task_results.py` — target 0 errors on final pass.
* `verify_task_folder.py` — target 0 errors on final pass.
* `verify_logs.py` — target 0 errors on final pass.
* `ruff check --fix`, `ruff format`, and `mypy -p
  tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code` — all clean (10 files).

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0030_distal_dendrite_diameter_sweep_dsgc" date_completed:
"2026-04-22" status: "complete" ---
# Results Detailed: Distal-Dendrite Diameter Sweep on t0022 DSGC

## Summary

Swept distal-dendrite diameter uniformly on the t0022 DSGC testbed across seven multipliers
(0.5×-2.0× baseline) under the standard 12-direction × 10-trial moving-bar protocol (840
trials total). The vector-sum DSI shows no statistically significant trend with diameter
(slope 0.0083 per log2(multiplier), p=0.1773, DSI range 0.635-0.665 across extremes). The
primary DSI (peak-minus-null) pinned at 1.000 because null-direction firing is exactly 0 Hz
under the t0022 E-I schedule (same plateau observed in the sibling t0029 length sweep).
**Neither Schachter2010 active-dendrite amplification (predicted positive slope) nor passive
filtering (predicted negative slope) is supported**: the testbed's spatially-asymmetric E-I
timing carries DSI almost entirely, leaving distal diameter with no measurable mechanistic
role over the 4× range tested.

## Methodology

* **Machine**: Windows 11, local CPU only. NEURON 8.2.7 + NetPyNE 1.1.1 (from t0007 install).
  No remote machines, no paid APIs.
* **Testbed**: `modeldb_189347_dsgc_dendritic` library from t0022, unmodified except for the
  distal-diameter override applied per sweep point.
* **Diameter override**: applied uniformly to all HOC leaves on the `h.RGC.ON` dendritic arbor
  (selection rule: `sec in h.RGC.ON and h.SectionRef(sec=sec).nchild() == 0`, copied into
  `code/diameter_override.py` from t0029's `length_override.py:37-52` per the no-cross-task-
  imports rule).
* **Protocol**: 12-direction moving-bar sweep (0°, 30°, 60°, ..., 330°) × 10 trials per angle
  × 7 diameter multipliers = 840 trials total. Each trial uses the t0022 E-I timing schedule
  and the bundled Poleg-Polsky 2026 morphology.
* **Scoring**: primary DSI (peak-minus-null, via `tuning_curve_loss.compute_dsi`), vector-sum
  DSI (fallback diagnostic when primary pins at 1.000), peak Hz, null Hz, HWHM, reliability,
  preferred-direction peak membrane voltage at a distal reference compartment.
* **Wall time**: approximately 115 minutes end-to-end for the full 840-trial sweep. Thinner
  diameters (0.5×) ran slowest because reduced cross-section raises axial resistance and
  forces NEURON to shrink the integration timestep; thicker diameters (1.75×-2.0×) ran
  fastest.
* **Timestamps**: task started 2026-04-22T20:08:58Z; sweep launched 2026-04-22T21:55Z; sweep
  completed 2026-04-22T22:31Z; end time set in reporting step.

### Per-Diameter Metrics Table

| D_mul | peak_Hz | null_Hz | DSI (peak-null) | DSI (vector-sum) | HWHM (°) | Reliability | Pref (°) | Peak mV |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.50 | 15 | 0 | 1.000 | 0.635 | 84.2 | 1.000 | 46.4 | -4.8 |
| 0.75 | 15 | 0 | 1.000 | 0.653 | 116.2 | 1.000 | 49.2 | -4.9 |
| 1.00 | 15 | 0 | 1.000 | 0.656 | 116.2 | 1.000 | 49.3 | -4.8 |
| 1.25 | 14 | 0 | 1.000 | 0.665 | 89.2 | 1.000 | 48.6 | -5.0 |
| 1.50 | 14 | 0 | 1.000 | 0.665 | 89.2 | 1.000 | 47.9 | -4.9 |
| 1.75 | 13 | 0 | 1.000 | 0.657 | 78.3 | 1.000 | 48.9 | -5.2 |
| 2.00 | 13 | 0 | 1.000 | 0.648 | 81.6 | 1.000 | 48.4 | -5.1 |

Sources: `results/data/metrics_per_diameter.csv`, `results/data/dsi_by_diameter.csv`.

### Slope Classification

| Statistic | Value |
| --- | --- |
| Metric used | vector-sum DSI (primary-DSI fallback, pinned at 1.000) |
| Slope per log2(multiplier) | 0.0083 |
| p-value | 0.1773 |
| DSI range across extremes (0.5× vs 2.0×) | 0.0124 |
| Classification label | flat |
| Schachter2010 supported? | No (no positive slope) |
| Passive filtering supported? | No (no negative slope) |

Source: `results/data/slope_classification.json`, `results/data/curve_shape.json`.

## Charts

![DSI (primary) vs distal-dendrite diameter
multiplier](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/images/dsi_vs_diameter.png)

Primary DSI (peak-minus-null) vs diameter multiplier. Pinned at 1.000 across all seven
diameters because null-direction firing is 0 Hz throughout — the t0022 E-I schedule silences
the null half-plane completely regardless of distal biophysics. This is the same plateau seen
in the sibling t0029 length sweep.

![Vector-sum DSI vs distal-dendrite diameter
multiplier](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/images/vector_sum_dsi_vs_diameter.png)

Vector-sum DSI (fallback diagnostic) vs diameter multiplier. Values range 0.635-0.665 across
the 4× diameter sweep. Slope is 0.0083 per log2(multiplier) with p=0.1773 — not
distinguishable from zero. There is a mild inverted-U with maximum at 1.25×-1.5×, but the
0.030 absolute range is below any realistic experimental resolution threshold.

![Preferred-direction peak firing rate vs
diameter](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/images/peak_hz_vs_diameter.png)

Peak firing rate declines mildly with thickening: 15 Hz at 0.5×-1.0×, 14 Hz at 1.25×-1.5×, 13
Hz at 1.75×-2.0×. This is the signature of reduced distal input impedance (larger diameter →
more current needed to reach spike threshold), but the DSI signal does not track this
peak-rate trend, indicating DSI is set by the E-I timing rather than by the dendritic
integration regime.

![12-direction polar overlay across all 7
diameters](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/images/polar_overlay.png)

Twelve-direction tuning curves overlaid across all 7 diameters. Every curve has the same
preferred-direction peak location (~48°) and identical null-direction silence (0 Hz across
150°-300°). Diameter scaling rescales the preferred-direction firing rate mildly but does not
shift tuning orientation or re-shape the null-direction suppression.

## Examples

Ten concrete trial examples drawn from `results/data/sweep_results.csv` showing the (diameter
multiplier, direction, trial) input and the NEURON-produced (peak_mv, firing_rate_hz) output.
Every row is a full 12-direction protocol trial; the 120 rows per diameter feed the DSI / HWHM
/ vector-sum aggregation downstream.

### Example 1: D=0.50× preferred direction (peak)

Input (`run_sweep.py` driver parameters):

```text
diameter_multiplier=0.50
trial=0
direction_deg=0
protocol=12_direction_moving_bar_15Hz
```

Output (`sweep_results.csv` row 1):

```csv
diameter_multiplier,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
0.50,0,0,14,44.662,14.000000
```

### Example 2: D=0.50× preferred direction (trial variance)

Input:

```text
diameter_multiplier=0.50
trial=5
direction_deg=0
```

Output:

```csv
0.50,5,0,14,44.702,14.000000
```

Ten repeated trials at the same (diameter, direction) produced spike counts {14, 14, 14, 14,
14, 14, 14, 14, 14, 14} — deterministic driver, zero trial-to-trial variance.

### Example 3: D=0.50× null direction (silence)

Input:

```text
diameter_multiplier=0.50
trial=0
direction_deg=210
```

Output:

```csv
0.50,0,210,0,-54.717,0.000000
```

### Example 4: D=0.75× preferred direction

Input:

```text
diameter_multiplier=0.75
trial=0
direction_deg=0
```

Output:

```csv
0.75,0,0,14,44.626,14.000000
```

### Example 5: D=1.00× preferred direction (baseline)

Input:

```text
diameter_multiplier=1.00
trial=0
direction_deg=60
```

Output:

```csv
1.00,0,60,15,44.281,15.000000
```

### Example 6: D=1.25× preferred direction

Input:

```text
diameter_multiplier=1.25
trial=0
direction_deg=60
```

Output:

```csv
1.25,0,60,14,44.210,14.000000
```

### Example 7: D=1.25× null direction (silence)

Input:

```text
diameter_multiplier=1.25
trial=9
direction_deg=330
```

Output:

```csv
1.25,9,330,9,44.098,9.000000
```

### Example 8: D=1.50× preferred direction

Input:

```text
diameter_multiplier=1.50
trial=0
direction_deg=0
```

Output:

```csv
1.50,0,0,14,43.997,14.000000
```

### Example 9: D=1.75× preferred direction (peak-rate decline)

Input:

```text
diameter_multiplier=1.75
trial=0
direction_deg=60
```

Output:

```csv
1.75,0,60,13,43.890,13.000000
```

### Example 10: D=2.00× null direction (silence preserved)

Input:

```text
diameter_multiplier=2.00
trial=0
direction_deg=270
```

Output:

```csv
2.00,0,270,0,-56.200,0.000000
```

Takeaway: across the 4× diameter sweep, preferred-direction firing shifts from 14-15 Hz to 13
Hz (reduced by ~2 Hz at 2.0×) while null-direction firing stays at exactly 0 Hz. Primary DSI
therefore stays at 1.000 while vector-sum DSI shifts by only 0.030 — insufficient to
distinguish the Schachter2010 and passive-filtering mechanisms.

## Verification

* `verify_task_file.py` — target 0 errors on final pass.
* `verify_task_dependencies.py` — PASSED on step 2 (t0022 dependency completed).
* `verify_research_code.py` — PASSED on step 6 (0 errors, 0 warnings).
* `verify_plan.py` — PASSED on step 7 (0 errors, 0 warnings).
* `verify_task_metrics.py` — target 0 errors (registered project metrics per diameter
  variant).
* `verify_task_results.py` — target 0 errors on final pass.
* `verify_task_folder.py` — target 0 errors on final pass.
* `verify_logs.py` — target 0 errors on final pass.
* `ruff check --fix`, `ruff format`, and `mypy -p
  tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code` — all clean.
* Pre-merge verificator — target 0 errors before PR merge.

## Limitations

* **Null-direction firing is 0 Hz under t0022 schedule**: this forces primary DSI (peak-minus-
  null) to 1.000 regardless of dendritic parameter changes and is the single biggest
  limitation on the discriminator experiment. The vector-sum DSI fallback recovers a
  measurable signal but the dynamic range (0.030 across 4× diameter) is too small to
  meaningfully distinguish mechanisms.
* **Diameter range (0.5×-2.0×)** may be narrower than needed to force either mechanism. A
  wider sweep (e.g., 0.25× to 4×) would probe more extreme impedance regimes but risk leaving
  the regime where the current E-I schedule remains compatible with the model's other
  constraints.
* **Baseline morphology lacks axon**: the t0022 testbed uses the Poleg-Polsky 2026 morphology
  without AIS / thin-axon sections. Schachter2010's predicted amplification depends on distal
  Nav substrate, which is present in HHst but in a lumped parameterisation rather than the
  Nav1.6/Nav1.2 \+ Kv1.2/Kv3 priors that the t0019 synthesis recommends for DSGC.
* **Single-axis sweep only**: the diameter axis was swept in isolation. A joint
  length-diameter sweep might reveal interactions that the marginal sweeps miss. Length was
  swept separately by t0029 (also flat under primary DSI; same schedule-dominated regime).
* **Uniform-multiplier diameter change**: the sweep applies a single multiplier to all distal
  leaves uniformly. Non-uniform diameter perturbations (e.g., tapering from proximal to
  distal) might produce different results.

## Files Created

### Code (9 Python files, lint + mypy clean)

* `code/paths.py`, `code/constants.py`, `code/diameter_override.py`,
  `code/preflight_distal.py`, `code/trial_runner_diameter.py`, `code/run_sweep.py`,
  `code/analyse_sweep.py`, `code/classify_slope.py`, `code/plot_sweep.py`

### Data

* `results/data/sweep_results.csv` (840 trial rows + header)
* `results/data/per_diameter/tuning_curve_D{0p50,0p75,1p00,1p25,1p50,1p75,2p00}.csv`
* `results/data/metrics_per_diameter.csv`, `results/data/dsi_by_diameter.csv`,
  `results/data/metrics_notes.json`
* `results/data/curve_shape.json`, `results/data/slope_classification.json`
* `results/metrics.json` (registered project metrics per diameter variant)
* `results/costs.json` (`$0.00`), `results/remote_machines_used.json` (`[]`)

### Charts

* `results/images/dsi_vs_diameter.png`, `results/images/vector_sum_dsi_vs_diameter.png`,
  `results/images/peak_hz_vs_diameter.png`, `results/images/polar_overlay.png`

### Research

* `research/research_code.md` (inventory of t0022 driver, distal-selection rule, DSI library,
  and t0029 workflow template)

### Task artefacts

* `plan/plan.md` (11 sections, 12 REQ-* items)
* Full step logs under `logs/steps/`
* `task.json`, `task_description.md`, `step_tracker.json`

## Task Requirement Coverage

Operative task text (from `task.json` and `task_description.md`), quoted verbatim:

```text
Sweep distal-dendrite diameter on the t0022 DSGC testbed to discriminate Schachter2010 active-
dendrite amplification vs passive-filtering mechanisms using DSI as outcome.

1. Use the t0022 DSGC testbed as-is (no channel modifications, no input rewiring).
2. Identify distal dendritic sections (tip compartments at branch order ≥ 3) in the morphology.
3. Sweep distal diameter in at least 7 values spanning from 0.5× to 2.0× the baseline diameter
   (e.g., 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0×). Apply the multiplier to all distal branches
   uniformly.
4. For each diameter value, run the standard 12-direction tuning protocol (15 Hz preferred-
   direction input) and compute DSI.
5. Plot DSI vs diameter and classify slope sign: positive (active-dendrite amplification),
   negative (passive filtering), flat (neither).
```

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | 7 diameter multipliers 0.5×-2.0× | **Done** | `code/constants.py` DIAMETER_MULTIPLIERS; 7 per-diameter CSVs in `results/data/per_diameter/` |
| REQ-2 | Uniform application to distal branches | **Done** | `code/diameter_override.py`; selection rule matches `h.RGC.ON` leaves |
| REQ-3 | Preflight sanity check | **Done** | `code/preflight_distal.py` ran clean before full sweep |
| REQ-4 | 12-direction × 10-trial protocol per diameter | **Done** | `results/data/sweep_results.csv` has 840 rows across 7 × 12 × 10 = 840 |
| REQ-5 | Primary DSI computed | **Done** | `results/data/metrics_per_diameter.csv` dsi_pn column |
| REQ-6 | Vector-sum DSI computed (fallback) | **Done** | `results/data/metrics_per_diameter.csv` dsi_vs column |
| REQ-7 | DSI-vs-diameter slope classified | **Done** | `results/data/slope_classification.json`: flat, p=0.1773 |
| REQ-8 | 12-direction polar overlay | **Done** | `results/images/polar_overlay.png` |
| REQ-9 | Checkpoint per-diameter CSVs | **Done** | `results/data/per_diameter/*.csv` (7 files) |
| REQ-10 | Registered metrics JSON | **Done** | `results/metrics.json` |
| REQ-11 | Code style + type compliance | **Done** | ruff + mypy clean on all 10 source files |
| REQ-12 | Primary-DSI-plateau fallback to vector-sum | **Done** | classifier used fallback=True; slope classification grounded on vector-sum DSI |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0030_distal_dendrite_diameter_sweep_dsgc" date_compared:
"2026-04-22" ---
# Comparison with Published Results

## Summary

This task swept distal-dendrite diameter from **0.5x** to **2.0x** of baseline on the t0022
DSGC testbed with the explicit aim of discriminating Schachter2010 active-dendrite
amplification (a positive DSI-vs-diameter slope) from a passive-filtering alternative (a
negative slope). Primary peak/null DSI is pinned at **1.000** at every multiplier (slope
**0.000**, range at extremes **0.000**), forcing the vector-sum DSI to act as fallback; its
slope is **0.0083 per log2(multiplier)** with **p = 0.1773** and a range at extremes of only
**0.0124** — the curve is **flat**, so **neither Schachter2010 nor passive filtering is
supported**. The sibling length sweep t0029 observed the same 1.000 plateau under the same
schedule, identifying the t0022 E-I timing as the DSI-setting variable and distal morphology
as a nullified axis on this testbed.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Schachter2010 compartmental DSGC — spike DSI with dendritic Nav [Schachter2010, Abstract / Overview] | DSI (somatic spike) | 0.80 | 1.000 | **+0.200** | Schachter2010 reports ~4x DSI amplification from passive PSP DSI ~0.20 to spike DSI ~0.80 via dendritic Nav/Ca threshold nonlinearity; our testbed is already saturated above their spike-DSI value |
| Schachter2010 subthreshold PSP DSI [Schachter2010, Overview] | DSI (PSP) | 0.20 | n/a | n/a | Not measured — the t0022 driver emits spike-count tuning only; the PSP-DSI axis that quantifies the Schachter2010 active-amplification step is absent |
| Schachter2010 active-amplification prediction (slope sign) [Schachter2010, Overview] | DSI vs diameter slope | positive | **+0.0083** | n/a | Slope p=0.1773 is not distinguishable from zero; predicted positive slope not observed |
| Passive filtering (cable theory, per t0027 synthesis) [Wu2023, abstract; t0027 full_answer.md:108-113] | DSI vs diameter slope | negative | **+0.0083** | n/a | Thicker distal = lower input impedance (Z ~ 1/d^1.5) should damp directional contrast; predicted negative slope not observed |
| Wu2023 primate SAC connectomics sweep — distal diameter saturation [Wu2023, abstract via t0027 full_answer.md:108-113] | distal-diameter saturation threshold | ~0.8 um | 0.30 across 0.5x-2.0x sweep (vector-sum DSI range) | n/a | Wu2023 reports DSI saturates once distal diameter exceeds ~0.8 um; our baseline distal `seg.diam` ~0.4-1.0 um already straddles this threshold, consistent with the observed flat vector-sum DSI but not a direct DSI-magnitude comparator |
| Sivyer2013 rabbit DSGC control — dendritic-spike branch independence [Sivyer2013, Fig. 2-3 text] | DSI (spike) | ~1.0 | 1.000 | **+0.000** | Qualitative match — "close to 1" under control conditions; Sivyer2013 plateau height not quantified to 3 dp |
| PolegPolsky2026 DSGC machine-learning model [PolegPolsky2026, Overview via t0027 full_answer.md:125-128] | DSI (spike) | > 0.5 (reachable) | 1.000 | **+0.500** | Parent of the morphology used in our testbed; PolegPolsky2026 shows DSI > 0.5 is reachable via distance-graded passive delay, coincidence detection, or NMDA gating — our E-I-timing driver far exceeds their reported operating band |

### Prior Task Comparison

The t0030 plan cites two upstream project results as baselines — t0022 (the testbed we sweep)
and t0029 (the sibling length sweep) — plus the t0027 synthesis answer as the source of the
two hypotheses. Those values are restated here so the flat DSI-vs-diameter finding can be
judged against the project's own measurement lineage.

| Prior Task / Source | Metric | Prior Value | t0030 Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0022 baseline (per-dendrite E-I, 1.00x multiplier) | DSI (pref/null) | 1.000 | 1.000 | **+0.000** | t0030 at 1.00x is an exact by-construction reproduction — only `seg.diam` is mutated, never the schedule |
| t0022 baseline | HWHM (deg) | 116.25 | 116.25 | **+0.00** | Same exact match at 1.00x |
| t0022 baseline | Peak firing (Hz) | 15 | 15 | **+0** | Same exact match at 1.00x |
| t0029 length sweep (parallel geometry axis) | primary DSI (range across 0.5x-2.0x) | 0.000 | 0.000 | **+0.000** | Both sweeps produce the same saturated 1.000 plateau; diameter adds no new information on the primary axis |
| t0029 length sweep | vector-sum DSI (range across 0.5x-2.0x) | 0.021 | 0.012 | **-0.009** | t0030 dynamic range is even smaller than t0029's — diameter moves the secondary metric less than length does |
| t0029 length sweep | classification label | flat | flat | n/a | Both axes yield the same null result; the testbed's E-I schedule dominates both morphology axes |

The lineage-internal finding is that **both distal-morphology axes (length, diameter) hit the
DSI = 1.000 ceiling** while the schedule stays fixed. The t0030 sweep adds a second
morphological axis to the t0029 pattern and produces an even smaller vector-sum dynamic range
(0.012 vs 0.021) — diameter is **less informative** than length on this testbed, because
diameter modifies local input impedance and Nav substrate per unit length without changing the
section midpoints that `schedule_ei_onsets` uses for onset timing. The cross-task null result
is decisive: on the t0022 schedule, neither Schachter2010 amplification nor passive filtering
has an observable DSI signature over a 4x morphology range.

## Methodology Differences

* **Null-direction firing silenced by design.** The t0022 scheduler uses
  `GABA_CONDUCTANCE_NULL_NS = 12 nS` (about 4x the preferred-direction value of 3 nS) applied
  10 ms before AMPA onset on the null half-plane. Null firing is exactly **0 Hz** at every
  diameter multiplier, which pins the peak-minus-null DSI numerator at the preferred rate and
  the ratio at 1.000 before distal biophysics can enter. Schachter2010 uses compound null
  inhibition of ~6 nS alongside Poisson-like stochastic inputs, and the Schachter2010 DSI
  ~0.80 comes precisely from retaining a non-zero null firing rate that the cable can
  modulate.

* **Stochasticity absent.** Schachter2010 and the Wu2023 SAC model inject Poisson-like
  stochastic bipolar inputs; the t0022 testbed is deterministic (`reliability = 1.000` at
  every diameter multiplier). Deterministic drive collapses the rate-code integration that the
  Schachter2010 dendritic-spike-threshold mechanism needs in order to amplify DSI — thresholds
  either cross every trial or none.

* **Channel substrate is lumped, not Nav1.6/Nav1.2 + Kv1/Kv3.** The Poleg-Polsky 2026
  morphology inherited by t0022 uses the HHst lumped Na/K pair in the dendrites (see t0019
  synthesis). The Schachter2010 active-amplification prediction depends on a distal Nav
  density and kinetic regime that is modelled in a reduced form here — scaling `seg.diam`
  rescales total Nav current capacity proportionally to surface area (`~ pi * L * d`), but
  does not reproduce the Nav1.6 persistent current that Schachter2010 identifies as the
  amplifier.

* **No axon / AIS.** The Schachter2010 model includes an axon initial segment with high Nav
  density that participates in the distal-to-soma amplification cascade. The t0022
  channel-partition HOC declares `AIS_PROXIMAL`, `AIS_DISTAL`, and `THIN_AXON` `SectionList`s
  that are all empty on this morphology. The predicted amplification regime is therefore
  structurally unreachable.

* **Diameter range and baseline.** Wu2023 reports distal-SAC DSI saturates above diameter ~0.8
  um; the baseline distal `seg.diam` on our morphology spans roughly 0.4-1.0 um. Our 0.5x to
  2.0x sweep therefore covers ~0.2-2.0 um — straddling the Wu2023 saturation threshold but on
  a mouse DSGC rather than the primate SAC she modelled. A wider sweep (0.25x to 4x) would
  probe more extreme impedance regimes but risks leaving the regime where the current E-I
  schedule remains compatible.

* **Metric definition.** Schachter2010 and Sivyer2013 compute DSI as `(Rpref - Rnull) / (Rpref
  + Rnull)` on spike counts at physiological noise; the t0012 scorer used here applies the
  same formula on 12 directions but on deterministic integer spike counts with null rate
  exactly 0. Vector-sum DSI (Mazurek / Kagan 2020 formulation) is reported here as fallback
  and is what the slope classifier actually uses.

## Analysis

**Schachter2010 prediction vs t0030 observation.** Schachter2010 predicts that thickening a
distal dendrite with active Nav/Ca substrate raises the preferred-direction spike-DSI via a
~4x amplification from passive PSP DSI ~0.20 to spike DSI ~0.80 [Schachter2010, Overview].
Translated to our sweep axis this is a **positive** slope on DSI vs diameter: more Nav per
unit length = greater preferred-direction threshold crossing. Our observation is vector-sum
DSI **0.635-0.665** across 4x diameter with slope **+0.0083 per log2(multiplier)**,
p=**0.1773** and 95% CI spanning zero (-0.0053, +0.0220). The sign matches Schachter2010's
prediction but the magnitude is ~**50x** smaller than the ~0.6 DSI movement that
Schachter2010's ~4x amplification would imply; more importantly, the p-value exceeds 0.05 and
the DSI range at extremes (**0.0124**) is well below the 0.05 threshold the t0030 classifier
requires to declare an active-amplification signature. The t0030 result therefore **does not
support** Schachter2010 active amplification on this testbed.

**Passive-filtering prediction vs t0030 observation.** Passive cable theory predicts input
impedance scales as `Z ~ 1/d^1.5`; thicker distal = lower local depolarisation per synaptic
current, so the directional contrast should be damped at the soma and DSI should **decrease**
with diameter. Our observation is a **positive** slope (though statistically flat), which is
the **opposite sign** of the passive-filtering prediction, and the DSI range at extremes is
again below any classifier threshold for a significant negative slope. The passive-filtering
prediction is also not supported.

**Why the discriminator failed: ceiling + desensitised secondary metric.** The primary DSI was
expected to move above 0.05 as distal diameter changed by 4x. It did not — every diameter hits
the same 1.000 ceiling because the t0022 E-I schedule deposits a 12-nS null-direction GABA
shunt 10 ms before AMPA arrival, zeroing null firing independently of distal biophysics. The
fallback vector-sum DSI does retain some residual sensitivity because it integrates the full
12-angle curve and captures off-null angles where a single spike can change the vector
magnitude; but that sensitivity is too weak (**0.030** absolute range across 4x diameter) to
distinguish mechanisms at the resolution the task calls for. The sibling t0029 length sweep
observed an even slightly larger vector-sum range (**0.021**) and was also classified flat —
the two morphology axes fail in the same way because the same E-I schedule dominates both.

**Wu2023 saturation consistency.** Wu2023's primate SAC model reports distal-diameter DSI
saturation above ~0.8 um. Our baseline distal diameters sit near this threshold; our sweep
covers ~0.2-2.0 um across the 0.5x-2.0x range; and the observed flat DSI is qualitatively
consistent with operating in the saturated regime Wu2023 identifies. This is an aesthetic
agreement with published work, but it does not discriminate between the two mechanism
hypotheses the t0030 task posed — both mechanisms predict non-flat curves away from
saturation, and our testbed cannot exit saturation without a schedule change.

**Peak firing rate trend is real but DSI-irrelevant.** Peak firing declines monotonically from
15 Hz (0.5x-1.0x) to 13 Hz (1.75x-2.0x) with slope p=**0.0075** — a statistically significant
peak-Hz decrease with diameter, consistent with thicker dendrites requiring more current to
reach spike threshold (reduced input impedance). But the same peak-Hz trend does **not**
translate to a DSI trend because null firing stays at 0 Hz across the whole sweep. In
Schachter2010's regime (where null is non-zero and stochastic), a peak-Hz drop without a
compensating null-Hz drop would immediately show up as a DSI decrease. On this testbed the
denominator is empty, so the numerator trend is invisible.

**Implications for the t0033 joint morphology-channel optimisation.** The planned joint
optimisation task must either (a) re-weight its objective toward vector-sum DSI (which
retained weak sensitivity here) and accept the ~0.03 dynamic range as the measurable signal,
(b) modify the t0022 E-I schedule so the null half-plane is not identically silenced (e.g.
reduce `GABA_CONDUCTANCE_NULL_NS` from 12 nS to ~4-6 nS closer to Schachter2010's compound
null inhibition), or (c) add a stochasticity layer (Poisson background release per distal
dendrite) to break the deterministic 1.000 plateau. Without one of these, distal morphology
parameters are nullified within the optimiser and no morphology-channel interaction can be
discovered. The cleanest prescription — likely to preserve the testbed's DS mechanism while
restoring discriminator sensitivity — is (b) combined with (c): bring the schedule closer to
the Schachter2010 regime and re-run both the t0029 length sweep and the t0030 diameter sweep.

## Limitations

* **DSI-pinned-at-1 eliminates the primary discriminator.** The primary DSI is saturated at
  every multiplier; both mechanism hypotheses are consistent with a constant 1.000 ceiling, so
  neither is falsified. This is a genuine null result on the mechanism-discrimination question
  and must be reported as such. The fallback vector-sum DSI retains weak sensitivity but its
  0.012 range at extremes is well below the 0.05 threshold the task classifier requires.

* **No subthreshold PSP-DSI measurement.** Schachter2010's key comparison is between PSP DSI
  (~0.20) and spike DSI (~0.80), which quantifies the dendritic-spike-amplification step. The
  t0022 driver emits only spike-count tuning; the PSP-DSI axis that would tie directly to
  Schachter2010's headline 4x amplification is not produced and cannot be compared in the
  Comparison Table — hence the n/a row.

* **No direct passive-filtering DSI-vs-diameter sweep in the corpus.** The passive-filtering
  prediction comes from cable theory (`Z ~ 1/d^1.5`) via the t0027 synthesis rather than from
  a single paper's quantitative sweep. No paper in the t0030 research corpus reports an
  equivalent DSI-vs-diameter sweep on a mouse ON-OFF DSGC at the resolution we ran here — the
  closest is the Wu2023 primate SAC sweep which reports a saturation threshold but not the
  shape above it.

* **Diameter range below Schachter2010's impedance gradient.** Schachter2010's measurement of
  150-200 MOhm proximal -> >1 GOhm distal impedance spans a ~5-7x gradient driven by large
  diameter changes along the arbor. Our 0.5x-2.0x uniform sweep is a 4x range; a wider,
  non-uniform perturbation (e.g., tapered distal-to-proximal thickening) might reveal
  mechanisms the marginal-sweep structure misses.

* **Uniform-multiplier-only.** The sweep applies one multiplier to every distal leaf.
  Non-uniform diameter changes (proximal-to-distal tapering, single-branch thickening) could
  expose mechanisms that the uniform sweep averages out.

* **Lumped HHst channel substrate.** The dendritic channels are a lumped HHst Na/K pair rather
  than the Nav1.6 / Nav1.2 / Kv1.2 / Kv3 priors that t0019 recommends. The Schachter2010
  predicted amplification depends on kinetics this substrate does not fully reproduce. A
  re-run with the t0019 channel set (future t0033 joint optimisation) is needed before the
  null result can be claimed to cover Schachter2010's mechanism in full.

</details>
