---
spec_version: "1"
task_id: "t0059_bar_locked_gaba_ampa_sweep_t0057"
research_stage: "code"
tasks_reviewed: 9
tasks_cited: 8
libraries_found: 14
libraries_relevant: 4
date_completed: "2026-04-29"
status: "complete"
---
# Research Code: Bar-Arrival-Locked Tonic GABA + AMPA Sweep on t0057 Substrate

## Task Objective

Fork [t0057]'s `minimal_dsgc_tonic_gaba_sweep` library and apply three bundled changes: (a) replace
the global `(t_on, t_off) = (100, 1400)` ms tonic GABA window with a per-synapse bar-arrival-locked
window `(t_on_i = (x_i cos theta + y_i sin theta) / v + 100, t_off_i = t_on_i + 200)` ms gated by
the same centripetal-gating predicate from [t0053]; (b) bundle the project-wide DSGC
measurement-protocol fix S-0055-01 (drop `E_ONLY` / `GABA_ONLY`; add `EPSP_PASSIVE` / `IPSP_PASSIVE`
modes that save-and-zero `gnabar_hh` / `gkbar_hh` on `soma` and `axon_initial_segment`; standardise
trial length at 1400 ms); and (c) sweep a 5x5 `(gAMPA, GABA_BASE_NS)` grid replacing [t0057]'s 1-D
GABA-only sweep, with `gAMPA in {0.5, 1.0, 2.0, 3.0, 4.0}` nS and
`GABA_BASE_NS in {0.1, 0.2, 0.5, 1.0, 2.0}` nS. The expected output is one library asset
(`minimal_dsgc_bar_locked_gaba_ampa_sweep` or similar slug) plus 25 grid cells x 12 directions x 10
trials x 3 modes = 9000 trials of metrics, plots, and cross-grid summary heatmaps.

## Library Landscape

The repository exposes 14 library assets across `tasks/*/assets/library/*/details.json`. The asset
aggregators (`aggregate_libraries.py`, `aggregate_answers.py`, etc.) are not yet implemented in this
fork, so libraries were enumerated by walking the filesystem directly (verified by listing 14
`details.json` paths). No `replaces` field was found on any library; no correction overlays apply.

* `minimal_dsgc_tonic_gaba_sweep` (from [t0057], 0.1.0) — primary upstream substrate. **Cannot be
  imported** per CLAUDE.md rule 3 (cross-task imports are only allowed for registered libraries that
  the current task explicitly depends on, and only via the `tasks.tXXXX_*.code.*` path convention).
  All 13 module paths and all four test files must be **copied into** `tasks/t0059_*/code/` and
  rewritten with the new task's import prefix. Entry points to preserve: `build_dsgc_from_swc`,
  `sample_dendritic_locations`, `i_synapse_fires`, `build_ei_pairs`, `schedule_ei_onsets`,
  `run_one_trial`, `run_full_sweep`, `compute_metrics_main`, `render_figures_main`,
  `compute_vector_sum_dsi`, `compute_preferred_direction_deg`, `ensure_gaba_tonic_compiled`, and the
  `gaba_tonic` POINT_PROCESS itself.
* `tuning_curve_loss` (from [t0012], 0.1.0,
  `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`) — relevant. **Import via
  library**. Provides `TuningCurve`, `load_tuning_curve`, `compute_dsi`, `compute_hwhm_deg`,
  `compute_peak_hz`, `compute_null_hz`, `compute_reliability`, `score`, `ScoreReport`,
  `check_envelope`. Used unchanged for FULL-mode metrics; used per grid cell to produce the 25-cell
  DSI / Peak Hz / HWHM / RMSE arrays consumed by the heatmap renderers.
* `tuning_curve_viz` (from [t0011], 0.1.0,
  `tasks.t0011_response_visualization_library.code.tuning_curve_viz`) — relevant. **Import via
  library**. Provides `plot_polar_tuning_curve`, `plot_cartesian_tuning_curve`,
  `plot_angle_raster_psth`, `plot_multi_model_overlay`, `OKABE_ITO`. Used per grid cell for the 25
  per-cell polar / Cartesian / raster+PSTH plots.
* `minimal_dsgc_mg_block_nmda` (from [t0055]) — relevant as a procedural template only:
  demonstrates the only existing repo pattern for compiling a custom `.mod` POINT_PROCESS via a
  `code/run_nrnivmodl.cmd` shim and registering it with `h.nrn_load_dll`. The `gaba_tonic.mod` file
  in [t0057] follows this exact pattern; the t0059 fork inherits it verbatim with only the per-task
  sentinel env-var rename (`_T0057_NEURONHOME_BOOTSTRAPPED` -> `_T0059_NEURONHOME_BOOTSTRAPPED`).

The remaining 10 libraries are not directly relevant to t0059 because they model different DSGC
paradigms or earlier substrate generations: `modeldb_189347_dsgc` ([t0008]),
`modeldb_189347_dsgc_gabamod` (t0020), `modeldb_189347_dsgc_dendritic` (t0022),
`de_rosenroll_2026_dsgc` (t0024), `modeldb_189347_dsgc_exact` ([t0046]), `dsgc_dummy_models`
(t0010), `minimal_dsgc_scalar_gaba` ([t0052]), `minimal_dsgc_spatial_gaba` ([t0053]),
`minimal_dsgc_ampa_nmda_scalar_gaba` ([t0054]), and `minimal_dsgc_mg_block_nmda` ([t0055]). They
either have NMDA on the E pathway (explicitly out of scope per the task description) or use
network-level / scalar gabaMOD inhibition rather than the tonic-GABA substrate this task forks.

## Key Findings

### The Bar-Arrival-Locked Window Replaces a Two-Constant Block in t0057

The change from t0057's global `(T_ON_MS, T_OFF_MS) = (100.0, 1400.0)` ms window to the new
per-synapse `(t_on_i, t_off_i)` window is localised to a single function in t0057's code:
`schedule_ei_onsets` at lines 180-230 of `tasks/t0057_tonic_gaba_sweep_t0053/code/synapses.py`
[t0057]. Currently lines 217-219 write a constant `(T_ON_MS, T_OFF_MS)` to every fired pair's
`gaba_syn`:

