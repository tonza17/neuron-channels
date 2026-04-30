# Add 5 voltage-gated channels to the t0065 soma; sweep densities; measure firing rate and DSI

## Motivation

The deposited Poleg-Polsky 2016 DSGC (used by t0008/t0020/t0065) carries only the Fohlmeister-
Miller `HHst` mechanism for somatic active conductances — one Nav and one Kv compartment-wide.
t0019's voltage-gated-channel literature survey documents that real RGCs co-express multiple Nav
subtypes (Nav1.2, Nav1.6) and multiple Kv families (Kv1, Kv3, Kv4, KCNQ) with distinct kinetics and
localisations. t0043 was scoped to add Nav1.6 + Kv3 to the t0022 channel testbed but was cancelled.
No prior task has measured the per-channel impact on DSGC firing rate and direction selectivity
index (DSI) on the deposited cell.

This task systematically tests, **one channel at a time**, how adding extra Nav and Kv mechanisms to
the soma changes (a) FULL-mode firing rate and (b) DSI, relative to the t0065 baseline (DSI = 0.875,
PD = 15 spikes, ND = 1 spike).

## Scope

* Cell: deposited Poleg-Polsky 2016 ModelDB 189347 DSGC, exactly as built in
  `tasks/t0008_port_modeldb_189347/code/build_cell.py::build_dsgc()`. No changes to dendrites,
  synapses, or the existing `HHst` mechanism on the soma.
* Mode: only `FULL` (HH on, all synapses at canonical defaults). Passive modes (EPSP_PASSIVE,
  IPSP_PASSIVE) are deliberately omitted because they are insensitive to active-channel changes by
  construction (HH off → new mechanisms also produce zero current at rest, traces would match
  t0065 exactly).
* Direction: PD (`gabaMOD = 0.33`) and ND (`gabaMOD = 0.99`), per t0020 / t0065 protocol.
* Seeds per condition: 5 (gives a mean ± SD on spike count and DSI; matches the user-confirmed
  cost-vs-precision tradeoff).
* Channels added (one per experiment): Nav1.6, NaP, NaR, Kv3, Kv4.
* Densities per channel: low / medium / high (factor of ~3 between levels). Medium is the
  literature-default density.

## Channel inventory

| Channel | Reference / MOD source | Low | Medium | High | Units |
| --- | --- | --- | --- | --- | --- |
| Nav1.6 (fast, low-threshold transient) | Carter & Bean 2009 / Khaliq 2003 ModelDB | 10 | 30 | 90 | mS/cm² |
| NaP (persistent sodium) | Magistretti & Alonso 1999 | 0.3 | 0.8 | 2.4 | mS/cm² |
| NaR (resurgent sodium) | Khaliq, Gouwens, Raman 2003 (Purkinje) | 3 | 8 | 24 | mS/cm² |
| Kv3 (fast delayed rectifier) | Erisir, Lau, Rudy, Leonard 1999 | 7 | 20 | 60 | mS/cm² |
| Kv4 / IA (transient A-type) | Hoffman, Magee, Colbert, Johnston 1997 | 4 | 12 | 36 | mS/cm² |

**16 conditions in total**: 1 baseline (HHst-only, no channel added) + 5 channels × 3 densities.
Each runs in PD and ND with 5 seeds = **160 FULL trials**.

## Approach

