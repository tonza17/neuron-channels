---
spec_version: "2"
predictions_id: "nsga2-seed44-bedb-morph-2dir-300gen"
documented_by_task: "t0106_long_pdnd_nsga2_300gen"
date_documented: "2026-05-18"
---
# NSGA-II seed 44 Bed B + morphology 2-direction 300-gen target

## Metadata

* **Name**: NSGA-II seed 44 on 68-d Bed B + 14-d morphology, 2 directions, 300-gen target
* **Model**: DSGC compartmental model (54-d Bed B electrophys via t0080 apply_parameter_vector +
  t0092-patched procedural morphology, canonical via C-0093-01)
* **Datasets**: none (simulator outputs)
* **Format**: json (single top-level object with `evaluations` list)
* **Instances**: 3,744 per-cell evaluations across 40 NSGA-II generations
* **Created by**: t0106_long_pdnd_nsga2_300gen

## Overview

This predictions asset captures every cell evaluated by the t0106 single-seed NSGA-II run on the
2-direction landscape: PD bar at 0 degrees and ND bar at 180 degrees, ratio DSI as the selectivity
objective. The run targeted 300 generations on GA seed 44, but the operator stopped after generation
40 once hourly HV polling showed the trace flat (less than 1% gain over 60 minutes).

The asset documents the **first joint-pass cells ever observed in the t0080 - t0104 - t0106 NSGA-II
lineage**: 123 unique cells with DSI >= 0.5 AND PD >= 30 Hz across 3,744 evaluations (3.3% yield).
Every prior task in the lineage returned exactly zero joint-pass cells. The reformulation from
16-direction vector-sum DSI to 2-direction ratio DSI is what produced the breakthrough; the longer
generation budget (40 vs 12) was secondary.

Each cell is recorded with its full 68-d parameter vector, the NSGA-II generation index, both
objectives (ratio DSI and preferred-direction firing rate), and the negated objective vector that
NSGA-II actually minimised. The DSI silence guard from S-0102-01 is active throughout: cells whose
total PD+ND spike count across the 3 trials falls below 10 are clamped to DSI = 0.0 before being
returned to NSGA-II selection.

## Model

The simulator is a compartmental DSGC neuron model on top of NEURON 8.2.7 / NetPyNE 1.1.1. The
electrophysiological substrate is the 54-d Bed B parameter vector from t0080 applied via
`apply_parameter_vector`; the morphology is the t0092-patched procedural generator
`generate_fixed_morphology` (canonical via correction C-0093-01) parameterised by 14 additional
dimensions covering soma offset, dendritic asymmetry, branch density, branch density gradient, and
related morphological knobs. The combined parameter space is 68-dimensional.

Each cell is evaluated by 2 NEURON simulations (PD bar at 0 degrees, ND bar at 180 degrees) x 3
noise replicates = 6 simulations per cell. The selectivity objective is the ratio DSI = (PD_rate -
ND_rate) / (PD_rate + ND_rate), which is mathematically identical to the vector-sum DSI for
antipodal sampling but well-defined for the 2-direction configuration. The DSI silence guard from
S-0102-01 forces DSI = 0.0 when the cell's total spike count across PD + ND falls below 10 per
trial.

Pymoo NSGA-II configuration: pop_size = 96, n_gen = 300 target, n_eval_seeds = 3, single GA seed =
44 (LHS-initialised initial population, explicit `np.random.SeedSequence(44)` seeding), SBX
crossover eta = 15 prob = 0.9, polynomial mutation eta = 20 prob = 1/68, duplicate elimination
enabled. The driver implements `PerGenerationPoolRestart(every=25)` — a new t0106 mitigation that
closes and re-creates the multiprocessing.Pool every 25 gens to reset NEURON-accumulated worker
memory. The restart fired off-by-one at gen 26 and dropped per-generation wall-clock from 110 min
back to 3 min.

## Data

No external dataset is consumed. Input vectors are 68-dimensional points sampled by NSGA-II starting
from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and explicitly
seeded with task_seed = 44. Bounds for the 68 parameters are inherited unchanged from the t0102 /
t0099 substrate (the same 54-d electrophys bounds from t0080 plus the 14-d morphology bounds from
t0090 patched via t0093). Noise replicates within each evaluation use the three deterministically
spawned RNG seeds drawn from `np.random.SeedSequence(42).spawn(5)` (the same seed family used by
t0102 and t0104).

