---
spec_version: "1"
task_id: "t0067_t0065_soma_channel_addition_sweep"
date_completed: "2026-05-01"
status: "complete"
---
# Plan: Add 5 voltage-gated channels to the t0065 soma; sweep densities

## Objective

Systematically test how adding each of {Nav1.6, NaP, NaR, Kv3, Kv4} on the deposited Poleg-Polsky
DSGC soma at low/medium/high densities changes (a) FULL-mode firing rate and (b) DSI relative to
t0065 baseline.

## Approach

1. Vendor 5 minimal MOD files into `code/mods/` with NONSPECIFIC_CURRENT pattern (avoids ion
   accumulation conflicts with the existing HHst mechanism).
2. Compile a task-local DLL containing only the 5 new mechanisms.
3. Build the t0008 cell once; load t0008 DLL via the cell builder; load t0067 DLL on top.
4. Insert all 5 new mechanisms on the soma with `gbar = 0`; per-trial set the active one's gbar to
   the target density and zero the others.
5. Run 160 FULL-mode trials (16 conditions × 2 directions × 5 seeds) using the t0065 gabaMOD-swap
   protocol.
6. Aggregate per-trial scalars to per-condition mean ± SD; compute DSI per condition.

## Cost Estimation

* Local Windows workstation. ~3 s/trial × 160 trials ≈ 8 min compute.
* External costs: $0.

## Step by Step

1. `code/paths.py` — Path constants.
2. `code/constants.py` — `ChannelKind`, `DensityLabel`, `Direction` enums; `CHANNEL_DEFS` tuple
   with per-channel densities; gabaMOD constants; instability thresholds.
3. `code/mods/{nav16t67,napt67,nart67,kv3t67,kv4t67}.mod` — 5 NEURON mechanism source files.
4. Build DLL via `run_nrnivmodl.cmd` → `code/build/nrnmech.dll`.
5. `code/run_sweep.py` — load both DLLs, build cell, insert mechanisms, loop trials.
6. `code/plot_results.py` — read `dsi_by_condition.json`, emit 3 PNGs.

All script invocations on the task branch must run via `arf.scripts.utils.run_with_logs`.

## Remote Machines

None. Local Windows workstation only.

## Assets Needed

* `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/` — HOC template + MOD
  sources.
* `tasks/t0008_port_modeldb_189347/code/build_cell.py` + `apply_params` — cell builder.
* `tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/...` — kinetic priors.
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py` — trial driver template.

## Expected Assets

None. Outputs are JSON, PNG, markdown — no new datasets/models/predictions/papers/libraries.

## Time Estimation

* Implementation (paths, constants, MODs, recompile, run_sweep, plot_results): 2 hours.
* Sweep run: 8 min.
* Plotting + reporting: 1 hour.
* Verification + PR: 30 min.
* Total: ~3.5 hours.

## Risks & Fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | New MOD files incompatible with deposited MOD set (USEION conflicts). | nrnivmodl fails or nrn_load_dll errors. | Use NONSPECIFIC_CURRENT pattern (already chosen — see research_code.md § 5). |
| 2 | Channel at high density makes cell unstable (depolarisation block, no spikes). | failure-mode policy: peak Vm > +60 mV, < -80 mV, or 0 spikes in BOTH directions. | Save trial data, flag as unstable, no auto-rerun. |
| 3 | New channel not affecting Vm because density too low (gbar too small). | All 3 densities give same firing as baseline. | Document the insensitivity in results. |
| 4 | The deposited cell has no AIS — somatic insertion of channels typically AIS-localised in real RGCs. | Results may diverge from in-vivo intuition. | Document limitation. |

## Verification Criteria

* All 160 trials complete.
* `data/per_trial_metrics.json` has 160 entries.
* `data/dsi_by_condition.json` has 16 entries.
* All 3 PNG plots exist and are embedded in `results_detailed.md`.
* `verify_logs`, `verify_research_code`, `verify_plan`, `verify_task_results`,
  `verify_task_metrics`, `verify_suggestions`, `verify_pr_premerge` all pass.

## Task Requirement Checklist

* **REQ-1 (5 channels added: Nav1.6, NaP, NaR, Kv3, Kv4)**: 5 MOD files vendored + compiled.
* **REQ-2 (3 densities per channel: low/med/high; factor ~3 between)**: encoded in CHANNEL_DEFS.
* **REQ-3 (one channel per experiment, isolation)**: per-trial only one channel has nonzero gbar;
  others zeroed.
* **REQ-4 (FULL mode only — passive identical across conditions by construction)**: only exptype=1
  used; passive trials skipped.
* **REQ-5 (PD and ND directions, gabaMOD-swap protocol)**: PD = 0.33, ND = 0.99.
* **REQ-6 (5 seeds per condition)**: SEED_BASE + 0..4.
* **REQ-7 (firing rate + DSI per condition)**: spike count per trial → mean ± SD per (condition,
  direction); DSI = (PD − ND) / (PD + ND).
* **REQ-8 (failure-mode flagging)**: peak > +60 mV or < −80 mV → `is_unstable = true`.
* **REQ-9 (3 plots: firing-rate-vs-density, DSI-vs-density, spike-count heatmap)**: emitted by
  `plot_results.py`.
* **REQ-10 (results_summary.md + results_detailed.md spec_version 2 with embedded plots)**: written
  in results step.
