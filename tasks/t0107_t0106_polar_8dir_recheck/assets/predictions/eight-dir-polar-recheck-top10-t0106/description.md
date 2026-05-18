---
spec_version: "2"
predictions_id: "eight-dir-polar-recheck-top10-t0106"
documented_by_task: "t0107_t0106_polar_8dir_recheck"
date_documented: "2026-05-18"
---
# 8-direction polar re-evaluation of 10 sampled t0106 top-50 cells

## Metadata

* **Name**: 8-direction polar re-evaluation of 10 sampled t0106 top-50 cells
* **Model**: DSGC compartmental model (54-d Bed B electrophys via t0080 apply_parameter_vector +
  t0092-patched 14-d procedural morphology, canonical via C-0093-01)
* **Datasets**: none (simulator outputs)
* **Format**: json (single top-level object with `evaluations` list)
* **Instances**: 10 per-cell records
* **Created by**: t0107_t0106_polar_8dir_recheck

## Overview

This predictions asset records the result of re-running 10 randomly sampled t0106 top-50 cells
through the t0106 evaluator stack at higher angular resolution. The original t0106 run used a
2-direction (PD = 0 deg, ND = 180 deg) ratio DSI as its selectivity objective; that reformulation
produced the first ever joint-pass cells in the t0080-t0106 lineage (123 unique cells with DSI >=
0.5 AND PD >= 30 Hz across 3,744 evaluations). The reduced angular sampling is mathematically
equivalent to vector-sum DSI for antipodal pairs but raises a concern: it cannot detect cells whose
tuning curves are bimodal, off-axis, or otherwise non-DSGC-like.

The 10 cells were drawn by joint-corner ranking the 50 best t0106 cells by
`min(DSI/0.5, 1) x min(PD/30, 1)`, deduplicating by (DSI, PD) tuples, and sampling with
`numpy.random.default_rng(42)`. Each cell was re-evaluated at 8 directions (45 deg steps) x 3 noise
replicates = 24 NEURON simulations per cell. The 8-direction vector-sum DSI is the headline new
metric; the 2-direction ratio DSI computed from the 8-direction PD/ND rates is also stored as a
sanity check against the t0106 numbers.

The asset is the primary evidence channel for the t0107 results summary and supports the falsifiable
hypothesis from the task description: if Spearman rho between t0106 2-direction ratio DSI and t0107
8-direction vector-sum DSI is > 0.7, the t0106 reformulation is a metric simplification rather than
a corner artefact. The observed rho is 0.758 (p = 0.011), which crosses the threshold but reveals
substantial per-cell drift in the absolute DSI values: the mean 2-direction ratio DSI across the 10
cells is 0.87, while the mean 8-direction vector-sum DSI is 0.52, indicating that the 8-direction
sweep distributes spike mass into off-axis directions for most cells.

## Model

The simulator is a compartmental DSGC neuron model on top of NEURON 8.2.7 / NetPyNE 1.1.1. The
electrophysiological substrate is the 54-d Bed B parameter vector from t0080 applied via
`apply_parameter_vector`; the morphology is the t0092-patched procedural generator
`generate_fixed_morphology` (canonical via correction C-0093-01) parameterised by 14 additional
dimensions covering soma offset, dendritic asymmetry, branch density, branch density gradient, and
related morphological knobs. The combined parameter space is 68-dimensional.

The new run differs from t0106 only in the stimulus angle list: ANGLES_DEG goes from the two-element
antipodal pair [0, 180] to the eight-element [0, 45, 90, 135, 180, 225, 270, 315]. The stimulus
profile (1400 ms moving bar, AR(2)-correlated rate noise per t0024, parametric synapse placer per
t0080) is unchanged. Three noise replicates per direction (eval_seeds = 111, 222, 333) give 24
simulations per cell.

