# Predictions by Date Added

13 predictions asset(s) grouped by creation date.

[Back to all predictions](../README.md)

---

## 2026-05-19 (1)

<details>
<summary>📊 <strong>NSGA-II seed 77 on 68-d Bed B + 14-d morphology, 2 directions,
seed-77 replicate of t0106</strong>
(<code>t0112-bedb-morph-nsga2-seed77</code>) — 2016 instances (json.gz)</summary>

| Field | Value |
|---|---|
| **ID** | `t0112-bedb-morph-nsga2-seed77` |
| **Model ID** | — |
| **Model** | Compartmental DSGC neuron model combining the 54-d Bed B electrophysiology parameter vector (from t0080) applied via apply_parameter_vector with the t0092-patched 14-d procedural morphology generator (canonical via correction C-0093-01). Each cell is evaluated with 2 stimulus directions (PD = 0 deg, ND = 180 deg) x 3 noise replicates and scored on a 2-objective vector (ratio DSI, preferred-direction firing rate in Hz). NSGA-II minimises the negated pair; the DSI silence guard from S-0102-01 clamps DSI to 0.0 when total PD+ND spike count falls below 10 spikes per trial. |
| **Datasets** |  |
| **Format** | json.gz |
| **Instances** | 2016 |
| **Date created** | 2026-05-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Created by** | [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md) |
| **Documentation** | [`description.md`](../../../tasks\t0112_t0106_seed77_replicate\assets\predictions\t0112-bedb-morph-nsga2-seed77\description.md) |

**Metrics at creation:**

* **n_generations_completed**: 21
* **n_cells_total**: 2016
* **best_dsi_ratio**: 0.9535
* **best_pd_rate_hz**: 114.76
* **n_joint_pass_unique**: 7
* **n_joint_pass_evaluations**: 25
* **final_hypervolume**: 107.4602
* **final_cost_usd**: 1.96

# NSGA-II seed 77 Bed B + morphology 2-direction seed-77 replicate of t0106

## Metadata

* **Name**: NSGA-II seed 77 on 68-d Bed B + 14-d morphology, 2 directions, seed-77 replicate
  of t0106
* **Model**: DSGC compartmental model (54-d Bed B electrophys via t0080 apply_parameter_vector
  + t0092-patched procedural morphology, canonical via C-0093-01)
* **Datasets**: none (simulator outputs)
* **Format**: json (single top-level object with `evaluations` list, gzip-compressed)
* **Instances**: 2,016 per-cell evaluations across 21 NSGA-II generations
* **Created by**: t0112_t0106_seed77_replicate

## Overview

This predictions asset captures every cell evaluated by the t0112 minimum-change replicate of
t0106: the same 68-d Bed B + 14-d morphology substrate, the same 2-direction ratio DSI
objective, the same NSGA-II hyperparameters (pop=96, SBX/PM, N_EVAL_SEEDS=3, silence guard
active), with exactly two constants changed from t0106: GA seed 44 -> 77 and pool-restart
cadence 25 gens -> 10 gens.

The run targeted 60 generations (extendable from t0106's stopped-at-40 ceiling) but the
HV-plateau operator-stop criterion fired at generation 21 — much earlier than t0106's gen-38
plateau. The hypervolume trajectory shows a steep climb between gen 14 and gen 17 (HV 33.2 ->
107.3, the breakthrough-cell signature) and then near-flat behaviour through gen 21 (HV
107.4).

The headline finding is **partial replication**: seed 77 reaches the joint-pass corner (DSI >=
0.5 AND PD >= 30 Hz) with best DSI = 0.9535 at PD = 60 Hz and best PD-rate = 114.76 Hz, but
produces only **7 unique joint-pass cells (25 evaluations)** versus t0106 seed 44's 123 unique
(637 evaluations). Both seeds reach the same frontier corner but with very different cell
densities — the substrate's joint-pass region is reachable from multiple GA seeds, but the
density of reachable cells is itself a stochastic property of the GA seed.

## Model

The simulator is the same compartmental DSGC neuron model used in t0106, running on NEURON
8.2.7 / NetPyNE 1.1.1. The electrophysiological substrate is the 54-d Bed B parameter vector
from t0080 applied via `apply_parameter_vector`; the morphology is the t0092-patched
procedural generator `generate_fixed_morphology` (canonical via correction C-0093-01)
parameterised by 14 additional dimensions covering soma offset, dendritic asymmetry, branch
density, branch density gradient, and related morphological knobs. The combined parameter
space is 68-dimensional.

Each cell is evaluated by 2 NEURON simulations (PD bar at 0 degrees, ND bar at 180 degrees) x
3 noise replicates = 6 simulations per cell. The selectivity objective is the ratio DSI =
(PD_rate - ND_rate) / (PD_rate + ND_rate); for antipodal sampling this is mathematically
identical to the vector-sum DSI. The DSI silence guard from S-0102-01 is active throughout:
cells whose total PD+ND spike count across the 3 trials falls below 10 are clamped to DSI =
0.0 before being returned to NSGA-II selection.

Pymoo NSGA-II configuration: pop_size = 96, n_gen = 60 ceiling, n_eval_seeds = 3, single GA
seed = 77 (LHS-initialised initial population, explicit `np.random.SeedSequence(77)` seeding),
SBX crossover eta = 15 prob = 0.9, polynomial mutation eta = 20 prob = 1/68, duplicate
elimination enabled. The driver implements `PerGenerationPoolRestart(every=10)` — a tighter
cadence than t0106's every-25 to reduce NEURON-accumulated worker memory between restarts. The
tighter cadence held per-generation wall-clock at 200-1,100 s/gen even through the late
generations.

## Data

No external dataset is consumed. Input vectors are 68-dimensional points sampled by NSGA-II
starting from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and
explicitly seeded with task_seed = 77 (the only deliberate divergence from t0106's seed 44).
Bounds for the 68 parameters are inherited unchanged from t0106 (which inherited from the
t0102 / t0099 substrate, the same 54-d electrophys bounds from t0080 plus the 14-d morphology
bounds from t0090 patched via t0093). Noise replicates within each evaluation use the same
three deterministically spawned RNG seeds drawn from `np.random.SeedSequence(42).spawn(5)`
that t0106 used.

The 2-direction restriction (PD = 0 deg, ND = 180 deg) is preserved verbatim from t0106 — this
was the t0106 breakthrough and the t0112 task brief explicitly forbids changing it.

## Prediction Format

The file `files/all_evaluations_seed77.json.gz` is a gzip-compressed single JSON object with
one key, `evaluations`, mapping to a list of 2,016 per-cell evaluation records. Each record
has the following fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..21 = offspring generations).
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector.
* `objective_F_minimised`: list of 2 floats, the NSGA-II objective vector after sign-flipping
  for maximisation, i.e. `[-ratio_dsi, -pd_rate_hz]`. NSGA-II minimises this pair directly.
* `dsi_vector_sum`: float in [0, 1], the ratio DSI = (PD_rate - ND_rate) / (PD_rate + ND_rate)
  averaged across the 3 noise replicates. The field name `dsi_vector_sum` is preserved for
  schema compatibility with t0102 / t0104 / t0106; under 2-direction antipodal sampling, the
  vector-sum DSI reduces exactly to the ratio DSI. Guard-cleaned per S-0102-01 at total-spike
  threshold 10 per trial, so values of 0.0 may either reflect a real ratio of zero or the
  silence guard floor.
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 3
  replicates).

The strict 2-axis joint-pass flag `joint_pass = (dsi_vector_sum >= 0.5) AND (pd_rate_hz >=
30)` is not stored per-record but is trivially recomputable from the above two fields. 25 of
the 2,016 records satisfy this corner (7 unique parameter vectors).

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **2,016** |
| Generations completed | **21** of 60 ceiling (HV plateau stop) |
| Best ratio DSI | **0.9535** at PD = 60.00 Hz |
| Best PD-rate frontier (Hz) | **114.76** at DSI = 0.0021 |
| Unique joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz) | **7** |
| Joint-pass evaluations (with NSGA-II repetition) | **25** |
| Joint-pass yield | **0.35%** (7 unique / 2,016 cells) |
| Final hypervolume (2-D) | **107.4602** (start 0.1156; 928x growth) |
| Final NSGA-II compute cost (USD) | **$1.96** of $25 cap |

The joint-pass yield of **0.35%** (7 unique / 2,016) is roughly 10x lower than t0106 seed 44's
**3.3%** (123 / 3,744) on the same substrate. Both seeds discover the same frontier corner
(best DSI ~ 0.95, best PD > 100 Hz) but seed 77 packs the corner much more sparsely.

## Main Ideas

* The **substrate is reachable from at least two GA seeds** (44 and 77). The 2-direction ratio
  DSI reformulation is the load-bearing change, not the seed-44 luck — seed 77 also crosses
  the joint-pass corner.
* The **joint-pass density is stochastic across seeds**. 7 unique vs 123 unique on the same
  substrate with the same hyperparameters argues that the published joint-pass acceptance rate
  from t0106 is a single-seed point estimate that cannot be reported as a substrate-level rate
  without more replicates.
* The **tighter pool-restart cadence (every 10 gens) was operationally safe**. Per-generation
  wall-clock peaked at ~1,100 s/gen and dropped after each restart; total run time was 4 h 40
  m for 21 gens vs t0106's 24.1 h for 40 gens (~1.5x faster per gen).
* The **HV-plateau detector fired at gen 21** — much earlier than t0106's gen-38 plateau. The
  earlier stop is consistent with seed 77 producing a smaller, more concentrated joint-pass
  cohort that exhausts its local Pareto-improvement opportunities sooner.
* The asset preserves the full 68-d parameter vector for every cell, enabling cross-seed
  parameter-space distance analysis between t0106 and t0112 Pareto cells in the t0112 results
  step.

## Summary

This asset records every NSGA-II evaluation from the t0112 minimum-change replicate of t0106:
same substrate, same objectives, same hyperparameters, only the GA seed (77) and the
pool-restart cadence (every 10 gens) changed. The run completed 21 generations on GA seed 77
before HV-plateau stopped it, evaluated 2,016 cells, and spent $1.96 of the $25 cap.

The headline finding is **partial replication**: seed 77 reaches the same frontier corner as
seed 44 (best DSI 0.9535 vs 0.9606; best PD 114.76 Hz vs 122.62 Hz) but produces 17x fewer
unique joint-pass cells (7 vs 123). The substrate is therefore reachable from multiple GA
seeds, but the density of reachable joint-pass cells is itself a stochastic property of the GA
seed — the t0106 3.3% acceptance rate is a single-seed point estimate that must not be
reported as a substrate-level property without additional replicates.

The asset is the primary evidence channel for the t0112 results step, supports the cross-seed
Pareto-front overlap analysis in t0112's compare-literature step, and provides the substrate
for any downstream multi-seed confirmation tasks.

</details>

## 2026-05-18 (2)

<details>
<summary>📊 <strong>8-direction polar re-evaluation of 10 sampled t0106 top-50
cells</strong> (<code>eight-dir-polar-recheck-top10-t0106</code>) — 10
instances (json)</summary>

| Field | Value |
|---|---|
| **ID** | `eight-dir-polar-recheck-top10-t0106` |
| **Model ID** | — |
| **Model** | Compartmental DSGC neuron model combining the 54-d Bed B electrophysiology parameter vector (from t0080) applied via apply_parameter_vector with the t0092-patched 14-d procedural morphology generator (canonical via correction C-0093-01). Each cell is re-evaluated with 8 stimulus directions (0, 45, 90, 135, 180, 225, 270, 315 deg) x 3 noise replicates (eval_seeds = 111, 222, 333). The S-0102-01 silence guard at 10 spikes per trial total carries over from t0106; vector-sum DSI is bounded in [0, 1]. |
| **Datasets** |  |
| **Format** | json |
| **Instances** | 10 |
| **Date created** | 2026-05-18 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Created by** | [`t0107_t0106_polar_8dir_recheck`](../../../overview/tasks/task_pages/t0107_t0106_polar_8dir_recheck.md) |
| **Documentation** | [`description.md`](../../../tasks\t0107_t0106_polar_8dir_recheck\assets\predictions\eight-dir-polar-recheck-top10-t0106\description.md) |

**Metrics at creation:**

