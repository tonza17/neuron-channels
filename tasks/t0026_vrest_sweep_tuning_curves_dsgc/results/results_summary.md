# Results Summary: V_rest sweep tuning curves for t0022 and t0024 DSGC ports

## Summary

Swept resting potential across eight values (**-90 mV to -20 mV in 10 mV steps**) for two DSGC
compartmental models under the standard 12-direction moving-bar protocol. Model t0022 (deterministic
ModelDB 189347 port) ran **96 trials** (~6.0 min wall time); model t0024 (de Rosenroll 2026 port
with AR(2)-correlated stochastic release at rho=0.6) ran **960 trials** (~3.21 h wall time). Both
models show strong V_rest dependence but with qualitatively different shapes: t0022 peaks DSI
sharply at V_rest=-60 mV, while t0024 is U-shaped with maxima at the extremes.

## Metrics

* **t0022 DSI range**: **0.046** (V=-30 mV) to **0.6555** (V=-60 mV) — 14x modulation
* **t0024 DSI range**: **0.3606** (V=-20 mV) to **0.6746** (V=-90 mV) — 1.9x modulation, U-shaped
* **t0022 peak firing rate**: **6 Hz** at V=-90 mV, monotone up to **129 Hz** at V=-30 mV, collapses
  to **26 Hz** at V=-20 mV (Na inactivation)
* **t0024 peak firing rate**: **1.5 Hz** at V=-90 mV, monotone up to **7.6 Hz** at V=-20 mV (no
  hyper-depolarisation collapse)
* **t0022 HWHM**: 0.77 deg at V≤-80 mV (near-binary curve) vs. 180 deg at V=-30/-40 mV (complete
  loss of tuning)
* **t0024 HWHM**: **65-83 deg** across the full V_rest range — AR(2) noise smooths tuning
* **Total trials executed**: 1,056 (96 + 960) across both models

## Verification

* `verify_logs.py` — PASSED (0 errors) after step 9 implementation commit
* `verify_task_file.py` — PASSED (0 errors) — task.json confirms
  `expected_assets = {"predictions": 2}`
* `verify_implementation.py` — PASSED for both predictions assets (expected PR-W014 model_id null
  \+ PR-W015 dataset_ids empty, both correct)
* Per-model tidy CSV row counts: **96** (t0022) and **960** (t0024), matching REQ-3 and REQ-4
  exactly
* Override unit test `vrest_override_smoke.py` — PASSED: every HHst-bearing and pas-bearing
  section responds to `set_vrest(h, -20.0)`
