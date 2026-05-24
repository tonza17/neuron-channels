---
spec_version: "2"
task_id: "t0123_bedb_mi_atp_per_spike_nsga2"
status: "completed"
date_completed: "2026-05-24"
---
# Results Summary: NSGA-II MI vs ATP-per-Spike (Bed B + 14-d Morph)

## Summary

68-d NSGA-II (54-d electrophys + 14-d morphology) on Bed B at GA seed 441, pop=96, N_EVAL_SEEDS=3, 4
antipodal directions, ran to gen 60 ceiling cleanly. The two-tier MI estimator surfaced a real
discrepancy: count-MI hit **1.459 bits** at the high-MI corner while Strong-Bialek direct-method
**bits/s = 0.0 for all 10 top Pareto cells**, because the optimiser exploited count-MI at the
silence-guard boundary (~3 PD spikes/trial) where spike-time information is degenerate.

## Metrics

* **Hypervolume gain**: 9.16 x 10^9 (gen 1) -> **2.917 x 10^10** (gen 60), +218%; converged by gen
  50 (last 10 gens added < 0.001%).
* **Best `mi_count_bits` (legit silence-passed)**: **1.459 bits** at cell 2 (PD-rate 2.86 Hz, DSI
  0.316). Ceiling = log2(4) = 2.0 bits.
* **Lowest `atp_per_spike_molecules` (MI > 0)**: **4.55 x 10^6 ATP/spike** at cell 1 (MI 0.11 bits,
  DSI 0.13). Degenerate silent corner: 6.76 x 10^5 ATP/spike at cell 0 (MI = 0).
* **Strong-Bialek `bits_per_sec` on top-10 cells**: **0.0 for all 10 cells** (8 dirs * 20 trials,
  dt=5 ms, T in {25, 50, 75, 100} ms). h_total = h_noise = 0 at every word length because PD-rate is
  too low (~3 spikes per 1400 ms trial) to populate non-trivial spike-time words.
* **Niven 2007 verdict**: **"Insufficient evidence"** -- log-log fit
  `log(bits_per_sec) = p * log(ATP/spike) + b` is undefined when bits/s = 0 across all 10 cells.
* **DSI across Pareto front**: 0.13 to 0.40 (DSI was NOT an optimiser objective; tracked as
  diagnostic). No legit cell by t0122's DSI>=0.5 + PD>=30Hz threshold.
* **Silence rate**: 95.8% (gen 1) -> 0% (gens 51-60). 10-gen pool restart fired at gens 10, 20, 30,
  40, 50 per the project's standing rule.
* **Total cost**: **$1.191 / $6 cap** (20% utilisation). NSGA-II 5h, post-hoc Strong-Bialek 35min,
  pre-/post-finalize idle 24min + 30min.

## Verification

* `verify_task_file`: PASSED.
* `verify_task_dependencies`: PASSED (all 9 dependencies completed).
* `verify_task_metrics`: PASSED (4 variants with `direction_selectivity_index` registered;
  task-specific MI/ATP keys in `dimensions`).
* `verify_predictions_asset`: PASSED, 0 errors (3 warnings, non-blocking).
* `verify_answer_asset`: PASSED, 0 errors, 0 warnings.
* `verify_machines_destroyed`: PASSED (0 errors, 1 expected RM-W001).
* `verify_plan`: PASSED.
* `verify_research_code`: PASSED.

See `results_detailed.md` for methodology, per-cell breakdown, charts, and the full Task Requirement
Coverage section.
