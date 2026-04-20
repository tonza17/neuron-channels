---
spec_version: "1"
task_id: "t0011_response_visualization_library"
research_stage: "code"
tasks_reviewed: 17
tasks_cited: 4
libraries_found: 2
libraries_relevant: 1
date_completed: "2026-04-20"
status: "complete"
---
# Research Code

## Task Objective

Survey previously completed tasks so the `tuning_curve_viz` library reuses existing CSV loaders and
schemas rather than reinventing them, and so the smoke tests plot real project data (t0004 target
curve, t0008 simulated curve) against a deterministic synthetic raster fixture generated locally.

## Library Landscape

Walking `tasks/*/assets/library/*/details.json` revealed 2 registered libraries. No
`aggregate_libraries.py` script exists in this project, so the filesystem walk is used as a direct
substitute.

* **`tuning_curve_loss`** (v0.1.0, created by [t0012]). Canonical 12-angle scorer — loss scalar
  over DSI/peak/null/HWHM residuals plus a `load_tuning_curve` CSV loader that already handles all
  three schemas this task cares about (canonical `(angle_deg, trial_seed, firing_rate_hz)`, t0004
  trials `(angle_deg, trial_index, rate_hz)`, t0004 mean `(angle_deg, mean_rate_hz)`). **Relevant.**
  Import via library path
  `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader.load_tuning_curve`.
* **`modeldb_189347_dsgc`** (v0.1.0, created by [t0008]). NEURON/HOC port of the Poleg-Polsky DSGC.
  Depends on `neuron` and runs full compartmental simulations. **Not relevant** —
  `tuning_curve_viz` never runs simulations; it only reads the CSV outputs.

Neither library has been corrected or replaced by a later task. Both are at spec version 2.

## Key Findings

### Canonical CSV schema is already fixed by t0012 and t0008

The canonical tuning-curve schema `(angle_deg, trial_seed, firing_rate_hz)` is the format used by
both t0008's `curve_modeldb_189347.csv` and t0012's primary loader entry point [t0008] [t0012].
t0012's `loader.py` also accepts the legacy t0004 schemas (`curve_trials.csv` with
`(angle_deg, trial_index, rate_hz)` and `curve_mean.csv` with `(angle_deg, mean_rate_hz)`) and folds
trials into per-angle means. The `tuning_curve_viz` library should inherit the same canonical schema
and reuse t0012's loader wherever possible.

### t0004 writes two files the viz library must support

[t0004] emits `assets/dataset/target-tuning-curve/files/curve_mean.csv` (columns
`angle_deg, mean_rate_hz`) and `curve_trials.csv` (columns `angle_deg, trial_index, rate_hz`). The
target-curve overlay on every multi-model plot reads `curve_mean.csv`. The bootstrap CI band on the
Cartesian plot needs the trial-level data, which t0012's loader handles natively.

### t0008 emits only firing rates — no spike times

[t0008] produces 8 angles × 8 trials = 64 rows in
`tasks/t0008_port_modeldb_189347/data/tuning_curves/curve_modeldb_189347.csv`, plus a
`smoke_test_single_angle.csv` with a single angle. **No spike-time CSV is produced.** The
raster+PSTH smoke test therefore cannot run against real simulated spike times; it must synthesise a
small Poisson fixture inside the smoke test with deterministic RNG seeding.

### 12-angle grid is the project convention

Both [t0004] and [t0008] use a 12-angle grid with 30° spacing (0, 30, 60, ..., 330). The
`tuning_curve_viz` functions should not hard-code 12 angles (the library must gracefully handle 8-,
12-, or 16-angle grids) but should default the polar-tick layout to multiples of 30° when the grid
is a divisor of 360°.

### Cross-task import rule

