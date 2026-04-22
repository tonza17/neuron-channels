---
spec_version: "1"
task_id: "t0029_distal_dendrite_length_sweep_dsgc"
research_stage: "code"
tasks_reviewed: 9
tasks_cited: 8
libraries_found: 6
libraries_relevant: 3
date_completed: "2026-04-22"
status: "complete"
---
# Research Code: Distal-Dendrite Length Sweep on the t0022 DSGC Testbed

## Task Objective

Sweep the length (`L`) of distal dendritic compartments on the existing t0022 DSGC channel testbed
(at least 7 multipliers from 0.5x to 2.0x of baseline), run the canonical 12-direction tuning
protocol at each length, compute DSI via the t0012 scorer, and classify the DSI-vs-length curve as
monotonic (favours Dan2018 passive transfer-resistance weighting), saturating (favours Sivyer2013
dendritic-spike branch independence), or non-monotonic. The experiment discriminates between two
mechanisms that both fit the baseline t0022 tuning data. No channel edits, no input rewiring, CPU
only, zero external cost. Outputs are `results/data/sweep_results.csv`,
`results/images/dsi_vs_length.png`, and per-length DSI entries in `results/metrics.json`.

## Library Landscape

Six libraries were discovered via `overview/libraries/README.md` (the asset-library aggregator
script is not present in this worktree, so the overview index served as the authoritative
enumeration). None of them has a correction overlay applied.

* `modeldb_189347_dsgc_dendritic` ([t0022], v0.1.0) — **Highly relevant.** This is the testbed we
  are sweeping. Its driver `run_tuning_curve.py`, `constants.py`, `paths.py`, `neuron_bootstrap.py`,
  `score_envelope.py`, `plot_tuning_curve.py`, and `dsgc_channel_partition.hoc` are all registered
  `module_paths`, so functions like `build_ei_pairs`, `schedule_ei_onsets`,
  `run_one_trial_dendritic`, `EiPair`, and the helpers `_preload_nrnmech_dll`,
  `_source_channel_partition_hoc`, `_silence_baseline_hoc_synapses`,
  `_assert_bip_and_gabamod_baseline`, and `_count_threshold_crossings` are importable via
  `from tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve import ...`.

* `tuning_curve_loss` ([t0012], v0.1.0) — **Highly relevant.** Canonical DSI / peak / null / HWHM
  / reliability / RMSE scorer. Import via
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (compute_dsi, compute_peak_hz, compute_null_hz, load_tuning_curve, score, ScoreReport, METRIC_KEY_DSI)`.
  The library accepts the canonical `(angle_deg, trial_seed, firing_rate_hz)` CSV that t0022 emits,
  so per-sweep-point curves can be scored without format conversion.

* `tuning_curve_viz` ([t0011], v0.1.0) — **Relevant for one chart.** Okabe-Ito palette plus
  `plot_cartesian_tuning_curve`, `plot_polar_tuning_curve`, `plot_multi_model_overlay`, and
  `plot_angle_raster_psth`. For this task the primary deliverable is a single `dsi_vs_length.png`
  chart (a scalar sweep), which is not a tuning-curve plot and is outside `tuning_curve_viz`'s
  current function surface. The library is still useful for optional diagnostic polar overlays (one
  per sweep point) if we want to visually inspect how tuning morphs with distal length.

* `modeldb_189347_dsgc` ([t0008], v0.1.0) — **Indirectly relevant.** Provides `build_dsgc`,
  `apply_params`, `read_synapse_coords`, `SynapseCoords`, and `rotate_synapse_coords_in_place` from
  `build_cell.py`. The t0022 driver already imports these; we do not import directly from t0008
  unless we need additional morphology helpers.

* `modeldb_189347_dsgc_gabamod` ([t0020], v0.1.0) — Not relevant. Sibling port that drives DS via
  the gabaMOD PD/ND scalar swap rather than per-dendrite E-I timing. No reusable morphology
  manipulation code.

* `de_rosenroll_2026_dsgc` (t0024, v0.1.0) — Not relevant. Alternative DSGC with a different cell
  template (`build_dsgc_cell`), AR(2) stochastic release, and its own tuning-curve driver. Outside
  the scope of a t0022-only distal-length sweep.

## Key Findings

### NEURON Windows bootstrap is a solved problem and must be reused verbatim

NEURON on this Windows workstation needs `NEURONHOME` set in the C runtime environment at
interpreter startup, `<NEURONHOME>/lib/python` on `sys.path`, and `os.add_dll_directory` pointing at
`<NEURONHOME>/bin`. The `ensure_neuron_importable` function in
`tasks/t0022_modify_dsgc_channel_testbed/code/neuron_bootstrap.py` (64 lines) re-execs the process
once with `NEURONHOME` set if absent, guarded by a per-task sentinel env-var
(`_T0022_NEURONHOME_BOOTSTRAPPED`) to prevent infinite re-exec loops [t0022]. The same pattern
appears verbatim in `tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py:29-81`
[t0020] and is imported via library in
`tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/trial_runner_t0022.py:29-33` [t0026]. For t0029 we
should use `ensure_neuron_importable` from the t0022 library and rename the sentinel env-var to
`_T0029_NEURONHOME_BOOTSTRAPPED` (or reuse the t0022 one — it is already idempotent).

### The t0022 cell context must be built once per process, not per sweep point

Building the DSGC once (~1.6 s in t0022's preflight; similar in t0026) and reusing the NEURON handle
across many (angle, trial) combinations saves non-trivial wall time. The pattern is established in
`trial_runner_t0022.py:88-101` [t0026]:

```python
def build_cell_context() -> CellContext:
    _preload_nrnmech_dll()
    h = build_dsgc()
    _source_channel_partition_hoc(h=h)
    pairs: list[EiPair] = build_ei_pairs(h=h)
    baseline_coords: list[SynapseCoords] = read_synapse_coords(h=h)
    baseline_gaba_mod: float = float(h.gabaMOD)
    return CellContext(h=h, pairs=pairs, baseline_coords=baseline_coords,
                      baseline_gaba_mod=baseline_gaba_mod)
