---
spec_version: "3"
task_id: "t0107_t0106_polar_8dir_recheck"
step_number: 10
step_name: "results"
status: "completed"
started_at: "2026-05-18T11:20:42Z"
completed_at: "2026-05-18T11:25:00Z"
---

# Step 10: results

## Summary

Wrote `results_summary.md`, `results_detailed.md`, `metrics.json`. `costs.json` and
`remote_machines_used.json` were already produced in the implementation step's Vast.ai
teardown. Headline: Spearman ρ(t0106 2-dir ratio DSI, t0107 8-dir vsum DSI) = 0.758 (p = 0.011,
n = 10); mean DSI gap = +0.42 (t0106 always higher). Registered metric
`direction_selectivity_index` = 0.519 (mean 8-dir vsum across the 10 cells).

## Actions Taken

1. Computed headline stats via scipy.stats.spearmanr / pearsonr on the per-cell
   evaluations JSON; recorded ranks, individual DSI values, and per-direction firing rates.
2. Wrote `metrics.json` in the variant format with one variant
   (`eight-dir-vsum-recheck-top10-t0106`) and the registered metric value.
3. Wrote `results_summary.md` (Summary, Metrics, Verification, Figures, Headline
   interpretation).
4. Wrote `results_detailed.md` with all mandatory sections including 10 example cells in
   fenced code blocks, methodology, per-cell results table, three-group analysis, limitations,
   verification, files created, and Task Requirement Coverage as the last section.

## Outputs

* `results/metrics.json`
* `results/results_summary.md`
* `results/results_detailed.md`

## Issues

No issues.
