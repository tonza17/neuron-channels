---
spec_version: "2"
task_id: "t0052_minimal_dsgc_scalar_gaba"
date_completed: "2026-04-25"
status: "complete"
---
# Plan: Minimal From-Scratch DSGC with Scalar gabaMOD Inhibition

## Objective

Build a minimal compartmental DSGC model from scratch on the project's calibrated baseline
morphology, where direction-dependent inhibition is implemented as a scalar `gabaMOD(theta)`
multiplier applied to every IPSC, and run a 12-direction by 10-trial moving-bar sweep on local CPU.
The model must use only NEURON built-in mechanisms (`hh`, `pas`, `Exp2Syn`) — no MOD compilation.
The task produces one library asset, `minimal_dsgc_scalar_gaba`, plus per-direction soma V(t),
aggregate EPSP, aggregate IPSP, PSTH, polar tuning curve, and per-synapse activation histograms.
Done means: library asset validates, all 12 direction figures exist, `metrics.json` contains primary
DSI / vector-sum DSI / preferred direction / peak Hz / null Hz, and the IPSP ratio sanity check
(gNULL/gPD between 2.7 and 3.3) passes as a hard gate.

## Task Requirement Checklist

The operative task request from `task_description.md`:

> Build a minimal compartmental DSGC model with the following specification, then report
> per-direction voltage and firing-rate data so the behaviour can be compared against the project's
> target tuning curve and against t0053. Morphology: `dsgc-baseline-morphology-calibrated`. `soma`
> and `axon_initial_segment` get standard NEURON `hh`; all dendritic sections passive (Rm=5999,
> Ra=100, cm=1, V_rest=-65). 100 E + 100 I co-located synapses; uniform random placement on the
> dendritic length with fixed seed 0. Excitatory: `Exp2Syn` (rise 0.5 ms, decay 2.5 ms, e=0 mV, peak
> 0.5 nS), one event per synapse per trial when bar leading edge crosses the synapse position.
> Inhibitory: `Exp2Syn` (rise 1 ms, decay 20 ms, e=-75 mV, peak 2 nS times `gabaMOD(theta)`).
> `gabaMOD(theta) = 0.33 + 0.66 * (1 - cos(theta - theta_ND)) / 2`, theta_PD=0, theta_ND=180.
> Stimulus: 12 directions (0..330 step 30 deg), bar 200 um wide x arena length, speed 1000 um/s,
> 1500 ms per trial, 10 trials per direction, 120 trials total. Outputs per direction: soma V(t)
> mean+/-SD, aggregate EPSP, aggregate IPSP, PSTH (5 ms bins), polar tuning curve (peak Hz, primary
> DSI, vector-sum DSI, preferred direction), per-synapse activation-time histogram. Library asset
> `minimal_dsgc_scalar_gaba` containing cell builder, synapse placer, excitation driver, inhibition
> driver, trial runner, recording helpers. Local CPU only, $0. Verification: library structure
> validates; 12 PNG plots in `results/images/` embedded in `results_detailed.md`; `metrics.json`
> contains DSI, vector-sum DSI, preferred direction, peak Hz, null Hz; gNULL/gPD ~= 3 IPSP sanity
> check.

Each requirement below has a stable ID used by the Step by Step section and the results step.

* `REQ-1` Morphology: load the t0009 calibrated SWC
  (`dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`) and build a
  pure-Python NEURON cell with explicit soma / dendrite / AIS tagging. Evidence: cell-build log
  prints section count and total dendritic length matching the t0009 summary (1,536.25 um).
  Satisfied by Step 4.

* `REQ-2` Channels: `hh` inserted only on `soma` and `axon_initial_segment`; all dendrite sections
  passive with `Rm=5999`, `Ra=100`, `cm=1.0`; `V_rest=-65 mV`; cell silent at rest. Evidence: a 50
  ms quiescent run reaches steady-state -65 mV +/- 0.5 mV. Satisfied by Step 4 + Step 5.

* `REQ-3` Synapse placement: 100 E + 100 I co-located pairs uniformly over total dendritic length,
  fixed seed = 0, no soma/AIS placement. Evidence: location list logged with seed, saved as
  `assets/library/.../code/code-snapshot/locations.json`-equivalent metadata, total count is exactly
  100 pairs. Satisfied by Step 6.

* `REQ-4` Excitatory mechanism: `Exp2Syn` rise=0.5 ms, decay=2.5 ms, e=0 mV, peak g=0.5 nS, one
  event per synapse per trial. Evidence: `Exp2Syn.tau1`, `tau2`, `e` and `NetCon.weight[0]` printed
  in setup log. Satisfied by Step 7.

* `REQ-5` Inhibitory mechanism: `Exp2Syn` rise=1 ms, decay=20 ms, e=-75 mV, peak g=2 nS times
  `gabaMOD(theta)`. Evidence: same as REQ-4. Satisfied by Step 7.

* `REQ-6` Position-gated firing: each synapse fires once per trial when the bar leading edge crosses
  its (x, y) projected onto the bar's normal, no E/I offset. Evidence: per-synapse activation-time
  histogram (Output 6) shows monotonic relationship between synapse coordinate and onset time.
  Satisfied by Step 7 + Step 12.

