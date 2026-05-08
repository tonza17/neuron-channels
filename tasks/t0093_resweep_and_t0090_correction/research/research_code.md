---
spec_version: "1"
task_id: "t0093_resweep_and_t0090_correction"
research_stage: "code"
tasks_reviewed: 7
tasks_cited: 7
libraries_found: 17
libraries_relevant: 3
date_completed: "2026-05-08"
status: "complete"
---
# Research Code: Patched-Generator 60-Morph Re-Sweep + t0090 Correction Overlay

## Task Objective

This task re-runs t0090's 60-morphology Phase D verification under the patched
`generate_fixed_morphology` shim from t0092, using the unmodified t0083 best-cell parameter vector
and the same 8-direction bar protocol (1400 ms / direction, HH on, single seed per direction). It
then issues a `replace` correction overlay against t0090's `procedural_dsgc_morphology_generator`
library asset that points downstream consumers at t0092's `procedural_dsgc_morphology_generator_fix`
[t0090] [t0092]. Pass criterion is at least 50/60 cells producing non-zero PD-rate post-fix (vs 0/60
pre-fix); the correction overlay is independent of that gate. The deliverables are a 60-row
`data/post_fix_verification_summary.json`, a `data/pre_post_delta.json`, three visualisations
(post-fix morph grid, paired pre-vs-post bar chart, transition flow), an explicit-variant
`metrics.json`, and the `corrections/library_procedural_dsgc_morphology_generator.json` overlay.

## Library Landscape

The library aggregator (`arf/scripts/aggregators/aggregate_libraries.py`) is **still not present**
in this branch — confirmed by listing `arf/scripts/aggregators/`, which shows only
`aggregate_categories.py`, `aggregate_costs.py`, `aggregate_machines.py`,
`aggregate_metric_results.py`, `aggregate_metrics.py`, `aggregate_suggestions.py`,
`aggregate_task_types.py`, and `aggregate_tasks.py`. The same gap was reported by t0092's
`research_code.md` [t0092]. The library survey was therefore performed by walking
`tasks/*/assets/library/*/details.json` directly. **17 library assets** were discovered; **3 are
directly relevant** to this task.

The framework's correction infrastructure does support `library` corrections: `target_kind`
`"library"` is listed in `arf/specifications/corrections_specification.md` (v3) and
`arf/scripts/common/artifacts.py` exports `TARGET_KIND_LIBRARY` and a `_load_library_record` path
through `paths.library_details_path`. `verify_corrections.py` validates library `replace` actions
end-to-end, including replacement-artifact existence checks. So even without
`aggregate_libraries.py`, the `replace` overlay this task writes will be visible to any future
aggregator and to all downstream skills that route library lookups through the corrections module.

