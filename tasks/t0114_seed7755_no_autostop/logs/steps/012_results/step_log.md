---
spec_version: "3"
task_id: "t0114_seed7755_no_autostop"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-20T14:20:00Z"
completed_at: "2026-05-20T14:45:00Z"
---
# Step 12: results

## Summary

Built the complete t0114 results stage in a single inline analysis script (`code/build_results.py`):
the predictions asset (gzipped JSONL of all 5,952 per-cell evaluations plus `details.json` +
`description.md`), `results/metrics.json` (explicit multi-variant format with three
`direction_selectivity_index` sub-variants), three CSV tables (`joint_pass_summary_4seeds.csv`,
`pareto_front_overlap_4seeds.csv`, `detector_replay.csv`), five charts in `results/images/`,
`results_summary.md`, and `results_detailed.md`. Implemented the S-0113-03 offline detector replay
over a 4-window x 6-threshold grid (24 cells x 4 seeds) and selected **(W*, T*) = (3, 0.015)** as
the recommended new project default — the smallest deviation from the current `(W=2, T=0.01)` that
fires on t0106 within [20, 60] gens, does NOT fire prematurely on t0113 within the recorded 14 gens,
and fires on t0114 at gen 26. All five required verificators PASS.

## Actions Taken

1. Inspected t0113's results stage for layout / pattern reference (`build_t0113_results.py`,
   `results_summary.md`, `results_detailed.md`, `metrics.json`).
2. Inspected the t0114 input data: `all_evaluations_seed7755.json` (5,952 cells across 62 gens),
   `hv_trajectory_seed7755.json` (62 entries, final HV 111.5353), `algorithm_config.json`.
3. Wrote a single inline analysis script `code/build_results.py` that loads all 4 seeds (t0106 seed
   44 via predictions asset gz, t0112 seed 77 via results/data gz, t0113 seed 2247 via predictions
   asset gz, t0114 seed 7755 via the local JSON), computes the strict Pareto front for t0114 (6
   cells), and writes every required output.
4. Built the predictions asset `assets/predictions/t0114-bedb-morph-nsga2-seed7755/` with
   `details.json` (`spec_version: "2"`, `prediction_format: "jsonl.gz"`, instance_count=5952,
   metrics_at_creation block with 9 headline numbers), `description.md` (7 mandatory sections per
   `meta/asset_types/predictions/specification.md`), and `files/predictions.jsonl.gz` (2.7 MB
   gzipped — well below the 5 MB pre-commit limit, well below the 3 MB compression threshold so
   `.gz` is the safe default).
5. Wrote `results/metrics.json` in the explicit multi-variant format with three variants encoding
   the `best_legit` (0.9926), `overall_max` (1.0), and `dsi_eq_one_count` (1073) sub-variants of the
   registered `direction_selectivity_index` metric.
6. Wrote the three CSVs in `results/data/`: `joint_pass_summary_4seeds.csv` (4 rows),
   `pareto_front_overlap_4seeds.csv` (6 rows — one per t0114 strict Pareto cell), and
   `detector_replay.csv` (32 rows = 4 windows x 2 thresholds x 4 seeds).
7. Rendered the 5 charts in `results/images/`: `hv_vs_gen_4seeds.png`, `pareto_front_4seeds.png`,
   `joint_pass_yield_per_gen_4seeds.png`, `detector_replay_heatmap.png`,
   `top50_morphologies_seed7755.png`.
8. Implemented the S-0113-03 offline detector replay. The headline 4 x 2 CSV grid shows that
   `(W=2, T=0.01)` fires prematurely on t0113 at gen 13; a wider 4 x 6 grid used for selection
   reveals that `(W=3, T=0.015)` satisfies all S-0113-03 criteria with smallest deviation from
   defaults (deviation metric = 1.5).
9. Wrote `results/results_summary.md` (3 mandatory sections + 3 Key Question answers) and
   `results/results_detailed.md` (7 mandatory sections + 10 Examples with full 68-d vectors, ending
   with `## Task Requirement Coverage`).
10. Updated `results/remote_machines_used.json` to include the verifier-required fields
    (`machine_id`, `gpu`, `gpu_count`, `duration_hours`, `cost_usd`) alongside the existing
    `instance_id` / `gpu_name` / `total_*` fields.
11. Ran all 5 verificators via `run_with_logs`.

## Outputs

* `assets/predictions/t0114-bedb-morph-nsga2-seed7755/` — predictions asset
  * `details.json` (4.5 KB)
  * `description.md` (5.8 KB)
  * `files/predictions.jsonl.gz` (2.7 MB; 5,952 records)
* `results/results_summary.md` (4.7 KB; 3 mandatory sections + 3 Key Question answers)
* `results/results_detailed.md` (40+ KB; 7 mandatory sections + 10 Examples with full 68-d vectors)
* `results/metrics.json` — registered `direction_selectivity_index` variant format with 3
  sub-variants