* `REQ-7` Scalar `gabaMOD(theta) = 0.33 + 0.66 * (1 - cos(theta - 180_deg)) / 2`; PD weight = 0.33 x
  base, ND weight = 0.99 x base. Evidence: per-trial gabaMOD value logged and matches closed-form
  expectation; IPSP ratio sanity check (REQ-15) passes. Satisfied by Step 8.

* `REQ-8` Stimulus: 12 directions (0, 30, ..., 330 deg), bar 200 um x arena length, speed 1000 um/s,
  1500 ms per trial. Evidence: bar geometry constants in `constants.py`; sweep loop logs 12 angles.
  Satisfied by Step 7 + Step 10.

* `REQ-9` Trials: 10 trials per direction (120 total) with deterministic seeds
  `1000 * angle_idx + trial_idx + 1`. Evidence: sweep CSV contains 120 rows in FULL mode. Satisfied
  by Step 10.

* `REQ-10` Three trial modes: FULL (E+I), AMPA_ONLY (zero IPSC weight), GABA_ONLY (zero EPSC
  weight). Evidence: three independent CSV files in `results/`. Satisfied by Step 9 + Step 10.

* `REQ-11` Per-direction soma V(t) mean +/- SD across 10 trials, 12 PNGs, embedded in
  `results_detailed.md`. Satisfied by Step 11.

* `REQ-12` Per-direction aggregate EPSP (AMPA_ONLY) and aggregate IPSP (GABA_ONLY) mean +/- SD, 12
  PNGs each. Satisfied by Step 11.

* `REQ-13` Per-direction firing-rate PSTH (5 ms bins) mean across 10 trials, 12 PNGs. Satisfied by
  Step 11.

* `REQ-14` Polar tuning curve: peak firing rate (Hz) vs direction, primary DSI, vector-sum DSI,
  preferred direction. Satisfied by Step 11 (polar plot via `tuning_curve_viz`) + Step 12 (metrics).

* `REQ-15` Per-synapse activation-time histogram per direction (sanity check that E synapses on the
  leading edge fire first), 12 PNGs. Satisfied by Step 11.

* `REQ-16` Library asset `minimal_dsgc_scalar_gaba` with: cell builder, synapse placer, AMPA driver,
  GABA driver, trial runner, recording helpers. Satisfied by Step 13.

* `REQ-17` `metrics.json` contains primary DSI, vector-sum DSI, preferred direction, peak Hz, null
  Hz. Satisfied by Step 12.

* `REQ-18` Hard-fail IPSP sanity check: ratio gNULL_IPSP_peak / gPD_IPSP_peak in [2.7, 3.3]
  (theoretical 1/0.33 ~= 3.03). Encoded as a derived metric and a hard assertion in the analysis
  script. Satisfied by Step 12.

* `REQ-19` All compute is local CPU; total cost $0. Satisfied by Step 14 (cost log).

* `REQ-20` Random seed for placement is fixed at 0 and reported in `results_detailed.md`. Satisfied
  by Step 6 + reporting orchestrator step.

## Approach

The model is a clean-room rebuild: no Poleg-Polsky / t0022 HOC carryover, no `nrnivmodl` step, no
custom MOD files. NEURON is bootstrapped on Windows via the same sentinel-guarded `os.execv` re-exec
pattern used in t0046. The cell is built in pure Python by parsing the t0009 calibrated SWC,
creating one `h.Section` per non-soma compartment, collapsing the 19 soma rows into a single `soma`
section, attaching a synthetic 30 um x 1 um `axon_initial_segment` to the soma origin (the SWC has
no axon), and inserting `hh` only on `soma + axon_initial_segment` and `pas` (with `g_pas = 1/Rm`,
`e_pas = V_rest`) on every dendrite.

100 dendritic locations are sampled uniformly by total dendritic length using
`numpy.random.default_rng(0)` so the placement is reproducible. Each location hosts one co-located E
\+ I pair: an `h.Exp2Syn` for AMPA (`tau1=0.5`, `tau2=2.5`, `e=0`) and one for GABA (`tau1=1`,
`tau2=20`, `e=-75`). Each synapse is driven by its own `h.NetStim(number=1, noise=0)` and an
`h.NetCon` whose `weight[0]` carries the unit conductance in microsiemens. Per-trial,
`NetStim.start` is set to the bar-leading-edge crossing time
`t_bar = (x*cos(theta) + y*sin(theta)) / v_um_per_ms + base_offset_ms`, which is the position-gated
event scheduler from t0022. The scalar `gabaMOD(theta)` is computed once per trial and assigned
uniformly to every `gaba_netcon.weight[0]` after scheduling.

Three trial modes are implemented behind a `TrialMode` enum: `FULL`, `AMPA_ONLY` (zeroes every GABA
NetCon weight), `GABA_ONLY` (zeroes every AMPA NetCon weight). Each mode runs the full 12 x 10 sweep
and writes its own CSVs and traces. Recording uses `Vector.record(_ref_v)` for soma voltage and an
`h.NetCon(soma._ref_v, None)` with `threshold = AP_THRESHOLD_MV` for spike detection (the t0046
pattern). Per-synapse activation times are produced as a derived list from the per-trial
`NetStim.start` values (no extra recording needed because each synapse fires exactly once with
`noise=0`).

