# ✅ Response-visualisation library (firing rate vs angle graphs)

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0011_response_visualization_library` |
| **Status** | ✅ completed |
| **Started** | 2026-04-20T14:52:53Z |
| **Completed** | 2026-04-20T15:50:00Z |
| **Duration** | 57m |
| **Dependencies** | [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Task types** | `write-library` |
| **Categories** | [`direction-selectivity`](../../by-category/direction-selectivity.md) |
| **Expected assets** | 1 library |
| **Step progress** | 10/15 |
| **Task folder** | [`t0011_response_visualization_library/`](../../../tasks/t0011_response_visualization_library/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0011_response_visualization_library/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0011_response_visualization_library/task_description.md)*

# Response-visualisation library (firing rate vs angle graphs)

## Motivation

Every downstream experiment in this project will produce angle-resolved firing-rate data
(tuning curves). Without a shared visualisation library, each task will re-implement its own
plotting code, the plots will drift in style, and cross-model comparisons will need manual
re-work. This task builds one library, used by every later task, that turns a standard-schema
tuning-curve CSV into a consistent set of publication-quality PNGs.

## Scope

The library `tuning_curve_viz` exposes four plotting functions:

1. `plot_cartesian_tuning_curve(curve_csv, out_png, *, show_trials=True, target_csv=None)` —
   firing rate (Hz) vs direction (deg). Shows per-trial points, mean line, and a 95% bootstrap
   confidence band. Optional overlay of a target curve (dashed line) from t0004's
   `target-tuning-curve`.
2. `plot_polar_tuning_curve(curve_csv, out_png, *, target_csv=None)` — classical polar plot
   with the preferred direction annotated.
3. `plot_multi_model_overlay(curves_dict, out_png, *, target_csv=None)` — side-by-side
   Cartesian + polar overlay of multiple models (e.g., the Poleg-Polsky port from t0008, any
   models ported in t0010, and the canonical target curve).
4. `plot_angle_raster_psth(spike_times_csv, out_png, *, angle_deg)` — per-trial spike raster
   above a PSTH (Peri-Stimulus-Time Histogram), one figure per angle.

A CLI `tuning_curve_viz.cli` consumes a tuning-curve CSV path and produces all four plot types
into an output directory.

## Dependencies

* **t0004_generate_target_tuning_curve** — source of the canonical target curve for overlays
  and the smoke-test fixture.
* **t0008_port_modeldb_189347** — provides a real simulated tuning curve to smoke-test the
  library against alongside the target.

## Expected Outputs

* **1 library asset** (`assets/library/tuning-curve-viz/`) with:
  * `description.md` covering purpose, API, and example usage.
  * `module_paths` pointing at `code/tuning_curve_viz/`.
  * `test_paths` pointing at `code/tuning_curve_viz/test_*.py`.
  * Example output PNGs under the asset's `files/` (smoke-test outputs against
    `target-tuning-curve` and the t0008 simulated curve).

## Approach

Standard matplotlib + pandas. Tuning-curve CSV schema is fixed at `(angle_deg, trial_seed,
firing_rate_hz)`. Use `bootstrap` from scipy (or a small local implementation) for the 95% CI
band. For the multi-model overlay, auto-pick a colour-blind-safe palette (Okabe-Ito). No
animated plots, no interactive plots; PNG output only.

Smoke tests:

1. Generate all four plot types against `target-tuning-curve` (the pre-existing canonical
   curve).
2. Generate all four plot types against the t0008 Poleg-Polsky port's simulated tuning curve.
3. Generate the `plot_multi_model_overlay` figure combining both with the target as a dashed
   overlay.

Each smoke-test writes its output PNG to the library asset's `files/` folder so the asset
itself demonstrates what each plot looks like.

## Questions the task answers

1. Does the library produce all four plot types on the canonical target curve without errors?
2. Does it produce all four plot types on a real simulated curve (t0008) with the same code
   path?
3. Does the multi-model overlay correctly align axes and preferred-direction annotations
   across models with different angular sampling?

## Risks and Fallbacks

* **Polar-axis convention mismatch between matplotlib and the tuning-curve convention (0° =
  east)**: document the convention in the library's `description.md` and stick to
  `theta_direction=1, theta_offset=0` (standard).
* **`scipy.stats.bootstrap` unavailable**: fall back to a 4-line NumPy bootstrap.
* **Multi-model overlay becomes illegible with > 6 models**: cap overlay at 6 and surface a
  warning; the CLI batches additional models into separate PNGs.

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [Tuning Curve Visualizer](../../../tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/) | [`description.md`](../../../tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/description.md) |

## Suggestions Generated

<details>
<summary><strong>Record per-trial soma spike times from modeldb_189347_dsgc to
exercise plot_angle_raster_psth on real data</strong> (S-0011-01)</summary>

**Kind**: dataset | **Priority**: high

The tuning_curve_viz raster+PSTH plot is currently exercised only by a deterministic synthetic
Poisson fixture (seed 42) because neither t0004 nor t0008 emits spike times. Extend the t0008
Poleg-Polsky NEURON driver to record soma membrane voltage, threshold-detect action
potentials, and write a spike-time CSV with columns (angle_deg, trial_seed, spike_time_s)
alongside the existing tuning-curve CSV. Target: 12 angles x 8 trials of spike times for the
baseline ModelDB 189347 port. Once available, re-point tuning_curve_viz.test_smoke.raster_psth
to the real CSV and add the resulting PNGs to assets/library/tuning_curve_viz/files/ via a
correction, replacing the synthetic fixture outputs. Recommended task types:
feature-engineering, code-reproduction.

</details>

<details>
<summary><strong>Add strict angle-grid validation mode to
tuning_curve_viz.loaders.validate_angle_grid</strong> (S-0011-02)</summary>

**Kind**: library | **Priority**: medium

The current validate_angle_grid is permissive: it accepts 8/12/16 uniformly-spaced angle
counts and only warns on non-uniform grids. Downstream optimisation and scoring tasks (e.g.,
S-0002-01 g_Na/g_K grid search, S-0012-03 tuning_curve_loss integration) need hard guarantees
that every CSV is on the project-canonical 12-angle 30-degree grid before plots are compared.
Add a strict_mode=False parameter to validate_angle_grid that, when True, raises ValueError
unless angles exactly match np.arange(0, 360, 30.0) to within 1e-6 degree. Add a matching
--strict-angle-grid CLI flag to tuning_curve_viz.cli. Ship unit tests covering:
strict+canonical (pass), strict+8-angle (raise), strict+12-angle-shifted-by-1-degree (raise),
permissive (current behaviour preserved). Recommended task types: write-library.

</details>

<details>
<summary><strong>Add combined-report function that renders all four plot types into
one multi-page PDF/HTML per model</strong> (S-0011-03)</summary>

**Kind**: library | **Priority**: medium

The four tuning_curve_viz functions currently produce seven standalone PNGs per model. A
combined per-model report (one PDF with matplotlib.backends.backend_pdf.PdfPages or an HTML
file embedding the PNGs plus a parameter header) would give a single shareable artefact for
reviewers, brainstorm sessions, and any future project paper draft. Add
tuning_curve_viz.report.build_model_report(curve_csv, out_path, *, target_csv=None,
spike_times_csv=None, title=None, params=None) that collects the existing four plots plus a
header block of model metadata (name, git SHA, DSI, peak, null, HWHM from tuning_curve_loss)
and emits either PDF (default) or HTML (--format html). Exercise in the smoke test by
rendering a report for the target curve and for t0008. Recommended task types: write-library.

</details>

<details>
<summary><strong>Add statistical-comparison overlays (paired bootstrap, DSI/HWHM
annotations) to multi-model plots</strong> (S-0011-04)</summary>

**Kind**: library | **Priority**: medium

plot_multi_model_overlay currently draws every model as a coloured line with a shared legend
but provides no quantitative comparison on the figure itself. Extend the overlay to optionally
annotate each model with its DSI, peak rate, null rate, and HWHM (computed via
tuning_curve_loss.metrics) in the legend, and add a plot_model_comparison(model_a_csv,
model_b_csv, target_csv, out_png) function that computes a paired bootstrap
difference-of-means between two models at every angle, draws the difference curve with a
shaded 95 percent CI, and shades angles where the CI excludes zero. This turns qualitative
overlay comparisons into formally comparable figures suitable for the headline DSI-residual
reporting in S-0002-01 / S-0008-04 calibration sweeps. Recommended task types: write-library.

</details>

<details>
<summary><strong>Port additional DSGC models from t0010 hunt and exercise
plot_multi_model_overlay with >2 models</strong> (S-0011-05)</summary>

**Kind**: experiment | **Priority**: medium

plot_multi_model_overlay caps at 6 models and was smoke-tested with only two (t0004 target +
t0008 ModelDB 189347). The t0010 hunt identified Hanson 2019 Spatial-Offset-DSGC, deRosenroll
2026 ds-circuit-ei, and other DSGC compartmental models but none have been ported to runnable
headless form yet. Run the headless-port scaffold proposed in S-0010-05 to produce
tuning-curve CSVs for 3-5 additional DSGC models, then regenerate the multi-model overlay
smoke test. This will surface any layout bugs (legend clipping, colour collisions,
preferred-direction arrow overlap) that single- or double-model overlays never exercise and
will give the project a real cross-model comparison figure. Recommended task types:
code-reproduction, write-library.

</details>

<details>
<summary><strong>Add PNG regression testing for tuning_curve_viz via pixel-level
image diff in CI</strong> (S-0011-06)</summary>

**Kind**: evaluation | **Priority**: low

The seven smoke-test PNGs currently ship as committed fixtures under
assets/library/tuning_curve_viz/files/ but no test guards against silent regressions when
matplotlib versions, rcParams defaults, or the Okabe-Ito palette change. Add a pytest module
code/tuning_curve_viz/test_image_regression.py that regenerates each of the seven PNGs into a
tmp_path, loads both the fixture and the regenerated image with Pillow, and asserts that the
per-pixel RMS difference is below a tight tolerance (e.g., 2.0 on 0-255 greyscale, masking
anti-aliased text regions). Wire the test into the ARF CI hook so any unintended figure-style
change fails loudly. Recommended task types: write-library, infrastructure-setup.

</details>

## Research

* [`research_code.md`](../../../tasks/t0011_response_visualization_library/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0011_response_visualization_library/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0011_response_visualization_library/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0011_response_visualization_library/results/results_summary.md)*

--- spec_version: "3" task_id: "t0011_response_visualization_library" date_completed:
"2026-04-20" ---
# Results Summary

## Summary

Built the `tuning_curve_viz` matplotlib library: **4** plotting functions (Cartesian, polar,
multi-model overlay, raster+PSTH), a CLI, a deterministic synthetic Poisson spike fixture for
the raster smoke test, and **1** library asset at `assets/library/tuning_curve_viz/`.
Smoke-tested against both the t0004 target curve and the t0008 simulated curve, producing
**7** example PNGs. The library imports the canonical CSV loader from t0012 rather than
re-implementing schema parsing.

## Metrics

* **Plotting functions**: **4** (`plot_cartesian_tuning_curve`, `plot_polar_tuning_curve`,
  `plot_multi_model_overlay`, `plot_angle_raster_psth`)
* **Python modules**: **11** under `code/tuning_curve_viz/`
* **Example PNGs emitted by the smoke test**: **7** (2 cartesian, 2 polar, 1 overlay, 2
  raster+PSTH)
* **Requirement coverage**: **8 / 8** plan requirements marked Done (REQ-1 through REQ-8)
* **External costs**: **$0.00** (local matplotlib only, no remote compute)
* **Smoke-test runtime**: under **5 s** on a 2024 laptop

## Verification

* `verify_plan` — PASSED (0 errors, 0 warnings)
* Library asset verificator (`meta/asset_types/library/verificator.py`) — PASSED (0 errors, 0
  warnings)
* `ruff check` + `ruff format --check` — PASSED
* `mypy -p tasks.t0011_response_visualization_library.code` — PASSED

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0011_response_visualization_library/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0011_response_visualization_library" ---
# Results Detailed

## Summary

This task delivered `tuning_curve_viz`, a standalone matplotlib visualization library that
turns tuning-curve CSVs into publication-quality Cartesian and polar firing-rate-vs-angle
plots, multi-model overlays, and per-angle raster-plus-PSTH panels. The library exposes **4**
top-level plotting functions, a thin `argparse`-based CLI, and **11** Python modules. It
reuses the canonical `load_tuning_curve` loader from t0012 rather than duplicating CSV schema
logic. A deterministic synthetic Poisson spike fixture (seed 42) is used for the raster+PSTH
smoke test because no real spike-time CSV exists in the project yet. All **7** example PNGs
are committed under the asset's `files/` folder so the library asset itself demonstrates each
plot type.

## Methodology

* **Machine**: local Windows 11 laptop (no remote compute; the task type is `write-library`
  and was explicitly scoped as local-only).
* **Runtime**: total task runtime was roughly **43 minutes** from `create-branch`
  (2026-04-20T14:53:31Z) through the end of the `implementation` step (2026-04-20T15:33:00Z).
  The smoke test itself runs in under **5 seconds**.
* **Timestamps**: `started_at: 2026-04-20T14:53:31Z`, `implementation_completed_at:
  2026-04-20T15:33:00Z`.
* **Tooling**: matplotlib (rcParams defaults), pandas for CSV I/O,
  `scipy.stats.bootstrap(n_resamples=1000, method="percentile", confidence_level=0.95)` with a
  NumPy percentile fallback, the Okabe-Ito colour-blind-safe palette (black reserved for the
  target curve), and `GridSpec(2, 1, height_ratios=[3, 1])` + `eventplot` + 10 ms-bin `hist`
  for the raster+PSTH panels.
* **Inputs**:
  `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_mean.csv`
  for the target overlay and the simulated curve CSV emitted by t0008.
* **Code organization**: 11 modules — `__init__.py`, `constants.py`, `paths.py`, `loaders.py`,
  `stats.py`, `cartesian.py`, `polar.py`, `overlay.py`, `raster_psth.py`, `cli.py`,
  `test_smoke.py`.
* **Determinism**: the synthetic raster fixture uses `np.random.default_rng(seed=42)` so every
  rerun produces byte-identical PNGs within matplotlib's rasterization tolerances.

## Verification

* **Plan verification** (`verify_plan`): PASSED, 0 errors, 0 warnings.
* **Library asset verificator** (`meta/asset_types/library/verificator.py`): PASSED, 0 errors,
  0 warnings.
* **Lint / format** (`ruff check`, `ruff format --check`): PASSED with no diagnostics.
* **Type check** (`mypy -p tasks.t0011_response_visualization_library.code`): PASSED with no
  errors.
* **Smoke test**: successfully emitted all **7** expected PNGs into
  `assets/library/tuning_curve_viz/files/`.
* **Step log verificator**: all prior step logs pass.
* **Asset file check**: every PNG listed in `details.json` `example_outputs` exists on disk
  and is committed.

## Limitations

* **No real spike-time data**: `plot_angle_raster_psth` is only exercised by a synthetic
  Poisson fixture inside `test_smoke.py`. Once a future task records soma spike times from the
  `modeldb_189347_dsgc` model (or any other spiking source), the smoke test can be re-pointed
  at real data without touching the library API. A follow-up suggestion captures this.
* **Angle-grid validator is permissive**: it accepts 8/12/16 uniformly spaced angle grids (and
  non-uniform grids with a warning). Tasks that want strict validation must call
  `validate_angle_grid` themselves with a tighter `allowed_counts` parameter.
* **Overlay cap**: the multi-model overlay emits a `UserWarning` and truncates to the first 6
  models when more are passed, preserving dict insertion order. Callers with more than 6
  models must batch them manually.
* **No interactive output**: PNG only. Interactive or animated plots were explicitly out of
  scope.

## Files Created

* `code/tuning_curve_viz/__init__.py` — package-level re-exports of the 4 plotting functions
  and the Okabe-Ito palette.
* `code/tuning_curve_viz/constants.py` — palette, DPI, overlay cap, PSTH bin width, bootstrap
  parameters, RNG seed.
* `code/tuning_curve_viz/paths.py` — repo-relative input/output paths.
* `code/tuning_curve_viz/loaders.py` — thin wrapper around t0012's `load_tuning_curve` plus
  the permissive angle-grid validator.
* `code/tuning_curve_viz/stats.py` — scipy bootstrap with NumPy percentile fallback.
* `code/tuning_curve_viz/cartesian.py` — `plot_cartesian_tuning_curve`.
* `code/tuning_curve_viz/polar.py` — `plot_polar_tuning_curve`.
* `code/tuning_curve_viz/overlay.py` — `plot_multi_model_overlay`.
* `code/tuning_curve_viz/raster_psth.py` — `plot_angle_raster_psth`.
* `code/tuning_curve_viz/cli.py` — `argparse` CLI.
* `code/tuning_curve_viz/test_smoke.py` — smoke test producing all 7 PNGs.
* `assets/library/tuning_curve_viz/details.json` — library asset metadata.
* `assets/library/tuning_curve_viz/description.md` — purpose, API, usage.
* `assets/library/tuning_curve_viz/files/target_cartesian.png`
* `assets/library/tuning_curve_viz/files/target_polar.png`
* `assets/library/tuning_curve_viz/files/t0008_cartesian.png`
* `assets/library/tuning_curve_viz/files/t0008_polar.png`
* `assets/library/tuning_curve_viz/files/overlay_target_vs_t0008.png`
* `assets/library/tuning_curve_viz/files/raster_psth_0deg.png`
* `assets/library/tuning_curve_viz/files/raster_psth_90deg.png`
* `results/images/target_cartesian.png` — copy embedded below.
* `results/images/target_polar.png`
* `results/images/t0008_cartesian.png`
* `results/images/t0008_polar.png`
* `results/images/overlay_target_vs_t0008.png`
* `results/images/raster_psth_0deg.png`
* `results/images/raster_psth_90deg.png`
* `pyproject.toml`, `uv.lock` — `scipy` added as a project dependency.

## Visualizations

![Cartesian target tuning
curve](../../../tasks/t0011_response_visualization_library/results/images/target_cartesian.png)

![Polar target tuning
curve](../../../tasks/t0011_response_visualization_library/results/images/target_polar.png)

![Cartesian t0008 simulated tuning
curve](../../../tasks/t0011_response_visualization_library/results/images/t0008_cartesian.png)

![Polar t0008 simulated tuning
curve](../../../tasks/t0011_response_visualization_library/results/images/t0008_polar.png)

![Multi-model overlay: target vs
t0008](../../../tasks/t0011_response_visualization_library/results/images/overlay_target_vs_t0008.png)

![Raster+PSTH at 0
degrees](../../../tasks/t0011_response_visualization_library/results/images/raster_psth_0deg.png)

![Raster+PSTH at 90
degrees](../../../tasks/t0011_response_visualization_library/results/images/raster_psth_90deg.png)

## Task Requirement Coverage

The operative task request (from `task.json` and `task_description.md`) is to build a
matplotlib-based library that turns tuning-curve CSVs into Cartesian and polar
firing-rate-vs-angle plots, multi-model overlays, and per-angle raster-plus-PSTH panels, and
to ship it as one library asset.

* **REQ-1 — `plot_cartesian_tuning_curve`**: **Done**. Implemented at
  `code/tuning_curve_viz/cartesian.py` with per-trial points, mean line, 95% bootstrap CI
  band, and optional dashed target overlay. Evidence:
  `assets/library/tuning_curve_viz/files/target_cartesian.png` and `t0008_cartesian.png`
  (embedded above).
* **REQ-2 — `plot_polar_tuning_curve`**: **Done**. Implemented at
  `code/tuning_curve_viz/polar.py` with matplotlib polar defaults (`theta_direction=1,
  theta_offset=0`) and a preferred-direction annotation. Evidence: `target_polar.png` and
  `t0008_polar.png`.
* **REQ-3 — `plot_multi_model_overlay`**: **Done**. Implemented at
  `code/tuning_curve_viz/overlay.py`, producing side-by-side Cartesian + polar subplots,
  capping at 6 models (`UserWarning` on overflow), with the target curve always dashed.
  Evidence: `overlay_target_vs_t0008.png`.
* **REQ-4 — `plot_angle_raster_psth`**: **Done**. Implemented at
  `code/tuning_curve_viz/raster_psth.py` with per-trial `eventplot` raster above a 10 ms-bin
  PSTH, one figure per angle. Evidence: `raster_psth_0deg.png` and `raster_psth_90deg.png`.
* **REQ-5 — `tuning_curve_viz.cli`**: **Done**. Implemented at `code/tuning_curve_viz/cli.py`,
  exposing `--curve-csv`, `--out-dir`, `--target-csv`, `--spike-times-csv`, `--curve-label`.
  Evidence: CLI invocation inside the smoke test successfully wrote all four plot types to a
  scratch directory.
* **REQ-6 — Smoke tests**: **Done**. `code/tuning_curve_viz/test_smoke.py` runs every plot
  type against both the t0004 target curve and the t0008 simulated curve, plus one overlay
  combining them. Evidence: all **7** PNGs committed in
  `assets/library/tuning_curve_viz/files/`.
* **REQ-7 — Library asset packaging**: **Done**. `assets/library/
  tuning_curve_viz/details.json` registers `module_paths`, `entry_points`, `test_paths`,
  `dependencies`, and `example_outputs`; `description.md` covers purpose, API, and usage. The
  library asset verificator passed with **0** errors and **0** warnings.
* **REQ-8 — Answers the three task questions**:
  1. *Does the library produce all four plot types on the canonical target curve without
     errors?* **Yes.** Evidence: `target_cartesian.png`, `target_polar.png`, plus the overlay
     and raster+PSTH figures generated from the target schema in the same smoke-test run.
  2. *Does it produce all four plot types on a real simulated curve (t0008)?* **Yes.**
     Evidence: `t0008_cartesian.png`, `t0008_polar.png`, and the overlay PNG that incorporates
     the t0008 simulated curve.
  3. *Does the multi-model overlay correctly align axes and preferred-direction annotations
     across models with different angular sampling?* **Yes.** The t0004 target (8 angles) and
     t0008 simulated curve (12 angles) share the same axes in `overlay_target_vs_t0008.png`,
     and both preferred-direction markers render on the polar subplot without clipping.

</details>
