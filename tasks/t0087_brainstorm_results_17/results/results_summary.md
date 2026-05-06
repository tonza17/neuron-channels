---
spec_version: "1"
task_id: "t0087_brainstorm_results_17"
date_completed: "2026-05-06"
status: "complete"
---
# Results Summary: Brainstorm Session 17

## Summary

Seventeenth strategic brainstorm, run on 2026-05-06 after t0086
(`robustness_cluster_bio_comparison`) classified the 20-cell test set as 6 Genuine + 7 Marginal + 7
Stochastic, found k=2 clusters on the 6 Genuine cells, both clusters classified exotic by the
biological scorecard (NMDA per-synapse +85-122 sigma above Sivyer 2013, NaP +7-24 sigma above Stuart
1999). One consolidated follow-up task commissioned: t0088 (`recluster_marginals_and_vm_motifs`)
extends S-0086-03's per-cluster Vm-trace deep-dive scope by re-clustering the 13-cell pool of 6
Genuine + 7 Marginal cells (instead of 6 Genuine cells only), then runs a t0084-style deep-dive at
16 directions on local CPU on representative cells, computes fractional channel attribution per
cluster, and produces one mechanism-distinctness answer asset. S-0086-03 rejected as covered.
Project budget $20.00; $15.56 spent before t0088; **$4.44 remaining**; t0088 estimated $0 (local-CPU
only) preserves the buffer for subsequent S-0086-* follow-ups.

## Session Overview

Date: 2026-05-06. Triggered by t0086's Genuine + Marginal + Stochastic classification (6 / 7 / 7)
and the k=2 exotic-cluster result. The researcher provided a one-shot directive bundling the
re-clustering and the per-cluster Vm-trace deep-dive into one combined task: "implement S-0086-03
but before doing this redo the clustering including marginal cells as well. All in one task." This
directive is consistent with the recorded researcher preference for one combined task bundling
related suggestions and infra/protocol fixes (memory: feedback_consolidated_task_design). The
session opened with an independent priority reassessment surfacing S-0086-03 as the seed of the new
task and the 13-cell pool (6 Genuine + 7 Marginal) as the natural extension. The directive itself
served as the explicit confirmation, authorising the entire remaining lifecycle.

## Decisions

1. **Create t0088** (`recluster_marginals_and_vm_motifs`). Three sequential phases:

   * **Phase A (re-cluster 13 cells)**: load the 6 Genuine + 7 Marginal cells from t0086's
     `cell_classification.json`. Total 13 cells:
     `[767, 1304, 1379, 1504, 1517, 1559, 1604, 1624, 1634, 1639, 1663, 1677, 1721]`. Load 54-d
     natural-unit parameter vectors per cell from t0083's `all_evaluations.json` (cells 1238-1727)
     and t0081's (cell 767). Re-run KMeans for k=2..6, hierarchical clustering with ward linkage and
     both cosine + euclidean metrics, UMAP / PCA visualisation; pick best k via silhouette + BIC.
     Compute per-cluster centroids in 54-d natural-unit space. Re-use t0086's `biological_priors.py`
     and `biological_scorecard.py` to score each new centroid against published priors.

   * **Phase B (per-cluster Vm-trace deep-dive)**: pick a representative cell per cluster (closest
     to centroid in 54-d Euclidean distance). Run a t0084-style deep-dive at **16 directions**
     (every 22.5 deg). Record per-segment Vm at proximal soma, mid-dendrite, distal-dendrite, AIS;
     per-segment NMDA conductance trajectories; per-segment Nav1.6 / NaP currents at distal
     dendrite; AIS Vm and threshold-crossing spike onset times. Generate 4 figures matching t0084
     per representative cell. Compute fractional channel contributions.

   * **Phase C (mechanism distinctness analysis)**: compare fractional contributions across
     clusters; do clusters use different dominant mechanisms (e.g., NMDA-dominant vs NaP-dominant vs
     Nav1.6-dominant), or share the same mechanism but vary in scale? Compare to t0084's cell 767
     attribution (NaP-dominant 93%, Nav1.6 7%, NMDA 0%). Output: one **answer asset** at
     `assets/answer/are-cluster-motifs-mechanistically-distinct/` with quantitative attribution.

   **Pass criteria**: Primary -- produce a clear mechanism-distinctness verdict. Secondary --
   per-cluster representative Vm-trace deep-dive figures published. Acceptable negative -- clusters
   are NOT mechanistically distinct (all NMDA-dominant differing only in parameter scale) is itself
   a useful finding aligning with t0086's exotic-NMDA verdict.

   **Compute**: Phase A pure data analysis ($0, ~10 min); Phase B per representative cell at 16
   directions x 1 inner replication = 16 NEURON sims at ~60 s each = ~16 min per cell; with 2-3
   cluster representatives = 32-48 min; Phase C analysis ($0). **Local CPU only. No remote machine.
   Total wall-clock ~1-2 hours, $0 cost.**

   Source suggestion: **S-0086-03** (extended scope). Dependencies: t0024, t0078, t0080, t0081,
   t0083, t0084, t0086. `expected_assets = {"answer": 1}`. Task types:
   `["data-analysis", "experiment-run", "answer-question"]`.

