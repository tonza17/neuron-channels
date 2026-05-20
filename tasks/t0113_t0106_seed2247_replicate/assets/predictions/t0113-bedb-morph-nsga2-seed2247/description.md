---
spec_version: "2"
predictions_id: "t0113-bedb-morph-nsga2-seed2247"
documented_by_task: "t0113_t0106_seed2247_replicate"
date_documented: "2026-05-20"
---
# NSGA-II seed 2247 Bed B + morphology 2-direction seed-2247 replicate of t0106/t0112

## Metadata

* **Name**: NSGA-II seed 2247 on 68-d Bed B + 14-d morphology, 2 directions, 60-gen replicate of
  t0106/t0112
* **Model**: DSGC compartmental model (54-d Bed B electrophys via t0080 apply_parameter_vector +
  t0092-patched procedural morphology, canonical via C-0093-01)
* **Datasets**: none (simulator outputs)
* **Format**: json (single top-level object with `evaluations` list, gzip-compressed)
* **Instances**: 1,344 per-cell evaluations across 14 NSGA-II generations
* **Created by**: t0113_t0106_seed2247_replicate

## Overview

This predictions asset captures every cell evaluated by the t0113 minimum-change replicate of t0112
(itself a minimum-change replicate of t0106): the same 68-d Bed B + 14-d morphology substrate, the
same 2-direction ratio DSI objective, the same NSGA-II hyperparameters (pop=96, SBX/PM,
N_EVAL_SEEDS=3, silence guard active), with exactly two changes from t0112: GA seed 77 -> 2247 and
the budget constants renamed from `T0112_*` to `T0113_*` (numeric values unchanged at $25 hard cap,
$20 per-instance watchdog). The seed value 2247 was drawn via `secrets.randbelow(10000)` immediately
before task creation to avoid the round-ish-low-number selection bias of seeds 44 (t0106) and 77
(t0112).

The run targeted 60 generations but the HV-plateau operator-stop fired at generation 14 — even
earlier than t0112's gen-21 stop and far short of t0106's gen-40 plateau. The hypervolume trajectory
shows a slow climb through gen 9 (HV 0.25 -> 6.59) followed by two discrete jumps at gen 10 (HV ->
35.98) and gen 14 (HV -> 45.62) when the first silence-guard cells entered the front; the
inter-generation HV deltas between gen 10 and gen 13 are all under 0.13, which is what triggered the
plateau detector.

The headline finding is **non-replication of the legitimate joint-pass corner**: seed 2247 produces
**zero non-silence-guard joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz). The only two cells that
satisfy the joint-pass thresholds (gen 10 PD=35.00 Hz and gen 14 PD=45.24 Hz) sit at exactly DSI =
1.0, the silence-guard or single-spike artefact value seen in t0106 / t0112 as the spurious-extreme
tail of the substrate. The best legitimate (non-DSI=1.0) cell achieves DSI = 0.3651 at PD = 10.24
Hz; the best PD-rate cell achieves 71.67 Hz at DSI = 0.0017. The substrate is reachable from seed
2247 in the sense that the run completes and produces evaluations, but the joint-pass cohort that
defined t0106's "120-cell breakthrough" and t0112's "7-cell partial replication" is absent. This
hardens the **seed-specific-density** reading established by t0112.

## Model

The simulator is the same compartmental DSGC neuron model used in t0106 / t0112, running on NEURON
8.2.7 / NetPyNE 1.1.1. The electrophysiological substrate is the 54-d Bed B parameter vector from
t0080 applied via `apply_parameter_vector`; the morphology is the t0092-patched procedural generator
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
2247 (LHS-initialised initial population, explicit `np.random.SeedSequence(2247)` seeding), SBX
crossover eta = 15 prob = 0.9, polynomial mutation eta = 20 prob = 1/68, duplicate elimination
enabled. The driver implements `PerGenerationPoolRestart(every=10)` — the same cadence as t0112,
tighter than t0106's every-25. With only 14 gens completed, exactly one pool restart fired (after
gen 10). Per-generation wall-clock ranged 63-252 s/gen for 1,344 cells in 2,236 s (37.3 min), or
~1.66 s/cell on 60 parallel workers — comfortably within the t0112 per-gen wall-clock baseline.