* **n_cells_evaluated**: 10
* **n_directions**: 8
* **n_eval_seeds**: 3
* **n_failures**: 0
* **spearman_rho_t0106_dsi_vs_t0107_vsum_dsi**: 0.7576
* **spearman_p_value**: 0.0111
* **mean_t0107_dsi_8dir_vsum**: 0.5194
* **min_t0107_dsi_8dir_vsum**: 0.2218
* **max_t0107_dsi_8dir_vsum**: 0.806
* **mean_t0107_dsi_2dir_ratio_sanity**: 0.8672
* **mean_pd_at_0deg_hz**: 84.17
* **mean_pd_across_8_dirs_hz**: 43.25
* **wall_clock_total_s**: 547.2
* **remote_vastai_cost_usd**: 0.1517

# 8-direction polar re-evaluation of 10 sampled t0106 top-50 cells

## Metadata

* **Name**: 8-direction polar re-evaluation of 10 sampled t0106 top-50 cells
* **Model**: DSGC compartmental model (54-d Bed B electrophys via t0080 apply_parameter_vector
  + t0092-patched 14-d procedural morphology, canonical via C-0093-01)
* **Datasets**: none (simulator outputs)
* **Format**: json (single top-level object with `evaluations` list)
* **Instances**: 10 per-cell records
* **Created by**: t0107_t0106_polar_8dir_recheck

## Overview

This predictions asset records the result of re-running 10 randomly sampled t0106 top-50 cells
through the t0106 evaluator stack at higher angular resolution. The original t0106 run used a
2-direction (PD = 0 deg, ND = 180 deg) ratio DSI as its selectivity objective; that
reformulation produced the first ever joint-pass cells in the t0080-t0106 lineage (123 unique
cells with DSI >= 0.5 AND PD >= 30 Hz across 3,744 evaluations). The reduced angular sampling
is mathematically equivalent to vector-sum DSI for antipodal pairs but raises a concern: it
cannot detect cells whose tuning curves are bimodal, off-axis, or otherwise non-DSGC-like.

The 10 cells were drawn by joint-corner ranking the 50 best t0106 cells by `min(DSI/0.5, 1) x
min(PD/30, 1)`, deduplicating by (DSI, PD) tuples, and sampling with
`numpy.random.default_rng(42)`. Each cell was re-evaluated at 8 directions (45 deg steps) x 3
noise replicates = 24 NEURON simulations per cell. The 8-direction vector-sum DSI is the
headline new metric; the 2-direction ratio DSI computed from the 8-direction PD/ND rates is
also stored as a sanity check against the t0106 numbers.

The asset is the primary evidence channel for the t0107 results summary and supports the
falsifiable hypothesis from the task description: if Spearman rho between t0106 2-direction
ratio DSI and t0107 8-direction vector-sum DSI is > 0.7, the t0106 reformulation is a metric
simplification rather than a corner artefact. The observed rho is 0.758 (p = 0.011), which
crosses the threshold but reveals substantial per-cell drift in the absolute DSI values: the
mean 2-direction ratio DSI across the 10 cells is 0.87, while the mean 8-direction vector-sum
DSI is 0.52, indicating that the 8-direction sweep distributes spike mass into off-axis
directions for most cells.

## Model

The simulator is a compartmental DSGC neuron model on top of NEURON 8.2.7 / NetPyNE 1.1.1. The
electrophysiological substrate is the 54-d Bed B parameter vector from t0080 applied via
`apply_parameter_vector`; the morphology is the t0092-patched procedural generator
`generate_fixed_morphology` (canonical via correction C-0093-01) parameterised by 14
additional dimensions covering soma offset, dendritic asymmetry, branch density, branch
density gradient, and related morphological knobs. The combined parameter space is
68-dimensional.

The new run differs from t0106 only in the stimulus angle list: ANGLES_DEG goes from the
two-element antipodal pair [0, 180] to the eight-element [0, 45, 90, 135, 180, 225, 270, 315].
The stimulus profile (1400 ms moving bar, AR(2)-correlated rate noise per t0024, parametric
synapse placer per t0080) is unchanged. Three noise replicates per direction (eval_seeds =
111, 222, 333) give 24 simulations per cell.

NEURON code ran on a Vast.ai EPYC 7532 32-effective-core instance (offer 33356672, dph
$0.36815) using `concurrent.futures.ProcessPoolExecutor` with `max_workers=10` -- one worker
per cell, no within-cell parallelism. The remote wall clock for the full 10-cell run was 547.2
s (9.12 min); per-cell wall clock ranged from 30.4 s (rank 45) to 547.1 s (rank 5, an outlier
with very expensive NEURON dynamics). Total compute cost was $0.15 against the project's
remaining $18.35 headroom.

## Data

No external dataset is consumed. Input vectors are the full 68-d parameter vectors of the 10
cells sampled from the t0106 top-50. The sampling procedure is reproducible: load
`tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json.gz`, deduplicate
by `(round(DSI, 4), round(PD, 2))`, rank by joint-corner score `min(DSI/0.5, 1) x min(PD/30,
1)`, break ties by `dsi + pd/100`, take the top 50, then draw 10 indices with
`numpy.random.default_rng(42).choice(50, size=10, replace=False)`.

The 10 selected cells have t0106 ranks 4, 5, 10, 20, 29, 33, 34, 40, 45, 50. Their
t0106-reported 2-direction ratio DSI ranges from 0.843 (rank 34) to 0.979 (rank 33); their
t0106-reported PD-rates range from 84.29 Hz (rank 50) to 121.67 Hz (rank 5). The same cells
are stored in `code/selected_cells.json` for full reproducibility.

## Prediction Format

The file `files/per_cell_polar_eval.json` is a single JSON object with three top-level keys
plus the `evaluations` payload:

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
* `per_direction_rates_hz`: list of 8 floats, mean firing rate per direction (Hz) across the 3
  noise replicates
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
  (Spearman rho = **0.758**, p = 0.011) but is consistently lower in absolute value (mean 0.52
  vs 0.87). The rank ordering is preserved, supporting the interpretation that the t0106
  reformulation is a metric simplification rather than a corner artefact, but the t0106 ratio
  DSI systematically overstates the strength of selectivity by absorbing off-axis spike mass
  into the PD/ND pair alone.
* The 2-direction ratio DSI sanity check from the 8-direction data agrees closely with the
  original t0106 numbers (sanity-DSI mean 0.87 vs t0106 mean 0.94; only rank 4 and rank 34
  drift more than 0.3), confirming that the 2-direction protocol itself is reproducible and
  the discrepancy comes from the angular sampling, not from random noise or evaluator drift.
* Rank 4 is the most striking discrepancy: t0106 reported DSI = 0.935 at PD = 121.4 Hz, but in
  the 8-direction re-evaluation the PD firing rate of 121.4 Hz is matched by an ND rate of
  41.9 Hz, pulling the ratio sanity DSI down to 0.487 and the vector-sum DSI to 0.305. This
  single cell diverged most from the t0106 number, suggesting the 2-direction protocol can
  occasionally pick cells with a partial null-direction response that the 8-direction sweep
  exposes.

## Summary

This asset records the 8-direction polar re-evaluation of 10 cells randomly sampled from the
t0106 top-50. The cells were evaluated with the same NEURON evaluator pipeline as t0106 but
with the angle list extended from [0, 180] to [0, 45, 90, 135, 180, 225, 270, 315]. All 10
cells completed without NEURON errors. The Vast.ai EPYC 7532 instance ran the 10-cell parallel
pool in 547 s of wall clock at a total cost of $0.15.

The headline finding is that the t0106 2-direction ratio DSI and the t0107 8-direction
vector-sum DSI are positively correlated (Spearman rho = 0.758, p = 0.011) but with
substantial absolute drift (mean 0.87 vs 0.52). The rank ordering of cells is largely
preserved, supporting the t0106 reformulation as a useful metric proxy, but the 8-direction
sweep reveals that several cells have non-trivial off-axis firing that the 2-direction
protocol does not capture. The 2-direction ratio DSI sanity check from the 8-direction PD/ND
rates agrees closely with t0106's numbers (only one cell drifts by more than 0.3), ruling out
evaluator-level reproducibility issues. The full per-cell per-direction firing-rate vectors
are stored for downstream polar tuning-curve plotting and any future angle-resolved analyses.

</details>

<details>
<summary>📊 <strong>NSGA-II seed 44 on 68-d Bed B + 14-d morphology, 2 directions,
300-gen target</strong> (<code>nsga2-seed44-bedb-morph-2dir-300gen</code>)
— 3744 instances (json.gz)</summary>

| Field | Value |
|---|---|
| **ID** | `nsga2-seed44-bedb-morph-2dir-300gen` |
| **Model ID** | — |
| **Model** | Compartmental DSGC neuron model combining the 54-d Bed B electrophysiology parameter vector (from t0080) applied via apply_parameter_vector with the t0092-patched 14-d procedural morphology generator (canonical via correction C-0093-01). Each cell is evaluated with 2 stimulus directions (PD = 0 deg, ND = 180 deg) x 3 noise replicates and scored on a 2-objective vector (ratio DSI, preferred-direction firing rate in Hz). NSGA-II minimises the negated pair; the DSI silence guard from S-0102-01 clamps DSI to 0.0 when total PD+ND spike count falls below 10 spikes per trial. |
| **Datasets** |  |
| **Format** | json.gz |
| **Instances** | 3744 |
| **Date created** | 2026-05-18 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Created by** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **Documentation** | [`description.md`](../../../tasks\t0106_long_pdnd_nsga2_300gen\assets\predictions\nsga2-seed44-bedb-morph-2dir-300gen\description.md) |

**Metrics at creation:**

* **n_generations_completed**: 40
* **n_cells_total**: 3744
* **best_dsi_ratio**: 1.0
* **best_pd_rate_hz**: 122.62
* **n_joint_pass_unique**: 123
* **n_joint_pass_evaluations**: 637
* **final_hypervolume**: 122.0288
* **final_cost_usd**: 10.37

# NSGA-II seed 44 Bed B + morphology 2-direction 300-gen target

## Metadata

* **Name**: NSGA-II seed 44 on 68-d Bed B + 14-d morphology, 2 directions, 300-gen target
* **Model**: DSGC compartmental model (54-d Bed B electrophys via t0080 apply_parameter_vector
  + t0092-patched procedural morphology, canonical via C-0093-01)
* **Datasets**: none (simulator outputs)
* **Format**: json (single top-level object with `evaluations` list)
* **Instances**: 3,744 per-cell evaluations across 40 NSGA-II generations
* **Created by**: t0106_long_pdnd_nsga2_300gen

## Overview

This predictions asset captures every cell evaluated by the t0106 single-seed NSGA-II run on
the 2-direction landscape: PD bar at 0 degrees and ND bar at 180 degrees, ratio DSI as the
selectivity objective. The run targeted 300 generations on GA seed 44, but the operator
stopped after generation 40 once hourly HV polling showed the trace flat (less than 1% gain
over 60 minutes).

The asset documents the **first joint-pass cells ever observed in the t0080 - t0104 - t0106
NSGA-II lineage**: 123 unique cells with DSI >= 0.5 AND PD >= 30 Hz across 3,744 evaluations
(3.3% yield). Every prior task in the lineage returned exactly zero joint-pass cells. The
reformulation from 16-direction vector-sum DSI to 2-direction ratio DSI is what produced the
breakthrough; the longer generation budget (40 vs 12) was secondary.

Each cell is recorded with its full 68-d parameter vector, the NSGA-II generation index, both
objectives (ratio DSI and preferred-direction firing rate), and the negated objective vector
that NSGA-II actually minimised. The DSI silence guard from S-0102-01 is active throughout:
cells whose total PD+ND spike count across the 3 trials falls below 10 are clamped to DSI =
0.0 before being returned to NSGA-II selection.

## Model

The simulator is a compartmental DSGC neuron model on top of NEURON 8.2.7 / NetPyNE 1.1.1. The
electrophysiological substrate is the 54-d Bed B parameter vector from t0080 applied via
`apply_parameter_vector`; the morphology is the t0092-patched procedural generator
`generate_fixed_morphology` (canonical via correction C-0093-01) parameterised by 14
additional dimensions covering soma offset, dendritic asymmetry, branch density, branch
density gradient, and related morphological knobs. The combined parameter space is
68-dimensional.

Each cell is evaluated by 2 NEURON simulations (PD bar at 0 degrees, ND bar at 180 degrees) x
3 noise replicates = 6 simulations per cell. The selectivity objective is the ratio DSI =
(PD_rate - ND_rate) / (PD_rate + ND_rate), which is mathematically identical to the vector-sum
DSI for antipodal sampling but well-defined for the 2-direction configuration. The DSI silence
guard from S-0102-01 forces DSI = 0.0 when the cell's total spike count across PD + ND falls
below 10 per trial.