```python
pair.gaba_syn.g = gaba_full_g_us
pair.gaba_syn.t_on = T_ON_MS
pair.gaba_syn.t_off = T_OFF_MS
```

The fork must replace those three lines with a per-pair computation that mirrors the existing
`_onset_time_ms` helper (lines 166-177 of t0057's `synapses.py` [t0057]):

```python
t_on_i = onset_ms  # already includes BASE_OFFSET_MS = 100 ms
t_off_i = onset_ms + WINDOW_MS  # WINDOW_MS = 200 ms (FIXED)
pair.gaba_syn.g = gaba_full_g_us
pair.gaba_syn.t_on = t_on_i
pair.gaba_syn.t_off = t_off_i
```

`onset_ms` is already computed in the same loop body — the AMPA `NetStim.start` is set to it (line
209), so the I window centre coincides with the AMPA spike at zero per-pair geometric latency. This
single-loop rewrite is a ~5-line diff plus deletion of `T_OFF_MS` from the import block. `T_ON_MS`
becomes unused at the synapse-scheduling site (the BASE_OFFSET_MS = 100 ms is already folded into
`onset_ms` by `_onset_time_ms`); it should remain in `constants.py` only as a sanity reference for
the `IPSP_SUSTAINED_T_EARLY_MS` / `IPSP_SUSTAINED_T_LATE_MS` constants, which become
direction-dependent and need a different gating strategy (see "Test Migration" below).

### HH Save-and-Zero Lives Inside the Trial Runner, Not the Synapse Layer

The S-0055-01 measurement-protocol fix replaces t0057's `E_ONLY` / `GABA_ONLY` (renamed `AMPA_ONLY`
/ `GABA_ONLY` in [t0057]) with `EPSP_PASSIVE` / `IPSP_PASSIVE`. The save-and-zero operation must run
on `cell.soma` and `cell.axon_initial_segment` only — the dendrites are passive in [t0057] (and
[t0053]) and have no `hh` mechanism, so attempting `seg.hh.gnabar = 0` on a dendrite would error.
The cleanest fork point is t0057's `_apply_mode_weights` in
`tasks/t0057_tonic_gaba_sweep_t0053/code/trial.py` lines 56-76 [t0057], which currently zeroes the
GABA `g` for `AMPA_ONLY` and the AMPA `weight[0]` for `GABA_ONLY`. The new dispatcher must:

1. For `EPSP_PASSIVE`: zero every fired pair's GABA `g` / `t_on` / `t_off` (same as t0057
   `AMPA_ONLY`); save and zero `cell.soma.gnabar_hh`, `cell.soma.gkbar_hh`,
   `cell.axon_initial_segment.gnabar_hh`, `cell.axon_initial_segment.gkbar_hh`.
2. For `IPSP_PASSIVE`: zero every pair's AMPA `weight[0]` (same as t0057 `GABA_ONLY`); save and zero
   the same four HH conductances.
3. For `FULL`: do nothing extra (HH active, both branches active).

The post-trial defensive-restore block at t0057's `trial.py` lines 135-149 [t0057] must be extended
to restore the saved HH conductances. This is a ~20-line addition, structured as a frozen dataclass
`HhConductanceSnapshot(soma_gnabar, soma_gkbar, ais_gnabar, ais_gkbar)` returned from a
`_save_and_zero_hh(*, cell)` helper and consumed by a `_restore_hh(*, cell, snapshot)` helper at the
end of `run_one_trial`. A try/finally guard ensures HH is always restored even if `h.continuerun`
raises.

### Trial Length Standardisation: 1500 ms -> 1400 ms

