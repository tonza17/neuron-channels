---
spec_version: "1"
task_id: "t0030_distal_dendrite_diameter_sweep_dsgc"
research_stage: "code"
tasks_reviewed: 11
tasks_cited: 11
libraries_found: 6
libraries_relevant: 3
date_completed: "2026-04-22"
status: "complete"
---
# Research Code: Distal-Dendrite Diameter Sweep on the t0022 DSGC Testbed

## Task Objective

Sweep the diameter of distal dendritic compartments on the existing t0022 DSGC channel testbed
across seven multipliers (**0.5×, 0.75×, 1.0×, 1.25×, 1.5×, 1.75×, 2.0×** of baseline `seg.diam`),
apply the multiplier uniformly to all distal branches (branch order ≥ 3 — operationally HOC leaf
dendrites on the ON arbor), run the canonical 12-direction × 10-trial tuning protocol at each
diameter, compute DSI via the t0012 `tuning_curve_loss` scorer, and classify the slope sign of the
DSI-vs-diameter curve to discriminate Schachter2010 active-dendrite amplification (positive slope
predicted) from passive-filtering alternatives (negative slope predicted). No channel edits, no
input rewiring, local CPU only, zero external cost. Outputs are `results/data/sweep_results.csv`,
`results/images/dsi_vs_diameter.png`, and per-diameter DSI entries in `results/metrics.json`. This
task is the geometry partner to the just-completed distal-length sweep [t0029] — length varies
spatial integration, diameter varies local impedance and Nav substrate per unit length.

## Library Landscape

Six libraries are registered in the project (confirmed via `overview/libraries/README.md`; no
correction overlays apply). Three are directly relevant to this task.

* `modeldb_189347_dsgc_dendritic` ([t0022], v0.1.0) — **Highly relevant.** The testbed we are
  sweeping. Registered `module_paths` include `code/neuron_bootstrap.py`,
  `code/run_tuning_curve.py`, `code/constants.py`, `code/paths.py`, `code/score_envelope.py`,
  `code/plot_tuning_curve.py`, and `code/dsgc_channel_partition.hoc`. Import via
  `from tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve import (EiPair, build_ei_pairs, schedule_ei_onsets, _preload_nrnmech_dll, _source_channel_partition_hoc, _silence_baseline_hoc_synapses, _assert_bip_and_gabamod_baseline, _count_threshold_crossings)`.

