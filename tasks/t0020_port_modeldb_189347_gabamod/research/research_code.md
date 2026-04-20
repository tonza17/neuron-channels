# Research: Code Review of t0008 and t0012

## Objective

Identify exactly which functions, constants, and conventions from `t0008_port_modeldb_189347` and
`t0012_tuning_curve_scoring_loss_library` can be reused for the gabaMOD-swap protocol, and which
pieces must be written anew. The purpose is to keep the new library asset as thin a refactor over
the t0008 driver as possible: the cell, mechanisms, HOC sourcing, parameter application, and
spike-counting tail of `run_one_trial` are all shared; only the per-trial-condition setup and the
scoring-and-CSV layer change.

## Background

Suggestion S-0008-02 (raised by t0008's analysis step) flagged that the rotation-proxy DSI of
**0.316 / 18.1 Hz** falls well below the Poleg-Polsky & Diamond 2016 envelope (DSI 0.70-0.85, peak
40-80 Hz). The shortfall is not a porting bug — it is the consequence of substituting a spatial
BIP-coordinate rotation for the paper's native protocol, which holds geometry fixed and instead
swaps the inhibitory `gabaMOD` scalar between PD (0.33) and ND (0.99). This task implements a new
sibling library asset that drives the same NEURON cell under that native protocol so the project can
quote a fair reproduction number.

## Methodology Review

Reviewed five files in `tasks/t0008_port_modeldb_189347/code/` and four files in
`tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/`. Read the t0008 library
asset's `details.json` to understand the canonical entry-point layout. No code execution; this is a
static review.

## Key Findings

### Reuse from t0008

* `build_cell.py:build_dsgc()` — loads `nrnmech.dll`, sources `RGCmodel.hoc` and `dsgc_model.hoc`,
  places synapses via the HOC `placeBIP()` proc, and returns a fully initialized `h` handle. Reused
  verbatim by importing from `tasks.t0008_port_modeldb_189347.code.build_cell`.
* `build_cell.py:read_synapse_coords()` and `apply_params()` — read baseline coords (only needed
  to assert BIP `locx` does not change across PD/ND trials, per the Risks & Fallbacks section of the
  task description) and apply per-trial seed plus all canonical paper parameters. The existing
  `apply_params` already writes `h.gabaMOD = GABA_MOD` (= 0.33). The new driver overrides this
  Python-side global per condition.
* `build_cell.py:run_one_trial()` — cannot be reused as-is because it calls
  `rotate_synapse_coords_in_place()` and `reset_synapse_coords()`. The new driver inlines the
  spike-counting tail (vector recording, `finitialize` + `continuerun`, threshold-crossing count)
  and skips the rotation calls.
* `constants.py` — `TSTOP_MS=1000.0`, `AP_THRESHOLD_MV`, `V_INIT_MV`, `GABA_MOD=0.33`,
  `N_TRIALS=20` are all reused. Only one new constant is needed: `GABA_MOD_ND = 0.99`. The new
  library asset will not redefine the canonical paper parameters; it imports them.
* `paths.py` — the new task's `paths.py` will mirror the t0008 layout (TASK_ROOT, DATA_DIR,
  RESULTS_DIR, LIBRARY_ASSET_DIR pointing at `assets/library/modeldb_189347_dsgc_gabamod/`). No need
  to add new global constants.

### Reuse from t0012

* `tuning_curve_loss.compute_dsi()` and `compute_peak_hz()` — these operate on the `TuningCurve`
  dataclass (a 12-angle grid). Cannot be called directly because the gabaMOD-swap protocol produces
  only 2 conditions, not a 12-angle grid; the loader's `_validate_angle_grid` would reject the new
  CSV schema. Instead, the new scorer computes DSI by formula:
  `DSI = (mean_PD - mean_ND) / (mean_PD + mean_ND)` and `peak = mean_PD`.
* `tuning_curve_loss.envelope.check_envelope()` — could be invoked, but it expects the four-
  metric envelope (DSI, peak, null, HWHM). The two-point protocol has no null-direction angle and no
  HWHM. The new scorer implements its own two-point envelope check instead, with thresholds DSI in
  [0.70, 0.85] and peak in [40, 80] Hz, copied from the canonical published ranges (these are the
  same numerical bounds used by t0012's `DSI_ENVELOPE` and `PEAK_ENVELOPE_HZ` before t0012 widened
  them for its own identity test).
* `score_envelope.py` from t0008 — referenced as a layout template, not imported. The new scorer
  is small enough to live in a single file (`code/score_two_point.py`).

### What must be written

1. New library asset folder under
   `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/` with
   `details.json` (spec_version 2, library_id `modeldb_189347_dsgc_gabamod`, module_paths pointing
   at the new code/ files) and `description.md` (the canonical description document referenced via
   `description_path`).