Pymoo NSGA-II configuration: pop_size = 96, n_gen = 300 target, n_eval_seeds = 3, single GA
seed = 44 (LHS-initialised initial population, explicit `np.random.SeedSequence(44)` seeding),
SBX crossover eta = 15 prob = 0.9, polynomial mutation eta = 20 prob = 1/68, duplicate
elimination enabled. The driver implements `PerGenerationPoolRestart(every=25)` — a new t0106
mitigation that closes and re-creates the multiprocessing.Pool every 25 gens to reset
NEURON-accumulated worker memory. The restart fired off-by-one at gen 26 and dropped
per-generation wall-clock from 110 min back to 3 min.

## Data

No external dataset is consumed. Input vectors are 68-dimensional points sampled by NSGA-II
starting from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and
explicitly seeded with task_seed = 44. Bounds for the 68 parameters are inherited unchanged
from the t0102 / t0099 substrate (the same 54-d electrophys bounds from t0080 plus the 14-d
morphology bounds from t0090 patched via t0093). Noise replicates within each evaluation use
the three deterministically spawned RNG seeds drawn from `np.random.SeedSequence(42).spawn(5)`
(the same seed family used by t0102 and t0104).

The 2-direction restriction (PD = 0 deg, ND = 180 deg) is the central change relative to
t0104's 16-direction sampling. ANGLES_DEG is reduced from a 16-element list every 22.5 deg to
the two-element antipodal pair, cutting per-cell NEURON cost from 64 simulations to 6 —
roughly a 10x speed-up per cell that funds the longer generation horizon.

## Prediction Format

The file `files/all_evaluations_seed44.json` is a single JSON object with one key,
`evaluations`, mapping to a list of 3,744 per-cell evaluation records. Each record has the
following fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..40 = offspring generations).
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector.
* `objective_F_minimised`: list of 2 floats, the NSGA-II objective vector after sign-flipping
  for maximisation, i.e. `[-ratio_dsi, -pd_rate_hz]`. NSGA-II minimises this pair directly.
* `dsi_vector_sum`: float in [0, 1], the ratio DSI = (PD_rate - ND_rate) / (PD_rate + ND_rate)
  averaged across the 3 noise replicates. The field name `dsi_vector_sum` is preserved for
  schema compatibility with t0102 / t0104; under 2-direction antipodal sampling, the
  vector-sum DSI reduces exactly to the ratio DSI. Guard-cleaned per S-0102-01 at total-spike
  threshold 10 per trial, so values of 0.0 may either reflect a real ratio of zero or the
  silence guard floor.
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 3
  replicates).

The strict 2-axis joint-pass flag `joint_pass = (dsi_vector_sum >= 0.5) AND (pd_rate_hz >=
30)` is not stored per-record but is trivially recomputable from the above two fields. 123 of
the 3,744 records satisfy this corner.

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **3,744** |
| Generations completed | **40** of 300 (operator stop at HV plateau) |
| Best ratio DSI (guard-cleaned) | **1.0000** at PD = 81.43 Hz |
| Best PD-rate frontier (Hz) | **122.62** at DSI = 0.92 |
| Unique joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz) | **123** |
| Joint-pass evaluations (with NSGA-II repetition) | **637** |
| Cells with DSI > 0.9 AND PD > 80 Hz | **24** unique (114 evals) |
| Joint-pass yield | **3.3%** (123 / 3,744) |
| Final hypervolume (2-D) | **122.0288** (start 0.2015; 604x growth) |
| Final NSGA-II compute cost (USD) | **$10.37** of $25 cap |

The joint-pass yield of **3.3%** exceeds the upper bound of published acceptance rates for
NSGA-II on comparable biophysical fits by roughly 8x (Druckmann2007 = 0.10%, Hay2011 = 0.40%,
Achard2006 = 0.028%). Best ratio DSI = **1.0000** exceeds the published DSGC biological
reference (Trenholm2013 mouse Hb9 control DSI = 0.76).

## Main Ideas

* The run produced the **first joint-pass cells in the t0080 - t0104 NSGA-II lineage** (123
  unique, 637 evaluations). Every prior task returned exactly 0 joint-pass cells. The
  reformulation from 16-direction vector-sum DSI to 2-direction ratio DSI is what made the
  corner reachable — generation budget alone (40 vs 12) was secondary.
* Per-cell `vector_68d` is sufficient to re-evaluate any cell off-line at higher noise
  replicate count, with 16 directions, or with alternative selectivity definitions, without
  re-running NSGA-II. The 24 unique DSGC-like cells (DSI > 0.9 AND PD > 80 Hz) are the primary
  follow-up targets for the N_EVAL_SEEDS = 20 robustness check (S-0106-02) and the
  16-direction re-evaluation (S-0106-03).
* The HV trace climbed from 0.2015 (gen 1) to 122.0288 (gen 40) — a 604x growth over 40
  generations — and was effectively flat (less than 1% per 60 min) by gen 36. The operator
  stop at gen 40 spent only $10.37 of the $25 cap. The empirical convergence point on the
  2-direction substrate is therefore approximately gen 36; subsequent generations contribute
  only vector-space exploration.

## Summary

This asset records every NSGA-II evaluation from the t0106 single-seed long-horizon run on the
68-d Bed B + 14-d morphology substrate, restricted to two antipodal directions (PD = 0 deg, ND
= 180 deg) with the ratio DSI as the selectivity objective. The run targeted 300 generations
on GA seed 44, completed 40 generations, and was operator-stopped at HV plateau for a total
cost of $10.37 against the $25 cap. The DSI silence guard from S-0102-01 was active
throughout.

The headline finding is that **123 of 3,744 evaluated cells (3.3%) cleared the strict 2-axis
joint-pass corner** (DSI >= 0.5 AND PD >= 30 Hz) — the first joint-pass cells anywhere in the
t0080 - t0104 - t0106 NSGA-II lineage. Best ratio DSI was 1.0000 at PD = 81.43 Hz; best
PD-rate frontier was 122.62 Hz at DSI = 0.92. The full 68-d parameter vector for every cell is
preserved, enabling targeted follow-ups (robustness re-evaluation at N_EVAL_SEEDS = 20,
16-direction re-evaluation, archetype-conditioned morphology sweeps) without re-running
NSGA-II.

The asset is the primary evidence channel for the t0106 answer asset
`t0106-joint-pass-recovery-2dir`. It also serves as the substrate-confirmation predecessor for
the multi-seed confirmation (S-0106-01), robustness retest (S-0106-02), and algorithm
comparison follow-ups (S-0106-06 IBEA on the working 2-direction substrate).

</details>

## 2026-05-12 (4)

<details>
<summary>📊 <strong>NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS
random init)</strong> (<code>nsga2-seed44-bedb-morph-n4-gen20</code>) —
1344 instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `nsga2-seed44-bedb-morph-n4-gen20` |
| **Model ID** | — |
| **Model** | Compartmental DSGC neuron model with the t0092-patched procedural morphology generator (canonical via correction C-0093-01) and the 54-d Bed B electrophys parameter vector applied via t0080's apply_parameter_vector. Each cell is evaluated with 16 stimulus directions x 4 noise replicates; NSGA-II minimises the negated triple (DSI vector-sum, PD-rate, robustness). |
| **Datasets** |  |
| **Format** | jsonl |
| **Instances** | 1344 |
| **Date created** | 2026-05-12 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Created by** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Documentation** | [`description.md`](../../../tasks\t0102_seedscale_n4_gen20\assets\predictions\nsga2-seed44-bedb-morph-n4-gen20\description.md) |

**Metrics at creation:**

* **n_generations_completed**: 14
* **n_cells**: 1344
* **max_dsi**: 1.0
* **max_pd_rate_hz**: 64.28571428571429
* **max_robustness**: 0.991628794830278
* **n_joint_pass**: 0
* **hypervolume_final**: 7.532779084144153
* **final_cost_usd**: 4.094182907241769

# NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init)

## Metadata

* **Name**: NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init)
* **Model**: DSGC compartmental model (t0092-patched procedural morphology + 54-d Bed B
  electrophys vector via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 1,344 per-cell evaluations across 14 NSGA-II generations
* **Created by**: t0102_seedscale_n4_gen20

## Overview

This predictions asset records every cell evaluated by the NSGA-II run with GA seed=44 in
t0102. The run is one of two independent random-init restarts (44 and 55) that test whether
dropping per-cell noise replicates from t0099's N_EVAL_SEEDS=5 down to 4 and extending
generations from 8 up to 20 recovers the strict joint-pass corner of objective space (DSI >=
0.5, preferred-direction firing rate >= 30 Hz, robustness >= 0.7) that t0099 failed to find
with 3 random-init seeds.

Each line of the JSONL captures one DSGC compartmental simulation: the 68-d parameter vector
(54 electrophys knobs + 14 morphology knobs), the three NSGA-II objectives (DSI vector-sum,
preferred-direction firing rate, robustness as inverse CV across noise replicates), and a
precomputed strict joint-pass flag. Together with the matched seed-other asset and the
per-seed history JSONs in `results/data/`, this is the raw evidence for the t0102 answer
asset.

The seed terminated at generation 14 after the per-seed cost watchdog tripped at the $4
budget; final hypervolume was 7.5328 and final cost $4.0942.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via correction C-0093-01) and the 54-d Bed B
electrophys parameter vector applied via t0080's `apply_parameter_vector`. Per-cell evaluation
runs 16 stimulus directions x 4 noise replicates with objectives = (DSI vector-sum,
preferred-direction firing rate in Hz, robustness as inverse CV of DSI across the 4 noise
replicates), all maximised. Pymoo NSGA-II minimises the negated triple. Crossover SBX eta=15
with prob=0.9; polynomial mutation eta=20 with prob=1/68; elimination of duplicates enabled.
Population size 96, max generations 20, LHS-initialised initial population with explicit
`np.random.SeedSequence` seeding for reproducibility.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting
from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and
explicitly seeded with task_seed=44. Bounds for the 68 parameters are inherited unchanged from
the t0099 / t0091 substrate (the same 54-d electrophys bounds from t0080 plus the 14-d
morphology bounds from t0090). Noise replicates inside each evaluation use the four
deterministically spawned RNG seeds (2684470948, 4091952314, 233227757, 3276785861) drawn from
`np.random.SeedSequence(42).spawn(5)` -- one fewer than t0099's five replicates.

## Prediction Format

JSONL with one line per evaluated cell (1,344 lines total). Each line is a JSON object with
fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..N = offspring generations)
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector
* `dsi_vector_sum`: float in [0, 1], vector-sum direction selectivity index averaged across
  the 4 noise replicates
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 4
  replicates)
* `robustness`: float in [0, 1], inverse CV of DSI across the 4 noise replicates
* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND `pd_rate_hz >= 30` AND `robustness
  >= 0.7` (the strict task-level biological-plausibility corner)

Example line (formatted for readability):

```
{
  "generation": 14,
  "vector_68d": [0.4576, 0.0550, ..., 0.2229],
  "dsi_vector_sum": 0.4321,
  "pd_rate_hz": 22.43,
  "robustness": 0.8104,
  "joint_pass": false
}
```

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **1,344** |
| Generations completed | **14** / 20 |
| Best DSI (vector sum) | **1.0000** |
| Best preferred-direction rate (Hz) | **64.29** |
| Best robustness (inverse CV) | **0.9916** |
| Strict joint-pass cells | **0** |
| Final hypervolume | **7.5328** |
| Final NSGA-II compute cost (USD) | **$4.0942** |

The strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz AND robustness >= 0.7) is met
by **0** of the 1,344 evaluated cells.

## Main Ideas

* The run terminated at generation 14 after the per-seed cost watchdog tripped at $4.00, not
  at the planned generation 20 -- the per-cell wall-clock at N_EVAL_SEEDS=4 was higher than
  the optimistic projection in the plan's cost table.
* Zero of the 1,344 evaluated cells cleared the strict joint-pass corner. Best per-axis maxima
  are DSI=1.0000, PD-rate=64.29 Hz, robustness=0.9916, all individually inside their
  thresholds for some cell but never simultaneously for the same cell.
* The per-cell vector_68d is sufficient to re-evaluate or re-score any cell without re-running
  the optimiser, enabling downstream noise-budget studies and joint comparisons against
  t0091's warm-started Pareto and t0099's three random-init seeds.

## Summary

This asset captures all 1,344 NSGA-II evaluations from the t0102 random-init run with GA
seed=44, covering generations 1 through 14. Each cell is a 68-d point in the Bed B electrophys
+ procedural morphology parameter space, evaluated with 16 stimulus directions and 4 noise
replicates against the triple objective (DSI vector-sum, preferred-direction firing rate,
robustness).

