---
spec_version: "1"
task_id: "t0024_port_de_rosenroll_2026_dsgc"
research_stage: "code"
tasks_reviewed: 6
tasks_cited: 6
libraries_found: 5
libraries_relevant: 3
date_completed: "2026-04-21"
status: "complete"
---
# Research Code: Port de Rosenroll 2026 DSGC

## Task Objective

Port the de Rosenroll et al. 2026 DSGC model into the project as a new library asset (proposed slug
`de_rosenroll_2026_dsgc`) following the HOC/MOD/morphology layout established by t0008, run the
canonical 12-angle moving-bar tuning-curve sweep against the t0004 target envelope, and compare
results against the existing Poleg-Polsky lineage (`modeldb_189347_dsgc` and siblings) and the
Hanson 2019 sibling. This is a third, structurally independent NEURON DSGC implementation that
should exercise more recent channel formulations (Nav1.6/Nav1.2 AIS split, modern Kv/Cav
mechanisms).

## Library Landscape

Five libraries are registered across prior tasks (enumerated by walking `tasks/*/assets/library/`
because no `aggregate_libraries.py` aggregator is wired in yet):

* **`modeldb_189347_dsgc`** (v0.1.0, created by [t0008]) — the reference HOC/MOD/morphology
  skeleton. Ships `code/build_cell.py` (NEURON bootstrap, DLL load, HOC sourcing, `build_dsgc`,
  `apply_params`, `run_one_trial`), `code/run_tuning_curve.py` (12 x 20 canonical sweep),
  `code/score_envelope.py` (t0012 scoring glue), `code/swc_io.py` (SWC parse/validate/write), and
  `sources/` with the ModelDB 189347 MOD/HOC files (`HHst.mod`, `SAC2RGCexc.mod`,
  `SAC2RGCinhib.mod`, `bipolarNMDA.mod`, `SquareInput.mod`, `spike.mod`, `RGCmodel.hoc`,
  `dsgc_model.hoc`, `nrnmech.dll` on Windows). Import path:
  `tasks.t0008_port_modeldb_189347.code.build_cell`. **Highly relevant** — the HOC-sourcing and
  per-trial loop pattern transfers directly.
* **`tuning_curve_loss`** (v0.1.0, [t0012]) — canonical scorer consuming a 12-angle CSV and
  returning a `ScoreReport` with DSI/peak/null/HWHM/RMSE/reliability. Import path:
  `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`. Exposes `score`,
  `score_curves`, `load_tuning_curve`, `compute_dsi`, `compute_hwhm_deg`, `check_envelope`, plus
  metric-key constants (`METRIC_KEY_DSI`, `METRIC_KEY_HWHM`, `METRIC_KEY_RELIABILITY`,
  `METRIC_KEY_RMSE`). **Highly relevant** — this is exactly the deliverable scorer.
* **`modeldb_189347_dsgc_gabamod`** (v0.1.0, [t0020]) — sibling port using the paper's native
  gabaMOD PD/ND parameter swap (PD=0.33, ND=0.99). Reference pattern for parameter-swap drivers, but
  built for a 2-condition schema (not 12-angle), so its driver is **not** the right template for
  t0024. **Moderately relevant** as a precedent.
* **`modeldb_189347_dsgc_dendritic`** (v0.1.0, [t0022]) — 12-angle moving-bar driver with per-
  dendrite AMPA/GABA_A `Exp2Syn` pairs driven by NetStim bursts and a channel-modular AIS partition
  (`dsgc_channel_partition.hoc`). **Highly relevant** — this is the closest match to what t0024
  needs. Note its `code/` is in the task folder, not wrapped as an importable Python module inside
  `assets/library/`, so cross-task reuse requires copy-in.
* **`tuning_curve_viz`** (v0.1.0, [t0011]) — Cartesian, polar, multi-model overlay, and
  raster+PSTH plotters for tuning-curve CSVs. **Optionally relevant** for the `results/images/`
  deliverable.

All aggregator output is the raw library state; no correction overlays touch these libraries.

## Key Findings

### HOC/MOD skeleton and port layout

