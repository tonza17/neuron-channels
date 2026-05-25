---
spec_version: "2"
predictions_id: "nsga2-dsi-atp-per-spike-bedb-morph"
documented_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"
date_documented: "2026-05-25"
---

# NSGA-II DSI vs ATP-per-Spike on Bed B + 14-d Morphology

## Metadata

* **Task**: `t0124_bedb_dsi_atp_per_spike_nsga2`
* **GA seed**: 6650
* **Pop size**: 96
* **N_EVAL_SEEDS**: 3; **N_DIRECTIONS**: 2 (antipodal pair 0/180 deg)
* **Generations completed**: 9 / 60
* **Pool-restart cadence**: every 10 generations
* **HV-plateau auto-stop**: disabled (per project policy)
* **Cost cap**: $6.00
* **Final cost**: $0.0728
* **Stop trigger**: operator_stop

## Overview

This predictions asset captures every cell evaluated by the t0124 single-seed NSGA-II run on the 68-d Bed B + 14-d morphology substrate. The two minimised objectives are F[0] = -dsi_vector_sum (DSI maximised, with silence-guard sentinel = -1 for cells with R_PD < 3 PD spikes) and F[1] = +atp_per_spike_molecules (Sengupta 2010 recipe; lower is better). The Pareto front captures the DSI / ATP trade-off across the 68-d parameter space.

## Model

68-d Bed B compartmental DSGC model (54-d electrophysiological + 14-d morphology). NEURON-backed simulation via the t0080 channel MOD pack and t0024 vendored DSGC NEURON template. NSGA-II driven by pymoo with default SBX crossover (eta=15) and polynomial mutation (eta=20).

## Data

Synthetic procedurally-generated DSGC morphologies (no external dataset; the 14-d morphology vector is sampled from tasks/t0090's PARAM_BOUNDS). Per cell the protocol runs 3 evaluation seeds x 2 directions (0 deg PD and 180 deg ND) = 6 trials. Each trial is a 1.4 s simulation with full HH mechanics and the Sengupta 2010 ATP-per-spike recipe (per-segment Na+ current integrated over each AP window).

## Prediction Format

JSONL gzip-compressed (`files/predictions.jsonl.gz`). One JSON object per evaluated cell. Schema (see `details.json` `prediction_schema` for full list): `generation`, `vector_68d` (54-d electrophys + 14-d morph), `dsi_vector_sum`, `atp_per_spike_molecules`, `objective_F_minimised`, `is_pareto`, `silence_failed_bool`, `legit_bool`, plus per-direction firing rates and diagnostic cytoplasm volume / MI / per-compartment ATP breakdown.

## Metrics

* **Best legit DSI**: 0.8824
* **Min ATP per spike**: 2.112e+06 molecules
* **Joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz AND ATP <= median)**: 0
* **Final hypervolume**: 1.7637e+10
* **n_cells_total**: 864
* **n_cells_pareto**: 5

## Main Ideas

* The Pareto front captures the DSI / ATP trade-off in the 68-d Bed B + 14-d morphology substrate; downstream tasks can mine this asset for joint-pass cells satisfying both function and energy criteria.
* Cells with DSI = -1 (silence guard tripped) are kept in the asset for completeness but flagged via `legit_bool = false` and `silence_failed_bool = true`.
* The Sengupta 2010 ATP recipe is verified against the Carter & Bean 2009 first-principles canonical band [1e8, 1e9] ATP/AP/cm via the pre-launch smoke-gate (check 9); on the canonical anchor cell the recipe sits inside the PASS band.

## Summary

This asset is the primary output of t0124. Downstream tasks (e.g., literature comparison, joint Pareto analysis with t0122's cytoplasm front, follow-up multi-seed replication) consume the per-cell records via the predictions aggregator. The asset's `metrics_at_creation` field summarises the headline numbers; the canonical `description.md` (this file) provides the methodological context, and the `details.json` field manifest enumerates every per-cell schema field.

## Reproducing the asset

1. Provision a Vast.ai EPYC instance.
2. `nrnivmodl` on `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`.
3. `python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.random_init`.
4. `python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.smoke_gate`.
5. `python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.nsga2_driver --seed 6650 --pop 96 --n-gen 60 --n-eval-seeds 3 --n-directions 2`.
6. `python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.build_t0124_outputs --seed 6650`.