```

`CellContext` is a mutable `@dataclass(slots=True)` holding `h`, `pairs`, `baseline_coords`, and
`baseline_gaba_mod` [t0026]. For a distal-length sweep we will need to either (a) rebuild the cell
for each length (guaranteed but slow: ~1.6 s x 7 = ~11 s extra), or (b) rescale section length
directly on the live HOC handle via `for sec in h.RGC.dends: sec.L = baseline_L[sec] * multiplier`
(faster but requires a baseline-length snapshot + a restore step at the end). The latter is
analogous to how `vrest_override.set_vrest` in t0026 mutates `seg.eleak_HHst` and `seg.e_pas` on the
live handle without re-building [t0026].

### Distal compartments are defined by Strahler order on the morphology graph, not by NEURON section index

The baseline morphology is the NeuroMorpho.org `141009_Pair1DSGC` CNG SWC (6,736 compartments: 19
soma, 6,717 dendrite, 0 axon, 129 branch points, 131 leaves, ~1.54 mm total dendritic path length
[t0005]). t0009 builds a pure-stdlib Horton-Strahler calculator in
`tasks/t0009_calibrate_dendritic_diameters/code/morphology.py:66-99`: iterative post-order DFS over
`SwcCompartment` rows, `children_by_parent` adjacency index from `swc_io.build_children_index`, soma
nodes get sentinel order 0, leaves get order 1, and internal nodes follow the maximum-child
tie-break rule (if the maximum child order appears `m >= 2` times, the parent is `max + 1`; else it
equals `max`) [t0009].

This Strahler calculator operates on the SWC file, not on the live HOC model. The t0022 testbed
builds its cell from `RGCmodel.hoc` + `dsgc_model.hoc` (a hand-edited Neurolucida export that
predates the NeuroMorpho SWC). The HOC side exposes `h.RGC.ON` as a `SectionList` of 282 ON-dendrite
sections (derived from the HOC's `z3d/y3d` test in `RGCmodel.hoc:11817-11826`). For the t0029 sweep
we have two options:

* Use the HOC-native topology: starting from `h.RGC.soma`, walk the HOC section tree via
  `sec.parentseg()` / `h.SectionRef(sec=sec).child` or equivalent to label sections by topological
  depth (branch order). A section is "distal" if it has no downstream dendrite children **in the HOC
  section tree** (i.e., a leaf of the HOC topology). This avoids dependency on the SWC.
* Port t0009's Strahler to HOC: map each HOC `dend[i]` to its SWC ancestry by matching
  `(x3d, y3d, z3d)` point coordinates, then compute Strahler on the SWC graph, then attach the order
  back to HOC sections. Heavier but gives Strahler-based identification.

The task description says `tip compartments at branch order >= 3`. The cleanest implementation is to
identify "distal" as **HOC leaf dendrites** (sections with no child dendrite sections in the HOC
tree). The t0022 HOC builds its tree with `connect dend[i](0), dend[i-1](1)` and similar, so leaf
dendrites are easy to identify by checking `h.SectionRef(sec=sec).nchild() == 0` after building the
cell [t0008]. If the "branch order >= 3" constraint turns out to be strict, we can use a simple HOC
iterative walk rooted at `soma` to assign depths.

### The sweep driver pattern from t0026 is the right template to copy

`tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/run_vrest_sweep_t0022.py` (166 lines) [t0026] is
the most directly applicable template for t0029. Structure:

1. Parse CLI args (`--limit-vrest`, `--limit-trials`, `--output`).
2. Make output directories.
3. Call `build_cell_context()` ONCE (the expensive NEURON bootstrap).
4. For each sweep value in the outer loop:
   * Apply the sweep-specific override (t0026 calls `set_vrest`; t0029 will rescale distal `sec.L`).
   * Iterate `(angle_deg, trial_idx)` and call `run_one_trial_*(...)`.
   * Write one row per trial to the tidy CSV with `fh.flush()` so crash recovery is possible.
   * Record wall time per sweep value to a JSON log.
5. Drop the sweep override (restore baseline L values on the live handle).

The CSV schema t0026 uses is tidy with columns
`v_rest_mv, trial, direction_deg, spike_count, peak_mv, firing_rate_hz` [t0026]. For t0029 the
equivalent would be `length_multiplier, trial, direction_deg, spike_count, peak_mv, firing_rate_hz`
— identical except for the first column name. Keeping the per-row tidy schema makes the
`compute_vrest_metrics.py` style reducer trivial to adapt (vector-sum DSI + HWHM + peak + null per
sweep value).

### DSI is computed by two different but equivalent conventions in the project

Two DSI formulations exist in the project:

* Peak-minus-null formulation in `tuning_curve_loss/metrics.py:41-47`:
  `(peak - null) / (peak + null)` with null = rate at `(preferred_idx + N/2) % N` [t0012].
* Vector-sum formulation in `t0026/compute_vrest_metrics.py:48-63`:
  `|sum_i r_i exp(i theta_i)| / sum_i r_i` with preferred direction taken from the vector-sum angle
  [t0026].

For t0029 we should follow t0022's own convention: t0022 reports DSI via the t0012 scorer (peak-
minus-null). Using `score()` or `compute_dsi()` on the per-sweep-point curve CSV keeps the DSI
values directly comparable to t0022's baseline DSI = 1.0 and t0026's DSI = 0.6555 at V = -60 mV
[t0022] [t0026]. The t0026 vector-sum DSI is a secondary diagnostic (more robust to noise at low
firing rates) and can be emitted alongside the primary DSI in the results.

### DSI charting patterns: follow t0026's summary plot

For the primary `dsi_vs_length.png` chart, the closest existing pattern is t0026's
`plot_polar_tuning.py:summary` figure: a two-panel Cartesian plot (DSI on the left axis, peak Hz on
the right axis, both vs V_rest) [t0026]. For t0029 the x-axis changes to "distal length multiplier"
(or the actual um length) and the panels become DSI-vs-length plus peak-vs-length. The
`tuning_curve_viz` library does not cover scalar-sweep plots, so this chart must be built directly
with `matplotlib` using the patterns from t0026/plot_polar_tuning.py.

### Guardrails against baseline drift are mandatory

t0022 includes a per-trial assertion via `_assert_bip_and_gabamod_baseline` [t0022] that fires if
`h.gabaMOD` drifted from baseline or any BIP synapse coordinate moved. t0029 must add an analogous
guardrail: after restoring baseline distal L at sweep end, assert each distal section's `sec.L`
matches the baseline snapshot within floating-point tolerance. Without this, a buggy restore could
silently leak state across sweep points.

### The canonical onset-scheduling contract depends on section midpoints, not section length

`_compute_onset_times_ms` in `run_tuning_curve.py:274-306` computes each AMPA/GABA onset from
`pair.x_mid_um` and `pair.y_mid_um`, which are stored once at `build_ei_pairs` time via
`_section_midpoint` averaging `x3d(i)` / `y3d(i)` over the section's 3D points [t0022]. When we
rescale `sec.L`, NEURON internally re-interpolates segments but does NOT rewrite the 3D points
(`x3d`/`y3d`/`z3d`). This means **rescaling `sec.L` alone changes the electrotonic length of the
section but leaves the bar-arrival-time calculation unchanged** — a subtle but important property
that preserves the directional-input structure while isolating the cable-length effect. Explicitly
document this in the sweep driver and assert it with a midpoint-snapshot check.

## Reusable Code and Assets

### t0022 testbed driver — copy into task

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py` (683 lines, but
  only ~350 lines need to be copied; the full-sweep `_main_full_sweep` and the argparse scaffolding
  can be replaced with the length-sweep equivalent).
