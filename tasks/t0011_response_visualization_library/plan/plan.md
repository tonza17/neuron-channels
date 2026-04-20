---
spec_version: "3"
task_id: "t0011_response_visualization_library"
date_created: "2026-04-20"
---

# Plan

## Objective

Build `tuning_curve_viz`, a reusable matplotlib library that turns standard tuning-curve CSVs into
Cartesian, polar, multi-model overlay, and per-angle raster+PSTH PNG plots for every downstream
DSGC experiment in the project.

## Approach

* Python package `tuning_curve_viz` under `code/`, with four top-level plotting functions, a thin
  CLI module, and the Okabe-Ito colour palette as a module-level constant.
* CSV loader helpers normalise both the t0004 and t0008 layouts into the canonical schema
  `(angle_deg, trial_seed, firing_rate_hz)`.
* 95 % bootstrap CI band via `scipy.stats.bootstrap` with 1 000 resamples.
* Polar axis uses matplotlib defaults (`theta_direction=1`, `theta_offset=0`); preferred direction
  annotated with a red arrow at the peak mean.
* Multi-model overlay caps at 6 models (Okabe-Ito minus black); target curve always drawn as a
  black dashed line.
* Raster+PSTH uses `GridSpec(2, 1, height_ratios=[3, 1])`; raster via `ax.eventplot`, PSTH via
  `ax.hist` with 10 ms bins.
* Smoke tests live in `code/tuning_curve_viz/test_smoke.py` and write PNG outputs to the library
  asset's `files/` folder so the asset demonstrates every plot type.

## Cost Estimation

No external services, no remote compute, no paid APIs. Local matplotlib runs only. Expected total
cost: **$0.00**.

## Step by Step

1. Write `code/tuning_curve_viz/__init__.py` exposing the 4 plotting functions and the palette.
2. Write `code/tuning_curve_viz/constants.py` — Okabe-Ito hex codes, default DPI (150), max overlay
   models (6), PSTH bin width (0.010 s).
3. Write `code/tuning_curve_viz/paths.py` — repository-relative paths to the t0004 target curve
   and the t0008 tuning curve (used only by smoke tests).
4. Write `code/tuning_curve_viz/loaders.py` — `load_canonical_curve`, `load_target_mean_curve`,
   `load_t0004_trials`. Each returns a typed pandas DataFrame.
5. Write `code/tuning_curve_viz/stats.py` — `bootstrap_ci` using scipy; small NumPy fallback
   function (unused by default).
6. Write `code/tuning_curve_viz/cartesian.py`, `polar.py`, `overlay.py`, `raster_psth.py` with one
   plotting function each. Each function takes paths and saves a PNG.
7. Write `code/tuning_curve_viz/cli.py` with `argparse`: `--curve-csv`, `--target-csv`,
   `--spike-times-csv`, `--out-dir`.
8. Write `code/tuning_curve_viz/test_smoke.py` — runs all four plot functions on both the target
   and t0008 curves, plus an overlay combining them, and writes outputs into the library asset's
   `files/` folder.
9. Run `uv run ruff check --fix . && uv run ruff format .` and
   `uv run mypy -p tasks.t0011_response_visualization_library.code`.
10. Run the smoke test: `uv run python -u -m
    tasks.t0011_response_visualization_library.code.tuning_curve_viz.test_smoke`.
11. Assemble the library asset (`details.json` + `description.md`) and run `verify_library_asset`.

## Remote Machines

None.

## Assets Needed

* `t0004_generate_target_tuning_curve` — `curve_mean.csv` and `curve_trials.csv`.
* `t0008_port_modeldb_189347` — `curve_modeldb_189347.csv`.

## Expected Assets

* 1 library asset: `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/`
  with `details.json`, `description.md`, and example output PNGs in `files/`.

## Time Estimation

3 - 4 hours wall-clock for implementation + smoke tests + asset packaging.

## Risks & Fallbacks

* **`scipy.stats.bootstrap` unavailable**: fall back to a 4-line NumPy bootstrap function already
  stubbed in `stats.py`.
* **Polar convention mismatch downstream**: convention is documented in `description.md`; the
  library never transforms input angles.
* **Overlay becomes illegible beyond 6 models**: `plot_multi_model_overlay` emits a `UserWarning`
  and truncates to 6 with a deterministic ordering of the input dict keys.

## Verification Criteria

* `verify_library_asset` passes with no errors.
* Smoke test writes 7 PNGs (Cartesian × 2, polar × 2, overlay × 1, raster+PSTH × 2) to the library
  asset's `files/` folder.
* `ruff check` and `mypy -p tasks.t0011_response_visualization_library.code` pass.
* `results/results_summary.md` and `results/results_detailed.md` embed at least one example PNG via
  the `![desc](images/file.png)` syntax.