* `tuning_curve_loss` ([t0012], v0.1.0) — **Highly relevant.** Primary DSI / peak / null / HWHM /
  reliability / RMSE scorer. Import via
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, load_tuning_curve, TuningCurve, METRIC_KEY_DSI, METRIC_KEY_HWHM, METRIC_KEY_RELIABILITY)`.
  The library consumes the canonical `(angle_deg, trial_seed, firing_rate_hz)` CSV that the t0022
  driver emits, so per-sweep-point curves score without format conversion.

* `modeldb_189347_dsgc` ([t0008], v0.1.0) — **Indirectly relevant.** Supplies `build_dsgc`,
  `apply_params`, `read_synapse_coords`, `SynapseCoords` via
  `tasks.t0008_port_modeldb_189347.code.build_cell`. These are already called transitively by the
  t0022 driver; t0030 imports them directly only to build the per-trial runner.

* `tuning_curve_viz` ([t0011], v0.1.0) — **Relevant for optional diagnostics.** Exports
  `plot_polar_tuning_curve`, `plot_cartesian_tuning_curve`, `plot_multi_model_overlay`, and the
  Okabe-Ito palette. The primary `dsi_vs_diameter.png` chart is a scalar sweep (not a tuning curve)
  and therefore lives outside this library's surface; but per-diameter polar plots are a cheap
  diagnostic.

* `modeldb_189347_dsgc_gabamod` ([t0020], v0.1.0) — **Not relevant.** Sibling port driving DS via
  the gabaMOD PD/ND scalar swap instead of per-dendrite E-I timing. No reusable geometry code.

* `de_rosenroll_2026_dsgc` ([t0024], v0.1.0) — **Not relevant.** Alternative DSGC port with an
  AR(2)-noise driver and a different HOC template; the t0030 sweep is t0022-only.

## Key Findings

### The t0022 driver entry-point is `run_tuning_curve.py`, and its `build_ei_pairs` must run exactly once per process

The canonical driver `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py` (683 lines)
[t0022] exposes three `_main_*` entry modes (`--dry-run`, `--preflight`, default full sweep). The
full-sweep body at lines 621-650 is the pattern to clone: preload `nrnmech.dll`, build the DSGC cell
via `build_dsgc()`, source the channel-partition HOC overlay, build per-dendrite E-I pairs, snapshot
baseline `SynapseCoords` and `h.gabaMOD`, then iterate `N_ANGLES × N_TRIALS = 120` trials through
`run_one_trial_dendritic`. Building the cell takes ~1.6 s and `build_ei_pairs` traverses `h.RGC.ON`
(282 sections on the bundled morphology) to create 282 AMPA/GABA `Exp2Syn` pairs with dedicated
NetStim/NetCon drivers; both must happen exactly once per process because the `EiPair.x_mid_um` /
`y_mid_um` fields are captured at build time from the section's 3D points [t0022] and are used in
`_compute_onset_times_ms` to schedule per-angle onsets
(`run_tuning_curve.py:181-196, 199-260, 274-306`). The sibling [t0029] driver proved this pattern
carries over unchanged to a geometry sweep: `trial_runner_length.build_cell_context` (84 lines)
builds once, mutates `sec.L` per outer sweep iteration, and amortises the build cost over 840 trials
[t0029].

### Distal sections are identified by HOC leaf + ON-arbor membership; this is an established rule on this morphology

The t0022 testbed reuses the bundled Poleg-Polsky morphology from [t0008]
(`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/RGCmodel.hoc`), which
declares soma + 350 dend sections (0 axon), of which 282 belong to the `h.RGC.ON` `SectionList`
(derived from the HOC's `z3d > 0` test in `RGCmodel.hoc:11817-11826`) [t0008]. The task
description's "branch order ≥ 3 tip compartments" rule is implementable as HOC leaves on the ON
arbor: a section `sec` is distal if `sec in h.RGC.ON` (by name match) and
`h.SectionRef(sec=sec).nchild() == 0`. [t0029] encoded this exact rule as
`identify_distal_sections(*, h: Any) -> list[Any]` in
`tasks/t0029_distal_dendrite_length_sweep_dsgc/code/length_override.py:37-52` (16 lines); the
sibling preflight logged the result in `logs/preflight/distal_sections.json`. **t0030 must copy this
function verbatim** into its own `code/diameter_override.py` (rule-9 prohibits cross-task
non-library imports; `length_override.py` is NOT registered in any library). A companion preflight
(cloned from `preflight_distal.py` [t0029]) must assert that `count >= 50` and `min_depth >= 3`
before the full sweep launches — the same validation gates [t0029] used.

### Diameter is set by `pt3dadd`, but `seg.diam *= multiplier` is the correct live-handle scaler

Section diameters on this morphology come from `pt3dadd(x, y, z, diam)` statements in `RGCmodel.hoc`
lines 214+ [t0008] (hundreds of 4-tuple calls; each `dend[i]` has 2-10 3D points with per-point
diameters ranging ~0.4-12 µm). No Python code in [t0008], [t0022], or [t0026] mutates diameter; only
`tasks/t0008_port_modeldb_189347/code/report_morphology.py:64` *reads* `float(sec(0.5).diam)`
[t0008]. NEURON's convention when `nseg=1` and 3D points exist: setting `seg.diam = v` on the single
segment propagates to the underlying 3D points via NEURON's d_lambda discretiser (internally a
uniform-diameter overwrite of the 3D profile), while the spatial `(x, y, z)` coordinates remain
untouched. Because `RGCmodel.hoc:11817-11818` sets `forall { nseg=1 }` on every section [t0008],
each section has exactly one segment and `sec.diam *= m` or `for seg in sec: seg.diam *= m` yields
an unambiguous uniform rescale. The t0030 diameter override should therefore follow the [t0029]
`set_distal_length_multiplier` pattern with `sec.L` replaced by `seg.diam`:

```python
def set_distal_diameter_multiplier(*, h, distal_sections, baseline_diam, multiplier):
    for sec in distal_sections:
        for seg in sec:
            baseline = baseline_diam[(id(sec), seg.x)]
            seg.diam = float(baseline) * float(multiplier)
