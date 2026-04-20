---
spec_version: "1"
task_id: "t0011_response_visualization_library"
research_stage: "internet"
searches_conducted: 6
sources_cited: 8
papers_discovered: 0
date_completed: "2026-04-20"
status: "complete"
---
# Research Internet

## Task Objective

Build `tuning_curve_viz`, a reusable matplotlib library that renders standard tuning-curve CSVs
(produced by t0004 and t0008) as Cartesian, polar, multi-model overlay, and per-angle raster+PSTH
PNGs for every downstream DSGC experiment. Collect engineering references that fix polar-axis
conventions, colour-blind-safe palette choices, confidence-band bootstrapping, and raster/PSTH
layout so that all downstream figures share a single publication-quality visual language.

## Gaps Addressed

This is a `write-library` task, so `research_papers.md` was skipped (no open research questions or
methodology reviews are required to produce a plotting library). There are therefore no gaps from
`research_papers.md` to resolve. The internet research instead targets engineering-convention gaps
— polar-axis direction, colour-blind palette, bootstrap API, raster+PSTH layout — that are not
peer-reviewed research questions but are necessary defaults for a consistent visualisation layer.
All four convention gaps listed below are marked **Resolved** via the matplotlib, scipy, and CUD
documentation sources indexed at the end of this file.

* **Polar-axis direction and zero-angle convention** — **Resolved** via [MPL-PolarAxes-Docs].
* **Colour-blind-safe palette for multi-model overlays** — **Resolved** via [CUD-Okabe-Ito-2008].
* **95 % confidence-interval bootstrap API** — **Resolved** via [SciPy-Bootstrap].
* **Raster + PSTH layout primitives** — **Resolved** via [MPL-Eventplot] and [MPL-GridSpec].

## Search Strategy

**Sources searched**: matplotlib official documentation, SciPy official documentation, Okabe & Ito
Color Universal Design (CUD) reference page, Stack Overflow (for raster/PSTH idioms), GitHub code
search for `eventplot` + `hist` PSTH patterns.

**Queries executed** (6 total):

1. `matplotlib polar axis set_theta_direction set_theta_offset default`
2. `Okabe Ito colour blind safe palette hex codes`
3. `scipy.stats.bootstrap confidence_interval mean n_resamples`
4. `matplotlib eventplot raster trial spike times`
5. `matplotlib gridspec height_ratios PSTH histogram shared x axis`
6. `matplotlib polar arrow annotate preferred direction radius`

**Date range**: no restriction — the relevant references are stable API documentation pages and
the 2008 CUD specification. matplotlib and SciPy docs consulted at their current (3.x and 1.11+)
versions.

**Inclusion criteria**: Must provide (a) an authoritative API reference for a matplotlib/SciPy
primitive we plan to call, or (b) the canonical specification of a colour-palette / visualisation
convention. Excluded: third-party blog posts with outdated APIs, and tutorials that rely on
deprecated `pyplot.polar` shortcuts.

**Search iterations**: Query 6 was a follow-up triggered when query 1 established that a
preferred-direction annotation overlay was feasible but not documented as a single recipe; it
confirmed that `ax.annotate` with `xycoords="polar"` is the standard pattern.

## Key Findings

### Polar-axis conventions in matplotlib

matplotlib polar axes default to `theta_direction=1` (counter-clockwise) and `theta_offset=0` (0°
at east, i.e. the positive x-axis) [MPL-PolarAxes-Docs]. This matches the mathematical convention
our upstream t0004/t0008 CSVs already use — `angle_deg` is measured CCW from east — so the
library never needs to transform input angles. We explicitly document this convention in
`description.md` and keep matplotlib's defaults. If a downstream task ever supplies a
clock-convention CSV (0° at north, clockwise), it must transform angles at the call site, not
inside `tuning_curve_viz`.

**Best practice**: do not silently transform angles inside the plotting library; surface the
convention in documentation so that downstream callers cannot mis-align data with axes.

### Okabe-Ito colour-blind-safe palette

The Okabe & Ito (2008) Color Universal Design (CUD) palette defines eight colour-blind-safe hex
codes [CUD-Okabe-Ito-2008]: `#000000` (black), `#E69F00` (orange), `#56B4E9` (sky blue), `#009E73`
(bluish green), `#F0E442` (yellow), `#0072B2` (blue), `#D55E00` (vermillion), `#CC79A7` (reddish
purple). The palette is recommended across the neuroscience-figure community because it preserves
distinguishability under deuteranopia and protanopia. We cap the multi-model overlay at **6 models**
(palette minus black, minus yellow which has low contrast on white) and reserve **black** for the
target tuning curve drawn as a dashed line on every overlay.

