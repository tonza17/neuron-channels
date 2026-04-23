# ✅ Rerun distal-diameter sweep on t0022 with halved null-GABA

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0036_rerun_t0030_halved_null_gaba` |
| **Status** | ✅ completed |
| **Started** | 2026-04-23T20:56:59Z |
| **Completed** | 2026-04-23T22:40:00Z |
| **Duration** | 1h 43m |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source suggestion** | `S-0030-01` |
| **Task types** | `experiment-run` |
| **Step progress** | 11/15 |
| **Task folder** | [`t0036_rerun_t0030_halved_null_gaba/`](../../../tasks/t0036_rerun_t0030_halved_null_gaba/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0036_rerun_t0030_halved_null_gaba/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0036_rerun_t0030_halved_null_gaba/task_description.md)*

# Rerun Distal-Diameter Sweep on t0022 with Halved Null-GABA

## Motivation

t0030 (distal-diameter sweep on t0022) produced a **null result** for the Schachter2010 vs
passive-filtering discriminator because **primary DSI was pinned at 1.000 across every
diameter multiplier**. Null-direction firing was exactly 0 Hz under the t0022 E-I schedule at
every diameter, so the peak-minus-null DSI metric had no dynamic range to express either
predicted mechanism slope.

t0030's compare_literature traced the ceiling to `GABA_CONDUCTANCE_NULL_NS = 12 nS` delivered
10 ms before AMPA on null trials — approximately **2× the ~6 nS compound null inhibition
reported by Schachter2010**. Lowering the null-GABA conductance to 6 nS (halved) should leave
enough residual excitation for occasional null-direction spikes while preserving preferred-
direction firing, restoring a measurable primary-DSI signal.

Source suggestion **S-0030-01** (high priority).

## Scope

1. Use the **t0022 DSGC testbed** as-is (channel set, morphology, AIS partition, 12-direction
   protocol, 10 trials per angle) — EXCEPT: set `GABA_CONDUCTANCE_NULL_NS = 6.0 nS` (half of
   the default 12 nS). Preferred-direction GABA stays at its default.
2. Identify distal dendritic sections via t0030's selection rule (HOC leaves on `h.RGC.ON`,
   branch order ≥ 3). COPY the helper into this task's `code/`; no cross-task imports.
3. Sweep 7 distal-diameter multipliers (0.5×, 0.75×, 1.0×, 1.25×, 1.5×, 1.75×, 2.0×) uniformly
   on all distal branches. Same set as t0030.
4. 12-direction moving-bar tuning × 10 trials per angle per diameter = **840 trials total**.
5. Compute **primary DSI (peak-minus-null)** as the operative metric. Unlike t0030, this is
   expected to vary because null-direction firing should now be non-zero. Also compute
   vector-sum DSI and standard secondary metrics.
6. Plot primary DSI vs diameter and classify slope sign:
   - Positive slope → **Schachter2010 active-dendrite amplification** supported
   - Negative slope → **Passive-filtering** supported
   - Flat → mechanism remains ambiguous; diagnose cause (inspect null-firing rate change)

## Approach

* **Local CPU only.** No remote compute, no paid APIs, $0.
* Copy the t0030 code/ workflow verbatim: `paths.py`, `constants.py`, `diameter_override.py`
  (with `identify_distal_sections`), `preflight_distal.py`, `trial_runner_diameter.py`,
  `run_sweep.py`, `analyse_sweep.py`, `classify_slope.py`, `plot_sweep.py`.
* Override the `GABA_CONDUCTANCE_NULL_NS` constant at import time (or expose a CLI override).
  Keep preferred-direction GABA at default.
* Save per-sweep-point tidy CSV incrementally (crash recovery via `fh.flush()`).
* Render DSI-vs-diameter curve, vector-sum DSI curve, polar overlay, null-Hz-vs-diameter curve
  (new diagnostic to confirm the fix is working).

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary including null-Hz-vs-diameter
  baseline (should be non-zero), primary DSI dynamic range, slope classification, mechanism
  attribution.
* `results/results_detailed.md` — per-direction breakdown, slope classification, comparison to
  t0030's pinned-1.000 baseline, discussion of which mechanism the schedule-fixed data
  favours.
* `results/images/dsi_vs_diameter.png`, `vector_sum_dsi_vs_diameter.png`, `polar_overlay.png`,
  `null_hz_vs_diameter.png` (new: confirms the fix desaturates null firing),
  `peak_hz_vs_diameter.png`.
* `results/metrics.json` — DSI primary, vector-sum, peak Hz, null Hz per diameter.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* Local CPU only. Expected runtime: **~2 hours** (extrapolated from t0030's ~115 min on same
  testbed; non-zero null firing doesn't change per-trial wall time meaningfully).
* $0 external cost.

## Measurement

* **Primary metric**: **primary DSI (peak-minus-null)** per diameter — expected to vary now
  that null firing is unpinned.
* **Critical diagnostic**: **null-direction firing rate per diameter** — must be non-zero to
  confirm the GABA change had the intended effect.
* **Secondary**: vector-sum DSI, peak Hz, HWHM, reliability, preferred-direction firing,
  per-direction spike counts, distal peak mV.

## Key Questions

1. Does null-direction firing become non-zero with GABA reduced to 6 nS? (Pre-condition for
   everything else. If it's still 0 Hz, the fix failed; consider a smaller reduction.)
2. With null firing unpinned, what is the primary DSI-vs-diameter slope sign?
3. Does the slope match Schachter2010 (positive), passive filtering (negative), or neither?
4. How does the halved-GABA result on t0022 compare to t0035 (same diameter sweep on t0024)?
   Both should now have unpinned primary DSI — do they agree on the diameter axis being a weak
   discriminator?

## Dependencies

* **t0022_modify_dsgc_channel_testbed** (completed) — provides the DSGC testbed architecture
  and the default `GABA_CONDUCTANCE_NULL_NS = 12 nS` to be overridden.
* **t0030_distal_dendrite_diameter_sweep_dsgc** (completed) — provides the workflow template,
  the `identify_distal_sections` helper (to be copied), and the null-result baseline for
  before/after comparison.

## Scientific Context

Source suggestion **S-0030-01** (high priority). Complementary to S-0029-04 (null-GABA sweep
at fixed length) and S-0029-01 (Poisson + length sweep) — this specifically targets the
diameter axis with a fixed halved-GABA schedule change. Also parallels t0035 (diameter sweep
on t0024) which found flat DSI, allowing a cross-testbed comparison under unpinned primary-DSI
conditions.

## Execution Notes

* Follow standard `/execute-task` flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 + t0030 already cover the mechanism
  predictions).
* Include `research-code` — inherit t0030 workflow + t0022 driver.
* Skip `setup-machines` / `teardown` (local CPU only).
* Include `creative-thinking` — if null-Hz rescue works, interpret the slope in the context of
  t0035 (diameter on t0024) result.
* Include `compare-literature` — compare DSI-vs-diameter slope to Schachter2010 /
  passive-filtering predictions AND to t0030 null baseline AND to t0035 flat-on-t0024 result.

</details>

## Metrics

### distal diam x 0.50

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **59.2308** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal diam x 0.75

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **66.2097** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.999864** |

### distal diam x 1.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **59.2308** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal diam x 1.25

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **119.6154** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal diam x 1.50

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **112.2727** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.999963** |

### distal diam x 1.75

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **110.7576** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.999955** |

### distal diam x 2.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **105.2083** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

## Suggestions Generated

<details>
<summary><strong>Sequential further null-GABA reductions (4, 2, 1 nS) on the t0022
distal-diameter sweep</strong> (S-0036-01)</summary>

**Kind**: experiment | **Priority**: high

t0036 halved GABA_CONDUCTANCE_NULL_NS from 12 nS to 6 nS and null firing stayed pinned at 0.0
Hz at every diameter multiplier, falsifying the Schachter2010 ~6 nS compound-inhibition
rescue. The classifier auto-recommendation was 'reduce null-GABA further to ~4 nS'. Rerun the
t0036 diameter sweep at 4 nS, 2 nS, and 1 nS (stop as soon as mean null firing exceeds 0.1 Hz
at 1.0x); each rerun is ~30 min CPU so worst case ~1.5 h. If null firing unpins at 4 or 2 nS,
primary DSI becomes measurable and the Schachter2010-vs-passive slope discriminator is rescued
on deterministic t0022. If it stays 0 Hz down to 1 nS, the testbed is structurally
incompatible with primary DSI on morphology axes and the project must adopt Poisson rescue
(S-0030-02) or migrate the optimiser substrate to t0024 (S-0034-07). Distinct from S-0029-04
(3-12 nS at fixed length on t0029 code) - this extends below the 3 nS floor on the t0036
diameter-sweep code path. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>GABA-to-AMPA timing offset sweep on t0022 diameter testbed to test
timing-dominates-conductance hypothesis</strong> (S-0036-02)</summary>

**Kind**: experiment | **Priority**: medium

t0036's creative_thinking cited 'timing dominates conductance' as the second-leading
explanation for why halving null-GABA from 12 nS to 6 nS did not unpin null firing: the t0022
schedule delivers GABA 10 ms BEFORE AMPA on null trials, and the integrated kinetic profile
(not the peak) may clamp the distal membrane below Nav threshold for the whole AMPA window.
Sweep the GABA-leads-AMPA offset across {10 ms (default), 5 ms, 0 ms, -5 ms (AMPA leads GABA)}
at two fixed GABA conductances (12 nS baseline and 6 nS) at diameter 1.0x only (12 angles x 10
trials x 4 offsets x 2 GABA = 960 trials, ~35 min CPU). Primary outcome: find the offset at
which null firing first exceeds 0.1 Hz, isolating timing as an independent rescue axis
orthogonal to S-0036-01's conductance axis. Distinct from S-0030-02 (Poisson) and S-0036-01
(conductance) - this targets the GABA-AMPA offset specifically. Recommended task types:
experiment-run.

</details>

<details>
<summary><strong>Distal voltage-trace capture at null direction on t0022 to confirm
sub-threshold-clamp hypothesis</strong> (S-0036-03)</summary>

**Kind**: experiment | **Priority**: medium

t0036 recorded per-trial scalar distal peak_mv only (~-55 mV at null direction) but did not
export the full distal membrane time course. Creative_thinking hypothesis 4 (distal Nav
channels sub-threshold at null regardless of diameter amplification) and limitation bullet 5
both flag missing voltage traces as blocking direct mechanistic confirmation. Extend the t0022
trial driver to save a 200-sample time-course of the most-distal compartment voltage (one
trial per direction at diameter 1.0x, GABA_NULL = 6 nS and 12 nS, 24 traces total, ~5 min
CPU). Plot v_distal(t) across directions and annotate Nav activation threshold (~-55 mV) and
AMPA/GABA event onsets. Expected: at null the distal membrane never crosses Nav threshold for
the whole AMPA window on either 6 nS or 12 nS; at preferred it crosses and fires. Closes
creative_thinking hypothesis 4 and confirms the sub-threshold-clamp failure mode. Recommended
task types: experiment-run, data-analysis.

</details>

<details>
<summary><strong>Extract the t0022 GABA-override monkey-patch into a reusable
library asset for downstream tasks</strong> (S-0036-04)</summary>

**Kind**: library | **Priority**: medium

t0036 introduced code/gaba_override.py which monkey-patches
_t0022_constants.GABA_CONDUCTANCE_NULL_NS at import time and re-binds the local name inside
trial_runner_diameter.py so the schedule_ei_onsets ratio is computed against the overridden
value. This pattern is immediately needed for S-0036-01 (further null-GABA reductions) and
S-0036-02 (GABA-AMPA timing offset). Rather than each task reimplementing the monkey-patch,
lift it into a library asset (working name: dsgc_t0022_schedule_overrides) exposing a typed
context-manager or setup function accepting gaba_null_ns, gaba_preferred_ns,
gaba_to_ampa_lead_ms, returning a provenance dict logged at task start. Ships a smoke test
asserting the override survived a fresh import and that the null/preferred ratio matches the
requested value. Distinct from S-0033-06 (DSI objective evaluator) which wraps the scoring
side - this wraps the schedule-parameter side. Recommended task types: write-library.

</details>

## Research

* [`creative_thinking.md`](../../../tasks/t0036_rerun_t0030_halved_null_gaba/research/creative_thinking.md)
* [`research_code.md`](../../../tasks/t0036_rerun_t0030_halved_null_gaba/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0036_rerun_t0030_halved_null_gaba/results/results_summary.md)*

--- spec_version: "2" task_id: "t0036_rerun_t0030_halved_null_gaba" date_completed:
"2026-04-23" status: "complete" ---
# Results Summary: Rerun Distal-Diameter Sweep on t0022 with Halved Null-GABA

## Summary

Reran the t0030 distal-diameter sweep on t0022 with `GABA_CONDUCTANCE_NULL_NS = 6.0 nS`
(halved from 12 nS, matching Schachter2010's compound null inhibition). **The halving was
INSUFFICIENT to unpin null firing**: mean null-direction firing remained exactly **0.0 Hz at
every diameter multiplier**, primary DSI stayed pinned at 1.000, and the classification label
is **`flat_partial`** (pre-condition gate failed). Vector-sum DSI range 0.579-0.590 (range
0.011, p=0.019 — statistically significant but practically negligible). The GABA- reduction
rescue hypothesis from S-0030-01 is falsified at 6 nS; follow-up queued to try further
reductions (4/2/1 nS) or switch to Poisson-noise rescue.

## Metrics

* **Null-direction firing (critical diagnostic)**: **0.00 Hz** at every diameter — pre-
  condition failed (threshold 0.1 Hz). Same as t0030 baseline.
* **Primary DSI (peak-minus-null)**: pinned at **1.000** across all 7 diameters.
* **Vector-sum DSI range**: **0.579** (0.50×) to **0.590** (1.75×) — 0.011 absolute range,
  slope 0.0049 per log2(multiplier), p=0.019.
* **Preferred-direction peak firing rate**: **15.0 Hz** at 0.50-1.00×, **14.0 Hz** at
  1.25-1.50×, **13.0 Hz** at 1.75-2.00× — same monotone decline with thickening as t0030.
* **HWHM**: narrower at thin diameters (59-66°), broader at thick (105-120°).
* **Slope classification**: `flat_partial` (mechanism ambiguous; pre-condition failed).
* **Total trials executed**: **840** (7 diameters × 12 directions × 10 trials).
* **Sweep wall time**: approximately **30 minutes** on local Windows CPU — faster than t0030's
  115 min because the `trial_runner` path was optimised during t0034/t0035 rewrites.

## Verification

* `verify_task_file.py` — target 0 errors.
* `verify_task_dependencies.py` — PASSED on step 2 (t0022 and t0030 completed).
* `verify_research_code.py` — PASSED on step 6 (0 errors, 0 warnings).
* `verify_plan.py` — PASSED on step 7 (0 errors, 0 warnings).
* `verify_task_metrics.py` — target 0 errors.
* `verify_task_results.py` — target 0 errors.
* `verify_task_folder.py` — target 0 errors.
* `verify_logs.py` — target 0 errors.
* `ruff check --fix`, `ruff format`, `mypy -p tasks.t0036_rerun_t0030_halved_null_gaba.code` —
  all clean (11 files).
* **Pre-condition gate**: **FAILED** (null_hz at 1.0× = 0.0; threshold 0.1). Classification
  label carries `_partial` suffix; auto-recommendation printed.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0036_rerun_t0030_halved_null_gaba/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0036_rerun_t0030_halved_null_gaba" date_completed:
"2026-04-23" status: "complete" ---
# Results Detailed: Rerun Distal-Diameter Sweep on t0022 with Halved Null-GABA

## Summary

Reran the t0030 distal-diameter sweep on t0022 with `GABA_CONDUCTANCE_NULL_NS = 6.0 nS`
(halved from 12 nS, targeting Schachter2010's ~6 nS compound null inhibition). The rescue
hypothesis (that halving would unpin null firing and restore primary DSI dynamic range) **was
falsified**: null-direction firing remained exactly 0.0 Hz at every diameter, primary DSI
stayed pinned at 1.000, and the classifier emitted the `flat_partial` label with an
auto-recommendation to further reduce the null-GABA conductance. Vector-sum DSI moved by only
0.011 absolute, with a statistically significant but practically negligible slope. The t0022
deterministic schedule appears to be structurally incompatible with peak-minus- null DSI on
morphology axes — any conductance-only fix is likely insufficient unless paired with timing
changes or a stochastic rescue (Poisson background).

## Methodology

* **Machine**: Windows 11, local CPU only. NEURON 8.2.7 + NetPyNE 1.1.1 (from t0007 install).
* **Testbed**: `modeldb_189347_dsgc_dendritic` library (t0022 port) with
  `GABA_CONDUCTANCE_NULL_NS = 6.0 nS` overridden at module load via `gaba_override.py`. All
  other t0022 parameters unchanged.
* **Distal selection**: t0030's `identify_distal_sections` helper (HOC leaves on `h.RGC.ON`),
  copied verbatim. 177 distal sections identified.
* **Protocol**: 7 diameter multipliers × 12 angles × 10 trials = 840 trials.
* **Scoring**: primary DSI (peak-minus-null via t0012 `compute_dsi`), vector-sum DSI, peak Hz,
  **null Hz (new diagnostic — pre-condition gate)**, HWHM, reliability.
* **Wall time**: approximately 30 minutes for 840 trials.
* **Timestamps**: task started 2026-04-23T20:58:12Z; sweep completed ~2026-04-23T22:18Z.

### Per-Diameter Metrics Table

| D_mul | peak_Hz | null_Hz | DSI (primary) | DSI (vector-sum) | HWHM (°) | Reliability | Pref (°) | peak_mV |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.50 | 15.00 | **0.00** | 1.000 | 0.579 | 59.2 | 1.000 | 53.0 | +5.4 |
| 0.75 | 15.00 | **0.00** | 1.000 | 0.580 | 66.2 | 1.000 | 52.5 | +5.2 |
| 1.00 | 15.00 | **0.00** | 1.000 | 0.583 | 59.2 | 1.000 | 52.6 | +5.2 |
| 1.25 | 14.00 | **0.00** | 1.000 | 0.583 | 119.6 | 1.000 | 50.8 | +5.0 |
| 1.50 | 14.00 | **0.00** | 1.000 | 0.589 | 112.3 | 1.000 | 53.6 | +5.1 |
| 1.75 | 13.00 | **0.00** | 1.000 | 0.590 | 110.8 | 1.000 | 55.1 | +4.8 |
| 2.00 | 13.00 | **0.00** | 1.000 | 0.585 | 105.2 | 1.000 | 56.1 | +4.9 |

Sources: `results/data/metrics_per_diameter.csv`, `results/data/metrics_notes.json`.

### Slope Classification

| Statistic | Value |
| --- | --- |
| Classification label | **flat_partial** (pre-condition failed) |
| Slope (vector-sum DSI per log2(multiplier)) | **0.0049** |
| p-value | **0.019** (statistically significant but practically negligible) |
| DSI range across extremes | 0.006 |
| Used vector-sum fallback? | Yes (primary DSI pinned at 1.000) |
| Pre-condition pass (null_hz ≥ 0.1)? | **FAIL** (null_hz = 0.0 everywhere) |
| Auto-recommendation | "reduce null-GABA further to ~4 nS" |

Source: `results/data/slope_classification.json`, `results/data/curve_shape.json`.

## Analysis

**Contradicted assumption**: the task plan's central hypothesis (S-0030-01) was that the 12 nS
→ 6 nS halving would restore non-zero null firing and unpin primary DSI. The hypothesis was
**falsified**: null firing stayed at exactly 0.0 Hz at every diameter, identical to t0030.
Halving the conductance was insufficient on the t0022 deterministic testbed.

Creative-thinking enumerated 5 candidate explanations:
1. 12 nS was far above threshold (not 2×); even 6 nS clamps null membrane below AP threshold.
2. Timing dominates conductance — the 10 ms pre-AMPA lead matters more than the peak level.
3. Deterministic testbed lacks the stochastic tail that t0024's AR(2) schedule provides.
4. Distal Nav channels are sub-threshold at null direction regardless of amplification.
5. Compound GABA-A/B dynamics not modelled.

Follow-up recommendations: try further reductions (4/2/1 nS) OR adopt Poisson-noise rescue
(S-0030-02, already high priority in backlog) OR accept that t0022 cannot support primary DSI
on morphology axes and use vector-sum DSI objective in the t0033 optimiser.

## Charts

![Primary DSI vs distal-dendrite diameter
multiplier](../../../tasks/t0036_rerun_t0030_halved_null_gaba/results/images/dsi_vs_diameter.png)

Primary DSI pinned at 1.000 across all 7 diameters — identical to t0030 baseline. The GABA
halving produced no measurable change in the primary discriminator.

![Null-direction firing rate vs diameter (critical
diagnostic)](../../../tasks/t0036_rerun_t0030_halved_null_gaba/results/images/null_hz_vs_diameter.png)

**The key chart**: null-direction firing is exactly 0.0 Hz at every diameter. This confirms
the halved GABA (6 nS) is still too strong to allow any null spike escape on this
deterministic schedule — the DSI discriminator has no dynamic range to express Schachter2010
or passive-filtering predictions.

![Vector-sum DSI vs
diameter](../../../tasks/t0036_rerun_t0030_halved_null_gaba/results/images/vector_sum_dsi_vs_diameter.png)

Vector-sum DSI is essentially flat (0.579-0.590, range 0.011). Slope is statistically
significant (p=0.019) but the absolute magnitude is negligible.

![Peak firing rate vs
diameter](../../../tasks/t0036_rerun_t0030_halved_null_gaba/results/images/peak_hz_vs_diameter.png)

Peak firing drops from 15 Hz (thin) to 13 Hz (thick) — same monotone decline as t0030.
Preferred-direction firing is unaffected by the GABA halving (GABA at preferred stayed at its
default).

![12-direction polar overlay across all 7
diameters](../../../tasks/t0036_rerun_t0030_halved_null_gaba/results/images/polar_overlay.png)

All 7 polar curves are near-identical, with preferred peaks around 50-60° and null half- plane
silenced. The GABA halving did not reshape the tuning.

## Verification

* `verify_task_file.py` — target 0 errors.
* `verify_task_dependencies.py` — PASSED on step 2.
* `verify_research_code.py` — PASSED on step 6.
* `verify_plan.py` — PASSED on step 7.
* `verify_task_metrics.py` — target 0 errors.
* `verify_task_results.py` — target 0 errors.
* `verify_task_folder.py` — target 0 errors.
* `verify_logs.py` — target 0 errors.
* `ruff check --fix`, `ruff format`, `mypy -p tasks.t0036_rerun_t0030_halved_null_gaba.code` —
  all clean.
* Pre-merge verificator — target 0 errors before merge.

## Limitations

* **Halving was insufficient**: 6 nS still clamps null firing to 0 Hz. This is the core
  finding, honestly documented.
* **Single GABA value tested**: the rescue might succeed at 4 nS, 2 nS, or 1 nS, or fail at
  all of them. Follow-up task S-0036-01 (sequence of reductions) queued.
* **Timing not varied**: the 10 ms GABA-leads-AMPA interval was kept at its default.
  creative_thinking item #2 flags this as a separate axis worth exploring.
* **Deterministic testbed**: t0022 has no stochastic synaptic source to produce near-
  threshold null spikes even when GABA is weakened. This is a fundamental feature, not a bug.
* **Distal peak_mv at null direction not captured**: would need voltage-trace output to
  confirm creative_thinking hypothesis #4 (distal Nav sub-threshold at null).

## Examples

Ten trial input/output pairs from `results/data/sweep_results.csv`. All use AR(2)-disabled
(deterministic) schedule with GABA_NULL = 6 nS:

### Example 1: D=0.50× preferred (14 spikes)

```text
diameter_multiplier=0.50, trial=0, direction_deg=0
```

```csv
0.50,0,0,14,44.662,14.000000
```

### Example 2: D=0.50× deterministic identical trial

```text
diameter_multiplier=0.50, trial=1, direction_deg=0
```

```csv
0.50,1,0,14,44.707,14.000000
```

All 10 repeats produced 14 spikes (deterministic testbed → zero variance).

### Example 3: D=0.50× null direction (0 spikes — the failure)

```text
diameter_multiplier=0.50, trial=0, direction_deg=180
```

```csv
0.50,0,180,0,-55.7,0.000000
```

Distal peak_mv = -55.7 mV at null, below HHst Nav activation. This is the root cause of the
GABA halving's failure: even with 6 nS, the distal membrane never depolarises enough at null
direction to fire.

### Example 4: D=0.75× preferred (15 spikes — peak rate)

```text
diameter_multiplier=0.75, trial=0, direction_deg=60
```

```csv
0.75,0,60,15,44.621,15.000000
```

### Example 5: D=1.00× baseline preferred

```text
diameter_multiplier=1.00, trial=0, direction_deg=60
```

```csv
1.00,0,60,15,44.609,15.000000
```

### Example 6: D=1.25× null direction

```text
diameter_multiplier=1.25, trial=0, direction_deg=180
```

```csv
1.25,0,180,0,-54.9,0.000000
```

### Example 7: D=1.50× preferred

```text
diameter_multiplier=1.50, trial=0, direction_deg=60
```

```csv
1.50,0,60,14,44.352,14.000000
```

### Example 8: D=1.75× peak rate drop

```text
diameter_multiplier=1.75, trial=0, direction_deg=60
```

```csv
1.75,0,60,13,43.980,13.000000
```

### Example 9: D=2.00× null direction

```text
diameter_multiplier=2.00, trial=0, direction_deg=180
```

```csv
2.00,0,180,0,-55.1,0.000000
```

### Example 10: D=2.00× preferred

```text
diameter_multiplier=2.00, trial=0, direction_deg=60
```

```csv
2.00,0,60,13,43.701,13.000000
```

Takeaway: across every diameter, null-direction firing is exactly 0. Preferred-direction
firing decreases mildly with thickening (15 → 13 Hz). Primary DSI therefore stays at (peak -
0)/(peak + 0) = 1.000 at every diameter, defeating the discriminator.

## Files Created

### Code (11 Python files, lint + mypy clean)

* `code/paths.py`, `code/constants.py`, `code/gaba_override.py` (NEW — monkey-patches t0022
  GABA at import), `code/diameter_override.py`, `code/preflight_distal.py`,
  `code/trial_runner_diameter.py`, `code/run_sweep.py`, `code/analyse_sweep.py`,
  `code/classify_slope.py` (with pre-condition gate), `code/plot_sweep.py` (+ null_hz chart).

### Data

* `results/data/sweep_results.csv` (840 trials + header)
* `results/data/per_diameter/tuning_curve_D{0p50,...,2p00}.csv`
* `results/data/metrics_per_diameter.csv`, `dsi_by_diameter.csv`, `metrics_notes.json`
* `results/data/curve_shape.json`, `results/data/slope_classification.json`
  (precondition_pass=False, mechanism_label=flat_partial)
* `results/metrics.json`

### Charts

* `results/images/dsi_vs_diameter.png`, `vector_sum_dsi_vs_diameter.png`,
  `null_hz_vs_diameter.png` (diagnostic), `peak_hz_vs_diameter.png`, `polar_overlay.png`

### Research

* `research/research_code.md`, `research/creative_thinking.md` (5 alternatives)

### Task artefacts

* `plan/plan.md` (11 sections, 12 REQs)
* `task.json`, `task_description.md`, `step_tracker.json`
* Full step logs under `logs/steps/`

## Task Requirement Coverage

Operative task text from task.json and task_description.md:

```text
Rerun t0030's distal-diameter sweep on t0022 with GABA_CONDUCTANCE_NULL_NS halved from
12 nS to 6 nS to unpin primary DSI from 1.000 and restore the Schachter2010 vs passive-
filtering discriminator.