```

Baseline capture must key on `(id(sec), seg.x)` because each `seg` has its own `diam` (though with
`nseg=1` there is one seg per section). The post-override assertion should compare `seg.diam` to
`baseline_diam[key] * multiplier` within 1e-9 µm tolerance.

### Geometry overrides must NOT disturb bar-arrival-time scheduling

`_compute_onset_times_ms` (`run_tuning_curve.py:274-306` [t0022]) computes each AMPA/GABA onset from
`pair.x_mid_um` and `pair.y_mid_um`, which are captured once at `build_ei_pairs` time via
`_section_midpoint` averaging `x3d(i)` / `y3d(i)` over the section's 3D points [t0022]. Rescaling
`seg.diam` changes the section's membrane capacitance, axial resistance, and local input impedance
but **does not move** the stored 3D points, so the bar onset schedule is preserved. This is the same
property [t0029] exploited for its length sweep. Document this in the driver with a comment and a
midpoint-snapshot assertion (compare `pair.x_mid_um` / `y_mid_um` before and after each override to
confirm no drift).

### Input-impedance physics: thicker = lower Z, leading to the Schachter2010 vs passive-filtering dichotomy

[t0027] synthesises the two competing predictions [t0027]. **Schachter2010 active-dendrite
amplification** [t0027, full_answer.md:117-119]: "local input resistance scales from 150-200 MΩ
proximally to >1 GΩ distally, producing a spatial gradient of dendritic-spike threshold: ~1 nS
suffices distally while 3-4 nS is needed proximally, yielding a ~4× amplification of DSI via
dendritic Na/Ca-channel threshold nonlinearity." Under this mechanism, thickening distal dendrites
increases their local Nav/Kv substrate per unit length (Nav channel density × membrane area ↑) and
tips the preferred-direction EPSP over the dendritic-spike threshold more readily than the
null-direction EPSP, so DSI should **increase** with multiplier. **Passive-filtering alternatives**
predict the opposite: thicker distal dendrites have lower input impedance (Z ∝ 1/d^1.5 per cable
theory), so the same synaptic current produces a smaller local depolarisation; the
directional-contrast signal is damped at the soma and DSI should **decrease** with multiplier.
[Wu2023] in the [t0027] synthesis [t0027, full_answer.md:108-113] reports that distal SAC diameter
saturates DSI once it exceeds ~0.8 µm — the baseline distal `diam` on our morphology is ~0.4-1.0 µm
per `pt3dadd` samples in `RGCmodel.hoc`, putting us near the transition region where both mechanisms
plausibly compete. This makes the sweep a sharp binary discriminator.

### Nav substrate density priors: relevant for interpretation, not for the sweep itself

[t0019] synthesised Nav/Kv density priors [t0019]. For an RGC, dendritic Nav peaks at ~0.03 S/cm² on
ModelDB-189347 (the prior used by the t0022 channel-partition HOC) with AIS Nav densities ~100×
higher [t0019, t0022]. The t0030 sweep does **not** change channel densities — it only changes
`seg.diam`. With uniform Nav density `gbar_Nav` (S/cm²), total Nav current capacity scales as
surface area ∝ `L × π × d`, so a 2× diameter increase doubles dendritic Nav current per unit length.
This is the quantitative lever behind the Schachter2010 prediction: if the DSI-vs-diameter slope is
strongly positive, the dendritic Nav substrate really is rate-limiting; if it is flat or negative,
the passive cable dominates and active amplification is below threshold. The t0030 results will
therefore inform any downstream "active-dendrite" morphology-channel co-optimisation task (e.g.
t0033 in the brainstorm pipeline).

### The sweep driver pattern from [t0029] is a direct, 20-line-delta clone target

`tasks/t0029_distal_dendrite_length_sweep_dsgc/code/run_length_sweep.py` (239 lines) [t0029] is
literally a length version of the diameter sweep t0030 needs. Structure: `CellContext` built once
via `build_cell_context` (cloned from t0026 pattern); outer loop over
`LENGTH_MULTIPLIERS = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)`; inner double loop over
`(angle_deg, trial_idx)`; tidy CSV with `fh.flush()` after each row for crash recovery; per-length
canonical-format curve CSV emitted at the end of each outer iteration; per-length wall-time JSON.
**t0030 delta**: rename the sweep grid to `DIAMETER_MULTIPLIERS` (same 7 values), swap
`set_distal_length_multiplier` for `set_distal_diameter_multiplier`, replace `length_multiplier` CSV
column with `diameter_multiplier`, and swap the baseline snapshot from `{id(sec): sec.L}` to
`{(id(sec), seg.x): seg.diam}` (to cover the `nseg=1` single-segment case cleanly and leave room for
future `nseg>1` extensions). All other lines — NEURON bootstrap, silence-HOC, E-I onset scheduling,
baseline-drift assertion, per-trial `apply_params` seeding — carry over verbatim.

### Wall-time estimate: ~42 min, matching [t0029] full-sweep wall time

[t0029] full sweep (7 multipliers × 12 angles × 10 trials = 840 trials) completed in **2,541 s ≈ 42
min** on this Windows workstation
(`tasks/t0029_distal_dendrite_length_sweep_dsgc/results/data/wall_time_by_length.json` [t0029]).
Per-sweep-point wall time ranged from 333 s (1.75×) to 437 s (1.5×), with a mean of ~363 s. Because
t0030 uses the identical protocol (same 840 trials, identical `TSTOP_MS=1000`, identical `nseg=1`
regime where `apply_params` → `h.finitialize` → `h.continuerun(1000)` is the dominant cost), the
expected t0030 wall time is **~40-60 min**, comfortably inside the 30-90 min budget in
`task_description.md`. No remote compute, no paid APIs. The full 840-trial sweep is therefore the
default; the preflight (3 angles × 2 trials × 3 multipliers = 18 trials) should complete in ~1 min.

### Metrics-reducer and plot-emitter patterns from [t0029] are directly transferable

[t0029] emits per-multiplier metrics (DSI, peak Hz, null Hz, HWHM, vector-sum DSI, reliability) via
`compute_length_metrics.py` [t0029] and the summary chart via `plot_dsi_vs_length.py` [t0029]. Both
files are non-library task code, so they must be copied into t0030's `code/` directory and adapted
(axis rename, path constants). The `classify_curve_shape.py` classifier in [t0029] (monotonic /
saturating / non-monotonic with `MONOTONIC_SLOPE_MIN_PER_UNIT = 0.05` and `MONOTONIC_P_MAX = 0.05`)
is directly applicable but the t0030 task description asks for a simpler binary decision: **positive
slope = Schachter2010 active amplification; negative slope = passive filtering; flat = neither**.
The classifier can be reduced to a signed-slope linear regression with a t-test on the slope
coefficient.

### Baseline DSI = 1.0 at the t0022 baseline is a known plateau; plan for secondary metrics

[t0029] discovered that DSI (peak-minus-null formulation per t0012) pins at **1.000 at every length
multiplier** in the t0022 testbed, because the deterministic driver produces zero firing at any
angle ≥ 150° from the preferred direction [t0029]. The `t0029/results_summary.md` reports this
explicitly: DSI = 1.000 range 0.000; vector-sum DSI moved only 0.021 across the entire sweep (0.664
→ 0.643) [t0029]. The same plateau is likely for t0030 unless diameter changes substantially alter
the null-direction firing rate. **Mitigation**: emit vector-sum DSI (Mazurek & Kagan 2020
formulation, already implemented in `t0029/compute_length_metrics.py` [t0029]) as the secondary DSI
and report peak Hz, null Hz, and vector-sum DSI side-by-side with the primary DSI. If primary DSI
saturates again, vector-sum DSI plus peak-vs-diameter plus null-vs-diameter trends still
discriminate Schachter2010 from passive filtering cleanly.

## Reusable Code and Assets

### t0022 per-dendrite E-I scheduler and helpers — import via library

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py` (683 lines,
  registered in `modeldb_189347_dsgc_dendritic` library).