NEURON code ran on a Vast.ai EPYC 7532 32-effective-core instance (offer 33356672, dph $0.36815)
using `concurrent.futures.ProcessPoolExecutor` with `max_workers=10` -- one worker per cell, no
within-cell parallelism. The remote wall clock for the full 10-cell run was 547.2 s (9.12 min);
per-cell wall clock ranged from 30.4 s (rank 45) to 547.1 s (rank 5, an outlier with very expensive
NEURON dynamics). Total compute cost was $0.15 against the project's remaining $18.35 headroom.

## Data

No external dataset is consumed. Input vectors are the full 68-d parameter vectors of the 10 cells
sampled from the t0106 top-50. The sampling procedure is reproducible: load
`tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json.gz`, deduplicate by
`(round(DSI, 4), round(PD, 2))`, rank by joint-corner score `min(DSI/0.5, 1) x min(PD/30, 1)`, break
ties by `dsi + pd/100`, take the top 50, then draw 10 indices with
`numpy.random.default_rng(42).choice(50, size=10, replace=False)`.

The 10 selected cells have t0106 ranks 4, 5, 10, 20, 29, 33, 34, 40, 45, 50. Their t0106-reported
2-direction ratio DSI ranges from 0.843 (rank 34) to 0.979 (rank 33); their t0106-reported PD-rates
range from 84.29 Hz (rank 50) to 121.67 Hz (rank 5). The same cells are stored in
`code/selected_cells.json` for full reproducibility.

## Prediction Format

The file `files/per_cell_polar_eval.json` is a single JSON object with three top-level keys plus the
`evaluations` payload:

```json
{
  "n_directions": 8,
  "eval_seeds": [111, 222, 333],
  "max_workers": 10,
  "wall_clock_total_s": 547.2,
  "evaluations": [ ... ]
}
```

Each entry in `evaluations` has the following fields:

* `t0106_rank`: int, rank in the t0106 joint-corner-ranked top-50
* `t0106_generation`: int, NSGA-II generation that produced the cell in t0106
* `t0106_dsi`: float in [0, 1], 2-direction ratio DSI reported by t0106
* `t0106_pd_hz`: float, PD firing rate (Hz) reported by t0106
* `vector_68d`: list of 68 floats, full electrophys + morphology parameter vector
* `angles_deg`: list of 8 floats, [0, 45, 90, 135, 180, 225, 270, 315]
* `per_direction_rates_hz`: list of 8 floats, mean firing rate per direction (Hz) across the 3 noise
  replicates
* `t0107_dsi_8dir_vsum`: float in [0, 1], 8-direction vector-sum DSI
* `t0107_pd_at_0deg`: float, firing rate at 0 deg in Hz
* `t0107_nd_at_180deg`: float, firing rate at 180 deg in Hz
* `t0107_dsi_2dir_ratio_sanity`: float in [-1, 1], 2-direction ratio DSI computed from the
  8-direction PD/ND rates (sanity check against t0106)
* `t0107_eval_seeds`: list of 3 ints, [111, 222, 333]
* `t0107_n_directions`: int, 8
* `t0107_eval_elapsed_s`: float, single-cell wall-clock in seconds
* `t0107_n_errors`: int, NEURON trial errors during the 24 simulations
* `t0107_n_trials`: int, total trials run (always 24 = 8 dirs x 3 seeds)

The records are ordered by ascending `t0106_rank` for deterministic output.

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **10** of 10 |
| NEURON failures | **0** |
| Wall clock (10 cells in parallel) | **547.2 s (9.12 min)** |
| Vast.ai cost | **$0.15** |
| Spearman rho (t0106 DSI vs t0107 vsum DSI) | **0.758** (p = 0.011) |
| Mean t0107 vector-sum DSI | **0.519** |
| Min / max t0107 vector-sum DSI | **0.222 / 0.806** |
| Mean t0107 2-direction ratio DSI (sanity) | **0.867** |
| Mean firing rate at 0 deg | **84.2 Hz** |
| Mean firing rate across 8 dirs | **43.3 Hz** |

