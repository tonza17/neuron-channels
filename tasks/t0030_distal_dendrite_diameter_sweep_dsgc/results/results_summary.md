---
spec_version: "2"
task_id: "t0030_distal_dendrite_diameter_sweep_dsgc"
date_completed: "2026-04-22"
status: "complete"
---
# Results Summary: Distal-Dendrite Diameter Sweep on t0022 DSGC

## Summary

Swept distal-dendrite diameter across seven multipliers (0.5×, 0.75×, 1.0×, 1.25×, 1.5×, 1.75×, 2.0×
baseline) on the t0022 DSGC testbed under the standard 12-direction × 10-trial protocol (840 trials
total). **Vector-sum DSI is essentially flat** across the 4× diameter range: slope 0.0083 per
log2(multiplier), p=0.1773, DSI range 0.635-0.665 across extremes. **Neither the Schachter2010
active-dendrite amplification prediction (positive slope) nor the passive-filtering prediction
(negative slope) is supported** — the t0022 testbed's E-I timing carries DSI almost entirely,
leaving distal diameter with no measurable mechanistic role.

## Metrics

* **Vector-sum DSI range**: **0.635** (0.5×) to **0.665** (1.5×) — 0.030 absolute range across the
  4× diameter sweep; slope not distinguishable from zero (p=0.1773).
* **Primary DSI (peak-minus-null)**: pinned at **1.000** across every diameter — same plateau as
  t0029 length sweep, because null-direction firing is 0 Hz under the t0022 E-I schedule.
* **Preferred-direction peak firing rate**: **15 Hz** at 0.5×-1.0×, **14 Hz** at 1.25×-1.5×, **13
  Hz** at 1.75×-2.0× — mild decline with thickening, consistent with reduced distal input impedance.
* **HWHM**: 84.2° at 0.5×, broadening to 116.2° at 0.75×-1.0×, narrowing to 78.3° at 1.75×; no
  monotonic trend.
* **Peak distal membrane voltage**: approximately **-5 mV** across all diameters — distal spike
  thresholds are cleared everywhere, so thickening-driven impedance changes do not break the
  existing amplification regime.
* **Slope classification**: **flat** (mechanism_label="flat", slope=0.0083, p=0.1773,
  dsi_range_extremes=0.0124, used_fallback=True).
* **Total trials executed**: **840** (7 diameters × 12 directions × 10 trials).
* **Sweep wall time**: approximately **115 min** end-to-end on local Windows CPU; thinner diameters
  ran slowest (raised axial resistance shrinks the NEURON integration timestep).

## Verification

* `verify_task_file.py` — target 0 errors on final pass.
* `verify_task_dependencies.py` — PASSED on step 2 (t0022 dependency completed).
* `verify_research_code.py` — PASSED on step 6 (0 errors, 0 warnings).
* `verify_plan.py` — PASSED on step 7 (0 errors, 0 warnings).
* `verify_task_metrics.py` — target 0 errors.
* `verify_task_results.py` — target 0 errors on final pass.
* `verify_task_folder.py` — target 0 errors on final pass.
* `verify_logs.py` — target 0 errors on final pass.
* `ruff check --fix`, `ruff format`, and
  `mypy -p tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code` — all clean (10 files).
