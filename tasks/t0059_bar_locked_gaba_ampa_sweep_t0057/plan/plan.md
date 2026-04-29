---
spec_version: "2"
task_id: "t0059_bar_locked_gaba_ampa_sweep_t0057"
date_completed: "2026-04-29"
status: "complete"
---
# Plan: Bar-Arrival-Locked Tonic GABA + AMPA Escape Sweep on t0057 Substrate

## Objective

Fork the t0057 `minimal_dsgc_tonic_gaba_sweep` library and apply three bundled changes on the same
calibrated DSGC morphology that t0052 / t0053 / t0057 have used: (a) replace t0057's global tonic
GABA window `(t_on, t_off) = (100, 1400)` ms with a per-synapse bar-arrival-locked window
`t_on_i = (x_i cos theta + y_i sin theta) / v + 100 ms`, `t_off_i = t_on_i + 200 ms` gated by the
same centripetal-gating predicate from t0053; (b) add the `EPSP_PASSIVE` / `IPSP_PASSIVE` modes that
share synapse activation but save-and-zero `gnabar_hh` / `gkbar_hh` on `soma` and
`axon_initial_segment` (replacing t0057's legacy `AMPA_ONLY` / `GABA_ONLY`); and (c) sweep a 5x5
`(gAMPA, GABA_BASE_NS)` grid replacing t0057's 1-D GABA-only sweep, with
`gAMPA in {0.5, 1.0, 2.0, 3.0, 4.0}` nS and `GABA_BASE_NS in {0.1, 0.2, 0.5, 1.0, 2.0}` nS. Trial
length is standardised to 1400 ms per the S-0055-01 protocol fix. "Done" means: a registered library
asset `minimal_dsgc_bar_locked_gaba_ampa_sweep` exists; per-cell V(t) / EPSP / IPSP / PSTH PNGs and
a polar tuning curve are produced for each of the 25 grid cells; six cross-grid heatmaps (primary
DSI, vector-sum DSI, peak Hz, null Hz, HWHM, RMSE vs t0004) plus a regime-boundary contour overlay
are produced; a 75-variant `metrics.json` (5 gAMPA x 5 GABA x 3 modes) is written; the new
bar-locked IPSP centre-of-mass shift regression test passes; the new HH save-and-zero bit-identity
regression test passes; and `verify_plan.py`, `verify_research_code.py`, `verify_task_metrics.py`,
and the library asset verificator all pass with 0 errors.

## Task Requirement Checklist

The operative task text from `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/task_description.md` is:

> Build the new bar-arrival-locked tonic GABA mechanism, integrate it into a fork of t0057's minimal
> DSGC code, ship the corrected measurement-protocol trio, sweep a 5x5 (gAMPA, GABA_BASE_NS) grid,
> and report whether any operating point on the swept grid produces non-trivial direction
> selectivity in the multi-spike regime — or rule it out.

> Sweep: `gAMPA in {0.5, 1.0, 2.0, 3.0, 4.0}` nS and `GABA_BASE_NS in {0.1, 0.2, 0.5, 1.0, 2.0}` nS,
> `window_ms = 200` (FIXED). Total grid: 25 cells. Per cell: 12 directions x 10 trials x 3 modes
> (FULL / EPSP_PASSIVE / IPSP_PASSIVE) = 360 trials. Total: 9000 trials. Estimated wall-clock ~8.75
> h on local CPU under CVODE.

> Library Asset: produce one library asset `minimal_dsgc_bar_locked_gaba_ampa_sweep` (or similar
> slug). Same 13-module structure as `minimal_dsgc_tonic_gaba_sweep` from t0057, with three
> substantive changes: (a) the GABA driver computes per-synapse `(t_on_i, t_off_i)` from synapse
> coordinate and stimulus direction; (b) the trial-mode dispatcher exposes `FULL`, `EPSP_PASSIVE`,
> `IPSP_PASSIVE`; HH save-and-zero is implemented inside the passive-mode entry points; (c) `gAMPA`
> is exposed as a public per-synapse parameter (was hard-coded at 0.5 nS in t0057).

The full task description is at `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/task_description.md`.

| ID | Requirement | Satisfying step(s) | Evidence of completion |
| --- | --- | --- | --- |
| REQ-1 | Per-synapse bar-arrival-locked GABA window: `t_on_i = (x_i cos theta + y_i sin theta) / v + 100`, `t_off_i = t_on_i + 200` ms; reuse t0057's `gaba_tonic.mod` POINT_PROCESS unchanged. | Steps 4, 8 | `code/synapses.py::schedule_ei_onsets` writes per-pair `t_on` / `t_off` from each pair's `onset_ms` plus `WINDOW_MS = 200.0`; `code/test_bar_locked_ipsp_envelope.py` passes. |
| REQ-2 | Spatial centripetal-gating predicate from t0053 / t0057 preserved bit-for-bit (`cos(theta_stim - theta_centrifugal) < 0`); active synapses get `g = GABA_BASE_NS * 1e-3 (uS)`, silent synapses get `g = 0` and a collapsed window. | Step 8 | `i_synapse_fires` predicate identical to t0057's; `test_spatial_gating.py` passes 4/4. |
| REQ-3 | Add `EPSP_PASSIVE` and `IPSP_PASSIVE` trial modes that save-and-zero `gnabar_hh` / `gkbar_hh` on `soma` and `axon_initial_segment` only, restore via try/finally. Drop legacy `AMPA_ONLY` / `GABA_ONLY`. | Steps 6, 9 | `code/constants.py::TrialMode` has members `{FULL, EPSP_PASSIVE, IPSP_PASSIVE}`; `code/trial.py::run_one_trial` wraps `h.continuerun` in try/finally with `_save_and_zero_hh` / `_restore_hh` helpers; `code/test_hh_save_and_zero.py` passes. |
| REQ-4 | Standardise trial length at `TSTOP_MS = 1400.0` ms per S-0055-01 (was 1500 ms in t0057). | Step 4 | `code/constants.py` reads `TSTOP_MS = 1400.0`; firing-rate normalisation in `compute_metrics.py` divides by 1.4 s. |
| REQ-5 | Drop the per-synapse activation-time histogram CSV and downstream PNG (no longer informative once the bar-arrival-locked windows are explicit in the schedule). | Steps 10, 13 | t0057's `_write_activation_times_csv` is removed from `code/run_tuning_curve.py`; `synapse_onset_times_ms` field of `TrialResult` becomes optional; no `activation_times.csv` and no per-synapse activation-time PNGs are produced. |
| REQ-6 | Sweep `gAMPA in {0.5, 1.0, 2.0, 3.0, 4.0}` nS x `GABA_BASE_NS in {0.1, 0.2, 0.5, 1.0, 2.0}` nS x 12 directions x 10 trials x 3 modes = 9000 trials. | Steps 10, 11 | Per-mode tuning-curve CSVs contain 5 (`gampa_ns`) x 5 (`gaba_base_ns`) x 12 (`angle_deg`) = 300 rows per mode; spike CSVs contain 9000 unique trial rows. |
| REQ-7 | Expose `gAMPA` as a public per-synapse parameter (was hard-coded at 0.5 nS in t0057). | Steps 4, 8, 9, 10 | `code/constants.py` declares `AMPA_PEAK_NS_VALUES = (0.5, 1.0, 2.0, 3.0, 4.0)`; `schedule_ei_onsets`, `run_one_trial`, and the outer `run_full_sweep` loop all accept `gampa_ns: float`; library `entry_points` includes `AMPA_PEAK_NS_VALUES`. |
| REQ-8 | Library asset `minimal_dsgc_bar_locked_gaba_ampa_sweep` registered per `meta/asset_types/library/specification.md` (v2) with `AMPA_PEAK_NS_VALUES`, `GABA_BASE_NS_VALUES`, `WINDOW_MS`, the new `TrialMode` members, and the new `_save_and_zero_hh` / `_restore_hh` helpers exposed as public entry points. | Step 14 | `assets/library/minimal_dsgc_bar_locked_gaba_ampa_sweep/details.json` exists; `description.md` documents the public API; library verificator passes with 0 errors. |
| REQ-9 | For each of the 25 grid cells: 12 PNGs of soma V(t) (FULL), 12 PNGs of aggregate EPSP at soma (EPSP_PASSIVE), 12 PNGs of aggregate IPSP at soma (IPSP_PASSIVE), 12 PNGs of firing-rate PSTH (FULL), and a polar tuning curve (1 PNG). | Step 13 | `results/images/` contains 25 x (12 + 12 + 12 + 12 + 1) = 1225 per-cell PNGs (file-name format: `<family>_gampa_<value>_gaba_<value>_theta_<angle>.png`). |
| REQ-10 | Cross-grid summary heatmaps: primary DSI, vector-sum DSI, peak Hz, null Hz, HWHM, RMSE vs t0004 target — each as a 2-D `(gAMPA, GABA_BASE_NS)` heatmap. | Step 13 | `results/images/heatmap_<metric>.png` for the six metrics; rendered via `matplotlib.pyplot.pcolormesh` with `gampa_ns` on one axis and `gaba_base_ns` on the other. |
| REQ-11 | Regime-boundary contour overlay: `single-spike-degenerate` (peak Hz ~ 0.667), `multi-spike` (5-50 Hz), `full-suppression` (peak Hz ~ 0) bands on the `(gAMPA, GABA_BASE_NS)` plane. | Step 13 | `results/images/regime_boundary_contour.png` rendered via `matplotlib.pyplot.contour` with three explicit contour levels. |
| REQ-12 | Per-grid-cell `metrics.json` entries with primary DSI, vector-sum DSI, preferred direction, peak Hz, null Hz, HWHM, RMSE vs t0004 — for each of the three modes. | Step 12 | `results/metrics.json` contains 75 variants (5 x 5 x 3) with `dimensions = {"mode": ..., "gampa_ns": ..., "gaba_base_ns": ...}` and the four registered metrics (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`) populated per FULL variant. |
| REQ-13 | Bar-locked IPSP envelope regression: the centre of mass of the IPSP voltage envelope at `theta = 0` and `theta = 90` differs by an amount consistent with the synapse-coordinate-derived bar-arrival-latency formula. | Steps 9, 11 | `code/test_bar_locked_ipsp_envelope.py` asserts ` |
| REQ-14 | HH save-and-zero correctness regression: at one representative `(gAMPA, GABA_BASE_NS)` point the FULL trace under the new code is bit-identical (within 1e-6 mV) to a reference produced from a code path with HH active throughout. | Steps 9, 11 | `code/test_hh_save_and_zero.py` runs one FULL trial and asserts `numpy.allclose(actual, reference, atol=1e-6)` against a stored `.npy` reference trace. |
| REQ-15 | EPSP_PASSIVE peak Vm < spike threshold (~ -50 mV) at every direction and grid cell — soft gate that the save-and-zero is wired correctly. | Step 12 | `code/compute_metrics.py` raises `RuntimeError` if any EPSP_PASSIVE trace exceeds `AP_THRESHOLD_MV = -20.0` mV; explicit assertion logged in implementation log. |
| REQ-16 | Same fixed placement seed (0) as t0052 / t0053 / t0057; placement_seed0 match test passes bit-for-bit against t0057's `placement_seed0.json`. | Steps 7, 11 | `code/test_placement_seed0_match.py` passes against `tasks/t0057_tonic_gaba_sweep_t0053/results/placement_seed0.json` at `POSITION_TOLERANCE = 1e-9`. |
| REQ-17 | Compile and load the (unchanged) `gaba_tonic.mod` POINT_PROCESS via the existing `code/run_nrnivmodl.cmd` shim and a renamed `_T0059_NEURONHOME_BOOTSTRAPPED` sentinel. | Step 5 | `code/mod/nrnmech.dll` builds; `hasattr(h, "gaba_tonic")` returns True after `ensure_gaba_tonic_compiled()`; bootstrap order is `ensure_neuron_importable -> load_stdrun -> ensure_gaba_tonic_compiled -> enable_cvode(atol=1e-3)`. |
| RQ1 | Does any `(gAMPA, GABA_BASE_NS)` grid cell produce FULL-mode peak Hz in the **5-50 Hz** multi-spike band? | Step 12, downstream summary | `results/derived_quantities.json` records peak Hz per grid cell; the answer is read directly from the heatmap and contour. |
| RQ2 | Among grid cells in the multi-spike regime, does any produce vector-sum DSI > 0.3? | Step 12 | `results/derived_quantities.json` records vector-sum DSI per cell; cross-referenced with the multi-spike band from RQ1. |
| RQ3 | Does the bar-arrival-locked window mechanism produce direction-dependent IPSP timing the global-window t0057 mechanism could not? | Steps 9, 13 | `code/test_bar_locked_ipsp_envelope.py` (REQ-13) is the formal test; the IPSP_PASSIVE per-direction PNGs are the visual evidence. |
| RQ4 | Where does the regime boundary lie between single-spike-degenerate, multi-spike, and full-suppression behaviour on the `(gAMPA, GABA_BASE_NS)` plane? | Step 13 | `results/images/regime_boundary_contour.png` (REQ-11) is the formal answer. |
| RQ5 | With clean spike-free EPSP_PASSIVE / IPSP_PASSIVE traces, does the EPSP-decay metric become well-defined again (was null on t0054 / t0055)? | Step 12 | `results/derived_quantities.json` records the EPSP-decay value per (gAMPA, GABA_BASE_NS, direction); per-cell EPSP_PASSIVE PNGs are inspected for non-null decay envelopes. |

## Approach

### Technical Approach

The chosen approach forks t0057's 13-module library verbatim, rewrites all import prefixes to
`tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.*`, then applies four targeted edits identified
in `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/research/research_code.md`:

1. **Per-synapse bar-arrival-locked GABA window in `code/synapses.py`.** Replace t0057's three-line
   constant write at `synapses.py` lines 217-219 (`pair.gaba_syn.t_on = T_ON_MS`,
   `pair.gaba_syn.t_off = T_OFF_MS`) with `pair.gaba_syn.t_on = onset_ms`,
   `pair.gaba_syn.t_off = onset_ms + WINDOW_MS`. `onset_ms` is already computed in the same loop
   body via `_onset_time_ms` (lines 166-177 of t0057's `synapses.py`), which uses
   `max(raw_t, 0.0) + BASE_OFFSET_MS = 100 ms`. The `gaba_tonic.mod` POINT_PROCESS is unchanged —
   only the Python caller writes different values per pair.

2. **HH save-and-zero in `code/trial.py`.** Replace t0057's `AMPA_ONLY` / `GABA_ONLY` mode toggles
   in `_apply_mode_weights` (`trial.py` lines 56-76) with `EPSP_PASSIVE` / `IPSP_PASSIVE` toggles
   that additionally save and zero `gnabar_hh`, `gkbar_hh` on `soma` and `axon_initial_segment`
   only. Wrap `h.continuerun` in try/finally so HH is always restored. Save / restore is per-segment
   (`for seg in section: ...`) because NEURON's `seg.hh.gnabar` is segment-scoped. Dendrites have no
   HH mechanism in t0057, so save-and-zero must NOT touch them — attempting `seg.hh.gnabar = 0` on
   a dendrite would raise.

3. **Outer `gampa_ns` loop in `code/run_tuning_curve.py`.** Add
   `AMPA_PEAK_NS_VALUES = (0.5, 1.0, 2.0, 3.0, 4.0)` to `constants.py` and replace
   `GABA_BASE_NS_VALUES = (0.25, 0.5, 1.0, 1.5, 2.0)` with `(0.1, 0.2, 0.5, 1.0, 2.0)`. Thread
   `gampa_ns` through `schedule_ei_onsets`, `run_one_trial`, and `run_full_sweep`. Add `gampa_ns` as
   the leading column to every per-mode CSV header. Drop the activation-time CSV writer.

4. **TSTOP_MS 1500 -> 1400 in `code/constants.py`.** One-character change. The firing-rate
   normalisation in `compute_metrics.py` (which divides spike counts by `TSTOP_MS / 1000.0`)
   tightens by ~7%. The IPSP-sustained-window check at `IPSP_SUSTAINED_T_LATE_MS = 1300.0` is
   replaced by the new bar-locked centre-of-mass shift test.

The CVODE bootstrap order from t0057 is preserved verbatim:
`ensure_neuron_importable -> load_stdrun -> ensure_gaba_tonic_compiled -> enable_cvode(atol=1e-3)`.
Without CVODE, fixed-step at ~75 s/trial would push the 9000-trial sweep from ~8.8 h to ~7.8 days.

The code-research stage cataloged every reusable file:

* **Cross-task library imports (registered libraries — no copying)**:
  `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss` (provides `compute_dsi`,
  `compute_hwhm_deg`, `compute_peak_hz`, `compute_null_hz`, `compute_reliability`,
  `load_tuning_curve`, `TuningCurve`, `score`) and
  `tasks.t0011_response_visualization_library.code.tuning_curve_viz` (provides
  `plot_polar_tuning_curve`, `plot_cartesian_tuning_curve`, `plot_angle_raster_psth`,
  `plot_multi_model_overlay`, `OKABE_ITO`).

* **Copy-and-adapt sources from t0057** (CLAUDE.md rule 3 forbids cross-task non-library imports;
  `minimal_dsgc_tonic_gaba_sweep` is task-specific and must be copied):
  `tasks/t0057_tonic_gaba_sweep_t0053/code/{cell.py, swc_io.py, placement.py, synapses.py, trial.py, run_tuning_curve.py, compute_metrics.py, render_figures.py, metrics_extra.py, neuron_bootstrap.py, paths.py, constants.py, mod/GabaTonic.mod, run_nrnivmodl.cmd, test_quiescent_rest.py, test_spatial_gating.py, test_placement_seed0_match.py}`.
  Rewrite all import prefixes from `tasks.t0057_tonic_gaba_sweep_t0053.code.*` to
  `tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.*` and rename the
  `_T0057_NEURONHOME_BOOTSTRAPPED` sentinel to `_T0059_NEURONHOME_BOOTSTRAPPED`.

* **Datasets read at runtime** (no copying — paths are wired in `paths.py`):
  `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/`
  (the calibrated SWC, identical to t0052 / t0053 / t0057) and
  `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/` (RMSE reference).

### Recommended Task Type(s)

`task.json` already declares `task_types: ["build-model", "experiment-run"]`. Both apply:

* **`build-model` Planning Guidelines** steered (a) the explicit hyperparameter logging requirement
  (per-grid-cell `gampa_ns`, `gaba_base_ns`, mode, seed, dt, `TSTOP_MS`, `WINDOW_MS`,
  `BASE_OFFSET_MS`, `atol`); (b) the explicit metrics variants format (75 variants in
  `metrics.json`); and (c) the model asset (here a library asset embedding the simulation code). No
  `model` asset is produced because the substrate is the calibrated DSGC morphology + computational
  mechanism, not a learned model — `expected_assets` in `task.json` is `{"library": 1}` and
  matches.

* **`experiment-run` Planning Guidelines** steered (a) the hypothesis-style framing (RQ1-RQ5 above);
  (b) the per-condition metrics breakdown (75 variants, one per `(gampa, gaba, mode)`); (c) the
  saved-predictions equivalent (per-trial spike CSVs and per-direction voltage traces are the
  diagnostic raw data — there is no separate `predictions` asset because spike trains, not labels,
  are the model's output and they live in `results/spike_times_*.csv`); and (d) explicit baseline
  comparisons (t0004 target peak ~32 Hz, t0052/t0053/t0057 0.667 Hz single-spike degenerate
  baseline, and t0057's 1.5 nS full-suppression baseline). The validation gate at step 11 reads five
  individual trials before committing to the full 9000-trial sweep, per the `experiment-run`
  guideline against running expensive operations with broken pipelines.

### Alternatives Considered

* **Sweep `window_ms` as a third axis.** Rejected: the task description fixes `window_ms = 200` ms
  (biologically motivated midpoint of the 100-300 ms SAC IPSC envelope range). Adding a third axis
  would 3x the trial budget and dilute the experimental signal. A future task can sweep `window_ms`
  on the operating point identified by t0059.

* **Add NMDA on the E pathway via the t0055 Mg-block mechanism.** Rejected: the task description
  explicitly puts NMDA out of scope ("AMPA-only on the E pathway; the AMPA + Mg-block-NMDA
  combination on this bar-locked substrate is the natural next task, covered by the still-active
  S-0057-06"). Mixing the gAMPA escape sweep with NMDA dynamics would confound the diagnosis of
  whether the multi-spike regime is reachable with AMPA alone.

* **Implement the per-synapse window as a global lookup table indexed by (theta, synapse_id) rather
  than per-pair attribute writes.** Rejected: the existing `gaba_tonic.mod` POINT_PROCESS already
  exposes per-instance `t_on` / `t_off` RANGE attributes, so per-pair writes are a one-line surgical
  change. A lookup-table indirection would add a second source of truth for window edges and
  complicate the test surface.

* **Compute IPSP centre-of-mass via an analytic predictor instead of a regression test.** Rejected:
  the regression test surfaces silent breakage of the per-synapse window mechanism (e.g., wrong
  attribute order in `schedule_ei_onsets`) at the cost of one ~30 s test run. An analytic predictor
  alone would not catch implementation bugs, only model-design bugs.

## Cost Estimation

* External API costs: **$0.00** (no LLM calls, no third-party APIs).
* Remote compute: **$0.00** (local CPU only; CVODE keeps the 9000-trial sweep within ~8.75 h
  wall-clock on the user's machine).
* Storage: **$0.00** (all artefacts written under the task folder; per-mode CSVs use stride-8
  voltage downsampling per the t0057 / t0055 guidance to keep disk usage bounded — estimated
  ~150-250 MB total across all 9000 trials).
* Total estimated cost: **$0.00** vs. project budget of $1.00 (`project/budget.json`,
  `total_budget = 1.0`, no paid services declared in `available_services`).

## Step by Step

### Milestone 1: Bootstrap MOD compilation pipeline and constants

1. **Create `code/paths.py` and `code/constants.py`.** Copy
   `tasks/t0057_tonic_gaba_sweep_t0053/code/paths.py` and
   `tasks/t0057_tonic_gaba_sweep_t0053/code/constants.py` to
   `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/paths.py` and `code/constants.py`. Rewrite the
   import prefix `tasks.t0057_tonic_gaba_sweep_t0053` to
   `tasks.t0059_bar_locked_gaba_ampa_sweep_t0057`. In `paths.py` rewrite all per-mode CSV path
   constants to use `epsp_passive` / `ipsp_passive` instead of `ampa_only` / `gaba_only` (e.g.,
   `TUNING_CURVE_EPSP_PASSIVE_CSV`, `SPIKE_TIMES_IPSP_PASSIVE_CSV`,
   `VOLTAGE_TRACES_EPSP_PASSIVE_CSV`). Add `T0057_PLACEMENT_JSON` pointing at
   `tasks/t0057_tonic_gaba_sweep_t0053/results/placement_seed0.json` for the bit-identity test. Drop
   `ACTIVATION_TIMES_CSV` (no longer written). In `constants.py` apply five edits:
   `TSTOP_MS = 1500.0` -> `1400.0`; `TrialMode` members `AMPA_ONLY` / `GABA_ONLY` -> `EPSP_PASSIVE`
   / `IPSP_PASSIVE`; replace `GABA_BASE_NS_VALUES = (0.25, 0.5, 1.0, 1.5, 2.0)` with
   `(0.1, 0.2, 0.5, 1.0, 2.0)`; add
   `AMPA_PEAK_NS_VALUES: tuple[float, ...] = (0.5, 1.0, 2.0, 3.0, 4.0)`; add
   `WINDOW_MS: float = 200.0`. Drop `T_OFF_MS` (no longer needed at synapse layer; window edges are
   computed per pair). Drop `IPSP_SUSTAINED_T_EARLY_MS`, `IPSP_SUSTAINED_T_LATE_MS`, and the
   `AMPA_ONLY_PEAK_HZ_EXPECTED` regression sentinel (these become direction-dependent under the new
   bar-locked windows). Add `COL_GAMPA_NS: str = "gampa_ns"` for the new CSV column. Satisfies
   REQ-4, REQ-7.

2. **Copy the Windows `nrnivmodl` shim verbatim.** Copy
   `tasks/t0057_tonic_gaba_sweep_t0053/code/run_nrnivmodl.cmd` (12 lines, task-agnostic) to
   `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/run_nrnivmodl.cmd`. The script is unchanged.
   Satisfies REQ-17.

3. **Copy the (unchanged) `gaba_tonic.mod` POINT_PROCESS.** Copy
   `tasks/t0057_tonic_gaba_sweep_t0053/code/mod/GabaTonic.mod` to
   `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/mod/GabaTonic.mod`. Zero edits — the
   mechanism's interface (per-instance `g`, `t_on`, `t_off`, `ramp_ms`, `e`) already supports
   per-pair window writes. Smoke-test by running `code/run_nrnivmodl.cmd` standalone first and
   confirming `code/mod/nrnmech.dll` exists with non-zero size before integrating. Satisfies REQ-1,
   REQ-17.

4. **Adapt `code/neuron_bootstrap.py` with the renamed sentinel.** Copy
   `tasks/t0057_tonic_gaba_sweep_t0053/code/neuron_bootstrap.py` (~150 lines). Rewrite import
   prefix. Rename the `_T0057_NEURONHOME_BOOTSTRAPPED` env-var sentinel to
   `_T0059_NEURONHOME_BOOTSTRAPPED`. Rebind `RUN_NRNIVMODL_CMD` and `NRNMECH_DLL` to the
   `tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.paths` constants. Keep the helper API:
   `ensure_neuron_importable`, `load_stdrun`, `ensure_gaba_tonic_compiled`,
   `enable_cvode(*, atol=1e-3)`. Confirm `ensure_gaba_tonic_compiled` is idempotent and that calling
   `h.nrn_load_dll(str(NRNMECH_DLL))` then asserting `hasattr(h, "gaba_tonic")` works. Satisfies
   REQ-17.

### Milestone 2: Port t0057 code skeleton

5. **Copy invariant modules from t0057 (bit-identical apart from import prefix rewrite).** Copy the
   following files from `tasks/t0057_tonic_gaba_sweep_t0053/code/` to
   `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/`: `cell.py` (~215 lines, builds the
   calibrated DSGC; HH only on `soma` and `axon_initial_segment` is already correct), `swc_io.py`
   (~150 lines, SWC parser), `placement.py` (~120 lines,
   `sample_dendritic_locations(*, cell, n_pairs, seed)` +
   `save_placement_json(*, locations, out_path)`; bit-identical to t0053 / t0057 with `seed = 0`),
   `metrics_extra.py` (~75 lines, `compute_vector_sum_dsi`, `compute_preferred_direction_deg`).
   Rewrite import prefix. No logic changes. Satisfies REQ-16 (preserves the placement contract).

6. **Adapt `code/synapses.py` for per-synapse bar-arrival-locked windows.** Copy
   `tasks/t0057_tonic_gaba_sweep_t0053/code/synapses.py` (~230 lines). Keep these unchanged (apart
   from import prefix rewrite): the `EiPair` dataclass field set, the `i_synapse_fires` predicate
   (lines 76-91 — bit-identical centripetal gating), the `theta_centrifugal_rad` precomputation
   (lines 146-149), the `_onset_time_ms` helper (lines 166-177), and the AMPA construction
   (`Exp2Syn` with `tau1 = 0.5 ms`, `tau2 = 2.5 ms`, `e = 0 mV`; `NetStim` + `NetCon` plumbing).
   Apply two surgical edits:

   * Replace lines 217-219 of t0057's `synapses.py` (the constant `T_ON_MS` / `T_OFF_MS` writes)
     with:
     `pair.gaba_syn.g = gaba_full_g_us; pair.gaba_syn.t_on = onset_ms; pair.gaba_syn.t_off = onset_ms + WINDOW_MS`
     where `WINDOW_MS = 200.0` is imported from
     `tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants`.

   * Add `gampa_ns: float` parameter to `schedule_ei_onsets`. Replace the previously hard-coded AMPA
     peak (line 142 of t0057's `synapses.py`) with `pair.ampa_netcon.weight[0] = gampa_ns * 1e-3`.
     For silent (non-firing) I synapses keep the t0057 zero pattern:
     `pair.gaba_syn.g = 0.0; pair.gaba_syn.t_on = 0.0; pair.gaba_syn.t_off = 0.0`. Drop the
     `T_OFF_MS` import.

   Satisfies REQ-1, REQ-2, REQ-7.

### Milestone 3: HH save-and-zero and trial dispatcher

7. **Adapt `code/trial.py` for HH save-and-zero in EPSP_PASSIVE / IPSP_PASSIVE.** Copy
   `tasks/t0057_tonic_gaba_sweep_t0053/code/trial.py` (~165 lines). Add a frozen dataclass
   `HhConductanceSnapshot(soma_gnabar: float, soma_gkbar: float, ais_gnabar: float, ais_gkbar: float)`
   with `frozen=True, slots=True`. Add two helpers:

   * `_save_and_zero_hh(*, cell: CellHandles) -> HhConductanceSnapshot`: iterate
     `for seg in cell.soma: ...` and `for seg in cell.axon_initial_segment: ...`, read
     `seg.hh.gnabar` and `seg.hh.gkbar`, save into a dict, then write `seg.hh.gnabar = 0.0` and
     `seg.hh.gkbar = 0.0`. Return the snapshot.

   * `_restore_hh(*, cell: CellHandles, snapshot: HhConductanceSnapshot) -> None`: iterate the same
     segments and write the saved values back.

   Rewrite `_apply_mode_weights` (t0057's `trial.py` lines 56-76):

   * **EPSP_PASSIVE**: zero every fired pair's GABA `g` / `t_on` / `t_off` (analogous to t0057
     `AMPA_ONLY`); the caller of `run_one_trial` invokes `_save_and_zero_hh` before `h.continuerun`.

   * **IPSP_PASSIVE**: zero every pair's AMPA `weight[0]` (analogous to t0057 `GABA_ONLY`); the
     caller invokes `_save_and_zero_hh` before `h.continuerun`.

   * **FULL**: leave both at scheduled values; HH stays active.

   Wrap `h.continuerun` in a try/finally:

   ```python
   snapshot: HhConductanceSnapshot | None = None
   try:
       if mode in {TrialMode.EPSP_PASSIVE, TrialMode.IPSP_PASSIVE}:
           snapshot = _save_and_zero_hh(cell=cell)
       h.continuerun(TSTOP_MS)
   finally:
       if snapshot is not None:
           _restore_hh(cell=cell, snapshot=snapshot)
   ```

   Add `gampa_ns: float` parameter to `run_one_trial` and thread it into the `schedule_ei_onsets`
   call. Add `gampa_ns` field to `TrialResult` for downstream CSV emission. Satisfies REQ-3, REQ-7.

### Milestone 4: Sweep harness, validation gate, and full sweep

8. **Adapt `code/run_tuning_curve.py` for the outer (gampa, gaba) loop.** Copy
   `tasks/t0057_tonic_gaba_sweep_t0053/code/run_tuning_curve.py` (~635 lines). Major changes:

   * Import `AMPA_PEAK_NS_VALUES`, `GABA_BASE_NS_VALUES`, `WINDOW_MS` from
     `tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants`.

   * In `setup_sweep_artifacts()` keep the bootstrap order
     `ensure_neuron_importable -> load_stdrun -> ensure_gaba_tonic_compiled -> enable_cvode(atol=1e-3)`.

   * Add `gampa_ns` outer loop wrapping the existing `gaba_base_ns` loop and the inner
     `(angle, trial, mode)` triple loop. Mirror t0057's loop nesting and progress-bar pattern;
     update the progress-bar total from `5 * 12 * 10 * 3 = 1800` to `5 * 5 * 12 * 10 * 3 = 9000`.

   * Thread `gampa_ns` into `_run_sweep_for_mode` and `run_one_trial`.

   * Add `gampa_ns` as the leading column to every per-mode CSV header and every per-trial spike /
     voltage / aggregate CSV (`tuning_curve_full.csv`, `tuning_curve_epsp_passive.csv`,
     `tuning_curve_ipsp_passive.csv`, `spike_times_<mode>.csv`, `voltage_traces_<mode>.csv`).

   * Drop t0057's `_write_activation_times_csv` (REQ-5).

   * Use stride-8 voltage downsampling for `voltage_traces_<mode>.csv` per t0057 / t0055 guidance.

   Satisfies REQ-5, REQ-6, REQ-7.

9. **Add the bar-locked-IPSP and HH save-and-zero regression tests (port the rest verbatim).** Copy
   `tasks/t0057_tonic_gaba_sweep_t0053/code/test_quiescent_rest.py`,
   `tasks/t0057_tonic_gaba_sweep_t0053/code/test_spatial_gating.py`,
   `tasks/t0057_tonic_gaba_sweep_t0053/code/test_placement_seed0_match.py` to
   `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/`. Rewrite import prefixes; in
   `test_placement_seed0_match.py` update the reference path to `T0057_PLACEMENT_JSON` from
   `paths.py`. Preserve `POSITION_TOLERANCE = 1e-9`. Then create two NEW test files in
   `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/`:

   * **`test_bar_locked_ipsp_envelope.py`** (~100 lines). Run two IPSP_PASSIVE trials at
     `(gampa_ns = 1.0, gaba_base_ns = 1.0)`, one at `theta = 0 deg` and one at `theta = 90 deg`.
     Compute the centre of mass of `|v(t) - V_INIT_MV|` over the trial as a scalar `com_v` (in ms).
     Compute a `predicted_lower_bound` from the 100 synapse coordinates: for each direction, average
     `(x_i cos theta + y_i sin theta) / v + 100 ms` over the active synapses, then take the absolute
     difference between the two direction averages and divide by 2 (a coarse but valid lower bound
     on the centre-of-mass shift). Assert `abs(com_v_at_0 - com_v_at_90) >= predicted_lower_bound`.

   * **`test_hh_save_and_zero.py`** (~80 lines). Run one FULL trial at
     `(gampa_ns = 0.5, gaba_base_ns = 1.0, theta = 0 deg, trial_seed = 0)` and write the soma V(t)
     to a numpy array. Compare against a reference array stored at
     `code/test_data/full_reference_trace.npy` via
     `numpy.testing.assert_allclose(actual, reference, atol=1e-6)`. The reference is generated ONCE
     by running the same trial with `mode = FULL` and HH active throughout (this is the reference
     implementation — the test guards against accidentally leaving HH disabled). On first run when
     no reference exists, the test writes the reference and skips with a "reference created"
     message; subsequent runs compare.

   Run all five tests with
   `uv run pytest tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/test_*.py -v`. Satisfies REQ-2,
   REQ-3, REQ-13, REQ-14, REQ-16.

10. **[CRITICAL] Validation gate: dry-run with one grid cell, two directions, two trials per mode.**
    Before launching the full 9000-trial sweep, run
    `tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.run_tuning_curve --dry-run` (or equivalent
    flag) at `(gampa_ns = 1.0, gaba_base_ns = 0.5)` (the centre of the new grid), `theta in {0, 90}`
    deg, 2 trials, all 3 modes — total 12 trials. Trivial baselines and observable thresholds:

    * **Single-spike-degenerate baseline**: t0057's `AMPA_ONLY` peak Hz = 0.6667 across all
      directions and conductances at `gampa_ns = 0.5 nS`. The new `EPSP_PASSIVE` mode disables HH,
      so by construction it produces 0 spikes (because no spike generator); peak-Hz comparison is
      moot for EPSP_PASSIVE / IPSP_PASSIVE. The relevant baseline is FULL spike count <=
      AMPA_ONLY-equivalent spike count at the same `gampa_ns` (i.e., GABA inhibits, never excites).

    * **EPSP_PASSIVE peak Vm soft gate**: max Vm across the EPSP_PASSIVE trace must be < `-50 mV`
      (well below `AP_THRESHOLD_MV = -20.0`). If not, the save-and-zero is wired wrong.

    * **IPSP centre-of-mass shift**: `abs(com_v_at_0 - com_v_at_90) >= predicted_lower_bound` from
      the same formula as `test_bar_locked_ipsp_envelope.py`. Catches a silent failure of the
      per-synapse window mechanism.

    * **Active fraction at theta=0**: in `[0.30, 0.70]` (the t0053 / t0057 spatial-gating polar
      range).

    **Failure condition**: if EPSP_PASSIVE peak Vm > -50 mV at any direction, or IPSP shift below
    bound, or active fraction outside `[0.30, 0.70]`, or FULL spike count > t0057 AMPA_ONLY spike
    count at the same `gampa_ns`, **STOP** and inspect 5 individual trials per failing mode (read
    raw spike CSV, raw voltage CSV) — do not proceed to the full 9000-trial sweep until the gate
    passes. The dry-run takes ~2 min wall-clock; the full sweep takes ~8.75 h, so the gate is
    mandatory. Satisfies REQ-13, REQ-14, REQ-15.

11. **[CRITICAL] Run the full 9000-trial sweep.** Execute
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0059_bar_locked_gaba_ampa_sweep_t0057 -- uv run python -u -m tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.run_tuning_curve`.
    Expected wall-clock: ~8.75 h on local CPU under CVODE (extrapolated from t0057's measured 6318 s
    for 1800 trials at the same per-trial CVODE budget). Outputs: `results/tuning_curve_full.csv`,
    `results/tuning_curve_epsp_passive.csv`, `results/tuning_curve_ipsp_passive.csv`,
    `results/spike_times_<mode>.csv`, `results/voltage_traces_<mode>.csv`,
    `results/active_fraction_per_direction.csv`, `results/placement_seed0.json`,
    `results/wallclock_log.json`. Verify file sizes are within expectations (per-mode tuning-curve
    CSV ~5 MB each, voltage trace CSV ~50-100 MB each at stride-8). Satisfies REQ-6, REQ-7.

### Milestone 5: Metrics and figures

12. **Adapt `code/compute_metrics.py` for the 75-variant `metrics.json`.** Copy
    `tasks/t0057_tonic_gaba_sweep_t0053/code/compute_metrics.py` (~500 lines). Pivot all loaders by
    `(gampa_ns, gaba_base_ns)` first, then by `mode`. For each `(gampa_ns, gaba_base_ns, mode)`
    triple compute `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
    `tuning_curve_reliability`, `tuning_curve_rmse` (vs t0004 target curve), `peak_hz`, `null_hz`,
    `vector_sum_dsi`, and `preferred_direction_deg`. Emit 5 x 5 x 3 = 75 variants in
    `results/metrics.json` using the explicit multi-variant schema defined in
    `arf/specifications/metrics_specification.md`:

    ```json
    {
      "variants": [
        {
          "variant_id": "gampa_0.50_gaba_0.10_full",
          "dimensions": {"mode": "full", "gampa_ns": 0.5, "gaba_base_ns": 0.1},
          "metrics": {
            "direction_selectivity_index": ...,
            "tuning_curve_hwhm_deg": ...,
            "tuning_curve_reliability": ...,
            "tuning_curve_rmse": ...
          }
        },
        ...
      ]
    }
    ```

    For EPSP_PASSIVE / IPSP_PASSIVE variants, populate only the metrics that are well-defined for
    spike-free traces (specifically `tuning_curve_rmse` will be near the target floor because no
    spikes; `direction_selectivity_index` and `tuning_curve_hwhm_deg` may be computed on the rate
    curve which is uniformly zero — treat these as `null` per
    `arf/styleguide/python_styleguide.md` "Use None for missing data, never zero or empty string").
    Use registered metrics only: `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
    `tuning_curve_reliability`, `tuning_curve_rmse` (from `meta/metrics/`). Use libraries from
    `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`: `compute_dsi`,
    `compute_hwhm_deg`, `compute_peak_hz`, `compute_null_hz`, `compute_reliability`,
    `load_tuning_curve`, `TuningCurve`, `score`, `ScoreReport`. Use `compute_vector_sum_dsi` and
    `compute_preferred_direction_deg` from local
    `tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.metrics_extra`.

    Also write `results/derived_quantities.json` with cross-grid summary arrays per mode:
    `peak_hz_grid`, `null_hz_grid`, `dsi_primary_grid`, `dsi_vector_sum_grid`, `hwhm_grid`,
    `rmse_grid`, `epsp_decay_grid` (per direction; well-defined now under EPSP_PASSIVE per RQ5),
    plus per-direction aggregate EPSP / IPSP envelope traces for the 25 grid cells.

    **EPSP_PASSIVE peak-Vm soft gate**: scan max Vm across all EPSP_PASSIVE traces; if any cell
    exceeds `AP_THRESHOLD_MV = -20.0` mV, raise `RuntimeError` with the offending
    `(gampa_ns, gaba_base_ns, theta_deg)`. This is the wiring check from the task's verification
    criteria. Satisfies REQ-12, REQ-15, RQ1, RQ2, RQ5.

13. **Adapt `code/render_figures.py` for per-cell PNGs and cross-grid heatmaps.** Copy
    `tasks/t0057_tonic_gaba_sweep_t0053/code/render_figures.py` (~480 lines). Each per-direction
    figure family becomes a per-(gampa, gaba, direction) family: the inner loop over 12 angles is
    wrapped by an outer loop over `AMPA_PEAK_NS_VALUES x GABA_BASE_NS_VALUES`. Output PNG names
    encode all three indices, e.g. `soma_v_gampa_1.0_gaba_0.50_theta_180.png`.

    Five per-cell figure families per `(gampa, gaba)` pair: soma V(t) (from FULL), aggregate EPSP
    (from EPSP_PASSIVE), aggregate IPSP (from IPSP_PASSIVE), firing-rate PSTH (from FULL), and the
    polar tuning curve (1 polar PNG per `(gampa, gaba)` cell, FULL mode). Use
    `tasks.t0011_response_visualization_library.code.tuning_curve_viz.plot_polar_tuning_curve(*, df=..., out_path=..., target_df=...)`
    and `plot_cartesian_tuning_curve` for tuning curves; use `plot_angle_raster_psth` for PSTH.

    Add the cross-grid heatmap family: 6 PNGs (`heatmap_dsi_primary.png`,
    `heatmap_dsi_vector_sum.png`, `heatmap_peak_hz.png`, `heatmap_null_hz.png`, `heatmap_hwhm.png`,
    `heatmap_rmse.png`), each rendered via `matplotlib.pyplot.pcolormesh` with `gampa_ns` on one
    axis, `gaba_base_ns` on the other, and the metric value as colour. Both axes log-spaced.

    Add the regime-boundary contour overlay (`regime_boundary_contour.png`): use
    `matplotlib.pyplot.contour` on the FULL peak-Hz grid with three contour levels: 0.5 Hz
    (separating full-suppression from single-spike-degenerate; the 0.667 Hz baseline sits just
    above), 5 Hz (entry to multi-spike regime per RQ1), and 50 Hz (exit). Annotate the three bands
    `single-spike-degenerate`, `multi-spike`, `full-suppression`.

    Total expected PNG count: 25 grid cells x (12 + 12 + 12 + 12 + 1) = 1225 per-cell PNGs + 6
    cross-grid heatmaps + 1 regime-boundary contour + 1 active-fraction polar (carried over from
    t0057, conductance-and-gampa-independent because spatial gating is unchanged) = 1233 PNGs.
    Satisfies REQ-9, REQ-10, REQ-11, RQ4.

### Milestone 6: Library asset

14. **Create the `minimal_dsgc_bar_locked_gaba_ampa_sweep` library asset.** Create
    `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/assets/library/minimal_dsgc_bar_locked_gaba_ampa_sweep/details.json`
    per `meta/asset_types/library/specification.md` (v2). Required fields: `spec_version: "2"`,
    `library_id: "minimal_dsgc_bar_locked_gaba_ampa_sweep"`,
    `name: "Minimal DSGC with Bar-Arrival-Locked Tonic GABA + AMPA Sweep"`, `version: "0.1.0"`,
    `short_description: "Pure-Python NEURON library for a minimal direction-selective ganglion cell with 100 co-located E + I synapses; the GABA branch uses the t0057 gaba_tonic POINT_PROCESS gated by a per-synapse bar-arrival-locked (t_on_i, t_off_i) window; trial-mode dispatcher exposes FULL / EPSP_PASSIVE / IPSP_PASSIVE with HH save-and-zero on soma + AIS for the passive modes; sweeps a 5x5 (gAMPA, GABA_BASE_NS) grid via public AMPA_PEAK_NS_VALUES and GABA_BASE_NS_VALUES constants."`,
    `description_path: "description.md"`,

    `module_paths`: same 13 modules as t0057's library (`code/cell.py`, `code/swc_io.py`,
    `code/placement.py`, `code/synapses.py`, `code/trial.py`, `code/run_tuning_curve.py`,
    `code/compute_metrics.py`, `code/render_figures.py`, `code/metrics_extra.py`,
    `code/neuron_bootstrap.py`, `code/paths.py`, `code/constants.py`, `code/mod/GabaTonic.mod`).

    `entry_points`: include `AMPA_PEAK_NS_VALUES` (function-kind constant in `constants.py`, REQ-7),
    `GABA_BASE_NS_VALUES` (function-kind constant), `WINDOW_MS` (function-kind constant, REQ-1),
    `TrialMode` (class in `constants.py` with members `FULL`, `EPSP_PASSIVE`, `IPSP_PASSIVE` per
    REQ-3), `gaba_tonic` (POINT_PROCESS class via `code/mod/GabaTonic.mod`),
    `ensure_gaba_tonic_compiled` (function), `build_dsgc_from_swc` (function),
    `sample_dendritic_locations` (function), `build_ei_pairs` (function), `i_synapse_fires`
    (function), `schedule_ei_onsets` (function — accepts `gampa_ns: float`),
    `HhConductanceSnapshot` (class in `trial.py`, REQ-3), `_save_and_zero_hh` (function in
    `trial.py`, REQ-3), `_restore_hh` (function in `trial.py`, REQ-3), `run_one_trial` (function —
    accepts `gampa_ns: float`), `run_full_sweep` (function — outer `gampa_ns` loop),
    `compute_metrics_main` (script), `render_figures_main` (script), `compute_vector_sum_dsi`
    (function), `compute_preferred_direction_deg` (function).

    `dependencies: ["neuron", "numpy", "matplotlib", "pandas", "tqdm"]`,
    `test_paths: ["code/test_quiescent_rest.py", "code/test_spatial_gating.py", "code/test_placement_seed0_match.py", "code/test_bar_locked_ipsp_envelope.py", "code/test_hh_save_and_zero.py"]`,
    `categories: ["compartmental-modeling", "direction-selectivity", "synaptic-integration"]` (use
    existing slugs from `meta/categories/`),
    `created_by_task: "t0059_bar_locked_gaba_ampa_sweep_t0057"`, `date_created: "2026-04-29"`.

    Then write `description.md` with YAML frontmatter (`spec_version: "2"`,
    `library_id: "minimal_dsgc_bar_locked_gaba_ampa_sweep"`,
    `documented_by_task: "t0059_bar_locked_gaba_ampa_sweep_t0057"`, `date_documented: "2026-04-29"`)
    and the seven mandatory sections (`## Metadata`, `## Overview`, `## API Reference`,
    `## Usage Examples`, `## Dependencies`, `## Testing`, `## Main Ideas`, `## Summary`). The
    `## API Reference` section must explicitly document `AMPA_PEAK_NS_VALUES`,
    `GABA_BASE_NS_VALUES`, `WINDOW_MS`, the new `TrialMode` members, and the `_save_and_zero_hh` /
    `_restore_hh` helpers as public API surface. Run
    `uv run python -m arf.scripts.verificators.verify_assets t0059_bar_locked_gaba_ampa_sweep_t0057`
    to confirm the library asset passes with 0 errors. Satisfies REQ-8.

## Remote Machines

None required. Local CPU only. CVODE (`atol = 1e-3`) keeps per-trial wall-clock at ~3-8 s, making
the 9000-trial sweep tractable in ~8.75 h on the user's local machine. No GPU is needed —
single-cell compartmental simulation on the t0009-calibrated 141009_Pair1DSGC morphology fits
comfortably in CPU and RAM budget. The user's local machine has already executed t0057's 1800-trial
sweep in 6318 s (~105 min) on this same hardware, validating the extrapolation.

## Assets Needed

* **From [t0009_calibrate_dendritic_diameters]**: the calibrated SWC morphology referenced via
  `tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.paths.MORPHOLOGY_SWC_PATH` pointing at the
  t0009 SWC file (same constant convention as t0057's `paths.py`).

* **From [t0011_response_visualization_library]**: registered library `tuning_curve_viz`, imported
  as
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import ( plot_polar_tuning_curve, plot_cartesian_tuning_curve, plot_angle_raster_psth, plot_multi_model_overlay, OKABE_ITO)`.

* **From [t0012_tuning_curve_scoring_loss_library]**: registered library `tuning_curve_loss`,
  imported as
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import ( TuningCurve, load_tuning_curve, compute_dsi, compute_hwhm_deg, compute_peak_hz, compute_null_hz, compute_reliability, score, ScoreReport)`.

* **From [t0057_tonic_gaba_sweep_t0053]**: 13 source files + `code/run_nrnivmodl.cmd` +
  `code/mod/GabaTonic.mod` + 3 test files copied verbatim into the t0059 `code/` directory (per
  CLAUDE.md rule 3, only registered libraries cross task boundaries via import; non-library code
  must be copied). Also the reference
  `tasks/t0057_tonic_gaba_sweep_t0053/results/placement_seed0.json` is read by
  `test_placement_seed0_match.py` for the bit-identity check.

* **From [t0004_target_tuning_curve]** (indirect via [t0012] / [t0057]): the t0004 target tuning
  curve CSV used as the RMSE reference. Path resolved via `paths.py` (same constant as t0057).

No external download or paid API calls required.

## Expected Assets

* **library: `minimal_dsgc_bar_locked_gaba_ampa_sweep`** — one library asset at
  `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/assets/library/minimal_dsgc_bar_locked_gaba_ampa_sweep/`.
  Contains `details.json` (per `meta/asset_types/library/specification.md` v2) and `description.md`
  (with frontmatter and the seven mandatory sections). Public API surface includes
  `AMPA_PEAK_NS_VALUES`, `GABA_BASE_NS_VALUES`, `WINDOW_MS` constants, `TrialMode` with `FULL` /
  `EPSP_PASSIVE` / `IPSP_PASSIVE` members, `gaba_tonic` POINT_PROCESS,
  `schedule_ei_onsets(*, theta_stim_rad, gampa_ns, gaba_base_ns, pairs, ...)`,
  `HhConductanceSnapshot`, `_save_and_zero_hh(*, cell)`, `_restore_hh(*, cell, snapshot)`,
  `run_one_trial(*, ..., gampa_ns, gaba_base_ns)`, and `run_full_sweep` script entry point.
  Component structure mirrors `minimal_dsgc_tonic_gaba_sweep` (from [t0057]) with the four targeted
  edits identified in research_code.md. Matches `task.json` `expected_assets: {"library": 1}`.

## Time Estimation

* Research: complete (`research/research_code.md` done 2026-04-29).
* Implementation (Milestones 1-3, MOD bootstrap + skeleton port + per-synapse window edit + HH
  save-and-zero): ~90-150 min.
* Implementation (Milestone 4 part 1, sweep harness refactor): ~60-90 min.
* Implementation (Milestone 4 part 2, new regression tests): ~45-60 min.
* Validation (dry-run gate per step 10): ~5-10 min wall-clock; debugging if gate fails: ~30-90 min
  worst case.
* Full sweep (9000 trials, step 11): **~8.75 h** wall-clock on local CPU under CVODE (extrapolated
  from t0057's measured 6318 s for 1800 trials). Recommend running overnight.
* Metrics + plotting (Milestone 5): ~45-60 min (1233 PNGs is matplotlib-heavy; use `Agg` backend).
* Library asset creation (Milestone 6): ~30-45 min.
* Verification (verify_plan.py, verify_research_code.py, verify_task_metrics.py, library asset
  verificator): ~5 min.
* Total: ~12-14 hours including the simulation sweep and a buffer; ~3-5 hours of active human
  attention plus an overnight sweep.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| HH save-and-zero is not exception-safe; one bad trial silently disables HH for the rest of the sweep | Medium | Critical — would silently invalidate every subsequent FULL trial; the spike rate would drop to ~0 across the multi-spike search region | Wrap `h.continuerun` in try/finally so HH is always restored even if NEURON raises (NaN voltage, segfault on dendrites). The `test_hh_save_and_zero.py` regression (REQ-14) catches drift on the canonical reference cell. The dry-run gate (step 10) and the EPSP_PASSIVE peak-Vm soft gate (REQ-15) catch silent failure within minutes |
| Bar-locked window mechanism silently writes the wrong attribute order (e.g., `g` set after `t_on` clears) | Medium | Critical — would degrade IPSP back to event-like behaviour or zero envelope | The `test_bar_locked_ipsp_envelope.py` regression (REQ-13) catches centre-of-mass collapse. The dry-run gate (step 10) replays this assertion at the centre grid cell. If failing, inspect raw `voltage_traces_ipsp_passive.csv` at the failing direction and `print(seg.gaba_tonic.t_on, seg.gaba_tonic.t_off)` after each trial-setup write |
| All 25 grid cells produce 0 Hz or 0.667 Hz FULL-mode tuning curves (no multi-spike regime entered) | Medium | Reduces task value but does not invalidate it — would still produce a published null result and rule out the AMPA-only escape on this substrate | The task description explicitly anticipates this scenario (RQ1 may yield "no"); the regime-boundary contour (REQ-11) becomes the headline negative result. Document in `results_detailed.md` and propose extending gAMPA to 8 nS or revisiting NMDA via S-0057-06 in a follow-up suggestion |
| 9000-trial sweep exceeds 8.75 h wall-clock budget significantly (e.g., > 14 hours) | Medium | Delays task delivery but does not invalidate it | CVODE (`atol = 1e-3`) is mandatory; if still too slow, stride-down voltage CSV resolution from stride-8 to stride-16; if still too slow, reduce trials per direction from 10 to 5 (still gives reasonable PSTH variance estimate); last resort, drop EPSP_PASSIVE / IPSP_PASSIVE for non-headline grid cells (keep only at corners and centre) |
| `nrnivmodl` fails on Windows due to missing toolchain or drifted NEURON installation | Low | Blocking for entire task — without `gaba_tonic.mod` compiled, no simulation can run | Run `code/run_nrnivmodl.cmd` standalone first; verify `code/mod/nrnmech.dll` exists with non-zero size before integrating; if it fails, inspect `nrnivmodl` stderr in detail and fall back to manual invocation of `nrnivmodl.bat`; if still blocked, create an `intervention/missing_neuron_toolchain.md` per the framework intervention mechanism |
| Bit-identical placement seed test fails (`test_placement_seed0_match.py`) due to numpy version drift since t0057 | Low | Blocking — invalidates the bit-identity claim against t0052 / t0053 / t0057 | Lock numpy version in `pyproject.toml` matching t0057; if drift detected, inspect each pair's coordinates side-by-side; fall back to relaxing `POSITION_TOLERANCE` to 1e-6 (still semantically meaningful but document the relaxation in the test) |
| EPSP_PASSIVE peak Vm exceeds threshold at high `gampa_ns` (4 nS) due to passive depolarisation alone reaching -50 mV without HH | Medium | Would trip the soft gate (REQ-15) and halt metric computation | Inspect: passive depolarisation alone with 100 simultaneous AMPA inputs at 4 nS may push soma Vm above -50 mV transiently. If the peak Vm gate trips at `gampa_ns = 4 nS`, raise `AP_THRESHOLD_MV` for the EPSP_PASSIVE check to -40 mV (still well below an active spike, but accommodates passive AMPA summation); document the threshold raise in `compute_metrics.py` and `results_detailed.md` |
| Cross-grid heatmap rendering fails due to NaN values in `metrics.json` (e.g., HWHM undefined when peak Hz = 0) | Low | Cosmetic — heatmaps render with masked cells | Use `matplotlib.pyplot.pcolormesh` with `numpy.ma.masked_invalid` and explicit `cmap.set_bad("lightgray")`; document in legend that masked cells correspond to undefined metrics (e.g., HWHM under full suppression) |
| Disk usage grows unexpectedly (1233 PNGs + ~5 large CSVs per mode = ~1-2 GB) | Low | Storage warning only; Git LFS not configured | Use stride-8 voltage downsampling per t0057 / t0055 pattern; ensure `results/voltage_traces_*.csv` total size stays under 500 MB by inspecting file sizes after the dry-run gate; if too large, reduce stride further or drop voltage CSVs for EPSP_PASSIVE / IPSP_PASSIVE (keep only FULL) |

## Verification Criteria

* **Plan structure**: Run
  `uv run python -m arf.scripts.verificators.verify_plan t0059_bar_locked_gaba_ampa_sweep_t0057`.
  Expected output: 0 errors. (PL-W warnings are acceptable but should be reviewed.)

* **Research-code structure**: Run
  `uv run python -m arf.scripts.verificators.verify_research_code t0059_bar_locked_gaba_ampa_sweep_t0057`.
  Expected output: 0 errors.

* **Library asset**: Run
  `uv run python -m arf.scripts.verificators.verify_assets t0059_bar_locked_gaba_ampa_sweep_t0057`.
  Expected output: 0 errors against `meta/asset_types/library/specification.md` (v2).

* **Task metrics**: Run
  `uv run python -m arf.scripts.verificators.verify_task_metrics t0059_bar_locked_gaba_ampa_sweep_t0057`.
  Expected output: 0 errors; `results/metrics.json` contains 75 variants
  (`gampa_{0.5,1.0,2.0,3.0,4.0}_gaba_{0.1,0.2,0.5,1.0,2.0}_{full,epsp_passive,ipsp_passive}`) with
  the four registered metrics (`direction_selectivity_index`, `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, `tuning_curve_rmse`) populated per FULL variant.

* **Spatial-gating regression**: Run
  `uv run pytest tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/test_spatial_gating.py -v`.
  Expected output: 4 passed, 0 failed. Confirms REQ-2.

* **Quiescent-rest regression**: Run
  `uv run pytest tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/test_quiescent_rest.py -v`.
  Expected output: 1 passed, 0 failed (V_rest = -65 mV +/- 0.5 mV).

* **Placement-seed bit-identity**: Run
  `uv run pytest tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/test_placement_seed0_match.py -v`.
  Expected output: 1 passed; all 100 pairs match
  `tasks/t0057_tonic_gaba_sweep_t0053/results/placement_seed0.json` to `POSITION_TOLERANCE = 1e-9`.
  Confirms REQ-16.

* **Bar-locked IPSP envelope regression**: Run
  `uv run pytest tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/test_bar_locked_ipsp_envelope.py -v`.
  Expected output: 1 passed; centre-of-mass shift between `theta = 0` and `theta = 90` exceeds the
  predicted lower bound. Confirms REQ-13.

* **HH save-and-zero correctness regression**: Run
  `uv run pytest tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/test_hh_save_and_zero.py -v`.
  Expected output: 1 passed; FULL trace at the canonical reference point matches
  `code/test_data/full_reference_trace.npy` to within `atol=1e-6` mV. Confirms REQ-14.

* **EPSP_PASSIVE peak-Vm soft gate**: Inspect `results/results_detailed.md` (orchestrator-managed)
  for the gate's success message, OR re-run `compute_metrics.py` and confirm no `RuntimeError` is
  raised (max EPSP_PASSIVE Vm < `AP_THRESHOLD_MV`). Confirms REQ-15.

* **Trial budget**: Inspect `results/spike_times_full.csv` and confirm 9000 unique
  `(gampa_ns, gaba_base_ns, angle_deg, trial_seed)` rows; inspect `results/tuning_curve_full.csv`
  and confirm 5 x 5 x 12 = 300 rows. Confirms REQ-6.

* **PNG count**: List `results/images/` and confirm at least 1233 PNG files present (25 grid cells x
  (12 + 12 + 12 + 12 + 1) = 1225 per-cell + 6 cross-grid heatmaps + 1 regime-boundary contour + 1
  active-fraction polar). Confirms REQ-9, REQ-10, REQ-11.

* **MOD compilation artifact**: Confirm `code/mod/nrnmech.dll` exists with non-zero size after the
  bootstrap; confirm
  `python -c "from neuron import h; h.nrn_load_dll('code/mod/nrnmech.dll'); print(hasattr(h, 'gaba_tonic'))"`
  prints `True`. Confirms REQ-1, REQ-17.

* **TSTOP_MS standardisation**: Read `code/constants.py` and confirm `TSTOP_MS = 1400.0`. Confirms
  REQ-4.

* **Activation-time CSV not produced**: Confirm `results/activation_times.csv` does NOT exist (it
  was dropped per S-0055-01). Confirms REQ-5.

* **Requirement coverage**: Cross-check each `REQ-*` row in `## Task Requirement Checklist` against
  the produced outputs (75-variant `metrics.json`, 1233 PNGs, library asset, regression tests). Each
  REQ must have at least one observable artefact in the task folder.