* **What it does**: Builds per-dendrite AMPA/GABA E-I pairs, schedules bar-direction-dependent
  onsets, runs one trial returning firing rate in Hz, writes canonical CSV.
* **Reuse method**: **copy into task**. Even though t0022 registers this file in its library
  `module_paths`, the helpers we need (`build_ei_pairs`, `schedule_ei_onsets`,
  `run_one_trial_dendritic`, `_preload_nrnmech_dll`, `_source_channel_partition_hoc`,
  `_silence_baseline_hoc_synapses`, `_assert_bip_and_gabamod_baseline`,
  `_count_threshold_crossings`, `EiPair`, `TrialResult`, `_section_midpoint`) are importable. Per
  the CLAUDE.md cross-task rule, library-registered modules CAN be imported; only non-library task
  code must be copied. **Decision**: import `EiPair`, `build_ei_pairs`, `schedule_ei_onsets`,
  `_preload_nrnmech_dll`, `_source_channel_partition_hoc`, `_silence_baseline_hoc_synapses`,
  `_assert_bip_and_gabamod_baseline`, `_count_threshold_crossings` directly from the t0022 library
  (same pattern as `trial_runner_t0022.py:50-59` in t0026), and write a thin local
  `run_one_trial_length` that adds the distal-length override in the same position `set_vrest`
  occupies in t0026 (after `apply_params` / `_silence_baseline_hoc_synapses` /
  `_assert_bip_and_gabamod_baseline`, before `h.finitialize`).
