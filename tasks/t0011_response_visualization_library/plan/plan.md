---
spec_version: "2"
task_id: "t0011_response_visualization_library"
date_completed: "2026-04-20"
status: "complete"
---
# Plan

## Objective

Build `tuning_curve_viz`, a reusable matplotlib library that turns standard-schema tuning-curve CSVs
into Cartesian, polar, multi-model overlay, and per-angle raster+PSTH PNG plots for every downstream
DSGC experiment in the project. Done means: the four plotting functions exist, a CLI wraps them,
smoke tests run cleanly against both the t0004 target curve and the t0008 simulated curve, seven
example PNGs ship with the library asset, and `verify_library_asset` passes.

## Task Requirement Checklist

Operative task text quoted verbatim from `task.json` `short_description` and `task_description.md`:

> **Name**: Response-visualisation library (firing rate vs angle graphs)
>
> **Short description**: Matplotlib-based library that turns tuning-curve CSVs into Cartesian +
> polar firing-rate-vs-angle plots, multi-model overlays, and per-angle raster-plus-PSTH panels,
> saved as PNG to images/.
>
> **Scope**: The library `tuning_curve_viz` exposes four plotting functions:
>
> 1. `plot_cartesian_tuning_curve(curve_csv, out_png, *, show_trials=True, target_csv=None)` —
>    firing rate (Hz) vs direction (deg). Shows per-trial points, mean line, and a 95% bootstrap
>    confidence band. Optional overlay of a target curve (dashed line) from t0004's
>    `target-tuning-curve`.
> 2. `plot_polar_tuning_curve(curve_csv, out_png, *, target_csv=None)` — classical polar plot with
>    the preferred direction annotated.
> 3. `plot_multi_model_overlay(curves_dict, out_png, *, target_csv=None)` — side-by-side Cartesian +
>    polar overlay of multiple models.
> 4. `plot_angle_raster_psth(spike_times_csv, out_png, *, angle_deg)` — per-trial spike raster above
>    a PSTH, one figure per angle.
>
> A CLI `tuning_curve_viz.cli` consumes a tuning-curve CSV path and produces all four plot types
> into an output directory.
>
> **Smoke tests**: (1) all four plot types against `target-tuning-curve`; (2) all four against the
> t0008 simulated curve; (3) a `plot_multi_model_overlay` combining both with the target as a dashed
> overlay. Each smoke test writes its PNG to the library asset's `files/` folder.
>
> **Expected outputs**: 1 library asset at `assets/library/tuning-curve-viz/` with `description.md`,
> `module_paths` -> `code/tuning_curve_viz/`, `test_paths` -> `code/tuning_curve_viz/test_*.py`, and
> example PNGs in `files/`.

Concrete requirements extracted:

* **REQ-1**: Implement `plot_cartesian_tuning_curve` with the exact signature above, including
  per-trial points, mean line, 95% bootstrap CI band, and optional dashed target overlay. Satisfied
  by Step 6, evidenced by two Cartesian PNGs (target, t0008) in
  `assets/library/ tuning-curve-viz/files/`.
* **REQ-2**: Implement `plot_polar_tuning_curve` with matplotlib polar defaults and a
  preferred-direction annotation. Satisfied by Step 6, evidenced by two polar PNGs in the asset
  folder.
* **REQ-3**: Implement `plot_multi_model_overlay` producing side-by-side Cartesian + polar subplots,
  capped at 6 models, with target curve always drawn dashed. Satisfied by Step 6, evidenced by one
  overlay PNG combining t0004 and t0008.
* **REQ-4**: Implement `plot_angle_raster_psth` with per-trial eventplot raster above a PSTH
  histogram, one figure per angle. Satisfied by Step 6, evidenced by two raster+PSTH PNGs in the
  asset folder.
* **REQ-5**: Provide a `tuning_curve_viz.cli` that consumes a tuning-curve CSV path and writes all
  four plot types into an output directory via `argparse`. Satisfied by Step 7, evidenced by
  `code/tuning_curve_viz/cli.py` plus a CLI smoke-test invocation log.
