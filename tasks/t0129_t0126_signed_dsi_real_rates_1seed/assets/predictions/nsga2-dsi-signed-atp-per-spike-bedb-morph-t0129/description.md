---
spec_version: "2"
predictions_id: "nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129"
documented_by_task: "t0129_t0126_signed_dsi_real_rates_1seed"
date_documented: "2026-05-26"
---
# NSGA-II Signed DSI vs ATP per Spike on Bed B + 14-d Morphology (t0129)

## Metadata

* **Task**: `t0129_t0126_signed_dsi_real_rates_1seed`
* **GA seed**: 3517 (fresh; not in the t0124/t0126/t0128 lineage)
* **Pop size**: 96
* **N_EVAL_SEEDS**: 3; **N_DIRECTIONS**: 2 (antipodal pair 0/180 deg)
* **Generations completed**: 60 / 60
* **Pool-restart cadence**: every 10 generations
* **HV-plateau auto-stop**: disabled (per project policy `feedback_disable_hv_plateau_autostop`)
* **Cost cap**: $8.00 (project per-task default)
* **Final cost (active NSGA-II window)**: $0.6469
* **Final cost (full instance lifetime)**: $0.9650
* **Stop trigger**: n_gen_reached

## Overview

This predictions asset captures every cell evaluated by the t0129 single-seed NSGA-II run on the
68-d Bed B + 14-d morphology substrate. The two minimised objectives are `F[0] = -dsi_signed`
(signed antipodal DSI maximised, range `[-1, 1]`, silence-guard sentinel = -1 for cells with
`R_PD < 3` PD spikes) and `F[1] = +atp_per_spike_molecules` (Sengupta 2010 recipe; lower is better).
The signed antipodal DSI is the literature DS-RGC definition `DSI = (R_PD - R_ND) / (R_PD + R_ND)`,
where `R_PD` is the mean PD-direction firing rate (0 deg) and `R_ND` is the mean ND-direction firing
rate (180 deg). The Pareto front captures the DSI / ATP trade-off across the 68-d parameter space
with reversed-preference cells now visible as negative values.

This asset corrects two known issues with t0126's analogous predictions
(`nsga2-dsi-atp-per-spike-bedb-morph-60gen`):

1. **Signed DSI replaces vector-sum DSI.** Vector-sum collapses the antipodal pair `[0, 180 deg]` to
   a non-negative scalar `|R_PD - R_ND| / (R_PD + R_ND)`, discarding the sign. Reversed-preference
   cells (R_ND > R_PD) look identical to true-PD-preferring cells under vector-sum; signed DSI makes
   them detectable as negative values.

2. **Real per-cell PD/ND firing rates.** t0126's downstream `cell_trace_seed8929.jsonl` was
   hand-synthesised after the run with `pd_rate_hz = 40` as a hard-coded placeholder for every cell
   (per project memory `project_t0126_cell_trace_synthesised`). This asset captures the real
   per-direction firing rates the evaluator computes from actual spike counts; no placeholders, no
   env-var-driven sink that can silently drop in worker processes.

## Model

68-d Bed B compartmental DSGC model (54-d electrophysiological + 14-d morphology). NEURON-backed
simulation via the t0080 channel MOD pack (13 channels, dendritic-spike capable) and the t0024
vendored DSGC NEURON template. NSGA-II driven by pymoo (0.6.1.6) with SBX crossover (`eta=15`) and
polynomial mutation (`eta=20`). Single GA seed (3517); 96 individuals per generation x 60
generations = 5,760 evaluations. Antipodal direction pair `[0 deg, 180 deg]`, `TSTOP_MS = 1400`,
`N_EVAL_SEEDS = 3`. Silence guard at `pd_spikes_sum < 3` returns the sentinel `dsi_signed = -1.0`.
Pool-restart cadence: every 10 generations (per project memory
`feedback_nsga2_pool_restart_every_10`). HV-plateau auto-stop is disabled (per project memory
`feedback_disable_hv_plateau_autostop`).

## Data

