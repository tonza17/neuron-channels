---
spec_version: "2"
task_id: "t0034_distal_dendrite_length_sweep_t0024"
date_completed: "2026-04-23"
status: "complete"
---
# Results Summary: Distal-Dendrite Length Sweep on t0024 DSGC

## Summary

Swept distal-dendrite length across seven multipliers (0.5×, 0.75×, 1.0×, 1.25×, 1.5×, 1.75×, 2.0×
baseline) on the t0024 de Rosenroll DSGC port under the standard 12-direction × 10-trial moving-bar
protocol (840 trials total). **Unlike t0029's null result on t0022, primary DSI varies measurably on
t0024** (range 0.545-0.774) because AR(2) stochastic release produces non-zero null firing. The
slope is **-0.1259 per unit multiplier (p=0.038)** — a statistically significant **negative** trend,
classified as **non_monotonic** overall. Neither Dan2018 (predicted monotonic increase) nor
Sivyer2013 (predicted saturating plateau) is supported; the data leans toward passive cable
filtering past an optimal electrotonic length, with superimposed local-spike-failure transitions at
1.5× and 2.0×.

## Metrics

* **Primary DSI range**: **0.545** (2.0×) to **0.774** (0.75×) — 0.229 absolute range, slope
  **-0.1259 per unit multiplier**, **p=0.038** (statistically significant, non-monotonic).
* **Vector-sum DSI range**: **0.357** (2.0×) to **0.507** (0.5×) — cleaner monotonic decline
  (R²=0.91), fully consistent with cable-filtering dominance.
* **Preferred-direction peak firing rate**: **5.70 Hz** at 0.5× → **3.40 Hz** at 2.0× — monotone
  decline of 40% across the 4× length sweep, signature of low-pass cable filtering.
* **Null-direction firing rate**: **0.70-1.00 Hz** across all lengths (never zero, unlike t0022's
  pinned 0 Hz — this is the critical t0024 advantage).
* **HWHM**: **62.7°-76.2°** across lengths — AR(2) noise smooths tuning as expected.
* **Preferred-direction angle**: stable at **0°** for 0.5×-1.25×, jumps to **330°** at 1.5× and
  **30°** at 2.0× — local-spike-failure fingerprint.
* **Slope classification**: **non_monotonic**, vector-sum DSI also non_monotonic with clean negative
  trend.
* **Total trials executed**: **840** (7 lengths × 12 directions × 10 trials).
* **Sweep wall time**: approximately **3 hours** end-to-end on local Windows CPU.

## Verification

* `verify_task_file.py` — target 0 errors on final pass.
* `verify_task_dependencies.py` — PASSED on step 2 (t0024 and t0029 dependencies completed).
* `verify_research_code.py` — PASSED on step 6 (0 errors, 0 warnings).
* `verify_plan.py` — PASSED on step 7 (0 errors, 0 warnings).
* `verify_task_metrics.py` — target 0 errors.
* `verify_task_results.py` — target 0 errors on final pass.
* `verify_task_folder.py` — target 0 errors on final pass.
* `verify_logs.py` — target 0 errors on final pass.
* `ruff check --fix`, `ruff format`, and
  `mypy -p tasks.t0034_distal_dendrite_length_sweep_t0024.code` — all clean (11 files).
