# t0107 — 8-Direction Polar Re-Evaluation of 10 Random Top-50 t0106 Cells

## Motivation

S-0106-03 proposes a 16-direction re-evaluation of all 50 top-ranked t0106 cells to test whether the
2-direction ratio-DSI breakthrough survives at higher angular sampling. This task is a
**reduced-scope variant** chosen by the operator:

* **8 directions** instead of 16 (every 45° rather than every 22.5°)
* **10 randomly selected cells** instead of all 50
* **Polar plots** of per-cell tuning curves as the primary output
* **No literature search, no suggestions** — tight, fast follow-up

The goal is a quick visual sanity check: do the t0106 winners look like proper DSGCs in polar
coordinates, or are their tuning curves bimodal / oddly shaped? An 8-direction sweep is sufficient
to distinguish a clean cosine-like tuning curve from a non-DSGC response pattern.

## Scope

### Fixed (inherited from t0106)

* Substrate: 68-d Bed B electrophys + 14-d morphology, same evaluator code as t0106
* DSI silence guard at 10 spikes per trial total (carried over from S-0102-01)
* Stimulus protocol: 1400 ms moving bar per direction; AR(2) noise per t0024
* `N_EVAL_SEEDS = 3` (matching t0106 to keep noise replicates comparable)

### Changed from t0106

| Knob | t0106 | t0107 |
| --- | --- | --- |
| Directions | 2 (PD=0°, ND=180°) | **8** (0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°) |
| Cells evaluated | 3,744 across NSGA-II | **10** randomly drawn from top-50 |
| DSI metric reported | Ratio DSI on PD/ND | **Both** ratio DSI (PD/ND only, comparable to t0106) **and** 8-direction vector-sum DSI |
| Output | NSGA-II Pareto front | **Per-cell polar tuning curves** + DSI comparison table |

### Cell selection

The top 50 cells from `tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json`
are ranked by joint-corner score `min(DSI/0.5, 1) × min(PD/30, 1)`, deduplicated by (DSI, PD)
tuple. From those 50, 10 are drawn uniformly at random with a fixed seed (numpy seed 42) for
reproducibility.

## Approach

1. Copy the t0106 evaluator pipeline into `code/`. Configure
   `ANGLES_DEG = [0, 45, 90, 135, 180, 225, 270, 315]` and `N_EVAL_SEEDS = 3`.
2. Load the t0106 `all_evaluations_seed44.json`, deduplicate and joint-corner-rank the cells, take
   top 50, sample 10 with numpy seed 42.
3. Run each cell's 68-d parameter vector through `evaluate_68d_vector` at the new 8-direction
   protocol. Local NEURON execution (10 cells × 8 dirs × 3 trials = 240 NEURON sims, ~75 s wall
   clock on the workstation; no Vast.ai needed).
4. Build the predictions asset `assets/predictions/eight-dir-polar-recheck-top10-t0106/` with
   per-cell per-direction firing rates and the recomputed metrics.
5. Render polar tuning curves: one polar subplot per cell in a 2 × 5 grid, with PD-rate annotated
   and 2-direction ratio DSI from t0106 + 8-direction vector-sum DSI from this task in each panel
   title. Save to `results/images/polar_tuning_curves_top10.png`.
6. Tabular comparison in `results_detailed.md`: original t0106 (DSI, PD) vs t0107 (vector-sum DSI,
   mean PD across 8 dirs).

## Key Questions

1. Do the 10 randomly selected cells produce **clean tuning curves** (single PD peak, depressed ND,
   smooth around the unit circle) as expected for DSGCs?
2. Does the **8-direction vector-sum DSI** roughly match the 2-direction ratio DSI? Spearman
   correlation across the 10 cells. Falsifiable: r > 0.7 supports the t0106 reformulation as a
   metric simplification; r < 0.4 says the 2-direction metric is masking non-DSGC behaviour.
3. Are there cells where the **PD axis is offset** from 0° (i.e., the cell prefers a different
   direction)? Would reveal a bias in the t0106 angle conventions.

## Compute and Budget

* **Per-cell evaluation**: 8 dirs × 3 trials = 24 NEURON sims per cell at ~0.3 s/sim = ~7 s/cell
* **All 10 cells**: ~70-90 s wall clock locally
* **Cost**: **$0** — runs on the workstation, no remote machine
* **Time envelope**: ~30-60 min total task wall-clock (implementation, plotting, reporting)

## Expected Assets

* **1 predictions asset** (`eight-dir-polar-recheck-top10-t0106`) — per-cell per-direction firing
  rates with metadata, recomputed DSI metrics

## Skipped Steps

Per operator instruction "no literature search or suggestions":

* `research-papers` — skipped (no new literature search needed)
* `research-internet` — skipped (no new literature search needed)
* `compare-literature` — skipped (no literature comparison needed)
* `suggestions` — minimal empty suggestions.json (`{"suggestions": []}`)

`research-code` is kept (need to identify the t0106 evaluator hooks for the 8-direction patch).
`planning` is kept (light plan). `setup-machines` / `teardown` are skipped (local execution).

## Verification Criteria

* `verify_task_file t0107_t0106_polar_8dir_recheck` passes with 0 errors.
* `verify_task_metrics t0107_t0106_polar_8dir_recheck` passes.
* `verify_predictions_asset --task-id t0107_t0106_polar_8dir_recheck` passes.
* `verify_task_complete t0107_t0106_polar_8dir_recheck` passes after merge.
* All 10 polar plots present in `results/images/polar_tuning_curves_top10.png`.

## References

* `tasks/t0106_long_pdnd_nsga2_300gen/` — source of the top-50 cells and the evaluator code base
* `S-0106-03` — the source suggestion (full 16-direction / 50-cell version is deferred for a later
  task if this reduced check looks clean)