* **What it does**: Builds per-dendrite AMPA/GABA E-I pairs on `h.RGC.ON`, schedules bar-
  direction-dependent onsets, runs one trial returning firing rate in Hz, writes canonical CSV.
* **Reuse method**: **import via library**.
* **Function signatures** to import:
  * `build_ei_pairs(*, h: Any) -> list[EiPair]`
  * `schedule_ei_onsets(*, h: Any, pairs: list[EiPair], angle_deg: float, velocity_um_per_ms: float, gaba_null_pref_ratio: float, trial_seed: int) -> list[dict[str, float]]`
  * `_preload_nrnmech_dll() -> None`
  * `_source_channel_partition_hoc(*, h: Any) -> None`
  * `_silence_baseline_hoc_synapses(*, h: Any) -> None`
  * `_assert_bip_and_gabamod_baseline(*, h: Any, baseline_coords: list[SynapseCoords], baseline_gaba_mod: float) -> None`
  * `_count_threshold_crossings(*, samples: list[float], threshold_mv: float) -> int`
  * `EiPair` (frozen-slots dataclass)

### t0022 NEURON bootstrap — import via library

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/neuron_bootstrap.py` (64 lines,
  registered in `modeldb_189347_dsgc_dendritic` library).
* **What it does**: `ensure_neuron_importable()` sets `NEURONHOME`, adds NEURON Python bindings to
  `sys.path`, registers the DLL directory, and re-execs once if `NEURONHOME` is missing.
* **Reuse method**: **import via library** — call at module scope before any `neuron` import.
* **Function signature**: `ensure_neuron_importable() -> None`.
* **Adaptation needed**: None. The t0022 sentinel env-var `_T0022_NEURONHOME_BOOTSTRAPPED` is
  idempotent.

### t0022 channel-partition HOC overlay — import via library

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/dsgc_channel_partition.hoc` (108 lines,
  registered in `modeldb_189347_dsgc_dendritic` library).
* **What it does**: After `build_dsgc()`, declares 5 `SectionList` globals (`SOMA_CHANNELS`,
  `DEND_CHANNELS`, `AIS_PROXIMAL`, `AIS_DISTAL`, `THIN_AXON`) and populates them from `RGC.soma` and
  `RGC.dends`. AIS lists are intentionally empty on this morphology. The `forsec` blocks are
  baseline passthrough (no channel density edits) — exactly what t0030 wants.
* **Reuse method**: **import via library** (called via `_source_channel_partition_hoc`).
* **Adaptation needed**: None.

### t0022 canonical constants — import via library

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/constants.py` (146 lines, registered in
  `modeldb_189347_dsgc_dendritic` library).
* **What it does**: Centralises every magic number the testbed uses: `TSTOP_MS=1000.0`, `DT_MS=0.1`,
  `CELSIUS_DEG_C=32.0`, `N_ANGLES=12`, `N_TRIALS=10`, `ANGLE_STEP_DEG=30.0`,
  `AP_THRESHOLD_MV=-10.0`, `V_INIT_MV=-65.0`, `BAR_VELOCITY_UM_PER_MS=1.0`,
  `BAR_BASE_ONSET_MS=200.0`, E-I onset offsets (`EI_OFFSET_PREFERRED_MS=10.0`,
  `EI_OFFSET_NULL_MS=-10.0`), conductances (`AMPA_CONDUCTANCE_NS=6.0`,
  `GABA_CONDUCTANCE_PREFERRED_NS=3.0`, `GABA_CONDUCTANCE_NULL_NS=12.0`), kinetics, segment locations
  (`AMPA_SEG_LOCATION=0.9`, `GABA_SEG_LOCATION=0.3`), CSV column names, and metric keys.
* **Reuse method**: **import via library**. Do not redefine any of these in t0030.

### t0012 tuning-curve scorer — import via library

* **Source**: `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/` (8 modules,
  registered as `tuning_curve_loss` library).
* **What it does**: Loads a canonical 12-angle CSV, computes DSI (peak-minus-null), peak Hz, null
  Hz, HWHM, split-half reliability, and RMSE against the t0004 target.
* **Reuse method**: **import via library** through the package `__init__.py`.
* **Function signatures**:
  * `load_tuning_curve(csv_path: Path) -> TuningCurve`
  * `compute_dsi(*, curve: TuningCurve) -> float`
  * `compute_peak_hz(*, curve: TuningCurve) -> float`
  * `compute_null_hz(*, curve: TuningCurve) -> float`
  * `compute_hwhm_deg(*, curve: TuningCurve) -> float`
  * `compute_reliability(*, curve: TuningCurve) -> float | None`
* **Metric-key constants**: `METRIC_KEY_DSI`, `METRIC_KEY_HWHM`, `METRIC_KEY_RELIABILITY`.
* **Adaptation needed**: None. For each of 7 sweep points emit one canonical-format
  `(angle_deg, trial_seed, firing_rate_hz)` CSV in `results/data/per_diameter/` and call
  `load_tuning_curve` followed by `compute_dsi`/`compute_peak_hz`/`compute_null_hz`/
  `compute_hwhm_deg`.

### t0029 distal-selection + override pattern — copy into task

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/length_override.py` (104 lines)
  and `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/preflight_distal.py` (149 lines).