Outputs are emitted in two CSV schemas the project already supports:
`(angle_deg, trial_seed, firing_rate_hz)` for the tuning curve and
`(angle_deg, trial_index, spike_time_s)` for the rasters. Plotting reuses
`tuning_curve_viz.plot_polar_tuning_curve`, `plot_cartesian_tuning_curve`, and
`plot_angle_raster_psth` by import. Scalar metrics reuse
`tuning_curve_loss.compute_dsi/peak_hz/null_hz/hwhm_deg` by import; vector-sum DSI is added in a new
~25-line `metrics_extra.py`.

The per-direction V(t), aggregate EPSP, aggregate IPSP, PSTH, and per-synapse activation histogram
plots use new lightweight matplotlib code in `code/render_figures.py` because `tuning_curve_viz`
does not cover those panels.

**Alternatives considered.**
* Use NEURON's built-in `h.Import3d_SWC_read` for the morphology. Rejected: requires sourcing
  `import3d.hoc`, gives less control over soma/AIS tagging, and would force HOC into an otherwise
  pure-Python build.
* Implement direction-dependent GABA via a HOC global `gabaMOD` (the t0020 pattern). Rejected: the
  project has no other HOC dependency in t0052; multiplying the scalar directly into each
  `NetCon.weight[0]` is simpler, equivalent, and keeps the cell library Python-only.
* Use a single monolithic 600-line script (the t0022 pattern). Rejected: the spec asks for six
  distinct output products. The t0046 multi-module layout (one renderer per output) gives cleaner
  traceability and matches per-renderer logs.
* Replace the placement seed with a per-trial seed. Rejected: the spec pins seed=0 for placement so
  results never depend on trial count.

**Task types.** `task.json` lists `build-model` and `experiment-run`, and both apply. `build-model`
drives the library-asset, hyperparameter logging, and reproducibility-seed guidelines used in the
plan. `experiment-run` drives the multi-mode sweep, per-direction breakdowns in `metrics.json`,
deterministic seeds, the explicit-variant metrics format (FULL / AMPA_ONLY / GABA_ONLY), the chart
requirements, and the validation-gate pattern (small-scale dry run before the full 120-trial sweep).

**Registered metrics applicable to this task** (from `aggregate_metrics`):
* `direction_selectivity_index` — applicable; written for FULL mode (and informationally for
  AMPA_ONLY).
* `tuning_curve_hwhm_deg` — applicable; written for FULL mode as an early-warning signal that the
  tuning curve is not a hard step.
* `tuning_curve_reliability` — applicable; computed via `tuning_curve_loss.compute_reliability`
  using cross-trial Pearson on the FULL CSV.
