---
spec_version: "2"
predictions_id: "t0115-bedb-morph-nsga2-seed9354"
documented_by_task: "t0115_seed9354_no_autostop"
date_documented: "2026-05-21"
---
# NSGA-II seed 9354 on 68-d Bed B + 14-d morphology, 2 directions, 55-gen run with HV-plateau auto-stop DISABLED (5th seed of S-0112-01 batch)

## Metadata

* **Name**: NSGA-II seed 9354 on 68-d Bed B + 14-d morphology, 2 directions, 55-gen run with
  HV-plateau auto-stop DISABLED (5th seed of S-0112-01 batch)
* **Model**: Compartmental DSGC model (t0092-patched procedural morphology + 54-d Bed B electrophys
  vector via t0080 apply_parameter_vector)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl.gz
* **Instances**: 5,280 per-cell evaluations across 55 NSGA-II generations
* **Created by**: t0115_seed9354_no_autostop

## Overview

These predictions capture every cell evaluated by the t0115 single-seed NSGA-II run with GA
seed=9354 (5,280 cells across 55 generations). The run is the 5th and final seed in the S-0112-01
substrate-rate confirmation batch: t0106 (seed 44), t0112 (seed 77), t0113 (seed 2247), t0114 (seed
7755), and t0115 (seed 9354). Like t0114 it disables the HV-plateau auto-stop and terminates by
operator decision; the run reached gen 55 before being stopped after the HV trajectory visibly
plateaued near HV = 50.56.

The 63 unique LEGIT joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz AND DSI < 0.9999) collected by this
seed contribute the fifth data point to the substrate-rate estimate. The asset is the primary
evidence channel for the t0115 results summary, the 5-seed cross-comparison CSVs in `results/data/`,
and the literature comparison against Hay 2011 (0.40%) and Druckmann 2007 (0.10%).

## Model

Compartmental DSGC neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via correction C-0093-01) and the 54-d Bed B electrophys
parameter vector applied via t0080's `apply_parameter_vector`. Per-cell evaluation runs 2 stimulus
directions (PD = 0 deg, ND = 180 deg) x 3 noise replicates with objectives = (ratio DSI,
preferred-direction firing rate in Hz), both maximised. Pymoo NSGA-II minimises the negated pair.
Crossover SBX eta=15 with prob=0.9; polynomial mutation eta=20 with prob=1/68; duplicate elimination
enabled. Population size 96, n_gen_max=300 (HV-plateau auto-stop DISABLED, so the run terminates
only by cost cap or operator stop), LHS-initialised initial population with explicit
`np.random.SeedSequence` seeding for reproducibility. Pool restart cadence 10 (same as t0112 / t0113
/ t0114). The DSI silence guard from S-0102-01 is active: cells whose total PD+ND spike count across
the 2 directions falls below 10 have DSI clamped to 0.0 before being returned to NSGA-II.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting from a
96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and explicitly seeded with
task_seed=9354. Bounds for the 68 parameters are inherited unchanged from the
t0106/t0112/t0113/t0114 substrate (54-d Bed B electrophys bounds from t0080 + 14-d morphology bounds
from t0090). Noise replicates inside each evaluation use the 3 deterministically spawned RNG seeds
drawn from `np.random.SeedSequence(42).spawn(4)`.

## Prediction Format

Gzipped JSONL with one line per evaluated cell (5,280 lines total). Each line is a JSON object with
fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2-55 = offspring generations)
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector
* `objective_F_minimised`: list of 2 floats, the NSGA-II objective vector with sign-flipped
  maximisation conventions: [-ratio_dsi, -pd_rate_hz]
* `dsi_vector_sum`: float in [0, 1], ratio DSI = (PD - ND) / (PD + ND), guard-cleaned per S-0102-01
* `pd_rate_hz`: float, preferred-direction mean firing rate (Hz) across the 3 noise replicates
* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND `pd_rate_hz >= 30` (the 2-axis strict
  criterion)
* `legit`: bool, true iff `dsi_vector_sum < 0.9999` — false flags the silence-guard / single-spike
  DSI=1.0 ceiling artefact

Example line (formatted for readability):

```
{
  "generation": 54,
  "vector_68d": [0.4576, 0.0550, ..., 0.2229],
  "objective_F_minimised": [-0.9833, -28.33],
  "dsi_vector_sum": 0.9833,
  "pd_rate_hz": 28.33,
  "joint_pass": false,
  "legit": true
}
```

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **5,280** |
| Generations completed | **55** of 300 ceiling (operator stop) |
| Best DSI overall | **1.0000** (silence-guard ceiling) |
| Best legit DSI (non-silence-guard) | **0.9833** |
| Best PD-rate | **89.29 Hz** |
| Unique joint-pass cells (DSI >= 0.5 AND PD >= 30) | **63** |
| Unique LEGIT joint-pass cells (DSI < 0.9999) | **63** |
| Cells at DSI = 1.0 ceiling (silence-guard) | **64** |
| Final hypervolume (2-D) | **50.5646** |
| Stop trigger | **operator_stop** |

The 2-axis strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz) is met by **63** unique
cells across the 5,280 evaluations. Filtering out silence-guard ceiling cells leaves **63** LEGIT
joint-pass cells.

## Main Ideas

* The run terminated at generation 55 via operator stop after the HV trajectory visibly plateaued
  near 50.56; the HV-plateau auto-stop was DISABLED for this run.
* 63 of the 5,280 evaluated cells cleared the strict 2-axis LEGIT joint-pass corner — adding seed
  9354 as the fifth data point for the S-0112-01 substrate-rate estimate.
* The best legit cell reaches DSI = 0.9833 and the best PD-rate cell reaches PD = 89.29 Hz. Per-cell
  `vector_68d` is sufficient to re-evaluate any cell without re-running the optimiser.
* Seed 9354 lands in an intermediate yield bucket between the high-yield t0106 / t0114 seeds and the
  sparse t0112 / t0113 seeds, providing useful variance to characterise the substrate-rate
  distribution.

## Summary

This asset captures all 5,280 NSGA-II evaluations from the t0115 random-init 2-objective run with GA
seed=9354, covering generations 1 through 55. Each cell is a 68-d point in the Bed B electrophys +
procedural morphology parameter space, evaluated with 2 stimulus directions and 3 noise replicates
against the 2-dimensional objective (ratio DSI, preferred-direction firing rate). The DSI silence
guard from S-0102-01 is active throughout; the HV-plateau auto-stop is DISABLED.

The headline finding is **63 unique LEGIT joint-pass cells** — the fifth and final data point for
the S-0112-01 substrate-rate confirmation batch. Best individual axes were DSI=0.9833 (legit) and
PD=89.29 Hz; final hypervolume 50.5646.

Combined with the matched four-other-seed assets (t0106 / t0112 / t0113 / t0114), this contributes
the fifth data point to the substrate-rate confirmation batch and provides the primary evidence
channel for the 5-seed mean +/- SE bar chart vs Hay 2011 (0.40%) and Druckmann 2007 (0.10%)
literature baselines. Cost watchdog and operator stop jointly govern run length; the productive
NSGA-II compute cost was $2.39 of the $25 cap.
