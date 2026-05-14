---
spec_version: "2"
predictions_id: "nsga2-seed44-bedb-morph-n4-gen20-2obj"
documented_by_task: "t0104_nsga2_2obj_dsi_pdrate_3seeds"
date_documented: "2026-05-12"
---
# NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init, 2-objective DSI+PD, DSI silence guard)

## Metadata

* **Name**: NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init, 2-objective
  DSI+PD, DSI silence guard)
* **Model**: DSGC compartmental model (t0092-patched procedural morphology + 54-d Bed B electrophys
  vector via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 1,152 per-cell evaluations across 12 NSGA-II generations
* **Created by**: t0104_nsga2_2obj_dsi_pdrate_3seeds

## Overview

This predictions asset records every cell evaluated by the t0104 NSGA-II run with GA seed=44. The
run is one of three independent random-init restarts (44, 55, 66) that test whether dropping the
robustness axis from NSGA-II's objective vector (3 -> 2) and applying the DSI silence guard
(S-0102-01) recover joint-pass cells where t0102's 3-objective N=4 run found zero across 2,592
cells.

Each line of the JSONL captures one DSGC compartmental simulation: the 68-d parameter vector (54
electrophys knobs + 14 morphology knobs), the two NSGA-II objectives (DSI vector-sum and
preferred-direction firing rate), and a precomputed strict 2-axis joint-pass flag (DSI >= 0.5 AND PD
>= 30 Hz). Robustness is computed internally per cell by the evaluator but is not persisted to this
JSONL because it is no longer an NSGA-II objective in t0104.

The seed terminated at generation 12 (either at the planned 20 cap or earlier via the cost watchdog
at $4.00 per seed); final hypervolume in the 2-D (DSI, PD) plane was 2.8545 and final cost $4.6945.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via correction C-0093-01) and the 54-d Bed B electrophys
parameter vector applied via t0080's `apply_parameter_vector`. Per-cell evaluation runs 16 stimulus
directions x 4 noise replicates with objectives = (DSI vector-sum, preferred-direction firing rate
in Hz), both maximised. Pymoo NSGA-II minimises the negated pair. Crossover SBX eta=15 with
prob=0.9; polynomial mutation eta=20 with prob=1/68; elimination of duplicates enabled. Population
size 96, max generations 20, LHS-initialised initial population with explicit
`np.random.SeedSequence` seeding for reproducibility. The DSI silence guard (REQ-3) is active: cells
whose total mean spike count across the 16 directions falls below 10 have DSI clamped to 0.0 before
being returned to NSGA-II.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting from a
96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and explicitly seeded with
task_seed=44. Bounds for the 68 parameters are inherited unchanged from the t0102 / t0099 substrate
(the same 54-d electrophys bounds from t0080 plus the 14-d morphology bounds from t0090). Noise
replicates inside each evaluation use the four deterministically spawned RNG seeds drawn from
`np.random.SeedSequence(42).spawn(5)`.

## Prediction Format

JSONL with one line per evaluated cell (1,152 lines total). Each line is a JSON object with fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..N = offspring generations)
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector
* `dsi_vector_sum`: float in [0, 1], vector-sum direction selectivity index averaged across the 4
  noise replicates (guard-cleaned per REQ-3 at threshold 10)
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 4 replicates)
* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND `pd_rate_hz >= 30` (the t0104 strict
  2-axis biological-plausibility corner; t0102's robustness >= 0.7 threshold is dropped because
  robustness is no longer an NSGA-II objective)

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

The 2-axis strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz) is met by **0** of the
1,152 evaluated cells.

## Main Ideas

* The run terminated at generation 12 (either at the planned cap of 20 or earlier via the per-seed
  cost watchdog at $4.00). Per-cell wall-clock at N_EVAL_SEEDS=4 was the operative throughput
  constant; the predictions JSONL captures every evaluation up to the termination point.
* 0 of the 1,152 evaluated cells cleared the strict 2-axis joint-pass corner (DSI >= 0.5 AND PD >=
  30 Hz). Best per-axis maxima are DSI=0.4073 and PD-rate=75.00 Hz on the guard-cleaned DSI.
* 25 of the 1,152 cells are at the DSI guard floor (DSI = 0.0 because total mean spikes < 10); these
  are the cells that would have produced the t0102 silence-corner artifact at DSI = 1.0 without the
  guard. Per-cell `vector_68d` is sufficient to re-evaluate any cell without re-running the
  optimiser.

## Summary

This asset captures all 1,152 NSGA-II evaluations from the t0104 random-init 2-objective run with GA
seed=44, covering generations 1 through 12. Each cell is a 68-d point in the Bed B electrophys +
procedural morphology parameter space, evaluated with 16 stimulus directions and 4 noise replicates
against the 2-dimensional objective (DSI vector-sum, preferred-direction firing rate). The DSI
silence guard from S-0102-01 is active throughout.

The headline finding for this seed is that 0 of the evaluated cells cleared the strict 2-axis
joint-pass corner. Best individual axes were DSI=0.4073 and PD=75.00 Hz. Combined with the matched
two-other-seed assets in t0104 and the t0102 three-objective prior, this contributes one of three
apples-to-apples comparisons of the 2-objective vs 3-objective NSGA-II formulations on the same
substrate.

The asset is a primary evidence channel for the t0104 answer asset. Cost watchdog and HV-plateau
termination jointly govern run length; the final cost reading was $4.6945 and the run reached
generation 12 of the planned 20.
