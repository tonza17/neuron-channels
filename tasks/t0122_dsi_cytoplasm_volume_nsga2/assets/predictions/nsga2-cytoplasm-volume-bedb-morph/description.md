---
spec_version: "2"
predictions_id: "nsga2-cytoplasm-volume-bedb-morph"
documented_by_task: "t0122_dsi_cytoplasm_volume_nsga2"
date_documented: "2026-05-24"
---
# NSGA-II Predictions: DSI vs Cytoplasm Volume on Bed B + 14-d Morph

## Metadata

* **Name**: NSGA-II Pareto front: DSI vs cytoplasm volume on Bed B + 14-d morph
* **Model**: Procedural Bed B DSGC cell (t0090 generator + t0092 z-axis soma patch, t0080 NEURON MOD
  channels)
* **Datasets**: (none; in-silico evaluation only)
* **Format**: jsonl.gz
* **Instances**: 5760
* **Created by**: t0122_dsi_cytoplasm_volume_nsga2
* **GA seed**: 1524
* **Generations completed**: 60 / 60
* **Final cost (USD)**: $0.2060 / $6.00 cap

## Overview

This predictions asset captures every per-cell evaluation from the t0122 single-seed 68-d NSGA-II
run on the Bed B + 14-d morphology substrate. The 2-objective optimisation maximises DSI and
simultaneously minimises cytoplasm volume (Cuntz 2010 wiring-cost interpretation of the Cajal
cytoplasm-conservation principle). The asset preserves the full per-cell vector and all derived
diagnostics so downstream tasks can recompute Pareto fronts, joint-pass cell counts, and
balancing-factor distributions without re-running the NSGA-II loop.

The run forks the t0115 NSGA-II substrate end-to-end (pop=96, N_EVAL_SEEDS=3,
_POOL_RESTART_EVERY=10, HV_PLATEAU_AUTO_STOP=False); the only behavioural deltas are the second
F-axis (cytoplasm volume in place of PD-rate), the tightened silence guard (`pd_spikes_sum < 3` in
place of `total_mean_spikes < 10`), and the reduced `N_GEN_MAX = 60` / `COST_CAP_USD = 6.0`
constraints from the task description. The Cuntz balancing factor is reported on the top-10 LEGIT
cells in the companion answer asset.

## Model

The cell is a procedural DSGC built by `generate_fixed_morphology` (t0092 fix wrapper around t0090's
generator) and parameterised by the 14-d morphology vector concatenated with the 54-d electrophys
vector. The electrophys block uses the t0080 BedB v3 13-channel MOD library: Nav1.6 + napt80 +
nart80 sodium channels, KDR, Kv3, Kv4, Kv7 potassium channels, BKT80 calcium-activated potassium,
IhT80 hyperpolarisation-activated, T-type and L-type calcium channels, SKAHPT80 calcium-activated
potassium, and SKT80. Synaptic inputs are AR(2)-correlated ACh / GABA bundles placed by the
parametric placer (t0024 de Rosenroll 2026 ports), with NMDA conductance on dendrites. The AIS is
split into proximal / distal segments at the t0080-default ratio. All parameters (channel densities,
synapse weights, NMDA conductance, AIS lengths, morphology branching parameters) are part of the
68-d optimisation vector and vary per cell.

## Data

No external dataset is used. The evaluation is in-silico under a 2-direction PD-vs-ND protocol: 2
angles (PD = 0 deg, ND = 180 deg) x 3 evaluation seeds = 6 trials per cell, each 1400 ms of
simulated NEURON time at h.dt = 0.025 ms (TSTOP_MS = 1400). Per-trial inputs are AR(2)-correlated
Poisson event sequences over the placed ACh and GABA synapses, with bar-arrival kinematic delays
derived from each synapse's xy coordinate on the realised morphology.

## Prediction Format

The predictions file is `files/predictions.jsonl.gz` -- one row per unique cell evaluated during the
NSGA-II run, gzipped JSONL (newline-delimited JSON). Per-row fields:

