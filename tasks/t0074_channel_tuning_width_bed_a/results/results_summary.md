---
spec_version: "2"
task_id: "t0074_channel_tuning_width_bed_a"
date_completed: "2026-05-02"
status: "complete"
---
# Results Summary: Channel Tuning-Width Sweep on Bed A

## Summary

Across 25 conditions (1 baseline + 8 channels × 3 densities) × 12 angles × 5 seeds = 1500 FULL +
600 passive = 2100 trials, **NaP_high collapses vector-sum DSI from 0.193 to 0.050** (legacy
DSI_PD-ND from 0.308 to 0.008) and produces the highest peak rate in the sweep (74.2 Hz vs 17.4 Hz
baseline); **SK_high cuts HWHM in half** (83.5 deg → 41.1 deg) while suppressing peak rate; **Kv3,
Kv4, and Kv7 are inert at all three densities tested** (no condition trips the |delta_HWHM| > 5 deg
or |delta_vec_DSI| > 0.05 thresholds). All 2100 trials completed with zero instability flags.

## Metrics

* **Baseline (no extra channels)**: vector-sum DSI = **0.193**, legacy DSI_PD-ND = **0.308**, peak
  rate = **17.4 Hz**, HWHM = **83.5 deg**, RMSE vs t0004 cosine target = **13.83 Hz**.
* **Strongest DSI suppressor**: NaP_high — vector-sum DSI = **0.050** (delta = **-0.143**), legacy
  DSI = **0.008**, peak rate = **74.2 Hz**, HWHM = **49.1 deg**.
* **Strongest HWHM narrower**: SK_high — HWHM = **41.1 deg** (delta = **-42.4 deg**), vector-sum
  DSI = **0.124**, peak rate = **15.6 Hz**.
* **Strongest HWHM broadener**: NaR_med — HWHM = **120.0 deg** (delta = **+36.5 deg**), but no
  change in vector-sum DSI (**0.197** vs baseline 0.193).
* **Strongest peak-rate amplifier**: Nav1.6_high — peak rate = **66.2 Hz** (delta = **+48.8 Hz**)
  with minimal change to vector-sum DSI (0.199).
* **Inert channels at every density tested**: **Kv3, Kv4, Kv7** (3 of 8 channels). The remaining 5
  channels (Nav1.6, NaP, NaR, BK, SK) all produce a measurable change at >= 1 density, satisfying
  the task's pass criterion.

## Verification

* `verify_task_metrics.py`: **PASSED** — 0 errors, 0 warnings (after `density_mS_cm2` →
  `density_ms_cm2` snake-case fix).
* `verify_plan.py`: passed at planning-step completion.
* All 2100 trials completed with `is_unstable = False` (peak Vm in [-80, +60] mV at every trial).
* Stage-2 regression gate passed exactly: measured DSI = 0.7974683544303798 (delta = 0.0, tolerance
  1e-3) under the no-cad code path that exactly reproduces the t0067 baseline fingerprint.
* `results/metrics.json` populated with 25 explicit-format variants, each containing the four
  registered metric keys (`direction_selectivity_index`, `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, `tuning_curve_rmse`).
* `results/metrics_summary.csv` populated with 25 rows × 17 columns; HWHM has no nulls (every
  condition exceeded 1-Hz peak rate).
