---
spec_version: "3"
task_id: "t0116_pooled_pca_cluster_factor_dsi07_pd10"
step_number: 10
step_name: "results"
status: "completed"
started_at: "2026-05-21T20:10:34Z"
completed_at: "2026-05-21T20:15:05Z"
---
# Step 10: results

## Summary

Wrote the canonical results documents for t0116. `results/results_summary.md` (the scannable 1-page
summary with the headline metrics and verificator outcomes) and `results/results_detailed.md` (the
exhaustive `spec_version: "2"` document with mandatory sections, all 8 charts embedded, the
`## Examples` section with 10 cell-level input-output pairs spanning the 3 morphology clusters and 4
source seeds, and the `## Task Requirement Coverage` table marking every one of the 17 REQ-* items
from `plan/plan.md` as `Done`). Also wrote `results/costs.json` (zero-cost task) and
`results/remote_machines_used.json` (`[]`). `results/metrics.json = {}` was already produced during
implementation; the empty value is intentional and is documented in both the methodology notes and
the detailed results' `## Limitations`.

## Actions Taken

1. Ran `prestep` for the `results` step.
2. Read `arf/specifications/task_results_specification.md` (sections on `results_summary.md`,
   `results_detailed.md`, mandatory `## Examples`, `## Task Requirement Coverage`), the plan, the
   methodology notes, and the result-data CSVs to ensure every quoted number matched its source.
3. Wrote `results/results_summary.md` with the three mandatory sections (`## Summary`, `## Metrics`,
   `## Verification`) and 10 quantified metric bullets.
4. Wrote `results/results_detailed.md` with all 6 mandatory sections (`## Summary`,
   `## Methodology`, `## Verification`, `## Limitations`, `## Files Created`,
   `## Task Requirement Coverage`), plus the recommended `## Methodology Notes`,
   `## Cohort Composition`, `## Visualizations`, `## Cluster Composition`,
   `## Factor Analysis: Per-Factor Variance and DSI / PD Correlations`, `## Gen-0 Displacement`, and
   `## Examples` (10 cell-level input-output pairs as required for data-analysis-typed tasks).
5. Wrote `results/costs.json` (`total_cost_usd: 0`, empty `breakdown`, explanatory note) and
   `results/remote_machines_used.json` (`[]`).
6. Ran `flowmark --inplace --nobackup` on every touched markdown file, then verified the result
   files against the spec.

## Outputs

* `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/results_summary.md`
* `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/results_detailed.md`
* `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/costs.json`
* `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/remote_machines_used.json`
* `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/logs/commands/` — flowmark `run_with_logs`
  captures

## Issues

No issues encountered.
