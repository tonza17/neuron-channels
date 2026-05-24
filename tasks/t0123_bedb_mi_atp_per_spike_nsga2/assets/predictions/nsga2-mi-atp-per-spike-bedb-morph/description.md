---
spec_version: "2"
predictions_id: "nsga2-mi-atp-per-spike-bedb-morph"
documented_by_task: "t0123_bedb_mi_atp_per_spike_nsga2"
date_documented: "2026-05-24"
---
# NSGA-II Predictions: MI vs ATP-per-Spike on Bed B + 14-d Morph

## Metadata

* **Name**: NSGA-II Pareto front: spike-count MI vs ATP-per-spike on Bed B + 14-d morph
* **Model**: Procedural Bed B DSGC cell (t0090 generator + t0092 z-axis soma patch, t0080 NEURON MOD
  channels)
* **Datasets**: (none; in-silico evaluation only)
* **Format**: jsonl.gz
* **Instances**: 5760
* **Created by**: t0123_bedb_mi_atp_per_spike_nsga2
* **GA seed**: 441
* **Generations completed**: 60 / 60
* **Final cost (USD)**: $0.7490 / $6.00 cap

## Overview

This predictions asset captures every per-cell evaluation from the t0123 single-seed 68-d NSGA-II
run on the Bed B + 14-d morphology substrate. The 2-objective optimisation maximises spike-count MI
(Miller-Madow corrected, 4-direction antipodal protocol) and simultaneously minimises ATP per spike
(Sengupta 2010 recipe, integrated inward Na charge across soma + AIS + every dendrite compartment).
DSI and PD-rate are tracked as diagnostics, not optimised. The top-10 Pareto cells are additionally
re-evaluated post-hoc under the Strong-Bialek 1998 direct method at 8 directions x 20 trials per
direction to recover a literature-comparable bits/s rate for the Niven 2007 comparison.

The run forks the t0122 NSGA-II substrate end-to-end (pop=96, N_EVAL_SEEDS=3,
_POOL_RESTART_EVERY=10, HV_PLATEAU_AUTO_STOP=False, silence guard pd_spikes_sum < 3); the only
behavioural deltas are both objectives swapped to (MI, ATP/spike), N_DIRECTIONS raised from 2 to 4,
and the reduced `N_GEN_MAX = 60` / `COST_CAP_USD = 6.0` constraints from the task description.

## Model

The cell is a procedural DSGC built by `generate_fixed_morphology` (t0092 fix wrapper around t0090's
generator) and parameterised by the 14-d morphology vector concatenated with the 54-d electrophys
vector. The electrophys block uses the t0080 BedB v3 13-channel MOD library (Nav1.6 + napt80 +
nart80 sodium; KDR / Kv3 / Kv4 / Kv7 potassium; BKT80 and SKAHPT80 calcium-activated potassium;
IhT80; T- and L-type calcium; SKT80). Synaptic inputs are AR(2)-correlated ACh / GABA bundles placed
by the parametric placer (t0024 de Rosenroll 2026 ports), with NMDA conductance on dendrites. The
AIS is split into proximal / distal segments at the t0080-default ratio. All parameters (channel
densities, synapse weights, NMDA conductance, AIS lengths, morphology branching parameters) are part
of the 68-d optimisation vector and vary per cell.

## Data

No external dataset is used. The evaluation is in-silico under a 4-direction antipodal-pair
protocol: 4 angles (0, 90, 180, 270 deg) x 3 evaluation seeds = 12 trials per cell, each 1400 ms of
simulated NEURON time at h.dt = 0.025 ms (TSTOP_MS = 1400). Per-trial inputs are AR(2)-correlated
Poisson event sequences over the placed ACh and GABA synapses, with bar-arrival kinematic delays
derived from each synapse's xy coordinate on the realised morphology. Inward Na current `seg.ina` is
recorded at simulation dt on every segment of the soma + AIS proximal + AIS distal + every dendrite;
AP windows are detected via somatic Vm threshold crossings at -20 mV with a 2 ms refractory and
integrated over +/-2 ms around each peak.

