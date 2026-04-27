---
spec_version: "1"
task_id: "t0052_minimal_dsgc_scalar_gaba"
research_stage: "code"
tasks_reviewed: 11
tasks_cited: 11
libraries_found: 7
libraries_relevant: 4
date_completed: "2026-04-25"
status: "complete"
---
# Research Code: Minimal From-Scratch DSGC with Scalar gabaMOD Inhibition

## Task Objective

Build a minimal from-scratch ON-OFF DSGC compartmental model on the project's calibrated baseline
morphology. The cell carries `hh` only on `soma` and `axon_initial_segment`, passive everywhere
else, 100 co-located E+I synapse pairs randomly placed on dendrites, position-gated AMPA events, and
direction-dependent inhibition implemented as a **scalar `gabaMOD(theta)` factor** applied to each
Exp2Syn IPSC weight (PD weight = 0.33 x base, ND weight = 0.99 x base, base = 2 nS). Run a
12-direction x 10-trial moving-bar sweep, emit per-direction soma V(t), aggregate EPSP/IPSP traces,
PSTHs, polar tuning curve, and DSI metrics; package the model as the `minimal_dsgc_scalar_gaba`
library asset. The implementation must be free of upstream Poleg-Polsky / t0022 lineage carryover.

## Library Landscape

The library aggregator is not yet implemented as a Python module on this branch
(`No module named arf.scripts.aggregators.aggregate_libraries`). Discovery used
`Glob tasks/*/assets/library/*` over the calibrated worktree state. Seven libraries are registered;
all `details.json` files are spec v2. None has correction overlays.

| Library ID | Created by | Relevance | Import path |
| --- | --- | --- | --- |
| `tuning_curve_viz` | [t0011] | **Relevant** — provides Cartesian + polar tuning-curve plots and per-angle raster+PSTH | `tasks.t0011_response_visualization_library.code.tuning_curve_viz` |
| `tuning_curve_loss` | [t0012] | **Relevant** — DSI / peak / null / HWHM / reliability / RMSE scoring | `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss` |
| `modeldb_189347_dsgc_exact` | [t0046] | **Relevant (pattern source)** — from-scratch DSGC layout, MOD compilation flow, NEURON Windows bootstrap, trial-runner skeleton, recording helpers (HOC-driven cell — not directly importable) |  |
| `modeldb_189347_dsgc_dendritic` | [t0022] | **Relevant (pattern source)** — Exp2Syn pair builder, NetStim/NetCon scheduler, position-gated event timing, 12-angle x 10-trial sweep harness (HOC-bundled cell — drop the HOC overlay) |  |
| `modeldb_189347_dsgc` | [t0008] | Marginal — superseded HOC-driven port using BIP coord rotation; only `apply_params` and `read_synapse_coords` patterns are referenced through t0022 |  |
| `modeldb_189347_dsgc_gabamod` | [t0020] | Marginal — `gabaMOD` swap pattern is what t0052 emulates (per-IPSC scaling) but the implementation is HOC-driven |  |
| `de_rosenroll_2026_dsgc` | [t0024] | Marginal — vendored HOC template + `_map_tree`/`_terminal_midpoint` helpers; cell construction is HOC-template-based |  |

For t0052 the only libraries that will be **imported** (vs. having patterns copied) are
`tuning_curve_viz` and `tuning_curve_loss`. Every DSGC cell library in the project loads its
morphology through a HOC `RGCmodel.hoc` or `RGCmodelGD.hoc` template; none of them load a SWC into
NEURON via Python. t0052 must therefore add a new SWC->NEURON loader; copying t0009's
`swc_io.parse_swc_file` is the right starting point but the SWC->`h.Section` builder is new code.

## Key Findings

### SWC Morphology Loading Is a New Code Path