* **REQ-6**: Run smoke tests against both the t0004 target curve and the t0008 simulated curve, plus
  one combined overlay. Satisfied by Step 8 and Step 10, evidenced by all seven PNGs landing in the
  asset's `files/` folder.
* **REQ-7**: Package the work as one library asset at `assets/library/tuning-curve-viz/` with
  `details.json` (`module_paths` -> `code/tuning_curve_viz/`, `test_paths` ->
  `code/ tuning_curve_viz/test_*.py`), a `description.md` covering purpose, API, and example usage,
  and the example PNGs under `files/`. Satisfied by Step 11, evidenced by `verify_library_asset`
  passing with no errors.
* **REQ-8**: Answer the three questions posed by the task (does it run on the target, does it run on
  a real simulated curve, does the overlay align axes correctly across models with different angular
  sampling). Satisfied by the smoke-test suite executing cleanly across heterogeneous angle grids;
  evidenced in `results/results_detailed.md`.

## Approach

Implement `tuning_curve_viz` as a pure Python package under `code/tuning_curve_viz/`, built on
matplotlib + pandas + numpy + scipy. The research-code stage established that t0012's
`tuning_curve_loss.loader.load_tuning_curve` already handles all three accepted CSV schemas
(canonical `(angle_deg, trial_seed, firing_rate_hz)`, t0004 trials, t0004 mean) and returns a
`TuningCurve` dataclass with per-angle means and optional trial matrix. The viz library imports this
loader directly via library path
`tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader.load_tuning_curve`
rather than re-implementing CSV parsing — this eliminates ~150 lines of duplicated code and keeps
schema definitions in one place.

Research-internet established the four convention choices: (1) Okabe-Ito 8-colour CUD palette for
colour-blind-safe overlays, (2) matplotlib polar defaults `theta_direction=1, theta_offset=0`, (3)
`scipy.stats.bootstrap(n_resamples=1000, method="percentile", confidence_level=0.95)` for the CI
band, (4) `GridSpec(2, 1, height_ratios=[3, 1])` + `eventplot`
+ `hist` with 10 ms bins for raster+PSTH.

No spike-time CSV exists anywhere in the project (t0008 emits only firing rates), so the raster+PSTH
smoke test generates a deterministic synthetic Poisson fixture via `np.random.default_rng(seed=42)`
inside the smoke-test module — the fixture is test-only code and is never shipped as a library
asset.

**Alternatives considered**: (1) seaborn instead of matplotlib — rejected because seaborn adds a
heavy dependency for a narrow benefit (no seaborn primitive for raster+PSTH). (2) plotly for
interactive HTML output — rejected because the task explicitly requires PNG output only. (3)
Re-implementing a CSV loader here — rejected because t0012's loader is the authoritative
project-wide source of truth for the three CSV schemas.

**Task types**: `write-library`, matching `task.json`. Planning guidelines for library tasks
emphasise stable APIs, keyword-only optional parameters, and example PNGs in the asset.

## Cost Estimation

No external services, no remote compute, no paid APIs. Only local matplotlib, pandas, numpy, and
scipy computation running in under 30 seconds on any dev machine. Expected total cost: **$0.00**.
Project budget in `project/budget.json` is unaffected.

## Step by Step

1. **Write `code/tuning_curve_viz/__init__.py`** exposing the 4 plotting functions and the
   `OKABE_ITO` palette at the package level. Expected output:
   `from tasks.t0011_....code. tuning_curve_viz import plot_cartesian_tuning_curve` succeeds.
   Satisfies REQ-1, REQ-2, REQ-3, REQ-4.
2. **Write `code/tuning_curve_viz/constants.py`** — `OKABE_ITO` (8 hex codes), `DEFAULT_DPI = 150`,
   `MAX_OVERLAY_MODELS = 6`, `PSTH_BIN_WIDTH_S = 0.010`, `BOOTSTRAP_N_RESAMPLES = 1000`,
   `BOOTSTRAP_CONFIDENCE_LEVEL = 0.95`. Column names mirror t0012's `paths.py`. Satisfies REQ-1,
   REQ-2, REQ-3, REQ-4.
