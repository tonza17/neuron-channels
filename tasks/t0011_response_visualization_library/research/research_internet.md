---
spec_version: "3"
task_id: "t0011_response_visualization_library"
research_stage: "internet"
date_completed: "2026-04-20"
---
# Research Internet

## Objective

Collect best-practice references for building the matplotlib-based tuning-curve visualization
library (`tuning_curve_viz`), including polar-axis conventions, colour-blind-safe palettes,
confidence-band bootstrapping, and raster/PSTH layout.

## Background

This task builds a reusable plotting library that every downstream DSGC experiment consumes. The
figures must be publication-quality, use a consistent colour convention across models, and render
angle-resolved firing-rate data both in Cartesian (Hz vs direction) and polar coordinates. The
library also needs a per-angle raster+PSTH layout driven by trial-level spike-time data.

## Methodology Review

Placeholder for internet-sourced technique review; see Key Findings for actionable conventions.

## Key Findings

* **Polar-axis convention**: matplotlib polar axes default to `theta_direction=1`
  (counter-clockwise) and `theta_offset=0` (0° at east). The task description fixes this convention
  — we keep the defaults and document that `angle_deg` in the input CSV is the mathematical
  convention (0° = east, 90° = north, positive = CCW).
* **Okabe-Ito palette (8 colour-blind-safe hex codes)**: `#000000` (black), `#E69F00` (orange),
  `#56B4E9` (sky blue), `#009E73` (bluish green), `#F0E442` (yellow), `#0072B2` (blue), `#D55E00`
  (vermillion), `#CC79A7` (reddish purple). Cap the multi-model overlay at 6 models to stay within
  visually distinct entries; reserve black for the target curve dashed overlay.
* **Bootstrap 95 % CI**:
  `scipy.stats.bootstrap(data, statistic=np.mean, confidence_level=0.95, n_resamples=1000, method="percentile")`
  is available from SciPy 1.7+. The project already depends on SciPy, so no extra dependency is
  needed. For robustness against unlikely environments we keep a short NumPy fallback that resamples
  with replacement and reports the 2.5/97.5 percentiles.
* **Raster + PSTH layout**: `matplotlib.gridspec.GridSpec(2, 1, height_ratios=[3, 1])` gives a
  raster on top and a histogram below, sharing the x-axis (time in seconds).
  `ax.eventplot(spike_times_by_trial, colors="black")` is the standard raster primitive. PSTH bin
  width defaults to 10 ms (0.010 s); this matches the t0008 spike output resolution.
* **Preferred direction annotation**: on polar axes, draw a red arrow from the origin to the radius
  equal to the maximum firing rate at the angle of peak mean response; compute via `numpy.argmax` on
  the per-angle mean. Label with the angle in degrees.

## Recommended Approach

1. Depend only on matplotlib, numpy, pandas, and scipy — all already in the project environment.
2. Put the Okabe-Ito palette in a module-level constant in `tuning_curve_viz/constants.py` and cap
   the overlay at 6 models with a `UserWarning` when exceeded.
3. Use `scipy.stats.bootstrap` for the 95 % CI band, with a NumPy fallback function stubbed out but
   not wired into the default code path.
4. Keep the CLI thin: one entry point `tuning_curve_viz.cli` that takes a tuning-curve CSV, an
   output directory, and optional `--target-csv` and `--spike-times-csv` paths.
5. All plots save at 150 DPI with `bbox_inches="tight"`. No interactive rendering, no animation.

## References

* matplotlib polar axes documentation (set_theta_direction, set_theta_offset).
* Okabe, M. & Ito, K. (2008). "Color Universal Design (CUD)" — Okabe-Ito palette spec.
* SciPy `scipy.stats.bootstrap` reference (available since 1.7).
* t0004 target-tuning-curve CSV schema (`angle_deg, firing_rate_hz`).
* t0008 simulated-tuning-curve CSV schema (`angle_deg, trial_seed, firing_rate_hz`).
