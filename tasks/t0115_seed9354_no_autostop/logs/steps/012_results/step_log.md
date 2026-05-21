---
spec_version: "3"
task_id: "t0115_seed9354_no_autostop"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-21T02:18:01Z"
completed_at: "2026-05-21T02:45:00Z"
---
# Step 12: results

## Summary

Built the complete t0115 results stage in two inline analysis scripts: `code/build_results.py`
(charts, CSVs, predictions asset, metrics.json) and `code/build_top50_morphologies.py` (top-50
morphology grid with FULL DENDRITE TREES, addressing operator feedback that t0114's morphology grid
was wrong). Produced the predictions asset (gzipped JSONL of all 5,280 per-cell evaluations plus
`details.json` + `description.md`), `results/metrics.json` (explicit multi-variant format with three
`direction_selectivity_index` sub-variants), three CSV tables (`joint_pass_summary_5seeds.csv`,
`pareto_front_overlap_5seeds.csv`, `substrate_rate_5seed.csv`), five charts in `results/images/`,
`results_summary.md`, and `results_detailed.md`. All three required verificators PASS.

## Headline Numbers

* `task_seed = 9354`
* `n_total_evals = 5280`
* `n_generations_completed = 55` of 300 (operator stop after HV plateau)
* `n_joint_pass_unique = 63`
* `n_joint_pass_legit_unique = 63` (all joint-pass are LEGIT)
* `best_legit_dsi = 0.9833` at PD = 28.33 Hz (gen 54, Pareto cell_id 1)
* `overall_max_dsi = 1.0000` (silence-guard ceiling)
* `n_dsi_eq_one = 64`
* `best_pd_rate_hz = 89.29` at DSI ~ 0 (gen 55)
* `final_hypervolume = 50.5646`
* `stop_trigger = operator_stop`
* `n_pareto = 23`

## 5-Seed Substrate-Rate Estimate (S-0112-01)

* t0106 / 44: 121 / 3744 = **3.23%**
* t0112 / 77: 7 / 2016 = **0.35%**
* t0113 / 2247: 0 / 1344 = **0.00%**
* t0114 / 7755: 484 / 5952 = **8.13%**
* t0115 / 9354: 63 / 5280 = **1.19%**
* **Mean = 2.58%, sample SD = 3.35%, sample SE = 1.50%**
* 95% CI (normal approx): (-0.36%, +5.52%)
* Hay 2011 baseline = 0.40% (within CI; mean is 6.45x above)
* Druckmann 2007 baseline = 0.10% (within CI; mean is 25.8x above)

## Verificator Outcomes

* `verify_task_results`: **PASSED** (0 errors, 0 warnings).
* `verify_task_metrics`: **PASSED** (0 errors, 0 warnings).
* `meta.asset_types.predictions.verificator --task-id t0115_seed9354_no_autostop`: **PASSED** (0
  errors, 2 non-blocking warnings: PR-W014 `model_id is null` and PR-W015 `dataset_ids is empty` —
  same shape as t0106 / t0112 / t0113 / t0114).
* **`top50_morphologies_seed9354.png` visual sanity check**: **PASSED**. Saved PNG (315 KB) was
  directly read into the Read tool and visually verified: every one of the 50 subplots renders a
  branching dendrite tree drawn via `generate_fixed_morphology` + `LineCollection` from
  `result.section_endpoints_xy`, NOT a single soma dot. This addresses the operator's explicit
  feedback that t0114's morphology grid was wrong.

## Actions Taken

1. Inspected t0114's results stage (`build_results.py`, `build_morphology_charts.py`,
   `results_summary.md`, `results_detailed.md`, `metrics.json`) as the template.
2. Inspected the t0115 input data: `all_evaluations_seed9354.json` (5,280 cells across 55 gens),
   `hv_trajectory_seed9354.json` (55 entries, final HV 50.5646).
3. Forked t0114's `build_results.py` to t0115 with the analysis expanded from 4-seed to 5-seed
   coverage. Replaced the S-0113-03 detector-replay artefacts (already analysed in t0114) with a
   substrate-rate confirmation analysis: 5-seed mean, SD, SE acceptance rates with Hay 2011 and
   Druckmann 2007 literature comparison.
4. Wrote a NEW standalone script `code/build_top50_morphologies.py` that uses the
   `generate_fixed_morphology` helper (same as t0099 / t0102 / t0103) to draw every dendrite section
   of every cell in the top-50 grid. Direct PNG read confirms branching trees in each subplot.