* **Function signatures** (to import via library):
  * `build_ei_pairs(*, h: Any) -> list[EiPair]`
  * `schedule_ei_onsets(*, h: Any, pairs: list[EiPair], angle_deg: float, velocity_um_per_ms: float, gaba_null_pref_ratio: float, trial_seed: int) -> list[dict[str, float]]`
  * `_preload_nrnmech_dll() -> None`
  * `_source_channel_partition_hoc(*, h: Any) -> None`
  * `_silence_baseline_hoc_synapses(*, h: Any) -> None`
  * `_assert_bip_and_gabamod_baseline(*, h: Any, baseline_coords: list[SynapseCoords], baseline_gaba_mod: float) -> None`
  * `_count_threshold_crossings(*, samples: list[float], threshold_mv: float) -> int`

### t0022 NEURON bootstrap — import via library

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/neuron_bootstrap.py` (64 lines).
* **What it does**: `ensure_neuron_importable()` sets `NEURONHOME`, adds NEURON Python bindings to
  `sys.path`, registers the DLL directory, and re-execs once if `NEURONHOME` is missing.
* **Reuse method**: **import via library**. t0022 registers `code/neuron_bootstrap.py` in its
  library module_paths. Call `ensure_neuron_importable()` at module scope before any `neuron`
  import, exactly as t0026 does in `trial_runner_t0022.py:29-33` [t0026].
* **Function signature**: `ensure_neuron_importable() -> None`.
* **Adaptation needed**: Either (a) reuse t0022's sentinel directly (the env-var is idempotent under
  repeated exec) or (b) clone the function into this task with a `_T0029_*` sentinel if we ever
  expect two sweeps to run back-to-back without process restart. Option (a) is simpler.

### t0022 channel-partition HOC overlay — import via library

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/dsgc_channel_partition.hoc` (108 lines).
* **What it does**: After `build_dsgc()`, declares 5 `SectionList` globals (`SOMA_CHANNELS`,
  `DEND_CHANNELS`, `AIS_PROXIMAL`, `AIS_DISTAL`, `THIN_AXON`) and populates them from `RGC.soma` and
  `RGC.dends`. AIS lists are intentionally empty on this morphology (no axon sections).
* **Reuse method**: **import via library**. It is listed in t0022's `module_paths`. Call
  `_source_channel_partition_hoc(h=h)` after `build_dsgc()` to guarantee the testbed matches t0022
  exactly.
* **Adaptation needed**: None. We do not modify channel densities in t0029; only `sec.L` changes.