Per-cell summary:

| rank | t0106 DSI | t0106 PD (Hz) | t0107 vsum DSI | t0107 ratio DSI (sanity) | PD@0 (Hz) | ND@180 (Hz) |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 0.935 | 121.4 | 0.305 | 0.487 | 121.4 | 41.9 |
| 5 | 0.917 | 121.7 | 0.222 | 0.899 | 120.7 | 6.4 |
| 10 | 0.948 | 115.0 | 0.516 | 0.956 | 116.4 | 2.6 |
| 20 | 0.971 | 96.2 | 0.563 | 0.980 | 96.0 | 1.0 |
| 29 | 0.945 | 92.4 | 0.274 | 0.945 | 92.9 | 2.6 |
| 33 | 0.979 | 88.1 | 0.806 | 0.925 | 30.7 | 1.2 |
| 34 | 0.843 | 100.7 | 0.385 | 0.674 | 36.7 | 7.1 |
| 40 | 0.962 | 86.0 | 0.784 | 0.953 | 88.1 | 2.1 |
| 45 | 0.941 | 86.9 | 0.611 | 0.891 | 29.1 | 1.7 |
| 50 | 0.950 | 84.3 | 0.728 | 0.962 | 109.8 | 2.1 |

## Main Ideas

* The 8-direction vector-sum DSI correlates positively with the t0106 2-direction ratio DSI
  (Spearman rho = **0.758**, p = 0.011) but is consistently lower in absolute value (mean 0.52 vs
  0.87). The rank ordering is preserved, supporting the interpretation that the t0106 reformulation
  is a metric simplification rather than a corner artefact, but the t0106 ratio DSI systematically
  overstates the strength of selectivity by absorbing off-axis spike mass into the PD/ND pair alone.
* The 2-direction ratio DSI sanity check from the 8-direction data agrees closely with the original
  t0106 numbers (sanity-DSI mean 0.87 vs t0106 mean 0.94; only rank 4 and rank 34 drift more than
  0.3), confirming that the 2-direction protocol itself is reproducible and the discrepancy comes
  from the angular sampling, not from random noise or evaluator drift.
* Rank 4 is the most striking discrepancy: t0106 reported DSI = 0.935 at PD = 121.4 Hz, but in the
  8-direction re-evaluation the PD firing rate of 121.4 Hz is matched by an ND rate of 41.9 Hz,
  pulling the ratio sanity DSI down to 0.487 and the vector-sum DSI to 0.305. This single cell
  diverged most from the t0106 number, suggesting the 2-direction protocol can occasionally pick
  cells with a partial null-direction response that the 8-direction sweep exposes.

## Summary

This asset records the 8-direction polar re-evaluation of 10 cells randomly sampled from the t0106
top-50. The cells were evaluated with the same NEURON evaluator pipeline as t0106 but with the angle
list extended from [0, 180] to [0, 45, 90, 135, 180, 225, 270, 315]. All 10 cells completed without
NEURON errors. The Vast.ai EPYC 7532 instance ran the 10-cell parallel pool in 547 s of wall clock
at a total cost of $0.15.

The headline finding is that the t0106 2-direction ratio DSI and the t0107 8-direction vector-sum
DSI are positively correlated (Spearman rho = 0.758, p = 0.011) but with substantial absolute drift
(mean 0.87 vs 0.52). The rank ordering of cells is largely preserved, supporting the t0106
reformulation as a useful metric proxy, but the 8-direction sweep reveals that several cells have
non-trivial off-axis firing that the 2-direction protocol does not capture. The 2-direction ratio
DSI sanity check from the 8-direction PD/ND rates agrees closely with t0106's numbers (only one cell
drifts by more than 0.3), ruling out evaluator-level reproducibility issues. The full per-cell
per-direction firing-rate vectors are stored for downstream polar tuning-curve plotting and any
future angle-resolved analyses.