The headline finding is that zero cells cleared the strict joint-pass corner. Best individual
axes were DSI=1.0000, PD=64.29 Hz, and robustness=0.9916. Combined with the matched
second-seed asset and the t0099 three-seed prior, this gives a 0/2 task-level reproducibility
outcome for the joint-pass corner, reinforcing the negative result that random initialisation
alone (no warm-start anchors) does not recover the biologically plausible region at this
compute budget.

The asset is the primary evidence channel for the t0102 answer asset. Cost watchdog triggered
at $4.00 of compute (actual $4.0942 final reading), terminating the run at generation 14 short
of the planned 20.

</details>

<details>
<summary>📊 <strong>NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS
random init, 2-objective DSI+PD, DSI silence guard)</strong>
(<code>nsga2-seed44-bedb-morph-n4-gen20-2obj</code>) — 1152 instances
(jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `nsga2-seed44-bedb-morph-n4-gen20-2obj` |
| **Model ID** | — |
| **Model** | Compartmental DSGC neuron model with the t0092-patched procedural morphology generator (canonical via correction C-0093-01) and the 54-d Bed B electrophys parameter vector applied via t0080's apply_parameter_vector. Each cell is evaluated with 16 stimulus directions x 4 noise replicates; NSGA-II minimises the negated pair (DSI vector-sum, PD-rate) — robustness is computed per cell but does NOT enter NSGA-II selection in t0104 (REQ-2). The DSI silence guard (REQ-3) clamps DSI to 0.0 when the cell's total mean spikes across directions fall below 10, eliminating the t0102 silence-corner artifact. |
| **Datasets** |  |
| **Format** | jsonl |
| **Instances** | 1152 |
| **Date created** | 2026-05-12 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Created by** | [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **Documentation** | [`description.md`](../../../tasks\t0104_nsga2_2obj_dsi_pdrate_3seeds\assets\predictions\nsga2-seed44-bedb-morph-n4-gen20-2obj\description.md) |

**Metrics at creation:**

* **n_generations_completed**: 12
* **n_cells**: 1152
* **max_dsi**: 0.40725524513608247
* **max_pd_rate_hz**: 75.0
* **n_joint_pass**: 0
* **n_at_guard_floor**: 25
* **hypervolume_final**: 2.854543785086947
* **final_cost_usd**: 4.694470022747195

# NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init, 2-objective DSI+PD, DSI silence guard)

## Metadata

* **Name**: NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init,
  2-objective DSI+PD, DSI silence guard)
* **Model**: DSGC compartmental model (t0092-patched procedural morphology + 54-d Bed B
  electrophys vector via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 1,152 per-cell evaluations across 12 NSGA-II generations
* **Created by**: t0104_nsga2_2obj_dsi_pdrate_3seeds

## Overview

This predictions asset records every cell evaluated by the t0104 NSGA-II run with GA seed=44.
The run is one of three independent random-init restarts (44, 55, 66) that test whether
dropping the robustness axis from NSGA-II's objective vector (3 -> 2) and applying the DSI
silence guard (S-0102-01) recover joint-pass cells where t0102's 3-objective N=4 run found
zero across 2,592 cells.

Each line of the JSONL captures one DSGC compartmental simulation: the 68-d parameter vector
(54 electrophys knobs + 14 morphology knobs), the two NSGA-II objectives (DSI vector-sum and
preferred-direction firing rate), and a precomputed strict 2-axis joint-pass flag (DSI >= 0.5
AND PD
>= 30 Hz). Robustness is computed internally per cell by the evaluator but is not persisted to this
JSONL because it is no longer an NSGA-II objective in t0104.

The seed terminated at generation 12 (either at the planned 20 cap or earlier via the cost
watchdog at $4.00 per seed); final hypervolume in the 2-D (DSI, PD) plane was 2.8545 and final
cost $4.6945.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via correction C-0093-01) and the 54-d Bed B
electrophys parameter vector applied via t0080's `apply_parameter_vector`. Per-cell evaluation
runs 16 stimulus directions x 4 noise replicates with objectives = (DSI vector-sum,
preferred-direction firing rate in Hz), both maximised. Pymoo NSGA-II minimises the negated
pair. Crossover SBX eta=15 with prob=0.9; polynomial mutation eta=20 with prob=1/68;
elimination of duplicates enabled. Population size 96, max generations 20, LHS-initialised
initial population with explicit `np.random.SeedSequence` seeding for reproducibility. The DSI
silence guard (REQ-3) is active: cells whose total mean spike count across the 16 directions
falls below 10 have DSI clamped to 0.0 before being returned to NSGA-II.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting
from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and
explicitly seeded with task_seed=44. Bounds for the 68 parameters are inherited unchanged from
the t0102 / t0099 substrate (the same 54-d electrophys bounds from t0080 plus the 14-d
morphology bounds from t0090). Noise replicates inside each evaluation use the four
deterministically spawned RNG seeds drawn from `np.random.SeedSequence(42).spawn(5)`.

## Prediction Format

JSONL with one line per evaluated cell (1,152 lines total). Each line is a JSON object with
fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..N = offspring generations)
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector
* `dsi_vector_sum`: float in [0, 1], vector-sum direction selectivity index averaged across
  the 4 noise replicates (guard-cleaned per REQ-3 at threshold 10)
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 4
  replicates)
* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND `pd_rate_hz >= 30` (the t0104
  strict 2-axis biological-plausibility corner; t0102's robustness >= 0.7 threshold is dropped
  because robustness is no longer an NSGA-II objective)

Example line (formatted for readability):

```
{
  "generation": 14,
  "vector_68d": [0.4576, 0.0550, ..., 0.2229],
  "dsi_vector_sum": 0.4321,
  "pd_rate_hz": 22.43,
  "joint_pass": false
}
```

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **1,152** |
| Generations completed | **12** / 20 |
| Best DSI (vector sum, guard-cleaned) | **0.4073** |
| Best preferred-direction rate (Hz) | **75.00** |
| Strict joint-pass cells (DSI >= 0.5 AND PD >= 30) | **0** |
| Cells at DSI guard floor (DSI = 0.0) | **25** |
| Final hypervolume (2-D) | **2.8545** |
| Final NSGA-II compute cost (USD) | **$4.6945** |

The 2-axis strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz) is met by **0** of
the 1,152 evaluated cells.

## Main Ideas

* The run terminated at generation 12 (either at the planned cap of 20 or earlier via the
  per-seed cost watchdog at $4.00). Per-cell wall-clock at N_EVAL_SEEDS=4 was the operative
  throughput constant; the predictions JSONL captures every evaluation up to the termination
  point.
* 0 of the 1,152 evaluated cells cleared the strict 2-axis joint-pass corner (DSI >= 0.5 AND
  PD >= 30 Hz). Best per-axis maxima are DSI=0.4073 and PD-rate=75.00 Hz on the guard-cleaned
  DSI.
* 25 of the 1,152 cells are at the DSI guard floor (DSI = 0.0 because total mean spikes < 10);
  these are the cells that would have produced the t0102 silence-corner artifact at DSI = 1.0
  without the guard. Per-cell `vector_68d` is sufficient to re-evaluate any cell without
  re-running the optimiser.

## Summary

This asset captures all 1,152 NSGA-II evaluations from the t0104 random-init 2-objective run
with GA seed=44, covering generations 1 through 12. Each cell is a 68-d point in the Bed B
electrophys + procedural morphology parameter space, evaluated with 16 stimulus directions and
4 noise replicates against the 2-dimensional objective (DSI vector-sum, preferred-direction
firing rate). The DSI silence guard from S-0102-01 is active throughout.

The headline finding for this seed is that 0 of the evaluated cells cleared the strict 2-axis
joint-pass corner. Best individual axes were DSI=0.4073 and PD=75.00 Hz. Combined with the
matched two-other-seed assets in t0104 and the t0102 three-objective prior, this contributes
one of three apples-to-apples comparisons of the 2-objective vs 3-objective NSGA-II
formulations on the same substrate.

The asset is a primary evidence channel for the t0104 answer asset. Cost watchdog and
HV-plateau termination jointly govern run length; the final cost reading was $4.6945 and the
run reached generation 12 of the planned 20.

</details>

<details>
<summary>📊 <strong>NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS
random init)</strong> (<code>nsga2-seed55-bedb-morph-n4-gen20</code>) —
1248 instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `nsga2-seed55-bedb-morph-n4-gen20` |
| **Model ID** | — |
| **Model** | Compartmental DSGC neuron model with the t0092-patched procedural morphology generator (canonical via correction C-0093-01) and the 54-d Bed B electrophys parameter vector applied via t0080's apply_parameter_vector. Each cell is evaluated with 16 stimulus directions x 4 noise replicates; NSGA-II minimises the negated triple (DSI vector-sum, PD-rate, robustness). |
| **Datasets** |  |
| **Format** | jsonl |
| **Instances** | 1248 |
| **Date created** | 2026-05-12 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Created by** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Documentation** | [`description.md`](../../../tasks\t0102_seedscale_n4_gen20\assets\predictions\nsga2-seed55-bedb-morph-n4-gen20\description.md) |

**Metrics at creation:**

* **n_generations_completed**: 13
* **n_cells**: 1248
* **max_dsi**: 1.0
* **max_pd_rate_hz**: 66.96428571428572
* **max_robustness**: 0.9999999999999982
* **n_joint_pass**: 0
* **hypervolume_final**: 3.3926397249887454
* **final_cost_usd**: 4.3626048569322275

# NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init)

## Metadata

* **Name**: NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init)
* **Model**: DSGC compartmental model (t0092-patched procedural morphology + 54-d Bed B
  electrophys vector via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 1,248 per-cell evaluations across 13 NSGA-II generations
* **Created by**: t0102_seedscale_n4_gen20

## Overview

This predictions asset records every cell evaluated by the NSGA-II run with GA seed=55 in
t0102. The run is one of two independent random-init restarts (44 and 55) that test whether
dropping per-cell noise replicates from t0099's N_EVAL_SEEDS=5 down to 4 and extending
generations from 8 up to 20 recovers the strict joint-pass corner of objective space (DSI >=
0.5, preferred-direction firing rate >= 30 Hz, robustness >= 0.7) that t0099 failed to find
with 3 random-init seeds.

Each line of the JSONL captures one DSGC compartmental simulation: the 68-d parameter vector
(54 electrophys knobs + 14 morphology knobs), the three NSGA-II objectives (DSI vector-sum,
preferred-direction firing rate, robustness as inverse CV across noise replicates), and a
precomputed strict joint-pass flag. Together with the matched seed-other asset and the
per-seed history JSONs in `results/data/`, this is the raw evidence for the t0102 answer
asset.

The seed terminated at generation 13 after the per-seed cost watchdog tripped at the $4
budget; final hypervolume was 3.3926 and final cost $4.3626.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via correction C-0093-01) and the 54-d Bed B
electrophys parameter vector applied via t0080's `apply_parameter_vector`. Per-cell evaluation
runs 16 stimulus directions x 4 noise replicates with objectives = (DSI vector-sum,
preferred-direction firing rate in Hz, robustness as inverse CV of DSI across the 4 noise
replicates), all maximised. Pymoo NSGA-II minimises the negated triple. Crossover SBX eta=15
with prob=0.9; polynomial mutation eta=20 with prob=1/68; elimination of duplicates enabled.
Population size 96, max generations 20, LHS-initialised initial population with explicit
`np.random.SeedSequence` seeding for reproducibility.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting
from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and
explicitly seeded with task_seed=55. Bounds for the 68 parameters are inherited unchanged from
the t0099 / t0091 substrate (the same 54-d electrophys bounds from t0080 plus the 14-d
morphology bounds from t0090). Noise replicates inside each evaluation use the four
deterministically spawned RNG seeds (2684470948, 4091952314, 233227757, 3276785861) drawn from
`np.random.SeedSequence(42).spawn(5)` -- one fewer than t0099's five replicates.

## Prediction Format

JSONL with one line per evaluated cell (1,248 lines total). Each line is a JSON object with
fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..N = offspring generations)
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector
* `dsi_vector_sum`: float in [0, 1], vector-sum direction selectivity index averaged across
  the 4 noise replicates
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 4
  replicates)
* `robustness`: float in [0, 1], inverse CV of DSI across the 4 noise replicates
* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND `pd_rate_hz >= 30` AND `robustness
  >= 0.7` (the strict task-level biological-plausibility corner)

Example line (formatted for readability):

