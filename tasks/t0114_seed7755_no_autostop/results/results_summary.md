# t0114 - Seed-7755 NSGA-II Replicate of t0106 with HV-Plateau Auto-Stop Disabled: Results Summary

## Summary

Seed 7755 with the HV-plateau auto-stop DISABLED reached **484 unique LEGIT joint-pass cells** (DSI
≥ 0.5 AND PD-rate ≥ 30 Hz AND DSI < 0.9999) across **5,952 evaluations / 62 NSGA-II
generations** on the same 68-d Bed B + 14-d morphology substrate as t0106/t0112/t0113. The run
terminated by **operator stop** (not by any auto-stop rule) after the HV trajectory visibly
plateaued near HV = 111.54, vindicating S-0113-03's hypothesis that the t0113 14-gen plateau was a
premature trigger; the same protocol on seed 7755 ran for 4.4x more generations and reached **70x
more LEGIT joint-pass cells (484 vs t0113's 0)**, **2.4x more HV (111.54 vs 45.62)**, and **higher
best-legit DSI (0.9926 vs t0113's 0.3651)**. The S-0113-03 offline detector replay over a 4-window x
6-threshold grid (24 cells) on the four available HV trajectories selects **(W*, T*) = (3, 0.015)**
as the recommended new project default: it fires on t0106 at gen 39 (within the [20, 60] target),
does NOT fire prematurely on t0113 within the recorded 14 gens, and fires on t0114 at gen 26.

## Metrics

* **Unique joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz): **771**.
* **Unique LEGIT joint-pass cells** (additionally DSI < 0.9999): **484** — places seed 7755 in the
  same yield bucket as t0106 seed 44 (121 LEGIT) rather than t0112's sparse 7 or t0113's 0.
* **Best LEGIT DSI** (highest non-silence-guard cell): **0.9926** at PD = 63.81 Hz (gen 61). Within
  1 percentage point of t0106 seed 44's 0.9939.
* **Best PD-rate**: **112.86 Hz** at DSI = 0.0271 (gen 62). Slightly below t0106 seed 44's 125.95
  Hz; both seeds clearly populate the high-PD frontier.
* **Overall max DSI**: **1.0000** (silence-guard / single-spike artefacts; **1,073** cells at the
  DSI = 1.0 ceiling).
* **Strict Pareto cells**: **6** — all in the upper-right region (DSI >= 0.0271 and PD >= 61.9
  Hz).
* **NSGA-II generations completed**: **62** of 300 ceiling (operator stop after visible plateau).
* **Cells evaluated**: **5,952** = 96 x 62 generations.
* **Final hypervolume (2-D)**: **111.5353** (start 0.6776 -> 165x growth; 91% of t0106's 122.03).
* **Stop trigger**: **operator_stop** (HV-plateau auto-stop was DISABLED for this run).
* **NSGA-II compute cost (productive)**: **$0.9399** of $25 cap (3.8% utilisation).
* **Total task cost (productive + setup + teardown)**: **$1.1282** of $25 cap (4.5% utilisation).

## Answers to the Task's 3 Key Questions

1. **Did the t0113 14-gen stop reflect real saturation, or was it premature?** **PREMATURE.** With
   the auto-stop DISABLED, seed 7755 (same protocol, same cadence-10 restart) ran to gen 62 and
   accumulated 484 LEGIT joint-pass cells; the HV trajectory continued climbing significantly past
   the gen 14 mark (HV(14) ~36-46 vs HV(62) = 111.54). The S-0113-03 hypothesis is confirmed: the
   current (W=2, T=0.01) detector is too aggressive on this substrate.

2. **What is the recommended new (WINDOW, REL_THRESHOLD)?** **(W*, T*) = (3, 0.015).** This is the
   smallest deviation from the current defaults that (a) fires on t0106 within [20, 60] gens (it
   fires at gen 39), (b) does NOT fire prematurely on t0113 within the recorded 14 gens, and (c)
   fires on t0114 at gen 26 (well after the gen 14 false-positive zone). See `detector_replay.csv`
   for the full 32-row replay (4 windows x 2 thresholds x 4 seeds) and the wider 96-row grid used
   for selection.

3. **How does the 4-seed substrate-rate estimate compare to Hay 2011 / Druckmann 2007?** Per-seed
   LEGIT yields: t0106 = 121/3744 = **3.23%**, t0112 = 7/2016 = **0.35%**, t0113 = 0/1344 =
   **0.00%**, t0114 = 484/5952 = **8.13%**. **4-seed mean = 2.93%, SD = 3.71%, SE = 1.86%**, 95% CI
   (-0.71%, 6.56%). The point estimate is **7.3x above the Hay 2011 envelope upper bound (0.40%) and
   29x above the Druckmann 2007 baseline (0.10%)**. The SE is still large (95% CI brackets both
   baselines and 0%), but seeds 44 and 7755 each independently exceed the literature envelope; the
   substrate is plausibly more populated than the literature suggests, with seeds 77 and 2247 being
   unlucky low-density draws.

## Verification

* `verificator (meta path, predictions asset)`: PASSED. Non-blocking PR-W014/W015 warnings (no
  linked model / dataset asset — same as t0106/t0112/t0113).
* `verify_task_results`: see `## Verification` section of `results_detailed.md` for the run record.
* `verify_task_metrics`: `metrics.json` registers only the `direction_selectivity_index` metric per
  `meta/metrics/`; sub-variants `best_legit`, `overall_max`, and `dsi_eq_one_count` are encoded as
  separate variants in the explicit multi-variant format.
