---
spec_version: "2"
task_id: "t0093_resweep_and_t0090_correction"
date_completed: "2026-05-08"
status: "complete"
---
# Plan: Patched-generator full 60-morph re-sweep + t0090 correction overlay

## Objective

Re-run task t0090's full 60-morphology Phase D verification under the patched
`generate_fixed_morphology` shim shipped by t0092 and the unmodified t0083 best-cell parameter
vector, then issue a `replace` correction overlay against t0090's
`procedural_dsgc_morphology_generator` library asset that points downstream consumers at t0092's
`procedural_dsgc_morphology_generator_fix`. The re-sweep must close the gap left by t0092 (which
only validated 1 BedB-equivalent + 5 of t0090's 9 STABLE cells) by exercising the remaining 51
NAN_VOLTAGE cells and the 4 untested STABLE cells under the patch.

The task is "done" when:

* `data/post_fix_verification_summary.json` exists with 60 entries (30 different + 30 similar)
  matching t0090's row schema plus pre-fix-comparison columns
* At least 50/60 cells have `pd_rate_hz > 0` post-fix (pass criterion); stretch goal 55/60
* `data/pre_post_delta.json` reports per-cell `transition_label` and aggregate counts
* Three charts exist under `results/images/`: morphology grid coloured by post-fix flag, paired
  pre-vs-post spike-count bar chart, transition-flow stacked bar
* `corrections/library_procedural_dsgc_morphology_generator.json` exists, `verify_corrections.py`
  passes with zero errors
* `results/metrics.json` is in explicit-variant format with `different_set_post_fix` and
  `similar_set_post_fix` variants, each carrying only the registered `direction_selectivity_index`
  key
* All quality gates (ruff, mypy, verify_task_metrics, verify_task_results, verify_logs,
  verify_task_folder, verify_task_file) PASS with zero errors

## Task Requirement Checklist

The operative task request from `task.json` and `task_description.md` (verbatim):

> Re-run t0090's 60-morph Phase D verification under the t0092 patched generator; issue correction
> overlay marking t0090's procedural_dsgc_morphology_generator as superseded by t0092's
> procedural_dsgc_morphology_generator_fix.

> Re-run the t0090 60-morphology Phase D verification (30 different + 30 similar) under the patched
> `generate_fixed_morphology` from t0092, with the unmodified t0083 best-cell parameter vector and
> the same 8-direction bar protocol (1400 ms / direction, HH on, single seed per direction matching
> t0090's protocol). [...] Issue a `replace` correction overlay against t0090's
> `procedural_dsgc_morphology_generator` library asset pointing consumers at t0092's
> `procedural_dsgc_morphology_generator_fix`. Verify the corrections-aware aggregator output
> reflects the supersession. Document the registered metric `direction_selectivity_index` per
> population (`different_set_post_fix`, `similar_set_post_fix`) in the explicit-variant
> `metrics.json`.

Concrete requirements decomposed into stable IDs:

* **REQ-1**: Produce `data/post_fix_verification_summary.json` with 60 entries (30 different + 30
  similar) matching t0090's row schema plus `pre_fix_stability_flag` and `pre_fix_spike_count_total`
  columns. Satisfied by Step 4. Evidence: file exists with 60 rows; schema matches t0090's
  `_to_dict` keys.
* **REQ-2**: At least 50/60 cells produce non-zero PD-rate post-fix (pass criterion); record stretch
  result against 55/60. Satisfied by Step 5. Evidence: aggregate counts in `pre_post_delta.json`
  field `cells_with_nonzero_pd_rate`.
* **REQ-3**: Use the unmodified t0083 best-cell parameter vector (loaded via
  `load_t0083_best_cell_param_vector`). Satisfied by Step 4. Evidence: Step 4 loads vector once and
  applies it to every morphology; logged in step output.
* **REQ-4**: Use the same 8-direction bar protocol as t0090 (1400 ms / direction, HH on, single
  trial seed per direction = `SEED_BASE + int(angle) * 13`). Satisfied by Step 4. Evidence:
  `_run_8direction_protocol` copied verbatim from t0090; per-direction spike counts in JSON.
* **REQ-5**: Produce `data/pre_post_delta.json` with per-cell `transition_label` and aggregate
  counts. Satisfied by Step 5. Evidence: file exists with one entry per cell + an aggregate block.
* **REQ-6**: Produce three visualisations: post-fix morphology grid coloured by stability flag,
  paired pre-vs-post spike-count bar chart, transition flow chart. Satisfied by Step 6. Evidence:
  three PNG files under `results/images/`.
* **REQ-7**: Issue a `replace` correction overlay against t0090's
  `procedural_dsgc_morphology_generator` pointing at t0092's
  `procedural_dsgc_morphology_generator_fix`. Satisfied by Step 7. Evidence:
  `corrections/library_procedural_dsgc_morphology_generator.json` exists with the required envelope;
  `verify_corrections.py` exits 0.
* **REQ-8**: Verify the corrections-aware aggregator output reflects the supersession. Satisfied by
  Step 8. Evidence: in this branch `aggregate_libraries.py` is not present; per the research
  consensus, library lookups go through `arf.scripts.common.artifacts._load_library_record`, which
  honours `replace` corrections. Step 8 invokes that code path directly and records the result in
  `data/library_supersession_check.json`. The plan adopts the literal evidence string "library
  aggregator not present in branch — verified via arf.scripts.common.artifacts directly" in the
  output JSON.
* **REQ-9**: Write `results/metrics.json` in explicit-variant format with two variants
  (`different_set_post_fix`, `similar_set_post_fix`), each carrying only registered metric keys
  (`direction_selectivity_index`). Satisfied by Step 9. Evidence: file exists; `verify_task_metrics`
  exits 0.
* **REQ-10**: Quality gates pass (ruff, mypy, verify_task_metrics, verify_task_results, verify_logs,
  verify_task_folder, verify_task_file). Satisfied by Step 10. Evidence: each verificator command
  exits 0.

## Approach

The technical approach is a tightly-scoped reproduction of t0090's verification harness with a
single load-bearing change: the morphology builder is swapped from t0090's unpatched
`generate_morphology` to t0092's drop-in `generate_fixed_morphology`. Everything else — the
`_LIVE_CELLS` GC defence, the 50 ms `_stability_check_no_stim`, the 8-direction
`_run_8direction_protocol` (PD=0°, ND=180°, plus 45/90/135/225/270/315 with seed
`SEED_BASE + int(angle) * 13`), the `apply_parameter_vector` / `setup_synapses_parametric` /
`run_one_trial` pipeline from t0080's library, and the `load_t0083_best_cell_param_vector` loader
— is reused verbatim. The diff-clean reuse is the point: any per-cell delta between t0090's
pre-fix JSON and the new post-fix JSON is attributable to the soma-area patch and nothing else.

Key research findings driving the approach (from `research_code.md`):

* `tasks.t0092_..code.morphology_generator_fix.generate_fixed_morphology` has signature
  `(*, params: MorphologyParams, morph_seed: int | None = None) -> MorphologyResult`, structurally
  identical to t0090's `generate_morphology`. The fix re-emits the soma's two `pt3dadd` points so
  `pi * d * L = BEDB_AREA_TARGET_UM2 = 220.0 µm²`, recovering the soma area collapse that was the
  load-bearing root cause of t0090's 0/60 spike rate.
* t0092 already validated the patch on 1 BedB-equivalent + 5/5 STABLE-from-t0090 cells (e.g.
  `different/morph_14` reaches PD-rate 36.4 Hz / DSI 0.962). The headline novelty of this task is
  recovery of the 51-cell NAN_VOLTAGE bucket.
* The ARF library aggregator (`aggregate_libraries.py`) is **not present** in this branch — the
  same gap that t0092 documented. The replacement library is still discoverable via
  `arf.scripts.common.artifacts._load_library_record`, which honours `replace` corrections.
  `verify_corrections.py` validates `target_kind=library` and `action=replace` end-to-end.
* The corrections specification (v3) requires the file to live at
  `corrections/library_procedural_dsgc_morphology_generator.json` (filename pattern
  `<target_kind>_<target_id>.json`), `correcting_task` must equal the task folder name exactly, and
  the replacement must be the same `target_kind`.
* The 9 STABLE rows in t0090's pre-fix JSON have `dsi=0.0, peak_vm_mv=-70.0` and all-zero
  `per_direction_spikes` — they are STABLE-but-silent. The delta taxonomy must distinguish
  `stable_silent_to_stable_firing` (recovery) from `unchanged_stable_silent` (not affected by
  patch).

**Alternatives considered**:

* **Forking t0090's `generate_morphology` directly** instead of using the t0092 shim. Rejected: the
  t0092 shim is already a registered library asset, and re-implementing the patch in this task would
  duplicate code, complicate the correction overlay (which target would the overlay point at?), and
  break diff-clean attribution.
* **Skipping the re-sweep and issuing the correction overlay alone** based on t0092's 6-cell
  evidence. Rejected: the task description explicitly asks for the full 60-morph re-sweep precisely
  because t0092's small validation set leaves the project-level claim ("the patch fully fixes
  t0090") unverified across the 51-cell NAN_VOLTAGE bucket.
* **Refining BEDB_BASE_POINT to match t0024's 287 µm² reference** (S-0092-02) in the same task.
  Rejected: explicitly out of scope per task_description.md; the patched generator already lifts the
  soma area to ~220 µm² (its own target), and chasing the 287 µm² reference is a separate
  follow-up suggestion.
* **NSGA-II joint 68-d optimisation** (S-0092-05 / t0091). Rejected: deferred to t0091.

**Recommended task types**: `experiment-run` + `data-analysis` + `correction`. These match the
`task_types` field in `task.json` and inform the approach as follows:

* From `experiment-run`: set fixed seeds (the placer seed
  `SEED_BASE + (hash(default_params.values.tobytes()) & 0xFFFF)` and angle seeds
  `SEED_BASE + int(angle) * 13`), report per-population breakdowns in `metrics.json` using explicit
  variants (one per population), include a validation gate before the full-scale run, and inspect
  individual outputs after the small-scale run.
* From `data-analysis`: produce the explicit `transition_label` taxonomy with raw per-cell counts
  + ratios, embed all charts in the orchestrator-owned detailed-results document, save intermediate
    JSON outputs (not just charts).
* From `correction`: write the correction file in `corrections/`, never modify t0090's folder, align
  replacement asset metadata, run `verify_corrections.py` and verify the corrections-aware effective
  state.

## Cost Estimation

* **API costs**: $0. All compute is local NEURON simulation; no LLM, no cloud APIs.
* **Remote compute**: $0. All work runs on the local 64-core EPYC; no cloud GPU rental.
* **Storage**: Negligible (60 JSON rows + 3 PNG charts + one correction file ~ < 1 MB total).
* **Total**: **$0**, well within the project's $20.0 USD total budget and the $5.0 USD per-task
  default cap. The only consumed resource is wall-clock time on the local 64-core EPYC.

## Step by Step

The implementation work below is organized into four milestones (M1–M4). Each milestone is
independently verifiable: the agent confirms the milestone's gate before proceeding.

### Milestone 1: Code scaffolding

1. **Create `code/paths.py`.** Copy `tasks/t0090_morphology_generator_diversity_test/code/paths.py`
   (78 lines) and adapt:
   * Drop t0090-specific paths (`DATA_DIFFERENT_DIR`, `DATA_VERIFICATION_JSON`,
     `DATA_BEDB_REPRO_JSON`, `DATA_G1`/`G2`/`G3*`).
   * Add t0093-local paths:
     `DATA_POST_FIX_VERIFICATION_JSON = DATA_DIR / "post_fix_verification_summary.json"`,
     `DATA_PRE_POST_DELTA_JSON = DATA_DIR / "pre_post_delta.json"`,
     `DATA_LIBRARY_SUPERSESSION_JSON = DATA_DIR / "library_supersession_check.json"`.
   * Add cross-task references:
     `T0090_VERIFICATION_JSON = REPO_ROOT / "tasks" / "t0090_morphology_generator_diversity_test" / "data" / "verification_summary.json"`,
     `T0090_DIFFERENT_DIR`, `T0090_SIMILAR_DIR`.
   * Add image outputs: `POST_FIX_GRID_PNG = RESULTS_IMAGES_DIR / "post_fix_morphology_grid.png"`,
     `PRE_VS_POST_BAR_PNG = RESULTS_IMAGES_DIR / "pre_vs_post_spike_counts.png"`,
     `TRANSITION_FLOW_PNG = RESULTS_IMAGES_DIR / "transition_sankey.png"`.
   * Add corrections path:
     `CORRECTION_LIBRARY_JSON = TASK_ROOT / "corrections" / "library_procedural_dsgc_morphology_generator.json"`.
   * Run `ensure_directories()` in `__main__` for safety.
   * Expected output: file imports cleanly under
     `python -c "from tasks.t0093_resweep_and_t0090_correction.code.paths import *"`.
   * Satisfies: scaffolding for REQ-1, REQ-5, REQ-6, REQ-7, REQ-8.

2. **Create `code/constants.py`.** Define typed constants:
   * `STABILITY_FLAG_STABLE: str = "stable"`, `STABILITY_FLAG_NAN_VOLTAGE: str = "nan_voltage"`,
     `STABILITY_FLAG_DIVERGED: str = "diverged"`,
     `STABILITY_FLAG_DISCONNECTED: str = "disconnected"`
   * `POPULATION_DIFFERENT: str = "different"`, `POPULATION_SIMILAR: str = "similar"`
   * `PASS_CRITERION_MIN_FIRING: int = 50`, `STRETCH_CRITERION_MIN_FIRING: int = 55`
   * `TRANSITION_LABELS: list[str] = ["nan_to_stable_firing", "nan_to_stable_silent", "unchanged_nan", "unchanged_stable_silent", "stable_silent_to_stable_firing", "regression_stable_to_nan", "regression_stable_to_diverged", "unchanged_diverged", "unchanged_disconnected"]`
   * `STABILITY_FLAG_TO_COLOR: dict[str, str]` mapping each flag to an Okabe-Ito hex code (firing vs
     silent distinguished via two separate keys: `"stable_firing"` vs `"stable_silent"`).
   * `CORRECTION_ID: str = "C-0093-01"`
   * Expected output:
     `python -c "from tasks.t0093_resweep_and_t0090_correction.code.constants import *"` succeeds.
   * Satisfies: scaffolding for REQ-2, REQ-5, REQ-6, REQ-7, REQ-9.

3. **Verify M1 gate.** Run
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -c "from tasks.t0093_resweep_and_t0090_correction.code import paths, constants; paths.ensure_directories(); print('OK')"`.
   Expected: prints `OK`. If imports fail, fix paths before proceeding.

### Milestone 2: Re-sweep driver and validation gate

4. **[CRITICAL] Create `code/resweep_driver.py`.** Copy
   `tasks/t0090_morphology_generator_diversity_test/code/verification.py` (~330 lines) and adapt:
   * Replace import
     `from tasks.t0090_morphology_generator_diversity_test.code.generator import generate_morphology`
     with
     `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.
   * Replace inline `_insert_baseline_channels(cell=cell)` with
     `from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import insert_baseline_channels`
     and call site `insert_baseline_channels(h=cell.h, cell=cell)`.
   * Rename build-cell call site from `cell = generate_morphology(...)` to
     `cell = generate_fixed_morphology(...)`. Keep the `_LIVE_CELLS.append(cell)` defence.
   * Reuse the t0080 library imports unchanged: `apply_parameter_vector`,
     `setup_synapses_parametric`, `run_one_trial`, `SEED_BASE`, `PD_DIRECTION_DEG`,
     `ND_DIRECTION_DEG`, `TSTOP_MS`, `CELSIUS_DEG_C`, `DT_MS`, `STEPS_PER_MS`, `DSGCCellWithAIS`,
     `ParameterVector` from
     `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.assets.library.de_rosenroll_2026_dsgc_ais_dendritic_spike`.
   * Reuse `load_t0083_best_cell_param_vector` from
     `tasks.t0090_morphology_generator_diversity_test.code.load_default_params` (called once at
     driver start; vector applied to every morphology).
   * Extend `VerificationResult` dataclass and `_to_dict` with two columns:
     `pre_fix_stability_flag: str` and `pre_fix_spike_count_total: int`. Populate by reading
     `T0090_VERIFICATION_JSON` once and looking up `(population, morph_id)`.
   * Wire output to `DATA_POST_FIX_VERIFICATION_JSON`.
   * Reuse `_worker_verify` and `ProcessPoolExecutor` parallelism unchanged. Driver entry point is
     `main()` parsing `--limit`, `--max-workers`, and writing to the path constant.
   * **Validation gate**: this step performs expensive multi-process NEURON simulation. Trivial
     baseline: t0090's pre-fix run produced 0/60 cells with `pd_rate_hz > 0`. t0092's 5/5
     STABLE-from-t0090 sample plus the BedB-equivalent gives a strong prior (≥4/5 STABLE on the
     first 5 morphs) for the post-fix small run. **Run with `--limit 5 --max-workers 1` first.**
     Failure condition: if fewer than 4/5 cells reach `stability_flag == "stable"` (i.e. the small
     run reproduces t0090's NAN_VOLTAGE pattern), STOP and debug — the patch is not being applied.
     Inspect `cell.soma.L` after `generate_fixed_morphology(...)`; should be ~15 µm not ~1e-9 µm.
   * Individual-output inspection requirement: after the small run, read 5 rows of the produced
     `post_fix_verification_summary.json` (limit=5 means file will have 5 entries). Verify each
     row's `stability_flag`, `dsi`, `pd_rate_hz`, `peak_vm_mv` are reasonable values (not all null,
     not all zero) and the `per_direction_spikes` dict has 8 angle keys.
   * Expected output (after small run): file at `data/post_fix_verification_summary.json` with 5
     entries, ≥ 4/5 STABLE.
   * Expected output (after full run): file with 60 entries; logs report wall-clock ~30 min on 64
     cores.
   * Run command (small):
     `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m tasks.t0093_resweep_and_t0090_correction.code.resweep_driver --limit 5 --max-workers 1`.
   * Run command (full):
     `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m tasks.t0093_resweep_and_t0090_correction.code.resweep_driver --max-workers 0`.
     (`--max-workers 0` autodetects `cpu_count() - 1`.)
   * Fallback: if Windows `ProcessPoolExecutor` blows up (per-worker NEURON DLL load cost), set
     `--max-workers 1` and accept ~5 hours wall-clock.
   * Satisfies REQ-1, REQ-3, REQ-4.

### Milestone 3: Delta analysis and visualisations

5. **Create `code/delta_analysis.py`.** New module with no direct prior. Reads
   `T0090_VERIFICATION_JSON` (60 rows) and `DATA_POST_FIX_VERIFICATION_JSON` (60 rows), keys both on
   `(population, morph_id)`, classifies each cell's transition into one of the `TRANSITION_LABELS`
   values from `constants.py`, writes `DATA_PRE_POST_DELTA_JSON` with:
   * `cells: list[dict]` — one entry per cell with fields `morph_id`, `population`,
     `pre_stability_flag`, `post_stability_flag`, `pre_spike_count_total`, `post_spike_count_total`,
     `transition_label`, `pre_dsi`, `post_dsi`, `pre_pd_rate_hz`, `post_pd_rate_hz`.
   * `aggregate: dict` — fields `total_cells: 60`, `cells_with_nonzero_pd_rate: int`,
     `cells_post_stable: int`, `pass_criterion_met: bool` (true iff
     `cells_with_nonzero_pd_rate >= PASS_CRITERION_MIN_FIRING`), `stretch_criterion_met: bool` (true
     iff `>= STRETCH_CRITERION_MIN_FIRING`), `transitions_count: dict[str, int]` keyed by transition
     label.
   * Decision rules for `transition_label`:
     * `pre=stable, post=stable, pre_spikes=0, post_spikes=0` -> `unchanged_stable_silent`
     * `pre=stable, post=stable, pre_spikes=0, post_spikes>0` -> `stable_silent_to_stable_firing`
     * `pre=nan_voltage, post=stable, post_spikes>0` -> `nan_to_stable_firing`
     * `pre=nan_voltage, post=stable, post_spikes==0` -> `nan_to_stable_silent`
     * `pre=nan_voltage, post=nan_voltage` -> `unchanged_nan`
     * `pre=stable, post=nan_voltage` -> `regression_stable_to_nan`
     * `pre=stable, post=diverged` -> `regression_stable_to_diverged`
     * `pre=diverged, post=diverged` -> `unchanged_diverged`
     * `pre=disconnected, post=disconnected` -> `unchanged_disconnected`
   * Run command:
     `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m tasks.t0093_resweep_and_t0090_correction.code.delta_analysis`.
   * Expected output: `data/pre_post_delta.json` with 60-cell entries; stdout reports
     `pass_criterion_met` and `transitions_count`.
   * Satisfies REQ-2, REQ-5.

6. **Create `code/visualization.py`.** Copy
   `tasks/t0090_morphology_generator_diversity_test/code/visualization.py` (~172 lines) and adapt:
   * Replace `from tasks.t0090_..code.generator import generate_morphology` with
     `from tasks.t0092_..code.morphology_generator_fix import generate_fixed_morphology` and update
     call site.
   * Reuse `plot_dendrogram`, `_line_segments_for_cell`, `OKABE_ITO_PALETTE`, `make_grid_panel`
     verbatim. Keep `matplotlib.use("Agg")` for headless rendering.
   * Add
     `make_post_fix_grid_panel(*, summary_path: Path, morph_dir_different: Path, morph_dir_similar: Path, output_png: Path)`:
     builds a 6x10 grid (60 cells) coloured by post-fix stability flag using
     `STABILITY_FLAG_TO_COLOR` (with stable cells split into stable_firing vs stable_silent based on
     `pd_rate_hz > 0`).
   * Add `make_paired_bar_chart(*, summary_path: Path, output_png: Path)`: reads
     `post_fix_verification_summary.json`; for each cell plots two bars (pre-fix red at
     `pre_fix_spike_count_total`, post-fix green at sum of `per_direction_spikes`); cells sorted by
     post-fix descending; x-axis labels `population/morph_id`.
   * Add `make_transition_flow_chart(*, delta_path: Path, output_png: Path)`: stacked-bar fallback
     for Sankey — two columns (pre / post), each stack split by stability flag using
     `STABILITY_FLAG_TO_COLOR`; segments sized by cell count.
   * Run command:
     `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m tasks.t0093_resweep_and_t0090_correction.code.visualization`.
   * Expected output: three PNG files at `POST_FIX_GRID_PNG`, `PRE_VS_POST_BAR_PNG`,
     `TRANSITION_FLOW_PNG`.
   * Satisfies REQ-6.

### Milestone 4: Correction overlay, supersession check, metrics

7. **[CRITICAL] Create the correction overlay file.** Write
   `corrections/library_procedural_dsgc_morphology_generator.json` with the v3 envelope:
   * `spec_version: "3"`
   * `correction_id: "C-0093-01"`
   * `correcting_task: "t0093_resweep_and_t0090_correction"` (must match folder name exactly)
   * `target_task: "t0090_morphology_generator_diversity_test"`
   * `target_kind: "library"`
   * `target_id: "procedural_dsgc_morphology_generator"`
   * `action: "replace"`
   * `changes: { "replacement_task": "t0092_diagnose_morphology_generator_silence", "replacement_id": "procedural_dsgc_morphology_generator_fix" }`
   * `rationale`: at least 10 chars, citing (a) t0092's diagnosis of the soma-pt3d collapse, (b)
     this task's 60-morph re-sweep evidence (link to `data/post_fix_verification_summary.json`), (c)
     the t0091 / t0086 / t0088 downstream consumers that need the patched generator.
   * Verifier:
     `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m arf.scripts.verificators.verify_corrections t0093_resweep_and_t0090_correction`.
   * Expected output: exit code 0, no errors. The check covers required fields, `correction_id`
     regex `^C-\d{4}-\d{2}$`, `correcting_task = folder` invariant, target exists, kind/action
     valid, replacement artifact exists, no cycles, filename matches
     `<target_kind>_<target_id>.json`, rationale ≥ 10 chars.
   * **Issue this file regardless of REQ-2 outcome**: even if fewer than 50/60 cells fire, the
     correction still applies because t0091 / t0086 / t0088 need the patched generator. The
     correction is independent of the pass-criterion gate.
   * Satisfies REQ-7.

8. **Create `code/library_supersession_check.py`.** Programmatic confirmation that the corrections
   overlay routes library lookups to the t0092 library:
   * `aggregate_libraries.py` is **not present** in this branch (per `research_code.md` —
     `arf/scripts/aggregators/` directory listing confirms only categories, costs, machines,
     metric_results, metrics, suggestions, task_types, tasks).
   * Instead, this script imports `arf.scripts.common.artifacts` and calls
     `_load_library_record(target_task="t0090_morphology_generator_diversity_test", target_id="procedural_dsgc_morphology_generator")`
     (or whichever public entry point exists in that module), with corrections enabled, and asserts
     the returned record's `task_id` is `t0092_diagnose_morphology_generator_silence` and
     `library_id` is `procedural_dsgc_morphology_generator_fix`.
   * Writes `data/library_supersession_check.json` containing:
     * `aggregator_present: false`
     * `evidence: "library aggregator not present in branch — verified via arf.scripts.common.artifacts directly"`
     * `effective_task_id: "t0092_diagnose_morphology_generator_silence"`
     * `effective_library_id: "procedural_dsgc_morphology_generator_fix"`
     * `correction_id: "C-0093-01"`
   * Run command:
     `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m tasks.t0093_resweep_and_t0090_correction.code.library_supersession_check`.
   * Expected output: exit code 0; JSON written; stdout prints "supersession verified".
   * If `arf.scripts.common.artifacts` does not expose a usable public entry, fall back to reading
     the correction file directly + checking the t0092 library's `details.json` exists; record the
     fallback path in `evidence` field.
   * Satisfies REQ-8.

9. **Create `code/write_metrics.py`.** Reads `DATA_POST_FIX_VERIFICATION_JSON`, aggregates DSI per
   population, writes `results/metrics.json` in explicit-variant format. Source pattern:
   `tasks/t0092_..code/post_fix_verification.py` `_write_metrics_json` block (~30 lines).

   * Output structure:

     ```json
     {
       "variants": [
         {
           "variant_id": "different_set_post_fix",
           "label": "Different-set 30 morphologies (post-fix)",
           "dimensions": {
             "morphology_population": "different",
             "channels": "t0083_best_cell",
             "generator": "procedural_dsgc_morphology_generator_fix"
           },
           "metrics": {
             "direction_selectivity_index": <mean DSI over STABLE-and-firing cells, or null>
           }
         },
         {
           "variant_id": "similar_set_post_fix",
           "label": "Similar-set 30 morphologies (post-fix)",
           "dimensions": {
             "morphology_population": "similar",
             "channels": "t0083_best_cell",
             "generator": "procedural_dsgc_morphology_generator_fix"
           },
           "metrics": {
             "direction_selectivity_index": <mean DSI over STABLE-and-firing cells, or null>
           }
         }
       ]
     }
     ```

   * "STABLE-and-firing" means `stability_flag == "stable" AND pd_rate_hz > 0`.

   * Use `null` (Python `None`) when no STABLE-and-firing cells exist in a population. NEVER use
     `0.0` for missing data (per Python style guide: "use `None` for missing data, never zero").

   * Only the registered `direction_selectivity_index` metric key appears under `metrics`; every
     other interesting per-population statistic (e.g. mean PD rate, count of firing cells) belongs
     in the orchestrator-owned detailed-results document, not here.

   * **Measurement step for the `direction_selectivity_index` registered metric** (per the planning
     skill's metric-applicability requirement): this step computes mean DSI over STABLE-and-firing
     cells, separately for `different` and `similar` populations, and writes them as the only
     registered metric in each variant.

   * Other registered metrics in `meta/metrics/` (`tuning_curve_hwhm_deg`,
     `tuning_curve_reliability`, `tuning_curve_rmse`) **do not apply** to this task because the task
     does not fit a parametric tuning curve to a target reference; it only computes the DSI scalar.
     Stating this omission explicitly so the absence is deliberate.

   * Run command:
     `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m tasks.t0093_resweep_and_t0090_correction.code.write_metrics`.

   * Expected output: `results/metrics.json` exists; `verify_task_metrics.py` exits 0.

   * Satisfies REQ-9.

10. **Run all quality gates.** From the task worktree:
    * `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- ruff check --fix .`
      (expected exit 0)
    * `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- ruff format .`
      (expected exit 0)
    * `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- mypy .`
      (expected exit 0)
    * `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m arf.scripts.verificators.verify_corrections t0093_resweep_and_t0090_correction`
      (expected 0 errors)
    * `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m arf.scripts.verificators.verify_task_metrics t0093_resweep_and_t0090_correction`
      (expected 0 errors)
    * `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m arf.scripts.verificators.verify_task_results t0093_resweep_and_t0090_correction`
      (expected 0 errors; this verificator may report missing orchestrator-managed result documents,
      which is acceptable until those steps run)
    * `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m arf.scripts.verificators.verify_logs t0093_resweep_and_t0090_correction`
      (expected 0 errors)
    * `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m arf.scripts.verificators.verify_task_folder t0093_resweep_and_t0090_correction`
      (expected 0 errors)
    * `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m arf.scripts.verificators.verify_task_file t0093_resweep_and_t0090_correction`
      (expected 0 errors)
    * Satisfies REQ-10.

The Step by Step ends here at "compute metrics and produce charts". Subsequent orchestrator-managed
steps (results writing, cost recording, suggestion generation, and literature comparison) are out of
scope for this plan.

## Remote Machines

None required. All computation runs on the local 64-core EPYC. The bottleneck is NEURON simulation
which is CPU-bound; the 64-core box gives ~30 min wall-clock for the 60-morph re-sweep at ~30 sec /
cell sequential time per cell. No GPU is needed.

## Assets Needed

* **Library `procedural_dsgc_morphology_generator_fix`** from t0092 — provides
  `generate_fixed_morphology` and `insert_baseline_channels`. Imported via library.
* **Library `de_rosenroll_2026_dsgc_ais_dendritic_spike`** from t0080 — provides
  `apply_parameter_vector`, `setup_synapses_parametric`, `run_one_trial`, `DSGCCellWithAIS`,
  `ParameterVector`, `SEED_BASE`, `PD_DIRECTION_DEG`, `ND_DIRECTION_DEG`, `TSTOP_MS`,
  `CELSIUS_DEG_C`, `DT_MS`, `STEPS_PER_MS`. Imported unchanged.
* **Library `procedural_dsgc_morphology_generator`** from t0090 — provides `MorphologyParams`,
  `MorphologyResult`, `StabilityKind`, `BEDB_BASE_POINT`, `PARAM_BOUNDS`,
  `load_t0083_best_cell_param_vector`, the 60 morph spec JSONs in `data/different_morphologies/` +
  `data/similar_morphologies/`, and the pre-fix `data/verification_summary.json` for delta analysis.
  Imported via library; data files read via paths from `code/paths.py`.
* **Pareto-front data file**
  `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json` — loaded transitively
  by `load_t0083_best_cell_param_vector`. No direct import.

## Expected Assets

No new library, dataset, model, paper, predictions, or answer assets are produced —
`expected_assets` in `task.json` is `{}`. The deliverables are data/result/correction artifacts:

* `data/post_fix_verification_summary.json` — 60-row JSON in t0090's row schema plus
  `pre_fix_stability_flag` and `pre_fix_spike_count_total` columns.
* `data/pre_post_delta.json` — per-cell `transition_label` + aggregate counts including pass /
  stretch criterion booleans.
* `data/library_supersession_check.json` — programmatic evidence that the corrections-aware
  effective library is the t0092 fix.
* `results/images/post_fix_morphology_grid.png` — 60-cell grid coloured by post-fix stability
  flag.
* `results/images/pre_vs_post_spike_counts.png` — paired bar chart per cell, sorted by post-fix
  spike count descending.
* `results/images/transition_sankey.png` — stacked-bar transition flow (Sankey-style fallback).
* `corrections/library_procedural_dsgc_morphology_generator.json` — v3 envelope, action `replace`.
* `results/metrics.json` — explicit-variant format with two variants (`different_set_post_fix`,
  `similar_set_post_fix`), each carrying only `direction_selectivity_index`.

## Time Estimation

* **M1 (scaffolding)**: ~15 min — paths.py + constants.py + import smoke test.
* **M2 (re-sweep driver + small + full run)**: ~45 min total — ~10 min driver code + ~5 min
  small-run validation gate + ~30 min full 60-morph run on 64 cores. Fallback to single-process is
  ~5 hours.
* **M3 (delta analysis + visualisations)**: ~60 min — ~30 min for `delta_analysis.py` + ~30 min
  for `visualization.py` (mostly copying t0090 + adding the bar / flow chart code).
* **M4 (correction overlay + supersession check + metrics + quality gates)**: ~45 min — ~10 min
  correction file + verifier, ~15 min `library_supersession_check.py`, ~10 min `write_metrics.py`,
  ~10 min ruff/mypy/verificators.
* **Total wall-clock**: ~3-4 hours including the validation gate on the small run.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Validation-gate small run reproduces t0090's NAN_VOLTAGE pattern (patch not being applied) | Low | Bug in import path or fix-shim invocation | Halt at the gate; inspect `cell.soma.L` and `cell.soma.diam` after `generate_fixed_morphology(...)`; should be ~15 µm and the diameter set so `pi * d * L = 220 µm²`. If still ~1e-9 µm, the unpatched generator is being called — re-check imports. |
| Post-fix re-sweep has fewer than 50/60 cells firing (REQ-2 miss) | Medium | Pass criterion miss but does not block correction overlay | Document the surviving failure modes per `transition_label`; correction overlay is independent of the pass-criterion outcome (acceptable-negative branch per task description). Record per-population pass rate and breakdown of `unchanged_nan` cells in `results_detailed.md`. |
| ProcessPoolExecutor on Windows / EPYC has high per-worker NEURON DLL load cost or pickling errors on `cell` reference | Medium | Wall-clock blow-out (~5 hours instead of ~30 min) | Single-process serial fallback (`--max-workers 1`); ~5 min × 60 = ~5 hours. Still within the day's budget. Driver already supports `--max-workers 1` from t0090's harness. |
| Correction-overlay format error (e.g. `correcting_task` mismatch, filename mismatch, missing `replacement_id`) | Low | `verify_corrections.py` fails | Re-read `arf/specifications/corrections_specification.md` v3 carefully before writing; copy the example library `replace` envelope (C-0042-04) verbatim and only change task / id fields; run `verify_corrections.py` immediately after writing. |
| `arf.scripts.common.artifacts` does not expose a usable public entry for the supersession check | Low | REQ-8 cannot be satisfied programmatically via the artifacts module | Fallback to reading the correction JSON directly and verifying the t0092 library's `details.json` exists; record the fallback path string in `evidence` field of `library_supersession_check.json`. The correction overlay itself remains the load-bearing artifact for downstream consumers; the supersession-check script is documentation. |
| Cross-task imports (t0080 / t0090 / t0092 libraries) fail due to PYTHONPATH or `__init__.py` missing in the worktree | Low | Driver / visualisation cannot start | Confirm each library has `__init__.py`; absolute imports use the form `tasks.t0XYZ_..code.module`; run a smoke import test in M1 step 3 before building further code. |

## Verification Criteria

* `data/post_fix_verification_summary.json` exists with **exactly 60 entries** (30 different + 30
  similar). Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -c "import json; d = json.load(open('tasks/t0093_resweep_and_t0090_correction/data/post_fix_verification_summary.json')); print(len(d))"`.
  Expected output: `60`. Covers REQ-1.
* `data/pre_post_delta.json` `aggregate.cells_with_nonzero_pd_rate >= 50`. Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -c "import json; d = json.load(open('tasks/t0093_resweep_and_t0090_correction/data/pre_post_delta.json')); print(d['aggregate']['cells_with_nonzero_pd_rate'], d['aggregate']['pass_criterion_met'])"`.
  Expected: a number ≥ 50 followed by `True`. Covers REQ-2, REQ-5.
* The three chart files exist: `results/images/post_fix_morphology_grid.png`,
  `results/images/pre_vs_post_spike_counts.png`, `results/images/transition_sankey.png`. Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -c "from pathlib import Path; assert all( Path(f'tasks/t0093_resweep_and_t0090_correction/results/images/{n}').exists() for n in ['post_fix_morphology_grid.png','pre_vs_post_spike_counts.png','transition_sankey.png']); print('OK')"`.
  Expected output: `OK`. Covers REQ-6.
* `corrections/library_procedural_dsgc_morphology_generator.json` exists and `verify_corrections.py`
  passes with 0 errors. Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m arf.scripts.verificators.verify_corrections t0093_resweep_and_t0090_correction`.
  Expected output: exit code 0, no error lines. Covers REQ-7.
* `data/library_supersession_check.json` exists with
  `effective_task_id == "t0092_diagnose_morphology_generator_silence"` and
  `effective_library_id == "procedural_dsgc_morphology_generator_fix"`. Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -c "import json; d = json.load(open('tasks/t0093_resweep_and_t0090_correction/data/library_supersession_check.json')); assert d['effective_task_id'] == 't0092_diagnose_morphology_generator_silence' and d['effective_library_id'] == 'procedural_dsgc_morphology_generator_fix'; print('OK')"`.
  Expected: `OK`. Covers REQ-8.
* `results/metrics.json` is in explicit-variant format with two variants and only the registered
  `direction_selectivity_index` key, and `verify_task_metrics.py` passes with 0 errors. Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0093_resweep_and_t0090_correction -- python -u -m arf.scripts.verificators.verify_task_metrics t0093_resweep_and_t0090_correction`.
  Expected: exit code 0. Covers REQ-9.
* `ruff check`, `ruff format`, `mypy` exit 0; `verify_task_results.py`, `verify_logs.py`,
  `verify_task_folder.py`, `verify_task_file.py` exit 0. Covers REQ-10.
* **Requirement-coverage check**:
  `grep "REQ-" tasks/t0093_resweep_and_t0090_correction/plan/plan.md | wc -l` returns at least 30
  (10 unique REQ-* IDs each referenced multiple times across Objective, Checklist, and Step by
  Step). Confirms every REQ-* item is mapped to at least one step.
