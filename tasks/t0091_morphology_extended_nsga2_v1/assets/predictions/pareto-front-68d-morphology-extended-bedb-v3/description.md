---
spec_version: "2"
predictions_id: "pareto-front-68d-morphology-extended-bedb-v3"
created_by_task: "t0091_morphology_extended_nsga2_v1"
date_created: "2026-05-08"
---

# pareto-front-68d-morphology-extended-bedb-v3

## Metadata

* **Predictions ID**: `pareto-front-68d-morphology-extended-bedb-v3`
* **Created by task**: `t0091_morphology_extended_nsga2_v1`
* **Date created**: 2026-05-08
* **Format**: JSONL (one line per Pareto cell)
* **Instance count**: 57 Pareto cells

## Overview

Per-cell predictions from the t0091 joint 68-d NSGA-II Pareto front. This
file documents 57 non-dominated cells from the 68-d joint (54-d
electrophys + 14-d morphology) multi-objective optimisation. The input
substrate is the t0092-patched procedural DSGC morphology generator
(`generate_fixed_morphology`, canonical per correction overlay
`C-0093-01`) applied per Pareto cell; the electrophys vector is the t0080
54-d v3 parameter space (channel densities, slow-AHP, synaptic, AIS
geometry, dendritic-spike machinery).

This is the first NSGA-II run in this project to call the procedural
morphology generator inside the per-cell evaluation loop. All prior
NSGA-II tasks (t0078, t0080, t0081, t0083, t0086) ran on a fixed Bed-B
substrate with 54-d electrophys parameters only; t0091 promotes the 14
morphology knobs from t0090 to first-class optimisation variables, producing
a 68-d joint search space.

## Model

DSGC compartmental neuron model with the t0092-patched procedural
morphology generator and the t0080 54-d electrophys parameter vector
applied via `apply_parameter_vector`. The morphology generator constructs a
DSGC cell with a programmable soma, primary/non-terminal/terminal
dendrites, and AIS subsegments per the 14 morphology knobs (number of
primary branches, branching probability, max Strahler depth, mean
branching angle, Rall exponent, soma offset along PD, field elongation,
branch density gradient, primary-branch concentration, mean segment
length, soma diameter, AIS length, deterministic morph seed, branch
length CV). Channel insertion uses the t0080 nrnmech library (12 t80
channel SUFFIXes plus skahpt80 slow-AHP); synapses are placed
parametrically with ACh + GABA + Exp2NMDA bundles per the t0080 v3
recipe.

## Data

No external dataset is consumed; the predictions are simulator outputs.
Input vectors are 68-d points sampled by the NSGA-II algorithm starting
from a 5-anchor warm-start population (Bed-B-like + symmetric +
PD-asymmetric + ND-asymmetric + alt-topology) each cloned with ~19 t0083
Pareto electrophys variants, plus 1 random LHS sample, total 96 cells.

## Prediction Format

JSONL with one line per Pareto cell. Each line is a JSON object with
fields:

* `cell_id`: int, unique within this file
* `dsi_vector_sum`: float, vector-sum direction selectivity index
* `pd_rate_hz`: float, preferred-direction mean firing rate (Hz)
* `robustness`: float in [0, 1], inverse CV of DSI across 5 seeds
* `morphology_vector_14d`: list[float], 14 morphology knobs
* `electrophys_vector_54d`: list[float], 54 electrophys / synaptic params
* `nearest_anchor`: str, nearest of the 5 anchors in normalised 14-d
  morphology space
* `verdict_biological`: str, plausible / stretched / exotic per the
  13-prior worst-case scorecard
* `v_opt_um_per_s`: float or null, cable-theoretic optimal bar velocity
* `effective_dendritic_length_um`: float or null, proxy total dendritic
  length

## Metrics

Per-cell metrics live in `pareto_cells.jsonl`. Aggregate metrics
(per-anchor mean DSI and robustness, all-Pareto mean DSI) live in
`results/metrics.json` under the `explicit_variants` schema.

## Main Ideas

* The 68-d Pareto front exposes the trade-off between direction
  selectivity (DSI), firing rate (PD-rate), and robustness across
  evaluation seeds.
* Anchor-tracking analysis classifies each Pareto cell to its nearest of
  5 morphology anchors; over- or under-representation of PD-asymmetric vs
  ND-asymmetric anchors tests whether morphology asymmetry is functional.
* Per-cell biological scoring (9 electrophys + 4 morphology priors)
  identifies which Pareto cells reach the published-prior plausibility
  region.

## Summary

This predictions asset records the 57-cell Pareto front of the
t0091 joint 68-d NSGA-II run with the t0092 patched morphology generator
inside the per-cell evaluation loop. Each cell is evaluated on 16
directions x 5 seeds; objectives are DSI vector-sum, PD firing rate, and
robustness (inverse CV of DSI). Per-cell metadata includes the nearest
anchor, biological plausibility verdict, and cable-theoretic v_opt for
downstream comparison with Hausselt 2007 / Trenholm 2013.

The Pareto front is intended as the input to downstream literature
comparison and follow-up tasks: each cell carries enough metadata
(electrophys vector, morphology vector, anchor, biological verdict,
cable v_opt, effective dendritic length) to support direction-selectivity
re-analysis, anchor-tracking statistical tests with bootstrap CIs, and
biological-plausibility scoring without re-running the simulator.
