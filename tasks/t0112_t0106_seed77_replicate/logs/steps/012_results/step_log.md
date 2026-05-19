---
spec_version: "3"
task_id: "t0112_t0106_seed77_replicate"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-19T21:27:43Z"
completed_at: "2026-05-19T22:35:00Z"
---
# Step 12: Results

## Summary

Wrote `results_summary.md`, `results_detailed.md`, `metrics.json`, and produced 5 charts and 2 CSV
data tables that compare seed 77 against seed 44 across joint-pass count, frontier metrics, HV
trajectory, and morphology distributions. `verify_task_results` and `verify_task_metrics` both pass.
Headline numbers: 7 unique joint-pass cells (vs t0106's 123), best DSI 0.9535, best PD 114.76 Hz,
final HV 107.46, total spend $1.99 of $25 cap.

## Actions Taken

1. Wrote `code/build_t0112_results.py` — a single script that loads `all_evaluations_seed77.json.gz`
   and t0106's `all_evaluations_seed44.json.gz`, plus both Pareto front JSON files and HV
   trajectories, and produces 5 charts + 2 CSV tables in `results/images/` and `results/data/`.
2. Ran the script to produce `pareto_front_seed44_vs_seed77.png`, `hv_vs_gen_seed44_vs_seed77.png`,
   `joint_pass_yield_per_gen.png`, `top50_morphologies_seed77.png` (placeholder — only 7 unique
   cells, well below 50), and `asymmetry_distribution_seed44_vs_seed77.png`, plus
   `joint_pass_summary.csv` and `pareto_front_overlap.csv`.
3. Wrote `results/metrics.json` in the explicit-variant format with the registered project metric
   `direction_selectivity_index` for the single seed-77 variant.
4. Wrote `results/results_summary.md` answering the 5 key questions from the task brief.
5. Wrote `results/results_detailed.md` with Methodology, Metrics table, deltas vs t0106, embedded
   charts, Analysis, Examples (10 concrete cells), Limitations, Verification, Files Created, and the
   mandatory Task Requirement Coverage section (15 REQ items, all marked Done except REQ-13 which is
   Partial pending a normalised-distance follow-up).
6. Ran the verificators (`verify_task_results`, `verify_task_metrics`): both PASSED.

## Outputs

* `tasks/t0112_t0106_seed77_replicate/code/build_t0112_results.py`
* `tasks/t0112_t0106_seed77_replicate/results/metrics.json`
* `tasks/t0112_t0106_seed77_replicate/results/results_summary.md`
* `tasks/t0112_t0106_seed77_replicate/results/results_detailed.md`
* `tasks/t0112_t0106_seed77_replicate/results/images/pareto_front_seed44_vs_seed77.png`
* `tasks/t0112_t0106_seed77_replicate/results/images/hv_vs_gen_seed44_vs_seed77.png`
* `tasks/t0112_t0106_seed77_replicate/results/images/joint_pass_yield_per_gen.png`
* `tasks/t0112_t0106_seed77_replicate/results/images/top50_morphologies_seed77.png`
* `tasks/t0112_t0106_seed77_replicate/results/images/asymmetry_distribution_seed44_vs_seed77.png`
* `tasks/t0112_t0106_seed77_replicate/results/data/joint_pass_summary.csv`
* `tasks/t0112_t0106_seed77_replicate/results/data/pareto_front_overlap.csv`

## Issues

* The first chart-builder iteration computed the strict Pareto front in-script with an inverted
  dominance check (it marked dominators rather than dominated as non-Pareto). Caught when the
  overlap CSV showed (0, 0) Pareto cells with huge L2 distances; switched the chart code to read the
  canonical `pareto_front_seed44.json` and `pareto_front_seed77.json` files that the NSGA-II driver
  writes. Final charts use the driver-blessed Pareto sets.
* The raw 68-d L2 distance in `pareto_front_overlap.csv` is dominated by conductance-scale
  parameters spanning 6 orders of magnitude; the CSV is produced as required by REQ-13 but its
  numerical interpretation is deferred to a future normalised-distance follow-up. This is noted
  explicitly in `results_detailed.md` and is the only Partial entry in the Task Requirement Coverage
  table.