### t0022 canonical constants — import via library

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/constants.py` (146 lines).
* **What it does**: Holds every magic number the driver needs: `TSTOP_MS=1000.0`, `DT_MS=0.1`,
  `CELSIUS_DEG_C=32.0`, `N_ANGLES=12`, `N_TRIALS=10`, `ANGLE_STEP_DEG=30.0`,
  `AP_THRESHOLD_MV=-10.0`, `V_INIT_MV=-65.0`, `BAR_VELOCITY_UM_PER_MS=1.0`,
  `BAR_BASE_ONSET_MS=200.0`, the E-I onset offsets (`EI_OFFSET_PREFERRED_MS=10.0`,
  `EI_OFFSET_NULL_MS=-10.0`), conductances (`AMPA_CONDUCTANCE_NS=6.0`,
  `GABA_CONDUCTANCE_PREFERRED_NS=3.0`, `GABA_CONDUCTANCE_NULL_NS=12.0`), kinetics, segment locations
  (`AMPA_SEG_LOCATION=0.9`, `GABA_SEG_LOCATION=0.3`), CSV column names, and metric keys.
* **Reuse method**: **import via library**. Listed in t0022's `module_paths`. Do not redefine any of
  these in t0029; import them.

### t0012 tuning-curve scorer — import via library

* **Source**: `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/` (8 files,
  registered library).
* **What it does**: Loads a canonical 12-angle CSV, computes DSI, peak Hz, null Hz, HWHM, split-half
  reliability, and RMSE against the t0004 target. `score` returns a `ScoreReport` dataclass with all
  metrics and envelope pass/fail.
* **Reuse method**: **import via library**.
* **Function signatures**:
  * `compute_dsi(*, curve: TuningCurve) -> float`
  * `compute_peak_hz(*, curve: TuningCurve) -> float`
  * `compute_null_hz(*, curve: TuningCurve) -> float`
  * `compute_hwhm_deg(*, curve: TuningCurve) -> float`
  * `load_tuning_curve(csv_path: Path) -> TuningCurve`
  * `score(*, simulated_curve_csv: Path) -> ScoreReport`
* **Adaptation needed**: For each sweep point we write one per-sweep-point 12-angle tidy CSV in the
  canonical schema and call `load_tuning_curve` followed by `compute_dsi`/`compute_peak_hz`/
  `compute_null_hz`/`compute_hwhm_deg` directly. We do not need the full `score()` because the
  loss-vs-t0004-target is not informative here — the sweep question is about DSI shape, not
  target-fit quality.

### t0011 tuning-curve visualizer — import via library (optional)

* **Source**: `tasks/t0011_response_visualization_library/code/tuning_curve_viz/` (10 files,
  registered library).
* **What it does**: Produces polar, Cartesian, multi-model-overlay, and raster+PSTH PNGs from
  tuning-curve CSVs.
* **Reuse method**: **import via library**.
* **Function signatures**:
  * `plot_polar_tuning_curve(curve_csv: Path, out_png: Path, *, show_trials: bool = True, target_csv: Path | None = None) -> None`
  * `plot_multi_model_overlay(curve_csvs: list[Path], labels: list[str], out_png: Path, ...) -> None`
* **Adaptation needed**: The primary chart (`dsi_vs_length.png`) is not a tuning curve; it is a
  scalar sweep. Write it directly with matplotlib using the t0026 summary-plot pattern (~30-50
  lines). Optionally produce a `plot_multi_model_overlay` diagnostic where "models" are labeled by
  length multiplier to confirm visually that the tuning curves look sensible at each point.

### t0026 length-multiplier override pattern (to clone, not copy) — copy into task

* **Source**: `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/vrest_override.py` (38 lines) and
  `trial_runner_t0022.py:104-160` (run_one_trial_vrest).
* **What it does**: `set_vrest` walks `h.allsec()` and mutates `seg.eleak_HHst` / `seg.e_pas` on the
  live handle. `run_one_trial_vrest` interleaves `set_vrest` between `apply_params` and
  `h.finitialize` so baseline values are re-applied on every trial then immediately overridden.
* **Reuse method**: **copy into task** (NOT registered as a library). Clone the 38-line structure of
  `vrest_override.py` into `code/length_override.py`. New function signature:
  * `snapshot_distal_lengths(*, h: Any, distal_sections: list[Any]) -> dict[int, float]` — record
    baseline `sec.L` keyed by section index; called once at `build_cell_context` time.
  * `set_distal_length_multiplier(*, h: Any, distal_sections: list[Any], baseline_L: dict[int, float], multiplier: float) -> None`
    — sets `sec.L = baseline_L[idx] * multiplier` for every distal section. Called after
    `apply_params` / `_silence_baseline_hoc_synapses` and before `h.finitialize`.
  * `identify_distal_sections(*, h: Any) -> list[Any]` — walks `h.RGC.dends` and returns only
    dendrite sections with no dendrite children in the HOC topology (i.e., HOC leaves). Returns
    about 100-150 sections on the 350-compartment bundled morphology (estimate; actual count will be
    logged in the implementation's preflight).
* **Adaptation needed**: The `set_vrest` pattern mutates `seg`-level RANGE variables; for length we
  must mutate `sec.L` directly (section-level, not segment-level). NEURON re-discretises segments
  automatically when `sec.L` or `sec.nseg` changes. The d_lambda rule is not enforced in the
  t0008/t0022 HOC (they use `nseg=1` globally per `RGCmodel.hoc:11817`), so changing `L` may
  under-resolve segmentation at 2.0x baseline. Post-rescale, either (a) leave `nseg=1` and accept
  the coarser spatial resolution at 2.0x (matches existing t0008/t0022 convention), or (b) re-apply
  d_lambda by setting `sec.nseg = int((sec.L / (0.1 * sec.lambda_f)) * 2) + 1` after the length
  change. Decision deferred to planning, but (a) is the simpler starting point.

### t0026 tidy-CSV sweep driver pattern — copy into task

* **Source**: `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/run_vrest_sweep_t0022.py` (166
  lines).
* **What it does**: Builds cell once, iterates outer sweep values and inner (angle, trial) loops,
  writes one CSV row per trial with `fh.flush()` after every row, emits a per-sweep-value wall-time
  JSON.
* **Reuse method**: **copy into task** (NOT registered as a library).
* **Adaptation needed**: ~20-line delta: rename `V_REST_VALUES_MV` to `LENGTH_MULTIPLIERS`, swap the
  `set_vrest(h, v_rest_mv)` override for
  `set_distal_length_multiplier(h=h, distal_sections=..., baseline_L=..., multiplier=m)`, and change
  the CSV schema to have `length_multiplier` as the first column. Per-trial count should match the
  task description's recommended 12-direction tuning protocol: use `N_TRIALS=10` (matching t0022's
  canonical count) or `N_TRIALS=1` if total runtime pushes past 90 min.

### t0026 per-sweep-value metrics reducer — copy into task

* **Source**: `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/compute_vrest_metrics.py` (265
  lines).
* **What it does**: Reads tidy CSV, groups by sweep value, computes per-group DSI (vector-sum),
  preferred direction, HWHM, peak, null, and mean peak V_soma. Writes a per-sweep-value metrics CSV.
* **Reuse method**: **copy into task**. Rename the sweep axis from V_rest to length_multiplier and
  adjust column names accordingly. Use the t0012 `compute_dsi` scorer for the primary DSI column and
  keep the `_vector_sum_dsi` helper as the secondary diagnostic.

### t0026 summary plot — copy into task

* **Source**: `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/plot_polar_tuning.py` summary
  function (~80 lines of the 263-line file).
* **What it does**: Two-panel Cartesian plot of DSI and peak Hz vs sweep axis.
* **Reuse method**: **copy into task**. Rename x-axis to "distal length multiplier" and x-values to
  the 7 multipliers.

### Baseline DSGC morphology dataset asset (context only)

* **Source**: `dsgc-baseline-morphology` dataset asset produced by [t0005]
  (`tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/`).
* **What it does**: Holds the `141009_Pair1DSGC.CNG.swc` reconstruction (6,736 compartments, 1.54 mm
  total dendritic length) on which t0009 calibrated diameters. This is NOT the HOC morphology that
  t0022 actually uses; t0022 uses the Poleg-Polsky bundled HOC (`RGCmodel.hoc` + `dsgc_model.hoc`
  under the t0008 library asset). The two trees are topologically different.
* **Reuse method**: Read-only reference. For t0029 we sweep on the HOC (t0022) morphology, not the
  NeuroMorpho SWC, because the full t0022 biophysics depends on the HOC cell template.

### t0009 Strahler calculator (optional reference)

* **Source**: `tasks/t0009_calibrate_dendritic_diameters/code/morphology.py:66-99` (Strahler DFS),
  `swc_io.py` (SWC parse + children index).
* **What it does**: Pure-stdlib Horton-Strahler on SWC trees.
* **Reuse method**: **copy into task** IF we decide to run Strahler on the HOC topology. For the
  initial implementation we default to HOC-leaf-dendrite identification (simpler), and only port
  Strahler if the "branch order >= 3" constraint turns out to matter. This is a planning decision,
  not an implementation prerequisite.

## Common Patterns

* **`ensure_neuron_importable()` before any `neuron` import** (t0022, t0026, t0024). Always call at
  module scope before `from neuron import h`.
* **NEURON bootstrap sentinel env-var per task** prevents re-exec loops. Current convention:
  `_T<TASK_ID>_NEURONHOME_BOOTSTRAPPED`.
* **Canonical CSV schema** `(angle_deg, trial_seed, firing_rate_hz)` is enforced across t0004,
  t0008, t0020, t0022, t0024 and accepted by t0012's `load_tuning_curve`. Per-sweep-point curves for
  t0029 should be written in this schema so they can be scored without conversion.
* **Per-trial seed** convention is `1000 * angle_idx + trial_idx + 1` [t0008] [t0022] [t0026]. Keep
  this for t0029 trial seeds; add the length-multiplier index as an outer dimension so seeds remain
  unique across sweep points.
* **Tidy wide CSV** for sweep results: one row per (sweep_value, angle, trial), with `fh.flush()`
  after every row for crash recovery [t0026].
* **Baseline-drift guards**: every trial asserts that `h.gabaMOD` and BIP coords are at their
  baseline values [t0022]. t0029 should add an analogous assertion that every distal section's
  `sec.L` matches `baseline_L[idx] * current_multiplier` to within 1e-9.
* **Keyword-only arguments** throughout the project per CLAUDE.md Python style rules. All helper
  signatures above follow this convention.

## Lessons Learned

* **Build cost matters**: t0026 flagged that NEURON cell build + channel-partition HOC source + E-I
  pair creation takes ~1-2 s, while one trial runs ~0.2-0.5 s. Over a 7-length x 12-angle x 10-trial
  sweep (840 trials), avoiding per-sweep-value rebuilds saves ~10 s and avoids spurious differences
  from stochastic cell-build state. **Takeaway for t0029**: build once, mutate `sec.L` on the live
  handle per sweep point.

* **Forgetting to silence bundled HOC synapses gives a spurious 13-15 Hz baseline firing rate** that
  confounds the E-I driver. t0022 fixed this with `_silence_baseline_hoc_synapses` which zeros
  `h.b2gampa`, `h.b2gnmda`, `h.s2ggaba`, `h.s2gach` and calls `update()` + `placeBIP()` [t0022].
  **Takeaway**: every trial in t0029 must call `_silence_baseline_hoc_synapses`; omitting it is a
  silent, hard-to-detect bug.

* **`apply_params` resets `v_init` and segment leak reversals to their t0008 defaults on every
  call**, which is why t0026's `set_vrest` must run AFTER `apply_params` and BEFORE `h.finitialize`
  [t0026]. The same ordering constraint applies to t0029's length override: `apply_params` does NOT
  touch `sec.L`, so overriding `sec.L` once per sweep point (outside the trial loop) is actually
  sufficient. **Optimisation**: set distal lengths at the top of the outer sweep loop, not inside
  the inner trial loop. Re-assert L before each trial as a cheap sanity check.

* **HOC global vs RANGE variable confusion burned t0020**: setting `h.gabaMOD = X` in Python does
  not retroactively update per-synapse objects unless `placeBIP()` is re-called [t0020]. The same
  class of bug applies to `sec.L`: changing `sec.L` on a live handle implicitly re-discretises the
  section, but only if `sec.nseg` is re-evaluated. Since the t0008 HOC uses `forall {nseg=1}` there
  is only one segment per section and discretisation is trivial. **Takeaway**: verify with a
  preflight that `sec.nseg == 1` for every distal section after our override, and that the d_lambda
  rule is not silently violated at the 2.0x endpoint.

* **Keep `apply_params` in the inner trial loop even with a constant sweep parameter**. t0022 and
  t0026 both do this because `apply_params` also re-seeds the NEURON Random123 streams
  (`h(f"seed2={seed}")`) per trial. If we pull `apply_params` out of the inner loop, trial seeds
  stop rotating and every trial returns identical firing rates. **Takeaway**: keep the t0026
  trial-runner structure; do not "optimise" by hoisting `apply_params`.

* **Results-CSV per-row `fh.flush()` in t0026 enabled successful crash-recovery** when the t0024
  sweep (960 trials, 3.21 h) had intermittent issues. **Takeaway**: follow the same pattern in t0029
  even though the sweep is ~840 trials (well under an hour).

* **t0022 DSI = 1.0 at baseline is unusually high** because the deterministic driver produces zero
  firing at any angle >= 150 deg from the preferred direction [t0022]. This means the sweep's
  "saturation" signature may appear as DSI pinned at 1.0 across a wide plateau of length values,
  which would need extra care in the curve-shape classifier — a plateau at DSI=1.0 is both
  "monotonic" (if approached from below) and "saturating" depending on where the plateau starts.
  **Takeaway**: compute DSI at length = 0.5x first to confirm DSI < 1.0 at the low end, and if not,
  propose a narrower sweep range around the 0.25x-1.0x regime as a follow-up suggestion.

## Recommendations for This Task

### Architecture

1. Follow the t0026 two-file architecture: `code/length_override.py` (~40 lines, clone of
   `vrest_override.py` logic) and `code/trial_runner_length.py` (~160 lines, clone of
   `trial_runner_t0022.py`). Plus a `code/run_length_sweep.py` driver (~160 lines, clone of
   `run_vrest_sweep_t0022.py`) and a `code/compute_length_metrics.py` reducer (~250 lines, clone of
   `compute_vrest_metrics.py`).

2. Import these pieces from the t0022 library (library, not copy): `ensure_neuron_importable`,
   `EiPair`, `build_ei_pairs`, `schedule_ei_onsets`, `_preload_nrnmech_dll`,
   `_source_channel_partition_hoc`, `_silence_baseline_hoc_synapses`,
   `_assert_bip_and_gabamod_baseline`, `_count_threshold_crossings`. Import from t0008 library:
   `build_dsgc`, `apply_params`, `read_synapse_coords`, `SynapseCoords`. Import from t0012 library:
   `compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `load_tuning_curve`,
   `TuningCurve`.