Synthetic procedurally-generated DSGC morphologies (no external dataset; the 14-d morphology vector
is sampled from the t0090 morphology generator's `PARAM_BOUNDS`). Per cell the protocol runs 3
evaluation seeds x 2 directions (0 deg PD and 180 deg ND) = 6 trials. Each trial is a 1.4 s
simulation with full HH mechanics, the t0080 channel pack, and the Sengupta 2010 ATP-per-spike
recipe (per-segment Na+ current integrated over each AP window). The same 68-d parameter bounds are
used as in t0126; no parameter-space changes.

## Prediction Format

Two files:

1. `files/predictions-pareto-9-cells.jsonl` -- one JSON record per Pareto cell. Fields:
   `pareto_rank`, `generation`, `cell_idx_in_gen`, `vector_68d`, `morphology_vector_14d`,
   `dsi_signed`, `atp_per_spike_molecules`, `pd_rate_hz`, `nd_rate_hz`, `silence_failed`,
   `n_errors`, `objective_F_minimised` (= `[-dsi_signed, +atp_per_spike_molecules]`), `is_pareto`.

2. `files/predictions-all-cells.jsonl.gz` -- one JSON record per evaluated cell, gzip-compressed
   (raw size 9.2 MB exceeds the 3 MB compression threshold). This is a verbatim copy of
   `results/cell_params.jsonl`. Fields: `gen` (-1 for Phase A random init, 1..59 for NSGA-II
   generations), `cell_idx`, `param_vector` (68 floats), `dsi_signed`, `atp_per_spike_molecules`,
   `pd_rate_hz`, `nd_rate_hz`, `silence_failed`, `n_errors`.

The Pareto file lets downstream tasks read the headline result without decompressing 5,760 rows; the
all-cells file lets them mine the full parameter-space coverage. Both files use the same 68-d vector
convention as t0126 (first 54 dimensions electrophys, last 14 morphology).

## Metrics

* **Best signed DSI**: **1.0000** (at ATP **0.780e+06** to **3.633e+06** molecules/spike across the
  front)
* **Median signed DSI (Pareto)**: **0.5714**
* **Min ATP per spike (Pareto)**: **0.780e+06** molecules
* **Median ATP per spike (Pareto)**: **3.633e+06** molecules
* **Headline cell PD/ND rates**: PD = **6.429 Hz**, ND = **0.000 Hz** (DSI=1.0 corner is
  ND-silenced)
* **n_cells_total**: **5,760** (96 Phase A + 5,664 NSGA-II)
* **n_cells_pareto**: **9**
* **n_cells_viable** (silence guard not tripped): **5,496**
* **n_cells_silenced** (silence guard tripped, `dsi_signed=-1` sentinel): **264**
* **n_cells_viable_negative_dsi** (reversed preference R_ND > R_PD): **95**
* **min DSI among viable cells** (deepest reversed-preference): **-0.7778**
* **Final hypervolume**: **1.9996e+10**

## Main Ideas

* The signed-DSI re-evaluation reveals **95 viable cells** with genuinely reversed preference (R_ND
  \> R_PD) that vector-sum DSI would have shown as positive- magnitude cells. The deepest reversal
  is `dsi_signed = -0.778`. None of these cells are Pareto-optimal under signed DSI (negative DSI is
  dominated in F-space by the large cluster of DSI=0 silent-or-bidirectional cells at the ATP
  minimum), but they WOULD have occupied the Pareto front under vector-sum, polluting the
  high-magnitude region with cells whose preferred direction is actually opposite to what vector-sum
  suggests.
* The 9-cell t0129 Pareto front is **structurally similar** to t0126's 6-cell front (both span DSI
  from 0 to 1 at ATP in the 1-8 million molecules/spike range), but the t0129 minimum ATP is about
  **2.3x lower** (0.78e+06 vs 1.83e+06 in t0126; the difference is seed variation, not a
  methodological change).
* Real per-cell PD/ND firing rates replace t0126's `pd_rate_hz = 40` placeholder. The Pareto-median
  PD rate is **2.62 Hz** and median ND rate is **0.71 Hz** -- far below t0126's recorded 40 Hz
  placeholder. Downstream analyses (joint-pass thresholds, factor analysis of rate-vs-DSI structure)
  that consumed t0126's placeholders gave biased results; t0129 provides the corrective baseline on
  a fresh seed.

## Summary

This asset is the primary output of t0129. It captures the full per-cell parameter-vector +
objective record for every evaluation in the NSGA-II run (5,760 cells across Phase A and 60
generations) plus the final 9-cell Pareto front under signed antipodal DSI. The two evaluator
corrections (signed DSI replacing vector-sum; real per-cell firing rates replacing the placeholder)
close the two known data-integrity gaps in t0126's analogous asset. Downstream tasks can mine the
all-cells file for parameter-space coverage analysis or the Pareto file for direct headline-cell
comparison; both files use the same 68-d vector convention as t0126 so cross-task comparisons are
direct.

The asset's `metrics_at_creation` field summarises the headline numbers; this canonical description
provides the methodological context, and `details.json` enumerates the full per-cell schema for both
files.
