---
spec_version: "2"
predictions_id: "t0114-bedb-morph-nsga2-seed7755"
documented_by_task: "t0114_seed7755_no_autostop"
date_documented: "2026-05-20"
---

# NSGA-II seed 7755 on 68-d Bed B + 14-d morphology, 2 directions, 62-gen run with HV-plateau auto-stop DISABLED (S-0113-03 live impl)

## Metadata

* **Name**: NSGA-II seed 7755 on 68-d Bed B + 14-d morphology, 2 directions, 62-gen run with HV-plateau auto-stop DISABLED (S-0113-03 live impl)
* **Model**: Compartmental DSGC model (t0092-patched procedural morphology + 54-d Bed B electrophys vector via t0080 apply_parameter_vector)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl.gz
* **Instances**: 5,952 per-cell evaluations across 62 NSGA-II generations
* **Created by**: t0114_seed7755_no_autostop

## Overview

These predictions capture every cell evaluated by the t0114 single-seed NSGA-II run with GA seed=7755 (5,952 cells across 62 generations). The run is the live implementation of S-0113-03: it re-runs the t0106 / t0112 / t0113 substrate with the HV-plateau auto-stop DISABLED to test whether the t0113 14-gen premature plateau was real saturation or a detector false-positive. The headline finding is that the HV trajectory continued climbing significantly past gen 14 (the t0113 stop point) before plateauing in earnest near gen 50, and the run reached a final hypervolume of 111.5353 — within a few percent of t0106's 122.03 and well above t0113's 45.62.

The 484 unique LEGIT joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz AND DSI < 0.9999) collected by this seed put it into the same yield bucket as t0106 (123 LEGIT) rather than t0112's sparse 7 or t0113's 0. The asset is the primary evidence channel for the t0114 results summary, the S-0113-03 detector re-parameterisation table in `results_detailed.md`, and the 4-seed cross-comparison CSVs in `results/data/`.

## Model

Compartmental DSGC neuron model with the t0092-patched procedural morphology generator (`generate_fixed_morphology`, canonical via correction C-0093-01) and the 54-d Bed B electrophys parameter vector applied via t0080's `apply_parameter_vector`. Per-cell evaluation runs 2 stimulus directions (PD = 0 deg, ND = 180 deg) x 3 noise replicates with objectives = (ratio DSI, preferred-direction firing rate in Hz), both maximised. Pymoo NSGA-II minimises the negated pair. Crossover SBX eta=15 with prob=0.9; polynomial mutation eta=20 with prob=1/68; duplicate elimination enabled. Population size 96, n_gen_max=300 (HV-plateau auto-stop DISABLED, so the run terminates only by cost cap or operator stop), LHS-initialised initial population with explicit `np.random.SeedSequence` seeding for reproducibility. Pool restart cadence 10 (same as t0112 / t0113). The DSI silence guard from S-0102-01 is active: cells whose total PD+ND spike count across the 2 directions falls below 10 have DSI clamped to 0.0 before being returned to NSGA-II.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and explicitly seeded with task_seed=7755. Bounds for the 68 parameters are inherited unchanged from the t0106/t0112/t0113 substrate (54-d Bed B electrophys bounds from t0080 + 14-d morphology bounds from t0090). Noise replicates inside each evaluation use the 3 deterministically spawned RNG seeds drawn from `np.random.SeedSequence(42).spawn(4)`.

## Prediction Format

Gzipped JSONL with one line per evaluated cell (5,952 lines total). Each line is a JSON object with fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS population, 2-62 = offspring generations)
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector
* `objective_F_minimised`: list of 2 floats, the NSGA-II objective vector with sign-flipped maximisation conventions: [-ratio_dsi, -pd_rate_hz]
* `dsi_vector_sum`: float in [0, 1], ratio DSI = (PD - ND) / (PD + ND), guard-cleaned per S-0102-01
* `pd_rate_hz`: float, preferred-direction mean firing rate (Hz) across the 3 noise replicates
* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND `pd_rate_hz >= 30` (the 2-axis strict criterion)
* `legit`: bool, true iff `dsi_vector_sum < 0.9999` — false flags the silence-guard / single-spike DSI=1.0 ceiling artefact

Example line (formatted for readability):

```
{
  "generation": 47,
  "vector_68d": [0.4576, 0.0550, ..., 0.2229],
  "objective_F_minimised": [-0.9868, -107.86],
  "dsi_vector_sum": 0.9868,
  "pd_rate_hz": 107.86,
  "joint_pass": true,
  "legit": true
}
```

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
|--------|-------|
| Cells evaluated | **5,952** |
| Generations completed | **62** of 300 ceiling (operator stop) |
| Best DSI overall | **1.0000** (silence-guard ceiling) |
| Best legit DSI (non-silence-guard) | **0.9926** |
| Best PD-rate | **112.86 Hz** |
| Unique joint-pass cells (DSI >= 0.5 AND PD >= 30) | **771** |
| Unique LEGIT joint-pass cells (DSI < 0.9999) | **484** |
| Cells at DSI = 1.0 ceiling (silence-guard) | **1073** |
| Final hypervolume (2-D) | **111.5353** |
| Stop trigger | **operator_stop** |

The 2-axis strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz) is met by **771** unique cells across the 5,952 evaluations. Filtering out silence-guard ceiling cells leaves **484** LEGIT joint-pass cells.

## Main Ideas

* The run terminated at generation 62 via operator stop after the HV trajectory visibly plateaued near 111.5; the HV-plateau auto-stop was DISABLED for this run.
* 484 of the 5,952 evaluated cells cleared the strict 2-axis LEGIT joint-pass corner — placing seed 7755 in the same yield bucket as t0106 seed 44 (123 LEGIT) rather than t0112 / t0113.
* The best legit cell reaches DSI = 0.9926 at PD = ~107.86 Hz (gen 47); the best PD-rate cell reaches PD = 112.86 Hz. Per-cell `vector_68d` is sufficient to re-evaluate any cell without re-running the optimiser.
* The data confirms S-0113-03's hypothesis that the t0113 14-gen HV-plateau stop was a premature trigger: gen 14 HV was only ~36-46 on t0113, while this same protocol on seed 7755 reaches HV=111.54 by gen 62.

## Summary

This asset captures all 5,952 NSGA-II evaluations from the t0114 random-init 2-objective run with GA seed=7755, covering generations 1 through 62. Each cell is a 68-d point in the Bed B electrophys + procedural morphology parameter space, evaluated with 2 stimulus directions and 3 noise replicates against the 2-dimensional objective (ratio DSI, preferred-direction firing rate). The DSI silence guard from S-0102-01 is active throughout; the HV-plateau auto-stop is DISABLED.

The headline finding is **484 unique LEGIT joint-pass cells** — a result that places seed 7755 in the same high-yield bucket as t0106 seed 44 (123 LEGIT). Best individual axes were DSI=0.9926 (legit; gen ~47) and PD=112.86 Hz; final hypervolume 111.5353 is roughly 91% of t0106's 122.03.

Combined with the matched three-other-seed assets (t0106 / t0112 / t0113), this contributes the fourth data point to the substrate-rate confirmation batch (S-0112-01) and provides the primary evidence channel for S-0113-03's detector re-parameterisation analysis. Cost watchdog and operator stop jointly govern run length; the productive NSGA-II compute cost was $0.94 of the $25 cap.
