---
spec_version: "3"
task_id: "t0110_relaxed_cohort_factor_analysis"
step_number: 8
step_name: "implementation"
status: "completed"
started_at: "2026-05-18T18:34:00Z"
completed_at: "2026-05-18T19:00:00Z"
---

# Step 8: implementation

## Summary

Implemented code/factor_analysis_relaxed.py: load t0106 evaluations, apply DSI>0.2 AND PD>3, dedupe by 68-d vector, run sklearn FactorAnalysis + manual varimax (reused from t0108), compute Pearson r vs DSI/PD, render side-by-side comparison + 68x10 loadings heatmap.

## Actions Taken

* Wrote code/factor_analysis_relaxed.py (~330 lines).
* Ran the pipeline: 3744 raw -> 1209 passing -> 247 unique cells.
* Eigenvalues > 1: 16; factors retained at Kaiser cap: 10.
* Sign counts: DSI 6 pos / 4 neg; PD 2 pos / 8 neg.
* Joint factor: F1 (r_DSI=-0.37, r_PD=-0.75) -- the joint failure axis.
* Wrote results/data/{filtered_cells,factor_analysis_relaxed}.json and results/images/{factor_correlations_comparison,factor_loadings_heatmap_relaxed}.png.

## Outputs

* results/data/filtered_cells.json (247 cells).
* results/data/factor_analysis_relaxed.json.
* results/images/factor_correlations_comparison.png.
* results/images/factor_loadings_heatmap_relaxed.png.

## Issues

* Initial summary doc had incorrect mean DSI / PD values; corrected after re-deriving from filtered_cells.json (DSI mean 0.669, PD mean 68.8 Hz).