3. **Write `code/tuning_curve_viz/paths.py`** — repository-relative `Path` constants pointing at the
   t0004 target curve (`curve_mean.csv`, `curve_trials.csv`) and the t0008 simulated curve
   (`curve_modeldb_189347.csv`), plus output PNG paths under the library asset's `files/` directory.
   Used only by the smoke tests. Satisfies REQ-6.
4. **Write `code/tuning_curve_viz/loaders.py`** — thin wrappers around
   `tasks.t0012_....tuning_curve_loss.loader.load_tuning_curve`. Functions:
   `load_curve(path: Path) -> TuningCurve` (re-export) and
   `validate_angle_grid(angles: np.ndarray) -> None` (permissive: accept 8, 12, 16 uniform angles;
   raise on non-uniform). Satisfies REQ-1, REQ-2, REQ-3.
5. **Write `code/tuning_curve_viz/stats.py`** —
   `bootstrap_ci(per_angle_trials: np.ndarray) -> tuple[np.ndarray, np.ndarray]` using
   `scipy.stats.bootstrap` with the constants from step 2. Plus a 4-line NumPy fallback guarded by
   `try: import scipy` for the risk listed below. Returns `(ci_low, ci_high)`, one value per angle.
   Satisfies REQ-1.
6. **Write `code/tuning_curve_viz/cartesian.py`, `polar.py`, `overlay.py`, `raster_psth.py`** — one
   public plotting function per module with the exact signature from the task text. Each function
   calls `load_curve`, computes the bootstrap CI (cartesian, overlay) or finds the preferred
   direction (polar, overlay), draws the figure using Okabe-Ito colours and `DEFAULT_DPI`, and saves
   to `out_png`. Each function closes the figure with `plt.close(fig)` to prevent memory leaks in
   loops. Satisfies REQ-1, REQ-2, REQ-3, REQ-4.
7. **Write `code/tuning_curve_viz/cli.py`** with `argparse`: flags `--curve-csv` (required),
   `--target-csv` (optional), `--spike-times-csv` (optional), `--out-dir` (required). When
   `--spike-times-csv` is supplied, emits one raster+PSTH PNG per distinct `angle_deg`. Expected
   output: running the CLI on a sample CSV produces 3-4 PNGs in the output directory. Satisfies
   REQ-5.
8. **Write `code/tuning_curve_viz/test_smoke.py`** — a module (not pytest-discovered) that runs all
   four plot functions on both the t0004 target curve and the t0008 simulated curve, plus one
   overlay combining them, plus two per-angle raster+PSTH panels using a deterministic
   `np.random.default_rng(seed=42)` Poisson fixture. Writes outputs to
   `assets/library/tuning-curve-viz/files/`. Satisfies REQ-6, REQ-8.
9. **Run quality checks.** `uv run ruff check --fix . && uv run ruff format .` and
   `uv run mypy -p tasks.t0011_response_visualization_library.code`. Expected output: zero errors
   from both. Satisfies all REQs (quality gate).
10. **Run the smoke test.**
    `uv run python -u -m tasks.t0011_response_visualization_library. code.tuning_curve_viz.test_smoke`.
    Expected output: 7 PNGs land in `assets/library/tuning-curve-viz/files/` (2 cartesian + 2 polar
    \+ 1 overlay + 2 raster+PSTH). Satisfies REQ-6.
11. **Assemble the library asset.** Write `assets/library/tuning-curve-viz/details.json`
    (schema-conformant; `library_id: "tuning_curve_viz"`, `module_paths` listing every `.py` under
    `code/tuning_curve_viz/`, `test_paths` listing `code/tuning_curve_viz/test_*.py`, dependencies
    `numpy`, `pandas`, `matplotlib`, `scipy`, `tuning_curve_loss`) and `description.md` (purpose,
    API, example usage, CSV schema reference pointing at t0012). Run
    `uv run python -m arf.scripts.verificators.verify_library_asset t0011_response_visualization_library tuning-curve-viz`.
    Expected output: no errors, possibly zero warnings. Satisfies REQ-7.

## Remote Machines

None required — all matplotlib, pandas, numpy, and scipy work runs locally on any dev machine in
under 30 seconds. No GPU needed; no CUDA dependency in the library.

## Assets Needed

