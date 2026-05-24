---
spec_version: "3"
task_id: "t0120_morph_generator_geometry_audit"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-23T23:33:47Z"
completed_at: "2026-05-23T23:42:00Z"
---
# Step 6: Research Code

## Summary

Spawned a `/research-code` subagent that reviewed 14 prior tasks and wrote
`research/research_code.md` (553 lines, 7 mandatory sections). The most consequential finding:
t0092's `morphology_generator_fix.py` patches the soma with pt3d on the **z-axis** at `(0, 0, 0)`
and `(0, 0, soma_diameter_um)`, which **pins the NEURON soma xy at (0, 0)** while Python's
`origin_xy` lives at `(soma_offset, 0)` after `_apply_asymmetry`. Two coordinate frames coexist for
the soma — this is the audit's primary hypothesis to verify.

## Actions Taken

1. Spawned a subagent to execute the `/research-code` skill against task t0120.
2. The subagent enumerated 14 prior tasks (t0008, t0011, t0012, t0090, t0091, t0092, t0099, t0112,
   t0114, t0115, t0117, t0118 plus context tasks), cited 11, and identified 18 library candidates of
   which 2 are directly relevant.
3. The subagent verified the file against `arf/specifications/research_code_specification.md` and
   ran `verify_research_code` -- PASSED with 0 errors / 0 warnings.

## Outputs

* `tasks/t0120_morph_generator_geometry_audit/research/research_code.md`
* `tasks/t0120_morph_generator_geometry_audit/logs/steps/006_research-code/step_log.md`

## Key Findings (carried into planning)

1. **Two coordinate frames for the soma**: t0092 fix re-emits pt3d on z-axis at
   (0,0,0)->(0,0,soma_diameter_um); Python `origin_xy` lives at `(soma_offset, 0)`. The audit must
   check this mismatch.
2. **Dendrite pt3d is in the post-asymmetry frame**: `pt3dadd` faithfully copies
   `(node.start_xy, node.end_xy)`; synapses placed on dendrites read midpoints from the same frame
   as `origin_xy` on the dendrite side.
3. **Electrical topology is `sec.connect()`-based**: independent of xy, so any geometry-frame
   mismatch cannot break electrical correctness. The risk is synaptic arrival timing only.
4. **Visual artefact in rendering**: t0115 renderer uses `section_endpoints_xy` (Python coords)
   consistently; the apparent gap is small soma circle + thin primary stems + auto-zoom on
   asymmetric cells.

## Reusable Assets Identified

* `generate_fixed_morphology` (t0092 fix wrapper) -- direct dependency.
* `_collect_pt3d`, `Pt3dPoint`, `SectionDump`, `CellDump` (t0092 code) -- copy into `code/`.
* `_section_midpoint_xy` (t0091 lineage) -- copy into `code/` with a degenerate-section assertion.
* Stratified quintile sampler (t0118 code) -- adapt to decile-based stratification across asymmetry
  parameters.
* NEURON DLL bypass pattern (t0115 morphology rendering) -- copy.
* Pooled cells parquet (t0117) -- data source for sampling 15-20 cells.

## Issues

No issues encountered. The library and answer aggregator scripts are not present on the current
main; library inventory was discovered via filesystem scan, documented in the subagent's Library
Landscape section.
