---
spec_version: "3"
task_id: "t0087_brainstorm_results_17"
step_number: 2
step_name: "discuss-decisions"
status: "completed"
started_at: "2026-05-06T11:10:00Z"
completed_at: "2026-05-06T11:25:00Z"
---
# Step 2 -- Discuss Decisions

## Summary

Three-round structured discussion: Round 1 proposed t0088 (re-cluster 13 Genuine + Marginal cells +
per-cluster Vm-trace deep-dive at 16 directions on local CPU, extension of S-0086-03); Round 2
proposed rejecting S-0086-03 as covered; Round 3 confirmed the decision list. The researcher's
one-shot directive served as the explicit Round 3 confirmation, authorising the entire remaining
lifecycle through PR merge.

## Actions Taken

1. **Round 1 -- New tasks**: proposed t0088 (`recluster_marginals_and_vm_motifs`) bundling two
   phases per researcher directive: Phase A re-clusters the 13-cell pool (6 Genuine + 7 Marginal
   from t0086) on the 54-d natural-unit parameter space using KMeans k=2..6 + hierarchical (ward,
   cosine + euclidean) + UMAP/PCA visualisation, picks best k via silhouette + BIC, computes
   centroids, scores against published biological priors via t0086's scorecard code; Phase B picks
   the cluster representative (closest cell to centroid in Euclidean distance) and runs a
   t0084-style deep-dive at 16 directions (every 22.5 deg) on local CPU, recording per-segment Vm
   + NMDA conductance + Nav1.6 / NaP currents + AIS spike onsets, then computes fractional channel
     attribution; Phase C compares attributions across clusters to issue a mechanism-distinctness
     verdict and produces one answer asset.
2. **Round 1 -- Compute estimate**: pure local-CPU; Phase A ~10 min; Phase B ~32-48 min for 2-3
   representative cells x 16 directions x 60 s each. Total wall-clock ~1-2 hours, $0 cost. No remote
   machine required.
3. **Round 1 -- Dependencies**: t0024, t0078, t0080, t0081 (cell 767 parameter vector), t0083 (cells
   1238-1727 parameter vectors), t0084 (run_deepdive recording pattern), t0086 (biological scorecard
   code, cell classification, original 6-Genuine clustering).
4. **Round 1 -- Task types**: data-analysis (Phase A), experiment-run (Phase B NEURON sims),
   answer-question (Phase C answer asset).
5. **Round 1 -- Source suggestion**: S-0086-03 (extension scope).
6. **Round 2 -- Suggestion cleanup**: proposed rejecting S-0086-03 as covered by t0088 (with
   extended scope: 13-cell pool instead of 6, 16 directions instead of 24, local CPU instead of
   remote). Proposed keeping S-0086-01 (NSGA-II rerun with tightened NMDA bounds, $1.50), S-0086-02
   (NMDA units calibration, $0.30), S-0086-04 (10-rep robustness extension, $0.65), S-0086-05 (RGC
   NaP literature search, $0.10), S-0086-06 (Bed A cross-bed validation, $2.50) active for future
   brainstorms; combined cost $5.05 vs $4.44 remaining means at most one of S-0086-01 / S-0086-06
   fits the remaining budget.
7. **Round 3 -- Confirmation**: the researcher's one-shot directive ("implement S-0086-03 but before
   doing this redo the clustering including marginal cells as well. All in one task.") is the
   explicit confirmation; no separate confirmation prompt needed. Authorises the remaining lifecycle
   including PR push and merge.

## Outputs

* No files produced in this step. Decisions consumed in-process for later application.

## Issues

No issues encountered.