Every prior DSGC build in the project [t0008] [t0020] [t0022] [t0024] [t0046] uses a HOC
`pt3dadd`-driven morphology template (`RGCmodel.hoc` or `RGCmodelGD.hoc`) bundled with the upstream
ModelDB code. The dendritic-diameter calibration task [t0009] produced
`dsgc-baseline-morphology-calibrated` as a SWC at
`tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`
(6,736 compartments: 19 soma + 6,717 dendrite, 129 branch points, 131 leaves, 1,536.25 um total
dendritic length, four distinct radii: soma 4.118 um / primary 3.694 um / mid 1.653 um / terminal
0.439 um). This dataset has **never been loaded into NEURON** by any prior task; the calibration
pipeline only validates SWC structure. The closest reusable code is
`tasks/t0009_calibrate_dendritic_diameters/code/swc_io.py` (215 lines), which contains
`parse_swc_file`, `validate_structure`, `summarize`, `build_children_index`, plus `SwcCompartment` /
`SwcSummary` dataclasses and the SWC type-code constants. t0052 must add a new
`build_dsgc_from_swc(swc_path) -> CellHandles` that converts each SWC row to an `h.Section`, sets
`pt3dadd(x, y, z, 2*r)` per compartment, hooks parents via `connect`, and tags soma vs dendrite
sections. NEURON's built-in `h.Import3d_SWC_read` is an alternative but requires sourcing
`import3d.hoc`; a pure-Python builder is preferred so soma/AIS/dendrite tagging is explicit.

### Position-Gated Event Scheduling Pattern Is Reusable

[t0022] established the position-gated event scheduler that this task needs. The core formula is the
bar-leading-edge crossing time:
`t_bar = (x_mid * cos(theta) + y_mid * sin(theta)) / velocity_um_per_ms + base_offset_ms`,
implemented in `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py:274-306` as
`_compute_onset_times_ms`. Each E and I synapse is given its own `h.NetStim` with `number=N`,
`noise=0`, `interval=...`, plus an `h.NetCon` whose `weight[0]` carries the scalar conductance in
microsiemens; `NetStim.start` is set per-trial per-synapse to the scheduled bar-crossing time. This
is the same "one event per synapse per trial" model the t0052 spec calls for, except t0052 needs
`number=1` (one event, not a burst) and per-pair (x, y) sampled from the dendritic arbor rather than
per-section midpoints. The `EiPair` dataclass at lines 104-127 is the right shape; copy it and trim
to `(ampa_syn, gaba_syn, ampa_netstim, gaba_netstim, ampa_netcon, gaba_netcon, x_um, y_um)`.

### Scalar `gabaMOD(theta)` Maps to Per-Trial NetCon Weight Updates

[t0022] implements direction-dependent GABA via per-pair conductance switching (preferred half-
plane vs null half-plane); [t0020] implements direction-dependent GABA via the HOC `h.gabaMOD`
global (PD=0.33, ND=0.99). The t0052 spec is closer to t0020 in that **every** I synapse's amplitude
is scaled by the same direction-dependent scalar
`gabaMOD(theta) = 0.33 + 0.66 * (1 - cos(theta - theta_ND)) / 2`, but unlike [t0020] the project
doesn't use a HOC global at all — the scalar is multiplied directly into each
`gaba_netcon.weight[0]` once per trial after `schedule_ei_onsets` sets the unit weight. This is
straightforward: compute `gaba_mod_theta = 0.33 + 0.66 * (1 - cos(radians(theta - 180))) / 2` once
per trial and assign `pair.gaba_netcon.weight[0] = GABA_BASE_NS * gaba_mod_theta * 1e-3` for every
pair.

### NEURON Bootstrap on Windows Is a Solved Problem

