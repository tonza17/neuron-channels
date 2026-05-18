---
spec_version: "2"
task_id: "t0110_relaxed_cohort_factor_analysis"
date_completed: "2026-05-18"
---

# t0110 — Relaxed-Cohort Factor Analysis: Results Summary

## Summary

Re-ran the t0108 varimax factor analysis on t0106 cells at a less-truncated cohort
(DSI > 0.2 AND PD > 3 Hz, **N=247** vs t0108's 150). The truncated-cohort hypothesis is
confirmed: at the relaxed threshold **2 of 10 factors now have positive r(PD)** (F2 +0.14,
F4 +0.05), whereas t0108 had 0 / 10. DSI sign distribution also flips: 6 positive vs 4 negative
in t0110 (vs 4/6 in t0108). The dominant axis F1 (NAP_MID, CAT, SK_MID, CAD_TAUR, RA_OHM_CM)
is now revealed as a **joint suppressor** of both objectives (r_DSI = −0.37, r_PD = −0.75),
not just a PD-dropper as t0108 suggested.

## Metrics

* Cohort: t0106 only, filter DSI > 0.2 AND PD > 3.
* **N raw evaluations**: 3,744.
* **N passing filter**: 1,209.
* **N unique (deduped at 6 decimals)**: **247**.
* Mean DSI in cohort: 0.669 (range 0.20 – 1.00).
* Mean PD-rate: 68.8 Hz (range 3.10 – 125.95 Hz).
* Eigenvalues > 1: **16** (vs 18 in t0108).
* Factors retained (Kaiser cap = 10): **10**.
* **DSI sign counts**: 6 positive, 4 negative (t0108: 4 pos, 6 neg).
* **PD sign counts**: 2 positive (F2 +0.136, F4 +0.048), 8 negative (t0108: 0 pos, 10 neg).
* **Joint factors** (|r_DSI| > 0.3 AND |r_PD| > 0.3): **F1** (r_DSI = −0.37, r_PD = −0.75).
* `direction_selectivity_index` (cohort mean DSI) = **0.669**.

## Verification

* `verify_task_complete` passes with 0 errors.
* All four output files exist and embed in `results_detailed.md`:
  `results/data/filtered_cells.json`, `results/data/factor_analysis_relaxed.json`,
  `results/images/factor_correlations_comparison.png`,
  `results/images/factor_loadings_heatmap_relaxed.png`.
* The numbers reported here match the JSON outputs exactly.
* `costs.json` = 0 USD; `remote_machines_used.json` = `[]`.

## Figures

* `results/images/factor_correlations_comparison.png` — side-by-side bar chart of factor-outcome
  correlations: t0108 strict cohort (left) vs t0110 relaxed cohort (right), same y-axis.
* `results/images/factor_loadings_heatmap_relaxed.png` — 68 × 10 varimax loadings heatmap for the
  relaxed cohort.

## Headline interpretation

The all-negative PD column in t0108 was a **truncated-cohort artifact**, not a fundamental
property of the parameter space. At the relaxed threshold, two factors emerge with positive
r(PD), and the dominant "fall off the corner" axis F1 reveals itself as a joint suppressor of
both DSI and PD rather than the PD-only dropper t0108 suggested. The strict cohort masked the
DSI effect because all 150 cells were already near the DSI ceiling.

The new joint factor (in the strict-cohort sense — |r_DSI| > 0.3 AND |r_PD| > 0.3) is F1, with
both signs negative. There is no relaxed-cohort analogue of t0108's F10 (the DSI-up / PD-down
trade-off axis) at the |r| > 0.3 threshold, but F5 (r_DSI = +0.29, r_PD = −0.10) is its closest
neighbour and carries similar loadings (branch_length_cv, W_ACH−, GNMDA+, morph_seed−,
BK_SOMA+).