* **What it does**: `identify_distal_sections(*, h)` returns HOC-leaf dendrite sections on the ON
  arbor; `snapshot_distal_lengths(*, h, distal_sections)` captures baseline `sec.L` keyed by
  `id(sec)`; `set_distal_length_multiplier(*, h, distal_sections, baseline_L, multiplier)` rescales;
  `assert_distal_lengths(..., tol=1e-9)` verifies. The preflight script asserts
  `count >= DISTAL_MIN_COUNT = 50` and `min_depth >= DISTAL_MIN_DEPTH = 3`.
* **Reuse method**: **copy into task** (NOT registered as a library — per the CLAUDE.md rule-3
  cross-task import prohibition, non-library code must be copied).
* **Adaptation**: Rename module to `diameter_override.py`; rename functions to
  `snapshot_distal_diameters` / `set_distal_diameter_multiplier` / `assert_distal_diameters`; swap
  `sec.L` for `seg.diam` and key the snapshot on `(id(sec), seg.x)`. `identify_distal_sections` is
  geometry-agnostic and can be copied verbatim. Estimated delta: ~15-line swap per module, total
  ~120 lines in `code/diameter_override.py` + ~150 in `code/preflight_distal.py`.

### t0029 trial runner — copy into task

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/trial_runner_length.py` (179
  lines).
* **What it does**: Wraps `build_cell_context` (one-time build) and
  `run_one_trial_length(*, ctx, angle_deg, trial_seed, multiplier) -> TrialOutcome`, where
  `TrialOutcome` is a frozen-slots dataclass with `(spike_count, peak_mv, firing_rate_hz)`.
  `run_one_trial_length` interleaves `apply_params` / `_silence_baseline_hoc_synapses` /
  `_assert_bip_and_gabamod_baseline` / `set_distal_length_multiplier` / `assert_distal_lengths` /
  `schedule_ei_onsets` / `h.finitialize` / `h.continuerun(TSTOP_MS)` in the exact order required.
* **Reuse method**: **copy into task**. Rename to `trial_runner_diameter.py`; rename
  `run_one_trial_length` → `run_one_trial_diameter`; swap override imports; the 20-line
  `build_cell_context` body extends to include `snapshot_distal_diameters` in the `CellContext`.

### t0029 sweep driver — copy into task

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/run_length_sweep.py` (239 lines).
* **What it does**: Parses CLI args (`--preflight`, `--output`, `--wall-time-output`), builds
  `CellContext` once, iterates the outer sweep, emits tidy CSV (flushed per-row), emits per-
  multiplier canonical-format curve CSV, emits per-multiplier wall-time JSON, and performs a final
  restore-to-baseline assertion.
* **Reuse method**: **copy into task**. Rename module to `run_diameter_sweep.py`; rename
  `LENGTH_MULTIPLIERS` → `DIAMETER_MULTIPLIERS`; rename `length_multiplier` column →
  `diameter_multiplier`; swap override call signature; rename per-multiplier filename from
  `tuning_curve_L<label>.csv` → `tuning_curve_D<label>.csv`.

### t0029 metrics reducer — copy into task

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/compute_length_metrics.py` (line
  count N/A; clone of `t0026/compute_vrest_metrics.py`).
* **What it does**: Reads tidy CSV, groups by sweep value, computes per-group DSI (vector-sum +
  peak-minus-null), preferred direction, HWHM, peak Hz, null Hz, and mean peak V_soma. Writes
  per-sweep-value metrics CSV + notes JSON.
* **Reuse method**: **copy into task**. Rename axis constants; otherwise structurally identical.

### t0029 classifier — copy and simplify

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/classify_curve_shape.py`.
* **What it does**: Labels the DSI-vs-multiplier curve as `monotonic`, `saturating`, or
  `non_monotonic` via signed-slope linear regression and max-fraction saturation tests.
* **Reuse method**: **copy into task**. For t0030 the task description asks for a simpler ternary:
  positive slope = Schachter2010 amplification; negative slope = passive filtering; flat = neither.
  Retain the regression machinery and add an `interpret_slope_sign` helper that maps
  `(slope, p_value)` → `{"schachter2010_amplification", "passive_filtering", "flat"}` labels.

### t0029 plot emitter — copy into task

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/plot_dsi_vs_length.py`.
* **What it does**: Two-panel Cartesian plot (DSI on left axis, peak Hz on right axis, vs sweep
  axis); per-multiplier polar plots via `tuning_curve_viz.plot_polar_tuning_curve`.
* **Reuse method**: **copy into task**. Rename axis; swap output path constant; point the loader at
  `tuning_curve_D*.csv` files.

### t0011 tuning-curve visualiser — import via library (optional)

* **Source**: `tasks/t0011_response_visualization_library/code/tuning_curve_viz/` (10 modules,
  registered as `tuning_curve_viz` library).
* **Function signatures**:
  * `plot_polar_tuning_curve(curve_csv: Path, out_png: Path, *, show_trials: bool = True, target_csv: Path | None = None) -> None`
  * `plot_multi_model_overlay(curve_csvs: list[Path], labels: list[str], out_png: Path, ...) -> None`
* **Reuse method**: **import via library** for optional per-diameter polar diagnostics. The primary
  `dsi_vs_diameter.png` scalar-sweep chart is out of scope for this library and must be written
  directly with matplotlib (see the plot-emitter item above).

### t0027 synthesis answer — reference only

* **Source**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/answer/ morphology-direction-selectivity-modeling-synthesis/full_answer.md`
  [t0027].