[t0008] establishes the canonical layout every NEURON port follows: ModelDB sources are dropped
verbatim into `assets/library/<slug>/sources/`, compiled in place with `nrnivmodl` via the
`run_nrnivmodl.cmd` Windows wrapper, and the resulting `nrnmech.dll` is loaded through
`h.nrn_load_dll` before any `h.load_file(...)` HOC import. `build_cell.py` (358 lines) wraps the
whole boot sequence: `load_neuron()` sets `NEURONHOME`, loads the DLL, sources `stdrun.hoc`;
`build_dsgc()` calls `h.chdir` on the sources dir using forward slashes (HOC parser treats `\` as an
escape character on Windows), then loads `RGCmodel.hoc` and the GUI-stripped `dsgc_model.hoc`, then
fires `init_sim()` / `init_active()` / `update()`. `apply_params(h, seed=...)` then sets
`celsius=32`, `dt=0.1`, `tstop=1000`, `v_init=-65`, synaptic conductances, and the HHst
`vshift_HHst` — the 30-parameter canonical block is already defined in `code/constants.py`.
[t0020] reuses this skeleton unchanged (library import of `build_dsgc`, `apply_params`,
`read_synapse_coords`, `SynapseCoords`). [t0022] also imports the same `build_cell` module and only
adds an extra HOC overlay (`dsgc_channel_partition.hoc`) on top. The de Rosenroll port will not
reuse this library verbatim because it is a different model with different channel files, but the
exact same layout (`sources/` + `build_cell.py` + `code/run_nrnivmodl.cmd`) is the right pattern.

### Driver evolution for 12-angle moving-bar sweeps

The project has now iterated the moving-bar driver three times. [t0008] drives direction selectivity
via **spatial rotation** of BIP synapse `(locx, locy)` around the soma while SAC coordinates stay
fixed (see `rotate_synapse_coords_in_place` at `build_cell.py:211-263`). Each trial calls
`apply_params` -> `rotate_synapse_coords_in_place` -> `h("update()")` -> `h("placeBIP()")` ->
`h.finitialize` -> `h.continuerun(1000 ms)` -> count rising threshold crossings at -10 mV at the
soma. This hit DSI 0.316 / peak 18.1 Hz — under target because rotation is a proxy for the paper's
native per-angle gabaMOD swap. [t0020] rewrote the driver as a 2-condition (PD, ND) protocol that
overrides `h.gabaMOD` to 0.33 vs 0.99 after `apply_params`; this reached DSI 0.7838 / peak 14.85 Hz.
[t0022] then moved to a fundamentally different protocol: baseline HOC synapses are silenced
(`_silence_baseline_hoc_synapses` zeros `b2gampa`, `b2gnmda`, `s2ggaba`, `s2gach` and re-runs
`update()`/`placeBIP()`), per-ON-dendrite AMPA (`sec(0.9)`) + GABA_A (`sec(0.3)`) `Exp2Syn` pairs
are created once at build time and driven by dedicated NetStim bursts, and `schedule_ei_onsets`
computes per-pair start times as a function of bar direction. The CSV schema is the canonical
`(angle_deg, trial_seed, firing_rate_hz)` across all three drivers [t0008, t0020, t0022] — that
schema is what `tuning_curve_loss.score` expects.

### Scoring glue with `tuning_curve_loss`

All three driver generations use identical scoring glue [t0008, t0020, t0022]. `score_envelope.py`
is effectively a 100-line copy across tasks: import `score`, `METRIC_KEY_DSI`, `METRIC_KEY_HWHM`,
`METRIC_KEY_RELIABILITY`, `METRIC_KEY_RMSE` from
`tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`, call
`score(simulated_curve_csv=<csv_path>)`, then serialize a 13-field debug dump to
`data/score_report.json` and the four registered metric keys to `results/metrics.json`
([t0012]-registered keys). `score()` resolves the default target to the t0004 canonical curve. The
identity gate `score(TARGET_MEAN_CSV).loss_scalar == 0.0` is the standard self-check [t0008].

### Library-vs-copy reuse boundary

[t0008]'s `modeldb_189347_dsgc` is the only port library whose Python code is physically rooted
inside `assets/library/<slug>/code/` — the library `details.json` declares it via `module_paths`.
[t0020]'s library also points at its task-folder `code/` via `module_paths`. [t0022]'s library
declares `module_paths` pointing to task-folder `code/` files, but nothing stops cross-task import
in principle since task folders are Python packages (t0022 imports
`tasks.t0008_port_modeldb_189347.code.build_cell` directly). The project rule is clear: cross-task
imports are permitted only through registered libraries; everything else must be copied.

## Reusable Code and Assets

* **`modeldb_189347_dsgc` library** from [t0008]. **Import via library.** Specifically
  `build_cell.py` provides `build_dsgc() -> h`, `apply_params(h, *, seed: int) -> None`,
  `read_synapse_coords(h) -> list[SynapseCoords]`, `get_cell_summary(h) -> CellSummary`, and
  `run_one_trial(*, h, angle_deg, seed, baseline_coords) -> float`. For t0024 these cannot be
  imported as-is (different model, different HOC file names) but are the template for a new
  analogous module. Approx 358 lines in `build_cell.py`; adapt to de Rosenroll HOC/MOD file names,
  new parameter block, new channel densities. The Windows-specific nrnmech.dll loading sequence
  (`_nrnmech_dll_path`, `load_neuron`, `_sources_dir_hoc_safe`) transfers unchanged.

* **`tuning_curve_loss` library** from [t0012]. **Import via library.** Use
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import score, METRIC_KEY_DSI, METRIC_KEY_HWHM, METRIC_KEY_RELIABILITY, METRIC_KEY_RMSE`
  and call `report = score(simulated_curve_csv=<path>)`. No adaptation needed if the CSV uses the
  canonical `(angle_deg, trial_seed, firing_rate_hz)` schema. Zero lines to copy.

* **`score_envelope.py` pattern** from `tasks/t0008_port_modeldb_189347/code/score_envelope.py`
  (also present almost verbatim in
  `tasks/t0022_modify_dsgc_channel_testbed/code/score_envelope.py`). **Copy into task.** Approx 100
  lines. Adapt only the input CSV constant and the output paths.

* **12-angle moving-bar driver pattern** from
  `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py` (683 lines) and its
  `neuron_bootstrap.py` (64 lines). **Copy into task**, since t0022's driver is not packaged as an
  importable library module. Key signatures to preserve: `build_ei_pairs(*, h) -> list[EiPair]`,
  `schedule_ei_onsets(*, h, pairs, angle_deg, velocity_um_per_ms, gaba_null_pref_ratio, trial_seed)`,
  `run_one_trial_dendritic(*, h, pairs, angle_deg, trial_seed, baseline_coords, baseline_gaba_mod) -> float`.
  Adapt to whatever direction-selectivity mechanism the de Rosenroll source uses; most likely the de
  Rosenroll paper provides its own driver and we should wire that up instead, keeping only the outer
  sweep loop and CSV writer (~150 lines).

* **Constants block layout** from `tasks/t0008_port_modeldb_189347/code/constants.py` (85 lines) —
  one flat module with `CELSIUS_DEG_C`, `DT_MS`, `TSTOP_MS`, `V_INIT_MV`, `AP_THRESHOLD_MV`,
  `ANGLE_STEP_DEG`, `N_ANGLES`, `N_TRIALS`, plus the paper's canonical parameter block. **Copy into
  task** and replace with de Rosenroll parameters.

* **Per-trial BIP position guard** from
  `tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py` function
  `_assert_bip_positions_baseline(*, h, baseline_coords)` — asserts BIP `(locx, locy)` match the
  baseline snapshot to catch silent rotation-logic re-engagement. **Copy into task**, ~20 lines,
  only if the de Rosenroll port also retains the Poleg-Polsky BIP synapses.

* **SWC morphology I/O** from `tasks/t0008_port_modeldb_189347/code/swc_io.py` (215 lines). **Copy
  into task** if de Rosenroll ships morphology as SWC rather than HOC. Provides `parse_swc_file`,
  `validate_structure`, `summarize`, `write_swc_file`.

* **Optional: `tuning_curve_viz` library** from [t0011]. **Import via library.** Polar + Cartesian
  plots consuming the canonical CSV schema. Zero lines to copy.

## Lessons Learned

* **Spatial-rotation proxy undershoots DSI**: [t0008] reached DSI 0.316 with a rotation-only driver;
  [t0020] reached DSI 0.7838 with the paper's native parameter swap on the same geometry. If the de
  Rosenroll paper specifies a native direction-selectivity mechanism, implement that mechanism
  directly rather than approximating with geometry.
* **Absolute firing rates lag the envelope even when DSI is right**: both [t0020] (peak 14.85 Hz)
  and [t0022] (peak 15 Hz) fell well below the 40-80 Hz envelope despite correct DSI, a Risk-3 class
  of failure. Expect to report this gap as a genuine experimental finding rather than chasing it as
  a bug, unless the de Rosenroll paper reports higher firing rates.
* **Windows nrnivmodl requires a CMD wrapper**: [t0008] introduced `code/run_nrnivmodl.cmd` to
  bypass MSYS path mangling; the compiled `nrnmech.dll` must live in the same directory as the MOD
  sources or `h.nrn_load_dll` fails.
* **HOC parser is brittle with backslashes**: always build HOC path strings with forward slashes,
  even on Windows ([t0008] `_sources_dir_hoc_safe` helper).
* **Re-running `update()` + `placeBIP()` is mandatory** after any global parameter change, because
  scalars sit in HOC globals but per-synapse instances retain old values until those procs run
  ([t0020, t0022]).
* **Silence baseline synapses** when adding a new direction-selectivity driver: [t0022] zeros
  `b2gampa`, `b2gnmda`, `s2ggaba`, `s2gach` to prevent the bundled Poleg-Polsky synapses from
  contributing background spikes.
* **Library-asset driver code can live in `assets/library/<slug>/code/`**: [t0008] and [t0020] do
  this; [t0022] leaves its driver in the task `code/` folder, which makes it harder for later tasks
  to reuse. Prefer the [t0008] pattern when packaging the new port library.

## Recommendations for This Task

1. **Adopt the [t0008] layout for the new library**: `assets/library/de_rosenroll_2026_dsgc/` with
   `sources/` for the paper's HOC/MOD/morphology files (clone the de Rosenroll repository in place,
   strip any nested `.git`), `code/` for the Python driver and scoring glue, and a
   `run_nrnivmodl.cmd` wrapper. Reuse the `build_cell.py` skeleton: NEURON bootstrap, DLL load,
   `build_dsgc`-equivalent, `apply_params`, `run_one_trial`, `SynapseCoords`-style dataclasses.
