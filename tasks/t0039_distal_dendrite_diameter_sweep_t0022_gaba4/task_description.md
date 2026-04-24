# 7-Diameter Sweep on t0022 DSGC at GABA=4 nS

## Motivation

t0030 originally ran a 7-diameter sweep on t0022 to measure the Schachter2010-vs-passive-filtering
DSI slope — the project's headline discriminator target since its inception. The attempt failed
because the t0022 default `GABA_CONDUCTANCE_NULL_NS = 12 nS` pins primary DSI at 1.000 (null firing
= 0 Hz), leaving the discriminator flat across all diameters. t0036 halved the GABA to 6 nS; still
pinned. t0037 then swept the ladder {4, 2, 1, 0.5, 0} nS and found **4 nS** is the operational sweet
spot (DSI=0.429, DSGC-like preferred direction 40.8°, matches Park2014's biological range
0.40–0.60).

This task reruns t0030's geometry sweep at the newly-discovered working GABA level, producing the
first diameter-vs-DSI measurement on t0022 with a discriminator that has dynamic range. The
resulting slope is the quantity the project needs to test the Schachter2010 active-amplification
hypothesis against the passive cable-theory prediction.

## Scope

Sweep **distal dendrite diameter** across 7 levels at `GABA_CONDUCTANCE_NULL_NS = 4.0 nS` on the
t0022 testbed. All other parameters match the t0030 baseline, so the two sweeps are directly
comparable except for the GABA value.

* Diameters (µm): {0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0}
* Trials per angle per diameter: 10
* Angles per sweep: 12 (standard DSGC tuning directions)
* Total trials: 7 × 12 × 10 = **840 trials**
* Expected wall time on local Windows CPU: ~30 minutes (~2 s/trial)
* Cost: $0.00

## Dependencies

* `t0022_modify_dsgc_channel_testbed` — testbed + `GABA_CONDUCTANCE_NULL_NS` knob
* `t0030_distal_dendrite_diameter_sweep_dsgc` — reuses diameter-sweep driver and analysis code
* `t0037_null_gaba_reduction_ladder_t0022` — source of the 4 nS GABA choice

## Approach

1. Copy t0030's code into t0039's `code/` folder (ARF cross-task import rule requires copying).
2. Adapt t0037's `gaba_override.py` — call `set_null_gaba_ns(4.0)` at the start of each trial
   before invoking `run_tuning_curve`.
3. Parameterise the diameter sweep over the t0030 diameter list.
4. Run all 840 trials locally; monitor the process until completion.
5. Analyse per-diameter DSI means and stddev; fit the DSI-vs-diameter slope and compare to
   Schachter2010 (active amplification expects concave-down, passive filtering expects monotonically
   decreasing).
6. Write `compare_literature.md` matching our slope against published DSGC diameter dependence.

## Expected Outputs

* `results/data/sweep_results.csv` — full 840-trial raw output (diameter, angle, trial, peak_hz,
  null_hz, dsi_primary, dsi_vector_sum, pref_angle).
* `results/data/metrics_per_diameter.csv` — per-diameter aggregated metrics (mean, stddev, n).
* `results/data/slope_fit.json` — fitted slope of DSI vs diameter with CI.
* `results/images/dsi_vs_diameter.png` — DSI means with error bars across 7 diameters.
* `results/images/tuning_curves_per_diameter.png` — 7-panel plot of fitted tuning curves.
* `results/results_summary.md`, `results/results_detailed.md` — full writeup.
* `results/compare_literature.md` — comparison to Schachter2010 vs passive cable predictions.
* `results/suggestions.json` — follow-ups based on outcome.

## Expected Assets

None beyond CSV / JSON / images. Task type: `experiment-run`.

## Compute and Budget

* Local Windows CPU only. No GPU, no remote machines, no paid APIs.
* Wall time: ~30 minutes for the sweep; total task wall time including ARF pipeline ~60 minutes.
* Cost: $0.00.

## Cross-References

* Source suggestion: **S-0037-01** — "Rerun t0030's 7-diameter sweep at GABA=4 nS on t0022".
* Evidence task: t0037 (DSI=0.429 at 4 nS, DSGC-like pref 40.8°).
* Pinned baselines: t0030 (12 nS, DSI=1.000 flat), t0036 (6 nS, DSI=1.000 still flat).
* Correction task: t0038 (recorded the base-parameter update on t0033's answer asset).

## Verification Criteria

1. 840 trials complete successfully (exit code 0 from the sweep driver).
2. `metrics_per_diameter.csv` has 7 rows, all with non-null DSI values.
3. At least one diameter has primary DSI measurably different from every other diameter (the sweep
   is informative, not pinned).
4. The DSI-vs-diameter slope is reported with a numeric value and 95% CI.
5. All standard verificators PASS with zero errors.