Every NEURON-using task (t0008, t0020, t0022, t0024, t0046) uses the same Windows bootstrap
sequence: set `NEURONHOME` env var to `C:\Users\md1avn\nrn-8.2.7`, `os.execv` re-exec if not already
set (so the C runtime sees it), insert `<NEURONHOME>/lib/python` into `sys.path`, call
`os.add_dll_directory(<NEURONHOME>/bin)`, then `import neuron`. The cleanest implementation is
`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/neuron_bootstrap.py` (57 lines) — it uses a
sentinel env var to prevent re-exec loops, and pairs with the `NEURONHOME_DEFAULT` constant in
`code/constants.py:NEURONHOME_DEFAULT`. Copy this file verbatim into t0052 with the sentinel renamed
to `_T0052_NEURONHOME_BOOTSTRAPPED`. The corresponding `paths.py:NEURONHOME_DEFAULT` constant is
shared across [t0007] [t0022] [t0024] [t0046] and is a pinned absolute path.

### MOD Compilation: Not Needed

Unlike [t0008] [t0020] [t0022] [t0024] [t0046] that all rely on Poleg-Polsky's custom MOD files
(`HHst.mod`, `bipolarNMDA.mod`, `SAC2RGCexc.mod`, `SAC2RGCinhib.mod`, `SquareInput.mod`,
`spike.mod`), t0052 needs **only** `Exp2Syn` (built into NEURON), `hh` (built into NEURON), and the
passive properties (`Ra`, `cm`, `pas`). No `nrnivmodl` step required, no custom DLL to load. This is
the largest simplification vs t0046; the cell builder reduces from ~170 lines (HOC sourcing
+ DLL loading + summary extraction) to roughly 80-120 lines of pure Python.

### Trial Runner and Recording Pattern

[t0046]'s `run_simplerun.run_one_trial` (197 lines, but only ~30 lines of recording machinery are
relevant) shows the canonical trial-recording loop: build a NEURON `Vector`, call
`v.record(soma(0.5)._ref_v)` and `t.record(_ref_t)`, optionally a
`NetCon(soma._ref_v, None, sec=soma)` with `netcon.threshold = AP_THRESHOLD_MV` and
`netcon.record(spike_vec)` for spike times, then `h.finitialize(V_INIT_MV)` and
`h.continuerun(TSTOP_MS)`. Convert the Vectors with `np.array(list(vec))`. [t0022]'s
`_count_threshold_crossings` (lines 386-397, 11 lines) is a simple alternative spike detector if the
NetCon path is undesirable. The t0052 spec asks for soma V(t) traces, EPSC/IPSC component sums
(which require **separate runs** with one set of synapses silenced), spike times, and per-synapse
activation times — so the trial-runner needs to support three modes: full E+I, AMPA-only,
GABA-only. The cleanest design is a `run_one_trial(*, mode: TrialMode, theta_deg, trial_seed)`
function with `TrialMode` enum.

### CSV Schemas for Tuning-Curve / Spike-Time Outputs

The project has two registered CSV schemas. The t0004/t0012 firing-rate schema is
`(angle_deg, trial_seed, firing_rate_hz)` — produced by [t0004] [t0008] [t0020] [t0022] [t0024]
and consumed by the `tuning_curve_loss.load_tuning_curve` and `tuning_curve_viz.load_curve` loaders.
The t0011 spike-time schema is `(angle_deg, trial_index, spike_time_s)` — produced and documented
in `tasks/t0011_response_visualization_library/code/tuning_curve_viz/raster_psth.py:23-25`. Emit
both schemas in t0052 so `tuning_curve_loss` and `tuning_curve_viz.plot_angle_raster_psth` work out
of the box.

### Lessons from t0046 / t0022 Reproduction Wave

[t0046] and the t0046-50 reproduction wave demonstrated that the deposited Poleg-Polsky code does
**not** implement what the paper text describes (synapse counts, GABA spatial distribution, NMDA
voltage-dependence), which is the strategic motivation for t0052. The concrete code-quality
takeaways: [t0022] hit DSI=1.0 / peak=15 Hz at the test gate but the tuning curve was a hard step
function rather than a graded cosine (HWHM=116.25 deg); [t0046] reproduced the slope-angle gates
within tolerance but had a 4x absolute PSP overshoot due to synapse-count discrepancy. For t0052,
both warn that **the per-direction firing-rate ratio is sensitive to: (a) the AMPA conductance, (b)
the inhibition modulation depth (here gabaMOD ratio 0.33:0.99 = 1:3), and (c) the bar-arrival timing
geometry**. The spec's `gNULL/gPD = 1/0.33 ~= 3` ratio in the IPSP sanity check is the explicit
verification gate.

