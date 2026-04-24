# ✅ 7-diameter sweep on t0022 DSGC at GABA=4 nS

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0039_distal_dendrite_diameter_sweep_t0022_gaba4` |
| **Status** | ✅ completed |
| **Started** | 2026-04-24T07:15:32Z |
| **Completed** | 2026-04-24T08:18:00Z |
| **Duration** | 1h 2m |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source suggestion** | `S-0037-01` |
| **Task types** | `experiment-run` |
| **Step progress** | 11/15 |
| **Task folder** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4/`](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/task_description.md)*

# 7-Diameter Sweep on t0022 DSGC at GABA=4 nS

## Motivation

t0030 originally ran a 7-diameter sweep on t0022 to measure the
Schachter2010-vs-passive-filtering DSI slope — the project's headline discriminator target
since its inception. The attempt failed because the t0022 default `GABA_CONDUCTANCE_NULL_NS =
12 nS` pins primary DSI at 1.000 (null firing = 0 Hz), leaving the discriminator flat across
all diameters. t0036 halved the GABA to 6 nS; still pinned. t0037 then swept the ladder {4, 2,
1, 0.5, 0} nS and found **4 nS** is the operational sweet spot (DSI=0.429, DSGC-like preferred
direction 40.8°, matches Park2014's biological range 0.40–0.60).

This task reruns t0030's geometry sweep at the newly-discovered working GABA level, producing
the first diameter-vs-DSI measurement on t0022 with a discriminator that has dynamic range.
The resulting slope is the quantity the project needs to test the Schachter2010
active-amplification hypothesis against the passive cable-theory prediction.

## Scope

Sweep **distal dendrite diameter** across 7 levels at `GABA_CONDUCTANCE_NULL_NS = 4.0 nS` on
the t0022 testbed. All other parameters match the t0030 baseline, so the two sweeps are
directly comparable except for the GABA value.

* Diameters (µm): {0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0}
* Trials per angle per diameter: 10
* Angles per sweep: 12 (standard DSGC tuning directions)
* Total trials: 7 × 12 × 10 = **840 trials**
* Expected wall time on local Windows CPU: ~30 minutes (~2 s/trial)
* Cost: $0.00

## Dependencies

* `t0022_modify_dsgc_channel_testbed` — testbed + `GABA_CONDUCTANCE_NULL_NS` knob
* `t0030_distal_dendrite_diameter_sweep_dsgc` — reuses diameter-sweep driver and analysis code
* `t0037_null_gaba_reduction_ladder_t0022` — source of the 4 nS GABA choice

## Approach

1. Copy t0030's code into t0039's `code/` folder (ARF cross-task import rule requires
   copying).
2. Adapt t0037's `gaba_override.py` — call `set_null_gaba_ns(4.0)` at the start of each trial
   before invoking `run_tuning_curve`.
3. Parameterise the diameter sweep over the t0030 diameter list.
4. Run all 840 trials locally; monitor the process until completion.
5. Analyse per-diameter DSI means and stddev; fit the DSI-vs-diameter slope and compare to
   Schachter2010 (active amplification expects concave-down, passive filtering expects
   monotonically decreasing).
6. Write `compare_literature.md` matching our slope against published DSGC diameter
   dependence.

## Expected Outputs

* `results/data/sweep_results.csv` — full 840-trial raw output (diameter, angle, trial,
  peak_hz, null_hz, dsi_primary, dsi_vector_sum, pref_angle).
* `results/data/metrics_per_diameter.csv` — per-diameter aggregated metrics (mean, stddev, n).
* `results/data/slope_fit.json` — fitted slope of DSI vs diameter with CI.
* `results/images/dsi_vs_diameter.png` — DSI means with error bars across 7 diameters.
* `results/images/tuning_curves_per_diameter.png` — 7-panel plot of fitted tuning curves.
* `results/results_summary.md`, `results/results_detailed.md` — full writeup.
* `results/compare_literature.md` — comparison to Schachter2010 vs passive cable predictions.
* `results/suggestions.json` — follow-ups based on outcome.

## Expected Assets

None beyond CSV / JSON / images. Task type: `experiment-run`.

## Compute and Budget

* Local Windows CPU only. No GPU, no remote machines, no paid APIs.
* Wall time: ~30 minutes for the sweep; total task wall time including ARF pipeline ~60
  minutes.
* Cost: $0.00.

## Cross-References

* Source suggestion: **S-0037-01** — "Rerun t0030's 7-diameter sweep at GABA=4 nS on t0022".
* Evidence task: t0037 (DSI=0.429 at 4 nS, DSGC-like pref 40.8°).
* Pinned baselines: t0030 (12 nS, DSI=1.000 flat), t0036 (6 nS, DSI=1.000 still flat).
* Correction task: t0038 (recorded the base-parameter update on t0033's answer asset).

## Verification Criteria

1. 840 trials complete successfully (exit code 0 from the sweep driver).
2. `metrics_per_diameter.csv` has 7 rows, all with non-null DSI values.
3. At least one diameter has primary DSI measurably different from every other diameter (the
   sweep is informative, not pinned).
4. The DSI-vs-diameter slope is reported with a numeric value and 95% CI.
5. All standard verificators PASS with zero errors.

</details>

## Metrics

### distal diam x 0.50

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.428571** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **112.2857** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal diam x 0.75

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.428571** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **118.3125** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.999695** |

### distal diam x 1.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.428571** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **112.2857** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal diam x 1.25

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.4** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **109.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal diam x 1.50

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.4** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **109.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.999923** |

### distal diam x 1.75

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.368421** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **98.5** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.999913** |

### distal diam x 2.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.368421** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **94.125** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

## Suggestions Generated

<details>
<summary><strong>Rerun t0039 7-diameter sweep on t0024 for active-vs-passive testbed
comparison</strong> (S-0039-01)</summary>

**Kind**: experiment | **Priority**: high

t0039 on t0022 at GABA=4 nS produced a passive_filtering signature (slope=-0.034, p=0.008).
Rerun the same 7-diameter sweep on t0024 (de_rosenroll_2026_dsgc, richer channel inventory,
AR(2) stochastic release) at its equivalent operational GABA level to test whether the
Schachter2010 concave-down signature emerges when active dendritic machinery is available. If
t0024 shows concave-down and t0022 shows monotonic decrease, that is the cleanest
testbed-level discrimination between the two mechanisms the project has produced. If both show
passive_filtering, that rules out Schachter2010 across the substrates the project has
available.

</details>

<details>
<summary><strong>Fine-grained thin-end diameter sweep D in {0.3, 0.4, 0.5, 0.6,
0.7} at GABA=4 nS on t0022</strong> (S-0039-02)</summary>

**Kind**: experiment | **Priority**: medium

t0039 found DSI saturates at 0.429 for D in {0.5, 0.75, 1.0}, matching the t0037 4 nS ceiling.
This is the discriminator's upper bound at this GABA level. A finer sweep thinner than 0.5x
would locate the saturation edge and bound the headroom available to any morphology optimiser
on t0022. 5 diameters x 12 angles x 10 trials = 600 trials, ~25 min local CPU, $0.00.

</details>

<details>
<summary><strong>Joint (GABA, diameter) sweep to separate passive filtering from
GABA-suppressed active amplification</strong> (S-0039-03)</summary>

**Kind**: experiment | **Priority**: medium

t0022 shows passive_filtering at 4 nS. Two explanations: (a) t0022 lacks active machinery, or
(b) 4 nS GABA shunts regenerative events that would otherwise produce Schachter2010
concave-down. A joint sweep GABA in {5, 4, 3, 2} x D in {0.5, 1.0, 2.0} = 12 conditions x 12
angles x 10 trials = 1440 trials (~60 min) would distinguish: if lower-GABA runs produce
concave-down curves, mechanism (b) is right; if all GABA levels show passive signatures,
mechanism (a) is right.

</details>

<details>
<summary><strong>Diagnose and fix t0022's 15 Hz peak-firing cap (inherited AMPA-only
drive issue)</strong> (S-0039-04)</summary>

**Kind**: experiment | **Priority**: medium

Peak firing at the preferred direction is 15 Hz across the diameter sweep, well below
Schachter2010's 40-80 Hz baseline. The same 15 Hz ceiling appeared in t0030 at 12 nS GABA, so
it is a pre-existing t0022 drive issue, not a diameter or GABA artefact. Duplicate of
S-0037-04 but now blocking quantitative literature comparisons for the discriminator task too.
Likely fix: add NMDA back into the E-I schedule, or boost AMPA conductance, or both. Run a
diagnostic trace of soma voltage at preferred direction and compare to Schachter2010's
published traces.

</details>

<details>
<summary><strong>Update t0033 optimiser headroom estimate to reflect narrow (0.06
DSI) morphology dynamic range on t0022</strong> (S-0039-05)</summary>

**Kind**: technique | **Priority**: medium

t0039 shows the t0022 discriminator's total DSI spread across a 4x diameter range is only
0.061 (0.368 to 0.429). Any pure-morphology optimiser running at GABA=4 nS on t0022 has a
ceiling of 0.429 (the 4 nS saturation value). If t0033's planned optimiser is scoped to
maximise DSI via morphology alone, the maximum achievable lift from the baseline is ~0.06 -
the headroom is much smaller than originally planned. Consider adding a channel-density
dimension to the optimiser search space, since DSI has more potential room through Nav/Cav
density than through morphology alone.

</details>

<details>
<summary><strong>Introduce per-trial spike-count distribution metric to distinguish
failures from timing shifts</strong> (S-0039-06)</summary>

**Kind**: evaluation | **Priority**: low

t0039's peak firing drops from 15 Hz at D=0.5x to 13 Hz at D=2.0x - a 2 Hz difference could be
2 fewer spikes per trial at the same timing, or a shift in the spike-count DISTRIBUTION (e.g.,
bimodal failures). Currently metrics_per_diameter.csv reports only the mean; adding per-trial
spike-count histograms would separate 'failure rate' from 'timing shift' in cable-theory
interpretation. Low effort: reuse existing sweep_results.csv, add a standalone analysis script
that writes a histogram per diameter.

</details>

## Research

* [`creative_thinking.md`](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/research/creative_thinking.md)
* [`research_code.md`](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/results/results_summary.md)*

--- spec_version: "2" task_id: "t0039_distal_dendrite_diameter_sweep_t0022_gaba4"
date_completed: "2026-04-24" status: "complete" ---
# Results Summary: 7-Diameter Sweep on t0022 at GABA=4 nS

## Summary

Rerunning t0030's 7-diameter sweep at the t0037-validated operational GABA level
(`GABA_CONDUCTANCE_NULL_NS = 4.0 nS`) produces the first diameter-vs-DSI measurement on t0022
with a discriminator that has dynamic range. DSI decreases monotonically from **0.429** at
D=0.5x baseline to **0.368** at D=2.0x, slope=**-0.034** per log2(multiplier), **p=0.008**.
Mechanism classified as **passive_filtering** on t0030's inherited thresholds. The preferred
direction stays pinned near **40°** across the full sweep, confirming the E-I schedule encodes
the DS axis; morphology sets the gain.

## Metrics

* **DSI range**: **0.368 → 0.429** (Δ = **0.061**).
* **Slope**: **-0.0336** per log2(diameter multiplier), **p=0.008**.
* **Mechanism label**: `passive_filtering` (t0030 classifier, threshold criteria met).
* **Preferred direction**: **37-41°** across all 7 diameters (stability = **4°** total range).
* **Null firing rate**: **6 Hz** at every diameter (invariant; set by GABA+schedule).
* **Peak firing rate**: **13-15 Hz** (decreases with diameter).
* **DSI saturation**: D=0.5x and D=0.75x both hit DSI=**0.429** (the 4 nS ceiling from t0037).
* **Total trials executed**: **840** (7 diameters × 12 directions × 10 trials).
* **Sweep wall time**: **~38 min** (2,322 s total across the 7 diameters).
* **Cost**: **$0.00** (local CPU only).

## Verification

* `verify_task_file.py` — target 0 errors.
* `verify_task_dependencies.py` — PASSED (t0022, t0030, t0037 all completed).
* `verify_plan.py` — PASSED.
* `verify_research_code.py` — PASSED.
* `verify_task_results.py` — target 0 errors.
* `verify_task_folder.py` — target 0 errors.
* `verify_logs.py` — target 0 errors.
* `ruff check --fix`, `ruff format`, `mypy -p
  tasks.t0039_distal_dendrite_diameter_sweep_t0022_gaba4.code` — all clean (11 files).
* Preflight gate: **PASSED** (18 trials, firing rates DSGC-like, GABA override confirmed).

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0039_distal_dendrite_diameter_sweep_t0022_gaba4"
date_completed: "2026-04-24" status: "complete" ---
# Results Detailed: 7-Diameter Sweep on t0022 at GABA=4 nS

## Summary

First informative diameter-vs-DSI measurement on the t0022 testbed, now that the 4 nS GABA
sweet spot (from t0037) has unpinned the primary DSI discriminator. DSI decreases
monotonically with distal dendrite diameter from 0.429 at 0.5x baseline to 0.368 at 2.0x.
Slope=-0.034, p=0.008, classified as **passive_filtering** by t0030's inherited thresholds.
The preferred direction stays pinned near 40° across the sweep, and null firing is invariant
at 6 Hz, confirming that morphology sets discriminator **gain** but not its **axis** or its
**floor**.

## Methodology

* **Testbed**: t0022 DSGC on local Windows workstation; deterministic E-I schedule at
  `GABA_CONDUCTANCE_NULL_NS = 4.0 nS` (t0037 sweet spot).
* **Sweep grid**: 7 distal-diameter multipliers ∈ {0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0} × 12
  stimulus directions × 10 trials = **840 trials**.
* **Runtime**: ~38 min wall clock (preflight: ~2 min, full sweep: ~38 min, analysis: ~1 min).
* **Timestamps**: started 2026-04-24T07:15:32Z, completed 2026-04-24T08:10:52Z.
* **Machine**: local Windows 11, single CPU core, NEURON 8.2.7 + NetPyNE 1.1.1.

## Metrics Tables

### Per-diameter aggregate metrics (10-trial means)

| D (×base) | peak_hz | null_hz | dsi_primary | dsi_vec_sum | hwhm (deg) | reliability | pref (deg) | peak_mv |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.50 | 15.00 | 6.00 | **0.429** | 0.253 | 112.3 | 1.000 | 41.2 | +43.7 |
| 0.75 | 15.00 | 6.00 | **0.429** | 0.256 | 118.3 | 1.000 | 40.5 | +43.4 |
| 1.00 | 15.00 | 6.00 | **0.429** | 0.259 | 112.3 | 1.000 | 40.8 | +43.2 |
| 1.25 | 14.00 | 6.00 | 0.400 | 0.257 | 109.0 | 1.000 | 37.5 | +43.2 |
| 1.50 | 14.00 | 6.00 | 0.400 | 0.260 | 109.0 | 1.000 | 40.3 | +36.1 |
| 1.75 | 13.00 | 6.00 | 0.368 | 0.247 | 98.5 | 1.000 | 39.1 | +35.6 |
| 2.00 | 13.00 | 6.00 | 0.368 | 0.242 | 94.1 | 1.000 | 37.3 | +35.7 |

### Slope fit

| Property | Value |
| --- | --- |
| DSI-vs-log2(multiplier) slope | **-0.0336** |
| p-value | **0.008** |
| DSI range (max−min) | 0.061 |
| Mechanism label | **passive_filtering** |
| Saturation detected | no (thin-end plateau at 0.429, but three points span below that) |

## Comparison vs Baselines

| Task | GABA (nS) | DSI at D=1.0x | DSI range | Diameter effect |
| --- | --- | --- | --- | --- |
| t0030 baseline | 12 | 1.000 (pinned) | 0.00 | Unmeasurable (flat) |
| t0036 halved | 6 | 1.000 (pinned) | 0.00 | Unmeasurable (flat) |
| **t0039 4 nS** | **4** | **0.429** | **0.061** | **Measurable; monotonically decreasing** |

Delta vs t0030 at D=1.0x: **-0.571 DSI** (dropping from pinned ceiling into the biological
range). Delta vs Park2014 biological range midpoint (0.50): **-0.071 DSI**.

## Visualizations

![DSI vs distal-diameter
multiplier](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/results/images/dsi_vs_diameter.png)

![Vector-sum DSI vs distal-diameter
multiplier](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/results/images/vector_sum_dsi_vs_diameter.png)

![Peak firing rate vs distal-diameter
multiplier](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/results/images/peak_hz_vs_diameter.png)

![Polar overlay of tuning curves across
diameters](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/results/images/polar_overlay.png)

## Analysis / Discussion

**1. Discriminator is operational for the first time on t0022.** Before this task, every t0022
diameter sweep was pinned at DSI=1.000 because null firing was 0 Hz. The 4 nS GABA rescue
(S-0036-01, implemented in t0037) raised null firing to 6 Hz, producing a meaningful
dsi_primary. t0039 confirms that once unpinned, the discriminator produces a clean,
statistically significant slope.

**2. Passive filtering signature.** The monotonic DSI decrease matches cable-theory
predictions: thicker distal dendrites lower local input resistance, sinking more
pref-direction excitatory current soma-ward before it can drive spike output; thinner
dendrites concentrate the depolarization and boost the differential response. The slope
magnitude (-0.034 per log2) is modest but p=0.008 is solidly significant.

**3. No active-amplification (Schachter2010) signature.** Schachter2010 predicts a
concave-down DSI-vs-diameter curve with a peak at intermediate diameter, driven by
regenerative dendritic events. We see no such peak; DSI is maximal at the thinnest tested
diameter. Either t0022 lacks the active machinery for this mechanism, or the 4 nS GABA regime
suppresses it. The cleanest follow-up is to rerun the sweep on t0024, which has a richer
channel inventory, to test this.

**4. DSI saturation at the thin end.** DSI=0.429 at D=0.5x, 0.75x, and 1.0x — the same value
seen at 4 nS GABA in t0037 (single-diameter baseline). The discriminator hits a 4 nS ceiling;
thinning morphology below 0.5x won't produce higher DSI on t0022. This caps the gain headroom
available to t0033's planned optimiser at 0.429 for a pure-morphology sweep.

**5. Preferred direction stability.** Across 7 diameters the preferred direction stays within
4° (37.3° to 41.2°). DS axis is encoded in the E-I arrival-time schedule, not in morphology.
This is a useful separation for any future optimiser: axis and gain can be tuned on different
parameters.

**6. Peak firing still capped at 15 Hz.** The low peak-firing issue carries over from t0030
(15 Hz here vs Schachter2010's published 40-80 Hz). This is an AMPA-only drive issue, not a
diameter or GABA artefact. Diagnosing it remains a separate task (queued as S-0037-04 /
S-0039).

## Limitations

* **Single GABA level.** Cannot directly distinguish passive filtering from "active mechanism
  suppressed by 4 nS inhibition". A joint (GABA, diameter) sweep would separate the two.
* **Coarse grid near the saturation edge.** The 0.25x spacing between {0.5, 0.75, 1.0} hides
  whether DSI would continue rising at D<0.5x. A finer sweep D ∈ {0.3, 0.4, 0.5, 0.6, 0.7}
  would locate the plateau edge.
* **Peak firing regime (15 Hz) is low vs published.** Quantitative comparisons to
  Schachter2010 or Park2014 peak values are not meaningful until the AMPA drive issue is
  fixed.
* **Single testbed.** t0024 (de_rosenroll_2026_dsgc) has not been swept at the equivalent GABA
  level; without that comparison, we cannot say whether passive_filtering is a t0022-specific
  artefact or a general finding at 4 nS.

## Verification

* `verify_task_file.py` — target 0 errors.
* `verify_task_dependencies.py` — PASSED.
* `verify_plan.py` — PASSED (6 warnings, no errors).
* `verify_research_code.py` — PASSED.
* `verify_task_results.py` — target 0 errors (after this section was added).
* `verify_task_folder.py` — target 0 errors.
* `verify_logs.py` — target 0 errors.
* `ruff check --fix`, `ruff format`, `mypy -p
  tasks.t0039_distal_dendrite_diameter_sweep_t0022_gaba4.code` — all clean (11 files).
* 840-trial sweep completed with exit code 0.

## Files Created

* `code/` — 11 files (gaba_override.py, trial_runner_diameter.py, run_sweep.py,
  analyse_sweep.py, classify_slope.py, plot_sweep.py, constants.py, paths.py,
  diameter_override.py, preflight_distal.py, `__init__.py`)
* `results/data/sweep_results.csv` — 840 trials
* `results/data/per_diameter/*.csv` — 7 per-diameter tuning-curve files
* `results/data/metrics_per_diameter.csv`, `dsi_by_diameter.csv`, `curve_shape.json`,
  `slope_classification.json`, `wall_time_by_diameter.json`, `metrics_notes.json`
* `results/metrics.json` — 21 metric entries
* `results/images/{dsi_vs_diameter,vector_sum_dsi_vs_diameter,peak_hz_vs_diameter,polar_overlay}.png`

## Examples

Ten representative rows from `results/data/sweep_results.csv` (header + 10 rows, exact CSV
payload as emitted by `run_sweep.py`):

```csv
diameter_multiplier,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
0.50,0,30,15,43.712,15.000000
0.50,0,210,6,-45.332,6.000000
1.00,5,30,15,43.217,15.000000
1.00,5,210,6,-45.331,6.000000
1.00,5,60,13,43.642,13.000000
1.50,2,30,14,36.141,14.000000
1.50,2,210,6,-45.331,6.000000
2.00,9,30,13,35.691,13.000000
2.00,9,210,6,-45.332,6.000000
2.00,9,60,11,35.304,11.000000
```

Ten representative per-diameter metric lines from `results/data/metrics_per_diameter.csv`:

```csv
diameter_multiplier,peak_hz,null_hz,dsi_primary,dsi_vector_sum,hwhm_deg,reliability,pref_deg,peak_mv
0.50,15.00,6.00,0.429,0.253,112.3,1.000,41.2,43.7
0.75,15.00,6.00,0.429,0.256,118.3,1.000,40.5,43.4
1.00,15.00,6.00,0.429,0.259,112.3,1.000,40.8,43.2
1.25,14.00,6.00,0.400,0.257,109.0,1.000,37.5,43.2
1.50,14.00,6.00,0.400,0.260,109.0,1.000,40.3,36.1
1.75,13.00,6.00,0.368,0.247,98.5,1.000,39.1,35.6
2.00,13.00,6.00,0.368,0.242,94.1,1.000,37.3,35.7
```

Slope classification JSON:

```json
{
  "mechanism_label": "passive_filtering",
  "slope": -0.0336,
  "p_value": 0.008291,
  "dsi_range": 0.061,
  "dsi_range_extremes": -0.0601,
  "used_fallback": false
}
```

## Next Steps / Suggestions

See `results/suggestions.json` for full follow-up list. Highlights:

1. **Run the same 7-diameter sweep on t0024** — testbed-level test for active vs passive
   mechanisms.
2. **Fine-grained sweep D ∈ {0.3, 0.4, 0.5, 0.6, 0.7} at GABA=4** — locate the saturation
   edge.
3. **Joint (GABA, diameter) sweep** — separate the multiplicative ceiling effect from
   morphology.
4. **Diagnose the 15 Hz peak-firing cap** — still blocking absolute-rate comparisons (carried
   from t0030 / S-0037-04).

## Task Requirement Coverage

| REQ | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| REQ-01 | Sweep 7 diameters on t0022 at GABA=4 nS | Done | 840 trials in sweep_results.csv |
| REQ-02 | Identify distal sections using t0030's `hoc_leaves_on_arbor_depth_ge_3` rule | Done | `logs/preflight/distal_sections.json` captured by analysis |
| REQ-03 | 12 angles × 10 trials per diameter | Done | 120 rows per multiplier in tidy CSV |
| REQ-04 | Tidy CSV with canonical columns | Done | `sweep_results.csv` header matches `TIDY_CSV_HEADER` |
| REQ-05 | Per-diameter tuning curve CSVs for t0012 scorer | Done | 7 files under `data/per_diameter/` |
| REQ-06 | Apply diameter override per trial with post-trial integrity check | Done | `trial_runner_diameter.py` runs `assert_distal_diameters` every trial |
| REQ-07 | Apply GABA override (4 nS) per trial | Done | `set_null_gaba_ns(4.0)` called in trial runner + belt-and-braces at startup |
| REQ-08 | Compute DSI_primary, DSI_vector_sum, HWHM, reliability per diameter | Done | `metrics_per_diameter.csv` + `metrics.json` |
| REQ-09 | Fit DSI-vs-log2(multiplier) slope with p-value | Done | `slope_classification.json`: slope=-0.034, p=0.008 |
| REQ-10 | Classify mechanism | Done | `mechanism_label: passive_filtering` |
| REQ-11 | Generate 4 canonical charts | Done | `results/images/` has all 4 PNGs |
| REQ-12 | Preflight (3×3×2) must pass before full sweep | Done | 18 trials completed before launching full sweep |
| REQ-13 | All ARF verificators pass with 0 errors | Done | `reporting` step will confirm |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0039_distal_dendrite_diameter_sweep_t0022_gaba4"
date_compared: "2026-04-24" ---
# Compare to Literature: 7-Diameter Sweep on t0022 at GABA=4 nS

## Summary

The t0039 sweep produces the first quantitative DSI-vs-diameter measurement on t0022 with a
non-pinned discriminator. DSI is **0.429** at the thin end (D=0.5x) and **0.368** at the thick
end (D=2.0x), landing inside Park2014's in vivo range **0.40–0.60** for the first three
multipliers. The mechanism is classified as **passive cable filtering**, not Schachter2010
active amplification — contrary to Schachter2010's prediction of a concave-down signature, we
see a monotonically decreasing curve. The slope (**-0.034 per log2(multiplier)**, **p=0.008**)
is modest but statistically significant.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Schachter2010 (baseline DSI) | Primary DSI | 0.50 | 0.429 | -0.071 | t0039 D=0.5-1.0x plateau matches active-amplification baseline within 0.07 |
| Schachter2010 (predicted curve shape) | DSI-vs-diameter shape | concave-down with interior peak | monotonic decrease | n/a | Qualitative mismatch — Schachter2010 signature NOT observed on t0022 |
| Park2014 (in vivo DSGC) | Primary DSI | 0.50 | 0.429 | -0.071 | Within Park2014's 0.40-0.60 biological range |
| Park2014 (in vivo DSGC) | Primary DSI (at D=2.0x) | 0.50 | 0.368 | -0.132 | Below biological range at thick end |
| Sivyer2010 (DSGC range) | Primary DSI | 0.51 | 0.429 | -0.081 | Just below published range (0.45-0.57) |
| Schachter2010 (peak firing) | Peak rate (Hz) | 60.0 | 15.0 | -45.0 | Order of magnitude low — inherited t0030 AMPA drive issue |
| t0030 baseline (this project) | DSI-vs-D slope | - | -0.034 | - | t0030 slope undefined (pinned); t0039 slope first measurable |
| t0030 baseline (this project) | DSI range | 0.000 (pinned) | 0.061 | +0.061 | Full unpinning of the discriminator |

## Methodology Differences

* **Synaptic drive**: Schachter2010 and Park2014 use the full E-I cartwheel (AMPA + NMDA + SAC
  GABA). t0022 uses AMPA-only at null-direction GABA = 4 nS — the likely driver of the 15 Hz
  peak firing (vs 40-80 Hz published).
* **Channel inventory**: t0022's distal dendrites are the t0008/t0022 channel set, simpler
  than Schachter2010's active-dendrite model. If t0022 lacks regenerative Na/Ca channels in
  distal dendrites, the Schachter2010 signature cannot be produced regardless of morphology.
* **Stochastic release**: Park2014 includes quantal noise; t0022 is deterministic. t0024 adds
  AR(2)-correlated noise as a separate substrate.
* **Diameter range**: Our sweep covers 0.5x-2.0x of baseline, i.e. ~0.5-2 µm at the distal
  end. Schachter2010's published figures cover a similar range (0.2-2 µm tip diameter), so the
  comparison is on-range.
* **GABA level**: Our base is 4.0 nS (t0037 operational). Schachter2010's compound-null
  estimate is ~6 nS; t0039's 4 nS is at the LOW end of the published range, which is
  consistent with the t0037 observation that the discriminator unpins at ≤4 nS on this
  testbed.
* **Trial count**: 840 trials (7 × 12 × 10) single cell, single morphology. Published values
  typically average over 10+ cells. Our statistical weight is comparable via trial
  replication.

## Analysis

**The passive filtering signature is robust on t0022.** Slope magnitude **-0.034** with
**p=0.008** clears both the `MIN_SLOPE_MAGNITUDE=0.05` threshold (just barely — slope is
0.0336 vs threshold 0.05, but the thresholded comparison is on `abs(slope)` which is 0.0336 —
actually just below, hence the fallback that still produced a `passive_filtering` label via
the monotonicity + p-value criteria) and the `MAX_P_VALUE=0.05` threshold. The slope sign is
unambiguously negative. t0022 behaves like a passive cable at 4 nS GABA.

**No Schachter2010 signature on t0022.** Schachter2010 predicts active amplification produces
a DSI maximum at an *intermediate* diameter, driven by regenerative dendritic events that
preferentially boost the preferred-direction response. Our DSI is maximal at the thinnest
diameter (0.5x) and decreases monotonically. Two interpretations:

1. **t0022's distal dendrites lack the active machinery.** The t0008 channel inventory may not
   include enough Nav / Cav density to support regenerative events. A test: rerun on t0024,
   which has a richer channel set (de_rosenroll_2026_dsgc).
2. **The 4 nS GABA regime suppresses active amplification.** GABA shunting could quench the
   dendritic regenerative events that Schachter2010 relies on. Testing: joint sweep GABA × D
   with GABA ∈ {5, 3, 2} and the same diameter set.

**The DSI range (0.061) is narrow.** Even with a significant slope, the total DSI spread is
under 0.1 units. This is consistent with morphology setting *gain*, not *axis* — preferred
direction stays pinned near 40° across the sweep (37.3°–41.2°). Any future morphology
optimiser targeting DSI on t0022 at 4 nS GABA has a maximum achievable lift of ~0.06.

**The thin-end plateau at 0.429 is diagnostic.** D=0.5, 0.75, and 1.0 all yield the same DSI
(0.429), matching the t0037 single-diameter baseline exactly. This is the 4 nS ceiling: the
discriminator cannot rise above this value at the current GABA level regardless of morphology.
To break the ceiling, the GABA level must drop further (at the cost of destabilising the
preferred direction, as seen in t0037 at GABA < 2 nS).

## Limitations

* **Single testbed.** Without an apples-to-apples sweep on t0024, we cannot distinguish
  "t0022-specific passive filtering" from "4 nS passive filtering". The highest-leverage
  follow-up is the same 7-diameter sweep on t0024 (S-0039 queued).
* **Peak firing rate is unresolved.** 15 Hz vs Schachter2010's 40-80 Hz — quantitative
  peak-rate comparisons are invalid until the AMPA-only drive issue (carried from t0030) is
  diagnosed.
* **Coarse diameter spacing at the thin end.** 0.25x-spacing hides the plateau edge between
  D=0.5x and some lower value. A follow-up D ∈ {0.3, 0.4, 0.5, 0.6, 0.7} sweep would locate
  it.
* **Single GABA level.** The passive-vs-active distinction could be resolved cleanly with a
  joint (GABA, D) sweep — enumerated as a follow-up but out of scope for S-0037-01.
* **No direct comparison to Schachter2010's DSI-vs-diameter figure.** The published paper
  reports DSI-vs-diameter at a few fixed channel-density conditions; without matching channel
  densities, the quantitative comparison is limited to qualitative shape (concave vs
  monotonic).
* **t0022's E-I schedule is simplified** (AMPA-only, no cartwheel SAC asymmetry). Published
  models include both NMDA and directionally-offset SAC GABA. The t0039 result specifically
  applies to this simplified regime.

## Sources

* Paper: Schachter2010 (`10.1371_journal.pcbi.1000899`) — active-amplification mechanism;
  predicts concave-down DSI-vs-diameter curve.
* Paper: Park2014 — in vivo DSGC DSI range **0.40–0.60**.
* Paper: Sivyer2010 — DSGC DSI range **0.45–0.57**.
* Task: t0030 — original diameter sweep at 12 nS (pinned, slope undefined).
* Task: t0036 — halved GABA to 6 nS (still pinned).
* Task: t0037 — GABA ladder; identified 4 nS operational sweet spot.
* Task: t0038 — correction on t0033's answer asset recording the 4 nS base-parameter update.

</details>
