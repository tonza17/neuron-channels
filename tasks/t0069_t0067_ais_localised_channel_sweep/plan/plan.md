---
spec_version: "1"
task_id: "t0069_t0067_ais_localised_channel_sweep"
date_completed: "2026-05-01"
status: "complete"
---
# Plan: Add virtual AIS to deposited DSGC and re-run t0067 channel sweep on AIS

## Objective

Test whether AIS-localised insertion of the t0067 channels produces substantially larger effects on
firing rate / DSI than soma-localised insertion. Hypothesis from S-0067-03: AIS is a
high-input-resistance compartment that should amplify per-gbar effects relative to the soma.

## Approach

1. Vendor 5 MOD files from t0067 (copy verbatim).
2. Compile t0069-local DLL.
3. Build the t0008 cell, then append a 30 μm AIS + 1 mm axon (HHst at biologically realistic
   densities).
4. Insert all 5 t0067 mechanisms on the AIS (gbar=0); per-trial set the active one.
5. Run 16 conditions × 2 directions × 5 seeds = 160 FULL trials.

## Cost Estimation

* Local Windows. ~3 s/trial × 160 = ~10 min.
* External costs: $0.

## Step by Step

1. `code/paths.py`, `code/constants.py` — new constants (AIS section properties).
2. `code/mods/{nav16t67,napt67,nart67,kv3t67,kv4t67}.mod` — copied from t0067.
3. `code/extend_with_ais.py` — AIS + axon section construction.
4. `code/run_sweep.py` — trial driver with AIS-localised channel insertion.
5. `code/plot_results.py` — 3 PNGs (firing rate, DSI, soma-vs-AIS comparison).

All scripts wrapped in `arf.scripts.utils.run_with_logs`.

## Remote Machines

None.

## Assets Needed

* t0008 cell builder + HOC.
* t0067 MOD files (vendored verbatim).
* t0019 channel priors.
* t0067 dsi_by_condition.json (read by plot_results for cross-task comparison).

## Expected Assets

None.

## Time Estimation

* Implementation: 1 hour.
* Sweep: 10 min.
* Plotting + reporting: 1 hour.
* Verification + PR: 30 min.
* Total: ~3 hours.

## Risks & Fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | AIS attachment changes t0069 baseline very differently from t0067 baseline. | t0069 baseline DSI < 0.5 or > 1.0; or PD spikes very different. | Expected: AIS adds electrical sink. Document the new baseline; comparisons are ΔDSI from each task's own baseline. |
| 2 | All AIS conditions show same DSI (no effect). | DSI variance < 0.05 across all 15 channel conditions. | Document the null result; the soma is dominant for spike initiation in this cell. |
| 3 | Some channel + density combo destabilises the cell. | peak Vm > +60 or no spikes both directions. | Save trial data, flag, no auto-rerun. |

## Verification Criteria

* All 160 trials complete.
* per_trial_metrics.json has 160 entries; dsi_by_condition.json has 16.
* All 3 PNG plots exist and embedded in results_detailed.md.
* All standard verificators pass.

## Task Requirement Checklist

* **REQ-1 (5 MOD files vendored)**: Done via copy from t0067.
* **REQ-2 (AIS + axon attached after build)**: Done in extend_with_ais.py.
* **REQ-3 (16 conditions: baseline + 5 channels × 3 densities)**: encoded in CHANNEL_DEFS + trial
  enumeration.
* **REQ-4 (channel insertion on AIS only, not soma)**: enforced in `_set_active_channel_on_ais`.
* **REQ-5 (FULL mode only, gabaMOD-swap)**: only exptype=1.
* **REQ-6 (5 seeds per condition)**: SEED_BASE + 0..4.
* **REQ-7 (3 plots: firing rate, DSI, soma-vs-AIS comparison)**: emitted by plot_results.py.
* **REQ-8 (results_summary.md + results_detailed.md spec_version 2)**: written in results step.
* **REQ-9 (cross-task comparison embedded)**: soma_vs_ais_comparison.png.
