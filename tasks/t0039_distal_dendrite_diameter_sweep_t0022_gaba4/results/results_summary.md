---
spec_version: "2"
task_id: "t0039_distal_dendrite_diameter_sweep_t0022_gaba4"
date_completed: "2026-04-24"
status: "complete"
---
# Results Summary: 7-Diameter Sweep on t0022 at GABA=4 nS

## Summary

Rerunning t0030's 7-diameter sweep at the t0037-validated operational GABA level
(`GABA_CONDUCTANCE_NULL_NS = 4.0 nS`) produces the first diameter-vs-DSI measurement on t0022 with a
discriminator that has dynamic range. DSI decreases monotonically from **0.429** at D=0.5x baseline
to **0.368** at D=2.0x, slope=**-0.034** per log2(multiplier), **p=0.008**. Mechanism classified as
**passive_filtering** on t0030's inherited thresholds. The preferred direction stays pinned near
**40°** across the full sweep, confirming the E-I schedule encodes the DS axis; morphology sets the
gain.

## Metrics

* **DSI range**: **0.368 → 0.429** (Δ = **0.061**).
* **Slope**: **-0.0336** per log2(diameter multiplier), **p=0.008**.
* **Mechanism label**: `passive_filtering` (t0030 classifier, threshold criteria met).
* **Preferred direction**: **37-41°** across all 7 diameters (stability = **4°** total range).
* **Null firing rate**: **6 Hz** at every diameter (invariant; set by GABA+schedule).
* **Peak firing rate**: **13-15 Hz** (decreases with diameter).
* **DSI saturation**: D=0.5x and D=0.75x both hit DSI=**0.429** (the 4 nS ceiling from t0037).
* **Total trials executed**: **840** (7 diameters × 12 directions × 10 trials).
* **Sweep wall time**: **~38 min** (2,322 s total across the 7 diameters).
* **Cost**: **$0.00** (local CPU only).

## Verification

* `verify_task_file.py` — target 0 errors.
* `verify_task_dependencies.py` — PASSED (t0022, t0030, t0037 all completed).
* `verify_plan.py` — PASSED.
* `verify_research_code.py` — PASSED.
* `verify_task_results.py` — target 0 errors.
* `verify_task_folder.py` — target 0 errors.
* `verify_logs.py` — target 0 errors.
* `ruff check --fix`, `ruff format`,
  `mypy -p tasks.t0039_distal_dendrite_diameter_sweep_t0022_gaba4.code` — all clean (11 files).
* Preflight gate: **PASSED** (18 trials, firing rates DSGC-like, GABA override confirmed).
