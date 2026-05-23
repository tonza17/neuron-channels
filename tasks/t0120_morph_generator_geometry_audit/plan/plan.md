---
spec_version: "2"
task_id: "t0120_morph_generator_geometry_audit"
date_completed: "2026-05-24"
status: "complete"
---
# Plan: Morphology Generator Geometry Audit (15-20 cells)

## Objective

Empirically verify that the procedural DSGC morphology generator
(`tasks/t0090_morphology_generator_diversity_test/code/generator.py` plus the
`generate_fixed_morphology` patch in
`tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py`) produces a
geometrically consistent cell across 15-20 cells stratified across the asymmetry-parameter extremes
that drive the visual artefact seen in t0115's `top50_morphologies_seed9354.png`.

For every sampled cell, the audit must run three coordinate-consistency checks:

1. **Check 1** -- every primary dendrite section's `start_xy` equals the cell's `origin_xy` within
   float tolerance.
2. **Check 2** -- every non-primary child section's `start_xy` equals its parent section's `end_xy`
   within float tolerance.
3. **Check 3** -- the NEURON `h.x3d(mid)/h.y3d(mid)` midpoint coordinate of each dendrite section
   lies on the line from its Python `start_xy` to `end_xy` and is in the same coordinate frame as
   `origin_xy` (the post-asymmetry frame).

In addition, the audit must explicitly inspect the **soma frame split** introduced by the t0092
patch: the patch calls `h.pt3dclear()` on the soma and re-emits two pt3d points along the z-axis at
`(0, 0, 0)` and `(0, 0, soma_diameter_um)`, pinning the NEURON soma pt3d at `xy = (0, 0)` while
Python `origin_xy` is set from the post-asymmetry `soma_node.end_xy = (soma_offset_pd_um, 0)`. The
plan must explicitly compare these two soma coordinates per cell and confirm that no downstream
synapse-bar-arrival-timing code reads soma pt3d (synapses are placed on dendrites in the t0091 +
t0118 protocol, so the subtraction `(syn_xy - origin_xy)` cancels `soma_offset` only if both
operands live in the post-asymmetry frame).

Done is defined as: one answer asset with an unambiguous verdict (rendering-only artefact vs real
geometry bug requiring framework re-runs), one per-cell pass/fail CSV, one full pt3d JSON dump per
cell, one sampled-cell manifest CSV, and one visual diagnostic gallery PNG. The verdict gates
whether every 68-d morphology-extended NSGA-II result from t0091 onward (t0091, t0099, t0102, t0104,
t0106, t0112, t0114, t0115, t0118) must be re-run.

## Task Requirement Checklist

The operative task text from `task.json` and `task_description.md`:

> Audit procedural morphology generator: verify primary stems start at origin_xy, parent/child
> endpoint match, and synapse pt3d xy frame matches origin_xy across 15-20 visually-diverse cells.
> Gates downstream NSGA-II.
>
> Sample 15-20 cells stratified across the asymmetry-parameter extremes that drive the visual
> artefact, plus symmetric controls. Dump the full `section_endpoints_xy` and NEURON `h.x3d/h.y3d`
> pt3d for each cell. Verify three properties analytically and visually for each cell: (1) Primary
> stems start at `origin_xy`; (2) Parent / child endpoint match; (3) Synapse-vs-soma coordinate
> frame consistency.

Concrete requirements (stable IDs used downstream in steps and verification):

* **REQ-1** -- Sample 15-20 cells stratified across the four asymmetry parameters
  (`soma_offset_pd_um`, `field_elongation_pd`, `branch_density_gradient_pd`,
  `primary_branch_pd_concentration`), 3 "worst-looking" visually-flagged cells, and 3-5 symmetric
  controls near BEDB_BASE_POINT defaults. Source: t0117 pooled cells parquet (4431 cells across
  seeds 44 / 77 / 7755 / 9354). Evidence: rows in `results/data/sampled_cell_manifest.csv`.
  Satisfied by Steps 3-4.

* **REQ-2** -- For each sampled cell, instantiate via `generate_fixed_morphology` (the patched
  generator that every NSGA-II run from t0091 onward uses) with the NEURON DLL bypass applied.
  Evidence: per-cell entries in `results/data/section_endpoints_dump.json`. Satisfied by Steps 5-6.

* **REQ-3** -- For each sampled cell, dump the full `section_endpoints_xy` (Python frame) **and**
  the NEURON `h.x3d(i)/h.y3d(i)/h.z3d(i)/h.diam3d(i)` pt3d for every section. Evidence:
  `results/data/section_endpoints_dump.json` per-section entries with both
  `python_start_xy / python_end_xy` and `neuron_pt3d` arrays. Satisfied by Step 6.

* **REQ-4** -- Run **Check 1** (primary stem `start_xy ≈ origin_xy`) on every primary dendrite
  section of every sampled cell. Evidence: `check1_primary_start` column in
  `results/data/coordinate_consistency_checks.csv` plus per-section detail in JSON dump. Satisfied
  by Step 7.

* **REQ-5** -- Run **Check 2** (`child.start_xy ≈ parent.end_xy`) on every non-primary dendrite
  section of every sampled cell. Evidence: `check2_parent_child` column in the CSV plus per-edge
  detail in JSON dump. Satisfied by Step 7.

* **REQ-6** -- Run **Check 3** (synapse pt3d midpoint frame consistency) on every dendrite section
  of every sampled cell, using a modified copy of `_section_midpoint_xy` that raises on `n3d() == 0`
  rather than silently returning `(0.0, 0.0)`. Evidence: `check3_synapse_frame` column in the CSV
  plus per-section midpoint coords in JSON dump. Satisfied by Step 7.

