---
spec_version: "2"
predictions_id: "t0112-bedb-morph-nsga2-seed77"
documented_by_task: "t0112_t0106_seed77_replicate"
date_documented: "2026-05-19"
---
# NSGA-II seed 77 Bed B + morphology 2-direction seed-77 replicate of t0106

## Metadata

* **Name**: NSGA-II seed 77 on 68-d Bed B + 14-d morphology, 2 directions, seed-77 replicate of
  t0106
* **Model**: DSGC compartmental model (54-d Bed B electrophys via t0080 apply_parameter_vector +
  t0092-patched procedural morphology, canonical via C-0093-01)
* **Datasets**: none (simulator outputs)
* **Format**: json (single top-level object with `evaluations` list, gzip-compressed)
* **Instances**: 2,016 per-cell evaluations across 21 NSGA-II generations
* **Created by**: t0112_t0106_seed77_replicate

## Overview

This predictions asset captures every cell evaluated by the t0112 minimum-change replicate of t0106:
the same 68-d Bed B + 14-d morphology substrate, the same 2-direction ratio DSI objective, the same
NSGA-II hyperparameters (pop=96, SBX/PM, N_EVAL_SEEDS=3, silence guard active), with exactly two
constants changed from t0106: GA seed 44 -> 77 and pool-restart cadence 25 gens -> 10 gens.

The run targeted 60 generations (extendable from t0106's stopped-at-40 ceiling) but the HV-plateau
operator-stop criterion fired at generation 21 — much earlier than t0106's gen-38 plateau. The
hypervolume trajectory shows a steep climb between gen 14 and gen 17 (HV 33.2 -> 107.3, the
breakthrough-cell signature) and then near-flat behaviour through gen 21 (HV 107.4).

The headline finding is **partial replication**: seed 77 reaches the joint-pass corner (DSI >= 0.5
AND PD >= 30 Hz) with best DSI = 0.9535 at PD = 60 Hz and best PD-rate = 114.76 Hz, but produces
only **7 unique joint-pass cells (25 evaluations)** versus t0106 seed 44's 123 unique (637
evaluations). Both seeds reach the same frontier corner but with very different cell densities — the
substrate's joint-pass region is reachable from multiple GA seeds, but the density of reachable
cells is itself a stochastic property of the GA seed.

## Model

The simulator is the same compartmental DSGC neuron model used in t0106, running on NEURON 8.2.7 /
NetPyNE 1.1.1. The electrophysiological substrate is the 54-d Bed B parameter vector from t0080
applied via `apply_parameter_vector`; the morphology is the t0092-patched procedural generator
`generate_fixed_morphology` (canonical via correction C-0093-01) parameterised by 14 additional
dimensions covering soma offset, dendritic asymmetry, branch density, branch density gradient, and
related morphological knobs. The combined parameter space is 68-dimensional.

Each cell is evaluated by 2 NEURON simulations (PD bar at 0 degrees, ND bar at 180 degrees) x 3
noise replicates = 6 simulations per cell. The selectivity objective is the ratio DSI = (PD_rate -
ND_rate) / (PD_rate + ND_rate); for antipodal sampling this is mathematically identical to the
vector-sum DSI. The DSI silence guard from S-0102-01 is active throughout: cells whose total PD+ND
spike count across the 3 trials falls below 10 are clamped to DSI = 0.0 before being returned to
NSGA-II selection.

Pymoo NSGA-II configuration: pop_size = 96, n_gen = 60 ceiling, n_eval_seeds = 3, single GA seed =
77 (LHS-initialised initial population, explicit `np.random.SeedSequence(77)` seeding), SBX
crossover eta = 15 prob = 0.9, polynomial mutation eta = 20 prob = 1/68, duplicate elimination
enabled. The driver implements `PerGenerationPoolRestart(every=10)` — a tighter cadence than t0106's
every-25 to reduce NEURON-accumulated worker memory between restarts. The tighter cadence held
per-generation wall-clock at 200-1,100 s/gen even through the late generations.

## Data

