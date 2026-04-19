# Results Summary: Generate Canonical Target Tuning Curve

## Summary

Synthesised the canonical direction tuning curve `target-tuning-curve` from a closed-form
half-wave-rectified cosine raised to power `n = 2` with `θ_pref = 90°`, `r_base = 2 Hz`,
`r_peak = 32 Hz`, and 20 Gaussian-noise trials per angle (`σ = 3 Hz`, seed `42`). The asset is
registered under `assets/dataset/target-tuning-curve/` with explicit generator parameters and a
diagnostic plot.

## Metrics

* **Direction Selectivity Index (DSI)**: **0.8824** — inside the required [0.6, 0.9] band
* **Tuning curve HWHM**: **68.5°** — computed from the closed-form curve
* **Sampled directions**: **12** angles at 30° spacing (0° to 330°)
* **Trials per direction**: **20** (240 rows total in `curve_trials.csv`)
* **Mean absolute bias (sample vs closed form)**: **0.419 Hz** (max 1.063 Hz)

## Verification

* `verify_task_folder.py` — PASSED (0 errors, 1 warning FD-W002 on empty `logs/searches/`)
* `verify_task_dependencies.py` — PASSED (0 errors, 0 warnings; no dependencies)
* `verify_plan.py` — PASSED (0 errors, 0 warnings)
* `verify_task_metrics.py` — to be run in the reporting step together with `verify_task_results`
* `verify_dataset_asset.py` — **not available** in this repository; the dataset asset structure is
  checked by `verify_task_folder` and re-checked by `verify_pr_premerge` at merge time