## Data

No external dataset is consumed. Input vectors are 68-dimensional points sampled by NSGA-II starting
from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and explicitly
seeded with task_seed = 2247 (the only deliberate divergence from t0112's seed 77; the seed itself
was drawn via `secrets.randbelow(10000)` immediately before task creation). Bounds for the 68
parameters are inherited unchanged from t0106 / t0112 (which inherited from the t0102 / t0099
substrate, the same 54-d electrophys bounds from t0080 plus the 14-d morphology bounds from t0090
patched via t0093). Noise replicates within each evaluation use the same three deterministically
spawned RNG seeds drawn from `np.random.SeedSequence(42).spawn(3)` that t0106 and t0112 used.

The 2-direction restriction (PD = 0 deg, ND = 180 deg) is preserved verbatim from t0106 / t0112 —
this was the t0106 breakthrough and the t0113 task brief explicitly forbids changing it.

## Prediction Format

The file `files/all_evaluations_seed2247.json.gz` is a gzip-compressed single JSON object with one
key, `evaluations`, mapping to a list of 1,344 per-cell evaluation records. Each record has the
following fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..14 = offspring generations).
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector.
* `objective_F_minimised`: list of 2 floats, the NSGA-II objective vector after sign-flipping for
  maximisation, i.e. `[-ratio_dsi, -pd_rate_hz]`. NSGA-II minimises this pair directly.
* `dsi_vector_sum`: float in [0, 1], the ratio DSI = (PD_rate - ND_rate) / (PD_rate + ND_rate)
  averaged across the 3 noise replicates. The field name `dsi_vector_sum` is preserved for schema
  compatibility with t0102 / t0104 / t0106 / t0112; under 2-direction antipodal sampling, the
  vector-sum DSI reduces exactly to the ratio DSI. Guard-cleaned per S-0102-01 at total-spike
  threshold 10 per trial, so values of 0.0 may either reflect a real ratio of zero or the silence
  guard floor, and values of 1.0 typically indicate that all spikes occurred in PD (often a
  single-spike artefact at the silence-guard boundary).
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 3 replicates).

The strict 2-axis joint-pass flag `joint_pass = (dsi_vector_sum >= 0.5) AND (pd_rate_hz >= 30)` is
not stored per-record but is trivially recomputable from the above two fields. 6 of the 1,344
records satisfy this corner, but **all 6 sit at exactly DSI = 1.0** and correspond to only **2
unique parameter vectors** (gen 10 PD=35.00 Hz and gen 14 PD=45.24 Hz, each re-evaluated 3 times
across the same vector via NSGA-II carry-over). There are **zero legitimate (non-DSI=1.0) joint-pass
cells**.

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **1,344** |
| Generations completed | **14** of 60 ceiling (HV plateau stop) |
| Best ratio DSI (overall) | **1.0000** (silence-guard / single-spike artefact) |
| Best legit ratio DSI (non-DSI=1.0) | **0.3651** at PD = 10.24 Hz |
| Best PD-rate frontier (Hz) | **71.67** at DSI = 0.0017 |
| Unique joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz) | **2** (both at DSI=1.0; silence-guard) |
| Joint-pass evaluations (with NSGA-II repetition) | **6** |
| Legit joint-pass yield (non-DSI=1.0) | **0** of 1,344 cells |
| Final hypervolume (2-D) | **45.6221** (start 0.2460; 185x growth) |
| Final NSGA-II compute cost (USD) | **$0.1467** of $25 cap |
| Wall-clock runtime | **37.3 min** for 14 gens (~160 s/gen avg) |
| HV plateau generation | **14** (operator-stop fired; watchdog NOT tripped) |