5. Built the predictions asset `assets/predictions/t0115-bedb-morph-nsga2-seed9354/` with
   `details.json` (`spec_version: "2"`, `prediction_format: "jsonl.gz"`, `instance_count = 5280`,
   `metrics_at_creation` block with 9 headline numbers), `description.md` (7 mandatory sections per
   `meta/asset_types/predictions/specification.md`), and `files/predictions.jsonl.gz` (2.6 MB
   gzipped — well below the 5 MB pre-commit limit).
6. Wrote `results/metrics.json` in explicit multi-variant format with 3 variants (`best_legit`,
   `overall_max`, `dsi_eq_one_count`), each registering exactly one `direction_selectivity_index`
   value.
7. Wrote `results/results_summary.md` (mandatory sections: Summary, Metrics, Verification) and
   `results/results_detailed.md` (Summary, Methodology, Verification, Metrics, Visualizations,
   5-Seed Substrate-Rate Estimate, Pareto-Front Overlap, Analysis, Limitations, Files Created,
   Examples with 10 cells, Task Requirement Coverage).
8. Updated `results/remote_machines_used.json` to the verificator-required schema (added
   `machine_id`, `gpu`, `gpu_count`, `duration_hours`, `cost_usd` fields).
9. Ran `verify_task_results`, `verify_task_metrics`, and the predictions-asset verificator. All
   PASS. Ran flowmark on the edited markdown files and ruff on the new Python files; all clean.

## Outputs

### Predictions asset

* `assets/predictions/t0115-bedb-morph-nsga2-seed9354/details.json`
* `assets/predictions/t0115-bedb-morph-nsga2-seed9354/description.md`
* `assets/predictions/t0115-bedb-morph-nsga2-seed9354/files/predictions.jsonl.gz` (2.6 MB)

### Results documents

* `results/results_summary.md` — task headline summary with 5-seed substrate-rate estimate.
* `results/results_detailed.md` — detailed results with methodology, metrics, visualisations,
  examples, limitations, files-created, and task-requirement coverage.

### metrics.json

* `results/metrics.json` — explicit multi-variant format, 3 variants of
  `direction_selectivity_index` (best_legit = 0.9833, overall_max = 1.0, dsi_eq_one_count variant
  tags `n_dsi_eq_one = 64`).

### 3 CSVs

* `results/data/joint_pass_summary_5seeds.csv` — per-seed totals (5 rows: 44, 77, 2247, 7755,
  9354).
* `results/data/pareto_front_overlap_5seeds.csv` — nearest-neighbour distances from each t0115
  Pareto cell to t0106 / t0112 / t0113 / t0114 Pareto cells (23 rows, one per t0115 Pareto cell).
* `results/data/substrate_rate_5seed.csv` — per-seed rate + summary statistics (mean, SD, SE) +
  Hay 2011 and Druckmann 2007 literature baselines (10 rows total).

### 5 charts

* `results/images/hv_vs_gen_5seeds.png` — log-y HV trajectory overlay for all 5 seeds with
  pool-restart events annotated.
* `results/images/pareto_front_5seeds.png` — strict Pareto fronts on (DSI, PD-rate) axes coloured
  by seed.
* `results/images/joint_pass_yield_per_gen_5seeds.png` — joint-pass count discovered per
  generation, 5 seeds.
* `results/images/substrate_rate_5seed_with_literature.png` — 5-seed mean +/- SE bar chart vs Hay
  2011 (0.40%) and Druckmann 2007 (0.10%) literature baselines.
* `results/images/top50_morphologies_seed9354.png` — 10x5 grid of best 50 cells WITH FULL DENDRITE
  TREES drawn via `generate_fixed_morphology` + `LineCollection` (NOT only somas).

### Other

* `results/data/pareto_front_seed9354.json` — strict Pareto front for t0115 (23 cells).
* `results/data/example_cells_seed9354.json` — 10 example cells underlying `## Examples`.
* `results/remote_machines_used.json` — updated to verificator-required schema.

## Issues

* Operator's headline numbers in the task description (57 LEGIT joint-pass cells, best legit DSI
  0.9815, best PD 88.57 Hz) were close but not identical to my computed values from the actual data
  file: 63 LEGIT joint-pass cells, best legit DSI 0.9833, best PD 89.29 Hz. The discrepancy is small
  but consistent (operator's numbers slightly under my computed values). I used the computed values
  throughout for internal consistency with the per-cell JSONL evaluations.
* The 5-seed mean substrate-rate point estimate (2.58%) is somewhat lower than t0114's 4-seed
  estimate (2.93%) because t0115 (1.19%) is a lower-yield draw than the 4-seed sample average. Both
  estimates remain 6-7x above the Hay 2011 envelope upper bound.
