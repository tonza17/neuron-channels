---
spec_version: "1"
task_id: "t0020_port_modeldb_189347_gabamod"
research_stage: "code"
tasks_reviewed: 2
tasks_cited: 2
libraries_found: 2
libraries_relevant: 2
date_completed: "2026-04-20"
status: "complete"
---
# Research: Code Review of t0008 and t0012

## Task Objective

Implement suggestion S-0008-02 by building a new sibling library asset `modeldb_189347_dsgc_gabamod`
that drives the same NEURON DSGC cell as t0008's `modeldb_189347_dsgc` but uses the Poleg-Polsky &
Diamond 2016 native protocol — swapping the inhibitory `gabaMOD` scalar between PD (0.33) and ND
(0.99) — instead of t0008's spatial-rotation proxy. Identify reusable code and surface anything
new that must be written.

## Library Landscape

Two libraries were found via the library aggregator and both are directly relevant:

* **`modeldb_189347_dsgc`** (version 0.1.0) created by `[t0008]` — the Python-driven port of
  ModelDB 189347 with NEURON/HOC back-end, 12-angle drifting-bar tuning-curve runner, and envelope
  scoring. No corrections recorded. Import path: `tasks.t0008_port_modeldb_189347.code.build_cell`
  for cell-construction helpers and `tasks.t0008_port_modeldb_189347.code.constants` for the
  canonical paper parameters. Critical for this task — the new library reuses `build_dsgc`,
  `apply_params`, `read_synapse_coords`, and the spike-counting tail of `run_one_trial`.
* **`tuning_curve_loss`** created by `[t0012]` — DSI/peak/null/HWHM/RMSE scoring library with a
  4-metric envelope check. No corrections recorded. Import path:
  `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`. Relevant as a reference
  implementation for the DSI formula and envelope conventions, but the high-level `score()` entry
  point cannot be invoked on the two-condition CSV produced by this task because its loader's
  `_validate_angle_grid` requires 12 angles on a 30-degree grid.

## Key Findings

### Cell construction and HOC sourcing are fully reusable

`[t0008]` `build_cell.py:build_dsgc()` (47 lines) loads the compiled `nrnmech.dll`, sources
`RGCmodel.hoc` and `dsgc_model.hoc`, calls `init_sim() / init_active() / update()`, and resets
celsius/dt/tstop/v_init to the canonical values. The function returns a fully initialized `h` handle
with all three synapse arrays (`BIPsyn`, `SACinhibsyn`, `SACexcsyn`) populated by the HOC
`placeBIP()` proc. The new library imports it as-is — no change is needed because the gabaMOD-swap
protocol uses the same cell, the same mechanisms, and the same synapse layout as the rotation-proxy
port.

### `gabaMOD` is already exposed at the Python level

`[t0008]` `build_cell.py:apply_params()` writes `h.gabaMOD = GABA_MOD` (= 0.33) on every trial along
with the other paper parameters. This means the new driver can override `gabaMOD` per condition
simply by mutating the `h.gabaMOD` global between trials, with no need for a HOC patch. The Risks &
Fallbacks section of the task description anticipated this might require reaching into each
`inh_syn` object — that turns out to be unnecessary. The HOC point processes read the global on
every `placeBIP()` call.

### The rotation logic must be removed, not just bypassed

`[t0008]` `run_one_trial()` calls `rotate_synapse_coords_in_place()` and `reset_synapse_coords()`
around the spike-counting body. The new driver inlines the spike- counting body (vector recording,
`finitialize` + `continuerun`, threshold-crossing count) and omits both rotation calls. To make this
guarantee explicit and survive future refactors of t0008, the new driver also asserts on every trial
that `h.RGC.BIPsyn[i].locx == baseline[i].bip_locx_um` for all `i`. If the assertion ever fires, the
new protocol has been silently re-mixed with the rotation proxy.

### t0012 envelope numbers were widened; use literature values directly

`[t0012]` `envelope.py` documents that `DSI_ENVELOPE = (0.7, 0.9)` and
`PEAK_ENVELOPE_HZ = (30.0, 80.0)` are *widened* from the literature `(0.7, 0.85)` and `(40, 80)` so
that t0012's identity test `score(target, target).passes_envelope is True` holds on the canonical
t0004 target. This task's two-point gate uses the unwidened literature values `DSI in [0.70, 0.85]`
and `peak in [40, 80] Hz` directly, matching the Poleg-Polsky paper's quoted ranges. This decision
is documented in the new library's `description.md`.

### t0012 loader cannot consume the two-point CSV

`[t0012]` `loader.py:_validate_angle_grid` requires exactly 12 angles with 30-degree spacing and
raises `ValueError` otherwise. The new CSV has 2 rows of `(condition, trial_seed, firing_rate_hz)`
aggregated to 2 means; the loader would reject it on column-name detection alone (`condition` is not
in any supported schema). The new scorer therefore reads the CSV with `pandas.read_csv` directly and
computes DSI by formula `(mean_PD - mean_ND) / (mean_PD + mean_ND)` — the same formula t0012's
`compute_dsi` evaluates internally on the 12-angle grid.

