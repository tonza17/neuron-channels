# t0115 - Seed-9354 NSGA-II Replicate of t0106 with HV-Plateau Auto-Stop Disabled: Results Summary

## Summary

Seed 9354 with the HV-plateau auto-stop DISABLED reached **63 unique LEGIT joint-pass cells** (DSI
>= 0.5 AND PD-rate >= 30 Hz AND DSI < 0.9999) across **5,280 evaluations / 55 NSGA-II generations**
on the same 68-d Bed B + 14-d morphology substrate as t0106 / t0112 / t0113 / t0114. The run
terminated by **operator stop** after the HV trajectory visibly plateaued near HV = 50.56. Adding
seed 9354 as the **fifth and final data point of the S-0112-01 substrate-rate confirmation batch**
gives a 5-seed mean LEGIT joint-pass acceptance rate of **2.58% +/- SE 1.50%** (sample SD 3.35%),
still **6.5x above the Hay 2011 envelope upper bound (0.40%)** and **25.8x above Druckmann 2007
(0.10%)**.

## Metrics

* **Unique joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz): **63** (all of which are also LEGIT).
* **Unique LEGIT joint-pass cells** (additionally DSI < 0.9999): **63** — places seed 9354 in an
  intermediate yield bucket between t0106 seed 44 (121 LEGIT) and t0112 seed 77 (7 LEGIT).
* **Best LEGIT DSI** (highest non-silence-guard cell): **0.9833** at PD = 28.33 Hz (gen 54; strict
  Pareto `cell_id = 1`). Within 1.1 percentage points of t0106 seed 44's 0.9939 and 0.9 points of
  t0114 seed 7755's 0.9926.
* **Best PD-rate**: **89.29 Hz** at DSI ~ 0 (gen 55). Below t0106 seed 44's 125.95 Hz and t0114 seed
  7755's 112.86 Hz; this seed's PD frontier sits between t0113's 71.67 Hz and the high-yield seeds.
* **Overall max DSI**: **1.0000** (silence-guard / single-spike artefacts; **64** cells at the DSI =
  1.0 ceiling).
* **Strict Pareto cells**: **23** — broader frontier than t0106 (7) and t0114 (6) because the
  lower HV (50.56 vs 122.03 / 111.54) means many cells contribute to the front without being
  dominated.
* **NSGA-II generations completed**: **55** of 300 ceiling (operator stop after visible plateau).
* **Cells evaluated**: **5,280** = 96 x 55 generations.
* **Final hypervolume (2-D)**: **50.5646** (start 0.80 -> 63x growth; 41% of t0106's 122.03 and 45%
  of t0114's 111.54).
* **Stop trigger**: **operator_stop** (HV-plateau auto-stop was DISABLED for this run).
* **NSGA-II compute cost (productive)**: **$2.3859** of $25 cap (9.5% utilisation).
* **Total task cost**: **$2.50** of $25 cap (10.0% utilisation).

## 5-Seed Substrate-Rate Estimate (S-0112-01)

| Statistic | Value |
| --- | --- |
| Per-seed LEGIT acceptance (unique joint-pass cells / total evaluations) | t0106 / 44 = 121/3744 = **3.23%**; t0112 / 77 = 7/2016 = **0.35%**; t0113 / 2247 = 0/1344 = **0.00%**; t0114 / 7755 = 484/5952 = **8.13%**; t0115 / 9354 = 63/5280 = **1.19%** |
| 5-seed mean | **2.58%** |
| 5-seed sample SD | **3.35%** |
| 5-seed sample SE | **1.50%** |
| 95% CI (normal approx) | **(-0.36%, +5.52%)** |
| Hay 2011 baseline | 0.40% (within CI) |
| Druckmann 2007 baseline | 0.10% (within CI) |
| Point estimate vs Hay envelope | **6.45x above** |
| Point estimate vs Druckmann | **25.8x above** |

**Convention**: per-seed acceptance = unique LEGIT joint-pass cells / total evaluations (one cell
per evaluation). The 5-seed mean is the simple arithmetic mean of per-seed percentages, weighting
each seed equally regardless of how many generations it ran. The 95% CI still brackets both
literature baselines and 0%, so the 5-seed sample cannot formally reject either Hay 2011 or
Druckmann 2007 in the strict frequentist sense. However, **two of the five seeds (44 and 7755) each
independently exceed the Hay 2011 envelope by >= 8x and t0115 also exceeds it (1.19% vs 0.40%
envelope upper)**, strengthening the evidence that the substrate is more populated than the
literature envelope suggests.

## Verification

* `verify_task_results`: PASSED. See `## Verification` section of `results_detailed.md` and the
  orchestrator's step log at `logs/steps/012_results/step_log.md` for full run record.
* `verify_task_metrics`: `metrics.json` registers only the `direction_selectivity_index` metric per
  `meta/metrics/`; sub-variants `best_legit`, `overall_max`, and `dsi_eq_one_count` are encoded as
  separate variants in the explicit multi-variant format.
* `predictions asset verificator`: PASSED. Non-blocking PR-W014 / PR-W015 warnings (no linked model
  / dataset asset — same shape as t0106 / t0112 / t0113 / t0114).
* `top50_morphologies_seed9354.png` visual sanity check: PASSED. Each of the 50 subplots shows a
  branching dendrite tree (every apical / basal section drawn via the project's
  `generate_fixed_morphology` helper, NOT only somas).