Per project rule, only libraries in `assets/library/` may be imported across tasks [t0008] [t0012].
t0012's loader is registered as the `tuning_curve_loss` library and is the authoritative source for
CSV parsing in this project. All other code (e.g., [t0004]'s one-off generator script) must be read
for schema reference only and never imported.

## Reusable Code and Assets

### `tuning_curve_loss.loader.load_tuning_curve`

* **Source**: `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/loader.py`
* **What it does**: Loads a CSV in any of the 3 supported schemas and returns a `TuningCurve`
  dataclass with `angles_deg: np.ndarray`, `firing_rates_hz: np.ndarray` (per-angle mean), and
  `trials: np.ndarray | None` of shape `(n_angles, n_trials)`.
* **Reuse method**: **import via library**. Path:
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader import load_tuning_curve, TuningCurve`.
* **Function signature**: `load_tuning_curve(path: Path) -> TuningCurve`
* **Adaptation needed**: none for the Cartesian and polar plots. For the multi-model overlay and the
  raster+PSTH, `tuning_curve_viz` defines its own thin wrappers around `load_tuning_curve` and adds
  a per-angle spike-times loader (new code — nothing exists to reuse).
* **Line count**: ~150 lines in the upstream loader; zero lines to copy.

### `tuning_curve_loss.paths` column-name constants

* **Source**: `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/paths.py`
* **What it does**: Defines `ANGLE_COLUMN`, `FIRING_RATE_COLUMN`, `TRIAL_SEED_COLUMN`,
  `TRIAL_INDEX_COLUMN`, `TRIAL_RATE_COLUMN`, `MEAN_RATE_COLUMN`, `N_ANGLES`, `ANGLE_STEP_DEG`.
* **Reuse method**: **import via library** (same path as loader).
* **Adaptation needed**: none. The viz library uses the same names so column references stay
  consistent across tasks.

### t0004 target curve CSV (data asset)

* **Source**:
  `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_mean.csv`
* **What it does**: Provides the canonical target tuning curve drawn as a dashed black overlay on
  every multi-model plot and exercised by two smoke-test plots.
* **Reuse method**: **read at runtime via path** (no Python import; not code reuse).

### t0008 simulated tuning-curve CSV (data asset)

* **Source**: `tasks/t0008_port_modeldb_189347/data/tuning_curves/curve_modeldb_189347.csv`
* **What it does**: Provides one concrete simulated tuning curve for the multi-model overlay and two
  single-curve smoke plots.
* **Reuse method**: **read at runtime via path**.

No spike-time assets exist anywhere in the project, so the raster+PSTH smoke test must generate a
synthetic spike-time fixture locally (see Lessons Learned below).

## Lessons Learned

* **Always import the upstream library rather than re-implementing a CSV loader**. [t0012] already
  absorbed every edge case of the t0004/t0008 schemas; re-implementing CSV parsing here would
  duplicate tests and silently diverge on future schema corrections.
* **Schema documentation lives in the library**. [t0012]'s `loader.py` docstring is the single
  source of truth for the three accepted CSV schemas. `tuning_curve_viz` should reference this
  docstring in `description.md` rather than restating the schema in yet another place.
* **Spike-time data is an unresolved gap**. Neither [t0004] nor [t0008] emits per-trial spike times.
  This task's raster+PSTH smoke test must generate a synthetic fixture; a future
  compartmental-simulation task that actually records soma spike times will be needed before the
  raster+PSTH plot can exercise real data. Emit a suggestion to that effect.
* **Library metadata conventions**: [t0008] and [t0012] use lowercase-underscore `library_id`
  (`modeldb_189347_dsgc`, `tuning_curve_loss`). Follow the same pattern: `tuning_curve_viz`.
* **12-angle grid is the project norm**. Hard-coded 12-angle assumptions exist in t0012's loader
  (`N_ANGLES = 12`, `ANGLE_STEP_DEG = 30`). The viz library must be more permissive — polar plots
  over 8 angles should still render — so `tuning_curve_viz` defines its own angle-validation logic
  rather than reusing t0012's `_validate_angle_grid`.

## Recommendations for This Task

1. **Import `tuning_curve_loss.loader.load_tuning_curve` and `TuningCurve`** instead of writing a
   new CSV loader. This eliminates ~150 lines of duplicated code and keeps the project's schema
   definitions in one place [t0012].
2. **Import `tuning_curve_loss.paths` column-name constants** for every `pd.read_csv` dtype spec and
   column reference [t0012].
3. **Do not import anything from t0008**. `modeldb_189347_dsgc` pulls in NEURON and runs simulations
   — `tuning_curve_viz` must remain a lightweight plotting-only dependency [t0008].
4. **Generate the raster+PSTH smoke-test fixture in-process** with a seeded `np.random.default_rng`
   so the smoke test remains deterministic and CI-friendly. The fixture is test-only code; do not
   ship a spike-time CSV in the library asset.
5. **Use `library_id = "tuning_curve_viz"`** (lowercase-underscore) to match the project's
   library-naming convention [t0008] [t0012].
6. **Emit a follow-up suggestion** for a future task that records per-angle soma spike times from
   the `modeldb_189347_dsgc` simulator, so the raster+PSTH plot can be exercised on real data.
7. **Do not reuse t0012's strict angle-grid validator** — the viz library must gracefully accept
   arbitrary uniform grids (8, 12, 16 angles) without raising. Implement a permissive validator in
   `tuning_curve_viz.loaders` instead [t0012].

## Task Index

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate canonical target angle-to-AP-rate tuning curve
* **Status**: completed
* **Relevance**: Produces the canonical target tuning curve CSVs (`curve_mean.csv`,
  `curve_trials.csv`) consumed by `tuning_curve_viz` as the dashed-black reference overlay on every
  multi-model plot and as a smoke-test input.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: Registers the `modeldb_189347_dsgc` library and emits the simulated tuning-curve
  CSV (`curve_modeldb_189347.csv`) consumed by `tuning_curve_viz` as a concrete model curve in the
  multi-model overlay and two single-curve smoke plots.

### [t0009]

* **Task ID**: `t0009_calibrate_dendritic_diameters`
* **Name**: Calibrate dendritic diameters for dsgc-baseline-morphology
* **Status**: completed
* **Relevance**: Out of scope for plotting but confirms the library-and-morphology asset pattern the
  `tuning_curve_viz` asset should follow — description.md + details.json + files/ layout.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: Registers the `tuning_curve_loss` library whose `loader.load_tuning_curve` and
  column-name constants are imported directly by `tuning_curve_viz`. This is the primary reusable
  dependency for this task.