### Distal-section identification

3. Define "distal" as **HOC leaf dendrites**: sections in `h.RGC.dends` with no dendrite children in
   the HOC section tree. This avoids a Strahler port and is implementable in ~15 lines using
   `h.SectionRef(sec=sec).nchild()`. Log the count in the preflight; expect 100-200 distal sections
   on the 350-dend bundled morphology.

4. If the task description's "branch order >= 3" must be enforced strictly, port the t0009 Strahler
   DFS to HOC in a follow-up step. This is a planning-time decision; defer until the leaf-dendrite
   approach is benchmarked.

### Sweep driver

5. Sweep values: use the task description's suggestion `(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)` —
   exactly 7 multipliers. Trial count: N_TRIALS=10 (canonical t0022 count). Total trials: 7 x 12 x
   10 = 840. Estimated wall time at t0026's t0022-model pace (~3.75 s/trial): ~52 min, comfortably
   within the 30-90 min budget.

6. CSV schema: tidy with columns
   `(length_multiplier, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`. Write one row
   per trial, flush after every row.

7. For each sweep point, after the outer sweep CSV row batch is complete, also emit a
   per-sweep-point canonical CSV `(angle_deg, trial_seed, firing_rate_hz)` so the t0012 scorer can
   be called without reshaping.

### Scorer integration