2. **Import the `modeldb_189347_dsgc` library only for the generic helpers** (NEURON bootstrap
   utilities); do **not** reuse its `build_dsgc` directly because the HOC/MOD files and parameter
   set are different. Write a `build_de_rosenroll_dsgc()` that mirrors the same lifecycle.
3. **Import `tuning_curve_loss` via library** and copy the ~100-line `score_envelope.py` pattern
   into the new task; keep the four registered metric keys and the canonical 12-angle CSV schema
   `(angle_deg, trial_seed, firing_rate_hz)`.
4. **Use the de Rosenroll paper's own direction-selectivity driver verbatim** when porting. Only
   fall back to copying [t0022]'s `schedule_ei_onsets` / `run_one_trial_dendritic` pattern if the
   paper does not specify a driver and we must synthesize one.
5. **Expect and plan for the peak-firing-rate envelope miss**. Frame the result in
   `results_detailed.md` as a third datapoint on whether the 40-80 Hz peak requirement is achievable
   across independent DSGC models, not as a port defect to chase.
6. **Keep the BIP-position guard only if the de Rosenroll model reuses Poleg-Polsky BIP synapses**;
   otherwise write an analogous guard for whatever the new model's direction-coding variables are.
7. **Copy-in versus library-import labels must be explicit in the plan**. Every piece of code from
   [t0022] is a copy-in because the task `code/` is not a module-registered library; every piece
   from [t0008] and [t0012] flows through `module_paths` in their `details.json` and must be
   imported.

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 DSGC and hunt sibling models
* **Status**: completed
* **Relevance**: Source of the `modeldb_189347_dsgc` library asset and the canonical
  HOC/MOD/morphology port layout; its `build_cell.py` bootstrap pattern, Windows nrnivmodl wrapper,
  and 12-angle tuning-curve driver are the direct templates for t0024.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response visualization library
