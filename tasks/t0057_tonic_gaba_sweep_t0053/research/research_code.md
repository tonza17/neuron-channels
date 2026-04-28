---
spec_version: "1"
task_id: "t0057_tonic_gaba_sweep_t0053"
research_stage: "code"
tasks_reviewed: 11
tasks_cited: 8
libraries_found: 11
libraries_relevant: 4
date_completed: "2026-04-28"
status: "complete"
---
# Research Code: Tonic GABA + Amplitude Sweep on t0053 Spatial DSGC

## Task Objective

This task replaces t0053's per-event `Exp2Syn` GABA mechanism with a new `gaba_tonic.mod` point
process that delivers a sustained conductance over a configurable `(t_on, t_off)` window per
synapse, then sweeps `GABA_BASE_NS` across `{0.25, 0.5, 1.0, 1.5, 2.0}` nS. Morphology, placement
(seed 0), AMPA path, and 12-direction stimulus protocol are kept bit-identical to t0053; only the
GABA mechanism and the per-synapse `gaba_netcon` weight semantics change. The expected output is one
library asset (`minimal_dsgc_tonic_gaba_sweep`) plus directional metrics (DSI primary, DSI
vector-sum, peak Hz, null Hz, HWHM, RMSE vs t0004) for each of the 5 swept conductance values.

## Library Landscape

The repository exposes 11 library assets across `tasks/*/assets/library/`. The aggregator script
`aggregate_libraries.py` is not present in this fork (no module under `arf.scripts.aggregators` of
that name), so libraries were enumerated by walking `tasks/t*/assets/library/*/details.json`
directly — verified by listing 11 paths. None of the 11 details files declare a `replaces` field
or correction overlay, so the raw filesystem state is the effective state.

* `tuning_curve_loss` (from [t0012],
  `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`) — relevant. Provides
  `TuningCurve`, `load_tuning_curve`, `compute_dsi`, `compute_hwhm_deg`, `compute_peak_hz`,
  `compute_null_hz`, `compute_reliability`. Used by t0053's `compute_metrics.py`; identical usage
  required here.
* `tuning_curve_viz` (from [t0011],
  `tasks.t0011_response_visualization_library.code.tuning_curve_viz`) — relevant. Provides
  `plot_polar_tuning_curve`, `plot_cartesian_tuning_curve`, `plot_angle_raster_psth`,
  `plot_multi_model_overlay`, and the `OKABE_ITO` palette. Used by t0053's `render_figures.py`. The
  `plot_multi_model_overlay` entry point is newly relevant for cross-conductance summary plots.
* `minimal_dsgc_spatial_gaba` (from [t0053]) — created by the parent task; **NOT importable** per
  CLAUDE.md rule 3 (only registered cross-task imports are allowed for non-library code). The 12
  listed `module_paths` (`code/cell.py`, `code/synapses.py`, `code/trial.py`,
  `code/run_tuning_curve.py`, `code/render_figures.py`, `code/compute_metrics.py`, etc.) define the
  swap surface but must be **copied into** `tasks/t0057_*/code/`.
* `minimal_dsgc_mg_block_nmda` (from [t0055]) — relevant as a procedural template only:
  demonstrates the only existing pattern in the repo for compiling a custom `.mod` file
  (`code/mod/`) and registering it via `h.nrn_load_dll` from `neuron_bootstrap.py`.

The remaining libraries are not directly relevant: `modeldb_189347_dsgc` ([t0008]),
`modeldb_189347_dsgc_gabamod` (t0020), `modeldb_189347_dsgc_dendritic` (t0022),
`de_rosenroll_2026_dsgc` (t0024), `modeldb_189347_dsgc_exact` ([t0046]), `minimal_dsgc_scalar_gaba`
([t0052]), `minimal_dsgc_ampa_nmda_scalar_gaba` (t0054). They model different DSGC paradigms
(network-level Poleg-Polsky, NMDA-on-AMPA branches, etc.) that this task explicitly excludes (see
task description "Out of Scope"). [t0052] is referenced indirectly via the bit-identical placement
seed but its library is not imported.

## Key Findings

### The Swap Surface for the GABA Mechanism

The smallest set of files that must change to swap from `Exp2Syn` GABA to `gaba_tonic` is well
defined. In t0053, GABA conductance is expressed in three places:

1. `tasks/t0053_minimal_dsgc_spatial_gaba/code/synapses.py` lines 121-124 construct
   `gaba_syn = h.Exp2Syn(seg)` with `tau1 = 1.0 ms`, `tau2 = 20.0 ms`, `e = -75 mV` [t0053].