* `t0004_generate_target_tuning_curve` — `assets/dataset/target-tuning-curve/files/curve_mean. csv`
  and `curve_trials.csv` (read at runtime by the smoke tests for REQ-6).
* `t0008_port_modeldb_189347` — `data/tuning_curves/curve_modeldb_189347.csv` (read at runtime by
  the smoke tests for REQ-6).
* `tuning_curve_loss` library (from t0012) — imported at module load for `load_tuning_curve` and
  `TuningCurve` (REQ-1, REQ-2, REQ-3).

## Expected Assets

* **1 library asset** at
  `tasks/t0011_response_visualization_library/assets/library/ tuning-curve-viz/` containing
  `details.json` (with `module_paths` -> `code/tuning_curve_viz/`, `test_paths` ->
  `code/tuning_curve_viz/test_*.py`), `description.md` (purpose, API, example usage, CSV schema
  reference), and 7 example PNG files under `files/` demonstrating every plot type on real project
  data. This matches `"expected_assets": {"library": 1}` in `task.json`.

## Time Estimation

* Research (already done): 0 hours.
* Implementation (Steps 1-8): 2.5 hours wall-clock.
* Quality checks (Step 9): 0.25 hours.
* Smoke test (Step 10): 0.25 hours.
* Library asset assembly (Step 11): 0.5 hours.
* **Total**: ~3.5 hours wall-clock.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `scipy.stats.bootstrap` unavailable in env | Low | Blocks REQ-1 | Guard the scipy import; fall back to the 4-line NumPy percentile bootstrap already stubbed in `stats.py`. |
| Polar convention mismatch between matplotlib and tuning-curve convention (0° = east) | Medium | REQ-2 plots rotated incorrectly | Stick to matplotlib defaults `theta_direction=1, theta_offset=0` and document the convention in `description.md`; never transform input angles. |
| Overlay illegible with >6 models | Low | REQ-3 plots unreadable | `plot_multi_model_overlay` emits a `UserWarning` and truncates to 6 models with deterministic ordering by input dict key. |
| t0008 simulated curve schema drift | Low | REQ-6 smoke test fails | t0012's loader already handles all three schemas; any drift is caught at load time with a clear error rather than silently producing a wrong plot. |
| No real spike-time data exists in project | High | REQ-4 raster+PSTH cannot use real data | Smoke test synthesises a deterministic Poisson fixture via `np.random.default_rng(seed=42)`; emit a follow-up suggestion for a future task to record soma spike times from `modeldb_189347_dsgc`. |
| Figures leak memory in smoke-test loops | Low | Smoke test OOMs | Every plotting function calls `plt.close(fig)` before returning. |

## Verification Criteria

* File check: `ls tasks/t0011_response_visualization_library/code/tuning_curve_viz/` lists
  `__init__.py`, `constants.py`, `paths.py`, `loaders.py`, `stats.py`, `cartesian.py`, `polar.py`,
  `overlay.py`, `raster_psth.py`, `cli.py`, `test_smoke.py`. Confirms REQ-1 through REQ-5.
* Quality check:
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0011_response_visualization_library -- ruff check .`
  exits 0; same for `ruff format --check .` and
  `mypy -p tasks.t0011_response_visualization_library.code`. Confirms code quality.
* Smoke-test check: after running `test_smoke`,
  `ls tasks/t0011_response_visualization_library/ assets/library/tuning-curve-viz/files/*.png | wc -l`
  returns 7. Confirms REQ-6 and REQ-8.
* CLI check:
  `uv run python -m tasks.t0011_response_visualization_library.code. tuning_curve_viz.cli --curve-csv <t0008 csv> --out-dir /tmp/viz`
  writes at least 2 PNGs into `/tmp/viz/`. Confirms REQ-5.
* Library-asset verificator:
  `uv run python -m arf.scripts.verificators.verify_library_asset t0011_response_visualization_library tuning-curve-viz`
  prints "OK" with no errors. Confirms REQ-7.
* Requirements coverage check: `results/results_detailed.md` contains a section listing REQ-1
  through REQ-8 with a per-item status and a link or embedded PNG proving completion. Confirms REQ-8
  reporting.
