---
spec_version: "2"
task_id: "t0120_morph_generator_geometry_audit"
date_completed: "2026-05-24"
status: "complete"
---
# Results Detailed: Morphology Generator Geometry Audit

## Summary

Audited the procedural DSGC morphology generator on 20 visually-diverse cells stratified across the
four asymmetry-parameter axes plus symmetric controls. All three coordinate-consistency checks pass
(60 / 60). The soma-frame split introduced by the t0092 z-axis pt3d patch is **benign**; the
rendering artefact in t0115's top-50 morphology grid is **not** a geometry bug; prior 68-d
morphology-extended NSGA-II runs (t0091, t0099, t0102, t0104, t0106, t0112-t0115, t0118) are **NOT
invalidated**. `t0122_dsi_cytoplasm_volume_nsga2` is unblocked.

## Methodology

* **Machine**: local Windows 11 EPYC; no remote machines provisioned.
* **Runtime**: ~28 min total (sample cells <1s; dump 20 cells ~5-10 min; run checks <1s; render
  gallery ~3 min; write answer asset <1s; verificators <1 min).
* **Timestamps**: implementation step started 2026-05-23T23:57:39Z, completed 2026-05-24T00:25:00Z
  (1647s).
* **Workers**: 1 (single-process; NEURON DLL bypass active so the generator runs without compiled
  MOD files).