```
{
  "generation": 14,
  "vector_68d": [0.4576, 0.0550, ..., 0.2229],
  "dsi_vector_sum": 0.4321,
  "pd_rate_hz": 22.43,
  "robustness": 0.8104,
  "joint_pass": false
}
```

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **1,248** |
| Generations completed | **13** / 20 |
| Best DSI (vector sum) | **1.0000** |
| Best preferred-direction rate (Hz) | **66.96** |
| Best robustness (inverse CV) | **1.0000** |
| Strict joint-pass cells | **0** |
| Final hypervolume | **3.3926** |
| Final NSGA-II compute cost (USD) | **$4.3626** |

The strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz AND robustness >= 0.7) is met
by **0** of the 1,248 evaluated cells.

## Main Ideas

* The run terminated at generation 13 after the per-seed cost watchdog tripped at $4.00, not
  at the planned generation 20 -- the per-cell wall-clock at N_EVAL_SEEDS=4 was higher than
  the optimistic projection in the plan's cost table.
* Zero of the 1,248 evaluated cells cleared the strict joint-pass corner. Best per-axis maxima
  are DSI=1.0000, PD-rate=66.96 Hz, robustness=1.0000, all individually inside their
  thresholds for some cell but never simultaneously for the same cell.
* The per-cell vector_68d is sufficient to re-evaluate or re-score any cell without re-running
  the optimiser, enabling downstream noise-budget studies and joint comparisons against
  t0091's warm-started Pareto and t0099's three random-init seeds.

## Summary

This asset captures all 1,248 NSGA-II evaluations from the t0102 random-init run with GA
seed=55, covering generations 1 through 13. Each cell is a 68-d point in the Bed B electrophys
+ procedural morphology parameter space, evaluated with 16 stimulus directions and 4 noise
replicates against the triple objective (DSI vector-sum, preferred-direction firing rate,
robustness).

The headline finding is that zero cells cleared the strict joint-pass corner. Best individual
axes were DSI=1.0000, PD=66.96 Hz, and robustness=1.0000. Combined with the matched
second-seed asset and the t0099 three-seed prior, this gives a 0/2 task-level reproducibility
outcome for the joint-pass corner, reinforcing the negative result that random initialisation
alone (no warm-start anchors) does not recover the biologically plausible region at this
compute budget.

The asset is the primary evidence channel for the t0102 answer asset. Cost watchdog triggered
at $4.00 of compute (actual $4.3626 final reading), terminating the run at generation 13 short
of the planned 20.

</details>

<details>
<summary>📊 <strong>NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS
random init, 2-objective DSI+PD, DSI silence guard)</strong>
(<code>nsga2-seed55-bedb-morph-n4-gen20-2obj</code>) — 1056 instances
(jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `nsga2-seed55-bedb-morph-n4-gen20-2obj` |
| **Model ID** | — |
| **Model** | Compartmental DSGC neuron model with the t0092-patched procedural morphology generator (canonical via correction C-0093-01) and the 54-d Bed B electrophys parameter vector applied via t0080's apply_parameter_vector. Each cell is evaluated with 16 stimulus directions x 4 noise replicates; NSGA-II minimises the negated pair (DSI vector-sum, PD-rate) — robustness is computed per cell but does NOT enter NSGA-II selection in t0104 (REQ-2). The DSI silence guard (REQ-3) clamps DSI to 0.0 when the cell's total mean spikes across directions fall below 10, eliminating the t0102 silence-corner artifact. |
| **Datasets** |  |
| **Format** | jsonl |
| **Instances** | 1056 |
| **Date created** | 2026-05-12 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Created by** | [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **Documentation** | [`description.md`](../../../tasks\t0104_nsga2_2obj_dsi_pdrate_3seeds\assets\predictions\nsga2-seed55-bedb-morph-n4-gen20-2obj\description.md) |

**Metrics at creation:**

* **n_generations_completed**: 11
* **n_cells**: 1056
* **max_dsi**: 0.541672311572628
* **max_pd_rate_hz**: 65.0
* **n_joint_pass**: 0
* **n_at_guard_floor**: 22
* **hypervolume_final**: 7.5934794279519995
* **final_cost_usd**: 4.187365977185278

# NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init, 2-objective DSI+PD, DSI silence guard)

## Metadata

* **Name**: NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init,
  2-objective DSI+PD, DSI silence guard)
* **Model**: DSGC compartmental model (t0092-patched procedural morphology + 54-d Bed B
  electrophys vector via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 1,056 per-cell evaluations across 11 NSGA-II generations
* **Created by**: t0104_nsga2_2obj_dsi_pdrate_3seeds

## Overview

This predictions asset records every cell evaluated by the t0104 NSGA-II run with GA seed=55.
The run is one of three independent random-init restarts (44, 55, 66) that test whether
dropping the robustness axis from NSGA-II's objective vector (3 -> 2) and applying the DSI
silence guard (S-0102-01) recover joint-pass cells where t0102's 3-objective N=4 run found
zero across 2,592 cells.

Each line of the JSONL captures one DSGC compartmental simulation: the 68-d parameter vector
(54 electrophys knobs + 14 morphology knobs), the two NSGA-II objectives (DSI vector-sum and
preferred-direction firing rate), and a precomputed strict 2-axis joint-pass flag (DSI >= 0.5
AND PD
>= 30 Hz). Robustness is computed internally per cell by the evaluator but is not persisted to this
JSONL because it is no longer an NSGA-II objective in t0104.

The seed terminated at generation 11 (either at the planned 20 cap or earlier via the cost
watchdog at $4.00 per seed); final hypervolume in the 2-D (DSI, PD) plane was 7.5935 and final
cost $4.1874.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via correction C-0093-01) and the 54-d Bed B
electrophys parameter vector applied via t0080's `apply_parameter_vector`. Per-cell evaluation
runs 16 stimulus directions x 4 noise replicates with objectives = (DSI vector-sum,
preferred-direction firing rate in Hz), both maximised. Pymoo NSGA-II minimises the negated
pair. Crossover SBX eta=15 with prob=0.9; polynomial mutation eta=20 with prob=1/68;
elimination of duplicates enabled. Population size 96, max generations 20, LHS-initialised
initial population with explicit `np.random.SeedSequence` seeding for reproducibility. The DSI
silence guard (REQ-3) is active: cells whose total mean spike count across the 16 directions
falls below 10 have DSI clamped to 0.0 before being returned to NSGA-II.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting
from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and
explicitly seeded with task_seed=55. Bounds for the 68 parameters are inherited unchanged from
the t0102 / t0099 substrate (the same 54-d electrophys bounds from t0080 plus the 14-d
morphology bounds from t0090). Noise replicates inside each evaluation use the four
deterministically spawned RNG seeds drawn from `np.random.SeedSequence(42).spawn(5)`.

## Prediction Format

JSONL with one line per evaluated cell (1,056 lines total). Each line is a JSON object with
fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..N = offspring generations)
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector
* `dsi_vector_sum`: float in [0, 1], vector-sum direction selectivity index averaged across
  the 4 noise replicates (guard-cleaned per REQ-3 at threshold 10)
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 4
  replicates)
* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND `pd_rate_hz >= 30` (the t0104
  strict 2-axis biological-plausibility corner; t0102's robustness >= 0.7 threshold is dropped
  because robustness is no longer an NSGA-II objective)

Example line (formatted for readability):

```
{
  "generation": 14,
  "vector_68d": [0.4576, 0.0550, ..., 0.2229],
  "dsi_vector_sum": 0.4321,
  "pd_rate_hz": 22.43,
  "joint_pass": false
}
```

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **1,056** |
| Generations completed | **11** / 20 |
| Best DSI (vector sum, guard-cleaned) | **0.5417** |
| Best preferred-direction rate (Hz) | **65.00** |
| Strict joint-pass cells (DSI >= 0.5 AND PD >= 30) | **0** |
| Cells at DSI guard floor (DSI = 0.0) | **22** |
| Final hypervolume (2-D) | **7.5935** |
| Final NSGA-II compute cost (USD) | **$4.1874** |

The 2-axis strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz) is met by **0** of
the 1,056 evaluated cells.

## Main Ideas

* The run terminated at generation 11 (either at the planned cap of 20 or earlier via the
  per-seed cost watchdog at $4.00). Per-cell wall-clock at N_EVAL_SEEDS=4 was the operative
  throughput constant; the predictions JSONL captures every evaluation up to the termination
  point.
* 0 of the 1,056 evaluated cells cleared the strict 2-axis joint-pass corner (DSI >= 0.5 AND
  PD >= 30 Hz). Best per-axis maxima are DSI=0.5417 and PD-rate=65.00 Hz on the guard-cleaned
  DSI.
* 22 of the 1,056 cells are at the DSI guard floor (DSI = 0.0 because total mean spikes < 10);
  these are the cells that would have produced the t0102 silence-corner artifact at DSI = 1.0
  without the guard. Per-cell `vector_68d` is sufficient to re-evaluate any cell without
  re-running the optimiser.

## Summary

This asset captures all 1,056 NSGA-II evaluations from the t0104 random-init 2-objective run
with GA seed=55, covering generations 1 through 11. Each cell is a 68-d point in the Bed B
electrophys + procedural morphology parameter space, evaluated with 16 stimulus directions and
4 noise replicates against the 2-dimensional objective (DSI vector-sum, preferred-direction
firing rate). The DSI silence guard from S-0102-01 is active throughout.

The headline finding for this seed is that 0 of the evaluated cells cleared the strict 2-axis
joint-pass corner. Best individual axes were DSI=0.5417 and PD=65.00 Hz. Combined with the
matched two-other-seed assets in t0104 and the t0102 three-objective prior, this contributes
one of three apples-to-apples comparisons of the 2-objective vs 3-objective NSGA-II
formulations on the same substrate.

The asset is a primary evidence channel for the t0104 answer asset. Cost watchdog and
HV-plateau termination jointly govern run length; the final cost reading was $4.1874 and the
run reached generation 11 of the planned 20.

</details>

## 2026-05-10 (3)

<details>
<summary>📊 <strong>Random-init Pareto front seed 11</strong>
(<code>random-init-pareto-seed11</code>) — 19 instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `random-init-pareto-seed11` |
| **Model ID** | — |
| **Model** | DSGC compartmental model with t0092-patched procedural morphology + 54-d electrophys vector, evaluated by 16-direction x 5-seed NSGA-II starting from a Latin Hypercube Sample of the 68-d parameter space. |
| **Datasets** |  |
| **Format** | jsonl |
| **Instances** | 19 |
| **Date created** | 2026-05-10 |
| **Categories** | — |
| **Created by** | [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md) |
| **Documentation** | [`description.md`](../../../tasks\t0099_random_init_pareto_robustness\assets\predictions\random-init-pareto-seed11\description.md) |

# Random-init Pareto front seed 11

## Metadata

* **Name**: Random-init Pareto front seed 11
* **Model**: DSGC compartmental model (t0092-patched procedural morphology generator + 54-d
  electrophys vector applied via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 19 Pareto cells
* **Created by**: t0099_random_init_pareto_robustness

## Overview

This predictions asset records the 19-cell Pareto front of one of three random-init NSGA-II
reproducibility runs in t0099 (task seed 11, RNG seeds chosen from {11, 22, 33}). The run
mirrors t0091's joint 68-d NSGA-II configuration (population 96, up to 8 generations, SBX
eta=15, polynomial mutation eta=20 with prob=1/68, eliminate_duplicates=True, 16 directions x
5 evaluation seeds per cell, HV-plateau + cost-watchdog termination) but replaces t0091's
5-anchor warm-start population with a fresh Latin Hypercube Sample over the 68-d parameter
bounds. The cost cap was $1.00 per seed instead of t0091's $4.00, reflecting the reduced scope
of a reproducibility check.

The intended use of this asset is direct comparison against t0091's
`pareto-front-68d-morphology-extended-bedb-v3` predictions: identical evaluator, identical
priors, identical objective space — only the initial population and the RNG seeds differ.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via `C-0093-01`) and the t0080 54-d electrophys
parameter vector applied via `apply_parameter_vector`. Per-cell evaluation runs 16 stimulus
directions x 5 evaluation seeds with objectives = (DSI vector-sum, PD firing rate, robustness
as inverse CV of DSI across seeds), all maximised. Pymoo NSGA-II minimises the negated
objectives.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting
from a 96-row LHS sample drawn with `pymoo LatinHypercubeSampling` and explicitly seeded via
`np.random.SeedSequence(11)`.

## Prediction Format

JSONL with one line per Pareto cell. Each line is a JSON object with fields:

