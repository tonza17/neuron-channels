---
spec_version: "1"
task_id: "t0120_morph_generator_geometry_audit"
date_completed: "2026-05-24"
status: "complete"
---
# Results Summary: Morphology Generator Geometry Audit

## Summary

Audited the procedural DSGC morphology generator on 20 cells stratified across asymmetry-parameter
extremes plus symmetric controls. All three coordinate-consistency checks pass for every cell
(60/60). The deliberate soma-frame split introduced by the t0092 z-axis pt3d patch is **benign**;
prior 68-d morphology-extended NSGA-II results (t0091, t0099, t0102, t0104, t0106, t0112-t0115,
t0118) are NOT invalidated. The visual disconnect in t0115's top-50 morphology grid is a
rendering-only artefact. **t0122_dsi_cytoplasm_volume_nsga2 is unblocked.**

## Metrics

* **Cells sampled**: **20** across 7 strata (SOMA_OFFSET_TOP 3, ELONGATION_TOP 2, ELONGATION_BOTTOM
  1, BRANCH_DENSITY_TOP 3, PRIMARY_CONCENTRATION_TOP 3, WORST_LOOKING 4, SYMMETRIC_CONTROL 4) from
  the t0117 pooled parquet (4431 cells, seeds 44/77/7755/9354).
* **Coordinate-consistency checks passed**: **60 / 60** (3 checks per cell x 20 cells).
* **Check 1 max error** (primary stem start_xy vs origin_xy): **0.0 um** across all primary stems of
  all 20 cells.
* **Check 2 max error** (child start_xy vs parent end_xy): **0.0 um** across all non-primary
  dendrite sections.
* **Check 3 max lateral deviation** (NEURON midpoint pt3d vs Python section line on dendrites):
  **19.6 nm** (1.96e-5 um) -- pure float-arithmetic noise, **four orders below the 0.1 um audit
  threshold**.
* **soma_frame_offset_um range**: **3.02 um** (symmetric controls) to **149.96 um** (extreme
  soma_offset_pd_um cells); exactly equals `|soma_offset_pd_um|` per cell (max residual **0.000000
  um**).
* **Files produced**: 1 answer asset, 1 PNG gallery (958 KB, 5x4 grid), 1 per-cell pass/fail CSV, 1
  2.0-MB section-endpoints JSON forensic dump, 9 Python source files.

## Verification

* `verify_research_code` -- PASSED (0 errors, 0 warnings).
* `verify_plan` -- PASSED (0 errors, 0 warnings).
* Local answer-asset verification (`meta.asset_types.answer.verificator`) -- PASSED (0 errors, 0
  warnings).
* `ruff check`, `ruff format`, `mypy -p tasks.t0120_morph_generator_geometry_audit.code` -- all
  PASSED on 10 task code files.
* Per-cell pass/fail (`coordinate_consistency_checks.csv`): 60 / 60 PASS, 0 FAIL.

## Verdict

**Rendering-only artefact.** No NSGA-II re-runs needed. Prior 68-d morphology-extended NSGA-II
lineage (t0091, t0099, t0102, t0104, t0106, t0112, t0114, t0115, t0118) remains valid. The
brainstorm-session-23 gating condition for `t0122_dsi_cytoplasm_volume_nsga2` is satisfied; that
task may now proceed.
