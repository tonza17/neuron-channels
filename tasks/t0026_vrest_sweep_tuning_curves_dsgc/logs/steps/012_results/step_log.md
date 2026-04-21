---
spec_version: "3"
task_id: "t0026_vrest_sweep_tuning_curves_dsgc"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-04-21T17:17:59Z"
completed_at: "2026-04-21T17:27:35Z"
---
## Summary

Wrote `results_summary.md` and `results_detailed.md` for the V_rest sweep, embedding all 20 polar
and summary plots and quantifying per-model DSI, peak firing rate, and HWHM across the eight V_rest
values for both t0022 and t0024. Answered the five key questions from `task_description.md` using
the per-V_rest metrics tables and flagged three partial items (summary plot naming, metrics.json
shape, metric-key registration) in the Task Requirement Coverage and Limitations sections.

## Actions Taken

1. Read `results/metrics.json`, the per-V_rest metric CSVs, wall-time JSONs, `plan/plan.md`, and
   `task_description.md` to extract numeric evidence for every section of the results files.
2. Wrote `results/results_summary.md` with the mandatory Summary / Metrics / Verification sections
   and seven quantitative bullets (DSI ranges, peak firing ranges, HWHM ranges, total trials).
3. Wrote `results/results_detailed.md` with `spec_version: "2"` frontmatter and the six mandatory
   sections (Summary, Methodology, Visualizations, Analysis, Examples, Verification) plus
   Limitations, Files Created, and a 12-row Task Requirement Coverage table mapping each plan.md REQ
   to its evidence.
4. Ran `flowmark --inplace --nobackup` on both results markdown files to normalize formatting ahead
   of the pre-commit hook.

## Outputs

* `tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/results_summary.md`
* `tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/results_detailed.md`
* `tasks/t0026_vrest_sweep_tuning_curves_dsgc/logs/steps/012_results/step_log.md`

## Issues

No issues encountered. Three partial items were recorded in the Task Requirement Coverage and
Limitations sections of `results_detailed.md` for the reporting step to address: (a) the summary
plots are named `summary_<model>_vrest.png` instead of the `dsi_vs_vrest.png` /
`peak_hz_vs_vrest.png` names specified in `plan/plan.md` REQ-9; (b) `metrics.json` uses a map-shaped
`variants` block instead of the array form required by the multi-variant
`task_results_specification.md`; (c) the `dsi_at_vrest_<value>` and `peak_hz_at_vrest_<value>`
metric keys have not yet been registered under `meta/metrics/`.