* `cell_id`: int (unique within this seed)
* `task_seed`: int = 11
* `dsi_vector_sum`: float, vector-sum direction selectivity index
* `pd_rate_hz`: float, preferred-direction mean firing rate (Hz)
* `robustness`: float in [0, 1], inverse CV of DSI across 5 evaluation seeds
* `morphology_vector_14d`: list[float], 14 morphology knobs (concatenated 54+14 layout)
* `electrophys_vector_54d`: list[float], 54 electrophys / synaptic parameters
* `nearest_anchor_index`: int in 0..4, nearest of t0091's 5 fixed anchors in
  min-max-normalised 14-d morphology space
* `nearest_anchor_name`: str (bedb_like / symmetric / pd_asymmetric / nd_asymmetric /
  alt_topology)
* `nearest_anchor_distance_normalised`: float, Euclidean distance to nearest anchor in
  normalised morphology space
* `verdict_biological`: str (plausible / stretched / exotic / no_data), worst-case 13-prior
  aggregation

## Metrics

Per-cell metrics live in `pareto_cells.jsonl`. Aggregate metrics are in
`results/metrics.json`.

Anchor distribution for this seed:

* `bedb_like`: 2 cells
* `symmetric`: 0 cells
* `pd_asymmetric`: 7 cells
* `nd_asymmetric`: 5 cells
* `alt_topology`: 5 cells

Biological-plausibility verdict counts:

* plausible: 0
* stretched: 0
* exotic: 19

Strict joint-pass count (DSI >= 0.5 AND PD-rate >= 30 Hz AND robust >= 0.7): **0**

## Main Ideas

* This is one of three independent random-init replicates of t0091's joint 68-d NSGA-II run,
  used to test reproducibility under RNG variation and the load-bearing role of the 5-anchor
  warm-start.
* The Pareto front records every non-dominated cell from the NSGA-II run; the per-cell
  vector_68d is sufficient to re-evaluate or re-score any cell without re-running the
  optimiser.
* Anchor classification here is post-hoc — the run itself never used anchors to seed the
  population, so the nearest-anchor labels reflect the geometry found by random search +
  NSGA-II selection rather than warm-start bias.

## Summary

This asset captures the Pareto front of a random-init NSGA-II run with task seed 11 (19
cells). It is one of three replicates whose cross-comparison drives the headline answer asset
``random_init_reproducibility_and_warmstart_dependence``. Each line of the JSONL file carries
the 68-d parameter vector, the three NSGA-II objectives, the post-hoc anchor classification,
and the 13-prior biological verdict — all required inputs for the cross-seed and
warm-start-dependence analyses.

The intended downstream uses are direct comparison with t0091's Pareto front (anchor
distribution, plausibility verdicts, strict joint-pass count) and possible re-scoring under
future biological priors without re-running the NSGA-II loop.

</details>

<details>
<summary>📊 <strong>Random-init Pareto front seed 22</strong>
(<code>random-init-pareto-seed22</code>) — 22 instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `random-init-pareto-seed22` |
| **Model ID** | — |
| **Model** | DSGC compartmental model with t0092-patched procedural morphology + 54-d electrophys vector, evaluated by 16-direction x 5-seed NSGA-II starting from a Latin Hypercube Sample of the 68-d parameter space. |
| **Datasets** |  |
| **Format** | jsonl |
| **Instances** | 22 |
| **Date created** | 2026-05-10 |
| **Categories** | — |
| **Created by** | [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md) |
| **Documentation** | [`description.md`](../../../tasks\t0099_random_init_pareto_robustness\assets\predictions\random-init-pareto-seed22\description.md) |

# Random-init Pareto front seed 22

## Metadata

* **Name**: Random-init Pareto front seed 22
* **Model**: DSGC compartmental model (t0092-patched procedural morphology generator + 54-d
  electrophys vector applied via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 22 Pareto cells
* **Created by**: t0099_random_init_pareto_robustness

## Overview

This predictions asset records the 22-cell Pareto front of one of three random-init NSGA-II
reproducibility runs in t0099 (task seed 22, RNG seeds chosen from {11, 22, 33}). The run
mirrors t0091's joint 68-d NSGA-II configuration (population 96, up to 8 generations, SBX
eta=15, polynomial mutation eta=20 with prob=1/68, eliminate_duplicates=True, 16 directions x
5 evaluation seeds per cell, HV-plateau + cost-watchdog termination) but replaces t0091's
5-anchor warm-start population with a fresh Latin Hypercube Sample over the 68-d parameter
bounds. The cost cap was $1.00 per seed instead of t0091's $4.00, reflecting the reduced scope
of a reproducibility check.

The intended use of this asset is direct comparison against t0091's
`pareto-front-68d-morphology-extended-bedb-v3` predictions: identical evaluator, identical
priors, identical objective space — only the initial population and the RNG seeds differ.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via `C-0093-01`) and the t0080 54-d electrophys
parameter vector applied via `apply_parameter_vector`. Per-cell evaluation runs 16 stimulus
directions x 5 evaluation seeds with objectives = (DSI vector-sum, PD firing rate, robustness
as inverse CV of DSI across seeds), all maximised. Pymoo NSGA-II minimises the negated
objectives.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting
from a 96-row LHS sample drawn with `pymoo LatinHypercubeSampling` and explicitly seeded via
`np.random.SeedSequence(22)`.

## Prediction Format

JSONL with one line per Pareto cell. Each line is a JSON object with fields:

* `cell_id`: int (unique within this seed)
* `task_seed`: int = 22
* `dsi_vector_sum`: float, vector-sum direction selectivity index
* `pd_rate_hz`: float, preferred-direction mean firing rate (Hz)
* `robustness`: float in [0, 1], inverse CV of DSI across 5 evaluation seeds
* `morphology_vector_14d`: list[float], 14 morphology knobs (concatenated 54+14 layout)
* `electrophys_vector_54d`: list[float], 54 electrophys / synaptic parameters
* `nearest_anchor_index`: int in 0..4, nearest of t0091's 5 fixed anchors in
  min-max-normalised 14-d morphology space
* `nearest_anchor_name`: str (bedb_like / symmetric / pd_asymmetric / nd_asymmetric /
  alt_topology)
* `nearest_anchor_distance_normalised`: float, Euclidean distance to nearest anchor in
  normalised morphology space
* `verdict_biological`: str (plausible / stretched / exotic / no_data), worst-case 13-prior
  aggregation

## Metrics

Per-cell metrics live in `pareto_cells.jsonl`. Aggregate metrics are in
`results/metrics.json`.

Anchor distribution for this seed:

* `bedb_like`: 4 cells
* `symmetric`: 0 cells
* `pd_asymmetric`: 4 cells
* `nd_asymmetric`: 2 cells
* `alt_topology`: 12 cells

Biological-plausibility verdict counts:

* plausible: 0
* stretched: 0
* exotic: 22

Strict joint-pass count (DSI >= 0.5 AND PD-rate >= 30 Hz AND robust >= 0.7): **0**

## Main Ideas

* This is one of three independent random-init replicates of t0091's joint 68-d NSGA-II run,
  used to test reproducibility under RNG variation and the load-bearing role of the 5-anchor
  warm-start.
* The Pareto front records every non-dominated cell from the NSGA-II run; the per-cell
  vector_68d is sufficient to re-evaluate or re-score any cell without re-running the
  optimiser.
* Anchor classification here is post-hoc — the run itself never used anchors to seed the
  population, so the nearest-anchor labels reflect the geometry found by random search +
  NSGA-II selection rather than warm-start bias.

## Summary

This asset captures the Pareto front of a random-init NSGA-II run with task seed 22 (22
cells). It is one of three replicates whose cross-comparison drives the headline answer asset
``random_init_reproducibility_and_warmstart_dependence``. Each line of the JSONL file carries
the 68-d parameter vector, the three NSGA-II objectives, the post-hoc anchor classification,
and the 13-prior biological verdict — all required inputs for the cross-seed and
warm-start-dependence analyses.

The intended downstream uses are direct comparison with t0091's Pareto front (anchor
distribution, plausibility verdicts, strict joint-pass count) and possible re-scoring under
future biological priors without re-running the NSGA-II loop.

</details>

<details>
<summary>📊 <strong>Random-init Pareto front seed 33</strong>
(<code>random-init-pareto-seed33</code>) — 14 instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `random-init-pareto-seed33` |
| **Model ID** | — |
| **Model** | DSGC compartmental model with t0092-patched procedural morphology + 54-d electrophys vector, evaluated by 16-direction x 5-seed NSGA-II starting from a Latin Hypercube Sample of the 68-d parameter space. |
| **Datasets** |  |
| **Format** | jsonl |
| **Instances** | 14 |
| **Date created** | 2026-05-10 |
| **Categories** | — |
| **Created by** | [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md) |
| **Documentation** | [`description.md`](../../../tasks\t0099_random_init_pareto_robustness\assets\predictions\random-init-pareto-seed33\description.md) |

# Random-init Pareto front seed 33

## Metadata

* **Name**: Random-init Pareto front seed 33
* **Model**: DSGC compartmental model (t0092-patched procedural morphology generator + 54-d
  electrophys vector applied via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 14 Pareto cells
* **Created by**: t0099_random_init_pareto_robustness

## Overview

This predictions asset records the 14-cell Pareto front of one of three random-init NSGA-II
reproducibility runs in t0099 (task seed 33, RNG seeds chosen from {11, 22, 33}). The run
mirrors t0091's joint 68-d NSGA-II configuration (population 96, up to 8 generations, SBX
eta=15, polynomial mutation eta=20 with prob=1/68, eliminate_duplicates=True, 16 directions x
5 evaluation seeds per cell, HV-plateau + cost-watchdog termination) but replaces t0091's
5-anchor warm-start population with a fresh Latin Hypercube Sample over the 68-d parameter
bounds. The cost cap was $1.00 per seed instead of t0091's $4.00, reflecting the reduced scope
of a reproducibility check.

The intended use of this asset is direct comparison against t0091's
`pareto-front-68d-morphology-extended-bedb-v3` predictions: identical evaluator, identical
priors, identical objective space — only the initial population and the RNG seeds differ.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via `C-0093-01`) and the t0080 54-d electrophys
parameter vector applied via `apply_parameter_vector`. Per-cell evaluation runs 16 stimulus
directions x 5 evaluation seeds with objectives = (DSI vector-sum, PD firing rate, robustness
as inverse CV of DSI across seeds), all maximised. Pymoo NSGA-II minimises the negated
objectives.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting
from a 96-row LHS sample drawn with `pymoo LatinHypercubeSampling` and explicitly seeded via
`np.random.SeedSequence(33)`.

## Prediction Format

JSONL with one line per Pareto cell. Each line is a JSON object with fields:

* `cell_id`: int (unique within this seed)
* `task_seed`: int = 33
* `dsi_vector_sum`: float, vector-sum direction selectivity index
* `pd_rate_hz`: float, preferred-direction mean firing rate (Hz)
* `robustness`: float in [0, 1], inverse CV of DSI across 5 evaluation seeds
* `morphology_vector_14d`: list[float], 14 morphology knobs (concatenated 54+14 layout)
* `electrophys_vector_54d`: list[float], 54 electrophys / synaptic parameters
* `nearest_anchor_index`: int in 0..4, nearest of t0091's 5 fixed anchors in
  min-max-normalised 14-d morphology space
* `nearest_anchor_name`: str (bedb_like / symmetric / pd_asymmetric / nd_asymmetric /
  alt_topology)
* `nearest_anchor_distance_normalised`: float, Euclidean distance to nearest anchor in
  normalised morphology space
* `verdict_biological`: str (plausible / stretched / exotic / no_data), worst-case 13-prior
  aggregation

## Metrics

Per-cell metrics live in `pareto_cells.jsonl`. Aggregate metrics are in
`results/metrics.json`.

Anchor distribution for this seed:

* `bedb_like`: 1 cells
* `symmetric`: 0 cells
* `pd_asymmetric`: 9 cells
* `nd_asymmetric`: 0 cells
* `alt_topology`: 4 cells

Biological-plausibility verdict counts:

* plausible: 0
* stretched: 0
* exotic: 14

Strict joint-pass count (DSI >= 0.5 AND PD-rate >= 30 Hz AND robust >= 0.7): **0**

## Main Ideas

* This is one of three independent random-init replicates of t0091's joint 68-d NSGA-II run,
  used to test reproducibility under RNG variation and the load-bearing role of the 5-anchor
  warm-start.
* The Pareto front records every non-dominated cell from the NSGA-II run; the per-cell
  vector_68d is sufficient to re-evaluate or re-score any cell without re-running the
  optimiser.
* Anchor classification here is post-hoc — the run itself never used anchors to seed the
  population, so the nearest-anchor labels reflect the geometry found by random search +
  NSGA-II selection rather than warm-start bias.

## Summary

