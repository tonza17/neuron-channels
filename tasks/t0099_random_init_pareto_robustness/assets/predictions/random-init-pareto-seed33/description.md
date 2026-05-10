---
spec_version: "2"
predictions_id: "random-init-pareto-seed33"
documented_by_task: "t0099_random_init_pareto_robustness"
date_documented: "2026-05-10"
---

# Random-init Pareto front seed 33

## Metadata

* **Name**: Random-init Pareto front seed 33
* **Model**: DSGC compartmental model (t0092-patched procedural morphology
  generator + 54-d electrophys vector applied via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 14 Pareto cells
* **Created by**: t0099_random_init_pareto_robustness

## Overview

This predictions asset records the 14-cell Pareto front of one of three
random-init NSGA-II reproducibility runs in t0099 (task seed 33, RNG seeds
chosen from {11, 22, 33}). The run mirrors t0091's joint 68-d NSGA-II
configuration (population 96, up to 8 generations, SBX eta=15, polynomial
mutation eta=20 with prob=1/68, eliminate_duplicates=True, 16 directions x 5
evaluation seeds per cell, HV-plateau + cost-watchdog termination) but
replaces t0091's 5-anchor warm-start population with a fresh Latin Hypercube
Sample over the 68-d parameter bounds. The cost cap was $1.00 per seed instead
of t0091's $4.00, reflecting the reduced scope of a reproducibility check.

The intended use of this asset is direct comparison against t0091's
`pareto-front-68d-morphology-extended-bedb-v3` predictions: identical
evaluator, identical priors, identical objective space — only the initial
population and the RNG seeds differ.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology
generator (`generate_fixed_morphology`, canonical via `C-0093-01`) and the
t0080 54-d electrophys parameter vector applied via `apply_parameter_vector`.
Per-cell evaluation runs 16 stimulus directions x 5 evaluation seeds with
objectives = (DSI vector-sum, PD firing rate, robustness as inverse CV of DSI
across seeds), all maximised. Pymoo NSGA-II minimises the negated objectives.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by
NSGA-II starting from a 96-row LHS sample drawn with `pymoo
LatinHypercubeSampling` and explicitly seeded via `np.random.SeedSequence(33)`.

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
* `nearest_anchor_name`: str (bedb_like / symmetric / pd_asymmetric /
  nd_asymmetric / alt_topology)
* `nearest_anchor_distance_normalised`: float, Euclidean distance to nearest
  anchor in normalised morphology space
* `verdict_biological`: str (plausible / stretched / exotic / no_data),
  worst-case 13-prior aggregation

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

* This is one of three independent random-init replicates of t0091's joint
  68-d NSGA-II run, used to test reproducibility under RNG variation and the
  load-bearing role of the 5-anchor warm-start.
* The Pareto front records every non-dominated cell from the NSGA-II run; the
  per-cell vector_68d is sufficient to re-evaluate or re-score any cell
  without re-running the optimiser.
* Anchor classification here is post-hoc — the run itself never used anchors
  to seed the population, so the nearest-anchor labels reflect the geometry
  found by random search + NSGA-II selection rather than warm-start bias.

## Summary

This asset captures the Pareto front of a random-init NSGA-II run with task
seed 33 (14 cells). It is one of three replicates whose
cross-comparison drives the headline answer asset
``random_init_reproducibility_and_warmstart_dependence``. Each line of the
JSONL file carries the 68-d parameter vector, the three NSGA-II objectives,
the post-hoc anchor classification, and the 13-prior biological verdict — all
required inputs for the cross-seed and warm-start-dependence analyses.

The intended downstream uses are direct comparison with t0091's Pareto
front (anchor distribution, plausibility verdicts, strict joint-pass count)
and possible re-scoring under future biological priors without re-running the
NSGA-II loop.
