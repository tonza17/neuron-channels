---
spec_version: "1"
task_id: "t0068_t0067_nav16_kv3_coexpression_rescue"
date_completed: "2026-05-01"
status: "complete"
---
# Plan: Nav1.6 + Kv3 co-expression rescue test

## Objective

Test whether co-inserting Kv3 with Nav1.6 on the deposited Poleg-Polsky soma rescues the direction
selectivity that Nav1.6 alone erodes (t0067 anchors: DSI = 0.48 at Nav1.6_med, 0.23 at Nav1.6_high;
baseline DSI = 0.80).

## Approach

1. Vendor 5 MOD files from t0067 (copy verbatim to `code/mods/`).
2. Compile task-local DLL.
3. Build cell once via t0008. Insert all 5 mechanisms with gbar=0; per-trial set Nav1.6 and Kv3
   gbars to their target densities.
4. Run 90 FULL-mode trials (9 conditions × 2 directions × 5 seeds).

## Cost Estimation

* Local Windows. ~3 s/trial × 90 = ~5 min.
* External costs: $0.

## Step by Step

1. `code/paths.py`, `code/constants.py` — task-local constants + 9-condition schema.
2. `code/mods/{nav16t67,napt67,nart67,kv3t67,kv4t67}.mod` — copied from t0067.
3. Build DLL via run_nrnivmodl.cmd → `code/build/nrnmech.dll`.
4. `code/run_sweep.py` — trial driver with multi-channel `_set_active_channels`.
5. `code/plot_results.py` — 2 PNGs (DSI rescue curve, firing-rate rescue).

All scripts wrapped in `arf.scripts.utils.run_with_logs`.

## Remote Machines

None.

## Assets Needed

* t0008 cell builder + HOC.
* t0067 MOD files (vendored verbatim).
* t0065 / t0067 trial-driver pattern.

## Expected Assets

None.

## Time Estimation

* Implementation: 1 hour.
* Sweep: 5 min.
* Plotting + reporting: 45 min.
* Verification + PR: 30 min.
* Total: ~2.5 hours.

## Risks & Fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Kv3 at high density breaks the cell. | spike_count = 0 in BOTH directions. | Document; no auto-rerun. |
| 2 | Kv3 has no rescue effect. | DSI(co-insert) ≈ DSI(Nav1.6 alone). | Report null result. |
| 3 | Kv3 amplifies DSI loss. | DSI(co-insert) < DSI(Nav1.6 alone). | Document and explore. |

## Verification Criteria

* All 90 trials complete.
* per_trial_metrics.json has 90 entries; dsi_by_condition.json has 9.
* 2 PNGs exist and embedded in results_detailed.md.
* All standard verificators pass.

## Task Requirement Checklist

* **REQ-1 (5 MOD files vendored from t0067)**: copied to `code/mods/`.
* **REQ-2 (9 conditions per task description)**: encoded in constants.py.
* **REQ-3 (FULL mode only, gabaMOD-swap)**: only exptype=1; PD=0.33, ND=0.99.
* **REQ-4 (5 seeds per condition)**: SEED_BASE + 0..4.
* **REQ-5 (DSI per condition)**: computed in `_summarise_by_condition`.
* **REQ-6 (2 plots)**: dsi_rescue_curve.png + firing_rate_rescue.png.
* **REQ-7 (results_summary.md + results_detailed.md spec_version 2)**: written in results step.
