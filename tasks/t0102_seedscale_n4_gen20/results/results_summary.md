# Results Summary: t0102 Seed-scale N=4, Gen=20 Random-Init NSGA-II

## Summary

Both random-init NSGA-II GA seeds (44, 55) completed at `N_EVAL_SEEDS=4` on the 68-d Bed B +
morphology DSGC substrate but were terminated by the per-seed $4 cost watchdog before reaching
generation 20 (seed 44: 14/20 gens, seed 55: 13/20 gens). Across all **2,592** evaluated cells,
**zero** cleared the strict joint-pass corner (DSI >= 0.5 AND PD-rate >= 30 Hz AND robustness >=
0.7) and **zero** cleared even the loosest 2-axis variant (DSI >= 0.5 AND PD >= 5 Hz). The 5x noise
drop + 2.5x generation extension hypothesis from the brainstorm is therefore rejected; t0099's
negative result replicates at a different seed/gen/noise budget. A previously unreported
floating-point artifact in the DSI vector-sum objective was uncovered: 27 cells with max DSI = 1.0
are silenced cells (PD = 0 Hz) where divide-by-near-zero in the vector-sum formula produces a
spurious "perfect DSI" signal — the real DSI corner sits at DSI ~= 0.35 with PD >= 5 Hz.

## Metrics

* **Total cells evaluated**: **2,592** (1,344 seed 44 + 1,248 seed 55)
* **Strict joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz AND rob >= 0.7): **0** in both seeds
* **2-axis loose joint-pass cells** (DSI >= 0.5 AND PD >= 5 Hz): **0** across both seeds
* **Max DSI (vector-sum)**: **1.0000** in both seeds — but on silenced cells (PD = 0 Hz),
  reflecting a floating-point artifact, not a real direction-selectivity signal
* **Max PD-rate**: seed 44 = **64.29 Hz**, seed 55 = **66.96 Hz** (both with DSI ~ 0)
* **Real-DSI corner** (excluding silenced cells, PD > 0): **DSI ~ 0.35** at PD ~ 4 Hz
* **Final hypervolume**: seed 44 = **7.53** (gen 14), seed 55 = **3.39** (gen 13)
* **Total task cost**: **$12.0733** — over the $8 plan cap by $4.07, under the user-authorized $15
  ceiling; $8.46 of that was productive NSGA-II compute, $3.51 was idle uptime

## Verification

* `verify_task_results.py t0102_seedscale_n4_gen20` — PASSED (0 errors)
* `verify_task_metrics.py t0102_seedscale_n4_gen20` — PASSED (0 errors)
* Predictions assets `nsga2-seed44-bedb-morph-n4-gen20` and `nsga2-seed55-bedb-morph-n4-gen20` —
  both PASS predictions verificator
* Remote machine entry in `results/remote_machines_used.json` matches the Vast.ai instance log
  (machine 36556586 destroyed at 2026-05-12T17:57:21Z)