## Reusable Code and Assets

* **Source**: `tasks/t0008_port_modeldb_189347/code/build_cell.py` (~360 lines). **What it does**:
  builds the DSGC cell and exposes per-trial helpers. **Reuse method**: import via library
  (registered in `modeldb_189347_dsgc` `details.json` `module_paths`). **Function signatures**:
  * `build_dsgc() -> h_handle` — sources HOC and returns initialized NEURON handle.
  * `read_synapse_coords(h) -> list[SynapseCoords]` — returns BIP/SACinhib/SACexc baseline coords.
  * `apply_params(h, *, seed: int) -> None` — applies canonical paper parameters and seeds the rNG
    streams.
  * `get_cell_summary(h) -> CellSummary` — returns `numsyn` and section counts for sanity logging.
    **Adaptation needed**: none for `build_dsgc`/`read_synapse_coords`/`get_cell_summary`. For
    `apply_params`, the new driver calls it as-is then overrides `h.gabaMOD` to the
    condition-specific value (PD=0.33 or ND=0.99) before `placeBIP()`. **Line count**: ~360 lines
    imported wholesale, no copy.
* **Source**: `tasks/t0008_port_modeldb_189347/code/constants.py`. **What it does**: canonical paper
  parameters (TSTOP_MS, V_INIT_MV, AP_THRESHOLD_MV, GABA_MOD, ACH_MOD, etc.). **Reuse method**:
  import via library. **Adaptation needed**: none. The new task's own `constants.py` adds two values
  (`GABA_MOD_ND = 0.99` and `N_TRIALS_PER_CONDITION = 20`) and the two-point envelope bounds,
  importing the rest from t0008.
* **Source**:
  `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/metrics.py:compute_dsi`.
  **What it does**: reference DSI formula on a 12-angle TuningCurve. **Reuse method**: not imported
  (CSV schema mismatch). Used as a formula reference; the new scorer re-implements
  `(mean_PD - mean_ND) / (mean_PD + mean_ND)` inline (5 lines).

## Lessons Learned

* `[t0008]` reached **DSI 0.316 / peak 18.1 Hz** under the rotation-proxy protocol — well below
  the published envelope. The post-mortem (recorded in suggestion S-0008-02) attributes this to the
  rotation substituting for the native gabaMOD swap; the cell, mechanisms, and parameters are
  otherwise correct. Lesson: when a port misses an envelope, distinguish between a porting bug (HOC
  sourcing, parameter mismatch) and a protocol mismatch (the wrong stimulus is being applied). The
  current task is the protocol fix.
* `[t0008]` `apply_params` re-seeds the RNG streams via `seed2` before every trial. Lesson:
  trial-level seed control must happen *before* `placeBIP()` so the synaptic-noise streams pick it
  up; the new driver follows the same ordering.
* `[t0012]` had to widen its envelope to make the identity test pass on the canonical target.
  Lesson: when borrowing envelope thresholds, distinguish between literature values and
  test-conformant values; this task uses literature values because the test does not need to pass
  the t0004 target.

## Recommendations for This Task

1. **Import `build_dsgc`, `read_synapse_coords`, `apply_params`, and `get_cell_summary` from
   `[t0008]`** via the registered library path. Do not copy them.
2. **Inline the spike-counting tail** of `run_one_trial` (vector recording, finitialize +
   continuerun, threshold-crossing count) into the new driver's per-trial body. Skip the rotation
   calls.
3. **Set `h.gabaMOD` per-condition immediately after `apply_params(h, seed=...)`** and before
   `placeBIP()` so the inhibitory point processes pick up the new scalar. Use 0.33 for PD, 0.99 for
   ND.
4. **Add a per-trial assertion** `h.RGC.BIPsyn[i].locx == baseline[i].bip_locx_um` to guarantee the
   rotation logic is not silently re-engaged.
5. **Compute DSI and peak by direct formula** in the new scorer; do not attempt to feed the
   two-condition CSV through `[t0012]` `score()`. Use literature envelope values DSI in
   `[0.70, 0.85]` and peak in `[40, 80]` Hz.
6. **Keep the new library asset's `details.json`** structurally identical to `[t0008]`'s
   (spec_version 2, module_paths, entry_points), substituting the new module names.
7. **Run 20 trials per condition** (40 total) for the canonical sweep — matches `[t0008]`'s
   `N_TRIALS = 20` and gives a per-condition standard error small enough to make the DSI estimate
   stable.

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 (Poleg-Polsky & Diamond 2016 ON-OFF DSGC)
* **Status**: completed
* **Relevance**: Provides the source HOC/MOD layout, the `build_dsgc` / `apply_params` /
  `run_one_trial` helpers, the canonical paper parameters, and the rotation-proxy baseline numbers
  used in this task's comparison note.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Build the tuning_curve_loss scoring library
* **Status**: completed
* **Relevance**: Provides the reference DSI/peak/null/HWHM formulas and the four-metric envelope
  conventions. The new scorer borrows the DSI formula but cannot use the high-level `score()` entry
  point because the two-point CSV does not satisfy the 12-angle loader contract.
