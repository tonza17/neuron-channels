# ✅ Morphology generator geometry audit (15-20 cells)

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0120_morph_generator_geometry_audit` |
| **Status** | ✅ completed |
| **Started** | 2026-05-23T23:22:10Z |
| **Completed** | 2026-05-24T00:45:00Z |
| **Duration** | 1h 22m |
| **Dependencies** | [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0119_brainstorm_results_23`](../../../overview/tasks/task_pages/t0119_brainstorm_results_23.md) |
| **Task types** | `data-analysis`, `answer-question` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md) |
| **Expected assets** | 1 answer |
| **Step progress** | 9/12 |
| **Task folder** | [`t0120_morph_generator_geometry_audit/`](../../../tasks/t0120_morph_generator_geometry_audit/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0120_morph_generator_geometry_audit/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0120_morph_generator_geometry_audit/task_description.md)*

# Morphology Generator Geometry Audit (15-20 cells)

## Motivation

In t0115's `top50_morphologies_seed9354.png` and earlier seed-77 / seed-7755 morphology grids,
several panels show the soma circle appearing far away from the dendrite tree with apparent
empty space between them. The researcher flagged this as a possible geometry bug: if the soma
is genuinely disconnected from the dendrites in the procedural generator
(`tasks/t0090_morphology_generator_diversity_test/code/generator.py`), every 68-d
morphology-extended NSGA-II result from t0091 onwards (t0091, t0099, t0102, t0104, t0106,
t0112-t0115) could be electrically invalid and would need to be re-run.

A preliminary code trace in brainstorm session 23 suggests the issue is most likely a
rendering artefact (small soma circle, thin connecting primary stem, auto-zoomed bounding box
on extreme asymmetric cells), and that:

* NEURON electrical topology is `sec.connect()`-based and indifferent to xy coordinates.
* Synapse pt3d xy and `origin_xy` are written by the same `_materialise_neuron_sections`
  function, so the bar-arrival-time projection `(syn_xy - origin_xy)` is computed in a
  self-consistent frame.

But this trace must be empirically verified before any new NSGA-II optimisation runs. The
researcher selected this as the gating task for the post-t0118 wave.

## Scope

Sample 15-20 cells stratified across the asymmetry-parameter extremes that drive the visual
artefact, plus symmetric controls. Dump the full `section_endpoints_xy` and NEURON
`h.x3d/h.y3d` pt3d for each cell. Verify three properties analytically and visually for each
cell:

1. **Primary stems start at `origin_xy`**: for every primary dendrite section, `start_xy ==
   origin_xy` (within float tolerance).
2. **Parent / child endpoint match**: for every non-primary dendrite section, `child.start_xy
   == parent.end_xy` (within float tolerance).
3. **Synapse-vs-soma coordinate frame consistency**: place a test SAC synapse on each section,
   read `h.x3d(mid), h.y3d(mid)`, and confirm it is in the same coordinate frame as
   `origin_xy` (no offset, no scaling mismatch).

## Cells to Sample (15-20 total, stratified)

Sample cells from the pooled Pareto fronts of t0091, t0099, t0112, t0114, t0115 across these
strata:

* 3 cells with high `|soma_offset_pd_um|` (top decile of the pooled distribution).
* 3 cells with extreme `field_elongation_pd` (top and bottom deciles, 1-2 each).
* 3 cells with extreme `branch_density_gradient_pd` (top decile by absolute value).
* 3 cells with high `primary_branch_pd_concentration` (top decile, von Mises kappa).
* 3 cells flagged visually as "worst-looking" by inspection of the t0115 top-50 PNG.
* 3-5 symmetric controls with all 4 asymmetry parameters near their BEDB_BASE_POINT defaults
  (soma_offset = 0, field_elongation = 1, branch_density_gradient = 0,
  primary_branch_pd_concentration = 0).

## Approach

1. **Sample cells**: load the pooled cells parquet from t0117 (4431 cells), compute per-cell
   stratification keys from the 14-d morphology subvector, sample 15-20 cells across the
   strata above.
