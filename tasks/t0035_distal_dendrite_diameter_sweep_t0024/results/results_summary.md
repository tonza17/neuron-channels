---
spec_version: "2"
task_id: "t0035_distal_dendrite_diameter_sweep_t0024"
date_completed: "2026-04-23"
status: "complete"
---
# Results Summary: Distal-Dendrite Diameter Sweep on t0024 DSGC

## Summary

Swept distal-dendrite diameter across seven multipliers (0.5×-2.0× baseline) on the t0024 de
Rosenroll DSGC port under the standard 12-direction × 10-trial moving-bar protocol (840 trials
total). **DSI-vs-diameter slope is flat** (slope 0.0041 per log2(multiplier), **p=0.8808**, range
across extremes -0.0237). **Neither Schachter2010 (predicted positive slope) nor passive filtering
(predicted negative slope) is supported.** Primary DSI range 0.680-0.808 — measurable (unlike
t0030's pinned 1.000 on t0022) but with no mechanism-driven trend. Contrasts sharply with sibling
t0034 (length sweep on same t0024 port) which showed a statistically significant non-monotonic
negative slope (p=0.038): **length modulates DSI on t0024, diameter does not.**

## Metrics

* **Primary DSI range**: **0.680** (2.0×) to **0.808** (1.5×) — 0.128 absolute range, slope 0.0041
  per log2(multiplier), **p=0.8808** (not distinguishable from zero).
* **Vector-sum DSI range**: **0.417** (2.0×) to **0.463** (0.5×) — 0.046 absolute range, no
  meaningful trend.
* **Preferred-direction peak firing rate**: **4.20 Hz** at 2.0× to **5.40 Hz** at 0.75× / 1.00× —
  mild ~25% variation but not monotonic in either direction.
* **Null-direction firing rate**: **0.50-0.80 Hz** across all diameters (non-zero throughout —
  confirms AR(2) rescue holds on the diameter axis too).
* **HWHM**: **61.4°-77.8°** across diameters.
* **Slope classification**: **flat** (mechanism_class="flat", slope=0.0041, p=0.8808,
  dsi_range_extremes=-0.0237, used_fallback=False).
* **Total trials executed**: **840** (7 diameters × 12 directions × 10 trials).
* **Sweep wall time**: approximately **3 hours** end-to-end on local Windows CPU.
* **Sibling comparison**: t0034 (length sweep) on same t0024 port produced slope -0.1259 (p=0.038);
  t0035 (diameter) produced slope 0.0041 (p=0.88). **Length modulates DSI; diameter does not.**

## Verification

* `verify_task_file.py` — target 0 errors on final pass.
* `verify_task_dependencies.py` — PASSED on step 2 (t0024 and t0030 dependencies completed).
* `verify_research_code.py` — PASSED on step 6 (0 errors, 0 warnings).
* `verify_plan.py` — PASSED on step 7 (0 errors, 0 warnings).
* `verify_task_metrics.py` — target 0 errors.
* `verify_task_results.py` — target 0 errors on final pass.
* `verify_task_folder.py` — target 0 errors on final pass.
* `verify_logs.py` — target 0 errors on final pass.
* `ruff check --fix`, `ruff format`, and
  `mypy -p tasks.t0035_distal_dendrite_diameter_sweep_t0024.code` — all clean (11 files).