* **What it provides**: The Schachter2010 (~4× DSI amplification via dendritic Nav threshold
  nonlinearity, distal 1-GΩ impedance) and Wu2023 (DSI saturates above distal diameter ~0.8 µm)
  predictions that define the slope-sign hypothesis test for this task. Read-only; no code reuse.

### t0019 Nav/Kv density priors — reference only

* **Source**:
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/ nav-kv-combinations-for-dsgc-modelling/full_answer.md`
  [t0019].
* **What it provides**: Dendritic Nav density ~0.03 S/cm² prior used by the t0022 channel-partition
  HOC [t0022]; relevant for interpreting whether the sweep's DSI-vs-diameter slope is rate-limited
  by Nav substrate.

## Common Patterns

* **Call `ensure_neuron_importable()` before any `neuron` import** [t0022, t0026, t0029].
* **Canonical CSV schema** `(angle_deg, trial_seed, firing_rate_hz)` is the t0012 scorer input
  format [t0004, t0008, t0020, t0022, t0024, t0026, t0029]. t0030 per-diameter CSVs follow this.
* **Per-trial seed** `1000 * angle_idx + trial_idx + 1` [t0008, t0022, t0026, t0029]. t0030 retains
  this, with the diameter-multiplier index as an orthogonal outer dimension so seeds remain unique
  across sweep points.
* **Tidy wide CSV + `fh.flush()` after every row** enables crash-recovery [t0026, t0029].
* **Build once, override per outer sweep iteration, re-seed per inner trial** [t0026, t0029].
  `apply_params` MUST stay inside the inner trial loop because it re-seeds NEURON Random123.
* **Baseline-drift assertions after every override** [t0022, t0026, t0029]. t0030 must add
  `assert_distal_diameters` after every `set_distal_diameter_multiplier` call and restore to
  baseline (multiplier = 1.0) at sweep end.
* **Preflight gate before full sweep** [t0022, t0029]. t0030 preflight uses 3 angles × 2 trials × 3
  multipliers (0.5, 1.0, 2.0) = 18 trials, ~1 min.

## Lessons Learned

* **Build-once vs rebuild-per-sweep-point**: NEURON cell build + channel-partition HOC source +
  282-pair E-I creation costs ~1.6 s [t0022]. Rebuilding per diameter multiplier (7×) would waste
  ~11 s and introduce spurious differences from stochastic cell-build state. [t0029] proved that
  mutating `sec.L` on the live handle per sweep iteration works correctly; the same will be true for
  `seg.diam`.

* **Silencing bundled HOC synapses is mandatory**: omitting `_silence_baseline_hoc_synapses`
  produces a ~13-15 Hz baseline firing rate that confounds the per-dendrite E-I driver [t0022].
  Every t0030 trial must call it right after `apply_params`.

* **`apply_params` resets Random123 streams and `v_init`**: hoisting it out of the inner trial loop
  makes every trial return the same result because the deterministic seed never rotates
  [t0026, t0029]. Keep `apply_params(h, seed=trial_seed)` inside the `run_one_trial_diameter` body.

* **`sec.L` and `seg.diam` rescaling with `nseg=1` is unambiguous** [t0029]. The t0008 HOC sets
  `forall { nseg=1 }` [t0008], so each section has exactly one segment and
  `seg.diam = baseline * multiplier` is a direct uniform rescale. If a future task changes
  `nseg > 1`, the per-segment snapshot `{(id(sec), seg.x): baseline_diam}` keyed-by-segment keeps
  the override correct.

* **HOC 3D-point coordinates do not change when `seg.diam` is mutated** (NEURON convention).
  `pair.x_mid_um` / `y_mid_um` stay stable across diameter multipliers, so bar-arrival-time
  scheduling is preserved. Add a midpoint-snapshot assertion in the driver to make this guarantee
  explicit.

* **DSI can saturate at 1.000 on this testbed** [t0029]. If null-direction firing is zero at every
  angle ≥ 150° from preferred, primary DSI (peak-minus-null) pins at 1.0 regardless of geometry.
  Mitigation: emit vector-sum DSI, peak Hz, and null Hz as parallel diagnostics so the slope-sign
  decision remains tractable even if primary DSI is flat.

* **Crash-recovery via per-row `fh.flush()` proved valuable in [t0024]** (960-trial sweep,
  intermittent issues over 3.2 h) and was retained in [t0026] and [t0029]. t0030 follows the same
  pattern: the ~45-min sweep is short enough that a single NEURON crash at trial 800 would be
  recoverable by inspecting the partial tidy CSV.

## Recommendations for This Task

### Architecture

1. Clone the [t0029] four-file architecture: `code/diameter_override.py`,
   `code/preflight_distal.py`, `code/trial_runner_diameter.py`, `code/run_diameter_sweep.py`, plus
   `code/compute_diameter_metrics.py`, `code/classify_curve_shape.py`,
   `code/plot_dsi_vs_diameter.py`, `code/constants.py`, and `code/paths.py`. All non-library; all
   copies per the CLAUDE.md cross-task import rule.

2. Import the following via the `modeldb_189347_dsgc_dendritic` library: `ensure_neuron_importable`,
   `EiPair`, `build_ei_pairs`, `schedule_ei_onsets`, `_preload_nrnmech_dll`,
   `_source_channel_partition_hoc`, `_silence_baseline_hoc_synapses`,
   `_assert_bip_and_gabamod_baseline`, `_count_threshold_crossings`, plus all t0022 `constants.py`
   symbols.

3. Import the following via the `modeldb_189347_dsgc` library: `build_dsgc`, `apply_params`,
   `read_synapse_coords`, `SynapseCoords`.

4. Import the following via the `tuning_curve_loss` library: `load_tuning_curve`, `TuningCurve`,
   `compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`,
   `METRIC_KEY_DSI`, `METRIC_KEY_HWHM`, `METRIC_KEY_RELIABILITY`.

### Distal-section identification

5. Define "distal" as **HOC leaves on the ON arbor**: `sec in h.RGC.ON` (by name match) AND
   `h.SectionRef(sec=sec).nchild() == 0`. Copy `identify_distal_sections` verbatim from [t0029]'s
   `length_override.py:37-52`.

6. Preflight must assert `count >= 50` (expected ~100-150 on the bundled morphology) and
   `min_depth >= 3` (topological depth from soma along the HOC parent chain). Log counts, depth
   range, and baseline-diameter distribution (min / median / max) to
   `logs/preflight/distal_sections.json`.

### Sweep driver

7. Use `DIAMETER_MULTIPLIERS = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)` exactly as [t0029] used
   `LENGTH_MULTIPLIERS`. Trial count: `N_TRIALS = 10` (canonical t0022). Total trials: 7 × 12 × 10 =
   840\. Expected wall time ~42-60 min on this workstation based on [t0029]'s 2,541 s run.

8. Tidy CSV schema:
   `(diameter_multiplier, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`. One row per
   trial, `fh.flush()` after every row.

9. Emit one per-diameter canonical-format CSV `results/data/per_diameter/tuning_curve_D<label>.csv`
   with the t0012 schema `(angle_deg, trial_seed, firing_rate_hz)` so the t0012 scorer can be called
   without reshaping. File labels: `D0p50`, `D0p75`, ..., `D2p00`.

### Scorer integration

10. For each diameter point call `compute_dsi(curve=load_tuning_curve(csv_path=...))` and also
    `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, and `compute_reliability`. Write
    `dsi_diameter_<m>`, `hwhm_diameter_<m>`, `reliability_diameter_<m>` to `results/metrics.json`
    using the explicit multi-variant format (one variant per multiplier; follow the [t0029]
    `metrics.json` layout).

### Chart

11. Primary `results/images/dsi_vs_diameter.png`: two-panel Cartesian plot — left axis DSI vs
    multiplier, right axis peak Hz vs multiplier. Use the Okabe-Ito palette from
    `tuning_curve_viz.constants.OKABE_ITO`. Overlay vector-sum DSI as a dotted line on the DSI panel
    to guard against the baseline-DSI-plateau pitfall [t0029].

12. Diagnostic: 7 per-diameter polar PNGs via
    `plot_polar_tuning_curve(curve_csv=per_diameter_csv, out_png=images/polar_D<label>.png)`. This
    is optional but strongly recommended for visual QA.

### Slope-sign classifier

13. Fit a linear regression of DSI (primary and vector-sum) against `log2(multiplier)` across the 7
    sweep points. Report (slope, 95 % CI, p-value). Classification:

    * Positive slope with p < 0.05 and Δ(DSI) > 0.05 across 0.5×-2.0× → **Schachter2010 active-
      dendrite amplification** (favours dendritic Nav/Ca substrate amplifying preferred-direction
      EPSPs).
    * Negative slope with p < 0.05 and Δ(DSI) > 0.05 → **passive-filtering damping** (favours
      thicker-dendrite low-impedance equalising preferred and null inputs).
    * Otherwise → **flat / inconclusive** (fallback: inspect peak-vs-diameter and null-vs-diameter
      curves separately to check whether Schachter2010's predicted null-direction suppression vs
      passive-filtering's global damping is discernible).

14. If primary DSI saturates at 1.000 (the [t0029] pattern), fall back to vector-sum DSI for the
    slope-sign decision but retain primary DSI in the reported metrics.

### Guardrails

15. `build_cell_context` snapshots `{(id(sec), seg.x): seg.diam}` for every distal `(sec, seg)` pair
    before the outer sweep starts. After the outer sweep loop finishes, call
    `set_distal_diameter_multiplier(multiplier=1.0)` and `assert_distal_diameters(...)` to verify
    the live handle is back at baseline.

16. Add a per-trial midpoint-snapshot assertion inside `run_one_trial_diameter` comparing
    `pair.x_mid_um` / `y_mid_um` to the build-time snapshot (confirms the diameter override does not
    perturb 3D coordinates).

### Preflight

17. `--preflight` mode: 3 angles (0°, 120°, 240°) × 2 trials × 3 multipliers (0.5, 1.0, 2.0) = 18
    trials (~1 min). Must pass before launching the full sweep. Preflight output is written to
    `logs/preflight/tuning_curve_preflight.csv` and inspected by the plan's verification step.

### Logging

18. Emit to `logs/preflight/distal_sections.json`: distal count, min/median/max depth,
    min/median/max baseline diameter, total distal surface area (∑ π·L·d).
19. Emit to `data/wall_time_by_diameter.json`: wall-clock seconds per diameter point.
20. Emit to `data/curve_shape.json`: slope, 95 % CI, p-value, and mechanism label.

## Task Index

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate target DSGC tuning curve
* **Status**: completed
* **Relevance**: Defines the canonical `(angle_deg, trial_seed, firing_rate_hz)` CSV schema that
  t0012's scorer consumes and that every subsequent DSGC tuning-curve task emits. Used here as
  schema reference for per-diameter curve files.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 DSGC model (12-angle tuning curve)
* **Status**: completed
* **Relevance**: Registers the `modeldb_189347_dsgc` library. Bundles the Poleg-Polsky HOC sources
  (`RGCmodel.hoc` defines soma + 350 dend sections via `pt3dadd`; `forall { nseg=1 }`) that t0022
  and t0030 inherit. Supplies `build_dsgc`, `apply_params`, `read_synapse_coords`, `SynapseCoords`
  imported by the per-trial runner.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Tuning-curve response visualization library
* **Status**: completed
* **Relevance**: Registers the `tuning_curve_viz` library. Supplies `plot_polar_tuning_curve`,
  `plot_cartesian_tuning_curve`, `plot_multi_model_overlay`, and the Okabe-Ito colour palette. Used
  optionally for per-diameter diagnostic polar plots and for colour consistency on the primary
  `dsi_vs_diameter.png` chart.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring and loss library
* **Status**: completed
* **Relevance**: Registers the `tuning_curve_loss` library — the primary DSI scorer for this task.
  `compute_dsi` (peak-minus-null), `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`,
  `compute_reliability`, and `load_tuning_curve` are imported once per diameter point.

### [t0019]

* **Task ID**: `t0019_literature_survey_voltage_gated_channels`
* **Name**: Literature survey of voltage-gated channels for DSGC modelling
* **Status**: completed
* **Relevance**: Provides the `nav-kv-combinations-for-dsgc-modelling` answer asset with Nav/Kv
  density priors (dendritic Nav ~0.03 S/cm², AIS Nav ~2500-5000 pS/µm²). Relevant to interpreting
  the t0030 slope sign — whether the sweep is rate-limited by dendritic Nav substrate as
  Schachter2010 predicts.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC with gabaMOD PD/ND swap
* **Status**: completed
* **Relevance**: Registers the `modeldb_189347_dsgc_gabamod` library. Sibling DSGC port that drives
  DS via the gabaMOD PD/ND scalar swap instead of per-dendrite E-I timing; not relevant for geometry
  manipulation and therefore not reused, but documented in Library Landscape so the full library
  survey is auditable.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC port with spatially asymmetric inhibition for channel testbed
* **Status**: completed
* **Relevance**: **The direct dependency.** Registers the `modeldb_189347_dsgc_dendritic` library.
  Supplies the 12-direction per-dendrite E-I tuning protocol (`run_tuning_curve.py`), the
  channel-partition HOC overlay (SOMA/DEND/AIS_PROXIMAL/AIS_DISTAL/THIN_AXON `SectionList`s), the
  canonical constants, the Windows NEURON bootstrap, the per-trial baseline-drift guardrails, and
  the tuning-curve CSV schema. Every t0030 simulation trial runs through this testbed unchanged.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Sibling DSGC port (AR(2) stochastic release, different template). Not reused by
  t0030 but cited in [t0029]'s lessons for per-row-flushed crash-recovery pattern.

### [t0026]

* **Task ID**: `t0026_vrest_sweep_tuning_curves_dsgc`
* **Name**: V_rest sweep tuning curves for t0022 and t0024 DSGC ports
* **Status**: completed
* **Relevance**: The structural precursor to [t0029] and the present task — established the
  one-parameter sweep driver pattern on the t0022 testbed (`run_vrest_sweep_t0022.py`,
  `vrest_override.py`, `trial_runner_t0022.py`, `compute_vrest_metrics.py`, `plot_polar_tuning.py`
  summary figure). Also the source of the "build cell context once" optimisation. Cited through
  [t0029]'s research_code.md as an indirect reference.

### [t0027]

* **Task ID**: `t0027_literature_survey_morphology_ds_modeling`
* **Name**: Literature survey of morphology × direction-selectivity modelling
* **Status**: completed
* **Relevance**: Provides the `morphology-direction-selectivity-modeling-synthesis` answer asset
  which states the Schachter2010 active-dendrite amplification hypothesis (thicker distal ↑ DSI via
  Nav/Ca substrate) and the passive-filtering alternative (thicker distal ↓ DSI via lower local
  impedance) that define t0030's slope-sign hypothesis test. Also cites Wu2023's distal-SAC
  saturation above ~0.8 µm, useful for interpreting where our baseline sits on the mechanism
  landscape.

### [t0029]

* **Task ID**: `t0029_distal_dendrite_length_sweep_dsgc`
* **Name**: Distal-dendrite length sweep on the t0022 DSGC testbed
* **Status**: completed
* **Relevance**: **The direct structural template.** The sibling sweep task on the same testbed with
  an identical workflow — only the overridden geometry attribute differs (`sec.L` vs `seg.diam`).
  Every non-library module t0030 needs (override, preflight, trial runner, sweep driver, metrics
  reducer, classifier, plot emitter, constants, paths) has a 100-250-line analogue in
  `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/` that can be copied verbatim and adapted with
  a ~20-line delta per file per CLAUDE.md rule-3. The full [t0029] sweep ran in 2,541 s (~42 min) —
  the direct wall-time prior for t0030.