1. Use t0022 testbed as-is EXCEPT GABA_NULL = 6 nS.
2. Identify distal via t0030's selection rule. COPY helper.
3. Sweep 7 diameter multipliers 0.5×-2.0× uniformly.
4. 12-direction × 10-trial protocol per diameter = 840 trials total.
5. Compute primary DSI (peak-minus-null) as operative metric — EXPECTED TO VARY.
6. Plot DSI vs diameter and classify slope sign (positive=Schachter, negative=passive,
   flat=mechanism ambiguous; diagnose cause).
```

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | t0022 testbed + GABA=6nS override | **Done** | gaba_override.py monkey-patches constants.py:84 at import; banner confirms |
| REQ-2 | Distal selection via h.RGC.ON leaves | **Done** | identify_distal_sections copied from t0030; 177 sections found |
| REQ-3 | Copy helper (no cross-task import) | **Done** | diameter_override.py + distal_selector copied verbatim |
| REQ-4 | 7 diameter multipliers | **Done** | DIAMETER_MULTIPLIERS in constants.py |
| REQ-5 | 12 × 10 protocol | **Done** | 840 rows in sweep_results.csv |
| REQ-6 | AR(2) / stochastic preservation | N/A | t0022 is deterministic; no AR(2) |
| REQ-7 | Secondary metrics | **Done** | metrics_per_diameter.csv has all columns including null_Hz |
| REQ-8 | Slope classification | **Done** | slope_classification.json label=flat_partial |
| REQ-9 | Vector-sum defensive fallback | **Done** | vector_sum_dsi_vs_diameter.png + classifier used fallback |
| REQ-10 | Null-Hz-vs-diameter diagnostic chart | **Done** | null_hz_vs_diameter.png (all values at 0 Hz — the critical finding) |
| REQ-11 | Per-row flush | **Done** | run_sweep.py fh.flush() after every row |
| REQ-12 | **Primary DSI becomes measurable (null firing non-zero)** | **Not done** | **null_hz = 0.0 at every diameter**; primary DSI pinned at 1.000; GABA halving was insufficient. This is the honest, documented result. |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0036_rerun_t0030_halved_null_gaba/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0036_rerun_t0030_halved_null_gaba" date_compared:
"2026-04-22" ---
# Comparison with Published Results

## Summary

This task halved the null-direction GABA conductance from **12 nS** to **6 nS** — matching the
compound null inhibition reported by Schachter2010 [Schachter2010, Architecture/Methods p. 3]
— with the explicit goal of unpinning null-direction firing on the t0022 testbed and restoring
a measurable primary-DSI dynamic range across the 0.5×-2.0× distal-diameter sweep. **The
Schachter2010-derived rescue hypothesis is falsified**: mean null-direction firing stayed at
exactly **0.00 Hz** at every diameter multiplier, primary DSI remained pinned at **1.000**,
and the classifier emitted the `flat_partial` label with a pre-condition-failure flag. The
fallback vector-sum DSI moved by only **0.011** absolute (range 0.579-0.590, slope
**+0.0049**, p=**0.019**) — statistically distinguishable from zero but three orders of
magnitude below the ~**0.6** DSI movement Schachter2010 reports between PSP and spike regimes.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Schachter2010 compound null inhibition [Schachter2010, Architecture/Methods p. 3] | null_GABA (nS) | 6.0 | 6.0 | +0.0 | GABA level matched exactly by t0036 override |
| Schachter2010 rescue hypothesis (S-0030-01) [Schachter2010, Architecture/Methods p. 3; t0030 compare_literature.md Analysis] | mean null firing at 1.0× (Hz) | >= 0.1 | 0.00 | **-0.1** | Pre-condition failed; halving did not unpin null firing on deterministic t0022 |
| Schachter2010 spike-DSI ceiling [Schachter2010, Abstract; Overview p. 1] | spike DSI | 0.80 | 1.000 | **+0.200** | Our testbed remains saturated above Schachter2010's spike-DSI value even after GABA halving |
| Schachter2010 PSP-to-spike amplification [Schachter2010, Overview p. 1] | DSI change (PSP -> spike) | ~0.60 | 0.011 | **-0.589** | Vector-sum range across 4x diameter is three orders of magnitude below the dendritic-Nav amplification step |
| Schachter2010 active-amplification prediction [Schachter2010, Overview p. 1] | DSI vs diameter slope sign | positive | +0.0049 | n/a | Sign matches Schachter2010 but magnitude negligible; primary DSI discriminator saturated at 1.000 |
| Passive filtering (cable theory via t0027 synthesis) [Wu2023, abstract via t0027 full_answer.md:108-113] | DSI vs diameter slope sign | negative | +0.0049 | n/a | Sign is opposite Wu2023's Z~1/d^1.5 prediction; passive filtering also not supported |
| Sivyer2013 rabbit DSGC control DSI [Sivyer2013, Fig. 2-3 text via t0002 summary] | spike DSI | ~1.0 | 1.000 | **+0.000** | Qualitative match but uninformative because ceiling is schedule-driven, not biophysical |

### Prior Task Comparison

The t0036 task plan cites two prior tasks as direct comparators: **t0030** (same diameter
sweep on t0022 at 12 nS GABA — the "before schedule fix" baseline) and **t0035** (same
diameter sweep on the t0024 AR(2) testbed). The t0034 length sweep on t0024 provides a second
cross-testbed reference. All four rows below compare t0036's halved-GABA result against those
prior measurements.

| Prior Task / Source | Metric | Prior Value | t0036 Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0030 (same sweep, GABA=12 nS) | mean null firing (Hz) | 0.00 | 0.00 | **+0.00** | Halving GABA produced zero change — the core negative finding |
| t0030 (same sweep, GABA=12 nS) | primary DSI range across extremes | 0.000 | 0.000 | **+0.000** | Pinned at 1.000 in both cases; GABA halving did not unpin |
| t0030 (same sweep, GABA=12 nS) | vector-sum DSI range across extremes | 0.012 | 0.011 | **-0.001** | Marginal contraction of the fallback range despite halved GABA |
| t0030 (same sweep, GABA=12 nS) | vector-sum DSI slope (per log2 mult) | +0.0083 | +0.0049 | **-0.0034** | Slope halved and now statistically significant (p=0.019 vs t0030 p=0.177) but absolute range below practical threshold |
| t0035 (diameter sweep on t0024 AR(2)) | mean null firing (Hz) | 0.50-0.80 | 0.00 | **-0.50 to -0.80** | AR(2) stochasticity keeps null firing non-zero; halved-GABA on deterministic t0022 does not |
| t0035 (diameter sweep on t0024 AR(2)) | primary DSI range | 0.680-0.808 | 1.000 (pinned) | n/a | t0024 preserves a measurable primary DSI dynamic range that t0022 cannot produce, even with halved GABA |
| t0035 (diameter sweep on t0024 AR(2)) | primary DSI slope (per log2 mult) | 0.0041 (p=0.88) | 0.000 (pinned) | n/a | Both testbeds produce flat diameter-axis slopes; only t0035 produces a measurable primary signal |
| t0034 (length sweep on t0024 AR(2)) | primary DSI slope | -0.1259 (p=0.038) | n/a | n/a | Length modulates primary DSI on t0024; diameter does not; t0022 cannot even produce the measurement |

The lineage-internal finding is decisive: **the rescue hypothesis is falsified at 6 nS on the
t0022 deterministic schedule**, and the only testbed in the project where primary DSI remains
measurable on any morphology axis is **t0024 with AR(2)** (t0034 length sweep, t0035 diameter
sweep). Halving the conductance alone does not substitute for stochastic release.

## Methodology Differences

* **Deterministic t0022 schedule vs Schachter2010 stochastic drive.** The t0022 testbed
  delivers one AMPA and one GABA event per dendrite per trial at seeded, fixed onset times,
  with GABA leading AMPA by 10 ms on null trials. Schachter2010 uses a full drifting-bar
  simulation with SAC-derived presynaptic DS templates and Poisson-like stochastic release
  [Schachter2010, Architecture/Methods p. 3]; their non-zero null spike rate emerges from the
  stochastic release tail, not from the peak GABA conductance alone. Halving the peak
  conductance without adding stochasticity does not reproduce the near-threshold spike escape
  Schachter2010's regime requires.

* **Timing lead preserved at 10 ms.** The t0022 driver keeps GABA leading AMPA by 10 ms at the
  null direction. Schachter2010 reports per-input spatially offset inhibition within ~20 um of
  each excitatory input [Schachter2010, Architecture/Methods p. 3]; the integrated kinetic
  profile, not the peak, is the operative variable. The t0036 intervention scaled peak only;
  the timing lead remained at the t0022 default.

* **Channel substrate is HHst-lumped, not Nav1.6 + Kv1/Kv3 + Ca.** Schachter2010 uses a fast
  Nav1.6-like sodium channel plus delayed rectifier Kv, A-type Kv4, Ca, and Ca-activated K
  currents [Schachter2010, Architecture/Methods p. 3]. The t0022 morphology inherits the
  Poleg-Polsky 2026 HHst Na/K lumped pair; scaling `seg.diam` rescales total Nav current with
  surface area but does not reproduce the persistent Nav1.6 current Schachter2010 identifies
  as the amplifier.

* **No AIS.** The t0022 channel partition declares AIS_PROXIMAL, AIS_DISTAL, and THIN_AXON
  section lists that are empty on this morphology. Schachter2010's model includes a high-Nav
  AIS that participates in the distal-to-soma amplification cascade.

* **Uniform diameter multiplier, no tapering.** Our 0.5×-2.0× sweep applies one multiplier to
  all 177 identified distal leaves. Schachter2010's 150-200 MOhm proximal -> >1 GOhm distal
  impedance gradient arises from tapered, non-uniform diameters along the arbor
  [Schachter2010, Architecture/Methods p. 3]; a uniform-multiplier sweep cannot probe that
  regime.

* **DSI definition is identical but input distribution is not.** Both studies compute `DSI =
  (R_pref - R_null) / (R_pref + R_null)` on 12-direction spike counts. On the t0022 testbed
  `R_null = 0` at every trial (deterministic + 6 nS GABA still sufficient to clamp),
  collapsing the ratio to 1.000 before biophysics can modulate it. Vector-sum DSI
  (Mazurek/Kagan 2020 formulation) retains weak sensitivity and is what the slope classifier
  used in fallback mode.

## Analysis

**The Schachter2010 conductance-matching hypothesis is falsified on the t0022 deterministic
schedule.** The plan's central prediction — that moving GABA from 12 nS (roughly 2×
Schachter2010) to 6 nS (matching Schachter2010's compound null inhibition) would restore
non-zero null firing — was tested cleanly and failed. Mean null-direction firing stayed at
exactly **0.00 Hz** at every diameter, primary DSI stayed pinned at **1.000**, and the
pre-condition gate built into the classifier flagged the sweep as `flat_partial`. This is a
stronger negative finding than t0030 provided, because t0030 could be explained by "GABA is
too strong"; t0036 rules out that explanation at the Schachter2010 level. The failure
therefore implicates either **timing dominance** (the 10 ms pre-AMPA GABA lead matters more
than the peak conductance) or **the absence of stochastic release** (deterministic drive
cannot produce the near-threshold spike tail Schachter2010's regime depends on) as the true
rate-limiter.

**Vector-sum DSI slope acquired statistical significance but lost magnitude.** Compared to
t0030, the halved-GABA sweep produced a vector-sum DSI slope of **+0.0049** per
log2(multiplier) with p=**0.019** — below the 0.05 threshold, unlike t0030's p=**0.177**. But
the absolute DSI range across the sweep contracted from **0.012** (t0030) to **0.011**
(t0036), and the slope magnitude halved. This combination (more significant slope, smaller
range) is the statistical fingerprint of a tighter null distribution rather than a genuine
mechanism signal — halving GABA reduced trial-to-trial noise-equivalent fluctuations in the
vector sum without introducing any null-direction firing. The sign still matches
Schachter2010's positive prediction but the magnitude is three orders of magnitude below
Schachter2010's PSP-to-spike amplification of ~0.6 DSI units [Schachter2010, Overview p. 1].

**Cross-testbed comparison strengthens the stochasticity attribution.** t0035 (the matched
diameter sweep on t0024 with AR(2) release) produced a flat DSI-vs-diameter slope
(**+0.0041**, p=**0.88**) but with a **measurable primary DSI dynamic range of 0.128**
(0.680-0.808), while t0036's primary DSI range remained **0.000**. Both testbeds agree that
the **diameter axis is a weak discriminator** for either mechanism; they disagree on whether a
primary-DSI measurement is even recoverable. The only testbed-axis combination in the project
where primary DSI varies meaningfully is **t0024 + length** (t0034, slope **-0.1259**,
p=**0.038**) — and that signal is cable-filtering-shaped, not Schachter-amplification-shaped.
The pattern across t0030/t0034/t0035/t0036 is consistent: Schachter2010's active-amplification
prediction is not observable on any of these testbeds, and the one testbed where the
discriminator works at all (t0024 length) leans toward passive filtering.

**Implications for the t0033 joint morphology-channel optimiser.** Three options follow from
this result. (1) **Abandon t0022 for primary-DSI objectives.** The deterministic testbed
cannot support the peak-minus-null metric on any morphology axis, even at
Schachter2010-matched GABA — the optimiser should default to t0024 with AR(2) for any task
whose objective is primary DSI. (2) **Use vector-sum DSI if t0022 is required.** The fallback
retains ~0.01 absolute sensitivity, enough to register the peak-firing-rate trend already
visible in t0030 and t0036 but not to discriminate Schachter2010 from passive filtering. (3)
**Adopt a stochasticity or timing intervention.** Poisson background release (S-0030-02) or
reducing the 10 ms GABA pre-AMPA lead would plausibly restore the null tail, but neither has
been tested and both constitute schedule mutations beyond the single-knob parameter space the
current optimiser is designed for. The clean recommendation is (1): **the t0033 optimiser
should prefer t0024 + primary DSI, or t0022 + vector-sum DSI, and should not rely on the t0022
+ primary DSI combination.**

## Limitations

* **Single GABA value tested.** t0036 tested exactly one intermediate point (6 nS). It is
  possible — though not predicted by creative_thinking — that further reductions to 4, 2, or 1
  nS would unpin null firing. Follow-up suggestion S-0036-01 is queued to sweep this axis.

* **Timing axis unexplored.** The 10 ms GABA-leads-AMPA interval was kept at its t0022
  default. Creative_thinking hypothesis #2 identifies timing as a plausible dominant variable;
  this task did not vary it.

* **Schachter2010 spike-DSI ceiling comparison is confounded by schedule.** Our DSI=1.000 does
  not quantitatively exceed Schachter2010's DSI=0.80 because it comes from a schedule-clamped
  null denominator, not from a stronger active-amplification mechanism. The +0.200 delta in
  the comparison table is a methodological artefact, not a biological finding.

* **Schachter2010 PSP-DSI axis not measured.** The t0022 driver emits spike-count tuning only;
  the PSP-DSI axis (~0.20 in Schachter2010) that would isolate the
  dendritic-spike-amplification step is not produced and cannot be compared.

* **Distal voltage traces not captured.** The trial runner records `peak_mv` per trial but not
  the full voltage time course at null direction. Creative_thinking hypothesis #4 (distal Nav
  sub-threshold at null) cannot be confirmed without trace data.

* **Only one paper's quantitative null-GABA estimate exists in the corpus.** Wu2023's passive
  filtering prediction is derived from cable theory (`Z ~ 1/d^1.5`) via the t0027 synthesis
  rather than from a direct DSI-vs-diameter sweep. No paper in the t0036 research corpus
  reports a GABA-reduction rescue of primary DSI on a deterministic DSGC simulation, so the
  negative result cannot be cross-validated against a direct published precedent.

</details>
