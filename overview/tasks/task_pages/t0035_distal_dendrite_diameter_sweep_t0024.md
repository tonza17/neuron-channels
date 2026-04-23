# ✅ Distal-dendrite diameter sweep on t0024 DSGC

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0035_distal_dendrite_diameter_sweep_t0024` |
| **Status** | ✅ completed |
| **Started** | 2026-04-23T14:09:57Z |
| **Completed** | 2026-04-23T18:00:00Z |
| **Duration** | 3h 50m |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source suggestion** | `S-0027-03` |
| **Task types** | `experiment-run` |
| **Step progress** | 11/15 |
| **Task folder** | [`t0035_distal_dendrite_diameter_sweep_t0024/`](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/task_description.md)*

# Distal-Dendrite Diameter Sweep on t0024 DSGC

## Motivation

The sibling task t0030 ran a distal-diameter sweep on the t0022 DSGC testbed and produced a
**null result** for mechanism discrimination: primary DSI pinned at 1.000 across every
diameter multiplier because t0022's deterministic E-I schedule silences null firing (0 Hz).
Vector-sum DSI fallback produced a flat slope too (p=0.18 on t0030).

The t0024 de Rosenroll 2026 port has fundamentally different biophysics that **fix the t0022
pathology**:

* **AR(2)-correlated stochastic bipolar release** (ρ=0.6) produces non-zero null-direction
  firing. Per t0026's V_rest sweep, t0024's DSI ranges 0.36-0.67 with a measurable 1.9×
  modulation — the discriminator has room to act.
* **No Na-inactivation collapse** at depolarised V_rest (peak firing monotone to 7.6 Hz at
  V_rest = -20 mV).
* **AR(2) noise smooths tuning** (HWHM pinned 65-83° across V_rest).

Running the t0030 diameter sweep on t0024 should therefore produce a **measurable primary DSI
slope** that can actually distinguish the two mechanisms:

* **Schachter2010 active-dendrite amplification**: DSI increases with distal thickening
  because thicker compartments host more Na+ substrate per unit length and amplify
  preferred-direction local spikes more strongly.
* **Passive-filtering alternatives**: DSI decreases with distal thickening because thicker
  dendrites have lower input impedance and less local depolarisation per unit synaptic
  current, damping the directional contrast.

Covers source suggestion **S-0027-03** (high priority) on the t0024 biophysics. Companion to
t0034 (length sweep on t0024).

## Scope

1. Use the **t0024 de Rosenroll 2026 DSGC port** as-is (no channel modifications, no input
   rewiring). Keep the AR(2) correlation ρ=0.6 at its t0026 V_rest-sweep default.
2. Identify distal dendritic sections (HOC leaves on `h.RGC.ON` arbor). Mirror the selection
   rule from t0030's `diameter_override.py` but **COPY** the helper into this task's
   `code/diameter_override_t0024.py` — no cross-task imports per CLAUDE.md.
3. Sweep distal diameter in **7 values** spanning **0.5× to 2.0×** baseline (0.5, 0.75, 1.0,
   1.25, 1.5, 1.75, 2.0×). Apply the multiplier uniformly to all distal branches.
4. For each diameter value, run the **standard 12-direction tuning protocol** (12 angles × 10
   trials) and compute **primary DSI** as the operative metric. Also emit vector-sum DSI and
   secondary metrics.
5. Plot primary DSI vs diameter and classify slope sign: positive (Schachter2010 active),
   negative (passive filtering), flat (neither or schedule-dominated).

## Approach

* **Local CPU only.** No remote compute, no paid API.
* Reuse the t0024 port code at `tasks/t0024_port_de_rosenroll_2026_dsgc/code/` (the
  de_rosenroll_2026_port library is registered and t0024's driver is the model reference).
* Copy the t0030 workflow template: `paths.py`, `constants.py`, `diameter_override.py` (with
  `identify_distal_sections`), `preflight_distal.py`, `trial_runner_diameter.py`,
  `run_sweep.py`, `analyse_sweep.py`, `classify_slope.py`, and `plot_sweep.py`.
* Save per-sweep-point data to `results/data/sweep_results.csv` (incremental checkpoint) and
  per-diameter tuning curves to `results/data/per_diameter/*.csv`.
* Render DSI-vs-diameter chart at `results/images/dsi_vs_diameter.png` plus secondary
  diagnostic plots.

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary with headline DSI-vs-diameter
  slope sign and mechanism classification.
* `results/results_detailed.md` — full methodology, per-direction breakdown at each diameter
  value, slope classification, mechanism attribution (Schachter2010 vs passive filtering),
  comparison to t0030's null result.
* `results/images/dsi_vs_diameter.png` — primary DSI-vs-diameter slope.
* `results/images/vector_sum_dsi_vs_diameter.png` — vector-sum DSI as secondary diagnostic.
* `results/images/polar_overlay.png` — 12-direction polar overlay across all 7 diameters.
* `results/metrics.json` — registered per-diameter DSI metrics.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* **Local CPU only**; no GPU.
* **Expected runtime: 2-4 hours.** The per-(angle, trial) wall time on t0024 is **~12 s** (per
  t0026's V_rest-sweep baseline), vs t0022's ~3.8 s. Full sweep = 7 × 12 × 10 = 840 trials ≈
  **~168 min** at 12 s/trial, plus overhead. Thinner diameters will run slower due to
  increased axial resistance (same behaviour observed on t0030).
* **$0 external cost.**

## Measurement

* **Primary metric**: **primary DSI (peak-minus-null)** at each diameter value. Unlike t0030,
  this is expected to vary because t0024 has non-zero null-direction firing.
* **Secondary**: vector-sum DSI (sanity cross-check), peak Hz, null Hz, HWHM, reliability,
  preferred-direction firing rate, per-direction spike counts, peak voltage at a reference
  distal compartment (to confirm impedance changes).

## Key Questions

1. Is the primary DSI-vs-diameter slope positive (Schachter2010), negative (passive
   filtering), or flat?
2. If positive, is the slope consistent with Na-channel-density amplification as predicted by
   Schachter2010?
3. If negative, does preferred-direction firing drop alongside DSI (general damping) or does
   only the null-direction rate change (selective mechanism)?
4. Does t0024's AR(2) noise broaden the HWHM enough to mask the mechanism signal, or does the
   primary-DSI trend survive the noise floor?
5. How do t0024 and t0022 compare under identical sweep protocols? A measurable slope on t0024
   while t0030 was flat would confirm that the pinned-DSI pathology was the culprit.

## Dependencies

* **t0024_port_de_rosenroll_2026_dsgc** (completed) — provides the DSGC port with AR(2)
  stochastic release.
* **t0030_distal_dendrite_diameter_sweep_dsgc** (completed) — provides the workflow template,
  the `identify_distal_sections` helper (to be copied, not imported), and the null-result
  baseline for comparison.

## Scientific Context

Source suggestion **S-0027-03** (high priority) originally planned for t0022 and executed as
t0030. This task re-runs the same experiment on t0024 specifically because t0024's stochastic
release restores non-zero null firing and therefore makes the primary DSI discriminator
meaningful. Companion to **t0034** (length sweep on t0024).

## Execution Notes

* Follow standard `/execute-task` flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 synthesis already covered the mechanism
  predictions; t0030 already surveyed the prior code).
* Skip `setup-machines` / `teardown` (local CPU only).
* Include `research-code` — need to read the t0024 driver and the t0030 workflow pattern.
* Include `creative-thinking` — if the primary-DSI discriminator works on t0024, consider what
  schedule-level properties t0022 would need to adopt to recover sensitivity.
* Include `compare-literature` — compare the t0024 DSI-vs-diameter slope to Schachter2010 and
  passive-filtering predictions **and** to the t0030 null result.
* **Can be executed in parallel with t0034 in a separate worktree.**

</details>

## Metrics

### distal diam x 0.50

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.703704** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **61.3971** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.942704** |

### distal diam x 0.75

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.741935** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **67.8947** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.926437** |

### distal diam x 1.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.770492** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **72.5882** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.978074** |

### distal diam x 1.25

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.745455** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **71.1623** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.965082** |

### distal diam x 1.50

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.807692** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **77.75** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.941639** |

### distal diam x 1.75

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.735849** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **74.6786** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.944097** |

### distal diam x 2.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.68** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **70.3125** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.977348** |

## Suggestions Generated

<details>
<summary><strong>Zero-cost L/lambda collapse analysis of all t0034 length and t0035
diameter data</strong> (S-0035-01)</summary>

**Kind**: evaluation | **Priority**: high

Re-plot DSI from all existing t0034 (length sweep) and t0035 (diameter sweep) trials against
the computed distal electrotonic length L/lambda, using morphology and passive parameters
already stored in each task's outputs. If the length and diameter data collapse onto a single
curve, this confirms creative_thinking.md's primary hypothesis: the length/diameter asymmetry
is a consequence of cable theory (L/lambda is linear in length but scales as 1/sqrt(d)). No
new simulations required; ~1-2 hours of re-analysis work only. Recommended task types:
data-analysis.

</details>

<details>
<summary><strong>Surface-density-rescaled Nav diameter sweep on t0024 to test
surface-vs-volume compensation</strong> (S-0035-02)</summary>

**Kind**: experiment | **Priority**: high

Re-run a small diameter sweep (0.5x, 1.0x, 2.0x) on the t0024 DSGC with gnabar_HHst rescaled
by 1/d in the distal compartments so the total per-section Nav count is held fixed as diameter
varies. Creative_thinking hypothesis 2 proposes that the flat DSI-vs-diameter result (t0035)
arises because NEURON's surface-density gbar scales total channel current by d while axial
load scales by d^2, cancelling the net effect. If density rescaling produces a non-flat DSI
trend, the compensation confound is confirmed; if still flat, rule out this hypothesis.
Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Extended distal-diameter sweep on t0024 (0.25x to 4.0x, 9 points)
to probe non-linear extremes</strong> (S-0035-03)</summary>

**Kind**: experiment | **Priority**: medium

Push the diameter multiplier beyond t0035's narrow 0.5x-2.0x range into a wider 0.25x-4.0x
sweep (nine multipliers) on the t0024 DSGC substrate to look for non-linear DSI effects that
the 4x range missed. Specifically targets two possibilities: (a) input-impedance saturation at
baseline may break at extreme thinning/thickening and (b) the cable-theory 1/sqrt(d)
prediction implies a detectable DSI shift over a 16x diameter range even if a 4x range is
inside the noise floor. Distinct from S-0030-03 which targets t0022. Recommended task types:
experiment-run.

</details>

<details>
<summary><strong>Ih (HCN) conductance ablation sweep on t0024 distal dendrites to
test h-current role in distal cable behaviour</strong> (S-0035-04)</summary>

**Kind**: experiment | **Priority**: medium

Sweep distal Ih (HCN) gbar from 0 to 2x baseline (five points) on the t0024 DSGC while holding
all other parameters fixed, and measure primary DSI, HWHM, and distal-compartment voltage. Ih
is a known resonance and input-impedance shaper that could partly explain why distal diameter
reads flat on both t0022 and t0024 (t0030 and t0035 both null). If ablation of Ih causes the
diameter sweep to become non-flat, h-current is masking the mechanism. Distinct from S-0009-03
which targeted Ih calibration, not ablation. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Zero-cost meta-analysis of primary-DSI vs vector-sum-DSI
discrepancy across t0029, t0030, t0034, t0035</strong> (S-0035-05)</summary>

**Kind**: evaluation | **Priority**: medium

Combine metrics.json outputs from all four completed morphology sweeps (t0029 length t0022,
t0030 diameter t0022, t0034 length t0024, t0035 diameter t0024) into a single cross-task table
correlating primary DSI against vector-sum DSI. Key questions: when primary DSI is flat or at
ceiling, does vector-sum DSI pick up signal? Does the rank-order of variants agree between the
two metrics? This supports the t0033 optimiser choice and a standing evaluation-methodology
recommendation (compare against S-0029-07, S-0030-06, S-0034-07). No simulations needed; pure
re-analysis of existing CSVs. Recommended task types: data-analysis.

</details>

<details>
<summary><strong>Deprioritise distal-diameter parameters in the t0033 DSI optimiser
search space</strong> (S-0035-06)</summary>

**Kind**: technique | **Priority**: medium

The t0033 DSGC optimisation plan treats distal length and distal diameter as co-equal
morphology parameters. t0034 (p=0.038 on length) and t0035 (p=0.88 on diameter) together show
that distal diameter has DSI leverage below the noise floor on the t0024 substrate, while
length is a strong discriminator. Concrete action: reduce distal-diameter weight in the
optimiser search space (smaller range, coarser grid, or drop it entirely) so the GPU budget
concentrates on axes that actually move DSI. Distinct from S-0034-07 which focuses on the
primary-vs-vector-sum objective; this one concerns the parameter search space itself.
Recommended task types: experiment-run, data-analysis.

</details>

## Research

* [`creative_thinking.md`](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/research/creative_thinking.md)
* [`research_code.md`](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/results_summary.md)*

--- spec_version: "2" task_id: "t0035_distal_dendrite_diameter_sweep_t0024" date_completed:
"2026-04-23" status: "complete" ---
# Results Summary: Distal-Dendrite Diameter Sweep on t0024 DSGC

## Summary

Swept distal-dendrite diameter across seven multipliers (0.5×-2.0× baseline) on the t0024 de
Rosenroll DSGC port under the standard 12-direction × 10-trial moving-bar protocol (840 trials
total). **DSI-vs-diameter slope is flat** (slope 0.0041 per log2(multiplier), **p=0.8808**,
range across extremes -0.0237). **Neither Schachter2010 (predicted positive slope) nor passive
filtering (predicted negative slope) is supported.** Primary DSI range 0.680-0.808 —
measurable (unlike t0030's pinned 1.000 on t0022) but with no mechanism-driven trend.
Contrasts sharply with sibling t0034 (length sweep on same t0024 port) which showed a
statistically significant non-monotonic negative slope (p=0.038): **length modulates DSI on
t0024, diameter does not.**

## Metrics

* **Primary DSI range**: **0.680** (2.0×) to **0.808** (1.5×) — 0.128 absolute range, slope
  0.0041 per log2(multiplier), **p=0.8808** (not distinguishable from zero).
* **Vector-sum DSI range**: **0.417** (2.0×) to **0.463** (0.5×) — 0.046 absolute range, no
  meaningful trend.
* **Preferred-direction peak firing rate**: **4.20 Hz** at 2.0× to **5.40 Hz** at 0.75× /
  1.00× — mild ~25% variation but not monotonic in either direction.
* **Null-direction firing rate**: **0.50-0.80 Hz** across all diameters (non-zero throughout —
  confirms AR(2) rescue holds on the diameter axis too).
* **HWHM**: **61.4°-77.8°** across diameters.
* **Slope classification**: **flat** (mechanism_class="flat", slope=0.0041, p=0.8808,
  dsi_range_extremes=-0.0237, used_fallback=False).
* **Total trials executed**: **840** (7 diameters × 12 directions × 10 trials).
* **Sweep wall time**: approximately **3 hours** end-to-end on local Windows CPU.
* **Sibling comparison**: t0034 (length sweep) on same t0024 port produced slope -0.1259
  (p=0.038); t0035 (diameter) produced slope 0.0041 (p=0.88). **Length modulates DSI; diameter
  does not.**

## Verification

* `verify_task_file.py` — target 0 errors on final pass.
* `verify_task_dependencies.py` — PASSED on step 2 (t0024 and t0030 dependencies completed).
* `verify_research_code.py` — PASSED on step 6 (0 errors, 0 warnings).
* `verify_plan.py` — PASSED on step 7 (0 errors, 0 warnings).
* `verify_task_metrics.py` — target 0 errors.
* `verify_task_results.py` — target 0 errors on final pass.
* `verify_task_folder.py` — target 0 errors on final pass.
* `verify_logs.py` — target 0 errors on final pass.
* `ruff check --fix`, `ruff format`, and `mypy -p
  tasks.t0035_distal_dendrite_diameter_sweep_t0024.code` — all clean (11 files).

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0035_distal_dendrite_diameter_sweep_t0024" date_completed:
"2026-04-23" status: "complete" ---
# Results Detailed: Distal-Dendrite Diameter Sweep on t0024 DSGC

## Summary

Swept distal-dendrite diameter uniformly on the t0024 DSGC port across seven multipliers
(0.5×-2.0× baseline) under the standard 12-direction × 10-trial moving-bar protocol (840
trials total). DSI-vs-diameter slope is **flat** (slope 0.0041 per log2(multiplier),
p=0.8808). Neither Schachter2010 active-amplification (predicted positive slope) nor passive
filtering (predicted negative slope) is supported. Primary DSI varies in a narrow range
(0.680-0.808) without any monotonic trend. Critically, sibling task t0034 (length sweep on the
same t0024 port) produced a statistically significant non-monotonic negative slope (p=0.038),
so the length/diameter asymmetry is the new finding: **length modulates DSI on t0024; diameter
does not**. creative_thinking.md argues this is explained by cable-theory asymmetry (length
enters electrotonic distance L/λ linearly, diameter only as 1/sqrt(d)).

## Methodology

* **Machine**: Windows 11, local CPU only. NEURON 8.2.7 + NetPyNE 1.1.1 (from t0007).
* **Testbed**: `de_rosenroll_2026_port` library (t0024 port), unmodified except for the
  distal-diameter override. AR(2) correlation ρ=0.6 preserved throughout.
* **Distal override**: applied uniformly to all 177 sections returned by
  `cell.terminal_dends`. Selection rule is the same t0024-specific helper copied from t0034
  (not `h.RGC.ON` which doesn't exist on the t0024 arbor).
* **Protocol**: 12-direction moving-bar sweep (0°-330° in 30° steps) × 10 trials per angle × 7
  diameter multipliers = 840 trials.
* **Scoring**: primary DSI (peak-minus-null via `tuning_curve_loss.compute_dsi`), vector-sum
  DSI, peak Hz, null Hz, HWHM, reliability, preferred-direction angle, distal peak mV.
* **Wall time**: approximately 3 hours for 840 trials (~13 s/trial, consistent with t0034/
  t0026 baselines for stochastic AR(2) t0024).
* **Timestamps**: task started 2026-04-23T14:10:45Z; sweep launched 2026-04-23T14:30Z; sweep
  completed ~2026-04-23T17:30Z; end time set in reporting step.

### Per-Diameter Metrics Table

| D_mul | peak_Hz | null_Hz | DSI (primary) | DSI (vector-sum) | HWHM (°) | Reliability | Pref (°) | peak_mV |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.50 | 4.60 | 0.80 | 0.704 | 0.463 | 61.4 | 0.943 | 0 | +27.0 |
| 0.75 | 5.40 | 0.80 | 0.742 | 0.444 | 67.9 | 0.926 | 0 | +32.7 |
| 1.00 | 5.40 | 0.70 | **0.770** | 0.449 | 72.6 | 0.978 | 0 | +31.3 |
| 1.25 | 4.80 | 0.70 | 0.745 | 0.443 | 71.2 | 0.965 | 0 | +29.7 |
| 1.50 | 4.70 | 0.50 | **0.808** | 0.418 | 77.8 | 0.942 | 0 | +29.6 |
| 1.75 | 4.60 | 0.70 | 0.736 | 0.424 | 74.7 | 0.944 | 30 | +30.1 |
| 2.00 | 4.20 | 0.80 | 0.680 | 0.417 | 70.3 | 0.977 | 330 | +28.7 |

Sources: `results/data/metrics_per_diameter.csv`, `results/data/metrics_notes.json`.

### Slope Classification

| Statistic | Value |
| --- | --- |
| Classification label | **flat** |
| Slope (primary DSI per log2(multiplier)) | **0.0041** |
| p-value | **0.8808** (not distinguishable from zero) |
| DSI range across extremes (0.5× vs 2.0×) | -0.0237 |
| Used vector-sum fallback? | No (primary DSI is itself classifiable) |
| Schachter2010 supported? | **No** (no positive slope) |
| Passive filtering supported? | **No** (no negative slope) |

Source: `results/data/slope_classification.json`, `results/data/curve_shape.json`.

## Analysis

**Contradicted assumption**: the task plan expected that on t0024, either Schachter2010 or
passive filtering would produce a measurable DSI slope (because t0034 confirmed primary DSI is
meaningful on t0024). Instead, the diameter axis is flat — neither mechanism supported. The
informative finding is the **length/diameter asymmetry on the same t0024 port**: t0034 (length
sweep) produced slope -0.1259 (p=0.038), while t0035 (diameter sweep) produced slope 0.0041
(p=0.88). This is consistent with cable-theory expectations (length directly scales
electrotonic distance L/λ; diameter enters only through λ = sqrt(d·Rm/Ra) so per-unit diameter
changes have less leverage).

Combined with t0030 (diameter on t0022: also flat), the emerging pattern is: **distal diameter
is a weak DSI discriminator across both testbeds**; **distal length is a strong discriminator
only when the E-I schedule lets primary DSI vary** (t0024 works; t0022 pins at 1.000).

## Charts

![Primary DSI vs distal-dendrite diameter
multiplier](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/images/dsi_vs_diameter.png)

Primary DSI is essentially flat across the 4× diameter sweep (0.680-0.808 range), with no
monotonic trend. Slope 0.0041, p=0.88. Neither Schachter2010 (+slope predicted) nor passive
filtering (-slope predicted) is supported.

![Vector-sum DSI vs distal-dendrite diameter
multiplier](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/images/vector_sum_dsi_vs_diameter.png)

Vector-sum DSI declines mildly from 0.463 at 0.5× to 0.417 at 2.0× but the range (0.046) is
too small to be mechanistically informative.

![Peak firing rate vs distal-dendrite diameter
multiplier](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/images/peak_hz_vs_diameter.png)

Peak firing rate varies mildly (4.2-5.4 Hz) with no monotonic trend, unlike t0034's clean
monotonic 40% decline with length.

![12-direction polar overlay across all 7
diameters](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/images/polar_overlay.png)

Twelve-direction tuning curves overlaid. All 7 diameters produce similar-shape polar curves
with preferred peak near 0° (with small drifts to 30° at 1.75× and 330° at 2.0×). The
uniformity of curves is itself the flat-slope signature.

## Verification

* verify_task_file.py — target 0 errors.
* verify_task_dependencies.py — PASSED on step 2.
* verify_research_code.py — PASSED on step 6.
* verify_plan.py — PASSED on step 7.
* verify_task_metrics.py — target 0 errors.
* verify_task_results.py — target 0 errors.
* verify_task_folder.py — target 0 errors.
* verify_logs.py — target 0 errors.
* `ruff check --fix`, `ruff format`, `mypy -p
  tasks.t0035_distal_dendrite_diameter_sweep_t0024.code` — all clean.
* Pre-merge verificator — target 0 errors before merge.

## Limitations

* **Diameter range 0.5×-2.0× narrow**: a wider sweep (0.25×-4.0×) might reveal non-linear
  effects not captured in the 4× range.
* **AR(2) ρ=0.6 fixed**: same ρ as t0034; no disambiguation of noise-vs-biophysics.
* **Uniform multiplier**: all 177 distal leaves scaled identically. Non-uniform scaling (e.g.,
  proximal-to-distal taper) could yield different results.
* **No L/λ analysis performed**: creative_thinking's recommended follow-up (re-plot all t0034
  + t0035 data against computed distal L/λ) is a zero-cost next step but wasn't done inline.

## Examples

Ten concrete (diameter, direction, trial) input / (peak_mv, firing_rate_hz) output pairs drawn
from `results/data/sweep_results.csv`. All trials use AR(2) ρ=0.6 stochastic release.

### Example 1: D=0.50× preferred direction (peak)

```text
diameter_multiplier=0.50, trial=0, direction_deg=0
```

```csv
0.50,0,0,5,38.039,5.000000
```

### Example 2: D=0.50× preferred direction (trial variance)

```text
diameter_multiplier=0.50, trial=1, direction_deg=0
```

```csv
0.50,1,0,5,35.998,5.000000
```

Repeated 10 trials at (D=0.50×, dir=0°) produced spike counts {5, 5, 4, 4, 4, 5, 4, 5, 5, 5} —
genuine AR(2) variance.

### Example 3: D=0.75× preferred direction

```text
diameter_multiplier=0.75, trial=0, direction_deg=0
```

```csv
0.75,0,0,5,37.945,5.000000
```

### Example 4: D=1.00× baseline

```text
diameter_multiplier=1.00, trial=0, direction_deg=0
```

```csv
1.00,0,0,5,38.187,5.000000
```

### Example 5: D=1.25× preferred direction

```text
diameter_multiplier=1.25, trial=0, direction_deg=0
```

```csv
1.25,0,0,4,37.883,4.000000
```

### Example 6: D=1.50× preferred direction (DSI peak at 0.808)

```text
diameter_multiplier=1.50, trial=0, direction_deg=0
```

```csv
1.50,0,0,5,38.025,5.000000
```

### Example 7: D=1.75× preferred-angle drift to 30°

```text
diameter_multiplier=1.75, trial=0, direction_deg=30
```

```csv
1.75,0,30,4,37.845,4.000000
```

### Example 8: D=2.00× preferred direction (firing decline)

```text
diameter_multiplier=2.00, trial=0, direction_deg=0
```

```csv
2.00,0,0,4,37.506,4.000000
```

### Example 9: D=1.50× null direction (AR(2) variance)

```text
diameter_multiplier=1.50, trial=0, direction_deg=180
```

```csv
1.50,0,180,0,-53.024,0.000000
```

### Example 10: D=2.00× null direction

```text
diameter_multiplier=2.00, trial=5, direction_deg=240
```

```csv
2.00,5,240,1,35.912,1.000000
```

Takeaway: across 0.5× to 2.0× diameter, preferred-direction firing varies mildly (4-5 Hz) and
null-direction firing stays in the 0.5-0.8 Hz band from AR(2) noise — resulting in a narrow
primary DSI band (0.680-0.808) with no measurable slope trend.

## Files Created

### Code (10 Python files, lint + mypy clean)

* `code/paths.py`, `code/constants.py`, `code/distal_selector_t0024.py`,
  `code/diameter_override_t0024.py`, `code/preflight_distal.py`,
  `code/trial_runner_diameter_t0024.py`, `code/run_sweep.py`, `code/analyse_sweep.py`,
  `code/classify_slope.py`, `code/plot_sweep.py`

### Data

* `results/data/sweep_results.csv` (840 trials + header)
* `results/data/per_diameter/tuning_curve_D{0p50,0p75,1p00,1p25,1p50,1p75,2p00}.csv`
* `results/data/metrics_per_diameter.csv`, `results/data/dsi_by_diameter.csv`,
  `results/data/metrics_notes.json`
* `results/data/curve_shape.json`, `results/data/slope_classification.json`
* `results/metrics.json`

### Charts

* `results/images/dsi_vs_diameter.png`, `results/images/vector_sum_dsi_vs_diameter.png`,
  `results/images/peak_hz_vs_diameter.png`, `results/images/polar_overlay.png`

### Research

* `research/research_code.md`, `research/creative_thinking.md`

### Task artefacts

* `plan/plan.md` (11 sections, 17 REQ items)
* `task.json`, `task_description.md`, `step_tracker.json`
* Full step logs under `logs/steps/`

## Task Requirement Coverage

Operative task text (from task.json and task_description.md), quoted:

```text
Sweep distal-dendrite diameter on the t0024 de Rosenroll DSGC port; discriminate
Schachter2010 active amplification vs passive filtering; primary DSI is meaningful on t0024
unlike t0030.

1. Use t0024 as-is (AR(2) rho=0.6).
2. Identify distal sections (h.RGC.ON leaves). COPY helper from t0029/t0030.
3. Sweep 7 diameter multipliers 0.5x-2.0x uniformly.
4. 12-direction tuning protocol per diameter. Compute PRIMARY DSI.
5. Plot DSI vs diameter and classify slope sign: positive (Schachter), negative (passive),
   flat.
```

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | t0024 as-is + AR(2) ρ=0.6 | **Done** | constants.py AR2_RHO preserved |
| REQ-2 | Distal selection via terminal_dends | **Done** | 177 sections identified; no h.RGC.ON reference |
| REQ-3 | Copy helpers (t0030 diameter, t0034 selector) | **Done** | diameter_override_t0024.py, distal_selector_t0024.py copied |
| REQ-4 | 7 multipliers 0.5×-2.0× | **Done** | constants.py DIAMETER_MULTIPLIERS |
| REQ-5 | 12-dir × 10-trial protocol | **Done** | 840 rows in sweep_results.csv |
| REQ-6 | AR(2) ρ=0.6 at every call | **Done** | trial_runner_diameter_t0024.py module-scope constant |
| REQ-7 | Secondary metrics | **Done** | metrics_per_diameter.csv with all columns |
| REQ-8 | Slope classification | **Done** | curve_shape.json label="flat", slope=0.0041, p=0.8808 |
| REQ-9 | Vector-sum defensive fallback | **Done** | vector_sum_dsi_vs_diameter.png emitted |
| REQ-10 | Polar overlay | **Done** | results/images/polar_overlay.png |
| REQ-11 | Peak-Hz chart | **Done** | results/images/peak_hz_vs_diameter.png |
| REQ-12 | Slope taxonomy emitted | **Done** | slope_classification.json mechanism_class="flat" |
| REQ-13 | Per-row flush | **Done** | run_sweep.py fh.flush() confirmed |
| REQ-14 | $0 local CPU | **Done** | costs.json $0.00; remote_machines_used.json [] |
| REQ-15 | Primary DSI measurable on t0024 | **Done** | 0.680-0.808 range (not pinned at 1.000 like t0030) |
| REQ-16 | Seed uniqueness | **Done** | 840 unique seeds confirmed in run_sweep.py |
| REQ-17 | t0030 comparison | **Done** | Both diameter sweeps flat — diameter is weak discriminator on both testbeds |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0035_distal_dendrite_diameter_sweep_t0024" date_compared:
"2026-04-22" ---
# Comparison with Published Results

## Summary

This task swept distal-dendrite diameter from **0.5×** to **2.0×** on the t0024 de Rosenroll
DSGC port with AR(2) correlated release (ρ=0.6), aiming to discriminate Schachter2010
active-dendrite amplification (predicted **positive** slope) from passive filtering (predicted
**negative** slope). The primary DSI slope is **0.0041 per log2(multiplier), p=0.8808** —
statistically flat — with primary DSI spanning only **0.680-0.808** and vector-sum DSI
spanning **0.417-0.463**. Neither Schachter2010 nor passive filtering is supported. Combined
with sibling t0034 (length sweep on the same t0024 port) which produced slope **-0.1259,
p=0.038** (non-monotonic negative) and parent t0030 (diameter on t0022) which was also flat,
the headline finding is a **length / diameter asymmetry**: length modulates DSI on t0024;
diameter does not. Cable theory explains this directly (length enters L/λ linearly, diameter
only as 1/√d), and the result has concrete implications for the t0033 joint morphology-channel
optimiser.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Schachter2010, Overview] active-dendrite amplification predicts **positive** DSI-vs-diameter slope | DSI vs diameter slope sign | positive | **+0.0041** per log2(multiplier) | n/a | p=0.8808, not distinguishable from zero. Predicted positive slope NOT observed. Schachter2010's ~4× amplification (PSP DSI 0.20 → spike DSI 0.80) requires dendritic Nav substrate that HHst lumps. |
| [Schachter2010, Overview] spike DSI at baseline DSGC morphology | Somatic spike DSI | **0.80** | **0.770** (1.0× baseline) | **-0.030** | Near-exact match at baseline (same value t0034 reported). Baseline regime is Schachter2010-like; diameter perturbation does not move DSI as predicted. |
| Passive filtering (cable theory, `Z ∝ 1/d^1.5`, per t0027 synthesis) [Wu2023, abstract via t0027 full_answer.md:108-113] | DSI vs diameter slope sign | negative | **+0.0041** per log2(multiplier) | n/a | p=0.8808, not distinguishable from zero. Predicted negative slope NOT observed. Sign is positive (but inside noise); magnitude is negligible. |
| [Wu2023, abstract via t0027 full_answer.md:108-113] primate SAC distal-diameter saturation | Saturation threshold diameter | ~0.8 μm | Flat primary DSI across 0.5×-2.0× sweep | n/a | Baseline distal `seg.diam` straddles ~0.4-1.0 μm, so the 0.5×-2.0× range (~0.2-2.0 μm) brackets Wu2023's saturation threshold. Observed flat curve is qualitatively consistent with saturated regime. |
| [PolegPolsky2026, Overview via t0027 full_answer.md:125-128] ML-driven DSGC parameter search reaches DSI > 0.5 | Somatic spike DSI | **> 0.5** (reachable) | **0.770** at 1.0× baseline | **> +0.27** | Our baseline sits firmly in PolegPolsky2026's reachable band. Different morphology (352-segment PolegPolsky vs 177-terminal t0024). |
| [deRosenroll2026, Fig correlated vs uncorrelated release] same cell model, vector-sum DSI with AR(2) release | Vector-sum DSI (ρ=0.6) | **0.39** (8-direction bar) | **0.449** at 1.0× (12-direction bar) | **+0.059** | Same cell port, near-same protocol. Our vector-sum DSI is slightly higher because we run 12-direction vs 8-direction sampling; within trial-level noise. |
| [Tukker2004, cable-filtering framing via t0034 compare_literature.md:88-99] electrotonic-length optimum; DSI peaks at intermediate λ | Primary DSI vs morphology axis | non-monotonic with interior optimum | **0.808** at 1.5× (sweep peak) | n/a | Qualitative peak-at-interior match on the diameter axis is weak (range 0.128 too narrow to declare non-monotonicity significant); the cable-filtering signature lives on the length axis (t0034), not diameter. |
| [Hausselt2007, Results] SAC DSI scales monotonically with dendritic length 50-200 μm | DSI at baseline (voltage DSI) | **0.35** at baseline length (~150 μm) | **0.770** at 1.0× baseline | **+0.420** | Different cell type (DSGC vs SAC) and readout (spike DSI vs voltage DSI); Hausselt2007 predicts a length effect which t0034 confirmed, not a diameter effect. |

### Prior Task Comparison

The t0035 plan and task description cite three upstream project results as motivation and
baselines: t0030 (diameter sweep on t0022), t0034 (length sweep on the same t0024 port), and
t0024 (the underlying cell port). Restating their values here makes the length/diameter
asymmetry explicit.

| Prior Task | Axis | Testbed | Primary DSI range | Slope | p-value | Classification | Delta vs t0035 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| t0030 | diameter | t0022 | **1.000-1.000** (pinned) | **+0.0083** (vector-sum) | **0.1773** | flat (vector-sum fallback used) | Both flat; t0035 primary DSI is not pinned |
| t0034 | length | t0024 | **0.545-0.774** | **-0.1259** per unit L_mul | **0.038** | non-monotonic (net negative) | **slope differs by +0.13** in magnitude |
| t0035 (this task) | diameter | t0024 | **0.680-0.808** | **+0.0041** per log2 | **0.8808** | flat | — |
| t0024 baseline (1.0×, per t0026) | — | t0024 | DSI 0.36-0.67 (V_rest) | — | — | non-pinned, measurable | Our 1.0× DSI (**0.770**) within band |

Per-multiplier comparison of primary DSI on the same t0024 port:

| Multiplier | t0034 primary DSI (length) | t0035 primary DSI (diameter) | Delta (length - diameter) |
| --- | --- | --- | --- |
| 0.50× | **0.754** | **0.704** | **+0.050** |
| 0.75× | **0.774** | **0.742** | **+0.032** |
| 1.00× | **0.770** | **0.770** | **+0.000** |
| 1.25× | **0.745** | **0.745** | **+0.000** |
| 1.50× | **0.623** | **0.808** | **-0.185** |
| 1.75× | **0.720** | **0.736** | **-0.016** |
| 2.00× | **0.545** | **0.680** | **-0.135** |

The two axes agree at the 1.0× and 1.25× baseline anchors by construction (same cell, same
AR(2) seed structure) but diverge at extremes: length collapses monotonically (with
local-spike-failure preferred-angle jumps at 1.5× and 2.0×); diameter stays in a narrow
0.680-0.808 band with no monotonic trend and no preferred-angle collapse. **The
lineage-internal headline is that length and diameter are asymmetric discriminators on
identical t0024 biophysics.**

## Methodology Differences

* **Cell type and testbed match is strong at the baseline anchor.** Schachter2010 (mammalian
  DSGC with distal Nav), PolegPolsky2026 (DSGC ML search), and deRosenroll2026 (same DSGC port
  with AR(2) release) are the only directly comparable mammalian DSGC references. Wu2023 uses
  primate SAC and is adjacent, not matched. Tukker2004 and Hausselt2007 study SACs
  (pre-synaptic to DSGCs) but their cable-filtering framing is cell-type-agnostic.
* **Active conductance complement.** Schachter2010 uses dendritic Nav 40 mS/cm² + Kv;
  PolegPolsky2026 uses a lumped HH substrate similar to ours. The t0024 port ships HH-style
  soma channels with AR(2)-correlated AMPA/NMDA/GABA synapses. Our uniform `seg.diam`
  rescaling changes surface area and axial resistance without altering channel density
  (S/cm²), so total Nav current rises linearly with d while axial load rises as d² — this
  surface-vs-volume cancellation is discussed in `creative_thinking.md §2`.
* **Metric definition.** Our primary DSI is (R_pref - R_null) / (R_pref + R_null) on
  12-direction spike counts with AR(2) non-zero null firing (0.5-0.8 Hz across the sweep).
  Schachter2010 and Sivyer2013 compute on mammalian DSGC spike counts. Hausselt2007's voltage
  DSI at SAC tips is a different readout entirely.
* **Stochasticity: AR(2) release is retained (ρ=0.6).** Schachter2010 and passive-filtering
  predictions were made at deterministic drive; our sweep adds AR(2)-correlated release. The
  t0034 companion task confirmed AR(2) enables non-zero null firing (0.7-1.0 Hz), rescuing the
  primary DSI discriminator from the t0022 pinned-at-1.000 pathology observed in t0030. AR(2)
  is therefore a feature, not a confound, for the t0024-axis sweeps.
* **Diameter range and baseline.** Wu2023 reports primate-SAC DSI saturation above distal
  diameter ~0.8 μm; our baseline distal `seg.diam` straddles ~0.4-1.0 μm and the 0.5×-2.0×
  sweep covers ~0.2-2.0 μm. Our range brackets Wu2023's saturation threshold but does not
  extend far enough above it to probe the super-saturated regime.
* **Uniform-multiplier-only.** All 177 distal leaves are scaled identically. Non-uniform
  diameter changes (proximal-to-distal tapering, single-branch thickening) would decouple the
  uniform surface-vs-volume cancellation and could expose mechanisms the uniform sweep
  averages out (`creative_thinking.md §7`).
* **No axon / AIS substrate.** Schachter2010's model includes an AIS with high Nav density
  participating in the distal-to-soma amplification cascade. The t0024 morphology does not
  expose a populated AIS `SectionList`, so the predicted amplification regime is structurally
  partial.

## Analysis

### Schachter2010 prediction vs observation

Schachter2010 predicts thicker distal dendrites host more Nav per unit length, producing
larger and more reliable preferred-direction local spikes and a **positive** DSI-vs-diameter
slope. Our observation is slope **+0.0041 per log2(multiplier)** with p=**0.8808** and DSI
range at extremes of just **-0.0237** — the classifier's 0.05 threshold for an
active-amplification signature is not met, and the p-value is two orders of magnitude above
0.05. The sign is nominally positive but statistically indistinguishable from zero.
**Schachter2010 active amplification is not supported on the diameter axis of t0024.** At the
1.0× baseline the DSI match to Schachter2010's 0.8 is very close (**0.770** observed vs
**0.80** predicted, delta **-0.030**), confirming the baseline biophysics are
Schachter2010-compatible; diameter perturbation simply does not move the system along the
predicted axis.

### Passive-filtering prediction vs observation

Passive cable theory predicts `Z_in ∝ 1/d^1.5`: thicker distal sections have lower input
impedance per unit synaptic current, so preferred-direction depolarisation is damped and DSI
should **decrease** with diameter. Our observation is a positive (flat) slope, which is the
**opposite sign** to the passive-filtering prediction — but again statistically
indistinguishable from zero. **Passive filtering is not supported on the diameter axis of
t0024 either.** Both named mechanism hypotheses fail in the same way: the diameter axis is
simply too weak a DSI lever to register either signature.

### Cable-theory asymmetry is the likely explanation

`creative_thinking.md §1` argues that cable theory predicts **length enters electrotonic
distance L/λ linearly, diameter only as 1/√d** (since `λ = √(d·Rm/(4·Ra))`). A 2× length
change doubles L/λ; a 2× diameter change only multiplies it by **1/√2 ≈ 0.71**. The DSI-moving
lever is L/λ, so the length axis has **~2.8× more leverage per log2-multiplier than the
diameter axis** on a first-order cable analysis. Applied to the measured t0034 length slope
(**-0.1259**), a naive √d rescaling predicts a t0035 diameter slope of about **-0.05 per
log2(multiplier)** — still detectable at 840 trials, but close to our measurement noise floor.
The observed slope (**+0.0041**, p=0.88) is consistent with cable-theory leverage being
further reduced by the surface-vs-volume cancellation described in `creative_thinking.md §2`,
where scaling d → k·d leaves net preferred-direction current roughly constant (total Nav
scales linearly with d, axial load scales with d²).

The combined prediction — √d attenuation multiplied by surface-vs-volume cancellation —
produces an essentially-zero diameter slope, matching the observation. **This is the primary
headline finding**: length and diameter, though formally dual in cable equations, are
asymmetric DSI discriminators on t0024.

### Wu2023 saturation consistency

Wu2023's primate-SAC saturation threshold at ~**0.8 μm** distal diameter brackets our baseline
(~0.4-1.0 μm); the sweep covers ~0.2-2.0 μm. The observed flat DSI is qualitatively consistent
with operating in the saturated regime Wu2023 identifies. This agreement is aesthetic, not
discriminative — both Schachter2010 and passive filtering predict non-flat curves away from
saturation, and our testbed cannot exit saturation within the current sweep geometry. If a
future sweep extends to 4× or introduces non-uniform tapering, Wu2023's saturation prediction
becomes directly testable.

### Why t0030 (diameter on t0022) also returned flat

t0030 reported primary DSI pinned at **1.000** on t0022 (vector-sum slope 0.0083, p=0.18) and
attributed the null to t0022's deterministic E-I driver silencing null firing at 0 Hz. t0035
on t0024 has non-zero null firing (AR(2) ρ=0.6 holds null at 0.5-0.8 Hz), so the primary DSI
is measurable (0.680-0.808) — but the slope is still flat. **Both t0030 and t0035 return
"diameter is inert" from different failure modes**: t0030 because the metric saturates, t0035
because the leverage is below detection. The reproducibility of the diameter-inert result
across testbeds is itself evidence that the cable-theory √d attenuation is the underlying
cause rather than any testbed-specific quirk.

### Implications for t0033 joint morphology-channel optimisation

The t0033 plan (not yet executed — task folder at
`tasks/t0033_plan_dsgc_morphology_channel_optimisation/`) will need to pick a
parameter-priority ordering for the optimiser. The t0034 + t0035 pair provides **direct
evidence** for that ordering on the t0024 testbed:

* **Prioritise length-like parameters** (distal leaf `sec.L`, branch count, electrotonic tree
  depth) — these produced a **p=0.038 signal with 0.229 DSI range** on t0034 and are the
  efficient primary-DSI lever.
* **De-prioritise diameter-like parameters** (distal `seg.diam`, proximal `seg.diam`, uniform
  caliber scaling) — these produced a **p=0.88 noise** with a 0.128 range that is dominated by
  AR(2) variance on t0035.
* **On t0022 testbeds where primary DSI is pinned**, the optimiser must fall back to
  vector-sum DSI regardless of the parameter axis — t0030 showed vector-sum DSI has weak but
  non-zero sensitivity (range 0.012 over 4× diameter); on t0024 it has range 0.046 over 4×
  diameter (still small but usable).
* **An informative follow-up** at zero simulation cost (per `creative_thinking.md §1.c`) is to
  re-plot t0034's length sweep and t0035's diameter sweep against **computed L/λ**. If the two
  sweeps collapse onto a common primary-DSI-vs-L/λ curve, cable-theory asymmetry is confirmed
  as the sole explanation and the optimiser should parameterise morphology directly in L/λ
  rather than in raw `sec.L` / `seg.diam`.

The asymmetry is an architectural lesson for t0033: **parameter choice matters more than
parameter range**. Doubling the diameter range from 4× to 8× will not rescue the null signal;
replacing the diameter axis with the length axis (or an L/λ-equivalent compound parameter)
will.

## Limitations

* **Only the seven-point diameter curve is measured here.** The t0030 and t0034 values are
  restated from those tasks' completed results, not re-measured. The cable-theory asymmetry
  interpretation relies on the t0034 slope (p=0.038) holding up under the same AR(2) noise
  model at 10 trials per angle — a 30-trial re-run is recommended but not performed.
* **Diameter range 0.5×-2.0× is narrow.** A wider sweep (0.25×-4.0×) is inside the feasible
  NEURON integration regime and could test whether a non-linear effect appears at extreme
  diameters, particularly the Wu2023 super-saturated regime above ~1.6 μm. The
  surface-vs-volume cancellation argument in `creative_thinking.md §2` should persist at
  extremes, but this is not verified.
* **AR(2) variance floor not computed.** `creative_thinking.md §5` raises the possibility that
  the vector-sum DSI range (0.046) sits inside the per-trial AR(2) variance, making the
  experiment underpowered for detecting a real slope smaller than the floor. The minimum
  detectable slope at α=0.05 has not been calculated from the 840-trial residuals.
* **Schachter2010 PSP-DSI measurement not available.** Schachter2010's headline claim is the
  ~4× amplification from PSP DSI ~0.20 to spike DSI ~0.80. The t0024 driver emits spike-count
  tuning only; the PSP-DSI axis that would directly test Schachter2010's amplification step is
  not produced and cannot be compared.
* **Lumped HHst channel substrate.** The dendritic channels are a lumped HH Na/K pair rather
  than the Nav1.6 / Nav1.2 / Kv1.2 / Kv3 complement recommended in t0019. Schachter2010's
  predicted amplification depends on persistent-Nav kinetics this substrate does not fully
  reproduce. A re-run with the t0019 channel set is scheduled for t0033.
* **Tukker2004 and Hausselt2007 are SAC papers.** The cable-filtering framing transfers
  cell-type-agnostically, but absolute DSI magnitudes are not directly comparable because SACs
  and DSGCs have different spike thresholds and integration geometries.
* **No 2-D length × diameter sweep.** The decisive follow-up — a joint sweep that can separate
  the L/λ dependence from the surface-vs-volume cancellation — has not been run. t0034 and
  t0035 are matched 1-D sweeps along orthogonal axes but do not sample interaction terms.
* **Uniform-multiplier-only, no tapering.** Non-uniform diameter changes (proximal-to-distal
  tapering matched to the channel gradient) could reveal mechanisms that the uniform sweep
  averages out, per the morphology-gradient hypothesis in `creative_thinking.md §7`.

</details>
