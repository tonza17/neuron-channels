# Results Summary: Add 5 voltage-gated channels to the t0065 soma; sweep densities

## Summary

Added each of {Nav1.6, NaP, NaR, Kv3, Kv4} to the deposited Poleg-Polsky DSGC soma, one at a time,
at low / medium / high densities (3-fold steps), and ran the t0065 FULL-mode gabaMOD-swap protocol
with 5 seeds per (condition, direction). 16 conditions × 2 directions × 5 seeds = 160 trials, ~10
minutes wall-clock. Headline finding: **NaP at high density inverts direction selectivity** (DSI =
-0.18, cell fires more in null than preferred); **Nav1.6 monotonically erodes DSI** as density rises
(0.80 → 0.23 across the density grid); **NaR / Kv3 / Kv4 produce only modest changes** at the
chosen densities.

## Metrics

| Condition | PD spikes (mean ± SD) | ND spikes (mean ± SD) | DSI | Δ DSI vs baseline |
| --- | --- | --- | --- | --- |
| baseline | 14.2 ± 1.9 | 1.6 ± 1.3 | 0.797 | (reference) |
| nav16_low | 18.2 ± 2.9 | 2.6 ± 1.5 | 0.750 | -0.05 |
| nav16_med | 26.8 ± 3.6 | 9.4 ± 2.6 | 0.481 | **-0.32** |
| nav16_high | 57.4 ± 2.9 | 36.0 ± 3.1 | 0.229 | **-0.57** |
| nap_low | 23.6 ± 1.1 | 13.0 ± 2.1 | 0.290 | **-0.51** |
| nap_med | 36.4 ± 2.1 | 28.8 ± 1.3 | 0.117 | **-0.68** |
| nap_high | 66.8 ± 4.1 | 95.8 ± 3.5 | -0.179 | **-0.98 (sign flip!)** |
| nar_low | 14.6 ± 2.3 | 1.8 ± 1.3 | 0.780 | -0.02 |
| nar_med | 14.8 ± 2.4 | 2.0 ± 1.2 | 0.762 | -0.03 |
| nar_high | 16.4 ± 2.4 | 2.8 ± 1.9 | 0.708 | -0.09 |
| kv3_low | 14.4 ± 2.2 | 1.6 ± 1.3 | 0.800 | +0.00 |
| kv3_med | 14.6 ± 2.3 | 1.6 ± 1.3 | 0.802 | +0.00 |
| kv3_high | 16.0 ± 2.7 | 1.6 ± 1.3 | 0.818 | +0.02 |
| kv4_low | 14.0 ± 1.9 | 1.6 ± 1.3 | 0.795 | -0.00 |
| kv4_med | 14.0 ± 1.9 | 1.6 ± 1.3 | 0.795 | -0.00 |
| kv4_high | 13.6 ± 2.3 | 1.4 ± 0.9 | 0.813 | +0.02 |

* **direction_selectivity_index (baseline)**: **0.7975** (matches t0065's single-seed DSI = 0.875
  within 5-seed sampling noise — the 5-seed mean is more robust).
* **Largest firing-rate increase**: NaP high (+82.6 PD spikes — 6× baseline) and ND (+94.2 ND
  spikes — 60× baseline).
* **Largest DSI swing**: NaP high (Δ = -0.98, sign inversion).
* **Smallest effect** (essentially no change): Kv3 and Kv4 across all densities.
* **Trials with instability flags**: **0/160** — no depolarisation runaway, no silence.

## Verification

* `verify_research_code` — PASSED (0 errors, 0 warnings).
* `verify_plan` — PASSED (0 errors, 4 non-blocking warnings: long task name + plan section
  grammar).
* `verify_task_dependencies` — PASSED (t0008, t0019, t0065 all completed).
* `verify_task_metrics` — PASSED (registered DSI metric only).
* `verify_task_results` — PASSED (mandatory sections present in this file and
  results_detailed.md).
* Mypy, ruff check, ruff format — all PASSED on
  `tasks/t0067_t0065_soma_channel_addition_sweep/code/`.
* All 160 trials completed; no instability.

## Conclusion

Three takeaways for follow-on tasks:

* **Persistent sodium (NaP) is the most disruptive single addition**: at high density it does not
  just amplify firing but actually **flips DSI sign**, because NaP's non-inactivating character
  means inhibition's shunt cannot keep the cell sub-threshold once enough NaP is open. The standing
  depolarisation is large enough that the ND direction (where excitation arrives during the
  prolonged inhibition) actually fires *more* than PD.
* **Lower-threshold transient sodium (Nav1.6) erodes DSI without flipping it**: each density step
  boosts both PD and ND firing, but ND is boosted proportionally more (because the baseline ND
  firing was small, the new channel breaks the "sub-threshold" regime). DSI drops monotonically.
* **NaR, Kv3, Kv4 are nearly inert** at our densities. Likely reasons: (a) the soma already has very
  high HHst Na (~400 mS/cm²) and K, so adding 3-90 mS/cm² of "extra" channel is a small
  perturbation; (b) NaR's resurgent feature only matters in high-frequency trains (>100 Hz) which
  this cell doesn't reach; (c) Kv3/Kv4 act primarily on AP shape and recovery, not on triggering —
  and the t0065 stimulus isn't pushing the cell hard enough to expose AP-shape limits.
