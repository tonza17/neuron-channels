# Predictions: `voltage-gated-channels`

3 predictions asset(s).

[Back to all predictions](../README.md)

---

<details>
<summary>📊 <strong>NSGA-II DSI vs ATP-per-Spike on Bed B + 14-d Morphology</strong>
(<code>nsga2-dsi-atp-per-spike-bedb-morph</code>) — 864 instances
(jsonl.gz)</summary>

| Field | Value |
|---|---|
| **ID** | `nsga2-dsi-atp-per-spike-bedb-morph` |
| **Model ID** | — |
| **Model** | 68-d Bed B compartmental DSGC model (54-d electrophysiological + 14-d morphology), NEURON-backed, NSGA-II via pymoo, single GA seed. |
| **Datasets** |  |
| **Format** | jsonl.gz |
| **Instances** | 864 |
| **Date created** | 2026-05-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Created by** | [`t0124_bedb_dsi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0124_bedb_dsi_atp_per_spike_nsga2.md) |
| **Documentation** | [`description.md`](../../../tasks\t0124_bedb_dsi_atp_per_spike_nsga2\assets\predictions\nsga2-dsi-atp-per-spike-bedb-morph\description.md) |

**Metrics at creation:**

* **best_dsi_legit**: 0.8823529411764706
* **min_atp_per_spike**: 2111996.058295004
* **joint_pass_count**: 0
* **n_generations_completed**: 9
* **n_cells_total**: 864
* **n_cells_pareto**: 5
* **final_hypervolume**: 17636714765.016483
* **final_cost_usd**: 0.0728
* **stop_trigger**: operator_stop

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

This predictions asset captures every cell evaluated by the t0124 single-seed NSGA-II run on
the 68-d Bed B + 14-d morphology substrate. The two minimised objectives are F[0] =
-dsi_vector_sum (DSI maximised, with silence-guard sentinel = -1 for cells with R_PD < 3 PD
spikes) and F[1] = +atp_per_spike_molecules (Sengupta 2010 recipe; lower is better). The
Pareto front captures the DSI / ATP trade-off across the 68-d parameter space.

## Model

68-d Bed B compartmental DSGC model (54-d electrophysiological + 14-d morphology).
NEURON-backed simulation via the t0080 channel MOD pack and t0024 vendored DSGC NEURON
template. NSGA-II driven by pymoo with default SBX crossover (eta=15) and polynomial mutation
(eta=20).

## Data

Synthetic procedurally-generated DSGC morphologies (no external dataset; the 14-d morphology
vector is sampled from tasks/t0090's PARAM_BOUNDS). Per cell the protocol runs 3 evaluation
seeds x 2 directions (0 deg PD and 180 deg ND) = 6 trials. Each trial is a 1.4 s simulation
with full HH mechanics and the Sengupta 2010 ATP-per-spike recipe (per-segment Na+ current
integrated over each AP window).

## Prediction Format

JSONL gzip-compressed (`files/predictions.jsonl.gz`). One JSON object per evaluated cell.
Schema (see `details.json` `prediction_schema` for full list): `generation`, `vector_68d`
(54-d electrophys + 14-d morph), `dsi_vector_sum`, `atp_per_spike_molecules`,
`objective_F_minimised`, `is_pareto`, `silence_failed_bool`, `legit_bool`, plus per-direction
firing rates and diagnostic cytoplasm volume / MI / per-compartment ATP breakdown.

## Metrics

* **Best legit DSI**: 0.8824
* **Min ATP per spike**: 2.112e+06 molecules
* **Joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz AND ATP <= median)**: 0
* **Final hypervolume**: 1.7637e+10
* **n_cells_total**: 864
* **n_cells_pareto**: 5

## Main Ideas

* The Pareto front captures the DSI / ATP trade-off in the 68-d Bed B + 14-d morphology
  substrate; downstream tasks can mine this asset for joint-pass cells satisfying both
  function and energy criteria.
* Cells with DSI = -1 (silence guard tripped) are kept in the asset for completeness but
  flagged via `legit_bool = false` and `silence_failed_bool = true`.
* The Sengupta 2010 ATP recipe is verified against the Carter & Bean 2009 first-principles
  canonical band [1e8, 1e9] ATP/AP/cm via the pre-launch smoke-gate (check 9); on the
  canonical anchor cell the recipe sits inside the PASS band.

## Summary

This asset is the primary output of t0124. Downstream tasks (e.g., literature comparison,
joint Pareto analysis with t0122's cytoplasm front, follow-up multi-seed replication) consume
the per-cell records via the predictions aggregator. The asset's `metrics_at_creation` field
summarises the headline numbers; the canonical `description.md` (this file) provides the
methodological context, and the `details.json` field manifest enumerates every per-cell schema
field.

## Reproducing the asset

1. Provision a Vast.ai EPYC instance.
2. `nrnivmodl` on `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`.
3. `python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.random_init`.
4. `python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.smoke_gate`.
5. `python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.nsga2_driver --seed 6650 --pop
   96 --n-gen 60 --n-eval-seeds 3 --n-directions 2`.
6. `python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.build_t0124_outputs --seed
   6650`.

</details>

<details>
<summary>📊 <strong>V_rest sweep on t0022 DSGC channel testbed
(deterministic)</strong> (<code>t0026-vrest-sweep-t0022</code>) — 96
instances (csv)</summary>

| Field | Value |
|---|---|
| **ID** | `t0026-vrest-sweep-t0022` |
| **Model ID** | — |
| **Model** | ModelDB 189347 DSGC compartmental model (Mazurek lab) ported in t0008 and modified in t0022 to expose deterministic per-dendrite E-I scheduling. The model uses HHst membrane (with leak reversal eleak_HHst) on the soma and pas membrane (with e_pas) on dendrites, plus deterministic glutamate/GABA stimulus pairs constructed by tasks/t0022_modify_dsgc_channel_testbed/code (library asset modeldb_189347_dsgc). The V_rest is shifted by overriding both h.v_init and the resting parameters of every HHst- and pas-bearing section before h.finitialize. |
| **Datasets** |  |
| **Format** | csv |
| **Instances** | 96 |
| **Date created** | 2026-04-21 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Created by** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Documentation** | [`description.md`](../../../tasks\t0026_vrest_sweep_tuning_curves_dsgc\assets\predictions\t0026-vrest-sweep-t0022\description.md) |

**Metrics at creation:**

* **best_dsi_across_vrest**: 0.6562
* **best_dsi_at_vrest_mv**: -60.0
* **min_hwhm_deg_across_vrest**: 0.8
* **peak_hz_at_minus_60mv**: 15.0
* **null_hz_at_minus_60mv**: 0.0

# V_rest sweep on t0022 DSGC channel testbed (deterministic)

## Metadata

* **Name**: V_rest sweep on t0022 DSGC channel testbed (deterministic)
* **Model**: t0022 DSGC channel testbed (library `modeldb_189347_dsgc` ported in t0008,
  exposed-knobs version in t0022) — ModelDB 189347 cable-theory DSGC with HHst soma and pas
  dendrites, deterministic per-dendrite glutamate/GABA scheduling
* **Datasets**: none (synthetic stimulus generated in-script)
* **Format**: csv
* **Instances**: 96 (8 V_rest x 12 directions x 1 trial)
* **Created by**: t0026_vrest_sweep_tuning_curves_dsgc

## Overview

These predictions capture how the t0022 DSGC compartmental model responds to a moving-bar
stimulus across eight resting potentials spanning the physiological range (-90 mV to -20 mV in
10 mV steps). At each V_rest, the model is driven by the standard 12-direction protocol and
the per-trial spike count, peak somatic voltage, and firing rate are recorded.

V_rest is set by overriding both `h.v_init` and the resting parameters of every HHst- and
pas-bearing section (`eleak_HHst` and `e_pas`) before each trial's `h.finitialize`. Moving
both together (rather than just `v_init`) produces a true resting-potential shift instead of a
transient initial-condition tweak that would re-settle to `eleak` within a few milliseconds.

The t0022 model uses deterministic per-dendrite E-I scheduling, so a single trial per (V_rest,
angle) pair is sufficient to characterise the tuning curve — there is no trial-to-trial noise
to average out. The predictions support biophysical analysis of how V_rest modulates direction
tuning sharpness, peak firing rate, and HWHM via Na-channel inactivation and the resulting
changes in spike threshold.

## Model

The model is the ModelDB 189347 cable-theory DSGC originally published by the Mazurek lab and
ported in task t0008 (`modeldb_189347_dsgc`), then extended in t0022 to expose the
per-dendrite E-I scheduling knobs needed for parameter sweeps. Key biophysical parameters:

* Soma: HHst membrane (transient Na, K-DR, and leak), `eleak_HHst` is the leak reversal that
  determines V_rest in the absence of synaptic drive.
* Dendrites: pas membrane (passive cable) with `e_pas` reversal.
* Synapses: per-dendrite (glutamate, GABA) pairs scheduled deterministically by the t0022
  simulation harness based on motion direction (282 pairs constructed at cell build).

For each trial in this sweep, the harness:

1. Builds the cell once (cached in CellContext across the full sweep).
2. Resets the per-trial schedule using `apply_params + schedule_ei_onsets`.
3. Calls `set_vrest(h=h, v_rest_mv=V)` which writes V to `h.v_init`, all `eleak_HHst`, and all
   `e_pas`.
4. Runs `h.finitialize(V) + h.continuerun(TSTOP_MS)` for a 1-second simulation window.
5. Records spike count (threshold crossings of the soma), peak somatic mV, and firing rate.

## Data

No external dataset is consumed. The stimulus is a synthetic moving bar at 12 evenly spaced
directions (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330 deg), with the stimulus
schedule generated by the t0022 simulation harness. The same per-direction onset schedule is
used for every V_rest value, so cross-V_rest differences are attributable to membrane
biophysics, not stimulus variation.

## Prediction Format

`files/predictions-vrest-sweep-t0022.csv` is a UTF-8 CSV with header row and 96 data rows.
Columns:

| Column | Type | Description |
| --- | --- | --- |
| `v_rest_mv` | float | Resting potential set by `set_vrest`, one of -90/-80/-70/-60/-50/-40/-30/-20 mV |
| `trial` | int | Trial index per (V_rest, angle); always 0 for this deterministic sweep |
| `direction_deg` | int | Motion direction in degrees, one of 0/30/60/90/120/150/180/210/240/270/300/330 |
| `spike_count` | int | Count of soma spikes during the 1-second simulation window |
| `peak_mv` | float | Peak somatic membrane voltage during the trial, in mV |
| `firing_rate_hz` | float | spike_count / 1.0 s |

Example rows:

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-90.0,0,0,6,43.272,6.000000
-60.0,0,0,14,44.288,14.000000
-30.0,0,0,129,43.825,129.000000
```

## Metrics

Per-V_rest scalar metrics are derived in
`tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/compute_vrest_metrics.py` and stored in
`data/t0022/vrest_metrics.csv`. DSI is computed as the magnitude of the vector sum of mean
firing rates across angles, normalised by their sum (Mazurek convention). HWHM is
half-width-at-half-max of the mean firing-rate curve interpolated around the preferred
direction.

| V_rest (mV) | Peak Hz | Null Hz | DSI | HWHM (deg) | Pref dir (deg) |
| --- | --- | --- | --- | --- | --- |
| -90 | 6.00 | 0.00 | 0.485 | 0.8 | 19.4 |
| -80 | 11.00 | 0.00 | 0.600 | 0.8 | 42.3 |
| -70 | 12.00 | 0.00 | 0.637 | 84.0 | 50.7 |
| -60 | 15.00 | 0.00 | 0.656 | 86.2 | 49.3 |
| -50 | 41.00 | 20.41 | 0.205 | 102.2 | 42.4 |
| -40 | 70.00 | 50.64 | 0.095 | 180.0 | 49.1 |
| -30 | 129.00 | 111.20 | 0.046 | 180.0 | 48.0 |
| -20 | 26.00 | 7.40 | 0.275 | 107.8 | 48.0 |

## Main Ideas

* DSI peaks around V_rest = -60 mV (DSI = 0.656, HWHM = 86 deg) — close to the model's default
  resting potential — and degrades both when hyperpolarised below -80 mV (insufficient drive
  to cross spike threshold) and depolarised above -50 mV (null direction recruits
  suprathreshold firing, washing out selectivity).
* Peak firing rate is non-monotonic with V_rest: it climbs from 6 Hz at -90 to a maximum of
  129 Hz at -30, then collapses to 26 Hz at -20 mV consistent with Na-channel inactivation
  reducing spike availability when the membrane sits above approximately -25 mV.
* The sweep validates the multi-knob V_rest override approach: the deterministic t0022 model
  produces clean, reproducible tuning curves at every V_rest value, with no trial-to-trial
  noise. Downstream tasks can use this V_rest x direction grid to fit phenomenological models
  of resting-potential modulation of direction tuning.

## Summary

This predictions asset records the per-trial outcomes (96 rows) of the t0022 DSGC
compartmental model under a V_rest sweep across the eight values -90 / -80 / -70 / -60 / -50 /
-40 / -30 / -20 mV crossed with the 12-direction moving-bar protocol. V_rest is shifted by
simultaneously overriding `h.v_init`, all `eleak_HHst`, and all `e_pas` parameters before each
trial's `h.finitialize`, producing a stable steady-state V_rest rather than a transient.

The headline finding is a non-monotonic relationship between V_rest and direction selectivity:
DSI is maximised at V_rest approximately equal to -60 mV (DSI = 0.66) and collapses both at
hyperpolarised potentials (insufficient drive) and depolarised potentials (null-direction
firing washes out selectivity). Peak firing rate climbs monotonically until V_rest = -30 mV
(129 Hz) and then crashes at V_rest = -20 mV (26 Hz) consistent with sodium channel
inactivation. These predictions feed the polar plots in `results/images/` and the per-V_rest
metric grid in `results/metrics.json`, providing a baseline against which the stochastic t0024
DSGC model can be compared in the same task.

</details>

<details>
<summary>📊 <strong>V_rest sweep on t0024 DSGC channel testbed (stochastic AR(2)
release)</strong> (<code>t0026-vrest-sweep-t0024</code>) — 960 instances
(csv)</summary>

| Field | Value |
|---|---|
| **ID** | `t0026-vrest-sweep-t0024` |
| **Model ID** | — |
| **Model** | de Rosenroll 2026 DSGC compartmental model ported in t0024 (library asset de_rosenroll_2026_dsgc). The model uses HHst membrane (with leak reversal eleak_HHst) on the soma and pas membrane (with e_pas) on dendrites, plus per-dendrite AR(2)-correlated stochastic glutamate/GABA release with a default temporal correlation rho=0.6 between successive synaptic events. The V_rest is shifted by overriding both h.v_init and the resting parameters of every HHst- and pas-bearing section before h.finitialize. |
| **Datasets** |  |
| **Format** | csv |
| **Instances** | 960 |
| **Date created** | 2026-04-21 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Created by** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Documentation** | [`description.md`](../../../tasks\t0026_vrest_sweep_tuning_curves_dsgc\assets\predictions\t0026-vrest-sweep-t0024\description.md) |

**Metrics at creation:**

* **best_dsi_across_vrest**: 0.6754
* **best_dsi_at_vrest_mv**: -90.0
* **min_hwhm_deg_across_vrest**: 65.2
* **peak_hz_at_minus_60mv**: 5.0
* **null_hz_at_minus_60mv**: 0.51

# V_rest sweep on t0024 DSGC channel testbed (stochastic AR(2) release)

## Metadata

* **Name**: V_rest sweep on t0024 DSGC channel testbed (stochastic AR(2) release)
* **Model**: t0024 DSGC channel testbed (library asset `de_rosenroll_2026_dsgc`) — de
  Rosenroll 2026 cable-theory DSGC with HHst soma, pas dendrites, and AR(2)-correlated
  per-dendrite glutamate/GABA scheduling at default rho=0.6
* **Datasets**: none (synthetic stimulus generated in-script)
* **Format**: csv
* **Instances**: 960 (8 V_rest x 12 directions x 10 trials)
* **Created by**: t0026_vrest_sweep_tuning_curves_dsgc

## Overview

These predictions capture how the t0024 DSGC compartmental model responds to a moving-bar
stimulus across eight resting potentials spanning the physiological range (-90 mV to -20 mV in
10 mV steps). At each V_rest, the model is driven by the standard 12-direction protocol with
10 trials per angle to average out the trial-to-trial variability introduced by the
AR(2)-correlated stochastic release process (rho=0.6). For each trial the per-trial spike
count, peak somatic voltage, and firing rate are recorded.

V_rest is set by overriding both `h.v_init` and the resting parameters of every HHst- and
pas-bearing section (`eleak_HHst` and `e_pas`) before each trial's `h.finitialize`. Moving
both together (rather than just `v_init`) produces a true resting-potential shift instead of a
transient initial-condition tweak that would re-settle to `eleak` within a few milliseconds.

The t0024 model uses temporally correlated stochastic E-I release scheduling, so 10 trials per
(V_rest, angle) pair are required to estimate the mean firing rate against the variance
introduced by the AR(2) process. The total sweep runtime was 11,562 s (~3.21 h) on the local
Windows workstation. The predictions support biophysical analysis of how V_rest modulates
direction tuning sharpness, peak firing rate, and HWHM in the presence of physiologically
realistic correlated noise that the deterministic t0022 sister sweep cannot reproduce.

## Model

The model is the de Rosenroll 2026 DSGC ported in task t0024 (library asset
`de_rosenroll_2026_dsgc`), which extends the ModelDB-based DSGC architecture with
AR(2)-correlated per-dendrite stochastic release. Key biophysical parameters:

* Soma: HHst membrane (transient Na, K-DR, and leak), `eleak_HHst` is the leak reversal that
  determines V_rest in the absence of synaptic drive.
* Dendrites: pas membrane (passive cable) with `e_pas` reversal.
* Synapses: per-dendrite (glutamate, GABA) pairs scheduled by the t0024 simulation harness
  with AR(2) temporal correlation between successive events; rho=0.6 is the default
  correlation coefficient.

For each trial in this sweep, the harness:

1. Builds the cell once (cached in CellContext across the full sweep).
2. Resets the per-trial schedule using `apply_params + schedule_ei_onsets` with a fresh AR(2)
   draw.
3. Calls `set_vrest(h=h, v_rest_mv=V)` which writes V to `h.v_init`, all `eleak_HHst`, and all
   `e_pas`.
4. Runs `h.finitialize(V) + h.continuerun(TSTOP_MS)` for a 1-second simulation window.
5. Records spike count (threshold crossings of the soma), peak somatic mV, and firing rate.

## Data

No external dataset is consumed. The stimulus is a synthetic moving bar at 12 evenly spaced
directions (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330 deg), with the stimulus
schedule generated by the t0024 simulation harness. Each (V_rest, angle, trial) combination
receives a fresh AR(2)-correlated synaptic schedule, so cross-V_rest differences are
attributable to membrane biophysics and noise realisations, not deterministic stimulus
variation.

## Prediction Format

`files/predictions-vrest-sweep-t0024.csv` is a UTF-8 CSV with header row and 960 data rows.
Columns:

| Column | Type | Description |
| --- | --- | --- |
| `v_rest_mv` | float | Resting potential set by `set_vrest`, one of -90/-80/-70/-60/-50/-40/-30/-20 mV |
| `trial` | int | Trial index per (V_rest, angle); 0..9 for this stochastic sweep |
| `direction_deg` | int | Motion direction in degrees, one of 0/30/60/90/120/150/180/210/240/270/300/330 |
| `spike_count` | int | Count of soma spikes during the 1-second simulation window |
| `peak_mv` | float | Peak somatic membrane voltage during the trial, in mV |
| `firing_rate_hz` | float | spike_count / 1.0 s |

Example rows:

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-90.0,0,0,0,-26.118,0.000000
-60.0,0,0,3,38.792,3.000000
-20.0,0,0,8,42.611,8.000000
```

## Metrics

Per-V_rest scalar metrics are derived in
`tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/compute_vrest_metrics.py` and stored in
`data/t0024/vrest_metrics.csv`. Mean firing rate per (V_rest, angle) is computed across the 10
trials before DSI/HWHM evaluation. DSI uses the Mazurek vector-sum convention, normalised by
the sum of mean firing rates. HWHM is half-width-at-half-max of the mean firing-rate curve
interpolated around the preferred direction.

| V_rest (mV) | Peak Hz | Null Hz | DSI | HWHM (deg) | Pref dir (deg) |
| --- | --- | --- | --- | --- | --- |
| -90 | 1.50 | 0.00 | 0.675 | 65.2 | 351.6 |
| -80 | 2.70 | 0.06 | 0.549 | 68.4 | 350.4 |
| -70 | 4.00 | 0.26 | 0.470 | 70.5 | 355.6 |
| -60 | 5.00 | 0.51 | 0.446 | 78.5 | 0.9 |
| -50 | 6.30 | 0.30 | 0.560 | 70.0 | 6.8 |
| -40 | 6.80 | 0.00 | 0.625 | 67.7 | 10.7 |
| -30 | 7.40 | 0.16 | 0.590 | 66.5 | 11.5 |
| -20 | 7.60 | 1.88 | 0.361 | 83.3 | 11.9 |

## Main Ideas

* DSI is U-shaped across V_rest with maxima at the extremes (-90 mV: DSI = 0.675, -40 mV: DSI
  = 0.625) and a minimum near V_rest = -60 mV (DSI = 0.446) — a qualitatively different
  pattern from the t0022 deterministic sweep, where DSI peaks sharply at -60 mV and degrades
  monotonically away from it.
* Peak firing rate increases monotonically with depolarisation (1.5 Hz at -90 → 7.6 Hz at -20)
  with no hyper-depolarisation collapse from Na inactivation. The AR(2) noise apparently
  flattens the spike-availability response so the model never reaches the saturating regime
  that the deterministic t0022 model enters above -50 mV.
* HWHM is broad (65-83 deg) and only weakly modulated by V_rest in this stochastic model — in
  sharp contrast to t0022 where HWHM compresses to <1 deg below V=-60 because almost no spikes
  fire off the preferred direction. The AR(2) release introduces enough off-preferred firing
  to smooth the curve everywhere.
* The two strongest DSI conditions (-90 and -40 mV) bracket the model's default operating
  regime, suggesting that the AR(2) release stochasticity could be exploited by upstream
  circuitry to tune direction selectivity by adjusting the cell's holding potential — a
  possibility absent from the deterministic model.

## Summary

This predictions asset records the per-trial outcomes (960 rows) of the t0024 DSGC
compartmental model with AR(2)-correlated stochastic release (rho=0.6) under a V_rest sweep
across the eight values -90 / -80 / -70 / -60 / -50 / -40 / -30 / -20 mV crossed with the
12-direction moving-bar protocol and 10 trials per angle. V_rest is shifted by simultaneously
overriding `h.v_init`, all `eleak_HHst`, and all `e_pas` parameters before each trial's
`h.finitialize`, producing a stable steady-state V_rest rather than a transient.

The headline finding is a U-shaped DSI vs V_rest relationship: DSI is highest at the extremes
(-90 mV: DSI = 0.675; -40 mV: DSI = 0.625) and lowest near V_rest approximately equal to -60
mV (DSI = 0.446). Peak firing rate climbs monotonically with depolarisation (1.5 Hz at -90 to
7.6 Hz at -20) without the sharp collapse seen in the deterministic t0022 model at -20 mV.
HWHM is substantially broader (65-83 deg vs 0.8-180 deg in t0022), indicating that AR(2)
release smooths the angular tuning even at hyperpolarised V_rest where t0022 produces
near-binary responses. These predictions feed the polar plots in `results/images/` and the
per-V_rest metric grid in `results/metrics.json`, providing the stochastic counterpart to the
deterministic t0022 baseline in the same task.

</details>