The legit joint-pass yield of **0** (0 / 1,344) is consistent with seed 77's sparse joint-pass
cohort (7 / 2,016 = 0.35%) being a stochastic outcome rather than a substrate-level rate, and
strongly contradicts seed 44's 123 / 3,744 = 3.3% yield. The three-seed sample (44 / 77 / 2247: 123
/ 7 / 0 unique legit joint-pass cells) shows a 17x-then-infinity dispersion across just-three-points
— the substrate's joint-pass acceptance rate cannot be reported as a population parameter from this
sample.

## Main Ideas

* **The substrate-level joint-pass acceptance rate is not estimable from a 3-seed sample.** Seeds
  44, 77, and 2247 produced 123 / 7 / 0 unique legitimate joint-pass cells — a dispersion that spans
  two orders of magnitude and includes a true zero. The S-0112-01 batch needs at least 2 more seeds
  before any substrate-level mean can be reported.
* **The HV-plateau detector fires earlier on seeds that fail to reach the joint-pass corner.** t0106
  (seed 44) plateaued at gen 40 after reaching DSI = 0.9606 at PD > 100 Hz; t0112 (seed 77)
  plateaued at gen 21 after reaching DSI = 0.9535 at PD = 60 Hz; t0113 (seed 2247) plateaued at gen
  14 without reaching the joint-pass corner at all. The plateau detector is sensitive to whether the
  Pareto front improvements are large or small in absolute HV terms, and a front that never enters
  the joint-pass region has nothing to drive late-stage HV gains.
* **The silence-guard DSI=1.0 region remains a recurring contaminant.** Seeds 44 and 77 both
  reported handfuls of DSI = 1.0 cells; seed 2247 is unique only in that **all** of its
  joint-pass-region cells are DSI=1.0 silence-guard artefacts rather than legitimate selective
  cells. This validates the t0106 reporting convention of always splitting `best_dsi_ratio` from
  `best_legit_dsi` and reporting `dsi_eq_one_count` as an operational diagnostic.
* **The cadence-10 pool-restart protocol remains operationally safe at low cost.** t0113 spent $0.15
  in 37 min for 14 gens — extrapolated, ~$0.66 / 60 gens. The protocol's compute envelope is now
  well-characterised across three seeds and three different termination patterns.
* The asset preserves the full 68-d parameter vector for every cell, enabling cross-seed
  parameter-space distance analysis between t0106, t0112 and t0113 Pareto cells in the t0113 results
  step (`pareto_front_overlap_3seeds.csv`).

## Summary

This asset records every NSGA-II evaluation from the t0113 minimum-change replicate of t0112: same
substrate, same objectives, same hyperparameters, only the GA seed (2247, drawn via
`secrets.randbelow(10000)` immediately before task creation) and the budget constant names changed.
The run completed 14 generations on GA seed 2247 before the HV-plateau operator-stop fired,
evaluated 1,344 cells, and spent $0.1467 of the $25 cap. No watchdog termination, no cost overrun,
no operator intervention.

The headline finding is **non-replication of the legitimate joint-pass corner**. Seed 2247 produces
zero non-silence-guard joint-pass cells; the only two cells with PD >= 30 Hz in the DSI >= 0.5 band
sit at exactly DSI = 1.0, the silence-guard / single-spike artefact value. The best legitimate cell
reaches DSI = 0.3651 at PD = 10.24 Hz, and the best PD-rate cell reaches 71.67 Hz at DSI = 0.0017 —
both far from the joint-pass corner. The three-seed sample (44: 123; 77: 7; 2247: 0) therefore spans
a 100x+ dispersion of unique legit joint-pass cells, hardening the conclusion that t0106's reported
3.3% acceptance rate is not a substrate-level property.

The asset is the primary evidence channel for the t0113 results step, supports the cross-seed
Pareto-front overlap analysis in t0113's compare-literature step, and provides the third seed point
in the S-0112-01 substrate-rate confirmation batch. Two additional seeds (a fourth and fifth point)
are still required before any substrate-level rate can be reported with even minimal sampling
confidence.