Five sibling tasks ([t0052], [t0053], [t0054], [t0055], [t0057]) all use `TSTOP_MS = 1500.0` (line
19 of t0057's `constants.py` [t0057]). The S-0055-01 bundled fix sets it to 1400 ms. This is a
one-character change (`1500.0` -> `1400.0`) plus three downstream impacts:

* `compute_metrics.py` divides spike counts by `TSTOP_MS / 1000.0` to compute firing rate (line 130
  of t0057's `trial.py` [t0057]); the rate normalisation tightens by ~7% (one fewer 100 ms of silent
  tail per trial).
* The IPSP-sustained-window check at `IPSP_SUSTAINED_T_LATE_MS = 1300.0` ms (line 101 of t0057's
  `constants.py` [t0057]) is no longer well-defined under the bar-arrival-locked windows — the
  late-direction synapses' windows close at `t_on_max + 200 ms` which can be much earlier than 1300
  ms. This test must be redesigned (see "Test Migration" below).
* The `BASE_OFFSET_MS = 100.0` buffer remains correct: at `theta = 180 deg, v = 1 um/ms`, the most
  proximal synapse's `onset_ms` is `(x cos 180 + y sin 180) / 1 + 100`, which is positive only for
  synapses with `x cos theta + y sin theta > -100`. With the calibrated morphology spanning ~250 um
  in each direction and `BASE_OFFSET_MS = 100 ms`, all 100 synapses' onsets are positive across all
  12 directions (verified by reading t0057's `_onset_time_ms` helper which uses
  `max(raw_t, 0.0) + BASE_OFFSET_MS` on line 177 of `synapses.py` [t0057]).

### The 5x5 Sweep Replaces a 1x5 Sweep — Outer Loop Refactor

t0057's `run_full_sweep` at lines 522-628 of `run_tuning_curve.py` [t0057] iterates over
`GABA_BASE_NS_VALUES = (0.25, 0.5, 1.0, 1.5, 2.0)` with `gAMPA` hard-coded at 0.5 nS via
`AMPA_PEAK_NS = 0.5` (line 69 of t0057's `constants.py` [t0057]). The fork must:

1. Add `AMPA_PEAK_NS_VALUES: tuple[float, ...] = (0.5, 1.0, 2.0, 3.0, 4.0)` to constants and replace
   `GABA_BASE_NS_VALUES` with the new sub-0.25 grid `(0.1, 0.2, 0.5, 1.0, 2.0)` nS.
2. Thread `gampa_ns` through `schedule_ei_onsets` (currently fixed at `AMPA_PEAK_NS * 1e-3` on line
   142 of t0057's `synapses.py` [t0057]; the `_apply_mode_weights` AMPA-only-zero path on line 74 of
   t0057's `trial.py` [t0057] also sets `weight[0]` and must read from the swept `gampa_ns`).
3. Add an outer `gampa_ns` loop in `run_full_sweep` and prefix every per-mode CSV row with
   `(gampa_ns, gaba_base_ns)` (extending t0057's leading `gaba_base_ns` column convention from line
   192 of `run_tuning_curve.py` [t0057]).
4. Skip the per-synapse activation-time CSV (no longer informative once the windows are explicit in
   the schedule). t0057's `_write_activation_times_csv` at lines 260-299 of `run_tuning_curve.py`
   [t0057] is dropped; the `synapse_onset_times_ms` field of `TrialResult` becomes optional.

The trial budget grows from 5 x 12 x 10 x 3 = 1800 (t0057 actual) to 25 x 12 x 10 x 3 = 9000.
Extrapolating t0057's measured 6318 s wall-clock under CVODE at `atol = 1e-3`, the t0059 sweep
should complete in ~5x = 31580 s ~ 8.77 h on the same local CPU (matches the task description's 8.75
h estimate).

### Convergent Negative Result: Five Tasks Topped Out at 0.667 Hz

Five completed minimal-DSGC tasks ([t0052], [t0053], [t0054], [t0055], [t0057]) all converge on the
same single-spike-per-trial regime: peak Hz = 0.6667 (one spike per 1500 ms = 0.667 Hz) under any
non-saturating inhibition. The diagnosis is that AMPA at 0.5 nS x 100 synapses is too weak to drive
a multi-spike train on the t0009 calibrated morphology. Specific evidence:

* [t0052] FULL peak Hz = 0.667 with scalar gabaMOD inhibition and primary DSI = 1.0 (degenerate).
* [t0053] FULL peak Hz = 0.000 (full suppression at gGABA = 2 nS) — too strong but never
  intermediate.
* [t0054] with NMDA-Exp2Syn at gNMDA = 0.25 nS recovers peak Hz to 8.0 but vector-sum DSI collapses
  from 0.746 to 0.082 because scalar gabaMOD cannot keep up.
* [t0055] with Mg-block NMDA recovers DSI to 0.7464 but peak Hz reverts to 0.667 because Mg block
  keeps NMDA blocked when GABA holds Vm hyperpolarised.
* [t0057] AMPA_ONLY peak Hz = 0.6667 uniformly across all 12 directions and all 5 GABA conductance
  values — bit-identical to [t0052] / [t0053].

The t0059 task explicitly targets this failure mode by adding the
`gAMPA in {0.5, 1.0, 2.0, 3.0, 4.0}` axis. Whether any cell on the 5x5 grid produces FULL peak Hz in
the 5-50 Hz multi-spike band (RQ1 / RQ4) is the headline experimental question.

### CVODE is Mandatory; Fixed-Step is a Performance Cliff

t0057's `enable_cvode` helper (lines 82-96 of `neuron_bootstrap.py` [t0057]) drops per-trial
wall-clock from ~75 s to ~3-8 s by enabling NEURON's variable-step solver at `atol = 1e-3`. With
9000 trials at fixed-step (~75 s/trial), the t0059 sweep would take ~187 h ~ 7.8 days; under CVODE,
~8.8 h. The fork must call `enable_cvode()` AFTER `ensure_gaba_tonic_compiled()` per the order
documented at lines 144-155 of t0057's `run_tuning_curve.py` [t0057]: `ensure_neuron_importable` ->
`load_stdrun` -> `ensure_gaba_tonic_compiled` -> `enable_cvode`. Skipping any step or reordering
fails noisily (NEURON refuses to construct `h.gaba_tonic(seg)` if the DLL is not loaded).

### Test Migration: Bar-Arrival-Locked IPSP Has a Direction-Dependent Centre of Mass

t0057's headline regression test `test_gaba_tonic_envelope.py` [t0057] asserts that at theta = 210
deg (most-active direction), `|v(t = 1300 ms) - V_init| >= 0.5 * |v(t = 200 ms) - V_init|` for each
of the 5 conductance values. With per-synapse 200 ms windows, this assertion is no longer
meaningful: the windows of all 100 active synapses span at most ~600 ms (bar takes ~500 ms to cross
the ~500 um arena at 1 um/ms, plus a 200 ms window) and close at varying times depending on the
direction. The replacement test (per the task's verification criteria) is a centre-of-mass shift
test:

> Compute the centre of mass of the IPSP voltage envelope at theta = 0 and theta = 90; assert that
> their difference is consistent with the stimulus geometry — i.e.,
> `|com_v(theta=0) - com_v(theta=90)| >= predicted_lower_bound` where `predicted_lower_bound` is
> computed from the 100 synapse coordinates and the bar-arrival latency formula.

This is a new test file `test_bar_locked_ipsp_envelope.py` to be created in t0059's `code/`,
replacing the old `test_gaba_tonic_envelope.py`. The other three t0057 test files
(`test_quiescent_rest.py`, `test_spatial_gating.py`, `test_placement_seed0_match.py`) carry over
unchanged in logic; only the import prefix is rewritten from
`tasks.t0057_tonic_gaba_sweep_t0053.code.*` to `tasks.t0059_*.code.*`.

A NEW regression test required by the task's verification criteria asserts HH save-and-zero
correctness: at one representative `(gAMPA, GABA_BASE_NS)` point, the FULL trace under the new code
is bit-identical (within 1e-6 mV) to a reference produced from the t0057 code path with HH active
throughout. This is implementable as a recorded reference array stored in
`code/test_data/full_reference_trace_g0p5_g1p0.npy` and a numpy `assert_allclose` check.

EPSP_PASSIVE peak Vm < spike threshold (~ -50 mV) at every direction and grid cell is a soft gate
— implementable inside `compute_metrics.py` as a max-Vm scan over EPSP_PASSIVE traces and a
`RuntimeError` if any cell exceeds `AP_THRESHOLD_MV = -20.0` (line 23 of t0057's `constants.py`
[t0057]).

### Placement Seed 0 Bit-Identity Is the Canonical Cross-Task Anchor

[t0052], [t0053], [t0054], [t0055], and [t0057] all use `PLACEMENT_SEED = 0` and the same
`sample_dendritic_locations` algorithm. The t0057 `test_placement_seed0_match.py` [t0057] regression
checks that the saved `placement_seed0.json` matches t0053's reference file at
`POSITION_TOLERANCE = 1e-9`. The t0059 fork inherits this anchor: the test must be ported to compare
against t0057's `placement_seed0.json` at the same tolerance. This guarantees that the only
scientifically meaningful changes in the new task are (a) the per-synapse window mechanism, (b) the
HH save-and-zero, (c) the gAMPA sweep — not any drift in synapse placement.

## Reusable Code and Assets

### Primary Reuse: Fork [t0057] `minimal_dsgc_tonic_gaba_sweep` Library

Copy all 13 module paths and 4 test files from `tasks/t0057_tonic_gaba_sweep_t0053/code/` into
`tasks/t0059_*/code/`. Rewrite all import prefixes from `tasks.t0057_tonic_gaba_sweep_t0053.code.*`
to `tasks.t0059_*.code.*`. Specific files:

* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/cell.py` (~215 lines)
  * **Reuse method**: copy into task
  * **What it does**: `build_dsgc_from_swc(swc_path) -> CellHandles`. Parses the calibrated SWC,
    collapses the 19 soma rows, builds one `h.Section` per non-soma compartment, attaches a
    synthetic AIS, returns the `CellHandles` dataclass with `soma`, `axon_initial_segment`,
    `dendrites`, `dendrite_xyz_um`, `soma_origin_um`.
  * **Adaptation needed**: rewrite import prefix only; no logic changes. Place HH only on `soma` and
    `axon_initial_segment` (already correct in [t0057]).
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/swc_io.py` (~150 lines)
  * **Reuse method**: copy into task
  * **What it does**: `parse_swc_file(swc_path) -> list[SwcCompartment]` and
    `validate_structure(compartments)`. SWC parsing pipeline.
  * **Adaptation needed**: rewrite import prefix only.
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/placement.py` (~120 lines)
  * **Reuse method**: copy into task
  * **What it does**: `sample_dendritic_locations(*, cell, n_pairs, seed) -> list[Location]` and
    `save_placement_json(*, locations, out_path)`. Bit-identical to [t0053] / [t0054] / [t0055] /
    [t0057] with `seed = 0`.
  * **Adaptation needed**: rewrite import prefix only.
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/synapses.py` (~230 lines)
  * **Reuse method**: copy into task with substantial edits
  * **What it does**: `build_ei_pairs`, `i_synapse_fires`, `schedule_ei_onsets`, `_onset_time_ms`,
    `EiPair`, `ScheduleResult`.
  * **Adaptation needed**: in `schedule_ei_onsets`, replace lines 217-219 (the constant `T_ON_MS` /
    `T_OFF_MS` writes) with per-pair `t_on_i = onset_ms`, `t_off_i = onset_ms + WINDOW_MS`. Add
    `WINDOW_MS = 200.0` to constants. Thread `gampa_ns` through `schedule_ei_onsets` so the AMPA
    `weight[0]` is set per call rather than from the constant `AMPA_PEAK_NS`. Drop the t0057
    `T_OFF_MS` import.
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/trial.py` (~165 lines)
  * **Reuse method**: copy into task with substantial edits
  * **What it does**: `run_one_trial`, `_apply_mode_weights`, `TrialResult`, the post-trial
    defensive-restore block.
  * **Adaptation needed**: replace `AMPA_ONLY` / `GABA_ONLY` with `EPSP_PASSIVE` / `IPSP_PASSIVE` in
    the `TrialMode` enum (constants.py). Add `_save_and_zero_hh(cell)` and
    `_restore_hh(cell, snapshot)` helpers. Wrap `h.continuerun` in try/finally so HH is always
    restored. Add `gampa_ns` parameter and thread it into `schedule_ei_onsets`.
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/run_tuning_curve.py` (~635 lines)
  * **Reuse method**: copy into task with substantial edits
  * **What it does**: `setup_sweep_artifacts`, `run_dry_run_validation`, `run_full_sweep`, all CSV
    writers, dry-run gates.
  * **Adaptation needed**: add outer `gampa_ns` loop inside `run_full_sweep`. Drop
    `_write_activation_times_csv` (no longer informative). Replace the 1300 ms IPSP-sustained check
    with the new centre-of-mass shift check. Update CSV column writers to prefix every row with
    `(gampa_ns, gaba_base_ns)`. Update progress-bar totals (5 -> 25).
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/compute_metrics.py` (~500 lines)
  * **Reuse method**: copy into task with substantial edits
  * **What it does**: `compute_metrics_main` + `CurveKey` dataclass + 15-variant `metrics.json`
    writer + `derived_quantities.json` writer.
  * **Adaptation needed**: extend the `CurveKey` to `(gampa_ns, gaba_base_ns, mode)`; raise variant
    count from 15 to 75 (5 x 5 x 3). Add the EPSP_PASSIVE peak Vm soft gate. Drop the
    `AMPA_ONLY_PEAK_HZ_EXPECTED` regression sentinel (the AMPA path now varies with `gampa_ns`).
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/render_figures.py` (~480 lines)
  * **Reuse method**: copy into task with substantial edits
  * **What it does**: per-cell V/EPSP/IPSP/PSTH plots + 6 cross-conductance summary plots.
  * **Adaptation needed**: rewire from 1-D scalar-vs-conductance line plots to 2-D `(gampa, gaba)`
    heatmaps using `matplotlib.pyplot.pcolormesh`. Add the regime-boundary contour overlay using
    `matplotlib.pyplot.contour` with three regions: single-spike-degenerate (peak Hz ~ 0.667 within
    tolerance), multi-spike (5-50 Hz), and full-suppression (peak Hz ~ 0).
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/metrics_extra.py` (~75 lines)
  * **Reuse method**: copy into task
  * **What it does**: `compute_vector_sum_dsi(rates, angles_deg) -> float` and
    `compute_preferred_direction_deg(rates, angles_deg) -> float`.
  * **Adaptation needed**: rewrite import prefix only.
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/neuron_bootstrap.py` (~150 lines)
  * **Reuse method**: copy into task
  * **What it does**: `ensure_neuron_importable`, `load_stdrun`, `enable_cvode`,
    `ensure_gaba_tonic_compiled`, `_build_gaba_tonic_dll`.
  * **Adaptation needed**: rewrite import prefix; rename sentinel env-var
    `_T0057_NEURONHOME_BOOTSTRAPPED` -> `_T0059_NEURONHOME_BOOTSTRAPPED`. The
    `ensure_gaba_tonic_compiled` machinery is unchanged.
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/constants.py` (~150 lines)
  * **Reuse method**: copy into task with substantial edits
  * **What it does**: numeric constants, column names, `TrialMode` enum, regression sentinels.
  * **Adaptation needed**: `TSTOP_MS = 1500.0` -> `1400.0`. `TrialMode` members `AMPA_ONLY` /
    `GABA_ONLY` -> `EPSP_PASSIVE` / `IPSP_PASSIVE`. Replace
    `GABA_BASE_NS_VALUES = (0.25, 0.5, 1.0, 1.5, 2.0)` with `(0.1, 0.2, 0.5, 1.0, 2.0)`. Add
    `AMPA_PEAK_NS_VALUES: tuple[float, ...] = (0.5, 1.0, 2.0, 3.0, 4.0)`. Add
    `WINDOW_MS: float = 200.0`. Drop `T_OFF_MS` (no longer needed at synapse layer; window edges are
    computed per pair). Drop `IPSP_SUSTAINED_*` constants and the AMPA_ONLY regression sentinel
    constants. Add `COL_GAMPA_NS: str = "gampa_ns"` for the new CSV column.
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/paths.py` (~100 lines)
  * **Reuse method**: copy into task
  * **What it does**: `MORPHOLOGY_SWC_PATH`, `PLACEMENT_JSON`, all per-mode CSV paths,
    `NRNMECH_DLL`, `RUN_NRNIVMODL_CMD`, `MOD_DIR`.
  * **Adaptation needed**: rewrite all per-mode CSV names to use `epsp_passive` / `ipsp_passive`
    instead of `ampa_only` / `gaba_only`. Rewrite import prefix.
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/mod/GabaTonic.mod` (~100 lines)
  * **Reuse method**: copy into task
  * **What it does**: NEURON POINT_PROCESS `gaba_tonic` with `(g, e, t_on, t_off, ramp_ms)` RANGE
    attributes and 1 ms cosine envelope at each window edge.
  * **Adaptation needed**: zero — the `.mod` source is identical because the mechanism's interface
    (per-instance `t_on` / `t_off`) is unchanged. Only the Python caller writes different values per
    pair.
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/run_nrnivmodl.cmd` (~12 lines)
  * **Reuse method**: copy into task
  * **What it does**: Windows batch shim that wraps `nrnivmodl.bat` against `code/mod/`.
  * **Adaptation needed**: zero.
* **Source**: `tasks/t0057_tonic_gaba_sweep_t0053/code/test_quiescent_rest.py`,
  `test_spatial_gating.py`, `test_placement_seed0_match.py` (~80, 60, 70 lines)
  * **Reuse method**: copy into task
  * **What it does**: V_rest = -65 mV passive run; `i_synapse_fires` predicate sweep; placement
    bit-identity vs t0057's `placement_seed0.json`.
  * **Adaptation needed**: rewrite import prefix; update the placement reference from t0053's
    `placement_seed0.json` to t0057's `placement_seed0.json` (semantically identical content).

### Library Imports (cross-task — no copying)

* **Source**: `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/`
  * **Reuse method**: import via library
  * **Function signatures**:
    * `load_tuning_curve(*, path: Path, schema: str = "canonical") -> TuningCurve`
    * `compute_dsi(*, peak: float, null: float) -> float` — returns
      `(peak - null) / (peak + null)` with zero-sum protection.
    * `compute_peak_hz(curve: TuningCurve) -> float`, `compute_null_hz(curve: TuningCurve) -> float`
    * `compute_hwhm_deg(curve: TuningCurve) -> float`
    * `compute_reliability(curve: TuningCurve) -> float | None`
    * `score(*, candidate_path: Path, target_path: Path, weights: dict[str, float] | None) -> ScoreReport`
* **Source**: `tasks/t0011_response_visualization_library/code/tuning_curve_viz/`
  * **Reuse method**: import via library
  * **Function signatures**:
    * `plot_polar_tuning_curve(*, df, out_path, target_df=None, ...)`
    * `plot_cartesian_tuning_curve(*, df, out_path, target_df=None, ...)`
    * `plot_angle_raster_psth(*, df, out_path, ...)`
    * `plot_multi_model_overlay(*, dfs, labels, out_path, ...)`

### Datasets

* **Source**:
  `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/`
  * **Reuse method**: read at runtime via `MORPHOLOGY_SWC_PATH` (already wired in t0057's
    `paths.py`).
  * **What it is**: t0009 Strahler-calibrated 141009_Pair1DSGC SWC reconstruction, identical to
    [t0052] / [t0053] / [t0054] / [t0055] / [t0057].
* **Source**: `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/`
  * **Reuse method**: read at runtime via `TARGET_TUNING_CURVE_CSV` for RMSE-vs-target metrics
    (already wired in t0057's `paths.py` and `compute_metrics.py`).

## Lessons Learned

* **The 0.667 Hz single-spike-per-trial regime is the convergent failure mode of the entire
  minimal-DSGC family.** Five tasks ([t0052], [t0053], [t0054], [t0055], [t0057]) all topped out
  there. The t0059 task's primary contribution to ruling this out is the gAMPA sweep up to 4.0 nS
  (8x the long-fixed 0.5 nS). If the multi-spike regime still does not appear at gAMPA = 4.0 nS, the
  5x5 grid will at least bracket the boundary precisely.
* **Tonic GABA at 1.5 nS or 2.0 nS fully suppresses, at 0.25 / 0.5 / 1.0 nS does not modulate the
  single-spike regime at all.** [t0057]'s headline finding (peak Hz = 0.667 for gGABA <= 1.0 nS, 0.0
  for gGABA >= 1.5 nS) shows there is no intermediate operating point under sustained 1300 ms
  windows. The t0059 sub-0.25 grid (`{0.1, 0.2, 0.5, 1.0, 2.0}`) explores whether even weaker tonic
  GABA can produce graded suppression once the AMPA drive is also varied.
* **Sustained 1300 ms tonic GABA is biologically unrealistic.** Real SAC->DSGC IPSCs envelope over
  100-300 ms as the bar passes the SAC's dendritic field. [t0057]'s rectangular global window was
  the simplest possible substitute for [t0053]'s collapsed Exp2Syn pulse; t0059's per-synapse
  bar-arrival-locked 200 ms windows are the next step toward biological realism on this substrate.
* **The Exp2Syn GABA mechanism in [t0053] decayed away within 100-200 ms of bar arrival, leaving the
  cell uninhibited for the remaining ~1100 ms of the 1500 ms trial.** This was the diagnostic
  finding that motivated [t0057]; the new tonic mechanism cures the over-decay but introduces the
  opposite problem (over-sustained, no longer modulated by bar arrival). The t0059 200 ms window is
  the negotiated middle ground.
* **CVODE is mandatory at this trial budget.** [t0057] dropped per-trial wall-clock from ~75 s
  (fixed-step) to ~3-8 s (CVODE at `atol = 1e-3`). The t0059 sweep is 5x larger than t0057 (9000 vs
  1800 trials); fixed-step would push wall-clock from 8.8 h to ~7.8 days.
* **The MOD compilation pipeline must be invoked exactly once and in the right order.** [t0057]'s
  `ensure_gaba_tonic_compiled` is idempotent and works correctly only when called AFTER
  `load_stdrun` and BEFORE any `h.gaba_tonic(seg)` construction. Calling it in
  `setup_sweep_ artifacts` (line 150 of t0057's `run_tuning_curve.py` [t0057]) is the canonical
  pattern.
* **HH conductance writes are per-segment, not per-section.** The save-and-zero pattern must iterate
  `for seg in section: ...` because NEURON's `seg.hh.gnabar` is segment-scoped. With `nseg = 1`
  (default) on `soma` and `axon_initial_segment`, this is a single segment per section, but the loop
  pattern is robust to future `nseg` increases.
* **EPSP-decay metric returned null on [t0054] and [t0055] due to spike contamination.** Once the
  cell spikes, the AHP and stacked NMDA conductance keep Vm depolarised at trial end, and the EPSP
  envelope never returns below 1/e of peak within the 1500 ms window. [t0054]'s
  `epsp_decay_vs_gnmda.png` shows an empty / null y-axis. The t0059 `EPSP_PASSIVE` mode (HH zeroed
  at soma + AIS) makes this metric well-defined again — RQ5 of the task description.
* **Do not skip the placement bit-identity test.** [t0053] / [t0054] / [t0055] / [t0057] all enforce
  `placement_seed0.json` bit-identity at `POSITION_TOLERANCE = 1e-9`. Drift in this file invalidates
  cross-task comparisons (the AMPA_ONLY 0.667 Hz baseline regression sentinel relies on it). t0059
  must add the same test against t0057's reference.

## Recommendations for This Task

### Architecture Recommendations

1. **Fork [t0057] verbatim, then surgical-edit.** Copy the full 13-module + 4-test [t0057] code tree
   into `tasks/t0059_*/code/`, rewrite import prefixes, then apply the four targeted edits
   (per-synapse window, HH save-and-zero, gAMPA outer loop, 1400 ms TSTOP). This minimises drift and
   keeps the diff auditable. Do NOT attempt to import [t0057]'s code as a library —
   `minimal_dsgc_tonic_gaba_sweep` is task-specific and CLAUDE.md rule 3 forbids cross-task
   non-library imports.
2. **Re-use the [t0057] `gaba_tonic.mod` POINT_PROCESS unchanged.** The mechanism's interface (`g`,
   `t_on`, `t_off`, `ramp_ms`, `e`) already supports per-pair window writes. The only change is in
   the Python `schedule_ei_onsets` function that calls those attributes.
3. **Inherit the [t0057] CVODE bootstrap pattern.** Order: `ensure_neuron_importable` ->
   `load_stdrun` -> `ensure_gaba_tonic_compiled` -> `enable_cvode(atol=1e-3)`. Document this in the
   new `setup_sweep_artifacts` docstring.
4. **Use `tuning_curve_loss` and `tuning_curve_viz` libraries unchanged.** Both libraries are stable
   and registered; the t0059 `compute_metrics.py` and `render_figures.py` should import from them
   exactly as [t0057] does.
5. **Drop the per-synapse activation-time CSV.** Per the task description; the bar-arrival-locked
   windows are explicit in the design and the histogram is no longer informative.

### Test Recommendations

1. **Port `test_quiescent_rest.py`, `test_spatial_gating.py`, and `test_placement_seed0_match.py`
   verbatim** with import-prefix rewrites only. Update the placement reference to point at t0057's
   `placement_seed0.json` rather than t0053's.
2. **Replace `test_gaba_tonic_envelope.py` with `test_bar_locked_ipsp_envelope.py`** that asserts
   the centre of mass of the IPSP voltage envelope shifts with bar direction by an amount consistent
   with stimulus geometry. This is the headline new test for the per-synapse window mechanism.
3. **Add `test_hh_save_and_zero.py`** that runs one FULL trial at one representative
   `(gAMPA, GABA_BASE_NS)` and asserts bit-identity (within 1e-6 mV) against a stored reference
   trace. This guards against accidentally leaving HH disabled in FULL mode.
4. **Add an EPSP_PASSIVE peak-Vm soft gate inside `compute_metrics.py`** that raises if any cell
   exceeds `AP_THRESHOLD_MV = -20.0` in EPSP_PASSIVE mode. This is a validation-time check that the
   save-and-zero is wired correctly.

### Sweep Strategy

1. **Run a dry-run gate at a single grid cell first** (probably `(gAMPA = 1.0, GABA_BASE_NS = 0.5)`,
   the centre of the new grid). Validate FULL <= EPSP_PASSIVE peak rate, EPSP_PASSIVE peak Vm below
   threshold, IPSP_PASSIVE centre-of-mass shifts with direction. Only then commit to the full
   25-cell sweep.
2. **Write all 75 per-(gampa, gaba, mode) variants to one `metrics.json`** in the explicit
   multi-variant format. The legacy flat format does not support this many variants cleanly.
3. **Generate the 6 cross-grid heatmaps** using `pcolormesh` with the gAMPA values on the y-axis and
   GABA_BASE_NS on the x-axis (both log-spaced). Add a regime-boundary contour overlay for the
   multi-spike band (5-50 Hz peak Hz).
4. **Reserve ~9 h wall-clock budget** for the full 9000-trial sweep on local CPU under CVODE. Plan
   implementation to fit within one overnight session.

### Risks to Mitigate

1. **HH save-and-zero must be exception-safe.** Wrap `h.continuerun` in try/finally so that even if
   the simulator raises (NaN voltage, segmentation fault on the dendritic compartments), HH is
   restored before the next trial. Without this, one bad trial could silently disable HH for the
   rest of the sweep.
2. **CSV column count grows.** Each per-mode CSV gains a `gampa_ns` leading column on top of the
   `gaba_base_ns` column inherited from [t0057]. Update column-name constants in `constants.py` and
   downstream readers in `compute_metrics.py` and the new test file.
3. **The 5x5 = 25 grid produces 25 x 12 = 300 PNGs per mode-type plot, plus 6 cross-grid heatmaps =
   ~1500 PNGs total.** Render figures incrementally and cache intermediate metric pickles to allow
   re-rendering without re-running the sweep.
4. **Window collapse for synapses with negative bar-arrival latency.** At theta = 180 deg, some
   synapses' geometric arrival time is negative; [t0057]'s `_onset_time_ms` clamps this to 0 with
   `max(raw_t, 0.0) + BASE_OFFSET_MS`. Verify that the per-pair `t_off_i = onset_ms + WINDOW_MS`
   computation handles this correctly (it does, because `onset_ms` is already clamped).

## Common Patterns

### Path Centralisation

[t0057] and the entire minimal-DSGC family centralise all paths in a `paths.py` module: morphology
SWC path, all per-mode CSV paths, the placement JSON, the NEURON DLL paths, the wallclock log JSON.
The t0059 fork inherits this pattern verbatim — every file path is a constant in `paths.py`, and
every script reads it from there.

### Constants Module With Numeric Pin

`constants.py` in [t0057] is the single source of truth for every numeric simulation parameter:
TSTOP_MS, DT_MS, AMPA_E_MV / TAU1 / TAU2 / PEAK, GABA_E_MV / RAMP_MS, AIS dimensions, HH
conductances, V_INIT_MV, AP_THRESHOLD_MV. The t0059 fork extends this with `WINDOW_MS = 200.0` and
`AMPA_PEAK_NS_VALUES = (0.5, 1.0, 2.0, 3.0, 4.0)`. No hardcoded magic numbers in any other module.

### CSV Schema Convention

Every per-mode CSV in the minimal-DSGC family has a leading set of "indexer" columns followed by the
metric columns: `(angle_deg, trial_seed, ...)` -> `(gaba_base_ns, angle_deg, trial_seed, ...)` in
[t0057] -> `(gampa_ns, gaba_base_ns, angle_deg, trial_seed, ...)` in t0059. Column-name constants in
`constants.py` (`COL_GAMPA_NS`, `COL_GABA_BASE_NS`, `COL_ANGLE_DEG`, etc.) ensure producer-consumer
agreement.

### Frozen Dataclasses Throughout

Every internal data container in [t0057] is a `@dataclass(frozen=True, slots=True)`: `EiPair`,
`Location`, `ScheduleResult`, `TrialResult`, `CellHandles`, `CellBuildSummary`, `SweepArtifacts`,
`ModeOutputPaths`, `CurveKey`. The t0059 fork inherits this pattern for every new container
including `HhConductanceSnapshot` introduced for the save-and-zero machinery.

## Architecture Overview

The t0059 library has the same 13-module structure as the [t0057] library, plus the same 4 test
files (one of which is renamed and rewritten). The data flow is:

```text
neuron_bootstrap.py  -- (NEURON import + CVODE + GabaTonic.mod compile)
       |
       v
swc_io.py + cell.py  -- (SWC parse + NEURON cell construction)
       |
       v
placement.py         -- (uniform-random N=100 dendritic locations, seed=0)
       |
       v
synapses.py          -- (build EiPair list + per-trial schedule with
       |                 per-synapse bar-arrival-locked windows)
       v
trial.py             -- (run_one_trial with HH save-and-zero for
       |                 EPSP_PASSIVE / IPSP_PASSIVE; FULL keeps HH)
       v
run_tuning_curve.py  -- (5 gampa x 5 gaba x 12 angles x 10 trials x 3 modes
       |                 = 9000 trials, dry-run gates, CSV writers)
       v
compute_metrics.py   -- (75-variant metrics.json + cross-grid summary
       |                 derived_quantities.json + EPSP_PASSIVE peak-Vm gate)
       v
render_figures.py    -- (per-cell V/EPSP/IPSP/PSTH/polar plots, plus
                         6 cross-grid heatmaps + regime-boundary contour)
```

External integration points:

* `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss` — `compute_metrics.py`
  imports `compute_dsi`, `compute_hwhm_deg`, `compute_peak_hz`, `compute_null_hz`,
  `compute_reliability`, `load_tuning_curve`, `TuningCurve`, `score`.
* `tasks.t0011_response_visualization_library.code.tuning_curve_viz` — `render_figures.py` imports
  `plot_polar_tuning_curve`, `plot_cartesian_tuning_curve`, `plot_angle_raster_psth`,
  `plot_multi_model_overlay`, `OKABE_ITO`.
* `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/` --
  read at runtime as `MORPHOLOGY_SWC_PATH`.
* `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/` — read at runtime
  as `TARGET_TUNING_CURVE_CSV` for RMSE-vs-target metrics.

## Test Coverage

The four test files inherited and adapted from [t0057] cover four orthogonal correctness axes:

* **Quiescent rest (`test_quiescent_rest.py`)** — passive 200 ms run with no synapses; asserts
  V_rest = -65 mV +/- 0.5 mV. Catches HH / passive-cable misconfiguration.
* **Spatial gating (`test_spatial_gating.py`)** — 4-test sweep of `i_synapse_fires` predicate
  including a 1000-sample uniform-random active-fraction-near-half check. Catches centripetal-
  gating drift.
* **Placement bit-identity (`test_placement_seed0_match.py`)** — compares the saved
  `placement_seed0.json` against t0057's reference at `POSITION_TOLERANCE = 1e-9`. Catches drift in
  the synapse-placement RNG.
* **Bar-locked IPSP envelope (`test_bar_locked_ipsp_envelope.py`, NEW)** — replaces t0057's
  `test_gaba_tonic_envelope.py`. Asserts that the centre of mass of the IPSP voltage envelope at
  theta = 0 differs from theta = 90 by an amount consistent with the synapse coordinates and the
  bar-arrival-latency formula. Catches per-synapse window failure.

A NEW fifth test (`test_hh_save_and_zero.py`) is added to cover the HH save-and-zero correctness
gate from the verification criteria. All five tests are run by
`pytest tasks/t0059_*/code/test_*.py -v` and gate the implementation step.

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 DSGC
* **Status**: completed
* **Relevance**: Original ModelDB 189347 port. Library `modeldb_189347_dsgc` is not relevant to
  t0059 (different DSGC paradigm — network-level inputs and active dendrites), but cited in the
  Library Landscape as one of the 14 enumerated libraries.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response Visualization Library
* **Status**: completed
* **Relevance**: Provides `tuning_curve_viz` library used unchanged by t0059's `render_figures.py`
  for per-cell polar / Cartesian / raster+PSTH plots and the multi-model overlay.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning Curve Scoring / Loss Library
* **Status**: completed
* **Relevance**: Provides `tuning_curve_loss` library used unchanged by t0059's `compute_metrics.py`
  for DSI, peak Hz, null Hz, HWHM, reliability, and RMSE-vs-target metrics on each of the 75
  variants.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Reproduce Poleg-Polsky 2016 Exact
* **Status**: completed
* **Relevance**: Cited in Library Landscape as one of the 14 enumerated libraries
  (`modeldb_189347_dsgc_exact`); not directly used by t0059. Establishes the project's reference for
  full-detail DSGC paradigms not used in the minimal-DSGC family.

### [t0052]

* **Task ID**: `t0052_minimal_dsgc_scalar_gaba`
* **Name**: Minimal From-Scratch DSGC With Scalar gabaMOD Inhibition
* **Status**: completed
* **Relevance**: First minimal-DSGC family member. Establishes the 100 E + 100 I co-located synapse
  architecture, uniform-random seed-0 placement, position-gated AMPA, soma + AIS HH pattern that
  t0059 inherits. Establishes the convergent 0.667 Hz single-spike-per-trial baseline that t0059's
  gAMPA sweep is designed to break.

### [t0053]

* **Task ID**: `t0053_minimal_dsgc_spatial_gaba`
* **Name**: Minimal From-Scratch DSGC With Spatial PD/ND-Asymmetric Inhibition
* **Status**: completed
* **Relevance**: Establishes the centripetal-gating predicate `i_synapse_fires` (cos(theta_stim
  - theta_centrifugal) < 0) that t0059 inherits unchanged. The full inhibitory-suppression failure
    mode at gGABA = 2 nS motivates t0057's tonic-window mechanism that t0059 forks.

### [t0054]

* **Task ID**: `t0054_minimal_dsgc_ampa_nmda_scalar_gaba`
* **Name**: Minimal DSGC With AMPA + NMDA Excitation and Scalar gabaMOD Inhibition
* **Status**: completed
* **Relevance**: Demonstrates that NMDA on the E pathway breaks the 0.667 Hz regime (peak Hz reaches
  8.0) but collapses DSI. Out of scope for t0059 (AMPA-only), but documents the EPSP-decay-null
  failure mode that S-0055-01's EPSP_PASSIVE mode is designed to fix — RQ5 of the t0059 task
  description.

### [t0055]

* **Task ID**: `t0055_nmda_mg_block_dsi_recovery`
* **Name**: Add Mg-Block NMDA to Recover DSI in t0054 Minimal Architecture
* **Status**: completed
* **Relevance**: Source of the custom-MOD-compilation pattern (`run_nrnivmodl.cmd` shim +
  `ensure_<mech>_compiled` bootstrap) that [t0057] reused for `gaba_tonic.mod` and that t0059
  inherits via the [t0057] fork. Confirms that scalar gabaMOD inhibition holds Vm too hyperpolarised
  for Mg-block NMDA to unblock — independent of the t0059 substrate, but motivates the
  bar-arrival-locked window's explicit per-direction modulation.

### [t0057]

* **Task ID**: `t0057_tonic_gaba_sweep_t0053`
* **Name**: Tonic GABA + Amplitude Sweep on t0053 Spatial DSGC
* **Status**: completed
* **Relevance**: Primary upstream substrate. Provides the entire 13-module + 4-test
  `minimal_dsgc_tonic_gaba_sweep` library that t0059 forks. The `gaba_tonic.mod` POINT_PROCESS, the
  CVODE bootstrap, the per-mode CSV-writer pattern, the dry-run gate machinery, the 15-variant
  `metrics.json` schema, and the placement-bit-identity test all originate here. The convergent
  negative result (peak Hz = 0.667 below 1.5 nS, peak Hz = 0.0 above) motivates the t0059 gAMPA +
  sub-0.25 GABA + bar-locked-window combination.