2. `code/paths.py` — task-local path constants (TASK_ROOT, DATA_DIR, RESULTS_DIR, the new library
   asset dir, the new tuning_curves CSV path under `data/`, the score_report path).
3. `code/constants.py` — `GABA_MOD_PD = 0.33` and `GABA_MOD_ND = 0.99`,
   `N_TRIALS_PER_CONDITION = 20`, the two condition labels `CONDITION_PD = "PD"` and
   `CONDITION_ND = "ND"`, the two-point envelope bounds (`DSI_MIN`, `DSI_MAX`, `PEAK_MIN_HZ`,
   `PEAK_MAX_HZ`).
4. `code/run_gabamod_sweep.py` — top-level driver that builds the DSGC once, loops over
   `(condition, trial_seed)` pairs, sets `h.gabaMOD` to the condition's value, asserts BIP `locx`
   did not drift from its baseline, calls `apply_params` + `placeBIP` + `finitialize` +
   `continuerun`, counts spikes, and writes `data/tuning_curves.csv` with the new schema.
5. `code/score_two_point.py` — reads the CSV, computes mean firing rate per condition, derives DSI
   and peak, applies the two-point envelope gate, and writes `results/score_report.json` plus the
   comparison table fragment for `results_detailed.md`.
6. `code/generate_charts.py` — bar chart of mean firing rate by condition with per-trial scatter,
   saved to `results/images/firing_rate_by_condition.png`.
7. The new library asset's `description.md` — explains the gabaMOD-swap protocol, references t0008
   as the parent port, lists the new constants, and quotes the entry points.

### Cross-task import constraint

Per `CLAUDE.md` rule "tasks must not import from other tasks' `code/` directories ... the only
cross-task import mechanism is libraries (registered in `assets/library/`)". The t0008
`build_cell.py` is registered in t0008's library asset (`module_paths` in `details.json` lists
`code/build_cell.py`), so importing it as `tasks.t0008_port_modeldb_189347.code.build_cell` is
allowed — it goes through the registered library. The same applies to t0012's `tuning_curve_loss`
package.

## Recommended Approach

* Build a single new library asset `modeldb_189347_dsgc_gabamod` whose code is a thin wrapper over
  t0008's `build_dsgc()` + `apply_params()` + spike-counting tail. Write the new driver
  (`run_gabamod_sweep.py`), the new scorer (`score_two_point.py`), and the new charts
  (`generate_charts.py`) under `tasks/t0020_port_modeldb_189347_gabamod/code/`.
* Do not vendor a second copy of the HOC/MOD sources. The t0008 library asset's `sources/` directory
  and compiled `nrnmech.dll` under t0008's `build/` are reused via the path constants imported from
  t0008's `paths.py` (specifically, `MODELDB_BUILD_DIR` and `MODELDB_SOURCES_DIR` via the chain of
  imports inside t0008's `build_cell`).
* Compute DSI and peak in the new scorer by direct formula, avoiding the t0012 `score()` entry point
  because its loader requires a 12-angle grid that the two-point protocol does not produce. The DSI
  formula `(mean_PD - mean_ND) / (mean_PD + mean_ND)` is identical to what t0012's `compute_dsi`
  does internally.
* Add an explicit assertion in the driver that `h.RGC.BIPsyn[i].locx` equals
  `baseline[i].bip_locx_um` for every synapse on every trial — this guards against any latent
  reuse of the rotation logic if the imports drift.

## References

* `tasks/t0008_port_modeldb_189347/code/build_cell.py` — `build_dsgc`, `apply_params`,
  `run_one_trial`, `read_synapse_coords`, `rotate_synapse_coords_in_place`, `reset_synapse_coords`.
* `tasks/t0008_port_modeldb_189347/code/run_tuning_curve.py` — top-level driver template.
* `tasks/t0008_port_modeldb_189347/code/score_envelope.py` — scoring layer template.
* `tasks/t0008_port_modeldb_189347/code/constants.py` — `GABA_MOD`, `TSTOP_MS`, `AP_THRESHOLD_MV`,
  `N_TRIALS`.
* `tasks/t0008_port_modeldb_189347/code/paths.py` — `MODELDB_BUILD_DIR`, `MODELDB_SOURCES_DIR`,
  `DATA_DIR`, `RESULTS_DIR` layout.
* `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/details.json` — library
  asset layout to mirror.
* `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/__init__.py` — public API
  of the scorer library.
* `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/envelope.py` —
  `DSI_ENVELOPE`, `PEAK_ENVELOPE_HZ`, `check_envelope` reference; not directly invoked by the new
  scorer because the two-point protocol has no null/HWHM.
* `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/loader.py` —
  `_validate_angle_grid` confirms the 12-angle restriction that prevents direct use of the scorer's
  CSV path on the two-point CSV.
* `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/metrics.py` —
  `compute_dsi`, `compute_peak_hz` reference formulas (re-implemented inline in the new scorer for
  the two-point case).