## Reusable Code and Assets

### Import via library

* **Source**: `tasks.t0011_response_visualization_library.code.tuning_curve_viz` (registered as
  library `tuning_curve_viz`)

* **What it does**: Cartesian + polar tuning-curve plots, multi-model overlay, per-angle raster +
  PSTH

* **Reuse method**: **import via library**

* **Key entry points**:
  * `plot_cartesian_tuning_curve(curve_csv: Path, out_png: Path, *, target_csv: Path | None) -> None`
  * `plot_polar_tuning_curve(curve_csv: Path, out_png: Path, *, target_csv: Path | None) -> None`
  * `plot_angle_raster_psth(spike_times_csv: Path, out_png_pattern: str, *, angles_deg: list[float]) -> None`

* **Adaptation needed**: emit CSVs in the canonical schemas
  (`(angle_deg, trial_seed, firing_rate_hz)` for tuning curve,
  `(angle_deg, trial_index, spike_time_s)` for raster + PSTH)

* **Line count**: zero (library import only)

* **Source**: `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss` (registered as
  library `tuning_curve_loss`)

* **What it does**: DSI / peak / null / HWHM / reliability / weighted scalar loss

* **Reuse method**: **import via library**

* **Key entry points**:
  * `compute_dsi(*, curve: TuningCurve) -> float`
  * `compute_peak_hz(*, curve: TuningCurve) -> float`
  * `compute_null_hz(*, curve: TuningCurve) -> float`
  * `compute_hwhm_deg(*, curve: TuningCurve) -> float`
  * `compute_reliability(*, curve: TuningCurve) -> float | None`
  * `load_tuning_curve(csv_path: Path) -> TuningCurve`

* **Adaptation needed**: For vector-sum DSI (which the t0012 library does **not** expose; it only
  computes the primary DSI = (peak - null) / (peak + null)), implement a thin helper in
  `tasks/t0052_minimal_dsgc_scalar_gaba/code/metrics_extra.py` (~25 lines) using
  `np.sum(rate * np.exp(1j * angles)) / np.sum(rate)`.

* **Line count**: zero (library import) + ~25 lines of new vector-sum DSI helper

### Copy into task

* **Source**: `tasks/t0009_calibrate_dendritic_diameters/code/swc_io.py:1-216`

* **What it does**: SWC parser (`parse_swc_file`), structural validator (`validate_structure`),
  topology summary (`summarize`), children index (`build_children_index`), `SwcCompartment` /
  `SwcSummary` dataclasses, and SWC-type-code constants (1=soma, 3=basal-dendrite)

* **Reuse method**: **copy into task** -> `tasks/t0052_minimal_dsgc_scalar_gaba/code/swc_io.py`

* **Function signatures**:
  * `parse_swc_file(*, swc_path: Path) -> list[SwcCompartment]`
  * `validate_structure(*, compartments: list[SwcCompartment]) -> None`
  * `summarize(*, compartments: list[SwcCompartment]) -> SwcSummary`
  * `build_children_index(*, compartments: list[SwcCompartment]) -> dict[int, list[int]]`

