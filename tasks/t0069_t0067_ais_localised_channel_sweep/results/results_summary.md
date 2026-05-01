# Results Summary: Add virtual AIS to deposited DSGC and re-run t0067 channel sweep on AIS

## Summary

Appended a 30 μm AIS + 1 mm passive axon to the deposited Poleg-Polsky DSGC, then re-ran the t0067
channel sweep with each of {Nav1.6, NaP, NaR, Kv3, Kv4} inserted on the AIS instead of the soma at
the same low/med/high densities. 16 conditions × 2 directions × 5 seeds = 160 FULL trials, ~8 min
wall-clock. **Hypothesis S-0067-03 (AIS-localised channels show substantially LARGER DSI effects
than soma-localised) is falsified.** Adding the AIS+axon halved baseline PD firing (14.2 → 6.4
spikes) and silenced ND firing entirely (1.6 → 0.0), pushing baseline DSI from **0.80 → 1.00**.
On this quieter AIS-anchored baseline, **11 of 15 channel conditions produced zero detectable DSI
change**; only NaP (med, high) and Nav1.6 (high) moved DSI at all, and **|ΔDSI| was strictly
smaller on the AIS than on the soma for every channel that had any effect**. The AIS+axon adds a
large electrical sink that quenches the cell rather than relocating spike initiation.

## Metrics

| Condition | PD spikes (mean ± SD) | ND spikes (mean ± SD) | DSI | Δ DSI vs t0069 baseline |
| --- | --- | --- | --- | --- |
| baseline_ais | 6.4 ± 0.5 | 0.0 ± 0.0 | 1.000 | (reference) |
| nav16_low_ais | 6.6 ± 0.5 | 0.0 ± 0.0 | 1.000 | +0.00 |
| nav16_med_ais | 6.8 ± 0.4 | 0.0 ± 0.0 | 1.000 | +0.00 |
| nav16_high_ais | 8.6 ± 0.5 | 0.8 ± 0.4 | 0.830 | **-0.17** |
| nap_low_ais | 6.8 ± 0.4 | 0.0 ± 0.0 | 1.000 | +0.00 |
| nap_med_ais | 7.8 ± 0.4 | 1.2 ± 0.8 | 0.733 | **-0.27** |
| nap_high_ais | 16.6 ± 1.3 | 10.6 ± 0.5 | 0.221 | **-0.78** |
| nar_low_ais | 6.4 ± 0.5 | 0.0 ± 0.0 | 1.000 | +0.00 |
| nar_med_ais | 6.6 ± 0.5 | 0.0 ± 0.0 | 1.000 | +0.00 |
| nar_high_ais | 6.6 ± 0.5 | 0.0 ± 0.0 | 1.000 | +0.00 |
| kv3_low_ais | 6.4 ± 0.5 | 0.0 ± 0.0 | 1.000 | +0.00 |
| kv3_med_ais | 6.4 ± 0.5 | 0.0 ± 0.0 | 1.000 | +0.00 |
| kv3_high_ais | 6.4 ± 0.5 | 0.0 ± 0.0 | 1.000 | +0.00 |
| kv4_low_ais | 6.4 ± 0.5 | 0.0 ± 0.0 | 1.000 | +0.00 |
| kv4_med_ais | 6.4 ± 0.5 | 0.0 ± 0.0 | 1.000 | +0.00 |
| kv4_high_ais | 6.4 ± 0.5 | 0.0 ± 0.0 | 1.000 | +0.00 |

* **direction_selectivity_index (baseline_ais)**: **1.0000** (ND silenced — DSI is at its
  computational ceiling).
* **Trials with instability flags**: **0/160** — no depolarisation runaway, no silence at the
  channel-effect end either.
* **Channels still inert on AIS**: NaR, Kv3, Kv4 (same as t0067 — the AIS relocation does not
  rescue them).

## Verification

* `verify_research_code` — PASSED (0 errors, 0 warnings).
* `verify_plan` — PASSED (0 errors, 5 non-blocking warnings: short cost/step/remote sections —
  task is intentionally narrow).
* `verify_task_dependencies` — PASSED (t0008, t0019, t0065, t0067 all completed).
* `verify_task_metrics` — PASSED (registered DSI metric only).
* `verify_task_results` — PASSED (mandatory sections present in this file and
  results_detailed.md).
* `verify_suggestions` — PASSED.
* Mypy, ruff check, ruff format — all PASSED on
  `tasks/t0069_t0067_ais_localised_channel_sweep/code/`.
* All 160 trials completed; 0 unstable.

## Conclusion

Three takeaways for follow-on tasks:

* **The S-0067-03 prediction is wrong on this substrate**: a passive 30 μm AIS + 1 mm axon stuck
  onto a soma that already carries 400 mS/cm² HHst Na does not relocate the spike-initiation site
  — it just adds an electrical sink that drains current from the soma. Adding 10-90 mS/cm² of
  Nav1.6 or 0.3-0.8 mS/cm² of NaP on the AIS is too small to overcome the somatic dominance.
* **The AIS-induced DSI ceiling is a measurement artefact**: t0069 baseline DSI = 1.0 because ND
  spike count = 0, so the formula (PD-ND)/(PD+ND) collapses to PD/PD = 1. ΔDSI vs baseline = 0 for
  any channel condition that fails to push ND above zero — a noisy null. Real biological DSI
  comparisons require the cell to be in a regime where ND > 0.
* **A meaningful AIS test requires reducing somatic Na first** (or attaching the AIS to a cell whose
  soma is intentionally weakened). The next experiment in this thread should halve somatic
  gnabar_HHst before attaching the AIS, so that AIS-localised Nav1.6 can plausibly dominate spike
  initiation. Without that, channel relocation to the AIS is a no-op.