* `results/data/joint_pass_summary_4seeds.csv` — 4 rows (one per seed)
* `results/data/pareto_front_overlap_4seeds.csv` — 6 rows (one per t0114 Pareto cell)
* `results/data/detector_replay.csv` — 32 rows (4 windows x 2 thresholds x 4 seeds)
* `results/data/pareto_front_seed7755.json` — strict Pareto front (6 cells) for t0114
* `results/data/example_cells_seed7755.json` — 10 representative cells with full 68-d vectors
* `results/images/hv_vs_gen_4seeds.png` — log-scale HV trajectory (4 seeds)
* `results/images/pareto_front_4seeds.png` — 4-seed Pareto-front overlay
* `results/images/joint_pass_yield_per_gen_4seeds.png` — per-gen joint-pass discovery (4 seeds)
* `results/images/detector_replay_heatmap.png` — 4-panel detector replay heatmap
* `results/images/top50_morphologies_seed7755.png` — top-50 cell grid
* `code/build_results.py` — one-stop 4-seed analysis script (results + predictions asset)
* `results/remote_machines_used.json` — updated with `machine_id` / `gpu` / `gpu_count` /
  `duration_hours` / `cost_usd` fields required by `verify_task_results`

## Verificator Outcomes

All five requested verificators executed via the `run_with_logs` wrapper.

| Verificator | Result | Errors | Warnings | Notes |
| --- | --- | --- | --- | --- |
| `verify_task_results` | **PASSED** | 0 | 0 | After updating `remote_machines_used.json` to include the verifier-required `machine_id` / `gpu` / `gpu_count` / `duration_hours` / `cost_usd` fields (initial run reported 5 TR-E014 errors). |
| `verify_task_metrics` | **PASSED** | 0 | 0 | `metrics.json` registers only the `direction_selectivity_index` metric per `meta/metrics/`; sub-variants encoded as `dsi_subvariant` dimension. |
| Predictions asset verificator (combined: folder + details + description, via `meta.asset_types.predictions.verificator`) | **PASSED** | 0 | 2 | Non-blocking PR-W014 (no linked model asset) and PR-W015 (no linked dataset asset) — same shape as t0106 / t0112 / t0113. Note: the orchestrator's instruction referred to three separate `verify_predictions_*` modules; the actual entry point is the unified `meta.asset_types.predictions.verificator` which performs all three checks. |

## Headline Findings (3 Key Question answers)

1. **Is the t0113 14-gen stop premature?** YES, decisively. Same protocol, auto-stop disabled, seed
   7755 ran for 62 gens and reached HV 111.54 (2.4x t0113's 45.62) and 484 LEGIT joint-pass cells
   (vs t0113's 0).
2. **Recommended new (WINDOW, REL_THRESHOLD) for the HV-plateau detector?** **(W=3, T=0.015)** —
   smallest deviation from the current `(W=2, T=0.01)` that simultaneously (a) fires on t0106 within
   [20, 60] gens at gen 39, (b) does NOT fire prematurely on t0113 within the recorded 14 gens, and
   (c) fires on t0114 at gen 26.
3. **4-seed substrate-rate vs literature?** Per-seed LEGIT yields: 3.23% / 0.35% / 0.00% / 8.13% (44
   / 77 / 2247 / 7755). 4-seed mean = 2.93%, SE = 1.86%, 95% CI (-0.71%, 6.56%). Point estimate is
   7.3x above the Hay 2011 envelope upper bound; SE still brackets both literature baselines, but
   seeds 44 and 7755 each independently exceed the envelope by >= 8x.

## Issues

1. **Initial detector grid was too narrow.** The default `(W=2, T=0.01)` and the next-smaller
   `(W=2, T=0.005)` both still fire prematurely on t0113 at gen 13. The S-0113-03 criteria cannot be
   satisfied with the headline 4 x 2 grid alone. Resolved by computing a wider 4 x 6 grid for the
   `(W*, T*)` selection while still committing only the 4 x 2 grid to the CSV per task description.
2. **The "fires >= gen 20 on every seed" criterion cannot be strictly tested on truncated
   trajectories.** t0112 (21 gens) and t0113 (14 gens) were both truncated by the current rule, so
   we cannot run the new rule against ground-truth long trajectories. The acceptable proxy is "does
   NOT fire prematurely on the recorded short trajectory". Documented as a caveat in
   `## Detector Reparameterisation (S-0113-03)`.
3. **The orchestrator's stated headline numbers (194 legit cells, DSI=0.9868 / PD=107.86 at gen 47)
   do not match the data.** The actual recomputed values are 484 LEGIT cells, best legit DSI =
   0.9926 / PD = 63.81 at gen 61, and best PD-rate = 112.86 at gen 62. The recomputed numbers are
   used throughout the results files since they are the ground truth from the
   `all_evaluations_ seed7755.json` log.
4. **`remote_machines_used.json` required field rename.** Initial file used `instance_id` /
   `gpu_ name` / `total_*` field names (matching the format already on disk before the results
   step). The verifier requires `machine_id` / `gpu` / `gpu_count` / `duration_hours` / `cost_usd`.
   Both sets of field names are preserved in the updated file for compatibility.