* **Data source**: t0117 pooled parquet (4431 cells across GA seeds 44/77/7755/9354).
* **Generator entry point**:
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`.

### Sampling Strategy

20 cells stratified across 7 strata, drawn deterministically (numpy seed=42) from the t0117 pooled
parquet using `code/stratified_sampler.py` (decile thresholds adapted from t0118's quintile
pattern):

| Stratum | Cells | Selection rule |
| --- | --- | --- |
| `SOMA_OFFSET_TOP` | 3 | top decile of abs(soma_offset_pd_um) |
| `ELONGATION_TOP` | 2 | top decile of `field_elongation_pd` |
| `ELONGATION_BOTTOM` | 1 | bottom decile of `field_elongation_pd` |
| `BRANCH_DENSITY_TOP` | 3 | top decile of abs(branch_density_gradient_pd) |
| `PRIMARY_CONCENTRATION_TOP` | 3 | top decile of `primary_branch_pd_concentration` (kappa) |
| `WORST_LOOKING` | 4 | hand-curated list in `code/worst_looking_cells.csv` from t0115 PNG |
| `SYMMETRIC_CONTROL` | 4 | all 4 asymmetry parameters within +/- 1 SD of defaults |

### Coordinate-Consistency Checks

For each sampled cell, the audit ran three checks against the t0092-fixed generator output:

1. **Check 1 -- primary stem origin alignment**:
   `all(close(section.start_xy, origin_xy) for section in primary_dends)`. Tolerance 0.1 um.
2. **Check 2 -- parent / child endpoint match**: for each non-primary dendrite section, walk the
   parent chain and assert `child.start_xy == parent.end_xy`. Tolerance 0.1 um.
3. **Check 3 -- synapse pt3d frame consistency**: for each dendrite section, read
   `h.x3d(mid), h.y3d(mid)` from NEURON, assert it lies on the line from `section.start_xy` to
   `section.end_xy` (in Python coords). Lateral deviation threshold 0.1 um.

### Soma-Frame Diagnostic (REQ-7)

An additional diagnostic computes `soma_frame_offset_um` = L2 distance between Python `origin_xy`
and NEURON soma pt3d centroid. If the t0092 z-axis pt3d fix is the source of the visual artefact,
`soma_frame_offset_um == |soma_offset_pd_um|` exactly.

## Metrics

* Cells sampled: **20**.
* Coordinate-consistency checks passed: **60 / 60** (100%).
* Check 1 max error: **0.0 um** across all primary stems of all 20 cells.
* Check 2 max error: **0.0 um** across all non-primary dendrite sections.
* Check 3 max lateral deviation: **19.6 nm** = 1.96e-5 um (float noise; threshold 0.1 um => passes
  by four orders of magnitude).
* `soma_frame_offset_um` range: **3.02 um -- 149.96 um**; equals `|soma_offset_pd_um|` exactly (max
  residual **0.000000 um** over all 20 cells).

## Visualizations

![Geometry audit gallery — 5x4 panel grid; primary stems highlighted in red linewidth 2.0; soma circle scaled to `soma_diameter_um / 2`; debug line from `origin_xy` to each primary-stem tip.](images/geometry_audit_gallery.png)

The gallery shows the same 20 cells the audit instrumented. The primary-stem-to-soma connection is
unambiguous in every panel because (a) primary stems are drawn in red at 2x linewidth, (b) the soma
circle is sized to the actual `soma_diameter_um` rather than the fixed 6 px used in t0115's top-50
grid, and (c) a thin grey debug line is drawn from `origin_xy` to each primary stem's tip so the
connection is visible even when the primary stem itself is short. Compare with
`tasks/t0115_seed9354_no_autostop/results/images/top50_morphologies_seed9354.png` where the same
cells (under different rendering conventions) appear soma-disconnected.

## Analysis

### Why the soma appears disconnected in t0115's grid

The t0115 (and t0112 / t0114 / earlier lineage) `build_top50_morphologies.py` uses three rendering
conventions that conspire to make the soma look disconnected on asymmetric cells:

* `Circle(radius=6.0)` -- fixed soma radius in axis-units (um); on a 300 um panel, 6 um is ~2% of
  the panel width.
* `LineCollection(linewidths=0.4)` -- thin dendrite strokes; primary stems often <30 um long; at 0.4
  px they nearly vanish.
* Auto-zoom via `ax.set_xlim(cx - half, cx + half)` covering both `geom.soma_xy` and the dendrite
  bounding box; for cells with `|soma_offset_pd_um| > 100` and elongated dendrite fields, the panel
  becomes wide enough that the soma is in one corner and the dendrite tree extends to the other.

When the audit re-renders the same cells with `Circle(radius=soma_diameter_um / 2)` (typically 6-9
um, but proportionally sized), `LineCollection(linewidths=0.5-0.6)`, primary stems in contrasting
red `linewidth=2.0`, and a debug line from `origin_xy` to each primary-stem tip, every panel shows
an unambiguous connection.

### The benign two-frame soma split

`tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py` (lines 61-75)
calls `h.pt3dclear()` on the soma section and re-emits two pt3d points along the **z-axis**:
`(0, 0, 0, d_target)` and `(0, 0, soma_diameter_um, d_target)`. This was introduced to fix the t0090
degenerate-zero-area bug where the soma's two pt3d points coincided in xy and NEURON computed
cumulative pt3d distance ~0.

The downstream consequence is two coordinate frames for the soma:

* **Python frame**: `origin_xy = (params.soma_offset_pd_um, 0)` (set by `_apply_asymmetry`).
* **NEURON frame** (pt3d, as the simulator sees it): soma pt3d at `(0, 0, *)` regardless of
  `soma_offset_pd_um`.

This would matter if any electrically-relevant code read the **soma's** NEURON pt3d xy to compute
synaptic arrival times. The audit confirms this never happens:

1. **Synapse placement**: SAC synapses (AChE / GABA / NMDA) are placed only on **dendrite** sections
   in the t0091 / t0118 protocol via `place_synapses` and inherit the dendrite section's pt3d
   midpoint via `_section_midpoint_xy`. Dendrite pt3d is faithfully written in the post-asymmetry
   frame, matching `origin_xy`.
2. **Bar arrival-time projection**: `_bar_arrival_times(syn_xy, origin_xy, direction_deg)` in
   `tasks/t0091_morphology_extended_nsga2_v1/code/trial_helpers.py` projects `(syn_xy - origin_xy)`
   onto the bar direction. Both `syn_xy` and `origin_xy` are in the same Python frame; the
   `soma_offset` term cancels.
3. **Electrical topology**: `sec.connect()` is independent of pt3d xy.

Therefore the two-frame soma split is **deliberate, contained to the soma section, and electrically
benign**.

## Limitations

* The audit instruments 20 of 4431 pooled cells (0.5%). Stratification covers the asymmetry
  parameter extremes and the "worst-looking" set hand-curated from the t0115 PNG; if a specific
  failure mode requires a parameter combination outside the sampled strata, this audit would miss
  it. The 60/60 PASS result with max errors well below thresholds makes this risk small.
* The audit verifies geometric consistency, not the **correctness** of the asymmetry transform
  itself (i.e., whether `field_elongation_pd > 1` is the biologically right way to encode PD
  elongation). That is a separate biological-plausibility question; see the t0097 multi-objective
  optimisation answer asset.
* The `_section_midpoint_xy` strict implementation raises on `h.n3d() == 0` (degenerate sections),
  unlike the t0091 lineage which silently returns `(0.0, 0.0)`. No cells in the sampled set tripped
  this; if the production code ever passes a degenerate section, the audit's strict check would fail
  where the production code would silently miscompute. Out of scope for this audit -- noted as a
  follow-up suggestion.

## Files Created

* `code/paths.py`, `code/constants.py` -- path and constant declarations.
* `code/stratified_sampler.py` -- decile-based stratified sampling helper.
* `code/sample_cells.py` -- driver: load t0117 parquet, sample 20 cells, write manifest.
* `code/dump_helpers.py` -- `Pt3dPoint`, `SectionDump`, `CellDump` dataclasses + strict
  `_section_midpoint_xy_strict`.
* `code/dump_cells.py` -- per-cell dump driver (instantiates morphology, reads Python + NEURON
  pt3d).
* `code/run_checks.py` -- runs the 3 consistency checks and writes the per-cell CSV.
* `code/build_audit_gallery.py` -- renders the 5x4 panel gallery PNG.
* `code/build_answer_asset.py` -- generates the answer asset details.json + short_answer.md +
  full_answer.md.
* `code/worst_looking_cells.csv` -- hand-curated 6-cell list from t0115 visual inspection.
* `results/data/sampled_cell_manifest.csv` -- 20 rows x 22 columns (cell keys, stratum tag, 14
  morphology params, DSI, PD rate).
* `results/data/section_endpoints_dump.json` -- 2.0 MB; per-cell pt3d dump in both Python and NEURON
  frames.
* `results/data/coordinate_consistency_checks.csv` -- 20 rows x 29 columns (3 check pass/fail + 5
  soma-frame columns + per-check max-error stats + asymmetry parameter values + metadata).
* `results/images/geometry_audit_gallery.png` -- 958 KB; 5x4 panel grid.
* `assets/answer/morphology-generator-geometry-consistency/details.json`, `short_answer.md`,
  `full_answer.md` -- 1 answer asset, confidence high.

## Verification

* `verify_research_code` -- PASSED (0 errors, 0 warnings).
* `verify_plan` -- PASSED (0 errors, 0 warnings).
* Local answer-asset verificator (`meta.asset_types.answer.verificator`) -- PASSED (0 errors, 0
  warnings).
* `ruff check` on `code/` -- PASSED (10 files clean).
* `ruff format` on `code/` -- PASSED (10 files unchanged).
* `mypy -p tasks.t0120_morph_generator_geometry_audit.code` -- PASSED.
* Per-cell pass/fail (`coordinate_consistency_checks.csv`): 60 / 60 PASS, 0 FAIL.

## Task Requirement Coverage

The task description in `tasks/t0120_morph_generator_geometry_audit/task_description.md` (the
brainstorm-23 commission) states:

> "Audit procedural morphology generator: verify primary stems start at origin_xy, parent/child
> endpoint match, and synapse pt3d xy frame matches origin_xy across 15-20 visually-diverse cells.
> Gates downstream NSGA-II."

Plan REQ-* items (from `plan/plan.md` "Task Requirement Checklist"):

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Sample 15-20 visually-diverse cells stratified across asymmetry-parameter extremes plus symmetric controls | Done | `results/data/sampled_cell_manifest.csv` (20 cells, 7 strata) |
| REQ-2 | Each cell instantiated via `generate_fixed_morphology` with NEURON DLL bypass | Done | `code/dump_cells.py` + per-cell entries in `section_endpoints_dump.json` |
| REQ-3 | Per-section dump contains both Python and NEURON pt3d xy | Done | `section_endpoints_dump.json` section schema |
| REQ-4 | Check 1 (primary stem `start_xy ~= origin_xy`) evaluated for all primary stems of all cells | Done | `check1_primary_start` column; 20/20 PASS |
| REQ-5 | Check 2 (child `start_xy ~= parent.end_xy`) evaluated for all non-primary sections | Done | `check2_parent_child` column; 20/20 PASS |
| REQ-6 | Check 3 (NEURON synapse midpoint frame consistency via strict `_section_midpoint_xy`) | Done | `check3_synapse_frame` column; 20/20 PASS |
| REQ-7 | `soma_origin_x/y`, `soma_pt3d_x/y_min/max`, `soma_frame_offset_um` columns; expected fingerprint `soma_frame_offset_um ~= | soma_offset_pd_um | ` |
| REQ-8 | Narrative analytic argument that the two-frame soma split is benign for bar-arrival timing | Done | `full_answer.md` Evidence-from-Code section + this file's Analysis section |
| REQ-9 | Per-cell pass/fail CSV | Done | `results/data/coordinate_consistency_checks.csv` |
| REQ-10 | Sampled-cell manifest CSV | Done | `results/data/sampled_cell_manifest.csv` |
| REQ-11 | Full pt3d JSON dump | Done | `results/data/section_endpoints_dump.json` (2.0 MB) |
| REQ-12 | Visual diagnostic gallery PNG (15-20 panels at 2x t0115's size, primary-stem highlight, soma circle scaled to `soma_diameter_um`, debug origin-to-primary-tip line) | Done | `results/images/geometry_audit_gallery.png` |
| REQ-13 | 1 answer asset answering the question | Done | `assets/answer/morphology-generator-geometry-consistency/` |
| REQ-14 | Unambiguous verdict: "rendering-only" or "real geometry bug" | Done | Answer asset; verdict is "rendering-only", confidence high |
