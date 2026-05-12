---
spec_version: "3"
task_id: "t0102_seedscale_n4_gen20"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-12T19:25:00Z"
completed_at: "2026-05-12T19:55:00Z"
---
# Step 12: results

## Summary

Wrote all task-results artifacts per `arf/specifications/task_results_specification.md` v8:
`results_summary.md`, `results_detailed.md` (spec_version "2"), `metrics.json` (two-variant explicit
format), and verified that `costs.json` ($12.0733) and `remote_machines_used.json` (machine
36556586, 24.842 h) already in place from the implementation/teardown steps. Generated four PNG
charts in `results/images/` via `code/make_charts.py` and embedded all of them in
`results_detailed.md` `## Visualizations`. Ran `verify_task_results` and `verify_task_metrics`
against the task. Reported 0 strict joint-pass cells in both seeds, identified the floating-point
DSI = 1.0 silenced-cell artifact, reframed t0091's joint-pass cell as a single-mutation descendant
of the alt_topology anchor, and produced 10 concrete cell examples covering the bimodal extremes,
diagonal candidates, random samples, and failure modes.

## Actions Taken

1. Read `task.json`, `plan/plan.md` (REQ-1 .. REQ-16), `results/creative_analysis.md`,
   `results/data/all_evaluations_seed{44,55}.json`, `results/data/hv_trajectory_seed{44,55}.json`,
   `results/costs.json`, `results/remote_machines_used.json`, the two predictions assets'
   `description.md`, `logs/steps/008_setup-machines/machine_log.json`, and
   `logs/steps/009_implementation/{step_log.md,smoke_gate_5anchor_remote.json}`.
2. Wrote `tasks/t0102_seedscale_n4_gen20/code/make_charts.py` (a single 250-line script that reads
   the per-seed JSONL predictions and HV-trajectory JSON files and writes four PNG charts).
3. Ran
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0102_seedscale_n4_gen20 -- uv run python -u -m tasks.t0102_seedscale_n4_gen20.code.make_charts`.
   Generated `results/images/dsi_vs_pd_scatter.png`, `hv_trajectory.png`, `dsi_pd_density.png`, and
   `per_gen_best_dsi_pd.png`.
4. Wrote `results/metrics.json` in explicit-variant format with variants `random-init-seed44` and
   `random-init-seed55`. Only `direction_selectivity_index` is populated (the t0099 substrate
   evaluator does not export per-cell `tuning_curve_*` metrics; this matches t0099's pattern).
5. Wrote `results/results_summary.md` (~ 250 words) with the mandatory `## Summary`, `## Metrics`,
   `## Verification` sections.
6. Wrote `results/results_detailed.md` (~ 3,500 words) with YAML frontmatter `spec_version: "2"` and
   all mandatory sections: Summary, Methodology, Verification, Limitations, Files Created, Task
   Requirement Coverage, plus the experiment-type-mandatory `## Examples` (10 concrete cells with
   their full 68-d vectors), `## Comparison vs Baselines`, `## Visualizations`, `## Analysis`.
7. Ran `uv run flowmark --inplace --nobackup` on `results_summary.md` and `results_detailed.md`.
8. Ran `uv run ruff check --fix tasks/t0102_seedscale_n4_gen20/code/make_charts.py` and
   `uv run ruff format tasks/t0102_seedscale_n4_gen20/code/make_charts.py`.
9. Ran `uv run mypy -p tasks.t0102_seedscale_n4_gen20.code`.
10. Ran `verify_task_results t0102_seedscale_n4_gen20` and
    `verify_task_metrics t0102_seedscale_n4_gen20` via `run_with_logs`.

## Outputs

* `tasks/t0102_seedscale_n4_gen20/results/results_summary.md` (~ 250 words).
* `tasks/t0102_seedscale_n4_gen20/results/results_detailed.md` (~ 3,500 words, spec_version "2").
* `tasks/t0102_seedscale_n4_gen20/results/metrics.json` (two-variant explicit format).
* `tasks/t0102_seedscale_n4_gen20/results/images/dsi_vs_pd_scatter.png`.
* `tasks/t0102_seedscale_n4_gen20/results/images/hv_trajectory.png`.
* `tasks/t0102_seedscale_n4_gen20/results/images/dsi_pd_density.png`.
* `tasks/t0102_seedscale_n4_gen20/results/images/per_gen_best_dsi_pd.png`.
* `tasks/t0102_seedscale_n4_gen20/code/make_charts.py` (chart-generation script).

## Issues

* `metrics.json` populates only `direction_selectivity_index` (1 of 4 registered metrics). The t0099
  substrate's evaluator does not produce per-cell `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, or `tuning_curve_rmse`; deriving them from the per-cell history would
  require re-running the evaluator on the saved 68-d vectors, which is out of scope for the results
  step (and matches t0099's pattern of reporting only `direction_selectivity_index`). Marked REQ-13
  as `Partial` in `results_detailed.md` `## Task Requirement Coverage`.
* The headline `direction_selectivity_index = 1.0` reflects the silenced-cell floating-point
  artifact described in Finding 1 of `results_detailed.md` `## Analysis`. Downstream consumers must
  read the limitations note to interpret the value correctly.
