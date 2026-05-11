---
spec_version: "3"
task_id: "t0103_extract_baden_2016_ds_morphologies"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-11T22:57:56Z"
completed_at: "2026-05-12T01:30:00Z"
---
# results

## Summary

Wrote all five results artefacts: `results_summary.md`, `results_detailed.md`, `metrics.json` (empty
— no registered project metric applies to this extraction task), `costs.json` (zero, local only),
and `remote_machines_used.json` (empty). The detailed results file ends with a
`## Task Requirement Coverage` table that maps every REQ-* item in the plan to its evidence path.

## Actions Taken

1. Ran prestep for the `results` step.
2. Sampled the produced Parquet (1,238 × 40) to compute per-group selectivity and RF-diameter
   summary statistics; pulled five representative per-cell records (G2, G12 × 2, G16, and the
   loading recipe).
3. Confirmed via `aggregate_metrics --format ids` that none of the four registered project metrics
   (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
   `tuning_curve_rmse`) is produced by this extraction task — `metrics.json` is therefore `{}`.
4. Wrote `results_summary.md` (2-3 sentence summary + headline metrics + verification check list).
5. Wrote `results_detailed.md` with all mandatory sections including `## Examples` (5 concrete
   per-cell records and a loading recipe), `## Analysis`, `## Limitations`, and
   `## Task Requirement Coverage` (12 REQs all done).
6. Wrote `costs.json = {"total_cost_usd": 0, "breakdown": {}}` and `remote_machines_used.json = []`.
7. Cross-checked every number in the results markdown against the Parquet and against
   `code/group_count_check.json` — all numbers match exactly.

## Outputs

* `tasks/t0103_extract_baden_2016_ds_morphologies/results/results_summary.md`
* `tasks/t0103_extract_baden_2016_ds_morphologies/results/results_detailed.md`
* `tasks/t0103_extract_baden_2016_ds_morphologies/results/metrics.json`
* `tasks/t0103_extract_baden_2016_ds_morphologies/results/costs.json`
* `tasks/t0103_extract_baden_2016_ds_morphologies/results/remote_machines_used.json`
* `tasks/t0103_extract_baden_2016_ds_morphologies/logs/steps/012_results/step_log.md`

## Issues

No issues encountered.
