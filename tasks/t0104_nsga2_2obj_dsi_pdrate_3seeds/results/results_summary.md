# Results Summary: t0104 — 68-d 2-Objective NSGA-II at 2 Random-Init GA Seeds (DSI Silence Guard Active)

## Summary

t0104 ran 2-objective NSGA-II `(DSI, PD-rate)` on the 68-d Bed B + morphology DSGC substrate with
the new DSI silence guard active. Two random-init GA seeds (44 and 55) completed before the
researcher elected to stop after seed 55 (intervention file
`intervention/early_stop_after_seed_55.md`); seed 66 was skipped. Across **2,208** evaluated cells,
**zero** cleared the strict joint-pass corner (DSI >= 0.5 AND PD >= 30 Hz). The **DSI extreme
cleanly broke past 0.5 for the first time** in the t0080-t0104 NSGA-II lineage (seed 55 gen 11,
**DSI = 0.5417** at PD = 3.57 Hz), confirming the substrate is not artificially capped by the
silenced-cell DSI=1.0 floating-point artifact that contaminated [t0102]'s Pareto front. The L-shaped
Pareto replicates [t0102]'s structural finding, ruling out objective-vector dimensionality as the
operative factor.

## Metrics

* **Total cells evaluated**: **2,208** (1,152 seed 44 + 1,056 seed 55)
* **Strict joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz): **0** in both seeds
* **Best DSI in the lineage** (first non-artifact DSI > 0.5): seed 55 gen 11, **DSI = 0.5417**, PD =
  3.57 Hz
* **Best joint trade-off so far**: seed 55 gen 8, **DSI = 0.4192 at PD = 15.00 Hz** (closest cell to
  the joint corner across t0080-t0104)
* **Max PD-rate**: seed 44 = **75.00 Hz**, seed 55 = **65.00 Hz** (both with DSI = 0)
* **Cells at DSI silence-guard floor** (DSI = 0.0 because total spikes < 10): **47 / 2,208 (2.1%)**;
  zero spurious DSI = 1.0 silenced-cell artifacts (vs 27 in [t0102])
* **Final hypervolume**: seed 44 = **2.85** (gen 12), seed 55 = **7.59** (gen 11)
* **Total task cost**: **$10.30** (under the $15 hard cap; under the planned $10-12 envelope)

## Verification

* `verify_task_file.py` — PASSED (0 errors)
* `verify_task_dependencies.py` — PASSED
* `verify_task_metrics.py` — PASSED
* `verify_task_results.py` — PASSED
* `verify_task_folder.py` — PASSED
* `verify_logs.py` — PASSED
* `verify_suggestions.py` — PASSED (0 errors)
* `verify_compare_literature.py` — PASSED (0 errors)
* `verify_machines_destroyed.py` — PASSED (Vast.ai instance 36645796 destroyed at
  2026-05-14T02:30:00Z)
* Predictions assets `nsga2-seed44-bedb-morph-n4-gen20-2obj` and
  `nsga2-seed55-bedb-morph-n4-gen20-2obj` — both PASS predictions verificator
* Answer asset `t0104-joint-pass-recovery-2obj` — PASS answer verificator

[t0102]: ../../t0102_seedscale_n4_gen20/
