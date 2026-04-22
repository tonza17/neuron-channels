# Results Summary: Distal-Dendrite Length Sweep on t0022 DSGC

## Summary

Swept distal-dendrite length on the t0022 DSGC testbed across seven multipliers (**0.5×, 0.75×,
1.0×, 1.25×, 1.5×, 1.75×, 2.0×**) of baseline `sec.L` while holding the rest of the testbed
fixed — **840 trials** across **12 directions × 10 trials × 7 lengths** in **~42 min** wall time
on the local Windows workstation. **DSI (preferred/null definition) pins at 1.000 at every
multiplier**, so the experiment cannot discriminate Dan2018 passive-transfer-resistance weighting
from Sivyer2013 dendritic-spike branch independence on the DSI axis. Secondary metrics (vector-sum
DSI, peak firing rate, HWHM) move only weakly or non-monotonically.

## Metrics

* **DSI (preferred/null)**: **1.000** at every multiplier (range = **0.000**)
* **Vector-sum DSI**: **0.664** at 0.5× → **0.643** at 2.0× (weak monotonic decrease,
  **−0.021** across the sweep)
* **Peak firing rate**: **15 Hz** at L ≤ 1.00× → **14 Hz** at L ≥ 1.25× (single-Hz step)
* **Null firing rate**: **0 Hz** at every multiplier
* **HWHM**: oscillates **71.7°–116.2°**, non-monotonic
* **Reliability**: **1.000** at every multiplier (deterministic driver)
* **Curve-shape classification**: `saturating` at multiplier **0.5×**, plateau DSI = **1.000**
* **Total wall time**: 2,541 s (≈ 42 min); **total cost**: **$0.00**

## Verification

* `verify_task_dependencies.py` — PASSED (0 errors) at `check-deps`
* `verify_research_code.py` — PASSED (0 errors, 0 warnings) at `research-code`
* `verify_plan.py` — PASSED (0 errors, 0 warnings) at `planning`
* `verify_task_metrics.py` — to be run in the `reporting` step; `metrics.json` is in explicit
  multi-variant format, 7 variants, registered keys only (DSI, HWHM, reliability)
* `verify_task_results.py` — to be run in the `reporting` step; all required files present
* `ruff check --fix . && ruff format . && mypy -p tasks.t0029_distal_dendrite_length_sweep_dsgc.code`
  — all clean (no issues)