The 2-direction restriction (PD = 0 deg, ND = 180 deg) is the central change relative to t0104's
16-direction sampling. ANGLES_DEG is reduced from a 16-element list every 22.5 deg to the
two-element antipodal pair, cutting per-cell NEURON cost from 64 simulations to 6 — roughly a 10x
speed-up per cell that funds the longer generation horizon.

## Prediction Format

The file `files/all_evaluations_seed44.json` is a single JSON object with one key, `evaluations`,
mapping to a list of 3,744 per-cell evaluation records. Each record has the following fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..40 = offspring generations).
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector.
* `objective_F_minimised`: list of 2 floats, the NSGA-II objective vector after sign-flipping for
  maximisation, i.e. `[-ratio_dsi, -pd_rate_hz]`. NSGA-II minimises this pair directly.
* `dsi_vector_sum`: float in [0, 1], the ratio DSI = (PD_rate - ND_rate) / (PD_rate + ND_rate)
  averaged across the 3 noise replicates. The field name `dsi_vector_sum` is preserved for schema
  compatibility with t0102 / t0104; under 2-direction antipodal sampling, the vector-sum DSI reduces
  exactly to the ratio DSI. Guard-cleaned per S-0102-01 at total-spike threshold 10 per trial, so
  values of 0.0 may either reflect a real ratio of zero or the silence guard floor.
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 3 replicates).

The strict 2-axis joint-pass flag `joint_pass = (dsi_vector_sum >= 0.5) AND (pd_rate_hz >= 30)` is
not stored per-record but is trivially recomputable from the above two fields. 123 of the 3,744
records satisfy this corner.

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

The joint-pass yield of **3.3%** exceeds the upper bound of published acceptance rates for NSGA-II
on comparable biophysical fits by roughly 8x (Druckmann2007 = 0.10%, Hay2011 = 0.40%, Achard2006 =
0.028%). Best ratio DSI = **1.0000** exceeds the published DSGC biological reference (Trenholm2013
mouse Hb9 control DSI = 0.76).

## Main Ideas

* The run produced the **first joint-pass cells in the t0080 - t0104 NSGA-II lineage** (123 unique,
  637 evaluations). Every prior task returned exactly 0 joint-pass cells. The reformulation from
  16-direction vector-sum DSI to 2-direction ratio DSI is what made the corner reachable —
  generation budget alone (40 vs 12) was secondary.
* Per-cell `vector_68d` is sufficient to re-evaluate any cell off-line at higher noise replicate
  count, with 16 directions, or with alternative selectivity definitions, without re-running
  NSGA-II. The 24 unique DSGC-like cells (DSI > 0.9 AND PD > 80 Hz) are the primary follow-up
  targets for the N_EVAL_SEEDS = 20 robustness check (S-0106-02) and the 16-direction re-evaluation
  (S-0106-03).
* The HV trace climbed from 0.2015 (gen 1) to 122.0288 (gen 40) — a 604x growth over 40
  generations — and was effectively flat (less than 1% per 60 min) by gen 36. The operator stop at
  gen 40 spent only $10.37 of the $25 cap. The empirical convergence point on the 2-direction
  substrate is therefore approximately gen 36; subsequent generations contribute only vector-space
  exploration.

## Summary

This asset records every NSGA-II evaluation from the t0106 single-seed long-horizon run on the 68-d
Bed B + 14-d morphology substrate, restricted to two antipodal directions (PD = 0 deg, ND = 180 deg)
with the ratio DSI as the selectivity objective. The run targeted 300 generations on GA seed 44,
completed 40 generations, and was operator-stopped at HV plateau for a total cost of $10.37 against
the $25 cap. The DSI silence guard from S-0102-01 was active throughout.

The headline finding is that **123 of 3,744 evaluated cells (3.3%) cleared the strict 2-axis
joint-pass corner** (DSI >= 0.5 AND PD >= 30 Hz) — the first joint-pass cells anywhere in the
t0080 - t0104 - t0106 NSGA-II lineage. Best ratio DSI was 1.0000 at PD = 81.43 Hz; best PD-rate
frontier was 122.62 Hz at DSI = 0.92. The full 68-d parameter vector for every cell is preserved,
enabling targeted follow-ups (robustness re-evaluation at N_EVAL_SEEDS = 20, 16-direction
re-evaluation, archetype-conditioned morphology sweeps) without re-running NSGA-II.

The asset is the primary evidence channel for the t0106 answer asset
`t0106-joint-pass-recovery-2dir`. It also serves as the substrate-confirmation predecessor for the
multi-seed confirmation (S-0106-01), robustness retest (S-0106-02), and algorithm comparison
follow-ups (S-0106-06 IBEA on the working 2-direction substrate).
