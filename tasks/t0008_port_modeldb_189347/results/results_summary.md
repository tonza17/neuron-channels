# Results Summary: Port ModelDB 189347 DSGC and Hunt Sibling Models

## Summary

Ported ModelDB 189347 (Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC compartmental model) as a
registered library asset, compiled its six MOD files cleanly on NEURON 8.2.7, and ran a canonical
12-angle x 20-trial (240 total) drifting-bar tuning-curve sweep using the t0012 `tuning_curve_loss`
scoring library. The port is **technically faithful** — all MOD files compile, the morphology-swap
report confirms section-count and surface-area parity, and every trial completes end-to-end on the
local Windows workstation — but it does **not** reproduce the project envelope (DSI **0.316** vs
target 0.70-0.85; peak **18.1 Hz** vs 40-80 Hz). The gap is a protocol mismatch, not a port bug:
Poleg-Polsky 2016 implements direction selectivity via a per-angle `gabaMOD` parameter swap, whereas
this task applied a spatial-rotation proxy. Follow-up captured in `S-0008-02`. Phase B completed as
a desk survey ranking Hanson 2019 as the highest-priority sibling port.

## Metrics

* **DSI (direction-selectivity index)**: **0.316** (target 0.70-0.85) - **FAIL**
* **Peak firing rate**: **18.1 Hz** (target 40-80 Hz) - **FAIL**
* **Null firing rate**: **9.4 Hz** (target <10 Hz) - **PASS**
* **HWHM (half-width at half-maximum)**: **82.81 deg** (target 60-90 deg) - **PASS**
* **Reliability (trial-to-trial)**: **0.991** (target >0.9) - **PASS**
* **RMSE vs target curve**: **13.73 Hz** (diagnostic only, no envelope target)
* **Envelope axes passing**: **2 of 4** (null + HWHM pass; DSI + peak fail)
* **Assets produced**: 1 library, 1 answer, 1 tuning-curve CSV (240 rows), 1 morphology-swap report,
  1 Phase B survey CSV

## Verification

* `verify_library_asset.py` on `modeldb_189347_dsgc` - **PASSED** (0 errors, 0 warnings)
* `verify_answer_asset.py` on `dsgc-modeldb-port-reproduction-report` - **PASSED** (0 errors, 0
  warnings)
* `verify_task_metrics.py` (implicit via spec) - all four registered metric keys populated with
  floats
* Tuning-curve schema check - **PASSED** (240 rows, canonical
  `(angle_deg, trial_seed, firing_rate_hz)` columns, 12 angles x 20 trials)
* Scoring-library identity gate (`score(TARGET_MEAN_CSV).loss_scalar == 0.0`) - **PASSED**
* Smoke test (single-angle preferred-direction firing) - **PASSED** (non-zero rate at angle 0 deg)
