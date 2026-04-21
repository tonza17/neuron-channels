---
spec_version: "3"
task_id: "t0024_port_de_rosenroll_2026_dsgc"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-04-21T07:19:15Z"
completed_at: "2026-04-21T07:35:00Z"
---
## Summary

Wrote the full results bundle for the de Rosenroll 2026 DSGC port: `results_summary.md`,
`results_detailed.md` (with cross-model comparison vs t0008/t0020/t0022/t0023, per-angle metrics
tables, REQ-5 mechanistic root-cause analysis, and >=10 trial-level examples), `costs.json` (zero,
local-only run), `remote_machines_used.json` (empty), and a placeholder `suggestions.json` to be
populated by step 14. Linked the four polar/Cartesian PNGs in `results_detailed.md`. Recorded the
REQ-5 port-fidelity miss as a first-class finding (gate failed on all three sub-criteria; mechanism:
per-terminal Exp2Syn driver does not capture the spatially-distributed SAC release correlation
needed to reproduce the de Rosenroll correlation-drop effect) and surfaced the t0023 unavailability
(intervention_blocked, deferred pending t0022) as a known gap in REQ-6 cross-comparison coverage.

## Actions Taken

1. Aggregated cross-model metric data via
   `aggregate_metric_results.py --task-ids t0008/t0020/t0022/t0023` and
   `aggregate_tasks.py --status completed`; confirmed t0023 is `intervention_blocked` and could not
   contribute a row.
2. Sampled per-angle, best-PD, worst-PD, null-silence, and null-breakthrough trials directly from
   the four `data/tuning_curves_*.csv` files with pandas to construct the `## Examples` section.
3. Wrote `results/results_summary.md` (>=80 words, >=3 metric bullets, verification block).
4. Wrote `results/results_detailed.md` with frontmatter `spec_version: "2"`, all 6 mandatory
   sections plus Metrics Tables, Comparison vs Baselines, Analysis, Visualizations, Examples (>=10
   individual examples for the experiment-task `## Examples` requirement), Limitations, Files
   Created, and Task Requirement Coverage covering REQ-1..REQ-6.
5. Wrote `results/costs.json` (zero, local-only sweep), `results/remote_machines_used.json` (empty),
   `results/suggestions.json` (empty placeholder for step 14).
6. Ran `uv run flowmark --inplace --nobackup` on the two markdown files; ruff and mypy already clean
   on `code/` from step 9.

## Outputs

* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/results_summary.md`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/results_detailed.md`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/costs.json`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/remote_machines_used.json`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/suggestions.json` (placeholder, step 14 fills)

## Issues

REQ-6 cross-comparison cannot include t0023 (Hanson port) because t0023 has status
`intervention_blocked` (`intervention/deferred_pending_t0022.md`). Documented as a partial-coverage
note in the Task Requirement Coverage table; the Hanson row will need to be retrofitted into a
future cross-comparison task once t0023 executes. REQ-5 port-fidelity gate fails on all three
sub-criteria — recorded as a first-class finding per plan step 13, not a step blocker.
