# t0113 - Seed-2247 Random-Seed Replicate of t0106: Results Summary

## Summary

Seed 2247 reaches **0 LEGIT joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz with the silence-guard
excluded) on the same 68-d Bed B + 14-d morphology substrate, while the 2 cells the asset records as
joint-pass-unique are both DSI = 1.0 silence-guard saturations (1-spike PD / 0-spike ND), not
biological selectivity. The HV-plateau detector fired at gen 14 (8% of `N_GEN = 60`, well below both
t0106 gen 40 and t0112 gen 21), the per-generation wall-clock averaged **160 s/gen** on a 64-core
EPYC 7B13 (3.9x faster than t0112's 620 s/gen baseline because the instance had 2x more cores), and
total task spend was **$0.4773** of the $25 cap.

## Metrics

* **Joint-pass cells (asset-declared, unique)**: **2** at DSI = 1.0 silence-guard ceiling (PD = 35.0
  and 45.24 Hz). **0 LEGIT joint-pass cells** (no cell reached BOTH DSI >= 0.5 AND PD >= 30 Hz
  without silence-guard saturation).
* **Best legit DSI** (highest non-silence-guard cell): **0.3651** at PD = 10.24 Hz (gen 7).
* **Best PD-rate**: **71.67 Hz** at DSI = 0.0017 (gen 10).
* **Overall max DSI**: **1.0000** (silence-guard / single-spike artefact).
* **NSGA-II generations completed**: **14** of 60 ceiling (HV plateau triggered; watchdog NOT
  tripped).
* **Cells evaluated**: **1,344** = 96 x 14 generations.
* **Final hypervolume (2-D)**: **45.6221** (start 0.2460 -> 185x growth).
* **HV-plateau generation**: **14** (vs t0112's 21 and t0106's 40 — earliest plateau of the 3-seed
  sample).
* **Per-generation wall-clock**: **160 s/gen** mean on 64-core EPYC 7B13 (vs t0112's 620 s/gen on
  32-core EPYC; 26% of t0112's baseline = **NOT within +/- 20%** but in the FAVOURABLE direction).
* **NSGA-II compute cost (productive)**: **$0.1467** of $25 cap (0.6% utilisation).
* **Total task cost (productive + setup + retries)**: **$0.4773** of $25 cap.

## Answers to the Task's 7 Key Questions

1. **Seed-2247 joint-pass count bucket (>= 40 / 7-39 / 1-6 / 0)?** **0 LEGIT** joint-pass cells; the
   2 asset-declared unique cells are both DSI = 1.0 silence-guard artefacts at PD = 35.0 and 45.24
   Hz, so by the substrate-density reading the count is **0** (substrate not populated at this seed)
   and by the raw asset-declared reading the count is **2** (sparse bucket: 1-6 cells).
2. **Best ratio DSI >= 0.95?** **NO, decisively.** Overall max = 1.0000 but is a silence-guard
   ceiling, not biological selectivity. Best legit DSI = **0.3651** (62% below the 0.95 target and
   far below t0106's 0.9939 / t0112's 0.9535).
3. **Best PD-rate >= 100 Hz?** **NO.** Best PD = **71.67 Hz** (28% below the 100-Hz target; 58% of
   t0106's 122.62 Hz and 62% of t0112's 114.76 Hz).
4. **3-seed substrate-rate mean and SE vs Hay 2011 0.40% / Druckmann 2007 0.10% baselines?**
   Per-seed acceptance: t0106 = 3.29%, t0112 = 0.35%, t0113 = 0.15%. **Mean = 1.26%, SD = 1.76%, SE
   = 1.01%**, 95% CI (-0.73%, 3.25%). The point estimate is **3x above the Hay 2011 envelope upper
   bound (0.40%) and 13x above the Druckmann 2007 baseline (0.10%)**, but the SE is larger than the
   mean — the 95% CI brackets BOTH literature baselines and 0%. The 3-seed sample is still too noisy
   to reject either baseline; the 5-seed batch from S-0112-01 is still required.
5. **HV-plateau generation vs t0106 gen 40 / t0112 gen 21?** **Gen 14**, **OUTSIDE the t0106-t0112
   range** by 7 generations on the early side. Cost watchdog NOT tripped. The same
   `HV_PLATEAU_REL_THRESHOLD = 0.01` over `HV_PLATEAU_WINDOW = 2` constants fired earlier on this
   seed because the HV climb between gen 12-14 (36.07 -> 36.10 -> 45.62) had a one-step plateau that
   the detector tolerated as the start of saturation. **This is plausibly a premature trigger** —
   see Limitations in `results_detailed.md`.
6. **Per-gen wall-clock within +/- 20% of t0112's 620 s/gen baseline?** **NO** — t0113 averaged
   **160 s/gen** (vs t0112's 620 s/gen), which is **74% LOWER** than t0112 and **far outside the +/-
   20% (496-744 s/gen) band**. The driver is identical to t0112; the 3.9x speedup is entirely
   attributable to the larger EPYC 7B13 instance (t0113 had 64 cores / 256 threads with 125 GB RAM;
   t0112 had 32 effective cores with 503 GB RAM, but RAM was never the bottleneck). The cadence-10
   protocol persists; at the per-core level wall-clock is consistent with t0112.
7. **Pareto front overlap (closer to seed 44 or seed 77)?** **MIXED** — of t0113's 8 strict Pareto
   cells, 4 are closer to a t0106 (seed 44) cell in z-scored 68-d parameter space and 4 are closer
   to a t0112 (seed 77) cell (see `results/data/pareto_front_overlap_3seeds.csv`). The nearest-
   neighbour z-scored distances are all in the 9.7-11.5 range (mean ~10.7) regardless of target,
   indicating that t0113's Pareto cells are **roughly equidistant from both seed-44 and seed-77
   cells in normalised parameter space** — neither seed is a closer match than the other.

## Verification

* `verify_predictions_asset` (meta path): expected PASSED, non-blocking PR-W014/W015 warnings (no
  linked model / dataset asset — same as t0106/t0112).
* `verify_predictions_description`, `verify_predictions_details`: expected PASSED.
* `verify_task_results` (this file + `results_detailed.md`): see `## Verification` section of
  `results_detailed.md` for the verificator run record.
* `verify_task_metrics`: `metrics.json` registers only the `direction_selectivity_index` metric per
  `meta/metrics/`; sub-variants `best_legit`, `overall_max`, and `dsi_eq_one_count` are encoded as
  separate variants in the explicit multi-variant format.
* `verify_machines_destroyed`: PASSED (instance 37107202 destroyed at 2026-05-20T02:11:25Z, within 5
  min of the HV-plateau stop).
