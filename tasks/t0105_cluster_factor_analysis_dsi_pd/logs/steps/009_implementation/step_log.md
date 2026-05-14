---
spec_version: "3"
task_id: "t0105_cluster_factor_analysis_dsi_pd"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-14T13:31:41Z"
completed_at: "2026-05-14T14:30:00Z"
---
## Summary

Executed all 15 implementation REQs. Pooled 7,003 cells across 4 lineages, filtered to primary
cohort (N=85 unique cells after dedupe + silence-artifact exclusions) and strict cohort (N=30).
Classified each cell as symmetric or asymmetric (20 sym / 65 asym in primary). Built morphology
gallery (30 cells, stratified). Ran PCA on 54-d electrophys: PC1 strongly separates the two
morphology classes (Mann-Whitney U p = 1.48e-10). Ran varimax factor analysis on full 68-d: 10
factors retained by Kaiser criterion; F1 loads on Ca-K (SK/BK) and Nav channels and is the top
correlate of both DSI (r = -0.32) and PD (r = -0.27); no factor reaches the joint-corner threshold
(|r| > 0.3 on BOTH). Built 2 answer assets, both verifier-clean. Added factor_analyzer
> = 0.5.1 to pyproject.toml.

## Actions Taken

1. Spawned the `/implementation` subagent with detailed plan REQ list.
2. Subagent created 12 Python files in `code/` (load_filter_cells, classify_asymmetry,
   build_gallery, pca_electrophys, factor_analysis, factor_correlations, factor_bootstrap,
   run_strict_cohort, build_metrics_json, paths, constants, schemas).
3. Subagent added `factor_analyzer>=0.5.1` to pyproject.toml (REQ-2) plus a sklearn 1.8 / FA 0.5.1
   compatibility shim documented in factor_analysis.py.
4. Subagent ran the analysis pipeline; produced 16 result data files and 10 PNG charts at DPI 150.
5. Subagent built and verified 2 answer assets (`symmetric-vs-asymmetric-electrophys-cluster` and
   `dsi-pd-diversity-factor-decomposition`); both pass `verify_answer_asset` 0/0.
6. ruff check + ruff format clean; mypy clean.

## Outputs

* 12 files in `code/` (paths, constants, schemas, load+filter, asymmetry classifier, gallery
  builder, PCA, factor analysis, factor correlations, bootstrap, strict cohort runner, metrics
  builder)
* 16 JSON outputs in `results/data/` (selected cells per cohort, asym distribution, PCA results,
  Mann-Whitney, factor loadings/scores/correlations, bootstrap stability, gallery quota table)
* 10 PNG charts at DPI 150 in `results/images/` (asym histogram, morphology gallery, PCA 4-panels
  primary/strict, eigenvalue scree, factor loadings primary/strict, factor correlations
  primary/strict, factor loadings bootstrap)
* `results/metrics.json` (multi-variant, primary + strict cohorts)
* 2 answer assets in `assets/answer/`
* `pyproject.toml`, `uv.lock` updated (top-level allowed change)

## Key Quantitative Findings

* Primary cohort N=85 unique cells; strict cohort N=30 unique cells; 73 silenced-cell artifacts
  excluded across t0091/t0099/t0102 (t0091:5, t0099:23, t0102:45).
* PC1 of 54-d electrophys explains 29.5% of variance; PC2 8.4%; PC3 6.1%.
* Mann-Whitney U on PC1: U=31.00, **p = 1.48e-10** — symmetric and asymmetric cells are cleanly
  separated by their electrophys parameter regime. PC2 p=0.78 (no separation).
* Top PC1 loadings: SK_TERMINAL, BK_TERMINAL, SK_SOMA, BK_MID, NAP_PRIMARY — the asymmetric vs
  symmetric morphology distinction is mirrored by Ca-activated K-channel densities.
* Factor analysis: 10 factors retained (Kaiser eigenvalues > 1 capped at 10). F1 loads on
  NAP_PRIMARY (+0.75), morph_seed (+0.68), SK_MID (+0.66), MG_CONC_MM (+0.65), RA_OHM_CM (+0.65).
* Top factors for DSI: F1 (r = -0.322, p = 0.003), F3, F5.
* Top factors for PD: F1 (r = -0.265, p = 0.014), F3, F10.
* **No joint DSI-PD factor** (no factor passes |r| > 0.3 on BOTH outcomes simultaneously).
* Bootstrap (200 resamples): F1 and F2 are stable (median |λ| > 0.4 + 90% sign-consistent); F3-F10
  unstable at N=85.
* Strict cohort (N=30) reproduces PC1 class separation (p = 8.23e-5) but factor analysis loses
  power.

## Issues

REQ-13 (charts embedded in results_detailed.md) is marked partial in the subagent's report — this
is normal because results_detailed.md is written by the orchestrator's `results` step (step 12), not
by the implementation subagent. The charts are saved at the correct paths ready for the results
step.
