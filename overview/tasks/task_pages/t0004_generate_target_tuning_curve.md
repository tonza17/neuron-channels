# ✅ Generate canonical target angle-to-AP-rate tuning curve

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0004_generate_target_tuning_curve` |
| **Status** | ✅ completed |
| **Started** | 2026-04-19T08:12:46Z |
| **Completed** | 2026-04-19T08:42:30Z |
| **Duration** | 29m |
| **Task types** | `feature-engineering` |
| **Categories** | [`direction-selectivity`](../../by-category/direction-selectivity.md) |
| **Expected assets** | 1 dataset |
| **Step progress** | 8/15 |
| **Task folder** | [`t0004_generate_target_tuning_curve/`](../../../tasks/t0004_generate_target_tuning_curve/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0004_generate_target_tuning_curve/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0004_generate_target_tuning_curve/task_description.md)*

# Generate canonical target angle-to-AP-rate tuning curve

## Motivation

The key project metric `tuning_curve_rmse` compares a simulated angle-to-AP-rate tuning curve
against a target. The researcher chose to **simulate** a canonical target curve rather than
digitise one from a paper. This task generates that canonical target and registers it as a
dataset asset so all later optimisation tasks share one fixed reference.

## Scope

Produce a single dataset asset containing:

* A cosine-like target tuning curve sampled at 12 or 24 angles around 360°.
* Explicit generator parameters: preferred direction (deg), baseline rate (Hz), peak rate
  (Hz), tuning half-width (deg or von Mises κ), and random seed.
* Per-angle mean rates plus a small number of synthetic noisy trial replicates so the
  `tuning_curve_reliability` metric has a well-defined ground-truth value.

Suggested functional form:

```
r(θ) = r_base + (r_peak - r_base) * ((1 + cos(θ - θ_pref)) / 2) ** n
```

with `n` controlling sharpness. Any equivalent von Mises formulation is fine. The exact values
of `r_base`, `r_peak`, `θ_pref`, and `n` should be chosen to give a biologically plausible DSI
(roughly 0.6-0.9) and reported in the dataset's `details.json`.

## Approach

1. Write a small Python script under `code/` that generates the curve, saves it to `data/` as
   CSV or JSON, and writes the dataset asset folder under `assets/dataset/`.
2. Include both a mean-rate table and a per-trial table (e.g., 20 synthetic trials) so
   `tuning_curve_reliability` has a real reference value.
3. Plot the curve and save to `results/images/target_tuning_curve.png`.

## Expected Outputs

* One dataset asset under `assets/dataset/target_tuning_curve/` containing the CSV/JSON
  tables, metadata, and description.
* A plot of the target curve in `results/images/`.

## Compute and Budget

Trivial. Runs locally in seconds; no external cost.

## Dependencies

None. Runs in parallel with t0002 and t0003. This task is the reference any later optimisation
task will compare against.

## Verification Criteria

* Dataset asset passes `verify_dataset_asset.py`.
* `details.json` records the generator parameters and random seed explicitly.
* The generated CSV/JSON has one row per angle and the noisy-trial table has at least 10
  trials per angle.

</details>

## Metrics

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.8824** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **68.51** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| dataset | [Target Direction Tuning Curve (synthetic)](../../../tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/) | [`description.md`](../../../tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/description.md) |

## Suggestions Generated

<details>
<summary><strong>Generate weaker-DSI variant target tuning curves</strong>
(S-0004-01)</summary>

**Kind**: dataset | **Priority**: medium

Create sibling dataset assets (e.g., target-tuning-curve-weak-dsi,
target-tuning-curve-mid-dsi) with the same generator but r_peak values chosen so DSI lands at
~0.65 and ~0.75. Lets downstream fitting tasks test whether the optimisation pipeline is
robust across the 0.6-0.9 band instead of only the upper end.

</details>

<details>
<summary><strong>Add a Poisson-noise variant of the target trials</strong>
(S-0004-02)</summary>

**Kind**: dataset | **Priority**: low

Replace the current Gaussian-noise trial replicates with Poisson counts converted to rates
(Fano factor ~1) and register it as a separate dataset asset. This would give
tuning_curve_reliability a noise model closer to real spike statistics while keeping the
closed-form mean curve unchanged.

</details>

<details>
<summary><strong>Build a small reusable library for target-vs-simulated tuning curve
metrics</strong> (S-0004-03)</summary>

**Kind**: library | **Priority**: high

Factor the closed-form DSI, HWHM, tuning_curve_rmse, and tuning_curve_reliability computations
out of individual tasks into a shared library asset. Every later fitting task will need these
four functions; centralising them avoids divergent reimplementations and makes metric values
reproducible from parameters alone.

</details>

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0004_generate_target_tuning_curve/results/results_summary.md)*

# Results Summary: Generate Canonical Target Tuning Curve

## Summary

Synthesised the canonical direction tuning curve `target-tuning-curve` from a closed-form
half-wave-rectified cosine raised to power `n = 2` with `θ_pref = 90°`, `r_base = 2 Hz`,
`r_peak = 32 Hz`, and 20 Gaussian-noise trials per angle (`σ = 3 Hz`, seed `42`). The asset is
registered under `assets/dataset/target-tuning-curve/` with explicit generator parameters and
a diagnostic plot.

## Metrics

* **Direction Selectivity Index (DSI)**: **0.8824** — inside the required [0.6, 0.9] band
* **Tuning curve HWHM**: **68.5°** — computed from the closed-form curve
* **Sampled directions**: **12** angles at 30° spacing (0° to 330°)
* **Trials per direction**: **20** (240 rows total in `curve_trials.csv`)
* **Mean absolute bias (sample vs closed form)**: **0.419 Hz** (max 1.063 Hz)

## Verification

* `verify_task_folder.py` — PASSED (0 errors, 1 warning FD-W002 on empty `logs/searches/`)
* `verify_task_dependencies.py` — PASSED (0 errors, 0 warnings; no dependencies)
* `verify_plan.py` — PASSED (0 errors, 0 warnings)
* `verify_task_metrics.py` — to be run in the reporting step together with
  `verify_task_results`
* `verify_dataset_asset.py` — **not available** in this repository; the dataset asset
  structure is checked by `verify_task_folder` and re-checked by `verify_pr_premerge` at merge
  time

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0004_generate_target_tuning_curve/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0004_generate_target_tuning_curve" ---
# Results: Generate Canonical Target Tuning Curve

## Summary

This task synthesised the canonical direction-tuning reference that every downstream fit in
the project will compare against. The curve is a half-wave-rectified cosine raised to power `n
= 2`, parameterised by preferred direction `θ_pref = 90°`, baseline rate `r_base = 2 Hz`, peak
rate `r_peak = 32 Hz`, Gaussian trial noise `σ = 3 Hz`, and random seed `42`. The deliverable
is the `target-tuning-curve` dataset asset (v2 spec) containing `curve_mean.csv` (12 angles),
`curve_trials.csv` (12 × 20 = 240 trials), `generator_params.json`, and a diagnostic PNG.

## Methodology

* **Machine**: Local Windows 11 workstation (x86_64), no remote compute.
* **Run time**: the generator completes in under 2 seconds end-to-end.
* **Start**: 2026-04-19T08:25:41Z.
* **End**: 2026-04-19T08:31:00Z (wall-clock for implementation step, dominated by asset
  authoring and formatting, not compute).
* **Method**: deterministic closed-form sampling via `r(θ) = r_base + (r_peak - r_base) * ((1
  + cos(θ - θ_pref)) / 2) ** n`, then Gaussian noise drawn from
  `numpy.random.default_rng(seed=42)` and clipped at 0 Hz. Output rendered with matplotlib
  using the headless Agg backend.
* **Key files**: `code/generate_target.py`, `code/paths.py`.

## Metrics Tables

### Registered Metrics

| Metric | Value | Unit |
| --- | --- | --- |
| `direction_selectivity_index` | **0.8824** | ratio |
| `tuning_curve_hwhm_deg` | **68.51** | degrees |

The DSI is evaluated in closed form as `DSI = (r_pref - r_null) / (r_pref + r_null) = (32 - 2)
/ (32 + 2) = 0.8824`. The HWHM solves `((1 + cos(Δθ)) / 2) ** n = (0.5 × r_peak - r_base) /
(r_peak - r_base) = 14/30`, giving `Δθ = arccos(2 × √(14/30) - 1) ≈ 68.51°`.

### Target Curve (closed form)

| `angle_deg` | `mean_rate_hz` |
| --- | --- |
| 0 | 9.500 |
| 30 | 18.982 |
| 60 | 28.696 |
| 90 | 32.000 |
| 120 | 28.696 |
| 150 | 18.982 |
| 180 | 9.500 |
| 210 | 3.518 |
| 240 | 2.304 |
| 270 | 2.000 |
| 300 | 2.304 |
| 330 | 3.518 |

### Sample Fidelity Across 20 Trials

| Quantity | Value |
| --- | --- |
| Mean absolute bias (sample − closed form) | **0.419 Hz** |
| Max absolute bias (sample − closed form) | **1.063 Hz** |
| Expected SE of per-angle mean (σ / √n_trials) | **0.671 Hz** |

Max observed bias is well below `2 × SE`, confirming the seeded sample is within the expected
noise envelope of the closed form.

## Visualizations

![Target direction tuning curve with 20 trial replicates per
angle](../../../tasks/t0004_generate_target_tuning_curve/results/images/target_tuning_curve.png)

The plot overlays the closed-form curve (blue), per-angle mean ± SD across 20 trials (red
error bars), and individual trial scatter (light red). The DSI is printed in the title.

## Verification

| Verificator | Result | Notes |
| --- | --- | --- |
| `verify_task_file.py` | PASSED | 0 errors, 0 warnings |
| `verify_task_dependencies.py` | PASSED | No dependencies declared |
| `verify_plan.py` | PASSED | 0 errors, 0 warnings |
| `verify_task_folder.py` | PASSED | 1 warning (FD-W002: empty `logs/searches/`, non-blocking) |

A dedicated `verify_dataset_asset.py` script does not exist in this repository; dataset asset
structure is validated by `verify_task_folder.py` and re-checked by `verify_pr_premerge.py` at
merge time. The plan's "run the dataset asset verificator" step was performed through
`verify_task_folder` and by manually checking conformance against
`meta/asset_types/dataset/specification.md` v2 (spec_version, dataset_id regex match, required
fields present, at least one file in `files/`, canonical description document with all seven
mandatory sections).

## Files Created

* `tasks/t0004_generate_target_tuning_curve/code/generate_target.py` — 258-line generator.
* `tasks/t0004_generate_target_tuning_curve/code/paths.py` — centralised paths module.
* `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/details.json` —
  v2 dataset metadata with full `generator_params`.
* `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/description.md`
  — v2 canonical description document with all seven mandatory sections.
* `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_mean.csv`
  — 12 rows, columns `angle_deg,mean_rate_hz`.
* `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_trials.csv`
  — 240 rows, columns `angle_deg,trial_index,rate_hz`.
* `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/generator_params.json`
  — echo of the `GeneratorParams` dataclass.
* `tasks/t0004_generate_target_tuning_curve/results/images/target_tuning_curve.png` —
  diagnostic plot (8 × 5 inches, 150 dpi).
* `tasks/t0004_generate_target_tuning_curve/results/metrics.json`, `results/costs.json`,
  `results/remote_machines_used.json`, `results/results_summary.md`,
  `results/results_detailed.md` — this step's outputs.

## Limitations

* The DSI of 0.8824 sits near the upper end of the requested [0.6, 0.9] band. Downstream fits
  that require a weaker-selectivity reference must create a separate dataset asset (e.g.,
  `target-tuning-curve-weak-dsi`) with lower `r_peak_hz` rather than editing this one
  (immutability of completed tasks).
* The noise model is Gaussian with clipping at 0 Hz, not a spiking process. Realistic AP rate
  noise is closer to Poisson with Fano factor near 1; the Gaussian approximation is used
  because `tuning_curve_reliability` operates on per-trial rate correlations and the Gaussian
  assumption keeps the noise floor closed-form-tractable.
* The HWHM metric is evaluated analytically from the closed-form curve, not numerically from
  the sampled angles — the discrete 30° sampling would make a numerical estimate coarse.
* No paper-level literature review was performed (step 4 was skipped); parameter choices
  follow the task description rather than citation to specific direction-selective neuron
  measurements.

## Task Requirement Coverage

The operative task request from `task.json` and `task_description.md`:

> **Name**: Generate canonical target angle-to-AP-rate tuning curve.
>
> **Short description**: Analytically generate a canonical cosine-like target tuning curve to use as
> the optimisation reference for all later fits.
>
> **Scope**: produce a single dataset asset containing a cosine-like target tuning curve sampled at
> 12 or 24 angles around 360°; explicit generator parameters (preferred direction in deg, baseline
> rate in Hz, peak rate in Hz, tuning half-width / sharpness `n`, random seed); per-angle mean rates
> plus synthetic noisy trial replicates so `tuning_curve_reliability` has a ground-truth value.
>
> **Approach**: Python script under `code/` that generates the curve, writes CSV/JSON, writes the
> asset under `assets/dataset/`, and plots to `results/images/target_tuning_curve.png`.
>
> **Verification**: dataset passes `verify_dataset_asset.py`; `details.json` records generator
> params and seed; noisy-trial table has ≥ 10 trials per angle.

Requirements inherited from `plan/plan.md`:

| ID | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Dataset asset `target-tuning-curve` exists with v2 layout (details + description + files/) | Done | `assets/dataset/target-tuning-curve/details.json`, `description.md`, three files in `files/`; `verify_task_folder` PASSED with 1 non-blocking warning |
| REQ-2 | Curve sampled at 12 or 24 evenly-spaced angles | Done | `curve_mean.csv` has 12 rows at 0°/30°/…/330° (details.json `size_description`) |
| REQ-3 | Generator parameters explicit and recorded | Done | `details.json.generator_params` contains all 8 keys (`theta_pref_deg`, `r_base_hz`, `r_peak_hz`, `n`, `n_angles`, `n_trials`, `noise_sd_hz`, `random_seed`) plus `functional_form` and `dsi_closed_form`; `files/generator_params.json` mirrors the dataclass |
| REQ-4 | ≥ 10 trials per angle in the noisy-trial table | Done | `curve_trials.csv` has 240 rows = 12 × 20; verified by file length |
| REQ-5 | Mean-rate table with closed-form values per angle | Done | `curve_mean.csv` 12 rows, values match the formula (see Metrics Tables above); max absolute bias of sample means vs closed form is 1.063 Hz, well below `2 × σ / √n_trials ≈ 1.34 Hz` |
| REQ-6 | Closed-form DSI in [0.6, 0.9] | Done | DSI = **0.8824**, recorded in `metrics.json`, `details.json.generator_params.dsi_closed_form`, and asserted in `generate_target.py` (`assert 0.6 <= dsi <= 0.9`) |
| REQ-7 | Plot at `results/images/target_tuning_curve.png` | Done | File exists, 8×5 inches, 150 dpi; embedded in Visualizations above |
| REQ-8 | Dataset categories exist in `meta/categories/` | Done | `details.json.categories = ["direction-selectivity"]`; slug confirmed present under `meta/categories/` |

</details>