2. **Dump generator coords**: for each sampled cell, instantiate the morphology via
   `generate_fixed_morphology` (matching the lineage convention), monkey-patch the NEURON DLL
   loader, extract `section_endpoints_xy`, `origin_xy`, and per-section `h.x3d/h.y3d/h.z3d`
   for every pt3d.
3. **Coordinate-consistency checks** (analytic):
   * For every primary dendrite section: `assert close(section.start_xy, origin_xy)`.
   * For every non-primary section: walk the parent chain, assert child.start_xy close to
     parent.end_xy at each level.
   * For each section, place a temporary `ExpSyn` at midpoint, read `h.x3d/h.y3d` of the
     midpoint pt3d, assert it falls on the line from `section.start_xy` to `section.end_xy`.
4. **Per-cell pass/fail CSV**: write a CSV with one row per cell, columns for each of the
   three checks (pass/fail), the asymmetry-parameter values, and the visual stratum tag.
5. **Visual diagnostic gallery**: re-render each cell at 2x larger panel with explicit
   primary-stem highlight (line-width 2.0, contrasting color) and a soma circle scaled to
   `soma_diameter_um` (not the fixed 6 px). Add a thin debug line from `origin_xy` to each
   primary stem's `end_xy` if the primary stem origin would otherwise be invisible. Save as
   `results/images/geometry_audit_gallery.png`.
6. **Answer asset**: write one answer asset answering "Is the procedural morphology
   generator's asymmetry transform geometrically consistent across the 15-20 sampled cells?"
   with conditional verdicts: (a) all 3 checks pass for all sampled cells -> rendering-only
   issue, no re-runs needed; (b) any check fails -> framework-level decision needed before
   further NSGA-II.

## Expected Outputs

* `results/data/sampled_cell_manifest.csv` -- which cells were sampled, stratum tag,
  asymmetry-parameter values.
* `results/data/coordinate_consistency_checks.csv` -- per-cell pass/fail for each of the 3
  checks.
* `results/data/section_endpoints_dump.json` -- full pt3d dump per cell for forensic analysis.
* `results/images/geometry_audit_gallery.png` -- visual diagnostic gallery.
* `assets/answer/morphology-generator-geometry-consistency/` -- 1 answer asset with the
  verdict.
* `results/results_summary.md` and `results/results_detailed.md` with the verdict and per-cell
  table.

## Budget

Local CPU only, no remote machines. Estimate <$0.10 (essentially $0 -- a few CPU hours).

## Dependencies

* `t0090_morphology_generator_diversity_test` -- provides the procedural generator.
* `t0092_diagnose_morphology_generator_silence` -- provides the `generate_fixed_morphology`
  wrapper with the soma-area patch.
* `t0115_seed9354_no_autostop` (or `t0117`) -- provides the pooled cells parquet for sampling.
* `t0119_brainstorm_results_23` -- commissions this task.

## Verification Criteria

* All 3 coordinate-consistency checks defined and run for every sampled cell.
* Per-cell pass/fail CSV exists with one row per cell.
* Visual diagnostic gallery saved and embedded in `results_detailed.md`.
* Answer asset passes `verify_answer_asset` (or the local `verify_answers_local.py` fallback
  used by recent tasks).
* Verdict in the results summary unambiguously states either "rendering-only" or "real
  geometry bug requires framework decision".

## Cross-References

* Researcher concern raised in `t0119_brainstorm_results_23/logs/session_log.md`.
* Preliminary code trace performed in the brainstorm session covering `_apply_asymmetry`
  (`generator.py` lines 333-355) and `_section_midpoint_xy` (`trial_helpers.py` line 160).

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Is the procedural morphology generator's asymmetry transform geometrically consistent across the 15-20 sampled cells, and do its results invalidate prior NSGA-II runs?](../../../tasks/t0120_morph_generator_geometry_audit/assets/answer/morphology-generator-geometry-consistency/) | [`full_answer.md`](../../../tasks/t0120_morph_generator_geometry_audit/assets/answer/morphology-generator-geometry-consistency/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>Re-render t0112 / t0114 / t0115 top-50 morphology grids with
t0120's rendering conventions (correction)</strong> (S-0120-01)</summary>

**Kind**: technique | **Priority**: medium