* `vector_68d` -- 54-d electrophys + 14-d morphology parameter vector (concatenated; see
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants_electrophys.py` and
  `tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py` for field order)
* `dsi_vector_sum` -- ratio DSI in [0, 1]; vector-sum reduction of per-direction mean spike counts
  over PD = 0 deg and ND = 180 deg
* `pd_rate_hz` -- mean PD spike rate in Hz (over 3 eval seeds, 1400 ms trial length)
* `robustness` -- inverse-CV of per-seed DSI, in (0, 1]
* `cytoplasm_volume_um3` --
  `sum(pi * (sec.diam/2)^2 * sec.L for sec in [soma, *all_dends, ais_proximal, ais_distal])` in um^3
* `objective_F_minimised` -- 2-tuple `[-dsi, +cytoplasm_volume_um3]` (the F vector that NSGA-II
  minimises)
* `silence_failed_bool` -- True iff DSI >= 0.9999 (silence-corner saturation surrogate)
* `legit_bool` -- True iff DSI in [0.5, 0.9999) AND PD-rate >= 30 Hz AND volume <= 50000 um^3 AND
  NOT silence-failed

## Metrics

| Metric | Value |
| --- | --- |
| `n_cells_total` | 5760 |
| `n_legit_cells` (DSI in [0.5, 0.9999), PD >= 30 Hz, vol <= 50000) | 10 |
| `best_legit_dsi` | 0.9753 |
| `min_legit_cytoplasm_volume_um3` | 250.2 |
| `n_pareto_cells` (driver final population) | 2 |
| `final_hypervolume` (ref = (0, V_MAX_UM3)) | 49763.3511 |
| `final_cost_usd` | 0.2060 |
| `cuntz_top10_in_band` (Cuntz [0.2, 0.7]) | 10 / 10 |

## Main Ideas

* The cytoplasm-volume objective collapsed the optimiser onto very small dendritic trees (top-10
  LEGIT cells at ~250 um^3 cytoplasm), orders of magnitude below the t0091 cells that topped at
  ~30000 um^3 under the DSI-only or DSI-vs-PD-rate objectives.
* All top-10 LEGIT cells (ranked by DSI) cluster at Cuntz balancing factor bf = 0.5 -- squarely
  inside the Cuntz 2010 [0.2, 0.7] empirical band for real dendritic trees.
* The tightened `pd_spikes_sum < 3` silence guard correctly identified silence-corner DSI = 1.0
  cells (n_silence_corner = 1116 in this run) and excluded them from the LEGIT pool; the best legit
  DSI achieved was 0.9753 on volumes around 250.2 um^3.

## Summary

This predictions asset is the per-cell record of a single-seed 60-generation NSGA-II run optimising
DSI vs cytoplasm volume on the 68-d Bed B + 14-d morphology substrate. The run produced 5760 unique
cell evaluations at a final hypervolume of 49763.35 (reference point (0, V_MAX_UM3) with V_MAX_UM3 =
50000 um^3) and a total cost of $0.2060, well under the $6.00 cap. The asset includes the full
per-cell 68-d vector plus all evaluated diagnostics (DSI, PD-rate, robustness, cytoplasm volume, F
vector, silence-failure and LEGIT booleans).

Key findings: the cytoplasm-volume cost objective drove the optimiser onto small dendritic trees
(top-10 LEGIT volumes ~250 um^3) and produced 10 LEGIT cells (DSI in
[0.5, 0.9999), PD >= 30 Hz, vol <= 50000 um^3) -- distinct from the t0091 lineage which optimised DSI alone and converged on much larger cells. The top-10 LEGIT cells have Cuntz balancing factor bf = 0.5, inside the Cuntz 2010 [0.2, 0.7]
empirical band; the companion answer asset `cuntz-balancing-factor-prediction-check` reports the
prediction check.