8. For each of 7 sweep points, call `compute_dsi(curve=load_tuning_curve(csv_path=...))` on the
   per-sweep-point curve CSV and write `dsi_length_<m>` entries to `results/metrics.json`. This
   matches t0022's metric key convention.

### Chart

9. `dsi_vs_length.png` is the primary chart. Follow t0026's `summary_<model>_vrest.png` two-panel
   Cartesian pattern: left axis DSI vs multiplier, right axis peak Hz vs multiplier. Use the
   Okabe-Ito palette from `tuning_curve_viz.constants.OKABE_ITO` for colour consistency across the
   project.

10. As a diagnostic, generate 7 per-length polar tuning-curve PNGs via
    `plot_polar_tuning_curve(curve_csv=per_length_csv, out_png=images/polar_L<m>.png)` to visually
    inspect how the curve morphs with length. Optional but recommended.

### Curve-shape classifier

11. Classify the resulting DSI-vs-length curve as:
    * **Monotonic** (favours Dan2018) if DSI is strictly non-decreasing with a significant slope
      (e.g., linear regression slope > 0.05 per unit multiplier, p < 0.05).
    * **Saturating** (favours Sivyer2013) if the DSI-vs-length curve reaches within 5% of its max by
      the 1.0x or 1.25x point and stays flat thereafter.
    * **Non-monotonic** otherwise — flag kinetic tiling (Espinosa 2010) as a possible mechanism in
      the results discussion per the task description's guidance.

