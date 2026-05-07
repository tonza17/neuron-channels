---
spec_version: "1"
task_id: "t0089_brainstorm_results_18"
date_completed: "2026-05-07"
status: "complete"
---
# Results Summary: Brainstorm Session 18

## Summary

Eighteenth strategic brainstorm, run on 2026-05-07 after t0088 (`recluster_marginals_and_vm_motifs`)
extended t0086's biological-plausibility analysis to a 13-cell pool and confirmed
`shared_mechanism_different_scale` across 4 clusters (all NaP-dominant in PD-minus-ND attribution).
The researcher's strategic directive was a pivot from electrophys-only optimisation (t0080-t0088) to
**morphology-extended optimisation**: "Optimisation technique seems to work. We now need to add a
big and important part of cells - cell morphology." After four iterations on parametrisation
strategy, the agreed approach is a procedural DSGC morphology generator with 14 explicit knobs
spanning topology + asymmetry + geometry, called inside the NSGA-II evaluation loop. The work is
split into two tasks: t0090 (`morphology_generator_diversity_test`, ~$0.30, ~3-4 days local) builds
and validates the generator with 30 different + 30 similar morphologies and bundles three validation
suggestions; t0091 (`morphology_extended_nsga2_v1`, ~$3.00-3.50, ~14-16 hours Vast.ai) runs the
first joint 68-d NSGA-II with 5-anchor warm-start (Bed-B-like + symmetric + PD-asymmetric
+ ND-asymmetric + alt-topology). Cleaned 5 covered / duplicate suggestions and reprioritised 3 high
  suggestions to medium. Project budget $20.00; $15.56 spent; **$4.44 remaining** before t0090 /
  t0091; estimated **$0.94-1.44 buffer remaining** after both tasks complete.

## Session Overview

Date: 2026-05-07. Triggered by t0088's `shared_mechanism_different_scale` verdict (all 4 clusters
NaP-dominant) and the surfacing of cluster 1's AIS-to-soma Nav ratio = 116x as the most extreme
single-prior violation in the project. The researcher provided an explicit strategic-pivot directive
to add cell morphology to the optimisation. The session went through four iterations on
parametrisation strategy:

1. Option A (tier-based geometric scaling, 8 params) -- rejected by researcher: "It has to reflect
   branching morphology and also asymmetry etc. Think more."
2. Option H (procedural generator with 14 DS-relevant knobs spanning topology + asymmetry +
   geometry) -- proposed in response to feedback.