* **Status**: completed
* **Relevance**: Provides `tuning_curve_viz`, the optional Cartesian + polar + overlay plotter that
  consumes the canonical tuning-curve CSV; t0024 may import it to populate `results/images/`.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning curve scoring loss library
* **Status**: completed
* **Relevance**: Provides the `tuning_curve_loss` library consumed by every port's scoring step;
  t0024 will import `score()` and the four registered metric keys without adaptation.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol
* **Status**: completed
* **Relevance**: Demonstrates how to package a driver variant as a new library while reusing
  [t0008]'s `build_cell` via library import; also contributes the per-trial BIP-position baseline
  guard.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC port with spatially-asymmetric inhibition for channel testbed
* **Status**: completed
* **Relevance**: Supplies the 12-angle moving-bar driver infrastructure with per-dendrite
  AMPA/GABA_A NetStim pairs and channel-modular AIS partition; t0024's plan identifies this driver
  as the soft-dependency reference implementation for the moving-bar protocol.

### [t0023]

* **Task ID**: `t0023_port_hanson_2019_dsgc`
* **Name**: Port Hanson 2019 DSGC model
* **Status**: intervention_blocked
* **Relevance**: Sibling port using the same infrastructure as t0024; its task description documents
  the intended reuse pattern (t0008 layout + t0022 driver) that t0024 should also follow, even
  though t0023 has not executed yet.