t0120 confirmed the soma-disconnect visual artefact in t0115's top50_morphologies_seed9354.png
(and the seed-44/77/7755 analogues from t0106/t0112/t0114) is rendering-only, driven by three
conventions in build_top50_morphologies.py: fixed Circle(radius=6.0) soma (too small vs
typical 100-150 um soma_offset_pd_um), LineCollection(linewidths=0.4) primary stems (visually
negligible), and auto-zoom that amplifies asymmetry. Concrete action: regenerate the four PNGs
using t0120's conventions (Circle(radius=soma_diameter_um/2), tab:red primary stems at
linewidth 2.0, optional debug line from origin_xy to each primary-stem tip), file corrections/
overlays at the new chart paths, and add a README noting the originals were not
geometry-wrong. Broader than S-0115-05 (which targets only t0114's dots-only artefact); the
two can be merged into one correction task. Recommended task types: correction.

</details>

<details>
<summary><strong>Replace lineage `_section_midpoint_xy` silent-(0,0) fallback with
t0120's strict raise-on-n3d==0 version</strong> (S-0120-02)</summary>

**Kind**: library | **Priority**: medium

t0120 ships a strict `_section_midpoint_xy_strict` in `code/dump_helpers.py` that raises
`RuntimeError('degenerate section: h.n3d() == 0')` instead of silently returning `(0.0, 0.0)`
(lineage behaviour in `tasks/t0091_morphology_extended_nsga2_v1/code/trial_helpers.py` lines
160-178, copied into every NSGA-II task t0091-t0118). The silent fallback is dangerous: if a
degenerate dendrite section ever appears, every synapse on that section would be placed at the
world origin and the bar arrival-time projection would be silently wrong by tens of
micrometres. The 20-cell t0120 audit never tripped the strict raise but covers only 0.5% of
the t0117 pool. Concrete action: package the strict version as a shared library (or extend
S-0090-07's generator-promotion path) with a deprecation shim on lineage callsites so future
NSGA-II tasks (incl. t0122) raise loudly. Recommended task types: write-library.

</details>

<details>
<summary><strong>Add a degenerate-section detector to the NSGA-II evaluation loop
(flag cells with any h.n3d() == 0 section)</strong> (S-0120-03)</summary>

**Kind**: library | **Priority**: low

Out of scope for t0120 but flagged during it: the procedural DSGC generator could in principle
produce dendrite sections whose pt3d count is zero (degenerate stubs) under combinations of
asymmetry knobs not covered by existing t0092 / t0120 tests. Such sections would silently
corrupt synapse placement and bar arrival timing under the lineage `_section_midpoint_xy` (see
S-0120-02). Concrete action: extend the NSGA-II eval loop (used by t0122 and future NSGA-II
tasks) with a one-line check after `generate_fixed_morphology`: `for sec in cell.all_dends:
assert int(cell.h.n3d(sec=sec)) > 0`. If the assertion fires, mark the individual as
infeasible (constraint violation) and record the failing 14-d morphology vector so the
generator can be patched. Pairs naturally with S-0092-05 (generator regression battery) and
S-0120-02. Recommended task types: write-library, infrastructure-setup.

</details>

<details>
<summary><strong>Whole-pool geometry audit: scale t0120's 20-cell sample up to all
4431 t0117 cells (background batch)</strong> (S-0120-04)</summary>

**Kind**: evaluation | **Priority**: low

t0120 verified geometry consistency on 20 cells stratified across asymmetry-parameter extremes
plus symmetric controls (0.5% of the t0117 pooled pool); 60 / 60 checks passed with max errors
four orders below threshold. A whole-pool audit would surface any rare combination of the 14
morphology knobs that triggers a frame mismatch outside the sampled strata. Concrete action:
reuse `code/dump_cells.py` and `code/run_checks.py` from t0120; iterate over all 4431 t0117
cells (skip per-cell pt3d JSON dump to keep disk bounded; retain only the per-cell check
pass/fail row); write a single coordinate_consistency_checks_full.csv and a short summary
stating the count of any cell failing any check. Runs in background (~12 CPU hours
single-process); cost effectively $0. Low priority because the stratified sample already
covers realistic failure modes; this is defence-in-depth. Recommended task types:
data-analysis.

</details>

## Research

* [`research_code.md`](../../../tasks/t0120_morph_generator_geometry_audit/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0120_morph_generator_geometry_audit/results/results_summary.md)*

--- spec_version: "1" task_id: "t0120_morph_generator_geometry_audit" date_completed:
"2026-05-24" status: "complete" ---
# Results Summary: Morphology Generator Geometry Audit

## Summary

Audited the procedural DSGC morphology generator on 20 cells stratified across
asymmetry-parameter extremes plus symmetric controls. All three coordinate-consistency checks
pass for every cell (60/60). The deliberate soma-frame split introduced by the t0092 z-axis
pt3d patch is **benign**; prior 68-d morphology-extended NSGA-II results (t0091, t0099, t0102,
t0104, t0106, t0112-t0115, t0118) are NOT invalidated. The visual disconnect in t0115's top-50
morphology grid is a rendering-only artefact. **t0122_dsi_cytoplasm_volume_nsga2 is
unblocked.**

## Metrics

* **Cells sampled**: **20** across 7 strata (SOMA_OFFSET_TOP 3, ELONGATION_TOP 2,
  ELONGATION_BOTTOM 1, BRANCH_DENSITY_TOP 3, PRIMARY_CONCENTRATION_TOP 3, WORST_LOOKING 4,
  SYMMETRIC_CONTROL 4) from the t0117 pooled parquet (4431 cells, seeds 44/77/7755/9354).
* **Coordinate-consistency checks passed**: **60 / 60** (3 checks per cell x 20 cells).
* **Check 1 max error** (primary stem start_xy vs origin_xy): **0.0 um** across all primary
  stems of all 20 cells.
* **Check 2 max error** (child start_xy vs parent end_xy): **0.0 um** across all non-primary
  dendrite sections.
* **Check 3 max lateral deviation** (NEURON midpoint pt3d vs Python section line on
  dendrites): **19.6 nm** (1.96e-5 um) -- pure float-arithmetic noise, **four orders below the
  0.1 um audit threshold**.
* **soma_frame_offset_um range**: **3.02 um** (symmetric controls) to **149.96 um** (extreme
  soma_offset_pd_um cells); exactly equals `|soma_offset_pd_um|` per cell (max residual
  **0.000000 um**).
* **Files produced**: 1 answer asset, 1 PNG gallery (958 KB, 5x4 grid), 1 per-cell pass/fail
  CSV, 1 2.0-MB section-endpoints JSON forensic dump, 9 Python source files.

## Verification

* `verify_research_code` -- PASSED (0 errors, 0 warnings).
* `verify_plan` -- PASSED (0 errors, 0 warnings).
* Local answer-asset verification (`meta.asset_types.answer.verificator`) -- PASSED (0 errors,
  0 warnings).
* `ruff check`, `ruff format`, `mypy -p tasks.t0120_morph_generator_geometry_audit.code` --
  all PASSED on 10 task code files.
* Per-cell pass/fail (`coordinate_consistency_checks.csv`): 60 / 60 PASS, 0 FAIL.

## Verdict

**Rendering-only artefact.** No NSGA-II re-runs needed. Prior 68-d morphology-extended NSGA-II
lineage (t0091, t0099, t0102, t0104, t0106, t0112, t0114, t0115, t0118) remains valid. The
brainstorm-session-23 gating condition for `t0122_dsi_cytoplasm_volume_nsga2` is satisfied;
that task may now proceed.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0120_morph_generator_geometry_audit/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0120_morph_generator_geometry_audit" date_completed:
"2026-05-24" status: "complete" ---
# Results Detailed: Morphology Generator Geometry Audit

## Summary

Audited the procedural DSGC morphology generator on 20 visually-diverse cells stratified
across the four asymmetry-parameter axes plus symmetric controls. All three
coordinate-consistency checks pass (60 / 60). The soma-frame split introduced by the t0092
z-axis pt3d patch is **benign**; the rendering artefact in t0115's top-50 morphology grid is
**not** a geometry bug; prior 68-d morphology-extended NSGA-II runs (t0091, t0099, t0102,
t0104, t0106, t0112-t0115, t0118) are **NOT invalidated**. `t0122_dsi_cytoplasm_volume_nsga2`
is unblocked.

## Methodology

* **Machine**: local Windows 11 EPYC; no remote machines provisioned.
* **Runtime**: ~28 min total (sample cells <1s; dump 20 cells ~5-10 min; run checks <1s;
  render gallery ~3 min; write answer asset <1s; verificators <1 min).
* **Timestamps**: implementation step started 2026-05-23T23:57:39Z, completed
  2026-05-24T00:25:00Z (1647s).
* **Workers**: 1 (single-process; NEURON DLL bypass active so the generator runs without
  compiled MOD files).
* **Data source**: t0117 pooled parquet (4431 cells across GA seeds 44/77/7755/9354).
* **Generator entry point**:
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`.

### Sampling Strategy

20 cells stratified across 7 strata, drawn deterministically (numpy seed=42) from the t0117
pooled parquet using `code/stratified_sampler.py` (decile thresholds adapted from t0118's
quintile pattern):

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

1. **Check 1 -- primary stem origin alignment**: `all(close(section.start_xy, origin_xy) for
   section in primary_dends)`. Tolerance 0.1 um.
2. **Check 2 -- parent / child endpoint match**: for each non-primary dendrite section, walk
   the parent chain and assert `child.start_xy == parent.end_xy`. Tolerance 0.1 um.
3. **Check 3 -- synapse pt3d frame consistency**: for each dendrite section, read `h.x3d(mid),
   h.y3d(mid)` from NEURON, assert it lies on the line from `section.start_xy` to
   `section.end_xy` (in Python coords). Lateral deviation threshold 0.1 um.

### Soma-Frame Diagnostic (REQ-7)

An additional diagnostic computes `soma_frame_offset_um` = L2 distance between Python
`origin_xy` and NEURON soma pt3d centroid. If the t0092 z-axis pt3d fix is the source of the
visual artefact, `soma_frame_offset_um == |soma_offset_pd_um|` exactly.

## Metrics

* Cells sampled: **20**.
* Coordinate-consistency checks passed: **60 / 60** (100%).
* Check 1 max error: **0.0 um** across all primary stems of all 20 cells.
* Check 2 max error: **0.0 um** across all non-primary dendrite sections.
* Check 3 max lateral deviation: **19.6 nm** = 1.96e-5 um (float noise; threshold 0.1 um =>
  passes by four orders of magnitude).
* `soma_frame_offset_um` range: **3.02 um -- 149.96 um**; equals `|soma_offset_pd_um|` exactly
  (max residual **0.000000 um** over all 20 cells).

## Visualizations

![Geometry audit gallery — 5x4 panel grid; primary stems highlighted in red linewidth 2.0;
soma circle scaled to `soma_diameter_um / 2`; debug line from `origin_xy` to each primary-stem
tip.](../../../tasks/t0120_morph_generator_geometry_audit/results/images/geometry_audit_gallery.png)

The gallery shows the same 20 cells the audit instrumented. The primary-stem-to-soma
connection is unambiguous in every panel because (a) primary stems are drawn in red at 2x
linewidth, (b) the soma circle is sized to the actual `soma_diameter_um` rather than the fixed
6 px used in t0115's top-50 grid, and (c) a thin grey debug line is drawn from `origin_xy` to
each primary stem's tip so the connection is visible even when the primary stem itself is
short. Compare with
`tasks/t0115_seed9354_no_autostop/results/images/top50_morphologies_seed9354.png` where the
same cells (under different rendering conventions) appear soma-disconnected.

## Analysis

### Why the soma appears disconnected in t0115's grid

The t0115 (and t0112 / t0114 / earlier lineage) `build_top50_morphologies.py` uses three
rendering conventions that conspire to make the soma look disconnected on asymmetric cells:

* `Circle(radius=6.0)` -- fixed soma radius in axis-units (um); on a 300 um panel, 6 um is ~2%
  of the panel width.
* `LineCollection(linewidths=0.4)` -- thin dendrite strokes; primary stems often <30 um long;
  at 0.4 px they nearly vanish.
* Auto-zoom via `ax.set_xlim(cx - half, cx + half)` covering both `geom.soma_xy` and the
  dendrite bounding box; for cells with `|soma_offset_pd_um| > 100` and elongated dendrite
  fields, the panel becomes wide enough that the soma is in one corner and the dendrite tree
  extends to the other.

When the audit re-renders the same cells with `Circle(radius=soma_diameter_um / 2)` (typically
6-9 um, but proportionally sized), `LineCollection(linewidths=0.5-0.6)`, primary stems in
contrasting red `linewidth=2.0`, and a debug line from `origin_xy` to each primary-stem tip,
every panel shows an unambiguous connection.

### The benign two-frame soma split

`tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py` (lines
61-75) calls `h.pt3dclear()` on the soma section and re-emits two pt3d points along the
**z-axis**: `(0, 0, 0, d_target)` and `(0, 0, soma_diameter_um, d_target)`. This was
introduced to fix the t0090 degenerate-zero-area bug where the soma's two pt3d points
coincided in xy and NEURON computed cumulative pt3d distance ~0.

The downstream consequence is two coordinate frames for the soma:

* **Python frame**: `origin_xy = (params.soma_offset_pd_um, 0)` (set by `_apply_asymmetry`).
* **NEURON frame** (pt3d, as the simulator sees it): soma pt3d at `(0, 0, *)` regardless of
  `soma_offset_pd_um`.

This would matter if any electrically-relevant code read the **soma's** NEURON pt3d xy to
compute synaptic arrival times. The audit confirms this never happens:

1. **Synapse placement**: SAC synapses (AChE / GABA / NMDA) are placed only on **dendrite**
   sections in the t0091 / t0118 protocol via `place_synapses` and inherit the dendrite
   section's pt3d midpoint via `_section_midpoint_xy`. Dendrite pt3d is faithfully written in
   the post-asymmetry frame, matching `origin_xy`.
2. **Bar arrival-time projection**: `_bar_arrival_times(syn_xy, origin_xy, direction_deg)` in
   `tasks/t0091_morphology_extended_nsga2_v1/code/trial_helpers.py` projects `(syn_xy -
   origin_xy)` onto the bar direction. Both `syn_xy` and `origin_xy` are in the same Python
   frame; the `soma_offset` term cancels.
3. **Electrical topology**: `sec.connect()` is independent of pt3d xy.

Therefore the two-frame soma split is **deliberate, contained to the soma section, and
electrically benign**.

## Limitations

* The audit instruments 20 of 4431 pooled cells (0.5%). Stratification covers the asymmetry
  parameter extremes and the "worst-looking" set hand-curated from the t0115 PNG; if a
  specific failure mode requires a parameter combination outside the sampled strata, this
  audit would miss it. The 60/60 PASS result with max errors well below thresholds makes this
  risk small.
* The audit verifies geometric consistency, not the **correctness** of the asymmetry transform
  itself (i.e., whether `field_elongation_pd > 1` is the biologically right way to encode PD
  elongation). That is a separate biological-plausibility question; see the t0097
  multi-objective optimisation answer asset.
* The `_section_midpoint_xy` strict implementation raises on `h.n3d() == 0` (degenerate
  sections), unlike the t0091 lineage which silently returns `(0.0, 0.0)`. No cells in the
  sampled set tripped this; if the production code ever passes a degenerate section, the
  audit's strict check would fail where the production code would silently miscompute. Out of
  scope for this audit -- noted as a follow-up suggestion.

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
* `results/data/section_endpoints_dump.json` -- 2.0 MB; per-cell pt3d dump in both Python and
  NEURON frames.
* `results/data/coordinate_consistency_checks.csv` -- 20 rows x 29 columns (3 check pass/fail
  + 5 soma-frame columns + per-check max-error stats + asymmetry parameter values + metadata).
* `results/images/geometry_audit_gallery.png` -- 958 KB; 5x4 panel grid.
* `assets/answer/morphology-generator-geometry-consistency/details.json`, `short_answer.md`,
  `full_answer.md` -- 1 answer asset, confidence high.

## Verification

* `verify_research_code` -- PASSED (0 errors, 0 warnings).
* `verify_plan` -- PASSED (0 errors, 0 warnings).
* Local answer-asset verificator (`meta.asset_types.answer.verificator`) -- PASSED (0 errors,
  0 warnings).
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

</details>