* **Adaptation needed**: drop `write_swc_file` (t0052 doesn't write SWCs); keep parser + validator
  + children index. Update the file-header docstring's copy-attribution to cite t0009 instead of
    t0005.

* **Line count**: ~150 lines after dropping the writer

* **Source**: `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/neuron_bootstrap.py:1-58`

* **What it does**: Windows NEURON bootstrap with sentinel env-var re-exec guard

* **Reuse method**: **copy into task** ->
  `tasks/t0052_minimal_dsgc_scalar_gaba/code/neuron_bootstrap.py`

* **Function signatures**: `ensure_neuron_importable() -> None`

* **Adaptation needed**: rename sentinel `_T0046_NEURONHOME_BOOTSTRAPPED` to
  `_T0052_NEURONHOME_BOOTSTRAPPED`; import `NEURONHOME_DEFAULT` from t0052's own `paths.py`.

* **Line count**: ~57 lines verbatim

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py:104-307` (EiPair
  dataclass, `_section_midpoint`, `_compute_onset_times_ms`, `_angular_delta_deg`, `build_ei_pairs`,
  `schedule_ei_onsets`)

* **What it does**: Exp2Syn / NetStim / NetCon construction per E-I pair; bar-position-gated event
  scheduling; angular-delta math

* **Reuse method**: **copy into task** -> `tasks/t0052_minimal_dsgc_scalar_gaba/code/synapses.py`

* **Function signatures**:
  * `_compute_onset_times_ms(*, pair: EiPair, angle_deg: float, velocity_um_per_ms: float) -> tuple[float, float]`
  * `build_ei_pairs(*, h: Any, locations_xy: list[tuple[float, float]], dendrite_sections: list[Any]) -> list[EiPair]`
  * `schedule_ei_onsets(*, pairs: list[EiPair], angle_deg: float, velocity_um_per_ms: float, gaba_mod_theta: float) -> list[dict]`

* **Adaptation needed**: (a) drop the burst behaviour: `NetStim.number = 1`, no `interval`
  parameter; (b) drop the per-pair preferred/null GABA conductance switch — replace with a single
  `gaba_mod_theta` scalar applied to every pair's `gaba_netcon.weight[0]`; (c) drop the
  `EI_OFFSET_*` co-arrival logic — t0052 fires E and I at the same `t_bar` with no offset; (d)
  pair construction takes pre-sampled `(x, y)` locations, not auto-iterated section midpoints; (e)
  drop the `gaba_null_pref_ratio` argument and the `is_preferred` branching.

* **Line count**: ~150 lines after trimming

* **Source**: `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_simplerun.py:81-188`
  (recording vectors, NetCon spike detector, baseline + peak PSP extraction)

* **What it does**: trial recording skeleton (Vector recording for `_ref_v`, `_ref_t`; spike-vec via
  NetCon)

* **Reuse method**: **copy into task** -> `tasks/t0052_minimal_dsgc_scalar_gaba/code/trial.py`

* **Function signatures**:
  `run_one_trial(*, mode: TrialMode, theta_deg: float, trial_seed: int) -> TrialResult`

* **Adaptation needed**: (a) drop `h.simplerun()` invocation (no HOC procs in t0052); replace with
  `h.finitialize(V_INIT_MV); h.continuerun(TSTOP_MS)`; (b) drop `assert_bip_positions_baseline` (no
  BIP synapses); (c) drop NMDA-related logic (`b2gnmda`, `nmdaOn`, `flickerVAR`); (d) extend return
  type to carry the full V(t) trace, not just peak/baseline scalars; (e) add per-synapse
  activation-time list output for the sanity-check histogram.

* **Line count**: ~100 lines after restructuring

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py:466-530` (sweep loop
  and CSV writer)

* **What it does**: 12-angle x N-trial sweep harness with tqdm progress bar; per-angle summary
  printer; canonical-schema CSV writer

* **Reuse method**: **copy into task** ->
  `tasks/t0052_minimal_dsgc_scalar_gaba/code/run_tuning_curve.py`

* **Function signatures**:
  * `_run_sweep(*, h: Any, pairs: list[EiPair], angles_deg: tuple[float, ...], n_trials: int, label: str) -> list[TrialResult]`
  * `_write_csv(*, results: list[TrialResult], out_path: Path) -> None`
  * `_print_per_angle_summary(*, results: list[TrialResult]) -> None`

* **Adaptation needed**: switch to t0052's TrialResult shape; emit both the firing-rate CSV and a
  separate spike-times CSV (`(angle_deg, trial_index, spike_time_s)`); add the EPSP/IPSP component
  CSVs (one per (mode, angle, trial) triple).

* **Line count**: ~80 lines after adaptation

### Asset reuse

* **Source dataset**: `dsgc-baseline-morphology-calibrated` from [t0009] at
  `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`
* **What it provides**: 6,736-compartment SWC, four-tier diameter taper, 1,536.25 um total dendritic
  length
* **Reuse method**: **read SWC file directly** (datasets do not have an "import" path; resolve the
  path via t0052's own `paths.py`)
* **Adaptation needed**: none — read the SWC verbatim; do not rewrite.

## Dataset Landscape

The only project-produced dataset relevant to t0052 is `dsgc-baseline-morphology-calibrated` [t0009]
(see Asset reuse above). The earlier `dsgc-baseline-morphology` from [t0005] is superseded — its
0.125 um placeholder radii bias every downstream simulation by ~8x in surface area and ~20x in axial
resistance, per the t0009 calibration report. t0052 must consume **only** the calibrated variant.

The Poleg-Polsky vendored sources at
`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/sources/RGCmodel.hoc` are **not** consumed by
t0052; the calibrated SWC supersedes the HOC `pt3dadd` morphology entirely.

## Common Patterns

### Constants Modules and Path Centralisation

Every NEURON task in this project pairs its `code/` with a `constants.py` and a `paths.py` (see
[t0022] [t0024] [t0046]). Constants include simulation timing (`TSTOP_MS`, `DT_MS`, `CELSIUS_DEG_C`,
`V_INIT_MV`), bar geometry, synapse kinetics, and AP threshold. Paths centralise SWC / DLL / output
locations and provide `*_HOC_SAFE` variants (forward-slash-only) for HOC's `load_file` on Windows.
t0052 should follow this layout: `code/constants.py`, `code/paths.py`, `code/swc_io.py`,
`code/neuron_bootstrap.py`, `code/cell.py`, `code/synapses.py`, `code/trial.py`,
`code/run_tuning_curve.py`, `code/metrics_extra.py`, `code/render_figures.py`.

### Deterministic Per-Trial Seeds

[t0022] uses `seed = 1000 * angle_idx + trial_idx + 1`; [t0046] uses opaque `seed2` ints. t0052
should adopt the t0022 convention so seeds are reproducible from `(angle_idx, trial_idx)` alone. For
position sampling, the spec pins `seed=0` for the uniform-random dendritic location draw — keep
this **separate** from per-trial seeds so changing trial count never reshuffles synapse locations.

### One-Module-Per-Concern Splits

[t0046] has
`build_cell.py / run_simplerun.py / run_all_figures.py / compute_metrics.py / render_figures.py`;
[t0022] collapses everything into one `run_tuning_curve.py` (683 lines). Following [t0046]'s split
is the right move for t0052 because the spec asks for several distinct output products (V(t), EPSP,
IPSP, PSTH, polar curve, per-synapse activation histogram) that each deserve their own renderer.

## Lessons Learned

* **DSI=1.0 hard-step is a failure mode, not a success.** [t0022] cleared the DSI>=0.5 gate at
  DSI=1.0 / peak=15 Hz / null=0 Hz across 5 of 12 directions — but the curve was a binary step,
  not a graded cosine. The spec's gabaMOD scaling is **graded** (1 -> 3 across 180 deg) so this
  failure mode is structurally unlikely, but include the HWHM in `metrics.json` as an early warning.
* **Absolute PSP amplitudes scale with synapse count.** [t0046] reported a ~4x PSP overshoot vs
  paper attributable to using 282 synapses instead of the paper's claimed 177. t0052 fixes 100 E +
  100 I; the absolute peak firing rate is going to depend on the synapse count, so the question
  "what peak Hz at default HH densities?" cannot be answered from prior tasks — it is a genuinely
  new measurement.
* **Per-synapse activation-time histograms catch position-gating bugs.** [t0022] does not produce
  per-synapse activation histograms; the spec specifically asks for one. This is a cheap sanity
  check: assert that for a leftward bar, activation times decrease with synapse x-coordinate.
* **`apply_params` global re-application is a HOC-driven artefact.** [t0022]'s
  `_silence_baseline_hoc_synapses` had to zero `b2gampa`, `b2gnmda`, `s2ggaba`, `s2gach` and call
  HOC `update()` and `placeBIP()` to suppress the bundled HOC synapses. t0052 has no HOC and no
  bundled synapses; this whole class of pitfall does not apply.
* **NEURON Vector to numpy conversion: use `np.array(list(vec), dtype=np.float64)`.** [t0046] uses
  this pattern (`run_simplerun.py:160`). Do not use `vec.to_python()` (returns a list of Python
  floats; slower for long traces) or `np.fromiter(vec, dtype=...)` (less robust on Windows).
* **Library viz/loss are well-tested and do not need patching.** [t0011] [t0012] both ship test
  suites (`test_smoke.py`, 5 `test_*.py` files for t0012). Treat them as black-box dependencies.

## Recommendations for This Task

1. **Adopt the t0046 multi-module layout** —
   `cell.py / synapses.py / trial.py / run_tuning_curve.py / render_figures.py / metrics_extra.py`
   plus `constants.py / paths.py / swc_io.py / neuron_bootstrap.py`. Don't replicate t0022's
   monolithic 683-line run script.
2. **Copy `swc_io.py` from [t0009]** verbatim minus the SWC writer and use it as the SWC parser.
   Then write a new `cell.py:build_dsgc_from_swc(swc_path) -> CellHandles` that walks the SWC tree,
   creates one `h.Section` per non-soma compartment plus a single `soma` section made by collapsing
   the 19 soma rows, inserts `hh` on `soma + axon_initial_segment`, and inserts `pas` with
   `Rm=5999`, `Ra=100`, `cm=1.0` on every dendrite. The AIS is not present in the SWC (no axonal
   compartments); create it as a synthetic 1 um diameter x 30 um section attached to the soma
   origin.
3. **Copy `neuron_bootstrap.py` from [t0046]** verbatim (rename sentinel) — Windows bootstrap is a
   solved problem.
4. **Copy `EiPair`, `_compute_onset_times_ms`, `_section_midpoint`, `_angular_delta_deg`,
   `build_ei_pairs`, `schedule_ei_onsets` from [t0022]'s `run_tuning_curve.py:104-307`** but trim
   aggressively: `NetStim.number=1`, no E-I offset, no per-pair preferred/null branching, gabaMOD
   scalar applied uniformly to every pair's `gaba_netcon.weight[0]`.
5. **Copy the recording skeleton from [t0046]'s `run_simplerun.py:113-128`** (Vector recording +
   NetCon-based spike detection); replace `h.simplerun(exptype, dir)` with explicit
   `h.finitialize(V_INIT_MV); h.continuerun(TSTOP_MS)`.
6. **Copy the sweep harness from [t0022]'s `run_tuning_curve.py:466-530`** (12-angle x N-trial tqdm
   loop + CSV writer); extend the writer to emit both schemas (firing rate and spike times).