2. The same file lines 132-136 build `gaba_netstim` (a `NetStim` with `number=1, noise=0`) and lines
   142-144 build `gaba_netcon = h.NetCon(gaba_netstim, gaba_syn)` with `weight[0]` in microsiemens
   [t0053].
3. `schedule_ei_onsets` at lines 184-229 sets `pair.gaba_netstim.start = onset_ms` and
   `pair.gaba_netcon.weight[0] = GABA_BASE_NS * 1e-3` for "fired" synapses, otherwise pushes `start`
   past `TSTOP_MS` and zeroes the weight [t0053].

The new `gaba_tonic.mod` POINT_PROCESS replaces the `Exp2Syn` instance and the NetStim/NetCon
event-driven plumbing entirely: the conductance is set via direct attribute writes to the mechanism
(`g`, `t_on`, `t_off`, `e`), not via `NetCon` events. `i_fired_mask` from t0053 still controls which
synapses receive `g = GABA_BASE_NS * 1e-3` (uS) vs `g = 0`; the spatial gating function
`i_synapse_fires` (lines 76-91 of [t0053]'s `synapses.py`) is re-used unchanged.

`tasks/t0053_minimal_dsgc_spatial_gaba/code/trial.py` lines 47-64 (`_apply_mode_weights`) toggle
GABA via `pair.gaba_netcon.weight[0] = 0.0`. With `gaba_tonic` there is no NetCon weight; the
equivalent toggle is `pair.gaba_syn.g = 0.0` (or equivalently
`pair.gaba_syn.t_off = pair.gaba_syn.t_on`) for `AMPA_ONLY` mode. `GABA_ONLY` mode keeps `g` at the
gated value and zeros AMPA NetCon weight as before [t0053]. The 14-line `run_one_trial`
defensive-restore block at lines 119-127 of [t0053]'s `trial.py` must also be rewritten in tonic
terms.

### Custom MOD File Compilation Pattern

The only existing repo precedent for shipping a custom `.mod` POINT_PROCESS in the minimal-DSGC
family lives in [t0055]. The pattern is:

* Place the `.mod` source at `tasks/<task>/code/mod/<Mechanism>.mod`.
* Provide a `code/run_nrnivmodl.cmd` Windows batch shim that pushd's into `code/mod/` and calls
  `C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat .` to produce `code/mod/nrnmech.dll` (12 lines total;
  verbatim from [t0055]).
* Add `_T0057_NEURONHOME_BOOTSTRAPPED` sentinel constant and `NRNMECH_DLL`, `RUN_NRNIVMODL_CMD`,
  `MOD_DIR` paths to `paths.py` (mirrors lines 38-41 of [t0055]'s `paths.py`).
* Extend `neuron_bootstrap.py` with `ensure_<mech>_compiled()` (~30 lines, mirror of
  `ensure_nmda_mg_block_compiled` at lines 127-145 of [t0055]'s `neuron_bootstrap.py`). The function
  rebuilds the DLL via `subprocess.run` if missing, then calls `h.nrn_load_dll(str(NRNMECH_DLL))`
  and asserts `hasattr(h, "<MechName>")` [t0055].
* Call `ensure_<mech>_compiled()` AFTER `load_stdrun()` and BEFORE any `h.<MechName>(seg)`
  construction in `setup_sweep_artifacts()`. See lines 128-131 of [t0055]'s `run_tuning_curve.py`
  for the canonical call order.

The actual MOD content for the new `gaba_tonic.mod` should follow the structure of the
`NMDA_MgBlock.mod` body at lines 55-120 of [t0055]:
`NEURON {POINT_PROCESS gaba_tonic; RANGE g, e, t_on, t_off, i; NONSPECIFIC_CURRENT i}`, `PARAMETER`
block with `e = -75 mV` and tunable `g` (uS), `t_on` (ms), `t_off` (ms) defaults, `BREAKPOINT` block
with `i = g_eff * (v - e)` where `g_eff` is `g` if `t_on <= t <= t_off` (with optional 1-2 ms cosine
ramp at the edges per the task description) and 0 otherwise. No `NET_RECEIVE` block is needed
because there are no event drivers; the conductance is set by direct attribute write at trial-setup
time.

The optional 1-2 ms cosine ramp at window edges (preferred per task description) avoids stiff-step
integrator artefacts; this is best implemented inside `BREAKPOINT` as a piecewise function of
`t - t_on` and `t_off - t`, since `cnexp` would not apply (the conductance is not a state variable).
A simple `PROCEDURE g_envelope(t)` returning a scalar in `[0, 1]` is sufficient.

### GABA Conductance Lifetime Is the Root Cause Pinpointed in t0053

[t0053]'s `results_summary.md` lines 11-13 document the 0 Hz FULL-mode tuning curve: 2 nS GABA on
~50% of 100 synapses (~100 nS aggregate per trial) fully suppresses spiking on the t0009-calibrated
morphology. [t0053]'s `results_detailed.md` line 32 ("IPSP voltage ratio (max / min) = 1.24×")
confirms driving-force saturation: a 3× active-synapse-count modulation (active fraction 0.34 vs
0.66) produces only a 1.24× IPSP voltage modulation. Per the task description, the deeper issue is
that `Exp2Syn` GABA decays in `tau2 = 20 ms` after each per-synapse event at the bar-arrival time,
so the conductance envelope is non-zero for only ~100-200 ms per trial out of 1500 ms —
biologically unrealistic and the likely cause of the all-or-nothing amplitude sensitivity.

The tonic mechanism with `(t_on, t_off) = (100 ms, 1400 ms)` solves both issues simultaneously: GABA
is on for the full 1300 ms stimulus window (matching SAC->DSGC envelopes from synaptic-integration
literature) and the conductance amplitude is decoupled from the event-decay-tau interaction, so the
sweep over `GABA_BASE_NS` produces a clean amplitude-vs-suppression curve.

### Spatial Gating Logic Is Preserved Bit-for-Bit

The centripetal-gating predicate `cos(radians(theta_stim - theta_centrifugal_synapse)) < 0` from
`i_synapse_fires` (lines 76-91 of [t0053]'s `synapses.py`) and the per-pair
`theta_centrifugal_rad = atan2(y - y_soma, x - x_soma)` precomputation (lines 146-149) are
mechanism-agnostic — they decide *which* synapses are active per trial, not *how* the active
synapses deliver inhibition. Both must be carried over unchanged, and the existing unit tests in
`code/test_spatial_gating.py` ([t0053], 67 lines) can be copied verbatim. The
`active_fraction_per_direction.csv` artefact (12 rows, written by lines 243-256 of [t0053]'s
`run_tuning_curve.py`) and the `active_fraction_polar.png` figure (lines 256-295 of [t0053]'s
`render_figures.py`) likewise transfer unchanged because the activation rule has not changed.

### Multi-Variant `metrics.json` Schema Is Already Established

[t0053]'s `compute_metrics.py` lines 196-205 emit the explicit multi-variant `metrics.json` format
allowed by `arf/specifications/`: `{"variants": [{"variant_id": "full", "metrics": {...}}, ...]}`.
For t0057 each of the 5 conductance values needs its own variant with the full metric set
(`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`, plus the derived `peak_hz`, `null_hz`, `vector_sum_dsi`,
`preferred_direction_deg`). Following [t0055]'s pattern (which sweeps gNMDA across 4 values), the
`variant_id` should encode both the conductance value and the mode, e.g. `"gaba_0.50_full"`,
`"gaba_0.50_ampa_only"`, `"gaba_0.50_gaba_only"`. The `dimensions` block ({"mode": ...,
"gaba_base_ns": ...}) makes downstream aggregation by the existing `aggregate_metric_results.py`
script straightforward.

### Per-Trial Sweep Loop Pattern Is Already Solved in t0055

[t0055]'s `run_tuning_curve.py` adds a gNMDA outer loop on top of [t0054]'s 12-direction x 10-trial
x 3-mode skeleton: lines 269-298 show `_run_sweep_for_mode` accepting `gnmda_ns` as a parameter that
is threaded into `run_one_trial`. For t0057 the analogous parameter is `gaba_base_ns` (threaded into
`schedule_ei_onsets` to set the per-pair `gaba_syn.g` value). The CSV schema extension is also
pre-solved: [t0055]'s tuning-curve CSV gains a leading `gnmda_ns` column (line 169 of
`run_tuning_curve.py`); t0057 should add a `gaba_base_ns` column in the same way. With 5 conductance
values x 12 angles x 10 trials x 3 modes = 1800 trials, [t0055]'s CSV size scaling guidance applies:
stride-8 voltage downsampling keeps disk usage reasonable.

### IPSP Sustained-Window Regression Test Is the New Headline Validator

The verification criteria in the task description introduce a new gate not present in t0053: at the
highest-active direction (`theta = 210 deg` per [t0053]'s active-fraction polar plot), the GABA-only
IPSP voltage at `t = 1300 ms` must be at least 50% of the IPSP voltage at `t = 200 ms`. This
directly tests that the tonic mechanism keeps the conductance up across the full window. The test
should pivot the existing `voltage_traces_gaba_only.csv` (already produced per [t0053]'s
`run_tuning_curve.py`) to `(angle, sample_idx) -> mean_v_mv` and assert
`abs(v_at_1300 - v_rest) >= 0.5 * abs(v_at_200 - v_rest)` for `theta = 210 deg`. Existing
`_voltage_pivot_per_angle` at lines 72-97 of [t0053]'s `render_figures.py` provides the right pivot
template.

## Reusable Code and Assets

### Imported via Library

* **`tuning_curve_loss`** (registered library from [t0012]). Import path:
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (TuningCurve, load_tuning_curve, compute_dsi, compute_hwhm_deg, compute_null_hz, compute_peak_hz, compute_reliability)`.
  Function signatures: `compute_dsi(*, curve: TuningCurve) -> float`,
  `compute_hwhm_deg(*, curve: TuningCurve) -> float`,
  `compute_peak_hz(*, curve: TuningCurve) -> float`,
  `compute_null_hz(*, curve: TuningCurve) -> float`,
  `compute_reliability(*, curve: TuningCurve) -> float | None`,
  `load_tuning_curve(*, csv_path: Path) -> TuningCurve`. Used unchanged by [t0053]'s
  `compute_metrics.py` lines 25-33; t0057 will use them per-conductance instead of once.

* **`tuning_curve_viz`** (registered library from [t0011]). Import path:
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import (plot_polar_tuning_curve, plot_cartesian_tuning_curve, plot_angle_raster_psth, plot_multi_model_overlay)`.
  Per-conductance polar/Cartesian curves use
  `plot_polar_tuning_curve(curve_csv, out_png, target_csv=...)` and
  `plot_cartesian_tuning_curve(curve_csv, out_png, target_csv=...)`. Cross-conductance overlays use
  `plot_multi_model_overlay(...)` with one curve per `GABA_BASE_NS` value.
  `plot_angle_raster_psth(spike_csv, out_png, angle_deg=...)` for per-direction raster+PSTH panels.

### Copy Into Task

* **Source**: `tasks/t0053_minimal_dsgc_spatial_gaba/code/cell.py` (~226 lines). **What it does**:
  builds the calibrated DSGC from the t0009 SWC, collapses the soma, attaches a synthetic AIS,
  returns a `CellHandles` dataclass with `soma_origin_um`. **Adaptation**: rewrite imports to
  reference `tasks.t0057_tonic_gaba_sweep_t0053.code.constants` and
  `tasks.t0057_tonic_gaba_sweep_t0053.code.swc_io`; no logic changes [t0053].

* **Source**: `tasks/t0053_minimal_dsgc_spatial_gaba/code/swc_io.py` (small parser, also imported by
  `cell.py`). **What it does**: parses calibrated SWC into `SwcCompartment` objects. **Adaptation**:
  rewrite imports only [t0053].

* **Source**: `tasks/t0053_minimal_dsgc_spatial_gaba/code/placement.py` (~88 lines). **What it
  does**: length-weighted random sampling of 100 dendritic locations with seed=0; saves
  `placement_seed0.json`. **Adaptation**: rewrite imports only; bit-identical output guaranteed by
  seed [t0053].

* **Source**: `tasks/t0053_minimal_dsgc_spatial_gaba/code/synapses.py` (~229 lines). **What it
  does**: builds AMPA `Exp2Syn` + GABA `Exp2Syn` pairs and per-trial scheduler. **Adaptation
  (significant)**: replace GABA `Exp2Syn` construction (lines 121-124) with `h.gaba_tonic(seg)` and
  per-instance attribute defaults (`e = -75 mV`, `g = 0`, `t_on = 0`, `t_off = 0`); remove
  `gaba_netstim` and `gaba_netcon` (lines 132-136, 142-144); `schedule_ei_onsets` (lines 184-229)
  replaces `pair.gaba_netstim.start = onset_ms` / `pair.gaba_netcon.weight[0] = GABA_BASE_NS * 1e-3`
  with direct attribute writes `pair.gaba_syn.g = gaba_base_ns * 1e-3`,
  `pair.gaba_syn.t_on = T_ON_MS`, `pair.gaba_syn.t_off = T_OFF_MS` for fired synapses (and `g = 0`
  for silent ones); accept `gaba_base_ns` as a per-trial argument. The `i_synapse_fires` predicate
  (lines 76-91) and `theta_centrifugal_rad` computation (lines 146-149) remain bit-identical
  [t0053].

* **Source**: `tasks/t0053_minimal_dsgc_spatial_gaba/code/trial.py` (~140 lines). **What it does**:
  single-trial NEURON runner. **Adaptation**: rewrite `_apply_mode_weights` (lines 47-64) to switch
  between modes via `pair.gaba_syn.g = 0.0` (AMPA_ONLY) instead of
  `pair.gaba_netcon.weight[0] = 0.0`; same for `GABA_ONLY` (zero AMPA NetCon weight as before).
  Update the post-trial restore block (lines 119-127) similarly. Add `gaba_base_ns: float` parameter
  to `run_one_trial` and add it to `TrialResult` for CSV emission [t0053].

* **Source**: `tasks/t0053_minimal_dsgc_spatial_gaba/code/run_tuning_curve.py` (~459 lines). **What
  it does**: top-level sweep harness writing per-mode tuning-curve, spike-time, voltage,
  activation-time, active-fraction CSVs. **Adaptation (largest)**: add
  `GABA_BASE_NS_VALUES = (0.25, 0.5, 1.0, 1.5, 2.0)` outer loop (mirror of [t0055]'s
  `NMDA_PEAK_NS_VALUES`); thread `gaba_base_ns` into `_run_sweep_for_mode` and `run_one_trial`; add
  `gaba_base_ns` column to every per-mode CSV header (mirror lines 165-178 of [t0055]'s
  `run_tuning_curve.py`); call `ensure_gaba_tonic_compiled()` in `setup_sweep_artifacts()` after
  `load_stdrun()` and before `build_ei_pairs()`. Dry-run validation gate at lines 301-385 needs a
  single conductance pass (e.g., `gaba_base_ns = 1.0`) and an additional check that the IPSP voltage
  envelope at `theta = 210 deg` is sustained across the trial window (the new t0057 regression
  criterion).

* **Source**: `tasks/t0053_minimal_dsgc_spatial_gaba/code/compute_metrics.py` (~298 lines). **What
  it does**: emits multi-variant `metrics.json` and a `derived_quantities.json` with per-direction
  EPSP/IPSP envelopes and per-variant peak/null/vector-sum-DSI/preferred-direction. **Adaptation**:
  pivot all loaders by `gaba_base_ns` first, then by `mode`; emit `5 x 3 = 15` variants in
  `metrics.json`; emit cross-conductance summary arrays (`peak_hz_vs_gaba`, `dsi_primary_vs_gaba`,
  `dsi_vector_sum_vs_gaba`, `null_hz_vs_gaba`, `hwhm_vs_gaba`, `rmse_vs_gaba`) in
  `derived_quantities.json`; keep the soft active-fraction sanity (lines 167-193) as-is since the
  gating rule is unchanged from [t0053].

* **Source**: `tasks/t0053_minimal_dsgc_spatial_gaba/code/render_figures.py` (~324 lines). **What it
  does**: per-direction soma V(t), EPSP, IPSP, PSTH, activation histogram PNGs; Cartesian/polar
  tuning curves; raster+PSTH; active-fraction polar. **Adaptation**: each of the per-direction
  figure families becomes a per-(conductance, direction) family (5 x 12 = 60 PNGs per family, 6
  families). Per the task description the most informative representatives can be embedded in
  `results_detailed.md`. Add a new figure family of 6 cross-conductance summary plots (DSI
  primary/vector-sum, peak Hz, null Hz, HWHM, RMSE all vs `GABA_BASE_NS`) using `matplotlib.pyplot`
  directly (or `plot_multi_model_overlay` from [t0011]'s `tuning_curve_viz`) [t0053].

* **Source**: `tasks/t0053_minimal_dsgc_spatial_gaba/code/metrics_extra.py` (~44 lines). **What it
  does**: `compute_vector_sum_dsi` and `compute_preferred_direction_deg`. **Adaptation**: rewrite
  imports only [t0053].

* **Source**: `tasks/t0053_minimal_dsgc_spatial_gaba/code/test_placement_seed0_match.py` (~74
  lines). **What it does**: bit-identity check vs t0052/t0053 placement_seed0.json. **Adaptation**:
  rebind `T0052_PLACEMENT_JSON` reference to `T0053_PLACEMENT_JSON` (or both) in `paths.py`;
  preserve the 1e-9 floating-point tolerance [t0053].

* **Source**: `tasks/t0053_minimal_dsgc_spatial_gaba/code/test_spatial_gating.py` (~67 lines).
  **What it does**: 4 unit tests for the centripetal-gating predicate, including a 1000-sample
  uniform-random active-fraction-near-half check. **Adaptation**: rewrite imports only [t0053].

* **Source**: `tasks/t0053_minimal_dsgc_spatial_gaba/code/test_quiescent_rest.py` (small, untouched
  here). **What it does**: V_rest = -65 mV +/- 0.5 mV gate. **Adaptation**: rewrite imports only
  [t0053].

* **Source**: `tasks/t0055_nmda_mg_block_dsi_recovery/code/run_nrnivmodl.cmd` (12 lines). **What it
  does**: Windows nrnivmodl shim that produces `code/mod/nrnmech.dll`. **Adaptation**: change MOD
  subdirectory only (still `code/mod/`); the script is otherwise task-agnostic [t0055].

* **Source**: `tasks/t0055_nmda_mg_block_dsi_recovery/code/neuron_bootstrap.py` (~146 lines). **What
  it does**: NEURON-on-Windows bootstrap with MOD compilation hook. **Adaptation**: rename
  `ensure_nmda_mg_block_compiled` to `ensure_gaba_tonic_compiled`; change `NMDA_MgBlock` references
  to `gaba_tonic` (or whatever the MOD's POINT_PROCESS is named); change
  `_T0055_NEURONHOME_BOOTSTRAPPED` sentinel to `_T0057_NEURONHOME_BOOTSTRAPPED`; rebind
  `RUN_NRNIVMODL_CMD` and `NRNMECH_DLL` paths via `paths.py`. Logic is otherwise bit-identical
  [t0055].

* **Net new (no source)**: `tasks/t0057_tonic_gaba_sweep_t0053/code/mod/gaba_tonic.mod` (~50-80
  lines new MOD file). The
  `NEURON{POINT_PROCESS gaba_tonic; RANGE g, e, t_on, t_off, i; NONSPECIFIC_CURRENT i}` skeleton,
  `BREAKPOINT { i = g_eff(t) * (v - e) }` body, and optional cosine-ramp `PROCEDURE` are all
  task-specific. Reference style: `tasks/t0055_nmda_mg_block_dsi_recovery/code/mod/NMDA_MgBlock.mod`
  (121 lines) [t0055].

* **Net new (no source)**: a `test_gaba_tonic_envelope.py` regression test that runs one trial at
  `theta = 210 deg`, `mode = GABA_ONLY`, `gaba_base_ns = 1.0` and asserts
  `abs(v_at_1300_ms - V_INIT_MV) >= 0.5 * abs(v_at_200_ms - V_INIT_MV)`. Pivot template comes from
  lines 72-97 of [t0053]'s `render_figures.py`.

## Lessons Learned

* **Spatial centripetal-gating works at the gating level but the t0053 amplitude was 4-5x too
  high.** [t0053]'s active-fraction polar (0.34-0.66) confirms direction-dependent activation, but
  driving-force saturation collapses the IPSP voltage modulation to 1.24x. The per-event Exp2Syn
  mechanism + 2 nS amplitude was the wrong operating point. This task's sweep is designed to find
  the right operating point.

* **Bit-identical placement seeding is the right cross-task gate.** [t0053]'s
  `test_placement_seed0_match.py` against [t0052]'s placement passed at floating-point precision
  (POSITION_TOLERANCE = 1e-9, all 100 pairs). The same pattern must apply to t0057 vs t0053 — same
  `numpy.random.default_rng(seed=0)` + same morphology + same dendrite ordering yields bit-identical
  placements.

* **AMPA_ONLY 0.667 Hz uniform peak is the structural regression gate.** Both [t0052] and [t0053]
  report `AMPA_ONLY peak Hz = 0.667` across all 12 directions. This is the unchanged-AMPA-path
  invariant; t0057 must reproduce it bit-for-bit (because AMPA mechanism, placement, and morphology
  are unchanged).

* **CVODE makes the sweep tractable.** Per [t0055]'s `enable_cvode` with `atol = 1e-3`, per-trial
  wall-clock drops from ~75 s (fixed-step) to ~3-8 s. With 1800 trials in t0057, CVODE is mandatory;
  the comment block in [t0055]'s `neuron_bootstrap.py` lines 82-91 documents the speedup.

* **Custom MOD compilation is robust on Windows when wrapped in a `.cmd` shim.** [t0055]'s pattern
  (`run_nrnivmodl.cmd` + `subprocess.run` + `h.nrn_load_dll`) compiles and registers the new
  POINT_PROCESS without manual user intervention; this is the only existing pattern in the repo for
  shipping a custom MOD as part of a task's build.

* **The dry-run gate catches integration bugs before the full sweep.** [t0053]'s 1-angle x 2-trial
  gate (lines 301-385 of `run_tuning_curve.py`) ensures AMPA_ONLY produces non-zero spikes, FULL
  spike count <= AMPA_ONLY, and `i_active_fraction` lands in `[0.3, 0.7]` at theta=0 — caught at
  least one bug per [t0053]'s commit history. The t0057 dry-run should add the IPSP-sustained-window
  regression at `theta = 210 deg`.

* **`Exp2Syn` decay tau dominates IPSP envelope and amplitude sensitivity.** The `tau2 = 20 ms` is
  the design root cause of the t0053 amplitude-degeneration: the conductance is effectively
  pulse-like, and any amplitude that does not produce a full near-instantaneous shunt produces
  nothing at all. Replacing the kinetics decouples the amplitude axis from the timing axis, which is
  exactly what this task is trying to test.

## Recommendations for This Task

1. **Bootstrap the MOD compilation pipeline first.** Copy `run_nrnivmodl.cmd` from [t0055] verbatim,
   write the new `gaba_tonic.mod` file, set `paths.py` constants (`NRNMECH_DLL`,
   `RUN_NRNIVMODL_CMD`, `MOD_DIR`), and add `ensure_gaba_tonic_compiled` to `neuron_bootstrap.py`.
   Test locally with a single `h.gaba_tonic(seg)` construction and `print(seg.gaba_tonic.g)` smoke
   check before integrating.

2. **Copy [t0053]'s code/ verbatim, then localize.** Per CLAUDE.md rule 3, copy 12 modules from
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/` to `tasks/t0057_*/code/` and rewrite the
   `tasks.t0053_*` import prefix to `tasks.t0057_*` everywhere. This is purely mechanical and
   preserves bit-identity for `cell.py`, `placement.py`, `swc_io.py`, `metrics_extra.py`, and the
   test files.

3. **Modify `synapses.py` last.** The GABA-mechanism swap is the highest-risk diff. Keep the
   `i_synapse_fires` predicate, `theta_centrifugal_rad` computation, `_onset_time_ms`, and `EiPair`
   dataclass field set unchanged where possible; replace only the GABA branch (Exp2Syn construction
   \+ NetStim/NetCon plumbing). Drop `gaba_netstim` and `gaba_netcon` from `EiPair`; add nothing —
   `gaba_syn` is the only handle needed (attribute writes only).

4. **Use [t0055]'s outer-loop pattern verbatim.** Add
   `GABA_BASE_NS_VALUES = (0.25, 0.5, 1.0, 1.5, 2.0)` to `constants.py`, mirror [t0055]'s line
   285-294 sweep loop in `run_tuning_curve.py`, and add `gaba_base_ns` as a column in every per-mode
   CSV header. The same 1000 * angle_idx + trial_idx + 1 trial seed is fine; uniqueness is preserved
   because seeds are advisory (deterministic noiseless trial).

5. **Emit a 15-variant `metrics.json`.** 5 conductance values x 3 modes = 15 variants following the
   [t0053] explicit multi-variant schema. Use `dimensions = {"mode": ..., "gaba_base_ns": ...}` so
   downstream `aggregate_metric_results.py` picks them up cleanly.

6. **Add cross-conductance summary plots.** 6 net new PNGs (DSI primary, DSI vector-sum, peak Hz,
   null Hz, HWHM, RMSE vs `GABA_BASE_NS`) at the end of `render_figures.py`. Use
   `plot_multi_model_overlay` from [t0011]'s `tuning_curve_viz` for the per-conductance tuning-curve
   overlay if visually useful, otherwise plain `matplotlib.pyplot` is fine for single-curve summary
   plots.

7. **Add the IPSP-sustained-window regression test.** Pivot `voltage_traces_gaba_only.csv` by
   `(gaba_base_ns, angle, sample_idx)`, find the angle with maximum mean IPSP (expected
   `theta = 210 deg` from [t0053]), and assert
   `abs(v_at_1300 - V_INIT_MV) >= 0.5 * abs(v_at_200 - V_INIT_MV)` for each of the 5 sweep
   conductance values. This is the headline t0057 quality gate — without it, the new mechanism
   could silently degrade back to event-like behaviour and we would not detect it.

8. **Preserve the bit-identical AMPA_ONLY peak Hz regression.** Add an assertion to
   `compute_metrics.py` that `peak_hz_ampa_only == 0.6667 Hz` for every conductance value (since
   AMPA path is GABA-mechanism-independent). This is the no-regression sentinel.

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: hosts the `modeldb_189347_dsgc` library whose `SAC2RGCinhib.mod`
  (assets/library/modeldb_189347_dsgc/sources/SAC2RGCinhib.mod) is the only existing
  presynaptic-driven GABA POINT_PROCESS in the repo; useful as a structural reference for the new
  `gaba_tonic.mod` even though the mechanism is different.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response-visualisation library (firing rate vs angle graphs)
* **Status**: completed
* **Relevance**: registered library `tuning_curve_viz` provides the polar/Cartesian tuning curve and
  raster+PSTH plots reused for per-conductance figures, plus `plot_multi_model_overlay` for
  cross-conductance summary panels.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: registered library `tuning_curve_loss` provides `compute_dsi`, `compute_hwhm_deg`,
  `compute_peak_hz`, `compute_null_hz`, `compute_reliability`, and `load_tuning_curve` used
  per-conductance in `compute_metrics.py`.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Reproduce Poleg-Polsky & Diamond 2016 exact
* **Status**: completed
* **Relevance**: hosts a verbatim mirror of ModelDB 189347 MODs including a second copy of
  `SAC2RGCinhib.mod`; not directly imported but the canonical reference for GABA presynaptic-driven
  kinetics in the project.

### [t0052]

* **Task ID**: `t0052_minimal_dsgc_scalar_gaba`
* **Name**: Minimal DSGC with scalar gabaMOD
* **Status**: completed
* **Relevance**: parent of t0053; supplies the bit-identical placement seed-0 reference
  (`placement_seed0.json`) and the `0.667 Hz AMPA_ONLY` regression invariant. Indirect dependency
  via t0053.

### [t0053]

* **Task ID**: `t0053_minimal_dsgc_spatial_gaba`
* **Name**: Minimal DSGC with spatial centripetal-gating GABA
* **Status**: completed
* **Relevance**: direct parent. Almost the entire codebase is copied verbatim from
  `tasks/t0053_*/code/`; only `synapses.py` (GABA branch), `trial.py` (mode toggling),
  `run_tuning_curve.py` (outer conductance loop), `compute_metrics.py` (multi-variant output),
  `render_figures.py` (per-conductance + cross-conductance summary plots), and
  `paths.py`/`constants.py` are touched. `cell.py`, `placement.py`, `swc_io.py`, `metrics_extra.py`,
  and the test files are bit-identical with import-prefix rewrites.

### [t0054]

* **Task ID**: `t0054_minimal_dsgc_ampa_nmda_scalar_gaba`
* **Name**: Minimal DSGC with AMPA+NMDA Exp2Syn and scalar gabaMOD
* **Status**: completed
* **Relevance**: parent of [t0055] and the structural template for the gNMDA outer-loop sweep that
  [t0055] then extended; not a direct ancestor of t0057 but its outer-loop pattern feeds into
  [t0055]'s, which is what t0057 borrows.

### [t0055]

* **Task ID**: `t0055_nmda_mg_block_dsi_recovery`
* **Name**: Mg-Block NMDA DSI recovery (NMDA_MgBlock minimal DSGC)
* **Status**: completed
* **Relevance**: the only existing repo precedent for a custom `.mod` POINT_PROCESS that is built
  and registered as part of a task: `code/mod/NMDA_MgBlock.mod`, `code/run_nrnivmodl.cmd`,
  `ensure_nmda_mg_block_compiled` in `neuron_bootstrap.py`. Direct template for the new
  `gaba_tonic.mod` build pipeline. Also supplies the `gNMDA` outer-loop sweep pattern
  (`NMDA_PEAK_NS_VALUES`, per-trial `gnmda_ns` argument, CSV column extension) that t0057 mirrors
  with `GABA_BASE_NS_VALUES`.