**Best practice**: pre-register the palette as a module-level constant so every figure in the
project inherits an identical colour mapping for the same model label.

### Bootstrap 95 % confidence band via SciPy

`scipy.stats.bootstrap(data, statistic=np.mean, confidence_level=0.95, n_resamples=1000, method="percentile")`
is the canonical API and has been available since SciPy 1.7 [SciPy-Bootstrap]. It returns a
`BootstrapResult` with `.confidence_interval.low` and `.high` arrays, suitable for
`ax.fill_between(angles, low, high, alpha=0.3)`. The project already depends on SciPy, so no new
dependency is needed. For defensive robustness, we keep a four-line NumPy fallback
(`np.random.default_rng().choice(..., replace=True)` + `np.percentile(..., [2.5, 97.5])`) that is
stubbed but not wired into the default code path.

**Hypothesis** (testable): the 95 % CI width at each angle is a monotonic function of trial count
per angle; downstream tasks with noisy sampling should verify this rather than assume it.

### Raster + PSTH layout

The community-standard layout for per-angle raster+PSTH is a `GridSpec(2, 1, height_ratios=[3, 1])`
with a shared x-axis (time in seconds) [MPL-GridSpec]. The raster is drawn with
`ax.eventplot(spike_times_by_trial, colors="black")` [MPL-Eventplot] where `spike_times_by_trial` is
a list of 1-D arrays (one array of spike times per trial). The PSTH below uses `ax.hist` with 10 ms
bins (0.010 s), matching t0008's spike-time resolution.

**Best practice**: call `ax.sharex(raster_ax)` on the PSTH axis so zoom/pan stays aligned.

### Preferred-direction annotation on polar axes

Preferred direction is the angle at which the per-angle mean firing rate is maximal. Compute via
`np.argmax` on the mean vector, then draw a red arrow from the origin to the radius equal to the
peak rate via
`ax.annotate("", xy=(theta_pref, r_max), xytext=(0, 0), xycoords="polar", arrowprops=dict(arrowstyle="->", color="red"))`
[MPL-PolarAxes-Docs]. Label with the angle in degrees.

**Best practice**: compute the preferred direction from the per-angle mean of the sample — not
from a vector sum — so that noisy low-rate tails do not skew the arrow.

## Methodology Insights

* **Dependencies**: depend only on `matplotlib`, `numpy`, `pandas`, and `scipy` — all already in
  the project environment. No new `pyproject.toml` entries.
* **Palette constant**: store the 8 Okabe-Ito hex codes in `tuning_curve_viz/constants.py`. Cap the
  multi-model overlay at 6 models; emit a `UserWarning` and truncate deterministically (sorted dict
  keys) when exceeded.
* **Bootstrap wiring**: default to `scipy.stats.bootstrap` with `n_resamples=1000`,
  `method="percentile"`, `confidence_level=0.95`, and `vectorized=True`. Keep the NumPy fallback
  present but inert.
* **Thin CLI**: one entry point `tuning_curve_viz.cli` with `argparse` flags `--curve-csv`,
  `--target-csv`, `--spike-times-csv`, `--out-dir`. No interactive rendering, no animation.
* **PNG save defaults**: `dpi=150`, `bbox_inches="tight"`, `facecolor="white"`. No vector output
  (SVG/PDF) from the library — downstream tasks that need vector can reopen the returned Figure.
* **Polar angle pass-through**: never transform `angle_deg`. Callers must pre-align to the
  mathematical convention (0° east, CCW positive).
* **Hypothesis to test in future tasks**: the raster+PSTH view at the preferred direction is
  sufficient to diagnose most DSGC response pathologies without needing a full 8-angle raster grid.
  A future task should empirically compare single-angle vs. grid diagnostic value.

## Discovered Papers

No new papers were discovered. This is a write-library task producing an engineering artefact
(matplotlib visualisation layer); the relevant references are API documentation and a single
colour-palette specification, not peer-reviewed research. The project's existing paper corpus is not
affected by this task.

## Recommendations for This Task

1. **Use matplotlib defaults for polar axes** (`theta_direction=1`, `theta_offset=0`) and document
   the input-angle convention in `description.md` [MPL-PolarAxes-Docs].
2. **Adopt the Okabe-Ito palette** as a module-level constant; reserve black for the target curve
   and cap overlays at 6 models [CUD-Okabe-Ito-2008].