* `tuning_curve_rmse` — applicable only if a target tuning curve from t0004 is used as the
  reference. The plan computes it against `tasks/t0004_generate_target_tuning_curve/` output if the
  `target_tuning_curve.csv` is present; otherwise the metric is omitted with a documented note ("no
  target curve loaded; t0052 is a profiling task, not an optimisation task").

`efficiency_*` metrics are not in the registry. Inference time is not meaningful for a fixed
120-trial NEURON sweep; the plan instead logs total wall-clock and reports it in
`results_detailed.md` rather than `metrics.json`.

## Cost Estimation

* NEURON simulation: local CPU, $0.
* Plotting and analysis: local CPU, $0.
* No API calls (no LLM, no external data fetches).
* No remote machines (`available_services` is empty in `project/budget.json`).

**Total: $0.00.** Project budget is $1.00, current spend is $0.00. This task does not consume any of
the budget. `results/costs.json` will record `{}` (no paid services).

## Step by Step

### Milestone 1 — Bootstrap and SWC Loader

1. **Create `code/__init__.py` and the constants module.** Create
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/__init__.py` (empty) and
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/constants.py` defining: `TSTOP_MS = 1500.0`,
   `DT_MS = 0.025`, `CELSIUS_DEG_C = 36.0`, `V_INIT_MV = -65.0`, `AP_THRESHOLD_MV = -20.0`,
   `BAR_WIDTH_UM = 200.0`, `BAR_VELOCITY_UM_PER_MS = 1.0`,
   `ANGLES_DEG = (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)`,
   `N_TRIALS_PER_ANGLE = 10`, `N_PAIRS = 100`, `PLACEMENT_SEED = 0`, `RM_OHM_CM2 = 5999.0`,
   `RA_OHM_CM = 100.0`, `CM_UF_PER_CM2 = 1.0`, `AIS_LENGTH_UM = 30.0`, `AIS_DIAMETER_UM = 1.0`,
   `AMPA_TAU1_MS = 0.5`, `AMPA_TAU2_MS = 2.5`, `AMPA_E_MV = 0.0`, `AMPA_PEAK_NS = 0.5`,
   `GABA_TAU1_MS = 1.0`, `GABA_TAU2_MS = 20.0`, `GABA_E_MV = -75.0`, `GABA_BASE_NS = 2.0`,
   `THETA_ND_DEG = 180.0`, `BASE_OFFSET_MS = 100.0`. Create `code/paths.py` with
   `NEURONHOME_DEFAULT`, `MORPHOLOGY_SWC_PATH` (absolute path to the t0009 calibrated SWC),
   `RESULTS_DIR = Path("tasks/t0052_minimal_dsgc_scalar_gaba/results")`,
   `IMAGES_DIR = RESULTS_DIR / "images"`, and CSV-output paths for FULL / AMPA_ONLY / GABA_ONLY
   tuning-curve and spike-time files. Satisfies `REQ-8`.

2. **Copy and adapt `swc_io.py`.** Copy `tasks/t0009_calibrate_dendritic_diameters/code/swc_io.py`
   to `tasks/t0052_minimal_dsgc_scalar_gaba/code/swc_io.py`. Drop the `write_swc_file` function and
   any writer-only helpers; keep `parse_swc_file`, `validate_structure`, `summarize`,
   `build_children_index`, the `SwcCompartment` and `SwcSummary` dataclasses, and the SWC type-code
   constants. Update the file-header docstring to attribute the copy to t0009. Expected output:
   `python -c "from tasks.t0052_minimal_dsgc_scalar_gaba.code.swc_io import parse_swc_file"`
   succeeds. Satisfies `REQ-1`.

3. **Copy `neuron_bootstrap.py`.** Copy
   `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/neuron_bootstrap.py` to
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/neuron_bootstrap.py`, rename the sentinel env var to
   `_T0052_NEURONHOME_BOOTSTRAPPED`, and import `NEURONHOME_DEFAULT` from t0052's own `paths.py`.
   Expected output:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0052_minimal_dsgc_scalar_gaba -- uv run python -c "from tasks.t0052_minimal_dsgc_scalar_gaba.code.neuron_bootstrap import ensure_neuron_importable; ensure_neuron_importable(); from neuron import h; print(h)"`
   prints a non-error `<HocTopLevelInterpreter>`. Satisfies `REQ-1` (runtime prerequisite).

### Milestone 2 — Cell Builder and Quiescent-Rest Validation Gate

4. **[CRITICAL] Build `code/cell.py`.** Implement
   `build_dsgc_from_swc(*, swc_path: Path) -> CellHandles` where `CellHandles` is a
   `@dataclass(frozen=True, slots=True)` carrying `soma`, `axon_initial_segment`,
   `dendrites: list[Section]`, and a parallel
   `dendrite_xyz_um: list[tuple[float, float, float, float]]` (compartment midpoints + length used
   for placement). The function: (a) parses the SWC via `swc_io.parse_swc_file`, (b) collapses the
   19 soma rows into a single `h.Section(name="soma")` with mean radius and total length, (c)
   creates one `h.Section(name=f"dend[{i}]")` per non-soma compartment, sets `pt3dadd` for each, and
   `connect`s parents using the SWC parent index, (d) creates a synthetic
   `h.Section(name="axon_initial_segment")` with `L=AIS_LENGTH_UM`, `diam=AIS_DIAMETER_UM` connected
   to `soma(1)`, (e) inserts `hh` on `soma` and `axon_initial_segment` only, (f) inserts `pas` on
   every dendrite with `g_pas = 1.0 / RM_OHM_CM2`, `e_pas = V_INIT_MV`, sets `Ra = RA_OHM_CM`,
   `cm = CM_UF_PER_CM2` on every section. Print the section count and total dendritic length on
   completion. Expected output: `dendrites` has > 6,000 sections; total dendritic length is
   `1536.25 +/- 1` um. Satisfies `REQ-1`, `REQ-2`.

5. **[VALIDATION GATE] Quiescent-rest dry run, `code/test_quiescent_rest.py`.** With no synapses,
   run `h.finitialize(V_INIT_MV); h.continuerun(50.0)` and read soma voltage. **Baseline**: V_rest =
   -65 mV (passive). **Failure condition**: if final soma voltage is outside `-65 +/- 0.5 mV`, STOP,
   print the soma voltage trace, and debug the `pas` / `e_pas` / `Ra` / `cm` values before
   proceeding. **Inspection**: print soma voltage at t = 0, 25, 50 ms; print conductance summary for
   soma and one dendrite section. Satisfies `REQ-2`. Idempotent: re-runnable.

### Milestone 3 — Synapse Placement and Drivers

6. **Build `code/placement.py`.** Implement
   `sample_dendritic_locations(*, cell: CellHandles, n_pairs: int, seed: int) -> list[Location]`,
   where `Location` is a `@dataclass(frozen=True, slots=True)` with
   `(section_index: int, section_x: float, x_um: float, y_um: float)`. Use
   `numpy.random.default_rng(seed)` and length-weighted sampling: build a cumulative-length array
   over `cell.dendrites`, sample 100 uniform draws in `[0, total_length]`, map each draw back to
   `(section_index, section_x_in_[0,1])`, and resolve `(x_um, y_um)` via `pt3dadd` interpolation.
   Save the resulting list as JSON to `results/placement_seed0.json` for traceability. Expected
   output: 100 entries; total uniqueness on `(section_index, section_x)` (allow ties); JSON written.
   Satisfies `REQ-3`, `REQ-20`.

7. **Build `code/synapses.py`** by adapting t0022's `EiPair` machinery. Copy lines 104-307 of
   `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py` (the `EiPair` dataclass,
   `_section_midpoint`, `_compute_onset_times_ms`, `_angular_delta_deg`, `build_ei_pairs`,
   `schedule_ei_onsets`) into `code/synapses.py`. Then trim: (a) `NetStim.number = 1`, no
   `interval`; (b) drop the per-pair preferred/null-half-plane GABA branching — every pair uses
   the same `gaba_netcon.weight[0]`; (c) drop the `EI_OFFSET_*` co-arrival logic — E and I fire at
   the same `t_bar`; (d)
   `build_ei_pairs(*, h, locations: list[Location], sections: list[Section]) -> list[EiPair]`
   constructs per-pair Exp2Syn, NetStim, NetCon from the pre-sampled `Location` list, no
   auto-iteration over section midpoints; (e)
   `schedule_ei_onsets(*, pairs, angle_deg, velocity_um_per_ms, gaba_mod_theta) -> None` sets
   `NetStim.start = max(t_bar, 0.0) + BASE_OFFSET_MS` per synapse, sets
   `ampa_netcon.weight[0] = AMPA_PEAK_NS * 1e-3` and
   `gaba_netcon.weight[0] = GABA_BASE_NS * gaba_mod_theta * 1e-3`. Satisfies `REQ-4`, `REQ-5`,
   `REQ-6`.

8. **Add the `gabaMOD(theta)` helper.** In `code/synapses.py` add
   `gaba_mod(*, theta_deg: float, theta_nd_deg: float = THETA_ND_DEG) -> float` returning
   `0.33 + 0.66 * (1.0 - cos(radians(theta_deg - theta_nd_deg))) / 2.0`. Add `test_gaba_mod.py`
   asserting `gaba_mod(theta_deg=0) == 0.33 +/- 1e-9` and
   `gaba_mod(theta_deg=180) == 0.99 +/- 1e-9`. Satisfies `REQ-7`.

### Milestone 4 — Trial Runner and Sweep

9. **Build `code/trial.py`** by adapting t0046's recording skeleton. Copy lines 81-188 of
   `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_simplerun.py` into `code/trial.py`.
   Replace `h.simplerun(exptype, dir)` with explicit
   `h.finitialize(V_INIT_MV); h.continuerun(TSTOP_MS)`. Drop NMDA / BIP / `b2gnmda` logic. Define
   `class TrialMode(StrEnum)` with members `FULL`, `AMPA_ONLY`, `GABA_ONLY`. Define
   `@dataclass(frozen=True, slots=True) class TrialResult` with fields
   `mode: TrialMode, angle_deg: float, trial_seed: int, t_ms: np.ndarray, v_soma_mv: np.ndarray, spike_times_ms: list[float], synapse_onset_times_ms: list[float], firing_rate_hz: float`.
   Implement
   `run_one_trial(*, h, cell: CellHandles, pairs: list[EiPair], mode: TrialMode, angle_deg: float, trial_seed: int) -> TrialResult`.
   Inside: compute `gaba_mod_theta = gaba_mod(theta_deg=angle_deg)`; call `schedule_ei_onsets(...)`;
   if mode is `AMPA_ONLY` set every `pair.gaba_netcon.weight[0] = 0.0`; if mode is `GABA_ONLY` set
   every `pair.ampa_netcon.weight[0] = 0.0`; record `_ref_v` at `soma(0.5)` and `_ref_t`; wire an
   `h.NetCon(soma(0.5)._ref_v, None, sec=soma)` with `netcon.threshold = AP_THRESHOLD_MV` and
   `netcon.record(spike_vec)`. Convert vectors with `np.array(list(vec), dtype=np.float64)`. Compute
   `firing_rate_hz = len(spike_times_ms) / (TSTOP_MS / 1000.0)`. Satisfies `REQ-10`, plus the
   recording subset of `REQ-11..15`.

10. **[CRITICAL][VALIDATION GATE] Build `code/run_tuning_curve.py`** by adapting the t0022 sweep
    harness. Copy lines 466-530 of
    `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py` into
    `code/run_tuning_curve.py`. Adapt to: (a) accept a `mode: TrialMode` argument and write one CSV
    per mode, (b) emit `(angle_deg, trial_seed, firing_rate_hz)` for the tuning curve and
    `(angle_deg, trial_index, spike_time_s)` for spike times, (c) loop angles in the order from
    `ANGLES_DEG`, trials 0..9, with seed `1000 * angle_idx + trial_idx + 1`, (d) emit
    `(angle_deg, trial_seed, sample_idx, voltage_mv)` long-form CSVs for soma V, AMPA-only V,
    GABA-only V (used by Step 11 plots), (e) emit `(angle_deg, synapse_index, onset_time_ms)`
    long-form CSV for the activation histograms.

    **Validation gate.** Before launching the full 12 x 10 x 3 = 360-trial sweep, run a 1-direction
    x 2-trial dry run for each mode (6 trials total, ~10 s wall-clock). **Trivial baseline**:
    AMPA-only at the preferred direction (theta=0) must produce a non-zero firing rate (lower bound
    ~1 Hz; one event per E synapse depolarizes the soma enough). Full mode at the preferred
    direction must produce >= the AMPA_ONLY rate **minus 20%** (because gabaMOD(0)=0.33 is small but
    non-zero). Full mode at the null direction (theta=180) should produce <= the AMPA_ONLY
    null-direction rate. **Failure condition**: if AMPA_ONLY at theta=0 produces 0 spikes, STOP and
    read 5 individual trial trace samples from the CSV; verify `pair.ampa_netcon.weight[0]` was
    non-zero at scheduling time, verify `NetStim.start` was non-NaN, verify the soma voltage trace
    shows EPSP onsets. Do not run the full 360-trial sweep until the dry-run gate passes. Then run
    the full sweep with a `tqdm` progress bar.

    Expected outputs after the full sweep: `results/tuning_curve_full.csv` (120 rows),
    `results/tuning_curve_ampa_only.csv` (120 rows), `results/tuning_curve_gaba_only.csv` (120
    rows), `results/spike_times_full.csv` (variable rows), `results/voltage_traces_full.csv`
    (long-form, ~6e5 rows at dt=0.025 ms), `results/voltage_traces_ampa_only.csv`,
    `results/voltage_traces_gaba_only.csv`, `results/activation_times.csv` (1,200 rows: 12 angles x
    100 synapses). Satisfies `REQ-8..REQ-13`.

### Milestone 5 — Figures and Metrics

11. **Build `code/render_figures.py`.** Implement six figure functions, each writing to
    `results/images/`:
    * `render_soma_voltage_per_direction(*, traces_csv, out_dir)` — for each of 12 angles, mean
      +/- SD soma V(t) across 10 FULL trials, one PNG per direction (`v_soma_dir_<deg>.png`).
    * `render_aggregate_epsp(*, traces_csv, out_dir)` — same for AMPA_ONLY voltage traces
      (`epsp_dir_<deg>.png`).
    * `render_aggregate_ipsp(*, traces_csv, out_dir)` — same for GABA_ONLY voltage traces
      (`ipsp_dir_<deg>.png`).
    * `render_psth(*, spike_times_csv, out_dir)` — 5-ms-bin firing-rate histogram per direction,
      mean across 10 trials (`psth_dir_<deg>.png`).
    * `render_activation_histogram(*, activation_csv, out_dir)` — per-direction histogram of
      synapse onset times (`activation_dir_<deg>.png`).
    * Polar tuning curve and Cartesian tuning curve via library imports
      `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_polar_tuning_curve, plot_cartesian_tuning_curve, plot_angle_raster_psth`,
      writing `polar_tuning_curve.png`, `cartesian_tuning_curve.png`, and
      `raster_psth_dir_<deg>.png`. Satisfies `REQ-11..REQ-15`.

12. **Build `code/compute_metrics.py`.** Import
    `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, compute_reliability, load_tuning_curve`.
    Add a thin `code/metrics_extra.py` (~25 lines) implementing
    `compute_vector_sum_dsi(*, curve) -> float` as
    `abs(sum(rate * exp(1j * radians(angle)))) / sum(rate)` and
    `compute_preferred_direction_deg(*, curve) -> float` as the angle of the same complex sum.
    Compute the AMPA_ONLY and GABA_ONLY peak somatic depolarisation per direction (mean across
    trials of `max(v_soma_mv) - V_INIT_MV`); the `IPSP_PEAK_NS` ratio is then
    `mean_peak_dep_gaba_only(theta=180) / mean_peak_dep_gaba_only(theta=0)`. **Hard-fail
    assertion**: `2.7 <= ipsp_ratio_null_over_pref <= 3.3`. If the assertion fails, write a clear
    error message including the two means and the ratio, and exit non-zero before any metrics are
    written — so the orchestrator does not silently advance. Write `results/metrics.json` in
    **explicit multi-variant format** with three variants:

    ```json
    {
      "variants": {
        "full": {
          "metrics": {
            "direction_selectivity_index": <float>,
            "tuning_curve_hwhm_deg": <float>,
            "tuning_curve_reliability": <float>
          }
        },
        "ampa_only": {
          "metrics": {
            "direction_selectivity_index": <float>,
            "tuning_curve_reliability": <float>
          }
        },
        "gaba_only": {
          "metrics": {}
        }
      }
    }
    ```

    Also write `results/derived_quantities.json` with the non-registered keys: peak Hz, null Hz,
    vector-sum DSI, preferred direction (deg), ipsp_ratio_null_over_pref,
    aggregate_epsp_peak_per_direction, aggregate_ipsp_peak_per_direction. The `tuning_curve_rmse`
    registered metric is computed and added to `full.metrics` if and only if
    `tasks/t0004_generate_target_tuning_curve/results/target_tuning_curve.csv` exists; otherwise it
    is omitted with a documented note in `derived_quantities.json`. Satisfies `REQ-14`, `REQ-17`,
    `REQ-18`.

### Milestone 6 — Library Asset

13. **Create the `minimal_dsgc_scalar_gaba` library asset.** Create
    `tasks/t0052_minimal_dsgc_scalar_gaba/assets/library/minimal_dsgc_scalar_gaba/details.json` with
    `spec_version="2"`, `library_id="minimal_dsgc_scalar_gaba"`,
    `name="Minimal DSGC Scalar gabaMOD"`, `version="0.1.0"`, `short_description` (10+ words),
    `description_path="description.md"`,
    `module_paths=["code/constants.py", "code/paths.py", "code/swc_io.py", "code/neuron_bootstrap.py", "code/cell.py", "code/placement.py", "code/synapses.py", "code/trial.py", "code/run_tuning_curve.py", "code/render_figures.py", "code/compute_metrics.py", "code/metrics_extra.py"]`,
    `entry_points` listing `build_dsgc_from_swc`, `sample_dendritic_locations`, `build_ei_pairs`,
    `schedule_ei_onsets`, `gaba_mod`, `run_one_trial`, `TrialMode`, `compute_vector_sum_dsi`,
    `compute_preferred_direction_deg`, `dependencies=["neuron", "numpy", "matplotlib", "tqdm"]`,
    `test_paths=["code/test_quiescent_rest.py", "code/test_gaba_mod.py"]`,
    `categories=["compartmental-modeling", "direction-selectivity", "synaptic-integration"]`,
    `created_by_task="t0052_minimal_dsgc_scalar_gaba"`, `date_created="2026-04-25"`. Create
    `assets/library/minimal_dsgc_scalar_gaba/description.md` with YAML frontmatter and the eight
    mandatory sections: Metadata, Overview, API Reference, Usage Examples, Dependencies, Testing,
    Main Ideas, Summary (each meeting its minimum word count from
    `meta/asset_types/library/specification.md`). Run
    `uv run python -u -m meta.asset_types.library.verificator tasks/t0052_minimal_dsgc_scalar_gaba/assets/library/minimal_dsgc_scalar_gaba`
    (or the project's library verificator) and confirm zero errors. Satisfies `REQ-16`.

14. **Confirm $0 cost.** Verify no remote machines were created and no paid API calls were made
    during implementation. (The orchestrator's standard cost step writes the cost JSON itself; this
    plan item only flags the implementation-side requirement that nothing paid is invoked.)
    Satisfies `REQ-19`.

## Remote Machines

None required. Local CPU only. The model has roughly 6,700 dendritic compartments, 200 synapses, and
a 1.5-second simulation window at `dt = 0.025 ms`; one trial completes in ~5-15 seconds on a modern
CPU. Total: 360 trials x ~10 s = ~1 hour wall-clock for the full sweep. No GPU, no remote
provisioning, no `available_services` consumed.

## Assets Needed

* `dsgc-baseline-morphology-calibrated` from `t0009_calibrate_dendritic_diameters`. Read directly
  from
  `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`.
* Library `tuning_curve_viz` from `t0011_response_visualization_library`. Imported as
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import ...`.
* Library `tuning_curve_loss` from `t0012_tuning_curve_scoring_loss_library`. Imported as
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import ...`.
* NEURON 8.2.7 install at `C:\Users\md1avn\nrn-8.2.7` (toolchain established in t0007; imported via
  `code/neuron_bootstrap.py`).
* Optional: `tasks/t0004_generate_target_tuning_curve/results/target_tuning_curve.csv` for
  `tuning_curve_rmse` computation; if absent the metric is omitted with a note.

## Expected Assets

This task produces exactly one library asset, matching `task.json`
`expected_assets = {"library": 1}`:

* `library/minimal_dsgc_scalar_gaba` — the cell builder, SWC loader, synapse placer, AMPA and GABA
  position-gated event drivers, scalar-gabaMOD scaling helper, three-mode trial runner (FULL /
  AMPA_ONLY / GABA_ONLY), 12-direction sweep harness, and renderer suite that together implement the
  minimal scalar-gabaMOD DSGC. Code lives under `tasks/t0052_minimal_dsgc_scalar_gaba/code/`; the
  asset folder contains only `details.json` and `description.md`.

No other asset types (paper, dataset, model, predictions, answer) are produced.

## Time Estimation

* Research (already done): ~3 hours total for `research_code.md`. No remaining research time.
* Milestone 1 (bootstrap, constants, SWC loader): ~2 hours.
* Milestone 2 (cell builder, quiescent-rest gate): ~3 hours including debug.
* Milestone 3 (placement, synapses, gabaMOD helper): ~2 hours.
* Milestone 4 (trial runner, sweep, validation gate, full 360-trial run): ~3 hours wall-clock
  (including the ~1 hour of NEURON simulation).
* Milestone 5 (renderers, metrics, IPSP-ratio sanity check): ~2 hours.
* Milestone 6 (library asset metadata + description.md): ~1 hour.
* Verification, fixing verificator errors: ~1 hour.
* **Total implementation wall-clock: ~14 hours**, comfortably under the spec's "~1 week" ceiling.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| SWC -> NEURON section construction is buggy (parents wired wrong, soma not collapsed correctly) | Medium | Critical — cell silent or unstable | Step 5 quiescent-rest gate runs a 50 ms passive sim and checks V_rest = -65 +/- 0.5 mV before any synapse code runs. If the gate fails, log soma voltage, dump first 20 sections' parent indices, and debug `connect` calls; if 3 attempts fail file an intervention. |
| AMPA-only at theta=0 produces 0 spikes (synapses misconfigured or NetStim.start out of window) | Low | Critical — the entire experiment is meaningless | Step 10 dry-run validation gate: 1 angle x 2 trials before full sweep. If 0 spikes, inspect 5 individual `NetStim.start` and `NetCon.weight[0]` values, verify `Exp2Syn.tau1`, `tau2`, `e` were assigned, and verify `BASE_OFFSET_MS` puts events inside `[0, TSTOP_MS]`. Do not advance to full sweep until non-zero. |
| IPSP gNULL/gPD ratio is far from 3 (e.g., < 2.7 or > 3.3) — gabaMOD scalar wired wrong or AMPA leakage in GABA_ONLY mode | Medium | Critical — fails REQ-18 | `compute_metrics.py` raises `AssertionError` with the two means and the ratio printed; this halts the task and forces debugging before `metrics.json` is written. |
| Hard-step DSI=1.0 tuning curve (the t0022 failure mode) | Low | Soft — informative but not a blocker; the gabaMOD scaling is graded so a hard step is structurally unlikely | HWHM is written to `metrics.json` for FULL; if HWHM > 100 deg flag in `derived_quantities.json` for the orchestrator's reporting step to discuss. |
| NEURON Windows bootstrap fails (env var, DLL path, version mismatch) | Low | Blocking | Reuse the t0046 bootstrap pattern (battle-tested across 5 prior tasks); if `ensure_neuron_importable()` raises, file an intervention noting expected vs actual NEURONHOME. |
| Per-direction wall-clock blows up beyond 1 hour (compartment count larger than expected on the calibrated SWC) | Low | Soft | The dry-run gate also profiles 1 trial. If a single trial takes > 60 s, raise `DT_MS` to 0.05 ms (still safe for `hh` integration) and re-profile; if still > 30 s, reduce `N_TRIALS_PER_ANGLE` to 5 and document the deviation in `results_detailed.md`. |
| `tuning_curve_loss` or `tuning_curve_viz` API changes since the research was written | Low | Soft | Imports use the registered library paths; if `compute_dsi` signature changes, the function call will raise immediately, the implementation patches the call, and re-runs Step 12. |

## Verification Criteria

* `tasks/t0052_minimal_dsgc_scalar_gaba/plan/plan.md` exists with all 11 mandatory sections and zero
  verificator errors. Run
  `uv run python -m arf.scripts.verificators.verify_plan t0052_minimal_dsgc_scalar_gaba` and confirm
  `errors: 0`.

* The library asset validates. Run the project's library verificator
  `uv run python -u -m meta.asset_types.library.verificator tasks/t0052_minimal_dsgc_scalar_gaba/assets/library/minimal_dsgc_scalar_gaba`
  and confirm zero errors. Confirms `REQ-16`.

* All three sweep CSVs exist and have 120 rows each. Run
  `python -c "import pandas as pd; [print(p, len(pd.read_csv(p))) for p in ['tasks/t0052_minimal_dsgc_scalar_gaba/results/tuning_curve_full.csv', '.../tuning_curve_ampa_only.csv', '.../tuning_curve_gaba_only.csv']]"`
  and confirm 120 in every file. Confirms `REQ-9`, `REQ-10`.

* All 12 per-direction PNGs exist for soma V, EPSP, IPSP, PSTH, and activation histograms. Run
  `python -c "from pathlib import Path; d = Path('tasks/t0052_minimal_dsgc_scalar_gaba/results/images'); [print(name, sum(1 for _ in d.glob(name + '_dir_*.png'))) for name in ['v_soma','epsp','ipsp','psth', 'activation']]"`
  and confirm 12 per category. Confirms `REQ-11`, `REQ-12`, `REQ-13`, `REQ-15`.

* The IPSP ratio gate passes. Run
  `python -c "import json; d = json.load(open('tasks/t0052_minimal_dsgc_scalar_gaba/results/derived_quantities.json')); r = d['ipsp_ratio_null_over_pref']; assert 2.7 <= r <= 3.3, r; print('ipsp_ratio', r)"`
  and confirm a numeric value in `[2.7, 3.3]` is printed. Confirms `REQ-18`.

* `metrics.json` is in explicit multi-variant format with at least the FULL variant's
  `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`. Run
  `python -c "import json; m = json.load(open('tasks/t0052_minimal_dsgc_scalar_gaba/results/metrics.json')); assert 'variants' in m and 'full' in m['variants']; full = m['variants']['full']['metrics']; for k in ['direction_selectivity_index','tuning_curve_hwhm_deg', 'tuning_curve_reliability']: assert k in full, k; print(full)"`
  and confirm. Confirms `REQ-14`, `REQ-17`.

* `derived_quantities.json` contains peak Hz, null Hz, vector-sum DSI, preferred direction (deg).
  Run
  `python -c "import json; d = json.load(open('tasks/t0052_minimal_dsgc_scalar_gaba/results/derived_quantities.json')); for k in ['peak_hz','null_hz','vector_sum_dsi','preferred_direction_deg']: assert k in d, k"`
  and confirm. Confirms `REQ-14`, `REQ-17`.

* All `REQ-*` items map to at least one Step by Step item. Run
  `python -c "import re; t=open('tasks/t0052_minimal_dsgc_scalar_gaba/plan/plan.md').read(); reqs={m for m in re.findall(r'REQ-\d+', t)}; print(sorted(reqs, key=lambda s:int(s[4:])))"`
  and confirm `REQ-1` through `REQ-20` are all present in the plan body. Confirms requirement
  coverage.

* Cost gate: confirm `results/costs.json` is `{}` (no paid services) and no machine-setup log
  exists. Run
  `python -c "import json; assert json.load(open( 'tasks/t0052_minimal_dsgc_scalar_gaba/results/costs.json')) == {}; print('zero cost confirmed')"`.
  Confirms `REQ-19`.