1. Vendor 5 MOD files (Nav1.6, NaP, NaR, Kv3, Kv4) into the task's `code/sources/` from the
   published model sources (preferred order: ModelDB first, then re-implementation from published
   kinetics if the ModelDB MOD is incompatible with the deposited cell's MOD set).
2. Compile a task-local `nrnmech.dll` that includes the deposited Poleg-Polsky mechanisms PLUS the 5
   new channels.
3. Reuse the t0008 cell builder unchanged. After building, programmatically `insert(<mech>)` the
   single new channel on the soma section and set its peak conductance density.
4. Reuse the t0065 trial driver structure (gabaMOD-swap, FULL mode only) but loop over
   `(channel_kind, density_level, direction, seed)`.
5. For each trial, capture peak Vm, baseline Vm, spike count. No per-sample Vm trace stored to CSV
   (each trial would produce 10001 rows × 160 trials = 1.6M rows, exceeds the 5 MB pre-merge gate).
   Save only per-trial scalars to `data/per_trial_metrics.json`.

## Configurations

| condition_id | channel | density_label | density_mS_cm2 |
| --- | --- | --- | --- |
| baseline | (none) | n/a | 0 |
| nav16_low | Nav1.6 | low | 10 |
| nav16_med | Nav1.6 | med | 30 |
| nav16_high | Nav1.6 | high | 90 |
| nap_low | NaP | low | 0.3 |
| nap_med | NaP | med | 0.8 |
| nap_high | NaP | high | 2.4 |
| nar_low | NaR | low | 3 |
| nar_med | NaR | med | 8 |
| nar_high | NaR | high | 24 |
| kv3_low | Kv3 | low | 7 |
| kv3_med | Kv3 | med | 20 |
| kv3_high | Kv3 | high | 60 |
| kv4_low | Kv4 | low | 4 |
| kv4_med | Kv4 | med | 12 |
| kv4_high | Kv4 | high | 36 |

## Outputs

* `data/per_trial_metrics.json` — list of 160 trial records with `condition_id`, `channel`,
  `density_label`, `direction`, `seed`, `peak_v_mv`, `baseline_v_mv`, `spike_count`, `n_samples`.
* `data/dsi_by_condition.json` — for each of the 16 conditions: PD spike-count mean ± SD, ND
  spike-count mean ± SD, DSI ((PD − ND) / (PD + ND)), PD firing rate (Hz), ND firing rate (Hz).
* `results/metrics.json` — registered project metric `direction_selectivity_index` for the
  baseline condition only (since the metric is per-task, not per-variant in the legacy schema — or
  use the variants format to register one DSI per condition).
* `results/images/firing_rate_vs_density.png` — 5 panels (one per channel), each showing PD and ND
  mean firing rate ± SD across the 3 density levels, with the baseline as a horizontal reference
  line.
* `results/images/dsi_vs_density.png` — 5 panels (one per channel), each showing DSI vs density
  level, baseline as horizontal reference.
* `results/images/spike_count_heatmap.png` — channel × density grid heatmap of mean spike count
  in PD and ND, side by side.
* `results/results_summary.md`, `results/results_detailed.md` (spec_version 2) with per-channel
  narrative findings, instability flagging, and the cross-channel comparison.

## Failure-mode policy

A trial is flagged "unstable" if **either**:

* peak Vm > +60 mV (depolarisation runaway), or
* peak Vm < −80 mV (hyperpolarisation past leak reversal), or
* spike count = 0 in BOTH PD and ND (no spike generation despite full synaptic drive).

Flagged trials are still saved (their data is part of the per_trial_metrics dump), but they are
called out in `results_detailed.md` as "channel + density failed sanity gate". No automatic re-run.

## Key Questions

1. Which channel produces the largest absolute change in FULL-mode firing rate from the t0065
   baseline (15 spikes PD, 1 spike ND)?
2. Which channel produces the largest absolute change in DSI?
3. Are there channel + density combinations that **break** the cell (depolarisation block, silence)?
   Does the failure scale predictably with density?
4. Do Na channels and K channels have opposite signs of effect on firing rate (Na ↑, K ↓), or
   are there exceptions (e.g., Kv3 enabling sustained trains → firing ↑)?
5. Does any channel preferentially affect PD over ND (or vice versa), changing DSI in a non- trivial
   way (i.e., not just scaling both directions equally)?

## Compute and Budget

* Local Windows workstation. Per-trial wall-clock for the deposited Poleg-Polsky cell is ~3 s. 160
  trials × 3 s ≈ **8 minutes**.
* External costs: **$0**.

## Time Estimation

* Implementation (paths, constants, vendor MODs, recompile DLL, run driver): 2 hours (most time on
  sourcing and validating MOD files).
* Sweep run: 8 minutes.
* Plotting + reporting: 1 hour.
* Verification + PR: 30 minutes.
* Total: ~3.5 hours.

## Dependencies

* `t0008_port_modeldb_189347` — provides the cell builder and the existing MOD mechanisms (HHst,
  bipNMDA, SACinhib, SACexc).
* `t0019_literature_survey_voltage_gated_channels` — provides the kinetic priors and references
  for the 5 added channels via answer asset `nav-kv-combinations-for-dsgc-modelling`.
* `t0065_t0020_epsp_ipsp_vm_protocol` — provides the gabaMOD-swap FULL trial driver template,
  baseline DSI = 0.875, baseline PD spike count = 15, baseline ND spike count = 1.

## Risks and Fallbacks

* **Risk 1**: ModelDB MOD files for some channels (especially NaR, Kv3) use NEURON conventions
  incompatible with the deposited Poleg-Polsky MOD set (e.g., SUFFIX collisions, USEION conflicts).
  Detection: `nrnivmodl` fails or `nrn_load_dll` errors. Fallback: re-implement the mechanism from
  published kinetics in a clean MOD file using only NONSPECIFIC_CURRENT (no Ca USEION), matching the
  HHst pattern.
* **Risk 2**: A channel at the high density makes the cell unstable (depolarisation block, no
  spikes). Detection: failure-mode policy above. Fallback: documented in results, no re-run.
* **Risk 3**: The deposited cell has no AIS — somatic insertion of channels typically AIS-
  localised in real RGCs is a simplification. Detection: results may diverge from in-vivo intuition.
  Fallback: document the limitation; this task's purpose is to scan parameter space, not to claim
  biological fidelity.

## Verification Criteria

* All 160 trials complete without raising `_assert_bip_positions_baseline`.
* `data/per_trial_metrics.json` has 160 entries.
* `data/dsi_by_condition.json` has 16 entries.
* All 3 PNG plots exist and are embedded in `results_detailed.md`.
* `verify_logs`, `verify_research_code`, `verify_plan`, `verify_task_results`,
  `verify_task_metrics`, `verify_suggestions`, `verify_pr_premerge` all pass.