* **REQ-7** -- Explicitly compare the soma's Python `origin_xy` against the NEURON soma pt3d xy
  (`h.x3d(0)`, `h.y3d(0)`, `h.x3d(1)`, `h.y3d(1)`) and record the discrepancy per cell. The expected
  result (from the t0092 fix's z-axis re-emission) is `origin_xy = (soma_offset_pd_um, 0)` and soma
  pt3d at `(0, 0)`. Evidence: `soma_origin_x`, `soma_origin_y`, `soma_pt3d_x_min`,
  `soma_pt3d_x_max`, `soma_pt3d_y_min`, `soma_pt3d_y_max`, `soma_frame_offset_um` columns in the
  CSV. Satisfied by Step 7.

* **REQ-8** -- Confirm analytically that no synapse-placement code in the t0091 / t0118 protocol
  reads soma pt3d for arrival-time projection (synapses are placed only on dendrites). Evidence: a
  narrative paragraph in the answer asset's full answer citing
  `tasks/t0091_morphology_extended_nsga2_v1/code/trial_helpers.py` lines 64-178 and
  `tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/code/` synapse placement. Satisfied by Step
  8 (verdict narrative).

* **REQ-9** -- Produce a per-cell pass/fail CSV with one row per sampled cell at
  `results/data/coordinate_consistency_checks.csv` with three pass/fail columns plus
  asymmetry-parameter values plus the soma-frame columns from REQ-7. Satisfied by Step 7.

* **REQ-10** -- Produce a sampled-cell manifest CSV at `results/data/sampled_cell_manifest.csv` with
  one row per sampled cell, the stratum tag, all 14 morphology parameters, plus the source task,
  seed, generation, and individual_idx columns from the t0117 parquet. Satisfied by Step 4.

* **REQ-11** -- Produce a full pt3d JSON dump at `results/data/section_endpoints_dump.json` with one
  entry per sampled cell containing all section endpoints in both frames. Satisfied by Step 6.

* **REQ-12** -- Produce a visual diagnostic gallery at `results/images/geometry_audit_gallery.png`
  with each cell rendered at 2x t0115's panel size, primary-stem linewidth 2.0, contrasting color
  (e.g. `tab:red`), soma `Circle` with `radius = soma_diameter_um / 2` (not fixed 6 px), and a thin
  debug line from `origin_xy` to each primary stem's `end_xy`. Satisfied by Step 9.

* **REQ-13** -- Write one answer asset under
  `assets/answer/morphology-generator-geometry-consistency/` answering "Is the procedural morphology
  generator's asymmetry transform geometrically consistent across the 15-20 sampled cells?" using v2
  `details.json` format with `answer_methods: ["code-experiment"]`, source-task IDs covering t0090,
  t0092, t0115, t0117, t0119, and a confidence level reflecting check pass/fail counts. Satisfied by
  Step 8.

* **REQ-14** -- The verdict in the answer asset must unambiguously state one of: (a) "rendering-only
  artefact -- no NSGA-II re-runs needed" if all 3 checks pass on all sampled cells, or (b) "real
  geometry bug detected -- framework decision needed before further NSGA-II runs" if any check
  fails. Satisfied by Step 8.

## Approach

This is a **data-analysis** + **answer-question** task with no electrical simulation, no remote
machines, and no paid services. The recommended task types (already set in `task.json`:
`["data-analysis", "answer-question"]`) match perfectly. The data-analysis Planning Guidelines drive
the requirement to define metrics/charts upfront and to centralize paths in `code/paths.py`; the
answer-question Planning Guidelines drive the requirement to define the single canonical question
text and to plan the evidence stopping criterion before writing code.

**Key research findings that ground the approach:**

1. **The t0092 fix introduces a deliberate soma-frame split.** The patch
   (`morphology_generator_fix.py` lines 61-75) calls `h.pt3dclear()` on the soma and re-emits two
   pt3d points along the z-axis at `(0, 0, 0)` and `(0, 0, soma_diameter_um)` to fix a
   zero-pt3d-distance bug (t0092's diagnosis: the t0090 generator emitted two coincident soma pt3d
   points at `(0, 0)`, causing NEURON to override `sec.L` from `soma_diameter_um` down to ~1e-9 um,
   collapsing the soma area to ~9.4e-14 um^2 and driving Vm to NaN). After the fix, the NEURON soma
   pt3d xy is **pinned at (0, 0)** regardless of `soma_offset_pd_um`, while the Python `origin_xy`
   is set from the post-asymmetry `soma_node.end_xy = (soma_offset_pd_um, 0)`. **This is the most
   critical thing to audit empirically**, and step 7 contains the explicit soma-frame comparison.

2. **Synapse arrival time uses `(syn_xy - origin_xy)`** in
   `tasks/t0091_morphology_extended_nsga2_v1/code/trial_helpers.py` lines 64-75. Synapse xy is read
   via `_section_midpoint_xy` (lines 160-178) which calls `h.x3d(mid), h.y3d(mid)`. **Because all
   SAC synapses are placed on dendrites (never the soma) in the t0091 / t0118 protocol, the
   subtraction cancels `soma_offset` correctly** -- provided both `syn_xy` and `origin_xy` are in
   the post-asymmetry frame for dendrite sections. Check 3 is the empirical verification of this
   frame consistency for dendrites.

3. **Electrical topology is `sec.connect()`-based** (lines 455-462 of `generator.py`), which ignores
   pt3d coordinates. So even if Check 3 reveals a frame mismatch on dendrites, the electrical
   simulation itself would remain valid; only the bar arrival timing would be affected. This is the
   rationale for the conditional verdict in REQ-14.

4. **The visual artefact is almost certainly a rendering convention choice** (the brainstorm-23
   preliminary trace). [t0115]'s `build_top50_morphologies.py` uses fixed `radius=6.0` soma circles,
   linewidth 0.4 dendrite strokes, and an auto-zoom bounding box that amplifies asymmetry. The audit
   gallery (Step 9) renders at 2x panel size with `radius = soma_diameter_um / 2` and linewidth 2.0
   on primary stems to discriminate visual artefact from real disconnection.

5. **Reuse rather than re-derive.** Copy `_collect_pt3d`, `_pt3d_euclidean_length`, `Pt3dPoint`,
   `SectionDump`, `CellDump` from
   `tasks/t0092_diagnose_morphology_generator_silence/code/structural_dump.py` (~140 lines). Copy
   `_section_midpoint_xy` from `tasks/t0091_morphology_extended_nsga2_v1/code/trial_helpers.py`
   lines 160-178 (~19 lines). Adapt `_assign_quintile` decile-stratification pattern from
   `tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/code/stratified_sample.py` (~50 lines).
   Copy the NEURON DLL bypass pattern from
   `tasks/t0115_seed9354_no_autostop/code/build_top50_morphologies.py` lines 42-59 (~10 lines). Copy
   `_params_from_14d` from the same t0115 file lines 100-116 (~17 lines). **Total: ~240 lines copied
   \+ ~150 lines of audit-specific glue.**

6. **Import `generate_fixed_morphology` via library**:
   `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.

7. **Sampling source**:
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_all_cells.parquet` (4431
   cells, with full 68-d vectors including `morph_seed`, `generation`, `individual_idx`, `seed`,
   `source_task`). The 14 morphology parameter names are exposed as
   `tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.constants.MORPHOLOGY_PARAM_NAMES`.

**Alternatives considered:**

* **Alt A: Audit every cell in the pooled parquet (4431 cells).** Rejected because the audit's
  purpose is to detect a systematic generator bug, not to characterize per-cell variation. 15-20
  cells stratified across the asymmetry extremes is enough statistical coverage to detect any
  systematic frame mismatch with high confidence, and finishes in minutes of CPU time rather than
  hours.
* **Alt B: Run a full electrical simulation per cell and verify bar arrival timing end-to-end.**
  Rejected because that would conflate geometry consistency with electrical correctness, expanding
  scope and inflating runtime by 100x+. The brainstorm-23 trace already established that electrical
  topology is `sec.connect()`-based; the audit's job is to verify the geometry assumption that
  arrival timing depends on.
* **Alt C: Add the audit to the existing t0115 / t0117 codebase and check coordinates inline during
  rendering.** Rejected because that would require modifying completed task folders (forbidden by
  rule 5 / the immutability principle) and would not produce a standalone audit artefact.
* **Alt D: Use a registered project metric (e.g., DSI) for the audit's pass/fail.** Rejected because
  the four registered metrics (DSI, tuning_curve_hwhm_deg, tuning_curve_reliability,
  tuning_curve_rmse) all apply to electrical-simulation tasks; none measure geometry consistency.
  This is explicitly noted in "Cost Estimation" and the metrics-omission rationale below.

## Cost Estimation

**Total estimated cost: $0.00.**

* **API calls (LLM inference)**: $0 -- no LLM calls inside the audit pipeline.
* **Remote compute (GPU rental, cloud)**: $0 -- local CPU only. See "Remote Machines" section.
* **External services / paid downloads**: $0 -- all data is already in the project repo (t0117
  parquet) and all libraries are project-internal.
* **Local CPU time**: ~1-2 CPU hours total (15-20 cells x ~30-60 seconds per cell for generator
  invocation + pt3d dump + check evaluation + gallery rendering). On the researcher's local Windows
  machine this is essentially free.

The t0119 brainstorm-23 budget estimate noted "<$0.10 (essentially $0)". The project budget
(`project/budget.json`) allows $8.00 per task by default and $100.00 total; this task uses well
under 1% of either envelope.

## Step by Step

All steps are executed locally on Windows via `PYTHONIOENCODING=utf-8 uv run python ...` wrapped in
`arf.scripts.utils.run_with_logs --task-id t0120_morph_generator_geometry_audit`. Every step writes
its outputs to deterministic paths defined in `code/paths.py` so the pipeline is idempotent.

### Milestone A: Setup and sampling (Steps 1-4)

1. **Create `code/paths.py` with all path constants.** Define `REPO_ROOT`, `TASK_ROOT`, `CODE_DIR`,
   `DATA_DIR`, `RESULTS_DIR`, `RESULTS_DATA_DIR`, `RESULTS_IMAGES_DIR`, `ASSETS_DIR`, `ANSWERS_DIR`
   as `pathlib.Path` constants. Define per-output constants `POOLED_ALL_CELLS_PARQUET` (pointing at
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_all_cells.parquet`),
   `SAMPLED_CELL_MANIFEST_CSV`, `COORDINATE_CONSISTENCY_CHECKS_CSV`, `SECTION_ENDPOINTS_DUMP_JSON`,
   `GEOMETRY_AUDIT_GALLERY_PNG`. Pattern source:
   `tasks/t0115_seed9354_no_autostop/code/build_top50_morphologies.py` lines 33-37 and
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/paths.py`. Expected observable
   output: file created, no path errors when imported. Satisfies REQ-1, REQ-9, REQ-10, REQ-11,
   REQ-12.

2. **Create `code/constants.py` with audit constants.** Define `MORPHOLOGY_PARAM_NAMES` (re-export
   from `tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.constants`), the four
   asymmetry-parameter names as
   `ASYMMETRY_PARAM_NAMES = ["soma_offset_pd_um", "field_elongation_pd", "branch_density_gradient_pd", "primary_branch_pd_concentration"]`,
   BEDB_BASE_POINT defaults for symmetric-control selection (re-export from t0090 / t0091 or copy
   verbatim), tolerance constants `CHECK_ABS_TOL: float = 1e-6` and `CHECK_REL_TOL: float = 1e-9`
   (per the research_code.md recommendation), and the stratum-tag enum (`StratumTag(Enum)` with
   values `SOMA_OFFSET_TOP`, `ELONGATION_TOP`, `ELONGATION_BOTTOM`, `BRANCH_DENSITY_TOP`,
   `PRIMARY_CONCENTRATION_TOP`, `WORST_LOOKING`, `SYMMETRIC_CONTROL`). Expected: imports succeed, no
   NameErrors. Satisfies REQ-1.

3. **Copy + adapt the stratified sampler into `code/stratified_sampler.py`.** Copy the
   `_assign_quintile` function (~50 lines) from
   `tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/code/stratified_sample.py` into
   `code/stratified_sampler.py`. Adapt it to use
   `pd.qcut(x=series, q=10, labels=False, duplicates="drop")` (deciles instead of quintiles). Add a
   per-stratum sampler
   `sample_extreme_decile(*, df: pd.DataFrame, column: str, top: bool = True, n: int = 3) -> pd.DataFrame`
   that returns up to `n` rows from the top (or bottom) decile of `column`. Add
   `sample_symmetric_controls(*, df: pd.DataFrame, n: int = 4, tol: float = 0.10) -> pd.DataFrame`
   that returns up to `n` rows where all four asymmetry parameters are within `tol` (fractional) of
   their BEDB_BASE_POINT defaults. Satisfies REQ-1.

4. **Create `code/sample_cells.py` that produces `results/data/sampled_cell_manifest.csv`.** Load
   the pooled parquet via `pd.read_parquet(POOLED_ALL_CELLS_PARQUET)`. Use the samplers from Step 3
   to select:
   * 3 cells with `|soma_offset_pd_um|` in top decile (tag `SOMA_OFFSET_TOP`)
   * 1-2 cells with `field_elongation_pd` in top decile + 1-2 in bottom decile (tags
     `ELONGATION_TOP`, `ELONGATION_BOTTOM`, total 3)
   * 3 cells with `|branch_density_gradient_pd|` in top decile (tag `BRANCH_DENSITY_TOP`)
   * 3 cells with `primary_branch_pd_concentration` in top decile (tag `PRIMARY_CONCENTRATION_TOP`)
   * 3 cells flagged manually from inspection of `top50_morphologies_seed9354.png` (tag
     `WORST_LOOKING`). The script reads a small CSV `code/worst_looking_cells.csv` of
     `(source_task, seed, generation, individual_idx)` tuples hand-curated from the t0115 PNG;
     create that CSV during the step by picking 3 visually-suspect cells from the existing
     `tasks/t0115_seed9354_no_autostop/results/images/top50_morphologies_seed9354.png` review.
   * 3-5 symmetric controls (tag `SYMMETRIC_CONTROL`) from `sample_symmetric_controls`.

   Deduplicate by `(source_task, seed, generation, individual_idx)`. Target final count: 15-20
   cells; if duplicates drop the count below 15, fall back to top-decile single-parameter sampling
   to top up. Write to `SAMPLED_CELL_MANIFEST_CSV` with columns
   `cell_id, source_task, seed, generation, individual_idx, stratum_tag` plus all 14 columns from
   `MORPHOLOGY_PARAM_NAMES` plus `dsi` and `pd_rate_hz` (for narrative context only -- the audit
   does not run electrical simulations). Use explicit dtypes per the data-analysis Planning
   Guidelines. Expected observable output: CSV with 15-20 rows, all stratum tags represented, no
   duplicate `cell_id`. Satisfies REQ-1, REQ-10.

### Milestone B: Coordinate dump and check execution (Steps 5-7)

5. **Copy the NEURON DLL bypass + `_section_midpoint_xy` + structural-dump helpers into
   `code/dump_helpers.py`.** Copy the NEURON DLL bypass (~10 lines) from
   `tasks/t0115_seed9354_no_autostop/code/build_top50_morphologies.py` lines 42-59. Copy
   `_collect_pt3d`, `_pt3d_euclidean_length`, `_section_area`, `_dump_one_section`, `_parent_name`,
   `Pt3dPoint`, `SectionDump`, `CellDump` (~140 lines) from
   `tasks/t0092_diagnose_morphology_generator_silence/code/structural_dump.py` lines 39-186. Copy
   `_section_midpoint_xy` (~19 lines) from
   `tasks/t0091_morphology_extended_nsga2_v1/code/trial_helpers.py` lines 160-178, **modified** to
   raise `RuntimeError("degenerate section: h.n3d() == 0")` when `h.n3d() == 0` instead of silently
   returning `(0.0, 0.0)` (per the research_code.md "approaches to avoid" guidance). Copy
   `_params_from_14d` (~17 lines) from the t0115 file lines 100-116. Extend `SectionDump` with new
   frozen fields `python_start_xy: tuple[float, float] | None`,
   `python_end_xy: tuple[float, float] | None`, and
   `midpoint_xy_neuron: tuple[float, float] | None`. Extend `CellDump` with
   `origin_xy: tuple[float, float]`, `soma_pt3d_xy_min: tuple[float, float]`,
   `soma_pt3d_xy_max: tuple[float, float]`, `soma_frame_offset_um: float`,
   `asymmetry_params: dict[str, float]`, `stratum_tag: str`, and `check_results: dict[str, bool]`.
   Satisfies REQ-2, REQ-3, REQ-6.

6. **Create `code/dump_cells.py` that produces `results/data/section_endpoints_dump.json`.** Read
   the sampled manifest from Step 4. For each row, build a `MorphologyParams` via `_params_from_14d`
   on the 14 morphology columns, then call
   `generate_fixed_morphology(params=params, morph_seed=int(row.morph_seed))`. For each cell,
   iterate the NEURON sections via `cell.h`, run `_dump_one_section` per section, and serialize the
   resulting `CellDump` list to JSON via `dataclasses.asdict`. Strip the `_t90` NEURON suffix when
   matching to `section_endpoints_xy` keys (per the t0092 / t0115 pattern). Apply the NEURON DLL
   bypass monkey-patch once at module import time before any `generate_fixed_morphology` call.
   Expected observable output: JSON file with one top-level entry per sampled cell, each entry
   containing `origin_xy`, `soma_pt3d_xy_min`, `soma_pt3d_xy_max`, `soma_frame_offset_um`, and a
   `sections: list[SectionDump]` array with both `python_start_xy / python_end_xy` and full
   `neuron_pt3d` arrays for every section. Print per-cell stdout summary:
   `"cell_id={...} n_sections={...} soma_frame_offset_um={...}"`. Satisfies REQ-2, REQ-3, REQ-11.

   **Validation gate**: this step processes only 15-20 cells (well under 100 items) and runs no paid
   API or remote compute, so the standard expensive-operation validation gate (REQ baseline +
   `--limit` flag) does not strictly apply. However, the step still validates by running on the
   first cell only as a smoke test (manual `--limit 1` flag) before proceeding to the full sample:
   `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs --task-id t0120_morph_generator_geometry_audit -- uv run python -u -m tasks.t0120_morph_generator_geometry_audit.code.dump_cells --limit 1`.
   Failure condition: if the first cell raises an exception or produces an empty `sections` list,
   STOP and debug `generate_fixed_morphology` invocation before processing all cells. Inspection
   requirement: open the resulting JSON entry for cell 1 and confirm at least 30 sections appear,
   the soma entry has `n3d() == 2`, and `soma_pt3d_xy_min == soma_pt3d_xy_max == (0.0, 0.0)` (the
   expected fingerprint of the t0092 fix).

7. **Create `code/run_checks.py` that produces `results/data/coordinate_consistency_checks.csv`.**
   Read the JSON dump from Step 6. For each cell, evaluate the three checks using `math.isclose`
   with `abs_tol=CHECK_ABS_TOL=1e-6` and `rel_tol=CHECK_REL_TOL=1e-9`:
   * **Check 1 (primary stem origin)**: iterate `cell.primary_dends` (from
     `MorphologyResult.primary_dends`), look up each section's `section_endpoints_xy[node.name]`
     start, assert
     `math.isclose(start_x, origin_xy[0], abs_tol=...) and math.isclose(start_y, origin_xy[1], abs_tol=...)`.
     Boolean AND across all primary stems.
   * **Check 2 (parent/child match)**: iterate `cell.all_dends`, skip primary stems (no parent in
     dendrite tree), and for each section look up `connectivity[node.name]` to find the parent name.
     Assert `child.start_xy ≈ parent.end_xy`. Boolean AND across all non-primary sections.
   * **Check 3 (synapse pt3d frame)**: iterate `cell.all_dends`, call the modified
     `_section_midpoint_xy(h=cell.h, section=sec)`. For each section, assert (a) the midpoint xy
     lies on the line segment from `python_start_xy` to `python_end_xy` within tolerance (use
     `abs((end_x - start_x) * (mid_y - start_y) - (end_y - start_y) * (mid_x - start_x)) < 1e-6` for
     cross-product = 0), and (b) the midpoint xy differs from `origin_xy` by no more than the
     cumulative dendrite path length from soma + a generous slack of `100.0 um` (coarse frame-shift
     sanity check that catches a `soma_offset` shift on the order of typical 20-30 um). Boolean AND
     across all dendrite sections.

   Also compute the soma-frame columns from REQ-7: `soma_origin_x = origin_xy[0]`,
   `soma_origin_y = origin_xy[1]`, `soma_pt3d_x_min`, `soma_pt3d_x_max`, `soma_pt3d_y_min`,
   `soma_pt3d_y_max`,
   `soma_frame_offset_um = sqrt((soma_origin_x - soma_pt3d_center_x)**2 + (soma_origin_y - soma_pt3d_center_y)**2)`
   (this is the **expected** mismatch from the t0092 patch, not a check failure; it should equal
   `|soma_offset_pd_um|` for every cell).

   Write to `COORDINATE_CONSISTENCY_CHECKS_CSV` with columns
   `cell_id, source_task, seed, generation, individual_idx, stratum_tag, soma_offset_pd_um, field_elongation_pd, branch_density_gradient_pd, primary_branch_pd_concentration, check1_primary_start: bool, check2_parent_child: bool, check3_synapse_frame: bool, n_primary_stems: int, n_non_primary_sections: int, n_dendrite_sections: int, max_check1_error_um: float, max_check2_error_um: float, max_check3_error_um: float, soma_origin_x, soma_origin_y, soma_pt3d_x_min, soma_pt3d_x_max, soma_pt3d_y_min, soma_pt3d_y_max, soma_frame_offset_um`.
   Use explicit dtypes per the data-analysis Planning Guidelines. Print stdout summary per cell:
   `"cell_id={...} check1={pass/fail} check2={pass/fail} check3={pass/fail} soma_frame_offset={...:.3f} (expected={|soma_offset|:.3f})"`
   plus an aggregate count: `"PASS counts: check1={...}/{N}, check2={...}/{N}, check3={...}/{N}"`.
   Satisfies REQ-4, REQ-5, REQ-6, REQ-7, REQ-9.

### Milestone C: Verdict and reporting (Steps 8-9)

8. **Create `code/build_answer_asset.py` that writes the one answer asset.** Read the CSV from Step
   7 and compute the pass counts. Apply the verdict logic from REQ-14:
   * If all three checks pass for all cells (60/60 total): verdict = "rendering-only artefact" and
     confidence = `"high"`.
   * If 1-3 isolated checks fail (i.e., on 1-3 cell+check pairs out of 60): verdict = "mostly
     consistent, isolated discrepancies on extreme-asymmetry cells; recommend per-cell follow-up"
     and confidence = `"medium"`.
   * If more than 3 checks fail: verdict = "real geometry bug detected -- framework decision needed
     before further NSGA-II runs" and confidence = `"low"`.

   Also include REQ-8: the answer's full-answer document narrative must explicitly cite
   `tasks/t0091_morphology_extended_nsga2_v1/code/trial_helpers.py` lines 64-178 (synapse bar
   arrival timing uses `(syn_xy - origin_xy)` projection on dendrite-only synapses) and the
   conclusion that the soma-frame split (Python `origin_xy = (soma_offset, 0)` vs NEURON soma pt3d
   `(0, 0)`) is benign **because no electrically-relevant code path reads soma pt3d for synapse
   placement**.

   Write `assets/answer/morphology-generator-geometry-consistency/details.json` v2 format matching
   the t0117 / t0118 precedent (see
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-truncated-cohort-artefact-test/details.json`).
   Fields: `spec_version: "2"`, `answer_id: "morphology-generator-geometry-consistency"`,
   `question: "Is the procedural morphology generator's asymmetry transform geometrically consistent across the 15-20 sampled cells?"`,
   `short_title:` (1-line verdict), `short_answer_path: "short_answer.md"`,
   `full_answer_path: "full_answer.md"`, `categories: ["compartmental-modeling"]`,
   `answer_methods: ["code-experiment"]`, `source_paper_ids: []`, `source_urls: []`,
   `source_task_ids: ["t0090_morphology_generator_diversity_test", "t0092_diagnose_morphology_generator_silence", "t0115_seed9354_no_autostop", "t0117_pooled_pca_cluster_factor_all_cells_4_seeds", "t0119_brainstorm_results_23"]`,
   `confidence:` (per the rule above), `created_by_task: "t0120_morph_generator_geometry_audit"`,
   `date_created: "2026-05-24"`.

   Write `assets/answer/morphology-generator-geometry-consistency/short_answer.md` with `## Answer`
   in 2-5 sentences directly stating the verdict (no inline citations, no hedging, begins with "Yes"
   or "No"). Write `full_answer.md` with all sections required by
   `meta/asset_types/answer/specification.md`: `## Short Answer`, `## Background`,
   `## Research Process`, `## Evidence from Existing Papers` (state "None -- audit is code-only"),
   `## Evidence from Internet Sources` (state "None"), `## Evidence from Prior Project Findings`
   (cite t0090 generator, t0092 fix, t0091 trial_helpers, t0115 rendering, t0117 pooled parquet,
   t0119 brainstorm), `## Evidence from Code or Experiments` (cite the three checks, the soma-frame
   measurement, and the per-cell CSV), `## Synthesis`, `## Limitations`, `## Sources` (with markdown
   reference link definitions for clickable inline citations). Run the answer verificator (or local
   fallback) and fix any errors. Satisfies REQ-8, REQ-13, REQ-14.

9. **Create `code/build_audit_gallery.py` that produces
   `results/images/geometry_audit_gallery.png`.** Use `matplotlib.use("Agg")` for headless
   rendering. Re-instantiate each sampled cell via `generate_fixed_morphology`. Render a grid (rows
   x cols = e.g., 5 x 4 = 20 panels, with unused panels blanked) where each panel:
   * Draws the soma as
     `matplotlib.patches.Circle(xy=cell.origin_xy, radius=params.soma_diameter_um / 2)` with edge
     color `black`, face color `lightgray`, alpha 0.7. **Do not** use the fixed `radius=6.0` from
     the t0115 renderer.
   * Draws every dendrite section from `section_endpoints_xy` as a line segment via
     `matplotlib.collections.LineCollection(linewidths=0.8, colors="tab:blue")`.
   * Draws the **primary stems** (sections in `cell.primary_dends`) as a separate
     `LineCollection(linewidths=2.0, colors="tab:red")` overlaid on top, so the soma->primary stem
     connection is visually unambiguous.
   * Draws a thin debug line (linewidth 0.5, color `black`, alpha 0.5) from `origin_xy` to each
     primary stem's `end_xy` to make any geometric gap immediately visible.
   * Sets per-panel xy bounds to a square centered on the cell's geometric center with half-width
     `max(x_max - x_min, y_max - y_min) * 0.6 + 15.0` (slightly more generous than t0115's
     `0.55 + 10.0`).
   * Adds a per-panel title in 8 pt font listing `cell_id`, `stratum_tag`, the four asymmetry
     parameters, and the three check pass/fail booleans (color-coded green/red).

   Save as `GEOMETRY_AUDIT_GALLERY_PNG` with `dpi=150`. Print stdout
   `"Saved gallery with {N} panels to {path}"`. Satisfies REQ-12.

**Metrics measurement note**: No registered project metric applies to this task. The four metrics
registered in `meta/metrics/` (`direction_selectivity_index`, `tuning_curve_hwhm_deg`,
`tuning_curve_reliability`, `tuning_curve_rmse`) all apply to electrical-simulation tasks measuring
directional tuning. This task performs no electrical simulation; the per-cell check pass/fail counts
are project-specific audit metrics that are not registered and therefore not written to
`results/metrics.json`. This is a **deliberate omission** explicitly documented here per the
planning skill's metric-coverage rule: the implementation agent should not invent a fake metric key.
The per-cell pass/fail booleans live in the CSV; the aggregate pass counts live in the answer
asset's short and full answer documents.

## Remote Machines

**None required.** This task runs entirely on the researcher's local Windows machine. No GPU is
needed because the audit performs no electrical simulation -- the NEURON DLL is monkey-patched to a
no-op via the bypass pattern copied from t0115. Total CPU time is ~1-2 hours for 15-20 cells x
generator invocation + pt3d dump + check evaluation + gallery rendering.

## Assets Needed

* **`procedural_dsgc_morphology_generator_fix`** library (created by
  `t0092_diagnose_morphology_generator_silence`) -- the patched generator with the soma-pt3d z-axis
  re-emission fix. Import path:
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`.
* **`procedural_dsgc_morphology_generator`** library (created by
  `t0090_morphology_generator_diversity_test`) -- transitive dependency providing
  `MorphologyParams`, `MorphologyResult`, `_apply_asymmetry`, `_materialise_neuron_sections`,
  `section_endpoints_xy`. Import path:
  `tasks.t0090_morphology_generator_diversity_test.code.morphology_params.MorphologyParams`.
* **t0117 pooled cells parquet** -- the 4431-cell sampling pool with full 68-d morphology +
  electrophys vectors and per-cell `morph_seed`. Source path:
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_all_cells.parquet`. Not a
  registered asset, but a stable data product from a completed task.
* **t0115 top-50 morphology PNG** -- the source of the "worst-looking" stratum hand-curation. Source
  path: `tasks/t0115_seed9354_no_autostop/results/images/top50_morphologies_seed9354.png`.
* **t0091 trial_helpers `_section_midpoint_xy`** -- copy source for Check 3.
* **t0092 `structural_dump.py` helpers** -- copy source for Step 5.
* **t0115 `build_top50_morphologies.py` rendering + DLL bypass + `_params_from_14d`** -- copy source
  for Step 5 and Step 9.
* **t0118 `stratified_sample.py` `_assign_quintile`** -- copy source for Step 3.

## Expected Assets

This task produces **1 answer asset**, matching the `expected_assets: {"answer": 1}` declaration in
`task.json`:

* **Asset type**: answer
* **Asset ID**: `morphology-generator-geometry-consistency`
* **Description**: One answer asset answering "Is the procedural morphology generator's asymmetry
  transform geometrically consistent across the 15-20 sampled cells?" with a conditional verdict
  (rendering-only artefact vs real geometry bug requiring framework decision). Uses v2 details.json
  format with `answer_methods: ["code-experiment"]`. Folder:
  `tasks/t0120_morph_generator_geometry_audit/assets/answer/morphology-generator-geometry-consistency/`
  containing `details.json`, `short_answer.md`, `full_answer.md`.

No other asset types are produced. The pt3d JSON dump, per-cell CSV, manifest CSV, and gallery PNG
are intermediate artefacts written under `results/data/` and `results/images/`, not registered
assets.

## Time Estimation

* **Research stages** (already complete): research_papers, research_internet, research_code -- no
  additional time needed.
* **Planning** (this stage): 20-30 minutes.
* **Implementation Milestone A (setup + sampling, Steps 1-4)**: 30-45 minutes (path constants,
  copying the stratified-sampler pattern, hand-curating 3 worst-looking cells from the t0115 PNG).
* **Implementation Milestone B (dump + checks, Steps 5-7)**: 1-2 hours (most of the engineering
  work: copying ~240 lines of helpers, writing ~150 lines of audit-specific glue, the smoke-test
  validation gate on cell 1).
* **Implementation Milestone C (verdict + gallery, Steps 8-9)**: 30-60 minutes (answer asset
  authoring, gallery rendering).
* **Local CPU wall-clock for the full pipeline**: ~1-2 hours additional once the code is written
  (15-20 cells x ~30-60 seconds per cell for generator invocation + pt3d dump + check evaluation +
  gallery rendering).
* **Validation + verificator runs**: 15-30 minutes (running `verify_plan`, `verify_answer_asset` or
  the local fallback, then fixing any issues).

**Total wall-clock estimate**: 4-6 hours including coding and execution.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `_section_midpoint_xy` raises on some degenerate dendrite section (n3d == 0) found in the sample | Medium | Blocks Check 3 evaluation for that cell | The modified copy raises explicitly per the research_code.md guidance; Check 3 records the failure as `False` for that section and continues; per-cell pass/fail in CSV captures it cleanly. No intervention needed -- a degenerate section is a real audit finding. |
| t0117 pooled parquet schema differs from what research_code.md describes (e.g., missing `morph_seed` or `source_task` columns) | Low | Blocks Step 4 sampling | Step 4 explicitly inspects the parquet schema first via `df.columns.tolist()` and `df.dtypes` printed to stdout; if expected columns are missing, fall back to grouping by `(seed, generation, individual_idx)` alone and recompute `morph_seed` deterministically from the row index per the t0117 conventions. If the parquet itself is missing, escalate via an intervention file. |
| Soma-frame split is NOT a benign artefact -- some other code path I haven't found reads soma pt3d for synapse placement | Low | Verdict swings to "real geometry bug" requiring re-run of every t0091-t0118 NSGA-II run | The audit is exactly designed to surface this. The full-answer narrative in Step 8 must explicitly enumerate the searched code paths (`grep` for `h.x3d`, `h.y3d` across `tasks/t009*/code/` and `tasks/t011*/code/`) so future readers can verify the search was exhaustive. If found, escalate via the verdict + a suggestion for a framework-level dedicated re-run task. |
| `generate_fixed_morphology` produces different cells on Windows vs the parquet was generated on (non-determinism risk) | Low | Per-cell checks could pass on a "different" cell than the NSGA-II saw | The t0092 docstring (lines 36-42) guarantees byte-identical cells for the same `(params, morph_seed)` pair. Verify on the first cell by running it twice and asserting all `section_endpoints_xy` values are bitwise identical; record the determinism check result in the audit's stdout log. If determinism fails, escalate via an intervention file. |
| Visual gallery is hard to read at 4x5 grid because cells with extreme asymmetry have very different xy ranges | Medium | Visual artefact diagnosis weakened | Per-panel auto-zoom with `half_width = max(x_max - x_min, y_max - y_min) * 0.6 + 15.0` adapts per cell. If still too dense, fall back to two galleries: one for extreme-asymmetry cells (3 cols x ceil(N/3) rows) and one for symmetric controls. |
| Worst-looking cells from t0115 PNG hand-curation are subjective | Medium | "WORST_LOOKING" stratum may be biased | Step 4 records the exact `(source_task, seed, generation, individual_idx)` tuples in `code/worst_looking_cells.csv` so the selection is reproducible; the full-answer narrative documents the selection criteria. If unclear, default to top-5 cells by Euclidean distance between `origin_xy` and dendrite-tree centroid (a quantitative proxy for the visual "disconnection"). |

## Verification Criteria

Each criterion includes the exact command to run and the expected observable output. The criteria
are designed to confirm both file existence and REQ coverage.

* **Plan verificator passes with zero errors.** Run:

  ```bash
  PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs \
    --task-id t0120_morph_generator_geometry_audit -- \
    uv run python -m arf.scripts.verificators.verify_plan \
    t0120_morph_generator_geometry_audit
  ```

  Expected: exit code 0, no `PL-E*` errors. Warnings are acceptable if they reflect deliberate
  omissions (e.g., no `--limit` baseline gate for the smoke test in Step 6, because the operation is
  local-CPU and small-N).

* **All 15-20 sampled cells appear in the manifest CSV with all required columns.** Run:

  ```bash
  PYTHONIOENCODING=utf-8 uv run python -c \
    "import pandas as pd; df = pd.read_csv('tasks/t0120_morph_generator_geometry_audit/results/data/sampled_cell_manifest.csv'); print(f'n_rows={len(df)} unique_strata={df.stratum_tag.nunique()} cols={list(df.columns)}')"
  ```

  Expected: `15 <= n_rows <= 20`, `unique_strata >= 6` (all StratumTag values except possibly
  `ELONGATION_BOTTOM` if no eligible cells exist), columns include `cell_id`, `stratum_tag`, all 14
  morphology parameter names, plus `dsi` and `pd_rate_hz`. Confirms REQ-1 and REQ-10.

* **All 3 checks evaluated for every sampled cell, with explicit pass/fail booleans in CSV.** Run:

  ```bash
  PYTHONIOENCODING=utf-8 uv run python -c \
    "import pandas as pd; df = pd.read_csv('tasks/t0120_morph_generator_geometry_audit/results/data/coordinate_consistency_checks.csv'); print(df[['cell_id','check1_primary_start','check2_parent_child','check3_synapse_frame','soma_frame_offset_um']].to_string())"
  ```

  Expected: one row per sampled cell, all three check columns boolean (no NaN), and
  `soma_frame_offset_um` numerically close to `|soma_offset_pd_um|` for every cell (the expected
  fingerprint of the t0092 z-axis fix). Confirms REQ-4, REQ-5, REQ-6, REQ-7, REQ-9.

* **Pt3d JSON dump exists and contains per-cell `sections` arrays with both Python and NEURON
  coordinates.** Run:

  ```bash
  PYTHONIOENCODING=utf-8 uv run python -c \
    "import json; d = json.loads(open('tasks/t0120_morph_generator_geometry_audit/results/data/section_endpoints_dump.json').read()); print(f'n_cells={len(d)} first_cell_keys={list(d[0].keys())} first_cell_n_sections={len(d[0][\"sections\"])}')"
  ```

  Expected: `n_cells == 15..20`, `first_cell_keys` includes `origin_xy`, `soma_pt3d_xy_min`,
  `soma_pt3d_xy_max`, `soma_frame_offset_um`, `sections`, and each section entry contains
  `python_start_xy`, `python_end_xy`, `neuron_pt3d`. Confirms REQ-2, REQ-3, REQ-11.

* **Visual diagnostic gallery PNG exists and is non-empty.** Run:

  ```bash
  PYTHONIOENCODING=utf-8 uv run python -c \
    "from pathlib import Path; p = Path('tasks/t0120_morph_generator_geometry_audit/results/images/geometry_audit_gallery.png'); print(f'exists={p.exists()} size_bytes={p.stat().st_size if p.exists() else 0}')"
  ```

  Expected: `exists=True`, `size_bytes >= 50000` (a 4x5 panel grid at dpi=150 should be at least
  ~50KB; smaller suggests a rendering failure). Confirms REQ-12.

* **One answer asset exists at the expected path with v2 details.json and passes the answer
  verificator.** Run:

  ```bash
  PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs \
    --task-id t0120_morph_generator_geometry_audit -- \
    uv run python -m meta.asset_types.answer.verificator \
    tasks/t0120_morph_generator_geometry_audit/assets/answer/morphology-generator-geometry-consistency
  ```

  Expected: exit code 0, `details.json` has `spec_version: "2"`,
  `answer_id: "morphology-generator-geometry-consistency"`, `answer_methods: ["code-experiment"]`,
  `confidence` in `{high, medium, low}`, `source_task_ids` includes t0090, t0092, t0115, t0117,
  t0119. If the canonical verificator is unavailable on this branch, fall back to the local check
  used by t0117 / t0118 (`verify_answers_local.py`). Confirms REQ-8, REQ-13, REQ-14.

* **Requirement coverage check.** Manually grep the plan and outputs to confirm every `REQ-*` ID
  from the checklist appears in at least one step description and is satisfied by at least one
  produced artefact. Run:

  ```bash
  PYTHONIOENCODING=utf-8 uv run python -c \
    "import re; text = open('tasks/t0120_morph_generator_geometry_audit/plan/plan.md').read(); reqs = set(re.findall(r'REQ-\\d+', text)); print(sorted(reqs, key=lambda s: int(s.split('-')[1])))"
  ```

  Expected: prints `['REQ-1', 'REQ-2', ..., 'REQ-14']` -- every requirement ID is present. Confirms
  the entire Task Requirement Checklist is wired to steps and outputs.
