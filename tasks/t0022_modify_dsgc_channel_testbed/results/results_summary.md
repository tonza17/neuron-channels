# Results Summary: Modify DSGC Port with Spatially-Asymmetric Inhibition for Channel Testbed

## Summary

Built the `modeldb_189347_dsgc_dendritic` library asset, a sibling to the t0008 rotation-proxy and
t0020 gabaMOD-swap ports of Poleg-Polsky & Diamond 2016. Direction selectivity now arises from
per-dendrite E-I temporal scheduling (E leads I by **+10 ms** in the preferred half-plane; I leads E
by **10 ms** in the null half-plane) on top of a channel-modular AIS partitioned into five `forsec`
regions (`SOMA_CHANNELS`, `DEND_CHANNELS`, `AIS_PROXIMAL`, `AIS_DISTAL`, `THIN_AXON`). The canonical
12-angle x 10-trial sweep (120 rows) yields **DSI 1.0**, **peak 15 Hz** at 120 deg, and **null 0
Hz** across 150-300 deg, clearing both acceptance gates (DSI >= 0.5 and peak >= 10 Hz).

## Metrics

* **Direction Selectivity Index**: **1.0** (gate >= 0.5 — pass; up from 0.316 in t0008 and 0.7838
  in t0020)
* **Peak firing rate**: **15 Hz** at 120 deg (gate >= 10 Hz — pass)
* **Null firing rate**: **0 Hz** (150-300 deg half-plane completely silenced by early inhibition)
* **HWHM**: **116.25 deg** (broader than t0008's 82.81 deg — the 120-deg lit half-plane covers 5
  of 12 angles)
* **Tuning-curve reliability**: **1.0** (zero trial-to-trial std at every angle; deterministic
  driver)
* **RMSE vs t0004 target**: **10.48 Hz** (t0008: 13.73 Hz; dendritic driver is closer to target
  shape despite the 17 Hz peak gap)

## Verification

* `verify_task_file.py` — PASSED at init-folders (0 errors, 0 warnings)
* `verify_task_dependencies.py` — PASSED (all 7 dependency tasks completed)
* `verify_task_metrics.py` — PASSED (all 4 keys registered in `meta/metrics/` and non-null)
* `verify_task_results.py` — to be run in Step 15 (reporting); structure manually confirmed
  against `task_results_specification.md` v8
* **Acceptance envelope (REQ-4)** — PASSED: DSI 1.0 >= 0.5 and peak 15 Hz >= 10 Hz
* **CSV schema (REQ-2)** — PASSED: 120 rows with columns `angle_deg,trial_seed,firing_rate_hz`
* **Library asset** — structural check PASSED manually against
  `meta/asset_types/library/specification.md` (no `verify_library_asset.py` script exists; flagged
  as a framework gap in the implementation step log)
* **Lint / type** — `ruff check --fix`, `ruff format`, `mypy .` all clean across the full tree