No external dataset is consumed. Input vectors are 68-dimensional points sampled by NSGA-II starting
from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and explicitly
seeded with task_seed = 77 (the only deliberate divergence from t0106's seed 44). Bounds for the 68
parameters are inherited unchanged from t0106 (which inherited from the t0102 / t0099 substrate, the
same 54-d electrophys bounds from t0080 plus the 14-d morphology bounds from t0090 patched via
t0093). Noise replicates within each evaluation use the same three deterministically spawned RNG
seeds drawn from `np.random.SeedSequence(42).spawn(5)` that t0106 used.

The 2-direction restriction (PD = 0 deg, ND = 180 deg) is preserved verbatim from t0106 — this was
the t0106 breakthrough and the t0112 task brief explicitly forbids changing it.

## Prediction Format

The file `files/all_evaluations_seed77.json.gz` is a gzip-compressed single JSON object with one
key, `evaluations`, mapping to a list of 2,016 per-cell evaluation records. Each record has the
following fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..21 = offspring generations).
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector.
* `objective_F_minimised`: list of 2 floats, the NSGA-II objective vector after sign-flipping for
  maximisation, i.e. `[-ratio_dsi, -pd_rate_hz]`. NSGA-II minimises this pair directly.
* `dsi_vector_sum`: float in [0, 1], the ratio DSI = (PD_rate - ND_rate) / (PD_rate + ND_rate)
  averaged across the 3 noise replicates. The field name `dsi_vector_sum` is preserved for schema
  compatibility with t0102 / t0104 / t0106; under 2-direction antipodal sampling, the vector-sum DSI
  reduces exactly to the ratio DSI. Guard-cleaned per S-0102-01 at total-spike threshold 10 per
  trial, so values of 0.0 may either reflect a real ratio of zero or the silence guard floor.
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 3 replicates).

The strict 2-axis joint-pass flag `joint_pass = (dsi_vector_sum >= 0.5) AND (pd_rate_hz >= 30)` is
not stored per-record but is trivially recomputable from the above two fields. 25 of the 2,016
records satisfy this corner (7 unique parameter vectors).

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
**3.3%** (123 / 3,744) on the same substrate. Both seeds discover the same frontier corner (best DSI
~ 0.95, best PD > 100 Hz) but seed 77 packs the corner much more sparsely.

## Main Ideas

* The **substrate is reachable from at least two GA seeds** (44 and 77). The 2-direction ratio DSI
  reformulation is the load-bearing change, not the seed-44 luck — seed 77 also crosses the
  joint-pass corner.
* The **joint-pass density is stochastic across seeds**. 7 unique vs 123 unique on the same
  substrate with the same hyperparameters argues that the published joint-pass acceptance rate from
  t0106 is a single-seed point estimate that cannot be reported as a substrate-level rate without
  more replicates.
* The **tighter pool-restart cadence (every 10 gens) was operationally safe**. Per-generation
  wall-clock peaked at ~1,100 s/gen and dropped after each restart; total run time was 4 h 40 m for
  21 gens vs t0106's 24.1 h for 40 gens (~1.5x faster per gen).
* The **HV-plateau detector fired at gen 21** — much earlier than t0106's gen-38 plateau. The
  earlier stop is consistent with seed 77 producing a smaller, more concentrated joint-pass cohort
  that exhausts its local Pareto-improvement opportunities sooner.
* The asset preserves the full 68-d parameter vector for every cell, enabling cross-seed
  parameter-space distance analysis between t0106 and t0112 Pareto cells in the t0112 results step.

## Summary

This asset records every NSGA-II evaluation from the t0112 minimum-change replicate of t0106: same
substrate, same objectives, same hyperparameters, only the GA seed (77) and the pool-restart cadence
(every 10 gens) changed. The run completed 21 generations on GA seed 77 before HV-plateau stopped
it, evaluated 2,016 cells, and spent $1.96 of the $25 cap.

The headline finding is **partial replication**: seed 77 reaches the same frontier corner as seed 44
(best DSI 0.9535 vs 0.9606; best PD 114.76 Hz vs 122.62 Hz) but produces 17x fewer unique joint-pass
cells (7 vs 123). The substrate is therefore reachable from multiple GA seeds, but the density of
reachable joint-pass cells is itself a stochastic property of the GA seed — the t0106 3.3%
acceptance rate is a single-seed point estimate that must not be reported as a substrate-level
property without additional replicates.

The asset is the primary evidence channel for the t0112 results step, supports the cross-seed
Pareto-front overlap analysis in t0112's compare-literature step, and provides the substrate for any
downstream multi-seed confirmation tasks.