7. **Import `tuning_curve_viz` and `tuning_curve_loss` libraries** for plotting and metrics; do not
   reimplement DSI / HWHM / polar plotting. Add a ~25-line `metrics_extra.py` for vector-sum DSI
   which `tuning_curve_loss` does not expose.
8. **Run the AMPA-only and GABA-only EPSP/IPSP component sweeps as separate trial-runner modes**.
   Add a `TrialMode` enum with values `FULL`, `AMPA_ONLY`, `GABA_ONLY`. In `AMPA_ONLY` mode set
   every `gaba_netcon.weight[0] = 0`; in `GABA_ONLY` mode set every `ampa_netcon.weight[0] = 0`.
9. **Skip MOD compilation entirely** — t0052 needs only `Exp2Syn`, `hh`, and `pas`, all built into
   NEURON. No `nrnivmodl.cmd`, no `sources/` directory, no DLL loading.
10. **Use the `(angle_deg, trial_seed, firing_rate_hz)` and `(angle_deg, trial_index, spike_time_s)`
    CSV schemas** so library plotters and the t0012 scorer ingest the outputs directly.
11. **Reserve the IPSP-ratio sanity check** from the spec (gNULL/gPD ~= 3) as a hard-fail assertion
    in the analysis stage. Add it to `metrics.json` as a derived metric.

