# ⏹ Morphology generator geometry audit (15-20 cells)

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0120_morph_generator_geometry_audit` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0119_brainstorm_results_23`](../../../overview/tasks/task_pages/t0119_brainstorm_results_23.md) |
| **Task types** | `data-analysis`, `answer-question` |
| **Expected assets** | 1 answer |
| **Task folder** | [`t0120_morph_generator_geometry_audit/`](../../../tasks/t0120_morph_generator_geometry_audit/) |

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