2. **Reject S-0086-03** -- t0088 covers the per-cluster Vm-trace deep-dive with extended scope (13
   cells re-clustered, 16 directions instead of 24, mechanism-distinctness narrative as the answer
   asset, local CPU instead of remote). The original S-0086-03 deep-dive scope is fully subsumed by
   t0088's Phase B.

## Metrics

| Metric | Value |
| --- | --- |
| New tasks created | 1 (t0088 recluster + Vm-trace deep-dive) |
| Tasks cancelled | 0 |
| Tasks updated (other than cancellations) | 0 |
| Suggestions rejected | 1 (S-0086-03) |
| Suggestions reprioritised | 0 |
| Corrections written | 1 |
| New suggestions created | 0 |
| Answer assets created in this brainstorm | 0 |
| Session duration | ~50 minutes interactive |
| Session cost | $0.00 |
| Estimated cost of commissioned task | $0.00 (local-CPU only) |

## Verification

* `verify_task_file.py t0087_brainstorm_results_17` -- target 0 errors.
* `verify_corrections.py t0087_brainstorm_results_17` -- target 0 errors for 1 correction file.
* `verify_suggestions.py t0087_brainstorm_results_17` -- target 0 errors (empty array).
* `verify_logs.py t0087_brainstorm_results_17` -- target 0 errors; LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture.
* `verify_task_file.py t0088_recluster_marginals_and_vm_motifs` -- target 0 errors.
* `verify_pr_premerge.py t0087_brainstorm_results_17 --pr-number <N>` -- target 0 errors.

## Next Steps

1. **t0088 execution** is the immediate follow-up: it bundles the re-clustering with the 7 Marginal
   cells included and the per-cluster Vm-trace deep-dive at 16 directions into one combined task.
   Expected wall-clock 1-2 hours local CPU; $0 cost. Output: one mechanism-distinctness answer
   asset.

2. **Decision point after t0088 completes**:
   * If clusters are mechanistically distinct (e.g., NMDA-dominant cluster vs NaP-dominant cluster),
     this confirms biophysical heterogeneity in the v3 substrate Pareto cells and opens two parallel
     follow-ups: ablation of the dominant mechanism per cluster (cheap local-CPU experiments) and
     targeted searches in the biologically-plausible neighbourhood of the non-NMDA-dominant cluster
     (S-0086-01 NSGA-II re-run with tightened NMDA bounds, $1.50).
   * If clusters share a single dominant mechanism (e.g., all NMDA-dominant differing only in
     scale), this aligns with t0086's exotic-NMDA verdict and motivates S-0086-02 (NMDA units
     calibration, $0.30) and S-0086-01 (NSGA-II re-run with tightened NMDA bounds, $1.50) as primary
     follow-ups.

3. **Remaining S-0086-* follow-ups** (kept active for future brainstorms):
   * S-0086-01 (NSGA-II re-run with tightened NMDA bounds, $1.50) -- high priority, fits the $4.44
     buffer
   * S-0086-02 (NMDA units calibration, $0.30) -- high priority, very cheap
   * S-0086-04 (10-rep robustness extension, $0.65) -- medium priority
   * S-0086-05 (RGC-specific NaP literature search, $0.10) -- low priority, very cheap
   * S-0086-06 (Bed A cross-bed validation, $2.50) -- medium priority, fits the buffer alone but not
     alongside S-0086-01

4. **t0075** (Bed A bio-realistic AIS one-axis sweep) remains queued.
