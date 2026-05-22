---
spec_version: "3"
task_id: "t0117_pooled_pca_cluster_factor_all_cells_4_seeds"
step_number: 10
step_name: "results"
status: "completed"
started_at: "2026-05-22T12:52:43Z"
completed_at: "2026-05-22T12:56:31Z"
---
# Step 10: results

## Summary

Wrote the canonical results documents for t0117. `results/results_summary.md` (scannable 1-page
summary with headline numbers and verificator outcomes), `results/results_detailed.md` (the
exhaustive `spec_version: "2"` document with all mandatory sections, 9 charts embedded, the
`## Examples` section with 10 input-output pairs that explicitly contrast high-quality and
low-quality cells across the cohort boundary, and the `## Task Requirement Coverage` table marking
every one of the 17 REQ-* items from `plan/plan.md` as `Done`), plus `costs.json` (zero-cost) and
`remote_machines_used.json` (`[]`). The new "Comparison vs t0116 (head-to-head)" subsection
explicitly contrasts pool sizes, k chosen, NMI / silhouette, factor structure, and per-seed
displacement, and gives a plain-English verdict for each of the three answer-asset questions.
`results/metrics.json = {}` was already written during implementation; the empty value is
intentional and documented in both the methodology notes and the detailed-results limitations.

## Actions Taken

1. Ran `prestep` for the `results` step.
2. Read `arf/specifications/task_results_specification.md` (mandatory sections, `## Examples`
   requirement, `## Task Requirement Coverage`), the plan, the methodology notes, and every
   result-data CSV (`per_seed_pool_counts`, `gen0_displacement`, `cluster_seed_purity`,
   `factor_correlations`, `t0116_comparison`, plus all 5 morphology cluster representative CSVs).
   Verified that every quoted number in the markdown matches the JSON / CSV source exactly.
3. Wrote `results/results_summary.md` with the three mandatory sections and 11 quantified metric
   bullets covering pool size, cluster purity, factor structure (with explicit joint-factor
   highlight), and per-seed displacement.
4. Wrote `results/results_detailed.md` with all 6 mandatory sections plus recommended sections
   `## Methodology Notes`, `## Cohort Composition`, `## Visualizations`, `## Cluster Composition`,
   `## Factor Analysis`, `## Gen-0 Displacement`, `## Comparison vs t0116 (head-to-head)`, and
   `## Examples` (10 cell-level input-output pairs explicitly contrasting high-quality and
   low-quality cells).
5. Wrote `results/costs.json` and `results/remote_machines_used.json`.
6. Ran `flowmark --inplace --nobackup` on every touched markdown file and re-ran
   `verify_task_results` to confirm the results pass.

## Outputs

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/results_summary.md`
* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/results_detailed.md`
* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/costs.json`
* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/remote_machines_used.json`
* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/logs/commands/` — `run_with_logs`
  captures of the flowmark calls

## Issues

No issues encountered.