3. **Use `scipy.stats.bootstrap`** with 1 000 resamples for 95 % CI bands; keep a NumPy fallback
   stubbed but not wired by default [SciPy-Bootstrap].
4. **Implement raster+PSTH via `GridSpec(2, 1, [3, 1])`** + `ax.eventplot` + `ax.hist` with 10 ms
   bins [MPL-GridSpec] [MPL-Eventplot].
5. **Annotate preferred direction** with a red polar arrow from the origin to the peak mean rate.
6. **Save all PNGs at 150 DPI** with `bbox_inches="tight"` and a white face colour. No SVG/PDF
   output from the library itself.

## Source Index

### [MPL-PolarAxes-Docs]

* **Type**: documentation
* **Title**: matplotlib.projections.polar.PolarAxes
* **Author/Org**: Matplotlib Development Team
* **Date**: 2024
* **URL**: https://matplotlib.org/stable/api/projections/polar_api.html
* **Last updated**: 2024-09
* **Peer-reviewed**: no
* **Relevance**: Authoritative reference for `set_theta_direction`, `set_theta_offset`, polar
  `annotate`, and the default CCW-from-east convention we inherit unchanged.

### [CUD-Okabe-Ito-2008]

* **Type**: documentation
* **Title**: Color Universal Design (CUD) — How to make figures and presentations that are
  friendly to colour-blind people
* **Author/Org**: Okabe, M. & Ito, K.
* **Date**: 2008
* **URL**: https://jfly.uni-koeln.de/color/
* **Peer-reviewed**: no
* **Relevance**: Canonical spec for the eight colour-blind-safe hex codes adopted as our multi-model
  palette. Recommended by the neuroscience figure community for preserving distinguishability under
  deuteranopia/protanopia.

### [SciPy-Bootstrap]

* **Type**: documentation
* **Title**: scipy.stats.bootstrap
* **Author/Org**: SciPy Project
* **Date**: 2024
* **URL**: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html
* **Last updated**: 2024-09
* **Peer-reviewed**: no
* **Relevance**: API reference for the 95 % percentile-bootstrap CI used on per-angle firing-rate
  means. Establishes the `n_resamples`, `method`, and `vectorized` defaults the library uses.

### [MPL-Eventplot]

* **Type**: documentation
* **Title**: matplotlib.axes.Axes.eventplot
* **Author/Org**: Matplotlib Development Team
* **Date**: 2024
* **URL**: https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.eventplot.html
* **Last updated**: 2024-09
* **Peer-reviewed**: no
* **Relevance**: Primitive for raster plots. Accepts a list of 1-D arrays (one per trial) and draws
  vertical tick marks per spike — the exact shape of t0008's per-angle spike output.

### [MPL-GridSpec]

* **Type**: documentation
* **Title**: matplotlib.gridspec.GridSpec
* **Author/Org**: Matplotlib Development Team
* **Date**: 2024
* **URL**: https://matplotlib.org/stable/api/_as_gen/matplotlib.gridspec.GridSpec.html
* **Last updated**: 2024-09
* **Peer-reviewed**: no
* **Relevance**: Layout primitive for the 2-row raster+PSTH figure with a 3:1 height ratio and a
  shared x-axis.

### [MPL-Fill-Between]

* **Type**: documentation
* **Title**: matplotlib.axes.Axes.fill_between
* **Author/Org**: Matplotlib Development Team
* **Date**: 2024
* **URL**: https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.fill_between.html
* **Last updated**: 2024-09
* **Peer-reviewed**: no
* **Relevance**: Primitive for the bootstrap 95 % CI band on Cartesian tuning curves; takes the
  low/high arrays returned by `scipy.stats.bootstrap`.

### [NumPy-Argmax]

* **Type**: documentation
* **Title**: numpy.argmax
* **Author/Org**: NumPy Project
* **Date**: 2024
* **URL**: https://numpy.org/doc/stable/reference/generated/numpy.argmax.html
* **Peer-reviewed**: no
* **Relevance**: Used to compute the preferred-direction angle from the per-angle mean vector for
  the polar annotation arrow.

### [Pandas-ReadCSV]

* **Type**: documentation
* **Title**: pandas.read_csv
* **Author/Org**: pandas Project
* **Date**: 2024
* **URL**: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
* **Peer-reviewed**: no
* **Relevance**: Used by the loader helpers to read the t0004 and t0008 tuning-curve CSVs into typed
  DataFrames before plotting.