12. Watch out for DSI pinned at 1.0 across a wide plateau (expected at baseline length per [t0022]
    results). Compute and report the full tuning-curve peak Hz and null Hz vectors at each sweep
    point so the mechanism interpretation has enough resolution even when DSI saturates at 1.0.

### Guardrails

13. Add a pre-sweep snapshot of baseline distal `sec.L` values and a post-sweep assertion that they
    have been restored to the snapshot (to within 1e-9 relative tolerance). Follow the
    `_assert_bip_and_gabamod_baseline` pattern from t0022.

14. Add a preflight mode (analogous to t0022's `--preflight`): 3 angles x 2 trials x 3 multipliers
    (0.5, 1.0, 2.0), total 18 trials, ~1 min wall time. This validates the override logic and curve
    shape before committing to the full 840-trial sweep.

### Logging

15. Log the number of identified distal sections, the baseline-L distribution (min / median / max /
    total distal length), and per-sweep-point wall time. Emit as JSON under
    `logs/preflight/distal_sections.json` and `data/wall_time_by_length.json`.

## Task Index

### [t0005]

* **Task ID**: `t0005_download_dsgc_morphology`
* **Name**: Download candidate DSGC morphology
* **Status**: completed
* **Relevance**: Produces the `dsgc-baseline-morphology` dataset asset (141009_Pair1DSGC CNG SWC,
  6,736 compartments, 1.54 mm total dendritic length). Background context for the
  morphology-provenance discussion, though t0029 sweeps on the Poleg-Polsky HOC topology (t0008
  library), not directly on this SWC.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 DSGC model (12-angle tuning curve)
* **Status**: completed
* **Relevance**: Registers the `modeldb_189347_dsgc` library and bundles the Poleg-Polsky HOC
  sources (`RGCmodel.hoc`, `dsgc_model.hoc`) + compiled mechanisms that the t0022 testbed inherits.
  Exposes `build_dsgc`, `apply_params`, `read_synapse_coords`, `SynapseCoords` that we import for
  the cell build and baseline-coord snapshot.

### [t0009]

* **Task ID**: `t0009_calibrate_dendritic_diameters`
* **Name**: Calibrate dendritic diameters on DSGC morphology
* **Status**: completed
* **Relevance**: Provides the pure-stdlib Horton-Strahler DFS in `morphology.py` that can be ported
  to HOC in a follow-up if leaf-dendrite identification proves insufficient for the "branch order >=
  3" constraint in the task description.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Tuning-curve response visualization library
* **Status**: completed
* **Relevance**: Provides the `tuning_curve_viz` library with polar / Cartesian / multi-model-
  overlay / raster+PSTH plot functions and the Okabe-Ito palette. Used optionally for diagnostic
  per-length polar plots.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring and loss library
* **Status**: completed
* **Relevance**: Provides the `tuning_curve_loss` library with `compute_dsi`, `compute_peak_hz`,
  `compute_null_hz`, `compute_hwhm_deg`, `load_tuning_curve`, and `score`. Primary DSI scorer for
  this task — one call per sweep point.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC with gabaMOD PD/ND swap
* **Status**: completed
* **Relevance**: Sibling DSGC port (not directly reused). Demonstrates an alternative DS driver
  (gabaMOD swap) and the same NEURON bootstrap pattern that t0022 inherits. Background only.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC port with spatially-asymmetric inhibition for channel testbed
* **Status**: completed
* **Relevance**: **The direct dependency.** Provides the `modeldb_189347_dsgc_dendritic` library —
  the testbed we are sweeping. Supplies the per-dendrite E-I scheduler, the channel-partition HOC
  overlay, the canonical constants, the Windows NEURON bootstrap, the per-trial baseline-drift
  guardrails, and the tuning-curve CSV schema. The t0022 baseline DSI = 1.0 at baseline length is
  the reference point for the sweep.

### [t0026]

* **Task ID**: `t0026_vrest_sweep_tuning_curves_dsgc`
* **Name**: V_rest sweep tuning curves for t0022 and t0024 DSGC ports
* **Status**: completed
* **Relevance**: **The direct structural template.** Demonstrates exactly how to design a
  one-parameter sweep driver on top of t0022: override helper, build-once cell context,
  per-row-flushed tidy CSV, per-sweep-value metrics reducer, two-panel summary plot. t0029's
  architecture is a straight analogue with `L` in place of `V_rest`.