3. Architectural-clarification round 1 ("why can't we incorporate generation of neurons into the
   optimisation?") -- confirmed that in-loop generation is the architecture.
4. Architectural-clarification round 2 ("wait, I still don't understand. Why don't we generate
   morphologies during optimisation? Or is it what you propose?") -- explicitly contrasted the
   proposed in-loop architecture against alternatives, walked through per-evaluation pseudocode.

The researcher then specified the two-task split: "Let's split it into two tasks. 1 - write and test
generator - generate and visualise say 30 random very different morphologies and 30 very similar
ones. ... And then second task - first optimisation attempt. Use one seed that we currently have
(WITH MORPHOLOGY SIMILAR TO WHAT WE HAVE) and few more very different seeds - symmetric and
asymmetric." Pushed back on a 3-4 day Phase A estimate ("Why phase A takes 4 days?"); revised
honestly to ~1.5-2 days based on a sub-step breakdown. Final confirmation: "all approved. fire away"
-- the explicit Phase 2 Round 3 confirmation authorising the entire remaining lifecycle including
push, PR, premerge, and merge.

## Decisions

1. **Create t0090** (`morphology_generator_diversity_test`). Seven phases:

   * **Phase A (generator implementation)**: implement procedural generator in Python emitting
     NEURON sections + connectivity, deterministic given (`params`, `morph_seed`); 14 parameters
     spanning 5 topology (`num_primary_branches` 3-7, `branch_prob_per_um` 0.005-0.05,
     `max_strahler_depth` 2-6, `mean_branching_angle_deg` 30-90, `rall_exponent` 0.5-2.0); 4
     asymmetry (`soma_offset_pd_um` -150 to +150, `field_elongation_pd` 1.0-3.0,
     `branch_density_gradient_pd` -1 to +1, `primary_branch_pd_concentration` 0-5 von Mises kappa);
     3 geometry (`mean_segment_length_um` 10-60, `soma_diameter_um` 8-18, `ais_length_um` 15-60); 2
     stochastic control (`morph_seed`, `branch_length_cv` 0-0.5).
   * **Phase B (30 very-different morphologies)**: wide LHS over 14-d morph space, parallel on
     64-core EPYC.
   * **Phase C (30 very-similar morphologies)**: tight +/- 5 percent perturbations around a
     Bed-B-equivalent base point, parallel on 64 cores.
   * **Phase D (verification simulation)**: build each morphology in NEURON, run 50 ms no-stim
     stability + 8-direction bar protocol with default t0083 best-cell channels; catch NaN /
     divergence / disconnected sections.
   * **Phase E (visualisation)**: 2D dendrograms for all 60 morphologies; PCA / UMAP of morphometric
     features; side-by-side panels of 30-different vs 30-similar.
   * **Phase F (Bed-B reproducibility)**: 5 t0083 Pareto cells through the generator at the
     Bed-B-equivalent point, DSI / PD within 5 percent.
   * **Phase G (validation bundle)**: bundle covering S-0088-02 (AIS-to-soma Nav ratio audit),
     S-0086-02 (NMDA units calibration ablation), S-0088-01 (causal NaP-knockout per cluster
     representative). One synthesis answer asset.

   Pass criteria: generator deterministic; 60 / 60 morphologies simulate; "different" set covers
   visibly distinct morphology classes; "similar" set produces tight PCA cluster; Bed-B
   reproducibility within 5 percent; all 3 validation suggestions answered.

   Source suggestions: covers S-0088-02 + S-0086-02 + S-0088-01. Dependencies: t0024, t0078, t0080,
   t0081, t0083, t0086, t0088. `expected_assets = {"library": 1, "answer": 1}`. Task types
   `["write-library", "data-analysis", "answer-question"]`.

   **Cost ~$0.30, ~3-4 days wall-clock, mostly local 64-core CPU.**

2. **Create t0091** (`morphology_extended_nsga2_v1`). Five phases:

   * **Phase A (warm-start population)**: pop 96 = 5 anchors x ~19 t0083 Pareto electrophys variants
     per anchor + 1 random sample. Anchors: (1) Bed-B-like; (2) symmetric; (3) PD-asymmetric (soma
     offset +100 um, field elongated 2x along PD); (4) ND-asymmetric (mirror of #3); (5) alternative
     topology.
   * **Phase B (joint NSGA-II)**: pop 96 x <=8 generations, generator inside eval loop, adaptive
     HV-plateau stop, $4.00 cost watchdog. Vast.ai EPYC 7B13.
   * **Phase C (Pareto + biological-plausibility analysis)**: extend t0086 / t0088 framework to 68-d
     cells; do morph-extended cells reach biologically-plausible NMDA / NaP regimes?
   * **Phase D (anchor-tracking analysis)**: which anchors over- vs under-represented in final
     Pareto? PD- vs ND-asymmetric preservation as evidence for soma-displacement-toward-PD as DS
     mechanism.
   * **Phase E (answer asset)**: morphology-extension biological plausibility synthesis.

   Pass criteria: HV plateau or 8-gen cap reached; 68-d Pareto with at least 8 cells; definitive
   anchor-tracking table with bootstrap p-values; definitive yes/no on biological plausibility.

   Source suggestion: none directly (new direction). Dependencies: t0024, t0078, t0080, t0081,
   t0083, t0086, t0088, t0090. `expected_assets = {"answer": 1, "predictions": 1}`. Task types
   `["experiment-run", "data-analysis", "answer-question"]`.

   **Cost ~$3.00-3.50, ~14-16 hours wall-clock, Vast.ai EPYC 7B13.**

3. **Reject 5 suggestions** (all covered or duplicate):
   * **S-0086-02** (NMDA units calibration) -- covered by t0090 Phase G.
   * **S-0088-01** (causal NaP-knockout per cluster representative) -- covered by t0090 Phase G.
   * **S-0088-02** (AIS-to-soma Nav ratio audit) -- covered by t0090 Phase G.
   * **S-0084-05** (channel-knockout DSI causal-attribution variant) -- duplicate of S-0088-01.
   * **S-0083-03** (per-direction Vm-trace deep-dive of cell 1304) -- covered by t0088 cluster 1
     attribution (cell 1304 is in cluster 1, mechanism NaP-dominant).

4. **Reprioritise 3 suggestions high -> medium**:
   * **S-0083-01** (NSGA-II to gen 25 with pop 144, $8-12) -- out-of-budget; superseded by
     morphology-extended NSGA-II direction.
   * **S-0084-01** (NaP density sweep on cells 767 / 637 / 762) -- superseded by S-0088-01-style
     binary knockout in t0090 Phase G; older single-cell scope.
   * **S-0084-02** (per-seed mechanism decomposition of cell 767) -- superseded by population- level
     mechanism attribution from t0088; older single-cell scope.

5. **Stays high**:
   * **S-0086-01** (NSGA-II re-run with tightened NMDA bounds, $1.50) -- post-t0091 follow-up.
   * **S-0070-01** (harmonise PD / ND encoding across Bed A and Bed B) -- independent infra.

## Metrics

| Metric | Value |
| --- | --- |
| New tasks created | 2 (t0090 generator + diversity test, t0091 first joint NSGA-II) |
| Tasks cancelled | 0 |
| Tasks updated (other than cancellations) | 0 |
| Suggestions rejected | 5 (S-0086-02, S-0088-01, S-0088-02, S-0084-05, S-0083-03) |
| Suggestions reprioritised | 3 (S-0083-01, S-0084-01, S-0084-02 high -> medium) |
| Corrections written | 8 (5 rejections + 3 reprioritisations) |
| New suggestions created | 0 |
| Answer assets created in this brainstorm | 0 |
| Session duration | ~90 minutes interactive |
| Session cost | $0.00 |
| Estimated cost of commissioned tasks | $3.30-3.80 (t0090 ~$0.30 + t0091 ~$3.00-3.50) |

## Verification

* `verify_task_file.py t0089_brainstorm_results_18` -- target 0 errors.
* `verify_corrections.py t0089_brainstorm_results_18` -- target 0 errors for 8 correction files.
* `verify_suggestions.py t0089_brainstorm_results_18` -- target 0 errors (empty array).
* `verify_logs.py t0089_brainstorm_results_18` -- target 0 errors; LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture.
* `verify_task_file.py t0090_morphology_generator_diversity_test` -- PASSED with 0 errors.
* `verify_task_file.py t0091_morphology_extended_nsga2_v1` -- PASSED with 0 errors.
* `verify_pr_premerge.py t0089_brainstorm_results_18 --pr-number <N>` -- target 0 errors.

## Next Steps

1. **t0090 execution** is the immediate follow-up: generator implementation + 30 different + 30
   similar morphologies + visualisation + Bed-B reproducibility + validation triplet bundle.
   Expected wall-clock ~3-4 days, mostly local 64-core CPU; ~$0.30 cost. Output: validated generator
   library + curated warm-start anchor archive for t0091 + 1 mechanism-distinctness answer asset on
   the validation triplet.

2. **t0091 execution** follows t0090 completion: first joint 68-d NSGA-II with morphology generator
   inside eval loop and 5-anchor warm-start. Expected wall-clock ~14-16 hours Vast.ai; ~$3.00-3.50
   cost. Output: 68-d Pareto-front predictions asset + biological-plausibility answer asset.

3. **Decision point after t0091 completes**:
   * If morphology extension opens biologically-plausible joint-pass cells (any cell scoring
     "plausible" or "stretched" on all 9 priors simultaneously), this confirms morphology as a
     functional DS mechanism on top of the channel mechanism; opens cross-bed validation follow-ups
     (S-0070-01 PD / ND encoding harmonisation; Bed A morphology-extended NSGA-II).
   * If anchor 3 (PD-asymmetric) is preserved more than anchor 4 (ND-asymmetric), this is strong
     evidence for soma-displacement-toward-PD as a functional DS mechanism (Schachter 2010, Trenholm
     2013).
   * If morphology pegs at near-Bed-B defaults across the entire Pareto, motivates Option G
     (NeuroMorpho real-cell library + categorical selector + parametric deformation) as a future
     task.

4. **Remaining S-0086-* / S-0070-* follow-ups** (kept active for future brainstorms):
   * **S-0086-01** (NSGA-II re-run with tightened NMDA bounds, $1.50) -- high priority, fits the
     ~$0.94-1.44 buffer if t0091 negative result motivates revisiting 54-d search.
   * **S-0070-01** (harmonise PD / ND encoding across Bed A and Bed B) -- high priority, infra work;
     not affected by morphology direction.
   * **S-0086-04** (10-rep robustness extension, $0.65) -- medium priority.
   * **S-0086-05** (RGC-specific NaP literature search, $0.10) -- low priority.
   * **S-0086-06** (Bed A cross-bed validation, $2.50) -- medium priority.

5. **t0075** (Bed A bio-realistic AIS one-axis sweep) remains queued.
