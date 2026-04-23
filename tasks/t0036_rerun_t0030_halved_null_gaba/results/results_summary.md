---
spec_version: "2"
task_id: "t0036_rerun_t0030_halved_null_gaba"
date_completed: "2026-04-23"
status: "complete"
---
# Results Summary: Rerun Distal-Diameter Sweep on t0022 with Halved Null-GABA

## Summary

Reran the t0030 distal-diameter sweep on t0022 with `GABA_CONDUCTANCE_NULL_NS = 6.0 nS` (halved from
12 nS, matching Schachter2010's compound null inhibition). **The halving was INSUFFICIENT to unpin
null firing**: mean null-direction firing remained exactly **0.0 Hz at every diameter multiplier**,
primary DSI stayed pinned at 1.000, and the classification label is **`flat_partial`**
(pre-condition gate failed). Vector-sum DSI range 0.579-0.590 (range 0.011, p=0.019 — statistically
significant but practically negligible). The GABA- reduction rescue hypothesis from S-0030-01 is
falsified at 6 nS; follow-up queued to try further reductions (4/2/1 nS) or switch to Poisson-noise
rescue.

## Metrics

* **Null-direction firing (critical diagnostic)**: **0.00 Hz** at every diameter — pre- condition
  failed (threshold 0.1 Hz). Same as t0030 baseline.
* **Primary DSI (peak-minus-null)**: pinned at **1.000** across all 7 diameters.
* **Vector-sum DSI range**: **0.579** (0.50×) to **0.590** (1.75×) — 0.011 absolute range, slope
  0.0049 per log2(multiplier), p=0.019.
* **Preferred-direction peak firing rate**: **15.0 Hz** at 0.50-1.00×, **14.0 Hz** at 1.25-1.50×,
  **13.0 Hz** at 1.75-2.00× — same monotone decline with thickening as t0030.
* **HWHM**: narrower at thin diameters (59-66°), broader at thick (105-120°).
* **Slope classification**: `flat_partial` (mechanism ambiguous; pre-condition failed).
* **Total trials executed**: **840** (7 diameters × 12 directions × 10 trials).
* **Sweep wall time**: approximately **30 minutes** on local Windows CPU — faster than t0030's 115
  min because the `trial_runner` path was optimised during t0034/t0035 rewrites.

## Verification

* `verify_task_file.py` — target 0 errors.
* `verify_task_dependencies.py` — PASSED on step 2 (t0022 and t0030 completed).
* `verify_research_code.py` — PASSED on step 6 (0 errors, 0 warnings).
* `verify_plan.py` — PASSED on step 7 (0 errors, 0 warnings).
* `verify_task_metrics.py` — target 0 errors.
* `verify_task_results.py` — target 0 errors.
* `verify_task_folder.py` — target 0 errors.
* `verify_logs.py` — target 0 errors.
* `ruff check --fix`, `ruff format`, `mypy -p tasks.t0036_rerun_t0030_halved_null_gaba.code` — all
  clean (11 files).
* **Pre-condition gate**: **FAILED** (null_hz at 1.0× = 0.0; threshold 0.1). Classification label
  carries `_partial` suffix; auto-recommendation printed.