## Prediction Format

The predictions file is `files/predictions.jsonl.gz` -- one row per unique cell evaluated during the
NSGA-II run, gzipped JSONL. Per-row fields:

* `generation` -- generation index (0..60) when the cell was evaluated
* `cell_index` -- 0-indexed identifier within the run
* `vector_68d` -- 54-d electrophys + 14-d morphology parameter vector (concatenated)
* `mi_count_bits` -- spike-count MI in bits, Miller-Madow corrected, 4-direction contingency table
* `atp_per_spike_molecules` -- mean ATP molecules per AP across all trials
* `atp_per_ap_molecules` -- same as `atp_per_spike_molecules` (retained for back-compat)
* `atp_per_ap_compartment_breakdown` -- {"soma": float, "ais": float, "dendrites_total": float}
* `firing_hz_per_dir` -- per-direction firing rate in Hz (dir_0, dir_90, dir_180, dir_270)
* `dsi_vector_sum` -- vector-sum DSI in [0, 1] (tracked diagnostic)
* `pd_rate_hz` -- mean PD spike rate in Hz (tracked diagnostic)
* `objective_F_minimised` -- 2-tuple `[-mi_count_bits, +atp_per_spike_molecules]` (F vector that
  NSGA-II minimised)
* `silence_failed_bool` (alias `silence_failed`) -- True iff pd_spikes_sum < 3 OR ATP/spike was NaN
* `legit_bool` -- True iff DSI >= 0.5 AND PD-rate >= 30 Hz AND NOT silence-failed

The 10 cells included in the post-hoc Strong-Bialek rerun additionally carry
`mi_strong_bialek_bits_per_sec`, `std_err_bits_per_sec`, and `r_squared`.

## Metrics

| Metric | Value |
| --- | --- |
| `n_cells_total` | 5760 |
| `n_legit_cells` (DSI >= 0.5, PD >= 30 Hz, NOT silence-failed) | 0 |
| `best_mi_count_bits` | 1.4590 bits |
| `min_atp_per_spike_molecules` | 6.755e+05 |
| `n_pareto_cells` (driver final population) | 10 |
| `final_hypervolume` | 29173000508.2351 |
| `final_cost_usd` | $0.7490 |
| `top10_max_bits_per_sec` (Strong-Bialek) | 0.0 |

## Main Ideas

* The 2-objective (max MI, min ATP/spike) Pareto front traces the information-energy trade-off for
  the DSGC substrate at the resolution of a 4-direction spike-count code (2-bit MI ceiling). The
  top-10 cells re-evaluated under Strong-Bialek 1998 give the bits/s rate that is directly
  comparable to the Niven 2007 fly-photoreceptor curve.
* DSI / PD-rate are computed and stored per cell for downstream joint-pass filtering even though
  they do not enter the F vector; the silence guard (`pd_spikes_sum < 3`) inherited from t0122
  catches cells that achieve low ATP/spike by simply not spiking and excludes them from the LEGIT
  cohort.
* The Carter-Bean 2009 ATP/AP/cm benchmark at the AIS calibrates the Sengupta 2010 recipe before
  launch; see the smoke gate report and `results/images/carter_bean_atp_per_ap_check.png`.

## Summary

This predictions asset is the per-cell record of a single-seed 60-generation NSGA-II run optimising
MI vs ATP-per-spike on the 68-d Bed B + 14-d morphology substrate. The run produced 5760 unique cell
evaluations at a final hypervolume of 29173000508.24 and a total cost of $0.7490, within the $6.00
cap. The asset includes the full per-cell 68-d vector plus all evaluated diagnostics (MI, ATP/spike,
per-compartment ATP breakdown, per-direction firing rates, DSI / PD-rate, F vector, silence-failure
and LEGIT booleans). The top-10 Pareto cells additionally carry Strong-Bialek 1998 direct-method MI
in bits/s for the Niven 2007 comparison documented in the companion answer asset
`dsgc-bits-per-atp-vs-niven-2007`.