This asset captures the Pareto front of a random-init NSGA-II run with task seed 33 (14
cells). It is one of three replicates whose cross-comparison drives the headline answer asset
``random_init_reproducibility_and_warmstart_dependence``. Each line of the JSONL file carries
the 68-d parameter vector, the three NSGA-II objectives, the post-hoc anchor classification,
and the 13-prior biological verdict — all required inputs for the cross-seed and
warm-start-dependence analyses.

The intended downstream uses are direct comparison with t0091's Pareto front (anchor
distribution, plausibility verdicts, strict joint-pass count) and possible re-scoring under
future biological priors without re-running the NSGA-II loop.

</details>

## 2026-05-08 (1)

<details>
<summary>📊 <strong>Pareto front 68-d morphology-extended Bed-B v3</strong>
(<code>pareto-front-68d-morphology-extended-bedb-v3</code>) — 57 instances
(jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `pareto-front-68d-morphology-extended-bedb-v3` |
| **Model ID** | — |
| **Model** | DSGC compartmental model with t0092-patched procedural morphology + 54-d electrophys parameter vector applied via t0080 apply_params. |
| **Datasets** |  |
| **Format** | jsonl |
| **Instances** | 57 |
| **Date created** | 2026-05-08 |
| **Categories** | — |
| **Created by** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Documentation** | [`description.md`](../../../tasks\t0091_morphology_extended_nsga2_v1\assets\predictions\pareto-front-68d-morphology-extended-bedb-v3\description.md) |

# pareto-front-68d-morphology-extended-bedb-v3

## Metadata

* **Predictions ID**: `pareto-front-68d-morphology-extended-bedb-v3`
* **Created by task**: `t0091_morphology_extended_nsga2_v1`
* **Date created**: 2026-05-08
* **Format**: JSONL (one line per Pareto cell)
* **Instance count**: 57 Pareto cells

## Overview

Per-cell predictions from the t0091 joint 68-d NSGA-II Pareto front. This file documents 57
non-dominated cells from the 68-d joint (54-d electrophys + 14-d morphology) multi-objective
optimisation. The input substrate is the t0092-patched procedural DSGC morphology generator
(`generate_fixed_morphology`, canonical per correction overlay `C-0093-01`) applied per Pareto
cell; the electrophys vector is the t0080 54-d v3 parameter space (channel densities,
slow-AHP, synaptic, AIS geometry, dendritic-spike machinery).

This is the first NSGA-II run in this project to call the procedural morphology generator
inside the per-cell evaluation loop. All prior NSGA-II tasks (t0078, t0080, t0081, t0083,
t0086) ran on a fixed Bed-B substrate with 54-d electrophys parameters only; t0091 promotes
the 14 morphology knobs from t0090 to first-class optimisation variables, producing a 68-d
joint search space.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator and the
t0080 54-d electrophys parameter vector applied via `apply_parameter_vector`. The morphology
generator constructs a DSGC cell with a programmable soma, primary/non-terminal/terminal
dendrites, and AIS subsegments per the 14 morphology knobs (number of primary branches,
branching probability, max Strahler depth, mean branching angle, Rall exponent, soma offset
along PD, field elongation, branch density gradient, primary-branch concentration, mean
segment length, soma diameter, AIS length, deterministic morph seed, branch length CV).
Channel insertion uses the t0080 nrnmech library (12 t80 channel SUFFIXes plus skahpt80
slow-AHP); synapses are placed parametrically with ACh + GABA + Exp2NMDA bundles per the t0080
v3 recipe.

## Data

No external dataset is consumed; the predictions are simulator outputs. Input vectors are 68-d
points sampled by the NSGA-II algorithm starting from a 5-anchor warm-start population
(Bed-B-like + symmetric + PD-asymmetric + ND-asymmetric + alt-topology) each cloned with ~19
t0083 Pareto electrophys variants, plus 1 random LHS sample, total 96 cells.

## Prediction Format

JSONL with one line per Pareto cell. Each line is a JSON object with fields:

* `cell_id`: int, unique within this file
* `dsi_vector_sum`: float, vector-sum direction selectivity index
* `pd_rate_hz`: float, preferred-direction mean firing rate (Hz)
* `robustness`: float in [0, 1], inverse CV of DSI across 5 seeds
* `morphology_vector_14d`: list[float], 14 morphology knobs
* `electrophys_vector_54d`: list[float], 54 electrophys / synaptic params
* `nearest_anchor`: str, nearest of the 5 anchors in normalised 14-d morphology space
* `verdict_biological`: str, plausible / stretched / exotic per the 13-prior worst-case
  scorecard
* `v_opt_um_per_s`: float or null, cable-theoretic optimal bar velocity
* `effective_dendritic_length_um`: float or null, proxy total dendritic length

## Metrics

Per-cell metrics live in `pareto_cells.jsonl`. Aggregate metrics (per-anchor mean DSI and
robustness, all-Pareto mean DSI) live in `results/metrics.json` under the `explicit_variants`
schema.

## Main Ideas

* The 68-d Pareto front exposes the trade-off between direction selectivity (DSI), firing rate
  (PD-rate), and robustness across evaluation seeds.
* Anchor-tracking analysis classifies each Pareto cell to its nearest of 5 morphology anchors;
  over- or under-representation of PD-asymmetric vs ND-asymmetric anchors tests whether
  morphology asymmetry is functional.
* Per-cell biological scoring (9 electrophys + 4 morphology priors) identifies which Pareto
  cells reach the published-prior plausibility region.

## Summary

This predictions asset records the 57-cell Pareto front of the t0091 joint 68-d NSGA-II run
with the t0092 patched morphology generator inside the per-cell evaluation loop. Each cell is
evaluated on 16 directions x 5 seeds; objectives are DSI vector-sum, PD firing rate, and
robustness (inverse CV of DSI). Per-cell metadata includes the nearest anchor, biological
plausibility verdict, and cable-theoretic v_opt for downstream comparison with Hausselt 2007 /
Trenholm 2013.

The Pareto front is intended as the input to downstream literature comparison and follow-up
tasks: each cell carries enough metadata (electrophys vector, morphology vector, anchor,
biological verdict, cable v_opt, effective dendritic length) to support direction-selectivity
re-analysis, anchor-tracking statistical tests with bootstrap CIs, and biological-plausibility
scoring without re-running the simulator.

</details>

## 2026-04-21 (2)

<details>
<summary>📊 <strong>V_rest sweep on t0022 DSGC channel testbed
(deterministic)</strong> (<code>t0026-vrest-sweep-t0022</code>) — 96
instances (csv)</summary>

| Field | Value |
|---|---|
| **ID** | `t0026-vrest-sweep-t0022` |
| **Model ID** | — |
| **Model** | ModelDB 189347 DSGC compartmental model (Mazurek lab) ported in t0008 and modified in t0022 to expose deterministic per-dendrite E-I scheduling. The model uses HHst membrane (with leak reversal eleak_HHst) on the soma and pas membrane (with e_pas) on dendrites, plus deterministic glutamate/GABA stimulus pairs constructed by tasks/t0022_modify_dsgc_channel_testbed/code (library asset modeldb_189347_dsgc). The V_rest is shifted by overriding both h.v_init and the resting parameters of every HHst- and pas-bearing section before h.finitialize. |
| **Datasets** |  |
| **Format** | csv |
| **Instances** | 96 |
| **Date created** | 2026-04-21 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Created by** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Documentation** | [`description.md`](../../../tasks\t0026_vrest_sweep_tuning_curves_dsgc\assets\predictions\t0026-vrest-sweep-t0022\description.md) |

**Metrics at creation:**

* **best_dsi_across_vrest**: 0.6562
* **best_dsi_at_vrest_mv**: -60.0
* **min_hwhm_deg_across_vrest**: 0.8
* **peak_hz_at_minus_60mv**: 15.0
* **null_hz_at_minus_60mv**: 0.0

# V_rest sweep on t0022 DSGC channel testbed (deterministic)

## Metadata

* **Name**: V_rest sweep on t0022 DSGC channel testbed (deterministic)
* **Model**: t0022 DSGC channel testbed (library `modeldb_189347_dsgc` ported in t0008,
  exposed-knobs version in t0022) — ModelDB 189347 cable-theory DSGC with HHst soma and pas
  dendrites, deterministic per-dendrite glutamate/GABA scheduling
* **Datasets**: none (synthetic stimulus generated in-script)
* **Format**: csv
* **Instances**: 96 (8 V_rest x 12 directions x 1 trial)
* **Created by**: t0026_vrest_sweep_tuning_curves_dsgc

## Overview

These predictions capture how the t0022 DSGC compartmental model responds to a moving-bar
stimulus across eight resting potentials spanning the physiological range (-90 mV to -20 mV in
10 mV steps). At each V_rest, the model is driven by the standard 12-direction protocol and
the per-trial spike count, peak somatic voltage, and firing rate are recorded.

V_rest is set by overriding both `h.v_init` and the resting parameters of every HHst- and
pas-bearing section (`eleak_HHst` and `e_pas`) before each trial's `h.finitialize`. Moving
both together (rather than just `v_init`) produces a true resting-potential shift instead of a
transient initial-condition tweak that would re-settle to `eleak` within a few milliseconds.

The t0022 model uses deterministic per-dendrite E-I scheduling, so a single trial per (V_rest,
angle) pair is sufficient to characterise the tuning curve — there is no trial-to-trial noise
to average out. The predictions support biophysical analysis of how V_rest modulates direction
tuning sharpness, peak firing rate, and HWHM via Na-channel inactivation and the resulting
changes in spike threshold.

## Model

The model is the ModelDB 189347 cable-theory DSGC originally published by the Mazurek lab and
ported in task t0008 (`modeldb_189347_dsgc`), then extended in t0022 to expose the
per-dendrite E-I scheduling knobs needed for parameter sweeps. Key biophysical parameters:

* Soma: HHst membrane (transient Na, K-DR, and leak), `eleak_HHst` is the leak reversal that
  determines V_rest in the absence of synaptic drive.
* Dendrites: pas membrane (passive cable) with `e_pas` reversal.
* Synapses: per-dendrite (glutamate, GABA) pairs scheduled deterministically by the t0022
  simulation harness based on motion direction (282 pairs constructed at cell build).

For each trial in this sweep, the harness:

1. Builds the cell once (cached in CellContext across the full sweep).
2. Resets the per-trial schedule using `apply_params + schedule_ei_onsets`.
3. Calls `set_vrest(h=h, v_rest_mv=V)` which writes V to `h.v_init`, all `eleak_HHst`, and all
   `e_pas`.
4. Runs `h.finitialize(V) + h.continuerun(TSTOP_MS)` for a 1-second simulation window.
5. Records spike count (threshold crossings of the soma), peak somatic mV, and firing rate.

## Data

No external dataset is consumed. The stimulus is a synthetic moving bar at 12 evenly spaced
directions (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330 deg), with the stimulus
schedule generated by the t0022 simulation harness. The same per-direction onset schedule is
used for every V_rest value, so cross-V_rest differences are attributable to membrane
biophysics, not stimulus variation.

## Prediction Format

`files/predictions-vrest-sweep-t0022.csv` is a UTF-8 CSV with header row and 96 data rows.
Columns:

| Column | Type | Description |
| --- | --- | --- |
| `v_rest_mv` | float | Resting potential set by `set_vrest`, one of -90/-80/-70/-60/-50/-40/-30/-20 mV |
| `trial` | int | Trial index per (V_rest, angle); always 0 for this deterministic sweep |
| `direction_deg` | int | Motion direction in degrees, one of 0/30/60/90/120/150/180/210/240/270/300/330 |
| `spike_count` | int | Count of soma spikes during the 1-second simulation window |
| `peak_mv` | float | Peak somatic membrane voltage during the trial, in mV |
| `firing_rate_hz` | float | spike_count / 1.0 s |

Example rows:

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-90.0,0,0,6,43.272,6.000000
-60.0,0,0,14,44.288,14.000000
-30.0,0,0,129,43.825,129.000000
```

## Metrics

Per-V_rest scalar metrics are derived in
`tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/compute_vrest_metrics.py` and stored in
`data/t0022/vrest_metrics.csv`. DSI is computed as the magnitude of the vector sum of mean
firing rates across angles, normalised by their sum (Mazurek convention). HWHM is
half-width-at-half-max of the mean firing-rate curve interpolated around the preferred
direction.

| V_rest (mV) | Peak Hz | Null Hz | DSI | HWHM (deg) | Pref dir (deg) |
| --- | --- | --- | --- | --- | --- |
| -90 | 6.00 | 0.00 | 0.485 | 0.8 | 19.4 |
| -80 | 11.00 | 0.00 | 0.600 | 0.8 | 42.3 |
| -70 | 12.00 | 0.00 | 0.637 | 84.0 | 50.7 |
| -60 | 15.00 | 0.00 | 0.656 | 86.2 | 49.3 |
| -50 | 41.00 | 20.41 | 0.205 | 102.2 | 42.4 |
| -40 | 70.00 | 50.64 | 0.095 | 180.0 | 49.1 |
| -30 | 129.00 | 111.20 | 0.046 | 180.0 | 48.0 |
| -20 | 26.00 | 7.40 | 0.275 | 107.8 | 48.0 |

## Main Ideas

* DSI peaks around V_rest = -60 mV (DSI = 0.656, HWHM = 86 deg) — close to the model's default
  resting potential — and degrades both when hyperpolarised below -80 mV (insufficient drive
  to cross spike threshold) and depolarised above -50 mV (null direction recruits
  suprathreshold firing, washing out selectivity).
* Peak firing rate is non-monotonic with V_rest: it climbs from 6 Hz at -90 to a maximum of
  129 Hz at -30, then collapses to 26 Hz at -20 mV consistent with Na-channel inactivation
  reducing spike availability when the membrane sits above approximately -25 mV.
* The sweep validates the multi-knob V_rest override approach: the deterministic t0022 model
  produces clean, reproducible tuning curves at every V_rest value, with no trial-to-trial
  noise. Downstream tasks can use this V_rest x direction grid to fit phenomenological models
  of resting-potential modulation of direction tuning.

## Summary

This predictions asset records the per-trial outcomes (96 rows) of the t0022 DSGC
compartmental model under a V_rest sweep across the eight values -90 / -80 / -70 / -60 / -50 /
-40 / -30 / -20 mV crossed with the 12-direction moving-bar protocol. V_rest is shifted by
simultaneously overriding `h.v_init`, all `eleak_HHst`, and all `e_pas` parameters before each
trial's `h.finitialize`, producing a stable steady-state V_rest rather than a transient.

The headline finding is a non-monotonic relationship between V_rest and direction selectivity:
DSI is maximised at V_rest approximately equal to -60 mV (DSI = 0.66) and collapses both at
hyperpolarised potentials (insufficient drive) and depolarised potentials (null-direction
firing washes out selectivity). Peak firing rate climbs monotonically until V_rest = -30 mV
(129 Hz) and then crashes at V_rest = -20 mV (26 Hz) consistent with sodium channel
inactivation. These predictions feed the polar plots in `results/images/` and the per-V_rest
metric grid in `results/metrics.json`, providing a baseline against which the stochastic t0024
DSGC model can be compared in the same task.

</details>

<details>
<summary>📊 <strong>V_rest sweep on t0024 DSGC channel testbed (stochastic AR(2)
release)</strong> (<code>t0026-vrest-sweep-t0024</code>) — 960 instances
(csv)</summary>

| Field | Value |
|---|---|
| **ID** | `t0026-vrest-sweep-t0024` |
| **Model ID** | — |
| **Model** | de Rosenroll 2026 DSGC compartmental model ported in t0024 (library asset de_rosenroll_2026_dsgc). The model uses HHst membrane (with leak reversal eleak_HHst) on the soma and pas membrane (with e_pas) on dendrites, plus per-dendrite AR(2)-correlated stochastic glutamate/GABA release with a default temporal correlation rho=0.6 between successive synaptic events. The V_rest is shifted by overriding both h.v_init and the resting parameters of every HHst- and pas-bearing section before h.finitialize. |
| **Datasets** |  |
| **Format** | csv |
| **Instances** | 960 |
| **Date created** | 2026-04-21 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Created by** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Documentation** | [`description.md`](../../../tasks\t0026_vrest_sweep_tuning_curves_dsgc\assets\predictions\t0026-vrest-sweep-t0024\description.md) |

**Metrics at creation:**

* **best_dsi_across_vrest**: 0.6754
* **best_dsi_at_vrest_mv**: -90.0
* **min_hwhm_deg_across_vrest**: 65.2
* **peak_hz_at_minus_60mv**: 5.0
* **null_hz_at_minus_60mv**: 0.51

# V_rest sweep on t0024 DSGC channel testbed (stochastic AR(2) release)

## Metadata

* **Name**: V_rest sweep on t0024 DSGC channel testbed (stochastic AR(2) release)
* **Model**: t0024 DSGC channel testbed (library asset `de_rosenroll_2026_dsgc`) — de
  Rosenroll 2026 cable-theory DSGC with HHst soma, pas dendrites, and AR(2)-correlated
  per-dendrite glutamate/GABA scheduling at default rho=0.6
* **Datasets**: none (synthetic stimulus generated in-script)
* **Format**: csv
* **Instances**: 960 (8 V_rest x 12 directions x 10 trials)
* **Created by**: t0026_vrest_sweep_tuning_curves_dsgc

## Overview

These predictions capture how the t0024 DSGC compartmental model responds to a moving-bar
stimulus across eight resting potentials spanning the physiological range (-90 mV to -20 mV in
10 mV steps). At each V_rest, the model is driven by the standard 12-direction protocol with
10 trials per angle to average out the trial-to-trial variability introduced by the
AR(2)-correlated stochastic release process (rho=0.6). For each trial the per-trial spike
count, peak somatic voltage, and firing rate are recorded.

V_rest is set by overriding both `h.v_init` and the resting parameters of every HHst- and
pas-bearing section (`eleak_HHst` and `e_pas`) before each trial's `h.finitialize`. Moving
both together (rather than just `v_init`) produces a true resting-potential shift instead of a
transient initial-condition tweak that would re-settle to `eleak` within a few milliseconds.

The t0024 model uses temporally correlated stochastic E-I release scheduling, so 10 trials per
(V_rest, angle) pair are required to estimate the mean firing rate against the variance
introduced by the AR(2) process. The total sweep runtime was 11,562 s (~3.21 h) on the local
Windows workstation. The predictions support biophysical analysis of how V_rest modulates
direction tuning sharpness, peak firing rate, and HWHM in the presence of physiologically
realistic correlated noise that the deterministic t0022 sister sweep cannot reproduce.

## Model

The model is the de Rosenroll 2026 DSGC ported in task t0024 (library asset
`de_rosenroll_2026_dsgc`), which extends the ModelDB-based DSGC architecture with
AR(2)-correlated per-dendrite stochastic release. Key biophysical parameters:

* Soma: HHst membrane (transient Na, K-DR, and leak), `eleak_HHst` is the leak reversal that
  determines V_rest in the absence of synaptic drive.
* Dendrites: pas membrane (passive cable) with `e_pas` reversal.
* Synapses: per-dendrite (glutamate, GABA) pairs scheduled by the t0024 simulation harness
  with AR(2) temporal correlation between successive events; rho=0.6 is the default
  correlation coefficient.

For each trial in this sweep, the harness:

1. Builds the cell once (cached in CellContext across the full sweep).
2. Resets the per-trial schedule using `apply_params + schedule_ei_onsets` with a fresh AR(2)
   draw.
3. Calls `set_vrest(h=h, v_rest_mv=V)` which writes V to `h.v_init`, all `eleak_HHst`, and all
   `e_pas`.
4. Runs `h.finitialize(V) + h.continuerun(TSTOP_MS)` for a 1-second simulation window.
5. Records spike count (threshold crossings of the soma), peak somatic mV, and firing rate.

## Data

No external dataset is consumed. The stimulus is a synthetic moving bar at 12 evenly spaced
directions (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330 deg), with the stimulus
schedule generated by the t0024 simulation harness. Each (V_rest, angle, trial) combination
receives a fresh AR(2)-correlated synaptic schedule, so cross-V_rest differences are
attributable to membrane biophysics and noise realisations, not deterministic stimulus
variation.

## Prediction Format

`files/predictions-vrest-sweep-t0024.csv` is a UTF-8 CSV with header row and 960 data rows.
Columns:

| Column | Type | Description |
| --- | --- | --- |
| `v_rest_mv` | float | Resting potential set by `set_vrest`, one of -90/-80/-70/-60/-50/-40/-30/-20 mV |
| `trial` | int | Trial index per (V_rest, angle); 0..9 for this stochastic sweep |
| `direction_deg` | int | Motion direction in degrees, one of 0/30/60/90/120/150/180/210/240/270/300/330 |
| `spike_count` | int | Count of soma spikes during the 1-second simulation window |
| `peak_mv` | float | Peak somatic membrane voltage during the trial, in mV |
| `firing_rate_hz` | float | spike_count / 1.0 s |

Example rows:

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-90.0,0,0,0,-26.118,0.000000
-60.0,0,0,3,38.792,3.000000
-20.0,0,0,8,42.611,8.000000
```

## Metrics

Per-V_rest scalar metrics are derived in
`tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/compute_vrest_metrics.py` and stored in
`data/t0024/vrest_metrics.csv`. Mean firing rate per (V_rest, angle) is computed across the 10
trials before DSI/HWHM evaluation. DSI uses the Mazurek vector-sum convention, normalised by
the sum of mean firing rates. HWHM is half-width-at-half-max of the mean firing-rate curve
interpolated around the preferred direction.

| V_rest (mV) | Peak Hz | Null Hz | DSI | HWHM (deg) | Pref dir (deg) |
| --- | --- | --- | --- | --- | --- |
| -90 | 1.50 | 0.00 | 0.675 | 65.2 | 351.6 |
| -80 | 2.70 | 0.06 | 0.549 | 68.4 | 350.4 |
| -70 | 4.00 | 0.26 | 0.470 | 70.5 | 355.6 |
| -60 | 5.00 | 0.51 | 0.446 | 78.5 | 0.9 |
| -50 | 6.30 | 0.30 | 0.560 | 70.0 | 6.8 |
| -40 | 6.80 | 0.00 | 0.625 | 67.7 | 10.7 |
| -30 | 7.40 | 0.16 | 0.590 | 66.5 | 11.5 |
| -20 | 7.60 | 1.88 | 0.361 | 83.3 | 11.9 |

## Main Ideas

* DSI is U-shaped across V_rest with maxima at the extremes (-90 mV: DSI = 0.675, -40 mV: DSI
  = 0.625) and a minimum near V_rest = -60 mV (DSI = 0.446) — a qualitatively different
  pattern from the t0022 deterministic sweep, where DSI peaks sharply at -60 mV and degrades
  monotonically away from it.
* Peak firing rate increases monotonically with depolarisation (1.5 Hz at -90 → 7.6 Hz at -20)
  with no hyper-depolarisation collapse from Na inactivation. The AR(2) noise apparently
  flattens the spike-availability response so the model never reaches the saturating regime
  that the deterministic t0022 model enters above -50 mV.
* HWHM is broad (65-83 deg) and only weakly modulated by V_rest in this stochastic model — in
  sharp contrast to t0022 where HWHM compresses to <1 deg below V=-60 because almost no spikes
  fire off the preferred direction. The AR(2) release introduces enough off-preferred firing
  to smooth the curve everywhere.
* The two strongest DSI conditions (-90 and -40 mV) bracket the model's default operating
  regime, suggesting that the AR(2) release stochasticity could be exploited by upstream
  circuitry to tune direction selectivity by adjusting the cell's holding potential — a
  possibility absent from the deterministic model.

## Summary

This predictions asset records the per-trial outcomes (960 rows) of the t0024 DSGC
compartmental model with AR(2)-correlated stochastic release (rho=0.6) under a V_rest sweep
across the eight values -90 / -80 / -70 / -60 / -50 / -40 / -30 / -20 mV crossed with the
12-direction moving-bar protocol and 10 trials per angle. V_rest is shifted by simultaneously
overriding `h.v_init`, all `eleak_HHst`, and all `e_pas` parameters before each trial's
`h.finitialize`, producing a stable steady-state V_rest rather than a transient.

The headline finding is a U-shaped DSI vs V_rest relationship: DSI is highest at the extremes
(-90 mV: DSI = 0.675; -40 mV: DSI = 0.625) and lowest near V_rest approximately equal to -60
mV (DSI = 0.446). Peak firing rate climbs monotonically with depolarisation (1.5 Hz at -90 to
7.6 Hz at -20) without the sharp collapse seen in the deterministic t0022 model at -20 mV.
HWHM is substantially broader (65-83 deg vs 0.8-180 deg in t0022), indicating that AR(2)
release smooths the angular tuning even at hyperpolarised V_rest where t0022 produces
near-binary responses. These predictions feed the polar plots in `results/images/` and the
per-V_rest metric grid in `results/metrics.json`, providing the stochastic counterpart to the
deterministic t0022 baseline in the same task.

</details>