## Task Index

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate canonical target angle-to-AP-rate tuning curve
* **Status**: completed
* **Relevance**: Defines the canonical CSV schema `(angle_deg, trial_seed, firing_rate_hz)` that
  t0052 emits so the t0012 scorer and t0011 viz library ingest it directly.

### [t0005]

* **Task ID**: `t0005_download_dsgc_morphology`
* **Name**: Download candidate DSGC morphology
* **Status**: completed
* **Relevance**: Originator of the `dsgc-baseline-morphology` SWC. Superseded by t0009's
  diameter-calibrated variant; cited only to flag that t0052 must not consume the placeholder
  diameters.

### [t0007]

* **Task ID**: `t0007_install_neuron_netpyne`
* **Name**: Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain
* **Status**: completed
* **Relevance**: Establishes the NEURON 8.2.7 install at `C:\Users\md1avn\nrn-8.2.7` referenced by
  every Windows bootstrap. t0052 inherits the toolchain.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: Originator of the HOC-driven cell builder (`build_cell.py`) and `apply_params`
  pattern that downstream tasks layer on top of. Not directly reused by t0052 (HOC-bundled), but
  cited via t0022.

### [t0009]

* **Task ID**: `t0009_calibrate_dendritic_diameters`
* **Name**: Calibrate dendritic diameters for dsgc-baseline-morphology
* **Status**: completed
* **Relevance**: Direct dependency. Produces the `dsgc-baseline-morphology-calibrated` SWC dataset
  consumed by t0052; provides reusable `swc_io.py` SWC parser.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response-visualisation library (firing rate vs angle graphs)
