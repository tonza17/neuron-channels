---
spec_version: "2"
predictions_id: "nsga2-seed55-bedb-morph-n4-gen20"
documented_by_task: "t0102_seedscale_n4_gen20"
date_documented: "2026-05-12"
---
# NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init)

## Metadata

* **Name**: NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init)
* **Model**: DSGC compartmental model (t0092-patched procedural morphology + 54-d Bed B electrophys
  vector via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 1,248 per-cell evaluations across 13 NSGA-II generations
* **Created by**: t0102_seedscale_n4_gen20

## Overview

This predictions asset records every cell evaluated by the NSGA-II run with GA seed=55 in t0102. The
run is one of two independent random-init restarts (44 and 55) that test whether dropping per-cell
noise replicates from t0099's N_EVAL_SEEDS=5 down to 4 and extending generations from 8 up to 20
recovers the strict joint-pass corner of objective space (DSI >= 0.5, preferred-direction firing
rate >= 30 Hz, robustness >= 0.7) that t0099 failed to find with 3 random-init seeds.

Each line of the JSONL captures one DSGC compartmental simulation: the 68-d parameter vector (54
electrophys knobs + 14 morphology knobs), the three NSGA-II objectives (DSI vector-sum,
preferred-direction firing rate, robustness as inverse CV across noise replicates), and a
precomputed strict joint-pass flag. Together with the matched seed-other asset and the per-seed
history JSONs in `results/data/`, this is the raw evidence for the t0102 answer asset.

The seed terminated at generation 13 after the per-seed cost watchdog tripped at the $4 budget;
final hypervolume was 3.3926 and final cost $4.3626.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via correction C-0093-01) and the 54-d Bed B electrophys
parameter vector applied via t0080's `apply_parameter_vector`. Per-cell evaluation runs 16 stimulus
directions x 4 noise replicates with objectives = (DSI vector-sum, preferred-direction firing rate
in Hz, robustness as inverse CV of DSI across the 4 noise replicates), all maximised. Pymoo NSGA-II
minimises the negated triple. Crossover SBX eta=15 with prob=0.9; polynomial mutation eta=20 with
prob=1/68; elimination of duplicates enabled. Population size 96, max generations 20,
LHS-initialised initial population with explicit `np.random.SeedSequence` seeding for
reproducibility.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting from a
96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and explicitly seeded with
task_seed=55. Bounds for the 68 parameters are inherited unchanged from the t0099 / t0091 substrate
(the same 54-d electrophys bounds from t0080 plus the 14-d morphology bounds from t0090). Noise
replicates inside each evaluation use the four deterministically spawned RNG seeds (2684470948,
4091952314, 233227757, 3276785861) drawn from `np.random.SeedSequence(42).spawn(5)` -- one fewer
than t0099's five replicates.

## Prediction Format

JSONL with one line per evaluated cell (1,248 lines total). Each line is a JSON object with fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..N = offspring generations)
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector
* `dsi_vector_sum`: float in [0, 1], vector-sum direction selectivity index averaged across the 4
  noise replicates
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 4 replicates)
* `robustness`: float in [0, 1], inverse CV of DSI across the 4 noise replicates
* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND `pd_rate_hz >= 30` AND
  `robustness >= 0.7` (the strict task-level biological-plausibility corner)

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

The strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz AND robustness >= 0.7) is met by
**0** of the 1,248 evaluated cells.

## Main Ideas

* The run terminated at generation 13 after the per-seed cost watchdog tripped at $4.00, not at the
  planned generation 20 -- the per-cell wall-clock at N_EVAL_SEEDS=4 was higher than the optimistic
  projection in the plan's cost table.
* Zero of the 1,248 evaluated cells cleared the strict joint-pass corner. Best per-axis maxima are
  DSI=1.0000, PD-rate=66.96 Hz, robustness=1.0000, all individually inside their thresholds for some
  cell but never simultaneously for the same cell.
* The per-cell vector_68d is sufficient to re-evaluate or re-score any cell without re-running the
  optimiser, enabling downstream noise-budget studies and joint comparisons against t0091's
  warm-started Pareto and t0099's three random-init seeds.

## Summary

This asset captures all 1,248 NSGA-II evaluations from the t0102 random-init run with GA seed=55,
covering generations 1 through 13. Each cell is a 68-d point in the Bed B electrophys + procedural
morphology parameter space, evaluated with 16 stimulus directions and 4 noise replicates against the
triple objective (DSI vector-sum, preferred-direction firing rate, robustness).

The headline finding is that zero cells cleared the strict joint-pass corner. Best individual axes
were DSI=1.0000, PD=66.96 Hz, and robustness=1.0000. Combined with the matched second-seed asset and
the t0099 three-seed prior, this gives a 0/2 task-level reproducibility outcome for the joint-pass
corner, reinforcing the negative result that random initialisation alone (no warm-start anchors)
does not recover the biologically plausible region at this compute budget.

The asset is the primary evidence channel for the t0102 answer asset. Cost watchdog triggered at
$4.00 of compute (actual $4.3626 final reading), terminating the run at generation 13 short of the
planned 20.
