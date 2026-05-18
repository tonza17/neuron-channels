---
spec_version: "2"
task_id: "t0107_t0106_polar_8dir_recheck"
date_created: "2026-05-18"
---
# t0107 Implementation Plan

## Objective

Re-evaluate 10 randomly selected cells from the t0106 top-50 at an 8-direction protocol (45° steps)
and produce polar tuning-curve plots plus a comparison table of 2-direction ratio DSI (t0106) vs
8-direction vector-sum DSI (t0107). No literature search, no follow-up suggestions, no remote
compute.

## Approach

Reuse the t0106 evaluator stack with a minor patch to expose per-direction firing rates. Run locally
on the workstation in under 90 s wall clock. Sample selection is deterministic (numpy seed 42).

## Cost Estimation

| Line item | Estimate |
| --- | --- |
| Local NEURON wall clock | ~75 s (10 cells × 8 dirs × 3 trials) |
| Vast.ai compute | $0 (no remote) |
| Total cost | **$0** |

## Step by Step

1. Copy 13 source files verbatim from `tasks/t0106_long_pdnd_nsga2_300gen/code/` into
   `tasks/t0107_t0106_polar_8dir_recheck/code/` (constants, evaluator, generator wrapper, recorder,
   helpers, MODs). Rename task slug in `paths.py` only.
2. Patch the copied `evaluator.py` to surface `per_direction_rates_hz` in the `EvaluationResult`
   dataclass.
3. Write `code/sample_top10.py` — read
   `tasks/t0106_*/results/data/all_evaluations_seed44.json.gz`, dedup, joint-corner-rank, pick top
   50, sample 10 with `numpy.random.default_rng(42)`. Write `code/selected_cells.json` with the
   chosen cells' 68-d vectors + t0106-reported DSI / PD.
4. Write `code/eval_polar.py` — for each of the 10 cells, call
   `evaluate_68d_vector(vec, n_directions=8, eval_seeds=[111, 222, 333])`. Write
   `results/data/per_cell_polar_eval.json` with per-cell per-direction firing rates + recomputed
   8-direction vector-sum DSI + 2-direction ratio DSI (for sanity-check against t0106).
5. Write `code/plot_polar.py` — render the 10-cell polar grid (2 × 5) into
   `results/images/polar_tuning_curves_top10.png`. Each panel: polar plot of mean firing rate per
   direction, soma at centre, annotated with t0106 DSI / PD and t0107 vector-sum DSI / mean PD.
6. Compute Spearman correlation between t0106 2-direction ratio DSI and t0107 8-direction vector-sum
   DSI across the 10 cells.

## Remote Machines

None. All compute runs on the workstation.

## Assets Needed

* Read-only: `tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json.gz`
* Read-only: pre-compiled NEURON mod files at `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/`

## Expected Assets

* **1 predictions asset** `assets/predictions/eight-dir-polar-recheck-top10-t0106/` — per-cell
  per-direction firing rates with t0106 vs t0107 DSI comparison metadata.

## Time Estimation

* Code copy + patch: 10 min
* Sample + evaluate + plot: 5 min (most of which is matplotlib rendering)
* Results writeup: 15 min
* Total task wall clock: ~30 min

## Risks & Fallbacks

* **NEURON local install missing or broken**: if `evaluate_68d_vector` fails to import or run
  locally, fall back to spinning up a tiny Vast.ai CPU instance (~$0.20 for the few minutes needed).
  Operator-approved budget headroom is $18.35 of $75 remaining.
* **Sampled cell is biologically degenerate** (e.g., DSI = 1.0 silence-guard edge): the polar plot
  will show one or more zero directions. Acceptable; this is a fact about t0106 not a t0107 failure.
* **8-direction DSI collapses for a cell**: equally informative — would mean the 2-direction
  metric was masking off-axis structure. Recorded in results, not treated as a failure mode.

## Verification Criteria

* `verify_task_file t0107_t0106_polar_8dir_recheck` passes 0 errors.
* `verify_research_code t0107_t0106_polar_8dir_recheck` passes 0 errors.
* `verify_plan t0107_t0106_polar_8dir_recheck` passes 0 errors.
* `verify_task_metrics t0107_t0106_polar_8dir_recheck` passes 0 errors.
* `verify_task_results t0107_t0106_polar_8dir_recheck` passes 0 errors.
* `verify_predictions_asset --task-id t0107_t0106_polar_8dir_recheck` passes 0 errors.
* `verify_task_complete t0107_t0106_polar_8dir_recheck` passes 0 errors after PR merge.
* `results/images/polar_tuning_curves_top10.png` contains all 10 polar subplots.
* Spearman correlation between t0106 and t0107 DSI values is computed and reported in
  `results_detailed.md`.

## Task Requirement Checklist

* REQ-1: Sample 10 distinct cells from the t0106 top 50 via joint-corner-ranking and numpy seed 42.
* REQ-2: Evaluate each cell at 8 directions × 3 noise replicates.
* REQ-3: Surface per-direction firing rates from the evaluator.
* REQ-4: Produce a 2 × 5 polar tuning-curve grid in `results/images/polar_tuning_curves_top10.png`.
* REQ-5: Compute 8-direction vector-sum DSI for each cell.
* REQ-6: Compare t0106 (2-dir ratio) vs t0107 (8-dir vector-sum) DSI with Spearman correlation.
* REQ-7: Predictions asset registered with per-direction firing rates as the payload.
* REQ-8: No remote compute used (cost = $0).
* REQ-9: No literature research, no compare-literature, no follow-up suggestions.
