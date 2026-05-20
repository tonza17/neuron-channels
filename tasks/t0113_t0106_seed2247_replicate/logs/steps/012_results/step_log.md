---
spec_version: "3"
task_id: "t0113_t0106_seed2247_replicate"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-20T02:15:23Z"
completed_at: "2026-05-20T02:35:00Z"
---
# Step 12: results

## Summary

Spawned the results subagent to synthesise the gen-14 NSGA-II outcome into the full results package:
`results_summary.md`, `results_detailed.md`, `metrics.json`, two CSVs
(`joint_pass_summary_3seeds.csv`, `pareto_front_overlap_3seeds.csv`), five charts in
`results/images/`, and a one-stop 3-seed analysis script `code/build_t0113_results.py`. All seven
Key Questions from `task_description.md` answered with definite quantitative values, all five charts
embedded in `results_detailed.md` with descriptions. Verificators `verify_task_results` and
`verify_task_metrics` pass with zero errors and zero warnings.

## Actions Taken

1. Spawned a results subagent to execute step 12 with the full plan REQ context.
2. The subagent built `code/build_t0113_results.py` (one-stop analysis: loads t0106 / t0112 / t0113
   predictions assets, computes joint-pass summaries, Pareto-front nearest-neighbour distances in
   normalised parameter space, renders 5 charts).
3. The subagent wrote `results/metrics.json` (variant format with `direction_selectivity_index`
   sub-variants `best_legit`, `overall_max`, `dsi_eq_one_count`) and ran `verify_task_metrics`
   (PASSED).
4. The subagent wrote `results/data/joint_pass_summary_3seeds.csv` and
   `results/data/pareto_front_overlap_3seeds.csv` plus a helper `example_cells.json` capturing the
   10 representative cells embedded in `results_detailed.md`.
5. The subagent rendered 5 charts in `results/images/` and embedded all 5 in `results_detailed.md`
   with descriptions.
6. The subagent wrote `results/results_summary.md` (3 mandatory sections + 7 Key Questions answered)
   and `results/results_detailed.md` (all 7 mandatory sections including 10 concrete Examples with
   full 68-d input vectors and raw outputs in fenced JSON blocks, ending with
   `## Task Requirement Coverage`).
7. Ran `verify_task_results` (PASSED 0/0), `ruff check + format` on new code (PASSED), `mypy` on the
   new code (PASSED), `flowmark` on both markdown files.

## Outputs

* `results/results_summary.md` — 3.9 KB, 3 mandatory sections + 7 Key Question answers
* `results/results_detailed.md` — 33 KB, 7 mandatory sections + 10 Examples with full vectors
* `results/metrics.json` — registered `direction_selectivity_index` variant format
* `results/data/joint_pass_summary_3seeds.csv` — 3 rows (one per seed)
* `results/data/pareto_front_overlap_3seeds.csv` — 8 rows (one per t0113 Pareto cell)
* `results/data/example_cells.json` — 10 representative cells with full 68-d vectors
* `results/images/pareto_front_3seeds.png` (41 KB) — 3-seed Pareto fronts overlay
* `results/images/hv_vs_gen_3seeds.png` (68 KB) — log-scale HV trajectory
* `results/images/joint_pass_yield_per_gen_3seeds.png` (62 KB) — per-gen joint-pass discovery
* `results/images/top50_morphologies_seed2247.png` (74 KB) — best-available cells grid
* `results/images/asymmetry_distribution_3seeds.png` (54 KB) — 4-panel asymmetry histograms
* `code/build_t0113_results.py` — one-stop 3-seed analysis script

## Headline Findings (7 Key Question answers)

1. Joint-pass count bucket: 0 LEGIT cells; 2 asset-declared at DSI = 1.0 silence-guard (PD = 35.0
   and 45.24 Hz). Substrate-density bucket = "not populated"; asset-declared bucket = "sparse
   (1-6)".
2. Best DSI >= 0.95? NO — best legit = 0.3651 (62% below target).
3. Best PD >= 100 Hz? NO — best = 71.67 Hz (28% below target; cell has DSI = 0.0017, fires roughly
   equally in both directions).
4. 3-seed substrate-rate mean ± SE = 1.26% ± 1.01% (95% CI -0.73%, 3.25%). Point estimate 3x above
   Hay 2011 (0.40%) and 13x above Druckmann 2007 (0.10%); CI brackets both baselines so the 3-seed
   sample still cannot reject either literature value.
5. HV-plateau gen = 14 — OUTSIDE the t0106 (40) / t0112 (21) range on the early side. Gen 14 had a
   +26% HV jump from a silence-guard cell, suggesting possible premature trigger.
6. Per-gen wall-clock = 160 s/gen — 74% LOWER than t0112's 620 s/gen baseline. The gap is
   attributable to the 64-core EPYC selection vs t0112's 32-core EPYC, not the cadence-10 protocol
   per se.
7. Pareto overlap: 4 of 8 t0113 Pareto cells closer to t0106 (z-scored L2), 4 closer to t0112 —
   roughly equidistant. Mean z-scored L2 to t0106 = 10.5, to t0112 = 10.7.

## Issues

1. Initial mypy reported 14 errors from `dict[str, object]` and untyped `json.load` returns in the
   new `build_t0113_results.py`; resolved by narrowing the type and adding
   `assert isinstance(..., list)` guards. Final mypy: 0 errors.
2. Recomputed t0106 joint-pass count (136 unique) differed from the asset-declared 123. The summary
   CSV uses the asset-declared canonical values for cross-task consistency and recomputes only
   `best_legit_dsi` (which is not in the asset blocks). The discrepancy is documented in
   `results_detailed.md` `## Limitations`.
