# Rerun Distal-Diameter Sweep on t0022 with Halved Null-GABA

## Motivation

t0030 (distal-diameter sweep on t0022) produced a **null result** for the Schachter2010 vs
passive-filtering discriminator because **primary DSI was pinned at 1.000 across every diameter
multiplier**. Null-direction firing was exactly 0 Hz under the t0022 E-I schedule at every diameter,
so the peak-minus-null DSI metric had no dynamic range to express either predicted mechanism slope.

t0030's compare_literature traced the ceiling to `GABA_CONDUCTANCE_NULL_NS = 12 nS` delivered 10 ms
before AMPA on null trials — approximately **2× the ~6 nS compound null inhibition reported by
Schachter2010**. Lowering the null-GABA conductance to 6 nS (halved) should leave enough residual
excitation for occasional null-direction spikes while preserving preferred- direction firing,
restoring a measurable primary-DSI signal.

Source suggestion **S-0030-01** (high priority).

## Scope

1. Use the **t0022 DSGC testbed** as-is (channel set, morphology, AIS partition, 12-direction
   protocol, 10 trials per angle) — EXCEPT: set `GABA_CONDUCTANCE_NULL_NS = 6.0 nS` (half of the
   default 12 nS). Preferred-direction GABA stays at its default.
2. Identify distal dendritic sections via t0030's selection rule (HOC leaves on `h.RGC.ON`, branch
   order ≥ 3). COPY the helper into this task's `code/`; no cross-task imports.
3. Sweep 7 distal-diameter multipliers (0.5×, 0.75×, 1.0×, 1.25×, 1.5×, 1.75×, 2.0×) uniformly on
   all distal branches. Same set as t0030.
4. 12-direction moving-bar tuning × 10 trials per angle per diameter = **840 trials total**.
5. Compute **primary DSI (peak-minus-null)** as the operative metric. Unlike t0030, this is expected
   to vary because null-direction firing should now be non-zero. Also compute vector-sum DSI and
   standard secondary metrics.
6. Plot primary DSI vs diameter and classify slope sign:
   - Positive slope → **Schachter2010 active-dendrite amplification** supported
   - Negative slope → **Passive-filtering** supported
   - Flat → mechanism remains ambiguous; diagnose cause (inspect null-firing rate change)

## Approach

* **Local CPU only.** No remote compute, no paid APIs, $0.
* Copy the t0030 code/ workflow verbatim: `paths.py`, `constants.py`, `diameter_override.py` (with
  `identify_distal_sections`), `preflight_distal.py`, `trial_runner_diameter.py`, `run_sweep.py`,
  `analyse_sweep.py`, `classify_slope.py`, `plot_sweep.py`.
* Override the `GABA_CONDUCTANCE_NULL_NS` constant at import time (or expose a CLI override). Keep
  preferred-direction GABA at default.
* Save per-sweep-point tidy CSV incrementally (crash recovery via `fh.flush()`).
* Render DSI-vs-diameter curve, vector-sum DSI curve, polar overlay, null-Hz-vs-diameter curve (new
  diagnostic to confirm the fix is working).

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary including null-Hz-vs-diameter
  baseline (should be non-zero), primary DSI dynamic range, slope classification, mechanism
  attribution.
* `results/results_detailed.md` — per-direction breakdown, slope classification, comparison to
  t0030's pinned-1.000 baseline, discussion of which mechanism the schedule-fixed data favours.
* `results/images/dsi_vs_diameter.png`, `vector_sum_dsi_vs_diameter.png`, `polar_overlay.png`,
  `null_hz_vs_diameter.png` (new: confirms the fix desaturates null firing),
  `peak_hz_vs_diameter.png`.
* `results/metrics.json` — DSI primary, vector-sum, peak Hz, null Hz per diameter.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* Local CPU only. Expected runtime: **~2 hours** (extrapolated from t0030's ~115 min on same
  testbed; non-zero null firing doesn't change per-trial wall time meaningfully).
* $0 external cost.

## Measurement

* **Primary metric**: **primary DSI (peak-minus-null)** per diameter — expected to vary now that
  null firing is unpinned.
* **Critical diagnostic**: **null-direction firing rate per diameter** — must be non-zero to confirm
  the GABA change had the intended effect.
* **Secondary**: vector-sum DSI, peak Hz, HWHM, reliability, preferred-direction firing,
  per-direction spike counts, distal peak mV.

## Key Questions

1. Does null-direction firing become non-zero with GABA reduced to 6 nS? (Pre-condition for
   everything else. If it's still 0 Hz, the fix failed; consider a smaller reduction.)
2. With null firing unpinned, what is the primary DSI-vs-diameter slope sign?
3. Does the slope match Schachter2010 (positive), passive filtering (negative), or neither?
4. How does the halved-GABA result on t0022 compare to t0035 (same diameter sweep on t0024)? Both
   should now have unpinned primary DSI — do they agree on the diameter axis being a weak
   discriminator?

## Dependencies

* **t0022_modify_dsgc_channel_testbed** (completed) — provides the DSGC testbed architecture and the
  default `GABA_CONDUCTANCE_NULL_NS = 12 nS` to be overridden.
* **t0030_distal_dendrite_diameter_sweep_dsgc** (completed) — provides the workflow template, the
  `identify_distal_sections` helper (to be copied), and the null-result baseline for before/after
  comparison.

## Scientific Context

Source suggestion **S-0030-01** (high priority). Complementary to S-0029-04 (null-GABA sweep at
fixed length) and S-0029-01 (Poisson + length sweep) — this specifically targets the diameter axis
with a fixed halved-GABA schedule change. Also parallels t0035 (diameter sweep on t0024) which found
flat DSI, allowing a cross-testbed comparison under unpinned primary-DSI conditions.

## Execution Notes

* Follow standard `/execute-task` flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 + t0030 already cover the mechanism
  predictions).
* Include `research-code` — inherit t0030 workflow + t0022 driver.
* Skip `setup-machines` / `teardown` (local CPU only).
* Include `creative-thinking` — if null-Hz rescue works, interpret the slope in the context of t0035
  (diameter on t0024) result.
* Include `compare-literature` — compare DSI-vs-diameter slope to Schachter2010 / passive-filtering
  predictions AND to t0030 null baseline AND to t0035 flat-on-t0024 result.