| Library ID | Created by | Relevance |
| --- | --- | --- |
| `procedural_dsgc_morphology_generator` | t0090 | **Relevant** — the buggy generator. Target of the correction overlay; provides `MorphologyParams`, `MorphologyResult`, `StabilityKind`, `BEDB_BASE_POINT`, the 60 morph spec JSONs in `data/different_morphologies/` + `data/similar_morphologies/`, and the pre-fix `data/verification_summary.json` for delta diffing. |
| `procedural_dsgc_morphology_generator_fix` | t0092 | **Relevant** — the patched generator. Provides `generate_fixed_morphology` (drop-in for `generate_morphology`) and `insert_baseline_channels` (HHst+cad insertion helper extracted from t0090's verification.py). Replacement target for the correction overlay. |
| `de_rosenroll_2026_dsgc_ais_dendritic_spike` | t0080 | **Relevant** — `apply_parameter_vector`, `setup_synapses_parametric`, `run_one_trial`, `SEED_BASE`, `PD_DIRECTION_DEG`, `ND_DIRECTION_DEG`, `TSTOP_MS`, `CELSIUS_DEG_C`, `DT_MS`, `STEPS_PER_MS`, `DSGCCellWithAIS`, `ParameterVector`. Used unchanged by both t0090's `verification.py` and t0092's `post_fix_verification.py`. |
| `tuning_curve_viz` | t0011 | **Reference only** — provides `plot_polar_tuning_curve` and an Okabe-Ito palette but is firing-rate-vs-direction focused; this task's grid + paired-bar + transition-flow plots are easier to keep self-contained in `code/visualization.py` (mirroring t0090 + t0092 practice). |
| `de_rosenroll_2026_dsgc` | t0024 | Not relevant for this task — the patched generator already lifts the soma area to ~287 µm² (matching the t0024 reference), and the re-sweep imports nothing from t0024 directly. |
| `de_rosenroll_2026_dsgc_ais` | t0078 | Not relevant — superseded by t0080's v3 substrate. |
| `dsgc_active_channel_pack` | t0074 | Not relevant — independent Bed-A channel calibration line. |
| `tuning_curve_loss` | t0012 | Not relevant — scoring library, no morphology / re-sweep code. |
| `modeldb_189347_dsgc`, `modeldb_189347_dsgc_gabamod`, `modeldb_189347_dsgc_dendritic`, `modeldb_189347_dsgc_exact`, `minimal_dsgc_scalar_gaba`, `minimal_dsgc_spatial_gaba`, `minimal_dsgc_ampa_nmda_scalar_gaba`, `minimal_dsgc_mg_block_nmda`, `minimal_dsgc_tonic_gaba_sweep`, `minimal_dsgc_bar_locked_gaba_ampa_sweep` | t0008, t0020, t0022, t0046, t0052-t0059 | Not relevant — older Bed-A / minimal-DSGC lines, no procedural morphology, no t0083-vector compatibility. |

## Key Findings

### t0090's verification harness is the authoritative re-sweep template

`tasks/t0090_morphology_generator_diversity_test/code/verification.py` is the exact pipeline this
task must reproduce — only the morphology builder changes [t0090]. The driver (488 lines) walks
the 60 morph spec JSONs, builds the cell, runs a 50 ms no-stim stability check, then the 8-direction
bar protocol (1400 ms / direction at PD=0°, ND=180°, plus 45/90/135/225/270/315), and serialises
one row per cell to `data/verification_summary.json` [t0090]. Key control points:

* Module-level `_LIVE_CELLS: list[Any] = []` defends against Python GC reusing cell ids across the
  loop, which would otherwise let t0080's `_INSERTED_CELLS / _INSERTED_BASELINE_CELLS` caches skip
  channel insertion on a fresh cell [t0090].
* `_insert_baseline_channels` inserts HHst + cad on `cell.soma` + every `cell.all_dends` section and
  HHst on the two AIS subsegments. NEURON's `insert(name)` is silently idempotent so no per-cell
  cache is needed [t0090]. t0092 lifted this helper into its library as
  `insert_baseline_channels(*, h, cell)` so the re-sweep can import it instead of copying it
  [t0092].
* `_stability_check_no_stim` runs `h.run()` for `VERIFY_NO_STIM_MS = 50.0` ms at
  `VERIFY_V_INIT_MV = -70.0` mV with `h.celsius = CELSIUS_DEG_C`, `h.dt = DT_MS`, classifies the
  trace into `StabilityKind.{STABLE, NAN_VOLTAGE, DIVERGED, DISCONNECTED}` based on
  `np.isfinite(v_arr)` and `abs(peak) > VERIFY_V_NAN_THRESHOLD_MV = 1e6` [t0090].
* `_run_8direction_protocol` calls `run_one_trial(cell=, bundle=, direction_deg=, seed=)` for each
  angle with seed `SEED_BASE + int(angle) * 13`, returning `dict[float, int]` of spike counts per
  angle [t0090].
* The trial seed for `_run_8direction_protocol` is `SEED_BASE + int(params.morph_seed)`. This is the
  seed pattern this task must match for comparable results. The placer seed is
  `SEED_BASE + (int(hash(default_params.values.tobytes())) & 0xFFFF)` [t0090].

### Row schema in data/verification_summary.json

The 60-row JSON format produced by `_to_dict(r=...)` in `verification.py` is [t0090]:

```python
{
    "morph_id": str,                # e.g. "morph_00"
    "population": str,              # "different" or "similar"
    "morph_index": int,             # 0..29 within the population
    "stability_flag": str,          # StabilityKind value
    "dsi": float | None,
    "pd_rate_hz": float | None,
    "nd_rate_hz": float | None,
    "peak_vm_mv": float | None,
    "n_dendrites": int,
    "n_terminals": int,
    "elapsed_s": float,
    "error": str | None,
    "per_direction_spikes": dict[str, int],  # angle string -> spike count
}
```

The first row of `tasks/t0090_morphology_generator_diversity_test/data/verification_summary.json`
confirms the schema:
`morph_00 / different / morph_index=0 / stability_flag="stable" / dsi=0.0 / pd_rate_hz=0.0 / per_direction_spikes={"0.0": 0, ..., "315.0": 0}`
(8 angle keys). The phase-A output of this task should reuse this schema verbatim and add two
columns — `pre_fix_stability_flag` and `pre_fix_spike_count_total` — copied from t0090 for
downstream diffing [t0090].

### t0092's morphology_generator_fix is a drop-in shim

`tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`
has signature `(*, params: MorphologyParams, morph_seed: int | None = None) -> MorphologyResult`,
which is **structurally identical** to t0090's
`tasks.t0090_morphology_generator_diversity_test.code.generator.generate_morphology` [t0092]. The
fix is purely post-hoc: it calls the unmodified t0090 `generate_morphology`, then re-emits the
soma's two `pt3dadd` points along the z-axis with diameter chosen so
`pi * d_target * soma_diameter_um = BEDB_AREA_TARGET_UM2 = 220.0 µm²` [t0092]. Determinism is
preserved: same `(params, morph_seed)` -> identical output across two calls. Replacing the import in
`verification.py:64-66` with this fix is the **only** code change the re-sweep driver needs.

### Validation gate: t0092's BedB + 5-cell evidence

t0092's results show the patch fully recovers the BedB-equivalent (PD=43.6 Hz, DSI=0.034) and **5/5
STABLE-from-t0090 cells** (`different/morph_00`, `13`, `14`, `15`, `19`) under the t0083 vector
[t0092]. Standout cells: morph_14 reaches PD-rate 36.4 Hz / DSI 0.962, morph_13 reaches DSI 1.00
(PD-only spikes), morph_19 reaches DSI 0.21 [t0092]. This sets the prior for the re-sweep: the
9-cell STABLE bucket from t0090 is expected to fire post-fix. The 51-cell NAN_VOLTAGE bucket is
where the new evidence sits — recovery of those is the headline outcome. The plan's validation
gate (re-run on the first 5 morphologies before scaling) directly reuses t0092's signal: at least
4/5 should reach STABLE.

### Pre-fix stability distribution to diff against

t0090's pre-fix `verification_summary.json` reports **9 STABLE** (6 different + 3 similar) and **51
NAN_VOLTAGE** (24 different + 27 similar) [t0090]. All 9 STABLE cells have
`dsi=0.0, pd_rate_hz=0.0, peak_vm_mv=-70.0` and `per_direction_spikes` all-zero —
STABLE-but-silent. The NAN_VOLTAGE rows have `dsi/pd_rate_hz/nd_rate_hz/peak_vm_mv = null`,
`per_direction_spikes = {}`, and `elapsed_s ~ 0.5-1.0 s` (early termination) [t0090]. The pass
criterion (≥50/60 cells with `pd_rate_hz > 0` post-fix) requires recovering at least 50 of these
60 cells, vs the **0/60 pre-fix** firing baseline.

### t0083 best-cell parameter vector loader

`tasks.t0090_morphology_generator_diversity_test.code.load_default_params.load_t0083_best_cell_param_vector(*, path: Path = T0083_PARETO_FRONT_JSON) -> ParameterVector`
walks the t0083 Pareto front JSON, filters to `is_feasible=True and not is_unstable`, picks the
highest-DSI cell, and returns a 54-d `ParameterVector` [t0090] [t0083]. This is the canonical loader
that t0092 also reuses [t0092]. The re-sweep imports it unchanged.

### ProcessPoolExecutor parallelism pattern

t0090's `run_verification` accepts `--max-workers`, with 1 = sequential and N = process pool
[t0090]. The pickleable worker is a top-level
`_worker_verify(*, morph_path_str: str, default_params_values: NDArray[np.float64], population: str, morph_index: int) -> dict[str, Any]`
[t0090]. It loads the morph JSON, builds + verifies one cell, and returns the result dict. Results
are sorted `(population, morph_index)` after collection for deterministic JSON output [t0090]. The
plan calls for 64-core EPYC parallelism (~30 min wall-clock); single-process serial is the listed
fallback for any Windows-side ProcessPool DLL pain (~5 hours).

### Corrections specification: library replace shape

`arf/specifications/corrections_specification.md` (v3) defines library replacement as a `replace`
action with `changes` containing `replacement_task` and `replacement_id`, and **no** `file_changes`
[corrections-spec]. The required envelope is:

```json
{
  "spec_version": "3",
  "correction_id": "C-0093-01",
  "correcting_task": "t0093_resweep_and_t0090_correction",
  "target_task": "t0090_morphology_generator_diversity_test",
  "target_kind": "library",
  "target_id": "procedural_dsgc_morphology_generator",
  "action": "replace",
  "changes": {
    "replacement_task": "t0092_diagnose_morphology_generator_silence",
    "replacement_id": "procedural_dsgc_morphology_generator_fix"
  },
  "rationale": "..."
}
```

The filename must be `library_<target_id>.json` per the spec, so the file lives at
`tasks/t0093_resweep_and_t0090_correction/corrections/library_procedural_dsgc_morphology_generator.json`.
`correcting_task` must match the containing folder name **exactly** — i.e. the literal task slug
`t0093_resweep_and_t0090_correction`, not the longer label that appears in some plan / suggestion
texts. The replacement must be the same `target_kind`. `verify_corrections.py` checks: required
fields, `correction_id` regex `^C-\d{4}-\d{2}$`, the `correcting_task=folder` invariant, target
exists, kind/action valid, replacement artifact exists, no cycles, filename matches
`<target_kind>_<target_id>.json`, rationale ≥10 chars [corrections-spec]. The example in the spec
itself is a library replacement (`C-0042-04`), confirming the action is fully supported.

### Visualisation: stay self-contained

t0090's `code/visualization.py` (172 lines) builds 5x6 morph grids via
`make_grid_panel(*, morph_jsons: list[Path], output_png: Path, title: str, line_color: str)` using
`plot_dendrogram(*, cell, ax, color, line_width_scale=0.8)` with `LineCollection`-backed dendrite
segments and an Okabe-Ito-inspired palette inlined as `OKABE_ITO_PALETTE` [t0090]. The grid layout
is `GRID_NCOLS=6, GRID_NROWS=5`, `figsize=(GRID_NCOLS*2.4, GRID_NROWS*2.4)`. t0092's
`post_fix_verification.py` builds polar tuning panels with `matplotlib.use("Agg")` for headless
rendering and `plt.subplots(..., subplot_kw={"projection": "polar"})` [t0092]. The
`tuning_curve_viz` library [t0011] exposes
`plot_polar_tuning_curve(curve_csv, out_png, *, target_csv=None)` but it works off CSVs and a
single-cell tuning curve, not the morphology grid / paired-bar / transition-flow plots this task
needs. The pragmatic choice — and the pattern both t0090 and t0092 chose — is to write the three
plots inline in `code/visualization.py` using matplotlib directly, copying t0090's grid scaffolding
and adding a colour overlay keyed on post-fix `stability_flag`.

### Metrics: explicit-variant format with the registered DSI metric

`meta/metrics/direction_selectivity_index/description.json` registers `direction_selectivity_index`
as a unitless float (`unit: "ratio"`) [meta-metrics]. t0092's `results/metrics.json` is a clean
reference for the explicit-variant shape: a top-level `{"variants": [...]}` object where each
variant has `variant_id`, `label`, a `dimensions` map (e.g.
`{"morphology": "...", "channels": "..."}`), and a `metrics` map keyed only by registered metric
names [t0092]. Null is the canonical "not measured" value (t0092 used it for the pre-fix variant
where every trial NaN'd out). This task's `results/metrics.json` should declare
`different_set_post_fix` and `similar_set_post_fix` variants with mean-DSI-over-STABLE-and-firing
cells (or null if none).

## Reusable Code and Assets

### Import via library (cross-task imports allowed)

#### `generate_fixed_morphology` from t0092

* **Source**:
  `tasks/t0092_diagnose_morphology_generator_silence/assets/library/procedural_dsgc_morphology_generator_fix/`
* **Module**: `tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py`
* **What it does**: Builds a procedural DSGC cell with the soma-pt3d collapse patched by re-emitting
  two pt3d points along the z-axis. Drop-in for t0090's `generate_morphology`.
* **Reuse method**: **import via library**.
* **Signature**:
  `def generate_fixed_morphology(*, params: MorphologyParams, morph_seed: int | None = None) -> MorphologyResult`
* **Adaptation needed**: None. Replace the import in the re-sweep driver:
  `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.
* **Line count**: 99 lines (the shim itself).

#### `insert_baseline_channels` from t0092

* **Source**:
  `tasks/t0092_diagnose_morphology_generator_silence/assets/library/procedural_dsgc_morphology_generator_fix/`
* **Module**: `tasks/t0092_diagnose_morphology_generator_silence/code/baseline_channels.py`
* **What it does**: Inserts HHst + cad on soma + every dendrite + AIS of one cell. Idempotent.
* **Reuse method**: **import via library**.
* **Signature**: `def insert_baseline_channels(*, h: Any, cell: Any) -> None`
* **Adaptation needed**: None. Replaces the inline `_insert_baseline_channels` in t0090's
  verification.py.
* **Line count**: 34 lines.

#### `MorphologyParams`, `MorphologyResult`, `StabilityKind`, `BEDB_BASE_POINT`, `PARAM_BOUNDS` from t0090

* **Source**:
  `tasks/t0090_morphology_generator_diversity_test/assets/library/procedural_dsgc_morphology_generator/`
* **Modules**: `code/morphology_params.py`, `code/constants.py`
* **What they do**: Frozen dataclass for the 14-knob morphology spec, the result wrapper duck-typed
  as `DSGCCellWithAIS`, the four-state stability enum, and the BedB base point + bounds.
* **Reuse method**: **import via library**.
* **Adaptation needed**: None.
* **Line count**: ~140 lines (params dataclass) + ~190 lines (constants).

#### `apply_parameter_vector`, `setup_synapses_parametric`, `run_one_trial`, `SEED_BASE`, `PD_DIRECTION_DEG`, `ND_DIRECTION_DEG`, `TSTOP_MS`, `CELSIUS_DEG_C`, `DT_MS`, `STEPS_PER_MS`, `DSGCCellWithAIS`, `ParameterVector` from t0080

* **Source**:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/library/de_rosenroll_2026_dsgc_ais_dendritic_spike/`

* **Modules**: `code/apply_params.py`, `code/trial_helpers.py`, `code/trial_driver.py`,
  `code/build_cell_ais.py`, `code/constants.py`

* **What they do**: Apply the 54-d parameter vector to a procedurally built cell, place parametric
  AMPA + NMDA + GABA synapses with their bar arrival times, run one 1400 ms trial at one direction,
  and provide the reusable cell type + 8-direction protocol constants.

* **Reuse method**: **import via library** — exactly as both t0090's verification.py and t0092's
  post_fix_verification.py already do.

* **Signatures of the three callables**:

  ```python
  def apply_parameter_vector(*, cell: DSGCCellWithAIS, params: ParameterVector) -> None: ...

  def setup_synapses_parametric(
      *,
      cell: DSGCCellWithAIS,
      n_ach: int, n_gaba: int,
      rho_0_ach: float, lambda_ach_um: float,
      rho_0_gaba: float, lambda_gaba_um: float,
      w_ach_us: float, w_gaba_us: float,
      placer_seed: int,
      gnmda_dend: float, mg_conc_mm: float, voff_nmda: float,
  ) -> SynapseBundle: ...

  def run_one_trial(
      *, cell: DSGCCellWithAIS, bundle: SynapseBundle,
      direction_deg: float, seed: int,
  ) -> TrialResult: ...
  ```

* **Adaptation needed**: None.

#### `load_t0083_best_cell_param_vector` from t0090

* **Source**:
  `tasks/t0090_morphology_generator_diversity_test/assets/library/procedural_dsgc_morphology_generator/`
* **Module**: `tasks/t0090_morphology_generator_diversity_test/code/load_default_params.py`
* **What it does**: Reads t0083's Pareto front JSON, filters to feasible-and-stable, returns the
  highest-DSI cell as a 54-d `ParameterVector`.
* **Reuse method**: **import via library**.
* **Signature**:
  `def load_t0083_best_cell_param_vector(*, path: Path = T0083_PARETO_FRONT_JSON) -> ParameterVector`
* **Adaptation needed**: None. Library re-exports `T0083_PARETO_FRONT_JSON` via its `paths.py`.
* **Line count**: ~58 lines.

### Copy into task

#### Re-sweep driver `code/resweep_driver.py`

* **Source**: `tasks/t0090_morphology_generator_diversity_test/code/verification.py`
* **What to copy**: ~330 lines of the verification harness — `VerificationResult` dataclass,
  `_to_dict`, `_LIVE_CELLS` defense, `_stability_check_no_stim`, `_run_8direction_protocol`,
  `verify_one_morphology`, `_worker_verify`, `collect_morph_paths`, `run_verification`, `main`. Drop
  the in-file `_insert_baseline_channels` (now imported from t0092's library).
* **Reuse method**: **copy into task** (cross-task code imports are forbidden by ARF rule;
  `verification.py` is task-internal in t0090, not exposed as a library entry point).
* **Adaptation needed**:
  * Replace `from tasks.t0090_..code.generator import generate_morphology` with
    `from tasks.t0092_..code.morphology_generator_fix import generate_fixed_morphology`, and rename
    the call site `cell = generate_fixed_morphology(...)`.
  * Replace the inline `_insert_baseline_channels(cell=cell)` with
    `insert_baseline_channels(h=cell.h, cell=cell)` imported from t0092.
  * Add two extra columns to `_to_dict` and `VerificationResult`: `pre_fix_stability_flag: str`,
    `pre_fix_spike_count_total: int`, populated from t0090's `verification_summary.json` lookup
    keyed on `(population, morph_id)`.
  * Wire output to a t0093-local
    `DATA_POST_FIX_VERIFICATION_JSON = TASK_ROOT / "data" / "post_fix_verification_summary.json"`
    defined in `code/paths.py`.
* **Line count**: ~330 lines copied + ~30 lines of pre-fix-lookup glue.

#### Delta analysis `code/delta_analysis.py`

* **Source**: New code with no direct prior. Closest analogue is the `_summarise_stability` /
  metrics-aggregation pattern in t0090's `verification.py:run_verification` (~10 lines).
* **What it does**: Reads the pre-fix `tasks/t0090_..data/verification_summary.json` and the new
  `data/post_fix_verification_summary.json`, computes per-cell `transition_label` (e.g.
  `nan_to_stable_firing`, `stable_silent_to_stable_firing`, `unchanged_nan`,
  `regression_stable_to_nan`) and aggregate counts, writes `data/pre_post_delta.json`.
* **Reuse method**: **copy into task** (new module).
* **Line count**: ~120 lines.

#### Visualisations `code/visualization.py`

* **Source**: `tasks/t0090_morphology_generator_diversity_test/code/visualization.py` (lines 1-172).
* **What to copy**: `plot_dendrogram`, `_line_segments_for_cell`, `OKABE_ITO_PALETTE`,
  `make_grid_panel`, `matplotlib.use("Agg")` headless setup, the GRID_NCOLS=6 / GRID_NROWS=5 layout.
* **Reuse method**: **copy into task** (visualisation code is task-internal in t0090).
* **Adaptation needed**:
  * Replace `generate_morphology` import with `generate_fixed_morphology`.
  * Add per-cell colour mapping keyed on post-fix stability_flag in
    `{stable_firing, stable_silent, nan_voltage, diverged, disconnected}`.
  * Add a paired-bar plot (`pre_vs_post_spike_counts.png`): two bars per cell, sorted by post-fix
    spike count descending, pre-fix red, post-fix green; uses
    `matplotlib.pyplot.bar(x - 0.2, pre, width=0.4)` + `bar(x + 0.2, post, width=0.4)`.
  * Add a transition flow plot (`transition_sankey.png`) — a stacked bar with two columns (pre /
    post) and segments coloured by stability_flag; the plan accepts a stacked bar fallback if Sankey
    is too heavy. Use vanilla matplotlib stacked-bar; no `plotly` or `holoviews` dependency.
* **Line count**: ~250 lines (170 reused + ~80 new for the bar + flow charts).

#### Paths module `code/paths.py`

* **Source**: `tasks/t0090_morphology_generator_diversity_test/code/paths.py` (78 lines).
* **What to copy**: The `TASK_ROOT`, `DATA_DIR`, `RESULTS_DIR`, `RESULTS_IMAGES_DIR`, `ASSETS_DIR`,
  `ensure_directories()` skeleton.
* **Reuse method**: **copy into task** — paths are inherently task-local.
* **Adaptation needed**: Drop t0090-specific paths (`DATA_DIFFERENT_DIR`, `DATA_VERIFICATION_JSON`,
  `DATA_BEDB_REPRO_JSON`, `DATA_G1/G2/G3*`); add t0093-local paths:
  * `DATA_POST_FIX_VERIFICATION_JSON = DATA_DIR / "post_fix_verification_summary.json"`
  * `DATA_PRE_POST_DELTA_JSON = DATA_DIR / "pre_post_delta.json"`
  * Cross-task references:
    `T0090_VERIFICATION_JSON = REPO_ROOT / "tasks" / "t0090_morphology_generator_diversity_test" / "data" / "verification_summary.json"`,
    `T0090_DIFFERENT_DIR`, `T0090_SIMILAR_DIR`.
  * Image outputs: `POST_FIX_GRID_PNG`, `PRE_VS_POST_BAR_PNG`, `TRANSITION_FLOW_PNG`.
* **Line count**: ~80 lines.

#### Metrics writer `code/write_metrics.py`

* **Source**: `tasks/t0092_diagnose_morphology_generator_silence/code/post_fix_verification.py` (the
  `_write_metrics_json` block, ~30 lines).
* **What it does**: Reads the post-fix summary, computes mean DSI per population over
  STABLE-and-firing cells (or null if none), serialises to the explicit-variant `metrics.json` shape
  with `different_set_post_fix` and `similar_set_post_fix` variants.
* **Reuse method**: **copy into task** (small inline writer, not a library entry point).
* **Adaptation needed**: Two variants instead of t0092's pre-fix / post-fix pair; aggregate over
  population subsets instead of single cells.
* **Line count**: ~80 lines.

### Pre-fix data to read

* `tasks/t0090_morphology_generator_diversity_test/data/verification_summary.json` — 60 rows; the
  pre-fix baseline for the delta analysis. Schema given in Key Findings above. Read-only; treated as
  upstream input.
* `tasks/t0090_morphology_generator_diversity_test/data/different_morphologies/morph_00.json`
  through `morph_29.json` — 30 morph spec JSONs (the `MorphologyParams` payloads).
* `tasks/t0090_morphology_generator_diversity_test/data/similar_morphologies/morph_00.json` through
  `morph_29.json` — 30 more morph spec JSONs.
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json` — t0083 Pareto front;
  loaded via `load_t0083_best_cell_param_vector` to obtain the unmodified best-cell 54-d vector.

## Lessons Learned

### Patches via thin shim libraries are the right move

t0092's decision to ship a shim library (`procedural_dsgc_morphology_generator_fix`) instead of a
forked generator dramatically simplifies this task: the only code change in the re-sweep driver is a
one-line import swap, and the correction overlay is a pure metadata redirect [t0092]. This was worth
the small overhead of registering a second library asset because it preserves diff-clean debugging
— every other line of `verify_one_morphology` stays identical, which is what makes the
side-by-side delta analysis cleanly attributable to the soma-area patch and nothing else [t0092].

### Process pool pitfalls on Windows

t0090's plan assumes a 64-core EPYC; this task's plan inherits that assumption but lists "single-
process serial fallback" as a Risk row [t0093-plan]. Per-worker NEURON DLL load cost on Windows can
make `ProcessPoolExecutor` net-negative for small batches. The mitigation is already in t0090's
driver: `--max-workers 1` reproduces the sequential path bit-for-bit and `--max-workers 0`
auto-detects `cpu_count() - 1`. The plan's validation gate (`--limit 5`) is also a useful proxy for
early failure detection on the parallelism path.

### Non-zero stable cells with zero spikes are real

t0090's pre-fix data has 9 STABLE rows with `dsi=0.0, peak_vm_mv=-70.0, per_direction_spikes` all
zero [t0090]. These are not bugs — they are the morphologies whose AP threshold is never crossed
by the t0083-vector synaptic input on the unpatched soma. The delta analysis must distinguish
`stable_silent_to_stable_firing` (recovery) from `unchanged_stable_silent` (not affected by the
patch). Both transitions are informative; the plan's pass criterion (≥50/60 cells with
`pd_rate_hz > 0`) lumps them with the NAN_VOLTAGE recoveries which is fine for the headline number,
but the `transition_label` taxonomy in `pre_post_delta.json` should be granular enough to attribute
each one [t0093-plan].

### Acceptable-negative branch

The plan explicitly decouples the correction overlay from the pass-criterion outcome: even if fewer
than 50/60 cells fire post-fix, the correction is issued because t0091 needs the patched generator
regardless [t0093-plan]. This is a deliberate design choice — the project-level fact ("the patched
generator is the canonical procedural DSGC morphology generator") is independent of how many of
t0090's specific 60 cells the patch happens to recover. Implementation should mirror this
independence: write the correction file as soon as Phase D completes, not gated on Phase B's delta
counts.

### Aggregator-vs-walker awareness for libraries

t0092 already noted the missing `aggregate_libraries.py` and walked `tasks/*/assets/library/`
directly [t0092]. Same pattern applies here — but the correction overlay this task writes is still
a load-bearing artifact for downstream skills, because `verify_corrections.py` validates it,
`arf/scripts/common/artifacts.py` exposes library lookup through correction-aware code paths, and
any future `aggregate_libraries.py` will pick it up automatically. ARF rule 9 ("always use
aggregators to enumerate cross-task data") is satisfied for the kinds that *do* have aggregators
(tasks, suggestions, costs, machines, metric_results). For libraries, walking is the only option in
this branch and is acceptable as long as the survey is complete and documented.

### Metrics: only registered keys

`verify_task_metrics.py` (which this task's plan calls out as a verification gate) checks that every
key under each variant's `metrics` map is registered in `meta/metrics/` [t0093-plan][meta-metrics].
The four registered keys in this branch are `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
`tuning_curve_reliability`, `tuning_curve_rmse`; only the first applies to this task's two variants.
Adding ad-hoc keys like `pd_rate_hz_mean` would fail the verifier; those summaries belong in
`results_detailed.md`, not `metrics.json`.

## Recommendations for This Task

1. **Reuse t0090's `verification.py` as the structural skeleton for `code/resweep_driver.py`.** Copy
   ~330 lines, change exactly two imports (`generate_fixed_morphology`, `insert_baseline_channels`),
   add two pre-fix-lookup columns to the row schema, and route output through
   `code/paths.py:DATA_POST_FIX_VERIFICATION_JSON`. Do not refactor — the diff-clean reuse is the
   point.

2. **Import t0092's library as the only generator the driver knows about.** Do not import
   `tasks.t0090_..code.generator.generate_morphology` anywhere in this task. Consumers should see a
   single canonical entry point. The `_LIVE_CELLS` defense, the placer-seed pattern
   (`SEED_BASE + (hash(default_params.values.tobytes()) & 0xFFFF)`), and the angle-seed pattern
   (`SEED_BASE + int(angle) * 13`) all carry over verbatim.

3. **Run the validation gate first, every time.** `--limit 5 --max-workers 1` reproduces the first 5
   morphologies sequentially; expectation per the plan is at least 4/5 STABLE (vs t0090's 0/5)
   [t0093-plan]. If the small run reproduces NAN_VOLTAGE, the patch is not being applied — halt
   and inspect `cell.soma.L` after `generate_fixed_morphology`, which should be `~15 µm` not
   `~1e-9 µm` [t0092].

4. **Write `code/delta_analysis.py` as a standalone module that consumes both summary JSONs.** The
   mapping key is `(population, morph_id)`; the per-cell diff produces one of these
   `transition_label` values: `nan_to_stable_firing`, `nan_to_stable_silent`, `unchanged_nan`,
   `unchanged_stable_silent`, `stable_silent_to_stable_firing`, `regression_stable_to_nan`,
   `regression_stable_to_diverged`, `unchanged_diverged`, `unchanged_disconnected`. Aggregate counts
   go in the same JSON.

5. **Stay self-contained on visualisations.** Reuse t0090's `make_grid_panel` and `plot_dendrogram`
   verbatim; add a `stability_flag -> color` map for the 5x6 grid panel variants. Write the
   paired-bar and transition-flow plots inline using vanilla matplotlib — no `holoviews` or
   `plotly`. Headless rendering via `matplotlib.use("Agg")` is mandatory on Windows / headless EPYC
   alike [t0090].

6. **Issue the correction overlay regardless of Phase B outcome.** Write
   `corrections/library_procedural_dsgc_morphology_generator.json` with
   `correction_id = "C-0093-01"`, `target_kind = "library"`, `action = "replace"`, and a `changes`
   block pointing at the t0092 library. Run
   `verify_corrections.py t0093_resweep_and_t0090_correction` and ensure it passes
   [corrections-spec].

7. **Use t0092's `metrics.json` as the explicit-variant template.** Two variants:
   `different_set_post_fix` and `similar_set_post_fix`. Single registered key per variant:
   `direction_selectivity_index`, computed as the mean over STABLE-and-firing cells in that
   population (null if none) [meta-metrics][t0092].

8. **Aggregate counts in `pre_post_delta.json` should beat the `pd_rate_hz > 0` pass criterion
   without restating it.** Specifically: total cells with `post_pd_rate_hz > 0`, total cells with
   `post_stability_flag == "stable"`, the 9-cell STABLE-firing recovery count from t0090's pre-fix
   STABLE bucket, and the 51-cell NAN_VOLTAGE recovery count.

9. **Do not refine `BEDB_BASE_POINT` or chase the synapse-XY symmetry residual** — those are out
   of scope per the task description (S-0092-02, S-0092-04 follow-ups) [t0093-plan]. The patch from
   t0092 is the only generator change; everything else is data analysis + correction overlay.

10. **Document the library walker as a known gap.** Note in `results_detailed.md` that the
    correction is written and verified, but that downstream consumers won't *see* the corrected
    canonical library until either (a) `aggregate_libraries.py` lands, or (b) consumers route
    library lookups through `arf/scripts/common/artifacts.py` (which already understands library
    `replace` corrections via `_load_library_record`).

## Task Index

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response visualization library
* **Status**: completed
* **Relevance**: Source of the `tuning_curve_viz` library (`plot_polar_tuning_curve`,
  `plot_cartesian_tuning_curve`, `plot_multi_model_overlay`, Okabe-Ito palette). Reference only —
  this task's plots (morph grid, paired bar, transition flow) do not match the library's
  CSV-input/single-cell-tuning shape, so the visualisations are written inline mirroring t0090 +
  t0092 practice.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: BedB MOBO v3 dendritic-spike NSGA-II
* **Status**: completed
* **Relevance**: Source of the `de_rosenroll_2026_dsgc_ais_dendritic_spike` library used unchanged
  by the re-sweep driver: `apply_parameter_vector`, `setup_synapses_parametric`, `run_one_trial`,
  `DSGCCellWithAIS`, `ParameterVector`, and the protocol constants `SEED_BASE`, `PD_DIRECTION_DEG`,
  `ND_DIRECTION_DEG`, `TSTOP_MS`, `CELSIUS_DEG_C`, `DT_MS`, `STEPS_PER_MS`.

### [t0083]

* **Task ID**: `t0083_bedb_v3_extend_nsga2_gen8plus`
* **Name**: BedB v3 NSGA-II extension to gen 8+
* **Status**: completed
* **Relevance**: Owns `results/data/pareto_front.json`, the Pareto front from which
  `load_t0083_best_cell_param_vector` selects the highest-DSI feasible-and-stable cell. That 54-d
  vector is applied unchanged to every one of the 60 morphologies in this task's re-sweep.

### [t0086]

* **Task ID**: `t0086_robustness_cluster_bio_comparison`
* **Name**: Robustness cluster bio-comparison
* **Status**: completed
* **Relevance**: Cited indirectly via the task description as a downstream consumer (cluster
  re-score work) that benefits from this task's correction overlay so it picks up the patched
  generator. No code is imported from t0086.

### [t0088]

* **Task ID**: `t0088_recluster_marginals_and_vm_motifs`
* **Name**: Re-cluster t0086 marginals + Vm-motif deep-dive
* **Status**: completed
* **Relevance**: Cited as another downstream consumer alongside t0091 — its representative-cells
  JSON is referenced via t0090's `paths.py` (`T0088_REPRESENTATIVE_CELLS_JSON`) but is not loaded in
  this task's re-sweep. Listed for traceability of the correction's downstream impact.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Procedural DSGC morphology generator + diversity test + validation bundle
* **Status**: completed
* **Relevance**: **Target of the correction overlay** and the source of the verification harness,
  the 60 morph spec JSONs in `data/different_morphologies/` + `data/similar_morphologies/`, the
  pre-fix `verification_summary.json`, the `MorphologyParams` / `MorphologyResult` / `StabilityKind`
  types, the `BEDB_BASE_POINT` constant, the `load_t0083_best_cell_param_vector` helper, and the
  `make_grid_panel` / `plot_dendrogram` visualisation primitives. Most reused task in this research.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose t0090 procedural-cell silence
* **Status**: completed
* **Relevance**: Source of `procedural_dsgc_morphology_generator_fix` — the patched
  `generate_fixed_morphology` shim (drop-in for t0090's `generate_morphology`) and the
  `insert_baseline_channels` helper. Both are imported via library and form the only generator this
  task's re-sweep driver knows about. Also the source of the explicit-variant `metrics.json`
  template, the validation evidence (5/5 STABLE-from-t0090 cells fire post-fix; BedB-equivalent
  reaches PD-rate 43.6 Hz / DSI 0.034), and the diagnosis the correction's `rationale` cites.
