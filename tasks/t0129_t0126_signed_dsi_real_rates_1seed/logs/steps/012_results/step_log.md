---
spec_version: "3"
task_id: "t0129_t0126_signed_dsi_real_rates_1seed"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-26T19:59:55Z"
completed_at: "2026-05-26T20:38:00Z"
---
# Step 12: results

## Summary

Spawned a results subagent that built all four required charts
(`pareto_front_dsi_signed_vs_atp.png`, `dsi_signed_distribution.png`, `pd_vs_nd_rate_scatter.png`,
`pareto_t0126_vs_t0129_overlay.png`), wrote `results/metrics.json` (3-variant explicit format
covering the headline Pareto cell, Pareto-median, and the t0126-vs-t0129 sign-flip comparison),
`results/results_summary.md`, `results/results_detailed.md` (with all 11 mandatory sections
including ≥10 concrete cell examples from `cell_params.jsonl`), and the two expected assets
(`assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/` and
`assets/answer/does-signed-dsi-change-t0126-pareto-structure/`). `verify_task_results`,
`verify_task_metrics`, and `verify_task_folder` all passed with 0 errors.

REQ-20 (count of t0126-Pareto cells whose `dsi_vector_sum > 0.5` but `dsi_signed < 0`) is marked
**PARTIAL** — the upper bound is 4 (cells with `dsi_vector_sum > 0.5` in t0126's Pareto front),
but the true count is **unknowable** from t0126 artefacts because t0126 did not persist
per-direction spike counts and its `pd_rate_hz = 40` is a synthesised placeholder per project memory
`project_t0126_cell_trace_synthesised`. Documented in `results_detailed.md` Comparison section, the
answer asset full_answer.md, and the metrics.json `sign_flip_count_provenance` dimension. Resolution
requires re-running t0126's seed 8929 with the t0129 evaluator — captured as suggestion
**S-0129-01** (high priority).

## Actions Taken

1. Ran `prestep results`.
2. Spawned the results subagent. Subagent wrote `code/build_t0129_charts.py` (chart-generation
   script using matplotlib), generated all four PNGs into `results/images/`, computed
   Pareto-aggregate metrics, and assembled the results documents.
3. Subagent created the predictions asset folder
   (`assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/`) with `details.json` (spec
   v2), `description.md`, `files/predictions-pareto-9-cells.jsonl`, and
   `files/predictions-all-cells.jsonl.gz`.
4. Subagent created the answer asset folder
   (`assets/answer/does-signed-dsi-change-t0126-pareto-structure/`) with `details.json` (spec v2),
   `short_answer.md`, and `full_answer.md`.
5. Subagent ran `verify_task_results`, `verify_task_metrics`, `verify_task_folder`, `ruff check`,
   `ruff format`, `mypy --explicit-package-bases` — all PASS.
6. Subagent committed in 5 logical commits: charts, metrics, assets, results docs, command logs.

## Outputs

* `tasks/t0129_*/results/results_summary.md`
* `tasks/t0129_*/results/results_detailed.md` (spec_version 2, all 11 sections, 10+ examples,
  REQ-1..REQ-23 coverage table)
* `tasks/t0129_*/results/metrics.json` (3-variant explicit format)
* `tasks/t0129_*/results/images/pareto_front_dsi_signed_vs_atp.png`
* `tasks/t0129_*/results/images/dsi_signed_distribution.png`
* `tasks/t0129_*/results/images/pd_vs_nd_rate_scatter.png`
* `tasks/t0129_*/results/images/pareto_t0126_vs_t0129_overlay.png`
* `tasks/t0129_*/assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/`
* `tasks/t0129_*/assets/answer/does-signed-dsi-change-t0126-pareto-structure/`
* `tasks/t0129_*/code/build_t0129_charts.py`
* `tasks/t0129_*/logs/steps/012_results/step_log.md`

## Issues

REQ-20 marked PARTIAL — see Summary. Step log was missing from the original results-step commit
(subagent committed `[results]: command + step logs` covering command transcripts only); this file
was backfilled post-merge to clear `LG-E008` reported by `verify_task_complete` after the worktree
was removed.