* **Status**: completed
* **Relevance**: Direct dependency. Library `tuning_curve_viz` provides the per-angle Cartesian /
  polar / raster + PSTH plotters used by t0052 for output rendering.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: Direct dependency. Library `tuning_curve_loss` provides DSI / peak / null / HWHM /
  reliability / weighted scalar loss for t0052 metrics computation.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol
* **Status**: completed
* **Relevance**: Closest precedent for the per-IPSC scalar `gabaMOD` mechanism that t0052
  implements; cited as a pattern reference rather than a code source (t0020 implements gabaMOD as a
  HOC global; t0052 implements it as per-NetCon weight scaling).

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC
* **Status**: completed
* **Relevance**: Provides the `de_rosenroll_2026_dsgc` library and the `_map_tree` /
  `_terminal_midpoint` HOC-tree-walk helpers; cited as a marginal pattern reference rather than a
  reuse target since its cell construction is HOC-template-based.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC port with spatially-asymmetric inhibition for channel testbed
* **Status**: completed
* **Relevance**: Primary code-pattern source. Provides the `EiPair` dataclass, position-gated event
  scheduler, NetStim+NetCon construction, 12-angle x 10-trial sweep harness, and CSV writer that
  t0052 will copy and trim.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347) with audit
* **Status**: completed
* **Relevance**: Provides the cleanest NEURON-on-Windows bootstrap (`neuron_bootstrap.py`),
  trial-runner recording pattern, and the multi-module layout that t0052 should mirror. Also the
  source of the strategic motivation: t0046's audit revealed that the deposited code does not match
  the paper text, motivating the from-scratch t0052 build.
